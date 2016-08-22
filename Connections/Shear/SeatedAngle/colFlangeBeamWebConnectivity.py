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
    
    def __init__(self,column,beam,angle,topclipangle,nutBoltArray):
        self.column = column
        self.beam = beam
#         self.weldLeft = Fweld
#         self.weldRight = copy.deepcopy(Fweld)
        self.angle = angle
#         self.topclipangle = topclipangle
        self.topclipangle = topclipangle
        self.nutBoltArray = nutBoltArray
#         self.bnutBoltArray = bnutBoltArray
        self.columnModel = None
        self.beamModel = None
        self.angleModel = None
        self.topclipangleModel = None
#         self.weldModelLeft = None
#         self.weldModelRight = None
#         self.plateModel = None
        self.sphereModel = None
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
#         self.bnutBoltArrayModels = self.bnutBoltArray.createModel()
        
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
#         angleOrigin =(self.column.secOrigin+self.column.D/2) * (-self.angle.vDir) + (self.column.length/2 - self.beam.D/2)* (-self.angle.uDir)+self.column.secOrigin*self.angle.wDir
        angleOrigin =((self.column.secOrigin + self.column.D/2) * (-self.column.vDir)) + ((self.column.length/2-self.beam.D/2) * self.column.wDir)+(self.angle.L/2 * (-self.column.uDir))
        uDir = numpy.array([0.0, -1.0, 0.0])
        wDir = numpy.array([1.0, 0.0, 0.0])
        self.angle.place(angleOrigin, uDir, wDir)
        
        topclipangleOrigin =((self.column.secOrigin + self.column.D/2) * (-self.column.vDir)) + ((self.column.length/2+self.beam.D/2) * self.column.wDir)+(self.angle.L/2 * (self.column.uDir))
        tcuDir = numpy.array([0.0, -1.0, 0.0])
        tcwDir = numpy.array([-1.0, 0.0, 0.0])
        self.topclipangle.place(topclipangleOrigin, tcuDir, tcwDir)

        
    
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
        # return [self.columnModel,self.plateModel, self.weldModelLeft,self.weldModelRight,
        #         self.beamModel] + self.nutBoltArray.getModels()
        return [self.columnModel,self.beamModel,self.angleModel,self.topclipangleModel] + self.nutBoltArray.getModels() 
             
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
#         nutBoltlist = self.nutBoltArray.getModels()
#         for bolt in nutBoltlist[0:(len(nutBoltlist)//2)]:
#             finalAngle = BRepAlgoAPI_Cut(finalAngle,bolt).Shape()
        return finalAngle
        
    
    
    
    
    
    
    