"""
Initialized on 23-04-2019
Commenced on 24-04-2019
@author: Anand Swaroop
"""""

import numpy
import copy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse


class CADFillet(object):
    def __init__(self, column, beam, plate, nut_bolt_array, bolt, bcWeldAbvFlang,
                 bcWeldBelwFlang, bcWeldSideWeb, contWeldD, contWeldB, bcWeldStiffHeight, bcWeldStiffLength,
                 contPlates, beam_stiffeners, endplate_type, conn_type, outputobj):
        """

        :param column: Column
        :param beam: Beam
        :param plate: extended plate
        :param nut_bolt_array: Bolt placement on the end plates
        :param bolt: bolt
        :param bcWeldAbvFlang: Weld surface on the outer side of flange
        :param bcWeldBelwFlang: Weld surface on the inner side of flange
        :param bcWeldSideWeb: Weld surface on the sides of the web
        :param contWeldD: Weld surface on the continuity plate along the depth 'D' of column
        :param contWeldB: Weld surface on the continuity plate along the bredth 'B' of column
        :param bcWeldStiffHeight: Weld surface along the height of the stiffeners
        :param bcWeldStiffLength: Weld surface along the length of the stiffeners
        :param contPlates: Continuity plates in the column section
        :param beam_stiffeners: Stiffeners for the enxtended and one-way endplate
        :param endplate_type: type of endplate i.e extended both ways, one-way or flushed
        :param conn_type: connection type, similiar to above?(#TODO: check it if it is necessory)
        :param outputobj: Output dictionary
        """

        # Initializing the arguments
        self.column = column  # beamLeft represents the column
        self.beam = beam
        self.plate = plate
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
        self.bcWeldAbvFlang_21 = bcWeldAbvFlang  # Right beam upper side
        self.bcWeldAbvFlang_22 = copy.deepcopy(bcWeldAbvFlang)  # Right beam lower side

        self.bcWeldBelwFlang_21 = bcWeldBelwFlang  # behind bcWeldBelwFlang_11
        self.bcWeldBelwFlang_22 = copy.deepcopy(bcWeldBelwFlang)  # behind bcWeldBelwFlang_12
        self.bcWeldBelwFlang_23 = copy.deepcopy(bcWeldBelwFlang)  # behind bcWeldBelwFlang_13
        self.bcWeldBelwFlang_24 = copy.deepcopy(bcWeldBelwFlang)  # behind bcWeldBelwFlang_14

        self.bcWeldSideWeb_21 = bcWeldSideWeb  # Behind bcWeldSideWeb_11
        self.bcWeldSideWeb_22 = copy.deepcopy(bcWeldSideWeb)  # Behind bcWeldSideWeb_12

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
        :return: CAD model of each entity
        """
        self.createColumnGeometry()
        self.createBeamGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.create_contPlatesGeometry()
        self.create_beam_stiffenersGeometry()
        # self.create_beam_stiffener_2Geometry()

        self.create_bcWelds()  # left beam above flange weld

        self.create_contWelds()

        self.create_bcWeldStiff()

        # call for create_model of filletweld from Components directory
        self.columnModel = self.column.create_model()
        self.beamModel = self.beam.create_model()
        self.plateModel = self.plate.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        self.contPlate_L1Model = self.contPlate_L1.create_model()
        self.contPlate_L2Model = self.contPlate_L2.create_model()
        self.contPlate_R1Model = self.contPlate_R1.create_model()
        self.contPlate_R2Model = self.contPlate_R2.create_model()
        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()

        self.bcWeldAbvFlang_21Model = self.bcWeldAbvFlang_21.create_model()
        self.bcWeldAbvFlang_22Model = self.bcWeldAbvFlang_22.create_model()

        self.bcWeldBelwFlang_21Model = self.bcWeldBelwFlang_21.create_model()
        self.bcWeldBelwFlang_22Model = self.bcWeldBelwFlang_22.create_model()
        self.bcWeldBelwFlang_23Model = self.bcWeldBelwFlang_23.create_model()
        self.bcWeldBelwFlang_24Model = self.bcWeldBelwFlang_24.create_model()

        self.bcWeldSideWeb_21Model = self.bcWeldSideWeb_21.create_model()
        self.bcWeldSideWeb_22Model = self.bcWeldSideWeb_22.create_model()

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

    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        # if self.conn_type == 'col_flange_connectivity':
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamGeometry(self):
        """

        :return: Geometric Orientation of this component
        """

        gap = self.column.D / 2 + self.plate.T
        beamOriginR = numpy.array([0.0, gap, self.column.length / 2])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beam.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):
        """

        :return: Geometric Orientation of this component
        """

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plate.T + self.column.D / 2
            plateOriginR = numpy.array([-self.plate.W / 2, gap, self.column.length / 2 + (
                    self.plate.L / 2 - self.boltProjection - self.beam.D / 2)])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plate.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:  # self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plate.T + self.column.D / 2
            plateOriginR = numpy.array([-self.plate.W / 2, gap, self.column.length / 2])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plate.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        """

        :return: Geometric Orientation of this component
        """

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array(
                [0.0, self.plate.T / 2, + (self.plate.L / 2)])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array(
                [0.0, self.plate.T / 2, self.plate.L / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array(
                [0.0, self.plate.T / 2, self.beam.D / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        beamOriginL = numpy.array([self.column.B / 2 - self.contPlate_L1.W / 2, 0.0,
                                   self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([self.column.B / 2 - self.contPlate_L2.W / 2, 0.0,
                                   self.column.length / 2 - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-self.column.B / 2 + self.contPlate_R1.W / 2, 0.0,
                                   self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_R1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-self.column.B / 2 + self.contPlate_R2.W / 2, 0.0,
                                   self.column.length / 2 - self.beam.D / 2 + self.beam.T / 2 - self.contPlate_R1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R2.place(beamOriginL, beamL_uDir, beamL_wDir)

    ##############################################  Adding beam stiffeners #############################################
    def create_beam_stiffenersGeometry(self):
        """

        :return: Geometric Orientation of this components
        """
        gap = self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                        self.column.length / 2 + self.beam.D / 2 + self.beam_stiffener_1.W / 2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

        gap = self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                        self.column.length / 2 - self.beam.D / 2 - self.beam_stiffener_1.W / 2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    ##############################################  creating weld sections ########################################
    def create_bcWelds(self):
        """

        :return: Geometric Orientation of this components
        """
        weldAbvFlangOrigin_21 = numpy.array([-self.beam.B / 2, self.column.D / 2 + self.plate.T,
                                             self.column.length / 2 + self.beam.D / 2])
        uDirAbv_21 = numpy.array([0, 1.0, 0])
        wDirAbv_21 = numpy.array([1.0, 0, 0])
        self.bcWeldAbvFlang_21.place(weldAbvFlangOrigin_21, uDirAbv_21, wDirAbv_21)

        weldAbvFlangOrigin_22 = numpy.array([self.beam.B / 2, self.column.D / 2 + self.plate.T,
                                             self.column.length / 2 - self.beam.D / 2])
        uDirAbv_22 = numpy.array([0, 1.0, 0])
        wDirAbv_22 = numpy.array([-1.0, 0, 0])
        self.bcWeldAbvFlang_22.place(weldAbvFlangOrigin_22, uDirAbv_22, wDirAbv_22)

        weldBelwFlangOrigin_21 = numpy.array([-self.beam.t / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 + (self.beam.D / 2) -
                                              self.beam.T])
        uDirBelw_21 = numpy.array([0, 1.0, 0])
        wDirBelw_21 = numpy.array([-1.0, 0, 0])
        self.bcWeldBelwFlang_21.place(weldBelwFlangOrigin_21, uDirBelw_21, wDirBelw_21)

        weldBelwFlangOrigin_22 = numpy.array([self.beam.B / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 + (self.beam.D / 2) -
                                              self.beam.T])
        uDirBelw_22 = numpy.array([0, 1.0, 0])
        wDirBelw_22 = numpy.array([-1.0, 0, 0])
        self.bcWeldBelwFlang_22.place(weldBelwFlangOrigin_22, uDirBelw_22, wDirBelw_22)

        weldBelwFlangOrigin_23 = numpy.array([-self.beam.B / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 - (self.beam.D / 2) +
                                              self.beam.T])
        uDirBelw_23 = numpy.array([0, 1.0, 0])
        wDirBelw_23 = numpy.array([1.0, 0, 0])
        self.bcWeldBelwFlang_23.place(weldBelwFlangOrigin_23, uDirBelw_23, wDirBelw_23)

        weldBelwFlangOrigin_24 = numpy.array([self.beam.t / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 - (self.beam.D / 2) +
                                              self.beam.T])
        uDirBelw_24 = numpy.array([0, 1.0, 0])
        wDirBelw_24 = numpy.array([1.0, 0, 0])
        self.bcWeldBelwFlang_24.place(weldBelwFlangOrigin_24, uDirBelw_24, wDirBelw_24)

        weldSideWebOrigin_21 = numpy.array([-self.beam.t / 2, self.column.D / 2 + self.plate.T,
                                            self.column.length / 2 - self.bcWeldSideWeb_21.L / 2])
        uDirWeb_21 = numpy.array([0, 1.0, 0])
        wDirWeb_21 = numpy.array([0, 0, 1.0])
        self.bcWeldSideWeb_21.place(weldSideWebOrigin_21, uDirWeb_21, wDirWeb_21)

        weldSideWebOrigin_22 = numpy.array([self.beam.t / 2, self.column.D / 2 + self.plate.T,
                                            self.column.length / 2 + self.bcWeldSideWeb_21.L / 2])
        uDirWeb_22 = numpy.array([0, 1.0, 0])
        wDirWeb_22 = numpy.array([0, 0, -1.0])
        self.bcWeldSideWeb_22.place(weldSideWebOrigin_22, uDirWeb_22, wDirWeb_22)

    ################################################ welds for continutiy plates #########################################3

    def create_contWelds(self):

        """

        :return: Geometric Orientation of this components
        """
        contWeldL1_U2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        contWeldL2_U2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        contWeldL1_L2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        contWeldL2_L2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2, self.column.length / 2
                                            - self.beam.D / 2 - self.contPlate_L1.T / 2 + self.beam.T / 2])
        contWeldL2_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        contWeldR1_U2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldR1_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_U2.place(contWeldR1_U2OriginL, contWeldR1_U2_uDir, contWeldR1_U2_wDir)

        contWeldR2_U2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldR2_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_U2.place(contWeldR2_U2OriginL, contWeldR2_U2_uDir, contWeldR2_U2_wDir)

        contWeldR1_L2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldR1_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_L2.place(contWeldR1_L2OriginL, contWeldR1_L2_uDir, contWeldR1_L2_wDir)

        contWeldR2_L2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldR2_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_L2.place(contWeldR2_L2OriginL, contWeldR2_L2_uDir, contWeldR2_L2_wDir)

        contWeldL1_U3OriginL = numpy.array([self.column.t / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        contWeldL1_L3OriginL = numpy.array([self.column.t / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        contWeldR2_U3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])  # TODO: shuffel it with R2_U3
        uDircontWeldR2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U3.place(contWeldR2_U3OriginL, uDircontWeldR2_U3, wDircontWeldR2_U3)

        contWeldL2_L3OriginL = numpy.array([self.column.t / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        contWeldR1_U3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U3.place(contWeldR1_U3OriginL, uDircontWeldR1_U3, wDircontWeldR1_U3)

        contWeldR1_L3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L3.place(contWeldR1_L3OriginL, uDircontWeldR1_L3, wDircontWeldR1_L3)

        contWeldL2_U3OriginL = numpy.array([self.column.t / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        contWeldR2_L3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)

        contWeldL1_U1OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        contWeldL1_L1OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldL1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        contWeldL2_U1OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        contWeldR2_L1OriginL = numpy.array([-self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR2_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldR2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L1.place(contWeldR2_L1OriginL, uDircontWeldR2_L1, wDircontWeldR2_L1)

        contWeldR1_U1OriginL = numpy.array([- self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR1_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U1.place(contWeldR1_U1OriginL, uDircontWeldR1_U1, wDircontWeldR1_U1)

        contWeldR1_L1OriginL = numpy.array([-self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR1_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldR1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L1.place(contWeldR1_L1OriginL, uDircontWeldR1_L1, wDircontWeldR1_L1)

        contWeldR2_U1OriginL = numpy.array([-self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR2_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U1.place(contWeldR2_U1OriginL, uDircontWeldR2_U1, wDircontWeldR2_U1)

        contWeldL2_L1OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldL2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

    ############### Weld for the beam stiffeners ##################################
    def create_bcWeldStiff(self):
        """

        :return: Geometric Orientation of this components
        """
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 + self.beam.D / 2 + self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 - self.beam.D / 2 - self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 + self.beam.D / 2 + self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 - self.beam.D / 2 - self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L,
             self.column.length / 2 + self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([1, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0, -1.0, 0.0])
        self.bcWeldStiffLL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L22,
             self.column.length / 2 - self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([1.0, 0.0, 0.0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L22,
             self.column.length / 2 + self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L,
             self.column.length / 2 - self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bcWeldStiffLR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    #############################################################################################################
    #   Following functions returns the CAD model to the function display_3DModel of main file                  #
    #############################################################################################################

    def get_column_models(self):
        """

        :return: CAD model of the column
        """

        final_column = self.columnModel
        bolt_list = self.nut_bolt_array.get_bolt_list()
        for bolt in bolt_list[:]:
            final_column = BRepAlgoAPI_Cut(final_column, bolt).Shape()  # TODO: Anand #cuts the colum in section shape
        return final_column

    def get_beam_models(self):
        """

        :return:  CAD model of the beam
        """
        return self.beamModel

    def get_plate_connector_models(self):
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.contPlate_L1Model,
                                   self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model]
            else:
                connector_plate = [self.plateModel, self.contPlate_L1Model, self.contPlate_L2Model,
                                   self.contPlate_R1Model, self.contPlate_R2Model]
        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                                   self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model,
                                   self.contPlate_R2Model]
            else:
                connector_plate = [self.plateModel, self.contPlate_L1Model, self.contPlate_L2Model,
                                   self.contPlate_R1Model, self.contPlate_R2Model]
        elif self.endplate_type == "flush":
            connector_plate = [self.plateModel,
                               self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model,
                               self.contPlate_R2Model, ]

        plates = connector_plate[0]
        for comp in connector_plate[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_welded_models(self):
        """

        :return: CAD model for all the welds
        """
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model, self.bcWeldAbvFlang_21Model,
                              self.bcWeldAbvFlang_22Model, self.bcWeldBelwFlang_21Model,
                              self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                              self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]
            else:
                welded_sec = [self.bcWeldAbvFlang_21Model, self.bcWeldAbvFlang_22Model, self.bcWeldBelwFlang_21Model,
                              self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                              self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]

        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffHR_2Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                              self.bcWeldStiffLR_2Model, self.bcWeldAbvFlang_21Model, self.bcWeldAbvFlang_22Model,
                              self.bcWeldBelwFlang_21Model,
                              self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                              self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]
            else:
                welded_sec = [self.bcWeldAbvFlang_21Model, self.bcWeldAbvFlang_22Model, self.bcWeldBelwFlang_21Model,
                              self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                              self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]

        elif self.endplate_type == "flush":
            welded_sec = [self.bcWeldAbvFlang_21Model, self.bcWeldAbvFlang_22Model, self.bcWeldBelwFlang_21Model,
                          self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                          self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                          self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                          self.contWeldL2_L2Model,
                          self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                          self.contWeldR2_L2Model,
                          self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                          self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                          self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                          self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                          self.contWeldL2_U1Model,
                          self.contWeldL2_L1Model,
                          self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                          self.contWeldR2_L1Model]

        welds = welded_sec[0]
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_nut_bolt_array_models(self):
        nut_bolts = self.nut_bolt_array.get_models()
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array

    def get_connector_models(self):
        """

        :return: CAD models of the connecting components
        """
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD

    def get_models(self):
        """

        :return: complete CAD model
        """
        columns = self.get_column_models()
        beams = self.get_beam_models()
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [columns, beams, plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD


class CADColWebFillet(CADFillet):

    def createColumnGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        beamOriginL = numpy.array([0.0, self.column.D / 2 - self.column.t / 2, 0.0])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(beamOriginL, beamL_uDir, beamL_wDir)

        ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        beamOriginL = numpy.array(
            [0.0, self.column.D / 2 - self.column.t - self.contPlate_L1.W / 2,
             self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array(
            [0.0, self.column.D / 2 - self.column.t - self.contPlate_L2.W / 2,
             self.column.length / 2 - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contWelds(self):
        """

        :return: Geometric Orientation of this components
        """
        contWeldL1_U2OriginL = numpy.array([-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([1.0, 0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        contWeldL2_U2OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t, self.column.length / 2
             - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        contWeldL1_L2OriginL = numpy.array([-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        contWeldL2_L2OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t, self.column.length / 2
             - self.beam.D / 2 + self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL2_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        contWeldL1_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0.0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([0.0, -1, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        contWeldL1_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([-1, 0, 0.0])
        wDircontWeldL1_L3 = numpy.array([0.0, -1.0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        contWeldL2_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([0, -1, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        contWeldL2_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([-1, 0.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([0.0, -1, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        contWeldL1_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.B / 2 - self.column.t / 2,
             self.column.length / 2 + (self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL1_U1 = numpy.array([0.0, 1, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        contWeldL1_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.B / 2 - self.column.t / 2,
             self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL1_L1 = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        contWeldL2_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.B / 2 - self.column.t / 2,
             self.column.length / 2 - (self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL2_U1 = numpy.array([0, 1, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        contWeldL2_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.B / 2 - self.column.t / 2,
             self.column.length / 2 - (self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL2_L1 = numpy.array([0.0, 1.0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

        #############################################################################################################
        #   Following functions returns the CAD model to the function display_3DModel of main file                  #
        #############################################################################################################

    def get_plate_connector_models(self):
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.contPlate_L1Model,
                                   self.contPlate_L2Model, ]
            else:
                connector_plate = [self.plateModel, self.contPlate_L1Model, self.contPlate_L2Model, ]
        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                                   self.contPlate_L1Model, self.contPlate_L2Model, ]
            else:
                connector_plate = [self.plateModel, self.contPlate_L1Model, self.contPlate_L2Model, ]
        elif self.endplate_type == "flush":
            connector_plate = [self.plateModel,
                               self.contPlate_L1Model, self.contPlate_L2Model, ]

        plates = connector_plate[0]
        for comp in connector_plate[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_welded_models(self):
        """

        :return: CAD model for all the welds
        """
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model, self.bcWeldAbvFlang_21Model,
                              self.bcWeldAbvFlang_22Model, self.bcWeldBelwFlang_21Model,
                              self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                              self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                              self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model]
            else:
                welded_sec = [self.bcWeldAbvFlang_21Model, self.bcWeldAbvFlang_22Model, self.bcWeldBelwFlang_21Model,
                              self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                              self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                              self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model, ]

        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffHR_2Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                              self.bcWeldStiffLR_2Model, self.bcWeldAbvFlang_21Model, self.bcWeldAbvFlang_22Model,
                              self.bcWeldBelwFlang_21Model,
                              self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                              self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                              self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model, ]
            else:
                welded_sec = [self.bcWeldAbvFlang_21Model, self.bcWeldAbvFlang_22Model, self.bcWeldBelwFlang_21Model,
                              self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                              self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                              self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model, ]

        elif self.endplate_type == "flush":
            welded_sec = [self.bcWeldAbvFlang_21Model, self.bcWeldAbvFlang_22Model, self.bcWeldBelwFlang_21Model,
                          self.bcWeldBelwFlang_22Model, self.bcWeldBelwFlang_23Model, self.bcWeldBelwFlang_24Model,
                          self.bcWeldSideWeb_21Model, self.bcWeldSideWeb_22Model,
                          self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                          self.contWeldL2_L2Model,
                          self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                          self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                          self.contWeldL1_L1Model, self.contWeldL2_U1Model,
                          self.contWeldL2_L1Model]

        welds = welded_sec[0]
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_connector_models(self):
        """

        :return: CAD models of the connecting components
        """
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD

    def get_models(self):
        """

        :return: complete CAD model
        """
        columns = self.get_column_models()
        beams = self.get_beam_models()
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [columns, beams, plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD


class CADGroove(object):

    def __init__(self, column, beam, plate, nut_bolt_array, bolt, bcWeldFlang, bcWeldWeb,
                 bcWeldStiffHeight, bcWeldStiffLength, contWeldD, contWeldB,
                 contPlates, beam_stiffeners, endplate_type, outputobj):
        """

        :param column: Column
        :param beam: Beam
        :param plate: extended plate
        :param nut_bolt_array: Bolt placement on the end plates
        :param bolt: bolt
        :param bcWeldFlang: Weld surface on side of flange
        :param bcWeldWeb: Weld surface on the side of the web
        :param bcWeldStiffHeight: Weld surface along the height of the stiffeners
        :param bcWeldStiffLength: Weld surface along the length of the stiffeners
        :param contWeldD: Weld surface on the continuity plate along the depth 'D' of column
        :param contWeldB: Weld surface on the continuity plate along the bredth 'B' of column
        :param contPlates: Continuity plates in the column section
        :param beam_stiffeners: Stiffeners for the enxtended and one-way endplate
        :param endplate_type: type of endplate i.e extended both ways, one-way or flushed
        :param outputobj: Output dictionary
        """

        # Initializing the arguments
        self.column = column  # beamLeft represents the column
        self.beam = beam
        self.plate = plate
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
        :return: CAD model of each entity
        """
        self.createBeamLGeometry()
        self.createBeamGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        self.create_contPlatesGeometry()

        self.create_beam_stiffenersGeometry()

        self.create_bcWelds()

        self.create_bcWeldStiff()

        self.create_contWelds()

        # call for create_model of filletweld from Components directory
        self.columnModel = self.column.create_model()
        self.beamModel = self.beam.create_model()
        self.plateModel = self.plate.create_model()
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
        """

        :return: Geometric Orientation of this component
        """
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        gap = self.column.D / 2 + self.plate.T + self.bcWeldWeb_3.b
        beamOriginR = numpy.array([0.0, gap, self.column.length / 2])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beam.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):
        """

        :return: Geometric Orientation of this component
        """

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plate.T + self.column.D / 2
            plateOriginR = numpy.array([-self.plate.W / 2, gap, self.column.length / 2 + (
                    self.plate.L / 2 - self.boltProjection - self.beam.D / 2)])  # TODO #Add weld thickness here
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plate.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:  # self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plate.T + self.column.D / 2
            plateOriginR = numpy.array([-self.plate.W / 2, gap, self.column.length / 2])
            plateR_uDir = numpy.array([0.0, 1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plate.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        """

        :return: Geometric Orientation of this component
        """

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array([0.0, self.plate.T / 2, + (
                    self.plate.L / 2)])  # self.plateRight.L/2+ (self.plateRight.L/2 - (10) - self.beamRight.D /2) - 40#TODO add end distance here #self.plateRight.L/2 + (self.plateRight.L/2 - (10 + 8) - self.beamRight.D /2)
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array(
                [0.0, self.plate.T / 2, self.plate.L / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array(
                [0.0, self.plate.T / 2, self.beam.D / 2])  # TODO Add self.Lv instead of 25
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, -1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        """

        :return: Geometric Orientation of this components
        """
        beamOriginL = numpy.array([self.column.B / 2 - self.contPlate_L1.W / 2, 0.0,
                                   self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([self.column.B / 2 - self.contPlate_L2.W / 2, 0.0,
                                   self.column.length / 2 - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-self.column.B / 2 + self.contPlate_R1.W / 2, 0.0,
                                   self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_R1.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-self.column.B / 2 + self.contPlate_R2.W / 2, 0.0,
                                   self.column.length / 2 - self.beam.D / 2 + self.beam.T / 2 - self.contPlate_R2.T / 2])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.contPlate_R2.place(beamOriginL, beamL_uDir, beamL_wDir)

    ##############################################  Adding beam stiffeners #############################################
    def create_beam_stiffenersGeometry(self):
        """

        :return: Geometric Orientation of this components
        """
        gap = self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, gap,
                                        self.column.length / 2 + self.beam.D / 2 + self.beam_stiffener_1.W / 2])
        stiffener1_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

        gap = self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, gap,
                                        self.column.length / 2 - self.beam.D / 2 - self.beam_stiffener_1.W / 2])
        stiffener2_uDir = numpy.array([0.0, 1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    ##############################################  creating weld sections ########################################

    def create_bcWelds(self):
        """

        :return: Geometric Orientation of this components
        """
        weldFlangOrigin_1 = numpy.array(
            [-self.beam.B / 2, self.column.D / 2 + self.plate.T + self.bcWeldWeb_3.b / 2,
             self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2])
        uDir_1 = numpy.array([0, 1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bcWeldFlang_1.place(weldFlangOrigin_1, uDir_1, wDir_1)

        weldFlangOrigin_2 = numpy.array(
            [self.beam.B / 2, self.column.D / 2 + self.plate.T + self.bcWeldWeb_3.b / 2,
             self.column.length / 2 - self.beam.D / 2 + self.beam.T / 2])
        uDir_2 = numpy.array([0, 1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bcWeldFlang_2.place(weldFlangOrigin_2, uDir_2, wDir_2)

        weldWebOrigin_3 = numpy.array([0.0, self.column.D / 2 + self.plate.T + self.bcWeldWeb_3.b / 2,
                                       self.column.length / 2 - self.bcWeldWeb_3.L / 2])
        uDirWeb_3 = numpy.array([0, 1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bcWeldWeb_3.place(weldWebOrigin_3, uDirWeb_3, wDirWeb_3)

    def create_bcWeldStiff(self):
        """

        :return: Geometric Orientation of this components
        """
        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 + self.beam.D / 2 + self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 - self.beam.D / 2 - self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 + self.beam.D / 2 + self.beam_stiffener_1.L22])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T,
                                              self.column.length / 2 - self.beam.D / 2 - self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, 1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L,
             self.column.length / 2 + self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([1, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0, -1.0, 0.0])
        self.bcWeldStiffLL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L22,
             self.column.length / 2 - self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([1.0, 0.0, 0.0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L22,
             self.column.length / 2 + self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, self.column.D / 2 + self.plate.T + self.beam_stiffener_1.L,
             self.column.length / 2 - self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bcWeldStiffLR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

    ####################################### welding continuity plates with fillet weld##################################

    def create_contWelds(self):
        """

        :return: Geometric Orientation of this components
        """
        contWeldL1_U2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        contWeldL2_U2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        contWeldL1_L2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        contWeldL2_L2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2, self.column.length / 2
                                            - self.beam.D / 2 - self.contPlate_L1.T / 2 + self.beam.T / 2])
        contWeldL2_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        contWeldR1_U2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldR1_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_U2.place(contWeldR1_U2OriginL, contWeldR1_U2_uDir, contWeldR1_U2_wDir)

        contWeldR2_U2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldR2_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_U2.place(contWeldR2_U2OriginL, contWeldR2_U2_uDir, contWeldR2_U2_wDir)

        contWeldR1_L2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldR1_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_L2.place(contWeldR1_L2OriginL, contWeldR1_L2_uDir, contWeldR1_L2_wDir)

        contWeldR2_L2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldR2_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_L2.place(contWeldR2_L2OriginL, contWeldR2_L2_uDir, contWeldR2_L2_wDir)

        contWeldL1_U3OriginL = numpy.array([self.column.t / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        contWeldL1_L3OriginL = numpy.array([self.column.t / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        contWeldR2_U3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])  # TODO: shuffel it with R2_U3
        uDircontWeldR2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U3.place(contWeldR2_U3OriginL, uDircontWeldR2_U3, wDircontWeldR2_U3)

        contWeldL2_L3OriginL = numpy.array([self.column.t / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        contWeldR1_U3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U3.place(contWeldR1_U3OriginL, uDircontWeldR1_U3, wDircontWeldR1_U3)

        contWeldR1_L3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L3.place(contWeldR1_L3OriginL, uDircontWeldR1_L3, wDircontWeldR1_L3)

        contWeldL2_U3OriginL = numpy.array([self.column.t / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        contWeldR2_L3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)

        contWeldL1_U1OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        contWeldL1_L1OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldL1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        contWeldL2_U1OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        contWeldR2_L1OriginL = numpy.array([-self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR2_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldR2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L1.place(contWeldR2_L1OriginL, uDircontWeldR2_L1, wDircontWeldR2_L1)

        contWeldR1_U1OriginL = numpy.array([- self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR1_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U1.place(contWeldR1_U1OriginL, uDircontWeldR1_U1, wDircontWeldR1_U1)

        contWeldR1_L1OriginL = numpy.array([-self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR1_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldR1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L1.place(contWeldR1_L1OriginL, uDircontWeldR1_L1, wDircontWeldR1_L1)

        contWeldR2_U1OriginL = numpy.array([-self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR2_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U1.place(contWeldR2_U1OriginL, uDircontWeldR2_U1, wDircontWeldR2_U1)

        contWeldL2_L1OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldL2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

    #############################################################################################################
    #   Following functions returns the CAD model to the function display_3DModel of main file                  #
    #############################################################################################################

    def get_column_models(self):
        """

        :return: CAD model of the column
        """

        final_column = self.columnModel
        bolt_list = self.nut_bolt_array.get_bolt_list()
        for bolt in bolt_list[:]:
            final_column = BRepAlgoAPI_Cut(final_column, bolt).Shape()  # TODO: Anand #cuts the colum in section shape
        return final_column

    def get_beam_models(self):
        """

        :return:  CAD model of the beam
        """
        return self.beamModel

    def get_plate_connector_models(self):
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.contPlate_L1Model,
                                   self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model]
            else:
                connector_plate = [self.plateModel, self.contPlate_L1Model, self.contPlate_L2Model,
                                   self.contPlate_R1Model, self.contPlate_R2Model]
        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                                   self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model,
                                   self.contPlate_R2Model]
            else:
                connector_plate = [self.plateModel, self.contPlate_L1Model, self.contPlate_L2Model,
                                   self.contPlate_R1Model, self.contPlate_R2Model]
        elif self.endplate_type == "flush":
            connector_plate = [self.plateModel,
                               self.contPlate_L1Model, self.contPlate_L2Model, self.contPlate_R1Model,
                               self.contPlate_R2Model, ]

        plates = connector_plate[0]
        for comp in connector_plate[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_welded_models(self):
        """

        :return: CAD model for all the welds
        """
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model, self.contWeldR1_U2Model,
                              self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]
            else:
                welded_sec = [self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]

        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffHR_2Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                              self.bcWeldStiffLR_2Model, self.contWeldR1_U2Model, self.contWeldR2_U2Model,
                              self.contWeldR1_L2Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]
            else:
                welded_sec = [self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]

        elif self.endplate_type == "flush":
            welded_sec = [self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                          self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                          self.contWeldL2_L2Model,
                          self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                          self.contWeldR2_L2Model,
                          self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                          self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                          self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                          self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                          self.contWeldL2_U1Model,
                          self.contWeldL2_L1Model,
                          self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                          self.contWeldR2_L1Model]

        welds = welded_sec[0]
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_nut_bolt_array_models(self):
        nut_bolts = self.nut_bolt_array.get_models()
        array = nut_bolts[0]
        for comp in nut_bolts:
            array = BRepAlgoAPI_Fuse(comp, array).Shape()

        return array

    def get_connector_models(self):
        """

        :return: CAD models of the connecting components
        """
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD

    def get_models(self):
        """

        :return: complete CAD model
        """
        columns = self.get_column_models()
        beams = self.get_beam_models()
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [columns, beams, plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD


class CADcolwebGroove(CADGroove):
    def createBeamLGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        beamOriginL = numpy.array([0.0, self.column.D / 2 - self.column.t / 2, 0.0])
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(beamOriginL, beamL_uDir, beamL_wDir)

        ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        """

        :return: Geometric Orientation of this component
        """
        beamOriginL = numpy.array(
            [0.0, self.column.D / 2 - self.column.t - self.contPlate_L1.W / 2,
             self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array(
            [0.0, self.column.D / 2 - self.column.t - self.contPlate_L2.W / 2,
             self.column.length / 2 - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contWelds(self):
        """

        :return: Geometric Orientation of this components
        """
        contWeldL1_U2OriginL = numpy.array([-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([1.0, 0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        contWeldL2_U2OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t, self.column.length / 2
             - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        contWeldL1_L2OriginL = numpy.array([-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        contWeldL2_L2OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t, self.column.length / 2
             - self.beam.D / 2 + self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL2_L2_uDir = numpy.array([0.0, -1.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([1.0, 0.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        contWeldL1_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0.0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([0.0, -1, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        contWeldL1_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([-1, 0, 0.0])
        wDircontWeldL1_L3 = numpy.array([0.0, -1.0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        contWeldL2_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([0, -1, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        contWeldL2_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.D / 2 - self.column.t,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([-1, 0.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([0.0, -1, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        contWeldL1_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.B / 2 - self.column.t / 2,
             self.column.length / 2 + (self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL1_U1 = numpy.array([0.0, 1, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        contWeldL1_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.B / 2 - self.column.t / 2,
             self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL1_L1 = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        contWeldL2_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.B / 2 - self.column.t / 2,
             self.column.length / 2 - (self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL2_U1 = numpy.array([0, 1, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        contWeldL2_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, self.column.D / 2 - self.column.B / 2 - self.column.t / 2,
             self.column.length / 2 - (self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL2_L1 = numpy.array([0.0, 1.0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

    def get_plate_connector_models(self):
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.contPlate_L1Model,
                                   self.contPlate_L2Model, ]
            else:
                connector_plate = [self.plateModel, self.contPlate_L1Model, self.contPlate_L2Model, ]
        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                                   self.contPlate_L1Model, self.contPlate_L2Model, ]
            else:
                connector_plate = [self.plateModel, self.contPlate_L1Model, self.contPlate_L2Model, ]
        elif self.endplate_type == "flush":
            connector_plate = [self.plateModel,
                               self.contPlate_L1Model, self.contPlate_L2Model, ]

        plates = connector_plate[0]
        for comp in connector_plate[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_welded_models(self):
        """

        :return: CAD model for all the welds
        """
        if self.endplate_type == "one_way":
            if self.numberOfBolts == 12:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model, self.bcWeldFlang_1Model,
                              self.bcWeldFlang_2Model, self.bcWeldWeb_3Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                              self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model]
            else:
                welded_sec = [self.bcWeldFlang_1Model, self.bcWeldFlang_2Model, self.bcWeldWeb_3Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                              self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model, ]

        elif self.endplate_type == "both_way":
            if self.numberOfBolts == 20:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffHR_2Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                              self.bcWeldStiffLR_2Model, self.bcWeldFlang_1Model, self.bcWeldFlang_2Model,
                              self.bcWeldWeb_3Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                              self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model, ]
            else:
                welded_sec = [self.bcWeldFlang_1Model, self.bcWeldFlang_2Model, self.bcWeldWeb_3Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                              self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model, ]

        elif self.endplate_type == "flush":
            welded_sec = [self.bcWeldFlang_1Model, self.bcWeldFlang_2Model, self.bcWeldWeb_3Model,
                          self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                          self.contWeldL2_L2Model,
                          self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                          self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                          self.contWeldL1_L1Model, self.contWeldL2_U1Model,
                          self.contWeldL2_L1Model]

        welds = welded_sec[0]
        for comp in welded_sec[1:]:
            welds = BRepAlgoAPI_Fuse(comp, welds).Shape()

        return welds

    def get_connector_models(self):
        """

        :return: CAD models of the connecting components
        """
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD

    def get_models(self):
        """

        :return: complete CAD model
        """
        columns = self.get_column_models()
        beams = self.get_beam_models()
        plate_connectors = self.get_plate_connector_models()
        welds = self.get_welded_models()
        nut_bolt_array = self.get_nut_bolt_array_models()

        CAD_list = [columns, beams, plate_connectors, welds, nut_bolt_array]
        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD
