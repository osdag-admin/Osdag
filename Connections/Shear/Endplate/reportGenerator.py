'''
Created on Dec 10, 2015
@author: deepa
'''
from __builtin__ import str
from PyQt4.QtCore import QString
import time
import math


# def save_html(outobj, uiobj, dictbeamdata, dictcolumndata, reportsummary, filename, folder, base, base_front, base_top, base_side):
def save_html(outobj, uiobj, dictbeamdata, dictcolumndata, reportsummary, filename, folder):

    print outobj
    fileName = (filename)
    myfile = open(fileName, "w")
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

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# EndPlate Main Data

    beam_tw = str(float(dictbeamdata[QString("tw")]))
    beam_f_t = str(float(dictbeamdata[QString("T")]))
    beam_d = str(float(dictbeamdata[QString("D")]))
    beam_R1 = str(float(dictbeamdata[QString("R1")]))
    beam_b = str(float(dictbeamdata[QString("B")]))

    column_w_t = str(float(dictcolumndata[QString("tw")]))
    column_f_t = str(float(dictcolumndata[QString("T")]))
    column_R1 = str(float(dictcolumndata[QString("R1")]))
    column_d = str(float(dictcolumndata[QString("D")]))
    column_b = str(float(dictcolumndata[QString("B")]))

###############################################################################################################################
    connectivity = str(uiobj['Member']['Connectivity'])
    shear_load = str(uiobj['Load']['ShearForce (kN)'])
    column_sec = str(uiobj['Member']['ColumSection'])
    beam_sec = str(uiobj['Member']['BeamSection'])
    plateThick = str(uiobj['Plate']['Thickness (mm)'])
    boltType = str(uiobj['Bolt']['Type'])
    boltGrade = str(uiobj['Bolt']['Grade'])
    boltDia = str(uiobj['Bolt']['Diameter (mm)'])
    beam_fu = str(uiobj['Member']['fu (MPa)'])
    beam_fy = str(uiobj['Member']['fy (MPa)'])
    weldSize = str(uiobj["Weld"]['Size (mm)'])
    # 'Size (mm)'

    minplatethk = str(int(round(outobj['Plate']['MinThick'], 1)))
    blockshear = str(int(round(outobj['Plate']['blockshear'], 1)))

    plateWidth = str(int(round(outobj['Plate']['Width'], 1)))
    plateMinWidth = str(int(round(outobj['Plate']['MinWidth'], 1)))
    plateLength = str(int(round(outobj['Plate']['Height'], 1)))
#     weldSize = str(int(round(outobj["Weld"]['Size (mm)'],1)))

    plateDimension = plateLength + 'X' + plateWidth + 'X' + plateThick
    noOfBolts = str(outobj['Bolt']['numofbolts'])
    noOfRows = str(outobj['Bolt']['numofrow'])
    noOfCol = str(outobj['Bolt']['numofcol'])
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
    shearCapacity = str(round(outobj['Bolt']['shearcapacity'], 3))
    bearingcapacity = str(round(outobj['Bolt']['bearingcapacity'], 4))
    criticalShear = str(round(outobj['Bolt']['critshear'], 3))

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox
    rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>''&nbsp''<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right"') + row[2] + t('/td')
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
    row = [0, 'Method']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
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

    row = [1, "Endplate", "Pass"]
    rstr += t('tr')
    rstr += t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail1 "') + row[2] + t('/td')
    # rstr += t('td class="header1 safe"') + row[3] + t('/td')
    rstr += t('/tr')

    row = [0, "Endplate", " "]
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

    row = [1, "Connection Title", " Flexible Endplate"]
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

    row = [1, "Beam Connection", "Welded"]
    rstr += t('tr')
    rstr += t('td class="detail2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

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
    row = [2, "Size (mm)", weldSize]
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
    row = [1, "Column-Beam Clearance (mm)", plateThick]
    rstr += t('tr')
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2 "') + row[2] + t('/td')
    rstr += t('/tr')

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

# *************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>'
           ' &nbsp' '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right"') + row[2] + t('/td')
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
    row = [0, 'Method']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
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
    row = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsb</sub> = ((" + bolt_fu + "*" + const + "*" + bolt_dia + "*" +
           bolt_dia + ")/(&#8730;3*1.25*1000) = " + shearCapacity + "<br> [cl. 10.3.3]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt bearing capacity (kN)",""," <i>V</i><sub>dsb</sub> = (2.5*0.5*20*8.9*410)  = 72.98<br> [cl. 10.3.4]"]
    row = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + t_thinner + "*" + beam_fu + ")/(1.25*1000) = " +
           bearingcapacity + "<br> [cl. 10.3.4]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt capacity (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    boltCapacity = str(min(float(shearCapacity), float(bearingcapacity)))
    row = [0, "Bolt capacity (kN)", "", "Min (" + shearCapacity + ", " + bearingcapacity + ") = " + boltCapacity,
           "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Critical Bolt Shear (kN)","","Min (90.53,72.98) = 72.98","<p align=right style=color:green><b>Pass</b></p>"]
    row = [0, "Critical bolt shear (kN)", " &#8804; " + boltCapacity, criticalShear,
           "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"No. of bolts","140/72.98 = 1.9","3","<p align=right style=color:green><b>Pass</b></p>"]
#     bolts = str(round(float(shear_load)/float(boltCapacity),1))
#     row =[0,"No. of bolts", shear_load + "/" + boltCapacity + " = " + bolts, noOfBolts, " <p align=left style=color:green><b>Pass</b></p>"]
    row = [0, "No. of bolts", "", noOfBolts, " "]
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
    row = [0, "No. of bolts per column per side of end plate", " ", noOfRows, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt pitch (mm)","&#8805;2.5*20 = 50, &#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","100"]
    minPitch = str(int(2.5 * float(bolt_dia)))
    maxPitch = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    row = [0, "Bolt pitch (mm)", " &#8805; 2.5*" + bolt_dia + " = " + minPitch + ",  &#8804; Min(32*" + beam_tw + ", 300) = " + maxPitch +
           "<br> [cl. 10.2.2]", pitch, "<p align=left style=color:green><b>Pass</b></p>"]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Bolt gauge (mm)","&#8805;2.5*20 = 50,&#8804; Min(32*8.9, 300) = 300 <br> [cl. 10.2.2]","0"]
    minGauge = str(int(2.5 * float(bolt_dia)))
    maxGauge = str(300) if 32 * float(beam_tw) > 300 else str(int(math.ceil(32 * float(beam_tw))))
    row = [0, "Bolt gauge (mm)", " &#8805; 2.5*" + bolt_dia + " = " + minGauge + ", &#8804; Min(32*" + beam_tw + ", 300) = " + maxGauge +
           " <br> [cl. 10.2.2]", gauge, ""]
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
           "<p align=left style=color:green><b>Pass</b></p>"]
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
    row = [0, "Block shear capacity (kN)", "&#8805;  " + shear_load, "<i>V</i><sub>db</sub> = " + blockshear + "<br> [cl. 6.4.1]", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Plate thickness (mm)","(5*140*1000)/(300*250)= 9.33","10"]

    row = [0, "Plate thickness (mm)", "&#8805;  " + minplatethk, plateThick, " <p align=left style=color:green><b>Pass</b></p> "]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    if connectivity == "Beam-Beam":
        maxLen = str(float(beam_d) - float(column_R1) - float(column_f_t) - float(beam_f_t) - float(beam_R1) - 5)
        strmaxLen = "-" + beam_f_t + "-" + beam_R1 + "-" + column_f_t + "-" + column_R1 + "- 5"
    else:
        maxLen = str(float(beam_d) - 2 * (float(beam_f_t) + float(beam_R1) + 5))
        strmaxLen = "-" + beam_f_t + "-" + beam_R1 + "-" + beam_f_t + "-" + beam_R1 + "- 10"
    minLen = str(0.6 * float(beam_d))
    row = [0, "Plate height (mm)", "&#8805; 0.6*" + beam_d + "=" + minLen + ", &#8804; " + beam_d + strmaxLen + "=" + maxLen +
           "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", plateLength, " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    strmaxWidth = ""
    maxWidth = ""
    if connectivity == "Column web-Beam web":
        maxWidth = str(float(column_d) - 2 * (float(column_R1) + float(column_f_t) + 5))
        strmaxWidth = column_d + "-2*(" + column_f_t + "+" + column_R1 + " +5)"
    elif connectivity == "Column flange-Beam web":
        maxWidth = str(float(column_b))
        strmaxWidth = column_b
    else:
        maxWidth = str(int(140 + 2 * (int(gauge + end))))
        strmaxWidth = "140" + "2*(" + gauge + end + ")"

    minWidth = plateMinWidth
    row = [0, "Plate Width (mm)", "&#8805; " + minWidth + ", &#8804; " + maxWidth + "<br>", plateWidth,
           " <p align=left style=color:green><b>Pass</b></p>", "300", ""]
    # row =[0,"Plate width (mm)","",plateWidth]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Effective weld length (mm)","","300 - 2*6 = 288"]
    effWeldLen = str(int(float(plateLength) - (2 * float(weldSize))))
    row = [0, "Effective weld length (mm)", "", plateLength + "-2*" + weldSize + " = " + effWeldLen, ""]
    rstr += t('td class="detail1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[2] + t('/td')
    rstr += t('td class="detail2"') + space(row[0]) + row[3] + t('/td')
    rstr += t('td class="detail1"') + space(row[0]) + row[4] + t('/td')
    rstr += t('/tr')

    rstr += t('tr')
    # row =[0,"Weld strength (kN/mm)","&#8730;[(18100*6)/(2*288)<sup>2</sup>]<sup>2</sup> + [140/(2*288)]<sup>2</sup> <br>=0.699","<i>f</i><sub>v</sub>=(0.7*6*410)/(&#8730;3*1.25)<br>= 0.795<br>[cl. 10.5.7]"," <p align=right style=color:green><b>Pass</b></p>"]
    row = [0, "Weld strength (kN/mm)", weld_shear, "<i>f</i><sub>v</sub> =(0.7*" + weldSize + "*" + weld_fu + ")/(&#8730;3*1.25*1000)<br> = " + weld_strength +
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
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>'' &nbsp'
           '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right"') + row[2] + t('/td')
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
    row = [0, 'Method']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')

    rstr += t('hr')
    rstr += t('/hr')

# ************************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Digram

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

    rstr += t('/table')
    rstr += t('h1 style="page-break-before:always"')  # page break
    rstr += t('/h1')

# *************************************************************************************************************************
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Header of the pdf fetched from dialogbox

    rstr += t('table border-collapse= "collapse" border="1px solid black" width=100%')
    rstr += t('tr')
    row = [0, '<object type= "image/PNG" data= "cmpylogoEnd.png" height=60 ></object>',
           '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>'' &nbsp'
           '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp></object>']
    rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td colspan="2" align= "right"') + row[2] + t('/td')
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
    row = [0, 'Method']
    rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
    row = [0, method]
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
