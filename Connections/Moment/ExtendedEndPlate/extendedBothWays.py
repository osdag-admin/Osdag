"""
Initialized on 22-01-2018
Commenced on 16-02-2018
@author: Siddhesh S. Chavan
"""""

import numpy


class CADFillet(object):

    def __init__(self, beamLeft, beamRight, plateLeft, plateRight, nut_bolt_array,
                 bbWeldAbvFlang_11, bbWeldAbvFlang_12, bbWeldAbvFlang_21, bbWeldAbvFlang_22,
                 bbWeldBelwFlang_11, bbWeldBelwFlang_12, bbWeldBelwFlang_13, bbWeldBelwFlang_14,
                 bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23, bbWeldBelwFlang_24,
                 bbWeldSideWeb_11, bbWeldSideWeb_12, bbWeldSideWeb_21, bbWeldSideWeb_22,
                 bbWeldstiff1_u1, bbWeldstiff1_u2, bbWeldstiff2_u1, bbWeldstiff2_u2, bbWeldstiff3_u1,
                 bbWeldstiff3_u2, bbWeldstiff4_u1, bbWeldstiff4_u2,
                 bbWeldstiff1_l1, bbWeldstiff1_l2, bbWeldstiff2_l1, bbWeldstiff2_l2, bbWeldstiff3_l1,
                 bbWeldstiff3_l2, bbWeldstiff4_l1, bbWeldstiff4_l2,
                 bbWeldStiffHL_1, bbWeldStiffHL_2, bbWeldStiffHL_3, bbWeldStiffHL_4,
                 bbWeldStiffLL_1, bbWeldStiffLL_2, bbWeldStiffLL_3, bbWeldStiffLL_4,
                 bbWeldStiffHR_1, bbWeldStiffHR_2, bbWeldStiffHR_3, bbWeldStiffHR_4,
                 bbWeldStiffLR_1, bbWeldStiffLR_2, bbWeldStiffLR_3, bbWeldStiffLR_4,
                 beam_stiffener_1, beam_stiffener_2, beam_stiffener_3,beam_stiffener_4,
                 beam_stiffener_F1,beam_stiffener_F2,beam_stiffener_F3,beam_stiffener_F4,alist, outputobj):

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
        self.beam_stiffener_1 = beam_stiffener_1
        self.beam_stiffener_2 = beam_stiffener_2
        self.beam_stiffener_3 = beam_stiffener_3
        self.beam_stiffener_4 = beam_stiffener_4

        self.beam_stiffener_F1 = beam_stiffener_F1
        self.beam_stiffener_F2 = beam_stiffener_F2
        self.beam_stiffener_F3 = beam_stiffener_F3
        self.beam_stiffener_F4 = beam_stiffener_F4
        self.alist = alist
        self.outputobj = outputobj
        self.boltProjection = float(outputobj['Plate']['Projection'])
        if alist["Member"]["Connectivity"] == "Flush":
            self.loc = float(outputobj['Stiffener']['Location'])

        else:
            self.loc = 0
        # self.boltProjection = float(outputobj["Bolt"]['projection'])          #TODO: ask danish to edit it into dictionary

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

        self.bbWeldStiffHL_1 = bbWeldStiffHL_1
        self.bbWeldStiffHL_2 = bbWeldStiffHL_2
        self.bbWeldStiffHL_3 = bbWeldStiffHL_3
        self.bbWeldStiffHL_4 = bbWeldStiffHL_4

        self.bbWeldStiffLL_1 = bbWeldStiffLL_1
        self.bbWeldStiffLL_2 = bbWeldStiffLL_2
        self.bbWeldStiffLL_3 = bbWeldStiffLL_3
        self.bbWeldStiffLL_4 = bbWeldStiffLL_4

        self.bbWeldStiffHR_1 = bbWeldStiffHR_1
        self.bbWeldStiffHR_2 = bbWeldStiffHR_2
        self.bbWeldStiffHR_3 = bbWeldStiffHR_3
        self.bbWeldStiffHR_4 = bbWeldStiffHR_4

        self.bbWeldStiffLR_1 = bbWeldStiffLR_1
        self.bbWeldStiffLR_2 = bbWeldStiffLR_2
        self.bbWeldStiffLR_3 = bbWeldStiffLR_3
        self.bbWeldStiffLR_4 = bbWeldStiffLR_4

        self.bbWeldstiff1_u1 = bbWeldstiff1_u1
        self.bbWeldstiff1_u2 = bbWeldstiff1_u2
        self.bbWeldstiff1_l1 = bbWeldstiff1_l1
        self.bbWeldstiff1_l2 = bbWeldstiff1_l2

        self.bbWeldstiff2_u1 = bbWeldstiff2_u1
        self.bbWeldstiff2_u2 = bbWeldstiff2_u2
        self.bbWeldstiff2_l1 = bbWeldstiff2_l1
        self.bbWeldstiff2_l2 = bbWeldstiff2_l2

        self.bbWeldstiff3_u1 = bbWeldstiff3_u1
        self.bbWeldstiff3_u2 = bbWeldstiff3_u2
        self.bbWeldstiff3_l1 = bbWeldstiff3_l1
        self.bbWeldstiff3_l2 = bbWeldstiff3_l2

        self.bbWeldstiff4_u1 = bbWeldstiff4_u1
        self.bbWeldstiff4_u2 = bbWeldstiff4_u2
        self.bbWeldstiff4_l1 = bbWeldstiff4_l1
        self.bbWeldstiff4_l2 = bbWeldstiff4_l2


    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateLGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.createbeam_stiffener_1Geometry()
        self.createbeam_stiffener_2Geometry()
        self.createbeam_stiffener_3Geometry()
        self.createbeam_stiffener_4Geometry()

        self.createbeam_stiffener_F1Geometry()
        self.createbeam_stiffener_F2Geometry()
        self.createbeam_stiffener_F3Geometry()
        self.createbeam_stiffener_F4Geometry()

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

        self.create_bbWeldStiffHL_1()
        self.create_bbWeldStiffHL_2()
        self.create_bbWeldStiffHL_3()
        self.create_bbWeldStiffHL_4()

        self.create_bbWeldStiffLL_1()
        self.create_bbWeldStiffLL_2()
        self.create_bbWeldStiffLL_3()
        self.create_bbWeldStiffLL_4()

        self.create_bbWeldStiffHR_1()
        self.create_bbWeldStiffHR_2()
        self.create_bbWeldStiffHR_3()
        self.create_bbWeldStiffHR_4()

        self.create_bbWeldStiffLR_1()
        self.create_bbWeldStiffLR_2()
        self.create_bbWeldStiffLR_3()
        self.create_bbWeldStiffLR_4()

        self.create_bbWeldstiff1_u1()
        self.create_bbWeldstiff1_u2()
        self.create_bbWeldstiff1_l1()
        self.create_bbWeldstiff1_l2()

        self.create_bbWeldstiff2_u1()
        self.create_bbWeldstiff2_u2()
        self.create_bbWeldstiff2_l1()
        self.create_bbWeldstiff2_l2()

        self.create_bbWeldstiff3_u1()
        self.create_bbWeldstiff3_u2()
        self.create_bbWeldstiff3_l1()
        self.create_bbWeldstiff3_l2()

        self.create_bbWeldstiff4_u1()
        self.create_bbWeldstiff4_u2()
        self.create_bbWeldstiff4_l1()
        self.create_bbWeldstiff4_l2()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateLModel = self.plateLeft.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()
        self.beam_stiffener_3Model = self.beam_stiffener_3.create_model()
        self.beam_stiffener_4Model = self.beam_stiffener_4.create_model()

        self.beam_stiffener_F1Model = self.beam_stiffener_F1.create_model()
        self.beam_stiffener_F2Model = self.beam_stiffener_F2.create_model()
        self.beam_stiffener_F3Model = self.beam_stiffener_F3.create_model()
        self.beam_stiffener_F4Model = self.beam_stiffener_F4.create_model()

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

        self.bbWeldStiffHL_1Model = self.bbWeldStiffHL_1.create_model()
        self.bbWeldStiffHL_2Model = self.bbWeldStiffHL_2.create_model()
        self.bbWeldStiffHL_3Model = self.bbWeldStiffHL_3.create_model()
        self.bbWeldStiffHL_4Model = self.bbWeldStiffHL_4.create_model()

        self.bbWeldStiffLL_1Model = self.bbWeldStiffLL_1.create_model()
        self.bbWeldStiffLL_2Model = self.bbWeldStiffLL_2.create_model()
        self.bbWeldStiffLL_3Model = self.bbWeldStiffLL_3.create_model()
        self.bbWeldStiffLL_4Model = self.bbWeldStiffLL_4.create_model()
        self.bbWeldStiffHR_1Model = self.bbWeldStiffHR_1.create_model()
        self.bbWeldStiffHR_2Model = self.bbWeldStiffHR_2.create_model()
        self.bbWeldStiffHR_3Model = self.bbWeldStiffHR_3.create_model()
        self.bbWeldStiffHR_4Model = self.bbWeldStiffHR_4.create_model()

        self.bbWeldStiffLR_1Model = self.bbWeldStiffLR_1.create_model()
        self.bbWeldStiffLR_2Model = self.bbWeldStiffLR_2.create_model()
        self.bbWeldStiffLR_3Model = self.bbWeldStiffLR_3.create_model()
        self.bbWeldStiffLR_4Model = self.bbWeldStiffLR_4.create_model()

        self.bbWeldstiff1_u1Model = self.bbWeldstiff1_u1.create_model()
        self.bbWeldstiff1_u2Model = self.bbWeldstiff1_u2.create_model()
        self.bbWeldstiff1_l1Model = self.bbWeldstiff1_l1.create_model()
        self.bbWeldstiff1_l2Model = self.bbWeldstiff1_l2.create_model()

        self.bbWeldstiff2_u1Model = self.bbWeldstiff2_u1.create_model()
        self.bbWeldstiff2_u2Model = self.bbWeldstiff2_u2.create_model()
        self.bbWeldstiff2_l1Model = self.bbWeldstiff2_l1.create_model()
        self.bbWeldstiff2_l2Model = self.bbWeldstiff2_l2.create_model()

        self.bbWeldstiff3_u1Model = self.bbWeldstiff3_u1.create_model()
        self.bbWeldstiff3_u2Model = self.bbWeldstiff3_u2.create_model()
        self.bbWeldstiff3_l1Model = self.bbWeldstiff3_l1.create_model()
        self.bbWeldstiff3_l2Model = self.bbWeldstiff3_l2.create_model()

        self.bbWeldstiff4_u1Model = self.bbWeldstiff4_u1.create_model()
        self.bbWeldstiff4_u2Model = self.bbWeldstiff4_u2.create_model()
        self.bbWeldstiff4_l1Model = self.bbWeldstiff4_l1.create_model()
        self.bbWeldstiff4_l2Model = self.bbWeldstiff4_l2.create_model()


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

        if self.alist["Member"]["Connectivity"] == "Extended one way":
            plateOriginL = numpy.array([-self.plateLeft.W/2, self.beamRight.length + 0.5 * self.plateLeft.T, (self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])
            plateL_uDir = numpy.array([0.0, 1.0, 0.0])    #TODO: self.boltProjection
            plateL_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

        else:
            plateOriginL = numpy.array([-self.plateLeft.W / 2, self.beamRight.length + 0.5 * self.plateLeft.T, 0.0])
            plateL_uDir = numpy.array([0.0, 1.0, 0.0])
            plateL_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

    def createPlateRGeometry(self):

        if self.alist["Member"]["Connectivity"] == "Extended one way":
            gap = 1.5 * self.plateRight.T + self.beamLeft.length
            plateOriginR = numpy.array([-self.plateRight.W/2, gap, (self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:
            gap = 1.5 * self.plateRight.T + self.beamLeft.length
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, 0.0])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        nutboltArrayOrigin = self.plateLeft.sec_origin + numpy.array([0.0, -0.5 * self.plateLeft.T, self.plateLeft.L/2])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, 0, -1.0])
        boltDir = numpy.array([0, 1.0, 0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def createbeam_stiffener_1Geometry(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                         self.beamRight.D / 2 + self.beam_stiffener_1.W / 2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

    def createbeam_stiffener_2Geometry(self):
        gap = self.beamLeft.length + self.plateLeft.T +  self.plateRight.T+ self.beam_stiffener_1.L / 2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                         - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    def createbeam_stiffener_3Geometry(self):
        gap = self.beamLeft.length - self.beam_stiffener_1.L / 2
        stiffenerOrigin3 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                         self.beamRight.D / 2 + self.beam_stiffener_1.W / 2])
        stiffener3_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener3_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_3.place(stiffenerOrigin3, stiffener3_uDir, stiffener3_wDir)

    def createbeam_stiffener_4Geometry(self):
        gap = self.beamLeft.length - self.beam_stiffener_1.L / 2
        stiffenerOrigin4 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                         - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2])
        stiffener4_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener4_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_4.place(stiffenerOrigin4, stiffener4_uDir, stiffener4_wDir)

    def createbeam_stiffener_F1Geometry(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L / 2
        stiffenerOriginF1 = numpy.array([-self.beam_stiffener_F1.W/2 - self.beamLeft.t/2, gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffenerF1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF1_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F1.place(stiffenerOriginF1, stiffenerF1_uDir, stiffenerF1_wDir)

    def createbeam_stiffener_F2Geometry(self):
        gap = self.beamLeft.length - self.beam_stiffener_F2.L / 2
        stiffenerOriginF2 = numpy.array([self.beam_stiffener_F2.W/2 + self.beamLeft.t/2 , gap,
                                         self.beamRight.D / 2 -self.beam_stiffener_2.T - self.loc])
        stiffenerF2_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF2_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F2.place(stiffenerOriginF2, stiffenerF2_uDir, stiffenerF2_wDir)


    def createbeam_stiffener_F3Geometry(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L / 2
        stiffenerOriginF3 = numpy.array([-(self.beam_stiffener_F3.W/2 + self.beamRight.t/2), gap,
                                         self.beamRight.D / 2 -self.beam_stiffener_F3.T- self.loc])
        stiffenerF3_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffenerF3_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F3.place(stiffenerOriginF3, stiffenerF3_uDir, stiffenerF3_wDir)

    def createbeam_stiffener_F4Geometry(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F4.L / 2
        stiffenerOriginF4 = numpy.array([(self.beam_stiffener_F4.W/2 + self.beamRight.t/2), gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffenerF4_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffenerF4_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F4.place(stiffenerOriginF4, stiffenerF4_uDir, stiffenerF4_wDir)

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

    def create_bbWeldstiff1_u1(self):
        gap = self.beamLeft.length
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff1_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

    def create_bbWeldstiff1_u2(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L
        stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t/2 , gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff1_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

    def create_bbWeldstiff1_l1(self):
        gap = self.beamLeft.length
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                         self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff1_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bbWeldstiff1_l2(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L22
        stiffenerOrigin1_l2 = numpy.array([-self.beamLeft.t/2 , gap,
                                         self.beamRight.D / 2 - self.loc- self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff1_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

    def create_bbWeldstiff2_u1(self):
        gap = self.beamLeft.length
        stiffenerOrigin1_u1 = numpy.array([(self.beam_stiffener_F1.W + self.beamLeft.t / 2), gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff2_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

    def create_bbWeldstiff2_u2(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L
        stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t/2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff2_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

    def create_bbWeldstiff2_l1(self):
        gap = self.beamLeft.length
        stiffenerOrigin1_l1 = numpy.array([(self.beam_stiffener_F1.L22 + self.beamLeft.t / 2), gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff2_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bbWeldstiff2_l2(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L22
        stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t/2 , gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff2_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

    def create_bbWeldstiff3_u1(self):
        gap = self.beamLeft.length + self.plateLeft.T+self.plateRight.T
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff3_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

    def create_bbWeldstiff3_u2(self):
        gap = self.beamLeft.length + self.plateLeft.T+self.plateRight.T + self.beam_stiffener_F3.L22
        stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff3_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

    def create_bbWeldstiff3_l1(self):
        gap = self.beamLeft.length + self.plateLeft.T+self.plateRight.T
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc- self.beam_stiffener_F1.T ])
        stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff3_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bbWeldstiff3_l2(self):
        gap = self.beamLeft.length + self.plateLeft.T+self.plateRight.T + self.beam_stiffener_F3.L
        stiffenerOrigin3_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener3_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener3_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff3_l2.place(stiffenerOrigin3_l2, stiffener3_l2_uDir, stiffener3_l2_wDir)

    def create_bbWeldstiff4_u1(self):
        gap = self.beamLeft.length + self.plateLeft.T+self.plateRight.T
        stiffenerOrigin1_u1 = numpy.array([self.beam_stiffener_F1.L22 + self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff4_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

    def create_bbWeldstiff4_u2(self):
        gap = self.beamLeft.length + self.plateLeft.T+self.plateRight.T + self.beam_stiffener_F3.L22
        stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff4_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

    def create_bbWeldstiff4_l1(self):
        gap = self.beamLeft.length + self.plateLeft.T+self.plateRight.T
        stiffenerOrigin1_l1 = numpy.array([self.beam_stiffener_F1.W + self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc- self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff4_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bbWeldstiff4_l2(self):
        gap = self.beamLeft.length + self.plateLeft.T+self.plateRight.T + self.beam_stiffener_F3.L
        stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t/2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff4_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)


    ################################################# Welding Beam Stiffeners ###################################################


    def create_bbWeldStiffHL_1(self):
        weldstiffOriginH_1 = numpy.array([-self.beam_stiffener_1.T/2, self.beamLeft.length , self.beamLeft.D/2 + self.beam_stiffener_1.W ])
        uDirstiffH_1 = numpy.array([0, -1.0, 0])
        wDirstiffH_1 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHL_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)


    def create_bbWeldStiffLL_1(self):
        weldstiffOriginL_1 = numpy.array([-self.beam_stiffener_1.T/2, self.beamLeft.length - self.beam_stiffener_1.L22, self.beamLeft.D/2])
        uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldStiffLL_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)


    def create_bbWeldStiffHL_3(self):
        gap = self.beamLeft.length  + self.plateLeft.T + self.plateRight.T
        weldstiffOriginH_3 = numpy.array([self.beam_stiffener_3.T/2, gap, self.beamLeft.D/2 + self.beam_stiffener_3.W])
        uDirstiffH_3 = numpy.array([0, 1.0, 0])
        wDirstiffH_3 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHL_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)

    def create_bbWeldStiffLL_3(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22 + self.bbWeldStiffLL_3.L
        weldstiffOriginL_3 = numpy.array([-self.beam_stiffener_3.T/2, gap, self.beamLeft.D/2])
        uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_3 = numpy.array([0.0, -1.0,0.0])
        self.bbWeldStiffLL_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)


    def create_bbWeldStiffHL_2(self):
        weldstiffOriginH_2 = numpy.array([self.beam_stiffener_2.T/2, self.beamLeft.length, -(self.beamLeft.D/2 + self.beam_stiffener_3.W )])
        uDirstiffH_2 = numpy.array([0, -1.0, 0])
        wDirstiffH_2 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHL_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)


    def create_bbWeldStiffLL_2(self):
        weldstiffOriginL_2 = numpy.array([self.beamLeft.t/2 , self.beamLeft.length - self.beam_stiffener_1.L22 , -self.beamLeft.D/2 ])
        uDirstiffL_2 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_2 = numpy.array([0, -1.0, 0.0])
        self.bbWeldStiffLL_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)

    def create_bbWeldStiffHL_4(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        weldstiffOriginH_4 = numpy.array([-self.beam_stiffener_3.T/2, gap, -(self.beamLeft.D/2 + self.beam_stiffener_4.W)])
        uDirstiffH_4 = numpy.array([0, 1.0, 0])
        wDirstiffH_4 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHL_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)

    def create_bbWeldStiffLL_4(self):
        gap =  self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22 + self.bbWeldStiffLL_3.L
        weldstiffOriginL_4 = numpy.array([self.beamLeft.t/2, gap, -self.beamLeft.D/2 ])
        uDirstiffL_4 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_4 = numpy.array([0, -1.0, 0.0])
        self.bbWeldStiffLL_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)

    def create_bbWeldStiffHR_1(self):
        weldstiffOriginH_1 = numpy.array([self.beam_stiffener_1.T/2, self.beamLeft.length, self.beamLeft.D/2 + self.beam_stiffener_1.L21])
        uDirstiffH_1 = numpy.array([0, -1.0, 0])
        wDirstiffH_1 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHR_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)

    def create_bbWeldStiffLR_1(self):
        weldstiffOriginL_1 = numpy.array([self.beamLeft.t/2, self.beamLeft.length - self.beam_stiffener_2.L , self.beamLeft.D/2 ])
        uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldStiffLR_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)


    def create_bbWeldStiffHR_3(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T
        weldstiffOriginH_3 = numpy.array([-self.beam_stiffener_3.T/2, gap, self.beamLeft.D/2 + self.beam_stiffener_3.L21 ])
        uDirstiffH_3 = numpy.array([0, 1.0, 0])
        wDirstiffH_3 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHR_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)

    def create_bbWeldStiffLR_3(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22
        weldstiffOriginL_3 = numpy.array([self.beamLeft.t/2, gap , self.beamLeft.D/2 ])
        uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_3 = numpy.array([0.0, 1.0,0.0])
        self.bbWeldStiffLR_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)


    def create_bbWeldStiffHR_2(self):
        weldstiffOriginH_2 = numpy.array([-self.beam_stiffener_2.T/2, self.beamLeft.length, -(self.beamLeft.D/2 + self.beam_stiffener_2.L21)])
        uDirstiffH_2 = numpy.array([0, -1.0, 0])
        wDirstiffH_2 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHR_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)


    def create_bbWeldStiffLR_2(self):
        weldstiffOriginL_2 = numpy.array([-self.beam_stiffener_2.T/2 , self.beamLeft.length - self.beam_stiffener_2.L , -self.beamLeft.D/2])
        uDirstiffL_2 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_2 = numpy.array([0, 1.0, 0.0])
        self.bbWeldStiffLR_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)

    def create_bbWeldStiffHR_4(self):
        gap = self.beamLeft.length  + self.plateLeft.T + self.plateRight.T
        weldstiffOriginH_4 = numpy.array([self.beam_stiffener_4.T/2, gap, -(self.beamLeft.D/2 + self.beam_stiffener_4.L21)])
        uDirstiffH_4 = numpy.array([0, 1.0, 0])
        wDirstiffH_4 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHR_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)

    def create_bbWeldStiffLR_4(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22
        weldstiffOriginL_4 = numpy.array([-self.beamLeft.t/2, gap , -self.beamLeft.D/2 ])
        uDirstiffL_4 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_4 = numpy.array([0, 1.0, 0.0])
        self.bbWeldStiffLR_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)

#############################################################################################################
#   Following functions returns the CAD model to the function display_3DModel of main file                  #
#############################################################################################################
    # def get_beam_models(self):
    #     '''
    #
    #     Returns: Returns model of beam (left and right)
    #
    #     '''
    #     return [self.beamRModel, self.beamLModel]
    #
    # def get_connector_models(self):
    #     '''
    #
    #     Returns: Returns model related to connector (plates and weld)
    #
    #     '''
    #     return [self.plateRModel, self.plateLModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model, self.beam_stiffener_3Model,
    #             self.beam_stiffener_4Model, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
    #             self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model,
    #             self.bbWeldBelwFlang_13Model, self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model, self.bbWeldBelwFlang_22Model,
    #             self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model, self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model,
    #             self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model] + self.nut_bolt_array.get_models()
    #
    # def get_models(self):
    #     '''
    #
    #     Returns: Returns model related to complete model (beams, plates and weld)
    #
    #     '''
    #     return [self.beamRModel, self.beamLModel, self.plateRModel, self.plateLModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
    #             self.beam_stiffener_3Model, self.beam_stiffener_4Model, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
    #             self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model,
    #             self.bbWeldBelwFlang_13Model, self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model, self.bbWeldBelwFlang_22Model,
    #             self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model, self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model,
    #             self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model] + self.nut_bolt_array.get_models()


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

    def get_beam_stiffener_1Model(self):
        return self.beam_stiffener_1Model

    def get_beam_stiffener_2Model(self):
        return self.beam_stiffener_2Model

    def get_beam_stiffener_3Model(self):
        return self.beam_stiffener_3Model

    def get_beam_stiffener_4Model(self):
        return self.beam_stiffener_4Model

    def get_beam_stiffener_F1Model(self):
        return self.beam_stiffener_F1Model

    def get_beam_stiffener_F2Model(self):
        return self.beam_stiffener_F2Model

    def get_beam_stiffener_F3Model(self):
        return self.beam_stiffener_F3Model

    def get_beam_stiffener_F4Model(self):
        return self.beam_stiffener_F4Model

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

    def get_bbWeldStiffHL_1Model(self):
        return self.bbWeldStiffHL_1Model

    def get_bbWeldStiffLL_1Model(self):
        return self.bbWeldStiffLL_1Model

    def get_bbWeldStiffHL_3Model(self):
        return self.bbWeldStiffHL_3Model

    def get_bbWeldStiffLL_3Model(self):
        return self.bbWeldStiffLL_3Model

    def get_bbWeldStiffHL_2Model(self):
        return self.bbWeldStiffHL_2Model

    def get_bbWeldStiffLL_2Model(self):
        return self.bbWeldStiffLL_2Model

    def get_bbWeldStiffHL_4Model(self):
        return self.bbWeldStiffHL_4Model

    def get_bbWeldStiffLL_4Model(self):
        return self.bbWeldStiffLL_4Model

    def get_bbWeldStiffHR_1Model(self):
        return self.bbWeldStiffHR_1Model

    def get_bbWeldStiffLR_1Model(self):
        return self.bbWeldStiffLR_1Model

    def get_bbWeldStiffHR_3Model(self):
        return self.bbWeldStiffHR_3Model

    def get_bbWeldStiffLR_3Model(self):
        return self.bbWeldStiffLR_3Model

    def get_bbWeldStiffHR_2Model(self):
        return self.bbWeldStiffHR_2Model

    def get_bbWeldStiffLR_2Model(self):
        return self.bbWeldStiffLR_2Model

    def get_bbWeldStiffHR_4Model(self):
        return self.bbWeldStiffHR_4Model

    def get_bbWeldStiffLR_4Model(self):
        return self.bbWeldStiffLR_4Model

    def get_bbWeldstiff1_u1Model(self):
        return self.bbWeldstiff1_u1Model

    def get_bbWeldstiff1_u2Model(self):
        return self.bbWeldstiff1_u2Model

    def get_bbWeldstiff1_l1Model(self):
        return self.bbWeldstiff1_l1Model

    def get_bbWeldstiff1_l2Model(self):
        return self.bbWeldstiff1_l2Model

    def get_bbWeldstiff2_u1Model(self):
        return self.bbWeldstiff2_u1Model

    def get_bbWeldstiff2_u2Model(self):
        return self.bbWeldstiff2_u2Model

    def get_bbWeldstiff2_l1Model(self):
        return self.bbWeldstiff2_l1Model

    def get_bbWeldstiff2_l2Model(self):
        return self.bbWeldstiff2_l2Model

    def get_bbWeldstiff3_u1Model(self):
        return self.bbWeldstiff3_u1Model

    def get_bbWeldstiff3_u2Model(self):
        return self.bbWeldstiff3_u2Model

    def get_bbWeldstiff3_l1Model(self):
        return self.bbWeldstiff3_l1Model

    def get_bbWeldstiff3_l2Model(self):
        return self.bbWeldstiff3_l2Model

    def get_bbWeldstiff4_u1Model(self):
        return self.bbWeldstiff4_u1Model

    def get_bbWeldstiff4_u2Model(self):
        return self.bbWeldstiff4_u2Model

    def get_bbWeldstiff4_l1Model(self):
        return self.bbWeldstiff4_l1Model

    def get_bbWeldstiff4_l2Model(self):
        return self.bbWeldstiff4_l2Model

    def get_models(self):
        '''Returning 3D models
        '''
        if self.alist["Member"]["Connectivity"] == "Extended one way":
            return [self.beamLModel, self.beamRModel, self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
                    self.beam_stiffener_3Model, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
                    self.bbWeldAbvFlang_21Model,
                    self.bbWeldAbvFlang_22Model,
                    self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model, self.bbWeldBelwFlang_13Model,
                    self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model, self.bbWeldSideWeb_21Model,
                    self.bbWeldSideWeb_22Model, self.bbWeldStiffHL_1Model,
                    self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
                     self.bbWeldStiffHR_1Model,
                    self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
                    self.bbWeldStiffLR_3Model,
                    ] + self.nut_bolt_array.get_models()
        elif self.alist["Member"]["Connectivity"] == "Extended both ways":
            return [self.beamLModel, self.beamRModel, self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
                    self.beam_stiffener_2Model, self.beam_stiffener_3Model,
                    self.beam_stiffener_4Model, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
                    self.bbWeldAbvFlang_21Model,
                    self.bbWeldAbvFlang_22Model,
                    self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model, self.bbWeldBelwFlang_13Model,
                    self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model, self.bbWeldSideWeb_21Model,
                    self.bbWeldSideWeb_22Model, self.bbWeldStiffHL_1Model,
                    self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
                    self.bbWeldStiffHL_2Model, self.bbWeldStiffLL_2Model,
                    self.bbWeldStiffHL_4Model, self.bbWeldStiffLL_4Model, self.bbWeldStiffHR_1Model,
                    self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
                    self.bbWeldStiffLR_3Model, self.bbWeldStiffHR_2Model, self.bbWeldStiffLR_2Model,
                    self.bbWeldStiffHR_4Model, self.bbWeldStiffLR_4Model,
                     ] + self.nut_bolt_array.get_models()
        elif self.alist["Member"]["Connectivity"] == "Flush":

            return [self.beamLModel, self.beamRModel, self.plateLModel, self.plateRModel, self.beam_stiffener_F1Model, self.beam_stiffener_F2Model,
                    self.beam_stiffener_F3Model,self.beam_stiffener_F4Model, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
                    self.bbWeldAbvFlang_21Model,
                    self.bbWeldAbvFlang_22Model,
                    self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model, self.bbWeldBelwFlang_13Model,
                    self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model, self.bbWeldSideWeb_21Model,
                    self.bbWeldSideWeb_22Model,
                    self.bbWeldstiff1_u1Model, self.bbWeldstiff1_u2Model, self.bbWeldstiff1_l1Model,
                    self.bbWeldstiff1_l2Model, self.bbWeldstiff2_u1Model,
                    self.bbWeldstiff2_u2Model, self.bbWeldstiff2_l1Model, self.bbWeldstiff2_l2Model,
                    self.bbWeldstiff3_u1Model, self.bbWeldstiff3_u2Model,
                    self.bbWeldstiff3_l1Model, self.bbWeldstiff3_l2Model, self.bbWeldstiff4_u1Model,
                    self.bbWeldstiff4_u2Model, self.bbWeldstiff4_l1Model,
                    self.bbWeldstiff4_l2Model, ] + self.nut_bolt_array.get_models()

        # return [self.beamLModel, self.beamRModel, self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
        #         self.beam_stiffener_2Model, self.beam_stiffener_3Model,
        #         self.beam_stiffener_4Model, self.beam_stiffener_F1Model, self.beam_stiffener_F2Model,
        #         self.beam_stiffener_F3Model,
        #         self.beam_stiffener_F4Model, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
        #         self.bbWeldAbvFlang_21Model,
        #         self.bbWeldAbvFlang_22Model,
        #         self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model, self.bbWeldBelwFlang_13Model,
        #         self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model,
        #         self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
        #         self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model, self.bbWeldSideWeb_21Model,
        #         self.bbWeldSideWeb_22Model, self.bbWeldStiffHL_1Model,
        #         self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
        #         self.bbWeldStiffHL_2Model, self.bbWeldStiffLL_2Model,
        #         self.bbWeldStiffHL_4Model, self.bbWeldStiffLL_4Model, self.bbWeldStiffHR_1Model,
        #         self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
        #         self.bbWeldStiffLR_3Model, self.bbWeldStiffHR_2Model, self.bbWeldStiffLR_2Model,
        #         self.bbWeldStiffHR_4Model, self.bbWeldStiffLR_4Model,
        #         self.bbWeldstiff1_u1Model, self.bbWeldstiff1_u2Model, self.bbWeldstiff1_l1Model,
        #         self.bbWeldstiff1_l2Model, self.bbWeldstiff2_u1Model,
        #         self.bbWeldstiff2_u2Model, self.bbWeldstiff2_l1Model, self.bbWeldstiff2_l2Model,
        #         self.bbWeldstiff3_u1Model, self.bbWeldstiff3_u2Model,
        #         self.bbWeldstiff3_l1Model, self.bbWeldstiff3_l2Model, self.bbWeldstiff4_u1Model,
        #         self.bbWeldstiff4_u2Model, self.bbWeldstiff4_l1Model,
        #         self.bbWeldstiff4_l2Model, ] + self.nut_bolt_array.get_models()



class CADGroove(object):
    def __init__(self,beamLeft,beamRight, plateLeft, plateRight, nut_bolt_array,
									bbWeldFlang_R1, bbWeldFlang_R2, bbWeldWeb_R3,bbWeldFlang_L1, bbWeldFlang_L2, bbWeldWeb_L3,
                                     bbWeldStiffHL_1, bbWeldStiffHL_2, bbWeldStiffHL_3, bbWeldStiffHL_4,
                                     bbWeldStiffLL_1, bbWeldStiffLL_2, bbWeldStiffLL_3, bbWeldStiffLL_4,
                                     bbWeldStiffHR_1, bbWeldStiffHR_2, bbWeldStiffHR_3, bbWeldStiffHR_4,
                                     bbWeldStiffLR_1, bbWeldStiffLR_2, bbWeldStiffLR_3, bbWeldStiffLR_4,
                                     bbWeldstiff1_u1, bbWeldstiff1_u2, bbWeldstiff2_u1, bbWeldstiff2_u2, bbWeldstiff3_u1,
                                     bbWeldstiff3_u2, bbWeldstiff4_u1, bbWeldstiff4_u2,
                                     bbWeldstiff1_l1, bbWeldstiff1_l2, bbWeldstiff2_l1, bbWeldstiff2_l2, bbWeldstiff3_l1,
                                     bbWeldstiff3_l2, bbWeldstiff4_l1, bbWeldstiff4_l2,
									beam_stiffener_1, beam_stiffener_2,beam_stiffener_3, beam_stiffener_4,
                 beam_stiffener_F1,beam_stiffener_F2,beam_stiffener_F3,beam_stiffener_F4, alist, outputobj):
        self.beamLeft = beamLeft
        self.beamRight = beamRight
        self.plateLeft = plateLeft
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.beamLModel = None
        self.beamRModel = None
        self.plateLModel = None
        self.plateRModel = None
        self.beam_stiffener_1 = beam_stiffener_1
        self.beam_stiffener_2 = beam_stiffener_2
        self.beam_stiffener_3 = beam_stiffener_3
        self.beam_stiffener_4 = beam_stiffener_4

        self.beam_stiffener_F1 = beam_stiffener_F1
        self.beam_stiffener_F2 = beam_stiffener_F2
        self.beam_stiffener_F3 = beam_stiffener_F3
        self.beam_stiffener_F4 = beam_stiffener_F4
        self.alist = alist
        self.outputobj = outputobj
        self.boltProjection = float(outputobj['Plate']['Projection'])
        if alist["Member"]["Connectivity"] == "Flush":
            self.loc = float(outputobj['Stiffener']['Location'])

        else:
            self.loc = 0

        self.bbWeldFlang_R1 = bbWeldFlang_R1
        self.bbWeldFlang_R2 = bbWeldFlang_R2
        self.bbWeldFlang_L1 = bbWeldFlang_L1
        self.bbWeldFlang_L2 = bbWeldFlang_L2
        self.bbWeldWeb_R3 = bbWeldWeb_R3
        self.bbWeldWeb_L3 = bbWeldWeb_L3


        #TODO: Grove weld for the stiffeneres are removed, may be added in the future
        # self.bbWeldStiffH_1 = bbWeldStiffH_1
        # self.bbWeldStiffH_2 = bbWeldStiffH_2
        # self.bbWeldStiffH_3 = bbWeldStiffH_3
        # self.bbWeldStiffH_4 = bbWeldStiffH_4
        #
        # self.bbWeldStiffL_1 = bbWeldStiffL_1
        # self.bbWeldStiffL_2 = bbWeldStiffL_2
        # self.bbWeldStiffL_3 = bbWeldStiffL_3
        # self.bbWeldStiffL_4 = bbWeldStiffL_4
        #Fillet weld
        self.bbWeldStiffHL_1 = bbWeldStiffHL_1
        self.bbWeldStiffHL_2 = bbWeldStiffHL_2
        self.bbWeldStiffHL_3 = bbWeldStiffHL_3
        self.bbWeldStiffHL_4 = bbWeldStiffHL_4

        self.bbWeldStiffLL_1 = bbWeldStiffLL_1
        self.bbWeldStiffLL_2 = bbWeldStiffLL_2
        self.bbWeldStiffLL_3 = bbWeldStiffLL_3
        self.bbWeldStiffLL_4 = bbWeldStiffLL_4

        self.bbWeldStiffHR_1 = bbWeldStiffHR_1
        self.bbWeldStiffHR_2 = bbWeldStiffHR_2
        self.bbWeldStiffHR_3 = bbWeldStiffHR_3
        self.bbWeldStiffHR_4 = bbWeldStiffHR_4

        self.bbWeldStiffLR_1 = bbWeldStiffLR_1
        self.bbWeldStiffLR_2 = bbWeldStiffLR_2
        self.bbWeldStiffLR_3 = bbWeldStiffLR_3
        self.bbWeldStiffLR_4 = bbWeldStiffLR_4

        self.bbWeldstiff1_u1 = bbWeldstiff1_u1
        self.bbWeldstiff1_u2 = bbWeldstiff1_u2
        self.bbWeldstiff1_l1 = bbWeldstiff1_l1
        self.bbWeldstiff1_l2 = bbWeldstiff1_l2

        self.bbWeldstiff2_u1 = bbWeldstiff2_u1
        self.bbWeldstiff2_u2 = bbWeldstiff2_u2
        self.bbWeldstiff2_l1 = bbWeldstiff2_l1
        self.bbWeldstiff2_l2 = bbWeldstiff2_l2

        self.bbWeldstiff3_u1 = bbWeldstiff3_u1
        self.bbWeldstiff3_u2 = bbWeldstiff3_u2
        self.bbWeldstiff3_l1 = bbWeldstiff3_l1
        self.bbWeldstiff3_l2 = bbWeldstiff3_l2

        self.bbWeldstiff4_u1 = bbWeldstiff4_u1
        self.bbWeldstiff4_u2 = bbWeldstiff4_u2
        self.bbWeldstiff4_l1 = bbWeldstiff4_l1
        self.bbWeldstiff4_l2 = bbWeldstiff4_l2



    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateLGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()

        self.createbeam_stiffener_1Geometry()
        self.createbeam_stiffener_2Geometry()
        self.createbeam_stiffener_3Geometry()
        self.createbeam_stiffener_4Geometry()

        self.createbeam_stiffener_F1Geometry()
        self.createbeam_stiffener_F2Geometry()
        self.createbeam_stiffener_F3Geometry()
        self.createbeam_stiffener_F4Geometry()

        self.create_bbWeldFlang_R1()
        self.create_bbWeldFlang_R2()
        self.create_bbWeldFlang_L1()
        self.create_bbWeldFlang_L2()
        self.create_bbWeldWeb_R3()
        self.create_bbWeldWeb_L3()

        #Groove weld
        # self.create_bbWeldStiffH_1()
        # self.create_bbWeldStiffH_2()
        # self.create_bbWeldStiffH_3()
        # self.create_bbWeldStiffH_4()
        #
        # self.create_bbWeldStiffL_1()
        # self.create_bbWeldStiffL_2()
        # self.create_bbWeldStiffL_3()
        # self.create_bbWeldStiffL_4()

        #Fillet weld
        self.create_bbWeldStiffHL_1()
        self.create_bbWeldStiffHL_2()
        self.create_bbWeldStiffHL_3()
        self.create_bbWeldStiffHL_4()

        self.create_bbWeldStiffLL_1()
        self.create_bbWeldStiffLL_2()
        self.create_bbWeldStiffLL_3()
        self.create_bbWeldStiffLL_4()

        self.create_bbWeldStiffHR_1()
        self.create_bbWeldStiffHR_2()
        self.create_bbWeldStiffHR_3()
        self.create_bbWeldStiffHR_4()

        self.create_bbWeldStiffLR_1()
        self.create_bbWeldStiffLR_2()
        self.create_bbWeldStiffLR_3()
        self.create_bbWeldStiffLR_4()


        self.create_bbWeldstiff1_u1()
        self.create_bbWeldstiff1_u2()
        self.create_bbWeldstiff1_l1()
        self.create_bbWeldstiff1_l2()

        self.create_bbWeldstiff2_u1()
        self.create_bbWeldstiff2_u2()
        self.create_bbWeldstiff2_l1()
        self.create_bbWeldstiff2_l2()

        self.create_bbWeldstiff3_u1()
        self.create_bbWeldstiff3_u2()
        self.create_bbWeldstiff3_l1()
        self.create_bbWeldstiff3_l2()

        self.create_bbWeldstiff4_u1()
        self.create_bbWeldstiff4_u2()
        self.create_bbWeldstiff4_l1()
        self.create_bbWeldstiff4_l2()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateLModel = self.plateLeft.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()

        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()
        self.beam_stiffener_3Model = self.beam_stiffener_3.create_model()
        self.beam_stiffener_4Model = self.beam_stiffener_4.create_model()

        self.beam_stiffener_F1Model = self.beam_stiffener_F1.create_model()
        self.beam_stiffener_F2Model = self.beam_stiffener_F2.create_model()
        self.beam_stiffener_F3Model = self.beam_stiffener_F3.create_model()
        self.beam_stiffener_F4Model = self.beam_stiffener_F4.create_model()

        self.bbWeldFlang_R1Model = self.bbWeldFlang_R1.create_model()
        self.bbWeldFlang_R2Model = self.bbWeldFlang_R2.create_model()
        self.bbWeldFlang_L1Model = self.bbWeldFlang_L1.create_model()
        self.bbWeldFlang_L2Model = self.bbWeldFlang_L2.create_model()
        self.bbWeldWeb_R3Model = self.bbWeldWeb_R3.create_model()
        self.bbWeldWeb_L3Model = self.bbWeldWeb_L3.create_model()

        #Grove weld
        # self.bbWeldStiffH_1Model = self.bbWeldStiffH_1.create_model()
        # self.bbWeldStiffH_2Model = self.bbWeldStiffH_2.create_model()
        # self.bbWeldStiffH_3Model = self.bbWeldStiffH_3.create_model()
        # self.bbWeldStiffH_4Model = self.bbWeldStiffH_4.create_model()
        #
        # self.bbWeldStiffL_1Model = self.bbWeldStiffL_1.create_model()
        # self.bbWeldStiffL_2Model = self.bbWeldStiffL_2.create_model()
        # self.bbWeldStiffL_3Model = self.bbWeldStiffL_3.create_model()
        # self.bbWeldStiffL_4Model = self.bbWeldStiffL_4.create_model()

        #Fillet weld
        self.bbWeldStiffHL_1Model = self.bbWeldStiffHL_1.create_model()
        self.bbWeldStiffHL_2Model = self.bbWeldStiffHL_2.create_model()
        self.bbWeldStiffHL_3Model = self.bbWeldStiffHL_3.create_model()
        self.bbWeldStiffHL_4Model = self.bbWeldStiffHL_4.create_model()

        self.bbWeldStiffLL_1Model = self.bbWeldStiffLL_1.create_model()
        self.bbWeldStiffLL_2Model = self.bbWeldStiffLL_2.create_model()
        self.bbWeldStiffLL_3Model = self.bbWeldStiffLL_3.create_model()
        self.bbWeldStiffLL_4Model = self.bbWeldStiffLL_4.create_model()
        self.bbWeldStiffHR_1Model = self.bbWeldStiffHR_1.create_model()
        self.bbWeldStiffHR_2Model = self.bbWeldStiffHR_2.create_model()
        self.bbWeldStiffHR_3Model = self.bbWeldStiffHR_3.create_model()
        self.bbWeldStiffHR_4Model = self.bbWeldStiffHR_4.create_model()

        self.bbWeldStiffLR_1Model = self.bbWeldStiffLR_1.create_model()
        self.bbWeldStiffLR_2Model = self.bbWeldStiffLR_2.create_model()
        self.bbWeldStiffLR_3Model = self.bbWeldStiffLR_3.create_model()
        self.bbWeldStiffLR_4Model = self.bbWeldStiffLR_4.create_model()



        self.bbWeldstiff1_u1Model = self.bbWeldstiff1_u1.create_model()
        self.bbWeldstiff1_u2Model = self.bbWeldstiff1_u2.create_model()
        self.bbWeldstiff1_l1Model = self.bbWeldstiff1_l1.create_model()
        self.bbWeldstiff1_l2Model = self.bbWeldstiff1_l2.create_model()

        self.bbWeldstiff2_u1Model = self.bbWeldstiff2_u1.create_model()
        self.bbWeldstiff2_u2Model = self.bbWeldstiff2_u2.create_model()
        self.bbWeldstiff2_l1Model = self.bbWeldstiff2_l1.create_model()
        self.bbWeldstiff2_l2Model = self.bbWeldstiff2_l2.create_model()

        self.bbWeldstiff3_u1Model = self.bbWeldstiff3_u1.create_model()
        self.bbWeldstiff3_u2Model = self.bbWeldstiff3_u2.create_model()
        self.bbWeldstiff3_l1Model = self.bbWeldstiff3_l1.create_model()
        self.bbWeldstiff3_l2Model = self.bbWeldstiff3_l2.create_model()

        self.bbWeldstiff4_u1Model = self.bbWeldstiff4_u1.create_model()
        self.bbWeldstiff4_u2Model = self.bbWeldstiff4_u2.create_model()
        self.bbWeldstiff4_l1Model = self.bbWeldstiff4_l1.create_model()
        self.bbWeldstiff4_l2Model = self.bbWeldstiff4_l2.create_model()




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
        gap = self.beamRight.length + 2 * self.plateRight.T + 2* self.bbWeldWeb_L3.b
        beamOriginR = numpy.array([0.0, gap, 0.0])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateLGeometry(self):

        if self.alist["Member"]["Connectivity"] == "Extended one way":
            plateOriginL = numpy.array([-self.plateLeft.W / 2, self.beamRight.length + 0.5 * self.plateLeft.T + self.bbWeldWeb_L3.b,
                                        (self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])
            plateL_uDir = numpy.array([0.0, 1.0, 0.0])  # TODO: self.boltProjection
            plateL_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

        else:
            plateOriginL = numpy.array([-self.plateLeft.W / 2, self.beamRight.length + 0.5 * self.plateLeft.T + self.bbWeldWeb_L3.b, 0.0])
            plateL_uDir = numpy.array([0.0, 1.0, 0.0])
            plateL_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateLeft.place(plateOriginL, plateL_uDir, plateL_wDir)

    def createPlateRGeometry(self):

        if self.alist["Member"]["Connectivity"] == "Extended one way":
            gap = 1.5 * self.plateRight.T + self.beamLeft.length + self.bbWeldWeb_L3.b
            plateOriginR = numpy.array(
                [-self.plateRight.W / 2, gap, (self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:
            gap = 1.5 * self.plateRight.T + self.beamLeft.length + self.bbWeldWeb_L3.b
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, 0.0])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        nutboltArrayOrigin = self.plateLeft.sec_origin + numpy.array([0.0, -0.5 * self.plateLeft.T, self.plateLeft.L / 2])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, 0, -1.0])
        boltDir = numpy.array([0, 1.0, 0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def createbeam_stiffener_1Geometry(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_1.L / 2 + self. bbWeldWeb_L3.b
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                        self.beamRight.D / 2 + self.beam_stiffener_1.W / 2 ])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

    def createbeam_stiffener_2Geometry(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_1.L / 2 + self. bbWeldWeb_L3.b
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                        - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2 ])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    def createbeam_stiffener_3Geometry(self):
        gap = self.beamLeft.length - self.beam_stiffener_1.L / 2 + self. bbWeldWeb_L3.b
        stiffenerOrigin3 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                        self.beamRight.D / 2 + self.beam_stiffener_1.W / 2 ])
        stiffener3_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener3_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_3.place(stiffenerOrigin3, stiffener3_uDir, stiffener3_wDir)

    def createbeam_stiffener_4Geometry(self):
        gap = self.beamLeft.length - self.beam_stiffener_1.L / 2 + self. bbWeldWeb_L3.b
        stiffenerOrigin4 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                        - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2 ])
        stiffener4_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener4_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_4.place(stiffenerOrigin4, stiffener4_uDir, stiffener4_wDir)


    def createbeam_stiffener_F1Geometry(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L / 2 + self.bbWeldWeb_L3.b
        stiffenerOriginF1 = numpy.array([-self.beam_stiffener_F1.W/2 - self.beamLeft.t/2, gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffenerF1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF1_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F1.place(stiffenerOriginF1, stiffenerF1_uDir, stiffenerF1_wDir)

    def createbeam_stiffener_F2Geometry(self):
        gap = self.beamLeft.length - self.beam_stiffener_F2.L / 2 + self.bbWeldWeb_L3.b
        stiffenerOriginF2 = numpy.array([self.beam_stiffener_F2.W/2 + self.beamLeft.t/2 , gap,
                                         self.beamRight.D / 2 -self.beam_stiffener_2.T - self.loc])
        stiffenerF2_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF2_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F2.place(stiffenerOriginF2, stiffenerF2_uDir, stiffenerF2_wDir)


    def createbeam_stiffener_F3Geometry(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L / 2 +  self.bbWeldWeb_L3.b
        stiffenerOriginF3 = numpy.array([-(self.beam_stiffener_F3.W/2 + self.beamRight.t/2), gap,
                                         self.beamRight.D / 2 -self.beam_stiffener_F3.T- self.loc])
        stiffenerF3_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffenerF3_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F3.place(stiffenerOriginF3, stiffenerF3_uDir, stiffenerF3_wDir)

    def createbeam_stiffener_F4Geometry(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F4.L / 2 +  self.bbWeldWeb_L3.b
        stiffenerOriginF4 = numpy.array([(self.beam_stiffener_F4.W/2 + self.beamRight.t/2), gap,
                                         self.beamRight.D / 2 - self.loc])
        stiffenerF4_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffenerF4_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F4.place(stiffenerOriginF4, stiffenerF4_uDir, stiffenerF4_wDir)

    ##############################################  creating weld sections ########################################

    def create_bbWeldFlang_R1(self):
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T  + self.bbWeldWeb_L3.b/2
        weldFlangOrigin_R1 = numpy.array([- self.beamLeft.B/2, gap, self.beamLeft.D/2 - self.beamLeft.T/2])
        uDir_1 = numpy.array([0, 1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bbWeldFlang_R1.place(weldFlangOrigin_R1, uDir_1, wDir_1)

    def create_bbWeldFlang_R2(self):
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T  + self.bbWeldWeb_L3.b / 2
        weldFlangOrigin_R2 = numpy.array([self.beamLeft.B/2, gap, -(self.beamLeft.D/2 - self.beamLeft.T/2)])
        uDir_2 = numpy.array([0, 1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bbWeldFlang_R2.place(weldFlangOrigin_R2, uDir_2, wDir_2)

    def create_bbWeldFlang_L1(self):
        weldFlangOrigin_L1 = numpy.array([ - self.beamLeft.B/2 , self.beamLeft.length + self.bbWeldWeb_L3.b/2, self.beamLeft.D/2 - self.beamLeft.T/2])
        uDir_1 = numpy.array([0, 1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bbWeldFlang_L1.place(weldFlangOrigin_L1, uDir_1, wDir_1)

    def create_bbWeldFlang_L2(self):
        weldFlangOrigin_L2 = numpy.array([self.beamLeft.B/2, self.beamLeft.length + self.bbWeldWeb_L3.b/2,-(self.beamLeft.D/2 - self.beamLeft.T/2)])
        uDir_2 = numpy.array([0, 1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bbWeldFlang_L2.place(weldFlangOrigin_L2, uDir_2, wDir_2)

    def create_bbWeldWeb_R3(self):
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T  + self.bbWeldWeb_L3.b / 2
        weldWebOrigin_R3 = numpy.array([0.0, gap,-self.bbWeldWeb_L3.L/2])
        uDirWeb_3 = numpy.array([0, 1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bbWeldWeb_R3.place(weldWebOrigin_R3, uDirWeb_3, wDirWeb_3)

    def create_bbWeldWeb_L3(self):
        weldWebOrigin_L3 = numpy.array([0.0, self.beamLeft.length + self.bbWeldWeb_L3.b/2, -self.bbWeldWeb_L3.L/2])
        uDirWeb_3 = numpy.array([0, 1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bbWeldWeb_L3.place(weldWebOrigin_L3, uDirWeb_3, wDirWeb_3)

    #Groove weld
    # def create_bbWeldStiffH_1(self):
    #     weldstiffOriginH_1 = numpy.array([0.0, self.beamLeft.length + self.bbWeldWeb_L3.b/2, self.beamLeft.D/2 + self.bbWeldWeb_L3.b + self.beam_stiffener_1.L21])
    #     uDirstiffH_1 = numpy.array([0, 1.0, 0])
    #     wDirstiffH_1 = numpy.array([0, 0, 1.0])
    #     self.bbWeldStiffH_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)
    #
    # def create_bbWeldStiffL_1(self):
    #     weldstiffOriginL_1 = numpy.array([0.0, self.beamLeft.length -self.beam_stiffener_1.L22, self.beamLeft.D/2 + self.bbWeldWeb_L3.b/2])
    #     uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
    #     wDirstiffL_1 = numpy.array([0.0, -1.0, 0.0])
    #     self.bbWeldStiffL_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)
    #
    #
    # def create_bbWeldStiffH_3(self):
    #     gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b / 2
    #     weldstiffOriginH_3 = numpy.array([0.0, gap, self.beamLeft.D/2+ self.bbWeldWeb_L3.b + self.beam_stiffener_3.L21])
    #     uDirstiffH_3 = numpy.array([0, 1.0, 0])
    #     wDirstiffH_3 = numpy.array([0, 0, 1.0])
    #     self.bbWeldStiffH_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)
    #
    # def create_bbWeldStiffL_3(self):
    #     gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b+ self.beam_stiffener_4.L22
    #     weldstiffOriginL_3 = numpy.array([0.0, gap, self.beamLeft.D/2 + self.bbWeldWeb_L3.b/2])
    #     uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
    #     wDirstiffL_3 = numpy.array([0.0, 1.0,0.0])
    #     self.bbWeldStiffL_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)
    #
    #
    # def create_bbWeldStiffH_2(self):
    #     weldstiffOriginH_2 = numpy.array([0.0, self.beamLeft.length + self.bbWeldWeb_L3.b/2, -(self.beamLeft.D/2 + self.beam_stiffener_3.W + self.bbWeldWeb_L3.b )])
    #     uDirstiffH_2 = numpy.array([0, 1.0, 0])
    #     wDirstiffH_2 = numpy.array([0, 0, 1.0])
    #     self.bbWeldStiffH_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)
    #
    #
    # def create_bbWeldStiffL_2(self):
    #     weldstiffOriginL_2 = numpy.array([0.0, self.beamLeft.length -self.beam_stiffener_1.L22, -(self.beamLeft.D/2 + self.bbWeldWeb_L3.b/2)])
    #     uDirstiffL_2 = numpy.array([0, 0.0, 1.0])
    #     wDirstiffL_2 = numpy.array([0, -1.0, 0.0])
    #     self.bbWeldStiffL_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)
    #
    # def create_bbWeldStiffH_4(self):
    #     gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b / 2
    #     weldstiffOriginH_4 = numpy.array([0.0, gap, -(self.beamLeft.D/2 + self.beam_stiffener_4.W + self.bbWeldWeb_L3.b)])
    #     uDirstiffH_4 = numpy.array([0, 1.0, 0])
    #     wDirstiffH_4 = numpy.array([0, 0, 1.0])
    #     self.bbWeldStiffH_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)
    #
    # def create_bbWeldStiffL_4(self):
    #     gap = self.beamLeft.length + self.bbWeldWeb_L3.b + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b + self.beam_stiffener_4.L22
    #     weldstiffOriginL_4 = numpy.array([0.0, gap, -(self.beamLeft.D/2 + self.bbWeldWeb_L3.b/2)])
    #     uDirstiffL_4 = numpy.array([0, 0.0, 1.0])
    #     wDirstiffL_4 = numpy.array([0, 1.0, 0.0])
    #     self.bbWeldStiffL_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)


    ################################################# Welding Beam Stiffeners ###################################################


    def create_bbWeldStiffHL_1(self):
        weldstiffOriginH_1 = numpy.array([-self.beam_stiffener_1.T/2, self.beamLeft.length + self.bbWeldWeb_L3.b, self.beamLeft.D/2 + self.beam_stiffener_1.W ])
        uDirstiffH_1 = numpy.array([0, -1.0, 0])
        wDirstiffH_1 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHL_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)


    def create_bbWeldStiffLL_1(self):
        weldstiffOriginL_1 = numpy.array([-self.beam_stiffener_1.T/2, self.beamLeft.length - self.beam_stiffener_1.L22+ self.bbWeldWeb_L3.b, self.beamLeft.D/2])
        uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldStiffLL_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)


    def create_bbWeldStiffHL_3(self):
        gap = self.beamLeft.length  + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        weldstiffOriginH_3 = numpy.array([self.beam_stiffener_3.T/2, gap, self.beamLeft.D/2 + self.beam_stiffener_3.W])
        uDirstiffH_3 = numpy.array([0, 1.0, 0])
        wDirstiffH_3 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHL_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)

    def create_bbWeldStiffLL_3(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22 + self.bbWeldStiffLL_3.L+ self.bbWeldWeb_L3.b
        weldstiffOriginL_3 = numpy.array([-self.beam_stiffener_3.T/2, gap, self.beamLeft.D/2])
        uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_3 = numpy.array([0.0, -1.0,0.0])
        self.bbWeldStiffLL_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)


    def create_bbWeldStiffHL_2(self):
        weldstiffOriginH_2 = numpy.array([self.beam_stiffener_2.T/2, self.beamLeft.length+ self.bbWeldWeb_L3.b, -(self.beamLeft.D/2 + self.beam_stiffener_3.W )])
        uDirstiffH_2 = numpy.array([0, -1.0, 0])
        wDirstiffH_2 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHL_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)


    def create_bbWeldStiffLL_2(self):
        weldstiffOriginL_2 = numpy.array([self.beamLeft.t/2 , self.beamLeft.length - self.beam_stiffener_1.L22+ self.bbWeldWeb_L3.b , -self.beamLeft.D/2 ])
        uDirstiffL_2 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_2 = numpy.array([0, -1.0, 0.0])
        self.bbWeldStiffLL_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)

    def create_bbWeldStiffHL_4(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        weldstiffOriginH_4 = numpy.array([-self.beam_stiffener_3.T/2, gap, -(self.beamLeft.D/2 + self.beam_stiffener_4.W)])
        uDirstiffH_4 = numpy.array([0, 1.0, 0])
        wDirstiffH_4 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHL_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)

    def create_bbWeldStiffLL_4(self):
        gap =  self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22 + self.bbWeldStiffLL_3.L+ self.bbWeldWeb_L3.b
        weldstiffOriginL_4 = numpy.array([self.beamLeft.t/2, gap, -self.beamLeft.D/2 ])
        uDirstiffL_4 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_4 = numpy.array([0, -1.0, 0.0])
        self.bbWeldStiffLL_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)

    def create_bbWeldStiffHR_1(self):
        weldstiffOriginH_1 = numpy.array([self.beam_stiffener_1.T/2, self.beamLeft.length+ self.bbWeldWeb_L3.b, self.beamLeft.D/2 + self.beam_stiffener_1.L21])
        uDirstiffH_1 = numpy.array([0, -1.0, 0])
        wDirstiffH_1 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHR_1.place(weldstiffOriginH_1, uDirstiffH_1, wDirstiffH_1)

    def create_bbWeldStiffLR_1(self):
        weldstiffOriginL_1 = numpy.array([self.beamLeft.t/2, self.beamLeft.length - self.beam_stiffener_2.L + self.bbWeldWeb_L3.b, self.beamLeft.D/2 ])
        uDirstiffL_1 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldStiffLR_1.place(weldstiffOriginL_1, uDirstiffL_1, wDirstiffL_1)


    def create_bbWeldStiffHR_3(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        weldstiffOriginH_3 = numpy.array([-self.beam_stiffener_3.T/2, gap, self.beamLeft.D/2 + self.beam_stiffener_3.L21 ])
        uDirstiffH_3 = numpy.array([0, 1.0, 0])
        wDirstiffH_3 = numpy.array([0, 0, 1.0])
        self.bbWeldStiffHR_3.place(weldstiffOriginH_3, uDirstiffH_3, wDirstiffH_3)

    def create_bbWeldStiffLR_3(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22+ self.bbWeldWeb_L3.b
        weldstiffOriginL_3 = numpy.array([self.beamLeft.t/2, gap , self.beamLeft.D/2 ])
        uDirstiffL_3 = numpy.array([0.0, 0.0, 1.0])
        wDirstiffL_3 = numpy.array([0.0, 1.0,0.0])
        self.bbWeldStiffLR_3.place(weldstiffOriginL_3, uDirstiffL_3, wDirstiffL_3)


    def create_bbWeldStiffHR_2(self):
        weldstiffOriginH_2 = numpy.array([-self.beam_stiffener_2.T/2, self.beamLeft.length+ self.bbWeldWeb_L3.b, -(self.beamLeft.D/2 + self.beam_stiffener_2.L21)])
        uDirstiffH_2 = numpy.array([0, -1.0, 0])
        wDirstiffH_2 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHR_2.place(weldstiffOriginH_2, uDirstiffH_2, wDirstiffH_2)


    def create_bbWeldStiffLR_2(self):
        weldstiffOriginL_2 = numpy.array([-self.beam_stiffener_2.T/2 , self.beamLeft.length - self.beam_stiffener_2.L+ self.bbWeldWeb_L3.b , -self.beamLeft.D/2])
        uDirstiffL_2 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_2 = numpy.array([0, 1.0, 0.0])
        self.bbWeldStiffLR_2.place(weldstiffOriginL_2, uDirstiffL_2, wDirstiffL_2)

    def create_bbWeldStiffHR_4(self):
        gap = self.beamLeft.length  + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        weldstiffOriginH_4 = numpy.array([self.beam_stiffener_4.T/2, gap, -(self.beamLeft.D/2 + self.beam_stiffener_4.L21)])
        uDirstiffH_4 = numpy.array([0, 1.0, 0])
        wDirstiffH_4 = numpy.array([0, 0, -1.0])
        self.bbWeldStiffHR_4.place(weldstiffOriginH_4, uDirstiffH_4, wDirstiffH_4)

    def create_bbWeldStiffLR_4(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_3.L22+ self.bbWeldWeb_L3.b
        weldstiffOriginL_4 = numpy.array([-self.beamLeft.t/2, gap , -self.beamLeft.D/2 ])
        uDirstiffL_4 = numpy.array([0, 0.0, -1.0])
        wDirstiffL_4 = numpy.array([0, 1.0, 0.0])
        self.bbWeldStiffLR_4.place(weldstiffOriginL_4, uDirstiffL_4, wDirstiffL_4)

    def create_bbWeldstiff1_u1(self):
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff1_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

    def create_bbWeldstiff1_u2(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff1_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

    def create_bbWeldstiff1_l1(self):
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff1_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bbWeldstiff1_l2(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L22 + self.bbWeldWeb_L3.b
        stiffenerOrigin1_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff1_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

    def create_bbWeldstiff2_u1(self):
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u1 = numpy.array([(self.beam_stiffener_F1.W + self.beamLeft.t / 2), gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff2_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

    def create_bbWeldstiff2_u2(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff2_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

    def create_bbWeldstiff2_l1(self):
        gap = self.beamLeft.length + self.bbWeldWeb_L3.b
        stiffenerOrigin1_l1 = numpy.array([(self.beam_stiffener_F1.L22 + self.beamLeft.t / 2), gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff2_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bbWeldstiff2_l2(self):
        gap = self.beamLeft.length - self.beam_stiffener_F1.L22 + self.bbWeldWeb_L3.b
        stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t/2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff2_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

    def create_bbWeldstiff3_u1(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff3_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

    def create_bbWeldstiff3_u2(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_u2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff3_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

    def create_bbWeldstiff3_l1(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff3_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bbWeldstiff3_l2(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L+ self.bbWeldWeb_L3.b
        stiffenerOrigin3_l2 = numpy.array([-self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener3_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener3_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff3_l2.place(stiffenerOrigin3_l2, stiffener3_l2_uDir, stiffener3_l2_wDir)

    def create_bbWeldstiff4_u1(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_u1 = numpy.array([self.beam_stiffener_F1.L22 + self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bbWeldstiff4_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

    def create_bbWeldstiff4_u2(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bbWeldstiff4_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

    def create_bbWeldstiff4_l1(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_l1 = numpy.array([self.beam_stiffener_F1.W + self.beamLeft.t / 2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bbWeldstiff4_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bbWeldstiff4_l2(self):
        gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L+ self.bbWeldWeb_L3.b
        stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t/2, gap,
                                           self.beamRight.D / 2 - self.loc - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bbWeldstiff4_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

        #############################################################################################################
        #   Following functions returns the CAD model to the function display_3DModel of main file                  #
        #############################################################################################################
        # def get_beam_models(self):
        #     '''
        #
        #     Returns: Returns model of beam (left and right)
        #
        #     '''
        #     return [self.beamRModel, self.beamLModel]
        #
        # def get_connector_models(self):
        #     '''
        #
        #     Returns: Returns model related to connector (plates and weld)
        #
        #     '''
        #     return [self.plateRModel, self.plateLModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model, self.beam_stiffener_3Model,
        #             self.beam_stiffener_4Model, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
        #             self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model,
        #             self.bbWeldBelwFlang_13Model, self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model, self.bbWeldBelwFlang_22Model,
        #             self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model, self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model,
        #             self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model] + self.nut_bolt_array.get_models()
        #
        # def get_models(self):
        #     '''
        #
        #     Returns: Returns model related to complete model (beams, plates and weld)
        #
        #     '''
        #     return [self.beamRModel, self.beamLModel, self.plateRModel, self.plateLModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
        #             self.beam_stiffener_3Model, self.beam_stiffener_4Model, self.bbWeldAbvFlang_11Model, self.bbWeldAbvFlang_12Model,
        #             self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_11Model, self.bbWeldBelwFlang_12Model,
        #             self.bbWeldBelwFlang_13Model, self.bbWeldBelwFlang_14Model, self.bbWeldBelwFlang_21Model, self.bbWeldBelwFlang_22Model,
        #             self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model, self.bbWeldSideWeb_11Model, self.bbWeldSideWeb_12Model,
        #             self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model] + self.nut_bolt_array.get_models()

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

    def get_beam_stiffener_1Model(self):
        return self.beam_stiffener_1Model

    def get_beam_stiffener_2Model(self):
        return self.beam_stiffener_2Model

    def get_beam_stiffener_3Model(self):
        return self.beam_stiffener_3Model

    def get_beam_stiffener_4Model(self):
        return self.beam_stiffener_4Model

    def get_beam_stiffener_F1Model(self):
        return self.beam_stiffener_F1Model

    def get_beam_stiffener_F2Model(self):
        return self.beam_stiffener_F2Model

    def get_beam_stiffener_F3Model(self):
        return self.beam_stiffener_F3Model

    def get_beam_stiffener_F4Model(self):
        return self.beam_stiffener_F4Model

    def get_bbWeldFlang_R1Model(self):
        return self.bbWeldFlang_R1Model

    def get_bbWeldFlang_R2Model(self):
        return self.bbWeldFlang_R2Model

    def get_bbWeldFlang_L1Model(self):
        return self.bbWeldFlang_L1Model

    def get_bbWeldFlang_L2Model(self):
        return self.bbWeldFlang_L2Model

    def get_bbWeldWeb_R3Model(self):
        return self.bbWeldWeb_R3Model

    def get_bbWeldWeb_L3Model(self):
        return self.bbWeldWeb_L3Model

    # def get_bbWeldStiffH_1Model(self):
    #     return self.bbWeldStiffH_1Model
    #
    # def get_bbWeldStiffL_1Model(self):
    #     return self.bbWeldStiffL_1Model
    #
    # def get_bbWeldStiffH_3Model(self):
    #     return self.bbWeldStiffH_3Model
    #
    # def get_bbWeldStiffL_3Model(self):
    #     return self.bbWeldStiffL_3Model
    #
    # def get_bbWeldStiffH_2Model(self):
    #     return self.bbWeldStiffH_2Model
    #
    # def get_bbWeldStiffL_2Model(self):
    #     return self.bbWeldStiffL_2Model
    #
    # def get_bbWeldStiffH_4Model(self):
    #     return self.bbWeldStiffH_4Model
    #
    # def get_bbWeldStiffL_4Model(self):
    #     return self.bbWeldStiffL_4Model

    def get_bbWeldStiffHL_1Model(self):
        return self.bbWeldStiffHL_1Model

    def get_bbWeldStiffLL_1Model(self):
        return self.bbWeldStiffLL_1Model

    def get_bbWeldStiffHL_3Model(self):
        return self.bbWeldStiffHL_3Model

    def get_bbWeldStiffLL_3Model(self):
        return self.bbWeldStiffLL_3Model

    def get_bbWeldStiffHL_2Model(self):
        return self.bbWeldStiffHL_2Model

    def get_bbWeldStiffLL_2Model(self):
        return self.bbWeldStiffLL_2Model

    def get_bbWeldStiffHL_4Model(self):
        return self.bbWeldStiffHL_4Model

    def get_bbWeldStiffLL_4Model(self):
        return self.bbWeldStiffLL_4Model

    def get_bbWeldStiffHR_1Model(self):
        return self.bbWeldStiffHR_1Model

    def get_bbWeldStiffLR_1Model(self):
        return self.bbWeldStiffLR_1Model

    def get_bbWeldStiffHR_3Model(self):
        return self.bbWeldStiffHR_3Model

    def get_bbWeldStiffLR_3Model(self):
        return self.bbWeldStiffLR_3Model

    def get_bbWeldStiffHR_2Model(self):
        return self.bbWeldStiffHR_2Model

    def get_bbWeldStiffLR_2Model(self):
        return self.bbWeldStiffLR_2Model

    def get_bbWeldStiffHR_4Model(self):
        return self.bbWeldStiffHR_4Model

    def get_bbWeldStiffLR_4Model(self):
        return self.bbWeldStiffLR_4Model

    def get_bbWeldstiff1_u1Model(self):
        return self.bbWeldstiff1_u1Model

    def get_bbWeldstiff1_u2Model(self):
        return self.bbWeldstiff1_u2Model

    def get_bbWeldstiff1_l1Model(self):
        return self.bbWeldstiff1_l1Model

    def get_bbWeldstiff1_l2Model(self):
        return self.bbWeldstiff1_l2Model

    def get_bbWeldstiff2_u1Model(self):
        return self.bbWeldstiff2_u1Model

    def get_bbWeldstiff2_u2Model(self):
        return self.bbWeldstiff2_u2Model

    def get_bbWeldstiff2_l1Model(self):
        return self.bbWeldstiff2_l1Model

    def get_bbWeldstiff2_l2Model(self):
        return self.bbWeldstiff2_l2Model

    def get_bbWeldstiff3_u1Model(self):
        return self.bbWeldstiff3_u1Model

    def get_bbWeldstiff3_u2Model(self):
        return self.bbWeldstiff3_u2Model

    def get_bbWeldstiff3_l1Model(self):
        return self.bbWeldstiff3_l1Model

    def get_bbWeldstiff3_l2Model(self):
        return self.bbWeldstiff3_l2Model

    def get_bbWeldstiff4_u1Model(self):
        return self.bbWeldstiff4_u1Model

    def get_bbWeldstiff4_u2Model(self):
        return self.bbWeldstiff4_u2Model

    def get_bbWeldstiff4_l1Model(self):
        return self.bbWeldstiff4_l1Model

    def get_bbWeldstiff4_l2Model(self):
        return self.bbWeldstiff4_l2Model


    def get_models(self):
        '''Returning 3D models
        '''

        if self.alist["Member"]["Connectivity"] == "Extended one way":
            return [self.beamLModel, self.beamRModel, self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
                    self.beam_stiffener_3Model,  self.bbWeldStiffHL_1Model, self.bbWeldFlang_R1Model,
                    self.bbWeldFlang_R2Model, self.bbWeldFlang_L1Model,
                    self.bbWeldFlang_L2Model, self.bbWeldWeb_R3Model, self.bbWeldWeb_L3Model,
                    self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
                    self.bbWeldStiffHR_1Model,
                    self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
                    self.bbWeldStiffLR_3Model
                    ] + self.nut_bolt_array.get_models()
        elif self.alist["Member"]["Connectivity"] == "Extended both ways":
            return [self.beamLModel, self.beamRModel, self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
                    self.beam_stiffener_2Model, self.beam_stiffener_3Model,
                    self.beam_stiffener_4Model, self.bbWeldStiffHL_1Model, self.bbWeldFlang_R1Model,
                    self.bbWeldFlang_R2Model, self.bbWeldFlang_L1Model,
                    self.bbWeldFlang_L2Model, self.bbWeldWeb_R3Model, self.bbWeldWeb_L3Model,
                    self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model,
                    self.bbWeldStiffHL_2Model, self.bbWeldStiffLL_2Model,
                    self.bbWeldStiffHL_4Model, self.bbWeldStiffLL_4Model, self.bbWeldStiffHR_1Model,
                    self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
                    self.bbWeldStiffLR_3Model, self.bbWeldStiffHR_2Model, self.bbWeldStiffLR_2Model,
                    self.bbWeldStiffHR_4Model, self.bbWeldStiffLR_4Model,
                    ] + self.nut_bolt_array.get_models()
        elif self.alist["Member"]["Connectivity"] == "Flush":

            return [self.beamLModel, self.beamRModel, self.plateLModel, self.plateRModel, self.beam_stiffener_F1Model, self.beam_stiffener_F2Model,
                    self.beam_stiffener_F3Model,
                    self.beam_stiffener_F4Model, self.bbWeldFlang_R1Model,
                    self.bbWeldFlang_R2Model, self.bbWeldFlang_L1Model,
                    self.bbWeldFlang_L2Model, self.bbWeldWeb_R3Model, self.bbWeldWeb_L3Model,
                    self.bbWeldstiff1_u1Model, self.bbWeldstiff1_u2Model, self.bbWeldstiff1_l1Model,
                    self.bbWeldstiff1_l2Model, self.bbWeldstiff2_u1Model,
                    self.bbWeldstiff2_u2Model, self.bbWeldstiff2_l1Model, self.bbWeldstiff2_l2Model,
                    self.bbWeldstiff3_u1Model, self.bbWeldstiff3_u2Model,
                    self.bbWeldstiff3_l1Model, self.bbWeldstiff3_l2Model, self.bbWeldstiff4_u1Model,
                    self.bbWeldstiff4_u2Model, self.bbWeldstiff4_l1Model,
                    self.bbWeldstiff4_l2Model] + self.nut_bolt_array.get_models()


     #    return [self.beamLModel, self.beamRModel, self.plateLModel, self.plateRModel, self.beam_stiffener_1Model,
     # self.beam_stiffener_2Model, self.beam_stiffener_3Model,
     # self.beam_stiffener_4Model, self.beam_stiffener_F1Model, self.beam_stiffener_F2Model, self.beam_stiffener_F3Model,
     # self.beam_stiffener_F4Model, self.bbWeldStiffHL_1Model, self.bbWeldFlang_R1Model, self.bbWeldFlang_R2Model, self.bbWeldFlang_L1Model,
     #            self.bbWeldFlang_L2Model, self.bbWeldWeb_R3Model, self.bbWeldWeb_L3Model,
     # self.bbWeldStiffLL_1Model, self.bbWeldStiffHL_3Model, self.bbWeldStiffLL_3Model, self.bbWeldStiffHL_2Model, self.bbWeldStiffLL_2Model,
     # self.bbWeldStiffHL_4Model, self.bbWeldStiffLL_4Model, self.bbWeldStiffHR_1Model, self.bbWeldStiffLR_1Model, self.bbWeldStiffHR_3Model,
     # self.bbWeldStiffLR_3Model, self.bbWeldStiffHR_2Model, self.bbWeldStiffLR_2Model, self.bbWeldStiffHR_4Model, self.bbWeldStiffLR_4Model,
     # self.bbWeldstiff1_u1Model, self.bbWeldstiff1_u2Model, self.bbWeldstiff1_l1Model, self.bbWeldstiff1_l2Model, self.bbWeldstiff2_u1Model,
     # self.bbWeldstiff2_u2Model, self.bbWeldstiff2_l1Model, self.bbWeldstiff2_l2Model, self.bbWeldstiff3_u1Model, self.bbWeldstiff3_u2Model,
     # self.bbWeldstiff3_l1Model, self.bbWeldstiff3_l2Model, self.bbWeldstiff4_u1Model, self.bbWeldstiff4_u2Model, self.bbWeldstiff4_l1Model,
     # self.bbWeldstiff4_l2Model,] + self.nut_bolt_array.get_models()
