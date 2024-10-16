
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

    def create_marking(self):
        middel_pnt = []
        line = []
        labels = ["z","y","u","v"]
        offset = self.D
        uvoffset = offset/numpy.sqrt(2)

        z_points = [numpy.array([-offset,0.,self.H/2]), numpy.array([offset,0.,self.H/2])]
        line.append(makeEdgesFromPoints(z_points))

        y_points = [numpy.array([0.,-offset,self.H/2]), numpy.array([0,offset,self.H/2])]
        line.append(makeEdgesFromPoints(y_points))
        
        u_points = [numpy.array([-uvoffset,uvoffset,self.H/2]), numpy.array([uvoffset,-uvoffset,self.H/2])]
        line.append(makeEdgesFromPoints(u_points))

        v_points = [numpy.array([-uvoffset,-uvoffset,self.H/2]), numpy.array([uvoffset,uvoffset,self.H/2])]
        line.append(makeEdgesFromPoints(v_points))

        start_pnt = [[-offset,0,self.H/2],[0,-offset+1,self.H/2],[uvoffset,-uvoffset,self.H/2],[uvoffset,uvoffset,self.H/2]]
        end_pnt = [[offset,0,self.H/2],[0,offset-3,self.H/2],[-uvoffset,uvoffset,self.H/2],[-uvoffset,-uvoffset,self.H/2]]

        return line, [start_pnt, end_pnt], labels

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    def display_lines(lines, points, labels):
        for l,p1,p2,n in zip(lines,points[0],points[1], labels):
            display.DisplayShape(l, update=True)
            display.DisplayMessage(getGpPt(p1), n, height=24, message_color=(0,0,0))
            display.DisplayMessage(getGpPt(p2), n, height=24, message_color=(0,0,0))

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
    lines, pnts, labels = CrossISec.create_marking()
    display.DisplayShape(prism, update=True)
    display_lines(lines, pnts, labels)
    display.View_Top()
    display.FitAll()
    display.DisableAntiAliasing()
    start_display()