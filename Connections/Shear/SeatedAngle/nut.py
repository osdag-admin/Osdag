'''
Created on 12-Dec-2014
NUT COMMENT
@author: deepa
'''
from OCC.BRepFilletAPI import BRepFilletAPI_MakeFillet
#from OCC import TopoDS.TopoDS_Compound
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
import numpy
from ModelUtils import *
import math
from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
#from OCC.BRepAlgo import BRepAlgo_BooleanOperation

from OCC.TopAbs import TopAbs_EDGE #TopAbs_FACE
from OCC.TopExp import TopExp_Explorer
from OCC.TopoDS import TopoDS_Compound, topods
from OCC.TopTools import *
from OCC.Geom import *
from OCC.gp import gp_Pnt,gp_Ax2,gp_DZ,gp_Ax3,gp_Pnt2d,gp_Dir2d,gp_Ax2d
from OCC.Geom import *
from OCC.Geom2d import *
from OCC.GCE2d import *
import OCC.BRepLib as BRepLib
from OCC.BRepOffsetAPI import *
import OCC.BRep as BRep

class Nut(object):
    
    def __init__(self,R,T,H,innerR1):        
        self.R = R
        self.H = H
        self.T = T
        self.r1 = innerR1
        #self.r2 = outerR2
        self.secOrigin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.computeParams()
    
    def place(self, secOrigin, uDir, wDir):
        self.secOrigin = secOrigin
        self.uDir = uDir
        self.wDir = wDir        
        self.computeParams()
        
    def getPoint(self,theta):
        theta = math.radians(theta)
        point = self.secOrigin + (self.R * math.cos(theta)) * self.uDir + (self.R * math.sin(theta)) * self.vDir 
        return point
    
    def computeParams(self):
        
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.getPoint(0)
        self.a2 = self.getPoint(60)
        self.a3 = self.getPoint(120)
        self.a4 = self.getPoint(180)
        self.a5 = self.getPoint(240)
        self.a6 = self.getPoint(300)
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]
       
        
    def createModel(self):
        
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * self.wDir # extrudeDir is a numpy array
        prism =  makePrismFromFace(aFace, extrudeDir)
        mkFillet = BRepFilletAPI_MakeFillet(prism)
        anEdgeExplorer = TopExp_Explorer(prism, TopAbs_EDGE)
        while anEdgeExplorer.More():
            aEdge = topods.Edge(anEdgeExplorer.Current())
            mkFillet.Add(self.T / 17. , aEdge)
            anEdgeExplorer.Next()
                
        prism = mkFillet.Shape()
        cylOrigin = self.secOrigin
        #cylOrigin = self.secOrigin + self.T * self.wDir
        innerCyl = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(cylOrigin), getGpDir(self.wDir)), self.r1, self.H).Shape()
        #outerCyl = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(cylOrigin), getGpDir(self.wDir)), self.r2, self.H).Shape()
        #nutBody = BRepAlgoAPI_Fuse(prism, outerCyl).Shape()
        #my_cyl = BRepPrimAPI_MakeCylinder(9.0, 6.0).Shape()
        #result_shape = BRepAlgoAPI_Cut(nutBody, innerCyl).Shape() 
        result_shape = BRepAlgoAPI_Cut(prism, innerCyl).Shape() 
        
        
#         self.secOrigin = gp_Pnt(0 , 0 , 0)
#         neckNormal = gp_DZ()
#         # Threading : Create Surfaces
# 
#         nutAx2_bis = gp_Ax3(self.secOrigin , neckNormal)
#         aCyl1 = Geom_CylindricalSurface(nutAx2_bis , self.T * 0.99)
#         aCyl2 = Geom_CylindricalSurface(nutAx2_bis , self.T * 1.05)
#         #aCyl3 = Geom_CylindricalSurface(nutAx2_bis , self.T * 1.11)
#         aCyl1_handle = aCyl1.GetHandle()
#         aCyl2_handle = aCyl2.GetHandle()
#         #aCyl3_handle = aCyl3.GetHandle()
#         
#         # Threading : Define 2D Curves
#         aPnt = gp_Pnt2d(2. * math.pi , self.H / 2.)
#         aDir = gp_Dir2d(2. * math.pi , self.H / 4.)
#         aAx2d = gp_Ax2d(aPnt , aDir)
#         aMajor = 2. * math.pi
#         aMinor = self.H / 7.
#         anEllipse1 = Geom2d_Ellipse(aAx2d , aMajor , aMinor)
#         anEllipse2 = Geom2d_Ellipse(aAx2d , aMajor , aMinor / 4.)
#         anEllipse1_handle = anEllipse1.GetHandle()
#         anEllipse2_handle = anEllipse2.GetHandle()
#         aArc1 = Geom2d_TrimmedCurve(anEllipse1_handle, 0 , math.pi)
#         aArc2 = Geom2d_TrimmedCurve(anEllipse2_handle, 0 , math.pi)
#         aArc1_handle = aArc1.GetHandle()
#         aArc2_handle = aArc2.GetHandle()
#         anEllipsePnt1 = anEllipse1.Value(0)
#         anEllipsePnt2 = anEllipse1.Value(math.pi)
#         aSegment = GCE2d_MakeSegment(anEllipsePnt1 , anEllipsePnt2)
#         
#         # Threading : Build Edges and Wires
# 
#         aEdge1OnSurf1 = BRepBuilderAPI_MakeEdge( aArc1_handle , aCyl1_handle)
#         aEdge2OnSurf1 = BRepBuilderAPI_MakeEdge( aSegment.Value() , aCyl1_handle)
#         aEdge1OnSurf2 = BRepBuilderAPI_MakeEdge( aArc2_handle , aCyl2_handle)
#         aEdge2OnSurf2 = BRepBuilderAPI_MakeEdge( aSegment.Value() , aCyl2_handle)
#         threadingWire1 = BRepBuilderAPI_MakeWire(aEdge1OnSurf1.Edge() , aEdge2OnSurf1.Edge())#aEdge3OnSurf1.Edge())
#         self.threading1 = threadingWire1
#         threadingWire2 = BRepBuilderAPI_MakeWire(aEdge1OnSurf2.Edge() , aEdge2OnSurf2.Edge())#aEdge3OnSurf2.Edge())
#         BRepLib.breplib.BuildCurves3d(threadingWire1.Shape())
#         BRepLib.breplib.BuildCurves3d(threadingWire2.Shape())
#         
#         # Create Threading
# 
#         aTool = BRepOffsetAPI_ThruSections(True)
#         aTool.AddWire(threadingWire1.Wire())
#         aTool.AddWire(threadingWire2.Wire())
#         aTool.CheckCompatibility(False)
#         myThreading = aTool.Shape()
#         
#         #Building the resulting compound
#         
#         aRes = TopoDS_Compound()
#         aBuilder = BRep.BRep_Builder()
#         aBuilder.MakeCompound(aRes)
#         aBuilder.Add(aRes, result_shape)
#         aBuilder.Add(aRes, myThreading)
#         final_shape = BRepAlgoAPI_Cut(result_shape, myThreading).Shape() 

        
        return result_shape
    
            