from design_type.connection.moment_connection import MomentConnection
from utils.common.component import *
from Common import *
from utils.common.load import Load
import yaml
import os
import shutil
import logging
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QMessageBox
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice


class BeamCoverPlate(MomentConnection):

    def __init__(self):
        super(BeamCoverPlate, self).__init__()
        self.design_status = False



    def set_osdaglogger(key):
        global logger
        logger = logging.getLogger('osdag')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = OurLog(key)
        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def input_values(self, existingvalues={}):

        options_list = []

        if KEY_SECSIZE in existingvalues:
            existingvalue_key_secsize = existingvalues[KEY_SECSIZE]
        else:
            existingvalue_key_secsize = ''

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

        if KEY_FLANGEPLATE_PREFERENCES in existingvalues:
            existingvalue_key_fplate_pref = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_fplate_pref = ''

        if KEY_FLANGEPLATE_THICKNESS in existingvalues:
            existingvalue_key_fplate_thk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_fplate_thk = ''

        if KEY_WEBPLATE_THICKNESS in existingvalues:
            existingvalue_key_wplate_thk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_wplate_thk = ''

        t16 = (KEY_MODULE, KEY_DISP_BEAMCOVERPLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, existingvalue_key_secsize, connectdb("Beams"))
        options_list.append(t4)

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

        t18 = (None, DISP_TITLE_FLANGESPLICEPLATE, TYPE_TITLE, None, None)
        options_list.append(t18)

        t19 = (KEY_FLANGEPLATE_PREFERENCES, KEY_DISP_FLANGESPLATE_PREFERENCES, TYPE_COMBOBOX, existingvalue_key_fplate_pref, VALUES_FLANGEPLATE_PREFERENCES)
        options_list.append(t19)

        t20 = (KEY_FLANGEPLATE_THICKNESS, KEY_DISP_FLANGESPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_fplate_thk, VALUES_FLANGEPLATE_THICKNESS)
        options_list.append(t20)

        t21 = (None, DISP_TITLE_WEBSPLICEPLATE, TYPE_TITLE, None, None)
        options_list.append(t21)

        t22 = (KEY_WEBPLATE_THICKNESS, KEY_DISP_WEBPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_wplate_thk, VALUES_WEBPLATE_THICKNESS)
        options_list.append(t22)

        return options_list

    def flangespacing(self, flag):

        flangespacing = []

        t21 = (KEY_FLANGE_PITCH, KEY_DISP_FLANGE_PLATE_PITCH, TYPE_TEXTBOX,
               self.flange_plate.pitch_provided )
        flangespacing.append(t21)

        t22 = (KEY_ENDDIST_FLANGE, KEY_DISP_END_DIST_FLANGE, TYPE_TEXTBOX,
               self.flange_plate.end_dist_provided )
        flangespacing.append(t22)

        t23 = (KEY_FLANGE_PLATE_GAUGE, KEY_DISP_FLANGE_PLATE_GAUGE, TYPE_TEXTBOX,
               self.flange_plate.gauge_provided )
        flangespacing.append(t23)

        t24 = (KEY_EDGEDIST_FLANGE, KEY_DISP_EDGEDIST_FLANGE, TYPE_TEXTBOX,
               self.flange_plate.edge_dist_provided )
        flangespacing.append(t24)
        return flangespacing
    #
    def webspacing(self, flag):

        webspacing = []

        t8 = (KEY_WEB_PITCH, KEY_DISP_WEB_PLATE_PITCH, TYPE_TEXTBOX, self.web_plate.pitch_provided if flag else '')
        webspacing.append(t8)

        t9 = (KEY_ENDDIST_W, KEY_DISP_END_DIST_W, TYPE_TEXTBOX,
            self.web_plate.end_dist_provided if flag else '')
        webspacing.append(t9)

        t10 = ( KEY_WEB_GAUGE, KEY_DISP_WEB_PLATE_GAUGE, TYPE_TEXTBOX, self.web_plate.gauge_provided if flag else '')
        webspacing.append(t10)

        t11 = (KEY_EDGEDIST_W, KEY_DISP_EDGEDIST_W, TYPE_TEXTBOX,
               self.web_plate.edge_dist_provided if flag else '')
        webspacing.append(t11)
        return webspacing
    #
    def flangecapacity(self, flag):

        flangecapacity = []
        t30= (KEY_TENSIONYIELDINGCAP_FLANGE, KEY_DISP_TENSIONYIELDINGCAP_FLANGE, TYPE_TEXTBOX,
               round(self.flange_plate.tension_yielding_capacity/1000, 2) if flag else '')
        flangecapacity.append(t30)

        t31 = (KEY_TENSIONRUPTURECAP_FLANGE,KEY_DISP_TENSIONRUPTURECAP_FLANGE , TYPE_TEXTBOX,
               round(self.flange_plate.tension_rupture_capacity/1000, 2) if flag else '')
        flangecapacity.append(t31)

        t25 = (KEY_SHEARYIELDINGCAP_FLANGE, KEY_DISP_SHEARYIELDINGCAP_FLANGE, TYPE_TEXTBOX,
               round(self.flange_plate.shear_yielding_capacity/1000, 2) if flag else '')
        flangecapacity.append(t25)

        t26 = (KEY_BLOCKSHEARCAP_FLANGE, KEY_DISP_BLOCKSHEARCAP_FLANGE, TYPE_TEXTBOX,
               round(self.flange_plate.block_shear_capacity/1000, 2) if flag else '')
        flangecapacity.append(t26)

        t27 = ( KEY_SHEARRUPTURECAP_FLANGE,KEY_DISP_SHEARRUPTURECAP_FLANGE,TYPE_TEXTBOX,
               round(self.flange_plate.shear_rupture_capacity/1000, 2) if flag else '')
        flangecapacity.append(t27)

        t28 = (KEY_FLANGE_PLATE_MOM_DEMAND, KEY_FLANGE_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX,
               round(self.flange_plate.moment_demand / 1000000, 2) if flag else '')
        flangecapacity.append(t28)

        t29 = (KEY_FLANGE_PLATE_MOM_CAPACITY, KEY_FLANGE_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX,
               round(self.flange_plate.moment_capacity/1000, 2) if flag else '')
        flangecapacity.append( t29)

        return flangecapacity

    def webcapacity(self, flag):

        webcapacity = []
        t12 = (KEY_SHEARYIELDINGCAP_WEB, KEY_DISP_SHEARYIELDINGCAP_WEB, TYPE_TEXTBOX,
               round(self.web_plate.shear_yielding_capacity/1000, 2) if flag else '')
        webcapacity.append(t12)

        t13 = (KEY_BLOCKSHEARCAP_WEB, KEY_DISP_BLOCKSHEARCAP_WEB, TYPE_TEXTBOX,
               round(self.web_plate.block_shear_capacity/1000, 2) if flag else '')
        webcapacity.append(t13)

        t14 = (KEY_SHEARRUPTURECAP_WEB, KEY_DISP_SHEARRUPTURECAP_WEB, TYPE_TEXTBOX,
               round(self.web_plate.shear_rupture_capacity/1000, 2) if flag else '')
        webcapacity.append(t14)

        t15 = (KEY_WEB_PLATE_MOM_DEMAND, KEY_WEB_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX,
               round(self.web_plate.moment_demand / 1000000, 2) if flag else '')
        webcapacity.append(t15)

        t16 = (KEY_WEB_PLATE_MOM_CAPACITY, KEY_WEB_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX,
               round(self.web_plate.moment_capacity/1000, 2) if flag else '')
        webcapacity.append(t16)
        return webcapacity

    def output_values(self, flag):

        out_list = []

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None)
        out_list.append(t1)

        t2 = (KEY_D, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,
              self.web_bolt.bolt_diameter_provided if flag else '')
        out_list.append(t2)

        t3 = (KEY_GRD, KEY_DISP_GRD, TYPE_TEXTBOX,
              self.web_bolt.bolt_grade_provided if flag else '')
        out_list.append(t3)

        t4 = (None, DISP_TITLE_WEBSPLICEPLATE, TYPE_TITLE, None)
        out_list.append(t4)

        t5 = (KEY_WEB_PLATE_HEIGHT, KEY_DISP_WEB_PLATE_HEIGHT, TYPE_TEXTBOX,
              self.web_plate.height if flag else '' )
        out_list.append(t5)

        t6 = (KEY_WEB_PLATE_LENGTH, KEY_DISP_WEB_PLATE_LENGTH, TYPE_TEXTBOX,
              self.web_plate.length if flag else '')
        out_list.append(t6)

        t7 = (KEY_WEBPLATE_THICKNESS, KEY_DISP_WEBPLATE_THICKNESS, TYPE_TEXTBOX,
              self.web_plate.thickness_provided if flag else '')
        out_list.append(t7)

        t21 = (KEY_WEB_SPACING, KEY_DISP_WEB_SPACING, TYPE_OUT_BUTTON, ['Web Spacing Details', self.webspacing])
        out_list.append(t21)

        t21 = (KEY_WEB_CAPACITY, KEY_DISP_WEB_CAPACITY, TYPE_OUT_BUTTON, ['Web Capacity', self.webcapacity])
        out_list.append(t21)

        t17 = (None, DISP_TITLE_FLANGESPLICEPLATE, TYPE_TITLE, None)
        out_list.append(t17)

        t18 = (KEY_FLANGE_PLATE_HEIGHT, KEY_DISP_FLANGE_PLATE_HEIGHT, TYPE_TEXTBOX,
               self.flange_plate.height if flag else '')
        out_list.append(t18)

        t19 = (
            KEY_FLANGE_PLATE_LENGTH, KEY_DISP_FLANGE_PLATE_LENGTH, TYPE_TEXTBOX,
            self.flange_plate.length if flag else '')
        out_list.append(t19)

        t20 = (KEY_FLANGEPLATE_THICKNESS, KEY_DISP_FLANGESPLATE_THICKNESS, TYPE_TEXTBOX,
               self.flange_plate.thickness_provided if flag else '')
        out_list.append(t20)
        t21 = (
        KEY_FLANGE_SPACING, KEY_DISP_FLANGE_SPACING, TYPE_OUT_BUTTON, ['Flange Spacing Details', self.flangespacing])
        out_list.append(t21)

        t21 = (
            KEY_FLANGE_CAPACITY, KEY_DISP_FLANGE_CAPACITY, TYPE_OUT_BUTTON, ['Flange Capacity', self.flangecapacity])
        out_list.append(t21)

        return out_list

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

        if len(missing_fields_list) > 0:
            QMessageBox.information(window, "Information",
                                    self.generate_missing_fields_error_string(self, missing_fields_list))
            # flag = False
        else:
            flag = True

        if flag:
            self.set_input_values(self, design_dictionary)
        else:
            pass

        # for option in option_list:
        #     if option[0] == KEY_CONN:
        #         continue
        #     s = p.findChild(QtWidgets.QWidget, option[0])
        #
        #     if option[2] == TYPE_COMBOBOX:
        #         if option[0] in [KEY_D, KEY_GRD, KEY_PLATETHK]:
        #             continue
        #         if s.currentIndex() == 0:
        #             missing_fields_list.append(option[1])
        #
        #
        #     elif option[2] == TYPE_TEXTBOX:
        #         if s.text() == '':
        #             missing_fields_list.append(option[1])
        #     else:
        #         pass

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


    def module(self):
        return KEY_DISP_BEAMCOVERPLATE

    def set_input_values(self, design_dictionary):
        super(BeamCoverPlate, self).set_input_values(self, design_dictionary)
        # self.module = design_dictionary[KEY_MODULE]
        # global design_status
        self.design_status = True
        #
        self.module = design_dictionary[KEY_MODULE]
        self.preference = design_dictionary[KEY_FLANGEPLATE_PREFERENCES]

        self.section = Beam(designation=design_dictionary[KEY_SECSIZE],
                              material_grade=design_dictionary[KEY_MATERIAL])

        self.web_bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                             bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
                             bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                             edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                             mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                             corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        self.flange_bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                                bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
                                bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                                edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                                mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                                corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        self.flange_plate = Plate(thickness=design_dictionary.get(KEY_FLANGEPLATE_THICKNESS, None),
                                  material_grade=design_dictionary[KEY_MATERIAL],
                                  gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.web_plate = Plate(thickness=design_dictionary.get(KEY_WEBPLATE_THICKNESS, None),
                               material_grade=design_dictionary[KEY_MATERIAL],
                               gap=design_dictionary[KEY_DP_DETAILING_GAP])
        # print("input values are set. Doing preliminary member checks")
        #
        # self.load.axial_force = self.load.axial_force * 1000
        # self.load.shear_force = self.load.shear_force * 1000
        # self.load.moment = self.load.moment * 1000000

        self.member_capacity(self)

    def member_capacity(self):
        #     # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        #     if self.connectivity in VALUES_CONN_1:
        if self.section.type == "Rolled":
            length = self.section.depth
        else:
            length = self.section.depth - (
                    2 * self.section.flange_thickness)  # -(2*self.supported_section.root_radius)
        #     else:
        #         length = self.supported_section.depth - 50.0  # TODO: Subtract notch height for beam-beam connection

        ###WEB MENBER CAPACITY CHECK

        ###### # capacity Check for web in axial = min(block, yielding, rupture)

        # A_vn_web = ( self.section.depth - 2 * self.section.flange_thickness - self.web_plate.bolts_one_line * self.web_bolt.dia_hole) * self.section.web_thickness
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.web_plate.fy)
        # self.section.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
        #     A_vn=A_vn_web, fu=self.web_plate.fu)

        # print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
        #       self.supported_section.tension_yielding_capacity, self.load.axial_force)

        print("tension_yielding_capacity_web", self.tension_yielding_capacity_web)
        if self.tension_yielding_capacity_web > self.load.axial_force *1000:
            #             self.supported_section.tension_yielding_capacity > self.load.axial_force:
            # print("AAAA Web member check is satisfactory. Doing bolt checks")
            self.design_status = True
            if self.design_status == True:
                self.section.tension_yielding_capacity == self.tension_yielding_capacity_web
            else:
                pass
            ### FLANGE MEMBER CAPACITY CHECK
            # A_vn_flange = (self.section.flange_width - self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole) * \
            #               self.section.flange_thickness
            A_v_flange = self.section.flange_thickness * self.section.flange_width

            self.tension_yielding_capacity_flange = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange,
                fy=self.flange_plate.fy)
            print("tension_yielding_capacity_flange", self.tension_yielding_capacity_flange)
            #
            # self.section.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
            #     A_vn=A_vn_flange,
            #     fu=self.flange_plate.fu)

            if self.tension_yielding_capacity_flange > self.load.axial_force*1000:
                #             self.supported_section.tension_yielding_capacity > self.load.axial_force:
                # print("BBB flange member check is satisfactory. Doing bolt checks")
                self.select_bolt_dia(self)
                self.design_status = True
                if self.design_status == True:
                    self.section.tension_yielding_capacity = self.tension_yielding_capacity_flange
                else:
                    pass
            else:
                self.design_status = False
                logger.error(" : tension_yielding_capacity  {} and/or tension_rupture_capacit{} is less "
                             "than applied loads, Please select larger sections or decrease loads"
                            )
                # print(" BBB failed in flange member checks. Select larger sections or decrease loads")
        else:
            self.design_status = False
            logger.error(" : tension_yielding_capacity  {} and/or tension_rupture_capacit{} is less "
                         "than applied loads, Please select larger sections or decrease loads"
                       )
            # print("BBB failed in web member checks. Select larger sections or decrease loads")

    def module_name(self):
        return KEY_DISP_COLUMNCOVERPLATE

    def select_bolt_dia(self):
        min_plate_height = self.section.flange_width
        max_plate_height = self.section.flange_width
        axial_force_f = self.load.axial_force * 1000 * self.section.flange_width * self.section.flange_thickness / (
                self.section.area * 100)
        flange_force = (((self.load.moment * 1000000) / (self.section.depth - self.section.flange_thickness)) + (
            axial_force_f))
        print("flange_force",flange_force )

        self.res_force = math.sqrt((self.load.shear_force *1000)** 2 + (self.load.axial_force*1000) ** 2)
        self.flange_plate.thickness_provided = max(min(self.flange_plate.thickness),
                                                   math.ceil(self.section.flange_thickness))
        bolts_required_previous = 2
        bolt_diameter_previous = self.flange_bolt.bolt_diameter[-1]

        # res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000
        self.flange_bolt.bolt_grade_provided = self.flange_bolt.bolt_grade[-1]
        count = 0
        bolts_one_line = 1

        for self.flange_bolt.bolt_diameter_provided in reversed(self.flange_bolt.bolt_diameter):
            self.flange_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
                                                           connecting_plates_tk=[self.flange_plate.thickness[0],
                                                                                 self.section.flange_thickness])
            self.flange_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
                                                           connecting_plates_tk=[self.flange_plate.thickness[0],
                                                                                 self.section.flange_thickness])

            if self.preference == "Outside":
                self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
                                                         bolt_grade_provided=self.flange_bolt.bolt_grade[0],
                                                         connecting_plates_tk=[self.flange_plate.thickness[0],
                                                                               self.section.flange_thickness],
                                                         n_planes=1)
            else:
                self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
                                                         bolt_grade_provided=self.flange_bolt.bolt_grade[0],
                                                         connecting_plates_tk=[self.flange_plate.thickness[0],
                                                                               self.section.flange_thickness],
                                                         n_planes=2)

            self.flange_plate.bolts_required = (1.05 * (flange_force / (self.flange_bolt.bolt_capacity)))
            [bolt_line, bolts_one_line, flange_plate_h] = self.flange_plate.get_web_plate_l_bolts_one_line(
                web_plate_h_max=max_plate_height, web_plate_h_min=min_plate_height,
                bolts_required=self.flange_plate.bolts_required, edge_dist=self.flange_bolt.min_edge_dist_round,
                gauge=self.flange_bolt.min_gauge_round)
            self.flange_plate.bolts_required = bolt_line * bolts_one_line

            if self.flange_plate.bolts_required > bolts_required_previous and count >= 1:
                self.flange_bolt.bolt_grade_provided = bolt_grade_previous
                self.flange_plate.bolts_required = bolts_required_previous
                break
            bolts_required_previous = self.flange_plate.bolts_required
            bolt_grade_previous = self.flange_bolt.bolt_grade_provided
            count += 1

            self.flange_plate.get_web_plate_details(bolt_dia=self.flange_bolt.bolt_diameter[0],
                                                    web_plate_h_min=min_plate_height,
                                                    web_plate_h_max=max_plate_height,
                                                    bolt_capacity=self.flange_bolt.bolt_capacity,
                                                    min_edge_dist=self.flange_bolt.max_end_dist_round,
                                                    min_gauge=self.flange_bolt.min_gauge_round,
                                                    max_spacing=self.flange_bolt.max_spacing,
                                                    max_edge_dist=self.flange_bolt.max_edge_dist,
                                                    axial_load=flange_force,
                                                    shear_ecc=False)

            # print("check",self.flange_bolt.bolt_capacity, self.flange_bolt.bolt_grade_provided, self.flange_plate.bolts_required, self.flange_plate.bolts_one_line)

        # def get_bolt_details(self):
        #     # global design_status
        #
        #     self.flange_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
        #                                             connecting_plates_tk=[self.flange_plate.thickness[0],
        #                                                                   self.section.flange_thickness])
        #
        #
        #     if self.preference == "Outside":
        #         self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
        #                                       bolt_grade_provided=self.flange_bolt.bolt_grade[0],
        #                                       connecting_plates_tk=[self.flange_plate.thickness[0],
        #                                                             self.section.flange_thickness],
        #                                       n_planes=1)
        #     else:
        #         self.flange_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.flange_bolt.bolt_diameter[0],
        #                                       bolt_grade_provided=self.flange_bolt.bolt_grade[0],
        #                                       connecting_plates_tk=[self.flange_plate.thickness[0],
        #                                                             self.section.flange_thickness],
        #                                       n_planes=2)
        #
        #
        #     min_plate_height = self.section.flange_width
        #     max_plate_height = self.section.flange_width
        #     axial_force_f = self.load.axial_force * 1000 * self.section.flange_width * self.section.flange_thickness / (
        #                 self.section.area * 100)
        #     flange_force = (((self.load.moment * 1000000) / (self.section.depth - self.section.flange_thickness)) + (
        #         axial_force_f))
        #     flange_force = flange_force / 1000
        #
        #     self.flange_plate.get_web_plate_details(bolt_dia=self.flange_bolt.bolt_diameter[0], web_plate_h_min=min_plate_height,
        #                                      web_plate_h_max=max_plate_height, bolt_capacity=self.flange_bolt.bolt_capacity,
        #                                      min_edge_dist=self.flange_bolt.max_end_dist_round, min_gauge = self.flange_bolt.min_gauge_round,
        #                                             max_spacing = self.flange_bolt.max_spacing, max_edge_dist = self.flange_bolt.max_edge_dist,
        #                                             axial_load=flange_force,
        #                                      shear_ecc=False)

        # end_dist_temp = self.flange_plate.end_dist_provided
        # gauge_temp = self.flange_plate.gauge_provided
        # self.flange_plate.end_dist_provided = self.flange_plate.edge_dist_provided
        # self.flange_plate.gauge_provided = self.flange_plate.pitch_provided
        # self.flange_plate.edge_dist_provided = end_dist_temp
        # self.flange_plate.pitch_provided = gauge_temp

        block_shear_capactity = 0
        moment_capacity = 0
        self.flange_plate.get_moment_cacacity(self.flange_plate.fy, self.flange_plate.thickness[0],
                                              self.flange_plate.length)
        ###### # capacity Check for flange = min(block, yielding, rupture)

        ###### # capacity Check for flange = min(block, yielding, rupture)

        #### Block shear capacity of  flange ###

        A_vn_flange = (self.section.flange_width - self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole) * \
                      self.section.flange_thickness
        A_v_flange = self.section.flange_thickness * self.flange_plate.height

        self.section.shear_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_flange,
            fy=self.flange_plate.fy)

        self.section.shear_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_vn_flange,
            fu=self.flange_plate.fu)
        #  Block shear strength for flange
        design_status_block_shear = False
        edge_dist = self.flange_plate.edge_dist_provided
        end_dist = self.flange_plate.end_dist_provided
        gauge = self.flange_plate.gauge_provided
        pitch = self.flange_plate.pitch_provided

        while design_status_block_shear == False:

            Avg = 2 * (end_dist + (
                    self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) \
                  * self.section.flange_thickness
            Avn = 2 * (self.flange_plate.end_dist_provided + (
                    self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided - (
                               self.flange_plate.bolt_line - 0.5) * self.flange_bolt.dia_hole) * \
                  self.section.flange_thickness
            Atg = (self.section.flange_width - (
                    self.flange_plate.bolts_one_line - 1) * self.flange_plate.gauge_provided) \
                  * self.section.flange_thickness
            Atn = (self.section.flange_width - (
                    (self.flange_plate.bolts_one_line - 1) * self.flange_plate.gauge_provided)
                   - (self.flange_plate.bolts_one_line - 1) * self.flange_bolt.dia_hole) * \
                  self.section.flange_thickness
            # print(Avg, Avn, Atg, Atn)
            # print(8, self.flange_plate.bolt_line, pitch, end_dist)

            self.section.block_shear_capacity = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn, A_tg=Atg,
                                                                                  A_tn=Atn,
                                                                                  f_u=self.flange_plate.fu,
                                                                                  f_y=self.flange_plate.fy)
            # print(9,  self.flange_plate.block_shear_capacity, self.load.axial_force, self.flange_plate.pitch_provided)

            if self.flange_plate.block_shear_capacity < self.load.axial_force*1000:
                if self.flange_bolt.max_spacing_round >= pitch + 5 and self.flange_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                    if self.flange_plate.bolt_line == 1:
                        end_dist += 5
                    else:
                        pitch += 5

                else:
                    break

            else:
                design_status_block_shear = True
                break

        # if design_status_block_shear is True:
        #     break

        axial_force_f = self.load.axial_force * 1000 * self.section.flange_width * self.section.flange_thickness / (
                    self.section.area * 100)
        flange_force = (((self.load.moment * 1000000) / (self.section.depth - self.section.flange_thickness)) + (
            axial_force_f))
        flange_force = flange_force

        self.Tension_capacity_flange = min(self.section.shear_yielding_capacity, self.section.shear_rupture_capacity,
                                           self.section.block_shear_capacity)

        if self.Tension_capacity_flange < flange_force:
            self.design_status = False
            logger.warning(": Tension capacity flange is less than required flange force kN Select larger beam section")

        else:
            pass

        # capacity Check for flange_outsite_plate =min(block, yielding, rupture)

        ####Capacity of flange cover plate for bolted Outside #
        print(self.preference)
        if self.preference == "Outside":
            print(self.preference)
            A_vn_flange = (self.section.flange_width - self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole) * \
                          self.flange_plate.thickness[0]
            A_v_flange = self.flange_plate.thickness[0] * self.flange_plate.height
            self.flange_plate.shear_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange,
                fy=self.flange_plate.fy)

            self.flange_plate.shear_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_vn_flange,
                fu=self.flange_plate.fu)

            #  Block shear strength for outside flange plate
            available_flange_thickness = list(
                [x for x in self.flange_plate.thickness if (self.section.flange_thickness <= x)])
            # print(111,self.flange_plate.pitch_provided)
            # print(available_flange_thickness,self.flange_plate.thickness)
            for self.flange_plate.thickness_provided in available_flange_thickness:
                design_status_block_shear = False
                edge_dist = self.flange_plate.edge_dist_provided
                end_dist = self.flange_plate.end_dist_provided
                gauge = self.flange_plate.gauge_provided
                pitch = self.flange_plate.pitch_provided
                # print(1)
                #### Block shear capacity of flange plate ###

                while design_status_block_shear == False:

                    Avg = 2 * (self.flange_plate.end_dist_provided + (
                            self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) * self.flange_plate.thickness_provided
                    Avn = 2 * (self.flange_plate.end_dist_provided + (
                            self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided - (
                                       self.flange_plate.bolt_line - 0.5) * self.flange_bolt.dia_hole) * \
                          self.flange_plate.thickness_provided
                    Atg = ((self.flange_plate.bolts_one_line - 1) * self.flange_plate.gauge_provided) * \
                          self.flange_plate.thickness_provided
                    Atn = (((self.flange_plate.bolts_one_line - 1) * self.flange_plate.gauge_provided) - (
                            self.flange_plate.bolts_one_line - 1) * self.flange_bolt.dia_hole) * self.flange_plate.thickness_provided

                    # print(8, self.flange_plate.bolt_line, pitch, end_dist, self.flange_plate.thickness_provided)

                    self.flange_plate.block_shear_capacity = self.block_shear_strength_plate(A_vg=Avg, A_vn=Avn,
                                                                                             A_tg=Atg,
                                                                                             A_tn=Atn,
                                                                                             f_u=self.flange_plate.fu,
                                                                                             f_y=self.flange_plate.fy)

                    # print(9, self.flange_plate.thickness_provided, self.flange_plate.block_shear_capacity, self.load.axial_force,
                    #       self.flange_plate.pitch_provided)
                    if self.flange_plate.block_shear_capacity < self.load.axial_force *1000:
                        if self.flange_bolt.max_spacing_round >= pitch + 5 and self.flange_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                            if self.flange_plate.bolt_line == 1:
                                end_dist += 5
                            else:
                                pitch += 5

                        else:
                            design_status_block_shear = False
                            break

                        # print(Avg, Avn, Atg, Atn)
                    else:
                        design_status_block_shear = True
                        break
                # print(design_status_block_shear)
                if design_status_block_shear is True:
                    break

            self.Tension_capacity_flange = min(self.flange_plate.shear_yielding_capacity,
                                                self.flange_plate.shear_rupture_capacity,
                                                self.flange_plate.block_shear_capacity)

            if self.Tension_capacity_flange < flange_force:
                self.design_status = False
                logger.warning(": Tension capacity flange is less than required flange force kN")
                logger.info(": Increase the size of Beam section")

            else:
                pass
        else:
            # capacity Check for flange_outsite_plate =min(block, yielding, rupture)

            #  yielding,rupture  for  inside flange plate
            flange_plate_height_inside = (
                                                     self.section.flange_width - self.section.web_thickness - self.section.root_radius) / 2 - \
                                         self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole
            flange_plate_height_outside = self.flange_plate.thickness_provided * self.flange_plate.height
            A_vn_flange = ((self.flange_plate.height - self.section.web_thickness - 2 * self.section.root_radius) / 2 *
                           self.flange_plate.thickness_provided) / 2
            A_v_flange = (flange_plate_height_outside * self.flange_plate.thickness_provided) + \
                         2 * (flange_plate_height_inside * self.flange_plate.thickness_provided)

            self.flange_plate.shear_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange,
                fy=self.flange_plate.fy)
            flange_plate_height_inside = (
                                                     self.section.flange_width - self.section.web_thickness - self.section.root_radius) / 2 - \
                                         self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole

            self.flange_plate.shear_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_vn_flange,
                fu=self.flange_plate.fu)

            #  Block shear strength for outside + inside flange plate

            # OUTSIDE
            available_flange_thickness = list(
                [x for x in self.flange_plate.thickness if (self.section.flange_thickness <= x)])
            # print(111,self.flange_plate.pitch_provided)
            # print(available_flange_thickness,self.flange_plate.thickness)
            for self.flange_plate.thickness_provided in available_flange_thickness:
                design_status_block_shear = False
                edge_dist = self.flange_plate.edge_dist_provided
                end_dist = self.flange_plate.end_dist_provided
                gauge = self.flange_plate.gauge_provided
                pitch = self.flange_plate.pitch_provided
                # print(11)
                #### Block shear capacity of flange plate ###

                while design_status_block_shear == False:

                    Avg = 2 * (self.flange_plate.end_dist_provided + (
                            self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) * self.flange_plate.thickness_provided
                    Avn = 2 * (self.flange_plate.end_dist_provided + (
                            self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided - (
                                       self.flange_plate.bolt_line - 0.5) * self.flange_bolt.dia_hole) * \
                          self.flange_plate.thickness_provided
                    Atg = ((self.flange_plate.bolts_one_line - 1) * self.flange_plate.gauge_provided) * \
                          self.flange_plate.thickness_provided
                    Atn = (((self.flange_plate.bolts_one_line - 1) * self.flange_plate.gauge_provided) - (
                            self.flange_plate.bolts_one_line - 1) * self.flange_bolt.dia_hole) * self.flange_plate.thickness_provided
                    # print(12, self.flange_plate.bolt_line, pitch, end_dist, self.flange_plate.thickness_provided)

                    flange_plate_block_shear_capactity_outside = self.block_shear_strength_plate(A_vg=Avg, A_vn=Avn,
                                                                                                 A_tg=Atg,
                                                                                                 A_tn=Atn,
                                                                                                 f_u=self.flange_plate.fu,
                                                                                                 f_y=self.flange_plate.fy)

                    #  Block shear strength for inside flange plate under shear
                    Avg = 2 * (self.flange_plate.end_dist_provided + (
                            self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided) \
                          * self.flange_plate.thickness_provided
                    Avn = 2 * (self.flange_plate.end_dist_provided + (
                            self.flange_plate.bolt_line - 1) * self.flange_plate.pitch_provided - (
                                       self.flange_plate.bolt_line - 0.5) * self.flange_bolt.dia_hole) * \
                          self.flange_plate.thickness_provided
                    Atg = (self.section.flange_width - (
                                self.flange_plate.bolt_line - 1) * self.flange_plate.gauge_provided) * \
                          self.flange_plate.thickness_provided
                    Atn = (self.section.flange_width - (
                            (self.flange_plate.bolt_line - 1) * self.flange_plate.gauge_provided) - (
                                   self.flange_plate.bolt_line - 1) * self.flange_bolt.dia_hole) * self.flange_plate.thickness_provided
                    # print(13, self.flange_plate.bolt_line, pitch, end_dist, self.flange_plate.thickness_provided)

                    flange_plate_block_shear_capacity_inside = self.block_shear_strength_plate(A_vg=Avg, A_vn=Avn,
                                                                                               A_tg=Atg,
                                                                                               A_tn=Atn,
                                                                                               f_u=self.flange_plate.fu,
                                                                                               f_y=self.flange_plate.fy)
                    self.flange_plate.block_shear_capacity = flange_plate_block_shear_capactity_outside + flange_plate_block_shear_capacity_inside

                    # print(14, self.flange_plate.thickness_provided, self.flange_plate.block_shear_capacity,
                    #       self.load.axial_force,
                    #       self.flange_plate.pitch_provided)
                    if self.flange_plate.block_shear_capacity < self.load.axial_force * 1000:
                        if self.flange_bolt.max_spacing_round >= pitch + 5 and self.flange_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                            if self.flange_plate.bolt_line == 1:
                                end_dist += 5
                            else:
                                pitch += 5

                        else:
                            design_status_block_shear = False
                            break

                        # print(Avg, Avn, Atg, Atn)
                        # logger.error(": flange_plate_t is less than min_thk_flange_plate:")
                        # logger.warning(": Minimum flange_plate_t required is %2.2f mm" % (min_thk_flange_plate))
                    else:
                        design_status_block_shear = True
                        break
                # print(design_status_block_shear)
                if design_status_block_shear is True:
                    break
            # print(design_status_block_shear)
            # self.flange_plate.end_dist_provided = end_dist
            # self.flange_plate.gauge_provided = gauge
            # self.flange_plate.pitch_provided = pitch
            self.Tension_capacity_flange_= min(self.flange_plate.shear_yielding_capacity,
                                                self.flange_plate.shear_rupture_capacity,
                                                self.flange_plate.block_shear_capacity)
            if self.Tension_capacity_flange < flange_force:
                self.design_status = False
                logger.warning(": Tension capacity flange is less than required flange force kN")
                logger.info(": Increase the size of Beam section")

            else:
                pass
            # print(300, design_status)
        ##########################################################################
        # Design of web splice plate
        self.web_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.web_bolt.bolt_diameter[0],
                                                    connecting_plates_tk=[self.web_plate.thickness[0],
                                                                          self.section.web_thickness])
        min_web_plate_height = self.section.min_plate_height()
        max_web_plate_height = self.section.max_plate_height()
        axial_force_w = int(((self.section.depth - 2 * (
            self.section.flange_thickness)) * self.section.web_thickness * self.load.axial_force * 10) / self.section.area)

        self.web_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.web_bolt.bolt_diameter[0],
                                              bolt_grade_provided=self.web_bolt.bolt_grade[0],
                                              connecting_plates_tk=[self.web_plate.thickness[0],
                                                                    self.section.web_thickness],
                                              n_planes=2)

        self.web_plate.get_web_plate_details(bolt_dia=self.web_bolt.bolt_diameter[0],
                                             web_plate_h_min=min_web_plate_height,
                                             web_plate_h_max=max_web_plate_height,
                                             bolt_capacity=self.web_bolt.bolt_capacity,
                                             min_edge_dist=self.web_bolt.max_end_dist_round,
                                             min_gauge=self.web_bolt.min_gauge_round,
                                             max_spacing=self.web_bolt.max_spacing_round,
                                             max_edge_dist=self.web_bolt.max_edge_dist
                                             , shear_load=self.load.shear_force * 1000, axial_load=axial_force_w,
                                             gap=self.web_plate.gap, shear_ecc=True)

        block_shear_capacity = 0
        moment_capacity = 0
        self.web_plate.get_moment_cacacity(self.web_plate.fy, self.web_plate.thickness[0],
                                           self.web_plate.length)

        ################################ CAPACITY CHECK FOR WEB #####################################################################################

        ###### # capacity Check for web in axial = min(block, yielding, rupture)

        A_vn_web = (
                               self.section.depth - 2 * self.section.flange_thickness - self.web_plate.bolts_one_line * self.web_bolt.dia_hole) * self.section.web_thickness
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.section.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.web_plate.fy)
        self.section.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_vn_web, fu=self.web_plate.fu)

        # available_web_thickness = list([x for x in self.web_plate.thickness if (self.section.web_thickness <= x)])
        # print(111,self.web_plate.pitch_provided)
        # print(available_web_thickness,self.web_plate.thickness)
        design_status_block_shear = False
        edge_dist = self.web_plate.edge_dist_provided
        end_dist = self.web_plate.end_dist_provided
        gauge = self.web_plate.gauge_provided
        pitch = self.web_plate.pitch_provided
        # print(1)

        #### Block shear capacity of web in axial ###

        while design_status_block_shear == False:
            # print(design_status_block_shear)
            # print(0, self.web_plate.max_end_dist, self.web_plate.end_dist_provided, self.web_plate.max_spacing_round, self.web_plate.pitch_provided)
            Atg = (self.web_plate.edge_dist_provided + (
                    self.web_plate.bolts_one_line - 1) * gauge) * self.section.web_thickness
            Atn = (self.web_plate.edge_dist_provided + (
                    self.web_plate.bolts_one_line - 1) * gauge - (
                           self.web_plate.bolts_one_line - 0.5) * self.web_bolt.dia_hole) * self.section.web_thickness
            Avg = 2 * ((self.web_plate.bolt_line - 1) * pitch + end_dist) * \
                  self.section.web_thickness
            Avn = 2 * ((self.web_plate.bolt_line - 1) * pitch + (
                    self.web_plate.bolt_line - 1) * self.web_bolt.dia_hole + end_dist) * \
                  self.section.web_thickness
            # print(17,self.web_plate.bolt_line, self.web_plate.pitch_provided, self.web_plate.bolt_line,
            #      self.web_bolt.dia_hole, self.web_plate.end_dist_provided, self.web_plate.thickness_provided)
            # print(18, self.web_plate.bolt_line, pitch, end_dist, self.section.web_thickness)

            self.web_plate.block_shear_capacity = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn, A_tg=Atg,
                                                                                    A_tn=Atn,
                                                                                    f_u=self.web_plate.fu,
                                                                                    f_y=self.web_plate.fy)
            # print(19, self.web_plate.thickness_provided, self.web_plate.block_shear_capacity, self.load.axial_force, self.web_plate.pitch_provided)
            if self.web_plate.block_shear_capacity < self.load.axial_force *1000:
                if self.web_bolt.max_spacing_round >= pitch + 5 and self.web_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                    if self.web_plate.bolt_line == 1:
                        end_dist += 5
                    else:
                        pitch += 5

                else:
                    design_status_block_shear = False
                    break

                # print(Avg, Avn, Atg, Atn)
                # logger.error(": flange_plate_t is less than min_thk_flange_plate:")
                # logger.warning(": Minimum flange_plate_t required is %2.2f mm" % (min_thk_flange_plate))
            else:
                design_status_block_shear = True
                break
        Tension_capacity_web_plate = min(self.section.shear_yielding_capacity, self.section.shear_rupture_capacity,
                                         self.section.block_shear_capacity)
        self.webforce = self.web_force(column_d=self.section.depth, column_f_t=self.section.flange_thickness,
                                       column_t_w=self.section.web_thickness,
                                       axial_force=self.load.axial_force , column_area=self.section.area)
        if Tension_capacity_web_plate < self.webforce:
            self.design_status = False
            logger.warning(": Tension capacity web_plate is less than required web force kN Select larger beam section")  # todo

        else:
            pass

        ###### # capacity Check for web plate in axial = min(block, yielding, rupture)
        A_vn_web = (self.web_plate.height - (
                    self.web_plate.bolts_one_line * self.web_bolt.dia_hole)) * self.section.web_thickness
        A_v_web = self.web_plate.height * self.section.web_thickness
        self.section.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.web_plate.fy)
        self.section.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_vn_web, fu=self.web_plate.fu)

        available_web_thickness = list([x for x in self.web_plate.thickness if (self.section.web_thickness <= x)])
        # print(111,self.web_plate.pitch_provided)
        # print(available_web_thickness,self.web_plate.thickness)
        for self.web_plate.thickness_provided in available_web_thickness:
            design_status_block_shear = False
            edge_dist = self.web_plate.edge_dist_provided
            end_dist = self.web_plate.end_dist_provided
            gauge = self.web_plate.gauge_provided
            pitch = self.web_plate.pitch_provided
            # print(1)

            #### Block shear capacity of web plate in axial ###

            while design_status_block_shear == False:
                # print(design_status_block_shear)
                # print(0, self.web_plate.max_end_dist, self.web_plate.end_dist_provided, self.web_plate.max_spacing_round, self.web_plate.pitch_provided)
                Avg = 2 * ((self.web_plate.bolt_line - 1) * pitch + end_dist) * \
                      self.web_plate.thickness_provided
                Avn = 2 * ((self.web_plate.bolt_line - 1) * pitch + (
                        self.web_plate.bolt_line - 1) * self.web_bolt.dia_hole + end_dist) * \
                      self.web_plate.thickness_provided
                Atg = (self.web_plate.edge_dist_provided + (
                        self.web_plate.bolts_one_line - 1) * gauge) * self.web_plate.thickness_provided
                Atn = (self.web_plate.edge_dist_provided + (
                        self.web_plate.bolts_one_line - 1) * gauge - (
                               self.web_plate.bolts_one_line - 0.5) * self.web_bolt.dia_hole) * self.web_plate.thickness_provided

                # print(self.web_plate.bolt_line, self.web_plate.pitch_provided, self.web_plate.bolt_line,
                # self.web_plate.dia_hole, self.web_plate.end_dist_provided, self.web_plate.thickness_provided)
                # print(1, self.web_plate.bolt_line, pitch, end_dist, self.web_plate.thickness_provided)

                self.web_plate.block_shear_capacity = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn, A_tg=Atg,
                                                                                        A_tn=Atn,
                                                                                        f_u=self.web_plate.fu,
                                                                                        f_y=self.web_plate.fy)
                # print(2, self.web_plate.thickness_provided, self.web_plate.block_shear_capacity, self.load.axial_force, self.web_plate.pitch_provided)
                if self.web_plate.block_shear_capacity < self.load.axial_force *1000:
                    if self.web_bolt.max_spacing_round >= pitch + 5 and self.web_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                        if self.web_plate.bolt_line == 1:
                            end_dist += 5
                        else:
                            pitch += 5

                    else:
                        break

                else:
                    design_status_block_shear = True
                    break
            Tension_capacity_web_plate = min( self.section.tension_yielding_capacity , self.section.tension_rupture_capacity,
                                             self.section.block_shear_capacity)
            self.webforce = self.web_force(column_d=self.section.depth, column_f_t=self.section.flange_thickness,
                                           column_t_w=self.section.web_thickness,
                                           axial_force=self.load.axial_force, column_area=self.section.area)
            if Tension_capacity_web_plate < self.webforce:
                self.design_status = False
                logger.warning(": Tension capacity web_plate is less than required web force kN Select larger beam section")  # todo

            else:
                pass

        ###### # capacity Check for web plate  in shear = min(block, yielding, rupture)

        A_vn_web = (self.web_plate.height - (self.web_plate.bolts_one_line * self.web_bolt.dia_hole)) * \
                   self.web_plate.thickness[0]
        A_v_web = self.web_plate.height * self.web_plate.thickness[0]
        self.web_plate.shear_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=A_vn_web)
        self.web_plate.shear_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_vn_web, fu=self.web_plate.fu)

        available_web_thickness = list([x for x in self.web_plate.thickness if (self.section.web_thickness <= x)])
        # print(111,self.web_plate.pitch_provided)
        # print(available_web_thickness,self.web_plate.thickness)
        for self.web_plate.thickness_provided in available_web_thickness:  #
            design_status_block_shear = False
            edge_dist = self.web_plate.edge_dist_provided
            end_dist = self.web_plate.end_dist_provided
            gauge = self.web_plate.gauge_provided
            pitch = self.web_plate.pitch_provided
            # print(1)

            #### Block shear capacity of web plate ###

            while design_status_block_shear == False:
                Avg = ((
                                   self.web_plate.bolt_line - 1) * self.web_plate.pitch_provided + self.web_plate.end_dist_provided) * self.web_plate.thickness_provided
                Avn = ((self.web_plate.bolt_line - 1) * self.web_plate.pitch_provided + (
                            self.web_plate.bolt_line - 1) * self.web_bolt.dia_hole + self.web_plate.end_dist_provided) * self.web_plate.thickness_provided
                Atg = (self.web_plate.edge_dist_provided + (
                            self.web_plate.bolts_one_line - 1) * self.web_plate.gauge_provided) * self.web_plate.thickness_provided
                Atn = (self.web_plate.edge_dist_provided + (
                            self.web_plate.bolts_one_line - 1) * self.web_plate.gauge_provided - (
                               self.web_plate.bolts_one_line - 0.5) * self.web_bolt.dia_hole) * self.web_plate.thickness_provided
                self.web_plate.block_shear_capacity = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn, A_tg=Atg,
                                                                                        A_tn=Atn,
                                                                                        f_u=self.web_plate.fu,
                                                                                        f_y=self.web_plate.fy)

                # print(2, self.web_plate.thickness_provided, self.web_plate.block_shear_capacity, self.load.axial_force, self.web_plate.pitch_provided)
                if self.web_plate.block_shear_capacity < self.load.axial_force *1000:
                    if self.web_bolt.max_spacing_round >= pitch + 5 and self.web_bolt.max_end_dist_round >= end_dist + 5:  # increase thickness todo
                        if self.web_plate.bolt_line == 1:
                            end_dist += 5
                        else:
                            pitch += 5

                    else:
                        design_status_block_shear = False
                        break

                    # print(Avg, Avn, Atg, Atn)
                    # logger.error(": flange_plate_t is less than min_thk_flange_plate:")
                    # logger.warning(": Minimum flange_plate_t required is %2.2f mm" % (min_thk_flange_plate))
                else:
                    design_status_block_shear = True
                    break
                # print(design_status_block_shear)
            if design_status_block_shear is True:
                break
            Tension_capacity_web_plate = min(self.section.shear_yielding_capacity, self.section.shear_rupture_capacity,
                                             self.section.block_shear_capacity)
        self.webforce = self.web_force(column_d=self.section.depth, column_f_t=self.section.flange_thickness,
                                       column_t_w=self.section.web_thickness,
                                       axial_force=self.load.axial_force, column_area=self.section.area)
        if Tension_capacity_web_plate < self.webforce:
            self.design_status = False
            logger.warning(": Tension capacity web_plate is less than required web force kN Select larger beam section") # todo

        else:
            pass
        # print(600, design_status)

        print(self.section)
        print(self.load)
        # print(self.flange_bolt)
        # print(self.flange_plate)
        # print(self.web_bolt)
        print(self.web_plate)
        print(self.web_plate.thickness_provided)
        print(self.flange_plate.thickness_provided)
        #print(design_status)

        if self.design_status == True:

            logger.error(": Overall bolted cover plate splice connection design is safe \n")
            logger.debug(" :=========End Of design===========")
        else:
            logger.error(": Design is not safe \n ")
            logger.debug(" :=========End Of design===========")

        ################################ CAPACITY CHECK #####################################################################################

    @staticmethod
    def block_shear_strength_plate(A_vg, A_vn, A_tg, A_tn, f_u, f_y):  # for flange plate
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
        Tdb = round(Tdb , 3)
        return Tdb

        # Function for block shear capacity calculation

    @staticmethod
    def block_shear_strength_section(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
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
        Tdb = round(Tdb , 3)
        return Tdb
        # cl 6.2 Design Strength Due to Yielding of Gross Section

    @staticmethod
    def tension_member_design_due_to_yielding_of_gross_section(A_v, fy):
        '''
             Args:
                 A_v (float) Area under shear
                 Beam_fy (float) Yield stress of Beam material
             Returns:
                 Capacity of Beam web in shear yielding
             '''
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        # A_v = height * thickness
        tdg = (A_v * fy) / (gamma_m0 )
        return tdg

    @staticmethod
    def tension_member_design_due_to_rupture_of_critical_section(A_vn, fu):
        '''
               Args:
                   A_vn (float) Net area under shear
                   Beam_fu (float) Ultimate stress of Beam material
               Returns:
                   Capacity of beam web in shear rupture
               '''

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        # A_vn = (height- bolts_one_line * dia_hole) * thickness
        T_dn = 0.9 * A_vn * fu / (gamma_m1)
        return T_dn

    def web_force(column_d, column_f_t, column_t_w, axial_force, column_area):
        """
        Args:
           c_d: Overall depth of the column section in mm (float)
           column_f_t: Thickness of flange in mm (float)
           column_t_w: Thickness of flange in mm (float)
           axial_force: Factored axial force in kN (float)

        Returns:
            Force in flange in kN (float)
        """
        axial_force_w = int(
            ((column_d - 2 * (column_f_t)) * column_t_w * axial_force * 10) / column_area)   # N
        return round(axial_force_w)


    # def flange_force(column_d, column_f_t, column_b, column_area, factored_axial_force, moment_load):
    #     """
    #     Args:
    #        Column_d: Overall depth of the column section in mm (float)
    #        Column_b: width of the column section in mm (float)
    #        Column_f_t: Thickness of flange in mm (float)
    #        axial_force: Factored axial force in kN (float)
    #        moment_load: Factored bending moment in kN-m (float)
    #     Returns:
    #         Force in flange in kN (float)
    #     """
    #
    #     area_f = column_b * column_f_t
    #     axial_force_f = ((area_f * factored_axial_force * 1000 / (100 * column_area))) / 1000  # KN
    #     f_f = (((moment_load * 1000000) / (column_d - column_f_t)) + (axial_force_f * 1000)) / 1000  # KN
    #     # print(f_f)
    #     return (f_f)

    # print(self.web_bolt)
    # print(self.web_plate)
    # print(self.Tension_capacity_flange_plate)
    # print(self.Tension_capacity_flange)

    def call_3DModel(self,ui,bgcolor):
        # Call to calculate/create the BB Cover Plate Bolted CAD model
        # status = self.resultObj['Bolt']['status']
        # if status is True:
        #     self.createBBCoverPlateBoltedCAD()
        #     self.ui.btn3D.setChecked(Qt.Checked)
        if ui.btn3D.isChecked():
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.chkBxFinplate.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)

        # Call to display the BB Cover Plate Bolted CAD model
        #     ui.Commondisplay_3DModel("Model", bgcolor)  # "gradient_bg")
        ui.commLogicObj.display_3DModel("Model",bgcolor)

        # else:
        #     self.display.EraseAll()

    def call_3DBeam(self, ui, bgcolor):
        # status = self.resultObj['Bolt']['status']
        # if status is True:
        #     self.ui.chkBx_beamSec1.setChecked(Qt.Checked)
        if ui.chkBxBeam.isChecked():
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
        # self.display_3DModel("Beam", bgcolor)
        ui.commLogicObj.display_3DModel("Beam",bgcolor)


    def call_3DConnector(self, ui, bgcolor):
        # status = self.resultObj['Bolt']['status']
        # if status is True:
        #     self.ui.chkBx_extndPlate.setChecked(Qt.Checked)
        if ui.chkBxFinplate.isChecked():
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
        # self.display_3DModel("Connector", bgcolor)
        ui.commLogicObj.display_3DModel("Connector", bgcolor)