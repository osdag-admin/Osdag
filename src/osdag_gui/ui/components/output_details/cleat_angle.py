from PySide6.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
                             QGraphicsScene, QScrollArea)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtGui import QPolygonF, QBrush
from PySide6.QtCore import QPointF
from ..dialogs.custom_titlebar import CustomTitleBar
from .cleat_cfbw_dxf_renderer import try_draw_cfbw
from .cleat_cwbw_dxf_renderer import try_draw_cwbw
from .cleat_bb_dxf_renderer import try_draw_bb
from osdag_core.Common import *
from math import cos, pi, sin
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainterPath, QTransform
from PySide6.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsRectItem


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
            params['rows'] = int(
            data1.get('Bolt Rows (nos) + Bolt.OneLine',
            data1.get('Bolt Rows (no) + Bolt.OneLine', 0))
            )
            params['cols'] = int(
            data1.get('Bolt Columns (nos) + Bolt.Line',
            data1.get('Bolt Columns (no) + Bolt.Line', 0))
          )
        else:
            params['length'] = int(data1['Cleat Angle Designation + Cleat.Angle'][5:7])
            params['rows'] = int(
             data1.get('Bolt Rows (nos) + Cleat.Spting_leg.OneLine',
             data1.get('Bolt Rows (no) + Cleat.Spting_leg.OneLine', 0))
        )  
            params['cols'] = int(
              data1.get('Bolt Columns (nos) + Cleat.Spting_leg.Line',
              data1.get('Bolt Columns (no) + Cleat.Spting_leg.Line', 0))
          )

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
         self.params['rows'] = int(
         data1.get('Bolt Rows (nos) + Bolt.OneLine',
         data1.get('Bolt Rows (no) + Bolt.OneLine', 0))
        )
         self.params['cols'] = int(
         data1.get('Bolt Columns (nos) + Bolt.Line',
         data1.get('Bolt Columns (no) + Bolt.Line', 0))
         )
         cap_details = connection_obj.bolt_capacity_supported(True)
         self.capacity_title = "Failure Pattern due to Bolt Capacity in Supported Leg"
         spacing_data = connection_obj.spacing(True)
            
        else:
            self.params['length'] = int(data1['Cleat Angle Designation + Cleat.Angle'][5:7])

            
            self.params['rows'] = int(
    data1.get('Bolt Rows (nos) + Cleat.Spting_leg.OneLine',
    data1.get('Bolt Rows (no) + Cleat.Spting_leg.OneLine', 0))
)
            self.params['cols'] = int(
    data1.get('Bolt Columns (nos) + Cleat.Spting_leg.Line',
    data1.get('Bolt Columns (no) + Cleat.Spting_leg.Line', 0))
)
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
     if try_draw_cfbw(self, scene, "shear"):
        return
     if try_draw_cwbw(self, scene, "shear"):
        return
     if try_draw_bb(self, scene, "shear"):
        return
     if self.flag == 0:
        self._draw_supported_leg_shear(scene)
     else:
        self._draw_supporting_leg_shear(scene)

    def createTensionDrawing(self, scene):
     if try_draw_cfbw(self, scene, "tension"):
        return
     if try_draw_cwbw(self, scene, "tension"):
        return
     if try_draw_bb(self, scene, "tension"):
        return
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
          path_val = (start_y + plate_h) - top_bolt_y
          self.add_v_dim(scene, dim_x_r, top_bolt_y, start_y + plate_h, f"{path_val:.0f}", dim_pen)
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


# =====================================================================================================
# Section details -> Capacity diagrams (Cleat Angle: Column Web-Beam Web and Beam-Beam).
# Used only by CleatAngleSectionDetails.  Proportions are measured on the reference drawings and expressed in
# units of H = cleat plate height; layering (back -> front): primary member, beam flanges, plates, FAILURE
# PATTERN, beam web, thin cleat-leg strips, bolts.  Colours are fixed: column/primary #f4f4e3, plates #dbdbce,
# bolts #ff0d0d, beam #ffffff, failure pattern black.  Dimension numbers/formats are the legacy ones.
# Any other connectivity (or any failure) returns False -> the legacy drawing code is used.
# =====================================================================================================
_SEC_CWBW = "Column Web-Beam Web"
_SEC_BB = "Beam-Beam"

_SEC_COL_COLUMN = QColor("#f4f4e3")
_SEC_COL_PLATE = QColor("#dbdbce")
_SEC_COL_BOLT = QColor("#ff0d0d")
_SEC_COL_BEAM = QColor("#ffffff")
_SEC_COL_LINE = QColor("#000000")
_SEC_COL_FAIL = QColor("#000000")

# ---- reference proportions (units of H, or of D / B where stated)
_SEC_D_OVER_H = 2.19
_SEC_FLANGE_OVER_PLATES = 1.43          # beam flange width / overall plate width
_SEC_TF_OVER_H = 0.15
_SEC_TW_OVER_H = 0.11
_SEC_STRIP_OVER_H = 0.05                # thin strip beside the web (measured: ~2 px on a 36 px plate)
_SEC_GAP_TOP_CWBW, _SEC_GAP_TOP_BB = 0.186, 0.31
_SEC_COLUMN_H_OVER_D, _SEC_COLUMN_W_OVER_B, _SEC_COLUMN_STRIP = 6.54, 1.63, 0.03
_SEC_PRIMARY_W_OVER_B, _SEC_PRIMARY_D_OVER_D, _SEC_PRIMARY_TF_OVER_D = 6.78, 1.68, 0.06
_SEC_H_UNITS = 300.0                    # plate height in scene units (scale = _SEC_H_UNITS / total height in mm)
_SEC_TEXT_PX = 12                       # dimension number height on screen (constant)


# ------------------------------------------------------------------ helpers
def _sec_f(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _sec_pen(w=1.0, color=_SEC_COL_LINE, style=Qt.SolidLine):
    p = QPen(color, w, style)
    p.setCosmetic(True)                              # constant on-screen width at any zoom
    return p


def _sec_rect(scene, x0, y0, x1, y1, brush, pen=None, z=1):
    r = QGraphicsRectItem(QRectF(min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0)))
    r.setBrush(QBrush(brush) if brush is not None else QBrush(Qt.NoBrush))
    r.setPen(pen if pen is not None else QPen(Qt.NoPen))
    r.setZValue(z)
    scene.addItem(r)
    return r


def _sec_line(scene, x0, y0, x1, y1, pen, z=1):
    ln = scene.addLine(x0, y0, x1, y1, pen)
    ln.setZValue(z)
    return ln


def _sec_hexagon(scene, cx, cy, r, z):
    """Face-on bolt head: hexagon with vertices to the left / right."""
    path = QPainterPath()
    path.addPolygon(QPolygonF([QPointF(cx + r * cos(k * pi / 3.0), cy + r * sin(k * pi / 3.0)) for k in range(6)]))
    path.closeSubpath()
    item = QGraphicsPathItem(path)
    item.setBrush(QBrush(_SEC_COL_BOLT))
    item.setPen(_sec_pen(1.0))
    item.setZValue(z)
    scene.addItem(item)


def _sec_text(scene, text, x, y, where, shift=0):
    """Dimension number with constant on-screen size, anchored at scene point (x, y).
    where: 'above' | 'below' (centred) | 'right' | 'left' (vertically centred)."""
    t = scene.addText(str(text))
    f = QFont()
    f.setPixelSize(_SEC_TEXT_PX)
    f.setBold(True)
    t.setFont(f)
    t.document().setDocumentMargin(0)
    t.setDefaultTextColor(_SEC_COL_LINE)
    t.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
    t.setZValue(20)
    w, h = t.boundingRect().width(), t.boundingRect().height()
    dx, dy = {"above": (-w / 2.0, -h - 3), "below": (-w / 2.0, 3), "right": (9 + shift, -h / 2.0), "left": (-w - 9 - shift, -h / 2.0)}[where]
    t.setPos(x, y)
    t.setTransform(QTransform.fromTranslate(dx, dy))


class _SecDims:
    """Dimension drawing with arrow / tick sizes proportional to the plate height."""

    def __init__(self, scene, H):
        self.scene, self.a, self.ext = scene, 0.05 * H, 0.07 * H

    def _arrow(self, pts):
        path = QPainterPath()
        path.addPolygon(QPolygonF([QPointF(*p) for p in pts]))
        path.closeSubpath()
        it = QGraphicsPathItem(path)
        it.setBrush(QBrush(_SEC_COL_LINE))
        it.setPen(_sec_pen(1.0))
        it.setZValue(20)
        self.scene.addItem(it)

    def h(self, x1, x2, y, text, above=True):
        if abs(x2 - x1) < 2:
            return
        sc, a, e = self.scene, self.a, self.ext
        _sec_line(sc, x1, y, x2, y, _sec_pen(), 20)
        _sec_line(sc, x1, y - e / 2, x1, y + e / 2, _sec_pen(), 20)
        _sec_line(sc, x2, y - e / 2, x2, y + e / 2, _sec_pen(), 20)
        self._arrow([(x1, y), (x1 + a, y - a / 3), (x1 + a, y + a / 3)])
        self._arrow([(x2, y), (x2 - a, y - a / 3), (x2 - a, y + a / 3)])
        _sec_text(sc, text, (x1 + x2) / 2.0, y, "above" if above else "below")

    def v(self, x, y1, y2, text, left=False, shift=0):
        if abs(y2 - y1) < 2:
            return
        sc, a, e = self.scene, self.a, self.ext
        lo, hi = min(y1, y2), max(y1, y2)
        _sec_line(sc, x, lo, x, hi, _sec_pen(), 20)
        _sec_line(sc, x - e / 2, lo, x + e / 2, lo, _sec_pen(), 20)
        _sec_line(sc, x - e / 2, hi, x + e / 2, hi, _sec_pen(), 20)
        self._arrow([(x, lo), (x - a / 3, lo + a), (x + a / 3, lo + a)])
        self._arrow([(x, hi), (x - a / 3, hi - a), (x + a / 3, hi - a)])
        _sec_text(sc, text, x, (lo + hi) / 2.0, "left" if left else "right", shift)


def _sec_fail_pen():
    p = _sec_pen(2.0, _SEC_COL_FAIL, Qt.DashLine)
    p.setDashPattern([4.0, 3.0])
    return p


# ------------------------------------------------------------------ data
def _sec_conn(dialog):
    for attr in ("connection", "main"):
        c = getattr(getattr(dialog, attr, None), "connectivity", "")
        if c:
            return c
    return ""


class _SecDesign:
    """Design numbers (mm).  Uses the dialog's own _get_section_capacity_params() when available."""

    def __init__(self, dialog):
        p = dialog.params
        helper = getattr(dialog, "_get_section_capacity_params", None)
        if callable(helper):
            self.pitch, self.end, self.edge, self.gauge, rows, _cols, self.total = [_sec_f(v) for v in helper()]
            self.rows = max(2, int(rows))
        else:
            self.pitch, self.end, self.edge = _sec_f(p.get("pitch")), _sec_f(p.get("end")), _sec_f(p.get("edge"))
            self.gauge, self.rows = _sec_f(p.get("gauge1")), max(2, int(_sec_f(p.get("rows"), 2)))
            self.total = 2 * self.end + (self.rows - 1) * self.pitch
        self.bolt_d = _sec_f(p.get("hole")) or 16.0
        self.cleat_t = _sec_f(getattr(dialog, "angle_thickness", 0))


# ------------------------------------------------------------------ one diagram
def _sec_draw(dialog, scene, kind):
    """kind: 'main' (dashed rectangle through the bolts) | 'blockshear' (L-shaped path on each plate)."""
    des = _SecDesign(dialog)
    if des.total <= 0 or des.edge <= 0 or des.end <= 0:
        return False
    conn = _sec_conn(dialog)
    bb = conn == _SEC_BB
    scene.clear()

    s = _SEC_H_UNITS / des.total                          # px per mm
    H = _SEC_H_UNITS
    TW = _SEC_TW_OVER_H * H
    TC = _SEC_STRIP_OVER_H * H                            # thin cleat-leg strip beside the web (reference ratio)
    d_px = des.bolt_d * s
    r_hex = 0.42 * d_px
    # one plate, measured from the web face: gauge (= leg width, as in the branch drawing); 2 x edge if gauge is missing
    plate_w = (des.gauge if des.gauge > des.edge else 2.0 * des.edge) * s
    plate_w = max(plate_w, des.edge * s + TC + 1.3 * r_hex)       # keep the bolt clear of the web
    plate_mm = plate_w / s
    P = 2.0 * plate_w + TW                           # overall plate width
    B = _SEC_FLANGE_OVER_PLATES * P                       # beam flange: LONGER than the plates (as in the reference)
    TF = (_SEC_PRIMARY_TF_OVER_D * _SEC_D_OVER_H * H) if bb else _SEC_TF_OVER_H * H      # BB: as thick as the primary beam flange band
    D = _SEC_D_OVER_H * H
    gap_top = (_SEC_GAP_TOP_BB if bb else _SEC_GAP_TOP_CWBW) * H
    cx = 0.0
    web_l, web_r = cx - TW / 2.0, cx + TW / 2.0
    line = _sec_pen(1.0)

    # ---- primary member + position of the beam
    if bb:
        mw, mh = _SEC_PRIMARY_W_OVER_B * B, _SEC_PRIMARY_D_OVER_D * D
        bt = 1.45 * H                                # room above for two dimension rows
        mt = bt
        ptf = _SEC_PRIMARY_TF_OVER_D * D
        _sec_rect(scene, cx - mw / 2, mt, cx + mw / 2, mt + mh, _SEC_COL_COLUMN, line, 0)
        _sec_line(scene, cx - mw / 2, mt + ptf, cx + mw / 2, mt + ptf, line, 1)
        _sec_line(scene, cx - mw / 2, mt + mh - ptf, cx + mw / 2, mt + mh - ptf, line, 1)
        x0, x1, y0, y1 = cx - mw / 2 - 0.1 * H, cx + mw / 2 + 0.1 * H, 0.0, mt + mh + 0.2 * H
    else:
        mw, mh = _SEC_COLUMN_W_OVER_B * B, _SEC_COLUMN_H_OVER_D * D
        bt = (mh - D) / 2.0
        _sec_rect(scene, cx - mw / 2, 0, cx + mw / 2, mh, _SEC_COL_COLUMN, line, 0)
        sw = _SEC_COLUMN_STRIP * mw                       # column flanges, edge-on
        _sec_line(scene, cx - mw / 2 + sw, 0, cx - mw / 2 + sw, mh, line, 1)
        _sec_line(scene, cx + mw / 2 - sw, 0, cx + mw / 2 - sw, mh, line, 1)
        x0, x1, y0, y1 = cx - mw / 2 - 0.1 * H, cx + mw / 2 + 0.1 * H, -0.1 * H, mh + 0.1 * H

    # ---- secondary beam: flanges (back), web + joint patches are drawn later (front of the failure pattern)
    _sec_rect(scene, cx - B / 2, bt, cx + B / 2, bt + TF, _SEC_COL_BEAM, line, 2)
    _sec_rect(scene, cx - B / 2, bt + D - TF, cx + B / 2, bt + D, _SEC_COL_BEAM, line, 2)

    # ---- cleat plates
    plate_top = bt + TF + gap_top
    plate_bot = plate_top + H
    _sec_rect(scene, web_l - plate_w, plate_top, web_l, plate_bot, _SEC_COL_PLATE, line, 3)
    _sec_rect(scene, web_r, plate_top, web_r + plate_w, plate_bot, _SEC_COL_PLATE, line, 3)

    # ---- bolt geometry
    ys = [plate_top + (des.end + k * des.pitch) * s for k in range(des.rows)]
    y_top, y_bot = ys[0], ys[-1]
    xl, xr = web_l - plate_w + des.edge * s, web_r + plate_w - des.edge * s       # edge from the outer plate edge

    # ---- failure pattern: ABOVE the plates, BEHIND web / strips / bolts
    fp = _sec_fail_pen()
    if kind == "main":
        _sec_line(scene, xl, y_top, xr, y_top, fp, 4)
        _sec_line(scene, xl, y_bot, xr, y_bot, fp, 4)
        _sec_line(scene, xl, y_top, xl, y_bot, fp, 4)
        _sec_line(scene, xr, y_top, xr, y_bot, fp, 4)
    else:
        _sec_line(scene, xl, plate_top, xl, y_bot, fp, 4)           # plate top -> lowest bolt
        _sec_line(scene, xl, y_bot, web_l, y_bot, fp, 4)            # lowest bolt -> web
        _sec_line(scene, xr, plate_top, xr, y_bot, fp, 4)
        _sec_line(scene, web_r, y_bot, xr, y_bot, fp, 4)

    # ---- web (front of the failure pattern) + joint patches
    _sec_rect(scene, web_l, bt + TF, web_r, bt + D - TF, _SEC_COL_BEAM, line, 5)
    for yy in (bt + TF, bt + D - TF):
        _sec_rect(scene, web_l + 1.5, yy - 1.5, web_r - 1.5, yy + 1.5, _SEC_COL_BEAM, None, 5.5)
    # cleat-leg strips: the small rectangle around the web, full plate height
    _sec_rect(scene, web_l - TC, plate_top, web_l, plate_bot, _SEC_COL_PLATE, line, 5)
    _sec_rect(scene, web_r, plate_top, web_r + TC, plate_bot, _SEC_COL_PLATE, line, 5)

    # ---- bolts (front): hexagon heads + head / nut / shank side parts seated against the strips
    avail = max((plate_w - des.edge * s) - TC - r_hex, 4.0)
    hw, nw, sw_ = min(0.45 * d_px, 0.4 * avail), min(0.5 * d_px, 0.35 * avail), min(0.5 * d_px, 0.25 * avail)
    hh = 0.4 * d_px
    for y in ys:
        _sec_hexagon(scene, xl, y, r_hex, 6)
        _sec_hexagon(scene, xr, y, r_hex, 6)
        _sec_rect(scene, web_l - TC - hw, y - hh, web_l - TC, y + hh, _SEC_COL_BOLT, _sec_pen(1.0), 6)               # head
        _sec_rect(scene, web_r + TC, y - hh, web_r + TC + nw, y + hh, _SEC_COL_BOLT, _sec_pen(1.0), 6)               # nut
        _sec_rect(scene, web_r + TC + nw, y - 0.2 * d_px, web_r + TC + nw + sw_, y + 0.2 * d_px,
              _SEC_COL_BOLT, _sec_pen(1.0), 6)                                                                   # shank

    # ---- dimensions: every number comes from the design (nothing hard-coded)
    dm = _SecDims(scene, H)
    left_x, right_x = web_l - plate_w - 0.18 * H, web_r + plate_w + 0.18 * H
    top_row = bt - 0.30 * H
    bottom_row = bt + D + 0.30 * H
    k = _sec_planned_k(dialog, x1 - x0, y1 - y0)
    fmt = (lambda v: f"{v:.1f}") if kind == "main" else (lambda v: f"{v:.0f}")
    segs = [(plate_top, y_top, des.end)] + [(ya, yb, des.pitch) for ya, yb in zip(ys, ys[1:])] + [(y_bot, plate_bot, des.end)]
    crowded = min(abs(b_ - a_) for a_, b_, _v in segs) * k < _SEC_TEXT_PX + 4      # many rows: alternate the labels sideways
    for i, (ya, yb, val) in enumerate(segs):
        dm.v(right_x, ya, yb, fmt(val), shift=(34 if (crowded and i % 2) else 0))
    dm.v(left_x, plate_top, plate_bot, fmt(des.total), left=True)
    step = (_SEC_TEXT_PX + 10) / k

    def h_row(items, y, above):
        """Horizontal dimensions on one row; neighbours whose numbers would touch alternate between two rows."""
        centres = [(a_ + b_) / 2.0 for a_, b_, _t in items]
        wmax = max(0.62 * _SEC_TEXT_PX * len(t_) + 6 for _a, _b, t_ in items)
        tight = any(abs(c2 - c1) * k < wmax for c1, c2 in zip(centres, centres[1:]))
        for i, (a_, b_, t_) in enumerate(items):
            off = step if (tight and i % 2) else 0.0
            dm.h(a_, b_, y - off if above else y + off, t_, above=above)

    if kind == "main":
        if des.gauge > 0:                                            # top: gauge | gauge (as in the branch drawing)
            h_row([(web_l - plate_w, web_l, fmt(des.gauge)), (web_r, web_r + plate_w, fmt(des.gauge))], top_row, True)
        if des.edge > 0:                                             # bottom: edge (outer plate edge -> bolt), both plates
            h_row([(web_l - plate_w, xl, fmt(des.edge)), (xr, web_r + plate_w, fmt(des.edge))], bottom_row, False)
    else:
        dm.h(web_r, web_r + plate_w, top_row, fmt(plate_mm))         # plate width (real value; was a hard-coded 262)
        dm.h(xr, web_r + plate_w, top_row - 0.45 * H, fmt(des.edge))

    scene.setSceneRect(x0, y0, x1 - x0, y1 - y0)
    sheet = _sec_rect(scene, x0, y0, x1, y1, _SEC_COL_BEAM, None, -10)          # white sheet: readable in both themes
    sheet.setData(0, "backdrop")
    return True


def _sec_planned_k(dialog, w, h):
    """On-screen scale (px per scene unit) the popup view will get for a drawing of w x h scene units."""
    try:
        ww, wh = dialog._section_window_size()
    except Exception:                                # noqa: BLE001
        ww, wh = 980, 620
    vw = max(620.0, ww - 430.0)
    vh = (wh - 200.0) / 2.0 if getattr(dialog, "show_third", False) else wh - 150.0
    return max(0.01, min(vw / w, vh / h))


# ------------------------------------------------------------------ public hooks
def _sec_applies(dialog):
    return (type(dialog).__name__ == "CleatAngleSectionDetails"
            and _sec_conn(dialog) in (_SEC_CWBW, _SEC_BB))


def _sec_try_main(dialog, scene):
    """Diagram 'Failure Pattern in Section' (CWBW, Beam-Beam).  False -> caller keeps the legacy drawing."""
    if not _sec_applies(dialog):
        return False
    try:
        return _sec_draw(dialog, scene, "main")
    except Exception as exc:                          # noqa: BLE001 - never break the popup
        print("[WARN] cleat section diagram failed, using legacy drawing:", exc)
        scene.clear()
        return False


def _sec_try_blockshear(dialog, scene):
    """Beam-Beam only: diagram 'Failure Pattern due to Block Shear in Section'."""
    if not _sec_applies(dialog) or _sec_conn(dialog) != _SEC_BB:
        return False
    try:
        return _sec_draw(dialog, scene, "blockshear")
    except Exception as exc:                          # noqa: BLE001
        print("[WARN] cleat block-shear diagram failed, using legacy drawing:", exc)
        scene.clear()
        return False


class CleatAngleSectionDetails(CleatAngleCapacityDetails):
    """
    Section capacity popup:
    - left side: section capacity values in 2 text groups
    - right side: only ONE image
    """

    def __init__(self, connection_obj, rows=3, cols=2, main=None):
        if isinstance(main, tuple):
            # To show another failure pattern when connectivity is Beam-Beam
            self.show_third = main[2] if len(main) > 2 else False
            super().__init__(connection_obj, rows, cols, (main[0], main[1]))
        else:
            # To show another failure pattern when connectivity is Beam-Beam
            self.show_third = False
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

    def _section_window_size(self):
        """Popup size: big enough to show the whole diagram without scrolling (limited by the screen)."""
        g = QApplication.primaryScreen().availableGeometry()
        conn = getattr(self.connection, 'connectivity', '')
        if conn == _SEC_BB:                      # wide drawing; two stacked diagrams when block shear is shown
            return min(g.width() - 60, 1500), min(g.height() - 60, 980 if self.show_third else 700)
        if conn == _SEC_CWBW:                    # tall drawing (column)
            return min(g.width() - 60, 980), min(g.height() - 60, 1000)
        return 980, 620

    def _section_view_height(self, scene):
        """Height of a diagram view: follows the drawing's aspect ratio, never taller than the popup allows."""
        sr = scene.sceneRect()
        ww, wh = self._section_window_size()
        if sr.width() <= 0:
            return 520
        vw = max(620, ww - 430)
        cap = (wh - 200) // 2 if self.show_third else wh - 150
        return int(max(200, min(vw * sr.height() / sr.width(), cap)))

    def initUI(self):
        self.setupWrapper()

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = self._section_window_size()
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
        self.view1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.createSectionDrawing(self.scene1)
        self.view1.setMinimumHeight(self._section_view_height(self.scene1))
        self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
        right_layout.addWidget(self.view1)

        # To show another failure pattern when connectivity is Beam-Beam
        if self.show_third:
            title3 = QLabel("Failure Pattern due to Block Shear in Section:")
            title3.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
            right_layout.addWidget(title3)

            self.scene3 = QGraphicsScene()
            self.view3 = QGraphicsView(self.scene3)
            self.view3.setBackgroundBrush(
                QBrush(Qt.white) if self.theme.is_light()
                else QBrush(QColor("#4A4A4A"))
            )
            self.view3.setRenderHint(QPainter.Antialiasing)
            self.view3.setMinimumWidth(620)
            self.view3.setMinimumHeight(520)
            self.view3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.view3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.createSecondDrawing(self.scene3)
            self.view3.setMinimumHeight(self._section_view_height(self.scene3))
            self.view3.fitInView(self.scene3.sceneRect(), Qt.KeepAspectRatio)
            right_layout.addWidget(self.view3)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        scroll_area.setWidget(scroll)
        content_layout.addWidget(scroll_area)
    
    # To show another failure pattern when connectivity is Beam-Beam
    def createSecondDrawing(self, scene):
        self._draw_section_block_shear_pattern(scene)

    def _draw_section_block_shear_pattern(self, scene):
        # Beam-Beam diagram #2: same geometry, previous (L-shaped) failure pattern
        if _sec_try_blockshear(self, scene):
            return
        scene.clear()

        if self.theme.is_light():
            plate_pen   = QPen(QColor("#444444"), 2)
            dim_pen     = QPen(Qt.black, 1)
            dash_pen    = QPen(QColor("#E8A000"), 2.5, Qt.DashLine)
            plate_brush = QBrush(QColor("#F8F8F8"))
            weld_brush  = QBrush(QColor("#9A9A9A"))
            weld_pen    = QPen(QColor("#777777"), 1)
        else:
            plate_pen   = QPen(QColor("#DADADA"), 2)
            dim_pen     = QPen(QColor("#E0E0E0"), 1)
            dash_pen    = QPen(QColor("#E8A000"), 2.5, Qt.DashLine)
            plate_brush = QBrush(QColor("#505050"))
            weld_brush  = QBrush(QColor("#808080"))
            weld_pen    = QPen(QColor("#909090"), 1)

        scene.setSceneRect(-140, -100, 700, 800)

        pitch = float(self.params.get("pitch", 0))
        end   = float(self.params.get("end", 0))
        edge  = float(self.params.get("edge", 0))
        gauge = float(self.params.get("gauge1", 0))

        # Single plate geometry
        plate_x = 80
        plate_y = 80
        plate_w = 280
        plate_h = 420
        weld_w  = 18

        # Scale factor: map real dimensions to scene pixels
        # plate_h in scene = total real height = 2*end + pitch (if only 2 bolts)
        total_real_h = 2 * end + pitch
        scale = plate_h / total_real_h if total_real_h > 0 else 1.0

        # plate_w (excluding weld strip) maps to real width
        # real width = edge (from weld face to bolt column)
        # bolt_x is measured from the RIGHT of the weld strip
        bolt_x = plate_x + weld_w + edge * scale   # edge from weld face (left side)
        top_bolt_y = plate_y + end * scale
        bot_bolt_y = plate_y + (end + pitch) * scale

        bolt_r = 13

        # Plate
        scene.addRect(plate_x, plate_y, plate_w, plate_h, plate_pen, plate_brush)
        # Weld strip on left
        scene.addRect(plate_x, plate_y, weld_w, plate_h, weld_pen, weld_brush)

        # Bolts
        self.draw_blue_bolt(scene, bolt_x, top_bolt_y, bolt_r)
        self.draw_blue_bolt(scene, bolt_x, bot_bolt_y, bolt_r)

        # L-shape fracture path:
        # vertical: top of plate → bottom bolt
        scene.addLine(bolt_x, plate_y,      bolt_x,        bot_bolt_y, dash_pen)
        # horizontal: bottom bolt → weld face (right edge of weld strip)
        scene.addLine(plate_x + weld_w, bot_bolt_y, bolt_x, bot_bolt_y, dash_pen)

        # ── Dimensions ──────────────────────────────────────────────
        right_dim_x = plate_x + plate_w + 40
        left_dim_x  = plate_x - 60
        top_dim_y   = plate_y - 40

        # Right side vertical dims: end | pitch | end
        if end > 0:
            self.add_v_dim(scene, right_dim_x, plate_y,      top_bolt_y,            f"{end:.0f}",   dim_pen)
        if pitch > 0:
            self.add_v_dim(scene, right_dim_x, top_bolt_y,   bot_bolt_y,            f"{pitch:.0f}", dim_pen)
        if end > 0:
            self.add_v_dim(scene, right_dim_x, bot_bolt_y,   plate_y + plate_h,     f"{end:.0f}",   dim_pen)

        # Left side vertical dim: total plate height label
        if total_real_h > 0:
            self.add_v_dim(scene, left_dim_x, plate_y, plate_y + plate_h, f"{total_real_h:.0f}", dim_pen)

        # Top horizontal dim: full plate width (weld face to right edge)
        plate_real_w = plate_w - weld_w  # or use a real width param if available
        if edge > 0:
            self.add_h_dim(scene, plate_x + weld_w, plate_x + plate_w, top_dim_y, f"{plate_real_w:.0f}", dim_pen)

        # Edge dim: weld face to bolt column (shown at top or between dims)
        if edge > 0:
            self.add_h_dim(scene, plate_x + weld_w, bolt_x, top_dim_y - 30, f"{edge:.0f}", dim_pen)

    def createSectionDrawing(self, scene):
        # CWBW / Beam-Beam diagram #1: measured-proportion drawing; anything else -> code below
        if _sec_try_main(self, scene):
            return
        connectivity = getattr(self.connection, 'connectivity', '')
        if connectivity == 'Beam-Beam':
            self._draw_section_bb(scene)
        else:
            self._draw_section_cwbw(scene)

    def _get_section_capacity_params(self):
        pitch = float(self.params.get("pitch", 0))
        end = float(self.params.get("end", 0))
        edge = float(self.params.get("edge", 0))
        gauge = float(self.params.get("gauge1", 0) or self.params.get("gauge", 0))
        rows = int(self.params.get("rows", 0))
        cols = int(self.params.get("cols", 1))

        sptd = getattr(self.connection, 'sptd_leg', None)
        spting = getattr(self.connection, 'spting_leg', None)
        if pitch == 0:
            pitch = float(getattr(sptd, 'pitch_provided', 0) or getattr(spting, 'pitch_provided', 0) or 0)
        if end == 0:
            end = float(getattr(sptd, 'end_dist_provided', 0) or getattr(spting, 'end_dist_provided', 0) or 0)
        if edge == 0:
            edge = float(getattr(sptd, 'edge_dist_provided', 0) or getattr(spting, 'edge_dist_provided', 0) or 0)
        if gauge == 0:
            gauge = float(getattr(sptd, 'gauge_provided', 0) or getattr(spting, 'gauge_provided', 0) or 0)
        if rows <= 0:
            rows = int(getattr(sptd, 'bolts_one_line', 0) or getattr(spting, 'bolts_one_line', 0) or 2)
        if cols <= 0:
            cols = int(getattr(sptd, 'bolt_line', 0) or getattr(spting, 'bolt_line', 0) or 1)

        rows = max(2, min(rows, 6))
        cols = max(1, min(cols, 4))

        total_height = (2.0 * end + (rows - 1) * pitch) if (end > 0 and pitch > 0) else float(self.params.get("width", 0))
        if total_height <= 0 and end > 0:
            total_height = 2.0 * end + (rows - 1) * 40.0

        return pitch, end, edge, gauge, rows, cols, total_height

    def _draw_h_dimension(self, scene, x1, x2, y, text, ext_y1=None, ext_y2=None, text_above=True):
        if abs(x2 - x1) < 2:
            return
        dim_pen = QPen(Qt.black, 1)
        ext_pen = QPen(QColor("#777777"), 1)

        if ext_y1 is not None:
            min_y = min(ext_y1, y)
            max_y = max(ext_y1, y)
            overshoot = 4 if text_above else -4
            scene.addLine(x1, min_y, x1, max_y + overshoot, ext_pen)
        if ext_y2 is not None:
            min_y = min(ext_y2, y)
            max_y = max(ext_y2, y)
            overshoot = 4 if text_above else -4
            scene.addLine(x2, min_y, x2, max_y + overshoot, ext_pen)

        scene.addLine(x1, y, x2, y, dim_pen)

        arrow = 6
        pts_l = [QPointF(x1, y), QPointF(x1 + arrow, y - arrow / 2), QPointF(x1 + arrow, y + arrow / 2)]
        pts_r = [QPointF(x2, y), QPointF(x2 - arrow, y - arrow / 2), QPointF(x2 - arrow, y + arrow / 2)]
        for pts in (pts_l, pts_r):
            poly = scene.addPolygon(QPolygonF(pts), dim_pen)
            poly.setBrush(QBrush(Qt.black))

        t = scene.addText(str(text))
        f = QFont()
        f.setPointSize(10)
        f.setBold(True)
        t.setFont(f)
        t.setDefaultTextColor(Qt.black)
        tw = t.boundingRect().width()
        th = t.boundingRect().height()
        tx = (x1 + x2) / 2.0 - tw / 2.0
        ty = y - th - 3 if text_above else y + 4
        t.setPos(tx, ty)

    def _draw_v_dimension(self, scene, y1, y2, x, text, ext_x1=None, ext_x2=None, text_right=True, x_offset=0):
        if abs(y2 - y1) < 2:
            return
        dim_pen = QPen(Qt.black, 1)
        ext_pen = QPen(QColor("#777777"), 1)

        if ext_x1 is not None:
            min_x = min(ext_x1, x)
            max_x = max(ext_x1, x)
            overshoot = 4 if text_right else -4
            scene.addLine(min_x, y1, max_x + overshoot, y1, ext_pen)
        if ext_x2 is not None:
            min_x = min(ext_x2, x)
            max_x = max(ext_x2, x)
            overshoot = 4 if text_right else -4
            scene.addLine(min_x, y2, max_x + overshoot, y2, ext_pen)

        scene.addLine(x, y1, x, y2, dim_pen)

        arrow = 6
        if y2 > y1:
            pts_top = [QPointF(x, y1), QPointF(x - arrow / 2, y1 + arrow), QPointF(x + arrow / 2, y1 + arrow)]
            pts_bot = [QPointF(x, y2), QPointF(x - arrow / 2, y2 - arrow), QPointF(x + arrow / 2, y2 - arrow)]
        else:
            pts_top = [QPointF(x, y2), QPointF(x - arrow / 2, y2 + arrow), QPointF(x + arrow / 2, y2 + arrow)]
            pts_bot = [QPointF(x, y1), QPointF(x - arrow / 2, y1 - arrow), QPointF(x + arrow / 2, y1 - arrow)]
        for pts in (pts_top, pts_bot):
            poly = scene.addPolygon(QPolygonF(pts), dim_pen)
            poly.setBrush(QBrush(Qt.black))

        t = scene.addText(str(text))
        f = QFont()
        f.setPointSize(10)
        f.setBold(True)
        t.setFont(f)
        t.setDefaultTextColor(Qt.black)
        tw = t.boundingRect().width()
        th = t.boundingRect().height()
        ty = (y1 + y2) / 2.0 - th / 2.0
        tx = x + 6 + x_offset if text_right else x - tw - 6 - x_offset
        t.setPos(tx, ty)

    def _draw_section_cwbw(self, scene):
        scene.clear()

        struct_pen = QPen(QColor("#333333"), 2)
        plate_pen = QPen(QColor("#333333"), 2)
        dash_pen = QPen(Qt.black, 1.5, Qt.DashLine)
        col_brush = QBrush(QColor("#f4f4e3"))   # Cream column matching Image 1
        beam_brush = QBrush(Qt.white)           # White beam cross section matching Image 1
        plate_brush = QBrush(QColor("#dbdbce")) # Grey cleat angle matching Image 1
        bolt_brush = QBrush(QColor("#ff0d0d"))  # Red bolt matching Image 1
        bolt_pen = QPen(QColor("#550000"), 1.5)

        scene.setSceneRect(-60, -20, 920, 940)
        cx = 400
        cy = 450

        pitch, end, edge, gauge, rows, cols, total_height = self._get_section_capacity_params()

        # ── Column (vertical member, cream with left/right flange lines) ──
        col_w = 340
        col_h = 860
        col_top = cy - col_h / 2
        col_bot = cy + col_h / 2
        col_tf = 16

        scene.addRect(cx - col_w / 2, col_top, col_w, col_h, struct_pen, col_brush)
        scene.addLine(cx - col_w / 2 + col_tf, col_top, cx - col_w / 2 + col_tf, col_bot, struct_pen)
        scene.addLine(cx + col_w / 2 - col_tf, col_top, cx + col_w / 2 - col_tf, col_bot, struct_pen)

        # ── Supported Beam in Center (I-section in white) ──
        beam_d = 200
        beam_bf = 190
        beam_tf = 14
        beam_tw = 12

        # Top flange
        scene.addRect(cx - beam_bf / 2, cy - beam_d / 2, beam_bf, beam_tf, struct_pen, beam_brush)
        # Bottom flange
        scene.addRect(cx - beam_bf / 2, cy + beam_d / 2 - beam_tf, beam_bf, beam_tf, struct_pen, beam_brush)
        # Web
        scene.addRect(cx - beam_tw / 2, cy - beam_d / 2 + beam_tf, beam_tw, beam_d - 2 * beam_tf, struct_pen, beam_brush)

        # ── Cleat Angles (grey rectangles on left and right of beam web) ──
        cleat_h = 130
        cleat_top = cy - cleat_h / 2
        cleat_bot = cy + cleat_h / 2
        cleat_w = 60

        left_cleat_x = cx - beam_tw / 2 - cleat_w
        right_cleat_x = cx + beam_tw / 2

        scene.addRect(left_cleat_x, cleat_top, cleat_w, cleat_h, plate_pen, plate_brush)
        scene.addRect(right_cleat_x, cleat_top, cleat_w, cleat_h, plate_pen, plate_brush)

        # ── Bolts ──
        if total_height > 0 and end > 0 and pitch > 0:
            bolt_ys = [cleat_top + cleat_h * (end + k * pitch) / total_height for k in range(rows)]
        else:
            step = cleat_h / (rows + 1)
            bolt_ys = [cleat_top + (k + 1) * step for k in range(rows)]

        left_bolt_x = left_cleat_x + cleat_w * 0.45
        right_bolt_x = right_cleat_x + cleat_w * 0.55
        bolt_r = 11

        for by in bolt_ys:
            for bx in (left_bolt_x, right_bolt_x):
                scene.addEllipse(bx - bolt_r / 2, by - bolt_r / 2, bolt_r, bolt_r, bolt_pen, bolt_brush)
                scene.addEllipse(bx - 3, by - 3, 6, 6, QPen(Qt.transparent), QBrush(QColor("#ff8888")))

        # ── Failure Pattern (dashed rectangle) ──
        scene.addLine(left_bolt_x, bolt_ys[0], right_bolt_x, bolt_ys[0], dash_pen)
        scene.addLine(left_bolt_x, bolt_ys[-1], right_bolt_x, bolt_ys[-1], dash_pen)
        scene.addLine(left_bolt_x, bolt_ys[0], left_bolt_x, bolt_ys[-1], dash_pen)
        scene.addLine(right_bolt_x, bolt_ys[0], right_bolt_x, bolt_ys[-1], dash_pen)

        # ── Dimensions (Zero overlap with structure and each other) ──
        beam_left_x = cx - beam_bf / 2
        beam_right_x = cx + beam_bf / 2
        beam_top_y = cy - beam_d / 2
        beam_bot_y = cy + beam_d / 2

        # Left: Total Height (placed well left of column)
        dim_left_x = 130
        if total_height > 0:
            self._draw_v_dimension(scene, cleat_top, cleat_bot, dim_left_x, f"{total_height:.1f}",
                                   ext_x1=beam_left_x, ext_x2=beam_left_x, text_right=False)

        # Right: End, Pitch..., End (placed well right of column)
        dim_right_x = 670
        if end > 0:
            self._draw_v_dimension(scene, cleat_top, bolt_ys[0], dim_right_x, f"{end:.1f}",
                                   ext_x1=beam_right_x, ext_x2=beam_right_x, text_right=True)
        for k in range(rows - 1):
            if pitch > 0:
                self._draw_v_dimension(scene, bolt_ys[k], bolt_ys[k + 1], dim_right_x, f"{pitch:.1f}",
                                       ext_x1=beam_right_x, ext_x2=beam_right_x, text_right=True)
        if end > 0:
            self._draw_v_dimension(scene, bolt_ys[-1], cleat_bot, dim_right_x, f"{end:.1f}",
                                   ext_x1=beam_right_x, ext_x2=beam_right_x, text_right=True)

        # Top: Gauge / Leg width (well above beam top flange)
        dim_top_y = 280
        if gauge > 0:
            self._draw_h_dimension(scene, left_cleat_x, cx - beam_tw / 2, dim_top_y, f"{gauge:.1f}",
                                   ext_y1=beam_top_y, ext_y2=beam_top_y, text_above=True)
            self._draw_h_dimension(scene, cx + beam_tw / 2, right_cleat_x + cleat_w, dim_top_y, f"{gauge:.1f}",
                                   ext_y1=beam_top_y, ext_y2=beam_top_y, text_above=True)

        # Bottom: Edge distance (well below beam bottom flange)
        dim_bot_y = 620
        if edge > 0:
            self._draw_h_dimension(scene, left_cleat_x, left_bolt_x, dim_bot_y, f"{edge:.1f}",
                                   ext_y1=beam_bot_y, ext_y2=beam_bot_y, text_above=False)
            self._draw_h_dimension(scene, right_bolt_x, right_cleat_x + cleat_w, dim_bot_y, f"{edge:.1f}",
                                   ext_y1=beam_bot_y, ext_y2=beam_bot_y, text_above=False)

    def _draw_section_bb(self, scene):
        scene.clear()

        struct_pen = QPen(QColor("#333333"), 2)
        plate_pen = QPen(QColor("#333333"), 2)
        dash_pen = QPen(Qt.black, 1.5, Qt.DashLine)
        col_brush = QBrush(QColor("#f4f4e3"))   # Cream supporting girder matching Image 2
        beam_brush = QBrush(Qt.white)           # White beam cross section matching Image 2
        plate_brush = QBrush(QColor("#dbdbce")) # Grey cleat angle matching Image 2
        bolt_brush = QBrush(QColor("#ff0d0d"))  # Red bolt matching Image 2
        bolt_pen = QPen(QColor("#550000"), 1.5)

        scene.setSceneRect(-40, -40, 1040, 540)
        cx = 480

        pitch, end, edge, gauge, rows, cols, total_height = self._get_section_capacity_params()

        # ── Supporting Girder (horizontal member, cream with top/bottom flange lines) ──
        s_left = 40
        s_right = 920
        s_w = s_right - s_left
        s_top = 80
        s_bot = 400
        s_h = s_bot - s_top
        s_tf = 16

        scene.addRect(s_left, s_top, s_w, s_h, struct_pen, col_brush)

        # ── Supported Beam in Center (flush at top, depth sup_d < s_h) ──
        sup_d = 200
        sup_bot = s_top + sup_d
        beam_bf = 190
        beam_tf = 14
        beam_tw = 12

        # Supporting girder flange inner lines (broken at supported beam top flange)
        scene.addLine(s_left, s_top + s_tf, cx - beam_bf / 2, s_top + s_tf, struct_pen)
        scene.addLine(cx + beam_bf / 2, s_top + s_tf, s_right, s_top + s_tf, struct_pen)
        scene.addLine(s_left, s_bot - s_tf, s_right, s_bot - s_tf, struct_pen)

        # Supported beam:
        # Top flange (flush at top!)
        scene.addRect(cx - beam_bf / 2, s_top, beam_bf, beam_tf, struct_pen, beam_brush)
        # Bottom flange
        scene.addRect(cx - beam_bf / 2, sup_bot - beam_tf, beam_bf, beam_tf, struct_pen, beam_brush)
        # Web
        scene.addRect(cx - beam_tw / 2, s_top + beam_tf, beam_tw, sup_d - 2 * beam_tf, struct_pen, beam_brush)

        # ── Cleat Angles ──
        cleat_h = 130
        cleat_y = s_top + beam_tf + (sup_d - 2 * beam_tf - cleat_h) / 2
        cleat_bot = cleat_y + cleat_h
        cleat_w = 60

        left_cleat_x = cx - beam_tw / 2 - cleat_w
        right_cleat_x = cx + beam_tw / 2

        scene.addRect(left_cleat_x, cleat_y, cleat_w, cleat_h, plate_pen, plate_brush)
        scene.addRect(right_cleat_x, cleat_y, cleat_w, cleat_h, plate_pen, plate_brush)

        # ── Bolts ──
        if total_height > 0 and end > 0 and pitch > 0:
            bolt_ys = [cleat_y + cleat_h * (end + k * pitch) / total_height for k in range(rows)]
        else:
            step = cleat_h / (rows + 1)
            bolt_ys = [cleat_y + (k + 1) * step for k in range(rows)]

        left_bolt_x = left_cleat_x + cleat_w * 0.45
        right_bolt_x = right_cleat_x + cleat_w * 0.55
        bolt_r = 11

        for by in bolt_ys:
            for bx in (left_bolt_x, right_bolt_x):
                scene.addEllipse(bx - bolt_r / 2, by - bolt_r / 2, bolt_r, bolt_r, bolt_pen, bolt_brush)
                scene.addEllipse(bx - 3, by - 3, 6, 6, QPen(Qt.transparent), QBrush(QColor("#ff8888")))

        # ── Failure Pattern ──
        scene.addLine(left_bolt_x, bolt_ys[0], right_bolt_x, bolt_ys[0], dash_pen)
        scene.addLine(left_bolt_x, bolt_ys[-1], right_bolt_x, bolt_ys[-1], dash_pen)
        scene.addLine(left_bolt_x, bolt_ys[0], left_bolt_x, bolt_ys[-1], dash_pen)
        scene.addLine(right_bolt_x, bolt_ys[0], right_bolt_x, bolt_ys[-1], dash_pen)

        # ── Dimensions (Zero overlap with structure and each other) ──
        beam_left_x = cx - beam_bf / 2
        beam_right_x = cx + beam_bf / 2

        # Left: Total Height (placed in open web zone to the left of supported beam)
        dim_left_x = beam_left_x - 50
        if total_height > 0:
            self._draw_v_dimension(scene, cleat_y, cleat_bot, dim_left_x, f"{total_height:.1f}",
                                   ext_x1=beam_left_x, ext_x2=beam_left_x, text_right=False)

        # Right: End, Pitch..., End (placed in open web zone to the right of supported beam)
        dim_right_x = beam_right_x + 50
        if end > 0:
            self._draw_v_dimension(scene, cleat_y, bolt_ys[0], dim_right_x, f"{end:.1f}",
                                   ext_x1=beam_right_x, ext_x2=beam_right_x, text_right=True)
        for k in range(rows - 1):
            if pitch > 0:
                self._draw_v_dimension(scene, bolt_ys[k], bolt_ys[k + 1], dim_right_x, f"{pitch:.1f}",
                                       ext_x1=beam_right_x, ext_x2=beam_right_x, text_right=True)
        if end > 0:
            self._draw_v_dimension(scene, bolt_ys[-1], cleat_bot, dim_right_x, f"{end:.1f}",
                                   ext_x1=beam_right_x, ext_x2=beam_right_x, text_right=True)

        # Top: Gauge / Leg width (above top flange)
        dim_top_y = s_top - 25
        if gauge > 0:
            self._draw_h_dimension(scene, left_cleat_x, cx - beam_tw / 2, dim_top_y, f"{gauge:.1f}",
                                   ext_y1=s_top, ext_y2=s_top, text_above=True)
            self._draw_h_dimension(scene, cx + beam_tw / 2, right_cleat_x + cleat_w, dim_top_y, f"{gauge:.1f}",
                                   ext_y1=s_top, ext_y2=s_top, text_above=True)

        # Bottom: Edge distance (between sup_bot and girder bottom flange)
        dim_bot_y = sup_bot + 35
        if edge > 0:
            self._draw_h_dimension(scene, left_cleat_x, left_bolt_x, dim_bot_y, f"{edge:.1f}",
                                   ext_y1=sup_bot, ext_y2=sup_bot, text_above=False)
            self._draw_h_dimension(scene, right_bolt_x, right_cleat_x + cleat_w, dim_bot_y, f"{edge:.1f}",
                                   ext_y1=sup_bot, ext_y2=sup_bot, text_above=False)

    # Legacy alias
    _draw_section_capacity_pattern = _draw_section_cwbw

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'view1'):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
        if hasattr(self, 'view3') and self.show_third:
            self.view3.fitInView(self.scene3.sceneRect(), Qt.KeepAspectRatio)