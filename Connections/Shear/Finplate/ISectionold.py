'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from ModelUtils import *


class ISection(object):
    '''
                              ^ v
                              |                     
            c2                .                c1                            
     ---    +-----------------|-----------------+     ---
      ^     |                 .                 |      ^
      | T   |                 |                 |      |
      v     |                 .                 |      |  
     ---    +------------+    |    +------------+      |
            b2         a2|         | a1         b1     |
                         |    t    |                   |
                         |<------->|                   |
                         |    |    |                   |
                         |    .    |                   |D
                         |    |O   |                   |
    -- -- -- -- -- -- -- -- --.-- -- -- -- -- -- -- -- |-- -- -> u
                         |    |    |                   |
                         |    .    |                   |
                         |    |    |                   |
                         |    .    |                   |
             b3        a3|    |    |a4          b4     |
             +-----------+    .    +------------+      |
             |                |                 |      |
             |                .                 |      |
             |                |                 |      v
             +----------------.-----------------+     ---
             c3               B                 c4       
             |<-------------------------------->| 
                                                    
    '''  
    def __init__(self, B, T, D, t, R1, R2, alpha, length):        
        self.B = B
        self.T = T 
        self.D = D
        self.t = t
        self.R1 = R1
        self.R2 = R2
        self.alpha = alpha
        self.length = length
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
        self.a1 = self.secOrigin + (self.t / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.b1 = self.secOrigin + (self.B / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir   
        self.c1 = self.secOrigin + (self.B / 2.0) * self.uDir + (self.D / 2.0) * self.vDir
        self.a2 = self.secOrigin + (-self.t / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.b2 = self.secOrigin + (-self.B / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir   
        self.c2 = self.secOrigin + (-self.B / 2.0) * self.uDir + (self.D / 2.0) * self.vDir
        self.a3 = self.secOrigin + (-self.t / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.b3 = self.secOrigin + (-self.B / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir   
        self.c3 = self.secOrigin + (-self.B / 2.0) * self.uDir + -(self.D / 2.0) * self.vDir
        self.a4 = self.secOrigin + (self.t / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.b4 = self.secOrigin + (self.B / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir   
        self.c4 = self.secOrigin + (self.B / 2.0) * self.uDir + -(self.D / 2.0) * self.vDir
        self.points = [self.a1, self.b1, self.c1,
                       self.c2, self.b2, self.a2,
                       self.a3, self.b3, self.c3,
                       self.c4, self.b4, self.a4]
        # self.points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]  
        
    def createModel(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.length * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)
        
        return prism
    
        
        
