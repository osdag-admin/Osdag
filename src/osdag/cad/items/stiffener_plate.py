'''
Created on 16-May-2019

@author: Anand Swaroop
'''

import numpy
from cad.items.ModelUtils import *
from OCC.Core.gp import (gp_Vec, gp_Pnt, gp_Trsf, gp_OX, gp_OY,
                         gp_OZ, gp_XYZ, gp_Ax2, gp_Dir, gp_GTrsf, gp_Mat)
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge,
                                     BRepBuilderAPI_MakeVertex,
                                     BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge2d,
                                     BRepBuilderAPI_Transform)
from math import radians


class StiffenerPlate(object):
    '''
                                   L11                                      R11

                                        a1                              a2
                    ^            X      X+-----------------------------+X       X
                    |                  X                                 X
                    |      L12        X                                    X         R12
                    |               X                                        X
                    |          a8 X                                            X+  a3
                    |             |                                             |
                    |             |                     (0,0)                   |
                W   |             |                       x                     |
                    |             |                                             |
                    |             |                                             |
                    |             |                                             |
                    |             |                                             |
                    |           a7+X                                            X a4
                    |               X                                         X
                    |       L22       X                                     X         R22
                    |             X     X+--------------------------------+X    X
                    +                   a6                                  a5

                                     L21                                      R21



                                  +---------------------------------------------->
                                                        L



    '''

    def __init__(self, L, W, T,L11=0.01, L12=0.0, R11=0.01, R12=0.0, R21=0.01, R22=0.0, L21=0.01, L22=0.0):
        self.L = L
        self.W = W
        self.T = T
        self.L11 = L11
        self.L12 = L12
        self.R11 = R11
        self.R12 = R12
        self.R21 = R21
        self.R22 = R22
        self.L21 = L21
        self.L22 = L22
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0.0, 0.0])
        self.wDir = numpy.array([0.0, 0.0, 1.0])
        self.vDir = self.wDir * self.uDir
        # self.compute_params(VDir=True)
        self.compute_params()


    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        # self.compute_params(VDir)
        self.compute_params()

    def compute_params(self):
        # if VDir == None:
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin - (self.L / 2.0 - self.L11) * self.uDir + (self.W / 2.0) * self.vDir
        self.a2 = self.sec_origin + (self.L / 2.0 - self.R11) * self.uDir + (self.W / 2.0) * self.vDir
        self.a3 = self.sec_origin + (self.L / 2.0) * self.uDir + (self.W /2.0 - self.R12) * self.vDir
        self.a4 = self.sec_origin + (self.L / 2.0) * self.uDir - (self.W /2.0 - self.R22) * self.vDir
        self.a5 = self.sec_origin + (self.L / 2.0 - self.R21) * self.uDir - (self.W / 2.0) * self.vDir
        self.a6 = self.sec_origin - (self.L / 2.0 - self.L21) * self.uDir - (self.W / 2.0) * self.vDir
        self.a7 = self.sec_origin - (self.L / 2.0) * self.uDir - (self.W / 2.0 - self.L22) * self.vDir
        self.a8 = self.sec_origin - (self.L / 2.0) * self.uDir + (self.W / 2.0 - self.L12) * self.vDir
        self.points = [self.a1, self.a2, self.a3, self.a4,self.a5, self.a6, self.a7, self.a8]
        # else:
        #     # self.vDir = numpy.cross(self.wDir, self.uDir)
        #     self.a1 = self.sec_origin - (self.L / 2.0 - self.L11) * self.uDir + (self.W / 2.0)*self.wDir
        #     self.a2 = self.sec_origin + (self.L / 2.0 - self.R11) * self.uDir + (self.W / 2.0)*self.wDir
        #     self.a3 = self.sec_origin + (self.L / 2.0) * self.uDir + (self.W / 2.0 - self.R12)*self.wDir
        #     self.a4 = self.sec_origin + (self.L / 2.0) * self.uDir - (self.W / 2.0 - self.R22)*self.wDir
        #     self.a5 = self.sec_origin + (self.L / 2.0 - self.R21) * self.uDir - (self.W / 2.0)*self.wDir
        #     self.a6 = self.sec_origin - (self.L / 2.0 - self.L21) * self.uDir - (self.W / 2.0)*self.wDir
        #     self.a7 = self.sec_origin - (self.L / 2.0) * self.uDir - (self.W / 2.0 - self.L22)*self.wDir
        #     self.a8 = self.sec_origin - (self.L / 2.0) * self.uDir + (self.W / 2.0 - self.L12)*self.wDir
        #     self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8]


    def create_model(self, rotate_angle=None):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * self.wDir  # extrudeDir is a numpy array
        if rotate_angle == None:
            prism1 = makePrismFromFace(aFace, extrudeDir)
        else:
            prism = makePrismFromFace(aFace, extrudeDir)
            trns = gp_Trsf()
            # axis = numpy.array([1.0, 0.0, 0.0])
            angle = radians(rotate_angle)
            trns.SetRotation(gp_OX(), angle)
            brep_trns = BRepBuilderAPI_Transform(prism, trns, False)
            brep_trns.Build()
            prism1 = brep_trns.Shape()

        return prism1

if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()
    
    L = 10
    W = 10
    T = 1

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    SPlate = StiffenerPlate(L, W, T)
    _place = SPlate.place(origin, uDir, wDir)
    point = SPlate.compute_params()
    prism = SPlate.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()