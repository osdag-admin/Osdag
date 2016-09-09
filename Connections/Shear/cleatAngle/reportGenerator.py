'''
Created on 16-Mar-2016

@author: reshma
'''
import sys
import time
import math
import pdfkit
# import os.path
# import pickle
from numpy.core.defchararray import rstrip
from PyQt4.Qt import QString 



def save_html(outputObj, uiObj, dictBeamData, dictColData, dictCleatData, reportsummary, filename, folder, base, base_front, base_top, base_side):
    print outputObj
    fileName = (filename)
    myfile = open(fileName, 'w')
    myfile.write(t('! DOCTYPE html'))
    myfile.write(t('html'))
    myfile.write(t('head'))
    myfile.write(t('link type="text/css" rel="stylesheet"'))
        
############################   mystyle.css is written here  ##############################################################################
    myfile.write(t('style'))
    myfile.write('table{width= 100%; border-collapse:collapse; border:1px solid black collapse}')
    myfile.write('th,td {padding:3px}')
    # Provides light green background color(#D5DF93), font-weight bold, font-size 20 and font-family
    myfile.write('td.detail{background-color:#D5DF93; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
    # Provides font-weight bold, font-size 20 and font-family 
    myfile.write('td.detail1{font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
    # Provides font-size 20 and font-family
    myfile.write('td.detail2{font-size:20; font-family:Helvetica, Arial, Sans Serif}')
    # Provides dark green background color(#8FAC3A), font-weight bold, font-size 20 and font-family
    myfile.write('td.header0{background-color:#8fac3a; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
    # Provides grey background color(#E6E6E6), font-weight bold, font-size 20 and font-family
    myfile.write('td.header1{background-color:#E6E6E6; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
    # Provides only font-size 20 and width of the images box
    myfile.write('td.header2{font-size:20; width:50%}')
    myfile.write(t('/style'))
##############################################################################################################################################
   

    myfile.write(t('/head'))
    myfile.write(t('body'))
    
    
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DATA PARAMS
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Project summary data
    companyname = str(reportsummary["ProfileSummary"]['CompanyName'])
    companylogo = str(reportsummary["ProfileSummary"]['CompanyLogo'])
    groupteamname = str(reportsummary["ProfileSummary"]['Group/TeamName'])
    designer = str(reportsummary["ProfileSummary"]['Designer'])
    projecttitle = str(reportsummary['ProjectTitle'])
    subtitle = str(reportsummary['Subtitle'])
    jobnumber = str(reportsummary['JobNumber'])
    method = str(reportsummary['Method'])
    addtionalcomments = str(reportsummary['AdditionalComments'])
    
    
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# FinPlate Main Data
    beam_sec = str(uiObj['Member']['BeamSection'])
    column_sec = str(uiObj['Member']['ColumSection'])
    connectivity = str(uiObj['Member']['Connectivity'])
    beam_fu = str(uiObj['Member']['fu (MPa)'])
    beam_fy = str(uiObj['Member']['fy (MPa)'])
              
    shear_load = str(uiObj['Load']['ShearForce (kN)'])
                  
    bolt_dia = str(uiObj['Bolt']['Diameter (mm)'])
    bolt_type = str(uiObj["Bolt"]["Type"])
    bolt_grade = str(uiObj['Bolt']['Grade'])
    
    bolt_fu = int(float(bolt_grade)) * 100
    bolt_fy = (float(bolt_grade) - int(float(bolt_grade))) * bolt_fu
    
    bolt_fu = str(bolt_fu)
    bolt_fy = str(bolt_fy)
    
   
    cleat_length = str(uiObj['cleat']['Height (mm)'])
    cleat_fu = str(uiObj['Member']['fu (MPa)'])
    cleat_fy = str(uiObj['Member']['fy (MPa)'])
    cleat_sec = str(uiObj['cleat']['section'])
    
    
#     dictbeamdata  = get_beamdata(beam_sec)
    beam_tw = str(float(dictBeamData[QString("tw")]))
    beam_f_t = str(float(dictBeamData[QString("T")]))
    beam_d = str(float(dictBeamData[QString("D")]))
    beam_R1 = str(float(dictBeamData[QString("R1")]))
    beam_B = str(float(dictBeamData[QString("B")]))
    beam_D = str(float(dictBeamData[QString("D")]))
       
#      dictcolumndata = get_columndata(column_sec)
    column_w_t = str(float(dictColData[QString("tw")]))
    column_f_t = str(float(dictColData[QString("T")]))
    column_R1 = str(float(dictColData[QString("R1")]))
    column_D = str(float(dictColData[QString("D")]))
    column_B = str(float(dictColData[QString("B")]))

        
   
#     dictCleatData = get_angledata(cleat_sec)
    cleat_legsize = str(int(dictCleatData[QString("A")]))
    cleat_legsize_1 = str(int(dictCleatData[QString("B")]))
    cleat_thk = str(int(dictCleatData[QString("t")]))
    
    
    
    
    
    # 'Size (mm)'
#     weld_Thick = str(uiObj['Weld']['Size (mm)'])
#     
#     beamdepth = str(int(round(outObj['Plate']['beamdepth'],1)))
#     beamflangethk = str(int(round(outObj['Plate']['beamflangethk'],1)))
#     beamrootradius = str(int(round(outObj['Plate']['beamrootradius'],1)))
#     platethk = str(int(round(outObj['Plate']['platethk'],1)))
#     blockshear = str(int(round(outObj['Plate']['blockshear'],1)))
#     colflangethk = str(int(round(outObj['Plate']["colflangethk"],1)))
#     colrootradius = str(int(round(outObj['Plate']['colrootradius'])))
#     
#     plateWidth = str(int(round(outObj['Plate']['width'],1)))
#     plateLength = str(int(round(outObj['Plate']['height'],1)))
#     weldSize = str(int(round(outObj['Weld']['thickness'],1)))   
#     plateDimension = plateLength +'X'+ plateWidth + 'X'+ plateThick
    
    
    
    ##########################Output###########################
#     
#     noOfBolts = str(outObj['Bolt']['numofbolts'])
#     noOfRows = str(outObj['Bolt']['numofrow'])
#     noOfCol = str(outObj['Bolt']['numofcol'])
#     edge = str(int(round(outObj['Bolt']['edge'],1)))
#     gauge = str(int(round(outObj['Bolt']['gauge'],1)))
#     pitch = str(int(round(outObj['Bolt']['pitch'],1)))
#     end = str(int(round(outObj['Bolt']['enddist'],1)))
#     weld_strength = str(round(float(outObj['Weld']['weldstrength']/1000),3))
#     moment_demand = str(outObj['Plate']['externalmoment'])
#     
#     beam_tw = str(float(dictBeamData["tw"]))
# 
#     bolt_fu = str(outObj['Bolt']['bolt_fu'])
#     bolt_dia = str(outObj['Bolt']['bolt_dia'] )
#     kb = str(outObj['Bolt']['k_b'])
#     beam_w_t = str(outObj['Bolt']['beam_w_t'] )
#     web_plate_t = str(outObj['Bolt']['web_plate_t'])
#     beam_fu = str(outObj['Bolt']['beam_fu'])
#     dia_hole = str(outObj['Bolt']['dia_hole'])
#     web_plate_fy = str(outObj['Plate']['web_plate_fy'])
#     weld_fu = str(outObj['Weld']['weld_fu'] )
#     weld_l = str(outObj['Weld']['effectiveWeldlength'])
#     shearCapacity = str(round(outObj['Bolt']['shearcapacity'],3))
#     bearingcapacity = str(round(outObj['Bolt']['bearingcapacity'],4))
#     momentDemand = str(outObj['Plate']['externalmoment'])
#     
#     gap = '20'
    
    ##################output beam part ###########
#     kb = "0.5"
    kb = str(outputObj['Bolt']['kb'])
    shearCapacity_b = str(outputObj['Bolt']['shearcapacity'])  
    bearingcapacity_b = str(outputObj['Bolt']['bearingcapacity']) 
    boltbearingcapacity_b = str(outputObj['Bolt']['boltbearingcapacity'])
    bearingcapacitybeam_b = str(outputObj['Bolt']['bearingcapacitybeam'])
    bearingcapacitycleat_b = str(outputObj['Bolt']['bearingcapacitycleat'])
    
    moment_demand_b = str(outputObj['Bolt']['externalmoment'])  
    moment_capacity_b = str(outputObj['Bolt']['momentcapacity'])  
    
    blockshear_b = str(outputObj['Bolt']['blockshear'])
    critboltshear_b = str(outputObj['Bolt']['critshear'])
     
    boltCapacity_b = str(outputObj['Bolt']['boltcapacity'])
    noOfBolts_b = str(outputObj['Bolt']['numofbolts'])
    noOfRows_b = str(outputObj['Bolt']['numofrow'])
    noOfCol_b = str(outputObj['Bolt']['numofcol'])
    pitch_b = str(outputObj['Bolt']['pitch'])
    dia_hole = str(outputObj['Bolt']['diahole'])
    edge_b = str(outputObj['Bolt']['enddist']) 
    end_b = str(outputObj['Bolt']['edge'])
    gauge_b = str(outputObj['Bolt']['gauge'])  
    boltGrpCapacity_b = str(outputObj['Bolt']['boltgrpcapacity'])
    thinner_b = str(outputObj['Bolt']['thinner'])
    ##################output column part ###########
    shearCapacity_c = str(outputObj['cleat']['shearcapacity'])  
    bearingcapacity_c = str(outputObj['cleat']['bearingcapacity']) 
    boltbearingcapacity_c = str(outputObj['cleat']['boltbearingcapacity'])
    bearingcapacitycolumn_c = str(outputObj['cleat']['bearingcapacitycolumn'])
    bearingcapacitycleat_c = str(outputObj['cleat']['bearingcapacitycleat'])
    
    
    blockshear_c = str(outputObj['cleat']['blockshear'])
    critboltshear_c = str(outputObj['cleat']['critshear'])
    
    moment_demand_c = str(outputObj['cleat']['externalmoment'])  
    moment_capacity_c = str(outputObj['cleat']['momentcapacity'])  
    
    
    boltCapacity_c = str(outputObj['cleat']['boltcapacity'])
    noOfBolts_c = str(outputObj['cleat']['numofbolts'])
    noOfRows_c = str(outputObj['cleat']['numofrow'])
    noOfCol_c = str(outputObj['cleat']['numofcol'])
    pitch_c = str(outputObj['cleat']['pitch'])
    height_c = str(outputObj['cleat']['height'])
    edge_c = str(outputObj['cleat']['end']) 
    end_c = str(outputObj['cleat']['edge'])
    gauge_c = str(outputObj['cleat']['guage'])  
    boltGrpCapacity_c = str(outputObj['cleat']['boltgrpcapacity'])
    thinner_c = str(outputObj['cleat']['thinner'])
    gap = '20'

    
    
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%')

    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "images_html/cmpylogoCleat.png"  height=60></object>', '<font face="Helvetica, Arial, Sans Serif" size="2">Created with</font>'' &nbsp' '<object type= "image/PNG" data= "images_html/Osdag_header.png" height=60></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" ') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Method']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')    
    rstr += t('/hr')    

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Design Conclusion
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    row = [0, "Design Conclusion", "IS800:2007/Limit state design"]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
      
    row = [1, "Cleat Angle", "Pass"]
    rstr += t('tr')
    rstr += t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1"') + row[2] + t('/td')
    # rstr += t('td class="header1 safe"') + row[3] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Cleat Angle", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Connection Properties", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Connection ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    row = [1, "Connection Title", " Double Angle Web Cleat"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [1, "Connection Type", "Shear Connection"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Connection Category ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    # row = [1, "Connectivity", "Column Web Beam Web"]
    row = [1, "Connectivity", connectivity]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [1, "Beam Connection", "Bolted"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
 
#     row = [1, "Beam Connection", "Bolted"]
#     rstr += t('tr')
#     rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td class="header2 "') + row[2] + t('/td')
#     rstr += t('/tr')
     
# 
    row = [1, "Column Connection", "Bolted"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [0, "Loading (Factored Load) ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    # row = [1, "Shear Force (kN)", "140"]
    row = [1, "Shear Force (kN)", shear_load]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
     
    row = [0, "Components ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    # row = [1, "Column Section", "ISSC 200"]
    row = [1, "Column Section", column_sec]
     
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [2, "Material", "Fe " + beam_fu]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [1, "Beam Section", "ISMB 400"]
    row = [1, "Beam Section", beam_sec]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [2, "Material", "Fe " + beam_fu]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [2, "Hole", "STD"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [1, "Cleat Section ", "ISA 300X10X100 "]
    row = [1, "Cleat Section", cleat_sec]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Thickness (mm)", "10"]
    row = [2, "Thickness (mm)", cleat_thk]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
#     row = [2, "Cleat Leg Size A (mm)", 50]
    row = [2, "Cleat Leg Size B (mm)", cleat_legsize]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
#     row = [2, "Cleat Leg Size B (mm)", 50]
    row = [2, "Cleat Leg Size A (mm)", cleat_legsize_1]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [2, "Hole", "STD"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
     
    row = [1, "Bolts on Beam", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Type", "HSFG"]
    row = [2, "Type", bolt_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Grade", "8.8"]
    row = [2, "Grade", bolt_grade]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Diameter (mm)", "20"]
    row = [2, "Diameter (mm)", bolt_dia]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Bolt Numbers", "3"]
    row = [2, "Bolt Numbers", noOfBolts_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Columns (Vertical Lines)", "1 "]
    row = [2, "Columns (Vertical Lines)", noOfCol_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Bolts Per Column", "3"]
    row = [2, "Bolts Per Column", noOfRows_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Gauge (mm)", "0"]
    row = [2, "Gauge (mm)", gauge_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Pitch (mm)", "100"]
    row = [2, "Pitch (mm)", pitch_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "End Distance (mm)", "50"]
    row = [2, "End Distance (mm)", end_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Edge Distance (mm)", "50"]
    row = [2, "Edge Distance (mm)", edge_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Bolts on Column", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    # row = [2, "Type", "HSFG"]
    row = [2, "Type", bolt_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Grade", "8.8"]
    row = [2, "Grade", bolt_grade]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    # row = [2, "Diameter (mm)", "20"]
    row = [2, "Diameter (mm)", bolt_dia]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Bolt Numbers", "3"]
    row = [2, "Bolt Numbers", noOfBolts_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Columns (Vertical Lines)", "1 "]
    row = [2, "Columns (Vertical Lines)", noOfCol_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Bolts Per Column", "3"]
    row = [2, "Bolts Per Column", noOfRows_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Gauge (mm)", "0"]
    row = [2, "Gauge (mm)", gauge_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Pitch (mm)", "100"]
    row = [2, "Pitch (mm)", pitch_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "End Distance (mm)", "50"]
    row = [2, "End Distance (mm)", end_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')
     
    # row = [2, "Edge Distance (mm)", "50"]
    row = [2, "Edge Distance (mm)", edge_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
    row = [0, "Assembly ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    # row = [1, "Column-Beam Clearance (mm)", "20"]
    row = [1, "Column-Beam Clearance (mm)", gap]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

#*************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "images_html/cmpylogoCleat.png"  height=60></object>', '<font face="Helvetica, Arial, Sans Serif" size="2">Created with</font>'' &nbsp' '<object type= "image/PNG" data= "images_html/Osdag_header.png" height=60></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" ') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Method']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')    
    rstr += t('/hr')    


#*************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Design Check

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    if connectivity == "Beam-Beam":
        check_name_b = "Design Check: Secondary Beam Connectivity"
    else:
        check_name_b = "Design Check: Beam Connectivity"
        
    row = [0, check_name_b, " "]
    rstr += t('tr')
    rstr += t('td colspan="4" class="detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    row = [0, "Check", "Required", "Provided", "Remark"]
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header1"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    const = str(round(math.pi / 4 * 0.78, 4))
    # row =[0,"Bolt shear capacity (kN)"," ","<i>V</i><sub>dsb</sub> = ((800*0.6123*20*20)/(&#8730;3*1.25*1000) = 90.53 <br> [cl. 10.3.3]"]
    row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsb</sub> = ((2*" + bolt_fu + "*" + const + "*" + bolt_dia + "*" + bolt_dia + ")/(&#8730;3*1.25*1000) = " + shearCapacity_b + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + thinner_b + "*" + bolt_fu + ")/(1.25*1000)  = " + boltbearingcapacity_b + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    # row =[0,"Bearing capacity of beam web (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, "Bearing capacity of beam web (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + beam_tw + "*" + beam_fu + ")/(1.25*1000)  = " + bearingcapacitybeam_b + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    # row =[0,"Bearing capacity of cleat (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, "Bearing capacity of cleat (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + cleat_thk + "*" + beam_fu + ")/(1.25*1000)  = " + bearingcapacitycleat_b + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    # row =[0,"Bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    bearcapacity = str(min(float(boltbearingcapacity_b), float(bearingcapacitybeam_b), float(bearingcapacitycleat_b)))
    row = [0, "Bearing capacity (kN)", "", "Min (" + boltbearingcapacity_b + ", " + bearingcapacitybeam_b + ", " + bearingcapacitycleat_b + ") = " + bearcapacity  , ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
         
    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    row = [0, "Bolt capacity (kN)", "", "Min (" + shearCapacity_b + ", " + bearcapacity + ") = " + boltCapacity_b  , ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    # row =[0,"Critical Bolt Shear (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    row = [0, "Critical bolt shear (kN)", "&#8804; " + boltCapacity_b , critboltshear_b , "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
#     bolts = str(round(float(shear_load)/float(boltCapacity_b),1))
#     row =[0,"No. of bolts", shear_load + "/" + boltCapacity_b + " = " + bolts, noOfBolts_b, " <p align=left style=color:green><b>Pass</b></p>"]
    row = [0, "No. of bolts", "" , noOfBolts_b, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No.of column(s)", " &#8804; 2", noOfCol_b, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"No. of bolts per column"," ","3"]
    row = [0, "No. of bolts per column", " ", noOfRows_b, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    minPitch = str(int(2.5 * float(bolt_dia)))
    maxPitch = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + minPitch + ",  &#8804; Min(32*" + beam_tw + ", 300) = " + maxPitch + "<br> [cl. 10.2.2]", pitch_b, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    
    minGauge = str(int(2.5 * float(bolt_dia)))
    maxGauge = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))        
    row = [0, "Bolt gauge (mm)", " &#8805 ;2.5*" + bolt_dia + " = " + minGauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + maxGauge + " <br> [cl. 10.2.2]", gauge_b, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"End distance (mm)","&#8805;1.7* 22 = 37.4,&#8804;12*8.9 = 106.9 <br> [cl. 10.2.4]","50"]
    minEnd = str(1.7 * float(dia_hole))
    maxEnd = str(12 * float(beam_tw))
    row = [0, "End distance (mm)", " &#8805; 1.7*" + dia_hole + " = " + minEnd + ", &#8804; 12*" + beam_tw + " = " + maxEnd + " <br> [cl. 10.2.4]", end_b, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"Edge distance (mm)","&#8805; 1.7* 22 = 37.4,&#8804;12*8.9 = 106.9<br> [cl. 10.2.4]","50"," <p align=right style=color:green><b>Pass</b></p>"]
    minEdge = str(1.7 * float(dia_hole))
    maxEdge = str(12 * float(beam_tw))
    row = [0, "Edge distance (mm)", " &#8805; 1.7*" + dia_hole + " = " + minEdge + ", &#8804; 12*" + beam_tw + " = " + maxEdge + "<br> [cl. 10.2.4]", edge_b, " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    row = [0, "Block shear capacity (kN)", " &#8805; " + shear_load, "<i>V</i><sub>db</sub> = " + blockshear_b + "<br> [cl. 6.4.1]", "<p align=left style=color:green><b>Pass</b></p>"] 
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
     
     
    rstr += t('tr')
    if connectivity == "Beam-Beam":
        maxLen = str(float(beam_D) - float(column_R1) - float(column_f_t) - float(beam_f_t) - float(beam_R1) - 5)
        strmaxLen = "-" + beam_f_t + "-" + beam_R1 + "-" + column_f_t + "-" + column_R1 + "- 5"
    else:
        maxLen = str(float(beam_D) - 2 * (float(beam_f_t) + float(beam_R1) + 5))
        strmaxLen = "-" + beam_f_t + "-" + beam_R1 + "-" + beam_f_t + "-" + beam_R1 + "- 10"
    minLen = str(0.6 * float(beam_D))
    row = [0, "Cleat height (mm)", "&#8805; 0.6*" + beam_D + "=" + minLen + ", &#8804; " + beam_D + strmaxLen + "=" + maxLen + "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", height_c, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
     
    rstr += t('tr')
    # row =[0,"cleat moment capacity (kNm)","(2*90.5*100<sup>2</sup>)/100 = 18.1","<i>M</i><sub>d</sub> =1.2*250*<i>Z</i> = 40.9 <br>[cl. 8.2.1.2]","<p align=right style=color:green><b>Pass</b></p>"]
#     z = math.pow(float(cleat_length),2)* (float(cleat_thk)/(6 *1.1* 1000000))
#     momentCapacity = str(round(1.2 * float(web_plate_fy)* z,2))
    row = [0, "Cleat moment capacity (kNm)", "(2*" + shearCapacity_b + "*" + pitch_b + "<sup>2</sup>)/(" + pitch_b + "*1000) = " + moment_demand_b, "<i>M</i><sub>d</sub> = (1.2*" + cleat_fy + "*<i>Z</i>)/(1000*1.1) = " + moment_capacity_b + "<br>[cl. 8.2.1.2]", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
        
    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')
    
    
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "images_html/cmpylogoCleat.png"  height=60></object>', '<font face="Helvetica, Arial, Sans Serif" size="2">Created with</font>'' &nbsp' '<object type= "image/PNG" data= "images_html/Osdag_header.png" height=60></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" ') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Method']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')    
    rstr += t('/hr')    

#*************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Design Check

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    if connectivity == "Beam-Beam":
        check_name_c = "Design Check: Primary Beam Connectivity"
    else:
        check_name_c = "Design Check: Column Connectivity    "
    
    
    row = [0, check_name_c, " "]
    rstr += t('tr')
    rstr += t('td colspan="4" class="detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    row = [0, "Check", "Required", "Provided", "Remark"]
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="header1"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="header1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    const = str(round(math.pi / 4 * 0.78, 4))
    # row =[0,"Bolt shear capacity (kN)"," ","<i>V</i><sub>dsb</sub> = ((800*0.6123*20*20)/(&#8730;3*1.25*1000) = 90.53 <br> [cl. 10.3.3]"]
    row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsb</sub> = ((" + bolt_fu + "*" + const + "*" + bolt_dia + "*" + bolt_dia + ")/(&#8730;3*1.25*1000) = " + shearCapacity_c + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + thinner_c + "*" + bolt_fu + ")/(1.25*1000)  = " + boltbearingcapacity_c + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
    
    thk = 0.0
    strCon = " "
    if connectivity == "Column falange-Beam web":
        thk = str(column_f_t)
        strCon = "Bearing capacity of column flange (kN)"
    elif connectivity == "Column web-Beam web":
        thk = str(column_w_t)
        strCon = "Bearing capacity of column flange (kN)"
    else:
        thk = str(column_w_t)
        strCon = "Bearing capacity of beam web (kN)"
           
    rstr += t('tr')
    # row =[0,"Bearing capacity of beam web (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, strCon, "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + thk + "*" + beam_fu + ")/(1.25*1000)  = " + bearingcapacitycolumn_c + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')
    
    # row =[0,"Bearing capacity of cleat (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, "Bearing capacity of cleat (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + cleat_thk + "*" + beam_fu + ")/(1.25*1000)  = " + bearingcapacitycleat_c + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    # row =[0,"Bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, "Bearing capacity (kN)", "", "Min (" + boltbearingcapacity_c + ", " + bearingcapacitycolumn_c + ", " + bearingcapacitycleat_c + ") = " + bearingcapacitycleat_c  , ""]
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
         
    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    row = [0, "Bolt capacity (kN)", "", "Min (" + shearCapacity_c + ", " + bearingcapacitycleat_c + ") = " + boltCapacity_c  , ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    # row =[0,"Critical Bolt Shear (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    row = [0, "Critical bolt shear (kN)", "&#8804; " + boltCapacity_c , critboltshear_c , "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
#     rstr += t('tr')
#     #row =[0,"Critical Bolt Shear (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
#     row =[0,"Critical Bolt Shear (kN)","&#8804;" + boltCapacity_c , critboltshear_c , "<p align=right style=color:green><b>Pass</b></p>"]
#     rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
#     rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
#     rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
#     rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
#     bolts = str(round(float(shear_load)/float(boltCapacity_c),1))
#     row =[0,"No. of bolts", shear_load + "/" + boltCapacity_c + " = " + bolts, noOfBolts_c, " <p align=left style=color:green><b>Pass</b></p>"]
    row = [0, "No. of bolts", "", noOfBolts_c, ""]
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No.of column(s) per angle", " &#8804; 2", noOfCol_c, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"No. of bolts per column"," ","3"]
    row = [0, "No. of bolts per column per angle", " ", noOfRows_c, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    minPitch = str(int(2.5 * float(bolt_dia)))
    maxPitch = str(300) if 32 * float(thinner_c) > 300 else str(int(math.ceil(32 * float(thinner_c))))
    row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + minPitch + ",  &#8804; Min(32*" + thinner_c + ", 300) = " + maxPitch + "<br> [cl. 10.2.2]", pitch_c, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    minGauge = str(int(2.5 * float(bolt_dia)))
    maxGauge = str(300) if 32 * float(thinner_c) > 300 else str(int(math.ceil(32 * float(thinner_c))))
    row = [0, "Bolt gauge (mm)", " &#8805; 2.5*" + bolt_dia + " = " + minGauge + ", &#8804; Min(32*" + thinner_c + ", 300) = " + maxGauge + " <br> [cl. 10.2.2]", gauge_c, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"End distance (mm)","&#8805;1.7* 22 = 37.4,&#8804;12*8.9 = 106.9 <br> [cl. 10.2.4]","50"]
    minEnd = str(1.7 * float(dia_hole))
    maxEnd = str(12 * float(thinner_c))
    row = [0, "End distance (mm)", " &#8805; 1.7*" + dia_hole + " = " + minEnd + ", &#8804; 12*" + thinner_c + " = " + maxEnd + " <br> [cl. 10.2.4]", end_c, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    # row =[0,"Edge distance (mm)","&#8805; 1.7* 22 = 37.4,&#8804;12*8.9 = 106.9<br> [cl. 10.2.4]","50"," <p align=right style=color:green><b>Pass</b></p>"]
    minEdge = str(1.7 * float(dia_hole))
    maxEdge = str(12 * float(thinner_c))
    row = [0, "Edge distance (mm)", " &#8805;1.7*" + dia_hole + " = " + minEdge + ", &#8804;12*" + thinner_c + " = " + maxEdge + "<br> [cl. 10.2.4]", edge_c, " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
    rstr += t('tr')
    row = [0, "Block shear capacity (kN)", " &#8805;" + shear_load, "<i>V</i><sub>db</sub> = " + blockshear_c + "<br> [cl. 6.4.1]", "<p align=left style=color:green><b>Pass</b></p>"] 
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
     
     
    rstr += t('tr')
    if connectivity == "Beam-Beam":
        maxLen = str(float(beam_D) - float(column_R1) - float(column_f_t) - float(beam_f_t) - float(beam_R1) - 5)
        strmaxLen = "-" + beam_f_t + "-" + beam_R1 + "-" + column_f_t + "-" + column_R1 + "- 5"
    else:
        maxLen = str(float(beam_D) - 2 * (float(beam_f_t) + float(beam_R1) + 5))
        strmaxLen = "2*(" + beam_f_t + "+" + beam_R1 + "+5)"
    minLen = str(0.6 * float(beam_D))
    row = [0, "Cleat height (mm)", "&#8805; 0.6*" + beam_D + "=" + minLen + ", &#8804; " + beam_D + strmaxLen + "=" + maxLen + "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", height_c, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
     
     
    rstr += t('tr')
    # row =[0,"cleat moment capacity (kNm)","(2*90.5*100<sup>2</sup>)/100 = 18.1","<i>M</i><sub>d</sub> =1.2*250*<i>Z</i> = 40.9 <br>[cl. 8.2.1.2]","<p align=right style=color:green><b>Pass</b></p>"]
#     z = math.pow(float(cleat_length),2)* (float(cleat_thk)/(6 *1.1* 1000000))
#     momentCapacity = str(round(1.2 * float(beam_fy)* z/1.1,2))
    row = [0, "Cleat moment capacity (kNm)", "(2*" + shearCapacity_c + "*" + pitch_c + "<sup>2</sup>)/(" + pitch_c + "*1000) = " + moment_demand_c, "<i>M</i><sub>d</sub> = (1.2*" + cleat_fy + "*<i>Z</i>)/(1000*1.1) = " + moment_capacity_c + "<br>[cl. 8.2.1.2]", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    
        
    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

#*************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "images_html/cmpylogoCleat.png"  height=60></object>', '<font face="Helvetica, Arial, Sans Serif" size="2">Created with</font>'' &nbsp' '<object type= "image/PNG" data= "images_html/Osdag_header.png" height=60></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" ') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Method']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')    
    rstr += t('/hr')    


#*************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Diagram

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    row = [0, "Views", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class=" viewtbl "') + row[2] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    png = folder + "/images_html/" + base
    datapng = '<object type="image/PNG" data= %s width ="400"></object">' % png
    
    side = folder + "/images_html/" + base_side
    dataside = '<object type="image/svg+xml" data= %s width ="400"></object>' % side
    
    top = folder + "/images_html/" + base_top
    datatop = '<object type="image/svg+xml" data= %s width ="400"></object>' % top
    
    front = folder + "/images_html/" + base_front
    datafront = '<object type="image/svg+xml" data= %s width ="450"></object>' % front

    row = [0, datapng, datatop]
    rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td  align="center" class=" header2"') + row[2] + t('/td')
    rstr += t('/tr')
     
    row = [0, dataside, datafront ]
    rstr += t('tr')
    rstr += t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td align="center" class=" header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

#*************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "images_html/cmpylogoCleat.png"  height=60></object>', '<font face="Helvetica, Arial, Sans Serif" size="2">Created with</font>'' &nbsp' '<object type= "image/PNG" data= "images_html/Osdag_header.png" height=60></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right" ') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Project Title']
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td float="right" class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Method']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    
    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')    
    rstr += t('/hr')    


#*************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Additional comments

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('''col width=30%''')
    rstr += t('''col width=70%''')
    
    rstr += t('tr')
    row = [0, "Additional Comments", addtionalcomments]
    rstr += t('td class= "detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class= "detail2" align="justified"') + row[2] + t('/td')
    rstr += t('/tr')
    
    rstr += t('/table')
    
    
    myfile.write(rstr)
    myfile.write(t('/body'))
    myfile.write(t('/html'))
    myfile.close()
    

def space(n):
    rstr = "&nbsp;" * 4 * n
    return rstr

def t(n):
    return '<' + n + '/>'

def quote(m):
    return '"' + m + '"'

# reportsummary = useUserProfile()
# print reportsummary
# save_html(outObj, uiObj, dictBeamData, dictColData)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# COnverting HTML to PDF
# pdfkit.from_file('output/reshma.html','output/reshmaReport.pdf')
# print "PDF generated"



