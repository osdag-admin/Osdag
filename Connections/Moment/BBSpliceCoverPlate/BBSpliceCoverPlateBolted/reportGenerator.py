
'''
@author: Swathi M.
Created on: 28 May 2018
Revised on: 15 June 2018 (expert suggestions)
Revised on: 18 June 2018 (expert suggestions)
'''

from __builtin__ import str
import time
import math
import os
import pickle
from Connections.connection_calculations import ConnectionCalculations

def save_html(outputObj, uiObj, dictbeamdata, filename, reportsummary, folder):
    filename = (filename)
    myfile = open(filename, "w")
    myfile.write(t('! DOCTYPE html'))
    myfile.write(t('html'))
    myfile.write(t('head'))
    myfile.write(t('link type="text/css" rel="stylesheet" '))

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
    client = str(reportsummary['Client'])
    addtionalcomments = str(reportsummary['AdditionalComments'])

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # BB Splice Cover Plate Bolted Main Data
    beam_w_t = str(float(dictbeamdata["tw"]))
    beam_f_t = str(float(dictbeamdata["T"]))
    beam_d = str(float(dictbeamdata["D"]))

    beam_r1 = str(float(dictbeamdata["R1"]))
    beam_b = str((float(dictbeamdata["B"])))
    beam_b1 = ((float(dictbeamdata["B"])))

    connectivity = str(uiObj["Member"]["Connectivity"])
    beam_section = str(uiObj["Member"]["BeamSection"])
    beam_fu = str(float(uiObj["Member"]["fu (MPa)"]))
    beam_fy = str(float(uiObj["Member"]["fy (MPa)"]))
    beam_fy1 = (float(uiObj["Member"]["fy (MPa)"]))


    shear_load = str(float(uiObj["Load"]["ShearForce (kN)"]))
    moment_load = str(float(uiObj["Load"]["Moment (kNm)"]))
    axial_force = str((uiObj["Load"]["AxialForce"]))
    if axial_force == '':
        axial_force = str(float(0))
    else:
        axial_force = str(float(uiObj["Load"]["AxialForce"]))

    bolt_diameter = str(int(uiObj["Bolt"]["Diameter (mm)"]))
    bolt_grade = str(float(uiObj["Bolt"]["Grade"]))
    bolt_type = str((uiObj["Bolt"]["Type"]))

    # Design Preferences
    gap = str(float(uiObj["detailing"]["gap"])) # gap between two beams
    gap1 = (float(uiObj["detailing"]["gap"]))  # gap between two beams
    mu_f = str(float(uiObj["bolt"]["slip_factor"]))
    dp_bolt_hole_type = str(str(uiObj["bolt"]["bolt_hole_type"]))
    bolt_hole_clrnce = str(str(float(uiObj["bolt"]["bolt_hole_clrnce"])))
    slip_factor = str(str(float(uiObj["bolt"]["slip_factor"])))
    type_edge = str(uiObj["detailing"]["typeof_edge"])

    flange_plate_t = str(int(uiObj["FlangePlate"]["Thickness (mm)"]))
    flange_plate_preference = str(uiObj['FlangePlate']['Preferences'])

    web_plate_t = str(int(uiObj["WebPlate"]["Thickness (mm)"]))
    web_plate_w = str(uiObj["WebPlate"]["Width (mm)"])

    k_h = str(float(ConnectionCalculations.calculate_k_h(dp_bolt_hole_type)))
    bolt_fu = str(float(uiObj["bolt"]["bolt_fu"]))
    F_0 = str(float(ConnectionCalculations.proof_load_F_0(bolt_diameter, bolt_fu)))

    beamdepth = str(int(outputObj['FlangeBolt']['beamdepth']))
    beamflangethk = str(float(outputObj['FlangeBolt']['beamflangethk']))
    beamrootradius = str(float(outputObj['FlangeBolt']['beamrootradius']))
    ShearCapacity = str((outputObj["WebBolt"]["ShearCapacity"]))
    BearingCapacity = str((outputObj["WebBolt"]["BearingCapacity"]))
    CapacityBolt = str(float(outputObj["WebBolt"]["CapacityBolt"]))
    BoltsRequired = str(float(outputObj["WebBolt"]["BoltsRequired"]))
    TotalBoltsRequired = str(int(outputObj["WebBolt"]["TotalBoltsRequired"]))
    TotalBoltsRequired1 = (int(outputObj["WebBolt"]["TotalBoltsRequired"]))
    Pitch = str(int(outputObj["WebBolt"]["Pitch"]))
    End = str(int(outputObj["WebBolt"]["End"]))
    Edge = str(int(outputObj["WebBolt"]["Edge"]))
    WebPlateHeight = str(int(outputObj["WebBolt"]["WebPlateHeight"]))
    WebGauge = str(int(outputObj["WebBolt"]["WebGauge"]))
    webPlateDemand = str(float(outputObj["WebBolt"]["webPlateDemand"]))
    WebPlateWidth = str(int(outputObj["WebBolt"]["WebPlateWidth"]))
    WebPlateCapacity = str(float(outputObj["WebBolt"]["WebPlateCapacity"]))

    ShearCapacityF = str((outputObj["FlangeBolt"]["ShearCapacityF"]))
    BearingCapacityF = str((outputObj["FlangeBolt"]["BearingCapacityF"]))
    CapacityBoltF = str(float(outputObj["FlangeBolt"]["CapacityBoltF"]))
    BoltsRequiredF = str(int(outputObj["FlangeBolt"]["BoltsRequiredF"]))
    BoltsRequiredF1 = (int(outputObj["FlangeBolt"]["BoltsRequiredF"]))
    TotalBoltsRequiredF = str(int(outputObj["FlangeBolt"]["TotalBoltsRequiredF"]))
    NumberBoltColFlange = str(int(outputObj["FlangeBolt"]["NumberBoltColFlange"]))
    PitchF = str(int(outputObj["FlangeBolt"]["PitchF"]))
    EndF = str(int(outputObj["FlangeBolt"]["EndF"]))
    EdgeF = str(int(outputObj["FlangeBolt"]["EdgeF"]))
    FlangePlateHeight = str(int(outputObj["FlangeBolt"]["FlangePlateHeight"]))
    FlangePlateWidth = str(int(outputObj["FlangeBolt"]["FlangePlateWidth"]))
    ThicknessFlangePlate = str(float(outputObj["FlangeBolt"]["ThicknessFlangePlate"]))
    FlangeGauge = str(int(outputObj["FlangeBolt"]["FlangeGauge"]))
    FlangePlateDemand = str(float(outputObj["FlangeBolt"]["FlangePlateDemand"]))
    FlangeCapacity = str(float(outputObj["FlangeBolt"]["FlangeCapacity"]))
    FlangeForce = str(float(outputObj['FlangeBolt']['FlangeForce']))
    FlangeForce1 = (float(outputObj['FlangeBolt']['FlangeForce']))
    InnerFlangePlateWidth = str(float(outputObj["FlangeBolt"]["InnerFlangePlateWidth"]))
    flangeplatethick = str(float(outputObj["FlangeBolt"]["flangeplatethick"]))

    WebBlockShear = str(float(outputObj["WebBolt"]["WebBlockShear"]))
    ShearYielding = str(float(outputObj["WebBolt"]["ShearYielding"]))
    ShearRupture = str(float(outputObj["WebBolt"]["ShearRupture"]))
    FlangeCapacity = str(float(outputObj["FlangeBolt"]["FlangeCapacity"]))
    Yielding = str(float(outputObj["FlangeBolt"]["Yielding"]))
    Rupture = str(float(outputObj["FlangeBolt"]["Rupture"]))
    FlangeBlockShear = str(float(outputObj["FlangeBolt"]["FlangeBlockShear"]))
    FlangeBlockShear1 = (float(outputObj["FlangeBolt"]["FlangeBlockShear"]))
    Yielding = str(float(outputObj["FlangeBolt"]["Yielding"]))
    Rupture = str(float(outputObj["FlangeBolt"]["Rupture"]))
    ShearYielding = str(float(outputObj["WebBolt"]["ShearYielding"]))
    ShearRupture = str(float(outputObj["WebBolt"]["ShearRupture"]))

    status = str(outputObj['Bolt']['status'])
    FlangePlateDimension = FlangePlateHeight + ' X ' + FlangePlateWidth + ' X ' + flange_plate_t
    WebPlateDimension = WebPlateHeight + ' X ' + WebPlateWidth + ' X ' + web_plate_t

    corrosive = str(uiObj["detailing"]["is_env_corrosive"])
    design_method = str(uiObj["design"]["design_method"])
    kb = str(outputObj['FlangeBolt']['kb'])
    min_edgend_dist = str(float(uiObj["detailing"]["min_edgend_dist"]))
    dia_hole = str(int(outputObj['FlangeBolt']['DiaHole']))
    dia_hole1 = (int(outputObj['FlangeBolt']['DiaHole']))

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Header of the pdf fetched from dialogbox
    rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoExtendEndplate.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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
        row = [1, "Beam to Beam Spliced Cover Plate", "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [1, "Beam to Beam Spliced Cover Plate", "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('tr')
    rstr += t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1"') + row[2] + t('/td')
    # rstr += t('td class="header1 safe"') + row[3] + t('/td')
    rstr += t('/tr')

    row = [0, "Beam to Beam Spliced Cover Plate", " "]
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

    row = [1, "Connection Title", "Beam to Beam Spliced Cover Plate"]
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

    #
    # row = [1, "Beam Connection", "Bolted"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')

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
    row = [2, "Preference", flange_plate_preference]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
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

    # writing for Flange Splice plate
    row = [2, "Flange Splice Plate ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolt Numbers", "3"]
    row = [3, "Total no. of Bolts", TotalBoltsRequiredF]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [4, "No. of Rows" + " <br> " + "(Parallel to Beam Length; Connecting Each Beam)", str(BoltsRequiredF1/2)]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [4, "No. of Columns <br> (Perpendicular to Beam Length; Connecting Each Beam)", "2"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Gauge (mm)", "0"]
    row = [3, "Gauge (mm)", FlangeGauge]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Pitch (mm)", "100"]
    row = [3, "Pitch (mm)", PitchF]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "End Distance (mm)", "50"]
    row = [3, "End Distance (mm)", EndF]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Edge Distance (mm)", "50"]
    row = [3, "Edge Distance (mm)", EdgeF]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # writing for Web Splice plate
    row = [2, "Web Splice Plate ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolt Numbers", "3"]
    row = [3, "Total no. of Bolts", TotalBoltsRequired]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [4, "No. of Rows <br> (Parallel to Beam Length; Connecting Each Beam)", str(TotalBoltsRequired1/2)]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [4, "No. of Columns <br> (Perpendicular to Beam Length; Connecting Each Beam)", "1"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Gauge (mm)", "0"]
    row = [3, "Gauge (mm)", WebGauge]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Pitch (mm)", "100"]
    row = [3, "Pitch (mm)", Pitch]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "End Distance (mm)", "50"]
    row = [3, "End Distance (mm)", End]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Edge Distance (mm)", "50"]
    row = [3, "Edge Distance (mm)", Edge]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [0, "Assembly ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # row = [1, "Column-Beam Clearance (mm)", "20"]
    row = [1, "Beam-Beam Clearance (mm)", gap]
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
    row = [0, '<object type= "image/PNG" data= "cmpylogoExtendEndplate.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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

    row = [1, "Hole Type", dp_bolt_hole_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Hole Clearance (mm)", bolt_hole_clrnce]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Material Grade (MPa) (overwrite)", bolt_fu]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    if bolt_type == "Friction Grip Bolt":
        row = [1, "Slip Factor", slip_factor]
    else:
        row = [1, "Slip Factor", "N/A"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # --------------------------------      DETAILING      -----------------------------------------------------------------------------------------------
    row = [0, "Detailing ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Type of Edges", type_edge[4:]]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Minimum Edge/End Distance", min_edgend_dist + " times the hole diameter"]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Gap between Beams (mm)", gap]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Are Members Exposed to Corrosive Influences?", corrosive]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # --------------------------------      DESIGN      -----------------------------------------------------------------------------------------------
    row = [0, "Design ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Design Method", design_method]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

    # *************************************************************************************************************************
    # Header of the pdf fetched from dialogbox
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoExtendEndplate.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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
    # Design Check - Flange Splice Plate

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
    row = [0, "Design Check: Flange Splice Plate", " "]
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
    n_e = str(1)
    if BearingCapacityF == "N/A":
        row = [0, "Bolt shear capacity (kN)", " ",
               "<i>V</i><sub>dsf</sub> = ((" + slip_factor + " * " + n_e + " * " + k_h + " * " + F_0 +
               ") / (1.25)) = " + ShearCapacityF + "<br> [cl. 10.4.3]", ""]
    else:
        row = [0, "Bolt shear capacity (kN)", " ",
               "<i>V</i><sub>dsb</sub> = (" + beam_fu + "*" + const + "*" + bolt_diameter + "*" + bolt_diameter +
               ")/(&#8730;3*1.25*1000) = " + ShearCapacityF + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if BearingCapacityF == "N/A":
        row = [0, "Bolt bearing capacity (kN)", "", "N/A", ""]
    else:
        row = [0, "Bolt bearing capacity (kN)", "",
               " <i>V</i><sub>dpb</sub> = (2.5 * " + kb + " * " + bolt_diameter + " * " + beam_w_t + " * " + beam_fu + ") / (1.25 * 1000)  = " +
               BearingCapacityF + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    if BearingCapacityF == "N/A":
        boltCapacity = str(float(ShearCapacityF))
        row = [0, "Bolt capacity (kN)", "", boltCapacity, ""]
    else:
        # boltCapacity = bearingcapacity if bearingcapacity < shearCapacity else shearCapacity
        boltCapacity = str(min(float(ShearCapacityF), float(BearingCapacityF)))
        row = [0, "Bolt capacity (kN)", "", "min (" + ShearCapacityF + ", " + BearingCapacityF + ") = " + boltCapacity,
               ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
    bolts = str(round(1.05 * (float(FlangeForce) / float(boltCapacity)), 1))
    if float(bolts) > int(BoltsRequiredF):
        row = [0, "No. of bolts parallel to beam length; connecting each beam, ", "(1.05 * " + FlangeForce + ") / " + boltCapacity + "<br>" + " = " + bolts, BoltsRequiredF,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "No. of bolts parallel to beam length; connecting each beam", "(1.05 * " + FlangeForce + ") / " + boltCapacity + "<br>" + " = " + bolts, BoltsRequiredF,
               " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    row = [0, "No. of rows of bolt (parallel to beam length; connecting each beam)", "", str(BoltsRequiredF1/2), ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No. of column(s) of bolt (perpendicular to beam length; connecting each beam)", "", "2", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')


    if float(bolts) > int(BoltsRequiredF):
        row = [0, "Total no. of bolts", "4" + " * " + BoltsRequiredF + " = " + TotalBoltsRequiredF, TotalBoltsRequiredF,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Total no. of bolts", "4" + " * " + BoltsRequiredF + " = " + TotalBoltsRequiredF, TotalBoltsRequiredF,
               " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    # # row =[0,"No. of bolts per column"," ","3"]
    # row = [0, "No. of bolts per column", " ", noOfRows, ""]
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')
    #
    # rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    minPitch = str((2.5 * float(bolt_diameter)))
    MaxPitchF = str(float(outputObj['FlangeBolt']['MaxPitchF']))
    FlangeTThinner = str(float(outputObj["FlangeBolt"]["FlangeTThinner"]))
    #maxPitch = str(300) if 32 * float(beam_f_t) > 300 else str((math.ceil(32 * float(beam_w_t))))
    if float(PitchF) < float(minPitch):
        row = [0, "Bolt pitch (mm)", " &#8805; 2.5 * " + bolt_diameter + " = " + minPitch + ",  &#8804; min(32 * " + FlangeTThinner + ", 300) = " + MaxPitchF + "<br> [cl. 10.2.2]",
               PitchF, "<p align=left style=color:red><b>Fail</b></p>"]

    # elif str(PitchF) > (MaxPitchF):
    #     row = [0, "Bolt pitch (mm)",
    #            " &#8805; 2.5 * " + bolt_diameter + " = " + minPitch + ",  &#8804; min(32 * " + FlangeTThinner + ", 300) = " + MaxPitchF + "<br> [cl. 10.2.2]",
    #            PitchF, "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Bolt pitch (mm)", " &#8805; 2.5 * " + bolt_diameter + " = " + minPitch + ",  &#8804; min(32 * " + FlangeTThinner + ", 300) = " + MaxPitchF + "<br> [cl. 10.2.2]",
               PitchF, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    minGauge = str(int(2.5 * float(bolt_diameter)))
    if float(FlangeGauge) < float(minGauge):
        row = [0, "Bolt gauge (mm)", " &#8805; 2.5 * " + bolt_diameter + " = " + minGauge + ", &#8804; min(32 * " + FlangeTThinner + ", 300) = " + MaxPitchF + " <br> [cl. 10.2.2]",
               FlangeGauge, "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Bolt gauge (mm)", " &#8805; 2.5 * " + bolt_diameter + " = " + minGauge + ", &#8804; min(32 * " + FlangeTThinner + ", 300) = " + MaxPitchF + " <br> [cl. 10.2.2]",
               FlangeGauge, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    minEnd = str(int(float(min_edgend_dist) * float(dia_hole)))
    maxEnd = str(float(12 * float(beam_w_t)))
    if float(EndF) < float(minEnd):
        row = [0, "End distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + minEnd + ", &#8804; 12 * " + FlangeTThinner + " = " + maxEnd + " <br> [cl. 10.2.4]",
               EndF,
               "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "End distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + minEnd + ", &#8804; 12 * " + FlangeTThinner + " = " + maxEnd + " <br> [cl. 10.2.4]",
               EndF, "<p align=left style=color:green><b>Pass</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')

    minEdge = str(int(float(min_edgend_dist) * float(dia_hole)))
    maxEdge = str(float(12 * float(beam_w_t)))
    if float(EdgeF) < float(minEdge):
        row = [0, "Edge distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + minEdge + ", &#8804; 12 * " + FlangeTThinner + " = " + maxEdge + " <br> [cl. 10.2.4]",
               EdgeF, "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Edge distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + minEdge + ", &#8804; 12 * " + FlangeTThinner + " = " + maxEdge + " <br> [cl. 10.2.4]",
               EdgeF, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    if FlangeBlockShear1 < FlangeForce1:
        row = [0, "Block shear capacity (kN)", " &#8805; " + FlangeForce, "<i>V</i><sub>db</sub> = " + FlangeBlockShear + "<br> [cl. 6.4.1]" + "<br>", "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Block shear capacity (kN)", " &#8805; " + FlangeForce, "<i>V</i><sub>db</sub> = " + FlangeBlockShear + "<br> [cl. 6.4.1]" + "<br>", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    if float(Yielding) < FlangeForce1:
        row = [0, "Strength due to yielding of gross section (kN)", " &#8805; " + FlangeForce, "<i>V</i><sub>db</sub> = " + Yielding + "<br> [cl. 6.2]" + "<br>", "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Strength due to yielding of gross section (kN)", " &#8805; " + FlangeForce, "<i>V</i><sub>db</sub> = " + Yielding + "<br> [cl. 6.2]" + "<br>", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    if float(Rupture) < FlangeForce1:
        row = [0, "Strength due to rupture of critical section (kN)", " &#8805; " + FlangeForce, "<i>V</i><sub>db</sub> = " + Rupture + "<br> [cl. 6.3.1]" + "<br>", "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Strength due to rupture of critical section (kN)", " &#8805; " + FlangeForce, "<i>V</i><sub>db</sub> = " + Rupture + "<br> [cl. 6.3.1]" + "<br>", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Plate thickness (mm)","(5*140*1000)/(300*250)= 9.33","10"]
    if flange_plate_preference == "Outside":
        flangeplatethick2 = str(float(flangeplatethick))
        if float(flange_plate_t) < float(flangeplatethick2):
            row = [0, "Flange splice plate thickness (mm)",
                   flangeplatethick + "<br> [Cl. 6.2]", flange_plate_t, "<p align=left style=color:red><b>Fail</b></p>"]

        else:
            row = [0, "Flange splice plate thickness (mm)", flangeplatethick +
                   "<br> [Cl. 6.2]", flange_plate_t, "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        rstr += t('tr')

        # Height of flange splice plate
        minPlateHeight1 = (2 * (min(beam_b1, 225)) + gap1)
        minPlateHeight = str(minPlateHeight1)
        if float(FlangePlateHeight) < float(minPlateHeight):
            row = [0, "Flange splice plate height (mm)", " &#8805; " + "2 * min("+ beam_b +", 225)" + " + " + gap + " = " + minPlateHeight +
                   "<br> [SCI - 6th edition, page 754]", FlangePlateHeight, "<p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Flange splice plate height (mm)", " &#8805; " + "2 * min("+ beam_b +", 225)" + " + " + gap + " = " + minPlateHeight +
                   "<br> [SCI - 6th edition, page-754]", FlangePlateHeight, "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        rstr += t('tr')

        # Width of flange splice plate
        minPlateWidth = str(beam_b1 - 20) # Beam width - 20 mm (half inch on each side of the flange)
        if float(FlangePlateWidth) < float(minPlateWidth):
            row = [0, "Flange splice plate width (mm)", " &#8805; " + minPlateWidth + ", &#8804;" + beam_b, FlangePlateWidth, "<p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Flange splice plate width (mm)", " &#8805; " + minPlateWidth + ", &#8804;" + beam_b, FlangePlateWidth, "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

    elif flange_plate_preference == "Outside + Inside":
        flangeplatethick2 = round(float(flangeplatethick), 2)
        flangeplatethick1 = str(float(flangeplatethick2 / 2))
        if float(flange_plate_t) < float(flangeplatethick1):
            row = [0, "Outer flange splice plate thickness (mm)",
                   flangeplatethick1 + "<br> [Cl. 6.2]", flange_plate_t, "<p align=left style=color:red><b>Fail</b></p>"]

        else:
            row = [0, "Outer flange splice plate thickness (mm)", flangeplatethick1 +
                   "<br> [Cl. 6.2]", flange_plate_t, "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        rstr += t('tr')

        # Height of flange splice plate
        minPlateHeight1 = (2 * (min(beam_b1, 225)) + gap1)
        minPlateHeight = str(minPlateHeight1)
        if float(FlangePlateHeight) < float(minPlateHeight):
            row = [0, "Outer flange splice plate height (mm)",
                   " &#8805; " + "2 * min(" + beam_b + ", 225)" + " + " + gap + " = " + minPlateHeight +
                   "<br> [SCI - 6th edition, page 754]", FlangePlateHeight,
                   "<p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Outer flange splice plate height (mm)",
                   " &#8805; " + "2 * min(" + beam_b + ", 225)" + " + " + gap + " = " + minPlateHeight +
                   "<br> [SCI - 6th edition, page-754]", FlangePlateHeight,
                   "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        rstr += t('tr')

        # Width of flange splice plate
        minPlateWidth = str(beam_b1 - 20)  # Beam width - 20 mm (half inch on each side of the flange)
        if float(FlangePlateWidth) < float(minPlateWidth):
            row = [0, "Outer flange splice plate width (mm)", " &#8805; " + minPlateWidth + ", &#8804;" + beam_b, FlangePlateWidth,
                   "<p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Outer flange splice plate width (mm)", " &#8805; " + minPlateWidth + ", &#8804;" + beam_b, FlangePlateWidth,
                   "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        if float(flange_plate_t) < float(flangeplatethick1):
            row = [0, "Inner flange splice plate thickness (mm)",
                   flangeplatethick1 + "<br> [Cl. 6.2]", flange_plate_t, "<p align=left style=color:red><b>Fail</b></p>"]

        else:
            row = [0, "Inner flange splice plate thickness (mm)", flangeplatethick1 +
                   "<br> [Cl. 6.2]", flange_plate_t, "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        rstr += t('tr')

        # Height of flange splice plate
        minPlateHeight1 = (2 * (min(beam_b1, 225)) + gap1)
        minPlateHeight = str(minPlateHeight1)
        if float(FlangePlateHeight) < float(minPlateHeight):
            row = [0, "Inner flange splice plate height (mm)",
                   " &#8805; " + "2 * min(" + beam_b + ", 225)" + " + " + gap + " = " + minPlateHeight +
                   "<br> [SCI - 6th edition, page 754]", FlangePlateHeight,
                   "<p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Inner flange splice plate height (mm)",
                   " &#8805; " + "2 * min(" + beam_b + ", 225)" + " + " + gap + " = " + minPlateHeight +
                   "<br> [SCI - 6th edition, page-754]", FlangePlateHeight,
                   "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        rstr += t('tr')

        # Width of flange splice plate
        minPlateWidthI = str(int(2 * int(EdgeF)))
        if float(InnerFlangePlateWidth) < float(minPlateWidthI):
            row = [0, "Inner flange splice plate width (mm)", " &#8805; " + minPlateWidthI, InnerFlangePlateWidth,
                   "<p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Inner flange splice plate width (mm)", " &#8805; " + minPlateWidthI, InnerFlangePlateWidth,
                   "<p align=left style=color:green><b>Pass</b></p>"]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

    # *************************************************************************************************************************
    # *************************************************************************************************************************
    # Header of the pdf fetched from dialogbox
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoExtendEndplate.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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
    # *************************************************************************************************************************
    # Design Check ## Web Splice Plate

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
    row = [0, "Design Check: Web Splice Plate", " "]
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
    n_e = str(2)
    if BearingCapacity == "N/A":
        row = [0, "Bolt shear capacity (kN)", " ",
               "<i>V</i><sub>dsf</sub> = ((" + slip_factor + " * " + n_e + " * " + k_h + " * " + F_0 +
               ") / (1.25)) = " + ShearCapacity + "<br> [cl. 10.4.3]", ""]
    else:
        row = [0, "Bolt shear capacity (kN)", " ",
               "<i>V</i><sub>dsb</sub> = (" + beam_fu + "*" + const + "*" + bolt_diameter + "*" + bolt_diameter +
               ")/(&#8730;3*1.25*1000) = " + ShearCapacity + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if BearingCapacity == "N/A":
        row = [0, "Bolt bearing capacity (kN)", "", "N/A", ""]
    else:
        row = [0, "Bolt bearing capacity (kN)", "",
               " <i>V</i><sub>dpb</sub> = (2.5 * " + kb + " * " + bolt_diameter + " * " + web_plate_t + " * " + beam_fu + ") / (1.25 * 1000)  = " +
               BearingCapacity + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    if BearingCapacity == "N/A":
        boltCapacityW = (ShearCapacity)
        row = [0, "Bolt capacity (kN)", "", boltCapacityW, ""]
    else:
        # boltCapacityW = bearingcapacity if bearingcapacity < shearCapacity else shearCapacity
        boltCapacityW = str(min(float(ShearCapacity), float(BearingCapacity)))
        row = [0, "Bolt capacity (kN)", "", "min (" + ShearCapacity + ", " + BearingCapacity + ") = " + boltCapacityW,
               ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
    boltsW1 = round(float(shear_load) / float(boltCapacityW), 2)
    boltsW2 = str(boltsW1)
    boltsW = str(float(shear_load) / float(boltCapacityW))
    if float(boltsW) > float(BoltsRequired):
        row = [0, "No. of bolts parallel to beam length; connecting each beam", shear_load + " / " + boltCapacityW + " = " + boltsW2, BoltsRequired,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "No. of bolts parallel to beam length; connecting each beam", shear_load + " / " + boltCapacityW + " = " + boltsW2, BoltsRequired,
               " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    row = [0, "No. of rows of bolt (parallel to beam length; connecting each beam)", "", str(TotalBoltsRequired1/2), ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No. of column(s) of bolt (perpendicular to beam length; connecting each beam)", "", "1", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    if float(boltsW) > float(BoltsRequired):
        row = [0, "Total no. of bolts", "2" + " * " + BoltsRequired + " = " + TotalBoltsRequired,
               TotalBoltsRequired,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Total no. of bolts", "2" + " * " + BoltsRequired + " = " + TotalBoltsRequired,
               TotalBoltsRequired,
               " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    # # row =[0,"No. of bolts per column"," ","3"]
    # row = [0, "No. of bolts per column", " ", noOfRows, ""]
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')
    #
    # rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    minPitch = str((2.5 * float(bolt_diameter)))
    # minPitch1 = str((2.5 * float(bolt_diameter)))
    MaxPitchF = str(float(outputObj['FlangeBolt']['MaxPitchF']))
    # maxPitch = str(300) if 32 * float(beam_f_t) > 300 else str((math.ceil(32 * float(beam_w_t))))
    if float(Pitch) < float(minPitch):
        row = [0, "Bolt pitch (mm)",
               " &#8805; 2.5 * " + bolt_diameter + " = " + minPitch + ",  &#8804; min(32 * " + beam_w_t + ", 300) = " + MaxPitchF + "<br> [cl. 10.2.2]",
               Pitch, "<p align=left style=color:red><b>Fail</b></p>"]

    # elif str(PitchF) > (MaxPitchF):
    #     row = [0, "Bolt pitch (mm)",
    #            " &#8805; 2.5 * " + bolt_diameter + " = " + minPitch + ",  &#8804; min(32 * " + FlangeTThinner + ", 300) = " + MaxPitchF + "<br> [cl. 10.2.2]",
    #            PitchF, "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Bolt pitch (mm)",
               " &#8805; 2.5 * " + bolt_diameter + " = " + minPitch + ",  &#8804; min(32 * " + beam_w_t + ", 300) = " + MaxPitchF + "<br> [cl. 10.2.2]",
               Pitch, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    minGauge = str(int(2.5 * float(bolt_diameter)))
    if float(WebGauge) < float(minGauge):
        row = [0, "Bolt gauge (mm)",
               " &#8805; 2.5 * " + bolt_diameter + " = " + minGauge + ", &#8804; min(32 * " + beam_w_t + ", 300) = " + MaxPitchF + " <br> [cl. 10.2.2]",
               WebGauge, "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Bolt gauge (mm)",
               " &#8805; 2.5 * " + bolt_diameter + " = " + minGauge + ", &#8804; min(32 * " + beam_w_t + ", 300) = " + MaxPitchF + " <br> [cl. 10.2.2]",
               WebGauge, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    minEnd = str(int(float(min_edgend_dist) * float(dia_hole)))
    maxEnd = str(float(12 * float(beam_w_t)))
    if float(EndF) < float(minEnd):
        row = [0, "End distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + minEnd + ", &#8804; 12 * " + beam_w_t + " = " + maxEnd + " <br> [cl. 10.2.4]",
               EndF,
               "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "End distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + minEnd + ", &#8804; 12 * " + beam_w_t + " = " + maxEnd + " <br> [cl. 10.2.4]",
               EndF, "<p align=left style=color:green><b>Pass</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')

    minEdge = str(int(float(min_edgend_dist) * float(dia_hole)))
    maxEdge = str(float(12 * float(beam_w_t)))
    if float(EdgeF) < float(minEdge):
        row = [0, "Edge distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + minEdge + ", &#8804; 12 * " + beam_w_t + " = " + maxEdge + " <br> [cl. 10.2.4]",
               Edge, "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Edge distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + minEdge + ", &#8804; 12 * " + beam_w_t + " = " + maxEdge + " <br> [cl. 10.2.4]",
               Edge, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    if float(WebBlockShear) < float(shear_load):
        row = [0, "Block shear capacity (kN)", " &#8805; " + shear_load,
               "<i>V</i><sub>db</sub> = " + WebBlockShear + "<br> [cl. 6.4.1]" + "<br>", "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Block shear capacity (kN)", " &#8805; " + shear_load,
               "<i>V</i><sub>db</sub> = " + WebBlockShear + "<br> [cl. 6.4.1]" + "<br>",
               "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    if float(ShearYielding) < float(shear_load):
        row = [0, "Shear yielding (kN)", " &#8805; " + shear_load,
               "<i>V</i><sub>db</sub> = " + ShearYielding + "<br> [cl. 8.4.1]" + "<br>", "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Shear yielding (kN)", " &#8805; " + shear_load,
               "<i>V</i><sub>db</sub> = " + ShearYielding + "<br> [cl. 8.4.1]" + "<br>", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    if float(ShearRupture) < float(shear_load):
        row = [0, "Shear rupture (kN)", " &#8805; " + shear_load,
               "<i>V</i><sub>db</sub> = " + ShearRupture + "<br> [cl. 8.4.1]" + "<br>",
               "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Shear rupture (kN)", " &#8805; " + shear_load,
               "<i>V</i><sub>db</sub> = " + ShearRupture + "<br> [cl. 8.4.1]" + "<br>", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Plate thickness (mm)","(5*140*1000)/(300*250)= 9.33","10"]
    minPlateThickW1 = round(((5 * float(shear_load) * 1000) / (beam_fy1 * 0.5 * float(beam_d))), 1)
    minPlateThickW = str(minPlateThickW1)
    webplatet = str(max(minPlateThickW1, (float(beam_w_t) / 2)))
    beam_w_t2 = str(float(beam_w_t) / 2)

    if float(web_plate_t) < float(webplatet):
        row = [0, "Web plate thickness (mm)",
               " &#8805; " + "max(" + minPlateThickW + ", " + beam_w_t2 + ")" + " = " + webplatet, web_plate_t, "<p align=left style=color:red><b>Fail</b></p>"]

    else:
        row = [0, "Web plate thickness (mm)",
               " &#8805; " + "max(" + minPlateThickW + ", " + beam_w_t2 + ")" + " = " + webplatet, web_plate_t, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    # Height of flange splice plate
    minPlateHeight1W = float(beam_d) - 2 * float(beam_f_t) - 2 * float(beam_r1) - 2 * 10
    minPlateHeightW = str(minPlateHeight1W)
    if float(WebPlateHeight) > float(minPlateHeightW):
        row = [0, "Web plate height (mm)",
               " &#8804; " + beam_d + " - 2 * " + beam_f_t + " - 2 * " + beam_r1 + " - 2 * 5"+ " = " + minPlateHeightW +
               "<br> [SCI - 6th edition, page 754]", WebPlateHeight, "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Web plate height (mm)",
               " &#8804; " + beam_d + " - 2 * " + beam_f_t + " - 2 * " + beam_r1 + " - 2 * 5"+ " = " + minPlateHeightW +
               "<br> [SCI - 6th edition, page 754]", WebPlateHeight,
               "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    # Width of flange splice plate
    minPlateWidthW = str(beam_b1 - 20)  # Beam width - 20 mm (half inch on each side of the flange)
    # if (FlangePlateWidth) < (minPlateWidthW):
    row = [0, "Web plate width (mm)", "", WebPlateWidth, ""]
    # else:
    #     row = [0, "Plate width (mm)", " &#8805; " + minPlateWidthW + " &#8804;, " + beam_b, WebPlateWidth, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

    # *************************************************************************************************************************
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    # *************************************************************************************************************************
    # *************************************************************************************************************************
    # Header of the pdf fetched from dialogbox
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoExtendEndplate.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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
    # Diagram

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

    row = [0, "Views", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    png = folder + "/images_html/3D_Model.png"
    datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png

    side = folder + "/images_html/coverboltedSide.png"
    dataside = '<object type="image/PNG" data= %s width ="400"></object>' % side

    top = folder + "/images_html/coverboltedTop.png"
    datatop = '<object type="image/PNG" data= %s width ="400"></object>' % top

    front = folder + "/images_html/coverboltedFront.png"
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
    # Header of the pdf fetched from dialogbox
    if flange_plate_preference == "Outside + Inside":
        rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
        rstr += t('tr')
        row = [0, '<object type= "image/PNG" data= "cmpylogoExtendEndplate.png" height=60 ></object>',
               '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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
        # Diagram

        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

        row = [0, "Views", " "]
        rstr += t('tr')
        rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
        rstr += t('/tr')
        png = folder + "/images_html/3D_Model.png"
        datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png

        plan = folder + "/images_html/coverboltedPlan.png"
        dataplan = '<object type="image/PNG" data= %s width ="400"></object>' % plan

        row = [0, dataplan]
        rstr += t('tr')
        rstr += t('td align="center" class="header2"') + space(row[0]) + row[1] + t('/d')
        rstr += t('/tr')

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

    # *************************************************************************************************************************
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Header of the pdf fetched from dialogbox
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoExtendEndplate.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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
