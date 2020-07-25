
import numpy
from cad.items.ModelUtils import *


class TISection(object):
   

    def __init__(self, D, B, T, t, P, Q, H):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.d = P
        self.b = Q
        self.length = H
        
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin + (self.t / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.b1 = self.sec_origin + (self.B / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.c1 = self.sec_origin + (self.B / 2.0) * self.uDir + (self.D / 2.0) * self.vDir
        self.a2 = self.sec_origin + (-self.t / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.b2 = self.sec_origin + (-self.B / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.c2 = self.sec_origin + (-self.B / 2.0) * self.uDir + (self.D / 2.0) * self.vDir
        self.a3 = self.sec_origin + (-self.t / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.d5 = self.sec_origin + ((-self.B / 2.0) + self.b) * self.uDir + -((self.D / 2.0) -self.T - self.d) * self.vDir
        self.d7 = self.sec_origin + ((-self.B / 2.0) + self.b) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.b3 = self.sec_origin + (-self.B / 2.0) * self.uDir + -((self.D / 2.0) - self.T - self.d) * self.vDir
        self.c3 = self.sec_origin + (-self.B / 2.0) * self.uDir + -(self.D / 2.0) * self.vDir
        self.a4 = self.sec_origin + (self.t / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.d6 = self.sec_origin + ((self.B / 2.0) - self.b) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.d4 = self.sec_origin + ((self.B / 2.0) - self.b) * self.uDir + -((self.D / 2.0) -self.T - self.d) * self.vDir
        self.b4 = self.sec_origin + (self.B / 2.0) * self.uDir + -((self.D / 2.0) - self.T - self.d) * self.vDir
        self.c4 = self.sec_origin + (self.B / 2.0) * self.uDir + -(self.D / 2.0) * self.vDir
        
        
        
        
        self.points = [self.a1, self.b1, self.c1,
                       self.c2, self.b2, self.a2,
                       self.a3, self.d7, self.d5,
                       self.b3, self.c3, self.c4, 
                       self.b4, self.d4, self.d6,
                       self.a4]

    def create_model(self):

        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.length * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)
                
        return prism

    def create_marking(self):
        middel_pnt = []
        line = []
        labels = ["z","y","u","v"]
        offset = self.D
        uvoffset = offset/numpy.sqrt(2)

        z_points = [numpy.array([-offset,0.,self.length/2]), numpy.array([offset,0.,self.length/2])]
        line.append(makeEdgesFromPoints(z_points))

        y_points = [numpy.array([0.,-offset,self.length/2]), numpy.array([0,offset,self.length/2])]
        line.append(makeEdgesFromPoints(y_points))
        
        u_points = [numpy.array([-uvoffset,uvoffset,self.length/2]), numpy.array([uvoffset,-uvoffset,self.length/2])]
        line.append(makeEdgesFromPoints(u_points))

        v_points = [numpy.array([-uvoffset,-uvoffset,self.length/2]), numpy.array([uvoffset,uvoffset,self.length/2])]
        line.append(makeEdgesFromPoints(v_points))

        start_pnt = [[-offset,0,self.length/2],[0,-offset+3,self.length/2],[uvoffset,-uvoffset,self.length/2],[uvoffset,uvoffset,self.length/2]]
        end_pnt = [[offset,0,self.length/2],[0,offset-2,self.length/2],[-uvoffset,uvoffset,self.length/2],[-uvoffset,-uvoffset,self.length/2]]

        return line, [start_pnt, end_pnt], labels

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    def display_lines(lines, points, labels):
        for l,p1,p2,n in zip(lines,points[0],points[1], labels):
            display.DisplayShape(l, update=True)
            display.DisplayMessage(getGpPt(p1), n, height=24,message_color=(0,0,0))
            display.DisplayMessage(getGpPt(p2), n, height=24,message_color=(0,0,0))

    B = 40
    T = 3
    D = 50
    t = 2
    P = 8
    Q = 4
    H = 100
    
    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    TISec = TISection(D, B, T, t, P, Q, H)
    _place = TISec.place(origin, uDir, shaftDir)
    point = TISec.compute_params()
    prism = TISec.create_model()
    lines, pnts, labels = TISec.create_marking()
    display.DisplayShape(prism, update=True)
    display_lines(lines, pnts, labels)
    display.View_Bottom()
    display.FitAll()
    display.DisableAntiAliasing()
    start_display()