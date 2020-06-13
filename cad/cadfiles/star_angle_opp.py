import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.cadfiles.anglebar import Angle
from cad.items.plate import Plate

class StarAngleOpposite(object):
    def __init__(self, L, A, B, T, R1, R2, W, t):
        self.L = L
        self.A = A
        self.B = B
        self.T = T
        self.t = t
        #self.R1 = R1
        self.R1 = 0.0
        #self.R2 = R2
        self.R2 = 0.0
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.angle1 = Angle(L, A, B, T, R1, R2)
        self.angle2 = Angle(L, A, B, T, R1, R2)
        self.plate1 = Plate(W, L, t)

    def place(self, secOrigin, uDir, wDir):
        self.sec_origin = secOrigin
        self.uDir = uDir
        self.wDir = wDir
        origin1 = numpy.array([self.t/2., 0., 0.])
        self.angle1.place(origin1, self.uDir, self.wDir)
        origin2 = numpy.array([0., self.t/2., 0])
        self.angle2.place(origin2, self.uDir, self.wDir)
        self.plate1.place(self.sec_origin, self.uDir, self.wDir)

    def compute_params(self):
        self.angle1.computeParams()
        self.angle2.computeParams()
        self.angle2.points = self.rotate(self.angle2.points)
        self.plate1.compute_params()

    def create_model(self):
        prism1 = self.angle1.create_model()
        prism2 = self.angle2.create_model()

        prism3 = self.plate1.create_model()

        prism = BRepAlgoAPI_Fuse(prism1, prism2).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism3).Shape()      
        return prism

    def rotate(self, points):
        rotated_points = []
        rmatrix = numpy.array([[0, -1, 0],[1, 0, 0],[0, 0, 1]]) 
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

    star_angle_opposite = StarAngleOpposite(L, A, B, T, R1, R2, W, t)
    _place = star_angle_opposite.place(origin, uDir, wDir)
    point = star_angle_opposite.compute_params()
    prism = star_angle_opposite.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()    