import sys
from PySide6.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
                             QGraphicsScene)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtGui import QPolygonF, QBrush
from PySide6.QtCore import QPointF
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *

class BoltPatternGenerator(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2 , main = None):
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager

        self.connection = connection_obj
        self.main=main
        self.plate_height = main.plate.height
        self.plate_width = main.plate.length 
        self.hole_dia=main.bolt.bolt_diameter_provided
        self.rows=rows
        self.cols=cols
        if self.rows is None or self.rows == 0:
             self.rows = main.plate.bolts_one_line
        if self.cols is None or self.cols == 0:
             self.cols = main.plate.bolt_line
        if self.cols is None or self.cols == 0:
             self.cols = main.plate.bolt_line
        
        # Check if Strut Bolted module
        self.is_strut = False
        if self.main:
            try:
                self.is_strut = (self.main.module_name() == 'Struts Bolted to End Gusset')
            except AttributeError:
                pass
        
        print(self.plate_height,self.plate_width)
        output=main.output_values(True)
        dict1={i[0] : i[3] for i in output}
        for i in output:
            print(i)
        self.weldsize=0
        if 'Weld.Size' in dict1:
            self.weldsize=dict1['Weld.Size']
            
        self.member_height_designation = None
        if 'section_size.designation' in dict1:
             desig = str(dict1['section_size.designation'])
             # Expected format "60 x 60 x 4" or "ISA 60 x 60 x 6"
             parts = []
             if 'x' in desig:
                 parts = desig.split('x')
             elif 'X' in desig:
                 parts = desig.split('X')
             
             if parts:
                 try:
                     # parts[0] might be "ISA 60 " or "60 "
                     tup = parts[0].strip().split()
                     # Take the last token which should be the number
                     val_str = tup[-1]
                     self.member_height_designation = float(val_str)
                 except (ValueError, IndexError):
                     pass
                     
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
        
        # Center the window on the screen with the same dimensions
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = 800, 500
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel for parameter display
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Parameter display labels
        params = self.get_parameters()
        

        # Display the parameter values
        for key, value in params.items():
            param_layout = QHBoxLayout()
            param_label = QLabel(f'{key.title()} Distance :')
            param_label.setStyleSheet("font-size: 15px; font-weight: bold;")
            value_label = QLabel(f'{float(value):.2f}')
            value_label.setStyleSheet("font-size: 15px;")
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            left_layout.addLayout(param_layout)

        param_layout = QHBoxLayout()
        param_label = QLabel("(All Dimensions are in mm)")
        param_label.setStyleSheet("font-size: 12px; font-style: italic;")
        param_layout.addWidget(param_label)
        left_layout.addLayout(param_layout)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Right panel for the drawing using QGraphicsView
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        if self.theme.is_light():
            self.view.setBackgroundBrush(QBrush(Qt.white))
        else:
            self.view.setBackgroundBrush(QBrush(QColor("#4A4A4A")))
        # Create and add the drawing to the scene
        self.createDrawing(params)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.view, 3)
        
        self.content_widget.setLayout(main_layout)
        
        # Ensure the view shows all content
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
    def get_parameters(self):
        spacing_data = self.connection.spacing(status=True)  # Get actual values
        param_map = {}
        print('spacing_data length' , len(spacing_data))
        
        # Check if Strut Bolted module
        is_strut = False
        if self.main:
            try:
                # Import commonly used keys if needed or rely on string comparison since main.module_name returns string
                is_strut = (self.main.module_name() == 'Struts Bolted to End Gusset')
            except AttributeError:
                pass

        for item in spacing_data:
            key, _, _, value = item
            # print('key : ', key)
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
            elif key == 'Member.Depth':
                param_map['Member.Depth'] = float(value)

        # For Strut Bolted module, the interpretation of parameters changes for drawing.
        # The drawing assumes:
        #   'pitch' for vertical spacing (Y-axis)
        #   'gauge' for horizontal spacing (X-axis)
        #   'end' for vertical margin (Y-axis)
        #   'edge' for horizontal margin (X-axis)
        #
        # Osdag Core for Strut (Horizontal Member):
        #   KEY_OUT_PITCH: Axial/Horizontal spacing
        #   KEY_OUT_GAUGE: Transverse/Vertical spacing
        #   KEY_OUT_END_DIST: Axial/Horizontal margin
        #   KEY_OUT_EDGE_DIST: Transverse/Vertical margin
        
        if self.is_strut:
            # Map Strut's horizontal spacing (Pitch) to drawing's horizontal spacing (gauge)
            # Map Strut's vertical spacing (Gauge) to drawing's vertical spacing (pitch)
            drawing_gauge = param_map['pitch']
            drawing_pitch = param_map['gauge']
            
            # Map Strut's horizontal margin (End Dist) to drawing's horizontal margin (edge)
            # Map Strut's vertical margin (Edge Dist) to drawing's vertical margin (end)
            drawing_edge = param_map['end']
            drawing_end = param_map['edge']

            param_map['pitch'] = drawing_pitch
            param_map['gauge'] = drawing_gauge
            param_map['end'] = drawing_end
            param_map['edge'] = drawing_edge
            
            # If gauge1/gauge2 were present, they would also need to be remapped if they represent horizontal spacing.
            # Assuming for strut, 'gauge' is the primary transverse spacing.
            if param_map.get('gauge1', 0) != 0 or param_map.get('gauge2', 0) != 0:
                # If gauge1/gauge2 are used for strut, they would represent vertical spacing.
                # In the drawing, vertical spacing is 'pitch'.
                # So, if strut uses gauge1/gauge2, they should be mapped to drawing's pitch.
                # This scenario is less common for struts, but if it happens, it needs careful handling.
                # For now, we'll assume 'gauge' is the primary transverse spacing for strut.
                pass


        # Add hardcoded hole diameter
        param_map['hole'] = self.main.bolt.bolt_diameter_provided

        print("Extracted parameters:", param_map)

        return param_map

    def createDrawing(self, params):
        
        # Extract parameters
        pitch = params['pitch']
        end = params['end']
        if 'gauge' in params:
            gauge = params['gauge']
        else:
            gauge1 = params['gauge1']
            gauge2 = params['gauge2']
        edge = params['edge']
        hole_diameter = params['hole']
        
        # Calculate dimensions
        if 'gauge' in params:
            gauge1 = gauge
            gauge2 = gauge
        width = self.plate_width

        height = self.plate_height
        if self.is_strut:
             if self.member_height_designation is not None:
                 height = self.member_height_designation
             elif 'Member.Depth' in params:
                 height = params['Member.Depth']
        
        # Set up pens
        if self.theme.is_light():
            dimension_pen = QPen(Qt.black, 1.0)
        else:
            dimension_pen = QPen(QColor("#8A8A8A"), 1.0)
        weld_pen = QPen(Qt.red, 1)
        outline_pen = QPen(QColor("#723B17"), 2)
        red_brush = QBrush(Qt.red)

        # Dimension offsets
        h_offset = 60 # Increased to ensure left dimensions fit
        v_offset = 60
        
        # Create scene rectangle with extra space for dimensions
        # setSceneRect(x, y, w, h)
        self.scene.setSceneRect(-h_offset, -v_offset, 
                                width + 2*h_offset, height + 2*v_offset)
        
        # Draw rectangle
        background_brush = QBrush(QColor("#A7A796"))
        self.scene.addRect(0, 0, width, height, dimension_pen, background_brush)

        # Draw holes
        # Draw holes
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_strut:
                    # Strut Logic (Horizontal Member)
                    # X = Left Start + End Dist (First Bolt margin) + Column Index * Pitch
                    # Y = Top Start + Edge Dist + Row Index * Gauge
                    # Note: Using 'end' as horizontal margin (End Distance) and 'pitch' as horizontal spacing
                    # Using 'edge' as vertical margin (Edge Distance) and 'gauge' as vertical spacing
                    
                    x_center = end + col * pitch
                    # Assuming symmetric placement vertically or just simple pattern from top
                    y_center = edge + row * gauge1 # Use gauge1/gauge/gauge2 logic if needed, simplify to gauge
                    
                    x = x_center - hole_diameter / 2
                    y = y_center - hole_diameter / 2
                else:
                    # Fin Plate Logic (Vertical Member/Plate)
                    # Start from right edge (for example: total plate width - edge)
                    x_center = self.plate_width - edge

                    # Subtract gauges from right to left
                    for i in range(col):
                        x_center -= gauge1 if i % 2 == 0 else gauge2

                    # Y-position stays the same
                    y_center = end + row * pitch

                    # Top-left corner for drawing the circle
                    x = x_center - hole_diameter / 2
                    y = y_center - hole_diameter / 2

                # print(f"row: {row}, col: {col}, x: {x}, y: {y}")
                self.scene.addEllipse(x, y, hole_diameter, hole_diameter, outline_pen)
        
        if not self.is_strut:
            weld_size=self.weldsize
            self.scene.addRect(0, 0, weld_size, height, weld_pen,red_brush)

        print(params,dimension_pen)
        # Add dimensions
        self.addDimensions(params, dimension_pen, width, height)

    def addDimensions(self, params, pen, width, height):
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
        
        # Offsets for dimension lines
        h_offset = 15
        v_offset = 10
        
        if self.is_strut:
             # STRUT DIMENSIONS (Horizontal Layout)
             
             # Horizontal Dimensions (Top)
             # End Distance (Left Edge -> First Bolt Column)
             self.addHorizontalDimension(0, -h_offset, end, -h_offset, f"{end:g}", pen)
             
             # Pitch Spacing (Between Columns)
             for i in range(self.cols - 1):
                 x1 = end + i * pitch
                 x2 = end + (i + 1) * pitch
                 self.addHorizontalDimension(x1, -h_offset, x2, -h_offset, f"{pitch:g}", pen)
                 
             # Remaining Length (Last Bolt Column -> Right Edge)
             last_bolt_x = end + (self.cols - 1) * pitch
             rem_len = width - last_bolt_x
             self.addHorizontalDimension(last_bolt_x, -h_offset, width, -h_offset, f"{rem_len:g}", pen)
             
             # Vertical Dimensions (Right)
             # Edge Distance (Top Edge -> First Bolt Row)
             self.addVerticalDimension(width + v_offset, 0, width + v_offset, edge, f"{edge:g}", pen)
             
             # Gauge Spacing (Between Rows)
             for i in range(self.rows - 1):
                 y1 = edge + i * gauge1
                 y2 = edge + (i + 1) * gauge1
                 self.addVerticalDimension(width + v_offset, y1, width + v_offset, y2, f"{gauge1:g}", pen)
                 
             # Remaining Height (Last Bolt Row -> Bottom Edge)
             last_bolt_y = edge + (self.rows - 1) * gauge1
             rem_h = height - last_bolt_y
             self.addVerticalDimension(width + v_offset, last_bolt_y, width + v_offset, height, f"{rem_h:g}", pen)
             
             # Overall Height (Left)
             self.addVerticalDimension(-v_offset, 0, -v_offset, height, f"{height:g}", pen)
             
             # Overall Width (Bottom) - Optional but good for complete member detail
             # self.addHorizontalDimension(0, height + h_offset, width, height + h_offset, f"{width:g}", pen)

        else:
            # FIN PLATE LOGIC (Vertical Layout)
            
            # Add horizontal dimensions (Gauge/Edge from Right)
            x_start = width
            segments = []
            # First edge
            segments.append(('edge', x_start-edge, x_start ))
            x_start -=edge
        
            # Last edge
            segments.append(('edge', 0, x_start))

            # Draw each segment
            for label, x1, x2 in segments:
                value = x2 - x1
                self.addHorizontalDimension(x1, -h_offset + 5, x2, -h_offset + 5, f"{value:g}", pen)
            # Add vertical dimensions (Pitch/End from Top)
            self.addVerticalDimension(width + v_offset, 0, width + v_offset, end, f"{end:g}", pen)
            for i in range(self.rows - 1):
                self.addVerticalDimension(width + v_offset, end + i * pitch, width + v_offset, end + (i + 1) * pitch, f"{pitch:g}", pen)
            
            # Add bottom end distance dimension
            last_bolt_y = end + (self.rows - 1) * pitch
            rem_len = height - last_bolt_y
            self.addVerticalDimension(width + v_offset, last_bolt_y, width + v_offset, height, f"{rem_len:g}", pen)
            
            # Add left side dimension
            self.addVerticalDimension(-v_offset, 0, -v_offset, height, f"{height:g}", pen)

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        try:
            val = float(text)
            if val == 0:
                return
        except ValueError:
            pass
            
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 3
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
        
        # Add text
        text_item = self.scene.addText(text)
        font = QFont()
        font.setPointSize(5)
        text_item.setFont(font)
        if self.theme.is_light():
            text_item.setDefaultTextColor(Qt.black)
        else:
            text_item.setDefaultTextColor(Qt.white)
        
        if y1 < 0:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 15)
        else:
            text_item.setPos((x1 + x2) / 2 - text_item.boundingRect().width() / 2, y1 - 15)

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        try:
            val = float(text)
            if val == 0:
                return
        except ValueError:
            pass

        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = 3
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
        font.setPointSize(5)
        text_item.setFont(font)
        if self.theme.is_light():
            text_item.setDefaultTextColor(Qt.black)
        else:
            text_item.setDefaultTextColor(Qt.white)

        if x1 < 0:
            text_item.setPos(x1 - text_item.boundingRect().width(), (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
        else:
            text_item.setPos(x1, (y1 + y2) / 2 - text_item.boundingRect().height() / 2)
