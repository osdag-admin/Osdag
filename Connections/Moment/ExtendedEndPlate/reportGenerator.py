"""
Created on 4th January, 2018

@author: Danish Ansari
"""

from __builtin__ import str
import time
import math
import os
import pickle
from Connections.connection_calculations import ConnectionCalculations

######################################################################
# Start of Report
def save_html(outObj, uiObj, dictbeamdata, filename, reportsummary, folder):
    filename = filename
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

######################################################################
# Project Summary data
    companyname = str(reportsummary["ProfileSummary"]['CompanyName'])
    companylogo = str(reportsummary["ProfileSummary"]['CompanyLogo'])
    groupteamname = str(reportsummary["ProfileSummary"]['Group/TeamName'])
    designer = str(reportsummary["ProfileSummary"]['Designer'])
    projecttitle = str(reportsummary['ProjectTitle'])
    subtitle = str(reportsummary['Subtitle'])
    jobnumber = str(reportsummary['JobNumber'])
    client = str(reportsummary['Client'])
    addtionalcomments = str(reportsummary['AdditionalComments'])

######################################################################
# Extended End Plate Data

    # Section properties
    beam_tw = float(dictbeamdata["tw"])
    beam_tf = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])
    beam_B = float(dictbeamdata["B"])
    beam_R1 = float(dictbeamdata["R1"])

    # Data from Input dock
    connectivity = str(uiObj['Member']['Connectivity'])
    beam_sec = uiObj['Member']['BeamSection']
    beam_fu = str(float(uiObj['Member']['fu (MPa)']))
    beam_fy = str(float(uiObj['Member']['fy (MPa)']))

    factored_moment = str(float(uiObj['Load']['Moment (kNm)']))
    factored_shear_load = str(float(uiObj['Load']['ShearForce (kN)']))

    factored_axial_load = str(uiObj['Load']['AxialForce (kN)'])

    bolt_dia = str(int(uiObj['Bolt']['Diameter (mm)']))
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = str(float(uiObj['Bolt']['Grade']))
    bolt_fu = str((int(float(bolt_grade)) * 100))
    # bolt_fy = str((float(bolt_grade) - int(float(bolt_grade)))) * bolt_fu
    # bolt_fy = (float(bolt_grade) - float(int(float(bolt_grade)))) * bolt_fu
    bolt_fy = str(float(outObj['Bolt']['BoltFy']))
    net_area_thread = {12: str(84.3), 16: str(157), 20: str(245), 22: str(303), 24: str(353), 27: str(459), 30: str(561), 36: str(817)}[int(bolt_dia)]
    net_area_shank = {12: str(113), 16: str(201), 20: str(314), 22: str(380), 24: str(452), 27: str(572), 30: str(706), 36: str(1017)}[int(bolt_dia)]

    end_plate_thickness = str(float(uiObj['Plate']['Thickness (mm)']))
    end_plate_fu = str(float(uiObj['Member']['fu (MPa)']))
    end_plate_fy = str(float(uiObj['Member']['fy (MPa)']))

    weld_thickness_flange = str(float(uiObj['Weld']['Flange (mm)']))
    weld_thickness_web = str(float(uiObj['Weld']['Web (mm)']))

    # Design Preferences

    bolt_hole_clrnce = str(float(uiObj["bolt"]["bolt_hole_clrnce"]))
    bolt_hole_type = str(uiObj["bolt"]["bolt_hole_type"])
    bolt_grade_fu = str(float(uiObj["bolt"]["bolt_fu"]))
    slip_factor = str(float(uiObj["bolt"]["slip_factor"]))
    bolt_Type = str(uiObj['bolt']['bolt_type'])  # for pre-tensioned/ non- pretensioned bolts

    typeof_weld = str(uiObj["weld"]["typeof_weld"])
    safety_factor = str(float(uiObj["weld"]["safety_factor"]))
    fu_overwrite = str(float(uiObj["weld"]["fu_overwrite"]))

    typeof_edge = str(uiObj["detailing"]["typeof_edge"])
    min_edgend_dist = str(float(uiObj["detailing"]["min_edgend_dist"]))  # factor: 1.7 or 1.5 depending on type of edge, IS 800- Cl 10.2.4.2
    # gap = float(uiObj["detailing"]["gap"])
    corrosive = str(uiObj["detailing"]["is_env_corrosive"])
    design_method = str(uiObj["design"]["design_method"])

    # Bolt
    # print "out", outObj
    number_of_bolts = str(float(int(outObj['Bolt']['NumberOfBolts'])))
    number_of_rows = str(int(round(outObj['Bolt']['NumberOfRows'])))
    bolts_per_column = str(outObj['Bolt']['BoltsPerColumn'])
    end_distance = str(float(outObj['Bolt']['End']))
    edge_distance = str(float(outObj['Bolt']['Edge']))
    gauge_distance = str(float(outObj['Bolt']['Gauge']))
    tension_capacity = str(float(outObj['Bolt']['TensionCapacity']))
    bearingcapacity = str(outObj['Bolt']['BearingCapacity'])
    shearcapacity = str(outObj['Bolt']['ShearCapacity'])
    boltcapacity = str(outObj['Bolt']['BoltCapacity'])
    kb = str(outObj['Bolt']['kb'])
    plate_thk = str(outObj['Bolt']['SumPlateThick'])  # Sum of plate thickness experiencing bearing in same direction
    combinedcapacity = str(float(outObj['Bolt']['CombinedCapacity']))
    if bolt_type == "HSFG":
        Vsf = str(float(outObj['Bolt']['Vsf']))
        Vdf = str(float(outObj['Bolt']['Vdf']))
        Tf = str(float(outObj['Bolt']['Tf']))
        Tdf = str(float(outObj['Bolt']['Tdf']))
    else:
        Vsb = str(float(outObj['Bolt']['Vsb']))
        Vdb = str(float(outObj['Bolt']['Vdb']))
        Tb = str(float(outObj['Bolt']['Tb']))
        Tdb = str(float(outObj['Bolt']['Tdb']))

    pitch_mini = str(outObj['Bolt']['PitchMini'])
    pitch_max = str(outObj['Bolt']['PitchMax'])

    gauge_mini = str(float(pitch_mini))
    gauge_max = str(float(pitch_max))
    end_mini = str(outObj['Bolt']['EndMini'])
    end_max = str(outObj['Bolt']['EndMax'])
    edge_mini = str(end_mini)
    edge_max = str(end_max)
    dia_hole = str(int(outObj['Bolt']['DiaHole']))

    # Plate
    tp_required = str(float(outObj['Plate']['ThickRequired']))
    be = float(beam_B / 2)
    b_e = str(be)
    M_p = str(float(outObj['Plate']['Mp']))
    plate_height = str(float(outObj['Plate']['Height']))
    plate_width = str(float(outObj['Plate']['Width']))
    plate_moment_demand = str(float(outObj['Plate']['MomentDemand']))
    plate_moment_capacity = str(float(outObj['Plate']['MomentCapacity']))

    # Weld
    critical_stress_flange = str(float(outObj['Weld']['CriticalStressflange']))
    critical_stress_web = str(float(outObj['Weld']['CriticalStressWeb']))
    weld_strength = str(float(outObj['Weld']['WeldStrength']))
    force_flange = str(float(outObj['Weld']['ForceFlange']))
    effective_length_flange = float(outObj['Weld']['LeffectiveFlange'])
    effective_length_web = float(outObj['Weld']['LeffectiveWeb'])
    fa_web = float(outObj['Weld']['FaWeb'])
    q_web = float(outObj['Weld']['Qweb'])
    resultant = float(outObj['Weld']['Resultant'])
    capacity_flange = float(outObj['Weld']['UnitCapacity'])

    # Stiffener
    stiffener_height = str(float(outObj['Stiffener']['Height']))
    stiffener_length = str(float(outObj['Stiffener']['Length']))
    stiffener_thickness = str(float(outObj['Stiffener']['Thickness']))

    # Calling pitch distance values from Output dict of calc file
    if str(int(float(number_of_bolts))) == str(8):
        pitch_distance = str(float(outObj['Bolt']['Pitch']))
        tension_critical = str(float(outObj['Bolt']['TensionCritical']))
        prying_force = str(float(outObj['Bolt']['PryingForce']))
    elif str(int(float(number_of_bolts))) == str(12):
        pitch_distance_2_3 = str(float(outObj['Bolt']['Pitch23']))
        pitch_distance_3_4 = str(float(outObj['Bolt']['Pitch34']))
        pitch_distance_4_5 = str(float(outObj['Bolt']['Pitch45']))
        tension_critical = str(float(outObj['Bolt']['TensionCritical']))
        prying_force = str(float(outObj['Bolt']['PryingForce']))
    elif str(int(float(number_of_bolts))) == str(16):
        pitch_distance_2_3 = str(float(outObj['Bolt']['Pitch23']))
        pitch_distance_3_4 = str(float(outObj['Bolt']['Pitch34']))
        pitch_distance_4_5 = str(float(outObj['Bolt']['Pitch45']))
        pitch_distance_5_6 = str(float(outObj['Bolt']['Pitch56']))
        pitch_distance_6_7 = str(float(outObj['Bolt']['Pitch67']))
        tension_critical = str(float(outObj['Bolt']['TensionCritical']))
        prying_force = str(float(outObj['Bolt']['PryingForce']))
    elif str(int(float(number_of_bolts))) == str(20):
        pitch_distance_1_2 = str(float(outObj['Bolt']['Pitch']))
        pitch_distance_3_4 = str(float(outObj['Bolt']['Pitch']))
        pitch_distance_4_5 = str(float(outObj['Bolt']['Pitch']))
        pitch_distance_5_6 = str(float(outObj['Bolt']['Pitch']))
        pitch_distance_6_7 = str(float(outObj['Bolt']['Pitch']))
        pitch_distance_7_8 = str(float(outObj['Bolt']['Pitch']))
        pitch_distance_9_10 = str(float(outObj['Bolt']['Pitch']))
        tension_critical = str(float(outObj['Bolt']['TensionCritical']))
        prying_force = str(float(outObj['Bolt']['PryingForce']))

    # Calls from connection calculations file
    k_h = str(float(ConnectionCalculations.calculate_k_h(bolt_hole_type)))
    F_0 = str(float(ConnectionCalculations.proof_load_F_0(bolt_dia, bolt_fu)))

    # End Plate

    plateDimension = str(plate_height) + " X " + str(plate_width) + " X " + str(end_plate_thickness)

    status = str(outObj['Bolt']['status'])

    ######################################################################
    # Header of the pdf fetched from dialogbox

    rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoExtendEndplate.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Company Name']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
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

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Page 1 & 2 of report
    # Design Conclusion

    rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100% ')

    row = [0, 'Design Conclusion', "IS800:2007/Limit state design"]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    if status == 'True':
        row = [1, "Extended End Plate", "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [1, "Extended End Plate", "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('tr')
    rstr += t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [0, "Extended End Plate", " "]
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

    # TODO: should we add Single Extended End Plate
    # row = [1, "Connection Title", " Single Fin Plate"]
    row = [1, "Connection Title", "Extended End Plate"]
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

    row = [1, "Beam Connection", "Bolted and Welded"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [0, "Loading (Factored Load) ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Bending Moment (kNm)", factored_moment]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Shear Force (kN)", factored_shear_load]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Axial Force (kN)", factored_axial_load]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [0, "Components ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

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

    # TODO: Check with sir weather to add below lines (Danish)
    # row = [2, "Hole", bolt_hole_type]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')

    row = [1, "Plate Section", plateDimension]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Thickness (mm)", end_plate_thickness]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Width (mm)", plate_width]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Depth (mm)", plate_height]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Hole", bolt_hole_type]
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

    row = [2, "Weld at Flange (mm)", weld_thickness_flange]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Weld at Web (mm)", weld_thickness_web]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Bolts ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [2, "Type", bolt_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Grade", bolt_grade]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Diameter (mm)", bolt_dia]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Bolt Numbers", number_of_bolts]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Columns (Vertical Lines)", "2"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Bolts Per Column", number_of_rows]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "End Distance (mm)", end_distance]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Edge Distance (mm)", edge_distance]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Gauge Distance (mm)", gauge_distance]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')


    row = [2, "Pitch Distance (mm)", ]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [1, "Pitch Distance (mm)", ]
    # rstr += t('tr')
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')

    # TODO: Create a table for pitch distance values
    if number_of_bolts == 8:
        row = [2, "Pitch (mm)", pitch_distance]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')
    elif number_of_bolts == 12:
        row = [2, "Pitch_2_3 (mm)", pitch_distance_2_3]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_3_4 (mm)", pitch_distance_3_4]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_4_5 (mm)", pitch_distance_4_5]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')
    elif number_of_bolts == 16:
        row = [2, "Pitch_2_3 (mm)", pitch_distance_2_3]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_3_4 (mm)", pitch_distance_3_4]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_4_5 (mm)", pitch_distance_4_5]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_5_6 (mm)", pitch_distance_5_6]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_6_7 (mm)", pitch_distance_6_7]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')
    elif number_of_bolts == 20:
        row = [2, "Pitch_1_2 (mm)", pitch_distance_1_2]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_3_4 (mm)", pitch_distance_3_4]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_4_5 (mm)", pitch_distance_4_5]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_5_6 (mm)", pitch_distance_5_6]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_6_7 (mm)", pitch_distance_6_7]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_7_8 (mm)", pitch_distance_7_8]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

        row = [2, "Pitch_9_10 (mm)", pitch_distance_9_10]
        rstr += t('tr')
        rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2 "') + row[2] + t('/td')
        rstr += t('/tr')

    row = [0, "Assembly ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Beam-Beam Clearance (mm)", "N/A"]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # page break
    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')
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

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Start of page 3
    # Design Preferences

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
    row = [0, "Design Preferences", " "]
    rstr += t('tr')
    rstr += t('td colspan="4" class="detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Bolt &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
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

    row = [1, "Material Grade (MPa) (overwrite)", bolt_grade_fu]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    if bolt_type == "HSFG":
        row = [1, "Slip factor", slip_factor]
    else:
        row = [1, "Slip factor", "N/A"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    if bolt_Type == "Pretensioned":
        row = [1, "Beta (pre-tensioned bolt)", str(1)]
    else:
        row = [1, "Beta (non pre-tensioned)", str(2)]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Weld &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    row = [0, "Weld ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Type of Weld", typeof_weld]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Material Grade (MPa) (overwrite)", fu_overwrite]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Detailing &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    row = [0, "Detailing ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Type of Edges", typeof_edge]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Minimum Edge-End Distance", min_edgend_dist + " times the hole diameter"]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # TODO: Should there be a gap b/w beams?
    # row = [1, "Gap between Beam and Column (mm)", gap]
    # rstr += t('tr')
    # rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + row[2] + t('/td')
    # rstr += t('/tr')

    row = [1, "Are members exposed to corrosive influences?", corrosive]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Design &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
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

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Bolt &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Start of page 4 & 5 (Design Checks)

    # Header of the pdf fetched from dialogue

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

    # Check for tension in critical bolt
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

    row = [0, "Tension in critical bolt (kN)", " Tension in bolt due to external factored moment + Prying force = " + tension_critical + "+" + prying_force + " = " + str(float(tension_critical) + float(prying_force)) + " <br> [cl. 10.4.7] ", " ", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Check for Tension capacity of bolt
    # TODO: Check for bearing bolt type (Danish)
    rstr += t('tr')
    tension_critical_bolt = str(float(tension_critical) + float(prying_force))

    if tension_critical_bolt > tension_capacity:
        row = [0, "Tension capacity of critical bolt (kN)", tension_critical_bolt, " Tension capacity = "  "(0.9" "*" + bolt_fu + "*" + net_area_thread + ") / " "(1.25*1000) = "
               + tension_capacity + " <br> [cl. 10.4.5]", " <p align=left style=color:red><b>Fail</b></p> "]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')
    else:

        row = [0, "Tension capacity of critical bolt (kN)", tension_critical_bolt, " Tension capacity = "  "(0.9" "*" + bolt_fu + "*" + net_area_thread + " / " "(1.25*1000) = "
               + tension_capacity + " <br> [cl. 10.4.5]", " <p align=left style=color:green><b>Pass</b></p> "]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

    # Check for shear capacity
    rstr += t('tr')

    required_shear_force = str(float(factored_shear_load) / float(number_of_bolts))
    const = str(round(math.pi / 4 * 0.78, 4))
    n_e = str(1)
    n_n = str(1)

    if required_shear_force > shearcapacity:
        if bearingcapacity == "N/A" :
            row = [0, "Bolt shear capacity (kN)", "Factored shear force / Number of bolts = " + factored_shear_load + " / " + number_of_bolts + " = "
                   + required_shear_force, "<i>V</i><sub>dsf</sub> = (" + slip_factor + "*" + n_e + "*" + k_h + "*" + F_0 +
                ") / 1.25 = " + shearcapacity + "<br> [cl. 10.4.3]", " <p align=left style=color:red><b>Fail</b></p> "]
        else:
            row = [0, "Bolt shear capacity (kN)", "Factored shear force / Number of bolts = " + factored_shear_load + " / " + number_of_bolts + " = "
                   + required_shear_force, "<i>V</i><sub>dsb</sub> = (" + bolt_fu + "*" + n_n + "*" + const + "*" + bolt_dia + "*" + bolt_dia +
            ")/(&#8730;3*1.25*1000) = " + shearcapacity + "<br> [cl. 10.3.3]", " <p align=left style=color:red><b>Fail</b></p> "]
    else:
        if bearingcapacity == "N/A" :
            row = [0, "Bolt shear capacity (kN)", "Factored shear force / Number of bolts = " + factored_shear_load + " / " + number_of_bolts + " = "
                   + required_shear_force, "<i>V</i><sub>dsf</sub> = (" + slip_factor + "*" + n_e + "*" + k_h + "*" + F_0 +
                ") / 1.25 = " + shearcapacity + "<br> [cl. 10.4.3]", " <p align=left style=color:green><b>Pass</b></p> "]
        else:
            row = [0, "Bolt shear capacity (kN)", "Factored shear force / Number of bolts = " + factored_shear_load + " / " + number_of_bolts + " = "
                   + required_shear_force, "<i>V</i><sub>dsb</sub> = (" + bolt_fu + "*" + n_n + "*" + const + "*" + bolt_dia + "*" + bolt_dia +
            ")/(&#8730;3*1.25*1000) = " + shearcapacity + "<br> [cl. 10.3.3]", " <p align=left style=color:green><b>Pass</b></p> "]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Check for bearing capacity
    rstr += t('tr')
    if bearingcapacity == "N/A" :
        row = [0, "Bolt bearing capacity (kN)", "", "N/A", ""]
    else:
        row = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + plate_thk + "*" + beam_fu + ")"

                " / (1.25*1000)  = " + bearingcapacity + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Check for bolt capacity
    rstr += t('tr')
    if bearingcapacity == "N/A":
        # boltCapacity = str(float(shearcapacity))
        row = [0, "Bolt capacity (kN)", shearcapacity, boltcapacity, ""]
    else:
        # boltCapacity = bearingcapacity if bearingcapacity < shearcapacity else shearcapacity
        # boltCapacity = str(min(float(shearCapacity), float(bearingcapacity)))
        row = [0, "Bolt capacity (kN)", " Min (" + shearcapacity + ", " + bearingcapacity + ") = ", boltcapacity, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Check for Combined capacity
    rstr += t('tr')
    if bolt_type == "HSFG":

        if combinedcapacity < str(float(1)):
            row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0", "(<i>V</i><sub>sf</sub>/<i>V</i><sub>df</sub>)^2 + (<i>T</i><sub>f</sub>/<i>T</i><sub>df</sub>)^2 = (" + Vsf + "/" + Vdf + ")^2 + ("
                + Tf + "/" + Tdf + ")^2 = " + combinedcapacity +  " <br> [cl. 10.4.6]", " <p align=left style=color:green><b>Pass</b></p> "]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')
        else:

            row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0",
                   "(<i>V</i><sub>sf</sub>/<i>V</i><sub>df</sub>)^2 + (<i>T</i><sub>f</sub>/<i>T</i><sub>df</sub>)^2 = (" + Vsf + "/" + Vdf + ")^2 + ("
                   + Tf + "/" + Tdf + ")^2 = " + combinedcapacity + " <br> [cl. 10.4.6]", " <p align=left style=color:red><b>Fail</b></p> "]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')
    else:
        if combinedcapacity > float(1):

            row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0", "(<i>V</i><sub>sb</sub>/<i>V</i><sub>db</sub>)^2 + (<i>T</i><sub>b</sub>/<i>T</i><sub>db</sub>)^2 = (" + Vsb + "/" + Vdb + "+"
                   + Tb + "/" + Tdb + ") = " + combinedcapacity + " <br> [cl. 10.3.6]", " <p align=left style=color:red><b>Fail</b></p> "]
            print(type(row))
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')
        else:

            row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0", "(<i>V</i><sub>sb</sub>/<i>V</i><sub>db</sub>)^2 + (<i>T</i><sub>b</sub>/<i>T</i><sub>db</sub>)^2 = (" + Vsb + "/" + Vdb + "+"
                   + Tb + "/" + Tdb + ") = " + combinedcapacity + " <br> [cl. 10.3.6]", " <p align=left style=color:green><b>Pass</b></p> "]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')

    # Number of bolts required
    rstr += t('tr')
    row = [0, "No. of bolts required", " ", number_of_bolts, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Number of Column(s)
    rstr += t('tr')

    row = [0, "No. of column(s)", " ", "2", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Number of bolts per column
    rstr += t('tr')

    row = [0, "No. of row(s)", " ", bolts_per_column, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')


    # TODO: Add pitch checks (Danish)
    # Bolt pitch
    if number_of_bolts == 8:
        if pitch_distance < pitch_mini or pitch_distance > pitch_max:
            row = [0, "Bolt pitch (mm)"," &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                   + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]",pitch_distance, "  <p align=left style=color:red><b>Fail</b></p>"]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')
        else:
            row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                   + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch_distance, "  <p align=left style=color:green><b>Pass</b></p>"]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')
    elif number_of_bolts == 12:
        if pitch_distance_2_3 == pitch_distance_4_5 < pitch_mini or pitch_distance_3_4 < pitch_mini:
            if pitch_distance_2_3 == pitch_distance_4_5 > pitch_mini or pitch_distance_3_4 > pitch_max:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch_distance_2_3 and pitch_distance_3_4, "  <p align=left style=color:red><b>Fail</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
            else:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch_distance_2_3 and pitch_distance_3_4, "  <p align=left style=color:green><b>Pass</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
    elif number_of_bolts == 16:
        if pitch_distance_2_3 == pitch_distance_3_4 == pitch_distance_5_6 == pitch_distance_6_7 < pitch_mini or pitch_distance_4_5 < pitch_mini:
            if pitch_distance_2_3 == pitch_distance_3_4 == pitch_distance_5_6 == pitch_distance_6_7 > pitch_mini or pitch_distance_4_5 > pitch_mini:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch_distance_2_3 and pitch_distance_4_5, "  <p align=left style=color:red><b>Fail</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
            else:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch_distance_2_3 and pitch_distance_4_5,
                       "  <p align=left style=color:green><b>Pass</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
    elif number_of_bolts == 20:
        if pitch_distance_1_2 == pitch_distance_3_4 == pitch_distance_4_5 == pitch_distance_6_7 == pitch_distance_7_8 == pitch_distance_9_10 < pitch_mini or pitch_distance_5_6 < pitch_mini:
            if pitch_distance_1_2 == pitch_distance_3_4 == pitch_distance_4_5 == pitch_distance_6_7 == pitch_distance_7_8 == pitch_distance_9_10 > pitch_mini or pitch_distance_5_6 > pitch_mini:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch_distance_1_2 and pitch_distance_5_6, "  <p align=left style=color:red><b>Fail</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
            else:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch_distance_1_2 and pitch_distance_5_6,
                       "  <p align=left style=color:green><b>Pass</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')

    # Bolt Gauge
    rstr += t('tr')

    if gauge_distance < gauge_mini:
        if gauge_distance > gauge_max:
            row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + gauge_mini + ", &#8804; Min(32*" + end_plate_thickness + ", 300) = " + gauge_max + " <br> [cl. 10.2.2 & cl. 10.2.3]",
               gauge_distance, " <p align=left style=color:red><b>Fail</b></p> "]
        else:
            row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + gauge_mini + ", &#8804; Min(32*" + end_plate_thickness + ", 300) = " + gauge_max + " <br> [cl. 10.2.2 & cl. 10.2.3]",
                   gauge_distance, " <p align=left style=color:green><b>Pass</b></p> "]
    else:
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + gauge_mini + ", &#8804; Min(32*" + end_plate_thickness + ", 300) = " + gauge_max + " <br> [cl. 10.2.2 & cl. 10.2.3]",
               gauge_distance, " <p align=left style=color:green><b>Pass</b></p> "]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # End Distance
    rstr += t('tr')

    if end_distance < end_mini:
        if end_distance > end_max:
            row = [0, "End distance (mm)",
                   " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + end_mini + ", &#8804; 12*" + end_plate_thickness + " = " + end_max + " <br> [cl. 10.2.4]", end_distance,
                    "  <p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "End distance (mm)",
                   " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + end_mini + ", &#8804; 12*" + end_plate_thickness + " = " + end_max + " <br> [cl. 10.2.4]",
                   end_distance,
                   "  <p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "End distance (mm)",
               " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + end_mini + ", &#8804; 12*" + end_plate_thickness + " = " + end_max + " <br> [cl. 10.2.4]",
               end_distance, "  <p align=left style=color:green><b>Pass</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')

    # Edge Distance
    rstr += t('tr')

    if edge_distance < edge_mini:
        if edge_distance > edge_max:
            row = [0, "Edge distance (mm)",
               " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + edge_mini + ", &#8804; 12*" + end_plate_thickness + " = " + edge_max + " <br> [cl. 10.2.4]",
               end_distance,"  <p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Edge distance (mm)"," &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + edge_mini + ", &#8804; 12*" + end_plate_thickness + " = " + edge_max + " <br> [cl. 10.2.4]",
                   end_distance, "  <p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Edge distance (mm)"," &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + edge_mini + ", &#8804; 12*" + end_plate_thickness + " = " + edge_max + " <br> [cl. 10.2.4]",
               end_distance, "  <p align=left style=color:green><b>Pass</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')

    # Plate thickness
    rstr += t('tr')
    if tp_required > end_plate_thickness:
        row = [0, "Plate thickness (mm)",

               "( (4" "*" "1.10" "*" + M_p + "*1000)/(" + end_plate_fy + "*" + b_e + ") ) ^ 0.5 = " + str(round(float(tp_required), 3)) +
               "<br> [Design of Steel Structures - N. Subramanian, 2014]", end_plate_thickness, "  <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Plate thickness (mm)",
               "( (4" "*" "1.10" "*" + M_p + "*1000)/(" + end_plate_fy + "*" + b_e + ") ) ^ 0.5 = " + str(round(float(tp_required), 3)) +
               "<br> [Design of Steel Structures - N. Subramanian, 2014]", end_plate_thickness, "  <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Plate Height
    hp_mini = str(float(beam_d) + float(50) + float(2 * float(pitch_mini)) + float(2 * float(end_mini)))  # for 20 number of bolts
    hp_max = str(float(beam_d) + float(50) + float(2 * float(pitch_mini)) + float(2 * float(end_max)))  # for 20 number of bolts
    hp_minimum = str(float(beam_d) + float(50) + float(2 * float(end_mini)))  # for bolts less than 20
    hp_maximum = str(float(beam_d) + float(50) + float(2 * float(end_max)))  # for bolts less than 20

    if number_of_bolts == 20:
        plate_height_mini = hp_mini
        plate_height_max = hp_max
    else:
        plate_height_mini = hp_minimum
        plate_height_max = hp_maximum

    rstr += t('tr')
    if number_of_bolts == 20:

        if plate_height < plate_height_mini:
            if plate_height > plate_height_max:
                row = [0, "Plate height (mm)", "&#8805; (" + beam_d + "+ 50.0 + (2*" + pitch_mini + ") + (2* " + end_mini+ ") , &#8804; (" + beam_d + "+ 50.0 + (2*" + pitch_mini +
                      ") + (2*" + end_max + ") <br> [based on reasoning (detailing requirements)]", plate_height, " <p align=left style=color:red><b>Fail</b></p>", "300", ""]
        else:
            row = [0, "Plate height (mm)","&#8805; (" + beam_d + "+ 50.0 + (2*" + pitch_mini + ") + (2* " + end_mini + ") , &#8804; (" + beam_d + "+ 50.0 + (2*" + pitch_mini +
                   ") + (2*" + end_max + ") <br> [based on reasoning (detailing requirements)]", plate_height, " <p align=left style=color:green><b>Pass</b></p>","300", ""]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')
    else:
        if plate_height < plate_height_mini:
            if plate_height > plate_height_max:
                row = [0, "Plate height (mm)",
                       "&#8805; (" + str(beam_d) + "+ 50.0 +" " (2*" + str(float(end_mini)) + ")) = " + hp_minimum + ", &#8804; (" + str(
                           beam_d) + "+ 50.0 + (" "2*" + end_max +
                       ")) = " + hp_maximum + " <br> [based on reasoning (detailing requirements)]", plate_height,
                       " <p align=left style=color:red><b>Fail</b></p>", "300", ""]
            else:
                row = [0, "Plate height (mm)",
                       "&#8805; (" + str(beam_d) + "+ 50.0 +" " (2*" + str(float(end_mini)) + ")) = " + hp_minimum + ", &#8804; (" + str(
                           beam_d) + "+ 50.0 + (" "2*" + end_max +
                       ")) = " + hp_maximum + " <br> [based on reasoning (detailing requirements)]", plate_height,
                       " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
        else:
            row = [0, "Plate height (mm)","&#8805; (" + str(beam_d) + "+ 50.0 +" " (2*" + str(float(end_mini)) + ")) = " + hp_minimum + ", &#8804; (" + str(beam_d) + "+ 50.0 + (" "2*" + end_max +
                   ")) = " + hp_maximum + " <br> [based on reasoning (detailing requirements)]", plate_height," <p align=left style=color:green><b>Pass</b></p>", "300", ""]

        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')

    # Plate Width
    g_1 = float(90)  # cross centre gauge distance
    plate_width_mini = max(float((g_1 + (2 * float(edge_mini)))), beam_B)
    plate_width_max = max(float((beam_B + 25)), float(plate_width_mini))

    rstr += t('tr')

    if plate_width < plate_width_mini:
        if plate_width > plate_width_max:
            row = [0, "Plate width (mm)", "&#8805; max ((" + str(g_1) + "+ (2*" + str(float(edge_mini)) + ")), " + str(beam_B) + "), &#8804; max ((" + str(beam_B) + "+ 25), " + str(plate_width_mini) +
                   ") <br> [based on reasoning (detailing requirements)]", plate_width, " <p align=left style=color:red><b>Fail</b></p>", "300", ""]
        else:
            row = [0, "Plate width (mm)","&#8805; max ((" + str(g_1) + "+ (2*" + str(float(edge_mini)) + ")), " + str(beam_B) + "), &#8804; max ((" + str(beam_B) + "+ 25), " + str(
                       plate_width_mini) +") <br> [based on reasoning (detailing requirements)]", plate_width, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    else:
        row = [0, "Plate width (mm)","&#8805; max ((" + str(g_1) + "+ (2*" + str(float(edge_mini)) + ")), " + str(beam_B) + "), &#8804; max ((" + str(beam_B) + "+ 25), " + str(
                   plate_width_mini) + ") <br> [based on reasoning (detailing requirements)]", plate_width, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Plate Moment capacity
    rstr += t('tr')

    if plate_moment_demand > plate_moment_capacity:
        row = [0, "Plate moment capacity (kNm)",

               "Moment demand <i>M</i><sub>d</sub> = ((" + tp_required + "<sup>2</sup>" + "*" + end_plate_fy + "*" + b_e + ")/(4.4*10^2)) * 10^-6 = " + plate_moment_demand,
               "Moment capacity <i>M</i><sub>c</sub> = ((" + end_plate_thickness + "<sup>2</sup>" + "*" + end_plate_fy + "*" + b_e + ")/(4.4*10 ^ 2)) * 10 ^ -6 = " + plate_moment_capacity +
               "<br>[Design of Steel Structures - N. Subramanian, 2014]", "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Plate moment capacity (kNm)",
               "Moment demand <i>M</i><sub>d</sub> = ((" + tp_required + "<sup>2</sup>" + "*" + end_plate_fy + "*" + b_e + ")/(4.4*10^2)) * 10^-6 = " + plate_moment_demand,
               "Moment capacity <i>M</i><sub>c</sub> = ((" + end_plate_thickness + "<sup>2</sup>" + "*" + end_plate_fy + "*" + b_e + ")/(4.4*10 ^ 2)) * 10 ^ -6 = " + plate_moment_capacity +
               "<br>[Design of Steel Structures - N. Subramanian, 2014]", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Weld thickness at flange
    rstr += t('tr')

    flange_weld_req = str(float((resultant * 10 ** 3) / capacity_flange))

    if weld_thickness_flange < flange_weld_req:
        row = [0, "Weld thickness at flange (mm)",
               "&#8805; (" + str(resultant) + "* 10^3" ")/" + str(capacity_flange) + "=" + str(round(float(flange_weld_req), 3)) +
               "<br> [Design of Steel Structures - N. Subramanian, 2014]", weld_thickness_flange,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Weld thickness at flange (mm)",

               "&#8805; (" + str(resultant) + "* 10^3" ")/" + str(capacity_flange) + "=" + str(round(float(flange_weld_req), 3)) +
               "<br> [Design of Steel Structures - N. Subramanian, 2014]", weld_thickness_flange,
               " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Weld thickness at web
    rstr += t('tr')

    web_weld_req = str(int(min(beam_tw, tp_required)))

    if weld_thickness_web < web_weld_req:
        row = [0, "Weld thickness at web (mm)",
               "&#8804; minimum(" + str(beam_tw) + "," + tp_required + ")" "<br> [based on reasoning]", weld_thickness_web,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Weld thickness at web (mm)",
               "&#8804; minimum(" + str(beam_tw) + "," + tp_required + ")" "<br> [based on reasoning]", weld_thickness_web,
               " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Effective length of weld on flange
    length_flange_effective = float(effective_length_flange / 2)
    length_flange = str(length_flange_effective)
    rstr += t('tr')
    row = [0, "Effective weld length on flange (each side) (mm)", "", length_flange, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Effective length of weld on web
    length_web_effective = float(effective_length_web / 2)
    length_web = str(length_web_effective)
    rstr += t('tr')

    row = [0, "Effective weld length on flange (each side) (mm)", "", length_web, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Weld at flange
    rstr += t('tr')
    # TODO Check values of fu and fy
    weld_fu = str(410)
    weld_fy = str(250)

    if float(critical_stress_flange) > float(weld_strength):
        row = [0, "Critical stress in weld at flange (N/mm^2)",
               "&#8804; " + weld_fu + " / (&#8730;3 * 1.25) = " + weld_strength +
               "<br> [cl. 10.5.7]", "(" + force_flange + "* 10^3)/(3 * " + str(effective_length_flange) + ") = " + critical_stress_flange,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Critical stress in weld at flange (N/mm^2)",
               "&#8804; " + weld_fu + " / (&#8730;3 * 1.25) = " + weld_strength +
               "<br> [cl. 10.5.7]", "(" + force_flange + "* 10^3)/(3 * " + str(effective_length_flange) + ") = " + critical_stress_flange,
               " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Weld at web

    rstr += t('tr')
    # f_a_web = float(round((fa_web ** 2), 3))
    # fa_web = str(f_a_web)
    # q_Web = float(round((q_web ** 2), 3))
    # q_web = str(q_Web)

    if float(critical_stress_web) > float(weld_strength):
        row = [0, "Critical stress in weld at web (N/mm ^ 2)",
               "&#8804; " + weld_fu + "/(&#8730;3 * 1.25) = " + weld_strength +
               "<br> [cl. 10.5.7 and cl. 10.5.10]", "&#8730;((" + str(fa_web) + ")^2 + (3 * " + str(q_web) + "^2)) =" + critical_stress_web,
               " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Critical stress in weld at web (N/mm ^ 2)",
               "&#8804; " + weld_fu + "/(&#8730;3 * 1.25) = " + weld_strength +
               "<br> [cl. 10.5.7 and cl. 10.5.10]", "&#8730;((" + str(fa_web) + ")^2 + (3 * " + str(q_web) + "^2)) =" + critical_stress_web,
               " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

    # ######################################### End of checks #########################################
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

    # ################################### Page 6: Views###################################################

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

    row = [0, "Views", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    png = folder + "/images_html/3D_Model.png"
    datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png

    side = folder + "/images_html/extendSide.png"
    dataside = '<object type="image/PNG" data= %s width ="400"></object>' % side

    top = folder + "/images_html/extendTop.png"
    datatop = '<object type="image/PNG" data= %s width ="400"></object>' % top

    front = folder + "/images_html/extendFront.png"
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

    # ###########################################################################################
    # Header of the pdf fetched from dialougebox

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
    #
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
