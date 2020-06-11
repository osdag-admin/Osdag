from builtins import str
import time
from Report_functions import *
import math
from utils.common.common_calculation import *
# from Common import *
import os
# from utils.common import component
from pylatex import Document, Section, Subsection
from pylatex.utils import italic, bold
#import pdflatex
import sys
import datetime
import pylatex as pyl

from pylatex import Document, Section, Subsection, Tabular, Tabularx,MultiColumn, LongTable, LongTabularx, LongTabu, MultiRow, StandAloneGraphic
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
#from pdflatex import PDFLaTeX
import os
from pylatex.base_classes import Environment, CommandBase, Arguments
from pylatex.package import Package
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number, NewPage


from pylatex.utils import bold

class CreateLatex(Document):

    def __init__(self):
        super().__init__()


    def save_latex(self, uiObj, Design_Check, reportsummary, filename, rel_path, Disp_3d_image):
        companyname = str(reportsummary["ProfileSummary"]['CompanyName'])
        companylogo = str(reportsummary["ProfileSummary"]['CompanyLogo'])
        groupteamname = str(reportsummary["ProfileSummary"]['Group/TeamName'])
        designer = str(reportsummary["ProfileSummary"]['Designer'])
        projecttitle = str(reportsummary['ProjectTitle'])
        subtitle = str(reportsummary['Subtitle'])
        jobnumber = str(reportsummary['JobNumber'])
        client = str(reportsummary['Client'])

        does_design_exist = reportsummary['does_design_exist']
        # Add document header
        geometry_options = {"top": "4cm", "hmargin": "2cm", "headheight": "65pt", "footskip": "65pt"}
        doc = Document(geometry_options=geometry_options,indent=False)
        doc.packages.append(Package('amsmath'))
        doc.packages.append(Package('graphicx'))
        doc.packages.append(Package('needspace'))
        doc.append(pyl.Command('fontsize', arguments= [8,12]))
        doc.append(pyl.Command('selectfont'))

        doc.add_color('OsdagGreen', 'HTML', 'D5DF93')

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
            header.append(NoEscape(r'Page \thepage'))
        #
        # doc.preamble.append(header)
        # doc.change_document_style("header")

        # Add Heading
        # with doc.create(MiniPage(align='c')):


        doc.preamble.append(header)
        doc.change_document_style("header")

        with doc.create(Section('Input Parameters')):
            with doc.create(LongTable('|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4.5cm}|', row_height=1.2)) as table:
                table.add_hline()
                for i in uiObj:
                    # row_cells = ('9', MultiColumn(3, align='|c|', data='Multicolumn not on left'))
                    if i == "Selected Section Details":
                        continue
                    if type(uiObj[i]) == dict:
                        table.add_hline()
                        sectiondetails = uiObj[i]
                        image_name = sectiondetails[KEY_DISP_SEC_PROFILE]

                        Img_path = '/ResourceFiles/images/'+image_name+'.png'
                        if (len(sectiondetails))% 2 == 0:
                        # merge_rows = int(round_up(len(sectiondetails),2)/2 + 2)
                            merge_rows = int((len(sectiondetails)/2)) +2
                        else:
                            merge_rows = round_up((len(sectiondetails)/2),2)
                        if (len(sectiondetails))% 2 == 0:
                            sectiondetails['']=''

                        a = list(sectiondetails.keys())
                        # index=0
                        for x in range(1, (merge_rows + 1)):
                            # table.add_row("Col.Det.",i,columndetails[i])
                            if x == 1:
                                table.add_row(
                                    (MultiRow(merge_rows, data=StandAloneGraphic(image_options="width=5cm,height=5cm",
                                                                                 filename=rel_path + Img_path)),
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
                    elif i == 'Section Size*':
                        table.add_hline()
                        table.add_row((MultiColumn(3, align='|c|', data=i, ),MultiColumn(2, align='|c|', data="Ref List of Input Section"),))
                        table.add_hline()
                    elif len(str(uiObj[i])) > 55 and type(uiObj[i]) != pyl.math.Math:
                        str_len = len(str(uiObj[i]))
                        loop_len = round_up((str_len / 55), 1, 1)
                        for j in range(1, loop_len + 1):
                            b = 55 * j + 1
                            if j == 1:
                                table.add_row(
                                    (MultiColumn(3, align='|c|', data=MultiRow(loop_len,data=i)), MultiColumn(2, align='|c|', data=uiObj[i][0:b]),))
                            else:
                                table.add_row(
                                    (MultiColumn(3, align='|c|', data=MultiRow(loop_len,data="")),
                                     MultiColumn(2, align='|c|', data=uiObj[i][b - 55:b]),))
                        table.add_hline()
                    else:
                        table.add_hline()
                        table.add_row((MultiColumn(3, align='|c|', data=i), MultiColumn(2, align='|c|', data=uiObj[i]),))
                        table.add_hline()
            for i in uiObj:
                if i == 'Section Size*':
                    with doc.create(Subsection("List of Input Section")):
                        with doc.create(LongTable('|p{8cm}|p{8cm}|', row_height=1.2)) as table:
                                str_len = len(uiObj[i])
                                loop_len = round_up((str_len/83),1,1)
                                for j in range(1,loop_len+1):
                                    table.add_hline()
                                    b= 83*j+1
                                    if j ==1:
                                        table.add_row((MultiColumn(1, align='|c|', data=i, ),
                                                       MultiColumn(1, align='|c|', data=uiObj[i][0:b]),))
                                    else:
                                        table.add_row((MultiColumn(1, align='|c|', data=" ", ),
                                                       MultiColumn(1, align='|c|', data=uiObj[i][b-83:b]),))
                                    table.add_hline()

        doc.append(pyl.Command('Needspace', arguments=NoEscape(r'10\baselineskip')))
        # doc.append(NewPage())
        count = 0
        with doc.create(Section('Design Checks')):
            for check in Design_Check:
                if check[0] == 'SubSection':
                    if count >=1:
                        # doc.append(NewPage())
                        doc.append(pyl.Command('Needspace', arguments=NoEscape(r'10\baselineskip')))
                    with doc.create(Subsection(check[1])):
                        with doc.create(LongTable(check[2], row_height=1.2)) as table:  # todo anjali remove
                            table.add_hline()
                            table.add_row(('Check', 'Required', 'Provided', 'Remarks'), color='OsdagGreen')
                            table.add_hline()
                            table.end_table_header()
                            table.add_hline()
                            count = count + 1
                elif check[0] == "Selected":
                    if count >=1:
                        # doc.append(NewPage())
                        doc.append(pyl.Command('Needspace', arguments=NoEscape(r'10\baselineskip')))
                    with doc.create(Subsection(check[1])):
                        with doc.create(LongTable(check[2], row_height=1.2)) as table:
                            table.add_hline()
                            for i in uiObj:
                                # row_cells = ('9', MultiColumn(3, align='|c|', data='Multicolumn not on left'))

                                print(i)
                                if type(uiObj[i]) == dict:
                                    table.add_hline()
                                    sectiondetails = uiObj[i]
                                    image_name = sectiondetails[KEY_DISP_SEC_PROFILE]
                                    Img_path = '/ResourceFiles/images/' + image_name + '.png'
                                    if (len(sectiondetails)) % 2 == 0:
                                        # merge_rows = int(round_up(len(sectiondetails),2)/2 + 2)
                                        merge_rows = int(round_up((len(sectiondetails) / 2), 1, 0) + 2)
                                    else:
                                        merge_rows = int(round_up((len(sectiondetails) / 2), 1, 0) + 1)
                                    print('Hi', len(sectiondetails) / 2, round_up(len(sectiondetails), 2) / 2,
                                          merge_rows)
                                    if merge_rows % 2 == 0:
                                        sectiondetails[''] = ''
                                    a = list(sectiondetails.keys())
                                    # index=0
                                    for x in range(1, (merge_rows + 1)):
                                        # table.add_row("Col.Det.",i,columndetails[i])
                                        if x == 1:
                                            table.add_row(
                                                (MultiRow(merge_rows,
                                                          data=StandAloneGraphic(image_options="width=5cm,height=5cm",
                                                                                 filename=rel_path + Img_path)),
                                                 MultiColumn(2, align='|c|', data=a[x]),
                                                 MultiColumn(2, align='|c|', data=sectiondetails[a[x]]),))
                                        elif x <= 4:
                                            table.add_row(('', MultiColumn(2, align='|c|', data=a[x]),
                                                           MultiColumn(2, align='|c|', data=sectiondetails[a[x]]),))
                                        else:
                                            table.add_row(('', a[x], sectiondetails[a[x]], a[merge_rows + x - 4],
                                                           sectiondetails[a[merge_rows + x - 4]],))
                                        table.add_hline(2, 5)
                            table.add_hline()
                        count = count + 1
                else:
                    table.add_row((check[0], check[1], check[2], check[3]))
                    table.add_hline()
        # doc.append(pyl.Command('Needspace', arguments=NoEscape(r'10\baselineskip')))

        doc.append(NewPage())


        if (not 'TRAVIS' in os.environ) and (does_design_exist):
            with doc.create(Section('3D View')):
                with doc.create(Figure(position='h!')) as view_3D:
                    view_3dimg_path = rel_path + Disp_3d_image
                    # view_3D.add_image(filename=view_3dimg_path, width=NoEscape(r'\linewidth'))
                    view_3D.add_image(filename=view_3dimg_path)

                    view_3D.add_caption('3D View')

        doc.generate_pdf(filename, compiler='pdflatex', clean_tex=False)

