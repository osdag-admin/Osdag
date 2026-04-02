from PySide6.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
    QGraphicsScene, QScrollArea
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import (
    QPainter, QPen, QFont, QColor,
    QPolygonF, QBrush, QPixmap
)

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *


class TensionBoltedDetails(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2, main=None):
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager
        self.connection = connection_obj

        self.detail_type = "spacing"
        self.window_title = "Bolt Pattern"

        if isinstance(main, tuple) and len(main) > 1:
            self.detail_type = main[1]

        if self.detail_type == "plate_capacity":
            data = connection_obj.plate_capacity_details(True)
            self.window_title = "Plate Capacity Details"

        elif self.detail_type == "section_capacity":
            data = connection_obj.section_capacity_details(True)
            self.window_title = "Section Capacity Details"

        else:
            data = connection_obj.spacing(True)
            self.window_title = "Bolt Pattern"

        self.member_height = getattr(connection_obj.plate, "height", 200.0)
        self.member_length = getattr(connection_obj, "length", 1000.0)

        self.section_data = None
        self.param_map = {}
        self.section_failure_case = int(self.param_map.get("SECTION_FAILURE_CASE", 2))
        self.plate_failure_case = int(self.param_map.get("PLATE_FAILURE_CASE", 2))
        for elem in data:
            if len(elem) < 4:
                continue
            if elem[2] == TYPE_SECTION:
                self.section_data = elem[3]
            elif elem[2] == TYPE_TEXTBOX:
                self.param_map[elem[1]] = elem[3]

        self.initUI()

    # ──────────────────────────────────────────────────────────────────────
    # Window shell
    # ──────────────────────────────────────────────────────────────────────

    def setupWrapper(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setObjectName("spacing_capacity_details")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle(self.window_title)
        main_layout.addWidget(self.title_bar)

        self.content_widget = QWidget(self)
        main_layout.addWidget(self.content_widget, 1)

        size_grip = QSizeGrip(self)
        size_grip.setFixedSize(16, 16)

        overlay = QHBoxLayout()
        overlay.setContentsMargins(0, 0, 4, 4)
        overlay.addStretch(1)
        overlay.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)
        main_layout.addLayout(overlay)

    def initUI(self):
        self.setupWrapper()

        screen = QApplication.primaryScreen().availableGeometry()
        width, height = 980, 760
        self.setGeometry(
            screen.x() + (screen.width() - width) // 2,
            screen.y() + (screen.height() - height) // 2,
            width,
            height
        )

        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll = QWidget()
        scroll.setObjectName("spacing_scroll_widget")

        main_layout = QHBoxLayout(scroll)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        # LEFT PANEL
        left_panel = QWidget()
        left_panel.setMaximumWidth(380)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(6)

        if self.detail_type == "spacing":
            self._build_spacing_left_panel(left_layout)
        else:
            self._build_capacity_left_panel(left_layout)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # RIGHT PANEL
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)
        right_panel.setLayout(right_layout)

        if self.detail_type == "spacing":
            self.scene = QGraphicsScene()
            self.view = QGraphicsView(self.scene)
            self._apply_view_style(self.view)
            self.createSpacingDrawing()
            self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            right_layout.addWidget(self.view)

            if self.section_data and isinstance(self.section_data, list):
                image_holder = QWidget()
                image_layout = QVBoxLayout(image_holder)
                image_layout.setAlignment(Qt.AlignTop)
                image_layout.setContentsMargins(8, 8, 8, 8)

                title = self.section_data[3] if len(self.section_data) > 3 else ""
                image_path = self.section_data[0] if len(self.section_data) > 0 else ""
                img_w = self.section_data[1] if len(self.section_data) > 1 else 400
                img_h = self.section_data[2] if len(self.section_data) > 2 else 202

                if title:
                    title_label = QLabel(title)
                    title_label.setWordWrap(True)
                    image_layout.addWidget(title_label)

                image_label = QLabel()
                image_label.setAlignment(Qt.AlignCenter)
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    image_label.setPixmap(
                        pixmap.scaled(img_w, img_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    )
                image_layout.addWidget(image_label)
                right_layout.addWidget(image_holder)

        elif self.detail_type == "plate_capacity":
            title = QLabel("Failure Pattern due to Tension in Plate:")
            title.setStyleSheet("font-size: 14px; font-weight: bold;")
            right_layout.addWidget(title)

            self.scene1 = QGraphicsScene()
            self.view1 = self._make_capacity_view(self.scene1, self.createPlateCapacityDrawing, 420)
            right_layout.addWidget(self.view1)

        elif self.detail_type == "section_capacity":
            title = QLabel("Failure Pattern in Section:")
            title.setStyleSheet("font-size: 14px; font-weight: bold;")
            right_layout.addWidget(title)

            self.scene1 = QGraphicsScene()
            self.view1 = self._make_capacity_view(self.scene1, self.createSectionCapacityDrawing, 420)
            self.view1.setStyleSheet("border: 1px solid #888;")
            right_layout.addWidget(self.view1)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        scroll_area.setWidget(scroll)
        content_layout.addWidget(scroll_area)

    # ──────────────────────────────────────────────────────────────────────
    # Left panel builders
    # ──────────────────────────────────────────────────────────────────────

    def _build_spacing_left_panel(self, left_layout):
        note = QLabel("Note: Representative image for Spacing Details")
        note.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        note.setWordWrap(True)
        left_layout.addWidget(note)

        for key, value in self.param_map.items():
            row = QHBoxLayout()
            label = QLabel(f"{key}")
            val = QLabel(f"{value}")
            val.setStyleSheet("font-size: 12px; font-weight: bold;")
            row.addWidget(label)
            row.addStretch()
            row.addWidget(val)
            left_layout.addLayout(row)

    def _build_capacity_left_panel(self, left_layout):
        note = QLabel("Note: Representative image for Failure Pattern")
        note.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        note.setWordWrap(True)
        left_layout.addWidget(note)

        title_map = {
            "plate_capacity": "Capacity Details",
            "section_capacity": "Capacity Details",
        }

        title = QLabel(title_map.get(self.detail_type, "Capacity Details"))
        title.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;"
        )
        left_layout.addWidget(title)

        for key, value in self.param_map.items():
            row = QHBoxLayout()
            row.addWidget(QLabel(str(key)))
            row.addStretch()

            val = QLabel(str(value))
            val.setStyleSheet("font-size: 12px; font-weight: bold;")
            row.addWidget(val)

            left_layout.addLayout(row)

    # ──────────────────────────────────────────────────────────────────────
    # View helpers
    # ──────────────────────────────────────────────────────────────────────

    def _apply_view_style(self, view):
        if self.theme.is_light():
            view.setBackgroundBrush(QBrush(Qt.white))
        else:
            view.setBackgroundBrush(QBrush(QColor("#4A4A4A")))
        view.setRenderHint(QPainter.Antialiasing)

    def _make_capacity_view(self, scene, draw_fn, min_h=300):
     view = QGraphicsView(scene)
     self._apply_view_style(view)
     view.setMinimumWidth(620)
     view.setMinimumHeight(min_h)
     view.setScene(scene)
     view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
     view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

     draw_fn(scene)

     if not scene.items():
        scene.setSceneRect(0, 0, 600, 400)

     view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
     return view
    # ──────────────────────────────────────────────────────────────────────
    # Spacing drawing
    # ──────────────────────────────────────────────────────────────────────

    def _spacing_params(self):
        params = {}
        for key, value in self.param_map.items():
            text_key = key.lower()
            if "end" in text_key:
                params["end"] = float(value)
            elif "pitch" in text_key:
                params["pitch"] = float(value)
            elif "edge" in text_key:
                params["edge"] = float(value)
            elif "gauge" in text_key:
                params["gauge"] = float(value)
            elif "bolt line" in text_key or "columns" in text_key:
                params["columns"] = int(float(value))
            elif "bolts one line" in text_key or "rows" in text_key:
                params["rows"] = int(float(value))

        params.setdefault("end", 40.0)
        params.setdefault("pitch", 60.0)
        params.setdefault("edge", 40.0)
        params.setdefault("gauge", 50.0)
        params.setdefault("rows", 2)
        params.setdefault("columns", 1)
        return params

    def createSpacingDrawing(self):
        params = self._spacing_params()

        end = params["end"]
        gauge = params["gauge"]
        edge = params["edge"]
        pitch = params["pitch"]
        hole_diameter = getattr(self.connection, "bolt_diameter_min", 16.0)
        self.rows = params["rows"]
        self.cols = params["columns"]

        self.member_height = 2 * end + pitch * (self.rows - 1)
        height = self.member_height
        width = edge + gauge * max(0, (self.cols - 1)) + 100
        self.length = width

        outline_pen = QPen(Qt.blue, 2)
        dimension_pen = QPen(Qt.black if self.theme.is_light() else QColor("#8A8A8A"), 1.5)

        h_offset = 40
        v_offset = 60

        self.scene.setSceneRect(-h_offset, -v_offset, width + 2 * v_offset, height + 2 * h_offset)

        mid_offset = 5

        self.scene.addLine(0, 0, width, 0, dimension_pen)
        self.scene.addLine(width, 0, width, height / 2 - mid_offset, dimension_pen)
        self.scene.addLine(width, height / 2 - mid_offset, width - mid_offset, (height - mid_offset) / 2, dimension_pen)
        self.scene.addLine(width - mid_offset, (height - mid_offset) / 2, width + mid_offset, (height + mid_offset) / 2, dimension_pen)
        self.scene.addLine(width + mid_offset, (height + mid_offset) / 2, width, height / 2 + mid_offset, dimension_pen)
        self.scene.addLine(width, height / 2 + mid_offset, width, height, dimension_pen)

        self.scene.addLine(width, height, 0, height, dimension_pen)
        self.scene.addLine(0, height, 0, 0, dimension_pen)

        for row in range(self.rows):
            for col in range(self.cols):
                x_center = edge + gauge * col
                y_center = end + pitch * row
                x = x_center - hole_diameter / 2
                y = y_center - hole_diameter / 2
                self.scene.addEllipse(x, y, hole_diameter, hole_diameter, outline_pen)

        self.addDimensions(params, dimension_pen)

    def addDimensions(self, params, pen):
        end = params["end"]
        gauge = params["gauge"]
        pitch = params["pitch"]
        edge = params["edge"]

        height = self.member_height
        width = self.length

        h_offset = 20
        v_offset = 30

        x_start = 0
        x_segments = [("edge", x_start, x_start + edge)]
        x_start += edge
        for _ in range(self.cols - 1):
            x_segments.append(("gauge", x_start, x_start + gauge))
            x_start += gauge

        y_start = 0
        y_segments = [("end", y_start, y_start + end)]
        y_start += end
        for _ in range(self.rows - 1):
            y_segments.append(("pitch", y_start, y_start + pitch))
            y_start += pitch
        y_segments.append(("remain", y_start, height))

        for _, x1, x2 in x_segments:
            value = x2 - x1
            self.addHorizontalDimension(x1, -h_offset, x2, -h_offset, f"{value:.1f}", pen)

        for _, y1, y2 in y_segments:
            value = y2 - y1
            self.addVerticalDimension(-v_offset / 2, y1, -v_offset / 2, y2, f"{value:.1f}", pen)

        self.addVerticalDimension(width + v_offset, 0, width + v_offset, height, str(height), pen)

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 5
        ext_length = 10

        self.scene.addLine(x1, y1 - ext_length / 2, x1, y1 + ext_length / 2, pen)
        self.scene.addLine(x2, y2 - ext_length / 2, x2, y2 + ext_length / 2, pen)

        points_left = [(x1, y1), (x1 + arrow_size, y1 - arrow_size / 2), (x1 + arrow_size, y1 + arrow_size / 2)]
        polygon_left = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_left]), pen)
        polygon_left.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#4A4A4A")))

        points_right = [(x2, y2), (x2 - arrow_size, y2 - arrow_size / 2), (x2 - arrow_size, y2 + arrow_size / 2)]
        polygon_right = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_right]), pen)
        polygon_right.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#4A4A4A")))

        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)

        if y1 < 0:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 25)
        else:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 + 5)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 5
        ext_length = 10

        self.scene.addLine(x1 - ext_length / 2, y1, x1 + ext_length / 2, y1, pen)
        self.scene.addLine(x2 - ext_length / 2, y2, x2 + ext_length / 2, y2, pen)

        if y2 > y1:
            points_top = [(x1, y1), (x1 - arrow_size / 2, y1 + arrow_size), (x1 + arrow_size / 2, y1 + arrow_size)]
            polygon_top = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
            polygon_top.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#4A4A4A")))

            points_bottom = [(x2, y2), (x2 - arrow_size / 2, y2 - arrow_size), (x2 + arrow_size / 2, y2 - arrow_size)]
            polygon_bottom = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            polygon_bottom.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#4A4A4A")))
        else:
            points_top = [(x2, y2), (x2 - arrow_size / 2, y2 + arrow_size), (x2 + arrow_size / 2, y2 + arrow_size)]
            polygon_top = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
            polygon_top.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#4A4A4A")))

            points_bottom = [(x1, y1), (x1 - arrow_size / 2, y1 - arrow_size), (x1 + arrow_size / 2, y1 - arrow_size)]
            polygon_bottom = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            polygon_bottom.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#4A4A4A")))

        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)

        if x1 < 0:
            text_item.setPos(x1 - 10 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1 + 15, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)

    # ──────────────────────────────────────────────────────────────────────
    # Capacity drawing logic
    # ──────────────────────────────────────────────────────────────────────

    def _tc(self):
        return Qt.black if self.theme.is_light() else Qt.white

    def _fill_brush(self):
        return QBrush(Qt.black if self.theme.is_light() else QColor("#8A8A8A"))

    def _capacity_geom(self):
        spacing = self.connection.spacing(True)

        dd = {}
        for item in spacing:
            if len(item) < 4:
                continue
            if item[2] == TYPE_TEXTBOX:
                dd[item[0]] = item[3]
                dd[item[1]] = item[3]

        pitch = float(dd.get(KEY_OUT_PITCH, dd.get("Pitch (mm)", 60.0)))
        end = float(dd.get(KEY_OUT_END_DIST, dd.get("End Distance (mm)", 40.0)))
        gauge = float(dd.get(KEY_OUT_GAUGE, dd.get("Gauge (mm)", 0.0)))
        edge = float(dd.get(KEY_OUT_EDGE_DIST, dd.get("Edge Distance (mm)", 40.0)))

        rows = max(2, int(float(dd.get(KEY_OUT_BOLTS_ONE_LINE, dd.get("Bolts in One Line", 2)))))
        cols = max(1, int(float(dd.get(KEY_OUT_BOLT_LINE, dd.get("Bolt Line", 1)))))

        hole = float(getattr(self.connection, "bolt_diameter_min", 16.0))

        return {
            "pitch": pitch,
            "end": end,
            "gauge": gauge,
            "edge": edge,
            "rows": rows,
            "cols": cols,
            "hole": hole,
        }

    def _draw_common(self, scene, mode):
        g = self._capacity_geom()

        coeff = 2.0
        pitch = g["pitch"] / coeff
        end = g["end"] / coeff
        edge = g["edge"] / coeff
        gauge = max(g["gauge"] / coeff, 40 / coeff)
        hole = g["hole"] / coeff
        rows = g["rows"]
        cols = g["cols"]

        plate_h = 2 * end + pitch * (rows - 1)
        plate_w = 2 * edge + gauge * max(0, cols - 1)

        plate_h = max(plate_h, 120 / coeff)
        plate_w = max(plate_w, 120 / coeff)

        beam_w = plate_w * 0.18
        beam_h = plate_h * 2.1
        beam_x = plate_w * 0.41
        beam_y = plate_h * 0.1

        plate_x = beam_x + beam_w
        plate_y = beam_y + (beam_h - plate_h) / 2

        scene.setSceneRect(-80, -50, plate_w + beam_w + 220, beam_h + 120)

        struct_pen = QPen(QColor("#555555"), 1.5)
        plate_pen = QPen(QColor("#444444"), 1.2)
        dim_pen = QPen(Qt.black if self.theme.is_light() else QColor("#E0E0E0"), 1.0)
        dash_pen = QPen(Qt.black if self.theme.is_light() else QColor("#AFAFAF"), 1.0, Qt.DashLine)

        beam_brush = QBrush(QColor("#A0A0A0"))
        plate_brush = QBrush(QColor("#FFFFFF"))
        bolt_pen = QPen(QColor("#1E2BFF"), 2.0)
        bolt_brush = QBrush(Qt.white)

        flange_w = plate_w * 1.6
        flange_h = plate_h * 0.10
        web_w = plate_w * 0.14
        web_x = beam_x + (flange_w - web_w) / 2
        top_flange_y = beam_y
        bottom_flange_y = beam_y + beam_h - flange_h

        scene.addRect(beam_x - plate_w * 0.25, top_flange_y, flange_w, flange_h, struct_pen).setBrush(beam_brush)
        scene.addRect(web_x, beam_y + flange_h, web_w, beam_h - 2 * flange_h, struct_pen).setBrush(beam_brush)
        scene.addRect(beam_x - plate_w * 0.25, bottom_flange_y, flange_w, flange_h, struct_pen).setBrush(beam_brush)

        scene.addRect(plate_x, plate_y, plate_w, plate_h, plate_pen).setBrush(plate_brush)

        x_positions = [plate_x + edge + gauge * c for c in range(cols)]
        y_positions = [plate_y + end + pitch * r for r in range(rows)]

        for cx in x_positions:
            for cy in y_positions:
                r = hole / 2
                ellipse = scene.addEllipse(cx - r, cy - r, 2 * r, 2 * r, bolt_pen)
                ellipse.setBrush(bolt_brush)

        if mode == "plate":
            x_fail = x_positions[-1] if x_positions else plate_x + plate_w / 2
            y_top = y_positions[0] if y_positions else plate_y + plate_h * 0.25
            y_bot = y_positions[-1] if y_positions else plate_y + plate_h * 0.75

            scene.addLine(x_fail, y_top, x_fail, y_bot, dash_pen)
            scene.addLine(x_fail, y_top, plate_x + plate_w, y_top, dash_pen)
            scene.addLine(x_fail, y_bot, plate_x + plate_w, y_bot, dash_pen)

        elif mode == "section":
            if x_positions and y_positions:
                cx = x_positions[0]
                y_top = y_positions[0]
                y_bot = y_positions[-1]
                scene.addLine(cx, y_top, cx, y_bot, dash_pen)

                beam_face = plate_x
                scene.addLine(beam_face, y_top, cx, y_top, dash_pen)
                scene.addLine(beam_face, y_bot, cx, y_bot, dash_pen)

        top_dim_y = plate_y - 35
        bottom_dim_y = plate_y + plate_h + 28
        left_dim_x = plate_x - 35
        right_dim_x = plate_x + plate_w + 35

        if cols > 1:
            current_x = plate_x
            self._add_horizontal_dimension(scene, current_x, bottom_dim_y, current_x + edge, f"{g['edge']:.1f}", dim_pen)
            current_x += edge
            for _ in range(cols - 1):
                self._add_horizontal_dimension(scene, current_x, bottom_dim_y, current_x + gauge, f"{g['gauge']:.1f}", dim_pen)
                current_x += gauge
            self._add_horizontal_dimension(scene, current_x, bottom_dim_y, plate_x + plate_w, f"{g['edge']:.1f}", dim_pen)
        else:
            if x_positions:
                self._add_horizontal_dimension(scene, plate_x, bottom_dim_y, x_positions[0], f"{g['edge']:.1f}", dim_pen)
                self._add_horizontal_dimension(scene, x_positions[0], bottom_dim_y, plate_x + plate_w, f"{g['edge']:.1f}", dim_pen)

        if rows > 1 and y_positions:
            self._add_vertical_dimension(scene, right_dim_x, plate_y, y_positions[0], f"{g['end']:.1f}", dim_pen)
            for i in range(len(y_positions) - 1):
                self._add_vertical_dimension(scene, right_dim_x, y_positions[i], y_positions[i + 1], f"{g['pitch']:.1f}", dim_pen)
            self._add_vertical_dimension(scene, right_dim_x, y_positions[-1], plate_y + plate_h, f"{g['end']:.1f}", dim_pen)
        else:
            self._add_vertical_dimension(scene, right_dim_x, plate_y, plate_y + plate_h, f"{g['end'] * 2:.1f}", dim_pen)

        self._add_vertical_dimension(scene, left_dim_x, plate_y, plate_y + plate_h, f"{plate_h * coeff:.1f}", dim_pen, right_side=False)
        self._add_horizontal_dimension(scene, plate_x, top_dim_y, plate_x + plate_w, f"{plate_w * coeff:.1f}", dim_pen, above=True)

    def _add_horizontal_dimension(self, scene, x1, y, x2, text, pen, above=False):
        arrow = 4
        fill = self._fill_brush()

        scene.addLine(x1, y, x2, y, pen)
        scene.addLine(x1, y - 5, x1, y + 5, pen)
        scene.addLine(x2, y - 5, x2, y + 5, pen)

        p1 = [(x1, y), (x1 + arrow, y - arrow / 2), (x1 + arrow, y + arrow / 2)]
        p2 = [(x2, y), (x2 - arrow, y - arrow / 2), (x2 - arrow, y + arrow / 2)]

        scene.addPolygon(QPolygonF([QPointF(px, py) for px, py in p1]), pen).setBrush(fill)
        scene.addPolygon(QPolygonF([QPointF(px, py) for px, py in p2]), pen).setBrush(fill)

        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(5)
        ti.setFont(f)
        ti.setDefaultTextColor(self._tc())

        y_off = -18 if above else 3
        ti.setPos((x1 + x2) / 2 - ti.boundingRect().width() / 2, y + y_off)

    def _add_vertical_dimension(self, scene, x, y1, y2, text, pen, right_side=True):
        arrow = 4
        fill = self._fill_brush()

        scene.addLine(x, y1, x, y2, pen)
        scene.addLine(x - 5, y1, x + 5, y1, pen)
        scene.addLine(x - 5, y2, x + 5, y2, pen)

        p1 = [(x, y1), (x - arrow / 2, y1 + arrow), (x + arrow / 2, y1 + arrow)]
        p2 = [(x, y2), (x - arrow / 2, y2 - arrow), (x + arrow / 2, y2 - arrow)]

        scene.addPolygon(QPolygonF([QPointF(px, py) for px, py in p1]), pen).setBrush(fill)
        scene.addPolygon(QPolygonF([QPointF(px, py) for px, py in p2]), pen).setBrush(fill)

        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(5)
        ti.setFont(f)
        ti.setDefaultTextColor(self._tc())

        mid_y = (y1 + y2) / 2 - ti.boundingRect().height() / 2
        if right_side:
            ti.setPos(x + 8, mid_y)
        else:
            ti.setPos(x - ti.boundingRect().width() - 8, mid_y)

    def createPlateCapacityDrawing(self, scene):
        self._draw_common(scene, "plate")

    def createSectionCapacityDrawing(self, scene):
        scene.clear()
        self._draw_common(scene, "section")

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, "view"):
            self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        if hasattr(self, "view1"):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)