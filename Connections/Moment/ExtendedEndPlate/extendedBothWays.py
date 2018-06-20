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
                 bbWeldSideFlange_11, bbWeldSideFlange_12, bbWeldSideFlange_13, bbWeldSideFlange_14,
                 bbWeldSideFlange_21, bbWeldSideFlange_22, bbWeldSideFlange_23, bbWeldSideFlange_24,
                 bbWeldSideWeb_11, bbWeldSideWeb_12, bbWeldSideWeb_21, bbWeldSideWeb_22,
                 bbWeldQtrCone_11, bbWeldQtrCone_12, bbWeldQtrCone_13, bbWeldQtrCone_14,
                 bbWeldQtrCone_15, bbWeldQtrCone_16, bbWeldQtrCone_17, bbWeldQtrCone_18,
                 bbWeldQtrCone_21, bbWeldQtrCone_22, bbWeldQtrCone_23, bbWeldQtrCone_24,
                 bbWeldQtrCone_25, bbWeldQtrCone_26, bbWeldQtrCone_27, bbWeldQtrCone_28):

        # Initializing the arguments
        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.plateLeft = plateLeft
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array

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

        self.bbWeldSideFlange_11 = bbWeldSideFlange_11  # Left beam, upper, left
        self.bbWeldSideFlange_12 = bbWeldSideFlange_12  # Left beam, upper, right
        self.bbWeldSideFlange_13 = bbWeldSideFlange_13  # Left beam, lower, left
        self.bbWeldSideFlange_14 = bbWeldSideFlange_14  # Left beam, lower, right
        self.bbWeldSideFlange_21 = bbWeldSideFlange_21  # behind bbWeldSideFlange_11
        self.bbWeldSideFlange_22 = bbWeldSideFlange_22  # behind bbWeldSideFlange_12
        self.bbWeldSideFlange_23 = bbWeldSideFlange_23  # behind bbWeldSideFlange_13
        self.bbWeldSideFlange_24 = bbWeldSideFlange_24  # behind bbWeldSideFlange_14

        self.bbWeldSideWeb_11 = bbWeldSideWeb_11        # Left beam, left of Web
        self.bbWeldSideWeb_12 = bbWeldSideWeb_12        # Left beam, right of Web
        self.bbWeldSideWeb_21 = bbWeldSideWeb_21        # Behind bbWeldSideWeb_11
        self.bbWeldSideWeb_22 = bbWeldSideWeb_22        # Behind bbWeldSideWeb_12

        self.bbWeldQtrCone_11 = bbWeldQtrCone_11        # Left beam, upper flange, left side, above flange
        self.bbWeldQtrCone_12 = bbWeldQtrCone_12        # Left beam, upper flange, left side, below flange
        self.bbWeldQtrCone_13 = bbWeldQtrCone_13        # Left beam, upper flange, right side, above flange
        self.bbWeldQtrCone_14 = bbWeldQtrCone_14        # Left beam, upper flange, right side, below flange
        self.bbWeldQtrCone_15 = bbWeldQtrCone_15        # Left beam, lower flange, left side, above flange
        self.bbWeldQtrCone_16 = bbWeldQtrCone_16        # Left beam, lower flange, left side, below flange
        self.bbWeldQtrCone_17 = bbWeldQtrCone_17        # Left beam, lower flange, right side, above flange
        self.bbWeldQtrCone_18 = bbWeldQtrCone_18        # Left beam, lower flange, right side, below flange

        self.bbWeldQtrCone_21 = bbWeldQtrCone_21        # behind bbWeldQtrCone_11
        self.bbWeldQtrCone_22 = bbWeldQtrCone_22        # behind bbWeldQtrCone_12
        self.bbWeldQtrCone_23 = bbWeldQtrCone_23        # behind bbWeldQtrCone_13
        self.bbWeldQtrCone_24 = bbWeldQtrCone_24        # behind bbWeldQtrCone_14
        self.bbWeldQtrCone_25 = bbWeldQtrCone_25        # behind bbWeldQtrCone_15
        self.bbWeldQtrCone_26 = bbWeldQtrCone_26        # behind bbWeldQtrCone_16
        self.bbWeldQtrCone_27 = bbWeldQtrCone_27        # behind bbWeldQtrCone_17
        self.bbWeldQtrCone_28 = bbWeldQtrCone_28        # behind bbWeldQtrCone_18

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

        self.create_bbWeldSideFlange_11()
        self.create_bbWeldSideFlange_12()
        self.create_bbWeldSideFlange_13()
        self.create_bbWeldSideFlange_14()
        self.create_bbWeldSideFlange_21()
        self.create_bbWeldSideFlange_22()
        self.create_bbWeldSideFlange_23()
        self.create_bbWeldSideFlange_24()

        self.create_bbWeldSideWeb_11()
        self.create_bbWeldSideWeb_12()
        self.create_bbWeldSideWeb_21()
        self.create_bbWeldSideWeb_22()

        self.create_bbWeldQtrCone_11()
        self.create_bbWeldQtrCone_12()
        self.create_bbWeldQtrCone_13()
        self.create_bbWeldQtrCone_14()
        self.create_bbWeldQtrCone_15()
        self.create_bbWeldQtrCone_16()
        self.create_bbWeldQtrCone_17()
        self.create_bbWeldQtrCone_18()

        self.create_bbWeldQtrCone_21()
        self.create_bbWeldQtrCone_22()
        self.create_bbWeldQtrCone_23()
        self.create_bbWeldQtrCone_24()
        self.create_bbWeldQtrCone_25()
        self.create_bbWeldQtrCone_26()
        self.create_bbWeldQtrCone_27()
        self.create_bbWeldQtrCone_28()

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

        self.bbWeldSideFlange_11Model = self.bbWeldSideFlange_11.create_model()
        self.bbWeldSideFlange_12Model = self.bbWeldSideFlange_12.create_model()
        self.bbWeldSideFlange_13Model = self.bbWeldSideFlange_13.create_model()
        self.bbWeldSideFlange_14Model = self.bbWeldSideFlange_14.create_model()
        self.bbWeldSideFlange_21Model = self.bbWeldSideFlange_21.create_model()
        self.bbWeldSideFlange_22Model = self.bbWeldSideFlange_22.create_model()
        self.bbWeldSideFlange_23Model = self.bbWeldSideFlange_23.create_model()
        self.bbWeldSideFlange_24Model = self.bbWeldSideFlange_24.create_model()

        self.bbWeldSideWeb_11Model = self.bbWeldSideWeb_11.create_model()
        self.bbWeldSideWeb_12Model = self.bbWeldSideWeb_12.create_model()
        self.bbWeldSideWeb_21Model = self.bbWeldSideWeb_21.create_model()
        self.bbWeldSideWeb_22Model = self.bbWeldSideWeb_22.create_model()

        self.bbWeldQtrCone_11Model = self.bbWeldQtrCone_11.create_model()
        self.bbWeldQtrCone_12Model = self.bbWeldQtrCone_12.create_model()
        self.bbWeldQtrCone_13Model = self.bbWeldQtrCone_13.create_model()
        self.bbWeldQtrCone_14Model = self.bbWeldQtrCone_14.create_model()
        self.bbWeldQtrCone_15Model = self.bbWeldQtrCone_15.create_model()
        self.bbWeldQtrCone_16Model = self.bbWeldQtrCone_16.create_model()
        self.bbWeldQtrCone_17Model = self.bbWeldQtrCone_17.create_model()
        self.bbWeldQtrCone_18Model = self.bbWeldQtrCone_18.create_model()

        self.bbWeldQtrCone_21Model = self.bbWeldQtrCone_21.create_model()
        self.bbWeldQtrCone_22Model = self.bbWeldQtrCone_22.create_model()
        self.bbWeldQtrCone_23Model = self.bbWeldQtrCone_23.create_model()
        self.bbWeldQtrCone_24Model = self.bbWeldQtrCone_24.create_model()
        self.bbWeldQtrCone_25Model = self.bbWeldQtrCone_25.create_model()
        self.bbWeldQtrCone_26Model = self.bbWeldQtrCone_26.create_model()
        self.bbWeldQtrCone_27Model = self.bbWeldQtrCone_27.create_model()
        self.bbWeldQtrCone_28Model = self.bbWeldQtrCone_28.create_model()

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
        weldBelwFlangOrigin_11 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length, (self.beamLeft.D / 2) - self.beamLeft.T])
        uDirBelw_11 = numpy.array([0, -1.0, 0])
        wDirBelw_11 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_11.place(weldBelwFlangOrigin_11, uDirBelw_11, wDirBelw_11)

    def create_bbWeldBelwFlang_12(self):
        weldBelwFlangOrigin_12 = numpy.array([self.beamLeft.t / 2, self.beamLeft.length, (self.beamLeft.D / 2) - self.beamLeft.T])
        uDirBelw_12 = numpy.array([0, -1.0, 0])
        wDirBelw_12 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_12.place(weldBelwFlangOrigin_12, uDirBelw_12, wDirBelw_12)

    def create_bbWeldBelwFlang_13(self):
        weldBelwFlangOrigin_13 = numpy.array([-self.beamLeft.t / 2, self.beamLeft.length, -(self.beamLeft.D / 2) + self.beamLeft.T])
        uDirBelw_13 = numpy.array([0, -1.0, 0])
        wDirBelw_13 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_13.place(weldBelwFlangOrigin_13, uDirBelw_13, wDirBelw_13)

    def create_bbWeldBelwFlang_14(self):
        weldBelwFlangOrigin_14 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, -(self.beamLeft.D / 2) + self.beamLeft.T])
        uDirBelw_14 = numpy.array([0, -1.0, 0])
        wDirBelw_14 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_14.place(weldBelwFlangOrigin_14, uDirBelw_14, wDirBelw_14)

    def create_bbWeldBelwFlang_21(self):
        weldBelwFlangOrigin_21 = numpy.array([-self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, (self.beamLeft.D / 2) -
                                              self.beamLeft.T])
        uDirBelw_21 = numpy.array([0, 1.0, 0])
        wDirBelw_21 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_21.place(weldBelwFlangOrigin_21, uDirBelw_21, wDirBelw_21)

    def create_bbWeldBelwFlang_22(self):
        weldBelwFlangOrigin_22 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, (self.beamLeft.D / 2) -
                                              self.beamLeft.T])
        uDirBelw_22 = numpy.array([0, 1.0, 0])
        wDirBelw_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_22.place(weldBelwFlangOrigin_22, uDirBelw_22, wDirBelw_22)

    def create_bbWeldBelwFlang_23(self):
        weldBelwFlangOrigin_23 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -(self.beamLeft.D / 2) +
                                              self.beamLeft.T])
        uDirBelw_23 = numpy.array([0, 1.0, 0])
        wDirBelw_23 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_23.place(weldBelwFlangOrigin_23, uDirBelw_23, wDirBelw_23)

    def create_bbWeldBelwFlang_24(self):
        weldBelwFlangOrigin_24 = numpy.array([self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, -(self.beamLeft.D / 2) +
                                              self.beamLeft.T])
        uDirBelw_24 = numpy.array([0, 1.0, 0])
        wDirBelw_24 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_24.place(weldBelwFlangOrigin_24, uDirBelw_24, wDirBelw_24)

    def create_bbWeldSideFlange_11(self):
        weldSideFlangOrigin_11 = numpy.array([-self.beamLeft.B/2, self.beamLeft.length, self.beamLeft.D/2])
        uDirSide_11 = numpy.array([0, -1.0, 0])
        wDirSide_11 = numpy.array([0, 0, -1.0])
        self.bbWeldSideFlange_11.place(weldSideFlangOrigin_11, uDirSide_11, wDirSide_11)

    def create_bbWeldSideFlange_12(self):
        weldSideFlangOrigin_12 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, self.beamLeft.D / 2 - self.beamLeft.T])
        uDirSide_12 = numpy.array([0, -1.0, 0])
        wDirSide_12 = numpy.array([0, 0, 1.0])
        self.bbWeldSideFlange_12.place(weldSideFlangOrigin_12, uDirSide_12, wDirSide_12)

    def create_bbWeldSideFlange_13(self):
        weldSideFlangOrigin_13 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length, -self.beamLeft.D / 2 + self.beamLeft.T])
        uDirSide_13 = numpy.array([0, -1.0, 0])
        wDirSide_13 = numpy.array([0, 0, -1.0])
        self.bbWeldSideFlange_13.place(weldSideFlangOrigin_13, uDirSide_13, wDirSide_13)

    def create_bbWeldSideFlange_14(self):
        weldSideFlangOrigin_14 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, -self.beamLeft.D / 2])
        uDirSide_14 = numpy.array([0, -1.0, 0])
        wDirSide_14 = numpy.array([0, 0, 1.0])
        self.bbWeldSideFlange_14.place(weldSideFlangOrigin_14, uDirSide_14, wDirSide_14)

    def create_bbWeldSideFlange_21(self):
        weldSideFlangOrigin_21 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2 -
                                              self.beamLeft.T])
        uDirSide_21 = numpy.array([0, 1.0, 0])
        wDirSide_21 = numpy.array([0, 0, 1.0])
        self.bbWeldSideFlange_21.place(weldSideFlangOrigin_21, uDirSide_21, wDirSide_21)

    def create_bbWeldSideFlange_22(self):
        weldSideFlangOrigin_22 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2])
        uDirSide_22 = numpy.array([0, 1.0, 0])
        wDirSide_22 = numpy.array([0, 0, -1.0])
        self.bbWeldSideFlange_22.place(weldSideFlangOrigin_22, uDirSide_22, wDirSide_22)

    def create_bbWeldSideFlange_23(self):
        weldSideFlangOrigin_23 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2 + self.beamLeft.T])
        uDirSide_23 = numpy.array([0, 1.0, 0])
        wDirSide_23 = numpy.array([0, 0, -1.0])
        self.bbWeldSideFlange_23.place(weldSideFlangOrigin_23, uDirSide_23, wDirSide_23)

    def create_bbWeldSideFlange_24(self):
        weldSideFlangOrigin_24 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2])
        uDirSide_24 = numpy.array([0, 1.0, 0])
        wDirSide_24 = numpy.array([0, 0, 1.0])
        self.bbWeldSideFlange_24.place(weldSideFlangOrigin_24, uDirSide_24, wDirSide_24)

    def create_bbWeldSideWeb_11(self):
        weldSideWebOrigin_11 = numpy.array([-self.beamLeft.t/2, self.beamLeft.length, self.beamLeft.D / 2 - self.beamLeft.T])
        uDirWeb_11 = numpy.array([0, -1.0, 0])
        wDirWeb_11 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_11.place(weldSideWebOrigin_11, uDirWeb_11, wDirWeb_11)

    def create_bbWeldSideWeb_12(self):
        weldSideWebOrigin_12 = numpy.array([self.beamLeft.t / 2, self.beamLeft.length, -self.beamLeft.D / 2 + self.beamLeft.T])
        uDirWeb_12 = numpy.array([0, -1.0, 0])
        wDirWeb_12 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_12.place(weldSideWebOrigin_12, uDirWeb_12, wDirWeb_12)

    def create_bbWeldSideWeb_21(self):
        weldSideWebOrigin_21 = numpy.array([-self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2 +
                                            self.beamLeft.T])
        uDirWeb_21 = numpy.array([0, 1.0, 0])
        wDirWeb_21 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_21.place(weldSideWebOrigin_21, uDirWeb_21, wDirWeb_21)

    def create_bbWeldSideWeb_22(self):
        weldSideWebOrigin_22 = numpy.array([self.beamLeft.t / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2 - self.beamLeft.T])
        uDirWeb_22 = numpy.array([0, 1.0, 0])
        wDirWeb_22 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_22.place(weldSideWebOrigin_22, uDirWeb_22, wDirWeb_22)

    def create_bbWeldQtrCone_11(self):  # Beam Left, upper flange, Left part of flange, upper side
        QtrOrigin_11 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length, self.beamLeft.D / 2])
        uDirQtr_11 = numpy.array([0, 0, 1.0])
        wDirQtr_11 = numpy.array([0, -1.0, 0])
        self.bbWeldQtrCone_11.place(QtrOrigin_11, uDirQtr_11, wDirQtr_11)

    def create_bbWeldQtrCone_12(self):  # Beam Left, upper flange, Left part of flange, lower side
        QtrOrigin_12 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length, self.beamLeft.D / 2 - self.beamLeft.T])
        uDirQtr_12 = numpy.array([-1.0, 0, 0])
        wDirQtr_12 = numpy.array([0, -1.0, 0])
        self.bbWeldQtrCone_12.place(QtrOrigin_12, uDirQtr_12, wDirQtr_12)

    def create_bbWeldQtrCone_13(self):  # Beam Left, upper flange, Right part of flange, upper side
        QtrOrigin_13 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, self.beamLeft.D / 2])
        uDirQtr_13 = numpy.array([1.0, 0, 0])
        wDirQtr_13 = numpy.array([0, -1.0, 0])
        self.bbWeldQtrCone_13.place(QtrOrigin_13, uDirQtr_13, wDirQtr_13)

    def create_bbWeldQtrCone_14(self):  # Beam Left, upper flange, Right part of flange, lower side
        QtrOrigin_14 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, self.beamLeft.D / 2 - self.beamLeft.T])
        uDirQtr_14 = numpy.array([0, 0, -1.0])
        wDirQtr_14 = numpy.array([0, -1.0, 0])
        self.bbWeldQtrCone_14.place(QtrOrigin_14, uDirQtr_14, wDirQtr_14)

    def create_bbWeldQtrCone_15(self):  # Beam Left, lower flange, Left part of flange, upper side
        QtrOrigin_15 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length, -self.beamLeft.D / 2 + self.beamLeft.T])
        uDirQtr_15 = numpy.array([0, 0, 1.0])
        wDirQtr_15 = numpy.array([0, -1.0, 0])
        self.bbWeldQtrCone_15.place(QtrOrigin_15, uDirQtr_15, wDirQtr_15)

    def create_bbWeldQtrCone_16(self):  # Beam Left, lower flange, Left part of flange, lower side
        QtrOrigin_16 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length, -self.beamLeft.D / 2])
        uDirQtr_16 = numpy.array([-1.0, 0, 0])
        wDirQtr_16 = numpy.array([0, -1.0, 0])
        self.bbWeldQtrCone_16.place(QtrOrigin_16, uDirQtr_16, wDirQtr_16)

    def create_bbWeldQtrCone_17(self):  # Beam Left, lower flange, Right part of flange, upper side
        QtrOrigin_17 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, -self.beamLeft.D / 2 + self.beamLeft.T])
        uDirQtr_17 = numpy.array([1.0, 0, 0])
        wDirQtr_17 = numpy.array([0, -1.0, 0])
        self.bbWeldQtrCone_17.place(QtrOrigin_17, uDirQtr_17, wDirQtr_17)

    def create_bbWeldQtrCone_18(self):  # Beam Left, lower flange, Right part of flange, lower side
        QtrOrigin_18 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length, -self.beamLeft.D / 2])
        uDirQtr_18 = numpy.array([0, 0, -1.0])
        wDirQtr_18 = numpy.array([0, -1.0, 0])
        self.bbWeldQtrCone_18.place(QtrOrigin_18, uDirQtr_18, wDirQtr_18)

    def create_bbWeldQtrCone_21(self):  # Replica of bbWeldQtrCone_11
        QtrOrigin_21 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2])
        uDirQtr_21 = numpy.array([-1.0, 0, 0])
        wDirQtr_21 = numpy.array([0, 1.0, 0])
        self.bbWeldQtrCone_21.place(QtrOrigin_21, uDirQtr_21, wDirQtr_21)

    def create_bbWeldQtrCone_22(self):  # Replica of bbWeldQtrCone_12
        QtrOrigin_22 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2 - self.beamLeft.T])
        uDirQtr_22 = numpy.array([0, 0, -1.0])
        wDirQtr_22 = numpy.array([0, 1.0, 0])
        self.bbWeldQtrCone_22.place(QtrOrigin_22, uDirQtr_22, wDirQtr_22)

    def create_bbWeldQtrCone_23(self):  # Replica of bbWeldQtrCone_13
        QtrOrigin_23 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2])
        uDirQtr_23 = numpy.array([0, 0, 1.0])
        wDirQtr_23 = numpy.array([0, 1.0, 0])
        self.bbWeldQtrCone_23.place(QtrOrigin_23, uDirQtr_23, wDirQtr_23)

    def create_bbWeldQtrCone_24(self):  # Replica of bbWeldQtrCone_14
        QtrOrigin_24 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, self.beamLeft.D / 2 - self.beamLeft.T])
        uDirQtr_24 = numpy.array([1.0, 0, 0])
        wDirQtr_24 = numpy.array([0, 1.0, 0])
        self.bbWeldQtrCone_24.place(QtrOrigin_24, uDirQtr_24, wDirQtr_24)

    def create_bbWeldQtrCone_25(self):  # Replica of bbWeldQtrCone_15
        QtrOrigin_25 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2 + self.beamLeft.T])
        uDirQtr_25 = numpy.array([-1.0, 0, 0])
        wDirQtr_25 = numpy.array([0, 1.0, 0])
        self.bbWeldQtrCone_25.place(QtrOrigin_25, uDirQtr_25, wDirQtr_25)

    def create_bbWeldQtrCone_26(self):  # Replica of bbWeldQtrCone_16
        QtrOrigin_26 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2])
        uDirQtr_26 = numpy.array([0, 0, -1.0])
        wDirQtr_26 = numpy.array([0, 1.0, 0])
        self.bbWeldQtrCone_26.place(QtrOrigin_26, uDirQtr_26, wDirQtr_26)

    def create_bbWeldQtrCone_27(self):
        QtrOrigin_27 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2 + self.beamLeft.T])
        uDirQtr_27 = numpy.array([0, 0, 1.0])
        wDirQtr_27 = numpy.array([0, 1.0, 0])
        self.bbWeldQtrCone_27.place(QtrOrigin_27, uDirQtr_27, wDirQtr_27)

    def create_bbWeldQtrCone_28(self):
        QtrOrigin_28 = numpy.array([self.beamLeft.B / 2, self.beamLeft.length + 2 * self.plateLeft.T, -self.beamLeft.D / 2])
        uDirQtr_28 = numpy.array([1.0, 0, 0])
        wDirQtr_28 = numpy.array([0, 1.0, 0])
        self.bbWeldQtrCone_28.place(QtrOrigin_28, uDirQtr_28, wDirQtr_28)

#############################################################################################################
#   Following functions returns the CAD model to the function display_3DModel of main file                  #
#############################################################################################################
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

    def get_bbWeldSideFlange_11Model(self):
        return self.bbWeldSideFlange_11Model

    def get_bbWeldSideFlange_12Model(self):
        return self.bbWeldSideFlange_12Model

    def get_bbWeldSideFlange_13Model(self):
        return self.bbWeldSideFlange_13Model

    def get_bbWeldSideFlange_14Model(self):
        return self.bbWeldSideFlange_14Model

    def get_bbWeldSideFlange_21Model(self):
        return self.bbWeldSideFlange_21Model

    def get_bbWeldSideFlange_22Model(self):
        return self.bbWeldSideFlange_22Model

    def get_bbWeldSideFlange_23Model(self):
        return self.bbWeldSideFlange_23Model

    def get_bbWeldSideFlange_24Model(self):
        return self.bbWeldSideFlange_24Model

    def get_bbWeldSideWeb_11Model(self):
        return self.bbWeldSideWeb_11Model

    def get_bbWeldSideWeb_12Model(self):
        return self.bbWeldSideWeb_12Model

    def get_bbWeldSideWeb_21Model(self):
        return self.bbWeldSideWeb_21Model

    def get_bbWeldSideWeb_22Model(self):
        return self.bbWeldSideWeb_22Model

    def get_bbWeldQtrCone_11Model(self):
        return self.bbWeldQtrCone_11Model

    def get_bbWeldQtrCone_12Model(self):
        return self.bbWeldQtrCone_12Model

    def get_bbWeldQtrCone_13Model(self):
        return self.bbWeldQtrCone_13Model

    def get_bbWeldQtrCone_14Model(self):
        return self.bbWeldQtrCone_14Model

    def get_bbWeldQtrCone_15Model(self):
        return self.bbWeldQtrCone_15Model

    def get_bbWeldQtrCone_16Model(self):
        return self.bbWeldQtrCone_16Model

    def get_bbWeldQtrCone_17Model(self):
        return self.bbWeldQtrCone_17Model

    def get_bbWeldQtrCone_18Model(self):
        return self.bbWeldQtrCone_18Model

    def get_bbWeldQtrCone_21Model(self):
        return self.bbWeldQtrCone_21Model

    def get_bbWeldQtrCone_22Model(self):
        return self.bbWeldQtrCone_22Model

    def get_bbWeldQtrCone_23Model(self):
        return self.bbWeldQtrCone_23Model

    def get_bbWeldQtrCone_24Model(self):
        return self.bbWeldQtrCone_24Model

    def get_bbWeldQtrCone_25Model(self):
        return self.bbWeldQtrCone_25Model

    def get_bbWeldQtrCone_26Model(self):
        return self.bbWeldQtrCone_26Model

    def get_bbWeldQtrCone_27Model(self):
        return self.bbWeldQtrCone_27Model

    def get_bbWeldQtrCone_28Model(self):
        return self.bbWeldQtrCone_28Model
