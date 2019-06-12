"""
Initialized on 23-04-2019
Commenced on 24-04-2019
@author: Anand Swaroop
"""""

import numpy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut

class CADFillet(object):
    def __init__(self, beamLeft, beamRight, plateRight, nut_bolt_array,bolt, bbWeldAbvFlang_21, bbWeldAbvFlang_22,
                 bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23, bbWeldBelwFlang_24, bbWeldSideWeb_21,
                 bbWeldSideWeb_22,contWeldL1_U2 ,contWeldL2_U2,contWeldL1_L2 ,contWeldL2_L2,
                 contWeldR1_U2, contWeldR2_U2, contWeldR1_L2, contWeldR2_L2,contWeldL1_U3,contWeldL1_L3,contWeldL2_U3,contWeldL2_L3,
                 contWeldR1_U3, contWeldR1_L3, contWeldR2_U3,
                 contWeldR2_L3,contWeldL1_U1,contWeldL1_L1,contWeldL2_U1,contWeldL2_L1,
                 contWeldR1_U1, contWeldR1_L1, contWeldR2_U1,
                 contWeldR2_L1, bcWeldStiffHL_1,bcWeldStiffHL_2,bcWeldStiffHR_1,bcWeldStiffHR_2,
                 bcWeldStiffLL_1,bcWeldStiffLL_2, bcWeldStiffLR_1, bcWeldStiffLR_2,
                 contPlate_L1, contPlate_L2, contPlate_R1, contPlate_R2,beam_stiffener_1,beam_stiffener_2, endplate_type, conn_type, outputobj):

        # Initializing the arguments
        self.beamLeft = beamLeft  # beamLeft represents the column
        self.beamRight = beamRight
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.bolt = bolt
        # self.beamRight.length = 100.0
        self.contPlate_L1 = contPlate_L1
        self.contPlate_L2 = contPlate_L2
        self.contPlate_R1 = contPlate_R1
        self.contPlate_R2 = contPlate_R2
        self.beam_stiffener_1 = beam_stiffener_1
        self.beam_stiffener_2 = beam_stiffener_2

        self.endplate_type = endplate_type
        self.conn_type = conn_type                  #TODO: Remove this type if not needed
        self.outputobj = outputobj
        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection
        # self.Lv = float(outputobj["Bolt"]["Lv"])

        # Weld above flange for left and right beam
        self.bbWeldAbvFlang_21 = bbWeldAbvFlang_21  # Right beam upper side
        self.bbWeldAbvFlang_22 = bbWeldAbvFlang_22  # Right beam lower side

        self.bbWeldBelwFlang_21 = bbWeldBelwFlang_21  # behind bbWeldBelwFlang_11
        self.bbWeldBelwFlang_22 = bbWeldBelwFlang_22  # behind bbWeldBelwFlang_12
        self.bbWeldBelwFlang_23 = bbWeldBelwFlang_23  # behind bbWeldBelwFlang_13
        self.bbWeldBelwFlang_24 = bbWeldBelwFlang_24  # behind bbWeldBelwFlang_14

        self.bbWeldSideWeb_21 = bbWeldSideWeb_21  # Behind bbWeldSideWeb_11
        self.bbWeldSideWeb_22 = bbWeldSideWeb_22  # Behind bbWeldSideWeb_12

        self.contWeldL1_U2 = contWeldL1_U2
        self.contWeldL2_U2 = contWeldL2_U2
        self.contWeldL1_L2 = contWeldL1_L2
        self.contWeldL2_L2 = contWeldL2_L2
        self.contWeldR1_U2 = contWeldR1_U2
        self.contWeldR2_U2 = contWeldR2_U2
        self.contWeldR1_L2 = contWeldR1_L2
        self.contWeldR2_L2 = contWeldR2_L2
        self.contWeldL1_U3 = contWeldL1_U3
        self.contWeldL1_L3 = contWeldL1_L3
        self.contWeldL2_U3 = contWeldL2_U3
        self.contWeldL2_L3 = contWeldL2_L3
        self.contWeldR1_U3 = contWeldR1_U3
        self.contWeldR1_L3 = contWeldR1_L3
        self.contWeldR2_U3 = contWeldR2_U3
        self.contWeldR2_L3 = contWeldR2_L3
        self.contWeldL1_U1 = contWeldL1_U1
        self.contWeldL1_L1 = contWeldL1_L1
        self.contWeldL2_U1 = contWeldL2_U1
        self.contWeldL2_L1 = contWeldL2_L1
        self.contWeldR1_U1 = contWeldR1_U1
        self.contWeldR1_L1 = contWeldR1_L1
        self.contWeldR2_U1 = contWeldR2_U1
        self.contWeldR2_L1 = contWeldR2_L1

        self.bcWeldStiffHL_1 = bcWeldStiffHL_1
        self.bcWeldStiffHL_2 = bcWeldStiffHL_2
        self.bcWeldStiffHR_1 = bcWeldStiffHR_1
        self.bcWeldStiffHR_2 = bcWeldStiffHR_2

        self.bcWeldStiffLL_1 = bcWeldStiffLL_1
        self.bcWeldStiffLL_2 = bcWeldStiffLL_2
        self.bcWeldStiffLR_1 = bcWeldStiffLR_1
        self.bcWeldStiffLR_2 = bcWeldStiffLR_2

    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.create_contPlate_L1Geometry()
        self.create_contPlate_L2Geometry()
        self.create_contPlate_R1Geometry()
        self.create_contPlate_R2Geometry()
        self.create_beam_stiffener_1Geometry()
        self.create_beam_stiffener_2Geometry()

        self.create_bbWeldAbvFlang_21()  # left beam above flange weld
        self.create_bbWeldAbvFlang_22()  # left beam above 2nd (lower) flange

        self.create_bbWeldBelwFlang_21()  # right beam weld similar to left beam
        self.create_bbWeldBelwFlang_22()
        self.create_bbWeldBelwFlang_23()
        self.create_bbWeldBelwFlang_24()

        self.create_bbWeldSideWeb_21()  # right beam weld behind left beam
        self.create_bbWeldSideWeb_22()  # right beam weld behind left beam

        self.create_contWeldL1_U2()
        self.create_contWeldL2_U2()
        self.create_contWeldL1_L2()
        self.create_contWeldL2_L2()
        self.create_contWeldR1_U2()
        self.create_contWeldR2_U2()
        self.create_contWeldR1_L2()
        self.create_contWeldR2_L2()
        self.create_contWeldL1_U3()
        self.create_contWeldL1_L3()
        self.create_contWeldL2_U3()
        self.create_contWeldL2_L3()
        self.create_contWeldR1_U3()
        self.create_contWeldR1_L3()
        self.create_contWeldR2_U3()
        self.create_contWeldR2_L3()
        self.create_contWeldL1_U1()
        self.create_contWeldL1_L1()
        self.create_contWeldL2_U1()
        self.create_contWeldL2_L1()
        self.create_contWeldR1_U1()
        self.create_contWeldR1_L1()
        self.create_contWeldR2_U1()
        self.create_contWeldR2_L1()

        self.create_bcWeldStiffHL_1()
        self.create_bcWeldStiffHL_2()
        self.create_bcWeldStiffHR_1()
        self.create_bcWeldStiffHR_2()

        self.create_bcWeldStiffLL_1()
        self.create_bcWeldStiffLL_2()
        self.create_bcWeldStiffLR_1()
        self.create_bcWeldStiffLR_2()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        self.contPlate_L1Model = self.contPlate_L1.create_model()
        self.contPlate_L2Model = self.contPlate_L2.create_model()
        self.contPlate_R1Model = self.contPlate_R1.create_model()
        self.contPlate_R2Model = self.contPlate_R2.create_model()
        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()

        self.bbWeldAbvFlang_21Model = self.bbWeldAbvFlang_21.create_model()
        self.bbWeldAbvFlang_22Model = self.bbWeldAbvFlang_22.create_model()

        self.bbWeldBelwFlang_21Model = self.bbWeldBelwFlang_21.create_model()
        self.bbWeldBelwFlang_22Model = self.bbWeldBelwFlang_22.create_model()
        self.bbWeldBelwFlang_23Model = self.bbWeldBelwFlang_23.create_model()
        self.bbWeldBelwFlang_24Model = self.bbWeldBelwFlang_24.create_model()

        self.bbWeldSideWeb_21Model = self.bbWeldSideWeb_21.create_model()
        self.bbWeldSideWeb_22Model = self.bbWeldSideWeb_22.create_model()

        self.contWeldL1_U2Model = self.contWeldL1_U2.create_model()
        self.contWeldL2_U2Model = self.contWeldL2_U2.create_model()
        self.contWeldL1_L2Model = self.contWeldL1_L2.create_model()
        self.contWeldL2_L2Model = self.contWeldL2_L2.create_model()
        self.contWeldR1_U2Model = self.contWeldR1_U2.create_model()
        self.contWeldR2_U2Model = self.contWeldR2_U2.create_model()
        self.contWeldR1_L2Model = self.contWeldR1_L2.create_model()
        self.contWeldR2_L2Model = self.contWeldR2_L2.create_model()
        self.contWeldL1_U3Model = self.contWeldL1_U3.create_model()
        self.contWeldL1_L3Model = self.contWeldL1_L3.create_model()
        self.contWeldL2_U3Model = self.contWeldL2_U3.create_model()
        self.contWeldL2_L3Model = self.contWeldL2_L3.create_model()
        self.contWeldR1_U3Model = self.contWeldR1_U3.create_model()
        self.contWeldR1_L3Model = self.contWeldR1_L3.create_model()
        self.contWeldR2_U3Model = self.contWeldR2_U3.create_model()
        self.contWeldR2_L3Model = self.contWeldR2_L3.create_model()
        self.contWeldL1_U1Model = self.contWeldL1_U1.create_model()
        self.contWeldL1_L1Model = self.contWeldL1_L1.create_model()
        self.contWeldL2_U1Model = self.contWeldL2_U1.create_model()
        self.contWeldL2_L1Model = self.contWeldL2_L1.create_model()
        self.contWeldR1_U1Model = self.contWeldR1_U1.create_model()
        self.contWeldR1_L1Model = self.contWeldR1_L1.create_model()
        self.contWeldR2_U1Model = self.contWeldR2_U1.create_model()
        self.contWeldR2_L1Model = self.contWeldR2_L1.create_model()

        self.bcWeldStiffHL_1Model = self.bcWeldStiffHL_1.create_model()
        self.bcWeldStiffHL_2Model = self.bcWeldStiffHL_2.create_model()
        self.bcWeldStiffHR_1Model = self.bcWeldStiffHR_1.create_model()
        self.bcWeldStiffHR_2Model = self.bcWeldStiffHR_2.create_model()

        self.bcWeldStiffLL_1Model = self.bcWeldStiffLL_1.create_model()
        self.bcWeldStiffLL_2Model = self.bcWeldStiffLL_2.create_model()
        self.bcWeldStiffLR_1Model = self.bcWeldStiffLR_1.create_model()
        self.bcWeldStiffLR_2Model = self.bcWeldStiffLR_2.create_model()


    #############################################################################################################
    #   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
    #   same component at appropriate place                                                                     #
    #############################################################################################################

    def createBeamLGeometry(self):
        # if self.conn_type == 'col_flange_connectivity':
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

        # else: #self.conn_type ==  'col_web_connectivity'
        #     beamOriginL = numpy.array([0.0, self.beamLeft.D/2, 0.0])
        #     beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        #     beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        #     self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T
        beamOriginR = numpy.array([0.0, gap, self.beamLeft.length / 2])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plateRight.T + self.beamLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.beamLeft.length / 2 + (
                        self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:  # self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plateRight.T + self.beamLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.beamLeft.length / 2])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        # elif self.endplate_type == "flush":
        #     pass

    def create_nut_bolt_array(self):

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.plateRight.T/2 , + (self.plateRight.L / 2)])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.plateRight.T/2, self.plateRight.L / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.plateRight.T/2, self.beamRight.D/2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlate_L1Geometry(self):
        beamOriginL = numpy.array([self.beamLeft.B / 2 - self.contPlate_L1.W / 2, 0.0,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_L2Geometry(self):
        beamOriginL = numpy.array([self.beamLeft.B / 2 - self.contPlate_L2.W / 2, 0.0,
                                   self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_R1Geometry(self):
        beamOriginL = numpy.array([-self.beamLeft.B / 2 + self.contPlate_R1.W / 2, 0.0,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_R1.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_R2Geometry(self):
        beamOriginL = numpy.array([-self.beamLeft.B / 2 + self.contPlate_R2.W / 2, 0.0,
                                   self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_R1.T/2 ])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R2.place(beamOriginL, beamL_uDir, beamL_wDir)

    ##############################################  Adding beam stiffeners #############################################
    def create_beam_stiffener_1Geometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L/2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T/2, gap, self.beamLeft.length / 2 + self.beamRight.D/2 + self.beam_stiffener_1.W/2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

    def create_beam_stiffener_2Geometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L/2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T/2, gap, self.beamLeft.length / 2 - self.beamRight.D/2 - self.beam_stiffener_1.W/2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    ##############################################  creating weld sections ########################################
    def create_bbWeldAbvFlang_21(self):
        weldAbvFlangOrigin_21 = numpy.array([-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                             self.beamLeft.length / 2 + self.beamRight.D / 2])
        uDirAbv_21 = numpy.array([0, 1.0, 0])
        wDirAbv_21 = numpy.array([1.0, 0, 0])
        self.bbWeldAbvFlang_21.place(weldAbvFlangOrigin_21, uDirAbv_21, wDirAbv_21)

    def create_bbWeldAbvFlang_22(self):
        weldAbvFlangOrigin_22 = numpy.array([self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                             self.beamLeft.length / 2 - self.beamRight.D / 2])
        uDirAbv_22 = numpy.array([0, 1.0, 0])
        wDirAbv_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldAbvFlang_22.place(weldAbvFlangOrigin_22, uDirAbv_22, wDirAbv_22)

    def create_bbWeldBelwFlang_21(self):
        weldBelwFlangOrigin_21 = numpy.array([-self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) -
                                              self.beamRight.T])
        uDirBelw_21 = numpy.array([0, 1.0, 0])
        wDirBelw_21 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_21.place(weldBelwFlangOrigin_21, uDirBelw_21, wDirBelw_21)

    def create_bbWeldBelwFlang_22(self):
        weldBelwFlangOrigin_22 = numpy.array([self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) -
                                              self.beamRight.T])
        uDirBelw_22 = numpy.array([0, 1.0, 0])
        wDirBelw_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_22.place(weldBelwFlangOrigin_22, uDirBelw_22, wDirBelw_22)

    def create_bbWeldBelwFlang_23(self):
        weldBelwFlangOrigin_23 = numpy.array([-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) +
                                              self.beamRight.T])
        uDirBelw_23 = numpy.array([0, 1.0, 0])
        wDirBelw_23 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_23.place(weldBelwFlangOrigin_23, uDirBelw_23, wDirBelw_23)

    def create_bbWeldBelwFlang_24(self):
        weldBelwFlangOrigin_24 = numpy.array([self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) +
                                              self.beamRight.T])
        uDirBelw_24 = numpy.array([0, 1.0, 0])
        wDirBelw_24 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_24.place(weldBelwFlangOrigin_24, uDirBelw_24, wDirBelw_24)

    def create_bbWeldSideWeb_21(self):
        weldSideWebOrigin_21 = numpy.array([-self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 - self.bbWeldSideWeb_21.L / 2])
        uDirWeb_21 = numpy.array([0, 1.0, 0])
        wDirWeb_21 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_21.place(weldSideWebOrigin_21, uDirWeb_21, wDirWeb_21)

    def create_bbWeldSideWeb_22(self):
        weldSideWebOrigin_22 = numpy.array([self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 + self.bbWeldSideWeb_21.L / 2])
        uDirWeb_22 = numpy.array([0, 1.0, 0])
        wDirWeb_22 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_22.place(weldSideWebOrigin_22, uDirWeb_22, wDirWeb_22)

    def create_contWeldL1_U2(self):
        contWeldL1_U2OriginL = numpy.array([self.beamLeft.t/2, -self.contPlate_L1.L/2,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

    def create_contWeldL2_U2(self):
        contWeldL2_U2OriginL = numpy.array([self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T/2 ])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

    def create_contWeldL1_L2(self):
        contWeldL1_L2OriginL = numpy.array([self.beamLeft.t/2, -self.contPlate_L1.L/2,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        contWeldL1_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

    def create_contWeldL2_L2(self):
        contWeldL2_L2OriginL = numpy.array([self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2
                                            - self.beamRight.D / 2  -self.contPlate_L1.T/2+ self.beamRight.T / 2 ])
        contWeldL2_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

    def create_contWeldR1_U2(self):
        contWeldR1_U2OriginL = numpy.array([-self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2 ])
        contWeldR1_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_U2.place(contWeldR1_U2OriginL, contWeldR1_U2_uDir, contWeldR1_U2_wDir)

    def create_contWeldR2_U2(self):
        contWeldR2_U2OriginL = numpy.array([-self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2
                                            - self.beamRight.D/2 + self.beamRight.T / 2 + self.contPlate_L1.T/2 ])
        contWeldR2_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_U2.place(contWeldR2_U2OriginL, contWeldR2_U2_uDir, contWeldR2_U2_wDir)

    def create_contWeldR1_L2(self):
        contWeldR1_L2OriginL = numpy.array([-self.beamLeft.t/2, -self.contPlate_L1.L/2,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        contWeldR1_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_L2.place(contWeldR1_L2OriginL, contWeldR1_L2_uDir, contWeldR1_L2_wDir)

    def create_contWeldR2_L2(self):
        contWeldR2_L2OriginL = numpy.array([-self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2
                                            - self.beamRight.D / 2  + self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        contWeldR2_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_L2.place(contWeldR2_L2OriginL, contWeldR2_L2_uDir, contWeldR2_L2_wDir)

    def create_contWeldL1_U3(self):
        contWeldL1_U3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldL1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)
    def create_contWeldL1_L3(self):
        contWeldL1_L3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        uDircontWeldL1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)
    def create_contWeldR2_U3(self):
        contWeldR2_U3OriginL = numpy.array([ -self.beamLeft.B/ 2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2)+ self.beamRight.T / 2 + self.contPlate_L1.T/2])   #TODO: shuffel it with R2_U3
        uDircontWeldR2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U3.place(contWeldR2_U3OriginL, uDircontWeldR2_U3, wDircontWeldR2_U3)

    # def create_contWeldL2_L3(self):
    #     contWeldL2_L3OriginL = numpy.array([ -self.beamLeft.B/2, self.contPlate_L1.L/2 ,
    #                                           self.beamLeft.length / 2 + (self.beamRight.D / 2) -self.beamRight.D])
    #     uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
    #     wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
    #     self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

    def create_contWeldL2_L3(self):
        contWeldL2_L3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)


    def create_contWeldR1_U3(self):
        contWeldR1_U3OriginL = numpy.array([ -self.beamLeft.B/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldR1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U3.place(contWeldR1_U3OriginL, uDircontWeldR1_U3, wDircontWeldR1_U3)
    def create_contWeldR1_L3(self):
        contWeldR1_L3OriginL = numpy.array([ -self.beamLeft.B/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        uDircontWeldR1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L3.place(contWeldR1_L3OriginL, uDircontWeldR1_L3, wDircontWeldR1_L3)
    def create_contWeldL2_U3(self):
        contWeldL2_U3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)
    # def create_contWeldR2_L3(self):
    #     contWeldR2_L3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
    #                                           self.beamLeft.length / 2 + (self.beamRight.D / 2) -self.beamRight.D])
    #     uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
    #     wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
    #     self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)

    def create_contWeldR2_L3(self):
        contWeldR2_L3OriginL = numpy.array([ -self.beamLeft.B/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)
    def create_contWeldL1_U1(self):
        contWeldL1_U1OriginL = numpy.array([self.beamLeft.t/2 , -self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 + self.contPlate_L1.T/2 ])
        uDircontWeldL1_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)
    def create_contWeldL1_L1(self):
        contWeldL1_L1OriginL = numpy.array([ self.beamLeft.t/2,-self.contPlate_L1.L/2,
                                             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldL1_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldL1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)
    def create_contWeldL2_U1(self):
        contWeldL2_U1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                       self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T/2 ])
        uDircontWeldL2_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)
    def create_contWeldR2_L1(self):
        contWeldR2_L1OriginL = numpy.array([ -self.beamLeft.B / 2,-self.contPlate_L1.L/2,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldR2_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldR2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L1.place(contWeldR2_L1OriginL, uDircontWeldR2_L1, wDircontWeldR2_L1)
    def create_contWeldR1_U1(self):
        contWeldR1_U1OriginL = numpy.array([ - self.beamLeft.B/2, -self.contPlate_L1.L/2,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldR1_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U1.place(contWeldR1_U1OriginL, uDircontWeldR1_U1, wDircontWeldR1_U1)
    def create_contWeldR1_L1(self):
        contWeldR1_L1OriginL = numpy.array([ -self.beamLeft.B/2, -self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        uDircontWeldR1_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldR1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L1.place(contWeldR1_L1OriginL, uDircontWeldR1_L1, wDircontWeldR1_L1)
    def create_contWeldR2_U1(self):
        contWeldR2_U1OriginL = numpy.array([ -self.beamLeft.B/2, -self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldR2_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U1.place(contWeldR2_U1OriginL, uDircontWeldR2_U1, wDircontWeldR2_U1)
    def create_contWeldL2_L1(self):
        contWeldL2_L1OriginL = numpy.array([ self.beamLeft.t/2, -self.contPlate_L1.L/2,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldL2_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldL2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

    ############### Weld for the beam stiffeners ##################################
    def create_bcWeldStiffHL_1(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 + self.beamRight.D/2 + self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffHL_2(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 - self.beamRight.D/2 - self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffHR_1(self):
        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 + self.beamRight.D/2 + self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffHR_2(self):
        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 - self.beamRight.D/2 - self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffLL_1(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L,
                                            self.beamLeft.length / 2 + self.beamRight.D/2 ])
        uDirStiffHL_1 = numpy.array([1, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0, -1.0, 0.0])
        self.bcWeldStiffLL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffLL_2(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T+ self.beam_stiffener_1.L22,
                                            self.beamLeft.length / 2 - self.beamRight.D/2])
        uDirStiffHL_1 = numpy.array([1.0, 0.0, 0.0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffLR_1(self):
        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T+ self.beam_stiffener_1.L22,
                                            self.beamLeft.length / 2 + self.beamRight.D/2 ])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffLR_2(self):
        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T+ self.beam_stiffener_1.L,
                                            self.beamLeft.length / 2 - self.beamRight.D/2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bcWeldStiffLR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)




    #############################################################################################################
    #   Following functions returns the CAD model to the function display_3DModel of main file                  #
    #############################################################################################################
    def get_beamLModel(self):
        # return self.beamLModel
        final_column = self.beamLModel
        bolt_list = self.nut_bolt_array.get_bolt_list()
        for bolt in bolt_list[:]:
            final_column = BRepAlgoAPI_Cut(final_column, bolt).Shape()  # TODO: Anand #cuts the colum in section shape
        return final_column


    def get_beamRModel(self):
        return self.beamRModel

    def get_plateRModel(self):
        return self.plateRModel

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()

    def get_contPlate_L1Model(self):
        return self.contPlate_L1Model

    def get_contPlate_L2Model(self):
        return self.contPlate_L2Model

    def get_contPlate_R1Model(self):
        return self.contPlate_R1Model

    def get_contPlate_R2Model(self):
        return self.contPlate_R2Model

    def get_beam_stiffener_1Model(self):
        return  self.beam_stiffener_1Model

    def get_beam_stiffener_2Model(self):
        return self.beam_stiffener_2Model

    def get_bbWeldAbvFlang_21Model(self):
        return self.bbWeldAbvFlang_21Model

    def get_bbWeldAbvFlang_22Model(self):
        return self.bbWeldAbvFlang_22Model

    def get_bbWeldBelwFlang_21Model(self):
        return self.bbWeldBelwFlang_21Model

    def get_bbWeldBelwFlang_22Model(self):
        return self.bbWeldBelwFlang_22Model

    def get_bbWeldBelwFlang_23Model(self):
        return self.bbWeldBelwFlang_23Model

    def get_bbWeldBelwFlang_24Model(self):
        return self.bbWeldBelwFlang_24Model

    def get_bbWeldSideWeb_21Model(self):
        return self.bbWeldSideWeb_21Model

    def get_bbWeldSideWeb_22Model(self):
        return self.bbWeldSideWeb_22Model

    def get_contWeldL1_U2Model(self):
        return self.contWeldL1_U2Model
    def get_contWeldL2_U2Model(self):
        return self.contWeldL2_U2Model
    def get_contWeldL1_L2Model(self):
        return self.contWeldL1_L2Model
    def get_contWeldL2_L2Model(self):
        return self.contWeldL2_L2Model
    def get_contWeldR1_U2Model(self):
        return self.contWeldR1_U2Model
    def get_contWeldR2_U2Model(self):
        return self.contWeldR2_U2Model
    def get_contWeldR1_L2Model(self):
        return self.contWeldR1_L2Model
    def get_contWeldR2_L2Model(self):
        return self.contWeldR2_L2Model
    def get_contWeldL1_U3Model(self):
        return self.contWeldL1_U3Model
    def get_contWeldL1_L3Model(self):
        return self.contWeldL1_L3Model
    def get_contWeldL2_U3Model(self):
        return self.contWeldL2_U3Model
    def get_contWeldL2_L3Model(self):
        return self.contWeldL2_L3Model
    def get_contWeldR1_U3Model(self):
        return self.contWeldR1_U3Model
    def get_contWeldR1_L3Model(self):
        return self.contWeldR1_L3Model
    def get_contWeldR2_U3Model(self):
        return self.contWeldR2_U3Model
    def get_contWeldR2_L3Model(self):
        return self.contWeldR2_L3Model
    def get_contWeldL1_U1Model(self):
        return self.contWeldL1_U1Model
    def get_contWeldL1_L1Model(self):
        return self.contWeldL1_L1Model
    def get_contWeldL2_U1Model(self):
        return self.contWeldL2_U1Model
    def get_contWeldL2_L1Model(self):
        return self.contWeldL2_L1Model
    def get_contWeldR1_U1Model(self):
        return self.contWeldR1_U1Model
    def get_contWeldR1_L1Model(self):
        return self.contWeldR1_L1Model
    def get_contWeldR2_U1Model(self):
        return self.contWeldR2_U1Model
    def get_contWeldR2_L1Model(self):
        return self.contWeldR2_L1Model


    def get_bcWeldStiffHL_1Model(self):
        return self.bcWeldStiffHL_1Model

    def get_bcWeldStiffHL_2Model(self):
        return self.bcWeldStiffHL_2Model

    def get_bcWeldStiffHR_1Model(self):
        return self.bcWeldStiffHR_1Model

    def get_bcWeldStiffHR_2Model(self):
        return self.bcWeldStiffHR_2Model

    def get_bcWeldStiffLL_1Model(self):
        return self.bcWeldStiffLL_1Model

    def get_bcWeldStiffLL_2Model(self):
        return self.bcWeldStiffLL_2Model

    def get_bcWeldStiffLR_1Model(self):
        return self.bcWeldStiffLR_1Model

    def get_bcWeldStiffLR_2Model(self):
        return self.bcWeldStiffLR_2Model


    def get_models(self):
        '''Returning 3D models
        '''

        if self.endplate_type == "one_way":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model, ] + self.nut_bolt_array.get_models()        #self.beam_stiffener_1Model,
        elif self.endplate_type == "both_way":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model, ] + self.nut_bolt_array.get_models()        #self.beam_stiffener_1Model,self.beam_stiffener_2Model,

        elif self.endplate_type == "flush":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model, ] + self.nut_bolt_array.get_models()



class CADColWebFillet(CADFillet):

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, self.beamLeft.D/2 - self.beamLeft.t/2, 0.0])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)



        ##############################################  Adding contPlates ########################################

    def create_contPlate_L1Geometry(self):
        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D / 2 - self.beamLeft.t  - self.contPlate_L1.W / 2,
             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_L2Geometry(self):
        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D / 2 - self.beamLeft.t - self.contPlate_L2.W / 2,
             self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T/2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contWeldL1_U2(self):
        contWeldL1_U2OriginL = numpy.array([-self.contPlate_L1.L/2,  self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([1.0, 0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

    def create_contWeldL2_U2(self):
        contWeldL2_U2OriginL = numpy.array([-self.contPlate_L1.L/2, self.beamLeft.D/2-self.beamLeft.t, self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

    def create_contWeldL1_L2(self):
        contWeldL1_L2OriginL = numpy.array([-self.contPlate_L1.L / 2,  self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

    def create_contWeldL2_L2(self):
        contWeldL2_L2OriginL = numpy.array([-self.contPlate_L1.L / 2,  self.beamLeft.D/2-self.beamLeft.t, self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL2_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)



    def create_contWeldL1_U3(self):
        contWeldL1_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0.0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([0.0, -1, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

    def create_contWeldL1_L3(self):
        contWeldL1_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 + (
                                                        self.beamRight.D / 2)- self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([-1, 0, 0.0])
        wDircontWeldL1_L3 = numpy.array([0.0, -1.0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

    def create_contWeldL2_U3(self):
        contWeldL2_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([0, -1, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

    def create_contWeldL2_L3(self):

        contWeldL2_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([-1, 0.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([0.0, -1, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)



    def create_contWeldL1_U1(self):
        contWeldL1_U1OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.B/2-self.beamLeft.t/2,
                                            self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL1_U1 = numpy.array([0.0, 1, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

    def create_contWeldL1_L1(self):
        contWeldL1_L1OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.B/2-self.beamLeft.t/2,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL1_L1 = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

    def create_contWeldL2_U1(self):
        contWeldL2_U1OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.B/2-self.beamLeft.t/2,
                                            self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL2_U1 = numpy.array([0, 1, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

    def create_contWeldL2_L1(self):
        contWeldL2_L1OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.B/2-self.beamLeft.t/2,
                                            self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([1.0, 0.0,0.0])
        wDircontWeldL2_L1 = numpy.array([0.0, 1.0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)


        #############################################################################################################
        #   Following functions returns the CAD model to the function display_3DModel of main file                  #
        #############################################################################################################


    def get_models(self):
        '''Returning 3D models
        '''

        if self.endplate_type == "one_way":
            return [self.beamLModel, self.beamRModel, self.plateRModel,

                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model, ] + self.nut_bolt_array.get_models()        #self.beam_stiffener_1Model,

        elif self.endplate_type == "both_way":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model, ] + self.nut_bolt_array.get_models()        #self.beam_stiffener_1Model,self.beam_stiffener_2Model,

        elif self.endplate_type == "flush":
            return [self.beamLModel, self.beamRModel, self.plateRModel,

                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model, ] + self.nut_bolt_array.get_models()

    # def get_beamLModel(self):
    #     # return self.beamLModel
    #     final_column = self.beamLModel
    #     bolt_list = self.nut_bolt_array.get_bolt_list()
    #     for bolt in bolt_list[:]:
    #         final_column = BRepAlgoAPI_Cut(final_column, bolt).Shape()  # TODO: Anand #cuts the colum in section shape
    #     return final_column
    #
    # def get_contPlate_L1Model(self):
    #     return self.contPlate_L1Model
    #
    # def get_contPlate_L2Model(self):
    #     return self.contPlate_L2Model

class CADGroove(object):

    def __init__(self, beamLeft, beamRight, plateRight, nut_bolt_array,bolt,  bcWeldFlang_1, bcWeldFlang_2, bcWeldWeb_3,
                 bcWeldStiffHL_1, bcWeldStiffHL_2, bcWeldStiffHR_1, bcWeldStiffHR_2,
                 bcWeldStiffLL_1, bcWeldStiffLL_2, bcWeldStiffLR_1, bcWeldStiffLR_2,
                 contWeldL1_U2, contWeldL2_U2, contWeldL1_L2, contWeldL2_L2,
                 contWeldR1_U2, contWeldR2_U2, contWeldR1_L2, contWeldR2_L2,
                 contWeldL1_U3, contWeldL1_L3, contWeldL2_U3, contWeldL2_L3,
                 contWeldR1_U3, contWeldR1_L3, contWeldR2_U3, contWeldR2_L3,
                 contWeldL1_U1, contWeldL1_L1, contWeldL2_U1, contWeldL2_L1,
                 contWeldR1_U1, contWeldR1_L1, contWeldR2_U1, contWeldR2_L1,
                 contPlate_L1,contPlate_L2,contPlate_R1,contPlate_R2,beam_stiffener_1,beam_stiffener_2, endplate_type, outputobj):

        # Initializing the arguments
        self.beamLeft = beamLeft                            # beamLeft represents the column
        self.beamRight = beamRight
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.bolt = bolt
        self.contPlate_L1 = contPlate_L1
        self.contPlate_L2 = contPlate_L2
        self.contPlate_R1 = contPlate_R1
        self.contPlate_R2 = contPlate_R2
        self.beam_stiffener_1 = beam_stiffener_1
        self.beam_stiffener_2 = beam_stiffener_2
        self.endplate_type = endplate_type
        self.outputobj = outputobj
        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection
        # self.Lv = float(outputobj["Bolt"]["Lv"])

        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection d


        # Weld above flange for left and right beam
        self.bcWeldFlang_1 = bcWeldFlang_1
        self.bcWeldFlang_2 = bcWeldFlang_2
        self.bcWeldWeb_3 = bcWeldWeb_3

        self.bcWeldStiffHL_1 = bcWeldStiffHL_1
        self.bcWeldStiffHL_2 = bcWeldStiffHL_2
        self.bcWeldStiffHR_1 = bcWeldStiffHR_1
        self.bcWeldStiffHR_2 = bcWeldStiffHR_2

        self.bcWeldStiffLL_1 = bcWeldStiffLL_1
        self.bcWeldStiffLL_2 = bcWeldStiffLL_2
        self.bcWeldStiffLR_1 = bcWeldStiffLR_1
        self.bcWeldStiffLR_2 = bcWeldStiffLR_2

        self.contWeldL1_U2 = contWeldL1_U2
        self.contWeldL2_U2 = contWeldL2_U2
        self.contWeldL1_L2 = contWeldL1_L2
        self.contWeldL2_L2 = contWeldL2_L2
        self.contWeldR1_U2 = contWeldR1_U2
        self.contWeldR2_U2 = contWeldR2_U2
        self.contWeldR1_L2 = contWeldR1_L2
        self.contWeldR2_L2 = contWeldR2_L2
        self.contWeldL1_U3 = contWeldL1_U3
        self.contWeldL1_L3 = contWeldL1_L3
        self.contWeldL2_U3 = contWeldL2_U3
        self.contWeldL2_L3 = contWeldL2_L3
        self.contWeldR1_U3 = contWeldR1_U3
        self.contWeldR1_L3 = contWeldR1_L3
        self.contWeldR2_U3 = contWeldR2_U3
        self.contWeldR2_L3 = contWeldR2_L3
        self.contWeldL1_U1 = contWeldL1_U1
        self.contWeldL1_L1 = contWeldL1_L1
        self.contWeldL2_U1 = contWeldL2_U1
        self.contWeldL2_L1 = contWeldL2_L1
        self.contWeldR1_U1 = contWeldR1_U1
        self.contWeldR1_L1 = contWeldR1_L1
        self.contWeldR2_U1 = contWeldR2_U1
        self.contWeldR2_L1 = contWeldR2_L1




    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.create_contPlate_L1Geometry()
        self.create_contPlate_L2Geometry()
        self.create_contPlate_R1Geometry()
        self.create_contPlate_R2Geometry()
        self.create_beam_stiffener_1Geometry()
        self.create_beam_stiffener_2Geometry()


        self.create_bcWeldFlang_1()
        self.create_bcWeldFlang_2()
        self.create_bcWeldWeb_3()

        self.create_bcWeldStiffHL_1()
        self.create_bcWeldStiffHL_2()
        self.create_bcWeldStiffHR_1()
        self.create_bcWeldStiffHR_2()

        self.create_bcWeldStiffLL_1()
        self.create_bcWeldStiffLL_2()
        self.create_bcWeldStiffLR_1()
        self.create_bcWeldStiffLR_2()

        self.create_contWeldL1_U2()
        self.create_contWeldL2_U2()
        self.create_contWeldL1_L2()
        self.create_contWeldL2_L2()
        self.create_contWeldR1_U2()
        self.create_contWeldR2_U2()
        self.create_contWeldR1_L2()
        self.create_contWeldR2_L2()
        self.create_contWeldL1_U3()
        self.create_contWeldL1_L3()
        self.create_contWeldL2_U3()
        self.create_contWeldL2_L3()
        self.create_contWeldR1_U3()
        self.create_contWeldR1_L3()
        self.create_contWeldR2_U3()
        self.create_contWeldR2_L3()
        self.create_contWeldL1_U1()
        self.create_contWeldL1_L1()
        self.create_contWeldL2_U1()
        self.create_contWeldL2_L1()
        self.create_contWeldR1_U1()
        self.create_contWeldR1_L1()
        self.create_contWeldR2_U1()
        self.create_contWeldR2_L1()


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        self.contPlate_L1Model = self.contPlate_L1.create_model()
        self.contPlate_L2Model = self.contPlate_L2.create_model()
        self.contPlate_R1Model = self.contPlate_R1.create_model()
        self.contPlate_R2Model = self.contPlate_R2.create_model()
        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()

        self.bcWeldFlang_1Model =  self.bcWeldFlang_1.create_model()
        self.bcWeldFlang_2Model = self.bcWeldFlang_2.create_model()
        self.bcWeldWeb_3Model = self.bcWeldWeb_3.create_model()

        self.bcWeldStiffHL_1Model = self.bcWeldStiffHL_1.create_model()
        self.bcWeldStiffHL_2Model = self.bcWeldStiffHL_2.create_model()
        self.bcWeldStiffHR_1Model = self.bcWeldStiffHR_1.create_model()
        self.bcWeldStiffHR_2Model = self.bcWeldStiffHR_2.create_model()

        self.bcWeldStiffLL_1Model = self.bcWeldStiffLL_1.create_model()
        self.bcWeldStiffLL_2Model = self.bcWeldStiffLL_2.create_model()
        self.bcWeldStiffLR_1Model = self.bcWeldStiffLR_1.create_model()
        self.bcWeldStiffLR_2Model = self.bcWeldStiffLR_2.create_model()

        self.contWeldL1_U2Model = self.contWeldL1_U2.create_model()
        self.contWeldL2_U2Model = self.contWeldL2_U2.create_model()
        self.contWeldL1_L2Model = self.contWeldL1_L2.create_model()
        self.contWeldL2_L2Model = self.contWeldL2_L2.create_model()
        self.contWeldR1_U2Model = self.contWeldR1_U2.create_model()
        self.contWeldR2_U2Model = self.contWeldR2_U2.create_model()
        self.contWeldR1_L2Model = self.contWeldR1_L2.create_model()
        self.contWeldR2_L2Model = self.contWeldR2_L2.create_model()
        self.contWeldL1_U3Model = self.contWeldL1_U3.create_model()
        self.contWeldL1_L3Model = self.contWeldL1_L3.create_model()
        self.contWeldL2_U3Model = self.contWeldL2_U3.create_model()
        self.contWeldL2_L3Model = self.contWeldL2_L3.create_model()
        self.contWeldR1_U3Model = self.contWeldR1_U3.create_model()
        self.contWeldR1_L3Model = self.contWeldR1_L3.create_model()
        self.contWeldR2_U3Model = self.contWeldR2_U3.create_model()
        self.contWeldR2_L3Model = self.contWeldR2_L3.create_model()
        self.contWeldL1_U1Model = self.contWeldL1_U1.create_model()
        self.contWeldL1_L1Model = self.contWeldL1_L1.create_model()
        self.contWeldL2_U1Model = self.contWeldL2_U1.create_model()
        self.contWeldL2_L1Model = self.contWeldL2_L1.create_model()
        self.contWeldR1_U1Model = self.contWeldR1_U1.create_model()
        self.contWeldR1_L1Model = self.contWeldR1_L1.create_model()
        self.contWeldR2_U1Model = self.contWeldR2_U1.create_model()
        self.contWeldR2_L1Model = self.contWeldR2_L1.create_model()

#############################################################################################################
#   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
#   same component at appropriate place                                                                     #
#############################################################################################################

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0,0.0,0.0 ])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamLeft.D /2  +  self.plateRight.T +  self.bcWeldWeb_3.b
        beamOriginR = numpy.array([0.0, gap, self.beamLeft.length /2 ])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plateRight.T + self.beamLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.beamLeft.length / 2 + (self.plateRight.L/2 - self.boltProjection - self.beamRight.D /2)])  #TODO #Add weld thickness here
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:         #self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plateRight.T + self.beamLeft.D/2
            plateOriginR = numpy.array([-self.plateRight.W/2, gap, self.beamLeft.length /2 ])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)



    def create_nut_bolt_array(self):

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0,  self.plateRight.T/2,  + (self.plateRight.L/2 )])       # self.plateRight.L/2+ (self.plateRight.L/2 - (10) - self.beamRight.D /2) - 40#TODO add end distance here #self.plateRight.L/2 + (self.plateRight.L/2 - (10 + 8) - self.beamRight.D /2)
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.plateRight.T/2 , self.plateRight.L /2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.plateRight.T/2, self.beamRight.D/2])       #TODO Add self.Lv instead of 25
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlate_L1Geometry(self):
        beamOriginL = numpy.array([self.beamLeft.B/2 - self.contPlate_L1.W/2, 0.0, self.beamLeft.length/2 + self.beamRight.D/2 - self.beamRight.T/2 + self.contPlate_L1.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_L2Geometry(self):
        beamOriginL = numpy.array([self.beamLeft.B/2 - self.contPlate_L2.W/2, 0.0, self.beamLeft.length/2 - self.beamRight.D/2 + self.beamRight.T/2 + self.contPlate_L2.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_R1Geometry(self):
        beamOriginL = numpy.array([-self.beamLeft.B/2 + self.contPlate_R1.W/2, 0.0, self.beamLeft.length/2 + self.beamRight.D/2 - self.beamRight.T/2 - self.contPlate_R1.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_R2Geometry(self):
        beamOriginL = numpy.array([-self.beamLeft.B/2 + self.contPlate_R2.W/2, 0.0, self.beamLeft.length/2 - self.beamRight.D/2 + self.beamRight.T/2 - self.contPlate_R2.T/2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R2.place(beamOriginL, beamL_uDir, beamL_wDir)

    ##############################################  Adding beam stiffeners #############################################
    def create_beam_stiffener_1Geometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L/2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T/2, gap, self.beamLeft.length / 2 + self.beamRight.D/2 + self.beam_stiffener_1.W/2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

    def create_beam_stiffener_2Geometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L/2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T/2, gap, self.beamLeft.length / 2 - self.beamRight.D/2 - self.beam_stiffener_1.W/2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    ##############################################  creating weld sections ########################################

    def create_bcWeldFlang_1(self):
        weldFlangOrigin_1 = numpy.array([-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T+self.bcWeldWeb_3.b/2,
                                             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T/2])
        uDir_1 = numpy.array([0, 1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bcWeldFlang_1.place(weldFlangOrigin_1, uDir_1, wDir_1)
    def create_bcWeldFlang_2(self):
        weldFlangOrigin_2 = numpy.array([self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T+self.bcWeldWeb_3.b/2,
                                             self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T/2])
        uDir_2 = numpy.array([0, 1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bcWeldFlang_2.place(weldFlangOrigin_2, uDir_2, wDir_2)
    def create_bcWeldWeb_3(self):
        weldWebOrigin_3 = numpy.array([0.0, self.beamLeft.D / 2 + self.plateRight.T+self.bcWeldWeb_3.b/2,
                                            self.beamLeft.length / 2 - self.bcWeldWeb_3.L / 2])
        uDirWeb_3 = numpy.array([0, 1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bcWeldWeb_3.place(weldWebOrigin_3, uDirWeb_3, wDirWeb_3)

    def create_bcWeldStiffHL_1(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 + self.beamRight.D/2 + self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffHL_2(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 - self.beamRight.D/2 - self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffHR_1(self):
        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 + self.beamRight.D/2 + self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffHR_2(self):
        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                            self.beamLeft.length / 2 - self.beamRight.D/2 - self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffLL_1(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L,
                                            self.beamLeft.length / 2 + self.beamRight.D/2 ])
        uDirStiffHL_1 = numpy.array([1, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0, -1.0, 0.0])
        self.bcWeldStiffLL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffLL_2(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T+ self.beam_stiffener_1.L22,
                                            self.beamLeft.length / 2 - self.beamRight.D/2])
        uDirStiffHL_1 = numpy.array([1.0, 0.0, 0.0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffLR_1(self):
        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T+ self.beam_stiffener_1.L22,
                                            self.beamLeft.length / 2 + self.beamRight.D/2 ])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    def create_bcWeldStiffLR_2(self):
        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T+ self.beam_stiffener_1.L,
                                            self.beamLeft.length / 2 - self.beamRight.D/2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bcWeldStiffLR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

####################################### welding continuity plates with fillet weld##################################

    def create_contWeldL1_U2(self):
        contWeldL1_U2OriginL = numpy.array([self.beamLeft.t/2, -self.contPlate_L1.L/2,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

    def create_contWeldL2_U2(self):
        contWeldL2_U2OriginL = numpy.array([self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T/2 ])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

    def create_contWeldL1_L2(self):
        contWeldL1_L2OriginL = numpy.array([self.beamLeft.t/2, -self.contPlate_L1.L/2,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        contWeldL1_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

    def create_contWeldL2_L2(self):
        contWeldL2_L2OriginL = numpy.array([self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2
                                            - self.beamRight.D / 2  -self.contPlate_L1.T/2+ self.beamRight.T / 2 ])
        contWeldL2_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

    def create_contWeldR1_U2(self):
        contWeldR1_U2OriginL = numpy.array([-self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2 ])
        contWeldR1_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_U2.place(contWeldR1_U2OriginL, contWeldR1_U2_uDir, contWeldR1_U2_wDir)

    def create_contWeldR2_U2(self):
        contWeldR2_U2OriginL = numpy.array([-self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2
                                            - self.beamRight.D/2 + self.beamRight.T / 2 + self.contPlate_L1.T/2 ])
        contWeldR2_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_U2.place(contWeldR2_U2OriginL, contWeldR2_U2_uDir, contWeldR2_U2_wDir)

    def create_contWeldR1_L2(self):
        contWeldR1_L2OriginL = numpy.array([-self.beamLeft.t/2, -self.contPlate_L1.L/2,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        contWeldR1_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_L2.place(contWeldR1_L2OriginL, contWeldR1_L2_uDir, contWeldR1_L2_wDir)

    def create_contWeldR2_L2(self):
        contWeldR2_L2OriginL = numpy.array([-self.beamLeft.t/2, -self.contPlate_L1.L/2,self.beamLeft.length / 2
                                            - self.beamRight.D / 2  + self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        contWeldR2_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_L2.place(contWeldR2_L2OriginL, contWeldR2_L2_uDir, contWeldR2_L2_wDir)

    def create_contWeldL1_U3(self):
        contWeldL1_U3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldL1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)
    def create_contWeldL1_L3(self):
        contWeldL1_L3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        uDircontWeldL1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)
    def create_contWeldR2_U3(self):
        contWeldR2_U3OriginL = numpy.array([ -self.beamLeft.B/ 2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2)+ self.beamRight.T / 2 + self.contPlate_L1.T/2])   #TODO: shuffel it with R2_U3
        uDircontWeldR2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U3.place(contWeldR2_U3OriginL, uDircontWeldR2_U3, wDircontWeldR2_U3)

    # def create_contWeldL2_L3(self):
    #     contWeldL2_L3OriginL = numpy.array([ -self.beamLeft.B/2, self.contPlate_L1.L/2 ,
    #                                           self.beamLeft.length / 2 + (self.beamRight.D / 2) -self.beamRight.D])
    #     uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
    #     wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
    #     self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

    def create_contWeldL2_L3(self):
        contWeldL2_L3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)


    def create_contWeldR1_U3(self):
        contWeldR1_U3OriginL = numpy.array([ -self.beamLeft.B/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldR1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U3.place(contWeldR1_U3OriginL, uDircontWeldR1_U3, wDircontWeldR1_U3)
    def create_contWeldR1_L3(self):
        contWeldR1_L3OriginL = numpy.array([ -self.beamLeft.B/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        uDircontWeldR1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L3.place(contWeldR1_L3OriginL, uDircontWeldR1_L3, wDircontWeldR1_L3)
    def create_contWeldL2_U3(self):
        contWeldL2_U3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)
    # def create_contWeldR2_L3(self):
    #     contWeldR2_L3OriginL = numpy.array([ self.beamLeft.t/2, self.contPlate_L1.L/2 ,
    #                                           self.beamLeft.length / 2 + (self.beamRight.D / 2) -self.beamRight.D])
    #     uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
    #     wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
    #     self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)

    def create_contWeldR2_L3(self):
        contWeldR2_L3OriginL = numpy.array([ -self.beamLeft.B/2, self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)
    def create_contWeldL1_U1(self):
        contWeldL1_U1OriginL = numpy.array([self.beamLeft.t/2 , -self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 + self.contPlate_L1.T/2 ])
        uDircontWeldL1_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)
    def create_contWeldL1_L1(self):
        contWeldL1_L1OriginL = numpy.array([ self.beamLeft.t/2,-self.contPlate_L1.L/2,
                                             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldL1_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldL1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)
    def create_contWeldL2_U1(self):
        contWeldL2_U1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                       self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T/2 ])
        uDircontWeldL2_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)
    def create_contWeldR2_L1(self):
        contWeldR2_L1OriginL = numpy.array([ -self.beamLeft.B / 2,-self.contPlate_L1.L/2,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldR2_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldR2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L1.place(contWeldR2_L1OriginL, uDircontWeldR2_L1, wDircontWeldR2_L1)
    def create_contWeldR1_U1(self):
        contWeldR1_U1OriginL = numpy.array([ - self.beamLeft.B/2, -self.contPlate_L1.L/2,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldR1_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U1.place(contWeldR1_U1OriginL, uDircontWeldR1_U1, wDircontWeldR1_U1)
    def create_contWeldR1_L1(self):
        contWeldR1_L1OriginL = numpy.array([ -self.beamLeft.B/2, -self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T/2 ])
        uDircontWeldR1_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldR1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L1.place(contWeldR1_L1OriginL, uDircontWeldR1_L1, wDircontWeldR1_L1)
    def create_contWeldR2_U1(self):
        contWeldR2_U1OriginL = numpy.array([ -self.beamLeft.B/2, -self.contPlate_L1.L/2 ,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T/2])
        uDircontWeldR2_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U1.place(contWeldR2_U1OriginL, uDircontWeldR2_U1, wDircontWeldR2_U1)
    def create_contWeldL2_L1(self):
        contWeldL2_L1OriginL = numpy.array([ self.beamLeft.t/2, -self.contPlate_L1.L/2,
                                              self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T/2])
        uDircontWeldL2_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldL2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

#############################################################################################################
#   Following functions returns the CAD model to the function display_3DModel of main file                  #
#############################################################################################################
    def get_beamLModel(self):
        # return self.beamLModel
        final_column = self.beamLModel
        bolt_list = self.nut_bolt_array.get_bolt_list()
        for bolt in bolt_list[:]:
            final_column = BRepAlgoAPI_Cut(final_column, bolt).Shape()  # TODO: Anand #cuts the colum in section shape
        return final_column
    def get_beamRModel(self):
        return self.beamRModel

    def get_plateRModel(self):
        return self.plateRModel

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()

    def get_contPlate_L1Model(self):
        return self.contPlate_L1Model

    def get_contPlate_L2Model(self):
        return self.contPlate_L2Model

    def get_contPlate_R1Model(self):
        return self.contPlate_R1Model

    def get_contPlate_R2Model(self):
        return self.contPlate_R2Model

    def get_beam_stiffener_1Model(self):
        return  self.beam_stiffener_1Model

    def get_beam_stiffener_2Model(self):
        return self.beam_stiffener_2Model

    def get_bcWeldFlang_1Model(self):
        return self.bcWeldFlang_1Model

    def get_bcWeldFlang_2Model(self):
        return self.bcWeldFlang_2Model

    def get_bcWeldWeb_3Model(self):
        return self.bcWeldWeb_3Model

    def get_bcWeldStiffHL_1Model(self):
        return self.bcWeldStiffHL_1Model

    def get_bcWeldStiffHL_2Model(self):
        return self.bcWeldStiffHL_2Model

    def get_bcWeldStiffHR_1Model(self):
        return self.bcWeldStiffHR_1Model

    def get_bcWeldStiffHR_2Model(self):
        return self.bcWeldStiffHR_2Model

    def get_bcWeldStiffLL_1Model(self):
        return self.bcWeldStiffLL_1Model

    def get_bcWeldStiffLL_2Model(self):
        return self.bcWeldStiffLL_2Model

    def get_bcWeldStiffLR_1Model(self):
        return self.bcWeldStiffLR_1Model

    def get_bcWeldStiffLR_2Model(self):
        return self.bcWeldStiffLR_2Model

    def get_contWeldL1_U2Model(self):
        return self.contWeldL1_U2Model
    def get_contWeldL2_U2Model(self):
        return self.contWeldL2_U2Model
    def get_contWeldL1_L2Model(self):
        return self.contWeldL1_L2Model
    def get_contWeldL2_L2Model(self):
        return self.contWeldL2_L2Model
    def get_contWeldR1_U2Model(self):
        return self.contWeldR1_U2Model
    def get_contWeldR2_U2Model(self):
        return self.contWeldR2_U2Model
    def get_contWeldR1_L2Model(self):
        return self.contWeldR1_L2Model
    def get_contWeldR2_L2Model(self):
        return self.contWeldR2_L2Model
    def get_contWeldL1_U3Model(self):
        return self.contWeldL1_U3Model
    def get_contWeldL1_L3Model(self):
        return self.contWeldL1_L3Model
    def get_contWeldL2_U3Model(self):
        return self.contWeldL2_U3Model
    def get_contWeldL2_L3Model(self):
        return self.contWeldL2_L3Model
    def get_contWeldR1_U3Model(self):
        return self.contWeldR1_U3Model
    def get_contWeldR1_L3Model(self):
        return self.contWeldR1_L3Model
    def get_contWeldR2_U3Model(self):
        return self.contWeldR2_U3Model
    def get_contWeldR2_L3Model(self):
        return self.contWeldR2_L3Model
    def get_contWeldL1_U1Model(self):
        return self.contWeldL1_U1Model
    def get_contWeldL1_L1Model(self):
        return self.contWeldL1_L1Model
    def get_contWeldL2_U1Model(self):
        return self.contWeldL2_U1Model
    def get_contWeldL2_L1Model(self):
        return self.contWeldL2_L1Model
    def get_contWeldR1_U1Model(self):
        return self.contWeldR1_U1Model
    def get_contWeldR1_L1Model(self):
        return self.contWeldR1_L1Model
    def get_contWeldR2_U1Model(self):
        return self.contWeldR2_U1Model
    def get_contWeldR2_L1Model(self):
        return self.contWeldR2_L1Model

    def get_models(self):
        '''Returning 3D models
        '''

        if self.endplate_type == "one_way":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model] + self.nut_bolt_array.get_models()       #self.beam_stiffener_1Model,
        elif self.endplate_type == "both_way":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model] + self.nut_bolt_array.get_models()       # self.beam_stiffener_1Model,self.beam_stiffener_2Model,
        elif self.endplate_type == "flush":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model] + self.nut_bolt_array.get_models()



class CADcolwebGroove(CADGroove):
    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, self.beamLeft.D/2 - self.beamLeft.t/2, 0.0])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)



        ##############################################  Adding contPlates ########################################

    def create_contPlate_L1Geometry(self):
        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D / 2 - self.beamLeft.t  - self.contPlate_L1.W / 2,
             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T/2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contPlate_L2Geometry(self):
        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D / 2 - self.beamLeft.t - self.contPlate_L2.W / 2,
             self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T/2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contWeldL1_U2(self):
        contWeldL1_U2OriginL = numpy.array([-self.contPlate_L1.L/2,  self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([1.0, 0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

    def create_contWeldL2_U2(self):
        contWeldL2_U2OriginL = numpy.array([-self.contPlate_L1.L/2, self.beamLeft.D/2-self.beamLeft.t, self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

    def create_contWeldL1_L2(self):
        contWeldL1_L2OriginL = numpy.array([-self.contPlate_L1.L / 2,  self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

    def create_contWeldL2_L2(self):
        contWeldL2_L2OriginL = numpy.array([-self.contPlate_L1.L / 2,  self.beamLeft.D/2-self.beamLeft.t, self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL2_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)



    def create_contWeldL1_U3(self):
        contWeldL1_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0.0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([0.0, -1, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

    def create_contWeldL1_L3(self):
        contWeldL1_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 + (
                                                        self.beamRight.D / 2)- self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([-1, 0, 0.0])
        wDircontWeldL1_L3 = numpy.array([0.0, -1.0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

    def create_contWeldL2_U3(self):
        contWeldL2_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([0, -1, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

    def create_contWeldL2_L3(self):

        contWeldL2_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.t,
                                            self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([-1, 0.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([0.0, -1, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)



    def create_contWeldL1_U1(self):
        contWeldL1_U1OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.B/2-self.beamLeft.t/2,
                                            self.beamLeft.length / 2 + (self.beamRight.D / 2)- self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL1_U1 = numpy.array([0.0, 1, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

    def create_contWeldL1_L1(self):
        contWeldL1_L1OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.B/2-self.beamLeft.t/2,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL1_L1 = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

    def create_contWeldL2_U1(self):
        contWeldL2_U1OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.B/2-self.beamLeft.t/2,
                                            self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL2_U1 = numpy.array([0, 1, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

    def create_contWeldL2_L1(self):
        contWeldL2_L1OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D/2-self.beamLeft.B/2-self.beamLeft.t/2,
                                            self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([1.0, 0.0,0.0])
        wDircontWeldL2_L1 = numpy.array([0.0, 1.0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)


    def get_models(self):
        '''Returning 3D models
        '''

        if self.endplate_type == "one_way":
            return [self.beamLModel, self.beamRModel, self.plateRModel,

                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model] + self.nut_bolt_array.get_models()       #self.beam_stiffener_1Model,
        elif self.endplate_type == "both_way":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model] + self.nut_bolt_array.get_models()       #self.beam_stiffener_1Model,self.beam_stiffener_2Model,
        elif self.endplate_type == "flush":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model] + self.nut_bolt_array.get_models()


