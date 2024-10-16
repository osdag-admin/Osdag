'''
Created on 29-Nov-2014

@author: Anand Swaroop
'''
import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
#from notch import Notch
from cad.items.notch import Notch
"""


"""

"""
                     <---------------+ B +----------------------->

                                                         +
                                                         |
                                                         |
+--+--+          a3  +-----------------------------------v-------+  a4
   |                 |                                           |
   |                 |                                           |
   |                 |                                   T       |
   |                 |                                           |
   |                 |          +------------------------^-------+ a5
   |                 |          | a6                     |
   |                 |          |                        |
   |                 |          |                        +
   |                 |          |
   |                 |          |
   |                 |          |
   |                 |          |
   |                 |          |
   +                 |          |
   D          +----->+    t     <------+
   +                 |          |
   |                 |          |
   |                 |          |
   |                 |          |
   |                 |          |
   |                 |          |                         +
   |                 |          |                         |
   |                 |          |                         |
   |                 |          |a7                       |
   |                 |          +-------------------------v-------+  a8
   |                 |                                            |
   |                 |                                            |
   |                 |                                    T       |
   |                 |                                            |
   v                 +------------------------------------^-------+a1
                    a2                                    |
                                                          |
                                                          |
                                                          +

"""


class Channel(object):
    '''


    '''

    def __init__(self, B, T, D, t, R1, R2, L):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.R1 = R1
        self.R2 = R2
        self.L = L
        self.clearDist = 20
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])

        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin
        self.a2 = self.a1 - (self.B) * self.uDir
        self.a3 = self.a2 + (self.D) * self.vDir
        self.a4 = self.a3 + (self.B) * self.uDir
        self.a5 = self.a4 - (self.T) * self.vDir
        self.a6 = self.a5 - (self.B - self.t) * self.uDir
        self.a7 = self.a6 - (self.D - 2 * self.T) * self.vDir
        self.a8 = self.a7 + (self.B - self.t) * self.uDir

        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8]

        # self.points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]

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
    
    B = 20
    T = 2
    D = 40
    t = 1.5
    L = 100

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    channel = Channel(B, T, D, t, 0, 0, L)
    _place = channel.place(origin, uDir, shaftDir)
    point = channel.compute_params()
    prism = channel.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()