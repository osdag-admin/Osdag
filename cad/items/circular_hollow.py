
import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Dir, gp_Circ, gp_Ax2
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

class CircularHollow(object):


    def __init__(self, r, T, H):
        self.r = r
        self.H = H
        self.T = T
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.shaftDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.shaftDir * self.uDir

    def place(self, sec_origin, uDir, shaftDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.shaftDir = shaftDir
        self.compute_params()

    def compute_params(self):
        self.p1 = self.sec_origin - (self.H)/2 * self.shaftDir

    def create_model(self):
        cylinder1 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p1), getGpDir(self.shaftDir)), self.r,
                                                 self.H).Shape()
        cylinder2 = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(self.p1), getGpDir(self.shaftDir)), self.r-self.T,
                                                 self.H).Shape()
        prism = BRepAlgoAPI_Cut(cylinder1, cylinder2).Shape()
        return prism


if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    r = 100
    T = 6
    H = 1000

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    chollow = CircularHollow(r, T, H)
    _place = chollow.place(origin, uDir, wDir)
    point = chollow.compute_params()
    prism = chollow.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()