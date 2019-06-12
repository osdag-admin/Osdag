"""created on 19-01-2018

@author: Siddhesh C.
"""
from Connections.Component.bolt import Bolt
from Connections.Component.nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from Connections.Component.ModelUtils import getGpPt
import numpy as np


class NutBoltArray(object):
    def __init__(self, uiObjWeld, beamDim, boltPlaceObj, nut, bolt, numberOfBolts, nut_space, alist):
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

        self.uiObjW = uiObjWeld
        self.beamDim = beamDim
        self.bolt = bolt
        self.nut = nut
        self.numOfBolts = numberOfBolts
        self.gap = nut_space
        self.alist = alist
        self.boltProjection = float(boltPlaceObj['Plate']['Projection'])

        self.initBoltPlaceParams(boltPlaceObj, numberOfBolts)

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
        self.Lv = boltPlaceObj["Bolt"]["Lv"]
        self.endDist = boltPlaceObj["Bolt"]["End"]
        self.edgeDist = boltPlaceObj["Bolt"]["Edge"]
        self.crossCgauge = float(boltPlaceObj["Plate"]["Width"]) - 2 * float(self.edgeDist)
        self.row = numberOfBolts / 2
        self.col = 2

        if self.alist["Member"]["Connectivity"] == "Extended both ways":
            if numberOfBolts == 8:
                self.pitch23 = boltPlaceObj["Bolt"]["Pitch"]

            elif numberOfBolts == 12:
                self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
                self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
                self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]

            elif numberOfBolts == 16:
                self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
                self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
                self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]
                self.pitch56 = boltPlaceObj["Bolt"]["Pitch56"]
                self.pitch67 = boltPlaceObj["Bolt"]["Pitch67"]

            elif numberOfBolts == 20:
                self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]
                self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
                self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]
                self.pitch56 = boltPlaceObj["Bolt"]["Pitch56"]
                self.pitch67 = boltPlaceObj["Bolt"]["Pitch67"]
                self.pitch78 = boltPlaceObj["Bolt"]["Pitch78"]
                self.pitch910 = boltPlaceObj["Bolt"]["Pitch910"]

        elif self.alist["Member"]["Connectivity"] == "Extended one way":
            if numberOfBolts == 6:
                self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]


            elif numberOfBolts == 8:
                self.pitch23 = boltPlaceObj['Bolt']['Pitch23']
                self.pitch34 = boltPlaceObj['Bolt']['Pitch34']

            elif numberOfBolts == 10:
                self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]
                # self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]
                self.pitch34 = boltPlaceObj["Bolt"]["Pitch34"]
                self.pitch45 = boltPlaceObj["Bolt"]["Pitch45"]

        else: #"Flush"
            # self.Lv = boltPlaceObj["Bolt"]["Lv"]
            if numberOfBolts == 4:
                self.pitch12 = boltPlaceObj["Bolt"]["Pitch"]

            elif numberOfBolts == 6:
                self.pitch12 = boltPlaceObj["Bolt"]["Pitch12"]
                self.pitch23 = boltPlaceObj["Bolt"]["Pitch23"]



    def calculatePositions(self, numberOfBolts):
        '''
        The bolt placement is carried out in such a way that bolt @1X1 is considered as Bolt origin and w.r.t this bolt origin,
        rest of the rows ob bolts are placed.
        :return: The position of bolts 
        '''
        self.positions = []

        if self.alist["Member"]["Connectivity"] == "Extended both ways":
            if numberOfBolts == 8:
                self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir   # self.origin here is vertex of endplate, translate by Edge distance in X
                self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir    # Translate by endDistance in Z direction
                for rw in range(1, self.row + 1):
                    if rw == 1:
                        for col in range(self.col):
                            pos = self.boltOrigin
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 2:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space12 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"]
                            pos = pos + self.boltOrigin + space12 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 3:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space23 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23
                            pos = pos + self.boltOrigin + space23 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 4:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space23 = 4 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + 2 * self.beamDim["T"] + self.pitch23
                            pos = pos + self.boltOrigin + space23 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)

            elif numberOfBolts == 12:
                    self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir   # self.origin here is vertex of endplate, translate by Edge distance in X
                    self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir    # Translate by endDistance in Z direction
                    for rw in range(1, self.row + 1):
                        if rw == 1:
                            for col in range(self.col):
                                pos = self.boltOrigin
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 2:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space12 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"]
                                pos = pos + self.boltOrigin + space12 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 3:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space23 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23
                                pos = pos + self.boltOrigin + space23 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 4:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space34 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23 + self.pitch34
                                pos = pos + self.boltOrigin + space34 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 5:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space45 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23 + self.pitch34 \
                                          + self.pitch45
                                pos = pos + self.boltOrigin + space45 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 6:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space45 = 4 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + 2 * self.beamDim["T"] + self.pitch23 + \
                                                    self.pitch34 + self.pitch45
                                pos = pos + self.boltOrigin + space45 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)

            elif numberOfBolts == 16:
                    self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir   # self.origin here is vertex of endplate, translate by Edge distance in X
                    self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir    # Translate by endDistance in Z direction
                    for rw in range(1, self.row + 1):
                        if rw == 1:
                            for col in range(self.col):
                                pos = self.boltOrigin
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 2:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space12 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"]
                                pos = pos + self.boltOrigin + space12 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 3:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space32 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23
                                pos = pos + self.boltOrigin + space32 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 4:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space34 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23 + self.pitch34
                                pos = pos + self.boltOrigin + space34 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 5:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space45 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23 + self.pitch34 +\
                                          self.pitch45
                                pos = pos + self.boltOrigin + space45 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 6:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space56 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23 + self.pitch34 +\
                                          self.pitch45 + self.pitch56
                                pos = pos + self.boltOrigin + space56 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 7:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space67 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch23 + self.pitch34 +\
                                          self.pitch45 + self.pitch56 + self.pitch67
                                pos = pos + self.boltOrigin + space67 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 8:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space78 = 4 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + 2 * self.beamDim["T"] + self.pitch23 + \
                                          self.pitch34 + self.pitch45 + self.pitch56 + self.pitch67
                                pos = pos + self.boltOrigin + space78 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)

            elif numberOfBolts == 20:
                    self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir   # self.origin here is vertex of endplate, translate by Edge distance in X
                    self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir    # Translate by endDistance in Z direction
                    for rw in range(1, self.row + 1):
                        if rw == 1:
                            for col in range(self.col):
                                pos = self.boltOrigin
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 2:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space12 = self.pitch12
                                pos = pos + self.boltOrigin + space12 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 3:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space23 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch12
                                pos = pos + self.boltOrigin + space23 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 4:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space34 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch12 + self.pitch34
                                pos = pos + self.boltOrigin + space34 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 5:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space45 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch12 + self.pitch34 +\
                                          self.pitch45
                                pos = pos + self.boltOrigin + space45 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 6:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space56 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch12 + self.pitch34 +\
                                          self.pitch45 + self.pitch56
                                pos = pos + self.boltOrigin + space56 * self.pitchDir  #
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 7:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space67 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch12 + self.pitch34 +\
                                          self.pitch45 + self.pitch56 + self.pitch67
                                pos = pos + self.boltOrigin + space67 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 8:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space78 = 2 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + self.beamDim["T"] + self.pitch12 + self.pitch34 +\
                                          self.pitch45 + self.pitch56 + self.pitch67 + self.pitch78
                                pos = pos + self.boltOrigin + space78 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 9:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space89 = 4 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + 2 * self.beamDim["T"] + self.pitch12 + \
                                          self.pitch34 + self.pitch45 + self.pitch56 + self.pitch67 + self.pitch78
                                pos = pos + self.boltOrigin + space89 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)
                        if rw == 10:
                            for col in range(self.col):
                                pos = np.array([0.0, 0.0, 0.0])
                                space910 = 4 * (self.Lv + float(self.uiObjW["Weld"]["Flange (mm)"])) + 2 * self.beamDim["T"] + self.pitch12 + \
                                           self.pitch34 + self.pitch45 + self.pitch56 + self.pitch67 + self.pitch78 + self.pitch910
                                pos = pos + self.boltOrigin + space910 * self.pitchDir
                                pos = pos + col * self.crossCgauge * self.gaugeDir
                                self.positions.append(pos)

        elif self.alist["Member"]["Connectivity"] == "Extended one way":
            if numberOfBolts == 6:
                self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir   # self.origin here is vertex of endplate, translate by Edge distance in X
                self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir    # Translate by endDistance in Z direction
                for rw in range(1, self.row + 1):
                    if rw == 1:
                        for col in range(self.col):
                            pos = self.boltOrigin
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 2:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space12 =  2 * (self.Lv) + self.beamDim["T"]     #space is the distance between 1st row and 2nd row
                            pos = pos + self.boltOrigin + space12 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 3:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space23 =  2 * (self.Lv) + self.beamDim["T"] + self.pitch23  #Distance between 1st row and 3rd row #TODO make better variable for space13
                            pos = pos + self.boltOrigin + space23 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)

            elif numberOfBolts == 8:
                self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir  # self.origin here is vertex of endplate, translate by Edge distance in X
                self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir  # Translate by endDistance in Z direction
                for rw in range(1, self.row + 1):
                    if rw == 1:
                        for col in range(self.col):
                            pos = self.boltOrigin
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 2:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space12 =  2 * (self.Lv)  + self.beamDim["T"]
                            pos = pos + self.boltOrigin + space12 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 3:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space23 = 2 * (self.Lv ) + self.beamDim[
                                "T"] + self.pitch23
                            pos = pos + self.boltOrigin + space23 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 4:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space34 = 2 *  (self.Lv) + self.beamDim[
                                "T"] + self.pitch23 + self.pitch34                                      #TODO may be different for Ajmal code (may not need to add pitch45)
                            pos = pos + self.boltOrigin + space34 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)

            elif numberOfBolts == 10:
                self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir  # self.origin here is vertex of endplate, translate by Edge distance in X
                self.boltOrigin = self.boltOrigin + self.endDist * self.pitchDir  # Translate by endDistance in Z direction
                for rw in range(1, self.row + 1):
                    if rw == 1:
                        for col in range(self.col):
                            pos = self.boltOrigin
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 2:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space12 = self.pitch12
                            pos = pos + self.boltOrigin + space12 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 3:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space23 = 2 *  (self.Lv ) + self.beamDim[
                                "T"] + self.pitch12
                            pos = pos + self.boltOrigin + space23 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 4:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space34 = 2 *  (self.Lv ) + self.beamDim[
                                "T"] + self.pitch12 + self.pitch34
                            pos = pos + self.boltOrigin + space34 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 5:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space45 = 2 *  (self.Lv ) + self.beamDim[
                                "T"] + self.pitch12 + self.pitch34 +  self.pitch45
                            pos = pos + self.boltOrigin + space45 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)

        else: #"Flush"
            if numberOfBolts == 4:
                self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir  # self.origin here is vertex of endplate, translate by Edge distance in X
                self.boltOrigin = self.boltOrigin  # + self.endDist * self.pitchDir    # Translate by endDistance in Z direction
                for rw in range(1, self.row + 1):

                    # TODO remove this lines

                    if rw == 1:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space12 =  (self.Lv)+ self.beamDim["T"] + self.boltProjection  ##+ 2*float(self.uiObjW["Weld"]["Flange (mm)"]) # TODO  check if this formula is right, changed this formula
                            pos = pos + self.boltOrigin + space12 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 2:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space23 = (self.Lv) + self.beamDim["T"] + self.pitch12 + self.boltProjection
                            pos = pos + self.boltOrigin + space23 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)

            elif numberOfBolts == 6:
                self.boltOrigin = self.origin + self.edgeDist * self.gaugeDir  # self.origin here is vertex of endplate, translate by Edge distance in X
                self.boltOrigin = self.boltOrigin  # + self.endDist * self.pitchDir    # Translate by endDistance in Z direction
                for rw in range(1, self.row + 1):


                    # TODO have to modefy this formulas according to appropriate rows
                    if rw == 1:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space12 = (self.Lv) + self.beamDim["T"] + self.boltProjection       #+ 2*float(self.uiObjW['Weld']['Flange (mm)'])
                            pos = pos + self.boltOrigin + space12 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 2:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space23 = (self.Lv) + self.beamDim["T"] + self.pitch12 + self.boltProjection
                            pos = pos + self.boltOrigin + space23 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
                            self.positions.append(pos)
                    if rw == 3:
                        for col in range(self.col):
                            pos = np.array([0.0, 0.0, 0.0])
                            space34 = (self.Lv) + self.beamDim["T"] + self.pitch12 + self.pitch23 + self.boltProjection # + self.pitch34
                            pos = pos + self.boltOrigin + space34 * self.pitchDir
                            pos = pos + col * self.crossCgauge * self.gaugeDir
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
            self.nuts[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)  # gap here is between bolt head and nut

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