'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from cad.items.ModelUtils import getGpPt, getGpDir, makeEdgesFromPoints, makeWireFromEdges, makePrismFromFace, makeFaceFromWire
import math
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Ax2
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse


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

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    R = 8
    H = 10
    T = 5
    r = 3

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    bolt = Bolt(R, T, H, r)
    _place = bolt.place(origin, uDir, shaftDir)
    point = bolt.compute_params()
    prism = bolt.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()