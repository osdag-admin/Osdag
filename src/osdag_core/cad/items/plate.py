import numpy
from .ModelUtils import *

class Plate(object):
    def __init__(self, L, W, T, chamfer_w=0):
        self.L = L
        self.W = W
        self.T = T
        self.chamfer_w = chamfer_w
        self.sec_origin = numpy.array([0., 0., 0.])
        self.uDir = numpy.array([1., 0., 0.])
        self.wDir = numpy.array([0., 0., 1.])
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.compute_params()

    def compute_params(self):
        half_T = self.T / 2.0
        half_L = self.L / 2.0
        # Vertices for the face
        a1 = self.sec_origin + half_T * self.uDir + half_L * self.vDir
        a2 = self.sec_origin - half_T * self.uDir + half_L * self.vDir
        a3 = self.sec_origin - half_T * self.uDir - half_L * self.vDir
        a4 = self.sec_origin + half_T * self.uDir - half_L * self.vDir

        # Apply chamfer to create the V-groove slope
        if self.chamfer_w > 0:
            a1 = a1 - self.chamfer_w * self.vDir
            a4 = a4 + self.chamfer_w * self.vDir

        self.points = [a1, a2, a3, a4]

    def create_model(self, rotate_angle=None):
        from OCC.Core.gp import gp_Trsf, gp_OX
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
        from math import radians

        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.W * self.wDir
        prism = makePrismFromFace(aFace, extrudeDir)

        if rotate_angle is not None:
            trns = gp_Trsf()
            trns.SetRotation(gp_OX(), radians(rotate_angle))
            brep_trns = BRepBuilderAPI_Transform(prism, trns, False)
            brep_trns.Build()
            prism = brep_trns.Shape()
        return prism