import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.channel import Channel
from cad.items.plate import Plate

class ChannelSection(object):

    def __init__(self, B, T, D, t, R1, R2, L, l, W, H, d):
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
        self.Plate1 = Plate(l, W, H)
        self.Plate2 = Plate(l, W, H)
        self.channel1 = Channel(B, T, D, t, 0, 0, L)
        self.channel2 = Channel(B, T, D, t, 0, 0, L)
        #self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        origin = numpy.array([-self.d/2,0.,0.])
        self.channel1.place(origin, self.uDir, self.wDir)
        origin1 = numpy.array([-self.d/2,0.,0.])
        self.channel2.place(origin1, self.uDir, self.wDir)
        origin2 = numpy.array([0.,-self.l/2,0.])
        self.Plate1.place(origin2, self.uDir, self.wDir)
        origin3 = numpy.array([0.,self.D+self.l/2,0.])
        self.Plate2.place(origin3, self.uDir, self.wDir)
        #self.compute_params()

    def compute_params(self):
        self.channel1.compute_params()
        self.channel2.compute_params()
        self.channel2.points = self.rotateY(self.channel2.points)
        self.channel2.points = self.rotateY(self.channel2.points)
        self.Plate1.compute_params()
        self.Plate2.compute_params()

    def create_model(self):
        prism1 = self.channel1.create_model()
        prism2 = self.channel2.create_model()

        prism3 = self.Plate1.create_model()
        prism4 = self.Plate2.create_model()

        prism = BRepAlgoAPI_Fuse(prism1, prism2).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism3).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism4).Shape()
        return prism

    def rotateY(self, points):
        rotated_points = []
        rmatrix = numpy.array([[0, 0, 1],[0, 1, 0],[-1, 0, 0]]) 
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
    t = 2
    L = 100
    l = 4
    W = 100
    H = 60
    d = 10

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    channel_section = ChannelSection(B, T, D, t, 0, 0, L, l, W, H, d)
    _place = channel_section.place(origin, uDir, shaftDir)
    point = channel_section.compute_params()
    prism = channel_section.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
