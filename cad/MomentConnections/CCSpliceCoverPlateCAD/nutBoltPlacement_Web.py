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


class NutBoltArray_Web():
    def __init__(self, Obj, nut, bolt, numOfboltsW, nutSpaceW):
        """
        :param alist: Input values, entered by user
        :param beam_data: Beam dimensions
        :param outputobj: Output dictionary
        :param nut: Nut dimensions
        :param bolt: Bolt dimensions
        :param numOfboltsF: Number of bolts required for over plate above flange
        :param nutSpaceF: Spacing between bolt head and nut
        """
        self.boltOrigin_W = None
        self.originW = None
        self.gaugeDirW = None
        self.pitchDirW = None
        self.boltDirW = None

        # self.uiObj = alist
        # self.beamDim = beam_data
        self.bolt = bolt
        self.nut = nut
        self.numOfboltsW = numOfboltsW
        self.nutSpaceW = nutSpaceW

        self.initBoltPlaceParams_Web(Obj)
        self.bolts_W = []
        self.nuts_W = []
        self.initialiseNutBolts_Web()
        self.positions_W = []
        self.models_W = []

    #################################################################
    #           Nut_Bolt placement over Web of beam                 #
    #################################################################

    def initialiseNutBolts_Web(self):
        '''
        :return: This initializes required number of bolts and nuts for web bolting.
        '''
        b_W = self.bolt
        n_W = self.nut
        for k in range(self.numOfboltsW):
            bolt_length_required = float(n_W.H + self.nutSpaceW)
            b_W.H = bolt_length_required + 10
            self.bolts_W.append(Bolt(b_W.R, b_W.T, b_W.H, b_W.r))
            self.nuts_W.append(Nut(n_W.R, n_W.T, n_W.H, n_W.r1))

    def initBoltPlaceParams_Web(self, Obj):
        '''
        :param outputobj: This is output dictionary for bolt placement parameters
        :return: Edge, end, gauge and pitch distances for placement
        '''
        self.edge_W = Obj.web_plate.edge_dist_provided  # 33
        self.end_W = Obj.web_plate.end_dist_provided  # 33
        # self.pitch_W = 150     #70
        # self.gauge_W = outputobj.web_plate.length - 2* self.edge_W
        self.pitch_W = Obj.web_plate.pitch_provided
        self.pitch_MW = Obj.web_plate.midpitch  # todo for gap
        self.gauge_W = Obj.web_plate.gauge_provided

        self.row_W = Obj.web_plate.bolts_one_line
        self.col_W = Obj.web_plate.bolt_line

    def calculatePositions_Web(self):
        """

        :return: The positions/coordinates to place the bolts in the form of list, positions_W = [list of bolting coordinates]
        """
        self.positions_W = []
        # self.boltOrigin_W = self.originW - ((self.row_W/2 * self.gauge_W) - self.end_W/2) * self.pitchDirW - (((self.col_W/2)*self.pitch_W)*self.gaugeDirW)
        self.boltOrigin_W = self.originW + self.end_W * self.pitchDirW + (self.edge_W) * self.gaugeDirW
        for rw_W in range(self.row_W):
            for cl_W in range(self.col_W):
                pos_W = self.boltOrigin_W
                pos_W = pos_W + rw_W * self.gauge_W * self.pitchDirW
                print(self.gauge_W)
                if self.col_W / 2 > cl_W:
                    pos_W = pos_W + cl_W * self.pitch_W * self.gaugeDirW
                else:
                    pos_W = pos_W + (cl_W - 1) * self.pitch_W * self.gaugeDirW + 1 * self.pitch_MW * self.gaugeDirW
                self.positions_W.append(pos_W)
                # else:
                #     pos_AF = pos_AF + rw_W * self.pitch_AF * self.pitchDirAF
                #     if self.col_AF / 2 > cl_AF:
                #         pos_AF = pos_AF + cl_AF * self.gauge * self.gaugeDirAF
                #     else:
                #         pos_AF = pos_AF + (
                #                     cl_AF - 1) * self.gauge * self.gaugeDirAF + 1 * self.gauge_AF * self.gaugeDirAF
                #     self.positions_AF.append(pos_AF)

                # pos_W = pos_W + rw_W * self.pitch_W * self.pitchDirW
                # pos_W = pos_W + cl_W * self.gauge_W * self.gaugeDirW
                # pos_W = pos_W + rw_W * self.gauge_W * self.pitchDirW
                # pos_W = pos_W + cl_W * self.pitch_W * self.gaugeDirW
                #
                #
                # self.positions_W.append(pos_W)

    def placeW(self, originW, gaugeDirW, pitchDirW, boltDirW):
        """
        :param originW: Origin for bolt placement
        :param gaugeDirW: Gauge direction for gauge distance
        :param pitchDirW: Pitch direction for pitch distance
        :param boltDirW: Bolt screwing direction
        :return:
        """
        self.originW = originW
        self.gaugeDirW = gaugeDirW
        self.pitchDirW = pitchDirW
        self.boltDirW = boltDirW

        self.calculatePositions_Web()
        for index_W, pos_W in enumerate(self.positions_W):
            self.bolts_W[index_W].place(pos_W, gaugeDirW, boltDirW)
            self.nuts_W[index_W].place((pos_W + self.nutSpaceW * boltDirW), gaugeDirW, boltDirW)

    def create_modelW(self):
        for bolt in self.bolts_W:
            self.models_W.append(bolt.create_model())
            pass
        for nut in self.nuts_W:
            self.models_W.append(nut.create_model())
            pass

        dbg = self.dbgSphere(self.originW)
        self.models_W.append(dbg)

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_modelsW(self):
        return self.models_W

    def get_bolt_web_list(self):
        boltlist = []
        for bolt in self.bolts_W:
            boltlist.append(bolt.create_model())
            dbg = self.dbgSphere(self.originW)
            self.models_W.append(dbg)
        return boltlist

    def get_bolt_listRB(self):
        boltlist = []
        for bolt in self.bolts_W:
            boltlist.append(bolt.create_model())
            dbg = self.dbgSphere(self.originW)
            self.models_W.append(dbg)
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

    nut_bolt_array = NutBoltArray_Web(Obj, nut, bolt, numOfboltsF, nut_space)

    nut_bolt_array.placeW(nutboltArrayOrigin, pitchDir, gaugeDir, boltDir)
    nut_bolt_array.create_modelW()

    array = nut_bolt_array.get_modelsW()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(array, color='YELLOW', update=True)
    # display.DisplayShape(parray, color= 'BLUE', update=True)
    display.DisableAntiAliasing()
    start_display()
