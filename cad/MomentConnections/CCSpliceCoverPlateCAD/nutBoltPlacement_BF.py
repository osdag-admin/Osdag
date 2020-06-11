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


class NutBoltArray_BF():
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
        self.boltOrigin_BF = None
        self.pitch_new_BF = None
        self.originBF = None
        self.gaugeDirBF = None
        self.pitchDirBF = None
        self.boltDirBF = None

        # self.uiObj = alist
        # self.beamDim = beam_data
        self.bolt = bolt
        self.nut = nut
        self.numOfboltsF = numOfboltsF
        self.nutSpaceF = nutSpaceF

        self.initBoltPlaceParams_BF(Obj)
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
            bolt_length_required = float(n_BF.H + self.nutSpaceF)
            b_BF.H = bolt_length_required + 10
            self.bolts_BF.append(Bolt(b_BF.R, b_BF.T, b_BF.H, b_BF.r))
            self.nuts_BF.append(Nut(n_BF.R, n_BF.T, n_BF.H, n_BF.r1))

    def initBoltPlaceParams_BF(self, Obj):
        '''
        :param outputobj: This is output dictionary for bolt placement parameters
        :return: Edge, end, gauge and pitch distances for placement
        '''
        self.edge_BF = Obj.flange_plate.edge_dist_provided
        self.end_BF = Obj.flange_plate.end_dist_provided
        self.edge_gauge_BF = Obj.flange_plate.edge_dist_provided
        self.pitch_BF = Obj.flange_plate.pitch_provided
        self.gauge_BF = Obj.flange_plate.midgauge
        self.gauge = Obj.flange_plate.gauge_provided
        # outputobj.flange_plate.gauge_provided  # Revised gauge distance
        self.row_BF = Obj.flange_plate.bolt_line
        self.col_BF = Obj.flange_plate.bolts_one_line
        self.gap = Obj.flange_plate.gap

    def calculatePositions_BF(self):
        """
        :return: The positions/coordinates to place the bolts in the form of list, positions_BF = [list of bolting coordinates]
        """
        self.positions_BF = []
        # self.boltOrigin_BF = self.originBF - (self.row_BF/2* self.pitch_BF) * self.pitchDirBF - (((self.col_BF / 2) * self.gauge)) * self.gaugeDirBF
        self.boltOrigin_BF = self.originBF + self.end_BF * self.pitchDirBF + (self.edge_BF) * self.gaugeDirBF

        for rw_BF in range(self.row_BF):
            for cl_BF in range(self.col_BF):
                pos_BF = self.boltOrigin_BF
                if self.row_BF / 2 < rw_BF or self.row_BF / 2 == rw_BF:
                    self.pitch_new_BF = 2 * self.end_BF + self.gap
                    pos_BF = pos_BF + ((rw_BF - 1) * self.pitch_BF + self.pitch_new_BF) * self.pitchDirBF
                    if self.col_BF / 2 > cl_BF:
                        pos_BF = pos_BF + cl_BF * self.gauge * self.gaugeDirBF
                    else:
                        pos_BF = pos_BF + (
                                cl_BF - 1) * self.gauge * self.gaugeDirBF + 1 * self.gauge_BF * self.gaugeDirBF
                    self.positions_BF.append(pos_BF)
                else:
                    pos_BF = pos_BF + rw_BF * self.pitch_BF * self.pitchDirBF
                    if self.col_BF / 2 > cl_BF:
                        pos_BF = pos_BF + cl_BF * self.gauge * self.gaugeDirBF
                    else:
                        pos_BF = pos_BF + (
                                cl_BF - 1) * self.gauge * self.gaugeDirBF + 1 * self.gauge_BF * self.gaugeDirBF
                    self.positions_BF.append(pos_BF)

                # pos_BF = self.boltOrigin_BF
        #                 # if self.row_BF / 2 < rw_BF or self.row_BF / 2 == rw_BF:
        #                 #     self.pitch_new_BF = 2 * self.edge_gauge_BF + self.gap
        #                 #     pos_BF = pos_BF + ((rw_BF - 1) * self.pitch_BF + self.pitch_new_BF) * self.pitchDirBF
        #                 #     pos_BF = pos_BF + cl_BF * self.gauge_BF * self.gaugeDirBF
        #                 #     self.positions_BF.append(pos_BF)
        #                 # else:
        #                 #     pos_BF = pos_BF + rw_BF * self.pitch_BF * self.pitchDirBF
        #                 #     pos_BF = pos_BF + cl_BF * self.gauge_BF * self.gaugeDirBF
        #                 #     self.positions_BF.append(pos_BF)

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
            pass
        for nut in self.nuts_BF:
            self.models_BF.append(nut.create_model())
            pass

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

    bolt = Bolt(R=12, T=5, H=6, r=6)
    nut = Nut(R=bolt.R, T=bolt.T, H=bolt.T + 1, innerR1=bolt.r)
    nut_space = 10 + 5 + nut.T  # member.T + plate.T + nut.T
    Obj = '6'
    boltDir = numpy.array([0, 0, 1.0])
    numOfboltsF = 24
    plateAbvFlangeL = 100

    nut_bolt_array = NutBoltArray_BF(Obj, nut, bolt, numOfboltsF, nut_space)

    nut_bolt_array.placeBF(nutboltArrayOrigin, pitchDir, gaugeDir, boltDir, plateAbvFlangeL)
    nut_bolt_array.create_modelBF()

    array = nut_bolt_array.get_modelsBF()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(array, color='YELLOW', update=True)
    # display.DisplayShape(parray, color= 'BLUE', update=True)
    display.DisableAntiAliasing()
    start_display()
