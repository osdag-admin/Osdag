import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
    QGraphicsScene, QGraphicsRectItem
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPolygonF, QBrush
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *


class C2CEndPlateDetails(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2, main=None):
        if main:
            self.flag = main[1]
            main = main[0]

        super().__init__()
        self.connection = connection_obj
        data = main.output_values(True)

        dict1 = {i[0]: i[3] for i in data}

        self.plate_width = float(dict1['Plate.Height'])
        self.plate_length = float(dict1['Plate.Length'])
        self.stiffener_length = float(dict1['Stiffener.Width'])
        self.stiffener_thickness = float(dict1['Stiffener.Thickness'])
        self.web_thickness = float(main.section.web_thickness)
        self.flange_thickness = float(main.section.flange_thickness)
        self.webdetail_width = self.plate_width - 2 * self.stiffener_length
        self.webdetail_len = self.plate_length
        self.hole_dia = float(dict1['Bolt.Diameter'])

        webspacing = dict1['Bolt.web_bolts'][1]
        flangespacing = dict1['Bolt.flange_bolts'][1]
        flangespacing = flangespacing(True)
        webspacing = webspacing(True)

        dict2 = {i[1]: i[3] for i in webspacing}

        self.web_bolts = int(dict2['No. of Bolts (along web)'])
        self.pitch1 = float(dict2.get('Pitch 1-2', 0))
        self.pitch2 = float(dict2.get('Pitch 2-3', 0))
        self.pitch3 = float(dict2.get('Pitch 3-4', 0))
        self.pitch4 = float(dict2.get('Pitch 4-5', 0))
        self.web_end = float(dict2['End Distance (mm)'])

        dict3 = {i[0]: i[3] for i in flangespacing}
        self.flangeend = float(dict3.get('Bolt.EndDist', 45))
        self.boltoneside = int(dict3.get('ColumnEndPlate.nbf', 1))
        self.flangetotal = int(dict3.get('ColumnEndPlate.nbftotal', 4))
        self.flangepitch = float(dict3.get('ColumnEndPlate.p2_flange', 0))

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
        width, height = 700, 450
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

        main_layout = QHBoxLayout()

        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        values_to_display = {
            'Plate Length (mm)': self.plate_length,
            'Plate Width (mm)': self.plate_width,
            'Bolt Diameter (mm)': self.hole_dia,
            'Pitch Distance 1 (mm)': self.pitch1,
            'Pitch Distance 2 (mm)': self.pitch2,
            'Pitch Distance 3 (mm)': self.pitch3,
            'Pitch Distance 4 (mm)': self.pitch4,
            'End Distance (mm)': self.web_end,
            'Flange End Distance (mm)': self.flangeend,
            'Number of Rows': self.web_bolts / 2 if self.web_bolts else 0,
            'Number of Columns': 2,
            'Bolts One Side': self.boltoneside,
            'Total Flange Bolts': self.flangetotal
        }

        for key, value in values_to_display.items():
            label = QLabel(f"<b>{key}:</b> {value}")
            left_layout.addWidget(label)

        unit_label = QLabel("(All dimensions are in mm)")
        unit_font = QFont()
        unit_font.setItalic(True)
        unit_label.setFont(unit_font)
        left_layout.addWidget(unit_label)
        left_layout.addStretch()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.scene.setBackgroundBrush(Qt.white)

        main_layout.addWidget(left_panel, stretch=1)
        main_layout.addWidget(self.view, stretch=2)

        self.fontsize = 10
        self.arrowsize = 10

        if self.plate_length > 1200 or self.plate_width > 1200:
            self.fontsize = 5
            self.arrowsize = 5
        elif self.plate_length > 600 or self.plate_width > 600:
            self.fontsize = 10
            self.arrowsize = 10

        self.createDrawing()

        if self.plate_length > 1200 or self.plate_width > 1200:
            self.view.resetTransform()
            self.view.scale(0.4, 0.4)
        elif self.plate_length > 600 or self.plate_width > 600:
            self.view.resetTransform()
            self.view.scale(0.75, 0.75)

        self.content_widget.setLayout(main_layout)

    def draw_welded_plate(self, x, y, width, height, center_gap=10):
        plate_fill = QBrush(QColor("#b7b4a8"))
        black_border_pen = QPen(Qt.black)
        black_border_pen.setWidth(1)
        orange_fill = QBrush(QColor("orange"))

        strip_thickness = 8
        edge_inset = 2

        base_rect = QGraphicsRectItem(x, y, width, height)
        base_rect.setPen(Qt.NoPen)
        base_rect.setBrush(plate_fill)
        self.scene.addItem(base_rect)

        top_strip = QGraphicsRectItem(
            x + edge_inset,
            y + edge_inset,
            width - (2 * edge_inset),
            strip_thickness
        )
        top_strip.setPen(Qt.NoPen)
        top_strip.setBrush(orange_fill)
        self.scene.addItem(top_strip)

        bottom_strip = QGraphicsRectItem(
            x + edge_inset,
            y + height - strip_thickness - edge_inset,
            width - (2 * edge_inset),
            strip_thickness
        )
        bottom_strip.setPen(Qt.NoPen)
        bottom_strip.setBrush(orange_fill)
        self.scene.addItem(bottom_strip)

        cx = x + width / 2
        gap = center_gap / 2
        y1 = y + edge_inset
        y2 = y + height - edge_inset

        center_strip = QGraphicsRectItem(
            cx - gap,
            y1,
            center_gap,
            y2 - y1
        )
        center_strip.setPen(Qt.NoPen)
        center_strip.setBrush(orange_fill)
        self.scene.addItem(center_strip)

        self.scene.addLine(x, y, x, y + height, black_border_pen)
        self.scene.addLine(x + width, y, x + width, y + height, black_border_pen)
        self.scene.addLine(x, y, x + width, y, black_border_pen)
        self.scene.addLine(x, y + height, x + width, y + height, black_border_pen)

    def createDrawing(self):
        dim_pen = QPen(Qt.black)
        dim_pen.setWidth(2)

        bolt_pen = QPen(QColor("#8B4A1F"))
        bolt_pen.setWidth(5)
        bolt_brush = QBrush(Qt.NoBrush)

        if self.flag == 0:
            self.draw_web_spacing(dim_pen, bolt_pen, bolt_brush)
        else:
            self.draw_flange_spacing(dim_pen, bolt_pen, bolt_brush)

    def draw_web_spacing(self, dim_pen, bolt_pen, bolt_brush):
        x0 = 0
        y0 = 0

        plate_len = self.webdetail_len
        plate_wid = self.webdetail_width
        web_thick = self.web_thickness
        flange_thick = self.flange_thickness
        hole_dia = self.hole_dia
        web_end = self.web_end

        self.draw_welded_plate(x0, y0, plate_len, plate_wid, center_gap=10)

        center_x = x0 + plate_len / 2

        self.addHorizontalDimension(
            x0, -30,
            x0 + plate_len, -30,
            f"{plate_len} mm", dim_pen
        )

        self.addVerticalDimension(
            x0 + plate_len + 30, y0,
            x0 + plate_len + 30, y0 + plate_wid,
            f"{plate_wid} mm", dim_pen
        )

        num_rows = int(self.web_bolts / 2)
        x_left = center_x - web_thick / 2 - web_end
        x_right = center_x + web_thick / 2 + web_end
        y_pos = y0 + flange_thick + web_end
        pitch_list = [self.pitch1, self.pitch2, self.pitch3, self.pitch4]

        bolt_centers_y = []
        for row in range(num_rows):
            bolt_centers_y.append(y_pos)

            self.scene.addEllipse(
                x_left - hole_dia / 2,
                y_pos - hole_dia / 2,
                hole_dia, hole_dia,
                bolt_pen, bolt_brush
            )
            self.scene.addEllipse(
                x_right - hole_dia / 2,
                y_pos - hole_dia / 2,
                hole_dia, hole_dia,
                bolt_pen, bolt_brush
            )

            if row < num_rows - 1:
                pitch_index = min(row, len(pitch_list) - 1)
                y_pos += pitch_list[pitch_index]

        # Small diameter line first, directly below ring and outside diagram
        x_dia_center = x_right
        y_dia = y0 + plate_wid + 12
        self.addHorizontalDimension(
            x_dia_center - hole_dia / 2, y_dia,
            x_dia_center + hole_dia / 2, y_dia,
            f"{hole_dia:.1f} mm",
            dim_pen
        )

        # Long bottom chain line below the small diameter line
        y_chain = y_dia + 35

        self.addHorizontalDimension(
            x0, y_chain,
            x_left, y_chain,
            f"{round(x_left - x0, 1)} mm",
            dim_pen
        )
        self.addHorizontalDimension(
            x_left, y_chain,
            x_right, y_chain,
            f"{round(x_right - x_left, 1)} mm",
            dim_pen
        )
        self.addHorizontalDimension(
            x_right, y_chain,
            x0 + plate_len, y_chain,
            f"{round((x0 + plate_len) - x_right, 1)} mm",
            dim_pen
        )

        x_dim = -20
        if bolt_centers_y:
            self.addVerticalDimension(
                x_dim, y0,
                x_dim, bolt_centers_y[0],
                f"{round(bolt_centers_y[0] - y0, 1)} mm",
                dim_pen
            )

            for i in range(len(bolt_centers_y) - 1):
                pitch_val = round(bolt_centers_y[i + 1] - bolt_centers_y[i], 1)
                self.addVerticalDimension(
                    x_dim, bolt_centers_y[i],
                    x_dim, bolt_centers_y[i + 1],
                    f"{pitch_val} mm",
                    dim_pen
                )

            self.addVerticalDimension(
                x_dim, bolt_centers_y[-1],
                x_dim, y0 + plate_wid,
                f"{round((y0 + plate_wid) - bolt_centers_y[-1], 1)} mm",
                dim_pen
            )

    def draw_flange_spacing(self, dim_pen, bolt_pen, bolt_brush):
        x0 = 0
        y0 = 0

        plate_len = self.plate_length
        plate_wid = self.plate_width / 2
        web_thick = self.web_thickness
        hole_dia = self.hole_dia
        edge = self.flangeend if self.flangeend else 45.0

        self.draw_welded_plate(x0, y0, plate_len, plate_wid, center_gap=10)

        center_x = x0 + plate_len / 2
        center_y = y0 + plate_wid / 2

        self.addHorizontalDimension(
            x0, -30,
            x0 + plate_len, -30,
            f"{plate_len} mm", dim_pen
        )

        self.addVerticalDimension(
            x0 + plate_len + 30, y0,
            x0 + plate_len + 30, y0 + plate_wid,
            f"{plate_wid} mm", dim_pen
        )

        x_left = center_x - web_thick / 2 - edge
        x_right = center_x + web_thick / 2 + edge
        y_bolt = center_y

        self.scene.addEllipse(
            x_left - hole_dia / 2,
            y_bolt - hole_dia / 2,
            hole_dia, hole_dia,
            bolt_pen, bolt_brush
        )
        self.scene.addEllipse(
            x_right - hole_dia / 2,
            y_bolt - hole_dia / 2,
            hole_dia, hole_dia,
            bolt_pen, bolt_brush
        )

        # Small diameter line first, directly below ring and outside diagram
        x_dia_center = x_right
        y_dia = y0 + plate_wid + 12
        self.addHorizontalDimension(
            x_dia_center - hole_dia / 2, y_dia,
            x_dia_center + hole_dia / 2, y_dia,
            f"{hole_dia:.1f} mm",
            dim_pen
        )

        # Long bottom chain line below the small diameter line
        y_chain = y_dia + 35

        self.addHorizontalDimension(
            x0, y_chain,
            x_left, y_chain,
            f"{round(x_left - x0, 1)} mm",
            dim_pen
        )
        self.addHorizontalDimension(
            x_left, y_chain,
            x_right, y_chain,
            f"{round(x_right - x_left, 1)} mm",
            dim_pen
        )
        self.addHorizontalDimension(
            x_right, y_chain,
            x0 + plate_len, y_chain,
            f"{round((x0 + plate_len) - x_right, 1)} mm",
            dim_pen
        )

        x_dim = -20
        self.addVerticalDimension(
            x_dim, y0,
            x_dim, y_bolt,
            f"{round(y_bolt - y0, 1)} mm",
            dim_pen
        )
        self.addVerticalDimension(
            x_dim, y_bolt,
            x_dim, y0 + plate_wid,
            f"{round((y0 + plate_wid) - y_bolt, 1)} mm",
            dim_pen
        )

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = self.arrowsize
        ext_length = 10

        self.scene.addLine(x1, y1 - ext_length / 2, x1, y1 + ext_length / 2, pen)
        self.scene.addLine(x2, y2 - ext_length / 2, x2, y2 + ext_length / 2, pen)

        points_left = [
            (x1, y1),
            (x1 + arrow_size, y1 - arrow_size / 2),
            (x1 + arrow_size, y1 + arrow_size / 2)
        ]
        polygon_left = self.scene.addPolygon(
            QPolygonF([QPointF(x, y) for x, y in points_left]), pen
        )
        polygon_left.setBrush(QBrush(Qt.black))

        points_right = [
            (x2, y2),
            (x2 - arrow_size, y2 - arrow_size / 2),
            (x2 - arrow_size, y2 + arrow_size / 2)
        ]
        polygon_right = self.scene.addPolygon(
            QPolygonF([QPointF(x, y) for x, y in points_right]), pen
        )
        polygon_right.setBrush(QBrush(Qt.black))

        text_item = self.scene.addText(str(text))
        font = QFont()
        font.setPointSize(self.fontsize)
        text_item.setFont(font)

        if y1 < 0:
            text_item.setPos(
                (x1 + x2) / 2 - text_item.boundingRect().width() / 2,
                y1 - 25
            )
        else:
            text_item.setPos(
                (x1 + x2) / 2 - text_item.boundingRect().width() / 2,
                y1 + 5
            )

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = self.arrowsize
        ext_length = 10

        self.scene.addLine(x1 - ext_length / 2, y1, x1 + ext_length / 2, y1, pen)
        self.scene.addLine(x2 - ext_length / 2, y2, x2 + ext_length / 2, y2, pen)

        if y2 > y1:
            points_top = [
                (x1, y1),
                (x1 - arrow_size / 2, y1 + arrow_size),
                (x1 + arrow_size / 2, y1 + arrow_size)
            ]
            polygon_top = self.scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in points_top]), pen
            )
            polygon_top.setBrush(QBrush(Qt.black))

            points_bottom = [
                (x2, y2),
                (x2 - arrow_size / 2, y2 - arrow_size),
                (x2 + arrow_size / 2, y2 - arrow_size)
            ]
            polygon_bottom = self.scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen
            )
            polygon_bottom.setBrush(QBrush(Qt.black))
        else:
            points_top = [
                (x2, y2),
                (x2 - arrow_size / 2, y2 + arrow_size),
                (x2 + arrow_size / 2, y2 + arrow_size)
            ]
            polygon_top = self.scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in points_top]), pen
            )
            polygon_top.setBrush(QBrush(Qt.black))

            points_bottom = [
                (x1, y1),
                (x1 - arrow_size / 2, y1 - arrow_size),
                (x1 + arrow_size / 2, y1 - arrow_size)
            ]
            polygon_bottom = self.scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen
            )
            polygon_bottom.setBrush(QBrush(Qt.black))

        text_item = self.scene.addText(str(text))
        font = QFont()
        font.setPointSize(self.fontsize)
        text_item.setFont(font)

        if x1 < 0:
            text_item.setPos(
                x1 - 10 - text_item.boundingRect().width(),
                (y1 + y2) / 2 - text_item.boundingRect().height() / 2
            )
        else:
            text_item.setPos(
                x1 + 15,
                (y1 + y2) / 2 - text_item.boundingRect().height() / 2
            )