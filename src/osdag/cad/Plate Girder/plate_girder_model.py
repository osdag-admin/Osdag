# optimised_plate_girder_refactored.py

from ISection import ISection
from notch import Notch
from plate import Plate
from filletweld import FilletWeld
import math
import numpy as np
import time

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Ax1, gp_Dir, gp_Ax3
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform,
    BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM
from OCC.Display.SimpleGui import init_display


class PlateGirder:
    def __init__(self, D, tw, length, gap, T_ft, T_fb, B_ft, B_fb):
        self.D = D
        self.tw = tw
        self.length = length
        self.gap = gap
        self.T_ft = T_ft
        self.T_fb = T_fb
        self.B_ft = B_ft
        self.B_fb = B_fb

    def createPlateGirder(self):
        chamfer_length = 30
        T_is = 15
        L = (min(self.B_ft, self.B_fb) - self.tw) / 2
        b = h = 15
        l = L - chamfer_length
        vertical_weld_height = 0.5 * chamfer_length

        center_plate_color = Quantity_Color(5/255, 5/255, 255/255, Quantity_TOC_RGB)
        top_bottom_plate_color = Quantity_Color(137/255, 95/255, 16/255, Quantity_TOC_RGB)

        display, start_display, *_ = init_display()
        display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])

        def plate_model_with_color(origin, l, b, h, color):
            plate = Plate(l, b, h)
            plate.place(origin, [0., 0., 1.], [0., 1., 0.])
            shape = plate.create_model()
            ais_shape = AIS_Shape(shape)
            ais_shape.SetColor(color)
            display.Context.Display(ais_shape, True)
            return shape

        def fuse_models(models):
            builder = BRep_Builder()
            compound = TopoDS_Compound()
            builder.MakeCompound(compound)
            for m in models:
                builder.Add(compound, m)
            return compound

        def translation_movement(x, y, z, model):
            trsf = gp_Trsf()
            trsf.SetTranslation(gp_Vec(x, y, z))
            return BRepBuilderAPI_Transform(model, trsf).Shape()

        def translation_rotation(angle, axis, model):
            trsf = gp_Trsf()
            trsf.SetRotation(axis, math.radians(angle))
            return BRepBuilderAPI_Transform(model, trsf).Shape()

        def stiffner_plate(position, b, a, thickness, direction):
            c = chamfer_length
            x, y, z = map(float, position)
            y -= thickness/2
            if direction == "right":
                pts = [gp_Pnt(0, 0, (a/2)-c), gp_Pnt(c, 0, a/2), gp_Pnt(b, 0, a/2),
                       gp_Pnt(b, 0, -a/2), gp_Pnt(c, 0, -a/2), gp_Pnt(0, 0, (-a/2)+c)]
            else:
                pts = [gp_Pnt(0, 0, (a/2)-c), gp_Pnt(-c, 0, a/2), gp_Pnt(-b, 0, a/2),
                       gp_Pnt(-b, 0, -a/2), gp_Pnt(-c, 0, -a/2), gp_Pnt(0, 0, (-a/2)+c)]

            wire = BRepBuilderAPI_MakeWire()
            for i in range(len(pts)):
                wire.Add(BRepBuilderAPI_MakeEdge(pts[i], pts[(i+1) % len(pts)]).Edge())
            face = BRepBuilderAPI_MakeFace(wire.Wire()).Face()
            prism = BRepPrimAPI_MakePrism(face, gp_Vec(0, thickness, 0)).Shape()

            local_ax3 = gp_Ax3(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1), gp_Dir(0, 1, 0))
            global_ax3 = gp_Ax3(gp_Pnt(x, y, z), gp_Dir(0, 0, 1), gp_Dir(0, 1, 0))
            trsf = gp_Trsf()
            trsf.SetDisplacement(local_ax3, global_ax3)
            return BRepBuilderAPI_Transform(prism, trsf, True).Shape()

        def vertical_weld(weld_height, length):
            p1, p2, p3 = gp_Pnt(0, 0, 0), gp_Pnt(weld_height, 0, 0), gp_Pnt(0, -weld_height, 0)
            edges = [BRepBuilderAPI_MakeEdge(p1, p2).Edge(), BRepBuilderAPI_MakeEdge(p2, p3).Edge(),
                     BRepBuilderAPI_MakeEdge(p3, p1).Edge()]
            wire = BRepBuilderAPI_MakeWire(*edges).Wire()
            face = BRepBuilderAPI_MakeFace(wire).Face()
            return BRepPrimAPI_MakePrism(face, gp_Vec(0, 0, self.D - 2 * chamfer_length)).Shape()

        def create_weld_model(thickness, width, position, direction):
            uDir, shaftDir = ([0., 0., 1.], [0., 1., 0.]) if direction == 'y' else ([1., 0., 0.], [0., 0., 1.])
            FWeld = FilletWeld(thickness, thickness, width)
            FWeld.place(position, uDir, shaftDir)
            return FWeld.create_model(0)

        def filletWeld_model(b, h, l, y, position):
            x = self.tw//2 + chamfer_length if position == "right" else -self.tw//2 - l - chamfer_length
            FWeld = FilletWeld(b, h, l)
            FWeld.place([0., 0., 0.], [0., 0., 1.], [1., 0., 0.])
            base = FWeld.create_model(0)

            def rotate_and_translate(angle, dx, dy, dz):
                shape = translation_rotation(angle, gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), base)
                return translation_movement(dx, dy, dz, shape)

            front = BRepAlgoAPI_Fuse(
                rotate_and_translate(0, x, y - T_is//2, self.D//2),
                rotate_and_translate(90, x, y - T_is//2, -self.D//2)
            ).Shape()

            back = BRepAlgoAPI_Fuse(
                rotate_and_translate(180, x, y + T_is//2, self.D//2),
                rotate_and_translate(270, x, y + T_is//2, -self.D//2)
            ).Shape()

            return BRepAlgoAPI_Fuse(front, back).Shape()

        # --- Begin assembling model ---
        center_plate = plate_model_with_color(np.array([0., 0., 0.]), self.tw, self.length, self.D, center_plate_color)
        top_plate = plate_model_with_color(np.array([0, 0, (self.D + self.T_ft) // 2]), self.B_ft, self.length, self.T_ft, top_bottom_plate_color)
        bottom_plate = plate_model_with_color(np.array([0, 0, -(self.D + self.T_fb) // 2]), self.B_fb, self.length, self.T_fb, top_bottom_plate_color)

        ISection_model = BRepAlgoAPI_Fuse(bottom_plate, top_plate).Shape()

        # Longitudinal welds
        welds = [
            create_weld_model(0.5 * chamfer_length, self.length, np.array([self.tw // 2, 0., -self.D // 2]), "y"),
            create_weld_model(0.5 * chamfer_length, self.length, np.array([-self.tw // 2, 0., -self.D // 2]), "y"),
            create_weld_model(0.5 * chamfer_length, self.length, np.array([self.tw // 2, 0., self.D // 2]), "y"),
            create_weld_model(0.5 * chamfer_length, self.length, np.array([-self.tw // 2, 0., self.D // 2]), "y")
        ]
        longitudinal_weld = fuse_models(welds)

        stiffners, welds = [], []
        v_weld = vertical_weld(vertical_weld_height, self.D - 2 * chamfer_length)
        for y in range(self.gap, self.length, self.gap):
            stiffners.extend([
                stiffner_plate(np.array([self.tw/2, y, 0]), L, self.D, T_is, "right"),
                stiffner_plate(np.array([-self.tw/2, y, 0]), L, self.D, T_is, "left")
            ])
            welds.extend([
                filletWeld_model(b, h, l, y, "right"),
                filletWeld_model(b, h, l, y, "left"),
                translation_movement(self.tw/2, y, (-self.D/2)+chamfer_length, v_weld),
                translation_movement(self.tw/2, y+T_is/2, (-self.D/2)+chamfer_length,
                                     translation_rotation(90, gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), v_weld)),
                translation_movement(-self.tw/2, y, (-self.D/2)+chamfer_length,
                                     translation_rotation(-90, gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), v_weld)),
                translation_movement(-self.tw/2, y+T_is/2, (-self.D/2)+chamfer_length,
                                     translation_rotation(-180, gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), v_weld))
            ])

        stiffners = fuse_models(stiffners)
        welds = fuse_models(welds)
        display.DisplayShape(ISection_model, update=True)
        display.DisplayShape(center_plate, update=True)
        display.DisplayShape(stiffners, material=Graphic3d_NOM_ALUMINIUM, update=True)
        display.DisplayShape(longitudinal_weld, color="red", update=True)
        display.DisplayShape(welds, color="red", update=True)
        start_display()

        plate_girder_model = BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(center_plate, ISection_model).Shape(), stiffners)
        plate_girder_model = BRepAlgoAPI_Fuse(plate_girder_model, welds).Shape()
        return plate_girder_model
