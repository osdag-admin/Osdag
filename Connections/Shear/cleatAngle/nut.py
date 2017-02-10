'''
Created on 12-Dec-2014
NUT COMMENT
@author: deepa
'''
from OCC.BRepFilletAPI import BRepFilletAPI_MakeFillet
# from OCC import TopoDS.TopoDS_Compound
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
import numpy
from ModelUtils import *
import math
from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
# from OCC.BRepAlgo import BRepAlgo_BooleanOperation

from OCC.TopAbs import TopAbs_EDGE  # TopAbs_FACE
from OCC.TopExp import TopExp_Explorer
from OCC.TopoDS import TopoDS_Compound, topods
from OCC.TopTools import *
from OCC.Geom import *
from OCC.gp import gp_Pnt, gp_Ax2, gp_DZ, gp_Ax3, gp_Pnt2d, gp_Dir2d, gp_Ax2d
from OCC.Geom import *
from OCC.Geom2d import *
from OCC.GCE2d import *
import OCC.BRepLib as BRepLib
from OCC.BRepOffsetAPI import *
import OCC.BRep as BRep


class Nut(object):

    def __init__(self, R, T, H, innerR1):
        self.R = R
        self.H = H
        self.T = T
        self.r1 = innerR1
        # self.r2 = outerR2
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def get_point(self, theta):
        theta = math.radians(theta)
        point = self.sec_origin + (self.R * math.cos(theta)) * self.uDir + (self.R * math.sin(theta)) * self.vDir
        return point

    def compute_params(self):

        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.get_point(0)
        self.a2 = self.get_point(60)
        self.a3 = self.get_point(120)
        self.a4 = self.get_point(180)
        self.a5 = self.get_point(240)
        self.a6 = self.get_point(300)
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]

    def create_model(self):

        edges = make_edges_from_points(self.points)
        wire = make_wire_from_edges(edges)
        aFace = make_face_from_wire(wire)
        extrudeDir = self.T * self.wDir  # extrudeDir is a numpy array
        prism = make_prism_from_face(aFace, extrudeDir)

        cylOrigin = self.sec_origin
        innerCyl = BRepPrimAPI_MakeCylinder(gp_Ax2(get_gp_pt(cylOrigin), get_gp_dir(self.wDir)), self.r1, self.H).Shape()

        result_shape = BRepAlgoAPI_Cut(prism, innerCyl).Shape()

        return result_shape


