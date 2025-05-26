import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView,
                             QGraphicsScene)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtGui import QPolygonF, QBrush
from PyQt5.QtCore import QPointF
from ..Common import *
from .additionalfns import calculate_total_width
class SeatedanglespacingOnCol(QMainWindow):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        super().__init__()
        self.connection = connection_obj
        self.val=rows
        if self.val==3 or self.val==4:
            self.plate_width=main.seated_angle.width
            self.plate_length=main.seated_angle.leg_a_length
        else:
            self.plate_width=main.top_angle.width
            self.plate_length=main.top_angle.leg_a_length
        arr=[main.top_spacing_col(main,True),main.top_spacing_beam(main,True),main.seated_spacing_col(main,True),
             main.seated_spacing_beam(main,True)]
        val=self.val-1
        print(val)
        # print(arr[0],len(arr[0]))
        # print('\n\n')
        # for i in range(len(arr[0])):
        #     print(f"INDEX : {i}  : {arr[0][i]} , {arr[0][i][3]}")
        for i in arr[2]:
            print(i)
            print('\n\n')
        
        data = {entry[0]: entry[3] for entry in arr[val] if entry[0]}
        print(data)
        self.rows  = data['Bolt.Rows']
        self.cols  = data['Bolt.Cols']
        self.End   = data['Bolt.EndDist']
        self.Gauge = data['Bolt.Gauge']
        if self.Gauge==0 and 'Bolt.GaugeCentral' in data:
            self.Gauge=data['Bolt.GaugeCentral']
        self.Edge  = data['Bolt.EdgeDist']
        # return
        print(f"""
        Plate Dimensions
        ----------------
        Plate Width  : {self.plate_width} mm
        Plate Length : {self.plate_length} mm

        Bolt Layout
        -----------
        Rows         : {self.rows}
        Columns      : {self.cols}
        End Distance : {self.End} mm
        Gauge        : {self.Gauge} mm
        Edge Distance: {self.Edge} mm
        """)
        # self.initUI()
        self.param_map = {
    'end': self.End,
    'gauge': self.Gauge,
    'edge': self.Edge,
     'hole': main.bolt.bolt_diameter_provided
}
        
        print(self.param_map)
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        self.setGeometry(100, 100, 800, 500)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel for parameter display
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        params=self.param_map
        # Parameter display labels        
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
    


    def createDrawing(self, params):
        
        # Extract parameters

        end = params['end']
        if 'gauge' in params:
            gauge = params['gauge']
        edge = params['edge']
        hole_diameter = params['hole']
        print(f"rows: {self.rows}, cols: {self.cols}")
        # Calculate dimensions
 
        width = self.plate_width

        height = self.plate_length
        # Set up pens
        outline_pen = QPen(Qt.blue, 2)
        dimension_pen = QPen(Qt.black, 1.5)
        
        # Dimension offsets
        h_offset = 40
        v_offset = 60
        
        # Create scene rectangle with extra space for dimensions
        self.scene.setSceneRect(-h_offset, -v_offset, 
                               width + 2*v_offset, height + 2*h_offset)
        
        # Draw rectangle
        self.scene.addRect(0, 0, width, height, dimension_pen)

        # Draw holes
        for row in range(self.rows):
            for col in range(self.cols):
                # Start from edge distance (center of first hole)
                x_center = edge
                for i in range(col):
                    x_center += gauge

                # Center of hole is at (x_center, y_center)
                # Subtract hole_diameter/2 to draw ellipse properly from top-left
                x = x_center - hole_diameter / 2
                y_center = end 
                y = y_center - hole_diameter / 2

                print(f"row: {row}, col: {col}, x: {x}, y: {y}")
                self.scene.addEllipse(x, y, hole_diameter, hole_diameter, outline_pen)
        print(params,dimension_pen)
        # Add dimensions
        self.addDimensions(params, dimension_pen)

    def addDimensions(self, params, pen):
        # Extract parameters
        end = params['end']
        if 'gauge' in params:
            gauge = params['gauge']

        edge = params['edge']


        
        width=self.plate_width
        height=self.plate_length
        
        # Offsets for dimension lines
        h_offset = 20
        v_offset = 30
        
        # Add horizontal dimensions
        x_start = 0
        segments = []
        # First edge
        segments.append(('edge', x_start, x_start + edge))
        x_start += edge
        segments.append(('edge' ,x_start,x_start+gauge ))
        x_start+=gauge
        # Last edge
        segments.append(('edge', x_start, x_start + edge))

        # Draw each segment
        for label, x1, x2 in segments:
            value = x2 - x1
            self.addHorizontalDimension(x1, -h_offset, x2, -h_offset, f"{value:.1f}", pen)
        # Add vertical dimensions
        self.addVerticalDimension(width + v_offset, 0, width + v_offset, end, str(end), pen)
        
        # Add bottom end distance dimension
        self.addVerticalDimension(width + v_offset, height, width + v_offset, height - end, str(end), pen)
        
        # Add left side dimension
        total_height = 2 * end + (self.rows - 1)
        self.addVerticalDimension(-v_offset, 0, -v_offset, total_height, str(total_height), pen)

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 5
        ext_length = 10
        self.scene.addLine(x1, y1 - ext_length/2, x1, y1 + ext_length/2, pen)
        self.scene.addLine(x2, y2 - ext_length/2, x2, y2 + ext_length/2, pen)
        
        points_left = [
            (x1, y1),
            (x1 + arrow_size, y1 - arrow_size/2),
            (x1 + arrow_size, y1 + arrow_size/2)
        ]
        polygon_left = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_left]), pen)
        polygon_left.setBrush(QBrush(Qt.black))
        
        points_right = [
            (x2, y2),
            (x2 - arrow_size, y2 - arrow_size/2),
            (x2 - arrow_size, y2 + arrow_size/2)
        ]
        polygon_right = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_right]), pen)
        polygon_right.setBrush(QBrush(Qt.black))
        
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        
        if y1 < 0:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 25)
        else:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 + 5)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 5
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
            polygon_top.setBrush(QBrush(Qt.black))
            
            points_bottom = [
                (x2, y2),
                (x2 - arrow_size/2, y2 - arrow_size),
                (x2 + arrow_size/2, y2 - arrow_size)
            ]
            polygon_bottom = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            polygon_bottom.setBrush(QBrush(Qt.black))
        else:
            points_top = [
                (x2, y2),
                (x2 - arrow_size/2, y2 + arrow_size),
                (x2 + arrow_size/2, y2 + arrow_size)
            ]
            polygon_top = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
            polygon_top.setBrush(QBrush(Qt.black))
            
            points_bottom = [
                (x1, y1),
                (x1 - arrow_size/2, y1 - arrow_size),
                (x1 + arrow_size/2, y1 - arrow_size)
            ]
            polygon_bottom = self.scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            polygon_bottom.setBrush(QBrush(Qt.black))
        
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        
        if x1 < 0:
            text_item.setPos(x1 - 10 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1 + 15, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)