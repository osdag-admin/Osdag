
'''
Created on 14-Oct-2015

@author: Deepa
'''
import numpy
import math
from OCC.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.GC import GC_MakeArcOfCircle
from OCC.TopExp import TopExp_Explorer
from OCC.TopoDS import topods
from OCC.TopAbs import TopAbs_EDGE
from ModelUtils import getGpPt, make_edge, makeWireFromEdges, \
    makeFaceFromWire, makePrismFromFace,makeEdgesFromPoints

"""
    +
    |   a2  XXXXXXXXXX    a4
    |       X          X
    |       X           X   a5
    |       X           X
    |       X           X
    |       X           X
    |       X           X
    |       X           X
    |       X           X
    |       X           X
    |       X           X
    |       X           X              Angle Geometry
A   |       X           X
    |       X           X
    |       X           X
    |       X           X  a6
    |       X            X                                  a9
    |       X             X    a8
    |       X         a7   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     a10
    |       X                                                X
    |       X                                                 X    a11
    |       X                                                 X
    |       X                                                 X
    v       X                                                 X
       a1   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    a12

            +-------------------------------------------------->

                                          B


"""

'''
Created on 14-Oct-2015
@author: Deepa
'''
import numpy
import math
from OCC.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.GC import GC_MakeArcOfCircle
from OCC.TopExp import TopExp_Explorer
from OCC.TopoDS import topods
from OCC.TopAbs import TopAbs_EDGE
from ModelUtils import getGpPt, make_edge, makeWireFromEdges, \
    makeFaceFromWire, makePrismFromFace


class Angle(object):
    def __init__(self, L, A, B, T, R1, R2):
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
        self.a3 = self.sec_origin + (self.T - self.R2) * self.uDir + self.A * self.vDir
        self.a4 = self.sec_origin + (self.T - self.R2 + self.R2 / root2) * self.uDir + (
                                                                                      self.A - self.R2 + self.R2 / root2) * self.vDir
        self.a5 = self.sec_origin + (self.T) * self.uDir + (self.A - self.R2) * self.vDir
        self.a6 = self.sec_origin + (self.T) * self.uDir + (self.T + self.R1) * self.vDir
        self.a7 = self.sec_origin + (self.T + self.R1 - self.R1 / root2) * self.uDir + (
                                                                                      self.T + self.R1 - self.R1 / root2) * self.vDir
        self.a8 = self.sec_origin + (self.T + self.R1) * self.uDir + self.T * self.vDir
        self.a9 = self.sec_origin + (self.B - self.R2) * self.uDir + self.T * self.vDir
        self.a10 = self.sec_origin + (self.B - self.R2 + self.R2 / root2) * self.uDir + (
                                                                                       self.T - self.R2 + self.R2 / root2) * self.vDir
        self.a11 = self.sec_origin + (self.B) * self.uDir + (self.T - self.R2) * self.vDir
        self.a12 = self.sec_origin + self.B * self.uDir

        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9, self.a10,
                      self.a11, self.a12]

    def create_model(self):

        ######################################################
        edges = []
        if self.R2 == 0.0 or self.R1 == 0.0:
            self.a3 = self.a4 = self.a5
            edge1 = make_edge(getGpPt(self.a1), getGpPt(self.a2))
            edges.append(edge1)
            edge2 = make_edge(getGpPt(self.a2), getGpPt(self.a3))
            edges.append(edge2)
            edge3 = make_edge(getGpPt(self.a3), getGpPt(self.a6))
            edges.append(edge3)
            # arc2 = GC_MakeArcOfCircle(getGpPt(self.a6), getGpPt(self.a7), getGpPt(self.a8))
            # edge4 = make_edge(arc2.Value())
            # edges.append(edge4)
            # edge5 = make_edge(getGpPt(self.a8), getGpPt(self.a9))
            # edges.append(edge5)
            # edge6 = make_edge(getGpPt(self.a9), getGpPt(self.a12))
            # edges.append(edge6)
            # edge7 = make_edge(getGpPt(self.a12), getGpPt(self.a1))
            # edges.append(edge7)
            edge4 = make_edge(getGpPt(self.a6), getGpPt(self.a9))
            edges.append(edge4)
            edge5 = make_edge(getGpPt(self.a9), getGpPt(self.a12))
            edges.append(edge5)
            edge6 = make_edge(getGpPt(self.a12), getGpPt(self.a1))
            edges.append(edge6)

        else:
            edge1 = make_edge(getGpPt(self.a1), getGpPt(self.a2))
            edges.append(edge1)
            edge2 = make_edge(getGpPt(self.a2), getGpPt(self.a3))
            edges.append(edge2)
            arc1 = GC_MakeArcOfCircle(getGpPt(self.a3), getGpPt(self.a4), getGpPt(self.a5))
            edge3 = make_edge(arc1.Value())
            edges.append(edge3)
            edge4 = make_edge(getGpPt(self.a5), getGpPt(self.a6))
            edges.append(edge4)
            arc2 = GC_MakeArcOfCircle(getGpPt(self.a6), getGpPt(self.a7), getGpPt(self.a8))
            edge5 = make_edge(arc2.Value())
            edges.append(edge5)
            edge6 = make_edge(getGpPt(self.a8), getGpPt(self.a9))
            edges.append(edge6)
            arc3 = GC_MakeArcOfCircle(getGpPt(self.a9), getGpPt(self.a10), getGpPt(self.a11))
            edge7 = make_edge(arc3.Value())
            edges.append(edge7)
            edge8 = make_edge(getGpPt(self.a11), getGpPt(self.a12))
            edges.append(edge8)
            edge9 = make_edge(getGpPt(self.a12), getGpPt(self.a1))
            edges.append(edge9)

        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.L * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)
        mkFillet = BRepFilletAPI_MakeFillet(prism)
        anEdgeExplorer = TopExp_Explorer(prism, TopAbs_EDGE)
        while anEdgeExplorer.More():
            aEdge = topods.Edge(anEdgeExplorer.Current())
            mkFillet.Add(self.T / 17., aEdge)
            anEdgeExplorer.Next()

        prism = mkFillet.Shape()
        return prism