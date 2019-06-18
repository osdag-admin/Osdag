"""
Created on April, 2019

@author: Yash Lokhande
"""



from __builtin__ import str
import time
import math
import os
import pickle
from Connections.connection_calculations import ConnectionCalculations

######################################################################
# Start of Report
def save_html(outObj, uiObj, dictcolumndata, dictbeamdata, filename, reportsummary, folder):
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
    # beam_fy = str(float(uiObj['Member']['fy (MPa)']))
    # weld_fu_govern = str(outObj['Weld']['WeldFuGovern'])

    column_sec = uiObj['Member']['ColumnSection']
    column_fu = str(float(uiObj['Member']['fu (MPa)']))



    factored_moment = str(float(uiObj['Load']['Moment (kNm)']))
    factored_shear_load = str(float(uiObj['Load']['ShearForce (kN)']))

    factored_axial_load = str(float(uiObj['Load']['AxialForce (kN)']))

    bolt_dia = str(int(uiObj['Bolt']['Diameter (mm)']))
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = str(float(uiObj['Bolt']['Grade']))
    bolt_fu = str((int(float(bolt_grade)) * 100))

    net_area_thread = {12: str(84.3), 16: str(157), 20: str(245), 22: str(303), 24: str(353), 27: str(459), 30: str(561), 36: str(817)}[int(bolt_dia)]

    endplate_type = str(uiObj['Member']['EndPlate_type'])

    weld_method =  str((uiObj['Weld']['Method']))


    # Design Preferences

    bolt_hole_clrnce = str(float(uiObj["bolt"]["bolt_hole_clrnce"]))
    bolt_hole_type = str(uiObj["bolt"]["bolt_hole_type"])
    bolt_grade_fu = str(float(uiObj["bolt"]["bolt_fu"]))
    slip_factor = str(float(uiObj["bolt"]["slip_factor"]))
    bolt_Type = str(uiObj['bolt']['bolt_type'])  # for pre-tensioned/ non- pretensioned bolts

    typeof_weld = str(uiObj["weld"]["typeof_weld"])
    fu_overwrite = str(float(uiObj["weld"]["fu_overwrite"]))

    typeof_edge = str(uiObj["detailing"]["typeof_edge"])
    min_edgend_dist = str(float(uiObj["detailing"]["min_edgend_dist"]))  # factor: 1.7 or 1.5 depending on type of edge, IS 800- Cl 10.2.4.2
    # gap = float(uiObj["detailing"]["gap"])
    corrosive = str(uiObj["detailing"]["is_env_corrosive"])
    design_method = str(uiObj["design"]["design_method"])

    # Bolt
    # print "out", outObj
    number_of_bolts = str(int(outObj['Bolt']['NumberOfBolts']))

    if float(number_of_bolts) <= 20:
        #no_rows = str(int(outObj['Bolt']['NumberOfRows']))
        #bolts_per_column = str(outObj['Bolt']['BoltsPerColumn'])
        cross_centre_gauge = str(outObj['Bolt']['CrossCentreGauge'])
    else:
        #no_rows = str(0)
        #bolts_per_column = str(0)
        cross_centre_gauge = str(outObj['Bolt']['CrossCentreGauge'])

    end_distance = str(int(float(outObj['Bolt']['End'])))
    edge_distance = str(int(float(outObj['Bolt']['Edge'])))
    # gauge_distance = str(int(float(outObj['Bolt']['Gauge'])))
    l_v = str(int(float(outObj['Bolt']['Lv'])))
    pitch_dist = str(int(float(outObj['Bolt']['Pitch'])))
    pitch_dist_min = str(int(float(outObj['Bolt']['PitchMini'])))
    pitch_dist_max = str(int(float(outObj['Bolt']['PitchMax'])))

    slip_capacity = str(float(outObj["Bolt"]["SlipCapacity"]))
    shear_capacity = str(float(outObj["Bolt"]["ShearCapacity"]))
    bearing_capacity = str(float(outObj["Bolt"]["BearingCapacity"]))
    bolt_capacity = str(float(outObj["Bolt"]["BoltCapacity"]))
    bolt_tension_capacity = str(float(outObj["Bolt"]["TensionCapacity"]))
    tension_in_bolt = str(float(outObj["Bolt"]["TensionBolt"]))
    combined_capacity = str(float(outObj["Bolt"]["CombinedCapacity"]))
    moment_tension = str(float(outObj["Bolt"]["TensionMoment"]))
    axial_tension = str(float(outObj["Bolt"]["TensionAxial"]))
    prying_force = str(float(outObj["Bolt"]["TensionPrying"]))

    plate_thk = str(outObj['Plate']['Thickness'])  # Sum of plate thickness experiencing bearing in same direction

    if float(number_of_bolts) <= 20:
        if bolt_type == "Friction Grip Bolt":
            Vsf = str(float(outObj['Bolt']['ShearBolt']))
            Vdf = str(float(outObj['Bolt']['BoltCapacity']))
            Tf = str(float(outObj['Bolt']['TensionBolt']))
            Tdf = str(float(outObj['Bolt']['TensionCapacity']))
        else:
            Vsb = str(float(outObj['Bolt']['ShearBolt']))
            Vdb = str(float(outObj['Bolt']['BoltCapacity']))
            Tb = str(float(outObj['Bolt']['TensionBolt']))
            Tdb = str(float(outObj['Bolt']['TensionCapacity']))

        combinedcapacity = str(float(outObj['Bolt']['CombinedCapacity']))
    else:
        if bolt_type == "Friction Grip Bolt":
            Vsf = str(float(outObj['Bolt']['ShearBolt']))
            Vdf = str(float(outObj['Bolt']['BoltCapacity']))
            Tf = str(float(outObj['Bolt']['TensionBolt']))
            Tdf = str(float(outObj['Bolt']['TensionCapacity']))
        else:
            Vsb = str(float(outObj['Bolt']['ShearBolt']))
            Vdb = str(float(outObj['Bolt']['BoltCapacity']))
            Tb = str(float(outObj['Bolt']['TensionBolt']))
            Tdb = str(float(outObj['Bolt']['TensionCapacity']))

        combinedcapacity = str(0)

    pitch_mini = str(int(float(outObj['Bolt']['PitchMini'])))
    pitch_max = str(outObj['Bolt']['PitchMax'])
    end_mini = str(outObj['Bolt']['EndMini'])
    end_max = str(outObj['Bolt']['EndMax'])
    edge_mini = str(end_mini)
    edge_max = str(end_max)
    dia_hole = str(int(outObj['Bolt']['DiaHole']))

# Stiffener and Continuity plate


    cont_plate_tens_length = str(float(outObj['ContPlateTens']['Length']))
    cont_plate_tens_width = str(float(outObj['ContPlateTens']['Width']))
    cont_plate_tens_thk = str(float(outObj['ContPlateTens']['Thickness']))
    cont_plate_tens_thk_min = str(float(outObj['ContPlateTens']['ThicknessMin']))
    cont_plate_tens_weld = str(float(outObj['ContPlateTens']['Weld']))

    cont_plate_comp_length = str(float(outObj['ContPlateComp']['Length']))
    cont_plate_comp_width = str(float(outObj['ContPlateComp']['Width']))
    cont_plate_comp_thk = str(float(outObj['ContPlateComp']['Thickness']))
    cont_plate_comp_thk_min = str(float(outObj['ContPlateComp']['ThicknessMin']))
    cont_plate_comp_weld = str(float(outObj['ContPlateComp']['Weld']))

    st_length = str(float(outObj['Stiffener']['Length']))
    st_height = str(float(outObj['Stiffener']['Height']))
    st_thk = str(float(outObj['Stiffener']['Thickness']))
    st_notch_bottom = str(float(outObj['Stiffener']['NotchBottom']))
    st_notch_top = str(float(outObj['Stiffener']['NotchTop']))
    st_weld = str(float(outObj['Stiffener']['Weld']))

  # Plate
    plate_tk_min = str(float(outObj['Plate']['ThickRequired']))
    end_plate_thickness = str(float(outObj['Plate']['Thickness']))
    # M_p = str(float(outObj['Plate']['Mp']))
    plate_height = str(float(outObj['Plate']['Height']))
    plate_width = str(float(outObj['Plate']['Width']))
    toe_of_weld_moment = str(float(outObj['Plate']['Moment']))
    beam_B = str(float(outObj['Plate']['be']))
    end_plate_fy = str(float(outObj['Plate']['fy']))
    bf = str(float(outObj['Plate']['WidthMin']))
    # plate_moment_demand = str(float(outObj['Plate']['MomentDemand']))
    # plate_moment_capacity = str(float(outObj['Plate']['MomentCapacity']))

    # Weld
    if weld_method == "Fillet Weld":

        if float(number_of_bolts) <= 20:

            flange_weld_size_min = str(float(outObj["Weld"]["FlangeSizeMin"]))
            flange_weld_size_max = str(float(outObj["Weld"]["FlangeSizeMax"]))
            flange_weld_throat_size = str(float(outObj["Weld"]["FlangeThroat"]))
            flange_weld_size_provd = str(float(uiObj["Weld"]["Flange (mm)"]))

            flange_weld_stress = str(float(outObj["Weld"]["FlangeStress"]))
            flange_weld_strength = str(float(outObj["Weld"]["FlangeStrength"]))

            flange_weld_effective_length_top = str(float(outObj["Weld"]["FlangeLengthTop"]))
            flange_weld_effective_length_bottom = str(float(outObj["Weld"]["FlangeLengthBottom"]))


            web_weld_stress = str(float(outObj["Weld"]["WebStress"]))
            web_weld_strength = str(float(outObj["Weld"]["WebStrength"]))

            web_weld_size_min = str(float(outObj["Weld"]["WebSizeMin"]))
            web_weld_size_max = str(float(outObj["Weld"]["WebSizeMax"]))
            web_weld_throat_size = str(float(outObj["Weld"]["WebThroat"]))
            web_weld_size_provd = str(float(uiObj["Weld"]["Web (mm)"]))

            web_weld_effective_length = str(float(outObj["Weld"]["WebLength"]))



    else:
        weld_size = str(float(outObj["Weld"]["Size"]))
        groove_weld_size_flange = str(float(outObj["Weld"]["FlangeSize"]))
        groove_weld_size_web = str(float(outObj["Weld"]["WebSize"]))


# Calling pitch distance values from Output dict of calc file
    if endplate_type == 'Flush end plate':
        if float(number_of_bolts) == float(4):
            pitch12 = str(float(outObj['Bolt']['Pitch12']))

        elif float(number_of_bolts) == float(8):
            pitch12 = str(float(outObj['Bolt']['Pitch12']))
            pitch23 = str(float(outObj['Bolt']['Pitch23']))
            pitch34 = str(float(outObj['Bolt']['Pitch34']))

        elif float(number_of_bolts) == float(12):
            pitch12 = str(float(outObj['Bolt']['Pitch12']))
            pitch23 = str(float(outObj['Bolt']['Pitch23']))
            pitch34 = str(float(outObj['Bolt']['Pitch34']))
            pitch45 = str(float(outObj['Bolt']['Pitch45']))
            pitch56 = str(float(outObj['Bolt']['Pitch56']))

    elif endplate_type == 'Extended one way':

        if float(number_of_bolts) == float(6):
            pitch12 = str(float(outObj['Bolt']['Pitch12']))
            pitch23 = str(float(outObj['Bolt']['Pitch23']))

        elif float(number_of_bolts) == float(8):
            pitch12 = str(float(outObj['Bolt']['Pitch12']))
            pitch23 = str(float(outObj['Bolt']['Pitch23']))
            pitch34 = str(float(outObj['Bolt']['Pitch34']))

        elif float(number_of_bolts) == float(10):
            pitch12 = str(float(outObj['Bolt']['Pitch12']))
            pitch23 = str(float(outObj['Bolt']['Pitch23']))
            pitch34 = str(float(outObj['Bolt']['Pitch34']))
            pitch45 = str(float(outObj['Bolt']['Pitch45']))

        elif float(number_of_bolts) == float(12):
            pitch12 = str(float(outObj['Bolt']['Pitch12']))
            pitch23 = str(float(outObj['Bolt']['Pitch23']))
            pitch34 = str(float(outObj['Bolt']['Pitch34']))
            pitch45 = str(float(outObj['Bolt']['Pitch45']))
            pitch56 = str(float(outObj['Bolt']['Pitch56']))

    else:  # endplate_type == 'both_way':
        if float(number_of_bolts) == float(8):
            pitch = str(float(outObj['Bolt']['Pitch']))
        elif float(number_of_bolts) == float(12):
            pitch23 = str(float(outObj['Bolt']['Pitch23']))
            pitch34 = str(float(outObj['Bolt']['Pitch34']))
            pitch45 = str(float(outObj['Bolt']['Pitch45']))
        elif float(number_of_bolts) == float(16):
            pitch23 = str(float(outObj['Bolt']['Pitch23']))
            pitch34 = str(float(outObj['Bolt']['Pitch34']))
            pitch45 = str(float(outObj['Bolt']['Pitch45']))
            pitch56 = str(float(outObj['Bolt']['Pitch56']))
            pitch67 = str(float(outObj['Bolt']['Pitch67']))
        elif float(number_of_bolts) == float(20):
            pitch12 = str(float(outObj['Bolt']['Pitch12']))
            pitch34 = str(float(outObj['Bolt']['Pitch34']))
            pitch45 = str(float(outObj['Bolt']['Pitch45']))
            pitch56 = str(float(outObj['Bolt']['Pitch56']))
            pitch67 = str(float(outObj['Bolt']['Pitch67']))
            pitch78 = str(float(outObj['Bolt']['Pitch78']))
            pitch910 = str(float(outObj['Bolt']['Pitch910']))

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
        row = [1, "Beam to Column End Plate Moment Connection", "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [1, "Beam to Column End Plate Moment Connection", "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('tr')
    rstr += t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1"') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [0, "Extended End Plate", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')

    row = [0, "Connection Properties", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [0, "Connection ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Connection Type", "Moment Connection"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # TODO: should we add Single Extended End Plate
    # row = [1, "Connection Title", " Single Fin Plate"]
    row = [1, "Connection Title", "Extended End Plate"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    if endplate_type == "Flush end plate":
        row = [1, "End plate type", "Flush end plate"]
    elif endplate_type == "Extended one way":
        row = [1,"End plate type", "Extended one way"]
    else:
        row = [1,"End plate type", "Extended both way"]
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

    row = [1, "Beam to end plate Connection", "Welded"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    if connectivity == "Column flange-Beam web":
        row = [1, "Column flange to end plate Connection", "Bolted"]
    else:
        row = [1, "Column web to end plate Connection", "Bolted"]

    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [0, "Loading Details ", " "]
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

    row = [2, "Grade of Steel", "Fe " + beam_fu]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Column Section", column_sec]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Grade of Steel", "Fe " + column_fu]
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

    row = [2, "Thickness (t) (mm)", end_plate_thickness]
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

    row = [2, "Clearance holes for fasteners", bolt_hole_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Weld ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [2, "Type", uiObj["Weld"]["Method"]]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Weld at Flange (mm)", uiObj['Weld']['Flange (mm)']]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Weld at Web (mm)", uiObj['Weld']['Web (mm)']]
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

    row = [2, "Property Class", bolt_grade]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Diameter (d) (mm)", bolt_dia]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    bolt_hole_dia = float(bolt_dia) + float(bolt_hole_clrnce)
    bolt_hole_dia_str = str(float(bolt_hole_dia))
    row = [2, "Hole diameter (<i>d</i><sub>o</sub>) (mm)", bolt_hole_dia_str]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Number of Bolts (n)", number_of_bolts]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Columns (Vertical Lines)", "2"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    #
    # row = [2, "Bolts Per Column", no_rows]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')

    row = [2, "End Distance (e)(mm)", end_distance]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Edge Distance (<i>e</i><sup>'</sup>) (mm)", edge_distance]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [2, "Cross-centre gauge (<i>g</i><sup>'</sup>) (mm)", cross_centre_gauge]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')


    row = [2, "Pitch Distance (p) (mm)",""]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    if endplate_type == "Flush end plate":
        if float(number_of_bolts) == (4):
            row = [3, "Pitch-1,2", pitch12]
        elif float(number_of_bolts) == float(8):
            row = [3, "Pitch-1,2", pitch12]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-2,3", pitch23]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-3,4", pitch34]

        elif float(number_of_bolts) == float(12):
            row = [3, "Pitch-1,2", pitch12]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-2,3", pitch23]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-3,4", pitch34]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-4,5", pitch45]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-5,6", pitch56]

    elif endplate_type == "Extended one way":
        if float(number_of_bolts) == float(6):
            row = [3, "Pitch-1,2", pitch12]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-2,3", pitch23]

        elif float(number_of_bolts) == float(8):
            row = [3, "Pitch-1,2", pitch12]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-2,3", pitch23]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-3,4", pitch34]

        elif float(number_of_bolts) == float(10):
            row = [3, "Pitch-1,2", pitch12]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-2,3", pitch23]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-3,4", pitch34]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-4,5", pitch45]

        elif float(number_of_bolts) == float(12):
            row = [3, "Pitch-1,2", pitch12]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-2,3", pitch23]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-3,4", pitch34]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-4,5", pitch45]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-5,6", pitch56]

    else:
        if float(number_of_bolts) == float(8):
            row = [3, "Pitch", pitch]

        elif float(number_of_bolts) == float(12):
            row = [3, "Pitch-2,3", pitch23]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-3,4", pitch34]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-4,5", pitch45]

        elif float(number_of_bolts) == float(16):
            row = [3, "Pitch-2,3", pitch23]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-3,4", pitch34]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-4,5", pitch45]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-5,6", pitch56]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-6,7", pitch67]

        elif float(number_of_bolts) == float(20):
            row = [3, "Pitch-1,2", pitch12]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-3,4", pitch34]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-4,5", pitch45]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-5,6", pitch56]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-6,7", pitch67]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-7,8", pitch78]
            rstr += t('tr')
            rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2 "') + row[2] + t('/td')
            rstr += t('/tr')

            row = [3, "Pitch-9,10", pitch910]

    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')


    # row = [0, "Assembly ", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    #
    # if connectivity == "Column flange-Beam web":
    #     row = [1, "Beam-Column flange Clearance (mm)", plate_thk]
    # else:
    #     row = [1, "Beam-Column web Clearance (mm)", plate_thk]
    #
    # rstr += t('tr')
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    #
    # row = [1,"Note :- Here clearance is the thickness of the plate which lies between beam and column. "," "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # page break
    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')
    rstr += t('/h1')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Header of the pdf fetched from dialogbox

    rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100%')
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

    row = [1, "Ultimate Strength (<i>f</i><sub>u</sub>) (MPa)", bolt_grade_fu]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    if bolt_type == "Friction Grip Bolt":
        row = [1, "Slip factor", slip_factor]
    else:
        row = [1, "Slip factor", "N/A"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    if bolt_Type == "Pre-tensioned":
        row = [1, "Beta (&#946;)(pre-tensioned bolt)", str(1)]
    else:
        row = [1, "Beta (&#946;)(non pre-tensioned)", str(2)]
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

    # row = [1, "Material Grade (MPa) (overwrite)", fu_overwrite]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + row[2] + t('/td')
    # rstr += t('/tr')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Detailing &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    row = [0, "Detailing ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    if typeof_edge == "a - Sheared or hand flame cut":
        row = [1, "Type of Edges", "Sheared or hand flame cut"]
    else:
        row = [1, "Type of Edges", "Rolled, machine-flame cut, sawn and planed"]

    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Minimum Edge-End Distance", min_edgend_dist + " times the hole diameter"]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

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

    rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100%')
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

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
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

    # # Check for tension in critical bolt
    # if float(number_of_bolts) <= float(20):
    #     row = [0, "Tension in critical bolt (kN)", " Tension in bolt due to external factored moment + Prying force = " + tension_critical + "+" + prying_force + " = " + str(float(tension_critical) + float(prying_force)) + " <br> [cl. 10.4.7] ", " ", ""]
    # else:
    #     row = [0, "Tension in critical bolt (kN)",
    #            " Tension in bolt due to external factored moment + Prying force = Cannot compute" " <br> [cl. 10.4.7] ", " ", ""]
    #
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Bolt Checks", " "]
    rstr += t('td colspan="4" class="detail" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')



# Check for shear capacity
    rstr += t('tr')

    required_shear_force = str(float(factored_shear_load) / float(number_of_bolts))
    const = str(round(math.pi / 4 * 0.78, 4))
    n_e = str(1)
    n_n = str(1)

    if bolt_type == "Bearing Bolt":
        if float(required_shear_force) > float(shear_capacity):
            row = [0, "Bolt shear capacity (kN)",
                   "Factored shear force / Number of bolts = " + factored_shear_load + " / " + number_of_bolts + " = "
                   + str(round(float(required_shear_force), 3)),
                   "<i>V</i><sub>dsb</sub> = (" + bolt_fu + "*" + n_n + "*" + const + "*" + bolt_dia + "*" + bolt_dia +
                   ")/(&#8730;3*1.25) = " + shear_capacity + "<br> [cl. 10.3.3]",
                   " <p align=left style=color:red><b>Fail</b></p> "]
        else:
            row = [0, "Bolt shear capacity (kN)", "Factored shear force / Number of bolts = " + factored_shear_load + " / " + number_of_bolts + " = "
                   + str(round(float(required_shear_force), 3)), "<i>V</i><sub>dsb</sub> = (" + bolt_fu + "*" + n_n + "*" + const + "*" + bolt_dia + "*" + bolt_dia +
            ")/(&#8730;3*1.25) = " + shear_capacity + "<br> [cl. 10.3.3]", " <p align=left style=color:green><b>Pass</b></p> "]
    else:
        if float(required_shear_force) > float(slip_capacity):
            row = [0, "Bolt slip resistance (kN)", "Factored shear force / Number of bolts = " + factored_shear_load + " / " + number_of_bolts + " = "
                   + str(round(float(required_shear_force), 3)), "<i>V</i><sub>dsf</sub> = (" + slip_factor + "*" + n_e + "*" + k_h + "*" + F_0 +
                ") / 1.25 = " + slip_capacity + "<br> [cl. 10.4.3]", " <p align=left style=color:red><b>Fail</b></p> "]
        else:
            row = [0, "Bolt slip resistance (kN)",
                   "Factored shear force / Number of bolts = " + factored_shear_load + " / " + number_of_bolts + " = "
                   + str(round(float(required_shear_force), 3)),
                   "<i>V</i><sub>dsf</sub> = (" + slip_factor + "*" + n_e + "*" + k_h + "*" + F_0 +
                   ") / 1.25 = " + slip_capacity + "<br> [cl. 10.4.3]",
                   " <p align=left style=color:green><b>Pass</b></p> "]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Check for bearing capacity
    rstr += t('tr')
    if bolt_type == "Friction Grip Bolt" :
        row = [0, "Bolt bearing capacity (kN)", "N/A", "N/A", ""]
    else:
        row = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5 * <i>k</i><sub>b</sub> * d * t * <i>f</i><sub>u</sub>  = " + bearing_capacity + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Check for bolt capacity
    rstr += t('tr')
    if bolt_type == "Bearing Bolt":
        row = [0, "Bolt capacity (kN)","min(Shear Capacity, Bearing Capacity) =" + " min (" + shear_capacity + ", " + bearing_capacity + ") ", bolt_capacity, ""]
    else:
        row = [0, "Bolt capacity (kN)","", "Bolt slip resistance ="+bolt_capacity, ""]


    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Check for Tension capacity of bolt
    # TODO: Check for bearing bolt type (Danish)
    rstr += t('tr')

    if float(number_of_bolts) <= float(20):

        if float(tension_in_bolt) > float(bolt_tension_capacity):
            row = [0, "Tension capacity of bolt (kN)", "&#8805; Tension in bolt due to external moment + external axial load + prying force ="+ str(float(moment_tension))+"+" + str(float(axial_tension))+"+" + str(float(prying_force)) + "=" +  str(float(tension_in_bolt)),
                   " Tension capacity = "  "(0.9" "*" + bolt_fu + "*" + net_area_thread + ") / (1.25*1000) = "
                   + bolt_tension_capacity + " <br> [cl. 10.4.5]", " <p align=left style=color:red><b>Fail</b></p> "]
        else:

            row = [0, "Tension capacity of bolt (kN)", "&#8805; Tension in bolt due to external moment + external axial load + prying force ="+ str(float(moment_tension))+"+" + str(float(axial_tension))+"+" + str(float(prying_force)) + "=" + str(float(tension_in_bolt)),
                   " Tension capacity = "  "(0.9" "*" + bolt_fu + "*" + net_area_thread + ") / " "(1.25*1000) = "
                   + bolt_tension_capacity + " <br> [cl. 10.4.5]", " <p align=left style=color:green><b>Pass</b></p> "]
    else:
        row = [0, "Tension capacity of critical bolt (kN)", "Cannot compute",
               " Tension capacity = "  "(0.9" "*" + bolt_fu + "*" + net_area_thread + ") / (1.25*1000) = "
               + bolt_tension_capacity + " <br> [cl. 10.4.5]", " <p align=left style=color:red><b>Fail</b></p> "]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Check for Combined capacity
    rstr += t('tr')
    if float(number_of_bolts) <= float(20):
        if bolt_type == "Friction Grip Bolt":
            if float(combined_capacity) > float(1):
                row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0", "(<i>V</i><sub>sf</sub>/<i>V</i><sub>df</sub>)^2 + (<i>T</i><sub>f</sub>/<i>T</i><sub>df</sub>)^2 = (" + Vsf + "/" + Vdf + ")^2 + ("
                    + Tf + "/" + Tdf + ")^2 = " + combined_capacity + " <br> [cl. 10.4.6]", " <p align=left style=color:red><b>Fail</b></p> "]
            else:

                row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0",
                       "(<i>V</i><sub>sf</sub>/<i>V</i><sub>df</sub>)^2 + (<i>T</i><sub>f</sub>/<i>T</i><sub>df</sub>)^2 = (" + Vsf + "/" + Vdf + ")^2 + ("
                       + Tf + "/" + Tdf + ")^2 = " + combined_capacity + " <br> [cl. 10.4.6]", " <p align=left style=color:green><b>Pass</b></p> "]
        else:
            if float(combined_capacity) > float(1):
                row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0", "(<i>V</i><sub>sb</sub>/<i>V</i><sub>db</sub>)^2 + (<i>T</i><sub>b</sub>/<i>T</i><sub>db</sub>)^2 = (" + Vsb + "/" + Vdb + ")^2 + ("
                       + Tb + "/" + Tdb + ")^2 = " + combined_capacity + " <br> [cl. 10.3.6]", " <p align=left style=color:red><b>Fail</b></p> "]
                # print(type(row))

            else:
                row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0", "(<i>V</i><sub>sb</sub>/<i>V</i><sub>db</sub>)^2 + (<i>T</i><sub>b</sub>/<i>T</i><sub>db</sub>)^2 = (" + Vsb + "/" + Vdb + ")^2 + ("
                       + Tb + "/" + Tdb + ")^2 = " + combined_capacity + " <br> [cl. 10.3.6]", " <p align=left style=color:green><b>Pass</b></p> "]
    else:
        row = [0, "Combined shear and tension capacity of bolt", "&#8804; 1.0",
               "(<i>V</i><sub>sb</sub>/<i>V</i><sub>db</sub>)^2 + (<i>T</i><sub>b</sub>/<i>T</i><sub>db</sub>)^2 = Cannot compute" " <br> [cl. 10.3.6]", " <p align=left style=color:red><b>Fail</b></p> "]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # Number of bolts required
    rstr += t('tr')
    row = [0, "No. of bolts", "&#8805; 4 , &#8804; 12", str(float(number_of_bolts)), ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # # Number of Column(s)
    # rstr += t('tr')
    #
    # row = [0, "No. of column(s)", " ", "2", ""]
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')
    #
    # # Number of bolts per column
    # rstr += t('tr')
    # if float(number_of_bolts) <= float(20):
    #     row = [0, "No. of row(s)", " ", no_rows, ""]
    # else:
    #     row = [0, "No. of row(s)", " ", " Cannot compute", ""]
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')


    # TODO: Add pitch checks (Danish)
    # Bolt pitch
    if number_of_bolts == 8:
        if float(pitch) < float(pitch_mini) or float(pitch) > float(pitch_max):
            row = [0, "Bolt pitch (mm)"," &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                   + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]",pitch, "  <p align=left style=color:red><b>Fail</b></p>"]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')
        else:
            row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                   + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch, "  <p align=left style=color:green><b>Pass</b></p>"]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')
    elif number_of_bolts == 12:
        if float(pitch23) == float(pitch45) < float(pitch_mini) or float(pitch34) < float(pitch_mini):
            if float(pitch23) == float(pitch45) > float(pitch_mini) or float(pitch34) > float(pitch_max):
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch23 and pitch34, "  <p align=left style=color:red><b>Fail</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
            else:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch23 and pitch34, "  <p align=left style=color:green><b>Pass</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
    elif number_of_bolts == 16:
        if float(pitch23) == float(pitch34) == float(pitch56) == float(pitch67) < float(pitch_mini) or float(pitch45) < float(pitch_mini):
            if float(pitch23) == float(pitch34) == float(pitch56) == float(pitch67) > float(pitch_mini) or float(pitch45) > float(pitch_mini):
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch23 and pitch45, "  <p align=left style=color:red><b>Fail</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
            else:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch23 and pitch45,
                       "  <p align=left style=color:green><b>Pass</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
    elif number_of_bolts == 20:
        if float(pitch12) == float(pitch34) == float(pitch45) == float(pitch67) == float(pitch78) == float(pitch910) < float(pitch_mini) or float(pitch56) < float(pitch_mini):
            if float(pitch12) == float(pitch34) == float(pitch45) == float(pitch67) == float(pitch78) == float(pitch910) > float(pitch_mini) or float(pitch56) > float(pitch_mini):
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch12 and pitch56, "  <p align=left style=color:red><b>Fail</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')
            else:
                row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + pitch_mini + ",  &#8804; Min(32*" + end_plate_thickness + ", 300) = "
                       + pitch_max + "<br> [cl. 10.2.2 & cl. 10.2.3]", pitch12 and pitch56,
                       "  <p align=left style=color:green><b>Pass</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')

    # Pitch Distance
    rstr += t('tr')

    if float(pitch_dist) < float(pitch_dist_min) or float(pitch_dist) > float(pitch_dist_max):
        row = [0, "Pitch distance (mm)"," &#8805; 2.5 * d  = " + pitch_dist_min + ", &#8804; min(32 * t, 300) = " + pitch_dist_max + " <br> [cl. 10.2.2 & cl. 10.2.3]",
               pitch_dist, " <p align=left style=color:red><b>Fail</b></p> "]
    else:
        row = [0, "Pitch distance (mm)"," &#8805; 2.5 * d  = " + pitch_dist_min + ", &#8804; min(32 * t, 300) = " + pitch_dist_max + " <br> [cl. 10.2.2 & cl. 10.2.3]",
               pitch_dist, " <p align=left style=color:green><b>Pass</b></p> "]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # if float(gauge_distance) > float(gauge_max):
    #     row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + gauge_mini + ", &#8804; min(32*" + end_plate_thickness + ", 300) = " + gauge_max + " <br> [cl. 10.2.2 & cl. 10.2.3]",
    #        gauge_distance, " <p align=left style=color:red><b>Fail</b></p> "]
    # else:
    #     row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + gauge_mini + ", &#8804; min(32*" + end_plate_thickness + ", 300) = " + gauge_max + " <br> [cl. 10.2.2 & cl. 10.2.3]",
    #            gauge_distance, " <p align=left style=color:green><b>Pass</b></p> "]
	#
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')

    # End Distance
    rstr += t('tr')

    end_mini_actual = str(float(min_edgend_dist) * float(dia_hole))

    if typeof_edge == "a - Sheared or hand flame cut":

        if float(end_distance) < float(end_mini) or float(end_distance) > float(end_max):
            row = [0, "End distance (mm)"," &#8805; 1.7 <i>d</i><sub>o</sub>" + " = " + end_mini_actual + ", &#8804; 12*t*&#949;" + " = " + end_max + " <br> [cl. 10.2.4]",
                   end_distance,"  <p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "End distance (mm)"," &#8805; 1.7 <i>d</i><sub>o</sub>" + " = " + end_mini_actual + ", &#8804; 12*t*&#949;" + " = " + end_max + " <br> [cl. 10.2.4]",
                   end_distance,"  <p align=left style=color:green><b>Pass</b></p>"]

    else:
        if float(end_distance) < float(end_mini) or float(end_distance) > float(end_max):
            row = [0, "End distance (mm)",
                   " &#8805; 1.5 <i>d</i><sub>o</sub>" + " = " + end_mini_actual + ", &#8804; 12*t*&#949;" + " = " + end_max + " <br> [cl. 10.2.4]",
                   end_distance, "  <p align=left style=color:red><b>Fail</b></p>"]
        else:

            row = [0, "End distance (mm)",
                   " &#8805; 1.5 <i>d</i><sub>o</sub>" + " = " + end_mini_actual + ", &#8804; 12*t*&#949;" + " = " + end_max + " <br> [cl. 10.2.4]",
                   end_distance, "  <p align=left style=color:green><b>Pass</b></p>"]

# " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + end_mini_actual + ", &#8804; 12*" + end_plate_thickness + " = " + end_max + " <br> [cl. 10.2.4]"

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')

    # if float(end_distance) > float(end_max):
    #     row = [0, "End distance (mm)",
    #            " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + end_mini_actual + ", &#8804; 12*" + end_plate_thickness + " = " + end_max + " <br> [cl. 10.2.4]", end_distance,
    #             "  <p align=left style=color:red><b>Fail</b></p>"]
    # else:
    #     row = [0, "End distance (mm)",
    #            " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + end_mini_actual + ", &#8804; 12*" + end_plate_thickness + " = " + end_max + " <br> [cl. 10.2.4]",
    #            end_distance, "  <p align=left style=color:green><b>Pass</b></p>"]
	#
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')
    # rstr += t('tr')

    # Edge Distance
    rstr += t('tr')

    edge_mini_actual = end_mini_actual
    if typeof_edge == "a - Sheared or hand flame cut":
        if float(edge_distance) < float(edge_mini) or float(edge_distance) > float(edge_max):
            row = [0, "Edge distance (mm)"," &#8805; 1.7 <i>d</i><sub>o</sub>" + " = " + edge_mini_actual + ", &#8804; 12*t*&#949;" + " = " + edge_max + " <br> [cl. 10.2.4]",
                   end_distance, "  <p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Edge distance (mm)"," &#8805; 1.7 <i>d</i><sub>o</sub>" + " = " + edge_mini_actual + ", &#8804; 12*t*&#949;" + " = " + edge_max + " <br> [cl. 10.2.4]",
                   end_distance, "  <p align=left style=color:green><b>Pass</b></p>"]
    else:
        if float(edge_distance) < float(edge_mini) or float(edge_distance) > float(edge_max):
            row = [0, "Edge distance (mm)"," &#8805; 1.5 <i>d</i><sub>o</sub>" + " = " + edge_mini_actual + ", &#8804; 12*t*&#949;" + " = " + edge_max + " <br> [cl. 10.2.4]",end_distance, "<p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Edge distance (mm)"," &#8805; 1.5 <i>d</i><sub>o</sub>" + " = " + edge_mini_actual + ", &#8804; 12*t*&#949;" + " = " + edge_max + " <br> [cl. 10.2.4]",end_distance, "  <p align=left style=color:green><b>Pass</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')

    rstr += t('tr')
    if float(number_of_bolts) <= float(20):

        if endplate_type == "Flush end plate":
            if float(l_v) < float(33) or float(l_v) > float(47):
                row = [0, "Distance to the centre line of bolt from face of beam flange (mm)", "33mm &#8804; <i>l</i><sub>v</sub> &#8804; 47mm",l_v, "<p align=left style=color:red><b>Fail</b></p>"]
            else:
                row = [0, "Distance to the centre line of bolt from face of beam flange (mm)", "33mm &#8804; <i>l</i><sub>v</sub> &#8804; 47mm",l_v, "<p align=left style=color:green><b>Pass</b></p>"]

        elif endplate_type == "Extended one way":
            if float(l_v) < float(25) or float(l_v) > float(63.5):
                row = [0, "Distance to the centre line of bolt from face of beam flange (mm)", "25mm &#8804; <i>l</i><sub>v</sub> &#8804; 63.5mm",l_v, "<p align=left style=color:red><b>Fail</b></p>"]
            else:
                row = [0, "Distance to the centre line of bolt from face of beam flange (mm)", "25mm &#8804; <i>l</i><sub>v</sub> &#8804; 63.5mm",l_v, "<p align=left style=color:green><b>Pass</b></p>"]
        else:
            if float(l_v) < float(50) or float(l_v) > float(62.5):
                row = [0, "Distance to the centre line of bolt from face of beam flange (mm)", "50mm &#8804; <i>l</i><sub>v</sub> &#8804; 62.5mm",l_v, "<p align=left style=color:red><b>Fail</b></p>"]
            else:
                row = [0, "Distance to the centre line of bolt from face of beam flange (mm)", "50mm &#8804; <i>l</i><sub>v</sub> &#8804; 62.5mm",l_v, "<p align=left style=color:green><b>Pass</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')

    rstr += t('tr')
    row = [0, "Plate Checks", " "]
    rstr += t('td colspan="4" class="detail" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # Plate thickness

    rstr += t('tr')
    if float(number_of_bolts) <= (20):
        if float(plate_tk_min) > float(end_plate_thickness):
            row = [0, "Plate thickness (mm)", ("&#8805; &#8730; (M *" + "(1.1/fy) *" + "(4/<i>b</i><sub>e</sub>)) = &#8805; &#8730; ("+moment_tension+"*"+"(1.1/"+end_plate_fy+") * (4/"+beam_B+")) ="+plate_tk_min), end_plate_thickness, "  <p align=left style=color:red><b>Fail</b></p>"]
        else:
            row = [0, "Plate thickness (mm)", ("&#8805; &#8730; (M *" + "(1.1/fy) *" + "(4/<i>b</i><sub>e</sub>)) = &#8805; &#8730; ("+moment_tension+"*"+"(1.1/"+end_plate_fy+") * (4/"+beam_B+")) ="+plate_tk_min), end_plate_thickness, "  <p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Plate thickness (mm)", " Cannot compute ", end_plate_thickness, "  <p align=left style=color:red><b>Fail</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # "( (4" "*" "1.10" "*" + M_p + "*1000)/(" + end_plate_fy + "*" + b_e + ") ) ^ 0.5 = " + str(round(float(plate_tk_min), 3)) +
    #                    "<br> [Design of Steel Structures - N. Subramanian, 2014]"

    # Plate Height

    # if number_of_bolts == 20:
    #     plate_height_mini = str(float(beam_d) + float(50) + float(2 * float(pitch_mini)) + float(2 * float(end_mini)))  # for 20 number of bolts
    #     plate_height_max = str(float(beam_d) + float(50) + float(2 * float(pitch_mini)) + float(2 * float(end_max)))  # for 20 number of bolts
    # else:
    #     plate_height_mini = str(float(beam_d) + float(50) + float(2 * float(end_mini)))  # for bolts less than 20
    #     plate_height_max = str(float(beam_d) + float(50) + float(2 * float(end_max)))  # for bolts less than 20

    rstr += t('tr')

    if float(number_of_bolts) <= float(20):
        row = [0, "Plate height (mm)", "", plate_height, ""]

    else:
        row = [0, "Plate height (mm)", " Cannot compute ", " Cannot compute", " <p align=left style=color:red><b>Fail</b></p>", "300",""]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

# "&#8805; (" + str(beam_d) + "+ 50.0 +" " (2*" + str(float(end_mini)) + ")) = " + plate_height_mini + ", &#8804; (" + str(beam_d) + "+ 50.0 + (" "2*" + end_max +
    #                        ")) = " + plate_height_max + " <br> [based on detailing requirements]"


    # Plate Width
    rstr += t('tr')

    if float(number_of_bolts) <= 20:
        #g_1 = float(90)  # cross centre gauge distance
        # plate_width_mini = beam_B        # max(float((g_1 + (2 * float(edge_mini)))), beam_B)
        # plate_width_max = beam_B+25    # max(float((beam_B + 25)), float(plate_width_mini))

        if float(plate_width) < float(bf):
            row = [0, "Plate width (mm)","&#8805; width of beam flange" + " , "+"&#8805;" + str(float(bf)), plate_width, " <p align=left style=color:red><b>Fail</b></p>", "300", ""]
        else:
            row = [0, "Plate width (mm)","&#8805; width of beam flange" + " , "+"&#8805;" + str(float(bf)), plate_width, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    else:
        row = [0, "Plate width (mm)", " Cannot compute ", " Cannot compute ", " <p align=left style=color:red><b>Fail</b></p>", "300", ""]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

# "&#8805; max (" + str(g_1) + "+ (2*" + str(float(edge_mini)) + ")), " + str(beam_B) + "), &#8804; max ((" + str(beam_B) + "+ 25), " + str(plate_width_mini) +
    #                        ") <br> [based on detailing requirements]"

# "&#62; <i>b</i><sub>f</sub ," + "&#8805; <i>b</i><sub>f</sub> + 25

    # # Plate Moment capacity
    # rstr += t('tr')
    #
    # if float(number_of_bolts) <= 20:
    #     if float(plate_moment_demand) > float(plate_moment_capacity):
    #         row = [0, "Plate moment capacity (kNm)",
    #                "Moment demand (<i>M</i><sub>d</sub>) = ((" + plate_tk_min + "<sup>2</sup>" + "*" + end_plate_fy + "*" + b_e + ")/(4.4)) * 10^ -3 = " + plate_moment_demand + " <br>[Design of Steel Structures - N. Subramanian, 2014]",
    #                "Moment capacity (<i>M</i><sub>c</sub>) = ((" + end_plate_thickness + "<sup>2</sup>" + "*" + end_plate_fy + "*" + b_e + ")/(4.4)) * 10^ -3 = " + plate_moment_capacity +
    #                "<br>[Design of Steel Structures - N. Subramanian, 2014]", "<p align=left style=color:red><b>Fail</b></p>"]
    #     else:
    #         row = [0, "Plate moment capacity (kNm)",
    #                "Moment demand (<i>M</i><sub>d</sub>) = ((" + plate_tk_min + "<sup>2</sup>" + "*" + end_plate_fy + "*" + b_e + ")/(4.4)) * 10^ -3 = " + plate_moment_demand + " <br>[Design of Steel Structures - N. Subramanian, 2014]",
    #                "Moment capacity (<i>M</i><sub>c</sub>) = ((" + end_plate_thickness + "<sup>2</sup>" + "*" + end_plate_fy + "*" + b_e + ")/(4.4)) * 10^ -3 = " + plate_moment_capacity +
    #                "<br>[Design of Steel Structures - N. Subramanian, 2014]", "<p align=left style=color:green><b>Pass</b></p>"]
    # else:
    #     row = [0, "Plate moment capacity (kNm)", "Moment demand (<i>M</i><sub>d</sub>) = Cannot compute",
    #            "Moment capacity (<i>M</i><sub>c</sub>) = Cannot compute", "<p align=left style=color:red><b>Fail</b></p>"]
    #
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')

# weld checks
    rstr += t('tr')
    row = [0, "Weld Checks", " "]
    rstr += t('td colspan="4" class="detail" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')


    if weld_method == "Groove Weld (CJP)":
        row = [0, "Gap between beam and plate","Refernce: IS 9595:1996, Annex B",weld_size,""]
        rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
        rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
        rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
        rstr += t('/tr')
    else:
        rstr += t('/tr')
        # row = [0,"","","",""]


  # flange web checks
    rstr += t('tr')
    row = [0, "Flange", " "]
    rstr += t('td colspan="4" class="detail1" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')


    # Weld thickness at flange
    rstr += t('tr')
    if weld_method == "Fillet Weld":
        if float(number_of_bolts) <= 20:
            row = [0, "Effective weld length on top flange (mm)", "", flange_weld_effective_length_top, ""]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')

            row = [0, "Effective weld length on bottom flange (mm)", "", flange_weld_effective_length_bottom, ""]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')

            if float(flange_weld_size_provd) < float(flange_weld_size_min) or float(flange_weld_size_provd) > (flange_weld_size_max):
                row = [0, "Weld throat thickness at flange (mm)", "&#60; " + str(flange_weld_size_max) + ",""&#62; " + str(flange_weld_size_min) , str(float(flange_weld_size_provd)), " <p align=left style=color:red><b>Fail</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')

            else:
                row = [0, "Weld throat thickness at flange (mm)", "&#60; " + str(flange_weld_size_max) + ",""&#62; " + str(flange_weld_size_min) , str(float(flange_weld_size_provd)), " <p align=left style=color:green><b>Pass</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')

            if float(flange_weld_stress) > float(flange_weld_strength):
                row = [0, "Critical stress in weld at flange (N/mm^2)","&#8805; ((M/<i>Z</i><sub>weld,flange</sub>) + (P/<i>A</i><sub>weld</sub>)) ="+ flange_weld_stress,"(<i>f</i><sub>u</sub> / &#8730;3 * <i>&#120574;</i><sub>mb</sub>) = "+ flange_weld_strength, " <p align=left style=color:red><b>Fail</b></p>"]


            else:
                row = [0, "Critical stress in weld at flange (N/mm^2)","&#8805; ((M/<i>Z</i><sub>weld,flange</sub>) + (P/<i>A</i><sub>weld</sub>)) ="+ flange_weld_stress,"(<i>f</i><sub>u</sub> / &#8730;3 * <i>&#120574;</i><sub>mb</sub>) = "+ flange_weld_strength, " <p align=left style=color:green><b>Pass</b></p>"]

    else:
        row = [0,"Weld Size at Flange (mm)","min(beam flange thickness, end plate thickness) = min(" +str(float(beam_tf)) + " , "+str(float(plate_thk))+")" ,groove_weld_size_flange,""]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # rstr += t('tr')
    # if weld_method == "Fillet Weld":
    #     if float(number_of_bolts) <= 20:
    #
    #
    #         if float(flange_weld_stress) > float(flange_weld_strength):
    #             row = [0, "Critical stress in weld at flange (N/mm^2)",
    #                    "&#8805; (<i>f</i><sub>u</sub> / (<i>&#120574;</i><sub>mb</sub> * &#8730;3)) =" + flange_weld_stress,
    #                    "(<i>f</i><sub>u</sub> * <i>l</i><sub>w</sub> * <i>t</i><sub>e</sub>) / (<i>&#120574;</i><sub>mw</sub> * &#8730;3) = " + flange_weld_strength, " <p align=left style=color:red><b>Fail</b></p>"]
    #         else:
    #             row = [0, "Critical stress in weld at flange (N/mm^2)",
    #                    "&#8805; (<i>f</i><sub>u</sub> / (<i>&#120574;</i><sub>mb</sub> * &#8730;3)) =" + flange_weld_stress,
    #                    "(<i>f</i><sub>u</sub> * <i>l</i><sub>w</sub> * <i>t</i><sub>e</sub>) / (<i>&#120574;</i><sub>mw</sub> * &#8730;3) = " + flange_weld_strength, " <p align=left style=color:green><b>Pass</b></p>"]
    # else:
    #     pass
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')


# web checks
    rstr += t('tr')
    row = [0, "Web", " "]
    rstr += t('td colspan="4" class="detail1" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # Weld thickness at web
    rstr += t('tr')
    if weld_method == "Fillet Weld":
        if float(number_of_bolts) <= 20:
            row = [0, "Effective weld length at web (each side) (mm)", "", web_weld_effective_length, ""]
            rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
            rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
            rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
            rstr += t('/tr')

            if float(web_weld_size_provd) < float(web_weld_size_min) or float(web_weld_size_provd) > (web_weld_size_max):
                row = [0, "Weld throat thickness at web (mm)", "&#60; " + str(web_weld_size_max)+ ",""&#62; " + str(web_weld_size_min) , web_weld_size_provd, " <p align=left style=color:red><b>Fail</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')

            else:
                row = [0, "Weld throat thickness at web (mm)", "&#60; " + str(web_weld_size_max)+ ",""&#62; " + str(web_weld_size_min) , web_weld_size_provd, " <p align=left style=color:green><b>Pass</b></p>"]
                rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
                rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
                rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
                rstr += t('/tr')

            if float(web_weld_stress) > float(web_weld_strength):
                row = [0, "Critical stress in weld at web (N/mm^2)",
                       "&#8805; &#8730; ((M/<i>Z</i><sub>weld,web</sub> + P/<i>A</i><sub>weld</sub>)<i></i><sup>2</sup>)) + (V/<i>A</i><sub>weld,web</sub>)<i></i><sup>2</sup> =" + web_weld_stress,
                       "(<i>f</i><sub>u</sub> / &#8730;3 * <i>&#120574;</i><sub>mb</sub>) = " + web_weld_strength,
                       " <p align=left style=color:red><b>Fail</b></p>"]

            else:
                row = [0, "Critical stress in weld at web (N/mm^2)",
                       "&#8805; &#8730; ((M/<i>Z</i><sub>weld,web</sub> + P/<i>A</i><sub>weld</sub>)<i></i><sup>2</sup>)) + (V/<i>A</i><sub>weld,web</sub>)<i></i><sup>2</sup> =" + web_weld_stress,
                       "(<i>f</i><sub>u</sub> / &#8730;3 * <i>&#120574;</i><sub>mb</sub>) = " + web_weld_strength,
                       " <p align=left style=color:green><b>Pass</b></p>"]

    else:
        row = [0, "Weld Size at Web (mm)","min(beam web thickness, plate thickness) = min("+ str(float(beam_tw)) +" , "+ str(float(plate_thk)) + ")", groove_weld_size_web, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # rstr += t('tr')
    # if weld_method == "Fillet Weld":
    #     if float(number_of_bolts) <= 20:
    #         if float(web_weld_stress) > float(web_weld_strength):
    #             row = [0, "Critical stress in weld at flange (N/mm^2)",
    #                    "&#8805; (<i>f</i><sub>u</sub> / (<i>&#120574;</i><sub>mb</sub> * &#8730;3)) =" + web_weld_stress,
    #                    "(<i>f</i><sub>u</sub> * <i>l</i><sub>w</sub> * <i>t</i><sub>e</sub>) / (<i>&#120574;</i><sub>mw</sub> * &#8730;3) = " + web_weld_strength,
    #                    " <p align=left style=color:red><b>Fail</b></p>"]
    #         else:
    #             row = [0, "Critical stress in weld at flange (N/mm^2)",
    #                    "&#8805; (<i>f</i><sub>u</sub> / (<i>&#120574;</i><sub>mb</sub> * &#8730;3)) =" + web_weld_stress,
    #                    "(<i>f</i><sub>u</sub> * <i>l</i><sub>w</sub> * <i>t</i><sub>e</sub>) / (<i>&#120574;</i><sub>mw</sub> * &#8730;3) = " + web_weld_strength,
    #                    " <p align=left style=color:green><b>Pass</b></p>"]
    # else:
    #     pass
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')



    # if float(number_of_bolts) <= 20:
    #     if float(critical_stress_flange) > float(weld_strength):
    #         row = [0, "Critical stress in weld at flange (N/mm^2)", "&#8804; " + str(weld_fu_govern) + " / (&#8730;3 * 1.25) = " + weld_strength +
    #                "<br> [cl. 10.5.7]", "(" + force_flange + "* 10^3)/(3 * " + str(effective_length_flange) + ") = " + critical_stress_flange,
    #                " <p align=left style=color:red><b>Fail</b></p>"]
    #     else:
    #         row = [0, "Critical stress in weld at flange (N/mm^2)", "&#8804; " + str(weld_fu_govern) + " / (&#8730;3 * 1.25) = " + weld_strength +
    #                "<br> [cl. 10.5.7]", "(" + force_flange + "* 10^3)/(3 * " + str(effective_length_flange) + ") = " + critical_stress_flange,
    #                " <p align=left style=color:green><b>Pass</b></p>"]
    # else:
    #     row = [0, "Critical stress in weld at flange (N/mm^2)", " Cannot compute ", " Cannot compute ", " <p align=left style=color:red><b>Fail</b></p>"]
    #
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    # rstr += t('/tr')
    #
    # # Weld at web
    # rstr += t('tr')
    #
    # if float(number_of_bolts) <= 20:
    #     if float(critical_stress_web) > float(weld_strength):
    #         row = [0, "Critical stress in weld at web (N/mm ^ 2)",
    #                "&#8804; " + str(weld_fu_govern) + "/(&#8730;3 * 1.25) = " + weld_strength +
    #                "<br> [cl. 10.5.7 and cl. 10.5.10]", "&#8730;((" + str(fa_web) + ")^2 + (3 * " + str(q_web) + "^2)) =" + critical_stress_web,
    #                " <p align=left style=color:red><b>Fail</b></p>"]
    #     else:
    #         row = [0, "Critical stress in weld at web (N/mm ^ 2)",
    #                "&#8804; " + str(weld_fu_govern) + "/(&#8730;3 * 1.25) = " + weld_strength +
    #                "<br> [cl. 10.5.7 and cl. 10.5.10]", "&#8730;((" + str(fa_web) + ")^2 + (3 * " + str(q_web) + "^2)) =" + critical_stress_web,
    #                " <p align=left style=color:green><b>Pass</b></p>"]
    # else:
    #     row = [0, "Critical stress in weld at web (N/mm ^ 2)", " Cannot compute", " Cannot compute ", " <p align=left style=color:red><b>Fail</b></p>"]
    #
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    # rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    # rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    #
    # # Stiffener Checks
    rstr += t('tr')
    row = [0, "Stiffener Checks", " "]
    rstr += t('td colspan="4" class="detail" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

# Horizontal continuity plate in tension
    rstr += t('tr')
    row = [0, "Horizontal Continuity Plate in Tension", " "]
    rstr += t('td colspan="4" class="detail1" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')


    rstr += t('tr')
    row = [0, "Length (mm)", "", cont_plate_tens_length, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')


    rstr += t('tr')
    row = [0, "Width (mm)", "", cont_plate_tens_width, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')


    rstr += t('tr')
    row = [0, "Thickness (mm)", "&#8805;"+ str(round(float(cont_plate_comp_thk_min),3)), cont_plate_tens_thk, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')


    rstr += t('tr')
    row = [0, "Weld (mm)", "", cont_plate_tens_weld, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

# Horizontal continuity plate in comp
    rstr += t('tr')
    row = [0, "Horizontal Continuity Plate in Compression", " "]
    rstr += t('td colspan="4" class="detail1" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Length (mm)", "", cont_plate_comp_length, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Width (mm)", "", cont_plate_comp_width, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Thickness (mm)", "&#8805;"+ str(round(float(cont_plate_comp_thk_min),3)), cont_plate_comp_thk, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Weld (mm)", "", cont_plate_comp_weld, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    # End Plate Stifferners
    rstr += t('tr')
    row = [0, "End Plate Stiffeners", " "]
    rstr += t('td colspan="4" class="detail1" align="center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Length (mm)", "", st_length, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Height (mm)", "", st_height, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Thickness (mm)", "", st_thk, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Noch at top side of plate (mm)", "", st_notch_top, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Noch at bottom side of plate (mm)", "", st_notch_bottom, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Fillet weld size (mm)", "", st_weld, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

    # ######################################### End of checks #########################################
    # Header of the pdf fetched from dialogbox

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
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

    if status == "True":

        row = [0, "Fabrication Drawings", " "]
        rstr += t('tr')
        rstr += t('td colspan="2" class=" detail" align=center '
                  '') + space(row[0]) + row[1] + t('/td')
        rstr += t('/tr')
        png = folder + "/images_html/3D_Model.png"
        datapng = '<object type="image/PNG" data= %s height = "360px" width = "auto" ></object>' % png

        side = folder + "/images_html/extendSide.png"
        dataside = '<object type="image/PNG" data= %s height = "480px" width = "auto" ></object>' % side

        top = folder + "/images_html/extendTop.png"
        datatop = '<object type="image/PNG" data= %s height = "360px" width = "560px" ></object>' % top

        front = folder + "/images_html/extendFront.png"
        datafront = '<object type="image/PNG" data= %s height = "480px" width = "auto" ></object>' % front

        if status == 'True':
            row = [0, datapng]
            rstr += t('tr')
            rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')


            row = [1, datatop]
            rstr += t('tr')
            rstr += t('td align="center" class=" header2 "') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

        else:
            pass

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')




        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
        row = [0, "Fabrication Drawings", " "]
        rstr += t('tr')
        rstr += t('td colspan="2" class=" detail" align=center '
                  '') + space(row[0]) + row[1] + t('/td')
        rstr += t('/tr')
        png = folder + "/images_html/3D_Model.png"
        datapng = '<object type="image/PNG" data= %s height = "360px" width = "auto" ></object>' % png

        side = folder + "/images_html/extendSide.png"
        dataside = '<object type="image/PNG" data= %s height = "450px" width = "560px" ></object>' % side

        top = folder + "/images_html/extendTop.png"
        datatop = '<object type="image/PNG" data= %s height = "360px" width = "auto" ></object>' % top

        front = folder + "/images_html/extendFront.png"
        datafront = '<object type="image/PNG" data= %s height = "450px" width = "560px" </object>' % front

        if status == 'True':
            row = [1, dataside]
            rstr += t('tr')
            rstr += t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

            row = [1, datafront]
            rstr += t('tr')
            rstr += t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

        else:
            pass

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

    else:
        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

        row = [0, "Fabrication Drawings", " "]
        rstr += t('tr')
        rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
        rstr += t('/tr')

        row = [0, "The fabrication drawings are not been generated due to the failure of the connection.", " "]
        rstr += t('tr')
        rstr += t('td colspan="2" class=" detail1"') + space(row[0]) + row[1] + t('/td')
        rstr += t('/tr')

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

        # png = folder + "/images_html/3D_Model.png"
        # datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png
        #
        # side = folder + "/images_html/extendSide.png"
        # dataside = '<object type="image/PNG" data= %s width ="400"></object>' % side
        #
        # top = folder + "/images_html/extendTop.png"
        # datatop = '<object type="image/PNG" data= %s width ="400"></object>' % top
        #
        # front = folder + "/images_html/extendFront.png"
        # datafront = '<object type="image/PNG" data= %s width ="450"></object>' % front
        #
        # if status == 'True':
        #     row = [0, datapng, datatop]
        #     rstr += t('tr')
        #     rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
        #     rstr += t('td  align="center" class=" header2"') + row[2] + t('/td')
        #     rstr += t('/tr')
        #
        #     row = [0, dataside, datafront]
        #     rstr += t('tr')
        #     rstr += t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
        #     rstr += t('td align="center" class=" header2 "') + row[2] + t('/td')
        #     rstr += t('/tr')
        #
        # else:
        #     pass



    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

    if weld_method == "Groove Weld (CJP)":

        # rstr += t('/table')
        # rstr += t('hr')
        # rstr += t('/hr')

        row = [0, "Weld Detailing", " "]
        rstr += t('tr')
        rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
        rstr += t('/tr')

        if float(beam_tf) <= float(12):
            row = [0, '<object type= "image/PNG" data= "Butt_weld_single_flange.png"  ></object>']
            rstr += t('tr')
            rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

            row = [0, "Note :- As flange thickness, <i>t</i><sub>f</sub> (" + str(float(beam_tf)) + "mm) <= 12mm, single bevel butt welding is provided [Reference: IS 9595: 1996] (All dimensions are in mm )", " "]
            rstr += t('tr')
            rstr += t('td colspan="1" class=" detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

        else:
            row = [0, '<object type= "image/PNG" data= "Butt_weld_double_flange.png"  ></object>']
            rstr += t('tr')
            rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

            row = [0,
                   "Note :- As flange thickness, <i>t</i><sub>f</sub> (" + str(float(beam_tf)) + "mm) >= 12mm, double bevel butt welding is provided [Reference: IS 9595: 1996] (All dimensions are in mm )",
                   " "]
            rstr += t('tr')
            rstr += t('td colspan="2" class=" detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

        if float(beam_tw) <= float(12):
            row = [0, '<object type= "image/PNG" data= "Butt_weld_single_web.png"  ></object>']
            rstr += t('tr')
            rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

            row = [0,
                   "Note :- As flange thickness, <i>t</i><sub>w</sub> (" + str(float(beam_tw)) + "mm) <= 12mm, single bevel butt welding is provided [Reference: IS 9595: 1996] (All dimensions are in mm )",
                   " "]
            rstr += t('tr')
            rstr += t('td colspan="2" class=" detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

        else:
            row = [0, '<object type= "image/PNG" data= "Butt_weld_double_web.png"  ></object>']
            rstr += t('tr')
            rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

            row = [0,
                   "Note :- As flange thickness, <i>t</i><sub>w</sub> (" + str(float(beam_tw)) + "mm) >= 12mm, double bevel butt welding is provided [Reference: IS 9595: 1996] (All dimensions are in mm )",
                   " "]
            rstr += t('tr')
            rstr += t('td colspan="2" class=" detail1"') + space(row[0]) + row[1] + t('/td')
            rstr += t('/tr')

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

    else:
        rstr += t('/tr')

    # ###########################################################################################
    # Header of the pdf fetched from dialougebox

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
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
