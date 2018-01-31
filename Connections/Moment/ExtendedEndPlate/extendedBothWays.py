'''
Initialized on 22-01-2018
Commenced on
@author: Siddhesh S. Chavan
'''

import numpy
# import copy

class ExtendedBothWays(object):

    # def __init__(self, beam, Fweld, Wweld, plate, nut_bolt_array):
    def __init__(self, beamLeft, beamRight, plateLeft, plateRight):
        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.plateLeft = plateLeft
        self.plateRight = plateRight
        # self.nut_bolt_array = nut_bolt_array
        # self.beamModel = None
        # self.weldModelF = None
        # self.weldModelW = None
        # self.plateModel = None

    def create_3DModel(self):
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateLGeometry()
        self.createPlateRGeometry()
        # self.createWebWeldGeometry()
        # self.create_nut_bolt_array()

        #call for create_model from Components
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateLModel = self.plateLeft.create_model()
        self.plateRModel = self.plateRight.create_model()
        # self.plateModel = self.plate.create_model()
        # self.weldModelF = self.Fweld.create_model()
        # self.weldModelW = self.Wweld.create_model()
        # self.nutBoltArrayModels = self.nut_bolt_array.create_model()

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamLeft.length + 2 * self.plateLeft.T
        beamOriginR = numpy.array([0.0, gap, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateLGeometry(self):
        plateOriginL = numpy.array([0.0, self.beamLeft.length, 0.0])
        plateL_uDir = numpy.array([1.0, 0.0, 0.0])
        plateL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

    def createPlateRGeometry(self):
        gap = self.beamLeft.length + self.plateLeft.T / 2
        plateOriginR = numpy.array([-self.plateRight.W/2, gap, 0.0])
        plateR_uDir = numpy.array([0.0, 1.0, 0.0])
        plateR_wDir = numpy.array([1.0, 0.0, 0.0])
        self.plateLeft.place(plateOriginR, plateR_uDir, plateR_wDir)

    def get_beamLModel(self):
        return self.beamLModel

    def get_beamRModel(self):
        return self.beamRModel

    def get_plateLModel(self):
        return self.plateLModel

    def get_plateRModel(self):
        return self.plateRModel

    def createFlangeWeldGeometry(self):
        pass

    def createWebWeldGeometry(self):
        pass

    def create_nut_bolt_array(self):
        pass


