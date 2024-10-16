'''
Created on 19-March-2020

@author : Anand Swaroop
'''

from cad.items.anchor_bolt import *
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt
import copy


class NutBoltArray():
    """
    add a diagram here
    """

    def __init__(self, BP, nut, nut_in, bolt, bolt_in, nutSpace, washer, washer_in):


        self.BP = BP
        self.nut = nut
        self.nut_in = nut_in
        self.bolt = bolt
        self.bolt_in = bolt_in
        self.gap = nutSpace
        self.washer = washer
        self.washer_in = washer_in
        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.noOfBolts_outFlange = self.BP.anchors_outside_flange
        self.noofBolts_inFlange = self.BP.anchors_inside_flange

        self.ab1 = copy.deepcopy(self.bolt)
        self.ab2 = copy.deepcopy(self.bolt)
        self.ab3 = copy.deepcopy(self.bolt)
        self.ab4 = copy.deepcopy(self.bolt)

        self.ab5 = copy.deepcopy(self.bolt)
        self.ab6 = copy.deepcopy(self.bolt)
        self.ab7 = copy.deepcopy(self.bolt)
        self.ab8 = copy.deepcopy(self.bolt)

        self.ab9 = copy.deepcopy(self.bolt)
        self.ab10 = copy.deepcopy(self.bolt)
        self.ab11 = copy.deepcopy(self.bolt)
        self.ab12 = copy.deepcopy(self.bolt)


        self.ab_inflg1 = copy.deepcopy(self.bolt_in)
        self.ab_inflg2 = copy.deepcopy(self.bolt_in)

        self.ab_inflg3 = copy.deepcopy(self.bolt_in)
        self.ab_inflg4 = copy.deepcopy(self.bolt_in)

        self.ab_inflg5 = copy.deepcopy(self.bolt_in)
        self.ab_inflg6 = copy.deepcopy(self.bolt_in)
        self.ab_inflg7 = copy.deepcopy(self.bolt_in)
        self.ab_inflg8 = copy.deepcopy(self.bolt_in)
        
        self.w1 = copy.deepcopy(self.washer)
        self.w2 = copy.deepcopy(self.washer)
        self.w3 = copy.deepcopy(self.washer)
        self.w4 = copy.deepcopy(self.washer)
        self.w5 = copy.deepcopy(self.washer)
        self.w6 = copy.deepcopy(self.washer)
        self.w7 = copy.deepcopy(self.washer)
        self.w8 = copy.deepcopy(self.washer)
        self.w9 = copy.deepcopy(self.washer)
        self.w10 = copy.deepcopy(self.washer)
        self.w11 = copy.deepcopy(self.washer)
        self.w12 = copy.deepcopy(self.washer)

        self.w_in1 = copy.deepcopy(self.washer_in)
        self.w_in2 = copy.deepcopy(self.washer_in)
        self.w_in3 = copy.deepcopy(self.washer_in)
        self.w_in4 = copy.deepcopy(self.washer_in)
        self.w_in5 = copy.deepcopy(self.washer_in)
        self.w_in6 = copy.deepcopy(self.washer_in)
        self.w_in7 = copy.deepcopy(self.washer_in)
        self.w_in8 = copy.deepcopy(self.washer_in)

        self.nt1 = copy.deepcopy(self.nut)
        self.nt2 = copy.deepcopy(self.nut)
        self.nt3 = copy.deepcopy(self.nut)
        self.nt4 = copy.deepcopy(self.nut)

        self.nt5 = copy.deepcopy(self.nut)
        self.nt6 = copy.deepcopy(self.nut)
        self.nt7 = copy.deepcopy(self.nut)
        self.nt8 = copy.deepcopy(self.nut)

        self.nt9 = copy.deepcopy(self.nut)
        self.nt10 = copy.deepcopy(self.nut)
        self.nt11 = copy.deepcopy(self.nut)
        self.nt12 = copy.deepcopy(self.nut)

        self.nt_inflg1 = copy.deepcopy(self.nut_in)
        self.nt_inflg2 = copy.deepcopy(self.nut_in)

        self.nt_inflg3 = copy.deepcopy(self.nut_in)
        self.nt_inflg4 = copy.deepcopy(self.nut_in)

        self.nt_inflg5 = copy.deepcopy(self.nut_in)
        self.nt_inflg6 = copy.deepcopy(self.nut_in)
        self.nt_inflg7 = copy.deepcopy(self.nut_in)
        self.nt_inflg8 = copy.deepcopy(self.nut_in)
        # self.initBoltPlaceParam(plateObj)
        self.initBoltPlaceParam()

        self.bolts = []
        self.nuts = []

        self.positions = []

        self.models = []

        self.initialiseNutBolts()

    def initialiseNutBolts(self):
        """
        Initializing the Nut and Bolt
        :return:
        """
        pass


    def initBoltPlaceParam(self):
        self.enddist = self.BP.end_distance_out
        self.edgedist = self.BP.edge_distance_out
        # self.clearence = 50

        self.pitch = self.BP.bp_length_provided - 2 * self.enddist
        self.gauge = self.BP.bp_width_provided - 2 * self.edgedist

        self.pitch1 = self.BP.pitch_distance_out
        self.gauge1 = self.BP.gauge_distance_out

        if self.BP.load_axial_tension > 0 or self.BP.load_moment_minor > 0:
            self.enddist_in = self.BP.end_distance_in
            self.edgedist_in = self.BP.edge_distance_in
            if self.BP.anchors_inside_flange == 8:
                self.pitch_in = self.BP.pitch_distance_in
                self.gauge_in = self.BP.gauge_distance_in

        if self.BP.connectivity != 'Hollow/Tubular Column Base':
            if self.BP.stiffener_across_web != 'Yes':
                self.BP.stiffener_plt_thick_across_web = 0
            self.stiffener_inflg_thickness = self.BP.stiffener_plt_thick_across_web
            self.pitch_inflg = (self.BP.column_D - (2*self.BP.column_tf + 2*self.BP.column_r1 + self.stiffener_inflg_thickness))/4
            self.web_thick = self.BP.column_tw/2


    def calculatePositions(self):
        pass


    def place(self, origin, gaugeDir, pitchDir, boltDir):
        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir

        # self.calculatePositions()
        pos = self.origin
        pos1 = pos + self.edgedist * self.gaugeDir + self.enddist * self.pitchDir       #bottom left
        pos2 = pos1 + self.gauge * self.gaugeDir        #bottom right
        pos3 = pos2 + self.pitch * self.pitchDir        #top left
        pos4 = pos3 - self.gauge * self.gaugeDir        #top right



        self.ab1.place(pos1 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.ab2.place(pos2 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.ab3.place(pos3 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.ab4.place(pos4 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        self.nt1.place(pos1 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.nt2.place(pos2 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.nt3.place(pos3 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.nt4.place(pos4 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        self.w1.place(pos1 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.w2.place(pos2 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.w3.place(pos3 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
        self.w4.place(pos4 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        if 2*self.BP.anchors_outside_flange == 6 :
            pos5 = pos2 - self.gauge/2 * self.gaugeDir
            pos6 = pos4 + self.gauge/2 * self.gaugeDir

            self.ab5.place(pos5 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab6.place(pos6 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.nt5.place(pos5 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt6.place(pos6 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.w5.place(pos5 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w6.place(pos6 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        if 2*self.BP.anchors_outside_flange == 8:
            pos5 = pos1 + self.pitch1 * self.pitchDir
            pos6 = pos2 + self.pitch1 * self.pitchDir
            pos7 = pos3 - self.pitch1 * self.pitchDir
            pos8 = pos4 - self.pitch1 * self.pitchDir

            self.ab5.place(pos5 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab6.place(pos6 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab7.place(pos7 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab8.place(pos8 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.nt5.place(pos5 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt6.place(pos6 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt7.place(pos7 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt8.place(pos8 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.w5.place(pos5 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w6.place(pos6 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w7.place(pos7 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w8.place(pos8 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        if 2*self.BP.anchors_outside_flange == 12:
            pos5 = pos1 + self.pitch1 * self.pitchDir
            pos6 = pos2 + self.pitch1 * self.pitchDir
            pos7 = pos3 - self.pitch1 * self.pitchDir
            pos8 = pos4 - self.pitch1 * self.pitchDir

            pos9 = pos2 - self.gauge / 2 * self.gaugeDir
            pos10 = pos4 + self.gauge / 2 * self.gaugeDir
            pos11 = pos9 + self.pitch1 * self.pitchDir
            pos12 = pos10 - self.pitch1 * self.pitchDir

            self.ab5.place(pos5 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab6.place(pos6 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab7.place(pos7 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab8.place(pos8 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.ab9.place(pos9 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab10.place(pos10 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab11.place(pos11 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab12.place(pos12 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.nt5.place(pos5 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt6.place(pos6 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt7.place(pos7 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt8.place(pos8 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.nt9.place(pos9 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt10.place(pos10 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt11.place(pos11 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt12.place(pos12 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.w5.place(pos5 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w6.place(pos6 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w7.place(pos7 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w8.place(pos8 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.w9.place(pos9 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w10.place(pos10 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w11.place(pos11 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w12.place(pos12 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        if self.BP.anchors_inside_flange == 2:

            pos_inflg_1 = pos2 + self.pitch/2 * self.pitchDir + (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir
            pos_inflg_2 = pos4 - self.pitch/2 * self.pitchDir - (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir

            self.ab_inflg1.place(pos_inflg_1 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg2.place(pos_inflg_2 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.nt_inflg1.place(pos_inflg_1 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg2.place(pos_inflg_2 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.w_in1.place(pos_inflg_1 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in2.place(pos_inflg_2 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        if self.BP.anchors_inside_flange == 4:

            pos_inflg_1 = pos2 + self.pitch/2 * self.pitchDir - self.pitch_inflg * self.pitchDir + (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir
            pos_inflg_2 = pos4 - self.pitch/2 * self.pitchDir - self.pitch_inflg * self.pitchDir - (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir
            pos_inflg_3 = pos2 + self.pitch/2 * self.pitchDir + self.pitch_inflg * self.pitchDir + (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir
            pos_inflg_4 = pos4 - self.pitch/2 * self.pitchDir + self.pitch_inflg * self.pitchDir - (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir

            self.ab_inflg1.place(pos_inflg_1 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg2.place(pos_inflg_2 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg3.place(pos_inflg_3 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg4.place(pos_inflg_4 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.nt_inflg1.place(pos_inflg_1 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg2.place(pos_inflg_2 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg3.place(pos_inflg_3 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg4.place(pos_inflg_4 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.w_in1.place(pos_inflg_1 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in2.place(pos_inflg_2 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in3 .place(pos_inflg_3 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in4.place(pos_inflg_4 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

        if self.BP.anchors_inside_flange == 8:

            pos_inflg_1 = pos2 + self.pitch/2 * self.pitchDir - self.pitch_inflg * self.pitchDir + (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir
            pos_inflg_2 = pos4 - self.pitch/2 * self.pitchDir - self.pitch_inflg * self.pitchDir - (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir
            pos_inflg_3 = pos2 + self.pitch/2 * self.pitchDir + self.pitch_inflg * self.pitchDir + (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir
            pos_inflg_4 = pos4 - self.pitch/2 * self.pitchDir + self.pitch_inflg * self.pitchDir - (self.edgedist_in-self.gauge / 2 + self.web_thick) * self.gaugeDir

            pos_inflg_5 = pos2 + self.pitch / 2 * self.pitchDir - self.pitch_inflg * self.pitchDir + (self.edgedist_in - self.gauge / 2 + self.web_thick + self.gauge_in) * self.gaugeDir
            pos_inflg_6 = pos4 - self.pitch / 2 * self.pitchDir - self.pitch_inflg * self.pitchDir - (self.edgedist_in - self.gauge / 2 + self.web_thick + self.gauge_in) * self.gaugeDir
            pos_inflg_7 = pos2 + self.pitch / 2 * self.pitchDir + self.pitch_inflg * self.pitchDir + (self.edgedist_in - self.gauge / 2 + self.web_thick + self.gauge_in) * self.gaugeDir
            pos_inflg_8 = pos4 - self.pitch / 2 * self.pitchDir + self.pitch_inflg * self.pitchDir - (self.edgedist_in - self.gauge / 2 + self.web_thick + self.gauge_in) * self.gaugeDir

            self.ab_inflg1.place(pos_inflg_1 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg2.place(pos_inflg_2 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg3.place(pos_inflg_3 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg4.place(pos_inflg_4 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.ab_inflg5.place(pos_inflg_5 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg6.place(pos_inflg_6 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg7.place(pos_inflg_7 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.ab_inflg8.place(pos_inflg_8 - (self.bolt.ex) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.nt_inflg1.place(pos_inflg_1 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg2.place(pos_inflg_2 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg3.place(pos_inflg_3 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg4.place(pos_inflg_4 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.nt_inflg5.place(pos_inflg_5 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg6.place(pos_inflg_6 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg7.place(pos_inflg_7 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.nt_inflg8.place(pos_inflg_8 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.w_in1.place(pos_inflg_1 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in2.place(pos_inflg_2 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in3 .place(pos_inflg_3 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in4.place(pos_inflg_4 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)

            self.w_in5.place(pos_inflg_5 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in6.place(pos_inflg_6 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in7.place(pos_inflg_7 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)
            self.w_in8.place(pos_inflg_8 - (self.nt1.T + 50) * numpy.array([0, 0, 1.0]), gaugeDir, boltDir)



    def create_model(self):
        # for bolt in self.bolts:
        #     self.models.append(bolt.create_model())

        self.ab1Model = self.ab1.create_model()
        self.ab2Model = self.ab2.create_model()
        self.ab3Model = self.ab3.create_model()
        self.ab4Model = self.ab4.create_model()

        self.nt1Model = self.nt1.create_model()
        self.nt2Model = self.nt2.create_model()
        self.nt3Model = self.nt3.create_model()
        self.nt4Model = self.nt4.create_model()

        self.w1Model = self.w1.create_model()
        self.w2Model = self.w2.create_model()
        self.w3Model = self.w3.create_model()
        self.w4Model = self.w4.create_model()

        self.models = [self.ab1Model, self.ab2Model, self.ab3Model, self.ab4Model, self.nt1Model, self.nt2Model, self.nt3Model, self.nt4Model, self.w1Model, self.w2Model, self.w3Model, self.w4Model]

        if 2* self.BP.anchors_outside_flange == 6:
            self.ab5Model = self.ab5.create_model()
            self.ab6Model = self.ab6.create_model()

            self.nt5Model = self.nt5.create_model()
            self.nt6Model = self.nt6.create_model()

            self.w5Model = self.w5.create_model()
            self.w6Model = self.w6.create_model()

            models = [self.ab5Model, self.ab6Model,self.w5Model, self.w6Model, self.nt5Model, self.nt6Model]
            self.models.extend(models)

        if 2* self.BP.anchors_outside_flange == 8:
            self.ab5Model = self.ab5.create_model()
            self.ab6Model = self.ab6.create_model()
            self.ab7Model = self.ab7.create_model()
            self.ab8Model = self.ab8.create_model()

            self.nt5Model = self.nt5.create_model()
            self.nt6Model = self.nt6.create_model()
            self.nt7Model = self.nt7.create_model()
            self.nt8Model = self.nt8.create_model()

            self.w5Model = self.w5.create_model()
            self.w6Model = self.w6.create_model()
            self.w7Model = self.w7.create_model()
            self.w8Model = self.w8.create_model()

            models = [self.ab5Model, self.ab6Model, self.ab7Model, self.ab8Model, self.w5Model, self.w6Model, self.w7Model, self.w8Model, self.nt5Model, self.nt6Model, self.nt7Model, self.nt8Model]
            self.models.extend(models)

        if 2* self.BP.anchors_outside_flange == 12:
            self.ab5Model = self.ab5.create_model()
            self.ab6Model = self.ab6.create_model()
            self.ab7Model = self.ab7.create_model()
            self.ab8Model = self.ab8.create_model()

            self.ab9Model = self.ab9.create_model()
            self.ab10Model = self.ab10.create_model()
            self.ab11Model = self.ab11.create_model()
            self.ab12Model = self.ab12.create_model()

            self.nt5Model = self.nt5.create_model()
            self.nt6Model = self.nt6.create_model()
            self.nt7Model = self.nt7.create_model()
            self.nt8Model = self.nt8.create_model()

            self.nt9Model = self.nt9.create_model()
            self.nt10Model = self.nt10.create_model()
            self.nt11Model = self.nt11.create_model()
            self.nt12Model = self.nt12.create_model()

            self.w5Model = self.w5.create_model()
            self.w6Model = self.w6.create_model()
            self.w7Model = self.w7.create_model()
            self.w8Model = self.w8.create_model()

            self.w9Model = self.w9.create_model()
            self.w10Model = self.w10.create_model()
            self.w11Model = self.w11.create_model()
            self.w12Model = self.w12.create_model()

            models = [self.ab5Model, self.ab6Model, self.ab7Model, self.ab8Model, self.ab9Model, self.ab10Model, self.ab11Model, self.ab12Model,
                      self.nt5Model, self.nt6Model, self.nt7Model, self.nt8Model, self.nt9Model, self.nt10Model, self.nt11Model, self.nt12Model,
                      self.w5Model, self.w6Model, self.w7Model, self.w8Model, self.w9Model, self.w10Model, self.w11Model, self.w12Model]
            self.models.extend(models)

        if self.BP.anchors_inside_flange == 2:
            self.ab_inflg1Model = self.ab_inflg1.create_model()
            self.ab_inflg2Model = self.ab_inflg2.create_model()
            self.nt_inflg1Model = self.nt_inflg1.create_model()
            self.nt_inflg2Model = self.nt_inflg2.create_model()

            self.w_in1Model = self.w_in1.create_model()
            self.w_in2Model = self.w_in2.create_model()

            models = [ self.ab_inflg1Model, self.ab_inflg2Model, self.w_in1Model, self.w_in2Model, self.nt_inflg1Model, self.nt_inflg2Model]
            self.models.extend(models)

        if self.BP.anchors_inside_flange == 4:
            self.ab_inflg1Model = self.ab_inflg1.create_model()
            self.ab_inflg2Model = self.ab_inflg2.create_model()
            self.nt_inflg1Model = self.nt_inflg1.create_model()
            self.nt_inflg2Model = self.nt_inflg2.create_model()
            self.w_in1Model = self.w_in1.create_model()
            self.w_in2Model = self.w_in2.create_model()

            self.ab_inflg3Model = self.ab_inflg3.create_model()
            self.ab_inflg4Model = self.ab_inflg4.create_model()
            self.nt_inflg3Model = self.nt_inflg3.create_model()
            self.nt_inflg4Model = self.nt_inflg4.create_model()
            self.w_in3Model = self.w_in3.create_model()
            self.w_in4Model = self.w_in4.create_model()

            models = [ self.ab_inflg1Model, self.ab_inflg2Model, self.ab_inflg3Model, self.ab_inflg4Model,
                       self.nt_inflg1Model, self.nt_inflg2Model, self.nt_inflg3Model, self.nt_inflg4Model,
                       self.w_in1Model, self.w_in2Model, self.w_in3Model, self.w_in4Model]
            self.models.extend(models)

        if self.BP.anchors_inside_flange == 8:
            self.ab_inflg1Model = self.ab_inflg1.create_model()
            self.ab_inflg2Model = self.ab_inflg2.create_model()
            self.nt_inflg1Model = self.nt_inflg1.create_model()
            self.nt_inflg2Model = self.nt_inflg2.create_model()
            self.w_in1Model = self.w_in1.create_model()
            self.w_in2Model = self.w_in2.create_model()

            self.ab_inflg5Model = self.ab_inflg5.create_model()
            self.ab_inflg6Model = self.ab_inflg6.create_model()
            self.nt_inflg5Model = self.nt_inflg5.create_model()
            self.nt_inflg6Model = self.nt_inflg6.create_model()
            self.w_in5Model = self.w_in5.create_model()
            self.w_in6Model = self.w_in6.create_model()

            self.ab_inflg3Model = self.ab_inflg3.create_model()
            self.ab_inflg4Model = self.ab_inflg4.create_model()
            self.nt_inflg3Model = self.nt_inflg3.create_model()
            self.nt_inflg4Model = self.nt_inflg4.create_model()
            self.w_in3Model = self.w_in3.create_model()
            self.w_in4Model = self.w_in4.create_model()

            self.ab_inflg7Model = self.ab_inflg7.create_model()
            self.ab_inflg8Model = self.ab_inflg8.create_model()
            self.nt_inflg7Model = self.nt_inflg7.create_model()
            self.nt_inflg8Model = self.nt_inflg8.create_model()
            self.w_in7Model = self.w_in7.create_model()
            self.w_in8Model = self.w_in8.create_model()

            models = [ self.ab_inflg1Model, self.ab_inflg2Model, self.ab_inflg3Model, self.ab_inflg4Model,
                       self.ab_inflg5Model, self.ab_inflg6Model, self.ab_inflg7Model, self.ab_inflg8Model,
                       self.nt_inflg1Model, self.nt_inflg2Model, self.nt_inflg3Model, self.nt_inflg4Model,
                       self.nt_inflg5Model, self.nt_inflg6Model, self.nt_inflg7Model, self.nt_inflg8Model,
                       self.w_in1Model, self.w_in2Model, self.w_in3Model, self.w_in4Model,
                       self.w_in5Model, self.w_in6Model, self.w_in7Model, self.w_in8Model
                       ]
            self.models.extend(models)


    def get_models(self):
        return self.models


if __name__ == '__main__':

    from cad.items.anchor_bolt import *
    from cad.items.nut import Nut
    from cad.items.ISection import ISection
    from cad.items.plate import Plate

    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    nutboltArrayOrigin = numpy.array([0., 0., 0.])
    gaugeDir = numpy.array([1.0, 0, 0])
    pitchDir = numpy.array([0, 1.0, 0])
    boltDir = numpy.array([0, 0, 1.0])

    numberOfBolts = 6
    column = ISection(B=250, T=13.7, D=450, t=9.8, R1=14.0, R2=7.0, alpha=94, length=1500, notchObj=None)
    baseplate = Plate(L=700, W=500, T=30)

    l = 550
    c = 225
    a = 175
    r = 24
    ex_length = (50 + 24 + baseplate.T)  # nut.T = 24
    bolt = AnchorBolt_A(l=250, c=125, a=75, r=12, ex=ex_length)
    # bolt = AnchorBolt_B(l= 250, c= 125, a= 75, r= 12)
    # bolt = AnchorBolt_Endplate(l= 250, c= 125, a= 75, r= 12)

    nut = Nut(R=bolt.r * 3, T=24, H=30, innerR1=bolt.r)

    nutSpace = bolt.c + baseplate.T

    nut_bolt_array = NutBoltArray(column, baseplate, nut, bolt, numberOfBolts, nutSpace)

    place = nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    nut_bolt_array_Model = nut_bolt_array.create_model()

    nut_bolts = nut_bolt_array.get_models()
    array = nut_bolts[0]
    for comp in nut_bolts:
        array = BRepAlgoAPI_Fuse(comp, array).Shape()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")
    display.DisplayShape(array, update=True)
    display.DisableAntiAliasing()
    start_display()

