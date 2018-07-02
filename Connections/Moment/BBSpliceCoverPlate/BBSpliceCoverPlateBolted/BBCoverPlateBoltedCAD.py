"""
created on 06-03-2018

@author: Siddhesh Chavan

This file is for creating CAD model for cover plate bolted moment connection for connectivity Beam-Beam

"""""

import numpy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut


class BBCoverPlateBoltedCAD(object):
    def __init__(self, beamLeft, beamRight, plateAbvFlange, plateBelwFlange, WebPlateLeft, WebPlateRight, nut_bolt_array_AF,
                 nut_bolt_array_BF, nut_bolt_array_Web, alist):

        """
        :param beamLeft: Left beam 
        :param beamRight: Right beam
        :param plateAbvFlange: Flange plate present above the flange
        :param plateBelwFlange: Flange plate present below the flange 
        :param WebPlateLeft: Web plate present left of flange
        :param WebPlateRight: Web plate present right of flange
        :param nut_bolt_array_AF: Bolt placement of flange plate present above flange
        :param nut_bolt_array_BF: Bolt placement of flange plate present below flange
        :param nut_bolt_array_Web: Bolt placement of web plate
        """
        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.alist = alist
        self.gap = alist["detailing"]["gap"]
        self.plateAbvFlange = plateAbvFlange
        self.plateBelwFlange = plateBelwFlange
        self.WebPlateLeft = WebPlateLeft
        self.WebPlateRight = WebPlateRight
        self.nut_bolt_array_AF = nut_bolt_array_AF
        self.nut_bolt_array_BF = nut_bolt_array_BF
        self.nut_bolt_array_Web = nut_bolt_array_Web
        self.beamLModel = None
        self.beamRModel = None
        self.WebPlateLeftModel = None

    def create_3DModel(self):
        '''
        :return:  CAD model of each of the followings. Debugging each command below would give give clear picture
        '''
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateAbvFlangeGeometry()
        self.createPlateBelwFlangeGeometry()
        self.createWebPlateLeftGeometry()
        self.createWebPlateRightGeometry()
        self.create_nut_bolt_array_AF()
        self.create_nut_bolt_array_BF()
        self.create_nut_bolt_array_Web()

        self.beamLModel = self.beamLeft.create_model()  # Call to ISection.py in Component directory
        self.beamRModel = self.beamRight.create_model()
        self.plateAbvFlangeModel = self.plateAbvFlange.create_model()   # Call to plate.py in Component directory
        self.plateBelwFlangeModel = self.plateBelwFlange.create_model()
        self.WebPlateLeftModel = self.WebPlateLeft.create_model()
        self.WebPlateRightModel = self.WebPlateRight.create_model()
        self.nutBoltArrayModels_AF = self.nut_bolt_array_AF.create_modelAF()    # call to nutBoltPlacement_AF.py
        self.nutBoltArrayModels_BF = self.nut_bolt_array_BF.create_modelBF()    # call to nutBoltPlacement_BF.py
        self.nutBoltArrayModels_Web = self.nut_bolt_array_Web.create_modelW()   # call to nutBoltPlacement_Web.py

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamRight.length + self.gap
        beamOriginR = numpy.array([0.0, gap, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateAbvFlangeGeometry(self):
        AbvFlange_shiftY = self.beamLeft.length + self.gap / 2 - self.plateAbvFlange.W / 2
        AbvFlange_shiftZ = (self.beamLeft.D + self.plateAbvFlange.T) / 2
        plateAbvFlangeOrigin = numpy.array([0.0, AbvFlange_shiftY, AbvFlange_shiftZ])
        plateAF_uDir = numpy.array([0.0, 0.0, 1.0])
        plateAF_wDir = numpy.array([0.0, 1.0, 0.0])
        self.plateAbvFlange.place(plateAbvFlangeOrigin, plateAF_uDir, plateAF_wDir)

    def createPlateBelwFlangeGeometry(self):
        BelwFlange_shiftY = self.beamLeft.length + self.gap / 2 - self.plateAbvFlange.W / 2
        BelwFlange_shiftZ = -(self.beamLeft.D + self.plateAbvFlange.T) / 2
        plateBelwFlangeOrigin = numpy.array([0.0, BelwFlange_shiftY, BelwFlange_shiftZ])
        plateBF_uDir = numpy.array([0.0, 0.0, 1.0])
        plateBF_wDir = numpy.array([0.0, 1.0, 0.0])
        self.plateBelwFlange.place(plateBelwFlangeOrigin, plateBF_uDir, plateBF_wDir)

    def createWebPlateLeftGeometry(self):
        WPL_shiftX = -(self.beamLeft.t + self.WebPlateLeft.T) / 2
        WPL_shiftY = self.beamLeft.length + self.gap / 2 - self.WebPlateLeft.W / 2
        WebPlateLeftOrigin = numpy.array([WPL_shiftX, WPL_shiftY, 0.0])
        WPL_uDir = numpy.array([1.0, 0.0, 0.0])
        WPL_wDir = numpy.array([0.0, 1.0, 0.0])
        self.WebPlateLeft.place(WebPlateLeftOrigin, WPL_uDir, WPL_wDir)

    def createWebPlateRightGeometry(self):
        WPR_shiftX = (self.beamLeft.t + self.WebPlateLeft.T) / 2
        WPR_shiftY = self.beamLeft.length + self.gap / 2 - self.WebPlateLeft.W / 2
        WebPlateRightOrigin = numpy.array([WPR_shiftX, WPR_shiftY, 0.0])
        WPR_uDir = numpy.array([1.0, 0.0, 0.0])
        WPR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.WebPlateRight.place(WebPlateRightOrigin, WPR_uDir, WPR_wDir)

    def create_nut_bolt_array_AF(self):
        nutBoltOriginAF = self.plateAbvFlange.sec_origin + numpy.array([-self.beamLeft.B / 2, 0.0, self.plateAbvFlange.T / 2])
        gaugeDirAF = numpy.array([1.0, 0, 0])
        pitchDirAF = numpy.array([0, 1.0, 0])
        boltDirAF = numpy.array([0, 0, -1.0])
        self.nut_bolt_array_AF.placeAF(nutBoltOriginAF, gaugeDirAF, pitchDirAF, boltDirAF)

    def create_nut_bolt_array_BF(self):
        nutBoltOriginBF = self.plateBelwFlange.sec_origin + numpy.array([-self.beamLeft.B / 2, 0.0, -self.plateAbvFlange.T / 2])
        gaugeDirBF = numpy.array([1.0, 0, 0])
        pitchDirBF = numpy.array([0, 1.0, 0])
        boltDirBF = numpy.array([0, 0, 1.0])
        self.nut_bolt_array_BF.placeBF(nutBoltOriginBF, gaugeDirBF, pitchDirBF, boltDirBF)

    def create_nut_bolt_array_Web(self):
        boltWeb_X = self.WebPlateRight.T / 2
        boltWeb_Z = self.WebPlateRight.L / 2
        nutBoltOriginW = self.WebPlateRight.sec_origin + numpy.array([boltWeb_X, 0.0, boltWeb_Z])
        gaugeDirW = numpy.array([0, 1.0, 0])
        pitchDirW = numpy.array([0, 0, -1.0])
        boltDirW = numpy.array([-1.0, 0, 0])
        self.nut_bolt_array_Web.placeW(nutBoltOriginW, gaugeDirW, pitchDirW, boltDirW)

    def get_plateAbvFlangeModel(self):
        return self.plateAbvFlangeModel

    def get_plateBelwFlangeModel(self):
        return self.plateBelwFlangeModel

    def get_WebPlateLeftModel(self):
        return self.WebPlateLeftModel

    def get_WebPlateRightModel(self):
        return self.WebPlateRightModel

    def get_nutboltmodelsAF(self):
        return self.nut_bolt_array_AF.get_modelsAF()

    def get_nutboltmodelsBF(self):
        return self.nut_bolt_array_BF.get_modelsBF()

    def get_nutboltmodelsWeb(self):
        return self.nut_bolt_array_Web.get_modelsWeb()

    # Below methods are for creating holes in flange and web
    def get_beamLModel(self):
        final_beam = self.beamLModel
        bolt_listLA = self.nut_bolt_array_AF.get_bolt_listLA()
        bolt_listLB = self.nut_bolt_array_BF.get_bolt_listLB()
        bolt_listWL = self.nut_bolt_array_Web.get_bolt_web_list()
        for boltLB in bolt_listLB[:]:
            final_beam = BRepAlgoAPI_Cut(final_beam, boltLB).Shape()
        for boltLA in bolt_listLA[:]:
            final_beam = BRepAlgoAPI_Cut(final_beam, boltLA).Shape()
        for boltWL in bolt_listWL[:]:
            final_beam = BRepAlgoAPI_Cut(final_beam, boltWL).Shape()
        return final_beam

    def get_beamRModel(self):
        final_beam = self.beamRModel
        bolt_listRA = self.nut_bolt_array_AF.get_bolt_listRA()
        bolt_listRB = self.nut_bolt_array_BF.get_bolt_listRB()
        bolt_listWR = self.nut_bolt_array_Web.get_bolt_web_list()
        for boltRB in bolt_listRB[:]:
            final_beam = BRepAlgoAPI_Cut(final_beam, boltRB).Shape()
        for boltRA in bolt_listRA[:]:
            final_beam = BRepAlgoAPI_Cut(final_beam, boltRA).Shape()
        for boltWR in bolt_listWR[:]:
            final_beam = BRepAlgoAPI_Cut(final_beam, boltWR).Shape()
        return final_beam

