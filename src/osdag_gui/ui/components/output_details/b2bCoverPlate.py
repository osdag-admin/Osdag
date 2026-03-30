import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGraphicsView,
    QSizeGrip,
    QGraphicsScene,
    QGraphicsRectItem,
)
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPolygonF, QBrush

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *


class B2BCoverPlateDetails(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2, main=None):
        web = False
        if main:
            web = main[1]
            main = main[0]

        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager
        self.connection = connection_obj

        data = main.output_values(True)
        dict1 = {i[0]: i[3] for i in data}

        for i in dict1:
            print(f"{i} : {dict1[i]}")

        if web is True:
            self.plate_length = dict1["Web_Plate.Height (mm)"]
            self.plate_width = dict1["Web_Plate.Width"]
            self.bolt_diameter = dict1["Bolt.Diameter"]

            web_capcity = dict1["Web_plate.spacing"][1]
            print(web_capcity(True))
            data2 = web_capcity(True)
            for i in range(len(data2)):
                print(f"{i} : {data2[i]}")

            self.pitch = data2[2][3]
            self.End = data2[3][3]
            self.Gauge = data2[4][3]
            self.Edge = data2[5][3]

            bolt_cap = dict1["Web Bolt.Capacities"][1]
            print(bolt_cap(True))
            bolt_cap = bolt_cap(True)

        else:
            self.plate_length = dict1["Flange_Plate.Width (mm)"]
            self.plate_width = dict1["flange_plate.Length"]
            self.bolt_diameter = dict1["Bolt.Diameter"]

            flange_capcity = dict1["Web_plate.spacing"][1]
            data2 = flange_capcity(True)

            self.pitch = data2[2][3]
            self.End = data2[3][3]
            self.Gauge = data2[4][3]
            self.Edge = data2[5][3]

            bolt_cap = dict1["Bolt.Capacities"][1]
            print(bolt_cap(True))
            bolt_cap = bolt_cap(True)

        self.cols = int(bolt_cap[1][3])
        self.rows = int(bolt_cap[2][3] / self.cols)

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

        print(
            f"""
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
        """
        )

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)

        params = self.get_parameters()

        for key, value in params.items():
            if key in ["Number of Columns", "Number of Rows"]:
                label_text = f"{key}:"
            else:
                label_text = f"{key} :"

            param_label = QLabel(label_text)
            param_label.setStyleSheet(
                "font-size:14px; font-weight:600; color:#101010;"
            )

            value_label = QLabel(f"{value:.2f}" if isinstance(value, (int, float)) else f"{value}")
            value_label.setStyleSheet(
                "font-size:14px; font-weight:500; color:#202020;"
            )

            param_layout = QHBoxLayout()
            param_layout.setSpacing(10)
            param_layout.addWidget(param_label)
            param_layout.addWidget(value_label)
            param_layout.addStretch()

            left_layout.addLayout(param_layout)

        # Only added this note, nothing removed
        note_label = QLabel("(All Dimensions are in mm)")
        note_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-style: italic;
                color: #202020;
                margin-top: 6px;
            }
        """)
        left_layout.addWidget(note_label)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(Qt.white))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setBackgroundBrush(QBrush(Qt.white))
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.view.setStyleSheet("""
            QGraphicsView {
                background-color: white;
                border: none;
            }
        """)

        self.fontsize = 10
        self.arrowsize = 10

        try:
            pl = float(self.plate_length)
            pw = float(self.plate_width)
        except (TypeError, ValueError):
            pl, pw = 0, 0

        if pl > 1200 or pw > 1200:
            self.fontsize = 12
            self.arrowsize = 12
        elif pl > 600 or pw > 600:
            self.fontsize = 7.5
            self.arrowsize = 7.5

        self.createDrawing()

        if pl > 1200 or pw > 1200:
            self.view.resetTransform()
            self.view.scale(0.35, 0.35)
        elif pl > 600 or pw > 600:
            self.view.resetTransform()
            self.view.scale(0.5, 0.5)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.view, 3)

        self.content_widget.setLayout(main_layout)

    def get_parameters(self):
        return {
            "Plate Length": self.plate_length,
            "Plate Width": self.plate_width,
            "Bolt Diameter": self.bolt_diameter,
            "Pitch Distance": self.pitch,
            "End Distance": self.End,
            "Gauge Distance": self.Gauge,
            "Edge Distance": self.Edge,
            "Number of Columns": self.cols,
            "Number of Rows": self.rows,
        }

    def createDrawing(self):
        try:
            plate_length = float(self.plate_length)
            plate_width = float(self.plate_width)
            hole_dia = float(self.bolt_diameter)
            pitch = float(self.pitch)
            gauge = float(self.Gauge)
            end = float(self.End)
            edge = float(self.Edge)
        except (TypeError, ValueError):
            print("Invalid plate dimensions")
            return

        self.scene.clear()
        self.scene.setBackgroundBrush(QBrush(Qt.white))

        plate_fill_color = QColor("#B8B7AA")
        plate_border_color = QColor("#000000")
        dim_color = QColor("#000000")
        bolt_ring_color = QColor("#8B4A1D")
        bolt_inner_color = plate_fill_color

        dim_pen = QPen(dim_color)
        dim_pen.setWidth(2)

        plate_pen = QPen(plate_border_color)
        plate_pen.setWidth(2)

        bolt_pen = QPen(bolt_ring_color)
        bolt_pen.setWidth(5)

        rect_item = QGraphicsRectItem(QRectF(0, 0, plate_length, plate_width))
        rect_item.setPen(plate_pen)
        rect_item.setBrush(QBrush(plate_fill_color))
        self.scene.addItem(rect_item)

        self.addHorizontalDimension(
            0,
            -30,
            plate_length,
            -30,
            f"{plate_length:.0f}" if plate_length.is_integer() else f"{plate_length}",
            dim_pen,
        )

        self.addVerticalDimension(
            plate_length + 30,
            0,
            plate_length + 30,
            plate_width,
            f"{plate_width:.0f}" if plate_width.is_integer() else f"{plate_width}",
            dim_pen,
        )

        rows = int(self.rows)
        cols = int(self.cols)
        radius = hole_dia / 2

        bolt_x_positions = []
        bolt_y_positions = []

        def draw_bolt(x_center, y_center):
            self.scene.addEllipse(
                x_center - radius,
                y_center - radius,
                hole_dia,
                hole_dia,
                bolt_pen,
                QBrush(bolt_inner_color),
            )

        if rows % 2 != 0:
            y_center = plate_width / 2
            bolt_y_positions.append(y_center)

            for i in range(cols // 2):
                x_center = edge + i * gauge
                bolt_x_positions.append(x_center)
                draw_bolt(x_center, y_center)

            for i in range(cols // 2):
                x_center = plate_length - edge - i * gauge
                bolt_x_positions.append(x_center)
                draw_bolt(x_center, y_center)

            if cols % 2 != 0:
                x_center = plate_length / 2
                bolt_x_positions.append(x_center)
                draw_bolt(x_center, y_center)

        if cols % 2 != 0 and rows % 2 == 0:
            x_center = plate_length / 2
            bolt_x_positions.append(x_center)

            for j in range(rows // 2):
                y_center_top = end + j * pitch
                y_center_bottom = plate_width - end - j * pitch

                bolt_y_positions.append(y_center_top)
                bolt_y_positions.append(y_center_bottom)

                draw_bolt(x_center, y_center_top)
                draw_bolt(x_center, y_center_bottom)

        for row in range(rows):
            if row < rows // 2:
                y_center = end + row * pitch
            else:
                row_from_bottom = row - rows // 2
                y_center = plate_width - end - row_from_bottom * pitch

            bolt_y_positions.append(y_center)

            for i in range(cols // 2):
                x_center = edge + i * gauge
                bolt_x_positions.append(x_center)
                draw_bolt(x_center, y_center)

            for i in range(cols // 2):
                x_center = plate_length - edge - i * gauge
                bolt_x_positions.append(x_center)
                draw_bolt(x_center, y_center)

        bolt_x_positions = sorted(list(set(bolt_x_positions)))
        bolt_y_positions = sorted(list(set(bolt_y_positions)))

        h_dim_y = plate_width + 30
        x_positions = [0] + bolt_x_positions + [plate_length]

        for i in range(len(x_positions) - 1):
            x1 = x_positions[i]
            x2 = x_positions[i + 1]
            distance = abs(x2 - x1)
            self.addHorizontalDimension(
                x1, h_dim_y, x2, h_dim_y, f"{distance:.1f}", dim_pen
            )

        v_dim_x = -30
        y_positions = [0] + bolt_y_positions + [plate_width]

        for i in range(len(y_positions) - 1):
            y1 = y_positions[i]
            y2 = y_positions[i + 1]
            distance = abs(y2 - y1)
            self.addVerticalDimension(
                v_dim_x, y1, v_dim_x, y2, f"{distance:.1f}", dim_pen
            )

        margin = 80
        self.scene.setSceneRect(
            -margin,
            -margin,
            plate_length + 2 * margin,
            plate_width + 2 * margin,
        )

    def addHorizontalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = float(self.arrowsize)
        ext_length = 10

        self.scene.addLine(x1, y1 - ext_length / 2, x1, y1 + ext_length / 2, pen)
        self.scene.addLine(x2, y2 - ext_length / 2, x2, y2 + ext_length / 2, pen)

        points_left = [
            (x1, y1),
            (x1 + arrow_size, y1 - arrow_size / 2),
            (x1 + arrow_size, y1 + arrow_size / 2),
        ]
        polygon_left = self.scene.addPolygon(
            QPolygonF([QPointF(x, y) for x, y in points_left]), pen
        )
        polygon_left.setBrush(QBrush(Qt.black))

        points_right = [
            (x2, y2),
            (x2 - arrow_size, y2 - arrow_size / 2),
            (x2 - arrow_size, y2 + arrow_size / 2),
        ]
        polygon_right = self.scene.addPolygon(
            QPolygonF([QPointF(x, y) for x, y in points_right]), pen
        )
        polygon_right.setBrush(QBrush(Qt.black))

        text_item = self.scene.addText(text)
        font = QFont("Arial")
        font.setPointSizeF(float(self.fontsize))
        font.setWeight(QFont.Medium)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black)

        if y1 < 0:
            text_item.setPos(
                (x1 + x2) / 2 - text_item.boundingRect().width() / 2,
                y1 - 25,
            )
        else:
            text_item.setPos(
                (x1 + x2) / 2 - text_item.boundingRect().width() / 2,
                y1 + 5,
            )

    def addVerticalDimension(self, x1, y1, x2, y2, text, pen):
        self.scene.addLine(x1, y1, x2, y2, pen)
        arrow_size = float(self.arrowsize)
        ext_length = 10

        self.scene.addLine(x1 - ext_length / 2, y1, x1 + ext_length / 2, y1, pen)
        self.scene.addLine(x2 - ext_length / 2, y2, x2 + ext_length / 2, y2, pen)

        if y2 > y1:
            points_top = [
                (x1, y1),
                (x1 - arrow_size / 2, y1 + arrow_size),
                (x1 + arrow_size / 2, y1 + arrow_size),
            ]
            polygon_top = self.scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in points_top]), pen
            )
            polygon_top.setBrush(QBrush(Qt.black))

            points_bottom = [
                (x2, y2),
                (x2 - arrow_size / 2, y2 - arrow_size),
                (x2 + arrow_size / 2, y2 - arrow_size),
            ]
            polygon_bottom = self.scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen
            )
            polygon_bottom.setBrush(QBrush(Qt.black))
        else:
            points_top = [
                (x2, y2),
                (x2 - arrow_size / 2, y2 + arrow_size),
                (x2 + arrow_size / 2, y2 + arrow_size),
            ]
            polygon_top = self.scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in points_top]), pen
            )
            polygon_top.setBrush(QBrush(Qt.black))

            points_bottom = [
                (x1, y1),
                (x1 - arrow_size / 2, y1 - arrow_size),
                (x1 + arrow_size / 2, y1 - arrow_size),
            ]
            polygon_bottom = self.scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in points_bottom]), pen
            )
            polygon_bottom.setBrush(QBrush(Qt.black))

        text_item = self.scene.addText(text)
        font = QFont("Arial")
        font.setPointSizeF(float(self.fontsize))
        font.setWeight(QFont.Medium)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.black)

        if x1 < 0:
            text_item.setPos(
                x1 - 10 - text_item.boundingRect().width(),
                (y1 + y2) / 2 - text_item.boundingRect().height() / 2,
            )
        else:
            text_item.setPos(
                x1 + 15,
                (y1 + y2) / 2 - text_item.boundingRect().height() / 2,
            )