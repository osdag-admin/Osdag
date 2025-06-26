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
class B2BEndPlateSketch(QMainWindow):
    def __init__(self, connection_obj,main, rows=3, cols=2):
        super().__init__()
        self.connection = connection_obj
        data=main.output_values(main,True)
        self.web_thick=main.beam_tw
        self.endplatetype=main.endplate_type
        self.flange_thick=main.beam_tf
        self.middle_bolts=main.bolt_row_web
        self.stiffener_length = main.stiffener_height
        self.stiffener_thickness=main.stiffener_thickness
        self.stiffener_width=main.stiffener_length
        self.rows_inside_D_max = main.rows_inside_D_max
        self.rows_outside_D_max = main.rows_outside_D_max
        self.detail_dict = {
                                entry[1]: entry[3]
                                for entry in data
                                }
        for i in self.detail_dict:
            print(f' {i} : {self.detail_dict[i]}')
        self.beam_width=main.beam_D
        print(f'Beam Width : {main.beam_bf} , Beam Depth : {main.beam_D}')
        print(self.stiffener_width,self.stiffener_length)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        print(f'End Plate Type :  {self.endplatetype}')
        print(f'middle bolts : {self.middle_bolts}')
        print(f'stiffener length : {self.stiffener_length}')
        
        self.setGeometry(100, 100, 1200, 500)
        print(f'web thickness : {self.web_thick}, flange thickness : {self.flange_thick} ')
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
            
        ]

        # Add labels
        for key in keys_to_display:
            if key in self.detail_dict:
                value = self.detail_dict[key]
                label = QLabel(f"<b>{key}</b>: {value}")
                left_layout.addWidget(label)

        # Step 4: Graphics view and scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        # Background and test shape (optional)
        self.scene.setBackgroundBrush(Qt.white)

        # Step 5: Add to main layout
        main_layout.addWidget(left_panel, stretch=1)
        main_layout.addWidget(self.view, stretch=3)

        # Step 6: Call parameter extraction and drawing
        self.get_parameters()
    def get_parameters(self):
        print('setting parameters')
        self.rows=self.detail_dict['No. of Rows']
        self.cols=self.detail_dict['No. of Columns']
        print(f'rows : {self.rows} , cols : {self.cols}')
        self.pitch=self.detail_dict['Pitch Distance (mm)']
        self.CrossGauge=self.detail_dict['Cross-centre Gauge (mm)']
        value = self.detail_dict['Gauge Distance (mm)']
        self.Gauge = float(value) if str(value).isdigit() else self.CrossGauge
        self.End=self.detail_dict['End Distance (mm)']
        self.Edge=self.detail_dict['Edge Distance (mm)']
        self.height=self.detail_dict['Height (mm)']
        self.width=self.detail_dict['Width (mm)']
        self.hole_diameter=self.detail_dict['Diameter (mm)']
        self.plate_thickness=self.detail_dict['Thickness (mm)']
        if self.endplatetype.startswith('Flushed'):
            self.createDrawingFlushedReversible()
        elif self.endplatetype.startswith('Extended One'):
            self.createDrawingExtendedOneWay()
        else:
            self.createDrawingExtendedTwoWay()
    def createDrawingFlushedReversible(self):
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPen, QColor, QBrush,QPolygonF
        from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsPolygonItem
        # === Input Parameters ===
        plate_height = self.height
        stiffener_height = self.stiffener_length
        stiffener_width=self.stiffener_width
        stiffener_thickness=self.stiffener_thickness
        plate_thickness=self.plate_thickness
        print('stiff thicknes:',stiffener_thickness , 'stiff width : ',stiffener_width)
        h_gap = 12.5
        flange_thick=self.flange_thick
        beam_width=self.beam_width
        total_plate_width = 2 * plate_thickness
        view_width,view_height=800,800
        start_x = (view_width - total_plate_width) / 2
        start_y = (view_height - plate_height) / 2

        # Draw first plate
        total_plate_width = 2 * plate_thickness
        start_x = (view_width - total_plate_width) / 2
        start_y = (view_height - plate_height) / 2

        # === Pen (blue border, no fill) ===
        blue_pen = QPen(QColor("blue"))
        blue_pen.setWidth(2)
        blackpen=QPen(QColor("black"))
        # === Draw Rectangles ===
        self.scene.addRect(start_x, start_y, plate_thickness, plate_height, blue_pen)
        dim_y = start_y + plate_height + 20  # 20 px below
        self.addHorizontalDimension(start_x, dim_y, start_x + plate_thickness, dim_y, str(plate_thickness), blackpen)
        self.addHorizontalDimension(start_x, dim_y, start_x -beam_width, dim_y, str(beam_width), blackpen)
        self.addVerticalDimension(start_x-beam_width-20,start_y,start_x-beam_width-20,start_y+plate_height , str(plate_height),blackpen)
        self.scene.addRect(start_x + plate_thickness, start_y, plate_thickness, plate_height, blue_pen, )
        red_brush = QBrush(QColor("red"))
        red_pen = QPen(Qt.NoPen)  # No border for stiffeners

        stiffener_width = stiffener_thickness / 2

        beam_y = start_y + 12.5
        beam_height = plate_height - 2 *12.5
        pen =  QPen(QColor("orange"))
        # Left beam rectangle (left of left plate)
        self.scene.addRect(
            start_x - beam_width,
            beam_y,
            beam_width,
            beam_height,
            pen,
            QBrush(Qt.NoBrush)
        )

        # Right beam rectangle (right of right plate)
        self.scene.addRect(
            start_x + 2 * plate_thickness,
            beam_y,
            beam_width,
            beam_height,
            pen,
            QBrush(Qt.NoBrush)
        )
        
        stiffener_width=self.stiffener_width
        # X coordinates
        x_left_start = start_x
        x_left_end = start_x-beam_width

        x_right_end = start_x+2*plate_thickness
        x_right_start = x_right_end +beam_width

        # Y positions
        y_top = start_y+  flange_thick + 12.5
        y_bottom = (start_y+plate_height) - 12.5 - flange_thick

        # Left-top horizontal line
        self.scene.addLine(x_left_start, y_top, x_left_end, y_top, pen)

        # Left-bottom horizontal line
        self.scene.addLine(x_left_start, y_bottom, x_left_end, y_bottom, pen)

        # Right-top horizontal line
        self.scene.addLine(x_right_start, y_top, x_right_end, y_top, pen)

        # Right-bottom horizontal line
        self.scene.addLine(x_right_start, y_bottom, x_right_end, y_bottom, pen)
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        offset_len = 25  # 25mm offset for both lines

# Coordinates for the top-left corner of the left plate
        pen = QPen(Qt.black, 2)
        pen2=QPen(Qt.black, 1)
        brush = QBrush(Qt.NoBrush)
        half_thick = stiffener_thickness / 2.0

        self.scene.addRect(
            start_x - stiffener_thickness,
            start_y+12.5,
            stiffener_thickness,
            plate_height - 2*12.5,
            red_pen,
            red_brush
        )
        self.scene.addRect(
            start_x +2*plate_thickness,
            start_y+12.5,
            stiffener_thickness,
            plate_height - 2*12.5,
            red_pen,
            red_brush
        )
    
    def createDrawingExtendedOneWay(self):
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPen, QColor, QBrush,QPolygonF
        from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsPolygonItem
        # === Input Parameters ===
        plate_height = self.height
        stiffener_height = self.stiffener_length
        stiffener_width=self.stiffener_width
        stiffener_thickness=self.stiffener_thickness
        plate_thickness=self.plate_thickness
        print('stiff thicknes:',stiffener_thickness , 'stiff width : ',stiffener_width)
        h_gap = 12.5
        flange_thick=self.flange_thick
        beam_width=self.beam_width
        total_plate_width = 2 * plate_thickness
        view_width,view_height=800,800
        start_x = (view_width - total_plate_width) / 2
        start_y = (view_height - plate_height) / 2
        blackpen=QPen(QColor("black"))
        # Draw first plate
        total_plate_width = 2 * plate_thickness
        start_x = (view_width - total_plate_width) / 2
        start_y = (view_height - plate_height) / 2

        # === Pen (blue border, no fill) ===
        blue_pen = QPen(QColor("blue"))
        blue_pen.setWidth(2)

        # === Draw Rectangles ===
        self.scene.addRect(start_x, start_y, plate_thickness, plate_height, blue_pen)
        self.scene.addRect(start_x + plate_thickness, start_y, plate_thickness, plate_height, blue_pen, )
        red_brush = QBrush(QColor("red"))
        red_pen = QPen(Qt.NoPen)  # No border for stiffeners
        dim_y = start_y + plate_height + 20  # 20 px below
        self.addHorizontalDimension(start_x, dim_y, start_x + plate_thickness, dim_y, str(plate_thickness), blackpen)
        self.addHorizontalDimension(start_x, dim_y, start_x -beam_width, dim_y, str(beam_width), blackpen)
        self.addVerticalDimension(start_x-beam_width-20,start_y,start_x-beam_width-20,start_y+plate_height , str(plate_height),blackpen)
        
        stiffener_width = stiffener_thickness / 2

        # Top stiffener (left of left plate)
        self.scene.addRect(
            start_x - stiffener_width,
            start_y,
            stiffener_width,
            stiffener_height,
            red_pen,
            red_brush
        )
        self.scene.addRect(
            start_x - 2*stiffener_width,
            start_y+stiffener_height,
            2*stiffener_width,
            plate_height-stiffener_height,
            red_pen,
            red_brush
        )
        self.scene.addRect(
            start_x + 2 * plate_thickness,
            start_y+stiffener_height,
            2*stiffener_width,
            plate_height-stiffener_height,
            red_pen,
            red_brush
        )
        self.scene.addRect(
        start_x + 2 * plate_thickness,              # Right side of right plate
        start_y,
        stiffener_width,
        stiffener_height,
        red_pen,
        red_brush
    )
        
        beam_y = start_y + stiffener_height
        beam_height = plate_height -stiffener_height-12.5
        pen =  QPen(QColor("orange"))
        # Left beam rectangle (left of left plate)
        self.scene.addRect(
            start_x - beam_width,
            beam_y,
            beam_width,
            beam_height,
            pen,
            QBrush(Qt.NoBrush)
        )

        # Right beam rectangle (right of right plate)
        self.scene.addRect(
            start_x + 2 * plate_thickness,
            beam_y,
            beam_width,
            beam_height,
            pen,
            QBrush(Qt.NoBrush)
        )
        
        stiffener_width=self.stiffener_width
        # X coordinates
        x_left_start = start_x
        x_left_end = start_x-beam_width

        x_right_end = start_x+2*plate_thickness
        x_right_start = x_right_end +beam_width

        # Y positions
        y_top = start_y+stiffener_height + flange_thick
        y_bottom = (start_y+plate_height)  - flange_thick-12.5

        # Left-top horizontal line
        self.scene.addLine(x_left_start, y_top, x_left_end, y_top, pen)

        # Left-bottom horizontal line
        self.scene.addLine(x_left_start, y_bottom, x_left_end, y_bottom, pen)

        # Right-top horizontal line
        self.scene.addLine(x_right_start, y_top, x_right_end, y_top, pen)

        # Right-bottom horizontal line
        self.scene.addLine(x_right_start, y_bottom, x_right_end, y_bottom, pen)
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        offset_len = 25  # 25mm offset for both lines

# Coordinates for the top-left corner of the left plate
        pen = QPen(Qt.black, 2)
        pen2=QPen(Qt.black, 1)
        brush = QBrush(Qt.NoBrush)
        half_thick = stiffener_thickness / 2.0
        # === TOP LEFT ===
        x1, y1 = start_x, start_y
        x2, y2 = start_x - offset_len, start_y
        x3, y3 = start_x - stiffener_width, start_y + stiffener_height - offset_len
        x4, y4 = start_x - stiffener_width, start_y + stiffener_height
        x5, y5 = start_x, start_y + stiffener_height
        points_tl = [QPointF(x1, y1), QPointF(x2, y2), QPointF(x3, y3), QPointF(x4, y4), QPointF(x5, y5)]
        polygon_tl = QGraphicsPolygonItem(QPolygonF(points_tl))
        polygon_tl.setPen(pen)
        polygon_tl.setBrush(brush)
        self.scene.addItem(polygon_tl)
        # Red cap
        x6, y6 = x5, y5 - half_thick
        x7, y7 = x4, y4 - half_thick
        polygon_tl = QGraphicsPolygonItem(QPolygonF([QPointF(x4, y4), QPointF(x5, y5), QPointF(x6, y6), QPointF(x7, y7)]))
        polygon_tl.setPen(pen)
        polygon_tl.setBrush(red_brush)
        self.scene.addItem(polygon_tl)
        
        # Red cap
        
        # === TOP RIGHT ===
        x1, y1 = start_x + 2 * plate_thickness, start_y
        x2, y2 = x1 + offset_len, start_y
        x3, y3 = x1 + stiffener_width, start_y + stiffener_height - offset_len
        x4, y4 = x1 + stiffener_width, start_y + stiffener_height
        x5, y5 = x1, start_y + stiffener_height
        points_tr = [QPointF(x1, y1), QPointF(x2, y2), QPointF(x3, y3), QPointF(x4, y4), QPointF(x5, y5)]
        polygon_tr = QGraphicsPolygonItem(QPolygonF(points_tr))
        polygon_tr.setPen(pen)
        polygon_tr.setBrush(brush)
        self.scene.addItem(polygon_tr)
        # Red cap
        x6, y6 = x5, y5 - half_thick
        x7, y7 = x4, y4 - half_thick
        polygon_tl = QGraphicsPolygonItem(QPolygonF([QPointF(x4, y4), QPointF(x5, y5), QPointF(x6, y6), QPointF(x7, y7)]))
        polygon_tl.setPen(pen)
        polygon_tl.setBrush(red_brush)
        self.scene.addItem(polygon_tl)

        # Red cap
        
        self.addHorizontalDimension(start_x,start_y-40,start_x-stiffener_width,start_y-40,str(stiffener_width),blackpen)
        xpos=start_x +2*plate_thickness +stiffener_width+20
        self.addVerticalDimension(xpos,start_y,xpos,start_y+stiffener_height,str(stiffener_height),blackpen)
        # self.addInternalGapsExtendedOneWay()
        # self.addDimensionsExtendedOneWay(edge,self.Gauge,self.CrossGauge,self.cols)
    
    def createDrawingExtendedTwoWay(self):
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPen, QColor, QBrush,QPolygonF
        from PyQt5.QtWidgets import QGraphicsRectItem,QGraphicsPolygonItem
        # === Input Parameters ===
        plate_height = self.height
        stiffener_height = self.stiffener_length
        stiffener_width=self.stiffener_width
        stiffener_thickness=self.stiffener_thickness
        plate_thickness=self.plate_thickness
        print('stiff thicknes:',stiffener_thickness , 'stiff width : ',stiffener_width)
        h_gap = 12.5
        flange_thick=self.flange_thick
        beam_width=self.beam_width
        total_plate_width = 2 * plate_thickness
        view_width,view_height=800,800
        start_x = (view_width - total_plate_width) / 2
        start_y = (view_height - plate_height) / 2

        # Draw first plate
        total_plate_width = 2 * plate_thickness
        start_x = (view_width - total_plate_width) / 2
        start_y = (view_height - plate_height) / 2

        # === Pen (blue border, no fill) ===
        blue_pen = QPen(QColor("blue"))
        blue_pen.setWidth(2)
        blackpen=QPen(QColor("black"))
        # === Draw Rectangles ===
        self.scene.addRect(start_x, start_y, plate_thickness, plate_height, blue_pen)
        self.scene.addRect(start_x + plate_thickness, start_y, plate_thickness, plate_height, blue_pen, )
        red_brush = QBrush(QColor("red"))
        red_pen = QPen(Qt.NoPen)  # No border for stiffeners
        dim_y = start_y + plate_height + 20  # 20 px below
        self.addHorizontalDimension(start_x, dim_y, start_x + plate_thickness, dim_y, str(plate_thickness), blackpen)
        self.addHorizontalDimension(start_x, dim_y, start_x -beam_width, dim_y, str(beam_width), blackpen)
        self.addVerticalDimension(start_x-beam_width-20,start_y,start_x-beam_width-20,start_y+plate_height , str(plate_height),blackpen)
        
        stiffener_width = stiffener_thickness / 2

        # Top stiffener (left of left plate)
        self.scene.addRect(
            start_x - stiffener_width,
            start_y,
            stiffener_width,
            stiffener_height,
            red_pen,
            red_brush
        )
        self.scene.addRect(
            start_x - 2*stiffener_width,
            start_y+stiffener_height,
            stiffener_width*2,
            plate_height-2*stiffener_height,
            red_pen,
            red_brush
        )

        # Bottom stiffener (left of left plate)
        self.scene.addRect(
            start_x - stiffener_width,
            start_y + plate_height - stiffener_height,
            stiffener_width,
            stiffener_height,
            red_pen,
            red_brush
        )
        self.scene.addRect(
        start_x + 2 * plate_thickness,              # Right side of right plate
        start_y,
        stiffener_width,
        stiffener_height,
        red_pen,
        red_brush
    )
        self.scene.addRect(
        start_x + 2 * plate_thickness,              # Right side of right plate
        start_y+stiffener_height,
        stiffener_width*2,
        plate_height-2*stiffener_height,
        red_pen,
        red_brush
    )

        self.scene.addRect(
            start_x + 2 * plate_thickness,              # Right side of right plate
            start_y + plate_height - stiffener_height,
            stiffener_width,
            stiffener_height,
            red_pen,
            red_brush
        )
        beam_y = start_y + stiffener_height
        beam_height = plate_height - 2 * stiffener_height
        pen =  QPen(QColor("orange"))
        # Left beam rectangle (left of left plate)
        self.scene.addRect(
            start_x - beam_width,
            beam_y,
            beam_width,
            beam_height,
            pen,
            QBrush(Qt.NoBrush)
        )

        # Right beam rectangle (right of right plate)
        self.scene.addRect(
            start_x + 2 * plate_thickness,
            beam_y,
            beam_width,
            beam_height,
            pen,
            QBrush(Qt.NoBrush)
        )
        
        stiffener_width=self.stiffener_width
        # X coordinates
        x_left_start = start_x
        x_left_end = start_x-beam_width

        x_right_end = start_x+2*plate_thickness
        x_right_start = x_right_end +beam_width

        # Y positions
        y_top = start_y+stiffener_height + flange_thick
        y_bottom = (start_y+plate_height) - stiffener_height - flange_thick

        # Left-top horizontal line
        self.scene.addLine(x_left_start, y_top, x_left_end, y_top, pen)

        # Left-bottom horizontal line
        self.scene.addLine(x_left_start, y_bottom, x_left_end, y_bottom, pen)

        # Right-top horizontal line
        self.scene.addLine(x_right_start, y_top, x_right_end, y_top, pen)

        # Right-bottom horizontal line
        self.scene.addLine(x_right_start, y_bottom, x_right_end, y_bottom, pen)
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        offset_len = 25  # 25mm offset for both lines

# Coordinates for the top-left corner of the left plate
        pen = QPen(Qt.black, 2)
        pen2=QPen(Qt.black, 1)
        brush = QBrush(Qt.NoBrush)
        half_thick = stiffener_thickness / 2.0
        # === TOP LEFT ===
        x1, y1 = start_x, start_y
        x2, y2 = start_x - offset_len, start_y
        x3, y3 = start_x - stiffener_width, start_y + stiffener_height - offset_len
        x4, y4 = start_x - stiffener_width, start_y + stiffener_height
        x5, y5 = start_x, start_y + stiffener_height
        points_tl = [QPointF(x1, y1), QPointF(x2, y2), QPointF(x3, y3), QPointF(x4, y4), QPointF(x5, y5)]
        polygon_tl = QGraphicsPolygonItem(QPolygonF(points_tl))
        polygon_tl.setPen(pen)
        polygon_tl.setBrush(brush)
        self.scene.addItem(polygon_tl)
        # Red cap
        x6, y6 = x5, y5 - half_thick
        x7, y7 = x4, y4 - half_thick
        polygon_tl = QGraphicsPolygonItem(QPolygonF([QPointF(x4, y4), QPointF(x5, y5), QPointF(x6, y6), QPointF(x7, y7)]))
        polygon_tl.setPen(pen)
        polygon_tl.setBrush(red_brush)
        self.scene.addItem(polygon_tl)
        # === BOTTOM LEFT ===
        x1, y1 = start_x, start_y + plate_height
        x2, y2 = start_x - offset_len, start_y + plate_height
        x3, y3 = start_x - stiffener_width, start_y + plate_height - stiffener_height + offset_len
        x4, y4 = start_x - stiffener_width, start_y + plate_height - stiffener_height
        x5, y5 = start_x, start_y + plate_height - stiffener_height
        points_bl = [QPointF(x1, y1), QPointF(x2, y2), QPointF(x3, y3), QPointF(x4, y4), QPointF(x5, y5)]
        polygon_bl = QGraphicsPolygonItem(QPolygonF(points_bl))
        polygon_bl.setPen(pen)
        polygon_bl.setBrush(brush)
        self.scene.addItem(polygon_bl)
        # Red cap
        x6, y6 = x5, y5 + half_thick
        x7, y7 = x4, y4 + half_thick
        polygon_tl = QGraphicsPolygonItem(QPolygonF([QPointF(x4, y4), QPointF(x5, y5), QPointF(x6, y6), QPointF(x7, y7)]))
        polygon_tl.setPen(pen)
        polygon_tl.setBrush(red_brush)
        self.scene.addItem(polygon_tl)
        # === TOP RIGHT ===
        x1, y1 = start_x + 2 * plate_thickness, start_y
        x2, y2 = x1 + offset_len, start_y
        x3, y3 = x1 + stiffener_width, start_y + stiffener_height - offset_len
        x4, y4 = x1 + stiffener_width, start_y + stiffener_height
        x5, y5 = x1, start_y + stiffener_height
        points_tr = [QPointF(x1, y1), QPointF(x2, y2), QPointF(x3, y3), QPointF(x4, y4), QPointF(x5, y5)]
        polygon_tr = QGraphicsPolygonItem(QPolygonF(points_tr))
        polygon_tr.setPen(pen)
        polygon_tr.setBrush(brush)
        self.scene.addItem(polygon_tr)
        # Red cap
        x6, y6 = x5, y5 - half_thick
        x7, y7 = x4, y4 - half_thick
        polygon_tl = QGraphicsPolygonItem(QPolygonF([QPointF(x4, y4), QPointF(x5, y5), QPointF(x6, y6), QPointF(x7, y7)]))
        polygon_tl.setPen(pen)
        polygon_tl.setBrush(red_brush)
        self.scene.addItem(polygon_tl)
        # === BOTTOM RIGHT ===
        x1, y1 = start_x + 2 * plate_thickness, start_y + plate_height
        x2, y2 = x1 + offset_len, y1
        x3, y3 = x1 + stiffener_width, start_y + plate_height - stiffener_height + offset_len
        x4, y4 = x1 + stiffener_width, start_y + plate_height - stiffener_height
        x5, y5 = x1, start_y + plate_height - stiffener_height
        points_br = [QPointF(x1, y1), QPointF(x2, y2), QPointF(x3, y3), QPointF(x4, y4), QPointF(x5, y5)]
        polygon_br = QGraphicsPolygonItem(QPolygonF(points_br))
        polygon_br.setPen(pen)
        polygon_br.setBrush(brush)
        self.scene.addItem(polygon_br)
        # Red cap
        x6, y6 = x5, y5 + half_thick
        x7, y7 = x4, y4 + half_thick
        polygon_tl = QGraphicsPolygonItem(QPolygonF([QPointF(x4, y4), QPointF(x5, y5), QPointF(x6, y6), QPointF(x7, y7)]))
        polygon_tl.setPen(pen)
        polygon_tl.setBrush(red_brush)
        self.scene.addItem(polygon_tl)
        self.addHorizontalDimension(start_x,start_y-40,start_x-stiffener_width,start_y-40,str(stiffener_width),blackpen)
        xpos=start_x +2*plate_thickness +stiffener_width+20
        self.addVerticalDimension(xpos,start_y,xpos,start_y+stiffener_height,str(stiffener_height),blackpen)
        
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
        font.setPointSize(10)
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
        font.setPointSize(10)
        text_item.setFont(font)
        
        if x1 < 0:
            text_item.setPos(x1 - 10 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1 + 15, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)