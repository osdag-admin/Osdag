import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView,
                             QGraphicsScene,QGraphicsRectItem)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtGui import QPolygonF, QBrush
from PyQt5.QtCore import QPointF
from ..Common import *
from .additionalfns import calculate_total_width
class BasePlateDetailing(QMainWindow):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        super().__init__()
        self.connection = connection_obj
        data=main.output_values(main,True)
        print(type(main))

        bp_width_provided=main.bp_width_provided
        column_bf=main.column_bf
        effective_length_flange=self.connection.effective_length_flange
        plate_thk_provided=main.plate_thk_provided
        column_tw=main.column_tw
        columnflange_tf=main.column_tf
        effective_length_web=self.connection.effective_length_web
        plate_thk_provided=main.plate_thk_provided
        column_D=main.column_D
        # print(data)
        print(f"""
        bp_width_provided: {bp_width_provided}
        column_bf: {column_bf}
        effective_length_flange: {effective_length_flange}
        plate_thk_provided: {plate_thk_provided}
        column_tw: {column_tw}\\column thickness
        effective_length_web: {effective_length_web}
        column_D:{column_D}
        col thickness : {columnflange_tf}
        """)
        # for i in data:
        #     print(i)
        self.column_len=column_D
        self.column_width=column_bf
        self.web_thickness=column_tw
        self.column_thickness=columnflange_tf
        self.detail_dict = {
                                f'{entry[1]} + {entry[0]}': entry[3]
                                for entry in data
                                }
        for i in self.detail_dict.keys():
            print(i)
        self.no_outsidebolts=self.detail_dict['No. of Anchors + Anchor Bolt.No of Anchor Bolts']
        self.dia_outside_bolt=self.detail_dict['Diameter (mm) + Anchor Bolt.Diameter']
        self.no_insidebolts=self.detail_dict['No. of Anchors + Anchor Bolt.No of Anchor Bolts_Uplift']
        self.dia_inside_bolt=self.detail_dict['Diameter (mm) + Anchor Bolt.Diameter_Uplift']
        self.plate_length=self.detail_dict['Length (mm) + Baseplate.Length']
        self.plate_width=self.detail_dict['Width (mm) + Baseplate.Width']
        self.Endout=self.detail_dict['End Distance (mm) + Detailing.EndDistanceOut']
        self.Edgeout=self.detail_dict['Edge Distance (mm) + Detailing.EdgeDistanceOut']
        self.pitchout=self.detail_dict['Pitch Distance (mm) + Detailing.PitchDistanceOut']
        self.Gaugeout=self.detail_dict['Gauge Distance (mm) + Detailing.GaugeDistanceOut']
        self.Endin=self.detail_dict['End Distance (mm) + Detailing.EndDistanceIn']
        self.Edgein=self.detail_dict['Edge Distance (mm) + Detailing.EdgeDistanceIn']
        self.pitchin=self.detail_dict['Pitch Distance (mm) + Detailing.PitchDistanceIn']
        self.Gaugein=self.detail_dict['Gauge Distance (mm) + Detailing.GaugeDistanceIn']
        
        stiffacrossdata=main.stiffener_across_web_details(main,True)

        stiffalongdata=main.stiffener_along_web_details(main,True)

        stiffflangedata=main.stiffener_flange_details(main,True)
        self.stiff_across_length=stiffacrossdata[0][3]
        self.stiff_across_thickness=stiffacrossdata[2][3]
        self.stiff_along_length=stiffalongdata[0][3]
        self.stiff_along_thickness=stiffalongdata[2][3]
        self.stiff_flange_length=stiffflangedata[0][3]
        self.stiff_flange_thickness=stiffflangedata[2][3]
        
        self.rows = rows
        self.cols = cols
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        print(f"""
        Base Plate & Bolt Details:
        --------------------------
        No. of Outside Bolts : {self.no_outsidebolts}
        Diameter Outside Bolt: {self.dia_outside_bolt}
        No. of Inside Bolts  : {self.no_insidebolts}
        Diameter Inside Bolt : {self.dia_inside_bolt}
        Base Plate Length     : {self.plate_length}
        Base Plate Width      : {self.plate_width}  
        End Distance          : {self.Endout}
        Edge Distance         : {self.Edgeout}

        Stiffener Plate Dimensions:
        ---------------------------
        Across Web - Length: {self.stiff_across_length}, Thickness: {self.stiff_across_thickness}
        Along Web  - Length: {self.stiff_along_length}, Thickness: {self.stiff_along_thickness}
        Flange     - Length: {self.stiff_flange_length}, Thickness: {self.stiff_flange_thickness}
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
            
        ]

        # Add labels

        # Step 4: Graphics view and scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        # Background and test shape (optional)
        self.scene.setBackgroundBrush(Qt.white)

        # Step 5: Add to main layout
        main_layout.addWidget(self.view, stretch=2)

        # Step 6: Call parameter extraction and drawing
        # self.get_parameters()
        self.createDrawing()
    def createDrawing(self):
        try:
            plate_length = float(self.plate_length)
            plate_width = float(self.plate_width)
        except (TypeError, ValueError):
            print("Invalid plate dimensions")
            return
        rect = QRectF(0, 0, plate_length, plate_width)
        column_len=self.column_len
        column_width=self.column_width
        flange_thickness=self.column_thickness
        web_thickness=self.web_thickness
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
        outline_pen = QPen(Qt.blue)
        outline_pen.setWidth(3)
        # === Center of the base plate ===
        center_x = plate_length / 2
        center_y = plate_width / 2
        web_top_y=center_y-web_thickness/2
        web_bot_y=center_y+web_thickness/2
        web_left_x=center_x-column_len/2
        web_right_x=center_x+column_len/2
        self.scene.addLine(web_left_x,web_top_y,web_right_x,web_top_y,outline_pen)
        self.scene.addLine(web_left_x,web_bot_y,web_right_x,web_bot_y,outline_pen)
        #LEFT FLANGE
        left_x=web_left_x-flange_thickness
        right_x=web_left_x
        top_y=center_y-column_width/2
        bot_y=center_y+column_width/2
        junctiontop_y=web_top_y
        junctionbot_y=web_bot_y
        #1
        self.scene.addLine(left_x,bot_y,left_x,top_y,outline_pen)
        self.scene.addLine(left_x,top_y,right_x,top_y,outline_pen)
        self.scene.addLine(right_x,top_y,right_x,junctiontop_y,outline_pen)
        self.scene.addLine(right_x,junctionbot_y,right_x,bot_y,outline_pen)
        self.scene.addLine(right_x,bot_y,left_x,bot_y,outline_pen)
        # === RIGHT FLANGE ===
        left_x = web_right_x                     # Inner edge (adjacent to web)
        right_x = web_right_x + flange_thickness  # Outer edge of flange
        top_y = center_y - column_width / 2
        bot_y = center_y + column_width / 2
        junctiontop_y = web_top_y
        junctionbot_y = web_bot_y

        # 1. Right vertical line
        self.scene.addLine(right_x, bot_y, right_x, top_y, outline_pen)

        # 2. Top horizontal line
        self.scene.addLine(right_x, top_y, left_x, top_y, outline_pen)

        # 3. Left vertical line (top segment above web)
        self.scene.addLine(left_x, top_y, left_x, junctiontop_y, outline_pen)

        # 4. Left vertical line (bottom segment below web)
        self.scene.addLine(left_x, junctionbot_y, left_x, bot_y, outline_pen)

        # 5. Bottom horizontal line
        self.scene.addLine(left_x, bot_y, right_x, bot_y, outline_pen)
        red_brush = QBrush(Qt.red)
        if isinstance(self.stiff_flange_length, (int, float)):
            print('her')
            stiff_thk = self.stiff_flange_thickness
            offset = (stiff_thk - flange_thickness) / 2

            # === Left Flange Stiffeners ===
            # Top stiffener (left)
            left_x=web_left_x-flange_thickness
            stiffener_left_top = QRectF(
                left_x - offset,     # shift outward from flange face
                0,                   # top of plate
                stiff_thk,
                top_y                # height to top of flange
            )
            self.scene.addRect(stiffener_left_top, outline_pen, red_brush)

            # Bottom stiffener (left)
            stiffener_left_bottom = QRectF(
                left_x - offset,
                bot_y,               # just below bottom of flange
                stiff_thk,
                plate_width - bot_y  # height from flange to bottom of plate
            )
            self.scene.addRect(stiffener_left_bottom, outline_pen, red_brush)
            left_x=web_left_x-flange_thickness
            # === Right Flange Stiffeners ===
            # Top stiffener (right)
            stiffener_right_top = QRectF(
                right_x - flange_thickness - offset,
                0,
                stiff_thk,
                top_y
            )
            self.scene.addRect(stiffener_right_top, outline_pen, red_brush)

            # Bottom stiffener (right)
            stiffener_right_bottom = QRectF(
                right_x - flange_thickness - offset,
                bot_y,
                stiff_thk,
                plate_width - bot_y
            )
            self.scene.addRect(stiffener_right_bottom, outline_pen, red_brush)
        if isinstance(self.stiff_along_thickness, (int, float)):
            # Web center X range
            web_center_left = plate_length/2 - column_len/2 - flange_thickness
            web_center_right = center_x + column_len/2+flange_thickness
            offset=(web_thickness-self.stiff_along_thickness)/2
            # Left web stiffener: from left edge to web start
            stiffener_web_left = QRectF(
                0,  # x-position (starts from left edge of plate)
                plate_width / 2 - self.stiff_along_thickness/2+offset ,  # y-position (top edge of stiffener)
                web_center_left ,  # width (same as before, up to web)
                self.stiff_along_thickness  # height (from y-position down)
            )
            self.scene.addRect(stiffener_web_left, outline_pen, red_brush)

            # Right web stiffener: from web end to right edge
            stiffener_web_right = QRectF(
            web_center_right,  # x-position (starts from web outward)
            plate_width / 2 - self.stiff_along_thickness / 2 + offset,  # centered vertically
            plate_length - web_center_right,  # width from web to right edge
            self.stiff_along_thickness
        )
            self.scene.addRect(stiffener_web_right, outline_pen, red_brush)
    
        if isinstance(self.stiff_across_thickness, (int, float)):
            web_center_left=center_x-self.stiff_across_thickness/2
            web_center_right=center_x+self.stiff_across_thickness/2
            stiffener_web_top = QRectF(
                web_center_left,                     # x
                center_y - self.stiff_across_length-web_thickness/2,                                   # y
                self.stiff_across_thickness,        # width = right - left
                self.stiff_across_length        # height from top to web
            )
            stiffener_web_bot = QRectF(
                web_center_left,                              # x-start
                center_y + self.web_thickness/2,                     # y-start (just below web)
                self.stiff_across_thickness,                  # width
                self.stiff_across_length      # height to bottom of plate
            )
            self.scene.addRect(stiffener_web_top, outline_pen, red_brush)
            self.scene.addRect(stiffener_web_bot, outline_pen, red_brush)
        bolts=self.no_outsidebolts
        hole_dia=self.dia_outside_bolt
        radius=hole_dia/2
        #2 rows
        #FINDING EFFECTIVE Edge distance
        edge=self.Edgeout
        end=self.Endout
        if self.Gaugeout!='N/A':
            Gauge=self.Gaugeout
        if self.pitchout!='N/A':
            pitch=self.pitchout
        print(bolts/4,edge,hole_dia)
        if bolts/4 ==1:
            edge = (plate_length-column_len-2*flange_thickness)/4
        else:
            edge=((plate_length-column_len)/2 - flange_thickness - Gauge)/2
        print(edge)
        from PyQt5.QtGui import QColor
        gold_brush = QBrush(QColor("gold"))
        black_pen = QPen(Qt.black)
        black_pen.setWidth(2)
        for col in range(int(bolts/4)):
            x =  edge + col * Gauge  # horizontal position

            # Top row bolt
            y_top = end
            self.scene.addEllipse(x - radius, y_top - radius, 2 * radius, 2 * radius, black_pen, gold_brush)

            # Bottom bolt
            y_bot = plate_width - end
            self.scene.addEllipse(x - radius, y_bot - radius, 2 * radius, 2 * radius, black_pen, gold_brush)
        for col in range(int(bolts/4)):
            x = plate_length - edge - col * Gauge
            y_top = end
            y_bot = plate_width - end

            self.scene.addEllipse(x - radius, y_top - radius, 2 * radius, 2 * radius, black_pen, gold_brush)
            self.scene.addEllipse(x - radius, y_bot - radius, 2 * radius, 2 * radius, black_pen, gold_brush)
    def createDrawing1(self):
        try:
            plate_length = float(self.plate_length)
            plate_width = float(self.plate_width)
        except (TypeError, ValueError):
            print("Invalid plate dimensions")
            return

        # Define the rectangle: (x, y, width, height)
        rect = QRectF(0, 0, plate_length, plate_width)
        column_len=self.column_len
        column_width=self.column_width
        flange_thickness=self.column_thickness
        web_thickness=self.web_thickness
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
        outline_pen = QPen(Qt.blue)
        outline_pen.setWidth(3)
        # === Center of the base plate ===
        center_x = plate_length / 2
        center_y = plate_width / 2

        # === Flange X dimensions ===
        # === Parameters ===
        flange_width = flange_thickness          # vertical width of flange
        flange_length = column_len               # horizontal length of flange (same as web)
        web_width = web_thickness                # vertical width of web
        web_length = column_len                  # horizontal length of web (same as flange)

        # === Column Center ===
        center_x = plate_length / 2
        center_y = plate_width / 2

        # === Y positions ===
        flange_top_y = center_y - column_width / 2
        flange_bottom_y = center_y + column_width / 2

        web_top_y = center_y - web_width / 2
        web_bottom_y = center_y + web_width / 2

        # === X positions (shared by web and flanges) ===
        web_left_x = center_x - web_length / 2
        web_right_x = center_x + web_length / 2

        # === Pen for drawing ===
        outline_pen = QPen(Qt.blue)
        outline_pen.setWidth(3)

        # === Draw Left Flange ===
        self.scene.addLine(web_left_x, flange_top_y, web_right_x, flange_top_y, outline_pen)   # Top
        self.scene.addLine(web_left_x, flange_top_y, web_left_x, web_top_y, outline_pen)       # Left top segment
        self.scene.addLine(web_left_x, web_bottom_y, web_left_x, flange_bottom_y, outline_pen) # Left bottom segment
        self.scene.addLine(web_left_x, flange_bottom_y, web_right_x, flange_bottom_y, outline_pen) # Bottom
        self.scene.addLine(web_right_x, flange_top_y, web_right_x, web_top_y, outline_pen)     # Right top segment
        self.scene.addLine(web_right_x, web_bottom_y, web_right_x, flange_bottom_y, outline_pen) # Right bottom segment

        # === Draw Web (as rectangle) ===
        # Top line
        self.scene.addLine(web_left_x, web_top_y, web_right_x, web_top_y, outline_pen)
        # Bottom line
        self.scene.addLine(web_left_x, web_bottom_y, web_right_x, web_bottom_y, outline_pen)
        # Left edge
        self.scene.addLine(web_left_x, web_top_y, web_left_x, web_bottom_y, outline_pen)
        # Right edge
        self.scene.addLine(web_right_x, web_top_y, web_right_x, web_bottom_y, outline_pen)

        #stifferener plate along column flange
        red_brush = QBrush(Qt.red)
        if self.stiff_flange_length != 'N/A':
            # === Left Flange Stiffeners ===
            # Top stiffener (left)
            stiffener_left_top = QRectF(
                left_flange_x1 -(self.stiff_flange_thickness-flange_thickness)/2 ,   # shift left by thickness
                0,                                   # from top of plate
                self.stiff_flange_thickness,                    # width
                top_y                                # height from plate top to top of flange
            )
            self.scene.addRect(stiffener_left_top, outline_pen, red_brush)

            # Bottom stiffener (left)
            stiffener_left_bottom = QRectF(
                left_flange_x1 - (self.stiff_flange_thickness-flange_thickness)/2,
                bottom_y,                            # start just below flange
                self.stiff_flange_thickness,
                plate_width - bottom_y              # height from flange to base plate bottom
            )
            self.scene.addRect(stiffener_left_bottom, outline_pen, red_brush)

            # === Right Flange Stiffeners ===
            # Top stiffener (right)
            stiffener_right_top = QRectF(
                right_flange_x2 - flange_thickness - (self.stiff_flange_thickness-flange_thickness)/2,                    # start at flange outer edge
                0,
                self.stiff_flange_thickness,
                top_y
            )
            self.scene.addRect(stiffener_right_top, outline_pen, red_brush)

            # Bottom stiffener (right)
            stiffener_right_bottom = QRectF(
                right_flange_x2-flange_thickness - (self.stiff_flange_thickness-flange_thickness)/2,
                bottom_y,
                self.stiff_flange_thickness,
                plate_width - bottom_y
            )
            self.scene.addRect(stiffener_right_bottom, outline_pen, red_brush)
        if self.stiff_along_thickness != 'N/A':
            # Web center X range
            web_center_left = plate_length
            web_center_right = center_x + web_thickness / 2

            # Left web stiffener: from left edge to web start
            stiffener_web_left = QRectF(
        0,  # x-position (starts from left edge of plate)
        plate_width / 2 - web_thickness / 2,  # y-position (top edge of stiffener)
        web_center_left ,  # width (same as before, up to web)
        web_thickness  # height (from y-position down)
    )
            self.scene.addRect(stiffener_web_left, outline_pen, red_brush)

            # Right web stiffener: from web end to right edge
            stiffener_web_right = QRectF(
                web_center_right,
                top_y,
                plate_length - web_center_right,  # width from web to right edge
                web_thickness
            )
            self.scene.addRect(stiffener_web_right, outline_pen, red_brush)
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
        
        width = calculate_total_width(edge, gauge1, gauge2, self.cols)
        height = 2 * end + (self.rows - 1) * pitch
        
        # Offsets for dimension lines
        h_offset = 20
        v_offset = 30
        
        # Add horizontal dimensions
        x_start = 0
        segments = []
        # First edge
        segments.append(('edge', x_start, x_start + edge))
        x_start += edge
        # Alternate gauges
        for i in range(self.cols - 1):
            gauge = gauge1 if i % 2 == 0 else gauge2
            label = f'gauge{i % 2 + 1}'
            segments.append((label, x_start, x_start + gauge))
            x_start += gauge
        # Last edge
        segments.append(('edge', x_start, x_start + edge))

        # Draw each segment
        for label, x1, x2 in segments:
            value = x2 - x1
            self.addHorizontalDimension(x1, -h_offset, x2, -h_offset, f"{value:.1f}", pen)
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