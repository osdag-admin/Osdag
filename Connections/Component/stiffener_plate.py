'''
Created on 16-May-2019

@author: Anand Swaroop
@author: Anand Swaroop
'''
import numpy
from ModelUtils import *


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
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
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

    def create_model(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)

        return prism
