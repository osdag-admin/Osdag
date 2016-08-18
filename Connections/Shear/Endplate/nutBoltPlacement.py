'''
Created on 07-Jun-2015

@author: deepa
'''
import numpy
from bolt import Bolt
from nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from ModelUtils import getGpPt

class NutBoltArray():
    def __init__(self,boltPlaceObj,nut,bolt,gap):
        self.origin = None
        self.origin1 = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir =  None
        
        self.initBoltPlaceParams(boltPlaceObj)
        
        self.bolt = bolt
        self.nut = nut
        self.gap = gap
        
        self.bolts = []
        self.nuts = []
        self.bolts1 = []
        self.nuts1 = []
        self.initialiseNutBolts()
        
        self.positions = []
        self.positions1 = []
        #self.calculatePositions()
        
        self.models = []
        
    def initialiseNutBolts(self):
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            self.bolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T,n.H, n.r1))
        for i in range(self.row * self.col):
            self.bolts1.append(Bolt(b.R,b.T, b.H, b.r))
            self.nuts1.append(Nut(n.R, n.T,n.H, n.r1))
        
    def initBoltPlaceParams(self,boltPlaceObj):
        self.pitch = boltPlaceObj['Bolt']['pitch']
        self.gauge = boltPlaceObj['Bolt']['gauge']
        self.edge = boltPlaceObj['Bolt']['edge']
        self.end = boltPlaceObj['Bolt']['enddist']
        self.row = boltPlaceObj['Bolt']['numofrow']
        self.col = boltPlaceObj['Bolt']['numofcol']
        self.sectional_gauge = boltPlaceObj['Plate']['Sectional Gauge']
        self.col = int(self.col/2)
        #self.row = 3
        #self.col = 2
         
    def calculatePositions(self):
        self.positions = []
        for rw in  range(self.row):
            for col in range(self.col):
                pos = self.origin 
                pos = pos + (self.edge) * self.gaugeDir
                pos = pos + col * self.gauge * self.gaugeDir 
                pos = pos + self.end * self.pitchDir 
                pos = pos + rw * self.pitch * self.pitchDir
                
                self.positions.append(pos)
        self.positions1 = []        
        for rw in  range(self.row):
            for col in range(self.col):
                pos = self.origin1 
                pos = pos - (self.edge) * self.gaugeDir
                pos = pos - col * self.gauge * self.gaugeDir 
                pos = pos + self.end * self.pitchDir 
                pos = pos + rw * self.pitch * self.pitchDir
                
                self.positions1.append(pos)
    
    def place(self, origin,origin1, gaugeDir, pitchDir, boltDir):
        self.origin = origin
        self.origin1 = origin1
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir
        
        self.calculatePositions()
        
        for index, pos in enumerate (self.positions):
            self.bolts[index].place(pos, gaugeDir, boltDir)
            self.nuts[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)
        for index, pos in enumerate (self.positions1):
            self.bolts1[index].place(pos, gaugeDir, boltDir)
            self.nuts1[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)
    
        
    def createModel(self):
        for bolt in self.bolts:
            self.models.append(bolt.createModel())        
        
        for nut in self.nuts:
            self.models.append(nut.createModel())
            
        dbg = self.dbgSphere(self.origin)
        self.models.append(dbg)
        
        for bolt in self.bolts1:
            self.models.append(bolt.createModel())        
        
        for nut in self.nuts1:
            self.models.append(nut.createModel())
            
        dbg1 = self.dbgSphere(self.origin1)
        self.models.append(dbg1)
            
    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()
        
    def getModels(self): 
        return self.models   
        
        