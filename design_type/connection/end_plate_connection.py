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



class EndPlateConnection(ShearConnection):

    def __init__(self, connectivity, supporting_member_section, supported_member_section, fu, fy, shear_load,
                 bolt_diameter, bolt_type, bolt_grade, weld_size, plate_thickness, plate_height=0.0, plate_width=0.0):
        super(EndPlateConnection, self).__init__(connectivity, supporting_member_section, supported_member_section,
                                                      fu, fy, shear_load, bolt_diameter, bolt_type, bolt_grade)
        self.plate = Plate(thickness=plate_thickness, height=plate_height, width=plate_width, material=self.material)
        self.weld = Weld(weld_size)
        self.weld_size_list = []
        self.design_status = False


    def set_osdaglogger(key):

        """
        Function to set Logger for End Plate Module
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

    def module(self):
        return KEY_DISP_ENDPLATE






    def input_values(self, existingvalues={}):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair
        self.module = KEY_DISP_ENDPLATE
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

        t16 = (KEY_MODULE, KEY_DISP_ENDPLATE, TYPE_MODULE, None, None)
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
            # elif option[2] == TYPE_MODULE:
            #     if design_dictionary[option[0]] == "End Plate":

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
                                    generate_missing_fields_error_string(missing_fields_list))
            # flag = False
        else:
            flag = True

        if flag and flag1:
            self.set_input_values(self, design_dictionary)
        else:
            pass


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
        super(EndPlateConnection,self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.weld = Weld(size=10, length= 100, material_grade=design_dictionary[KEY_MATERIAL])
        print("input values are set. Doing preliminary member checks")
        self.member_capacity(self)



    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.type == "Rolled":
                length = self.supported_section.depth
            else:
                length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        else:
            length = self.supported_section.depth - round_up((2*self.supporting_section.flange_thickness),5)  # TODO: Subtract notch height for beam-beam connection

        self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.tension_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)

        print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
              self.supported_section.tension_yielding_capacity, self.load.axial_force)

        if self.supported_section.shear_yielding_capacity > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity > self.load.axial_force:
            print("preliminary member check is satisfactory. Doing bolt checks")
            self.select_bolt_dia(self)
            self.design_status = True

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
        # if self.connectivity == VALUES_CONN_1[1]:
        self.plate.thickness_provided = max(min(self.plate.thickness), math.ceil(self.supported_section.web_thickness))
        # elif self.connectivity == VALUES_CONN_1[2]:
        #     self.plate.thickness_provided = max(min(self.plate.thickness),
        #                                         math.ceil(self.supporting_section.web_thickness))
        # else:
        #     self.plate.thickness_provided = max(min(self.plate.thickness), math.ceil(self.supporting_section.web_thickness))
        for pl_thick in self.plate.thickness:
            if pl_thick >= self.plate.thickness_provided:
                self.plate.thickness_provided = pl_thick
                break

        bolts_required_previous = 4
        bolt_diameter_previous = self.bolt.bolt_diameter[-1]


        if self.connectivity == VALUES_CONN_1[1]:
            self.connecting_plates_tk = [self.plate.thickness_provided, self.supported_section.flange_thickness]
        else:
            self.connecting_plates_tk = [self.plate.thickness_provided, self.supported_section.web_thickness]


        # res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        count = 0
        bolts_one_line = 1
        for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    connecting_plates_tk=self.connecting_plates_tk)

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              connecting_plates_tk=self.connecting_plates_tk,
                                              n_planes=1)

            self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided)
            print("Bolt tension capacity:", self.bolt.bolt_tension_capacity)
            # print("Shear force:", self.load.shear_force)

            # comb_bolt_ir=2
            bolts_required = bolts_required_previous
            while True:
                bolt_shear = self.load.shear_force*1000 / bolts_required  # N
                bolt_tension = self.load.axial_force*1000 / bolts_required  # N
                comb_bolt_ir = (bolt_shear/self.bolt.bolt_capacity)**2 + (bolt_tension/self.bolt.bolt_tension_capacity)**2
                print(comb_bolt_ir)
                if comb_bolt_ir > 1:
                    bolts_required += 2
                else:
                    break



            print("Bolts required:", bolts_required)


            bolt_rows = bolts_required/2

            # self.plate.bolts_required = max(int(math.ceil(self.res_force / self.bolt.bolt_capacity)), 2)
            [bolt_line, bolts_one_line, web_plate_h] = \
                self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height,
                                                          self.plate.bolts_required,
                                                          self.bolt.min_edge_dist_round, self.bolt.min_gauge_round)

            if bolt_rows < bolts_one_line:
                self.design_status = True
                break



            self.plate.bolts_required = bolt_line * bolts_one_line
            print(1, self.res_force, self.bolt.bolt_capacity, self.bolt.bolt_diameter_provided,
                  self.plate.bolts_required, bolts_one_line)
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

        edge_dist_rem = self.plate.edge_dist_provided+self.plate.gap

        #################################
        # Block Shear Check for supporting section
        #################################
        # design_status_block_shear = False
        # while design_status_block_shear is False:
            # print(design_status_block_shear)
            # print(0, self.web_plate.max_end_dist, self.web_plate.end_dist_provided, self.web_plate.max_spacing_round, self.web_plate.pitch_provided)
            # Avg_a = 2 * (self.plate.end_dist_provided + self.plate.gap + (self.plate.bolt_line - 1) * self.plate.pitch_provided)\
            #         * self.supporting_section.web_thickness
            # Avn_a = 2 * (self.plate.end_dist_provided + (self.plate.bolt_line - 1) * self.plate.pitch_provided
            #          - (self.plate.bolt_line - 0.5) * self.bolt.dia_hole) * self.supporting_section.web_thickness
            #
            # Atg_a = ((self.plate.bolts_one_line - 1) * self.plate.pitch_provided)\
            #         * self.supporting_section.web_thickness
            # Atn_a = ((self.plate.bolts_one_line - 1) * self.plate.pitch_provided -
            #          (self.plate.bolt_line - 1) * self.bolt.dia_hole) * \
            #         self.supporting_section.web_thickness
            #
            # Avg_s = (self.plate.edge_dist_provided + (self.plate.bolts_one_line - 1) * self.plate.gauge_provided)\
            #         * self.supporting_section.web_thickness
            # Avn_s = ((self.plate.edge_dist_provided + (self.plate.bolts_one_line - 1) * self.plate.gauge_provided)
            #          - (self.plate.bolts_one_line - 0.5) * self.bolt.dia_hole) * self.supporting_section.web_thickness
            #
            # Atg_s = ((self.plate.bolt_line - 1) * self.plate.pitch_provided + self.plate.end_dist_provided + self.plate.gap)\
            #         * self.supporting_section.web_thickness
            # Atn_s = ((self.plate.bolt_line - 1) * self.plate.pitch_provided -
            #          (self.plate.bolt_line - 0.5) * self.bolt.dia_hole + self.plate.end_dist_provided + self.plate.gap) * \
            #         self.supporting_section.web_thickness
            #
            # self.supporting_section.block_shear_capacity_axial = self.block_shear_strength_section(A_vg=Avg_a, A_vn=Avn_a, A_tg=Atg_a,
            #                                                                         A_tn=Atn_a,
            #                                                                         f_u=self.supporting_section.fu,
            #                                                                         f_y=self.supporting_section.fy)
            #
            # self.supporting_section.block_shear_capacity_shear = self.block_shear_strength_section(A_vg=Avg_s, A_vn=Avn_s, A_tg=Atg_s,
            #                                                                         A_tn=Atn_s,
            #                                                                         f_u=self.supporting_section.fu,
            #                                                                         f_y=self.supporting_section.fy)
            #
            # if self.supporting_section.block_shear_capacity_axial < self.load.axial_force:
            #     if self.bolt.max_spacing_round >= self.plate.pitch_provided + 5 and self.bolt.max_end_dist >= self.plate.end_dist_provided + 5:  # increase thickness todo
            #         if self.plate.bolt_line == 1:
            #             self.plate.end_dist_provided += 5
            #         else:
            #             self.plate.pitch_provided += 5
            #     else:
            #         design_status_block_shear = False
            # else:
            #     design_status_block_shear = True

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
        # self.design_status = True
        print(self.connectivity)
        print(self.supporting_section)
        print(self.supported_section)
        print(self.load)
        print(self.bolt)
        print(self.plate)


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
            return ''

    def input_value_changed(self):

        lst = []

        t1 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_LABEL, self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_COMBOBOX, self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = (KEY_CONN, KEY_SUPTDSEC, TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = (KEY_CONN, KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = (KEY_CONN, KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        return lst

    def to_get_d(my_d):
        print(my_d)