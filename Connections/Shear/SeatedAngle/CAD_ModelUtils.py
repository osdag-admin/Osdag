'''
Created on 29-Nov-2014

@author: deepa
'''
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.gp import gp_Pnt, gp_Dir, gp_Vec
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge,
                                BRepBuilderAPI_MakeVertex,
                                BRepBuilderAPI_MakeWire)
from OCC.BRepFill import BRepFill_Filling
from OCC.GeomAbs import GeomAbs_C0
from OCC.GeomAPI import GeomAPI_PointsToBSpline
from OCC.TColgp import TColgp_Array1OfPnt

    
def make_edge(*args):
    edge = BRepBuilderAPI_MakeEdge(*args)
    result = edge.Edge()
    return result


def make_vertex(*args):
    vert = BRepBuilderAPI_MakeVertex(*args)
    result = vert.Vertex()
    return result


def make_n_sided(edges, continuity=GeomAbs_C0):
    n_sided = BRepFill_Filling()
    for edg in edges:
        n_sided.Add(edg, continuity)
    n_sided.Build()
    face = n_sided.Face()
    return face


def make_wire(*args):
    # if we get an iterable, than add all edges to wire builder
    if isinstance(args[0], list) or isinstance(args[0], tuple):
        wire = BRepBuilderAPI_MakeWire()
        for i in args[0]:
            wire.Add(i)
        wire.Build()
        return wire.Wire()
    wire = BRepBuilderAPI_MakeWire(*args)
    return wire.Wire()


def points_to_bspline(pnts):
    pts = TColgp_Array1OfPnt(0, len(pnts)-1)
    for n, i in enumerate(pnts):
        pts.SetValue(n, i)
    crv = GeomAPI_PointsToBSpline(pts)
    return crv.Curve()

def makeWireFromEdges(edges):
    wire = None
    
    for edge in edges:
        if wire :
            wire = make_wire(wire, edge)
        else:
            wire = make_wire(edge)
    return wire

def makeFaceFromWire(wire):
    return BRepBuilderAPI_MakeFace(wire).Face()

def getGpPt(point):
    return gp_Pnt(point[0], point[1], point[2])

def getGpDir(direction):
    return gp_Dir(direction[0], direction[1], direction[2])

def makeEdgesFromPoints(points):
    edges = []
    num = len(points)
    for i in range(num - 1):
        edge = make_edge(getGpPt(points[i]), getGpPt(points[i + 1]))
        edges.append(edge)
    
    cycleEdge = make_edge(getGpPt(points[num - 1]), getGpPt(points[0]))
    edges.append(cycleEdge)
    
    return edges

def makePrismFromFace(aFace, eDir):
    return BRepPrimAPI_MakePrism(aFace, gp_Vec(gp_Pnt(0., 0., 0.),gp_Pnt(eDir[0], eDir[1], eDir[2]))).Shape()
