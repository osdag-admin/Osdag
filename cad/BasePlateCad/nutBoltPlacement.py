'''
Created on 19-March-2020

@author : Anand Swaroop
'''

from cad.items.anchor_bolt import *
from cad.items.nut import Nut
from OCC.Core.BRepAlgoAPI import BrepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt


class NutBoltArray():
    """
    add a diagram here
    """

    def __init__(self, boltplaceObj, plateObj, nut, bolt, nut_space):
        self.boltplaceObj = boltplaceObj
        self.plateObj = plateObj
        self.nut = nut
        self.bolt = bolt
        self.gap = nut_space

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.initBoltPlaceParam(plateObj)

        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()

        self.position = []

        self.models = []

    def initialiseNutBolts(self):
        """
        Initializing the Nut and Bolt
        :return:
        """
        b =  self.bolt
        n = self.nut
        for i in range(self.row*self.col):
            bolt_len_required = flot(b.T + self.gap)
            b.H = bolt_len_required + (5-bolt_len_required) % 5 #Todo : enter the length fo the anchor bolt
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))         #Todo: change this with respect to anchor bolt parameters)
            self.nut.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParam(self, plateObj):

        self.pitch = 50
        self.gauge = 50
        self.edge = 100
        self.plateedge = 50
        self.end = 50
        self.row = 2
        self.col = 2

    def calculatePositions(self):
        self.position = []
        pos = self.origin

        self.pitch1 = 400
        self.gauge1 = 100

        pos1 =  pos + self.plateedge * self.gaugeDir
        pos2 = pos1 +  self.gauge * self.gaugeDir
        pos3 = pos2 + self.pitch1 * self.pitchDir
        pos4 = pos3 - self.gauge1 * self.gaugeDir

        self.position = [pos1, pos2, pos3, pos4]

    def place(self, origin, gaugeDir, pitchDir, boltDir):
        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir

        self.calculatePositions()

        for index, pos in enumerate(self.position):
            self.bolt[index].place(pos, gaugeDir, boltDir)
            self.nut[index].place((pos+self.gap*boltDir), gaugeDir, -boltDir)

    def create_model(self):
        for bolt in self.bolts:
            self.models.append(bolt.create_model())

        for nut in self.nuts:
            self.models.append(nut.create_model())

        dbg =  self.dbgSphere(self.origin)
        self.models.append(dbg)

    def dbgSphere(selfself, pt):
        return BrepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_models(self):
        return self.models




