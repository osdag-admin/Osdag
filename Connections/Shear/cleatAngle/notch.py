'''
Created on 14-Mar-2016

@author: deepa
'''
from OCC.gp import gp_Circ, gp_Ax2
'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from ModelUtils import *


class Notch(object):
    '''
                                                    
    ''' 
    
    def __init__(self, R1, height, width, length):  
        
        self.R1 = R1
        self.height = height
        self.width = width
        self.length = length
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0.0, 1.0])
        
        self.compute_params()
    
    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir        
        self.compute_params()
        
    def compute_params(self):
        
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a = self.sec_origin + (self.width / 2.0) * self.uDir
        self.b1 = self.a + (self.height - self.R1) * (-self.vDir)
        self.o1 = self.b1 + self.R1 * (-self.uDir)
        self.b = self.sec_origin + (self.width / 2.0) * self.uDir + self.height * (-self.vDir)
        self.b2 = self.b + self.R1 * (-self.uDir)
        
        self.d = self.sec_origin + (-self.width / 2.0) * self.uDir
        self.c1 = self.d + (self.height - self.R1) * (-self.vDir)
        self.o2 = self.c1 + self.R1 * self.uDir
        self.c = self.sec_origin + (self.width / 2.0) * (-self.uDir) + self.height * (-self.vDir)
        self.c2 = self.c + self.R1 * (self.uDir)
        
        self.points = [self.a, self.b1, self.o1, self.b, self.b2, self.d, self.c1, self.o2, self.c, self.c2]
        
        # self.points = [self.a, self.b, self.c, self.d]
    
    def create_edges(self):
        
        edges = []
        # Join points a,b
        edge = make_edge(get_gp_pt(self.a), get_gp_pt(self.b))
        edges.append(edge)
        # # Join points b1 and b2
        # cirl = gp_Circ(gp_Ax2(get_gp_pt(self.o1), get_gp_dir(self.wDir)), self.R1)
        # edge = make_edge(cirl,get_gp_pt(self.b2), get_gp_pt(self.b1))
        # edges.append(edge)
        # Join points b and c2
        edge = make_edge(get_gp_pt(self.b), get_gp_pt(self.c2))
        edges.append(edge)
        # join points c2 and c1
        cirl2 = gp_Circ(gp_Ax2(get_gp_pt(self.o2), get_gp_dir(self.wDir)), self.R1)
        edge = make_edge(cirl2, get_gp_pt(self.c1), get_gp_pt(self.c2))
        edges.append(edge)
        # Join points c1 and d
        edge = make_edge(get_gp_pt(self.c1), get_gp_pt(self.d))
        edges.append(edge)
        # Join points d and a
        edge = make_edge(get_gp_pt(self.d), get_gp_pt(self.a))
        edges.append(edge)
          
        return edges
    
    def create_model(self):
        edges = self.create_edges()
        wire = make_wire_from_edges(edges)
        aFace = make_face_from_wire(wire)
        extrude_dir = self.length * self.wDir  # extrude_dir is a numpy array
        prism = make_prism_from_face(aFace, extrude_dir)
        return prism

