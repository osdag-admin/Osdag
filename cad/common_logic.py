'''
Created on 18-Nov-2016

@author: deepa,
modified : Sourabh Das, Darshan Vishwakarma
'''

# from utils.common.component import Bolt,Beam,Section,Angle,Plate,Nut,Column,Weld
from cad.items.notch import Notch
from cad.items.bolt import Bolt
from cad.items.nut import Nut
from cad.items.plate import Plate
from cad.items.washer import Washer
from cad.items.ISection import ISection
from cad.items.filletweld import FilletWeld
from cad.items.groove_weld import GrooveWeld
from cad.items.angle import Angle
from cad.items.anchor_bolt import AnchorBolt_A, AnchorBolt_B, AnchorBolt_Endplate
from cad.items.stiffener_plate import StiffenerPlate
from cad.items.grout import Grout
from cad.items.angle import Angle
from cad.items.channel import Channel
from cad.items.Gasset_plate import GassetPlate
from cad.items.stiffener_flange import Stiffener_flange
from cad.items.rect_hollow import RectHollow
from cad.items.circular_hollow import CircularHollow

from cad.ShearConnections.FinPlate.beamWebBeamWebConnectivity import BeamWebBeamWeb as FinBeamWebBeamWeb
from cad.ShearConnections.FinPlate.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as FinColFlangeBeamWeb
from cad.ShearConnections.FinPlate.colWebBeamWebConnectivity import ColWebBeamWeb as FinColWebBeamWeb
from cad.ShearConnections.FinPlate.nutBoltPlacement import NutBoltArray as finNutBoltArray

from cad.ShearConnections.CleatAngle.beamWebBeamWebConnectivity import BeamWebBeamWeb as cleatBeamWebBeamWeb
from cad.ShearConnections.CleatAngle.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as cleatColFlangeBeamWeb
from cad.ShearConnections.CleatAngle.colWebBeamWebConnectivity import ColWebBeamWeb as cleatColWebBeamWeb
from cad.ShearConnections.CleatAngle.nutBoltPlacement import NutBoltArray as cleatNutBoltArray

from cad.ShearConnections.EndPlate.beamWebBeamWebConnectivity import BeamWebBeamWeb as EndBeamWebBeamWeb
from cad.ShearConnections.EndPlate.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as EndColFlangeBeamWeb
from cad.ShearConnections.EndPlate.colWebBeamWebConnectivity import ColWebBeamWeb as EndColWebBeamWeb
from cad.ShearConnections.EndPlate.nutBoltPlacement import NutBoltArray as endNutBoltArray

from cad.ShearConnections.SeatedAngle.CAD_col_web_beam_web_connectivity import ColWebBeamWeb as seatColWebBeamWeb
from cad.ShearConnections.SeatedAngle.CAD_col_flange_beam_web_connectivity import ColFlangeBeamWeb as seatColFlangeBeamWeb
from cad.ShearConnections.SeatedAngle.CAD_nut_bolt_placement import NutBoltArray as seatNutBoltArray
# from cad.ShearConnections.SeatedAngle.seat_angle_calc import SeatAngleCalculation

from cad.BBCad.nutBoltPlacement_AF import NutBoltArray_AF
from cad.BBCad.nutBoltPlacement_BF import NutBoltArray_BF
from cad.BBCad.nutBoltPlacement_Web import NutBoltArray_Web
from cad.BBCad.BBCoverPlateBoltedCAD import BBCoverPlateBoltedCAD

from cad.MomentConnections.BBSpliceCoverlateCAD.WeldedCAD import BBSpliceCoverPlateWeldedCAD
from cad.MomentConnections.BBEndplate.BBEndplate_cadFile import CADFillet
from cad.MomentConnections.BBEndplate.BBEndplate_cadFile import CADGroove
from cad.MomentConnections.BCEndplate.BCEndplate_cadfile import CADGroove as BCECADGroove
from cad.MomentConnections.BCEndplate.BCEndplate_cadfile import CADcolwebGroove

from cad.MomentConnections.CCSpliceCoverPlateCAD.WeldedCAD import CCSpliceCoverPlateWeldedCAD
from cad.MomentConnections.CCSpliceCoverPlateCAD.BoltedCAD import CCSpliceCoverPlateBoltedCAD
from cad.MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_AF import NutBoltArray_AF as CCSpliceNutBolt_AF
from cad.MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_BF import NutBoltArray_BF as CCSpliceNutBolt_BF
from cad.MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_Web import NutBoltArray_Web as CCSpliceNutBolt_Web

from cad.BasePlateCad.baseplateconnection import BasePlateCad, HollowBasePlateCad
from cad.BasePlateCad.nutBoltPlacement import NutBoltArray as bpNutBoltArray

from cad.Tension.WeldedCAD import TensionAngleWeldCAD, TensionChannelWeldCAD
from cad.Tension.BoltedCAD import TensionAngleBoltCAD, TensionChannelBoltCAD
from cad.Tension.nutBoltPlacement import NutBoltArray as TNutBoltArray
from cad.Tension.intermittentConnections import IntermittentNutBoltPlateArray, IntermittentWelds

from cad.MomentConnections.CCEndPlateCAD.CAD import CCEndPlateCAD
from cad.MomentConnections.CCEndPlateCAD.nutBoltPlacement import NutBoltArray as CEPNutBoltArray

# from design_type.connection.fin_plate_connection import FinPlateConnection
# from design_type.connection.cleat_angle_connection import CleatAngleConnection
from design_type.connection.beam_cover_plate import BeamCoverPlate
# from design_type.connection.base_plate_connection import BasePlateConnection
from utilities import osdag_display_shape, DisplayMsg
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
import copy

from cad.BBCad.nutBoltPlacement_AF import NutBoltArray_AF
from cad.BBCad.nutBoltPlacement_BF import NutBoltArray_BF
from cad.BBCad.nutBoltPlacement_Web import NutBoltArray_Web
from cad.BBCad.BBCoverPlateBoltedCAD import BBCoverPlateBoltedCAD
from cad.MomentConnections.BBEndplate.BBE_nutBoltPlacement import BBENutBoltArray
from cad.MomentConnections.BCEndplate.BCE_nutBoltPlacement import BCE_NutBoltArray
from Common import *
from math import *

# from Connections.Shear.Finplate.colWebBeamWebConnectivity import ColWebBeamWeb as finColWebBeamWeb
# from Connections.Shear.Endplate.colWebBeamWebConnectivity import ColWebBeamWeb as endColWebBeamWeb
# from Connections.Shear.cleatAngle.colWebBeamWebConnectivity import ColWebBeamWeb as cleatColWebBeamWeb
# from Connections.Shear.SeatedAngle.CAD_col_web_beam_web_connectivity import ColWebBeamWeb as seatColWebBeamWeb
#
# from Connections.Shear.Finplate.beamWebBeamWebConnectivity import BeamWebBeamWeb as finBeamWebBeamWeb
# from Connections.Shear.Endplate.beamWebBeamWebConnectivity import BeamWebBeamWeb as endBeamWebBeamWeb
# from Connections.Shear.cleatAngle.beamWebBeamWebConnectivity import BeamWebBeamWeb as cleatBeamWebBeamWeb
#
# from Connections.Shear.Finplate.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as finColFlangeBeamWeb
# from Connections.Shear.Endplate.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as endColFlangeBeamWeb
# from Connections.Shear.cleatAngle.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as cleatColFlangeBeamWeb
# from Connections.Shear.SeatedAngle.CAD_col_flange_beam_web_connectivity import ColFlangeBeamWeb as seatColFlangeBeamWeb

# from Connections.Shear.Finplate.finPlateCalc import finConn
# from Connections.Shear.Endplate.endPlateCalc import end_connection
# from Connections.Shear.cleatAngle.cleatCalculation import cleat_connection
# from Connections.Shear.SeatedAngle.seat_angle_calc import SeatAngleCalculation
# from Connections.Component.filletweld import FilletWeld
# from Connections.Component.plate import Plate
# from Connections.Component.bolt import Bolt
# from Connections.Component.nut import Nut
# from Connections.Component.notch import Notch
# from Connections.Component.ISection import ISection
# from Connections.Component.angle import Angle
# from Connections.Shear.Finplate.nutBoltPlacement import NutBoltArray as finNutBoltArray
# from Connections.Shear.Endplate.nutBoltPlacement import NutBoltArray as endNutBoltArray
# from Connections.Shear.cleatAngle.nutBoltPlacement import NutBoltArray as cleatNutBoltArray
# from Connections.Shear.SeatedAngle.CAD_nut_bolt_placement import NutBoltArray as seatNutBoltArray
# from utilities import osdag_display_shape

from OCC.Core.gp import (gp_Vec, gp_Pnt, gp_Trsf, gp_OX, gp_OY,
                         gp_OZ, gp_XYZ, gp_Ax2, gp_Dir, gp_GTrsf, gp_Mat)
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge,
                                     BRepBuilderAPI_MakeVertex,
                                     BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge2d,
                                     BRepBuilderAPI_Transform)

import OCC.Core.V3d
from OCC.Core.Quantity import *
from OCC.Core.Graphic3d import *
from OCC.Core.Quantity import Quantity_NOC_GRAY25 as GRAY
# from OCC.Core.AIS import Erase
# from OCC.Display.OCCViewer import V3d_XposYnegZneg
from OCC.Core.TNaming import tnaming
import multiprocessing

# from Connections.Shear.Finplate.drawing_2D import FinCommonData
# from Connections.Shear.Endplate.drawing_2D import EndCommonData
# from Connections.Shear.cleatAngle.drawing2D import cleatCommonData
# from Connections.Shear.SeatedAngle.drawing_2D import SeatCommonData
#
# from Connections.Shear.Finplate.reportGenerator import save_html as fin_save_html
# from Connections.Shear.Endplate.reportGenerator import save_html as end_save_html
# from Connections.Shear.cleatAngle.reportGenerator import save_html as cleat_save_html
# from Connections.Shear.SeatedAngle.design_report_generator import ReportGenerator
# ----------------------------------------- from reportGenerator import save_html


class CommonDesignLogic(object):
    # --------------------------------------------- def __init__(self, **kwargs):
    # -------------------------------------------- self.uiObj = kwargs[uiObj]
    # ------------------------------ self.dictbeamdata = kwargs[dictbeamdata]
    # -------------------------------- self.dictcoldata = kwargs[dictcoldata]
    # ------------------------------------------------ self.loc = kwargs[loc]
    # ------------------------------------ self.component = kwargs[component]
    # ------------------------------------------ self.bolt_R = kwargs[bolt_R]
    # ------------------------------------------ self.bolt_T = kwargs[bolt_T]
    # ---------------------------------------- self.bolt_Ht = kwargs[bolt_Ht]
    # -------------------------------------------- self.nut_T = kwargs[nut_T]
    # ----------------------------------------- self.display =kwargs[display]
    # --------------------------- self.resultObj = self.call_finCalculation()
    # ------------------------------------------- self.connectivityObj = None


    def __init__(self, display, folder, connection, mainmodule):

        self.display = display
        self.mainmodule = mainmodule
        self.connection = connection
        print(self.connection)


        self.connectivityObj = None
        self.folder = folder


    def get_notch_ht(self, PB_T, PB_R1, SB_T, SB_R1):
        """
        Args:
            PB_T: (Float)Flange thickness of Primary beam
            PB_R1: (Float) Root radius of Primary beam
            SB_T: (Float) Flange thickness of Secondary beam
            SB_R1: (Float) Root radius of Secondary beam

        Returns: (Float)Height of the coping based on maximum of sectional properties of Primary beam and Secondary beam

        """
        notch_ht = max([PB_T, SB_T]) + max([PB_R1, SB_R1]) + max([(PB_T/2), (SB_T/2),10])

        return notch_ht

    def boltHeadThick_Calculation(self, boltDia):
        '''
        This routine takes the bolt diameter and return bolt head thickness as per IS:3757(1989) and IS:1364 (PART-1) : 2002


       bolt Head Dia
        <-------->
        __________
        |        | | T = Thickness
        |________| |
           |  |
           |  |
           |  |

        Note: The head thickness for diameter 72 has been assumed and not taken from the IS code

        '''
        boltHeadThick = {5: 3.5, 6: 4, 8: 5.3, 10: 6.4, 12: 7.5, 14: 8.8, 16: 10, 18: 11.5, 20: 12.5, 22: 14, 24: 15,
                         27: 17, 30: 18.7, 33: 21, 36: 22.5, 39: 25, 42: 26, 45: 28, 48: 30, 52: 33, 56: 35, 60: 38, 64: 40, 72: 45}
        return boltHeadThick[boltDia]

    def boltHeadDia_Calculation(self, boltDia):
        '''
        This routine takes the bolt diameter and return bolt head diameter as per IS:3757(1989) and IS:1364 (PART-1) : 2002

       bolt Head Dia
        <-------->
        __________
        |        |
        |________|
           |  |
           |  |
           |  |

        '''
        boltHeadDia = {5: 8, 6: 10, 8: 13, 10: 16, 12: 18, 14: 21, 16: 24, 18: 27, 20: 30, 22: 34, 24: 36, 27: 41,
                       30: 46, 33: 50, 36: 55, 39: 60, 42: 65, 45: 70, 48: 75, 52: 80, 56: 85, 60: 90, 64: 95, 72: 110}
        return boltHeadDia[boltDia]

    def boltLength_Calculation(self, boltDia):
        '''
        This routine takes the bolt diameter and return bolt head diameter as per IS:3757(1985)

       bolt Head Dia
        <-------->
        __________  ______
        |        |    |
        |________|    |
           |  |       |
           |  |       |
           |  |       |
           |  |       |
           |  |       |  l= length
           |  |       |
           |  |       |
           |  |       |
           |__|    ___|__

        '''
        # boltHeadDia = {5: 40, 6: 40, 8: 40, 10: 40, 12: 40, 16: 50, 20: 50, 22: 50, 24: 50, 27: 60, 30: 65, 36: 75}

        '''
        This routine takes the bolt diameter and return bolt head diameter as per IS:1364 (PART-1) : 2002

        __________ 
        |        |  
        |________|  ______
           |  |       |
           |  |       |
           |  |       |
           |  |       |
           |  |       |  l= length
           |  |       |
           |  |       |
           |  |       |
           |__|    ___|__

        '''
        boltLength = {5: 25, 6: 30, 8: 40, 10: 45, 12: 50, 14: 60, 16: 65, 18: 70, 20: 80, 22: 90, 24: 90, 27: 100,
                      30: 110, 33: 130, 36: 140, 39: 150, 42: 180, 45: 200, 48: 220, 52: 240, 56: 260, 60: 280, 64: 300, 72: 320}

        return boltLength[boltDia]

    @staticmethod
    def nutThick_Calculation(boltDia):
        '''
        Returns the thickness of the hexagon nut (Grade A and B) depending upon the nut diameter as per IS1364-3(2002) - Table 1

        Note: The nut thk for 72 diameter is not available in IS code, however an approximated value is assumed.
              72 mm dia bolt is used in the base plate module.
        '''

        # nutDia = {5: 5, 6: 5.65, 8: 7.15, 10: 8.75, 12: 11.3, 16: 15, 20: 17.95, 22: 19.0, 24: 21.25, 27: 23, 30: 25.35,
        #           36: 30.65}

        '''
        Returns the thickness of the nut depending upon the nut diameter as per IS1364-3(2002)
        '''
        nutDia = {5: 4.7, 6: 5.2, 8: 6.8, 10: 8.4, 12: 10.8, 14: 12.8, 16: 14.8, 18: 15.8, 20: 18.0, 22: 19.4, 24: 21.5, 27: 23.8, 30: 25.6,
                  33: 28.7, 36: 31, 39: 33.4, 42: 34.0, 45: 36, 48: 38.0, 52: 42, 56: 45.0, 60: 48, 64: 51.0, 72: 60.0}

        return nutDia[boltDia]


    def create3DBeamWebBeamWeb(self):
        '''self,uiObj,resultObj,dictbeamdata,dictcoldata):
        creating 3d cad model with beam web beam web

        '''

        A = self.module_class()

        if self.connection == KEY_DISP_FINPLATE:
            # A = self.module_class()
            # A = FinPlateConnection()
            plate = Plate(L=A.plate.height, W=A.plate.length, T=A.plate.thickness_provided)
            Fweld1 = FilletWeld(L=A.weld.length, b=A.weld.size, h=A.weld.size)

        elif self.connection == KEY_DISP_CLEATANGLE:
            # A = CleatAngleConnection()
            angle = Angle(L=A.cleat.height, A=A.cleat.leg_a_length, B=A.cleat.leg_b_length, T=A.cleat.thickness,
                          R1=A.cleat.root_radius, R2=A.cleat.toe_radius)

        elif self.connection == KEY_DISP_ENDPLATE:
            # A = self.module_class()
            plate = Plate(L=A.plate.height, W=A.plate.width, T=A.plate.thickness_provided)
            Fweld1 = FilletWeld(L=A.plate.height, b=A.weld.size, h=A.weld.size)

        else:
            pass

        bolt_dia = int(A.bolt.bolt_diameter_provided)
        bolt_r = bolt_dia / 2.0
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2.0
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = bolt_dia
        notch_height = A.supported_section.notch_ht
        notch_R1 = max([A.supporting_section.root_radius, A.supported_section.root_radius, 10])

        ##### SECONDARY BEAM PARAMETERS ######


        # --Notch dimensions
        if self.connection == KEY_DISP_FINPLATE:
            gap = A.plate.gap
            notchObj = Notch(R1=notch_R1,
                             height=notch_height,
                             # width= (pBeam_B/2.0 - (pBeam_tw/2.0 ))+ gap,
                             width=(A.supporting_section.flange_width / 2.0 - (
                                         A.supporting_section.web_thickness / 2.0 + gap)) + gap,
                             length=A.supported_section.flange_width)

        elif self.connection == KEY_DISP_CLEATANGLE:
            gap = A.cleat.gap
            notchObj = Notch(R1=notch_R1,
                             height=notch_height,
                             width=(A.supporting_section.flange_width / 2.0 - (
                                     A.supporting_section.web_thickness / 2.0 + gap)) + gap,
                             length=A.supported_section.flange_width)
            # print(notch_R1,notch_height,(A.supporting_section.flange_width / 2.0 -
            #                              (A.supporting_section.web_thickness / 2.0 + gap)) + gap, A.supported_section.flange_width)

        elif self.connection == KEY_DISP_ENDPLATE:
            notchObj = Notch(R1=notch_R1, height=notch_height,
                             width=(A.supporting_section.flange_width / 2.0 - (
                                     A.supporting_section.web_thickness / 2.0 + A.plate.thickness_provided)) + A.plate.gap,
                             length=A.supported_section.flange_width)

        else:
            pass
            # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
            #
            # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)

        supporting = ISection(B=A.supporting_section.flange_width, T=A.supporting_section.flange_thickness,
                              D=A.supporting_section.depth, t=A.supporting_section.web_thickness,
                              R1=A.supporting_section.root_radius, R2=A.supporting_section.toe_radius,
                              alpha=A.supporting_section.flange_slope,
                              length=1000, notchObj=None)

        supported = ISection(B=A.supported_section.flange_width, T=A.supported_section.flange_thickness,
                             D=A.supported_section.depth,
                             t=A.supported_section.web_thickness, R1=A.supported_section.root_radius,
                             R2=A.supported_section.toe_radius,
                             alpha=A.supported_section.flange_slope, length=500, notchObj=notchObj)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == KEY_DISP_FINPLATE:  # finBeamWebBeamWeb/endBeamWebBeamWeb
            nut_space = A.supported_section.web_thickness + A.plate.thickness_provided + nut_T
            nutBoltArray = finNutBoltArray(A.bolt,  A.plate, nut, bolt, nut_space)
            beamwebconn = FinBeamWebBeamWeb(supporting, supported, notchObj, plate, Fweld1, nutBoltArray, gap)
            # column, beam, notch, plate, Fweld, nut_bolt_array

        elif self.connection == KEY_DISP_ENDPLATE:
            nut_space = A.supporting_section.web_thickness + A.plate.thickness_provided + nut_T
            nutBoltArray = endNutBoltArray(A.bolt, A.plate, nut, bolt, nut_space)
            beamwebconn = EndBeamWebBeamWeb(supporting, supported, notchObj, Fweld1, plate, nutBoltArray)

        elif self.connection == KEY_DISP_CLEATANGLE:
            # nut_space = sBeam_tw + 2 * cleat_thick + nut_T
            # cnut_space = pBeam_tw + cleat_thick + nut_T
            # nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)
            # beamwebconn = cleatBeamWebBeamWeb(column, beam, notchObj, angle, nut_bolt_array,gap)
            nut_space = A.supported_section.web_thickness + 2 * A.cleat.thickness + nut_T
            cnut_space = A.supporting_section.web_thickness + A.cleat.thickness + nut_T
            nut_bolt_array = cleatNutBoltArray(A.cleat, nut, bolt, nut_space, cnut_space)
            beamwebconn = cleatBeamWebBeamWeb(supporting, supported, notchObj, angle, nut_bolt_array,gap)

        else:
            pass

        beamwebconn.create_3dmodel()

        return beamwebconn

    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web

        '''

        A = self.module_class()

        # if self.connection == KEY_DISP_FINPLATE:
            # A = self.module_class()
            # A = FinPlateConnection()
        if self.connection == KEY_DISP_CLEATANGLE:
            # A = CleatAngleConnection()
            angle = Angle(L=A.cleat.height, A=A.cleat.leg_a_length, B=A.cleat.leg_b_length, T=A.cleat.thickness,
                          R1=A.cleat.root_radius, R2=A.cleat.toe_radius)

        elif self.connection == KEY_DISP_SEATED_ANGLE:
            angle = Angle(L=A.seated_angle.width, A=A.seated.leg_a_length, B=A.seated.leg_b_length,
                          T=A.seated.thickness, R1=A.seated.root_radius, R2=A.seated.toe_radius)
        else:
            pass
        #### PLATE,BOLT,ANGLE AND NUT PARAMETERS #####

        # if self.connection == "cleatAngle":
        #     cleat_length = self.resultObj['cleat']['height']
        #     cleat_thick = float(self.dictangledata["t"])
        #     cleat_legsizes = str(self.dictangledata["AXB"])
        #     angle_A = int(cleat_legsizes.split('x')[0])
        #     angle_B = int(cleat_legsizes.split('x')[1])
        #     angle_r1 = float(str(self.dictangledata["R1"]))
        #     angle_r2 = float(str(self.dictangledata["R2"]))
        #
        # elif self.connection == 'SeatedAngle':
        #     seat_length = self.resultObj['SeatAngle']['Length (mm)']
        #     seat_thick = float(self.dictangledata["t"])
        #     seat_legsizes = str(self.dictangledata["AXB"])
        #     seatangle_A = int(seat_legsizes.split('x')[0])
        #     seatangle_B = int(seat_legsizes.split('x')[1])
        #     seatangle_r1 = float(str(self.dictangledata["R1"]))
        #     seatangle_r2 = float(str(self.dictangledata["R2"]))
        #
        #     topangle_length = self.resultObj['SeatAngle']['Length (mm)']
        #     topangle_thick = float(self.dicttopangledata["t"])
        #     top_legsizes = str(self.dicttopangledata["AXB"])
        #     topangle_A = int(top_legsizes.split('x')[0])
        #     topangle_B = int(top_legsizes.split('x')[1])
        #     topangle_r1 = float(str(self.dicttopangledata["R1"]))
        #     topangle_r2 = float(str(self.dicttopangledata["R2"]))
        # else:
        #     fillet_length = self.resultObj['Plate']['height']
        #     fillet_thickness = str(self.uiObj['Weld']['Size (mm)'])
        #     plate_width = self.resultObj['Plate']['width']
        #     plate_thick = str(self.uiObj['Plate']['Thickness (mm)'])

        bolt_dia = int(A.bolt.bolt_diameter_provided)
        bolt_r = bolt_dia / 2.0
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2.0
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = bolt_dia
        # notch_height = A.supported_section.notch_ht
        # notch_R1 = max([A.supporting_section.root_radius, A.supported_section.root_radius, 10])

        if self.connection == KEY_DISP_CLEATANGLE:
            gap = A.cleat.gap
            # notchObj = Notch(R1=notch_R1,
            #                  height=notch_height,
            #                  width=(A.supporting_section.flange_width / 2.0 - (
            #                          A.supporting_section.web_thickness / 2.0 + gap)) + gap,
            #                  length=A.supported_section.flange_width)
            # print(notch_R1, notch_height, (A.supporting_section.flange_width / 2.0 -
            #                                (A.supporting_section.web_thickness / 2.0 + gap)) + gap,
            #       A.supported_section.flange_width)
        elif self.connection == KEY_DISP_SEATED_ANGLE:
            gap = A.plate.gap
            seatangle = Angle(L=A.seated_angle.width, A=A.seated.leg_a_length, B=A.seated.leg_b_length,     #TODO:Check leg b length
                              T=A.seated.thickness, R1=A.seated.root_radius, R2=A.seated.toe_radius)
            topclipangle = Angle(L=A.top_angle.width, A=A.top_angle.leg_a_length, B=A.top_angle.leg_b_length,
                                 T=A.top_angle.thickness, R1=A.top_angle.root_radius, R2=A.top_angle.toe_radius)

        elif self.connection == KEY_DISP_ENDPLATE:
            plate = Plate(L=A.plate.height, W=A.plate.width, T=A.plate.thickness_provided)
            Fweld1 = FilletWeld(L=A.weld.length, b=A.weld.size, h=A.weld.size)

        else:
            plate = Plate(L=A.plate.height, W=A.plate.length, T=A.plate.thickness_provided)
            Fweld1 = FilletWeld(L=A.weld.length, b=A.weld.size, h=A.weld.size)

        supporting = ISection(B=A.supporting_section.flange_width, T=A.supporting_section.flange_thickness,
                              D=A.supporting_section.depth, t=A.supporting_section.web_thickness,
                              R1=A.supporting_section.root_radius, R2=A.supporting_section.toe_radius,
                              alpha=A.supporting_section.flange_slope,
                              length=max(1000, (500 + A.supported_section.depth)), notchObj=None)
        supported = ISection(B=A.supported_section.flange_width, T=A.supported_section.flange_thickness,
                             D=A.supported_section.depth,
                             t=A.supported_section.web_thickness, R1=A.supported_section.root_radius,
                             R2=A.supported_section.toe_radius,
                             alpha=A.supported_section.flange_slope, length=500, notchObj=None)

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == KEY_DISP_FINPLATE:  # finColWebBeamWeb
            gap = A.plate.gap
            nut_space = A.supported_section.web_thickness + int(A.plate.thickness_provided) + nut_T
            nutBoltArray = finNutBoltArray(A.bolt, A.plate, nut, bolt, nut_space)
            colwebconn = FinColWebBeamWeb(supporting, supported, Fweld1, plate, nutBoltArray,gap)

        elif self.connection == KEY_DISP_ENDPLATE:
            nut_space = A.supporting_section.web_thickness + int(A.plate.thickness_provided) + nut_T
            nutBoltArray = endNutBoltArray(A.bolt, A.plate, nut, bolt, nut_space)
            colwebconn = EndColWebBeamWeb(supporting, supported, Fweld1, plate, nutBoltArray)

        elif self.connection == KEY_DISP_CLEATANGLE:
            # nut_space = beam_tw + 2 * cleat_thick + nut_T
            # cnut_space = column_tw + cleat_thick + nut_T
            # nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)
            # colwebconn = cleatColWebBeamWeb(column, beam, angle, nut_bolt_array,gap)
            nut_space = A.supported_section.web_thickness + 2 * A.cleat.thickness + nut_T
            cnut_space = A.supporting_section.web_thickness + A.cleat.thickness + nut_T
            nut_bolt_array = cleatNutBoltArray(A.cleat, nut, bolt, nut_space, cnut_space)
            colwebconn = cleatColWebBeamWeb(supporting, supported, angle, nut_bolt_array, gap)

        else:
            snut_space = A.supporting_section.web_thickness + A.seated.thickness + nut_T
            sbnut_space = A.supported_section.flange_thickness + A.seated.thickness + nut_T
            tnut_space = A.supported_section.flange_thickness + A.top_angle.thickness + nut_T
            tbnut_space = A.supporting_section.web_thickness + A.top_angle.thickness + nut_T

            nutBoltArray = seatNutBoltArray(A.bolt, nut, bolt, snut_space, sbnut_space, tnut_space, tbnut_space)
            colwebconn = seatColWebBeamWeb(supporting, supported, seatangle, topclipangle, nutBoltArray, gap)

        colwebconn.create_3dmodel()
        return colwebconn

    def create3DColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection

        '''

        A = self.module_class()

        if self.connection == KEY_DISP_FINPLATE:
            # A = self.module_class()
            # A = FinPlateConnection()
            gap = A.plate.gap
        elif self.connection == KEY_DISP_CLEATANGLE:
            # A = CleatAngleConnection()
            angle = Angle(L=A.cleat.height, A=A.cleat.leg_a_length, B=A.cleat.leg_b_length, T=A.cleat.thickness,
                          R1=A.cleat.root_radius, R2=A.cleat.toe_radius)
        elif self.connection == KEY_DISP_SEATED_ANGLE:
            angle = Angle(L=A.seated_angle.width, A=A.seated.leg_a_length, B=A.seated.leg_b_length,
                          T=A.seated.thickness, R1=A.seated.root_radius, R2=A.seated.toe_radius)
        else:
            pass

        bolt_dia = int(A.bolt.bolt_diameter_provided)
        bolt_r = bolt_dia / 2.0
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2.0
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = bolt_dia
        # gap = A.plate.gap
        # notch_height = A.supported_section.notch_ht
        # notch_R1 = max([A.supporting_section.root_radius, A.supported_section.root_radius, 10])

        if self.connection == KEY_DISP_CLEATANGLE:
            gap = A.cleat.gap
            # notchObj = Notch(R1=notch_R1,
            #                  height=notch_height,
            #                  width=(A.supporting_section.flange_width / 2.0 - (
            #                          A.supporting_section.web_thickness / 2.0 + gap)) + gap,
            #                  length=A.supported_section.flange_width)
            # print(notch_R1, notch_height, (A.supporting_section.flange_width / 2.0 -
            #                                (A.supporting_section.web_thickness / 2.0 + gap)) + gap,
            #       A.supported_section.flange_width)

        elif self.connection == KEY_DISP_SEATED_ANGLE:
            gap = A.plate.gap
            seatangle = Angle(L=A.seated_angle.width, A=A.seated.leg_a_length, B=A.seated.leg_b_length,     #TODO:Check leg b length
                              T=A.seated.thickness, R1=A.seated.root_radius, R2=A.seated.toe_radius)
            topclipangle = Angle(L=A.top_angle.width, A=A.top_angle.leg_a_length, B=A.top_angle.leg_b_length,
                                 T=A.top_angle.thickness, R1=A.top_angle.root_radius, R2=A.top_angle.toe_radius)

        elif self.connection == KEY_DISP_ENDPLATE:
            plate = Plate(L=A.plate.height, W=A.plate.width, T=A.plate.thickness_provided)
            Fweld1 = FilletWeld(L=A.weld.length, b=A.weld.size, h=A.weld.size)
        else:
            # plate = Plate(L= 300,W =100, T = 10)
            plate = Plate(L=A.plate.height, W=A.plate.length, T=A.plate.thickness_provided)

            # Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
            Fweld1 = FilletWeld(L=A.weld.length, b=A.weld.size, h=A.weld.size)

        supported = ISection(B=A.supported_section.flange_width, T=A.supported_section.flange_thickness,
                             D=A.supported_section.depth,
                             t=A.supported_section.web_thickness, R1=A.supported_section.root_radius,
                             R2=A.supported_section.toe_radius,
                             alpha=A.supported_section.flange_slope, length=500, notchObj=None)

        supporting = ISection(B=A.supporting_section.flange_width, T=A.supporting_section.flange_thickness,
                              D=A.supporting_section.depth, t=A.supporting_section.web_thickness,
                              R1=A.supporting_section.root_radius, R2=A.supporting_section.toe_radius,
                              alpha=A.supporting_section.flange_slope,
                              length=max(1000, (500 + A.supported_section.depth)), notchObj=None)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == KEY_DISP_FINPLATE:
            nut_space = A.supported_section.web_thickness+ int(A.plate.thickness_provided) + nut_T
            # nutBoltArray = finNutBoltArray(A, nut, bolt, nut_space)  # finColFlangeBeamWeb
            # colflangeconn = finColFlangeBeamWeb(column, beam, Fweld1, plate, nutBoltArray, gap)

            nutBoltArray = finNutBoltArray(A.bolt, A.plate, nut, bolt, nut_space)
            colflangeconn = FinColFlangeBeamWeb(supporting, supported, Fweld1, plate, nutBoltArray,gap)

        elif self.connection == KEY_DISP_ENDPLATE:
            nut_space = A.supporting_section.flange_thickness + int(A.plate.thickness_provided) + nut_T
            nutBoltArray = endNutBoltArray(A.bolt, A.plate, nut, bolt, nut_space)
            colflangeconn = EndColFlangeBeamWeb(supporting, supported, Fweld1, plate, nutBoltArray)

        elif self.connection == KEY_DISP_CLEATANGLE:

            # nut_space =  A.supported_section.web_thickness + 2 *  + nut_T
            # cnut_space = column_T + cleat_thick + nut_T
            # nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)
            # colflangeconn = cleatColFlangeBeamWeb(column, beam, angle, nut_bolt_array,gap)
            nut_space = A.supported_section.web_thickness + 2 * A.cleat.thickness + nut_T
            cnut_space = A.supporting_section.flange_thickness + A.cleat.thickness + nut_T
            nut_bolt_array = cleatNutBoltArray(A.cleat, nut, bolt, nut_space, cnut_space)
            colflangeconn = cleatColFlangeBeamWeb(supporting, supported, angle, nut_bolt_array, gap)

        else:
            # pass
            snut_space = A.supporting_section.flange_thickness + A.seated.thickness + nut_T
            sbnut_space = A.supported_section.flange_thickness + A.seated.thickness + nut_T
            tnut_space = A.supported_section.flange_thickness + A.top_angle.thickness + nut_T
            tbnut_space = A.supporting_section.flange_thickness + A.top_angle.thickness + nut_T

            nutBoltArray = seatNutBoltArray(A.bolt, nut, bolt, snut_space, sbnut_space, tnut_space, tbnut_space, True)
            colflangeconn = seatColFlangeBeamWeb(supporting, supported, seatangle, topclipangle, nutBoltArray, gap)
            #

        # else:
        #     snut_space = column_T + seat_thick + nut_T
        #     sbnut_space = beam_T + seat_thick + nut_T
        #     tnut_space = beam_T + topangle_thick + nut_T
        #     tbnut_space = column_T + topangle_thick + nut_T
        #
        #     nutBoltArray = seatNutBoltArray(self.resultObj, nut, bolt, snut_space, sbnut_space, tnut_space, tbnut_space)
        #     colflangeconn = seatColFlangeBeamWeb(column, beam, seatangle, topclipangle, nutBoltArray,gap)

        colflangeconn.create_3dmodel()
        return colflangeconn

    def createBBCoverPlateCAD(self):
        '''
        :return: The calculated values/parameters to create 3D CAD model of individual components.
        '''

        if self.connection == KEY_DISP_BEAMCOVERPLATE:
            B = BeamCoverPlate()
            # beam_data = self.fetchBeamPara()  # Fetches the beam dimensions

            beam_tw = float(B.section.web_thickness)
            beam_T = float(B.section.flange_thickness)
            beam_d = float(B.section.depth)
            beam_B = float(B.section.flange_width)
            beam_R1 = float(B.section.root_radius)
            beam_R2 = float(B.section.toe_radius)
            beam_alpha = float(B.section.flange_slope)
            beam_length = B.flange_plate.length/2+300

            beam_Left = ISection(B=beam_B, T=beam_T, D=beam_d, t=beam_tw,
                                 R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                                 length=beam_length, notchObj=None)  # Call to ISection in Component repository
            beam_Right = copy.copy(beam_Left)  # Since both the beams are same


            plateAbvFlange = Plate(L=B.flange_plate.height,
                                   W=B.flange_plate.length,
                                   T=float(B.flange_plate.thickness_provided))  # Call to Plate in Component repository
            plateBelwFlange = copy.copy(plateAbvFlange)  # Since both the flange plates are identical

            innerplateAbvFlangeFront = Plate(L=B.flange_plate.Innerheight,
                                             W=B.flange_plate.Innerlength,
                                             T=float(B.flange_plate.thickness_provided))
            innerplateAbvFlangeBack = copy.copy(innerplateAbvFlangeFront)
            innerplateBelwFlangeFront = copy.copy(innerplateAbvFlangeBack)
            innerplateBelwFlangeBack = copy.copy(innerplateBelwFlangeFront)

            WebPlateLeft = Plate(L=B.web_plate.height,
                                 W=B.web_plate.length,
                                 T=float(B.web_plate.thickness_provided))  # Call to Plate in Component repository
            WebPlateRight = copy.copy(WebPlateLeft)  # Since both the Web plates are identical

            bolt_d = float(B.flange_bolt.bolt_diameter_provided)  # Bolt diameter (shank part), entered by user
            bolt_r = bolt_d / 2  # Bolt radius (Shank part)
            bolt_T = self.boltHeadThick_Calculation(bolt_d)  # Bolt head thickness
            bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
            bolt_Ht = self.boltLength_Calculation(bolt_d)  # Bolt head height

            bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component directory
            nut_T = self.nutThick_Calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
            nut_Ht = nut_T
            nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)  # Call to create Nut from Component directory

            numOfBoltsF = int(B.flange_plate.bolts_required)  # Number of flange bolts for both beams
            if B.preference == "Outside":
                nutSpaceF = float(
                    B.flange_plate.thickness_provided) + beam_T  # Space between bolt head and nut for flange bolts
            else:
                nutSpaceF = 2 * float(B.flange_plate.thickness_provided) + beam_T

                # TODO : update nutSpace from Osdag test

            numOfBoltsW = int(B.web_plate.bolts_required)  # Number of web bolts for both beams
            nutSpaceW = 2 * float(
                B.web_plate.thickness_provided) + beam_tw  # Space between bolt head and nut for web bolts

            # Bolt placement for Above Flange bolts, call to nutBoltPlacement_AF.py
            bolting_AF = NutBoltArray_AF(BeamCoverPlate(), nut, bolt, numOfBoltsF, nutSpaceF)

            # Bolt placement for Below Flange bolts, call to nutBoltPlacement_BF.py
            bolting_BF = NutBoltArray_BF(BeamCoverPlate(), nut, bolt, numOfBoltsF, nutSpaceF)

            # Bolt placement for Web Plate bolts, call to nutBoltPlacement_Web.py
            bolting_Web = NutBoltArray_Web(BeamCoverPlate(), nut, bolt, numOfBoltsW, nutSpaceW)

            # bbCoverPlate is an object which is passed BBCoverPlateBoltedCAD.py file, which initialized the parameters of each CAD component
            bbCoverPlate = BBCoverPlateBoltedCAD(beam_Left, beam_Right, plateAbvFlange, plateBelwFlange,
                                                 innerplateAbvFlangeFront,
                                                 innerplateAbvFlangeBack, innerplateBelwFlangeFront,
                                                 innerplateBelwFlangeBack,
                                                 WebPlateLeft, WebPlateRight, bolting_AF, bolting_BF, bolting_Web,
                                                 BeamCoverPlate())

            # bbCoverPlate.create_3DModel() will create the CAD model of each component, debugging this line will give moe clarity
            bbCoverPlate.create_3DModel()

        elif self.connection == KEY_DISP_BEAMCOVERPLATEWELD:
            B = self.module_class()
            beamLenght = (max(float(B.flange_plate.length), float(B.web_plate.length)) + 600) / 2
            beam = ISection(B=float(B.section.flange_width), T=float(B.section.flange_thickness),
                            D=float(B.section.depth), t=float(B.section.web_thickness), R1=float(B.section.root_radius),
                            R2=float(B.section.toe_radius), alpha=float(B.section.flange_slope), length=beamLenght,
                            notchObj=None)
            flangePlate = Plate(L=float(B.flange_plate.length), W=float(B.flange_plate.height),
                                T=float(B.flange_plate.thickness_provided))
            innerFlangePlate = Plate(L=float(B.flange_plate.Innerlength), W=float(B.flange_plate.Innerheight),
                                     T=float(B.flange_plate.thickness_provided))
            webPlate = Plate(L=float(B.web_plate.length), W=float(B.web_plate.height),
                             T=float(B.web_plate.thickness_provided))

            flangePlateWeldL = FilletWeld(h=float(B.flange_weld.size), b=float(B.flange_weld.size), L=flangePlate.L)
            flangePlateWeldW = FilletWeld(h=float(B.flange_weld.size), b=float(B.flange_weld.size), L=flangePlate.W)

            innerflangePlateWeldL = FilletWeld(h=float(B.flange_weld.size), b=float(B.flange_weld.size),
                                               L=innerFlangePlate.L)
            innerflangePlateWeldW = FilletWeld(h=float(B.flange_weld.size), b=float(B.flange_weld.size),
                                               L=innerFlangePlate.W)

            webPlateWeldL = FilletWeld(h=float(B.web_weld.size), b=float(B.web_weld.size), L=webPlate.L)
            webPlateWeldW = FilletWeld(h=float(B.web_weld.size), b=float(B.web_weld.size), L=webPlate.W)

            bbCoverPlate = BBSpliceCoverPlateWeldedCAD(B, beam, flangePlate, innerFlangePlate, webPlate,
                                                       flangePlateWeldL, flangePlateWeldW,
                                                       innerflangePlateWeldL,
                                                       innerflangePlateWeldW, webPlateWeldL, webPlateWeldW)

            # bbCoverPlate.create_3DModel() will create the CAD model of each component, debugging this line will give moe clarity
            bbCoverPlate.create_3DModel()

        return bbCoverPlate

    def createBBEndPlateCAD(self):
        """
        Calls the CAD components like beam, plate, stiffeners, fillet and grove weld, nut and bolt. Also calls CAD file
        :return: creates CAD model
        """

        BBE = self.module_class

        beam_tw = float(BBE.beam_tw)
        beam_T = float(BBE.beam_tf)
        beam_d = float(BBE.beam_D)
        beam_B = float(BBE.beam_bf)
        beam_R1 = 0.0
        beam_R2 = 0.0
        beam_alpha = 0.0
        beam_length = 500



        beam_Left = ISection(B=beam_B, T=beam_T, D=beam_d, t=beam_tw,
                             R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                             length=beam_length, notchObj=None)
        beam_Right = copy.copy(beam_Left)  # Since both the beams are same


        plate_Left = Plate(W=BBE.ep_width_provided,
                           L=BBE.ep_height_provided,
                           T=BBE.plate_thickness)
        plate_Right = copy.copy(plate_Left)  # Since both the end plates are identical

        # Beam stiffeners 4 if extended both ways, only 1 and 3 if extended oneway and non for flus type
        beam_stiffeners = StiffenerPlate(W=BBE.stiffener_height, L=BBE.stiffener_length,
                                         T=BBE.stiffener_thickness,
                                         R11=BBE.stiffener_length - 25,
                                         R12=BBE.stiffener_height - 25,
                                         L21=5.0, L22=5.0)  # TODO: given hard inputs to L21 and L22
        #
        # # Beam stiffeners for the flush type endplate
        beam_stiffenerFlush = StiffenerPlate(W=BBE.stiffener_height, L=BBE.stiffener_length,
                                         T=BBE.stiffener_thickness,
                                         L21=5.0, L22=5.0)


        # alist = self.designParameters()  # An object to save all input values entered by user

        bolt_d = float(BBE.bolt_diameter_provided)  # Bolt diameter, entered by user
        bolt_r = bolt_d / 2
        print(bolt_d)
        bolt_T = self.boltHeadThick_Calculation(bolt_d)
        bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2
        bolt_Ht = self.boltLength_Calculation(bolt_d)

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component repo
        nut_T = self.nutThick_Calculation(bolt_d)
        nut_Ht = nut_T
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        numberOfBolts = int(BBE.bolt_numbers)

        nutSpace = 2 * float(BBE.plate_thickness) + nut_T  # Space between bolt head and nut

        bbNutBoltArray = BBENutBoltArray(BBE, nut, bolt, numberOfBolts, nutSpace)

        # Following welds are for to weld stiffeners for extended bothways and ext4ended oneway
        # bbWeld for stiffener hight on left side
        bbWeldStiffHeight = FilletWeld(b=BBE.weld_size_stiffener, h=BBE.weld_size_stiffener,

                                       L=BBE.stiffener_height - 5.0)  # outputobj['Stiffener']['Length'] - 25

        # bbWeld for stiffener length on left side
        bbWeldStiffLength = FilletWeld(b=BBE.weld_size_stiffener, h=BBE.weld_size_stiffener,
                                       L=BBE.stiffener_length-5.0)
        #
        # # following welds are fillet welds for the flush endplate stiffeners
        bbWeldFlushstiffHeight = FilletWeld(b=BBE.weld_size_stiffener, h=BBE.weld_size_stiffener,
                                       L=BBE.stiffener_height-5.0)

        bbWeldFlushstiffLength = FilletWeld(b=BBE.weld_size_stiffener, h=BBE.weld_size_stiffener,
                                       L=BBE.stiffener_length-5.0)
        #
        # # if BBE.weld.type == "Fillet Weld":
        # #
            # Fillet Weld for connecting end plate to beam

        # # Followings welds are welds above beam flange, Qty = 4
        # bbWeldAbvFlang = FilletWeld(b=float(BBE.flange_weld.size), h=float(BBE.flange_weld.size),
        #                             L=beam_B)
        #
        # # Followings welds are welds below beam flange, Qty = 8
        # bbWeldBelwFlang = FilletWeld(b=float(BBE.flange_weld.size), h=float(BBE.flange_weld.size),
        #                              L=(beam_B - beam_tw) / 2 -
        #                                beam_R1 - beam_R2)
        #
        # # Followings welds are welds placed aside of beam web, Qty = 4
        # bbWeldSideWeb = FilletWeld(b=float(BBE.web_weld.size), h=float(BBE.web_weld.size),
        #                            L=beam_d - 2 * (beam_T + beam_R1) - (2 * 5))
        # # #
        # #     extbothWays = BBEndplateCAD(beam_Left, beam_Right, plate_Left, plate_Right, bbNutBoltArray,
        # #                             bbWeldAbvFlang, bbWeldBelwFlang, bbWeldSideWeb, bbWeldFlushstiffHeight,
        # #                             bbWeldFlushstiffLength,
        # #                             bbWeldStiffHeight, bbWeldStiffLength, beam_stiffeners, beam_stiffenerFlush, alist,
        # #                             outputobj)
        # #     extbothWays.create_3DModel()
        # #
        # #     return extbothWays
        # #
        # # else:  # Groove Weld
        #
        # # Grove Weld for connecting end plate to beam
        bbWeldFlang = GrooveWeld(b=float(beam_tw), h=float(beam_T),
                                 L=beam_B)  # outputobj["Weld"]["Size"]
        #
        # # Followings welds are welds placed aside of beam web, Qty = 4           # edited length value by Anand Swaroop
        # bbWeldSideWeb = FilletWeld(b=float(BBE.web_weld.size), h=float(BBE.web_weld.size),
        #                                                       L=beam_d - 2 * (beam_T + beam_R1) - (2 * 5))
        bbWeldWeb = GrooveWeld(b=float(beam_tw), h=float(beam_tw),
                               L=beam_d - 2 * beam_T)  # outputobj["Weld"]["Size"]



        extbothWays = CADGroove(BBE,beam_Left, beam_Right, plate_Left, plate_Right, bbNutBoltArray,bbWeldFlang,
                                    bbWeldWeb,beam_stiffeners,beam_stiffenerFlush,bbWeldStiffHeight,bbWeldStiffLength,bbWeldFlushstiffHeight,bbWeldFlushstiffLength)
        extbothWays.create_3DModel()

        return extbothWays

    def createBCEndPlateCAD(self):
        """
        Calls the CAD components like beam, plate, stiffeners, fillet and grove weld, nut and bolt. Also calls CAD file
        :return: creates CAD model
        """
        BCE = self.module_class

        column_tw = float(BCE.column_tw)
        column_T = float(BCE.column_tf)
        column_d = float(BCE.column_D)
        column_B = float(BCE.column_bf)
        column_R1 = float(BCE.column_r1)
        column_R2 = float(BCE.column_r2)
        column_alpha = 0.0
        self.column_length = float(BCE.ep_height_provided + 1000)
        # print(column_T,column_B,column_d,column_tw,column_R1,column_R2)

        beam_tw = float(BCE.beam_tw)
        beam_T = float(BCE.beam_tf)
        beam_d = float(BCE.beam_D)
        beam_B = float(BCE.beam_bf)
        beam_R1 = float(BCE.beam_r1)
        beam_R2 = float(BCE.beam_r2)
        beam_alpha = 0.0
        self.beam_length = BCE.stiffener_length +500

        beam_Left = ISection(B=column_B, T=column_T, D=column_d, t=column_tw,
                             R1=column_R1, R2=column_R2, alpha=column_alpha,
                             length=self.column_length, notchObj=None)

        beam_Right = ISection(B=beam_B, T=beam_T, D=beam_d, t=beam_tw,
                              R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                              length=self.beam_length, notchObj=None)  # Since both the beams are same

        # outputobj = self.outputs  # Save all the claculated/displayed out in outputobj

        plate_Right = Plate(W=BCE.ep_width_provided,
                            L=BCE.ep_height_provided,
                            T=BCE.plate_thickness)



        # TODO adding enpplate type and check if code is working
        # TODO added connectivity type here



        if  BCE.connectivity == "Column Web-Beam Web":
            conn_type = 'col_web_connectivity'
        else:  # "Column flange-Beam web"
            conn_type = 'col_flange_connectivity'

        print(conn_type,"hfhfh")

        # endplate_type = alist['Member']['EndPlate_type']
        if BCE.endplate_type == 'Extended One Way - Irreversible Moment':
            endplate_type = "one_way"
        elif BCE.endplate_type == 'Flushed - Reversible Moment':
            endplate_type = "flush"
        else:  # uiObj['Member']['EndPlate_type'] == "Extended both ways":
            endplate_type = "both_way"

        if BCE.continuity_plate_tension_flange_status == True or BCE.continuity_plate_tension_flange_status == True:

            if BCE.connectivity != "Column Web-Beam Web":
                contPlates = StiffenerPlate(W=(float(column_B) - float(column_tw)) / 2,
                                            L=float(column_d) - 2 * float(column_T),
                                            T=BCE.cont_plate_thk_provided, L21=BCE.notch_size, R22=BCE.notch_size,
                                            R21=BCE.notch_size, L22=BCE.notch_size)

                contWeldD = FilletWeld(b=BCE.weld_size_continuity_plate, h=BCE.weld_size_continuity_plate,
                                       L=float(column_d) - 2 * float(column_T)-2*BCE.notch_size)
                contWeldB = FilletWeld(b=BCE.weld_size_continuity_plate, h=BCE.weld_size_continuity_plate,
                                       L=float(column_B) / 2 - float(column_tw) / 2-BCE.notch_size)
            else:
                contPlates = StiffenerPlate(W=(float(column_B) - float(column_tw)) / 2,
                                            L=float(column_d) - 2 * float(column_T),
                                            T=BCE.cont_plate_thk_provided, L11=BCE.notch_size, R11=BCE.notch_size,
                                            R12=BCE.notch_size, L12=BCE.notch_size)
                contWeldD = FilletWeld(b=BCE.weld_size_continuity_plate, h=BCE.weld_size_continuity_plate,
                                       L=float(column_d) - 2 * float(column_T)-2*BCE.notch_size)
                contWeldB = FilletWeld(b=BCE.weld_size_continuity_plate, h=BCE.weld_size_continuity_plate,
                                       L=float(column_B) / 2 - float(column_tw) / 2-BCE.notch_size)
        else:
            contPlates = None
            contWeldD = None
            contWeldB = None

        if BCE.web_stiffener_status == True:


            webplate = StiffenerPlate(W=BCE.web_stiffener_width,
                                       L=BCE.web_stiffener_depth,
                                       T=BCE.web_stiffener_thk_provided)
            webWeldD = FilletWeld(b=BCE.weld_size_web_stiffener, h=BCE.weld_size_web_stiffener,
                                   L=BCE.web_stiffener_depth)
            webWeldB = FilletWeld(b=BCE.weld_size_web_stiffener, h=BCE.weld_size_web_stiffener,
                                   L=BCE.web_stiffener_width)
        else:
            webplate = None
            webWeldD = None
            webWeldB = None




        # if BCE.web_stiffener_status == True:
        #     diagplate = StiffenerPlate(W=(float(column_B) - float(column_tw)) / 2,
        #                                 L=BCE.diag_stiffener_length,
        #                                 T=BCE.diag_stiffener_thk_provided)
        #     diagWeldD = FilletWeld(b=BCE.weld_size_diag_stiffener, h=BCE.weld_size_diag_stiffener,
        #                            L=BCE.diag_stiffener_length)
        #     diagWeldB = FilletWeld(b=BCE.diag_stiffener_thk_provided, h=BCE.diag_stiffener_thk_provided,
        #                            L=float(column_B) / 2 - float(column_tw) / 2)
        # else:
        ########## diagplate is omitted due to detailing issues ###########
        diagplate = None
        diagWeldD = None
        diagWeldB = None
        ########## diagplate is omitted due to detailing issues ###########

        # contPlate_L2 = StiffenerPlate(W=(float(column_data["B"]) - float(column_data["tw"])) / 2,
        # 							  L=float(column_data["D"]) - 2 * float(column_data["T"]),
        # 							  T=outputobj['ContPlateTens']['Thickness'])
        # contPlate_R1 = copy.copy(contPlate_L1)
        # contPlate_R2 = copy.copy(contPlate_L2)



        beam_stiffeners = StiffenerPlate(W=BCE.stiffener_height, L=BCE.stiffener_length,
                                         T=BCE.stiffener_thickness,
                                         R11=BCE.stiffener_length- 25,
                                         R12=BCE.stiffener_height - 25,
                                         L21=5.0, L22=5.0)  # TODO: given hard inputs to L21 and L22

        beam_stiffenerFlush = StiffenerPlate(W=BCE.stiffener_height, L=BCE.stiffener_length,
                                             T=BCE.stiffener_thickness,
                                             L21=5.0, L22=5.0)

        bcWeldFlushstiffHeight = FilletWeld(b=BCE.weld_size_stiffener, h=BCE.weld_size_stiffener,
                                            L=BCE.stiffener_height - 5.0)

        bcWeldFlushstiffLength = FilletWeld(b=BCE.weld_size_stiffener, h=BCE.weld_size_stiffener,
                                            L=BCE.stiffener_length - 5.0)

        # beam_stiffener_2 = copy.copy(beam_stiffener_1)

        bolt_d = float(BCE.bolt.bolt_diameter_provided)  # Bolt diameter, entered by user
        bolt_r = bolt_d / 2
        bolt_T = self.boltHeadThick_Calculation(bolt_d)
        bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2
        bolt_Ht = self.boltLength_Calculation(bolt_d)

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component repo
        nut_T = self.nutThick_Calculation(bolt_d)
        nut_Ht = nut_T
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        numberOfBolts = int(BCE.bolt_numbers)


        # TODO remove all the clutter later

        # nutSpace = 2 * float(outputobj["Plate"]["Thickness"]) + nut_T   # Space between bolt head and nut
        if conn_type == 'col_flange_connectivity':
            nutSpace = float(column_T) + float(BCE.plate_thickness) + nut_T # / 2 + bolt_T / 2  # Space between bolt head and nut

        else:
            nutSpace = float(column_tw) + float(BCE.plate_thickness) + nut_T  # / 2 + bolt_T / 2  # Space between bolt head and nut
            print(nutSpace,column_tw,BCE.plate_thickness,nut_T,"121")
        bbNutBoltArray = BCE_NutBoltArray(BCE, nut, bolt, numberOfBolts, nutSpace, endplate_type)

        ###########################
        #       WELD SECTIONS     #
        ###########################
        '''
        Following sections are for creating Fillet Welds and Groove Welds
        Welds are numbered from Top to Bottom in Z-axis, Front to Back in Y axis and Left to Right in X axis. 
        '''
        ############################### Weld for the beam stiffeners ################################################

        # bcWeld for stiffener hight on left side
        print(BCE.notch_size,BCE.stiffener_thickness,BCE.stiffener_height,BCE.stiffener_length, BCE.cont_plate_thk_provided,BCE.weld_size_continuity_plate,BCE.weld_size_continuity_plate,"jjjj")
        bcWeldStiffHeight = FilletWeld(b=BCE.weld_size_stiffener, h=BCE.weld_size_stiffener,
                                       L=BCE.stiffener_height-5.0)

        #
        bcWeldStiffLength = FilletWeld(b=BCE.weld_size_stiffener, h=BCE.weld_size_stiffener,
                                       L=BCE.stiffener_length-5.0)



        bcWeldFlang = GrooveWeld(b=float(beam_tw), h=float(beam_T),
                                 L=beam_B)
        # #     # bcWeldFlang_2 = copy.copy(bcWeldFlang_1)
        # #
        # #     # Followings welds are welds placed aside of beam web, Qty = 4 			# edited length value by Anand Swaroop
        bcWeldWeb = GrooveWeld(b=float(beam_tw), h=float(beam_tw),
                               L=beam_d - 2 * beam_T)

        if conn_type == 'col_flange_connectivity':
        #
        #     if alist["Weld"]["Method"] == "Fillet Weld":
        #
        #         # # Followings welds are welds above beam flange, Qty = 4
        #         # bcWeldAbvFlang = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]),
        #         # 							   h=float(alist["Weld"]["Flange (mm)"]),
        #         # 							   L=beam_B)
        #         # # bcWeldAbvFlang_22 = copy.copy(bcWeldAbvFlang_21)
        #         #
        #         # # Followings welds are welds below beam flange, Qty = 8
        #         # bcWeldBelwFlang = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]),
        #         # 								h=float(alist["Weld"]["Flange (mm)"]), L=(beam_B - beam_tw) / 2)
        #         # # bcWeldBelwFlang_22 = copy.copy(bcWeldBelwFlang_21)
        #         # # bcWeldBelwFlang_23 = copy.copy(bcWeldBelwFlang_21)
        #         # # bcWeldBelwFlang_24 = copy.copy(bcWeldBelwFlang_21)
        #         #
        #         # # Followings welds are welds placed aside of beam web, Qty = 4 			# edited length value by Anand Swaroop
        #         # bcWeldSideWeb = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
        #         # 							  L=beam_d - 2 * beam_T - 40)
        #         # # bcWeldSideWeb_22 = copy.copy(bcWeldSideWeb_21)
        #
        #         extbothWays = CADFillet(beam_Left, beam_Right, plate_Right, bbNutBoltArray, bolt, bcWeldAbvFlang,
        #                                 bcWeldBelwFlang,
        #                                 bcWeldSideWeb, contWeldD, contWeldB,
        #                                 bcWeldStiffHeight, bcWeldStiffLength,
        #                                 contPlates, beam_stiffeners, endplate_type, conn_type,
        #                                 outputobj)
        #         extbothWays.create_3DModel()
        #
        #         return extbothWays
        #
        #     else:  # Groove Weld

            # extbothWays = CADGroove(beam_Left, beam_Right, plate_Right, bbNutBoltArray, bolt,
            #                         bcWeldFlang, bcWeldWeb,
            #                         bcWeldStiffHeight, bcWeldStiffLength, contWeldD, contWeldB,
            #                         contPlates, beam_stiffeners, endplate_type, outputobj)
            extbothWays = BCECADGroove(BCE,beam_Left, beam_Right, plate_Right, bbNutBoltArray, bolt,bcWeldFlang,
                                    bcWeldWeb, contPlates,beam_stiffeners,bcWeldStiffHeight,bcWeldStiffLength,contWeldD,contWeldB,diagplate, diagWeldD, diagWeldB, webplate, webWeldB, webWeldD, beam_stiffenerFlush,bcWeldFlushstiffHeight, bcWeldFlushstiffLength,endplate_type)


            extbothWays.create_3DModel()

            return extbothWays

        else:  # conn_type = 'col_web_connectivity'
            bcWeldFlang = GrooveWeld(b=float(beam_tw), h=float(beam_T),
                                     L=beam_B)
            # #     # bcWeldFlang_2 = copy.copy(bcWeldFlang_1)
            # #
            # #     # Followings welds are welds placed aside of beam web, Qty = 4 			# edited length value by Anand Swaroop
            bcWeldWeb = GrooveWeld(b=float(beam_tw), h=float(beam_tw),
                                   L=beam_d - 2 * beam_T)

            ########## diagplate is omitted due to detailing issues ###########
            diagplate = None
            diagWeldD = None
            diagWeldB = None
            ########## diagplate is omitted due to detailing issues ###########

            webplate = None
            webWeldD = None
            webWeldB = None
            # if alist["Weld"]["Method"] == "Fillet Weld":
            #     # # Followings welds are welds above beam flange, Qty = 4
            #     # bcWeldAbvFlang_21 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]),
            #     # 							   h=float(alist["Weld"]["Flange (mm)"]),
            #     # 							   L=beam_B)
            #     # bcWeldAbvFlang_22 = copy.copy(bcWeldAbvFlang_21)
            #     #
            #     # # Followings welds are welds below beam flange, Qty = 8
            #     # bcWeldBelwFlang_21 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]),
            #     # 								h=float(alist["Weld"]["Flange (mm)"]), L=(beam_B - beam_tw) / 2)
            #     # bcWeldBelwFlang_22 = copy.copy(bcWeldBelwFlang_21)
            #     # bcWeldBelwFlang_23 = copy.copy(bcWeldBelwFlang_21)
            #     # bcWeldBelwFlang_24 = copy.copy(bcWeldBelwFlang_21)
            #     #
            #     # # Followings welds are welds placed aside of beam web, Qty = 4 			# edited length value by Anand Swaroop
            #     # bcWeldSideWeb_21 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
            #     # 							  L=beam_d - 2 * beam_T - 40)
            #     # bcWeldSideWeb_22 = copy.copy(bcWeldSideWeb_21)

            #     col_web_connectivity = CADColWebFillet(beam_Left, beam_Right, plate_Right, bbNutBoltArray, bolt,
            #                                            bcWeldAbvFlang,
            #                                            bcWeldBelwFlang,
            #                                            bcWeldSideWeb,
            #                                            contWeldD, contWeldB,
            #                                            bcWeldStiffHeight, bcWeldStiffLength,
            #                                            contPlates, beam_stiffeners, endplate_type,
            #                                            conn_type, outputobj)
            #
            #     col_web_connectivity.create_3DModel()
            #
            #     return col_web_connectivity
            #
            # else:  # Groove Weld

                # else:

                #######################################
                #       WELD SECTIONS QUARTER CONE    #
                #######################################

            # col_web_connectivity = CADcolwebGroove(beam_Left, beam_Right, plate_Right, bbNutBoltArray, bolt,
            #                                        bcWeldFlang, bcWeldWeb,
            #                                        bcWeldStiffHeight, bcWeldStiffLength,
            #                                        contWeldD, contWeldB,
            #                                        contPlates, beam_stiffeners, endplate_type,
            #                                        outputobj)

            col_web_connectivity = CADcolwebGroove(BCE, beam_Left, beam_Right, plate_Right, bbNutBoltArray, bolt,
                                                   bcWeldFlang,bcWeldWeb,contPlates,beam_stiffeners,bcWeldStiffHeight,bcWeldStiffLength,contWeldD,contWeldB,  diagplate, diagWeldD, diagWeldB, webplate, webWeldB, webWeldD, beam_stiffenerFlush,bcWeldFlushstiffHeight, bcWeldFlushstiffLength,endplate_type)


            col_web_connectivity.create_3DModel()

            return col_web_connectivity



    def createCCCoverPlateCAD(self):

        if self.connection == KEY_DISP_COLUMNCOVERPLATE:
            C = self.module_class()
            columnLenght = (max(float(C.flange_plate.length), float(C.web_plate.length)) + 600) / 2
            # column = ISection(B=206.4, T=17.3, D=215.8, t=10, R1=15, R2=75, alpha=94, length=1000, notchObj=None)
            # flangePlate = Plate(L=240, W=203.6, T=10)
            # innerFlangePlate = Plate(L=240, W=85, T=10)
            # webPlate = Plate(L=600, W=120, T=8)
            # gap = 10
            column = ISection(B=float(C.section.flange_width), T=float(C.section.flange_thickness),
                              D=float(C.section.depth), t=float(C.section.web_thickness),
                              R1=float(C.section.root_radius),
                              R2=float(C.section.toe_radius), alpha=float(C.section.flange_slope), length=columnLenght,
                              notchObj=None)
            flangePlate = Plate(L=float(C.flange_plate.length), W=float(C.flange_plate.height),
                                T=float(C.flange_plate.thickness_provided))
            innerFlangePlate = Plate(L=float(C.flange_plate.Innerlength), W=float(C.flange_plate.Innerheight),
                                     T=float(C.flange_plate.thickness_provided))
            webPlate = Plate(L=float(C.web_plate.length), W=float(C.web_plate.height),
                             T=float(C.web_plate.thickness_provided))

            bolt_d = float(C.bolt.bolt_diameter_provided)  # Bolt diameter (shank part), entered by user
            bolt_r = bolt_d / 2  # Bolt radius (Shank part)
            bolt_T = self.boltHeadThick_Calculation(bolt_d)  # Bolt head thickness
            bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
            bolt_Ht = self.boltLength_Calculation(bolt_d)  # Bolt head height

            bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component directory
            nut_T = self.nutThick_Calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
            nut_Ht = nut_T
            nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)
            if C.preference != 'Outside':
                nut_space = 2 * flangePlate.T + column.T
                nut_spaceW = 2 * webPlate.T + column.t
            else:
                nut_space = flangePlate.T + column.T
                nut_spaceW = 2*webPlate.T + column.t

            numOfboltsF = C.flange_plate.bolts_required
            numOfboltsW = C.web_plate.bolts_required

            nut_bolt_array_AF = CCSpliceNutBolt_AF(C, nut, bolt, numOfboltsF, nut_space)
            nut_bolt_array_BF = CCSpliceNutBolt_BF(C, nut, bolt, numOfboltsF, nut_space)
            nut_bolt_array_Web = CCSpliceNutBolt_Web(C, nut, bolt, numOfboltsW, nut_spaceW)

            ccCoverPlateCAD = CCSpliceCoverPlateBoltedCAD(C, column, flangePlate, innerFlangePlate, webPlate,
                                                                nut_bolt_array_AF, nut_bolt_array_BF,
                                                                nut_bolt_array_Web)

            ccCoverPlateCAD.create_3DModel()


        elif self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:

            C = self.module_class()
            columnLenght = (max(float(C.flange_plate.length), float(C.web_plate.length)) + 600) / 2
            column = ISection(B=float(C.section.flange_width), T=float(C.section.flange_thickness),
                              D=float(C.section.depth), t=float(C.section.web_thickness),
                              R1=float(C.section.root_radius),
                              R2=float(C.section.toe_radius), alpha=float(C.section.flange_slope), length=columnLenght,
                              notchObj=None)
            flangePlate = Plate(L=float(C.flange_plate.length), W=float(C.flange_plate.height),
                                T=float(C.flange_plate.thickness_provided))
            innerFlangePlate = Plate(L=float(C.flange_plate.Innerlength), W=float(C.flange_plate.Innerheight),
                                     T=float(C.flange_plate.thickness_provided))
            webPlate = Plate(L=float(C.web_plate.length), W=float(C.web_plate.height),
                             T=float(C.web_plate.thickness_provided))

            flangePlateWeldL = FilletWeld(h=float(C.flange_weld.size), b=float(C.flange_weld.size), L=flangePlate.L)
            flangePlateWeldW = FilletWeld(h=float(C.flange_weld.size), b=float(C.flange_weld.size), L=flangePlate.W)

            innerflangePlateWeldL = FilletWeld(h=float(C.flange_weld.size), b=float(C.flange_weld.size),
                                               L=innerFlangePlate.L)
            innerflangePlateWeldW = FilletWeld(h=float(C.flange_weld.size), b=float(C.flange_weld.size),
                                               L=innerFlangePlate.W)

            webPlateWeldL = FilletWeld(h=float(C.web_weld.size), b=float(C.web_weld.size), L=webPlate.L)
            webPlateWeldW = FilletWeld(h=float(C.web_weld.size), b=float(C.web_weld.size), L=webPlate.W)

            ccCoverPlateCAD = CCSpliceCoverPlateWeldedCAD(C, column, flangePlate, innerFlangePlate, webPlate,
                                                          flangePlateWeldL, flangePlateWeldW,
                                                          innerflangePlateWeldL,
                                                          innerflangePlateWeldW, webPlateWeldL, webPlateWeldW)

            ccCoverPlateCAD.create_3DModel()

        return ccCoverPlateCAD

    def createCCEndPlateCAD(self):
        CEP = self.module_class

        bolt_d = float(CEP.bolt_diam_provided)  # Bolt diameter (shank part), entered by user
        bolt_r = bolt_d / 2  # Bolt radius (Shank part)
        bolt_T = self.boltHeadThick_Calculation(bolt_d)  # Bolt head thickness
        bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
        bolt_Ht = self.boltLength_Calculation(bolt_d)  # Bolt head height

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component directory
        nut_T = self.nutThick_Calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
        nut_Ht = nut_T
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)
        if CEP.weld_size <= 16:
            stiffener = StiffenerPlate(L=CEP.stiff_wt, W=CEP.stiff_ht, T=CEP.t_s, L11=CEP.stiff_wt / 2,
                                       L12=CEP.stiff_ht / 2, R21=10, R22=10)
            weld_stiff_h = GrooveWeld(b=stiffener.T, h= stiffener.T, L=stiffener.L - stiffener.R22)
            weld_stiff_v = FilletWeld(b= CEP.weld_size, h= CEP.weld_size, L=stiffener.W - stiffener.R21)
        else:
            stiffener = StiffenerPlate(L=CEP.stiff_wt  - CEP.t_s, W=CEP.stiff_ht, T=CEP.t_s, L11=CEP.stiff_wt / 2,
                                       L12=CEP.stiff_ht / 2, R21=10, R22=10)
            weld_stiff_h = GrooveWeld(b=stiffener.T, h= stiffener.T, L=stiffener.L - stiffener.R22)
            weld_stiff_v = GrooveWeld(b=stiffener.T, h= stiffener.T, L=stiffener.W - stiffener.R21)

        column = ISection(B=float(CEP.section.flange_width), T=float(CEP.section.flange_thickness),
                          D=float(CEP.section.depth), t=float(CEP.section.web_thickness),
                          R1=float(CEP.section.root_radius), R2=float(CEP.section.toe_radius),
                          alpha=float(CEP.section.flange_slope), length=1000, notchObj=None)
        endPlate = Plate(L=float(CEP.plate_height), W=float(CEP.plate_width), T=float(CEP.plate_thickness_provided))
        flangeWeld = GrooveWeld(b=column.T, h=float(10.0), L=column.B)
        webWeld = GrooveWeld(b=column.t, h=flangeWeld.h, L=column.D - 2 * column.T)

        # bolt = Bolt(R=14, T=10, H=13, r=8)
        # nut = Nut(R=bolt.R, T=bolt.T, H=bolt.T + 1, innerR1=bolt.r)
        nut_space = 2 * endPlate.T + nut.T  # member.T + plate.T + nut.T

        nut_bolt_array = CEPNutBoltArray(CEP, column, nut, bolt, nut_space)

        ccEndPlateCad = CCEndPlateCAD(CEP, column, endPlate, flangeWeld, webWeld, nut_bolt_array, stiffener, weld_stiff_h, weld_stiff_v)

        ccEndPlateCad.create_3DModel()

        return ccEndPlateCad

    def createBasePlateCAD(self):
        """
        :return: The calculated values/parameters to create 3D CAD model of individual components.
        """

        BP = self.module_class

        if BP.connectivity == 'Hollow/Tubular Column Base':
            if BP.dp_column_designation[1:4] == 'SHS' or BP.dp_column_designation[1:4] == 'RHS':
                sec = RectHollow(L=float(BP.column_bf), W=float(BP.column_D), H=1000, T=float(BP.column_tf))

                BP.weld_size_stiffener = max(sec.T, BP.stiffener_plt_thk)/2
                weld_sec = RectHollow(L=sec.L, W=sec.W, H=float(BP.weld_size_stiffener), T=sec.T)
                stiff_alg_l = StiffenerPlate(L=BP.stiffener_plt_len_along_D - BP.weld_size_stiffener, W=BP.stiffener_plt_height, T= BP.stiffener_plt_thk,
                                             L11= BP.stiffener_plt_len_along_D - BP.weld_size_stiffener - 50, L12=BP.stiffener_plt_height - 100, R21=15, R22=15)
                stiff_alg_b = StiffenerPlate(L= BP.stiffener_plt_len_along_B - BP.weld_size_stiffener, W=BP.stiffener_plt_height, T=BP.stiffener_plt_thk,
                                             L11= BP.stiffener_plt_len_along_B - BP.weld_size_stiffener - 50, L12=BP.stiffener_plt_height - 100, R21=15, R22=15)

                weld_stiff_l_v = GrooveWeld(b=stiff_alg_l.T, h=BP.weld_size_stiffener, L=stiff_alg_l.W - stiff_alg_l.R22)
                weld_stiff_l_h = GrooveWeld(b=stiff_alg_l.T, h=BP.weld_size_stiffener, L=stiff_alg_l.L - stiff_alg_l.R22)
                weld_stiff_b_v = GrooveWeld(b=stiff_alg_b.T, h=BP.weld_size_stiffener, L=stiff_alg_b.W - stiff_alg_b.R22)
                weld_stiff_b_h = GrooveWeld(b=stiff_alg_b.T, h=BP.weld_size_stiffener, L=stiff_alg_b.L - stiff_alg_b.R22)


            else:       #self.BP.dp_column_designation[1:4] == 'CHS':
                sec = CircularHollow(r=float(BP.column_D)/ 2, T=float(BP.column_tf), H=1500)

                BP.weld_size_stiffener = max(sec.T, BP.stiffener_plt_thk)/2

                weld_sec = CircularHollow(r=sec.r, T=sec.T, H=float(BP.weld_size_stiffener))
                stiff_alg_l = StiffenerPlate(L=BP.stiffener_plt_len_across_D - BP.weld_size_stiffener, W=BP.stiffener_plt_height, T=BP.stiffener_plt_thk,
                                             L11=BP.stiffener_plt_len_across_D - BP.weld_size_stiffener - 50, L12=BP.stiffener_plt_height - 100, R21=15, R22=15)
                stiff_alg_b = StiffenerPlate(L=BP.stiffener_plt_len_across_D - BP.weld_size_stiffener, W=BP.stiffener_plt_height, T=BP.stiffener_plt_thk,
                                             L11=BP.stiffener_plt_len_across_D - BP.weld_size_stiffener - 50, L12=BP.stiffener_plt_height - 100, R21=15, R22=15)

                weld_stiff_l_v = GrooveWeld(b=stiff_alg_l.T, h=BP.weld_size_stiffener, L=stiff_alg_l.W - stiff_alg_l.R22)
                weld_stiff_l_h = GrooveWeld(b=stiff_alg_l.T, h=BP.weld_size_stiffener, L=stiff_alg_l.L - stiff_alg_l.R22)
                weld_stiff_b_v = GrooveWeld(b=stiff_alg_b.T, h=BP.weld_size_stiffener, L=stiff_alg_b.W - stiff_alg_b.R22)
                weld_stiff_b_h = GrooveWeld(b=stiff_alg_b.T, h=BP.weld_size_stiffener, L=stiff_alg_b.L - stiff_alg_b.R22)

            baseplate = Plate(L=float(BP.bp_length_provided), W=float(BP.bp_width_provided), T=float(BP.plate_thk))

            bolt_d = float(BP.anchor_dia_outside_flange)
            bolt_r = bolt_d / 2  # Bolt radius (Shank part)
            bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
            # bolt_T = self.boltHeadThick_Calculation(bolt_d)      # Bolt head thickness
            nut_T = self.nutThick_Calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
            nut_HT = nut_T

            ex_length_out = BP.anchor_len_above_footing_out
            if BP.anchor_type == 'IS 5624-Type A':
                bolt = AnchorBolt_A(l=float(BP.anchor_len_below_footing_out), c=125, a=75,
                                    r=float(BP.anchor_dia_outside_flange) / 2,
                                    ex=ex_length_out)
            elif BP.anchor_type == 'IS 5624-Type B':
                bolt = AnchorBolt_B(l=float(BP.anchor_len_below_footing_out), r=float(BP.anchor_dia_outside_flange) / 2,
                                    ex=ex_length_out)
            else:  # BP.anchor_type == 'End Plate Type':
                bolt = AnchorBolt_Endplate(l=float(BP.anchor_len_below_footing_out), r=float(BP.anchor_dia_outside_flange) / 2,  a= BP.plate_washer_dim_out*1.5,
                                           ex=ex_length_out)

            bolt_in = bolt

            nut = Nut(R=bolt_R, T=nut_T, H=nut_HT, innerR1=bolt_r)
            nut_in = nut
            washer = Washer(a=BP.plate_washer_dim_out , d=BP.plate_washer_inner_dia_out , t=BP.plate_washer_thk_out)
            washer_in = washer
            nutSpace = bolt.c + baseplate.T
            bolthight = washer.T + nut.T + 50

            concrete = Plate(L=baseplate.L * 1.5, W=baseplate.W * 1.5, T=bolt.l * 1.2)
            grout = Grout(L=baseplate.L * 1.5, W=baseplate.W * 1.5, T=50)

            if BP.shear_key_along_ColDepth == 'Yes':
                shearkey_1 = Plate(L=float(BP.shear_key_len_ColDepth), W=float(BP.shear_key_thk), T=float(BP.shear_key_depth_ColDepth))
            else:
                shearkey_1 = Plate(L=float(0), W=float(0), T=float(0))

            if BP.shear_key_along_ColWidth == 'Yes':
                shearkey_2 = Plate(L=float(BP.shear_key_thk), W=float(BP.shear_key_len_ColWidth), T=float(BP.shear_key_depth_ColWidth))
            else:
                shearkey_2 = Plate(L=float(0), W=float(0), T=float(0))

            nut_bolt_array = bpNutBoltArray(BP, nut, nut_in, bolt, bolt_in, nutSpace,  washer, washer_in)

            basePlate = HollowBasePlateCad(BP, sec, weld_sec, nut_bolt_array, bolthight, baseplate, concrete, grout,
                                           stiff_alg_l, stiff_alg_b, weld_stiff_l_v, weld_stiff_l_h, weld_stiff_b_v,
                                           weld_stiff_b_h, shearkey_1, shearkey_2)
        else:
            column_tw = float(BP.column_tw)
            column_T = float(BP.column_tf)
            column_d = float(BP.column_D)
            column_B = float(BP.column_bf)
            column_R1 = float(BP.column_r1)
            column_R2 = float(BP.column_r2)
            column_alpha = 94  # Todo: connect this. Waiting for danish to give variable
            column_length = 1500

            column = ISection(B=column_B, T=column_T, D=column_d, t=column_tw, R1=column_R1, R2=column_R2,
                              alpha=column_alpha, length=column_length, notchObj=None)
            baseplate = Plate(L=float(BP.bp_length_provided), W=float(BP.bp_width_provided), T=float(BP.plate_thk))

            if BP.weld_type == 'Fillet Weld':
                weldAbvFlang = FilletWeld(b=float(BP.weld_size_flange), h=float(BP.weld_size_flange), L=column.B)
                weldBelwFlang = FilletWeld(b=float(BP.weld_size_flange), h=float(BP.weld_size_flange),
                                           L=(column.B - column.t - 2 * (column.R1 + column.R2)) / 2)
                weldSideWeb = FilletWeld(b=float(BP.weld_size_web), h=float(BP.weld_size_web),
                                         L=column.D - 2 * (column.t + column.R1))
            else:
                BP.weld_size_flange = max(column.T/2, column.t/2)
                BP.weld_size_web = BP.weld_size_flange
                weldAbvFlang = GrooveWeld(b= column.T, h=float(BP.weld_size_flange), L=column.B)
                weldBelwFlang = GrooveWeld(b= column.T, h=float(BP.weld_size_flange), L=column.B)
                weldSideWeb = GrooveWeld(b=column.t, h=float(BP.weld_size_web), L=column.D)


            BP.weld_size_stiffener = max(BP.stiffener_plt_thick_along_web, BP.stiffener_plt_thick_across_web, column.T) / 2
            stiffener = StiffenerPlate(L=float(BP.stiffener_plt_len_along_web) - float(BP.weld_size_stiffener), W=float(BP.stiffener_plt_height_along_web),
                                       T=float(BP.stiffener_plt_thick_along_web),
                                       L11=float(BP.stiffener_plt_len_along_web - 50), L12=float(BP.stiffener_plt_height_along_web - 100), R21=15, R22=15)

            concrete = Plate(L=baseplate.L * 2, W=baseplate.W * 2, T=float(BP.anchor_len_below_footing_out) * 1.5)
            grout = Grout(L=concrete.L, W=concrete.W, T=50)

            stiffener_acrsWeb = StiffenerPlate(L=float(BP.stiffener_plt_len_across_web) - float(BP.weld_size_stiffener), W=float(BP.stiffener_plt_height_across_web), T=float(BP.stiffener_plt_thick_across_web),
                                               L11=float(BP.stiffener_plt_len_across_web) - 50, L12=float(BP.stiffener_plt_height_across_web) - 100,
                                               R21=15, R22=15)  # todo: add L21 and L22 as max(15, weldsize + 3)

            stiffener_algflangeL = Stiffener_flange(H=float(BP.stiffener_plt_height_along_flange), L=BP.stiffener_plt_len_along_flange - float(BP.weld_size_stiffener), T=BP.stiffener_plt_thick_along_flange,
                                                    t_f=column.T, L_h=50, L_v=100, to_left=True)
            stiffener_algflangeR = Stiffener_flange(H=float(BP.stiffener_plt_height_along_flange), L=BP.stiffener_plt_len_along_flange - float(BP.weld_size_stiffener), T= BP.stiffener_plt_thick_along_flange,
                                                    t_f=column.T, L_h=50, L_v=100, to_left=False)
            stiffener_algflange_tapperLength = (stiffener_algflangeR.T - column.T) * 5

            stiffener_insideflange = StiffenerPlate(L= (column.D - 2*column.T - 2 * float(BP.weld_size_stiffener)), W= (column.B- column.t - 2*column.R1 - 2 * 5)/2, T =12,  R21 = column.R1 + 5, R22= column.R1 + 5, L21 = column.R1 + 5, L22= column.R1 + 5)  # self.extraspace=5


            weld_stiffener_algflng_v = GrooveWeld(b=column.T, h=float(BP.weld_size_stiffener), L=stiffener_algflangeL.H)
            weld_stiffener_algflng_h = FilletWeld(b=float(BP.weld_size_stiffener), h=float(BP.weld_size_stiffener),
                                                  L=stiffener_algflangeL.L)  # Todo: create another weld for inner side of the stiffener
            weld_stiffener_algflag_gh = GrooveWeld(b=stiffener_algflangeR.T, h=float(BP.weld_size_stiffener),
                                                   L=stiffener_algflangeL.L - stiffener_algflange_tapperLength)

            weld_stiffener_acrsWeb_v = GrooveWeld(b=stiffener_acrsWeb.T, h=float(BP.weld_size_stiffener),
                                                  L=stiffener_acrsWeb.W - stiffener_acrsWeb.R22)
            weld_stiffener_acrsWeb_h = FilletWeld(b=10, h=10, L=stiffener_acrsWeb.L - stiffener_acrsWeb.R22)
            weld_stiffener_acrsWeb_gh = GrooveWeld(b=stiffener_acrsWeb.T, h=float(BP.weld_size_stiffener),
                                                   L=stiffener_acrsWeb.L - stiffener_acrsWeb.R22)

            # gussetweld = GrooveWeld(b=gusset.T, h=float(BP.weld_size_stiffener), L=gusset.L)
            weld_stiffener_alongWeb_h = FilletWeld(b=float(BP.weld_size_stiffener), h=float(BP.weld_size_stiffener), L=stiffener.L - stiffener.R22)
            weld_stiffener_alongWeb_v = GrooveWeld(b=stiffener.T, h=float(BP.weld_size_stiffener), L=stiffener.W - stiffener.R22)
            weld_stiffener_alongWeb_gh = GrooveWeld(b=stiffener.T, h=float(BP.weld_size_stiffener), L=stiffener.L - stiffener.R22)

            weld_stiffener_inflange = GrooveWeld(b=stiffener_insideflange.T, h=float(BP.weld_size_stiffener), L=stiffener_insideflange.W - stiffener_insideflange.R22)
            weld_stiffener_inflange_d = GrooveWeld(b=stiffener_insideflange.T, h=float(BP.weld_size_stiffener),
                                                   L=stiffener_insideflange.L - stiffener_insideflange.R22 - 2 * weld_stiffener_inflange.h)

            if BP.load_axial_tension > 0:
                BP.anchor_len_above_footing_in = BP.anchor_len_above_footing_in
                BP.anchor_len_below_footing_in = BP.anchor_len_below_footing_in
                BP.anchor_dia_inside_flange = BP.anchor_dia_inside_flange
                BP.plate_washer_dim_in = BP.plate_washer_dim_in
                BP.plate_washer_inner_dia_in = BP.plate_washer_inner_dia_in
                BP.plate_washer_thk_in = BP.plate_washer_thk_in
            else:
                BP.anchor_len_above_footing_in = BP.anchor_len_above_footing_out
                BP.anchor_len_below_footing_in = BP.anchor_len_below_footing_out
                BP.anchor_dia_inside_flange = BP.anchor_dia_outside_flange
                BP.plate_washer_dim_in = BP.plate_washer_dim_out
                BP.plate_washer_inner_dia_in = BP.plate_washer_inner_dia_out
                BP.plate_washer_thk_in = BP.plate_washer_thk_out

            bolt_d = float(BP.anchor_dia_outside_flange)
            bolt_r = bolt_d / 2  # Bolt radius (Shank part)
            bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
            # bolt_T = self.boltHeadThick_Calculation(bolt_d)      # Bolt head thickness
            nut_T = self.nutThick_Calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
            nut_HT = nut_T

            bolt_d_in = float(BP.anchor_dia_inside_flange)
            bolt_r_in = bolt_d_in / 2  # Bolt radius (Shank part)
            bolt_R_in = self.boltHeadDia_Calculation(bolt_d_in) / 2  # Bolt head diameter (Hexagon)
            # bolt_T = self.boltHeadThick_Calculation(bolt_d)      # Bolt head thickness
            nut_T_in = self.nutThick_Calculation(bolt_d_in)  # Nut thickness, usually nut thickness = nut height
            nut_HT_in = nut_T_in

            ex_length_out = BP.anchor_len_above_footing_out
            ex_length_in = BP.anchor_len_above_footing_in
            if BP.anchor_type == 'IS 5624-Type A':
                bolt = AnchorBolt_A(l=float(BP.anchor_len_below_footing_out), c=125, a=75, r=float(BP.anchor_dia_outside_flange) / 2,
                                    ex=ex_length_out)
                bolt_in = AnchorBolt_A(l=float(BP.anchor_len_below_footing_in), c=125, a=75, r=float(BP.anchor_dia_inside_flange) / 2,
                                    ex=ex_length_in)
            elif BP.anchor_type == 'IS 5624-Type B':
                bolt = AnchorBolt_B(l=float(BP.anchor_len_below_footing_out), r=float(BP.anchor_dia_outside_flange) / 2, ex=ex_length_out)
                bolt_in = AnchorBolt_B(l=float(BP.anchor_len_below_footing_in), r=float(BP.anchor_dia_inside_flange) / 2,
                                    ex=ex_length_in)
            else: #BP.anchor_type == 'End Plate Type':
                bolt = AnchorBolt_Endplate(l=float(BP.anchor_len_below_footing_out), r=float(BP.anchor_dia_outside_flange) / 2,  a= BP.plate_washer_dim_out * 1.5,
                                           ex=ex_length_out)
                bolt_in = AnchorBolt_Endplate(l=float(BP.anchor_len_below_footing_in),
                                           r=float(BP.anchor_dia_inside_flange) / 2, a= BP.plate_washer_inner_dia_in * 1.5,
                                           ex=ex_length_in)

            nut = Nut(R=bolt_R, T=nut_T, H=nut_HT, innerR1=bolt_r)
            nut_in = Nut(R=bolt_R_in, T=nut_T_in, H=nut_HT_in, innerR1=bolt_r_in)
            washer = Washer(a=BP.plate_washer_dim_out , d=BP.plate_washer_inner_dia_out , t=BP.plate_washer_thk_out)
            washer_in = Washer(a=BP.plate_washer_dim_in, d=BP.plate_washer_inner_dia_in, t=BP.plate_washer_thk_out)
            nutSpace = bolt.c + baseplate.T
            bolthight = washer.T + nut.T + 50

            if BP.shear_key_along_ColDepth == 'Yes':
                shearkey_1 = Plate(L=float(BP.shear_key_len_ColDepth), W=float(BP.shear_key_thk), T=float(BP.shear_key_depth_ColDepth))
            else:
                shearkey_1 = Plate(L=float(0), W=float(0), T=float(0))

            if BP.shear_key_along_ColWidth == 'Yes':
                shearkey_2 = Plate(L=float(BP.shear_key_thk), W=float(BP.shear_key_len_ColWidth), T=float(BP.shear_key_depth_ColWidth))
            else:
                shearkey_2 = Plate(L=float(0), W=float(0), T=float(0))

            nut_bolt_array = bpNutBoltArray(BP, nut, nut_in, bolt, bolt_in, nutSpace, washer, washer_in)

            basePlate = BasePlateCad(BP, column, nut_bolt_array, bolthight, baseplate, shearkey_1, shearkey_2, weldAbvFlang, weldBelwFlang, weldSideWeb,
                                     concrete, stiffener, grout, weld_stiffener_alongWeb_h, weld_stiffener_alongWeb_gh, weld_stiffener_alongWeb_v,
                                     stiffener_algflangeL, stiffener_algflangeR, stiffener_acrsWeb, weld_stiffener_algflng_v, weld_stiffener_algflng_h, weld_stiffener_algflag_gh,
                                     weld_stiffener_acrsWeb_v, weld_stiffener_acrsWeb_h, weld_stiffener_acrsWeb_gh, stiffener_insideflange, weld_stiffener_inflange, weld_stiffener_inflange_d)

        basePlate.create_3DModel()

        return basePlate

    def createTensionCAD(self):
        """
        :return: The calculated values/parameters to create 3D CAD model of individual components.
        """
        T = self.module_class

        # Types of connections =  #'Angles', 'Back to Back Angles', 'Star Angles', 'Channels', 'Back to Back Channels'
        if self.connection == KEY_DISP_TENSION_BOLTED:
            bolt_d = float(T.bolt.bolt_diameter_provided)  # Bolt diameter (shank part), entered by user
            bolt_r = bolt_d / 2  # Bolt radius (Shank part)
            bolt_T = self.boltHeadThick_Calculation(bolt_d)  # Bolt head thickness
            bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
            bolt_Ht = self.boltLength_Calculation(bolt_d)  # Bolt head height

            bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component directory
            nut_T = self.nutThick_Calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
            nut_Ht = nut_T
            nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)  # Call to create Nut from Component directory

            plate = GassetPlate(L=float(T.plate.length + 50), H=float(T.plate.height),
                                T=float(T.plate.thickness_provided), degree=30)
            intermittentPlates = Plate(L=float(T.inter_plate_height), W=float(T.inter_plate_length), T=float(plate.T))


            if T.sec_profile == 'Channels' or T.sec_profile == 'Back to Back Channels':
                member = Channel(B=float(T.section_size_1.flange_width), T=float(T.section_size_1.flange_thickness),
                                 D=float(T.section_size_1.depth), t=float(T.section_size_1.web_thickness),
                                 R1=float(T.section_size_1.root_radius), R2=float(T.section_size_1.toe_radius),
                                 L=float(T.length))
                if T.sec_profile == 'Channels':
                    nut_space = member.t + plate.T + nut.T  # member.T + plate.T + nut.T

                else:
                    nut_space = 2 * member.t + plate.T + nut.T  # 2*member.T + plate.T + nut.T

                intermittentConnection = IntermittentNutBoltPlateArray(T, nut, bolt, intermittentPlates, nut_space)
                nut_bolt_array = TNutBoltArray(T, nut, bolt, nut_space)
                tensionCAD = TensionChannelBoltCAD(T, member, plate, nut_bolt_array, intermittentConnection)

            else:
                member = Angle(L=float(T.length), A=float(T.section_size_1.max_leg), B=float(T.section_size_1.min_leg),
                               T=float(T.section_size_1.thickness), R1=float(T.section_size_1.root_radius),
                               R2=float(T.section_size_1.toe_radius))
                if T.sec_profile == 'Back to Back Angles':
                    nut_space = 2 * member.T + plate.T + nut.T
                else:
                    nut_space = member.T + plate.T + nut.T

                intermittentConnection = IntermittentNutBoltPlateArray(T, nut, bolt, intermittentPlates, nut_space)
                nut_bolt_array = TNutBoltArray(T, nut, bolt, nut_space)
                tensionCAD = TensionAngleBoltCAD(T, member, plate, nut_bolt_array, intermittentConnection)

        else:
            plate = GassetPlate(L=float(T.plate.length + 50), H=float(T.plate.height),
                                T=float(T.plate.thickness_provided), degree=30)

            intermittentPlates = Plate(L=float(T.inter_plate_height), W=float(T.inter_plate_length), T=plate.T)
            intermittentWelds = FilletWeld(h=float(T.inter_weld_size), b=float(T.inter_weld_size), L=intermittentPlates.W)
            weld_plate_array = IntermittentWelds(T, intermittentWelds, intermittentPlates)

            s = max(15, float(T.weld.size))
            plate_intercept = plate.L - s - 50
            if T.sec_profile == 'Channels' or T.sec_profile == 'Back to Back Channels':
                member = Channel(B=float(T.section_size_1.flange_width), T=float(T.section_size_1.flange_thickness),
                                 D=float(T.section_size_1.depth), t=float(T.section_size_1.web_thickness),
                                 R1=float(T.section_size_1.root_radius), R2=float(T.section_size_1.toe_radius),
                                 L=float(T.length))
                inline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(plate_intercept))
                opline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(member.D))


                tensionCAD = TensionChannelWeldCAD(T, member, plate, inline_weld, opline_weld, weld_plate_array)

            else:
                member = Angle(L=float(T.length), A=float(T.section_size_1.max_leg), B=float(T.section_size_1.min_leg),
                               T=float(T.section_size_1.thickness), R1=float(T.section_size_1.root_radius),
                               R2=float(T.section_size_1.toe_radius))
                inline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(plate_intercept))
                if T.loc == 'Long Leg':
                    opline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(member.A))
                else:  # 'Short Leg'
                    opline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(member.B))

                # weld_plate_array = IntermittentWelds(T, intermittentWelds, intermittentPlates)
                tensionCAD = TensionAngleWeldCAD(T, member, plate, inline_weld, opline_weld, weld_plate_array)

        tensionCAD.create_3DModel()

        return tensionCAD

    def display_3DModel(self, component, bgcolor):

        self.component = component

        self.display.EraseAll()

        self.display.View_Iso()

        self.display.FitAll()

        self.display.DisableAntiAliasing()

        if bgcolor == "gradient_bg":

            self.display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])
        else:
            self.display.set_bg_gradient_color([255, 255, 255], [255, 255, 255])

        if self.mainmodule  == "Shear Connection":

            A = self.module_class()

            self.loc = A.connectivity


            if self.loc == "Column Flange-Beam Web" and self.connection == "Fin Plate":
                # pass
                # print("hghghghg")
                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
            elif self.loc == "Column Flange-Beam Web" and self.connection == "Seated Angle":
                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
            elif self.loc == "Column Flange-Beam Web" and self.connection == "Seated Angle":
                self.display.View.SetProj(OCC.Core.V3d.V3d_XposYnegZpos)

            if self.component == "Column":
                osdag_display_shape(self.display, self.connectivityObj.get_columnModel(), update=True)
            elif self.component == "Beam":
                osdag_display_shape(self.display, self.connectivityObj.get_beamModel(), material=Graphic3d_NOT_2D_ALUMINUM,
                                    update=True)
            elif component == "cleatAngle":

                osdag_display_shape(self.display, self.connectivityObj.angleModel, color=Quantity_NOC_BLUE1, update=True)
                osdag_display_shape(self.display, self.connectivityObj.angleLeftModel, color=Quantity_NOC_BLUE1,
                                    update=True)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

            elif component == "SeatAngle":
                osdag_display_shape(self.display, self.connectivityObj.topclipangleModel, color=Quantity_NOC_BLUE1,
                                    update=True)
                osdag_display_shape(self.display, self.connectivityObj.angleModel, color=Quantity_NOC_BLUE1, update=True)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

            elif self.component == "Plate":
                osdag_display_shape(self.display, self.connectivityObj.weldModelLeft, color=Quantity_NOC_RED, update=True)
                osdag_display_shape(self.display, self.connectivityObj.weldModelRight, color=Quantity_NOC_RED, update=True)
                osdag_display_shape(self.display, self.connectivityObj.plateModel, color=Quantity_NOC_BLUE4, update=True)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

            elif self.component == "Model":

                osdag_display_shape(self.display, self.connectivityObj.columnModel, update=True)
                osdag_display_shape(self.display, self.connectivityObj.beamModel, material=Graphic3d_NOT_2D_ALUMINUM,
                                    update=True)
                if self.connection == KEY_DISP_FINPLATE or self.connection == KEY_DISP_ENDPLATE:
                    osdag_display_shape(self.display, self.connectivityObj.weldModelLeft, color=Quantity_NOC_RED, update=True)
                    osdag_display_shape(self.display, self.connectivityObj.weldModelRight, color=Quantity_NOC_RED, update=True)
                    osdag_display_shape(self.display, self.connectivityObj.plateModel, color=Quantity_NOC_BLUE1,
                                        update=True)

                elif self.connection == KEY_DISP_CLEATANGLE:
                    osdag_display_shape(self.display, self.connectivityObj.angleModel, color=Quantity_NOC_BLUE1,
                                        update=True)
                    osdag_display_shape(self.display, self.connectivityObj.angleLeftModel, color=Quantity_NOC_BLUE1,
                                        update=True)
                else:
                    osdag_display_shape(self.display, self.connectivityObj.topclipangleModel, color=Quantity_NOC_BLUE1,
                                        update=True)
                    osdag_display_shape(self.display, self.connectivityObj.angleModel, color=Quantity_NOC_BLUE1,
                                        update=True)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

        if self.mainmodule == "Moment Connection":
            if self.connection == KEY_DISP_BEAMCOVERPLATE:

                self.B = self.module_class()
                # else:
                #     pass
                #
                # self.loc = A.connectivity
                self.CPObj = self.createBBCoverPlateCAD()  # CPBoltedObj is an object which gets all the calculated values of CAD models
                if self.component == "Beam":
                    # Displays both beams
                    osdag_display_shape(self.display, self.CPObj.get_only_beams_Models(), update=True)

                elif self.component == "Connector":
                    osdag_display_shape(self.display, self.CPObj.get_flangewebplatesModel(), update=True,
                                        color=Quantity_NOC_BLUE1)
                    if self.B.preference != 'Outside':
                        osdag_display_shape(self.display, self.CPObj.get_innetplatesModels(), update=True,
                                            color=Quantity_NOC_BLUE1)

                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_arrayModels(), update=True,
                                        color=Quantity_NOC_YELLOW)

                elif self.component == "Model":
                    osdag_display_shape(self.display, self.CPObj.get_beamsModel(), update=True)
                    osdag_display_shape(self.display, self.CPObj.get_flangewebplatesModel(), update=True,
                                        color=Quantity_NOC_BLUE1)

                    # Todo: remove velove commented lines

                    if self.B.preference != 'Outside':
                        osdag_display_shape(self.display, self.CPObj.get_innetplatesModels(), update=True,
                                            color=Quantity_NOC_BLUE1)

                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_arrayModels(), update=True,
                                        color=Quantity_NOC_YELLOW)
            elif self.connection == KEY_DISP_BB_EP_SPLICE:
                self.B = self.module_class()

                self.ExtObj = self.createBBEndPlateCAD()

                if component == "Beam":
                    osdag_display_shape(self.display, self.ExtObj.get_beam_models(), update=True)

                elif component == "Connector":
                    osdag_display_shape(self.display, self.ExtObj.get_plate_connector_models(), update=True,
                                        color='Blue')
                    osdag_display_shape(self.display, self.ExtObj.get_welded_models(), update=True, color='Red')
                    osdag_display_shape(self.display, self.ExtObj.get_nut_bolt_array_models(), update=True,
                                        color=Quantity_NOC_SADDLEBROWN)

                elif component == "Model":

                    # osdag_display_shape(self.display, self.ExtObj.get_models(), update=True)
                    osdag_display_shape(self.display, self.ExtObj.get_beam_models(), update=True)
                    osdag_display_shape(self.display, self.ExtObj.get_plate_connector_models(), update=True,
                                        color='Blue')
                    osdag_display_shape(self.display, self.ExtObj.get_welded_models(), update=True, color='Red')
                    osdag_display_shape(self.display, self.ExtObj.get_nut_bolt_array_models(), update=True,
                                        color=Quantity_NOC_SADDLEBROWN)



            elif self.connection == KEY_DISP_BEAMCOVERPLATEWELD:
                self.B = self.module_class()
                self.CPObj = self.createBBCoverPlateCAD()
                beams = self.CPObj.get_beam_models()
                plates = self.CPObj.get_plate_models()
                welds = self.CPObj.get_welded_modules()

                if self.component == "Beam":
                    # Displays both beams
                    osdag_display_shape(self.display, beams, update=True)
                elif self.component == "Connector":
                    osdag_display_shape(self.display, plates, update=True, color=Quantity_NOC_BLUE1)
                    osdag_display_shape(self.display, welds, update=True, color=Quantity_NOC_RED)
                elif self.component == "Model":
                    osdag_display_shape(self.display, beams, update=True)
                    osdag_display_shape(self.display, plates, update=True, color=Quantity_NOC_BLUE1)
                    osdag_display_shape(self.display, welds, update=True, color=Quantity_NOC_RED)

            elif self.connection == KEY_DISP_COLUMNCOVERPLATE:
                self.C = self.module_class()
                self.CPObj = self.createCCCoverPlateCAD()
                columns = self.CPObj.get_column_models()
                plates = self.CPObj.get_plate_models()
                nutbolt = self.CPObj.get_nut_bolt_models()
                onlycolumn = self.CPObj.get_only_column_models()

                if self.component == "Column":
                    # Displays both beams
                    osdag_display_shape(self.display, onlycolumn, update=True)
                elif self.component == "Cover Plate":
                    osdag_display_shape(self.display, plates, update=True, color=Quantity_NOC_BLUE1)
                    osdag_display_shape(self.display, nutbolt, update=True, color=Quantity_NOC_YELLOW)
                elif self.component == "Model":
                    osdag_display_shape(self.display, columns, update=True)
                    osdag_display_shape(self.display, plates, update=True, color=Quantity_NOC_BLUE1)
                    osdag_display_shape(self.display, nutbolt, update=True, color=Quantity_NOC_YELLOW)


            elif self.connection == KEY_DISP_BCENDPLATE:
                self.Bc = self.module_class()
                self.ExtObj = self.createBCEndPlateCAD()

                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
                c_length = self.column_length
                # Point1 = gp_Pnt(0.0, 0.0, c_length)
                # DisplayMsg(self.display, Point1, self.Bc.supporting_section.designation)
                b_length = self.beam_length + self.Bc.supporting_section.depth/2+100
                # Point2 = gp_Pnt(0.0,-b_length, c_length/2)
                # DisplayMsg(self.display, Point2, self.Bc.supported_section.designation)
                # Displays the beams #TODO ANAND
                if component == "Column":
                    self.display.View_Iso()
                    osdag_display_shape(self.display, self.ExtObj.columnModel, update=True)
                    # Point1 = gp_Pnt(-self.Bc.supporting_section.flange_width/2, 0, c_length)
                    # DisplayMsg(self.display, Point1, self.Bc.supporting_section.designation)
                    # Point = gp_Pnt(0.0, 0.0, 10)
                    # DisplayMsg(self.display,Point, "Column")

                elif component == "Beam":
                    self.display.View_Iso()
                    osdag_display_shape(self.display, self.ExtObj.beamModel, update=True,
                                        material=Graphic3d_NOT_2D_ALUMINUM)
                    # Point2 = gp_Pnt(0.0, -b_length, c_length / 2)
                    # DisplayMsg(self.display, Point2, self.Bc.supported_section.designation)
                    # , color = 'Dark Gray'

                elif component == "Connector":
                    osdag_display_shape(self.display, self.ExtObj.get_plate_connector_models(), update=True,
                                        color='Blue')
                    osdag_display_shape(self.display, self.ExtObj.get_welded_models(), update=True, color='Red')
                    osdag_display_shape(self.display, self.ExtObj.get_nut_bolt_array_models(), update=True,
                                        color=Quantity_NOC_SADDLEBROWN)


                elif component == "Model":

                    osdag_display_shape(self.display, self.ExtObj.get_column_models(), update=True)
                    osdag_display_shape(self.display, self.ExtObj.get_beam_models(), update=True,
                                        material=Graphic3d_NOT_2D_ALUMINUM)
                    osdag_display_shape(self.display, self.ExtObj.get_plate_connector_models(), update=True,
                                        color='Blue')
                    osdag_display_shape(self.display, self.ExtObj.get_welded_models(), update=True, color='Red')
                    osdag_display_shape(self.display, self.ExtObj.get_nut_bolt_array_models(), update=True,
                                        color=Quantity_NOC_SADDLEBROWN)
                    # Point1 = gp_Pnt(self.Bc.supporting_section.flange_width/2, -self.Bc.supporting_section.depth/2, c_length*0.75)
                    # DisplayMsg(self.display, Point1, self.Bc.supporting_section.designation)
                    # Point2 = gp_Pnt(self.Bc.supporting_section.flange_width/2, -b_length, c_length / 2)
                    # DisplayMsg(self.display, Point2, self.Bc.supported_section.designation)
                    # Erase(DisplayMsg(self.display, Point2, self.Bc.supported_section.designation))


            elif self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:
                self.C = self.module_class()
                self.CPObj = self.createCCCoverPlateCAD()
                columns = self.CPObj.get_column_models()
                plates = self.CPObj.get_plate_models()
                welds = self.CPObj.get_welded_modules()

                if self.component == "Column":
                    # Displays both beams
                    osdag_display_shape(self.display, columns, update=True)
                elif self.component == "Cover Plate":
                    osdag_display_shape(self.display, plates, update=True, color=Quantity_NOC_BLUE1)
                    osdag_display_shape(self.display, welds, update=True, color=Quantity_NOC_RED)
                elif self.component == "Model":
                    osdag_display_shape(self.display, columns, update=True)
                    osdag_display_shape(self.display, plates, update=True, color=Quantity_NOC_BLUE1)
                    osdag_display_shape(self.display, welds, update=True, color=Quantity_NOC_RED)

            elif self.connection == KEY_DISP_COLUMNENDPLATE:
                self.CEP = self.module_class()
                self.CEPObj = self.createCCEndPlateCAD()
                columns = self.CEPObj.get_column_models()
                plates = self.CEPObj.get_plate_models()
                welds = self.CEPObj.get_weld_models()
                nutBolts = self.CEPObj.get_nut_bolt_models()

                if self.component == "Column":
                    osdag_display_shape(self.display, columns, update=True)

                elif self.component == "Connector":
                    osdag_display_shape(self.display, plates, update=True, color=Quantity_NOC_BLUE1)
                    osdag_display_shape(self.display, welds, update=True, color=Quantity_NOC_RED)
                    osdag_display_shape(self.display, nutBolts, update=True, color=Quantity_NOC_YELLOW)

                elif self.component == "Model":
                    osdag_display_shape(self.display, columns, update=True)
                    osdag_display_shape(self.display, plates, update=True, color=Quantity_NOC_BLUE1)
                    osdag_display_shape(self.display, welds, update=True, color=Quantity_NOC_RED)
                    osdag_display_shape(self.display, nutBolts, update=True, color=Quantity_NOC_YELLOW)

            elif self.connection == KEY_DISP_BASE_PLATE:
                self.Bp = self.module_class

                self.BPObj = self.createBasePlateCAD()

                column = self.BPObj.get_column_model()
                plate = self.BPObj.get_plate_connector_models()
                weld = self.BPObj.get_welded_models()
                nut_bolt = self.BPObj.get_nut_bolt_array_models()
                conc = self.BPObj.get_concrete_models()
                grout = self.BPObj.get_grout_models()

                if self.component == "Model":  # Todo: change this into key
                    osdag_display_shape(self.display, column, update=True)
                    osdag_display_shape(self.display, plate, color=Quantity_NOC_BLUE1, update=True)
                    osdag_display_shape(self.display, weld, color=Quantity_NOC_RED, update=True)
                    osdag_display_shape(self.display, nut_bolt, color=Quantity_NOC_YELLOW, update=True)
                    osdag_display_shape(self.display, conc, color=GRAY, transparency=0.5, update=True)
                    osdag_display_shape(self.display, grout, color=GRAY, transparency=0.5, update=True)

                elif self.component == "Column":
                    osdag_display_shape(self.display, column, update=True)

                elif self.component == "Connector":
                    osdag_display_shape(self.display, plate, color=Quantity_NOC_BLUE1, update=True)
                    osdag_display_shape(self.display, weld, color=Quantity_NOC_RED, update=True)
                    osdag_display_shape(self.display, nut_bolt, color=Quantity_NOC_YELLOW, update=True)

        else:
            if self.connection == KEY_DISP_TENSION_BOLTED:
                self.T = self.module_class()
                self.TObj = self.createTensionCAD()

                member = self.TObj.get_members_models()
                plate = self.TObj.get_plates_models()

                nutbolt = self.TObj.get_nut_bolt_array_models()

                onlymember = self.TObj.get_only_members_models()
                # distance = self.T.length/2 - (2* self.T.plate.end_dist_provided + (self.T.plate.bolt_line - 1 ) * self.T.plate.pitch_provided)
                # Point = gp_Pnt(distance, 0.0, 300)
                # DisplayMsg(self.display, Point, self.T.section_size_1.designation)


                if self.component == "Member":  # Todo: change this into key
                    osdag_display_shape(self.display, onlymember, update=True)
                elif self.component == "Plate":
                    osdag_display_shape(self.display, plate, color=Quantity_NOC_BLUE1, update=True)
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_YELLOW, update=True)
                elif self.component == "Endplate":
                    endplate = self.TObj.get_end_plates_models()
                    end_nutbolt = self.TObj.get_end_nut_bolt_array_models()
                    osdag_display_shape(self.display, endplate, color=Quantity_NOC_BLUE1, update=True)
                    osdag_display_shape(self.display, end_nutbolt, color=Quantity_NOC_YELLOW, update=True)
                else:
                    connector = BRepAlgoAPI_Fuse(nutbolt, plate).Shape()
                    shape = BRepAlgoAPI_Fuse(connector, member).Shape()
                    self.TObj.shape = shape
                    osdag_display_shape(self.display, member, update=True)
                    osdag_display_shape(self.display, plate, color=Quantity_NOC_BLUE1, update=True)
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_YELLOW, update=True)


            elif self.connection == KEY_DISP_TENSION_WELDED:
                self.T = self.module_class()
                self.TObj = self.createTensionCAD()

                member = self.TObj.get_members_models()
                plate = self.TObj.get_plates_models()
                welds = self.TObj.get_welded_models()
                if self.component == "Member":  # Todo: change this into key
                    osdag_display_shape(self.display, member, update=True)
                elif self.component == "Plate":
                    osdag_display_shape(self.display, plate, color=Quantity_NOC_BLUE1, update=True)
                    osdag_display_shape(self.display, welds, color=Quantity_NOC_RED, update=True)
                elif self.component == "Endplate":
                    endplate = self.TObj.get_end_plates_models()
                    osdag_display_shape(self.display, endplate, color=Quantity_NOC_BLUE1, update=True)
                else:
                    connector = BRepAlgoAPI_Fuse(welds, plate).Shape()
                    shape = BRepAlgoAPI_Fuse(connector, member).Shape()
                    self.TObj.shape = shape
                    osdag_display_shape(self.display, member, update=True)
                    osdag_display_shape(self.display, plate, color=Quantity_NOC_BLUE1, update=True)
                    osdag_display_shape(self.display, welds, color=Quantity_NOC_RED, update=True)
    #
    # def display_msg(self):
    #     if self.connection == KEY_DISP_TENSION_BOLTED:
    #         self.T = self.module_class()
    #         #
    #         # distance = self.T.length / 2 - (
    #         #             2 * self.T.plate.end_dist_provided + (self.T.plate.bolt_line - 1) * self.T.plate.pitch_provided)
    #         # Point = gp_Pnt(distance, 0.0, 300)
    #         self.display_msg()



    def call_3DModel(self, flag, module_class):  # Done

        self.module_class = module_class

        if self.mainmodule == "Shear Connection":

            A = self.module_class()

            self.loc = A.connectivity

            if flag is True:

                if self.loc == CONN_CWBW:
                    self.connectivityObj = self.create3DColWebBeamWeb()

                elif self.loc == CONN_CFBW:
                    self.connectivityObj = self.create3DColFlangeBeamWeb()

                else:
                    self.connectivityObj = self.create3DBeamWebBeamWeb()

                self.display_3DModel("Model","gradient_bg")
            else:
                self.display.EraseAll()

        elif self.mainmodule == "Moment Connection":

            if self.connection == KEY_DISP_BEAMCOVERPLATE or self.connection == KEY_DISP_BEAMCOVERPLATEWELD:
                if flag is True:

                    self.CPObj = self.createBBCoverPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")
                else:
                    self.display.EraseAll()

            elif self.connection == KEY_DISP_BB_EP_SPLICE:
                if flag is True:

                    self.CPObj = self.createBBEndPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()

            elif self.connection == KEY_DISP_BCENDPLATE:
                if flag is True:

                    self.CPObj = self.createBCEndPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()

            elif self.connection == KEY_DISP_COLUMNCOVERPLATE or self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:
                if flag is True:

                    self.CPObj = self.createCCCoverPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()

            elif self.connection == KEY_DISP_COLUMNENDPLATE:
                if flag is True:
                    self.CEPObj = self.createCCEndPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")
                else:
                    self.display.EraseAll()

            elif self.connection == KEY_DISP_BASE_PLATE:

                if flag is True:
                    self.BPObj = self.createBasePlateCAD()

                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()

        else:
            if self.connection == KEY_DISP_TENSION_BOLTED or self.connection == KEY_DISP_TENSION_WELDED:

                if flag is True:
                    self.TObj = self.createTensionCAD()

                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()

    # def call_saveOutputs(self):  # Done
    #     return self.call_calculation(self.uiObj)
    #
    # def call2D_Drawing(self, viKEY_DISP_BASE_PLATEew, fileName, folder):  # Rename function with call_view_images()
    #     ''' This routine saves the 2D SVG image as per the connectivity selected
    #     SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
    #     '''
    #     if view == "All":
    #
    #         self.callDesired_View(fileName, view, folder)
    #         # self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)
    #         #
    #         # data = os.path.join(str(folder), "images_html", "3D_Model.png")
    #         #
    #         # self.display.ExportToImage(data)
    #         #
    #         # # self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
    #         # self.display.View_Iso()
    #         # self.display.FitAll()
    #
    #     else:
    #
    #         f = open(fileName, 'w')
    #
    #         self.callDesired_View(fileName, view, folder)
    #         f.close()
    #
    # def callDesired_View(self, fileName, view, folder):
    #
    #     if self.connection == "Fin Plate":
    #         finCommonObj = FinCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata, folder)
    #         finCommonObj.saveToSvg(str(fileName), view)
    #     elif self.connection == "Endplate":
    #         endCommonObj = EndCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata, folder)
    #         endCommonObj.save_to_svg(str(fileName), view)
    #     elif self.connection == "cleatAngle":
    #         cleatCommonObj = cleatCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata,
    #                                          self.dictangledata, folder)
    #         cleatCommonObj.save_to_svg(str(fileName), view)
    #     else:
    #         seatCommonObj = SeatCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata,
    #                                        self.dictangledata, self.dicttopangledata, folder)
    #         seatCommonObj.save_to_svg(str(fileName), view)
    #
    # def call_saveMessages(self):  # Done
    #
    #     if self.connection == "Fin Plate":
    #         fileName = os.path.join("Connections", "Shear", "Fin Plate", "fin.log")
    #
    #     elif self.connection == "Endplate":
    #         fileName = os.path.join("Connections", "Shear", "Endplate", "end.log")
    #
    #     elif self.connection == "cleatAngle":
    #         fileName = os.path.join("Connections", "Shear", "cleatAngle", "cleat.log")
    #
    #     else:
    #         fileName = os.path.join("Connections", "Shear", "SeatedAngle", "seatangle.log")
    #
    #     return fileName
    #
    # def call_designReport(self, htmlfilename, profileSummary):
    #
    #     fileName = str(htmlfilename)
    #
    #     if self.connection == "Fin Plate":
    #         fin_save_html(self.resultObj, self.uiObj, self.dictbeamdata, self.dictcoldata, profileSummary,
    #                       htmlfilename, self.folder)
    #     elif self.connection == "Endplate":
    #         end_save_html(self.resultObj, self.uiObj, self.dictbeamdata, self.dictcoldata, profileSummary,
    #                       htmlfilename, self.folder)
    #     elif self.connection == "cleatAngle":
    #         cleat_save_html(self.resultObj,self.uiObj,self.dictbeamdata,self.dictcoldata,self.dictangledata,
    #                         profileSummary,htmlfilename, self.folder)
    #     else:
    #         self.sa_report = ReportGenerator(self.sa_calc_obj)
    #         self.sa_report.save_html(profileSummary,htmlfilename,self.folder)
    #
    # def load_userProfile(self):
    #     # TODO load_userProfile - deepa
    #     pass
    #
    #
    # def save_userProfile(self, profile_summary, fileName):
    #     # TODO save_userProfile - deepa
    #     filename = str(fileName)
    #
    #     infile = open(filename, 'w')
    #     json.dump(profile_summary, infile)
    #     infile.close()
    #     pass
    #
    # def save_CADimages(self):  # png,jpg and tiff
    #     # TODO save_CADimages - deepa
    #     pass

    def create2Dcad(self):
        ''' Returns the 3D model of finplate depending upon component
        '''

        final_model = None
        cadlist = []

        if self.mainmodule == "Shear Connection":
            if self.component == "Beam":
                final_model = self.connectivityObj.get_beamModel()
            elif self.component == "Column":
                final_model = self.connectivityObj.get_columnModel()
            elif self.component == "Plate":
                cadlist = [self.connectivityObj.weldModelLeft, self.connectivityObj.weldModelRight,
                           self.connectivityObj.plateModel] + self.connectivityObj.nut_bolt_array.get_models()
            elif self.component == "cleatAngle":
                cadlist = [self.connectivityObj.angleModel, self.connectivityObj.angleLeftModel] + \
                          self.connectivityObj.nut_bolt_array.get_models()
            elif self.component == "SeatAngle":
                cadlist = [self.connectivityObj.topclipangleModel, self.connectivityObj.angleModel] + \
                          self.connectivityObj.nut_bolt_array.get_models()
            else:
                cadlist = self.connectivityObj.get_models()

        elif self.mainmodule == "Moment Connection":
            if self.connection == KEY_DISP_BEAMCOVERPLATE or self.connection == KEY_DISP_BEAMCOVERPLATEWELD:
                if self.component == "Beam":
                    if self.connection == KEY_DISP_BEAMCOVERPLATE:
                        final_model = self.CPObj.get_only_beams_Models()
                    else:
                        final_model = self.CPObj.get_beam_models()
                elif self.component == "Connector":
                    if self.connection == KEY_DISP_BEAMCOVERPLATE:
                        cadlist = [self.CPObj.get_flangewebplatesModel(), self.CPObj.get_nut_bolt_arrayModels()]
                        if self.B.preference != 'Outside':
                            cadlist.insert(1, self.CPObj.get_innetplatesModels())
                    else:
                        cadlist = [self.CPObj.get_plate_models(), self.CPObj.get_welded_modules()]
                else:
                    cadlist = self.CPObj.get_models()

            elif self.connection == KEY_DISP_BB_EP_SPLICE:

                if self.component == "Beam":
                    final_model = self.CPObj.get_beam_models()

                elif self.component == "Connector":

                    final_model = self.CPObj.get_connector_models()

                else:
                    final_model = self.CPObj.get_models()

            elif self.connection == KEY_DISP_BCENDPLATE:

                # self.ExtObj = self.create_extended_both_ways()
                if self.component == "Column":
                    final_model = self.CPObj.get_column_models()

                elif self.component == "Beam":
                    final_model = self.CPObj.get_beam_models()

                elif self.component == "Connector":
                    final_model = self.CPObj.get_connector_models()

                else:
                    final_model = self.CPObj.get_models()


            elif self.connection == KEY_DISP_COLUMNCOVERPLATE or self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:
                if self.component == "Column":
                    if self.connection == KEY_DISP_COLUMNCOVERPLATE:
                        final_model = self.CPObj.get_only_column_models()
                    else:
                        final_model = self.CPObj.get_column_models()
                elif self.component == "Cover Plate":
                    if self.connection == KEY_DISP_COLUMNCOVERPLATE:
                        cadlist = [self.CPObj.get_plate_models(), self.CPObj.get_nut_bolt_models()]
                    else:
                        cadlist = [self.CPObj.get_plate_models(), self.CPObj.get_welded_modules()]
                else:
                    cadlist = self.CPObj.get_models()

            elif self.connection == KEY_DISP_COLUMNENDPLATE:
                if self.component == "Column":
                    final_model = self.CEPObj.get_column_models()
                elif self.component == "Connector":
                    plates = self.CEPObj.get_plate_models()
                    welds = self.CEPObj.get_weld_models()
                    nutBolts = self.CEPObj.get_nut_bolt_models()
                    cadlist = [plates, welds, nutBolts]
                else:
                    final_model = self.CEPObj.get_models()

            elif self.connection == KEY_DISP_BASE_PLATE:
                if self.component == "Column":
                    final_model = self.BPObj.get_column_model()
                elif self.component == "Connector":
                    plate = self.BPObj.get_plate_connector_models()
                    weld = self.BPObj.get_welded_models()
                    nut_bolt = self.BPObj.get_nut_bolt_array_models()
                    cadlist = [plate, weld, nut_bolt]
                else:
                    final_model = self.BPObj.get_models()

        elif self.mainmodule == "Member":
            if self.connection == KEY_DISP_TENSION_BOLTED or self.connection == KEY_DISP_TENSION_WELDED:
                if self.component == "Member":
                    final_model = self.TObj.get_members_models()
                elif self.component == "Plate":
                    if self.connection == KEY_DISP_TENSION_BOLTED:
                        cadlist = [self.TObj.get_plates_models(), self.TObj.get_nut_bolt_array_models()]
                    else:
                        cadlist = [self.TObj.get_plates_models(), self.TObj.get_welded_models()]
                else:
                    # print(type(self.TObj.shape))
                    final_model = self.TObj.shape
                    # cadlist = self.TObj.get_models() #TODO: get_models() in BoltedCAD.py and WeldedCAD.py is not returning anything right now.

        if cadlist and len(cadlist) > 1:
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

        return final_model

        # if self.component == "Beam":
        #     # final_model = self.connectivityObj.get_beamModel()
        #     final_model = Obj.get_beamModel()
        #
        # elif self.component == "Column":
        #     # final_model = self.connectivityObj.columnModel
        #     final_model = Obj.columnModel
        #
        # elif self.component == "Plate":
        #     # cadlist = [self.connectivityObj.weldModelLeft,
        #     #            self.connectivityObj.weldModelRight,
        #     #            self.connectivityObj.plateModel] + self.connectivityObj.nut_bolt_array.get_models()
        #     cadlist = [Obj.weldModelLeft,
        #                Obj.weldModelRight,
        #                Obj.plateModel] + Obj.nut_bolt_array.get_models()
        #     final_model = cadlist[0]
        #     for model in cadlist[1:]:
        #         final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        # else:
        #     # cadlist = self.connectivityObj.get_models()
        #     cadlist = Obj.get_models()
        #     if self.connection == KEY_DISP_BASE_PLATE:
        #         return cadlist
        #     final_model = cadlist[0]
        #     for model in cadlist[1:]:
        #         final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

# if __name__!= "__main__":
#
#     CommonDesignLogic()



