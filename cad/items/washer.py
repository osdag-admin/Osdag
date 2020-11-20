'''
Created on 29-Nov-2014

@author: deepa
@author: deepa
'''
import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Ax2

class Washer(object):
    '''

                                    a2   XX-------------------------+
                                         |X                          X
                                         | X                          X
                                         |  X                          X
                                         |   X--------------------------X
                                         |   |                          |
+-------------->                         |   |  a1                      |
|               w dir                    |   |                          |
|                                        |   |                          |
|                                        |   |    +---------->  gDir    |
|                                        |   |    |                     |
|                                        |   |    |                     |
|                                        |   |    |                     |
|                                        |   |    |                     |
v                                        |   |    |                     |
                                         |   |    v                     |
v dir                                    |   |                          |
                                         |   |    pDir                  |
                                         |   |                          |
                                         |   |                          |
                                         |   |                          |
                                         |   |                          |
                                    a3   X   |                          |
                                          X  |                          |
                                            X+--------------------------+

                                             a4

    '''

    def __init__(self, a, d, t):
        self.a = a
        self.d = d
        self.T = t
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
        self.a1 = self.sec_origin + (self.a / 2.0) * self.uDir + (self.a / 2.0) * self.vDir
        self.a2 = self.sec_origin + (-self.a / 2.0) * self.uDir + (self.a / 2.0) * self.vDir
        self.a3 = self.sec_origin + (-self.a / 2.0) * self.uDir + (-self.a / 2.0) * self.vDir
        self.a4 = self.sec_origin + (self.a / 2.0) * self.uDir + (-self.a / 2.0) * self.vDir
        self.points = [self.a1, self.a2, self.a3, self.a4]

    def create_model(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * -self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)

        cylOrigin = self.sec_origin
        innerCyl = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(cylOrigin), getGpDir(-self.wDir)), self.d/2, self.T+1).Shape()

        prism = BRepAlgoAPI_Cut(prism, innerCyl).Shape()

        return prism


#TOdo : delete this
    # def create_wire(self):
    #     edges = makeEdgesFromPoints(self.points)
    #     wire = makeWireFromEdges(edges)
    #     aFace = makeFaceFromWire(wire)
    #     extrudeDir = self.W * self.wDir  # extrudeDir is a numpy array
    #     prism = makePrismFromFace(aFace, extrudeDir)
    #
    #     return extrudeDir

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    a = 8
    T = 0.5
    d = 2

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    plate = Washer(a, d, T)
    _place = plate.place(origin, uDir, wDir)
    point = plate.compute_params()
    prism = plate.create_model()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()