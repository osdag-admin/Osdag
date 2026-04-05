from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *

from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QSizePolicy, QFrame, QDialog,
    QScrollArea, QSizeGrip, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem
)
from PySide6.QtGui import (
    QPainter, QPen, QFont, QColor, QBrush
)
from PySide6.QtCore import Qt, QRectF


class ColFlangeFractureDialog(QDialog):
    """
    Four fracture-pattern cards stacked vertically for Column Flange fracture.

    Each card:
      LEFT  — bold title + capacity value rows
      RIGHT — portrait plate diagram with bolt grid and fracture lines

    The column diagram is the beam flange diagram rotated 90°:
      • Beam "left half"  (left group of bolt columns) → Column "top half"
        (top group of bolt rows)
      • Fracture lines that were horizontal in beam become vertical in column,
        and vice-versa.
      • "Left plate edge"  in beam → "Top plate edge"  in column
      • "Corner_x" (last bolt of left half) → "corner_y" (last bolt of top half)

    Fracture patterns (90°-rotated equivalents of beam Flange patterns):

      Pattern 1 (beam C-bracket on left half → column inverted-U on top half):
        • Vertical   : top plate edge → corner_y, LEFT bolt column
        • Horizontal : left col → right col at corner_y
        • Vertical   : corner_y → top plate edge, RIGHT bolt column

      Pattern 2 (beam two outward L-lines from left edge →
                 column two outward L-lines from top edge):
        • Line A (left col):  top edge → corner_y,
                              then LEFT to left plate edge
        • Line B (right col): top edge → corner_y,
                              then RIGHT to right plate edge

      Pattern 3 (beam single L bottom-row left→half then UP →
                 column single L right-col top→half then LEFT):
        • Vertical   : top plate edge → corner_y, RIGHT bolt column
        • Horizontal : right col → left plate edge at corner_y

      Pattern 4 (beam two inward L-lines from first bolt column →
                 column two inward L-lines from first/topmost bolt row):
        • Line A (left col):
            Horizontal : left plate edge → right plate edge at top_y  (first bolt row)
                         — only left_x → corner_x portion actually needed;
                         rather: left plate edge → right col at top_y
            Actually the 90°-rotation of beam Pattern 4 is:
              Beam P4: vert UP from first_x to top-plate, horiz right first_x→corner_x
                       vert DOWN from first_x to bot-plate, horiz right first_x→corner_x
              Rotated: horiz LEFT from first_y to left-plate, vert DOWN first_y→corner_y
                       horiz RIGHT from first_y to right-plate, vert DOWN first_y→corner_y
            i.e. two outward T-arms from the FIRST (topmost) bolt row:
              • Line A (left col):
                  Horizontal : first_y, left col → LEFT plate edge
                  Vertical   : first_y → corner_y at left col
              • Line B (right col):
                  Horizontal : first_y, right col → RIGHT plate edge
                  Vertical   : first_y → corner_y at right col
    """

    # Card metadata: (title, pattern_index)
    CARDS = [
        ("Failure Pattern 1 – Tension in Flange and Plate", 1),
        ("Failure Pattern 2 – Tension in Flange and Plate", 2),
        ("Failure Pattern 3 – Tension in Flange and Plate", 3),
        ("Failure Pattern 4 – Tension in Flange and Plate", 4),
    ]

    def __init__(self, main, fn):
        super().__init__()

        app = QApplication.instance()
        self.theme = app.theme_manager
        self.main  = main
        self.fn    = fn

        # ── Geometry — row/col counts for the COLUMN flange plate ────
        # bolts_one_line → number of bolt columns (vertical lines)
        # bolt_line      → number of bolt rows    (horizontal lines)
        self.rows = int(main.flange_plate.bolts_one_line)
        self.cols = int(main.flange_plate.bolt_line)

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
            print(f"[ColumnFlangeFractureDialog] parse error: {e}")
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
    # Main content — 4 cards, vertical scroll on dialog only
    # ------------------------------------------------------------------
    def _build_ui(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = 1200, 860
        x = screen_geometry.x() + (screen_geometry.width()  - width)  // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

        outer = QVBoxLayout(self.content_widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Dialog scrolls vertically only
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        outer.addWidget(scroll)

        container = QWidget()
        container.setObjectName("cff_container")
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
        card.setObjectName("cff_card")
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
        title_lbl.setObjectName("cff_card_title")
        title_lbl.setWordWrap(True)
        f = title_lbl.font()
        f.setBold(True)
        title_lbl.setFont(f)
        ll.addWidget(title_lbl)
        ll.addSpacing(6)

        for lbl_text, val_text in self._cap_rows:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(6)
            lbl = QLabel(lbl_text)
            lbl.setObjectName("cff_left_label")
            lbl.setWordWrap(True)
            val = QLabel(val_text)
            val.setObjectName("cff_left_value")
            val.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            row_layout.addWidget(lbl, 1)
            row_layout.addWidget(val)
            ll.addLayout(row_layout)

        ll.addStretch()
        layout.addWidget(left)

        # ── RIGHT: diagram — horizontal scroll only ─────────────────
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
    # Core drawing — 90° rotation of the beam flange diagram.
    #
    # The beam flange diagram is LANDSCAPE:
    #   • rows  = horizontal bolt lines (bolts_one_line)
    #   • cols  = two groups of vertical bolt columns (bolt_line), left half / right half
    #   • "left half" = first  cols//2 columns
    #   • "corner_x"  = x of the last bolt in the left half
    #   • fracture lines are anchored at the left plate edge and corner_x
    #
    # For the COLUMN diagram we rotate 90° clockwise so:
    #   • The plate is PORTRAIT  (CANVAS_W < CANVAS_H)
    #   • What were "rows"  → now vertical bolt COLUMNS  (num_vcols = self.rows)
    #   • What were "cols"  → now horizontal bolt ROWS   (num_hrows = self.cols)
    #   • "Left half"       → "Top half"  (top num_hrows//2 rows)
    #   • "corner_x"        → "corner_y"  (y of last bolt in top half)
    #   • "Left plate edge" → "Top plate edge"  (y = MY)
    #   • Beam horizontal lines  → column vertical lines
    #   • Beam vertical lines    → column horizontal lines
    #
    # Variable naming:
    #   bolt_cx[c]  — x of vertical bolt COLUMN  c  (c in 0..num_vcols-1)
    #   bolt_cy[r]  — y of horizontal bolt ROW    r  (r in 0..num_hrows-1)
    #   half        — number of rows in TOP group  = num_hrows // 2
    #   corner_y    — bolt_cy[half - 1]
    #   first_y     — bolt_cy[0]   (topmost bolt row)
    #
    # Fracture patterns (column / rotated):
    # ──────────────────────────────────────
    # Pattern 1 — inverted-U on top half:
    #   • Vertical   : top plate edge (MY) → corner_y,  at left_x
    #   • Horizontal : left_x → right_x  at corner_y
    #   • Vertical   : corner_y → top plate edge (MY),  at right_x
    #
    # Pattern 2 — two outward L-lines from top plate edge:
    #   • Line A (left col):
    #       Vertical   : top edge → corner_y  at left_x
    #       Horizontal : left_x → LEFT plate edge  at corner_y
    #   • Line B (right col):
    #       Vertical   : top edge → corner_y  at right_x
    #       Horizontal : right_x → RIGHT plate edge  at corner_y
    #
    # Pattern 3 — single L: right col top→corner, then LEFT to left plate edge:
    #   • Vertical   : top plate edge → corner_y  at right_x
    #   • Horizontal : right_x → LEFT plate edge  at corner_y
    #
    # Pattern 4 — two inward L-lines anchored at first (topmost) bolt row:
    #   • Line A (left col):
    #       Horizontal : first_y, left_x → LEFT plate edge
    #       Vertical   : left_x,  first_y → corner_y
    #   • Line B (right col):
    #       Horizontal : first_y, right_x → RIGHT plate edge
    #       Vertical   : right_x, first_y → corner_y
    # ------------------------------------------------------------------
    def _draw_plate(self, scene, pattern=1):

        # ── Portrait canvas ───────────────────────────────────────────
        CANVAS_W = 220    # narrower (was CANVAS_H in beam)
        CANVAS_H = 340    # taller   (was CANVAS_W in beam)
        MX       = 20
        MY       = 20

        # In column orientation:
        #   self.rows → number of vertical bolt COLUMNS  (beam bolts_one_line)
        #   self.cols → number of horizontal bolt ROWS   (beam bolt_line)
        num_vcols = self.rows
        num_hrows = self.cols
        half      = max(1, num_hrows // 2)   # rows in the TOP group

        pw = CANVAS_W - 2 * MX
        ph = CANVAS_H - 2 * MY

        # ── Derived bolt spacing ──────────────────────────────────────
        pad_x = pw * 0.15
        pad_y = ph * 0.12

        # Horizontal spacing between vertical bolt columns (simple equal spacing)
        avail_w = pw - 2 * pad_x
        gauge_x = avail_w / (num_vcols - 1) if num_vcols > 1 else avail_w

        # Vertical spacing between rows — two groups + mid_gap
        #   2*(half-1)*g + 1.5*g = avail_h  (same formula as beam, applied vertically)
        avail_h = ph - 2 * pad_y
        gauge_y = avail_h / (2 * (half - 1) + 1.5) if half > 1 else avail_h / 2.5
        mid_gap = gauge_y * 1.5

        bolt_r = min(gauge_x, gauge_y) * 0.28

        # ── Bolt centre x-coordinates (vertical columns, equally spaced) ──
        h_offset = MX + pad_x
        bolt_cx  = [h_offset + c * gauge_x for c in range(num_vcols)]

        # ── Bolt centre y-coordinates (horizontal rows, two groups) ──────
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
        for c in range(num_vcols):
            for r_idx in range(num_hrows):
                cx, cy = bolt_cx[c], bolt_cy[r_idx]
                scene.addEllipse(cx - bolt_r, cy - bolt_r,
                                 2 * bolt_r, 2 * bolt_r, hole_pen)

        # ── Fracture line pen ─────────────────────────────────────────
        frac_pen = QPen(QColor("#3A7FD5"), 1.5)
        frac_pen.setStyle(Qt.DashLine)

        left_x   = bolt_cx[0]           # leftmost bolt column x
        right_x  = bolt_cx[-1]          # rightmost bolt column x
        corner_y = bolt_cy[half - 1]    # last row of TOP group
        first_y  = bolt_cy[0]           # topmost bolt row y

        if pattern == 1:
            # ── Inverted-U on top half ─────────────────────────────────
            # Vertical   : top plate edge → corner_y,  LEFT col
            # Horizontal : left_x → right_x  at corner_y
            # Vertical   : corner_y → top plate edge,  RIGHT col
            scene.addLine(left_x,  MY,       left_x,  corner_y, frac_pen)
            scene.addLine(left_x,  corner_y, right_x, corner_y, frac_pen)
            scene.addLine(right_x, corner_y, right_x, MY,       frac_pen)

        elif pattern == 2:
            # ── Two outward L-lines from top plate edge ────────────────
            # Line A (left col):
            #   Vertical   : top edge → corner_y  at left_x
            #   Horizontal : left_x → LEFT plate edge  at corner_y
            scene.addLine(left_x, MY,       left_x,  corner_y, frac_pen)   # vert down
            scene.addLine(left_x, corner_y, MX,      corner_y, frac_pen)   # horiz to left edge

            # Line B (right col):
            #   Vertical   : top edge → corner_y  at right_x
            #   Horizontal : right_x → RIGHT plate edge  at corner_y
            scene.addLine(right_x, MY,       right_x,    corner_y, frac_pen)  # vert down
            scene.addLine(right_x, corner_y, MX + pw,    corner_y, frac_pen)  # horiz to right edge

        elif pattern == 3:
            # ── Single L: right col top→corner, then LEFT to left plate edge ─
            # Vertical   : top plate edge → corner_y  at right_x
            # Horizontal : right_x → LEFT plate edge  at corner_y
            scene.addLine(right_x, MY,       right_x, corner_y, frac_pen)  # vert down
            scene.addLine(right_x, corner_y, MX,      corner_y, frac_pen)  # horiz to left edge

        elif pattern == 4:
            # ── Two inward L-lines anchored at first (topmost) bolt row ──
            # The horizontal runs outward from each bolt column to the plate edge,
            # and the vertical extends downward to corner_y.
            #
            # Line A (left col):
            #   Horizontal : first_y, left_x → LEFT plate edge
            #   Vertical   : left_x, first_y → corner_y
            scene.addLine(left_x,  first_y, MX,       first_y, frac_pen)   # horiz to left edge
            scene.addLine(left_x,  first_y, left_x,  corner_y, frac_pen)   # vert down to corner

            # Line B (right col):
            #   Horizontal : first_y, right_x → RIGHT plate edge
            #   Vertical   : right_x, first_y → corner_y
            scene.addLine(right_x, first_y, MX + pw,  first_y, frac_pen)   # horiz to right edge
            scene.addLine(right_x, first_y, right_x, corner_y, frac_pen)   # vert down to corner

        # ── Scene rect — exactly the canvas ───────────────────────────
        scene.setSceneRect(0, 0, CANVAS_W, CANVAS_H)