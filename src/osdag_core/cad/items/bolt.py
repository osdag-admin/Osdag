'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from .ModelUtils import getGpPt, getGpDir, makeEdgesFromPoints, makeWireFromEdges, makePrismFromFace, makeFaceFromWire
import math
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Ax2
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse


class Bolt(object):
    '''

        a3  X-------------------+  a2
           X                   X|X
          X                   X | X
         X                   X  |  X
        X                   X   |   X
       X                   X    |    X
      X                   X     |     X
     X                   X 60   |      X
a4  X                   XXXXXXXXXXXXXXXXX  a1
     X                                 X
      X                               X
       XX                            X
        X                           X
         X                         X
          X                       X
           X                     X
            X-------------------X
                                   a6
            a5


    '''

    def __init__(self, R, T, H, r):
        self.R = R
        self.H = H
        self.T = T
        self.r = r
        self.origin = None
        self.uDir = None
        self.shaftDir = None
        self.vDir = None
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.a4 = None
        self.a5 = None
        self.a6 = None
        self.points = []

    def place(self, origin, uDir, shaftDir):
        self.origin = origin
        self.uDir = uDir
        self.shaftDir = shaftDir
        self.compute_params()

    def getPoint(self, theta):
        theta = math.radians(theta)
        point = self.origin + (self.R * math.cos(theta)) * self.uDir + (self.R * math.sin(theta)) * self.vDir 
        return point

    def compute_params(self):
        self.vDir = numpy.cross(self.shaftDir, self.uDir)
        self.a1 = self.getPoint(0)
        self.a2 = self.getPoint(60)
        self.a3 = self.getPoint(120)
        self.a4 = self.getPoint(180)
        self.a5 = self.getPoint(240)
        self.a6 = self.getPoint(300)
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]


    def create_model(self):
        # Standardize the key for caching: (R, T, H, r)
        # We model the bolt at the origin (0,0,0) with shaft along Z+ (0,0,1)
        
        cache_key = (self.R, self.T, self.H, self.r)
        
        # Check if we already have this shape cached
        if not hasattr(Bolt, "_shape_cache"):
            Bolt._shape_cache = {}
            
        if cache_key in Bolt._shape_cache:
            standard_shape = Bolt._shape_cache[cache_key]
        else:
            # Create the standard shape at Origin, Z+
            # Points for the hex head at Z=0, radius R
            # Note: We need to re-compute points for the STANDARD position, 
            # ignoring self.origin/self.shaftDir for the mesh generation.
            
            std_uDir = numpy.array([1.0, 0.0, 0.0])
            std_shaftDir = numpy.array([0.0, 0.0, 1.0]) # +Z
            std_vDir = numpy.array([0.0, 1.0, 0.0])
            
            # Helper to get point for standard hex
            def get_std_point(theta):
                rad = math.radians(theta)
                return numpy.array([0.,0.,0.]) + (self.R * math.cos(rad)) * std_uDir + (self.R * math.sin(rad)) * std_vDir

            a1 = get_std_point(0)
            a2 = get_std_point(60)
            a3 = get_std_point(120)
            a4 = get_std_point(180)
            a5 = get_std_point(240)
            a6 = get_std_point(300)
            
            points = [a1, a2, a3, a4, a5, a6]
            
            edges = makeEdgesFromPoints(points)
            wire = makeWireFromEdges(edges)
            aFace = makeFaceFromWire(wire)
            
            # Extrude downwards (along -Z) for the head thickness T
            extrudeDir = -self.T * std_shaftDir 
            boltHead = makePrismFromFace(aFace, extrudeDir)
            
            # Cylinder along +Z
            boltCylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(numpy.array([0.,0.,0.])), getGpDir(std_shaftDir)), self.r, self.H).Shape()
            
            standard_shape = BRepAlgoAPI_Fuse(boltHead, boltCylinder).Shape()
            
            # Cache it
            Bolt._shape_cache[cache_key] = standard_shape

        # Now move the standard shape to the desired location
        # 1. Create transformation from Standard (Origin, Z+) to Target (self.origin, self.shaftDir)
        
        from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Ax3, gp_Dir, gp_Pnt
        from OCC.Core.TopLoc import TopLoc_Location
        
        # Target System
        # Origin: self.origin
        # Direction: self.shaftDir
        # XDirection: self.uDir
        
        target_ax3 = gp_Ax3(getGpPt(self.origin), getGpDir(self.shaftDir), getGpDir(self.uDir))
        standard_ax3 = gp_Ax3(gp_Pnt(0.,0.,0.), gp_Dir(0.,0.,1.), gp_Dir(1.,0.,0.))
        
        trsf = gp_Trsf()
        trsf.SetTransformation(target_ax3, standard_ax3)
        
        # Apply transformation
        final_shape = standard_shape.Moved(TopLoc_Location(trsf))
        
        return final_shape

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    R = 8
    H = 10
    T = 5
    r = 3

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    bolt = Bolt(R, T, H, r)
    _place = bolt.place(origin, uDir, shaftDir)
    # point = bolt.compute_params() # No longer needed for create_model with cache
    prism = bolt.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()

