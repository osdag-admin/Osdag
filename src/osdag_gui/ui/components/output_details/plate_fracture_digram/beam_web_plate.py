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


class BeamWebFractureDialog(QDialog):
    """
    Three fracture-pattern cards stacked vertically.

    Each card:
      LEFT  — bold title + capacity value rows
      RIGHT — landscape plate diagram with bolt grid and fracture lines

    Fracture patterns (matching Images 1, 2, 3):
      Pattern 1 (Image 1):
        • Horizontal dashed line through top-row bolt centres
        • Vertical dashed line from top-row rightmost bolt DOWN to bottom-row rightmost bolt
        (reversed-L on the RIGHT side)

      Pattern 2 (Image 2):
        • Horizontal dashed line through top-row bolt centres (full width)
        • Horizontal dashed line through bottom-row bolt centres (full width)
        • Vertical dashed line connecting LEFT ends of the two horizontals
        • Vertical dashed line connecting RIGHT ends of the two horizontals
        (closed rectangle through all bolt centres)

      Pattern 3 (Image 3):
        • Same as Pattern 1 but the horizontal line only spans up to the
          rightmost bolt, and the vertical drop is on the RIGHT side — identical
          visual to Pattern 1 (the reference images show the same L-shape
          with the arm on the right).
        NOTE: To give Pattern 3 a distinct identity we draw the L mirrored:
          • Horizontal dashed line through BOTTOM-row bolt centres
          • Vertical dashed line from bottom-row rightmost bolt UP to top-row rightmost bolt
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

        # ── Geometry — only row/col counts needed for drawing ────────
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
            print(f"[WebFractureDialog] parse error: {e}")
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
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
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
        container.setObjectName("wf_container")
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
        card.setObjectName("wf_card")
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
        title_lbl.setObjectName("wf_card_title")
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
            lbl.setObjectName("wf_left_label")
            lbl.setWordWrap(True)
            val = QLabel(val_text)
            val.setObjectName("wf_left_value")
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
    # Core drawing — fixed canvas, all spacing derived from rows/cols only.
    # No real mm values are used; the diagram always fits the view.
    #
    # Canvas:  CANVAS_W × CANVAS_H  (landscape, fixed pixels)
    # Margins: MX left/right,  MY top/bottom  (inside canvas)
    # Plate fills the inner area:  pw = CANVAS_W - 2*MX,  ph = CANVAS_H - 2*MY
    # Bolt grid is centred inside the plate with a proportional middle gap.
    # ------------------------------------------------------------------
    def _draw_plate(self, scene, pattern=1):
        # ── Fixed canvas constants ────────────────────────────────────
        CANVAS_W = 340
        CANVAS_H = 220
        MX       = 20    # horizontal margin (plate left/right inset)
        MY       = 20    # vertical   margin (plate top/bottom inset)

        rows = self.rows
        cols = self.cols
        half = max(1, cols // 2)   # cols in each half-group

        pw = CANVAS_W - 2 * MX    # plate pixel width
        ph = CANVAS_H - 2 * MY    # plate pixel height

        # ── Derived bolt spacing — fit grid inside plate with padding ─
        pad_x   = pw * 0.12        # horizontal padding inside plate per side
        pad_y   = ph * 0.15        # vertical   padding inside plate per side

        # Each half-group spans  (half-1)*gauge  pixels.
        # Two halves + mid_gap must fit in  pw - 2*pad_x.
        # We give mid_gap = 1.5 * gauge  so:  2*(half-1)*g + 1.5*g = avail_w
        # → g = avail_w / (2*(half-1) + 1.5)
        avail_w  = pw - 2 * pad_x
        gauge    = avail_w / (2 * (half - 1) + 1.5) if half > 1 else avail_w / 2.5
        mid_gap  = gauge * 1.5

        avail_h  = ph - 2 * pad_y
        pitch    = avail_h / (rows - 1) if rows > 1 else avail_h

        # Bolt radius — slightly smaller than half the min spacing
        r = min(gauge, pitch) * 0.28

        # ── Bolt centre coordinates ───────────────────────────────────
        half_span   = (half - 1) * gauge
        total_bolt_w = half_span * 2 + mid_gap
        h_offset    = MX + (pw - total_bolt_w) / 2    # x of col 0

        bolt_cx = []
        for c in range(cols):
            if c < half:
                bolt_cx.append(h_offset + c * gauge)
            else:
                bolt_cx.append(h_offset + half_span + mid_gap + (c - half) * gauge)

        v_offset = MY + pad_y
        bolt_cy  = [v_offset + ri * pitch for ri in range(rows)]

        fg = self._fg()

        # ── Plate ────────────────────────────────────────────────────
        rect = QGraphicsRectItem(QRectF(MX, MY, pw, ph))
        rect.setPen(QPen(fg, 2.0))
        rect.setBrush(self._plate_brush())
        scene.addItem(rect)

        # ── Bolt holes ───────────────────────────────────────────────
        hole_pen = QPen(fg, 1.5)
        for c in range(cols):
            for ri in range(rows):
                cx, cy = bolt_cx[c], bolt_cy[ri]
                scene.addEllipse(cx - r, cy - r, 2*r, 2*r, hole_pen)

        # ── Fracture line pen ────────────────────────────────────────
        frac_pen = QPen(QColor("#3A7FD5"), 1.5)
        frac_pen.setStyle(Qt.DashLine)

        top_y    = bolt_cy[0]
        bot_y    = bolt_cy[-1]
        left_x   = bolt_cx[0]
        right_x  = bolt_cx[-1]
        corner_x = bolt_cx[half - 1]   # last bolt of left half

        if pattern == 1:
            # C-bracket on left half: top horiz → corner vert down → bot horiz back
            scene.addLine(MX,       top_y, corner_x, top_y, frac_pen)
            scene.addLine(corner_x, top_y, corner_x, bot_y, frac_pen)
            scene.addLine(corner_x, bot_y, MX,       bot_y, frac_pen)

        elif pattern == 2:
            # Full rectangle connecting outermost bolt corners
            scene.addLine(left_x,  top_y, right_x, top_y, frac_pen)
            scene.addLine(left_x,  bot_y, right_x, bot_y, frac_pen)
            scene.addLine(left_x,  top_y, left_x,  bot_y, frac_pen)
            scene.addLine(right_x, top_y, right_x, bot_y, frac_pen)

        elif pattern == 3:
            # Two L-lines: top row goes left→corner then UP to plate edge;
            #              bottom row goes left→corner then DOWN to plate edge
            scene.addLine(MX,       top_y, corner_x, top_y, frac_pen)   # top horiz
            scene.addLine(corner_x, top_y, corner_x, MY,    frac_pen)   # up to top edge

            scene.addLine(MX,       bot_y, corner_x, bot_y,    frac_pen)  # bot horiz
            scene.addLine(corner_x, bot_y, corner_x, MY + ph,  frac_pen)  # down to bot edge

        # ── Scene rect — exactly the canvas ──────────────────────────
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