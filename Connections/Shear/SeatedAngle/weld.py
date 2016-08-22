'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from ModelUtils import *

class Weld(object):
    
    def __init__(self,L, W, T):        
        self.L = L
        self.W = W 
        self.T = T
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
        self.a1 = self.secOrigin + (self.W/2.0) * self.uDir + (self.L/2.0) * self.vDir
        self.a2 = self.secOrigin + (-self.W/2.0) * self.uDir + (self.L/2.0) * self.vDir 
        self.a3 = self.secOrigin + (-self.W/2.0) * self.uDir + (-self.L/2.0) * self.vDir
        self.a4 = self.secOrigin + (self.W/2.0) * self.uDir + (-self.L/2.0) * self.vDir
        self.points = [self.a1, self.a2, self.a3, self.a4]
       
        
    def createModel(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * self.wDir # extrudeDir is a numpy array
        prism =  makePrismFromFace(aFace, extrudeDir)
        
        return prism
    
            