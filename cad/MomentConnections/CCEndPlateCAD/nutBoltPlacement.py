"""
created on 02-06-2020
@auther: Anand Swaroop
"""

import numpy as np
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from cad.items.ModelUtils import getGpPt
from cad.items.bolt import Bolt
from cad.items.nut import Nut


class NutBoltArray(object):
    def __init__(self, Obj, nut, bolt, nut_space):
        self.Obj = Obj
        self.nut = nut
        self.bolt = bolt
        self.gap = nut_space

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.initBoltPlaceParams()

        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()

        self.positions = []

        self.models = []

    def initialiseNutBolts(self):
        """
        Initialise the Nut and Bolt 
        """
        b = self.bolt
        n = self.nut
        for i in range(self.numOfBolts):
            bolt_length_required = float(b.T + self.gap)
            b.H = bolt_length_required + (bolt_length_required - 5) % 5
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParams(self):
        self.row = 3
        self.col = 4
        self.numOfBolts = self.row * self.col
        self.endDist = 65
        self.edgeDist = 55.45
        self.pitch = 82.5
        self.p2flange = 122.3
        if self.col == 2:
            self.gauge = [self.edgeDist, 65 + 12.7 + 65]  # end+T+end
        elif self.col == 4:
            self.gauge = [self.endDist, self.endDist + self.p2flange,
                          self.endDist + self.p2flange + 2 * self.endDist + 10,
                          self.endDist + self.p2flange + 2 * self.endDist + 10 + self.p2flange]
        elif self.col == 6:
            self.gauge = [self.endDist, self.endDist + self.p2flange, self.endDist + self.p2flange + self.p2flange,
                          self.endDist + self.p2flange + self.p2flange + 2 * self.endDist + 10,
                          self.endDist + self.p2flange + self.p2flange + 2 * self.endDist + 10 + self.p2flange,
                          self.endDist + self.p2flange + self.p2flange + 2 * self.endDist + 10 + self.p2flange + self.p2flange]
        elif self.col == 8:
            self.gauge = [self.endDist, self.endDist + self.pitch, self.endDist + self.pitch + self.p2flange,
                          self.endDist + self.pitch + self.p2flange + self.pitch,
                          self.endDist + self.pitch + self.p2flange + self.pitch + 2 * self.endDist + 10,
                          self.endDist + self.pitch + self.p2flange + self.pitch + 2 * self.endDist + 10 + self.pitch,
                          self.endDist + self.pitch + self.p2flange + self.pitch + 2 * self.endDist + 10 + self.pitch + self.p2flange,
                          self.endDist + self.pitch + self.p2flange + self.pitch + 2 * self.endDist + 10 + self.pitch + self.p2flange + self.pitch]

    def calculatePositions(self):
        self.positions = []
        # Todo: if member == flush:
        self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir
        self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir
        for col in range(self.col):
            for rw in range(self.row):
                pos = self.boltOrigin
                pos = pos + rw * self.p2flange * self.pitchDir
                pos = pos + self.gauge[col] * self.gaugeDir

                self.positions.append(pos)
        # 4 column bolts
        # elif self.col == 4:
        #     self.boltOrigin = self.origin + self.endDist * self.gaugeDir
        #     self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir
        #     for col in range(self.col):
        #         if col <= 2:
        #             for rw in range(self.row)

    def place(self, origin, gaugeDir, pitchDir, boltDir):
        """
        :param origin: Origin for bolt placement 
        :param gaugeDir: gauge distance direction
        :param pitchDir: pitch distance direction
        :param boltDir: bolts screwing direction
        :return: 
        """

        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir

        self.calculatePositions()

        for index, pos in enumerate(self.positions):
            self.bolts[index].place(pos, gaugeDir, boltDir)
            self.nuts[index].place((pos + self.gap * boltDir), gaugeDir,
                                   -boltDir)  # gap here is between bolt head and nut

    def create_model(self):
        """

        :return: cad model of nut bolt arrangement
        """
        for bolt in self.bolts:
            self.models.append(bolt.create_model())

        for nut in self.nuts:
            self.models.append(nut.create_model())

        dbg = self.dbgSphere(self.origin)  # TODO : know why sphere is appended to the model (by Anand Swaroop)
        self.models.append(dbg)

        nut_bolts = self.models
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array

    def dbgSphere(self, pt):
        """
        TODO : know why sphere is appended to the model, if no reason than remove sphere from all the cad files (by Anand Swaroop)
        :param pt: pt of origin for the nut bol placement
        :return: returns the sphere
        """
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_models(self):
        """

        :return: cad model for nut and bolt arrangement
        """
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
    Obj = '6'

    nut_bolt_array = NutBoltArray(Obj, nut, bolt, nut_space)

    nut_bolt_array.place(nutboltArrayOrigin, pitchDir, gaugeDir, boltDir)
    nut_bolt_array.create_model()

    array = nut_bolt_array.get_models()

    Point = gp_Pnt(0.0, 0.0, 0.0)
    display.DisplayMessage(Point, "Origin")

    display.DisplayShape(array, color='YELLOW', update=True)
    # display.DisplayShape(parray, color= 'BLUE', update=True)
    display.DisableAntiAliasing()
    start_display()
