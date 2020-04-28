from design_type.connection.moment_connection import MomentConnection
from design_report.reportGenerator_latex import CreateLatex

from utils.common.component import *
from cad.common_logic import CommonDesignLogic
from utils.common.material import *
from Common import *
from PyQt5.QtWidgets import QMessageBox
from Common import *
from Report_functions import *
import os
import shutil
import logging
from utils.common.load import Load
import yaml
import os
import shutil
import time
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QMessageBox
import pickle
import pdfkit
import configparser
import cairosvg
from io import StringIO

class ColumnEndPlate(MomentConnection):

    def __init__(self):
        super(ColumnEndPlate, self).__init__()
        self.design_status = False

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """
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
        return KEY_DISP_COLUMNENDPLATE

    def input_values(self, existingvalues={}):

        options_list = []

        if KEY_SECSIZE in existingvalues:
            existingvalue_key_secsize = existingvalues[KEY_SECSIZE]
        else:
            existingvalue_key_secsize = ''

        if KEY_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_CONN]
        else:
            existingvalue_key_conn = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_MOMENT in existingvalues:
            existingvalues_key_moment = existingvalues[KEY_MOMENT]
        else:
            existingvalues_key_moment = ''

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

        if KEY_ENDPLATE_THICKNESS in existingvalues:
            existingvalue_key_endplatethk = existingvalues[KEY_ENDPLATE_THICKNESS]
        else:
            existingvalue_key_endplatethk = ''

        t16 = (KEY_MODULE, KEY_DISP_COLUMNENDPLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, existingvalue_key_secsize, connectdb("Columns"))
        options_list.append(t4)

        t8 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN_3)
        options_list.append(t8)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        options_list.append(t15)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

        t17 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX,existingvalues_key_moment,None)
        options_list.append(t17)

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

        t21 = (None, DISP_TITLE_ENDPLATE, TYPE_TITLE, None, None)
        options_list.append(t21)

        t22 = (KEY_ENDPLATE_THICKNESS, KEY_DISP_ENDPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_endplatethk, VALUES_ENDPLATE_THICKNESS)
        options_list.append(t22)

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

    def plate_details(self, flag):
        plate_details = []

        t8 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.plate.height if flag else '')
        plate_details.append(t8)

        t9 = (KEY_OUT_PLATE_WIDTH, KEY_OUT_DISP_PLATE_WIDTH, TYPE_TEXTBOX,self.plate.length if flag else '')
        plate_details.append(t9)

        t10 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.plate.thickness if flag else '')
        plate_details.append(t10)

        return plate_details

    def output_values(self, flag):

        out_list = []

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None)
        out_list.append(t1)

        t2 = (KEY_D, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,self.bolt_diam_provided if flag else '')
        out_list.append(t2)

        t3 = (KEY_GRD, KEY_DISP_GRD, TYPE_TEXTBOX,self.bolt.bolt_grade_provided if flag else '')
        out_list.append(t3)

        t4 = (None, DISP_TITLE_BOLT_CAPACITIES, TYPE_TITLE, None)
        out_list.append(t4)

    def func_for_validation(self, window, design_dictionary):
        self.design_status = False
        flag = False

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

        if len(missing_fields_list) > 0:
            QMessageBox.information(window, "Information",
                                    generate_missing_fields_error_string(missing_fields_list))
            # flag = False
        else:
            flag = True

        if flag:
            self.set_input_values(self, design_dictionary)
        else:
            pass

    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from Column and Beams table.
        """
        global logger
        red_list = red_list_function()
        if self.section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def set_input_values(self, design_dictionary, window):

        print(design_dictionary)

        super(ColumnEndPlate, self).set_input_values(self, design_dictionary)

        self.section = Column(designation=design_dictionary[KEY_SECSIZE],
                              material_grade=design_dictionary[KEY_MATERIAL])

        self.start_time = time.time()

        self.module = design_dictionary[KEY_MODULE]
        self.connection = design_dictionary[KEY_CONN]

        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None), material_grade=design_dictionary[KEY_PLATE_MATERIAL])
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        if self.design_status:
            self.commLogicObj = CommonDesignLogic(window.display, window.folder, self.module, self.mainmodule)
            status = self.design_status
            self.commLogicObj.call_3DModel(status, ColumnEndPlate)

    def member_capacity(self):
        gamma_m0 = 1.1
        ### Check for axial load ######
        self.axial_capacity = self.section.area * self.section.fy / gamma_m0
        if self.load.axial_force <= self.axial_capacity:
            self.factored_axial_load = self.load.axial_force
        else:
            self.design_status = False
            logger.warning(": axial capacity {} of section is less then applied loads, Please select larger section or decrease loads").format(self.axial_capacity)
        ###############

        ###### Check for shear load  ######
        self.shear_capacity = (self.section.depth * self.section.web_thickness * self.section.fy) / (math.sqrt(3) * gamma_m0)
        if self.load.shear_force <= self.shear_capacity:
            self.factored_shear_load = self.load.shear_force
        else:
            self.design_status = False
            logger.warning(": shear capacity {} of section is less then applied loads, Please select larger section or decrease loads").format(self.shear_capacity)
        #############

        ###### Check for moment #######
        if self.section.type == "Rolled":

            self.limitwidththkratio_flange = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                           column_t_w=self.section.web_thickness,
                                                                           column_d=self.section.depth,
                                                                           column_b=self.section.flange_width,
                                                                           column_fy=self.section.fy,
                                                                           factored_axial_force=self.factored_axial_load,
                                                                           column_area=self.section.area,
                                                                           compression_element="External",
                                                                           section="Rolled")
            print("limitwidththkratio_flange", self.limitwidththkratio_flange)

        elif self.section.type2 == "generally":
            self.limitwidththkratio_web = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                        column_t_w=self.section.web_thickness,
                                                                        column_d=self.section.depth,
                                                                        column_b=self.section.flange_width,
                                                                        column_fy=self.section.fy,
                                                                        factored_axial_force=self.factored_axial_load,
                                                                        column_area=self.section.area,
                                                                        compression_element="Web of an I-H",
                                                                        section="generally")
            print("limitwidththkratio_flange", self.limitwidththkratio_web)

        else:
            pass

        if self.load.shear_force < (0.6 * self.shear_capacity):
            self.Z_p = float((self.section.web_thickness * (self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 4)  # mm3
            self.Z_e = float((self.section.web_thickness * (self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 6)  # mm3

        self.class_of_section = int(max(self.limitwidththkratio_flange, self.limitwidththkratio_web))
        if self.class_of_section == 1 or self.class_of_section == 2:
            Z_w = self.Z_p
        elif self.class_of_section == 3:
            Z_w = self.Z_e

        if self.class_of_section == 1 or self.class_of_section == 2:
            beta_b = 1
        elif self.class_of_section == 3:
            beta_b = self.Z_e / self.Z_p

        self.section.plastic_moment_capacty(beta_b=beta_b, Z_p=self.Z_p,fy=self.section.fy)
        self.section.moment_d_deformation_criteria(fy=self.section.fy, Z_e=self.section.elast_sec_mod_z)
        self.section.moment_capacity = min(self.section.plastic_moment_capactiy, self.section.moment_d_def_criteria)

        if self.load.moment <= self.section.moment_capacity / 1000000:
            self.factored_moment = self.load.moment
        else:
            self.design_status = False
            logger.warning(": moment capacity {} of section is less then applied loads, Please select larger section or decrease loads").format(self.section.moment_capacity / 1000000)
        if self.load.moment == 0:
            self.load.moment = self.section.moment_capacity
        else:
            pass
        print("self.load.moment", self.section.moment_capacity)
        ##################

    ##### no of bolts, pitch and end distances  #######
    def detailing(self):
        self.n_bw = ((self.section.depth -(2 * self.section.flange_thickness - (2 * self.plate.end_dist_provided))) / self.plate.pitch_provided) + 1
        self.n_bf = ((self.section.flange_width/2) - (self.section.web_thickness/2) - (2 * self.plate.end_dist_provided) / self.plate.pitch_provided) + 1

        if self.connection == 'Flush End Plate':
            self.no_bolts = self.n_bw * 2 + self.n_bf - 4
        else:
            self.no_bolts = self.n_bw * 2 + 2 * self.n_bf - 4

        if self.n_bw % 2 == 0:
            self.p_2 = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.plate.end_dist_provided) - ((self.n_bw - 2) * self.plate.pitch_provided)
        else:
            self.p_2 = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.plate.end_dist_provided) - ((self.n_bw - 3) * self.plate.pitch_provided)

        self.x = (self.section.flange_width/2) - (self.section.web_thickness/2) - self.plate.end_dist_provided - (self.n_bf * self.plate.pitch_provided)
    ##############

    def y_sqre(self):
        if self.connection == 'Flush End Plate':
            self.y_max = self.section.depth - 3/2 * self.section.flange_thickness - self.plate.end_dist_provided
        else:
            self.y_max = self.section.depth - self.section.flange_thickness/2 + self.plate.end_dist_provided

        if self.connection == 'Flush End Plate':
            if self.n_bf % 2 == 0:
                for i in range(1,self.n_bf+1):
                    self.y_sqr1 = (self.section.flange_thickness/2 + self.plate.end_dist_provided + ((i/2) -1) * self.plate.pitch_provided) ** 2
                    self.y_sqr2 = self.y_sqr1 + (self.p_2 + ((i/2) - 1) * self.plate.pitch_provided) ** 2
                    self.y_sqr = self.y_sqr1 + self.y_sqr2
            else:
                for i in range(1,self.n_bf+1):
                    self.y_sqr1 = (self.section.flange_thickness/2 + self.plate.end_dist_provided + ((i/2) -1.5) * self.plate.pitch_provided) ** 2
                    self.y_sqr2 = self.y_sqr1 + (2 * self.p_2 + ((i/2) - 1) * self.plate.pitch_provided) ** 2
                    self.y_sqr = self.y_sqr1 + self.y_sqr2
        else:
            self.y_sqr = self.y_sqr + (2 * self.plate.end_dist_provided + self.section.flange_thickness) ** 2

    def bolt_checks(self):
        self.t_b = self.load.axial_force/self.no_bolts + self.load.moment * self.y_max/ self.y_sqr

        self.bolt_conn_plates_t_fu_fy=[]
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))

        # bolts_required_previous = 2
        # bolt_diameter_previous = self.bolt.bolt_diameter[-1]
        # self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        # count = 0

        # for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):

        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter,
                                          bolt_grade_provided=self.bolt.bolt_grade,
                                          conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                          n_planes=1)
        self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt.bolt_diameter,
                                          bolt_grade_provided=self.bolt.bolt_grade)

        self.v_sb = self.load.shear_force/ 2* self.n_bw

        if self.t_b > self.bolt.bolt_tension_capacity:
            self.design_status = False
            logger.error("Force is not sufficient")
            logger.info("Increase bolt diam")

        if self.v_sb > self.bolt.bolt_capacity:
            self.design_status = False
            logger.error("Force is not sufficient")
            logger.info("Increase bolt diam")

        if ((self.v_sb/self.bolt.bolt_capacity) ** 2 + (self.t_b/self.bolt.bolt_tension_capacity) ** 2) > 1.0:
            self.design_status = False
            logger.error("Force is not sufficient")
            logger.info("Increase bolt diam")
        return self.design_status

            # if self.design_status is True:
            #     if self.plate.bolts_required > bolts_required_previous and count >= 1:
            #         self.bolt.bolt_diameter_provided = bolt_diameter_previous
            #         self.plate.bolts_required = bolts_required_previous
            #         break
                # bolts_required_previous = self.plate.bolts_required
                # bolt_diameter_previous = self.bolt.bolt_diameter_provided
                # count += 1
            # else:
            #     pass

    # def get_bolt_diam(self):
    #     for i in self.bolt.bolt_diameter:
    #         self.bolt_checks(self.bolt.bolt_diameter[i])
    #         if self.design_status:
    #             self.bolt.bolt_diameter_provided = i
    #             break
    #
    # def get_bolt_grade(self):
    #     for i in self.bolt.bolt_grade:
    #         self.bolt_checks(self.bolt.bolt_grade[i])
    #         if self.design_status:
    #             self.bolt.bolt_grade_provided = i
    #             break

    def get_bolt_diam(self):
        self.lst1 = []
        self.lst2 = []
        # self.lst2 = []
        # for (x,y) in (self.bolt.bolt_diameter,self.bolt.bolt_grade):
        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
        for x in self.bolt.bolt_diameter:
            self.pitch = IS800_2007.cl_10_2_2_min_spacing(x)
            self.end_dist = IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt.bolt_diameter[x],self.bolt.bolt_hole_type,self.bolt.edge_type)

            self.n_bw = ((self.section.depth - (2 * self.section.flange_thickness + (2 * self.end_dist))) / self.pitch) + 1
            self.n_bf = ((self.section.flange_width / 2) - (self.section.web_thickness / 2) - (2 * self.end_dist) / self.pitch) + 1

            if self.connection == 'Flush End Plate':
                self.no_bolts = self.n_bw * 2 + self.n_bf * 4 - 4
            else:
                self.no_bolts = self.n_bw * 2 + 8 * self.n_bf - 4

            if self.n_bw % 2 == 0:
                self.p_2 = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.end_dist) - ((self.n_bw - 2) * self.pitch)
            else:
                self.p_2 = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.end_dist) - ((self.n_bw - 3) * self.pitch)

            self.x = (self.section.flange_width / 2) - (self.section.web_thickness / 2) - self.end_dist - (self.n_bf * self.pitch)

            if self.connection == 'Flush End Plate':
                self.y_max = self.section.depth - 3/2 * self.section.flange_thickness - self.end_dist
            else:
                self.y_max = self.section.depth - self.section.flange_thickness/2 + self.end_dist

            if self.connection == 'Flush End Plate':
                if self.n_bf % 2 == 0:
                    for p in range(1,self.n_bf+1):
                        self.y_sqr1 = (self.section.flange_thickness/2 + self.end_dist + ((p/2) -1) * self.pitch) ** 2
                        self.y_sqr2 = self.y_sqr1 + (self.p_2 + ((p/2) - 1) * self.plate.pitch_provided) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                else:
                    for p in range(1,self.n_bf+1):
                        self.y_sqr1 = (self.section.flange_thickness/2 + self.end_dist + ((p/2) -1.5) * self.pitch) ** 2
                        self.y_sqr2 = self.y_sqr1 + (2 * self.p_2 + ((p/2) - 1) * self.pitch) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
            else:
                self.y_sqr = self.y_sqr + (2 * self.end_dist + self.section.flange_thickness) ** 2

            self.t_b = self.load.axial_force / self.no_bolts + self.load.moment * self.y_max / self.y_sqr


            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter[x],
                                              # bolt_grade_provided=self.bolt.bolt_grade[y],
                                              bolt_grade_provided=self.bolt.bolt_grade[-1],
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=1)
            self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=x,
                                                      # bolt_grade_provided=self.bolt.bolt_grade[y]
                                                      bolt_grade_provided=self.bolt.bolt_grade[-1])

            self.v_sb = self.load.shear_force / 2 * self.n_bw

            if self.t_b > self.bolt.bolt_tension_capacity:
                self.design_status = False
                logger.error("Force is not sufficient")
                logger.info("Increase bolt diam")

            if self.v_sb > self.bolt.bolt_capacity:
                self.design_status = False
                logger.error("Force is not sufficient")
                logger.info("Increase bolt diam")

            if ((self.v_sb / self.bolt.bolt_capacity) ** 2 + (self.t_b / self.bolt.bolt_tension_capacity) ** 2) > 1.0:
                self.design_status = False
                logger.error("Force is not sufficient")
                logger.info("Increase bolt diam")
                return self.design_status

            if self.design_status:
                self.lst1.append(x)
                self.lst2.append(self.no_bolts)
                # self.lst2.append(y)
        res = dict(zip(self.lst1, self.lst2))
        key_min = min(res.keys(), key=(lambda k: res[k]))
        self.bolt_diam_provided = res[key_min]
        # self.bolt_grade_provided = min(self.lst2)

    def get_bolt_grade(self):
        self.lst1 = []
        # self.lst2 = []
        # for (x,y) in (self.bolt.bolt_diameter,self.bolt.bolt_grade):
        for x in self.bolt.bolt_grade:
            self.pitch = IS800_2007.cl_10_2_2_min_spacing(self.bolt_diam_provided)
            self.end_dist = IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt_diam_provided,self.bolt.bolt_hole_type,self.bolt.edge_type)

            self.n_bw = int(math.floor(((self.section.depth - (2 * self.section.flange_thickness + (2 * self.end_dist))) / self.pitch) + 1))
            self.n_bf = int(math.floor(((self.section.flange_width / 2) - (self.section.web_thickness / 2) - (2 * self.end_dist) / self.pitch) + 1))

            if self.connection == 'Flush End Plate':
                self.no_bolts = self.n_bw * 2 + self.n_bf * 4 - 4
            else:
                self.no_bolts = self.n_bw * 2 + 8 * self.n_bf - 4

            if self.n_bw % 2 == 0:
                self.p_2 = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.end_dist) - ((self.n_bw - 2) * self.pitch)
            else:
                self.p_2 = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.end_dist) - ((self.n_bw - 3) * self.pitch)

            self.x = (self.section.flange_width / 2) - (self.section.web_thickness / 2) - self.end_dist - (self.n_bf * self.pitch)

            if self.connection == 'Flush End Plate':
                self.y_max = self.section.depth - 3/2 * self.section.flange_thickness - self.end_dist
            else:
                self.y_max = self.section.depth - self.section.flange_thickness/2 + self.end_dist

            if self.connection == 'Flush End Plate':
                if self.n_bf % 2 == 0:
                    for p in range(1,self.n_bf+1):
                        self.y_sqr1 = (self.section.flange_thickness/2 + self.end_dist + ((p/2) -1) * self.pitch) ** 2
                        self.y_sqr2 = self.y_sqr1 + (self.p_2 + ((p/2) - 1) * self.plate.pitch_provided) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                else:
                    for p in range(1,self.n_bf+1):
                        self.y_sqr1 = (self.section.flange_thickness/2 + self.end_dist + ((p/2) -1.5) * self.pitch) ** 2
                        self.y_sqr2 = self.y_sqr1 + (2 * self.p_2 + ((p/2) - 1) * self.pitch) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
            else:
                self.y_sqr = self.y_sqr + (2 * self.end_dist + self.section.flange_thickness) ** 2

            self.t_b = self.load.axial_force / self.no_bolts + self.load.moment * self.y_max / self.y_sqr


            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt_diam_provided,
                                              bolt_grade_provided=x,
                                              # bolt_grade_provided=12.9,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=1)
            self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt_diam_provided,
                                                      bolt_grade_provided=x)
                                                      # bolt_grade_provided=12.9)

            self.v_sb = self.load.shear_force / 2 * self.n_bw

            if self.t_b > self.bolt.bolt_tension_capacity:
                self.design_status = False
                logger.error("Force is not sufficient")
                logger.info("Increase bolt diam")

            if self.v_sb > self.bolt.bolt_capacity:
                self.design_status = False
                logger.error("Force is not sufficient")
                logger.info("Increase bolt diam")

            if ((self.v_sb / self.bolt.bolt_capacity) ** 2 + (self.t_b / self.bolt.bolt_tension_capacity) ** 2) > 1.0:
                self.design_status = False
                logger.error("Force is not sufficient")
                logger.info("Increase bolt diam")
                return self.design_status

            if self.design_status:
                self.lst1.append(x)
                # self.lst2.append(y)
        self.bolt_grade_provided = min(self.lst1)
        # self.bolt_grade_provided = min(self.lst2)

    def plate_details(self):
        if self.connection == 'Flush End Plate':
            self.plate_height = self.section.depth
        else:
            self.plate_height = self.section.depth + 4 * self.end_dist
        self.plate_width = self.section.flange_width
        self.y_2 = self.y_max - self.plate.end_dist_provided
        self.t_b2 = self.load.axial_force / self.no_bolts + self.load.moment * self.y_2 / self.y_sqr

        if self.connection == 'Flush End Plate':
            if self.n_bf <= 1:
                self.m_ep = max(0.5 * self.t_b * self.plate.end_dist_provided, self.t_b2 * self.plate.end_dist_provided)
            else:
                self.m_ep = self.t_b * self.plate.end_dist_provided

        else:
            self.m_ep = self.t_b * self.plate.end_dist_provided

        if self.pitch >= self.end_dist*2:
            self.b_eff = self.end_dist
        elif self.pitch < self.end_dist*2:
            self.b_eff = self.pitch

        gamma_m0 = 1.1
        lst_pl = []

        for x in self.plate.thickness:
            self.m_dp = self.b_eff * x**2 * self.plate.fy / (4 * gamma_m0)
            if self.m_dp > self.m_ep:
                self.design_status = False
                logger.error('Plate thickness provided is not sufficient')
                logger.info('Please select higher tplate thickness')

            if self.design_status:
                lst_pl.append(x)

    def hard_values(self):
            # flange bolt
            self.load.moment = 20  # kN
            self.factored_axial_load = 300  # KN
            self.load.shear_force = 50  # kN
            self.flange_bolt.bolt_type = "Bearing Bolt"
            # self.flange_bolt.bolt_hole_type = bolt_hole_type
            # self.flange_bolt.edge_type = edge_type
            # self.flange_bolt.mu_f = float(mu_f)
            self.flange_bolt.connecting_plates_tk = None

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    @staticmethod
    def endplate_thick_customized():
        d = VALUES_COLUMN_ENDPLATE_THICKNESS_CUSTOMIZED
        return d

    @staticmethod
    def limiting_width_thk_ratio(column_f_t, column_t_w, column_d, column_b, column_fy, factored_axial_force,
                                 column_area, compression_element, section):

        epsilon = float(math.sqrt(250 / column_fy))
        axial_force_w = int(
            ((column_d - 2 * (column_f_t)) * column_t_w * factored_axial_force) / (column_area))  # N

        des_comp_stress_web = column_fy
        des_comp_stress_section = column_fy
        avg_axial_comp_stress = axial_force_w / ((column_d - 2 * column_f_t) * column_t_w)
        r1 = avg_axial_comp_stress / des_comp_stress_web
        r2 = avg_axial_comp_stress / des_comp_stress_section
        a = column_b / column_f_t
        # compression_element=["External","Internal","Web of an I-H" ,"box section" ]
        # section=["rolled","welded","compression due to bending","generally", "Axial compression" ]
        # section = "rolled"
        if compression_element == "External" or compression_element == "Internal":
            if section == "Rolled":
                if column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 10.5 * epsilon:
                    class_of_section1 = "compact"
                elif column_b * 0.5 / column_f_t <= 15.7 * epsilon:
                    class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
                # print("class_of_section", class_of_section )
            elif section == "welded":
                if column_b * 0.5 / column_f_t <= 8.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "compact"
                elif column_b * 0.5 / column_f_t <= 13.6 * epsilon:
                    class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            elif section == "compression due to bending":
                if column_b * 0.5 / column_f_t <= 29.3 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 33.5 * epsilon:
                    class_of_section1 = "compact"
                elif column_b * 0.5 / column_f_t <= 42 * epsilon:
                    class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            # else:
            #     pass

        elif compression_element == "Web of an I-H" or compression_element == "box section":
            if section == "generally":
                if r1 < 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= (max(105 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "compact"
                    elif column_d / column_t_w <= max((126 * epsilon / (1 + 2 * r1)), column_d / column_t_w >= (
                            42 * epsilon)):
                        class_of_section1 = "semi-compact"
                    # else:
                    #     print('fail')
                    # print("class_of_section3", class_of_section)
                elif r1 > 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= max((105 * epsilon / (1 + (r1 * 1.5))), (
                            42 * epsilon)):
                        class_of_section1 = "compact"
                    elif column_d / column_t_w <= max((126 * epsilon / (1 + 2 * r1)), (
                            42 * epsilon)):
                        class_of_section1 = "semi-compact"
                    # else:
                    #     self.design_status ==False
                    #     # print(self.design_status,"reduce Axial Force")
                    #     logger.warning(
                    #         ": Reduce Axial Force, web is slender under given forces")
                    # else:
                    #     print('fail')
                    # print("class_of_section4", class_of_section)
            elif section == "Axial compression":
                if column_d / column_t_w <= (42 * epsilon):
                    class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "N/A"
        #     else:
        #         print('fail')
        # else:
        #     pass
        print("class_of_section", class_of_section1)
        if class_of_section1 == "plastic":
            class_of_section1 = 1
        elif class_of_section1 == "compact":
            class_of_section1 = 2
        elif class_of_section1 == "semi-compact":
            class_of_section1 = 3
        # else:
        #     print('fail')
        print("class_of_section2", class_of_section1)

        return class_of_section1

        print("class_of_section1", class_of_section1)

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        t6 = (KEY_ENDPLATE_THICKNESS, self.endplate_thick_customized)
        list1.append(t6)
        return list1