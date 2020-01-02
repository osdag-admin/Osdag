from design_type.connection.shear_connection import ShearConnection

from utils.common.component import Bolt, Plate, Weld
# from gui.ui_summary_popup import Ui_Dialog
from gui.ui_template import Ui_ModuleWindow
from utils.common.component import *
from Common import *
from utils.common.load import Load
import yaml
from design_report.reportGenerator import save_html
import os
import shutil
import logging
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QMessageBox
import pickle
import pdfkit
import configparser
import cairosvg
from gui.ui_template import Ui_ModuleWindow

#from ...gui.newnew import Ui_Form
#newnew_object = Ui_Form()

connectivity = "column_flange_beam_web"
supporting_member_section = "HB 400"
supported_member_section = "MB 300"
fy = 250.0
fu = 410.0
shear_force = 100.0
axial_force=100.0
bolt_diameter = 24.0
bolt_type = "friction_grip"
bolt_grade = 8.8
plate_thickness = 10.0
weld_size = 6
material_grade = "E 250 (Fe 410 W)B"
material = Material(material_grade)

logger = None


def module_setup():
    global logger
    logger = logging.getLogger("osdag.finPlateCalc")
module_setup()

# def set_osdaglogger():
#     global logger
#     if logger is None:
#
#         logger = logging.getLogger("osdag")
#     else:
#         for handler in logger.handlers[:]:
#             logger.removeHandler(handler)
#
#     logger.setLevel(logging.DEBUG)
#
#     # create the logging file handler
#     fh = logging.FileHandler("Connections/Shear/Finplate/fin.log", mode="a")
#
#     # ,datefmt='%a, %d %b %Y %H:%M:%S'
#     # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
#     formatter = logging.Formatter('''
#     <div  class="LOG %(levelname)s">
#         <span class="DATE">%(asctime)s</span>
#         <span class="LEVEL">%(levelname)s</span>
#         <span class="MSG">%(message)s</span>
#     </div>''')
#     formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)


def desired_location(self, filename, base_type):
    if base_type == ".svg":
        cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.maincontroller.folder), "images_html",
                                                                  "cmpylogoExtendEndplate.svg"))
    else:
        shutil.copyfile(filename,
                        os.path.join(str(self.maincontroller.folder), "images_html", "cmpylogoExtendEndplate.png"))

def saveUserProfile(self):
    inputData = self.get_report_summary()
    filename, _ = QFileDialog.getSaveFileName(self, 'Save Files',
                                              os.path.join(str(self.maincontroller.folder), "Profile"), '*.txt')
    if filename == '':
        flag = False
        return flag
    else:
        infile = open(filename, 'w')
        pickle.dump(inputData, infile)
        infile.close()


def getPopUpInputs(self):
    input_summary = {}
    input_summary["ProfileSummary"] = {}
    input_summary["ProfileSummary"]["CompanyName"] = str(self.ui.lineEdit_companyName.text())
    input_summary["ProfileSummary"]["CompanyLogo"] = str(self.ui.lbl_browse.text())
    input_summary["ProfileSummary"]["Group/TeamName"] = str(self.ui.lineEdit_groupName.text())
    input_summary["ProfileSummary"]["Designer"] = str(self.ui.lineEdit_designer.text())

    input_summary["ProjectTitle"] = str(self.ui.lineEdit_projectTitle.text())
    input_summary["Subtitle"] = str(self.ui.lineEdit_subtitle.text())
    input_summary["JobNumber"] = str(self.ui.lineEdit_jobNumber.text())
    input_summary["AdditionalComments"] = str(self.ui.txt_additionalComments.toPlainText())
    input_summary["Client"] = str(self.ui.lineEdit_client.text())


def useUserProfile(self):
    filename, _ = QFileDialog.getOpenFileName(self, 'Open Files',
                                              os.path.join(str(self.maincontroller.folder), "Profile"),
                                              "All Files (*)")
    if os.path.isfile(filename):
        outfile = open(filename, 'r')
        reportsummary = pickle.load(outfile)
        self.ui.lineEdit_companyName.setText(reportsummary["ProfileSummary"]['CompanyName'])
        self.ui.lbl_browse.setText(reportsummary["ProfileSummary"]['CompanyLogo'])
        self.ui.lineEdit_groupName.setText(reportsummary["ProfileSummary"]['Group/TeamName'])
        self.ui.lineEdit_designer.setText(reportsummary["ProfileSummary"]['Designer'])
    else:
        pass


class FinPlateConnection(ShearConnection):


    def __init__(self):
        super(FinPlateConnection, self).__init__()


    def input_values(self, existingvalues={}):

        options_list = []

        if KEY_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_CONN]
        else:
            existingvalue_key_conn = ''

        if KEY_SUPTNGSEC in existingvalues:
           existingvalue_key_suptngsec = existingvalues[KEY_SUPTNGSEC]
        else:
            existingvalue_key_suptngsec = ''

        if KEY_SUPTDSEC in existingvalues:
            existingvalue_key_suptdsec = existingvalues[KEY_SUPTDSEC]
        else:
            existingvalue_key_suptdsec = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_SHEAR in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_SHEAR]
        else:
            existingvalue_key_versh = ''

        if KEY_AXIAL in existingvalues:
            existingvalue_key_axial = existingvalues[KEY_AXIAL]
        else:
            existingvalue_key_axial = ''

        if KEY_D in existingvalues:
            existingvalue_key_d = existingvalues[KEY_D]
        else:
            existingvalue_key_d = ''

        if KEY_TYP in existingvalues:
            existingvalue_key_typ = existingvalues[KEY_TYP]
        else:
            existingvalue_key_typ = ''

        if KEY_GRD in existingvalues:
            existingvalue_key_grd = existingvalues[KEY_GRD]
        else:
            existingvalue_key_grd = ''

        if KEY_PLATETHK in existingvalues:
            existingvalue_key_platethk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_platethk = ''

        t16 = (KEY_MODULE, KEY_DISP_FINPLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN)
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, VALUES_COLSEC)
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, VALUES_BEAMSEC)
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None)
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None)
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None)
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D)
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        options_list.append(t14)

        return options_list


    @staticmethod
    def pltthk_customized():
        a = VALUES_PLATETHK_CUSTOMIZED
        return a

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t2 = (KEY_PLATETHK, self.pltthk_customized)
        list1.append(t2)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        return list1

    def fn_conn_suptngsec_lbl(self):

        if self in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        elif self in VALUES_CONN_2:
            return KEY_DISP_PRIBM
        else:
            return ''

    def fn_conn_suptdsec_lbl(self):

        if self in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        elif self in VALUES_CONN_2:
            return KEY_DISP_SECBM
        else:
            return ''

    def fn_conn_suptngsec(self):

        if self in VALUES_CONN_1:
            return VALUES_COLSEC
        elif self in VALUES_CONN_2:
            return VALUES_PRIBM
        else:
            return []

    def fn_conn_suptdsec(self):

        if self in VALUES_CONN_1:
            return VALUES_BEAMSEC
        elif self in VALUES_CONN_2:
            return VALUES_SECBM
        else:
            return []

    def fn_conn_image(self):
        if self == VALUES_CONN[0]:
            return './ResourceFiles/images/fin_cf_bw.png'
        elif self == VALUES_CONN[1]:
            return './ResourceFiles/images/fin_cw_bw.png'
        elif self in VALUES_CONN_2:
            return './ResourceFiles/images/fin_beam_beam.png'
        else:
            return''

    def input_value_changed(self):

        lst = []

        t1 = (KEY_CONN, KEY_SUPTNGSEC , TYPE_LABEL,self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_COMBOBOX, self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = (KEY_CONN, KEY_SUPTDSEC , TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = (KEY_CONN, KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = (KEY_CONN, KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        return lst

    def to_get_d(self, my_d):
        # self.set_connectivity(self, my_d[KEY_CONN])
        # self.set_supporting_section(self,my_d[KEY_SUPTNGSEC])
        # self.set_supported_section(self,my_d[KEY_SUPTDSEC])
        # self.set_material(self,my_d[KEY_MATERIAL])
        # self.set_shear(self, my_d[KEY_SHEAR])
        # self.set_axial(self,my_d[KEY_AXIAL])
        # self.set_bolt_dia(self,my_d[KEY_D])
        # self.set_bolt_type(self,my_d[KEY_TYP])
        # self.set_bolt_grade(self,my_d[KEY_GRD])
        # self.set_plate_thk(self,my_d[KEY_PLATETHK])
        # self.weld = Weld(weld_size)
        # self.weld_size_list = []
        print(my_d)
        self.connectivity = my_d[KEY_CONN]

        if self.connectivity in VALUES_CONN_1:
            self.supporting_section = Column(designation=my_d[KEY_SUPTNGSEC], material_grade=my_d[KEY_MATERIAL])
        else:
            self.supporting_section = Beam(designation=my_d[KEY_SUPTNGSEC], material_grade=my_d[KEY_MATERIAL])


        self.supported_section = Beam(designation=my_d[KEY_SUPTDSEC], material_grade=my_d[KEY_MATERIAL])
        self.bolt = Bolt(grade=my_d[KEY_GRD], diameter=my_d[KEY_D], bolt_type=my_d[KEY_TYP],
                         material_grade=material_grade)
        self.load = Load(shear_force=my_d[KEY_SHEAR], axial_force=my_d[KEY_AXIAL])
        self.plate = Plate(thickness=my_d[KEY_PLATETHK], material_grade=my_d[KEY_MATERIAL])

        print(self.connectivity)
        print(self.supporting_section)
        print(self.supported_section)
        print(self.bolt)
        print(self.load)
        print(self.plate)

    def get_weld(self):
        return self.weld

    def set_weld(self, weld):
        self.weld = weld

    def set_weld_by_size(self, weld_size, length=0, material=Material(material_grade)):
        self.weld = Weld(weld_size,length,material)

    def call_designreport(self, fileName, report_summary,folder):
        self.alist = {'Designation': 'MB 500', 'Mass': 86.9, 'Area': 111.0, 'D': 500.0, 'B': 180.0, 'tw': 10.2, 'T': 17.2, 'FlangeSlope': 98, 'R1': 17.0, 'R2': 8.5, 'Iz': 45228.0, 'Iy': 1320.0, 'rz': 20.2, 'ry': 3.5, 'Zz': 1809.1, 'Zy': 147.0, 'Zpz': 2074.8, 'Zpy': 266.7, 'Source': 'IS808_Rev', 'Bolt': {'Diameter (mm)': '24', 'Grade': '8.8', 'Type': 'Friction Grip Bolt'}, 'Weld': {'Size (mm)': '12'}, 'Member': {'BeamSection': 'MB 500', 'ColumSection': 'UC 305 x 305 x 97', 'Connectivity': 'Column flange-Beam web', 'fu (MPa)': '410', 'fy (MPa)': '250'}, 'Plate': {'Thickness (mm)': '12', 'Height (mm)': '', 'Width (mm)': ''}, 'Load': {'ShearForce (kN)': '140'}, 'Connection': 'Finplate', 'bolt': {'bolt_hole_type': 'Standard', 'bolt_hole_clrnce': 2, 'bolt_fu': 800.0, 'slip_factor': 0.3}, 'weld': {'typeof_weld': 'Shop weld', 'safety_factor': 1.25, 'fu_overwrite': '410'}, 'detailing': {'typeof_edge': 'a - Sheared or hand flame cut', 'min_edgend_dist': 1.7, 'gap': 10.0, 'is_env_corrosive': 'No'}, 'design': {'design_method': 'Limit State Design'}}
        self.result = {'Bolt': {'status': True, 'shearcapacity': 47.443, 'bearingcapacity': 'N/A', 'boltcapacity': 47.443, 'numofbolts': 3, 'boltgrpcapacity': 142.33, 'numofrow': 3, 'numofcol': 1, 'pitch': 96.0, 'edge': 54.0, 'enddist': 54.0, 'gauge': 0.0, 'bolt_fu': 800.0, 'bolt_dia': 24, 'k_b': 0.519, 'beam_w_t': 10.2, 'web_plate_t': 12.0, 'beam_fu': 410.0, 'shearforce': 140.0, 'dia_hole': 26}, 'Weld': {'thickness': 10, 'thicknessprovided': 12.0, 'resultantshear': 434.557, 'weldstrength': 1590.715, 'weld_fu': 410.0, 'effectiveWeldlength': 276.0}, 'Plate': {'minHeight': 300.0, 'minWidth': 118.0, 'plateedge': 64.0, 'externalmoment': 8.96, 'momentcapacity': 49.091, 'height': 300.0, 'width': 118.0, 'blockshear': 439.837, 'web_plate_fy': 250.0, 'platethk': 12.0, 'beamdepth': 500.0, 'beamrootradius': 17.0, 'colrootradius': 15.2, 'beamflangethk': 17.2, 'colflangethk': 15.4}}
        # print("resultobj", self.result)
        # self.column_data = self.fetchColumnPara()
        # self.beam_data = self.fetchBeamPara()
        save_html(self.result, self.alist, fileName, report_summary, folder)



    def save_design(self, report_summary,folder):

        filename = os.path.join(str(folder), "images_html", "Html_Report.html")
        file_name = str(filename)
        self.call_designreport(file_name, report_summary)

        config = configparser.ConfigParser()
        config.readfp(open(r'Osdag.config'))
        wkhtmltopdf_path = config.get('wkhtml_path', 'path1')

        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        options = {
            'margin-bottom': '10mm',
            'footer-right': '[page]'
        }
        file_type = "PDF(*.pdf)"
        fname, _ = QFileDialog.getSaveFileName(self, "Save File As", folder + "/", file_type)
        fname = str(fname)
        flag = True
        if fname == '':
            flag = False
            return flag
        else:
            pdfkit.from_file(filename, fname, configuration=config, options=options)
            QMessageBox.about(self, 'Information', "Report Saved")


# fin_plate_input = FinPlateConnectionInput(connectivity, supporting_member_section, supported_member_section, material)


# fin_plate_input = FinPlateConnection(connectivity, supporting_member_section, supported_member_section, fu, fy,
#                                      shear_force, axial_force, bolt_diameter, bolt_type, bolt_grade,
#                                      weld_size, plate_thickness,Ui_ModuleWindow)
# bolt = Bolt(grade=bolt_grade, diameter=bolt_diameter, bolt_type=bolt_type, material=material)
# load = Load(shear_force=shear_force)
# plate = Plate(thickness=plate_thickness, material=material)
# weld = Weld(size=weld_size, material=material)
#
# fin_plate_input.bolt = bolt
# fin_plate_input.load = load
# fin_plate_input.plate = plate
# fin_plate_input.weld = weld

# print(fin_plate_input.bolt)

# with open("filename", 'w') as out_file:
#     yaml.dump(fin_plate_input, out_file)

        
    def warn_text(self,key, my_d):
        old_col_section = get_oldcolumncombolist()
        old_beam_section = get_oldbeamcombolist()

        if my_d[KEY_SUPTNGSEC] in old_col_section or my_d[KEY_SUPTDSEC] in old_beam_section:
            del_data = open('logging_text.log', 'w')
            del_data.truncate()
            del_data.close()
            logging.basicConfig(format='%(asctime)s %(message)s', filename='logging_text.log',level=logging.DEBUG)
            logging.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")
            with open('logging_text.log') as file:
                data = file.read()
                file.close()
            # file = open('logging_text.log', 'r')
            # # This will print every line one by one in the file
            # for each in file:
            #     print(each)
            key.setText(data)
        else:
            key.setText("")


    # def set_axial(self, axial):
    #     self.axial = axial
    #
    # def set_plate_thk(self, plate_thk):
    #     self.plate_thk = plate_thk
    #
    # def set_supporting_section(self, supporting_section):
    #     self.supporting_section = supporting_section
    #
    # def set_supported_section(self, supported_section):
    #     self.supported_section = supported_section
    #
    # def set_material(self, material=Material(material_grade)):
    #     self.material = Material(material)
    #     print(self.material)
    #
    # def set_weld_by_size(self, weld_size, length=0, material=Material(material_grade)):
    #     self.weld = Weld(weld_size,length,material)
    #
    # def get_shear_capacity(self):
    #     shear_capacity = self.shear

    # fin_plate_input = FinPlateConnectionInput(connectivity, supporting_member_section, supported_member_section, material)

# fin_plate_input = FinPlateConnection(FinPlateConnection.connectivity, supporting_member_section, supported_member_section, fu, fy,

# fin_plate_input = FinPlateConnection(FinPlateConnection.connectivity, supporting_member_section,
#                                       supported_member_section, fu, fy,

#                                      shear_force, axial_force, bolt_diameter, bolt_type, bolt_grade,
#                                      weld_size, plate_thickness)
# bolt = Bolt(grade=bolt_grade, diameter=bolt_diameter, bolt_type=bolt_type, material_grade=material_grade)
# load = Load(shear_force=shear_force)
# plate = Plate(thickness=plate_thickness, material_grade=material_grade)
# weld = Weld(size=weld_size, material_grade=material_grade)
# FinPlateConnection.to_get_d(design_dictionary)
# fin_plate_input.bolt = bolt
# fin_plate_input.load = load
# fin_plate_input.plate = plate
# fin_plate_input.weld = weld
#
# print(FinPlateConnection.to_get_d().bolt)
#
# with open("filename", 'w') as out_file:
#     yaml.dump(fin_plate_input, out_file)
#
#
# # print(fin_plate_input.bolt)
#
# with open("filename", 'w') as out_file:
#     yaml.dump(fin_plate_input, out_file)

