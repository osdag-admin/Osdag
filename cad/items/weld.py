'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from cad.items.ModelUtils import *

'''

                                 X--------------X
                               X              X |
                             X              X   |
                    ^   a2 +--------------+     |
                    |      |              | a1  |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    +      |              |     |
                    L      |              |     |
                    +      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     |
                    |      |              |     X
                    |      |              |   X
                    |      |              | X
                    v      +--------------+
                        a3                  a4

                           <------ W ----->


'''

class Weld(object):
    
    def __init__(self, L, W, T):        
        self.L = L
        self.W = W 
        self.T = T
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.compute_params()
    
    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir        
        self.compute_params()
        
    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin + (self.W / 2.0) * self.uDir + (self.L / 2.0) * self.vDir
        self.a2 = self.sec_origin + (-self.W / 2.0) * self.uDir + (self.L / 2.0) * self.vDir 
        self.a3 = self.sec_origin + (-self.W / 2.0) * self.uDir + (-self.L / 2.0) * self.vDir
        self.a4 = self.sec_origin + (self.W / 2.0) * self.uDir + (-self.L / 2.0) * self.vDir
        self.points = [self.a1, self.a2, self.a3, self.a4]
       
        
    def create_model(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)
        
        return prism
    
            
if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    L = 20
    W = 3
    T = 2

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    weld = Weld(L, W, T)
    _place = weld.place(origin, uDir, wDir)
    point = weld.compute_params()
    prism = weld.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()