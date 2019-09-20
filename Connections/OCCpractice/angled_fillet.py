'''
Created on 27-May-2015

@author: deepa
'''
import numpy
# import math

from Connections.Component.ModelUtils import getGpPt, makeEdgesFromPoints, makeWireFromEdges, makeFaceFromWire, makePrismFromFace


from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()

b = 5
h = 5
L = 50


sec_origin = numpy.array([0, 0, 0])
uDir = numpy.array([1.0, 0, 0])
wDir = numpy.array([0.0, 0, 1.0])
vDir = numpy.cross(wDir, uDir)

# angle= math.sin(math.radians(5))
# angle = wDir * theta

a1 = sec_origin
a2 = sec_origin + b * uDir
a3 = sec_origin + h * vDir

points = [a1, a2, a3]
edges = makeEdgesFromPoints(points)
wire = makeWireFromEdges(edges)
aFace = makeFaceFromWire(wire)
extrudeDir = L * wDir   # extrudeDir is a numpy array
prism = makePrismFromFace(aFace, extrudeDir)
# return prism

display.DisplayShape(prism, update=True)

display.DisableAntiAliasing()
start_display()