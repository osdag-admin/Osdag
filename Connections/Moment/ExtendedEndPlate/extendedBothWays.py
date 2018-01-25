'''
Initialized on 22-01-2018
Commenced on
@author: Siddhesh S. Chavan
'''

import numpy
import copy

class ExtendedBothWays(object):

    # def __init__(self, beam, Fweld, Wweld, plate, nut_bolt_array):
    def __init__(self, beamLeft, beamRight):
        self.beamLeft = beamLeft
        self.beamRight = beamRight
        # self.Fweld = Fweld
        # self.Wweld = Wweld
        # self.plate = plate
        # self.nut_bolt_array = nut_bolt_array
        # self.beamModel = None
        # self.weldModelF = None
        # self.weldModelW = None
        # self.plateModel = None

    def create_3DModel(self):
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        # self.createFlangeWeldGeometry()
        # self.createWebWeldGeometry()
        # self.create_nut_bolt_array()

        #call for create_model from Components
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        # self.plateModel = self.plate.create_model()
        # self.weldModelF = self.Fweld.create_model()
        # self.weldModelW = self.Wweld.create_model()
        # self.nutBoltArrayModels = self.nut_bolt_array.create_model()

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_vDir = numpy.array([0.0, 1.0, 0.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_vDir)

    def createBeamRGeometry(self):
        beamOriginR = numpy.array([0.0, 850.0, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_vDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_vDir)

    def createPlateGeometry(self):
        pass

    def createFlangeWeldGeometry(self):
        pass

    def createWebWeldGeometry(self):
        pass

    def create_nut_bolt_array(self):
        pass

    def get_beamLModel(self):
        return self.beamLModel

    def get_beamRModel(self):
        return self.beamRModel
