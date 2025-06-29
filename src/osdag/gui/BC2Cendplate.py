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
class BC2CEndPlate(QMainWindow):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        print(main)
        if main:
            self.flag=main[1]
            main=main[0]
        super().__init__()
        self.connection = connection_obj
        data=main.output_values(main,True)
        
        print(type(main))
        dict1={i[0] : i[3] for i in data}
        for i in dict1:
            print(f'{i} : {dict1[i]}')
        self.plate_width=dict1['Plate.Height']
        self.plate_length=dict1['Plate.Length']
        self.stiffener_length=dict1['Stiffener.Width']
        self.stiffener_thickness=dict1['Stiffener.Thickness']
        self.web_thickness=main.section.web_thickness
        self.flange_thickness=main.section.flange_thickness
        self.webdetail_width=self.plate_width-2*self.stiffener_length
        self.webdetail_len=self.plate_length
        self.hole_dia=dict1['Bolt.Diameter']
        webspacing=dict1['Bolt.web_bolts'][1]
        flangespacing=dict1['Bolt.flange_bolts'][1]
        flangespacing=flangespacing(main,True)
        # print(webspacing)
        webspacing=webspacing(main,True)
        print(webspacing)
        # for i in webspacing:
        #     print(i)
        dict2={i[1] : i[3] for i in webspacing}
        for i in dict2:
            print(f'{i} : {dict2[i]}')
        self.web_bolts=dict2['No. of Bolts (along web)']
        self.pitch1,self.pitch2,self.pitch3,self.pitch4=0,0,0,0
        if 'Pitch 1-2' in dict2:
            self.pitch1=dict2['Pitch 1-2']
        if 'Pitch 2-3' in dict2:
            self.pitch2=dict2['Pitch 2-3']
        if 'Pitch 3-4' in dict2:
            self.pitch3=dict2['Pitch 3-4']
        if 'Pitch 4-5' in dict2:
            self.pitch4=dict2['Pitch 4-5']
        for i in flangespacing:
            print(i)
        dict3={i[0] : i[3] for i in flangespacing}
        self.flangeend,self.boltoneside,self.flangetotal,self.pitchflange=0,0,0,0
        if 'Bolt.EndDist' in dict3:
            self.flangeend=dict3['Bolt.EndDist']
        if 'ColumnEndPlate.nbf' in dict3:
            self.boltoneside=dict3['ColumnEndPlate.nbf']
        if 'ColumnEndPlate.nbftotal' in dict3:
            self.flangetotal=dict3['ColumnEndPlate.nbftotal']
        if 'ColumnEndPlate.p2_flange' in dict3:
            self.flangepitch=dict3['ColumnEndPlate.p2_flange']
        print(f' Flange End Distance : {self.flangeend} , TotalBolt : {self.flangetotal}')
        self.web_end=dict2['End Distance (mm)']
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        print(f"""
        Plate Width              : {self.plate_width}
        Plate Length             : {self.plate_length}
        Stiffener Length (Width) : {self.stiffener_length}
        Stiffener Thickness      : {self.stiffener_thickness}
        Web Thickness            : {self.web_thickness}
        Flange Thickness         : {self.flange_thickness}
        Web Detail Length        : {self.webdetail_len}
        Web Detail Width         : {self.webdetail_width}
        """)
        
        self.setGeometry(100, 100, 1200, 900)
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
            stiff_len=self.stiffener_length
            stiff_thick=self.stiffener_thickness
            web_thick=self.web_thickness
            flange_thick=self.flange_thickness
            webdetailinglen=self.webdetail_len
            webdetailingwidth=self.webdetail_width
            web_bolts=self.web_bolts
            web_end=self.web_end
            pitch1=self.pitch1
            pitch2=self.pitch2
            pitch3=self.pitch3
            pitch4=self.pitch4
            hole_dia=self.hole_dia
        except (TypeError, ValueError):
            print("Invalid plate dimensions")
            return
        if self.flag==0:
            rect = QRectF(0, 0, webdetailinglen, webdetailingwidth)
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
            rect_item = QGraphicsRectItem(QRectF(0, 0, webdetailinglen, webdetailingwidth))
            rect_item.setPen(outline_pen)
            rect_item.setBrush(QBrush(Qt.white))
            self.scene.addItem(rect_item)
        # === Center of the base plate ===
            center_x = webdetailinglen / 2
            center_y = webdetailingwidth / 2
            self.addHorizontalDimension(
                0, -30,  # x1 at left edge, y above plate
                webdetailinglen, -30,  # x2 at right edge, same y
                f"{webdetailinglen} mm", pen
            )

            # Vertical dimension for plate width (to the left of the plate)
            self.addVerticalDimension(
                webdetailinglen+30, 0,  # x left of plate, y1 at top
                webdetailinglen+30, webdetailingwidth,  # x2 same, y2 at bottom
                f"{webdetailingwidth} mm", pen
            )
            line_pen = QPen(QColor("orange"))
            line_pen.setWidth(2)

            # Line at y = 0 (full length)
            line_top = self.scene.addLine(
                0, 0,  # Start point (x=0, y=0)
                webdetailinglen, 0,  # End point (x=plate_length, y=0)
                line_pen
            )

            # Lines at y = flange_thickness
            # First line: from x = 0 to center_x - web_thickness / 2
            line_flange_left = self.scene.addLine(
                0, flange_thick,
                center_x - web_thick / 2, flange_thick,
                line_pen
            )

            # Second line: from x = center_x + web_thickness / 2 to x = plate_length
            line_flange_right = self.scene.addLine(
                center_x + web_thick / 2, flange_thick,
                webdetailinglen, flange_thick,
                line_pen
            )
            line_left_vertical = self.scene.addLine(
                0, 0,  # x = 0, y = 0
                0, flange_thick,  # x = 0, y = flange_thickness
                line_pen
            )

            # Right vertical line at x = plate_length
            line_right_vertical = self.scene.addLine(
                plate_length, 0,  # x = plate_length, y = 0
                webdetailinglen, flange_thick,  # x = plate_length, y = flange_thickness
                line_pen
            )
            # === Bottom side ===

            # Line at y = webdetailingwidth (full length)
            line_bottom = self.scene.addLine(
                0, webdetailingwidth,
                webdetailinglen, webdetailingwidth,
                line_pen
            )

            # Lines at y = webdetailingwidth - flange_thick
            # First line: from x = 0 to center_x - web_thick / 2
            line_bottom_flange_left = self.scene.addLine(
                0, webdetailingwidth - flange_thick,
                center_x - web_thick / 2, webdetailingwidth - flange_thick,
                line_pen
            )

            # Second line: from x = center_x + web_thick / 2 to x = webdetailinglen
            line_bottom_flange_right = self.scene.addLine(
                center_x + web_thick / 2, webdetailingwidth - flange_thick,
                webdetailinglen, webdetailingwidth - flange_thick,
                line_pen
            )

            # Vertical line at x = 0, from y = webdetailingwidth - flange_thick to y = webdetailingwidth
            line_bottom_left_vertical = self.scene.addLine(
                0, webdetailingwidth - flange_thick,
                0, webdetailingwidth,
                line_pen
            )

            # Vertical line at x = webdetailinglen, from y = webdetailingwidth - flange_thick to y = webdetailingwidth
            line_bottom_right_vertical = self.scene.addLine(
                webdetailinglen, webdetailingwidth - flange_thick,
                webdetailinglen, webdetailingwidth,
                line_pen
            )
            # === Web vertical lines ===

            # Left web vertical line at x = center_x - web_thick / 2
            line_web_left_vertical = self.scene.addLine(
                center_x - web_thick / 2, flange_thick,
                center_x - web_thick / 2, webdetailingwidth - flange_thick,
                line_pen
            )

            # Right web vertical line at x = center_x + web_thick / 2
            line_web_right_vertical = self.scene.addLine(
                center_x + web_thick / 2, flange_thick,
                center_x + web_thick / 2, webdetailingwidth - flange_thick,
                line_pen
            )
            bolt_pen = QPen(QColor("blue"))
            bolt_pen.setWidth(2)
            bolt_brush = QBrush(Qt.NoBrush)

            # Number of rows = web_bolts / 2
            num_rows = int(web_bolts / 2)

            # X positions of columns
            x_left = center_x - web_thick / 2 - web_end
            x_right = center_x + web_thick / 2 + web_end

            # Starting Y position
            y_pos = flange_thick + web_end

            # Pitch list to cycle through
            pitch_list = [pitch1, pitch2, pitch3, pitch4]

            # Draw bolts row by row
            for row in range(num_rows):
                # Draw left bolt
                self.scene.addEllipse(
                    x_left - hole_dia / 2,  # X center aligned
                    y_pos - hole_dia / 2,   # Y center aligned
                    hole_dia,
                    hole_dia,
                    bolt_pen,
                    bolt_brush
                )

                # Draw right bolt
                self.scene.addEllipse(
                    x_right - hole_dia / 2,
                    y_pos - hole_dia / 2,
                    hole_dia,
                    hole_dia,
                    bolt_pen,
                    bolt_brush
                )

                # Increment Y position by next pitch
                pitch_index = row % len(pitch_list)  # Cycle through pitches
                y_pos += pitch_list[pitch_index]
                self.addHorizontalDimension(
                center_x + web_thick / 2, webdetailingwidth+20,  # x1, y1
                center_x + web_thick / 2 + web_end, webdetailingwidth+20,  # x2, y2
                f"{web_end} mm",  # Dimension label
                pen  # Use the pen you already have (black or any color)
            )
                y_temp=flange_thick+web_end+hole_dia+5
                self.addHorizontalDimension(
                center_x + web_thick / 2+web_end-hole_dia/2, y_temp,  # x1, y1
                center_x + web_thick / 2 + web_end+hole_dia/2, y_temp,  # x2, y2
                f"{hole_dia} mm",  # Dimension label
                pen  # Use the pen you already have (black or any color)
            )
                x_dim = -20

                # Starting Y
                y_current = flange_thick + web_end
                self.addVerticalDimension(
                        x_dim, y_current-web_end,  # x1, y1
                        x_dim, y_current,     # x2, y2
                        f"{web_end} mm",     # Dimension label
                        pen  # Use your dimension pen (black or any color)
                    )
                # List of pitches
                pitch_list = [pitch1, pitch2, pitch3, pitch4]

                # Iterate over pitches
                for pitch in pitch_list:
                    if pitch == 0:
                        break  # Stop if pitch is 0
                    
                    y_next = y_current + pitch
                    
                    # Add vertical dimension for this pitch
                    self.addVerticalDimension(
                        x_dim, y_current,  # x1, y1
                        x_dim, y_next,     # x2, y2
                        f"{pitch} mm",     # Dimension label
                        pen  # Use your dimension pen (black or any color)
                    )
                    
                    # Move to next position
                    y_current = y_next
        else:
            flangelen=plate_length
            flangewidth=plate_width/2
            webdetailingwidth=flangewidth
            
            rect = QRectF(0, 0, flangelen, flangewidth)
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
            rect_item = QGraphicsRectItem(QRectF(0, 0, flangelen, flangewidth))
            rect_item.setPen(outline_pen)
            rect_item.setBrush(QBrush(Qt.white))
            self.scene.addItem(rect_item)
        # === Center of the base plate ===
            center_x = flangelen / 2
            center_y = flangewidth / 2
            self.addHorizontalDimension(
                0, -30,  # x1 at left edge, y above plate
                flangelen, -30,  # x2 at right edge, same y
                f"{flangelen} mm", pen
            )

            # Vertical dimension for plate width (to the left of the plate)
            self.addVerticalDimension(
                flangelen+30, 0,  # x left of plate, y1 at top
                flangelen+30, flangewidth,  # x2 same, y2 at bottom
                f"{flangewidth} mm", pen
            )
            stiffener_rect = QRectF(
                center_x - stiff_thick / 2,  # x1
                0,                           # y1
                stiff_thick,                # width
                stiff_len                   # height
            )
            stiffener_item = QGraphicsRectItem(stiffener_rect)
            stiffener_item.setPen(QPen(Qt.black))
            stiffener_item.setBrush(QBrush(Qt.blue))
            self.scene.addItem(stiffener_item)
            line_pen = QPen(QColor("orange"))
            line_pen.setWidth(2)
            line_top = self.scene.addLine(
                0, stiff_len,  # Start point (x=0, y=stiff_len)
                webdetailinglen, stiff_len,  # End point (x=plate_length, y=stiff_len)
                line_pen
            )

            # Lines at y = stiff_len + flange_thickness
            # First line: from x = 0 to center_x - web_thickness / 2
            line_flange_left = self.scene.addLine(
                0, stiff_len + flange_thick,
                center_x - web_thick / 2, stiff_len + flange_thick,
                line_pen
            )

            # Second line: from x = center_x + web_thickness / 2 to x = plate_length
            line_flange_right = self.scene.addLine(
                center_x + web_thick / 2, stiff_len + flange_thick,
                webdetailinglen, stiff_len + flange_thick,
                line_pen
            )

            # Left vertical line at x = 0
            line_left_vertical = self.scene.addLine(
                0, stiff_len,
                0, stiff_len + flange_thick,
                line_pen
            )

            # Right vertical line at x = plate_length
            line_right_vertical = self.scene.addLine(
                plate_length, stiff_len,
                plate_length, stiff_len + flange_thick,
                line_pen
            )
            stiff_line_vertical=self.scene.addLine(
                center_x-web_thick/2,stiff_len+flange_thick,
                center_x-web_thick/2,webdetailingwidth,line_pen
            )
            stiff_line_vertical=self.scene.addLine(
                center_x+web_thick/2,stiff_len+flange_thick,
                center_x+web_thick/2,webdetailingwidth,line_pen
            )
            totalbolts=self.flangetotal/2
            flangeend=self.flangeend
            cols=self.boltoneside*2
            line_pen=QPen(Qt.blue)
            if stiff_len>0 and totalbolts>2 :
                y_pos = flangeend  # You need to define this depending on your layout logic

                # Calculate center
                center_x = self.plate_length / 2

                # Calculate bolt positions
                left_bolt_x = center_x-web_thick/2-flangeend
                right_bolt_x = center_x+web_thick/2+flangeend

                # Add bolts to scene (assuming addEllipse represents bolts)
                bolt_radius = hole_dia/2 # or whatever radius you use
                self.scene.addEllipse(left_bolt_x - bolt_radius, y_pos - bolt_radius,
                                    2 * bolt_radius, 2 * bolt_radius, line_pen)
                self.scene.addEllipse(right_bolt_x - bolt_radius, y_pos - bolt_radius,
                                    2 * bolt_radius, 2 * bolt_radius, line_pen)
                totalbolts-=2
            num_rows = int(web_bolts // 4)
            # X positions of columns
            x_left = center_x - web_thick / 2 - web_end
            x_right = center_x + web_thick / 2 + web_end

            # Starting Y position
            y_pos = flange_thick + web_end+stiff_len

            # Pitch list to cycle through
            pitch_list = [pitch1, pitch2, pitch3, pitch4]

            # Draw bolts row by row
            for row in range(num_rows):
                # Draw left bolt
                self.scene.addEllipse(
                    x_left - hole_dia / 2,  # X center aligned
                    y_pos - hole_dia / 2,   # Y center aligned
                    hole_dia,
                    hole_dia,
                    line_pen                    
                )

                # Draw right bolt
                self.scene.addEllipse(
                    x_right - hole_dia / 2,
                    y_pos - hole_dia / 2,
                    hole_dia,
                    hole_dia,
                    line_pen
                )

                # Increment Y position by next pitch
                pitch_index = row % len(pitch_list)  # Cycle through pitches
                y_pos += pitch_list[pitch_index]
                self.addHorizontalDimension(
                center_x + web_thick / 2, webdetailingwidth+20,  # x1, y1
                center_x + web_thick / 2 + web_end, webdetailingwidth+20,  # x2, y2
                f"{web_end} mm",  # Dimension label
                pen  # Use the pen you already have (black or any color)
            )
                y_temp=flange_thick+web_end+hole_dia+5
                self.addHorizontalDimension(
                center_x + web_thick / 2+web_end-hole_dia/2, y_temp,  # x1, y1
                center_x + web_thick / 2 + web_end+hole_dia/2, y_temp,  # x2, y2
                f"{hole_dia} mm",  # Dimension label
                pen  # Use the pen you already have (black or any color)
            )
                x_dim = -20

                # Starting Y
                if stiff_len==0:
                    y_current=flange_thick+web_end
                else:
                    y_current =   flangeend
                self.addVerticalDimension(
                        x_dim, y_current-web_end,  # x1, y1
                        x_dim, y_current,     # x2, y2
                        f"{flangeend} mm",     # Dimension label
                        pen  # Use your dimension pen (black or any color)
                    )
                
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
