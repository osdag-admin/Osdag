'''
Created on 11-May-2015

@author: deepa
'''
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut
'''
Created on 11-May-2015

@author: deepa
'''

import numpy


from bolt import Bolt
from nut import Nut 
import copy

class ColFlangeBeamWeb(object):
    
    def __init__(self,column,beam,angle,nutBoltArray):
        self.column = column
        self.beam = beam
        self.angle = angle
        self.angleLeft = copy.deepcopy(angle)
        self.nutBoltArray = nutBoltArray
        self.columnModel = None
        self.beamModel = None
        self.angleModel = None
        self.angleLeftModel = None
        self.plateModel = None
        self.clearDist = 20.0 # This distance between edge of the column web/flange and beam cross section
        
    def create_3dmodel(self):
        self.creatColumGeometry()
        self.createBeamGeometry()
        self.createAngleGeometry()
        self.createNutBoltArray()
        
        # Call for createModel
        self.columnModel = self.column.createModel()
        self.beamModel = self.beam.createModel()
        self.angleModel = self.angle.createModel()
        self.angleLeftModel = self.angleLeft.createModel()
        self.nutboltArrayModels = self.nutBoltArray.createModel()
        
    def creatColumGeometry(self):
        
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        self.column.place(columnOrigin, column_uDir, wDir1)
        
    def createBeamGeometry(self):
        beamOrigin =((self.column.secOrigin + self.column.D/2) * (-self.column.vDir)) + (self.column.length/2 * self.column.wDir) + (self.clearDist * (-self.column.vDir))
        uDir = numpy.array([1.0, 0.0, 0])
        wDir = numpy.array([0.0, -1.0, 0.0])
        self.beam.place(beamOrigin, uDir, wDir)
        
    
    def createAngleGeometry(self):
        angle0Origin = (self.column.secOrigin + 
                   (self.column.length/2.0 + self.angle.L/2.0) * self.column.wDir - (self.column.D/2 * self.column.vDir) +
                   +self.beam.t/2.0 * (self.column.uDir))
        uDir0 = numpy.array([0, -1.0, 0])
        wDir0 = numpy.array([1.0, 0, 0])
        self.angle.place(angle0Origin, uDir0, wDir0)
        
        angle1Origin = (self.column.secOrigin + 
                   (self.column.length/2.0 - self.angle.L/2.0) * self.column.wDir - (self.column.D/2 * self.column.vDir) 
                   -self.beam.t/2.0 * (self.column.uDir))
        uDir1 = numpy.array([0, -1.0, 0])
        wDir1 = numpy.array([-1.0, 0, 0])
        self.angleLeft.place(angle1Origin, uDir1, wDir1) 
        

    def createNutBoltArray(self):
        nutboltArrayOrigin = self.angle.secOrigin 
        nutboltArrayOrigin = nutboltArrayOrigin +self.angle.T * self.angle.wDir  
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.A * self.angle.uDir
        
        gaugeDir = self.angle.uDir
        pitchDir = self.angle.vDir
        boltDir = -self.angle.wDir
        
        cNutboltArrayOrigin = self.angle.secOrigin
        cNutboltArrayOrigin = cNutboltArrayOrigin + self.angle.T * self.angle.uDir
        cNutboltArrayOrigin = cNutboltArrayOrigin + self.angle.B * self.angle.wDir
        
        cguageDir = self.angle.wDir
        cpitchDir = self.angle.vDir
        cboltDir = -self.angle.uDir
        
        cNutboltArrayOrigin1 = self.angle.secOrigin
        cNutboltArrayOrigin1 = cNutboltArrayOrigin1 + self.angle.T * self.angle.uDir
        cNutboltArrayOrigin1 = cNutboltArrayOrigin -(self.beam.t + self.angle.B) * self.angle.wDir
        
        cguageDir1 = self.angle.wDir
        cpitchDir1 = self.angle.vDir
        cboltDir1 = -self.angle.uDir
        
        
        
        self.nutBoltArray.place(nutboltArrayOrigin, -gaugeDir, pitchDir, boltDir,cNutboltArrayOrigin, -cguageDir,cpitchDir, cboltDir, cNutboltArrayOrigin1, cguageDir1,cpitchDir1, cboltDir1 )
    
    
    def get_models(self):
        '''Returning 3D models
        '''
        return [self.columnModel,self.beamModel
                ,self.angleModel] + self.nutBoltArray.getModels()
             
    def get_nutboltmodels(self):
        
        return self.nutBoltArray.getModels()
        #return self.nutBoltArray.getboltModels() 
         
    def get_beamModel(self):
        finalBeam = self.beamModel
        nutBoltlist = self.nutBoltArray.getModels()
        for bolt in nutBoltlist[0:(len(nutBoltlist)//2)]:
            finalBeam = BRepAlgoAPI_Cut(finalBeam,bolt).Shape()
        return finalBeam
        
    
    
    
    
    
    
    