
import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
#from notch import Notch
from cad.items.plate import Plate
from cad.items.ISection import ISection

class cross_isection(object):

    def __init__(self, B, T, D, t, R1, R2, alpha, length):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.R1 = R1
        self.R2 = R2
        self.alpha = alpha
        self.length = length
        self.clearDist = 20
        self.Isection1 = ISection(B, T, D, t, R1, R2, alpha, length, None)
        self.Isection2 = ISection(B, T, D, t, R1, R2, alpha, length, None)
    
        
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

    B = 45
    T = 3
    D = 50
    t = 2
    R1 = 5
    R2 = 5
    alpha = 1
    length = 100
#    width = 10
#    hight = 10
#    d = 10
#    L = 3
#    W = 200
#    H = 90
    
    ISecPlate = cross_isection(B, T, D, t, R1, R2, alpha, length)

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    #iseccover = IsectionCoverPlate(Isec1, Isec2, plate1, plate2)
    ISecPlate.place(origin, uDir, shaftDir)
    ISecPlate.compute_params()
    prism = ISecPlate.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
    #print(prism.Orientation())