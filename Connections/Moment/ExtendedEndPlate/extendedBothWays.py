'''
Initialized on 22-01-2018
Commenced on
@author: Siddhesh S. Chavan
'''

import numpy
from Connections.Component.bolt import Bolt
from Connections.Moment.ExtendedEndPlate.nutBoltPlacement import NutBoltArray
# import copy

class ExtendedBothWays(object):

    # def __init__(self, beam, Fweld, Wweld, plate, nut_bolt_array):
    def __init__(self, beamLeft, beamRight, plateLeft, plateRight, nut_bolt_array, WeldModelsF, WeldModelsW):
        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.plateLeft = plateLeft
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.WeldModelsF = WeldModelsF
        self.WeldModelsW = WeldModelsW
        # self.beamModel = None
        # self.weldModelF = None
        # self.weldModelW = None
        # self.plateModel = None

    def create_3DModel(self):
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateLGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.createWeldGeometryF()
        self.createWeldGeometryW()
        # self.create_nut_bolt_array()

        #call for create_model from Components
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateLModel = self.plateLeft.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        self.WeldModelsF = self.WeldModelsF.create_model()
        self.WeldModelsW = self.WeldModelsW.create_model()
        # self.weldModelW = self.Wweld.create_model()
        # self.nutBoltArrayModels = self.nut_bolt_array.create_model()

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamRight.length + 2 * self.plateRight.T
        beamOriginR = numpy.array([0.0, gap, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateLGeometry(self):
        plateOriginL = numpy.array([-0.5 * self.plateLeft.W, 1.5 * self.plateLeft.T + self.beamLeft.length, 0.0])
        plateL_uDir = numpy.array([0.0, 1.0, 0.0])
        plateL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.plateRight.place(plateOriginL, plateL_uDir, plateL_wDir)

    def createPlateRGeometry(self):
        gap = self.beamRight.length + 0.5 * self.plateRight.T
        plateOriginR = numpy.array([-self.plateRight.W/2, gap, 0.0])
        plateR_uDir = numpy.array([0.0, 1.0, 0.0])
        plateR_wDir = numpy.array([1.0, 0.0, 0.0])
        self.plateLeft.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        nutboltArrayOrigin = self.plateLeft.sec_origin + numpy.array([0.0, 0.0, self.plateLeft.L/2])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, 0, -1.0])
        boltDir = numpy.array([0, 1.0, 0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def createWeldGeometryF(self):
        weld1origin = numpy.array([self.beamLeft.B/2, self.beamLeft.length, self.beamLeft.D / 2])
        uDir5 = numpy.array([0, -1.0, 0])
        wDir5 = numpy.array([-1.0, 0, 0])
        self.WeldModelsF.place(weld1origin, uDir5, wDir5)

    def createWeldGeometryW(self):
        weld2origin = numpy.array([-self.beamLeft.T / 2, self.beamLeft.length, self.beamLeft.D / 2 - self.beamLeft.T])
        uDir6 = numpy.array([0, -1.0, 0])
        wDir6 = numpy.array([0.0, 0, -1.0])
        self.WeldModelsW.place(weld2origin, uDir6, wDir6)

    def get_beamLModel(self):
        return self.beamLModel

    def get_beamRModel(self):
        return self.beamRModel

    def get_plateLModel(self):
        return self.plateLModel

    def get_plateRModel(self):
        return self.plateRModel

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()

    def get_weldmodelsF(self):
        return self.WeldModelsF

    def get_weldmodelsW(self):
        return self.WeldModelsW

