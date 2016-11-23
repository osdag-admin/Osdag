'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from ModelUtils import *
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut
from notch import Notch


class ISection(object):

    '''
                              ^ v
                              |                     
            c2                .                c1                            
     ---    +-----------------|-----------------+     ---
      ^     |                 .                 |      ^
      | T   |                 |                 |      |
      v     |                 .                 |      |  
     ---    +------------+    |    +------------+      |
            b2         a2|         | a1         b1     |
                         |    t    |                   |
                         |<------->|                   |
                         |    |    |                   |
                         |    .    |                   |D
                         |    |O   |                   |
    -- -- -- -- -- -- -- -- --.-- -- -- -- -- -- -- -- |-- -- -> u
                         |    |    |                   |
                         |    .    |                   |
                         |    |    |                   |
                         |    .    |                   |
             b3        a3|    |    |a4          b4     |
             +-----------+    .    +------------+      |
             |                |                 |      |
             |                .                 |      |
             |                |                 |      v
             +----------------.-----------------+     ---
             c3               B                 c4       
             |<-------------------------------->| 
                                                    
    ''' 
    
    def __init__(self, B, T, D, t, R1, R2, alpha, length, notch_obj):
        self.B = B
        self.T = T 
        self.D = D
        self.t = t
        self.R1 = R1
        self.R2 = R2
        self.alpha = alpha
        self.length = length
        self.clearDist = 20
        self.notch_obj = notch_obj
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
        self.a1 = self.sec_origin + (self.t / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.b1 = self.sec_origin + (self.B / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.c1 = self.sec_origin + (self.B / 2.0) * self.uDir + (self.D / 2.0) * self.vDir
        self.a2 = self.sec_origin + (-self.t / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.b2 = self.sec_origin + (-self.B / 2.0) * self.uDir + ((self.D / 2.0) - self.T) * self.vDir
        self.c2 = self.sec_origin + (-self.B / 2.0) * self.uDir + (self.D / 2.0) * self.vDir
        self.a3 = self.sec_origin + (-self.t / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.b3 = self.sec_origin + (-self.B / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.c3 = self.sec_origin + (-self.B / 2.0) * self.uDir + -(self.D / 2.0) * self.vDir
        self.a4 = self.sec_origin + (self.t / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.b4 = self.sec_origin + (self.B / 2.0) * self.uDir + -((self.D / 2.0) - self.T) * self.vDir
        self.c4 = self.sec_origin + (self.B / 2.0) * self.uDir + -(self.D / 2.0) * self.vDir
        self.points = [self.a1, self.b1, self.c1,
                       self.c2, self.b2, self.a2,
                       self.a3, self.b3, self.c3,
                       self.c4, self.b4, self.a4]
        # self.points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    
    def create_model(self):
        
        edges = make_edges_from_points(self.points)
        wire = make_wire_from_edges(edges)
        aFace = make_face_from_wire(wire)
        extrude_dir = self.length * self.wDir  # extrude_dir is a numpy array
        prism = make_prism_from_face(aFace, extrude_dir)
        
        if self.notch_obj is not None:
            uDir = numpy.array([-1.0, 0.0, 0])
            wDir = numpy.array([0.0, 1.0, 0.0])
            shift_origin = self.D / 2.0 * self.vDir + self.notch_obj.width / 2.0 * self.wDir + self.B / 2.0 * -self.uDir
            # + self.notch_obj.width* self.wDir + self.T/2.0 * -self.uDir
            origin2 = self.sec_origin + shift_origin
             
            self.notch_obj.place(origin2, uDir, wDir)

            notch_model = self.notch_obj.create_model()
            prism = BRepAlgoAPI_Cut(prism, notch_model).Shape()
        
        return prism

