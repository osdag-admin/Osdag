import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.channel import Channel
from cad.items.plate import Plate
from cad.items.ISection import ISection

class ISectionChannel(object):

    def __init__(self, D, B, T, t, T1, t1, d, b, H, s):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.T1 = T1
        self.t1 = t1
        self.d = d
        self.b = b
        self.H = H
        self.s = s
        self.B = 2*self.s-2*T1
        self.d = 2*self.s

        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        
        self.channel1 = Channel(b, T1, self.d, t1, 0, 0, H)
        self.isection = ISection(self.B, T, D, t, 0, 0, 0, H, None)
        #self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        D = self.D/2 
        origin = numpy.array([-D+self.b-self.t1,0.,0.])
        self.channel1.place(origin , self.uDir, self.wDir)
        origin1 = numpy.array([self.s,0.,0.])
        self.isection.place(origin1, self.uDir, self.wDir)

    def compute_params(self):
        self.channel1.compute_params()
        self.isection.compute_params()
        self.isection.points = self.rotateZ(self.isection.points)

    def create_model(self):
        prism1 = self.channel1.create_model()
        prism3 = self.isection.create_model()

        prism = BRepAlgoAPI_Fuse(prism1, prism3).Shape()
        return prism

    def rotateZ(self, points):
        rotated_points = []
        rmatrix = numpy.array([[0, -1, 0],[1, 0, 0],[0, 0, 1]]) 
        for point in points:
            point = numpy.matmul(rmatrix, point)
            rotated_points.append(point)
        return rotated_points

if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()
    
    B = 20
    T = 2
    D = 40
    t = 1.5
    T1 = 2
    t1 = 2
    H = 60
    b = 20
    d = 50
    s = 15

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    isection_channel = ISectionChannel(D, B, T, t, T1, t1, d, b, H, s)
    print(isection_channel.B)
    _place = isection_channel.place(origin, uDir, shaftDir)
    point = isection_channel.compute_params()
    prism = isection_channel.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
