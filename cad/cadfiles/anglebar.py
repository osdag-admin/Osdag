
import numpy
import math
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.GC import GC_MakeArcOfCircle
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods
from OCC.Core.TopAbs import TopAbs_EDGE
from cad.items.ModelUtils import getGpPt, make_edge, makeWireFromEdges, \
    makeFaceFromWire, makePrismFromFace, makeEdgesFromPoints

class Angle(object):
    def __init__(self, L, A, B, T, R1=0, R2=0):
        self.L = L
        self.A = A
        self.B = B
        self.T = T
        #self.R1 = R1
        self.R1 = 0.0
        #self.R2 = R2
        self.R2 = 0.0
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.computeParams()

    def place(self, secOrigin, uDir, wDir):
        self.sec_origin = secOrigin
        self.uDir = uDir
        self.wDir = wDir
        self.computeParams()


    def computeParams(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        root2 = math.sqrt(2)
        self.a1 = self.sec_origin
        self.a2 = self.sec_origin + (self.A) * self.vDir
        self.a3 = self.sec_origin + (self.T) * self.uDir + self.A * self.vDir
        self.a4 = self.sec_origin + (self.T) * self.uDir + (self.T) * self.vDir
        self.a5 = self.sec_origin + (self.B) * self.uDir + self.T * self.vDir
        self.a6 = self.sec_origin + self.B * self.uDir

        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]

    def create_model(self):

        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.L * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)

        return prism

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    L = 50
    A = 15
    B = 15
    T = 2
    R1 = 8
    R2 = 5

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    angle = Angle(L, A, B, T, R1, R2)
    _place = angle.place(origin, uDir, wDir)
    point = angle.computeParams()
    prism = angle.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()