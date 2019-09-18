'''
Created on 27-May-2015

@author: deepa
'''
import numpy
from Connections.Component.ModelUtils import getGpPt, makeEdgesFromPoints, makeWireFromEdges, makeFaceFromWire, makePrismFromFace


# from OCC.Display.SimpleGui import init_display
# display, start_display, add_menu, add_function_to_menu = init_display()

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
        self.points = [self.a1, self.a2, self.a3]

    def create_model(self):
        Pnt = getGpPt(self.sec_origin)
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.L * (self.wDir)  # extrudeDir is a numpy array
        prism = makePrismFromFace(aFace, extrudeDir)
        return prism


# b = 5
# h = 5
# L = 50
#
# channel = FilletWeld(b,h,L)
# # angles = channel.place()
# point = channel.compute_params()
# prism = channel.create_model()
# display.DisplayShape(prism, update=True)
# display.ExportToImage('./CAD_image.png')
# display.DisableAntiAliasing()
# start_display()