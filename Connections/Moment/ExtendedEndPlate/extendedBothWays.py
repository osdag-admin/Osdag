"""
Initialized on 22-01-2018
Commenced on 16-02-2018
@author: Siddhesh S. Chavan
"""""

import numpy


class ExtendedBothWays(object):

    def __init__(self, beamLeft, beamRight, plateLeft, plateRight, nut_bolt_array,
                 bbWeldAbvFlang_11, bbWeldAbvFlang_12, bbWeldAbvFlang_21, bbWeldAbvFlang_22,
                 bbWeldBelwFlang_11, bbWeldBelwFlang_12, bbWeldBelwFlang_13, bbWeldBelwFlang_14,
                 bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23, bbWeldBelwFlang_24,
                 bbWeldSideWeb_11, bbWeldSideWeb_12, bbWeldSideWeb_21, bbWeldSideWeb_22):

        # Initializing the arguments
        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.plateLeft = plateLeft
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.beamLModel = None
        self.beamRModel = None
        self.plateLModel = None
        self.plateRModel = None
        self.bbWeldAbvFlang_11Model = None
        self.bbWeldAbvFlang_12Model = None
        self.bbWeldAbvFlang_21Model = None
        self.bbWeldAbvFlang_22Model = None

        self.bbWeldBelwFlang_11Model = None
        self.bbWeldBelwFlang_12Model = None
        self.bbWeldBelwFlang_13Model = None
        self.bbWeldBelwFlang_14Model = None
        self.bbWeldBelwFlang_21Model = None
        self.bbWeldBelwFlang_22Model = None
        self.bbWeldBelwFlang_23Model = None
        self.bbWeldBelwFlang_24Model = None


        self.bbWeldSideWeb_11Model = None
        self.bbWeldSideWeb_12Model = None
        self.bbWeldSideWeb_21Model = None
        self.bbWeldSideWeb_22Model = None



        # Weld above flange for left and right beam
        self.bbWeldAbvFlang_11 = bbWeldAbvFlang_11      # Left beam upper side
        self.bbWeldAbvFlang_12 = bbWeldAbvFlang_12      # Left beam lower side
        self.bbWeldAbvFlang_21 = bbWeldAbvFlang_21      # Right beam upper side
        self.bbWeldAbvFlang_22 = bbWeldAbvFlang_22      # Right beam lower side

        self.bbWeldBelwFlang_11 = bbWeldBelwFlang_11    # Left beam, upper, left
        self.bbWeldBelwFlang_12 = bbWeldBelwFlang_12    # Left beam, upper, right
        self.bbWeldBelwFlang_13 = bbWeldBelwFlang_13    # Left beam, lower, left
        self.bbWeldBelwFlang_14 = bbWeldBelwFlang_14    # Left beam, lower, right
        self.bbWeldBelwFlang_21 = bbWeldBelwFlang_21    # behind bbWeldBelwFlang_11
        self.bbWeldBelwFlang_22 = bbWeldBelwFlang_22    # behind bbWeldBelwFlang_12
        self.bbWeldBelwFlang_23 = bbWeldBelwFlang_23    # behind bbWeldBelwFlang_13
        self.bbWeldBelwFlang_24 = bbWeldBelwFlang_24    # behind bbWeldBelwFlang_14


        self.bbWeldSideWeb_11 = bbWeldSideWeb_11        # Left beam, left of Web
        self.bbWeldSideWeb_12 = bbWeldSideWeb_12        # Left beam, right of Web
        self.bbWeldSideWeb_21 = bbWeldSideWeb_21        # Behind bbWeldSideWeb_11
        self.bbWeldSideWeb_22 = bbWeldSideWeb_22        # Behind bbWeldSideWeb_12


    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on 
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateLGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()

        self.create_bbWeldAbvFlang_11()
        self.create_bbWeldAbvFlang_12()
        self.create_bbWeldAbvFlang_21()
        self.create_bbWeldAbvFlang_22()

        self.create_bbWeldBelwFlang_11()
        self.create_bbWeldBelwFlang_12()
        self.create_bbWeldBelwFlang_13()
        self.create_bbWeldBelwFlang_14()
        self.create_bbWeldBelwFlang_21()
        self.create_bbWeldBelwFlang_22()
        self.create_bbWeldBelwFlang_23()
        self.create_bbWeldBelwFlang_24()


        self.create_bbWeldSideWeb_11()
        self.create_bbWeldSideWeb_12()
        self.create_bbWeldSideWeb_21()
        self.create_bbWeldSideWeb_22()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateLModel = self.plateLeft.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()

        self.bbWeldAbvFlang_11Model = self.bbWeldAbvFlang_11.create_model()
        self.bbWeldAbvFlang_12Model = self.bbWeldAbvFlang_12.create_model()
        self.bbWeldAbvFlang_21Model = self.bbWeldAbvFlang_21.create_model()
        self.bbWeldAbvFlang_22Model = self.bbWeldAbvFlang_22.create_model()

        self.bbWeldBelwFlang_11Model = self.bbWeldBelwFlang_11.create_model()
        self.bbWeldBelwFlang_12Model = self.bbWeldBelwFlang_12.create_model()
        self.bbWeldBelwFlang_13Model = self.bbWeldBelwFlang_13.create_model()
        self.bbWeldBelwFlang_14Model = self.bbWeldBelwFlang_14.create_model()
        self.bbWeldBelwFlang_21Model = self.bbWeldBelwFlang_21.create_model()
        self.bbWeldBelwFlang_22Model = self.bbWeldBelwFlang_22.create_model()
        self.bbWeldBelwFlang_23Model = self.bbWeldBelwFlang_23.create_model()
        self.bbWeldBelwFlang_24Model = self.bbWeldBelwFlang_24.create_model()


        self.bbWeldSideWeb_11Model = self.bbWeldSideWeb_11.create_model()
        self.bbWeldSideWeb_12Model = self.bbWeldSideWeb_12.create_model()
        self.bbWeldSideWeb_21Model = self.bbWeldSideWeb_21.create_model()
        self.bbWeldSideWeb_22Model = self.bbWeldSideWeb_22.create_model()


#############################################################################################################
#   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
#   same component at appropriate place                                                                     #
#############################################################################################################

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamRight.length + 2 * self.plateRight.T
        beamOriginR = numpy.array([0.0, gap, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateLGeometry(self):
        plateOriginL = numpy.array([-self.plateLeft.W/2, self.beamRight.length + 0.5 * self.plateLeft.T, 0.0])
        plateL_uDir = numpy.array([0.0, 1.0, 0.0])
        plateL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

    def createPlateRGeometry(self):
        gap = 1.5 * self.plateRight.T + self.beamLeft.length
        plateOriginR = numpy.array([-self.plateRight.W/2, gap, 0.0])
        plateR_uDir = numpy.array([0.0, 1.0, 0.0])
        plateR_wDir = numpy.array([1.0, 0.0, 0.0])
        self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        nutboltArrayOrigin = self.plateLeft.sec_origin + numpy.array([0.0, -0.5 * self.plateLeft.T, self.plateLeft.L/2])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, 0, -1.0])
        boltDir = numpy.array([0, 1.0, 0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def create_bbWeldAbvFlang_11(self):
        weldAbvFlangOrigin_11 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, self.beamLeft.D / 2])
        uDirAbv_11 = numpy.array([0, -1.0, 0])
        wDirAbv_11 = numpy.array([-1.0, 0, 0])
        self.bbWeldAbvFlang_11.place(weldAbvFlangOrigin_11, uDirAbv_11, wDirAbv_11)

    def create_bbWeldAbvFlang_12(self):
        weldAbvFlangOrigin_12 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length, -self.beamLeft.D / 2])
        uDirAbv_12 = numpy.array([0, -1.0, 0])
        wDirAbv_12 = numpy.array([1.0, 0, 0])
        self.bbWeldAbvFlang_12.place(weldAbvFlangOrigin_12, uDirAbv_12, wDirAbv_12)

    def create_bbWeldAbvFlang_21(self):
        weldAbvFlangOrigin_21 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2])
        uDirAbv_21 = numpy.array([0, 1.0, 0])
        wDirAbv_21 = numpy.array([1.0, 0, 0])
        self.bbWeldAbvFlang_21.place(weldAbvFlangOrigin_21, uDirAbv_21, wDirAbv_21)

    def create_bbWeldAbvFlang_22(self):
        weldAbvFlangOrigin_22 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2])
        uDirAbv_22 = numpy.array([0, 1.0, 0])
        wDirAbv_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldAbvFlang_22.place(weldAbvFlangOrigin_22, uDirAbv_22, wDirAbv_22)

    def create_bbWeldBelwFlang_11(self):
        weldBelwFlangOrigin_11 = numpy.array([self.beamLeft.R2 -self.beamLeft.B / 2, self.beamLeft.length, (self.beamLeft.D / 2) - self.beamLeft.T])
        uDirBelw_11 = numpy.array([0, -1.0, 0])
        wDirBelw_11 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_11.place(weldBelwFlangOrigin_11, uDirBelw_11, wDirBelw_11)

    def create_bbWeldBelwFlang_12(self):
        weldBelwFlangOrigin_12 = numpy.array([self.beamLeft.R1 + self.beamLeft.t / 2, self.beamLeft.length, (self.beamLeft.D / 2) - self.beamLeft.T])
        uDirBelw_12 = numpy.array([0, -1.0, 0])
        wDirBelw_12 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_12.place(weldBelwFlangOrigin_12, uDirBelw_12, wDirBelw_12)

    def create_bbWeldBelwFlang_13(self):
        weldBelwFlangOrigin_13 = numpy.array([-self.beamLeft.R1-self.beamLeft.t / 2, self.beamLeft.length, -(self.beamLeft.D / 2) + self.beamLeft.T])
        uDirBelw_13 = numpy.array([0, -1.0, 0])
        wDirBelw_13 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_13.place(weldBelwFlangOrigin_13, uDirBelw_13, wDirBelw_13)

    def create_bbWeldBelwFlang_14(self):
        weldBelwFlangOrigin_14 = numpy.array([-self.beamLeft.R2+self.beamLeft.B / 2, self.beamLeft.length, -(self.beamLeft.D / 2) + self.beamLeft.T])
        uDirBelw_14 = numpy.array([0, -1.0, 0])
        wDirBelw_14 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_14.place(weldBelwFlangOrigin_14, uDirBelw_14, wDirBelw_14)

    def create_bbWeldBelwFlang_21(self):
        weldBelwFlangOrigin_21 = numpy.array([-self.beamLeft.R1-self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, (self.beamLeft.D / 2) -
                                              self.beamLeft.T])
        uDirBelw_21 = numpy.array([0, 1.0, 0])
        wDirBelw_21 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_21.place(weldBelwFlangOrigin_21, uDirBelw_21, wDirBelw_21)

    def create_bbWeldBelwFlang_22(self):
        weldBelwFlangOrigin_22 = numpy.array([-self.beamLeft.R2+self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, (self.beamLeft.D / 2) -
                                              self.beamLeft.T])
        uDirBelw_22 = numpy.array([0, 1.0, 0])
        wDirBelw_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_22.place(weldBelwFlangOrigin_22, uDirBelw_22, wDirBelw_22)

    def create_bbWeldBelwFlang_23(self):
        weldBelwFlangOrigin_23 = numpy.array([self.beamLeft.R2-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -(self.beamLeft.D / 2) +
                                              self.beamLeft.T])
        uDirBelw_23 = numpy.array([0, 1.0, 0])
        wDirBelw_23 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_23.place(weldBelwFlangOrigin_23, uDirBelw_23, wDirBelw_23)

    def create_bbWeldBelwFlang_24(self):
        weldBelwFlangOrigin_24 = numpy.array([self.beamLeft.R1+self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, -(self.beamLeft.D / 2) +
                                              self.beamLeft.T])
        uDirBelw_24 = numpy.array([0, 1.0, 0])
        wDirBelw_24 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_24.place(weldBelwFlangOrigin_24, uDirBelw_24, wDirBelw_24)

    def create_bbWeldSideWeb_11(self):
        weldSideWebOrigin_11 = numpy.array([-self.beamLeft.t/2, self.beamLeft.length, self.bbWeldSideWeb_21.L / 2])
        uDirWeb_11 = numpy.array([0, -1.0, 0])
        wDirWeb_11 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_11.place(weldSideWebOrigin_11, uDirWeb_11, wDirWeb_11)

    def create_bbWeldSideWeb_12(self):
        weldSideWebOrigin_12 = numpy.array([self.beamLeft.t / 2, self.beamLeft.length, -self.bbWeldSideWeb_21.L / 2])
        uDirWeb_12 = numpy.array([0, -1.0, 0])
        wDirWeb_12 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_12.place(weldSideWebOrigin_12, uDirWeb_12, wDirWeb_12)

    def create_bbWeldSideWeb_21(self):
        weldSideWebOrigin_21 = numpy.array([-self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.bbWeldSideWeb_21.L / 2])
        uDirWeb_21 = numpy.array([0, 1.0, 0])
        wDirWeb_21 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_21.place(weldSideWebOrigin_21, uDirWeb_21, wDirWeb_21)

    def create_bbWeldSideWeb_22(self):
        weldSideWebOrigin_22 = numpy.array([self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.bbWeldSideWeb_21.L / 2])
        uDirWeb_22 = numpy.array([0, 1.0, 0])
        wDirWeb_22 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_22.place(weldSideWebOrigin_22, uDirWeb_22, wDirWeb_22)

#############################################################################################################
#   Following functions returns the CAD model to the function display_3DModel of main file                  #
#############################################################################################################
    def get_beam_models(self):
        '''

        Returns: Returns model of beam (left and right)

        '''
        return [self.beamRModel, self.beamLModel]

    def get_connector_models(self):
        '''

        Returns: Returns model related to connector (plates and weld)

        '''
        return [self.plateRModel, self.plateLModel, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
                self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model,
                self.bbWeldBelwFlang_13Model, self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model, self.bbWeldBelwFlang_22Model,
                self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model, self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model,
                self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model] + self.nut_bolt_array.get_models()

    def get_models(self):
        '''

        Returns: Returns model related to complete model (beams, plates and weld)

        '''
        return [self.beamRModel, self.beamLModel, self.plateRModel, self.plateLModel, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
                self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model,
                self.bbWeldBelwFlang_13Model, self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model, self.bbWeldBelwFlang_22Model,
                self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model, self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model,
                self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model] + self.nut_bolt_array.get_models()


    def get_beamLModel(self):
        return self.beamLModel

    def get_beamRModel(self):
        return self.beamRModel

    def get_plateLModel(self):
        return self.plateLModel

    def get_plateRModel(self):
        return self.plateRModel

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()

    def get_bbWeldAbvFlang_11Model(self):
        return self.bbWeldAbvFlang_11Model

    def get_bbWeldAbvFlang_12Model(self):
        return self.bbWeldAbvFlang_12Model

    def get_bbWeldAbvFlang_21Model(self):
        return self.bbWeldAbvFlang_21Model

    def get_bbWeldAbvFlang_22Model(self):
        return self.bbWeldAbvFlang_22Model

    def get_bbWeldBelwFlang_11Model(self):
        return self.bbWeldBelwFlang_11Model

    def get_bbWeldBelwFlang_12Model(self):
        return self.bbWeldBelwFlang_12Model

    def get_bbWeldBelwFlang_13Model(self):
        return self.bbWeldBelwFlang_13Model

    def get_bbWeldBelwFlang_14Model(self):
        return self.bbWeldBelwFlang_14Model

    def get_bbWeldBelwFlang_21Model(self):
        return self.bbWeldBelwFlang_21Model

    def get_bbWeldBelwFlang_22Model(self):
        return self.bbWeldBelwFlang_22Model

    def get_bbWeldBelwFlang_23Model(self):
        return self.bbWeldBelwFlang_23Model

    def get_bbWeldBelwFlang_24Model(self):
        return self.bbWeldBelwFlang_24Model

    def get_bbWeldSideWeb_11Model(self):
        return self.bbWeldSideWeb_11Model

    def get_bbWeldSideWeb_12Model(self):
        return self.bbWeldSideWeb_12Model

    def get_bbWeldSideWeb_21Model(self):
        return self.bbWeldSideWeb_21Model

    def get_bbWeldSideWeb_22Model(self):
        return self.bbWeldSideWeb_22Model

