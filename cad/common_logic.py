'''
Created on 18-Nov-2016

@author: deepa
'''

# from utils.common.component import Bolt,Beam,Section,Angle,Plate,Nut,Column,Weld
from cad.items.notch import Notch
from cad.items.bolt import Bolt
from cad.items.nut import Nut
from cad.items.plate import Plate
from cad.items.ISection import ISection
from cad.items.filletweld import FilletWeld
from cad.items.angle import Angle
from cad.items.anchor_bolt import AnchorBolt_A, AnchorBolt_B, AnchorBolt_Endplate
from cad.items.stiffener_plate import StiffenerPlate
from cad.items.grout import Grout
from cad.items.angle import Angle
from cad.items.channel import Channel
from cad.items.Gasset_plate import GassetPlate

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
# from cad.ShearConnections.EndPlate.nutBoltPlacement import NutBoltArray as endNutBoltArray

from cad.ShearConnections.SeatedAngle.CAD_col_web_beam_web_connectivity import ColWebBeamWeb as seatColWebBeamWeb
from cad.ShearConnections.SeatedAngle.CAD_col_flange_beam_web_connectivity import \
    ColFlangeBeamWeb as seatColFlangeBeamWeb
from cad.ShearConnections.SeatedAngle.CAD_nut_bolt_placement import NutBoltArray as seatNutBoltArray
# from cad.ShearConnections.SeatedAngle.seat_angle_calc import SeatAngleCalculation

from cad.BBCad.nutBoltPlacement_AF import NutBoltArray_AF
from cad.BBCad.nutBoltPlacement_BF import NutBoltArray_BF
from cad.BBCad.nutBoltPlacement_Web import NutBoltArray_Web
from cad.BBCad.BBCoverPlateBoltedCAD import BBCoverPlateBoltedCAD

from cad.MomentConnections.BBSpliceCoverlateCAD.WeldedCAD import BBSpliceCoverPlateWeldedCAD

from cad.MomentConnections.CCSpliceCoverPlateCAD.WeldedCAD import CCSpliceCoverPlateWeldedCAD

from cad.BasePlateCad.baseplateconnection import BasePlateCad
from cad.BasePlateCad.nutBoltPlacement import NutBoltArray as bpNutBoltArray

from cad.Tension.WeldedCAD import TensionAngleWeldCAD, TensionChannelWeldCAD
from cad.Tension.BoltedCAD import TensionAngleBoltCAD, TensionChannelBoltCAD
from cad.Tension.nutBoltPlacement import NutBoltArray as TNutBoltArray
from cad.Tension.intermittentConnections import IntermittentNutBoltPlateArray, IntermittentWelds

# from design_type.connection.fin_plate_connection import FinPlateConnection
# from design_type.connection.cleat_angle_connection import CleatAngleConnection
from design_type.connection.beam_cover_plate import BeamCoverPlate
from design_type.connection.base_plate_connection import BasePlateConnection
from utilities import osdag_display_shape
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
import copy

from Common import *

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

import OCC.Core.V3d
from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_BLUE1
from OCC.Core.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from OCC.Core.Quantity import Quantity_NOC_GRAY25 as GRAY

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


    # def __init__(self, uiObj, dictbeamdata, dictcoldata, dictangledata,
    #              dicttopangledata, loc, component, bolt_R, bolt_T,
    #              bolt_Ht, nut_T, display, folder, connection):
    def __init__(self, display, folder, connection, mainmodule):

        # self.bolt = Bolt
        # self.beam = Beam
        # # self.section = Section
        # self.angle = Angle
        # self.plate = Plate
        # self.nut = Nut
        # self.column = Column
        # self.weld = Weld

        self.display = display
        self.mainmodule = mainmodule
        self.connection = connection
        # self.resultObj = self.call_calculation()

        self.connectivityObj = None
        self.folder = folder

    # ============================= FinCalculation ===========================================
    # def call_calculation(self):  # Done
    #     if self.connection == "Fin Plate":
    #         outputs = finConn(self.uiObj)
    #     # elif self.connection == "Endplate":
    #     #     outputs = end_connection(self.uiObj)
    #     # elif self.connection == "cleatAngle":
    #     #     outputs = cleat_connection(self.uiObj)
    #     # elif self.connection == "SeatedAngle":
    #     #     self.sa_calc_obj = SeatAngleCalculation()
    #     #     outputs = self.sa_calc_obj.seat_angle_connection(self.uiObj)
    #     else:
    #         pass
    #     return outputs

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
        This routine takes the bolt diameter and return bolt head thickness as per IS:3757(1989)


       bolt Head Dia
        <-------->
        __________
        |        | | T = Thickness
        |________| |
           |  |
           |  |
           |  |

        '''
        boltHeadThick = {5: 4, 6: 5, 8: 6, 10: 7, 12: 8, 16: 10, 20: 12.5, 22: 14, 24: 15, 27: 17, 30: 18.7, 36: 22.5}
        return boltHeadThick[boltDia]

    def boltHeadDia_Calculation(self, boltDia):
        '''
        This routine takes the bolt diameter and return bolt head diameter as per IS:3757(1989)

       bolt Head Dia
        <-------->
        __________
        |        |
        |________|
           |  |
           |  |
           |  |

        '''
        boltHeadDia = {5: 7, 6: 8, 8: 10, 10: 15, 12: 20, 16: 27, 20: 34, 22: 36, 24: 41, 27: 46, 30: 50, 36: 60}
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
        boltHeadDia = {5: 40, 6: 40, 8: 40, 10: 40, 12: 40, 16: 50, 20: 50, 22: 50, 24: 50, 27: 60, 30: 65, 36: 75}

        return boltHeadDia[boltDia]

    def nutThick_Calculation(self, boltDia):
        '''
        Returns the thickness of the nut depending upon the nut diameter as per IS1363-3(2002)
        '''
        nutDia = {5: 5, 6: 5.65, 8: 7.15, 10: 8.75, 12: 11.3, 16: 15, 20: 17.95, 22: 19.0, 24: 21.25, 27: 23, 30: 25.35,
                  36: 30.65}

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
        notch_height = A.supported_section.notch_ht
        notch_R1 = max([A.supporting_section.root_radius, A.supported_section.root_radius, 10])

        if self.connection == KEY_DISP_CLEATANGLE:
            gap = A.cleat.gap
            notchObj = Notch(R1=notch_R1,
                             height=notch_height,
                             width=(A.supporting_section.flange_width / 2.0 - (
                                     A.supporting_section.web_thickness / 2.0 + gap)) + gap,
                             length=A.supported_section.flange_width)
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
                              length=1000, notchObj=None)
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
        notch_height = A.supported_section.notch_ht
        notch_R1 = max([A.supporting_section.root_radius, A.supported_section.root_radius, 10])

        if self.connection == KEY_DISP_CLEATANGLE:
            gap = A.cleat.gap
            notchObj = Notch(R1=notch_R1,
                             height=notch_height,
                             width=(A.supporting_section.flange_width / 2.0 - (
                                     A.supporting_section.web_thickness / 2.0 + gap)) + gap,
                             length=A.supported_section.flange_width)
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
                              length=1000, notchObj=None)

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
            cnut_space = A.supporting_section.web_thickness + A.cleat.thickness + nut_T
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
            beam_length = 800.0

            beam_Left = ISection(B=beam_B, T=beam_T, D=beam_d, t=beam_tw,
                                 R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                                 length=beam_length, notchObj=None)  # Call to ISection in Component repository
            beam_Right = copy.copy(beam_Left)  # Since both the beams are same
            # outputobj = self.outputs  # Output dictionary from calculation file
            # alist = self.designParameters()  # An object to save all input values entered by user

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

    def createCCCoverPlateCAD(self):

        if self.connection == KEY_DISP_COLUMNCOVERPLATE:
            pass
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

    def createBasePlateCAD(self):
        """
        :return: The calculated values/parameters to create 3D CAD model of individual components.
        """
        BP = self.module_class

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
        weldAbvFlang = FilletWeld(b=float(BP.weld_size_flange), h=float(BP.weld_size_flange), L=column.B)
        weldBelwFlang = FilletWeld(b=float(BP.weld_size_flange), h=float(BP.weld_size_flange),
                                   L=(column.B - column.t - 2 * (column.R1 + column.R2)) / 2)
        weldSideWeb = FilletWeld(b=float(BP.weld_size_web), h=float(BP.weld_size_web),
                                 L=column.D - 2 * (column.t + column.R1))

        gusset = StiffenerPlate(L=BP.gusset_plate_length, W=BP.gusset_plate_height, T=BP.gusset_plate_thick,
                                L11=(BP.gusset_plate_length - (column.B + 100)) / 2, L12=BP.gusset_plate_height - 100,
                                R11=(baseplate.W - (column.B + 100)) / 2, R12=200 - 100)
        stiffener = StiffenerPlate(L=BP.stiffener_plate_length, W=BP.stiffener_plate_height, T=BP.stiffener_plate_thick,
                                   L11=BP.stiffener_plate_length - 50, L12=BP.stiffener_plate_height - 100)

        concrete = Plate(L=baseplate.L * 1.5, W=baseplate.W * 1.5, T=BP.anchor_length_provided * 1.3)
        grout = Grout(L=concrete.L, W=concrete.W, T=50)

        bolt_d = float(BP.anchor_dia_provided)
        bolt_r = bolt_d / 2  # Bolt radius (Shank part)
        bolt_R = self.boltHeadDia_Calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
        # bolt_T = self.boltHeadThick_Calculation(bolt_d)      # Bolt head thickness
        nut_T = self.nutThick_Calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
        nut_HT = nut_T

        ex_length = (50 + 24 + baseplate.T + grout.T)  # nut.T = 24
        if BP.dp_anchor_type == 'IS 5624-Type A':
            bolt = AnchorBolt_A(l=float(BP.anchor_length_provided), c=125, a=75, r=float(BP.anchor_dia_provided) / 2,
                                ex=ex_length)
        elif BP.dp_anchor_type == 'IS 5624-Type B':
            bolt = AnchorBolt_B(l=float(BP.anchor_length_provided), r=float(BP.anchor_dia_provided) / 2, ex=ex_length)
        elif BP.dp_anchor_type == 'End Plate Type':
            bolt = AnchorBolt_Endplate(l=float(BP.anchor_length_provided), r=float(BP.anchor_dia_provided) / 2,
                                       ex=ex_length)

        nut = Nut(R=bolt_R, T=nut_T, H=nut_HT, innerR1=bolt_r)
        numberOfBolts = 4
        nutSpace = bolt.c + baseplate.T
        bolthight = nut.T + 50

        nut_bolt_array = bpNutBoltArray(column, baseplate, nut, bolt, numberOfBolts, nutSpace)

        basePlate = BasePlateCad(BP, column, nut_bolt_array, bolthight, baseplate, weldAbvFlang, weldBelwFlang,
                                 weldSideWeb, concrete, gusset, stiffener, grout)
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
            intermittentPlates = Plate(L=float(T.inter_plate_length), W=float(T.inter_plate_height),
                                       T=float(T.plate.thickness_provided))

            if T.sec_profile == 'Channels' or T.sec_profile == 'Back to Back Channels':
                member = Channel(B=float(T.section_size_1.flange_width), T=float(T.section_size_1.flange_thickness),
                                 D=float(T.section_size_1.depth), t=float(T.section_size_1.web_thickness),
                                 R1=float(T.section_size_1.root_radius), R2=float(T.section_size_1.toe_radius),
                                 L=float(T.length))
                if T.sec_profile == 'Channels':
                    nut_space = member.t + plate.T + nut.T  # member.T + plate.T + nut.T
                else:
                    nut_space = 2 * member.t + plate.T + nut.T  # 2*member.T + plate.T + nut.T

                inter_array = IntermittentNutBoltPlateArray(T, nut, bolt, intermittentPlate, nut_space)
                nut_bolt_array = TNutBoltArray(T, nut, bolt, nut_space)
                tensionCAD = TensionChannelBoltCAD(T, member, plate, nut_bolt_array, inter_array)

            else:
                member = Angle(L=float(T.length), A=float(T.section_size_1.max_leg), B=float(T.section_size_1.min_leg),
                               T=float(T.section_size_1.thickness), R1=float(T.section_size_1.root_radius),
                               R2=float(T.section_size_1.toe_radius))
                if T.sec_profile == 'Back to Back Angles':
                    nut_space = 2 * member.T + plate.T + nut.T
                else:
                    nut_space = member.T + plate.T + nut.T

                inter_array = IntermittentNutBoltPlateArray(T, nut, bolt, intermittentPlates, nut_space)
                nut_bolt_array = TNutBoltArray(T, nut, bolt, nut_space)
                tensionCAD = TensionAngleBoltCAD(T, member, plate, nut_bolt_array, inter_array)

        else:
            plate = GassetPlate(L=float(T.plate.length + 50), H=float(T.plate.height),
                                T=float(T.plate.thickness_provided), degree=30)
            intermittentPlates = Plate(L=float(T.inter_plate_length), W=float(T.inter_plate_height),
                                       T=float(T.plate.thickness_provided))

            intermittentWelds = FilletWeld(h=float(T.inter_weld_size), b=float(T.inter_weld_size),
                                           L=intermittentPlates.W)
            s = max(15, float(T.weld.size))
            plate_intercept = plate.L - s - 50
            if T.sec_profile == 'Channels' or T.sec_profile == 'Back to Back Channels':
                member = Channel(B=float(T.section_size_1.flange_width), T=float(T.section_size_1.flange_thickness),
                                 D=float(T.section_size_1.depth), t=float(T.section_size_1.web_thickness),
                                 R1=float(T.section_size_1.root_radius), R2=float(T.section_size_1.toe_radius),
                                 L=float(T.length))
                inline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(plate_intercept))
                opline_weld = FilletWeld(b=float(T.weld.size), h=float(T.weld.size), L=float(member.D))

                weld_plate_array = IntermittentWelds(T, intermittentWelds, intermittentPlates)
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

                weld_plate_array = IntermittentWelds(T, intermittentWelds, intermittentPlates)
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

            # if self.connection == KEY_DISP_FINPLATE:
            #     A = self.module_class()
            #     # A = FinPlateConnection()
            # elif self.connection == KEY_DISP_CLEATANGLE:
            #     A = CleatAngleConnection()
            # else:
            #     pass

            self.loc = A.connectivity


            if self.loc == "Column flange-Beam web" and self.connection == "Fin Plate":
                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
            elif self.loc == "Column flange-Beam flange" and self.connection == "SeatedAngle":
                self.display.View.SetProj(OCC.Core.V3d.V3d_XnegYnegZpos)
            elif self.loc == "Column web-Beam flange" and self.connection == "SeatedAngle":
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
                osdag_display_shape(self.display, self.connectivityObj.weldModelLeft, color='red', update=True)
                osdag_display_shape(self.display, self.connectivityObj.weldModelRight, color='red', update=True)
                osdag_display_shape(self.display, self.connectivityObj.plateModel, color=Quantity_NOC_BLUE1, update=True)
                nutboltlist = self.connectivityObj.nut_bolt_array.get_models()
                for nutbolt in nutboltlist:
                    osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

            elif self.component == "Model":

                osdag_display_shape(self.display, self.connectivityObj.columnModel, update=True)
                osdag_display_shape(self.display, self.connectivityObj.beamModel, material=Graphic3d_NOT_2D_ALUMINUM,
                                    update=True)
                if self.connection == KEY_DISP_FINPLATE or self.connection == KEY_DISP_ENDPLATE:
                    osdag_display_shape(self.display, self.connectivityObj.weldModelLeft, color='red', update=True)
                    osdag_display_shape(self.display, self.connectivityObj.weldModelRight, color='red', update=True)
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
                    osdag_display_shape(self.display, self.CPObj.get_beamsModel(), update=True)

                elif self.component == "Connector":
                    osdag_display_shape(self.display, self.CPObj.get_flangewebplatesModel(), update=True,
                                        color='Blue')
                    if self.B.preference != 'Outside':
                        osdag_display_shape(self.display, self.CPObj.get_innetplatesModels(), update=True,
                                            color='Blue')

                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_arrayModels(), update=True,
                                        color=Quantity_NOC_SADDLEBROWN)

                elif self.component == "Model":
                    osdag_display_shape(self.display, self.CPObj.get_beamsModel(), update=True)
                    osdag_display_shape(self.display, self.CPObj.get_flangewebplatesModel(), update=True,
                                        color='Blue')

                    # Todo: remove velove commented lines

                    if self.B.preference != 'Outside':
                        osdag_display_shape(self.display, self.CPObj.get_innetplatesModels(), update=True,
                                            color='Blue')

                    osdag_display_shape(self.display, self.CPObj.get_nut_bolt_arrayModels(), update=True,
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
                    osdag_display_shape(self.display, plates, update=True, color='Blue')
                    osdag_display_shape(self.display, welds, update=True, color='Red')
                elif self.component == "Model":
                    osdag_display_shape(self.display, beams, update=True)
                    osdag_display_shape(self.display, plates, update=True, color='Blue')
                    osdag_display_shape(self.display, welds, update=True, color='Red')

            elif self.connection == KEY_DISP_COLUMNCOVERPLATE:
                pass
            elif self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:
                self.C = self.module_class()
                self.CPObj = self.createCCCoverPlateCAD()
                columns = self.CPObj.get_column_models()
                plates = self.CPObj.get_plate_models()
                welds = self.CPObj.get_welded_modules()

                if self.component == "Beam":
                    # Displays both beams
                    osdag_display_shape(self.display, columns, update=True)
                elif self.component == "Connector":
                    osdag_display_shape(self.display, plates, update=True, color='Blue')
                    osdag_display_shape(self.display, welds, update=True, color='Red')
                elif self.component == "Model":
                    osdag_display_shape(self.display, columns, update=True)
                    osdag_display_shape(self.display, plates, update=True, color='Blue')
                    osdag_display_shape(self.display, welds, update=True, color='Red')

            elif self.connection == KEY_DISP_BASE_PLATE:
                self.Bp = self.module_class()

                self.BPObj = self.createBasePlateCAD()

                column = self.BPObj.get_column_model()
                plate = self.BPObj.get_plate_connector_models()
                weld = self.BPObj.get_welded_models()
                nut_bolt = self.BPObj.get_nut_bolt_array_models()
                conc = self.BPObj.get_concrete_models()
                grout = self.BPObj.get_grout_models()

                if self.component == "Model":  # Todo: change this into key
                    osdag_display_shape(self.display, column, update=True)
                    osdag_display_shape(self.display, plate, color='Blue', update=True)
                    osdag_display_shape(self.display, weld, color='RED', update=True)
                    osdag_display_shape(self.display, nut_bolt, color='YELLOW', update=True)
                    osdag_display_shape(self.display, conc, color=GRAY, transparency=0.5, update=True)
                    osdag_display_shape(self.display, grout, color=GRAY, transparency=0.5, update=True)

                elif self.component == "Column":
                    osdag_display_shape(self.display, column, update=True)

                elif self.component == "Connector":
                    osdag_display_shape(self.display, plate, color='Blue', update=True)
                    osdag_display_shape(self.display, weld, color='RED', update=True)
                    osdag_display_shape(self.display, nut_bolt, color='YELLOW', update=True)

        else:
            if self.connection == KEY_DISP_TENSION_BOLTED:
                self.T = self.module_class()
                self.TObj = self.createTensionCAD()

                member = self.TObj.get_members_models()
                plate = self.TObj.get_plates_models()
                nutbolt = self.TObj.get_nut_bolt_array_models()
                if self.component == "Model":  # Todo: change this into key
                    osdag_display_shape(self.display, member, update=True)
                    osdag_display_shape(self.display, plate, color='BLUE', update=True)
                    osdag_display_shape(self.display, nutbolt, color='YELLOW', update=True)

                # elif self.component == "end bolt":
                #     pass
                # elif self.component == "intermediate bolt":
                #     pass

            elif self.connection == KEY_DISP_TENSION_WELDED:
                self.T = self.module_class()
                self.TObj = self.createTensionCAD()

                member = self.TObj.get_members_models()
                plate = self.TObj.get_plates_models()
                welds = self.TObj.get_welded_models()
                if self.component == "Model":  # Todo: change this into key
                    osdag_display_shape(self.display, member, update=True)
                    osdag_display_shape(self.display, plate, color='BLUE', update=True)
                    osdag_display_shape(self.display, welds, color='RED', update=True)

                # elif self.component == "end bolt":
                #     pass
                # elif self.component == "intermediate bolt":
                #     pass

    def call_3DModel(self, flag, module_class):  # Done

        self.module_class = module_class

        if self.mainmodule == "Shear Connection":

            A = self.module_class()

            # if self.connection == "Fin Plate":
            #     # A = FinPlateConnection()
            #     A = self.module_class()
            # elif self.connection == KEY_DISP_CLEATANGLE:
            #     A = CleatAngleConnection()
            # pass

            self.loc = A.connectivity

            if flag is True:

                if self.loc == "Column web-Beam web" or self.loc == "Column web-Beam flange":
                    self.connectivityObj = self.create3DColWebBeamWeb()

                elif self.loc == "Column flange-Beam web" or self.loc == "Column flange-Beam flange":
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

            elif self.connection == KEY_DISP_COLUMNCOVERPLATE or self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:
                if flag is True:

                    self.CPObj = self.createCCCoverPlateCAD()

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
        # TODO: changed for saving 3dmodels for different modules, add conditions for "connector",
        #         "cleatAngle", "seatedAngle" etc.
        if self.mainmodule == "Shear Connection":
            Obj = self.connectivityObj
        elif self.mainmodule == "Moment Connection":
            if self.connection == KEY_DISP_BEAMCOVERPLATE or self.connection == KEY_DISP_BEAMCOVERPLATEWELD:
                Obj = self.CPObj
            if self.connection == KEY_DISP_COLUMNCOVERPLATE or self.connection == KEY_DISP_COLUMNCOVERPLATEWELD:
                Obj = self.CPObj
            elif self.connection == KEY_DISP_BASE_PLATE:
                Obj = self.BPObj

            #Todo: add tension module

        if self.component == "Beam":
            # final_model = self.connectivityObj.get_beamModel()
            final_model = Obj.get_beamModel()

        elif self.component == "Column":
            # final_model = self.connectivityObj.columnModel
            final_model = Obj.columnModel

        elif self.component == "Plate":
            # cadlist = [self.connectivityObj.weldModelLeft,
            #            self.connectivityObj.weldModelRight,
            #            self.connectivityObj.plateModel] + self.connectivityObj.nut_bolt_array.get_models()
            cadlist = [Obj.weldModelLeft,
                       Obj.weldModelRight,
                       Obj.plateModel] + Obj.nut_bolt_array.get_models()
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        else:
            # cadlist = self.connectivityObj.get_models()
            cadlist = Obj.get_models()
            if self.connection == KEY_DISP_BASE_PLATE:
                return cadlist
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

        return final_model
