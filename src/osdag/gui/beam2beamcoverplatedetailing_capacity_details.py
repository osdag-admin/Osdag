import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView,
                             QGraphicsScene,QGraphicsRectItem, QFrame)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtGui import QPolygonF, QBrush
from PyQt5.QtCore import QPointF
from ..Common import *
from .additionalfns import calculate_total_width

try:
    pen_style_dash = Qt.PenStyle.DashLine
except AttributeError:
    raise RuntimeError("Your PyQt5 version does not support dashed lines via Qt.PenStyle.DashLine. Please update PyQt5.")

class B2Bcoverplate_capacity_details(QMainWindow):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        print(main)
        
        if main:
            self.drawing_type=main[2]
            self.web=main[1]
            web=main[1]
            main=main[0]
        super().__init__()
        self.connection = connection_obj
        # return
        data=main.output_values(main,True)
        print(type(main))
        dict1={i[0] : i[3] for i in data}

        
        
        for i in dict1:
            print(f'{i} : {dict1[i]}')


        if web==True:
            self.plate_length=dict1['Web_Plate.Height (mm)']
            self.plate_width=dict1['Web_Plate.Width']
            self.bolt_diameter=dict1['Bolt.Diameter']
            web_capcity=dict1['Web_plate.spacing'][1]
            print(web_capcity(main,True))
            data2=web_capcity(main,True)
            for i in range(len(data2)):
                print(f"{i} : {data2[i]}")
            self.pitch=data2[2][3]
            self.End=data2[3][3]
            self.Gauge=data2[4][3]
            self.Edge=data2[5][3]
            bolt_cap=dict1['Web Bolt.Capacities'][1]
            print(bolt_cap(main,True))
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
    


        #capacity
        if web==True and self.drawing_type=="capacity":
            #web capacity details
            web_capacity_fnc=dict1['section.web_capacities'][1]
            web_capacity_val=web_capacity_fnc(main,True)
            self.web_capacity_details = {item[1]: float(item[3]) for item in web_capacity_val if item[2] == 'TextBox'}
                
        #capacity
        elif web==False and self.drawing_type=="capacity":
            #flange capacity details
            flange_capacity_fnc=dict1['section.flange_capacity'][1]
            flange_capacity_val=flange_capacity_fnc(main,True)
            self.flange_capacity_details={item[1]: float(item[3]) for item in flange_capacity_val if item[2] == 'TextBox'}




        self.cols=bolt_cap[1][3]
        self.rows=bolt_cap[2][3]/self.cols
        self.initUI()

        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        self.setGeometry(100, 100, 1050, 500)

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
        params = self.get_parameters((self.web,self.drawing_type))
        count=0
        for key, value in params.items():
            if self.web==False and self.drawing_type=="capacity":
                param_layout = QHBoxLayout()
                space_label = QLabel('  ')
                param_label = QLabel(f'{key.title()} (mm):')
                value_label = QLabel(f'{value}')
                param_layout.addWidget(param_label)
                param_layout.addWidget(value_label)
                left_layout.addLayout(param_layout)
                # Add a blank label for vertical spacing
                left_layout.addWidget(QLabel(''))
            elif self.web==True and self.drawing_type=="capacity":
                param_layout = QHBoxLayout()
                space_label = QLabel('  ')
                param_label = QLabel(f'{key.title()} (mm):')
                value_label = QLabel(f'{value}')
                param_layout.addWidget(param_label)
                param_layout.addWidget(value_label)
                left_layout.addLayout(param_layout)
                # Add a blank label for vertical spacing
                left_layout.addWidget(QLabel(''))

                count+=1
            else:
                param_layout = QHBoxLayout()
                param_label = QLabel(f'{key.title()} (mm):')
                value_label = QLabel(f'{value}')
                param_layout.addWidget(param_label)
                param_layout.addWidget(value_label)
                left_layout.addLayout(param_layout)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # Determine font and arrow size based on plate size
        self.fontsize = 10
        self.arrowsize = 10
        if self.plate_length > 1200 or self.plate_width > 1200:
            self.fontsize = 12
            self.arrowsize = 12
        elif self.plate_length > 600 or self.plate_width > 600:
            self.fontsize = 7.5
            self.arrowsize = 7.5

        if self.web == True and self.drawing_type == "capacity":
            # Two drawings, each with its own parameter set, separated by a horizontal line
            self.scene1 = QGraphicsScene()
            self.view1 = QGraphicsView(self.scene1)
            self.view1.setRenderHint(QPainter.Antialiasing)

            self.scene2 = QGraphicsScene()
            self.view2 = QGraphicsView(self.scene2)
            self.view2.setRenderHint(QPainter.Antialiasing)

            self.createDrawing((self.web, self.drawing_type), self.scene1)
            self.createDrawing((self.web, self.drawing_type), self.scene2)

            if self.plate_length > 1200 or self.plate_width > 1200:
                self.view1.resetTransform()
                self.view1.scale(0.35, 0.35)
                self.view2.resetTransform()
                self.view2.scale(0.35, 0.35)
            elif self.plate_length > 600 or self.plate_width > 600:
                self.view1.resetTransform()
                self.view1.scale(0.5, 0.5)
                self.view2.resetTransform()
                self.view2.scale(0.5, 0.5)

            # Split parameters into two groups (first two, next two)
            params = list(self.get_parameters((self.web, self.drawing_type)).items())
            params1 = params[:2]
            params2 = params[2:]

            # Section 1: first two parameters and first drawing
            section1_layout = QHBoxLayout()
            section1_text_widget = QWidget()
            section1_text_layout = QVBoxLayout(section1_text_widget)
            param_label = QLabel('Failure Pattern due to tension in Member and Plate')
            param_label.setFont(QFont('Arial',12,QFont.Bold))
            section1_text_layout.addWidget(param_label)
            for key, value in params1:
                param_label = QLabel(f'{key}: {value}')
                section1_text_layout.addWidget(param_label)
            section1_text_layout.addStretch()
            section1_text_widget.setMinimumWidth(180)
            section1_layout.addWidget(section1_text_widget, 1)
            section1_layout.addWidget(self.view1, 2)

            # Section 2: next two parameters and second drawing
            section2_layout = QHBoxLayout()
            section2_text_widget = QWidget()
            section2_text_layout = QVBoxLayout(section2_text_widget)
            param_label = QLabel('Failure Pattern due to tension in Member and Plate')
            param_label.setFont(QFont('Arial',12,QFont.Bold))
            section2_text_layout.addWidget(param_label)
            for key, value in params2:
                param_label = QLabel(f'{key}: {value}')
                section2_text_layout.addWidget(param_label)
            section2_text_layout.addStretch()
            section2_text_widget.setMinimumWidth(180)
            section2_layout.addWidget(section2_text_widget, 1)
            section2_layout.addWidget(self.view2, 2)

            # Horizontal line between sections
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)

            # Main vertical layout
            main_vlayout = QVBoxLayout()
            main_vlayout.addLayout(section1_layout)
            main_vlayout.addWidget(line)
            main_vlayout.addLayout(section2_layout)

            self.view1.setMaximumWidth(400)
            self.view2.setMaximumWidth(400)

            main_widget = QWidget()
            main_widget.setLayout(main_vlayout)
            self.setCentralWidget(main_widget)
        else:
            # Only one drawing (original layout)
            left_panel = QWidget()
            left_layout = QVBoxLayout()
            params = self.get_parameters((self.web, self.drawing_type))
            for key, value in params.items():
                if self.web==False and self.drawing_type=="capacity":
                    param_layout = QHBoxLayout()
                    space_label = QLabel('  ')
                    param_label = QLabel(f'{key.title()} (mm):')
                    value_label = QLabel(f'{value}')
                    param_layout.addWidget(param_label)
                    param_layout.addWidget(value_label)
                    left_layout.addLayout(param_layout)
                    left_layout.addWidget(QLabel(''))
                else:
                    param_layout = QHBoxLayout()
                    param_label = QLabel(f'{key.title()} (mm):')
                    value_label = QLabel(f'{value}')
                    param_layout.addWidget(param_label)
                    param_layout.addWidget(value_label)
                    left_layout.addLayout(param_layout)
            left_layout.addStretch()
            left_panel.setLayout(left_layout)

            self.scene = QGraphicsScene()
            self.view = QGraphicsView(self.scene)
            self.view.setRenderHint(QPainter.Antialiasing)
            self.createDrawing((self.web, self.drawing_type), self.scene)

            if self.plate_length > 1200 or self.plate_width > 1200:
                self.view.resetTransform()
                self.view.scale(0.35, 0.35)
            elif self.plate_length > 600 or self.plate_width > 600:
                self.view.resetTransform()
                self.view.scale(0.5, 0.5)

            main_layout = QHBoxLayout()
            main_layout.addWidget(left_panel, 1)
            main_layout.addWidget(self.view, 3)
            main_widget = QWidget()
            main_widget.setLayout(main_layout)
            self.setCentralWidget(main_widget)

        # Automatically adjust view to fit scene
    def get_parameters(self,type_):
        if (type_[0]==True and type_[1]=="spacing") or (type_[0]==False and type_[1]=="spacing") :
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
        elif type_[0]==True and type_[1]=="capacity":
            return self.web_capacity_details
        elif type_[0]==False and type_[1]=="capacity":
            return self.flange_capacity_details
        
    def createDrawing(self, type_, scene):

        
        
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
        pen = QPen(QColor('black'))
        pen.setWidth(2)
        rect_item.setPen(pen)
        rect_item.setBrush(QBrush())  # Default is NoBrush

        # Add rectangle to the scene
        scene.addItem(rect_item)
        
        
        # Extract parameters
        outline_pen = QPen(QColor('black'))
        outline_pen.setWidth(1)
        
        # === Draw Base Plate Rectangle ===
        rect_item = QGraphicsRectItem(QRectF(0, 0, plate_length, plate_width))
        rect_item.setPen(outline_pen)
        rect_item.setBrush(QBrush(QColor('white')))
        scene.addItem(rect_item)
        dashed_pen = QPen(QColor('black'))
        dashed_pen.setStyle(pen_style_dash)
        dashed_pen.setWidth(2)
        if type_[0]==False and type_[1]=="capacity":
            
            #top drawing
            scene.addLine(self.Edge, 0, self.Edge, self.End, dashed_pen)

            scene.addLine(self.Edge, self.End, plate_length, self.End, dashed_pen)


            #bottom drawing
            scene.addLine(self.Edge, plate_width, self.Edge, plate_width-self.End, dashed_pen)

            scene.addLine(self.Edge, plate_width-self.End, plate_length, plate_width-self.End, dashed_pen)
        
        elif type_[0]==True and type_[1]=="capacity" and scene==self.scene1:

            scene.addLine(self.End, self.Edge, self.End, plate_width-self.End, dashed_pen)

            scene.addLine(self.End, self.Edge, plate_length, self.Edge, dashed_pen)

            scene.addLine(self.End, plate_width-self.Edge, plate_length, plate_width-self.Edge, dashed_pen)

            
        elif type_[0]==True and type_[1]=="capacity" and scene==self.scene2:
        
            scene.addLine(0, self.Edge, plate_length-self.End, self.Edge, dashed_pen)

            scene.addLine(plate_length-self.End, self.Edge, plate_length-self.End, plate_width, dashed_pen)


        # === Center of the base plate ===
        center_x = plate_length / 2
        center_y = plate_width / 2
        self.addHorizontalDimension(
            0, -30,  # x1 at left edge, y above plate
            self.plate_length, -30,  # x2 at right edge, same y
            f"{self.plate_length} mm", pen, scene
        )

        # Vertical dimension for plate width (to the left of the plate)
        self.addVerticalDimension(
            self.plate_length+30, 0,  # x left of plate, y1 at top
            self.plate_length+30, self.plate_width,  # x2 same, y2 at bottom
            f"{self.plate_width} mm", pen, scene
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
        outline_pen = QPen(QColor('blue'))
        outline_pen.setWidth(1)
        if rows % 2 != 0:
            y_center = self.plate_width / 2
            for i in range(cols // 2):
                x_center = edge + i * gauge
                scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

            for i in range(cols // 2):
                x_center = self.plate_length - edge - i * gauge
                scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

            # Center bolt if cols is also odd
            if cols % 2 != 0:
                x_center = self.plate_length / 2
                scene.addEllipse(
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
                scene.addEllipse(
                    x_center - radius,
                    y_center_top - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )
                scene.addEllipse(
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
                scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )

            # Right half bolts
            for i in range(cols // 2):
                x_center = self.plate_length - edge - i * gauge
                scene.addEllipse(
                    x_center - radius,
                    y_center - radius,
                    hole_dia,
                    hole_dia,
                    outline_pen,
                )
        self.addHorizontalDimension(
            0, self.plate_width+10,  # x1 at left edge, y above plate
            self.Edge, self.plate_width+10,  # x2 at right edge, same y
            f"{self.Edge} mm", pen, scene
        )
        self.addVerticalDimension(
            -10, 0,  # x left of plate, y1 at top
            -10, self.End,  # x2 same, y2 at bottom
            f"{self.End} mm", pen, scene
        )
        # self.addHorizontalDimension(
        #     self.Edge-hole_dia/2, 10,  
        #     self.Edge+hole_dia/2,10, 
        #     f"{hole_dia} mm", pen
        # )
    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen, scene):
        scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = int(self.arrowsize)
        ext_length = 10
        scene.addLine(x1, y1 - ext_length/2, x1, y1 + ext_length/2, pen)
        scene.addLine(x2, y2 - ext_length/2, x2, y2 + ext_length/2, pen)
        
        points_left = [
            (x1, y1),
            (x1 + arrow_size, y1 - arrow_size/2),
            (x1 + arrow_size, y1 + arrow_size/2)
        ]
        polygon_left = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_left]), pen)
        polygon_left.setBrush(QBrush(QColor('black')))
        
        points_right = [
            (x2, y2),
            (x2 - arrow_size, y2 - arrow_size/2),
            (x2 - arrow_size, y2 + arrow_size/2)
        ]
        polygon_right = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_right]), pen)
        polygon_right.setBrush(QBrush(QColor('black')))
        
        text_item = scene.addText(text)
        font = QFont()
        font.setPointSize(int(self.fontsize))
        text_item.setFont(font)
        
        if y1 < 0:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 25)
        else:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 + 5)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen, scene):
        scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = int(self.arrowsize)
        ext_length = 10
        scene.addLine(x1 - ext_length/2, y1, x1 + ext_length/2, y1, pen)
        scene.addLine(x2 - ext_length/2, y2, x2 + ext_length/2, y2, pen)
        
        if y2 > y1:
            points_top = [
                (x1, y1),
                (x1 - arrow_size/2, y1 + arrow_size),
                (x1 + arrow_size/2, y1 + arrow_size)
            ]
            polygon_top = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
            polygon_top.setBrush(QBrush(QColor('black')))
            
            points_bottom = [
                (x2, y2),
                (x2 - arrow_size/2, y2 - arrow_size),
                (x2 + arrow_size/2, y2 - arrow_size)
            ]
            polygon_bottom = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            polygon_bottom.setBrush(QBrush(QColor('black')))
        else:
            points_top = [
                (x2, y2),
                (x2 - arrow_size/2, y2 + arrow_size),
                (x2 + arrow_size/2, y2 + arrow_size)
            ]
            polygon_top = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
            polygon_top.setBrush(QBrush(QColor('black')))
            
            points_bottom = [
                (x1, y1),
                (x1 - arrow_size/2, y1 - arrow_size),
                (x1 + arrow_size/2, y1 - arrow_size)
            ]
            polygon_bottom = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            polygon_bottom.setBrush(QBrush(QColor('black')))
        
        text_item = scene.addText(text)
        font = QFont()
        font.setPointSize(int(self.fontsize))
        text_item.setFont(font)
        
        if x1 < 0:
            text_item.setPos(x1 - 10 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1 + 15, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
