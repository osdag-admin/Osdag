
import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
#from notch import Notch
from cad.items.plate import Plate
from cad.items.ISection import ISection

class cross_isection(object):

    def __init__(self, D, B, T, t, H, s, d):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.H = H
        self.s = s
        self.d = d

        self.Isection1 = ISection(2*s+t+2*T, T, 2*d+2*T+t, t, 0, 0, None, H, None)
        self.Isection2 = ISection(2*d+t, T, 2*s+t+2*T, t, 0, 0, None, H, None)
    
        
    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        
        self.Isection1.place(self.sec_origin, self.uDir, self.wDir)
        self.Isection2.place(self.sec_origin, self.uDir, self.wDir)

    def compute_params(self):
        self.Isection1.compute_params()
        self.Isection2.compute_params()
        self.Isection2.points = self.retate(self.Isection2.points)
        

    def create_model(self):
        
        prism1 = self.Isection1.create_model()
        prism2 = self.Isection2.create_model()
        
        prism = BRepAlgoAPI_Fuse(prism1, prism2).Shape()
        return prism

    def retate(self, points):
        rotated_points = []
        rmatrix = numpy.array([[0, -1, 0],[1, 0, 0],[0, 0, 1]]) 
        for point in points:
            point = numpy.matmul(rmatrix, point)
            rotated_points.append(point)
        return rotated_points

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    B = 50
    T = 3
    D = 70
    t = 2
    H = 100
    d = (B - 2*T - t)/2
    s = (D - t)/2
    
    CrossISec = cross_isection(D, B, T, t, H, s, d)

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    CrossISec.place(origin, uDir, shaftDir)
    CrossISec.compute_params()
    prism = CrossISec.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()