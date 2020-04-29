'''
Created on 29-Nov-2014

@author: deepa
@author: deepa
'''
import numpy
from cad.items.ModelUtils import *


class Plate(object):
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

    def __init__(self, L, W, T):
        self.L = L
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
        self.a1 = self.sec_origin + (self.T / 2.0) * self.uDir + (self.L / 2.0) * self.vDir
        self.a2 = self.sec_origin + (-self.T / 2.0) * self.uDir + (self.L / 2.0) * self.vDir
        self.a3 = self.sec_origin + (-self.T / 2.0) * self.uDir + (-self.L / 2.0) * self.vDir
        self.a4 = self.sec_origin + (self.T / 2.0) * self.uDir + (-self.L / 2.0) * self.vDir
        self.points = [self.a1, self.a2, self.a3, self.a4]

    def create_model(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.W * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)

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

    L = 10
    T = 2
    W = 8

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    channel = Plate(L, W, T)
    angles = channel.place(origin, uDir, wDir)
    point = channel.compute_params()
    prism = channel.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()