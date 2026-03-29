
from PySide6.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
    QGraphicsScene, QScrollArea
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import (
    QPainter, QPen, QFont, QColor, QPolygonF, QBrush
)

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *


class SeatedAngleCapacityDetails(QDialog):
    def __init__(self, connection_obj, rows=0, cols=0, main=None):
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager
        self.connection = connection_obj
        self.main = main

        # ---------------- geometry ----------------
        self.plate_width = float(main.seated_angle.width)
        self.plate_height = float(main.seated_angle.leg_a_length)
        self.hole_dia = float(main.bolt.bolt_diameter_provided)

        self.rows = max(1, int(getattr(main.bolt, "bolt_row", 1) or 1))
        self.cols = max(1, int(getattr(main.bolt, "bolt_col", 1) or 1))

        # ---------------- output dictionary ----------------
        output = main.output_values(True)
        dict1 = {i[0]: i[3] for i in output if i[0]}

        # ---------------- plate capacity values ----------------
        cap_fn = dict1[KEY_OUT_PLATE_CAPACITIES][1]
        cap_details = cap_fn(True)
        dd = {i[1]: i[3] for i in cap_details if len(i) > 3}

        def _v(label):
            val = dd.get(label, "N/A")
            try:
                return round(float(val), 3)
            except Exception:
                return "N/A"

        self.shear_demand = _v(KEY_OUT_DISP_PLATE_SHEAR_DEMAND)
        self.shear_capacity = _v(KEY_OUT_DISP_PLATE_SHEAR)
        self.moment_demand = _v(KEY_OUT_DISP_PLATE_MOM_DEMAND)
        self.moment_capacity = _v(KEY_OUT_DISP_PLATE_MOM_CAPACITY)

        self.dict_shear_failure = {
            "Shear Yielding Capacity (kN)": self.shear_capacity,
            "Shear Demand (kN)": self.shear_demand,
        }

        self.dict_moment_failure = {
            "Moment Demand (kNm)": self.moment_demand,
            "Moment Capacity (kNm)": self.moment_capacity,
        }

        # ---------------- section capacity values ----------------
        try:
            sec_fn = dict1["button_section_capacity"][1]
            sec_details = sec_fn(True)
            sec_dd = {i[1]: i[3] for i in sec_details if len(i) > 3}
        except Exception:
            sec_dd = {}

        self.dict_section_failure = {
            "Supported Section Shear Yielding Capacity (kN)": sec_dd.get(
                "Supported Section Shear Yielding Capacity (kN)", "N/A"
            ),
            "Supported Section Allowable Shear Capacity (kN)": sec_dd.get(
                "Supported Section Allowable Shear Capacity (kN)", "N/A"
            ),
            "Supporting Section Tension Yielding Capacity (kN)": sec_dd.get(
                "Supporting Section Tension Yielding Capacity (kN)", "N/A"
            ),
        }

        # ---------------- spacing values ----------------
        self.spacing = self._get_spacing_values()

        self.initUI()

    # ------------------------------------------------------------------
    # wrapper
    # ------------------------------------------------------------------
    def setupWrapper(self, title="Capacity Details"):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setObjectName("spacing_capacity_details")

        ml = QVBoxLayout(self)
        ml.setContentsMargins(1, 1, 1, 1)
        ml.setSpacing(0)

        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle(title)
        ml.addWidget(self.title_bar)

        self.content_widget = QWidget(self)
        ml.addWidget(self.content_widget, 1)

        sg = QSizeGrip(self)
        sg.setFixedSize(16, 16)

        ov = QHBoxLayout()
        ov.setContentsMargins(0, 0, 4, 4)
        ov.addStretch(1)
        ov.addWidget(sg, 0, Qt.AlignBottom | Qt.AlignRight)
        ml.addLayout(ov)

    # ------------------------------------------------------------------
    # spacing extraction
    # ------------------------------------------------------------------
    def _safe_float(self, value, default=0.0):
        try:
            return float(value)
        except Exception:
            return default

    def _get_spacing_values(self):
        """
        Pull seated-angle spacing values from the actual design object.
        This keeps capacity details aligned with spacing details dialog.
        """
        bolt = self.main.bolt

        end_dist = self._safe_float(getattr(bolt, "seated_angle_end_column", 0.0))
        edge_dist = self._safe_float(getattr(bolt, "seated_angle_edge_column", 0.0))
        pitch = self._safe_float(getattr(bolt, "min_pitch_round", 0.0)) if self.rows > 1 else 0.0

        gauge_central = self._safe_float(getattr(bolt, "seated_angle_gauge_column", 0.0))
        gauge = self._safe_float(getattr(bolt, "min_gauge_round", 0.0))

        # For seated angle capacity picture, use central gauge first.
        # If unavailable, use min_gauge_round.
        effective_gauge = gauge_central if gauge_central > 0 else gauge

        return {
            "end": end_dist,
            "edge": edge_dist,
            "pitch": pitch,
            "gauge": effective_gauge,
            "gauge_central": gauge_central,
            "gauge_side": gauge,
            "hole": self.hole_dia,
            "width": self.plate_width,
            "height": self.plate_height,
        }

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def initUI(self):
        self.setupWrapper("Capacity Details")

        sg = QApplication.primaryScreen().availableGeometry()
        w, h = 1150, 800
        self.setGeometry(
            sg.x() + (sg.width() - w) // 2,
            sg.y() + (sg.height() - h) // 2,
            w, h
        )

        cl = QVBoxLayout(self.content_widget)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        sa.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll = QWidget()
        scroll.setObjectName("spacing_scroll_widget")

        main_layout = QHBoxLayout(scroll)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(18)

        # ---------------- LEFT PANEL ----------------
        lp = QWidget()
        lp.setMaximumWidth(400)
        ll = QVBoxLayout(lp)
        ll.setSpacing(5)

        note = QLabel("Note: Representative image for\nFailure Pattern")
        note.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        note.setWordWrap(True)
        ll.addWidget(note)

        def add_section(title, data):
            lbl = QLabel(title)
            lbl.setStyleSheet(
                "font-size: 14px; font-weight: bold;"
                "margin-top: 15px; margin-bottom: 5px;"
            )
            lbl.setWordWrap(True)
            ll.addWidget(lbl)

            for key, val in data.items():
                row = QHBoxLayout()
                row.setContentsMargins(0, 2, 0, 2)

                text_label = QLabel(key)
                text_label.setWordWrap(True)
                row.addWidget(text_label, 1)

                row.addStretch()

                v = QLabel(str(val))
                v.setStyleSheet("font-size: 12px; font-weight: bold;")
                row.addWidget(v, 0)

                ll.addLayout(row)

        add_section("Failure Pattern due to Shear in Plate", self.dict_shear_failure)
        add_section("Failure Pattern due to Moment in Plate", self.dict_moment_failure)
        ll.addStretch()

        # ---------------- RIGHT PANEL ----------------
        rp = QWidget()
        rl = QVBoxLayout(rp)
        rl.setSpacing(10)

        def make_view(scene, draw_fn):
            v = QGraphicsView(scene)
            v.setBackgroundBrush(
                QBrush(Qt.white) if self.theme.is_light()
                else QBrush(QColor("#4A4A4A"))
            )
            v.setRenderHint(QPainter.Antialiasing)
            v.setMinimumWidth(350)
            v.setMinimumHeight(220)
            v.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            v.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            draw_fn(scene)
            v.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
            return v

        lb1 = QLabel("Failure Pattern due to Shear in Plate:")
        lb1.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        rl.addWidget(lb1)

        self.scene1 = QGraphicsScene()
        self.view1 = make_view(self.scene1, self.createShearDrawing)
        rl.addWidget(self.view1)

        lb2 = QLabel("Failure Pattern due to Moment in Plate:")
        lb2.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin-bottom: 5px; margin-top: 10px;"
        )
        rl.addWidget(lb2)

        self.scene2 = QGraphicsScene()
        self.view2 = make_view(self.scene2, self.createMomentDrawing)
        rl.addWidget(self.view2)

        main_layout.addWidget(lp, 1)
        main_layout.addWidget(rp, 2)

        sa.setWidget(scroll)
        cl.addWidget(sa)

    # ------------------------------------------------------------------
    # common helpers
    # ------------------------------------------------------------------
    def _sc(self, coeff=3):
        s = self.spacing
        return {
            "width": s["width"] / coeff,
            "height": s["height"] / coeff,
            "hole": s["hole"] / coeff,
            "end": s["end"] / coeff,
            "edge": s["edge"] / coeff,
            "gauge": s["gauge"] / coeff,
            "pitch": s["pitch"] / coeff,
        }

    def _pens(self, coeff=2):
        outline = QPen(Qt.blue, 2 / coeff)

        if self.theme.is_light():
            dim = QPen(Qt.black, 1.5 / coeff)
            dash = QPen(Qt.black, 1.5 / coeff, Qt.DashLine)
            text_color = Qt.black
        else:
            dim = QPen(QColor("#D0D0D0"), 1.5 / coeff)
            dash = QPen(QColor("#D0D0D0"), 1.5 / coeff, Qt.DashLine)
            text_color = Qt.white

        return outline, dim, dash, text_color

    def _get_reference_bolts(self, s, w, h, for_moment=False):
        """
        Representative bolt row.
        For plate shear -> use top bolt row.
        For plate moment -> use mid-height representative row.
        """
        if self.cols <= 1:
            left_x = w / 2
            right_x = w / 2
        else:
            left_x = s["edge"]
            right_x = s["edge"] + s["gauge"]

            max_right = w - s["edge"]
            if right_x > max_right or right_x <= left_x:
                left_x = w * 0.25
                right_x = w * 0.75

        bolt_y = h * 0.50 if for_moment else s["end"]
        return [(left_x, bolt_y), (right_x, bolt_y)]

    # ------------------------------------------------------------------
    # plate drawings
    # ------------------------------------------------------------------
    def createShearDrawing(self, scene):
        coeff = 2
        s = self._sc(coeff)
        outline, dim, dash, _ = self._pens(coeff)

        w, h = s["width"], s["height"]

        top_margin = 35 / coeff
        bottom_margin = 55 / coeff
        left_margin = 35 / coeff
        right_margin = 45 / coeff

        scene.clear()
        scene.setSceneRect((-left_margin), (-top_margin),
                           w + left_margin + right_margin,
                           h + top_margin + bottom_margin)

        # plate
        strip_h = h * 0.12
        scene.addRect(0, 0, w, strip_h, dim, QBrush(QColor("#C0C0C0")))
        scene.addRect(0, 0, w, h, dim)

        row0 = self._get_reference_bolts(s, w, h, for_moment=False)

        # bolt holes
        for cx, cy in row0:
            scene.addEllipse(cx - s["hole"] / 2, cy - s["hole"] / 2,
                             s["hole"], s["hole"], outline)

        # failure path
        scene.addLine(row0[0][0], row0[0][1], row0[1][0], row0[1][1], dash)
        for cx, cy in row0:
            scene.addLine(cx, cy, cx, h, dash)

        self._addPlateDimensions(scene, w, h, s, dim, coeff)

    def createMomentDrawing(self, scene):
        coeff = 2
        s = self._sc(coeff)
        outline, dim, dash, _ = self._pens(coeff)

        w, h = s["width"], s["height"]

        top_margin = 35 / coeff
        bottom_margin = 55 / coeff
        left_margin = 35 / coeff
        right_margin = 45 / coeff

        scene.clear()
        scene.setSceneRect((-left_margin), (-top_margin),
                           w + left_margin + right_margin,
                           h + top_margin + bottom_margin)

        # plate
        strip_h = h * 0.12
        scene.addRect(0, 0, w, strip_h, dim, QBrush(QColor("#C0C0C0")))
        scene.addRect(0, 0, w, h, dim)

        row0 = self._get_reference_bolts(s, w, h, for_moment=True)

        # bolt holes
        for cx, cy in row0:
            scene.addEllipse(cx - s["hole"] / 2, cy - s["hole"] / 2,
                             s["hole"], s["hole"], outline)

        # failure path
        scene.addLine(0, row0[0][1], row0[1][0], row0[1][1], dash)
        cx, cy = row0[1]
        scene.addLine(cx, cy, cx, h, dash)

        self._addPlateDimensions(scene, w, h, s, dim, coeff)

    def _addPlateDimensions(self, scene, width, height, s, pen, coeff):
        ho = 20 / coeff
        vo = 30 / coeff

        x1 = 0
        x2 = s["edge"]
        x3 = s["edge"] + s["gauge"]
        x4 = width

        # top horizontal dimensions
        self.addHorizontalDimension(scene, x1, -ho, x2, -ho, f"{s['edge']:.1f}", pen)
        self.addHorizontalDimension(scene, x2, -ho, x3, -ho, f"{s['gauge']:.1f}", pen)
        self.addHorizontalDimension(scene, x3, -ho, x4, -ho, f"{max(0.0, width - x3):.1f}", pen)

        # bottom total width
        self.addHorizontalDimension(
            scene, 0, height + ho, width, height + ho, f"{width:.1f} mm", pen
        )

        # right vertical dimensions
        self.addVerticalDimension(
            scene, width + vo, 0, width + vo, s["end"], f"{s['end']:.1f}", pen
        )
        self.addVerticalDimension(
            scene, width + vo, s["end"], width + vo, height,
            f"{max(0.0, height - s['end']):.1f}", pen
        )

        # left total
        self.addVerticalDimension(
            scene, -vo, 0, -vo, height, f"{height:.1f}", pen
        )

    # ------------------------------------------------------------------
    # shared dimension methods
    # ------------------------------------------------------------------
    def addHorizontalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)

        ext = 10
        arr = 2
        scene.addLine(x1, y1 - ext / 2, x1, y1 + ext / 2, pen)
        scene.addLine(x2, y2 - ext / 2, x2, y2 + ext / 2, pen)

        fill = QBrush(Qt.black) if self.theme.is_light() else QBrush(QColor("#D0D0D0"))

        for pts in [
            [(x1, y1), (x1 + arr, y1 - arr / 2), (x1 + arr, y1 + arr / 2)],
            [(x2, y2), (x2 - arr, y2 - arr / 2), (x2 - arr, y2 + arr / 2)],
        ]:
            poly = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in pts]), pen)
            poly.setBrush(fill)

        text_item = scene.addText(text)
        font = QFont()
        font.setPointSize(2)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)

        if y1 < 0:
            text_item.setPos(
                (x1 + x2) / 2 - text_item.boundingRect().width() / 2,
                y1 - 12
            )
        else:
            text_item.setPos(
                (x1 + x2) / 2 - text_item.boundingRect().width() / 2,
                y1 + 5
            )

    def addVerticalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)

        ext = 10
        arr = 2
        scene.addLine(x1 - ext / 2, y1, x1 + ext / 2, y1, pen)
        scene.addLine(x2 - ext / 2, y2, x2 + ext / 2, y2, pen)

        fill = QBrush(Qt.black) if self.theme.is_light() else QBrush(QColor("#D0D0D0"))

        if y2 > y1:
            polys = [
                [(x1, y1), (x1 - arr / 2, y1 + arr), (x1 + arr / 2, y1 + arr)],
                [(x2, y2), (x2 - arr / 2, y2 - arr), (x2 + arr / 2, y2 - arr)],
            ]
        else:
            polys = [
                [(x2, y2), (x2 - arr / 2, y2 + arr), (x2 + arr / 2, y2 + arr)],
                [(x1, y1), (x1 - arr / 2, y1 - arr), (x1 + arr / 2, y1 - arr)],
            ]

        for pts in polys:
            poly = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in pts]), pen)
            poly.setBrush(fill)

        text_item = scene.addText(text)
        font = QFont()
        font.setPointSize(2)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)

        if x1 < 0:
            text_item.setPos(
                x1 - text_item.boundingRect().width(),
                (y1 + y2) / 2 - text_item.boundingRect().height() / 2
            )
        else:
            text_item.setPos(
                x1,
                (y1 + y2) / 2 - text_item.boundingRect().height() / 2
            )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "view1"):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
        if hasattr(self, "view2"):
            self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)


class SeatedAngleSectionDetails(SeatedAngleCapacityDetails):
    """
    Section capacity popup:
    - left side: section capacity values
    - right side: one representative section drawing
    """

    def initUI(self):
        self.setupWrapper("Section Capacity Details")

        sg = QApplication.primaryScreen().availableGeometry()
        w, h = 960, 620
        self.setGeometry(
            sg.x() + (sg.width() - w) // 2,
            sg.y() + (sg.height() - h) // 2,
            w, h
        )

        cl = QVBoxLayout(self.content_widget)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        sa.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll = QWidget()
        scroll.setObjectName("spacing_scroll_widget")

        main_layout = QHBoxLayout(scroll)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(18)

        # ---------------- LEFT PANEL ----------------
        lp = QWidget()
        lp.setMaximumWidth(360)
        ll = QVBoxLayout(lp)
        ll.setSpacing(8)

        note = QLabel("Note: Representative image for\nFailure Pattern")
        note.setWordWrap(True)
        note.setStyleSheet("font-size: 16px; margin-bottom: 12px;")
        ll.addWidget(note)

        title1 = QLabel("Failure Pattern due to Shear in Supported Section")
        title1.setWordWrap(True)
        title1.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin-top: 10px; margin-bottom: 6px;"
        )
        ll.addWidget(title1)

        shear_items = [
            (
                "Supported Section Shear Yielding Capacity (kN)",
                self.dict_section_failure.get(
                    "Supported Section Shear Yielding Capacity (kN)", "N/A"
                )
            ),
            (
                "Supported Section Allowable Shear Capacity (kN)",
                self.dict_section_failure.get(
                    "Supported Section Allowable Shear Capacity (kN)", "N/A"
                )
            ),
        ]

        for key, val in shear_items:
            row = QHBoxLayout()
            row.setContentsMargins(0, 2, 0, 2)

            lbl = QLabel(key)
            lbl.setWordWrap(True)
            row.addWidget(lbl, 1)

            row.addStretch()

            v = QLabel(str(val))
            v.setStyleSheet("font-size: 12px; font-weight: bold;")
            row.addWidget(v, 0)

            ll.addLayout(row)

        title2 = QLabel("Failure Pattern due to Tension in Supporting Section")
        title2.setWordWrap(True)
        title2.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin-top: 14px; margin-bottom: 6px;"
        )
        ll.addWidget(title2)

        row = QHBoxLayout()
        row.setContentsMargins(0, 2, 0, 2)

        lbl = QLabel("Supporting Section Tension Yielding Capacity (kN)")
        lbl.setWordWrap(True)
        row.addWidget(lbl, 1)

        row.addStretch()

        v = QLabel(str(self.dict_section_failure.get(
            "Supporting Section Tension Yielding Capacity (kN)", "N/A"
        )))
        v.setStyleSheet("font-size: 12px; font-weight: bold;")
        row.addWidget(v, 0)

        ll.addLayout(row)
        ll.addStretch()

        # ---------------- RIGHT PANEL ----------------
        rp = QWidget()
        rl = QVBoxLayout(rp)
        rl.setSpacing(8)

        lbl = QLabel("Failure Pattern in Section:")
        lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
        rl.addWidget(lbl)

        self.scene1 = QGraphicsScene()
        self.view1 = QGraphicsView(self.scene1)
        self.view1.setRenderHint(QPainter.Antialiasing)
        self.view1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view1.setMinimumWidth(540)
        self.view1.setMinimumHeight(500)

        if self.theme.is_light():
            self.view1.setBackgroundBrush(QBrush(Qt.white))
        else:
            self.view1.setBackgroundBrush(QBrush(QColor("#4A4A4A")))

        self.createSectionDrawing(self.scene1)
        self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
        rl.addWidget(self.view1)

        main_layout.addWidget(lp, 1)
        main_layout.addWidget(rp, 2)

        sa.setWidget(scroll)
        cl.addWidget(sa)

    def createSectionDrawing(self, scene):
     scene.clear()

     if self.theme.is_light():
        line_pen = QPen(Qt.black, 1.2)
        faint_pen = QPen(QColor("#777777"), 1.0, Qt.DashLine)
        steel_pen = QPen(QColor("#777777"), 1.0)
        dim_pen = QPen(Qt.black, 1.0)
        fill_brush = QBrush(QColor("#EAE7D6"))
     else:
        line_pen = QPen(QColor("#E0E0E0"), 1.2)
        faint_pen = QPen(QColor("#B0B0B0"), 1.0, Qt.DashLine)
        steel_pen = QPen(QColor("#C0C0C0"), 1.0)
        dim_pen = QPen(QColor("#CFCFCF"), 1.0)
        fill_brush = QBrush(QColor("#5A5A5A"))

     scene.setSceneRect(0, 0, 520, 660)
 
    # ---------------- actual geometry source ----------------
     s = self.spacing
     gauge = s["gauge"] if s["gauge"] > 0 else 70.0
     end_dist = s["end"] if s["end"] > 0 else 65.0
     pitch = s["pitch"] if s["pitch"] > 0 else 290.0
     total_height = end_dist + pitch if self.rows > 1 else end_dist + 290.0

    # drawing anchors
     left_outer_1 = 75
     left_outer_2 = 82
     right_outer_1 = 258
     right_outer_2 = 265

     top_y = 70
     bot_y = 560

     scene.addLine(left_outer_1, top_y, left_outer_1, bot_y, steel_pen)
     scene.addLine(left_outer_2, top_y, left_outer_2, bot_y, steel_pen)
     scene.addLine(right_outer_1, top_y, right_outer_1, bot_y, steel_pen)
     scene.addLine(right_outer_2, top_y, right_outer_2, bot_y, steel_pen)

    # top plate
     top_plate_x = 115
     top_plate_y = 95
     plate_w = 110
     plate_h = 60

     scene.addRect(top_plate_x, top_plate_y, plate_w, plate_h, line_pen, fill_brush)
     scene.addLine(
        top_plate_x - 5, top_plate_y + plate_h,
        top_plate_x + plate_w + 5, top_plate_y + plate_h, line_pen
     )
     scene.addLine(
        top_plate_x - 5, top_plate_y + plate_h + 5,
        top_plate_x + plate_w + 5, top_plate_y + plate_h + 5, steel_pen
     )

    # bottom plate
     bot_plate_x = 115
     bot_plate_y = 390
     scene.addRect(bot_plate_x, bot_plate_y, plate_w, plate_h, line_pen, fill_brush)
     scene.addLine(
        bot_plate_x - 5, bot_plate_y - 5,
        bot_plate_x + plate_w + 5, bot_plate_y - 5, steel_pen
     )
     scene.addLine(
        bot_plate_x - 5, bot_plate_y,
        bot_plate_x + plate_w + 5, bot_plate_y, line_pen
    )

    # bolts centered wrt plate
     plate_cx = top_plate_x + plate_w / 2
     left_bolt_x = plate_cx - gauge / 2
     right_bolt_x = plate_cx + gauge / 2

    # keep inside plate
     left_limit = top_plate_x + 12
     right_limit = top_plate_x + plate_w - 12
     if left_bolt_x < left_limit or right_bolt_x > right_limit:
        left_bolt_x = top_plate_x + 20
        right_bolt_x = top_plate_x + plate_w - 20
        gauge = right_bolt_x - left_bolt_x

     top_bolt_y = 125
     bottom_bolt_y = 420

     top_bolts = [(left_bolt_x, top_bolt_y), (right_bolt_x, top_bolt_y)]
     bottom_bolts = [(left_bolt_x, bottom_bolt_y), (right_bolt_x, bottom_bolt_y)]

     bolt_pen = QPen(Qt.blue, 2.5)
     bolt_brush = QBrush(Qt.transparent)

     for cx, cy in top_bolts + bottom_bolts:
        scene.addEllipse(cx - 8, cy - 8, 16, 16, bolt_pen, bolt_brush)

    # supported section rectangle aligned with plate edges
     web_top = top_plate_y + plate_h + 5
     web_bottom = bot_plate_y - 5

     left_solid_x = top_plate_x
     right_solid_x = top_plate_x + plate_w

     scene.addLine(left_solid_x, web_top, left_solid_x, web_bottom, steel_pen)
     scene.addLine(right_solid_x, web_top, right_solid_x, web_bottom, steel_pen)

    # inner 2 vertical lines only
     inner_gap = 5.0
     inner_left_x = plate_cx - inner_gap / 2
     inner_right_x = plate_cx + inner_gap / 2

     scene.addLine(inner_left_x, web_top, inner_left_x, web_bottom, steel_pen)
     scene.addLine(inner_right_x, web_top, inner_right_x, web_bottom, steel_pen)

    # failure / load path
     scene.addLine(top_bolts[0][0], top_bolts[0][1], bottom_bolts[0][0], bottom_bolts[0][1], faint_pen)
     scene.addLine(top_bolts[1][0], top_bolts[1][1], bottom_bolts[1][0], bottom_bolts[1][1], faint_pen)
     scene.addLine(top_bolts[0][0], top_bolts[0][1], top_bolts[1][0], top_bolts[1][1], faint_pen)
     scene.addLine(bottom_bolts[0][0], bottom_bolts[0][1], bottom_bolts[1][0], bottom_bolts[1][1], faint_pen)

    # ---------------- dimension helpers ----------------
     top_dim_y = 38
     top_dim_y_2 = 18
     top_dim_y_3 = 0

     right_dim_x = 330
     right_dim_x_2 = 365
     left_dim_x = 35
     left_dim_x_2 = 70

     def add_h_dim(x1, y1, x2, y2, text):
        scene.addLine(x1, y1, x2, y2, dim_pen)
        ext = 10
        arr = 4
        scene.addLine(x1, y1 - ext / 2, x1, y1 + ext / 2, dim_pen)
        scene.addLine(x2, y2 - ext / 2, x2, y2 + ext / 2, dim_pen)

        fill = QBrush(Qt.black) if self.theme.is_light() else QBrush(QColor("#D0D0D0"))
        for pts in [
            [(x1, y1), (x1 + arr, y1 - arr / 2), (x1 + arr, y1 + arr / 2)],
            [(x2, y2), (x2 - arr, y2 - arr / 2), (x2 - arr, y2 + arr / 2)],
        ]:
            p = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in pts]), dim_pen)
            p.setBrush(fill)

        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(7)
        f.setBold(True)
        ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        ti.setPos((x1 + x2) / 2 - ti.boundingRect().width() / 2, y1 - 18)

     def add_v_dim(x1, y1, x2, y2, text):
        scene.addLine(x1, y1, x2, y2, dim_pen)
        ext = 10
        arr = 4
        scene.addLine(x1 - ext / 2, y1, x1 + ext / 2, y1, dim_pen)
        scene.addLine(x2 - ext / 2, y2, x2 + ext / 2, y2, dim_pen)

        fill = QBrush(Qt.black) if self.theme.is_light() else QBrush(QColor("#D0D0D0"))
        if y2 > y1:
            polys = [
                [(x1, y1), (x1 - arr / 2, y1 + arr), (x1 + arr / 2, y1 + arr)],
                [(x2, y2), (x2 - arr / 2, y2 - arr), (x2 + arr / 2, y2 - arr)],
            ]
        else:
            polys = [
                [(x2, y2), (x2 - arr / 2, y2 + arr), (x2 + arr / 2, y2 + arr)],
                [(x1, y1), (x1 - arr / 2, y1 - arr), (x1 + arr / 2, y1 - arr)],
            ]

        for pts in polys:
            p = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in pts]), dim_pen)
            p.setBrush(fill)

        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(7)
        f.setBold(True)
        ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)

        if x1 < 170:
            ti.setPos(
                x1 - ti.boundingRect().width() - 6,
                (y1 + y2) / 2 - ti.boundingRect().height() / 2
            )
        else:
            ti.setPos(
                x1 + 6,
                (y1 + y2) / 2 - ti.boundingRect().height() / 2
            )

    # ---------------- added horizontal dimensions ----------------

    # left edge distance
     add_h_dim(top_plate_x, top_dim_y, left_bolt_x, top_dim_y, f"{left_bolt_x - top_plate_x:.1f}")

    # gauge between bolts
     add_h_dim(left_bolt_x, top_dim_y, right_bolt_x, top_dim_y, f"{gauge:.1f}")

    # right edge distance
     add_h_dim(right_bolt_x, top_dim_y, top_plate_x + plate_w, top_dim_y, f"{top_plate_x + plate_w - right_bolt_x:.1f}")

    # total plate width
     add_h_dim(top_plate_x, top_dim_y_2, top_plate_x + plate_w, top_dim_y_2, f"{plate_w:.1f}")

    # inner web gap
     add_h_dim(inner_left_x, top_dim_y_3, inner_right_x, top_dim_y_3, f"{inner_gap:.1f}")

    # ---------------- vertical dimensions ----------------

     top_offset = web_top - top_plate_y
     middle_height = (bot_plate_y + plate_h) - web_top
     total_height_draw = (bot_plate_y + plate_h) - top_plate_y

    # right side split dimensions
     add_v_dim(right_dim_x, top_plate_y, right_dim_x, web_top, f"{top_offset:.1f}")
     web_gap = bot_plate_y - web_top
     add_v_dim(right_dim_x, web_top, right_dim_x, bot_plate_y, f"{web_gap:.1f}")
     add_v_dim(right_dim_x, bot_plate_y, right_dim_x, bot_plate_y + plate_h, f"{plate_h:.1f}")

    # left side overall height
     add_v_dim(left_dim_x, top_plate_y, left_dim_x, bot_plate_y + plate_h, f"{total_height_draw:.1f}")

    # top plate thickness
     add_v_dim(left_dim_x_2, top_plate_y, left_dim_x_2, top_plate_y + plate_h, f"{plate_h:.1f}")

    # bottom plate thickness
     add_v_dim(left_dim_x_2, bot_plate_y, left_dim_x_2, bot_plate_y + plate_h, f"{plate_h:.1f}")

    # clear gap between plates
     clear_gap = bot_plate_y - (top_plate_y + plate_h)
     add_v_dim(right_dim_x_2, top_plate_y + plate_h, right_dim_x_2, bot_plate_y, f"{clear_gap:.1f}")
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "view1"):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)