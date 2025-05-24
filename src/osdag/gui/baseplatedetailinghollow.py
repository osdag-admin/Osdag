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
class BasePlateDetailingHollow(QMainWindow):
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
        print(f'Connectivity  : {main.connectivity}\n\n')
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
            print(f'{i} : {self.detail_dict[i]}')
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
        print(f'Column Section : {main.column_section}')
        self.column_section=main.column_section
        stiffdata=main.stiffener_hollow_details(main,True)
        self.stiff_D_len=stiffdata[1][3]
        self.stiff_D_thickness=stiffdata[3][3]
        self.stiff_B_len=stiffdata[9][3]
        self.stiff_B_thickness=stiffdata[11][3]
        self.stiff_OD_len=stiffdata[17][3]
        self.stiff_OD_thickness=stiffdata[19][3]
        for i in stiffdata:
            print(i)
        
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
        End Out Distance          : {self.Endout}
        Edge Out Distance         : {self.Edgeout}
        End In Distance : {self.Endin}
        Edge In Distance  : {self.Edgein}
        Plate Width : {self.plate_width}
        Plate Length : {self.plate_length}
        Stiffener Plate Dimensions:
        ---------------------------
        STIFFENER_D     - Length: {self.stiff_D_len}, Thickness: {self.stiff_D_thickness}
        STIFFENER B    - Length: {self.stiff_B_len}, Thickness: {self.stiff_B_thickness}
        STIFFENER OD- Diameter: {self.stiff_OD_len}, Thickness: {self.stiff_OD_thickness}
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
            "No. of Outside Bolts",
            "Diameter Outside Bolt",
            "No. of Inside Bolts",
            "Diameter Inside Bolt",
            "Base Plate Length",
            "Base Plate Width",
            "End Out Distance",
            "Edge Out Distance",
            "End In Distance",
            "Edge In Distance",
            "STIFFENER_D Length",
            "STIFFENER_D Thickness",
            "STIFFENER_B Length",
            "STIFFENER_B Thickness",
            "STIFFENER_OD Diameter",
            "STIFFENER_OD Thickness",
            "COLUMN WIDTH",
            "COLUMN LENGTH"
        ]


        # Add labels
        values_to_display = {
            "No. of Outside Bolts": self.no_outsidebolts,
            "Diameter Outside Bolt": self.dia_outside_bolt,
            "Base Plate Length": self.plate_length,
            "Base Plate Width": self.plate_width,
            "End  Distance": self.Endout,
            "Edge Distance": self.Edgeout,
            "COLUMN WIDTH": self.column_width,
            "COLUMN LENGTH":self.column_len
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
        # Step 6: Call parameter extraction and drawing
        # self.get_parameters()
        self.createDrawing()
        if self.plate_length>600:
            self.view.resetTransform()
            self.view.scale(0.5, 0.5)
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
        outline_pen.setWidth(1)
        # === Center of the base plate ===
        center_x = plate_length / 2
        center_y = plate_width / 2
        print(self.column_section)
        if self.column_section.startswith(' RHS') or self.column_section.startswith(' SHS'):
            col_len=self.column_len
            col_width=self.column_width
            col_thickness=self.column_thickness
            top_left_x = center_x - col_len / 2
            top_left_y = center_y - col_width / 2
        
            # Add rectangle
            self.scene.addRect(top_left_x, top_left_y, col_len, col_width, outline_pen)
            self.scene.addRect(top_left_x+col_thickness, top_left_y+col_thickness, col_len-2*col_thickness, col_width-2*col_thickness, outline_pen)
            #innerrectangle
            self.addHorizontalDimension(
                top_left_x,                # x1
                top_left_y - 20,           # y above the column
                top_left_x + col_len,      # x2
                top_left_y - 20,           # y2 (same as y1)
                f"{col_len} mm", pen
            )

            # Vertical dimension (Width)
            self.addVerticalDimension(
                top_left_x - 20,           # x to the left of column
                top_left_y,                # y1 (top)
                top_left_x - 20,           # x2 (same as x1)
                top_left_y + col_width,    # y2 (bottom)
                f"{col_width} mm", pen
            )
            stiff_thickness = self.stiff_D_thickness
        else:
            col_len=self.column_len
            col_width=self.column_width
            col_thickness=self.column_thickness
            top_left_x = center_x - col_len / 2
            top_left_y = center_y - col_width / 2
            self.scene.addEllipse(top_left_x, top_left_y, col_len, col_width, outline_pen)

            # Inner ellipse (hollow cutout)
            inner_x = top_left_x + col_thickness
            inner_y = top_left_y + col_thickness
            inner_len = col_len - 2 * col_thickness
            inner_width = col_width - 2 * col_thickness
            self.scene.addEllipse(inner_x, inner_y, inner_len, inner_width, outline_pen)
            self.addHorizontalDimension(
                top_left_x,                # x1
                center_y - 20,           # y above the column
                top_left_x + col_len,      # x2
                center_y - 20,           # y2 (same as y1)
                f"{col_len} mm", pen
            )
            stiff_thickness=self.stiff_OD_thickness
        outline_pen = QPen(Qt.black)
        outline_pen.setWidth(2)
        
        
        stiff_top = 0  # Top of plate
        stiff_start_y = center_y - col_width / 2  # col_width/2 above center
        stiff_x = center_x - stiff_thickness / 2  # centered left

        # Height from top of plate to start of stiffener
        stiff_height = stiff_start_y - stiff_top
        
        # Draw vertical stiffener rectangle
        self.scene.addRect(
            stiff_x,
            stiff_top,
            stiff_thickness,
            stiff_height,
            outline_pen,
            QBrush(Qt.red)  # Optional: red fill
        )
        stiff_start_y=center_y+col_width/2
        stiff_x=center_x-stiff_thickness/2
        self.scene.addRect(
            stiff_x,stiff_start_y,
            stiff_thickness,
            stiff_height,
            outline_pen,
            QBrush(Qt.red)
        )
        self.addVerticalDimension(
            stiff_x + stiff_thickness + 10,                  # x (offset right)
            stiff_start_y,                                   # y1 (top)
            stiff_x + stiff_thickness + 10,                  # x2 (same x)
            stiff_start_y + stiff_height,                    # y2 (bottom)
            f"{round(stiff_height)} mm", pen
        )
        if self.column_section.startswith(' RHS') or self.column_section.startswith(' SHS'):
            stiff_thickness=self.stiff_B_thickness
        stiff_x=0
        stiff_start_y=center_y-stiff_thickness/2
        stiff_length=center_x-col_len/2
        stiff_height=stiff_thickness
        self.scene.addRect(
            stiff_x,stiff_start_y,
            stiff_length,
            stiff_height,
            outline_pen,
            QBrush(Qt.red)
        )
        self.addHorizontalDimension(
            0, stiff_start_y + 35,                      # x1, y1 (slightly above the stiffener)
            stiff_length, stiff_start_y +35,           # x2, y2 (same y-level)
            f"{round(stiff_length)} mm", pen
        )
        stiff_x=center_x+col_len/2
        self.scene.addRect(
            stiff_x,stiff_start_y,
            stiff_length,
            stiff_height,
            outline_pen,
            QBrush(Qt.red)
        )
        bolts=self.no_outsidebolts
        hole_dia=self.dia_outside_bolt
        edge=self.Edgeout
        end=self.Endout
        radius=hole_dia/2
        from PyQt5.QtGui import QColor
        gold_brush = QBrush(QColor("gold"))
        x1 = edge
        y1 = end
        self.scene.addEllipse(x1 - radius, y1 - radius, hole_dia, hole_dia, outline_pen, gold_brush)
        self.addHorizontalDimension(0, y1 + 20, x1, y1 + 20, f"{edge} mm", pen)
        self.addVerticalDimension(x1 + 20, 0, x1 + 20, y1, f"{end} mm", pen)

        # Top-right bolt
        x2 = self.plate_length - edge
        y2 = end
        self.scene.addEllipse(x2 - radius, y2 - radius, hole_dia, hole_dia, outline_pen, gold_brush)
        self.addHorizontalDimension(x2, y2 + 20, self.plate_length, y2 + 20, f"{edge} mm", pen)
        self.addVerticalDimension(x2 + 20, 0, x2 + 20, y2, f"{end} mm", pen)

        # Bottom-left bolt
        x3 = edge
        y3 = self.plate_width - end
        self.scene.addEllipse(x3 - radius, y3 - radius, hole_dia, hole_dia, outline_pen, gold_brush)
        self.addHorizontalDimension(0, y3 + 20, x3, y3 + 20, f"{edge} mm", pen)
        self.addVerticalDimension(x3 + 20, y3, x3 + 20, self.plate_width, f"{end} mm", pen)

        # Bottom-right bolt
        x4 = self.plate_length - edge
        y4 = self.plate_width - end
        self.scene.addEllipse(x4 - radius, y4 - radius, hole_dia, hole_dia, outline_pen, gold_brush)
        self.addHorizontalDimension(x4, y4 + 20, self.plate_length, y4 + 20, f"{edge} mm", pen)
        self.addVerticalDimension(x4 + 20, y4, x4 + 20, self.plate_width, f"{end} mm", pen)
            
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
    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        from PyQt5.QtCore import QPointF
        from PyQt5.QtGui import QPolygonF
        from PyQt5.QtGui import QFont, QBrush
        from PyQt5.QtCore import Qt

        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 5
        if self.plate_length>500:
            arrow_size=10
        ext_length = 10

        # Extension lines
        self.scene.addLine(x1, y1 - ext_length / 2, x1, y1 + ext_length / 2, pen)
        self.scene.addLine(x2, y2 - ext_length / 2, x2, y2 + ext_length / 2, pen)

        # Left arrow
        poly_left = QPolygonF([
            QPointF(x1, y1),
            QPointF(x1 + arrow_size, y1 - arrow_size / 2),
            QPointF(x1 + arrow_size, y1 + arrow_size / 2)
        ])
        arrow_left = self.scene.addPolygon(poly_left, pen)
        arrow_left.setBrush(QBrush(Qt.black))

        # Right arrow
        poly_right = QPolygonF([
            QPointF(x2, y2),
            QPointF(x2 - arrow_size, y2 - arrow_size / 2),
            QPointF(x2 - arrow_size, y2 + arrow_size / 2)
        ])
        arrow_right = self.scene.addPolygon(poly_right, pen)
        arrow_right.setBrush(QBrush(Qt.black))

        # Text
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        if self.plate_length>500:
            font.setPointSize(10)
        text_item.setFont(font)
        text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 + 5)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        from PyQt5.QtCore import QPointF
        from PyQt5.QtGui import QPolygonF, QFont, QBrush
        from PyQt5.QtCore import Qt

        # Draw dimension line
        self.scene.addLine(x1, y1, x2, y2, pen)

        arrow_size = 5
        if self.plate_length>500:
            arrow_size=10
        ext_length = 10

        # Extension lines
        self.scene.addLine(x1 - ext_length / 2, y1, x1 + ext_length / 2, y1, pen)
        self.scene.addLine(x2 - ext_length / 2, y2, x2 + ext_length / 2, y2, pen)

        # Arrowheads
        if y2 > y1:
            # Arrow at top (y1)
            poly_top = QPolygonF([
                QPointF(x1, y1),
                QPointF(x1 - arrow_size / 2, y1 + arrow_size),
                QPointF(x1 + arrow_size / 2, y1 + arrow_size)
            ])
            self.scene.addPolygon(poly_top, pen).setBrush(QBrush(Qt.black))

            # Arrow at bottom (y2)
            poly_bot = QPolygonF([
                QPointF(x2, y2),
                QPointF(x2 - arrow_size / 2, y2 - arrow_size),
                QPointF(x2 + arrow_size / 2, y2 - arrow_size)
            ])
            self.scene.addPolygon(poly_bot, pen).setBrush(QBrush(Qt.black))
        else:
            # Reversed
            poly_top = QPolygonF([
                QPointF(x2, y2),
                QPointF(x2 - arrow_size / 2, y2 + arrow_size),
                QPointF(x2 + arrow_size / 2, y2 + arrow_size)
            ])
            self.scene.addPolygon(poly_top, pen).setBrush(QBrush(Qt.black))

            poly_bot = QPolygonF([
                QPointF(x1, y1),
                QPointF(x1 - arrow_size / 2, y1 - arrow_size),
                QPointF(x1 + arrow_size / 2, y1 - arrow_size)
            ])
            self.scene.addPolygon(poly_bot, pen).setBrush(QBrush(Qt.black))

        # === Label Text (only once)
        text_item = self.scene.addText(text)
        font = QFont()
        if self.plate_length>500:
            font.setPointSize(10)  # Bigger font
        text_item.setFont(font)

        # Position to right side of the line
        label_x_offset = 15
        label_y_center = (y1 + y2) / 2 - text_item.boundingRect().height() / 2
        text_item.setPos(x1 + label_x_offset, label_y_center)
