import sys
from PySide6.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
                             QGraphicsScene)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtGui import QPolygonF, QBrush
from PySide6.QtCore import QPointF
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *

class BoltPatternGenerator(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager

        self.connection = connection_obj
        self.main=main
        self.plate_height = main.plate.height
        self.plate_width = main.plate.length 
        self.hole_dia=main.bolt.bolt_diameter_provided
        self.rows=main.plate.bolts_one_line
        self.cols=main.plate.bolt_line
        print(self.plate_height,self.plate_width)
        output=main.output_values(True)
        dict1={i[0] : i[3] for i in output}
        for i in output:
            print(i)
        self.weldsize=0
        if 'Weld.Size' in dict1:
            self.weldsize=dict1['Weld.Size']
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
        
        # Center the window on the screen with the same dimensions
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = 800, 500
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel for parameter display
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Parameter display labels
        params = self.get_parameters()
        

        # Display the parameter values
        for key, value in params.items():
            param_layout = QHBoxLayout()
            param_label = QLabel(f'{key.title()} Distance :')
            param_label.setStyleSheet("font-size: 15px; font-weight: bold;")
            value_label = QLabel(f'{float(value):.2f}')
            value_label.setStyleSheet("font-size: 15px;")
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            left_layout.addLayout(param_layout)

        param_layout = QHBoxLayout()
        param_label = QLabel("(All Dimensions are in mm)")
        param_label.setStyleSheet("font-size: 12px; font-style: italic;")
        param_layout.addWidget(param_label)
        left_layout.addLayout(param_layout)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Right panel for the drawing using QGraphicsView
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        if self.theme.is_light():
            self.view.setBackgroundBrush(QBrush(Qt.white))
        else:
            self.view.setBackgroundBrush(QBrush(QColor("#4A4A4A")))
        # Create and add the drawing to the scene
        self.createDrawing(params)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.view, 3)
        
        self.content_widget.setLayout(main_layout)
        
        # Ensure the view shows all content
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
    def get_parameters(self):
        spacing_data = self.connection.spacing(status=True)  # Get actual values
        param_map = {}
        print('spacing_data length' , len(spacing_data))
        for item in spacing_data:
            key, _, _, value = item
            # print('key : ', key)
            if key == KEY_OUT_PITCH:  
                param_map['pitch'] = float(value)
            elif key == KEY_OUT_END_DIST:
                param_map['end'] = float(value)
            elif key == KEY_OUT_GAUGE1:
                param_map['gauge1'] = float(value)
            elif key == KEY_OUT_GAUGE2:
                param_map['gauge2'] = float(value)
            elif key == KEY_OUT_GAUGE:
                param_map['gauge'] = float(value)
            elif key == KEY_OUT_EDGE_DIST:
                param_map['edge'] = float(value)

        # Add hardcoded hole diameter
        param_map['hole'] = self.main.bolt.bolt_diameter_provided

        print("Extracted parameters:", param_map)

        return param_map

    def createDrawing(self, params):
        
        # Extract parameters
        pitch = params['pitch']
        end = params['end']
        if 'gauge' in params:
            gauge = params['gauge']
        else:
            gauge1 = params['gauge1']
            gauge2 = params['gauge2']
        edge = params['edge']
        hole_diameter = params['hole']
        
        # Calculate dimensions
        if 'gauge' in params:
            gauge1 = gauge
            gauge2 = gauge
        width = self.plate_width

        height = self.plate_height
        
        # Set up pens
        if self.theme.is_light():
            dimension_pen = QPen(Qt.black, 1.0)
        else:
            dimension_pen = QPen(QColor("#8A8A8A"), 1.0)
        weld_pen = QPen(Qt.red, 1)
        outline_pen = QPen(QColor("#723B17"), 2)
        red_brush = QBrush(Qt.red)

        # Dimension offsets
        h_offset = 40
        v_offset = 60
        
        # Create scene rectangle with extra space for dimensions
        self.scene.setSceneRect(-h_offset, -v_offset, 
                               width + 2*v_offset, height + 2*h_offset)
        
        # Draw rectangle
        background_brush = QBrush(QColor("#A7A796"))
        self.scene.addRect(0, 0, width, height, dimension_pen, background_brush)

        # Draw holes
        for row in range(self.rows):
            for col in range(self.cols):
                # Start from right edge (for example: total plate width - edge)
                x_center = self.plate_width - edge

                # Subtract gauges from right to left
                for i in range(col):
                    x_center -= gauge1 if i % 2 == 0 else gauge2

                # Y-position stays the same
                y_center = end + row * pitch

                # Top-left corner for drawing the circle
                x = x_center - hole_diameter / 2
                y = y_center - hole_diameter / 2

                print(f"row: {row}, col: {col}, x: {x}, y: {y}")
                self.scene.addEllipse(x, y, hole_diameter, hole_diameter, outline_pen)
        weld_size=self.weldsize
        self.scene.addRect(0, 0, weld_size, height, weld_pen,red_brush)
        print(params,dimension_pen)
        # Add dimensions
        self.addDimensions(params, dimension_pen)

    def addDimensions(self, params, pen):
        # Extract parameters
        pitch = params['pitch']
        end = params['end']
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
        
        # Offsets for dimension lines
        h_offset = 15
        v_offset = 10
        
        # Add horizontal dimensions
        x_start = width
        segments = []
        # First edge
        segments.append(('edge', x_start-edge, x_start ))
        x_start -=edge
       
        # Last edge
        segments.append(('edge', 0, x_start))

        # Draw each segment
        for label, x1, x2 in segments:
            value = x2 - x1
            self.addHorizontalDimension(x1, -h_offset + 5, x2, -h_offset + 5, f"{value:.1f}", pen)
        # Add vertical dimensions
        self.addVerticalDimension(width + v_offset, 0, width + v_offset, end, str(end), pen)
        for i in range(self.rows - 1):
            self.addVerticalDimension(width + v_offset, end + i * pitch, width + v_offset, end + (i + 1) * pitch, str(pitch), pen)
        
        # Add bottom end distance dimension
        self.addVerticalDimension(width + v_offset, height, width + v_offset, height - end, str(end), pen)
        
        # Add left side dimension
        total_height = 2 * end + (self.rows - 1) * pitch
        self.addVerticalDimension(-v_offset, 0, -v_offset, total_height, str(total_height), pen)

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 3
        ext_length = 10
        self.scene.addLine(x1, y1 - ext_length/2, x1, y1 + ext_length/2, pen)
        self.scene.addLine(x2, y2 - ext_length/2, x2, y2 + ext_length/2, pen)
        
        points_left = [
            (x1, y1),
            (x1 + arrow_size, y1 - arrow_size/2),
            (x1 + arrow_size, y1 + arrow_size/2)
        ]
        polygon_left = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_left]), pen)
        if self.theme.is_light():
            polygon_left.setBrush(QBrush(Qt.black))
        else:
            polygon_left.setBrush(QBrush(QColor("#8A8A8A")))
        
        points_right = [
            (x2, y2),
            (x2 - arrow_size, y2 - arrow_size/2),
            (x2 - arrow_size, y2 + arrow_size/2)
        ]
        polygon_right = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_right]), pen)
        if self.theme.is_light():
            polygon_left.setBrush(QBrush(Qt.black))
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
        
        if y1 < 0:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 15)
        else:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 15)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 3
        ext_length = 10
        self.scene.addLine(x1 - ext_length/2, y1, x1 + ext_length/2, y1, pen)
        self.scene.addLine(x2 - ext_length/2, y2, x2 + ext_length/2, y2, pen)
        
        if y2 > y1:
            points_top = [
                (x1, y1),
                (x1 - arrow_size/2, y1 + arrow_size),
                (x1 + arrow_size/2, y1 + arrow_size)
            ]
            polygon_top = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
            if self.theme.is_light():
                polygon_top.setBrush(QBrush(Qt.black))
            else:
                polygon_top.setBrush(QBrush(QColor("#8A8A8A")))
            
            points_bottom = [
                (x2, y2),
                (x2 - arrow_size/2, y2 - arrow_size),
                (x2 + arrow_size/2, y2 - arrow_size)
            ]
            polygon_bottom = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            if self.theme.is_light():
                polygon_bottom.setBrush(QBrush(Qt.black))
            else:
                polygon_bottom.setBrush(QBrush(QColor("#8A8A8A")))
        else:
            points_top = [
                (x2, y2),
                (x2 - arrow_size/2, y2 + arrow_size),
                (x2 + arrow_size/2, y2 + arrow_size)
            ]
            polygon_top = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
            if self.theme.is_light():
                polygon_top.setBrush(QBrush(Qt.black))
            else:
                polygon_top.setBrush(QBrush(QColor("#8A8A8A")))
            
            points_bottom = [
                (x1, y1),
                (x1 - arrow_size/2, y1 - arrow_size),
                (x1 + arrow_size/2, y1 - arrow_size)
            ]
            polygon_bottom = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            if self.theme.is_light():
                polygon_bottom.setBrush(QBrush(Qt.black))
            else:
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
