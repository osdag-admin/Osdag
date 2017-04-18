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
from nut_bolt_placement import NutBoltArray
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut
import math


class ColWebBeamWeb(object):
    
    def __init__(self,column,beam,angle,topclipangle,nutBoltArray):
        self.column = column
        self.beam = beam
        self.angle = angle
        self.topclipangle = topclipangle
        self.nut_bolt_array = nutBoltArray
        self.columnModel = None
        self.beamModel = None
        self.angleModel= None
        self.topclipangleModel = None
        self.clearDist = 20.0 # This distance between edge of the column web/flange and beam cross section
        
    def create_3dmodel(self):
        self.creatColumGeometry()
        self.createBeamGeometry()
        self.createAngleGeometry()
        self.createNutBoltArray()
        
        # Call for createModel
        self.columnModel = self.column.create_model()
        self.beamModel = self.beam.create_model()
        self.angleModel = self.angle.createModel()
        self.topclipangleModel = self.topclipangle.createModel()
        self.nutboltArrayModels = self.nut_bolt_array.createModel()
        
    def creatColumGeometry(self):
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        self.column.place(columnOrigin, column_uDir, wDir1)
        
                
    def createBeamGeometry(self):
        beamorigin = self.column.sec_origin + (self.column.t/2 * self.column.uDir) + (self.column.length/2 * self.column.wDir) + (self.clearDist * self.column.uDir)
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        self.beam.place(beamorigin, uDir, wDir)
        
    def createAngleGeometry(self):
        angleOrigin =((self.column.sec_origin)*self.column.vDir)+((self.column.length/2-self.beam.D/2) * self.column.wDir)+(self.angle.L/2 * (-self.column.vDir))

        wDir = numpy.array([0.0, 1.0, 0.0])
        uDir = numpy.array([1.0, 0.0, 0.0])
        self.angle.place(angleOrigin, uDir, wDir)
                 
        topclipangleOrigin =((self.column.sec_origin)*self.column.vDir)+((self.column.length/2+self.beam.D/2) * self.column.wDir)+(self.topclipangle.L/2 * (self.column.vDir))

        wDir = numpy.array([0.0, -1.0, 0.0])
        uDir = numpy.array([1.0, 0.0, 0.0])
        self.topclipangle.place(topclipangleOrigin, uDir, wDir)
                 
    
    def createNutBoltArray(self):
    
        gaugeDir = self.angle.wDir
        pitchDir = -self.angle.vDir
        boltDir = -self.angle.uDir
        
        #=======================================================================
        # nutboltArrayOrigin = self.angle.secOrigin 
        # nutboltArrayOrigin = nutboltArrayOrigin + self.angle.L/4 * self.angle.wDir  
        # nutboltArrayOrigin = nutboltArrayOrigin + self.angle.T * self.angle.uDir  
        # nutboltArrayOrigin = nutboltArrayOrigin + self.angle.A * self.angle.vDir
        #=======================================================================
        
        root2 = math.sqrt(2)
        nutboltArrayOrigin = self.angle.secOrigin  
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.A * self.angle.vDir 
        nutboltArrayOrigin= nutboltArrayOrigin + self.angle.T * self.angle.uDir 
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.R2*(1-1/root2) * self.angle.uDir 
        nutboltArrayOrigin = nutboltArrayOrigin - self.angle.R2/root2*self.angle.vDir
        
        
        bgaugeDir = self.angle.wDir
        bpitchDir = -self.angle.uDir
        bboltDir = -self.angle.vDir
        
        bnutboltArrayOrigin = self.angle.secOrigin + self.angle.B * self.angle.uDir 
        bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.T * self.angle.vDir 
        bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.R2*(1-1/root2) * self.angle.vDir 
        bnutboltArrayOrigin = bnutboltArrayOrigin - self.angle.R2/root2*self.angle.uDir
        
        #=======================================================================
        # bnutboltArrayOrigin = self.angle.secOrigin 
        # bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.L/4 * self.angle.wDir  
        # bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.T * self.angle.vDir  
        # bnutboltArrayOrigin = bnutboltArrayOrigin + (self.angle.B) * self.angle.uDir
        #=======================================================================
        
        topclipgaugeDir = -self.topclipangle.wDir
        topclippitchDir = -self.topclipangle.uDir
        topclipboltDir = -self.topclipangle.vDir
        
        topclipnutboltArrayOrigin = self.topclipangle.secOrigin  
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.B * self.topclipangle.uDir 
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.vDir 
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin - self.topclipangle.R2/root2 * self.topclipangle.uDir 
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.R2*(1-1/root2)*self.topclipangle.vDir
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.L * self.topclipangle.wDir
        
        #=======================================================================
        # topclipnutboltArrayOrigin = self.topclipangle.secOrigin 
        # topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.L/4 * self.topclipangle.wDir  
        # topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.uDir  
        # topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.A * self.topclipangle.vDir
        #=======================================================================
        
        topclipbgaugeDir = -self.topclipangle.wDir
        topclipbpitchDir = -self.topclipangle.vDir
        topclipbboltDir = -self.topclipangle.uDir
        
        topclipbnutboltArrayOrigin = self.topclipangle.secOrigin  
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.A * self.topclipangle.vDir 
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.uDir 
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin - self.topclipangle.R2/root2 * self.topclipangle.vDir 
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin+ self.topclipangle.R2*(1-1/root2)*self.topclipangle.uDir
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.L * self.topclipangle.wDir
        
        #=======================================================================
        # topclipbnutboltArrayOrigin = self.topclipangle.secOrigin 
        # topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.L/4 * self.topclipangle.wDir  
        # topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.vDir  
        # topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + (self.topclipangle.B) * self.topclipangle.uDir
        #=======================================================================
                  
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir, bnutboltArrayOrigin, bgaugeDir, bpitchDir,
                                bboltDir, topclipnutboltArrayOrigin, topclipgaugeDir, topclippitchDir, topclipboltDir, topclipbnutboltArrayOrigin,
                                topclipbgaugeDir, topclipbpitchDir, topclipbboltDir)
      
    def get_models(self):
        '''Returning 3D models
        '''
        return [self.columnModel,self.angleModel,self.beamModel,self.topclipangleModel] + self.nutBoltArray.get_models()
        
                
    def get_nutboltmodels(self):
        return self.nutBoltArray.get_models()
    
    def get_beamModel(self):
        finalbeam = self.beamModel
        nutBoltlist = self.nutBoltArray.get_beam_bolts()
        for bolt in nutBoltlist:
            finalbeam = BRepAlgoAPI_Cut(finalbeam,bolt).Shape()
        return finalbeam
    
    def get_angleModel(self):
        finalAngle = self.angleModel
        return finalAngle
    
    def get_columnModel(self):
        finalcol = self.columnModel
        nutBoltlist = self.nutBoltArray.get_column_bolts()
        for bolt in nutBoltlist:
            finalcol = BRepAlgoAPI_Cut(finalcol,bolt).Shape()
        return finalcol

                
                