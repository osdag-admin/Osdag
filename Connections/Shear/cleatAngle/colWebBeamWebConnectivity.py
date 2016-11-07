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


class ColWebBeamWeb(object):
    
    def __init__(self, column, beam, angle, nut_bolt_array):
        self.column = column
        self.beam = beam
        self.angle = angle
        self.angleLeft = copy.deepcopy(angle)
        self.nut_bolt_array = nut_bolt_array
        self.columnModel = None
        self.beamModel = None
        self.angleModel = None
        self.angleLeftModel = None
        self.clearDist = 20.0  # This distance between edge of the column web/flange and beam cross section
        
    def create_3dmodel(self):
        self.create_column_geometry()
        self.create_beam_geometry()
        self.create_angle_geometry()
        self.create_nut_bolt_array()
        
        # Call for createModel
        self.columnModel = self.column.createModel()
        self.beamModel = self.beam.createModel()
        self.angleModel = self.angle.createModel()
        self.angleLeftModel = self.angleLeft.createModel()
        self.nutboltArrayModels = self.nut_bolt_array.createModel()
        
    def create_column_geometry(self):
        column_origin = numpy.array([0, 0, 0])
        column_u_dir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        self.column.place(column_origin, column_u_dir, wDir1)

    def create_beam_geometry(self):
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        origin2 = self.column.secOrigin + (self.column.t / 2 * self.column.uDir) + (self.column.length / 2 * self.column.wDir) + (self.clearDist *
                                                                                                                                  self.column.uDir)
        self.beam.place(origin2, uDir, wDir)

    def create_angle_geometry(self):
        angle0_origin = (self.beam.secOrigin + (self.beam.D / 2.0 - self.beam.T - self.beam.R1 - 5) * self.beam.vDir + (self.beam.t / 2 * self.beam.uDir) +
                         self.clearDist * (-self.beam.wDir))
        uDir0 = numpy.array([1.0, 0, 0])
        wDir0 = numpy.array([0, 1, 0])
        self.angle.place(angle0_origin, uDir0, wDir0)

        angle1_origin = (self.beam.secOrigin + (self.beam.D / 2.0 - self.beam.T - self.beam.R1 - 5 - self.angle.L) * self.beam.vDir -
                         (self.beam.t / 2 * self.beam.uDir) + self.clearDist * (-self.beam.wDir))
        uDir1 = numpy.array([1.0, 0.0, 0])
        wDir1 = numpy.array([0, -1.0, 0])
        self.angleLeft.place(angle1_origin, uDir1, wDir1)
        
    def create_nut_bolt_array(self):
        nut_bolt_array_origin = self.angleLeft.secOrigin
        nut_bolt_array_origin = nut_bolt_array_origin + self.angleLeft.T * self.angleLeft.wDir
        nut_bolt_array_origin = nut_bolt_array_origin + self.angleLeft.A * self.angleLeft.uDir

        gauge_dir = self.angleLeft.uDir
        pitch_dir = self.angleLeft.vDir
        bolt_dir = -self.angleLeft.wDir
        #####################################################################################
        c_nutbolt_array_origin = self.angle.secOrigin
        c_nutbolt_array_origin = c_nutbolt_array_origin + self.angle.T * self.angle.uDir
        c_nutbolt_array_origin = c_nutbolt_array_origin + self.angle.B * self.angle.wDir

        c_gauge_dir = self.angle.wDir
        c_pitch_dir = self.angle.vDir
        c_bolt_dir = -self.angle.uDir

        c_nutbolt_array_origin1 = self.angleLeft.secOrigin
        c_nutbolt_array_origin1 = c_nutbolt_array_origin1 + self.angle.T * self.angle.uDir
        c_nutbolt_array_origin1 = c_nutbolt_array_origin - (self.beam.t + self.angle.B) * self.angle.wDir
        c_nutbolt_array_origin1 = c_nutbolt_array_origin1 + (self.angle.L * self.angle.vDir)

        c_gauge_dir1 = self.angle.wDir
        c_pitch_dir1 = self.angle.vDir
        c_bolt_dir1 = -self.angle.uDir
        
        self.nut_bolt_array.place(nut_bolt_array_origin, -gauge_dir, pitch_dir, bolt_dir, c_nutbolt_array_origin, -c_gauge_dir, c_pitch_dir, c_bolt_dir,
                                  c_nutbolt_array_origin1, c_gauge_dir1, c_pitch_dir1, c_bolt_dir1)

    def get_models(self):
        '''Returning 3D models
        '''
        return [self.columnModel, self.angleModel, self.angleLeftModel,
                self.beamModel] + self.nut_bolt_array.getModels()

    def get_nut_bolt_models(self):
        return self.nut_bolt_array.getModels()
        # return self.nut_bolt_array.getboltModels()
    
    def get_beam_model(self):
        final_beam = self.beamModel
        nut_bolt_list = self.nut_bolt_array.getModels()
        for bolt in nut_bolt_list[0:(len(nut_bolt_list) // 2)]:
            final_beam = BRepAlgoAPI_Cut(final_beam, bolt).Shape()
        return final_beam
    
    def get_column_model(self):
        final_beam = self.columnModel
        nut_bolt_list = self.nut_bolt_array.getModels()
        for bolt in nut_bolt_list[:]:
            final_beam = BRepAlgoAPI_Cut(final_beam, bolt).Shape()
        return final_beam
