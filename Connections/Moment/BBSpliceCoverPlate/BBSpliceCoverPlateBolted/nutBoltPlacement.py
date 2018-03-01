'''
created on 25-02-2018

@author: Siddhesh Chavan

AF abbreviation used here is for Above Flange for bolting.
BF abbreviation used here is for Below Flange for bolting.
W is for bolting over Web.
'''

from Connections.Component.bolt import Bolt
from Connections.Component.nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from Connections.Component.ModelUtils import getGpPt
import numpy as np

class NutBoltArray():
    def __init__(self, alist, beam_data, outputobj, nut, bolt, numOfboltsF, nutSpaceF, numOfboltsW, nutSpaceW):
        self.origin = None
        # self.gaugeDir = None
        # self.pitchDir = None
        # self.boltDir = None

        self.uiObj = alist
        self.beamDim = beam_data
        self.bolt = bolt
        self.nut = nut
        self.outputobj = outputobj
        self.numOfboltsF = numOfboltsF
        self.nutSpaceF = nutSpaceF
        self.numOfboltsW = numOfboltsW
        self.nutSpaceW = nutSpaceW

        self.initBoltPlaceParams_AF(outputobj)
        self.bolts_AF = []
        self.nuts_AF = []
        self.initialiseNutBolts_AF()
        self.positions_AF = []
        self.models_AF = []

        # self.initBoltPlaceParams_BF(outputobj)
        # self.bolts_BF = []
        # self.nuts_BF = []
        # self.initialiseNutBolts_BF()
        # self.positions_BF = []
        # self.models_BF = []
        #
        # self.initBoltPlaceParams_Web(outputobj)
        # self.bolts_Web = []
        # self.nuts_Web = []
        # self.initialiseNutBolts_Web()
        # self.positions_Web = []
        # self.models_Web = []

    def initialiseNutBolts_AF(self):
        '''
        :return: This initializes nut & bolt for bolts above flange 
        '''
        b_AF = self.bolt
        n_AF = self.nut
        for i in range(self.numOfboltsF):
            bolt_length_required = float(b_AF.T + self.nutSpaceF)
            b_AF.H = 1.5 * bolt_length_required
            self.bolts_AF.append(Bolt(b_AF.R, b_AF.T, b_AF.H, b_AF.r))
            self.nuts_AF.append(Nut(n_AF.R, n_AF.T, n_AF.H, n_AF.r1))

    def initBoltPlaceParams_AF(self, outputobj):
        '''
        :param outputobj: This is output dictionary for bolt placement parameters 
        :return: Edge, end, gauge and pitch distances for placement
        '''
        self.edge_AF = outputobj["FlangeBolt"]["EdgeF"]
        self.end_AF = outputobj["FlangeBolt"]["EndF"]
        self.pitch_AF = outputobj["FlangeBolt"]["PitchF"]
        self.gauge_AF = self.beamDim["B"] - 2 * self.edge_AF
        self.row_AF = outputobj["FlangeBolt"]["BoltsRequiredF"]
        self.col_AF = 2

    def calculatePositions_AF(self):
        self.positions_AF = []
        self.boltOrigin_AF = self.originAF + self.end_AF * self.pitchDirAF + self.edge_AF * self.gaugeDirAF
        for rw_AF in range(self.row_AF):
            for cl_AF in range(self.col_AF):
                pos_AF = self.boltOrigin_AF
                if self.row_AF / 2 < rw_AF or self.row_AF / 2 == rw_AF:
                    self.pitch_new_AF = 2 * self.end_AF + 5.0      #TODO 5.0 = self.gap
                    pos_AF = pos_AF + ((rw_AF-1) * self.pitch_AF + self.pitch_new_AF) * self.pitchDirAF
                    pos_AF = pos_AF + cl_AF * self.gauge_AF * self.gaugeDirAF
                    self.positions_AF.append(pos_AF)
                else:
                    pos_AF = pos_AF + rw_AF * self.pitch_AF * self.pitchDirAF
                    pos_AF = pos_AF + cl_AF * self.gauge_AF * self.gaugeDirAF
                    self.positions_AF.append(pos_AF)

    def placeAF (self, originAF, gaugeDirAF, pitchDirAF, boltDirAF):
        self.originAF = originAF
        self.gaugeDirAF = gaugeDirAF
        self.pitchDirAF = pitchDirAF
        self.boltDirAF = boltDirAF

        self.calculatePositions_AF()

        for index, pos in enumerate(self.positions_AF):
            self.bolts_AF[index].place(pos, gaugeDirAF, boltDirAF)
            self.nuts_AF[index].place((pos + self.nutSpaceF * boltDirAF), gaugeDirAF, boltDirAF)

    def create_modelAF(self):
        for bolt in self.bolts_AF:
            self.models_AF.append(bolt.create_model())
        for nut in self.nuts_AF:
            self.models_AF.append(nut.create_model())

        dbg = self.dbgSphere(self.originAF)
        self.models_AF.append(dbg)

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Sphere()

    def get_modelsAF(self):
        return self.models_AF