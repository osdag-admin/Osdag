"created by anjali"

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


class BeamCoverPlateWeld(MomentConnection):

    def __init__(self):
        super(BeamCoverPlateWeld, self).__init__()
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

        if KEY_DP_WELD_TYPE in existingvalues:
            existingvalue_key_weld_type = existingvalues[KEY_DP_WELD_TYPE]
        else:
            existingvalue_key_weld_type = ''


        # if KEY_D in existingvalues:
        #     existingvalue_key_d = existingvalues[KEY_D]
        # else:
        #     existingvalue_key_d = ''

        # if KEY_TYP in existingvalues:
        #     existingvalue_key_typ = existingvalues[KEY_TYP]
        # else:
        #     existingvalue_key_typ = ''

        # if KEY_GRD in existingvalues:
        #     existingvalue_key_grd = existingvalues[KEY_GRD]
        # else:
        #     existingvalue_key_grd = ''

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

        t16 = (KEY_MODULE, KEY_DISP_BEAMCOVERPLATEWELD, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)


        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, existingvalue_key_secsize, connectdb("Beams"))
        options_list.append(t4)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        options_list.append(t15)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)
        t19 = (
            KEY_WELD_TYPE, KEY_DISP_WELD_TYPE, TYPE_COMBOBOX, existingvalue_key_weld_type,
            VALUES_WELD_TYPE)
        options_list.append(t19)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

        t17 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX,existingvalues_key_moment,None)
        options_list.append(t17)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None)
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None)
        options_list.append(t8)

        # t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None)
        # options_list.append(t9)

        # t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D)
        # options_list.append(t10)

        # t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        #         # options_list.append(t11)
        #         #
        # t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        # options_list.append(t12)

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

    # def flangespacing(self, flag):
    #
    #     flangespacing = []
    #
    #     t21 = (KEY_FLANGE_PITCH, KEY_DISP_FLANGE_PLATE_PITCH, TYPE_TEXTBOX,
    #            self.flange_plate.pitch_provided )
    #     flangespacing.append(t21)
    #
    #     t22 = (KEY_ENDDIST_FLANGE, KEY_DISP_END_DIST_FLANGE, TYPE_TEXTBOX,
    #            self.flange_plate.end_dist_provided)
    #     flangespacing.append(t22)
    #
    #     t23 = (KEY_FLANGE_PLATE_GAUGE, KEY_DISP_FLANGE_PLATE_GAUGE, TYPE_TEXTBOX,
    #            self.flange_plate.gauge_provided)
    #     flangespacing.append(t23)
    #
    #     t24 = (KEY_EDGEDIST_FLANGE, KEY_DISP_EDGEDIST_FLANGE, TYPE_TEXTBOX,
    #            self.flange_plate.edge_dist_provided )
    #     flangespacing.append(t24)
    #     return flangespacing
    #
    # def webspacing(self, flag):
    #
    #     webspacing = []
    #
    #     t8 = (KEY_WEB_PITCH, KEY_DISP_WEB_PLATE_PITCH, TYPE_TEXTBOX, self.web_plate.pitch_provided if flag else '')
    #     webspacing.append(t8)
    #
    #     t9 = (KEY_ENDDIST_W, KEY_DISP_END_DIST_W, TYPE_TEXTBOX,
    #         self.web_plate.end_dist_provided if flag else '')
    #     webspacing.append(t9)
    #
    #     t10 = ( KEY_WEB_GAUGE, KEY_DISP_WEB_PLATE_GAUGE, TYPE_TEXTBOX, self.web_plate.gauge_provided if flag else '')
    #     webspacing.append(t10)
    #
    #     t11 = (KEY_EDGEDIST_W, KEY_DISP_EDGEDIST_W, TYPE_TEXTBOX,
    #            self.web_plate.edge_dist_provided if flag else '')
    #     webspacing.append(t11)
    #     return webspacing
    #
    def flangecapacity(self, flag):

        flangecapacity = []

        t30 =(KEY_FLANGE_TEN_CAPACITY,KEY_DISP_FLANGE_TEN_CAPACITY,TYPE_TEXTBOX,
               round_up(self.section.tension_capacity_flange/1000, 5) if flag else '')
        flangecapacity.append(t30)
        t30 = (KEY_FLANGE_PLATE_TEN_CAP, KEY_DISP_FLANGE_PLATE_TEN_CAP, TYPE_TEXTBOX,
               round_up(self.flange_plate.tension_capacity_flange_plate / 1000, 5) if flag else '')
        flangecapacity.append(t30)

        t28 = (KEY_FLANGE_PLATE_MOM_DEMAND, KEY_FLANGE_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX,
               round_up(self.flange_plate.moment_demand / 1000000, 5) if flag else '')
        flangecapacity.append(t28)

        t29 = (KEY_FLANGE_PLATE_MOM_CAPACITY, KEY_FLANGE_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX,
               round_up(self.flange_plate.moment_capacity/1000, 5) if flag else '')
        flangecapacity.append( t29)

        return flangecapacity

    def webcapacity(self, flag):

        webcapacity = []
        t30 = (KEY_WEB_TEN_CAPACITY, KEY_DISP_WEB_TEN_CAPACITY, TYPE_TEXTBOX,
               round_up(self.section.tension_capacity_web / 1000, 5) if flag else '')
        webcapacity.append(t30)
        t30 = (KEY_TEN_CAP_WEB_PLATE, KEY_DISP_TEN_CAP_WEB_PLATE, TYPE_TEXTBOX,
               round_up(self.web_plate.tension_capacity_web_plate/ 1000, 5) if flag else '')
        webcapacity.append(t30)
        t30 = (KEY_WEBPLATE_SHEAR_CAPACITY, KEY_DISP_WEBPLATE_SHEAR_CAPACITY, TYPE_TEXTBOX,
               round_up(self.web_plate.shear_capacity_web_plate / 1000, 5) if flag else '')
        webcapacity.append(t30)

        # t30 = (KEY_TENSIONYIELDINGCAP_WEB, KEY_DISP_TENSIONYIELDINGCAP_WEB, TYPE_TEXTBOX,
        #        round(self.web_plate.tension_yielding_capacity / 1000, 2) if flag else '')
        # webcapacity.append(t30)
        #
        # t31 = (KEY_TENSIONRUPTURECAP_WEB, KEY_DISP_TENSIONRUPTURECAP_WEB, TYPE_TEXTBOX,
        #        round(self.web_plate.tension_rupture_capacity / 1000, 2) if flag else '')
        # webcapacity.append(t31)
        #
        # t12 = (KEY_SHEARYIELDINGCAP_WEB, KEY_DISP_SHEARYIELDINGCAP_WEB, TYPE_TEXTBOX,
        #        round(self.web_plate.shear_yielding_capacity/1000, 2) if flag else '')
        # webcapacity.append(t12)
        #
        # t13 = (KEY_BLOCKSHEARCAP_WEB, KEY_DISP_BLOCKSHEARCAP_WEB, TYPE_TEXTBOX,
        #        round(self.web_plate.block_shear_capacity/1000, 2) if flag else '')
        # webcapacity.append(t13)
        #
        # t14 = (KEY_SHEARRUPTURECAP_WEB, KEY_DISP_SHEARRUPTURECAP_WEB, TYPE_TEXTBOX,
        #        round(self.web_plate.shear_rupture_capacity/1000, 2) if flag else '')
        # webcapacity.append(t14)

        t15 = (KEY_WEB_PLATE_MOM_DEMAND, KEY_WEB_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX,
               round_up(self.web_plate.moment_demand / 1000000, 5) if flag else '')
        webcapacity.append(t15)

        t16 = (KEY_WEB_PLATE_MOM_CAPACITY, KEY_WEB_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX,
               round_up(self.web_plate.moment_capacity/1000, 5) if flag else '')
        webcapacity.append(t16)
        return webcapacity

    def web_weld_details(self,flag):
        web_weld_details = []
        t15 = (KEY_WEB_WELD_LENGTH, KEY_DISP_WEB_WELD_LENGTH, TYPE_TEXTBOX,
              (self.web_weld.length) if flag else '')
        web_weld_details.append(t15)

        t15 = (KEY_WEB_WELD_HEIGHT, KEY_DISP_WEB_WELD_HEIGHT, TYPE_TEXTBOX,
              (self.web_weld.height) if flag else '')
        web_weld_details.append(t15)
        t14 = (KEY_WEB_WELD_SIZE, KEY_WEB_DISP_WELD_SIZE, TYPE_TEXTBOX, self.web_weld.size if flag else '')
        web_weld_details.append(t14)

        t15 = (
            KEY_WEB_WELD_STRENGTH, KEY_WEB_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
           round_up(self.web_weld.strength,5) if flag else '')
        web_weld_details.append(t15)

        t16 = (
        KEY_WEB_WELD_STRESS, KEY_WEB_DISP_WELD_STRESS, TYPE_TEXTBOX, round_up(self.web_weld.stress, 5) if flag else '')
        web_weld_details.append(t16)

        return web_weld_details

    def flange_weld_details(self, flag):
        flange_weld_details = []
        t15 = (KEY_FLANGE_WELD_LENGTH, KEY_DISP_FLANGE_WELD_LENGTH, TYPE_TEXTBOX,
              (self.flange_weld.length) if flag else '')
        flange_weld_details.append(t15)

        t15 = (KEY_FLANGE_WELD_HEIGHT, KEY_DISP_FLANGE_WELD_HEIGHT, TYPE_TEXTBOX,
               (self.flange_weld.height) if flag else '')
        flange_weld_details.append(t15)

        t14 = (KEY_FLANGE_WELD_SIZE, KEY_FLANGE_DISP_WELD_SIZE, TYPE_TEXTBOX, self.flange_weld.size if flag else '')
        flange_weld_details.append(t14)

        t15 = (
            KEY_FLANGE_WELD_STRENGTH, KEY_FLANGE_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
            round_up(self.flange_weld.strength, 5) if flag else '')
        flange_weld_details.append(t15)

        t16 = (
        KEY_FLANGE_WELD_STRESS, KEY_FLANGE_DISP_WELD_STRESS, TYPE_TEXTBOX, round_up(self.flange_weld.stress, 5) if flag else '')
        flange_weld_details .append(t16)

        return flange_weld_details

    def output_values(self, flag):

        out_list = []
        t1 = (None, DISP_TITLE_WEBSPLICEPLATE, TYPE_TITLE, None)
        out_list.append(t1)

        t5 = (KEY_WEB_PLATE_HEIGHT, KEY_DISP_WEB_PLATE_HEIGHT, TYPE_TEXTBOX,
              self.web_plate.height if flag else '' )
        out_list.append(t5)

        t6 = (KEY_WEB_PLATE_LENGTH, KEY_DISP_WEB_PLATE_LENGTH, TYPE_TEXTBOX,
              self.web_plate.length if flag else '')
        out_list.append(t6)

        t7 = (KEY_WEBPLATE_THICKNESS, KEY_DISP_WEBPLATE_THICKNESS, TYPE_TEXTBOX,
              self.web_plate.thickness_provided if flag else '')
        out_list.append(t7)

        # t21 = (KEY_WEB_SPACING, KEY_DISP_WEB_SPACING, TYPE_OUT_BUTTON, ['Web Spacing Details', self.webspacing])
        # out_list.append(t21)

        t21 = (KEY_WEB_CAPACITY, KEY_DISP_WEB_CAPACITY, TYPE_OUT_BUTTON, ['Web Capacity', self.webcapacity])
        out_list.append(t21)

        t21 = (
        KEY_WEB_WELD_DETAILS, KEY_DISP_WEB_WELD_DETAILS, TYPE_OUT_BUTTON, ['Web Plate', self.web_weld_details])
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
        # t21 = (
        # KEY_FLANGE_SPACING, KEY_DISP_FLANGE_SPACING, TYPE_OUT_BUTTON, ['Flange Spacing Details', self.flangespacing])
        # out_list.append(t21)

        t21 = (
            KEY_FLANGE_CAPACITY, KEY_DISP_FLANGE_CAPACITY, TYPE_OUT_BUTTON, ['Flange Capacity', self.flangecapacity])
        out_list.append(t21)


        # t13 = (None, DISP_WEB_TITLE_WELD , TYPE_TITLE, None)
        # out_list.append(t13)

        t21 = (
        KEY_FLANGE_WELD_DETAILS, KEY_DISP_FLANGE_WELD_DETAILS, TYPE_OUT_BUTTON, ['Flange Plate', self.flange_weld_details])
        out_list.append(t21)



        # t13 = (None, DISP_FLANGE_TITLE_WELD, TYPE_TITLE, None)
        # out_list.append(t13)

        # t14 = (KEY_FLANGE_WELD_SIZE, KEY_FLANGE_DISP_WELD_SIZE, TYPE_TEXTBOX, self.flange_weld.size if flag else '')
        # out_list.append(t14)
        #
        # t15 = (
        #     KEY_FLANGE_WELD_STRENGTH, KEY_FLANGE_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
        #     round(self.flange_weld.strength, 2) if flag else '')
        # out_list.append(t15)
        #
        # t16 = (
        # KEY_FLANGE_WELD_STRESS, KEY_FLANGE_DISP_WELD_STRESS, TYPE_TEXTBOX, round(self.flange_weld.stress, 2) if flag else '')
        # out_list.append(t16)

        # t21 = (
        #     KEY_BOLT_DETAILS, KEY_DISP_BOLT_DETAILS, TYPE_OUT_BUTTON, ['Bolt details', self.boltdetails])
        # out_list.append(t21)


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

    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from beams and Beams table.
        """

        # @author Arsil Zunzunia
        global logger
        red_list = red_list_function()
        if self.section.designation in red_list or self.section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

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


    def module_name(self):

        return KEY_DISP_BEAMCOVERPLATEWELD
    def module_name(self):
        return KEY_DISP_BEAMCOVERPLATEWELD

    def set_input_values(self, design_dictionary):
        super(BeamCoverPlateWeld, self).set_input_values(self, design_dictionary)
        # self.module = design_dictionary[KEY_MODULE]
        # global design_status
        # self.design_status = False # todo doubt of true or false
        #
        self.module = design_dictionary[KEY_MODULE]
        # self.connectivity = design_dictionary[KEY_CONN]
        self.preference = design_dictionary[KEY_FLANGEPLATE_PREFERENCES]

        self.section = Beam(designation=design_dictionary[KEY_SECSIZE],
                              material_grade=design_dictionary[KEY_MATERIAL])
        print("anjali",design_dictionary[KEY_DP_DETAILING_EDGE_TYPE])
        # self.web_bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
        #                      bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
        #                      bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
        #                      edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
        #
        #                      mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
        #                      corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        #
        # self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
        #                      bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
        #                      bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
        #                      edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
        #                      mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
        #                      corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        # self.flange_bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
        #                         bolt_type=design_dictionary[KEY_TYP], material_grade=design_dictionary[KEY_MATERIAL],
        #                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
        #                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
        #                         mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
        #                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        self.flange_weld = Weld(material_grade=design_dictionary[KEY_MATERIAL],material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],fabrication = design_dictionary[KEY_DP_WELD_FAB])
        self.web_weld =Weld(material_grade=design_dictionary[KEY_MATERIAL],material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],fabrication = design_dictionary[KEY_DP_WELD_FAB])


        # self.web_weld =

        self.flange_plate = Plate(thickness=design_dictionary.get(KEY_FLANGEPLATE_THICKNESS, None),
                                  material_grade=design_dictionary[KEY_MATERIAL],
                                  gap=design_dictionary[KEY_DP_DETAILING_GAP])
        # self.plate = Plate(thickness=design_dictionary.get(KEY_FLANGEPLATE_THICKNESS, None),
        #                           material_grade=design_dictionary[KEY_MATERIAL],
        #                           gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.web_plate = Plate(thickness=design_dictionary.get(KEY_WEBPLATE_THICKNESS, None),
                               material_grade=design_dictionary[KEY_MATERIAL],
                               gap=design_dictionary[KEY_DP_DETAILING_GAP])
        # print("input values are set. Doing preliminary member checks")
        #
        # self.load.axial_force = self.load.axial_force * 1000
        # self.load.shear_force = self.load.shear_force * 1000
        # self.load.moment = self.load.moment * 1000000

        self.member_capacity(self)
        #self.hard_values(self)




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

        gamma_m0 = 1.1
        self.axial_capacity = ( self.section.area  * self.section.fy) / gamma_m0 #N
        self.axial_load =  0.3 *  self.axial_capacity
        self.factored_axial_load = max(self.load.axial_force * 1000, self.axial_load)  # N
        print("self.factored_axial_load" ,self.factored_axial_load)
        # self.axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (
        #     self.section.area)
        #
        # self.moment_web = (self.Z_w / (
        #     self.section.plast_sec_mod_z)) * self.load.moment  # KNm todo add in ddcl # z_w of web & z_p  of section
        # print('plast_sec_mod_z', self.section.plast_sec_mod_z)
        # self.moment_flange = ((self.load.moment * 1000000) - self.moment_web) / 1000000
        # self.flange_force = (((self.moment_flange * 1000000) / (self.section.depth - self.section.flange_thickness)) + (
        #     self.axial_force_f))  # todo added web moment -add in ddcl
        # print("flange_force", self.flange_force)
        # Shear Capacity  # N



        # design_shear_capacity = (self.section.depth* self.section.web_thickness * self.section.fy) / (


        design_shear_capacity = (self.section.depth* self.section.web_thickness * self.section.fy) / (
                math.sqrt(3) * gamma_m0)  # N # A_v: Total cross sectional area in shear in mm^2 (float)
        if self.load.shear_force * 1000 >= design_shear_capacity:
            self.load.shear_force = design_shear_capacity
        else:
            pass
        print('shear_force',self.load.shear_force)
        print( "design_shear_capacity", design_shear_capacity)
        # if self.section.type == "Rolled":
        if self.load.shear_force < (0.6 * design_shear_capacity):

            self.Z_p = float(
                (self.section.web_thickness * (
                            self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 4)  # mm3
            self.Z_e = float(
                (self.section.web_thickness * (
                            self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 6)  # mm3
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
            print("limitwidththkratio_flange",self.limitwidththkratio_flange)
        else:
           pass

        if self.section.type2 == "generally":

            self.limitwidththkratio_web = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                            column_t_w=self.section.web_thickness,
                                                                            column_d=self.section.depth,
                                                                            column_b=self.section.flange_width,
                                                                            column_fy=self.section.fy,
                                                                            factored_axial_force=self.factored_axial_load,
                                                                            column_area=self.section.area,
                                                                            compression_element="Web of an I-H",
                                                                        section="generally")
        else:
            pass

        self.class_of_section = int(max(self.limitwidththkratio_flange,self.limitwidththkratio_web))
        if self.class_of_section == 1 or self.class_of_section == 2:
            self.Z_w = self.Z_p
        elif self.class_of_section == 3:
            self.Z_w = self.Z_e
        # else:
        #     pass

        if self.class_of_section == 1 or self.class_of_section ==2:
            beta_b = 1
        elif self.class_of_section == 3:
            beta_b = self.Z_e / self.Z_p
        # else:
        #     # beta_b = 1
        #     pass

        self.section.plastic_moment_capacty(beta_b = beta_b, Z_p = self.Z_p, fy= self.section.fy) # N # for section #todo add in ddcl
        self.section.moment_d_deformation_criteria(fy= self.section.fy,Z_e = self.section.elast_sec_mod_z)
        # todo add in ddcl
        self.section.moment_capacity = min(  self.section.plastic_moment_capactiy, self.section.moment_d_def_criteria)

        print("design_bending_strength",  self.section.moment_capacity)
        # print(self.plast_sec_mod_z, "plast_sec_mod_z")
        # if self.section.plast_sec_mod_z is None:# Todo: add in database
        #     self.section.plast_sec_mod_z == self.section.elast_sec_mod_z
        # else:
        #     pass
        self.moment_web = (self.Z_w / ( self.section.plast_sec_mod_z )) * self.load.moment #  KNm todo add in ddcl # z_w of web & z_p  of section
        print('plast_sec_mod_z',self.section.plast_sec_mod_z)
        self.moment_flange = ((self.load.moment * 1000000) - self.moment_web)/1000000 #KNm todo add in ddcl

        if self.load.moment  >  self.section.moment_capacity/1000000:
            self.load.moment =  self.section.moment_capacity
        else:
            pass
        if self.load.moment == 0:
            self.load.moment =  self.section.moment_capacity
        else:
            pass
        print("self.load.moment", self.section.moment_capacity)

        ###WEB MENBER CAPACITY CHECK

        ###### # capacity Check for web in axial = min(block, yielding, rupture)

        # A_vn_web = ( self.section.depth - 2 * self.section.flange_thickness - self.web_plate.bolts_one_line * self.web_bolt.dia_hole) * self.section.web_thickness
        self.axial_force_w = ((self.section.depth - (
                2 * self.section.flange_thickness)) * self.section.web_thickness * self.factored_axial_load) / (
                                 self.section.area)
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.web_plate.fy)
        self.tension_rupture_capacity_web = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_v_web, fu=self.web_plate.fu)
        self.section.tension_capacity_web = min(self.tension_yielding_capacity_web,
                                                   self.tension_rupture_capacity_web)

        if self.section.tension_capacity_web < self.axial_force_w:
            logger.error(
                " : tension capacity web is less than applied loads, Please select larger sections or decrease loads")
        else:
            ### FLANGE MEMBER CAPACITY CHECK
            # A_vn_flange = (self.section.flange_width - self.flange_plate.bolts_one_line * self.flange_bolt.dia_hole) * \
            #               self.section.flange_thickness
            self.axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (
                self.section.area)
            self.flange_force = (
                        ((self.moment_flange * 1000000) / (self.section.depth - self.section.flange_thickness)) + (
                    self.axial_force_f))
            A_v_flange = self.section.flange_thickness * self.section.flange_width

            self.tension_yielding_capacity_flange = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange,
                fy=self.flange_plate.fy)
            self.section.tension_rupture_capacity_flange = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_v_flange, fu=self.flange_plate.fu)
            self.section.tension_capacity_flange = min(self.tension_yielding_capacity_web,
                                                    self.tension_rupture_capacity_web)


            if self.section.tension_capacity_flange >  self.flange_force:

                #             self.supported_section.tension_yielding_capacity > self.load.axial_force:
                # print("BBB flange member check is satisfactory. Doing bolt checks")
                self.web_plate_thickness_possible = [i for i in self.web_plate.thickness if i >= self.section.web_thickness]
                self.flange_plate_thickness_possible = [i for i in self.flange_plate.thickness if i >= self.section.flange_thickness]
                if len(self.flange_plate_thickness_possible) == 0 or self.web_plate_thickness_possible == 0:
                    logger.error(":Web Plate thickness should be greater than section  thicknesss.")
                else:

                    self.flange_plate.thickness_provided = self.min_thick_based_on_area(tk=self.section.flange_thickness,
                                                                                        width=self.section.flange_width,
                                                                                        list_of_pt_tk=self.flange_plate_thickness_possible,
                                                                                        t_w=self.section.web_thickness,
                                                                                        r_1=self.section.root_radius, )
                    self.web_plate.thickness_provided = self.min_thick_based_on_area(tk=self.section.web_thickness,
                                                                                     width=self.section.depth,
                                                                                     list_of_pt_tk=self.web_plate_thickness_possible,
                                                                                     t_w=self.section.web_thickness,
                                                                                     r_1=self.section.root_radius, )

                    self.section.tension_yielding_capacity = self.tension_yielding_capacity_flange
                    print("tension_yielding_capacity of flange", self.section.tension_yielding_capacity )
                    self.design_status = True
            else:
                self.design_status = False
                logger.error(" : tension capacity flange is less than applied loads, Please select larger sections or decrease loads")

        if self.design_status == True:

            self.web_plate_weld(self)
        else:
            logger.error(" :tension capacity of section is less than applied loads, Please select larger sections or decrease loads")



    def web_plate_weld(self):
        self.min_web_platethk = min(self.web_plate.thickness_provided,self.section.web_thickness)
        self.web_weld.size = (self.min_web_platethk- 2)
        if self.web_weld.size < 3:
            self.web_weld.size = 3
        else:
            pass
        if self.web_weld.size > 16:
            self.web_weld.size = 16
        else:
            pass

        self.design_strength_web_weld = self.web_weld.get_weld_strength(connecting_fu=self.web_weld.fu,
                                                                        weld_fabrication=KEY_DP_WELD_FAB_SHOP,
                                                                        t_weld=self.web_weld.size, weld_angle=90)
        self.web_weld.strength =(self.design_strength_web_weld)

        self.web_plate.height = int(
            self.section.depth - (2 * self.section.flange_thickness) - (2 * self.section.root_radius) - (
                        2 * self.web_plate.gap) - (2 * self.web_weld.size))
        self.available_long_web_length = self.web_plate.height # weld length

        # self.Required_weld_web_length_round = (2 * self.available_long_web_length + (
        #             4 * self.web_weld.size)) + self.web_plate.height

        self.design_status= False

        while self.design_status == False:

            d = self.available_long_web_length
            b = self.web_plate.height -(2*self.web_weld.size)
            cgy = d ** 2 / (2 * d + b)
            cgx = b / 2
            y_max =  (d ** 2 / (2 * d + b))
            x_max = b /2
            print(y_max, x_max)
            self.ecc = d - (d ** 2 / (2 * b + b))
            Ip_weld = (8 * d ** 3 + 6 * d * b ** 2 + b ** 3) / 12 - d ** 4 / (2 * d + b)
            self.weld_twist = (self.factored_axial_load * self.ecc) +self.moment_web
            # print("self.web_weld_length",self.web_weld_length )
            self.V_rest = self.web_weld.get_weld_stress( weld_shear=self.factored_axial_load, weld_axial =self.axial_force_w ,
                                                         weld_twist= self.weld_twist, Ip_weld= Ip_weld, y_max=y_max, x_max = x_max, l_weld=  self.available_long_web_length )

            if self.design_strength_web_weld  > self.V_rest :
                break
            else:
                self.available_long_web_length =  self.available_long_web_length + 20

        if  self.design_strength_web_weld  > self.V_rest :
            self.design_status = True
            self.web_weld.length =round_up(((2 * self.available_long_web_length) + self.web_plate.gap),5)
            self.web_plate.length =round_up((self.web_weld.length + (2 * self.web_weld.size)),5)
            self.web_plate.height = int(self.section.depth - (2 * self.section.flange_thickness) - (2 * self.section.root_radius) - (
                        2 * self.web_plate.gap) - (2 * self.web_weld.size))
            self.web_weld.height =round_down((self.web_plate.height - (2 * self.web_weld.size)),5)
            self.flange_plate_weld(self)

    # def capacity_web_axial(self):
    #     self.axial_force_w = ((self.section.depth - (
    #             2 * self.section.flange_thickness)) * self.section.web_thickness * self.factored_axial_load) / (
    #                              self.section.area)
    #     A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
    #     self.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
    #         A_v=A_v_web, fy=self.web_plate.fy)
    #     self.tension_rupture_capacity_web = self.tension_member_design_due_to_rupture_of_critical_section(
    #         A_vn=A_v_web, fu=self.web_plate.fu)
    #     self.section.tension_capacity_web = min(self.tension_yielding_capacity_web,
    #                                                self.tension_rupture_capacity_web)
    #
    #     if self.section.tension_capacity_web < self.axial_force_w:
    #         logger.error(" : tension capacity web is less than applied loads, Please select larger sections or decrease loads")
    #     else:
    #         self.flange_plate_weld(self)

    def flange_plate_weld(self):
        self.min_flange_platethk = min(self.flange_plate.thickness_provided, self.section.flange_thickness)
        self.flange_weld.size = (self.min_flange_platethk - 2)
        if self.flange_weld.size < 3:
            self.flange_weld.size = 3
        else:
            pass
        if self.flange_weld.size > 16:
            self.flange_weld.size = 16
        else:
            pass
        self.axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (
            self.section.area)
        self.flange_force = (((self.moment_flange * 1000000) / (self.section.depth - self.section.flange_thickness)) + (
            self.axial_force_f))  # todo added web moment -add in ddcl


        self.design_strength_flange_weld = self.flange_weld.get_weld_strength(connecting_fu=self.flange_weld.fu,
                                                                              weld_fabrication=KEY_DP_WELD_FAB_SHOP,
                                                                              t_weld=self.flange_weld.size,
                                                                              weld_angle=90)
        print("for req lenth", self.flange_force, self.design_strength_flange_weld)
        self.flange_weld.strength = (self.design_strength_flange_weld)
        self.Required_weld_flange_length = self.flange_force / self.design_strength_flange_weld
        self.Required_weld_flange_length_round = round_up(self.flange_force / self.design_strength_flange_weld, 5) #  c shape half of the splice  plate
        print("Requiredweldlength", self.Required_weld_flange_length_round)

        self.flange_plate.height = round_down(
            self.section.flange_width - (4 * self.flange_weld.size))  # width of the flange plate

        self.available_long_flange_length = int((self.Required_weld_flange_length_round - self.flange_plate.height - (
                    2 * self.flange_weld.size)) /2) # half of the one side of the flange plate
        print("self.available_long_length", self.available_long_flange_length)

        self.design_status= False

        while self.design_status == False:

            if self.available_long_flange_length  >=  self.flange_plate.height:
                self.design_status = True
                break

            else:
                 self.available_long_flange_length = int(self.available_long_flange_length + 20)


                # self.web_plate_weld(self)

        print("length",self.available_long_flange_length)
        if self.design_status == True:
            self.flange_weld.length = round_up(((2 * self.available_long_flange_length) + self.flange_plate.gap),5)
            self.flange_plate.length = round_up((self.flange_weld.length + (2 * self.flange_weld.size)),5)
            self.flange_plate.height = round_down((self.section.flange_width - (4 * self.flange_weld.size)),5)
            self.flange_weld.height = round_down((self.flange_plate.height - (2 * self.flange_weld.size)),5)

            self.flange_plate_capacity_axial(self)
        else:
            self.design_status = False
            logger.error(
                " : Length of flange plate is less than height of the flange plate")


    def flange_plate_capacity_axial(self): # flange plate capacity check in axial
        if  self.preference == "Outside":
            A_v_flange = self.flange_plate.thickness_provided * self.flange_plate.height

            self.flange_plate.tension_yielding_capacity= self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange,fy=self.flange_plate.fy)
            self.flange_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_v_flange, fu=self.flange_plate.fu)
            self.flange_plate.tension_capacity_flange_plate = min(self.flange_plate.tension_yielding_capacity,self.flange_plate.tension_rupture_capacity)
            if self.flange_plate.tension_capacity_flange_plate < self.flange_force:
                self.design_status = False
                logger.error(" : tension capacity flange plate is less than applied loads, Please select larger sections or decrease loads")
            else:
                self.web_plate_capacity_axial(self)
        else:
            #  yielding,rupture  for  inside flange plate
            flange_plate_height_inside = (self.section.flange_width - self.section.web_thickness - (
                        self.section.root_radius / 2)) / 2
            flange_plate_height_outside = self.flange_plate.height

            A_v_flange = ((2 * flange_plate_height_inside) + self.section.flange_width)* self.flange_plate.thickness_provided

            self.flange_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange,
                fy=self.flange_plate.fy)

            self.flange_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_v_flange ,
                fu=self.flange_plate.fu)
            self.flange_plate.tension_capacity_flange_plate = min( self.flange_plate.tension_yielding_capacity,
                                                                  self.flange_plate.tension_rupture_capacity )
            if self.flange_plate.tension_capacity_flange_plate < self.flange_force:
                self.design_status = False
                logger.error(
                    " : Tension capacity flange plate is less than applied loads, Please select larger sections or decrease loads")
            else:
                self.web_plate_capacity_axial(self)



    def web_plate_capacity_axial(self):

        A_v_web = 2 * self.web_plate.height * self.web_plate.thickness_provided
        self.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.web_plate.fy)
        self.tension_rupture_capacity_web = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_v_web, fu=self.web_plate.fu)
        self.web_plate.tension_capacity_web_plate = min(self.tension_yielding_capacity_web,
                                                              self.tension_rupture_capacity_web)
        if self.web_plate.tension_capacity_web_plate < self.axial_force_w:
            self.design_status = False
            logger.error(
                " : tension capacity web plate in axial is less than applied loads, Please select larger sections or decrease loads")

        else:
            self.cap_check_web_shear(self)

    def cap_check_web_shear(self):
        axial_force_w = ((self.section.depth - (
                2 * self.section.flange_thickness)) * self.section.web_thickness * self.factored_axial_load) / (
                            self.section.area)

        A_vn_web = 2 * (self.available_long_web_length + self.web_weld.size) * self.web_plate.thickness_provided

        self.web_plate.shear_yielding_capacity = self.shear_yielding(
            A_v= A_vn_web , fy=self.web_plate.fy)
        self.web_plate.shear_rupture_capacity = self.shear_rupture_(
            A_vn=A_vn_web, fu=self.web_plate.fu)
        self.web_plate.shear_capacity_web_plate = min(self.web_plate.shear_yielding_capacity ,self.web_plate.shear_rupture_capacity)
        if self.web_plate.shear_capacity_web_plate < self.axial_force_w:
            self.design_status = False
            logger.error(" : Shear capacity web plate is less than applied loads, Please select larger sections or decrease loads")
        else:
            self.cap_check_web_axial(self)

    def cap_check_web_axial(self):
        self.axial_force_w = ((self.section.depth - (
                2 * self.section.flange_thickness)) * self.section.web_thickness * self.factored_axial_load) / (
                                 self.section.area)
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.web_plate.fy)
        self.tension_rupture_capacity_web = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_v_web, fu=self.web_plate.fu)
        for self.web_plate.thickness_provided in self.web_plate_thickness_possible:
            design_status_block_shear = False
            while design_status_block_shear == False:
                # print(design_status_block_shear)
                # print(0, self.web_plate.max_end_dist, self.web_plate.end_dist_provided, self.web_plate.max_spacing_round, self.web_plate.pitch_provided)
                Avg = 2 * self.available_long_web_length * self.section.web_thickness
                Avn = 2 * self.available_long_web_length * self.section.web_thickness
                Atg = self.web_plate.height * self.section.web_thickness

                Atn = self.web_plate.height * self.section.web_thickness

                # print(17,self.web_plate.bolt_line, self.web_plate.pitch_provided, self.web_plate.bolt_line,
                #      self.web_bolt.dia_hole, self.web_plate.end_dist_provided, self.web_plate.thickness_provided)
                # print(18, self.web_plate.bolt_line, pitch, end_dist, self.section.web_thickness)

                self.section.block_shear_capacity = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn,
                                                                                      A_tg=Atg,
                                                                                      A_tn=Atn,
                                                                                      f_u=self.web_plate.fu,
                                                                                      f_y=self.web_plate.fy)

                self.section.block_shear_capacity = 2 * self.section.block_shear_capacity
                if self.section.block_shear_capacity < self.axial_force_w:
                    self.available_long_web_length = self.available_long_web_length + 5

                else:
                    design_status_block_shear = True
                    break
            if design_status_block_shear == True:
                break
        if design_status_block_shear == True:
            self.section.tension_capacity_web = min(self.tension_yielding_capacity_web,
                                                    self.tension_rupture_capacity_web,
                                                    self.section.block_shear_capacity)
            if self.section.tension_capacity_web < self.axial_force_w:
                logger.error(
                    " : tension capacity web is less than applied loads, Please select larger sections or decrease loads")
            else:
                pass



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

    @staticmethod
    def shear_yielding(A_v,fy):
        '''
        Args:
            length (float) length of member in direction of shear load
            thickness(float) thickness of member resisting shear
            beam_fy (float) Yield stress of section material
        Returns:
            Capacity of section in shear yeiding
        '''

        # A_v = length * thickness
        gamma_m0 = 1.1
        # print(length, thickness, fy, gamma_m0)
        # V_p = (0.6 * A_v * fy) / (math.sqrt(3) * gamma_m0 * 1000)  # kN
        V_p = (A_v * fy) / (math.sqrt(3) * gamma_m0 )  # N
        return V_p

    @staticmethod
    def shear_rupture_(A_vn, fu):
        '''
               Args:
                   A_vn (float) Net area under shear
                   Beam_fu (float) Ultimate stress of Beam material
               Returns:
                   Capacity of beam web in shear rupture
               '''

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        # A_vn = (height- bolts_one_line * dia_hole) * thickness
        T_dn = 0.9 * A_vn * fu / (math.sqrt(3) *gamma_m1)
        return T_dn


    # def web_force(column_d, column_f_t, column_t_w, axial_force, column_area):
    #     """
    #     Args:
    #        c_d: Overall depth of the column section in mm (float)
    #        column_f_t: Thickness of flange in mm (float)
    #        column_t_w: Thickness of flange in mm (float)
    #        axial_force: Factored axial force in kN (float)
    #
    #     Returns:
    #         Force in flange in kN (float)
    #     """
    #     axial_force_w = int(
    #         ((column_d - 2 * (column_f_t)) * column_t_w * axial_force ) / column_area)   # N
    #     return round(axial_force_w)

    @staticmethod
    def limiting_width_thk_ratio(column_f_t, column_t_w, column_d, column_b, column_fy, factored_axial_force,
                                 column_area, compression_element, section):

        epsilon = float(math.sqrt(250 / column_fy))
        axial_force_w = int(
            ((column_d - 2 * (column_f_t)) * column_t_w * factored_axial_force) /( column_area )) #N

        des_comp_stress_web = column_fy
        des_comp_stress_section = column_fy
        avg_axial_comp_stress = axial_force_w / ((column_d - 2 * column_f_t) * column_t_w)
        r1 = avg_axial_comp_stress / des_comp_stress_web
        r2 = avg_axial_comp_stress / des_comp_stress_section
        a = column_b / column_f_t
        # compression_element=["External","Internal","Web of an I-H" ,"box section" ]
        # section=["rolled","welded","compression due to bending","generally", "Axial compression" ]
        # section = "rolled"
        if compression_element == "External" or compression_element =="Internal":
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

        elif compression_element =="Web of an I-H"or compression_element == "box section":
            if section == "generally":
                if r1 < 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)) , (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= (max(105 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "compact"
                    elif column_d / column_t_w <= max((126 * epsilon / (1 + 2*r1)), column_d / column_t_w >= (
                            42 * epsilon)):
                        class_of_section1 = "semi-compact"
                    # else:
                    #     print('fail')
                    # print("class_of_section3", class_of_section)
                elif r1 > 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)) , (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= max((105 * epsilon / (1 + (r1 * 1.5))), (
                            42 * epsilon)):
                        class_of_section1 = "compact"
                    elif column_d / column_t_w <= max((126 * epsilon / (1 + 2*r1)), (
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
        print("class_of_section", class_of_section1 )
        if class_of_section1 == "plastic":
            class_of_section1 = 1
        elif class_of_section1 == "compact":
            class_of_section1 = 2
        elif class_of_section1 == "semi-compact":
            class_of_section1 = 3
        # else:
        #     print('fail')
        print( "class_of_section2",class_of_section1)

        return class_of_section1

        print("class_of_section1", class_of_section1)


    @staticmethod
    def min_thick_based_on_area(tk, width, list_of_pt_tk, t_w, r_1,
                                preference=None):  # area of flange plate should be greater than 1.05 times area of flange
        flange_crs_sec_area = tk * width
        for y in list_of_pt_tk:
            if preference == "Outside+Inside":

                flange_plate_crs_sec_area = (2 * width - t_w - (2 * r_1)) * y
            else:
                flange_plate_crs_sec_area = y * width

            if flange_plate_crs_sec_area >= flange_crs_sec_area * 1.05:
                thickness = y
                break
            else:
                pass

        return thickness


#

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

    def tab_list(self):

        tabs = []

        t1 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_beam_section)
        tabs.append(t1)

        t2 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t2)

        t3 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t3)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        t6 = ("Connector", TYPE_TAB_2, self.connector_values)
        tabs.append(t6)

        return tabs
    # def flange_force(self,):
    #     axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (
    #         self.section.area)
    #     moment_web = (Z_w / ( self.section.plast_sec_mod_z )) * self.load.moment #  KNm todo add in ddcl # z_w of web & z_p  of section
    #
    #     self.moment_flange = ((self.load.moment * 1000000) - moment_web) / 1000000
    #     flange_force = (((self.moment_flange * 1000000) / (self.section.depth - self.section.flange_thickness)) + (
    #         axial_force_f))


