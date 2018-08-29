"""
created on 06-03-2018

@author: Siddhesh Chavan

This file is for creating CAD model for cover plate bolted moment connection for connectivity Beam-Beam

"""""

import numpy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut


class BBCoverPlateBoltedCAD(object):
    def __init__(self, beamLeft, beamRight, plateAbvFlange, plateBelwFlange, innerplateAbvFlangeFront,innerplateAbvFlangeBack,
                 innerplateBelwFlangeFront, innerplateBelwFlangeBack, WebPlateLeft, WebPlateRight, nut_bolt_array_AF,
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
        self.flange_splice_preference = alist['FlangePlate']['Preferences']
        self.plateAbvFlange = plateAbvFlange
        self.plateBelwFlange = plateBelwFlange

        self.innerplateAbvFlangeFront = innerplateAbvFlangeFront
        self.innerplateAbvFlangeBack = innerplateAbvFlangeBack
        self.innerplateBelwFlangeFront = innerplateBelwFlangeFront
        self.innerplateBelwFlangeBack = innerplateBelwFlangeBack

        self.WebPlateLeft = WebPlateLeft
        self.WebPlateRight = WebPlateRight
        self.nut_bolt_array_AF = nut_bolt_array_AF
        self.nut_bolt_array_BF = nut_bolt_array_BF
        self.nut_bolt_array_Web = nut_bolt_array_Web
        self.beamLModel = None
        self.beamRModel = None
        self.WebPlateLeftModel = None
        self.WebPlateRightModel = None
        self.plateAbvFlangeModel = None
        self.plateBelwFlangeModel = None
        self.innerplateAbvFlangeFrontModel = None
        self.innerplateAbvFlangeBackModel = None
        self.innerplateBelwFlangeFrontModel = None
        self.innerplateBelwFlangeBackModel = None

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

        if self.flange_splice_preference != 'Outside':
            self.createInnerPlateAbvFlangeGeometryFront()
            self.createInnerPlateAbvFlangeGeometryBack()
            self.createInnerPlateBelwFlangeGeometryFront()
            self.createInnerPlateBelwFlangeGeometryBack()
            self.innerplateAbvFlangeFrontModel = self.innerplateAbvFlangeFront.create_model()
            self.innerplateAbvFlangeBackModel = self.innerplateAbvFlangeBack.create_model()
            self.innerplateBelwFlangeFrontModel = self.innerplateBelwFlangeFront.create_model()
            self.innerplateBelwFlangeBackModel = self.innerplateBelwFlangeBack.create_model()

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

    def createInnerPlateAbvFlangeGeometryFront(self):
        shiftY = self.beamLeft.length + self.gap /2 - self.innerplateAbvFlangeFront.W / 2
        shiftZ = (self.beamLeft.D - 2 * self.beamLeft.t)/2 - self.innerplateAbvFlangeFront.T
        shiftX = (self.beamLeft.B - (self.innerplateAbvFlangeFront.L + self.beamLeft.R1))/2
        innerplateAbvFlangeOrigin = numpy.array([shiftX, shiftY, shiftZ])
        innerplateAF_uDir = numpy.array([0.0, 0.0, 1.0])
        innerplateAF_wDir = numpy.array([0.0, 1.0, 0.0])
        self.innerplateAbvFlangeFront.place(innerplateAbvFlangeOrigin, innerplateAF_uDir, innerplateAF_wDir)

    def createInnerPlateAbvFlangeGeometryBack(self):
        shiftY1 = self.beamLeft.length + self.gap /2 - self.innerplateAbvFlangeFront.W / 2
        shiftZ1 = (self.beamLeft.D - 2 * self.beamLeft.t)/2 - self.innerplateAbvFlangeFront.T
        shiftX1 = (self.beamLeft.B - (self.innerplateAbvFlangeFront.L + self.beamLeft.R1))/2
        innerplateAbvFlangeOrigin1 = numpy.array([-shiftX1, shiftY1, shiftZ1])
        innerplateAF_uDir1 = numpy.array([0.0, 0.0, 1.0])
        innerplateAF_wDir1 = numpy.array([0.0, 1.0, 0.0])
        self.innerplateAbvFlangeBack.place(innerplateAbvFlangeOrigin1, innerplateAF_uDir1, innerplateAF_wDir1)

    def createInnerPlateBelwFlangeGeometryFront(self):
        shiftY = self.beamLeft.length + self.gap /2 - self.innerplateAbvFlangeFront.W / 2
        shiftZ = (self.beamLeft.D - 2 * self.beamLeft.t)/2 - self.innerplateAbvFlangeFront.T
        shiftX = (self.beamLeft.B - (self.innerplateAbvFlangeFront.L + self.beamLeft.R1))/2
        innerplateAbvFlangeOrigin = numpy.array([shiftX, shiftY, -shiftZ])
        innerplateAF_uDir = numpy.array([0.0, 0.0, 1.0])
        innerplateAF_wDir = numpy.array([0.0, 1.0, 0.0])
        self.innerplateBelwFlangeFront.place(innerplateAbvFlangeOrigin, innerplateAF_uDir, innerplateAF_wDir)

    def createInnerPlateBelwFlangeGeometryBack(self):
        shiftY1 = self.beamLeft.length + self.gap /2 - self.innerplateAbvFlangeFront.W / 2
        shiftZ1 = (self.beamLeft.D - 2 * self.beamLeft.t)/2 - self.innerplateAbvFlangeFront.T
        shiftX1 = (self.beamLeft.B - (self.innerplateAbvFlangeFront.L + self.beamLeft.R1))/2
        innerplateAbvFlangeOrigin1 = numpy.array([-shiftX1, shiftY1, -shiftZ1])
        innerplateAF_uDir1 = numpy.array([0.0, 0.0, 1.0])
        innerplateAF_wDir1 = numpy.array([0.0, 1.0, 0.0])
        self.innerplateBelwFlangeBack.place(innerplateAbvFlangeOrigin1, innerplateAF_uDir1, innerplateAF_wDir1)

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
        if self.flange_splice_preference != 'Outside':
            nutBoltOriginAF = self.plateAbvFlange.sec_origin + numpy.array(
                [-self.beamLeft.B / 2, 0.0, (self.plateAbvFlange.T - self.beamLeft.t)/2])
        else:
            nutBoltOriginAF = self.plateAbvFlange.sec_origin + numpy.array([-self.beamLeft.B / 2, 0.0, self.plateAbvFlange.T / 2])
        gaugeDirAF = numpy.array([1.0, 0, 0])
        pitchDirAF = numpy.array([0, 1.0, 0])
        boltDirAF = numpy.array([0, 0, -1.0])
        width = self.beamLeft.B
        self.nut_bolt_array_AF.placeAF(nutBoltOriginAF, gaugeDirAF, pitchDirAF, boltDirAF, width)

    def create_nut_bolt_array_BF(self):
        if self.flange_splice_preference != 'Outside':
            nutBoltOriginBF = self.plateBelwFlange.sec_origin + numpy.array(
                [-self.beamLeft.B / 2, 0.0, -(self.plateAbvFlange.T - self.beamLeft.t)/2])
        else:
            nutBoltOriginBF = self.plateBelwFlange.sec_origin + numpy.array(
                [-self.beamLeft.B / 2, 0.0, -self.plateAbvFlange.T / 2])
        gaugeDirBF = numpy.array([1.0, 0, 0])
        pitchDirBF = numpy.array([0, 1.0, 0])
        boltDirBF = numpy.array([0, 0, 1.0])
        width = self.beamLeft.B
        self.nut_bolt_array_BF.placeBF(nutBoltOriginBF, gaugeDirBF, pitchDirBF, boltDirBF, width)

    def create_nut_bolt_array_Web(self):
        boltWeb_X = self.WebPlateRight.T / 2
        boltWeb_Z = self.WebPlateRight.L / 2
        nutBoltOriginW = self.WebPlateRight.sec_origin + numpy.array([boltWeb_X, 0.0, boltWeb_Z])
        gaugeDirW = numpy.array([0, 1.0, 0])
        pitchDirW = numpy.array([0, 0, -1.0])
        boltDirW = numpy.array([-1.0, 0, 0])
        self.nut_bolt_array_Web.placeW(nutBoltOriginW, gaugeDirW, pitchDirW, boltDirW)


    def get_nutboltmodelsAF(self):
        return self.nut_bolt_array_AF.get_modelsAF()

    def get_nutboltmodelsBF(self):
        return self.nut_bolt_array_BF.get_modelsBF()

    def get_nutboltmodelsWeb(self):
        return self.nut_bolt_array_Web.get_modelsW()

    # Below methods are for creating holes in flange and web
    def get_beam_models(self):
        '''

        Returns: Returns model of beam (left and right)

        '''
        return [self.beamLModel, self.beamRModel]

    def get_connector_models(self):
        '''

        Returns: Returns model related to connector (plates and bolts)

        '''

        if self.flange_splice_preference != 'Outside':
            return [self.WebPlateLeftModel, self.WebPlateRightModel, self.innerplateAbvFlangeBackModel,
                self.innerplateAbvFlangeFrontModel, self.innerplateBelwFlangeBackModel,
                self.innerplateBelwFlangeFrontModel, self.plateAbvFlangeModel,
                    self.plateBelwFlangeModel] + self.nut_bolt_array_AF.get_modelsAF() + self.nut_bolt_array_BF.get_modelsBF() + self.nut_bolt_array_Web.get_modelsW()
        else:
            return [self.WebPlateLeftModel, self.WebPlateRightModel, self.plateAbvFlangeModel,
                    self.plateBelwFlangeModel] + self.nut_bolt_array_AF.get_modelsAF() + self.nut_bolt_array_BF.get_modelsBF() + self.nut_bolt_array_Web.get_modelsW()

    def get_models(self):
        '''

        Returns: Returns model related to complete model (beams, plates and bolts)

        '''

        if self.flange_splice_preference != 'Outside':
            return [self.beamLModel, self.beamRModel, self.WebPlateLeftModel, self.WebPlateRightModel,
                    self.innerplateAbvFlangeBackModel, self.innerplateAbvFlangeFrontModel,
                    self.innerplateBelwFlangeBackModel, self.innerplateBelwFlangeFrontModel, self.plateAbvFlangeModel,
                    self.plateBelwFlangeModel] + self.nut_bolt_array_AF.get_modelsAF() + self.nut_bolt_array_BF.get_modelsBF() + self.nut_bolt_array_Web.get_modelsW()
        else:
            return [self.beamLModel, self.beamRModel, self.WebPlateLeftModel, self.WebPlateRightModel,
                    self.plateAbvFlangeModel, self.plateBelwFlangeModel] + self.nut_bolt_array_AF.get_modelsAF() + self.nut_bolt_array_BF.get_modelsBF() + self.nut_bolt_array_Web.get_modelsW()


    def get_beamLModel(self):
        '''

        Returns: Wholes in left beam

        '''
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
        '''

        Returns: Wholes in right beam

        '''
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

    def get_WebPlateLeftModel(self):
        '''

        Returns: Wholes in left webplate

        '''
        final_plateLP = self.WebPlateLeftModel
        bolt_listLP = self.nut_bolt_array_Web.get_bolt_web_list()
        for boltLP in bolt_listLP[:]:
            final_plateLP = BRepAlgoAPI_Cut(final_plateLP, boltLP).Shape()
        return final_plateLP

    def get_WebPlateRightModel(self):
        '''

        Returns: Wholes in right webplate

        '''
        final_plateRP = self.WebPlateRightModel
        bolt_listRP = self.nut_bolt_array_Web.get_bolt_web_list()
        for boltRP in bolt_listRP[:]:
            final_plateRP = BRepAlgoAPI_Cut(final_plateRP, boltRP).Shape()
        return final_plateRP

    def get_plateAbvFlangeModel(self):
        '''

        Returns: Wholes in above plate of flange

        '''
        final_plateAP = self.plateAbvFlangeModel
        bolt_listAP = self.nut_bolt_array_AF.get_bolt_listLA()
        for boltAP in bolt_listAP[:]:
            final_plateAP = BRepAlgoAPI_Cut(final_plateAP, boltAP).Shape()
        return final_plateAP

    def get_plateBelwFlangeModel(self):
        '''

        Returns: Wholes in below plate of flange

        '''
        final_plateBP = self.plateBelwFlangeModel
        bolt_listBP = self.nut_bolt_array_BF.get_bolt_listRB()
        for boltBP in bolt_listBP[:]:
            final_plateBP = BRepAlgoAPI_Cut(final_plateBP, boltBP).Shape()
        return final_plateBP

    def get_innerplateAbvFlangeFront(self):
        '''

        Returns: Wholes in inner front plate of above flange

        '''
        final = self.innerplateAbvFlangeFrontModel
        boltt = self.nut_bolt_array_AF.get_bolt_listLA()
        for a in boltt[:]:
            final = BRepAlgoAPI_Cut(final, a).Shape()
        return final

    def get_innerplateAbvFlangeBack(self):
        '''

        Returns: Wholes in inner back plate of above flange

        '''
        final = self.innerplateAbvFlangeBackModel
        bolt = self.nut_bolt_array_AF.get_bolt_listLA()
        for a in bolt[:]:
            final = BRepAlgoAPI_Cut(final, a).Shape()
        return final

    def get_innerplateBelwFlangeFront(self):
        '''

        Returns: Wholes in inner front plate of below flange

        '''
        final = self.innerplateBelwFlangeFrontModel
        boltt = self.nut_bolt_array_BF.get_bolt_listRB()
        for a in boltt[:]:
            final = BRepAlgoAPI_Cut(final, a).Shape()
        return final

    def get_innerplateBelwFlangeBack(self):
        '''

        Returns: Wholes in inner back plate of below flange

        '''
        final = self.innerplateBelwFlangeBackModel
        bolt = self.nut_bolt_array_BF.get_bolt_listRB()
        for a in bolt[:]:
            final = BRepAlgoAPI_Cut(final, a).Shape()
        return final