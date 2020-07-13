import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.channel import Channel
from cad.items.plate import Plate

class ChannelSection(object):

    def __init__(self, D, B, T, t, s, l, t1, H):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.l = l
        self.s = s
        self.t1 = t1
        self.H = H

        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])

        self.Plate1 = Plate(t1, H, l)
        self.Plate2 = Plate(t1, H, l)
        self.channel1 = Channel(B, T, D, t, 0, 0, H)
        self.channel2 = Channel(B, T, D, t, 0, 0, H)
        #self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        space = -self.s/2+self.B-self.t
        origin = numpy.array([space,0.,0.])
        self.channel1.place(origin, self.uDir, self.wDir)
        origin1 = numpy.array([space,0.,0.])
        self.channel2.place(origin1, self.uDir, self.wDir)
        origin2 = numpy.array([0., -self.t1/2,0.])
        self.Plate1.place(origin2, self.uDir, self.wDir)
        origin3 = numpy.array([0.,self.D+self.t1/2,0.])
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
        # prism = BRepAlgoAPI_Fuse(prism, prism3).Shape()
        # prism = BRepAlgoAPI_Fuse(prism, prism4).Shape()
        return prism, [prism3, prism4]

    def rotateY(self, points):
        rotated_points = []
        rmatrix = numpy.array([[0, 0, 1],[0, 1, 0],[-1, 0, 0]]) 
        for point in points:
            point = numpy.matmul(rmatrix, point)
            rotated_points.append(point)
        return rotated_points

    def create_marking(self):
        middel_pnt = []
        line = []
        labels = ["z","y","u","v"]
        offset = self.s + self.B
        uvoffset = offset/numpy.sqrt(2)

        z_points = [numpy.array([-offset,self.D/2,self.H/2]), numpy.array([offset,self.D/2,self.H/2])]
        line.append(makeEdgesFromPoints(z_points))

        y_points = [numpy.array([0.,-offset+self.D/2,self.H/2]), numpy.array([0,offset+self.D/2,self.H/2])]
        line.append(makeEdgesFromPoints(y_points))
        
        u_points = [numpy.array([-uvoffset,uvoffset+self.D/2,self.H/2]), numpy.array([uvoffset,-uvoffset+self.D/2,self.H/2])]
        line.append(makeEdgesFromPoints(u_points))

        v_points = [numpy.array([-uvoffset,-uvoffset+self.D/2,self.H/2]), numpy.array([uvoffset,uvoffset+self.D/2,self.H/2])]
        line.append(makeEdgesFromPoints(v_points))

        start_pnt = [[-offset,self.D/2,self.H/2],[0,-offset+self.D/2+1,self.H/2],[uvoffset,-uvoffset+self.D/2,self.H/2],[uvoffset,uvoffset+self.D/2,self.H/2]]
        end_pnt = [[offset,self.D/2,self.H/2],[0,offset+self.D/2-2,self.H/2],[-uvoffset,uvoffset+self.D/2,self.H/2],[-uvoffset,-uvoffset+self.D/2,self.H/2]]

        return line, [start_pnt, end_pnt], labels

if __name__ == '__main__':
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    def display_lines(lines, points, labels):
        for l,p1,p2,n in zip(lines,points[0],points[1], labels):
            display.DisplayShape(l, update=True)
            display.DisplayMessage(getGpPt(p1), n, height=24, message_color=(0,0,0))
            display.DisplayMessage(getGpPt(p2), n, height=24, message_color=(0,0,0))
    
    B = 20
    T = 4
    D = 40
    t = 4
    t1 = 4
    s = 50
    l = s + 2*t
    H = 50

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    channel_section = ChannelSection(D, B, T, t, s, l, t1, H)
    _place = channel_section.place(origin, uDir, shaftDir)
    point = channel_section.compute_params()
    prism, prisms = channel_section.create_model()
    lines, pnts, labels = channel_section.create_marking()
    display.DisplayShape(prism, update=True)
    for p in prisms:
        display.DisplayColoredShape(p, color='BLUE', update=True)
    display_lines(lines, pnts, labels)
    display.View_Top()
    display.FitAll()
    display.DisableAntiAliasing()
    start_display()
