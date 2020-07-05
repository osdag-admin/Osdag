import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.cadfiles.anglebar import Angle
from cad.items.plate import Plate

class BoxAngle(object):
    def __init__(self, a, b, t, l, t1, l1, H, s, s1):
        self.l = s + 2*t1
        self.a = a
        self.b = b
        self.t = t
        self.s = s 
        self.s1 = s1
        self.t1 = t1
        self.l1 = s1 + 2*t1 + 2*t
        self.H = H

        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir

        self.angle1 = Angle(H, a, b, t, 0, 0)
        self.angle2 = Angle(H, b, a, t, 0, 0)
        self.angle3 = Angle(H, a, b, t, 0, 0)
        self.angle4 = Angle(H, b, a, t, 0, 0)
        self.plate1 = Plate(self.l, H, t1)
        self.plate2 = Plate(t1, H, self.l1)
        self.plate3 = Plate(self.l, H, t1)
        self.plate4 = Plate(t1, H, self.l1)

    def place(self, secOrigin, uDir, wDir):
        self.sec_origin = secOrigin
        self.uDir = uDir
        self.wDir = wDir
        verti = -self.t - self.s1/2#-self.s1/2 - self.b
        hori = -self.t - self.s/2 
        t = self.t1/2

        origin1 = numpy.array([verti, hori, 0.])
        self.angle1.place(origin1, self.uDir, self.wDir)
        origin2 = numpy.array([hori, verti, 0.])
        self.angle2.place(origin2, self.uDir, self.wDir)
        origin3 = numpy.array([verti, hori, 0.])
        self.angle3.place(origin3, self.uDir, self.wDir)
        origin4 = numpy.array([hori, verti, 0.])
        self.angle4.place(origin4, self.uDir, self.wDir)

        origin5 = numpy.array([-self.l1/2+t, 0., 0.])
        self.plate1.place(origin5, self.uDir, self.wDir)
        origin6 = numpy.array([0., -self.l/2-t, 0.])
        self.plate2.place(origin6, self.uDir, self.wDir)
        origin7 = numpy.array([self.l1/2-t, 0., 0.])
        self.plate3.place(origin7, self.uDir, self.wDir)
        origin8 = numpy.array([0., self.l/2+t, 0.])
        self.plate4.place(origin8, self.uDir, self.wDir)

    def compute_params(self):
        self.angle1.computeParams()
        self.angle2.computeParams()

        self.angle2.points = self.rotate(self.angle2.points, numpy.pi/2)
        self.angle3.computeParams()
        self.angle3.points = self.rotate(self.angle3.points, numpy.pi)
        self.angle4.computeParams()
        self.angle4.points = self.rotate(self.angle4.points, 3*numpy.pi/2)

        self.plate1.compute_params()
        self.plate2.compute_params()
        self.plate3.compute_params()
        self.plate4.compute_params()

    def create_model(self):
        prism1 = self.angle1.create_model()
        prism2 = self.angle2.create_model()
        prism3 = self.angle3.create_model()
        prism4 = self.angle4.create_model()


        prism5 = self.plate1.create_model()
        prism6 = self.plate2.create_model()
        prism7 = self.plate3.create_model()
        prism8 = self.plate4.create_model()

        prism = BRepAlgoAPI_Fuse(prism1, prism2).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism3).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism4).Shape() 
        # prism = BRepAlgoAPI_Fuse(prism, prism5).Shape()
        # prism = BRepAlgoAPI_Fuse(prism, prism6).Shape()
        # prism = BRepAlgoAPI_Fuse(prism, prism7).Shape()
        # prism = BRepAlgoAPI_Fuse(prism, prism8).Shape()        
        return prism, [prism5, prism6, prism7, prism8]

    def rotate(self, points, x):
        rotated_points = []
        rmatrix = numpy.array([[numpy.cos(x), -numpy.sin(x), 0],
                              [numpy.sin(x), numpy.cos(x), 0],
                              [0, 0, 1]]) 
        for point in points:
            point = numpy.matmul(rmatrix, point)
            rotated_points.append(point)
        return rotated_points

    def create_marking(self):
        middel_pnt = []
        line = []
        labels = ["z","y","u","v"]
        offset = (self.s + self.s1)/2
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
        end_pnt = [[offset,0,self.H/2],[0,offset-2,self.H/2],[-uvoffset,uvoffset,self.H/2],[-uvoffset,-uvoffset,self.H/2]]

        return line, [start_pnt, end_pnt], labels


if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    def display_lines(lines, points, labels):
        for l,p1,p2,n in zip(lines,points[0],points[1], labels):
            display.DisplayShape(l, update=True)
            display.DisplayMessage(getGpPt(p1), n, height=24, message_color=(0,0,0))
            display.DisplayMessage(getGpPt(p2), n, height=24, message_color=(0,0,0))


    a = 15
    b = 15
    t = 2
    t1 = 2
    s = 40
    s1 = 50
    l = s + 2*t1
    l1 = s1 + 2*t1 + 2*t
    H = 50


    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    box_angle = BoxAngle(a, b, t, l, t1, l1, H, s, s1)
    _place = box_angle.place(origin, uDir, wDir)
    point = box_angle.compute_params()
    prism, prisms = box_angle.create_model()
    lines, pnts, labels = box_angle.create_marking()
    display.DisplayShape(prism, update=True)
    for p in prisms:
        display.DisplayColoredShape(p, color='BLUE', update=True)
    display_lines(lines, pnts, labels)
    display.View_Top()
    display.FitAll()
    display.DisableAntiAliasing()
    start_display()    