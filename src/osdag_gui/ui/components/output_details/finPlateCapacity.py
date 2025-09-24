import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView,
                             QGraphicsScene)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtGui import QPolygonF, QBrush
from PySide6.QtCore import QPointF
from osdag_core.Common import *

class FinPlateCapacityDetails(QMainWindow):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        super().__init__()
        self.connection = connection_obj
        self.main=main
        self.plate_height = main.plate.height
        self.plate_width = main.plate.length 
        self.hole_dia=main.bolt.bolt_diameter_provided
        self.rows=main.plate.bolts_one_line
        self.cols=main.plate.bolt_line
        self.plate_thickness=main.plate.thickness
        print(self.plate_height,self.plate_width)
        output=main.output_values(main,True)
        dict1={i[0] : i[3] for i in output}

        capacity_fnc = dict1['button1'][1]
        print(capacity_fnc)
        capacity_details = capacity_fnc(main,True)
        print(capacity_details)
        details_dict={i[1]:i[3] for i in capacity_details}
        
        self.shear_yield_capacity=float(details_dict['Shear Yielding Capacity (kN)'])
        self.rupture_capacity=float(details_dict['Rupture Capacity (kN)'])
        self.Block_Shear_Capacity=float(details_dict['Block Shear Capacity (kN)'])
        self.Tension_Yielding_Capacity=float(details_dict['Tension Yielding Capacity (kN)'])
        self.Tension_rupture_Capacity=float(details_dict['Tension Rupture Capacity (kN)'])
        self.axial_block_shear_capacity=float(details_dict['Axial Block Shear Capacity (kN)'])
        self.moment_demand=float(details_dict['Moment Demand (kNm)'])
        self.moment_capacity=float(details_dict['Moment Capacity (kNm)'])
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("------------------------------------------------------------------")
        self.dict_shear_failure={
            'Shear Yielding Capacity (kN)':self.shear_yield_capacity,
            'Rupture Capacity (kN)':self.rupture_capacity,
            'Block Shear Capacity (kN)':self.Block_Shear_Capacity
        }
        self.dict_tension_failure={
            'Tension Yielding Capacity (kN)':self.Tension_Yielding_Capacity,
            'Tension Rupture Capacity (kN)':self.Tension_rupture_Capacity,
            'Axial Block Shear Capacity (kN)':self.axial_block_shear_capacity
        }
        self.dict_section_3={
            'Moment Demand (kNm)':self.moment_demand,
            'Moment Capacity (kNm)':self.moment_capacity
        }

        print(self.dict_shear_failure)
        print(self.dict_tension_failure)
        print(self.dict_section_3)
        print("------------------------------------------------------------------")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        
        for i in output:
            print(i)
        self.weldsize=0
        if 'Weld.Size' in dict1:
            self.weldsize=dict1['Weld.Size']
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        self.setGeometry(100, 100, 1650, 1050)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel for parameter display
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Parameter display labels
        params = self.get_parameters()
        
        heading_label = QLabel("Note: Representative image for Failure Pattern (Half Plate)- 2 x 3 Bolts pattern considered")
        heading_label.setStyleSheet("font-size: 20px;")
        left_layout.addWidget(heading_label)

        space_label=QLabel("  ")
        space_label.setStyleSheet("font-size: 25px;")
        left_layout.addWidget(space_label)
        
        sub_heading_label1 = QLabel("Failure Pattern due to Shear in Plate")
        sub_heading_label1.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(sub_heading_label1)

        space_label=QLabel("  ")
        space_label.setStyleSheet("font-size: 15px;")
        left_layout.addWidget(space_label)

        # Display the parameter values
        for key, value in self.dict_shear_failure.items():
            param_layout = QHBoxLayout()
            param_label = QLabel(key.title())
            value_label = QLabel(f'{value}')
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            left_layout.addLayout(param_layout)

            space_label=QLabel("  ")
            space_label.setStyleSheet("font-size: 5px;")
            left_layout.addWidget(space_label)

        space_label=QLabel("  ")
        space_label.setStyleSheet("font-size: 25px;")
        left_layout.addWidget(space_label)

        sub_heading_label2 = QLabel("Failure Pattern due to Tension in Plate")
        sub_heading_label2.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(sub_heading_label2)

        space_label=QLabel("  ")
        space_label.setStyleSheet("font-size: 15px;")
        left_layout.addWidget(space_label)

        for key, value in self.dict_tension_failure.items():
            param_layout = QHBoxLayout()
            param_label = QLabel(key.title())
            value_label = QLabel(f'{value}')
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            left_layout.addLayout(param_layout)

            space_label=QLabel("  ")
            space_label.setStyleSheet("font-size: 5px;")
            left_layout.addWidget(space_label)

        space_label=QLabel("  ")
        space_label.setStyleSheet("font-size: 25px;")
        left_layout.addWidget(space_label)

        sub_heading_label3 = QLabel("Section 3")
        sub_heading_label3.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(sub_heading_label3)

        space_label=QLabel("  ")
        space_label.setStyleSheet("font-size: 15px;")
        left_layout.addWidget(space_label)

        for key, value in self.dict_section_3.items():
            param_layout = QHBoxLayout()
            param_label = QLabel(key.title())
            value_label = QLabel(f'{value}')
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            left_layout.addLayout(param_layout)
            space_label=QLabel("  ")
            space_label.setStyleSheet("font-size: 5px;")
            left_layout.addWidget(space_label)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Right panel for the two vertical drawings
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        sub_heading_label1 = QLabel("Failure Pattern due to Shear in Plate:")
        sub_heading_label1.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(sub_heading_label1)

        # First drawing
        self.scene1 = QGraphicsScene()
        self.view1 = QGraphicsView(self.scene1)
        self.view1.setRenderHint(QPainter.Antialiasing)
        self.createDrawing(self.scene1)
        self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
        right_layout.addWidget(self.view1)


        space_label=QLabel("  ")
        space_label.setStyleSheet("font-size: 15px;")
        right_layout.addWidget(space_label)

        sub_heading_label2 = QLabel("Failure Pattern due to Tension in Plate:")
        sub_heading_label2.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(sub_heading_label2)

        # Second drawing (identical to first)
        self.scene2 = QGraphicsScene()
        self.view2 = QGraphicsView(self.scene2)
        self.view2.setRenderHint(QPainter.Antialiasing)
        self.createSecondDrawing(self.scene2)  # Using the same drawing function
        self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
        right_layout.addWidget(self.view2)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)
        
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def get_parameters(self):
        spacing_data = self.connection.spacing(status=True)  # Get actual values
        param_map = {}
        print('spacing_data length' , len(spacing_data))
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
        param_map['hole'] = self.main.bolt.bolt_diameter_provided

        print("Extracted parameters:", param_map)
        return param_map


# failure due to shear in plate   
    def createDrawing(self, scene):
        coeff = 2  # scaling coefficient
        params = self.get_parameters()
        pitch = params['pitch'] / coeff
        end = params['end'] / coeff
        if 'gauge' in params:
            gauge1 = gauge2 = params['gauge'] / coeff
        else:
            gauge1 = params['gauge1'] / coeff
            gauge2 = params['gauge2'] / coeff
        edge = params['edge'] / coeff
        width = self.plate_width / coeff
        height = self.plate_height / coeff
        hole_diameter = params['hole'] / coeff
        weld_size = self.weldsize / coeff

        outline_pen = QPen(Qt.blue, 2/coeff)
        dimension_pen = QPen(Qt.black, 1.5/coeff)
        red_brush = QBrush(Qt.red)
        
        # Create dashed pen for failure patterns
        dashed_pen = QPen(Qt.black, 1.5/coeff, Qt.DashLine)
    
        
        
        h_offset = 40 / coeff
        v_offset = 60 / coeff
        scene.setSceneRect(-h_offset, -v_offset, width + 2*v_offset, height + 2*h_offset)
        #adding the shear failure pattern
        scene.addLine(width-end, 0, width-end, height-edge, dashed_pen)
        scene.addLine(0, height-edge, width-end, height-edge, dashed_pen)
        scene.addRect(0, 0, width, height, dimension_pen)

        # Draw holes
        for row in range(self.rows):
            for col in range(self.cols):
                x_center = width - edge
                for i in range(col):
                    x_center -= gauge1 if i % 2 == 0 else gauge2
                y_center = end + row * pitch
                x = x_center - hole_diameter / 2
                y = y_center - hole_diameter / 2
                scene.addEllipse(x, y, hole_diameter, hole_diameter, outline_pen)
        # Draw weld area
        if weld_size > 0:
            scene.addRect(0, 0, weld_size, height, dimension_pen, red_brush)
        # Add dimensions
        self.addDimensions(scene, width, height, pitch, end, gauge1, gauge2, edge, dimension_pen, coeff)


    def createSecondDrawing(self, scene):
        coeff = 2  # scaling coefficient
        params = self.get_parameters()
        pitch = params['pitch'] / coeff
        end = params['end'] / coeff
        if 'gauge' in params:
            gauge1 = gauge2 = params['gauge'] / coeff
        else:
            gauge1 = params['gauge1'] / coeff
            gauge2 = params['gauge2'] / coeff
        edge = params['edge'] / coeff
        width = self.plate_width / coeff
        height = self.plate_height / coeff
        hole_diameter = params['hole'] / coeff
        weld_size = self.weldsize / coeff

        outline_pen = QPen(Qt.blue, 2/coeff)
        dimension_pen = QPen(Qt.black, 1.5/coeff)
        red_brush = QBrush(Qt.red)

        # Create dashed pen for failure patterns
        dashed_pen = QPen(Qt.black, 1.5/coeff, Qt.DashLine)

        


        if self.cols==1:
            x_line_dist=width-end
        else:
            x_line_dist=width-end - (self.cols-1)*gauge1

        h_offset = 40 / coeff
        v_offset = 60 / coeff
        scene.setSceneRect(-h_offset, -v_offset, width + 2*v_offset, height + 2*h_offset)
        #adding the tension failure pattern
        scene.addLine(x_line_dist, edge, width, edge, dashed_pen)
        scene.addLine(x_line_dist, edge, x_line_dist, height-edge, dashed_pen)
        scene.addLine(x_line_dist, height-edge, width, height-edge, dashed_pen)
        scene.addRect(0, 0, width, height, dimension_pen)

        
        # Draw holes
        for row in range(self.rows):
            for col in range(self.cols):
                x_center = width - edge
                for i in range(col):
                    x_center -= gauge1 if i % 2 == 0 else gauge2
                y_center = end + row * pitch
                x = x_center - hole_diameter / 2
                y = y_center - hole_diameter / 2
                scene.addEllipse(x, y, hole_diameter, hole_diameter, outline_pen)
        # Draw weld area
        if weld_size > 0:
            scene.addRect(0, 0, weld_size, height, dimension_pen, red_brush)
        # Add dimensions
        self.addDimensions(scene, width, height, pitch, end, gauge1, gauge2, edge, dimension_pen, coeff)



    def addDimensions(self, scene, width, height, pitch, end, gauge1, gauge2, edge, pen, coeff):
        h_offset = 20 / coeff
        v_offset = 30 / coeff
        x_start = width
        segments = []
        segments.append(('edge', x_start-edge, x_start))
        x_start -= edge
        segments.append(('edge', 0, x_start))
        for label, x1, x2 in segments:
            value = x2 - x1
            self.addHorizontalDimension(scene, x1, -h_offset, x2, -h_offset, f"{value:.1f}", pen)
        # Add vertical dimensions
        self.addVerticalDimension(scene, width + v_offset, 0, width + v_offset, end, str(end), pen)
        for i in range(self.rows - 1):
            self.addVerticalDimension(scene, width + v_offset, end + i * pitch, 
                                     width + v_offset, end + (i + 1) * pitch, str(pitch), pen)
        self.addVerticalDimension(scene, width + v_offset, height, width + v_offset, height - end, str(end), pen)
        total_height = 2 * end + (self.rows - 1) * pitch
        self.addVerticalDimension(scene, -v_offset, 0, -v_offset, total_height, str(total_height), pen)

    def addHorizontalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 2
        ext_length = 10
        scene.addLine(x1, y1 - ext_length/2, x1, y1 + ext_length/2, pen)
        scene.addLine(x2, y2 - ext_length/2, x2, y2 + ext_length/2, pen)
        
        points_left = [
            (x1, y1),
            (x1 + arrow_size, y1 - arrow_size/2),
            (x1 + arrow_size, y1 + arrow_size/2)
        ]
        polygon_left = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_left]), pen)
        polygon_left.setBrush(QBrush(Qt.black))
        
        points_right = [
            (x2, y2),
            (x2 - arrow_size, y2 - arrow_size/2),
            (x2 - arrow_size, y2 + arrow_size/2)
        ]
        polygon_right = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_right]), pen)
        polygon_right.setBrush(QBrush(Qt.black))
        
        text_item = scene.addText(text)
        font = QFont()
        font.setPointSize(2)
        text_item.setFont(font)
        
        if y1 < 0:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 25)
        else:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 + 5)

    def addVerticalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 2
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
            polygon_top.setBrush(QBrush(Qt.black))
            
            points_bottom = [
                (x2, y2),
                (x2 - arrow_size/2, y2 - arrow_size),
                (x2 + arrow_size/2, y2 - arrow_size)
            ]
            polygon_bottom = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            polygon_bottom.setBrush(QBrush(Qt.black))
        else:
            points_top = [
                (x2, y2),
                (x2 - arrow_size/2, y2 + arrow_size),
                (x2 + arrow_size/2, y2 + arrow_size)
            ]
            polygon_top = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_top]), pen)
            polygon_top.setBrush(QBrush(Qt.black))
            
            points_bottom = [
                (x1, y1),
                (x1 - arrow_size/2, y1 - arrow_size),
                (x1 + arrow_size/2, y1 - arrow_size)
            ]
            polygon_bottom = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen)
            polygon_bottom.setBrush(QBrush(Qt.black))
        
        text_item = scene.addText(text)
        font = QFont()
        font.setPointSize(2)
        text_item.setFont(font)
        
        if x1 < 0:
            text_item.setPos(x1 - 10 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1 + 15, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)