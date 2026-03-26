from PySide6.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
    QGraphicsScene, QScrollArea
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPolygonF, QBrush
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *


class EndPlateCapacityDetails(QDialog):

    def __init__(self, connection_obj, rows=3, cols=2, main=None):
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager
        self.connection = connection_obj
        self.main = main

        self.plate_height = main.plate.height
        self.plate_width = main.plate.width
        self.hole_dia = main.bolt.bolt_diameter_provided
        self.rows = main.plate.bolts_one_line
        self.cols = main.plate.bolt_line

        cap_details = main.capacities(True)
        dd = {i[1]: i[3] for i in cap_details}

        self.dict_shear_failure = {
            'Shear Yielding Capacity (kN)': dd.get('Shear Yielding Capacity (kN)', 'N/A'),
            'Rupture Capacity (kN)': dd.get('Rupture Capacity (kN)', 'N/A'),
            'Block Shear Capacity (kN)': dd.get('Block Shear Capacity (kN)', 'N/A'),
        }
        self.dict_tension_failure = {
            'Tension Yielding Capacity (kN)': dd.get('Tension Yielding Capacity (kN)', 'N/A'),
            'Tension Rupture Capacity (kN)': dd.get('Tension Rupture Capacity (kN)', 'N/A'),
            'Axial Block Shear Capacity (kN)': dd.get('Axial Block Shear Capacity (kN)', 'N/A'),
        }

        self.initUI()

    def setupWrapper(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setObjectName("spacing_capacity_details")

        ml = QVBoxLayout(self)
        ml.setContentsMargins(1, 1, 1, 1)
        ml.setSpacing(0)

        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle("Bolt Pattern")
        ml.addWidget(self.title_bar)

        self.content_widget = QWidget(self)
        ml.addWidget(self.content_widget, 1)

        sg = QSizeGrip(self)
        sg.setFixedSize(16, 16)

        ov = QHBoxLayout()
        ov.setContentsMargins(0, 0, 4, 4)
        ov.addStretch(1)
        ov.addWidget(sg, 0, Qt.AlignBottom | Qt.AlignRight)
        ml.addLayout(ov)

    def initUI(self):
        self.setupWrapper()
        sg = QApplication.primaryScreen().availableGeometry()
        w, h = 980, 760
        self.setGeometry(
            sg.x() + (sg.width() - w) // 2,
            sg.y() + (sg.height() - h) // 2,
            w, h
        )

        cl = QVBoxLayout(self.content_widget)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        sa.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll = QWidget()
        scroll.setObjectName("spacing_scroll_widget")
        ml = QHBoxLayout(scroll)
        ml.setContentsMargins(10, 10, 10, 10)

        # Left Panel
        lp = QWidget()
        lp.setMaximumWidth(380)
        ll = QVBoxLayout()
        ll.setSpacing(5)

        hl = QLabel("Note: Representative image for Failure Pattern (Half Plate)")
        hl.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        hl.setWordWrap(True)
        ll.addWidget(hl)

        def add_section(title, data):
            lbl = QLabel(title)
            lbl.setStyleSheet(
                "font-size: 14px; font-weight: bold; "
                "margin-top: 15px; margin-bottom: 5px;"
            )
            ll.addWidget(lbl)

            for key, val in data.items():
                row = QHBoxLayout()
                row.addWidget(QLabel(key))
                row.addStretch()
                v = QLabel(f"{val}")
                v.setStyleSheet("font-size: 12px; font-weight: bold;")
                row.addWidget(v)
                ll.addLayout(row)

        add_section("Failure Pattern due to Shear in Plate", self.dict_shear_failure)
        add_section("Failure Pattern due to Tension in Plate", self.dict_tension_failure)
        ll.addStretch()
        lp.setLayout(ll)

        # Right Panel
        rp = QWidget()
        rl = QVBoxLayout()
        rl.setSpacing(12)
        rp.setLayout(rl)

        def make_view(scene, draw_fn, min_h=290):
            v = QGraphicsView(scene)
            v.setBackgroundBrush(
                QBrush(Qt.white) if self.theme.is_light()
                else QBrush(QColor("#4A4A4A"))
            )
            v.setRenderHint(QPainter.Antialiasing)
            v.setMinimumWidth(620)
            v.setMinimumHeight(min_h)
            v.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            v.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            draw_fn(scene)
            v.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
            return v

        lb1 = QLabel("Failure Pattern due to Shear in Plate:")
        lb1.setStyleSheet("font-size: 14px; font-weight: bold;")
        rl.addWidget(lb1)

        self.scene1 = QGraphicsScene()
        self.view1 = make_view(self.scene1, self.createDrawing, 300)
        rl.addWidget(self.view1)

        lb2 = QLabel("Failure Pattern due to Tension in Plate:")
        lb2.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        rl.addWidget(lb2)

        self.scene2 = QGraphicsScene()
        self.view2 = make_view(self.scene2, self.createSecondDrawing, 300)
        rl.addWidget(self.view2)

        ml.addWidget(lp, 1)
        ml.addWidget(rp, 2)
        sa.setWidget(scroll)
        cl.addWidget(sa)

    def _sc(self):
        coeff = 2
        spacing_data = self.connection.spacing(status=True)
        p = {
            item[0]: float(item[3]) for item in spacing_data
            if item[0] in [KEY_OUT_PITCH, KEY_OUT_END_DIST, KEY_OUT_GAUGE, KEY_OUT_EDGE_DIST]
        }

        pitch = p.get(KEY_OUT_PITCH, 0)
        end = p.get(KEY_OUT_END_DIST, 0)
        edge = p.get(KEY_OUT_EDGE_DIST, 0)
        gauge = p.get(KEY_OUT_GAUGE, 0)

        return {
            'coeff': coeff,
            'width': self.plate_width / coeff,
            'height': self.plate_height / coeff,
            'pitch': pitch / coeff,
            'end': end / coeff,
            'edge': edge / coeff,
            'gauge': gauge / coeff,
            'hole': self.main.bolt.bolt_diameter_provided / coeff,
            'r_width': self.plate_width,
            'r_height': self.plate_height,
            'r_pitch': pitch,
            'r_end': end,
            'r_edge': edge,
            'r_gauge': gauge,
        }

    def _bolt_ys(self, s):
        h, pitch, rows = s['height'], s['pitch'], self.rows
        center_y = h / 2
        total_span = (rows - 1) * pitch
        y_start = center_y - total_span / 2
        return [y_start + i * pitch for i in range(rows)]

    def _draw_outer_box(self, scene, left_px, right_px, s, pen):
        w, h, c = s['width'], s['height'], s['coeff']
        margin_y = 14 / c
        flange_thick = 10 / c
        f_ext = 20 / c
        bg_brush = QBrush(QColor("#F0F3E8"))

        flange_x = left_px - f_ext
        flange_w = (right_px + w + f_ext) - flange_x
        web_x = left_px + w
        web_w = right_px - (left_px + w)

        scene.addRect(flange_x, -margin_y - flange_thick, flange_w, flange_thick, pen).setBrush(bg_brush)
        scene.addRect(flange_x, h + margin_y, flange_w, flange_thick, pen).setBrush(bg_brush)
        scene.addRect(web_x, -margin_y, web_w, h + 2 * margin_y, pen).setBrush(bg_brush)

        return flange_x, -margin_y - flange_thick, flange_w, h + 2 * margin_y + 2 * flange_thick

    def addHorizontalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)
        ext, arr = 10, 2
        scene.addLine(x1, y1 - ext / 2, x1, y1 + ext / 2, pen)
        scene.addLine(x2, y2 - ext / 2, x2, y2 + ext / 2, pen)

        fill = QBrush(Qt.black) if self.theme.is_light() else QBrush(QColor("#8A8A8A"))

        for pts in [
            [(x1, y1), (x1 + arr, y1 - arr / 2), (x1 + arr, y1 + arr / 2)],
            [(x2, y2), (x2 - arr, y2 - arr / 2), (x2 - arr, y2 + arr / 2)]
        ]:
            p = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in pts]), pen)
            p.setBrush(fill)

        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(2)
        ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        ti.setPos((x1 + x2) / 2 - ti.boundingRect().width() / 2, y1 - 12)

    def addVerticalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)
        ext, arr = 10, 2
        scene.addLine(x1 - ext / 2, y1, x1 + ext / 2, y1, pen)
        scene.addLine(x2 - ext / 2, y2, x2 + ext / 2, y2, pen)

        fill = QBrush(Qt.black) if self.theme.is_light() else QBrush(QColor("#8A8A8A"))

        for pts in [
            [(x1, y1), (x1 - arr / 2, y1 + arr), (x1 + arr / 2, y1 + arr)],
            [(x2, y2), (x2 - arr / 2, y2 - arr), (x2 + arr / 2, y2 - arr)]
        ]:
            p = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in pts]), pen)
            p.setBrush(fill)

        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(2)
        ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        ti.setPos(x1 - ti.boundingRect().width() - 4, (y1 + y2) / 2 - ti.boundingRect().height() / 2)

    def _draw_plate(self, scene, px, s, mode, pen, bolt_pen, dash_pen, side="left"):
        w, h, hole, c = s['width'], s['height'], s['hole'], s['coeff']
        scene.addRect(px, 0, w, h, pen).setBrush(QBrush(QColor("#DCDCDC")))

        bx = px + w / 2
        ys = self._bolt_ys(s)
        y_top = ys[0]
        y_bottom = ys[-1]

        if mode == "shear":
            scene.addLine(bx, 0, bx, y_bottom, dash_pen)
        elif mode == "tension":
            scene.addLine(bx, y_top, bx, y_bottom, dash_pen)
        elif mode == "section":
            scene.addLine(bx, y_top, bx, y_bottom, dash_pen)

        cross_pen = QPen(Qt.blue, 0.8 / c)
        for y in ys:
            scene.addEllipse(bx - hole / 2, y - hole / 2, hole, hole, bolt_pen)
            scene.addLine(bx, y - hole / 2, bx, y + hole / 2, cross_pen)
            scene.addLine(bx - hole / 2, y, bx + hole / 2, y, cross_pen)

        if mode == "shear":
            if side == "left":
                scene.addLine(px, y_bottom, bx, y_bottom, dash_pen)
            else:
                scene.addLine(bx, y_bottom, px + w, y_bottom, dash_pen)

        elif mode == "tension":
            if side == "left":
                scene.addLine(px, y_top, bx, y_top, dash_pen)
                scene.addLine(px, y_bottom, bx, y_bottom, dash_pen)
            else:
                scene.addLine(bx, y_top, px + w, y_top, dash_pen)
                scene.addLine(bx, y_bottom, px + w, y_bottom, dash_pen)

        elif mode == "section":
            if side == "left":
                for y in ys:
                    scene.addLine(bx, y, px + w, y, dash_pen)
            else:
                for y in ys:
                    scene.addLine(px, y, bx, y, dash_pen)

    def _add_plate_dimensions(self, scene, left_px, right_px, s, pen, outer_box):
        w = s['width']
        h = s['height']

        top_y = outer_box[1] - 28

        # bolt centers
        left_bolt_x = left_px + w / 2
        right_bolt_x = right_px + w / 2

        # plate outer ends
        left_plate_end_x = left_px
        right_plate_end_x = right_px + w

        # top dimension points
        x0 = left_plate_end_x
        x1 = left_bolt_x
        x2 = right_bolt_x
        x3 = right_plate_end_x

        # one continuous top dimension line
        scene.addLine(x0, top_y, x3, top_y, pen)

        # top ticks
        tick_h = 10
        for x in [x0, x1, x2, x3]:
            scene.addLine(x, top_y - tick_h / 2, x, top_y + tick_h / 2, pen)

        # top arrows
        arr = 2
        fill = QBrush(Qt.black) if self.theme.is_light() else QBrush(QColor("#8A8A8A"))

        arrow_sets = [
            [(x0, top_y), (x0 + arr, top_y - arr / 2), (x0 + arr, top_y + arr / 2)],
            [(x1, top_y), (x1 - arr, top_y - arr / 2), (x1 - arr, top_y + arr / 2)],
            [(x1, top_y), (x1 + arr, top_y - arr / 2), (x1 + arr, top_y + arr / 2)],
            [(x2, top_y), (x2 - arr, top_y - arr / 2), (x2 - arr, top_y + arr / 2)],
            [(x2, top_y), (x2 + arr, top_y - arr / 2), (x2 + arr, top_y + arr / 2)],
            [(x3, top_y), (x3 - arr, top_y - arr / 2), (x3 - arr, top_y + arr / 2)],
        ]

        for pts in arrow_sets:
            poly = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in pts]), pen)
            poly.setBrush(fill)

        def add_text(txt, xa, xb):
            ti = scene.addText(txt)
            f = QFont()
            f.setPointSize(2)
            ti.setFont(f)
            ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
            ti.setPos((xa + xb) / 2 - ti.boundingRect().width() / 2, top_y - 14)

        add_text("15.0", x0, x1)
        add_text("52.0", x1, x2)
        add_text("15.0", x2, x3)

        # left vertical overall dimension
        left_dim_x = left_px - 40
        self.addVerticalDimension(scene, left_dim_x, 0, left_dim_x, h, "70.0", pen)

        # right vertical dimension same logic as top
        right_dim_x = right_px + w + 40

        y0 = 0
        y3 = h

        ys = self._bolt_ys(s)
        y1 = ys[0]   # top bolt center
        y2 = ys[-1]  # bottom bolt center

        # one continuous vertical dimension line
        scene.addLine(right_dim_x, y0, right_dim_x, y3, pen)

        # ticks
        tick_w = 10
        for y in [y0, y1, y2, y3]:
            scene.addLine(right_dim_x - tick_w / 2, y, right_dim_x + tick_w / 2, y, pen)

        # vertical arrows
        arrow_sets_v = [
            [(right_dim_x, y0), (right_dim_x - arr / 2, y0 + arr), (right_dim_x + arr / 2, y0 + arr)],
            [(right_dim_x, y1), (right_dim_x - arr / 2, y1 - arr), (right_dim_x + arr / 2, y1 - arr)],
            [(right_dim_x, y1), (right_dim_x - arr / 2, y1 + arr), (right_dim_x + arr / 2, y1 + arr)],
            [(right_dim_x, y2), (right_dim_x - arr / 2, y2 - arr), (right_dim_x + arr / 2, y2 - arr)],
            [(right_dim_x, y2), (right_dim_x - arr / 2, y2 + arr), (right_dim_x + arr / 2, y2 + arr)],
            [(right_dim_x, y3), (right_dim_x - arr / 2, y3 - arr), (right_dim_x + arr / 2, y3 - arr)],
        ]

        for pts in arrow_sets_v:
            poly = scene.addPolygon(QPolygonF([QPointF(x, y) for x, y in pts]), pen)
            poly.setBrush(fill)

        def add_vtext(txt, ya, yb):
            ti = scene.addText(txt)
            f = QFont()
            f.setPointSize(2)
            ti.setFont(f)
            ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
            ti.setPos(right_dim_x + 6, (ya + yb) / 2 - ti.boundingRect().height() / 2)

        add_vtext("15.0", y0, y1)
        add_vtext("40.0", y1, y2)
        add_vtext("15.0", y2, y3)

    def _draw_common(self, scene, mode):
        s = self._sc()
        coeff = s['coeff']
        w = s['width']
        h = s['height']

        gap = 12 / coeff
        left_px = 0
        right_px = w + gap

        top_pad = 130 / coeff
        side_pad = 130 / coeff
        bottom_pad = 100 / coeff

        scene.setSceneRect(
            -side_pad,
            -top_pad,
            2 * w + gap + 2 * side_pad,
            h + top_pad + bottom_pad
        )

        if self.theme.is_light():
            pen = QPen(Qt.black, 1.2 / coeff)
            dash = QPen(Qt.black, 1.2 / coeff, Qt.DashLine)
            bolt_pen = QPen(Qt.blue, 2 / coeff)
        else:
            pen = QPen(QColor("#E0E0E0"), 1.2 / coeff)
            dash = QPen(QColor("#AFAFAF"), 1.2 / coeff, Qt.DashLine)
            bolt_pen = QPen(Qt.blue, 2 / coeff)

        outer_box = self._draw_outer_box(scene, left_px, right_px, s, pen)

        self._draw_plate(scene, left_px, s, mode, pen, bolt_pen, dash, "left")
        self._draw_plate(scene, right_px, s, mode, pen, bolt_pen, dash, "right")

        self._add_plate_dimensions(scene, left_px, right_px, s, pen, outer_box)

    def createDrawing(self, scene):
        self._draw_common(scene, "shear")

    def createSecondDrawing(self, scene):
        self._draw_common(scene, "tension")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'view1'):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
        if hasattr(self, 'view2'):
            self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)


class EndPlateSectionDetails(EndPlateCapacityDetails):

    def initUI(self):
        self.setupWrapper()
        sg = QApplication.primaryScreen().availableGeometry()

        w, h = 980, 620
        self.setGeometry(
            sg.x() + (sg.width() - w) // 2,
            sg.y() + (sg.height() - h) // 2,
            w, h
        )

        cl = QVBoxLayout(self.content_widget)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        sa.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll = QWidget()
        ml = QHBoxLayout(scroll)
        ml.setContentsMargins(10, 10, 10, 10)

        lp = QWidget()
        lp.setMaximumWidth(380)
        ll = QVBoxLayout()
        ll.setSpacing(5)

        hl = QLabel("Note: Representative image for Failure Pattern")
        hl.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        ll.addWidget(hl)

        def add_section(title, data):
            lbl = QLabel(title)
            lbl.setStyleSheet(
                "font-size: 14px; font-weight: bold; "
                "margin-top: 15px; margin-bottom: 5px;"
            )
            ll.addWidget(lbl)
            for k, v in data.items():
                row = QHBoxLayout()
                row.addWidget(QLabel(k))
                row.addStretch()
                val = QLabel(f"{v}")
                val.setStyleSheet("font-size: 12px; font-weight: bold;")
                row.addWidget(val)
                ll.addLayout(row)

        add_section("Failure Pattern in Section", self.dict_shear_failure)
        ll.addStretch()
        lp.setLayout(ll)

        rp = QWidget()
        rl = QVBoxLayout()
        rl.setSpacing(10)
        rp.setLayout(rl)

        def make_view(scene):
            v = QGraphicsView(scene)
            v.setBackgroundBrush(
                QBrush(Qt.white) if self.theme.is_light()
                else QBrush(QColor("#4A4A4A"))
            )
            v.setRenderHint(QPainter.Antialiasing)
            v.setMinimumWidth(620)
            v.setMinimumHeight(520)
            v.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            v.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.createSectionDrawing(scene)
            v.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
            return v

        lbl = QLabel("Failure Pattern in Section:")
        lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
        rl.addWidget(lbl)

        self.scene1 = QGraphicsScene()
        self.view1 = make_view(self.scene1)
        rl.addWidget(self.view1)

        ml.addWidget(lp, 1)
        ml.addWidget(rp, 2)
        sa.setWidget(scroll)
        cl.addWidget(sa)

    def createSectionDrawing(self, scene):
        self._draw_common(scene, "section")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'view1'):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)