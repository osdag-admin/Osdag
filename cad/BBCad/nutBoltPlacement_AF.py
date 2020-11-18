"""
created on 25-02-2018
@author: Siddhesh Chavan

modified: Darshan Vishwakarma (10-1-2020)

AF abbreviation used here is for Above Flange for bolting.
BF abbreviation used here is for Below Flange for bolting.
W is for bolting over Web.

"""""

from cad.items.bolt import Bolt
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt
import doctest


class NutBoltArray_AF():
    def __init__(self, outputobj, nut, bolt, numOfboltsF, nutSpaceF):
        """
        :param alist: Input values, entered by user 
        :param beam_data: Beam dimensions
        :param outputobj: Output dictionary
        :param nut: Nut dimensions
        :param bolt: Bolt dimensions
        :param numOfboltsF: Number of bolts required for over plate above flange
        :param nutSpaceF: Spacing between bolt head and nut
        """
        self.boltOrigin_AF = None
        self.pitch_new_AF = None
        self.originAF = None
        self.gaugeDirAF = None
        self.pitchDirAF = None
        self.boltDirAF = None


        self.bolt = bolt
        self.nut = nut
        self.outputobj = outputobj
        self.numOfboltsF = numOfboltsF
        self.nutSpaceF = nutSpaceF

        self.initBoltPlaceParams_AF(outputobj)
        self.bolts_AF = []
        self.nuts_AF = []
        self.initialiseNutBolts_AF()
        self.positions_AF = []
        self.models_AF = []

#################################################################
#           Nut_Bolt placement above flange(AF) of beam         #
#################################################################

    def initialiseNutBolts_AF(self):
        '''
        :return: This initializes required number of bolts and nuts for above flange.
        '''
        b_AF = self.bolt
        n_AF = self.nut

        for i in range(self.numOfboltsF):
            bolt_length_required = float(n_AF.H + self.nutSpaceF)#todo: anjali
            b_AF.H =  bolt_length_required + (bolt_length_required - 5) % 5
            self.bolts_AF.append(Bolt(b_AF.R, b_AF.T, b_AF.H, b_AF.r))
            # print("bolt", b_AF.R, b_AF.T, b_AF.H, b_AF.r)
            self.nuts_AF.append(Nut(n_AF.R, n_AF.T, n_AF.H, n_AF.r1))
            # print('Nut',(n_AF.R, n_AF.T, n_AF.H, n_AF.r1))

    def initBoltPlaceParams_AF(self, outputobj):
        '''
        :param outputobj: This is output dictionary for bolt placement parameters 
        :return: Edge, end, gauge and pitch distances for placement
        '''

        self.edge_AF = outputobj.flange_plate.edge_dist_provided     #33
        self.end_AF =  outputobj.flange_plate.end_dist_provided         #33
        self.edge_gauge_AF = outputobj.flange_plate.edge_dist_provided  #33
        self.pitch_AF = outputobj.flange_plate.pitch_provided           #50
        self.midpitch_AF = outputobj.flange_plate.midpitch
        self.gauge_AF = outputobj.flange_plate.midgauge
        self.gauge = outputobj.flange_plate.gauge_provided


        self.row_AF = outputobj.flange_plate.bolt_line             #2
        self.col_AF = outputobj.flange_plate.bolts_one_line                  #2
        self.gap = outputobj.flange_plate.gap

        # print('iniBoltPlaceParams_AF', (self.edge_AF, self.end_AF, self.edge_gauge_AF, self.pitch_AF, self.gauge_AF, self.row_AF, self.col_AF, self.gap))

    def calculatePositions_AF(self):
        """
        :return: The positions/coordinates to place the bolts in the form of list, positions_AF = [list of bolting coordinates] 
        """
        self.positions_AF = []
        self.boltOrigin_AF = self.originAF + self.end_AF * self.pitchDirAF + ((self.plateAbvFlangeL - self.gauge_AF)/2 - ((self.col_AF/2-1)*self.gauge)) * self.gaugeDirAF

        for rw_AF in range(self.row_AF):
            for cl_AF in range(self.col_AF):
                pos_AF = self.boltOrigin_AF
                if self.row_AF / 2 < rw_AF or self.row_AF / 2 == rw_AF:
                    self.pitch_new_AF = self.midpitch_AF
                    pos_AF = pos_AF + ((rw_AF - 1) * self.pitch_AF + self.pitch_new_AF) * self.pitchDirAF
                    if self.col_AF / 2 > cl_AF:
                        pos_AF = pos_AF + cl_AF * self.gauge * self.gaugeDirAF
                    else:
                        pos_AF = pos_AF + (cl_AF-1) * self.gauge * self.gaugeDirAF + 1 * self.gauge_AF * self.gaugeDirAF
                    self.positions_AF.append(pos_AF)
                else:
                    pos_AF = pos_AF + rw_AF * self.pitch_AF * self.pitchDirAF
                    if self.col_AF / 2 > cl_AF :
                        pos_AF = pos_AF + cl_AF * self.gauge * self.gaugeDirAF
                    else:
                        pos_AF = pos_AF + (cl_AF-1) * self.gauge * self.gaugeDirAF + 1 * self.gauge_AF * self.gaugeDirAF
                    self.positions_AF.append(pos_AF)

    def placeAF(self, originAF, gaugeDirAF, pitchDirAF, boltDirAF, plateAbvFlangeL):
        '''
        places the bolts and nuts based on the defined bolt arrangement
        '''
        self.originAF = originAF
        self.gaugeDirAF = gaugeDirAF
        self.pitchDirAF = pitchDirAF
        self.boltDirAF = boltDirAF
        self.plateAbvFlangeL = plateAbvFlangeL

        self.calculatePositions_AF()

        for index, pos in enumerate(self.positions_AF):
            self.bolts_AF[index].place(pos, gaugeDirAF, boltDirAF)
            self.nuts_AF[index].place((pos + self.nutSpaceF * boltDirAF), gaugeDirAF, boltDirAF)

    def create_modelAF(self):

        for bolt in self.bolts_AF:
            self.models_AF.append(bolt.create_model())

        for nut in self.nuts_AF:
            self.models_AF.append(nut.create_model())
            pass

        dbg = self.dbgSphere(self.originAF)
        self.models_AF.append(dbg)

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_modelsAF(self):
        return self.models_AF

    # Below methods are for creating holes in flange and web
    def get_bolt_listLA(self):
        boltlist = []
        for bolt in self.bolts_AF:
            boltlist.append(bolt.create_model())
            dbg = self.dbgSphere(self.originAF)
            self.models_AF.append(dbg)
        return boltlist

    def get_bolt_listRA(self):
        boltlist = []
        for bolt in self.bolts_AF:
            boltlist.append(bolt.create_model())
            dbg = self.dbgSphere(self.originAF)
            self.models_AF.append(dbg)
        return boltlist
