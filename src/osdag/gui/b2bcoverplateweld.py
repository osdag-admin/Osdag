import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView,
                             QGraphicsScene,QGraphicsRectItem)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont , QColor
from PyQt5.QtGui import QPolygonF, QBrush
from PyQt5.QtCore import QPointF
from ..Common import *
from .additionalfns import calculate_total_width
class B2Bcoverplateweld(QMainWindow):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        print(main)
        if main:
            self.web=main[1]
            web=main[1]
            main=main[0]
        super().__init__()
        self.connection = connection_obj
        data=main.output_values(main,True)
        
        print(type(main))
        dict1={i[0] : i[3] for i in data}
        for i in dict1:
            print(f'{i} : {dict1[i]}')
        print("????????????????????????????DEBUG?????????????????????????????")
        print(dict1)
        print("????????????????????????????DEBUG?????????????????????????????")
        
        if web==True:
            self.plate_length=main.web_plate.height
            self.plate_width=main.web_plate.length
            self.plate_thickness=float(dict1['Connector.Web_Plate.Thickness_List'])
            self.weld_size=main.web_weld.size
            self.weld_gap=main.web_plate.gap
        elif web==False:
            self.plate_width=main.flange_plate.length
            self.plate_length=main.flange_plate.height
            self.plate_thickness=float(dict1['Connector.Flange_Plate.Thickness_list'])
            self.weld_size=main.flange_weld.size
            self.weld_gap=main.flange_plate.gap
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        print(f"""
        -----------------------------------------
            Plate  Configuration Summary
        -----------------------------------------
        Plate Length           : {self.plate_length} mm
        Plate Width            : {self.plate_width} mm
        Weld size              : {self.weld_size} mm
        Weld gap               : {self.weld_gap} mm
        """)
        
        self.setGeometry(100, 100, 800, 500)
        # Step 1: Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Step 2: Create main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Step 3: Left panel for selected labels only
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # Only display selected keys
        keys_to_display = [
            'Plate Length',
            'Plate Width',
           
        ]

        # Define the corresponding values for the keys (assumes self.<attribute> are already set)
        values_to_display = {
            'Plate Length': self.plate_length,
            'Plate Width': self.plate_width,
            
        }


        for key in keys_to_display:
            if key in values_to_display:
                label = QLabel(f"<b>{key}:</b> {values_to_display[key]}")
                left_layout.addWidget(label)
        # Step 4: Graphics view and scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        # Background and test shape (optional)
        self.scene.setBackgroundBrush(Qt.white)

        # Step 5: Add to main layout
        main_layout.addWidget(self.view, stretch=2)
        main_layout.addWidget(left_panel, stretch=1)
        
        self.fontsize=10
        self.arrowsize=10
        
        if self.plate_length>1200 or self.plate_width>1200:
            self.fontsize=5
            self.arrowsize=5
        elif self.plate_length>600 or self.plate_width>600:
            self.fontsize=10
            self.arrowsize=10
        self.createDrawing()
        if self.plate_length>1200 or self.plate_width>1200:
            self.view.resetTransform()
            self.view.scale(0.4, 0.4)
        elif self.plate_length>600 or self.plate_width>600:
            self.view.resetTransform()
            self.view.scale(0.75, 0.75)
        
        # Step 6: Call parameter extraction and drawing
        
            
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
        outline_pen.setWidth(2)
        
        # === Draw Base Plate Rectangle ===
        rect_item = QGraphicsRectItem(QRectF(0, 0, plate_length, plate_width))
        rect_item.setPen(outline_pen)
        rect_item.setBrush(QBrush(Qt.white))
        self.scene.addItem(rect_item)

        dimension_pen = QPen(Qt.black, 1.5)
        weld_fill = QBrush(Qt.blue)
        if self.web==True:
            self.scene.addRect(0, (plate_width-self.plate_thickness)/2 , plate_length, self.plate_thickness, dimension_pen, weld_fill)
        elif self.web==False:
            self.scene.addRect((plate_length-self.plate_thickness)/2, 0 , self.plate_thickness, plate_width, dimension_pen, weld_fill)
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
        weld_size=self.weld_size
        weld_gap=self.weld_gap
        red_brush = QBrush(Qt.red)

        # === Top weld outside plate ===
        top_weld = QGraphicsRectItem(QRectF(0, -weld_size, plate_length, weld_size))
        top_weld.setBrush(red_brush)
        self.scene.addItem(top_weld)

        # === Bottom weld outside plate ===
        bottom_weld = QGraphicsRectItem(QRectF(0, plate_width, plate_length, weld_size))
        bottom_weld.setBrush(red_brush)
        self.scene.addItem(bottom_weld)

        # === Vertical welds (left and right), split due to weld_gap ===
        half_gap = weld_gap / 2
        half_height = (plate_width - weld_gap) / 2

        # Left side, top weld (outside)
        left_top = QGraphicsRectItem(QRectF(-weld_size, 0, weld_size, half_height))
        left_top.setBrush(red_brush)
        self.scene.addItem(left_top)

        # Left side, bottom weld (outside)
        left_bottom = QGraphicsRectItem(QRectF(-weld_size, plate_width - half_height, weld_size, half_height))
        left_bottom.setBrush(red_brush)
        self.scene.addItem(left_bottom)

        # Right side, top weld (outside)
        right_top = QGraphicsRectItem(QRectF(plate_length, 0, weld_size, half_height))
        right_top.setBrush(red_brush)
        self.scene.addItem(right_top)

        # Right side, bottom weld (outside)
        right_bottom = QGraphicsRectItem(QRectF(plate_length, plate_width - half_height, weld_size, half_height))
        right_bottom.setBrush(red_brush)
        self.scene.addItem(right_bottom)
    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = self.arrowsize
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
        font.setPointSize(self.fontsize)
        text_item.setFont(font)
        
        if y1 < 0:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 25)
        else:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 + 5)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = self.arrowsize
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
        font.setPointSize(self.fontsize)
        text_item.setFont(font)
        
        if x1 < 0:
            text_item.setPos(x1 - 10 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1 + 15, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
