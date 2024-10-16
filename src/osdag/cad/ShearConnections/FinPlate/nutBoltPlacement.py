'''
Created on 07-Jun-2015

@author: deepa
'''
from cad.items.bolt import Bolt
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt


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

    def __init__(self, boltPlaceObj, plateObj, nut, bolt, nut_space):
        # finNutBoltArray(A.bolt, nut, bolt, nut_space)

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.initBoltPlaceParams(plateObj)

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

    def initBoltPlaceParams(self, plateObj):

        self.pitch = plateObj.pitch_provided
        self.gauge = plateObj.gauge_provided
        self.edge = plateObj.end_dist_provided
        self.plateedge = plateObj.end_dist_provided + plateObj.gap
        self.end = plateObj.edge_dist_provided
        self.row = plateObj.bolts_one_line
        self.col = plateObj.bolt_line

    def calculatePositions(self):
        '''
        Calculates the exact position for nuts and bolts.
        '''
        self.positions = []
        for rw in range(self.col):
            for col in range(self.row):
                pos = self.origin
                # pos = pos + self.end * self.gaugeDir
                # #pos = pos + self.edge * self.gaugeDir
                pos = pos + self.plateedge * self.gaugeDir
                pos = pos + col * self.gauge * self.pitchDir
                # pos = pos + self.edge * self.pitchDirself.gauge self.pitchDir
                pos = pos + self.end * self.pitchDir
                pos = pos + rw * self.pitch * self.gaugeDir

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
    
