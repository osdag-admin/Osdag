"""
Created on 06-03-2018
aurthor @ Siddhesh S. Chavan

             25mm
         +--------->
        a1         a2
       + +--------X
       | |            X
       | |                 X
       | |                      X
Hst    | |                           X
       | |                                   X
       | |                                         X   X   X + a3  ^
       | |                                                   |     |
       | |                                                   |     |  25mm
       | |                                                   |     |
       | |                                                   |     |
       v +---------------------------------------------------+  a4 +
       Origin
                                Lst
         +---------------------------------------------------->

"""
import numpy
from ModelUtils import *

class Stiffener_CAD(object):
    def __init__(self, Hst, Lst, Tst):
        """
        :param Hst: Height of stiffener 
        :param Lst: Length of stiffener
        :param Tst: Thickness of stiffener
        """
        self.Hst = Hst
        self.Lst = Lst
        self.Tst = Tst
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0.0, 0.0])
        self.wDir = numpy.array([0.0, 0.0, 1.0])
        self.vDir = self.wDir * self.uDir
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        """
        :param sec_origin: Section origin as mentioned above in figure 
        :param uDir: Directional component in X -direction
        :param wDir: Directional component in Z -direction
        :return: Vertices of stiffener
        """
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def compute_params(self):
        """
        :return: Calculates the vertices of stiffener and returns vertices in python list
        """
        self.vDir = numpy.cross(self.wDir, self.uDir)   # Cross product of vector wDir and uDir
        self.a1 = self.sec_origin + self.Hst * self.vDir
        self.a2 = self.a1 + 25.0 * self.uDir
        self.a3 = self.a2 - (self.Hst - 25.0) * self.vDir + (self.Lst - 25.0) * self.uDir
        self.a4 = self.a3 - 25.0 * self.vDir
        self.points = [self.a1, self.a2, self.a3, self.a4, ]

    def create_model(self):
        """
        :return: The complete 3D CAD model of stiffener, debugging would give clear idea.
          prism is the 3D CAD model of stiffener
        """
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.Tst * self.wDir
        prism = makePrismFromFace(aFace, extrudeDir)
        return prism
