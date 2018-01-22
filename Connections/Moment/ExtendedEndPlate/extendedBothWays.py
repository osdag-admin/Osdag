'''
Initialized on 22-01-2018
Commenced on
@author: Siddhesh S. Chavan
'''

import numpy
import copy

class ExtendedBothWays(object):

    def __init__(self, beam, Fweld, Wweld, plate, nut_bolt_array):
        self.beam = beam
        self.Fweld = Fweld
        self.Wweld = Wweld
        self.plate = plate
        self.nut_bolt_array = nut_bolt_array
        self.beamModel = None
        self.weldModelF = None
        self.weldModelW = None
        self.plateModel = None

    def create_3DModel(self):
        self.createBeamGeometry()
        self.createPlateGeometry()
        self.createFlangeWeldGeometry()
        self.createWebWeldGeometry()
        self.create_nut_bolt_array()

        #call for create_model from Components
        self.beamModel = self.beam.create_model()
        self.plateModel = self.plate.create_model()
        self.weldModelF = self.Fweld.create_model()
        self.weldModelW = self.Wweld.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()

    def createBeamGeometry(self):
        beamOrigin = numpy.array([0.0, 0.0, 0.0])
        beam_uDir = numpy.array([1.0, 0.0, 0.0])
        beam_vDir = numpy.array([0.0, 1.0, 0.0])
        self.beam.place(beamOrigin, beam_uDir, beam_vDir)

    def createPlateGeometry(self):
        pass

    def createFlangeWeldGeometry(self):
        pass

    def createWebWeldGeometry(self):
        pass

    def create_nut_bolt_array(self):
        pass

    def get_models(self):
        return self.beamModel
