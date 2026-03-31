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