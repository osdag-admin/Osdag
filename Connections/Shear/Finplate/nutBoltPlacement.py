'''
Created on 07-Jun-2015

@author: deepa
'''
from Connections.Component.bolt import Bolt
from Connections.Component.nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from Connections.Component.ModelUtils import getGpPt


class NutBoltArray():

    '''
                                            gDir
          +---------------------------->
          |
          |
          |   P origin
          |      +-------+---------------+
          |      |       |               |
pDir      |      |       | End distance  |
          |      |       v               |
          |      |       X       X       |
          |      |                       |
          |      |                       |
          |      |                       |
          v      |                       |
                 |        Gauge distance |
                 |       X-------X       |
                 |       +               |
                 |       |               |
                 |       | Pitch         |
                 |       |               |
                 |       v               |
                 |       X       X+----> +
                 |               Edge distance
                 |                       |
                 |                       |
                 |                       |
                 +-----------------------+

                Nut Bolt Placement

    '''

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
        # self.calculatePositions()

        self.models = []

    def initialiseNutBolts(self):
        '''
        Initializing the Nut and Bolt
        '''
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            bolt_len_required = float(b.T + self.gap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParams(self, boltPlaceObj):

        self.pitch = boltPlaceObj['Bolt']['pitch']
        self.gauge = boltPlaceObj['Bolt']['gauge']
        self.edge = boltPlaceObj['Bolt']['edge']
        self.plateedge = boltPlaceObj['Plate']['plateedge']
        self.end = boltPlaceObj['Bolt']['enddist']
        self.row = boltPlaceObj['Bolt']['numofrow']
        self.col = boltPlaceObj['Bolt']['numofcol']

    def calculatePositions(self):
        '''
        Calculates the exact position for nuts and bolts.
        '''
        self.positions = []
        for rw in range(self.row):
            for col in range(self.col):
                pos = self.origin
                # pos = pos + self.end * self.gaugeDir
                # #pos = pos + self.edge * self.gaugeDir
                pos = pos + self.plateedge * self.gaugeDir
                pos = pos + col * self.gauge * self.gaugeDir
                # pos = pos + self.edge * self.pitchDir
                pos = pos + self.end * self.pitchDir
                pos = pos + rw * self.pitch * self.pitchDir

                self.positions.append(pos)

    def place(self, origin, gaugeDir, pitchDir, boltDir):

        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir

        self.calculatePositions()

        for index, pos in enumerate(self.positions):
            self.bolts[index].place(pos, gaugeDir, boltDir)
            self.nuts[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)

    def create_model(self):
        for bolt in self.bolts:
            self.models.append(bolt.create_model())

        for nut in self.nuts:
            self.models.append(nut.create_model())

        dbg = self.dbgSphere(self.origin)
        self.models.append(dbg)

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_models(self):
        return self.models
    
