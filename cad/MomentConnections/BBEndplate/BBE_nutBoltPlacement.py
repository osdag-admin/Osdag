"""created on 19-01-2018
@author: Siddhesh C.
modified: Darshan Vishwakarma (12-09-2020)
"""
import numpy as np

from cad.items.bolt import Bolt
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt


class BBENutBoltArray(object):
    def __init__(self, module, nut, bolt, numberOfBolts, nut_space):
        """
        :param uiObjWeld: User inputs 
        :param beamDim: Beam dimensions
        :param boltPlaceObj: Output dictionary required for bolt placement
        :param nut: Required nut dimensions
        :param bolt: Required bolt dimensions
        :param numberOfBolts: Required number of bolts
        :param nut_space: Gap between bolt head and nut
        :param alist: Input dictionary
        """
        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None
        self.module = module
        self.bolt = bolt
        self.nut = nut
        self.numOfBolts = numberOfBolts
        self.gap = nut_space
        self.plateProjection = self.module.projection

        self.initBoltPlaceParams(module, numberOfBolts)

        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()

        self.positions = []

        self.models = []

    def initialiseNutBolts(self):
        '''
        Initialise the Nut and Bolt 
        '''
        b = self.bolt
        n = self.nut
        for i in range(self.numOfBolts):
            bolt_length_required = float(b.T + self.gap)
            b.H = bolt_length_required + (bolt_length_required - 5) % 5
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParams(self, boltPlaceObj, numberOfBolts):
        '''
        :param boltPlaceObj: Output dictionary of Calculation file 
        :param numberOfBolts: Total number of bolts
        :return: Bolt placement coordinates
        '''
        # self.Lv = boltPlaceObj["Bolt"]["Lv"]
        self.Lv = boltPlaceObj.plate.edge_dist_provided
        self.endDist = boltPlaceObj.end_distance_provided
        self.edgeDist = boltPlaceObj.edge_distance_provided
        self.pitch = boltPlaceObj.pitch_distance_provided
        self.gauge = boltPlaceObj.gauge_distance_provided
        self.mid_bolt_row = boltPlaceObj.bolt_row_web
        self.row = (boltPlaceObj.bolt_row - boltPlaceObj.bolt_row_web)
        self.col = boltPlaceObj.bolt_column
        self.crossCgauge = boltPlaceObj.gauge_cs_distance_provided
        self.pitch_web = boltPlaceObj.pitch_distance_web



        self.endDist_flush = self.plateProjection + boltPlaceObj.beam_tf + self.endDist
        self.endDist_ext = boltPlaceObj.beam_tf + 2 * self.endDist

    def calculatePositions(self, numberOfBolts):
        '''
        The bolt placement is carried out in such a way that bolt @1X1 is considered as Bolt origin and w.r.t this bolt origin,
        rest of the rows ob bolts are placed.
        :return: The position of bolts 
        '''
        self.positions = []

        if self.module.endplate_type == 'Extended Both Ways - Reversible Moment':
            # if numberOfBolts == 8:

            for rw in np.arange(self.row):
                for col in np.arange(self.col):
                    pos = self.origin

                    pos = pos + (self.module.ep_width_provided / 2) * self.gaugeDir

                    if col == 0:
                        pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir
                    elif col < self.col / 2:
                        pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir + (col) * self.gauge * self.gaugeDir
                    else:
                        pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir + (
                                          col - 1) * self.gauge * self.gaugeDir + self.crossCgauge * self.gaugeDir


                    # if rw > 0:
                    if self.row <=6:
                        pos = pos + self.endDist * self.pitchDir
                        if rw == 1:
                            pos = pos + (self.endDist_ext) * self.pitchDir
                        elif rw == 2:
                            pos = pos + (self.module.ep_height_provided - 2*self.endDist  - self.endDist_ext) * self.pitchDir
                        elif rw == 3:
                            pos = pos + (self.module.ep_height_provided - 2*self.endDist ) * self.pitchDir
                        elif rw == 4:
                            pos = pos + (self.endDist_ext) * self.pitchDir + self.pitch * self.pitchDir
                        elif rw>4:
                            pos = pos + (self.module.ep_height_provided - 2*self.endDist  - self.endDist_ext) * self.pitchDir - self.pitch * self.pitchDir
                        else:
                            pass
                    else:
                        pos = pos + self.endDist * self.pitchDir+ self.pitch * self.pitchDir
                        if rw == 1:
                            pos = pos + (self.endDist_ext) * self.pitchDir
                        elif rw == 2:
                            pos = pos + (self.module.ep_height_provided - 2 * self.endDist - self.endDist_ext -2* self.pitch) * self.pitchDir
                        elif rw == 3:
                            pos = pos + (self.module.ep_height_provided - 2 * self.endDist-2* self.pitch) * self.pitchDir
                        elif rw == 4:
                            pos = pos + (self.endDist_ext) * self.pitchDir + self.pitch * self.pitchDir
                        elif rw == 5:
                            pos = pos + (self.module.ep_height_provided - 2 * self.endDist-2* self.pitch - self.endDist_ext) * self.pitchDir - self.pitch * self.pitchDir
                        elif rw == 6:
                            pos = pos - self.pitch * self.pitchDir
                        elif rw == 7:
                            pos = pos + (self.module.ep_height_provided - 2 * self.endDist - self.pitch) * self.pitchDir
                        elif rw >7 and rw%2==0:
                            pos = pos + (self.endDist_ext)*self.pitchDir + (rw/2-2)* self.pitch*self.pitchDir
                        elif rw > 7 and rw % 2 != 0:
                            pos = pos + (self.module.ep_height_provided - 2 * self.endDist - self.endDist_ext - 2 * self.pitch) * self.pitchDir - (rw/2-2.5)* self.pitch*self.pitchDir
                        else:
                            pass
                    self.positions.append(pos)

            if self.mid_bolt_row > 0:
                for rw in np.arange(self.mid_bolt_row):
                    for col in np.arange(self.col):
                        pos = self.origin

                        pos = pos + (self.module.ep_width_provided / 2) * self.gaugeDir

                        if col == 0:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir
                        elif col < self.col / 2:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir + (
                                      col) * self.gauge * self.gaugeDir
                        else:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir + (
                                          col - 1) * self.gauge * self.gaugeDir + self.crossCgauge * self.gaugeDir

                        if self.row < 5:
                            pos = pos + (self.endDist + self.endDist_ext) * self.pitchDir
                            pos = pos + (rw + 1) * self.pitch_web * self.pitchDir
                        elif self.row < 7:
                            pos = pos + (self.endDist + self.endDist_ext + self.pitch) * self.pitchDir
                            pos = pos + (rw + 1) * self.pitch_web * self.pitchDir
                        else:
                            pos = pos + (self.endDist + self.endDist_ext + 2 * self.pitch + ((self.row-8)/2)*self.pitch) * self.pitchDir
                            pos = pos + (rw + 1) * self.pitch_web * self.pitchDir

                        self.positions.append(pos)


        elif self.module.endplate_type =='Extended One Way - Irreversible Moment':

            for rw in np.arange(self.row):
                for col in np.arange(self.col):
                    pos = self.origin

                    pos = pos + (self.module.ep_width_provided / 2) * self.gaugeDir

                    if col == 0:
                        pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir
                    elif col < self.col / 2:
                        pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir + (col) * self.gauge * self.gaugeDir
                    else:
                        pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir + (
                                          col - 1) * self.gauge * self.gaugeDir + self.crossCgauge * self.gaugeDir

                    pos = pos + self.endDist * self.pitchDir
                    if rw>0:
                        if self.row < 5:
                            if rw == 1:
                                pos = pos + (self.endDist_ext ) * self.pitchDir
                            elif rw == 2:
                                pos = pos + (self.module.ep_height_provided-self.endDist_flush-self.endDist) * self.pitchDir
                            else:
                                pos = pos + (self.endDist_ext ) * self.pitchDir + self.pitch * self.pitchDir

                        else:
                            if rw == 1:
                                pos = pos + (self.pitch) * self.pitchDir
                            elif rw == (self.row -1):
                                pos = pos + (self.module.ep_height_provided-self.endDist_flush-self.endDist) * self.pitchDir
                            else:
                                pos = pos + (self.endDist_ext) * self.pitchDir + (rw-1)*self.pitch * self.pitchDir

                    self.positions.append(pos)

            if self.mid_bolt_row > 0:
                for rw in np.arange(self.mid_bolt_row):
                    for col in np.arange(self.col):
                        pos = self.origin

                        pos = pos + (self.module.ep_width_provided / 2) * self.gaugeDir

                        if col == 0:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir
                        elif col < self.col / 2:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir + (
                                      col) * self.gauge * self.gaugeDir
                        else:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                    self.col / 2 - 1) * self.gauge * self.gaugeDir + (
                                          col - 1) * self.gauge * self.gaugeDir + self.crossCgauge * self.gaugeDir


                        if self.row < 4:
                            pos = pos + (self.endDist + self.endDist_ext) * self.pitchDir
                            pos = pos + (rw + 1) * self.pitch_web * self.pitchDir
                        elif self.row < 5:
                            pos = pos + (self.endDist + self.endDist_ext + self.pitch) * self.pitchDir
                            pos = pos + (rw + 1) * self.pitch_web * self.pitchDir
                        else:
                            pos = pos + (self.endDist + self.endDist_ext + 2 * self.pitch + (self.row -5) * self.pitch) * self.pitchDir
                            pos = pos + (rw + 1) * self.pitch_web * self.pitchDir

                        self.positions.append(pos)

        else:
            for rw in np.arange(self.row):
                for col in np.arange(self.col):
                    pos = self.origin

                    pos = pos + (self.module.ep_width_provided/2) * self.gaugeDir

                    if col==0:
                        pos = pos - self.crossCgauge/2 * self.gaugeDir - (self.col/2-1) * self.gauge * self.gaugeDir
                    elif col<self.col/2:
                        pos = pos - self.crossCgauge/2 * self.gaugeDir - (self.col/2-1) * self.gauge * self.gaugeDir + (col) * self.gauge * self.gaugeDir
                    else:
                        pos = pos - self.crossCgauge/2 * self.gaugeDir - (self.col/2-1) * self.gauge * self.gaugeDir + (col-1) * self.gauge * self.gaugeDir + self.crossCgauge * self.gaugeDir

                    pos = pos + self.endDist_flush * self.pitchDir
                    if rw>0:
                        if rw%2==0:
                            pos = pos + ((rw/2) * self.pitch) * self.pitchDir
                        else:
                            pos = pos + (self.module.ep_height_provided - 2*self.endDist_flush - (rw/2-0.5)*self.pitch) * self.pitchDir
                    self.positions.append(pos)

            if self.mid_bolt_row>0:
                for rw in np.arange(self.mid_bolt_row):
                    for col in np.arange(self.col):
                        pos = self.origin

                        pos = pos + (self.module.ep_width_provided / 2) * self.gaugeDir

                        if col == 0:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                        self.col / 2 - 1) * self.gauge * self.gaugeDir
                        elif col < self.col / 2:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                        self.col / 2 - 1) * self.gauge * self.gaugeDir + (
                                      col) * self.gauge * self.gaugeDir
                        else:
                            pos = pos - self.crossCgauge / 2 * self.gaugeDir - (
                                        self.col / 2 - 1) * self.gauge * self.gaugeDir + (
                                              col - 1) * self.gauge * self.gaugeDir + self.crossCgauge * self.gaugeDir

                        pos = pos + self.endDist_flush * self.pitchDir +((self.row/2-1) * self.pitch) * self.pitchDir
                        pos = pos + (rw+1) * self.pitch_web * self.pitchDir
                        self.positions.append(pos)



    def place(self, origin, gaugeDir, pitchDir, boltDir):
        """
        :param origin: Origin for bolt placement 
        :param gaugeDir: gauge distance direction
        :param pitchDir: pitch distance direction
        :param boltDir: bolts screwing direction
        :return: places the bolts and nuts based on the defined bolt arrangement
        """

        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir

        self.calculatePositions(self.numOfBolts)
        print(self.numOfBolts)
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

        dbg = self.dbgSphere(self.origin) #TODO : know why sphere is appended to the model (by Anand Swaroop)
        self.models.append(dbg)

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
        return self.models
