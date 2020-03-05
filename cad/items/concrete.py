'''
Created on 29-Nov-2014

@author: deepa
@author: deepa
'''
import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


class Plate(object):
    '''

                                    a2   XX-------------------------+
                                         |X                          X
                                         | X                          X
                                         |  X                          X
                                         |   X--------------------------X
                                         |   |                          |
+-------------->                         |   |  a1                      |
|               w dir                    |   |                          |
|                                        |   |                          |
|                                        |   |    +---------->  gDir    |
|                                        |   |    |                     |
|                                        |   |    |                     |
|                                        |   |    |                     |
|                                        |   |    |                     |
v                                        |   |    |                     |
                                         |   |    v                     |
v dir                                    |   |                          |
                                         |   |    pDir                  |
                                         |   |                          |
                                         |   |                          |
                                         |   |                          |
                                         |   |                          |
                                    a3   X   |                          |
                                          X  |                          |
                                            X+--------------------------+

                                             a4

    '''

    def __init__(self, L, W, T):
        self.L = L
        self.W = W
        self.T = T
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin - self.L/2*self.uDir
        self.a2 = self.a1 - self.T/2*self.wDir
        self.a3 = self.a2 - self.W/2*self.vDir

    def create_model(self):
        prism = BRepPrimAPI_MakeBox(getGpPt(self.a3), self.L, self.W, self.T).Shape()

        return prism


L = 10
T = 5
W = 10

origin = numpy.array([0.,0.,0.])
uDir = numpy.array([1.,0.,0.])
shaftDir = numpy.array([0.,0.,1.])

channel = Plate(L, W, T)
angles = channel.place(origin, uDir, shaftDir)
point = channel.compute_params()
prism = channel.create_model()
display.DisplayShape(prism, update=True)
display.DisableAntiAliasing()
start_display()