import sys
from PySide6.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
                             QGraphicsScene, QGraphicsRectItem)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtGui import QPolygonF, QBrush
from PySide6.QtCore import QPointF
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *

class B2BCoverPlateDetails(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        # print(main)
        
        if main:
            web=main[1]
            main=main[0]
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager
        self.connection = connection_obj
        # return
        data=main.output_values(True)
        # print(type(main))
        dict1={i[0] : i[3] for i in data}


        # print("________________________DEBUG________________________")
        # print(dict1)
        # print("________________________DEBUG________________________")

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
            bolt_cap=bolt_cap(True)
        elif web==False:
            self.plate_length=dict1['Flange_Plate.Width (mm)']
            self.plate_width=dict1['flange_plate.Length']
            self.bolt_diameter=dict1['Bolt.Diameter']
            flange_capcity=dict1['Flange_plate.spacing'][1]
            data2=flange_capcity(True)
            self.pitch=data2[2][3]
            self.End=data2[3][3]
            self.Gauge=data2[4][3]
            self.Edge=data2[5][3]
            bolt_cap=dict1['Bolt.Capacities'][1]
            print(bolt_cap(True))
            bolt_cap=bolt_cap(True)
        self.cols=bolt_cap[1][3]
        self.rows=bolt_cap[2][3]/self.cols
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
        width, height = 800, 500
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

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
        
        if self.theme.is_light():
            self.view.setBackgroundBrush(QBrush(Qt.white))
        else:
            self.view.setBackgroundBrush(QBrush(QColor("#4A4A4A")))

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

        self.content_widget.setLayout(main_layout)

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
        if self.theme.is_light():
            pen = QPen(Qt.black)
        else:
            pen = QPen(QColor("#8A8A8A"))
        pen.setWidth(2)
        rect_item.setPen(pen)
        rect_item.setBrush(QBrush(Qt.NoBrush))

        # Add rectangle to the scene
        self.scene.addItem(rect_item)
        # Extract parameters
        if self.theme.is_light():
            outline_pen = QPen(Qt.black)
        else:
            outline_pen = QPen(QColor("#8A8A8A"))
        outline_pen.setWidth(1)
        
        # === Draw Base Plate Rectangle ===
        rect_item = QGraphicsRectItem(QRectF(0, 0, plate_length, plate_width))
        rect_item.setPen(outline_pen)
        if self.theme.is_light():
            rect_item.setBrush(QBrush(Qt.white))
        else:
            rect_item.setBrush(QBrush(QColor("#4A4A4A")))
        self.scene.addItem(rect_item)
        # === Center of the base plate ===
        center_x = plate_length / 2
        center_y = plate_width / 2
        self.addHorizontalDimension(
            0, -30,  # x1 at left edge, y above plate
            self.plate_length, -30,  # x2 at right edge, same y
            f"{self.plate_length} mm", pen
        )

        # Vertical dimension for plate width (to the right of the plate)
        self.addVerticalDimension(
            self.plate_length+30, 0,  # x right of plate, y1 at top
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
        
        # Collect all bolt x and y positions for dimensions
        bolt_x_positions = []
        bolt_y_positions = []
        
        if rows % 2 != 0:
            y_center = self.plate_width / 2
            bolt_y_positions.append(y_center)
            for i in range(cols // 2):
                x_center = edge + i * gauge
                bolt_x_positions.append(x_center)
                self.scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

            for i in range(cols // 2):
                x_center = self.plate_length - edge - i * gauge
                bolt_x_positions.append(x_center)
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
                bolt_x_positions.append(x_center)
                self.scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

        # Center column if cols is odd (and rows is even)
        if cols % 2 != 0 and rows % 2 == 0:
            x_center = self.plate_length / 2
            bolt_x_positions.append(x_center)
            for j in range(rows // 2):
                y_center_top = end + j * pitch
                y_center_bottom = self.plate_width - end - j * pitch
                
                bolt_y_positions.append(y_center_top)
                bolt_y_positions.append(y_center_bottom)

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

        # Draw left half bolts and right half bolts
        for row in range(int(rows)):
            if row < rows // 2:
                y_center = end + row * pitch
            else:
                row_from_bottom = row - rows // 2
                y_center = self.plate_width - end - row_from_bottom * pitch
            
            bolt_y_positions.append(y_center)

            # Left half bolts
            for i in range(cols // 2):
                x_center = edge + i * gauge
                bolt_x_positions.append(x_center)
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
                bolt_x_positions.append(x_center)
                self.scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )
        
        # Remove duplicates and sort positions
        bolt_x_positions = sorted(list(set(bolt_x_positions)))
        bolt_y_positions = sorted(list(set(bolt_y_positions)))
        
        # Horizontal dimensions at bottom (left edge → bolts → right edge)
        h_dim_y = self.plate_width + 30
        x_positions = [0] + bolt_x_positions + [self.plate_length]
        
        for i in range(len(x_positions) - 1):
            x1 = x_positions[i]
            x2 = x_positions[i + 1]
            distance = abs(x2 - x1)
            self.addHorizontalDimension(x1, h_dim_y, x2, h_dim_y, f"{distance:.1f}", pen)
        
        # Vertical dimensions at left (top edge → bolts → bottom edge)
        v_dim_x = -30
        y_positions = [0] + bolt_y_positions + [self.plate_width]
        
        for i in range(len(y_positions) - 1):
            y1 = y_positions[i]
            y2 = y_positions[i + 1]
            distance = abs(y2 - y1)
            self.addVerticalDimension(v_dim_x, y1, v_dim_x, y2, f"{distance:.1f}", pen)
            
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
            polygon_right.setBrush(QBrush(Qt.black))
        else:
            polygon_right.setBrush(QBrush(QColor("#8A8A8A")))
        
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(int(self.fontsize))
        text_item.setFont(font)
        if self.theme.is_light():
            text_item.setDefaultTextColor(Qt.black)
        else:
            text_item.setDefaultTextColor(Qt.white)
        
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
        font.setPointSize(int(self.fontsize))
        text_item.setFont(font)
        if self.theme.is_light():
            text_item.setDefaultTextColor(Qt.black)
        else:
            text_item.setDefaultTextColor(Qt.white)
        
        if x1 < 0:
            text_item.setPos(x1 - 10 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1 + 15, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)