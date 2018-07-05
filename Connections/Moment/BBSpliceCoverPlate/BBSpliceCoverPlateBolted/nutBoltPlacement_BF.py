"""
created on 25-02-2018

@author: Siddhesh Chavan

AF abbreviation used here is for Above Flange for bolting.
BF abbreviation used here is for Below Flange for bolting.
W is for bolting over Web.
"""""


from Connections.Component.bolt import Bolt
from Connections.Component.nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from Connections.Component.ModelUtils import getGpPt


class NutBoltArray_BF():
    def __init__(self, alist, beam_data, outputobj, nut, bolt, numOfboltsF, nutSpaceF):
        """
        :param alist: Input values, entered by user 
        :param beam_data: Beam dimensions
        :param outputobj: Output dictionary
        :param nut: Nut dimensions
        :param bolt: Bolt dimensions
        :param numOfboltsF: Number of bolts required for over plate above flange
        :param nutSpaceF: Spacing between bolt head and nut
        """
        self.boltOrigin_BF = None
        self.pitch_new_BF = None
        self.originBF = None
        self.gaugeDirBF = None
        self.pitchDirBF = None
        self.boltDirBF = None

        self.uiObj = alist
        self.beamDim = beam_data
        self.bolt = bolt
        self.nut = nut
        self.outputobj = outputobj
        self.numOfboltsF = numOfboltsF
        self.nutSpaceF = nutSpaceF

        self.initBoltPlaceParams_BF(outputobj, alist)
        self.bolts_BF = []
        self.nuts_BF = []
        self.initialiseNutBolts_BF()
        self.positions_BF = []
        self.models_BF = []

#################################################################
#           Nut_Bolt placement below flange(BF) of beam         #
#################################################################

    def initialiseNutBolts_BF(self):
        '''
        :return: This initializes required number of bolts and nuts for below flange. 
        '''
        b_BF = self.bolt
        n_BF = self.nut
        for j in range(self.numOfboltsF):
            bolt_length_required = float(b_BF.T + self.nutSpaceF)
            b_BF.H = 1.5 * bolt_length_required
            self.bolts_BF.append(Bolt(b_BF.R, b_BF.T, b_BF.H, b_BF.r))
            self.nuts_BF.append(Nut(n_BF.R, n_BF.T, n_BF.H, n_BF.r1))

    def initBoltPlaceParams_BF(self, outputobj, alist):
        '''
        :param outputobj: This is output dictionary for bolt placement parameters 
        :return: Edge, end, gauge and pitch distances for placement
        '''
        self.edge_BF = outputobj["FlangeBolt"]["EdgeF"]
        self.end_BF = outputobj["FlangeBolt"]["EndF"]
        self.edge_gauge_BF = outputobj["FlangeBolt"]["edge_dist_gauge"]
        self.pitch_BF = outputobj["FlangeBolt"]["PitchF"]
        self.gauge_BF = outputobj["FlangeBolt"]["FlangeGauge"]
        self.row_BF = outputobj["FlangeBolt"]["BoltsRequiredF"]
        self.col_BF = 2
        self.gap = alist["detailing"]["gap"]

    def calculatePositions_BF(self):
        """
        :return: The positions/coordinates to place the bolts in the form of list, positions_BF = [list of bolting coordinates] 
        """
        self.positions_BF = []
        self.boltOrigin_BF = self.originBF + self.edge_gauge_BF * self.pitchDirBF + (self.plateBelwFlangeL - self.gauge_BF) / 2 * self.gaugeDirBF
        for rw_BF in range(self.row_BF):
            for cl_BF in range(self.col_BF):
                pos_BF = self.boltOrigin_BF
                if self.row_BF / 2 < rw_BF or self.row_BF / 2 == rw_BF:
                    self.pitch_new_BF = 2 * self.edge_gauge_BF + self.gap
                    pos_BF = pos_BF + ((rw_BF - 1) * self.pitch_BF + self.pitch_new_BF) * self.pitchDirBF
                    pos_BF = pos_BF + cl_BF * self.gauge_BF * self.gaugeDirBF
                    self.positions_BF.append(pos_BF)
                else:
                    pos_BF = pos_BF + rw_BF * self.pitch_BF * self.pitchDirBF
                    pos_BF = pos_BF + cl_BF * self.gauge_BF * self.gaugeDirBF
                    self.positions_BF.append(pos_BF)

    def placeBF(self, originBF, gaugeDirBF, pitchDirBF, boltDirBF, plateBelwFlangeL):
        self.originBF = originBF
        self.gaugeDirBF = gaugeDirBF
        self.pitchDirBF = pitchDirBF
        self.boltDirBF = boltDirBF
        self.plateBelwFlangeL = plateBelwFlangeL

        self.calculatePositions_BF()

        for index_BF, pos_BF in enumerate(self.positions_BF):
            self.bolts_BF[index_BF].place(pos_BF, gaugeDirBF, boltDirBF)
            self.nuts_BF[index_BF].place((pos_BF + self.nutSpaceF * boltDirBF), gaugeDirBF, boltDirBF)

    def create_modelBF(self):
        for bolt in self.bolts_BF:
            self.models_BF.append(bolt.create_model())
        for nut in self.nuts_BF:
            self.models_BF.append(nut.create_model())

        dbg = self.dbgSphere(self.originBF)
        self.models_BF.append(dbg)

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_modelsBF(self):
        return self.models_BF

    # Below methods are for creating holes in flange and web
    def get_bolt_listLB(self):
        boltlist = []
        for bolt in self.bolts_BF:
            boltlist.append(bolt.create_model())
            dbg = self.dbgSphere(self.originBF)
            self.models_BF.append(dbg)
        return boltlist

    def get_bolt_listRB(self):
        boltlist = []
        for bolt in self.bolts_BF:
            boltlist.append(bolt.create_model())
            dbg = self.dbgSphere(self.originBF)
            self.models_BF.append(dbg)
        return boltlist

