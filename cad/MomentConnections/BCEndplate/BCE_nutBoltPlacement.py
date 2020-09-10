"""created on 24-04-2019

@author: Anand Swaroop.
"""

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

import numpy as np
from cad.items.bolt import Bolt
from cad.items.nut import Nut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from cad.items.ModelUtils import getGpPt



class BCE_NutBoltArray(object):
    # def __init__(self, uiObjWeld, beamDim, boltPlaceObj, nut, bolt, numberOfBolts, nut_space, endplate_type):
    def __init__(self, boltPlaceObj, nut, bolt, numberOfBolts, nut_space, endplate_type):

        """
        :param uiObjWeld: User inputs 
        :param beamDim: Beam dimensions
        :param boltPlaceObj: Output dictionary required for bolt placement
        :param nut: Required nut dimensions
        :param bolt: Required bolt dimensions
        :param numberOfBolts: Required number of bolts
        :param nut_space: Gap between bolt head and nut
        """
        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir = None

        # self.uiObjW = uiObjWeld
        # self.beamDim = beamDim
        self.bolt = bolt
        self.nut = nut
        self.numOfBolts = numberOfBolts
        self.gap = nut_space
        self.endplate_type = endplate_type

        self.initBoltPlaceParams(boltPlaceObj, numberOfBolts)

        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()
        self.boltProjection = 10.0
        self.positions = []

        self.models = []
        # self.uiObjW["Weld"]["Flange (mm)"] = 0.0

    def initialiseNutBolts(self):
        '''

        :return: Initialise the Nut and Bolt
        '''
        b = self.bolt
        n = self.nut
        for i in range(self.numOfBolts):
            bolt_length_required = float(b.T + self.gap)  #
            b.H = bolt_length_required + (bolt_length_required - 5) % 5
            self.bolts.append(Bolt(b.R, b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T, n.H, n.r1))

    def initBoltPlaceParams(self, boltPlaceObj, numberOfBolts):
        '''
        :param boltPlaceObj: Output dictionary of Calculation file 
        :param numberOfBolts: Total number of bolts
        :return: Bolt placement coordinates
        '''
        self.Lv = boltPlaceObj.plate.edge_dist_provided
        self.endDist = boltPlaceObj.plate.end_dist_provided
        self.edgeDist = boltPlaceObj.plate.edge_dist_provided
        self.crossCgauge = float(boltPlaceObj.plate.width) - 2 * float(self.edgeDist)
        self.row = boltPlaceObj.plate.bolt_line
        self.col = boltPlaceObj.plate.bolts_one_line
        self.pitch = boltPlaceObj.plate.pitch_provided
        # if self.endplate_type != "Flush end plate":
        self.out_pitch = boltPlaceObj.outside_pitch
        self.out_bolt = boltPlaceObj.out_bolt
        self.gauge = boltPlaceObj.plate.gauge_provided
        self.midgauge = 2 * boltPlaceObj.plate.edge_dist_provided + boltPlaceObj.supported_section.web_thickness
        self.endDist_flush = 10 + boltPlaceObj.supported_section.flange_thickness + self.endDist
        self.endDist_ext = boltPlaceObj.supported_section.flange_thickness + 2 * self.endDist

        # if self.endplate_type == "both_way":
        #     if numberOfBolts == 8:
        #         self.pitch23 = boltPlaceObj["Bolt"]["Pitch"]
        #         # self.endDist = boltPlaceObj["Bolt"]["End"]
        #         # self.edgeDist = boltPlaceObj["Bolt"]["Edge"]
        #         # self.crossCgauge = float(boltPlaceObj["Plate"]["Width"]) - 2 * float(self.edgeDist)
        #         self.row = numberOfBolts / 2
        #         # self.col = 2
        #     elif numberOfBolts == 12:
        #         self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
        #         self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
        #         self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]
        #         # self.endDist = boltPlaceObj["Bolt"]["End"]
        #         # self.edgeDist = boltPlaceObj["Bolt"]["Edge"]
        #         # self.crossCgauge = boltPlaceObj["Plate"]["Width"] - 2 * self.edgeDist
        #         # self.row = numberOfBolts / 2
        #         # self.col = 2
        #     elif numberOfBolts == 16:
        #         self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
        #         self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
        #         self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]
        #         self.pitch56 = boltPlaceObj["Bolt"]["Pitch56"]
        #         self.pitch67 = boltPlaceObj["Bolt"]["Pitch67"]
        #         # self.endDist = boltPlaceObj["Bolt"]["End"]
        #         # self.edgeDist = boltPlaceObj["Bolt"]["Edge"]
        #         # self.crossCgauge = boltPlaceObj["Plate"]["Width"] - 2 * self.edgeDist
        #         # self.row = numberOfBolts / 2
        #         # self.col = 2
        #     elif numberOfBolts == 20:
        #         self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]
        #         self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
        #         self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]
        #         self.pitch56 = boltPlaceObj["Bolt"]["Pitch56"]
        #         self.pitch67 = boltPlaceObj["Bolt"]["Pitch67"]
        #         self.pitch78 = boltPlaceObj["Bolt"]["Pitch78"]
        #         self.pitch910 = boltPlaceObj["Bolt"]["Pitch910"]
        #         # self.endDist = boltPlaceObj["Bolt"]["End"]
        #         # self.edgeDist = boltPlaceObj["Bolt"]["Edge"]
        #         # self.crossCgauge = boltPlaceObj["Plate"]["Width"] - 2 * self.edgeDist
        #         # self.row = numberOfBolts / 2
        #         # self.col = 2
        # elif self.endplate_type == "one_way":
        #     # pass
        #
        #     if numberOfBolts == 6:
        #         self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
        #         self.endDist = boltPlaceObj["Bolt"]["End"]
        #
        #     elif numberOfBolts == 8:
        #         self.pitch23 = boltPlaceObj['Bolt']['Pitch23']
        #         self.pitch34 = boltPlaceObj['Bolt']['Pitch34']
        #
        #     elif numberOfBolts == 10:
        #         self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]
        #         self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
        #         self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
        #         self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]
        #
        #     else:  # 1 numberOfBolts == 12:
        #         self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]
        #         self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
        #         self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
        #         self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]
        #         self.pitch56 = boltPlaceObj["Bolt"]["Pitch56"]
        #
        #
        # elif self.endplate_type == "flush":
        #
        #     if numberOfBolts == 4:
        #         self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]  # 250      #
        #
        #     elif numberOfBolts == 8:
        #         self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]  # 50       #] # TODO give dictionary values here
        #         self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]  # 150      #
        #         self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]  # 50       #
        #
        #     elif numberOfBolts == 12:
        #         self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]
        #         self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
        #         self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
        #         self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]
        #         self.pitch56 = boltPlaceObj["Bolt"]["Pitch56"]

    def calculatePositions(self, numberOfBolts):
        '''
        The bolt placement is carried out in such a way that bolt @1X1 is considered as Bolt origin and w.r.t this bolt origin,
        rest of the rows ob bolts are placed.
        :return: The position of bolts 
        '''
        self.positions = []

        if self.endplate_type == "Extended both ways":
            # if numberOfBolts == 8:

            for rw in np.arange(self.row + self.out_bolt):
                for col in np.arange(self.col):
                    pos = self.origin
                    pos = pos + (self.edgeDist) * self.gaugeDir

                    if col == self.col / 2:
                        pos = pos + 1 * self.midgauge * self.gaugeDir + (col - 1) * self.gauge * self.gaugeDir
                    else:
                        if col < self.col / 2:
                            pos = pos + col * self.gauge * self.gaugeDir
                        else:
                            pos = pos + 1 * self.midgauge * self.gaugeDir + (col - 1) * self.gauge * self.gaugeDir
                    pos = pos + (self.endDist) * self.pitchDir

                    if rw > (self.out_bolt / 2 - 1):
                        pos = pos + self.endDist_ext * self.pitchDir

                    if rw > (self.out_bolt / 2 - 1) and rw < ((self.out_bolt / 2 + self.row)):
                        pos = pos + (rw - 1) * self.pitch * self.pitchDir
                    elif rw > ((self.out_bolt / 2 + self.row) - 1):
                        pos = pos + (rw - 2) * self.pitch * self.pitchDir
                    else:
                        pos = pos + rw * self.pitch * self.pitchDir

                    if rw > ((self.out_bolt / 2 + self.row) - 1):
                        pos = pos + self.endDist_ext * self.pitchDir

                    self.positions.append(pos)


        elif self.endplate_type == "Extended one way":

            for rw in np.arange(self.row + self.out_bolt):
                for col in np.arange(self.col):
                    pos = self.origin
                    pos = pos + (self.edgeDist) * self.gaugeDir

                    if col == self.col / 2:
                        pos = pos + 1 * self.midgauge * self.gaugeDir + (col - 1) * self.gauge * self.gaugeDir
                    else:
                        if col < self.col / 2:
                            pos = pos + col * self.gauge * self.gaugeDir
                        else:
                            pos = pos + 1 * self.midgauge * self.gaugeDir + (col - 1) * self.gauge * self.gaugeDir
                    pos = pos + (self.endDist) * self.pitchDir
                    if rw > (self.out_bolt - 1):
                        pos = pos + self.endDist_ext * self.pitchDir
                    if rw > (self.out_bolt - 1):
                        pos = pos + (rw - 1) * self.pitch * self.pitchDir
                    else:
                        pos = pos + rw * self.pitch * self.pitchDir

                    self.positions.append(pos)

        else:
            for rw in np.arange(self.row):
                for col in np.arange(self.col):
                    pos = self.origin
                    pos = pos + (self.edgeDist) * self.gaugeDir
                    if col == self.col / 2:
                        pos = pos + 1 * self.midgauge * self.gaugeDir + (col - 1) * self.gauge * self.gaugeDir
                    else:
                        if col < self.col / 2:
                            pos = pos + col * self.gauge * self.gaugeDir
                        else:
                            pos = pos + 1 * self.midgauge * self.gaugeDir + (col - 1) * self.gauge * self.gaugeDir
                    pos = pos + self.endDist_flush * self.pitchDir
                    pos = pos + rw * self.pitch * self.pitchDir

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

        self.calculatePositions(self.numOfBolts)

        for index, pos in enumerate(self.positions):
            self.bolts[index].place(pos, gaugeDir, boltDir)
            self.nuts[index].place((pos + self.gap * boltDir), gaugeDir,
                                   -boltDir)  # gap here is between bolt head and nut

    def create_model(self):
        for bolt in self.bolts:
            self.models.append(bolt.create_model())

        for nut in self.nuts:
            self.models.append(nut.create_model())

        dbg = self.dbgSphere(self.origin)
        self.models.append(dbg)

    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 0.1).Shape()

    def get_models(self):
        return self.models

    def get_bolt_list(self):
        boltlist = []
        for bolt in self.bolts:
            boltlist.append(bolt.create_model())
            dbg = self.dbgSphere(self.origin)
            self.models.append(dbg)

        return boltlist
