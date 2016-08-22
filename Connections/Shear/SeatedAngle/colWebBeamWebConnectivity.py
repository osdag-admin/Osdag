'''
Created on 11-May-2015

@author: deepa
'''

import numpy
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from bolt import Bolt
from nut import Nut 
from ModelUtils import *
import copy
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.gp import gp_Pnt
from nutBoltPlacement import NutBoltArray
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut


class ColWebBeamWeb(object):
    
    def __init__(self,column,beam,angle,topclipangle,nutBoltArray):
        self.column = column
        self.beam = beam
        self.angle = angle
        self.topclipangle = topclipangle
#         self.weldLeft = Fweld
#         self.weldRight = copy.deepcopy(Fweld)
#         self.plate = plate
        self.nutBoltArray = nutBoltArray
        self.columnModel = None
        self.beamModel = None
        self.angleModel= None
        self.topclipangleModel = None
#         self.weldModelLeft = None
#         self.weldModelRight = None
#         self.plateModel = None
        self.clearDist = 20.0 # This distance between edge of the column web/flange and beam cross section
        
    def create_3dmodel(self):
        self.creatColumGeometry()
        self.createBeamGeometry()
        self.createAngleGeometry()
#         self.createPlateGeometry()
#         self.createFilletWeldGeometry()
        self.createNutBoltArray()
        
        # Call for createModel
        self.columnModel = self.column.createModel()
        self.beamModel = self.beam.createModel()
        self.angleModel = self.angle.createModel()
        self.topclipangleModel = self.topclipangle.createModel()
#         self.plateModel = self.plate.createModel()
#         self.weldModelLeft = self.weldLeft.createModel()
#         self.weldModelRight = self.weldRight.createModel()
        self.nutboltArrayModels = self.nutBoltArray.createModel()
        
    def creatColumGeometry(self):
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        self.column.place(columnOrigin, column_uDir, wDir1)
        
                
    def createBeamGeometry(self):
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        origin2 = self.column.secOrigin + (self.column.t/2 * self.column.uDir) + (self.column.length/2 * self.column.wDir) + (self.clearDist * self.column.uDir) 
        self.beam.place(origin2, uDir, wDir)
        
    def createAngleGeometry(self):
#         angleOrigin =((self.column.secOrigin + self.column.D/2) * (-self.column.vDir)) + ((self.column.length/2-self.beam.D/2) * self.column.wDir)+(self.angle.L/2 * (-self.column.uDir))
        angleOrigin =((self.column.secOrigin)*self.column.vDir)+((self.column.length/2-self.beam.D/2) * self.column.wDir)+(self.angle.L/2 * (-self.column.vDir))

        wDir = numpy.array([0.0, 1.0, 0.0])
        uDir = numpy.array([1.0, 0.0, 0.0])
        self.angle.place(angleOrigin, uDir, wDir)
                 
        topclipangleOrigin =((self.column.secOrigin)*self.column.vDir)+((self.column.length/2+self.beam.D/2) * self.column.wDir)+(self.topclipangle.L/2 * (self.column.vDir))

        wDir = numpy.array([0.0, -1.0, 0.0])
        uDir = numpy.array([1.0, 0.0, 0.0])
        self.topclipangle.place(topclipangleOrigin, uDir, wDir)
                 
    
    def createNutBoltArray(self):
    
        gaugeDir = self.angle.wDir
        pitchDir = -self.angle.vDir
        boltDir = -self.angle.uDir
        
        nutboltArrayOrigin = self.angle.secOrigin 
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.L/4 * self.angle.wDir  
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.T * self.angle.uDir  
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.A * self.angle.vDir
        
        bgaugeDir = self.angle.wDir
        bpitchDir = -self.angle.uDir
        bboltDir = -self.angle.vDir
        
        bnutboltArrayOrigin = self.angle.secOrigin 
        bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.L/4 * self.angle.wDir  
        bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.T * self.angle.vDir  
        bnutboltArrayOrigin = bnutboltArrayOrigin + (self.angle.B) * self.angle.uDir
        
        topclipgaugeDir = self.topclipangle.wDir
        topclippitchDir = -self.topclipangle.vDir
        topclipboltDir = -self.topclipangle.uDir
        
        topclipnutboltArrayOrigin = self.topclipangle.secOrigin 
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.L/4 * self.topclipangle.wDir  
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.uDir  
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.A * self.topclipangle.vDir
        
        topclipbgaugeDir = self.topclipangle.wDir
        topclipbpitchDir = -self.topclipangle.uDir
        topclipbboltDir = -self.topclipangle.vDir
        
        topclipbnutboltArrayOrigin = self.topclipangle.secOrigin 
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.L/4 * self.topclipangle.wDir  
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.vDir  
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + (self.topclipangle.B) * self.topclipangle.uDir
                  
        self.nutBoltArray.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir,bnutboltArrayOrigin,bgaugeDir,bpitchDir,bboltDir, topclipnutboltArrayOrigin, topclipgaugeDir, topclippitchDir, topclipboltDir, topclipbnutboltArrayOrigin,topclipbgaugeDir,topclipbpitchDir,topclipbboltDir)
      
    def get_models(self):
        '''Returning 3D models
        '''
        #+ self.nutBoltArray.getnutboltModels()
        return [self.columnModel,self.angleModel,self.beamModel,self.topclipangleModel] + self.nutBoltArray.getModels()
        
                
    def get_nutboltmodels(self):
        return self.nutBoltArray.getModels()
        #return self.nutBoltArray.getboltModels()      
    
    def get_beamModel(self):
        finalBeam = self.beamModel
        nutBoltlist = self.nutBoltArray.getModels()
        for bolt in nutBoltlist[0:(len(nutBoltlist)//2)]:
            finalBeam = BRepAlgoAPI_Cut(finalBeam,bolt).Shape()
        return finalBeam
    
    def get_angleModel(self):
        finalAngle = self.angleModel
        return finalAngle
                
                