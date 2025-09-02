'''
Created on 07-Jun-2015

@author: deepa
'''
import numpy
from ...items.bolt import Bolt
from ...items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
# from .ModelUtils import get_gp_pt
# from Connections.Component.bolt import Bolt
# from Connections.Component.nut import Nut
# from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from .CAD_ModelUtils import getGpPt

class NutBoltArray():
    #def __init__(self,boltPlaceObj,nut,bolt,sgap, sbgap,tgap,tbgap):
    def __init__(self, boltPlaceObj, nut, bolt, snut_space, sbnut_space, tnut_space, tbnut_space, flag= False):
        self.flag = flag
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
        self.sgap = snut_space
        self.sbgap = sbnut_space
        self.tgap = tnut_space
        self.tbgap = tbnut_space

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

        self.models = []

    def initialiseNutBolts(self):
        b = self.bolt
        n = self.nut
        if not self.flag:
            self.column = self.col
        else:
            self.column = int(self.col * 2)
        for i in range(self.row * self.column):
            bolt_len_required = float(b.T + self.sgap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.bolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T,n.H, n.r1))

        for i in range(self.brow * self.bcol):
            bolt_len_required = float(b.T + self.sbgap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.bbolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.bnuts.append(Nut(n.R, n.T,n.H, n.r1))

        for i in range(self.topcliprow * self.topclipcol):
            bolt_len_required= float(b.T + self.tgap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.topclipbolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.topclipnuts.append(Nut(n.R, n.T,n.H, n.r1))

        for i in range(self.topclipbrow * self.topclipbcol):
            bolt_len_required = float(b.T + self.tbgap)
            b.H = bolt_len_required + (5 - bolt_len_required) % 5
            self.topclipbbolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.topclipbnuts.append(Nut(n.R, n.T,n.H, n.r1))

    def initBoltPlaceParams(self, boltPlaceObj):

        self.gauge_two_bolt_ta_col = boltPlaceObj.top_angle_gauge_column
        self.edge_two_bolt_ta_col = boltPlaceObj.top_angle_edge_column
        self.TAEDC = boltPlaceObj.top_angle_end
        self.topcliprow = 1
        self.topclipcol = 2

        self.gauge_two_bolt_ta_beam = boltPlaceObj.top_angle_gauge_beam
        self.edge_two_bolt_ta_beam = boltPlaceObj.top_angle_edge_beam
        self.TAEDB = boltPlaceObj.top_angle_end
        self.topclipbrow = 1
        self.topclipbcol = 2

        self.gauge_two_bolt_sa_col = boltPlaceObj.seated_angle_gauge_column
        if self.flag:
            self.sa_length = boltPlaceObj.sa_length
        self.edge = boltPlaceObj.seated_angle_edge_column
        self.end = boltPlaceObj.seated_angle_end_column
        self.gauge = boltPlaceObj.gauge
        self.pitch = boltPlaceObj.min_pitch_round
        self.row = boltPlaceObj.bolt_row
        if not self.flag:
            self.col = boltPlaceObj.bolt_col
        else:
            self.col = int(boltPlaceObj.bolt_col/2)

        self.gauge_two_bolt_sa_beam = boltPlaceObj.seated_angle_gauge_beam
        self.edge_two_bolt_sa_beam = boltPlaceObj.seated_angle_edge_beam
        self.SAEDB = boltPlaceObj.seated_angle_end_beam
        self.brow = 1
        self.bcol= 2

    def calculatePositions(self):
        self.positions = []
        if not self.flag:
            for rw in range(self.row):
                for col in range(self.col):
                    pos = self.origin
                    pos = pos + self.edge * self.gaugeDir
                    pos = pos + col * self.gauge * self.gaugeDir
                    pos = pos + self.end * self.pitchDir
                    pos = pos + rw * self.pitch * self.pitchDir
                    self.positions.append(pos)

        else:
            for rw in range(self.row):
                for col in range(self.col):
                    pos = self.origin
                    pos = pos + self.edge * self.gaugeDir
                    pos = pos + col * self.gauge * self.gaugeDir
                    pos = pos + self.end * self.pitchDir
                    pos = pos + rw * self.pitch * self.pitchDir
                    self.positions.append(pos)

                for col in range(self.col):
                    pos = self.origin
                    pos = pos + (self.sa_length - self.edge) * self.gaugeDir
                    pos = pos - col * self.gauge * self.gaugeDir
                    pos = pos + self.end * self.pitchDir
                    pos = pos + rw * self.pitch * self.pitchDir
                    self.positions.append(pos)

    def calculatebPositions(self):
        self.bpositions = []
        for rw in  range(self.brow):
            for col in range(self.bcol):
                pos = self.borigin
                pos = pos + self.edge_two_bolt_sa_beam * self.bgaugeDir
                pos = pos + col * self.gauge_two_bolt_sa_beam * self.bgaugeDir
                pos = pos + self.SAEDB * self.bpitchDir
                pos = pos + rw * self.pitch * self.bpitchDir
                self.bpositions.append(pos)

    def calculatetopclipPositions(self):
        self.topclippositions = []
        for rw in  range(self.topcliprow):
            for col in range(self.topclipcol):
                pos = self.topcliporigin
                pos = pos + self.edge_two_bolt_ta_beam * self.topclipgaugeDir
                pos = pos + col * self.gauge_two_bolt_ta_beam * self.topclipgaugeDir
                pos = pos + self.TAEDB * self.topclippitchDir
                pos = pos + rw * self.pitch * self.topclippitchDir
                self.topclippositions.append(pos)

    def calculatetopclipbPositions(self):
        self.topclipbpositions = []
        for rw in  range(self.topclipbrow):
            for col in range(self.topclipbcol):
                pos = self.topclipborigin
                pos = pos + self.edge_two_bolt_ta_col * self.topclipbgaugeDir
                pos = pos + col * self.gauge_two_bolt_ta_col * self.topclipbgaugeDir
                pos = pos + self.TAEDC * self.topclipbpitchDir
                pos = pos + rw * self.pitch * self.topclipbpitchDir
                self.topclipbpositions.append(pos)

    def place(self, origin, gaugeDir, pitchDir, boltDir,borigin,bgaugeDir,bpitchDir,bboltDir, topcliporigin,topclipgaugeDir, topclippitchDir, topclipboltDir,topclipborigin,topclipbgaugeDir,topclipbpitchDir,topclipbboltDir):
        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir
        self.calculatePositions()

        # for index, pos in enumerate (self.positions):
        #     self.bolts[index].place(pos, gaugeDir, boltDir)
        #     self.nuts[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)
        for index, pos in enumerate(self.positions):
            self.bolts[index].place(pos, gaugeDir, boltDir)
            self.nuts[index].place((pos + self.sgap * boltDir), gaugeDir, -boltDir)

        self.borigin = borigin
        self.bgaugeDir = bgaugeDir
        self.bpitchDir = bpitchDir
        self.bboltDir = bboltDir
        self.calculatebPositions()

        # for index, pos in enumerate (self.bpositions):
        #     self.bbolts[index].place(pos, bgaugeDir, bboltDir)
        #     self.bnuts[index].place((pos + self.bgap * bboltDir), bgaugeDir, -bboltDir)
        for index, pos in enumerate(self.bpositions):
            self.bbolts[index].place(pos, bgaugeDir, bboltDir)
            self.bnuts[index].place((pos + self.sbgap * bboltDir), bgaugeDir, -bboltDir)

        self.topcliporigin = topcliporigin
        self.topclipgaugeDir = topclipgaugeDir
        self.topclippitchDir = topclippitchDir
        self.topclipboltDir = topclipboltDir
        self.calculatetopclipPositions()

        # for index, pos in enumerate (self.topclippositions):
        #     self.topclipbolts[index].place(pos, topclipgaugeDir, topclipboltDir)
        #     self.topclipnuts[index].place((pos + self.bgap * topclipboltDir), topclipgaugeDir, -topclipboltDir)

        # for index, pos in enumerate (self.topclippositions):
        #     self.topclipbolts[index].place(pos, topclipgaugeDir, topclipboltDir)
        #     self.topclipnuts[index].place((pos + self.tbgap * topclipboltDir), topclipgaugeDir, -topclipboltDir)

        for index, pos in enumerate (self.topclippositions):
            self.topclipbolts[index].place(pos, topclipgaugeDir, topclipboltDir)
            self.topclipnuts[index].place((pos + self.tgap * topclipboltDir), topclipgaugeDir, -topclipboltDir)

        self.topclipborigin = topclipborigin
        self.topclipbgaugeDir = topclipbgaugeDir
        self.topclipbpitchDir = topclipbpitchDir
        self.topclipbboltDir = topclipbboltDir
        self.calculatetopclipbPositions()

        # for index, pos in enumerate (self.topclipbpositions):
        #     self.topclipbbolts[index].place(pos, topclipbgaugeDir, topclipbboltDir)
        #     self.topclipbnuts[index].place((pos + self.gap * topclipbboltDir), topclipbgaugeDir, -topclipbboltDir)

        # for index, pos in enumerate (self.topclipbpositions):
        #     self.topclipbbolts[index].place(pos, topclipbgaugeDir, topclipbboltDir)
        #     self.topclipbnuts[index].place((pos + self.tgap * topclipbboltDir), topclipbgaugeDir, -topclipbboltDir)

        for index, pos in enumerate (self.topclipbpositions):
            self.topclipbbolts[index].place(pos, topclipbgaugeDir, topclipbboltDir)
            self.topclipbnuts[index].place((pos + self.tbgap * topclipbboltDir), topclipbgaugeDir, -topclipbboltDir)

    def createModel(self):

        for bolt in self.bolts:
            self.models.append(bolt.create_model())

        for nut in self.nuts:
            self.models.append(nut.create_model())

        dbg = self.dbgSphere(self.origin)
        self.models.append(dbg)

        for bolt in self.bbolts:
            self.models.append(bolt.create_model())

        for nut in self.bnuts:
            self.models.append(nut.create_model())

        dbg = self.dbgSphere(self.borigin)
        self.models.append(dbg)

        for bolt in self.topclipbolts:
            self.models.append(bolt.create_model())

        for nut in self.topclipnuts:
            self.models.append(nut.create_model())

        dbg = self.dbgSphere(self.topcliporigin)
        self.models.append(dbg)

        for bolt in self.topclipbbolts:
            self.models.append(bolt.create_model())

        for nut in self.topclipbnuts:
            self.models.append(nut.create_model())

        dbg = self.dbgSphere(self.topclipborigin)
        self.models.append(dbg)

    def get_beam_bolts(self):
        boltlist = []
        for bolt in self.bbolts:
            boltlist.append(bolt.create_model())
        for bolt in self.topclipbolts:
            boltlist.append(bolt.create_model())
        return boltlist

    def get_column_bolts(self):
        boltlist = []
        for bolt in self.bolts:
            boltlist.append(bolt.create_model())
        for bolt in self.topclipbbolts:
            boltlist.append(bolt.create_model())
        return boltlist

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_models(self):
        return self.models
