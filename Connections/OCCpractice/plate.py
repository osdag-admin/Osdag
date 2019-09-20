import  numpy
from Connections.Component.ModelUtils import getGpPt, makeEdgesFromPoints, makeWireFromEdges, makeFaceFromWire, makePrismFromFace

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()

l = 20
b = 10
w = 2

a = numpy.array([0,0,0])
b = numpy.array([0,20,0])
c = numpy.array([10,20,0])
d = numpy.array([10,0,0])
extrudeDir = numpy.array([0,0,2])

points = [a,b,c,d]
edges = makeEdgesFromPoints(points)
wire = makeWireFromEdges(edges)
face = makeFaceFromWire(wire)
prism = makePrismFromFace(face, extrudeDir)

display.DisplayShape(prism, update = True)
start_display()