import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
#from notch import Notch
from cad.items.plate import Plate
from cad.items.ISection import ISection

class IsectionCoverPlate(object):

    def __init__(self, B, T, D, t, length, d, t2, W=None, R1=0, R2=0, alpha=0):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.R1 = R1
        self.R2 = R2
        self.alpha = alpha
        self.length = length
        self.d = d
        self.t2 = t2
        if W is None:
            self.W = 2*B+d
        else:
            self.W = W
        self.clearDist = 20
        self.Isection1 = ISection(B, T, D, t, R1, R2, alpha, length, None)
        self.Isection2 = ISection(B, T, D, t, R1, R2, alpha, length, None)
        self.Plate1 = Plate(t2, length, self.W)
        self.Plate2 = Plate(t2, length, self.W)
        
    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        
        self.Isection1.place(self.sec_origin, self.uDir, self.wDir)
        origin = numpy.array([self.B+self.d,0.,0.])
        self.Isection2.place(origin, self.uDir, self.wDir)
        origin2 = numpy.array([(self.B+self.d)/2,(self.D+self.t2)/2,0.])
        self.Plate1.place(origin2, self.uDir, self.wDir)
        origin3 = numpy.array([(self.B+self.d)/2,-(self.D+self.t2)/2,0.])
        self.Plate2.place(origin3, self.uDir, self.wDir)
        #self.compute_params()

    def compute_params():
        self.Isection1.compute_params()
        self.Isection2.compute_params()
        self.Plate1.compute_params()
        self.Plate2.compute_params()

    def create_model(self):
        
        prism1 = self.Isection1.create_model()
        prism2 = self.Isection2.create_model()

        prism3 = self.Plate1.create_model()
        prism4 = self.Plate2.create_model()
        
        prism = BRepAlgoAPI_Fuse(prism1, prism2).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism3).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism4).Shape()
        return prism

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    B = 40
    T = 3
    D = 40
    t = 3
    R1 = 5
    R2 = 5
    alpha = 1
    length = 100
    d = 10
    t2 = 3
    W = 100
    
    ISecPlate = IsectionCoverPlate(B, T, D, t, length, d, t2)

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    ISecPlate.place(origin, uDir, shaftDir)
    prism = ISecPlate.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()