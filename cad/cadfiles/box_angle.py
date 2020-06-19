import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.cadfiles.anglebar import Angle
from cad.items.plate import Plate

class BoxAngle(object):
    def __init__(self, L, A, B, T, W, t, R1=0, R2=0):
        self.L = L
        self.A = A
        self.B = B
        self.T = T
        self.W = W
        self.t = t
        self.R1 = R1
        self.R2 = R2
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.angle1 = Angle(L, A, B, T, R1, R2)
        self.angle2 = Angle(L, A, B, T, R1, R2)
        self.angle3 = Angle(L, A, B, T, R1, R2)
        self.angle4 = Angle(L, A, B, T, R1, R2)
        self.plate1 = Plate(W, L, t)
        self.plate2 = Plate(t, L, W)
        self.plate3 = Plate(W, L, t)
        self.plate4 = Plate(t, L, W)

    def place(self, secOrigin, uDir, wDir):
        self.sec_origin = secOrigin
        self.uDir = uDir
        self.wDir = wDir
        width = self.W/2
        t = self.t/2
        origin1 = numpy.array([-width, -width+t*2, 0.])
        self.angle1.place(origin1, self.uDir, self.wDir)
        origin2 = numpy.array([-width+2*t, -width, 0.])
        self.angle2.place(origin2, self.uDir, self.wDir)
        origin3 = numpy.array([-width, -width+2*t, 0.])
        self.angle3.place(origin3, self.uDir, self.wDir)
        origin4 = numpy.array([-width+2*t, -width, 0.])
        self.angle4.place(origin4, self.uDir, self.wDir)
        origin5 = numpy.array([-width-t, 0., 0.])
        self.plate1.place(origin5, self.uDir, self.wDir)
        origin6 = numpy.array([0., -width+t, 0.])
        self.plate2.place(origin6, self.uDir, self.wDir)
        origin7 = numpy.array([width+t, 0., 0.])
        self.plate3.place(origin7, self.uDir, self.wDir)
        origin8 = numpy.array([0., width-t, 0.])
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
        prism = BRepAlgoAPI_Fuse(prism, prism5).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism6).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism7).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism8).Shape()        
        return prism

    def rotate(self, points, x):
        rotated_points = []
        rmatrix = numpy.array([[numpy.cos(x), -numpy.sin(x), 0],
                              [numpy.sin(x), numpy.cos(x), 0],
                              [0, 0, 1]]) 
        for point in points:
            point = numpy.matmul(rmatrix, point)
            rotated_points.append(point)
        return rotated_points




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

    box_angle = BoxAngle(L, A, B, T, W, t)
    _place = box_angle.place(origin, uDir, wDir)
    point = box_angle.compute_params()
    prism = box_angle.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()    