'''
Created on 10-Mar-2016

@author: deepa
'''
import numpy
import copy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut


class BeamWebBeamWeb(object):

    def __init__(self, column, beam, notch, plate, Fweld, nut_bolt_array,gap):
        self.column = column
        self.beam = beam
        self.weldLeft = Fweld
        self.weldRight = copy.deepcopy(Fweld)
        self.plate = plate
        self.nut_bolt_array = nut_bolt_array
        self.notch = notch
        self.gap = gap
        self.columnModel = None
        self.beamModel = None
        self.weldModelLeft = None
        self.weldModelRight = None
        self.plateModel = None
        # This distance between edge of the column web/flange and beam cross section
        self.clearDist = 20.0

    def create_3dmodel(self):
        self.create_column_geometry()
        self.create_beam_geometry()
        self.create_plate_geometry()
        self.create_fillet_weld_geometry()
        self.create_nut_bolt_array()

        # Call for create_model
        self.columnModel = self.column.create_model()
        self.beamModel = self.beam.create_model()
        self.plateModel = self.plate.create_model()
        self.weldModelLeft = self.weldLeft.create_model()
        self.weldModelRight = self.weldRight.create_model()
        self.nutboltArrayModels = self.nut_bolt_array.create_model()

    def create_column_geometry(self):
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 1.0, 0.0])
        self.column.place(columnOrigin, column_uDir, wDir1)

    def create_beam_geometry(self):
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        shiftOrigin = (self.column.D / 2 - self.beam.D / 2)
        origin2 = self.column.sec_origin + (-shiftOrigin) * self.column.vDir + \
                  (self.column.t / 2 * self.column.uDir) + (self.column.length / 2 * self.column.wDir)\
                  + (self.gap * self.column.uDir)
        self.beam.place(origin2, uDir, wDir)

#     def createButtWeld(self):
#         pass
#         # plateThickness = 10
#         # uDir3 = numpy.array([0, 1.0, 0])
#         # wDir3 = numpy.array([1.0, 0, 0.0])
#         # origin3 = (self.column.sec_origin + 
#         #            self.column.t/2.0 * self.column.uDir + 
#         #            self.column.length/2.0 * self.column.wDir +
#         #            self.beam.t/2.0 * (-self.beam.uDir)+
#         #            self.weld.W/2.0 * (-self.beam.uDir))
#         # #origin3 = numpy.array([0, 0, 500]) + t/2.0 *wDir3 + plateThickness/2.0 * (-self.beam.uDir)
#         # self.weld.place(origin3, uDir3, wDir3)

    def create_plate_geometry(self):
        plateOrigin = (self.beam.sec_origin +
                       (self.beam.D / 2 - self.notch.height) * self.beam.vDir +
                       self.beam.t / 2 * (-self.beam.uDir) +
                       self.plate.L / 2 * (-self.beam.vDir) +
                       self.plate.T / 2 * (-self.beam.uDir) +
                       self.gap * (-self.beam.wDir))
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        self.plate.place(plateOrigin, uDir, wDir)

    def create_fillet_weld_geometry(self):
        uDir = numpy.array([1.0, 0.0, 0])
        wDir = numpy.array([0.0, 0.0, 1.0])
        filletWeld1Origin = (self.plate.sec_origin + self.plate.T / 2.0 * self.weldLeft.vDir + self.weldLeft.L / 2.0 * (-self.weldLeft.wDir))
        self.weldLeft.place(filletWeld1Origin, uDir, wDir)

        uDir1 = numpy.array([0.0, -1.0, 0])
        wDir1 = numpy.array([0.0, 0.0, 1.0])
        filletWeld2Origin = (filletWeld1Origin + self.plate.T * (-self.weldLeft.vDir))
        self.weldRight.place(filletWeld2Origin, uDir1, wDir1)

    def create_nut_bolt_array(self):

        nutboltArrayOrigin = self.plate.sec_origin 
        nutboltArrayOrigin = nutboltArrayOrigin - self.plate.T / 2.0 * self.plate.uDir
        nutboltArrayOrigin = nutboltArrayOrigin + self.plate.L / 2.0 * self.plate.vDir

        gaugeDir = self.plate.wDir
        pitchDir = -self.plate.vDir
        boltDir = self.plate.uDir
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def get_models(self):
        '''Returning 3D models
        '''
        return [self.columnModel, self.plateModel, self.weldModelLeft, self.weldModelRight,
                self.beamModel] + self.nut_bolt_array.get_models()

    def get_nutboltmodels(self):

        return self.nut_bolt_array.get_models()

    def get_beamModel(self):
        finalBeam = self.beamModel
        nutBoltlist = self.nut_bolt_array.get_models()
        for bolt in nutBoltlist[0:(len(nutBoltlist) // 2)]:
            finalBeam = BRepAlgoAPI_Cut(finalBeam, bolt).Shape()
        return finalBeam

    def get_columnModel(self):
        return self.columnModel