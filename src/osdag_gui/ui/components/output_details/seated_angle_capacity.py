
from PySide6.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
    QGraphicsScene, QScrollArea
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import (
    QPainter, QPen, QFont, QColor, QPolygonF, QBrush
)

from ..dialogs.custom_titlebar import CustomTitleBar
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
    def _sc(self, coeff=1):
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
        self._draw_seated_elevation(scene, for_moment=False)

    def createMomentDrawing(self, scene):
        self._draw_seated_elevation(scene, for_moment=True)

    def _draw_seated_elevation(self, scene, for_moment):
        coeff = 1
        s = self._sc(coeff)
        
        if self.theme.is_light():
            col_brush = QBrush(QColor("#f4f4e3"))
            beam_brush = QBrush(Qt.white)
            angle_brush = QBrush(QColor("#dbdbce"))
            bolt_brush = QBrush(QColor("#ff4e4e"))
            bolt_pen = QPen(Qt.transparent, 0)
            shape_pen = QPen(Qt.black, 1)
            dash = QPen(QColor("#000000"), 2, Qt.DashLine)
            dim_pen = QPen(Qt.black, 1)
        else:
            col_brush = QBrush(QColor("#a8a89b"))
            beam_brush = QBrush(Qt.white)
            angle_brush = QBrush(QColor("#8b8b7e"))
            bolt_brush = QBrush(QColor("#ff4e4e"))
            bolt_pen = QPen(Qt.transparent, 0)
            shape_pen = QPen(Qt.black, 1)
            dash = QPen(Qt.black, 2, Qt.DashLine)
            dim_pen = QPen(QColor("#CFCFCF"), 1)

        scene.clear()

        # Dynamic Attributes
        top_w = self._safe_float(getattr(self.main.top_angle, "width", self.plate_width)) / coeff
        bot_w = self._safe_float(getattr(self.main.seated_angle, "width", self.plate_width)) / coeff
        beam_bf = self._safe_float(getattr(self.main.supported_section, "flange_width", 0.0)) / coeff
        if beam_bf == 0.0:
            beam_bf = top_w

        # Geometry scaling for visualization to match DXF schematic ratios
        h_draw = self.plate_height * 0.4 / coeff # roughly equivalent to old w * 0.25 but decoupled from width
        if h_draw == 0:
            h_draw = bot_w * 0.25
            
        beam_d = max(top_w, bot_w) * 0.8
        beam_tf = h_draw * 0.15
        beam_tw = max(2, beam_bf * 0.02)
        top_angle_h = h_draw
        angle_t = h_draw * 0.15
        
        # 1. Column Flange Background (Wavy lines conceptually -> just a wide rectangle here)
        col_w = max(top_w, bot_w, beam_bf) * 1.5
        scene.addRect(-col_w/2, -beam_d - top_angle_h - 60, col_w, beam_d + top_angle_h + h_draw + 120, shape_pen, col_brush)

        # 2. Top Angle
        top_angle_y = -beam_d - top_angle_h
        scene.addRect(-top_w/2, top_angle_y, top_w, top_angle_h - angle_t, shape_pen, angle_brush)
        scene.addRect(-top_w/2, top_angle_y + top_angle_h - angle_t, top_w, angle_t, shape_pen, angle_brush)
        top_bolt_y = top_angle_y + (top_angle_h - angle_t)/2
        
        top_gauge_val = self._safe_float(getattr(self.main.bolt, "top_angle_gauge_column", s["gauge"])) / coeff
        top_bolt_x_coords = [-top_gauge_val / 2, top_gauge_val / 2]

        # 3. I-Beam (Cross Section)
        scene.addRect(-beam_bf/2, -beam_d, beam_bf, beam_tf, shape_pen, beam_brush)
        scene.addRect(-beam_tw/2, -beam_d + beam_tf, beam_tw, beam_d - 2*beam_tf, shape_pen, beam_brush)
        scene.addRect(-beam_bf/2, -beam_tf, beam_bf, beam_tf, shape_pen, beam_brush)

        # 4. Seated Angle (Bottom Angle)
        scene.addRect(-bot_w/2, angle_t, bot_w, h_draw - angle_t, shape_pen, angle_brush)
        scene.addRect(-bot_w/2, 0, bot_w, angle_t, shape_pen, angle_brush)
        
        bottom_cols = int(getattr(self.main.bolt, "seated_angle_bolt_col", self.cols))
        bottom_gauge_val = self._safe_float(getattr(self.main.bolt, "seated_angle_gauge_column", s["gauge"])) / coeff
        
        bottom_bolt_x_coords = []
        if bottom_cols <= 1:
            bottom_bolt_x_coords = [0]
        else:
            start_x = - (bottom_cols - 1) * bottom_gauge_val / 2
            for i in range(bottom_cols):
                bottom_bolt_x_coords.append(start_x + i * bottom_gauge_val)

        bolt_y_draw = h_draw * 0.6  # slightly below middle
        if s["height"] > 0:
            bolt_y_draw = h_draw * (s["end"] / s["height"]) # Keep proportional if known

        left_bolt_x = bottom_bolt_x_coords[0]
        right_bolt_x = bottom_bolt_x_coords[-1]

        # 5. Failure Pattern
        if not for_moment:
            # Shear (L-shaped block tearing from left edge to right bolt)
            scene.addLine(-bot_w/2, bolt_y_draw, right_bolt_x, bolt_y_draw, dash)
            scene.addLine(right_bolt_x, bolt_y_draw, right_bolt_x, h_draw, dash)
        else:
            # Moment (U-shaped block tearing out middle)
            scene.addLine(left_bolt_x, h_draw, left_bolt_x, bolt_y_draw, dash)
            scene.addLine(left_bolt_x, bolt_y_draw, right_bolt_x, bolt_y_draw, dash)
            scene.addLine(right_bolt_x, bolt_y_draw, right_bolt_x, h_draw, dash)

        # 6. Draw Bolts (Drawn last to stay visible above failure pattern lines)
        hole_draw = max(8, bot_w * 0.04)
        # Top bolts
        for bx in top_bolt_x_coords:
            scene.addEllipse(bx - hole_draw/2, top_bolt_y - hole_draw/2, hole_draw, hole_draw, bolt_pen, bolt_brush)
        # Bottom bolts
        for bx in bottom_bolt_x_coords:
            scene.addEllipse(bx - hole_draw/2, bolt_y_draw - hole_draw/2, hole_draw, hole_draw, bolt_pen, bolt_brush)

        # 7. Dimensions
        self._addPlateDimensions(scene, bot_w, s["height"], s, dim_pen, coeff, top_y=0, left_x=-bot_w/2, h_draw=h_draw, bolt_y_draw=bolt_y_draw, bottom_bolt_x_coords=bottom_bolt_x_coords, bottom_gauge_val=bottom_gauge_val)

        # Adjust bounding rect to add margins so it doesn't clip
        rect = scene.itemsBoundingRect()
        scene.setSceneRect(rect.adjusted(-40, -40, 40, 40))

    def _addPlateDimensions(self, scene, width, height, s, pen, coeff, top_y, left_x, h_draw, bolt_y_draw, bottom_bolt_x_coords, bottom_gauge_val):
        ho = 70 / coeff
        vo = 50 / coeff

        y_bot = top_y + h_draw
        
        def fmt(val):
            return str(int(val))

        # Bottom horizontal dimensions
        if len(bottom_bolt_x_coords) > 0:
            actual_edge = (width - (len(bottom_bolt_x_coords)-1) * bottom_gauge_val) / 2
            
            # Left edge
            self.addHorizontalDimension(scene, left_x, y_bot + ho, bottom_bolt_x_coords[0], y_bot + ho, fmt(actual_edge), pen, above=False)
            
            # Gauges
            for i in range(len(bottom_bolt_x_coords)-1):
                self.addHorizontalDimension(scene, bottom_bolt_x_coords[i], y_bot + ho, bottom_bolt_x_coords[i+1], y_bot + ho, fmt(bottom_gauge_val), pen, above=False)
                
            # Right edge
            self.addHorizontalDimension(scene, bottom_bolt_x_coords[-1], y_bot + ho, left_x + width, y_bot + ho, fmt(actual_edge), pen, above=False)

        # Bottom total width
        self.addHorizontalDimension(scene, left_x, y_bot + ho + 40, left_x + width, y_bot + ho + 40, fmt(width), pen, above=False)

        # Vertical dimensions
        right_dim_x = left_x + width + vo
        self.addVerticalDimension(scene, right_dim_x, top_y, right_dim_x, bolt_y_draw, fmt(s.get('end', height/2)), pen)
        self.addVerticalDimension(scene, right_dim_x, bolt_y_draw, right_dim_x, top_y + h_draw, fmt(max(0.0, height - s.get('end', height/2))), pen)

        # Left total vertical dimension
        left_dim_x = left_x - vo
        self.addVerticalDimension(scene, left_dim_x, top_y, left_dim_x, top_y + h_draw, fmt(height), pen)

    # ------------------------------------------------------------------
    # shared dimension methods
    # ------------------------------------------------------------------
    def addHorizontalDimension(self, scene, x1, y1, x2, y2, text, pen, above=True):
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
        font.setPointSize(10)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)

        tw = text_item.boundingRect().width()
        if above:
            text_item.setPos((x1 + x2) / 2 - tw / 2, y1 - 12)
        else:
            text_item.setPos((x1 + x2) / 2 - tw / 2, y1 + 2)

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
        font.setPointSize(10)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        
        tw = text_item.boundingRect().width()
        th = text_item.boundingRect().height()

        if x1 < 0:
            text_item.setPos(
                x1 - tw - 2,
                (y1 + y2) / 2 - th / 2
            )
        else:
            text_item.setPos(
                x1 + 5,
                (y1 + y2) / 2 - th / 2
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
        fail_pen = QPen(Qt.black, 2.0, Qt.DashLine)
        steel_pen = QPen(QColor("#777777"), 1.0)
        dim_pen = QPen(Qt.black, 1.0)
        
        # Premium Colors
        plate_brush = QBrush(QColor("#dbdbce"))
        beam_brush = QBrush(QColor("#f4f4e3"))
        ibeam_brush = QBrush(Qt.white)
        bolt_brush = QBrush(QColor("#ff4e4e"))
        bolt_pen = QPen(Qt.transparent, 0)
     else:
        line_pen = QPen(QColor("#E0E0E0"), 1.2)
        faint_pen = QPen(QColor("#B0B0B0"), 1.0, Qt.DashLine)
        fail_pen = QPen(Qt.black, 2.0, Qt.DashLine)
        steel_pen = QPen(QColor("#C0C0C0"), 1.0)
        dim_pen = QPen(QColor("#CFCFCF"), 1.0)
        
        # Premium Colors Dark Mode 
        plate_brush = QBrush(QColor("#8b8b7e"))
        beam_brush = QBrush(QColor("#a8a89b"))
        ibeam_brush = QBrush(Qt.white)
        bolt_brush = QBrush(QColor("#ff6b6b"))
        bolt_pen = QPen(Qt.transparent, 0)

     scene.setSceneRect(0, 0, 520, 660)
 
    # ---------------- actual geometry source ----------------
     s = self.spacing
     gauge = s.get("gauge", 0) if s.get("gauge", 0) > 0 else 70.0
     end_dist = s.get("end", 0) if s.get("end", 0) > 0 else 65.0
     pitch = s.get("pitch", 0) if s.get("pitch", 0) > 0 else 290.0

    # ---------------- apply scaling to prevent overlap ----------------
     scale_x = 1.3
     scale_y = 1.3
     
     scene.setSceneRect(0, -90 * scale_y, 520 * scale_x, 750 * scale_y)

    # plate widths
     top_plate_width = self._safe_float(getattr(self.main.top_angle, "width", self.plate_width))
     bot_plate_width = self._safe_float(getattr(self.main.seated_angle, "width", self.plate_width))
     
     top_plate_w = top_plate_width * scale_x
     bot_plate_w = bot_plate_width * scale_x
     
     # Center X of the connection
     cx = 115 * scale_x + max(top_plate_w, bot_plate_w) / 2

     top_plate_x = cx - top_plate_w / 2
     bot_plate_x = cx - bot_plate_w / 2

    # drawing anchors (gap 60 units from plates, flange 10 units)
     left_outer_2 = cx - max(top_plate_w, bot_plate_w) / 2 - 60 * scale_x
     left_outer_1 = left_outer_2 - 10 * scale_x
     right_outer_1 = cx + max(top_plate_w, bot_plate_w) / 2 + 60 * scale_x
     right_outer_2 = right_outer_1 + 10 * scale_x

     top_plate_y = 85 * scale_y
     plate_h = 60 * scale_y
     bot_plate_y = 380 * scale_y
     
     top_y = -30 * scale_y
     top_margin = top_plate_y - top_y
     bot_y = bot_plate_y + plate_h + top_margin

     # Fill entire column with beam_brush (which is #f4f4e3)
     scene.addRect(left_outer_1, top_y, right_outer_2 - left_outer_1, bot_y - top_y, line_pen, beam_brush)
     
     # Draw the two inner flange lines of the column
     scene.addLine(left_outer_2, top_y, left_outer_2, bot_y, line_pen)
     scene.addLine(right_outer_1, top_y, right_outer_1, bot_y, line_pen)

     scene.addRect(top_plate_x, top_plate_y, top_plate_w, plate_h, line_pen, plate_brush)
     scene.addLine(
        top_plate_x - 5, top_plate_y + plate_h,
        top_plate_x + top_plate_w + 5, top_plate_y + plate_h, line_pen
     )

    # bottom plate
     scene.addRect(bot_plate_x, bot_plate_y, bot_plate_w, plate_h, line_pen, plate_brush)
     scene.addLine(
        bot_plate_x - 5, bot_plate_y,
        bot_plate_x + bot_plate_w + 5, bot_plate_y, line_pen
    )

    # bolts dynamic spacing
     plate_cx = cx
     
     s = self.spacing
     gauge_val = s.get("gauge", 0) if s.get("gauge", 0) > 0 else 100.0
     edge_val = s.get("edge", 0) if s.get("edge", 0) > 0 else 5.0
     
     # Top angle in seated connections explicitly has only 2 bolts on column face
     top_cols = 2
     bottom_cols = int(getattr(self.main.bolt, "seated_angle_bolt_col", self.cols))
     top_gauge_val = self._safe_float(getattr(self.main.bolt, "top_angle_gauge_column", gauge_val))
     bottom_gauge_val = self._safe_float(getattr(self.main.bolt, "seated_angle_gauge_column", gauge_val))
     
     top_gauge_draw = top_gauge_val * scale_x
     bottom_gauge_draw = bottom_gauge_val * scale_x
     
     top_bolt_x_coords = []
     if top_cols <= 1:
         top_bolt_x_coords = [plate_cx]
     else:
         start_x = plate_cx - (top_cols - 1) * top_gauge_draw / 2
         for i in range(top_cols):
             top_bolt_x_coords.append(start_x + i * top_gauge_draw)

     bottom_bolt_x_coords = []
     if bottom_cols <= 1:
         bottom_bolt_x_coords = [plate_cx]
     else:
         start_x = plate_cx - (bottom_cols - 1) * bottom_gauge_draw / 2
         for i in range(bottom_cols):
             bottom_bolt_x_coords.append(start_x + i * bottom_gauge_draw)

     top_bolt_y = top_plate_y + plate_h / 2
     bottom_bolt_y = bot_plate_y + plate_h / 2

     top_bolts = [(bx, top_bolt_y) for bx in top_bolt_x_coords]
     bottom_bolts = [(bx, bottom_bolt_y) for bx in bottom_bolt_x_coords]

    # supported section I-shape aligned perfectly with plate edges
     web_top = top_plate_y + plate_h
     web_bottom = bot_plate_y

     # Beam flange width logic
     beam_flange_w = self._safe_float(getattr(self.main.supported_section, "flange_width", 0.0)) * scale_x
     if beam_flange_w == 0.0:
         # Fallback to top plate width which generally matches the beam flange closer than the seated angle
         beam_flange_w = top_plate_w

     left_solid_x = cx - beam_flange_w / 2
     right_solid_x = cx + beam_flange_w / 2

     # Top flange lines (open ends)
     flange_t = 5 * scale_y
     scene.addLine(left_solid_x, web_top, right_solid_x, web_top, line_pen)
     scene.addLine(left_solid_x, web_top + flange_t, right_solid_x, web_top + flange_t, line_pen)
     
     # Bottom flange lines (open ends)
     scene.addLine(left_solid_x, web_bottom - flange_t, right_solid_x, web_bottom - flange_t, line_pen)
     scene.addLine(left_solid_x, web_bottom, right_solid_x, web_bottom, line_pen)

    # Two solid vertical lines representing the cleat angle legs at the edges
     scene.addLine(left_solid_x, web_top + flange_t, left_solid_x, web_bottom - flange_t, line_pen)
     scene.addLine(right_solid_x, web_top + flange_t, right_solid_x, web_bottom - flange_t, line_pen)

    # Web (THIN vertical rectangle in the center)
     inner_gap = 5.0 * scale_x
     inner_left_x = plate_cx - inner_gap / 2
     inner_right_x = plate_cx + inner_gap / 2
     
     scene.addRect(inner_left_x, web_top + flange_t, inner_gap, web_bottom - web_top - 2*flange_t, line_pen, ibeam_brush)

    # failure / load path (DRAWN BEFORE BOLTS)
     if len(top_bolts) > 0 and len(bottom_bolts) > 0:
         scene.addLine(top_bolts[0][0], top_bolts[0][1], bottom_bolts[0][0], bottom_bolts[0][1], fail_pen)
         scene.addLine(top_bolts[-1][0], top_bolts[-1][1], bottom_bolts[-1][0], bottom_bolts[-1][1], fail_pen)
         scene.addLine(top_bolts[0][0], top_bolts[0][1], top_bolts[-1][0], top_bolts[-1][1], fail_pen)
         scene.addLine(bottom_bolts[0][0], bottom_bolts[0][1], bottom_bolts[-1][0], bottom_bolts[-1][1], fail_pen)

     # DRAW BOLTS
     bolt_r = 20  # Increased radius for bigger bolts
     for cx, cy in top_bolts + bottom_bolts:
        scene.addEllipse(cx - bolt_r/2, cy - bolt_r/2, bolt_r, bolt_r, bolt_pen, bolt_brush)

    # ---------------- dimension helpers ----------------
     top_dim_y = top_plate_y - 15 * scale_y
     top_dim_y_2 = top_plate_y - 40 * scale_y
     top_dim_y_3 = top_plate_y - 65 * scale_y

     right_dim_x = right_outer_2 + 25 * scale_x
     right_dim_x_2 = right_dim_x + 35 * scale_x
     left_dim_x = left_outer_1 - 25 * scale_x
     left_dim_x_2 = left_dim_x - 35 * scale_x

     def add_h_dim(x1, y1, x2, y2, text):
        scene.addLine(x1, y1, x2, y2, dim_pen)
        ext = 10 * scale_y
        arr = 4 * scale_x
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
        f.setPointSize(int(9 * scale_y))
        f.setBold(True)
        ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        ti.setPos((x1 + x2) / 2 - ti.boundingRect().width() / 2, y1 - 18 * scale_y)

     def add_v_dim(x1, y1, x2, y2, text):
        scene.addLine(x1, y1, x2, y2, dim_pen)
        ext = 10 * scale_x
        arr = 4 * scale_y
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
        f.setPointSize(int(9 * scale_y))
        f.setBold(True)
        ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)

        if x1 < 170 * scale_x:
            ti.setPos(
                x1 - ti.boundingRect().width() - 6 * scale_x,
                (y1 + y2) / 2 - ti.boundingRect().height() / 2
            )
        else:
            ti.setPos(
                x1 + 6 * scale_x,
                (y1 + y2) / 2 - ti.boundingRect().height() / 2
            )

    # ---------------- added horizontal dimensions ----------------
     
     def fmt(val):
         val = float(val)
         return str(int(val)) if val.is_integer() else f"{val:.1f}"

    # left edge distance
     if len(top_bolt_x_coords) > 0:
         actual_top_edge_val = (top_plate_w / scale_x - (top_cols - 1) * top_gauge_val) / 2
         add_h_dim(top_plate_x, top_dim_y, top_bolt_x_coords[0], top_dim_y, fmt(actual_top_edge_val))

         # gauge between bolts
         for i in range(len(top_bolt_x_coords) - 1):
             add_h_dim(top_bolt_x_coords[i], top_dim_y, top_bolt_x_coords[i+1], top_dim_y, fmt(top_gauge_val))

         # right edge distance
         add_h_dim(top_bolt_x_coords[-1], top_dim_y, top_plate_x + top_plate_w, top_dim_y, fmt(actual_top_edge_val))

     # total plate width
     add_h_dim(top_plate_x, top_dim_y_2, top_plate_x + top_plate_w, top_dim_y_2, fmt(top_plate_w/scale_x))

    # inner web gap
     add_h_dim(inner_left_x, top_dim_y_3, inner_right_x, top_dim_y_3, fmt(inner_gap/scale_x))

    # ---------------- vertical dimensions ----------------

     top_offset = web_top - top_plate_y
     middle_height = (bot_plate_y + plate_h) - web_top
     total_height_draw = (bot_plate_y + plate_h) - top_plate_y

    # right side split dimensions
     add_v_dim(right_dim_x, top_plate_y, right_dim_x, web_top, fmt(top_offset/scale_y))
     web_gap = bot_plate_y - web_top
     add_v_dim(right_dim_x, web_top, right_dim_x, bot_plate_y, fmt(web_gap/scale_y))
     add_v_dim(right_dim_x, bot_plate_y, right_dim_x, bot_plate_y + plate_h, fmt(plate_h/scale_y))

    # left side overall height
     add_v_dim(left_dim_x, top_plate_y, left_dim_x, bot_plate_y + plate_h, fmt(total_height_draw/scale_y))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "view1"):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)