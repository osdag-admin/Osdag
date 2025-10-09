
import numpy
from .ModelUtils import *
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

class RectHollow(object):


    def __init__(self, L, W, H, T):
        self.L = L
        self.H = H
        self.W = W
        self.T = T
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin - (self.L) / 2 * self.uDir - (self.H) / 2 * self.wDir - (self.W) / 2 * self.vDir
        self.a2 = self.a1 + (self.T) / 2 * self.uDir + (self.T) / 2 * self.vDir

    def create_model(self):
        box1 = BRepPrimAPI_MakeBox(getGpPt(self.a1),self.L, self.W, self.H).Shape()
        box2 = BRepPrimAPI_MakeBox(getGpPt(self.a2),self.L-self.T, self.W-self.T, self.H).Shape()
        prism = BRepAlgoAPI_Cut(box1, box2).Shape()
        return prism


if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    L = 100
    T = 6
    W = 92
    H = 150

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    rhollow = RectHollow(L, W, H, T)
    _place = rhollow.place(origin, uDir, wDir)
    point = rhollow.compute_params()
    prism = rhollow.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
