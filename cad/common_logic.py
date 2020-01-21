'''
Created on 18-Nov-2016

@author: deepa
'''

import os

import math
# from utils.common.component import Bolt,Beam,Section,Angle,Plate,Nut,Column,Weld
from cad.items.notch import Notch
from cad.items.bolt import Bolt
from cad.items.nut import Nut
from cad.items.plate import Plate
from cad.items.ISection import ISection
from cad.items.filletweld import FilletWeld
from cad.beamWebBeamWebConnectivity import BeamWebBeamWeb as FinBeamWebBeamWeb
from cad.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as FinColFlangeBeamWeb
from cad.colWebBeamWebConnectivity import ColWebBeamWeb as FinColWebBeamWeb
from cad.nutBoltPlacement import NutBoltArray as finNutBoltArray
from design_type.connection.fin_plate_connection import FinPlateConnection
from utilities import osdag_display_shape
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

from cad.nutBoltPlacement import NutBoltArray
from design_type.connection import cleat_angle_connection
from design_type.connection import seated_angle_connection
from design_type.connection import end_plate_connection

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
import json
from cad.items.ModelUtils import *


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
    def __init__(self, display, folder, connection):

        # self.bolt = Bolt
        # self.beam = Beam
        # # self.section = Section
        # self.angle = Angle
        # self.plate = Plate
        # self.nut = Nut
        # self.column = Column
        # self.weld = Weld

        self.display = display
        self.connection = connection
        # self.resultObj = self.call_calculation()

        self.connectivityObj = None
        self.folder = folder

    # ============================= FinCalculation ===========================================
    # def call_calculation(self):  # Done
    #     if self.connection == "Finplate":
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
        # ##### PRIMARY BEAM PARAMETERS #####
        # pBeam_D = int(self.dictcoldata["D"])
        # pBeam_B = int(self.dictcoldata["B"])
        # pBeam_tw = float(self.dictcoldata["tw"])
        # pBeam_T = float(self.dictcoldata["T"])
        # pBeam_alpha = float(self.dictcoldata["FlangeSlope"])
        # pBeam_R1 = float(self.dictcoldata["R1"])
        # pBeam_R2 = float(self.dictcoldata["R2"])
        # pBeam_length = 800.0  # This parameter as per view of 3D cad model
        if self.connection == "Finplate":
            A = FinPlateConnection()
        else:
            pass


        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        supporting = ISection(B=A.supporting_section.flange_width , T=A.supporting_section.flange_thickness, D=A.supporting_section.depth, t=A.supporting_section.web_thickness,
                          R1=A.supporting_section.root_radius, R2=A.supporting_section.toe_radius, alpha=A.supporting_section.flange_slope,
                          length=1000, notchObj=None)

        ##### SECONDARY BEAM PARAMETERS ######

        # supported = ISection(B=A.supported_section.flange_width, T=A.supported_section.flange_thickness,
        #                       D=A.supported_section.depth, t=A.supported_section.web_thickness,
        #                       R1=A.supported_section.root_radius, R2=A.supported_section.toe_radius,
        #                       alpha=A.supported_section.flange_slope,
        #                       length=1000, notchObj=None)

        # sBeam_D = int(self.dictbeamdata["D"])
        # sBeam_B = int(self.dictbeamdata["B"])
        # sBeam_tw = float(self.dictbeamdata["tw"])
        # sBeam_T = float(self.dictbeamdata["T"])
        # sBeam_alpha = float(self.dictbeamdata["FlangeSlope"])
        # sBeam_R1 = float(self.dictbeamdata["R1"])
        # sBeam_R2 = float(self.dictbeamdata["R2"])
        # #cleardist = float(self.uiObj['detailing']['gap'])
        #
        # if self.connection == "cleatAngle":
        #     cleat_length = self.resultObj['cleat']['height']
        #     cleat_thick = float(self.dictangledata["t"])
        #     cleat_legsizes = str(self.dictangledata["AXB"])
        #     angle_A = int(cleat_legsizes.split('x')[0])
        #     angle_B = int(cleat_legsizes.split('x')[1])
        #     angle_r1 = float(str(self.dictangledata["R1"]))
        #     angle_r2 = float(str(self.dictangledata["R2"]))
        # else:
        #     plate_thick = float(self.uiObj['Plate']['Thickness (mm)'])
        #     fillet_length = float(self.resultObj['Plate']['height'])
        #     fillet_thickness = float(self.uiObj["Weld"]['Size (mm)'])
        #     plate_width = float(self.resultObj['Plate']['width'])

        bolt_dia = A.bolt.bolt_diameter_provided
        bolt_r = bolt_dia / 2.0
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2.0
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = bolt_dia
        gap = A.plate.gap
        notch_height = self.get_notch_ht(A.supporting_section.flange_width, A.supporting_section.flange_thickness, A.supported_section.flange_thickness, A.supported_section.root_radius)
        notch_R1 = max([A.supporting_section.root_radius, A.supported_section.root_radius, 10])

        if self.connection == "cleatAngle":
            pass
            # angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick, R1=angle_r1, R2=angle_r2)
        else:
            plate = Plate(L=A.plate.length, W=A.plate.height, T=A.plate.thickness_provided)

        Fweld1 = FilletWeld(L=A.weld.length, b=A.weld.size, h=A.weld.size)

        # --Notch dimensions
        if self.connection == "Finplate":
            notchObj = Notch(R1=notch_R1,
                             height=notch_height,
                             #width= (pBeam_B/2.0 - (pBeam_tw/2.0 ))+ gap,
                             width= (A.supporting_section.flange_width/2.0 - (A.supporting_section.web_thickness/2.0  + gap))+ gap,
                             length=A.supported_section.flange_width)

        # elif self.connection == "Endplate":
        #     notchObj = Notch(R1=notch_R1, height=notch_height,
        #                      width=(pBeam_B / 2.0 - (pBeam_tw / 2.0 + plate_thick)) + plate_thick,
        #                      length=sBeam_B)
        #
        # elif self.connection == "cleatAngle":
        #     #((pBeam_B - (pBeam_tw + 40)) / 2.0 + 10)
        #     notchObj = Notch(R1=notch_R1,
        #                      height=notch_height,
        #                      width= (pBeam_B / 2.0 - (pBeam_tw / 2.0 + gap)) + gap,
        #                      length=sBeam_B)

        # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        supported = ISection(B=A.supported_section.flange_width, T=A.supported_section.flange_thickness, D=A.supported_section.depth,
                        t=A.supported_section.web_thickness, R1=A.supported_section.root_radius, R2=A.supported_section.toe_radius,
                        alpha=A.supported_section.flange_slope, length=500, notchObj=notchObj)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == "Finplate":  # finBeamWebBeamWeb/endBeamWebBeamWeb
            nut_space = A.supported_section.web_thickness + A.plate.thickness_provided + nut_T
            nutBoltArray = finNutBoltArray(A.bolt, nut, bolt, nut_space)
            beamwebconn = FinBeamWebBeamWeb(supporting, supported, notchObj, plate, Fweld1, nutBoltArray, gap)
            # column, beam, notch, plate, Fweld, nut_bolt_array
        # elif self.connection == "Endplate":
        #     nut_space = sBeam_tw + plate_thick + nut_T
        #     nutBoltArray = endNutBoltArray(self.resultObj, nut, bolt, nut_space)
        #     beamwebconn = endBeamWebBeamWeb(column, beam, notchObj, Fweld1, plate, nutBoltArray)
        #
        # elif self.connection == "cleatAngle":
        #     nut_space = sBeam_tw + 2 * cleat_thick + nut_T
        #     cnut_space = pBeam_tw + cleat_thick + nut_T
        #     nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)
        #     beamwebconn = cleatBeamWebBeamWeb(column, beam, notchObj, angle, nut_bolt_array,gap)

        beamwebconn.create_3dmodel()

        return beamwebconn

    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web

        '''

        if self.connection == "Finplate":
            A = FinPlateConnection()
        else:
            pass


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

        bolt_dia = A.bolt.bolt_diameter_provided
        bolt_r = bolt_dia / 2.0
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2.0
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = bolt_dia
        gap = A.plate.gap

        if self.connection == "cleatAngle":
            pass
            # angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick, R1=angle_r1, R2=angle_r2)
        elif self.connection == 'SeatedAngle':
            pass
            # seatangle = Angle(L=seat_length, A=seatangle_A, B=seatangle_B, T=seat_thick, R1=seatangle_r1,
            #                   R2=seatangle_r2)
            # topclipangle = Angle(L=topangle_length, A=topangle_A, B=topangle_B, T=topangle_thick, R1=topangle_r1,
            #                      R2=topangle_r2)
        else:
            plate = Plate(L=A.plate.length, W=A.plate.height, T=A.plate.thickness_provided)

        Fweld1 = FilletWeld(L=A.weld.length, b=A.weld.size, h=A.weld.size)

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == "Finplate":  # finColWebBeamWeb
            nut_space = A.supported_section.web_thickness + int(A.plate.thickness_provided) + nut_T
            nutBoltArray = finNutBoltArray(A.bolt, nut, bolt, nut_space)
            colwebconn = FinColWebBeamWeb(supporting, supported, Fweld1, plate, nutBoltArray,gap)

        # elif self.connection == "Endplate":
        #     nut_space = column_tw + int(plate_thick) + nut_T
        #     nutBoltArray = endNutBoltArray(A,bolt, nut, bolt, nut_space)
        #     colwebconn = endColWebBeamWeb(A.supporting_section, A.supported_section, A.weld, A.plate, nutBoltArray)
        #
        # elif self.connection == "cleatAngle":
        #     nut_space = beam_tw + 2 * cleat_thick + nut_T
        #     cnut_space = column_tw + cleat_thick + nut_T
        #
        #     nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)
        #
        #     colwebconn = cleatColWebBeamWeb(column, beam, angle, nut_bolt_array,gap)
        else:
            pass
            # snut_space = column_tw + seat_thick  + nut_T
            # sbnut_space = beam_T + seat_thick + nut_T
            # tnut_space = beam_T + topangle_thick + nut_T
            # tbnut_space = column_tw + topangle_thick + nut_T
            #
            # nutBoltArray = seatNutBoltArray(self.resultObj, nut, bolt, snut_space, sbnut_space,tnut_space,tbnut_space)
            # colwebconn = seatColWebBeamWeb(column, beam, seatangle, topclipangle, nutBoltArray,gap)

        colwebconn.create_3dmodel()
        return colwebconn

    def create3DColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection

        '''
        ##### BEAM PARAMETERS #####
        # beam_D = int(self.dictbeamdata["D"])
        # beam_B = int(self.dictbeamdata["B"])
        # beam_tw = float(self.dictbeamdata["tw"])
        # beam_T = float(self.dictbeamdata["T"])
        # beam_alpha = float(self.dictbeamdata["FlangeSlope"])
        # beam_R1 = float(self.dictbeamdata["R1"])
        # beam_R2 = float(self.dictbeamdata["R2"])
        # beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        # beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
        #                 R1=beam_R1, R2=beam_R2, alpha=beam_alpha, length=beam_length, notchObj=None)
        if self.connection == "Finplate":
            A = FinPlateConnection()
        else:
            pass

        supported = ISection(B=A.supported_section.flange_width, T=A.supported_section.flange_thickness,
                             D=A.supported_section.depth,
                             t=A.supported_section.web_thickness, R1=A.supported_section.root_radius,
                             R2=A.supported_section.toe_radius,
                             alpha=A.supported_section.flange_slope, length=500, notchObj=None)

        ##### COLUMN PARAMETERS ######

        # column_D = int(self.dictcoldata["D"])
        # column_B = int(self.dictcoldata["B"])
        # column_tw = float(self.dictcoldata["tw"])
        # column_T = float(self.dictcoldata["T"])
        # column_alpha = float(self.dictcoldata["FlangeSlope"])
        # column_R1 = float(self.dictcoldata["R1"])
        # column_R2 = float(self.dictcoldata["R2"])

        # column = ISection(B=column_B, T=column_T, D=column_D,
        #                   t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notchObj=None)

        supporting = ISection(B=A.supporting_section.flange_width, T=A.supporting_section.flange_thickness,
                              D=A.supporting_section.depth, t=A.supporting_section.web_thickness,
                              R1=A.supporting_section.root_radius, R2=A.supporting_section.toe_radius,
                              alpha=A.supporting_section.flange_slope,
                              length=1000, notchObj=None)
        #
        # #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        # if self.connection == "cleatAngle":
        #     cleat_length = self.resultObj['cleat']['height']
        #     cleat_thick = float(self.dictangledata["t"])
        #     seat_legsizes = str(self.dictangledata["AXB"])
        #     angle_A = int(seat_legsizes.split('x')[0])
        #     angle_B = int(seat_legsizes.split('x')[1])
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
        #
        # else:
        #     fillet_length = self.resultObj['Plate']['height']
        #     fillet_thickness = str(self.uiObj['Weld']['Size (mm)'])
        #     # ---------------- fillet_thickness = self.resultObj['Weld']['thickness']
        #     plate_width = self.resultObj['Plate']['width']
        #     plate_thick = str(self.uiObj['Plate']['Thickness (mm)'])

        # bolt_dia = str(self.uiObj["Bolt"]["Diameter (mm)"])
        # bolt_r = (float(bolt_dia) / 2)
        # bolt_R = self.bolt_R
        # # bolt_R = bolt_r + 7
        # nut_R = bolt_R
        # bolt_T = self.bolt_T
        # bolt_Ht = self.bolt_Ht
        # nut_T = self.nut_T
        # nut_Ht = 12.2  #
        # gap = float(str(self.uiObj['detailing']['gap']))

        bolt_dia = A.bolt.bolt_diameter_provided
        bolt_r = bolt_dia / 2.0
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2.0
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = bolt_dia
        gap = A.plate.gap
        #
        if self.connection == "cleatAngle":
            pass
            # angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick, R1=angle_r1, R2=angle_r2)
            #bolt_len_required = float(bolt_T + 2 * (cleat_thick) + beam_tw + nut_T)
        elif self.connection == 'SeatedAngle':
            pass
            # seatangle = Angle(L=seat_length, A=seatangle_A, B=seatangle_B, T=seat_thick, R1=seatangle_r1,
                              # R2=seatangle_r2)
            #bolt_len_required = float(bolt_T + (seat_thick) + beam_tw + nut_T)
            # topclipangle = Angle(L=topangle_length, A=topangle_A, B=topangle_B, T=topangle_thick, R1=topangle_r1,
            #                      R2=topangle_r2)
        else:
            # plate = Plate(L= 300,W =100, T = 10)
            plate = Plate(L=A.plate.length, W=A.plate.height, T=A.plate.thickness_provided)

            # Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        Fweld1 = FilletWeld(L=A.weld.length, b=A.weld.size, h=A.weld.size)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == "Finplate":
            nut_space = A.supported_section.web_thickness+ int(A.plate.thickness_provided) + nut_T
            # nutBoltArray = finNutBoltArray(A, nut, bolt, nut_space)  # finColFlangeBeamWeb
            # colflangeconn = finColFlangeBeamWeb(column, beam, Fweld1, plate, nutBoltArray, gap)

            nutBoltArray = finNutBoltArray(A.bolt, A.plate, nut, bolt, nut_space)
            colflangeconn = FinColFlangeBeamWeb(supporting, supported, Fweld1, plate, nutBoltArray,gap)
        else:
            pass
        # elif self.connection == "Endplate":
        #     nut_space = column_T + int(plate_thick) + nut_T
        #     nutBoltArray = endNutBoltArray(self.resultObj, nut, bolt, nut_space)
        #     colflangeconn = endColFlangeBeamWeb(column, beam, Fweld1, plate, nutBoltArray)
        #
        # elif self.connection == "cleatAngle":
        #     nut_space = beam_tw + 2 * cleat_thick + nut_T
        #     cnut_space = column_T + cleat_thick + nut_T
        #     nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)
        #     colflangeconn = cleatColFlangeBeamWeb(column, beam, angle, nut_bolt_array,gap)
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

    def display_3DModel(self, component,bgcolor):

        self.component = component

        self.display.EraseAll()
        self.display.View_Iso()
        self.display.FitAll()

        self.display.DisableAntiAliasing()
        self.loc = FinPlateConnection().connectivity


        if bgcolor =="gradient_bg":

            self.display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])
        else:
            self.display.set_bg_gradient_color([255, 255, 255], [255, 255, 255])

        if self.loc == "Column flange-Beam web" and self.connection == "Finplate":
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
            if self.connection == "Finplate" or self.connection == "Endplate":
                osdag_display_shape(self.display, self.connectivityObj.weldModelLeft, color='red', update=True)
                osdag_display_shape(self.display, self.connectivityObj.weldModelRight, color='red', update=True)
                osdag_display_shape(self.display, self.connectivityObj.plateModel, color=Quantity_NOC_BLUE1,
                                    update=True)

            elif self.connection == "cleatAngle":
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

    def call_3DModel(self, flag):  # Done

        self.loc = FinPlateConnection().connectivity

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

    # def call_saveOutputs(self):  # Done
    #     return self.call_calculation(self.uiObj)
    #
    # def call2D_Drawing(self, view, fileName, folder):  # Rename function with call_view_images()
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
    #     if self.connection == "Finplate":
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
    #     if self.connection == "Finplate":
    #         fileName = os.path.join("Connections", "Shear", "Finplate", "fin.log")
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
    #     if self.connection == "Finplate":
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


        if self.component == "Beam":
            final_model = self.connectivityObj.get_beamModel()

        elif self.component == "Column":
            final_model = self.connectivityObj.columnModel

        elif self.component == "Plate":
            cadlist = [self.connectivityObj.weldModelLeft,
                       self.connectivityObj.weldModelRight,
                       self.connectivityObj.plateModel] + self.connectivityObj.nut_bolt_array.get_models()
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        else:
            cadlist = self.connectivityObj.get_models()
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

        return final_model