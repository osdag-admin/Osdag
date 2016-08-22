'''
Created on 14-Oct-2015

@author: jeffy
'''
from OCC.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.GC import GC_MakeArcOfCircle
from OCC.ShapeConstruct import shapeconstruct, \
    ShapeConstruct_CompBezierCurves2dToBSplineCurve2d
from OCC.TopExp import TopExp_Explorer
from OCC.TopoDS import topods
from OCC._TopAbs import TopAbs_EDGE
import math
import numpy

from ModelUtils import *


class Angle(object):
    
    def __init__(self,L, A, B, T, R1, R2):        
        self.L = L
        self.A = A
        self.B = B 
        self.T = T
        self.R1 = R1
        self.R2 = R2
        self.secOrigin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.computeParams()
    
    def place(self, secOrigin, uDir, wDir):
        self.secOrigin = secOrigin
        self.uDir = uDir
        self.wDir = wDir        
        self.computeParams()
        
    def computeParams(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        root2 = math.sqrt(2)
        self.a1 = self.secOrigin
        self.a2 = self.secOrigin + self.A * self.vDir
        self.a3 = self.secOrigin + (self.T - self.R2)* self.uDir + self.A * self.vDir 
        self.a4 = self.secOrigin + (self.T - self.R2 + self.R2/root2)* self.uDir + (self.A - self.R2 + self.R2/root2) * self.vDir 
        self.a5 = self.secOrigin + (self.T)* self.uDir + (self.A - self.R2) * self.vDir 
        self.a6 = self.secOrigin + (self.T)* self.uDir + (self.T + self.R1) * self.vDir 
        self.a7 = self.secOrigin + (self.T + self.R1 - self.R1/root2)* self.uDir + (self.T + self.R1 - self.R1/root2) * self.vDir 
        self.a8 = self.secOrigin + (self.T + self.R1)* self.uDir + self.T * self.vDir 
        self.a9 = self.secOrigin + (self.B - self.R2)* self.uDir + self.T * self.vDir 
        self.a10 = self.secOrigin + (self.B - self.R2 + self.R2/root2)* self.uDir + (self.T - self.R2 + self.R2/root2) * self.vDir 
        self.a11 = self.secOrigin + (self.B)* self.uDir + (self.T - self.R2) * self.vDir 
        self.a12 = self.secOrigin + self.B * self.uDir
        
#         self.a1 = self.secOrigin + (self.T/2.0) * self.uDir + (self.B/2.0) * self.vDir
#         self.a2 = self.secOrigin + (-self.T/2.0) * self.uDir + (self.B/2.0) * self.vDir 
#         self.a3 = self.secOrigin + (-self.T/2.0) * self.uDir + ((-self.B/2.0)-self.T) * self.vDir
#         self.a4 = self.secOrigin + ((self.T/2.0)+self.A) * self.uDir + ((-self.B/2.0)-self.T) * self.vDir
#         self.a5 = self.secOrigin + ((self.T/2.0)+self.A) * self.uDir + (-self.B/2.0) * self.vDir
#         self.a6 = self.secOrigin + (self.T/2.0) * self.uDir + (-self.B/2.0) * self.vDir
#         

        
        
#         ShapeConstruct_CompBezierCurves2dToBSplineCurve2d()
        
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9, self.a10, self.a11, self.a12]
       
        
    def createModel(self):
#         edges = makeEdgesFromPoints(self.points)
#         self.a1 = 
        edge1 = BRepBuilderAPI_MakeEdge(getGpPt(self.a1),getGpPt(self.a2))
        edge2 = BRepBuilderAPI_MakeEdge(getGpPt(self.a2),getGpPt(self.a3))
        arc1 = GC_MakeArcOfCircle(getGpPt(self.a3),getGpPt(self.a4),getGpPt(self.a5))
        edge3 = BRepBuilderAPI_MakeEdge(arc1.Value())
        edge4 = BRepBuilderAPI_MakeEdge(getGpPt(self.a5),getGpPt(self.a6))
        arc2 = GC_MakeArcOfCircle(getGpPt(self.a6),getGpPt(self.a7),getGpPt(self.a8))
        edge5 = BRepBuilderAPI_MakeEdge(arc2.Value())
        edge6 = BRepBuilderAPI_MakeEdge(getGpPt(self.a8),getGpPt(self.a9))
        arc3 = GC_MakeArcOfCircle(getGpPt(self.a9),getGpPt(self.a10),getGpPt(self.a11))
        edge7 = BRepBuilderAPI_MakeEdge(arc3.Value())
        edge8 = BRepBuilderAPI_MakeEdge(getGpPt(self.a11),getGpPt(self.a12))
        edge9 = BRepBuilderAPI_MakeEdge(getGpPt(self.a12),getGpPt(self.a1))
#         wire = makeWireFromEdges(edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9)
        wire = BRepBuilderAPI_MakeWire(edge1.Edge(),edge2.Edge(),edge3.Edge(),edge4.Edge())
        wire = BRepBuilderAPI_MakeWire(wire.Wire(),edge5.Edge())
        wire = BRepBuilderAPI_MakeWire(wire.Wire(),edge6.Edge())
        wire = BRepBuilderAPI_MakeWire(wire.Wire(),edge7.Edge())
        wire = BRepBuilderAPI_MakeWire(wire.Wire(),edge8.Edge())
        wire = BRepBuilderAPI_MakeWire(wire.Wire(),edge9.Edge())
        
        aFace = makeFaceFromWire(wire.Wire())
        extrudeDir = self.L * self.wDir # extrudeDir is a numpy array
        
        prism =  makePrismFromFace(aFace, extrudeDir)
        mkFillet = BRepFilletAPI_MakeFillet(prism)
        anEdgeExplorer = TopExp_Explorer(prism, TopAbs_EDGE)
        while anEdgeExplorer.More():
            aEdge = topods.Edge(anEdgeExplorer.Current())
            mkFillet.Add(self.T / 17. , aEdge)
            anEdgeExplorer.Next()
                
        prism = mkFillet.Shape()
        
        return prism
    
            