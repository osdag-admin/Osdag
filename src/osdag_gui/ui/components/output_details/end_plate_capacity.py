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

        self.rows = max(1, int(main.plate.bolts_one_line))
        self.cols = max(1, int(main.plate.bolt_line))

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
                # ---- section capacity values ----
        try:
            output = main.output_values(True)
            output_dict = {i[0]: i[3] for i in output}

            sec_fn = output_dict['button_section_capacity'][1]
            sec_details = sec_fn(True)
            sec_dd = {i[1]: i[3] for i in sec_details}
        except Exception:
            sec_dd = {}

        self.dict_section_failure = {
    'Supported Section Shear Yielding Capacity (kN)':
        round(main.supported_section.shear_yielding_capacity / 1000, 2),

    'Supported Section Allowable Shear Capacity (kN)':
        round(main.supported_section.shear_yielding_capacity / 1000, 2),

    'Supporting Section Tension Yielding Capacity (kN)':
        round(main.supporting_section.tension_yielding_capacity / 1000, 2),
        }
        self.initUI()

    # ──────────────────────────────────────────────────────────────────────────
    # Window shell
    # ──────────────────────────────────────────────────────────────────────────

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
        sg_rect = QApplication.primaryScreen().availableGeometry()
        w, h = 980, 760
        self.setGeometry(
            sg_rect.x() + (sg_rect.width() - w) // 2,
            sg_rect.y() + (sg_rect.height() - h) // 2,
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

        # ── Left info panel ────────────────────────────────────────────────
        lp = QWidget()
        lp.setMaximumWidth(380)
        ll = QVBoxLayout()
        ll.setSpacing(5)

        hl = QLabel("Note: Representative image for Failure Pattern")
        hl.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        hl.setWordWrap(True)
        ll.addWidget(hl)

        def add_section(title, data):
            lbl = QLabel(title)
            lbl.setStyleSheet(
                "font-size: 14px; font-weight: bold;"
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

        # ── Right drawing panel ────────────────────────────────────────────
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

    # ──────────────────────────────────────────────────────────────────────────
    # Data helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _sc(self):
        """All drawing dimensions, scaled by coeff=2."""
        coeff = 2
        spacing_data = self.connection.spacing(status=True)
        p = {
            item[0]: float(item[3]) for item in spacing_data
            if item[0] in [KEY_OUT_PITCH, KEY_OUT_END_DIST,
                           KEY_OUT_GAUGE, KEY_OUT_EDGE_DIST]
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
            'hole': self.hole_dia / coeff,
            # unscaled — used only for dimension text labels
            'r_width': self.plate_width,
            'r_height': self.plate_height,
            'r_pitch': pitch,
            'r_end': end,
            'r_edge': edge,
            'r_gauge': gauge,
        }

    def _bolt_ys(self, s):
        """Retained for compatibility; actual bolt row placement is fixed in _draw_common."""
        return [s['end'] + i * s['pitch'] for i in range(self.rows)]

    # ──────────────────────────────────────────────────────────────────────────
    # Dimension helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _tc(self):
        return Qt.black if self.theme.is_light() else Qt.white

    def _fill_brush(self):
        return (
            QBrush(Qt.black) if self.theme.is_light()
            else QBrush(QColor("#8A8A8A"))
        )

    def _add_dim_label(self, scene, text, x, y):
        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(2)
        ti.setFont(f)
        ti.setDefaultTextColor(self._tc())
        ti.setPos(x, y)
        return ti

    def addHorizontalDimension(self, scene, x1, y, x2, text, pen, coeff, above=True):
        arr = 2
        fill = self._fill_brush()
        scene.addLine(x1, y, x2, y, pen)
        for x in [x1, x2]:
            scene.addLine(x, y - 5 / coeff, x, y + 5 / coeff, pen)
        for pts in [
            [(x1, y), (x1 + arr, y - arr / 2), (x1 + arr, y + arr / 2)],
            [(x2, y), (x2 - arr, y - arr / 2), (x2 - arr, y + arr / 2)],
        ]:
            scene.addPolygon(
                QPolygonF([QPointF(px, py) for px, py in pts]), pen
            ).setBrush(fill)

        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(2)
        ti.setFont(f)
        ti.setDefaultTextColor(self._tc())
        off = -(ti.boundingRect().height() + 1) if above else 2
        ti.setPos((x1 + x2) / 2 - ti.boundingRect().width() / 2, y + off)

    def addVerticalDimension(self, scene, x, y1, y2, text, pen, coeff, right_side=True):
        arr = 2
        fill = self._fill_brush()
        scene.addLine(x, y1, x, y2, pen)
        for y in [y1, y2]:
            scene.addLine(x - 5 / coeff, y, x + 5 / coeff, y, pen)
        for pts in [
            [(x, y1), (x - arr / 2, y1 + arr), (x + arr / 2, y1 + arr)],
            [(x, y2), (x - arr / 2, y2 - arr), (x + arr / 2, y2 - arr)],
        ]:
            scene.addPolygon(
                QPolygonF([QPointF(px, py) for px, py in pts]), pen
            ).setBrush(fill)

        ti = scene.addText(text)
        f = QFont()
        f.setPointSize(2)
        ti.setFont(f)
        ti.setDefaultTextColor(self._tc())
        mid_y = (y1 + y2) / 2 - ti.boundingRect().height() / 2
        if right_side:
            ti.setPos(x + 3, mid_y)
        else:
            ti.setPos(x - ti.boundingRect().width() - 3, mid_y)

    # ──────────────────────────────────────────────────────────────────────────
    # Core drawing — produces ALL three modes
    # ──────────────────────────────────────────────────────────────────────────

    def _draw_common(self, scene, mode):
        s = self._sc()
        c = s['coeff']
        pw = s['width']
        ph = s['height']
        hole = s['hole']

        # Force portrait plate proportions to match the sketch
        pw = min(pw, ph * 0.72)
        ph = max(ph, pw * 1.45)

        # I-beam geometry
        flange_w = pw * 2.7
        flange_h = ph * 0.12
        web_w = ph * 0.07
        web_total_h = ph * 1.85

        # Center web horizontally inside flanges
        web_x = (flange_w - web_w) / 2

        # Small gap below top flange / web top
        gap_from_web_top = flange_h * 1.0
        plate_top = gap_from_web_top

        # Keep plates in upper half, leaving web visible below
        ph = min(ph, web_total_h * 0.52)

        # Plate positions: one on each side of web
        left_plate_x = web_x - pw
        right_plate_x = web_x + web_w

        # Pens & brushes
        if self.theme.is_light():
            struct_pen = QPen(QColor("#555555"), 1.5 / c)
            plate_pen = QPen(QColor("#444444"), 1.2 / c)
            dim_pen = QPen(Qt.black, 0.7 / c)
            dash_pen = QPen(Qt.black, 1.0 / c, Qt.DashLine)
        else:
            struct_pen = QPen(QColor("#B0B0B0"), 1.5 / c)
            plate_pen = QPen(QColor("#CCCCCC"), 1.2 / c)
            dim_pen = QPen(QColor("#E0E0E0"), 0.7 / c)
            dash_pen = QPen(QColor("#AFAFAF"), 1.0 / c, Qt.DashLine)

        beam_brush = QBrush(QColor("#A0A0A0"))
        plate_brush = QBrush(QColor("#FFFFFF"))
        weld_brush = QBrush(QColor("#D2905A"))
        weld_pen = QPen(QColor("#C07840"), 0.5 / c)
        bolt_pen = QPen(QColor("#1E2BFF"), 2.2 / c)
        bolt_brush = QBrush(Qt.white)

        # Beam first
        scene.addRect(0, -flange_h, flange_w, flange_h, struct_pen).setBrush(beam_brush)
        scene.addRect(0, web_total_h, flange_w, flange_h, struct_pen).setBrush(beam_brush)
        scene.addRect(web_x, 0, web_w, web_total_h, struct_pen).setBrush(beam_brush)

# Plates
        scene.addRect(left_plate_x, plate_top, pw, ph, plate_pen).setBrush(plate_brush)
        scene.addRect(right_plate_x, plate_top, pw, ph, plate_pen).setBrush(plate_brush)

# Weld strips on both sides of web — draw AFTER plates so they remain visible
        weld_strip_w = max(web_w * 0.30, 2.0 / c)

        scene.addRect(
    web_x - weld_strip_w,
    plate_top,
    weld_strip_w,
    ph,
    weld_pen
).setBrush(weld_brush)

        scene.addRect(
    web_x + web_w,
    plate_top,
    weld_strip_w,
    ph,
    weld_pen
).setBrush(weld_brush)

        # One centered bolt column per plate
        def plate_col_xs(plate_x):
            return [plate_x + pw / 2]

        left_col_xs = plate_col_xs(left_plate_x)
        right_col_xs = plate_col_xs(right_plate_x)

        # Explicit top + bottom bolt rows
        top_edge = ph * 0.22
        bot_edge = ph * 0.78
        abs_bolt_ys = [plate_top + top_edge, plate_top + bot_edge]
        y_top_b = abs_bolt_ys[0]
        y_bot_b = abs_bolt_ys[-1]

        # Draw bolts
        for cx in left_col_xs + right_col_xs:
         for by in abs_bolt_ys:
          r = hole / 2
          e = scene.addEllipse(cx - r, by - r, r * 2, r * 2, bolt_pen)
          e.setBrush(bolt_brush)

        # Failure-pattern dashed lines
                
        if mode == "shear":
    # LEFT plate
         for cx in left_col_xs:
        # vertical: plate top → bottom bolt
          scene.addLine(cx, plate_top, cx, y_bot_b, dash_pen)
        # horizontal: bottom bolt → left edge
          scene.addLine(cx, y_bot_b, left_plate_x, y_bot_b, dash_pen)

    # RIGHT plate
         for cx in right_col_xs:
        # vertical: plate top → bottom bolt
          scene.addLine(cx, plate_top, cx, y_bot_b, dash_pen)
        # horizontal: bottom bolt → right edge
          scene.addLine(cx, y_bot_b, right_plate_x + pw, y_bot_b, dash_pen)

        elif mode == "tension":
            for cx in left_col_xs:
             scene.addLine(cx, y_top_b, cx, y_bot_b, dash_pen)
             scene.addLine(left_plate_x, y_top_b, cx, y_top_b, dash_pen)
             scene.addLine(left_plate_x, y_bot_b, cx, y_bot_b, dash_pen)

    # RIGHT plate: horizontals to right outer edge + one vertical between bolts
            for cx in right_col_xs:
              scene.addLine(cx, y_top_b, cx, y_bot_b, dash_pen)
              scene.addLine(cx, y_top_b, right_plate_x + pw, y_top_b, dash_pen)
              scene.addLine(cx, y_bot_b, right_plate_x + pw, y_bot_b, dash_pen)
            # Pattern 2:
            # Horizontal dashed lines (top & bottom)
          

        elif mode == "section":
            # Section:
            # no dotted line between bolts
            # only small horizontal dotted lines like reference image
            for cx in left_col_xs:
        # vertical (top bolt → bottom bolt)
             scene.addLine(cx, y_top_b, cx, y_bot_b, dash_pen)

        # horizontal ONLY between bolt and web side (not full plate)
             scene.addLine(cx, y_top_b, web_x, y_top_b, dash_pen)
             scene.addLine(cx, y_bot_b, web_x, y_bot_b, dash_pen)

    # RIGHT plate
            for cx in right_col_xs:
        # vertical (top bolt → bottom bolt)
             scene.addLine(cx, y_top_b, cx, y_bot_b, dash_pen)

        # horizontal ONLY between bolt and web side
             scene.addLine(web_x + web_w, y_top_b, cx, y_top_b, dash_pen)
             scene.addLine(web_x + web_w, y_bot_b, cx, y_bot_b, dash_pen)
        # Scene rect with padding
        pad_top = 55 / c
        pad_side = 75 / c
        pad_bot = 50 / c

        scene.setSceneRect(
            -pad_side,
            -flange_h - pad_top,
            flange_w + 2 * pad_side,
            web_total_h + flange_h * 2 + pad_top + pad_bot
        )

        # Dimension lines
        dim_y_top = -flange_h - pad_top * 0.55
        dim_y_bot = plate_top + ph + pad_bot * 0.5
        dim_x_left = left_plate_x - pad_side * 0.65
        dim_x_rgt = right_plate_x + pw + pad_side * 0.65

        # Top: width on both plates
        self.addHorizontalDimension(
            scene, left_plate_x, dim_y_top, left_plate_x + pw,
            f"{s['r_width']:.1f}", dim_pen, c, above=True
        )
        self.addHorizontalDimension(
            scene, right_plate_x, dim_y_top, right_plate_x + pw,
            f"{s['r_width']:.1f}", dim_pen, c, above=True
        )

        # Left: height
        self.addVerticalDimension(
            scene, dim_x_left, plate_top, plate_top + ph,
            f"{s['r_height']:.1f}", dim_pen, c, right_side=False
        )

        # Right: end + pitch + end
        self.addVerticalDimension(
            scene, dim_x_rgt, plate_top, y_top_b,
            f"{s['r_end']:.1f}", dim_pen, c, right_side=True
        )
        self.addVerticalDimension(
            scene, dim_x_rgt, y_top_b, y_bot_b,
            f"{s['r_pitch']:.1f}", dim_pen, c, right_side=True
        )
        self.addVerticalDimension(
            scene, dim_x_rgt, y_bot_b, plate_top + ph,
            f"{s['r_end']:.1f}", dim_pen, c, right_side=True
        )

        # Bottom: edge distances only
                
        if left_col_xs:
            self.addHorizontalDimension(
                scene, left_plate_x, dim_y_bot, left_col_xs[0],
                f"{s['r_edge']:.1f}", dim_pen, c, above=False
            )
            self.addHorizontalDimension(
                scene, left_col_xs[0], dim_y_bot, left_plate_x + pw,
                f"{s['r_edge']:.1f}", dim_pen, c, above=False
            )

        if right_col_xs:
            self.addHorizontalDimension(
                scene, right_plate_x, dim_y_bot, right_col_xs[0],
                f"{s['r_edge']:.1f}", dim_pen, c, above=False
            )
            self.addHorizontalDimension(
                scene, right_col_xs[0], dim_y_bot, right_plate_x + pw,
                f"{s['r_edge']:.1f}", dim_pen, c, above=False
            )
    # ──────────────────────────────────────────────────────────────────────────
    # Public entry points
    # ──────────────────────────────────────────────────────────────────────────

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


# ──────────────────────────────────────────────────────────────────────────────
# Section variant
# ──────────────────────────────────────────────────────────────────────────────

class EndPlateSectionDetails(EndPlateCapacityDetails):

    def initUI(self):
        self.setupWrapper()
        sg_rect = QApplication.primaryScreen().availableGeometry()
        w, h = 980, 620
        self.setGeometry(
            sg_rect.x() + (sg_rect.width() - w) // 2,
            sg_rect.y() + (sg_rect.height() - h) // 2,
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
                "font-size: 14px; font-weight: bold;"
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

        add_section(
            "Failure Pattern due to Shear in Supported Section",
            {
                'Supported Section Shear Yielding Capacity (kN)':
                    self.dict_section_failure.get(
                        'Supported Section Shear Yielding Capacity (kN)', 'N/A'
                    ),
                'Supported Section Allowable Shear Capacity (kN)':
                    self.dict_section_failure.get(
                        'Supported Section Allowable Shear Capacity (kN)', 'N/A'
                    ),
            }
        )

        add_section(
            "Failure Pattern due to Tension in Supporting Section",
            {
                'Supporting Section Tension Yielding Capacity (kN)':
                    self.dict_section_failure.get(
                        'Supporting Section Tension Yielding Capacity (kN)', 'N/A'
                    ),
            }
        )

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