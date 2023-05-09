'''
Created on 19-April-2020

@author : Anand Swaroop
'''

from cad.items.bolt import Bolt
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.plate import Plate


class NutBoltArray():
    """
    add a diagram here
    """

    def __init__(self, Obj, nut, bolt, nut_space):

        self.nut = nut
        self.bolt = bolt

        self.Obj = Obj

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.gap = nut_space

        self.initBoltPlaceParams()

        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()

        self.positions = []

        self.models = []

        # if Obj == 'Channels' or Obj == 'Back to Back Channels':
        #     self.member_thickness = #Obj.section_size_1.flange_thickness
        # else:
        #     self.member_thickness = #Obj.section_size_1.thickness

    def initialiseNutBolts(self):
        '''
        Initializing the Nut Bolt
        '''
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            bolt_len_required = float(b.T + self.gap)
            b.H = bolt_len_required + (bolt_len_required) % 5
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParams(self):

        self.pitch = 45  # Obj.plate.pitch_provided
        self.gauge = 35  # Obj.plate.gauge_provided
        self.edge = 35  # Obj.plate.edge_dist_provided
        self.end = 35  # Obj.plate.end_dist_provided
        self.row = 2  # Obj.plate.bolts_one_line
        self.col = 2  # Obj.plate.bolt_line
        self.memberdeepth = 125
        self.member_thickness = 6.6
        self.member_web_thickness = 3
        self.root_radius = 6


    def calculatePositions(self):
        """
        Calculates the exact position for nut and bolts.
        """
        self.positions = []
        for rw in range(self.row):
            for col in range(self.col):
                pos = self.origin
                pos = pos + (self.member_thickness + self.root_radius) * self.gaugeDir
                pos = pos + self.edge * self.gaugeDir
                pos = pos + col * self.pitch * self.pitchDir
                pos = pos + self.end * self.pitchDir
                pos = pos + rw * self.gauge * self.gaugeDir

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

        nut_bolts = self.models
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_models(self):
        nut_bolts = self.models
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array


if __name__ == '__main__':
    from cad.items.bolt import Bolt
    from cad.items.nut import Nut
    from cad.items.plate import Plate
    import numpy

    from OCC.gp import gp_Pnt
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    nutboltArrayOrigin = numpy.array([0., 0., 0.])
    gaugeDir = numpy.array([0.0, 1.0, 0])
    pitchDir = numpy.array([1.0, 0.0, 0])
    boltDir = numpy.array([0, 0, 1.0])

    bolt = Bolt(R=6, T=5, H=6, r=3)
    nut = Nut(R=bolt.R, T=bolt.T, H=bolt.T + 1, innerR1=bolt.r)
    nut_space = 10 + 5 + nut.T  # member.T + plate.T + nut.T
    Obj = 'Star Angles'  # 'Back to Back Channels'  #'Channels'  #'  #'Angles'  #      or 'Back to Back Angles' 'Channels' or

    nut_bolt_array = NutBoltArray(Obj, nut, bolt, nut_space)
    #
    # intermittentPlate = Plate(L= 35+35+35, W=35+35,  T = 10)
    # nut_bolt_array = IntermittentNutBoltPlateArray(Obj, nut, bolt, intermittentPlate, nut_space)
    #
    # place = nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    nut_bolt_array_Model = nut_bolt_array.create_model()

    array = nut_bolt_array.get_models()
    # nbarray = nut_bolt_array.get_nut_bolt_models()
    # parray = nut_bolt_array.get_plate_models()
    # array = nut_bolts[0]
    # for comp in nut_bolts:
    #     array = BRepAlgoAPI_Fuse(comp, array).Shape()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(array, color='YELLOW', update=True)
    # display.DisplayShape(parray, color= 'BLUE', update=True)
    display.DisableAntiAliasing()
    start_display()
