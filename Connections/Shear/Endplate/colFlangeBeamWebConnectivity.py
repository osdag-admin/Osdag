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


class ColFlangeBeamWeb(object):
    
    def __init__(self,column,beam,Fweld,plate,nutBoltArray):
        self.column = column
        self.beam = beam
        self.weldLeft = Fweld
        self.weldRight = copy.deepcopy(Fweld)
        self.plate = plate
        self.nutBoltArray = nutBoltArray
        self.columnModel = None
        self.beamModel = None
        self.weldModelLeft = None
        self.weldModelRight = None
        self.plateModel = None
        self.sphereModel = None
        self.clearDist = 20.0 # This distance between edge of the column web/flange and beam cross section
        
    
    def create_3dmodel(self):
        self.creatColumGeometry()
        self.createBeamGeometry()
        self.createPlateGeometry()
        self.createFilletWeldGeometry()
        self.createNutBoltArray()
        
        # Call for createModel
        self.columnModel = self.column.createModel()
        self.beamModel = self.beam.createModel()
        self.plateModel = self.plate.createModel()
        self.weldModelLeft = self.weldLeft.createModel()
        self.weldModelRight = self.weldRight.createModel()
        self.nutboltArrayModels = self.nutBoltArray.createModel()
        
    def creatColumGeometry(self):
        
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([0, 1.0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        self.column.place(columnOrigin, column_uDir, wDir1)
        
    def createBeamGeometry(self):
        beamOrigin =((self.column.secOrigin + self.column.D/2) * (-self.column.vDir)) + (self.column.length/2 * self.column.wDir) + (self.plate.T * (-self.column.vDir))
        uDir = numpy.array([0.0, 1.0, 0])
        wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam.place(beamOrigin, uDir, wDir)
        
    def createButtWeld(self):
        pass
        # plateThickness = 10
        # uDir3 = numpy.array([0, 1.0, 0])
        # wDir3 = numpy.array([1.0, 0, 0.0])
        # origin3 = (self.column.secOrigin + 
        #            self.column.t/2.0 * self.column.uDir + 
        #            self.column.length/2.0 * self.column.wDir +
        #            self.beam.t/2.0 * (-self.beam.uDir)+
        #            self.weld.W/2.0 * (-self.beam.uDir))
        # #origin3 = numpy.array([0, 0, 500]) + t/2.0 *wDir3 + plateThickness/2.0 * (-self.beam.uDir)
        # self.weld.place(origin3, uDir3, wDir3)
        
    def createPlateGeometry(self):
        plateOrigin = self.beam.secOrigin + (self.plate.W/2)*(-self.beam.uDir) + (self.plate.T/2)*(-self.beam.wDir) + (self.beam.D/2 - self.beam.T - self.beam.R1 - 5 - self.plate.L/2)*(self.beam.vDir)
        uDir = numpy.array([1.0, 0.0, 0.0])
        wDir = numpy.array([0.0, 1.0, 0.0])
        self.plate.place(plateOrigin, uDir, wDir)
                
    def createFilletWeldGeometry(self):
        uDir = numpy.array([1.0, 0.0, 0.0])
        wDir = numpy.array([0.0, 0.0, -1.0])
        filletWeld1Origin = (self.plate.secOrigin + (self.plate.T/2.0 * self.plate.uDir) + (self.plate.W/2 - self.beam.t/2)* self.plate.wDir - self.plate.L/2 * self.plate.vDir)
        self.weldLeft.place(filletWeld1Origin, uDir, wDir)
         
        uDir1 = numpy.array([0.0, 1.0, 0.0])
        wDir1 = numpy.array([0.0, 0.0, -1.0])
        filletWeld2Origin = (filletWeld1Origin + self.beam.t * (self.plate.wDir))
        self.weldRight.place(filletWeld2Origin,uDir1,wDir1)

    def createNutBoltArray(self):
        # nutboltArrayOrigin = self.plate.secOrigin 
        # nutboltArrayOrigin -= self.plate.T/2.0 * self.plate.uDir  
        # nutboltArrayOrigin += self.plate.L/2.0 * self.plate.vDir
        
        nutboltArrayOrigin = self.plate.secOrigin 
        nutboltArrayOrigin = nutboltArrayOrigin +self.plate.T/2.0 * self.plate.uDir  
        nutboltArrayOrigin = nutboltArrayOrigin + (self.plate.L/2.0) * self.plate.vDir
        
        nutboltArrayOrigin1 = nutboltArrayOrigin + (self.plate.W) * self.plate.wDir

        
        gaugeDir = self.plate.wDir
        pitchDir = -self.plate.vDir
        boltDir = self.plate.uDir
        self.nutBoltArray.place(nutboltArrayOrigin,nutboltArrayOrigin1, gaugeDir, pitchDir, -boltDir)
    
    def get_models(self):
        '''Returning 3D models
        '''
        #+ self.nutBoltArray.getnutboltModels()
        # return [self.columnModel,self.plateModel, self.weldModelLeft,self.weldModelRight,
        #+ self.nutBoltArray.getnutboltModels()
        return [self.columnModel,self.plateModel, self.weldModelLeft,self.weldModelRight,
                self.beamModel] + self.nutBoltArray.getModels()
             
    def get_nutboltmodels(self):
        
        return self.nutBoltArray.getModels()
        #return self.nutBoltArray.getboltModels() 
         
    def get_columnModel(self):
        finalBeam = self.columnModel
        nutBoltlist = self.nutBoltArray.getModels()
        for bolt in nutBoltlist[:]:
            finalBeam = BRepAlgoAPI_Cut(finalBeam,bolt).Shape()
        return finalBeam
        
    
    
    
    
    
    
    