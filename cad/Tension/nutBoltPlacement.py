'''
Created on 19-April-2020

@author : Anand Swaroop
'''

from cad.items.bolt import Bolt
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse


class NutBoltArray():
    """
    add a diagram here
    """

    def __init__(self, plateObj, nut, bolt, nut_space):

        self.nut = nut
        self.bolt = bolt

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.gap = nut_space

        self.initBoltPlaceParams(plateObj)

        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()

        self.positions = []

        self.models = []

        if plateObj.sec_profile == 'Channels' or plateObj.sec_profile == 'Back to Back Channels':
            self.member_thickness = plateObj.section_size_1.flange_thickness
        else:
            self.member_thickness = plateObj.section_size_1.thickness
        self.root_radius = plateObj.section_size_1.root_radius
        # print(self.root_radius,self.member_thickness,"rad and thk")
    def initialiseNutBolts(self):
        '''
        Initializing the Nut Bolt
        '''
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            bolt_len_required = float(self.gap)
            b.H = bolt_len_required + 10
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParams(self, plateObj):

        self.pitch = plateObj.plate.pitch_provided
        self.gauge = plateObj.plate.gauge_provided
        self.edge = plateObj.plate.edge_dist_provided
        # print(self.edge,"edge")
        self.end = plateObj.plate.end_dist_provided
        self.row = plateObj.plate.bolts_one_line
        self.col = plateObj.plate.bolt_line

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
    plateObj = 0.0

    nut_bolt_array = NutBoltArray(plateObj, nut, bolt, nut_space)

    place = nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    nut_bolt_array_Model = nut_bolt_array.create_model()

    array = nut_bolt_array.get_models()
    # array = nut_bolts[0]
    # for comp in nut_bolts:
    #     array = BRepAlgoAPI_Fuse(comp, array).Shape()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(array, update=True)
    display.DisableAntiAliasing()
    start_display()
