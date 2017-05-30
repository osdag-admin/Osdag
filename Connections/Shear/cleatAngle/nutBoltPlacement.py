'''
Created on 07-Jun-2015

@author: deepa
'''
import numpy
from bolt import Bolt
from nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from ModelUtils import get_gp_pt
import copy


class NutBoltArray():
    def __init__(self, bolt_place_obj, nut, bolt, nut_space, cnut_space):
        self.origin = None
        self.gauge_dir = None
        self.pitch_dir = None
        self.bolt_dir = None
        
        #################################
        self.c_origin = None
        self.c_origin1 = None
        self.c_gauge_dir = None
        self.c_pitch_dir = None
        self.c_bolt_dir = None
        ############################################
        
        self.init_bolt_place_params(bolt_place_obj)
        
        self.bolt = bolt
        self.nut = nut
        #self.gap = gap
        self.gap = nut_space
        
        self.bolts = []
        self.nuts = []
        
        self.positions = []
        ######################
        #self.cGap = cgap
        self.cGap = cnut_space
        self.cBolts = []
        self.cNuts = []
        self.cBolts1 = []
        self.cNuts1 = []
        ##################################
        # self.calculate_positions()
        self.initialise_nut_bolts()
        
        self.models = []
        
    def initialise_nut_bolts(self):
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            bolt_len_required = float(b.T + self.gap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))
    # Newly added
        for i in range(self.cRow * self.cCol):
            bolt_len_required = float(b.T + self.cGap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.cBolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.cNuts.append(Nut(n.R, n.T, n.H, n.r1))
        for i in range(self.cRow * self.cCol):
            bolt_len_required = float(b.T + self.cGap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.cBolts1.append(Bolt(b.R, b.T, b.H, b.r))
            self.cNuts1.append(Nut(n.R, n.T, n.H, n.r1))
        
    def init_bolt_place_params(self, bolt_place_obj):
        self.pitch = bolt_place_obj['Bolt']['pitch']
        self.gauge = bolt_place_obj['Bolt']['gauge']
        self.edge = bolt_place_obj['Bolt']['edge']
        self.end = bolt_place_obj['Bolt']['enddist']
        self.row = bolt_place_obj['Bolt']['numofrow']
        self.col = bolt_place_obj['Bolt']['numofcol']

# ########changes have been made after 3d is integreted with main files####
        
        self.cPitch = bolt_place_obj['cleat']['pitch']
        self.cGauge = bolt_place_obj['cleat']['guage']
        self.cEdge = bolt_place_obj['cleat']['edge']
        self.cEnd = bolt_place_obj['cleat']['end']
        
        self.cRow = bolt_place_obj['cleat']['numofrow']
        self.cCol = bolt_place_obj['cleat']['numofcol']
    
        self.leg = bolt_place_obj['cleat']['legsize']
         
    def calculate_positions(self):
        self.positions = []
        for rw in range(self.row):
            for col in range(self.col):
                pos = self.origin 
                pos = pos + self.end * self.gauge_dir
                pos = pos + col * self.gauge * self.gauge_dir
                pos = pos + self.edge * self.pitch_dir
                pos = pos + rw * self.pitch * self.pitch_dir
                
                self.positions.append(pos)
# ###############Newly added######################
        self.cPositions = []
        for rw in range(self.cRow):
            for col in range(self.cCol):
                pos = self.c_origin
                pos = pos + self.cEnd * self.c_gauge_dir
                pos = pos + (col * self.cGauge * self.c_gauge_dir)
                pos = pos + self.cEdge * self.c_pitch_dir
                pos = pos + rw * self.cPitch * self.c_pitch_dir
                
                self.cPositions.append(pos)
        self.cPositions1 = []
        for rw in range(self.cRow):
            for col in range(self.cCol):
                pos = self.c_origin1
                pos = pos + ((self.leg - self.cEnd) * self.c_gauge_dir)
                pos = pos - col * self.cGauge * self.c_gauge_dir
                pos = pos - self.cEdge * self.c_pitch_dir
                pos = pos - rw * self.cPitch * self.c_pitch_dir
                
                self.cPositions1.append(pos)
    
    def place(self, origin, gauge_dir, pitch_dir, bolt_dir, c_origin, c_gauge_dir, c_pitch_dir, c_bolt_dir, c_origin1, c_gauge_dir1, c_pitch_dir1, c_bolt_dir1):
        self.origin = origin
        self.gauge_dir = gauge_dir
        self.pitch_dir = pitch_dir
        self.bolt_dir = bolt_dir
# ###############Newly added####################
        self.c_origin = c_origin
        self.c_gauge_dir = c_gauge_dir
        self.c_pitch_dir = c_pitch_dir
        self.c_bolt_dir = c_bolt_dir
        
        self.c_origin1 = c_origin1
        self.c_gauge_dir1 = c_gauge_dir1
        self.c_pitch_dir1 = c_pitch_dir1
        self.c_bolt_dir1 = c_bolt_dir1
        
        ################################################
        
        self.calculate_positions()
        for index, pos in enumerate(self.positions):
            self.bolts[index].place(pos, gauge_dir, bolt_dir)
            self.nuts[index].place((pos + self.gap * bolt_dir), gauge_dir, -bolt_dir)
# ###############Newly added####################
        for index, pos in enumerate(self.cPositions):
            self.cBolts[index].place(pos, c_gauge_dir, c_bolt_dir)
            self.cNuts[index].place((pos + self.cGap * c_bolt_dir), c_gauge_dir, -c_bolt_dir)
        for index, pos in enumerate(self.cPositions1):
            self.cBolts1[index].place(pos, c_gauge_dir1, c_bolt_dir1)
            self.cNuts1[index].place((pos + self.cGap * c_bolt_dir1), c_gauge_dir1, -c_bolt_dir1)
            
    def create_model(self):
        for bolt in self.bolts:
            self.models.append(bolt.create_model())
        
        for nut in self.nuts:
            self.models.append(nut.create_model())
        #########################################
        for bolt in self.cBolts:
            self.models.append(bolt.create_model())
        
        for nut in self.cNuts:
            self.models.append(nut.create_model())
        for bolt in self.cBolts1:
            self.models.append(bolt.create_model())
        
        for nut in self.cNuts1:
            self.models.append(nut.create_model())
# ################################################################
        dbg = self.dbg_sphere(self.origin)
        self.models.append(dbg)
        #########################################################################
        dbg1 = self.dbg_sphere(self.c_origin)
        self.models.append(dbg1)
        dbg2 = self.dbg_sphere(self.c_origin1)
        self.models.append(dbg2)
            
    def dbg_sphere(self, pt):
        return BRepPrimAPI_MakeSphere(get_gp_pt(pt), 0.1).Shape()
        
    def get_models(self):
        return self.models

    def get_beambolts(self):
        self.beambolts = []
        for bolt in self.bolts:
            self.beambolts.append(bolt.create_model())
            dbg = self.dbg_sphere(self.origin)
            self.beambolts.append(dbg)
        return self.beambolts


    def get_colbolts(self):
        self.colbolts =[]
        for bolt in self.cBolts:
            self.colbolts.append(bolt.create_model())
        for bolt in self.cBolts1:
            self.colbolts.append(bolt.create_model())
            dbg1 = self.dbg_sphere(self.c_origin)
            self.colbolts.append(dbg1)
            dbg2 = self.dbg_sphere(self.c_origin1)
            self.colbolts.append(dbg2)
        return self.colbolts