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
        self.channel1.points = self.rotateZ(self.channel1.points)
        self.isection.compute_params()
        # self.isection.points = self.rotateZ(self.isection.points)

    def create_model(self):
        prism1 = self.channel1.create_model()
        prism3 = self.isection.create_model()

        prism = BRepAlgoAPI_Fuse(prism1, prism3).Shape()
        return prism

    def rotateZ(self, points):
        rotated_points = []
        rmatrix = numpy.array([[0, 1, 0],[-1, 0, 0],[0, 0, 1]]) 
        for point in points:
            point = numpy.matmul(rmatrix, point)
            rotated_points.append(point)
        return rotated_points

    def create_marking(self):
        middel_pnt = []
        line = []
        labels = ["z","y","u","v"]
        offset = self.D
        uvoffset = offset/numpy.sqrt(2)

        x = self.B/2 + self.T1
        z_points = [numpy.array([-offset+x,0,self.H/2]), numpy.array([offset+x,0,self.H/2])]
        line.append(makeEdgesFromPoints(z_points))

        y_points = [numpy.array([x,-offset,self.H/2]), numpy.array([x,offset,self.H/2])]
        line.append(makeEdgesFromPoints(y_points))
        
        u_points = [numpy.array([-uvoffset+x,uvoffset,self.H/2]), numpy.array([uvoffset+x,-uvoffset,self.H/2])]
        line.append(makeEdgesFromPoints(u_points))

        v_points = [numpy.array([-uvoffset+x,-uvoffset,self.H/2]), numpy.array([uvoffset+x,uvoffset,self.H/2])]
        line.append(makeEdgesFromPoints(v_points))

        start_pnt = [[-offset+x,0,self.H/2],[x,-offset+1,self.H/2],[uvoffset+x,-uvoffset,self.H/2],[uvoffset+x,uvoffset,self.H/2]]
        end_pnt = [[offset+x,0,self.H/2],[x,offset-2,self.H/2],[-uvoffset+x,uvoffset,self.H/2],[-uvoffset+x,-uvoffset,self.H/2]]

        return line, [start_pnt, end_pnt], labels

if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    def display_lines(lines, points, labels):
        for l,p1,p2,n in zip(lines,points[0],points[1], labels):
            display.DisplayShape(l, update=True)
            display.DisplayMessage(getGpPt(p1), n, height=24,message_color=(0,0,0))
            display.DisplayMessage(getGpPt(p2), n, height=24,message_color=(0,0,0))
    
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
    lines, pnts, labels = isection_channel.create_marking()
    display.DisplayShape(prism, update=True)
    display_lines(lines, pnts, labels)
    display.View_Top()
    display.FitAll()
    display.DisableAntiAliasing()
    start_display()
