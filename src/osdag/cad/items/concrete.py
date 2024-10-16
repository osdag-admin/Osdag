'''
Created on 29-March-2020

@author: Anand Swaroop
'''
import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeWedge
from OCC.Core.gp import gp_Dir, gp_Circ, gp_Ax2, gp_Ax1
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse


# from OCC.Core.gp import gp_Ax1


class Concrete(object):
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
        self.uDir = None  # numpy.array([1.0, 0, 0])
        self.wDir = None  # numpy.array([0.0, 0, 1.0])
        # self.vDir = self.wDir * self.uDir
        # self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.wedge_base = self.T
        self.wedge_height = self.T
        self.box_length = self.L - 2 * self.wedge_base
        self.box_width = self.W - 2 * self.wedge_base

        # adjusting origin to the center of the box
        self.a1 = self.sec_origin - (self.L) / 2 * self.uDir
        # self.a1 = self.sec_origin - (self.L - 2 * self.wedge_base) / 2 * self.uDir
        self.a2 = self.a1 - self.T / 2 * self.wDir
        self.a3 = self.a2 - (self.W) / 2 * self.vDir  # origin of box
        # self.a3 = self.a2 - (self.W - 2 * self.wedge_base) / 2 * self.vDir  # origin of box

        # creating for corneres of the grout
        self.p0 = self.sec_origin - self.T / 2 * self.wDir
        self.p1 = self.p0 + self.L / 2 * self.uDir + self.W / 2 * self.vDir
        self.p2 = self.p1 - self.W * self.vDir
        self.p3 = self.p2 - self.L * self.uDir
        self.p4 = self.p3 + self.W * self.vDir

    def create_model(self):
        # box = BRepPrimAPI_MakeBox(getGpPt(self.a3), self.box_width, self.box_length, self.wedge_height).Shape()
        # wedge1_w = BRepPrimAPI_MakeWedge(gp_Ax2(getGpPt(self.p2- self.wedge_base*self.uDir), getGpDir(numpy.array([0.0, 1.0, 0.0]))), self.wedge_height,self.wedge_base,self.W, 0.001).Shape()
        # prism = BRepAlgoAPI_Fuse(box, wedge1_w).Shape()
        #
        # wedge2_w = BRepPrimAPI_MakeWedge(gp_Ax2(getGpPt(self.p3), getGpDir(numpy.array([0.0, 1.0, 0.0]))), 0.001,self.wedge_base,self.W, self.wedge_height).Shape()
        # prism = BRepAlgoAPI_Fuse(prism, wedge2_w).Shape()

        box = BRepPrimAPI_MakeBox(getGpPt(self.a3), self.L, self.W, self.T).Shape()
        prism = box
        return prism


if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()
    from OCC.gp import gp_Pnt

    L = 500
    T = 5
    W = 300

    origin = numpy.array([0., 0., 0.])
    uDir = numpy.array([1., 0., 0.])
    shaftDir = numpy.array([0., 0., 1.])

    channel = Concrete(L, W, T)
    angles = channel.place(origin, uDir, shaftDir)
    point = channel.compute_params()
    prism = channel.create_model()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
