'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from ModelUtils import *


class Plate(object):
    
    def __init__(self, L, W, T):        
        self.L = L
        self.W = W 
        self.T = T
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.compute_params()
    
    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir        
        self.compute_params()
        
    def compute_params(self):
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.sec_origin + (self.T / 2.0) * self.uDir + (self.L / 2.0) * self.vDir
        self.a2 = self.sec_origin + (-self.T / 2.0) * self.uDir + (self.L / 2.0) * self.vDir
        self.a3 = self.sec_origin + (-self.T / 2.0) * self.uDir + (-self.L / 2.0) * self.vDir
        self.a4 = self.sec_origin + (self.T / 2.0) * self.uDir + (-self.L / 2.0) * self.vDir
        self.points = [self.a1, self.a2, self.a3, self.a4]
        
    def create_model(self):
        edges = make_edges_from_points(self.points)
        wire = make_wire_from_edges(edges)
        aFace = make_face_from_wire(wire)
        extrude_dir = self.W * self.wDir  # extrude_dir is a numpy array
        prism = make_prism_from_face(aFace, extrude_dir)
        
        return prism
