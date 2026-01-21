'''
Created on 18-Nov-2016

@author: deepa,
modified : Sourabh Das, Darshan Vishwakarma
'''

# from utils.common.component import Bolt,Beam,Section,Angle,Plate,Nut,Column,Weld
import gc
from .items.notch import Notch
from .items.bolt import Bolt
from .items.nut import Nut
from .items.plate import Plate
from .items.washer import Washer
from .items.ISection import ISection
from .items.filletweld import FilletWeld
from .items.groove_weld import GrooveWeld
from .items.angle import Angle
from .items.anchor_bolt import AnchorBolt_A, AnchorBolt_B, AnchorBolt_Endplate
from .items.stiffener_plate import StiffenerPlate
from .items.grout import Grout
from .items.angle import Angle
from .items.channel import Channel
from .items.Gasset_plate import GassetPlate
from .items.stiffener_flange import Stiffener_flange
from .items.rect_hollow import RectHollow
from .items.circular_hollow import CircularHollow
from .items.double_angles import BackToBackAnglesWithGussetsSameSide
from .items.double_angles import BackToBackAnglesWithGussetsOppSide
from .items.purlin import *

from .ShearConnections.FinPlate.beamWebBeamWebConnectivity import BeamWebBeamWeb as FinBeamWebBeamWeb
from .ShearConnections.FinPlate.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as FinColFlangeBeamWeb
from .ShearConnections.FinPlate.colWebBeamWebConnectivity import ColWebBeamWeb as FinColWebBeamWeb
from .ShearConnections.FinPlate.nutBoltPlacement import NutBoltArray as finNutBoltArray

from .ShearConnections.CleatAngle.beamWebBeamWebConnectivity import BeamWebBeamWeb as cleatBeamWebBeamWeb
from .ShearConnections.CleatAngle.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as cleatColFlangeBeamWeb
from .ShearConnections.CleatAngle.colWebBeamWebConnectivity import ColWebBeamWeb as cleatColWebBeamWeb
from .ShearConnections.CleatAngle.nutBoltPlacement import NutBoltArray as cleatNutBoltArray

from .ShearConnections.EndPlate.beamWebBeamWebConnectivity import BeamWebBeamWeb as EndBeamWebBeamWeb
from .ShearConnections.EndPlate.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as EndColFlangeBeamWeb
from .ShearConnections.EndPlate.colWebBeamWebConnectivity import ColWebBeamWeb as EndColWebBeamWeb
from .ShearConnections.EndPlate.nutBoltPlacement import NutBoltArray as endNutBoltArray

from .ShearConnections.SeatedAngle.CAD_col_web_beam_web_connectivity import ColWebBeamWeb as seatColWebBeamWeb
from .ShearConnections.SeatedAngle.CAD_col_flange_beam_web_connectivity import ColFlangeBeamWeb as seatColFlangeBeamWeb
from .ShearConnections.SeatedAngle.CAD_nut_bolt_placement import NutBoltArray as seatNutBoltArray
# from .ShearConnections.SeatedAngle.seat_angle_calc import SeatAngleCalculation

from .CompressionMembers.WeldedCAD import StrutAngleWeldCAD, StrutChannelWeldCAD
from .BBCad.nutBoltPlacement_AF import NutBoltArray_AF
from .BBCad.nutBoltPlacement_BF import NutBoltArray_BF
from .BBCad.nutBoltPlacement_Web import NutBoltArray_Web
from .BBCad.BBCoverPlateBoltedCAD import BBCoverPlateBoltedCAD

from .SimpleConnections.BoltedLapJoint.bolted_lap_joint import *
from .SimpleConnections.WeldedLapJoint.welded_lap_joint import *
from .SimpleConnections.BoltedButtJoint.Butt_joint_bolted import *
from .SimpleConnections.WeldedButtJoint.Butt_joint_welded import *

from .FlexuralMember.plate_girder import create_plate_girder

from .MomentConnections.BBSpliceCoverlateCAD.WeldedCAD import BBSpliceCoverPlateWeldedCAD
from .MomentConnections.BBEndplate.BBEndplate_cadFile import CADFillet
from .MomentConnections.BBEndplate.BBEndplate_cadFile import CADGroove
from .MomentConnections.BCEndplate.BCEndplate_cadfile import CADGroove as BCECADGroove
from .MomentConnections.BCEndplate.BCEndplate_cadfile import CADcolwebGroove

from .MomentConnections.CCSpliceCoverPlateCAD.WeldedCAD import CCSpliceCoverPlateWeldedCAD
from .MomentConnections.CCSpliceCoverPlateCAD.BoltedCAD import CCSpliceCoverPlateBoltedCAD
from .MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_AF import NutBoltArray_AF as CCSpliceNutBolt_AF
from .MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_BF import NutBoltArray_BF as CCSpliceNutBolt_BF
from .MomentConnections.CCSpliceCoverPlateCAD.nutBoltPlacement_Web import NutBoltArray_Web as CCSpliceNutBolt_Web

from .BasePlateCad.baseplateconnection import BasePlateCad, HollowBasePlateCad
from .BasePlateCad.nutBoltPlacement import NutBoltArray as bpNutBoltArray

from .CompressionMembers.column import CompressionMemberCAD
from .CompressionMembers.BoltedCAD import StrutAngleBoltCAD, StrutChannelBoltCAD

from .Tension.WeldedCAD import TensionAngleWeldCAD, TensionChannelWeldCAD
from .Tension.BoltedCAD import TensionAngleBoltCAD, TensionChannelBoltCAD
from .Tension.nutBoltPlacement import NutBoltArray as TNutBoltArray
from .Tension.intermittentConnections import IntermittentNutBoltPlateArray, IntermittentWelds

from .MomentConnections.CCEndPlateCAD.CAD import CCEndPlateCAD
from .MomentConnections.CCEndPlateCAD.nutBoltPlacement import NutBoltArray as CEPNutBoltArray

# from ..design_type.connection.fin_plate_connection import FinPlateConnection
# from ..design_type.connection.cleat_angle_connection import CleatAngleConnection
from ..design_type.connection.beam_cover_plate import BeamCoverPlate
# from ..design_type.connection.base_plate_connection import BasePlateConnection
from ..utilities import osdag_display_shape, DisplayMsg
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
import copy

from .BBCad.nutBoltPlacement_AF import NutBoltArray_AF
from .BBCad.nutBoltPlacement_BF import NutBoltArray_BF
from .BBCad.nutBoltPlacement_Web import NutBoltArray_Web
from .BBCad.BBCoverPlateBoltedCAD import BBCoverPlateBoltedCAD
from .MomentConnections.BBEndplate.BBE_nutBoltPlacement import BBENutBoltArray
from .MomentConnections.BCEndplate.BCE_nutBoltPlacement import BCE_NutBoltArray
from ..Common import *
from math import *
from OCC.Core.TopoDS import TopoDS_Shape
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
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeBox
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound

import OCC.Core.V3d
from OCC.Core.Quantity import *
from OCC.Core.Graphic3d import *
from OCC.Core.Quantity import Quantity_NOC_GRAY25 as GRAY
# from OCC.Core.AIS import Erase
# from OCC.Display.OCCViewer import V3d_XposYnegZneg
from OCC.Core.TNaming import tnaming
import multiprocessing
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.AIS import AIS_Point
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

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
from osdag.cad.items.plate import Plate
from osdag.cad.items.angle import Angle
from ..utils.common.component import ISection as ISectionComponent
from ..utils.common.component import Column
from ..utils.common.component import Beam
from ..utils.common.component import CHS
from ..utils.common.component import RHS
from ..utils.common.component import SHS
from ..utils.common.component import Angle as AngleComponent
import numpy
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


    def __init__(self, display, cad_widget, folder, connection, mainmodule):

        self.display = display
        self.cad_widget = cad_widget
        self.mainmodule = mainmodule
        self.connection = connection
        print(self.connection)

        # To capture the type of model which is rendered
        self.rendering_models = {}

        # Initialize component attribute to avoid AttributeError
        self.component = None
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

        A = self.module_object  

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

        A = self.module_object  

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

        A = self.module_object  

        if self.connection == KEY_DISP_FINPLATE:
            # A = self.module_class()
            # A = FinPlateConnection()
            gap = A.plate.gap
        elif self.connection == KEY_DISP_CLEATANGLE:
            # A = CleatAngleConnection()
            angle = Angle(L=A.cleat.height, A=A.cleat.leg_a_length, B=A.cleat.leg_b_length, T=A.cleat.thickness,
                          R1=A.cleat.root_radius, R2=A.cleat.toe_radius)
            print("BOLT DETAILS")
            print("bolt:", A.bolt)
            print("bolt2:", A.bolt2)
            print("spting_leg.bolts_one_line:", A.spting_leg.bolts_one_line)
            print("spting_leg.bolt_line:", A.spting_leg.bolt_line)
            print("total_bolts_spting:", A.total_bolts_spting)
            print("get_bolt_PC:", A.get_bolt_PC)
            print("bolt_values:", A.bolt_values)
            print("END BOLT DETAILS")


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
            B = self.B 
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
            bolting_AF = NutBoltArray_AF(self.B, nut, bolt, numOfBoltsF, nutSpaceF)

            # Bolt placement for Below Flange bolts, call to nutBoltPlacement_BF.py
            bolting_BF = NutBoltArray_BF(self.B, nut, bolt, numOfBoltsF, nutSpaceF)

            # Bolt placement for Web Plate bolts, call to nutBoltPlacement_Web.py
            bolting_Web = NutBoltArray_Web(self.B, nut, bolt, numOfBoltsW, nutSpaceW)

            # bbCoverPlate is an object which is passed BBCoverPlateBoltedCAD.py file, which initialized the parameters of each CAD component
            bbCoverPlate = BBCoverPlateBoltedCAD(beam_Left, beam_Right, plateAbvFlange, plateBelwFlange,
                                                 innerplateAbvFlangeFront,
                                                 innerplateAbvFlangeBack, innerplateBelwFlangeFront,
                                                 innerplateBelwFlangeBack,
                                                 WebPlateLeft, WebPlateRight, bolting_AF, bolting_BF, bolting_Web,
                                                 self.B)

            # bbCoverPlate.create_3DModel() will create the CAD model of each component, debugging this line will give moe clarity
            bbCoverPlate.create_3DModel()

        elif self.connection == KEY_DISP_BEAMCOVERPLATEWELD:
            B = self.module_object  
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
        # NOTE: Do NOT call gc.collect() during CAD operations - it causes heap corruption
        # See OCC Memory Architecture documentation for details

        BBE = self.module_object  

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
        # CRITICAL: Create new instance instead of copy.copy to prevent shared numpy array state
        beam_Right = copy.copy(beam_Left) # Since both the beams are same

        plate_Left = Plate(W=BBE.ep_width_provided,
                           L=BBE.ep_height_provided,
                           T=BBE.plate_thickness)
        plate_Right = copy.copy(plate_Left) # Since both the end plates are identical

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
        BCE = self.module_object



        print("bolt_diameter_provided:", BCE.bolt_diameter_provided)
        print("bolt_grade_provided:", BCE.bolt_grade_provided)
        print("bolt_numbers:", BCE.bolt_numbers)
        print("BCE.ep_height_provided:", BCE.ep_height_provided)
        print("BCE.ep_width_provided:", BCE.ep_width_provided)

        print("BCE.edge_distance_provided:", BCE.edge_distance_provided)
        print("BCE.end_distance_provided:", BCE.end_distance_provided)
        print("BCE.endplate_type:", BCE.endplate_type)
        print("BCE.ep_height_max:", BCE.ep_height_max)
        print("BCE.epsilon_beam:", BCE.epsilon_beam)
        print("BCE.plate_thickness:", BCE.plate_thickness)








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
            C = self.module_object  
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

            C = self.module_object  
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
        CEP = self.module_object  

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

        BP = self.module_object  

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
        T = self.module_object

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

    def createColumnInFrameCAD(self):
        """
            :return: The calculated values/parameters to create 3D CAD model of individual components.
        """

        Col = self.module_object
        print("COL_DESIGINATION :",Col.result_designation)

        if 'RHS' in Col.result_designation or 'SHS' in Col.result_designation:  # hollow sections 'RHS and SHS'
            if 'RHS' in Col.result_designation:
                result = RHS(designation=Col.result_designation, material_grade=Col.material)
            else:
                result = SHS(designation=Col.result_designation, material_grade=Col.material)
            Col.section_property = result
            print(f"Parameter L (flange width): {float(Col.section_property.flange_width)}")
            print(f"Parameter W (depth): {float(Col.section_property.depth)}")
            print(f"Parameter H (length/height): {float(Col.length_zz)}")
            print(f"Parameter T (flange thickness): {float(Col.section_property.flange_thickness)}")
            sec = RectHollow(L=float(Col.section_property.flange_width), W=float(Col.section_property.depth),
                             H=float(Col.length_zz), T=float(Col.section_property.flange_thickness))
            col = CompressionMemberCAD(sec)
            sec=sec.create_model()
            col.create_3DModel()
        elif 'CHS' in Col.result_designation:  # CHS
            result = CHS(designation=Col.result_designation, material_grade=Col.material)
            Col.section_property = result
            print(f"Parameter r (radius): {float(Col.section_property.depth) / 2}")
            print(f"Parameter T (thickness): {float(Col.section_property.flange_thickness)}")
            print(f"Parameter H (height/length): {float(Col.length_zz)}")
            sec = CircularHollow(r=float(Col.section_property.depth) / 2, T=float(Col.section_property.flange_thickness),
                                 H=float(Col.length_zz))
            col = CompressionMemberCAD(sec)
            sec=sec.create_model()
            col.create_3DModel()
        else: # Beams and Columns (rolled sections)
            try:
                result = Beam(designation=Col.result_designation, material_grade=Col.material)
            except:
                result = Column(designation=Col.result_designation, material_grade=Col.material)
            Col.section_property = result

            column_tw = float(Col.section_property.web_thickness)
            print(f"column_tw (Web Thickness): {column_tw}")

            column_T = float(Col.section_property.flange_thickness)
            print(f"column_T (Flange Thickness): {column_T}")

            column_d = float(Col.section_property.depth)
            print(f"column_d (Depth): {column_d}")

            column_B = float(Col.section_property.flange_width)
            print(f"column_B (Flange Width): {column_B}")

            column_R1 = float(Col.section_property.root_radius)
            print(f"column_R1 (Root Radius): {column_R1}")

            column_R2 = float(Col.section_property.toe_radius)
            print(f"column_R2 (Toe Radius): {column_R2}")

            column_alpha = 94  # Todo: connect this. Waiting for danish to give variable
            column_length = float(Col.length_zz)

            sec = ISection(B=column_B, T=column_T, D=column_d, t=column_tw, R1=column_R1, R2=column_R2,
                              alpha=column_alpha, length=column_length, notchObj=None)
            col = CompressionMemberCAD(sec)
            sec=sec.create_model()

            col.create_3DModel()

        return sec

    def createBoltedLapJoint(self):

        Conn = self.module_object
        print("THIS IS CONN")
        print(Conn)
        for attr in dir(Conn):
            if not callable(getattr(Conn, attr)) and not attr.startswith("__"):
                print(f"{attr}: {getattr(Conn, attr)}")

        print(f"Plate 1 Thickness: {float(Conn.plate1thk)}")
        print(f"Plate 2 Thickness: {float(Conn.plate2thk)}")
        print(f"Plate Width: {float(Conn.width)}")
        print(f"Bolt Diameter: {Conn.bolt.bolt_diameter_provided}")
        print(f"Actual Overlap Length: {Conn.len_conn}")
        print(f"Bolt Columns: {Conn.cols}")
        print(f"Bolt Rows: {Conn.rows}")
        print(f"Number of Bolts: {Conn.number_bolts}")
        print(f"Pitch: {Conn.final_pitch}")
        print(f"Gauge: {Conn.final_gauge}")
        print(f"Edge Distance: {Conn.final_edge_dist}")
        print(f"End Distance: {Conn.final_end_dist}")

        lap_joint, plate1, plate2, bolts, nuts = create_bolted_lap_joint(plate1_thickness = float(Conn.plate1thk), plate2_thickness = float(Conn.plate2thk), plate_width = float(Conn.width), bolt_dia = Conn.bolt.bolt_diameter_provided,
                                                                         actual_overlap_length=Conn.len_conn,bolt_cols=Conn.cols,bolt_rows=Conn.rows, number_bolts=Conn.number_bolts,
                                                                         pitch=Conn.final_pitch,gauge=Conn.final_gauge,
                                                                         edge=Conn.final_edge_dist,end=Conn.final_end_dist)
        return lap_joint, plate1, plate2, bolts, nuts

    def createWeldedLapJoint(self):
        Conn = self.module_object
        
        plate1_thickness = float(Conn.plate1.thickness[0])
        plate2_thickness = float(Conn.plate2.thickness[0])
        plate_width = float(Conn.width)
        overlap_length = float(Conn.connection_length)
        weld_size = float(Conn.weld_size)
        
        print(f"DEBUG: createWeldedLapJoint called with: t1={plate1_thickness}, t2={plate2_thickness}, w={plate_width}, l={overlap_length}, s={weld_size}")
        
        lap_joint, plate1, plate2, welds = create_welded_lap_joint(plate1_thickness, plate2_thickness, plate_width, overlap_length, weld_size)
        print(f"DEBUG: create_welded_lap_joint returned: {lap_joint}, {plate1}, {plate2}, {welds}")
        return lap_joint, plate1, plate2, welds

    def createPlateGirderCAD(self):
        """
        Create the 3D CAD model for a welded plate girder.
        Extracts parameters from the PlateGirderWelded module object.
        """
        Conn = self.module_object
        
        print("DEBUG: createPlateGirderCAD called")
        print(f"DEBUG: Module object type: {type(Conn).__name__}")
        
        # Extract parameters from the PlateGirderWelded object
        D = float(getattr(Conn, 'total_depth', 750))
        tw = float(getattr(Conn, 'web_thickness', 14))
        length = float(getattr(Conn, 'length', 15000))
        T_ft = float(getattr(Conn, 'top_flange_thickness', 20))
        T_fb = float(getattr(Conn, 'bottom_flange_thickness', 20))
        B_ft = float(getattr(Conn, 'top_flange_width', 400))
        B_fb = float(getattr(Conn, 'bottom_flange_width', 400))
        
        # Stiffener parameters
        stiffener_spacing = float(getattr(Conn, 'c', 750)) if hasattr(Conn, 'c') and Conn.c not in ['NA', None, ''] else 750
        T_is = float(getattr(Conn, 'IntStiffThickness', 15)) if hasattr(Conn, 'IntStiffThickness') else 15
        
        # Handle NA values for spacing
        if isinstance(stiffener_spacing, str):
            stiffener_spacing = 750
        
        print(f"DEBUG: Plate Girder Parameters:")
        print(f"  D={D}, tw={tw}, length={length}")
        print(f"  T_ft={T_ft}, T_fb={T_fb}, B_ft={B_ft}, B_fb={B_fb}")
        print(f"  stiffener_spacing={stiffener_spacing}, T_is={T_is}")
        
        
        # Horizontal plate / Longitudinal Stiffener parameters
        include_horizontal_plate = False
        T_hp = 15.0
        horizontal_plate_offset_ratio = 0.2

        try:
            # Check number of longitudinal stiffeners
            # Handle both numeric values (0, 1, 2) and string "Not Required"
            num_long_stiff = getattr(Conn, 'longstiffener_no', 0)
            
            # Convert to number for comparison, treating "Not Required" and similar strings as 0
            if num_long_stiff is None or str(num_long_stiff).strip() in ['', 'Not Required', 'N/A', '0']:
                num_long_stiff_val = 0
            else:
                try:
                    num_long_stiff_val = float(num_long_stiff)
                except (ValueError, TypeError):
                    num_long_stiff_val = 0
            
            if num_long_stiff_val > 0:
                include_horizontal_plate = True
                
                # Get thickness
                thk_val = getattr(Conn, 'longstiffener_thk', 15)
                if thk_val is not None and str(thk_val).strip() not in ['', 'Not Required', 'N/A']:
                    try:
                        T_hp = float(thk_val)
                    except (ValueError, TypeError):
                        T_hp = 15.0
                
                # Get position/offset
                pos_val = getattr(Conn, 'x1', 0)
                if pos_val is not None and str(pos_val).strip() not in ['', 'Not Required', 'N/A']:
                    try:
                        # x1 is distance from compression flange (top)
                        horizontal_plate_offset_ratio = float(pos_val) / D
                    except (ValueError, TypeError):
                        horizontal_plate_offset_ratio = 0.2
        except Exception as e:
            print(f"Error extracting horizontal plate params: {e}")
            include_horizontal_plate = False

        # DEBUG: Print horizontal plate status
        print(f"DEBUG CAD: include_horizontal_plate={include_horizontal_plate}, num_long_stiff_val={num_long_stiff_val if 'num_long_stiff_val' in dir() else 'not set'}")
        
        # Create the plate girder model
        components = create_plate_girder(
            D=D,
            tw=tw,
            length=length,
            T_ft=T_ft,
            T_fb=T_fb,
            B_ft=B_ft,
            B_fb=B_fb,
            stiffener_spacing=stiffener_spacing,
            T_is=T_is,
            chamfer_length=30,
            weld_size=15,
            include_horizontal_plate=include_horizontal_plate,
            horizontal_plate_offset_ratio=horizontal_plate_offset_ratio,
            T_hp=T_hp,
        )
        
        # Store components for display_3DModel
        self.plate_girder_components = components
        
        return components

    def createButtJointBoltedCAD(self):
          
            # Get input values from the design object (i.e., instance of ButtJointBolted)
            Col = self.module_object

            # Extract parameters from the ButtJointBolted object
            self.plate1_thickness = float(Col.plate1.thickness[0])
            self.plate2_thickness = float(Col.plate2.thickness[0])
            self.cover_thickness = float(Col.calculated_cover_plate_thickness)
            self.plate_width = float(Col.width)
            self.bolt_dia = float(Col.bolt.bolt_diameter_provided)
            self.bolt_rows = int(Col.rows)
            self.bolt_cols = int(Col.cols)
            self.pitch = float(Col.final_pitch)
            self.gauge = float(Col.final_gauge)
            self.edge = float(Col.final_edge_dist)
            self.end = float(Col.final_end_dist)
            self.number_bolts = int(Col.number_bolts)
            
            # Cover plate type extraction
            self.cover_type = "Single-Cover"
            cp_input = str(Col.cover_plate_type) if hasattr(Col, 'cover_plate_type') else "Single Cover Plate"
            if "Double" in cp_input or "double" in cp_input:
                self.cover_type = "Double-Cover"

            butt_joint, plate1, plate2, platec, platec2, bolts, nuts, packing1, packing2 = create_bolted_butt_joint(
                self.plate1_thickness, self.plate2_thickness, self.cover_thickness, self.plate_width, self.bolt_dia,
                self.bolt_rows, self.bolt_cols, self.pitch, self.gauge, self.edge, self.end, self.number_bolts,
                cover_type=self.cover_type)
            return butt_joint, plate1, plate2, platec, platec2, bolts, nuts, packing1, packing2

    def createButtJointWeldedCAD(self):
        # Get input values from the design object
        Col = self.module_object

        # Extract parameters
        self.plate1_thickness = float(Col.plate1.thickness[0])
        self.plate2_thickness = float(Col.plate2.thickness[0])
        
        # Cover plate type extraction with defaults
        self.cover_type = "Single-Cover"
        cp_input = str(Col.cover_plate_type) if hasattr(Col, 'cover_plate_type') else "Single Cover Plate"
        print(f"DEBUG: cover_plate_type from design object: '{cp_input}' (hasattr: {hasattr(Col, 'cover_plate_type')})")
        if "Double" in cp_input or "double" in cp_input:
            self.cover_type = "Double-Cover"
        else:
             self.cover_type = "Single-Cover"
        print(f"DEBUG: Final cover_type: '{self.cover_type}'")

        self.cover_thickness = float(Col.calculated_cover_plate_thickness)
        self.plate_width = float(Col.width)
        # weld.size can be a list or scalar, handle both
        weld_size_val = Col.weld.size
        if isinstance(weld_size_val, list):
            self.weld_size = float(weld_size_val[0])
        else:
            self.weld_size = float(weld_size_val)

        # Call the standalone CAD generator
        # Call the standalone CAD generator
        print("CreateButtJointWeldedCAD: Parameters:")
        print(f"Plate1 Thk: {self.plate1_thickness} (type: {type(self.plate1_thickness)})")
        print(f"Plate2 Thk: {self.plate2_thickness} (type: {type(self.plate2_thickness)})")
        print(f"Cover Thk: {self.cover_thickness} (type: {type(self.cover_thickness)})")
        print(f"Width: {self.plate_width} (type: {type(self.plate_width)})")
        print(f"Weld Size: {self.weld_size} (type: {type(self.weld_size)})")
        print(f"Cover Type: {self.cover_type} (type: {type(self.cover_type)})")

        try:
            assembly, plate1, plate2, platec, platec2, welds, packing1, packing2 = create_welded_butt_joint(
                plate1_thickness=self.plate1_thickness,
                plate2_thickness=self.plate2_thickness,
                cover_thickness=self.cover_thickness,
                plate_width=self.plate_width,
                weld_size=self.weld_size,  # Use calculated weld size from design
                cover_type=self.cover_type
            )
        except Exception as e:
            print(f"ERROR in createButtJointWeldedCAD: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None, None, None, [], None, None
        return assembly, plate1, plate2, platec, platec2, welds, packing1, packing2

    def createSimplySupportedBeam(self):

        Flex = self.module_object

        print(f"Flex.support {Flex.support}")

        Flex.section_property = Flex.section_connect_database(Flex.result_designation)
        column_tw = float(Flex.section_property.web_thickness)
        print(f"Flex.section_property.web_thickness : {Flex.section_property.web_thickness}")
        column_T = float(Flex.section_property.flange_thickness)
        print(f"Flex.section_property.flange_thickness : {Flex.section_property.flange_thickness}")
        column_d = float(Flex.section_property.depth)
        print(f"Flex.section_property.depth : {Flex.section_property.depth}")
        column_B = float(Flex.section_property.flange_width)
        print(f"Flex.section_property.flange_width : {Flex.section_property.flange_width}")
        column_R1 = float(Flex.section_property.root_radius)
        print(f"Flex.section_property.root_radius : {Flex.section_property.root_radius}")
        column_R2 = float(Flex.section_property.toe_radius)
        print(f"Flex.section_property.toe_radius : {Flex.section_property.toe_radius}")
        column_alpha = 94  # Todo: connect this. Waiting for danish to give variable
        column_length = float(Flex.result_eff_len)*1000

        sec = ISection(B=column_B, T=column_T, D=column_d, t=column_tw, R1=column_R1, R2=column_R2,
                              alpha=column_alpha, length=column_length, notchObj=None)
        _place=sec.place(numpy.array([0.,0.,0.]),numpy.array([1.,0.,0.]),numpy.array([0.,1.,0.]))
        col = CompressionMemberCAD(sec)

        beam_model = sec.create_model()
        col.create_Flex3DModel()

        # --- Create Supports ---
        triangle_supp = None
        cyl_supp = None
        support_block = None
        hatching_lines = None
        support_knot = None

        if Flex.support == 'Simply Supported':
            # Dimensions
            x_start = -column_B / 2.0
            # Set contact level to the Bottom Flange
            z_contact = -column_d / 2.0
            
            # 2. Cylindrical Support at End (Right) - Roller
            # Determine Support Height based on Beam Length vs Depth
            if column_length <= column_d:
                h_supp = 0.30 * column_d
            else:
                h_supp = 0.75 * column_d
            
            # 2. Cylindrical Support at End (Right) - Roller
            # Radius = Half of Total Triangular Height (Prism + Small Cylinder)
            # Total Height = h_supp + 0.10 * h_supp = 1.10 * h_supp
            r_cyl = (1.10 * h_supp) / 2.0
            
            # Shift cylinder center inwards by radius so it doesn't stick out
            y_cyl = column_length - r_cyl
            z_cyl_center = z_contact - r_cyl # Below beam
            
            pt_cyl = gp_Pnt(x_start, y_cyl, z_cyl_center)
            axis_cyl = gp_Ax2(pt_cyl, gp_Dir(1, 0, 0))
            
            cyl_supp = BRepPrimAPI_MakeCylinder(axis_cyl, r_cyl, column_B).Shape()
            
            # 1. Triangular Support at Start (Left) - Fixed/Pinned
            # Height: Match the cylinder diameter for visual consistency
            # h_supp already calculated above
            # Base width = 1.5 times of height => Half-Base w_supp = 0.75 * height
            w_supp = 0.75 * h_supp
            
            # Position Apex at Y = w_supp (so start of base is at Y=0)
            y_apex = w_supp
            
            # small cylinder at the top of the prism 
            # diameter is 10% of the height of the triangular prism
            d_small = 0.10 * h_supp
            r_small = d_small / 2.0
            
            # Position small cylinder:
            # Centered at apex Y (y_apex)
            # Touching Beam Bottom (z_contact) -> Center at z_contact - r_small
            pt_small = gp_Pnt(x_start, y_apex, z_contact - r_small)
            axis_small = gp_Ax2(pt_small, gp_Dir(1, 0, 0))
            support_knot = BRepPrimAPI_MakeCylinder(axis_small, r_small, column_B).Shape()
            
            # Shift Triangle Down by Small Cylinder Diameter (2*r_small)
            z_apex = z_contact - d_small
            
            p1 = gp_Pnt(x_start, y_apex, z_apex) # Apex (touching small cylinder)
            p2 = gp_Pnt(x_start, y_apex - w_supp, z_apex - h_supp) # Base point 1 
            p3 = gp_Pnt(x_start, y_apex + w_supp, z_apex - h_supp)  # Base point 2
            
            edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
            edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
            edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
            
            wire_maker = BRepBuilderAPI_MakeWire()
            wire_maker.Add(edge1)
            wire_maker.Add(edge2)
            wire_maker.Add(edge3)
            wire = wire_maker.Wire()
            
            face = BRepBuilderAPI_MakeFace(wire).Face()
            vec = gp_Vec(column_B, 0, 0)
            triangle_supp = BRepPrimAPI_MakePrism(face, vec).Shape()
            
        elif Flex.support == 'Cantilever':
            # Create Support Block (Fixed Support)
            # Dimensions: Large block extending around the beam start
            # Resized to be standard (wall-like)
            # Make block Square (Height = Width)
            block_dim = max(column_d, column_B) * 2.5
            block_h = block_dim
            block_w = block_dim  
            # Thickness = Fixed 250.0 mm (User Request: Prevent scaling with length)
            block_t = 250.0
            beam_embed = 25.0         # Embed beam 25mm into block
            
            # Position: 
            # X: Centered [-w/2, w/2]
            # Z: Centered [-h/2, h/2] (Beam is at Z=0 relative to section center)
            # Y: Behind beam start [-t + embed, embed] to represent embedding/wall
            
            y_max = beam_embed
            y_min = -(block_t - beam_embed)
            
            pt_min = gp_Pnt(-block_w / 2.0, y_min, -block_h / 2.0)
            pt_max = gp_Pnt(block_w / 2.0, y_max, block_h / 2.0)
            
            
            support_block = BRepPrimAPI_MakeBox(pt_min, pt_max).Shape()

            # Create Hatching Lines (Diagonal lines on side faces)
            # User Request: Remove lines from block, add them at the left end (outside support)
            # We will create hatching lines in the region BEHIND the support: [y_min - block_t, y_min]
            # This simulates the "Fixed Wall" extending backwards.
            
            hatch_width = block_t # Arbitrary width for the hatching zone behind support
            y_hatch_end = y_min
            y_hatch_start = y_min - hatch_width
            
            # Face bounds for hatching: Y [y_hatch_start, y_hatch_end], Z [-block_h/2, block_h/2]
            # Line Eq: Z = Y + c  =>  c = Z - Y
            
            # Use Compound instead of Wire for disconnected edges
            hatching_lines = TopoDS_Compound()
            builder = BRep_Builder()
            builder.MakeCompound(hatching_lines)
            
            has_lines = False
            
            # Recalculate c range for the new Y-bounds
            # Min c: (-h/2) - y_hatch_end
            # Max c: (h/2) - y_hatch_start
            
            c_min = (-block_h / 2.0) - y_hatch_end
            c_max = (block_h / 2.0) - y_hatch_start
            step = 50.0
            
            for c in numpy.arange(c_min, c_max, step):
                # Intersection of Line Z = Y + c with Rectangle Bounds [y_hatch_start, y_hatch_end] x [-h/2, h/2]
                points = []
                z_min, z_max = -block_h / 2.0, block_h / 2.0
                
                # Check Y edges (Vertical lines at y_start and y_end)
                z1 = y_hatch_start + c
                if z_min <= z1 <= z_max:
                    points.append((y_hatch_start, z1))
                
                z2 = y_hatch_end + c
                if z_min <= z2 <= z_max:
                    points.append((y_hatch_end, z2))
                    
                # Check Z edges (Horizontal lines at z_min and z_max)
                y1 = z_min - c
                if y_hatch_start <= y1 <= y_hatch_end:
                    points.append((y1, z_min))
                    
                y2 = z_max - c
                if y_hatch_start <= y2 <= y_hatch_end:
                    points.append((y2, z_max))
                
                points = list(set(points))
                
                if len(points) == 2:
                    p1_2d, p2_2d = points[0], points[1]
                    for x_val in [-block_w / 2.0, block_w / 2.0]:
                        pt1 = gp_Pnt(x_val, p1_2d[0], p1_2d[1])
                        pt2 = gp_Pnt(x_val, p2_2d[0], p2_2d[1])
                        edge = BRepBuilderAPI_MakeEdge(pt1, pt2).Edge()
                        builder.Add(hatching_lines, edge)
                        has_lines = True
            
            if not has_lines:
                hatching_lines = None
        
        # Return Dictionary of Components
        components = {
            'beam': beam_model,
            'support_tri': triangle_supp,
            'support_knot': support_knot,
            'support_cyl': cyl_supp,
            'support_block': support_block,
            'support_hatch': hatching_lines
        }

        return components

    def createCantileverBeam(self):
        print("DEBUG: Entering createCantileverBeam")
        try:
            import traceback
            Flex = self.module_object
    
            print(f"Flex.support {Flex.support}")
    
            Flex.section_property = Flex.section_connect_database(Flex.result_designation)
            column_tw = float(Flex.section_property.web_thickness)
            print(f"Flex.section_property.web_thickness : {Flex.section_property.web_thickness}")
            column_T = float(Flex.section_property.flange_thickness)
            print(f"Flex.section_property.flange_thickness : {Flex.section_property.flange_thickness}")
            column_d = float(Flex.section_property.depth)
            print(f"Flex.section_property.depth : {Flex.section_property.depth}")
            column_B = float(Flex.section_property.flange_width)
            print(f"Flex.section_property.flange_width : {Flex.section_property.flange_width}")
            column_R1 = float(Flex.section_property.root_radius)
            print(f"Flex.section_property.root_radius : {Flex.section_property.root_radius}")
            column_R2 = float(Flex.section_property.toe_radius)
            print(f"Flex.section_property.toe_radius : {Flex.section_property.toe_radius}")
            column_alpha = 94  # Todo: connect this. Waiting for danish to give variable
            column_length = float(Flex.result_eff_len)*1000
    
            # Create the beam section
            sec = ISection(B=column_B, T=column_T, D=column_d, t=column_tw, R1=column_R1, R2=column_R2,
                                  alpha=column_alpha, length=column_length, notchObj=None)
            _place=sec.place(numpy.array([0.,0.,0.]),numpy.array([1.,0.,0.]),numpy.array([0.,1.,0.]))
            
            print("DEBUG: Creating CompressionMemberCAD...")
            col = CompressionMemberCAD(sec)
    
            print("DEBUG: Creating beam model...")
            beam_model = sec.create_model()
            
            print("DEBUG: Creating Flex3DModel...")
            col.create_Flex3DModel()
            
            print("DEBUG: Beam model created successfully, now creating support block...")
    
            # Create Support Block (Fixed Support)
            # Dimensions based on sketch: Large block extending around the beam start
            # Increased size as per user request (was 2.0x, now 2.5x)
            block_h = column_d * 2.5  
            block_w = column_B * 2.5  
            block_t = 250.0           # Total Thickness
            beam_embed = 25.0         # Embed beam 25mm into block
            
            # Position: 
            # X: Centered [-w/2, w/2]
            # Z: Centered [-h/2, h/2] (Beam is at Z=0 relative to section center)
            # Y: Behind beam start [-t + embed, embed] to represent embedding/wall
            # If Beam starts at Y=0, we want block to go from -(Thickness - Embed) to +Embed
            
            y_max = beam_embed
            y_min = -(block_t - beam_embed)
            
            pt_min = gp_Pnt(-block_w / 2.0, y_min, -block_h / 2.0)
            pt_max = gp_Pnt(block_w / 2.0, y_max, block_h / 2.0)
            
            print(f"DEBUG: Creating Box with min={pt_min.Coord()}, max={pt_max.Coord()}")
            support_block = BRepPrimAPI_MakeBox(pt_min, pt_max).Shape()
            print("DEBUG: Support block created successfully")
            
            # --- Hatching Lines (Behind Support) ---
            # Region: [y_min - block_t, y_min]
            hatch_width = block_t
            y_hatch_end = y_min
            y_hatch_start = y_min - hatch_width
            
            hatching_lines = TopoDS_Compound()
            builder = BRep_Builder()
            builder.MakeCompound(hatching_lines)
            
            has_lines = False
            
            c_min = (-block_h / 2.0) - y_hatch_end
            c_max = (block_h / 2.0) - y_hatch_start
            step = 50.0
            
            for c in numpy.arange(c_min, c_max, step):
                points = []
                z_min, z_max = -block_h / 2.0, block_h / 2.0
                
                # Check Y edges
                z1 = y_hatch_start + c
                if z_min <= z1 <= z_max: points.append((y_hatch_start, z1))
                
                z2 = y_hatch_end + c
                if z_min <= z2 <= z_max: points.append((y_hatch_end, z2))
                    
                # Check Z edges
                y1 = z_min - c
                if y_hatch_start <= y1 <= y_hatch_end: points.append((y1, z_min))
                    
                y2 = z_max - c
                if y_hatch_start <= y2 <= y_hatch_end: points.append((y2, z_max))
                
                points = list(set(points))
                
                if len(points) == 2:
                    p1_2d, p2_2d = points[0], points[1]
                    for x_val in [-block_w / 2.0, block_w / 2.0]:
                        pt1 = gp_Pnt(x_val, p1_2d[0], p1_2d[1])
                        pt2 = gp_Pnt(x_val, p2_2d[0], p2_2d[1])
                        edge = BRepBuilderAPI_MakeEdge(pt1, pt2).Edge()
                        builder.Add(hatching_lines, edge)
                        has_lines = True
            
            if not has_lines:
                hatching_lines = None

            # Return both beam and support block + hatch as a dictionary
            return {'beam': beam_model, 'support_block': support_block, 'support_hatch': hatching_lines}
            
        except Exception as e:
            print("DEBUG ERROR in createCantileverBeam:")
            print(e)
            traceback.print_exc()
            return {'beam': None, 'support_block': None}

    def createPurlin(self):

        Flex = self.module_object
        print(f"This is the module name {Flex}")

        Flex.section_property = Flex.section_connect_database(Flex.result_designation)
        print(f"Flex.section_property.web_thickness : {Flex.section_property.web_thickness}")
        print(f"Flex.section_property.flange_thickness : {Flex.section_property.flange_thickness}")
        print(f"Flex.section_property.depth : {Flex.section_property.depth}")
        print(f"Flex.section_property.flange_width : {Flex.section_property.flange_width}")
        print(f"Flex.section_property.root_radius : {Flex.section_property.root_radius}")
        print(f"Flex.section_property.toe_radius : {Flex.section_property.toe_radius}")
        print(f"Flex.support : {Flex.support}")
        print(dir(Flex.section_property))
        purlin=create_c_section(length = Flex.length*1000,
        depth = Flex.section_property.depth,
        flange_width = Flex.section_property.flange_width,
        web_thickness = Flex.section_property.web_thickness,
        flange_thickness = Flex.section_property.flange_thickness)

        return purlin

    def createStrutsInTrusses(self):
        Col = self.module_object
        Col.section_property = AngleComponent(designation = Col.result_designation, material_grade = Col.material)
        if Col.sec_profile=="Angles":

            L = float(Col.length)
            A = float(Col.section_property.max_leg)
            B = float(Col.section_property.min_leg)
            T = float(Col.section_property.thickness)
            R1 = float(Col.section_property.root_radius)
            R2 = float(Col.section_property.toe_radius)
            print("Length (L):", L)
            print("Max Leg (A):", A)
            print("Min Leg (B):", B)
            print("Thickness (T):", T)
            print("Root Radius (R1):", R1)
            print("Toe Radius (R2):", R2)

            origin = numpy.array([0.,0.,0.])
            uDir = numpy.array([1.,0.,0.])
            wDir = numpy.array([0.,1.,0.])

            angle = Angle(L, A, B, T, R1, R2)
            _place = angle.place(origin, uDir, wDir)
            point = angle.computeParams()
            prism = angle.create_model()

            return prism
        elif Col.sec_profile=="Back to Back Angles - Same side of gusset":

            L = float(Col.length)
            T = float(Col.section_property.thickness)
            R1 = float(Col.section_property.root_radius)
            R2 = float(Col.section_property.toe_radius)
            spacing = 0.0  # Gap between angles
            print("Length (L):", L)
            print("Thickness (T):", T)
            print("Root Radius (R1):", R1)
            print("Toe Radius (R2):", R2)

            # Example dimensions for gusset plates
            gusset_L = 100  # Length
            gusset_H = 100  # Height
            gusset_T = float(Col.plate_thickness)    # Thickness
            print("Gusset Thickness : ", Col.plate_thickness)
            gusset_degree = 30  # Angle in degrees

            # Create and display the assembly
            origin = numpy.array([0., 0., 0.])
            uDir = numpy.array([1., 0., 0.])
            wDir = numpy.array([0., 0., 1.])
            if Col.loc == "Long Leg":
                B = float(Col.section_property.max_leg)
                A = float(Col.section_property.min_leg)
            elif Col.loc == "Short Leg":
                A = float(Col.section_property.max_leg)
                B = float(Col.section_property.min_leg)
            print("Vertical Leg :", A)
            print("Horizontal Leg :", B)
            assembly = BackToBackAnglesWithGussetsSameSide(L, A, B, T, R1, R2, gusset_L, gusset_H, gusset_T, gusset_degree, spacing)
            assembly.place(origin, uDir, wDir)
            shape = assembly.create_model()

            return shape

        elif Col.sec_profile=="Back to Back Angles - Opposite side of gusset":

            L = float(Col.length)
            T = float(Col.section_property.thickness)
            R1 = float(Col.section_property.root_radius)
            R2 = float(Col.section_property.toe_radius)
            spacing = float(Col.plate_thickness)   # Gap between angles
            print("Length (L):", L)
            print("Thickness (T):", T)
            print("Root Radius (R1):", R1)
            print("Toe Radius (R2):", R2)


            # Example dimensions for gusset plates
            gusset_L = 100  # Length
            gusset_H = 100 # Height
            gusset_T =  float(Col.plate_thickness)   # Thickness
            print("Gusset Thickness : ", Col.plate_thickness)
            gusset_degree = 30  # Angle in degrees

            # Create and display the assembly
            origin = numpy.array([0., 0., 0.])
            uDir = numpy.array([1., 0., 0.])
            wDir = numpy.array([0., 0., 1.])
            if Col.loc == "Long Leg":
                A = float(Col.section_property.max_leg)
                B = float(Col.section_property.min_leg)
            elif Col.loc == "Short Leg":
                B = float(Col.section_property.max_leg)
                A = float(Col.section_property.min_leg)
            print("Vertical Leg :", A)
            print("Horizontal Leg :", B)
            assembly = BackToBackAnglesWithGussetsOppSide(L, A, B, T, R1, R2, gusset_L, gusset_H, gusset_T, gusset_degree, spacing)
            assembly.place(origin, uDir, wDir)
            shape = assembly.create_model()
            return shape

    def createStrutBoltedCAD(self):
        """
        :return: The calculated values/parameters to create 3D CAD model of individual components for Strut Bolted to End Gusset.
        """
        print("DEBUG: Entered createStrutBoltedCAD")
        Col = self.module_object

        # Types of connections =  #'Angles', 'Back to Back Angles', 'Star Angles', 'Channels', 'Back to Back Channels'
        
        # Extract Bolt Parameters
        bolt_d = float(Col.bolt.bolt_diameter_provided)  # Bolt diameter (shank part)
        bolt_r = bolt_d / 2  # Bolt radius (Shank part)
        bolt_T = self.boltHeadThick_Calculation(bolt_d)  # Bolt head thickness
        bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
        bolt_Ht = self.boltLength_Calculation(bolt_d)  # Bolt head height

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component directory
        nut_T = self.nutThick_Calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
        nut_Ht = nut_T
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)  # Call to create Nut from Component directory

        # Extract Plate Parameters
        # Assuming Col.plate has these attributes populated after design
        plate_L = float(Col.plate.length) + 50 if hasattr(Col, 'plate') and hasattr(Col.plate, 'length') else 300
        plate_H = float(Col.plate.height) if hasattr(Col, 'plate') and hasattr(Col.plate, 'height') else 300
        plate_T = float(Col.plate.thickness_provided) if hasattr(Col, 'plate') and hasattr(Col.plate, 'thickness_provided') else 10
        
        plate = GassetPlate(L=plate_L, H=plate_H, T=plate_T, degree=30)
        
        # Intermittent Connection Plates (if applicable)
        inter_plate_L = float(Col.inter_plate_length) if hasattr(Col, 'inter_plate_length') else 100
        inter_plate_H = float(Col.inter_plate_height) if hasattr(Col, 'inter_plate_height') else 100
        intermittentPlates = Plate(L=inter_plate_H, W=inter_plate_L, T=plate.T)


        if Col.sec_profile == 'Channels' or Col.sec_profile == 'Back to Back Channels':
            member = Channel(B=float(Col.section_size_1.flange_width), T=float(Col.section_size_1.flange_thickness),
                             D=float(Col.section_size_1.depth), t=float(Col.section_size_1.web_thickness),
                             R1=float(Col.section_size_1.root_radius), R2=float(Col.section_size_1.toe_radius),
                             L=float(Col.length))
            if Col.sec_profile == 'Channels':
                nut_space = member.t + plate.T + nut.T  # member.T + plate.T + nut.T

            else:
                nut_space = 2 * member.t + plate.T + nut.T  # 2*member.T + plate.T + nut.T

            intermittentConnection = IntermittentNutBoltPlateArray(Col, nut, bolt, intermittentPlates, nut_space)
            nut_bolt_array = TNutBoltArray(Col, nut, bolt, nut_space)
            strutCAD = StrutChannelBoltCAD(Col, member, plate, nut_bolt_array, intermittentConnection)

        else: # Angles
            member = Angle(L=float(Col.length), A=float(Col.section_size_1.max_leg), B=float(Col.section_size_1.min_leg),
                           T=float(Col.section_size_1.thickness), R1=float(Col.section_size_1.root_radius),
                           R2=float(Col.section_size_1.toe_radius))
            if Col.sec_profile == 'Back to Back Angles':
                nut_space = 2 * member.T + plate.T + nut.T
            else:
                nut_space = member.T + plate.T + nut.T

            print(f"DEBUG: Creating IntermittentNutBoltPlateArray with nut_space={nut_space}")
            intermittentConnection = IntermittentNutBoltPlateArray(Col, nut, bolt, intermittentPlates, nut_space)
            print("DEBUG: Creating TNutBoltArray")
            nut_bolt_array = TNutBoltArray(Col, nut, bolt, nut_space)
            print(f"DEBUG: Creating StrutAngleBoltCAD with parameters: {Col.sec_profile}, {member}, {plate}")
            strutCAD = StrutAngleBoltCAD(Col, member, plate, nut_bolt_array, intermittentConnection)

        print("DEBUG: Calling create_3DModel on strutCAD")
        strutCAD.create_3DModel()
        print("DEBUG: createStrutBoltedCAD completed successfully")

        return strutCAD

    def createStrutWeldedCAD(self):
        T = self.module_object

        plate = GassetPlate(L=float(T.plate.length + 50), H=float(T.plate.height),
                            T=float(T.plate.thickness_provided), degree=30)

        intermittentPlates = Plate(L=float(getattr(T, 'inter_plate_height', 0.0)), W=float(getattr(T, 'inter_plate_length', 0.0)), T=plate.T)
        intermittentWelds = FilletWeld(h=float(getattr(T, 'inter_weld_size', 0.0)), b=float(getattr(T, 'inter_weld_size', 0.0)), L=intermittentPlates.W)
        if not hasattr(T, 'inter_memb_length'):
            T.inter_memb_length = 0.0
        if not hasattr(T, 'inter_conn'):
            T.inter_conn = "0" 
        # Alias section_size_1 -> section_property for compatibility with IntermittentWelds
        if not hasattr(T, 'section_size_1') and hasattr(T, 'section_property'):
            T.section_size_1 = T.section_property
        # Inject 'depth' attribute for Angle sections to avoid AttributeError in IntermittentWelds
        if hasattr(T, 'section_size_1') and not hasattr(T.section_size_1, 'depth'):
            if hasattr(T.section_size_1, 'max_leg'):
                T.section_size_1.depth = T.section_size_1.max_leg
        weld_plate_array = IntermittentWelds(T, intermittentWelds, intermittentPlates)

        s = max(15, float(T.weld.size))
        plate_intercept = plate.L - s - 50
        print(f"DEBUG createStrutWeldedCAD: sec_profile = '{T.sec_profile}', section_property type = {type(T.section_property).__name__}")
        if T.sec_profile == 'Channels' or T.sec_profile == 'Back to Back Channels':
            member = Channel(B=float(T.section_property.flange_width), T=float(T.section_property.flange_thickness),
                             D=float(T.section_property.depth), t=float(T.section_property.web_thickness),
                             R1=float(T.section_property.root_radius), R2=float(T.section_property.toe_radius),
                             L=float(T.length))
            inline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(plate_intercept))
            opline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(member.D))


            strutCAD = StrutChannelWeldCAD(T, member, plate, inline_weld, opline_weld, weld_plate_array)

        else:
            member = Angle(L=float(T.length), A=float(T.section_property.max_leg), B=float(T.section_property.min_leg),
                           T=float(T.section_property.thickness), R1=float(T.section_property.root_radius),
                           R2=float(T.section_property.toe_radius))
            inline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(plate_intercept))
            if T.loc == 'Long Leg':
                opline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(member.A))
            else:  # 'Short Leg'
                opline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(member.B))

            # weld_plate_array = IntermittentWelds(T, intermittentWelds, intermittentPlates)
            strutCAD = StrutAngleWeldCAD(T, member, plate, inline_weld, opline_weld, weld_plate_array)

        strutCAD.create_3DModel()

        return strutCAD

    def display_3DModel(self, component, bgcolor):
        
        # Component colors
        weld_color = Quantity_NOC_SADDLEBROWN
        plate_color = Quantity_Color(47/255.0, 47/255.0, 35/255.0, Quantity_TOC_RGB)
        column_color = Quantity_Color(72/255.0, 72/255.0, 54/255.0, Quantity_TOC_RGB)
        beam_color = Quantity_Color(134/255.0, 134/255.0, 100/255.0, Quantity_TOC_RGB)
        bolt_color = Quantity_Color(255/255.0, 0/255.0, 0/255.0, Quantity_TOC_RGB)
        packing_plate_color = Quantity_NOC_GRAY

        self.component = component

        # Use CleanupCoordinator for centralized cleanup
        from osdag_gui.OS_safety_protocols import get_cleanup_coordinator
        coordinator = get_cleanup_coordinator()
        coordinator.cleanup_for_new_design(self.cad_widget, self.display)

        try:
            self.display.View_Iso()
        except Exception as e:
            print(f"[WARNING] Error setting iso view: {e}")

        try:
            self.display.FitAll()
        except Exception as e:
            print(f"[WARNING] Error fitting all: {e}")

        try:
            self.display.DisableAntiAliasing()
        except Exception as e:
            print(f"[WARNING] Error disabling anti-aliasing: {e}")

        if bgcolor == "gradient_light":
            self.display.set_bg_gradient_color([255, 255, 255], [126, 126, 126])
        else:
            self.display.set_bg_gradient_color([83, 83, 83], [0, 0, 0])

        if self.mainmodule  == "Shear Connection":
            # hover labels
            hover_dict = self.module_object.hover_dict
            self.cad_widget.model_hover_labels = hover_dict.copy()

            A = self.module_object

            self.loc = A.connectivity

            if self.loc == "Column Flange-Beam Web" and self.connection == KEY_DISP_FINPLATE:
                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
            elif self.loc == "Column Flange-Beam Web" and self.connection == KEY_DISP_SEATED_ANGLE:
                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
            elif self.loc == "Column Flange-Beam Web" and self.connection == KEY_DISP_SEATED_ANGLE:
                self.display.View.SetProj(OCC.Core.V3d.V3d_XposYnegZpos)

            if self.component == "Column":
                # hover label
                label = ["Column", hover_dict.get("Column")]
                osdag_display_shape(self.display, self.connectivityObj.get_columnModel(), color=column_color, update=True, label=label, canvas=self.cad_widget)
            elif self.component == "Beam":
                label = ["Beam", hover_dict.get("Beam")]
                osdag_display_shape(self.display, self.connectivityObj.get_beamModel(), color=beam_color, update=True, label=label, canvas=self.cad_widget)
            elif self.component == "cleatAngle":
                label = ["Angle", hover_dict.get("Angle")]
                osdag_display_shape(self.display, self.connectivityObj.angleModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                osdag_display_shape(self.display, self.connectivityObj.angleLeftModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    label = ["Bolt", hover_dict.get("Bolt")]
                    osdag_display_shape(self.display, nutbolt, color=bolt_color, update=True, label=label, canvas=self.cad_widget)

            elif self.component == "SeatAngle":
                label = ["Angle", hover_dict.get("Angle")]
                osdag_display_shape(self.display, self.connectivityObj.topclipangleModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                osdag_display_shape(self.display, self.connectivityObj.angleModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    label = ["Bolt", hover_dict.get("Bolt")]
                    osdag_display_shape(self.display, nutbolt, color=bolt_color, update=True, label=label, canvas=self.cad_widget)

            elif self.component == "Plate":
                # hover label
                label = ["Weld", hover_dict.get("Weld")]
                osdag_display_shape(self.display, self.connectivityObj.weldModelLeft, color=weld_color, update=True, label=label, canvas=self.cad_widget)
                osdag_display_shape(self.display, self.connectivityObj.weldModelRight, color=weld_color, update=True, label=label, canvas=self.cad_widget)
                label = ["Plate", hover_dict.get("Plate")]
                osdag_display_shape(self.display, self.connectivityObj.plateModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    label = ["Bolt", hover_dict.get("Bolt")]
                    osdag_display_shape(self.display, nutbolt, color=bolt_color, update=True, label=label, canvas=self.cad_widget)

            elif self.component == "Model":
                # hover label
                label = ["Column", hover_dict.get("Column")]
                osdag_display_shape(self.display, self.connectivityObj.columnModel, color=column_color, update=True, label=label, canvas=self.cad_widget)
                label = ["Beam", hover_dict.get("Beam")]
                osdag_display_shape(self.display, self.connectivityObj.beamModel, color=beam_color, update=True, label=label, canvas=self.cad_widget)
                if self.connection == KEY_DISP_FINPLATE or self.connection == KEY_DISP_ENDPLATE:
                    # Colors to be set on self.components
                    label = ["Weld", hover_dict.get("Weld")]
                    osdag_display_shape(self.display, self.connectivityObj.weldModelLeft, color=weld_color, update=True, label=label, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.connectivityObj.weldModelRight, color=weld_color, update=True, label=label, canvas=self.cad_widget)
                    label = ["Plate", hover_dict.get("Plate")]
                    osdag_display_shape(self.display, self.connectivityObj.plateModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)

                elif self.connection == KEY_DISP_CLEATANGLE:
                    label = ["Angle", hover_dict.get("Angle")]
                    osdag_display_shape(self.display, self.connectivityObj.angleModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.connectivityObj.angleLeftModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                else:
                    label = ["Angle", hover_dict.get("Angle")]
                    osdag_display_shape(self.display, self.connectivityObj.topclipangleModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.connectivityObj.angleModel, color=plate_color, update=True, label=label, canvas=self.cad_widget)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    label = ["Bolt", hover_dict.get("Bolt")]
                    osdag_display_shape(self.display, nutbolt, color=bolt_color, update=True, label=label, canvas=self.cad_widget)

        if self.mainmodule == "Moment Connection":
            if self.connection == KEY_DISP_BEAMCOVERPLATE:

                self.B = self.module_object

                # self.CPObj = self.createBBCoverPlateCAD()
                # NOTE: Reuse self.CPObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)
                
                hover_dict = self.B.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()
                    
                label_beam   = ["Beam",   hover_dict.get("Beam")]
                label_plate  = ["Plate",  hover_dict.get("Plate")]
                label_bolt   = ["Bolt",   hover_dict.get("Bolt")]
            
                if self.component == "Beam":
                    # Displays both beams
                    osdag_display_shape(self.display, self.CPObj.get_only_beams_Models(), update=True,color=beam_color,label=label_beam,canvas=self.cad_widget )

                elif self.component == "Connector":
                    osdag_display_shape( self.display, self.CPObj.get_flangewebplatesModel(), update=True, color=plate_color,label=label_plate,canvas=self.cad_widget)
                    if self.B.preference != 'Outside':
                        osdag_display_shape(self.display, self.CPObj.get_innetplatesModels(), update=True,color=plate_color, label=label_plate,canvas=self.cad_widget)

                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_arrayModels(), update=True,color=Quantity_NOC_SADDLEBROWN,label=label_bolt,canvas=self.cad_widget)

                elif self.component == "Model":    
                    
                    osdag_display_shape( self.display, self.CPObj.get_beamsModel(), update=True, color=beam_color,label=label_beam,canvas=self.cad_widget )
                    osdag_display_shape( self.display, self.CPObj.get_flangewebplatesModel(), update=True, color=plate_color, label=label_plate,canvas=self.cad_widget)

                    # Todo: remove velove commented lines

                    if self.B.preference != 'Outside':
                        osdag_display_shape( self.display, self.CPObj.get_innetplatesModels(), update=True, color=plate_color,label=label_plate,canvas=self.cad_widget)

                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_arrayModels(), update=True,color=Quantity_NOC_SADDLEBROWN,label=label_bolt,canvas=self.cad_widget)
                    
            elif self.connection == KEY_DISP_BB_EP_SPLICE:
                self.B = self.module_object  

                # self.ExtObj = self.createBBEndPlateCAD()
                # NOTE: Reuse self.CPObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)
                # Do NOT call createBBEndPlateCAD() again here

                hover_dict = self.B.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()
                    
                label_beam      = ["Beam", hover_dict.get("Beam")]
                label_plate     = ["Plate", hover_dict.get("Plate")]
                label_weld      = ["Weld", hover_dict.get("Weld")]
                label_bolt      = ["Bolt", hover_dict.get("Bolt")]

                if self.component == "Beam":
                    # NOTE: Do NOT call gc.collect() during CAD operations - it causes heap corruption
                    osdag_display_shape(self.display, self.CPObj.get_beam_models(), update=True,
                                        color=beam_color, label=label_beam, canvas=self.cad_widget)

                elif self.component == "Connector":
                    # NOTE: Do NOT call gc.collect() during CAD operations - it causes heap corruption
                    osdag_display_shape(self.display, self.CPObj.get_plate_connector_models(), update=True,
                                        color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_welded_models(), update=True,
                                        color=weld_color, label=label_weld, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_array_models(), update=True,
                                        color=bolt_color, label=label_bolt, canvas=self.cad_widget)


                elif self.component == "Model":
                    # NOTE: Do NOT call gc.collect() during CAD operations - it causes heap corruption
                    osdag_display_shape(self.display, self.CPObj.get_beam_models(), update=True,
                                        color=beam_color, label=label_beam, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_plate_connector_models(), update=True,
                                        color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_welded_models(), update=True,
                                        color=weld_color, label=label_weld, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_array_models(), update=True,
                                        color=bolt_color, label=label_bolt, canvas=self.cad_widget)

            elif self.connection == KEY_DISP_BEAMCOVERPLATEWELD:
                self.B = self.module_object

                # self.CPObj = self.createBBCoverPlateCAD()
                # NOTE: Reuse self.CPObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)
                beams = self.CPObj.get_beam_models()
                plates = self.CPObj.get_plate_models()
                welds = self.CPObj.get_welded_modules()

                hover_dict = self.module_object.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()
                    
                label_beam   = ["Beam", hover_dict.get("Beam")]
                label_plate  = ["Plate", hover_dict.get("Plate")]
                label_welds   = ["Weld", hover_dict.get("Weld")]
               
                if self.component == "Beam":
                    # Displays both beams
                    osdag_display_shape(self.display, beams, update=True, color=beam_color, label=label_beam, canvas=self.cad_widget)
                elif self.component == "Connector":
                    osdag_display_shape(self.display, plates, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, welds, update=True, color=Quantity_NOC_SADDLEBROWN, label=label_welds, canvas=self.cad_widget)
                elif self.component == "Model":
                    osdag_display_shape(self.display, beams, update=True, color=beam_color, label=label_beam, canvas=self.cad_widget)
                    osdag_display_shape(self.display, plates, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, welds, update=True, color=Quantity_NOC_SADDLEBROWN, label=label_welds, canvas=self.cad_widget)

            elif self.connection == KEY_DISP_COLUMNCOVERPLATE:
                self.C = self.module_object  

                # self.CPObj = self.createCCCoverPlateCAD()
                # NOTE: Reuse self.CPObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)
                columns = self.CPObj.get_column_models()
                plates = self.CPObj.get_plate_models()
                nutbolt = self.CPObj.get_nut_bolt_models()
                onlycolumn = self.CPObj.get_only_column_models()
                
                hover_dict = self.module_object.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()

                label_column = ["Column", hover_dict.get("Column")]
                label_plate  = ["Plate",  hover_dict.get("Plate")]
                label_bolt   = ["Bolt",   hover_dict.get("Bolt")]

                if self.component == "Column":
                    # Displays both beams
                    osdag_display_shape(self.display, onlycolumn, update=True, color=column_color, label=label_column, canvas=self.cad_widget)
                elif self.component == "Cover Plate":
                    osdag_display_shape(self.display, plates, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, nutbolt, update=True, color=Quantity_NOC_SADDLEBROWN, label=label_bolt, canvas=self.cad_widget)
                elif self.component == "Model":
                    osdag_display_shape(self.display, columns, update=True, color=column_color,label=label_column,canvas=self.cad_widget)
                    osdag_display_shape(self.display, plates, update=True,color=plate_color,label=label_plate,canvas=self.cad_widget)
                    osdag_display_shape(self.display, nutbolt, update=True, color=Quantity_NOC_SADDLEBROWN,label=label_bolt, canvas=self.cad_widget)


            elif self.connection == KEY_DISP_BCENDPLATE:
                self.Bc = self.module_object

                hover_dict = self.module_object.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()

                label_column = ["Column", hover_dict.get("Column")]
                label_beam = ["Beam", hover_dict.get("Beam")]
                label_plate = ["Plate", hover_dict.get("Plate")]
                label_weld = ["Weld", hover_dict.get("Weld")]
                label_bolt = ["Bolt", hover_dict.get("Bolt")]

                # self.ExtObj = self.createBCEndPlateCAD()
                # NOTE: Reuse self.CPObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)
                # Do NOT call createBCEndPlateCAD() again here

                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
                c_length = self.column_length
                # Point1 = gp_Pnt(0.0, 0.0, c_length)
                # DisplayMsg(self.display, Point1, self.Bc.supporting_section.designation)
                b_length = self.beam_length + self.Bc.supporting_section.depth/2+100
                # Point2 = gp_Pnt(0.0,-b_length, c_length/2)
                # DisplayMsg(self.display, Point2, self.Bc.supported_section.designation)
                # Displays the beams #TODO ANAND
                if self.component == "Column":
                    self.display.View_Iso()
                    osdag_display_shape(self.display, self.CPObj.columnModel, update=True, color=column_color, label=label_column, canvas=self.cad_widget)

                    # Point1 = gp_Pnt(-self.Bc.supporting_section.flange_width/2, 0, c_length)
                    # DisplayMsg(self.display, Point1, self.Bc.supporting_section.designation)
                    # Point = gp_Pnt(0.0, 0.0, 10)
                    # DisplayMsg(self.display,Point)

                elif self.component == "Beam":
                    self.display.View_Iso()
                    osdag_display_shape(self.display, self.CPObj.beamModel, update=True, color=beam_color,
                        label=label_beam, canvas=self.cad_widget)
                    # Point2 = gp_Pnt(0.0, -b_length, c_length / 2)
                    # DisplayMsg(self.display, Point2, self.Bc.supported_section.designation)
                    # , color = 'Dark Gray'

                elif self.component == "Connector":
                    osdag_display_shape(self.display, self.CPObj.get_plate_connector_models(), update=True,
                        color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_welded_models(), update=True,
                        color=weld_color, label=label_weld, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_array_models(), update=True,
                        color=bolt_color, label=label_bolt, canvas=self.cad_widget)


                elif self.component == "Model":
                    osdag_display_shape(self.display, self.CPObj.get_column_models(), update=True,
                        color=column_color, label=label_column, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_beam_models(), update=True,
                        color=beam_color, label=label_beam, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_plate_connector_models(), update=True,
                        color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_welded_models(), update=True,
                        color=weld_color, label=label_weld, canvas=self.cad_widget)
                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_array_models(), update=True,
                        color=bolt_color, label=label_bolt, canvas=self.cad_widget)
                    # Point1 = gp_Pnt(self.Bc.supporting_section.flange_width/2, -self.Bc.supporting_section.depth/2, c_length*0.75)
                    # DisplayMsg(self.display, Point1, self.Bc.supporting_section.designation)
                    # Point2 = gp_Pnt(self.Bc.supporting_section.flange_width/2, -b_length, c_length / 2)
                    # DisplayMsg(self.display, Point2, self.Bc.supported_section.designation)
                    # Erase(DisplayMsg(self.display, Point2, self.Bc.supported_section.designation))


            elif self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:
                self.C = self.module_object

                # self.CPObj = self.createCCCoverPlateCAD()
                # NOTE: Reuse self.CPObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)
                columns = self.CPObj.get_column_models()
                plates = self.CPObj.get_plate_models()
                welds = self.CPObj.get_welded_modules()
                
                hover_dict = self.C.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()
                    
                label_column = ["Column", hover_dict.get("Column")]
                label_plate  = ["Plate",  hover_dict.get("Plate")]
                label_weld   = ["Weld",   hover_dict.get("Weld")]
              

                if self.component == "Column":
                    # Displays both beams
                    osdag_display_shape(self.display, columns, update=True,color=column_color, label=label_column,canvas=self.cad_widget)
                elif self.component == "Cover Plate":
                    osdag_display_shape(self.display, plates, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, welds, update=True, color=weld_color, label=label_weld,canvas=self.cad_widget)
                elif self.component == "Model":
                    osdag_display_shape(self.display, columns, update=True,color=column_color, label=label_column, canvas=self.cad_widget)
                    osdag_display_shape(self.display, plates, update=True, color=plate_color, label=label_plate,canvas=self.cad_widget)
                    osdag_display_shape(self.display, welds, update=True, color=weld_color, label=label_weld, canvas=self.cad_widget)

            elif self.connection == KEY_DISP_COLUMNENDPLATE:
                self.CEP = self.module_object  

                # self.CEPObj = self.createCCEndPlateCAD()
                # NOTE: Reuse self.CEPObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)
                columns = self.CEPObj.get_column_models()
                plates = self.CEPObj.get_plate_models()
                welds = self.CEPObj.get_weld_models()
                nutBolts = self.CEPObj.get_nut_bolt_models()
                
                hover_dict = self.module_object.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()
                    
                label_column = ["Column", hover_dict.get("Column")]
                label_plate  = ["Plate",  hover_dict.get("Plate")]
                label_weld   = ["Weld",   hover_dict.get("Weld")]
                label_bolt   = ["Bolt",   hover_dict.get("Bolt")]

                if self.component == "Column":
                    osdag_display_shape(self.display, columns, update=True, color=column_color, label=label_column,canvas=self.cad_widget)

                elif self.component == "Connector":
                    osdag_display_shape(self.display, plates, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, welds, update=True,color=weld_color, label=label_weld,canvas=self.cad_widget)
                    osdag_display_shape(self.display, nutBolts, update=True, color=Quantity_NOC_SADDLEBROWN, label=label_bolt, canvas=self.cad_widget)

                elif self.component == "Model":
                    osdag_display_shape(self.display, columns, update=True,color=column_color, label=label_column, canvas=self.cad_widget)
                    osdag_display_shape(self.display, plates, update=True, color=plate_color, label=label_plate,  canvas=self.cad_widget)
                    osdag_display_shape(self.display, welds, update=True,   color=weld_color, label=label_weld, canvas=self.cad_widget)
                    osdag_display_shape(self.display, nutBolts, update=True,  color=Quantity_NOC_SADDLEBROWN, label=label_bolt, canvas=self.cad_widget)

            elif self.connection == KEY_DISP_BASE_PLATE:
                self.Bp = self.module_object  

                # self.BPObj = self.createBasePlateCAD()
                # NOTE: Reuse self.BPObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)

                column = self.BPObj.get_column_model()
                plate = self.BPObj.get_plate_connector_models()
                weld = self.BPObj.get_welded_models()
                nut_bolt = self.BPObj.get_nut_bolt_array_models()
                conc = self.BPObj.get_concrete_models()
                grout = self.BPObj.get_grout_models()

                hover_dict = self.Bp.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()

                label_column = ["Column", hover_dict.get("Column")]
                label_plate = ["Plate", hover_dict.get("Plate")]
                label_weld = ["Weld", hover_dict.get("Weld")]
                label_bolt = ["Bolt", hover_dict.get("Bolt")]
                label_conc = ["Conc", hover_dict.get("Conc")]
                label_grout = ["Grout", hover_dict.get("Grout")]

                if self.component == "Model":  # Todo: change this into key
                    osdag_display_shape(self.display, column, update=True, color=column_color, label=label_column, canvas=self.cad_widget)
                    osdag_display_shape(self.display, plate, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, weld, update=True, color=weld_color, label=label_weld, canvas=self.cad_widget)
                    osdag_display_shape(self.display, nut_bolt, update=True, color=bolt_color, label=label_bolt, canvas=self.cad_widget)
                    osdag_display_shape(self.display, conc, transparency=0.5, color=GRAY, update=True , label=label_conc, canvas=self.cad_widget)
                    osdag_display_shape(self.display, grout, transparency=0.5, color=GRAY, update=True , label=label_grout, canvas=self.cad_widget)

                elif self.component == "Column":
                    osdag_display_shape(self.display, column, update=True, color=column_color, label=label_column,canvas=self.cad_widget)

                elif self.component == "Connector":
                    osdag_display_shape(self.display, plate, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, weld, color=weld_color, label=label_weld,canvas=self.cad_widget)
                    osdag_display_shape(self.display, nut_bolt, update=True, color=Quantity_NOC_SADDLEBROWN, label=label_bolt, canvas=self.cad_widget)

        elif self.mainmodule == 'Columns with known support conditions':
            self.col = self.module_object  
            self.ColObj = self.createColumnInFrameCAD()
            
            hover_dict = self.module_object.hover_dict
            self.cad_widget.model_hover_labels = hover_dict.copy()
                    
            label_column = ["Column", hover_dict.get("Column")]
                    
            if self.component == "Model":
                osdag_display_shape(self.display, self.ColObj, update=True, color=column_color, label=label_column,canvas=self.cad_widget)

        elif self.mainmodule == KEY_DISP_LAPJOINTBOLTED:
            self.ColObj = self.createBoltedLapJoint()
            self.col = self.module_object 

            # Hover dict
            hover_dict = self.module_object.hover_dict
            self.cad_widget.model_hover_labels = hover_dict.copy()

            if isinstance(self.ColObj, (tuple, list)):
                _, plate1, plate2, _, _ = self.ColObj
            else:
                plate1 = self.ColObj.plate1
                plate2 = self.ColObj.plate2         
                bolt = self.ColObj.bolt         
                nut = self.ColObj.nut        

            # lap_joint, plate1, plate2, bolts, nuts
            label_plate1 = ["Plate 1", hover_dict.get("Plate 1")]
            label_plate2 = ["Plate 2", hover_dict.get("Plate 2")]
            label_bolt = ["Bolt", hover_dict.get("Bolt")]

            self.assembly,self.plate1_model,self.plate2_model,self.bolt_models,self.nuts_models = self.createBoltedLapJoint()

            if self.component == "Model":
                osdag_display_shape(self.display, plate1, update=True, color=column_color, label=label_plate1, canvas=self.cad_widget)
                osdag_display_shape(self.display, plate2, update=True, color=beam_color, label=label_plate2, canvas=self.cad_widget)
                for bolt in self.bolt_models:
                    osdag_display_shape(self.display, bolt, update=True,
                                            color=bolt_color, label=label_bolt, canvas=self.cad_widget)
                for nut in self.nuts_models:
                    osdag_display_shape(self.display, nut, update=True,
                                            color=bolt_color, label=label_bolt, canvas=self.cad_widget)

            elif self.component == "Plate 1":
                osdag_display_shape(self.display, plate1, update=True, color=column_color, label=label_plate1, canvas=self.cad_widget)
            elif self.component == "Plate 2":
                osdag_display_shape(self.display, plate2, update=True, color=beam_color, label=label_plate2, canvas=self.cad_widget)
            elif self.component == "Bolts":
                for bolt in self.bolt_models:
                    osdag_display_shape(self.display, bolt, update=True, color=bolt_color, label=label_bolt, canvas=self.cad_widget)
                for nut in self.nuts_models:
                    osdag_display_shape(self.display, nut, update=True, color=bolt_color, label=label_bolt, canvas=self.cad_widget)

        elif self.mainmodule == KEY_DISP_LAPJOINTWELDED:
            self.col = self.module_object
                            
            self.assembly, self.plate1_model, self.plate2_model, self.weld_models = self.createWeldedLapJoint()
            
            hover_dict = self.module_object.hover_dict
            self.cad_widget.model_hover_labels = hover_dict.copy()

            label_plate1 = ["Plate 1", hover_dict.get("Plate 1")]
            label_plate2 = ["Plate 2", hover_dict.get("Plate 2")]
            label_weld = ["Weld", hover_dict.get("Weld")]

            # Use direct DisplayShape
            if self.component == "Model":
                osdag_display_shape(self.display, self.plate1_model, update=True, color=column_color, label=label_plate1, canvas=self.cad_widget)
                osdag_display_shape(self.display, self.plate2_model, update=True, color=beam_color, label=label_plate2, canvas=self.cad_widget)
                for weld in self.weld_models:
                    osdag_display_shape(self.display, weld, update=True, color=weld_color, label=label_weld, canvas=self.cad_widget)

            elif self.component == "Plate 1":
                osdag_display_shape(self.display, self.plate1_model, update=True, color=column_color, label=label_plate1, canvas=self.cad_widget)

            elif self.component == "Plate 2":
                osdag_display_shape(self.display, self.plate2_model, update=True, color=beam_color, label=label_plate2, canvas=self.cad_widget)

            elif self.component == "Welds":
                for weld in self.weld_models:
                    osdag_display_shape(self.display, weld, update=True, color=weld_color, label=label_weld, canvas=self.cad_widget)

        elif self.mainmodule == KEY_DISP_BUTTJOINTBOLTED:
            self.col = self.module_object
            
            # Reuse ColObj if already created by call_3DModel, otherwise create it
            if hasattr(self, 'ColObj') and self.ColObj is not None:
                # ColObj is a tuple from createButtJointBoltedCAD()
                self.assembly, self.plate1_model, self.plate2_model, self.platec_model, self.platec2_model, self.bolt_models, self.nuts_models, self.packing1_model, self.packing2_model = self.ColObj
            else:
                self.assembly, self.plate1_model, self.plate2_model, self.platec_model, self.platec2_model, self.bolt_models, self.nuts_models, self.packing1_model, self.packing2_model = self.createButtJointBoltedCAD()

            hover_dict = self.module_object.hover_dict
            self.cad_widget.model_hover_labels = hover_dict.copy()

            # Use the unpacked models directly
            label_plate1 = ["Plate 1", hover_dict.get("Plate 1")]
            label_plate2 = ["Plate 2", hover_dict.get("Plate 2")]
            label_platec = ["Cover Plate", hover_dict.get("Cover Plate")]
            label_packing = ["Packing Plate", hover_dict.get("Packing Plate")]
            label_bolt = ["Bolt", hover_dict.get("Bolt")]
            
            if self.component == "Model":
                osdag_display_shape(self.display, self.plate1_model, update=True, color=column_color, label=label_plate1, canvas=self.cad_widget)
                osdag_display_shape(self.display, self.plate2_model, update=True, color=beam_color, label=label_plate2, canvas=self.cad_widget)
                osdag_display_shape(self.display, self.platec_model, update=True, color=plate_color, label=label_platec, canvas=self.cad_widget)
                if self.platec2_model:
                    osdag_display_shape(self.display, self.platec2_model, update=True, color=plate_color, label=label_platec, canvas=self.cad_widget)
                # Display packing plates if they exist
                if self.packing1_model is not None:
                    osdag_display_shape(self.display, self.packing1_model, update=True, color=packing_plate_color, label=label_packing, canvas=self.cad_widget)
                if self.packing2_model is not None:
                    osdag_display_shape(self.display, self.packing2_model, update=True, color=packing_plate_color, label=label_packing, canvas=self.cad_widget)
                for bolt in self.bolt_models:
                    osdag_display_shape(self.display, bolt, update=True,
                                            color=bolt_color, label=label_bolt, canvas=self.cad_widget)
                for nut in self.nuts_models:
                    osdag_display_shape(self.display, nut, update=True,
                                            color=bolt_color, label=label_bolt, canvas=self.cad_widget)
            
            # Handling for individual components
            elif self.component == "Plate 1":
                osdag_display_shape(self.display, self.plate1_model, update=True, color=column_color, label=label_plate1, canvas=self.cad_widget)
            elif self.component == "Plate 2":
                osdag_display_shape(self.display, self.plate2_model, update=True, color=beam_color, label=label_plate2, canvas=self.cad_widget)
            elif self.component == "Cover Plate":
                osdag_display_shape(self.display, self.platec_model, update=True, color=plate_color, label=label_platec, canvas=self.cad_widget)
                if self.platec2_model:
                    osdag_display_shape(self.display, self.platec2_model, update=True, color=plate_color, label=label_platec, canvas=self.cad_widget)
                # Also show packing plates with cover plates
                if self.packing1_model is not None:
                    osdag_display_shape(self.display, self.packing1_model, update=True, color=packing_plate_color, label=label_packing, canvas=self.cad_widget)
                if self.packing2_model is not None:
                    osdag_display_shape(self.display, self.packing2_model, update=True, color=packing_plate_color, label=label_packing, canvas=self.cad_widget)
            elif self.component == "Bolts":
                for bolt in self.bolt_models:
                    osdag_display_shape(self.display, bolt, update=True, color=bolt_color, label=label_bolt, canvas=self.cad_widget)
                for nut in self.nuts_models:
                    osdag_display_shape(self.display, nut, update=True, color=bolt_color, label=label_bolt, canvas=self.cad_widget)

        elif self.mainmodule == KEY_DISP_BUTTJOINTWELDED:
            # Create the CAD objects
            self.assembly, self.plate1_model, self.plate2_model, self.platec_model, self.platec2_model, self.weld_models, self.packing1_model, self.packing2_model = self.createButtJointWeldedCAD()
            self.col = self.module_object

            # Hover dict
            hover_dict = self.module_object.hover_dict
            self.cad_widget.model_hover_labels = hover_dict.copy()
            
            label_plate1 = ["Plate 1", hover_dict.get("Plate 1")]
            label_plate2 = ["Plate 2", hover_dict.get("Plate 2")]
            label_platec = ["Cover Plate", hover_dict.get("Cover Plate")] # Top Cover
            label_platec2 = ["Cover Plate", hover_dict.get("Cover Plate")] # Bottom Cover
            label_packing = ["Packing Plate", hover_dict.get("Packing Plate")]
            label_weld = ["Weld", hover_dict.get("Weld")]

            if self.component == "Model":
                osdag_display_shape(self.display, self.plate1_model, update=True, color=column_color, label=label_plate1, canvas=self.cad_widget)
                osdag_display_shape(self.display, self.plate2_model, update=True, color=beam_color, label=label_plate2, canvas=self.cad_widget)
                osdag_display_shape(self.display, self.platec_model, update=True, color=plate_color, label=label_platec, canvas=self.cad_widget)
                if self.platec2_model:
                    osdag_display_shape(self.display, self.platec2_model, update=True, color=plate_color, label=label_platec2, canvas=self.cad_widget)
                # Display packing plates if they exist
                if self.packing1_model is not None:
                    osdag_display_shape(self.display, self.packing1_model, update=True, color=packing_plate_color, label=label_packing, canvas=self.cad_widget)
                if self.packing2_model is not None:
                    osdag_display_shape(self.display, self.packing2_model, update=True, color=packing_plate_color, label=label_packing, canvas=self.cad_widget)
                for weld in self.weld_models:
                    osdag_display_shape(self.display, weld, update=True, color=weld_color, label=label_weld, canvas=self.cad_widget)
            
            # Handling for individual components if selected in UI
            elif self.component == "Plate 1":
                osdag_display_shape(self.display, self.plate1_model, update=True, color=column_color, label=label_plate1, canvas=self.cad_widget)
            elif self.component == "Plate 2":
                osdag_display_shape(self.display, self.plate2_model, update=True, color=beam_color, label=label_plate2, canvas=self.cad_widget)
            elif self.component == "Cover Plate":
                osdag_display_shape(self.display, self.platec_model, update=True, color=plate_color, label=label_platec, canvas=self.cad_widget)
                if self.platec2_model:
                    osdag_display_shape(self.display, self.platec2_model, update=True, color=plate_color, label=label_platec2, canvas=self.cad_widget)
                # Also show packing plates with cover plates
                if self.packing1_model is not None:
                    osdag_display_shape(self.display, self.packing1_model, update=True, color=packing_plate_color, label=label_packing, canvas=self.cad_widget)
                if self.packing2_model is not None:
                    osdag_display_shape(self.display, self.packing2_model, update=True, color=packing_plate_color, label=label_packing, canvas=self.cad_widget)
            elif self.component == "Welds":
                for weld in self.weld_models:
                    osdag_display_shape(self.display, weld, update=True, color=weld_color, label=label_weld, canvas=self.cad_widget)

        elif self.mainmodule == 'Flexure Member':
            self.flex = self.module_object  
            components = self.createSimplySupportedBeam()
            self.FObj = components.get('beam')
            
            hover_dict = self.module_object.hover_dict
            hover_dict["Hinged Support"] = "<b>Hinged Support</b>"
            hover_dict["Roller Support"] = "<b>Roller Support</b>"
            hover_dict["Support Block"] = "<b>Cantilever Support</b>"
            self.cad_widget.model_hover_labels = hover_dict.copy()
                
            label_flexure = ["Flexure Member", hover_dict.get("Flexure Member")]
            label_hinge = ["Hinged Support", hover_dict.get("Hinged Support")]
            label_roller = ["Roller Support", hover_dict.get("Roller Support")]
            label_block = ["Support Block", hover_dict.get("Support Block")]
            
           
            support_color_custom = Quantity_Color(20/255.0, 20/255.0, 20/255.0, Quantity_TOC_RGB)
            support_color_red = Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB) # Keeping red definition just in case, though unused for these supports now

            if self.component == "Model":
                if components.get('beam'):
                    osdag_display_shape(self.display, components['beam'], update=True, color=Quantity_NOC_SADDLEBROWN, label=label_flexure, canvas=self.cad_widget)
                if components.get('support_tri'):
                    osdag_display_shape(self.display, components['support_tri'], update=True, color=support_color_custom, transparency=0.6, label=label_hinge, canvas=self.cad_widget)
                if components.get('support_knot'):
                    osdag_display_shape(self.display, components['support_knot'], update=True, color=support_color_custom, transparency=0.6, label=label_hinge, canvas=self.cad_widget)
                if components.get('support_cyl'):
                    osdag_display_shape(self.display, components['support_cyl'], update=True, color=support_color_custom, transparency=0.6, label=label_roller, canvas=self.cad_widget)
                if components.get('support_block'):
                    osdag_display_shape(self.display, components['support_block'], update=True, color=support_color_custom, transparency=0.6, label=label_block, canvas=self.cad_widget)
                if components.get('support_hatch'):
                     osdag_display_shape(self.display, components['support_hatch'], update=True, color=Quantity_NOC_BLACK, label=label_block, canvas=self.cad_widget)

        elif self.mainmodule == 'Flexural Members - Cantilever':
            self.flex = self.module_object  
            cantilever_components = self.createCantileverBeam()
            
            print(f"DEBUG DISPLAY: Received components: {cantilever_components}")
            print(f"DEBUG DISPLAY: Beam: {cantilever_components.get('beam')}")
            print(f"DEBUG DISPLAY: Support block: {cantilever_components.get('support_block')}")
            
            hover_dict = self.module_object.hover_dict
            # Add support block to hover dictionary
            hover_dict["Support Block"] = (
                f"<b>Support Block</b><br>"
                f"Fixed support at cantilever left end<br>"
                f"Type: Cuboidal block<br>"
                f"Function: Represents fixed boundary condition"
            )
            self.cad_widget.model_hover_labels = hover_dict.copy()
                
            label_flexure = ["Flexure Member (Cantilever)", hover_dict.get("Flexure Member")]
            label_support = ["Support Block", hover_dict.get("Support Block")]
            
            # Define support block color (steel gray)
            support_color = Quantity_Color(0.7, 0.7, 0.7, Quantity_TOC_RGB)

            if self.component == "Model":
                # Display beam
                osdag_display_shape(self.display, cantilever_components['beam'], 
                                   update=True, color=Quantity_NOC_SADDLEBROWN, 
                                   label=label_flexure, canvas=self.cad_widget)
                
                # Debugging Support Block
                supp_block = cantilever_components.get('support_block')
                print(f"DEBUG DISPLAY: Support Block Object: {supp_block}")
                
                # Display support block if it exists
                if supp_block is not None:
                    print("DEBUG DISPLAY: Attempting to display support block...")
                    try:
                        osdag_display_shape(self.display, supp_block, 
                                           update=True, color=support_color, 
                                           label=label_support, canvas=self.cad_widget)
                        print("DEBUG DISPLAY: Support block display command executed.")
                    except Exception as e:
                        print(f"DEBUG DISPLAY ERROR: Failed to display support block: {e}")
                else:
                    print("DEBUG DISPLAY: Support block is None, not displaying")
                    
                # Display hatching lines if they exist
                supp_hatch = cantilever_components.get('support_hatch')
                if supp_hatch is not None:
                    try:
                        osdag_display_shape(self.display, supp_hatch,
                                            update=True, color=Quantity_NOC_BLACK,
                                            label=label_support, canvas=self.cad_widget)
                    except Exception as e:
                        print(f"DEBUG DISPLAY ERROR: Failed to display support hatch: {e}")


        elif self.mainmodule == 'Flexural Members - Purlins':
            if self.connection == KEY_DISP_FLEXURE4 :
                self.flex = self.module_object

                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
                
                # Hover dict
                hover_dict = self.module_object.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()

                label_flexure = ["Flexural Members", hover_dict.get("Flexural Members")]
                  
                print(f"THIS IS SELF.MODULE_OBJECT {self.flex}")
                self.FObj = self.createPurlin()

                if self.component == "Model":
                    osdag_display_shape(self.display, self.FObj, update=True, label=label_flexure, canvas=self.cad_widget)

        elif self.mainmodule == 'PLATE GIRDER':
            # Plate Girder display logic
            self.col = self.module_object
            
            # Reuse PGObj if already created by call_3DModel
            if hasattr(self, 'PGObj') and self.PGObj is not None:
                components = self.PGObj
            else:
                components = self.createPlateGirderCAD()
            
            # Define colors for components
            web_color = Quantity_Color(47/255.0, 47/255.0, 35/255.0, Quantity_TOC_RGB)
            flange_color = Quantity_Color(134/255.0, 134/255.0, 100/255.0, Quantity_TOC_RGB)
            stiffener_color = Quantity_Color(72/255.0, 72/255.0, 54/255.0, Quantity_TOC_RGB)
            weld_color = Quantity_NOC_SADDLEBROWN
            
            # Create hover labels dictionary
            hover_dict = {}
            if hasattr(self.col, "hover_dict"):
                hover_dict = self.col.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()
            
            label_web = ["Web Plate", hover_dict.get("Web Plate", "Web plate of the plate girder")]
            label_flange = ["Flange", hover_dict.get("Flange", "Flange plate of the plate girder")]
            label_stiffener = ["Stiffeners", hover_dict.get("Stiffeners", "Intermediate stiffener plates")]
            label_weld = ["Weld", hover_dict.get("Weld", "Fillet welds")]
            
            if self.component == "Model":
                # Display web plate
                if components.get('web_plate') is not None:
                    osdag_display_shape(self.display, components['web_plate'], update=True, 
                                       color=web_color, label=label_web, canvas=self.cad_widget)
                
                # Display top flange
                if components.get('top_flange') is not None:
                    osdag_display_shape(self.display, components['top_flange'], update=True, 
                                       color=flange_color, label=label_flange, canvas=self.cad_widget)
                
                # Display bottom flange
                if components.get('bottom_flange') is not None:
                    osdag_display_shape(self.display, components['bottom_flange'], update=True, 
                                       color=flange_color, label=label_flange, canvas=self.cad_widget)
                
                # Display stiffener plates
                if components.get('stiffener_plates') is not None:
                    osdag_display_shape(self.display, components['stiffener_plates'], update=True, 
                                       color=stiffener_color, label=label_stiffener, canvas=self.cad_widget)
                
                # Display horizontal plate (Longitudinal stiffener)
                if components.get('horizontal_plate') is not None:
                    osdag_display_shape(self.display, components['horizontal_plate'], update=True, 
                                       color=stiffener_color, label=label_stiffener, canvas=self.cad_widget)
                
                # Display longitudinal welds
                if components.get('longitudinal_welds') is not None:
                    osdag_display_shape(self.display, components['longitudinal_welds'], update=True, 
                                       color=weld_color, label=label_weld, canvas=self.cad_widget)
                
                # Display stiffener welds
                if components.get('stiffener_welds') is not None:
                    osdag_display_shape(self.display, components['stiffener_welds'], update=True, 
                                       color=weld_color, label=label_weld, canvas=self.cad_widget)
            
            elif self.component == "Web":
                if components.get('web_plate') is not None:
                    osdag_display_shape(self.display, components['web_plate'], update=True, 
                                       color=web_color, label=label_web, canvas=self.cad_widget)
            
            elif self.component == "Top Flange":
                if components.get('top_flange') is not None:
                    osdag_display_shape(self.display, components['top_flange'], update=True, 
                                       color=flange_color, label=label_flange, canvas=self.cad_widget)
            
            elif self.component == "Bottom Flange":
                if components.get('bottom_flange') is not None:
                    osdag_display_shape(self.display, components['bottom_flange'], update=True, 
                                       color=flange_color, label=label_flange, canvas=self.cad_widget)
            
            elif self.component == "Stiffeners":
                if components.get('stiffener_plates') is not None:
                    osdag_display_shape(self.display, components['stiffener_plates'], update=True, 
                                       color=stiffener_color, label=label_stiffener, canvas=self.cad_widget)
                
                if components.get('horizontal_plate') is not None:
                    osdag_display_shape(self.display, components['horizontal_plate'], update=True, 
                                       color=stiffener_color, label=label_stiffener, canvas=self.cad_widget)
            
            elif self.component == "Welds":
                if components.get('longitudinal_welds') is not None:
                    osdag_display_shape(self.display, components['longitudinal_welds'], update=True, 
                                       color=weld_color, label=label_weld, canvas=self.cad_widget)
                if components.get('stiffener_welds') is not None:
                    osdag_display_shape(self.display, components['stiffener_welds'], update=True, 
                                       color=weld_color, label=label_weld, canvas=self.cad_widget)

        elif self.mainmodule == KEY_DISP_STRUT_WELDED_END_GUSSET:
            self.col = self.module_object  
            # self.ColObj is created in call_3DModel
            if hasattr(self, 'ColObj') and self.ColObj is not None and not isinstance(self.ColObj, OCC.Core.TopoDS.TopoDS_Shape):
                 strutCAD = self.ColObj
            else:
                 strutCAD = self.createStrutWeldedCAD()
            
            # Setup hover labels
            hover_dict = {}
            if hasattr(self.col, "hover_dict"):
                hover_dict = self.col.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()
            
            member = strutCAD.get_members_models()
            plate = strutCAD.get_plates_models()
            welds = strutCAD.get_welded_models()

            # Define labels for hover
            label_member = ["Member", hover_dict.get("Member")]
            label_plate = ["Plate", hover_dict.get("Plate")]
            label_weld = ["Weld", hover_dict.get("Weld")]

            if self.component == "Model":
                osdag_display_shape(self.display, member, color=beam_color, update=True, label=label_member, canvas=self.cad_widget)
                osdag_display_shape(self.display, plate, color=plate_color, update=True, label=label_plate, canvas=self.cad_widget)
                osdag_display_shape(self.display, welds, color=weld_color, update=True, label=label_weld, canvas=self.cad_widget)
            elif self.component == "Member":
                osdag_display_shape(self.display, member, color=beam_color, update=True, label=label_member, canvas=self.cad_widget)
            elif self.component == "Plate":
                osdag_display_shape(self.display, plate, color=plate_color, update=True, label=label_plate, canvas=self.cad_widget)
                osdag_display_shape(self.display, welds, color=weld_color, update=True, label=label_weld, canvas=self.cad_widget)


        elif self.mainmodule == KEY_DISP_STRUT_BOLTED_END_GUSSET:
            print(f"DEBUG: display_3DModel called for KEY_DISP_STRUT_BOLTED_END_GUSSET. Component: {self.component}")
            self.col = self.module_object
            
            # Use self.ColObj if already created
            if hasattr(self, 'ColObj') and self.ColObj is not None:
                print("DEBUG: Using existing self.ColObj")
                strutCAD = self.ColObj
            else:
                print("DEBUG: Creating new strutCAD object")
                strutCAD = self.createStrutBoltedCAD()
            
            hover_dict = self.col.hover_dict
            self.cad_widget.model_hover_labels = hover_dict.copy()

            print("DEBUG: Fetching models from strutCAD")
            member = strutCAD.get_members_models()
            plate = strutCAD.get_plates_models()
            nutbolt = strutCAD.get_nut_bolt_array_models()
            onlymember = strutCAD.get_only_members_models()
            print(f"DEBUG: Models fetched. Member: {member}, Plate: {plate}, Bolts: {nutbolt}")

            label_member = ["Member", hover_dict.get("Member")]
            label_plate = ["Plate", hover_dict.get("Plate")]
            label_bolt = ["Bolt", hover_dict.get("Bolt")]

            if self.component == "Member":
                print("DEBUG: Displaying Member component")
                osdag_display_shape(self.display, onlymember, color=beam_color, update=True, label=label_member, canvas=self.cad_widget)
            elif self.component == "Plate":
                print("DEBUG: Displaying Plate component")
                osdag_display_shape(self.display, plate, color=plate_color, update=True, label=label_plate, canvas=self.cad_widget)
                osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True, label=label_bolt, canvas=self.cad_widget)
            else: # Model
                print("DEBUG: Displaying Full Model")
                osdag_display_shape(self.display, member, color=beam_color, update=True, label=label_member, canvas=self.cad_widget)
                osdag_display_shape(self.display, plate, color=plate_color, update=True, label=label_plate, canvas=self.cad_widget)
                osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True, label=label_bolt, canvas=self.cad_widget)
            print("DEBUG: Strut Bolted display logic finished")

        else:
            if self.connection == KEY_DISP_TENSION_BOLTED:
                self.T = self.module_object

                 # Hover dict
                hover_dict = self.module_object.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()

                # self.TObj = self.createTensionCAD()
                # NOTE: Reuse self.TObj created in call_3DModel() to prevent duplicate CAD creation
                # which causes OpenCASCADE memory corruption (malloc double linked list error)

                member = self.TObj.get_members_models()
                plate = self.TObj.get_plates_models()

                nutbolt = self.TObj.get_nut_bolt_array_models()

                onlymember = self.TObj.get_only_members_models()
                # distance = self.T.length/2 - (2* self.T.plate.end_dist_provided + (self.T.plate.bolt_line - 1 ) * self.T.plate.pitch_provided)
                # Point = gp_Pnt(distance, 0.0, 300)
                # DisplayMsg(self.display, Point, self.T.section_size_1.designation)
                
                label_bolt = ["Bolt", hover_dict.get("Bolt")]
                label_plate = ["Plate", hover_dict.get("Plate")]
                label_member = ["Member", hover_dict.get("Member")]

                if self.component == "Member":  # Todo: change this into key
                    osdag_display_shape(self.display, onlymember, color=beam_color, update=True,label=label_member, canvas=self.cad_widget)
                elif self.component == "Plate":
                    osdag_display_shape(self.display, plate, color=plate_color, update=True, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True, label=label_bolt, canvas=self.cad_widget)
                elif self.component == "Endplate":
                    endplate = self.TObj.get_end_plates_models()
                    end_nutbolt = self.TObj.get_end_nut_bolt_array_models()
                    osdag_display_shape(self.display, endplate, color=plate_color, update=True, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, end_nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True, label=label_bolt, canvas=self.cad_widget)
                else:
                    connector = BRepAlgoAPI_Fuse(nutbolt, plate).Shape()
                    shape = BRepAlgoAPI_Fuse(connector, member).Shape()
                    self.TObj.shape = shape
                    osdag_display_shape(self.display, member, color=beam_color, update=True, label=label_member, canvas=self.cad_widget)
                    osdag_display_shape(self.display, plate, color=plate_color, update=True, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True, label=label_bolt, canvas=self.cad_widget)

            elif self.connection == KEY_DISP_TENSION_WELDED:
                self.T = self.module_object
                hover_dict = self.module_object.hover_dict
                self.cad_widget.model_hover_labels = hover_dict.copy()

                # self.TObj = self.createTensionCAD()
                # NOTE: self.TObj is already created in call_3DModel() before display_3DModel() is called
                # Do NOT call createTensionCAD() again here - it causes OpenCASCADE memory corruption
                member = self.TObj.get_members_models()
                plate = self.TObj.get_plates_models()
                welds = self.TObj.get_welded_models()

                label_plate = ["Plate", hover_dict.get("Plate")]
                label_weld = ["Weld", hover_dict.get("Weld")]
                label_member = ["Member", hover_dict.get("Member")]

                if hasattr(self, "cad_widget") and hasattr(self.T, "hover_dict"):
                    self.cad_widget.model_hover_labels = self.T.hover_dict
                if self.component == "Member":  # Todo: change this into key
                    osdag_display_shape(self.display, member, update=True, color=beam_color, label=label_member, canvas=self.cad_widget)
                elif self.component == "Plate":
                    osdag_display_shape(self.display, plate, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, welds, update=True, color=weld_color, label=label_weld, canvas=self.cad_widget)      
                elif self.component == "Endplate":
                    endplate = self.TObj.get_end_plates_models()
                    osdag_display_shape(self.display, endplate, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                else:
                    connector = BRepAlgoAPI_Fuse(welds, plate).Shape()
                    shape = BRepAlgoAPI_Fuse(connector, member).Shape()
                    self.TObj.shape = shape
                    osdag_display_shape(self.display, member, update=True, color=beam_color, label=label_member, canvas=self.cad_widget)
                    osdag_display_shape(self.display, plate, update=True, color=plate_color, label=label_plate, canvas=self.cad_widget)
                    osdag_display_shape(self.display, welds, update=True, color=weld_color, label=label_weld, canvas=self.cad_widget)

    def call_3DModel(self, flag, module_object):  # Done
        self.module_object = module_object  # Store the object directly
        
        # Override mainmodule for Strut Bolted connection to ensure correct CAD generation
        # This handles the case where the module inherits from 'Member' generic class
        if hasattr(module_object, "module") and module_object.module == KEY_DISP_STRUT_BOLTED_END_GUSSET:
            self.mainmodule = KEY_DISP_STRUT_BOLTED_END_GUSSET
        elif hasattr(module_object, "module") and module_object.module == KEY_DISP_STRUT_WELDED_END_GUSSET:
             self.mainmodule = KEY_DISP_STRUT_WELDED_END_GUSSET



        if self.mainmodule == "Shear Connection":

            A = self.module_object  

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
                self.cad_widget.display_view_cube()

        elif self.mainmodule == "Moment Connection":

            if self.connection == KEY_DISP_BEAMCOVERPLATE or self.connection == KEY_DISP_BEAMCOVERPLATEWELD:
                if flag is True:

                    self.B = module_object
                    self.CPObj = self.createBBCoverPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")
                else:
                    self.display.EraseAll()
                self.cad_widget.display_view_cube()

            elif self.connection == KEY_DISP_BB_EP_SPLICE:
                if flag is True:
                    self.CPObj = self.createBBEndPlateCAD()
                    self.display_3DModel("Model", "gradient_bg")
                else:
                    self.display.EraseAll()
                self.cad_widget.display_view_cube()

            elif self.connection == KEY_DISP_BCENDPLATE:
                if flag is True:

                    self.CPObj = self.createBCEndPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()
                self.cad_widget.display_view_cube()

            elif self.connection == KEY_DISP_COLUMNCOVERPLATE or self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:
                if flag is True:

                    self.CPObj = self.createCCCoverPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()
                self.cad_widget.display_view_cube()

            elif self.connection == KEY_DISP_COLUMNENDPLATE:
                if flag is True:
                    self.CEPObj = self.createCCEndPlateCAD()

                    self.display_3DModel("Model", "gradient_bg")
                else:
                    self.display.EraseAll()
                self.cad_widget.display_view_cube()

            elif self.connection == KEY_DISP_BASE_PLATE:

                if flag is True:
                    self.BPObj = self.createBasePlateCAD()

                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()
                self.cad_widget.display_view_cube()
        elif self.mainmodule == 'Flexure Member':
            if flag is True:
                self.FObj = self.createSimplySupportedBeam()

                self.display_3DModel("Model", "gradient_bg")
            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()

        elif self.mainmodule == 'Flexural Members - Cantilever':
            if flag is True:
                self.FObj = self.createCantileverBeam()

                self.display_3DModel("Model", "gradient_bg")
            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()

        elif self.mainmodule == 'Flexural Members - Purlins':
            if flag is True:
                self.FObj = self.createPurlin()

                self.display_3DModel("Model", "gradient_bg")
            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()

        elif self.mainmodule == 'Columns with known support conditions':
            if flag is True:
                self.ColObj = self.createColumnInFrameCAD()

                self.display_3DModel("Model", "gradient_bg")

            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()
        elif self.mainmodule == KEY_DISP_STRUT_WELDED_END_GUSSET:
            if flag is True:
                self.ColObj = self.createStrutWeldedCAD()

                self.display_3DModel("Model", "gradient_bg")

            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()
        elif self.mainmodule == KEY_DISP_STRUT_BOLTED_END_GUSSET:
            if flag is True:
                print("DEBUG: Flag is True, calling createStrutBoltedCAD")
                self.ColObj = self.createStrutBoltedCAD()
                self.display_3DModel("Model", "gradient_bg")
            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()
        elif self.mainmodule == 'Lap Joint Bolted Connection':
            if flag is True:
                self.ColObj = self.createBoltedLapJoint()
                self.display_3DModel("Model", "gradient_bg")

            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()
                
        elif self.mainmodule == 'Butt Joint Bolted Connection':
            if flag is True:
                self.ColObj = self.createButtJointBoltedCAD()
                self.display_3DModel("Model", "gradient_bg")

            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()

        elif self.mainmodule == 'Butt Joint Welded Connection':
            if flag is True:
                self.ColObj = self.createButtJointWeldedCAD()
                self.display_3DModel("Model", "gradient_bg")
            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()
        elif self.mainmodule == KEY_DISP_LAPJOINTWELDED:
            if flag is True:
                self.display_3DModel("Model", "gradient_bg")
            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()
        elif self.mainmodule == 'PLATE GIRDER':
            print("DEBUG: PLATE GIRDER case triggered")
            if flag is True:
                print("DEBUG: Flag is True, calling createPlateGirderCAD")
                try:
                    self.PGObj = self.createPlateGirderCAD()
                    print(f"DEBUG: createPlateGirderCAD returned: {self.PGObj}")
                    self.display_3DModel("Model", "gradient_bg")
                    print("DEBUG: display_3DModel completed")
                except Exception as e:
                    print(f"ERROR in PLATE GIRDER CAD: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                self.display.EraseAll()
                self.cad_widget.display_view_cube()
        else:
            if self.connection == KEY_DISP_TENSION_BOLTED or self.connection == KEY_DISP_TENSION_WELDED:

                if flag is True:
                    self.TObj = self.createTensionCAD()
                    self.display_3DModel("Model", "gradient_bg")

                else:
                    self.display.EraseAll()
                self.cad_widget.display_view_cube()

    def create2Dcad(self):
        ''' Returns the 3D model depending upon component
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

        elif self.mainmodule == 'Flexure Member':
            # Simply supported beam - only has one component (the beam section)
            final_model = self.FObj

        elif self.mainmodule == 'Flexural Members - Cantilever':
            # Cantilever beam - only has one component (the beam section)
            final_model = self.FObj

        elif self.mainmodule == 'Flexural Members - Purlins':
            # Purlin - only has one component (the C-section)
            final_model = self.FObj

        elif self.mainmodule == 'Columns with known support conditions':
            # Column - only has one component (the column section)
            final_model = self.ColObj

        elif self.mainmodule == 'Struts in Trusses':
            # Strut - can be angle or back-to-back angles with gussets
            final_model = self.ColObj

        elif self.mainmodule == 'Lap Joint Bolted Connection':
            if self.component == "Plate1":
                final_model = self.plate1_model
            elif self.component == "Plate2":
                final_model = self.plate2_model
            elif self.component == "Connector":
                # Return bolts and nuts
                cadlist = self.bolt_models + self.nuts_models
            else:
                # Return complete assembly
                final_model = self.assembly

        elif self.mainmodule == 'Lap Joint Welded Connection':
            if self.component == "Plate1":
                final_model = self.plate1_model
            elif self.component == "Plate2":
                final_model = self.plate2_model
            elif self.component == "Weld":
                cadlist = self.weld_models
            else:
                # Return complete assembly
                final_model = self.assembly

        elif self.mainmodule == 'Butt Joint Bolted Connection':
            if self.component == "Plate1":
                final_model = self.plate1_model
            elif self.component == "Plate2":
                final_model = self.plate2_model
            elif self.component == "Cover Plate":
                final_model = self.platec_model
            elif self.component == "Connector":
                # Return bolts and nuts
                cadlist = self.bolt_models + self.nuts_models
            else:
                # Return complete assembly
                final_model = self.assembly

        elif self.mainmodule == "Member":
            if self.connection == KEY_DISP_TENSION_BOLTED or self.connection == KEY_DISP_TENSION_WELDED:
                if self.component == "Member":
                    final_model = self.TObj.get_members_models()
                elif self.component == "Plate":
                    if self.connection == KEY_DISP_TENSION_BOLTED:
                        cadlist = [self.TObj.get_plates_models(), self.TObj.get_nut_bolt_array_models()]
                    else:
                        cadlist = [self.TObj.get_plates_models(), self.TObj.get_welded_models()]
                elif self.component == "Endplate":
                    if self.connection == KEY_DISP_TENSION_BOLTED:
                        cadlist = [self.TObj.get_end_plates_models(), self.TObj.get_end_nut_bolt_array_models()]
                    else:
                        cadlist = [self.TObj.get_end_plates_models()]
                else:
                    final_model = self.TObj.shape

        # Fuse multiple models if cadlist is populated
        if cadlist and len(cadlist) > 1:
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        elif cadlist and len(cadlist) == 1:
            final_model = cadlist[0]

        # Fix for optimized modules returning lists (e.g. BB Endplate)
        # Exporters require a single TopoDS_Shape, so we must fuse here if we have a list.
        if isinstance(final_model, list):
            if len(final_model) > 0:
                fused_shape = final_model[0]
                for item in final_model[1:]:
                    fused_shape = BRepAlgoAPI_Fuse(item, fused_shape).Shape()
                final_model = fused_shape
            else:
                final_model = None
        
        return final_model

        