'''
Created on Dec 10, 2015
@author: deepa
'''
from __builtin__ import str
import time
import math

from Connections.connection_calculations import ConnectionCalculations


def save_html(outobj, uiobj, dictbeamdata, dictcolumndata, reportsummary, filename, folder):

    print outobj
    filename = filename
    myfile = open(filename, "w")
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
    client = str(reportsummary['Client'])
    addtionalcomments = str(reportsummary['AdditionalComments'])

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# End Plate Main Data

    beam_tw = str(float(dictbeamdata["tw"]))
    beam_f_t = str(float(dictbeamdata["T"]))
    beam_d = str(float(dictbeamdata["D"]))
    beam_R1 = str(float(dictbeamdata["R1"]))
    beam_b = str(float(dictbeamdata["B"]))

    column_w_t = str(float(dictcolumndata["tw"]))
    column_f_t = str(float(dictcolumndata["T"]))
    column_R1 = str(float(dictcolumndata["R1"]))
    column_d = str(float(dictcolumndata["D"]))
    column_b = str(float(dictcolumndata["B"]))

###############################################################################################################################
    connectivity = str(uiobj['Member']['Connectivity'])
    shear_load = str(uiobj['Load']['ShearForce (kN)'])
    column_sec = str(uiobj['Member']['ColumSection'])
    beam_sec = str(uiobj['Member']['BeamSection'])
    plate_thickness = str(uiobj['Plate']['Thickness (mm)'])
    bolt_type = str(uiobj['Bolt']['Type'])
    bolt_grade = str(uiobj['Bolt']['Grade'])
    bolt_diameter = str(uiobj['Bolt']['Diameter (mm)'])
    beam_fu = str(uiobj['Member']['fu (MPa)'])
    beam_fy = str(uiobj['Member']['fy (MPa)'])
    weld_size = str(uiobj["Weld"]['Size (mm)'])

    # Design Preferences
    bolt_hole_clrnce = str(float(uiobj["bolt"]["bolt_hole_clrnce"]))
    bolt_hole_type = str(uiobj["bolt"]["bolt_hole_type"])
    bolt_grade_fu = str(float(uiobj["bolt"]["bolt_fu"]))
    slip_factor = str(float(uiobj["bolt"]["slip_factor"]))

    typeof_weld = str(uiobj["weld"]["typeof_weld"])
    safety_factor = str(float(uiobj["weld"]["safety_factor"]))
    fu_overwrite = str(float(uiobj["weld"]["fu_overwrite"]))

    typeof_edge = str(uiobj["detailing"]["typeof_edge"])
    min_edgend_dist = str(float(uiobj["detailing"]["min_edgend_dist"]))
    gap = str(float(uiobj["detailing"]["gap"]))
    corrosive = str(uiobj["detailing"]["is_env_corrosive"])

    design_method = str(uiobj["design"]["design_method"])

    # To call k_h value from Friction Grip Bolt calculations
    bolt_param_k_h = ConnectionCalculations.calculate_k_h(bolt_hole_type=bolt_hole_type)
    k_h = str(float(bolt_param_k_h))

    # To call F_0 value from Friction Grip Bolt calculations
    bolt_param_F_0 = ConnectionCalculations.proof_load_F_0(bolt_diameter=bolt_diameter, bolt_fu=bolt_grade_fu)
    F_0 = str(float(bolt_param_F_0))

    maxplatethk = str(int(round(outobj['Plate']['MaxThick'], 1)))
    blockshear = str(int(round(outobj['Plate']['blockshear'], 1)))

    plate_width = str(int(round(outobj['Plate']['width'], 1)))
    plate_minwidth = str(int(round(outobj['Plate']['MinWidth'], 1)))
    plate_length = str(int(round(outobj['Plate']['height'], 1)))
#     weld_size = str(int(round(outobj["Weld"]['Size (mm)'],1)))

    plate_dimension = plate_length + 'X' + plate_width + 'X' + plate_thickness
    no_of_bolts = str(outobj['Bolt']['numofbolts'])
    no_of_rows = str(outobj['Bolt']['numofrow'])
    no_of_cols = str(outobj['Bolt']['numofcol']/2)
    edge = str(int(round(outobj['Bolt']['edge'], 1)))
    gauge = str(int(round(outobj['Bolt']['gauge'], 1)))
    pitch = str(int(round(outobj['Bolt']['pitch'], 1)))
    end = str(int(round(outobj['Bolt']['enddist'], 1)))
    weld_strength = str(round(float(outobj['Weld']['weldstrength']), 3))
    weld_shear = str(round(float(outobj['Weld']['weldshear']), 3))

    bolt_fu = str(outobj['Bolt']['bolt_fu'])
    bolt_dia = str(uiobj['Bolt']['Diameter (mm)'])
    kb = str(outobj['Bolt']['kb'])
    t_thinner = str(outobj['Bolt']['thinner'])

#     kb = str(0.5)
    dia_hole = str(outobj['Bolt']['dia_hole'])
    weld_fu = str(410)
    weld_l = str(outobj['Weld']['weldlength'])
    shear_capacity = str(float(round(outobj['Bolt']['shearcapacity'], 3)))
    # bearingcapacity = str(round(outobj['Bolt']['bearingcapacity'], 4))
    bearingcapacity = str(outobj['Bolt']['bearingcapacity'])
    critical_shear = str(float(round(outobj['Bolt']['critshear'], 0)))
    status = outobj['Bolt']['status']

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Design Conclusion
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    row = [0, "Design Conclusion", "IS800:2007/Limit state design"]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    if status is True:
        row = [1, "End Plate", "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [1, "End Plate", "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('tr')
    rstr += t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1 "') + row[2] + t('/td')
    # rstr += t('td class="header1 safe"') + row[3] + t('/td')
    rstr += t('/tr')

    row = [0, "End Plate", " "]
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

    row = [1, "Connection Title", " Flexible End Plate"]
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

    if connectivity == "Beam-Beam":
        row = [1, "Primary Beam", "Bolted"]
    else:
        row = [1, "Column Connection", "Bolted"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    if connectivity == "Beam-Beam":
        row = [1, "Secondary Beam", "Welded"]
    else:
        row = [1, "Beam Connection", "Welded"]
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
    if connectivity == "Beam-Beam":
        row = [1, "Primary Beam", column_sec]
    else:
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
    if connectivity == "Beam-Beam":
        row = [1, "Secondary Beam", beam_sec]
    else:
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

    row = [2, "Hole", bolt_hole_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [1, "Plate Section ", "PLT 300X10X100 "]
    row = [1, "Plate Section", plate_dimension]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Thickness (mm)", "10"]
    row = [2, "Thickness (mm)", plate_thickness]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Width (mm)", "10"]
    row = [2, "Width (mm)", plate_width]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Depth (mm)", "300"]
    row = [2, "Depth (mm)", plate_length]
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

    # row = [2, "Size (mm)", "6"]
    row = [2, "Size (mm)", weld_size]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Bolts ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    # row = [2, "Type", "Friction Grip Bolt"]
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
    row = [2, "Bolt Numbers", no_of_bolts]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Columns (Vertical Lines)", "1 "]
    row = [2, "Columns (Vertical Lines)", no_of_cols]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolts Per Column", "3"]
    row = [2, "Bolts Per Column", no_of_rows]
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
    if connectivity == "Beam-Beam":
        row = [1, "Beam-Beam Clearance (mm)", plate_thickness]
    else:
        row = [1, "Column-Beam Clearance (mm)", plate_thickness]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Header of the pdf fetched from dialogbox
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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

    row = [1, "Material Grade (MPa) (overwrite)", bolt_grade_fu]
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

    row = [1, "Material Grade (MPa) (overwrite)", fu_overwrite]
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

    row = [1, "Are members exposed to corrosive influences?", corrosive]
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
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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

# *******************************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Design Check

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

    rstr += t('tr')
    const = str(round(math.pi / 4 * 0.78, 4))
    # row =[0,"Bolt shear capacity (kN)"," ","<i>V</i><sub>dsb</sub> = ((800*0.6123*20*20)/(&#8730;3*1.25*1000) = 90.53 <br> [cl. 10.3.3]"]
    n_e = str(1)
    if bearingcapacity == "N/A":
        row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsf</sub> = ((" + slip_factor + "*" + n_e + "*" + k_h + "*" +F_0 +
               ")/(1.25)) = " + shear_capacity + "<br> [cl. 10.4.3]", ""]
    else:
        row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsb</sub> = ((" + bolt_fu + "*" + const + "*" + bolt_dia + "*" +
               bolt_dia + ")/(&#8730;3*1.25*1000) = " + shear_capacity + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if bearingcapacity == "N/A":
        row = [0, "Bolt bearing capacity (kN)", "", "N/A", ""]
    else:

        row = [0, "Bolt bearing capacity (kN)", "",
               " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + t_thinner + "*" + beam_fu + ")/(1.25*1000)  = " +
               bearingcapacity + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    if bearingcapacity == "N/A" :
        bolt_capacity = str(float(shear_capacity))
        row = [0, "Bolt capacity (kN)", "",   bolt_capacity, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        # boltCapacity = bearingcapacity if bearingcapacity < shearCapacity else shearCapacity
        bolt_capacity =  str(min(float(shear_capacity), float(bearingcapacity)))
        row = [0, "Bolt capacity (kN)", "", "Min (" + shear_capacity + ", " + bearingcapacity + ") = " + bolt_capacity, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Critical Bolt Shear (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    if critical_shear > bolt_capacity:
        row = [0, "Critical bolt shear (kN)", " &#8804; " + bolt_capacity, critical_shear,"<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Critical bolt shear (kN)", " &#8804; " + bolt_capacity, critical_shear,"<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
#     bolts = str(round(float(shear_load)/float(bolt_capacity),1))
#     row =[0,"No. of bolts", shear_load + "/" + bolt_capacity + " = " + bolts, no_of_bolts, " <p align=left style=color:green><b>Pass</b></p>"]
    row = [0, "No. of bolts", "", no_of_bolts, " "]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No.of column(s) per side of end plate", " &#8804; 2", no_of_cols , ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts per column"," ","3"]
    row = [0, "No. of bolts per column per side of end plate", " ", no_of_rows, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    min_pitch = str(int(2.5 * float(bolt_dia)))
    max_pitch = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    if pitch >= min_pitch or pitch <= max_pitch:
        row = [0, "Bolt pitch (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_pitch + ",  &#8804; Min(32*" + beam_tw + ", 300) = " + max_pitch +
               "<br> [cl. 10.2.2]", pitch, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Bolt pitch (mm)", " &#8805; 2.5*" + bolt_dia + " = " + min_pitch + ",  &#8804; Min(32*" + beam_tw + ", 300) = " + max_pitch +
           "<br> [cl. 10.2.2]", pitch, "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    min_gauge = str(int(2.5 * float(bolt_dia)))
    max_gauge = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    if gauge >= min_gauge or gauge <= max_gauge:
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge, "<p align=left style=color:red><b>Fail</b></p>"]

    if no_of_cols >= str(2):
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Bolt gauge (mm)", " &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + max_gauge +
           " <br> [cl. 10.2.2]", gauge, "<p align=left style=color:green><b>" "</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"End distance (mm)","&#8805;1.7* 22 = 37.4,&#8804;12*8.9 = 106.9 <br> [cl. 10.2.4]","50"]
    min_end = str(int(float(min_edgend_dist) * float(dia_hole)))
    max_end = str(float(12 * float(beam_tw)))
    if end >= min_end or end <= max_end:
        row = [0, "End distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + min_end + ", &#8804; 12*" + beam_tw + " = " + max_end + " <br> [cl. 10.2.4]",end,
               "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "End distance (mm)", " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + min_end + ", &#8804; 12*" + beam_tw + " = " + max_end + " <br> [cl. 10.2.4]", end,
           "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Edge distance (mm)","&#8805; 1.7* 22 = 37.4,&#8804;12*8.9 = 106.9<br> [cl. 10.2.4]","50"," <p align=right style=color:green><b>Pass</b></p>"]
    min_edge = str(int(float(min_edgend_dist) * float(dia_hole)))
    max_edge = str(float(12 * float(beam_tw)))
    if edge >= min_edge or edge <= max_edge:
        row = [0, "Edge distance (mm)",
               " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + min_edge + ", &#8804; 12*" + beam_tw + " = " + max_edge + "<br> [cl. 10.2.4]",edge,
               " <p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Edge distance (mm)", " &#8805; " + min_edgend_dist + " * " + dia_hole + " = " + min_edge + ", &#8804; 12*" + beam_tw + " = " + max_edge + "<br> [cl. 10.2.4]", edge,
           " <p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    if float(blockshear) < float(shear_load):
        row = [0, "Block shear capacity (kN)", "&#8805;  " + shear_load,
               "<i>V</i><sub>db</sub> = " + blockshear + "<br> [cl. 6.4.1]", "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Block shear capacity (kN)", "&#8805;  " + shear_load, "<i>V</i><sub>db</sub> = " + blockshear + "<br> [cl. 6.4.1]", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Plate thickness (mm)","(5*140*1000)/(300*250)= 9.33","10"]
    if int(maxplatethk) < int(plate_thickness):
        row = [0, "Plate thickness (mm)", "&#8804;  " + maxplatethk, plate_thickness,
               " <p align=left style=color:red><b>Fail</b></p> "]
    else:
        row = [0, "Plate thickness (mm)", "&#8804;  " + maxplatethk, plate_thickness, " <p align=left style=color:green><b>Pass</b></p> "]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    if connectivity == "Beam-Beam":
        max_len = str(float(beam_d) - float(column_R1) - float(column_f_t) - float(beam_f_t) - float(beam_R1) - 5)
        str_max_len = "-" + beam_f_t + "-" + beam_R1 + "-" + column_f_t + "-" + column_R1 + "- 5"
    else:
        max_len = str(float(beam_d) - 2 * (float(beam_f_t) + float(beam_R1) + 5))
        str_max_len = "-" + beam_f_t + "-" + beam_R1 + "-" + beam_f_t + "-" + beam_R1 + "- 10"
    min_len = str(0.6 * float(beam_d))

    if plate_length >= min_len or plate_length <= max_len:
        row = [0, "Plate height (mm)", "&#8805; 0.6*" + beam_d + "=" + min_len + ", &#8804; " + beam_d + str_max_len + "=" + max_len +
           "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", plate_length, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    else:
        row = [0, "Plate height (mm)","&#8805; 0.6*" + beam_d + "=" + min_len + ", &#8804; " + beam_d + str_max_len + "=" + max_len +
               "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", plate_length," <p align=left style=color:red><b>Fail</b></p>", "300", ""]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    str_max_len = ""
    max_width = ""
    if connectivity == "Column web-Beam web":
        max_width = str(float(column_d) - 2 * (float(column_R1) + float(column_f_t) + 5))
        str_max_len = column_d + "-2*(" + column_f_t + "+" + column_R1 + " +5)"
    elif connectivity == "Column flange-Beam web":
        max_width = str(float(column_b))
        str_max_len = column_b
    else:
        max_width = str(int(140 + 2 * (int(gauge + end))))
        str_max_len = "140" + "2*(" + gauge + end + ")"

    min_width = plate_minwidth

    if plate_width >= min_width or plate_width <= max_width:
        row = [0, "Plate Width (mm)", "&#8805; " + min_width + ", &#8804; " + max_width + "<br>", plate_width,
           " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    else:
        row = [0, "Plate Width (mm)", "&#8805; " + min_width + ", &#8804; " + max_width + "<br>", plate_width,
               " <p align=left style=color:red><b>Fail</b></p>", "300", ""]
    # row =[0,"Plate width (mm)","",plate_width]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Effective weld length (mm)","","300 - 2*6 = 288"]
    eff_weld_len = str(int(float(plate_length) - (2 * float(weld_size))))
    row = [0, "Effective weld length on each side(mm)", "", plate_length + "-2*" + weld_size + " = " + eff_weld_len, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Weld strength (kN/mm)","&#8730;[(18100*6)/(2*288)<sup>2</sup>]<sup>2</sup> + [140/(2*288)]<sup>2</sup> <br>=0.699","<i>f</i><sub>v</sub>=(0.7*6*410)/(&#8730;3*1.25)<br>= 0.795<br>[cl. 10.5.7]"," <p align=right style=color:green><b>Pass</b></p>"]
    if float(weld_shear) > float(weld_strength):
        row = [0, "Weld strength (kN/mm)", weld_shear, "<i>f</i><sub>v</sub> =(0.7*" + weld_size + "*" + weld_fu + ")/(&#8730;3*1.25*1000)<br> = " + weld_strength +
               "<br>[cl. 10.5.7]", " <p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Weld strength (kN/mm)", weld_shear, "<i>f</i><sub>v</sub> =(0.7*" + weld_size + "*" + weld_fu + ")/(&#8730;3*1.25*1000)<br> = " + weld_strength +
           "<br>[cl. 10.5.7]", " <p align=left style=color:green><b>Pass</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')


# ***********************************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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

# ************************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Diagram

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

    row = [0, "Views", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class=" viewtbl "') + row[2] + t('/td')
    rstr += t('/tr')

#     png = folder + "/images_html/" + base
    png = folder + "/images_html/3D_Model.png"
    datapng = '<object type="image/PNG" data= %s  width ="450"></object">' % png

# **************************************************** for svg to png ********************************************************************
#     side = folder + "/images_html/" + base_side
#     side = folder + "/images_html/endSide.svg"
#     dataside = '<object type="image/svg+xml" data=%s  width ="400"></object>' % side
# ******************************************************************************************************************************************
    side = folder + "/images_html/endSide.png"
    dataside = '<object type="image/PNG" data=%s  width ="400"></object>' % side

# ******************************************** for svg to png *****************************************************************************
#     top = folder + "/images_html/" + base_top
#     top = folder + "/images_html/endTop.svg"
#     datatop = '<object type="image/svg+xml" data= %s  width ="400"></object>' % top
# *****************************************************************************************************************************************
    top = folder + "/images_html/endTop.png"
    datatop = '<object type="image/PNG" data= %s  width ="400"></object>' % top

# ******************************************** for svg to png ****************************************************************************
#     front = folder + "/images_html/" + base_front
#     front = folder + "/images_html/endFront.svg"
#     datafront = '<object type="image/svg+xml" data=%s  width ="450"></object>' % front
# ******************************************************************************************************************************************
    front = folder + "/images_html/endFront.png"
    datafront = '<object type="image/PNG" data=%s  width ="450"></object>' % front

    if status is True:
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

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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


def quote(m):
    return '"' + m + '"'
