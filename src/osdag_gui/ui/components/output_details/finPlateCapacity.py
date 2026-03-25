import sys
from PySide6.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QGraphicsView, QSizeGrip,
                               QGraphicsScene, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPolygonF, QBrush
from PySide6.QtCore import QPointF
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
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

    def _sc(self, coeff=2):
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

    def _holes(self, scene, bxs, end, pitch, hole, pen):
        for row in range(self.rows):
            for col in range(self.cols):
                cx = bxs[col]
                cy = end + row * pitch
                scene.addEllipse(cx - hole/2, cy - hole/2, hole, hole, pen)

    def _weld_left(self, scene, weld, h, dim_pen):
        if weld > 0:
            scene.addRect(0, 0, weld, h, QPen(Qt.NoPen), QBrush(Qt.red))
            scene.addLine(weld, 0, weld, h, dim_pen)

    def _weld_right(self, scene, weld, w, h, dim_pen):
        if weld > 0:
            scene.addRect(w - weld, 0, weld, h, QPen(Qt.NoPen), QBrush(Qt.red))
            scene.addLine(w - weld, 0, w - weld, h, dim_pen)

    def createDrawing(self, scene):
        coeff = 2
        s = self._sc(coeff)
        outline, dim, dash = self._pens(coeff)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 40/coeff, 60/coeff
        scene.setSceneRect(-ho, -vo, w + 2*vo, h + 2*ho)

        bxs   = self._bxL(edge, g1, g2)
        x_cut = bxs[0]

        scene.addLine(x_cut, end, x_cut, h, dash)
        scene.addLine(x_cut, end, w, end, dash)

        scene.addRect(0, 0, w, h, dim)
        self._holes(scene, bxs, end, pitch, hole, outline)
        self._weld_left(scene, weld, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=False)

    def createSecondDrawing(self, scene):
        coeff = 2
        s = self._sc(coeff)
        outline, dim, dash = self._pens(coeff)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 40/coeff, 60/coeff
        scene.setSceneRect(-ho, -vo, w + 2*vo, h + 2*ho)

        bxs   = self._bxL(edge, g1, g2)
        x_cut = bxs[0]

        scene.addLine(x_cut, end,   w,     end,     dash)
        scene.addLine(x_cut, end,   x_cut, h - end, dash)
        scene.addLine(x_cut, h-end, w,     h - end, dash)

        scene.addRect(0, 0, w, h, dim)
        self._holes(scene, bxs, end, pitch, hole, outline)
        self._weld_left(scene, weld, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=False)

    def _addDimensions(self, scene, width, height, pitch, end,
                       g1, g2, edge, pen, coeff, mirror):
        ho, vo = 20/coeff, 30/coeff

        if not mirror:
            segs = [(0, edge), (edge, width)]
        else:
            segs = [(0, width - edge), (width - edge, width)]
        for x1, x2 in segs:
            self.addHorizontalDimension(scene, x1, -ho, x2, -ho,
                                        f"{x2-x1:.1f}", pen)

        self.addVerticalDimension(scene, width+vo, 0,
                                  width+vo, end, str(end), pen)
        for i in range(self.rows - 1):
            self.addVerticalDimension(scene, width+vo, end + i*pitch,
                                      width+vo, end + (i+1)*pitch,
                                      str(pitch), pen)
        self.addVerticalDimension(scene, width+vo, height,
                                  width+vo, height-end, str(end), pen)
        total = 2*end + (self.rows-1)*pitch
        self.addVerticalDimension(scene, -vo, 0, -vo, total,
                                  str(total), pen)

    def addHorizontalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)
        ext = 10;  arr = 2
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
        f  = QFont(); f.setPointSize(2); ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        if y1 < 0:
            ti.setPos((x1+x2)/2 - ti.boundingRect().width()/2, y1-12)
        else:
            ti.setPos((x1+x2)/2 - ti.boundingRect().width()/2, y1+5)

    def addVerticalDimension(self, scene, x1, y1, x2, y2, text, pen):
        scene.addLine(x1, y1, x2, y2, pen)
        ext = 10;  arr = 2
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
        f  = QFont(); f.setPointSize(2); ti.setFont(f)
        ti.setDefaultTextColor(Qt.black if self.theme.is_light() else Qt.white)
        if x1 < 0:
            ti.setPos(x1 - ti.boundingRect().width(),
                      (y1+y2)/2 - ti.boundingRect().height()/2)
        else:
            ti.setPos(x1, (y1+y2)/2 - ti.boundingRect().height()/2)


# =============================================================================
# SECTION CAPACITY — 
# =============================================================================
class SectionCapacityDetails(FinPlateCapacityDetails):

    def createDrawing(self, scene):
        coeff = 2
        s = self._sc(coeff)
        outline, dim, dash = self._pens(coeff)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 40/coeff, 60/coeff
        scene.setSceneRect(-ho, -vo, w + 2*vo, h + 2*ho)

        bxs   = self._bxR(w, edge, g1, g2)
        x_cut = bxs[0]

        scene.addLine(x_cut, end, x_cut, h, dash)
        scene.addLine(0, end, x_cut, end, dash)

        scene.addRect(0, 0, w, h, dim)
        self._holes(scene, bxs, end, pitch, hole, outline)
        self._weld_right(scene, weld, w, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=True)

    def createSecondDrawing(self, scene):
        coeff = 2
        s = self._sc(coeff)
        outline, dim, dash = self._pens(coeff)
        w, h  = s['width'], s['height']
        end   = s['end'];   pitch = s['pitch']
        edge  = s['edge'];  g1 = s['g1'];  g2 = s['g2']
        hole  = s['hole'];  weld = s['weld']

        ho, vo = 40/coeff, 60/coeff
        scene.setSceneRect(-ho, -vo, w + 2*vo, h + 2*ho)

        bxs   = self._bxR(w, edge, g1, g2)
        x_cut = bxs[0]

        scene.addLine(0,     end,   x_cut, end,     dash)
        scene.addLine(x_cut, end,   x_cut, h - end, dash)
        scene.addLine(0,     h-end, x_cut, h - end, dash)

        scene.addRect(0, 0, w, h, dim)
        self._holes(scene, bxs, end, pitch, hole, outline)
        self._weld_right(scene, weld, w, h, dim)

        self._addDimensions(scene, w, h, pitch, end, g1, g2,
                            edge, dim, coeff, mirror=True)


