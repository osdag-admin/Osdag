"""
Initialized on 23-04-2019
Commenced on 24-04-2019
@author: Anand Swaroop
"""""

from math import radians
import numpy
import copy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.gp import (gp_Vec, gp_Pnt, gp_Trsf, gp_OX, gp_OY,
                         gp_OZ, gp_XYZ, gp_Ax2, gp_Dir, gp_GTrsf, gp_Mat)
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge,
                                     BRepBuilderAPI_MakeVertex,
                                     BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge2d,
                                     BRepBuilderAPI_Transform)
from math import *

class CADFillet(object):# not used in the current version as groove weld is preferred best practice.
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
        '''
        initialise the location of the column by defining the local origin of the component with respect to global origin
        '''

        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamGeometry(self):
        '''
        initialise the location of the beam by defining the local origin of the component with respect to global origin
        '''

        gap = self.column.D / 2 + self.plate.T
        beamOriginR = numpy.array([0.0, gap, self.column.length / 2])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beam.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):
        '''
        initialise the location of the plate by defining the local origin of the component with respect to global origin
        '''

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
        '''
        initialise the location of the bolt group (top flange) by defining the local origin of the component with respect to global origin
        '''

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
        '''
        initialise the location of the continuity plate by defining the local origin of the component with respect to global origin
        '''
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
        '''
        initialise the location of the stiffener by defining the local origin of the component with respect to global origin
        '''
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
        '''
        initialise the location of the flange weld by defining the local origin of the component with respect to global origin
        '''
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
        '''
        initialise the location of the continuity plate weld by defining the local origin of the component with respect to global origin
        '''
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
        '''
        initialise the location of the web weld by defining the local origin of the component with respect to global origin
        '''
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

  

    def __init__(self, module, column, beam, plate, nut_bolt_array, bolt,bcWeldFlang,bcWeldWeb,
                 contPlates,beam_stiffeners,bcWeldStiffHeight,bcWeldStiffLength,contWeldD,contWeldB,diagplate,diagWeldD,diagWeldB,webplate, webWeldB, webWeldD, beam_stiffenerFlush, bcWeldFlushstiffHeight, bcWeldFlushstiffLength,endplate_type):
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
        self.contPlates = contPlates
        self.diagplate =diagplate
        self.diagWeldD = diagWeldD
        self.diagWeldB = diagWeldB
        self.webplate = webplate
        self.webWeldB = webWeldB
        self.webWeldD = webWeldD

        if self.webplate !=None:

            self.webplate_L = self.webplate
            self.webplate_R = copy.deepcopy(self.webplate)


        if self.diagplate!= None:
            self.diagplate_L1 = self.diagplate
            self.diagplate_R1= copy.deepcopy(self.diagplate)
        if self.contPlates!= None:

            self.contPlate_L1 = self.contPlates
            self.contPlate_L2 = copy.deepcopy(self.contPlates)
            self.contPlate_R1 = copy.deepcopy(self.contPlates)
            self.contPlate_R2 = copy.deepcopy(self.contPlates)
        self.beam_stiffener_1 = beam_stiffeners
        self.beam_stiffener_2 = copy.deepcopy(beam_stiffeners)

        # flush stiffener#
        # self.beam_stiffener_F1 = beam_stiffenerFlush
        # self.beam_stiffener_F2 = copy.deepcopy(beam_stiffenerFlush)
        # self.beam_stiffener_F3 = copy.deepcopy(beam_stiffenerFlush)
        # self.beam_stiffener_F4 = copy.deepcopy(beam_stiffenerFlush)

        self.endplate_type = endplate_type
        self.module= module
        self.numberOfBolts = int(self.module.plate.bolts_required)
        self.plateProjection = self.module.projection # gives the bolt projection


        self.bcWeldFlang_R1 = bcWeldFlang
        self.bcWeldFlang_R2 = copy.deepcopy(bcWeldFlang)

        self.bcWeldWeb_R3 = bcWeldWeb

        if self.module.endplate_type == 'Flushed - Reversible Moment' and self.module.bolt_row_web == 0:
            self.loc1 = float(self.module.beam_D / 2 - self.module.stiffener_thickness / 2)
            self.loc2 = None
        else:
            self.loc1 = float(
                self.module.beam_D / 2 - self.module.stiffener_thickness / 2 - self.module.pitch_distance_web / 2)
            self.loc2 = float(
                self.module.beam_D / 2 - self.module.stiffener_thickness / 2 + self.module.pitch_distance_web / 2)

        if self.webplate != None:
            self.webWeldB_LT = self.webWeldB
            self.webWeldB_LB = copy.deepcopy(self.webWeldB)
            self.webWeldB_RT = copy.deepcopy(self.webWeldB)
            self.webWeldB_RB = copy.deepcopy(self.webWeldB)
            self.webWeldD_LL = self.webWeldD
            self.webWeldD_LR = copy.deepcopy(self.webWeldD)
            self.webWeldD_RL = copy.deepcopy(self.webWeldD)
            self.webWeldD_RR = copy.deepcopy(self.webWeldD)


        self.bcWeldStiffHL_1 = bcWeldStiffHeight
        self.bcWeldStiffHL_2 = copy.deepcopy(bcWeldStiffHeight)
        self.bcWeldStiffHR_1 = copy.deepcopy(bcWeldStiffHeight)
        self.bcWeldStiffHR_2 = copy.deepcopy(bcWeldStiffHeight)

        self.bcWeldStiffLL_1 = bcWeldStiffLength
        self.bcWeldStiffLL_2 = copy.deepcopy(bcWeldStiffLength)
        self.bcWeldStiffLR_1 = copy.deepcopy(bcWeldStiffLength)
        self.bcWeldStiffLR_2 = copy.deepcopy(bcWeldStiffLength)
        self.contWeldD = contWeldD
        self.contWeldB = contWeldB

        if self.contWeldD != None:
            self.contWeldL1_U2 = self.contWeldD
            self.contWeldL2_U2 = copy.deepcopy(self.contWeldD)
            self.contWeldL1_L2 = copy.deepcopy(self.contWeldD)
            self.contWeldL2_L2 = copy.deepcopy(self.contWeldD)
            self.contWeldR1_U2 = copy.deepcopy(self.contWeldD)
            self.contWeldR2_U2 = copy.deepcopy(self.contWeldD)
            self.contWeldR1_L2 = copy.deepcopy(self.contWeldD)
            self.contWeldR2_L2 = copy.deepcopy(self.contWeldD)
        if self.contWeldB != None:

            self.contWeldL1_U3 = self.contWeldB
            self.contWeldL1_L3 = copy.deepcopy(self.contWeldB)
            self.contWeldL2_U3 = copy.deepcopy(self.contWeldB)
            self.contWeldL2_L3 = copy.deepcopy(self.contWeldB)
            self.contWeldR1_U3 = copy.deepcopy(self.contWeldB)
            self.contWeldR1_L3 = copy.deepcopy(self.contWeldB)
            self.contWeldR2_U3 = copy.deepcopy(self.contWeldB)
            self.contWeldR2_L3 = copy.deepcopy(self.contWeldB)
            self.contWeldL1_U1 = copy.deepcopy(self.contWeldB)
            self.contWeldL1_L1 = copy.deepcopy(self.contWeldB)
            self.contWeldL2_U1 = copy.deepcopy(self.contWeldB)
            self.contWeldL2_L1 = copy.deepcopy(self.contWeldB)
            self.contWeldR1_U1 = copy.deepcopy(self.contWeldB)
            self.contWeldR1_L1 = copy.deepcopy(self.contWeldB)
            self.contWeldR2_U1 = copy.deepcopy(self.contWeldB)
            self.contWeldR2_L1 = copy.deepcopy(self.contWeldB)
        if self.diagWeldD != None:
            self.diagWeldL1_L = self.diagWeldD
            self.diagWeldL1_U = copy.deepcopy(self.diagWeldD)
            self.diagWeldR1_L = copy.deepcopy(self.diagWeldD)
            self.diagWeldR1_U = copy.deepcopy(self.diagWeldD)
        if self.diagWeldB != None:
            self.diagWeldS1_U = self.diagWeldB
            self.diagWeldS1_L = copy.deepcopy(self.diagWeldB)
            self.diagWeldS2_U = copy.deepcopy(self.diagWeldB)
            self.diagWeldS2_L = copy.deepcopy(self.diagWeldB)

        # flush stiffener#
        # self.bcWeldstiff1_u1 = bcWeldFlushstiffHeight
        # self.bcWeldstiff1_l1 = copy.deepcopy(bcWeldFlushstiffHeight)
        # self.bcWeldstiff2_u1 = copy.deepcopy(bcWeldFlushstiffHeight)
        # self.bcWeldstiff2_l1 = copy.deepcopy(bcWeldFlushstiffHeight)
        # self.bcWeldstiff3_u1 = copy.deepcopy(bcWeldFlushstiffHeight)
        # self.bcWeldstiff3_l1 = copy.deepcopy(bcWeldFlushstiffHeight)
        # self.bcWeldstiff4_u1 = copy.deepcopy(bcWeldFlushstiffHeight)
        # self.bcWeldstiff4_l1 = copy.deepcopy(bcWeldFlushstiffHeight)
       
        #flush stiffener#
        # self.bcWeldstiff1_u2 = bcWeldFlushstiffLength
        # self.bcWeldstiff1_l2 = copy.deepcopy(bcWeldFlushstiffLength)
        # self.bcWeldstiff2_u2 = copy.deepcopy(bcWeldFlushstiffLength)
        # self.bcWeldstiff2_l2 = copy.deepcopy(bcWeldFlushstiffLength)
        # self.bcWeldstiff3_u2 = copy.deepcopy(bcWeldFlushstiffLength)
        # self.bcWeldstiff3_l2 = copy.deepcopy(bcWeldFlushstiffLength)
        # self.bcWeldstiff4_u2 = copy.deepcopy(bcWeldFlushstiffLength)
        # self.bcWeldstiff4_l2 = copy.deepcopy(bcWeldFlushstiffLength)



    def create_3DModel(self):
        """
        :return: CAD model of each entity
        """
        self.createBeamLGeometry()
        self.createBeamGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()
        if self.contPlates != None:
            self.create_contPlatesGeometry()

        if self.webplate != None:
            self.create_webPlatesGeometry()

        self.create_beam_stiffenersGeometry()
        # self.createbeam_stiffenerFlushGeometry()
        self.create_bcWeldFlangGeometry()
        self.create_bcWeldWebGeometry()
        # self.create_bcWeldFlushstiffHeight()
        # self.create_bcWeldFlushstiffLength()
        if self.diagplate != None:
            self.create_diagplateGeometry()

        self.create_bcWeldStiff()
        if self.contWeldD != None and self.contWeldB != None:
            # pass
            self.create_contWelds()
        if self.diagplate != None:
            self.create_diagWelds()

        if self.webplate != None:
            self.create_webWelds()

        # call for create_model of filletweld from Components directory
        self.columnModel = self.column.create_model()
        self.beamModel = self.beam.create_model()
        self.plateModel = self.plate.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()
        if self.diagplate!= None:
            self.diagplate_L1Model = self.diagplate_L1.create_model(-45)
            self.diagplate_R1Model = self.diagplate_R1.create_model(-45)
        if self.contPlates != None:
            if self.module.connectivity == "Column Web-Beam Web":
                self.contPlate_L1Model = self.contPlate_L1.create_model()
                self.contPlate_L2Model = self.contPlate_L2.create_model()
            else:
                self.contPlate_L1Model = self.contPlate_L1.create_model()
                self.contPlate_L2Model = self.contPlate_L2.create_model()
                self.contPlate_R1Model = self.contPlate_R1.create_model()
                self.contPlate_R2Model = self.contPlate_R2.create_model()

        if self.webplate != None:
            self.webplate_LModel = self.webplate_L.create_model()
            self.webplate_RModel = self.webplate_R.create_model()

        if self.webplate != None:
            self.webWeldB_LTModel = self.webWeldB_LT.create_model()
            self.webWeldB_LBModel = self.webWeldB_LB.create_model()
            self.webWeldB_RTModel = self.webWeldB_RT.create_model()
            self.webWeldB_RBModel = self.webWeldB_RB.create_model()
            self.webWeldD_LLModel = self.webWeldD_LL.create_model()
            self.webWeldD_LRModel = self.webWeldD_LR.create_model()
            self.webWeldD_RLModel = self.webWeldD_RL.create_model()
            self.webWeldD_RRModel = self.webWeldD_RR.create_model()

        self.beam_stiffener_1Model = self.beam_stiffener_1.create_model()
        self.beam_stiffener_2Model = self.beam_stiffener_2.create_model()


        self.bcWeldFlang_R1Model = self.bcWeldFlang_R1.create_model()
        self.bcWeldFlang_R2Model = self.bcWeldFlang_R2.create_model()

        self.bcWeldWeb_R3Model = self.bcWeldWeb_R3.create_model()


        self.bcWeldStiffHL_1Model = self.bcWeldStiffHL_1.create_model()
        self.bcWeldStiffHL_2Model = self.bcWeldStiffHL_2.create_model()
        self.bcWeldStiffHR_1Model = self.bcWeldStiffHR_1.create_model()
        self.bcWeldStiffHR_2Model = self.bcWeldStiffHR_2.create_model()

        self.bcWeldStiffLL_1Model = self.bcWeldStiffLL_1.create_model()
        self.bcWeldStiffLL_2Model = self.bcWeldStiffLL_2.create_model()
        self.bcWeldStiffLR_1Model = self.bcWeldStiffLR_1.create_model()
        self.bcWeldStiffLR_2Model = self.bcWeldStiffLR_2.create_model()

        # flush stiffener#
        # self.beam_stiffener_F1Model = self.beam_stiffener_F1.create_model()
        # self.beam_stiffener_F2Model = self.beam_stiffener_F2.create_model()
        # if self.loc2 != None:
        #     self.beam_stiffener_F3Model = self.beam_stiffener_F3.create_model()
        #     self.beam_stiffener_F4Model = self.beam_stiffener_F4.create_model()


        if self.contPlates != None:

            if self.module.connectivity == "Column Web-Beam Web":
                self.contWeldL1_U2Model = self.contWeldL1_U2.create_model()
                self.contWeldL2_U2Model = self.contWeldL2_U2.create_model()
                self.contWeldL1_L2Model = self.contWeldL1_L2.create_model()
                self.contWeldL2_L2Model = self.contWeldL2_L2.create_model()
                self.contWeldL1_U3Model = self.contWeldL1_U3.create_model()
                self.contWeldL1_L3Model = self.contWeldL1_L3.create_model()
                self.contWeldL2_U3Model = self.contWeldL2_U3.create_model()
                self.contWeldL2_L3Model = self.contWeldL2_L3.create_model()
                self.contWeldL1_U1Model = self.contWeldL1_U1.create_model()
                self.contWeldL1_L1Model = self.contWeldL1_L1.create_model()
                self.contWeldL2_U1Model = self.contWeldL2_U1.create_model()
                self.contWeldL2_L1Model = self.contWeldL2_L1.create_model()
            else:
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

        if self.diagplate != None: # omitted due to detailing issues

            self.diagWeldL1_LModel = self.diagWeldL1_L.create_model(-45)
            self.diagWeldL1_UModel = self.diagWeldL1_U.create_model(-45)
            self.diagWeldR1_LModel = self.diagWeldR1_L.create_model(-45)
            self.diagWeldR1_UModel = self.diagWeldR1_U.create_model(-45)

            self.diagWeldS1_UModel = self.diagWeldS1_U.create_model(45)
            self.diagWeldS1_LModel = self.diagWeldS1_L.create_model(-135)
            self.diagWeldS2_UModel = self.diagWeldS2_U.create_model(45)
            self.diagWeldS2_LModel = self.diagWeldS2_L.create_model(-135)

        # flush stiffener#
        # self.bcWeldstiff1_u1Model = self.bcWeldstiff1_u1.create_model()
        # self.bcWeldstiff1_u2Model = self.bcWeldstiff1_u2.create_model()
        # self.bcWeldstiff1_l1Model = self.bcWeldstiff1_l1.create_model()
        # self.bcWeldstiff1_l2Model = self.bcWeldstiff1_l2.create_model()
        # #
        # self.bcWeldstiff2_u1Model = self.bcWeldstiff2_u1.create_model()
        # self.bcWeldstiff2_u2Model = self.bcWeldstiff2_u2.create_model()
        # self.bcWeldstiff2_l1Model = self.bcWeldstiff2_l1.create_model()
        # self.bcWeldstiff2_l2Model = self.bcWeldstiff2_l2.create_model()
        # #
        # if self.loc2 != None:
        #     self.bcWeldstiff3_u1Model = self.bcWeldstiff3_u1.create_model()
        #     self.bcWeldstiff3_u2Model = self.bcWeldstiff3_u2.create_model()
        #     self.bcWeldstiff3_l1Model = self.bcWeldstiff3_l1.create_model()
        #     self.bcWeldstiff3_l2Model = self.bcWeldstiff3_l2.create_model()
        #     #
        #     self.bcWeldstiff4_u1Model = self.bcWeldstiff4_u1.create_model()
        #     self.bcWeldstiff4_u2Model = self.bcWeldstiff4_u2.create_model()
        #     self.bcWeldstiff4_l1Model = self.bcWeldstiff4_l1.create_model()
        #     self.bcWeldstiff4_l2Model = self.bcWeldstiff4_l2.create_model()
        #


        
    #############################################################################################################
    #   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
    #   same component at appropriate place                                                                     #
    #############################################################################################################

    def createBeamLGeometry(self):
        '''
        initialise the location of the left beam by defining the local origin of the component with respect to global origin
        '''
        beamOriginL = numpy.array([0.0, 0.0, 0.0])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamGeometry(self):
        '''
        initialise the location of the right beam by defining the local origin of the component with respect to global origin
        '''
        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B / 2
        else:
            offset = self.column.D / 2
        gap = offset + self.plate.T + self.bcWeldWeb_R3.b
        beamOriginR = numpy.array([0.0, -gap, self.column.length / 2])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, -1.0, 0.0])
        self.beam.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):
        '''
        initialise the location of the plate by defining the local origin of the component with respect to global origin
        '''
        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B / 2
        else:
            offset = self.column.D / 2

        if self.endplate_type == "one_way":
            gap = 0.5 * self.plate.T + offset
            plateOriginR = numpy.array([-self.plate.W / 2, -gap, self.column.length / 2 + (
                    self.plate.L / 2 - self.plateProjection - self.beam.D / 2)])  # TODO #Add weld thickness here
            plateR_uDir = numpy.array([0.0, -1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plate.place(plateOriginR, plateR_uDir, plateR_wDir)

        else:  # self.endplate_type == "both_way" and flushed
            gap = 0.5 * self.plate.T + offset
            plateOriginR = numpy.array([-self.plate.W / 2, -gap, self.column.length / 2])
            plateR_uDir = numpy.array([0.0, -1.0, 0.0])
            plateR_wDir = numpy.array([1.0, 0.0, 0.0])
            self.plate.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        '''
        initialise the location of the bolt group (top flange) by defining the local origin of the component with respect to global origin
        '''

        if self.endplate_type == "one_way":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array([0.0, -self.plate.T / 2, + (
                    self.plate.L / 2)])  # self.plateRight.L/2+ (self.plateRight.L/2 - (10) - self.beamRight.D /2) - 40#TODO add end distance here #self.plateRight.L/2 + (self.plateRight.L/2 - (10 + 8) - self.beamRight.D /2)
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, 1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "both_way":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array(
                [0.0, -self.plate.T / 2, self.plate.L / 2])
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, 1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

        elif self.endplate_type == "flush":
            nutboltArrayOrigin = self.plate.sec_origin + numpy.array(
                [0.0, -self.plate.T / 2, self.plate.L / 2])  # TODO Add self.Lv instead of 25
            gaugeDir = numpy.array([1.0, 0, 0])
            pitchDir = numpy.array([0, 0, -1.0])
            boltDir = numpy.array([0, 1.0, 0])
            self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        '''
        initialise the location of the continuity plate by defining the local origin of the component with respect to global origin
        '''
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

    def create_webPlatesGeometry(self):
        '''
        initialise the location of the column web stiffener by defining the local origin of the component with respect to global origin
        '''
        beamOriginL = numpy.array([self.column.t / 2 + self.webplate_L.T, 0.0,
                                   self.column.length / 2 ])
        beamL_uDir = numpy.array([0.0, 0.0,1.0])
        beamL_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.webplate_L.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array([-(self.column.t / 2 + self.webplate_L.T), 0.0,
                                   self.column.length / 2])
        beamL_uDir = numpy.array([0.0, 0.0, 1.0])
        beamL_wDir = numpy.array([1.0, 0.0, 0.0])
        self.webplate_R.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_diagplateGeometry(self): #omitted due to dettailing issue
        '''
        initialise the location of the diagonal stiffener by defining the local origin of the component with respect to global origin
        '''
        beamOriginL = numpy.array([self.diagplate_L1.W/2 +self.column.t/2,-self.column.length/2*cos(radians(45)),(((self.column.length / 2 )*sin(radians(45)))+self.diagplate_L1.T/2)])
        print(beamOriginL,"1")
        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.diagplate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)


        beamOriginL = numpy.array([-self.diagplate_R1.W / 2 - self.column.t/2, -self.column.length / 2 * cos(radians(45)),
                                   ((self.column.length / 2 )* sin(radians(45))) +self.diagplate_R1.T/2])

        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.diagplate_R1.place(beamOriginL, beamL_uDir, beamL_wDir)


    ##############################################  Adding beam stiffeners #############################################
    def create_beam_stiffenersGeometry(self):
        '''
        initialise the location of the top nad bottom stiffener by defining the local origin of the component with respect to global origin
        '''

        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B / 2
        else:
            offset = self.column.D / 2

        gap = offset + self.plate.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin1 = numpy.array([-self.beam_stiffener_1.T / 2, -gap,
                                        self.column.length / 2 - self.beam.D / 2 - self.beam_stiffener_1.W / 2])
        stiffener1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam_stiffener_1.place(stiffenerOrigin1, stiffener1_uDir, stiffener1_wDir)

        gap = offset + self.plate.T + self.beam_stiffener_1.L / 2
        stiffenerOrigin2 = numpy.array([self.beam_stiffener_1.T / 2, -gap,
                                        self.column.length / 2 + self.beam.D / 2 + self.beam_stiffener_1.W / 2])
        stiffener2_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.beam_stiffener_2.place(stiffenerOrigin2, stiffener2_uDir, stiffener2_wDir)

    def createbeam_stiffenerFlushGeometry(self): #todo darshan
        '''
        initialise the location of the side stiffener by defining the local origin of the bolt group with respect to global origin
        '''
        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B/2
        else:
            offset = self.column.D/2

        gap = -(offset + self.plate.T + self.beam_stiffener_F1.L / 2 + self.bcWeldWeb_R3.b)
        stiffenerOriginF1 = numpy.array([-self.beam_stiffener_F1.W/2 - self.beam.t/2, gap,
                                         self.column.length/ 2 - self.loc1])
        stiffenerF1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF1_wDir = numpy.array([0.0, 0.0, -1.0])
        self.beam_stiffener_F1.place(stiffenerOriginF1, stiffenerF1_uDir, stiffenerF1_wDir)

        gap = -(offset + self.plate.T + self.beam_stiffener_F2.L / 2 + self.bcWeldWeb_R3.b)
        stiffenerOriginF2 = numpy.array([self.beam_stiffener_F2.W/2 + self.beam.t/2 , gap,
                                         self.beam.Dself.column.length / 2 -self.beam_stiffener_2.T - self.loc1])
        stiffenerF2_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffenerF2_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beam_stiffener_F2.place(stiffenerOriginF2, stiffenerF2_uDir, stiffenerF2_wDir)

        # if self.loc2 != None:
        # 
        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L / 2 +  self.bbWeldWeb_L3.b
        #     stiffenerOriginF3 = numpy.array([-(self.beam_stiffener_F3.W/2 + self.beamRight.t/2), gap,
        #                                      self.beamRight.D / 2 -self.beam_stiffener_F3.T- self.loc1])
        #     stiffenerF3_uDir = numpy.array([0.0, 1.0, 0.0])
        #     stiffenerF3_wDir = numpy.array([0.0, 0.0, 1.0])
        #     self.beam_stiffener_F3.place(stiffenerOriginF3, stiffenerF3_uDir, stiffenerF3_wDir)
        # 
        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F4.L / 2 +  self.bbWeldWeb_L3.b
        #     stiffenerOriginF4 = numpy.array([(self.beam_stiffener_F4.W/2 + self.beamRight.t/2), gap,
        #                                      self.beamRight.D / 2 - self.loc1])
        #     stiffenerF4_uDir = numpy.array([0.0, 1.0, 0.0])
        #     stiffenerF4_wDir = numpy.array([0.0, 0.0, -1.0])
        #     self.beam_stiffener_F4.place(stiffenerOriginF4, stiffenerF4_uDir, stiffenerF4_wDir)

    ##############################################  creating weld sections ########################################

    def create_bcWeldFlangGeometry(self):
        '''
        initialise the location of the flange weld by defining the local origin of the component with respect to global origin
        '''

        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B / 2
        else:
            offset = self.column.D / 2

        gap = offset + self.plate.T + self.bcWeldWeb_R3.b/2
        weldFlangOrigin_R1 = numpy.array([- self.beam.B / 2, -gap, self.column.length/2+self.beam.D / 2 - self.beam.T / 2])
        uDir_1 = numpy.array([0, -1.0, 0])
        wDir_1 = numpy.array([1.0, 0, 0])
        self.bcWeldFlang_R1.place(weldFlangOrigin_R1, uDir_1, wDir_1)

        gap = offset + self.plate.T+ self.bcWeldWeb_R3.b/2
        weldFlangOrigin_R2 = numpy.array([self.beam.B / 2, -gap, self.column.length/2-(self.beam.D / 2 - self.beam.T / 2)])
        uDir_2 = numpy.array([0, -1.0, 0])
        wDir_2 = numpy.array([-1.0, 0, 0])
        self.bcWeldFlang_R2.place(weldFlangOrigin_R2, uDir_2, wDir_2)



    def create_bcWeldWebGeometry(self):
        '''
        initialise the location of the web weld by defining the local origin of the component with respect to global origin
        '''

        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B / 2
        else:
            offset = self.column.D / 2

        gap = offset + self.plate.T + self.bcWeldWeb_R3.b/2
        weldWebOrigin_R3 = numpy.array([0.0, -gap,self.column.length/2-self.beam.D/2 + self.beam.T])
        uDirWeb_3 = numpy.array([0, -1.0, 0])
        wDirWeb_3 = numpy.array([0, 0, 1.0])
        self.bcWeldWeb_R3.place(weldWebOrigin_R3, uDirWeb_3, wDirWeb_3)


    def create_bcWeldStiff(self):
        '''
        initialise the location of the stiffener weld by defining the local origin of the component with respect to global origin
        '''
        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B / 2
        else:
            offset = self.column.D / 2


        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, -(offset + self.plate.T),
                                              self.column.length / 2 + self.beam.D / 2+5 ])
        uDirStiffHL_1 = numpy.array([0, -1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)####

        weldStiffWebOriginHL_1 = numpy.array([self.beam_stiffener_1.T / 2, -(offset + self.plate.T),
                                              self.column.length / 2 - self.beam.D / 2- self.beam_stiffener_1.W ])
        uDirStiffHL_1 = numpy.array([0, -1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, 1.0])
        self.bcWeldStiffHL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)#####

        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, -(offset + self.plate.T),
                                              self.column.length / 2 + self.beam.D / 2+ self.beam_stiffener_1.W])
        uDirStiffHL_1 = numpy.array([0, -1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)#######

        weldStiffWebOriginHL_1 = numpy.array([-self.beam_stiffener_1.T / 2, -(offset + self.plate.T),
                                              self.column.length / 2 - self.beam.D / 2 -5])
        uDirStiffHL_1 = numpy.array([0, -1.0, 0])
        wDirStiffHL_1 = numpy.array([0, 0, -1.0])
        self.bcWeldStiffHR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)######

        weldStiffWebOriginHL_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, -(offset + self.plate.T+5),
             self.column.length / 2 + self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([1, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0, -1.0, 0.0])
        self.bcWeldStiffLL_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)####

        weldStiffWebOriginHL_1 = numpy.array(
            [self.beam_stiffener_1.T / 2, -(offset + self.plate.T + self.beam_stiffener_1.L),
             self.column.length / 2 - self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([1.0, 0.0, 0.0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLL_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, -(offset + self.plate.T + self.beam_stiffener_1.L),
             self.column.length / 2 + self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldStiffLR_1.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)

        weldStiffWebOriginHL_1 = numpy.array(
            [-self.beam_stiffener_1.T / 2, -(offset + self.plate.T+5),
             self.column.length / 2 - self.beam.D / 2])
        uDirStiffHL_1 = numpy.array([-1.0, 0.0, 0])
        wDirStiffHL_1 = numpy.array([0.0, -1.0, 0.0])
        self.bcWeldStiffLR_2.place(weldStiffWebOriginHL_1, uDirStiffHL_1, wDirStiffHL_1)#####

    def create_bcWeldFlushstiffHeight(self):#todo darshan
        '''
        initialise the location of the side stiffener weld along the height by defining the local origin of the bolt group with respect to global origin
        '''

        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B / 2
        else:
            offset = self.column.D / 2

        gap = offset + self.plate.T + self.bcWeldWeb_R3.b
        stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beam.t / 2, gap,
                                           self.beam.D / 2 - self.loc1])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bcWeldstiff1_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = offset + self.plate.T + self.bcWeldWeb_R3.b
        stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.W - self.beam.t / 2, gap,
                                           self.beam.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bcWeldstiff1_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        gap = offset + self.plate.T + self.bcWeldWeb_R3.b
        stiffenerOrigin1_u1 = numpy.array([(self.beam_stiffener_F1.W + self.beam.t / 2), gap,
                                           self.beam.D / 2 - self.loc1])
        stiffener1_u1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_u1_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.bcWeldstiff2_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)

        gap = offset + self.plate.T + self.bcWeldWeb_R3.b
        stiffenerOrigin1_l1 = numpy.array([(self.beam_stiffener_F1.L22 + self.beam.t / 2), gap,
                                           self.beam.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l1_uDir = numpy.array([0.0, -1.0, 0.0])
        stiffener1_l1_wDir = numpy.array([1.0, 0.0, 0.0])
        self.bcWeldstiff2_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

        # if self.loc2 != None:
        #
        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        #     stiffenerOrigin1_u1 = numpy.array([-self.beam_stiffener_F1.W - self.beamLeft.t / 2, gap,
        #                                        self.beamRight.D / 2 - self.loc1])
        #     stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        #     stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        #     self.bbWeldstiff3_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)
        #
        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        #     stiffenerOrigin1_l1 = numpy.array([-self.beam_stiffener_F1.L22 - self.beamLeft.t / 2, gap,
        #                                        self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        #     stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        #     stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        #     self.bbWeldstiff3_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)
        #
        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        #     stiffenerOrigin1_u1 = numpy.array([self.beam_stiffener_F1.L22 + self.beamLeft.t / 2, gap,
        #                                        self.beamRight.D / 2 - self.loc1])
        #     stiffener1_u1_uDir = numpy.array([0.0, 1.0, 0.0])
        #     stiffener1_u1_wDir = numpy.array([1.0, 0.0, 0.0])
        #     self.bbWeldstiff4_u1.place(stiffenerOrigin1_u1, stiffener1_u1_uDir, stiffener1_u1_wDir)
        #
        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.bbWeldWeb_L3.b
        #     stiffenerOrigin1_l1 = numpy.array([self.beam_stiffener_F1.W + self.beamLeft.t / 2, gap,
        #                                        self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        #     stiffener1_l1_uDir = numpy.array([0.0, 1.0, 0.0])
        #     stiffener1_l1_wDir = numpy.array([-1.0, 0.0, 0.0])
        #     self.bbWeldstiff4_l1.place(stiffenerOrigin1_l1, stiffener1_l1_uDir, stiffener1_l1_wDir)

    def create_bcWeldFlushstiffLength(self): #todo darshan
        '''
        initialise the location of the side stiffener weld along the length by defining the local origin of the bolt group with respect to global origin
        '''

        if self.module.connectivity == "Column Web-Beam Web":
            offset = self.column.B / 2
        else:
            offset = self.column.D / 2

        gap = offset + self.plate.T + self.beam_stiffener_F1.L + self.bcWeldWeb_R3.b
        stiffenerOrigin1_u2 = numpy.array([-self.beam.t / 2, gap,
                                           self.beam.D / 2 - self.loc1])
        stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldstiff1_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = offset + self.plate.T + self.beam_stiffener_F1.L22 + self.bcWeldWeb_R3.b
        stiffenerOrigin1_l2 = numpy.array([-self.beam.t / 2, gap,
                                           self.beam.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bcWeldstiff1_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

        gap = offset + self.plate.T + self.beam_stiffener_F1.L + self.bcWeldWeb_R3.b
        stiffenerOrigin1_u2 = numpy.array([self.beam.t / 2, gap,
                                           self.beam.D / 2 - self.loc1])
        stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.bcWeldstiff2_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)

        gap = offset + self.plate.T + self.beam_stiffener_F1.L22 + self.bcWeldWeb_R3.b
        stiffenerOrigin1_l2 = numpy.array([self.beam.t/2, gap,
                                           self.beam.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        self.bcWeldstiff2_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

        # if self.loc2 != None:
        # gap = self.beam.length + self.plate.T + self.beam_stiffener_F3.L22+ self.bcWeldWeb_R3.b
        # stiffenerOrigin1_u2 = numpy.array([-self.beam.t / 2, gap,
        #                                    self.beam.D / 2 - self.loc1])
        # stiffener1_u2_uDir = numpy.array([-1.0, 0.0, 0.0])
        # stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        # self.bcWeldstiff3_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)
        #

        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L+ self.bbWeldWeb_L3.b
        #     stiffenerOrigin3_l2 = numpy.array([-self.beamLeft.t / 2, gap,
        #                                        self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        #     stiffener3_l2_uDir = numpy.array([-1.0, 0.0, 0.0])
        #     stiffener3_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        #     self.bbWeldstiff3_l2.place(stiffenerOrigin3_l2, stiffener3_l2_uDir, stiffener3_l2_wDir)
        #
        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L22+ self.bbWeldWeb_L3.b
        #     stiffenerOrigin1_u2 = numpy.array([self.beamLeft.t / 2, gap,
        #                                        self.beamRight.D / 2 - self.loc1])
        #     stiffener1_u2_uDir = numpy.array([0.0, 0.0, 1.0])
        #     stiffener1_u2_wDir = numpy.array([0.0, 1.0, 0.0])
        #     self.bbWeldstiff4_u2.place(stiffenerOrigin1_u2, stiffener1_u2_uDir, stiffener1_u2_wDir)
        #
        #     gap = self.beamLeft.length + self.plateLeft.T + self.plateRight.T + self.beam_stiffener_F3.L+ self.bbWeldWeb_L3.b
        #     stiffenerOrigin1_l2 = numpy.array([self.beamLeft.t/2, gap,
        #                                        self.beamRight.D / 2 - self.loc1 - self.beam_stiffener_F1.T])
        #     stiffener1_l2_uDir = numpy.array([0.0, 0.0, -1.0])
        #     stiffener1_l2_wDir = numpy.array([0.0, -1.0, 0.0])
        #     self.bbWeldstiff4_l2.place(stiffenerOrigin1_l2, stiffener1_l2_uDir, stiffener1_l2_wDir)

    ####################################### welding continuity plates with fillet weld##################################

    def create_contWelds(self):
        '''
        initialise the location of the continuity weld by defining the local origin of the component with respect to global origin
        '''
        ####right top plate top depth weld#########
        contWeldL1_U2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2 + self.contPlate_L1.L21,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        ####right bottom plate top depth weld#########
        contWeldL2_U2OriginL = numpy.array([self.column.t / 2 , -self.contPlate_L1.L / 2+ self.contPlate_L1.L21, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        ####right top plate bottom depth weld#########
        contWeldL1_L2OriginL = numpy.array([self.column.t / 2, -self.contPlate_L1.L / 2+ self.contPlate_L1.L21,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        ####right bottom plate bottom depth weld#########
        contWeldL2_L2OriginL = numpy.array([self.column.t / 2 , -self.contPlate_L1.L / 2 + self.contPlate_L1.L21, self.column.length / 2
                                            - self.beam.D / 2 - self.contPlate_L1.T / 2 + self.beam.T / 2])
        contWeldL2_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        ####left top plate top depth weld#########
        contWeldR1_U2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2 + self.contPlate_L1.L21,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldR1_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_U2.place(contWeldR1_U2OriginL, contWeldR1_U2_uDir, contWeldR1_U2_wDir)

        ####left bottom plate top depth weld#########
        contWeldR2_U2OriginL = numpy.array([-self.column.t / 2 , -self.contPlate_L1.L / 2 + self.contPlate_L1.L21, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldR2_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        contWeldR2_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_U2.place(contWeldR2_U2OriginL, contWeldR2_U2_uDir, contWeldR2_U2_wDir)

        ####left top plate bottom depth weld#########
        contWeldR1_L2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2 + self.contPlate_L1.L21,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldR1_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR1_L2.place(contWeldR1_L2OriginL, contWeldR1_L2_uDir, contWeldR1_L2_wDir)

        ####left bottom plate bottom depth weld#########
        contWeldR2_L2OriginL = numpy.array([-self.column.t / 2, -self.contPlate_L1.L / 2 + self.contPlate_L1.L21, self.column.length / 2
                                            - self.beam.D / 2 + self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldR2_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        contWeldR2_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.contWeldR2_L2.place(contWeldR2_L2OriginL, contWeldR2_L2_uDir, contWeldR2_L2_wDir)

        ####right top plate outer width top weld#########
        contWeldL1_U3OriginL = numpy.array([self.column.t / 2 + self.contPlate_L1.L21, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        ####right top plate outer width bottom weld#########
        contWeldL1_L3OriginL = numpy.array([self.column.t / 2  + self.contPlate_L1.L21, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        ####left bottom plate outer width top weld#########
        contWeldR2_U3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])  # TODO: shuffel it with R2_U3
        uDircontWeldR2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U3.place(contWeldR2_U3OriginL, uDircontWeldR2_U3, wDircontWeldR2_U3)

        ####right bottom plate outer width bottom weld#########
        contWeldL2_L3OriginL = numpy.array([self.column.t / 2  + self.contPlate_L1.L21, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        ####left top plate outer width top weld#########
        contWeldR1_U3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR1_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldR1_U3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U3.place(contWeldR1_U3OriginL, uDircontWeldR1_U3, wDircontWeldR1_U3)

        ####left top plate outer width bottom weld#########
        contWeldR1_L3OriginL = numpy.array([-self.column.B / 2, self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR1_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR1_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L3.place(contWeldR1_L3OriginL, uDircontWeldR1_L3, wDircontWeldR1_L3)

        ####right bottom plate outer width top weld#########
        contWeldL2_U3OriginL = numpy.array([self.column.t/2 + self.contPlate_L1.L21, self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        ####left bottom plate outer width bottom weld#########
        contWeldR2_L3OriginL = numpy.array([-self.column.B/2  , self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR2_L3 = numpy.array([0, -1.0, 0.0])
        wDircontWeldR2_L3 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L3.place(contWeldR2_L3OriginL, uDircontWeldR2_L3, wDircontWeldR2_L3)

        ####right top plate inner width top weld#########
        contWeldL1_U1OriginL = numpy.array([self.column.t/2 + self.contPlate_L1.L21, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        ####right top plate inner width bottom weld#########
        contWeldL1_L1OriginL = numpy.array([self.column.t / 2+ self.contPlate_L1.L21, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldL1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        ####right bottom plate inner width top weld#########ch
        contWeldL2_U1OriginL = numpy.array([self.column.t / 2 + self.contPlate_L1.L21, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 1.0, 0.0])
        wDircontWeldL2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        ####left bottom plate inner width bottom weld#########
        contWeldR2_L1OriginL = numpy.array([-self.column.B / 2 , -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR2_L1 = numpy.array([0, 0.0, -1.0])
        wDircontWeldR2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_L1.place(contWeldR2_L1OriginL, uDircontWeldR2_L1, wDircontWeldR2_L1)

        ####left top plate inner width top weld#########
        contWeldR1_U1OriginL = numpy.array([- self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR1_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR1_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_U1.place(contWeldR1_U1OriginL, uDircontWeldR1_U1, wDircontWeldR1_U1)

        ####left top plate inner width bottom weld#########
        contWeldR1_L1OriginL = numpy.array([-self.column.B / 2 , -self.contPlate_L1.L / 2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldR1_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldR1_L1 = numpy.array([1.0, 0, 0])
        self.contWeldR1_L1.place(contWeldR1_L1OriginL, uDircontWeldR1_L1, wDircontWeldR1_L1)

        ####left bottom plate inner width top weld#########
        contWeldR2_U1OriginL = numpy.array([-self.column.B / 2, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldR2_U1 = numpy.array([0, 1.0, 0])
        wDircontWeldR2_U1 = numpy.array([1.0, 0, 0])
        self.contWeldR2_U1.place(contWeldR2_U1OriginL, uDircontWeldR2_U1, wDircontWeldR2_U1)

        ####right bottom plate inner width bottom weld#########
        contWeldL2_L1OriginL = numpy.array([self.column.t / 2 + self.contPlate_L1.L21, -self.contPlate_L1.L / 2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([0, 0, -1.0])
        wDircontWeldL2_L1 = numpy.array([1.0, 0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)

    def create_diagWelds(self):
        '''
        initialise the location of the diagonal plate weld by defining the local origin of the component with respect to global origin
        '''
        diagWeldL1_U2OriginL = numpy.array([self.column.t/2,-self.column.length/2*cos(radians(45))-self.diagplate_L1.L/2,(((self.column.length / 2 )*sin(radians(45)))+self.diagplate_L1.T/2)])
        diagWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        diagWeldL1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.diagWeldL1_U.place(diagWeldL1_U2OriginL, diagWeldL1_U2_uDir, diagWeldL1_U2_wDir)

        diagWeldS1_U3OriginL = numpy.array([self.column.t/2,((self.column.length/2)*cos(radians(45))+self.diagWeldS1_U.h/2),
                                            ((self.column.length/2+self.diagplate_L1.L*sin(radians(45)))*sin(radians(45)))])
        uDirdiagWeldS1_U3 = numpy.array([0, 0.0, 1.0])
        wDirdiagWeldS1_U3 = numpy.array([1.0, 0, 0])
        self.diagWeldS1_U.place(diagWeldS1_U3OriginL, uDirdiagWeldS1_U3, wDirdiagWeldS1_U3)


        diagWeldS1_L3OriginL = numpy.array(
            [self.column.t / 2, -(self.column.length/2)*sin(radians(45))+self.diagplate_L1.T/2,-((self.column.length/2-(self.diagplate_L1.L*cos(radians(45))))*cos(radians(45)))])
        uDirdiagWeldS1_L3 = numpy.array([0, 0.0, 1.0])
        wDirdiagWeldS1_L3 = numpy.array([1.0, 0, 0])
        self.diagWeldS1_L.place(diagWeldS1_L3OriginL, uDirdiagWeldS1_L3, wDirdiagWeldS1_L3)

        diagWeldS2_U3OriginL = numpy.array(
            [-self.column.t / 2-self.diagplate_L1.W, ((self.column.length / 2) * cos(radians(45)) + self.diagWeldS1_U.h / 2),
             ((self.column.length / 2 + self.diagplate_L1.L * sin(radians(45))) * sin(radians(45)))])
        uDirdiagWeldS2_U3 = numpy.array([0, 0.0, 1.0])
        wDirdiagWeldS2_U3 = numpy.array([1.0, 0, 0])
        self.diagWeldS2_U.place(diagWeldS2_U3OriginL, uDirdiagWeldS2_U3, wDirdiagWeldS2_U3)

        diagWeldS2_L3OriginL = numpy.array(
            [-self.column.t / 2-self.diagplate_L1.W, -(self.column.length / 2) * sin(radians(45)) + self.diagplate_L1.T / 2,
             -((self.column.length / 2 - (self.diagplate_L1.L * cos(radians(45)))) * cos(radians(45)))])
        uDirdiagWeldS2_L3 = numpy.array([0, 0.0, 1.0])
        wDirdiagWeldS2_L3 = numpy.array([1.0, 0, 0])
        self.diagWeldS2_L.place(diagWeldS2_L3OriginL, uDirdiagWeldS2_L3, wDirdiagWeldS2_L3)

        diagWeldL1_L2OriginL = numpy.array([self.column.t/2,-self.column.length/2*cos(radians(45))-self.diagplate_L1.L/2,(((self.column.length / 2 )*sin(radians(45)))-self.diagplate_L1.T/2)])
        diagWeldL1_L2_uDir = numpy.array([1.0, 0.0, 0.0])
        diagWeldL1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.diagWeldL1_L.place(diagWeldL1_L2OriginL, diagWeldL1_L2_uDir, diagWeldL1_L2_wDir)

        diagWeldR1_U2OriginL = numpy.array([-self.column.t/2, -self.column.length / 2 * cos(radians(45))-self.diagplate_L1.L/2,
                                   ((self.column.length / 2 )* sin(radians(45))) + self.diagplate_R1.T/2])
        diagWeldR1_U2_uDir = numpy.array([-1.0, 0.0, 0.0])
        diagWeldR1_U2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.diagWeldR1_U.place(diagWeldR1_U2OriginL, diagWeldR1_U2_uDir, diagWeldR1_U2_wDir)

        diagWeldR1_L2OriginL = numpy.array([-self.column.t/2, -self.column.length / 2 * cos(radians(45))-self.diagplate_R1.L/2,
                                   ((self.column.length / 2 )* sin(radians(45))) - self.diagplate_R1.T/2])
        diagWeldR1_L2_uDir = numpy.array([0.0, 0.0, -1.0])
        diagWeldR1_L2_wDir = numpy.array([0.0, 1.0, 0.0])
        self.diagWeldR1_L.place(diagWeldR1_L2OriginL, diagWeldR1_L2_uDir, diagWeldR1_L2_wDir)

    def create_webWelds(self):
        '''
        initialise the location of the web stiffener plate weld by defining the local origin of the component with respect to global origin
        '''

        webWeldLTOriginL = numpy.array([self.column.t / 2 , -self.webplate_L.W/2,
                                   self.column.length / 2 + self.webplate_L.L/2])
        webWeldLT_uDir = numpy.array([0.0, 0.0, 1.0])
        webWeldLT_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webWeldB_LT.place(webWeldLTOriginL, webWeldLT_uDir, webWeldLT_wDir)

        webWeldLBOriginL = numpy.array([self.column.t / 2 , self.webplate_L.W/2,
                                   self.column.length / 2 - self.webplate_L.L/2])
        webWeldLB_uDir = numpy.array([0.0, 0.0, -1.0])
        webWeldLB_wDir = numpy.array([0.0, -1.0, 0.0])
        self.webWeldB_LB.place(webWeldLBOriginL, webWeldLB_uDir, webWeldLB_wDir)

        webWeldRTOriginL = numpy.array([-self.column.t / 2 , self.webplate_L.W/2,
                                   self.column.length / 2 + self.webplate_L.L/2])
        webWeldRT_uDir = numpy.array([0.0, 0.0, 1.0])
        webWeldRT_wDir = numpy.array([0.0, -1.0, 0.0])
        self.webWeldB_RT.place(webWeldRTOriginL, webWeldRT_uDir, webWeldRT_wDir)

        webWeldRBOriginL = numpy.array([-self.column.t / 2 , -self.webplate_L.W/2,
                                   self.column.length / 2 - self.webplate_L.L/2])
        webWeldRB_uDir = numpy.array([0.0, 0.0, -1.0])
        webWeldRB_wDir = numpy.array([0.0, 1.0, 0.0])
        self.webWeldB_RB.place(webWeldRBOriginL, webWeldRB_uDir, webWeldRB_wDir)

        ######################
        webWeldLLOriginL = numpy.array([self.column.t / 2 , -self.webplate_L.W/2,
                                   self.column.length / 2 - self.webplate_L.L/2])
        webWeldLL_uDir = numpy.array([0.0, -1.0, 0])
        webWeldLL_wDir = numpy.array([0, 0.0, 1])
        self.webWeldD_LL.place(webWeldLLOriginL, webWeldLL_uDir, webWeldLL_wDir)

        webWeldLROriginL = numpy.array([self.column.t / 2 , self.webplate_L.W/2,
                                   self.column.length / 2 + self.webplate_L.L/2])
        webWeldLR_uDir = numpy.array([0.0, 1.0, 0])
        webWeldLR_wDir = numpy.array([0, 0.0, -1])
        self.webWeldD_LR.place(webWeldLROriginL, webWeldLR_uDir, webWeldLR_wDir)

        webWeldRLOriginL = numpy.array([-self.column.t / 2 , -self.webplate_L.W/2,
                                   self.column.length / 2 + self.webplate_L.L/2])
        webWeldRL_uDir = numpy.array([0.0, -1.0, 0])
        webWeldRL_wDir = numpy.array([0, 0.0, -1])
        self.webWeldD_RL.place(webWeldRLOriginL, webWeldRL_uDir, webWeldRL_wDir)

        webWeldRROriginL = numpy.array([-self.column.t / 2 , self.webplate_L.W/2,
                                   self.column.length / 2 - self.webplate_L.L/2])
        webWeldRR_uDir = numpy.array([0.0, 1.0, 0])
        webWeldRR_wDir = numpy.array([0, 0.0, 1])
        self.webWeldD_RR.place(webWeldRROriginL, webWeldRR_uDir, webWeldRR_wDir)



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
            # if self.numberOfBolts == 12:
            if self.webplate != None and self.contPlates != None:
                connector_plate = [self.plateModel,  self.beam_stiffener_2Model,self.contPlate_L1Model,
                                    self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                                   self.webplate_LModel,self.webplate_RModel]
            elif self.webplate == None and self.contPlates != None:
                connector_plate = [self.plateModel,  self.beam_stiffener_2Model,self.contPlate_L1Model,
                                   self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model]
            else:
                connector_plate = [self.plateModel,  self.beam_stiffener_2Model]

        elif self.endplate_type == "both_way":
            if self.webplate != None and self.contPlates != None:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                                   self.contPlate_L1Model,
                                   self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                                   self.webplate_LModel, self.webplate_RModel]
            elif self.webplate == None and self.contPlates != None:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                                   self.contPlate_L1Model,
                                   self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model]
            else:
                connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model]

        elif self.endplate_type == "flush":
            if self.webplate != None and self.contPlates != None:
                connector_plate = [self.plateModel,
                                   self.contPlate_L1Model,
                                   self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model,
                                   self.webplate_LModel, self.webplate_RModel]
            elif self.webplate == None and self.contPlates != None:
                connector_plate = [self.plateModel,
                                   self.contPlate_L1Model,
                                   self.contPlate_L2Model, self.contPlate_R1Model, self.contPlate_R2Model]
            else:
                if self.loc2 == None:
                    connector_plate = [self.plateModel]
                else:
                    pass


        plates = connector_plate[0]
        for comp in connector_plate[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates

    def get_welded_models(self):
        """

        :return: CAD model for all the welds
        """
        if self.endplate_type == "one_way":
            # if self.numberOfBolts == 12:
            if self.webplate != None and self.contPlates != None:
                welded_sec = [ self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                              self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                               self.webWeldB_LTModel, self.webWeldB_LBModel, self.webWeldB_RTModel,
                               self.webWeldB_RBModel,
                               self.webWeldD_LLModel, self.webWeldD_LRModel, self.webWeldD_RLModel,
                               self.webWeldD_RRModel,
                             self.contWeldR1_U2Model,self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldL1_U2Model, self.contWeldL2_U2Model,
                               self.contWeldL1_L2Model,
                              self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]
            elif self.webplate == None and self.contPlates != None:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                              self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                              self.contWeldR2_U2Model, self.contWeldR1_L2Model,self.contWeldL1_U2Model,
                              self.contWeldL2_U2Model, self.contWeldL1_L2Model,self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]
            else:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                              self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model]



        elif self.endplate_type == "both_way":
            # if self.numberOfBolts == 20:
            if self.webplate != None and self.contPlates != None:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model, self.bcWeldStiffHL_2Model,
                              self.bcWeldStiffHR_2Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_2Model,
                              self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                              self.webWeldB_LTModel, self.webWeldB_LBModel, self.webWeldB_RTModel,
                              self.webWeldB_RBModel,
                              self.webWeldD_LLModel, self.webWeldD_LRModel, self.webWeldD_RLModel,
                              self.webWeldD_RRModel,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
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
            elif self.webplate == None and self.contPlates != None:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model, self.bcWeldStiffHL_2Model,
                              self.bcWeldStiffHR_2Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_2Model,
                              self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                              self.contWeldR2_U2Model, self.contWeldR1_L2Model, self.contWeldL1_U2Model,
                              self.contWeldL2_U2Model, self.contWeldL1_L2Model, self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]
            else:
                welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                              self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model, self.bcWeldStiffHL_2Model,
                              self.bcWeldStiffHR_2Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_2Model,
                              self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model]

        elif self.endplate_type == "flush":
            if self.webplate != None and self.contPlates != None:
                welded_sec = [self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                              self.webWeldB_LTModel, self.webWeldB_LBModel, self.webWeldB_RTModel,
                              self.webWeldB_RBModel,
                              self.webWeldD_LLModel, self.webWeldD_LRModel, self.webWeldD_RLModel,
                              self.webWeldD_RRModel,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
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
            elif self.webplate == None and self.contPlates != None:
                welded_sec = [self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                              self.contWeldR2_U2Model, self.contWeldR1_L2Model, self.contWeldL1_U2Model,
                              self.contWeldL2_U2Model, self.contWeldL1_L2Model, self.contWeldL2_L2Model,
                              self.contWeldR1_U2Model, self.contWeldR2_U2Model, self.contWeldR1_L2Model,
                              self.contWeldR2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                              self.contWeldL2_U3Model, self.contWeldL2_L3Model,
                              self.contWeldR1_U3Model, self.contWeldR1_L3Model, self.contWeldR2_U3Model,
                              self.contWeldR2_L3Model, self.contWeldL1_U1Model, self.contWeldL1_L1Model,
                              self.contWeldL2_U1Model, self.contWeldL2_L1Model,
                              self.contWeldR1_U1Model, self.contWeldR1_L1Model, self.contWeldR2_U1Model,
                              self.contWeldR2_L1Model]
            else:
                welded_sec = [self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model]


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
        # CAD_list = [columns, beams, plate_connectors, nut_bolt_array]

        CAD = CAD_list[0]

        for model in CAD_list[1:]:
            CAD = BRepAlgoAPI_Fuse(CAD, model).Shape()

        return CAD


class CADcolwebGroove(CADGroove):


    def createBeamLGeometry(self):
        '''
        initialise the location of the left beam by defining the local origin of the component with respect to global origin
        '''
        beamOriginL = numpy.array([0.0, -self.column.B / 2 +self.column.t / 2, 0.0])

        beamL_uDir = numpy.array([0.0, 1.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.column.place(beamOriginL, beamL_uDir, beamL_wDir)

        ##############################################  Adding contPlates ########################################

    def create_contPlatesGeometry(self):
        '''
        initialise the location of the continuity plate by defining the local origin of the component with respect to global origin
        '''
        beamOriginL = numpy.array(
            [0.0,   self.column.t/2 - self.contPlate_L1.W / 2,
             self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L1.place(beamOriginL, beamL_uDir, beamL_wDir)

        beamOriginL = numpy.array(
            [0.0,  self.column.t/2 - self.contPlate_L2.W / 2,
             self.column.length / 2 - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L2.T / 2])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, -1.0])
        self.contPlate_L2.place(beamOriginL, beamL_uDir, beamL_wDir)

    def create_contWelds(self):
        '''
        initialise the location of the continuity plate weld by defining the local origin of the component with respect to global origin
        '''
        ####top plate top depth weld######
        contWeldL1_U2OriginL = numpy.array([self.column.D / 2 - self.column.T - self.contPlate_L1.L11,  -self.column.B / 2  +self.column.t,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL1_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL1_U2_wDir = numpy.array([-1.0, 0, 0.0])
        self.contWeldL1_U2.place(contWeldL1_U2OriginL, contWeldL1_U2_uDir, contWeldL1_U2_wDir)

        ####bottom plate top depth weld######
        contWeldL2_U2OriginL = numpy.array([self.column.D / 2 - self.column.T - self.contPlate_L1.L11, -self.column.B / 2  +self.column.t, self.column.length / 2
             - self.beam.D / 2 + self.beam.T / 2 + self.contPlate_L1.T / 2])
        contWeldL2_U2_uDir = numpy.array([0.0, 0.0, 1.0])
        contWeldL2_U2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.contWeldL2_U2.place(contWeldL2_U2OriginL, contWeldL2_U2_uDir, contWeldL2_U2_wDir)

        ####top plate bottom depth weld######
        contWeldL1_L2OriginL = numpy.array([self.column.D / 2 -self.column.T - self.contPlate_L1.L11,   -self.column.B / 2  +self.column.t ,
                                            self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL1_L2_uDir = numpy.array([0.0, 1.0, 0.0])
        contWeldL1_L2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.contWeldL1_L2.place(contWeldL1_L2OriginL, contWeldL1_L2_uDir, contWeldL1_L2_wDir)

        ####bottom plate bottom depth weld######
        contWeldL2_L2OriginL = numpy.array(
            [self.column.D / 2 -self.column.T - self.contPlate_L1.L11,   -self.column.B / 2  +self.column.t , self.column.length / 2
             - self.beam.D / 2 + self.beam.T / 2 - self.contPlate_L1.T / 2])
        contWeldL2_L2_uDir = numpy.array([0.0, 1.0, 0.0])
        contWeldL2_L2_wDir = numpy.array([-1.0, 0.0, 0.0])
        self.contWeldL2_L2.place(contWeldL2_L2OriginL, contWeldL2_L2_uDir, contWeldL2_L2_wDir)

        ####top plate right top weld######
        contWeldL1_U3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.t/2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U3 = numpy.array([0.0, 0.0, 1.0])
        wDircontWeldL1_U3 = numpy.array([0.0, -1, 0])
        self.contWeldL1_U3.place(contWeldL1_U3OriginL, uDircontWeldL1_U3, wDircontWeldL1_U3)

        ####top plate right bottom weld######
        contWeldL1_L3OriginL = numpy.array([self.contPlate_L1.L / 2,  self.column.t/2,
                                            self.column.length / 2 + (
                                                    self.beam.D / 2) - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L3 = numpy.array([-1, 0, 0.0])
        wDircontWeldL1_L3 = numpy.array([0.0, -1.0, 0])
        self.contWeldL1_L3.place(contWeldL1_L3OriginL, uDircontWeldL1_L3, wDircontWeldL1_L3)

        ####bottom plate right top weld######
        contWeldL2_U3OriginL = numpy.array([self.contPlate_L1.L / 2 , self.column.t/2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U3 = numpy.array([0, 0.0, 1.0])
        wDircontWeldL2_U3 = numpy.array([0, -1, 0])
        self.contWeldL2_U3.place(contWeldL2_U3OriginL, uDircontWeldL2_U3, wDircontWeldL2_U3)

        ####bottom plate right bottom weld######
        contWeldL2_L3OriginL = numpy.array([self.contPlate_L1.L / 2, self.column.t/2,
                                            self.column.length / 2 - (
                                                    self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L3 = numpy.array([-1, 0.0, 0.0])
        wDircontWeldL2_L3 = numpy.array([0.0, -1, 0])
        self.contWeldL2_L3.place(contWeldL2_L3OriginL, uDircontWeldL2_L3, wDircontWeldL2_L3)

        ####top plate left top weld######
        contWeldL1_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2, -self.column.B/2 +self.column.t  + self.contPlate_L1.L11,
             self.column.length / 2 + (self.beam.D / 2) - self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL1_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL1_U1 = numpy.array([0.0, 1, 0])
        self.contWeldL1_U1.place(contWeldL1_U1OriginL, uDircontWeldL1_U1, wDircontWeldL1_U1)

        ####top plate left bottom weld######
        contWeldL1_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2,  -self.column.B/2 +self.column.t  + self.contPlate_L1.L11,
             self.column.length / 2 + self.beam.D / 2 - self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL1_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL1_L1 = numpy.array([0.0, 1.0, 0.0])
        self.contWeldL1_L1.place(contWeldL1_L1OriginL, uDircontWeldL1_L1, wDircontWeldL1_L1)

        ####bottom plate left top weld######
        contWeldL2_U1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2,  -self.column.B/2 +self.column.t + self.contPlate_L1.L11,
             self.column.length / 2 - (self.beam.D / 2) + self.beam.T / 2 + self.contPlate_L1.T / 2])
        uDircontWeldL2_U1 = numpy.array([0, 0, 1.0])
        wDircontWeldL2_U1 = numpy.array([0, 1, 0])
        self.contWeldL2_U1.place(contWeldL2_U1OriginL, uDircontWeldL2_U1, wDircontWeldL2_U1)

        ####bottom plate left bottom weld######
        contWeldL2_L1OriginL = numpy.array(
            [-self.contPlate_L1.L / 2,  -self.column.B/2 +self.column.t  + self.contPlate_L1.L11,
             self.column.length / 2 - (self.beam.D / 2) + self.beam.T / 2 - self.contPlate_L1.T / 2])
        uDircontWeldL2_L1 = numpy.array([1.0, 0.0, 0.0])
        wDircontWeldL2_L1 = numpy.array([0.0, 1.0, 0])
        self.contWeldL2_L1.place(contWeldL2_L1OriginL, uDircontWeldL2_L1, wDircontWeldL2_L1)



    def get_plate_connector_models(self):
        """
        :return: CAD model for all the plates and stiffener
        """
        if self.endplate_type == "one_way":
             connector_plate = [self.plateModel, self.beam_stiffener_2Model, self.contPlate_L1Model,
                               self.contPlate_L2Model]

        elif self.endplate_type == "both_way":

            connector_plate = [self.plateModel, self.beam_stiffener_1Model, self.beam_stiffener_2Model,
                               self.contPlate_L1Model, self.contPlate_L2Model ]

        elif self.endplate_type == "flush":
            connector_plate = [self.plateModel,
                               self.contPlate_L1Model, self.contPlate_L2Model]

        plates = connector_plate[0]
        for comp in connector_plate[1:]:
            plates = BRepAlgoAPI_Fuse(comp, plates).Shape()

        return plates


    def get_welded_models(self):
        """

        :return: CAD model for all the welds
        """
        if self.endplate_type == "one_way":

            welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHR_1Model,
                          self.bcWeldStiffLL_1Model, self.bcWeldStiffLR_1Model,
                          self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                          self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                          self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                          self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                          self.contWeldL1_L1Model,
                          self.contWeldL2_U1Model, self.contWeldL2_L1Model
                          ]


        elif self.endplate_type == "both_way":

            welded_sec = [self.bcWeldStiffHL_1Model, self.bcWeldStiffHL_2Model, self.bcWeldStiffHR_1Model,
                          self.bcWeldStiffHR_2Model,
                          self.bcWeldStiffLL_1Model, self.bcWeldStiffLL_2Model, self.bcWeldStiffLR_1Model,
                          self.bcWeldStiffLR_2Model,
                          self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                          self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                          self.contWeldL2_L2Model, self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                          self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                          self.contWeldL1_L1Model,
                          self.contWeldL2_U1Model, self.contWeldL2_L1Model
                          ]


        elif self.endplate_type == "flush":
            welded_sec = [self.bcWeldFlang_R1Model, self.bcWeldFlang_R2Model, self.bcWeldWeb_R3Model,
                          self.contWeldL1_U2Model, self.contWeldL2_U2Model, self.contWeldL1_L2Model,
                          self.contWeldL2_L2Model,
                          self.contWeldL1_U3Model, self.contWeldL1_L3Model,
                          self.contWeldL2_U3Model, self.contWeldL2_L3Model, self.contWeldL1_U1Model,
                          self.contWeldL1_L1Model, self.contWeldL2_U1Model,self.contWeldL2_L1Model
                          ]


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
