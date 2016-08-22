'''
Created on 27-May-2015

@author: deepa
'''
import numpy
from ModelUtils import *
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse

class FilletWeld(object):
    
    def __init__(self,b,h,L):        
        self.L = L
        self.b = b
        self.h = h
        self.secOrigin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.computeParams()
    
    def place(self, secOrigin, uDir, wDir):
        self.secOrigin = secOrigin
        self.uDir = uDir
        self.wDir = wDir        
        self.computeParams()
        
    def computeParams(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.secOrigin 
        self.a2 = self.secOrigin + self.b * self.uDir
        self.a3 = self.secOrigin + self.h * self.vDir
        self.points = [self.a1, self.a2, self.a3,]
       
        
    def createModel(self):
        Pnt = getGpPt(self.secOrigin)
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.L * (self.wDir) # extrudeDir is a numpy array
        prism =  makePrismFromFace(aFace, extrudeDir)
        my_sphere = BRepPrimAPI_MakeSphere(Pnt,5.0).Shape()
        spherebody = BRepAlgoAPI_Fuse(prism, my_sphere).Shape()
        return prism