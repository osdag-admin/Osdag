import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView,
                             QGraphicsScene)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont
from ..Common import *

class BoltPatternGenerator(QMainWindow):
    def __init__(self, connection_obj):
        super().__init__()
        self.connection = connection_obj
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        self.setGeometry(100, 100, 800, 500)
        
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
            param_label = QLabel(f'{key.title()} Distance (mm):')
            value_label = QLabel(f'{value}')
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            left_layout.addLayout(param_layout)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Right panel for the drawing using QGraphicsView
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        
        # Create and add the drawing to the scene
        self.createDrawing(params)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.view, 3)
        
        # Set main widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Ensure the view shows all content
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
    
    def get_parameters(self):
        spacing_data = self.connection.spacing(status=True)  # Get actual values
        param_map = {}

        for item in spacing_data:
            key, _, _, value = item

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
        param_map['hole'] = 10.0

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
            gauge1=gauge
            gauge2=0
        width = gauge1 + gauge2 + edge
        height = 2 * end + 2 * pitch
        
        # Set up pens
        outline_pen = QPen(Qt.black, 2)
        dimension_pen = QPen(Qt.black, 1.5)  # Changed from blue to black
        
        # Dimension offsets
        h_offset = 40
        v_offset = 60
        
        # Create scene rectangle with extra space for dimensions
        self.scene.setSceneRect(-h_offset, -v_offset, 
                               width + 2*v_offset, height + 2*h_offset)
        
        # Draw rectangle
        self.scene.addRect(0, 0, width, height, outline_pen)
        
        # Draw holes
        # Top row
        if 'gauge' in params:
            gauge1=gauge
            gauge2=0
        self.scene.addEllipse(gauge1 - hole_diameter/2, end - hole_diameter/2, 
                             hole_diameter, hole_diameter, outline_pen)
        self.scene.addEllipse(gauge1 + gauge2 - hole_diameter/2, end - hole_diameter/2, 
                             hole_diameter, hole_diameter, outline_pen)
        
        # Middle row
        self.scene.addEllipse(gauge1 - hole_diameter/2, end + pitch - hole_diameter/2, 
                             hole_diameter, hole_diameter, outline_pen)
        self.scene.addEllipse(gauge1 + gauge2 - hole_diameter/2, end + pitch - hole_diameter/2, 
                             hole_diameter, hole_diameter, outline_pen)
        
        # Bottom row
        self.scene.addEllipse(gauge1 - hole_diameter/2, end + 2*pitch - hole_diameter/2, 
                             hole_diameter, hole_diameter, outline_pen)
        self.scene.addEllipse(gauge1 + gauge2 - hole_diameter/2, end + 2*pitch - hole_diameter/2, 
                             hole_diameter, hole_diameter, outline_pen)
        
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
            gauge1=gauge
            gauge2=0
        
        width = gauge1 + gauge2 + edge
        height = 2 * end + 2 * pitch
        
        # Offsets for dimension lines
        h_offset = 20
        v_offset = 30
        
        # Add horizontal dimensions
        self.addHorizontalDimension(0, -h_offset, gauge1, -h_offset, str(gauge1), pen)
        
        if gauge2 > 0:
            self.addHorizontalDimension(gauge1, -h_offset, gauge1 + gauge2, -h_offset, str(gauge2), pen)
            
        self.addHorizontalDimension(gauge1 + gauge2, -h_offset, width, -h_offset, str(edge), pen)
        
        # Add bottom horizontal dimension (edge_distance + gauge1 + gauge2)
        self.addHorizontalDimension(0, height + h_offset, width, height + h_offset, 
                                   str(edge + gauge1 + gauge2), pen)
        
        # Add vertical dimensions
        self.addVerticalDimension(width + v_offset, 0, width + v_offset, end, str(end), pen)
        self.addVerticalDimension(width + v_offset, end, width + v_offset, end + pitch, str(pitch), pen)
        self.addVerticalDimension(width + v_offset, end + pitch, width + v_offset, end + 2*pitch, str(pitch), pen)
        
        # Add bottom end distance dimension
        self.addVerticalDimension(width + v_offset, height, width + v_offset, height - end, str(end), pen)
        
        # Add left side dimension (2*(edge_distance + pitch_distance))
        self.addVerticalDimension(-v_offset, 0, -v_offset, height, 
                                 str(2 * (end + pitch)), pen)

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        # Draw dimension line
        self.scene.addLine(x1, y1, x2, y2, pen)
        
        # Draw extension lines
        ext_length = 10
        self.scene.addLine(x1, y1, x1, y1 + ext_length, pen)
        self.scene.addLine(x2, y2, x2, y2 + ext_length, pen)
        
        # Add arrows
        arrow_size = 2.5
        self.scene.addLine(x1, y1, x1 + arrow_size, y1 + arrow_size, pen)
        self.scene.addLine(x1, y1, x1 + arrow_size, y1 - arrow_size, pen)
        self.scene.addLine(x2, y1, x2 - arrow_size, y1 + arrow_size, pen)
        self.scene.addLine(x2, y1, x2 - arrow_size, y1 - arrow_size, pen)
        
        # Add text
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)  # Set your desired font size here
        text_item.setFont(font)
        text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 20)
        
    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        # Draw dimension line
        self.scene.addLine(x1, y1, x2, y2, pen)
        
        # Draw extension lines
        ext_length = 10
        self.scene.addLine(x1, y1, x1 - ext_length, y1, pen)
        self.scene.addLine(x2, y2, x2 - ext_length, y2, pen)
        
        # Add arrows
        arrow_size = 5
        self.scene.addLine(x1, y1, x1 + arrow_size, y1 + arrow_size, pen)
        self.scene.addLine(x1, y1, x1 - arrow_size, y1 + arrow_size, pen)
        self.scene.addLine(x1, y2, x1 + arrow_size, y2 - arrow_size, pen)
        self.scene.addLine(x1, y2, x1 - arrow_size, y2 - arrow_size, pen)
        
        # Add text
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)  # Set your desired font size here
        text_item.setFont(font)
        text_item.setPos(x1 - 30, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)