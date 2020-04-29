import numpy, math
from cad.items.ModelUtils import getGpPt, getGpDir, makeEdgesFromPoints, makeWireFromEdges, makeFaceFromWire
from OCC.Core.gp import gp_Ax1
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeRevol

class QuarterCone(object):

    def __init__(self, b, h, coneAngle):
        self.coneAngle = coneAngle
        self.b = b
        self.h = h
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0, 0, 1.0])
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.a1 = self.sec_origin + self.b * self.uDir
        self.a2 = self.sec_origin
        self.a3 = self.sec_origin + self.h * self.wDir
        self.points = [self.a1, self.a2, self.a3]

    def create_model(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        coneOrigin = self.sec_origin
        revolve_axis = gp_Ax1(getGpPt(coneOrigin), getGpDir(self.wDir))
        aSweep = BRepPrimAPI_MakeRevol(aFace,revolve_axis,math.radians(self.coneAngle)).Shape()
        return aSweep

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    b = 10
    h = 10
    coneAngle = 10

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    channel = QuarterCone(b, h, coneAngle)
    angles = channel.place(origin, uDir, wDir)
    point = channel.compute_params()
    prism = channel.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()