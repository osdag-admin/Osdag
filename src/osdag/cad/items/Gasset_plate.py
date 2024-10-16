'''
Created on 15-May-2020

@author: Anand Swaroop
'''
import numpy
import math
from cad.items.ModelUtils import *


class GassetPlate(object):

    def __init__(self, L, H, T, degree):
        self.L = L
        self.H = H
        self.T = T
        self.degree = degree
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
        self.vDir = numpy.cross(self.wDir, self.uDir)

        self.p1 = self.sec_origin + self.H / 2 * self.wDir
        self.p2 = self.p1 - self.H * self.wDir
        self.p3 = self.p2 - self.L * self.uDir - (self.L * math.tan(self.degree * math.pi / 180)) * self.wDir
        self.p4 = self.p3 + (self.H + 2 * self.L * math.tan(self.degree * math.pi / 180)) * self.wDir
        self.points = [self.p1, self.p2, self.p3, self.p4]

    def create_model(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * self.vDir
        prism = makePrismFromFace(aFace, extrudeDir)

        return prism


if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    L = 540
    H = 255
    T = 2
    D = 30

    origin = numpy.array([0., 0., 0.])
    uDir = numpy.array([1., 0., 0.])
    wDir = numpy.array([0., 0., 1.])

    GPlate = GassetPlate(L, H, T, D)
    _place = GPlate.place(origin, uDir, wDir)
    point = GPlate.compute_params()
    prism = GPlate.create_model()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
