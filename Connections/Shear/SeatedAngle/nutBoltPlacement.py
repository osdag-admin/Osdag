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
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir =  None
        
        self.borigin = None
        self.bgaugeDir = None
        self.bpitchDir = None
        self.bboltDir =  None
        
        self.topcliporigin = None
        self.topclipgaugeDir = None
        self.topclippitchDir = None
        self.topclipboltDir =  None
        
        self.topclipborigin = None
        self.topclipbgaugeDir = None
        self.topclipbpitchDir = None
        self.topclipbboltDir =  None
        
        self.initBoltPlaceParams(boltPlaceObj)
        
        self.bolt = bolt
        self.nut = nut
        self.gap = gap
         
        self.bolts = []
        self.nuts = []
        self.bbolts =[]
        self.bnuts = []
        self.topclipbolts = []
        self.topclipnuts = []
        self.topclipbbolts =[]
        self.topclipbnuts = []
        self.initialiseNutBolts()
        
        
        self.positions = []
        self.bpositions = []
        self.topclippositions = []
        self.topclipbpositions = []
        #self.calculatePositions()
        
        self.models = []
        
    def initialiseNutBolts(self):
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            self.bolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T,n.H, n.r1))
        
        for i in range(self.brow * self.bcol):
            self.bbolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.bnuts.append(Nut(n.R, n.T,n.H, n.r1))
            
        for i in range(self.topcliprow * self.topclipcol):
            self.topclipbolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.topclipnuts.append(Nut(n.R, n.T,n.H, n.r1))
        
        for i in range(self.topclipbrow * self.topclipbcol):
            self.topclipbbolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.topclipbnuts.append(Nut(n.R, n.T,n.H, n.r1))
        
    def initBoltPlaceParams(self,boltPlaceObj):
        self.pitch = boltPlaceObj['Bolt']["Pitch Distance (mm)"]
        self.gauge = boltPlaceObj['Bolt']["Guage Distance (mm)"]
        #self.gauge = 30
        self.edge = boltPlaceObj['Bolt']["Edge Distance (mm)"]
        self.end = boltPlaceObj['Bolt']["End Distance (mm)"]
        self.row = boltPlaceObj['Bolt']["No.Of Row"]
        self.col = boltPlaceObj['Bolt']["No.Of Column"]
        self.brow = 1
        self.bcol= 2
        
        self.topcliprow = 1
        self.topclipcol= 2
        self.topclipbrow = 1
        self.topclipbcol= 2
        #self.row = 3
        #self.col = 2
         
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
        
    
    def calculatebPositions(self):       
        self.bpositions = []
        for rw in  range(self.brow):
            for col in range(self.bcol):
                pos = self.borigin 
                pos = pos + self.end * self.bgaugeDir
                pos = pos + col * self.gauge * self.bgaugeDir 
                pos = pos + self.edge * self.bpitchDir 
                pos = pos + rw * self.pitch * self.bpitchDir
                
                self.bpositions.append(pos)
    
    
    def calculatetopclipPositions(self):
        self.topclippositions = []
        for rw in  range(self.topcliprow):
            for col in range(self.topclipcol):
                pos = self.topcliporigin 
                pos = pos + self.end * self.topclipgaugeDir
                pos = pos + col * self.gauge * self.topclipgaugeDir 
                pos = pos + self.edge * self.topclippitchDir 
                pos = pos + rw * self.pitch * self.topclippitchDir
                
                self.topclippositions.append(pos)
        
    
    def calculatetopclipbPositions(self):       
        self.topclipbpositions = []
        for rw in  range(self.topclipbrow):
            for col in range(self.topclipbcol):
                pos = self.topclipborigin 
                pos = pos + self.end * self.topclipbgaugeDir
                pos = pos + col * self.gauge * self.topclipbgaugeDir 
                pos = pos + self.edge * self.topclipbpitchDir 
                pos = pos + rw * self.pitch * self.topclipbpitchDir
                
                self.topclipbpositions.append(pos)
    
    
    def place(self, origin, gaugeDir, pitchDir, boltDir,borigin,bgaugeDir,bpitchDir,bboltDir, topcliporigin,topclipgaugeDir, topclippitchDir, topclipboltDir,topclipborigin,topclipbgaugeDir,topclipbpitchDir,topclipbboltDir):
        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir
                
        self.calculatePositions()
        
        for index, pos in enumerate (self.positions):
            self.bolts[index].place(pos, gaugeDir, boltDir)
            self.nuts[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)
        
        self.borigin = borigin
        self.bgaugeDir = bgaugeDir
        self.bpitchDir = bpitchDir
        self.bboltDir = bboltDir
        
        self.calculatebPositions()
        
        for index, pos in enumerate (self.bpositions):
            self.bbolts[index].place(pos, bgaugeDir, bboltDir)
            self.bnuts[index].place((pos + self.gap * bboltDir), bgaugeDir, -bboltDir)
        
        self.topcliporigin = topcliporigin
        self.topclipgaugeDir = topclipgaugeDir
        self.topclippitchDir = topclippitchDir
        self.topclipboltDir = topclipboltDir
                
        self.calculatetopclipPositions()
        
        for index, pos in enumerate (self.topclippositions):
            self.topclipbolts[index].place(pos, topclipgaugeDir, topclipboltDir)
            self.topclipnuts[index].place((pos + self.gap * topclipboltDir), topclipgaugeDir, -topclipboltDir)
        
        self.topclipborigin = topclipborigin
        self.topclipbgaugeDir = topclipbgaugeDir
        self.topclipbpitchDir = topclipbpitchDir
        self.topclipbboltDir = topclipbboltDir
        
        self.calculatetopclipbPositions()
        
        for index, pos in enumerate (self.topclipbpositions):
            self.topclipbbolts[index].place(pos, topclipbgaugeDir, topclipbboltDir)
            self.topclipbnuts[index].place((pos + self.gap * topclipbboltDir), topclipbgaugeDir, -topclipbboltDir)
    
        
    def createModel(self):
        for bolt in self.bolts:
            self.models.append(bolt.createModel())        
        
        for nut in self.nuts:
            self.models.append(nut.createModel())
            
        dbg = self.dbgSphere(self.origin)
        self.models.append(dbg)
        
        for bolt in self.bbolts:
            self.models.append(bolt.createModel())        
        
        for nut in self.bnuts:
            self.models.append(nut.createModel())
            
        dbg = self.dbgSphere(self.borigin)
        self.models.append(dbg)
        
        for bolt in self.topclipbolts:
            self.models.append(bolt.createModel())        
        
        for nut in self.topclipnuts:
            self.models.append(nut.createModel())
            
        dbg = self.dbgSphere(self.topcliporigin)
        self.models.append(dbg)
        
        for bolt in self.topclipbbolts:
            self.models.append(bolt.createModel())        
        
        for nut in self.topclipbnuts:
            self.models.append(nut.createModel())
            
        dbg = self.dbgSphere(self.topclipborigin)
        self.models.append(dbg)
            
    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()
        
    def getModels(self): 
        return self.models   
        
        