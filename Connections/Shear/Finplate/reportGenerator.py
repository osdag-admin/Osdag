"""This file is redundant. Use report_generator.py"""

'''
Created on Dec 10, 2015

@author: deepa
'''
from __builtin__ import str
import time
import math
import os
from os.path import exists
import pickle



def save_html(outObj, uiObj, dictBeamData, dictColData, reportsummary, filename, folder):
    fileName = (filename)
    myfile = open(fileName, "w")
    myfile.write(t('! DOCTYPE html'))
    myfile.write(t('html'))
    myfile.write(t('head'))
    myfile.write(t('link type="text/css" rel="stylesheet" '))

# mystyle.css is written here
    myfile.write(t('style'))
    myfile.write('table{width= 100%; border-collapse:collapse; border:1px solid black collapse}')
    myfile.write('th,td {padding:3px}')
#     Provides light green background color(#D5DF93), font-weight bold, font-size 20 and font-family
    myfile.write('td.detail{background-color:#D5DF93; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
#     Provides font-weight bold, font-size 20 and font-family
    myfile.write('td.detail1{font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
#     Provides font-size 20 and font-family
    myfile.write('td.detail2{font-size:20; font-family:Helvetica, Arial, Sans Serif}')
#     Provides dark green background color(#8FAC3A), font-weight bold, font-size 20 and font-family
    myfile.write('td.header0{background-color:#8fac3a; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
#     Provides grey background color(#E6E6E6), font-weight bold, font-size 20 and font-family
    myfile.write('td.header1{background-color:#E6E6E6; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
#     Provides only font-size 20 and width of the images box
    myfile.write('td.header2{font-size:20; width:50%}')
    myfile.write(t('/style'))
##############################################################################################################################################

    myfile.write(t('/head'))
    myfile.write(t('body'))
#     Connections/Shear/Finplate/
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
    client = str(reportsummary['Client'])
    addtionalcomments = str(reportsummary['AdditionalComments'])


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# FinPlate Main Data
    beam_tw = str(float(dictBeamData["tw"]))
    beam_f_t = str(float(dictBeamData["T"]))
    beam_d = str(float(dictBeamData["D"]))
    beam_R1 = str(float(dictBeamData["R1"]))
    beam_b = str(float(dictBeamData["B"]))

    column_w_t = str(float(dictColData["tw"]))
    column_f_t = str(float(dictColData["T"]))
    column_R1 = str(float(dictColData["R1"]))
    column_d = str(float(dictColData["D"]))
    column_b = str(float(dictColData["B"]))

    connectivity = str(uiObj['Member']['Connectivity'])
    shear_load = str(uiObj['Load']['ShearForce (kN)'])
    column_sec = str(uiObj['Member']['ColumSection'])
    beam_sec = str(uiObj['Member']['BeamSection'])
    plateThick = str(uiObj['Plate']['Thickness (mm)'])
    boltType = str(uiObj['Bolt']['Type'])
    boltGrade = str(uiObj['Bolt']['Grade'])
    boltDia = str(uiObj['Bolt']['Diameter (mm)'])
    # 'Size (mm)'
    weld_Thick = str(uiObj['Weld']['Size (mm)'])

    # Design Preferences
    bolt_hole_clrnce = str(float(uiObj["bolt"]["bolt_hole_clrnce"]))
    bolt_hole_type = str(uiObj["bolt"]["bolt_hole_type"])
    bolt_grade_fu = str(float(uiObj["bolt"]["bolt_fu"]))
    slip_factor = str(float(uiObj["bolt"]["slip_factor"]))

    typeof_weld = str(uiObj["weld"]["typeof_weld"])
    safety_factor = str(float(uiObj["weld"]["safety_factor"]))
    fu_overwrite = str(float(uiObj["weld"]["fu_overwrite"]))

    typeof_edge = str(uiObj["detailing"]["typeof_edge"])
    min_edgend_dist = str(float(uiObj["detailing"]["min_edgend_dist"]))
    gap = str(float(uiObj["detailing"]["gap"]))

    design_method = str(uiObj["design"]["design_method"])

    beamdepth = str(int(round(outObj['Plate']['beamdepth'], 1)))
    beamflangethk = str(int(round(outObj['Plate']['beamflangethk'], 1)))
    beamrootradius = str(int(round(outObj['Plate']['beamrootradius'], 1)))
    platethk = str(int(round(outObj['Plate']['platethk'], 1)))
    blockshear = str(int(round(outObj['Plate']['blockshear'], 1)))
    colflangethk = str(int(round(outObj['Plate']["colflangethk"], 1)))
    colrootradius = str(int(round(outObj['Plate']['colrootradius'])))

    plateWidth = str(int(round(outObj['Plate']['width'], 1)))
    plateLength = str(int(round(outObj['Plate']['height'], 1)))
    weldSize = str(int(round(outObj['Weld']['thickness'], 1)))

    plateDimension = plateLength + 'X' + plateWidth + 'X' + plateThick
    noOfBolts = str(outObj['Bolt']['numofbolts'])
    noOfRows = str(outObj['Bolt']['numofrow'])
    noOfCol = str(outObj['Bolt']['numofcol'])
    edge = str(int(round(outObj['Bolt']['edge'], 1)))
    gauge = str(int(round(outObj['Bolt']['gauge'], 1)))
    pitch = str(int(round(outObj['Bolt']['pitch'], 1)))
    end = str(int(round(outObj['Bolt']['enddist'], 1)))
    weld_strength = str(round(float(outObj['Weld']['weldstrength'] / 1000), 3))
    moment_demand = str(outObj['Plate']['externalmoment'])
    # gap = '20'
    beam_tw = str(float(dictBeamData["tw"]))

    bolt_fu = str(outObj['Bolt']['bolt_fu'])
    bolt_dia = str(outObj['Bolt']['bolt_dia'])
    kb = str(outObj['Bolt']['k_b'])
    beam_w_t = str(outObj['Bolt']['beam_w_t'])
    web_plate_t = str(outObj['Bolt']['web_plate_t'])
    beam_fu = str(outObj['Bolt']['beam_fu'])
    dia_hole = str(outObj['Bolt']['dia_hole'])
    web_plate_fy = str(outObj['Plate']['web_plate_fy'])
    weld_fu = str(outObj['Weld']['weld_fu'])
    weld_l = str(outObj['Weld']['effectiveWeldlength'])
    shearCapacity = str(outObj['Bolt']['shearcapacity'])
    bearingcapacity = str((outObj['Bolt']['bearingcapacity']))
    #bearingcapacity = str(outObj['Bolt']['bearingcapacity'])
    momentDemand = str(outObj['Plate']['externalmoment'])
    status = str(outObj['Bolt']['status'])

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoFin.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td style= "font:bold 20px Helvetica, Arial, Sans Serif;background-color:#D5DF93"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')

    row = [0, 'Project Title']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, "Client"]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')

    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
    rstr += t('/hr')

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Design Conclusion
#     rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
    rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100% ')

    row = [0, 'Design Conclusion', "IS800:2007/Limit state design"]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    if status == 'True':
        row = [1, "Finplate", "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [1, "Finplate", "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('tr')
    rstr += t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1"') + row[2] + t('/td')
    # rstr += t('td class="header1 safe"') + row[3] + t('/td')
    rstr += t('/tr')

    row = [0, "Finplate", " "]
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

    row = [1, "Connection Title", " Single Finplate"]
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

#
    row = [1, "Column Connection", "Welded"]
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

    # row = [1, "Plate Section ", "PLT 300X10X100 "]
    row = [1, "Plate Section", plateDimension]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Thickness (mm)", "10"]
    row = [2, "Thickness (mm)", plateThick]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Width (mm)", "10"]
    row = [2, "Width (mm)", plateWidth]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Depth (mm)", "300"]
    row = [2, "Depth (mm)", plateLength]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Hole", "STD"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Weld ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [2, "Type", "Double Fillet"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Size (mm)", "6"]
    row = [2, "Size (mm)", weld_Thick]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Bolts ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # row = [2, "Type", "HSFG"]
    row = [2, "Type", boltType]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Grade", "8.8"]
    row = [2, "Grade", boltGrade]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Diameter (mm)", "20"]
    row = [2, "Diameter (mm)", boltDia]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolt Numbers", "3"]
    row = [2, "Bolt Numbers", noOfBolts]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Columns (Vertical Lines)", "1 "]
    row = [2, "Columns (Vertical Lines)", noOfCol]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolts Per Column", "3"]
    row = [2, "Bolts Per Column", noOfRows]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Gauge (mm)", "0"]
    row = [2, "Gauge (mm)", gauge]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Pitch (mm)", "100"]
    row = [2, "Pitch (mm)", pitch]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "End Distance (mm)", "50"]
    row = [2, "End Distance (mm)", end]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Edge Distance (mm)", "50"]
    row = [2, "Edge Distance (mm)", edge]
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


    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Header of the pdf fetched from dialogbox
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoFin.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    #     rstr += t('td style= "font:bold 20px Helvetica, Arial, Sans Serif;background-color:#D5DF93"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')

    row = [0, 'Project Title']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, "Client"]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')

    rstr += t('hr')
    rstr += t('/hr')

    # *************************************************************************************************************************

    # Design Preferences

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
    row = [0, "Design Preferences", " "]
    rstr += t('tr')
    rstr += t('td colspan="4" class="detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
# --------------------------------      BOLT      -----------------------------------------------------------------------------------------------
    row = [0, "Bolt ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Hole Type", bolt_hole_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Hole Clearance (mm)", bolt_hole_clrnce]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Material Grade (MPa)", bolt_grade_fu]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Slip Factor", slip_factor]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')
    # --------------------------------      WELD      -----------------------------------------------------------------------------------------------
    row = [0, "Weld ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Type of Weld", typeof_weld]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Material Grade (MPa)", fu_overwrite]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # --------------------------------      DETAILING      -----------------------------------------------------------------------------------------------
    row = [0, "Detailing ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Type of Edges", typeof_edge[4:]]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Minimum Edge-End Distance", min_edgend_dist + " times the hole diameter"]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Gap between beam & support (mm)", gap]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # TODO add yes or no option??
    # row = [0, "Corrosive influences", " "]
    # rstr += t('tr')
    # rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + row[2] + t('/td')
    # rstr += t('/tr')

    # --------------------------------      DESIGN      -----------------------------------------------------------------------------------------------
    row = [0, "Design ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Design Method",  design_method]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')


# *************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoFin.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td style= "font:bold 20px Helvetica, Arial, Sans Serif;background-color:#D5DF93"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')

    row = [0, 'Project Title']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, "Client"]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')

    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')
    rstr += t('/hr')

# *************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Design Check

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
    row = [0, "Design Check", " "]
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
    if bearingcapacity == "N/A" :
        row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsf</sub> = (" + bolt_fu + "*" + const + "*" + bolt_dia + "*" + bolt_dia +
               ")/(&#8730;3*1.25*1000) = " + shearCapacity + "<br> [cl. 10.3.3]", ""]
    else:
        row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsb</sub> = (" + bolt_fu + "*" + const + "*" + bolt_dia + "*" + bolt_dia +
           ")/(&#8730;3*1.25*1000) = " + shearCapacity + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if bearingcapacity == "N/A" :
        row = [0, "Bolt bearing capacity (kN)", "", "N/A", ""]
    else:
        row = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + beam_tw + "*" + beam_fu + ")/(1.25*1000)  = " +
           bearingcapacity + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    if bearingcapacity == "N/A" :
        boltCapacity = str(float(shearCapacity))
        row = [0, "Bolt capacity (kN)", "",   boltCapacity, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        # boltCapacity = bearingcapacity if bearingcapacity < shearCapacity else shearCapacity
        boltCapacity =  str(min(float(shearCapacity), float(bearingcapacity)))
        row = [0, "Bolt capacity (kN)", "", "Min (" + shearCapacity + ", " + bearingcapacity + ") = " + boltCapacity, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
    bolts = str(round(float(shear_load) / float(boltCapacity), 1))
    if float(bolts) > int(noOfBolts):
        row = [0, "No. of bolts", shear_load + "/" + boltCapacity + " = " + bolts, noOfBolts,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "No. of bolts", shear_load + "/" + boltCapacity + " = " + bolts, noOfBolts, " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No.of column(s)", " &#8804; 2", noOfCol, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts per column"," ","3"]
    row = [0, "No. of bolts per column", " ", noOfRows, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    minPitch = str(int(2.5 * float(bolt_dia)))
    maxPitch = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + minPitch + ",  &#8804; Min(32*" + beam_tw + ", 300) = " + maxPitch + "<br> [cl. 10.2.2]",
           pitch, "  <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    minGauge = str(int(2.5 * float(bolt_dia)))
    maxGauge = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    row = [0, "Bolt gauge (mm)", " &#8805; 2.5*" + bolt_dia + " = " + minGauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + maxGauge + " <br> [cl. 10.2.2]",
           gauge, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"End distance (mm)","&#8805;1.7* 22 = 37.4,&#8804;12*8.9 = 106.9 <br> [cl. 10.2.4]","50"]
    minEnd = str(1.7 * float(dia_hole))
    maxEnd = str(12 * float(beam_tw))
    row = [0, "End distance (mm)", " &#8805; 1.7*" + dia_hole + " = " + minEnd + ", &#8804; 12*" + beam_tw + " = " + maxEnd + " <br> [cl. 10.2.4]", end,
           "  <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Edge distance (mm)","&#8805; 1.7* 22 = 37.4,&#8804;12*8.9 = 106.9<br> [cl. 10.2.4]","50"," <p align=right style=color:green><b>Pass</b></p>"]
    minEdge = str(1.7 * float(dia_hole))
    maxEdge = str(12 * float(beam_tw))
    row = [0, "Edge distance (mm)", " &#8805; 1.7*" + dia_hole + " = " + minEdge + ", &#8804; 12*" + beam_tw + " = " + maxEdge + "<br> [cl. 10.2.4]", edge,
           " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Block shear capacity (kN)", " &#8805; " + shear_load, "<i>V</i><sub>db</sub> = " + blockshear + "<br>",
           "  <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Plate thickness (mm)","(5*140*1000)/(300*250)= 9.33","10"]
    minPlateThick = str(round(5 * float(shear_load) * 1000 / (float(plateLength) * float(web_plate_fy)), 2))
    if float(minPlateThick) > int(plateThick):
        row = [0, "Plate thickness (mm)",
               "(5*" + shear_load + "*1000)/(" + plateLength + "*" + web_plate_fy + ") = " + minPlateThick +
               "<br> [Owens and Cheal, 1989]", plateThick, "  <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Plate thickness (mm)", "(5*" + shear_load + "*1000)/(" + plateLength + "*" + web_plate_fy + ") = " + minPlateThick +
           "<br> [Owens and Cheal, 1989]", plateThick, "  <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
#     if
    minEdge = str(0.6 * float(beamdepth))
    if connectivity == "Beam-Beam":
        maxEdge = str(float(beamdepth) - float(beamflangethk) - float(beamrootradius) - float(colflangethk) - float(colrootradius) - 5)
        maxedgestring = beamdepth + "-" + beamflangethk + "-" + beamrootradius + "-" + colflangethk + "-" + colrootradius + "- 5"
    else:
        maxEdge = str(float(beamdepth) - 2 * float(beamflangethk) - 2 * float(beamrootradius) - 10)
        maxedgestring = beamdepth + "-" + beamflangethk + "-" + beamrootradius + "-" + "10"

    row = [0, "Plate height (mm)", "&#8805; 0.6*" + beamdepth + "=" + minEdge + ", &#8804; " + maxedgestring + "=" + maxEdge +
           "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", plateLength, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
#        #row =[0,"Plate height (mm)","",plateLength]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Plate width (mm)", "", "100", ""]
    # row =[0,"Plate width (mm)","",plateWidth]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Plate moment capacity (kNm)","(2*90.5*100<sup>2</sup>)/100 = 18.1","<i>M</i><sub>d</sub> =1.2*250*<i>Z</i> = 40.9 <br>[cl. 8.2.1.2]","<p align=right style=color:green><b>Pass</b></p>"]
    z = math.pow(float(plateLength), 2) * (float(plateThick) / (6 * 1.1 * 1000000))
    momentCapacity = str(round(1.2 * float(web_plate_fy) * z, 2))
    if float(moment_demand) > float(web_plate_fy) :
        row = [0, "Plate moment capacity (kNm)",
               "(2*" + shearCapacity + "*" + pitch + "<sup>2</sup>)/(" + pitch + "*1000) = " + moment_demand,
               "<i>M</i><sub>d</sub> = (1.2*" + web_plate_fy + "*<i>Z</i>)/(1000*1.1) = " + momentCapacity + "<br>[cl. 8.2.1.2]",
               "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Plate moment capacity (kNm)", "(2*" + shearCapacity + "*" + pitch + "<sup>2</sup>)/(" + pitch + "*1000) = " + moment_demand,
           "<i>M</i><sub>d</sub> = (1.2*" + web_plate_fy + "*<i>Z</i>)/(1000*1.1) = " + momentCapacity + "<br>[cl. 8.2.1.2]",
           "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Effective weld length (mm)","","300 - 2*6 = 288"]
    effWeldLen = str(int(float(plateLength) - (2 * float(weld_Thick))))
    row = [0, "Effective weld length (mm)", "", plateLength + "-2*" + weld_Thick + " = " + effWeldLen, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Weld strength (kN/mm)","&#8730;[(18100*6)/(2*288)<sup>2</sup>]<sup>2</sup> + [140/(2*288)]<sup>2</sup> <br>=0.699","<i>f</i><sub>v</sub>=(0.7*6*410)/(&#8730;3*1.25)<br>= 0.795<br>[cl. 10.5.7]"," <p align=right style=color:green><b>Pass</b></p>"]
    a = float(2 * float(effWeldLen))
    b = 2 * math.pow((float(effWeldLen)), 2)
    x = (float(momentDemand) * 1000 * 6)
    resultant_shear = str(round(math.sqrt(math.pow((x / b), 2) + math.pow((float(shear_load) / a), 2)), 3))
    momentDemand_knmm = str(int(float(momentDemand) * 1000))
    if float(resultant_shear) > float(weld_strength):
        row = [0, "Weld strength (kN/mm)",
               " &#8730;[(" + momentDemand_knmm + "*6)/(2*" + effWeldLen + "<sup>2</sup>)]<sup>2</sup> + [" + shear_load + "/(2*" +
               effWeldLen + ")]<sup>2</sup> <br>= " + resultant_shear,
               "<i>f</i><sub>v</sub>= (0.7*" + weld_Thick + "*" + weld_fu + ")/(&#8730;3*1.25)<br>= " +
               weld_strength + "<br>[cl. 10.5.7]", " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Weld strength (kN/mm)", " &#8730;[(" + momentDemand_knmm + "*6)/(2*" + effWeldLen + "<sup>2</sup>)]<sup>2</sup> + [" + shear_load + "/(2*" +
               effWeldLen + ")]<sup>2</sup> <br>= " + resultant_shear, "<i>f</i><sub>v</sub>= (0.7*" + weld_Thick + "*" + weld_fu + ")/(&#8730;3*1.25)<br>= " +
               weld_strength + "<br>[cl. 10.5.7]", " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Weld thickness (mm)","(0.699*&#8730;3*1.25)/(0.7*410)=5.27<br>[cl. 10.5.7]","6","<p align=right style=color:green><b>Pass</b></p>"]

    weld_thickness = str(round((float(resultant_shear) * 1000 * (math.sqrt(3) * 1.25)) / (0.7 * float(weld_fu)), 2))
    x = str((float(platethk) * 0.8))
    maxweld = str(max(float(weld_thickness), float(x)))
#     maxweld = str(9) if str((float( platethk)*0.8)) > str(9) else str(round((float(resultant_shear) * 1000*(math.sqrt(3) * 1.25))/(0.7 * float(weld_fu)),2))
#     maxWeld = str(9) if str(round((float(resultant_shear) * 1000*(math.sqrt(3) * 1.25))/(0.7 * float(weld_fu)),2)) == 9 else str((float( platethk)*0.8))
#     row =[0,"Weld thickness (mm)","Max(("+resultant_shear+"*&#8730;3*1.25)/(0.7*"+weld_fu+")"+", 0.8*"+platethk+") = "+ maxWeld + "<br>[cl. 10.5.7, Insdag Detailing Manual, 2002]",weldSize,"<p align=right style=color:green><b>Pass</b></p>"]
    if float(maxweld) <= int(weld_Thick):
        row = [0, "Weld thickness (mm)", "Max((" + resultant_shear + "*1000*&#8730;3* 1.25)/(0.7 * " + weld_fu + ")" + "," + platethk + "* 0.8" + ") = " + maxweld +
               "<br>[cl. 10.5.7, Insdag Detailing Manual, 2002]", weld_Thick,
               "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Weld thickness (mm)", "Max((" + resultant_shear + "*1000*&#8730;3* 1.25)/(0.7 * " + weld_fu + ")" + "," + platethk + "* 0.8" + ") = " + maxweld +
               "<br>[cl. 10.5.7, Insdag Detailing Manual, 2002]", weld_Thick,
               "<p align=left style=color:red><b>Fail</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

# *************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    # *************************************************************************************************************************
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Header of the pdf fetched from dialogbox
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoFin.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td style= "font:bold 20px Helvetica, Arial, Sans Serif;background-color:#D5DF93"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')

    row = [0, 'Project Title']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, "Client"]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')

    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')
    rstr += t('/hr')

# *************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Digram

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

    row = [0, "Views", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    png = folder + "/images_html/3D_Model.png"
    datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png

    side = folder + "/images_html/finSide.png"
    dataside = '<object type="image/PNG" data= %s width ="400"></object>' % side

    top = folder + "/images_html/finTop.png"
    datatop = '<object type="image/PNG" data= %s width ="400"></object>' % top

    front = folder + "/images_html/finFront.png"
    datafront = '<object type="image/PNG" data= %s width ="450"></object>' % front

    if status == 'True':
        row = [0, datapng, datatop]
        rstr += t('tr')
        rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td  align="center" class=" header2"') + row[2] + t('/td')
        rstr += t('/tr')

        row = [0, dataside, datafront]
        rstr += t('tr')
        rstr += t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td align="center" class=" header2 "') + row[2] + t('/td')
        rstr += t('/tr')

    else:
        pass

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

# *************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoFin.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td style= "font:bold 20px Helvetica, Arial, Sans Serif;background-color:#D5DF93"') + space(row[0]) + row[1] + t('/td')
    row = [0, companyname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')

    row = [0, 'Project Title']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, projecttitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, groupteamname]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Subtitle']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, subtitle]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Designer']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, designer]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, 'Job Number']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, jobnumber]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Date']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, "Client"]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')

    rstr += t('hr')
#     rstr += t('p> &nbsp</p')
#     rstr += t('hr')
#     rstr += t('/hr')
    rstr += t('/hr')

# *************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Additional comments

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
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


def w(n):
    return '{' + n + '}'


def quote(m):
    return '"' + m + '"'

