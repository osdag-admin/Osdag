'''
created on 19-01-2018

@author: Siddhesh C.
'''

from Connections.Component.bolt import Bolt
from Connections.Component.nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from Connections.Component.ModelUtils import getGpPt

class NutBoltArray():
    def __init__(self, boltPlaceObj, nut, bolt, nut_space):

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.initBoltPlaceParams(boltPlaceObj)

        self.bolt = bolt
        self.nut = nut
        self.gap = nut_space

        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()

        self.positions = []

        self.models = []

    def initialiseNutBolts(self):
        '''
        Initialise the Nut and Bolt 
        '''
        b = self.bolt
        n = self.nut
        for i in range(self.number_of_bolts):
            bolt_length_required = float(b.T + self.gap)
            b.H = bolt_length_required + (5 - bolt_length_required) % 5
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParams(self, boltPlaceObj):

        pass

