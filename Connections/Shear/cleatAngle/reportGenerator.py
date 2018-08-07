'''
Created on 16-Mar-2016

@author: reshma
'''
import time
import math

from Connections.connection_calculations import ConnectionCalculations


def save_html(output_obj, uiobj, dict_beam_data, dict_col_data, dict_cleat_data, reportsummary, filename, folder):
    print output_obj
    filename = filename
    myfile = open(filename, 'w')
    myfile.write(t('! DOCTYPE html'))
    myfile.write(t('html'))
    myfile.write(t('head'))
    myfile.write(t('link type="text/css" rel="stylesheet"'))

    # ###########################   mystyle.css is written here  ##############################################################################
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

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # CleatAngle Main Data
    beam_sec = str(uiobj['Member']['BeamSection'])
    column_sec = str(uiobj['Member']['ColumSection'])
    connectivity = str(uiobj['Member']['Connectivity'])
    beam_fu = str(uiobj['Member']['fu (MPa)'])
    beam_fy = str(uiobj['Member']['fy (MPa)'])

    shear_load = str(uiobj['Load']['ShearForce (kN)'])

    bolt_dia = str(uiobj['Bolt']['Diameter (mm)'])
    bolt_type = str(uiobj["Bolt"]["Type"])
    bolt_grade = str(uiobj['Bolt']['Grade'])

    bolt_fu = int(float(bolt_grade)) * 100
    bolt_fy = (float(bolt_grade) - int(float(bolt_grade))) * bolt_fu

    bolt_fu = str(bolt_fu)
    bolt_fy = str(bolt_fy)

    cleat_length = str(uiobj['cleat']['Height (mm)'])
    cleat_fu = str(uiobj['Member']['fu (MPa)'])
    cleat_fy = str(uiobj['Member']['fy (MPa)'])
    cleat_sec = str(uiobj['cleat']['section'])

    # Design Preferences
    # bolt_hole_clrnce = str(float(uiobj["bolt"]["bolt_hole_clrnce"]))
    bolt_hole_type = str(uiobj["bolt"]["bolt_hole_type"])
    bolt_grade_fu = str(float(uiobj["bolt"]["bolt_fu"]))
    slip_factor = str(float(uiobj["bolt"]["slip_factor"]))

    typeof_edge = str(uiobj["detailing"]["typeof_edge"])
    min_edgend_dist = str(float(uiobj["detailing"]["min_edgend_dist"]))
    gap = str(float(uiobj["detailing"]["gap"]))
    corrosive = str(uiobj["detailing"]["is_env_corrosive"])

    design_method = str(uiobj["design"]["design_method"])

    # To call k_h value from Friction Grip Bolt calculations
    bolt_param_k_h = ConnectionCalculations.calculate_k_h(bolt_hole_type=bolt_hole_type)
    k_h = str(float(bolt_param_k_h))

    # To call F_0 value from Friction Grip Bolt calculations
    bolt_param_F_0 = ConnectionCalculations.proof_load_F_0(bolt_diameter=bolt_dia, bolt_fu=bolt_grade_fu)
    F_0 = str(float(bolt_param_F_0))

    #     dict_beam_data  = get_beamdata(beam_sec)
    beam_tw = str(float(dict_beam_data["tw"]))
    beam_f_t = str(float(dict_beam_data["T"]))
    beam_d = str(float(dict_beam_data["D"]))
    beam_R1 = str(float(dict_beam_data["R1"]))
    beam_B = str(float(dict_beam_data["B"]))
    beam_D = str(float(dict_beam_data["D"]))

    #      dictcolumndata = get_columndata(column_sec)
    column_w_t = str(float(dict_col_data["tw"]))
    column_f_t = str(float(dict_col_data["T"]))
    column_R1 = str(float(dict_col_data["R1"]))
    column_D = str(float(dict_col_data["D"]))
    column_B = str(float(dict_col_data["B"]))

    #     dict_cleat_data = get_angledata(cleat_sec)
    cleat_legsizes = str(dict_cleat_data["AXB"])
    cleat_legsize_A = int(cleat_legsizes.split('x')[0])
    cleat_legsize_B = int(cleat_legsizes.split('x')[1])

    cleat_legsize = str(int(cleat_legsize_A))
    cleat_legsize_1 = str(int(cleat_legsize_B))
    cleat_thk = str(int(dict_cleat_data["t"]))

    # 'Size (mm)'
    #     weld_Thick = str(uiobj['Weld']['Size (mm)'])
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

    # #########################Output###########################
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
    #     beam_tw = str(float(dict_beam_data["tw"]))
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

    status = str(output_obj['Bolt']['status'])
    # #################output beam part ###########
    #     kb = "0.5"
    kb = str(output_obj['Bolt']['kb'])
    shear_capacity_b = str(output_obj['Bolt']['shearcapacity'])
    bearingcapacity_b = str(output_obj['Bolt']['bearingcapacity'])
    boltbearingcapacity_b = str(output_obj['Bolt']['boltbearingcapacity'])
    bearingcapacitybeam_b = str(output_obj['Bolt']['bearingcapacitybeam'])
    bearingcapacitycleat_b = str(output_obj['Bolt']['bearingcapacitycleat'])

    moment_demand_b = str(output_obj['Bolt']['externalmoment'])
    moment_capacity_b = str(output_obj['Bolt']['momentcapacity'])

    blockshear_b = str(output_obj['Bolt']['blockshear'])
    critboltshear_b = str(output_obj['Bolt']['critshear'])

    bolt_capacity_b = str(output_obj['Bolt']['boltcapacity'])
    no_of_bolts_b = str(output_obj['Bolt']['numofbolts'])
    no_of_rows_b = str(output_obj['Bolt']['numofrow'])
    no_of_col_b = str(output_obj['Bolt']['numofcol'])
    pitch_b = str(output_obj['Bolt']['pitch'])
    dia_hole = str(output_obj['Bolt']['diahole'])
    # edge_b = str(output_obj['Bolt']['enddist'])
    # end_b = str(output_obj['Bolt']['edge'])

    end_b = str(output_obj['Bolt']['enddist'])
    edge_b = str(output_obj['Bolt']['edge'])

    gauge_b = str(output_obj['Bolt']['gauge'])
    bolt_grp_capacity_b = str(output_obj['Bolt']['boltgrpcapacity'])
    thinner_b = str(output_obj['Bolt']['thinner'])
    # ################# output column part ###########
    shear_capacity_c = str(output_obj['cleat']['shearcapacity'])
    bearingcapacity_c = str(output_obj['cleat']['bearingcapacity'])
    boltbearingcapacity_c = str(output_obj['cleat']['boltbearingcapacity'])
    bearingcapacitycolumn_c = str(output_obj['cleat']['bearingcapacitycolumn'])
    bearingcapacitycleat_c = str(output_obj['cleat']['bearingcapacitycleat'])

    blockshear_c = str(output_obj['cleat']['blockshear'])
    critboltshear_c = str(output_obj['cleat']['critshear'])

    moment_demand_c = str(output_obj['cleat']['externalmoment'])
    moment_capacity_c = str(output_obj['cleat']['momentcapacity'])

    bolt_capacity_c = str(output_obj['cleat']['boltcapacity'])
    no_of_bolts_c = str(output_obj['cleat']['numofbolts'])
    no_of_rows_c = str(output_obj['cleat']['numofrow'])
    no_of_col_c = str(output_obj['cleat']['numofcol'])
    pitch_c = str(output_obj['cleat']['pitch'])
    height_c = str(output_obj['cleat']['height'])
    # edge_c = str(output_obj['cleat']['end'])
    # end_c = str(output_obj['cleat']['edge'])

    end_c = str(output_obj['cleat']['end'])
    edge_c = str(output_obj['cleat']['edge'])

    gauge_c = str(output_obj['cleat']['guage'])
    bolt_grp_capacity_c = str(output_obj['cleat']['boltgrpcapacity'])
    thinner_c = str(output_obj['cleat']['thinner'])
    # gap = '20'

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Header of the pdf fetched from dialogbox
    rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%')

    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoCleat.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center" ') + row[2] + t('/td')
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
    row = [0, 'Client']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
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

    if status == 'True':
        row = [1, "Cleat Angle", "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [1, "Cleat Angle", "<p align=left style=color:red><b>Fail</b></p>"]
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

    if connectivity == "Beam-Beam":
        row = [1, "Secondary Beam", "Bolted"]
    else:
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

    if connectivity == "Beam-Beam":
        row = [1, "Primary Beam", "Bolted"]
    else:
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

    row = [2, "Hole", bolt_hole_type]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    if connectivity == "Beam-Beam":
        row = [1, "Bolts on Secondary Beam", " "]
    else:
        row = [1, "Bolts on Beam", " "]
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
    row = [2, "Diameter (mm)", bolt_dia]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolt Numbers", "3"]
    row = [2, "Bolt Numbers", no_of_bolts_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Columns (Vertical Lines)", "1 "]
    row = [2, "Columns (Vertical Lines)", no_of_col_b]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolts Per Column", "3"]
    row = [2, "Bolts Per Column", no_of_rows_b]
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

    if connectivity == "Beam-Beam":
        row = [1, "Bolts on Primary Beam", " "]
    else:
        row = [1, "Bolts on Column", " "]
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
    row = [2, "Diameter (mm)", bolt_dia]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolt Numbers", "3"]
    row = [2, "Bolt Numbers", no_of_bolts_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Columns (Vertical Lines)", "1 "]
    row = [2, "Columns (Vertical Lines)", no_of_col_c]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    # row = [2, "Bolts Per Column", "3"]
    row = [2, "Bolts Per Column", no_of_rows_c]
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
    if connectivity == "Beam-Beam":
        row = [1, "Beam-Beam Clearance (mm)", gap]
    else:
        row = [1, "Column-Beam Clearance (mm)", gap]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

    # *************************************************************************************************************************
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # Header of the pdf fetched from dialogbox
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoCleat.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
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
    row = [0, 'Client']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')

    rstr += t('hr')
    rstr += t('/hr')

    # *************************************************************************************************************************
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
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

    # row = [1, "Hole Clearance (mm)", bolt_hole_clrnce]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + row[2] + t('/td')
    # rstr += t('/tr')

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

    row = [1, "Minimum Edge-End Distance", min_edgend_dist + " times the hole diamter"]
    rstr += t('tr')
    rstr += t('td clospan="2" class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + row[2] + t('/td')
    rstr += t('/tr')

    if connectivity == "Beam-Beam":
        row = [1, "Gap between primary & secondary beam (mm)", gap]
    else:
        row = [1, "Gap between beam & column (mm)", gap]
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

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # *************************************************************************************************************************
    # Header of the pdf fetched from dialogbox
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoCleat.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center" ') + row[2] + t('/td')
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
    row = [0, 'Client']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')

    rstr += t('hr')
    #     rstr += t('p> &nbsp</p')
    #     rstr += t('hr')
    #     rstr += t('/hr')
    rstr += t('/hr')

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
    n_e = str(2)
    # row =[0,"Bolt shear capacity (kN)"," ","<i>V</i><sub>dsb</sub> = ((800*0.6123*20*20)/(&#8730;3*1.25*1000) = 90.53 <br> [cl. 10.3.3]"]

    if bolt_type == "Friction Grip Bolt":
        row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsf</sub> = ((" + slip_factor + "*" + n_e + "*" + k_h + "*" + F_0 +
               ")/(1.25)) = " + shear_capacity_b + "<br> [cl. 10.4.3]", ""]
    else:
        row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsb</sub> = ((2*" + bolt_fu + "*" + const + "*" + bolt_dia + "*" + bolt_dia +
               ")/(&#8730;3*1.25*1000)) = " + shear_capacity_b + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if bolt_type == "Friction Grip Bolt":
        row = [0, "Bolt bearing capaciy (kN)", "", "N/A", " "]
    else:
        row = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + thinner_b + "*" + bolt_fu +
        ")/(1.25*1000)  = " + boltbearingcapacity_b + "<br> [cl. 10.3.4]", ""]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bearing capacity of beam web (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if bolt_type ==  "Friction Grip Bolt":
        row = [0, "Bearing capacity of beam web (kN)", "", "N/A", ""]
    else:
        row = [0, "Bearing capacity of beam web (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + beam_tw + "*" + beam_fu +
               ")/(1.25*1000)  = " + bearingcapacitybeam_b + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bearing capacity of cleat (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"

    if bolt_type == "Friction Grip Bolt":
        row = [0, "Bearing capacity of cleat (kN)", "", "N/A", " "]
    else:
        row = [0, "Bearing capacity of cleat (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + cleat_thk + "*" + beam_fu +
           ")/(1.25*1000)  = " + bearingcapacitycleat_b + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if bolt_type == 'Friction Grip Bolt':
        row = [0, "Bearing capacity (kN)", "", "N/A", " "]
    else:
        bearcapacity = str(min(float(boltbearingcapacity_b), float(bearingcapacitybeam_b), float(bearingcapacitycleat_b)))
        row = [0, "Bearing capacity (kN)", "", "Min (" + boltbearingcapacity_b + ", " + bearingcapacitybeam_b + ", " + bearingcapacitycleat_b + ") = " +
           bearcapacity, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    if bolt_type == 'Friction Grip Bolt':
        row = [0, "Bolt capacity (kN)", "", shear_capacity_b ,""]
    else:
        row = [0, "Bolt capacity (kN)", "", "Min (" + shear_capacity_b + ", " + bearcapacity + ") = " + bolt_capacity_b, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Critical Bolt Shear (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    if float(critboltshear_b) > float(bolt_capacity_b):
        row = [0, "Critical bolt shear (kN)", "&#8804; " + bolt_capacity_b, critboltshear_b,
               "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Critical bolt shear (kN)", "&#8804; " + bolt_capacity_b, critboltshear_b, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
    #     bolts = str(round(float(shear_load)/float(bolt_capacity_b),1))
    #     row =[0,"No. of bolts", shear_load + "/" + bolt_capacity_b + " = " + bolts, no_of_bolts_b, " <p align=left style=color:green><b>Pass</b></p>"]
    row = [0, "No. of bolts", "", no_of_bolts_b, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No.of column(s)", " &#8804; 2", no_of_col_b, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts per column"," ","3"]
    row = [0, "No. of bolts per column", " ", no_of_rows_b, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    min_pitch = str(int(2.5 * float(bolt_dia)))
    max_pitch = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    if int(pitch_b) < int(min_pitch) or int(pitch_b) >  int(max_pitch):
        row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + min_pitch + ",  &#8804; Min(32*" + beam_tw + ", 300) = " + max_pitch +
           "<br> [cl. 10.2.2]", pitch_b, "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Bolt pitch (mm)",
               " &#8805; 2.5* " + bolt_dia + " = " + min_pitch + ",  &#8804; Min(32*" + beam_tw + ", 300) = " + max_pitch +
               "<br> [cl. 10.2.2]", pitch_b, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]

    min_gauge = str(int(2.5 * float(bolt_dia)))
    max_gauge = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    if gauge_b >= min_gauge or gauge_b <= max_gauge:
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge_b, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Bolt gauge (mm)", " &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge_b, "<p align=left style=color:red><b>Fail</b></p>"]
    if no_of_col_b >= str(2):
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge_b, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge_b, "<p align=left style=color:green><b>" "</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"End distance (mm)","&#8805;1.7* 22 = 37.4,&#8804;12*8.9 = 106.9 <br> [cl. 10.2.4]","50"]
    min_end = str(int(float(min_edgend_dist) * float(dia_hole)))
    max_end = str(12 * float(beam_tw))
    if int(end_b) >= int(min_end) or int(end_b) <=  int(max_end):
        row = [0, "End distance (mm)", " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + min_end + ", &#8804; 12*" + beam_tw + " = " + max_end + " <br> [cl. 10.2.4]", end_b,
           "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "End distance (mm)",
               " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + min_end + ", &#8804; 12*" + beam_tw + " = " + max_end + " <br> [cl. 10.2.4]",
               end_b,
               "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Edge distance (mm)","&#8805; 1.7* 22 = 37.4,&#8804;12*8.9 = 106.9<br> [cl. 10.2.4]","50"," <p align=right style=color:green><b>Pass</b></p>"]
    min_edge = str(int(float(min_edgend_dist) * float(dia_hole)))
    max_edge = str(12 * float(beam_tw))
    if int(edge_b) >= int(min_edge) or int(edge_b) <= int(max_edge) :
        row = [0, "Edge distance (mm)", " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + min_edge + ", &#8804; 12*" + beam_tw + " = " + max_edge + "<br> [cl. 10.2.4]", edge_b,
           " <p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Edge distance (mm)",
               " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + min_edge + ", &#8804; 12*" + beam_tw + " = " + max_edge + "<br> [cl. 10.2.4]",
               edge_b,
               " <p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    if float(blockshear_b) < float(shear_load):
        row = [0, "Block shear capacity (kN)", " &#8805; " + shear_load,"<i>V</i><sub>db</sub> = " + blockshear_b + "<br> [cl. 6.4.1]",
               "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Block shear capacity (kN)", " &#8805; " + shear_load, "<i>V</i><sub>db</sub> = " + blockshear_b + "<br> [cl. 6.4.1]",
           "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    if connectivity == "Beam-Beam":
        max_len = str(float(beam_D) - float(column_R1) - float(column_f_t) - float(beam_f_t) - float(beam_R1) - 5)
        str_max_len = "-" + beam_f_t + "-" + beam_R1 + "-" + column_f_t + "-" + column_R1 + "- 5"
    else:
        max_len = str(float(beam_D) - 2 * (float(beam_f_t) + float(beam_R1) + 5 ))
        str_max_len = "-" + beam_f_t + "-" + beam_R1 + "-" + beam_f_t + "-" + beam_R1 + "- 10"

    min_len = str(0.6 * float(beam_D))
    if float(height_c) < float(min_len) or float(height_c) > float(max_len) :
        row = [0, "Cleat height (mm)", "&#8805; 0.6*" + beam_D + "=" + min_len + ", &#8804; " + beam_D + str_max_len + "=" + max_len +
               "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", height_c,
               " <p align=left style=color:red><b>Fail</b></p>", "300", ""]
    else:
        row = [0, "Cleat height (mm)", "&#8805; 0.6*" + beam_D + "=" + min_len + ", &#8804; " + beam_D + str_max_len + "=" + max_len +
               "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", height_c, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"cleat moment capacity (kNm)","(2*90.5*100<sup>2</sup>)/100 = 18.1","<i>M</i><sub>d</sub> =1.2*250*<i>Z</i> = 40.9 <br>[cl. 8.2.1.2]","<p align=right style=color:green><b>Pass</b></p>"]
    #     z = math.pow(float(cleat_length),2)* (float(cleat_thk)/(6 *1.1* 1000000))
    #     momentCapacity = str(round(1.2 * float(web_plate_fy)* z,2))
    if float(moment_capacity_b) < float(moment_demand_b) :
        row = [0, "Cleat moment capacity (kNm)","(2*" + shear_capacity_b + "*" + pitch_b + "<sup>2</sup>)/(" + pitch_b + "*1000) = " + moment_demand_b,
               "<i>M</i><sub>d</sub> = (1.2*" + cleat_fy + "*<i>Z</i>)/(1000*1.1) = " + moment_capacity_b + "<br>[cl. 8.2.1.2]",
               "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Cleat moment capacity (kNm)", "(2*" + shear_capacity_b + "*" + pitch_b + "<sup>2</sup>)/(" + pitch_b + "*1000) = " + moment_demand_b,
           "<i>M</i><sub>d</sub> = (1.2*" + cleat_fy + "*<i>Z</i>)/(1000*1.1) = " + moment_capacity_b + "<br>[cl. 8.2.1.2]",
           "<p align=left style=color:green><b>Pass</b></p>"]
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
    row = [0, '<object type= "image/PNG" data= "cmpylogoCleat.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center" ') + row[2] + t('/td')
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
    row = [0, 'Client']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
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
    n_e = str(1)
    # row =[0,"Bolt shear capacity (kN)"," ","<i>V</i><sub>dsb</sub> = ((800*0.6123*20*20)/(&#8730;3*1.25*1000) = 90.53 <br> [cl. 10.3.3]"]
    if bolt_type == "Friction Grip Bolt":
        row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsf</sub> = ((" + slip_factor + "*" + n_e + "*" + k_h + "*" +
           F_0 + ")/(1.25)) = " + shear_capacity_c + "<br> [cl. 10.4.3]", ""]
    else:
        row = [0, "Bolt shear capacity (kN)", " ",
               "<i>V</i><sub>dsb</sub> = ((" + bolt_fu + "*" + const + "*" + bolt_dia + "*" +
               bolt_dia + ")/(&#8730;3*1.25*1000)) = " + shear_capacity_c + "<br> [cl. 10.3.3]", ""]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if bolt_type == 'Friction Grip Bolt':
        row = [0, "Bolt bearing capaciy (kN)", "", "N/A", " "]
    else:
        row = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + thinner_c + "*" +
               bolt_fu + ")/(1.25*1000)  = " + boltbearingcapacity_c + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    thk = 0.0
    str_con = " "
    if connectivity == "Column falange-Beam web":
        thk = str(column_f_t)
        str_con = "Bearing capacity of column flange (kN)"
    elif connectivity == "Column web-Beam web":
        thk = str(column_w_t)
        str_con = "Bearing capacity of column flange (kN)"
    else:
        thk = str(column_w_t)
        str_con = "Bearing capacity of beam web (kN)"

    rstr += t('tr')
    # row =[0,"Bearing capacity of beam web (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if bolt_type == 'Friction Grip Bolt':
        row = [0, "Bolt bearing capaciy (kN)", "", "N/A", " "]
    else:
        row = [0, str_con, "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + thk + "*" + beam_fu + ")/(1.25*1000)  = " + bearingcapacitycolumn_c +
               "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')
    rstr += t('tr')

    # row =[0,"Bearing capacity of cleat (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]

    if bolt_type == 'Friction Grip Bolt':
        row = [0, "Bolt bearing capaciy (kN)", "", "N/A", " "]
    else:
        row = [0, "Bearing capacity of cleat (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + cleat_thk + "*" + beam_fu +
               ")/(1.25*1000)  = " + bearingcapacitycleat_c + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    if bolt_type == 'Friction Grip Bolt':
        row = [0, "Bolt bearing capaciy (kN)", "", "N/A", " "]
    else:
        bearingcapacitycleat_c = str(min(float(boltbearingcapacity_c), float(bearingcapacitycolumn_c), float(bearingcapacitycleat_c)))
        row = [0, "Bearing capacity (kN)", "", "Min (" + boltbearingcapacity_c + ", " + bearingcapacitycolumn_c + ", " + bearingcapacitycleat_c + ") = " +
               bearingcapacitycleat_c, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]

    if bolt_type == 'Friction Grip Bolt':
        row = [0, "Bolt capacity (kN)", "",shear_capacity_c , ""]
    else:
        row = [0, "Bolt capacity (kN)", "", "Min (" + shear_capacity_c + ", " + bearingcapacitycleat_c + ") = " + bolt_capacity_c, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Critical Bolt Shear (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    if float(critboltshear_c) > float(bolt_capacity_c):
        row = [0, "Critical bolt shear (kN)", "&#8804; " + bolt_capacity_c, critboltshear_c,"<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Critical bolt shear (kN)", "&#8804; " + bolt_capacity_c, critboltshear_c, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    #     rstr += t('tr')
    #     #row =[0,"Critical Bolt Shear (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    #     row =[0,"Critical Bolt Shear (kN)","&#8804;" + bolt_capacity_c , critboltshear_c , "<p align=right style=color:green><b>Pass</b></p>"]
    #     rstr += t('td class="header2_col1"') + space(row[0]) + row[1] + t('/td')
    #     rstr += t('td class="header2"') + space(row[0]) + row[2] + t('/td')
    #     rstr += t('td class="header2"') + space(row[0]) + row[3] + t('/td')
    #     rstr += t('td class="header2"') + space(row[0]) + row[4] + t('/td')
    #     rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
    #     bolts = str(round(float(shear_load)/float(bolt_capacity_c),1))
    #     row =[0,"No. of bolts", shear_load + "/" + bolt_capacity_c + " = " + bolts, no_of_bolts_c, " <p align=left style=color:green><b>Pass</b></p>"]
    row = [0, "No. of bolts", "", no_of_bolts_c, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No.of column(s) per angle", " &#8804; 2", no_of_col_c, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts per column"," ","3"]
    row = [0, "No. of bolts per column per angle", " ", no_of_rows_c, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    min_pitch = str(int(2.5 * float(bolt_dia)))
    max_pitch = str(300) if 32 * float(thinner_c) > 300 else str(int(math.ceil(32 * float(thinner_c))))
    if int(pitch_c) < int(min_pitch) or int(pitch_c) > int(max_pitch):
        row = [0, "Bolt pitch (mm)",
           " &#8805; 2.5* " + bolt_dia + " = " + min_pitch + ",  &#8804; Min(32*" + thinner_c + ", 300) = " + max_pitch +
           "<br> [cl. 10.2.2]", pitch_c, "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Bolt pitch (mm)", " &#8805; 2.5* " + bolt_dia + " = " + min_pitch + ",  &#8804; Min(32*" + thinner_c + ", 300) = " + max_pitch +
           "<br> [cl. 10.2.2]", pitch_c, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    min_gauge = str(int(2.5 * float(bolt_dia)))
    max_gauge = str(300) if 32 * float(thinner_c) > 300 else str(int(math.ceil(32 * float(thinner_c))))
    if gauge_c >=min_gauge or gauge_c <= max_gauge:
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + thinner_c + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge_c, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Bolt gauge (mm)", " &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + thinner_c + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge_c, "<p align=left style=color:red><b>Fail</b></p>"]
    if no_of_col_c >= str(2):
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + thinner_c + ", 300) = " + max_gauge +
                " <br> [cl. 10.2.2]", gauge_c, "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "Bolt gauge (mm)"," &#8805; 2.5*" + bolt_dia + " = " + min_gauge + ", &#8804; Min(32*" + thinner_c + ", 300) = " + max_gauge +
               " <br> [cl. 10.2.2]", gauge_c, "<p align=left style=color:green><b>" "</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"End distance (mm)","&#8805;1.7* 22 = 37.4,&#8804;12*8.9 = 106.9 <br> [cl. 10.2.4]","50"]
    min_end = str(int(float(min_edgend_dist) * float(dia_hole)))
    max_end = str(12 * float(thinner_c))
    if float(end_c) >= int(min_end) or float(end_c) <= int(max_end):
        row = [0, "End distance (mm)",
               " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + min_end + ", &#8804; 12*" + thinner_c + " = " + max_end + " <br> [cl. 10.2.4]",
               end_c,
               "<p align=left style=color:green><b>Pass</b></p>"]
    else:
        row = [0, "End distance (mm)", " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + min_end + ", &#8804; 12*" + thinner_c + " = " + max_end + " <br> [cl. 10.2.4]", end_c,
           "<p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Edge distance (mm)","&#8805; 1.7* 22 = 37.4,&#8804;12*8.9 = 106.9<br> [cl. 10.2.4]","50"," <p align=right style=color:green><b>Pass</b></p>"]
    min_edge = str(int(float(min_edgend_dist) * float(dia_hole)))
    max_edge = str(12 * float(thinner_c))
    if edge_c >= min_edge or edge_c <= max_edge :
        row = [0, "Edge distance (mm)",
           " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + min_edge + ", &#8804;12*" + thinner_c + " = " + max_edge + "<br> [cl. 10.2.4]",
           edge_c,
           " <p align=left style=color:green><b>Pass</b></p>"]

    else:
        row = [0, "Edge distance (mm)", " &#8805; " + min_edgend_dist + "*" + dia_hole + " = " + min_edge + ", &#8804;12*" + thinner_c + " = " + max_edge + "<br> [cl. 10.2.4]", edge_c,
           " <p align=left style=color:red><b>Fail</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    if float(blockshear_c) < float(shear_load):
        row = [0, "Block shear capacity (kN)", " &#8805;" + shear_load,"<i>V</i><sub>db</sub> = " + blockshear_c + "<br> [cl. 6.4.1]",
               "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Block shear capacity (kN)", " &#8805;" + shear_load, "<i>V</i><sub>db</sub> = " + blockshear_c + "<br> [cl. 6.4.1]",
           "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    if connectivity == "Beam-Beam":
        max_len = str(float(beam_D) - float(column_R1) - float(column_f_t) - float(beam_f_t) - float(beam_R1) - 5)
        str_max_len = "-" + beam_f_t + "-" + beam_R1 + "-" + column_f_t + "-" + column_R1 + "- 5"
    else:
        max_len = str(float(beam_D) - 2 * (float(beam_f_t) + float(beam_R1) + 5))
        str_max_len = "2*(" + beam_f_t + "+" + beam_R1 + "+5)"
    min_len = str(0.6 * float(beam_D))

    if float(height_c) < float(min_len) or float(height_c) > float(max_len):
        row = [0, "Cleat height (mm)","&#8805; 0.6*" + beam_D + "=" + min_len + ", &#8804; " + beam_D + str_max_len + "=" + max_len +
               "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", height_c,
               " <p align=left style=color:red><b>Fail</b></p>", "300", ""]
    else:
        row = [0, "Cleat height (mm)", "&#8805; 0.6*" + beam_D + "=" + min_len + ", &#8804; " + beam_D + str_max_len + "=" + max_len +
           "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", height_c, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"cleat moment capacity (kNm)","(2*90.5*100<sup>2</sup>)/100 = 18.1","<i>M</i><sub>d</sub> =1.2*250*<i>Z</i> = 40.9 <br>[cl. 8.2.1.2]","<p align=right style=color:green><b>Pass</b></p>"]
    #     z = math.pow(float(cleat_length),2)* (float(cleat_thk)/(6 *1.1* 1000000))
    #     momentCapacity = str(round(1.2 * float(beam_fy)* z/1.1,2))
    if float(moment_capacity_c) < float(moment_demand_c):
        row = [0, "Cleat moment capacity (kNm)", "(2*" + shear_capacity_c + "*" + pitch_c + "<sup>2</sup>)/(" + pitch_c + "*1000) = " + moment_demand_c,
           "<i>M</i><sub>d</sub> = (1.2*" + cleat_fy + "*<i>Z</i>)/(1000*1.1) = " + moment_capacity_c + "<br>[cl. 8.2.1.2]",
           "<p align=left style=color:red><b>Fail</b></p>"]
    else:
        row = [0, "Cleat moment capacity (kNm)",
               "(2*" + shear_capacity_c + "*" + pitch_c + "<sup>2</sup>)/(" + pitch_c + "*1000) = " + moment_demand_c,
               "<i>M</i><sub>d</sub> = (1.2*" + cleat_fy + "*<i>Z</i>)/(1000*1.1) = " + moment_capacity_c + "<br>[cl. 8.2.1.2]",
               "<p align=left style=color:green><b>Pass</b></p>"]

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
    # Header of the pdf fetched from dialogbox
    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoCleat.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center" ') + row[2] + t('/td')
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
    row = [0, 'Client']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
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
    # Diagram

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')

    row = [0, "Views", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="detail"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class=" viewtbl "') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    png = folder + "/images_html/3D_Model.png"
    datapng = '<object type="image/PNG" data= %s width ="400"></object">' % png

    side = folder + "/images_html/cleatSide.png"
    dataside = '<object type="image/PNG" data= %s width ="400"></object>' % side

    top = folder + "/images_html/cleatTop.png"
    datatop = '<object type="image/PNG" data= %s width ="400"></object>' % top

    front = folder + "/images_html/cleatFront.png"
    datafront = '<object type="image/PNG" data= %s width ="450"></object>' % front

    if status == 'True':
        row = [0, datapng, datatop]
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
    row = [0, '<object type= "image/PNG" data= "cmpylogoCleat.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
    rstr += t('td colspan="2" align= "center" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "center" ') + row[2] + t('/td')
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
    row = [0, 'Client']
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
    row = [0, client]
    rstr += t('td class= "detail"') + space(row[0]) + row[1] + t('/td')
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
# save_html(outObj, uiobj, dict_beam_data, dict_col_data)


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# COnverting HTML to PDF
# pdfkit.from_file('output/reshma.html','output/reshmaReport.pdf')
# print "PDF generated"
