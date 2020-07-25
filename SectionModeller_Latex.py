from builtins import str
import time
from pylatex import Document, Section,Figure,Head,Foot,NewPage,Command,NoEscape,Tabularx,PageStyle,Package
from pylatex.utils import bold
import sys
import datetime
import os

class CreateLatex(Document):
    def __init__(self):
        super().__init__()
    def save_latex(self,reportsummary,filename,rel_path,Disp_3d_image):
        companyname = str(reportsummary["ProfileSummary"]['CompanyName'])
        companylogo = str(reportsummary["ProfileSummary"]['CompanyLogo'])
        groupteamname = str(reportsummary["ProfileSummary"]['Group/TeamName'])
        designer = str(reportsummary["ProfileSummary"]['Designer'])
        projecttitle = str(reportsummary['ProjectTitle'])
        subtitle = str(reportsummary['Subtitle'])
        jobnumber = str(reportsummary['JobNumber'])
        client = str(reportsummary['Client'])

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
        
        geometry_options = {"top": "1.2in", "bottom": "1in", "left": "0.6in", "right": "0.6in", "headsep": "0.8in"}
        doc = Document(geometry_options=geometry_options, indent=False)
        doc.packages.append(Package('amsmath'))
        doc.packages.append(Package('graphicx'))
        doc.packages.append(Package('needspace'))
        doc.add_color('OsdagGreen', 'HTML', 'D5DF93')
        doc.preamble.append(header)
        doc.change_document_style("header")


        with doc.create(Section('Design Conclusion')):
            with doc.create(Tabularx('|X|X|', row_height=1.2)) as table:
                table.add_hline()
                table.add_row(('Section Designation','Remarks'),color='OsdagGreen')
                table.add_hline()
                table.add_row((reportsummary['Define Section']['Section Designation'],'Pass'))
                table.add_hline()

        with doc.create(Section('Section Details')):
            with doc.create(Tabularx('|X|X|', row_height=1.2)) as table:
                table.add_hline()
                table.add_row((bold('Section Type'),reportsummary['Define Section']['Section Type']))
                table.add_hline()
                table.add_row((bold('Section Template'),reportsummary['Define Section']['Section Template']))
                table.add_hline()

        with doc.create(Section('Section Parameters')):
            with doc.create(Tabularx('|X|X|', row_height=1.2)) as table:
                for parameter in reportsummary['Define Section']['Section Parameters']:
                    para=reportsummary['Define Section']['Section Parameters'][parameter]
                    table.add_hline()
                    table.add_row((bold(para[0]),para[1]))
                table.add_hline()

        labels=[
                        'Area, a(cm²)',
                        'Moment of Inertia',
                        'I_zz(cm4)',
                        'I_yy(cm4)',
                        'Radius of Gyration',
                        'r_zz(cm)',
                        'r_yy(cm)',
                        'Centriod',
                        'c_z(cm)',
                        'c_y(cm)',
                        'Plastic Section modulus',
                        'Z_pz(cm³)',
                        'Z_py(cm³)',
                        'Elastic Section modulus',
                        'Z_zz(cm³)',
                        'Z_yy(cm³)',
                        ]
        values=list(reportsummary['Section Properties'].values())
        Properties=[
                        (labels[0],values[0]),
                        (labels[1],""),
                        (labels[2],values[1]),
                        (labels[3],values[2]),
                        (labels[4],""),
                        (labels[5],values[3]),
                        (labels[6],values[4]),
                        (labels[7],""),
                        (labels[8],values[5]),
                        (labels[9],values[6]),
                        (labels[10],""),
                        (labels[11],values[7]),
                        (labels[12],values[8]),
                        (labels[13],""),
                        (labels[14],values[9]),
                        (labels[15],values[10]),

                ]

        with doc.create(Section('Section Properties')):
            with doc.create(Tabularx('|X|X|',row_height=1.2)) as table:
                for ppty in Properties:
                    table.add_hline()
                    table.add_row((bold(ppty[0]),ppty[1]))
                table.add_hline()
        doc.append(NewPage())


        if (not 'TRAVIS' in os.environ):
            with doc.create(Section('3D View')):
                with doc.create(Figure(position='h!')) as view_3D:
                    view_3dimg_path = rel_path + Disp_3d_image
                    # view_3D.add_image(filename=view_3dimg_path, width=NoEscape(r'\linewidth'))
                    view_3D.add_image(filename=view_3dimg_path)

                    view_3D.add_caption('3D View')   
        try:            
            doc.generate_pdf(filename, compiler='pdflatex', clean_tex=False)
        except:
            pass