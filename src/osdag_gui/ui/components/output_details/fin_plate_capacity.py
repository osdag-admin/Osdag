import sys
from PySide6.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
                               QGraphicsScene, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPolygonF, QBrush
from PySide6.QtCore import QPointF
from ..dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *


class FinPlateCapacityDetails(QDialog):
    def __init__(self, connection_obj, rows=3, cols=2, main=None):
        super().__init__()
        app = QApplication.instance()
        self.theme      = app.theme_manager
        self.connection = connection_obj
        self.main       = main

        self.plate_height    = main.plate.height
        self.plate_width     = main.plate.length
        self.hole_dia        = main.bolt.bolt_diameter_provided
        self.rows            = main.plate.bolts_one_line
        self.cols            = main.plate.bolt_line
        
        try:
            connectivity = getattr(self.main, 'connectivity', '')
        except:
            connectivity = ''

        if connectivity == "Column Web-Beam Web" and self.rows * self.cols == 4:
            self.rows = 2
            self.cols = 2

        self.plate_thickness = main.plate.thickness

        output       = main.output_values(True)
        dict1        = {i[0]: i[3] for i in output}
        cap_fn       = dict1['button1'][1]
        cap_details  = cap_fn(True)
        dd           = {i[1]: i[3] for i in cap_details}

        self.shear_yield_capacity      = float(dd['Shear Yielding Capacity (kN)'])
        self.rupture_capacity          = float(dd['Rupture Capacity (kN)'])
        self.Block_Shear_Capacity      = float(dd['Block Shear Capacity (kN)'])
        self.Tension_Yielding_Capacity = float(dd['Tension Yielding Capacity (kN)'])
        self.Tension_rupture_Capacity  = float(dd['Tension Rupture Capacity (kN)'])
        self.axial_block_shear_capacity= float(dd['Axial Block Shear Capacity (kN)'])
        self.moment_demand             = float(dd['Moment Demand (kNm)'])
        self.moment_capacity           = float(dd['Moment Capacity (kNm)'])

        self.dict_shear_failure = {
            'Shear Yielding Capacity (kN)': self.shear_yield_capacity,
            'Rupture Capacity (kN)':        self.rupture_capacity,
            'Block Shear Capacity (kN)':    self.Block_Shear_Capacity,
        }
        self.dict_tension_failure = {
            'Tension Yielding Capacity (kN)':  self.Tension_Yielding_Capacity,
            'Tension Rupture Capacity (kN)':   self.Tension_rupture_Capacity,
            'Axial Block Shear Capacity (kN)': self.axial_block_shear_capacity,
        }
        self.dict_section_3 = {
            'Moment Demand (kNm)':   self.moment_demand,
            'Moment Capacity (kNm)': self.moment_capacity,
        }

        self.weldsize = 0
        if 'Weld.Size' in dict1:
            self.weldsize = dict1['Weld.Size']

        # Default — child class may override before calling super().__init__()
        if not hasattr(self, 'show_third'):
            self.show_third = False

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
        sg   = QApplication.primaryScreen().availableGeometry()
        w, h = 900, 500
        self.setGeometry(sg.x() + (sg.width()-w)//2,
                         sg.y() + (sg.height()-h)//2, w, h)

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

        # left panel
        lp = QWidget()
        lp.setMaximumWidth(400)
        ll = QVBoxLayout()
        ll.setSpacing(5)

        hl = QLabel("Note: Representative image for Failure Pattern (Half Plate)")
        hl.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        hl.setWordWrap(True)
        ll.addWidget(hl)

        def add_section(title, data):
            lbl = QLabel(title)
            lbl.setStyleSheet("font-size: 14px; font-weight: bold;"
                              "margin-top: 15px; margin-bottom: 5px;")
            ll.addWidget(lbl)
            for key, val in data.items():
                row = QHBoxLayout()
                row.setContentsMargins(0, 2, 0, 2)
                row.addWidget(QLabel(key))
                row.addStretch()
                v = QLabel(f'{val}')
                v.setStyleSheet("font-size: 12px; font-weight: bold;")
                row.addWidget(v)
                ll.addLayout(row)

        add_section("Failure Pattern due to Shear in Plate",   self.dict_shear_failure)
        add_section("Failure Pattern due to Tension in Plate", self.dict_tension_failure)
        ll.addStretch()
        lp.setLayout(ll)

        # right panel
        rp = QWidget()
        rl = QVBoxLayout()
        rl.setSpacing(10)
        rp.setLayout(rl)

        def make_view(scene, draw_fn):
            v = QGraphicsView(scene)
            v.setBackgroundBrush(
                QBrush(Qt.white) if self.theme.is_light()
                else QBrush(QColor("#4A4A4A")))
            v.setRenderHint(QPainter.Antialiasing)
            v.setMinimumWidth(500)
            v.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            v.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            draw_fn(scene)
            v.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
            return v

        lb1 = QLabel("Failure Pattern due to Shear in Plate:")
        lb1.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        rl.addWidget(lb1)
        self.scene1 = QGraphicsScene()
        self.view1  = make_view(self.scene1, self.createDrawing)
        rl.addWidget(self.view1)

        lb2 = QLabel("Failure Pattern due to Tension in Plate:")
        lb2.setStyleSheet("font-size: 14px; font-weight: bold;"
                          "margin-bottom: 5px; margin-top: 10px;")
        rl.addWidget(lb2)
        self.scene2 = QGraphicsScene()
        self.view2  = make_view(self.scene2, self.createSecondDrawing)
        rl.addWidget(self.view2)

        # Show third failure pattern only for Beam-Beam Connectivity
        if self.show_third:
            lb3 = QLabel("Failure Pattern due to Block Shear in Plate:")
            lb3.setStyleSheet("font-size: 14px; font-weight: bold;"
                            "margin-bottom: 5px; margin-top: 10px;")
            rl.addWidget(lb3)
            self.scene3 = QGraphicsScene()
            self.view3  = make_view(self.scene3, self.createThirdDrawing)
            rl.addWidget(self.view3)

        ml.addWidget(lp, 1)
        ml.addWidget(rp, 2)
        sa.setWidget(scroll)
        cl.addWidget(sa)

    def get_parameters(self):
        param_map = {}
        for item in self.connection.spacing(status=True):
            key, _, _, value = item
            if   key == KEY_OUT_PITCH:     param_map['pitch']  = float(value)
            elif key == KEY_OUT_END_DIST:  param_map['end']    = float(value)
            elif key == KEY_OUT_GAUGE1:    param_map['gauge1'] = float(value)
            elif key == KEY_OUT_GAUGE2:    param_map['gauge2'] = float(value)
            elif key == KEY_OUT_GAUGE:     param_map['gauge']  = float(value)
            elif key == KEY_OUT_EDGE_DIST: param_map['edge']   = float(value)
        param_map['hole'] = self.main.bolt.bolt_diameter_provided
        return param_map

    def _sc(self, coeff=1):
        p = self.get_parameters()
        s = {
            'pitch':  p['pitch'] / coeff,
            'end':    p['end']   / coeff,
            'edge':   p['edge']  / coeff,
            'width':  self.plate_width  / coeff,
            'height': self.plate_height / coeff,
            'hole':   p['hole']         / coeff,
            'weld':   self.weldsize     / coeff,
        }
        if 'gauge' in p:
            s['g1'] = s['g2'] = p['gauge'] / coeff
        else:
            s['g1'] = p.get('gauge1', 0) / coeff
            s['g2'] = p.get('gauge2', p.get('gauge1', 0)) / coeff

        if self.rows == 2 and self.cols == 2:
            if s['g1'] == 0:
                s['g1'] = s['g2'] = s['pitch']
            expected_height = 2 * s['end'] + (self.rows - 1) * s['pitch']
            expected_width = 2 * s['edge'] + (self.cols - 1) * s['g1']
            if s['height'] != expected_height:
                s['height'] = expected_height
            if s['width'] != expected_width:
                s['width'] = expected_width

        return s

    def _pens(self, coeff=2):
        out  = QPen(Qt.blue, 2 / coeff)
        if self.theme.is_light():
            dim  = QPen(Qt.black,          1.5 / coeff)
            dash = QPen(Qt.black,          1.5 / coeff, Qt.DashLine)
        else:
            dim  = QPen(QColor("#8A8A8A"), 1.5 / coeff)
            dash = QPen(QColor("#8A8A8A"), 1.5 / coeff, Qt.DashLine)
        return out, dim, dash

    def _bxL(self, edge, g1, g2):
        xs, x = [], edge
        for c in range(self.cols):
            xs.append(x)
            if c < self.cols - 1:
                x += g1 if c % 2 == 0 else g2
        return xs

    def _bxR(self, w, edge, g1, g2):
        xs, x = [], w - edge
        for c in range(self.cols):
            xs.append(x)
            if c < self.cols - 1:
                x -= g1 if c % 2 == 0 else g2
        return xs

    def _holes(self, scene, bxs, end, pitch, hole, pen, coeff=1, bolt_color="#FF3636"):
        bolt_pen = QPen(QColor(bolt_color), 2 / coeff)
        for row in range(self.rows):
            for col in range(self.cols):
                cx = bxs[col]
                cy = end + row * pitch
                scene.addEllipse(cx - hole/2, cy - hole/2, hole, hole, bolt_pen)

    def _weld_left(self, scene, weld, h, dim_pen):
        if weld > 0:
            scene.addRect(0, 0, weld, h, QPen(Qt.NoPen), QBrush(Qt.red))
            scene.addLine(weld, 0, weld, h, dim_pen)

    def _weld_right(self, scene, weld, w, h, dim_pen):
        if weld > 0:
            scene.addRect(w - weld, 0, weld, h, QPen(Qt.NoPen), QBrush(Qt.red))
            scene.addLine(w - weld, 0, w - weld, h, dim_pen)

    def _get_members(self):
        col_d = 150
        col_B = 150
        col_T = 10
        col_tw = 10
        beam_d = 200
        beam_T = 10
        if hasattr(self.main, 'column'):
            col_d = float(getattr(self.main.column, 'depth', 150))
            col_B = float(getattr(self.main.column, 'flange_width', 150))
            col_T = float(getattr(self.main.column, 'flange_thickness', 10))
            col_tw = float(getattr(self.main.column, 'web_thickness', 10))
        elif hasattr(self.main, 'supporting_section'):
            col_d = float(getattr(self.main.supporting_section, 'depth', 150))
            col_B = float(getattr(self.main.supporting_section, 'flange_width', 150))
            col_T = float(getattr(self.main.supporting_section, 'flange_thickness', 10))
            col_tw = float(getattr(self.main.supporting_section, 'web_thickness', 10))
            
        if hasattr(self.main, 'beam'):
            beam_d = float(getattr(self.main.beam, 'depth', 200))
            beam_T = float(getattr(self.main.beam, 'flange_thickness', 10))
        elif hasattr(self.main, 'supported_section'):
            beam_d = float(getattr(self.main.supported_section, 'depth', 200))
            beam_T = float(getattr(self.main.supported_section, 'flange_thickness', 10))
            
        return col_d, col_B, col_T, col_tw, beam_d, beam_T

    def _draw_primary_secondary(self, scene, w, h, coeff, dim, mirror=False, connectivity="", col_color=QColor("#BFBFA9"), beam_color=QColor("#F8F8DB")):
        from PySide6.QtGui import QPainterPath, QPolygonF
        from PySide6.QtCore import QPointF
        col_d, col_B, col_T, col_tw, beam_d, beam_T = self._get_members()
        col_d /= coeff
        col_B /= coeff
        col_T /= coeff
        col_tw /= coeff
        beam_d /= coeff
        beam_T /= coeff
        try:
            gap = float(getattr(self.main, 'clear_gap', 10)) / coeff
        except:
            gap = 10 / coeff
            
        col_h = max(h * 2.5, 400 / coeff)
        col_y = (h - col_h) / 2
        
        if connectivity == "Column Web-Beam Web":
            if getattr(self, 'rows', 0) * getattr(self, 'cols', 0) == 4:
                beam_w = col_d / 2 - gap + 100 / coeff
            elif getattr(self, 'rows', 0) * getattr(self, 'cols', 0) == 2:
                beam_w = max(w * 4, 350 / coeff) - 70 / coeff
            else:
                beam_w = max(w * 4, 350 / coeff)
        elif connectivity == "Column Flange-Beam Web":
            beam_w = max(w * 4, 350 / coeff) - 100 / coeff
        else:
            beam_w = max(w * 4, 350 / coeff)
        beam_y = (h - beam_d) / 2
        
        if connectivity == "Beam-Beam":
            col_y = beam_y - col_h/2 + col_d/2
            col_top_y = col_y + col_h/2 - col_d/2
            col_bot_y = col_y + col_h/2 + col_d/2
            
            cope_d = max(col_T + 10/coeff, -beam_y)
            r = 15/coeff

            if mirror:
                col_left_x = w + col_tw/2 - col_B/2
                col_right_x = w + col_tw/2 + col_B/2
                pts = [
                    QPointF(col_left_x, col_top_y),
                    QPointF(col_left_x, col_top_y + col_T),
                    QPointF(w, col_top_y + col_T),
                    QPointF(w, col_bot_y - col_T),
                    QPointF(col_left_x, col_bot_y - col_T),
                    QPointF(col_left_x, col_bot_y),
                    QPointF(col_right_x, col_bot_y),
                    QPointF(col_right_x, col_bot_y - col_T),
                    QPointF(w + col_tw, col_bot_y - col_T),
                    QPointF(w + col_tw, col_top_y + col_T),
                    QPointF(col_right_x, col_top_y + col_T),
                    QPointF(col_right_x, col_top_y)
                ]
                scene.addPolygon(QPolygonF(pts), dim, QBrush(col_color))
                self.addHorizontalDimension(scene, col_left_x, col_bot_y + 30/coeff, col_right_x, col_bot_y + 30/coeff, str(col_B*coeff), dim)

                gap_x = w - gap
                cope_x = min(gap_x, col_left_x - 10/coeff)
                beam_left = gap_x - beam_w
                
                path = QPainterPath()
                path.moveTo(cope_x, beam_y)
                path.lineTo(beam_left, beam_y)
                path.lineTo(beam_left, beam_y + beam_d)
                path.lineTo(gap_x, beam_y + beam_d)
            
                cope_y_top = beam_y + cope_d
                path.lineTo(gap_x, cope_y_top)
                path.arcTo(cope_x, cope_y_top - 2*r, 2*r, 2*r, 270, -90)
                path.lineTo(cope_x, beam_y)
            
                scene.addPath(path, dim, QBrush(beam_color))
                scene.addLine(beam_left, beam_y + beam_T, cope_x, beam_y + beam_T, dim)
                scene.addLine(beam_left, beam_y + beam_d - beam_T, gap_x, beam_y + beam_d - beam_T, dim)
                self.addVerticalDimension(scene, -beam_w - gap + w - 30/coeff, beam_y, -beam_w - gap + w - 30/coeff, beam_y + beam_d, str(beam_d*coeff), dim)
            else:
                col_left_x = -col_tw/2 - col_B/2
                col_right_x = -col_tw/2 + col_B/2
                pts = [
                    QPointF(col_right_x, col_top_y),
                    QPointF(col_right_x, col_top_y + col_T),
                    QPointF(0, col_top_y + col_T),
                    QPointF(0, col_bot_y - col_T),
                    QPointF(col_right_x, col_bot_y - col_T),
                    QPointF(col_right_x, col_bot_y),
                    QPointF(col_left_x, col_bot_y),
                    QPointF(col_left_x, col_bot_y - col_T),
                    QPointF(-col_tw, col_bot_y - col_T),
                    QPointF(-col_tw, col_top_y + col_T),
                    QPointF(col_left_x, col_top_y + col_T),
                    QPointF(col_left_x, col_top_y)
                ]
                scene.addPolygon(QPolygonF(pts), dim, QBrush(col_color))
                self.addHorizontalDimension(scene, col_left_x, col_bot_y + 30/coeff, col_right_x, col_bot_y + 30/coeff, str(col_B*coeff), dim)

                gap_x = gap
                cope_x = max(gap_x, col_right_x + 10/coeff)
                beam_right = gap_x + beam_w
                
                path = QPainterPath()
                path.moveTo(cope_x, beam_y)
                path.lineTo(beam_right, beam_y)
                path.lineTo(beam_right, beam_y + beam_d)
                path.lineTo(gap_x, beam_y + beam_d)
            
                cope_y_top = beam_y + cope_d
                path.lineTo(gap_x, cope_y_top)
                path.arcTo(cope_x - 2*r, cope_y_top - 2*r, 2*r, 2*r, 270, 90)
                path.lineTo(cope_x, beam_y)
            
                scene.addPath(path, dim, QBrush(beam_color))
                scene.addLine(cope_x, beam_y + beam_T, beam_right, beam_y + beam_T, dim)
                scene.addLine(gap_x, beam_y + beam_d - beam_T, beam_right, beam_y + beam_d - beam_T, dim)
                self.addVerticalDimension(scene, gap + beam_w + 30/coeff, beam_y, gap + beam_w + 30/coeff, beam_y + beam_d, str(beam_d*coeff), dim)
        else:
            if not mirror:
                if connectivity == "Column Web-Beam Web":
                    col_left = -col_d / 2
                    scene.addRect(col_left, col_y, col_d, col_h, dim, QBrush(col_color))
                    scene.addLine(col_left + col_T, col_y, col_left + col_T, col_y + col_h, dim)
                    scene.addLine(col_left + col_d - col_T, col_y, col_left + col_d - col_T, col_y + col_h, dim)
                    self.addHorizontalDimension(scene, col_left, col_y + col_h + 30/coeff, col_left + col_d, col_y + col_h + 30/coeff, str(col_d*coeff), dim)
                else:
                    scene.addRect(-col_d, col_y, col_d, col_h, dim, QBrush(col_color))
                    scene.addLine(-col_d + col_T, col_y, -col_d + col_T, col_y + col_h, dim)
                    scene.addLine(-col_T, col_y, -col_T, col_y + col_h, dim)
                    self.addHorizontalDimension(scene, -col_d, col_y + col_h + 30/coeff, 0, col_y + col_h + 30/coeff, str(col_d*coeff), dim)

                scene.addRect(gap, beam_y, beam_w, beam_d, dim, QBrush(beam_color))
                scene.addLine(gap, beam_y + beam_T, gap + beam_w, beam_y + beam_T, dim)
                scene.addLine(gap, beam_y + beam_d - beam_T, gap + beam_w, beam_y + beam_d - beam_T, dim)
                self.addVerticalDimension(scene, gap + beam_w + 30/coeff, beam_y, gap + beam_w + 30/coeff, beam_y + beam_d, str(beam_d*coeff), dim)
            else:
                if connectivity == "Column Web-Beam Web":
                    col_left = w - col_d / 2
                    scene.addRect(col_left, col_y, col_d, col_h, dim, QBrush(col_color))
                    scene.addLine(col_left + col_T, col_y, col_left + col_T, col_y + col_h, dim)
                    scene.addLine(col_left + col_d - col_T, col_y, col_left + col_d - col_T, col_y + col_h, dim)
                    self.addHorizontalDimension(scene, col_left, col_y + col_h + 30/coeff, col_left + col_d, col_y + col_h + 30/coeff, str(col_d*coeff), dim)
                else:
                    scene.addRect(w, col_y, col_d, col_h, dim, QBrush(col_color))
                    scene.addLine(w + col_T, col_y, w + col_T, col_y + col_h, dim)
                    scene.addLine(w + col_d - col_T, col_y, w + col_d - col_T, col_y + col_h, dim)
                    self.addHorizontalDimension(scene, w, col_y + col_h + 30/coeff, w + col_d, col_y + col_h + 30/coeff, str(col_d*coeff), dim)

                scene.addRect(w - gap - beam_w, beam_y, beam_w, beam_d, dim, QBrush(beam_color))
                scene.addLine(w - gap - beam_w, beam_y + beam_T, w - gap, beam_y + beam_T, dim)
                scene.addLine(w - gap - beam_w, beam_y + beam_d - beam_T, w - gap, beam_y + beam_d - beam_T, dim)
                self.addVerticalDimension(scene, -beam_w - gap + w - 30/coeff, beam_y, -beam_w - gap + w - 30/coeff, beam_y + beam_d, str(beam_d*coeff), dim)

    def createDrawing(self, scene):
        coeff = 1
        s = self._sc(coeff)
        outline, dim, dash = self._pens(3)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 60/coeff, 60/coeff
        
        try:
            connectivity = getattr(self.main, 'connectivity', '')
        except:
            connectivity = ''

        if connectivity == "Column Web-Beam Web" or connectivity == "Beam-Beam":
            col_color = QColor("#B5B5A0")
            beam_color = QColor("#EEEED1")
            plate_bg_str = "#969684"
            bolt_color = "#FF1D1D"
        else:
            col_color = QColor("#BFBFA9")
            beam_color = QColor("#F8F8DB")
            plate_bg_str = "#A0A08E"
            bolt_color = "#FF3636"

        self._draw_primary_secondary(scene, w, h, coeff, dim, mirror=False, connectivity=connectivity, col_color=col_color, beam_color=beam_color)

        bxs   = self._bxR(w, edge, g1, g2)
        x_cut = bxs[-1]

        plate_bg = QBrush(QColor(plate_bg_str))
        scene.addRect(0, 0, w, h, dim, plate_bg)

        scene.addLine(x_cut, end, x_cut, h, dash)
        scene.addLine(x_cut, end, w, end, dash)
        self._holes(scene, bxs, end, pitch, hole, outline, coeff, bolt_color)
        self._weld_left(scene, weld, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=False)
                            
        rect = scene.itemsBoundingRect()
        scene.setSceneRect(rect.adjusted(-ho, -vo, ho + 100/coeff, vo))

    def createSecondDrawing(self, scene):
        coeff = 1
        s = self._sc(coeff)
        outline, dim, dash = self._pens(3)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 60/coeff, 60/coeff
        
        try:
            connectivity = getattr(self.main, 'connectivity', '')
        except:
            connectivity = ''

        if connectivity == "Column Web-Beam Web" or connectivity == "Beam-Beam":
            col_color = QColor("#B5B5A0")
            beam_color = QColor("#EEEED1")
            plate_bg_str = "#969684"
            bolt_color = "#FF1D1D"
        else:
            col_color = QColor("#BFBFA9")
            beam_color = QColor("#F8F8DB")
            plate_bg_str = "#A0A08E"
            bolt_color = "#FF3636"

        self._draw_primary_secondary(scene, w, h, coeff, dim, mirror=False, connectivity=connectivity, col_color=col_color, beam_color=beam_color)

        bxs   = self._bxR(w, edge, g1, g2)
        x_cut = bxs[-1]

        plate_bg = QBrush(QColor(plate_bg_str))
        scene.addRect(0, 0, w, h, dim, plate_bg)

        scene.addLine(x_cut, end,   w,     end,     dash)
        scene.addLine(x_cut, end,   x_cut, h - end, dash)
        scene.addLine(x_cut, h-end, w,     h - end, dash)
        self._holes(scene, bxs, end, pitch, hole, outline, coeff, bolt_color)
        self._weld_left(scene, weld, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=False)
                            
        rect = scene.itemsBoundingRect()
        scene.setSceneRect(rect.adjusted(-ho, -vo, ho + 100/coeff, vo))

    def _addDimensions(self, scene, width, height, pitch, end,
                       g1, g2, edge, pen, coeff, mirror):
        ho, vo = 30/coeff, 40/coeff

        _, _, _, _, beam_d, _ = self._get_members()
        beam_d /= coeff
        beam_y = (height - beam_d) / 2
        top_y = beam_y - 15 / coeff

        # Horizontal dimensions mapping
        x_positions = [0]
        if not mirror:
            bxs = self._bxR(width, edge, g1, g2)
            bxs_reversed = list(reversed(bxs))
            x_positions.extend(bxs_reversed)
        else:
            bxs = self._bxL(edge, g1, g2)
            x_positions.extend(bxs)
        x_positions.append(width)

        for i in range(len(x_positions)-1):
            x1 = x_positions[i]
            x2 = x_positions[i+1]
            dist = abs(x2 - x1)
            self.addHorizontalDimension(scene, x1, top_y, x2, top_y,
                                        f"{dist * coeff:g}", pen)

        # Vertical dimensions mapping
        self.addVerticalDimension(scene, width+vo, 0,
                                  width+vo, end, f"{end * coeff:g}", pen)
        for i in range(self.rows - 1):
            self.addVerticalDimension(scene, width+vo, end + i*pitch,
                                      width+vo, end + (i+1)*pitch,
                                      f"{pitch * coeff:g}", pen)
        
        last_bolt_y = end + (self.rows - 1)*pitch
        rem_len = height - last_bolt_y
        self.addVerticalDimension(scene, width+vo, last_bolt_y,
                                  width+vo, height, f"{rem_len * coeff:g}", pen)

        self.addVerticalDimension(scene, -vo, 0, -vo, height,
                                  f"{height * coeff:g}", pen)
 
    def addHorizontalDimension(self, scene, x1, y1, x2, y2, text, pen):
        try:
            val = float(text)
            if val == 0:
                return
            if val.is_integer():
                text = str(int(val))
            else:
                text = f"{val:g}"
        except ValueError:
            pass

        scene.addLine(x1, y1, x2, y2, pen)
        ext = 10;  arr = 3
        scene.addLine(x1, y1-ext/2, x1, y1+ext/2, pen)
        scene.addLine(x2, y2-ext/2, x2, y2+ext/2, pen)
        fill = (QBrush(Qt.black) if self.theme.is_light()
                else QBrush(QColor("#8A8A8A")))
        for pts in [
            [(x1,y1),(x1+arr,y1-arr/2),(x1+arr,y1+arr/2)],
            [(x2,y2),(x2-arr,y2-arr/2),(x2-arr,y2+arr/2)],
        ]:
            p = scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in pts]), pen)
            p.setBrush(fill)
        ti = scene.addText(text)
        f  = QFont(); f.setPointSize(11); ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        if y1 < 0:
            ti.setPos((x1+x2)/2 - ti.boundingRect().width()/2, y1 - ti.boundingRect().height() - 8)
        else:
            ti.setPos((x1+x2)/2 - ti.boundingRect().width()/2, y1 + 8)

    def addVerticalDimension(self, scene, x1, y1, x2, y2, text, pen):
        try:
            val = float(text)
            if val == 0:
                return
            if val.is_integer():
                text = str(int(val))
            else:
                text = f"{val:g}"
        except ValueError:
            pass

        scene.addLine(x1, y1, x2, y2, pen)
        ext = 10;  arr = 3
        scene.addLine(x1-ext/2, y1, x1+ext/2, y1, pen)
        scene.addLine(x2-ext/2, y2, x2+ext/2, y2, pen)
        fill = (QBrush(Qt.black) if self.theme.is_light()
                else QBrush(QColor("#8A8A8A")))
        if y2 > y1:
            polys = [
                [(x1,y1),(x1-arr/2,y1+arr),(x1+arr/2,y1+arr)],
                [(x2,y2),(x2-arr/2,y2-arr),(x2+arr/2,y2-arr)],
            ]
        else:
            polys = [
                [(x2,y2),(x2-arr/2,y2+arr),(x2+arr/2,y2+arr)],
                [(x1,y1),(x1-arr/2,y1-arr),(x1+arr/2,y1-arr)],
            ]
        for pts in polys:
            p = scene.addPolygon(
                QPolygonF([QPointF(x, y) for x, y in pts]), pen)
            p.setBrush(fill)
        ti = scene.addText(text)
        f  = QFont(); f.setPointSize(11); ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        if x1 < 0:
            ti.setPos(x1 - ti.boundingRect().width() - 8,
                      (y1+y2)/2 - ti.boundingRect().height()/2)
        else:
            ti.setPos(x1 + 8, (y1+y2)/2 - ti.boundingRect().height()/2)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        from PyQt5.QtCore import Qt
        if hasattr(self, 'view1') and hasattr(self, 'scene1'):
            self.view1.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)
        if hasattr(self, 'view2') and hasattr(self, 'scene2'):
            self.view2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
        if hasattr(self, 'view3') and hasattr(self, 'scene3') and getattr(self, 'show_third', False):
            self.view3.fitInView(self.scene3.sceneRect(), Qt.KeepAspectRatio)


# =============================================================================
# SECTION CAPACITY — 
# =============================================================================
class SectionCapacityDetails(FinPlateCapacityDetails):

    def __init__(self, connection_obj, rows=3, cols=2, main=None, show_third=False):
        self.show_third = show_third
        super().__init__(connection_obj, rows, cols, main)

    def createDrawing(self, scene):
        coeff = 1
        s = self._sc(coeff)
        outline, dim, dash = self._pens(3)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 60/coeff, 60/coeff
        
        try:
            connectivity = getattr(self.main, 'connectivity', '')
        except:
            connectivity = ''

        if connectivity == "Column Web-Beam Web" or connectivity == "Beam-Beam":
            col_color = QColor("#B5B5A0")
            beam_color = QColor("#EEEED1")
            plate_bg_str = "#969684"
            bolt_color = "#FF1D1D"
        else:
            col_color = QColor("#BFBFA9")
            beam_color = QColor("#F8F8DB")
            plate_bg_str = "#A0A08E"
            bolt_color = "#FF3636"

        self._draw_primary_secondary(scene, w, h, coeff, dim, mirror=True, connectivity=connectivity, col_color=col_color, beam_color=beam_color)

        bxs   = self._bxL(edge, g1, g2)
        x_cut = bxs[-1]

        plate_bg = QBrush(QColor(plate_bg_str))
        scene.addRect(0, 0, w, h, dim, plate_bg)

        scene.addLine(x_cut, end, x_cut, h, dash)
        scene.addLine(0, end, x_cut, end, dash)
        self._holes(scene, bxs, end, pitch, hole, outline, coeff, bolt_color)
        self._weld_right(scene, weld, w, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=True)
                            
        scene.setSceneRect(scene.itemsBoundingRect().adjusted(-ho, -vo, ho, vo))

    def createSecondDrawing(self, scene):
        coeff = 1
        s = self._sc(coeff)
        outline, dim, dash = self._pens(3)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 60/coeff, 60/coeff
        
        try:
            connectivity = getattr(self.main, 'connectivity', '')
        except:
            connectivity = ''

        if connectivity == "Column Web-Beam Web" or connectivity == "Beam-Beam":
            col_color = QColor("#B5B5A0")
            beam_color = QColor("#EEEED1")
            plate_bg_str = "#969684"
            bolt_color = "#FF1D1D"
        else:
            col_color = QColor("#BFBFA9")
            beam_color = QColor("#F8F8DB")
            plate_bg_str = "#A0A08E"
            bolt_color = "#FF3636"

        self._draw_primary_secondary(scene, w, h, coeff, dim, mirror=True, connectivity=connectivity, col_color=col_color, beam_color=beam_color)

        bxs   = self._bxL(edge, g1, g2)
        x_cut = bxs[-1]

        plate_bg = QBrush(QColor(plate_bg_str))
        scene.addRect(0, 0, w, h, dim, plate_bg)

        scene.addLine(0,     end,   x_cut, end,     dash)
        scene.addLine(x_cut, end,   x_cut, h - end, dash)
        scene.addLine(0,     h-end, x_cut, h - end, dash)
        self._holes(scene, bxs, end, pitch, hole, outline, coeff, bolt_color)
        self._weld_right(scene, weld, w, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=True)
                            
        scene.setSceneRect(scene.itemsBoundingRect().adjusted(-ho, -vo, ho, vo))
    
    def createThirdDrawing(self, scene):
        coeff = 1
        s = self._sc(coeff)
        outline, dim, dash = self._pens(3)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 60/coeff, 60/coeff
        
        try:
            connectivity = getattr(self.main, 'connectivity', '')
        except:
            connectivity = ''

        if connectivity == "Column Web-Beam Web" or connectivity == "Beam-Beam":
            col_color = QColor("#B5B5A0")
            beam_color = QColor("#EEEED1")
            bolt_color = "#FF1D1D"
        else:
            col_color = QColor("#BFBFA9")
            beam_color = QColor("#F8F8DB")
            bolt_color = "#FF3636"
            
        self._draw_primary_secondary(scene, w, h, coeff, dim, mirror=True, connectivity=connectivity, col_color=col_color, beam_color=beam_color)

        bxs   = self._bxL(edge, g1, g2)
        x_cut = bxs[-1]   # innermost bolt column (closest to weld)

        last_bolt_y = end + (self.rows - 1) * pitch  # y of last bolt row

        plate_bg = QBrush(QColor("#A0A08E"))
        scene.addRect(0, 0, w, h, dim, plate_bg)

        # Vertical: top edge → last bolt row
        scene.addLine(x_cut, 0, x_cut, last_bolt_y, dash)
        # Horizontal: bolt column x → left plate edge, at last bolt row
        scene.addLine(x_cut, last_bolt_y, 0, last_bolt_y, dash)

        self._holes(scene, bxs, end, pitch, hole, outline, coeff, bolt_color)
        self._weld_right(scene, weld, w, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=True)
                            
        scene.setSceneRect(scene.itemsBoundingRect().adjusted(-ho, -vo, ho, vo))


