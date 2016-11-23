'''
Created on 27-May-2015

@author: deepa
'''
import numpy
from ModelUtils import *
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse


class FilletWeld(object):
    
    def __init__(self, b, h, L):        
        self.L = L
        self.b = b
        self.h = h
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
        self.a1 = self.sec_origin
        self.a2 = self.sec_origin + self.b * self.uDir
        self.a3 = self.sec_origin + self.h * self.vDir
        self.points = [self.a1, self.a2, self.a3, ]

    def create_model(self):
        pnt = get_gp_pt(self.sec_origin)
        edges = make_edges_from_points(self.points)
        wire = make_wire_from_edges(edges)
        aFace = make_face_from_wire(wire)
        extrude_dir = self.L * self.wDir  # extrude_dir is a numpy array
        prism = make_prism_from_face(aFace, extrude_dir)
        my_sphere = BRepPrimAPI_MakeSphere(pnt, 5.0).Shape()
        spherebody = BRepAlgoAPI_Fuse(prism, my_sphere).Shape()
        return prism
