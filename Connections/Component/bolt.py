'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from ModelUtils import getGpPt, getGpDir, makeEdgesFromPoints, makeWireFromEdges, makePrismFromFace, makeFaceFromWire
import math
from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.gp import gp_Ax2
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse


class Bolt(object):
    '''

        a3  X-------------------+  a2
           X                   X|X
          X                   X | X
         X                   X  |  X
        X                   X   |   X
       X                   X    |    X
      X                   X     |     X
     X                   X 60   |      X
a4  X                   XXXXXXXXXXXXXXXXX  a1
     X                                 X
      X                               X
       XX                            X
        X                           X
         X                         X
          X                       X
           X                     X
            X-------------------X
                                   a6
            a5


    '''

    def __init__(self, R, T, H, r):
        self.R = R
        self.H = H
        self.T = T
        self.r = r
        self.origin = None
        self.uDir = None
        self.shaftDir = None
        self.vDir = None
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.a4 = None
        self.a5 = None
        self.a6 = None
        self.points = []

    def place(self, origin, uDir, shaftDir):
        self.origin = origin
        self.uDir = uDir
        self.shaftDir = shaftDir
        self.compute_params()

    def getPoint(self, theta):
        theta = math.radians(theta)
        point = self.origin + (self.R * math.cos(theta)) * self.uDir + (self.R * math.sin(theta)) * self.vDir 
        return point

    def compute_params(self):
        self.vDir = numpy.cross(self.shaftDir, self.uDir)
        self.a1 = self.getPoint(0)
        self.a2 = self.getPoint(60)
        self.a3 = self.getPoint(120)
        self.a4 = self.getPoint(180)
        self.a5 = self.getPoint(240)
        self.a6 = self.getPoint(300)
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]

    def create_model(self):

        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = -self.T * self.shaftDir  # extrudeDir is a numpy array
        boltHead = makePrismFromFace(aFace, extrudeDir)
        cylOrigin = self.origin
        boltCylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(cylOrigin), getGpDir(self.shaftDir)), self.r, self.H).Shape()

        whole_Bolt = BRepAlgoAPI_Fuse(boltHead, boltCylinder).Shape()

        return whole_Bolt
