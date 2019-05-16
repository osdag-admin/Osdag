'''
Created on 15-May-2019

@author: Anand Swaroop





'''
import numpy
from ModelUtils import *


class GrooveWeld(object):

    def __init__(self, b, h, L):
        self.b = b
        self.h = h
        self.L = L
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
        self.a1 = self.sec_origin + (self.b / 2.0) * self.uDir + (self.h / 2.0) * self.vDir
        self.a2 = self.sec_origin + (-self.b / 2.0) * self.uDir + (self.h / 2.0) * self.vDir
        self.a3 = self.sec_origin + (-self.b / 2.0) * self.uDir + (-self.h / 2.0) * self.vDir
        self.a4 = self.sec_origin + (self.b / 2.0) * self.uDir + (-self.h / 2.0) * self.vDir
        self.points = [self.a1, self.a2, self.a3, self.a4]

    def create_model(self):
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.L * self.wDir  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)

        return prism


