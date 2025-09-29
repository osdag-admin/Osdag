import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView,
                             QGraphicsScene,QGraphicsRectItem)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QFont , QColor
from PySide6.QtGui import QPolygonF, QBrush
from PySide6.QtCore import QPointF
from osdag_core.Common import *

class B2BCoverPlateDetails(QMainWindow):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        print(main)
        
        if main:
            web=main[1]
            main=main[0]
        super().__init__()
        self.connection = connection_obj
        # return
        data=main.output_values(True)
        print(type(main))
        dict1={i[0] : i[3] for i in data}


        print("________________________DEBUG________________________")
        print(dict1)
        print("________________________DEBUG________________________")

        for i in dict1:
            print(f'{i} : {dict1[i]}')
        if web==True:
            self.plate_length=dict1['Web_Plate.Height (mm)']
            self.plate_width=dict1['Web_Plate.Width']
            self.bolt_diameter=dict1['Bolt.Diameter']
            web_capcity=dict1['Web_plate.spacing'][1]
            print(web_capcity(True))
            data2=web_capcity(True)
            for i in range(len(data2)):
                print(f"{i} : {data2[i]}")
            self.pitch=data2[2][3]
            self.End=data2[3][3]
            self.Gauge=data2[4][3]
            self.Edge=data2[5][3]
            bolt_cap=dict1['Web Bolt.Capacities'][1]
            print(bolt_cap(True))
            bolt_cap=bolt_cap(main,True)
        elif web==False:
            self.plate_length=dict1['Flange_Plate.Width (mm)']
            self.plate_width=dict1['flange_plate.Length']
            self.bolt_diameter=dict1['Bolt.Diameter']
            flange_capcity=dict1['Flange_plate.spacing'][1]
            data2=flange_capcity(main,True)
            self.pitch=data2[2][3]
            self.End=data2[3][3]
            self.Gauge=data2[4][3]
            self.Edge=data2[5][3]
            bolt_cap=dict1['Bolt.Capacities'][1]
            print(bolt_cap(main,True))
            bolt_cap=bolt_cap(main,True)
        self.cols=bolt_cap[1][3]
        self.rows=bolt_cap[2][3]/self.cols
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        self.setGeometry(100, 100, 800, 500)

        # Print summary (optional debug/log info)
        print(f"""
        -----------------------------------------
            Plate & Bolt Configuration Summary
        -----------------------------------------
        Plate Length           : {self.plate_length} mm
        Plate Width            : {self.plate_width} mm
        Bolt Diameter          : {self.bolt_diameter} mm

        Bolt Spacing Details:
        ---------------------
        Pitch Distance         : {self.pitch} mm
        End Distance           : {self.End} mm
        Gauge Distance         : {self.Gauge} mm
        Edge Distance          : {self.Edge} mm

        Bolt Arrangement:
        -----------------
        Number of Columns      : {self.cols}
        Number of Rows         : {self.rows}
        """)

        # Main layout
        main_layout = QHBoxLayout()

        # Left panel for parameter display
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        # Get parameter dictionary
        params = self.get_parameters()

        for key, value in params.items():
            param_layout = QHBoxLayout()
            param_label = QLabel(f'{key.title()} (mm):')
            value_label = QLabel(f'{value}')
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            left_layout.addLayout(param_layout)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # Right panel: QGraphicsView with Scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        # Determine font and arrow size based on plate size
        self.fontsize = 10
        self.arrowsize = 10
        if self.plate_length > 1200 or self.plate_width > 1200:
            self.fontsize = 12
            self.arrowsize = 12
        elif self.plate_length > 600 or self.plate_width > 600:
            self.fontsize = 7.5
            self.arrowsize = 7.5

        # Draw bolts and plate
        self.createDrawing()
        if self.plate_length>1200 or self.plate_width>1200:
            self.view.resetTransform()
            self.view.scale(0.35, 0.35)
        elif self.plate_length>600 or self.plate_width>600:
            self.view.resetTransform()
            self.view.scale(0.5, 0.5)
        # Add panels to layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.view, 3)

        # Set central widget with main layout
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Automatically adjust view to fit scene
    def get_parameters(self):
        return {
            'Plate Length': self.plate_length,
            'Plate Width': self.plate_width,
            'Bolt Diameter': self.bolt_diameter,
            'Pitch Distance': self.pitch,
            'End Distance': self.End,
            'Gauge Distance': self.Gauge,
            'Edge Distance': self.Edge,
            'Number of Columns': self.cols,
            'Number of Rows': self.rows
        }
    def createDrawing(self):
        try:
            plate_length = float(self.plate_length)
            plate_width = float(self.plate_width)
        except (TypeError, ValueError):
            print("Invalid plate dimensions")
            return
        rect = QRectF(0, 0, plate_length, plate_width)
        # Create a rectangle item
        rect_item = QGraphicsRectItem(rect)

        # Set pen and brush (black border, transparent fill)
        pen = QPen(Qt.black)
        pen.setWidth(2)
        rect_item.setPen(pen)
        rect_item.setBrush(QBrush(Qt.NoBrush))

        # Add rectangle to the scene
        self.scene.addItem(rect_item)
        # Extract parameters
        outline_pen = QPen(Qt.black)
        outline_pen.setWidth(1)
        
        # === Draw Base Plate Rectangle ===
        rect_item = QGraphicsRectItem(QRectF(0, 0, plate_length, plate_width))
        rect_item.setPen(outline_pen)
        rect_item.setBrush(QBrush(Qt.white))
        self.scene.addItem(rect_item)
        # === Center of the base plate ===
        center_x = plate_length / 2
        center_y = plate_width / 2
        self.addHorizontalDimension(
            0, -30,  # x1 at left edge, y above plate
            self.plate_length, -30,  # x2 at right edge, same y
            f"{self.plate_length} mm", pen
        )

        # Vertical dimension for plate width (to the left of the plate)
        self.addVerticalDimension(
            self.plate_length+30, 0,  # x left of plate, y1 at top
            self.plate_length+30, self.plate_width,  # x2 same, y2 at bottom
            f"{self.plate_width} mm", pen
        )
        rows=int(self.rows)
        cols=int(self.cols)
        pitch=self.pitch
        gauge=self.Gauge
        end=self.End
        edge=self.Edge
        hole_dia = self.bolt_diameter
        radius = hole_dia / 2
        y_center = end  # Y position is fixed for top row
        # Center row if rows is odd
        outline_pen = QPen(Qt.blue)
        outline_pen.setWidth(1)
        if rows % 2 != 0:
            y_center = self.plate_width / 2
            for i in range(cols // 2):
                x_center = edge + i * gauge
                self.scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

            for i in range(cols // 2):
                x_center = self.plate_length - edge - i * gauge
                self.scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

            # Center bolt if cols is also odd
            if cols % 2 != 0:
                x_center = self.plate_length / 2
                self.scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

        # Center column if cols is odd (and rows is even)
        if cols % 2 != 0 and rows % 2 == 0:
            for j in range(rows // 2):
                y_center_top = end + j * pitch
                y_center_bottom = self.plate_width - end - j * pitch

                x_center = self.plate_length / 2
                self.scene.addEllipse(
                    x_center - radius,
                    y_center_top - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )
                self.scene.addEllipse(
                    x_center - radius,
                    y_center_bottom - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

        # Draw left half bolts
        for row in range(int(rows)):
            if row < rows // 2:
                y_center = end + row * pitch
            else:
                row_from_bottom = row - rows // 2
                y_center = self.plate_width - end - row_from_bottom * pitch

            # Left half bolts
            for i in range(cols // 2):
                x_center = edge + i * gauge
                self.scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

            # Right half bolts
            for i in range(cols // 2):
                x_center = self.plate_length - edge - i * gauge
                self.scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )
        self.addHorizontalDimension(
            0, self.plate_width+10,  # x1 at left edge, y above plate
            self.Edge, self.plate_width+10,  # x2 at right edge, same y
            f"{self.Edge} mm", pen
        )
        self.addVerticalDimension(
            -10, 0,  # x left of plate, y1 at top
            -10, self.End,  # x2 same, y2 at bottom
            f"{self.End} mm", pen
        )
        self.addHorizontalDimension(
            self.Edge-hole_dia/2, 10,  
            self.Edge+hole_dia/2,10, 
            f"{hole_dia} mm", pen
        )
    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = int(self.arrowsize)
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
        font.setPointSize(int(self.fontsize))
        text_item.setFont(font)
        
        if y1 < 0:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 25)
        else:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 + 5)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = int(self.arrowsize)
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
        font.setPointSize(int(self.fontsize))
        text_item.setFont(font)
        
        if x1 < 0:
            text_item.setPos(x1 - 10 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1 + 15, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
