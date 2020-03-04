from design_type.connection.shear_connection import ShearConnection
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from utils.common.component import Bolt, Plate, Weld
# from gui.ui_summary_popup import Ui_Dialog
from utils.common.component import *
# from cad.common_logic import CommonDesignLogic
from utils.common.material import *
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
from main import Main
import cairosvg
from io import StringIO

#from ...gui.newnew import Ui_Form
#newnew_object = Ui_Form()

# connectivity = "column_flange_beam_web"
# supporting_member_section = "HB 400"
# supported_member_section = "MB 300"
# fy = 250.0
# fu = 410.0
# shear_force = 100.0
# axial_force=100.0
# bolt_diameter = 24.0
# bolt_type = "friction_grip"
# bolt_grade = 8.8
# plate_thickness = 10.0
# weld_size = 6
# material_grade = "E 250 (Fe 410 W)B"
# material = Material(material_grade)


class Tension(Main):

    def __init__(self):
        super(Tension, self).__init__()


        self.design_status = False

    def set_osdaglogger(key):

        """
        Function to set Logger for Tension Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # handler.setLevel(logging.INFO)
        # formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        handler = OurLog(key)
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def module_name(self):
        return KEY_DISP_TENSION

    def customized_input(self):

        c_lst = []

        t1 = (KEY_SECSIZE, self.fn_profile_section)
        c_lst.append(t1)
        t2 = (KEY_GRD, self.grdval_customized)
        c_lst.append(t2)
        t3 = (KEY_D, self.diam_bolt_customized)
        c_lst.append(t3)
        t4 = (KEY_PLATETHK, self.plate_thick_customized)
        c_lst.append(t4)

        return c_lst

    def fn_profile_section(self):
        if self == 'Beams':
            return connectdb("Beams", call_type= "popup")
        elif self == 'Columns':
            return connectdb("Columns", call_type= "popup")
        elif self in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return connectdb("Angles", call_type= "popup")
        elif self in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type= "popup")

    def tab_list(self):

        tabs = []

        t1 = (KEY_DISP_BEAMSEC, self.tab_beam_section)
        tabs.append(t1)

        return tabs

    @staticmethod
    def tab_beam_section():
        supported_section = []

        t1 = (KEY_SUPTDSEC_DESIGNATION, KEY_DISP_SUPTDSEC_DESIGNATION, TYPE_TEXTBOX, None)
        supported_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
        supported_section.append(t2)

        t3 = (KEY_SUPTDSEC_FU, KEY_DISP_SUPTDSEC_FU, TYPE_TEXTBOX, None)
        supported_section.append(t3)

        t4 = (KEY_SUPTDSEC_FY, KEY_DISP_SUPTDSEC_FY, TYPE_TEXTBOX, None)
        supported_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
        supported_section.append(t5)

        t6 = (KEY_SUPTDSEC_DEPTH, KEY_DISP_SUPTDSEC_DEPTH, TYPE_TEXTBOX, None)
        supported_section.append(t6)

        t7 = (KEY_SUPTDSEC_FLANGE_W, KEY_DISP_SUPTDSEC_FLANGE_W, TYPE_TEXTBOX, None)
        supported_section.append(t7)

        t8 = (KEY_SUPTDSEC_FLANGE_T, KEY_DISP_SUPTDSEC_FLANGE_T, TYPE_TEXTBOX, None)
        supported_section.append(t8)

        t9 = (KEY_SUPTDSEC_WEB_T, KEY_DISP_SUPTDSEC_WEB_T, TYPE_TEXTBOX, None)
        supported_section.append(t9)

        t10 = (KEY_SUPTDSEC_FLANGE_S, KEY_DISP_SUPTDSEC_FLANGE_S, TYPE_TEXTBOX, None)
        supported_section.append(t10)

        t11 = (KEY_SUPTDSEC_ROOT_R, KEY_DISP_SUPTDSEC_ROOT_R, TYPE_TEXTBOX, None)
        supported_section.append(t11)

        t12 = (KEY_SUPTDSEC_TOE_R, KEY_DISP_SUPTDSEC_TOE_R, TYPE_TEXTBOX, None)
        supported_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None)
        supported_section.append(t13)

        t14 = (KEY_SUPTDSEC_TYPE, KEY_DISP_SUPTDSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
        supported_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None)
        supported_section.append(t18)

        t15 = (KEY_SUPTDSEC_MOD_OF_ELAST, KEY_SUPTDSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
        supported_section.append(t15)

        t16 = (KEY_SUPTDSEC_MOD_OF_RIGID, KEY_SUPTDSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
        supported_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
        supported_section.append(t17)

        t18 = (KEY_SUPTDSEC_MASS, KEY_DISP_SUPTDSEC_MASS, TYPE_TEXTBOX, None)
        supported_section.append(t18)

        t19 = (KEY_SUPTDSEC_SEC_AREA, KEY_DISP_SUPTDSEC_SEC_AREA, TYPE_TEXTBOX, None)
        supported_section.append(t19)

        t20 = (KEY_SUPTDSEC_MOA_LZ, KEY_DISP_SUPTDSEC_MOA_LZ, TYPE_TEXTBOX, None)
        supported_section.append(t20)

        t21 = (KEY_SUPTDSEC_MOA_LY, KEY_DISP_SUPTDSEC_MOA_LY, TYPE_TEXTBOX, None)
        supported_section.append(t21)

        t22 = (KEY_SUPTDSEC_ROG_RZ, KEY_DISP_SUPTDSEC_ROG_RZ, TYPE_TEXTBOX, None)
        supported_section.append(t22)

        t23 = (KEY_SUPTDSEC_ROG_RY, KEY_DISP_SUPTDSEC_ROG_RY, TYPE_TEXTBOX, None)
        supported_section.append(t23)

        t24 = (KEY_SUPTDSEC_EM_ZZ, KEY_DISP_SUPTDSEC_EM_ZZ, TYPE_TEXTBOX, None)
        supported_section.append(t24)

        t25 = (KEY_SUPTDSEC_EM_ZY, KEY_DISP_SUPTDSEC_EM_ZY, TYPE_TEXTBOX, None)
        supported_section.append(t25)

        t26 = (KEY_SUPTDSEC_PM_ZPZ, KEY_DISP_SUPTDSEC_PM_ZPZ, TYPE_TEXTBOX, None)
        supported_section.append(t26)

        t27 = (KEY_SUPTDSEC_PM_ZPY, KEY_DISP_SUPTDSEC_PM_ZPY, TYPE_TEXTBOX, None)
        supported_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None)
        supported_section.append(t28)

        t29 = (KEY_SUPTDSEC_SOURCE, KEY_DISP_SUPTDSEC_SOURCE, TYPE_TEXTBOX, None)
        supported_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None)
        supported_section.append(t30)

        t31 = (KEY_SUPTDSEC_POISSON_RATIO, KEY_DISP_SUPTDSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
        supported_section.append(t31)

        t32 = (KEY_SUPTDSEC_THERMAL_EXP, KEY_DISP_SUPTDSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
        supported_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        supported_section.append(t33)

        return supported_section

    def input_values(self, existingvalues={}):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair
        self.module = KEY_DISP_TENSION

        options_list = []

        # if KEY_SECTION in existingvalues:
        #     existingvalue_key_section = existingvalues[KEY_SECTION]
        # else:
        #     existingvalue_key_section = ''

        # if KEY_SUPTNGSEC in existingvalues:
        #    existingvalue_key_suptngsec = existingvalues[KEY_SUPTNGSEC]
        # else:
        #     existingvalue_key_suptngsec = ''
        #
        # if KEY_SUPTDSEC in existingvalues:
        #     existingvalue_key_suptdsec = existingvalues[KEY_SUPTDSEC]
        # else:
        #     existingvalue_key_suptdsec = ''

        if KEY_LOCATION in existingvalues:
            existingvalue_key_location = existingvalues[KEY_LOCATION]
        else:
            existingvalue_key_location = ''

        if KEY_SEC_PROFILE in existingvalues:
            existingvalue_key_sec_profile = existingvalues[KEY_SEC_PROFILE]
        else:
            existingvalue_key_sec_profile = ''

        if KEY_SECSIZE in existingvalues:
            existingvalue_key_sec_size = existingvalues[KEY_SECSIZE]
        else:
            existingvalue_key_sec_size = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        # if KEY_SHEAR in existingvalues:
        #     existingvalue_key_versh = existingvalues[KEY_SHEAR]
        # else:
        #     existingvalue_key_versh = ''

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

        # if KEY_PLATETHK in existingvalues:
        #     existingvalue_key_platethk = existingvalues[KEY_PLATETHK]
        # else:
        #     existingvalue_key_platethk = ''

        t16 = (KEY_MODULE, KEY_DISP_TENSION, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, existingvalue_key_sec_profile, VALUES_SEC_PROFILE_2)
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, "./ResourceFiles/images/fin_cf_bw.png")
        options_list.append(t15)

        t3 = (KEY_LOCATION, KEY_DISP_LOCATION, TYPE_COMBOBOX, existingvalue_key_location, VALUES_LOCATION)
        options_list.append(t3)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_sec_size, ['All','Customized'])
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

        # t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None)
        # options_list.append(t7)

        t7 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None)
        options_list.append(t7)

        t8 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None)
        options_list.append(t8)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D)
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        options_list.append(t12)

        # t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        # options_list.append(t13)

        # t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        # options_list.append(t14)

        return options_list

    def spacing(self, status):

        spacing = []

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair

        out_list = []

        t1 = (None, DISP_TITLE_TENSION_SECTION, TYPE_TITLE, None)
        out_list.append(t1)

        t2 = (KEY_DESIGNATION, KEY_DISP_DESIGNATION, TYPE_TEXTBOX,
              self.section_size_1.designation if flag else '')
        out_list.append(t2)

        t3 = (KEY_TENSION_YIELDCAPACITY, KEY_DISP_TENSION_YIELDCAPACITY, TYPE_TEXTBOX, self.section_size_1.tension_yielding_capacity if flag else '')
        out_list.append(t3)

        t4 = (KEY_TENSION_RUPTURECAPACITY, KEY_DISP_TENSION_RUPTURECAPACITY, TYPE_TEXTBOX,
              self.section_size_1.tension_rupture_capacity if flag else '')
        out_list.append(t4)

        t5 = (KEY_TENSION_BLOCKSHEARCAPACITY, KEY_DISP_TENSION_BLOCKSHEARCAPACITY, TYPE_TEXTBOX,
              self.section_size_1.block_shear_capacity_axial if flag else '')
        out_list.append(t5)

        t6 = (KEY_TENSION_CAPACITY, KEY_DISP_TENSION_CAPACITY, TYPE_TEXTBOX,
              self.section_size_1.tension_capacity if flag else '')
        out_list.append(t6)

        t7 = (KEY_EFFICIENCY, KEY_DISP_EFFICIENCY, TYPE_TEXTBOX,
               " great" if flag else '')
        out_list.append(t7)

        t8 = (None, DISP_TITLE_BOLT_CAPACITY, TYPE_TITLE, None)
        out_list.append(t8)

        t9 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_diameter_provided if flag else '')
        out_list.append(t9)

        t10 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_grade_provided if flag else '')

        out_list.append(t10)

        t11 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  round(self.bolt.bolt_shear_capacity/1000,2) if flag else '')
        out_list.append(t11)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
                pass
            else:
                bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '')
        out_list.append(t5)

        t13 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX, round(self.bolt.bolt_capacity/1000,2) if flag else '')
        out_list.append(t13)

        t14 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX, round(self.plate.bolt_force / 1000, 2) if flag else '')
        out_list.append(t14)

        t15 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.plate.bolt_line if flag else '')
        out_list.append(t15)

        t16 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.plate.bolts_one_line if flag else '')
        out_list.append(t16)

        t17 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing])
        out_list.append(t17)

        t18 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None)
        out_list.append(t18)

        t19 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.plate.thickness_provided if flag else '')
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.plate.height if flag else '')
        out_list.append(t20)

        t21 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_LENGTH, TYPE_TEXTBOX, self.plate.length if flag else '')
        out_list.append(t21)

        return out_list

    # def loadDesign_inputs(self, window, op_list, data, new):
    #     fileName, _ = QFileDialog.getOpenFileName(window, "Open Design", os.path.join(str(' '), ''), "InputFiles(*.osi)")
    #     if not fileName:
    #         return
    #     try:
    #         in_file = str(fileName)
    #         with open(in_file, 'r') as fileObject:
    #             uiObj = yaml.load(fileObject)
    #         module = uiObj[KEY_MODULE]
    #
    #         if module == KEY_DISP_FINPLATE:
    #             self.setDictToUserInputs(window, uiObj, op_list, data, new)
    #         else:
    #             QMessageBox.information(window, "Information",
    #                                 "Please load the appropriate Input")
    #
    #             return
    #     except IOError:
    #         QMessageBox.information(window, "Unable to open file",
    #                                 "There was an error opening \"%s\"" % fileName)
    #         return
    #
    #     # Function for loading inputs from a file to Ui
    #
    # '''
    # @author: Umair
    # '''
    #
    # def setDictToUserInputs(self, uiObj, op_list, data, new):
    #     for op in op_list:
    #         key_str = op[0]
    #         key = self.dockWidgetContents.findChild(QtWidgets.QWidget, key_str)
    #         if op[2] == TYPE_COMBOBOX:
    #             index = key.findText(uiObj[key_str], QtCore.Qt.MatchFixedString)
    #             if index >= 0:
    #                 key.setCurrentIndex(index)
    #         elif op[2] == TYPE_TEXTBOX:
    #             key.setText(uiObj[key_str])
    #         elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
    #             for n in new:
    #                 if n[0] == key_str:
    #                     if uiObj[key_str] != n[1]():
    #                         data[key_str + "_customized"] = uiObj[key_str]
    #                         key.setCurrentIndex(1)
    #                     else:
    #                         pass
    #         else:
    #             pass

    # def func_for_validation(self, window, design_dictionary):
    #     self.design_status = False
    #     flag = False
    #     flag1 = False
    #     option_list = self.input_values(self)
    #     missing_fields_list = []
    #     for option in option_list:
    #         if option[2] == TYPE_TEXTBOX:
    #             if design_dictionary[option[0]] == '':
    #                 missing_fields_list.append(option[1])
    #         elif option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
    #             val = option[4]
    #             if design_dictionary[option[0]] == val[0]:
    #                 missing_fields_list.append(option[1])
    #         elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
    #             if design_dictionary[option[0]] == []:
    #                 missing_fields_list.append(option[1])
    #         # elif option[2] == TYPE_MODULE:
    #         #     if design_dictionary[option[0]] == "Fin Plate":
    #
    #     # if design_dictionary[KEY_CONN] == 'Beam-Beam':
    #     #     primary = design_dictionary[KEY_SUPTNGSEC]
    #     #     secondary = design_dictionary[KEY_SUPTDSEC]
    #     #     conn = sqlite3.connect(PATH_TO_DATABASE)
    #     #     cursor = conn.execute("SELECT D FROM BEAMS WHERE Designation = ( ? ) ", (primary,))
    #     #     lst = []
    #     #     rows = cursor.fetchall()
    #     #     for row in rows:
    #     #         lst.append(row)
    #     #     p_val = lst[0][0]
    #     #     cursor2 = conn.execute("SELECT D FROM BEAMS WHERE Designation = ( ? )", (secondary,))
    #     #     lst1 = []
    #     #     rows1 = cursor2.fetchall()
    #     #     for row1 in rows1:
    #     #         lst1.append(row1)
    #     #     s_val = lst1[0][0]
    #     #     if p_val <= s_val:
    #     #         QMessageBox.about(window, 'Information',
    #     #                           "Secondary beam depth is higher than clear depth of primary beam web "
    #     #                           "(No provision in Osdag till now)")
    #     #     else:
    #     #         flag1 = True
    #     # else:
    #     #     flag1 = True
    #
    #     if len(missing_fields_list) > 0:
    #         QMessageBox.information(window, "Information",
    #                                 self.generate_missing_fields_error_string(self, missing_fields_list))
    #         # flag = False
    #     else:
    #         flag = True
    #
    #     if flag and flag1:
    #         self.set_input_values(self, design_dictionary)
    #     else:
    #         pass

    def func_for_validation(self, window, design_dictionary):
        self.design_status = False

        flag = False
        option_list = self.input_values(self)
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] not in [KEY_SEC_PROFILE, KEY_END1, KEY_END2]:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) > 0:
            QMessageBox.information(window, "Information",
                                    self.generate_missing_fields_error_string(self, missing_fields_list))
            # flag = False
        else:
            flag = True

        if flag:
            self.set_input_values(self, design_dictionary)
            print(design_dictionary)
        else:
            pass

    def generate_missing_fields_error_string(self, missing_fields_list):
        """
        Args:
            missing_fields_list: list of fields that are not selected or entered
        Returns:
            error string that has to be displayed
        """
        # The base string which should be displayed
        information = "Please input the following required field"
        if len(missing_fields_list) > 1:
            # Adds 's' to the above sentence if there are multiple missing input fields
            information += "s"
        information += ": "
        # Loops through the list of the missing fields and adds each field to the above sentence with a comma

        for item in missing_fields_list:
            information = information + item + ", "

        # Removes the last comma
        information = information[:-2]
        information += "."

        return information

    def warn_text(self):
      
        """
        Function to give logger warning when any old value is selected from Column and Beams table.
        """

        # @author Arsil Zunzunia
        global logger
        red_list = red_list_function()
        if self.supported_section.designation in red_list or self.supporting_section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def set_input_values(self, design_dictionary):

        super(Tension,self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.sizelist = design_dictionary[KEY_SECSIZE]
        self.plate_thickness = [3,4,6,8,10,12,16,20,24,28,30,32,36,40]
        # print(self.sizelist)

        # print(self.bolt)
        self.load = Load(shear_force=None, axial_force=design_dictionary.get(KEY_AXIAL))

        self.plate = Plate(thickness=self.plate_thickness,
                           material_grade=design_dictionary[KEY_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        # self.weld = Weld(size=10, length= 100, material_grade=design_dictionary[KEY_MATERIAL])
        print("input values are set. Doing preliminary member checks")
        self.i = 0

        self.initial_member_capacity(self,design_dictionary)


    def select_section(self, design_dictionary, selectedsize):
        if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles', 'Star Angles']:
            self.section_size = Angle(designation=selectedsize, material_grade=design_dictionary[KEY_MATERIAL])
        elif design_dictionary[KEY_SEC_PROFILE] in ['Channels', 'Back to Back Channels']:
            self.section_size = Channel(designation=selectedsize, material_grade=design_dictionary[KEY_MATERIAL])
        else:
            pass

        return self.section_size

    def max_force(self, design_dictionary):
        if design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Angles', 'Star Angles']:
            self.section_size_max = Angle(designation = "100 100 x 15", material_grade=design_dictionary[KEY_MATERIAL])

        elif design_dictionary[KEY_SEC_PROFILE] == 'Channels':
            self.section_size_max = Channel(designation="MCP 400", material_grade=design_dictionary[KEY_MATERIAL])
            # self.area = self.section_size_max.area
            self.section_size_max.tension_member_yielding(A_g = (self.section_size_max.area*100) , F_y = self.section_size_max.fy)
        elif design_dictionary[KEY_SEC_PROFILE] ==  'Back to Back Channels':
            self.section_size_max = Channel(designation="MCP 400", material_grade=design_dictionary[KEY_MATERIAL])
            # self.area = self.section_size_max.area
            self.max_member_force =  2* self.section_size_max.tension_member_yielding(A_g = (self.section_size_max.area*100) , F_y = self.section_size_max.fy)

        return self.section_size_max.tension_yielding_capacity


    def initial_member_capacity(self,design_dictionary,previous_size = None):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        # if self.connectivity in VALUES_CONN_1:
        #     if self.supported_section.build == "Rolled":
        #         length = self.supported_section.depth
        #     else:
        #         length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        # else:
        #     length = self.supported_section.depth - 50.0  # TODO: Subtract notch height for beam-beam connection
        #
        # self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        min_yield = 0
        # if previous_size != None:
        #     self.section_size_prev = self.select_section(self, design_dictionary, previous_size)
        #     self.cross_area_prev = self.section_size_prev.area * 100
        # else:
        #     pass

        max_force = self.max_force(self, design_dictionary)
        for selectedsize in self.sizelist:
            self.section_size = self.select_section(self,design_dictionary,selectedsize)
            self.cross_area = self.section_size.area * 100
            if previous_size != None:
                self.section_size_prev = self.select_section(self, design_dictionary, previous_size)
                self.cross_area_prev = self.section_size_prev.area * 100
            else:
                self.cross_area_prev = 0
            if self.cross_area > self.cross_area_prev or previous_size == None:
                self.section_size.tension_member_yielding(A_g = self.cross_area , F_y =self.section_size.fy)
                # print(self.section_size.tension_yielding_capacity)

                if (self.section_size.tension_yielding_capacity > self.load.axial_force):
                    min_yield_current = self.section_size.tension_yielding_capacity
                    if min_yield == 0:
                        min_yield = min_yield_current
                        self.section_size_1 = self.select_section(self, design_dictionary, selectedsize)
                        self.section_size_1.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
                        # self.select_bolt_dia(self, design_dictionary)

                    elif min_yield_current <= min_yield:
                        min_yield = min_yield_current
                        self.section_size_1 = self.select_section(self, design_dictionary, selectedsize)
                        self.section_size_1.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
                        # self.select_bolt_dia(self, design_dictionary)


                elif (self.load.axial_force > max_force) :
                    self.design_status = False
                    logger.error(" : Tension force exceeds tension capacity of maximum available member size")
                    break
                else:
                    pass

        if (self.load.axial_force > max_force):
            pass
        else:
             self.select_bolt_dia(self, design_dictionary)

        # print(self.load.axial_force)
        # print(min_yield)
        # print(self.section_size_1)




            # print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
            #       self.supported_section.tension_yielding_capacity, self.load.axial_force)
        #
        # if self.supported_section.shear_yielding_capacity > self.load.shear_force and \
        #         self.supported_section.tension_yielding_capacity > self.load.axial_force:
        #     print("preliminary member check is satisfactory. Doing bolt checks")
        #     self.select_bolt_dia(self)
        #
        # else:
        #     self.design_status = False
        #     logger.error(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
        #                    "than applied loads, Please select larger sections or decrease loads"
        #                     .format(self.supported_section.shear_yielding_capacity,
        #                             self.supported_section.tension_yielding_capacity))
        #     print("failed in preliminary member checks. Select larger sections or decrease loads")

    def closest(self, lst, K):

        return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]

    def select_bolt_dia(self,design_dictionary):
        self.min_plate_height = self.section_size_1.min_plate_height()
        self.max_plate_height = self.section_size_1.max_plate_height()
        # self.res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000
        self.res_force = self.load.axial_force*1000
        self.plate.thickness_provided = self.closest(self, self.plate_thickness,self.section_size_1.web_thickness)
        bolts_required_previous = 2
        bolt_diameter_previous = self.bolt.bolt_diameter[-1]
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        count = 0
        bolts_one_line = 1
        for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
            # print(self.bolt.bolt_diameter_provided)
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    connecting_plates_tk=[self.plate.thickness_provided,
                                                                          self.section_size.web_thickness])

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              connecting_plates_tk=[self.plate.thickness_provided,
                                                                    self.section_size.web_thickness],
                                              n_planes=1)

            self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                             web_plate_h_min=self.min_plate_height,
                                             web_plate_h_max=self.max_plate_height,
                                             bolt_capacity=self.bolt.bolt_capacity,
                                             min_edge_dist=self.bolt.min_edge_dist_round,
                                             min_gauge=self.bolt.min_gauge_round,
                                             max_spacing=self.bolt.max_spacing_round,
                                             max_edge_dist=self.bolt.max_edge_dist_round,
                                             shear_load=0,
                                             axial_load=self.load.axial_force * 1000, gap=self.plate.gap,
                                             shear_ecc=False)

            # self.plate.bolts_required = max(int(math.ceil(self.res_force / self.bolt.bolt_capacity)), 2)
            # [bolt_line, bolts_one_line, web_plate_h] = \
            #     self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height, self.plate.bolts_required,
            #                                         self.bolt.min_edge_dist_round, self.bolt.min_gauge_round)
            # # self.plate.bolts_required = bolt_line * bolts_one_line
            # print(1, self.plate.bolt_force, self.bolt.bolt_capacity, self.bolt.bolt_diameter_provided,
            #       self.plate.bolts_required, self.plate.bolts_one_line)
            if self.plate.design_status is True:
                if self.plate.bolts_required > bolts_required_previous and count >= 1:
                    self.bolt.bolt_diameter_provided = bolt_diameter_previous
                    self.plate.bolts_required = bolts_required_previous
                    self.plate.bolt_force = bolt_force_previous
                    break
                bolts_required_previous = self.plate.bolts_required
                bolt_diameter_previous = self.bolt.bolt_diameter_provided
                bolt_force_previous = self.plate.bolt_force
                count += 1
            else:
                pass
        bolt_capacity_req = self.bolt.bolt_capacity

        if self.plate.design_status is False:
            self.design_status = False
            logger.error(self.plate.reason)
        else:
            self.get_bolt_grade(self, design_dictionary)

        #     self.plate.bolts_required = max(int(math.ceil(self.res_force / self.bolt.bolt_capacity)), 2)
        #     [bolt_line, bolts_one_line, web_plate_h] = \
        #         self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height, self.plate.bolts_required,
        #                                             self.bolt.min_edge_dist_round, self.bolt.min_gauge_round)
        #     # print(bolts_one_line,"ggg")
        #     # print(bolt_line, "rrr")
        #     self.plate.bolts_required = bolt_line * bolts_one_line
        #     # print(1, self.res_force, self.bolt.bolt_capacity, self.bolt.bolt_diameter_provided, self.plate.bolts_required, bolts_one_line)
        #     if bolts_one_line >= 2:
        #         if self.plate.bolts_required > bolts_required_previous and count >= 1:
        #             self.bolt.bolt_diameter_provided = bolt_diameter_previous
        #             self.plate.bolts_required = bolts_required_previous
        #             break
        #         bolts_required_previous = self.plate.bolts_required
        #         bolt_diameter_previous = self.bolt.bolt_diameter_provided
        #         count += 1
        #
        # if bolts_one_line <2 and self.bolt.bolt_diameter_provided == 12:
        #     self.design_status = False
        #     logger.error(" : Bolted connection not possible")
        # elif bolts_one_line <2 and self.bolt.bolt_diameter_provided != 12:
        #     self.design_status = False
        #     logger.error(" : Select bolt of lower diameter")
        # else:
        #     self.design_status = True
        #     print(self.plate)
        #     print(self.bolt)
        #     self.get_bolt_grade(self,design_dictionary)

        # print(self.section_size)
        # print(self.load)

    def get_bolt_grade(self,design_dictionary):
        bolt_grade_previous = self.bolt.bolt_grade[-1]
        bolts_required_previous = self.plate.bolts_required
        for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
            count = 1
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    connecting_plates_tk=[self.plate.thickness_provided,
                                                                          self.section_size.web_thickness])

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              connecting_plates_tk=[self.plate.thickness_provided,
                                                                    self.section_size.web_thickness],
                                              n_planes=1)

            print(self.bolt.bolt_grade_provided, self.bolt.bolt_capacity, self.plate.bolt_force)

            bolt_capacity_reduced = self.plate.get_bolt_red(self.plate.bolts_one_line,
                                                            self.plate.gauge_provided, self.bolt.bolt_capacity,
                                                            self.bolt.bolt_diameter_provided)
            if bolt_capacity_reduced < self.plate.bolt_force and count >= 1:
                self.bolt.bolt_grade_provided = bolt_grade_previous
                break
            bolts_required_previous = self.plate.bolts_required
            bolt_grade_previous = self.bolt.bolt_grade_provided
            count += 1

        #     self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
        #                                      web_plate_h_min=self.min_plate_height,
        #                                      web_plate_h_max=self.max_plate_height,
        #                                      bolt_capacity=self.bolt.bolt_capacity,
        #                                      min_edge_dist=self.bolt.min_edge_dist_round,
        #                                      min_gauge=self.bolt.min_gauge_round,
        #                                      max_spacing=self.bolt.max_spacing_round,
        #                                      max_edge_dist=self.bolt.max_edge_dist_round,
        #                                      shear_load= 0.0 ,
        #                                      axial_load=self.load.axial_force * 1000, gap=self.plate.gap,
        #                                      shear_ecc=False)
        #
        #     if self.plate.design_status is True:
        #         if self.plate.bolts_required > bolts_required_previous and count >= 1:
        #             self.bolt.bolt_diameter_provided = bolt_diameter_previous
        #             self.plate.bolts_required = bolts_required_previous
        #             self.plate.bolt_force = bolt_force_previous
        #             break
        #         bolts_required_previous = self.plate.bolts_required
        #         bolt_diameter_previous = self.bolt.bolt_diameter_provided
        #         bolt_force_previous = self.plate.bolt_force
        #         count += 1
        #     else:
        #         pass
        # bolt_capacity_req = self.bolt.bolt_capacity
        #
        # if self.plate.design_status is False:
        #     self.design_status = False
        #     logger.error(self.plate.reason)
        # else:
        #     self.get_bolt_grade(self, bolt_capacity_req)

        #     self.plate.bolts_required = max(int(math.ceil(self.res_force / self.bolt.bolt_capacity)), 2)
        #     [bolt_line, bolts_one_line, web_plate_h] = \
        #         self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height, self.plate.bolts_required,
        #                                             self.bolt.min_edge_dist_round, self.bolt.min_gauge_round)
        #     self.plate.bolts_required = bolt_line * bolts_one_line
        #     # print(2, self.res_force, self.bolt.bolt_capacity, self.bolt.bolt_grade_provided, self.plate.bolts_required, bolts_one_line)
        #     if self.plate.bolts_required > bolts_required_previous and count >= 1:
        #         self.bolt.bolt_grade_provided = bolt_grade_previous
        #         self.plate.bolts_required = bolts_required_previous
        #         break
        #     bolts_required_previous = self.plate.bolts_required
        #     bolt_grade_previous = self.bolt.bolt_grade_provided
        #     count += 1
        # # self.get_fin_plate_details(self)
        self.member_check(self, design_dictionary)



    def member_check(self,design_dictionary):
        # self.net_area = self.cross_area - (self.plate.bolts_one_line * self.plate.thickness_provided)

        print("1")
        if design_dictionary[KEY_SEC_PROFILE] == "Channels" and design_dictionary[KEY_LOCATION] == "Web":
            member_Ag = self.section_size_1.area*100
            member_An = member_Ag - (self.plate.bolts_one_line * self.bolt.dia_hole * self.section_size_1.web_thickness)
            if self.plate.bolts_one_line >= 2:
                A_vg = ((self.bolt.min_pitch_round * (self.plate.bolt_line - 1) + self.bolt.min_end_dist_round) * self.section_size_1.web_thickness) * 2
                A_vn = ((self.bolt.min_pitch_round * (self.plate.bolt_line - 1) + self.bolt.min_end_dist_round - (
                            (self.plate.bolt_line - 0.5) * self.bolt.dia_hole)) * self.section_size_1.web_thickness) * 2
                A_tg = self.bolt.min_gauge_round* (self.plate.bolts_one_line - 1) * self.section_size_1.web_thickness
                A_tn = (self.bolt.min_gauge_round * (self.plate.bolts_one_line - 1) - ((1) * self.bolt.dia_hole)) * self.section_size_1.web_thickness
            else:
                A_vg = (self.bolt.min_pitch_round + self.bolt.min_end_dist_round) * self.section_size_1.web_thickness
                A_vn = ((self.bolt.min_pitch_round * (self.plate.bolt_line - 1) + self.bolt.min_end_dist_round - (
                            (self.plate.bolt_line - 0.5) * self.bolt.dia_hole)) * self.section_size_1.web_thickness)
                A_tg = (self.bolt.min_end_dist_round) * self.section_size_1.web_thickness
                A_tn = (self.bolt.min_end_dist_round - 0.5 * self.bolt.dia_hole) * self.section_size_1.web_thickness
        elif design_dictionary[KEY_SEC_PROFILE]  == "Back to Back Channels" and design_dictionary[KEY_LOCATION] == "Web":
            member_Ag = self.section_size_1.area
            member_An = member_Ag - (self.plate.bolts_one_line * self.bolt.dia_hole * 2 * self.section_size_1.web_thickness)
            if self.plate.bolts_one_line >= 2:
                A_vg = ((self.bolt.min_pitch_round * (self.plate.bolt_line - 1) + self.bolt.min_end_dist_round) * self.section_size_1.web_thickness) * 2 * 2
                A_vn = ((self.bolt.min_pitch_round * (self.plate.bolt_line - 1) + self.bolt.min_end_dist_round - (
                            (self.plate.bolt_line - 0.5) * self.bolt.dia_hole)) * self.section_size_1.web_thickness) * 2 * 2
                A_tg = self.bolt.min_gauge_round * (self.plate.bolts_one_line - 1) * self.section_size_1.web_thickness * 2
                A_tn = (self.bolt.min_gauge_round * (self.plate.bolts_one_line - 1) - ((1) * self.bolt.dia_hole)) * self.section_size_1.web_thickness * 2
            else:
                A_vg = (self.bolt.min_pitch_round + self.bolt.min_end_dist_round) * self.section_size_1.web_thickness * 2
                A_vn = ((self.bolt.min_pitch_round * (self.plate.bolt_line - 1) + self.bolt.min_end_dist_round - (
                            (self.plate.bolt_line - 0.5) * self.bolt.dia_hole)) * self.section_size_1.web_thickness) * 2
                A_tg = self.bolt.min_end_dist_round * self.section_size_1.web_thickness * 2
                A_tn = (self.bolt.min_end_dist_round - 0.5 * self.bolt.dia_hole) * self.section_size_1.web_thickness * 2

        self.section_size_1.tension_rupture(A_n= member_An,F_u= self.section_size_1.fu)

        self.section_size_1.tension_blockshear_area_input(A_vg = A_vg, A_vn = A_vn, A_tg = A_tg, A_tn = A_tn, f_u = self.section_size_1.fu, f_y = self.section_size_1.fy)

        # if self.i == 0:
        #     self.section_size_1.block_shear_capacity_axial = 400
        #     self.i = self.i + 1
        # else:
        #     pass

        self.section_size_1.tension_capacity_calc(self.section_size_1.tension_yielding_capacity,self.section_size_1.tension_rupture_capacity,self.section_size_1.block_shear_capacity_axial)
        print(self.section_size_1.tension_capacity)
        self.member_recheck(self, design_dictionary)

    def member_recheck(self,design_dictionary):

        if self.section_size_1.tension_capacity > self.load.axial_force:
            self.design_status = True
        else:
            print("recheck")
            previous_size = self.section_size_1.designation
            self.initial_member_capacity(self, design_dictionary, previous_size)



    # @staticmethod
    # def block_shear_strength_section(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
    #     """Calculate the block shear strength of bolted connections as per cl. 6.4.1
    #
    #     Args:
    #         A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
    #         A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
    #         A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
    #                        end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
    #         A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
    #                        end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
    #         f_u: Ultimate stress of the plate material in MPa (float)
    #         f_y: Yield stress of the plate material in MPa (float)
    #
    #     Return:
    #         block shear strength of bolted connection in N (float)
    #
    #     Note:
    #         Reference:
    #         IS 800:2007, cl. 6.4.1
    #
    #     """
    #     gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
    #     gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
    #     T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
    #     T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
    #     Tdb = min(T_db1, T_db2)
    #     Tdb = round(Tdb, 3)
    #     return Tdb
    # def get_fin_plate_details(self):
    #     self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
    #                                             connecting_plates_tk=[self.plate.thickness_provided,
    #                                                                   self.section_size.web_thickness])
    #
    #     self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
    #                                       bolt_grade_provided=self.bolt.bolt_grade_provided,
    #                                       connecting_plates_tk=[self.plate.thickness_provided,
    #                                                             self.section_size.web_thickness],
    #                                       n_planes=1)
    #
    #     self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
    #                                      web_plate_h_min=self.min_plate_height, web_plate_h_max=self.max_plate_height,
    #                                      bolt_capacity=self.bolt.bolt_capacity,
    #                                      min_edge_dist=self.bolt.min_edge_dist_round,
    #                                      min_gauge=self.bolt.min_gauge_round, max_spacing=self.bolt.max_spacing_round,
    #                                      max_edge_dist=self.bolt.max_edge_dist_round, shear_load= 0.0,
    #                                      axial_load=self.load.axial_force*1000, gap=self.plate.gap,
    #                                      shear_ecc=True)
    #
    # def section_block_shear_capacity(self):
    #     #################################
    #     # Block Shear Check for supporting section
    #     #################################
    #     edge_dist_rem = self.plate.edge_dist_provided + self.plate.gap
    #     design_status_block_shear = False
    #     while design_status_block_shear is False:
    #         print(design_status_block_shear)
    #         print(0, self.bolt.max_end_dist, self.plate.end_dist_provided, self.bolt.max_spacing_round, self.plate.pitch_provided)
    #         Avg_a = 2 * (self.plate.end_dist_provided + self.plate.gap + (self.plate.bolt_line - 1) * self.plate.pitch_provided)\
    #                 * self.supporting_section.web_thickness
    #         Avn_a = 2 * (self.plate.end_dist_provided + (self.plate.bolt_line - 1) * self.plate.pitch_provided
    #                  - (self.plate.bolt_line - 0.5) * self.bolt.dia_hole) * self.supporting_section.web_thickness
    #         Atg_a = ((self.plate.bolts_one_line - 1) * self.plate.pitch_provided)\
    #                 * self.supporting_section.web_thickness
    #         Atn_a = ((self.plate.bolts_one_line - 1) * self.plate.pitch_provided -
    #                  (self.plate.bolt_line - 1) * self.bolt.dia_hole) * \
    #                 self.supporting_section.web_thickness
    #
    #         Avg_s = (self.plate.edge_dist_provided + (self.plate.bolts_one_line - 1) * self.plate.gauge_provided)\
    #                 * self.supporting_section.web_thickness
    #         Avn_s = ((self.plate.edge_dist_provided + (self.plate.bolts_one_line - 1) * self.plate.gauge_provided)
    #                  - (self.plate.bolts_one_line - 0.5) * self.bolt.dia_hole) * self.supporting_section.web_thickness
    #
    #         Atg_s = ((self.plate.bolt_line - 1) * self.plate.pitch_provided + self.plate.end_dist_provided + self.plate.gap)\
    #                 * self.supporting_section.web_thickness
    #         Atn_s = ((self.plate.bolt_line - 1) * self.plate.pitch_provided -
    #                  (self.plate.bolt_line - 0.5) * self.bolt.dia_hole + self.plate.end_dist_provided + self.plate.gap) * \
    #                 self.supporting_section.web_thickness
    #
    #         # return [Avg_a, Avn_a, Atg_a, Atn_a], [Avg_s, Avn_s, Atg_s, Atn_s]
    #
    #         self.supporting_section.block_shear_capacity_axial = self.block_shear_strength_section(A_vg=Avg_a, A_vn=Avn_a, A_tg=Atg_a,
    #                                                                                 A_tn=Atn_a,
    #                                                                                 f_u=self.supporting_section.fu,
    #                                                                                 f_y=self.supporting_section.fy)
    #
    #         self.supporting_section.block_shear_capacity_shear = self.block_shear_strength_section(A_vg=Avg_s, A_vn=Avn_s, A_tg=Atg_s,
    #                                                                                 A_tn=Atn_s,
    #                                                                                 f_u=self.supporting_section.fu,
    #                                                                                 f_y=self.supporting_section.fy)
    #
    #         if self.supporting_section.block_shear_capacity_axial < self.load.axial_force*1000 or \
    #                 self.supporting_section.block_shear_capacity_shear < self.load.shear_force*1000:
    #             if self.bolt.max_spacing_round >= self.plate.gauge_provided + 5 and \
    #                     self.bolt.max_end_dist >= self.plate.edge_dist_provided + 5:  # increase thickness todo
    #                 if self.plate.bolt_line == 1:
    #                     self.plate.edge_dist_provided += 5
    #                 else:
    #                     self.plate.gauge_provided += 5
    #             else:
    #                 break
    #         else:
    #             design_status_block_shear = True
    #
    #     self.plate.blockshear(numrow=self.plate.bolts_one_line, numcol=self.plate.bolt_line, pitch=self.plate.pitch_provided,
    #                           gauge=self.plate.gauge_provided, thk=self.plate.thickness[0], end_dist=self.plate.end_dist_provided,
    #                           edge_dist=edge_dist_rem, dia_hole=self.bolt.dia_hole,
    #                           fy=self.supported_section.fy, fu=self.supported_section.fu)
    #
    #     self.plate.shear_yielding(self.plate.height, self.plate.thickness[0], self.plate.fy)
    #
    #     self.plate.shear_rupture_b(self.plate.height, self.plate.thickness[0], self.plate.bolts_one_line,
    #                                    self.bolt.dia_hole, self.plate.fu)
    #
    #     plate_shear_capacity = min(self.plate.block_shear_capacity, self.plate.shear_rupture_capacity,
    #                                self.plate.shear_yielding_capacity)
    #
    #     # if self.load.shear_force > plate_shear_capacity:
    #     #     design_status = False
    #     #     logger.error(":shear capacity of the plate is less than the applied shear force, %2.2f kN [cl. 6.4.1]"
    #     #                  % self.load.shear_force)
    #     #     logger.warning(":Shear capacity of plate is %2.2f kN" % plate_shear_capacity)
    #     #     logger.info(": Increase the plate thickness")
    #
    #     self.plate.get_moment_cacacity(self.plate.fy, self.plate.thickness[0], self.plate.height)
    #
    #     # if self.plate.moment_capacity < self.plate.moment_demand:
    #     #     design_status = False
    #     #     logger.error(": Plate moment capacity is less than the moment demand [cl. 8.2.1.2]")
    #     #     logger.warning(": Re-design with increased plate dimensions")
    #
    #     print(self.connectivity)
    #     print(self.supporting_section)
    #     print(self.supported_section)
    #     print(self.load)
    #     print(self.bolt)
    #     print(self.plate)

    def save_design(self,ui,popup_summary):


        self.report_input =  {'Connection':{"Connection Title" : 'Finplate', 'Connection Type': 'Shear Connection'},"Connection Category":{"Connectivity": 'Column flange-Beam web', "Beam Connection":"Bolted", "Column Connection": "Welded"},"Loading":{'ShearForce(kN) - Vs': 140},"Components":{"Column Section": 'UC 305 x 305 x 97',"Column Material":"E250(Fe410W)A", "Column(N/mm2)-Fuc":410, "Column(N/mm2)-Fyc":250,"Column Details": "","Beam Section": "MB 500", "Beam Material":"E250(Fe410W)A", "Beam(N/mm2)-Fub":410, "Beam(N/mm2)-Fyb":250, "Beam Details": "","Plate Section" : '300 x 100 x 12',  'Thickness(mm)-tp': 12.0, 'Depth(mm)-dp': 300.0, 'Width(mm)-wp': 118.0, 'externalmoment(kN) - md': 8.96, "Weld": "", "Weld Type":"Double Fillet", "Size(mm)-ws": 12, 'Type_of_weld': 'Shop weld', 'Safety_Factor- ': 1.25, 'Weld(kN) - Fuw ': 410, 'WeldStrength - wst': 1590.715 , "EffectiveWeldLength(mm) - efl": 276.0 ,"Bolts":"",'Diameter (mm) - d': 24 , 'Grade': 8.8 ,
                    'Bolt Type': 'Friction Grip Bolt','Bolt Hole Type': 'Standard', 'Bolt Hole Clearance - bc': 2,'Slip Factor - sf': 0.3, 'k_b': 0.519,"Number of effective interface - ne":1, "Factor for clearance- Kh":1,"Minimum Bolt Tension - F0": 50, "Bolt Fu - Fubo": 800, "Bolt Fy - Fybo": 400, "Bolt Numbers - nb": 3, "Bolts per Row - rb": 1, "Bolts per Column - cb": 1, "Gauge (mm) - g": 0, "Pitch(mm) - p": 100, 'colflangethk(mm) - cft ': 15.4, 'colrootradius(mm) - crr': 15.2,'End Distance(mm) - en': 54.0, 'Edge Distance(mm) - eg': 54.0, 'Type of Edge': 'a - Sheared or hand flame cut', 'Min_Edge/end_dist': 1.7, 'gap': 10.0,'is_env_corrosive': 'No'}}

        self.report_supporting = {'Mass': self.supporting_section.mass,
                                  'Area(cm2) - A': self.supporting_section.area,
                                  'D(mm)': self.supporting_section.depth,
                                  'B(mm)': self.supporting_section.flange_width,
                                  't(mm)': self.supporting_section.web_thickness,
                                  'T(mm)': self.supporting_section.flange_thickness,
                                  'FlangeSlope': self.supporting_section.flange_slope,
                                  'R1(mm)': self.supporting_section.root_radius,
                                  'R2(mm)': self.supporting_section.toe_radius,
                                  'Iz(cm4)': self.supporting_section.mom_inertia_z,
                                  'Iy(cm4)': self.supporting_section.mom_inertia_y,
                                  'rz(cm)': self.supporting_section.rad_of_gy_z,
                                  'ry(cm)': self.supporting_section.rad_of_gy_y,
                                  'Zz(cm3)': self.supporting_section.elast_sec_mod_z,
                                  'Zy(cm3)': self.supporting_section.elast_sec_mod_y,
                                  'Zpz(cm3)': self.supporting_section.plast_sec_mod_z,
                                  'Zpy(cm3)': self.supporting_section.elast_sec_mod_y}

        self.report_supported = {'Mass': 86.9, 'Area(cm2) - A': 111.0, 'D(mm)': 500.0, 'B(mm)': 180.0, 't(mm)': 10.2,
                                                    'T(mm)': 17.2, 'FlangeSlope': 98, 'R1(mm)': 17.0, 'R2(mm)': 8.5, 'Iz(cm4)': 45228.0,
                                                    'Iy(cm4)': 1320.0, 'rz(cm)': 20.2, 'ry(cm)': 3.5, 'Zz(cm3)': 1809.1, 'Zy(cm3)': 147.0,
                                                    'Zpz(cm3)': 2074.8, 'Zpy(cm3)': 266.7}
        self.report_result = {"thinnerplate": 10.2,
            'Bolt': {'status': True, 'shearcapacity': 47.443, 'bearingcapacity': 1.0, 'boltcapacity': 47.443,
                     'numofbolts': 3, 'boltgrpcapacity': 142.33, 'numofrow': 3, 'numofcol': 1, 'pitch': 96.0,
                     'edge': 54.0, 'enddist': 54.0, 'gauge': 0.0, 'bolt_fu': 800.0, 'bolt_dia': 24, 'k_b': 0.519,
                     'beam_w_t': 10.2, 'web_plate_t': 12.0, 'beam_fu': 410.0, 'shearforce': 140.0, 'dia_hole': 26},
            'FlangeBolt':{'MaxPitchF': 50},
            'Weld': {'thickness': 10, 'thicknessprovided': 12.0, 'resultantshear': 434.557, 'weldstrength': 1590.715,
                     'weld_fu': 410.0, 'effectiveWeldlength': 276.0},
            'Plate': {'minHeight': 300.0, 'minWidth': 118.0, 'plateedge': 64.0, 'externalmoment': 8.96,
                      'momentcapacity': 49.091, 'height': 300.0, 'width': 118.0, 'blockshear': 439.837,
                      'web_plate_fy': 250.0, 'platethk': 12.0, 'beamdepth': 500.0, 'beamrootradius': 17.0,
                      'colrootradius': 15.2, 'beamflangethk': 17.2, 'colflangethk': 15.4}}

        self.report_check = ["bolt_shear_capacity", "bolt_bearing_capacity", "bolt_capacity", "No_of_bolts", "No_of_Rows",
                        "No_of_Columns", "Thinner_Plate", "Bolt_Pitch", "Bolt_Gauge", "End_distance", "Edge_distance", "Block_Shear",
                        "Plate_thickness", "Plate_height", "Plate_Width", "Plate_Moment_Capacity", "Effective_weld_length",
                        "Weld_Strength"]


        folder = self.select_workspace_folder(self)
        filename = os.path.join(str(folder), "images_html", "Html_Report.html")
        file_name = str(filename)
        ui.call_designreport(self,file_name, popup_summary, folder)

        # Creates PDF
        config = configparser.ConfigParser()
        config.readfp(open(r'Osdag.config'))
        wkhtmltopdf_path = config.get('wkhtml_path', 'path1')

        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        options = {
            'margin-bottom': '10mm',
            'footer-right': '[page]'
        }
        file_type = "PDF(*.pdf)"
        fname, _ = QFileDialog.getSaveFileName(None, "Save File As", folder + "/", file_type)
        fname = str(fname)
        flag = True
        if fname == '':
            flag = False
            return flag
        else:
            pdfkit.from_file(filename, fname, configuration=config, options=options)
            QMessageBox.about(None, 'Information', "Report Saved")

        # with open("filename", 'w') as out_file:
        #     yaml.dump(fin_plate_input, out_file)

    def select_workspace_folder(self):
        # This function prompts the user to select the workspace folder and returns the name of the workspace folder
        config = configparser.ConfigParser()
        config.read_file(open(r'Osdag.config'))
        desktop_path = config.get("desktop_path", "path1")
        folder = QFileDialog.getExistingDirectory(None, "Select Workspace Folder (Don't use spaces in the folder name)",
                                                  desktop_path)
        return folder


    def call_3DModel(self,ui,bgcolor):
        '''
        This routine responsible for displaying 3D Cad model
        :param flag: boolean
        :return:
        '''
        if ui.btn3D.isChecked:
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.chkBxFinplate.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Model",bgcolor)

    def call_3DBeam(self,ui,bgcolor):
        '''
        Creating and displaying 3D Beam
        '''
        ui.chkBxBeam.setChecked(Qt.Checked)
        if ui.chkBxBeam.isChecked():
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.chkBxFinplate.setChecked(Qt.Unchecked)
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)

        ui.commLogicObj.display_3DModel("Beam", bgcolor)

    def call_3DColumn(self, ui, bgcolor):
        '''
        '''
        ui.chkBxCol.setChecked(Qt.Checked)
        if ui.chkBxCol.isChecked():
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.chkBxFinplate.setChecked(Qt.Unchecked)
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
        ui.commLogicObj.display_3DModel("Column", bgcolor)

    def call_3DFinplate(self,ui,bgcolor):
        '''
        Displaying FinPlate in 3D
        '''
        ui.chkBxFinplate.setChecked(Qt.Checked)
        if ui.chkBxFinplate.isChecked():
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
            ui.btn3D.setChecked(Qt.Unchecked)

        ui.commLogicObj.display_3DModel("Plate", bgcolor)

    def unchecked_allChkBox(self,ui):
        '''
        This routine is responsible for unchecking all checkboxes in GUI
        '''

        ui.btn3D.setChecked(Qt.Unchecked)
        ui.chkBxBeam.setChecked(Qt.Unchecked)
        ui.chkBxCol.setChecked(Qt.Unchecked)
        ui.chkBxFinplate.setChecked(Qt.Unchecked)

    def showColorDialog(self,ui):

        col = QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        ui.display.set_bg_gradient_color([r, g, b], [255, 255, 255])

    def generate_3D_Cad_image(self,ui,folder):

        # folder = self.select_workspace_folder(self)

        # status = self.resultObj['Bolt']['status']
        if self.design_status is True:
            self.call_3DModel(self, ui,"gradient_bg")
            data = os.path.join(str(folder), "images_html", "3D_Model.png")
            ui.display.ExportToImage(data)
            ui.display.FitAll()
            return data

        else:
            pass


    def block_shear_strength_section(self, A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1

        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)

        Return:
            block shear strength of bolted connection in N (float)

        Note:
            Reference:
            IS 800:2007, cl. 6.4.1

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        Tdb = min(T_db1, T_db2)
        Tdb = round(Tdb / 1000, 3)
        return Tdb

    def supporting_section_values(self):

        supporting_section = []
        t1 = (KEY_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_DESIGNATION, TYPE_TEXTBOX, None)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
        supporting_section.append(t2)

        t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None)
        supporting_section.append(t3)

        t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None)
        supporting_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
        supporting_section.append(t5)

        t6 = (KEY_SUPTNGSEC_DEPTH, KEY_DISP_SUPTNGSEC_DEPTH, TYPE_TEXTBOX, None)
        supporting_section.append(t6)

        t7 = (KEY_SUPTNGSEC_FLANGE_W, KEY_DISP_SUPTNGSEC_FLANGE_W, TYPE_TEXTBOX, None)
        supporting_section.append(t7)

        t8 = (KEY_SUPTNGSEC_FLANGE_T, KEY_DISP_SUPTNGSEC_FLANGE_T, TYPE_TEXTBOX, None)
        supporting_section.append(t8)

        t9 = (KEY_SUPTNGSEC_WEB_T, KEY_DISP_SUPTNGSEC_WEB_T, TYPE_TEXTBOX, None)
        supporting_section.append(t9)

        t10 = (KEY_SUPTNGSEC_FLANGE_S, KEY_DISP_SUPTNGSEC_FLANGE_S, TYPE_TEXTBOX, None)
        supporting_section.append(t10)

        t11 = (KEY_SUPTNGSEC_ROOT_R, KEY_DISP_SUPTNGSEC_ROOT_R, TYPE_TEXTBOX, None)
        supporting_section.append(t11)

        t12 = (KEY_SUPTNGSEC_TOE_R, KEY_DISP_SUPTNGSEC_TOE_R, TYPE_TEXTBOX, None)
        supporting_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None)
        supporting_section.append(t13)

        t14 = (KEY_SUPTNGSEC_TYPE, KEY_DISP_SUPTNGSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
        supporting_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None)
        supporting_section.append(t18)

        t15 = (KEY_SUPTNGSEC_MOD_OF_ELAST, KEY_SUPTNGSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
        supporting_section.append(t15)

        t16 = (KEY_SUPTNGSEC_MOD_OF_RIGID, KEY_SUPTNGSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
        supporting_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
        supporting_section.append(t17)

        t18 = (KEY_SUPTNGSEC_MASS, KEY_DISP_SUPTNGSEC_MASS, TYPE_TEXTBOX, None)
        supporting_section.append(t18)

        t19 = (KEY_SUPTNGSEC_SEC_AREA, KEY_DISP_SUPTNGSEC_SEC_AREA, TYPE_TEXTBOX, None)
        supporting_section.append(t19)

        t20 = (KEY_SUPTNGSEC_MOA_LZ, KEY_DISP_SUPTNGSEC_MOA_LZ, TYPE_TEXTBOX, None)
        supporting_section.append(t20)

        t21 = (KEY_SUPTNGSEC_MOA_LY, KEY_DISP_SUPTNGSEC_MOA_LY, TYPE_TEXTBOX, None)
        supporting_section.append(t21)

        t22 = (KEY_SUPTNGSEC_ROG_RZ, KEY_DISP_SUPTNGSEC_ROG_RZ, TYPE_TEXTBOX, None)
        supporting_section.append(t22)

        t23 = (KEY_SUPTNGSEC_ROG_RY, KEY_DISP_SUPTNGSEC_ROG_RY, TYPE_TEXTBOX, None)
        supporting_section.append(t23)

        t24 = (KEY_SUPTNGSEC_EM_ZZ, KEY_DISP_SUPTNGSEC_EM_ZZ, TYPE_TEXTBOX, None)
        supporting_section.append(t24)

        t25 = (KEY_SUPTNGSEC_EM_ZY, KEY_DISP_SUPTNGSEC_EM_ZY, TYPE_TEXTBOX, None)
        supporting_section.append(t25)

        t26 = (KEY_SUPTNGSEC_PM_ZPZ, KEY_DISP_SUPTNGSEC_PM_ZPZ, TYPE_TEXTBOX, None)
        supporting_section.append(t26)

        t27 = (KEY_SUPTNGSEC_PM_ZPY, KEY_DISP_SUPTNGSEC_PM_ZPY, TYPE_TEXTBOX, None)
        supporting_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None)
        supporting_section.append(t28)

        t29 = (KEY_SUPTNGSEC_SOURCE, KEY_DISP_SUPTNGSEC_SOURCE, TYPE_TEXTBOX, None)
        supporting_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None)
        supporting_section.append(t30)

        t31 = (KEY_SUPTNGSEC_POISSON_RATIO, KEY_DISP_SUPTNGSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
        supporting_section.append(t31)

        t32 = (KEY_SUPTNGSEC_THERMAL_EXP, KEY_DISP_SUPTNGSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
        supporting_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        supporting_section.append(t33)

        return supporting_section

    def supported_section_values(self):

        supported_section = []

        t1 = (KEY_SUPTDSEC_DESIGNATION, KEY_DISP_SUPTDSEC_DESIGNATION, TYPE_TEXTBOX, None)
        supported_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
        supported_section.append(t2)

        t3 = (KEY_SUPTDSEC_FU, KEY_DISP_SUPTDSEC_FU, TYPE_TEXTBOX, None)
        supported_section.append(t3)

        t4 = (KEY_SUPTDSEC_FY, KEY_DISP_SUPTDSEC_FY, TYPE_TEXTBOX, None)
        supported_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
        supported_section.append(t5)

        t6 = (KEY_SUPTDSEC_DEPTH, KEY_DISP_SUPTDSEC_DEPTH, TYPE_TEXTBOX, None)
        supported_section.append(t6)

        t7 = (KEY_SUPTDSEC_FLANGE_W, KEY_DISP_SUPTDSEC_FLANGE_W, TYPE_TEXTBOX, None)
        supported_section.append(t7)

        t8 = (KEY_SUPTDSEC_FLANGE_T, KEY_DISP_SUPTDSEC_FLANGE_T, TYPE_TEXTBOX, None)
        supported_section.append(t8)

        t9 = (KEY_SUPTDSEC_WEB_T, KEY_DISP_SUPTDSEC_WEB_T, TYPE_TEXTBOX, None)
        supported_section.append(t9)

        t10 = (KEY_SUPTDSEC_FLANGE_S, KEY_DISP_SUPTDSEC_FLANGE_S, TYPE_TEXTBOX, None)
        supported_section.append(t10)

        t11 = (KEY_SUPTDSEC_ROOT_R, KEY_DISP_SUPTDSEC_ROOT_R, TYPE_TEXTBOX, None)
        supported_section.append(t11)

        t12 = (KEY_SUPTDSEC_TOE_R, KEY_DISP_SUPTDSEC_TOE_R, TYPE_TEXTBOX, None)
        supported_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None)
        supported_section.append(t13)

        t14 = (KEY_SUPTDSEC_TYPE, KEY_DISP_SUPTDSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
        supported_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None)
        supported_section.append(t18)

        t15 = (KEY_SUPTDSEC_MOD_OF_ELAST, KEY_SUPTDSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
        supported_section.append(t15)

        t16 = (KEY_SUPTDSEC_MOD_OF_RIGID, KEY_SUPTDSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
        supported_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
        supported_section.append(t17)

        t18 = (KEY_SUPTDSEC_MASS, KEY_DISP_SUPTDSEC_MASS, TYPE_TEXTBOX, None)
        supported_section.append(t18)

        t19 = (KEY_SUPTDSEC_SEC_AREA, KEY_DISP_SUPTDSEC_SEC_AREA, TYPE_TEXTBOX, None)
        supported_section.append(t19)

        t20 = (KEY_SUPTDSEC_MOA_LZ, KEY_DISP_SUPTDSEC_MOA_LZ, TYPE_TEXTBOX, None)
        supported_section.append(t20)

        t21 = (KEY_SUPTDSEC_MOA_LY, KEY_DISP_SUPTDSEC_MOA_LY, TYPE_TEXTBOX, None)
        supported_section.append(t21)

        t22 = (KEY_SUPTDSEC_ROG_RZ, KEY_DISP_SUPTDSEC_ROG_RZ, TYPE_TEXTBOX, None)
        supported_section.append(t22)

        t23 = (KEY_SUPTDSEC_ROG_RY, KEY_DISP_SUPTDSEC_ROG_RY, TYPE_TEXTBOX, None)
        supported_section.append(t23)

        t24 = (KEY_SUPTDSEC_EM_ZZ, KEY_DISP_SUPTDSEC_EM_ZZ, TYPE_TEXTBOX, None)
        supported_section.append(t24)

        t25 = (KEY_SUPTDSEC_EM_ZY, KEY_DISP_SUPTDSEC_EM_ZY, TYPE_TEXTBOX, None)
        supported_section.append(t25)

        t26 = (KEY_SUPTDSEC_PM_ZPZ, KEY_DISP_SUPTDSEC_PM_ZPZ, TYPE_TEXTBOX, None)
        supported_section.append(t26)

        t27 = (KEY_SUPTDSEC_PM_ZPY, KEY_DISP_SUPTDSEC_PM_ZPY, TYPE_TEXTBOX, None)
        supported_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None)
        supported_section.append(t28)

        t29 = (KEY_SUPTDSEC_SOURCE, KEY_DISP_SUPTDSEC_SOURCE, TYPE_TEXTBOX, None)
        supported_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None)
        supported_section.append(t30)

        t31 = (KEY_SUPTDSEC_POISSON_RATIO, KEY_DISP_SUPTDSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
        supported_section.append(t31)

        t32 = (KEY_SUPTDSEC_THERMAL_EXP, KEY_DISP_SUPTDSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
        supported_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        supported_section.append(t33)

        return supported_section

    def input_value_changed(self):

        lst = []

        t1 = (KEY_SEC_PROFILE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t1)

        # t2 = (KEY_END1, KEY_END2, TYPE_COMBOBOX, self.fn_end1_end2)
        # lst.append(t2)
        #
        # t3 = (KEY_END1, KEY_IMAGE, TYPE_IMAGE, self.fn_end1_image)
        # lst.append(t3)
        #
        # t4 = (KEY_END2, KEY_IMAGE, TYPE_IMAGE, self.fn_end2_image)
        # lst.append(t4)

        return lst



# For Command Line


# from ast import literal_eval
#
# path = input("Enter the file location: ")
# with open(path, 'r') as f:
#     data = f.read()
#     d = literal_eval(data)
#     FinPlateConnection.set_input_values(FinPlateConnection(), d, False)
