import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.angle import Angle
from cad.items.plate import Plate

class StarAngle4(object):
    def __init__(self, L, A, B, T, R1, R2, W, t):
        self.L = L
        self.A = A
        self.B = B
        self.T = T
        #self.R1 = R1
        self.R1 = 0.0
        #self.R2 = R2
        self.R2 = 0.0
        self.t = t
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.angle1 = Angle(L, A, B, T, R1, R2)
        self.angle2 = Angle(L, A, B, T, R1, R2)
        self.angle3 = Angle(L, A, B, T, R1, R2)
        self.angle4 = Angle(L, A, B, T, R1, R2)
        #self.angle2 = Angle(L, -A, -B, -T, -T, R1, R2)
        #self.angle3 = Angle(L, A, -B, -T, T, R1, R2)
        #self.angle4 = Angle(L, -A, B, T, -T, R1, R2)
        self.plate1 = Plate(W, L, t)
        self.plate2 = Plate(t, L, W)

    def place(self, secOrigin, uDir, wDir):
        self.sec_origin = secOrigin
        self.uDir = uDir
        self.wDir = wDir
        t = self.t/2
        origin1 = numpy.array([t, t, 0.])
        self.angle1.place(origin1, self.uDir, self.wDir)
        origin2 = numpy.array([-t, -t, 0.])
        self.angle2.place(origin2, self.uDir, self.wDir)
        origin3 = numpy.array([-t, t, 0.])
        self.angle3.place(origin3, self.uDir, self.wDir)
        origin4 = numpy.array([t, -t, 0.])
        self.angle4.place(origin4, self.uDir, self.wDir)
        self.plate1.place(self.sec_origin, self.uDir, self.wDir)
        self.plate2.place(self.sec_origin, self.uDir, self.wDir)

    def compute_params(self):
        self.angle1.computeParams()
        self.angle2.computeParams()
        self.angle2.points = self.rotate(self.angle1.points)
        self.update_points(self.angle2, self.angle2.points)
        self.angle3.computeParams()
        self.angle3.points = self.rotate(self.angle2.points)
        self.update_points(self.angle3, self.angle3.points)
        self.angle4.computeParams()
        self.angle4.points = self.rotate(self.angle3.points)
        self.update_points(self.angle4, self.angle4.points)

        self.plate1.compute_params()
        self.plate2.compute_params()

    def create_model(self):
        prism1 = self.angle1.create_model()
        prism2 = self.angle2.create_model()
        prism3 = self.angle3.create_model()
        prism4 = self.angle4.create_model()


        prism5 = self.plate1.create_model()
        prism6 = self.plate2.create_model()

        prism = BRepAlgoAPI_Fuse(prism1, prism2).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism3).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism4).Shape() 
        prism = BRepAlgoAPI_Fuse(prism, prism5).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism6).Shape()        
        return prism


    def rotate(self, points):
        rotated_points = []
        rmatrix = numpy.array([[0, -1, 0],[1, 0, 0],[0, 0, 1]]) 
        for point in points:
            point = numpy.matmul(rmatrix, point)
            rotated_points.append(point)
        return rotated_points

    def update_points(self, angle, points):
        angle.a1,angle.a2,angle.a3,angle.a4,angle.a5,angle.a6, \
            angle.a7,angle.a8,angle.a9,angle.a10,angle.a11, angle.a12 = points

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    L = 50
    A = 15
    B = 15
    T = 2
    R1 = 8
    R2 = 5
    W = 40
    t = 2

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    star_angle = StarAngle4(L, A, B, T, R1, R2, W, t)
    _place = star_angle.place(origin, uDir, wDir)
    point = star_angle.compute_params()
    prism = star_angle.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()    