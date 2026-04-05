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


class BeamFlangeFractureDialog(QDialog):
    """
    Four fracture-pattern cards stacked vertically for Flange fracture.

    Each card:
      LEFT  — bold title + capacity value rows
      RIGHT — landscape plate diagram with bolt grid and fracture lines

    Fracture patterns:

      Pattern 1  (same as Web Pattern 1):
        C-bracket on LEFT HALF only, opening leftward:
          • Horizontal: left plate edge → last bolt of left half, TOP row
          • Vertical  : down to BOTTOM row at same x
          • Horizontal: back to left plate edge, BOTTOM row

      Pattern 2  (same as Web Pattern 3):
        Two separate L-lines:
          • Top row   : horizontal left edge → last bolt of left half,
                        then vertical UP   to top plate edge
          • Bottom row: horizontal left edge → last bolt of left half,
                        then vertical DOWN to bottom plate edge

      Pattern 3:
        Single L-line using BOTTOM row only:
          • Horizontal: left plate edge → last bolt of left half, BOTTOM row
          • Vertical  : UP to top plate edge at same x

      Pattern 4  (Image 3 — two outward L-lines from FIRST bolt):
        Two L-lines anchored at the FIRST (leftmost) bolt:
          • Top row   : horizontal first bolt → last bolt of left half,
                        then vertical UP   to top plate edge from FIRST bolt x
          • Bottom row: horizontal first bolt → last bolt of left half,
                        then vertical DOWN to bottom plate edge from FIRST bolt x
        i.e. the vertical segment is on the LEFT side (first bolt column),
        and the horizontal runs rightward to the end of the left half.
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

        # ── Geometry — only row/col counts needed for drawing ────────
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
            print(f"[FlangeFractureDialog] parse error: {e}")
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
        container.setObjectName("ff_container")
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
        card.setObjectName("ff_card")
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
        title_lbl.setObjectName("ff_card_title")
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
            lbl.setObjectName("ff_left_label")
            lbl.setWordWrap(True)
            val = QLabel(val_text)
            val.setObjectName("ff_left_value")
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
    # Horizontal scroll per diagram; vertical scroll handled by dialog.
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
    # Core drawing — fixed canvas, all spacing derived from rows/cols only.
    # No real mm values; diagram always fits the view without overflow.
    #
    # Canvas  : CANVAS_W × CANVAS_H  (landscape, fixed pixels)
    # Margins : MX (left/right),  MY (top/bottom)  inside the canvas
    # Plate   : pw = CANVAS_W - 2*MX,  ph = CANVAS_H - 2*MY
    # Bolt grid centred inside the plate with a proportional middle gap.
    #
    # Fracture patterns
    # -----------------
    # Pattern 1 — C-bracket on left half (same as Web P1)
    # Pattern 2 — Two outward L-lines from left edge (same as Web P3)
    # Pattern 3 — Single L: bottom row left→half, then UP to top border
    # Pattern 4 — Two inward L-lines anchored at first bolt column:
    #               top row   : vert UP from first-bolt x, horiz right to half
    #               bottom row: vert DOWN from first-bolt x, horiz right to half
    # ------------------------------------------------------------------
    def _draw_plate(self, scene, pattern=1):

        # ── Fixed canvas ─────────────────────────────────────────────
        CANVAS_W = 340
        CANVAS_H = 220
        MX       = 20
        MY       = 20

        rows = self.rows
        cols = self.cols
        half = max(1, cols // 2)

        pw = CANVAS_W - 2 * MX
        ph = CANVAS_H - 2 * MY

        # ── Derived bolt spacing ──────────────────────────────────────
        pad_x  = pw * 0.12
        pad_y  = ph * 0.15

        avail_w = pw - 2 * pad_x
        gauge   = avail_w / (2 * (half - 1) + 1.5) if half > 1 else avail_w / 2.5
        mid_gap = gauge * 1.5

        avail_h = ph - 2 * pad_y
        pitch   = avail_h / (rows - 1) if rows > 1 else avail_h

        r = min(gauge, pitch) * 0.28   # bolt radius

        # ── Bolt centre coordinates ───────────────────────────────────
        half_span    = (half - 1) * gauge
        total_bolt_w = half_span * 2 + mid_gap
        h_offset     = MX + (pw - total_bolt_w) / 2   # x of col 0

        bolt_cx = []
        for c in range(cols):
            if c < half:
                bolt_cx.append(h_offset + c * gauge)
            else:
                bolt_cx.append(h_offset + half_span + mid_gap + (c - half) * gauge)

        v_offset = MY + pad_y
        bolt_cy  = [v_offset + ri * pitch for ri in range(rows)]

        fg = self._fg()

        # ── Plate ─────────────────────────────────────────────────────
        rect = QGraphicsRectItem(QRectF(MX, MY, pw, ph))
        rect.setPen(QPen(fg, 2.0))
        rect.setBrush(self._plate_brush())
        scene.addItem(rect)

        # ── Bolt holes ────────────────────────────────────────────────
        hole_pen = QPen(fg, 1.5)
        for c in range(cols):
            for ri in range(rows):
                cx, cy = bolt_cx[c], bolt_cy[ri]
                scene.addEllipse(cx - r, cy - r, 2 * r, 2 * r, hole_pen)

        # ── Fracture line pen ─────────────────────────────────────────
        frac_pen = QPen(QColor("#3A7FD5"), 1.5)
        frac_pen.setStyle(Qt.DashLine)

        top_y    = bolt_cy[0]
        bot_y    = bolt_cy[-1]
        corner_x = bolt_cx[half - 1]   # last bolt of left half
        first_x  = bolt_cx[0]          # first (leftmost) bolt

        if pattern == 1:
            # ── C-bracket on left half (identical to Web P1) ──────────
            # Horizontal top  : left plate edge → corner_x, top row
            # Vertical        : corner_x, top row → corner_x, bottom row
            # Horizontal bot  : corner_x → left plate edge, bottom row
            scene.addLine(MX,       top_y, corner_x, top_y, frac_pen)
            scene.addLine(corner_x, top_y, corner_x, bot_y, frac_pen)
            scene.addLine(corner_x, bot_y, MX,       bot_y, frac_pen)

        elif pattern == 2:
            # ── Two outward L-lines from left edge (identical to Web P3) ─
            # Line A (top row): left edge → corner_x, then UP to top border
            # Line B (bot row): left edge → corner_x, then DOWN to bot border
            scene.addLine(MX,       top_y, corner_x, top_y, frac_pen)  # top horiz
            scene.addLine(corner_x, top_y, corner_x, MY,    frac_pen)  # up to top edge

            scene.addLine(MX,       bot_y, corner_x, bot_y,   frac_pen)  # bot horiz
            scene.addLine(corner_x, bot_y, corner_x, MY + ph, frac_pen)  # down to bot edge

        elif pattern == 3:
            # ── Single L: bottom row left→corner, then UP to top border ─
            # Horizontal: left plate edge → corner_x, BOTTOM row
            # Vertical  : corner_x, bottom row → corner_x, top plate edge
            scene.addLine(MX,       bot_y, corner_x, bot_y, frac_pen)  # bot horiz
            scene.addLine(corner_x, bot_y, corner_x, MY,    frac_pen)  # up to top edge

        elif pattern == 4:
            # ── Two inward L-lines anchored at first bolt column ──────
            # The vertical runs from the first bolt outward to the plate border,
            # and the horizontal extends rightward to corner_x.
            #
            # Line A (top row):
            #   Vertical   : first_x, top row → first_x, TOP plate edge
            #   Horizontal : first_x, top row → corner_x, top row
            #
            # Line B (bottom row):
            #   Vertical   : first_x, bottom row → first_x, BOTTOM plate edge
            #   Horizontal : first_x, bottom row → corner_x, bottom row
            scene.addLine(first_x, top_y, first_x, MY,       frac_pen)  # up to top edge
            scene.addLine(first_x, top_y, corner_x, top_y,   frac_pen)  # top horiz right

            scene.addLine(first_x, bot_y, first_x, MY + ph,  frac_pen)  # down to bot edge
            scene.addLine(first_x, bot_y, corner_x, bot_y,   frac_pen)  # bot horiz right

        # ── Scene rect — exactly the canvas ───────────────────────────
        scene.setSceneRect(0, 0, CANVAS_W, CANVAS_H)