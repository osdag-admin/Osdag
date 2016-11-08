'''
Created on 14-Oct-2016

@author: deepa
'''

import os
from PyQt4.QtCore import QString
from col_web_beam_web_connectivity import ColWebBeamWeb
#from beamWebBeamWebConnectivity import BeamWebBeamWeb
from col_flange_beam_web_connectivity import ColFlangeBeamWeb
from seat_angle_calc import SeatAngleCalculation
from bolt import Bolt
from nut import Nut
from notch import Notch
from ISection import ISection
from angle import Angle
from nut_bolt_placement import NutBoltArray

from utilities import osdagDisplayShape

import OCC.V3d
from OCC.Quantity import Quantity_NOC_SADDLEBROWN
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from drawing_2D import SeatCommonData
from report_generator import ReportGenerator
import json


class CommonDesignLogic(object):
    #--------------------------------------------- def __init__(self, **kwargs):
        #-------------------------------------------- self.uiObj = kwargs[uiObj]
        #------------------------------ self.dictbeamdata = kwargs[dictbeamdata]
        #-------------------------------- self.dictcoldata = kwargs[dictcoldata]
        #------------------------------------------------ self.loc = kwargs[loc]
        #------------------------------------ self.component = kwargs[component]
        #------------------------------------------ self.bolt_R = kwargs[bolt_R]
        #------------------------------------------ self.bolt_T = kwargs[bolt_T]
        #---------------------------------------- self.bolt_Ht = kwargs[bolt_Ht]
        #-------------------------------------------- self.nut_T = kwargs[nut_T]
        #----------------------------------------- self.display =kwargs[display]
        #--------------------------- self.resultObj = self.call_finCalculation()
        #------------------------------------------- self.connectivityObj = None

    def __init__(self, uiObj, dictbeamdata, dictcoldata, dictangledata, loc, component, bolt_R, bolt_T, bolt_Ht, nut_T, display, folder):
                    # self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5], self.alist[6], self.alist[7], self.alist[8], self.alist[9], self.display, self.folder, base, base_front, base_side, base_top)
        self.uiObj = uiObj
        self.dictbeamdata = dictbeamdata
        self.dictcoldata = dictcoldata
        self.dictangledata = dictangledata
        self.loc = loc
        self.component = component
        self.bolt_R = bolt_R
        self.bolt_T = bolt_T
        self.bolt_Ht = bolt_Ht
        self.nut_T = nut_T
        self.display = display
        self.resultObj = self.call_finCalculation()
        self.connectivityObj = None
        self.folder = folder
        self.sa_calc_object = None

    #============================= Seated angle calculation ===========================================

    def call_finCalculation(self):  # Done
        self.sa_calc_object = SeatAngleCalculation()
        outputs = self.sa_calc_object.seat_angle_connection(self.uiObj)
        return outputs

    #=========================================================================================

    #----------------------------------------- def create3DBeamWebBeamWeb(self):
        #-------------------- '''self,uiObj,resultObj,dictbeamdata,dictcoldata):
        #-------------------------- creating 3d cad model with beam web beam web
        #------------------------------------------------------------------- '''
        #----------------------------------- ##### PRIMARY BEAM PARAMETERS #####
        #------------------------- pBeam_D = int(self.dictcoldata[QString("D")])
        #------------------------- pBeam_B = int(self.dictcoldata[QString("B")])
        #--------------------- pBeam_tw = float(self.dictcoldata[QString("tw")])
        #----------------------- pBeam_T = float(self.dictcoldata[QString("T")])
        #--------- pBeam_alpha = float(self.dictcoldata[QString("FlangeSlope")])
        #--------------------- pBeam_R1 = float(self.dictcoldata[QString("R1")])
        #--------------------- pBeam_R2 = float(self.dictcoldata[QString("R2")])
        #---- pBeam_length = 800.0  # This parameter as per view of 3D cad model
#------------------------------------------------------------------------------ 
        # # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        #-------- column = ISection(B=pBeam_B, T=pBeam_T, D=pBeam_D, t=pBeam_tw,
                          #-------- R1=pBeam_R1, R2=pBeam_R2, alpha=pBeam_alpha,
                          #----------------- length=pBeam_length, notchObj=None)
#------------------------------------------------------------------------------ 
        #-------------------------------- ##### SECONDARY BEAM PARAMETERS ######
#------------------------------------------------------------------------------ 
        #------------------------ sBeam_D = int(self.dictbeamdata[QString("D")])
        #------------------------ sBeam_B = int(self.dictbeamdata[QString("B")])
        #-------------------- sBeam_tw = float(self.dictbeamdata[QString("tw")])
        #---------------------- sBeam_T = float(self.dictbeamdata[QString("T")])
        #-------- sBeam_alpha = float(self.dictbeamdata[QString("FlangeSlope")])
        #-------------------- sBeam_R1 = float(self.dictbeamdata[QString("R1")])
        #-------------------- sBeam_R2 = float(self.dictbeamdata[QString("R2")])
#------------------------------------------------------------------------------ 
        #-------------------------------------------------- # --Notch dimensions
        # notchObj = Notch(R1=pBeam_R1, height=(pBeam_T + pBeam_R1), width=((pBeam_B - (pBeam_tw + 40)) / 2.0 + 10), length=sBeam_B)
        # # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        #---------------------- beam = ISection(B=sBeam_B, T=sBeam_T, D=sBeam_D,
                        #----------------- t=sBeam_tw, R1=sBeam_R1, R2=sBeam_R2,
                        #----- alpha=sBeam_alpha, length=500, notchObj=notchObj)
#------------------------------------------------------------------------------ 
        #------------------------- #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
#------------------------------------------------------------------------------ 
        #--------------------- fillet_length = self.resultObj['Plate']['height']
        #---------------- fillet_thickness = self.resultObj['Weld']['thickness']
        #------------------------ plate_width = self.resultObj['Plate']['width']
        #------------------- plate_thick = self.uiObj['Plate']['Thickness (mm)']
        #------------------------ bolt_dia = self.uiObj["Bolt"]["Diameter (mm)"]
        #------------------------------------------------- bolt_r = bolt_dia / 2
        #-------------------------------------------------- bolt_R = self.bolt_R
        #-------------------------------------------------------- nut_R = bolt_R
        #-------------------------------------------------- bolt_T = self.bolt_T
        #------------------------------------------------ bolt_Ht = self.bolt_Ht
        #---------------------------------------------------- nut_T = self.nut_T
        #-------------------------------------------------- nut_Ht = 12.2  # 150
#------------------------------------------------------------------------------ 
        #-------------- # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        #------------------ bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)
#------------------------------------------------------------------------------ 
        # # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        #---------------- nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)
#------------------------------------------------------------------------------ 
        #---------------------------------- gap = sBeam_tw + plate_thick + nut_T
#------------------------------------------------------------------------------ 
        #----------- nutBoltArray = NutBoltArray(self.resultObj, nut, bolt, gap)
        # beamwebconn = BeamWebBeamWeb(column, beam, notchObj, plate, Fweld1, nutBoltArray)
        #------------------------------------------ beamwebconn.create_3dmodel()
#------------------------------------------------------------------------------ 
        #---------------------------------------------------- return beamwebconn

    #=========================================================================================

    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web
        '''
        ##### BEAM PARAMETERS #####
        beam_D = int(self.dictbeamdata[QString("D")])
        beam_B = int(self.dictbeamdata[QString("B")])
        beam_tw = float(self.dictbeamdata[QString("tw")])
        beam_T = float(self.dictbeamdata[QString("T")])
        beam_alpha = float(self.dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(self.dictbeamdata[QString("R1")])
        beam_R2 = float(self.dictbeamdata[QString("R2")])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                        R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                        length=beam_length, notchObj=None)

        ##### COLUMN PARAMETERS ######

        column_D = int(self.dictcoldata[QString("D")])
        column_B = int(self.dictcoldata[QString("B")])
        column_tw = float(self.dictcoldata[QString("tw")])
        column_T = float(self.dictcoldata[QString("T")])
        column_alpha = float(self.dictcoldata[QString("FlangeSlope")])
        column_R1 = float(self.dictcoldata[QString("R1")])
        column_R2 = float(self.dictcoldata[QString("R2")])

        # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B=column_B, T=column_T, D=column_D,
                           t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notchObj=None)
        ##### ANGLE PARAMETERS ######

        angle_l = self.resultObj['SeatAngle']["Length (mm)"]
        angle_a = int(self.dictangledata[QString("A")])
        angle_b = int(self.dictangledata[QString("B")])
        angle_t = float(self.dictangledata[QString("t")])
        angle_r1 = float(self.dictangledata[QString("R1")])
        angle_r2 = float(self.dictangledata[QString("R2")])

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        angle = Angle(L=angle_l, A=angle_a, B=angle_b, T=angle_t, R1=angle_r1, R2=angle_r2)
        # TODO add topclipangle field  in user inputs(changes in .ui file)
        topclipangle = Angle(L=angle_l, A=angle_a, B=angle_b, T=angle_t, R1=angle_r1, R2=angle_r2)
        bolt_dia = self.uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = self.bolt_R
        nut_R = bolt_R
        bolt_T = self.bolt_T 
        bolt_Ht = self.bolt_Ht
        nut_T = self.nut_T
        nut_Ht = 12.2 #150

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)
        
        gap = column_tw + angle_t + nut_T
        bgap = beam_T + angle_t + nut_T

        nutBoltArray = NutBoltArray(self.resultObj, nut, bolt, gap, bgap)

        colwebconn = ColWebBeamWeb(column, beam, angle, topclipangle, nutBoltArray)
        colwebconn.create_3dmodel()

        return colwebconn
    #=========================================================================================

    def create3DColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection
        '''
        ##### BEAM PARAMETERS #####
        beam_D = int(self.dictbeamdata[QString("D")])
        beam_B = int(self.dictbeamdata[QString("B")])
        beam_tw = float(self.dictbeamdata[QString("tw")])
        beam_T = float(self.dictbeamdata[QString("T")])
        beam_alpha = float(self.dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(self.dictbeamdata[QString("R1")])
        beam_R2 = float(self.dictbeamdata[QString("R2")])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                        R1=beam_R1, R2=beam_R2, alpha=beam_alpha, length=beam_length, notchObj=None)

        ##### COLUMN PARAMETERS ######

        column_D = int(self.dictcoldata[QString("D")])
        column_B = int(self.dictcoldata[QString("B")])
        column_tw = float(self.dictcoldata[QString("tw")])
        column_T = float(self.dictcoldata[QString("T")])
        column_alpha = float(self.dictcoldata[QString("FlangeSlope")])
        column_R1 = float(self.dictcoldata[QString("R1")])
        column_R2 = float(self.dictcoldata[QString("R2")])

        # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B=column_B, T=column_T, D=column_D,
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notchObj=None)

        ##### ANGLE PARAMETERS ######
#         dictangledata = self.fetchAnglePara()

        angle_l = self.resultObj['SeatAngle']["Length (mm)"]
        angle_a = int(self.dictangledata[QString("A")])
        angle_b = int(self.dictangledata[QString("B")])
        angle_t = float(self.dictangledata[QString("t")])
        angle_r1 = float(self.dictangledata[QString("R1")])
        
        angle_r2 = (self.dictangledata[QString("R2")]).toFloat()

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        angle = Angle(L=angle_l, A=angle_a, B=angle_b, T=angle_t, R1=angle_r1, R2=angle_r2[0])

        topclipangle = Angle(L=angle_l, A=angle_a, B=angle_b, T=angle_t, R1=angle_r1, R2=angle_r2[0])
        
        
        bolt_dia = self.uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = self.bolt_R
        nut_R = bolt_R
        bolt_T = self.bolt_T 
        #bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        bolt_Ht = self.bolt_Ht
        # bolt_Ht =100.0 # minimum bolt length as per Indian Standard
        nut_T = self.nut_T
        #nut_T = 12.0 # minimum nut thickness As per Indian Standard
        nut_Ht = 12.2 #

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = column_T + angle_t + nut_T
        bgap = beam_T + angle_t + nut_T

        nutBoltArray = NutBoltArray(self.resultObj, nut, bolt, gap,bgap)

        colflangeconn = ColFlangeBeamWeb(column, beam, angle, topclipangle, nutBoltArray)
        colflangeconn.create_3dmodel()
        return colflangeconn
    #=========================================================================================

    def display_3DModel(self, component):
        self.component = component

        self.display.EraseAll()

        self.display.SetModeShaded()

        self.display.DisableAntiAliasing()

        # self.display.set_bg_gradient_color(23,1,32,150,150,170)
        self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)

        if self.loc == "Column flange-Beam web":
            self.display.View.SetProj(OCC.V3d.V3d_XnegYnegZpos)
        else:
            self.display.View_Iso()
            self.display.FitAll()

        if component == "Column":
            osdagDisplayShape(self.display, self.connectivityObj.columnModel, update=True)
        elif component == "Beam":
            osdagDisplayShape(self.display, self.connectivityObj.get_beamModel(), material=Graphic3d_NOT_2D_ALUMINUM,
                              update=True)
        elif component == "SeatAngle":
            osdagDisplayShape(self.display, self.connectivityObj.topclipangleModel, color='blue', update=True)
            osdagDisplayShape(self.display, self.connectivityObj.angleModel, color='blue', update=True)
            nutboltlist = self.connectivityObj.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
        elif component == "Model":
            osdagDisplayShape(self.display, self.connectivityObj.columnModel, update=True)
            osdagDisplayShape(self.display, self.connectivityObj.beamModel, material=Graphic3d_NOT_2D_ALUMINUM,
                              update=True)
            osdagDisplayShape(self.display, self.connectivityObj.angleModel, color='blue', update=True)
            osdagDisplayShape(self.display, self.connectivityObj.topclipangleModel, color='blue', update=True)
            nutboltlist = self.connectivityObj.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
    #=========================================================================================
    def call_3DModel(self, flag):  # Done

        if flag is True:

            if self.loc == "Column web-Beam web":
                self.connectivityObj = self.create3DColWebBeamWeb()

            elif self.loc == "Column flange-Beam web":
                self.connectivityObj = self.create3DColFlangeBeamWeb()

            else:
                self.connectivityObj = self.create3DBeamWebBeamWeb()

            self.display_3DModel("Model")

        else:
            self.display.EraseAll()
    #=========================================================================================

    def call_saveOutputs(self):  # Done

        return self.call_finCalculation(self.uiObj)

    #=========================================================================================

    def call2D_Drawing(self, view, fileName, loc, folder):
        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        if view == "All":
            ''

            self.callDesired_View(fileName, view, folder)
            self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)

            data = str(folder) + "/images_html/3D_Model.png"
            self.display.ExportToImage(data)

        else:

            f = open(fileName, 'w')

            self.callDesired_View(fileName, view, folder)
            f.close()

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def callDesired_View(self, fileName, view, folder):

        finCommonObj = SeatCommonData(self.uiObj, self.resultObj, self.dictbeamdata, self.dictcoldata, self.dictangledata,folder)
        finCommonObj.saveToSvg(str(fileName), view)

    #=========================================================================================
    def call_saveMessages(self):  # Done

        fileName = "./seatangle.log"

        return fileName

    #=========================================================================================
    def call_designReport(self, htmlfilename, profileSummary):
        
        reportObj = ReportGenerator()
        fileName = str(htmlfilename)

        if not os.path.isfile(fileName):
            
            reportObj.save_html(self.resultObj, self.uiObj, self.dictbeamdata, self.dictcoldata, profileSummary, htmlfilename, self.folder)

    #=========================================================================================

    def load_userProfile(self):
        pass

    #=========================================================================================
    def save_userProfile(self, profile_summary, fileName):
        filename = str(fileName)

        infile = open(filename, 'w')
        json.dump(profile_summary, infile)
        infile.close()
        pass

    #=========================================================================================
    def save_CADimages(self):  # png,jpg and tiff
        pass
