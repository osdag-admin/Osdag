"""
created on 25-02-2018

@author: Siddhesh Chavan

AF abbreviation used here is for Above Flange for bolting.
BF abbreviation used here is for Below Flange for bolting.
W is for bolting over Web.

"""""

from cad.items.bolt import Bolt
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse


class NutBoltArray_AF():
    def __init__(self, Obj, nut, bolt, numOfboltsF, nutSpaceF):
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

        # self.uiObj = alist
        # self.beamDim = beam_data
        self.bolt = bolt
        self.nut = nut
        self.numOfboltsF = numOfboltsF
        self.nutSpaceF = nutSpaceF

        self.initBoltPlaceParams_AF(Obj)
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
            bolt_length_required = float(n_AF.H + self.nutSpaceF)  # todo: anjali
            print(bolt_length_required, "len")
            #  bolt_length_required = float(b_AF.T  + self.nutSpaceF)
            # bolt_length_required = 100
            b_AF.H = bolt_length_required + 10
            self.bolts_AF.append(Bolt(b_AF.R, b_AF.T, b_AF.H, b_AF.r))
            print("bolt", b_AF.R, b_AF.T, b_AF.H, b_AF.r)
            self.nuts_AF.append(Nut(n_AF.R, n_AF.T, n_AF.H, n_AF.r1))
            print('Nut', (n_AF.R, n_AF.T, n_AF.H, n_AF.r1))

    def initBoltPlaceParams_AF(self, Obj):
        '''
        :param outputobj: This is output dictionary for bolt placement parameters
        :return: Edge, end, gauge and pitch distances for placement
        '''

        self.edge_AF = Obj.flange_plate.edge_dist_provided
        self.end_AF = Obj.flange_plate.end_dist_provided
        self.edge_gauge_AF = Obj.flange_plate.edge_dist_provided
        self.pitch_AF = Obj.flange_plate.pitch_provided
        self.midpitch_AF = Obj.flange_plate.midpitch  #=(2 * self.flange_plate.end_dist_provided) + self.flange_plate.gap + self.section.web_thickness
        self.gauge_AF = Obj.flange_plate.midgauge
        self.gauge = Obj.flange_plate.gauge_provided

        # outputobj.flange_plate.gauge_provided   # Revised gauge distance   #0.0
        self.row_AF = Obj.flange_plate.bolt_line
        self.col_AF = Obj.flange_plate.bolts_one_line                  #2
        self.gap = Obj.flange_plate.gap
        # if self.col_AF ==2:
        #     self.gauge =0
        #     self.gauge_AF= Obj.flange_plate.midgauge
        # else:
        #     self.gauge = Obj.flange_plate.gauge_provided
        #     self.gauge_AF= Obj.flange_plate.midgauge

    def calculatePositions_AF(self):
        """
        :return: The positions/coordinates to place the bolts in the form of list, positions_AF = [list of bolting coordinates]
        """
        self.positions_AF = []
        self.boltOrigin_AF = self.originAF + self.end_AF * self.pitchDirAF + (self.edge_AF) * self.gaugeDirAF
        # self.boltOrigin_AF = self.originAF - (self.row_AF/2 * self.pitch_AF) * self.pitchDirAF  - ((self.col_AF / 2) * self.gauge) * self.gaugeDirAF
                # + ((self.plateAbvFlangeL - self.gauge_AF) / 2 - ((self.col_AF / 2 - 1) * self.gauge)) * self.gaugeDirAF

        for rw_AF in range(self.row_AF):
            for cl_AF in range(self.col_AF):
                pos_AF = self.boltOrigin_AF
                if self.row_AF / 2 < rw_AF or self.row_AF / 2 == rw_AF:
                    self.pitch_new_AF = self.midpitch_AF
                    pos_AF = pos_AF + ((rw_AF - 1) * self.pitch_AF + self.pitch_new_AF) * self.pitchDirAF
                    if self.col_AF / 2 > cl_AF:
                        pos_AF = pos_AF + cl_AF * self.gauge * self.gaugeDirAF
                    else:
                        pos_AF = pos_AF + (
                                cl_AF - 1) * self.gauge * self.gaugeDirAF + 1 * self.gauge_AF * self.gaugeDirAF
                    self.positions_AF.append(pos_AF)
                else:
                    pos_AF = pos_AF + rw_AF * self.pitch_AF * self.pitchDirAF
                    if self.col_AF / 2 > cl_AF:
                        pos_AF = pos_AF + cl_AF * self.gauge * self.gaugeDirAF
                    else:
                        pos_AF = pos_AF + (
                                cl_AF - 1) * self.gauge * self.gaugeDirAF + 1 * self.gauge_AF * self.gaugeDirAF
                    self.positions_AF.append(pos_AF)

    def placeAF(self, originAF, gaugeDirAF, pitchDirAF, boltDirAF, plateAbvFlangeL):
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
        print("hhhh", self.bolts_AF)
        for bolt in self.bolts_AF:
            print("bolt", bolt, "fgfg")
            self.models_AF.append(bolt.create_model())

        for nut in self.nuts_AF:
            self.models_AF.append(nut.create_model())
            pass

        dbg = self.dbgSphere(self.originAF)
        self.models_AF.append(dbg)

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_modelsAF(self):
        # nut_bolts = self.models_AF
        # array = nut_bolts[0]
        # for comp in nut_bolts:
        #     array = BRepAlgoAPI_Fuse(comp, array).Shape()
        #
        # return array
        #todo: using for loops is here is slowing down the cad generating process
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


if __name__ == '__main__':
    from cad.items.bolt import Bolt
    from cad.items.nut import Nut
    import numpy

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    nutboltArrayOrigin = numpy.array([0., 0., 0.])
    gaugeDir = numpy.array([0.0, 1.0, 0])
    pitchDir = numpy.array([1.0, 0.0, 0])
    boltDir = numpy.array([0, 0, 1.0])

    bolt = Bolt(R=12, T=5, H=6, r=6)
    nut = Nut(R=bolt.R, T=bolt.T, H=bolt.T + 1, innerR1=bolt.r)
    nut_space = 10 + 5 + nut.T  # member.T + plate.T + nut.T
    Obj = '6'
    numOfboltsF = 24
    plateAbvFlangeL = 100

    nut_bolt_array = NutBoltArray_AF(Obj, nut, bolt, numOfboltsF, nut_space)

    nut_bolt_array.placeAF(nutboltArrayOrigin, pitchDir, gaugeDir, boltDir, plateAbvFlangeL)
    nut_bolt_array.create_modelAF()

    array = nut_bolt_array.get_modelsAF()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(array, color='YELLOW', update=True)
    # display.DisplayShape(parray, color= 'BLUE', update=True)
    display.DisableAntiAliasing()
    start_display()
