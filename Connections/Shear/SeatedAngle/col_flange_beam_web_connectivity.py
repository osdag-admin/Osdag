'''
Created on 11-May-2015

@author: deepa
'''
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut
import math

'''
Created on 11-May-2015

@author: deepa
'''

import numpy

from bolt import Bolt
from nut import Nut
import copy


class ColFlangeBeamWeb(object):
    def __init__(self, column, beam, angle, topclipangle, nutBoltArray):
        self.column = column
        self.beam = beam
        #         self.weldLeft = Fweld
        #         self.weldRight = copy.deepcopy(Fweld)
        self.angle = angle
        #         self.topclipangle = topclipangle
        self.topclipangle = topclipangle
        self.nut_bolt_array = nutBoltArray
        #         self.bnut_bolt_array = bnutBoltArray
        self.columnModel = None
        self.beamModel = None
        self.angleModel = None
        self.topclipangleModel = None
        #         self.weldModelLeft = None
        #         self.weldModelRight = None
        #         self.plateModel = None
        self.sphereModel = None
        self.clearDist = 20.0  # This distance between edge of the column web/flange and beam cross section

    def create_3dmodel(self):
        self.creatColumGeometry()
        self.createBeamGeometry()
        self.createAngleGeometry()
        self.createNutBoltArray()

        # Call for createModel
        self.columnModel = self.column.create_model()
        self.beamModel = self.beam.create_model()
        self.angleModel = self.angle.create_model()
        self.topclipangleModel = self.topclipangle.create_model()
        #         self.plateModel = self.plate.createModel()
        #         self.weldModelLeft = self.weldLeft.createModel()
        #         self.weldModelRight = self.weldRight.createModel()
        self.nutboltArrayModels = self.nut_bolt_array.createModel()

    #         self.bnutBoltArrayModels = self.bnut_bolt_array.createModel()

    def creatColumGeometry(self):
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        self.column.place(columnOrigin, column_uDir, wDir1)

    def createBeamGeometry(self):
        beamOrigin = ((self.column.sec_origin + self.column.D / 2) * (-self.column.vDir)) + \
                     (self.column.length / 2 * self.column.wDir) + (self.clearDist * (-self.column.vDir))
        uDir = numpy.array([1.0, 0.0, 0])
        wDir = numpy.array([0.0, -1.0, 0.0])
        self.beam.place(beamOrigin, uDir, wDir)

    def createAngleGeometry(self):
        #         angleOrigin =(self.column.secOrigin+self.column.D/2) * (-self.angle.vDir) + (self.column.length/2 - self.beam.D/2)* (-self.angle.uDir)+self.column.secOrigin*self.angle.wDir
        angleOrigin = ((self.column.sec_origin + self.column.D / 2) * (-self.column.vDir)) + \
                      ((self.column.length / 2 - self.beam.D / 2) * self.column.wDir) + \
                      (self.angle.L / 2 * (-self.column.uDir))
        uDir = numpy.array([0.0, -1.0, 0.0])
        wDir = numpy.array([1.0, 0.0, 0.0])
        self.angle.place(angleOrigin, uDir, wDir)

        topclipangleOrigin = ((self.column.sec_origin + self.column.D / 2) * (-self.column.vDir)) + (
        (self.column.length / 2 + self.beam.D / 2) * self.column.wDir) + (self.angle.L / 2 * (self.column.uDir))
        tcuDir = numpy.array([0.0, -1.0, 0.0])
        tcwDir = numpy.array([-1.0, 0.0, 0.0])
        self.topclipangle.place(topclipangleOrigin, tcuDir, tcwDir)

    def createNutBoltArray(self):
        gaugeDir = self.angle.wDir
        pitchDir = -self.angle.vDir
        boltDir = -self.angle.uDir

        root2 = math.sqrt(2)
        nutboltArrayOrigin = self.angle.sec_origin
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.A * self.angle.vDir
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.T * self.angle.uDir
        nutboltArrayOrigin = nutboltArrayOrigin + self.angle.R2 * (1 - 1 / root2) * self.angle.uDir
        nutboltArrayOrigin = nutboltArrayOrigin - self.angle.R2 / root2 * self.angle.vDir

        ########################################################################
        # nutboltArrayOrigin = nutboltArrayOrigin + self.angle.L/4 * self.angle.wDir
        # nutboltArrayOrigin = nutboltArrayOrigin + self.angle.T * self.angle.uDir
        # nutboltArrayOrigin = nutboltArrayOrigin + self.angle.A * self.angle.vDir

        bgaugeDir = self.angle.wDir
        bpitchDir = -self.angle.uDir
        bboltDir = -self.angle.vDir

        bnutboltArrayOrigin = self.angle.sec_origin + self.angle.B * self.angle.uDir
        bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.T * self.angle.vDir
        bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.R2 * (1 - 1 / root2) * self.angle.vDir
        bnutboltArrayOrigin = bnutboltArrayOrigin - self.angle.R2 / root2 * self.angle.uDir

        # ---------------------------- bnutboltArrayOrigin = self.angle.secOrigin
        # bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.L/4 * self.angle.wDir
        # bnutboltArrayOrigin = bnutboltArrayOrigin + self.angle.T * self.angle.vDir
        # bnutboltArrayOrigin = bnutboltArrayOrigin + (self.angle.B) * self.angle.uDir

        topclipgaugeDir = -self.topclipangle.wDir
        topclippitchDir = -self.topclipangle.uDir
        topclipboltDir = -self.topclipangle.vDir

        topclipnutboltArrayOrigin = self.topclipangle.sec_origin
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.B * self.topclipangle.uDir
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.vDir
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin - self.topclipangle.R2 / root2 * self.topclipangle.uDir
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.R2 * (1 - 1 / root2) * self.topclipangle.vDir
        topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.L * self.topclipangle.wDir

        # --------------- topclipnutboltArrayOrigin = self.topclipangle.secOrigin

        # topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.L/4 * self.topclipangle.wDir
        # topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.uDir
        # topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.topclipangle.A * self.topclipangle.vDir

        topclipbgaugeDir = -self.topclipangle.wDir
        topclipbpitchDir = -self.topclipangle.vDir
        topclipbboltDir = -self.topclipangle.uDir

        topclipbnutboltArrayOrigin = self.topclipangle.sec_origin
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.A * self.topclipangle.vDir
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.uDir
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin - self.topclipangle.R2 / root2 * self.topclipangle.vDir
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.R2 * (1 - 1 / root2) * self.topclipangle.uDir
        topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.L * self.topclipangle.wDir
        
        #-------------- topclipbnutboltArrayOrigin = self.topclipangle.secOrigin

        # topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.L/4 * self.topclipangle.wDir
        # topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.topclipangle.T * self.topclipangle.vDir
        # topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + (self.topclipangle.B) * self.topclipangle.uDir

        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir, bnutboltArrayOrigin, bgaugeDir, bpitchDir, bboltDir, topclipnutboltArrayOrigin,
                                topclipgaugeDir, topclippitchDir, topclipboltDir, topclipbnutboltArrayOrigin, topclipbgaugeDir, topclipbpitchDir,
                                topclipbboltDir)

    def get_models(self):
        '''Returning 3D models
        '''
        # + self.nutBoltArray.getnutboltModels()
        # return [self.columnModel,self.plateModel, self.weldModelLeft,self.weldModelRight,
        #         self.beamModel] + self.nutBoltArray.get_models()
        return [self.columnModel, self.beamModel, self.angleModel, self.topclipangleModel] + self.nut_bolt_array.get_models()

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()
        # return self.nutBoltArray.getboltModels()

    def get_beamModel(self):
        finalbeam = self.beamModel
        nutBoltlist = self.nut_bolt_array.get_beam_bolts()
        print len(nutBoltlist)
        for bolt in nutBoltlist:
            finalbeam = BRepAlgoAPI_Cut(finalbeam,bolt).Shape()
        return finalbeam
    
    def get_angleModel(self):
        finalAngle = self.angleModel
        return finalAngle

    def get_column_model(self):
        finalcol = self.columnModel
        nutBoltlist = self.nut_bolt_array.get_column_bolts()
        print len(nutBoltlist)
        for bolt in nutBoltlist:
            finalcol = BRepAlgoAPI_Cut(finalcol,bolt).Shape()
        return finalcol

