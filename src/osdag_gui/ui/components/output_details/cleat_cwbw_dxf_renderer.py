"""DXF-driven failure-pattern diagrams for the Cleat Angle bolt-capacity popups,
connectivity "Column Web-Beam Web" (2, 3 or 4 bolts).

Sibling of ``cleat_cfbw_dxf_renderer`` (Column Flange-Beam Web), which stays untouched:
this module imports its generic helpers (text measuring, dimension primitives, label
placer, panel frames, view re-fit) and adds what is specific to this connectivity.

Scope: connectivity "Column Web-Beam Web" only.  For every other connectivity
``try_draw_cwbw`` returns False and the caller falls through (to the CFBW hook, then to
the original drawing code).

The picture (column, beam, cleat, bolts) comes from ``cleat_cwbw_dxf_geometry.DIAGRAMS``
(generated from the DXF).  Dimension arrows, lines and numbers are generated here from
the live design values - nothing numeric is hard-coded.

Popup layout (same as Column Flange-Beam Web):
    each popup partition = [ overview LEFT ][ overview RIGHT ]   entire DXF sheet
                           [ enlarged LEFT ][ enlarged RIGHT ]   cleat zone + dimensions

Failure patterns (taken from the DXF for 2 bolts, generalised to n bolts):
    tension (both legs)  : vertical dash through ALL bolts + horizontal dash at EVERY bolt
    shear, supported leg : vertical dash first bolt -> LAST bolt + horizontal dash at the LAST bolt
    shear, supporting leg: horizontal dash at the FIRST bolt + vertical dash first bolt -> plate bottom
(horizontal dashes run from the bolt line to the cleat's free edge).

Bolt count = dialog.params["rows"] (Bolt.OneLine for the supported leg, Cleat.Spting_leg.OneLine for
the supporting leg), clamped to 2..4 and drawn evenly between the DXF's first and last bolt.
"""
from PySide6.QtCore import QLineF, QRectF, Qt
from PySide6.QtGui import QBrush, QFont, QPainterPath, QPen
from PySide6.QtWidgets import (QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem,
                               QGraphicsPathItem, QGraphicsRectItem)

# generic helpers + constants shared with the CFBW module (read-only use)
from .cleat_cfbw_dxf_renderer import (
    ARROW_HALF_W, ARROW_LEN, CAPTION_ROW, CAPTION_TEXT, COL_BEAM, COL_BOLT, COL_COLUMN, COL_LINE,
    COL_PLATE, CROP_COLUMN_PAD_PX, CROP_FREE_PAD_PX, DETAIL_SCALE, DIM_COL_GAP_PX, DIM_GAP_PX,
    GAP_BETWEEN, MARGIN, OVERVIEW_SCALE, ROW_GAP_PX, TAG_BACKDROP, TAG_BOLT, TAG_CLIP_DETAIL,
    TAG_CLIP_OVERVIEW, TAG_FAILURE, TAG_FILL, TAG_STROKE, TEXT_PAD_PX,
    _Frame, _Layout, _Registry, _add_caption, _detail_crop, _fmt, _h_dim, _install_refit, effective_params,
    _label_values, _num, _overview_crop, _place_h_labels, _tag, _text_size, _v_dim)
from .cleat_cwbw_dxf_geometry import DIAGRAMS

CONNECTIVITY_CWBW = "Column Web-Beam Web"
FONT_PX = 12              # dimension text pixel height (same as CFBW)
MIN_BOLTS = 2
MAX_BOLTS = 4


# ------------------------------------------------------------------ bolts + patterns
def _bolt_count(params):
    """Bolts per line = popup param 'rows', clamped to 2..4 (the supported range)."""
    n = int(_num(params.get("rows")))
    if n < MIN_BOLTS:
        return MIN_BOLTS
    if n > MAX_BOLTS:
        print("[WARN] cleat angle DXF diagram: %d bolts requested, drawing %d (supported range %d..%d)"
              % (n, MAX_BOLTS, MIN_BOLTS, MAX_BOLTS))
        return MAX_BOLTS
    return n


def _bolt_ys(anchors, n):
    """y of each bolt (drawing units): n bolts evenly between the DXF's first and last bolt."""
    y0, y1 = anchors["bolt_y"]
    return [y0 + (y1 - y0) * k / float(n - 1) for k in range(n)]


def _vertical(x, ya, yb):
    """The vertical dash is ONE continuous segment: the DXF never splits it at a bolt."""
    return [(x, ya, x, yb)]


def _failure_segments(diag, mode, leg, ys):
    """Dashed failure-line segments (drawing units) for n bolts at heights `ys`."""
    a = diag["anchors"]
    bx, fe = a["bolt_x"], a["free_edge_x"]
    if mode == "tension":
        segs = [(bx, y, fe, y) for y in ys]                      # horizontal at EVERY bolt
        segs += _vertical(bx, ys[0], ys[-1])                     # vertical through all bolts
    elif leg == "supported":                                     # shear, supported leg
        segs = [(bx, ys[-1], fe, ys[-1])]                        # horizontal at the LAST bolt
        segs += _vertical(bx, ys[0], ys[-1])                     # vertical first -> last bolt
    else:                                                        # shear, supporting leg
        segs = [(bx, ys[0], fe, ys[0])]                          # horizontal at the FIRST bolt
        segs += _vertical(bx, ys[0], a["pattern_v_end_y"])       # vertical first bolt -> plate bottom
    return segs


def _rect_minus(r, cut):
    """r minus cut (both QRectF) as a list of up to 4 QRectF."""
    c = r.intersected(cut)
    if c.isEmpty():
        return [r]
    out = []
    if c.top() > r.top():
        out.append(QRectF(r.left(), r.top(), r.width(), c.top() - r.top()))
    if c.bottom() < r.bottom():
        out.append(QRectF(r.left(), c.bottom(), r.width(), r.bottom() - c.bottom()))
    if c.left() > r.left():
        out.append(QRectF(r.left(), c.top(), c.left() - r.left(), c.height()))
    if c.right() < r.right():
        out.append(QRectF(c.right(), c.top(), r.right() - c.right(), c.height()))
    return out


# ------------------------------------------------------------------ layout
class _LayoutCW(_Layout):
    """CFBW layout rules plus the constraint specific to this connectivity: with 3-4 bolts the pitch
    segments are shorter than the end segments."""

    def __init__(self, sides, params, font, n):
        super().__init__(sides, params, font)
        th = self.text_h
        need = [self.detail_scale]
        for d in sides:
            a = d["anchors"]
            ys = _bolt_ys(a, n)
            pitch_u = (ys[1] - ys[0]) if n > 1 else 1e9
            need.append((th + 6.0) / pitch_u)
        self.detail_scale = min(max(need), self.MAX_SCALE)


# ------------------------------------------------------------------ one diagram
def _draw_diagram(scene, diag, frame, mode, leg, params, font, detail, lay, n):
    a = diag["anchors"]
    fills = diag["fills"]
    tpl = diag["bolt_template"]
    ys = _bolt_ys(a, n)
    reg = _Registry()
    stroke_w, fail_w, dash, bolt_w = (1.0, 1.6, [5.0, 3.0], 1.0) if detail else (0.8, 1.2, [4.0, 2.5], 0.5)

    clip_path = QPainterPath()
    clip_path.addRect(frame.rect())
    clip = QGraphicsPathItem(clip_path)
    clip.setPen(QPen(Qt.NoPen))
    clip.setBrush(QBrush(Qt.NoBrush))
    clip.setFlag(QGraphicsItem.ItemClipsChildrenToShape, True)
    clip.setZValue(0)
    clip.setData(0, TAG_CLIP_DETAIL if detail else TAG_CLIP_OVERVIEW)
    scene.addItem(clip)

    def px_rect(box):
        x0, y0, x1, y1 = box
        return QRectF(frame.x(x0), frame.y(y0), (x1 - x0) * frame.s, (y1 - y0) * frame.s)

    def rect_item(box, color, z, tag=TAG_FILL):
        rect = px_rect(box)
        r = QGraphicsRectItem(rect, clip)
        r.setPen(QPen(Qt.NoPen))
        r.setBrush(QBrush(color))
        r.setZValue(z)
        _tag(r, tag)
        return r

    beam_px = px_rect(fills["beam"])
    # fills, painter's order.  The beam is IN FRONT of the column (section view), so it is drawn after it.
    rect_item(fills["column"], COL_COLUMN, 1)
    rect_item(fills["beam"], COL_BEAM, 2)
    rect_item(fills["plate"], COL_PLATE, 3)
    rect_item(fills["strip"], COL_PLATE, 3)
    for r_ in _rect_minus(px_rect(fills["column"]), beam_px):    # where the cream column is really visible
        reg.fills.append(r_.intersected(frame.rect()))
    reg.fills.append(px_rect(fills["plate"]).intersected(frame.rect()))
    reg.fills.append(px_rect(fills["strip"]).intersected(frame.rect()))

    # side-view bolt parts (head + nut) for every bolt: red fill from the template rectangles
    for y in ys:
        for (u0, dv0, u1, dv1) in tpl["rects"]:
            box = (u0, y + dv0, u1, y + dv1)
            rect_item(box, COL_BOLT, 5, TAG_BOLT)
            reg.fills.append(px_rect(box).intersected(frame.rect()))

    def stroke(x1, y1, x2, y2):
        ln = QGraphicsLineItem(frame.x(x1), frame.y(y1), frame.x(x2), frame.y(y2), clip)
        pen = QPen(COL_LINE, stroke_w)
        pen.setCapStyle(Qt.FlatCap)
        ln.setPen(pen)
        ln.setZValue(6)
        _tag(ln, TAG_STROKE)
        reg.lines.append(QLineF(frame.x(x1), frame.y(y1), frame.x(x2), frame.y(y2)))

    for (x1, y1, x2, y2) in diag["solid"]:                       # structure, exactly as drawn in the DXF
        stroke(x1, y1, x2, y2)
    for y in ys:                                                 # bolt-part outlines for every bolt
        for (x1, dv1, x2, dv2) in tpl["segments"]:
            stroke(x1, y + dv1, x2, y + dv2)

    for (x1, y1, x2, y2) in _failure_segments(diag, mode, leg, ys):   # dashed, under the bolt circles
        ln = QGraphicsLineItem(frame.x(x1), frame.y(y1), frame.x(x2), frame.y(y2), clip)
        pen = QPen(COL_LINE, fail_w)
        pen.setDashPattern(dash)
        pen.setCapStyle(Qt.FlatCap)
        ln.setPen(pen)
        ln.setZValue(7)
        _tag(ln, TAG_FAILURE)
        reg.lines.append(QLineF(frame.x(x1), frame.y(y1), frame.x(x2), frame.y(y2)))

    r = a["bolt_r"] * frame.s                                    # bolt holes seen face-on
    for y in ys:
        cx, cy = frame.x(a["bolt_x"]), frame.y(y)
        e = QGraphicsEllipseItem(cx - r, cy - r, 2 * r, 2 * r, clip)
        e.setPen(QPen(COL_LINE, bolt_w))
        e.setBrush(QBrush(COL_BOLT))
        e.setZValue(8)
        _tag(e, TAG_BOLT)
        reg.rects.append(QRectF(cx - r, cy - r, 2 * r, 2 * r))

    if not detail:
        return                                                   # overview: structure only

    # ------------------------------------------------------------ dimensions (live values only)
    away = frame.away
    fe = frame.x(a["free_edge_x"])
    top, bot = frame.y(a["plate_top_y"]), frame.y(a["plate_bottom_y"])
    by = [frame.y(y) for y in ys]
    bx = frame.x(a["bolt_x"])
    back = frame.x(a["column_face_x"])
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
def draw_cwbw_failure_pair(scene, mode, leg, params):
    """Draw the overview row + enlarged row for (mode, leg).  Returns scene (w, h)."""
    assert mode in ("shear", "tension")
    assert leg in ("supported", "supporting")
    scene.clear()

    key = "tension" if mode == "tension" else "shear_" + leg
    sides = [DIAGRAMS[key + "_left"], DIAGRAMS[key + "_right"]]
    n = _bolt_count(params)
    font = QFont()
    font.setPixelSize(FONT_PX)
    font.setBold(True)

    lay = _LayoutCW(sides, params, font, n)
    oc = _overview_crop(sides[0])
    ov_w = (oc[2] - oc[0]) * OVERVIEW_SCALE
    ov_h = (oc[3] - oc[1]) * OVERVIEW_SCALE
    det_crops = [_detail_crop(d, lay) for d in sides]
    det_w = max((c[2] - c[0]) * lay.detail_scale for c in det_crops)
    det_h = max((c[3] - c[1]) * lay.detail_scale for c in det_crops)
    panel_w = max(ov_w, det_w, lay.caption_w + 8)

    detail_top = MARGIN + ov_h + lay.caption_row
    for i, diag in enumerate(sides):
        px = MARGIN + i * (panel_w + GAP_BETWEEN)
        ov = _Frame(diag, px + (panel_w - ov_w) / 2.0, MARGIN, OVERVIEW_SCALE, _overview_crop(diag))
        dt = _Frame(diag, px + (panel_w - det_w) / 2.0, detail_top, lay.detail_scale, det_crops[i])
        _draw_diagram(scene, diag, ov, mode, leg, params, font, False, lay, n)
        _draw_diagram(scene, diag, dt, mode, leg, params, font, True, lay, n)
        _add_caption(scene, CAPTION_TEXT, font, px + panel_w / 2.0,
                     MARGIN + ov_h + (lay.caption_row - max(lay.caption_h, 16.0)) / 2.0)

    width = 2 * MARGIN + 2 * panel_w + GAP_BETWEEN
    height = detail_top + det_h + MARGIN
    scene.setSceneRect(0, 0, width, height)

    sheet = QGraphicsRectItem(QRectF(0, 0, width, height))       # white drawing sheet: readable in both themes
    sheet.setPen(QPen(Qt.NoPen))
    sheet.setBrush(QBrush(COL_BEAM))
    sheet.setZValue(-10)
    scene.addItem(_tag(sheet, TAG_BACKDROP))
    return width, height


def try_draw_cwbw(dialog, scene, mode):
    """Hook called from CleatAngleCapacityDetails.create{Shear,Tension}Drawing (after the CFBW hook).

    Returns True when this module drew the diagram (caller must stop), False when the caller must
    continue with the next hook / the original drawing code.
    """
    if type(dialog).__name__ != "CleatAngleCapacityDetails":
        return False                      # e.g. CleatAngleSectionDetails: untouched
    connectivity = getattr(getattr(dialog, "main", None), "connectivity", "")
    if connectivity != CONNECTIVITY_CWBW:
        return False                      # other connectivities: untouched
    leg = "supported" if dialog.flag == 0 else "supporting"
    params = effective_params(dialog)         # real bolt rows / columns (the popup's own params hold 0 in the real app)
    n = _bolt_count(params)
    print("[INFO] cleat angle DXF diagram (CWBW): leg=%s, mode=%s, flag=%s, bolts=%d, connectivity=%s"
          % (leg, mode, dialog.flag, n, connectivity))
    width, height = draw_cwbw_failure_pair(scene, mode, leg, params)
    _install_refit(scene, width, height)
    return True
