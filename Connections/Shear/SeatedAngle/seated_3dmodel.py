'''
Created on 17-Oct-2016

@author: deepa
'''
from OCC.Quantity  import Quantity_Color, Quantity_NOC_SADDLEBROWN

from OCC.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.GC import GC_MakeArcOfCircle
from OCC.TopExp import TopExp_Explorer
from OCC.TopoDS import topods
from OCC.TopAbs import TopAbs_EDGE
import math
import numpy

from ModelUtils import *

L = 140
A = 150
B = 75
T = 12
R1 = 10
R2 = 4.8

secOrigin = numpy.array([0, 0, 0])
uDir = numpy.array([1.0, 0, 0])
wDir = numpy.array([0.0, 0, 1.0])
vDir = wDir * uDir

vDir = numpy.cross(wDir, uDir)
root2 = math.sqrt(2)
a1 = secOrigin
a2 = secOrigin + (A) * vDir
a3 = secOrigin + (T - R2)* uDir + A * vDir 
a4 = secOrigin + (T - R2 + R2/root2)* uDir + (A - R2 + R2/root2) * vDir 
a5 = secOrigin + (T)* uDir + (A - R2) * vDir 
a6 = secOrigin + (T)* uDir + (T + R1) * vDir 
a7 = secOrigin + (T + R1 - R1/root2)* uDir + (T + R1 - R1/root2) * vDir 
a8 = secOrigin + (T + R1)* uDir + T * vDir 
a9 = secOrigin + (B - R2)* uDir + T * vDir 
a10 = secOrigin + (B - R2 + R2/root2)* uDir + (T - R2 + R2/root2) * vDir 
a11 = secOrigin + (B)* uDir + (T - R2) * vDir 
a12 = secOrigin + B * uDir

points = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12]

edges = []
if R2 == float(0.0):
    a3= a4 =a5
    edge1 = make_edge(getGpPt(a1),getGpPt(a2))
    edges.append(edge1)
    edge2 = make_edge(getGpPt(a2),getGpPt(a3))
    edges.append(edge2)
    edge3 = make_edge(getGpPt(a3),getGpPt(a6))
    edges.append(edge3)
    arc2 = GC_MakeArcOfCircle(getGpPt(a6),getGpPt(a7),getGpPt(a8))
    edge4 = make_edge(arc2.Value())
    edges.append(edge4)
    edge5 = make_edge(getGpPt(a8),getGpPt(a9))
    edges.append(edge5)
    edge6 = make_edge(getGpPt(a9),getGpPt(a12))
    edges.append(edge6)
    edge7 = make_edge(getGpPt(a12),getGpPt(a1))
    edges.append(edge7)
else:    
    edge1 = make_edge(getGpPt(a1),getGpPt(a2))
    edges.append(edge1)
    edge2 = make_edge(getGpPt(a2),getGpPt(a3))
    edges.append(edge2)
    arc1 = GC_MakeArcOfCircle(getGpPt(a3),getGpPt(a4),getGpPt(a5))
    edge3 = make_edge(arc1.Value())
    edges.append(edge3)
    edge4 = make_edge(getGpPt(a5),getGpPt(a6))
    edges.append(edge4)
    arc2 = GC_MakeArcOfCircle(getGpPt(a6),getGpPt(a7),getGpPt(a8))
    edge5 = make_edge(arc2.Value())
    edges.append(edge5)
    edge6 = make_edge(getGpPt(a8),getGpPt(a9))
    edges.append(edge6)
    arc3 = GC_MakeArcOfCircle(getGpPt(a9),getGpPt(a10),getGpPt(a11))
    edge7 = make_edge(arc3.Value())
    edges.append(edge7)
    edge8 = make_edge(getGpPt(a11),getGpPt(a12))
    edges.append(edge8)
    edge9 = make_edge(getGpPt(a12),getGpPt(a1))
    edges.append(edge9)
print"%%%%%%%%%%%%%%%%",edges

wire = makeWireFromEdges(edges)
aFace = makeFaceFromWire(wire)
extrudeDir = L * wDir # extrudeDir is a numpy array
prism =  makePrismFromFace(aFace, extrudeDir)
mkFillet = BRepFilletAPI_MakeFillet(prism)
anEdgeExplorer = TopExp_Explorer(prism, TopAbs_EDGE)
while anEdgeExplorer.More():
    aEdge = topods.Edge(anEdgeExplorer.Current())
    mkFillet.Add(T / 17. , aEdge)
    anEdgeExplorer.Next()
         
prism = mkFillet.Shape()

display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayColoredShape(prism,Quantity_Color(Quantity_NOC_SADDLEBROWN), update=True)

start_display()

   
           