'''
Created on 20-Jan-2020

@author: Anand Swaroop
'''
import numpy
from numpy import sqrt, square
from cad.items.ModelUtils import *  # getGpPt, getGpDir, makeEdgesFromPoints, makeWireFromEdges, makePrismFromFace, makeFaceFromWire
import math
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace

from OCC.Core.gp import gp_Dir, gp_Circ, gp_Ax2
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

from OCC.Core.gp import gp_Ax1
from OCC.Core.BRepPrimAPI import *



class AnchorBolt_A(object):

    def __init__(self, l, c, a, r, ex):
        self.ex = ex
        self.l = l
        self.c = c
        self.a = a
        self.r = r
        self.origin = None
        self.uDir = None
        self.shaftDir = None
        self.vDir = None
        self.points = []

    def place(self, origin, uDir, shaftDir):
        self.origin = origin
        self.uDir = uDir
        self.shaftDir = shaftDir
        self.compute_params()

    def compute_params(self):
        self.cylex_length = self.ex
        self.cyl1_length = self.l - self.c
        self.cyl2_length = self.c - self.a / 2
        self.cyl3_arc_dia = self.a / 2 - self.r
        self.cyl4_length = self.c - self.a / 2 - 4 * self.r

        self.p1 = self.origin
        self.p2 = self.p1 - self.cyl1_length * self.shaftDir
        self.p3 = self.p2 - self.cyl3_arc_dia * self.uDir - self.cyl2_length * self.shaftDir
        self.p4 = self.p3 + self.cyl3_arc_dia * self.uDir
        self.p5 = self.p4 + self.cyl3_arc_dia * self.uDir
        self.p6 = self.p5 - (self.a / 2) * self.uDir + - (self.cyl3_arc_dia - self.r) * self.shaftDir

        self.angle1 = numpy.array(self.p3 - self.p2)  # 30degrees
        self.angle2 = numpy.array(self.p2 - self.p5)

        self.hightcyl2 = sqrt(square(self.cyl2_length) + square(self.cyl3_arc_dia))

    def create_model(self):
        boltCylinderex = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p1), getGpDir(self.shaftDir)), self.r,
                                                 self.cylex_length).Shape()
        boltCylinder1 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p1), getGpDir(-self.shaftDir)), self.r,
                                                 self.cyl1_length).Shape()
        boltCylinder2 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p2), getGpDir(self.angle1)), self.r,
                                                 self.hightcyl2).Shape()
        sphere1 = BRepPrimAPI_MakeSphere(getGpPt(self.p2), self.r).Shape()
        sphere2 = BRepPrimAPI_MakeSphere(getGpPt(self.p3), self.r).Shape()
        sphere3 = BRepPrimAPI_MakeSphere(getGpPt(self.p5), self.r).Shape()

        edg_points = gp_Circ(gp_Ax2(getGpPt(self.p3), getGpDir(self.shaftDir)), self.r)
        hexwire = BRepBuilderAPI_MakeWire()
        hexedge = BRepBuilderAPI_MakeEdge(edg_points).Edge()
        hexwire.Add(hexedge)
        hexwire_wire = hexwire.Wire()
        hexface = BRepBuilderAPI_MakeFace(hexwire_wire).Face()
        revolve_axis = gp_Ax1(getGpPt(self.p4), gp_Dir(0, -1, 0))
        boltCylinder3 = BRepPrimAPI_MakeRevol(hexface, revolve_axis, math.radians(180.)).Shape()

        boltCylinder4 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p5), getGpDir(self.angle2)), self.r,
                                                 self.cyl4_length).Shape()

        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinder1, boltCylinder2).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(sphere1, Anchor_BOlt).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(sphere2, Anchor_BOlt).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinder3, Anchor_BOlt).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(sphere3, Anchor_BOlt).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinder4, Anchor_BOlt).Shape()

        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinderex, Anchor_BOlt).Shape()

        return Anchor_BOlt


class AnchorBolt_B(object):

    def __init__(self, l, r, ex, c=0, a=0):
        self.ex = ex
        self.l = l
        self.c = c
        self.a = a
        self.r = r
        self.origin = None
        self.uDir = None
        self.shaftDir = None
        self.vDir = None
        self.points = []

    def place(self, origin, uDir, shaftDir):
        self.origin = origin
        self.uDir = uDir
        self.shaftDir = -shaftDir
        self.compute_params()

    def compute_params(self):
        self.cylex_length = self.ex
        self.cyl4_arc_dia = 3 * self.r
        self.cyl3_length = 10 * self.r - self.cyl4_arc_dia
        self.cyl2_length = 2 * self.r
        self.cyl1_length = self.l - self.cyl3_length - self.cyl2_length - self.cyl4_arc_dia
        self.cyl5_length = 5 * self.r - 3 * self.r  # written like this to understand formula

        self.p1 = self.origin
        self.p2 = self.p1 + self.cyl1_length * self.shaftDir
        self.p3 = self.p2 - 2 * self.r * self.uDir + self.cyl2_length * self.shaftDir
        self.p4 = self.p3 + self.cyl3_length * self.shaftDir
        self.p5 = self.p4 + 2 * self.r * self.uDir
        self.p6 = self.p5 + 2 * self.r * self.uDir

        self.cyl2_angle = numpy.array(self.p3 - self.p2)
        self.cyl2_ht = sqrt(square(self.cyl2_length) + square(2 * self.r))

    def create_model(self):
        boltCylinderex = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p1), getGpDir(-self.shaftDir)), self.r,
                                                  self.cylex_length).Shape()
        boltCylinder1 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p1), getGpDir(self.shaftDir)), self.r,
                                                 self.cyl1_length).Shape()
        boltCylinder2 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p2), getGpDir(self.cyl2_angle)), self.r,
                                                 self.cyl2_ht).Shape()
        boltCylinder3 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p3), getGpDir(self.shaftDir)), self.r,
                                                 self.cyl3_length).Shape()
        boltCylinder4 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p6), getGpDir(-self.shaftDir)), self.r,
                                                 self.cyl5_length).Shape()

        sphere1 = BRepPrimAPI_MakeSphere(getGpPt(self.p2), self.r).Shape()
        sphere2 = BRepPrimAPI_MakeSphere(getGpPt(self.p3), self.r).Shape()

        edg_points = gp_Circ(gp_Ax2(getGpPt(self.p4), getGpDir(self.shaftDir)), self.r)
        hexwire = BRepBuilderAPI_MakeWire()
        hexedge = BRepBuilderAPI_MakeEdge(edg_points).Edge()
        hexwire.Add(hexedge)
        hexwire_wire = hexwire.Wire()
        hexface = BRepBuilderAPI_MakeFace(hexwire_wire).Face()
        revolve_axis = gp_Ax1(getGpPt(self.p5), gp_Dir(0, -1, 0))
        revolved_shape = BRepPrimAPI_MakeRevol(hexface, revolve_axis, math.radians(180.)).Shape()

        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinder1, boltCylinder2).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinder3, Anchor_BOlt).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(revolved_shape, Anchor_BOlt).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinder4, Anchor_BOlt).Shape()

        Anchor_BOlt = BRepAlgoAPI_Fuse(sphere1, Anchor_BOlt).Shape()
        Anchor_BOlt = BRepAlgoAPI_Fuse(sphere2, Anchor_BOlt).Shape()

        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinderex, Anchor_BOlt).Shape()

        return Anchor_BOlt


class AnchorBolt_Endplate(object):

    def __init__(self, l, r, ex, c=0, a=0):
        self.ex = ex
        self.l = l
        self.c = a
        self.a = a
        self.r = r
        self.origin = None
        self.uDir = None
        self.shaftDir = None
        self.vDir = None
        self.points = []

    def place(self, origin, uDir, shaftDir):
        self.origin = origin
        self.uDir = uDir
        self.shaftDir = shaftDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.shaftDir, self.uDir)

        self.cylex_length = self.ex
        self.cyl1_length = self.l
        self.endplate_thickness = 5
        self.head = self.endplate_thickness / 5
        self.endplate_width = self.a

        self.p1 = self.origin
        self.p2 = self.p1 - (self.l - self.endplate_thickness - self.head) * self.shaftDir
        self.p3 = self.p2 - self.endplate_width / 2 * self.uDir - self.endplate_width / 2 * self.vDir - self.endplate_thickness / 2 * self.shaftDir

    def create_model(self):
        boltCylinderex = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p1), getGpDir(self.shaftDir)), self.r,
                                                  self.cylex_length).Shape()
        boltCylinder1 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p1), getGpDir(-self.shaftDir)), self.r,
                                                 self.cyl1_length).Shape()
        bolt_endplate = BRepPrimAPI_MakeBox(getGpPt(self.p3), self.endplate_width, self.endplate_width,
                                            self.endplate_thickness).Shape()

        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinder1, bolt_endplate).Shape()

        Anchor_BOlt = BRepAlgoAPI_Fuse(boltCylinderex, Anchor_BOlt).Shape()

        return Anchor_BOlt



if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    l = 250
    c = 125
    a = 75
    r = 12
    ex = 100

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    ABolt_A = AnchorBolt_A(l,c,a,r, ex)
    # ABolt_B = AnchorBolt_B(l,c,a,r, ex)
    # ABolt_E = AnchorBolt_Endplate(l,c,a,r, ex)
    _place = ABolt_A.place(origin, uDir, shaftDir)
    point = ABolt_A.compute_params()
    prism = ABolt_A.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
