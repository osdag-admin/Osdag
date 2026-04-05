from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *

from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QSizePolicy, QFrame, QDialog,
    QScrollArea, QSizeGrip, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem
)
from PySide6.QtGui import (
    QPainter, QPen, QFont, QColor, QBrush, QPolygonF
)
from PySide6.QtCore import Qt, QPointF, QRectF


class ColWebFractureDialog(QDialog):
    """
    Three fracture-pattern cards stacked vertically for Column Web fracture.

    Each card:
      LEFT  — bold title + capacity value rows
      RIGHT — portrait plate diagram with bolt grid and fracture lines

    The column diagram is the beam web diagram rotated 90°:
      • Beam rows  (horizontal bolt lines) → Column cols  (vertical bolt lines)
      • Beam cols  (vertical bolt groups)  → Column rows  (horizontal bolt groups)
      • "Left half" in beam (left group of cols) → "Top half" in column (top group of rows)

    Fracture patterns (90°-rotated equivalents of beam Web patterns):

      Pattern 1 (beam C-bracket on left half → column C-bracket on TOP half):
        • Vertical   top plate edge → last bolt of top half, LEFT col
        • Horizontal left col → right col at same y (last bolt of top half)
        • Vertical   right col → top plate edge, same y
        (inverted-U / C rotated 90°, opening upward)

      Pattern 2 (beam full rectangle → column full rectangle):
        • Full rectangle through outermost bolt corners (unchanged by rotation)

      Pattern 3 (beam two outward L-lines from left edge →
                 column two outward L-lines from top edge):
        • Line A (left col):  top edge → last bolt of top half,
                              then LEFT to left plate edge
        • Line B (right col): top edge → last bolt of top half,
                              then RIGHT to right plate edge
    """

    # Card metadata: (title, pattern_index)
    CARDS = [
        ("Failure Pattern 1 – Tension in Member and Plate", 1),
        ("Failure Pattern 2 – Tension in Member and Plate", 2),
        ("Failure Pattern 3 – Tension in Member and Plate", 3),
    ]

    def __init__(self, main, fn):
        super().__init__()

        app = QApplication.instance()
        self.theme = app.theme_manager
        self.main  = main
        self.fn    = fn

        # ── Geometry — row/col counts for the COLUMN web plate ───────
        # bolts_one_line → number of bolt columns (vertical lines)
        # bolt_line      → number of bolt rows    (horizontal lines)
        self.rows = int(main.web_plate.bolts_one_line)
        self.cols = int(main.web_plate.bolt_line)

        # ── Capacity rows ─────────────────────────────────────────────
        self._cap_rows = self._parse_capacity()

        self._init_wrapper()
        self._build_ui()

    # ------------------------------------------------------------------
    # Parse fn() → flat list of (label, value) pairs
    # ------------------------------------------------------------------
    def _parse_capacity(self):
        rows = []
        try:
            for entry in self.fn(True):
                if len(entry) >= 4 and entry[2] == TYPE_TEXTBOX and entry[1]:
                    rows.append((str(entry[1]), str(entry[3]) if entry[3] != '' else '—'))
        except Exception as e:
            print(f"[ColumnWebFractureDialog] parse error: {e}")
        return rows

    # ------------------------------------------------------------------
    # Window chrome
    # ------------------------------------------------------------------
    def _init_wrapper(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setObjectName("spacing_capacity_details")

        root = QVBoxLayout(self)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(0)

        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle("Fracture Pattern")
        root.addWidget(self.title_bar)

        self.content_widget = QWidget(self)
        root.addWidget(self.content_widget, 1)

        grip = QSizeGrip(self)
        grip.setFixedSize(16, 16)
        grip_row = QHBoxLayout()
        grip_row.setContentsMargins(0, 0, 4, 4)
        grip_row.addStretch(1)
        grip_row.addWidget(grip, 0, Qt.AlignBottom | Qt.AlignRight)
        root.addLayout(grip_row)

    # ------------------------------------------------------------------
    # Main content — 3 cards
    # ------------------------------------------------------------------
    def _build_ui(self):

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = 1200, 800
        x = screen_geometry.x() + (screen_geometry.width()  - width)  // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

        outer = QVBoxLayout(self.content_widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        outer.addWidget(scroll)

        container = QWidget()
        container.setObjectName("cwf_container")
        scroll.setWidget(container)

        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(10, 10, 10, 10)
        vbox.setSpacing(10)

        for title, pattern in self.CARDS:
            vbox.addWidget(self._make_card(title=title, pattern=pattern))

        vbox.addStretch()

    # ------------------------------------------------------------------
    # One card — bordered frame, left text + right diagram
    # ------------------------------------------------------------------
    def _make_card(self, title, pattern):
        card = QFrame()
        card.setObjectName("cwf_card")
        card.setFrameShape(QFrame.StyledPanel)
        card.setFrameShadow(QFrame.Raised)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(0)

        # ── LEFT: title + value rows ────────────────────────────────
        left = QWidget()
        left.setFixedWidth(300)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 12, 0)
        ll.setSpacing(3)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("cwf_card_title")
        title_lbl.setWordWrap(True)
        f = title_lbl.font()
        f.setBold(True)
        title_lbl.setFont(f)
        ll.addWidget(title_lbl)
        ll.addSpacing(6)

        for lbl_text, val_text in self._cap_rows:
            row = QHBoxLayout()
            row.setSpacing(6)
            lbl = QLabel(lbl_text)
            lbl.setObjectName("cwf_left_label")
            lbl.setWordWrap(True)
            val = QLabel(val_text)
            val.setObjectName("cwf_left_value")
            val.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            row.addWidget(lbl, 1)
            row.addWidget(val)
            ll.addLayout(row)

        ll.addStretch()
        layout.addWidget(left)

        # ── RIGHT: diagram ──────────────────────────────────────────
        view = self._make_view()
        self._draw_plate(view._scene, pattern=pattern)
        view.fitInView(view._scene.sceneRect(), Qt.KeepAspectRatio)
        layout.addWidget(view, 1)

        return card

    # ------------------------------------------------------------------
    # QGraphicsView factory
    # ------------------------------------------------------------------
    def _make_view(self):
        scene = QGraphicsScene()
        view  = QGraphicsView(scene)
        view._scene = scene
        view.setRenderHint(QPainter.Antialiasing)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view.setMinimumHeight(200)
        view.setMaximumHeight(300)

        if self.theme.is_light():
            view.setBackgroundBrush(QBrush(Qt.white))
        else:
            view.setBackgroundBrush(QBrush(QColor("#4A4A4A")))

        return view

    # ------------------------------------------------------------------
    # Colour helpers
    # ------------------------------------------------------------------
    def _fg(self):
        return Qt.black if self.theme.is_light() else QColor("#DDDDDD")

    def _plate_brush(self):
        return QBrush(Qt.white) if self.theme.is_light() else QBrush(QColor("#5A5A5A"))

    # ------------------------------------------------------------------
    # Core drawing — 90° rotation of the beam web diagram.
    #
    # The beam diagram is LANDSCAPE with bolts arranged as:
    #   • rows  = horizontal lines of bolts
    #   • cols  = two groups of vertical bolt columns (left half / right half)
    #   • fracture lines run horizontally (left→right) and vertically
    #
    # For the COLUMN diagram we rotate 90° so:
    #   • The plate is PORTRAIT  (CANVAS_W < CANVAS_H)
    #   • What were "rows"  (bolt lines across) are now VERTICAL bolt columns
    #   • What were "cols"  (bolt groups)       are now HORIZONTAL bolt rows
    #   • "Left half"  in beam  →  "Top half"   in column
    #   • Fracture lines that were horizontal become vertical, and vice-versa
    #
    # Variable naming convention in this function:
    #   bolt_cx[c]  — x-coordinate of bolt COLUMN  c  (there are self.rows columns)
    #   bolt_cy[r]  — y-coordinate of bolt ROW      r  (there are self.cols rows)
    #
    #   half        — number of rows in the TOP group  (= cols // 2 from beam)
    #
    # Fracture patterns (rotated):
    # ─────────────────────────────
    # Pattern 1 — inverted-U bracket on TOP half (beam C-bracket rotated 90°):
    #   • Vertical   : top plate edge → corner_y, LEFT bolt column
    #   • Horizontal : LEFT col → RIGHT col at corner_y
    #   • Vertical   : corner_y → top plate edge, RIGHT bolt column
    #
    # Pattern 2 — full rectangle (same topology, just orientation changes):
    #   • top_y  horiz: left_x → right_x
    #   • bot_y  horiz: left_x → right_x
    #   • left_x vert : top_y  → bot_y
    #   • right_x vert: top_y  → bot_y
    #
    # Pattern 3 — two outward L-lines from TOP edge:
    #   • Line A (left col):  top edge → corner_y, then LEFT  to left plate edge
    #   • Line B (right col): top edge → corner_y, then RIGHT to right plate edge
    # ------------------------------------------------------------------
    def _draw_plate(self, scene, pattern=1):

        # ── Portrait canvas ──────────────────────────────────────────
        CANVAS_W = 220    # narrower  (was height in beam)
        CANVAS_H = 340    # taller    (was width  in beam)
        MX       = 20
        MY       = 20

        # In column orientation:
        #   self.rows  → number of vertical bolt COLUMNS  (beam's bolts_one_line)
        #   self.cols  → number of horizontal bolt ROWS   (beam's bolt_line)
        num_vcols = self.rows   # vertical columns of bolts
        num_hrows = self.cols   # horizontal rows of bolts
        half      = max(1, num_hrows // 2)   # rows in the TOP group

        pw = CANVAS_W - 2 * MX
        ph = CANVAS_H - 2 * MY

        # ── Derived bolt spacing ──────────────────────────────────────
        pad_x = pw * 0.15    # horizontal padding (fewer columns)
        pad_y = ph * 0.12    # vertical   padding

        # Horizontal spacing between vertical bolt columns
        avail_w = pw - 2 * pad_x
        gauge_x = avail_w / (num_vcols - 1) if num_vcols > 1 else avail_w

        # Vertical spacing between horizontal bolt rows (two groups + mid gap)
        # Same formula as beam but applied vertically:
        #   2*(half-1)*g + 1.5*g = avail_h
        avail_h  = ph - 2 * pad_y
        gauge_y  = avail_h / (2 * (half - 1) + 1.5) if half > 1 else avail_h / 2.5
        mid_gap  = gauge_y * 1.5

        r = min(gauge_x, gauge_y) * 0.28   # bolt radius

        # ── Bolt centre coordinates ───────────────────────────────────
        # x-coords: equally spaced vertical columns
        h_offset = MX + pad_x
        bolt_cx  = [h_offset + c * gauge_x for c in range(num_vcols)]

        # y-coords: two groups of rows separated by mid_gap (top group / bottom group)
        half_span    = (half - 1) * gauge_y
        total_bolt_h = half_span * 2 + mid_gap
        v_offset     = MY + (ph - total_bolt_h) / 2   # y of row 0

        bolt_cy = []
        for r_idx in range(num_hrows):
            if r_idx < half:
                bolt_cy.append(v_offset + r_idx * gauge_y)
            else:
                bolt_cy.append(v_offset + half_span + mid_gap + (r_idx - half) * gauge_y)

        fg = self._fg()

        # ── Plate ─────────────────────────────────────────────────────
        rect = QGraphicsRectItem(QRectF(MX, MY, pw, ph))
        rect.setPen(QPen(fg, 2.0))
        rect.setBrush(self._plate_brush())
        scene.addItem(rect)

        # ── Bolt holes ────────────────────────────────────────────────
        hole_pen = QPen(fg, 1.5)
        bolt_r   = min(gauge_x, gauge_y) * 0.28
        for c in range(num_vcols):
            for ri in range(num_hrows):
                cx, cy = bolt_cx[c], bolt_cy[ri]
                scene.addEllipse(cx - bolt_r, cy - bolt_r,
                                 2 * bolt_r, 2 * bolt_r, hole_pen)

        # ── Fracture line pen ─────────────────────────────────────────
        frac_pen = QPen(QColor("#3A7FD5"), 1.5)
        frac_pen.setStyle(Qt.DashLine)

        left_x   = bolt_cx[0]           # leftmost bolt column x
        right_x  = bolt_cx[-1]          # rightmost bolt column x
        top_y    = bolt_cy[0]           # topmost bolt row y
        bot_y    = bolt_cy[-1]          # bottommost bolt row y
        corner_y = bolt_cy[half - 1]    # last row of the TOP group

        if pattern == 1:
            # ── Inverted-U on top half (90°-rotated C-bracket) ────────
            # Vertical   : top plate edge → corner_y, LEFT col
            # Horizontal : left_x → right_x at corner_y
            # Vertical   : corner_y → top plate edge, RIGHT col
            scene.addLine(left_x,  MY,       left_x,  corner_y, frac_pen)
            scene.addLine(left_x,  corner_y, right_x, corner_y, frac_pen)
            scene.addLine(right_x, corner_y, right_x, MY,       frac_pen)

        elif pattern == 2:
            # ── Full rectangle through outermost bolt corners ──────────
            scene.addLine(left_x,  top_y, right_x, top_y, frac_pen)
            scene.addLine(left_x,  bot_y, right_x, bot_y, frac_pen)
            scene.addLine(left_x,  top_y, left_x,  bot_y, frac_pen)
            scene.addLine(right_x, top_y, right_x, bot_y, frac_pen)

        elif pattern == 3:
            # ── Two outward L-lines from top plate edge ────────────────
            # Line A (left col):
            #   Vertical   : top plate edge → corner_y at left_x
            #   Horizontal : left_x → LEFT plate edge at corner_y
            scene.addLine(left_x, MY,       left_x,  corner_y, frac_pen)   # vert down
            scene.addLine(left_x, corner_y, MX,      corner_y, frac_pen)   # horiz left to edge

            # Line B (right col):
            #   Vertical   : top plate edge → corner_y at right_x
            #   Horizontal : right_x → RIGHT plate edge at corner_y
            scene.addLine(right_x, MY,       right_x,    corner_y, frac_pen)   # vert down
            scene.addLine(right_x, corner_y, MX + pw,    corner_y, frac_pen)   # horiz right to edge

        # ── Scene rect — exactly the canvas ───────────────────────────
        scene.setSceneRect(0, 0, CANVAS_W, CANVAS_H)

    # ------------------------------------------------------------------
    # Text helper (kept for potential future use)
    # ------------------------------------------------------------------
    def _text(self, scene, text, x, y, align='center'):
        item = scene.addText(text)
        font = QFont()
        font.setPointSize(8)
        item.setFont(font)
        item.setDefaultTextColor(self._fg())
        w = item.boundingRect().width()
        h = item.boundingRect().height()
        if align == 'center':
            item.setPos(x - w / 2, y - h / 2)
        elif align == 'right':
            item.setPos(x - w, y - h / 2)
        else:
            item.setPos(x, y - h / 2)