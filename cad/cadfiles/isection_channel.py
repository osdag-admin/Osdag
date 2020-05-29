import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.channel import Channel
from cad.items.plate import Plate
from cad.items.ISection import ISection

class ISectionChannel(object):

    def __init__(self, B, T, D, t, R1, R2, L, l, W, H, b, d):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.R1 = R1
        self.R2 = R2
        self.L = L
        self.l = l
        self.W = W
        self.H = H
        self.d = d
        self.clearDist = 20
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.channel1 = Channel(B, t, D, t, 0, 0, L)
        self.isection = ISection(b, T, d, T, R1, R2, 0, L, None)
        #self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        d = self.d/2 
        origin = numpy.array([-d+self.B-self.t,0.,0.])
        self.channel1.place(origin , self.uDir, self.wDir)
        origin1 = numpy.array([self.D/2.,0.,0.])
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
    L = 100
    l = 4
    W = 100
    H = 60
    b = 25
    d = 50

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    isection_channel = ISectionChannel(B, T, D, t, 0, 0, L, l, W, H, b, d)
    _place = isection_channel.place(origin, uDir, shaftDir)
    point = isection_channel.compute_params()
    prism = isection_channel.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
