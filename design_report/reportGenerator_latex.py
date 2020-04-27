"""This file is redundant. Use report_generator.py"""

'''
Created on Dec 10, 2015

@author: deepa
'''
from builtins import str
import time
from Report_functions import *
import math
from utils.common.common_calculation import *
# from Common import *
import os
import pdfkit
import configparser
# from utils.common import component
from pylatex import Document, Section, Subsection
from pylatex.utils import italic, bold
import pdflatex
import sys
import datetime
from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject
import pylatex as pyl

from pylatex import Document, Section, Subsection, Tabular, Tabularx,MultiColumn, LongTable, LongTabularx, LongTabu, MultiRow, StandAloneGraphic
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
from pdflatex import PDFLaTeX
import os
from pylatex.base_classes import Environment, CommandBase, Arguments
from pylatex.package import Package
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number

from pylatex.utils import bold

class CreateLatex(Document):

    def __init__(self):
        super().__init__()

    @pyqtSlot()

    def save_latex(self, uiObj, Design_Check, reportsummary, filename, rel_path, Disp_3d_image):
        companyname = str(reportsummary["ProfileSummary"]['CompanyName'])
        companylogo = str(reportsummary["ProfileSummary"]['CompanyLogo'])
        groupteamname = str(reportsummary["ProfileSummary"]['Group/TeamName'])
        designer = str(reportsummary["ProfileSummary"]['Designer'])
        projecttitle = str(reportsummary['ProjectTitle'])
        subtitle = str(reportsummary['Subtitle'])
        jobnumber = str(reportsummary['JobNumber'])
        client = str(reportsummary['Client'])

        # Add document header

        header = PageStyle("header")
        # Create center header
        with header.create(Head("C")):
            with header.create(Tabularx('|l|p{6cm}|l|X|')) as table:
                table.add_hline()
                # MultiColumn(4)
                table.add_row(('Company Name', companyname, 'Project Title', projecttitle), color='OsdagGreen')
                table.add_hline()
                table.add_row(('Group/Team Name', groupteamname, 'Subtitle', subtitle), color='OsdagGreen')
                table.add_hline()
                table.add_row(('Designer', designer, 'Job Number', jobnumber), color='OsdagGreen')
                table.add_hline()
                table.add_row(('Date', time.strftime("%d /%m /%Y"), 'Client', client), color='OsdagGreen')
                table.add_hline()

        # Create right footer
        with header.create(Foot("R")):
            header.append(simple_page_number())
        #
        # doc.preamble.append(header)
        # doc.change_document_style("header")

        # Add Heading
        # with doc.create(MiniPage(align='c')):
        geometry_options = {"top": "1.2in", "bottom": "1in", "left": "0.6in", "right": "0.6in", "headsep": "0.8in"}
        doc = Document(geometry_options=geometry_options, indent=False)
        doc.packages.append(Package('amsmath'))
        doc.packages.append(Package('graphicx'))
        doc.packages.append(Package('needspace'))
        doc.add_color('OsdagGreen', 'HTML', 'D5DF93')
        doc.preamble.append(header)
        doc.change_document_style("header")

        with doc.create(Section('Input Parameters')):
            with doc.create(LongTable('|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{5cm}|', row_height=1.2)) as table:
                table.add_hline()
                for i in uiObj:
                    # row_cells = ('9', MultiColumn(3, align='|c|', data='Multicolumn not on left'))

                    print(i)
                    if type(uiObj[i]) == dict:
                        table.add_hline()
                        sectiondetails = uiObj[i]
                        image_name = sectiondetails[KEY_DISP_SEC_PROFILE]
                        Img_path = r'/ResourceFiles/images/'+image_name+r'".png'
                        if (len(sectiondetails))% 2 == 0:
                        # merge_rows = int(round_up(len(sectiondetails),2)/2 + 2)
                            merge_rows = int(round_up((len(sectiondetails)/2),1,0) + 2)
                        else:
                            merge_rows = int(round_up((len(sectiondetails)/2),1,0) + 1)
                        print('Hi', len(sectiondetails)/2,round_up(len(sectiondetails),2)/2, merge_rows)
                        if merge_rows%2 != 0:
                            sectiondetails['']=''
                        a = list(sectiondetails.keys())
                        # index=0
                        for x in range(1,(merge_rows+1)):
                            # table.add_row("Col.Det.",i,columndetails[i])
                            if x == 1:
                                table.add_row(
                                    (MultiRow(merge_rows, data=StandAloneGraphic(image_options="width=5cm,height=5cm",
                                                                                 filename=r'"' + rel_path + Img_path)),
                                     MultiColumn(2, align='|c|', data=a[x]),
                                     MultiColumn(2, align='|c|', data=sectiondetails[a[x]]),))
                            elif x <= 4:
                                table.add_row(('', MultiColumn(2, align='|c|', data=a[x]),
                                               MultiColumn(2, align='|c|', data=sectiondetails[a[x]]),))
                            else:
                                table.add_row(('', a[x], sectiondetails[a[x]], a[merge_rows + x - 4],
                                               sectiondetails[a[merge_rows + x - 4]],))
                            table.add_hline(2, 5)
                    elif uiObj[i] == "TITLE":
                        table.add_hline()
                        table.add_row((MultiColumn(5, align='|c|', data=bold(i), ),))
                        table.add_hline()
                    else:
                        table.add_hline()
                        table.add_row(
                            (MultiColumn(3, align='|c|', data=i), MultiColumn(2, align='|c|', data=uiObj[i]),))
                        table.add_hline()
        doc.append(pyl.Command('Needspace', arguments=NoEscape(r'10\baselineskip')))
        with doc.create(Section('Design Checks')):
            for check in Design_Check:
                if check[0] == 'SubSection':
                    with doc.create(Subsection(check[1])):
                        with doc.create(LongTable(check[2], row_height=1.2)) as table: # todo anjali remove
                            table.add_hline()
                            table.add_row(('Check', 'Required', 'Provided', 'Remarks'), color='OsdagGreen')
                            table.add_hline()
                            table.end_table_header()
                            table.add_hline()
                else:
                    table.add_row((check[0], check[1], check[2], check[3]))
                    table.add_hline()
        doc.append(pyl.Command('Needspace', arguments=NoEscape(r'10\baselineskip')))
        with doc.create(Section('3D View')):
            with doc.create(Figure(position='h!')) as view_3D:
                view_3dimg_path = rel_path + Disp_3d_image
                view_3D.add_image(filename=r'"' + view_3dimg_path, width=NoEscape(r'\linewidth'))
                view_3D.add_caption('3D View')

        doc.generate_pdf(filename, compiler='pdflatex', clean_tex=False)


# reportsummary = {}
# reportsummary["ProfileSummary"] = {}
# reportsummary["ProfileSummary"]["CompanyName"] = 'a'
# reportsummary["ProfileSummary"]["CompanyLogo"] = 'a'
# reportsummary["ProfileSummary"]["Group/TeamName"] = 'a'
# reportsummary["ProfileSummary"]["Designer"] = 'a'
#
# reportsummary["ProjectTitle"] = 'a'
# reportsummary["Subtitle"] = 'a'
# reportsummary["JobNumber"] = 'a'
# reportsummary["AdditionalComments"] = 'a'
# reportsummary["Client"] = 'a'
#
# # def save_latex(outObj, uiObj, Design_Check, section_1, section_2,reportsummary, filename, folder):
# #     call_latex(outObj, uiObj, Design_Check, section_1, section_2,reportsummary, filename, folder)
# report_check =[]
# t1 = ('Bolt_shear', report_bolt_shear_check)
# report_check.append(t1)
# CreateLatex.save_latex(CreateLatex(),[],[],report_check,[],[],reportsummary,'','')
# class ReportGenerator():
#     def __init__(self):
#         self.generate_header()
#
#     def generate_header(self):
#         geometry_options = {"top" : "1in", "bottom" : "1in", "left" : "0.8in", "right" : "0.6in"}
#         doc = Document(geometry_options=geometry_options)
#         # Add document header
#         header = PageStyle("header")
#
#         # Create center header
#         with header.create(Head("C")):
#             with header.create(Tabularx('|l|p{3cm}|l|r|')) as table:
#                 table.add_hline()
#                 table.add_row(('Company Name', '', 'Project Title', ''))
#                 table.add_hline()
#                 table.add_row(('Group/Team Name', '', 'Subtitle', ''))
#                 table.add_hline()
#                 table.add_row(('Designer', '', 'Job Number', ''))
#                 table.add_hline()
#                 table.add_row(('Date', '', 'Client', ''))
#             header.append(table)
#
#
#         # Create right footer
#         with header.create(Foot("R")):
#             header.append(simple_page_number())
#
#         doc.preamble.append(header)
#         doc.change_document_style("header")
#         doc.generate_pdf("header", clean_tex=False)



    # doc = Document(documentclass='article')
    #
    # # creating a pdf with title "the simple stuff"
    #
    # with doc.create(Tabularx('|l|p{3cm}|l|l|')) as table:
    #     table.add_hline()
    #     table.add_row(('Company Name', '', 'Project Title', ''))
    #     table.add_hline()
    #     table.add_row(('Group/Team Name', '', 'Subtitle', ''))
    #     table.add_hline()
    #     table.add_row(('Designer', '', 'Job Number', ''))
    #     table.add_hline()
    #     table.add_row(('Date', '', 'Client', ''))
    #
    # # making a pdf using .generate_pdf
    # doc.generate_pdf(clean_tex=False, compiler='pdflatex')

#
# # from Connections.connection_calculations import ConnectionCalculations
#
# def save_html(outObj, uiObj, Design_Check, section_1, section_2,reportsummary, filename, folder):
#     fileName = (filename)
#     myfile = open(fileName, "w")
#     myfile.write(t('! DOCTYPE html'))
#     myfile.write(t('html'))
#     myfile.write(t('head'))
#     myfile.write(t('link type="text/css" rel="stylesheet" '))
#
# # mystyle.css is written here
#     myfile.write(t('style'))
#     myfile.write('table{width= 100% height = 100%; border-collapse:collapse; border:1px solid black collapse}')
#     myfile.write('th,td {padding:3px}')
#
# # avoid page break
#     myfile.write('table{ page-break-inside:auto }')
#     myfile.write('tr{ page-break-inside:avoid; page-break-after:auto }')
#
# #     Provides light green background color(#D5DF93), font-weight bold, font-size 20 and font-family
#     myfile.write('td.detail{background-color:#D5DF93; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
# #     Provides font-weight bold, font-size 20 and font-family
#     myfile.write('td.detail1{font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
# #     Provides font-size 20 and font-family
#     myfile.write('td.detail2{font-size:20; font-family:Helvetica, Arial, Sans Serif}')
# #     Provides dark green background color(#8FAC3A), font-weight bold, font-size 20 and font-family
#     myfile.write('td.header0{background-color:#8fac3a; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
# #     Provides grey background color(#E6E6E6), font-weight bold, font-size 20 and font-family
#     myfile.write('td.header1{background-color:#E6E6E6; font-size:20; font-family:Helvetica, Arial, Sans Serif; font-weight:bold}')
# #     Provides only font-size 20 and width of the images box
#     myfile.write('td.header2{font-size:20; width:50%}')
#     myfile.write(t('/style'))
# ##############################################################################################################################################
#
#     myfile.write(t('/head'))
#     myfile.write(t('body'))
#
# # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# # Design Conclusion
#     rstr = ""
#     h = header(reportsummary)
#     rstr += h
#     rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
#     rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100% ')
#
#     row = [0, 'Design Conclusion', "IS800:2007/Limit state design"]
#     rstr += t('tr')
#     rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td colspan="2" class="header0"') + row[2] + t('/td')
#     # rstr += t('td colspan="2" class="header0"') + t('/td')
#     rstr += t('/tr')
#     mainfolder = "/home/darshan/Desktop/Osdag3_new/Osdag3/ResourceFiles/images"
#     mainfolder = r'C:\Users\Win10\Desktop\Osdag3-master\ResourceFiles\images'
#     for i in uiObj:
#         row1 = [0,i, uiObj[i]]
#         rstr += t('tr')
#         rstr += t('td colspan="3" class="detail1"') + space(row1[0]) + row1[1] + t('/td')
#         rstr += t('td colspan="2" class="detail2 "') + str(row1[2]) + t('/td')
#         rstr += t('/tr')
#         png = mainfolder + "/Columns_Beams.png"
#         datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png
#         if i == "Column Details":
#             row = [0, datapng, ""]
#             rstr += t('tr')
#             rstr += t('td rowspan = "17" align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
#             # rstr += t('td  align="center" class=" header2"') + row[2] + t('/td')
#             spec = extract_details(section_1)
#             for k in spec:
#                 # rstr += t('tr')
#                 rstr += t('td colspan = "2" width = "300" class="detail2"') + space(k[0]) + k[1] + t('/td')
#                 rstr += t('td colspan = "2" width = "300" class="detail2 "') + k[2] + t('/td')
#                 rstr += t('/tr')
#         if i == "Beam Details":
#             png = mainfolder + "/Columns_Beams.png"
#             datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png
#             row = [0, datapng, ""]
#             rstr += t('tr')
#             rstr += t('td rowspan = "17" align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
#             spec = extract_details(section_2)
#             for l in spec:
#                 # rstr += t('tr')
#                 rstr += t('td colspan = "2" width = "300" class="detail2"') + space(l[0]) + l[1] + t('/td')
#                 rstr += t('td colspan = "2" width = "300" class="detail2 "') + l[2] + t('/td')
#                 rstr += t('/tr')
#         # for k,v in subtitle:
#         #     print(k,v)
#         # for j in uiObj[i]:
#         #     if j =="Column Details":
#         #         row2 = [0, j ,""]
#         #         rstr += t('tr')
#         #         rstr += t('td colspan="3" class="detail1"') + space(row2[0]) + row2[1] + t('/td')
#         #         rstr += t('td colspan="2" class="detail1"') + row2[2] + t('/td')
#         #         rstr += t('/tr')
#         #         png = mainfolder + "/Columns_Beams.png"
#         #         datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png
#         #         row = [0, datapng, ""]
#         #         rstr += t('tr')
#         #         rstr += t('td rowspan = "17" align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
#         #         # rstr += t('td  align="center" class=" header2"') + row[2] + t('/td')
#         #         spec = extract_details(section_1)
#         #         for k in spec:
#         #             # rstr += t('tr')
#         #             rstr += t('td colspan = "2" width = "300" class="detail2"') + space(k[0]) + k[1] + t('/td')
#         #             rstr += t('td colspan = "2" width = "300" class="detail2 "') + k[2] + t('/td')
#         #             rstr += t('/tr')
#         #     elif j == "Beam Details":
#         #         row2 = [0, j,""]
#         #         rstr += t('tr')
#         #         rstr += t('td colspan="3" class="detail1"') + space(row2[0]) + row2[1] + t('/td')
#         #         rstr += t('td colspan="2" class="detail1" ') + row2[2] + t('/td')
#         #         rstr += t('/tr')
#         #         png = mainfolder + "/Columns_Beams.png"
#         #         datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png
#         #         row = [0, datapng, ""]
#         #         rstr += t('tr')
#         #         rstr += t('td rowspan = "17" align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
#         #         spec = extract_details(section_2)
#         #         for l in spec:
#         #             # rstr += t('tr')
#         #             rstr += t('td colspan = "2" width = "300" class="detail2"') + space(l[0]) + l[1] + t('/td')
#         #             rstr += t('td colspan = "2" width = "300" class="detail2 "') + l[2] + t('/td')
#         #             rstr += t('/tr')
#         #     else:
#         #         row2 = [1, j, str(uiObj[i][j])]
#         #         rstr += t('tr')
#         #         rstr += t('td colspan="3" class="detail2"') + space(row2[0]) + row2[1] + t('/td')
#         #         rstr += t('td colspan="2" class="detail2 "') + row2[2] + t('/td')
#         #         rstr += t('/tr')
#
# #     #
#     rstr += t('/table')
#     rstr += t('h1 style="page-break-before:always"')  # page break
#     rstr += t('/h1')
#
#     # Diagram
#     rstr += h
#     rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
#
#     row = [0, "Views", " "]
#     rstr += t('tr')
#     rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('/tr')
#     png = folder + "/images_html/3D_Model.png"
#     datapng = '<object type="image/PNG" data= %s width ="450"></object>' % png
#
#     side = folder + "/finSide.png"
#     dataside = '<object type="image/PNG" data= %s width ="400"></object>' % side
#
#     top = folder + "/finTop.png"
#     datatop = '<object type="image/PNG" data= %s width ="400"></object>' % top
#
#     front = folder + "/finFront.png"
#     datafront = '<object type="image/PNG" data= %s width ="450"></object>' % front
#
#     if str(outObj[KEY_MODULE_STATUS]) == 'True':
#         row = [0, datapng, datatop]
#         rstr += t('tr')
#         rstr += t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
#         rstr += t('td  align="center" class=" header2"') + row[2] + t('/td')
#         rstr += t('/tr')
#
#         row = [0, dataside, datafront]
#         rstr += t('tr')
#         rstr += t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td')
#         rstr += t('td align="center" class=" header2 "') + row[2] + t('/td')
#         rstr += t('/tr')
#
#     else:
#         pass
#
#     rstr += t('/table')
#     rstr += t('h1 style="page-break-before:always"')  # page break
#     rstr += t('/h1')
#
#     # # *************************************************************************************************************************
# # # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# # # Design Check
#     rstr +=h
#     rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
#     row = [0, "Design Check", " "]
#     rstr += t('tr')
#     rstr += t('td colspan="4" class="detail"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('/tr')
#
#     rstr += t('tr')
#     row = [0, "Check", "Required", "Provided", "Remark"]
#     rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td class="header1"') + space(row[0]) + row[2] + t('/td')
#     rstr += t('td class="header1"') + space(row[0]) + row[3] + t('/td')
#     rstr += t('td class="header1"') + space(row[0]) + row[4] + t('/td')
#     rstr += t('/tr')
#
#
#     def checks(i):
#         # Design_Check = ["bolt_shear_capacity" ]
#         if i == KEY_OUT_BOLT_SHEAR:
#             const = str(round(math.pi / 4 * 0.78, 4))
#             # row =[0,"Bolt shear capacity (kN)"," ","<i>V</i><sub>dsb</sub> = ((800*0.6123*20*20)/(&#8730;3*1.25*1000) = 90.53 <br> [cl. 10.3.3]"]
#             # n_e = str(1)
#             if outObj[KEY_OUT_BOLT_BEARING] == "N/A" :
#                 i = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsf</sub> = ((" + "sf" + "*" +"ne"+ "*" + "Kh" + "*" + "F0" +
#                        ")/(1.25)) = " + str(outObj[KEY_OUT_BOLT_SHEAR]) + "<br> [cl. 10.4.3]", ""]
#             else:
#                 i = [0, "Bolt shear capacity (kN)", " ", "<i>V</i><sub>dsb</sub> = (" + "Fubo" + "*" + const + "*" + "d" + "*" + "d" +
#                    ")/(&#8730;3*1.25*1000) = " + str(outObj[KEY_OUT_BOLT_SHEAR]) + "<br> [cl. 10.3.3]", ""]
#
#         elif i == KEY_OUT_BOLT_BEARING:
#             if outObj[KEY_OUT_BOLT_BEARING] == "N/A" :
#                 i = [0, "Bolt bearing capacity (kN)", "", "N/A", ""]
#             else:
#                 i = [0, "Bolt bearing capacity (kN)", "", " <i>V</i><sub>dpb</sub> = (2.5*" + "kb" + "*" + "d" + "*" + "t"+ "*" + "Fub" + ")/(1.25*1000)  = " +
#                    str(outObj[KEY_OUT_BOLT_BEARING]) + "<br> [cl. 10.3.4]", ""]
#
#         elif i == KEY_OUT_BOLT_CAPACITY:
#             if outObj[KEY_OUT_BOLT_BEARING] == "N/A":
#                 i = [0, "Bolt capacity (kN) - bcp", "",   outObj[KEY_OUT_BOLT_CAPACITY], ""]
#             else:
#                 i = [0, "Bolt capacity (kN) - bcp", "", "Min (" + str(outObj[KEY_OUT_BOLT_SHEAR]) + ", " + str(outObj[KEY_OUT_BOLT_BEARING]) + ") = " + str(outObj[KEY_OUT_BOLT_CAPACITY]), ""]
#
#         elif i == KEY_OUT_BOLTS_REQUIRED:
#             i = [0,"No. of bolts",("" + ' Vs' + "/" + "bcp" + "=" + str(round(float(uiObj[KEY_SHEAR])/float(outObj[KEY_OUT_D_PROVIDED]), 2))+ ""),("" + str(outObj[KEY_OUT_BOLTS_REQUIRED])+ ""), "<p align=center style=color:green><b>Pass</b></p>"]
#
#         elif i == KEY_OUT_BOLTS_ONE_LINE:
#             i = [0, "No of row(s)", "", str(outObj[KEY_OUT_BOLTS_ONE_LINE]), ""]
#
#         elif i == KEY_OUT_BOLT_LINE:
#             i = [0, "No of column(s)", " &#8804; 2", str(outObj[KEY_OUT_BOLT_LINE]), ""]
#
#         elif i == KEY_OUT_PITCH:
#             minPitch = str(int(2.5 * float(outObj[KEY_OUT_D_PROVIDED])))
#             maxPitch = str(300) if 32 * float(section_2["t(mm)"]) > 300 else str(int(math.ceil(32 * float(section_2["t(mm)"]))))
#             if int(outObj[KEY_OUT_PITCH]) < int(minPitch) or int(outObj[KEY_OUT_PITCH]) > int(maxPitch):
#                 i = [0, "Bolt pitch (mm)", "&#8805;2.5*d = p, &#8804; Min(32*tmin, 300) = 300 <br> [cl. 10.2.2]",
#                               ("" + str(outObj[KEY_OUT_PITCH]) + ""),
#                               "<p align=center style=color:red><b>Fail</b></p>"]
#             else:
#                 i = [0, "Bolt pitch (mm)", "&#8805;2.5*d = p, &#8804; Min(32*tmin, 300) = 300 <br> [cl. 10.2.2]",
#                               ("" + str(outObj[KEY_OUT_PITCH]) + ""),
#                               "<p align=center style=color:green><b>Pass</b></p>"]
#
#         elif i == KEY_OUT_GAUGE:
#             minGauge = str(int(2.5 * float(outObj[KEY_OUT_D_PROVIDED])))
#             maxGauge = str(300) if 32 * float(section_2["t(mm)"]) > 300 else str(int(math.ceil(32 * float(section_2["t(mm)"]))))
#             if (int(outObj[KEY_OUT_GAUGE]) < int(minGauge) or int(outObj[KEY_OUT_GAUGE]) > int(maxGauge)):
#                 i = [0, "Bolt gauge (mm)", "&#8805;2.5*d = g,&#8804; Min(32*tmin, 300) = 300 <br> [cl. 10.2.2]",
#                               ("" + str(outObj[KEY_OUT_GAUGE]) + ""), "<p align=center style=color:red><b>Fail</b></p>"]
#             else:
#                 i = [0, "Bolt gauge (mm)", "&#8805;2.5*d = g,&#8804; Min(32*tmin, 300) = 300 <br> [cl. 10.2.2]",
#                               ("" + str(outObj[KEY_OUT_GAUGE]) + ""),"<p align=center style=color:green><b>Pass</b></p>"]
#
#         elif i == KEY_OUT_END_DIST:
#             minEnd = outObj[KEY_OUT_MIN_EDGE_DIST]
#             maxEnd = outObj[KEY_OUT_MAX_EDGE_DIST]
#             print(outObj[KEY_OUT_MIN_EDGE_DIST],outObj[KEY_OUT_MAX_EDGE_DIST],outObj[KEY_OUT_EDGE_DIST])
#
#             if outObj[KEY_OUT_END_DIST] < minEnd or outObj[KEY_OUT_END_DIST] > maxEnd:
#                 i = [0, "End distance (mm)", " &#8805; " + str(outObj[KEY_OUT_MIN_EDGE_DIST]) + "*" + "d" + " = " + str(minEnd) + ", &#8804; 12*" + "tmin"+ " = " + str(maxEnd) + " <br> [cl. 10.2.4]",(""+
#                    str(outObj[KEY_OUT_END_DIST]) + ""), " <p align=center style=color:red><b>Fail</b></p>"]
#             else:
#                 i = [0, "End distance (mm)", " &#8805; " + str(outObj[KEY_OUT_MIN_EDGE_DIST]) + "*" + "d" + " = " + str(minEnd)  + ", &#8804; 12*" + "tmin"+ " = " + str(maxEnd) + " <br> [cl. 10.2.4]",(""+
#                    str(outObj[KEY_OUT_END_DIST]) + "")," <p align=center style=color:green><b>Pass</b></p>"]
#
#         elif i == KEY_OUT_EDGE_DIST:
#             minEdge = outObj[KEY_OUT_MIN_EDGE_DIST]
#             maxEdge = outObj[KEY_OUT_MAX_EDGE_DIST]
#             if outObj[KEY_OUT_END_DIST] < minEdge or outObj[KEY_OUT_END_DIST] > maxEdge:
#                 i = [0, "Edge distance (mm)", " &#8805; " + str(outObj[KEY_OUT_MIN_EDGE_DIST]) + "*" + "d" + " = " + str(minEdge) + ", &#8804; 12*" + "tmin" + " = " + str(maxEdge) + " <br> [cl. 10.2.4]",
#                                 ("" + str(outObj[KEY_ENDDIST]) + ""), " <p align=center style=color:red><b>Fail</b></p>"]
#             else:
#                 i = [0, "Edge distance (mm)", " &#8805; " + str(outObj[KEY_OUT_MIN_EDGE_DIST]) + "*" + "d" + " = " + str(minEdge) + ", &#8804; 12*" + "tmin" + " = " + str(maxEdge) + " <br> [cl. 10.2.4]",
#                                  ("" + str(outObj[KEY_OUT_EDGE_DIST]) + ""), " <p align=center style=color:green><b>Pass</b></p>"]
#
#         elif i == KEY_OUT_PLATE_BLK_SHEAR:
#             if float(outObj[KEY_OUT_PLATE_BLK_SHEAR]) < float(uiObj[KEY_SHEAR]):
#                 i = [0, "Block shear capacity (kN)", " &#8805; " + str(uiObj[KEY_SHEAR]), str(outObj[KEY_OUT_PLATE_BLK_SHEAR]), "<p align=left style=color:red><b>Fail</b></p>"]
#             else:
#                 i = [0, "Block shear capacity (kN)", " &#8805; " + str(uiObj[KEY_SHEAR]), str(outObj[KEY_OUT_PLATE_BLK_SHEAR]), "<p align=center style=color:green><b>Pass</b></p>"]
#
#         elif i == KEY_OUT_PLATE_HEIGHT:
#             minheight = outObj[KEY_PLATE_MIN_HEIGHT]
#             maxheight = outObj[KEY_PLATE_MAX_HEIGHT]
#             plateheight = outObj[KEY_OUT_PLATE_HEIGHT]
#             if uiObj[KEY_CONN] in VALUES_CONN_2:
#                 maxheightstring = "D" + "-" + "T" + "-" + 'R1'+ "-" + "cft" + "-" + "crr"+ "- 5"
#             else:
#                 maxheightstring = "D" + " - 2 * " + "T" + " - 2 * " + 'R1' + "-" + "10"
#             if int(plateheight) < float(minheight) or int(plateheight) > float(maxheight):
#                 i = [0, "Plate height (mm)", "&#8805; 0.6*" + "D" + "=" + str(minheight) + ", &#8804; " + maxheightstring + "=" + str(maxheight) +
#                        "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]", int(outObj[KEY_OUT_PLATE_HEIGHT]), " <p align=center style=color:red><b>Fail</b></p>"]
#             else:
#                 i = [0, "Plate height (mm)", "&#8805; 0.6*" + "D" + "=" + str(minheight) + ", &#8804; " + maxheightstring + "=" + str(maxheight) +
#                        "<br> [cl. 10.2.4, Insdag Detailing Manual, 2002]",int(outObj[KEY_OUT_PLATE_HEIGHT]), " <p align=center style=color:green><b>Pass</b></p>"]
#
#
#         elif i == KEY_OUT_PLATE_MOM_CAPACITY:
#
#             if float(outObj[KEY_OUT_PLATE_MOM_CAPACITY]) > float(outObj[KEY_OUT_PLATE_MOM_DEMAND]):
#                 i = [0, "Plate moment capacity (kNm)",
#                        "(2*" + "Bolt shear capacity" + "*" + "p" + "<sup>2</sup>)/(" + "p" + "*1000) = " + str(outObj[KEY_OUT_PLATE_MOM_DEMAND]),
#                        "<i>M</i><sub>d</sub> = (1.2*" +"Fyb" + "*<i>Z</i>)/(1000*1.1) = " + str(outObj[KEY_OUT_PLATE_MOM_CAPACITY]) + "<br>[cl. 8.2.1.2]",
#                        "<p align=center style=color:red><b>Fail</b></p>"]
#             else:
#                 i = [0, "Plate moment capacity (kNm)", "(2*" + "Bolt shear capacity" + "*" + "p" + "<sup>2</sup>)/(" + "p" + "*1000) = " + str(outObj[KEY_OUT_PLATE_MOM_DEMAND]),
#                    "<i>M</i><sub>d</sub> = (1.2*" + "Fyb "+ "*<i>Z</i>)/(1000*1.1) = " + str(outObj[KEY_OUT_PLATE_MOM_CAPACITY]) + "<br>[cl. 8.2.1.2]",
#                    "<p align=center style=color:green><b>Pass</b></p>"]
#
#         # effWeldLen = str(int(float(outObj["Plate"]['height']) - (2 * float(uiObj["Components"]["Size(mm)-ws"]))))
#         elif i == KEY_OUT_WELD_LENGTH_EFF:
#             i = [0, "Effective weld length on each side (mm)", "", "dp" + "-2*" + "ws" + " = " + str(outObj[KEY_OUT_WELD_LENGTH_EFF]), ""]
#
#         elif i == KEY_OUT_WELD_STRENGTH:
#             if float(outObj[KEY_OUT_WELD_STRESS]) > float(outObj[KEY_OUT_WELD_STRENGTH]):
#                 i = [0, "Weld strength (kN/mm)",
#                        " &#8730;[(" + "md*1000" + "*6)/(2*" +  "efl)]" + "<sup>2</sup>)]<sup>2</sup> + [" + "Vs" + "/(2*" +
#                        "efl" + ")]<sup>2</sup> <br>= " + str(outObj[KEY_OUT_WELD_STRESS]),
#                        "<i>f</i><sub>v</sub>= (0.7*" + "ws" + "*" + "Fuw" + ")/(&#8730;3*1.25)<br>= " +
#                        "wst" + "<br>[cl. 10.5.7]", " <p align=center style=color:red><b>Fail</b></p>"]
#             else:
#                 i = [0, "Weld strength (kN/mm)",
#                                  " &#8730;[(" + "md*1000" + "*6)/(2*" + "efl)]" + "<sup>2</sup>)]<sup>2</sup> + [" + "Vs" + "/(2*" +
#                                  "efl" + ")]<sup>2</sup> <br>= " + str(outObj[KEY_OUT_WELD_STRESS]),
#                                  "<i>f</i><sub>v</sub>= (0.7*" + "ws" + "*" + "Fuw" + ")/(&#8730;3*1.25)<br>= " +
#                                  str(round(outObj[KEY_OUT_WELD_STRENGTH],2))+ "<br>[cl. 10.5.7]",  "<p align=center style=color:green><b>Pass</b></p>"]
#
#         return i
#
#     for i in Design_Check:
#         rstr += t('tr')
#         a = checks(i)
#         for j in range(1,len(a)):
#             rstr += t('td class="detail2"') + space(a[0]) + str(a[j]) + t('/td')
#         rstr += t('/tr')
#
#
#     # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# # Additional comments
#     addtionalcomments = str(reportsummary['AdditionalComments'])
#     rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
#     rstr += t('''col width=30%''')
#     rstr += t('''col width=70%''')
#
#     rstr += t('tr')
#     row = [0, "Additional Comments", addtionalcomments]
#     rstr += t('td colspan = "3" class= "detail1"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td colspan = "3" class= "detail2" align="justified"') + row[2] + t('/td')
#     rstr += t('/tr')
#
#     rstr += t('/table')
#
#     myfile.write(rstr)
#     myfile.write(t('/body'))
#     myfile.write(t('/html'))
#     myfile.close()
#
# def space(n):
#     rstr = "&nbsp;" * 4 * n
#     return rstr
#
# def t(n):
#     return '<' + n + '/>'
#
# def w(n):
#     return '{' + n + '}'
#
# def quote(m):
#     return '"' + m + '"'
#
# #header
# def header(reportsummary):
#     companyname = str(reportsummary["ProfileSummary"]['CompanyName'])
#     companylogo = str(reportsummary["ProfileSummary"]['CompanyLogo'])
#     groupteamname = str(reportsummary["ProfileSummary"]['Group/TeamName'])
#     designer = str(reportsummary["ProfileSummary"]['Designer'])
#     projecttitle = str(reportsummary['ProjectTitle'])
#     subtitle = str(reportsummary['Subtitle'])
#     jobnumber = str(reportsummary['JobNumber'])
#     client = str(reportsummary['Client'])
#
#
#     # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# # Header of the pdf fetched from dialogbox
#     rstr = t('table border-collapse= "collapse" border="1px solid black" width=100%')
#     rstr += t('tr')
#     row = [0, '<object type= "image/PNG" data= "cmpylogoFin.png" height=60 ></object>', '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
#     rstr += t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td')
#     rstr += t('td colspan="2" align= "center"') + row[2] + t('/td')
#     rstr += t('/tr')
#
#     rstr += t('tr')
#     row = [0, 'Company Name']
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
# #     rstr += t('td style= "font:bold 20px Helvetica, Arial, Sans Serif;background-color:#D5DF93"') + space(row[0]) + row[1] + t('/td')
#     row = [0, companyname]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#
#     row = [0, 'Project Title']
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, projecttitle]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     rstr += t('/tr')
#
#     rstr += t('tr')
#     row = [0, 'Group/Team Name']
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, groupteamname]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, 'Subtitle']
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, subtitle]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     rstr += t('/tr')
#
#     rstr += t('tr')
#     row = [0, 'Designer']
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, designer]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, 'Job Number']
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, jobnumber]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     rstr += t('/tr')
#
#     rstr += t('tr')
#     row = [0, 'Date']
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, time.strftime("%d /%m /%Y")]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, "Client"]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     row = [0, client]
#     rstr += t('td class="detail" ') + space(row[0]) + row[1] + t('/td')
#     rstr += t('/tr')
#     rstr += t('/table')
#
#     rstr += t('hr')
# #     rstr += t('p> &nbsp</p')
#     rstr += t('/hr')
#     return rstr
#
#
# def extract_details(membertype):
#     details = []
#     for i in membertype:
#         print(i)
#         detail = [1, str(i), str(membertype[i])]
#         details.append(detail)
#     print (details)
#     return details
#
# if __name__ == '__main__':
#     ReportGenerator()

