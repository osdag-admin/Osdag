'''
Created on 08-May-2020

@author: Anand Swaroop
'''

import numpy
import copy
from numpy import sqrt, square
from cad.items.ModelUtils import *  # getGpPt, getGpDir, makeEdgesFromPoints, makeWireFromEdges, makePrismFromFace, makeFaceFromWire
import math
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace

from OCC.Core.gp import gp_Dir, gp_Circ, gp_Ax2
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

from OCC.Core.gp import gp_Ax1
from OCC.Core.BRepPrimAPI import *

from cad.items.plate import Plate
from cad.items.filletweld import FilletWeld


class Grout(object):

    def __init__(self, L, W, T):
        self.L = L
        self.W = W
        self.T = T

        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)

        self.p1 = self.sec_origin + numpy.array(
            [0.0, -self.L / 2, self.T / 2])  # self.T/2*self.wDir) + (self.L/2*self.uDir)
        self.p2 = self.p1 + numpy.array([0.0, self.L, 0.0])
        self.p3 = self.p2 + numpy.array([self.W, 0., 0.0])
        self.p4 = self.p3 + numpy.array([0.0, -self.L, 0.0])

        # self.p1 = self.sec_origin + self.L / 2 * self.uDir +  self.T / 2 * self.wDir
        # self.p2 = self.p1 - self.L*self.uDir
        # self.p3 = self.p2 + self.W*self.wDir
        # self.p4 = self.p3 + self.L*self.uDir

        return [self.p1, self.p2, self.p3, self.p4]

    def createWedgeGeometry(self):
        wedgeL_1 = FilletWeld(b=self.T, h=self.T, L=self.L)
        wedgeL_2 = copy.deepcopy(wedgeL_1)
        wedgeW_1 = FilletWeld(b=self.T, h=self.T, L=self.W)
        wedgeW_2 = copy.deepcopy(wedgeW_1)

        wedgeL_1uDir = numpy.array([-1.0, 0.0, 0.0])
        wedgeL_1wDir = numpy.array([0.0, -1.0, 0.0])
        wedgeL_1.place(self.p3, wedgeL_1uDir, wedgeL_1wDir)

        wedgeL_1Model = wedgeL_1.create_model()

        wedgeL_2uDir = numpy.array([1.0, 0.0, 0.0])
        wedgeL_2wDir = numpy.array([0.0, 1.0, 0.0])
        wedgeL_2.place(self.p1, wedgeL_2uDir, wedgeL_2wDir)

        wedgeL_2Model = wedgeL_2.create_model()

        wedgeW_1uDir = numpy.array([0.0, 1.0, 0.0])
        wedgeW_1wDir = numpy.array([-1.0, 0.0, 0.0])
        wedgeW_1.place(self.p4, wedgeW_1uDir, wedgeW_1wDir)
        wedgeW_1Model = wedgeW_1.create_model()
        #

        wedgeW_2uDir = numpy.array([0.0, -1.0, 0.0])
        wedgeW_2wDir = numpy.array([1.0, 0.0, 0.0])
        wedgeW_2.place(self.p2, wedgeW_2uDir, wedgeW_2wDir)

        wedgeW_2Model = wedgeW_2.create_model()

        wedge = BRepAlgoAPI_Fuse(wedgeL_1Model, wedgeL_2Model).Shape()
        wedge = BRepAlgoAPI_Fuse(wedge, wedgeW_1Model).Shape()
        wedge = BRepAlgoAPI_Fuse(wedge, wedgeW_2Model).Shape()

        return wedge

    def createPlateGeometry(self):
        body = Plate(L=self.L, W=self.W, T=self.T)
        body.place(self.sec_origin, self.uDir, self.wDir)

        part1 = body.create_model()
        return part1

    def create_model(self):
        part = self.createPlateGeometry()
        wedge = self.createWedgeGeometry()

        prism = BRepAlgoAPI_Cut(part, wedge).Shape()
        return prism


if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()
    from OCC.gp import gp_Pnt

    L = 500
    T = 50
    W = 300

    origin = numpy.array([0., 0., 0.])
    uDir = numpy.array([0., 0., 1.])
    wDir = numpy.array([1., 0., 0.])

    vDir = numpy.array([0.0, 1.0, 0.0])

    channel = Grout(L, W, T)
    angles = channel.place(origin, uDir, wDir)
    point = channel.compute_params()
    prism = channel.create_model()

    p1 = (T / 2 * wDir) - (L / 2 * vDir)
    p2 = p1 + L * vDir
    p3 = p2 + W * uDir
    p4 = p3 - L * vDir

    Point = gp_Pnt(0.0, -L / 2, T / 2)
    display.DisplayMessage(Point, "P1")

    Point = gp_Pnt(0.0, -L / 2 + L, T / 2)
    display.DisplayMessage(Point, "P2")

    Point = gp_Pnt(W, -L / 2 + L, T / 2)
    display.DisplayMessage(Point, "P3")

    Point = gp_Pnt(W, -L / 2 + L - L, T / 2)
    display.DisplayMessage(Point, "P4")

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
