"""
navicube_overlay.py  —  FreeCAD-style NaviCube  ·  Standalone PySide6 library
═══════════════════════════════════════════════════════════════════════════════
Zero renderer dependency · drop-in for any PySide6 application

Quick-start
───────────
  navicube = NaviCubeOverlay(parent=some_widget)
  navicube.viewOrientationRequested.connect(your_camera_update)
  navicube.show()

  # Push your camera state in whenever it changes:
  navicube.push_camera(dx, dy, dz, ux, uy, uz)   # inward dir + up

  # Signal interaction start / end so smoothing kicks in:
  navicube.set_interaction_active(True)    # mouse press
  navicube.set_interaction_active(False)   # mouse release

OCC users
─────────
  Use OCCNaviCubeSync (occ_navicube_sync.py) — it owns the polling
  timer, wires the signal, and calls push_camera() for you.

Sign-convention contract (critical — do not change)
────────────────────────────────────────────────────
  _dir  = inward camera direction = OCC cam.Direction() = eye → scene.

  This matches what the projection math and face-visibility check both
  require.  When we emit via viewOrientationRequested we negate
  (_dir → outward) because OCC SetProj(Vx,Vy,Vz) places the eye in
  the +V direction.

  Mnemonic:  read inward,  write outward.

Antipodal SLERP
───────────────
  dot(v0,v1) ≈ -1 → sin(ω) → 0 → division by zero → NaN.
  Fixed by routing through a stable perpendicular midpoint.
"""

import math
import numpy as np
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore    import Qt, QEvent, QPointF, Signal, QRectF, QTimer, QElapsedTimer
from PySide6.QtGui     import (
    QPainter, QColor, QPolygonF, QFont, QFontMetricsF, QPen, QBrush,
    QTransform, QCursor,
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

def _project_to_plane(v: np.ndarray, normal: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    n = _norm(np.asarray(normal, dtype=float))
    return v - np.dot(v, n) * n

def _camera_basis(d: np.ndarray, u: np.ndarray) -> np.ndarray:
    d = _norm(np.asarray(d, dtype=float))
    u = _norm(np.asarray(u, dtype=float))
    r = np.cross(d, u)
    if np.linalg.norm(r) < 1e-6:
        fallback = np.array([1.0, 0.0, 0.0]) if abs(d[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        r = np.cross(d, fallback)
    r = _norm(r)
    u = _norm(np.cross(r, d))
    return np.column_stack((r, u, -d))

def _qnorm(q: np.ndarray) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    n = np.linalg.norm(q)
    return q / n if n > 1e-10 else np.array([1.0, 0.0, 0.0, 0.0], dtype=float)

def _quat_from_matrix(m: np.ndarray) -> np.ndarray:
    m = np.asarray(m, dtype=float)
    tr = float(m[0, 0] + m[1, 1] + m[2, 2])
    if tr > 0.0:
        s = math.sqrt(tr + 1.0) * 2.0
        q = np.array([
            0.25 * s,
            (m[2, 1] - m[1, 2]) / s,
            (m[0, 2] - m[2, 0]) / s,
            (m[1, 0] - m[0, 1]) / s,
        ])
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2.0
        q = np.array([
            (m[2, 1] - m[1, 2]) / s,
            0.25 * s,
            (m[0, 1] + m[1, 0]) / s,
            (m[0, 2] + m[2, 0]) / s,
        ])
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2.0
        q = np.array([
            (m[0, 2] - m[2, 0]) / s,
            (m[0, 1] + m[1, 0]) / s,
            0.25 * s,
            (m[1, 2] + m[2, 1]) / s,
        ])
    else:
        s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2.0
        q = np.array([
            (m[1, 0] - m[0, 1]) / s,
            (m[0, 2] + m[2, 0]) / s,
            (m[1, 2] + m[2, 1]) / s,
            0.25 * s,
        ])
    return _qnorm(q)

def _matrix_from_quat(q: np.ndarray) -> np.ndarray:
    w, x, y, z = _qnorm(q)
    return np.array([
        [1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y - z * w), 2.0 * (x * z + y * w)],
        [2.0 * (x * y + z * w), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z - x * w)],
        [2.0 * (x * z - y * w), 2.0 * (y * z + x * w), 1.0 - 2.0 * (x * x + y * y)],
    ])

def _qslerp(q0: np.ndarray, q1: np.ndarray, t: float) -> np.ndarray:
    q0 = _qnorm(q0)
    q1 = _qnorm(q1)
    d = float(np.dot(q0, q1))
    if d < 0.0:
        q1 = -q1
        d = -d
    if d > 0.9995:
        return _qnorm(q0 + t * (q1 - q0))
    theta_0 = math.acos(max(-1.0, min(1.0, d)))
    sin_theta_0 = math.sin(theta_0)
    theta = theta_0 * t
    sin_theta = math.sin(theta)
    s0 = math.cos(theta) - d * sin_theta / sin_theta_0
    s1 = sin_theta / sin_theta_0
    return _qnorm((s0 * q0) + (s1 * q1))


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
    _SIZE  = 164          # widget side in px
    _SCALE = 35.0         # 3-D units → screen pixels
    _C     = 0.12         # FreeCAD-style chamfer ratio
    _AMS   = 240          # animation duration ms
    _VIS   = 0.10         # face-visibility dot-product threshold
    _STEP  = math.radians(15)
    _TICK_MS = 16
    _SYNC_EPS = 1e-3
    _INACTIVE_OPACITY = 0.72
    # ISO inward direction: camera is at (+X,−Y,+Z) → inward = (−X,+Y,−Z)
    _DDEF  = _norm(np.array([-1., 1., -1.]))
    _UDEF  = np.array([0., 0.,  1.])
    _LIGHT = _norm(np.array([-0.8, -1.0, -1.8]))   # Lambertian light dir

    def __init__(self, parent=None):
        super().__init__(parent)
        # Instance-level size/scale — overwritten by _update_dpi() below.
        # Kept as instance vars so all paint/hit-test code uses self._SIZE
        # and automatically picks up the DPI-adjusted value.
        self._SIZE  = self.__class__._SIZE
        self._SCALE = self.__class__._SCALE
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
        self._hovering = False
        self._label_font_sizes: dict[str, float] = {}

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
        self._q0 = _quat_from_matrix(_camera_basis(self._dir, self._up))
        self._q1 = self._q0.copy()
        self._interaction_active = False

        self._build_geo()
        self._update_dpi()   # sets _SIZE / _SCALE, calls setFixedSize + _build_ctrl

        self._tmr = QTimer(self)
        self._tmr.timeout.connect(self._tick)
        self._tmr.start(self._TICK_MS)

        self._anim_clock = QElapsedTimer()
        self._anim_clock.start()
        self._anim_last_ms = 0

    # ──────────────────────────── geometry ──────────────────────────

    def _build_geo(self):
        self._faces = {}

        x = np.array([1.0, 0.0, 0.0])
        y = np.array([0.0, 1.0, 0.0])
        z = np.array([0.0, 0.0, 1.0])

        self._add_cube_face("TOP", x, z, "main", "TOP")
        self._add_cube_face("FRONT", x, -y, "main", "FRONT")
        self._add_cube_face("LEFT", -y, -x, "main", "LEFT")
        self._add_cube_face("BACK", -x, y, "main", "BACK")
        self._add_cube_face("RIGHT", y, x, "main", "RIGHT")
        self._add_cube_face("BOTTOM", x, -z, "main", "BOTTOM")

        self._add_cube_face("FTR", -x - y, x - y + z, "corner")
        self._add_cube_face("FTL", -x + y, -x - y + z, "corner")
        self._add_cube_face("FBR", x + y, x - y - z, "corner")
        self._add_cube_face("FBL", x - y, -x - y - z, "corner")
        self._add_cube_face("RTR", x - y, x + y + z, "corner")
        self._add_cube_face("RTL", x + y, -x + y + z, "corner")
        self._add_cube_face("RBR", -x + y, x + y - z, "corner")
        self._add_cube_face("RBL", -x - y, -x + y - z, "corner")

        self._add_cube_face("FRONT_TOP", x, z - y, "edge")
        self._add_cube_face("FRONT_BOTTOM", x, -z - y, "edge")
        self._add_cube_face("REAR_BOTTOM", x, y - z, "edge")
        self._add_cube_face("REAR_TOP", x, y + z, "edge")
        self._add_cube_face("REAR_RIGHT", z, x + y, "edge")
        self._add_cube_face("FRONT_RIGHT", z, x - y, "edge")
        self._add_cube_face("FRONT_LEFT", z, -x - y, "edge")
        self._add_cube_face("REAR_LEFT", z, y - x, "edge")
        self._add_cube_face("TOP_LEFT", y, z - x, "edge")
        self._add_cube_face("TOP_RIGHT", y, x + z, "edge")
        self._add_cube_face("BOTTOM_RIGHT", y, x - z, "edge")
        self._add_cube_face("BOTTOM_LEFT", y, -z - x, "edge")

    def _add_cube_face(self, name, x_vec, z_vec, face_type, label=None):
        x_vec = np.asarray(x_vec, dtype=float)
        z_vec = np.asarray(z_vec, dtype=float)
        y_vec = np.cross(x_vec, -z_vec)
        chamfer = self._C

        if face_type == "corner":
            x_c = x_vec * chamfer
            y_c = y_vec * chamfer
            z_c = (1.0 - 2.0 * chamfer) * z_vec
            pts = [
                z_c - 2.0 * x_c,
                z_c - x_c - y_c,
                z_c + x_c - y_c,
                z_c + 2.0 * x_c,
                z_c + x_c + y_c,
                z_c - x_c + y_c,
            ]
            label_pts = None
        elif face_type == "edge":
            x_4 = x_vec * (1.0 - chamfer * 4.0)
            y_e = y_vec * chamfer
            z_e = z_vec * (1.0 - chamfer)
            pts = [
                z_e - x_4 - y_e,
                z_e + x_4 - y_e,
                z_e + x_4 + y_e,
                z_e - x_4 + y_e,
            ]
            label_pts = None
        else:
            x_2 = x_vec * (1.0 - chamfer * 2.0)
            y_2 = y_vec * (1.0 - chamfer * 2.0)
            x_4 = x_vec * (1.0 - chamfer * 4.0)
            y_4 = y_vec * (1.0 - chamfer * 4.0)
            pts = [
                z_vec - x_2 - y_4,
                z_vec - x_4 - y_2,
                z_vec + x_4 - y_2,
                z_vec + x_2 - y_4,
                z_vec + x_2 + y_4,
                z_vec + x_4 + y_2,
                z_vec - x_4 + y_2,
                z_vec - x_2 + y_4,
            ]
            label_pts = [
                z_vec - x_2 - y_2,
                z_vec + x_2 - y_2,
                z_vec + x_2 + y_2,
                z_vec - x_2 + y_2,
            ]

        pts = [np.asarray(pt, dtype=float) for pt in pts]
        ctr = np.mean(pts, axis=0)
        normal = _norm(ctr)
        self._faces[name] = {
            "pts": pts,
            "n": normal,
            "ctr": ctr,
            "lbl": label,
            "ft": face_type,
            "label_pts": label_pts,
        }

    def _build_ctrl(self):
        self._ctrl = {}
        self._add_button_shape("ArrowLeft", "roll_ccw")
        self._add_button_shape("ArrowRight", "roll_cw")
        self._add_button_shape("ArrowNorth", "orbit_u")
        self._add_button_shape("ArrowSouth", "orbit_d")
        self._add_button_shape("ArrowEast", "orbit_r")
        self._add_button_shape("ArrowWest", "orbit_l")
        self._add_button_shape("DotBackside", "backside")
        self._add_button_shape("ViewMenu", "home")

    def _add_button_shape(self, name, act):
        scale = 0.005
        off_x = 0.5
        off_y = 0.5

        if name in ("ArrowLeft", "ArrowRight"):
            point_data = [
                66.6, -66.6, 58.3, -74.0, 49.2, -80.3, 39.4, -85.5,
                29.0, -89.5, 25.3, -78.1, 34.3, -74.3, 42.8, -69.9,
                50.8, -64.4, 58.1, -58.1, 53.8, -53.8, 74.7, -46.8,
                70.7, -70.4,
            ]
        elif name in ("ArrowNorth", "ArrowSouth", "ArrowEast", "ArrowWest"):
            point_data = [100.0, 0.0, 80.0, -18.0, 80.0, 18.0]
        elif name == "ViewMenu":
            off_x = 0.84
            off_y = 0.84
            point_data = [
                0.0, 0.0,
                15.0, -6.0, 0.0, -12.0, -15.0, -6.0, 0.0, 0.0,
                -15.0, -6.0, -15.0, 12.0, 0.0, 18.0, 0.0, 0.0,
                0.0, 18.0, 15.0, 12.0, 15.0, -6.0,
            ]
        elif name == "DotBackside":
            point_data = []
            steps = 16
            for idx in range(steps):
                ang = 2.0 * math.pi * (idx + 0.5) / steps
                point_data.extend([10.0 * math.cos(ang) + 87.0, 10.0 * math.sin(ang) - 87.0])
        else:
            point_data = []

        pts = []
        count = len(point_data) // 2
        for idx in range(count):
            x_val = point_data[idx * 2] * scale + off_x
            y_val = point_data[idx * 2 + 1] * scale + off_y
            if name in ("ArrowNorth", "ArrowWest", "ArrowLeft"):
                x_val = 1.0 - x_val
            if name in ("ArrowSouth", "ArrowNorth"):
                pts.append(QPointF(y_val * self._SIZE, x_val * self._SIZE))
            else:
                pts.append(QPointF(x_val * self._SIZE, y_val * self._SIZE))

        self._ctrl[name] = {
            "poly": QPolygonF(pts),
            "act": act,
        }

    def _update_dpi(self) -> None:
        """
        Recompute _SIZE and _SCALE for the screen this widget is on, then
        apply setFixedSize and rebuild the pixel-space control polygons.

        Called once at construction and again whenever the widget moves to
        a screen with a different DPI (changeEvent ScreenChangeInternal).

        Logic
        ─────
        Qt's logical-pixel coordinate system already accounts for DPI on
        most platforms (Win/macOS HiDPI).  We use logicalDotsPerInch()
        relative to the 96 DPI baseline (Windows/FreeDesktop standard) as
        the scale factor.  This makes the cube physically the same size
        across 100 %, 125 %, 150 %, 200 % system scale settings.
        """
        try:
            screen = self.screen() if self.isVisible() else None
            if screen is None:
                screen = QApplication.primaryScreen()
            dpi_scale = (screen.logicalDotsPerInch() / 96.0) if screen else 1.0
            dpi_scale = max(0.75, min(dpi_scale, 4.0))   # sanity clamp
        except Exception:
            dpi_scale = 1.0

        base = self.__class__._SIZE
        new_size = round(base * dpi_scale)
        if new_size == self._SIZE and hasattr(self, "_ctrl"):
            return   # nothing changed

        self._SIZE  = new_size
        self._SCALE = self.__class__._SCALE * (new_size / base)
        self._label_font_sizes.clear()   # cached sizes are wrong at new DPI
        self.setFixedSize(self._SIZE, self._SIZE)
        self._build_ctrl()               # button polygons are pixel-space: rebuild

    # ──────────────────────────── camera ────────────────────────────

    # ── public API ───────────────────────────────────────────────────

    def push_camera(self, dx: float, dy: float, dz: float,
                    ux: float, uy: float, uz: float) -> None:
        """
        Update the navicube to match the current camera state.

        Call this whenever your camera changes (mouse drag, programmatic
        update, etc.).  The navicube will NOT call back to your renderer
        in response — it only redraws its own 2-D widget.

        Convention
        ──────────
          dx/dy/dz  INWARD direction (eye → scene).
                    For OCC: cam.Direction() values directly — no negation.
          ux/uy/uz  Camera up vector.

        During an active face-click animation the push is silently ignored
        (the navicube is driving the camera, not the other way around).
        Exception: if set_interaction_active(True) was already called, the
        animation is cancelled and the navicube immediately follows live.

        During active interaction (set_interaction_active(True)) the push
        is smoothed via quaternion SLERP to filter transient instabilities
        such as OCC Up-vector flicker near poles.
        """
        if self._at < 1.0:
            if not self._interaction_active:
                return                 # animation running; navicube drives camera
            self._at = 1.0            # interaction started mid-animation → cancel

        d = _norm(np.array([dx, dy, dz], dtype=float))
        u = _norm(np.array([ux, uy, uz], dtype=float))

        if self._interaction_active:
            if self._smooth_camera_state(d, u, 0.65):
                self.update()
        else:
            if self._set_camera_state(d, u):
                self.update()

    def set_interaction_active(self, active: bool) -> None:
        """
        Notify the navicube that the user is actively dragging the camera
        (active=True on mouse-press, active=False on mouse-release).

        While active, push_camera() applies SLERP smoothing (alpha 0.65,
        ~8 ms effective lag) to absorb momentary renderer instabilities.
        """
        self._interaction_active = bool(active)

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

    def _smooth_camera_state(self, d_tgt: np.ndarray, u_tgt: np.ndarray, alpha: float) -> bool:
        """
        SLERP current camera state toward (d_tgt, u_tgt) by factor alpha.
        Used during live interaction to follow OCC camera smoothly, which
        eliminates jitter from momentary OCC camera instabilities (e.g. Up
        vector flicker near poles) while keeping lag to ~1 tick.
        """
        d_tgt = _norm(np.asarray(d_tgt, dtype=float))
        u_tgt = _norm(np.asarray(u_tgt, dtype=float))
        r = np.cross(d_tgt, u_tgt)
        if np.linalg.norm(r) < 1e-6:
            return False
        u_tgt = _norm(np.cross(r, d_tgt))

        if (np.linalg.norm(d_tgt - self._dir) <= self._SYNC_EPS and
                np.linalg.norm(u_tgt - self._up) <= self._SYNC_EPS):
            return False

        q_cur = _quat_from_matrix(_camera_basis(self._dir, self._up))
        q_tgt = _quat_from_matrix(_camera_basis(d_tgt, u_tgt))
        q_new = _qslerp(q_cur, q_tgt, alpha)
        basis = _matrix_from_quat(q_new)
        self._dir = _norm(-basis[:, 2])
        self._up  = _norm( basis[:, 1])
        return True

    def request_sync(self):
        self._pending_sync = True

    def set_interaction_sync_active(self, active: bool):
        self._interaction_sync_active = bool(active)
        self._cooldown = 0
        self._idle_frames = 0
        if not active:
            self.request_sync()

    def _with_opacity(self, color: QColor, opacity: float) -> QColor:
        col = QColor(color)
        col.setAlpha(max(0, min(255, int(round(col.alpha() * opacity)))))
        return col

    def _label_font(self, text: str) -> QFont:
        size = self._label_font_sizes.get(text)
        if size is None:
            test_font = QFont("Arial", 100, QFont.Normal)
            test_font.setStyleHint(QFont.SansSerif)
            metrics = QFontMetricsF(test_font)
            bounds = metrics.boundingRect(text)
            target_w = self._SIZE * 0.72
            target_h = self._SIZE * 0.46
            if bounds.width() > 1e-6 and bounds.height() > 1e-6:
                size = 100.0 * min(target_w / bounds.width(), target_h / bounds.height())
            else:
                size = 30.0
            self._label_font_sizes[text] = max(20.0, size * 0.92)

        font = QFont("Arial")
        font.setStyleHint(QFont.SansSerif)
        font.setWeight(QFont.Medium)
        font.setPointSizeF(size)
        return font

    # ──────────────────────────── animation ─────────────────────────

    def _start_anim(self, tgt_dir: np.ndarray, tgt_up: np.ndarray):
        self._d0 = self._dir.copy()
        self._u0 = self._up.copy()
        self._d1 = _norm(np.asarray(tgt_dir, dtype=float))
        self._u1 = _norm(np.asarray(tgt_up,  dtype=float))
        self._q0 = _quat_from_matrix(_camera_basis(self._d0, self._u0))
        self._q1 = _quat_from_matrix(_camera_basis(self._d1, self._u1))
        self._at = 0.0
        self._anim_last_ms = self._anim_clock.elapsed()  # sync clock for accurate first dt
        self._pending_sync = False
        self._idle_frames = 0

    def _tick(self):
        """Animation-only tick. Camera sync is driven externally via push_camera()."""
        if self._at >= 1.0:
            return

        # Actual elapsed dt so animation runs at wall-clock speed even when
        # the renderer's Redraw() takes longer than _TICK_MS.
        now_ms = self._anim_clock.elapsed()
        dt = float(now_ms - self._anim_last_ms)
        self._anim_last_ms = now_ms
        dt = max(1.0, min(dt, 100.0))  # clamp: no huge jumps if tab was backgrounded

        self._at = min(1.0, self._at + dt / self._AMS)
        te = _smooth(self._at)
        q = _qslerp(self._q0, self._q1, te)
        basis = _matrix_from_quat(q)
        u = _norm(basis[:, 1])
        d = _norm(-basis[:, 2])
        self._dir, self._up = d, u

        # Emit outward (−d) for renderer (e.g. OCC SetProj convention)
        if np.linalg.norm(d) > 1e-6 and np.linalg.norm(u) > 1e-6:
            self.viewOrientationRequested.emit(
                -float(d[0]), -float(d[1]), -float(d[2]),
                 float(u[0]),  float(u[1]),  float(u[2]))

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
        # Universal light/dark detection via QPalette — works in any Qt app.
        # Falls back to light if palette is unavailable.
        from PySide6.QtGui import QPalette
        try:
            win_col = QApplication.palette().color(QPalette.Window)
            light = win_col.lightness() > 128
        except Exception:
            light = True
        pal = _Pal(light)
        opacity = 1.0 if self._hovering or self._at < 1.0 else self._INACTIVE_OPACITY

        cx = cy = self._SIZE/2
        D, U, R = self._axes()

        self._draw_cube(p, pal, D, U, R, cx, cy, opacity)
        self._draw_ctrl(p, pal, opacity)
        self._draw_gizmo(p, pal, D, U, R, opacity)
        p.end()

    # ── cube ────────────────────────────────────────────────────────

    def _draw_cube(self, p, pal, D, U, R, cx, cy, opacity):
        # Visibility uses INWARD D: faces with dot(n,D) < _VIS are toward camera
        vis = [(float(np.dot(f['ctr'], D)), nm, f)
               for nm,f in self._faces.items()
               if float(np.dot(f['n'],D)) < self._VIS]
        vis.sort(key=lambda x: x[0], reverse=True)   # deepest first

        p.save()
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._with_opacity(pal.shadow, opacity)))
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
            p.setBrush(QBrush(self._with_opacity(fill, opacity)))
            bw = 1.55 if f['ft'] == 'main' else 1.0
            bc = pal.bord if f['ft'] == 'main' else pal.bord_s
            p.setPen(QPen(self._with_opacity(bc, opacity), bw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p.drawPolygon(poly)
            if f['lbl']:
                self._draw_label(p, f, R, U, cx, cy, self._label_font(f['lbl']),
                                 self._with_opacity(pal.hov_tx if hov else pal.text, opacity))

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
        # The projected face quad uses the opposite horizontal handedness from
        # the painter's source rect, so we mirror the source horizontally to
        # keep the face labels readable instead of backwards.
        src = QPolygonF([QPointF(200,0),QPointF(0,0),QPointF(0,200),QPointF(200,200)])
        dst = QPolygonF([self._proj(pt, R, U, cx, cy) for pt in f['label_pts']])
        tf  = QTransform()
        if QTransform.quadToQuad(src, dst, tf):
            p.save(); p.setTransform(tf); p.setFont(font); p.setPen(QPen(col))
            p.drawText(QRectF(0,0,200,200), Qt.AlignCenter, f['lbl'])
            p.restore()

    # ── surrounding controls ─────────────────────────────────────────

    def _draw_ctrl(self, p, pal, opacity):
        for cid, ctrl in self._ctrl.items():
            hov = (cid == self.hovered_id)
            fill = self._with_opacity(pal.hover if hov else pal.ctrl, opacity)
            rim = self._with_opacity(pal.ctrl_r if hov else pal.bord_s, opacity)
            p.setBrush(QBrush(fill))
            p.setPen(QPen(rim, 1.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p.drawPolygon(ctrl["poly"])

    # ── XYZ gizmo ────────────────────────────────────────────────────

    def _draw_gizmo(self, p, pal, D, U, R, opacity):
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
            axis_col = self._with_opacity(col, opacity)
            p.setPen(QPen(axis_col,2.8,Qt.SolidLine,Qt.RoundCap))
            p.drawLine(QPointF(ax,ay), QPointF(ax+sx,ay+sy))
            p.setPen(QPen(axis_col))
            p.drawText(QPointF(ax+sx*1.44, ay+sy*1.44+4), lbl)
        p.setPen(Qt.NoPen); p.setBrush(QBrush(self._with_opacity(pal.dot, opacity)))
        p.drawEllipse(QPointF(ax,ay), 3.2, 3.2)
        p.restore()

    # ═══════════════════════════════════════════════════════════════
    #  Hit testing
    # ═══════════════════════════════════════════════════════════════

    def _hit(self, pos: QPointF) -> str | None:
        D, U, R = self._axes(); cx = cy = self._SIZE/2
        for cid, ctrl in self._ctrl.items():
            if ctrl["poly"].containsPoint(pos, Qt.OddEvenFill):
                return cid
        fs = sorted([(float(np.dot(f['ctr'],D)),nm,f)
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

    def changeEvent(self, event):   # noqa: N802
        """Re-scale when the widget moves to a screen with a different DPI."""
        if event.type() == QEvent.Type.ScreenChangeInternal:
            self._update_dpi()
        super().changeEvent(event)

    def mouseMoveEvent(self, event):   # noqa: N802
        was_hovering = self._hovering
        self._hovering = True
        hid = self._hit(event.position())
        if hid != self.hovered_id or not was_hovering:
            self.hovered_id = hid
            self.update()
        self.setCursor(QCursor(Qt.PointingHandCursor if hid else Qt.ArrowCursor))
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):   # noqa: N802
        if event.button() != Qt.LeftButton: return super().mousePressEvent(event)
        hid = self._hit(event.position())
        if not hid: return super().mousePressEvent(event)
        self.hovered_id = None
        event.accept()
        if hid in self._faces: self._act_face(hid)
        else: self._act_ctrl(self._ctrl[hid]['act'])
        self.update()

    def leaveEvent(self, event):   # noqa: N802
        self._hovering = False
        self.hovered_id = None
        self.update()
        super().leaveEvent(event)

    # ═══════════════════════════════════════════════════════════════
    #  Actions
    # ═══════════════════════════════════════════════════════════════

    def _nearest_face_up(self, tgt: np.ndarray, default_up: np.ndarray, face_type: str) -> np.ndarray:
        tgt = _norm(tgt)
        base_up = _project_to_plane(default_up, tgt)
        if np.linalg.norm(base_up) < 1e-6:
            fallback = np.array([0.0, 1.0, 0.0]) if abs(tgt[2]) > 0.9 else np.array([0.0, 0.0, 1.0])
            base_up = _project_to_plane(fallback, tgt)
        base_up = _norm(base_up)

        current_up = _project_to_plane(self._up, tgt)
        if np.linalg.norm(current_up) < 1e-6:
            current_up = _project_to_plane(np.cross(tgt, self._dir), tgt)
        if np.linalg.norm(current_up) < 1e-6:
            return base_up
        current_up = _norm(current_up)

        step = math.pi / 3.0 if face_type == "corner" else math.pi / 2.0
        sin_a = float(np.dot(np.cross(base_up, current_up), tgt))
        cos_a = float(np.clip(np.dot(base_up, current_up), -1.0, 1.0))
        ang = math.atan2(sin_a, cos_a)
        snap = round(ang / step) * step
        snapped_up = _rod(base_up, tgt, snap)
        return _norm(snapped_up)

    def _act_face(self, nm: str):
        face = self._faces[nm]
        n = face['n']
        # Target is INWARD direction = -face_normal
        tgt = -n
        default_up = np.array([0.,1.,0.]) if abs(n[2]) > 0.95 else np.array([0.,0.,1.])
        up = self._nearest_face_up(tgt, default_up, face['ft'])
        self._start_anim(tgt, up)

    def _act_ctrl(self, act: str):
        D, U, R = self._axes(); step = self._STEP
        if   act=='orbit_u': nd,nu = _rod(D,R,-step), _rod(U,R,-step)
        elif act=='orbit_d': nd,nu = _rod(D,R, step), _rod(U,R, step)
        elif act=='orbit_l': nd,nu = _rod(D,np.array([0.,0.,1.]), step), U.copy()
        elif act=='orbit_r': nd,nu = _rod(D,np.array([0.,0.,1.]),-step), U.copy()
        elif act=='roll_ccw':nd,nu = D.copy(), _rod(U,D,-step)
        elif act=='roll_cw': nd,nu = D.copy(), _rod(U,D, step)
        elif act=='backside': nd,nu = -D.copy(), U.copy()
        elif act=='home':    nd,nu = self._DDEF.copy(), self._UDEF.copy()
        else: return
        self._start_anim(_norm(nd), _norm(nu))
