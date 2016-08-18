'''
Created on 14-Oct-2015

@author: aravind
'''
import numpy
from ModelUtils import *





class Angle(object):
    
    def __init__(self,L, A, B, T):        
        self.L = L
        self.A = A
        self.B = B 
        self.T = T
        self.secOrigin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.computeParams()
    
    def place(self, secOrigin, uDir, wDir):
        self.secOrigin = secOrigin
#         self.secOrigin = self.secOrigin - (self.L/2.0) * self.wDir
        self.uDir = uDir
        self.wDir = wDir        
        self.computeParams()
        
    def computeParams(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.secOrigin
        self.a2 = self.secOrigin + self.A * self.uDir 
        self.a3 = self.secOrigin + self.A * self.uDir + self.T * self.wDir
        self.a4 = self.secOrigin + self.T * self.uDir + self.T * self.wDir
        self.a5 = self.secOrigin + self.T * self.uDir + self.B * self.wDir
        self.a6 = self.secOrigin + self.B * self.wDir
#         self.a1 = self.secOrigin + (self.T/2.0) * self.uDir + (self.B/2.0) * self.vDir
#         self.a2 = self.secOrigin + (-self.T/2.0) * self.uDir + (self.B/2.0) * self.vDir 
#         self.a3 = self.secOrigin + (-self.T/2.0) * self.uDir + ((-self.B/2.0)-self.T) * self.vDir
#         self.a6 = self.secOrigin + ((self.T/2.0)+self.A) * self.uDir + ((-self.B/2.0)-self.T) * self.vDir
#         self.a5 = self.secOrigin + ((self.T/2.0)+self.A) * self.uDir + (-self.B/2.0) * self.vDir
#         self.a4 = self.secOrigin + (self.T/2.0) * self.uDir + (-self.B/2.0) * self.vDir
           
        
        
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]
       
        
    def createModel(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.L * self.vDir # extrudeDir is a numpy array
        prism =  makePrismFromFace(aFace, extrudeDir)
        
        return prism
    
            