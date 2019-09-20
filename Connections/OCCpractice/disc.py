import numpy
import math
from Connections.Component.ModelUtils import getGpPt, makeEdgesFromPoints, makeWireFromEdges, makeFaceFromWire, makePrismFromFace


from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()

R = 100

sec_origin = numpy.array([0, 0, 0])
uDir = numpy.array([1.0, 0, 0])
wDir = numpy.array([0.0, 0, 1.0])
vDir = numpy.cross(wDir, uDir)

points = []

for theta in range(360):
    theta = math.radians(theta)
    point = sec_origin + (R * math.cos(theta)) * uDir + (R * math.sin(theta)) * vDir
    points.append(point)

edges = makeEdgesFromPoints(points)
wire = makeWireFromEdges(edges)
aFace = makeFaceFromWire(wire)
extrudeDir = 10 * (wDir)  # extrudeDir is a numpy array
prism = makePrismFromFace(aFace, extrudeDir)

display.DisplayShape(prism, update=True)
display.DisableAntiAliasing()
start_display()