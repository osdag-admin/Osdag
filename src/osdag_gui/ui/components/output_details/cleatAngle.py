from PySide6.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
                             QGraphicsScene, QScrollArea)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtGui import QPolygonF, QBrush
from PySide6.QtCore import QPointF
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *


class CleatAngleDetails(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager
        (main, self.flag) = main
        spacing_data = connection_obj.spacing(status=True)
        output = connection_obj.output_values(True)
        data1 = {f"{i[1]} + {i[0]}": i[3] for i in output}

        self.angle_thickness = float(data1['Cleat Angle Designation + Cleat.Angle'].split(" ")[-1])

        params = {
            'width': int(data1['Height (mm) + Plate.Height']),
            'hole': int(data1['Diameter (mm) + Bolt.Diameter']),
        }
        if self.flag == 0:
            params['length'] = int(data1['Cleat Angle Designation + Cleat.Angle'][0:2])
            params['rows'] = int(data1['Bolt Rows (no) + Bolt.OneLine'])
            params['cols'] = int(data1['Bolt Columns (no) + Bolt.Line'])
        else:
            params['length'] = int(data1['Cleat Angle Designation + Cleat.Angle'][5:7])
            params['rows'] = int(data1['Bolt Rows (no) + Cleat.Spting_leg.OneLine'])
            params['cols'] = int(data1['Bolt Columns (no) + Cleat.Spting_leg.Line'])

        for item in spacing_data:
            if not isinstance(item[0], str):
                continue
            key = item[0].lower()
            value = item[3]
            if 'pitch' in key:
                params['pitch'] = value
            elif 'gauge1' in key:
                params['gauge1'] = value
            elif 'gauge2' in key:
                params['gauge2'] = value
            elif 'end' in key:
                params['end'] = value
            elif 'edge' in key:
                params['edge'] = value

        self.params = params
        self.initUI()

    def setupWrapper(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setObjectName("spacing_capacity_details")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)
        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle("Bolt Pattern")
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
        # Center the window
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = 900, 500
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

        # Main layout
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

        # Left panel for parameters
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        params = self.params
        for key, value in params.items():
            if key in ('cols', 'rows', 'hole', 'length', 'width'):
                continue
            param_layout = QHBoxLayout()
            param_label = QLabel(f"{key.title()} Distance (mm):")
            param_label.setStyleSheet("font-size: 12px; font-weight: bold;")
            value_label = QLabel(f'{float(value):.2f}')
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            left_layout.addLayout(param_layout)
        # Add note about dimensions
        note_layout = QHBoxLayout()
        note_label = QLabel("(All Dimensions are in mm)")
        note_label.setStyleSheet("font-size: 12px; font-style: italic;")
        note_layout.addWidget(note_label)
        left_layout.addLayout(note_layout)
        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # Right panel for drawing
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        if self.theme.is_light():
            self.view.setBackgroundBrush(QBrush(Qt.white))
        else:
            self.view.setBackgroundBrush(QBrush(QColor("#4A4A4A")))
        self.view.setRenderHint(QPainter.Antialiasing)
        self.createDrawing(params)

        # Assemble panels
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.view, 3)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        scroll_area.setWidget(scroll)
        content_layout.addWidget(scroll_area)

    def createDrawing(self, params):
        pitch = params['pitch']
        end = params['end']
        if 'gauge' in params:
            gauge = params['gauge']
        else:
            gauge1 = params['gauge1']
            gauge2 = params['gauge2']
        edge = params['edge']
        hole_diameter = params['hole']
        self.rows = params['rows']
        self.cols = params['cols']
        if 'gauge' in params:
            gauge1 = gauge
            gauge2 = gauge
        width = params['length']
        height = params['width']
        self.plate_width = width
        self.plate_height = height
        outline_pen = QPen(QColor("#8b4513"), 2)
        if self.theme.is_light():
            dimension_pen = QPen(Qt.black, 1)
        else:
            dimension_pen = QPen(QColor("#8A8A8A"), 1)
        angle_pen = QBrush(QColor("#808080"))
        h_offset = 40
        v_offset = 60
        self.scene.setSceneRect(-h_offset, -v_offset, width + 2 * v_offset, height + 2 * h_offset)
        
        background_brush = QBrush(QColor("#A7A796"))
        
        self.scene.addRect(0, 0, width, height, dimension_pen, background_brush)
        self.scene.addRect(0, 0, self.angle_thickness, height, dimension_pen, angle_pen)
        for row in range(self.rows):
            for col in range(self.cols):
                x_center = self.plate_width - edge
                for i in range(col):
                    x_center -= gauge1 if i % 2 == 0 else gauge2
                y_center = end + row * pitch
                x = x_center - hole_diameter / 2
                y = y_center - hole_diameter / 2
                self.scene.addEllipse(x, y, hole_diameter, hole_diameter, outline_pen)
        self.addDimensions(params, dimension_pen)

    def addDimensions(self, params, pen):
        pitch = float(params['pitch'])
        end = float(params['end'])
        if 'gauge' in params:
            gauge = params['gauge']
        else:
            gauge1 = params['gauge1']
            gauge2 = params['gauge2']
        edge = params['edge']
        if 'gauge' in params:
            gauge1 = gauge
            gauge2 = gauge
        width = self.plate_width
        height = self.plate_height
        h_offset = 20
        v_offset = 30
        # Horizontal dimensions
        x_start = width
        segments = []
        segments.append(('edge', x_start - edge, x_start))
        x_start -= edge
        segments.append(('edge', 0, x_start))
        for label, x1, x2 in segments:
            value = x2 - x1
            self.addHorizontalDimension(x1, -h_offset + 10, x2, -h_offset + 10, f"{value:.1f}", pen)
        # Vertical dimensions
        self.addVerticalDimension(width + v_offset - 15, 0, width + v_offset - 15, end, str(end), pen)
        for i in range(self.rows - 1):
            self.addVerticalDimension(width + v_offset - 15, end + i * pitch, width + v_offset- 15, end + (i + 1) * pitch, str(pitch), pen)
        self.addVerticalDimension(width + v_offset - 15, height, width + v_offset - 15, height - end, str(end), pen)
        total_height = 2 * end + (self.rows - 1) * pitch
        self.addVerticalDimension(-v_offset + 10, 0, -v_offset + 10, total_height, str(total_height), pen)

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 3
        ext_length = 10
        self.scene.addLine(x1, y1 - ext_length / 2, x1, y1 + ext_length / 2, pen)
        self.scene.addLine(x2, y2 - ext_length / 2, x2, y2 + ext_length / 2, pen)
        points_left = [(x1, y1), (x1 + arrow_size, y1 - arrow_size / 2), (x1 + arrow_size, y1 + arrow_size / 2)]
        polygon_left = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_left]), pen)
        if self.theme.is_light():
            polygon_left.setBrush(QBrush(Qt.black))
        else:
            polygon_left.setBrush(QBrush(QColor("#8A8A8A")))
        points_right = [(x2, y2), (x2 - arrow_size, y2 - arrow_size / 2), (x2 - arrow_size, y2 + arrow_size / 2)]
        polygon_right = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_right]), pen)
        if self.theme.is_light():
            polygon_right.setBrush(QBrush(Qt.black))
        else:
            polygon_right.setBrush(QBrush(QColor("#8A8A8A")))
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        if self.theme.is_light():
            text_item.setDefaultTextColor(Qt.black)
        else:
            text_item.setDefaultTextColor(Qt.white)
        # Position text
        text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 15)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 3
        ext_length = 10
        self.scene.addLine(x1 - ext_length / 2, y1, x1 + ext_length / 2, y1, pen)
        self.scene.addLine(x2 - ext_length / 2, y2, x2 + ext_length / 2, y2, pen)
        if y2 > y1:
            points_top = [(x1, y1), (x1 - arrow_size / 2, y1 + arrow_size), (x1 + arrow_size / 2, y1 + arrow_size)]
            points_bottom = [(x2, y2), (x2 - arrow_size / 2, y2 - arrow_size), (x2 + arrow_size / 2, y2 - arrow_size)]
        else:
            points_top = [(x2, y2), (x2 - arrow_size / 2, y2 + arrow_size), (x2 + arrow_size / 2, y2 + arrow_size)]
            points_bottom = [(x1, y1), (x1 - arrow_size / 2, y1 - arrow_size), (x1 + arrow_size / 2, y1 - arrow_size)]
        polygon_top = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
        polygon_bottom = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
        if self.theme.is_light():
            polygon_top.setBrush(QBrush(Qt.black))
            polygon_bottom.setBrush(QBrush(Qt.black))
        else:
            polygon_top.setBrush(QBrush(QColor("#8A8A8A")))
            polygon_bottom.setBrush(QBrush(QColor("#8A8A8A")))
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        if self.theme.is_light():
            text_item.setDefaultTextColor(Qt.black)
        else:
            text_item.setDefaultTextColor(Qt.white)
        if x1 < 0:
            text_item.setPos(x1 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)

class CleatAngleCapacityDetails(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2, main=None):
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager
        self.connection = connection_obj
        (self.main, self.flag) = main  # 0 = supported, 1 = supporting

        output = connection_obj.output_values(True)
        data1 = {f"{i[1]} + {i[0]}": i[3] for i in output}

        self.angle_thickness = float(data1['Cleat Angle Designation + Cleat.Angle'].split(" ")[-1])

        self.params = {
            'width': int(data1['Height (mm) + Plate.Height']),
            'hole': int(data1['Diameter (mm) + Bolt.Diameter']),
        }

        if self.flag == 0:
            self.params['length'] = int(data1['Cleat Angle Designation + Cleat.Angle'][0:2])
            self.params['rows'] = int(data1['Bolt Rows (nos) + Bolt.OneLine'])
            self.params['cols'] = int(data1['Bolt Columns (nos) + Bolt.Line'])
            cap_details = connection_obj.bolt_capacity_supported(True)
            self.capacity_title = "Failure Pattern due to Bolt Capacity in Supported Leg"
            spacing_data = connection_obj.spacing(True)
        else:
            self.params['length'] = int(data1['Cleat Angle Designation + Cleat.Angle'][5:7])
            self.params['rows'] = int(data1['Bolt Rows (nos) + Cleat.Spting_leg.OneLine'])
            self.params['cols'] = int(data1['Bolt Columns (nos) + Cleat.Spting_leg.Line'])
            cap_details = connection_obj.bolt_capacity_supporting(True)
            self.capacity_title = "Failure Pattern due to Bolt Capacity in Supporting Leg"
            spacing_data = connection_obj.spting_spacing(True)

        for item in spacing_data:
            if not isinstance(item[0], str):
                continue
            key = item[0].lower()
            value = item[3]
            if 'pitch' in key:
                self.params['pitch'] = value
            elif 'gauge1' in key:
                self.params['gauge1'] = value
            elif 'gauge2' in key:
                self.params['gauge2'] = value
            elif 'end' in key:
                self.params['end'] = value
            elif 'edge' in key:
                self.params['edge'] = value

        dd = {}
        for item in cap_details:
            if item[1] is not None:
                dd[item[1]] = item[3]

        # same values reused in both sections for cleat bolt-capacity popup
        self.dict_shear_failure = {
            'Shear Capacity (kN)': dd.get('Shear Capacity (kN)', 'N/A'),
            'Bearing Capacity (kN)': dd.get('Bearing Capacity (kN)', 'N/A'),
            'Bolt Value (kN)': dd.get('Bolt Value (kN)', 'N/A'),
        }

        self.dict_tension_failure = {
            'Shear Capacity (kN)': dd.get('Shear Capacity (kN)', 'N/A'),
            'Bearing Capacity (kN)': dd.get('Bearing Capacity (kN)', 'N/A'),
            'Bolt Value (kN)': dd.get('Bolt Value (kN)', 'N/A'),
        }

        self.initUI()

    def setupWrapper(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setObjectName("spacing_capacity_details")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle("Bolt Pattern")
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

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = 980, 760
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

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

        # left panel
        left_panel = QWidget()
        left_panel.setMaximumWidth(380)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)

        head = QLabel("Note: Representative image for Beam  Failure Pattern")
        head.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        head.setWordWrap(True)
        left_layout.addWidget(head)

        def add_section(title, data):
            lbl = QLabel(title)
            lbl.setStyleSheet(
                "font-size: 14px; font-weight: bold;"
                "margin-top: 15px; margin-bottom: 5px;"
            )
            left_layout.addWidget(lbl)
            for key, val in data.items():
                row = QHBoxLayout()
                row.addWidget(QLabel(str(key)))
                row.addStretch()
                v = QLabel(f"{val}")
                v.setStyleSheet("font-size: 12px; font-weight: bold;")
                row.addWidget(v)
                left_layout.addLayout(row)

        add_section("Failure Pattern due to Shear", self.dict_shear_failure)
        add_section("Failure Pattern due to Tension", self.dict_tension_failure)
        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)
        right_panel.setLayout(right_layout)

        def make_view(scene, draw_fn, min_h=290):
            view = QGraphicsView(scene)
            view.setBackgroundBrush(
                QBrush(Qt.white) if self.theme.is_light()
                else QBrush(QColor("#4A4A4A"))
            )
            view.setRenderHint(QPainter.Antialiasing)
            view.setMinimumWidth(620)
            view.setMinimumHeight(min_h)
            view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            draw_fn(scene)
            view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
            return view

        lbl1 = QLabel("Failure Pattern due to Shear:")
        lbl1.setStyleSheet("font-size: 14px; font-weight: bold;")
        right_layout.addWidget(lbl1)

        self.scene1 = QGraphicsScene()
        self.view1 = make_view(self.scene1, self.createShearDrawing, 300)
        right_layout.addWidget(self.view1)

        lbl2 = QLabel("Failure Pattern due to Tension:")
        lbl2.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        right_layout.addWidget(lbl2)

        self.scene2 = QGraphicsScene()
        self.view2 = make_view(self.scene2, self.createTensionDrawing, 300)
        right_layout.addWidget(self.view2)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        scroll_area.setWidget(scroll)
        content_layout.addWidget(scroll_area)

    def createShearDrawing(self, scene):
        self._draw_two_variants(scene, mode="shear")

    def createTensionDrawing(self, scene):
        self._draw_two_variants(scene, mode="tension")
    
    def _draw_two_variants(self, scene, mode="shear"):
        scene.clear()
 
        if self.theme.is_light():
            line_pen    = QPen(Qt.black, 1)
            dash_pen    = QPen(Qt.black, 1, Qt.DashLine)
            text_color  = Qt.black
            plate_brush = QBrush(QColor("#F2F2F2"))
            angle_brush = QBrush(QColor("#D9D6C5"))
            bolt_pen    = QPen(QColor("#8B4513"), 2)
            dim_pen     = QPen(Qt.black, 1)
        else:
            line_pen    = QPen(QColor("#D0D0D0"), 1)
            dash_pen    = QPen(QColor("#D0D0D0"), 1, Qt.DashLine)
            text_color  = Qt.white
            plate_brush = QBrush(QColor("#505050"))
            angle_brush = QBrush(QColor("#707070"))
            bolt_pen    = QPen(QColor("#C08040"), 2)
            dim_pen     = QPen(QColor("#D0D0D0"), 1)
 
        # ── scene canvas ──────────────────────────────────────────────────
        scene.setSceneRect(0, 0, 820, 330)
 
        # ── title ─────────────────────────────────────────────────────────
        mode_label = "Shear Failure Pattern" if mode == "shear" else "Tension Failure Pattern"
        title = scene.addText(mode_label)
        f = QFont(); f.setPointSize(14); f.setBold(True)
        title.setFont(f)
        title.setDefaultTextColor(text_color)
        title.setPos(820 / 2 - title.boundingRect().width() / 2, 5)
 
        # ── "2 bolts" side label ──────────────────────────────────────────
        side_lbl = scene.addText("2 bolts")
        f2 = QFont(); f2.setPointSize(11)
        side_lbl.setFont(f2)
        side_lbl.setDefaultTextColor(text_color)
        side_lbl.setPos(8, 140)
 
        # ── group label "1" on left, "2" on right ────────────────────────
        # (drawn after _draw_variant so it sits below both plates)
 
        # ── draw group 1 : two plates, LEFT of scene ─────────────────────
        #    plate-A starts at x=160, plate-B right next to it
        self._draw_variant(scene, 160, 65, mode,
                           group=1,
                           line_pen=line_pen, dash_pen=dash_pen,
                           plate_brush=plate_brush, angle_brush=angle_brush,
                           bolt_pen=bolt_pen, text_color=text_color,
                           dim_pen=dim_pen)
 
        # ── draw group 2 : two plates, RIGHT of scene ────────────────────
        self._draw_variant(scene, 490, 65, mode,
                           group=2,
                           line_pen=line_pen, dash_pen=dash_pen,
                           plate_brush=plate_brush, angle_brush=angle_brush,
                           bolt_pen=bolt_pen, text_color=text_color,
                           dim_pen=dim_pen)
 
    # ─────────────────────────────────────────────────────────────────────
    def _draw_variant(self, scene, start_x, start_y, mode, group,
                      line_pen, dash_pen, plate_brush, angle_brush,
                      bolt_pen, text_color, dim_pen):
        """
        Draws TWO plates side-by-side starting at (start_x, start_y).
        Both plates carry the SAME failure-path dashes.
 
        Shear failure path (group 1 in reference image):
            - Vertical dashed line: top-bolt to bottom-bolt
            - Horizontal dashed line: left-angle-edge  →  bottom-bolt only
              (one-sided L-shape at the bottom)
 
        Tension failure path (group 2 in reference image):
            - Vertical dashed line: top-bolt to bottom-bolt
            - Horizontal dashed line: left-angle-edge  →  top-bolt
            - Horizontal dashed line: left-angle-edge  →  bottom-bolt
              (U/bracket shape touching both bolt rows from the left)
        """
 
        # ── visual geometry (pixels) ──────────────────────────────────────
        plate_w  = 70
        plate_h  = 140
        angle_t  = 12    # width of the darker left strip (angle/cleat leg)
        bolt_r   = 6
        gap_btw  = 20    # horizontal gap between the two plates in a group
 
        # ── real dimension values for labels ─────────────────────────────
        try:
            pitch = float(self.params.get('pitch', 0))
            end   = float(self.params.get('end',   0))
            edge  = float(self.params.get('edge',  0))
        except Exception:
            pitch = end = edge = 0
 
        # ── positions of plate-A and plate-B ─────────────────────────────
        pAx, pAy = start_x,                    start_y
        pBx, pBy = start_x + plate_w + gap_btw, start_y
 
        # ── draw both plates ──────────────────────────────────────────────
        for px, py in [(pAx, pAy), (pBx, pBy)]:
            # main plate rectangle
            scene.addRect(px, py, plate_w, plate_h, line_pen, plate_brush)
            # left darker strip = cleat angle leg / angle section
            scene.addRect(px, py, angle_t, plate_h, line_pen, angle_brush)
 
        # ── bolt centres (same row y for both plates) ─────────────────────
        by_top = pAy + 30
        by_bot = pAy + plate_h - 30
 
        for px in [pAx, pBx]:
            bx = px + plate_w * 0.60
            scene.addEllipse(bx - bolt_r, by_top - bolt_r,
                             2 * bolt_r, 2 * bolt_r, bolt_pen)
            scene.addEllipse(bx - bolt_r, by_bot - bolt_r,
                             2 * bolt_r, 2 * bolt_r, bolt_pen)
 
        # ── failure-path dashed lines on BOTH plates ───────────────────────
        for px in [pAx, pBx]:
            bx          = px + plate_w * 0.60   # bolt column x for this plate
            left_edge_x = px + angle_t           # right edge of the angle strip
 
            if mode == "shear":
                # vertical dash: top-bolt ↔ bottom-bolt
                scene.addLine(bx, by_top, bx, by_bot, dash_pen)
                # horizontal dash: left-edge → bottom-bolt  (L-shape at bottom)
                scene.addLine(left_edge_x, by_bot, bx, by_bot, dash_pen)
 
            else:  # tension
                # vertical dash: top-bolt ↔ bottom-bolt
                scene.addLine(bx, by_top, bx, by_bot, dash_pen)
                # horizontal dash: left-edge → top-bolt
                scene.addLine(left_edge_x, by_top, bx, by_top, dash_pen)
                # horizontal dash: left-edge → bottom-bolt
                scene.addLine(left_edge_x, by_bot, bx, by_bot, dash_pen)
 
        # ── group number label centred below the two-plate group ──────────
        lbl = scene.addText(str(group))
        ff = QFont(); ff.setPointSize(14)
        lbl.setFont(ff)
        lbl.setDefaultTextColor(text_color)
        # centre label under the whole group (spans plate-A + gap + plate-B)
        group_centre_x = start_x + (2 * plate_w + gap_btw) / 2
        lbl.setPos(group_centre_x - lbl.boundingRect().width() / 2,
                   start_y + plate_h + 6)
 
        # ── dimension annotations (on plate-A only, right side) ───────────
        #
        #   Vertical dims (right side of plate-A):
        #       plate-top  →  top-bolt     : end distance
        #       top-bolt   →  bottom-bolt  : pitch
        #       bottom-bolt →  plate-bottom : end distance
        #
        #   Horizontal dim (below plate-A):
        #       bolt-column-x  →  right plate edge : edge distance
        # ─────────────────────────────────────────────────────────────────
 
        arrow  = 4
        ext    = 8
        dim_x  = pAx + plate_w + 5     # x of vertical dim line
        bx_A   = pAx + plate_w * 0.60  # bolt x on plate-A
 
        def _v_dim(x, y1, y2, label):
            if abs(y2 - y1) < 4:
                return
            scene.addLine(x, y1, x, y2, dim_pen)
            scene.addLine(x - ext/2, y1, x + ext/2, y1, dim_pen)
            scene.addLine(x - ext/2, y2, x + ext/2, y2, dim_pen)
            if y2 > y1:
                pts_top = [QPointF(x, y1), QPointF(x-arrow/2, y1+arrow),
                           QPointF(x+arrow/2, y1+arrow)]
                pts_bot = [QPointF(x, y2), QPointF(x-arrow/2, y2-arrow),
                           QPointF(x+arrow/2, y2-arrow)]
            else:
                pts_top = [QPointF(x, y2), QPointF(x-arrow/2, y2+arrow),
                           QPointF(x+arrow/2, y2+arrow)]
                pts_bot = [QPointF(x, y1), QPointF(x-arrow/2, y1-arrow),
                           QPointF(x+arrow/2, y1-arrow)]
            for pts in [pts_top, pts_bot]:
                poly = scene.addPolygon(QPolygonF(pts), dim_pen)
                poly.setBrush(QBrush(
                    Qt.black if self.theme.is_light() else QColor("#D0D0D0")))
            ti = scene.addText(label)
            tf = QFont(); tf.setPointSize(5); ti.setFont(tf)
            ti.setDefaultTextColor(text_color)
            ti.setPos(x + 2, (y1 + y2)/2 - ti.boundingRect().height()/2)
 
        def _h_dim(x1, x2, y, label):
            if abs(x2 - x1) < 4:
                return
            scene.addLine(x1, y, x2, y, dim_pen)
            scene.addLine(x1, y - ext/2, x1, y + ext/2, dim_pen)
            scene.addLine(x2, y - ext/2, x2, y + ext/2, dim_pen)
            pts_l = [QPointF(x1, y), QPointF(x1+arrow, y-arrow/2),
                     QPointF(x1+arrow, y+arrow/2)]
            pts_r = [QPointF(x2, y), QPointF(x2-arrow, y-arrow/2),
                     QPointF(x2-arrow, y+arrow/2)]
            for pts in [pts_l, pts_r]:
                poly = scene.addPolygon(QPolygonF(pts), dim_pen)
                poly.setBrush(QBrush(
                    Qt.black if self.theme.is_light() else QColor("#D0D0D0")))
            ti = scene.addText(label)
            tf = QFont(); tf.setPointSize(5); ti.setFont(tf)
            ti.setDefaultTextColor(text_color)
            ti.setPos((x1+x2)/2 - ti.boundingRect().width()/2, y - 14)
 
        # vertical: end / pitch / end
        if end > 0:
            _v_dim(dim_x, pAy,          by_top,        f"end={end:.0f}")
        if pitch > 0:
            _v_dim(dim_x, by_top,       by_bot,         f"p={pitch:.0f}")
        if end > 0:
            _v_dim(dim_x, by_bot,       pAy + plate_h,  f"end={end:.0f}")
 
        # horizontal: edge distance
        dim_y_h = pAy + plate_h + 28
        if edge > 0:
            _h_dim(bx_A, pAx + plate_w, dim_y_h, f"edge={edge:.0f}")
       

    def _draw_common(self, scene, mode):
        pitch = float(self.params['pitch'])
        end = float(self.params['end'])
        gauge1 = float(self.params.get('gauge1', self.params.get('gauge', 0)))
        gauge2 = float(self.params.get('gauge2', self.params.get('gauge', 0)))
        edge = float(self.params['edge'])
        hole_diameter = float(self.params['hole'])
        self.rows = int(self.params['rows'])
        self.cols = int(self.params['cols'])
        width = float(self.params['length'])
        height = float(self.params['width'])

        self.plate_width = width
        self.plate_height = height

        outline_pen = QPen(QColor("#8b4513"), 2)
        if self.theme.is_light():
            dimension_pen = QPen(Qt.black, 1)
            dash_pen = QPen(Qt.black, 1, Qt.DashLine)
        else:
            dimension_pen = QPen(QColor("#8A8A8A"), 1)
            dash_pen = QPen(QColor("#8A8A8A"), 1, Qt.DashLine)

        angle_pen = QBrush(QColor("#808080"))
        background_brush = QBrush(QColor("#A7A796"))

        h_offset = 40
        v_offset = 60
        scene.setSceneRect(-h_offset, -v_offset, width + 2 * v_offset, height + 2 * h_offset)

        scene.addRect(0, 0, width, height, dimension_pen, background_brush)
        scene.addRect(0, 0, self.angle_thickness, height, dimension_pen, angle_pen)

        bolt_centers = []
        for row in range(self.rows):
            for col in range(self.cols):
                x_center = self.plate_width - edge
                for i in range(col):
                    x_center -= gauge1 if i % 2 == 0 else gauge2
                y_center = end + row * pitch
                bolt_centers.append((x_center, y_center))
                x = x_center - hole_diameter / 2
                y = y_center - hole_diameter / 2
                scene.addEllipse(x, y, hole_diameter, hole_diameter, outline_pen)

        if bolt_centers:
            xs = [p[0] for p in bolt_centers]
            ys = [p[1] for p in bolt_centers]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            if mode == "shear":
                scene.addLine(min_x, min_y, min_x, max_y, dash_pen)
                scene.addLine(min_x, min_y, 0, min_y, dash_pen)
                scene.addLine(min_x, max_y, 0, max_y, dash_pen)

            elif mode == "tension":
                scene.addLine(min_x, min_y, max_x, min_y, dash_pen)
                scene.addLine(min_x, max_y, max_x, max_y, dash_pen)
                scene.addLine(max_x, min_y, max_x, max_y, dash_pen)

        self.addDimensions(scene, dimension_pen)

    def addDimensions(self, scene, pen):
        pitch = float(self.params['pitch'])
        end = float(self.params['end'])
        gauge1 = float(self.params.get('gauge1', self.params.get('gauge', 0)))
        gauge2 = float(self.params.get('gauge2', self.params.get('gauge', 0)))
        edge = float(self.params['edge'])
        width = self.plate_width
        height = self.plate_height

        h_offset = 20
        v_offset = 30

        x_start = width
        segments = []
        segments.append(('edge', x_start - edge, x_start))
        x_start -= edge

        if self.cols > 1:
            current = x_start
            for i in range(self.cols - 1):
                g = gauge1 if i % 2 == 0 else gauge2
                segments.append(('gauge', current - g, current))
                current -= g
            segments.append(('edge', 0, current))
        else:
            segments.append(('edge', 0, x_start))

        for _, x1, x2 in segments:
            value = x2 - x1
            self.addHorizontalDimension(scene, x1, -h_offset + 10, x2, -h_offset + 10, f"{value:.1f}", pen)

        self.addVerticalDimension(scene, width + v_offset - 15, 0, width + v_offset - 15, end, str(end), pen)
        for i in range(self.rows - 1):
            self.addVerticalDimension(
                scene,
                width + v_offset - 15,
                end + i * pitch,
                width + v_offset - 15,
                end + (i + 1) * pitch,
                str(pitch),
                pen
            )
        self.addVerticalDimension(scene, width + v_offset - 15, height, width + v_offset - 15, height - end, str(end), pen)

        total_height = 2 * end + (self.rows - 1) * pitch
        self.addVerticalDimension(scene, -v_offset + 10, 0, -v_offset + 10, total_height, str(total_height), pen)

    def addHorizontalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 3
        ext_length = 10
        scene.addLine(x1, y1 - ext_length / 2, x1, y1 + ext_length / 2, pen)
        scene.addLine(x2, y2 - ext_length / 2, x2, y2 + ext_length / 2, pen)

        points_left = [(x1, y1), (x1 + arrow_size, y1 - arrow_size / 2), (x1 + arrow_size, y1 + arrow_size / 2)]
        polygon_left = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_left]), pen)
        polygon_left.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#8A8A8A")))

        points_right = [(x2, y2), (x2 - arrow_size, y2 - arrow_size / 2), (x2 - arrow_size, y2 + arrow_size / 2)]
        polygon_right = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_right]), pen)
        polygon_right.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#8A8A8A")))

        text_item = scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 15)

    def addVerticalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 3
        ext_length = 10
        scene.addLine(x1 - ext_length / 2, y1, x1 + ext_length / 2, y1, pen)
        scene.addLine(x2 - ext_length / 2, y2, x2 + ext_length / 2, y2, pen)

        if y2 > y1:
            points_top = [(x1, y1), (x1 - arrow_size / 2, y1 + arrow_size), (x1 + arrow_size / 2, y1 + arrow_size)]
            points_bottom = [(x2, y2), (x2 - arrow_size / 2, y2 - arrow_size), (x2 + arrow_size / 2, y2 - arrow_size)]
        else:
            points_top = [(x2, y2), (x2 - arrow_size / 2, y2 + arrow_size), (x2 + arrow_size / 2, y2 + arrow_size)]
            points_bottom = [(x1, y1), (x1 - arrow_size / 2, y1 - arrow_size), (x1 + arrow_size / 2, y1 - arrow_size)]

        polygon_top = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
        polygon_bottom = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
        polygon_top.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#8A8A8A")))
        polygon_bottom.setBrush(QBrush(Qt.black if self.theme.is_light() else QColor("#8A8A8A")))

        text_item = scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)

        if x1 < 0:
            text_item.setPos(x1 - text_item.boundingRect().width(),
                             (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)



class CleatAngleSectionDetails(CleatAngleCapacityDetails):
    """
    Section capacity popup:
    - left side: section capacity values in 2 text groups
    - right side: only ONE image
    """

    def __init__(self, connection_obj, rows=3, cols=2, main=None):
        if isinstance(main, tuple):
            super().__init__(connection_obj, rows, cols, main)
        else:
            super().__init__(connection_obj, rows, cols, (main, 1))

        sec_data = connection_obj.section_capacity_details(True)

        self.dict_shear_failure = {
            'Shear Yielding Capacity (kN)': sec_data[0][3] if len(sec_data) > 0 else 'N/A',
            'Block Shear Capacity (kN)': sec_data[1][3] if len(sec_data) > 1 else 'N/A',
        }

        self.dict_tension_failure = {
            'Moment Demand (kNm)': sec_data[2][3] if len(sec_data) > 2 else 'N/A',
            'Moment Capacity (kNm)': sec_data[3][3] if len(sec_data) > 3 else 'N/A',
        }

    def initUI(self):
        self.setupWrapper()

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = 980, 620
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

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
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(18)

        # ---------------- LEFT PANEL ----------------
        left_panel = QWidget()
        left_panel.setMaximumWidth(360)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(8)

        note = QLabel("Note: Representative image for\nFailure Pattern")
        note.setWordWrap(True)
        note.setStyleSheet("font-size: 16px; margin-bottom: 12px;")
        left_layout.addWidget(note)

        title1 = QLabel("Failure Pattern due to Shear in Supported Section")
        title1.setWordWrap(True)
        title1.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin-top: 10px; margin-bottom: 6px;"
        )
        left_layout.addWidget(title1)

        for key, val in self.dict_shear_failure.items():
            row = QHBoxLayout()
            row.setContentsMargins(0, 2, 0, 2)

            lbl = QLabel(str(key))
            lbl.setWordWrap(True)
            row.addWidget(lbl, 1)

            row.addStretch()

            v = QLabel(str(val))
            v.setStyleSheet("font-size: 12px; font-weight: bold;")
            row.addWidget(v, 0)

            left_layout.addLayout(row)

        title2 = QLabel("Failure Pattern due to Tension in Supporting Section")
        title2.setWordWrap(True)
        title2.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin-top: 20px; margin-bottom: 6px;"
        )
        left_layout.addWidget(title2)

        for key, val in self.dict_tension_failure.items():
            row = QHBoxLayout()
            row.setContentsMargins(0, 2, 0, 2)

            lbl = QLabel(str(key))
            lbl.setWordWrap(True)
            row.addWidget(lbl, 1)

            row.addStretch()

            v = QLabel(str(val))
            v.setStyleSheet("font-size: 12px; font-weight: bold;")
            row.addWidget(v, 0)

            left_layout.addLayout(row)

        left_layout.addStretch()

        # ---------------- RIGHT PANEL ----------------
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)

        title = QLabel("Failure Pattern in Section:")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        right_layout.addWidget(title)

        self.scene1 = QGraphicsScene()
        self.view1 = QGraphicsView(self.scene1)
        self.view1.setBackgroundBrush(
            QBrush(Qt.white) if self.theme.is_light()
            else QBrush(QColor("#4A4A4A"))
        )
        self.view1.setRenderHint(QPainter.Antialiasing)
        self.view1.setMinimumWidth(620)
        self.view1.setMinimumHeight(520)
        self.view1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.createSectionDrawing(self.scene1)
        self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
        right_layout.addWidget(self.view1)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        scroll_area.setWidget(scroll)
        content_layout.addWidget(scroll_area)

    def createSectionDrawing(self, scene):
        self._draw_common(scene, "section")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'view1'):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)