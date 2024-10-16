
import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse

class Stiffener_flange(object):
    def __init__(self, H, L, T, t_f, L_h, L_v, to_left=True):
       
        self.H = H
        self.L = L
        self.T = T
        self.t = t_f
        self.t_l = (T - t_f) * 5 + 0.001  #length of the cut
        self.L_h = L_h
        self.L_v = L_v
        self.to_left = to_left

        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0.0, 0.0])
        self.wDir = numpy.array([0.0, 0.0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
       
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
       
        self.vDir = numpy.cross(self.wDir, self.uDir)   # Cross product of vector wDir and uDir
        self.a1 = self.sec_origin + self.H * self.wDir
        self.a2 = self.a1 + self.L_h * self.uDir
        self.a3 = self.a2 - (self.H - self.L_v) * self.wDir + (self.L - self.L_h) * self.uDir
        self.a4 = self.a3 - self.L_v * self.wDir
        self.a5 = self.a4 - self.L*self.uDir
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5]

        self.b1 = self.sec_origin
        self.b2 = self.sec_origin + (self.T - self.t) * self.vDir - 0.001 * self.vDir
        self.b3 = self.sec_origin + self.t_l * self.uDir
        self.points2 = [self.b1, self.b2, self.b3] 

        self.c1 = self.sec_origin + self.T * self.vDir
        self.c2 = self.c1 + (self.t - self.T) * self.vDir - 0.01 * self.vDir
        self.c3 = self.c1 + self.t_l * self.uDir
        self.points3 = [self.c1, self.c2, self.c3]  

    def create_model(self):
        
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * self.vDir
        prism1 = makePrismFromFace(aFace, extrudeDir)

        edges = makeEdgesFromPoints(self.points2)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.H * self.wDir
        prism2 = makePrismFromFace(aFace, extrudeDir)

        edges = makeEdgesFromPoints(self.points3)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.H * self.wDir
        prism3 = makePrismFromFace(aFace, extrudeDir)

        if self.to_left:
            prism = BRepAlgoAPI_Cut(prism1, prism2).Shape()
        else:
            prism = BRepAlgoAPI_Cut(prism1, prism3).Shape()

        return prism


if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    H = 225
    L = 175
    T = 18
    L_h = 30
    L_v = 100

    t_f = 15
    t_l = 20

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    stiffener = Stiffener_flange(H, L, T, t_f, L_h, L_v,  to_left=True)
    _place = stiffener.place(origin, uDir, wDir)
    point = stiffener.compute_params()
    prism = stiffener.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()