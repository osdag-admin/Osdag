'''
Created on 12-Dec-2014
NUT COMMENT
@author: deepa
'''

import math
import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from .ModelUtils import getGpPt, getGpDir, makeEdgesFromPoints, makeWireFromEdges, makePrismFromFace, makeFaceFromWire
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Ax2


class Nut(object):

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

    def __init__(self, R, T, H, innerR1):
        self.R = R
        self.H = H
        self.T = T
        self.r1 = innerR1
        # self.r2 = outerR2
        self.sec_origin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.compute_params()

    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        self.compute_params()

    def getPoint(self, theta):
        theta = math.radians(theta)
        point = self.sec_origin + (self.R * math.cos(theta)) * self.uDir + (self.R * math.sin(theta)) * self.vDir 
        return point

    def compute_params(self):

        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.getPoint(0)
        self.a2 = self.getPoint(60)
        self.a3 = self.getPoint(120)
        self.a4 = self.getPoint(180)
        self.a5 = self.getPoint(240)
        self.a6 = self.getPoint(300)
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]


    def create_model(self):
        # Standardize cache key
        cache_key = (self.R, self.T, self.H, self.r1)
        
        if not hasattr(Nut, "_shape_cache"):
            Nut._shape_cache = {}
            
        if cache_key in Nut._shape_cache:
            standard_shape = Nut._shape_cache[cache_key]
        else:
            # Create standard nut at Origin, Z+
            std_uDir = numpy.array([1.0, 0.0, 0.0])
            std_wDir = numpy.array([0.0, 0.0, 1.0]) # +Z
            std_vDir = numpy.array([0.0, 1.0, 0.0])
            
            # Recompute points for standard hex
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
            
            extrudeDir = self.T * std_wDir
            prism = makePrismFromFace(aFace, extrudeDir)
            
            # Inner cylinder for hole
            innerCyl = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(numpy.array([0.,0.,0.])), getGpDir(std_wDir)), self.r1, self.H).Shape()
            
            standard_shape = BRepAlgoAPI_Cut(prism, innerCyl).Shape()
            Nut._shape_cache[cache_key] = standard_shape

        # Transform to location
        from OCC.Core.gp import gp_Trsf, gp_Ax3, gp_Dir, gp_Pnt
        from OCC.Core.TopLoc import TopLoc_Location
        
        target_ax3 = gp_Ax3(getGpPt(self.sec_origin), getGpDir(self.wDir), getGpDir(self.uDir))
        standard_ax3 = gp_Ax3(gp_Pnt(0.,0.,0.), gp_Dir(0.,0.,1.), gp_Dir(1.,0.,0.))
        
        trsf = gp_Trsf()
        trsf.SetTransformation(target_ax3, standard_ax3)
        
        return standard_shape.Moved(TopLoc_Location(trsf))



if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    R = 10
    T = 8
    H = 10
    innerR1 = 5

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    wDir = numpy.array([0.,0.,1.])

    nut = Nut(R, T, H, innerR1)
    _place = nut.place(origin, uDir, wDir)
    point = nut.compute_params()
    prism = nut.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()
