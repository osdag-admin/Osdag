'''
Created on 07-Jun-2015

@author: deepa
'''
from Connections.Component.bolt import Bolt
from Connections.Component.nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from ModelUtils import get_gp_pt


class NutBoltArray():
    def __init__(self, bolt_place_obj, nut, bolt, nut_space):
        self.origin = None
        self.origin1 = None
        self.gauge_dir = None
        self.pitch_dir = None
        self.bolt_dir = None
        
        self.init_bolt_place_params(bolt_place_obj)
        
        self.bolt = bolt
        self.nut = nut
        self.gap = nut_space
        
        self.bolts = []
        self.nuts = []
        self.bolts1 = []
        self.nuts1 = []
        self.initialise_nut_bolts()
        
        self.positions = []
        self.positions1 = []
        # self.calculate_positions()
        
        self.models = []
        
    def initialise_nut_bolts(self):
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            bolt_len_required = float(b.T + self.gap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))
        for i in range(self.row * self.col):
            bolt_len_required = float(b.T + self.gap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.bolts1.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts1.append(Nut(n.R, n.T, n.H, n.r1))
        
    def init_bolt_place_params(self, bolt_place_obj):
        self.pitch = bolt_place_obj['Bolt']['pitch']
        self.gauge = bolt_place_obj['Bolt']['gauge']
        self.edge = bolt_place_obj['Bolt']['edge']
        self.end = bolt_place_obj['Bolt']['enddist']
        self.row = bolt_place_obj['Bolt']['numofrow']
        self.col = bolt_place_obj['Bolt']['numofcol']
        self.sectional_gauge = bolt_place_obj['Plate']['Sectional Gauge']
        self.col = int(self.col / 2)
        # self.row = 3
        # self.col = 2
         
    def calculate_positions(self):
        self.positions = []
        for rw in range(self.row):
            for col in range(self.col):
                pos = self.origin 
                pos = pos + (self.edge) * self.gauge_dir
                pos = pos + col * self.gauge * self.gauge_dir
                pos = pos + self.end * self.pitch_dir
                pos = pos + rw * self.pitch * self.pitch_dir
                
                self.positions.append(pos)
        self.positions1 = []        
        for rw in range(self.row):
            for col in range(self.col):
                pos = self.origin1 
                pos = pos - (self.edge) * self.gauge_dir
                pos = pos - col * self.gauge * self.gauge_dir
                pos = pos + self.end * self.pitch_dir
                pos = pos + rw * self.pitch * self.pitch_dir
                
                self.positions1.append(pos)
    
    def place(self, origin, origin1, gauge_dir, pitch_dir, bolt_dir):
        self.origin = origin
        self.origin1 = origin1
        self.gauge_dir = gauge_dir
        self.pitch_dir = pitch_dir
        self.bolt_dir = bolt_dir
        
        self.calculate_positions()
        
        for index, pos in enumerate(self.positions):
            self.bolts[index].place(pos, gauge_dir, bolt_dir)
            self.nuts[index].place((pos + self.gap * bolt_dir), gauge_dir, -bolt_dir)
        for index, pos in enumerate(self.positions1):
            self.bolts1[index].place(pos, gauge_dir, bolt_dir)
            self.nuts1[index].place((pos + self.gap * bolt_dir), gauge_dir, -bolt_dir)

    def create_model(self):
        for bolt in self.bolts:
            self.models.append(bolt.create_model())
        
        for nut in self.nuts:
            self.models.append(nut.create_model())
            
        dbg = self.dbg_sphere(self.origin)
        self.models.append(dbg)
        
        for bolt in self.bolts1:
            self.models.append(bolt.create_model())
        
        for nut in self.nuts1:
            self.models.append(nut.create_model())
            
        dbg1 = self.dbg_sphere(self.origin1)
        self.models.append(dbg1)
            
    def dbg_sphere(self, pt):
        return BRepPrimAPI_MakeSphere(get_gp_pt(pt), 0.1).Shape()
        
    def get_models(self):
        return self.models   
    
    def get_bolt_list(self):
        boltlist = []
        for bolt in self.bolts:
            boltlist.append(bolt.create_model())
            dbg = self.dbg_sphere(self.origin)
            self.models.append(dbg)
        for bolt in self.bolts1:
            boltlist.append(bolt.create_model())
            dbg = self.dbg_sphere(self.origin1)
            self.models.append(dbg)
        return boltlist