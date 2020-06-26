import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.angle import Angle
from cad.items.plate import Plate

class Box(object):
    def __init__(self, L, B, H, T):
        self.L = L
        self.B = B
        self.H = H
        self.T = T
        
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        
        self.plate1 = Plate(B, H, T)
        self.plate2 = Plate(T, H, L)
        self.plate3 = Plate(B, H, T)
        self.plate4 = Plate(T, H, L)

    def place(self, secOrigin, uDir, wDir):
        self.sec_origin = secOrigin
        self.uDir = uDir
        self.wDir = wDir
    
        origin5 = numpy.array([-self.L//2, self.T/2, 0.])
        self.plate1.place(origin5, self.uDir, self.wDir)
        origin6 = numpy.array([-self.T/2, -self.B//2., 0.])
        self.plate2.place(origin6, self.uDir, self.wDir)
        origin7 = numpy.array([self.L//2., -self.T/2, 0.])
        self.plate3.place(origin7, self.uDir, self.wDir)
        origin8 = numpy.array([self.T/2, self.B//2., 0.])
        self.plate4.place(origin8, self.uDir, self.wDir)

    def compute_params(self):
        self.plate1.compute_params()
        self.plate2.compute_params()
        self.plate3.compute_params()
        self.plate4.compute_params()

    def create_model(self):
        prism1 = self.plate1.create_model()
        prism2 = self.plate2.create_model()
        prism3 = self.plate3.create_model()
        prism4 = self.plate4.create_model()

        prism = BRepAlgoAPI_Fuse(prism1, prism2).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism3).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism4).Shape()        
        return prism




if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    L = 50
    B = 30
    H = 50
    T = 2

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    box = Box(L, B, H, T)
    _place = box.place(origin, uDir, wDir)
    point = box.compute_params()
    prism = box.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()    