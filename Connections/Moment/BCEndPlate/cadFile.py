"""
Initialized on 23-04-2019
Commenced on 24-04-2019
@author: Anand Swaroop
"""""

import copy

import numpy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut


class CADFillet(object):
    def __init__(self, columnLeft, beamRight, plateRight, nut_bolt_array, bolt, bbWeldAbvFlang,
                 bbWeldBelwFlang, bbWeldSideWeb, contWeldD, contWeldB, bcWeldStiffHeight, bcWeldStiffLength,
                 contPlates, beam_stiffeners, endplate_type, conn_type, outputobj):
        """

        :param columnLeft:
        :param beamRight:
        :param plateRight:
        :param nut_bolt_array:
        :param bolt:
        :param bbWeldAbvFlang:
        :param bbWeldBelwFlang:
        :param bbWeldSideWeb:
        :param contWeldD:
        :param contWeldB:
        :param bcWeldStiffHeight:
        :param bcWeldStiffLength:
        :param contPlates:
        :param beam_stiffeners:
        :param endplate_type:
        :param conn_type:
        :param outputobj:
        """

        # Initializing the arguments
        self.columnLeft = columnLeft  # beamLeft represents the column
        self.beamRight = beamRight
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.bolt = bolt
        # self.beamRight.length = 100.0
        self.contPlate_L1 = contPlates
        self.contPlate_L2 = copy.deepcopy(contPlates)
        self.contPlate_R1 = copy.deepcopy(contPlates)
        self.contPlate_R2 = copy.deepcopy(contPlates)
        self.beam_stiffener_1 = beam_stiffeners
        self.beam_stiffener_2 = copy.deepcopy(beam_stiffeners)

        self.endplate_type = endplate_type
        self.conn_type = conn_type  # TODO: Remove this type if not needed
        self.outputobj = outputobj
        self.numberOfBolts = int(outputobj["Bolt"]["NumberOfBolts"])
        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection
        # self.Lv = float(outputobj["Bolt"]["Lv"])

        # Weld above flange for left and right beam
        self.bbWeldAbvFlang_21 = bbWeldAbvFlang  # Right beam upper side
        self.bbWeldAbvFlang_22 = copy.deepcopy(bbWeldAbvFlang)  # Right beam lower side

        self.bbWeldBelwFlang_21 = bbWeldBelwFlang  # behind bbWeldBelwFlang_11
        self.bbWeldBelwFlang_22 = copy.deepcopy(bbWeldBelwFlang)  # behind bbWeldBelwFlang_12
        self.bbWeldBelwFlang_23 = copy.deepcopy(bbWeldBelwFlang)  # behind bbWeldBelwFlang_13
        self.bbWeldBelwFlang_24 = copy.deepcopy(bbWeldBelwFlang)  # behind bbWeldBelwFlang_14

        self.bbWeldSideWeb_21 = bbWeldSideWeb  # Behind bbWeldSideWeb_11
        self.bbWeldSideWeb_22 = copy.deepcopy(bbWeldSideWeb)  # Behind bbWeldSideWeb_12

        self.contWeldL1_U2 = contWeldD
        self.contWeldL2_U2 = copy.deepcopy(contWeldD)
        self.contWeldL1_L2 = copy.deepcopy(contWeldD)
        self.contWeldL2_L2 = copy.deepcopy(contWeldD)
        self.contWeldR1_U2 = copy.deepcopy(contWeldD)
        self.contWeldR2_U2 = copy.deepcopy(contWeldD)
        self.contWeldR1_L2 = copy.deepcopy(contWeldD)
        self.contWeldR2_L2 = copy.deepcopy(contWeldD)
        self.contWeldL1_U3 = contWeldB
        self.contWeldL1_L3 = copy.deepcopy(contWeldB)
        self.contWeldL2_U3 = copy.deepcopy(contWeldB)
        self.contWeldL2_L3 = copy.deepcopy(contWeldB)
        self.contWeldR1_U3 = copy.deepcopy(contWeldB)
        self.contWeldR1_L3 = copy.deepcopy(contWeldB)
        self.contWeldR2_U3 = copy.deepcopy(contWeldB)
        self.contWeldR2_L3 = copy.deepcopy(contWeldB)
        self.contWeldL1_U1 = copy.deepcopy(contWeldB)
        self.contWeldL1_L1 = copy.deepcopy(contWeldB)
        self.contWeldL2_U1 = copy.deepcopy(contWeldB)
        self.contWeldL2_L1 = copy.deepcopy(contWeldB)
        self.contWeldR1_U1 = copy.deepcopy(contWeldB)
        self.contWeldR1_L1 = copy.deepcopy(contWeldB)
        self.contWeldR2_U1 = copy.deepcopy(contWeldB)
        self.contWeldR2_L1 = copy.deepcopy(contWeldB)

        self.bcWeldStiffHL_1 = bcWeldStiffHeight
        self.bcWeldStiffHL_2 = copy.deepcopy(bcWeldStiffHeight)
        self.bcWeldStiffHR_1 = copy.deepcopy(bcWeldStiffHeight)
        self.bcWeldStiffHR_2 = copy.deepcopy(bcWeldStiffHeight)

        self.bcWeldStiffLL_1 = bcWeldStiffLength
        self.bcWeldStiffLL_2 = copy.deepcopy(bcWeldStiffLength)
        self.bcWeldStiffLR_1 = copy.deepcopy(bcWeldStiffLength)
        self.bcWeldStiffLR_2 = copy.deepcopy(bcWeldStiffLength)

    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.create_contPlatesGeometry()
        # self.create_beam_stiffenersGeometry()
        # self.create_beam_stiffener_2Geometry()

        # self.create_bbWelds()  # left beam above flange weld
        #
        # self.create_contWelds()
        #
        # self.create_bcWeldStiff()

        # call for create_model of filletweld from Components directory
        self.beamLModel = self.columnLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        # self.contPlate_L1Model = self.contPlate_L1.create_model()
        # self.contPlate_L2Model = self.contPlate_L2.create_model()
        # self.contPlate_R1Model = self.contPlate_R1.create_model()
        # self.contPlate_R2Model = self.contPlate_R2.create_model()
        # self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        # self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()

        # self.bbWeldAbvFlang_21Model = self.bbWeldAbvFlang_21.create_model()
        # self.bbWeldAbvFlang_22Model = self.bbWeldAbvFlang_22.create_model()
        #
        # self.bbWeldBelwFlang_21Model = self.bbWeldBelwFlang_21.create_model()
        # self.bbWeldBelwFlang_22Model = self.bbWeldBelwFlang_22.create_model()
        # self.bbWeldBelwFlang_23Model = self.bbWeldBelwFlang_23.create_model()
        # self.bbWeldBelwFlang_24Model = self.bbWeldBelwFlang_24.create_model()
        #
        # self.bbWeldSideWeb_21Model = self.bbWeldSideWeb_21.create_model()
        # self.bbWeldSideWeb_22Model = self.bbWeldSideWeb_22.create_model()

        # self.contWeldL1_U2Model = self.contWeldL1_U2.create_model()
        # self.contWeldL2_U2Model = self.contWeldL2_U2.create_model()
        # self.contWeldL1_L2Model = self.contWeldL1_L2.create_model()
        # self.contWeldL2_L2Model = self.contWeldL2_L2.create_model()
        # self.contWeldR1_U2Model = self.contWeldR1_U2.create_model()
        # self.contWeldR2_U2Model = self.contWeldR2_U2.create_model()
        # self.contWeldR1_L2Model = self.contWeldR1_L2.create_model()
        # self.contWeldR2_L2Model = self.contWeldR2_L2.create_model()
        # self.contWeldL1_U3Model = self.contWeldL1_U3.create_model()
        # self.contWeldL1_L3Model = self.contWeldL1_L3.create_model()
        # self.contWeldL2_U3Model = self.contWeldL2_U3.create_model()
        # self.contWeldL2_L3Model = self.contWeldL2_L3.create_model()
        # self.contWeldR1_U3Model = self.contWeldR1_U3.create_model()
        # self.contWeldR1_L3Model = self.contWeldR1_L3.create_model()
        # self.contWeldR2_U3Model = self.contWeldR2_U3.create_model()
        # self.contWeldR2_L3Model = self.contWeldR2_L3.create_model()
        # self.contWeldL1_U1Model = self.contWeldL1_U1.create_model()
        # self.contWeldL1_L1Model = self.contWeldL1_L1.create_model()
        # self.contWeldL2_U1Model = self.contWeldL2_U1.create_model()
        # self.contWeldL2_L1Model = self.contWeldL2_L1.create_model()
        # self.contWeldR1_U1Model = self.contWeldR1_U1.create_model()
        # self.contWeldR1_L1Model = self.contWeldR1_L1.create_model()
        # self.contWeldR2_U1Model = self.contWeldR2_U1.create_model()
        # self.contWeldR2_L1Model = self.contWeldR2_L1.create_model()

        # self.bcWeldStiffHL_1Model = self.bcWeldStiffHL_1.create_model()
        # self.bcWeldStiffHL_2Model = self.bcWeldStiffHL_2.create_model()
        # self.bcWeldStiffHR_1Model = self.bcWeldStiffHR_1.create_model()
        # self.bcWeldStiffHR_2Model = self.bcWeldStiffHR_2.create_model()
        #
        # self.bcWeldStiffLL_1Model = self.bcWeldStiffLL_1.create_model()
        # self.bcWeldStiffLL_2Model = self.bcWeldStiffLL_2.create_model()
        # self.bcWeldStiffLR_1Model = self.bcWeldStiffLR_1.create_model()
        # self.bcWeldStiffLR_2Model = self.bcWeldStiffLR_2.create_model()

    #############################################################################################################
    #   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
    #   same component at appropriate place                                                                     #
    #############################################################################################################

    def createBeamLGeometry(self):
        # if self.conn_type == 'col_flange_connectivity':
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.columnLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        beamOriginR = numpy.array([0.0, 0.0, self.columnLeft.length])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plateRight.T + self.columnLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.columnLeft.length / 2 + (
                    self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:  # self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plateRight.T + self.columnLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.columnLeft.length])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array(
                [0.0, self.plateRight.T / 2, + (self.plateRight.L / 2)])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array(
                [0.0, self.plateRight.T / 2, self.plateRight.L / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array(
                [0.0, self.plateRight.T / 2, self.beamRight.D / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        beamOriginL = numpy.array([self.columnLeft.B / 2 - self.contPlate_L1.W / 2, 0.0,
                                   self.columnLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([self.columnLeft.B / 2 - self.contPlate_L2.W / 2, 0.0,
                                   self.columnLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-self.columnLeft.B / 2 + self.contPlate_R1.W / 2, 0.0,
                                   self.columnLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_R1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-self.columnLeft.B / 2 + self.contPlate_R2.W / 2, 0.0,
                                   self.columnLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_R1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R2.place(beamOriginL, beamL_uDir, beamL_wDir)

    ##############################################  Adding beam stiffeners #############################################
    # def create_beam_stiffenersGeometry(self):
    #     gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L / 2
    #     stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
    #                                     self.beamLeft.length / 2 + self.beamRight.D / 2 + self.beam_stiffener_1.W / 2])
    #     stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
    #     stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
    #     self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)
    #
    #     gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L / 2
    #     stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, gap,
    #                                     self.beamLeft.length / 2 - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2])
    #     stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
    #     stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
    #     self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    ##############################################  creating weld sections ########################################
    # def create_bbWelds(self):
    #     weldAbvFlangOrigin_21 = numpy.array([-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                          self.beamLeft.length / 2 + self.beamRight.D / 2])
    #     uDirAbv_21 = numpy.array([0, 1.0, 0])
    #     wDirAbv_21 = numpy.array([1.0, 0, 0])
    #     self.bbWeldAbvFlang_21.place(weldAbvFlangOrigin_21, uDirAbv_21, wDirAbv_21)
    #
    #     weldAbvFlangOrigin_22 = numpy.array([self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                          self.beamLeft.length / 2 - self.beamRight.D / 2])
    #     uDirAbv_22 = numpy.array([0, 1.0, 0])
    #     wDirAbv_22 = numpy.array([-1.0, 0, 0])
    #     self.bbWeldAbvFlang_22.place(weldAbvFlangOrigin_22, uDirAbv_22, wDirAbv_22)
    #
    #     weldBelwFlangOrigin_21 = numpy.array([-self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                           self.beamLeft.length / 2 + (self.beamRight.D / 2) -
    #                                           self.beamRight.T])
    #     uDirBelw_21 = numpy.array([0, 1.0, 0])
    #     wDirBelw_21 = numpy.array([-1.0, 0, 0])
    #     self.bbWeldBelwFlang_21.place(weldBelwFlangOrigin_21, uDirBelw_21, wDirBelw_21)
    #
    #     weldBelwFlangOrigin_22 = numpy.array([self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                           self.beamLeft.length / 2 + (self.beamRight.D / 2) -
    #                                           self.beamRight.T])
    #     uDirBelw_22 = numpy.array([0, 1.0, 0])
    #     wDirBelw_22 = numpy.array([-1.0, 0, 0])
    #     self.bbWeldBelwFlang_22.place(weldBelwFlangOrigin_22, uDirBelw_22, wDirBelw_22)
    #
    #     weldBelwFlangOrigin_23 = numpy.array([-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                           self.beamLeft.length / 2 - (self.beamRight.D / 2) +
    #                                           self.beamRight.T])
    #     uDirBelw_23 = numpy.array([0, 1.0, 0])
    #     wDirBelw_23 = numpy.array([1.0, 0, 0])
    #     self.bbWeldBelwFlang_23.place(weldBelwFlangOrigin_23, uDirBelw_23, wDirBelw_23)
    #
    #     weldBelwFlangOrigin_24 = numpy.array([self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                           self.beamLeft.length / 2 - (self.beamRight.D / 2) +
    #                                           self.beamRight.T])
    #     uDirBelw_24 = numpy.array([0, 1.0, 0])
    #     wDirBelw_24 = numpy.array([1.0, 0, 0])
    #     self.bbWeldBelwFlang_24.place(weldBelwFlangOrigin_24, uDirBelw_24, wDirBelw_24)
    #
    #     weldSideWebOrigin_21 = numpy.array([-self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                         self.beamLeft.length / 2 - self.bbWeldSideWeb_21.L / 2])
    #     uDirWeb_21 = numpy.array([0, 1.0, 0])
    #     wDirWeb_21 = numpy.array([0, 0, 1.0])
    #     self.bbWeldSideWeb_21.place(weldSideWebOrigin_21, uDirWeb_21, wDirWeb_21)
    #
    #     weldSideWebOrigin_22 = numpy.array([self.beamRight.t / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                         self.beamLeft.length / 2 + self.bbWeldSideWeb_21.L / 2])
    #     uDirWeb_22 = numpy.array([0, 1.0, 0])
    #     wDirWeb_22 = numpy.array([0, 0, -1.0])
    #     self.bbWeldSideWeb_22.place(weldSideWebOrigin_22, uDirWeb_22, wDirWeb_22)

    ################################################ welds for continutiy plates #########################################3
    #
    # def create_contWelds(self):
    #     contWeldL1_U2OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
    #     contWeldL1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
    #     self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)
    #
    #     contWeldL2_U2OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2, self.beamLeft.length
    #                                         - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
    #     contWeldL2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
    #     self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)
    #
    #     contWeldL1_L2OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     contWeldL1_L2_uDir = numpy.array([1.0, 0.0, 0.0])
    #     contWeldL1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
    #     self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)
    #
    #     contWeldL2_L2OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2, self.beamLeft.length
    #                                         - self.beamRight.D / 2 - self.contPlate_L1.T / 2 + self.beamRight.T / 2])
    #     contWeldL2_L2_uDir = numpy.array([1.0, 0.0, 0.0])
    #     contWeldL2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
    #     self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)
    #
    #     contWeldR1_U2OriginL = numpy.array([-self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     contWeldR1_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
    #     contWeldR1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
    #     self.contWeldR1_U2.place(contWeldR1_U2OriginL, contWeldR1_U2_uDir, contWeldR1_U2_wDir)
    #
    #     contWeldR2_U2OriginL = numpy.array([-self.beamLeft.t / 2, -self.contPlate_L1.L / 2, self.beamLeft.length
    #                                         - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     contWeldR2_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
    #     contWeldR2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
    #     self.contWeldR2_U2.place(contWeldR2_U2OriginL, contWeldR2_U2_uDir, contWeldR2_U2_wDir)
    #
    #     contWeldR1_L2OriginL = numpy.array([-self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     contWeldR1_L2_uDir = numpy.array([0.0, 0.0, -1.0])
    #     contWeldR1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
    #     self.contWeldR1_L2.place(contWeldR1_L2OriginL, contWeldR1_L2_uDir, contWeldR1_L2_wDir)
    #
    #     contWeldR2_L2OriginL = numpy.array([-self.beamLeft.t / 2, -self.contPlate_L1.L / 2, self.beamLeft.length
    #                                         - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     contWeldR2_L2_uDir = numpy.array([0.0, 0.0, -1.0])
    #     contWeldR2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
    #     self.contWeldR2_L2.place(contWeldR2_L2OriginL, contWeldR2_L2_uDir, contWeldR2_L2_wDir)
    #
    #     contWeldL1_U3OriginL = numpy.array([self.beamLeft.t / 2, self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length + (
    #                                                 self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     uDircontWeldL1_U3 = numpy.array([0, 0.0, 1.0])
    #     wDircontWeldL1_U3 = numpy.array([1.0, 0, 0])
    #     self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)
    #
    #     contWeldL1_L3OriginL = numpy.array([self.beamLeft.t / 2, self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  + (
    #                                                 self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     uDircontWeldL1_L3 = numpy.array([0, -1.0, 0.0])
    #     wDircontWeldL1_L3 = numpy.array([1.0, 0, 0])
    #     self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)
    #
    #     contWeldR2_U3OriginL = numpy.array([-self.beamLeft.B / 2, self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  - (
    #                                                 self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])  # TODO: shuffel it with R2_U3
    #     uDircontWeldR2_U3 = numpy.array([0, 0.0, 1.0])
    #     wDircontWeldR2_U3 = numpy.array([1.0, 0, 0])
    #     self.contWeldR2_U3.place(contWeldR2_U3OriginL, uDircontWeldR2_U3, wDircontWeldR2_U3)
    #
    #     contWeldL2_L3OriginL = numpy.array([self.beamLeft.t / 2, self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length - (
    #                                                 self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
    #     wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
    #     self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)
    #
    #     contWeldR1_U3OriginL = numpy.array([-self.beamLeft.B / 2, self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  + (
    #                                                 self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     uDircontWeldR1_U3 = numpy.array([0, 0.0, 1.0])
    #     wDircontWeldR1_U3 = numpy.array([1.0, 0, 0])
    #     self.contWeldR1_U3.place(contWeldR1_U3OriginL, uDircontWeldR1_U3, wDircontWeldR1_U3)
    #
    #     contWeldR1_L3OriginL = numpy.array([-self.beamLeft.B / 2, self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length + (
    #                                                 self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     uDircontWeldR1_L3 = numpy.array([0, -1.0, 0.0])
    #     wDircontWeldR1_L3 = numpy.array([1.0, 0, 0])
    #     self.contWeldR1_L3.place(contWeldR1_L3OriginL, uDircontWeldR1_L3, wDircontWeldR1_L3)
    #
    #     contWeldL2_U3OriginL = numpy.array([self.beamLeft.t / 2, self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  - (
    #                                                 self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
    #     wDircontWeldL2_U3 = numpy.array([1.0, 0, 0])
    #     self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)
    #
    #     contWeldR2_L3OriginL = numpy.array([-self.beamLeft.B / 2, self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  - (
    #                                                 self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
    #     wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
    #     self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)
    #
    #     contWeldL1_U1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  + (
    #                                                 self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     uDircontWeldL1_U1 = numpy.array([0, 1.0, 0.0])
    #     wDircontWeldL1_U1 = numpy.array([1.0, 0, 0])
    #     self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)
    #
    #     contWeldL1_L1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     uDircontWeldL1_L1 = numpy.array([0, 0.0, -1.0])
    #     wDircontWeldL1_L1 = numpy.array([1.0, 0, 0])
    #     self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)
    #
    #     contWeldL2_U1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  - (
    #                                                 self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     uDircontWeldL2_U1 = numpy.array([0, 1.0, 0.0])
    #     wDircontWeldL2_U1 = numpy.array([1.0, 0, 0])
    #     self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)
    #
    #     contWeldR2_L1OriginL = numpy.array([-self.beamLeft.B / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  - (
    #                                                 self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     uDircontWeldR2_L1 = numpy.array([0, 0.0, -1.0])
    #     wDircontWeldR2_L1 = numpy.array([1.0, 0, 0])
    #     self.contWeldR2_L1.place(contWeldR2_L1OriginL, uDircontWeldR2_L1, wDircontWeldR2_L1)
    #
    #     contWeldR1_U1OriginL = numpy.array([- self.beamLeft.B / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  + (
    #                                                 self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     uDircontWeldR1_U1 = numpy.array([0, 1.0, 0])
    #     wDircontWeldR1_U1 = numpy.array([1.0, 0, 0])
    #     self.contWeldR1_U1.place(contWeldR1_U1OriginL, uDircontWeldR1_U1, wDircontWeldR1_U1)
    #
    #     contWeldR1_L1OriginL = numpy.array([-self.beamLeft.B / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  + (
    #                                                 self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     uDircontWeldR1_L1 = numpy.array([0, 0, -1.0])
    #     wDircontWeldR1_L1 = numpy.array([1.0, 0, 0])
    #     self.contWeldR1_L1.place(contWeldR1_L1OriginL, uDircontWeldR1_L1, wDircontWeldR1_L1)
    #
    #     contWeldR2_U1OriginL = numpy.array([-self.beamLeft.B / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  - (
    #                                                 self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
    #     uDircontWeldR2_U1 = numpy.array([0, 1.0, 0])
    #     wDircontWeldR2_U1 = numpy.array([1.0, 0, 0])
    #     self.contWeldR2_U1.place(contWeldR2_U1OriginL, uDircontWeldR2_U1, wDircontWeldR2_U1)
    #
    #     contWeldL2_L1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
    #                                         self.beamLeft.length  - (
    #                                                 self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
    #     uDircontWeldL2_L1 = numpy.array([0, 0, -1.0])
    #     wDircontWeldL2_L1 = numpy.array([1.0, 0, 0])
    #     self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

    ############### Weld for the beam stiffeners ##################################
    # def create_bcWeldStiff(self):
    #     weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                           self.beamLeft.length  + self.beamRight.D / 2 + self.beam_stiffener_1.W])
    #     uDirStiffHL_1 = numpy.array([0, 1.0, 0])
    #     wDirStiffHL_1 = numpy.array([0, 0, -1.0])
    #     self.bcWeldStiffHL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)
    #
    #     weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                           self.beamLeft.length  - self.beamRight.D / 2 - self.beam_stiffener_1.L22])
    #     uDirStiffHL_1 = numpy.array([0, 1.0, 0])
    #     wDirStiffHL_1 = numpy.array([0, 0, -1.0])
    #     self.bcWeldStiffHL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)
    #
    #     weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                           self.beamLeft.length + self.beamRight.D / 2 + self.beam_stiffener_1.L22])
    #     uDirStiffHL_1 = numpy.array([0, 1.0, 0])
    #     wDirStiffHL_1 = numpy.array([0, 0, 1.0])
    #     self.bcWeldStiffHR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)
    #
    #     weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
    #                                           self.beamLeft.length - self.beamRight.D / 2 - self.beam_stiffener_1.W])
    #     uDirStiffHL_1 = numpy.array([0, 1.0, 0])
    #     wDirStiffHL_1 = numpy.array([0, 0, 1.0])
    #     self.bcWeldStiffHR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)
    #
    #     weldStiffWebOriginHL_1 = numpy.array(
    #         [self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L,
    #          self.beamLeft.length  + self.beamRight.D / 2])
    #     uDirStiffHL_1 = numpy.array([1, 0.0, 0])
    #     wDirStiffHL_1 = numpy.array([0, -1.0, 0.0])
    #     self.bcWeldStiffLL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)
    #
    #     weldStiffWebOriginHL_1 = numpy.array(
    #         [self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L22,
    #          self.beamLeft.length  - self.beamRight.D / 2])
    #     uDirStiffHL_1 = numpy.array([1.0, 0.0, 0.0])
    #     wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
    #     self.bcWeldStiffLL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)
    #
    #     weldStiffWebOriginHL_1 = numpy.array(
    #         [-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L22,
    #          self.beamLeft.length  + self.beamRight.D / 2])
    #     uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
    #     wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
    #     self.bcWeldStiffLR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)
    #
    #     weldStiffWebOriginHL_1 = numpy.array(
    #         [-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L,
    #          self.beamLeft.length  - self.beamRight.D / 2])
    #     uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
    #     wDirStiffHL_1 = numpy.array([0.0, -1.0, 0.0])
    #     self.bcWeldStiffLR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    #############################################################################################################
    #   Following functions returns the CAD model to the function display_3DModel of main file                  #
    #############################################################################################################

    def get_column_models(self):
        final_column = self.beamLModel
        bolt_list = self.nut_bolt_array.get_bolt_list()
        for bolt in bolt_list[:]:
            final_column = BRepAlgoAPI_Cut(final_column, bolt).Shape()  # TODO: Anand #cuts the colum in section shape
        return final_column

    def get_beam_models(self):
        return self.beamRModel

    def get_connector_models(self):
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                return [self.plateRModel, self.beam_stiffener_1Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:
                return [self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,
        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                return [self.plateRModel,
                        self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffHR_2Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                        self.bcWeldStiffLR_2Model,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:
                return [self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,self.beam_stiffener_2Model,

        elif self.endplate_type == "flush":
            return [self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                    self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model, self.contWeldL2_L2Model,
                    self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model, self.contWeldR2_L2Model,
                    self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                    self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                    self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                    self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model, self.contWeldL2_U1Model,
                    self.contWeldL2_L1Model,
                    self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model, self.contWeldR2_L1Model
                    ] + self.nut_bolt_array.get_models()

    def get_models(self):
        '''Returning 3D models
        '''

        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                return [self.beamLModel, self.beamRModel, self.plateRModel, self.beam_stiffener_1Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,
        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffHR_2Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                        self.bcWeldStiffLR_2Model,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,self.beam_stiffener_2Model,

        elif self.endplate_type == "flush":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                    self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model, self.contWeldL2_L2Model,
                    self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model, self.contWeldR2_L2Model,
                    self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                    self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                    self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                    self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model, self.contWeldL2_U1Model,
                    self.contWeldL2_L1Model,
                    self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model, self.contWeldR2_L1Model
                    ] + self.nut_bolt_array.get_models()


class CADColWebFillet(CADFillet):

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, self.columnLeft.D / 2 - self.columnLeft.t / 2, 0.0])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.columnLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

        ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        beamOriginL = numpy.array(
            [0.0, self.columnLeft.D / 2 - self.columnLeft.t - self.contPlate_L1.W / 2,
             self.columnLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array(
            [0.0, self.columnLeft.D / 2 - self.columnLeft.t - self.contPlate_L2.W / 2,
             self.columnLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contWelds(self):
        contWeldL1_U2OriginL = numpy.array([-self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.t,
                                            self.columnLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([1.0, 0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        contWeldL2_U2OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.t, self.columnLeft.length / 2
             - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        contWeldL1_L2OriginL = numpy.array([-self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.t,
                                            self.columnLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        contWeldL2_L2OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.t, self.columnLeft.length / 2
             - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL2_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        contWeldL1_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.t,
                                            self.columnLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0.0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([0.0, -1, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        contWeldL1_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.t,
                                            self.columnLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([-1, 0, 0.0])
        wDircontWeldL1_L3 = numpy.array([0.0, -1.0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        contWeldL2_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.t,
                                            self.columnLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([0, -1, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        contWeldL2_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.t,
                                            self.columnLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([-1, 0.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([0.0, -1, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        contWeldL1_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.B / 2 - self.columnLeft.t / 2,
             self.columnLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL1_U1 = numpy.array([0.0, 1, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        contWeldL1_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.B / 2 - self.columnLeft.t / 2,
             self.columnLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL1_L1 = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        contWeldL2_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.B / 2 - self.columnLeft.t / 2,
             self.columnLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL2_U1 = numpy.array([0, 1, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        contWeldL2_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.columnLeft.D / 2 - self.columnLeft.B / 2 - self.columnLeft.t / 2,
             self.columnLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL2_L1 = numpy.array([0.0, 1.0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

        #############################################################################################################
        #   Following functions returns the CAD model to the function display_3DModel of main file                  #
        #############################################################################################################

    def get_connector_models(self):
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                eturn[self.plateRModel,
                      self.beam_stiffener_1Model,
                      self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                      self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                      self.contPlate_L1Model, self.contPlate_L2Model,
                      self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                      self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                      self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                      self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                      self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                      self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                      self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                      self.contWeldL2_U1Model, self.contWeldL2_L1Model
                ] + self.nut_bolt_array.get_models()

            else:
                return [self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,

        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                return [self.plateRModel,
                        self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffHR_2Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                        self.bcWeldStiffLR_2Model,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()

            else:
                return [self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,self.beam_stiffener_2Model,

        elif self.endplate_type == "flush":
            return [self.plateRModel,

                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                    self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                    self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                    self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                    self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                    self.contWeldL2_U1Model, self.contWeldL2_L1Model
                    ] + self.nut_bolt_array.get_models()

    def get_models(self):
        '''Returning 3D models
        '''

        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                eturn[self.beamLModel, self.beamRModel, self.plateRModel,
                      self.beam_stiffener_1Model,
                      self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                      self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                      self.contPlate_L1Model, self.contPlate_L2Model,
                      self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                      self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                      self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                      self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                      self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                      self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                      self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                      self.contWeldL2_U1Model, self.contWeldL2_L1Model
                ] + self.nut_bolt_array.get_models()

            else:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,

        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffHR_2Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                        self.bcWeldStiffLR_2Model,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()

            else:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                        self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                        self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,self.beam_stiffener_2Model,

        elif self.endplate_type == "flush":
            return [self.beamLModel, self.beamRModel, self.plateRModel,

                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bbWeldAbvFlang_21Model, self.bbWeldAbvFlang_22Model, self.bbWeldBelwFlang_21Model,
                    self.bbWeldBelwFlang_22Model, self.bbWeldBelwFlang_23Model, self.bbWeldBelwFlang_24Model,
                    self.bbWeldSideWeb_21Model, self.bbWeldSideWeb_22Model,
                    self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                    self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                    self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                    self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                    self.contWeldL2_U1Model, self.contWeldL2_L1Model
                    ] + self.nut_bolt_array.get_models()


class CADGroove(object):

    def __init__(self, beamLeft, beamRight, plateRight, nut_bolt_array, bolt, bcWeldFlang, bcWeldWeb,
                 bcWeldStiffHeight, bcWeldStiffLength, contWeldD, contWeldB,
                 contPlates, beam_stiffeners, endplate_type, outputobj):

        # Initializing the arguments
        self.beamLeft = beamLeft  # beamLeft represents the column
        self.beamRight = beamRight
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.bolt = bolt
        self.contPlate_L1 = contPlates
        self.contPlate_L2 = copy.deepcopy(contPlates)
        self.contPlate_R1 = copy.deepcopy(contPlates)
        self.contPlate_R2 = copy.deepcopy(contPlates)
        self.beam_stiffener_1 = beam_stiffeners
        self.beam_stiffener_2 = copy.deepcopy(beam_stiffeners)
        self.endplate_type = endplate_type
        self.outputobj = outputobj
        self.numberOfBolts = int(outputobj["Bolt"]["NumberOfBolts"])
        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection
        # self.Lv = float(outputobj["Bolt"]["Lv"])

        self.boltProjection = float(outputobj["Bolt"]['projection'])  # gives the bolt projection d

        # Weld above flange for left and right beam
        self.bcWeldFlang_1 = bcWeldFlang
        self.bcWeldFlang_2 = copy.deepcopy(bcWeldFlang)
        self.bcWeldWeb_3 = copy.deepcopy(bcWeldWeb)

        self.bcWeldStiffHL_1 = bcWeldStiffHeight
        self.bcWeldStiffHL_2 = copy.deepcopy(bcWeldStiffHeight)
        self.bcWeldStiffHR_1 = copy.deepcopy(bcWeldStiffHeight)
        self.bcWeldStiffHR_2 = copy.deepcopy(bcWeldStiffHeight)

        self.bcWeldStiffLL_1 = bcWeldStiffLength
        self.bcWeldStiffLL_2 = copy.deepcopy(bcWeldStiffLength)
        self.bcWeldStiffLR_1 = copy.deepcopy(bcWeldStiffLength)
        self.bcWeldStiffLR_2 = copy.deepcopy(bcWeldStiffLength)

        self.contWeldL1_U2 = contWeldD
        self.contWeldL2_U2 = copy.deepcopy(contWeldD)
        self.contWeldL1_L2 = copy.deepcopy(contWeldD)
        self.contWeldL2_L2 = copy.deepcopy(contWeldD)
        self.contWeldR1_U2 = copy.deepcopy(contWeldD)
        self.contWeldR2_U2 = copy.deepcopy(contWeldD)
        self.contWeldR1_L2 = copy.deepcopy(contWeldD)
        self.contWeldR2_L2 = copy.deepcopy(contWeldD)
        self.contWeldL1_U3 = contWeldB
        self.contWeldL1_L3 = copy.deepcopy(contWeldB)
        self.contWeldL2_U3 = copy.deepcopy(contWeldB)
        self.contWeldL2_L3 = copy.deepcopy(contWeldB)
        self.contWeldR1_U3 = copy.deepcopy(contWeldB)
        self.contWeldR1_L3 = copy.deepcopy(contWeldB)
        self.contWeldR2_U3 = copy.deepcopy(contWeldB)
        self.contWeldR2_L3 = copy.deepcopy(contWeldB)
        self.contWeldL1_U1 = copy.deepcopy(contWeldB)
        self.contWeldL1_L1 = copy.deepcopy(contWeldB)
        self.contWeldL2_U1 = copy.deepcopy(contWeldB)
        self.contWeldL2_L1 = copy.deepcopy(contWeldB)
        self.contWeldR1_U1 = copy.deepcopy(contWeldB)
        self.contWeldR1_L1 = copy.deepcopy(contWeldB)
        self.contWeldR2_U1 = copy.deepcopy(contWeldB)
        self.contWeldR2_L1 = copy.deepcopy(contWeldB)

    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.create_contPlatesGeometry()

        self.create_beam_stiffenersGeometry()

        self.create_bcWelds()

        self.create_bcWeldStiff()

        self.create_contWelds()

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

        self.bcWeldFlang_1Model = self.bcWeldFlang_1.create_model()
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
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.bcWeldWeb_3.b
        beamOriginR = numpy.array([0.0, gap, self.beamLeft.length / 2])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plateRight.T + self.beamLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.beamLeft.length / 2 + (
                    self.plateRight.L / 2 - self.boltProjection - self.beamRight.D / 2)])  # TODO #Add weld thickness here
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:  # self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plateRight.T + self.beamLeft.D / 2
            plateOriginR = numpy.array([-self.plateRight.W / 2, gap, self.beamLeft.length / 2])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0, self.plateRight.T / 2, + (
                    self.plateRight.L / 2)])  # self.plateRight.L/2+ (self.plateRight.L/2 - (10) - self.beamRight.D /2) - 40#TODO add end distance here #self.plateRight.L/2 + (self.plateRight.L/2 - (10 + 8) - self.beamRight.D /2)
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array(
                [0.0, self.plateRight.T / 2, self.plateRight.L / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array(
                [0.0, self.plateRight.T / 2, self.beamRight.D / 2])  # TODO Add self.Lv instead of 25
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        beamOriginL = numpy.array([self.beamLeft.B / 2 - self.contPlate_L1.W / 2, 0.0,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([self.beamLeft.B / 2 - self.contPlate_L2.W / 2, 0.0,
                                   self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-self.beamLeft.B / 2 + self.contPlate_R1.W / 2, 0.0,
                                   self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_R1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-self.beamLeft.B / 2 + self.contPlate_R2.W / 2, 0.0,
                                   self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_R2.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R2.place(beamOriginL, beamL_uDir, beamL_wDir)

    ##############################################  Adding beam stiffeners #############################################
    def create_beam_stiffenersGeometry(self):
        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                        self.beamLeft.length / 2 + self.beamRight.D / 2 + self.beam_stiffener_1.W / 2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

        gap = self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                        self.beamLeft.length / 2 - self.beamRight.D / 2 - self.beam_stiffener_1.W / 2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    ##############################################  creating weld sections ########################################

    def create_bcWelds(self):
        weldFlangOrigin_1 = numpy.array(
            [-self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T + self.bcWeldWeb_3.b / 2,
             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2])
        uDir_1 = numpy.array([0, 1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bcWeldFlang_1.place(weldFlangOrigin_1, uDir_1, wDir_1)

        weldFlangOrigin_2 = numpy.array(
            [self.beamRight.B / 2, self.beamLeft.D / 2 + self.plateRight.T + self.bcWeldWeb_3.b / 2,
             self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2])
        uDir_2 = numpy.array([0, 1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bcWeldFlang_2.place(weldFlangOrigin_2, uDir_2, wDir_2)

        weldWebOrigin_3 = numpy.array([0.0, self.beamLeft.D / 2 + self.plateRight.T + self.bcWeldWeb_3.b / 2,
                                       self.beamLeft.length / 2 - self.bcWeldWeb_3.L / 2])
        uDirWeb_3 = numpy.array([0, 1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bcWeldWeb_3.place(weldWebOrigin_3, uDirWeb_3, wDirWeb_3)

    def create_bcWeldStiff(self):
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 + self.beamRight.D / 2 + self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 - self.beamRight.D / 2 - self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 + self.beamRight.D / 2 + self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T,
                                              self.beamLeft.length / 2 - self.beamRight.D / 2 - self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L,
             self.beamLeft.length / 2 + self.beamRight.D / 2])
        uDirStiffHL_1 = numpy.array([1, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0, -1.0, 0.0])
        self.bcWeldStiffLL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L22,
             self.beamLeft.length / 2 - self.beamRight.D / 2])
        uDirStiffHL_1 = numpy.array([1.0, 0.0, 0.0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L22,
             self.beamLeft.length / 2 + self.beamRight.D / 2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, self.beamLeft.D / 2 + self.plateRight.T + self.beam_stiffener_1.L,
             self.beamLeft.length / 2 - self.beamRight.D / 2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bcWeldStiffLR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    ####################################### welding continuity plates with fillet weld##################################

    def create_contWelds(self):
        contWeldL1_U2OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        contWeldL2_U2OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2, self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        contWeldL1_L2OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        contWeldL2_L2OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2, self.beamLeft.length / 2
                                            - self.beamRight.D / 2 - self.contPlate_L1.T / 2 + self.beamRight.T / 2])
        contWeldL2_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        contWeldR1_U2OriginL = numpy.array([-self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldR1_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_U2.place(contWeldR1_U2OriginL, contWeldR1_U2_uDir, contWeldR1_U2_wDir)

        contWeldR2_U2OriginL = numpy.array([-self.beamLeft.t / 2, -self.contPlate_L1.L / 2, self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldR2_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_U2.place(contWeldR2_U2OriginL, contWeldR2_U2_uDir, contWeldR2_U2_wDir)

        contWeldR1_L2OriginL = numpy.array([-self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldR1_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_L2.place(contWeldR1_L2OriginL, contWeldR1_L2_uDir, contWeldR1_L2_wDir)

        contWeldR2_L2OriginL = numpy.array([-self.beamLeft.t / 2, -self.contPlate_L1.L / 2, self.beamLeft.length / 2
                                            - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldR2_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_L2.place(contWeldR2_L2OriginL, contWeldR2_L2_uDir, contWeldR2_L2_wDir)

        contWeldL1_U3OriginL = numpy.array([self.beamLeft.t / 2, self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        contWeldL1_L3OriginL = numpy.array([self.beamLeft.t / 2, self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        contWeldR2_U3OriginL = numpy.array([-self.beamLeft.B / 2, self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])  # TODO: shuffel it with R2_U3
        uDircontWeldR2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U3.place(contWeldR2_U3OriginL, uDircontWeldR2_U3, wDircontWeldR2_U3)

        contWeldL2_L3OriginL = numpy.array([self.beamLeft.t / 2, self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        contWeldR1_U3OriginL = numpy.array([-self.beamLeft.B / 2, self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U3.place(contWeldR1_U3OriginL, uDircontWeldR1_U3, wDircontWeldR1_U3)

        contWeldR1_L3OriginL = numpy.array([-self.beamLeft.B / 2, self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L3.place(contWeldR1_L3OriginL, uDircontWeldR1_L3, wDircontWeldR1_L3)

        contWeldL2_U3OriginL = numpy.array([self.beamLeft.t / 2, self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        contWeldR2_L3OriginL = numpy.array([-self.beamLeft.B / 2, self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)

        contWeldL1_U1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        contWeldL1_L1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldL1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        contWeldL2_U1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        contWeldR2_L1OriginL = numpy.array([-self.beamLeft.B / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR2_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldR2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L1.place(contWeldR2_L1OriginL, uDircontWeldR2_L1, wDircontWeldR2_L1)

        contWeldR1_U1OriginL = numpy.array([- self.beamLeft.B / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR1_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U1.place(contWeldR1_U1OriginL, uDircontWeldR1_U1, wDircontWeldR1_U1)

        contWeldR1_L1OriginL = numpy.array([-self.beamLeft.B / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR1_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldR1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L1.place(contWeldR1_L1OriginL, uDircontWeldR1_L1, wDircontWeldR1_L1)

        contWeldR2_U1OriginL = numpy.array([-self.beamLeft.B / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR2_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U1.place(contWeldR2_U1OriginL, uDircontWeldR2_U1, wDircontWeldR2_U1)

        contWeldL2_L1OriginL = numpy.array([self.beamLeft.t / 2, -self.contPlate_L1.L / 2,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldL2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

    #############################################################################################################
    #   Following functions returns the CAD model to the function display_3DModel of main file                  #
    #############################################################################################################

    def get_column_models(self):
        final_column = self.beamLModel
        bolt_list = self.nut_bolt_array.get_bolt_list()
        for bolt in bolt_list[:]:
            final_column = BRepAlgoAPI_Cut(final_column, bolt).Shape()  # TODO: Anand #cuts the colum in section shape
        return final_column

    def get_beam_models(self):
        return self.beamRModel

    def get_connector_models(self):
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                return [self.plateRModel,
                        self.beam_stiffener_1Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:

                return [self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model, self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,

        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                return [self.plateRModel,
                        self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffHR_2Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                        self.bcWeldStiffLR_2Model,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:

                return [self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,self.beam_stiffener_2Model,
        elif self.endplate_type == "flush":
            return [self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model,
                    self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model, self.contWeldL2_L2Model,
                    self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model, self.contWeldR2_L2Model,
                    self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                    self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                    self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                    self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model, self.contWeldL2_U1Model,
                    self.contWeldL2_L1Model,
                    self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model, self.contWeldR2_L1Model
                    ] + self.nut_bolt_array.get_models()

    def get_models(self):
        '''Returning 3D models
        '''

        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.beam_stiffener_1Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:

                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model, self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,

        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffHR_2Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                        self.bcWeldStiffLR_2Model,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:

                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model,
                        self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                        self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                        self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                        self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                        self.contWeldR2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,self.beam_stiffener_2Model,
        elif self.endplate_type == "flush":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model,
                    self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model, self.contWeldL2_L2Model,
                    self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model, self.contWeldR2_L2Model,
                    self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                    self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                    self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                    self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model, self.contWeldL2_U1Model,
                    self.contWeldL2_L1Model,
                    self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model, self.contWeldR2_L1Model
                    ] + self.nut_bolt_array.get_models()


class CADcolwebGroove(CADGroove):
    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0, self.beamLeft.D / 2 - self.beamLeft.t / 2, 0.0])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

        ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D / 2 - self.beamLeft.t - self.contPlate_L1.W / 2,
             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array(
            [0.0, self.beamLeft.D / 2 - self.beamLeft.t - self.contPlate_L2.W / 2,
             self.beamLeft.length / 2 - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contWelds(self):
        contWeldL1_U2OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.t,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([1.0, 0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        contWeldL2_U2OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.t, self.beamLeft.length / 2
             - self.beamRight.D / 2 + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        contWeldL1_L2OriginL = numpy.array([-self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.t,
                                            self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        contWeldL2_L2OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.t, self.beamLeft.length / 2
             - self.beamRight.D / 2 + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        contWeldL2_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        contWeldL1_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.t,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0.0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([0.0, -1, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        contWeldL1_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.t,
                                            self.beamLeft.length / 2 + (
                                                    self.beamRight.D / 2) - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([-1, 0, 0.0])
        wDircontWeldL1_L3 = numpy.array([0.0, -1.0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        contWeldL2_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.t,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([0, -1, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        contWeldL2_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.t,
                                            self.beamLeft.length / 2 - (
                                                    self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([-1, 0.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([0.0, -1, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        contWeldL1_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.B / 2 - self.beamLeft.t / 2,
             self.beamLeft.length / 2 + (self.beamRight.D / 2) - self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL1_U1 = numpy.array([0.0, 1, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        contWeldL1_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.B / 2 - self.beamLeft.t / 2,
             self.beamLeft.length / 2 + self.beamRight.D / 2 - self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL1_L1 = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        contWeldL2_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.B / 2 - self.beamLeft.t / 2,
             self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL2_U1 = numpy.array([0, 1, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        contWeldL2_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.beamLeft.D / 2 - self.beamLeft.B / 2 - self.beamLeft.t / 2,
             self.beamLeft.length / 2 - (self.beamRight.D / 2) + self.beamRight.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL2_L1 = numpy.array([0.0, 1.0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

    def get_connector_models(self):
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                return [self.plateRModel,
                        self.beam_stiffener_1Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:
                return [self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model, self.contWeldL1_U2Model, self.contWeldL2_U2Model,
                        self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model,
                        self.contWeldL2_L1Model] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,
        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                return [self.plateRModel,
                        self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffHR_2Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                        self.bcWeldStiffLR_2Model,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:
                return [self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,self.beam_stiffener_2Model,
        elif self.endplate_type == "flush":
            return [self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model,
                    self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                    self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                    self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                    self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                    self.contWeldL2_U1Model, self.contWeldL2_L1Model
                    ] + self.nut_bolt_array.get_models()

    def get_models(self):
        '''Returning 3D models
        '''

        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.beam_stiffener_1Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model, self.contWeldL1_U2Model, self.contWeldL2_U2Model,
                        self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model,
                        self.contWeldL2_L1Model] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,
        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                        self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                        self.bcWeldStiffHR_2Model,
                        self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                        self.bcWeldStiffLR_2Model,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()
            else:
                return [self.beamLModel, self.beamRModel, self.plateRModel,
                        self.contPlate_L1Model, self.contPlate_L2Model,
                        self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                        self.bcWeldWeb_3Model,
                        self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                        self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                        self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                        self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                        self.contWeldL2_U1Model, self.contWeldL2_L1Model
                        ] + self.nut_bolt_array.get_models()  # self.beam_stiffener_1Model,self.beam_stiffener_2Model,
        elif self.endplate_type == "flush":
            return [self.beamLModel, self.beamRModel, self.plateRModel,
                    self.contPlate_L1Model, self.contPlate_L2Model,
                    self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                    self.bcWeldWeb_3Model,
                    self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                    self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                    self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                    self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                    self.contWeldL2_U1Model, self.contWeldL2_L1Model
                    ] + self.nut_bolt_array.get_models()
