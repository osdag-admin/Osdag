'''
Created on 07-Jun-2015

@author: deepa
'''
import numpy
from bolt import Bolt
from nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from ModelUtils import getGpPt
import copy

class NutBoltArray():
    def __init__(self,boltPlaceObj,nut,bolt,gap,cgap):
        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir =  None
        
        #################################
        self.cOrigin = None
        self.cOrigin1 = None
        self.cGaugeDir = None
        self.cPitchDir = None
        self.cBoltDir =  None
        ############################################
        
        self.initBoltPlaceParams(boltPlaceObj)
        
        self.bolt = bolt
        self.nut = nut
        self.gap = gap
        
        self.bolts = []
        self.nuts = []
        
        self.positions = []
        ######################
        self.cGap = cgap
        self.cBolts = []
        self.cNuts = []
        self.cBolts1 = []
        self.cNuts1 = []
        ##################################
        #self.calculatePositions()
        self.initialiseNutBolts()
        
        self.models = []
        
    def initialiseNutBolts(self):
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            self.bolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T,n.H, n.r1))
    #Newly added
        for i in range(self.cRow * self.cCol):
            self.cBolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.cNuts.append(Nut(n.R, n.T,n.H, n.r1))
        for i in range(self.cRow * self.cCol):
            self.cBolts1.append(Bolt(b.R,b.T, b.H, b.r))
            self.cNuts1.append(Nut(n.R, n.T,n.H, n.r1))
        
    def initBoltPlaceParams(self,boltPlaceObj):
        self.pitch = boltPlaceObj['Bolt']['pitch']
        self.gauge = boltPlaceObj['Bolt']['gauge']
        self.edge = boltPlaceObj['Bolt']['edge']
        self.end = boltPlaceObj['Bolt']['enddist']
        self.row = boltPlaceObj['Bolt']['numofrow']
        self.col = boltPlaceObj['Bolt']['numofcol']
        #########changes have been made after 3d is integreted with main files####
        
        self.cPitch = boltPlaceObj['cleat']['pitch']
        self.cGauge = boltPlaceObj['cleat']['guage']
        self.cEdge = boltPlaceObj['cleat']['edge']
        self.cEnd = boltPlaceObj['cleat']['end']
        
        self.cRow = boltPlaceObj['cleat']['numofrow']
        self.cCol = boltPlaceObj['cleat']['numofcol']
         
    def calculatePositions(self):
        self.positions = []
        for rw in  range(self.row):
            for col in range(self.col):
                pos = self.origin 
                pos = pos + self.end * self.gaugeDir
                pos = pos + col * self.gauge * self.gaugeDir 
                pos = pos + self.edge * self.pitchDir 
                pos = pos + rw * self.pitch * self.pitchDir
                
                self.positions.append(pos)
        ################Newly added######################
        self.cPositions = []
        for rw in  range(self.cRow):
            for col in range(self.cCol):
                pos = self.cOrigin 
                pos = pos + self.cEnd * self.cGaugeDir
                pos = pos + col * self.cGauge * self.cGaugeDir 
                pos = pos + self.cEdge * self.cPitchDir 
                pos = pos + rw * self.cPitch * self.cPitchDir
                
                self.cPositions.append(pos)
        self.cPositions1 = []
        for rw in  range(self.cRow):
            for col in range(self.cCol):
                pos = self.cOrigin1 
                pos = pos + self.cEnd * self.cGaugeDir
                pos = pos + col * self.cGauge * self.cGaugeDir 
                pos = pos + self.cEdge * self.cPitchDir 
                pos = pos + rw * self.cPitch * self.cPitchDir
                
                self.cPositions1.append(pos)
        
    
    def place(self, origin, gaugeDir, pitchDir, boltDir, cOrigin, cGaugeDir, cPitchDir, cBoltDir, cOrigin1, cGaugeDir1, cPitchDir1, cBoltDir1):
        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir
        ################Newly added####################
        self.cOrigin = cOrigin
        self.cGaugeDir = cGaugeDir
        self.cPitchDir = cPitchDir
        self.cBoltDir =  cBoltDir
        
        self.cOrigin1 = cOrigin1
        self.cGaugeDir1 = cGaugeDir1
        self.cPitchDir1 = cPitchDir1
        self.cBoltDir1 =  cBoltDir1
        
        ################################################
        
        self.calculatePositions()
        for index, pos in enumerate (self.positions):
            self.bolts[index].place(pos, gaugeDir, boltDir)
            self.nuts[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)
        ################Newly added####################
        for index, pos in enumerate (self.cPositions):
            self.cBolts[index].place(pos, cGaugeDir, cBoltDir)
            self.cNuts[index].place((pos + self.cGap * cBoltDir), cGaugeDir, -cBoltDir)
        for index, pos in enumerate (self.cPositions1):
            self.cBolts1[index].place(pos, cGaugeDir1, cBoltDir1)
            self.cNuts1[index].place((pos + self.cGap * cBoltDir1), cGaugeDir1, -cBoltDir1)
            
    def createModel(self):
        for bolt in self.bolts:
            self.models.append(bolt.createModel())        
        
        for nut in self.nuts:
            self.models.append(nut.createModel())
        #########################################
        for bolt in self.cBolts:
            self.models.append(bolt.createModel())        
        
        for nut in self.cNuts:
            self.models.append(nut.createModel())
        for bolt in self.cBolts1:
            self.models.append(bolt.createModel())        
        
        for nut in self.cNuts1:
            self.models.append(nut.createModel())
        #################################################################   
        dbg = self.dbgSphere(self.origin)
        self.models.append(dbg)
        #########################################################################
        dbg1 = self.dbgSphere(self.cOrigin)
        self.models.append(dbg1)
        dbg2 = self.dbgSphere(self.cOrigin1)
        self.models.append(dbg2)
            
    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()
        
    def getModels(self): 
        return self.models   
        
        