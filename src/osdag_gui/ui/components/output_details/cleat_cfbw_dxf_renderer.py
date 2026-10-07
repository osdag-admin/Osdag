"""DXF-driven failure-pattern diagrams for the Cleat Angle bolt-capacity popups.

Scope: connectivity "Column Flange-Beam Web" only.  For every other
connectivity ``try_draw_cfbw`` returns False and the caller keeps using the
original drawing code, so nothing else changes.

The picture (column, beam, cleat, bolts, dashed failure lines) comes from
``cleat_cfbw_dxf_geometry.DIAGRAMS`` (generated from the DXF).  Dimension
arrows, lines and numbers are generated here from the live design values -
nothing numeric is hard-coded.

Each popup view (one for shear, one for tension) is ONE scene, laid out as

    [ overview LEFT ] [ overview RIGHT ]    <- the ENTIRE DXF structure, outline fully visible
    [ enlarged LEFT ] [ enlarged RIGHT ]    <- magnified cleat zone: failure lines + ALL dimensions

LEFT has the column on the right, RIGHT is its mirror image.  Dimensions live
only in the enlarged panels because at overview scale a 20 mm end distance is
~5 px tall.  The view is re-fitted on every resize (see _install_refit), so
nothing can ever fall outside the window.
Bolts: 2, 3 or 4 per line (popup 'rows'; see effective_params).  The DXF draws 2; for 3 / 4 the
bolts are spaced evenly between the DXF's first and last bolt and each bolt gets its side-view
head + nut + tail from a one-bolt template.  For exactly 2 bolts the DXF's own dashed lines are used;
for 3 / 4 the same rules are applied to every bolt (see _rule_segments).
Failure lines:
    supported / shear    : taken from the DXF
    supported / tension  : taken from the DXF
    supporting / tension : identical to supported / tension (same DXF diagram)
    supporting / shear   : NOT in the DXF -> the previous (pre-DXF) pattern,
                           i.e. horizontal line at the TOP bolt to the free edge
                           + vertical line from the top bolt down to the plate
                           bottom.  This is the supported/shear DXF pattern
                           flipped top<->bottom (see _flip_vertically).
"""
import math

from PySide6.QtCore import QEvent, QLineF, QObject, QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import (QApplication, QGraphicsEllipseItem, QGraphicsItem,
                               QGraphicsLineItem, QGraphicsPathItem,
                               QGraphicsPolygonItem, QGraphicsRectItem,
                               QGraphicsSimpleTextItem, QScrollArea)

from .cleat_cfbw_dxf_geometry import DIAGRAMS

CONNECTIVITY_CFBW = "Column Flange-Beam Web"

# ----------------------------------------------------------------- colours
COL_COLUMN = QColor("#f4f4e3")
COL_PLATE = QColor("#acac9b")
COL_BOLT = QColor("#ff1f1f")
COL_BEAM = QColor("#ffffff")
COL_LINE = QColor("#000000")      # outlines, failure pattern, dimensions

# ------------------------------------------------------------ layout (px)
OVERVIEW_SCALE = 0.30     # scene px per drawing unit, entire structure
DETAIL_SCALE = 1.5        # scene px per drawing unit, magnified cleat zone
FONT_PX = 12              # dimension text pixel height
MARGIN = 12               # scene margin
GAP_BETWEEN = 40          # empty gap between LEFT and RIGHT panel
CAPTION_ROW = 30          # height reserved between overview and detail (caption lives here)
CAPTION_TEXT = "Enlarged view with dimensions"
OV_PAD_PX = 4             # overview window is this much larger than the sheet, so the outer
                          # outlines (column top/bottom/side, beam end) are drawn in full
CROP_FREE_PAD_PX = 150    # crop distance beyond the plate free edge (dims live here)
CROP_COLUMN_PAD_PX = 60   # crop distance beyond the column face (into the column)
CROP_V_PAD_UNITS = 6      # crop above/below the beam (drawing units)
DIM_GAP_PX = 22           # free edge -> first vertical dimension line
DIM_COL_GAP_PX = 16       # extra distance between the two vertical dimension columns
EXT_OVERSHOOT_PX = 4
ROW_GAP_PX = 28           # plate bottom -> first horizontal dim line, and row spacing
ARROW_LEN = 7.0
ARROW_HALF_W = 2.5
TEXT_PAD_PX = 5

# item tags (QGraphicsItem.data(0)) - used by the verification script
TAG_FILL = "fill"
TAG_STROKE = "stroke"
TAG_FAILURE = "failure"
TAG_BOLT = "bolt"
TAG_DIM_TEXT = "dim_text"
TAG_DIM_LINE = "dim_line"
TAG_DIM_ARROW = "dim_arrow"
TAG_DIM_EXT = "dim_ext"
TAG_CAPTION = "caption"
TAG_BACKDROP = "backdrop"
TAG_CLIP_OVERVIEW = "clip_overview"
TAG_CLIP_DETAIL = "clip_detail"


# ------------------------------------------------------------------ helpers
def _num(value):
    """Safe float: returns 0.0 for None / 'N/A' / ''."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _fmt(value):
    """155 -> '155', 37.5 -> '37.5'."""
    return "%d" % round(value) if abs(value - round(value)) < 0.05 else "%.1f" % value


def _flip_vertically(segments, plate_top, plate_bottom):
    """Mirror segments top<->bottom about the plate's horizontal mid line."""
    s = plate_top + plate_bottom
    return [(x1, s - y1, x2, s - y2) for (x1, y1, x2, y2) in segments]


MIN_BOLTS = 2
MAX_BOLTS = 4

# internal keys of the design's output list (label text differs between versions - keys do not)
_COUNT_KEYS = {0: ("Bolt.OneLine", "Bolt.Line"),                          # supported leg: rows, columns
               1: ("Cleat.Spting_leg.OneLine", "Cleat.Spting_leg.Line")}  # supporting leg


def effective_params(dialog):
    """The popup's params with the REAL bolt rows / columns.

    The legacy popup reads them with labels that do not exist in the real design ('Bolt Rows (nos)' instead of
    'Number of Row(s)'), so dialog.params['rows'] and ['cols'] are always 0 in the real app.  We therefore read
    the design's own output list by INTERNAL KEY (Bolt.OneLine, Bolt.Line, Cleat.Spting_leg.OneLine/.Line) and
    fall back to the popup's value when the design does not offer it."""
    params = dict(getattr(dialog, "params", {}) or {})
    keys = _COUNT_KEYS.get(getattr(dialog, "flag", 0), _COUNT_KEYS[0])
    design = getattr(dialog, "connection", None)
    try:
        items = {str(i[0]): i[3] for i in design.output_values(True)}
    except Exception:                                   # noqa: BLE001 - never break the popup because of this
        items = {}
    for name, key in (("rows", keys[0]), ("cols", keys[1])):
        raw = items.get(key)
        try:
            if raw is not None and str(raw).strip() != "":
                params[name] = int(float(raw))
        except (TypeError, ValueError):
            pass
    return params


def _bolt_count(params):
    """Bolts per line = params['rows'], clamped to 2..4 (the supported range)."""
    n = int(_num(params.get("rows")))
    if n < MIN_BOLTS:
        return MIN_BOLTS
    if n > MAX_BOLTS:
        print("[WARN] cleat angle DXF diagram: %d bolts requested, drawing %d (supported range %d..%d)"
              % (n, MAX_BOLTS, MIN_BOLTS, MAX_BOLTS))
        return MAX_BOLTS
    return n


def _interp(y_first, y_last, n):
    """n values evenly spaced from y_first to y_last."""
    return [y_first + (y_last - y_first) * k / float(n - 1) for k in range(n)]


def _vsplit(x, ya, yb, ys):
    """Vertical segment x from ya to yb, split at every bolt strictly inside (the dash restarts at each bolt,
    exactly like the DXF's own failure lines)."""
    cuts = [ya] + [y for y in ys if ya + 1e-6 < y < yb - 1e-6] + [yb]
    return [(x, cuts[i], x, cuts[i + 1]) for i in range(len(cuts) - 1)]


def _rule_segments(diag, mode, leg, ys):
    """Failure lines for n bolts from the rules (they reproduce the DXF's lines for 2 bolts)."""
    a = diag["anchors"]
    bx, fe = a["bolt_x"], a["free_edge_x"]
    if mode == "tension":
        return [(bx, y, fe, y) for y in ys] + _vsplit(bx, ys[0], ys[-1], ys)
    if leg == "supported":                                        # shear, supported leg
        return [(bx, ys[-1], fe, ys[-1])] + _vsplit(bx, a["plate_top_y"], ys[-1], ys)
    return [(bx, ys[0], fe, ys[0])] + _vsplit(bx, ys[0], a["plate_bottom_y"], ys)    # shear, supporting leg


def _failure_segments(diag, mode, leg, ys=None):
    """Dashed failure-line segments (drawing units) for this diagram.

    2 bolts (what the DXF draws): the DXF's own dashed lines (flipped for the supporting-leg shear).
    3 or 4 bolts: the same rules applied to every bolt."""
    if ys is not None and len(ys) != len(diag["anchors"]["bolt_y"]):
        return _rule_segments(diag, mode, leg, ys)
    segs = list(diag["dashed"])
    if mode == "shear" and leg == "supporting":
        a = diag["anchors"]
        segs = _flip_vertically(segs, a["plate_top_y"], a["plate_bottom_y"])
    return segs


class _Frame:
    """Drawing-unit -> scene-px transform for one panel (overview or detail).

    crop = (u0, v0, u1, v1) in drawing units: the part of the diagram shown.
    (ox, oy) = scene position of the panel's top-left corner, scale = px/unit.
    """

    def __init__(self, diag, ox, oy, scale, crop):
        self.column_on_right = diag["column_on_right"]
        self.away = -1 if self.column_on_right else 1      # direction column -> free edge
        self.u0, self.v0, self.u1, self.v1 = crop
        self.s = scale
        self.ox = ox
        self.oy = oy
        self.w = (self.u1 - self.u0) * scale
        self.h = (self.v1 - self.v0) * scale

    def x(self, u):
        return self.ox + (u - self.u0) * self.s

    def y(self, v):
        return self.oy + (v - self.v0) * self.s

    def rect(self):
        return QRectF(self.ox, self.oy, self.w, self.h)


def _text_size(font, text):
    """(width, height) in px of `text` drawn with `font` - measured, never assumed."""
    t = QGraphicsSimpleTextItem(text)
    t.setFont(font)
    br = t.boundingRect()
    return br.width(), br.height()


class _Layout:
    """Every size that depends on how big the text really is.

    The text is measured with the font Qt actually uses on this machine, then the
    enlarged panels are scaled / padded so that the labels always fit.  With the
    default font this reproduces the constants at the top of the module exactly
    (detail_scale == DETAIL_SCALE, ...); with a wider or taller fallback font it
    grows instead of overlapping or failing."""

    MAX_SCALE = 4.0

    def __init__(self, sides, params, font, n=2):
        self.font = font
        v = _label_values(params)
        _, th = _text_size(font, "0")
        self.text_h = th

        def w(value):
            return _text_size(font, _fmt(value))[0] if value > 0 else 0.0

        w_end, w_pitch, w_edge, w_len, w_height = (w(v["end"]), w(v["pitch"]), w(v["edge"]),
                                                   w(v["length"]), w(v["height"]))
        w_gauge = w(v["gauge"]) if v["show_gauge"] else 0.0

        need = [DETAIL_SCALE]
        for d in sides:
            a, f = d["anchors"], d["fills"]
            end_u = a["bolt_y"][0] - a["plate_top_y"]                       # shortest vertical span
            edge_u = abs(a["bolt_x"] - a["free_edge_x"])                    # free edge -> bolt line
            beam = f["beam"]
            beam_end_x = beam[2] if d["column_on_right"] else beam[0]       # beam end face (a drawn line)
            to_beam_end_u = abs(beam_end_x - a["bolt_x"])                   # bolt line -> beam end face
            centre_u = abs(beam_end_x - (a["free_edge_x"] + a["column_face_x"]) / 2.0)
            if v["end"] > 0:
                need.append((th + 6.0) / end_u)
            if n > 2 and v["pitch"] > 0:                                    # 3-4 bolts: shorter pitch segments
                pitch_u = (a["bolt_y"][1] - a["bolt_y"][0]) / (n - 1)
                need.append((th + 6.0) / pitch_u)
            if v["edge"] > 0:
                need.append((w_edge + 4.0) / edge_u)
            if w_gauge > 0:
                need.append((w_gauge + 4.0) / to_beam_end_u)
            if v["length"] > 0:
                need.append((w_len / 2.0 + 3.0) / centre_u)
        self.detail_scale = min(max(need), self.MAX_SCALE)

        # width reserved for the first column of vertical labels.  Never smaller than the original
        # estimate (so the approved look is unchanged for normal text); grows only for wider text.
        # (3px slack: DIM_COL_GAP_PX already leaves a clear gap before the next dimension line.)
        legacy = 3 * FONT_PX * 0.62 + TEXT_PAD_PX
        measured = max(w_end, w_pitch, _text_size(font, "000")[0]) + TEXT_PAD_PX
        self.stack_w = max(legacy, measured - 3.0)
        self.overall_w = max(w_height, _text_size(font, "000")[0])
        self.free_pad_px = max(CROP_FREE_PAD_PX,
                               DIM_GAP_PX + self.stack_w + DIM_COL_GAP_PX + self.overall_w + TEXT_PAD_PX + 16)
        self.row_gap = max(ROW_GAP_PX, th + 14.0)
        cw, ch = _text_size(font, CAPTION_TEXT)
        self.caption_w = cw
        self.caption_h = ch
        self.caption_row = max(CAPTION_ROW, ch + 16.0)


def _label_values(params):
    """The live design values the dimensions show (one place, used for sizing AND drawing)."""
    v = dict(height=_num(params.get("width")),      # NOTE: popup param 'width' == plate height
             length=_num(params.get("length")),
             pitch=_num(params.get("pitch")),
             end=_num(params.get("end")),
             edge=_num(params.get("edge")),
             gauge=_num(params.get("gauge1")),
             cols=int(_num(params.get("cols"))))
    v["show_gauge"] = v["cols"] > 1 and v["gauge"] > 0
    return v


def _overview_crop(diag):
    """The entire diagram, plus OV_PAD_PX so the outermost outlines are not half-clipped."""
    pad = OV_PAD_PX / OVERVIEW_SCALE
    return (-pad, -pad, diag["size"][0] + pad, diag["size"][1] + pad)


def _detail_crop(diag, lay):
    """Cleat zone: beam depth tall, CROP_FREE_PAD_PX of beam beyond the plate
    free edge (dimensions live there), CROP_COLUMN_PAD_PX into the column."""
    a = diag["anchors"]
    free_u = lay.free_pad_px / lay.detail_scale
    col_u = CROP_COLUMN_PAD_PX / lay.detail_scale
    if diag["column_on_right"]:
        u0, u1 = a["free_edge_x"] - free_u, a["column_face_x"] + col_u
    else:
        u0, u1 = a["column_face_x"] - col_u, a["free_edge_x"] + free_u
    beam = diag["fills"]["beam"]
    return (u0, beam[1] - CROP_V_PAD_UNITS, u1, beam[3] + CROP_V_PAD_UNITS)


# --------------------------------------------------------------- primitives
def _tag(item, tag):
    item.setData(0, tag)
    return item


class _Registry:
    """Obstacles (scene coordinates) that dimension labels must keep clear of.

    Filled while drawing.  NEVER iterate scene.items() in this module: with
    PySide6 that releases Python-created scene-level items and silently
    deletes them from the scene."""

    def __init__(self):
        self.lines = []      # QLineF
        self.rects = []      # QRectF (arrow heads, bolt circles, placed labels)
        self.fills = []      # QRectF visible area of every coloured fill (column, plate, bolts): text never goes there


def _add_dim_text(scene, text, font, x, y, anchor, reg=None):
    """Place text so that (x, y) is its horizontal `anchor` ('left'|'right'|
    'center') and its vertical centre."""
    t = QGraphicsSimpleTextItem(text)
    t.setFont(font)
    t.setBrush(QBrush(COL_LINE))
    br = t.boundingRect()
    if anchor == "right":
        px = x - br.width()
    elif anchor == "center":
        px = x - br.width() / 2.0
    else:
        px = x
    t.setPos(px, y - br.height() / 2.0)
    t.setZValue(30)
    scene.addItem(_tag(t, TAG_DIM_TEXT))
    if reg is not None:
        reg.rects.append(QRectF(px, y - br.height() / 2.0, br.width(), br.height()))
    return t


def _add_line(scene, x1, y1, x2, y2, tag, width=1.0, z=20, reg=None):
    if reg is not None:
        reg.lines.append(QLineF(x1, y1, x2, y2))
    ln = QGraphicsLineItem(x1, y1, x2, y2)
    pen = QPen(COL_LINE, width)
    pen.setCapStyle(Qt.FlatCap)
    ln.setPen(pen)
    ln.setZValue(z)
    scene.addItem(_tag(ln, tag))
    return ln


def _add_arrow(scene, tip_x, tip_y, dx, dy, reg=None):
    """Filled arrow head; (dx, dy) is the unit vector the arrow points along."""
    bx, by = tip_x - dx * ARROW_LEN, tip_y - dy * ARROW_LEN
    nx, ny = -dy, dx
    poly = QPolygonF([QPointF(tip_x, tip_y),
                      QPointF(bx + nx * ARROW_HALF_W, by + ny * ARROW_HALF_W),
                      QPointF(bx - nx * ARROW_HALF_W, by - ny * ARROW_HALF_W)])
    it = QGraphicsPolygonItem(poly)
    it.setPen(QPen(COL_LINE, 0.5))
    it.setBrush(QBrush(COL_LINE))
    it.setZValue(25)
    scene.addItem(_tag(it, TAG_DIM_ARROW))
    if reg is not None:
        reg.rects.append(poly.boundingRect())
    return it


def _v_dim(scene, font, reg, x_line, y1, y2, label, away, ext_from_x):
    """Vertical dimension between scene y1<y2 on the vertical line x_line.
    Label sits on the `away` side of the line.  Extension lines start at
    ext_from_x."""
    for yy in (y1, y2):
        _add_line(scene, ext_from_x, yy, x_line + away * EXT_OVERSHOOT_PX, yy, TAG_DIM_EXT, 0.8, 18, reg)
    _add_line(scene, x_line, y1, x_line, y2, TAG_DIM_LINE, 1.0, 20, reg)
    _add_arrow(scene, x_line, y1, 0, -1, reg)    # tips touch the extension lines,
    _add_arrow(scene, x_line, y2, 0, 1, reg)     # heads sit INSIDE the measured span
    anchor = "right" if away < 0 else "left"
    return _add_dim_text(scene, label, font, x_line + away * TEXT_PAD_PX, (y1 + y2) / 2.0, anchor, reg)


def _h_dim(scene, reg, y_line, x1, x2, label, ext_from_y):
    """Horizontal dimension between scene x1<x2 on the horizontal line y_line.
    Draws only lines + arrows and returns a pending label spec; the label is
    placed later by _place_h_labels (it needs to know every other line first)."""
    for xx in (x1, x2):
        _add_line(scene, xx, ext_from_y, xx, y_line + EXT_OVERSHOOT_PX, TAG_DIM_EXT, 0.8, 18, reg)
    _add_line(scene, x1, y_line, x2, y_line, TAG_DIM_LINE, 1.0, 20, reg)
    _add_arrow(scene, x1, y_line, -1, 0, reg)
    _add_arrow(scene, x2, y_line, 1, 0, reg)
    return (label, x1, x2, y_line)


def _hits_line(rect, line):
    """True if QLineF `line` touches QRectF `rect`."""
    if rect.contains(line.p1()) or rect.contains(line.p2()):
        return True
    edges = (QLineF(rect.topLeft(), rect.topRight()), QLineF(rect.topRight(), rect.bottomRight()),
             QLineF(rect.bottomRight(), rect.bottomLeft()), QLineF(rect.bottomLeft(), rect.topLeft()))
    for edge in edges:
        res = line.intersects(edge)            # PySide6 versions differ: enum or (enum, point)
        kind = res[0] if isinstance(res, tuple) else res
        if kind == QLineF.BoundedIntersection:
            return True
    return False


def _place_h_labels(scene, font, reg, pending, window):
    """Put each pending horizontal-dimension label BELOW its dimension line,
    sliding it sideways (0, -4, +4, -8, ... px) until it touches no line,
    arrow, bolt or other label inside the diagram window.

    Never raises: if no clean spot exists (extreme fonts) the least-bad spot is used
    and a warning is printed - a slightly tight label must never take the popup down."""
    for (label, x1, x2, y_line) in pending:
        t = QGraphicsSimpleTextItem(label)
        t.setFont(font)
        t.setBrush(QBrush(COL_LINE))
        br = t.boundingRect()
        cx = (x1 + x2) / 2.0
        y = y_line + TEXT_PAD_PX + 2
        shifts = [0.0] + [sg * k * 4.0 for k in range(1, 41) for sg in (-1, 1)]
        best, best_score = None, None
        for sh in shifts:
            r = QRectF(cx + sh - br.width() / 2.0, y, br.width(), br.height())
            padded = r.adjusted(-2, -2, 2, 2)
            score = 0 if window.contains(padded) else 1000
            score += sum(1 for ln in reg.lines if _hits_line(padded, ln))
            score += sum(1 for rc in reg.rects if padded.intersects(rc))
            score += sum(1 for fr in reg.fills if padded.intersects(fr))
            if best_score is None or score < best_score:
                best, best_score = r, score
            if score == 0:
                break
        if best_score:
            print("[WARN] cleat angle DXF diagram: label %r placed with %d unavoidable overlap(s)" % (label, best_score))
        t.setPos(best.x(), best.y())
        t.setZValue(30)
        scene.addItem(_tag(t, TAG_DIM_TEXT))
        reg.rects.append(best)


# ------------------------------------------------------------- one diagram
def _draw_diagram(scene, diag, frame, mode, leg, params, font, detail, lay, n=2):
    a = diag["anchors"]
    fills = diag["fills"]
    tpl = diag["bolt_template"]
    ys = _interp(a["bolt_y"][0], a["bolt_y"][1], n)                   # face-on bolt circles
    side_ys = _interp(a["side_bolt_y"][0], a["side_bolt_y"][1], n)    # side-view bolts (head + nut + tail)
    reg = _Registry()
    # pen styles: the overview is drawn ~5x smaller, so its lines are finer
    stroke_w, fail_w, dash, bolt_w = (1.0, 1.6, [5.0, 3.0], 1.0) if detail else (0.8, 1.2, [4.0, 2.5], 0.5)

    # clip group = panel window; everything geometric is a child of it
    clip_path = QPainterPath()
    clip_path.addRect(frame.rect())
    clip = QGraphicsPathItem(clip_path)
    clip.setPen(QPen(Qt.NoPen))
    clip.setBrush(QBrush(Qt.NoBrush))
    clip.setFlag(QGraphicsItem.ItemClipsChildrenToShape, True)
    clip.setZValue(0)
    clip.setData(0, TAG_CLIP_DETAIL if detail else TAG_CLIP_OVERVIEW)
    scene.addItem(clip)

    def rect_item(box, color, z, tag=TAG_FILL):
        x0, y0, x1, y1 = box
        r = QGraphicsRectItem(QRectF(frame.x(x0), frame.y(y0), (x1 - x0) * frame.s, (y1 - y0) * frame.s), clip)
        r.setPen(QPen(Qt.NoPen))
        r.setBrush(QBrush(color))
        r.setZValue(z)
        _tag(r, tag)
        if color != COL_BEAM:                                    # white beam fill is a legal place for text
            reg.fills.append(QRectF(frame.x(x0), frame.y(y0), (x1 - x0) * frame.s, (y1 - y0) * frame.s).intersected(frame.rect()))
        return r

    # fills (painter's order)
    rect_item(fills["beam"], COL_BEAM, 1)
    rect_item(fills["column"], COL_COLUMN, 2)
    rect_item(fills["plate"], COL_PLATE, 3)
    rect_item(fills["strip"], COL_PLATE, 3)
    for sy in side_ys:
        for (u0, dv0, u1, dv1) in tpl["rects"]:
            rect_item((u0, sy + dv0, u1, sy + dv1), COL_BOLT, 5, TAG_BOLT)

    # solid outlines, exactly as drawn in the DXF, plus the outline of every side-view bolt
    outlines = list(diag["solid"])
    for sy in side_ys:
        outlines += [(x1, sy + dv1, x2, sy + dv2) for (x1, dv1, x2, dv2) in tpl["segments"]]
    for (x1, y1, x2, y2) in outlines:
        ln = QGraphicsLineItem(frame.x(x1), frame.y(y1), frame.x(x2), frame.y(y2), clip)
        pen = QPen(COL_LINE, stroke_w)
        pen.setCapStyle(Qt.FlatCap)
        ln.setPen(pen)
        ln.setZValue(6)
        _tag(ln, TAG_STROKE)
        reg.lines.append(QLineF(frame.x(x1), frame.y(y1), frame.x(x2), frame.y(y2)))

    # dashed failure pattern (under the bolt circles so circles stay solid red)
    for (x1, y1, x2, y2) in _failure_segments(diag, mode, leg, ys):
        ln = QGraphicsLineItem(frame.x(x1), frame.y(y1), frame.x(x2), frame.y(y2), clip)
        pen = QPen(COL_LINE, fail_w)
        pen.setDashPattern(dash)
        pen.setCapStyle(Qt.FlatCap)
        ln.setPen(pen)
        ln.setZValue(7)
        _tag(ln, TAG_FAILURE)
        reg.lines.append(QLineF(frame.x(x1), frame.y(y1), frame.x(x2), frame.y(y2)))

    # bolt holes seen face-on
    r = a["bolt_r"] * frame.s
    for by in ys:
        cx, cy = frame.x(a["bolt_x"]), frame.y(by)
        e = QGraphicsEllipseItem(cx - r, cy - r, 2 * r, 2 * r, clip)
        e.setPen(QPen(COL_LINE, bolt_w))
        e.setBrush(QBrush(COL_BOLT))
        e.setZValue(8)
        _tag(e, TAG_BOLT)
        reg.rects.append(QRectF(cx - r, cy - r, 2 * r, 2 * r))

    if not detail:
        return                                   # overview: structure only, no dimensions

    # ------------------------------------------------------------ dimensions
    away = frame.away
    fe = frame.x(a["free_edge_x"])
    top, bot = frame.y(a["plate_top_y"]), frame.y(a["plate_bottom_y"])
    by = [frame.y(y) for y in ys]
    bx = frame.x(a["bolt_x"])
    back = frame.x(a["column_face_x"])           # back of the cleat (against column flange)

    v = _label_values(params)
    height, length, pitch, end, edge, gauge, cols = (v["height"], v["length"], v["pitch"], v["end"],
                                                     v["edge"], v["gauge"], v["cols"])

    ext_x = fe + away * 3
    x_stack = fe + away * DIM_GAP_PX
    x_overall = x_stack + away * (lay.stack_w + DIM_COL_GAP_PX)

    if end > 0:
        _v_dim(scene, font, reg, x_stack, top, by[0], _fmt(end), away, ext_x)
        _v_dim(scene, font, reg, x_stack, by[-1], bot, _fmt(end), away, ext_x)
    if pitch > 0:
        for k in range(n - 1):                                   # n bolts -> n-1 pitch dimensions
            _v_dim(scene, font, reg, x_stack, by[k], by[k + 1], _fmt(pitch), away, ext_x)
    if height > 0:
        _v_dim(scene, font, reg, x_overall, top, bot, _fmt(height), away, ext_x)

    # horizontal chain below the plate: row A = edge | gauge, row B = length
    row_a = bot + lay.row_gap
    row_b = row_a + lay.row_gap
    ext_y = bot + 2
    pending = []
    if edge > 0:
        xs = sorted((fe, bx))
        pending.append(_h_dim(scene, reg, row_a, xs[0], xs[1], _fmt(edge), ext_y))
    if cols > 1 and gauge > 0:
        xs = sorted((bx, back))
        pending.append(_h_dim(scene, reg, row_a, xs[0], xs[1], _fmt(gauge), ext_y))
    if length > 0:
        xs = sorted((fe, back))
        pending.append(_h_dim(scene, reg, row_b, xs[0], xs[1], _fmt(length), ext_y))
    _place_h_labels(scene, font, reg, pending, frame.rect())


# ---------------------------------------------------------------- public API
def _add_caption(scene, text, font, cx, y):
    t = QGraphicsSimpleTextItem(text)
    t.setFont(font)
    t.setBrush(QBrush(COL_LINE))
    br = t.boundingRect()
    t.setPos(cx - br.width() / 2.0, y)
    t.setZValue(30)
    scene.addItem(_tag(t, TAG_CAPTION))
    return t


def draw_cfbw_failure_pair(scene, mode, leg, params):
    """Draw the overview row + detail row for (mode, leg).  Returns scene (w, h)."""
    assert mode in ("shear", "tension")
    assert leg in ("supported", "supporting")
    scene.clear()

    sides = [DIAGRAMS[mode + "_left"], DIAGRAMS[mode + "_right"]]
    font = QFont()
    font.setPixelSize(FONT_PX)
    font.setBold(True)

    n = _bolt_count(params)
    lay = _Layout(sides, params, font, n)
    oc = _overview_crop(sides[0])
    ov_w = (oc[2] - oc[0]) * OVERVIEW_SCALE
    ov_h = (oc[3] - oc[1]) * OVERVIEW_SCALE
    det_crops = [_detail_crop(d, lay) for d in sides]
    det_w = max((c[2] - c[0]) * lay.detail_scale for c in det_crops)
    det_h = max((c[3] - c[1]) * lay.detail_scale for c in det_crops)
    panel_w = max(ov_w, det_w, lay.caption_w + 8)

    detail_top = MARGIN + ov_h + lay.caption_row
    for i, diag in enumerate(sides):
        px = MARGIN + i * (panel_w + GAP_BETWEEN)                 # panel left edge
        ov = _Frame(diag, px + (panel_w - ov_w) / 2.0, MARGIN, OVERVIEW_SCALE, _overview_crop(diag))
        dt = _Frame(diag, px + (panel_w - det_w) / 2.0, detail_top, lay.detail_scale, det_crops[i])
        _draw_diagram(scene, diag, ov, mode, leg, params, font, False, lay, n)
        _draw_diagram(scene, diag, dt, mode, leg, params, font, True, lay, n)
        _add_caption(scene, CAPTION_TEXT, font, px + panel_w / 2.0,
                     MARGIN + ov_h + (lay.caption_row - max(lay.caption_h, 16.0)) / 2.0)

    width = 2 * MARGIN + 2 * panel_w + GAP_BETWEEN
    height = detail_top + det_h + MARGIN
    scene.setSceneRect(0, 0, width, height)

    # White drawing sheet behind everything: every black line / caption / dimension is
    # then readable in BOTH themes (the dark view background would swallow black text).
    sheet = QGraphicsRectItem(QRectF(0, 0, width, height))
    sheet.setPen(QPen(Qt.NoPen))
    sheet.setBrush(QBrush(COL_BEAM))
    sheet.setZValue(-10)
    scene.addItem(_tag(sheet, TAG_BACKDROP))
    return width, height


class _RefitFilter(QObject):
    """Event filter for the QGraphicsViews this module draws into.

    1. Re-fits the view to its scene on every Show / Resize.  The legacy popup calls
       fitInView() once, BEFORE the view has its real size, and has scrollbars off -
       so content gets cut off.
    2. Mouse wheel over a diagram scrolls the popup's own QScrollArea.  A graphics view
       swallows wheel events by default, which would make the (tall) popup impossible
       to scroll while the mouse is over a diagram.

    It is parented to the view, so it lives and dies with it."""

    def __init__(self, view, scene):
        super().__init__(view)
        self._view = view
        self._scene = scene

    def _scroll_area(self):
        w = self._view.parentWidget()
        while w is not None and not isinstance(w, QScrollArea):
            w = w.parentWidget()
        return w

    def eventFilter(self, obj, event):
        kind = event.type()
        if obj is self._view and kind in (QEvent.Resize, QEvent.Show):
            self._view.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
        elif kind == QEvent.Wheel and obj is self._view.viewport():
            area = self._scroll_area()
            if area is not None:
                bar = area.verticalScrollBar()
                if not event.pixelDelta().isNull():
                    bar.setValue(bar.value() - event.pixelDelta().y())                      # touchpad
                else:
                    lines = QApplication.wheelScrollLines()
                    bar.setValue(bar.value() - int(round(event.angleDelta().y() / 120.0 * lines * bar.singleStep())))
                event.accept()
                return True
        return False


def _install_refit(scene, width, height):
    """Give every view of `scene` a minimum height that matches the scene's
    aspect ratio (at the view's minimum width) and keep it fitted."""
    for view in scene.views():
        min_w = max(view.minimumWidth(), 1)
        view.setMinimumHeight(int(math.ceil(min_w * height / width)) + 2)
        flt = _RefitFilter(view, scene)
        view.installEventFilter(flt)
        view.viewport().installEventFilter(flt)
        view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)


def try_draw_cfbw(dialog, scene, mode):
    """Hook called from CleatAngleCapacityDetails.create{Shear,Tension}Drawing.

    Returns True when this module drew the diagram (caller must stop), False
    when the caller must run its original drawing code.
    """
    if type(dialog).__name__ != "CleatAngleCapacityDetails":
        return False                      # e.g. CleatAngleSectionDetails: untouched
    connectivity = getattr(getattr(dialog, "main", None), "connectivity", "")
    if connectivity != CONNECTIVITY_CFBW:
        return False                      # other connectivities: untouched
    leg = "supported" if dialog.flag == 0 else "supporting"
    params = effective_params(dialog)         # real bolt rows / columns (the popup's own params hold 0 in the real app)
    # console trace (same style as the app's other [INFO] lines): shows what the popup really received
    print("[INFO] cleat angle DXF diagram: leg=%s, mode=%s, flag=%s, bolts=%d, connectivity=%s"
          % (leg, mode, dialog.flag, _bolt_count(params), connectivity))
    width, height = draw_cfbw_failure_pair(scene, mode, leg, params)
    _install_refit(scene, width, height)
    return True
