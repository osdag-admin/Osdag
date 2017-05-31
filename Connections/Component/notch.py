'''
Created on 14-Mar-2016

@author: deepa
'''
from OCC.gp import gp_Circ, gp_Ax2
import numpy
from ModelUtils import make_edge, getGpPt, getGpDir, makeWireFromEdges, makeFaceFromWire, makePrismFromFace


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

    def createEdges(self):

        edges = []
        # Join points a,b
        edge = make_edge(getGpPt(self.a), getGpPt(self.b))
        edges.append(edge)
        # # Join points b1 and b2
        # cirl = gp_Circ(gp_Ax2(getGpPt(self.o1), getGpDir(self.wDir)), self.R1)
        # edge = make_edge(cirl,getGpPt(self.b2), getGpPt(self.b1))
        # edges.append(edge)
        # Join points b and c2
        edge = make_edge(getGpPt(self.b), getGpPt(self.c2))
        edges.append(edge)
        # join points c2 and c1
        cirl2 = gp_Circ(gp_Ax2(getGpPt(self.o2), getGpDir(self.wDir)), self.R1)
        edge = make_edge(cirl2, getGpPt(self.c1), getGpPt(self.c2))
        edges.append(edge)
        # Join points c1 and d
        edge = make_edge(getGpPt(self.c1), getGpPt(self.d))
        edges.append(edge)
        # Join points d and a
        edge = make_edge(getGpPt(self.d), getGpPt(self.a))
        edges.append(edge)

        return edges

    def create_model(self):
        edges = self.createEdges()
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.length * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)
        return prism
