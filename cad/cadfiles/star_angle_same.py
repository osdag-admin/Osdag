import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
#from cad.items.angle import Angle
from cad.cadfiles.anglebar import Angle
from cad.items.plate import Plate

class StarAngleSame(object):
    def __init__(self, a, b, t, l, t1, H):
        self.l = l
        self.a = a
        self.b = b
        self.t = t
        self.t1 = t1
        self.H = H

        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.angle1 = Angle(H, a, b, t, 0, 0)
        self.angle2 = Angle(H, b, a, t, 0, 0)
        self.plate1 = Plate(l, H, t1)

    def place(self, secOrigin, uDir, wDir):
        self.sec_origin = secOrigin
        self.uDir = uDir
        self.wDir = wDir
        origin1 = numpy.array([self.t1/2., 0., 0.])
        self.angle1.place(origin1, self.uDir, self.wDir)
        origin2 = numpy.array([0., self.t1/2., 0])
        self.angle2.place(origin2, self.uDir, self.wDir)
        self.plate1.place(self.sec_origin, self.uDir, self.wDir)

    def compute_params(self):
        self.angle1.computeParams()
        self.angle2.computeParams()
        self.angle2.points = self.rotate(self.angle2.points)
        self.angle2.points = self.rotate(self.angle2.points)
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


    a = 15
    b = 15
    l = 2*a
    t = 2
    t1 = 2
    H = 50

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    star_angle_same = StarAngleSame(a, b, t, l, t1, H)
    _place = star_angle_same.place(origin, uDir, wDir)
    point = star_angle_same.compute_params()
    prism = star_angle_same.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()    