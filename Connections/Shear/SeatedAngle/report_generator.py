'''
Created on Oct 21, 2016

@author: Jayant Patil
'''
import time
import math
from PyQt4.QtCore import QString


def save_html(output_object, input_object, dict_beam_data, dict_col_data, report_summary, file_name, folder, base,
              base_front, base_top, base_side):
    """Create and save html report for Seated angle connection.

    Args:
        output_object (dict): Calculated output parameters
        input_object (dict): User input parameters
        dict_beam_data (dict): beam section properties
        dict_col_data (dict): column section properties
        report_summary (dict): User input parameters for design report
        file_name (string): Name of design report file
        folder (path): Location of folder to save design report
        base (path): Location of folder to save design report dependencies
        base_front (string): Location to save design report dependency (front view image)
        base_top  (string): Location to save design report dependency (top view image)
        base_side (string): Location to save design report dependency (side view image)

    Returns:
        None
        """
    file_name = (file_name)
    myfile = open(file_name, "w")
    myfile.write(t('! DOCTYPE html') + nl())
    myfile.write(t('html') + nl())
    myfile.write(t('head') + nl())
    myfile.write(t('link type="text/css" rel="stylesheet" ') + nl())

    myfile.write(html_space(4) + t('style'))
    myfile.write('table{width= 100%; border-collapse:collapse; border:1px solid black collapse}')
    myfile.write('th,td {padding:3px}' + nl())
    myfile.write(html_space(
        8) + 'td.detail{background-color:#D5DF93; font-size:20; font-family:Helvetica, Arial,'
             ' Sans Serif; font-weight:bold}' + nl())
    myfile.write(
        html_space(8) + 'td.detail1{font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
    myfile.write(html_space(8) + 'td.detail2{font-size:20; font-family:Helvetica, Arial, Sans Serif}' + nl())
    myfile.write(html_space(
        8) + 'td.header0{background-color:#8fac3a; font-size:20; font-family:Helvetica, Arial,'
             ' Sans Serif; font-weight:bold}' + nl())
    myfile.write(html_space(
        8) + 'td.header1{background-color:#E6E6E6; font-size:20; font-family:Helvetica, Arial,'
             ' Sans Serif; font-weight:bold}' + nl())
    myfile.write(html_space(8) + 'td.header2{font-size:20; width:50%}' + nl())
    myfile.write(html_space(4) + t('/style') + nl())

    myfile.write(t('/head') + nl())
    myfile.write(t('body') + nl())

    # Project summary
    company_name = str(report_summary["ProfileSummary"]['CompanyName'])
    companylogo = str(report_summary["ProfileSummary"]['CompanyLogo'])

    group_team_name = str(report_summary["ProfileSummary"]['Group/TeamName'])
    designer = str(report_summary["ProfileSummary"]['Designer'])
    project_title = str(report_summary['ProjectTitle'])
    subtitle = str(report_summary['Subtitle'])
    jobnumber = str(report_summary['JobNumber'])
    method = str(report_summary['Method'])
    additional_comments = str(report_summary['AdditionalComments'])

    # Seated angle design parameters
    connectivity = str(input_object['Member']['Connectivity'])
    shear_load = str(input_object['Load']['ShearForce (kN)'])
    column_sec = str(input_object['Member']['ColumnSection'])
    beam_sec = str(input_object['Member']['BeamSection'])
    plate_thk = str(input_object['Plate']['Thickness (mm)'])
    boltType = str(input_object['Bolt']['Type'])
    boltGrade = str(input_object['Bolt']['Grade'])
    bolt_diameter = str(input_object['Bolt']['Diameter (mm)'])
    weld_thickness= str(input_object['Weld']['Size (mm)'])

    beam_depth = str(int(round(output_object['Plate']['beamdepth'], 1)))
    beam_flange_thickness = str(int(round(output_object['Plate']['beamflangethk'], 1)))
    beam_root_radius = str(int(round(output_object['Plate']['beamrootradius'], 1)))
    plate_thickness = str(int(round(output_object['Plate']['platethk'], 1)))
    block_shear = str(int(round(output_object['Plate']['blockshear'], 1)))
    col_flange_thickness = str(int(round(output_object['Plate']["colflangethk"], 1)))
    col_root_radius = str(int(round(output_object['Plate']['colrootradius'])))

    plate_width = str(int(round(output_object['Plate']['width'], 1)))
    plate_length = str(int(round(output_object['Plate']['height'], 1)))
    weld_size = str(int(round(output_object['Weld']['thickness'], 1)))

    plate_dimension = plate_length + 'X' + plate_width + 'X' + plate_thk
    number_of_bolts = str(output_object['Bolt']['numofbolts'])
    number_of_rows = str(output_object['Bolt']['numofrow'])
    number_of_cols = str(output_object['Bolt']['numofcol'])
    edge = str(int(round(output_object['Bolt']['edge'], 1)))
    gauge = str(int(round(output_object['Bolt']['gauge'], 1)))
    pitch = str(int(round(output_object['Bolt']['pitch'], 1)))
    end = str(int(round(output_object['Bolt']['enddist'], 1)))
    weld_strength = str(round(float(output_object['Weld']['weldstrength'] / 1000), 3))
    moment_demand = str(output_object['Plate']['externalmoment'])
    gap = '20'
    # TODO replace hardcoded gap value
    beam_tw = str(float(dict_beam_data[QString("tw")]))

    bolt_fu = str(output_object['Bolt']['bolt_fu'])
    bolt_dia = str(output_object['Bolt']['bolt_dia'])
    kb = str(output_object['Bolt']['k_b'])
    beam_w_t = str(output_object['Bolt']['beam_w_t'])
    web_plate_t = str(output_object['Bolt']['web_plate_t'])
    beam_fu = str(output_object['Bolt']['beam_fu'])
    dia_hole = str(output_object['Bolt']['dia_hole'])
    web_plate_fy = str(output_object['Plate']['web_plate_fy'])
    weld_fu = str(output_object['Weld']['weld_fu'])
    weld_l = str(output_object['Weld']['effectiveWeldlength'])
    shear_capacity = str(round(output_object['Bolt']['shearCapacity'], 3))
    bearing_capacity = str(round(output_object['Bolt']['bearingCapacity'], 4))
    moment_demand = str(output_object['Plate']['externalmoment'])

    # Header of the pdf fetched from dialog box
    rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%') + nl()
    rstr += t('tr') + nl()
    row = [0, '<object type= "image/PNG" data= "css/cmpylogoFin.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>'' &nbsp'
           '<object type= "image/PNG" data= "css/Osdag_header.png" height=60 ''&nbsp></object>']
    rstr += html_space(1) + t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += html_space(1) + t('td colspan="2" align= "right"') + row[2] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Company Name']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, company_name]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()

    row = [0, 'Project Title']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, project_title]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, group_team_name]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Subtitle']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, subtitle]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Designer']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, designer]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Job Number']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, jobnumber]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Date']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Method']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, method]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr')
    rstr += t('/table') + nl() + " " + nl()

    rstr += t('hr')
    rstr += t('/hr') + nl() + " " + nl()

    # TODO delete html-code-generating lines that have been commented out
    # Design conclusion
    rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100% ') + nl()

    # row = [0, 'Design Conclusion', "IS800:2007/Limit state design"]
    # rstr += t('tr')
    # rstr += html_space(1) + t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')+nl()
    rstr += design_summary_row(0, "Design Conclusion", "header0", col_span="2")

    row = [1, "Finplate", "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('tr')
    rstr += html_space(1) + t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1"') + row[2] + t('/td') + nl()
    # rstr += t('td class="header1 safe"') + row[3] + t('/td')
    rstr += t('/tr')

    # row = [0, "Finplate", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(0, "Finplate", "header0", col_span="2")

    # row = [0, "Connection Properties", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(0, "Connection Properties", "detail", col_span="2")

    # row = [0, "Connection ", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(0, "Connection ", "detail1", col_span="2")

    # row = [1, "Connection Title", " Single Finplate"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Connection Title", "detail2", text_two=" Single Finplate")

    # row = [1, "Connection Type", "Shear Connection"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Connection Type", "detail2", text_two=" Shear Connection")

    # row = [0, "Connection Category ", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(0, "Connection Category", "detail1")

    # row = [1, "Connectivity", "Column Web Beam Web"]
    # row = [1, "Connectivity", connectivity]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Connectivity", "detail2", text_two=str(connectivity))

    # row = [1, "Beam Connection", "Bolted"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Beam Connection", "detail2", text_two="Bolted")

    # row = [1, "Column Connection", "Welded"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Column Connection", "detail2", text_two="Welded")

    # row = [0, "Loading (Factored Load) ", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(0, "Loading (Factored Load)", "detail1")

    # #row = [1, "Shear Force (kN)", "140"]
    # row = [1,"Shear Force (kN)", shear_load]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Shear Force (kN)", "detail2", text_two=str(shear_load))

    # row = [0, "Components ", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(0, "Components ", "detail1", col_span="2")

    # # row = [1, "Column Section", "ISSC 200"]
    # row = [1,"Column Section", column_sec]
    # rstr += t('tr')
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Column Section", "detail1", text_two=str(column_sec), text_two_css="detail2")

    # row = [2, "Material", "Fe "+beam_fu]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(beam_fu))

    # #row = [1, "Beam Section", "ISMB 400"]
    # row = [1,"Beam Section",beam_sec]
    # rstr += t('tr')
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Beam Section", "detail1", text_two=str(beam_sec), text_two_css="detail2")

    # row = [2, "Material", "Fe "+beam_fu]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(beam_fu))

    # row = [2, "Hole", "STD"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    # TODO Hole type - parameterise
    rstr += design_summary_row(2, "Hole", "detail2", text_two="STD")

    # #row = [1, "Plate Section ", "PLT 300X10X100 "]
    # row = [1, "Plate Section",plate_dimension]
    # rstr += t('tr')
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Plate Section", "detail1", text_two=plate_dimension, text_two_css="detail2")

    # # row = [2, "Thickness (mm)", "10"]
    # row = [2, "Thickness (mm)", plate_thk]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Thickness (mm)", "detail2", text_two=plate_thk)

    # # row = [2, "Width (mm)", "10"]
    # row = [2, "Width (mm)", plate_width]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Width (mm)", "detail2", text_two=plate_width)

    # # row = [2, "Depth (mm)", "300"]
    # row = [2, "Depth (mm)", plate_length]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Depth (mm)", "detail2", text_two=plate_length)

    # row = [2, "Hole", "STD"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    # TODO Hole type - parameterise
    rstr += design_summary_row(2, "Hole", "detail2", text_two="STD")

    # row = [1, "Weld ", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Weld", "detail1", col_span="2")

    # row = [2, "Type", "Double Fillet"]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Type", "detail2", text_two="Double Fillet")

    # # row = [2, "Size (mm)", "6"]
    # row = [2, "Size (mm)", weld_size]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Size (mm)", "detail2", text_two=weld_size)

    # row = [1, "Bolts ", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Bolts", "detail1", col_span="2")

    # # row = [2, "Type", "HSFG"]
    # row = [2, "Type", boltType]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Type", "detail2", text_two=boltType)

    # # row = [2, "Grade", "8.8"]
    # row = [2, "Grade", boltGrade]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Grade", "detail2", text_two=boltGrade)

    # # row = [2, "Diameter (mm)", "20"]
    # row = [2, "Diameter (mm)", bolt_diameter]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Diameter (mm)", "detail2", text_two=bolt_diameter)

    # # row = [2, "Bolt Numbers", "3"]
    # row = [2, "Bolt Numbers", number_of_bolts]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Bolt Numbers", "detail2", text_two=number_of_bolts)

    # # row = [2, "Columns (Vertical Lines)", "1 "]
    # row = [2, "Columns (Vertical Lines)", number_of_cols]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Columns (Vertical Lines)", "detail2", text_two=number_of_cols)

    # # row = [2, "Bolts Per Column", "3"]
    # row = [2, "Bolts Per Column", number_of_rows]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Bolts Per Columne", "detail2", text_two=number_of_rows)

    # # row = [2, "Gauge (mm)", "0"]
    # row = [2, "Gauge (mm)", gauge]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Gauge (mm)", "detail2", text_two=gauge)

    # # row = [2, "Pitch (mm)", "100"]
    # row = [2, "Pitch (mm)", pitch]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Pitch (mm)", "detail2", text_two=pitch)

    # # row = [2, "End Distance (mm)", "50"]
    # row = [2, "End Distance (mm)", end]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2"') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "End Distance (mm)", "detail2", text_two=end)

    # # row = [2, "Edge Distance (mm)", "50"]
    # row = [2, "Edge Distance (mm)", edge]
    # rstr += t('tr')
    # rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(2, "Edge Distance (mm)", "detail2", text_two=edge)

    # row = [0, "Assembly ", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(0, "Assembly", "detail1", col_span="2")

    # # row = [1, "Column-Beam Clearance (mm)", "20"]
    # row = [1, "Column-Beam Clearance (mm)", gap]
    # rstr += t('tr')
    # rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('td class="detail2 "') + row[2] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(1, "Column-Beam Clearance (mm)", "detail1", text_two=gap, text_two_css="detail2")

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

    # --------------------------------------------------------------------------------------------------------
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "css/cmpylogoFin.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>'' &nbsp'
           '<object type= "image/PNG" data= "css/Osdag_header.png" height=60></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right"') + row[2] + t('/td')
    rstr += t('/tr' + nl())

    rstr += t('tr') + nl()
    row = [0, 'Company Name']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, company_name]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()

    row = [0, 'Project Title']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, project_title]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, group_team_name]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Subtitle']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, subtitle]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Designer']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, designer]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Job Number']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, jobnumber]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Date']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Method']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, method]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr')
    rstr += t('/table') + nl() + " " + nl()

    rstr += t('hr')
    rstr += t('/hr') + nl() + " " + nl()

    # -----------------------------------------------------------------------------------
    # DESIGN CHECK
    # TODO IMPORTANT Remove calculations from below lines of code

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
    row = [0, "Bolt shear capacity (kN)", " ",
           "<i>V</i><sub>dsb</sub> = (" + bolt_fu + "*" + const + "*" + bolt_dia + "*" + bolt_dia + ")/(&#8730;3*1.25*1000) = " + shear_capacity + "<br> [cl. 10.3.3]",
           ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, "Bolt bearing capacity (kN)", "",
           " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + beam_tw + "*" + beam_fu + ")/(1.25*1000)  = " + bearing_capacity + "<br> [cl. 10.3.4]",
           ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    boltCapacity = bearing_capacity if bearing_capacity < shear_capacity else shear_capacity
    row = [0, "Bolt capacity (kN)", "", "Min (" + shear_capacity + ", " + bearing_capacity + ") = " + boltCapacity, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
    bolts = str(round(float(shear_load) / float(boltCapacity), 1))
    row = [0, "No. of bolts", shear_load + "/" + boltCapacity + " = " + bolts, number_of_bolts,
           " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No.of column(s)","&#8804;2","1"]
    row = [0, "No.of column(s)", " &#8804; 2", number_of_cols, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts per column"," ","3"]
    row = [0, "No. of bolts per column", " ", number_of_rows, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    minPitch = str(int(2.5 * float(bolt_dia)))
    maxPitch = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    row = [0, "Bolt pitch (mm)",
           " &#8805; 2.5* " + bolt_dia + " = " + minPitch + ",  &#8804; Min(32*" + beam_tw + ", 300) = " + maxPitch + "<br> [cl. 10.2.2]",
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
    row = [0, "Bolt gauge (mm)",
           " &#8805; 2.5*" + bolt_dia + " = " + minGauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + maxGauge + " <br> [cl. 10.2.2]",
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
    row = [0, "End distance (mm)",
           " &#8805; 1.7*" + dia_hole + " = " + minEnd + ", &#8804; 12*" + beam_tw + " = " + maxEnd + " <br> [cl. 10.2.4]",
           end, "  <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Edge distance (mm)","&#8805; 1.7* 22 = 37.4,&#8804;12*8.9 = 106.9<br> [cl. 10.2.4]","50"," <p align=right style=color:green><b>Pass</b></p>"]
    minEdge = str(1.7 * float(dia_hole))
    maxEdge = str(12 * float(beam_tw))
    row = [0, "Edge distance (mm)",
           " &#8805; 1.7*" + dia_hole + " = " + minEdge + ", &#8804; 12*" + beam_tw + " = " + maxEdge + "<br> [cl. 10.2.4]",
           edge, " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Block shear capacity (kN)", " &#8805; " + shear_load, "<i>V</i><sub>db</sub> = " + block_shear + "<br>",
           "  <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Plate thickness (mm)","(5*140*1000)/(300*250)= 9.33","10"]
    minplate_thk = str(round(5 * float(shear_load) * 1000 / (float(plate_length) * float(web_plate_fy)), 2))
    row = [0, "Plate thickness (mm)",
           "(5*" + shear_load + "*1000)/(" + plate_length + "*" + web_plate_fy + ") = " + minplate_thk + "<br> [Owens and Cheal, 1989]",
           plate_thk, "  <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    #     if
    minEdge = str(0.6 * float(beam_depth))
    if connectivity == "Beam-Beam":
        maxEdge = str(float(beam_depth) - float(beam_flange_thickness) - float(beam_root_radius) - float(col_flange_thickness) - float(
            col_root_radius) - 5)
        maxedgestring = beam_depth + "-" + beam_flange_thickness + "-" + beam_root_radius + "-" + col_flange_thickness + "-" + col_root_radius + "- 5"
    else:
        maxEdge = str(float(beam_depth) - 2 * float(beam_flange_thickness) - 2 * float(beam_root_radius) - 10)
        maxedgestring = beam_depth + "-" + beam_flange_thickness + "-" + beam_root_radius + "-" + "10"

    row = [0, "Plate height (mm)",
           "&#8805; 0.6*" + beam_depth + "=" + minEdge + ", &#8804; " + maxedgestring + "=" + maxEdge + "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]",
           plate_length, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    #        #row =[0,"Plate height (mm)","",plate_length]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, "Plate width (mm)", "", "100", ""]
    # row =[0,"Plate width (mm)","",plate_width]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Plate moment capacity (kNm)","(2*90.5*100<sup>2</sup>)/100 = 18.1","<i>M</i><sub>d</sub> =1.2*250*<i>Z</i> = 40.9 <br>[cl. 8.2.1.2]","<p align=right style=color:green><b>Pass</b></p>"]
    z = math.pow(float(plate_length), 2) * (float(plate_thk) / (6 * 1.1 * 1000000))
    momentCapacity = str(round(1.2 * float(web_plate_fy) * z, 2))
    row = [0, "Plate moment capacity (kNm)",
           "(2*" + shear_capacity + "*" + pitch + "<sup>2</sup>)/(" + pitch + "*1000) = " + moment_demand,
           "<i>M</i><sub>d</sub> = (1.2*" + web_plate_fy + "*<i>Z</i>)/(1000*1.1) = " + momentCapacity + "<br>[cl. 8.2.1.2]",
           "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Effective weld length (mm)","","300 - 2*6 = 288"]
    effWeldLen = str(int(float(plate_length) - (2 * float(weld_thickness))))
    row = [0, "Effective weld length (mm)", "", plate_length + "-2*" + weld_thickness + " = " + effWeldLen, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Weld strength (kN/mm)","&#8730;[(18100*6)/(2*288)<sup>2</sup>]<sup>2</sup> + [140/(2*288)]<sup>2</sup> <br>=0.699","<i>f</i><sub>v</sub>=(0.7*6*410)/(&#8730;3*1.25)<br>= 0.795<br>[cl. 10.5.7]"," <p align=right style=color:green><b>Pass</b></p>"]
    a = float(2 * float(effWeldLen))
    b = 2 * math.pow((float(effWeldLen)), 2)
    x = (float(moment_demand) * 1000 * 6)
    resultant_shear = str(round(math.sqrt(math.pow((x / b), 2) + math.pow((float(shear_load) / a), 2)), 3))
    moment_demand_knmm = str(int(float(moment_demand) * 1000))
    row = [0, "Weld strength (kN/mm)",
           " &#8730;[(" + moment_demand_knmm + "*6)/(2*" + effWeldLen + "<sup>2</sup>)]<sup>2</sup> + [" + shear_load + "/(2*" + effWeldLen + ")]<sup>2</sup> <br>= " + resultant_shear,
           "<i>f</i><sub>v</sub>= (0.7*" + weld_size + "*" + weld_fu + ")/(&#8730;3*1.25)<br>= " + weld_strength + "<br>[cl. 10.5.7]",
           " <p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0, "Weld thickness (mm)", "(0.699*&#8730;3*1.25)/(0.7*410)=5.27"+
    # "<br>[cl. 10.5.7]","6", "<p align=right style=color:green><b>Pass</b></p>"]

    weld_thickness = str(round((float(resultant_shear) * 1000 * (math.sqrt(3) * 1.25)) / (0.7 * float(weld_fu)), 2))
    x = str((float(plate_thickness) * 0.8))
    maxweld = str(max(float(weld_thickness), float(x)))
    # maxweld = str(9) if str((float( plate_thickness)*0.8)) > str(9) else str(round((float(resultant_shear)
    #       * 1000*(math.sqrt(3) * 1.25))/(0.7 * float(weld_fu)),2))
    # maxWeld = str(9) if str(round((float(resultant_shear) * 1000*(math.sqrt(3) * 1.25))/(0.7
    #       * float(weld_fu)),2)) == 9 else str((float( plate_thickness)*0.8))
    # row =[0,"Weld thickness (mm)","Max(("+resultant_shear+"*&#8730;3*1.25)/(0.7*"+weld_fu+")"+",
    #       0.8*"+plate_thickness+") = "+ maxWeld + "<br>[cl. 10.5.7, Insdag Detailing Manual, 2002]",
    #       weld_size,"<p align=right style=color:green><b>Pass</b></p>"]
    row = [0, "Weld thickness (mm)",
           "Max((" + resultant_shear + "*1000*&#8730;3* 1.25)/(0.7 * " + weld_fu + ")" + "," + plate_thickness +
           "* 0.8" + ") = " + maxweld + "<br>[cl. 10.5.7, Insdag Detailing Manual, 2002]",
           weld_size, "<p align=left style=color:green><b>Pass</b></p>"]

    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')
    rstr += t('/h1')

    # TODO IMPORTANT Remove calculations from above lines of code

    # ------------------------------------------------------------------------------------------------
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "css/cmpylogoFin.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>'' &nbsp'
           '<object type= "image/PNG" data= "css/Osdag_header.png" height=60></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr') + nl()
    row = [0, 'Company Name']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, company_name]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()

    row = [0, 'Project Title']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, project_title]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, group_team_name]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Subtitle']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, subtitle]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Designer']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, designer]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Job Number']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, jobnumber]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Date']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Method']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, method]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr')
    rstr += t('/table') + nl() + " " + nl()

    rstr += t('hr')
    rstr += t('/hr') + nl() + " " + nl()

    # Connection images (views)
    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

    # row = [0, "Views", " "]
    # rstr += t('tr')
    # rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
    # rstr += t('/tr')
    rstr += design_summary_row(0, "Views", "detail", col_span="2")

    png = folder + "/css/" + base
    datapng = '<object type="image/PNG" data= %s width ="450"></object">' % png

    side = folder + "/css/" + base_side
    dataside = '<object type="image/svg+xml" data= %s width ="400"></object>' % side

    top = folder + "/css/" + base_top
    datatop = '<object type="image/svg+xml" data= %s width ="400"></object>' % top

    front = folder + "/css/" + base_front
    datafront = '<object type="image/svg+xml" data= %s width ="450"></object>' % front

    row = [0, datapng, datatop]
    rstr += t('tr')
    rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td  align="center" class=" header2"') + row[2] + t('/td')
    rstr += t('/tr' + nl())

    row = [0, dataside, datafront]
    rstr += t('tr')
    rstr += t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td align="center" class=" header2 "') + row[2] + t('/td')
    rstr += t('/tr' + nl())

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')
    rstr += t('/h1')

    # ------------------------------------------------------------------------------------------------
    rstr += t('table width= 100% border-collapse= "collapse" border="1px solid black collapse"')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "css/cmpylogoFin.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>'' &nbsp'
           '<object type= "image/PNG" data= "css/Osdag_header.png" height=60></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right"') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('tr') + nl()
    row = [0, 'Company Name']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, company_name]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()

    row = [0, 'Project Title']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, project_title]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr')

    rstr += t('tr')
    row = [0, 'Group/Team Name']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, group_team_name]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Subtitle']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, subtitle]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Designer']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, designer]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Job Number']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, jobnumber]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr') + nl()

    rstr += t('tr') + nl()
    row = [0, 'Date']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, time.strftime("%d /%m /%Y")]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, 'Method']
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    row = [0, method]
    rstr += html_space(1) + t('td class="detail" ') + space(row[0]) + row[1] + t('/td') + nl()
    rstr += t('/tr')
    rstr += t('/table') + nl() + " " + nl()

    rstr += t('hr')
    rstr += t('/hr') + nl() + " " + nl()

    rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
    rstr += t('''col width=30%''')
    rstr += t('''col width=70%''')

    rstr += t('tr')
    row = [0, "Additional Comments", additional_comments]
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
    return '<' + n + '>'


def w(n):
    return '{' + n + '}'


def quote(m):
    return '"' + m + '"'


def nl():
    return '\n'


def html_space(n):
    return " " * n


def design_summary_row(tab_spaces, text_one, text_one_css, **kwargs):
    """Create formatted html row entry.

    Args:
        tab_spaces (int): number of (tab) spaces
        text_one (str): Text entry
        text_one_css (str): Key pointing to table-data css format
        text_two (str): Text entry
        text_two_css (str): Key pointing to table-data css format

    Returns (str):
        Formatted line of html-code.

    """
    text_two = kwargs.get('text_two', " ")
    text_two_css = kwargs.get('text_two_css', text_one_css)
    col_span = kwargs.get('col_span', "1")

    row_string = t('tr') + nl()

    if col_span == "2":
        row_string = row_string + html_space(4) + t('td colspan=' + col_span + ' class="' + text_one_css + '"') + space(
            tab_spaces) + text_one + t('/td') + nl()
    else:
        row_string = row_string + html_space(4) + t('td class="' + text_one_css + '"') + space(tab_spaces) + text_one \
                     + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + text_two_css + '"') + text_two + t('/td') + nl()
    row_string = row_string + t('/tr') + nl()
    return row_string