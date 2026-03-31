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
            self.params['rows'] = int(data1.get('Bolt Rows (nos) + Cleat.Spting_leg.OneLine', 0))
            self.params['cols'] = int(data1.get('Bolt Columns (nos) + Cleat.Spting_leg.Line', 0))
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

        head = QLabel("Note: Representative image for Failure Pattern")
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
    
    def draw_blue_bolt(self, scene, cx, cy, r):
     outer_pen = QPen(QColor("#1E2DFF"), 5)
     scene.addEllipse(cx - r, cy - r, 2 * r, 2 * r, outer_pen, QBrush(Qt.white))

    def _dim_text_color(self):
     return Qt.black if self.theme.is_light() else Qt.white

    def _dim_brush_color(self):
     return Qt.black if self.theme.is_light() else QColor("#D0D0D0")

    def add_h_dim(self, scene, x1, x2, y, text, pen, above=True):
     if abs(x2 - x1) < 4:
        return

     arrow = 6
     ext = 12

     scene.addLine(x1, y, x2, y, pen)
     scene.addLine(x1, y - ext / 2, x1, y + ext / 2, pen)
     scene.addLine(x2, y - ext / 2, x2, y + ext / 2, pen)

     pts_l = [QPointF(x1, y), QPointF(x1 + arrow, y - arrow / 2), QPointF(x1 + arrow, y + arrow / 2)]
     pts_r = [QPointF(x2, y), QPointF(x2 - arrow, y - arrow / 2), QPointF(x2 - arrow, y + arrow / 2)]

     for pts in [pts_l, pts_r]:
        poly = scene.addPolygon(QPolygonF(pts), pen)
        poly.setBrush(QBrush(self._dim_brush_color()))

     t = scene.addText(str(text))
     f = QFont()
     f.setPointSize(14)
     f.setBold(True)
     t.setFont(f)
     t.setDefaultTextColor(self._dim_text_color())

     text_x = (x1 + x2) / 2 - t.boundingRect().width() / 2
     if above:
        text_y = y - 28
     else:
        text_y = y + 8

     t.setPos(text_x, text_y)
    
    def add_v_dim(self, scene, x, y1, y2, text, pen):
     if abs(y2 - y1) < 4:
         return

     arrow = 4
     ext = 10

     scene.addLine(x, y1, x, y2, pen)
     scene.addLine(x - ext / 2, y1, x + ext / 2, y1, pen)
     scene.addLine(x - ext / 2, y2, x + ext / 2, y2, pen)

     if y2 > y1:
         pts_top = [QPointF(x, y1), QPointF(x - arrow / 2, y1 + arrow), QPointF(x + arrow / 2, y1 + arrow)]
         pts_bot = [QPointF(x, y2), QPointF(x - arrow / 2, y2 - arrow), QPointF(x + arrow / 2, y2 - arrow)]
     else:
        pts_top = [QPointF(x, y2), QPointF(x - arrow / 2, y2 + arrow), QPointF(x + arrow / 2, y2 + arrow)]
        pts_bot = [QPointF(x, y1), QPointF(x - arrow / 2, y1 - arrow), QPointF(x + arrow / 2, y1 - arrow)]

     for pts in [pts_top, pts_bot]:
        poly = scene.addPolygon(QPolygonF(pts), pen)
        poly.setBrush(QBrush(self._dim_brush_color()))

     t = scene.addText(str(text))
     f = QFont()
     f.setPointSize(14)
     f.setBold(True)
     t.setFont(f)
     t.setDefaultTextColor(self._dim_text_color())
     t.setPos(x + 8, (y1 + y2) / 2 - t.boundingRect().height() / 2)

    def createShearDrawing(self, scene):
     if self.flag == 0:
        self._draw_supported_leg_shear(scene)
     else:
        self._draw_supporting_leg_shear(scene)

    def createTensionDrawing(self, scene):
     if self.flag == 0:
        self._draw_supported_leg_tension(scene)
     else:
        self._draw_supporting_leg_tension(scene)
    
    def _draw_supported_leg_shear(self, scene):
     self._draw_plate_pair(scene, mode="shear", leg="supported")

    def _draw_supported_leg_tension(self, scene):
     self._draw_plate_pair(scene, mode="tension", leg="supported")
    
    def _draw_supporting_leg_shear(self, scene):
     self._draw_plate_pair(scene, mode="shear", leg="supporting")

    def _draw_supporting_leg_tension(self, scene):
     self._draw_plate_pair(scene, mode="tension", leg="supporting")

    def _draw_plate_pair(self, scene, mode="shear", leg="supported"):
     scene.clear()

     if self.theme.is_light():
        line_pen = QPen(Qt.black, 2)
        dash_pen = QPen(Qt.black, 2, Qt.DashLine)
        plate_brush = QBrush(QColor("#F2F2F2"))
        angle_brush = QBrush(QColor("#9A9A9A"))
        bolt_pen = QPen(Qt.black, 2)
     else:
        line_pen = QPen(QColor("#D0D0D0"), 2)
        dash_pen = QPen(QColor("#D0D0D0"), 2, Qt.DashLine)
        plate_brush = QBrush(QColor("#505050"))
        angle_brush = QBrush(QColor("#808080"))
        bolt_pen = QPen(QColor("#D0D0D0"), 2)
     
     if self.theme.is_light():
      dim_pen = QPen(Qt.black, 1)
     else:
      dim_pen = QPen(QColor("#D0D0D0"), 1)

     scene.setSceneRect(-80, -80, 1040, 560)
 
     plate_w = 180
     plate_h = 290
     strip_w = 14
     start_y = 40

     left_x = 110
     right_x = 480

     pitch = float(self.params.get("pitch", 0))
     end = float(self.params.get("end", 0))
     edge = float(self.params.get("edge", 0))
     gauge1 = float(self.params.get("gauge1", 0))
     gauge2 = float(self.params.get("gauge2", 0))
     length = float(self.params.get("length", 0))
     height = float(self.params.get("width", 0))
     hole = float(self.params.get("hole", 0))
     rows = int(self.params.get("rows", 0))
     cols = int(self.params.get("cols", 0))
    

    # bolt positions
     if leg == "supporting" and mode == "shear":
        top_bolt_y = start_y + 90
        bot_bolt_y = start_y + 240
     else:
        top_bolt_y = start_y + 60
        bot_bolt_y = start_y + 210

     bolt_r = 11
     bolt_x_left = left_x + plate_w * 0.50
     bolt_x_right = right_x + plate_w * 0.50

    # left plate
     scene.addRect(left_x, start_y, plate_w, plate_h, line_pen, plate_brush)
     scene.addRect(left_x + plate_w - strip_w, start_y, strip_w, plate_h, line_pen, angle_brush)

    # right plate
     scene.addRect(right_x, start_y, plate_w, plate_h, line_pen, plate_brush)
     scene.addRect(right_x, start_y, strip_w, plate_h, line_pen, angle_brush)

    # bolts
     self.draw_blue_bolt(scene, bolt_x_left, top_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_left, bot_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_right, top_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_right, bot_bolt_y, bolt_r)

    # -------- SUPPORTED LEG --------
     if leg == "supported":
        if mode == "shear":
            scene.addLine(bolt_x_left, start_y, bolt_x_left, bot_bolt_y, dash_pen)
            scene.addLine(left_x, bot_bolt_y, bolt_x_left, bot_bolt_y, dash_pen)

        # RIGHT figure
            scene.addLine(bolt_x_right, start_y, bolt_x_right, bot_bolt_y, dash_pen)
            scene.addLine(bolt_x_right, bot_bolt_y, right_x + plate_w, bot_bolt_y, dash_pen)

        elif mode == "tension":
            # left figure
            scene.addLine(bolt_x_left, top_bolt_y, bolt_x_left, bot_bolt_y, dash_pen)
            scene.addLine(left_x, top_bolt_y, bolt_x_left, top_bolt_y, dash_pen)
            scene.addLine(left_x, bot_bolt_y, bolt_x_left, bot_bolt_y, dash_pen)

            # right figure
            scene.addLine(bolt_x_right, top_bolt_y, bolt_x_right, bot_bolt_y, dash_pen)
            scene.addLine(bolt_x_right, top_bolt_y, right_x + plate_w, top_bolt_y, dash_pen)
            scene.addLine(bolt_x_right, bot_bolt_y, right_x + plate_w, bot_bolt_y, dash_pen)
            # ---- supported leg common dimensions ----
        dim_x_r = left_x + plate_w + 22
        dim_x_l = left_x - 28
        dim_y_b = start_y + plate_h + 26

    # vertical: end, pitch, end
        if end > 0:
         self.add_v_dim(scene, dim_x_r, start_y, top_bolt_y, f"{end:.0f}", dim_pen)

        if pitch > 0:
         self.add_v_dim(scene, dim_x_r, top_bolt_y, bot_bolt_y, f"{pitch:.0f}", dim_pen)

        if end > 0:
         self.add_v_dim(scene, dim_x_r, bot_bolt_y, start_y + plate_h, f"{end:.0f}", dim_pen)

   

    # horizontal: edge
        if edge > 0:
         self.add_h_dim(scene, bolt_x_left, left_x + plate_w, dim_y_b, f"{edge:.0f}", dim_pen, above=False)

    # horizontal: plate/leg length
        if length > 0:
         self.add_h_dim(scene, left_x, left_x + plate_w, start_y - 22, f"{length:.0f}", dim_pen, above=True)

    # vertical: plate height
        if height > 0:
         self.add_v_dim(scene, left_x - 55, start_y, start_y + plate_h, f"{height:.0f}", dim_pen)

    # hole diameter
        # if hole > 0:
        #  self.add_h_dim(scene, bolt_x_left - bolt_r, bolt_x_left + bolt_r, bot_bolt_y + 28, f"Ø{hole:.0f}", dim_pen)

    # gauge if available
        if cols > 1 and gauge1 > 0:
         self.add_h_dim(
            scene,
            left_x + plate_w - edge - gauge1,
            left_x + plate_w - edge,
            start_y - 42,
            f"g={gauge1:.0f}",
            dim_pen
        )
    # -------- SUPPORTING LEG --------
     elif leg == "supporting":
        if mode == "shear":
            # left figure: top horizontal to left edge, vertical from top bolt to bottom edge
            scene.addLine(left_x, top_bolt_y, bolt_x_left, top_bolt_y, dash_pen)
            scene.addLine(bolt_x_left, top_bolt_y, bolt_x_left, start_y + plate_h, dash_pen)

            # right figure: top horizontal to right edge, vertical from top bolt to bottom edge
            scene.addLine(bolt_x_right, top_bolt_y, right_x + plate_w, top_bolt_y, dash_pen)
            scene.addLine(bolt_x_right, top_bolt_y, bolt_x_right, start_y + plate_h, dash_pen)

        elif mode == "tension":
            # left figure
            scene.addLine(bolt_x_left, top_bolt_y, bolt_x_left, bot_bolt_y, dash_pen)
            scene.addLine(left_x, top_bolt_y, bolt_x_left, top_bolt_y, dash_pen)
            scene.addLine(left_x, bot_bolt_y, bolt_x_left, bot_bolt_y, dash_pen)

            # right figure
            scene.addLine(bolt_x_right, top_bolt_y, bolt_x_right, bot_bolt_y, dash_pen)
            scene.addLine(bolt_x_right, top_bolt_y, right_x + plate_w, top_bolt_y, dash_pen)
            scene.addLine(bolt_x_right, bot_bolt_y, right_x + plate_w, bot_bolt_y, dash_pen)
        
        # supporting leg dimensions (right side of left figure)
        dim_x_r = left_x + plate_w + 22
        dim_y_b = start_y + plate_h + 26

        if mode == "shear":
    # top bolt to bottom edge representative vertical
         if pitch > 0 or end > 0:
          self.add_v_dim(scene, dim_x_r, top_bolt_y, start_y + plate_h, f, dim_pen)
 
         if edge > 0:
          self.add_h_dim(scene, left_x, bolt_x_left, start_y - 22, f"{edge:.0f}", dim_pen)

        else:  # tension
         if end > 0:
          self.add_v_dim(scene, dim_x_r, start_y, top_bolt_y, f"{end:.0f}", dim_pen)
         if pitch > 0:
          self.add_v_dim(scene, dim_x_r, top_bolt_y, bot_bolt_y, f"{pitch:.0f}", dim_pen)
         if end > 0:
          self.add_v_dim(scene, dim_x_r, bot_bolt_y, start_y + plate_h, f"{end:.0f}", dim_pen)

         if edge > 0:
          self.add_h_dim(scene, left_x, bolt_x_left, start_y - 22, f"{edge:.0f}", dim_pen)

        if length > 0:
         self.add_h_dim(scene, left_x, left_x + plate_w, start_y - 12, f"{length:.0f}", dim_pen)

        if height > 0:
         self.add_v_dim(scene, left_x - 55, start_y, start_y + plate_h, f"{height:.0f}", dim_pen)

        # if hole > 0:
        #  self.add_h_dim(scene, bolt_x_left - bolt_r, bolt_x_left + bolt_r, bot_bolt_y + 28, f"Ø{hole:.0f}", dim_pen)

        if cols > 1 and gauge1 > 0:
         self.add_h_dim(scene, left_x + strip_w, bolt_x_left, start_y +3, f"{gauge1:.0f}", dim_pen)

    def _draw_supporting_leg_shear(self, scene):
     scene.clear()

     if self.theme.is_light():
        line_pen = QPen(Qt.black, 2)
        dash_pen = QPen(Qt.black, 2, Qt.DashLine)
        plate_brush = QBrush(QColor("#F2F2F2"))
        angle_brush = QBrush(QColor("#9A9A9A"))
        dim_pen = QPen(Qt.black, 1)
     else:
        line_pen = QPen(QColor("#D0D0D0"), 2)
        dash_pen = QPen(QColor("#D0D0D0"), 2, Qt.DashLine)
        plate_brush = QBrush(QColor("#505050"))
        angle_brush = QBrush(QColor("#808080"))
        dim_pen = QPen(QColor("#D0D0D0"), 1)

     scene.setSceneRect(-80, -80, 1040, 560)

     plate_w = 180
     plate_h = 290
     strip_w = 14
     start_y = 40

     left_x = 110
     right_x = 480

     pitch = float(self.params.get("pitch", 0))
     end = float(self.params.get("end", 0))
     edge = float(self.params.get("edge", 0))
     gauge1 = float(self.params.get("gauge1", 0))
     length = float(self.params.get("length", 0))
     height = float(self.params.get("width", 0))
     cols = int(self.params.get("cols", 0))

     top_bolt_y = start_y + 90
     bot_bolt_y = start_y + 240
     bolt_r = 11

     bolt_x_left = left_x + plate_w * 0.50
     bolt_x_right = right_x + plate_w * 0.50

    # left plate
     scene.addRect(left_x, start_y, plate_w, plate_h, line_pen, plate_brush)
     scene.addRect(left_x + plate_w - strip_w, start_y, strip_w, plate_h, line_pen, angle_brush)

    # right plate
     scene.addRect(right_x, start_y, plate_w, plate_h, line_pen, plate_brush)
     scene.addRect(right_x, start_y, strip_w, plate_h, line_pen, angle_brush)

    # bolts
     self.draw_blue_bolt(scene, bolt_x_left, top_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_left, bot_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_right, top_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_right, bot_bolt_y, bolt_r)

    # LEFT figure
     scene.addLine(left_x, top_bolt_y, bolt_x_left, top_bolt_y, dash_pen)
     scene.addLine(bolt_x_left, top_bolt_y, bolt_x_left, start_y + plate_h, dash_pen)

    # RIGHT figure
     scene.addLine(bolt_x_right, top_bolt_y, right_x + plate_w, top_bolt_y, dash_pen)
     scene.addLine(bolt_x_right, top_bolt_y, bolt_x_right, start_y + plate_h, dash_pen)

    # ---------------- DIMENSIONS ----------------
     dim_x_left = left_x - 42
     dim_x_right = left_x + plate_w + 28   # one common vertical dim line
     top_dim_y = start_y - 28
     bottom_dim_y = start_y + plate_h + 42
     gauge_dim_y = start_y + 18

# overall plate height
     if height > 0:
      self.add_v_dim(scene, dim_x_left, start_y, start_y + plate_h, f"{height:.0f}", dim_pen)

# one straight vertical stack: 15, 40, 15
     if end > 0:
      self.add_v_dim(scene, dim_x_right, start_y, top_bolt_y, f"{end:.0f}", dim_pen)

     if pitch > 0:
      self.add_v_dim(scene, dim_x_right, top_bolt_y, bot_bolt_y, f"{pitch:.0f}", dim_pen)

     if end > 0:
      self.add_v_dim(scene, dim_x_right, bot_bolt_y, start_y + plate_h, f"{end:.0f}", dim_pen)

# top overall width/leg size
     if length > 0:
      self.add_h_dim(scene, left_x, left_x + plate_w, top_dim_y, f"{length:.0f}", dim_pen)

# bottom edge distance
     if edge > 0:
      self.add_h_dim(scene, left_x, bolt_x_left, bottom_dim_y, f"{edge:.0f}", dim_pen, above=False)

# gauge
     if cols > 1 and gauge1 > 0:
      self.add_h_dim(scene, left_x + strip_w, bolt_x_left, gauge_dim_y, f"{gauge1:.0f}", dim_pen)

    def _draw_supporting_leg_tension(self, scene):
     scene.clear()

     if self.theme.is_light():
        line_pen = QPen(Qt.black, 2)
        dash_pen = QPen(Qt.black, 2, Qt.DashLine)
        plate_brush = QBrush(QColor("#F2F2F2"))
        angle_brush = QBrush(QColor("#9A9A9A"))
        bolt_pen = QPen(Qt.black, 2)
        dim_pen = QPen(Qt.black, 1)
     else:
        line_pen = QPen(QColor("#D0D0D0"), 2)
        dash_pen = QPen(QColor("#D0D0D0"), 2, Qt.DashLine)
        plate_brush = QBrush(QColor("#505050"))
        angle_brush = QBrush(QColor("#808080"))
        bolt_pen = QPen(QColor("#D0D0D0"), 2)
        dim_pen = QPen(QColor("#D0D0D0"), 1)

     scene.setSceneRect(-80, -80, 1040, 560)

     plate_w = 180
     plate_h = 290
     strip_w = 14
     start_y = 40

     left_x = 110
     right_x = 480

     pitch = float(self.params.get("pitch", 0))
     end = float(self.params.get("end", 0))
     edge = float(self.params.get("edge", 0))
     gauge1 = float(self.params.get("gauge1", 0))
     length = float(self.params.get("length", 0))
     height = float(self.params.get("width", 0))
     hole = float(self.params.get("hole", 0))
     cols = int(self.params.get("cols", 0)) 

     top_bolt_y = start_y + 60
     bot_bolt_y = start_y + 210
     bolt_r = 11

     bolt_x_left = left_x + plate_w * 0.50
     bolt_x_right = right_x + plate_w * 0.50

    # LEFT plate
     scene.addRect(left_x, start_y, plate_w, plate_h, line_pen, plate_brush)
     scene.addRect(left_x + plate_w - strip_w, start_y, strip_w, plate_h, line_pen, angle_brush)

    # RIGHT plate
     scene.addRect(right_x, start_y, plate_w, plate_h, line_pen, plate_brush)
     scene.addRect(right_x, start_y, strip_w, plate_h, line_pen, angle_brush)

    # bolts
     self.draw_blue_bolt(scene, bolt_x_left, top_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_left, bot_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_right, top_bolt_y, bolt_r)
     self.draw_blue_bolt(scene, bolt_x_right, bot_bolt_y, bolt_r)

    # LEFT figure
     scene.addLine(bolt_x_left, top_bolt_y, bolt_x_left, bot_bolt_y, dash_pen)
     scene.addLine(left_x, top_bolt_y, bolt_x_left, top_bolt_y, dash_pen)
     scene.addLine(left_x, bot_bolt_y, bolt_x_left, bot_bolt_y, dash_pen)

    # RIGHT figure
     scene.addLine(bolt_x_right, top_bolt_y, bolt_x_right, bot_bolt_y, dash_pen)
     scene.addLine(bolt_x_right, top_bolt_y, right_x + plate_w, top_bolt_y, dash_pen)
     scene.addLine(bolt_x_right, bot_bolt_y, right_x + plate_w, bot_bolt_y, dash_pen)

    # dimensions for supporting leg tension
     dim_x_r = left_x + plate_w + 30
     dim_x_l = left_x - 55

     if end > 0:
        self.add_v_dim(scene, dim_x_r, start_y, top_bolt_y, f"{end:.0f}", dim_pen)

     if pitch > 0:
        self.add_v_dim(scene, dim_x_r, top_bolt_y, bot_bolt_y, f"{pitch:.0f}", dim_pen)

     if end > 0:
        self.add_v_dim(scene, dim_x_r, bot_bolt_y, start_y + plate_h, f"{end:.0f}", dim_pen)

     if edge > 0:
        self.add_h_dim(scene, left_x, bolt_x_left, start_y + plate_h + 55, f"{edge:.0f}", dim_pen)

     if length > 0:
        self.add_h_dim(scene, left_x, left_x + plate_w, start_y - 12, f"{length:.0f}", dim_pen)

     if height > 0:
        self.add_v_dim(scene, dim_x_l, start_y, start_y + plate_h, f"{height:.0f}", dim_pen)

    #  if hole > 0:
    #     self.add_h_dim(scene, bolt_x_left - bolt_r, bolt_x_left + bolt_r, bot_bolt_y + 32, f"Ø{hole:.0f}", dim_pen)

     if cols > 1 and gauge1 > 0:
        self.add_h_dim(scene, left_x + strip_w, bolt_x_left, start_y + 28, f"{gauge1:.0f}", dim_pen)
       

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
        self._draw_section_capacity_pattern(scene)

    def _draw_section_capacity_pattern(self, scene):
        scene.clear()

        if self.theme.is_light():
            struct_pen = QPen(QColor("#5E5E5E"), 2)
            plate_pen = QPen(QColor("#444444"), 2)
            dim_pen = QPen(Qt.black, 1)
            dash_pen = QPen(Qt.black, 1.5, Qt.DashLine)
            beam_brush = QBrush(QColor("#9A9A9A"))
            plate_brush = QBrush(QColor("#F8F8F8"))
            weld_brush = QBrush(QColor("#D2905A"))
            weld_pen = QPen(QColor("#C07840"), 1)
        else:
            struct_pen = QPen(QColor("#D0D0D0"), 2)
            plate_pen = QPen(QColor("#DADADA"), 2)
            dim_pen = QPen(QColor("#E0E0E0"), 1)
            dash_pen = QPen(QColor("#D0D0D0"), 1.5, Qt.DashLine)
            beam_brush = QBrush(QColor("#7A7A7A"))
            plate_brush = QBrush(QColor("#505050"))
            weld_brush = QBrush(QColor("#C07A45"))
            weld_pen = QPen(QColor("#C07A45"), 1)

        scene.setSceneRect(-140, -100, 980, 1040)

        # -------- values from cleat inputs --------
        pitch = float(self.params.get("pitch", 0))
        end = float(self.params.get("end", 0))
        edge = float(self.params.get("edge", 0))
        gauge = float(self.params.get("gauge1", 0))
        total_height = 2 * end + pitch

        # -------- geometry --------
        flange_w = 360
        flange_t = 18
        web_t = 14
        cx = 365

        top_flange_y = 150
        bot_flange_y = 700
        web_y1 = top_flange_y + flange_t
        web_y2 = bot_flange_y

        # section / beam
        scene.addRect(cx - flange_w / 2, top_flange_y, flange_w, flange_t, struct_pen, beam_brush)
        scene.addRect(cx - web_t / 2, web_y1, web_t, web_y2 - web_y1, struct_pen, beam_brush)
        scene.addRect(cx - flange_w / 2, bot_flange_y, flange_w, flange_t, struct_pen, beam_brush)

        # plates
        plate_w = 190
        plate_h = 340
        plate_y = 220

        left_plate_x = 180
        right_plate_x = 360

        scene.addRect(left_plate_x, plate_y, plate_w, plate_h, plate_pen, plate_brush)
        scene.addRect(right_plate_x, plate_y, plate_w, plate_h, plate_pen, plate_brush)

        # weld strips near web
        weld_w = 10
        scene.addRect(cx - web_t / 2 - weld_w, plate_y, weld_w, plate_h, weld_pen, weld_brush)
        scene.addRect(cx + web_t / 2, plate_y, weld_w, plate_h, weld_pen, weld_brush)

        # bolts
        # bolts
        bolt_r = 13
        top_bolt_y = plate_y + 85
        bot_bolt_y = plate_y + 255

# bolt centres symmetric about web centre
        left_bolt_x = left_plate_x + plate_w / 2
        right_bolt_x = right_plate_x + plate_w / 2
        self.draw_blue_bolt(scene, left_bolt_x, top_bolt_y, bolt_r)
        self.draw_blue_bolt(scene, left_bolt_x, bot_bolt_y, bolt_r)
        self.draw_blue_bolt(scene, right_bolt_x, top_bolt_y, bolt_r)
        self.draw_blue_bolt(scene, right_bolt_x, bot_bolt_y, bolt_r)

        # dashed pattern rectangle
        scene.addLine(left_bolt_x, top_bolt_y, right_bolt_x, top_bolt_y, dash_pen)
        scene.addLine(left_bolt_x, bot_bolt_y, right_bolt_x, bot_bolt_y, dash_pen)
        scene.addLine(left_bolt_x, top_bolt_y, left_bolt_x, bot_bolt_y, dash_pen)
        scene.addLine(right_bolt_x, top_bolt_y, right_bolt_x, bot_bolt_y, dash_pen)

        # -------- dimensions --------

        # top: 82.0 82.0 style
        top_dim_y = top_flange_y - 70
        if gauge > 0:
            self.add_h_dim(scene, left_plate_x, cx - web_t / 2, top_dim_y, f"{gauge:.1f}", dim_pen)
            self.add_h_dim(scene, cx + web_t / 2, right_plate_x + plate_w, top_dim_y, f"{gauge:.1f}", dim_pen)

        # left: 70.0 style overall
        left_dim_x = left_plate_x - 110
        if total_height > 0:
            self.add_v_dim(scene, left_dim_x, plate_y, plate_y + plate_h, f"{total_height:.1f}", dim_pen)

        # right: 15.0 / 40.0 / 15.0 in one line
        right_dim_x = right_plate_x + plate_w + 110
        if end > 0:
            self.add_v_dim(scene, right_dim_x, plate_y, top_bolt_y, f"{end:.1f}", dim_pen)
        if pitch > 0:
            self.add_v_dim(scene, right_dim_x, top_bolt_y, bot_bolt_y, f"{pitch:.1f}", dim_pen)
        if end > 0:
            self.add_v_dim(scene, right_dim_x, bot_bolt_y, plate_y + plate_h, f"{end:.1f}", dim_pen)

        # bottom: 15.0 15.0 15.0 15.0 style
        bottom_dim_y = bot_flange_y - 55

        x0 = left_plate_x
        x1 = left_bolt_x
        x2 = cx - web_t / 2
        x3 = cx + web_t / 2
        x4 = right_bolt_x
        x5 = right_plate_x + plate_w

        if edge > 0:
            self.add_h_dim(scene, x0, x1, bottom_dim_y, f"{edge:.1f}", dim_pen, above=False)
            self.add_h_dim(scene, x1, x2, bottom_dim_y, f"{edge:.1f}", dim_pen, above=False)
            self.add_h_dim(scene, x3, x4, bottom_dim_y, f"{edge:.1f}", dim_pen, above=False)
            self.add_h_dim(scene, x4, x5, bottom_dim_y, f"{edge:.1f}", dim_pen, above=False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'view1'):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)