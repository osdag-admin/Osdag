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
    def __init__(self, Obj, column, nut, bolt, nut_space):

        self.Obj = Obj
        self.column = column
        self.nut = nut
        self.bolt = bolt
        self.gap = nut_space

        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        self.initBoltPlaceParams(Obj)

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

    def initBoltPlaceParams(self, Obj):
        self.row = int(Obj.n_bw)  # int(Obj.n_bw)  # 4    #         #4
        self.col = int(Obj.n_bf) * 2  # 2  # int(Obj.n_bf * 2)  #4    #        #4
        self.webcol = 2
        self.numOfBolts = Obj.no_bolts  # 12    #
        self.endDist = Obj.end_dist

        self.pitch = Obj.pitch
        self.p2flange = Obj.p_2_flange
        self.p2web = Obj.p_2_web
        # self.webColgauge = 2 * self.endDist + self.column.t
        self.edgeDist = self.column.B / 2 - self.endDist - self.column.t / 2
        # todo for flush plate
        if Obj.connection == "Flush End Plate":
            if self.row == 2:
                self.pitchDist = [self.endDist + self.column.T, self.p2web]
            elif self.row == 3:
                self.pitchDist = [self.endDist + self.column.T, self.p2web, self.p2web]
            elif self.row == 4:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.p2web, self.pitch]
            elif self.row == 5:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.p2web, self.p2web, self.pitch]

            elif self.row == 6:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch]
            elif self.row == 7:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.p2web, self.p2web, self.pitch, self.pitch]
            elif self.row == 8:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.pitch, self.p2web, self.pitch, self.pitch, self.pitch]
            elif self.row == 9:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch]
            elif self.row == 10:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 11:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.pitch, self.pitch,self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 12:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 13:
                self.pitchDist = [self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 14:
                self.pitchDist = [self.endDist + self.column.T, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 15:
                self.pitchDist = [self.endDist + self.column.T, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 16:
                self.pitchDist = [self.endDist + self.column.T, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 17:
                self.pitchDist = [self.endDist + self.column.T, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 18:
                self.pitchDist = [self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 19:
                self.pitchDist = [self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]

            elif self.row == 20:
                self.pitchDist = [self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.p2web, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch]


        elif Obj.connection == "Extended Both Ways":
            self.row = self.row + 2
            if self.row == 4:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.p2web,
                                  2 * self.endDist + self.column.T]
            elif self.row == 5:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.p2web, self.p2web,
                                  2 * self.endDist + self.column.T]
            elif self.row == 6:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch,
                                  self.p2web, self.pitch, 2 * self.endDist + self.column.T]
            elif self.row == 7:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch,
                                  self.p2web, self.p2web, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 8:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch, 2 * self.endDist + self.column.T]
            elif self.row == 9:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch,
                                  self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 10:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 11:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 12:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 13:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 14:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 15:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 16:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 17:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 18:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 19:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch,self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch,self.pitch, self.pitch,
                                  self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 20:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 21:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch,self.pitch, self.p2web, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch,self.pitch, self.pitch,
                                  self.pitch, self.pitch, 2 * self.endDist + self.column.T]

            elif self.row == 22:
                self.pitchDist = [self.endDist, 2 * self.endDist + self.column.T, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.p2web, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch, self.pitch,
                                  self.pitch, self.pitch, 2 * self.endDist + self.column.T]

        if self.col == 2:
            self.gauge = [self.edgeDist, 2 * self.endDist + self.column.t]  # end+T+end

        elif self.col == 4:
            self.gauge = [self.endDist, self.p2flange, 2 * self.endDist + self.column.t, self.p2flange]
        elif self.col == 6:
            self.gauge = [self.endDist, self.p2flange, self.p2flange, 2 * self.endDist + self.column.t, self.p2flange,
                          self.p2flange]

        elif self.col == 8:
            self.gauge = [self.endDist, self.pitch, self.p2flange, self.pitch, 2 * self.endDist + self.column.t,
                          self.pitch, self.p2flange, self.pitch]

        elif self.col == 10:
            self.gauge = [self.endDist, self.pitch, self.p2flange, self.p2flange, self.pitch,
                          self.column.t + 2 * self.endDist, self.pitch, self.p2flange, self.p2flange, self.pitch]

        elif self.col == 12:
            self.gauge = [self.endDist, self.pitch, self.pitch, self.p2flange, self.pitch, self.pitch, 2 * self.endDist + self.column.t,
                          self.pitch, self.pitch, self.p2flange, self.pitch, self.pitch]

        elif self.col == 14:
            self.gauge = [self.endDist, self.pitch, self.pitch, self.p2flange, self.p2flange, self.pitch, self.pitch, 2 * self.endDist + self.column.t,
                          self.pitch, self.pitch, self.p2flange, self.p2flange, self.pitch, self.pitch]

        elif self.col == 16:
            self.gauge = [self.endDist, self.pitch, self.pitch, self.pitch, self.p2flange, self.pitch, self.pitch, self.pitch, 2 * self.endDist + self.column.t,
                          self.pitch, self.pitch, self.pitch, self.p2flange, self.pitch, self.pitch, self.pitch]

    def calculatePositions(self):
        self.positions = []

        # Todo: if member == flush:
        self.boltOrigin = self.origin  # + (self.edgeDist + self.column.t) * self.gaugeDir
        # self.boltOrigin = self.boltOrigin  # + self.endDist * self.pitchDir
        xrow = 0.0
        for rw in range(self.row):
            xcol = 0.0
            xrow = xrow.__add__(self.pitchDist[rw])
            if self.Obj.connection == "Flush End Plate":
                if rw == 0 or rw == self.row - 1:
                    for col in range(self.col):
                        xcol = xcol.__add__(self.gauge[col])
                        pos = self.boltOrigin
                        pos = pos + xrow * self.pitchDir
                        pos = pos + xcol * self.gaugeDir

                        self.positions.append(pos)

                else:
                    for col in range(self.webcol):
                        # xcol = xcol.__add__(self.gauge[col])
                        pos = self.boltOrigin + self.edgeDist * self.gaugeDir
                        pos = pos + xrow * self.pitchDir
                        pos = pos + col * (2 * self.endDist + self.column.t) * self.gaugeDir

                        self.positions.append(pos)

            else:
                if rw == 0 or rw == 1 or rw == self.row - 1 or rw == self.row - 2:
                    for col in range(self.col):
                        xcol = xcol.__add__(self.gauge[col])
                        pos = self.boltOrigin
                        pos = pos + xrow * self.pitchDir
                        pos = pos + xcol * self.gaugeDir

                        self.positions.append(pos)

                else:
                    for col in range(self.webcol):
                        # xcol = xcol.__add__(self.gauge[col])
                        pos = self.boltOrigin + self.edgeDist * self.gaugeDir
                        pos = pos + xrow * self.pitchDir
                        pos = pos + col * (2 * self.endDist + self.column.t) * self.gaugeDir

                        self.positions.append(pos)

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
