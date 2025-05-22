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
class BeamtoColDetailing(QMainWindow):
    def __init__(self, connection_obj,main, rows=3, cols=2):
        super().__init__()
        self.connection = connection_obj
        data=main.output_values(main,True)
        self.web_thick=main.beam_tw
        self.endplatetype=main.endplate_type
        self.flange_thick=main.beam_tf
        self.middle_bolts=main.bolt_row_web
        self.stiffener_length = main.stiffener_length
        self.stiffener_thickness=main.stiffener_thickness
        self.rows_inside_D_max = main.rows_inside_D_max
        self.rows_outside_D_max = main.rows_outside_D_max
        self.detail_dict = {
                                entry[1]: entry[3]
                                for entry in data
                                }
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        print(f'End Plate Type :  {self.endplatetype}')
        print(f'middle bolts : {self.middle_bolts}')
        print(f'stiffener length : {self.stiffener_length}')
        
        self.setGeometry(100, 100, 800, 500)
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
            'No. of Rows',
            'No. of Columns',
            'Pitch Distance (mm)',
            'Gauge Distance (mm)',
            'Cross-centre Gauge (mm)',  # optional: if applicable
            'End Distance (mm)',
            'Edge Distance (mm)',
            'Height (mm)',
            'Width (mm)',
            'Diameter (mm)',
        ]

        # Add labels
        for key in keys_to_display:
            if key in self.detail_dict:
                value = self.detail_dict[key]
                label = QLabel(f"<b>{key}</b>: {value}")
                left_layout.addWidget(label)
        self.edge_label = QLabel("<b>Adjusted Edge Distance</b>: computing...")
        left_layout.addWidget(self.edge_label)
        # Step 4: Graphics view and scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        # Background and test shape (optional)
        self.scene.setBackgroundBrush(Qt.lightGray)

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
        if self.endplatetype.startswith('Flushed'):
            self.createDrawingFlushedReversible()
        elif self.endplatetype.startswith('Extended One'):
            self.createDrawingExtendedOneWay()
        else:
            self.createDrawingExtendedTwoWay()
    def createDrawingFlushedReversible(self):
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPen, QColor,QBrush

        # Inputs
        webthickness = self.web_thick
        flangethickness = self.flange_thick
        plate_height = self.height
        plate_width = self.width
        rows = self.rows
        cols = self.cols
        pitch = self.pitch
        crossgauge = float(self.CrossGauge)
        end = self.End
        edge = float(self.Edge)
        holedia = self.hole_diameter
        gauge = float(self.Gauge)
        print(f'rows: {rows} , cols : {cols}')
        h_gap = 12.5
        v_gap = 12.5
        outline_pen = QPen(Qt.blue, 2)
        black_pen = QPen(QColor("black"), 2)
        bolt_pen = QPen(Qt.black, 2)
        bolt_brush = QBrush(QColor("gold"))
        radius = holedia / 2
        total_span = 2 * edge + crossgauge
        extra_per_side = (cols - 2) // 2
        for _ in range(extra_per_side):
            total_span += 2 * gauge
        if total_span<= plate_width:
        # --- Adjust edge to center the bolt group ---
            edge += (plate_width - total_span) / 2
        # Scene setup
        self.adjusted_edge=edge
        if hasattr(self, 'edge_label'):
            self.edge_label.setText(f"<b>Adjusted Edge Distance</b>: {self.adjusted_edge:.2f} mm")
        self.scene.setSceneRect(-40, -60, plate_width + 80, plate_height + 120)

        # --- Draw plate rectangle (outer boundary) ---
        self.scene.addRect(0, 0, plate_width, plate_height, black_pen)

        # --- Web Coordinates ---
        web_x1 = (plate_width - webthickness) / 2
        web_x2 = web_x1 + webthickness
        flange_top_y = v_gap
        flange_bottom_y = plate_height - v_gap

        # Flange bottom/top edges
        flange_bottom_edge_y_top = flange_top_y + flangethickness
        flange_bottom_edge_y_bottom = flange_bottom_y - flangethickness

        web_y1 = flange_bottom_edge_y_top
        web_y2 = flange_bottom_edge_y_bottom

        # --- Web vertical lines ---
        self.scene.addLine(web_x1, web_y1, web_x1, web_y2, outline_pen)
        self.scene.addLine(web_x2, web_y1, web_x2, web_y2, outline_pen)

        # --- Top Flange ---
        self.scene.addLine(h_gap, flange_top_y, plate_width - h_gap, flange_top_y, outline_pen)
        self.scene.addLine(h_gap, flange_bottom_edge_y_top, web_x1, flange_bottom_edge_y_top, outline_pen)
        self.scene.addLine(web_x2, flange_bottom_edge_y_top, plate_width - h_gap, flange_bottom_edge_y_top, outline_pen)
        self.scene.addLine(h_gap, flange_top_y, h_gap, flange_bottom_edge_y_top, outline_pen)
        self.scene.addLine(plate_width - h_gap, flange_top_y, plate_width - h_gap, flange_bottom_edge_y_top, outline_pen)

        # --- Bottom Flange ---
        self.scene.addLine(h_gap, flange_bottom_y, plate_width - h_gap, flange_bottom_y, outline_pen)
        self.scene.addLine(h_gap, flange_bottom_edge_y_bottom, web_x1, flange_bottom_edge_y_bottom, outline_pen)
        self.scene.addLine(web_x2, flange_bottom_edge_y_bottom, plate_width - h_gap, flange_bottom_edge_y_bottom, outline_pen)
        self.scene.addLine(h_gap, flange_bottom_edge_y_bottom, h_gap, flange_bottom_y, outline_pen)
        self.scene.addLine(plate_width - h_gap, flange_bottom_edge_y_bottom, plate_width - h_gap, flange_bottom_y, outline_pen)

        # --- Calculate total bolt span ---
        # print(rows, cols)
        rowstop = int(rows / 2)

        

        print('Total Span:', total_span)
        
        print('Adjusted Edge:', edge)

        # --- Draw top half bolt rows ---
        y_start = 12.5 + flangethickness +end # inside top flange

        for row in range(rowstop):
            y = y_start + row * pitch
            x = edge  # Start from adjusted edge

            for col in range(cols):
                # Draw bolt at (x, y)
                # print(f'row : {row} , col : {col} , x : {x} y : {y}')

                self.scene.addEllipse(x - radius, y - radius, holedia, holedia, bolt_pen,bolt_brush)

                # Advance x for next column
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge
                # --- Draw bottom half bolt rows ---
        y_start_bottom = plate_height - (12.5 + flangethickness + end)

        for row in range(rowstop):
            y = y_start_bottom - row * pitch
            x = edge  # Reset x for each row

            for col in range(cols):
                self.scene.addEllipse(x - radius, y - radius, holedia, holedia, bolt_pen,bolt_brush)

                # Advance x
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge
        self.addDimensionsFlushedReversible(edge,gauge,crossgauge,cols)
        self.addInternalGapsFlushedReversible()
    
    def addInternalGapsFlushedReversible(self, margin=12.5):
        from PyQt5.QtGui import QPen, QFont, QBrush
        from PyQt5.QtCore import Qt, QPointF
        from PyQt5.QtGui import QPolygonF

        pen = QPen(Qt.darkMagenta, 1)
        pen.setStyle(Qt.SolidLine)

        label_text = f"{margin:.1f} mm"
        font = QFont()
        font.setPointSize(7)  # Increased font size

        pw = self.width
        ph = self.height

        # Internal gap lines and their label offsets (dx, dy)
        gap_lines = [
            # Top left
            ((0, margin, margin, margin), (margin + 4, margin - 10)),  # horizontal
            ((margin, 0, margin, margin), (margin + 4, 2)),            # vertical

            # Top right
            ((pw - margin, margin, pw, margin), (pw - margin - 30, margin - 10)),
            ((pw - margin, 0, pw - margin, margin), (pw - margin - 25, 2)),

            # Bottom left
            ((0, ph - margin, margin, ph - margin), (margin + 4, ph - margin - 15)),
            ((margin, ph - margin, margin, ph), (margin + 4, ph - margin + 2)),

            # Bottom right
            ((pw - margin, ph - margin, pw, ph - margin), (pw - margin - 30, ph - margin - 15)),
            ((pw - margin, ph - margin, pw - margin, ph), (pw - margin - 25, ph - margin + 2)),
        ]

        for (x1, y1, x2, y2), (tx, ty) in gap_lines:
            self.scene.addLine(x1, y1, x2, y2, pen)

            # Add label with clearer offset
            text_item = self.scene.addText(label_text)
            text_item.setFont(font)
            text_item.setPos(tx, ty)
    
    def addDimensionsFlushedReversible(self, edge, gauge, cross_gauge, cols, y_offset=20):
        """ 
        Draws clean, symmetric horizontal dimensions for even column layout:
        [edge] + N*gauge + cross_gauge + N*gauge + [edge]
        Uses self.addHorizontalDimension().
        """

        from PyQt5.QtGui import QPen
        from PyQt5.QtCore import Qt

        if cols % 2 != 0 or cols < 2:
            raise ValueError("Number of columns must be even and >= 2")

        pen = QPen(Qt.darkGreen, 1)
        pen.setStyle(Qt.DashLine)
        y = -y_offset

        x = 0
        segments = []

        # --- Left edge distance ---
        x1 = x
        x2 = x + edge
        segments.append(("edge", x1, x2))
        x = x2

        # --- Left-side gauge segments ---
        for _ in range((cols - 2) // 2):
            x1 = x
            x2 = x + gauge
            segments.append(("gauge", x1, x2))
            x = x2

        # --- Cross gauge ---
        x1 = x
        x2 = x + cross_gauge
        segments.append(("cross gauge", x1, x2))
        x = x2

        # --- Right-side gauge segments ---
        for _ in range((cols - 2) // 2):
            x1 = x
            x2 = x + gauge
            segments.append(("gauge", x1, x2))
            x = x2

        # --- Right edge distance ---
        x1 = x
        x2 = x + edge
        segments.append(("edge", x1, x2))

        # --- Draw all segments using your dimension method ---
        for label, x1, x2 in segments:
            self.addHorizontalDimension(x1, y, x2, y, f"{x2 - x1:.1f}", pen)
        plate_width = self.width
        y_plate = self.height + 20  # just below the plate

        self.addHorizontalDimension(0, y_plate, plate_width, y_plate, f"{plate_width:.1f} mm", pen)
                # --- Add vertical dimensions on left side for top half ---
        x_vdim = -30  # left of plate
        y_base = 12.5

        # 1. Flange thickness
        y1 = y_base
        y2 = y1 + self.flange_thick
        self.addVerticalDimension(x_vdim, y1, x_vdim, y2, f"{self.flange_thick:.1f}", pen)

        # 2. End distance
        y1 = y2
        y2 = y1 + self.End
        self.addVerticalDimension(x_vdim, y1, x_vdim, y2, f"{self.End:.1f}", pen)

        # 3. Pitch segments (top rows)
        for i in range(self.rows // 2 - 1):
            y1 = y2
            y2 = y1 + self.pitch
            self.addVerticalDimension(x_vdim, y1, x_vdim, y2, f"{self.pitch:.1f}", pen)

        # --- Add vertical dimensions on left side for bottom half ---
        y_base = self.height - 12.5

        # 1. Flange thickness
        y1 = y_base
        y2 = y1 - self.flange_thick
        self.addVerticalDimension(x_vdim, y2, x_vdim, y1, f"{self.flange_thick:.1f}", pen)

        # 2. End distance
        y1 = y2
        y2 = y1 - self.End
        self.addVerticalDimension(x_vdim, y2, x_vdim, y1, f"{self.End:.1f}", pen)

        # 3. Pitch segments (bottom rows)
        for i in range(self.rows // 2 - 1):
            y1 = y2
            y2 = y1 - self.pitch
            self.addVerticalDimension(x_vdim, y2, x_vdim, y1, f"{self.pitch:.1f}", pen)
        x_total_height = self.width + 20  # to the right of the plate
        y_top = 0
        y_bottom = self.height

        self.addVerticalDimension(x_total_height, y_top, x_total_height, y_bottom, f"{self.height:.1f} mm", pen)
    
    
    def createDrawingExtendedOneWay(self):
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPen, QColor, QBrush

        # === Input Parameters ===
        plate_height = self.height
        plate_width = self.width
        web_thickness = self.web_thick
        flange_thickness = self.flange_thick
        stiffener_height = self.stiffener_length
        stiffener_thickness = self.stiffener_thickness
        pitch = self.pitch
        end = self.End
        midbolts=self.middle_bolts
        rowsabovestiff=0
        crossgauge=self.CrossGauge
        edge=self.Edge
        gauge=self.Gauge
        cols=self.cols
        rows=self.rows
        # Margins
        h_gap = 12.5
        v_gap = 12.5
        holedia=self.hole_diameter
        radius=holedia/2
        # === Pens and Brushes ===
        outline_pen = QPen(Qt.blue, 2)
        red_pen = QPen(QColor("red"), 2)
        red_brush = QBrush(QColor("red"))
        black_pen = QPen(QColor("black"), 2)

        # === Setup Scene ===
        self.scene.setSceneRect(-40, -60, plate_width + 80, plate_height + 120)
        self.scene.clear()
        self.scene.setBackgroundBrush(Qt.lightGray)

        # === Draw Plate Boundary ===
        self.scene.addRect(0, 0, plate_width, plate_height, black_pen)

        # === Determine Effective Stiffener Height ===
        if end + pitch + end < stiffener_height:
            effective_stiffener_height = end + pitch + end
            rowsabovestiff=2
        else:
            effective_stiffener_height = 2 * end
            rowsabovestiff=1
        self.stiff_len=effective_stiffener_height
        # === Draw Top Stiffener ===
        stiffener_x = (plate_width - stiffener_thickness) / 2
        stiffener_y = 0
        self.scene.addRect(stiffener_x, stiffener_y, stiffener_thickness, effective_stiffener_height, red_pen, red_brush)

        # === Web and Flange Geometry ===
        top_flange_y = effective_stiffener_height
        top_flange_bottom_y = top_flange_y + flange_thickness
        bottom_flange_y = plate_height - v_gap
        bottom_flange_top_y = bottom_flange_y - flange_thickness

        web_x1 = (plate_width - web_thickness) / 2
        web_x2 = web_x1 + web_thickness
        web_y1 = top_flange_bottom_y
        web_y2 = bottom_flange_top_y
        weblen=web_y1-web_y2
        # === Draw Web ===
        self.scene.addLine(web_x1, web_y1, web_x1, web_y2, outline_pen)
        self.scene.addLine(web_x2, web_y1, web_x2, web_y2, outline_pen)

        # === Draw Top Flange (5 lines) ===
        self.scene.addLine(h_gap, top_flange_y, plate_width - h_gap, top_flange_y, outline_pen)
        self.scene.addLine(h_gap, top_flange_y, h_gap, top_flange_bottom_y, outline_pen)
        self.scene.addLine(plate_width - h_gap, top_flange_y, plate_width - h_gap, top_flange_bottom_y, outline_pen)
        self.scene.addLine(h_gap, top_flange_bottom_y, web_x1, top_flange_bottom_y, outline_pen)
        self.scene.addLine(web_x2, top_flange_bottom_y, plate_width - h_gap, top_flange_bottom_y, outline_pen)

        # === Draw Bottom Flange (5 lines) ===
        self.scene.addLine(h_gap, bottom_flange_y, plate_width - h_gap, bottom_flange_y, outline_pen)
        self.scene.addLine(h_gap, bottom_flange_top_y, h_gap, bottom_flange_y, outline_pen)
        self.scene.addLine(plate_width - h_gap, bottom_flange_top_y, plate_width - h_gap, bottom_flange_y, outline_pen)
        self.scene.addLine(h_gap, bottom_flange_top_y, web_x1, bottom_flange_top_y, outline_pen)
        self.scene.addLine(web_x2, bottom_flange_top_y, plate_width - h_gap, bottom_flange_top_y, outline_pen)
        total_span = 2 * edge + crossgauge
        extra_per_side = (cols - 2) // 2
        for _ in range(extra_per_side):
            total_span += 2 * gauge
        if total_span<= plate_width:
        # --- Adjust edge to center the bolt group ---
            edge += (plate_width - total_span) / 2
            
        y_bottom_bolt = plate_height - 12.5 - end -flange_thickness # From image: 12.5 mm gap, then e' up

        x = edge  # start x from edge

        for col in range(cols):
            self.scene.addEllipse(x - radius, y_bottom_bolt - radius, holedia, holedia, red_pen, red_brush)
            # Advance x for next column
            if col == 0 or col == 2:
                x += gauge
            elif col == 1:
                x += crossgauge
        #draw middle bolt
        if midbolts==1:
            print('drawing middle bolt')
            y_mid_bolt = plate_height - 12.5 - flange_thickness - abs(weblen / 2)
            x = edge  # Start x from adjusted edge
            for col in range(cols):
                print(f'x : {x} ,y : {y_mid_bolt} , col : {col}')
                self.scene.addEllipse(x - radius, y_mid_bolt - radius, holedia, holedia, red_pen, red_brush)
                # Advance x for next column
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge
        y_top_bolt = end  # distance from top of plate

        x = edge  # Start x from adjusted edge
        for col in range(cols):
            self.scene.addEllipse(x - radius, y_top_bolt - radius, holedia, holedia, red_pen, red_brush)
            # Advance x for next column
            if col == 0 or col == 2:
                x += gauge
            elif col == 1:
                x += crossgauge
        if rowsabovestiff == 2 :
            y_top_bolt = end + pitch
            x = edge  # Start x from adjusted edge
            for col in range(cols):
                self.scene.addEllipse(x - radius, y_top_bolt - radius, holedia, holedia, red_pen, red_brush)
                # Advance x for next column
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge
        remainingrows = rows - 1 - midbolts -rowsabovestiff
        self.remainingrows=remainingrows
        start_y = effective_stiffener_height + flange_thickness + end  # starting y position just below flange
        self.rowsabovestiff=rowsabovestiff
        for row in range(remainingrows):
            y = start_y + row * pitch
            x = edge  # reset x for each row

            for col in range(cols):
                self.scene.addEllipse(x - radius, y - radius, holedia, holedia, red_pen, red_brush)
                # Advance x for next column
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge
        self.addInternalGapsExtendedOneWay()
        self.addDimensionsExtendedOneWay(edge,self.Gauge,self.CrossGauge,self.cols)
    def addDimensionsExtendedOneWay(self, edge, gauge, cross_gauge, cols, y_offset=20):
        from PyQt5.QtGui import QPen, QFont
        from PyQt5.QtCore import Qt

        pen = QPen(Qt.darkGreen, 1)
        font = QFont()
        font.setPointSize(7)

        # === Draw vertical dimension for stiff_len from top ===
        x_dim_line = -15  # Position left of the plate
        y1 = 0
        y2 = self.stiff_len

        self.scene.addLine(x_dim_line, y1, x_dim_line, y2, pen)

        # Add label
        dim_label = f"{self.stiff_len:.1f} mm"
        text_item = self.scene.addText(dim_label)
        text_item.setFont(font)
        text_item.setPos(x_dim_line - 25, (y1 + y2) / 2 - 8) 
        # === Draw stacked vertical dimensions on right ===
        x_right = self.width + 20  # Position right of the plate
        current_y = 0  # Start from top

        # First end distance
        y_next = current_y + self.End
        self.addVerticalDimension(x_right, current_y, x_right, y_next, f"{self.End:.1f} mm", pen)
        current_y = y_next

        # If more than 1 row above stiffener, add pitch
        if self.rowsabovestiff > 1:
            y_next = current_y + self.pitch
            self.addVerticalDimension(x_right, current_y, x_right, y_next, f"{self.pitch:.1f} mm", pen)
            current_y = y_next

        # Add second end distance
        y_next = current_y + self.End
        self.addVerticalDimension(x_right, current_y, x_right, y_next, f"{self.End:.1f} mm", pen)
        # === Vertical Dimensions for Bolt Rows Below Stiffener ===
        y_start = y_next + self.flange_thick  # Below stiffener flange
        current_y = y_start

        if self.remainingrows >= 1:
            # First bolt row: end distance
            y_next = current_y + self.End
            self.addVerticalDimension(x_right, current_y, x_right, y_next, f"{self.End:.1f} mm", pen)
            current_y = y_next

        # Remaining rows: pitch
        for _ in range(self.remainingrows - 1):
            y_next = current_y + self.pitch
            self.addVerticalDimension(x_right, current_y, x_right, y_next, f"{self.pitch:.1f} mm", pen)
            current_y = y_next

        # === From bottom flange up to last bolt row ===
        y_bottom = self.height - 12.5 - self.flange_thick
        y_top = y_bottom - self.End
        self.addVerticalDimension(x_right, y_top, x_right, y_bottom, f"{self.End:.1f} mm", pen)
        from PyQt5.QtGui import QPen
        from PyQt5.QtCore import Qt

        if cols % 2 != 0 or cols < 2:
            raise ValueError("Number of columns must be even and >= 2")

        pen = QPen(Qt.darkGreen, 1)
        pen.setStyle(Qt.DashLine)
        y = -y_offset

        x = 0
        segments = []

        # --- Left edge distance ---
        x1 = x
        x2 = x + edge
        segments.append(("edge", x1, x2))
        x = x2

        # --- Left-side gauge segments ---
        for _ in range((cols - 2) // 2):
            x1 = x
            x2 = x + gauge
            segments.append(("gauge", x1, x2))
            x = x2

        # --- Cross gauge ---
        x1 = x
        x2 = x + cross_gauge
        segments.append(("cross gauge", x1, x2))
        x = x2

        # --- Right-side gauge segments ---
        for _ in range((cols - 2) // 2):
            x1 = x
            x2 = x + gauge
            segments.append(("gauge", x1, x2))
            x = x2

        # --- Right edge distance ---
        x1 = x
        x2 = x + edge
        segments.append(("edge", x1, x2))

        # --- Draw all segments using your dimension method ---
        for label, x1, x2 in segments:
            self.addHorizontalDimension(x1, y, x2, y, f"{x2 - x1:.1f}", pen)
        plate_width = self.width
        y_plate = self.height + 20  # just below the plate

        self.addHorizontalDimension(0, y_plate, plate_width, y_plate, f"{plate_width:.1f} mm", pen)
       
    def addInternalGapsExtendedOneWay(self, margin=12.5):
        from PyQt5.QtGui import QPen, QFont
        from PyQt5.QtCore import Qt

        pen = QPen(Qt.darkMagenta, 1)
        pen.setStyle(Qt.SolidLine)

        label_text = f"{margin:.1f} mm"
        font = QFont()
        font.setPointSize(7)

        pw = self.width
        ph = self.height
        stiff_y = self.stiff_len  # Bottom of stiffener

        # Internal gap lines and their label offsets
        gap_lines = [
            # Top left (only horizontal)
            ((0, stiff_y, margin, stiff_y), (margin + 4, stiff_y - 10)),

            # Top right (only horizontal)
            ((pw - margin, stiff_y, pw, stiff_y), (pw - margin - 30, stiff_y - 10)),

            # Bottom left
            ((0, ph - margin, margin, ph - margin), (margin + 4, ph - margin - 15)),
            ((margin, ph - margin, margin, ph), (margin + 4, ph - margin + 2)),

            # Bottom right
            ((pw - margin, ph - margin, pw, ph - margin), (pw - margin - 30, ph - margin - 15)),
            ((pw - margin, ph - margin, pw - margin, ph), (pw - margin - 25, ph - margin + 2)),
        ]

        for (x1, y1, x2, y2), (tx, ty) in gap_lines:
            self.scene.addLine(x1, y1, x2, y2, pen)

            text_item = self.scene.addText(label_text)
            text_item.setFont(font)
            text_item.setPos(tx, ty)

    def createDrawingExtendedTwoWay(self):
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPen, QColor, QBrush

        # === Input Parameters ===
        plate_height = self.height
        plate_width = self.width
        web_thickness = self.web_thick
        flange_thickness = self.flange_thick
        stiffener_height = self.stiffener_length
        stiffener_thickness = self.stiffener_thickness
        pitch = self.pitch
        end = self.End
        gauge= self.Gauge
        crossgauge=self.CrossGauge
        cols=self.cols
        rows=self.rows
        holedia=self.hole_diameter
        radius=holedia/2
        edge=self.Edge
        # Horizontal margin only
        h_gap = 12.5

        # === Pens and Brushes ===
        outline_pen = QPen(Qt.blue, 2)
        red_pen = QPen(QColor("red"), 2)
        red_brush = QBrush(QColor("red"))
        black_pen = QPen(QColor("black"), 2)

        # === Setup Scene ===
        self.scene.setSceneRect(-40, -60, plate_width + 80, plate_height + 120)
        self.scene.clear()
        self.scene.setBackgroundBrush(Qt.lightGray)

        # === Draw Plate Boundary ===
        self.scene.addRect(0, 0, plate_width, plate_height, black_pen)

        # === Determine Effective Stiffener Height (Top and Bottom) ===
        if end + pitch + end < stiffener_height:
            effective_stiffener_height = end + pitch + end
            rowsabovestiff = 2
        else:
            effective_stiffener_height = 2 * end
            rowsabovestiff = 1
        self.stiff_len = effective_stiffener_height
        self.rowsabovestiff = rowsabovestiff

        # === Draw Top Stiffener ===
        stiffener_x = (plate_width - stiffener_thickness) / 2
        self.scene.addRect(
            stiffener_x,
            0,
            stiffener_thickness,
            effective_stiffener_height,
            red_pen,
            red_brush
        )

        # === Draw Bottom Stiffener ===
        self.scene.addRect(
            stiffener_x,
            plate_height - effective_stiffener_height,
            stiffener_thickness,
            effective_stiffener_height,
            red_pen,
            red_brush
        )

        # === Calculate flange and web geometry ===
        top_flange_y = effective_stiffener_height
        top_flange_bottom_y = top_flange_y + flange_thickness

        bottom_flange_bottom_y = plate_height - effective_stiffener_height
        bottom_flange_top_y = bottom_flange_bottom_y - flange_thickness

        web_x1 = (plate_width - web_thickness) / 2
        web_x2 = web_x1 + web_thickness
        web_y1 = top_flange_bottom_y
        web_y2 = bottom_flange_top_y

        # === Draw Top Flange (5-line detail) ===
        self.scene.addLine(h_gap, top_flange_y, plate_width - h_gap, top_flange_y, outline_pen)
        self.scene.addLine(h_gap, top_flange_y, h_gap, top_flange_bottom_y, outline_pen)
        self.scene.addLine(plate_width - h_gap, top_flange_y, plate_width - h_gap, top_flange_bottom_y, outline_pen)
        self.scene.addLine(h_gap, top_flange_bottom_y, web_x1, top_flange_bottom_y, outline_pen)
        self.scene.addLine(web_x2, top_flange_bottom_y, plate_width - h_gap, top_flange_bottom_y, outline_pen)

        # === Draw Bottom Flange (5-line detail) ===
        self.scene.addLine(h_gap, bottom_flange_bottom_y, plate_width - h_gap, bottom_flange_bottom_y, outline_pen)
        self.scene.addLine(h_gap, bottom_flange_top_y, h_gap, bottom_flange_bottom_y, outline_pen)
        self.scene.addLine(plate_width - h_gap, bottom_flange_top_y, plate_width - h_gap, bottom_flange_bottom_y, outline_pen)
        self.scene.addLine(h_gap, bottom_flange_top_y, web_x1, bottom_flange_top_y, outline_pen)
        self.scene.addLine(web_x2, bottom_flange_top_y, plate_width - h_gap, bottom_flange_top_y, outline_pen)

        # === Draw Web (clean, between flanges only) ===
        self.scene.addLine(web_x1, web_y1, web_x1, web_y2, outline_pen)
        self.scene.addLine(web_x2, web_y1, web_x2, web_y2, outline_pen)
        total_span = 2 * edge + crossgauge
        extra_per_side = (cols - 2) // 2
        for _ in range(extra_per_side):
            total_span += 2 * gauge
        if total_span<= plate_width:
        # --- Adjust edge to center the bolt group ---
            edge += (plate_width - total_span) / 2
        x = edge
        y_top_bolt = self.End

        for col in range(cols):
            self.scene.addEllipse(x - radius, y_top_bolt - radius, holedia, holedia, red_pen, red_brush)
            if col == 0 or col == 2:
                x += gauge
            elif col == 1:
                x += crossgauge

# Optional second row above stiffener
        if self.rowsabovestiff == 2:
            x = edge
            y_top_bolt_2 = self.End + pitch
            for col in range(cols):
                self.scene.addEllipse(x - radius, y_top_bolt_2 - radius, holedia, holedia, red_pen, red_brush)
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge

# === Draw Bolt Rows from Bottom ===
        x = edge
        y_bottom_bolt = self.height - self.End

        for col in range(cols):
            self.scene.addEllipse(x - radius, y_bottom_bolt - radius, holedia, holedia, red_pen, red_brush)
            if col == 0 or col == 2:
                x += gauge
            elif col == 1:
                x += crossgauge

        # Optional second row below stiffener
        if self.rowsabovestiff == 2:
            x = edge
            y_bottom_bolt_2 = self.height - self.End - pitch
            for col in range(cols):
                self.scene.addEllipse(x - radius, y_bottom_bolt_2 - radius, holedia, holedia, red_pen, red_brush)
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge
        remainingrows=rows-2*self.rowsabovestiff-self.middle_bolts
        if self.middle_bolts==1:
            x = edge
            y_mid_bolt = self.height / 2

            for col in range(cols):
                self.scene.addEllipse(x - radius, y_mid_bolt - radius, holedia, holedia, red_pen, red_brush)
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge
        # === Split remaining rows symmetrically ===
        top_rows = (remainingrows + 1) // 2
        bottom_rows = remainingrows // 2

        # Determine starting y for top and bottom
        if self.rowsabovestiff == 2:
            last_top_y = self.End + pitch+flange_thickness
        else:
            last_top_y = self.End+flange_thickness

        if self.rowsabovestiff == 2:
            last_bottom_y = self.height - self.End - pitch-flange_thickness
        else:
            last_bottom_y = self.height - self.End-flange_thickness

        # === Draw top part of remaining rows ===
        for i in range(top_rows):
            y = last_top_y + (i + 1) * pitch  # start one pitch below the last top bolt
            x = edge
            for col in range(cols):
                self.scene.addEllipse(x - radius, y - radius, holedia, holedia, red_pen, red_brush)
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge

        # === Draw bottom part of remaining rows ===
        for i in range(bottom_rows):
            y = last_bottom_y - (i + 1) * pitch  # start one pitch above the last bottom bolt
            x = edge
            for col in range(cols):
                self.scene.addEllipse(x - radius, y - radius, holedia, holedia, red_pen, red_brush)
                if col == 0 or col == 2:
                    x += gauge
                elif col == 1:
                    x += crossgauge

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        from PyQt5.QtCore import QPointF
        from PyQt5.QtGui import QPolygonF
        from PyQt5.QtGui import QFont, QBrush
        from PyQt5.QtCore import Qt

        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 5
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
        text_item.setFont(font)
        text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 + 5)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        from PyQt5.QtCore import QPointF
        from PyQt5.QtGui import QPolygonF

        from PyQt5.QtGui import QFont, QBrush
        from PyQt5.QtCore import Qt

        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 5
        ext_length = 10

        # Extension lines
        self.scene.addLine(x1 - ext_length / 2, y1, x1 + ext_length / 2, y1, pen)
        self.scene.addLine(x2 - ext_length / 2, y2, x2 + ext_length / 2, y2, pen)

        # Determine direction (y1 to y2 or vice versa)
        up = y2 < y1

        # Arrowhead at y1
        poly1 = QPolygonF([
            QPointF(x1, y1),
            QPointF(x1 - arrow_size / 2, y1 + (arrow_size if up else -arrow_size)),
            QPointF(x1 + arrow_size / 2, y1 + (arrow_size if up else -arrow_size))
        ])
        arrow1 = self.scene.addPolygon(poly1, pen)
        arrow1.setBrush(QBrush(Qt.black))

        # Arrowhead at y2
        poly2 = QPolygonF([
            QPointF(x2, y2),
            QPointF(x2 - arrow_size / 2, y2 - (arrow_size if up else -arrow_size)),
            QPointF(x2 + arrow_size / 2, y2 - (arrow_size if up else -arrow_size))
        ])
        arrow2 = self.scene.addPolygon(poly2, pen)
        arrow2.setBrush(QBrush(Qt.black))

        # Text
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        text_item.setPos(x1 + 10, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
