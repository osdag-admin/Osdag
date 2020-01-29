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


class FinPlateConnection(ShearConnection):

    def __init__(self):
        super(FinPlateConnection, self).__init__()
        self.min_plate_height = 0.0
        self.max_plate_height = 0.0
        self.res_force = 0.0
        self.design_status = False

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
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

    def input_values(self, existingvalues={}):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair

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

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, "./ResourceFiles/images/fin_cf_bw.png")
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, connectdb("Columns"))
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, connectdb("Beams"))
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

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_diameter_provided if flag else '')
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_grade_provided if flag else '')

        out_list.append(t3)

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  round(self.bolt.bolt_shear_capacity/1000,2) if flag else '')
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, round(self.bolt.bolt_bearing_capacity/1000,2) if flag else '')
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX, round(self.bolt.bolt_capacity/1000,2) if flag else '')
        out_list.append(t6)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX, round(self.plate.bolt_force / 1000, 2) if flag else '')
        out_list.append(t21)

        t7 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.plate.bolt_line if flag else '')
        out_list.append(t7)

        t8 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.plate.bolts_one_line if flag else '')
        out_list.append(t8)

        t21 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing])
        out_list.append(t21)

        # t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if flag else '')
        # out_list.append(t9)
        #
        # t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if flag else '')
        # out_list.append(t10)
        #
        # t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if flag else '')
        # out_list.append(t11)
        #
        # t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if flag else '')
        # out_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None)
        out_list.append(t13)

        t14 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.plate.thickness_provided if flag else '')
        out_list.append(t14)

        t15 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.plate.height if flag else '')
        out_list.append(t15)

        t16 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_LENGTH, TYPE_TEXTBOX, self.plate.length if flag else '')
        out_list.append(t16)

        t17 = (KEY_OUT_PLATE_SHEAR, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX, round(self.plate.shear_yielding_capacity,2) if flag else '')
        out_list.append(t17)

        t18 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_OUT_DISP_PLATE_BLK_SHEAR, TYPE_TEXTBOX, round(self.plate.block_shear_capacity,2) if flag else '')
        out_list.append(t18)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX, round(self.plate.moment_demand/1000000,2) if flag else '')
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX, round(self.plate.moment_capacity,2) if flag else '')
        out_list.append(t20)

        return out_list

    def func_for_validation(self, window, design_dictionary):
        self.design_status = False
        flag = False
        flag1 = False
        option_list = self.input_values(self)
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    missing_fields_list.append(option[1])


        if design_dictionary[KEY_CONN] == 'Beam-Beam':
            primary = design_dictionary[KEY_SUPTNGSEC]
            secondary = design_dictionary[KEY_SUPTDSEC]
            conn = sqlite3.connect(PATH_TO_DATABASE)
            cursor = conn.execute("SELECT D FROM BEAMS WHERE Designation = ( ? ) ", (primary,))
            lst = []
            rows = cursor.fetchall()
            for row in rows:
                lst.append(row)
            p_val = lst[0][0]
            cursor2 = conn.execute("SELECT D FROM BEAMS WHERE Designation = ( ? )", (secondary,))
            lst1 = []
            rows1 = cursor2.fetchall()
            for row1 in rows1:
                lst1.append(row1)
            s_val = lst1[0][0]
            if p_val <= s_val:
                QMessageBox.about(window, 'Information',
                                  "Secondary beam depth is higher than clear depth of primary beam web "
                                  "(No provision in Osdag till now)")
            else:
                flag1 = True
        else:
            flag1 = True

        if len(missing_fields_list) > 0:
            QMessageBox.information(window, "Information",
                                    self.generate_missing_fields_error_string(self, missing_fields_list))
            # flag = False
        else:
            flag = True

        if flag and flag1:
            self.set_input_values(self, design_dictionary)
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

        super(FinPlateConnection,self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.weld = Weld(size=10, length= 100, material_grade=design_dictionary[KEY_MATERIAL])
        print("input values are set. Doing preliminary member checks")
        self.member_capacity(self)

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.build == "Rolled":
                length = self.supported_section.depth
            else:
                length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        else:
            length = self.supported_section.depth - 50.0  # TODO: Subtract notch height for beam-beam connection

        self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.tension_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)

        print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
              self.supported_section.tension_yielding_capacity, self.load.axial_force)

        if self.supported_section.shear_yielding_capacity > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity > self.load.axial_force:
            print("preliminary member check is satisfactory. Doing bolt checks")
            self.select_bolt_dia(self)

        else:
            self.design_status = False
            logger.error(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
                           "than applied loads, Please select larger sections or decrease loads"
                            .format(self.supported_section.shear_yielding_capacity,
                                    self.supported_section.tension_yielding_capacity))
            print("failed in preliminary member checks. Select larger sections or decrease loads")

    def select_bolt_dia(self):
        self.min_plate_height = self.supported_section.min_plate_height()
        self.max_plate_height = self.supported_section.max_plate_height()
        self.res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000
        self.plate.thickness_provided = max(min(self.plate.thickness), math.ceil(self.supported_section.web_thickness))
        bolts_required_previous = 2
        bolt_diameter_previous = self.bolt.bolt_diameter[-1]
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        count = 0
        bolts_one_line = 1
        for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    connecting_plates_tk=[self.plate.thickness_provided,
                                                                          self.supported_section.web_thickness])

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              connecting_plates_tk=[self.plate.thickness_provided,
                                                                    self.supported_section.web_thickness],
                                              n_planes=1)

            self.plate.bolts_required = max(int(math.ceil(self.res_force / self.bolt.bolt_capacity)), 2)
            [bolt_line, bolts_one_line, web_plate_h] = \
                self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height, self.plate.bolts_required,
                                                    self.bolt.min_edge_dist_round, self.bolt.min_gauge_round)
            self.plate.bolts_required = bolt_line * bolts_one_line
            print(1, self.res_force, self.bolt.bolt_capacity, self.bolt.bolt_diameter_provided, self.plate.bolts_required, bolts_one_line)
            if bolts_one_line > 1:
                if self.plate.bolts_required > bolts_required_previous and count >= 1:
                    self.bolt.bolt_diameter_provided = bolt_diameter_previous
                    self.plate.bolts_required = bolts_required_previous
                    break
                bolts_required_previous = self.plate.bolts_required
                bolt_diameter_previous = self.bolt.bolt_diameter_provided
                count += 1

        if bolts_one_line == 1:
            self.design_status = False
            logger.error(" : Select bolt of lower diameter")
        else:
            self.design_status = True
            self.get_bolt_grade(self)

    def get_bolt_grade(self):
        bolt_grade_previous = self.bolt.bolt_grade[-1]
        bolts_required_previous = self.plate.bolts_required
        for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
            count = 1
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    connecting_plates_tk=[self.plate.thickness_provided,
                                                                          self.supported_section.web_thickness])

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              connecting_plates_tk=[self.plate.thickness_provided,
                                                                    self.supported_section.web_thickness],
                                              n_planes=1)

            self.plate.bolts_required = max(int(math.ceil(self.res_force / self.bolt.bolt_capacity)), 2)
            [bolt_line, bolts_one_line, web_plate_h] = \
                self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height, self.plate.bolts_required,
                                                    self.bolt.min_edge_dist_round, self.bolt.min_gauge_round)
            self.plate.bolts_required = bolt_line * bolts_one_line
            print(2, self.res_force, self.bolt.bolt_capacity, self.bolt.bolt_grade_provided, self.plate.bolts_required, bolts_one_line)
            if self.plate.bolts_required > bolts_required_previous and count >= 1:
                self.bolt.bolt_grade_provided = bolt_grade_previous
                self.plate.bolts_required = bolts_required_previous
                break
            bolts_required_previous = self.plate.bolts_required
            bolt_grade_previous = self.bolt.bolt_grade_provided
            count += 1
        self.get_fin_plate_details(self)

    def get_fin_plate_details(self):
        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                connecting_plates_tk=[self.plate.thickness_provided,
                                                                      self.supported_section.web_thickness])

        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt.bolt_grade_provided,
                                          connecting_plates_tk=[self.plate.thickness_provided,
                                                                self.supported_section.web_thickness],
                                          n_planes=1)

        self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                         web_plate_h_min=self.min_plate_height, web_plate_h_max=self.max_plate_height,
                                         bolt_capacity=self.bolt.bolt_capacity,
                                         min_edge_dist=self.bolt.min_edge_dist_round,
                                         min_gauge=self.bolt.min_gauge_round, max_spacing=self.bolt.max_spacing_round,
                                         max_edge_dist=self.bolt.max_edge_dist_round, shear_load=self.load.shear_force*1000,
                                         axial_load=self.load.axial_force*1000, gap=self.plate.gap,
                                         shear_ecc=True)

    def section_block_shear_capacity(self):
        #################################
        # Block Shear Check for supporting section
        #################################
        edge_dist_rem = self.plate.edge_dist_provided + self.plate.gap
        design_status_block_shear = False
        while design_status_block_shear is False:
            print(design_status_block_shear)
            print(0, self.bolt.max_end_dist, self.plate.end_dist_provided, self.bolt.max_spacing_round, self.plate.pitch_provided)
            Avg_a = 2 * (self.plate.end_dist_provided + self.plate.gap + (self.plate.bolt_line - 1) * self.plate.pitch_provided)\
                    * self.supporting_section.web_thickness
            Avn_a = 2 * (self.plate.end_dist_provided + (self.plate.bolt_line - 1) * self.plate.pitch_provided
                     - (self.plate.bolt_line - 0.5) * self.bolt.dia_hole) * self.supporting_section.web_thickness
            Atg_a = ((self.plate.bolts_one_line - 1) * self.plate.pitch_provided)\
                    * self.supporting_section.web_thickness
            Atn_a = ((self.plate.bolts_one_line - 1) * self.plate.pitch_provided -
                     (self.plate.bolt_line - 1) * self.bolt.dia_hole) * \
                    self.supporting_section.web_thickness

            Avg_s = (self.plate.edge_dist_provided + (self.plate.bolts_one_line - 1) * self.plate.gauge_provided)\
                    * self.supporting_section.web_thickness
            Avn_s = ((self.plate.edge_dist_provided + (self.plate.bolts_one_line - 1) * self.plate.gauge_provided)
                     - (self.plate.bolts_one_line - 0.5) * self.bolt.dia_hole) * self.supporting_section.web_thickness

            Atg_s = ((self.plate.bolt_line - 1) * self.plate.pitch_provided + self.plate.end_dist_provided + self.plate.gap)\
                    * self.supporting_section.web_thickness
            Atn_s = ((self.plate.bolt_line - 1) * self.plate.pitch_provided -
                     (self.plate.bolt_line - 0.5) * self.bolt.dia_hole + self.plate.end_dist_provided + self.plate.gap) * \
                    self.supporting_section.web_thickness

            # return [Avg_a, Avn_a, Atg_a, Atn_a], [Avg_s, Avn_s, Atg_s, Atn_s]

            self.supporting_section.block_shear_capacity_axial = self.block_shear_strength_section(A_vg=Avg_a, A_vn=Avn_a, A_tg=Atg_a,
                                                                                    A_tn=Atn_a,
                                                                                    f_u=self.supporting_section.fu,
                                                                                    f_y=self.supporting_section.fy)

            self.supporting_section.block_shear_capacity_shear = self.block_shear_strength_section(A_vg=Avg_s, A_vn=Avn_s, A_tg=Atg_s,
                                                                                    A_tn=Atn_s,
                                                                                    f_u=self.supporting_section.fu,
                                                                                    f_y=self.supporting_section.fy)

            if self.supporting_section.block_shear_capacity_axial < self.load.axial_force*1000 or \
                    self.supporting_section.block_shear_capacity_shear < self.load.shear_force*1000:
                if self.bolt.max_spacing_round >= self.plate.gauge_provided + 5 and \
                        self.bolt.max_end_dist >= self.plate.edge_dist_provided + 5:  # increase thickness todo
                    if self.plate.bolt_line == 1:
                        self.plate.edge_dist_provided += 5
                    else:
                        self.plate.gauge_provided += 5
                else:
                    break
            else:
                design_status_block_shear = True

        self.plate.blockshear(numrow=self.plate.bolts_one_line, numcol=self.plate.bolt_line, pitch=self.plate.pitch_provided,
                              gauge=self.plate.gauge_provided, thk=self.plate.thickness[0], end_dist=self.plate.end_dist_provided,
                              edge_dist=edge_dist_rem, dia_hole=self.bolt.dia_hole,
                              fy=self.supported_section.fy, fu=self.supported_section.fu)

        self.plate.shear_yielding(self.plate.height, self.plate.thickness[0], self.plate.fy)

        self.plate.shear_rupture_b(self.plate.height, self.plate.thickness[0], self.plate.bolts_one_line,
                                       self.bolt.dia_hole, self.plate.fu)

        plate_shear_capacity = min(self.plate.block_shear_capacity, self.plate.shear_rupture_capacity,
                                   self.plate.shear_yielding_capacity)

        # if self.load.shear_force > plate_shear_capacity:
        #     design_status = False
        #     logger.error(":shear capacity of the plate is less than the applied shear force, %2.2f kN [cl. 6.4.1]"
        #                  % self.load.shear_force)
        #     logger.warning(":Shear capacity of plate is %2.2f kN" % plate_shear_capacity)
        #     logger.info(": Increase the plate thickness")

        self.plate.get_moment_cacacity(self.plate.fy, self.plate.thickness[0], self.plate.height)

        # if self.plate.moment_capacity < self.plate.moment_demand:
        #     design_status = False
        #     logger.error(": Plate moment capacity is less than the moment demand [cl. 8.2.1.2]")
        #     logger.warning(": Re-design with increased plate dimensions")

        print(self.connectivity)
        print(self.supporting_section)
        print(self.supported_section)
        print(self.load)
        print(self.bolt)
        print(self.plate)

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


# For Command Line


# from ast import literal_eval
#
# path = input("Enter the file location: ")
# with open(path, 'r') as f:
#     data = f.read()
#     d = literal_eval(data)
#     FinPlateConnection.set_input_values(FinPlateConnection(), d, False)
