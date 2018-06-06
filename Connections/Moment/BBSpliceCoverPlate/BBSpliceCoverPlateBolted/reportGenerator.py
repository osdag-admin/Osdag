'''
@author: Swathi M.
Created on: 28 May 2018
'''

from __builtin__ import str
import time
import math
import os
from os.path import exists
import pickle

from Connections.connection_calculations import ConnectionCalculations

def save_html(outputObj, uiObj, dictbeamdata, reportsummary, filename, folder):
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
#     Connections/Shear/Fin Plate/
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
# BB Splice Cover Plate Bolted Main Data
    beam_w_t = float(dictbeamdata["tw"])
    beam_f_t = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])

    beam_r1 = float(dictbeamdata["R1"])
    beam_b = float(dictbeamdata["B"])

    connectivity = uiObj["Member"]["Connectivity"]
    beam_section = uiObj["Member"]["BeamSection"]
    beam_fu = float(uiObj["Member"]["fu (MPa)"])
    beam_fy = float(uiObj["Member"]["fy (MPa)"])

    shear_load = float(uiObj["Load"]["ShearForce (kN)"])
    moment_load = float(uiObj["Load"]["Moment (kNm)"])
    axial_force = float(uiObj["Load"]["AxialForce"])

    bolt_diameter = int(uiObj["Bolt"]["Diameter (mm)"])
    bolt_grade = float(uiObj["Bolt"]["Grade"])
    bolt_type = (uiObj["Bolt"]["Type"])

    # Design Preferences
    gap = float(uiObj["detailing"]["gap"]) # gap between two beams
    mu_f = float(uiObj["bolt"]["slip_factor"])
    dp_bolt_hole_type = str(uiObj["bolt"]["bolt_hole_type"])
    dia_hole = int(uiObj["bolt"]["bolt_hole_clrnce"]) + bolt_diameter
    type_edge = str(uiObj["detailing"]["typeof_edge"])

    flange_plate_t = float(uiObj["FlangePlate"]["Thickness (mm)"])
    flange_plate_w = str(uiObj["FlangePlate"]["Width (mm)"])
    if flange_plate_w == '':
        flange_plate_w = 0
    else:
        flange_plate_w = int(flange_plate_w)

    flange_plate_l = str(uiObj["FlangePlate"]["Height (mm)"])
    if flange_plate_l == '':
        flange_plate_l = 0
    else:
        flange_plate_l = int(flange_plate_l)

    # flange_plate_fu = float(uiObj["Member"]["fu (Mpa)"])
    # flange_plate_fy = float(uiObj["Member"]["fy (MPa)"])
    flange_plate_fu = beam_fu
    flange_plate_fy = beam_fy

    web_plate_t = float(uiObj["WebPlate"]["Thickness (mm)"])
    web_plate_w = str(uiObj["WebPlate"]["Width (mm)"])
    if web_plate_w == '':
        web_plate_w = 0
    else:
        web_plate_w = int(web_plate_w)

    web_plate_l = str(uiObj["WebPlate"]["Height (mm)"])
    if web_plate_l == '':
        web_plate_l = 0
    else:
        web_plate_l = int(web_plate_l)

    web_plate_fu = int(beam_fu)
    web_plate_fy = int(beam_fy)


    ## To call k_h value from hsfg calculations
    bolt_param_k_h = ConnectionCalculations.calculate_k_h(bolt_hole_type=dp_bolt_hole_type)
    k_h = str(float(bolt_param_k_h))

    ## To call F_0 value from hsfg calculations
    bolt_param_F_0 = ConnectionCalculations.proof_load_F_0(bolt_diameter=bolt_diameter, bolt_fu=bolt_grade)
    F_0 = str(float(bolt_param_F_0))

    beamdepth = str(int(round(outputObj['FlangeBolt']['beamdepth'], 1)))
    beamflangethk = str(int(round(outputObj['FlangeBolt']['beamflangethk'], 1)))
    beamrootradius = str(int(round(outputObj['FlangeBolt']['beamrootradius'], 1)))
    ShearCapacity = str(int(round(outputObj["WebBolt"]["ShearCapacity"], 1)))
    CapacityBolt = str(int(round(outputObj["WebBolt"]["CapacityBolt"], 1)))
    BoltsRequired = str(int(round(outputObj["WebBolt"]["BoltsRequired"], 1)))
    TotalBoltsRequired = str(int(round(outputObj["WebBolt"]["TotalBoltsRequired"], 1)))
    Pitch = str(int(round(outputObj["WebBolt"]["Pitch"], 1)))
    End = str(int(round(outputObj["WebBolt"]["End"], 1)))
    Edge = str(int(round(outputObj["WebBolt"]["Edge"], 1)))
    WebPlateHeight = str(int(round(outputObj["WebBolt"]["WebPlateHeight"], 1)))
    WebGauge = str(int(round(outputObj["WebBolt"]["WebGauge"], 1)))
    webPlateDemand = str(int(round(outputObj["WebBolt"]["webPlateDemand"], 1)))
    WebPlateWidth = str(int(round(outputObj["WebBolt"]["WebPlateWidth"], 1)))
    WebPlateCapacity = str(int(round(outputObj["WebBolt"]["WebPlateCapacity"], 1)))

    ShearCapacityF = str(int(round(outputObj["FlangeBolt"]["ShearCapacityF"], 1)))
    BearingCapacityF = str(int(round(outputObj["FlangeBolt"]["BearingCapacityF"], 1)))
    CapacityBoltF = str(int(round(outputObj["FlangeBolt"]["CapacityBoltF"], 1)))
    BoltsRequiredF = str(int(round(outputObj["FlangeBolt"]["BoltsRequiredF"], 1)))
    TotalBoltsRequiredF = str(int(round(outputObj["FlangeBolt"]["TotalBoltsRequiredF"], 1)))
    NumberBoltColFlange = str(int(round(outputObj["FlangeBolt"]["NumberBoltColFlange"], 1)))
    PitchF = str(int(round(outputObj["FlangeBolt"]["PitchF"], 1)))
    EndF = str(int(round(outputObj["FlangeBolt"]["EndF"], 1)))
    EdgeF = str(int(round(outputObj["FlangeBolt"]["EdgeF"], 1)))
    FlangePlateHeight = str(int(round(outputObj["FlangeBolt"]["FlangePlateHeight"], 1)))
    FlangePlateWidth = str(int(round(outputObj["FlangeBolt"]["FlangePlateWidth"], 1)))
    FlangeGauge = str(int(round(outputObj["FlangeBolt"]["FlangeGauge"], 1)))
    FlangePlateDemand = str(int(round(outputObj["FlangeBolt"]["FlangePlateDemand"], 1)))
    FlangeCapacity = str(int(round(outputObj["FlangeBolt"]["FlangeCapacity"], 1)))

    WebBlockShear = str(int(round(outputObj["WebBolt"]["WebBlockShear"], 1)))
    ShearYielding = str(int(round(outputObj["WebBolt"]["ShearYielding"], 1)))
    ShearRupture = str(int(round(outputObj["WebBolt"]["ShearRupture"], 1)))
    FlangeCapacity = str(int(round(outputObj["FlangeBolt"]["FlangeCapacity"], 1)))
    Yielding = str(int(round(outputObj["FlangeBolt"]["Yielding"], 1)))
    Rupture = str(int(round(outputObj["FlangeBolt"]["Rupture"], 1)))
    FlangeBlockShear = str(int(round(outputObj["FlangeBolt"]["FlangeBlockShear"], 1)))

    status = str(outputObj['FlangeBolt']['status'])
    status = str(outputObj['WebBolt']['status'])
    FlangePlateDimension = FlangePlateHeight + 'X' + FlangePlateWidth + 'X' + flange_plate_t
    WebPlateDimension = WebPlateHeight + 'X' + WebPlateWidth + 'X' + web_plate_t

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
        row = [1, "Cover Plate", "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [1, "Cover Plate", "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('tr')
    rstr += t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1"') + row[2] + t('/td')
    # rstr += t('td class="header1 safe"') + row[3] + t('/td')
    rstr += t('/tr')

    row = [0, "Cover Plate", " "]
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

    row = [1, "Connection Title", "Cover Plate"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Connection Type", "Moment Connection"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [0, "Connection Category ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

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

    row = [0, "Loading (Factored Load) ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # row = [1, "Shear Force (kN)", "140"]
    row = [1, "Moment (kNm)", moment_load]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Shear Force (kN)", shear_load]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Axial Force (kN)", axial_force]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [0, "Components ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # row = [1, "Beam Section", "ISMB 400"]
    row = [1, "Beam Section", beam_section]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Material", "Fe " + beam_fu]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Hole", dp_bolt_hole_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [1, "Plate Section ", "PLT 300X10X100 "]
    row = [1, "Flange Splice Plate", FlangePlateDimension]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Thickness (mm)", "10"]
    row = [2, "Thickness (mm)", flange_plate_t]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Height (mm)", FlangePlateHeight]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Width (mm)", FlangePlateWidth]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Hole", dp_bolt_hole_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Web Splice Plate", WebPlateDimension]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Thickness (mm)", "10"]
    row = [2, "Thickness (mm)", web_plate_t]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Height (mm)", WebPlateHeight]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Width (mm)", WebPlateWidth]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Hole", dp_bolt_hole_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Bolts ", " "]
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
    row = [2, "Diameter (mm)", bolt_diameter]
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
def space(n):
    rstr = "&nbsp;" * 4 * n
    return rstr


def t(n):
    return '<' + n + '/>'


def w(n):
    return '{' + n + '}'


def quote(m):
    return '"' + m + '"'