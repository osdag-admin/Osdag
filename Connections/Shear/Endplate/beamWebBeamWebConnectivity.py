'''
Created on 10-Mar-2016

@author: deepa
'''
'''
Created on 11-May-2015

@author: deepa
'''

import numpy
import copy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut


class BeamWebBeamWeb(object):
    
    def __init__(self, column, beam, notch, Fweld, plate, nut_bolt_array):
        self.column = column
        self.beam = beam
        self.notch = notch
        self.weldLeft = Fweld
        self.weldRight = copy.deepcopy(Fweld)
        self.plate = plate
        self.nut_bolt_array = nut_bolt_array
        self.columnModel = None
        self.beamModel = None
        self.weldModelLeft = None
        self.weldModelRight = None
        self.plateModel = None
        
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
        column_origin = numpy.array([0, 0, 0])
        column_u_dir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 1.0, 0.0])
        self.column.place(column_origin, column_u_dir, wDir1)
        
    def create_beam_geometry(self):
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        shift_origin = (self.column.D / 2 - self.beam.D / 2)
        origin2 = self.column.sec_origin + (-shift_origin) * self.column.vDir + \
                  (self.column.t / 2 * self.column.uDir) + (self.column.length / 2 * self.column.wDir) + (self.plate.T * self.column.uDir)
        self.beam.place(origin2, uDir, wDir)
        
#     def create_column_geometry(self):
#         column_origin = numpy.array([0, 0, 0])
#         column_u_dir = numpy.array([1.0, 0, 0])
#         wDir1 = numpy.array([0.0, -1.0, 0.0])
#         self.column.place(column_origin, column_u_dir, wDir1)
            
#     def create_beam_geometry(self):
#         uDir = numpy.array([0, -1.0, 0])
#         wDir = numpy.array([1.0, 0, 0.0])
#         origin2 = self.column.sec_origin + (self.column.D/2 - self.beam.D/2) * (self.column.vDir) + (self.column.t/2 +self.plate.T) * (self.column.uDir) + (self.column.length/2) * (self.column.wDir)
#         self.beam.place(origin2, uDir, wDir)
        
    def create_butt_weld(self):
        pass
        # plateThickness = 10
        # uDir3 = numpy.array([0, 1.0, 0])
        # wDir3 = numpy.array([1.0, 0, 0.0])
        # origin3 = (self.column.sec_origin +
        #            self.column.t/2.0 * self.column.uDir + 
        #            self.column.length/2.0 * self.column.wDir +
        #            self.beam.t/2.0 * (-self.beam.uDir)+
        #            self.weld.W/2.0 * (-self.beam.uDir))
        # #origin3 = numpy.array([0, 0, 500]) + t/2.0 *wDir3 + plateThickness/2.0 * (-self.beam.uDir)
        # self.weld.place(origin3, uDir3, wDir3)
        
    def create_plate_geometry(self):
        plate_origin = self.beam.sec_origin + (self.plate.W / 2) * (-self.beam.uDir) + (self.plate.T / 2) * (-self.beam.wDir) + (self.beam.D / 2 - self.notch.height - self.plate.L / 2) * (self.beam.vDir)  # (self.beam.D/2 - self.notch.height - self.plate.L/2) * (-self.beam.vDir) + (self.plate.W/2) * (self.beam.uDir) + (self.plate.T/2) * (-self.beam.wDir)
        uDir = numpy.array([1.0, 0.0, 0])
        wDir = numpy.array([0, 1.0, 0.0])
        self.plate.place(plate_origin, uDir, wDir)
        
    def create_fillet_weld_geometry(self):
        uDir = numpy.array([1.0, 0.0, 0])
        wDir = numpy.array([0.0, 0.0, 1.0])
        fillet_weld1_origin = (self.plate.sec_origin + (self.plate.T / 2.0 * self.plate.uDir) + (self.plate.W / 2 + self.beam.t / 2) * self.plate.wDir + self.plate.L / 2 * self.plate.vDir)
        self.weldLeft.place(fillet_weld1_origin, uDir, wDir)
         
        uDir1 = numpy.array([0.0, -1.0, 0])
        wDir1 = numpy.array([0.0, 0.0, 1.0])
        fillet_weld2_origin = (fillet_weld1_origin + self.beam.t * (-self.weldLeft.vDir))
        self.weldRight.place(fillet_weld2_origin, uDir1, wDir1)
        
    def create_nut_bolt_array(self):
        # nut_bolt_array_origin = self.plate.sec_origin
        # nut_bolt_array_origin -= self.plate.T/2.0 * self.plate.uDir
        # nut_bolt_array_origin += self.plate.L/2.0 * self.plate.vDir

        nut_bolt_array_origin = self.plate.sec_origin
        nut_bolt_array_origin = nut_bolt_array_origin + self.plate.T / 2.0 * self.plate.uDir
        nut_bolt_array_origin = nut_bolt_array_origin + (self.plate.L / 2.0) * self.plate.vDir

        nut_bolt_array_origin1 = nut_bolt_array_origin + (self.plate.W) * self.plate.wDir

        gauge_dir = self.plate.wDir
        pitch_dir = -self.plate.vDir
        bolt_dir = self.plate.uDir
        self.nut_bolt_array.place(nut_bolt_array_origin, nut_bolt_array_origin1, gauge_dir, pitch_dir, -bolt_dir)
        
    def get_models(self):
        '''Returning 3D models
        '''
        return [self.columnModel, self.plateModel, self.weldModelLeft, self.weldModelRight,
                self.beamModel] + self.nut_bolt_array.get_models()

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()


    def get_columnModel(self):
        final_column = self.columnModel
        bolt_list = self.nut_bolt_array.get_bolt_list()
        for bolt in bolt_list[:]:
            final_column = BRepAlgoAPI_Cut(final_column, bolt).Shape()
        return final_column
    
    def get_beamModel(self):
        return self.beamModel
