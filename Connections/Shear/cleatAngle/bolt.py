'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from ModelUtils import *
import math
from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.BRepAlgo import BRepAlgo_BooleanOperations
from OCC.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Ax2
from OCC.BRepAlgoAPI import  BRepAlgoAPI_Fuse
from OCC.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.TopAbs import TopAbs_EDGE
from OCC.TopoDS import topods
from OCC.TopExp import TopExp_Explorer


class Bolt(object):
    #
    def __init__(self, R, T, H, r):        
        self.R = R
        self.H = H
        self.T = T
        self.r = r
        self.origin = None
        self.uDir = None
        self.shaft_dir = None
        self.vDir = None
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.a4 = None
        self.a5 = None
        self.a6 = None
        self.points = []        
        # self.compute_params()
    
    def place(self, origin, uDir, shaft_dir):
        self.origin = origin
        self.uDir = uDir
        self.shaft_dir = shaft_dir
        self.compute_params()
        
    def get_point(self, theta):
        theta = math.radians(theta)
        point = self.origin + (self.R * math.cos(theta)) * self.uDir + (self.R * math.sin(theta)) * self.vDir 
        return point
    
    def compute_params(self):
        self.vDir = numpy.cross(self.shaft_dir, self.uDir)
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
        extrudeDir = -self.T * self.shaft_dir  # extrudeDir is a numpy array
        boltHead = make_prism_from_face(aFace, extrudeDir)
        cylOrigin = self.origin
        boltCylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(get_gp_pt(cylOrigin), get_gp_dir(self.shaft_dir)), self.r, self.H).Shape()

        whole_Bolt = BRepAlgoAPI_Fuse(boltHead, boltCylinder).Shape()

        return whole_Bolt

    # def create_model(self):
    #
    #     edges = make_edges_from_points(self.points)
    #     wire = make_wire_from_edges(edges)
    #     aFace = make_face_from_wire(wire)
    #     extrude_dir = -self.T * self.shaft_dir  # extrude_dir is a numpy array
    #     bolt_head = make_prism_from_face(aFace, extrude_dir)
    #     mk_fillet = BRepFilletAPI_MakeFillet(bolt_head)
    #     an_edge_explorer = TopExp_Explorer(bolt_head, TopAbs_EDGE)
    #     while an_edge_explorer.More():
    #         aEdge = topods.Edge(an_edge_explorer.Current())
    #         mk_fillet.Add(self.T / 17., aEdge)
    #         an_edge_explorer.Next()
    #
    #     bolt_head = mk_fillet.Shape()
    #     cyl_origin = self.origin
    #
    #     bolt_cylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(get_gp_pt(cyl_origin), get_gp_dir(self.shaft_dir)), self.r, self.H).Shape()
    #     whole_bolt = BRepAlgoAPI_Fuse(bolt_head, bolt_cylinder).Shape()
    #     mk_fillet = BRepFilletAPI_MakeFillet(whole_bolt)
    #
    #     return whole_bolt
