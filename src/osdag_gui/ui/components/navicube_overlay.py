"""
navicube_overlay.py  —  FreeCAD-style NaviCube Overlay for Osdag
═════════════════════════════════════════════════════════════════
Pure PySide6 2-D rendering  ·  zero OCC dependency in this widget
Smooth SLERP camera animation  ·  FreeCAD-style visual

Sign-convention contract (critical — do not change)
────────────────────────────────────────────────────
  _dir  = inward camera direction = OCC cam.Direction() = eye → scene.

  This matches what the projection math and face-visibility check both
  require.  When we emit to OCC's SetProj we negate (_dir → outward)
  because SetProj(Vx,Vy,Vz) places the eye in the +V direction.

  Mnemonic:  read inward,  write outward.

Flicker cause & fix
───────────────────
  The previous slot called FitAll() on the first animation frame, which
  reset zoom mid-flight every time a face was clicked — that jump IS the
  "flicker".  We now call FitAll once AFTER the full animation completes
  (flagged via _needs_fit_after_anim) so zoom correction happens exactly
  once, after the cube has settled.

Antipodal SLERP
───────────────
  dot(v0,v1) ≈ -1 → sin(ω) → 0 → division by zero → NaN → OCC crash.
  Fixed by routing through a stable perpendicular midpoint.
"""

import math
import numpy as np
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore    import Qt, QPointF, Signal, QRectF, QTimer
from PySide6.QtGui     import (
    QPainter, QColor, QPolygonF, QFont, QPen, QBrush,
    QTransform, QCursor, QPainterPath,
)

# ═══════════════════════════════════════════════════════════════════════
#  Math helpers
# ═══════════════════════════════════════════════════════════════════════

def _norm(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 1e-10 else v

def _rod(v: np.ndarray, axis: np.ndarray, ang: float) -> np.ndarray:
    """Rodrigues rotation of v around unit-axis by ang radians."""
    a = _norm(np.asarray(axis, dtype=float))
    c, s = math.cos(ang), math.sin(ang)
    return v * c + np.cross(a, v) * s + a * float(np.dot(a, v)) * (1.0 - c)

def _vslerp(v0: np.ndarray, v1: np.ndarray, t: float) -> np.ndarray:
    """
    Spherical-linear interpolation.  Handles antipodal case (dot ≈ -1)
    that causes sin(ω)→0 → NaN → OCC V3d_BadValue crash.
    """
    v0 = _norm(np.asarray(v0, dtype=float))
    v1 = _norm(np.asarray(v1, dtype=float))
    d  = float(np.clip(np.dot(v0, v1), -1.0, 1.0))

    if d > 0.9999:
        return _norm(v0 + t * (v1 - v0))

    if d < -0.9999:                   # antipodal — route through perpendicular
        cand = np.array([1.,0.,0.]) if abs(v0[0]) < 0.9 else np.array([0.,1.,0.])
        mid  = _norm(np.cross(v0, cand))
        return _vslerp(v0, mid, t*2.) if t < 0.5 else _vslerp(mid, v1, (t-.5)*2.)

    omega = math.acos(d)
    s_o   = math.sin(omega)
    return (math.sin((1.-t)*omega)/s_o)*v0 + (math.sin(t*omega)/s_o)*v1

def _smooth(t: float) -> float:
    t = max(0., min(1., t))
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


# ═══════════════════════════════════════════════════════════════════════
#  Palette
# ═══════════════════════════════════════════════════════════════════════

class _Pal:
    def __init__(self, light: bool):
        if light:
            self.f_main = QColor(230, 230, 234)   # 6 main faces — bright
            self.f_edge = QColor(186, 186, 191)   # 12 edge chamfers
            self.f_corn = QColor(160, 160, 165)   # 8 corner triangles
            self.text   = QColor(18,  18,  18)
            self.bord   = QColor(82,  82,  88)
            self.bord_s = QColor(125, 125, 131)
            self.ctrl   = QColor(186, 186, 192, 120)
            self.ctrl_r = QColor(105, 105, 110, 170)
            self.hover  = QColor(0,   148, 255, 235)
            self.hov_tx = QColor(255, 255, 255)
            self.dot    = QColor(195, 195, 198, 225)
            self.shadow = QColor(0,   0,   0,   42)
        else:
            self.f_main = QColor(88,  88,  92)
            self.f_edge = QColor(65,  65,  69)
            self.f_corn = QColor(50,  50,  54)
            self.text   = QColor(238, 238, 238)
            self.bord   = QColor(20,  20,  24)
            self.bord_s = QColor(45,  45,  49)
            self.ctrl   = QColor(78,  78,  82,  125)
            self.ctrl_r = QColor(42,  42,  46,  175)
            self.hover  = QColor(0,   148, 255, 235)
            self.hov_tx = QColor(255, 255, 255)
            self.dot    = QColor(145, 145, 148, 225)
            self.shadow = QColor(0,   0,   0,   78)


# ═══════════════════════════════════════════════════════════════════════
#  Widget
# ═══════════════════════════════════════════════════════════════════════

class NaviCubeOverlay(QWidget):
    """
    FreeCAD-style NaviCube overlay.

    Signal: viewOrientationRequested(dx, dy, dz, ux, uy, uz)
        dx/dy/dz = outward direction  (ready for OCC SetProj)
        ux/uy/uz = camera up vector   (ready for OCC SetUp)
    """

    viewOrientationRequested = Signal(float, float, float, float, float, float)

    # ── tuneable ─────────────────────────────────────────────────────
    _SIZE  = 216          # widget side in px
    _SCALE = 43.0         # 3-D units → screen pixels
    _C     = 0.74         # chamfer inner half-size (larger = bigger main faces)
    _AMS   = 360          # animation duration ms
    _VIS   = 0.10         # face-visibility dot-product threshold
    _STEP  = math.radians(15)
    _TICK_MS = 16
    _IDLE_POLL_FRAMES = 2
    _SYNC_EPS = 1e-3
    # ISO inward direction: camera is at (+X,−Y,+Z) → inward = (−X,+Y,−Z)
    _DDEF  = _norm(np.array([-1., 1., -1.]))
    _UDEF  = np.array([0., 0.,  1.])
    _LIGHT = _norm(np.array([-0.8, -1.0, -1.8]))   # Lambertian light dir

    def __init__(self, cad_widget, parent=None):
        super().__init__(parent)
        self.cad_widget = cad_widget
        self.setFixedSize(self._SIZE, self._SIZE)
        self.setMouseTracking(True)
        self.setWindowFlags(
            Qt.Tool
            | Qt.FramelessWindowHint
            | Qt.NoDropShadowWindowHint
            | Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setAutoFillBackground(False)

        self.hovered_id: str | None = None

        # _dir = INWARD (eye→scene), same convention as OCC cam.Direction()
        self._dir = self._DDEF.copy()
        self._up  = self._UDEF.copy()

        # animation
        self._at    = 1.0
        self._adt   = 16.0 / self._AMS
        self._d0    = self._dir.copy()
        self._u0    = self._up.copy()
        self._d1: np.ndarray | None = None
        self._u1: np.ndarray | None = None
        self._needs_fit = False   # set True so FitAll fires once after anim

        # idle-sync cooldown: skip _read_cam for N frames after animation ends
        self._cooldown = 0
        self._pending_sync = True
        self._idle_frames = 0

        self._build_geo()
        self._build_ctrl()

        self._tmr = QTimer(self)
        self._tmr.timeout.connect(self._tick)
        self._tmr.start(self._TICK_MS)

    # ──────────────────────────── geometry ──────────────────────────

    def _build_geo(self):
        c = self._C
        raw = {
            'ZTR':( c, c, 1), 'ZTL':(-c, c, 1), 'ZBL':(-c,-c, 1), 'ZBR':( c,-c, 1),
            'ZTRb':( c, c,-1),'ZTLb':(-c, c,-1),'ZBLb':(-c,-c,-1),'ZBRb':( c,-c,-1),
            'YTR':( c, 1, c),'YTL':(-c, 1, c),'YBL':(-c, 1,-c),'YBR':( c, 1,-c),
            'YTRf':( c,-1, c),'YTLf':(-c,-1, c),'YBLf':(-c,-1,-c),'YBRf':( c,-1,-c),
            'XTR':( 1, c, c),'XTL':( 1, c,-c),'XBL':( 1,-c,-c),'XBR':( 1,-c, c),
            'XTRl':(-1, c, c),'XTLl':(-1, c,-c),'XBLl':(-1,-c,-c),'XBRl':(-1,-c, c),
        }
        V = {k: np.array(v, dtype=float) for k, v in raw.items()}

        defs = [
            # name           verts                            normal     label    type
            ('TOP',   ['ZBR','ZTR','ZTL','ZBL'],         ( 0, 0, 1), 'TOP',   'main'),
            ('BOTTOM',['ZTRb','ZBRb','ZBLb','ZTLb'],     ( 0, 0,-1), 'BOTTOM','main'),
            ('FRONT', ['YBRf','YTRf','YTLf','YBLf'],     ( 0,-1, 0), 'FRONT', 'main'),
            ('BACK',  ['YTR','YBR','YBL','YTL'],          ( 0, 1, 0), 'BACK',  'main'),
            ('RIGHT', ['XBR','XTR','XTL','XBL'],          ( 1, 0, 0), 'RIGHT', 'main'),
            ('LEFT',  ['XBLl','XTLl','XTRl','XBRl'],     (-1, 0, 0), 'LEFT',  'main'),
            ('TF', ['ZBR','ZBL','YTLf','YTRf'],           ( 0,-1, 1), None, 'edge'),
            ('TB', ['ZTL','ZTR','YTR','YTL'],              ( 0, 1, 1), None, 'edge'),
            ('TR', ['ZTR','ZBR','XBR','XTR'],              ( 1, 0, 1), None, 'edge'),
            ('TL', ['ZBL','ZTL','XTRl','XBRl'],           (-1, 0, 1), None, 'edge'),
            ('BF', ['ZBLb','ZBRb','YBRf','YBLf'],         ( 0,-1,-1), None, 'edge'),
            ('BB', ['ZTRb','ZTLb','YBL','YBR'],            ( 0, 1,-1), None, 'edge'),
            ('BR', ['ZBRb','ZTRb','XTL','XBL'],            ( 1, 0,-1), None, 'edge'),
            ('BL', ['ZTLb','ZBLb','XBLl','XTLl'],         (-1, 0,-1), None, 'edge'),
            ('FR', ['YTRf','YBRf','XBL','XBR'],            ( 1,-1, 0), None, 'edge'),
            ('FL', ['YBLf','YTLf','XBRl','XBLl'],         (-1,-1, 0), None, 'edge'),
            ('BKR',['YBR','YTR','XTR','XTL'],              ( 1, 1, 0), None, 'edge'),
            ('BKL',['YTL','YBL','XTLl','XTRl'],           (-1, 1, 0), None, 'edge'),
            ('TFR',['ZBR','YTRf','XBR'],                   ( 1,-1, 1), None, 'corner'),
            ('TFL',['ZBL','XBRl','YTLf'],                  (-1,-1, 1), None, 'corner'),
            ('TBR',['ZTR','XTR','YTR'],                    ( 1, 1, 1), None, 'corner'),
            ('TBL',['ZTL','YTL','XTRl'],                   (-1, 1, 1), None, 'corner'),
            ('BFR',['ZBRb','XBL','YBRf'],                  ( 1,-1,-1), None, 'corner'),
            ('BFL',['ZBLb','YBLf','XBLl'],                 (-1,-1,-1), None, 'corner'),
            ('BBR',['ZTRb','YBR','XTL'],                   ( 1, 1,-1), None, 'corner'),
            ('BBL',['ZTLb','XTLl','YBL'],                  (-1, 1,-1), None, 'corner'),
        ]

        self._faces: dict = {}
        for nm, vkeys, nrm, lbl, ft in defs:
            pts = [V[k] for k in vkeys]
            n   = _norm(np.array(nrm, dtype=float))
            ctr = np.mean(pts, axis=0)
            u_  = _norm(pts[0]-ctr);  v_ = np.cross(n, u_)
            pts = sorted(pts, key=lambda p: math.atan2(
                float(np.dot(p-ctr, v_)), float(np.dot(p-ctr, u_))))
            self._faces[nm] = {'pts':pts, 'n':n, 'ctr':ctr, 'lbl':lbl, 'ft':ft}

    def _build_ctrl(self):
        cx = cy = self._SIZE / 2
        AR = round(self._SIZE * 0.35)
        hs = max(8, round(self._SIZE * 0.052))
        roll_dx = round(self._SIZE * 0.23)
        roll_dy = round(self._SIZE * 0.21)
        dot_dx = round(self._SIZE * 0.31)
        dot_dy = round(self._SIZE * 0.245)
        mini_dx = round(self._SIZE * 0.30)
        mini_dy = round(self._SIZE * 0.30)
        dot_r = max(6, round(self._SIZE * 0.035))
        mini_r = max(12, round(self._SIZE * 0.065))
        def tri(x,y,d):
            if d=='U': return [(x,y-hs),(x-hs,y+hs),(x+hs,y+hs)]
            if d=='D': return [(x,y+hs),(x+hs,y-hs),(x-hs,y-hs)]
            if d=='L': return [(x-hs,y),(x+hs,y-hs),(x+hs,y+hs)]
            if d=='R': return [(x+hs,y),(x-hs,y+hs),(x-hs,y-hs)]
        self._ctrl: dict = {
            'AU':{'poly':tri(cx,    cy-AR,'U'),'act':'orbit_u'},
            'AD':{'poly':tri(cx,    cy+AR,'D'),'act':'orbit_d'},
            'AL':{'poly':tri(cx-AR, cy,  'L'),'act':'orbit_l'},
            'AR':{'poly':tri(cx+AR, cy,  'R'),'act':'orbit_r'},
            'RL':{'type':'arc','cx':cx-roll_dx,'cy':cy-roll_dy,'cw':False,'act':'roll_ccw'},
            'RR':{'type':'arc','cx':cx+roll_dx,'cy':cy-roll_dy,'cw':True, 'act':'roll_cw'},
            'HM':{'type':'dot',  'cx':cx+dot_dx,'cy':cy-dot_dy,'r':dot_r,  'act':'home'},
            'MC':{'type':'mcube','cx':cx+mini_dx,'cy':cy+mini_dy,'r':mini_r,'act':'home'},
        }

    # ──────────────────────────── camera ────────────────────────────

    def _read_cam(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Read live OCC camera.
        cam.Direction() = inward (eye→scene) — use directly, no negation.
        """
        try:
            cam = self.cad_widget.view.Camera()
            cd, cu = cam.Direction(), cam.Up()
            d = _norm(np.array([cd.X(), cd.Y(), cd.Z()], dtype=float))  # inward
            u = _norm(np.array([cu.X(), cu.Y(), cu.Z()], dtype=float))
            return d, u
        except Exception:
            return self._dir.copy(), self._up.copy()

    def _axes(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return (D_inward, U, R).  R and U re-orthogonalised each call."""
        D = self._dir
        U = self._up
        R = _norm(np.cross(D, U))
        U = _norm(np.cross(R, D))
        return D, U, R

    def _set_camera_state(self, d: np.ndarray, u: np.ndarray) -> bool:
        d = _norm(np.asarray(d, dtype=float))
        u = _norm(np.asarray(u, dtype=float))
        r = np.cross(d, u)
        u = _norm(np.cross(r, d))

        if (
            np.linalg.norm(d - self._dir) <= self._SYNC_EPS
            and np.linalg.norm(u - self._up) <= self._SYNC_EPS
        ):
            return False

        self._dir = d
        self._up = u
        return True

    def request_sync(self):
        self._pending_sync = True

    # ──────────────────────────── animation ─────────────────────────

    def _start_anim(self, tgt_dir: np.ndarray, tgt_up: np.ndarray,
                    fit_after: bool = False):
        self._d0 = self._dir.copy()
        self._u0 = self._up.copy()
        self._d1 = _norm(np.asarray(tgt_dir, dtype=float))
        self._u1 = _norm(np.asarray(tgt_up,  dtype=float))
        self._at = 0.0
        self._needs_fit = fit_after
        self._pending_sync = False
        self._idle_frames = 0

    def _tick(self):
        needs_update = False
        if self._at < 1.0:
            # ── animating ───────────────────────────────────────────
            self._at = min(1.0, self._at + self._TICK_MS / self._AMS)
            te = _smooth(self._at)
            d  = _vslerp(self._d0, self._d1, te)
            u  = _vslerp(self._u0, self._u1, te)
            R  = np.cross(d, u);  u = _norm(np.cross(R, d))
            self._dir, self._up = d, u
            needs_update = True

            # Emit outward (−d) for OCC SetProj
            if np.linalg.norm(d) > 1e-6 and np.linalg.norm(u) > 1e-6:
                self.viewOrientationRequested.emit(
                    -float(d[0]), -float(d[1]), -float(d[2]),
                     float(u[0]),  float(u[1]),  float(u[2]))

            if self._at >= 1.0:
                # Animation just finished — tell the viewer to FitAll once
                self._cooldown = 8   # skip _read_cam for 8 frames (~130 ms)
                if self._needs_fit:
                    self._needs_fit = False
                    self.viewOrientationRequested.emit(
                        -float(self._dir[0]), -float(self._dir[1]), -float(self._dir[2]),
                         float(self._up[0]),   float(self._up[1]),   float(self._up[2]))

        else:
            # ── idle: sync passively from OCC ───────────────────────
            if self._cooldown > 0:
                self._cooldown -= 1
            else:
                self._idle_frames += 1
                if self._pending_sync or self._idle_frames >= self._IDLE_POLL_FRAMES:
                    self._pending_sync = False
                    self._idle_frames = 0
                    d, u = self._read_cam()
                    needs_update = self._set_camera_state(d, u)

        if needs_update:
            self.update()

    # ──────────────────────────── projection ────────────────────────

    def _proj(self, P, R, U, cx, cy) -> QPointF:
        S = self._SCALE
        return QPointF(cx + float(np.dot(P,R))*S,
                       cy - float(np.dot(P,U))*S)

    # ═══════════════════════════════════════════════════════════════
    #  Paint
    # ═══════════════════════════════════════════════════════════════

    def paintEvent(self, event):   # noqa: N802
        p = QPainter(self)
        p.setCompositionMode(QPainter.CompositionMode_Source)
        p.fillRect(self.rect(), Qt.transparent)
        p.setCompositionMode(QPainter.CompositionMode_SourceOver)
        p.setRenderHints(QPainter.Antialiasing |
                         QPainter.TextAntialiasing |
                         QPainter.SmoothPixmapTransform)
        light = True
        try:  light = QApplication.instance().theme_manager.is_light()
        except Exception: pass
        pal = _Pal(light)

        cx = cy = self._SIZE/2
        D, U, R = self._axes()

        self._draw_cube(p, pal, D, U, R, cx, cy)
        self._draw_ctrl(p, pal)
        self._draw_gizmo(p, pal, D, U, R)
        p.end()

    # ── cube ────────────────────────────────────────────────────────

    def _draw_cube(self, p, pal, D, U, R, cx, cy):
        # Visibility uses INWARD D: faces with dot(n,D) < _VIS are toward camera
        vis = [(float(np.dot(f['n'],D)), nm, f)
               for nm,f in self._faces.items()
               if float(np.dot(f['n'],D)) < self._VIS]
        vis.sort(key=lambda x: x[0], reverse=True)   # deepest first

        font = QFont("DejaVu Sans", 14, QFont.DemiBold)

        p.save()
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(pal.shadow))
        for _, _, f in vis:
            shadow_poly = QPolygonF([
                QPointF(pt.x() + 1.8, pt.y() + 2.3)
                for pt in [self._proj(pt3, R, U, cx, cy) for pt3 in f['pts']]
            ])
            p.drawPolygon(shadow_poly)
        p.restore()

        for _, nm, f in vis:
            pts2d = [self._proj(pt,R,U,cx,cy) for pt in f['pts']]
            poly  = QPolygonF(pts2d)
            hov   = (nm == self.hovered_id)
            fill  = pal.hover if hov else self._face_col(f, pal)
            p.setBrush(QBrush(fill))
            bw = 1.8 if f['ft']=='main' else 0.9
            bc = pal.bord if f['ft']=='main' else pal.bord_s
            p.setPen(QPen(bc, bw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p.drawPolygon(poly)
            if f['lbl']:
                self._draw_label(p, f, R, U, cx, cy, font,
                                 pal.hov_tx if hov else pal.text)

    def _face_col(self, f, pal) -> QColor:
        """FreeCAD-style: main=bright, edge=medium, corner=dark.  Pure gray."""
        ft = f['ft']
        base = pal.f_main if ft=='main' else (pal.f_edge if ft=='edge' else pal.f_corn)
        # Lambertian shading
        shade = 0.70 + 0.30*max(0., float(np.dot(f['n'], -self._LIGHT)))
        return QColor(min(255,int(base.red()*shade)),
                      min(255,int(base.green()*shade)),
                      min(255,int(base.blue()*shade)))

    def _draw_label(self, p, f, R, U, cx, cy, font, col):
        n   = f['n']
        up3 = np.array([0.,1.,0.]) if abs(n[2])>0.5 else np.array([0.,0.,1.])
        r3  = _norm(np.cross(up3, n));  up3 = _norm(np.cross(n, r3))
        tw  = self._C * 0.76
        ctr = f['ctr']
        q   = [ctr-r3*tw+up3*tw, ctr+r3*tw+up3*tw,
               ctr+r3*tw-up3*tw, ctr-r3*tw-up3*tw]
        src = QPolygonF([QPointF(0,0),QPointF(200,0),QPointF(200,200),QPointF(0,200)])
        dst = QPolygonF([self._proj(pt,R,U,cx,cy) for pt in q])
        tf  = QTransform()
        if QTransform.quadToQuad(src, dst, tf):
            p.save(); p.setTransform(tf); p.setFont(font); p.setPen(QPen(col))
            p.drawText(QRectF(0,0,200,200), Qt.AlignCenter, f['lbl'])
            p.restore()

    # ── surrounding controls ─────────────────────────────────────────

    def _draw_ctrl(self, p, pal):
        for cid, ctrl in self._ctrl.items():
            hov  = (cid == self.hovered_id)
            fill = pal.hover    if hov else pal.ctrl
            rim  = pal.ctrl     if hov else pal.ctrl_r
            if 'poly' in ctrl:
                poly = QPolygonF([QPointF(*pt) for pt in ctrl['poly']])
                p.setBrush(QBrush(fill))
                p.setPen(QPen(rim,1.3,Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
                p.drawPolygon(poly)
            elif ctrl.get('type')=='arc':
                self._draw_arc(p, ctrl, fill, rim)
            elif ctrl.get('type')=='dot':
                p.setBrush(QBrush(fill)); p.setPen(QPen(rim,1.2))
                p.drawEllipse(QPointF(ctrl['cx'],ctrl['cy']),ctrl['r'],ctrl['r'])
            elif ctrl.get('type')=='mcube':
                self._draw_mcube(p, ctrl['cx'], ctrl['cy'], fill, pal)

    def _draw_arc(self, p, ctrl, fill, rim):
        cx_, cy_, cw, rad = ctrl['cx'], ctrl['cy'], ctrl['cw'], max(10.0, self._SIZE * 0.055)
        p.save()
        p.setPen(QPen(fill, 2.6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        p.setBrush(Qt.NoBrush)
        rect = QRectF(cx_-rad, cy_-rad, rad*2, rad*2)
        sd, sp = (210., -150.) if cw else (-30., 150.)
        path = QPainterPath(); path.arcMoveTo(rect,sd); path.arcTo(rect,sd,sp)
        p.drawPath(path)
        er = math.radians(-(sd+sp))
        ex, ey = cx_+rad*math.cos(er), cy_+rad*math.sin(er)
        tg = er + (math.pi/2 if cw else -math.pi/2)
        ah, sp2 = max(5.5, self._SIZE * 0.022), 2.6
        head = QPolygonF([QPointF(ex,ey),
                          QPointF(ex+ah*math.cos(tg+sp2),ey+ah*math.sin(tg+sp2)),
                          QPointF(ex+ah*math.cos(tg-sp2),ey+ah*math.sin(tg-sp2))])
        p.setPen(Qt.NoPen); p.setBrush(QBrush(fill)); p.drawPolygon(head)
        p.restore()

    def _draw_mcube(self, p, cx_, cy_, fill, pal):
        s = max(8, round(self._SIZE * 0.055))
        p.save()
        top=QPolygonF([QPointF(cx_,cy_-s),QPointF(cx_+s,cy_-s//2),
                       QPointF(cx_,cy_),  QPointF(cx_-s,cy_-s//2)])
        lft=QPolygonF([QPointF(cx_-s,cy_-s//2),QPointF(cx_,cy_),
                       QPointF(cx_,cy_+s//2),  QPointF(cx_-s,cy_)])
        rgt=QPolygonF([QPointF(cx_+s,cy_-s//2),QPointF(cx_,cy_),
                       QPointF(cx_,cy_+s//2),  QPointF(cx_+s,cy_)])
        for poly,sh in [(top,1.10),(rgt,0.87),(lft,0.70)]:
            c=QColor(min(255,int(fill.red()*sh)),min(255,int(fill.green()*sh)),
                     min(255,int(fill.blue()*sh)))
            p.setBrush(QBrush(c)); p.setPen(QPen(pal.bord,0.9)); p.drawPolygon(poly)
        p.restore()

    # ── XYZ gizmo ────────────────────────────────────────────────────

    def _draw_gizmo(self, p, pal, D, U, R):
        ax = round(self._SIZE * 0.15)
        ay = round(self._SIZE * 0.80)
        L = max(20, round(self._SIZE * 0.16))
        axes = [(np.array([1.,0.,0.]),QColor(215,52,52),'X'),
                (np.array([0.,1.,0.]),QColor(52,195,52),'Y'),
                (np.array([0.,0.,1.]),QColor(55,115,255),'Z')]
        axes.sort(key=lambda a: float(np.dot(a[0],D)))
        p.save(); p.setFont(QFont("DejaVu Sans",9,QFont.Bold))
        for wa, col, lbl in axes:
            sx =  float(np.dot(wa,R))*L
            sy = -float(np.dot(wa,U))*L
            p.setPen(QPen(col,2.8,Qt.SolidLine,Qt.RoundCap))
            p.drawLine(QPointF(ax,ay), QPointF(ax+sx,ay+sy))
            p.setPen(QPen(col))
            p.drawText(QPointF(ax+sx*1.44, ay+sy*1.44+4), lbl)
        p.setPen(Qt.NoPen); p.setBrush(QBrush(pal.dot))
        p.drawEllipse(QPointF(ax,ay), 3.2, 3.2)
        p.restore()

    # ═══════════════════════════════════════════════════════════════
    #  Hit testing
    # ═══════════════════════════════════════════════════════════════

    def _hit(self, pos: QPointF) -> str | None:
        D, U, R = self._axes(); cx = cy = self._SIZE/2
        for cid, ctrl in self._ctrl.items():
            if 'poly' in ctrl:
                if QPolygonF([QPointF(*pt) for pt in ctrl['poly']]).containsPoint(
                        pos, Qt.OddEvenFill): return cid
            else:
                dx,dy = pos.x()-ctrl['cx'], pos.y()-ctrl['cy']
                if dx*dx+dy*dy < ctrl.get('r',15)**2: return cid
        fs = sorted([(float(np.dot(f['n'],D)),nm,f)
                     for nm,f in self._faces.items()
                     if float(np.dot(f['n'],D)) < self._VIS])
        for _,nm,f in fs:
            if QPolygonF([self._proj(pt,R,U,cx,cy) for pt in f['pts']]).containsPoint(
                    pos, Qt.OddEvenFill): return nm
        return None

    # ═══════════════════════════════════════════════════════════════
    #  Qt events
    # ═══════════════════════════════════════════════════════════════

    def resizeEvent(self, event):   # noqa: N802
        super().resizeEvent(event)
        self.clearMask()

    def mouseMoveEvent(self, event):   # noqa: N802
        hid = self._hit(event.position())
        if hid != self.hovered_id:
            self.hovered_id = hid; self.update()
        self.setCursor(QCursor(Qt.PointingHandCursor if hid else Qt.ArrowCursor))

    def mousePressEvent(self, event):   # noqa: N802
        if event.button() != Qt.LeftButton: return super().mousePressEvent(event)
        hid = self._hit(event.position())
        if not hid: return super().mousePressEvent(event)
        event.accept()
        if hid in self._faces: self._act_face(hid)
        else: self._act_ctrl(self._ctrl[hid]['act'])

    def leaveEvent(self, event):   # noqa: N802
        self.hovered_id = None; self.update(); super().leaveEvent(event)

    # ═══════════════════════════════════════════════════════════════
    #  Actions
    # ═══════════════════════════════════════════════════════════════

    def _act_face(self, nm: str):
        n = self._faces[nm]['n']
        # Target is INWARD direction = -face_normal
        tgt = -n
        up = np.array([0.,1.,0.]) if abs(n[2])>0.95 else np.array([0.,0.,1.])
        r3 = np.cross(n, up);  up = _norm(np.cross(r3, n))
        self._start_anim(tgt, up, fit_after=True)

    def _act_ctrl(self, act: str):
        D, U, R = self._axes(); step = self._STEP
        if   act=='orbit_u': nd,nu = _rod(D,R,-step), _rod(U,R,-step)
        elif act=='orbit_d': nd,nu = _rod(D,R, step), _rod(U,R, step)
        elif act=='orbit_l': nd,nu = _rod(D,np.array([0.,0.,1.]), step), U.copy()
        elif act=='orbit_r': nd,nu = _rod(D,np.array([0.,0.,1.]),-step), U.copy()
        elif act=='roll_ccw':nd,nu = D.copy(), _rod(U,D,-step)
        elif act=='roll_cw': nd,nu = D.copy(), _rod(U,D, step)
        elif act=='home':    nd,nu = self._DDEF.copy(), self._UDEF.copy()
        else: return
        self._start_anim(_norm(nd), _norm(nu), fit_after=(act=='home'))
