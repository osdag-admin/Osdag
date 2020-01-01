from design_type.connection.shear_connection import ShearConnection
from utils.common.component import *
from Common import *
from utils.common.load import Load
import yaml
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
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import pickle

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
