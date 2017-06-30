'''
Created on 18-Nov-2016

@author: deepa
'''

import os

import math
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere

from Connections.Shear.Finplate.colWebBeamWebConnectivity import ColWebBeamWeb as finColWebBeamWeb
from Connections.Shear.Endplate.colWebBeamWebConnectivity import ColWebBeamWeb as endColWebBeamWeb
from Connections.Shear.cleatAngle.colWebBeamWebConnectivity import ColWebBeamWeb as cleatColWebBeamWeb
from Connections.Shear.SeatedAngle.CAD_col_web_beam_web_connectivity import ColWebBeamWeb as seatColWebBeamWeb

from Connections.Shear.Finplate.beamWebBeamWebConnectivity import BeamWebBeamWeb as finBeamWebBeamWeb
from Connections.Shear.Endplate.beamWebBeamWebConnectivity import BeamWebBeamWeb as endBeamWebBeamWeb
from Connections.Shear.cleatAngle.beamWebBeamWebConnectivity import BeamWebBeamWeb as cleatBeamWebBeamWeb

from Connections.Shear.Finplate.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as finColFlangeBeamWeb
from Connections.Shear.Endplate.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as endColFlangeBeamWeb
from Connections.Shear.cleatAngle.colFlangeBeamWebConnectivity import ColFlangeBeamWeb as cleatColFlangeBeamWeb
from Connections.Shear.SeatedAngle.CAD_col_flange_beam_web_connectivity import ColFlangeBeamWeb as seatColFlangeBeamWeb

from Connections.Shear.Finplate.finPlateCalc import finConn
from Connections.Shear.Endplate.endPlateCalc import end_connection
from Connections.Shear.cleatAngle.cleatCalculation import cleat_connection
from Connections.Shear.SeatedAngle.seat_angle_calc import SeatAngleCalculation
from Connections.Component.filletweld import FilletWeld
from Connections.Component.plate import Plate
from Connections.Component.bolt import Bolt
from Connections.Component.nut import Nut
from Connections.Component.notch import Notch
from Connections.Component.ISection import ISection
from Connections.Component.angle import Angle
from Connections.Shear.Finplate.nutBoltPlacement import NutBoltArray as finNutBoltArray
from Connections.Shear.Endplate.nutBoltPlacement import NutBoltArray as endNutBoltArray
from Connections.Shear.cleatAngle.nutBoltPlacement import NutBoltArray as cleatNutBoltArray
from Connections.Shear.SeatedAngle.CAD_nut_bolt_placement import NutBoltArray as seatNutBoltArray
from utilities import osdag_display_shape

import OCC.V3d
from OCC.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_BLUE1
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM

from Connections.Shear.Finplate.drawing_2D import FinCommonData
from Connections.Shear.Endplate.drawing_2D import EndCommonData
from Connections.Shear.cleatAngle.drawing2D import cleatCommonData
from Connections.Shear.SeatedAngle.drawing_2D import SeatCommonData

from Connections.Shear.Finplate.reportGenerator import save_html as fin_save_html
from Connections.Shear.Endplate.reportGenerator import save_html as end_save_html
from Connections.Shear.cleatAngle.reportGenerator import save_html as cleat_save_html
from Connections.Shear.SeatedAngle.design_report_generator import ReportGenerator
# ----------------------------------------- from reportGenerator import save_html
import json
from Connections.Component.ModelUtils import *


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


    def __init__(self, uiObj, dictbeamdata, dictcoldata, dictangledata,
                 dicttopangledata, loc, component, bolt_R, bolt_T,
                 bolt_Ht, nut_T, display, folder, connection):

        self.uiObj = uiObj
        self.dictbeamdata = dictbeamdata
        self.dictcoldata = dictcoldata
        self.dictangledata = dictangledata

        self.dicttopangledata = dicttopangledata
        self.loc = loc
        self.component = component
        self.bolt_R = bolt_R
        self.bolt_T = bolt_T
        self.bolt_Ht = bolt_Ht

        self.nut_T = nut_T

        self.display = display
        self.connection = connection
        self.resultObj = self.call_calculation()

        self.connectivityObj = None
        self.folder = folder

    # ============================= FinCalculation ===========================================
    def call_calculation(self):  # Done
        if self.connection == "Finplate":
            outputs = finConn(self.uiObj)
        elif self.connection == "Endplate":
            outputs = end_connection(self.uiObj)
        elif self.connection == "cleatAngle":
            outputs = cleat_connection(self.uiObj)
        elif self.connection == "SeatedAngle":
            self.sa_calc_obj = SeatAngleCalculation()
            outputs = self.sa_calc_obj.seat_angle_connection(self.uiObj)
        else:
            pass
        return outputs

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



    def create3DBeamWebBeamWeb(self):
        '''self,uiObj,resultObj,dictbeamdata,dictcoldata):
        creating 3d cad model with beam web beam web

        '''
        ##### PRIMARY BEAM PARAMETERS #####
        pBeam_D = int(self.dictcoldata["D"])
        pBeam_B = int(self.dictcoldata["B"])
        pBeam_tw = float(self.dictcoldata["tw"])
        pBeam_T = float(self.dictcoldata["T"])
        pBeam_alpha = float(self.dictcoldata["FlangeSlope"])
        pBeam_R1 = float(self.dictcoldata["R1"])
        pBeam_R2 = float(self.dictcoldata["R2"])
        pBeam_length = 800.0  # This parameter as per view of 3D cad model

        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        column = ISection(B=pBeam_B, T=pBeam_T, D=pBeam_D, t=pBeam_tw,
                          R1=pBeam_R1, R2=pBeam_R2, alpha=pBeam_alpha,
                          length=pBeam_length, notchObj=None)

        ##### SECONDARY BEAM PARAMETERS ######

        sBeam_D = int(self.dictbeamdata["D"])
        sBeam_B = int(self.dictbeamdata["B"])
        sBeam_tw = float(self.dictbeamdata["tw"])
        sBeam_T = float(self.dictbeamdata["T"])
        sBeam_alpha = float(self.dictbeamdata["FlangeSlope"])
        sBeam_R1 = float(self.dictbeamdata["R1"])
        sBeam_R2 = float(self.dictbeamdata["R2"])
        #cleardist = float(self.uiObj['detailing']['gap'])

        if self.connection == "cleatAngle":
            cleat_length = self.resultObj['cleat']['height']
            cleat_thick = float(self.dictangledata["t"])
            cleat_legsizes = str(self.dictangledata["AXB"])
            angle_A = int(cleat_legsizes.split('x')[0])
            angle_B = int(cleat_legsizes.split('x')[1])
            angle_r1 = float(str(self.dictangledata["R1"]))
            angle_r2 = float(str(self.dictangledata["R2"]))
        else:
            plate_thick = float(self.uiObj['Plate']['Thickness (mm)'])
            fillet_length = float(self.resultObj['Plate']['height'])
            fillet_thickness = float(self.uiObj["Weld"]['Size (mm)'])
            plate_width = float(self.resultObj['Plate']['width'])

        bolt_dia = int(self.uiObj["Bolt"]["Diameter (mm)"])
        bolt_r = bolt_dia / 2
        bolt_R = self.bolt_R
        nut_R = bolt_R
        bolt_T = self.bolt_T
        bolt_Ht = self.bolt_Ht
        nut_T = self.nut_T
        nut_Ht = 12.2  # 150
        gap = self.uiObj['detailing']['gap']
        notch_height = self.get_notch_ht(pBeam_T, sBeam_T, pBeam_R1, sBeam_R1)
        notch_R1 = max([pBeam_R1, sBeam_R1, 10])

        if self.connection == "cleatAngle":
            angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick, R1=angle_r1, R2=angle_r2)
        else:
            plate = Plate(L=fillet_length, W=plate_width, T=plate_thick)
            Fweld1 = FilletWeld(L=fillet_length, b=fillet_thickness, h=fillet_thickness)

        # --Notch dimensions
        if self.connection == "Finplate":
            notchObj = Notch(R1=notch_R1,
                             height=notch_height,
                             #width= (pBeam_B/2.0 - (pBeam_tw/2.0 ))+ gap,
                             width= (pBeam_B/2.0 - (pBeam_tw/2.0  + gap))+ gap,
                             length=sBeam_B)

        elif self.connection == "Endplate":
            notchObj = Notch(R1=notch_R1, height=notch_height,
                             width=(pBeam_B / 2.0 - (pBeam_tw / 2.0 + plate_thick)) + plate_thick,
                             length=sBeam_B)

        elif self.connection == "cleatAngle":
            #((pBeam_B - (pBeam_tw + 40)) / 2.0 + 10)
            notchObj = Notch(R1=notch_R1,
                             height=notch_height,
                             width= (pBeam_B / 2.0 - (pBeam_tw / 2.0 + gap)) + gap,
                             length=sBeam_B)

        # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B=sBeam_B, T=sBeam_T, D=sBeam_D,
                        t=sBeam_tw, R1=sBeam_R1, R2=sBeam_R2,
                        alpha=sBeam_alpha, length=500, notchObj=notchObj)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == "Finplate":  # finBeamWebBeamWeb/endBeamWebBeamWeb
            nut_space = sBeam_tw + plate_thick + nut_T
            nutBoltArray = finNutBoltArray(self.resultObj, nut, bolt, nut_space)
            beamwebconn = finBeamWebBeamWeb(column, beam, notchObj, plate, Fweld1, nutBoltArray,gap)
            # column, beam, notch, plate, Fweld, nut_bolt_array
        elif self.connection == "Endplate":
            nut_space = sBeam_tw + plate_thick + nut_T
            nutBoltArray = endNutBoltArray(self.resultObj, nut, bolt, nut_space)
            beamwebconn = endBeamWebBeamWeb(column, beam, notchObj, Fweld1, plate, nutBoltArray)

        elif self.connection == "cleatAngle":
            nut_space = sBeam_tw + 2 * cleat_thick + nut_T
            cnut_space = pBeam_tw + cleat_thick + nut_T
            nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)
            beamwebconn = cleatBeamWebBeamWeb(column, beam, notchObj, angle, nut_bolt_array,gap)

        beamwebconn.create_3dmodel()

        return beamwebconn

    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web

        '''
        ##### BEAM PARAMETERS #####
        beam_D = int(self.dictbeamdata["D"])
        beam_B = int(self.dictbeamdata["B"])
        beam_tw = float(self.dictbeamdata["tw"])
        beam_T = float(self.dictbeamdata["T"])
        beam_alpha = float(self.dictbeamdata["FlangeSlope"])
        beam_R1 = float(self.dictbeamdata["R1"])
        beam_R2 = float(self.dictbeamdata["R2"])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                        R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                        length=beam_length, notchObj=None)

        ##### COLUMN PARAMETERS ######
        column_D = int(self.dictcoldata["D"])
        column_B = int(self.dictcoldata["B"])
        column_tw = float(self.dictcoldata["tw"])
        column_T = float(self.dictcoldata["T"])
        column_alpha = float(self.dictcoldata["FlangeSlope"])
        column_R1 = float(self.dictcoldata["R1"])
        column_R2 = float(self.dictcoldata["R2"])

        column = ISection(B=column_B, T=column_T, D=column_D,
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notchObj=None)
        #### PLATE,BOLT,ANGLE AND NUT PARAMETERS #####

        if self.connection == "cleatAngle":
            cleat_length = self.resultObj['cleat']['height']
            cleat_thick = float(self.dictangledata["t"])
            cleat_legsizes = str(self.dictangledata["AXB"])
            angle_A = int(cleat_legsizes.split('x')[0])
            angle_B = int(cleat_legsizes.split('x')[1])
            angle_r1 = float(str(self.dictangledata["R1"]))
            angle_r2 = float(str(self.dictangledata["R2"]))

        elif self.connection == 'SeatedAngle':
            seat_length = self.resultObj['SeatAngle']['Length (mm)']
            seat_thick = float(self.dictangledata["t"])
            seat_legsizes = str(self.dictangledata["AXB"])
            seatangle_A = int(seat_legsizes.split('x')[0])
            seatangle_B = int(seat_legsizes.split('x')[1])
            seatangle_r1 = float(str(self.dictangledata["R1"]))
            seatangle_r2 = float(str(self.dictangledata["R2"]))

            topangle_length = self.resultObj['SeatAngle']['Length (mm)']
            topangle_thick = float(self.dicttopangledata["t"])
            top_legsizes = str(self.dicttopangledata["AXB"])
            topangle_A = int(top_legsizes.split('x')[0])
            topangle_B = int(top_legsizes.split('x')[1])
            topangle_r1 = float(str(self.dicttopangledata["R1"]))
            topangle_r2 = float(str(self.dicttopangledata["R2"]))
        else:
            fillet_length = self.resultObj['Plate']['height']
            fillet_thickness = str(self.uiObj['Weld']['Size (mm)'])
            plate_width = self.resultObj['Plate']['width']
            plate_thick = str(self.uiObj['Plate']['Thickness (mm)'])

        bolt_dia = str(self.uiObj["Bolt"]["Diameter (mm)"])
        bolt_r = (float(bolt_dia) / 2)
        bolt_R = self.bolt_R
        nut_R = bolt_R
        bolt_T = self.bolt_T
        bolt_Ht = self.bolt_Ht
        nut_T = self.nut_T
        nut_Ht = 12.2  # 150
        gap = self.uiObj['detailing']['gap']

        if self.connection == "cleatAngle":
            angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick, R1=angle_r1, R2=angle_r2)
        elif self.connection == 'SeatedAngle':
            seatangle = Angle(L=seat_length, A=seatangle_A, B=seatangle_B, T=seat_thick, R1=seatangle_r1,
                              R2=seatangle_r2)
            topclipangle = Angle(L=topangle_length, A=topangle_A, B=topangle_B, T=topangle_thick, R1=topangle_r1,
                                 R2=topangle_r2)
        else:
            plate = Plate(L=fillet_length, W=plate_width, T=int(plate_thick))

            Fweld1 = FilletWeld(L=fillet_length, b=int(fillet_thickness), h=int(fillet_thickness))

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == "Finplate":  # finColWebBeamWeb
            nut_space = beam_tw + int(plate_thick) + nut_T
            nutBoltArray = finNutBoltArray(self.resultObj, nut, bolt, nut_space)
            colwebconn = finColWebBeamWeb(column, beam, Fweld1, plate, nutBoltArray,gap)

        elif self.connection == "Endplate":
            nut_space = column_tw + int(plate_thick) + nut_T
            nutBoltArray = endNutBoltArray(self.resultObj, nut, bolt, nut_space)
            colwebconn = endColWebBeamWeb(column, beam, Fweld1, plate, nutBoltArray)

        elif self.connection == "cleatAngle":
            nut_space = beam_tw + 2 * cleat_thick + nut_T
            cnut_space = column_tw + cleat_thick + nut_T

            nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)

            colwebconn = cleatColWebBeamWeb(column, beam, angle, nut_bolt_array,gap)
        else:
            snut_space = column_tw + seat_thick  + nut_T
            sbnut_space = beam_T + seat_thick + nut_T
            tnut_space = beam_T + topangle_thick + nut_T
            tbnut_space = column_tw + topangle_thick + nut_T

            nutBoltArray = seatNutBoltArray(self.resultObj, nut, bolt, snut_space, sbnut_space,tnut_space,tbnut_space)
            colwebconn = seatColWebBeamWeb(column, beam, seatangle, topclipangle, nutBoltArray,gap)

        colwebconn.create_3dmodel()
        return colwebconn

    def create3DColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection

        '''
        ##### BEAM PARAMETERS #####
        beam_D = int(self.dictbeamdata["D"])
        beam_B = int(self.dictbeamdata["B"])
        beam_tw = float(self.dictbeamdata["tw"])
        beam_T = float(self.dictbeamdata["T"])
        beam_alpha = float(self.dictbeamdata["FlangeSlope"])
        beam_R1 = float(self.dictbeamdata["R1"])
        beam_R2 = float(self.dictbeamdata["R2"])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                        R1=beam_R1, R2=beam_R2, alpha=beam_alpha, length=beam_length, notchObj=None)

        ##### COLUMN PARAMETERS ######

        column_D = int(self.dictcoldata["D"])
        column_B = int(self.dictcoldata["B"])
        column_tw = float(self.dictcoldata["tw"])
        column_T = float(self.dictcoldata["T"])
        column_alpha = float(self.dictcoldata["FlangeSlope"])
        column_R1 = float(self.dictcoldata["R1"])
        column_R2 = float(self.dictcoldata["R2"])

        column = ISection(B=column_B, T=column_T, D=column_D,
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notchObj=None)

        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        if self.connection == "cleatAngle":
            cleat_length = self.resultObj['cleat']['height']
            cleat_thick = float(self.dictangledata["t"])
            seat_legsizes = str(self.dictangledata["AXB"])
            angle_A = int(seat_legsizes.split('x')[0])
            angle_B = int(seat_legsizes.split('x')[1])
            angle_r1 = float(str(self.dictangledata["R1"]))
            angle_r2 = float(str(self.dictangledata["R2"]))

        elif self.connection == 'SeatedAngle':
            seat_length = self.resultObj['SeatAngle']['Length (mm)']
            seat_thick = float(self.dictangledata["t"])
            seat_legsizes = str(self.dictangledata["AXB"])
            seatangle_A = int(seat_legsizes.split('x')[0])
            seatangle_B = int(seat_legsizes.split('x')[1])
            seatangle_r1 = float(str(self.dictangledata["R1"]))
            seatangle_r2 = float(str(self.dictangledata["R2"]))

            topangle_length = self.resultObj['SeatAngle']['Length (mm)']
            topangle_thick = float(self.dicttopangledata["t"])
            top_legsizes = str(self.dicttopangledata["AXB"])
            topangle_A = int(top_legsizes.split('x')[0])
            topangle_B = int(top_legsizes.split('x')[1])
            topangle_r1 = float(str(self.dicttopangledata["R1"]))
            topangle_r2 = float(str(self.dicttopangledata["R2"]))

        else:
            fillet_length = self.resultObj['Plate']['height']
            fillet_thickness = str(self.uiObj['Weld']['Size (mm)'])
            # ---------------- fillet_thickness = self.resultObj['Weld']['thickness']
            plate_width = self.resultObj['Plate']['width']
            plate_thick = str(self.uiObj['Plate']['Thickness (mm)'])

        bolt_dia = str(self.uiObj["Bolt"]["Diameter (mm)"])
        bolt_r = (float(bolt_dia) / 2)
        bolt_R = self.bolt_R
        # bolt_R = bolt_r + 7
        nut_R = bolt_R
        bolt_T = self.bolt_T
        bolt_Ht = self.bolt_Ht
        nut_T = self.nut_T
        nut_Ht = 12.2  #
        gap = float(str(self.uiObj['detailing']['gap']))

        if self.connection == "cleatAngle":
            angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick, R1=angle_r1, R2=angle_r2)
            #bolt_len_required = float(bolt_T + 2 * (cleat_thick) + beam_tw + nut_T)
        elif self.connection == 'SeatedAngle':
            seatangle = Angle(L=seat_length, A=seatangle_A, B=seatangle_B, T=seat_thick, R1=seatangle_r1,
                              R2=seatangle_r2)
            #bolt_len_required = float(bolt_T + (seat_thick) + beam_tw + nut_T)
            topclipangle = Angle(L=topangle_length, A=topangle_A, B=topangle_B, T=topangle_thick, R1=topangle_r1,
                                 R2=topangle_r2)
        else:
            # plate = Plate(L= 300,W =100, T = 10)
            plate = Plate(L=fillet_length, W=plate_width, T=int(plate_thick))

            # Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
            Fweld1 = FilletWeld(L=fillet_length, b=int(fillet_thickness), h=int(fillet_thickness))

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        if self.connection == "Finplate":
            nut_space = beam_tw + int(plate_thick) + nut_T
            nutBoltArray = finNutBoltArray(self.resultObj, nut, bolt, nut_space)  # finColFlangeBeamWeb
            colflangeconn = finColFlangeBeamWeb(column, beam, Fweld1, plate, nutBoltArray, gap)

        elif self.connection == "Endplate":
            nut_space = column_T + int(plate_thick) + nut_T
            nutBoltArray = endNutBoltArray(self.resultObj, nut, bolt, nut_space)
            colflangeconn = endColFlangeBeamWeb(column, beam, Fweld1, plate, nutBoltArray)

        elif self.connection == "cleatAngle":
            nut_space = beam_tw + 2 * cleat_thick + nut_T
            cnut_space = column_T + cleat_thick + nut_T
            nut_bolt_array = cleatNutBoltArray(self.resultObj, nut, bolt, nut_space, cnut_space)
            colflangeconn = cleatColFlangeBeamWeb(column, beam, angle, nut_bolt_array,gap)
        else:
            snut_space = column_T + seat_thick + nut_T
            sbnut_space = beam_T + seat_thick + nut_T
            tnut_space = beam_T + topangle_thick + nut_T
            tbnut_space = column_T + topangle_thick + nut_T

            nutBoltArray = seatNutBoltArray(self.resultObj, nut, bolt, snut_space, sbnut_space, tnut_space, tbnut_space)
            colflangeconn = seatColFlangeBeamWeb(column, beam, seatangle, topclipangle, nutBoltArray,gap)

        colflangeconn.create_3dmodel()
        return colflangeconn

    def display_3DModel(self, component,bgcolor):

        self.component = component

        self.display.EraseAll()
        self.display.View_Iso()
        self.display.FitAll()

        self.display.DisableAntiAliasing()
        if bgcolor =="gradient_bg":

            self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
        else:
            self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)

        if self.loc == "Column flange-Beam web" and self.connection == "Finplate":
            self.display.View.SetProj(OCC.V3d.V3d_XnegYnegZpos)
        elif self.loc == "Column flange-Beam flange" and self.connection == "SeatedAngle":
            self.display.View.SetProj(OCC.V3d.V3d_XnegYnegZpos)
        elif self.loc == "Column web-Beam flange" and self.connection == "SeatedAngle":
            self.display.View.SetProj(OCC.V3d.V3d_XposYnegZpos)

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

    def call_saveOutputs(self):  # Done
        return self.call_calculation(self.uiObj)

    def call2D_Drawing(self, view, fileName, folder):  # Rename function with call_view_images()
        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        if view == "All":

            self.callDesired_View(fileName, view, folder)
            # self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)
            #
            # data = os.path.join(str(folder), "images_html", "3D_Model.png")
            #
            # self.display.ExportToImage(data)
            #
            # # self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
            # self.display.View_Iso()
            # self.display.FitAll()

        else:

            f = open(fileName, 'w')

            self.callDesired_View(fileName, view, folder)
            f.close()

    def callDesired_View(self, fileName, view, folder):

        if self.connection == "Finplate":
            finCommonObj = FinCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata, folder)
            finCommonObj.saveToSvg(str(fileName), view)
        elif self.connection == "Endplate":
            endCommonObj = EndCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata, folder)
            endCommonObj.save_to_svg(str(fileName), view)
        elif self.connection == "cleatAngle":
            cleatCommonObj = cleatCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata,
                                             self.dictangledata, folder)
            cleatCommonObj.save_to_svg(str(fileName), view)
        else:
            seatCommonObj = SeatCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata,
                                           self.dictangledata, self.dicttopangledata, folder)
            seatCommonObj.save_to_svg(str(fileName), view)

    def call_saveMessages(self):  # Done

        if self.connection == "Finplate":
            fileName = os.path.join("Connections", "Shear", "Finplate", "fin.log")

        elif self.connection == "Endplate":
            fileName = os.path.join("Connections", "Shear", "Endplate", "end.log")

        elif self.connection == "cleatAngle":
            fileName = os.path.join("Connections", "Shear", "cleatAngle", "cleat.log")

        else:
            fileName = os.path.join("Connections", "Shear", "SeatedAngle", "seatangle.log")

        return fileName

    def call_designReport(self, htmlfilename, profileSummary):

        fileName = str(htmlfilename)

        if self.connection == "Finplate":
            fin_save_html(self.resultObj, self.uiObj, self.dictbeamdata, self.dictcoldata, profileSummary,
                          htmlfilename, self.folder)
        elif self.connection == "Endplate":
            end_save_html(self.resultObj, self.uiObj, self.dictbeamdata, self.dictcoldata, profileSummary,
                          htmlfilename, self.folder)
        elif self.connection == "cleatAngle":
            cleat_save_html(self.resultObj,self.uiObj,self.dictbeamdata,self.dictcoldata,self.dictangledata,
                            profileSummary,htmlfilename, self.folder)
        else:
            self.sa_report = ReportGenerator(self.sa_calc_obj)
            self.sa_report.save_html(profileSummary,htmlfilename,self.folder)

    def load_userProfile(self):
        # TODO load_userProfile - deepa
        pass


    def save_userProfile(self, profile_summary, fileName):
        # TODO save_userProfile - deepa
        filename = str(fileName)

        infile = open(filename, 'w')
        json.dump(profile_summary, infile)
        infile.close()
        pass

    def save_CADimages(self):  # png,jpg and tiff
        # TODO save_CADimages - deepa
        pass
