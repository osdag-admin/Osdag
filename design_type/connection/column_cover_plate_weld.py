
"""
Started on 1st April, 2020.

@author: Kumari Anjali Jatav

Module: Column-Column Cover Plate Welded Connection

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel Structures by N. Subramanian

"""

from design_type.connection.moment_connection import MomentConnection
from utils.common.component import *
from Common import *
from utils.common.load import Load
from design_report.reportGenerator_latex import CreateLatex
from Report_functions import *

import logging


class ColumnCoverPlateWeld(MomentConnection):

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        """

        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        Tab Title : Text which is displayed as Title of Tab,
        Type of Tab: There are Three types of tab layouts.
            Type_TAB_1: This have "Add", "Clear", "Download xlsx file" "Import xlsx file"
            TYPE_TAB_2: This contains a Text box for side note.
            TYPE_TAB_3: This is plain layout
        function for tab content: All the values like labels, input widgets can be passed as list of tuples,
        which will be displayed in chosen tab layout

        """
        tabs = []

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_section)
        tabs.append(t1)

        t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        tabs.append(t6)

        t2 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t2)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):
        """

        :return: This function is used to update the values of the keys in design preferences,
         which are dependent on other inputs.
         It returns list of tuple which contains, tab name, keys whose values will be changed,
         function to change the values and arguments for the function.

         [Tab Name, [Argument list], [list of keys to be updated], input widget type of keys, change_function]

         Here Argument list should have only one element.
         Changing of this element,(either changing index or text depending on widget type),
         will update the list of keys (this can be more than one).

         """
        change_tab = []

        t2 = (KEY_DISP_COLSEC, [KEY_SEC_MATERIAL], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX, self.get_fu_fy_I_section)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t3)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t6 = (KEY_DISP_COLSEC, [KEY_SECSIZE], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
                Not required for this module but empty list should be passed"""
        return []

    # def list_for_fu_fy_validation(self):
    #     """ This function is no longer required"""
    #     fu_fy_list = []
    #
    #     t2 = (KEY_SEC_MATERIAL, KEY_SEC_FU, KEY_SEC_FY)
    #     fu_fy_list.append(t2)
    #
    #     t3 = (KEY_CONNECTOR_MATERIAL, KEY_CONNECTOR_FU, KEY_CONNECTOR_FY)
    #     fu_fy_list.append(t3)
    #
    #     return fu_fy_list

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        t2 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        design_input.append(t4)

        t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        design_input.append(t4)

        t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to
        design dictionary if design preference is never opened by user. It sets are design preference values to default.
        If any design preference value needs to be set to input dock value, tuple shall be written as:

        (Key of input dock, [List of Keys from design preference], 'Input Dock')

        If the values needs to be set to default,

        (None, [List of Design Preference Keys], '')

         """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_WELD_FAB, KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_GAP,
                     KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

        :return: This function returns list of tuples which has keys that needs to be updated,
         on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

         [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
        """
        add_buttons = []

        t2 = (KEY_DISP_COLSEC, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE, None, None, "Columns")
        add_buttons.append(t2)

        return add_buttons

    def get_values_for_design_pref(self, key, design_dictionary):

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            fu = Material(design_dictionary[KEY_MATERIAL], 41).fu
        else:
            fu = ''

        val = {KEY_DP_BOLT_TYPE: "Pretensioned",
               KEY_DP_BOLT_HOLE_TYPE: "Standard",
               KEY_DP_BOLT_SLIP_FACTOR: str(0.3),
               KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
               KEY_DP_DETAILING_GAP: '3',
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No',
               KEY_DP_DESIGN_METHOD: "Limit State Design",
               KEY_CONNECTOR_MATERIAL: str(design_dictionary[KEY_MATERIAL])
               }[key]

        return val

    ####################################
    # Design Preference Functions End
    ####################################

    def __init__(self):
        super(ColumnCoverPlateWeld, self).__init__()
        self.design_status = False

    def set_osdaglogger(key):

        """
        Function to set Logger for Tension Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def preference_type(self):

        pref_type = self[0]
        if pref_type == VALUES_FLANGEPLATE_PREFERENCES[0]:
            return True
        else:
            return False

    def input_value_changed(self):

        lst = []

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        t8 = ([KEY_FLANGEPLATE_PREFERENCES], KEY_INNERFLANGE_PLATE_HEIGHT, TYPE_OUT_DOCK, self.preference_type)
        lst.append(t8)
        t8 = ([KEY_FLANGEPLATE_PREFERENCES], KEY_INNERFLANGE_PLATE_HEIGHT, TYPE_OUT_LABEL, self.preference_type)
        lst.append(t8)

        t8 = ([KEY_FLANGEPLATE_PREFERENCES], KEY_INNERFLANGE_PLATE_LENGTH, TYPE_OUT_DOCK, self.preference_type)
        lst.append(t8)
        t8 = ([KEY_FLANGEPLATE_PREFERENCES], KEY_INNERFLANGE_PLATE_LENGTH, TYPE_OUT_LABEL, self.preference_type)
        lst.append(t8)

        t8 = ([KEY_FLANGEPLATE_PREFERENCES], KEY_INNERFLANGEPLATE_THICKNESS, TYPE_OUT_DOCK, self.preference_type)
        lst.append(t8)
        t8 = ([KEY_FLANGEPLATE_PREFERENCES], KEY_INNERFLANGEPLATE_THICKNESS, TYPE_OUT_LABEL, self.preference_type)
        lst.append(t8)
        # t8 = ([KEY_FLANGEPLATE_PREFERENCES], KEY_INNERFLANGE_WELD_DETAILS, TYPE_OUT_DOCK, self.preference_type)
        # lst.append(t8)
        # t8 = ([KEY_FLANGEPLATE_PREFERENCES], KEY_INNERFLANGE_WELD_DETAILS, TYPE_OUT_LABEL, self.preference_type)
        # lst.append(t8)

        return lst
    def input_values(self):

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_COLUMNCOVERPLATEWELD, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, connectdb("Columns"), True, 'No Validator')
        options_list.append(t4)

        # t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, True, 'No Validator')
        # options_list.append(t15)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)
        t19 = (
            KEY_WELD_TYPE, KEY_DISP_WELD_TYPE, TYPE_COMBOBOX,
            ["Fillet Weld"], True, 'No Validator')
        options_list.append(t19)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'Int Validator')
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

        t18 = (None, DISP_TITLE_FLANGESPLICEPLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t18)

        t19 = (KEY_FLANGEPLATE_PREFERENCES, KEY_DISP_FLANGESPLATE_PREFERENCES, TYPE_COMBOBOX, VALUES_FLANGEPLATE_PREFERENCES, True, 'No Validator')
        options_list.append(t19)

        t20 = (KEY_FLANGEPLATE_THICKNESS, KEY_DISP_FLANGESPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_FLANGEPLATE_THICKNESS, True, 'No Validator')
        options_list.append(t20)

        t21 = (None, DISP_TITLE_WEBSPLICEPLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t21)

        t22 = (KEY_WEBPLATE_THICKNESS, KEY_DISP_WEBPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_WEBPLATE_THICKNESS, True, 'No Validator')
        options_list.append(t22)

        return options_list

    def customized_input(self):

        list1 = []
        t4 = (KEY_WEBPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t4)
        t5 = (KEY_FLANGEPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t5)

        return list1

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

        t30 = (KEY_FLANGE_TEN_CAPACITY, KEY_DISP_FLANGE_TEN_CAPACITY, TYPE_TEXTBOX,
               round(self.section.tension_capacity_flange / 1000, 2) if flag else '')
        flangecapacity.append(t30)
        t30 = (KEY_FLANGE_PLATE_TEN_CAP, KEY_DISP_FLANGE_PLATE_TEN_CAP, TYPE_TEXTBOX,
               round(self.flange_plate.tension_capacity_flange_plate / 1000, 2) if flag else '')
        flangecapacity.append(t30)

        return flangecapacity

    def customized_input(self):

        list1 = []
        t4 = (KEY_WEBPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t4)
        t5 = (KEY_FLANGEPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t5)

        return list1

    def webcapacity(self, flag):

        webcapacity = []
        t30 = (KEY_WEB_TEN_CAPACITY, KEY_DISP_WEB_TEN_CAPACITY, TYPE_TEXTBOX,
               round(self.section.tension_capacity_web / 1000, 2) if flag else '')
        webcapacity.append(t30)
        t30 = (KEY_WEB_PLATE_CAPACITY, KEY_DISP_WEB_PLATE_CAPACITY, TYPE_TEXTBOX,
               round(self.web_plate.tension_capacity_web_plate / 1000, 2) if flag else '')
        webcapacity.append(t30)
        t30 = (KEY_WEBPLATE_SHEAR_CAPACITY_PLATE, KEY_DISP_WEBPLATE_SHEAR_CAPACITY_PLATE, TYPE_TEXTBOX,
               round(self.web_plate.shear_capacity_web_plate / 1000, 2) if flag else '')
        webcapacity.append(t30)
        return webcapacity

    def web_weld_details(self, flag):
        web_weld_details = []
        # t15 = (KEY_WEB_WELD_LENGTH, DISP_EFF, TYPE_TEXTBOX,(self.l_req_weblength) if flag else '')
        # web_weld_details.append(t15)
        # t99 = (None, None, TYPE_SECTION, './ResourceFiles/images/UV_w.png')
        # web_weld_details.append(t99)

        t14 = (KEY_WEB_WELD_SIZE, KEY_WEB_DISP_WELD_SIZE, TYPE_TEXTBOX, self.web_weld.size if flag else '')
        web_weld_details.append(t14)

        t15 = (KEY_WEB_WELD_STRENGTH, KEY_WEB_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
               self.web_weld.strength if flag else '')
        web_weld_details.append(t15)  # in N/mm
        t5 = (
        KEY_REDUCTION_LONG_JOINT, KEY_DISP_REDUCTION, TYPE_TEXTBOX, round(self.Reduction_factor_web, 2) if flag else '',
        True)
        web_weld_details.append(t5)

        t10 = (KEY_OUT_WELD_STRENGTH_RED, KEY_OUT_DISP_WELD_STRENGTH_RED, TYPE_TEXTBOX,
               round(self.web_weld.strength_red, 2) if flag else '',
               True)
        web_weld_details.append(t10)
        t16 = (KEY_WEB_WELD_STRESS, KEY_WEB_DISP_WELD_STRESS, TYPE_TEXTBOX, self.web_weld.stress if flag else '')
        web_weld_details.append(t16)

        return web_weld_details

    def web_pattern(self, status):

        pattern = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern (Half Plate)")
        pattern.append(t00)

        t99 = (None, 'Failure Pattern Due to Tension Force in the Member', TYPE_SECTION,
               ['./ResourceFiles/images/U_Vw.png', 202, 400, "Web Block Shear Pattern"])  # [image, width, height, caption]
        pattern.append(t99)

        t9 = (KEY_OUT_Lw, KEY_OUT_DISP_Lw, TYPE_TEXTBOX, round(int((self.web_plate.length-self.flange_plate.gap - (4 *self.web_weld.size))/2),2) if status else '')
        pattern.append(t9)

        t10 = (KEY_OUT_Hw, KEY_OUT_DISP_Hw, TYPE_TEXTBOX, round(int(self.web_plate.height-(2 * self.web_weld.size)),2) if status else '')
        pattern.append(t10)

        return pattern
    def flange_weld_details(self, flag):
        flange_weld_details = []
        # t15 = (KEY_FLANGE_WELD_LENGTH, DISP_EFF, TYPE_TEXTBOX,
        #       (self.l_req_flangelength) if flag else '')
        # flange_weld_details.append(t15)

        # t15 = (KEY_FLANGE_WELD_HEIGHT, KEY_DISP_FLANGE_WELD_HEIGHT, TYPE_TEXTBOX,
        #        (self.flange_weld.height) if flag else '')
        # flange_weld_details.append(t15)
        # t99 = (None, None, TYPE_SECTION, './ResourceFiles/images/columnweld_flange.png')
        # flange_weld_details.append(t99)

        t14 = (KEY_FLANGE_WELD_SIZE, KEY_FLANGE_DISP_WELD_SIZE, TYPE_TEXTBOX, self.flange_weld.size if flag else '')
        flange_weld_details.append(t14)

        t15 = (KEY_FLANGE_WELD_STRENGTH, KEY_FLANGE_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
               self.flange_weld.strength if flag else '')
        flange_weld_details.append(t15)  # in N/mm
        t5 = (KEY_REDUCTION_LONG_JOINT, KEY_DISP_REDUCTION, TYPE_TEXTBOX,
              round(self.Reduction_factor_flange, 2) if flag else '',
              True)
        flange_weld_details.append(t5)
        t10 = (KEY_OUT_WELD_STRENGTH_RED, KEY_OUT_DISP_WELD_STRENGTH_RED, TYPE_TEXTBOX,
               round(self.flange_weld.strength_red, 2) if flag else '',
               True)
        flange_weld_details.append(t10)
        t16 = (
        KEY_FLANGE_WELD_STRESS, KEY_FLANGE_DISP_WELD_STRESS, TYPE_TEXTBOX, self.flange_weld.stress if flag else '')
        flange_weld_details.append(t16)  # in N/mm

        return flange_weld_details

    def Innerflange_weld_details(self, flag):
        Innerflange_weld_details = []
        # t15 = (KEY_INNERFLANGE_WELD_LENGTH, KEY_DISP_INNERFLANGE_WELD_LENGTH, TYPE_TEXTBOX,
        #       ( self.flange_weld.Innerlength ) if flag else '')
        # Innerflange_weld_details.append(t15)
        # t15 = (KEY_FLANGE_WELD_LENGTH, KEY_DISP_WELD_LEN_EFF_OUTSIDE, TYPE_TEXTBOX,
        #        (self.l_req_flangelength) if flag else '')
        # Innerflange_weld_details.append(t15)

        # t15 = (KEY_INNERFLANGE_WELD_HEIGHT, KEY_DISP_INNERFLANGE_WELD_HEIGHT, TYPE_TEXTBOX,
        #        (self.flange_weld.Innerheight) if flag else '')
        # Innerflange_weld_details.append(t15)

        t14 = (KEY_FLANGE_WELD_SIZE, KEY_FLANGE_DISP_WELD_SIZE, TYPE_TEXTBOX, self.flange_weld.size if flag else '')
        Innerflange_weld_details.append(t14)

        t15 = (KEY_INNERFLANGE_WELD_STRENGTH, KEY_INNERFLANGE_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
               self.flange_weld.strength if flag else '')
        Innerflange_weld_details.append(t15)  # in N/mm

        t16 = (KEY_INNERFLANGE_WELD_STRESS, KEY_INNERFLANGE_DISP_WELD_STRESS, TYPE_TEXTBOX,
               self.flange_weld.stress if flag else '')
        Innerflange_weld_details.append(t16)  # in N/mm

        return Innerflange_weld_details

    def member_capacityoutput(self, flag):
        member_capacityoutput = []
        t29 = (KEY_MEMBER_MOM_CAPACITY, KEY_OUT_DISP_MOMENT_CAPACITY, TYPE_TEXTBOX,
               round(self.section.moment_capacity / 1000000, 2) if flag else '')
        member_capacityoutput.append(t29)
        t29 = (KEY_MEMBER_SHEAR_CAPACITY, KEY_OUT_DISP_SHEAR_CAPACITY, TYPE_TEXTBOX,
               round(self.shear_capacity1 / 1000, 2) if flag else '')
        member_capacityoutput.append(t29)
        t29 = (KEY_MEMBER_AXIALCAPACITY, KEY_OUT_DISP_AXIAL_CAPACITY, TYPE_TEXTBOX,
               round(self.axial_capacity / 1000, 2) if flag else '')
        member_capacityoutput.append(t29)
        return member_capacityoutput

    def output_values(self, flag):

        out_list = []

        t4 = (None, DISP_TITLE_MEMBER_CAPACITY, TYPE_TITLE, None, True)
        out_list.append(t4)
        t21 = (
        KEY_MEMBER_CAPACITY, KEY_DISP_MEMBER_CAPACITY, TYPE_OUT_BUTTON, ['Member Capacity', self.member_capacityoutput],
        True)
        out_list.append(t21)

        t1 = (None, DISP_TITLE_WEBSPLICEPLATE, TYPE_TITLE, None, True)

        out_list.append(t1)

        t5 = (KEY_WEB_PLATE_HEIGHT, KEY_DISP_WEB_PLATE_HEIGHT, TYPE_TEXTBOX,
              self.web_plate.height if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_WEB_PLATE_LENGTH, KEY_DISP_WEB_PLATE_LENGTH, TYPE_TEXTBOX,
              self.web_plate.length if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_WEBPLATE_THICKNESS, KEY_DISP_WEBPLATE_THICKNESS, TYPE_TEXTBOX,
              int(self.web_plate.thickness_provided) if flag else '', True)
        out_list.append(t7)

        t21 = (KEY_WEB_CAPACITY, KEY_DISP_WEB_CAPACITY, TYPE_OUT_BUTTON, ['Web Capacity', self.webcapacity], True)
        out_list.append(t21)
        t17 = (KEY_OUT_PATTERN_2, KEY_OUT_DISP_PATTERN, TYPE_OUT_BUTTON, ['Block Shear Pattern ', self.web_pattern], True)
        out_list.append(t17)
        t21 = (
        KEY_WEB_WELD_DETAILS, KEY_DISP_WEB_WELD_DETAILS, TYPE_OUT_BUTTON, ['Web Plate Weld', self.web_weld_details],
        True)
        out_list.append(t21)
        t17 = (None, DISP_TITLE_FLANGESPLICEPLATE, TYPE_TITLE, None, True)
        out_list.append(t17)
        t17 = (None, DISP_TITLE_FLANGESPLICEPLATE_OUTER, TYPE_TITLE, None, True)

        out_list.append(t17)

        t18 = (KEY_FLANGE_PLATE_HEIGHT, KEY_DISP_FLANGE_PLATE_HEIGHT, TYPE_TEXTBOX,
               self.flange_plate.height if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_FLANGE_PLATE_LENGTH, KEY_DISP_FLANGE_PLATE_LENGTH, TYPE_TEXTBOX,
               self.plate_out_len if flag else '', True)

        out_list.append(t19)

        t20 = (KEY_FLANGEPLATE_THICKNESS, KEY_DISP_FLANGESPLATE_THICKNESS, TYPE_TEXTBOX,
               int(self.flange_out_plate_tk) if flag else '', True)
        out_list.append(t20)

        t21 = (
            KEY_FLANGE_CAPACITY, KEY_DISP_FLANGE_CAPACITY, TYPE_OUT_BUTTON, ['Flange Capacity', self.flangecapacity],
            True)
        out_list.append(t21)

        t21 = (
            KEY_FLANGE_WELD_DETAILS, KEY_DISP_FLANGE_WELD_DETAILS, TYPE_OUT_BUTTON,
            ['Flange Plate Weld', self.flange_weld_details],  True)
        out_list.append(t21)


        t17 = (None, DISP_TITLE_FLANGESPLICEPLATE_INNER, TYPE_TITLE, None,  False)


        out_list.append(t17)

        t18 = (KEY_INNERFLANGE_PLATE_HEIGHT, KEY_DISP_INNERFLANGE_PLATE_HEIGHT, TYPE_TEXTBOX,
               self.flange_plate.Innerheight if flag else '',  False)
        out_list.append(t18)

        t19 = (
            KEY_INNERFLANGE_PLATE_LENGTH, KEY_DISP_INNERFLANGE_PLATE_LENGTH, TYPE_TEXTBOX,
            self.plate_in_len if flag else '',  False)

        out_list.append(t19)

        t20 = (KEY_INNERFLANGEPLATE_THICKNESS, KEY_DISP_INNERFLANGESPLATE_THICKNESS, TYPE_TEXTBOX,
               self.flange_in_plate_tk if flag else '', False)
        out_list.append(t20)

        # t21 = (KEY_INNERFLANGE_WELD_DETAILS, KEY_DISP_INNERFLANGE_WELD_DETAILS, TYPE_OUT_BUTTON,
        #        ['Inner plate Weld', self.Innerflange_weld_details], False)
        # out_list.append(t21)

        # t17 = (None, DISP_EFF, TYPE_TITLE, None, True)
        # out_list.append(t17)
        #
        # t15 = (KEY_FLANGE_WELD_LENGTH, DISP_EFF, TYPE_TEXTBOX,
        #        (self.l_req_flangelength) if flag else '', True)
        # out_list.append(t15)

        return out_list

    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from Column and Column table.
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

    def module_name(self):

        return KEY_DISP_COLUMNCOVERPLATEWELD

    def set_input_values(self, design_dictionary):
        super(ColumnCoverPlateWeld, self).set_input_values(self, design_dictionary)
        # self.module = design_dictionary[KEY_MODULE]
        # global design_status
        # self.design_status = False # todo doubt of true or false
        #
        self.module = design_dictionary[KEY_MODULE]
        # self.connectivity = design_dictionary[KEY_CONN]
        self.preference = design_dictionary[KEY_FLANGEPLATE_PREFERENCES]

        self.section = Column(designation=design_dictionary[KEY_SECSIZE],
                            material_grade=design_dictionary[KEY_SEC_MATERIAL])

        self.flange_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                                fabrication=design_dictionary[KEY_DP_WELD_FAB])
        self.web_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                             fabrication=design_dictionary[KEY_DP_WELD_FAB])

        self.flange_plate = Plate(thickness=design_dictionary.get(KEY_FLANGEPLATE_THICKNESS, None),
                                  material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],
                                  gap=design_dictionary[KEY_DP_DETAILING_GAP])

        self.web_plate = Plate(thickness=design_dictionary.get(KEY_WEBPLATE_THICKNESS, None),
                               material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],
                               gap=design_dictionary[KEY_DP_DETAILING_GAP])
        # self.flange_check_thk = []
        # self.web_check_thk = []
        self.member_capacity_status = False
        self.initial_pt_thk_status= False
        self.web_plate_weld_status= False
        self.flange_plate_weld_status= False
        self.flange_plate_capacity_axial_status= False
        self.recheck_flange_capacity_axial_status= False
        self.web_plate_capacity_axial_status= False
        self.web_plate_capacity_shear_status= False
        self.shear_yielding_status =False
        self.cap_blockcheck_web_axial_status = False
        self.warn_text(self)
        self.member_capacity(self)


        # self.hard_values(self)

    #

    def hard_values(self):
        # Select Selection  HB 450* (inside Ouside)- material E 250 fe 450A

        # load
        self.load.axial_force = 740.181  # KN
        self.load.shear_force = 345.886 # KN
        self.load.moment = 52.745157 # KNM
        self.section.fy = 230
        self.section.fu = 410
        #  Flange Weld
        self.flange_weld.size = 10  # mm
        self.flangespace = 15 #mm
        self.flange_weld.length =500
        self.flange_weld.height = 200
        #  Flange plate
        self.flange_plate.thickness_provided = 12
        self.flange_plate.height = 220
        self.flange_plate.length = 520
        #  Web Weld
        self.web_weld.size = 9  # mm
        self.webspace = 15  # mm
        self.web_weld.length =730
        self.web_weld.height = 340
        #  Web plate
        self.web_plate.thickness_provided = 12
        self.web_plate.length = 750
        self.web_plate.height = 360
        #  Inner Flange weld
        self.flange_weld.size = 10  # mm
        self.flange_plate.thickness_provided = 14
        self.flange_weld.inner_height = 50
        self.flange_weld.inner_length = 500
        #  Inner Flange plate
        self.flange_plate.thickness_provided = 12
        self.flange_plate.Innerheight = 70
        self.flange_plate.Innerlength = 520
        self.flange_plate.gap = 10
        self.web_plate.gap = 10
        self.design_status = True

    def member_capacity(self):
        """
        Axial capacity: [Ref: cl.10.7 IS 800:2007]
        Moment capacity: [Ref: cl.10.7. IS 800:2007]
        Shear capacity: [Ref: cl.8.4 IS 800:2007]
        Limit width thickness ratio: [Ref: Table 2, cl. 3.7.2 and 3.7.4 IS 800:2007]
        Returns:

        """
        self.member_capacity_status = False
        if self.section.type == "Rolled":
            length = self.section.depth
        else:
            length = self.section.depth - (
                    2 * self.section.flange_thickness)  # -(2*self.supported_section.root_radius)
        gamma_m0 = 1.1

        ############################# Axial Capacity N ############################
        self.axial_capacity = round((self.section.area * self.section.fy) / gamma_m0, 2)  # N
        self.axial_load_sec_class = round(
            max(min(self.load.axial_force * 1000, self.axial_capacity), 0.3 * self.axial_capacity), 2)  # N

        # print("self.factored_axial_load", self.factored_axial_load)

        ############################# Shear Capacity  # N############################
        # TODO: Review by anjali. limit shear capacity to 0.6 times
        self.shear_capacity1 = round(((self.section.depth - (2 * self.section.flange_thickness)) *
                                      self.section.web_thickness * self.section.fy * 0.6) / (
                                             math.sqrt(3) * gamma_m0),
                                     2)  # N # A_v: Total cross sectional area in shear in mm^2 (float)
        # TODO: check with sourabh if minimum shear load is min(0.15Vd,40kN)
        self.shear_load1 = min(0.15 * self.shear_capacity1 / 0.6, 40000.0)  # N
        # print('shear_force', self.load.shear_force)

        # #############################################################
        # TODO: to be reviewed by anjali. web section modulus is renamed as Z_wp,Z_we instead of Z_p,Z_e
        self.Z_wp = round(((self.section.web_thickness * (
                self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 4), 2)  # mm3
        self.Z_we = round(((self.section.web_thickness * (
                self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 6), 2)  # mm3

        # TODO: To be reviewed by anjali. section modulus is saved in Z_p,Z_e
        self.Z_p = self.section.plast_sec_mod_z
        self.Z_e = self.section.elast_sec_mod_z

        if self.section.type == "Rolled":
            self.limitwidththkratio_flange = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                           column_t_w=self.section.web_thickness,
                                                                           D=self.section.depth,
                                                                           column_b=self.section.flange_width,
                                                                           column_fy=self.section.fy,
                                                                           factored_axial_force=self.axial_load_sec_class,
                                                                           column_area=self.section.area,
                                                                           compression_element="External",
                                                                           section="Rolled")
        else:
            pass

        if self.section.type2 == "generally":
            self.limitwidththkratio_web = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                        column_t_w=self.section.web_thickness,
                                                                        D=self.section.depth,
                                                                        column_b=self.section.flange_width,
                                                                        column_fy=self.section.fy,
                                                                        factored_axial_force=self.axial_load_sec_class,
                                                                        column_area=self.section.area,
                                                                        compression_element="Web of an I-H",
                                                                        section="generally")
        else:
            pass

        self.class_of_section = int(max(self.limitwidththkratio_flange, self.limitwidththkratio_web))
        # TODO:Review by anjali. initally Z_w = Z_p and Z_e now changed to Z_wp and Z_we
        if self.class_of_section == 1 or self.class_of_section == 2:
            self.Z_w = self.Z_wp
        elif self.class_of_section == 3:
            self.Z_w = self.Z_we

        if self.class_of_section == 1 or self.class_of_section == 2:
            self.beta_b = 1
        elif self.class_of_section == 3:
            self.beta_b = self.Z_e / self.Z_p
        ############################ moment_capacty ############################

        self.section.plastic_moment_capacty(beta_b=self.beta_b, Z_p=self.section.plast_sec_mod_z,
                                            fy=self.section.fy)  # N-mm # for section

        self.section.moment_d_deformation_criteria(fy=self.section.fy, Z_e=self.section.elast_sec_mod_z)
        self.Pmc = self.section.plastic_moment_capactiy  # N-mm
        self.Mdc = self.section.moment_d_def_criteria  # N-mm
        self.section.moment_capacity = round(
            min(self.section.plastic_moment_capactiy, self.section.moment_d_def_criteria), 2)  # N-mm
        ###############################################################################
        # Interaction Ratio
        ##############################################################################
        self.IR_axial = round(self.load.axial_force * 1000 / self.axial_capacity, 4)
        self.IR_shear = round(self.load.shear_force * 1000 / self.shear_capacity1, 4)
        self.IR_moment = round(self.load.moment * 1000000 / self.section.moment_capacity, 4)
        self.sum_IR = round(self.IR_axial + self.IR_moment, 4)

        if self.IR_axial < 0.3 and self.IR_moment < 0.5:
            self.min_axial_load = 0.3 * self.axial_capacity
            self.load_moment_min = 0.5 * self.section.moment_capacity
            logger.warning( "The defined factored load(s) are less than the minimum recommended value [Cl.10.7, IS 800:2007]")
            logger.info("The load values have been set as per the minimum recommendations of Cl.10.7, IS 800:2007")


        elif self.sum_IR <= 1.0 and self.IR_axial < 0.3:

            if (0.3 - self.IR_axial) < (1 - self.sum_IR):
                self.min_axial_load = 0.3 * self.axial_capacity
            else:
                self.min_axial_load = self.load.axial_force * 1000 + ((1 - self.sum_IR) * self.axial_capacity)
            self.load_moment_min = self.load.moment * 1000000
            logger.warning("The defined factored Axial Force is less than the minimum recommended value [Cl.10.7, IS 800:2007]")
            logger.info("The value of Axial Force is set at {} kN".format(round(self.min_axial_load / 1000, 2)))

        elif self.sum_IR <= 1.0 and self.IR_moment < 0.5:

            if (0.5 - self.IR_moment) < (1 - self.sum_IR):
                self.load_moment_min = 0.5 * self.section.moment_capacity
            else:
                self.load_moment_min = self.load.moment * 1000000 + (
                        (1 - self.sum_IR) * self.section.moment_capacity)
            self.min_axial_load = self.load.axial_force * 1000
            logger.warning("The defined factored Bending Moment is less than the minimum recommended value [Cl.10.7, IS 800:2007]")
            logger.info("The value of Bending Moment is set at {} kNm".format(round(self.load_moment_min / 1000000, 2)))
        else:
            self.min_axial_load = self.load.axial_force * 1000
            self.load_moment_min = self.load.moment * 1000000

        ####################
        """
        Load Considered
        """
        #################
        self.load_moment = round(max(self.load_moment_min, self.load.moment * 1000000), 2)  # N
        self.factored_axial_load = round(max(self.load.axial_force * 1000, self.min_axial_load), 2)  # N
        self.fact_shear_load = round(max(self.shear_load1, self.load.shear_force * 1000), 2)  # N

        self.moment_web = round((self.Z_w * self.load_moment / (self.section.plast_sec_mod_z)),
                                2)  # Nm todo add in ddcl # z_w of web & z_p  of section
        self.moment_flange = round(((self.load_moment) - self.moment_web), 2)
        self.axial_force_w = ((self.section.depth - (
                2 * self.section.flange_thickness)) * self.section.web_thickness * self.factored_axial_load) / (
                                 self.section.area)  # N
        self.axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (
            self.section.area)  # N
        self.flange_force = (((self.moment_flange) / (self.section.depth - self.section.flange_thickness)) + (
            self.axial_force_f))

        ###########################################################
        if self.factored_axial_load > self.axial_capacity:
            logger.warning(' : The factored Axial Force exceeds the axial capacity of the column section, {} kN.'.format(
                round(self.axial_capacity / 1000, 2)))
            logger.error(" : Design is UNSAFE \n ")
            logger.info(" :=========End of Design===========")
            self.member_capacity_status = False
        else:
            if self.fact_shear_load > self.shear_capacity1:
                logger.warning(' : The factored Shear Force exceeds the (0.6 times) the shear capacity of the column section, {} kN.'.format(
                    round(self.shear_capacity1 / 1000, 2)))
                logger.error(" : Design of the section subjected to high shear case is not recommended by Osdag. Design is UNSAFE \n ")
                logger.info(" :=========End of Design===========")
                self.member_capacity_status = False
            else:
                if self.load_moment > self.section.moment_capacity:
                    self.member_capacity_status = False

                    logger.warning(' : The factored Bending Moment exceeds the moment capacity of the section, {} kNm.'.format(
                        round(self.section.moment_capacity / 1000000), 2))
                    logger.error(" : Design is UNSAFE \n ")
                    logger.info(" :=========End of Design===========")
                else:
                    self.member_capacity_status = True
                    self.initial_pt_thk(self)

    def initial_pt_thk(self, previous_thk_flange=None, previous_thk_web=None):

        ############################### WEB MENBER CAPACITY CHECK ############################
        ###### # capacity Check for web in axial = yielding

        if (previous_thk_flange) == None:
            pass
        else:
            # for i in previous_thk_flange:
            if previous_thk_flange in self.flange_plate.thickness:
                self.flange_plate.thickness.remove(previous_thk_flange)
            else:
                pass

        if (previous_thk_web) == None:
            pass
        else:
            if previous_thk_web in self.web_plate.thickness:
                self.web_plate.thickness.remove(previous_thk_web)
            else:
                pass

        self.initial_pt_thk_status = False
        self.initial_pt_thk_status_web = False
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.section.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.section.fy)
        if self.section.tension_yielding_capacity_web > self.axial_force_w:

            ################################# FLANGE MEMBER CAPACITY CHECK##############################
            A_v_flange = self.section.flange_thickness * self.section.flange_width
            self.section.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange, fy=self.section.fy)
            if self.section.tension_yielding_capacity > self.flange_force:
                self.web_plate_thickness_possible = [i for i in self.web_plate.thickness if
                                                     i >= (self.section.web_thickness / 2)]
                if self.preference == "Outside":
                    self.flange_plate_thickness_possible = [i for i in self.flange_plate.thickness if
                                                            i >= self.section.flange_thickness]
                else:
                    self.flange_plate_thickness_possible = [i for i in self.flange_plate.thickness if
                                                            i >= (self.section.flange_thickness / 2)]
                if len(self.flange_plate_thickness_possible) == 0:
                    logger.warning(" : The thickness of the Flange Plate is less than the flange thickness")
                    logger.info(
                        " : The Flange Plate should be thicker than the flange of the section, {} mm.".format(self.section.flange_thickness))
                    self.initial_pt_thk_status = False
                    self.design_status = False
                else:
                    self.flange_plate.thickness_provided = self.min_thick_based_on_area(self,
                                                                                        tk=self.section.flange_thickness,
                                                                                        width=self.section.flange_width,
                                                                                        list_of_pt_tk=self.flange_plate_thickness_possible,
                                                                                        t_w=self.section.web_thickness,
                                                                                        r_1=self.section.root_radius,
                                                                                        D=self.section.depth,
                                                                                        preference=self.preference)
                    self.flange_plate.connect_to_database_to_get_fy_fu(self.flange_plate.material,
                                                                       self.flange_plate.thickness_provided)

                    if self.flange_plate.thickness_provided != 0:
                        if self.preference == "Outside":
                            if self.outerwidth < 50:
                                logger.error(" : Outer height of the Flange Plate is less than 50 mm")
                                logger.info(" : Select a wider section")
                                self.initial_pt_thk_status = False
                                self.design_status = False

                            else:
                                if self.flange_plate_crs_sec_area < (self.flange_crs_sec_area * 1.05):
                                    logger.warning(" : Area of the Flange Plate is less than the area of the flange")
                                    logger.info(
                                        " : Area of the Flange Plate should be greater than 1.05 times the area of the flange, {} mm2".format(
                                            round(self.Ap,2)))
                                    logger.info(" : Increase the thickness of the Flange Plate")
                                    self.initial_pt_thk_status = False
                                    self.design_status = False
                                else:
                                    self.initial_pt_thk_status = True
                                    pass
                        else:
                            if self.outerwidth < 50 or self.innerwidth < 50:
                                logger.warning(" : Height of the Flange Plate is less than 50 mm")
                                logger.info(" : Select a wider section")
                                self.initial_pt_thk_status = False
                                self.design_status = False
                            else:
                                if self.flange_plate_crs_sec_area < (self.flange_crs_sec_area * 1.05):
                                    logger.warning(" : Area of the Flange Plate is less than the area of the flange")
                                    logger.info(
                                        " : Area of the Flange Plate should be greater than 1.05 times the area of flange, {} mm2.".format(
                                            round(self.Ap,2)))
                                    logger.info(" : Increase the thickness of the Flange Plates")
                                    self.initial_pt_thk_status = False
                                    self.design_status = False
                                else:
                                    self.initial_pt_thk_status = True
                                    pass
                    else:
                        self.initial_pt_thk_status = False
                        self.design_status = False
                        logger.error(" : Provided Flange Plate thickness is insufficient")

                self.initial_pt_thk_status_web = False
                # self.webheight_status = False
                if len(self.web_plate_thickness_possible) == 0:
                    logger.warning(" : The Web Plate thickness is less than the web thickness of the section")
                    logger.info(
                        " : The Web Plate should be thicker than the web of the section, {} mm".format(self.section.web_thickness))
                    self.initial_pt_thk_status_web = False
                    self.design_status = False
                else:

                    self.web_plate.thickness_provided = self.min_thick_based_on_area(self,
                                                                                     tk=self.section.flange_thickness,
                                                                                     width=self.section.flange_width,
                                                                                     list_of_pt_tk=self.web_plate_thickness_possible,
                                                                                     t_w=self.section.web_thickness,
                                                                                     r_1=self.section.root_radius,
                                                                                     D=self.section.depth,
                                                                                     preference=None,
                                                                                     fp_thk=None)

                    self.web_plate.connect_to_database_to_get_fy_fu(self.web_plate.material,
                                                                    self.web_plate.thickness_provided)
                    if self.web_plate.thickness_provided != 0:
                        if self.preference == "Outside":
                            if self.webplatewidth < self.min_web_plate_height:
                                self.webheight_status = False
                                self.design_status = False
                                logger.error(" : Cannot perform Web Plate design")
                                logger.warning(
                                    " : Web Plate height ({} mm) is less than the min depth of the plate ({} mm)".format(
                                        self.webplatewidth, self.min_web_plate_height))
                                logger.warning("Try a deeper section")
                            else:
                                self.webheight_status = True
                                if self.web_plate_crs_sec_area < (self.web_crs_area * 1.05):
                                    logger.warning(" : Area of the Web Plate is less than the area of the web")
                                    logger.info(
                                        " : Area of the Web Plate should be greater by 1.05 times the area of web, {} mm2".format(
                                            round(self.Wp,2)))
                                    logger.info(" : Increase the thickness of the Web Plate")
                                    self.initial_pt_thk_status_web = False
                                    self.design_status = False
                                else:
                                    self.initial_pt_thk_status_web = True
                                    # self.webheight_status = True
                                    pass
                        else:
                            if self.webplatewidth < self.min_web_plate_height:
                                self.webheight_status = False
                                self.design_status = False
                                logger.error(" : Cannot design the Inner Plate")
                                logger.info(
                                    " : Decrease the thickness of the inner flange plate and/or try a wider/deeper section")

                            else:
                                self.webheight_status = True
                                if self.web_plate_crs_sec_area < (self.web_crs_area * 1.05):
                                    logger.warning(" : Area of the Web Plate is less than the area of the web")
                                    logger.info(
                                        " : Area of the Web Plate should be greater by 1.05 times the area of the web, {} mm2".format(
                                            round(self.Wp,2)))
                                    logger.info(" : Increase the thickness of the web plate")
                                    self.initial_pt_thk_status_web = False
                                    self.design_status = False
                                else:
                                    self.initial_pt_thk_status_web = True

                                    pass
                    else:
                        self.initial_pt_thk_status_web = False
                        logger.error(" : Provided Flange Plate thickness is insufficient")

                if len(self.flange_plate_thickness_possible) == 0:
                    if len(self.flange_plate.thickness) >= 2:
                        self.max_thick_f = max(self.flange_plate.thickness)
                    else:
                        self.max_thick_f = self.flange_plate.thickness[0]
                else:
                    self.max_thick_f = self.flange_plate.thickness_provided

                if len(self.web_plate_thickness_possible) == 0:
                    if len(self.web_plate.thickness) >= 2:
                        self.max_thick_w = max(self.web_plate.thickness)
                    else:
                        self.max_thick_w = self.web_plate.thickness[0]
                else:
                    self.max_thick_w = self.web_plate.thickness_provided

                if self.initial_pt_thk_status == True and self.initial_pt_thk_status_web == True and self.webheight_status == True:
                    self.design_status = True
                    self.web_plate_weld(self)
                else:
                    self.initial_pt_thk_status = False and self.initial_pt_thk_status_web == False and self.webheight_status == False
                    self.design_status = False
                    logger.error(" : Design is UNSAFE \n ")
                    logger.info(" : =========End of Design===========")

            else:
                self.initial_pt_thk_status = False
                self.design_status = False
                logger.warning(" : The tension capacity of the flange is less than the required flange force, {} kN.".format(round(
                    self.flange_force / 1000, 2)))
                logger.info(" : Select a larger column section and/or decrease the applied load(s)")
                logger.error(" : Design is UNSAFE \n ")
                logger.info(" : =========End of Design===========")
        else:
            self.initial_pt_thk_status_web = False
            self.design_status = False
            logger.warning(" : The tension capacity of the web is less than the required axial force, {} kN.".format( round(
                self.axial_force_w / 1000, 2)))
            logger.info(" : Select a larger column section and/or decrease the applied axial force")
            logger.error(" : Design is UNSAFE \n ")
            logger.info(" : =========End of Design===========")

    def web_plate_weld(self):
        """
         available_long_web_length = section.flange_width/2 - gap/2
         self.web_plate.height = width of web plate
         self.webplate.length = height of web plate
        Returns:

        """
        self.web_plate_weld_status = False
        self.min_web_platethk = min(self.web_plate.thickness_provided, self.section.web_thickness)
        self.web_weld.size = int(round_down(self.min_web_platethk - 1.5))
        if self.web_weld.size > self.min_web_platethk:
            self.web_weld.size = self.min_web_platethk
        else:
            pass
        if self.web_weld.size < 3:
            self.web_weld.size = 3
        else:
            pass
        if self.web_weld.size > 16:
            self.web_weld.size = 16
        else:
            pass
        self.webspace = max(15, (self.web_weld.size + 5))
        self.web_weld.get_weld_strength(connecting_fu=[self.web_weld.fu, self.section.fu, self.web_plate.fu],
                                        weld_fabrication=KEY_DP_FAB_SHOP,
                                        t_weld=self.web_weld.size, weld_angle=90)  # in N/mm
        self.web_plate.height = round_down((self.section.depth - (2 * self.section.flange_thickness)
                                            - (2 * self.section.root_radius) - (2 * self.webspace)), 5)
        self.available_long_web_length = round_up((self.section.flange_width / 2) - (self.flange_plate.gap / 2), 5)
        # self.available_long_web_length = round_up((self.web_plate.height/2) - (2*self.web_weld.size)- (self.flange_plate.gap/2) , 5)

        self.web_weld.strength_red = round(self.web_weld.strength, 2)
        # self.available_long_web_length = round_up((self.web_plate.height/2) - (2*self.web_weld.size)- (self.flange_plate.gap/2) , 5)
        self.web_plate_weld_status = False
        while self.web_plate_weld_status == False:
            self.weld_stress(self, d=self.available_long_web_length,
                             b=(self.web_plate.height - (2 * self.web_weld.size)),
                             shear_force=self.fact_shear_load, moment_web=self.moment_web,
                             plate_height=(self.web_plate.height - (2 * self.web_weld.size)),
                             weld_size=self.web_weld.size, axial_force_w=self.axial_force_w)

            self.web_plate.length = 2 * (self.available_long_web_length + (2 * self.web_weld.size)) + self.web_plate.gap
            self.Reduction_factor_web = 1
            if self.web_plate.length >= 150 * self.web_weld.throat_tk:
                self.Reduction_factor_web = round(IS800_2007.cl_10_5_7_3_weld_long_joint(l_j=self.web_plate.length,
                                                                                         t_t=self.web_weld.throat_tk),
                                                  2)
                self.web_weld.strength_red = self.web_weld.strength * self.Reduction_factor_web
                if self.web_weld.strength_red > self.web_weld.stress:
                    self.web_plate_weld_status = True
                    break
                else:
                    self.available_long_web_length = self.available_long_web_length + 50
            else:
                self.Reduction_factor_web = 1
                if self.web_weld.strength > self.web_weld.stress:
                    self.web_weld.strength_red = self.web_weld.strength
                    self.web_plate_weld_status = True
                    break
                else:
                    self.available_long_web_length = self.available_long_web_length + 50

        if self.web_plate_weld_status == True:
            self.web_weld.length = round_up(self.available_long_web_length, 5)
            self.web_plate.length = round_up(
                2 * (self.available_long_web_length + (2 * self.web_weld.size)) + self.web_plate.gap, 5)
            self.web_plate.height = round_down((self.section.depth - (2 * self.section.flange_thickness) -
                                                (2 * self.section.root_radius) - (2 * self.webspace)), 5)
            self.web_weld.height = round_down((self.web_plate.height - (2 * self.web_weld.size)), 5)
            self.l_req_weblength = round_up(self.l_req_weblength, 5)
            self.web_weld.strength = round(self.web_weld.strength, 2)
            self.web_weld.strength_red = round(self.web_weld.strength_red, 2)
            self.flange_plate_weld(self)

        else:
            logger.warning(" : The weld strength of the web plate is less than the required weld stress")
            logger.error(" : Design is UNSAFE \n ")
            logger.info(" : =========End of Design===========")

    def flange_plate_weld(self):
        """
        flange plate length >= 2* self.section.flange_width Eurocode 3 ,page no.176
        self.flange_plate.height = width of flange plate
        self.flange_plate.length = length of flange plate
        Returns:

        """
        self.flange_plate_weld_status = False
        self.min_flange_platethk = min(self.flange_plate.thickness_provided, self.section.flange_thickness)
        self.flange_weld.size = int(round_down(self.min_flange_platethk - 1.5))

        if self.flange_weld.size < 3:
            self.flange_weld.size = 3
        else:
            pass
        if self.flange_weld.size > 16:
            self.flange_weld.size = 16
        else:
            pass
        self.flangespace = max(15, (self.flange_weld.size + 5))
        print("space", self.flangespace)
        self.axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (
            self.section.area)
        self.flange_force = (((self.moment_flange) / (self.section.depth - self.section.flange_thickness)) + (
            self.axial_force_f))

        self.flange_weld.get_weld_strength(
            connecting_fu=[self.flange_weld.fu, self.section.fu, self.flange_plate.fu],
            weld_fabrication=KEY_DP_FAB_SHOP,
            t_weld=self.flange_weld.size,
            weld_angle=90)

        ########### ONLY OUTSIDE ##################################################3
        if self.preference == "Outside":
            self.Required_weld_flange_length = round(self.flange_force / self.flange_weld.strength, 2)
            self.Required_weld_flange_length_round = round_up(self.flange_force / self.flange_weld.strength,
                                                              5)  # c shape half of the splice  plate

            self.flange_plate.height = (self.section.flange_width - (2 * self.flangespace))  # width of the flange plate
            h_weld = self.flange_plate.height - (2 * self.flange_weld.size)
            self.available_long_flange_length = round_up(int((self.Required_weld_flange_length_round - h_weld) / 2), 5,
                                                         (self.section.flange_width))  # half of the one side of the flange plate

            self.l_req_flangelength = ((2 * self.available_long_flange_length) + self.flange_plate.height -
                                       (2 * self.flange_weld.size))
            self.flange_weld.stress = self.flange_force / self.l_req_flangelength
            self.flange_plate.length = (2 * (self.available_long_flange_length + (2 * self.flange_weld.size))
                                        + self.flange_plate.gap)
            self.Reduction_factor_flange = 1
            self.flange_weld.strength_red = round(self.flange_weld.strength, 2)

            # self.flange_plate.length =200
            # self.flange_weld.throat_tk =1
            while self.flange_plate.length >= 150 * self.flange_weld.throat_tk:
                self.Reduction_factor_flange = round(
                    IS800_2007.cl_10_5_7_3_weld_long_joint(l_j=self.flange_plate.length,
                                                           t_t=self.flange_weld.throat_tk), 2)
                self.flange_weld.strength_red = self.flange_weld.strength * self.Reduction_factor_flange
                self.flange_weld.stress = self.flange_force / self.l_req_flangelength
                if self.flange_weld.strength_red > self.flange_weld.stress:
                    break
                else:
                    self.available_long_flange_length = self.available_long_flange_length + 50
                    self.l_req_flangelength = round_up(
                        ((2 * self.available_long_flange_length) + self.flange_plate.height - (
                                2 * self.flange_weld.size)), 2)
                    self.flange_plate.length = 2 * (
                                self.available_long_flange_length + (2 * self.flange_weld.size)) + self.flange_plate.gap

            # self.flange_weld.strength_red = round(self.flange_weld.strength,2)

            if self.flange_weld.strength_red > self.flange_weld.stress:
                self.flange_plate_weld_status = True
                self.flange_weld.length = round_up(self.available_long_flange_length, 5)
                print("self.flange_weld.length", self.flange_weld.length)
                self.flange_plate.length = (2 * (self.available_long_flange_length + (2 * self.flange_weld.size))
                                            + self.flange_plate.gap)
                self.flange_plate.height = round_down((self.section.flange_width - (2 * self.flangespace)), 5)
                self.flange_weld.height = (self.flange_plate.height - (2 * self.flange_weld.size))
                self.l_req_flangelength = round_up(((2 * self.available_long_flange_length) + self.flange_plate.height -
                                                    (2 * self.flange_weld.size)), 5)
                self.flange_weld.strength = round(self.flange_weld.strength, 2)
                self.flange_weld.stress = round(self.flange_weld.stress, 2)
                self.flange_weld.strength_red = round(self.flange_weld.strength_red, 2)
                self.flange_plate_capacity_axial(self)
            else:
                self.flange_plate_weld_status = False
                self.design_status = False
                logger.warning(" : The weld strength of the web plate is less than the required weld stress")
                logger.error(" : Design is UNSAFE \n ")
                logger.info(" : =========End of Design===========")
        else:
            ################ OUTSIDE + INSIDE ###############################
            self.Required_weld_flange_length = round(self.flange_force / self.flange_weld.strength, 2)
            self.total_height_of_inner_plate = (
                        self.section.flange_width - (4 * self.flangespace) - self.section.web_thickness - (
                        2 * self.section.root_radius))  # total width of the inner flange plate
            if self.total_height_of_inner_plate > 0:
                self.flange_plate.Innerheight = (self.total_height_of_inner_plate / 2)
                if self.flange_plate.Innerheight < 50:
                    self.flange_plate_weld_status = False
                    self.design_status = False
                    logger.warning(" : Cannot design with the Inner Plate")
                    logger.info(": Select 'Outside' in the preference menu and re-design")
                else:
                    pass
            else:
                self.flange_plate_weld_status = False
                self.design_status = False

            self.flange_plate.height = (self.section.flange_width - (2 * self.flangespace))
            self.Area_flange_plates = ((2 * self.flange_plate.Innerheight) + self.flange_plate.height) * self.flange_plate.thickness_provided
            self.Outside_plate_area = self.flange_plate.height * self.flange_plate.thickness_provided
            self.Area_ratio = self.Outside_plate_area / self.Area_flange_plates
            self.weld_eff_length_outer = round_up(self.Required_weld_flange_length * self.Area_ratio, 5)


            h_weld = self.flange_plate.height - (2 * self.flange_weld.size)
            self.available_long_flange_length = round_up(int((self.weld_eff_length_outer - h_weld) / 2), 5,
                                                         (self.section.flange_width)) # half of the one side of the flange plate

            self.flange_plate.length = (2 * (self.available_long_flange_length + (2 * self.flange_weld.size))
                                        + self.flange_plate.gap)
            self.l_req_flangelength = ((6 * self.available_long_flange_length) + self.flange_plate.height +
                                       2 * self.flange_plate.Innerheight - (6 * self.flange_weld.size))
            self.flange_weld.stress = self.flange_force / self.l_req_flangelength
            self.flange_weld.strength_red = round(self.flange_weld.strength, 2)
            self.Reduction_factor_flange = 1
            # self.flange_plate.length = 200
            # self.flange_weld.throat_tk = 1
            while self.flange_plate.length >= 150 * self.flange_weld.throat_tk:
                self.flange_weld.stress = self.flange_force / self.l_req_flangelength
                self.Reduction_factor_flange = round(
                    IS800_2007.cl_10_5_7_3_weld_long_joint(l_j=self.flange_plate.length,
                                                           t_t=self.flange_weld.throat_tk), 2)
                self.flange_weld.strength_red = self.flange_weld.strength * self.Reduction_factor_flange
                if self.flange_weld.strength_red > self.flange_weld.stress:
                    break
                else:
                    self.available_long_flange_length = self.available_long_flange_length + 50
                    self.l_req_flangelength = round_up(
                        (6 * self.available_long_flange_length) + self.flange_plate.height \
                        + (2 * self.flange_plate.Innerheight) - (6 * self.flange_weld.size), 2)
                    self.flange_plate.length = (2 * (self.available_long_flange_length + (2 * self.flange_weld.size))
                                                + self.flange_plate.gap)

            if self.flange_weld.strength_red > self.flange_weld.stress:
                self.flange_plate_weld_status = True
                # Outer Plate Details
                self.flange_weld.length = round_up((self.available_long_flange_length), 5)
                self.flange_plate.length = (2 * (self.available_long_flange_length + (2 * self.flange_weld.size))
                                            + self.flange_plate.gap)
                self.flange_plate.height = round_down((self.section.flange_width - (2 * self.flangespace)), 5)
                self.flange_weld.height = round_down((self.flange_plate.height - (2 * self.flange_weld.size)), 5)
                self.l_req_flangelength = round_up(((6 * self.available_long_flange_length) + self.flange_plate.height +
                                                    2 * self.flange_plate.Innerheight - (6 * self.flange_weld.size)), 5)
                # Inner Plate Details
                self.flange_weld.inner_length = self.flange_weld.length
                self.available_long_flange_length = self.available_long_flange_length
                self.flange_plate.Innerlength = self.flange_plate.length
                self.flange_plate.Innerheight = round_down(self.flange_plate.Innerheight, 5)
                self.flange_weld.inner_height = (self.flange_plate.Innerheight - 2 * self.flange_weld.size)
                self.flange_weld.strength_red = round(self.flange_weld.strength_red, 2)
                self.flange_weld.strength = round(self.flange_weld.strength, 2)
                self.flange_weld.stress = round(self.flange_weld.stress, 2)

                if self.flange_plate.thickness_provided > (
                        self.section.root_radius + self.webspace - 5) and self.web_plate.thickness_provided > (
                        self.section.root_radius + self.flangespace - 5):
                    self.design_status = False
                    logger.warning(" : Maximum web plate thickness exceeded")
                    # logger.warning(" : Maximum possible web plate thickness should not be greater than {} mm, to avoid fouling between plates".format(
                    #         self.max_possible_tk))
                    logger.error(" : Design is UNSAFE \n ")
                    logger.info(" : =========End of Design===========")
                    self.flange_plate_weld_status = False

                else:
                    self.flange_plate_weld_status = True
                    self.design_status = True
                    self.flange_plate_capacity_axial(self)

            else:
                self.flange_plate_weld_status = False
                self.design_status = False
                logger.warning(" : The weld strength of the web plate is less than the required weld stress")
                logger.error(" : Design is UNSAFE \n ")
                logger.info(" : =========End of Design===========")

    def flange_plate_capacity_axial(self):  # flange plate capacity check in axial
        self.flange_plate_capacity_axial_status = False
        if self.preference == "Outside":
            A_v_flange = self.flange_plate.thickness_provided * self.flange_plate.height

            self.flange_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange, fy=self.flange_plate.fy)
            self.flange_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_v_flange, fu=self.flange_plate.fu)
            self.flange_plate.tension_capacity_flange_plate = min(self.flange_plate.tension_yielding_capacity,
                                                                  self.flange_plate.tension_rupture_capacity)
            if self.flange_plate.tension_capacity_flange_plate < self.flange_force:
                if len(self.flange_plate.thickness) >= 2:
                    thk = self.flange_plate.thickness_provided
                    self.initial_pt_thk(self, previous_thk_flange= thk)
                else:
                    self.flange_plate_capacity_axial_status = False
                    self.design_status = False
                    logger.warning(
                        ": The tension capacity of the flange is less than the required flange force, {} kN.".format(
                            round(self.flange_force * 1e-3, 2)))
                    logger.info(": Select a larger column section and/or decrease the applied load(s)")
                    logger.error(" : Design is UNSAFE \n ")
                    logger.info(" : =========End of Design===========")
            else:
                self.flange_plate_capacity_axial_status = True
                self.recheck_flange_capacity_axial(self)
        else:
            #  yielding,rupture  for  Oustide + Inside flange plate

            A_v_flange = ((2 * self.flange_plate.Innerheight) + self.flange_plate.height) * self.flange_plate.thickness_provided

            self.flange_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange,
                fy=self.flange_plate.fy)

            self.flange_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_v_flange,
                fu=self.flange_plate.fu)
            self.flange_plate.tension_capacity_flange_plate = round(min(self.flange_plate.tension_yielding_capacity,
                                                                        self.flange_plate.tension_rupture_capacity),
                                                                    2)
            if self.flange_plate.tension_capacity_flange_plate < self.flange_force:
                if len(self.flange_plate.thickness) >= 2:
                    thk = self.flange_plate.thickness_provided
                    self.initial_pt_thk(self, previous_thk_flange=thk)
                else:
                    self.flange_plate_capacity_axial_status = False
                    self.design_status = False
                    logger.warning(
                        ": The tension capacity of the flange plate is less than the required flange force, {} kN.".format(
                            round(self.flange_force / 1000, 2)))
                    logger.info(": Increase the thickness of the flange plate and/or decrease the applied load(s)")
                    logger.error(" : Design is UNSAFE \n ")
                    logger.info(" : =========End of Design===========")
            else:
                self.flange_plate_capacity_axial_status = True
                self.recheck_flange_capacity_axial(self)

    def recheck_flange_capacity_axial(self):
        self.recheck_flange_capacity_axial_status = False
        A_v_flange = self.section.flange_thickness * self.section.flange_width

        self.section.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_flange, fy=self.section.fy)
        self.section.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_v_flange, fu=self.section.fu)
        self.section.tension_capacity_flange = round(min(self.section.tension_yielding_capacity,
                                                         self.section.tension_rupture_capacity), 2)

        if self.section.tension_capacity_flange < self.flange_force:
            self.recheck_flange_capacity_axial_status = False
            self.design_status = False
            logger.warning(
                ": The tension capacity of the flange plate is less than the required flange force, {} kN.".format(
                    round(self.flange_force / 1000, 2)))
            logger.info(": Select a larger column section and/or decrease the applied load(s)")
            logger.error(" : Design is UNSAFE \n ")
            logger.info(" : =========End of Design===========")
        else:
            self.recheck_flange_capacity_axial_status = True
            self.web_plate_capacity_axial(self)

    def web_plate_capacity_axial(self):
        self.web_plate_capacity_axial_status = False
        A_v_web = 2 * self.web_plate.height * self.web_plate.thickness_provided
        self.web_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.web_plate.fy)
        self.web_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_v_web, fu=self.web_plate.fu)
        self.web_plate.tension_capacity_web_plate = round(min(self.web_plate.tension_yielding_capacity,
                                                              self.web_plate.tension_rupture_capacity), 2)
        if self.web_plate.tension_capacity_web_plate < self.axial_force_w:
            if len(self.web_plate.thickness) >= 2:
                thk = self.web_plate.thickness_provided
                self.initial_pt_thk(self, previous_thk_web=thk )
            else:
                self.web_plate_capacity_axial_status = False
                self.design_status = False
                logger.warning(
                    ": The tension capacity of the web plate is less than the required Axial Force, {} kN".format( round(
                        self.axial_force_w / 1000, 2)))
                logger.info(": Increase the thickness of the web plate and/or decrease the applied Axial Force")
                logger.error(" : Design is UNSAFE \n ")
                logger.info(" : =========End of Design===========")

        else:
            self.web_plate_capacity_axial_status = True
            self.web_plate_capacity_shear(self)

    def web_plate_capacity_shear(self):
        self.web_plate_capacity_shear_status = False
        self.shear_yielding_status = False
        A_v_web = 2 * self.web_plate.height * self.web_plate.thickness_provided
        self.web_plate.shear_yielding_capacity = round(0.6*self.shear_yielding(
            A_v=A_v_web, fy=self.web_plate.fy),2)
        if self.web_plate.shear_yielding_capacity  < self.fact_shear_load:
            if len(self.web_plate.thickness) >= 2:
                thk = self.web_plate.thickness_provided
                self.initial_pt_thk(self, previous_thk_web=  thk )
            else:
                self.shear_yielding_status = False
                self.design_status = False
                logger.warning(
                    ": The allowable shear capacity of the web plate is less than the required Shear Force, {} kN".format(
                        round(self.fact_shear_load / 1000, 2)))
                logger.info(": Increase the thickness of the web plate and/or decrease the applied Shear Force")
                logger.error(" : Design is UNSAFE \n ")
                logger.info(" : =========End of Design===========")
        else:
            self.design_status = True
            self.shear_yielding_status = True
        if self.design_status == True:
            self.web_plate.shear_rupture_capacity = self.shear_rupture_(
                A_vn=A_v_web, fu=self.web_plate.fu)
            self.web_plate.shear_capacity_web_plate = round(min(self.web_plate.shear_yielding_capacity,
                                                                self.web_plate.shear_rupture_capacity), 2)
            if self.web_plate.shear_capacity_web_plate < self.fact_shear_load:
                if len(self.web_plate.thickness) >= 2:
                    thk = self.web_plate.thickness_provided
                    self.initial_pt_thk(self, previous_thk_web=  thk )
                else:
                    self.web_plate_capacity_shear_status = False
                    self.design_status = False
                    logger.warning(
                        ": The allowable shear capacity of the web plate is less than the required Shear Force, {} kN".format(
                            round(self.fact_shear_load / 1000, 2)))
                    logger.info(": Increase the thickness of the web plate and/or decrease the applied Shear Force")
                    logger.error(" : Design is UNSAFE \n ")
                    logger.info(" : =========End of Design===========")
            else:
                self.web_plate_capacity_shear_status = True
                self.cap_blockcheck_web_axial(self)

    def cap_blockcheck_web_axial(self):

        self.axial_force_w = ((self.section.depth - (
                    2 * self.section.flange_thickness)) * self.section.web_thickness * self.factored_axial_load) / (
                                 self.section.area)
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.section.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.section.fy)
        self.section.tension_rupture_capacity_web = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_v_web, fu=self.section.fu)
        # available_web_thickness = list( [x for x in self.web_plate.thickness if ((self.web_plate.thickness_provided) <= x)])

        # for self.web_plate.thickness_provided in available_web_thickness:
        design_status_block_shear = False
        while design_status_block_shear == False:
            Avg = 2 * (self.available_long_web_length) * self.section.web_thickness
            Avn = 2 * (self.available_long_web_length) * self.section.web_thickness
            Atg = self.web_plate.height * self.section.web_thickness
            Atn = self.web_plate.height * self.section.web_thickness
            self.section.block_shear_capacity_web = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn,
                                                                                      A_tg=Atg,
                                                                                      A_tn=Atn,
                                                                                      f_u=self.section.fu,
                                                                                      f_y=self.section.fy)
            if self.section.block_shear_capacity_web < self.axial_force_w:
                self.available_long_web_length = self.available_long_web_length + 50
            else:
                design_status_block_shear = True
                break
            # if design_status_block_shear == True:
            #     break
        if design_status_block_shear == True:
            self.section.tension_capacity_web = round(min(self.section.tension_yielding_capacity_web,
                                                          self.section.tension_rupture_capacity_web,
                                                          self.section.block_shear_capacity_web), 2)
            if self.section.tension_capacity_web < self.axial_force_w:
                self.design_status = False
                logger.warning(
                    ": The tension capacity of the web is less than the required Axial Force, {} kN".format(round(self.axial_force_w * 1e-3, 2)))
                logger.info(": Select a larger column section and/or decrease the applied load(s)")
                logger.error(" : Design is UNSAFE \n ")
                logger.info(" : =========End of Design===========")
            else:
                self.design_status = True
                logger.info(" : Overall Column Cover Plate Welded member design is SAFE \n")
                logger.info(" : =========End of Design===========")
        else:
            self.design_status = False
            logger.warning(": The block shear capacity of the web is less than the required Axial Force, {} kN".format(round(self.axial_force_w * 1e-3, 2)))
            logger.info(": Select a larger section")
            logger.error(" : Design is UNSAFE \n ")
            logger.info(" : =========End of Design===========")
        if self.preference == "Outside":
            self.flange_out_plate_tk = self.flange_plate.thickness_provided
            self.flange_in_plate_tk = 0.0
        else:
            self.flange_in_plate_tk = self.flange_plate.thickness_provided
            self.flange_out_plate_tk = self.flange_plate.thickness_provided

        if self.preference == "Outside":
            self.plate_out_len = self.flange_plate.length
            self.plate_in_len = 0.0
        else:
            self.plate_out_len = self.flange_plate.length
            self.plate_in_len = self.flange_plate.Innerlength
        print(self.section)
        print(self.load)
        print("Outside Flange PLate")
        print(self.flange_weld)
        print(self.flange_plate)
        print("Web  PLate")
        print(self.web_weld)
        print(self.web_plate)
        print("flangegap", self.flange_plate.gap)
        print("webgap", self.web_plate.gap)
        print("A", self.load.axial_force)
        print("min_ac", self.min_axial_load / 1000)
        print("axial_capacity", self.axial_capacity / 1000)
        print("app_axial_load", self.factored_axial_load / 1000)
        # print(self.web_plate.thickness_provided)
        # print(self.flange_plate.thickness_provided)
        print("Inside PLate")

        ################################ Extra Functions  #####################################################################################

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
        Tdb = round(Tdb, 3)
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
        Tdb = round(Tdb, 3)
        return Tdb
        # cl 6.2 Design Strength Due to Yielding of Gross Section

    @staticmethod
    def tension_member_design_due_to_yielding_of_gross_section(A_v, fy):
        '''
             Args:
                 A_v (float) Area under shear
                 column_fy (float) Yield stress of  column material
             Returns:
                 Capacity of  column web in shear yielding
             '''
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        # A_v = height * thickness
        tdg = (A_v * fy) / (gamma_m0)
        return tdg

    @staticmethod
    def tension_member_design_due_to_rupture_of_critical_section(A_vn, fu):
        '''
               Args:
                   A_vn (float) Net area under shear
                    column_fu (float) Ultimate stress of  column material
               Returns:
                   Capacity of  column web in shear rupture
               '''

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        # A_vn = (height- bolts_one_line * dia_hole) * thickness
        T_dn = 0.9 * A_vn * fu / (gamma_m1)
        return T_dn

    @staticmethod
    def shear_yielding(A_v, fy):
        '''
        Args:
            length (float) length of member in direction of shear load
            thickness(float) thickness of member resisting shear
             column_fy (float) Yield stress of section material
        Returns:
            Capacity of section in shear yeiding
        '''

        # A_v = length * thickness
        gamma_m0 = 1.1
        # print(length, thickness, fy, gamma_m0)
        # V_p = (0.6 * A_v * fy) / (math.sqrt(3) * gamma_m0 * 1000)  # kN
        V_p = (A_v * fy) / (math.sqrt(3) * gamma_m0)  # N
        return V_p

    @staticmethod
    def shear_rupture_(A_vn, fu):
        '''
               Args:
                   A_vn (float) Net area under shear
                    column_fu (float) Ultimate stress of  column material
               Returns:
                   Capacity of column web in shear rupture
               '''

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        # A_vn = (height- bolts_one_line * dia_hole) * thickness
        T_dn = 0.75 * A_vn * fu / (math.sqrt(3) * gamma_m1)
        return T_dn

    @staticmethod
    def limiting_width_thk_ratio(column_f_t, column_t_w, D, column_b, column_fy, factored_axial_force,
                                 column_area, compression_element, section):
        column_d = D - (2 * column_f_t)
        epsilon = float(math.sqrt(250 / column_fy))
        axial_force_w = int(((D - 2 * (column_f_t)) * column_t_w * factored_axial_force) / (column_area))  # N

        des_comp_stress_web = column_fy
        des_comp_stress_section = column_fy
        avg_axial_comp_stress = axial_force_w / ((D - (2 * column_f_t)) * column_t_w)
        r1 = avg_axial_comp_stress / des_comp_stress_web
        r2 = avg_axial_comp_stress / des_comp_stress_section
        a = column_b / column_f_t
        # column_d = D - 2(column_f_t)
        # compression_element=["External","Internal","Web of an I-H" ,"box section" ]
        # section=["rolled","welded","compression due to bending","generally", "Axial compression" ]
        # section = "rolled"
        if compression_element == "External" or compression_element == "Internal":
            if section == "Rolled":
                if column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 10.5 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 15.7 * epsilon:
                #     class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "semi-compact"
            elif section == "welded":
                if column_b * 0.5 / column_f_t <= 8.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 13.6 * epsilon:
                # class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            elif section == "compression due to bending":
                if column_b * 0.5 / column_f_t <= 29.3 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 33.5 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 42 * epsilon:
                # class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "semi-compact"
                # else:

            #     pass

        elif compression_element == "Web of an I-H" or compression_element == "box section":
            if section == "generally":
                if r1 < 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= (max(105 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "compact"
                    else:
                        class_of_section1 = "semi-compact"
                    # elif column_d / column_t_w <= max((126 * epsilon / (1 + 2 * r2)), (42 * epsilon)):
                    #     class_of_section1 = "semi-compact"
                    # else:
                    #     print('fail')
                    # print("class_of_section3", class_of_section)
                elif r1 > 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= max((105 * epsilon / (1 + (r1 * 1.5))), (
                            42 * epsilon)):
                        class_of_section1 = "compact"
                    else:
                        class_of_section1 = "semi-compact"
                    # elif column_d / column_t_w <= max((126 * epsilon / (1 + 2 * r2)), (
                    #         42 * epsilon)):
                    #     class_of_section1 = "semi-compact"

            elif section == "Axial compression":
                if column_d / column_t_w <= (42 * epsilon):
                    class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "N/A"

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

    def min_thick_based_on_area(self, tk, width, list_of_pt_tk, t_w, r_1, D,
                                preference=None,
                                fp_thk=None):  # area of flange plate should be greater than 1.05 times area of flange
        # 20 is the maximum spacing either side of the plate

        """

              Args:
                  tk: flange thickness
                  width: flange width
                  list_of_pt_tk: list of plate thickness greater than the section thickness
                  t_w: web thickness
                  r_1: root radius
                  D: depth of the section
                  fp_thk: flange thickness provided

                  area of flange plate should be greater than 1.05 times area of flange [Ref: cl.8.6.3.2 IS 800:2007]
                  maximum spacing either side of the plate = 21mm
                  minimum outside flange plate width = 50 mm
                  minimum inside flange plate width = 50 mm

              Returns:

              """
        self.flange_crs_sec_area = tk * width
        self.Ap = self.flange_crs_sec_area * 1.05

        for y in list_of_pt_tk:

            if preference != None:
                if preference == "Outside":
                    self.outerwidth = round_down(width - (2 * 21),5)
                    if self.outerwidth < 50:
                        thickness = y
                        self.initial_pt_thk_status = False
                        self.design_status = False
                    else:
                        pass

                    self.flange_plate_crs_sec_area = y * self.outerwidth
                    if self.flange_plate_crs_sec_area >= self.Ap:
                        thickness = y
                        self.initial_pt_thk_status = True
                        break
                    else:
                        thickness = y
                        self.design_status = False
                elif preference == "Outside + Inside":
                    self.outerwidth = round_down(width - (2 * 21),5)
                    self.innerwidth = round_down((width - t_w - (2 * r_1) - (4 * 21)) / 2,2)
                    if self.innerwidth < 50 and self.outerwidth < 50:
                        thickness = y
                        self.initial_pt_thk_status = False
                        self.design_status = False

                    else:
                        self.flange_plate_crs_sec_area = (self.outerwidth + (2 * self.innerwidth)) * y
                        if self.flange_plate_crs_sec_area >= self.Ap:
                            thickness = y
                            self.initial_pt_thk_status = True
                            break
                        else:
                            thickness = y
                            self.design_status = False

            else:
                self.web_crs_area = round(t_w * (D - (2 * tk)), 2)
                self.Wp = self.web_crs_area * 1.05
                self.webplatewidth = round(D - (2 * tk) - (2 * r_1) - (2 * 21), 2)
                self.min_web_plate_height = self.section.min_plate_height()
                self.webheight_status = False
                if self.webplatewidth < self.min_web_plate_height:
                    thickness = y
                    self.webheight_status = False
                    self.design_status = False
                else:
                    self.web_plate_crs_sec_area = (2 * self.min_web_plate_height) * y

                    if self.web_plate_crs_sec_area >= self.Wp:
                        thickness = y
                        self.webheight_status = True
                        break
                    else:
                        thickness = y
                        self.webheight_status = False
                        self.design_status = False

        return thickness

    def weld_stress(self, d, b, shear_force, moment_web, plate_height, weld_size, axial_force_w):
        '''
        # while calling take the shearforce in KN and moment KNM and axial foce in N
        # d = self.available_long_web_length
        # b = self.web_plate.height - (2 * self.web_weld.size)
        # self.design_status = False
        '''
     #
        cgy = d ** 2 / (2 * d + b)
        cgx = b / 2
        self.y_max = (d ** 2 / (2 * d + b))
        self.x_max = b / 2
        # print("dfdbjfk", y_max, x_max)
        self.ecc = d - (d ** 2 / (2 * d + b))
        self.Ip_weld = ((8 * (d ** 3)) + (6 * d * (b ** 2)) + (b ** 3)) / 12 - ((d ** 4) / (2 * d + b))  # mm4
        self.weld_twist = (shear_force / 2 * self.ecc) + (moment_web / 2)  # Nmm
        # print("self.web_weld_length",self.web_weld_length )
        self.l_req_weblength = (2 * d) + plate_height
        self.web_weld.get_weld_stress(weld_shear=shear_force / 2, weld_axial=axial_force_w / 2,
                                      weld_twist=self.weld_twist, Ip_weld=self.Ip_weld, y_max=self.y_max,
                                      x_max=self.x_max,
                                      l_weld=self.l_req_weblength)

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Column', self.call_3DColumn)
        components.append(t2)

        t4 = ('Cover Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Cover Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Cover Plate", bgcolor)

    ##########################################################################################################################
    def results_to_test(self):
        # test_in_list = {KEY_MODULE: self.module,
        #                 KEY_MAIN_MODULE: self.mainmodule,
        #                 KEY_DISP_SEC_PROFILE: "ISection",
        #                 KEY_DISP_BEAMSEC: self.section.designation,
        #                 KEY_DISP_FLANGESPLATE_PREFERENCES: self.preference,
        #                 KEY_MATERIAL: self.section.material,
        #                 KEY_SEC_FU: self.section.fu,
        #                 KEY_SEC_FY: self.section.fy,
        #                 VALUES_WELD_TYPE: "Fillet Weld",
        #                 KEY_FLANGEPLATE_THICKNESS: self.flange_plate.thickness,
        #                 KEY_WEBPLATE_THICKNESS: self.web_plate.thickness,
        #                 KEY_DP_DETAILING_GAP: self.flange_plate.gap}
        #
        # # def member_capacityoutput(self, flag):

        test_out_list = {KEY_MEMBER_MOM_CAPACITY: round(self.section.moment_capacity / 1000000, 2),
                         KEY_MEMBER_SHEAR_CAPACITY: round(self.shear_capacity1 / 1000, 2),
                         KEY_MEMBER_AXIALCAPACITY: round(self.axial_capacity / 1000, 2),
                         KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY: round(self.Pmc / 1000000, 2),
                         KEY_OUT_DISP_MOMENT_D_DEFORMATION: round(self.Mdc / 1000000, 2),
                         # applied loads
                         KEY_DISP_APPLIED_AXIAL_FORCE: round(self.factored_axial_load / 1000, 2),
                         KEY_DISP_APPLIED_SHEAR_LOAD: round(self.fact_shear_load / 1000, 2),
                         KEY_DISP_APPLIED_MOMENT_LOAD: round(self.load_moment / 1000000, 2),
                         # Flange weld
                         KEY_FLANGE_WELD_SIZE: self.flange_weld.size,
                         KEY_FLANGE_WELD_STRENGTH: self.flange_weld.strength,
                         KEY_FLANGE_WELD_STRESS: self.flange_weld.stress,
                         # web weld
                         KEY_WEB_WELD_SIZE: self.web_weld.size,
                         KEY_WEB_WELD_STRENGTH: self.web_weld.strength_red,
                         KEY_WEB_WELD_STRESS: self.web_weld.stress,
                         # inner plate weld
                         KEY_FLANGE_WELD_SIZE: self.flange_weld.size,
                         KEY_INNERFLANGE_WELD_STRENGTH: self.flange_weld.strength,
                         KEY_INNERFLANGE_WELD_STRESS: self.flange_weld.stress,
                         # webplate
                         KEY_WEB_PLATE_HEIGHT: self.web_plate.height,
                         KEY_WEB_PLATE_LENGTH: self.web_plate.length,
                         KEY_DISP_WEBPLATE_THICKNESS: self.web_plate.thickness_provided,
                         # flange plate_outer
                         KEY_FLANGE_PLATE_HEIGHT: self.flange_plate.height,
                         KEY_FLANGE_PLATE_LENGTH: self.plate_out_len,
                         KEY_DISP_FLANGESPLATE_THICKNESS: self.flange_out_plate_tk,
                         # flange plate_inner
                         KEY_INNERFLANGE_PLATE_HEIGHT: self.flange_plate.Innerheight,
                         KEY_INNERFLANGE_PLATE_LENGTH: self.plate_in_len,
                         KEY_INNERFLANGEPLATE_THICKNESS: self.flange_in_plate_tk,
                         # FLANGE WELD
                         # def flangecapacity(self, flag):
                         KEY_TENSIONYIELDINGCAP_FLANGE: round(self.section.tension_yielding_capacity / 1000, 2),
                         KEY_TENSIONRUPTURECAP_FLANGE: round(self.section.tension_rupture_capacity / 1000, 2),
                         KEY_FLANGE_TEN_CAPACITY: round(self.section.tension_capacity_flange / 1000, 2),
                         # falnge plate capacities
                         KEY_TENSIONYIELDINGCAP_FLANGE_PLATE: round(
                             self.flange_plate.tension_yielding_capacity / 1000, 2),
                         KEY_TENSIONRUPTURECAP_FLANGE_PLATE: round(
                             self.flange_plate.tension_rupture_capacity / 1000, 2),
                         KEY_FLANGE_PLATE_TEN_CAP: round(self.flange_plate.tension_capacity_flange_plate / 1000, 2),
                         # def webcapacity(self, flag):
                         KEY_TENSIONYIELDINGCAP_WEB: round(self.section.tension_yielding_capacity_web / 1000, 2),
                         KEY_TENSIONRUPTURECAP_WEB: round(self.section.tension_rupture_capacity_web / 1000, 2),
                         KEY_TENSIONBLOCK_WEB: round(self.section.block_shear_capacity_web / 1000, 2),
                         KEY_WEB_TEN_CAPACITY: round(self.section.tension_capacity_web / 1000, 2),
                         # web plate capac in axial
                         KEY_TEN_YIELDCAPACITY_WEB_PLATE: round(self.web_plate.tension_yielding_capacity / 1000, 2),
                         KEY_TENSION_RUPTURECAPACITY_WEB_PLATE: round(
                             self.web_plate.tension_rupture_capacity / 1000, 2),
                         KEY_WEB_PLATE_CAPACITY: round(self.web_plate.tension_capacity_web_plate / 1000, 2),
                         # web plate capac in shear
                         KEY_SHEARYIELDINGCAP_WEB_PLATE: round(self.web_plate.shear_yielding_capacity / 1000, 2),
                         KEY_SHEARRUPTURECAP_WEB_PLATE: round(self.web_plate.shear_rupture_capacity / 1000, 2),
                         KEY_WEBPLATE_SHEAR_CAPACITY_PLATE: round(self.web_plate.shear_capacity_web_plate / 1000,
                                                                  2),
                         KEY_WEB_PLATE_MOM_DEMAND: round(self.web_plate.moment_demand / 1000000, 2)}

        return test_out_list
    ################################ Design Report #####################################################################################

    def save_design(self, popup_summary):
        self.gamma_mw_flange = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.flange_weld.fabrication]
        self.gamma_mw_web = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.web_weld.fabrication]
        if self.section.flange_slope == 90:
            image = "Parallel_Beam"
        else:
            image = "Slope_Beam"
        self.report_supporting = {KEY_DISP_SEC_PROFILE: image,
                                  KEY_DISP_BEAMSEC: self.section.designation,
                                  KEY_DISP_MATERIAL: self.section.material,
                                  KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.section.fu,
                                  KEY_DISP_YIELD_STRENGTH_REPORT: self.section.fy,
                                  KEY_REPORT_MASS: self.section.mass,
                                  KEY_REPORT_AREA: round(self.section.area * 1e-2, 2),
                                  KEY_REPORT_DEPTH: self.section.depth,
                                  KEY_REPORT_WIDTH: self.section.flange_width,
                                  KEY_REPORT_WEB_THK: self.section.web_thickness,
                                  KEY_REPORT_FLANGE_THK: self.section.flange_thickness,
                                  KEY_DISP_FLANGE_S_REPORT: self.section.flange_slope,
                                  KEY_REPORT_R1: self.section.root_radius,
                                  KEY_REPORT_R2: self.section.toe_radius,
                                  KEY_REPORT_IZ: round(self.section.mom_inertia_z * 1e-4, 2),
                                  KEY_REPORT_IY: round(self.section.mom_inertia_y * 1e-4, 2),
                                  KEY_REPORT_RZ: round(self.section.rad_of_gy_z * 1e-1, 2),
                                  KEY_REPORT_RY: round(self.section.rad_of_gy_y * 1e-1, 2),
                                  KEY_REPORT_ZEZ: round(self.section.elast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZEY: round(self.section.elast_sec_mod_y * 1e-3, 2),
                                  KEY_REPORT_ZPZ: round(self.section.plast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZPY: round(self.section.plast_sec_mod_y * 1e-3, 2)}

        self.report_input = \
            {KEY_MODULE: self.module,

             KEY_MAIN_MODULE: self.mainmodule,
             # KEY_CONN: self.connectivity,
             KEY_DISP_MOMENT: self.load.moment,
             KEY_DISP_SHEAR: self.load.shear_force,
             KEY_DISP_AXIAL: self.load.axial_force,

             "Column Section - Mechanical Properties": "TITLE",
             "Section Details": self.report_supporting,

             "Weld Details - Input and Design Preference": "TITLE",
             KEY_DISP_DP_WELD_TYPE: "Fillet",
             KEY_DISP_DP_WELD_FAB: self.flange_weld.fabrication,
             KEY_DISP_DP_WELD_MATERIAL_G_O_REPORT: self.flange_weld.fu,
             # KEY_WEBPLATE_THICKNESS:str(self.plate_thick_customized()),
             # KEY_FLANGEPLATE_THICKNESS:str(self.plate_thick_customized()),

             # "Safety Factors - IS 800:2007 Table 5 (Clause 5.4.1) ": "TITLE",
             # KEY_DISP_GAMMA_M0: cl_5_4_1_table_4_5_gamma_value(1.1, "m0"),
             # KEY_DISP_GAMMA_M1: cl_5_4_1_table_4_5_gamma_value(1.25, "m1"),
             # KEY_DISP_GAMMA_MW: cl_5_4_1_table_4_5_gamma_value(self.gamma_mw_flange, "mw"),

             "Plate Details - Input and Design Preference": "TITLE",
             KEY_DISP_FLANGESPLATE_PREFERENCES: self.preference,
             KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.flange_plate.fu,
             KEY_DISP_YIELD_STRENGTH_REPORT: self.flange_plate.fy,
             KEY_DISP_MATERIAL: self.flange_plate.material,
             KEY_DISP_FLANGESPLATE_THICKNESS: str(list(np.int_(self.flange_plate.thickness))),
             KEY_DISP_WEBPLATE_THICKNESS: str(list(np.int_(self.web_plate.thickness))),
             }

        self.report_check = []

        flange_weld_conn_plates_fu = [self.section.fu, self.flange_plate.fu]
        self.flange_weld_connecting_plates = [self.section.flange_thickness, self.flange_plate.thickness_provided]
        self.flange_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(self.section.flange_thickness,
                                                                         self.flange_plate.thickness_provided)
        self.gamma_mw_flange = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.flange_weld.fabrication]
        web_weld_strength_kn = round(self.web_weld.strength, 2)
        web_weld_strength_red_kn = round(self.web_weld.strength_red, 2)
        web_weld_stress_kn = round(self.web_weld.stress, 2)
        web_weld_strength_recal_kn = round(self.web_weld.stress, 2)

        flange_weld_strength_kn = round(self.flange_weld.strength, 2)
        flange_weld_strength_red_kn = round(self.flange_weld.strength_red, 2)
        flange_weld_stress_kn = round(self.flange_weld.stress, 2)
        flange_weld_strength_recal_kn = round(self.flange_weld.stress, 2)

        self.Kt = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness_constant()
        h = round(self.section.depth - (2 * self.section.flange_thickness), 2)
        self.Pmc = self.section.plastic_moment_capactiy
        self.Mdc = self.section.moment_d_def_criteria

        t1 = ('SubSection', 'Member Capacity', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        t1 = (SECTION_CLASSIFICATION, "", cl_3_7_2_section_classification(class_of_section=self.class_of_section), "")
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_AXIAL_CAPACITY, display_prov(self.load.axial_force, "P_x"),
              cl_6_2_tension_yield_capacity_member(l=None, t=None, f_y=self.section.fy, gamma=gamma_m0,
                                                   T_dg=round(self.axial_capacity / 1000, 2), multiple=None,
                                                   area=round(self.section.area, 2)),'')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_SHEAR_CAPACITY, '', cl_8_4_shear_yielding_capacity_member(h=h, t=self.section.web_thickness,
                                                                                     f_y=self.section.fy, gamma_m0=gamma_m0,
                                                                                     V_dg=round(
                                                                    self.shear_capacity1 / 1000 / 0.6, 2)), '')
        self.report_check.append(t1)
        initial_shear_capacity = round(self.shear_capacity1 / 1000 / 0.6, 2)
        reduced_shear_capacity = round(self.shear_capacity1 / 1000, 2)
        t1 = (KEY_DISP_ALLOW_SHEAR, display_prov(self.load.shear_force, "V_y"),
              allow_shear_capacity(initial_shear_capacity, reduced_shear_capacity),
              get_pass_fail(self.load.shear_force, reduced_shear_capacity, relation="lesser"))
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY, '', cl_8_2_1_2_plastic_moment_capacity_member(beta_b=round(self.beta_b, 2),
                                                                                                  Z_p=round(self.Z_p, 2),
                                                                                                  f_y=self.section.fy,
                                                                                                  gamma_m0=gamma_m0,
                                                                                                  Pmc=round(self.Pmc / 1000000, 2)), '')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_MOMENT_D_DEFORMATION, '', cl_8_2_1_2_deformation_moment_capacity_member(fy=self.section.fy,
                                                                                                   Z_e=round(
                                                                                       self.section.elast_sec_mod_z, 2),
                                                                                                   Mdc=round(self.Mdc / 1000000, 2)),
              '')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_MOMENT_CAPACITY, display_prov(self.load.moment, "M_z"), cl_8_2_moment_capacity_member(Pmc=round(self.Pmc / 1000000, 2),
                                                                                                               Mdc=round(self.Mdc / 1000000, 2),
                                                                                                               M_c=round(
                                                                                  self.section.moment_capacity / 1000000,
                                                                                  2)),
              '')
        self.report_check.append(t1)
        t1 = ('SubSection', 'Load Consideration', '|p{3cm}|p{6cm}|p{5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        #####INTERACTION RATIO#######

        t1 = (KEY_INTERACTION_RATIO, '', ir_sum_bb_cc(Al=self.load.axial_force, M=self.load.moment,
                                                      A_c=round(self.axial_capacity / 1000, 2),
                                                      M_c=round(self.section.moment_capacity / 1000000, 2),
                                                      IR_axial=self.IR_axial, IR_moment=self.IR_moment,
                                                      sum_IR=self.sum_IR), '')
        self.report_check.append(t1)
        #############################
        #### Min load Required ###############
        t2 = (MIN_LOADS_REQUIRED, min_loads_required(conn="beam_beam"),
              min_loads_provided(min_ac=round(self.min_axial_load / 1000, 2),
                                 min_mc=round(self.load_moment_min / 1000000, 2),
                                 conn="beam_beam"), '')
        self.report_check.append(t2)

        #############################
        t1 = (KEY_DISP_APPLIED_AXIAL_FORCE, display_prov(self.load.axial_force, "P_x"),
              prov_axial_load(axial_input=self.load.axial_force, min_ac=round(self.min_axial_load / 1000, 2),
                              app_axial_load=round(self.factored_axial_load / 1000, 2),
                              axial_capacity=round(self.axial_capacity / 1000, 2)), '')

        self.report_check.append(t1)
        V_dy = round(self.shear_capacity1 / 0.6 / 1000, 2)
        t1 = (KEY_DISP_APPLIED_SHEAR_LOAD, display_prov(self.load.shear_force, "V_y"),
              prov_shear_load(shear_input=self.load.shear_force, min_sc=round(self.shear_load1 / 1000, 2),
                              app_shear_load=round(self.fact_shear_load / 1000, 2),
                              shear_capacity_1=V_dy), "")
        self.report_check.append(t1)
        t1 = (KEY_DISP_APPLIED_MOMENT_LOAD, display_prov(self.load.moment, "M_z"),
              prov_moment_load(moment_input=self.load.moment, min_mc=round(self.load_moment_min / 1000000, 2),
                               app_moment_load=round(self.load_moment / 1000000, 2),
                               moment_capacity=round(self.section.moment_capacity / 1000000, 2), moment_capacity_supporting=0.0), "")

        self.report_check.append(t1)
        t23 = (KEY_OUT_DISP_FORCES_WEB, '', forces_in_web(Au=round(self.factored_axial_load / 1000, 2),
                                                          T=self.section.flange_thickness,
                                                          A=round(self.section.area, 2),
                                                          t=self.section.web_thickness, D=self.section.depth,
                                                          Zw=round(self.Z_w, 2),
                                                          Mu=round(self.load_moment / 1000000, 2),
                                                          Z=round(self.section.plast_sec_mod_z, 2),
                                                          Mw=round(self.moment_web / 1000000, 2),
                                                          Aw=round(self.axial_force_w / 1000, 2)), '')
        self.report_check.append(t23)
        t23 = (KEY_OUT_DISP_FORCES_FLANGE, '', forces_in_flange(Au=round(self.factored_axial_load / 1000, 2),
                                                                B=self.section.flange_width,
                                                                T=self.section.flange_thickness,
                                                                A=round(self.section.area, 2),
                                                                D=self.section.depth,
                                                                Mu=round(self.load_moment / 1000000, 2),
                                                                Mw=round(self.moment_web / 1000000, 2),
                                                                Mf=round(self.moment_flange / 1000000, 2),
                                                                Af=round(self.axial_force_f / 1000, 2),
                                                                ff=round(self.flange_force / 1000, 2), ), '')
        self.report_check.append(t23)
        if self.design_status == False:
            if self.member_capacity_status == True:
                t2 = ('SubSection', 'Initial Member Check', '|p{3cm}|p{4.5cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t2)
                t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE, display_prov(round(self.flange_force / 1000, 2), "F_f"),
                      cl_6_2_tension_yield_capacity_member(self.section.flange_width,
                                                           self.section.flange_thickness,
                                                           self.section.fy, gamma_m0,
                                                           round(self.section.tension_yielding_capacity / 1000, 2), 1),
                      get_pass_fail(round(self.flange_force / 1000, 2),
                                    round(self.section.tension_yielding_capacity / 1000, 2), relation="leq"))
                self.report_check.append(t1)
                if self.section.tension_yielding_capacity > self.flange_force:
                    webheight = round((self.section.depth - 2 * self.section.flange_thickness), 2)
                    t1 = (KEY_DISP_TENSIONYIELDINGCAP_WEB, display_prov(round(self.axial_force_w / 1000, 2), "A_w"),
                          cl_6_2_tension_yield_capacity_member(webheight,
                                                               self.section.web_thickness,
                                                               self.section.fy, gamma_m0,
                                                               round(self.section.tension_yielding_capacity_web / 1000, ), 1),
                          get_pass_fail(round(self.axial_force_w / 1000, 2),
                                        round(self.section.tension_yielding_capacity_web / 1000, ), relation="leq"))
                    self.report_check.append(t1)
            if self.member_capacity_status == True and (
                    self.section.tension_yielding_capacity > self.flange_force) and (
                    len(self.flange_plate_thickness_possible) != 0):
                t1 = ('SubSection', 'Initial Flange Plate Height Check', '|p{4.5cm}|p{2.5cm}|p{7cm}|p{1.5cm}|')
                self.report_check.append(t1)
                if self.preference == "Outside":
                    t1 = ('Flange Plate Width (mm)', 'Bfp >= 50',
                          width_pt_chk(B=self.section.flange_width,
                                       t=self.section.web_thickness, r_1=self.section.root_radius, pref="Outside"),
                          get_pass_fail(50, round(self.outerwidth, 2), relation="leq"))
                    self.report_check.append(t1)

                else:
                    t1 = ('Flange Plate Width (mm)', 'Bfp >= 50',
                          width_pt_chk(B=self.section.flange_width,
                                       t=self.section.web_thickness, r_1=self.section.root_radius, pref="Outside"),
                          get_pass_fail(50, round(self.outerwidth, 2), relation="leq"))
                    self.report_check.append(t1)

                    t1 = ('Flange Plate Inner Width (mm)', 'Bifp >= 50',
                          width_pt_chk(B=self.section.flange_width,
                                       t=self.section.web_thickness, r_1=self.section.root_radius,
                                       pref="Outside +Inside"),
                          get_pass_fail(50, round(self.innerwidth, 2), relation="leq"))
                    self.report_check.append(t1)

            if self.member_capacity_status == True and (self.section.tension_yielding_capacity > self.flange_force):
                if self.initial_pt_thk_status == True:
                    self.thick_f = self.flange_plate.thickness_provided
                    self.thick_w = self.web_plate.thickness_provided
                else:
                    self.thick_f = self.max_thick_f
                    self.thick_w = self.max_thick_w
                t1 = ('SubSection', 'Flange Plate Thickness', '|p{2.5cm}|p{5cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                if self.preference == "Outside":
                    t2 = (KEY_DISP_FLANGESPLATE_THICKNESS, display_prov(self.section.flange_thickness, "T"),
                          display_prov(self.thick_f, "t_{fp}"),
                          get_pass_fail(self.section.flange_thickness, self.thick_f, relation="lesser"))
                    self.report_check.append(t2)
                    if (len(self.flange_plate_thickness_possible) != 0) and self.outerwidth >= 50:
                        t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area, 2),
                                                                  flange_web_area=round(self.Ap, 2)),
                              flange_plate_area_prov(B=self.section.flange_width, pref="Outside", y=self.thick_f,
                                                     outerwidth=round(self.outerwidth, 2),
                                                     fp_area=round(self.flange_plate_crs_sec_area, 2),
                                                     t=self.section.web_thickness, r_1=self.section.root_radius, ),
                              get_pass_fail(self.Ap, self.flange_plate_crs_sec_area, relation="leq"))
                        self.report_check.append(t2)
                else:
                    t2 = (KEY_DISP_FLANGESPLATE_THICKNESS, display_prov(self.section.flange_thickness / 2, "T"),
                          display_prov(self.thick_f, "t_{fp}"),
                          get_pass_fail(self.section.flange_thickness / 2, self.thick_f, relation="lesser"))
                    self.report_check.append(t2)
                    # flange_plate_crs_sec_area = (self.outerwidth + (2 * self.innerwidth)) * self.thick_f
                    if len(
                            self.flange_plate_thickness_possible) != 0 and self.innerwidth >= 50 and self.outerwidth >= 50:
                        t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area, 2),
                                                                  flange_web_area=round(self.Ap, 2)),
                              flange_plate_area_prov(B=self.section.flange_width, pref="Outside+Inside",
                                                     y=self.thick_f,
                                                     outerwidth=round(self.outerwidth, 2),
                                                     fp_area=round(self.flange_plate_crs_sec_area, 2),
                                                     t=self.section.web_thickness, r_1=self.section.root_radius,
                                                     innerwidth=round(self.innerwidth, 2)),
                              get_pass_fail(self.Ap, self.flange_plate_crs_sec_area, relation="leq"))
                        self.report_check.append(t2)
                # if (self.flange_plate_crs_sec_area >= (1.05 * self.flange_crs_sec_area)) and len(self.flange_plate_thickness_possible) != 0 and len(self.web_plate_thickness_possible) != 0 :
            if self.member_capacity_status == True and (
                    self.section.tension_yielding_capacity > self.flange_force) and (
                    len(self.flange_plate_thickness_possible) != 0):
                t1 = ('SubSection', 'Initial Web Plate Height Check', '|p{3cm}|p{5.5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                t1 = (
                    'Web Plate Height (mm)', min_plate_ht_req(D=self.section.depth, min_req_width=self.min_web_plate_height, r_r=self.section.root_radius,
                                                           t_f=self.section.flange_thickness),
                    web_width_chk_weld(D=self.section.depth,
                                   tk=self.section.flange_thickness,
                                   R_1=self.section.root_radius,
                                   webplatewidth=self.webplatewidth),
                    get_pass_fail(self.min_web_plate_height, self.webplatewidth, relation="leq"))
                self.report_check.append(t1)

            if self.member_capacity_status == True and (self.section.tension_yielding_capacity > self.flange_force):
                t1 = ('SubSection', 'Web Plate Thickness', '|p{2.5cm}|p{5cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                t2 = (KEY_DISP_WEBPLATE_THICKNESS, display_prov(self.section.web_thickness / 2, "t"),
                      display_prov(self.thick_w, "t_{wp}"),
                      get_pass_fail(self.section.web_thickness / 2, self.thick_w, relation="lesser"))
                self.report_check.append(t2)
                if len(self.web_plate_thickness_possible) != 0 and self.webplatewidth > self.min_web_plate_height:
                    # if (self.flange_plate_crs_sec_area >= 1.05 * self.flange_crs_sec_area):
                    t2 = (KEY_DISP_AREA_CHECK,
                          plate_area_req(crs_area=round(self.web_crs_area, 2), flange_web_area=round(self.Wp, )),
                          web_plate_area_prov(D=self.section.depth, y=self.thick_w,
                                              webwidth=self.min_web_plate_height,
                                              wp_area=round(self.web_plate_crs_sec_area, 2),
                                              T=self.section.flange_thickness, r_1=self.section.root_radius),
                          get_pass_fail(self.Wp, self.web_plate_crs_sec_area, relation="leq"))
                    self.report_check.append(t2)
            # if self.initial_pt_thk_status == True and self.initial_pt_thk_status_web == True:
            #     t1 = ('SubSection', 'Recheck web height', '|p{2.5cm}|p{4.5cm}|p{7cm}|p{1.5cm}|')
            #     self.report_check.append(t1)
            #     t1 = (KEY_WEB_PLATE_HEIGHT, self.min_web_plate_height, self.web_plate.height,
            #           get_pass_fail(self.min_web_plate_height, self.web_plate.height, relation="leq"))
            #     self.report_check.append(t1)
        else:
            pass

        ##################################weld design check remains same for outside and " outside +inside" ########################################
        if self.initial_pt_thk_status == True and self.initial_pt_thk_status_web == True and self.web_plate_weld_status == True:
            t1 = ('SubSection', 'Flange Weld Design', '|p{3cm}|p{5.5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            if self.preference == "Outside":
                t2 = (DISP_MIN_FLANGE_PLATE_THICK, display_prov(self.section.flange_thickness, "T"),
                      display_prov(self.flange_plate.thickness_provided, "t_{fp}"),
                      get_pass_fail(self.section.flange_thickness, self.flange_plate.thickness_provided,
                                    relation="lesser"))
                self.report_check.append(t2)
            else:
                t2 = (DISP_MIN_FLANGE_PLATE_THICK, display_prov(self.section.flange_thickness / 2, "T"),
                      display_prov(self.flange_plate.thickness_provided, "t_{fp}"),
                      get_pass_fail(self.section.flange_thickness / 2, self.flange_plate.thickness_provided,
                                    relation="lesser"))
                self.report_check.append(t2)

            # Flange Weld size#
            t2 = (DISP_MIN_WELD_SIZE, cl_10_5_2_3_min_fillet_weld_size_required(conn_plates_weld=self.flange_weld_connecting_plates,
                                                                                min_weld_size=self.flange_weld_size_min),
                  display_prov(self.flange_weld.size, "t_w"),
                  get_pass_fail(self.flange_weld_size_min, self.flange_weld.size, relation="leq"))
            self.report_check.append(t2)
            t2 = (DISP_MAX_WELD_SIZE, cl_10_5_3_1_max_weld_size(conn_plates_weld=self.flange_weld_connecting_plates,
                                                                max_weld_size=self.min_flange_platethk),
                  display_prov(self.flange_weld.size, "t_w"),
                  get_pass_fail(self.min_flange_platethk, self.flange_weld.size, relation="geq"))
            self.report_check.append(t2)
            t2 = (KEY_DISP_CLEARANCE, spacing(sp=self.flangespace, t_w=self.flange_weld.size),
                  display_prov(self.flangespace, "sp"),
                  get_pass_fail(self.min_flange_platethk, self.flange_weld.size, relation="geq"))
            self.report_check.append(t2)
            # Throat thickness #
            t1 = (DISP_THROAT, cl_10_5_3_1_throat_thickness_req(), cl_10_5_3_1_throat_thickness_weld(self.flange_weld.size, self.Kt),
                  get_pass_fail(3.0, self.flange_weld.size, relation="leq"))
            self.report_check.append(t1)
            #####Strength of the weld ####
            if self.preference == "Outside":
                t1 = (DISP_EFF, ' ', eff_len_prov(l_w=self.flange_weld.length, b_fp=self.flange_plate.height,
                                                  t_w=self.flange_weld.size, l_eff=self.l_req_flangelength,
                                                  con="Flange"), "")
                self.report_check.append(t1)
                t2 = (KEY_FLANGE_DISP_WELD_STRENGTH,
                      flange_weld_stress(F_f=round(self.flange_force / 1000, 2), l_eff=self.l_req_flangelength,
                                         F_ws=round(self.flange_weld.stress, 2)),
                      cl_10_5_7_1_1_weld_strength(conn_plates_weld_fu=flange_weld_conn_plates_fu,
                                                  gamma_mw=self.gamma_mw_flange, t_t=self.flange_weld.throat_tk,
                                                  f_w=self.flange_weld.strength),
                      get_pass_fail(self.flange_weld.stress, self.flange_weld.strength, relation="lesser"))
                self.report_check.append(t2)
                t15 = (KEY_OUT_LONG_JOINT_WELD, long_joint_welded_req(),
                       long_joint_welded_beam_prov(plate_height=self.flange_plate.height,
                                                   l_w=self.available_long_flange_length, t_w=self.flange_weld.size,
                                                   gap=self.flange_plate.gap, t_t=self.flange_weld.throat_tk,
                                                   Tc=flange_weld_strength_kn, Tr=flange_weld_strength_red_kn), "")
                self.report_check.append(t15)
                t5 = (
                    KEY_OUT_DISP_RED_WELD_STRENGTH, flange_weld_stress_kn, flange_weld_strength_red_kn,
                    get_pass_fail(flange_weld_stress_kn, flange_weld_strength_red_kn,
                                  relation="lesser"))
                self.report_check.append(t5)

                # Outside +Inside#
            else:
                # Outside
                t1 = (KEY_DISP_WELD_LEN_EFF_OUTSIDE, '',
                      eff_len_prov_out_in(l_w=self.flange_weld.length, b_fp=self.flange_plate.height,
                                          b_ifp=self.flange_plate.Innerheight, t_w=self.flange_weld.size,
                                          l_eff=self.l_req_flangelength), "")
                self.report_check.append(t1)
                t2 = (KEY_FLANGE_DISP_WELD_STRENGTH,
                      flange_weld_stress(F_f=round(self.flange_force / 1000, 2), l_eff=self.l_req_flangelength,
                                         F_ws=round(self.flange_weld.stress, 2)),
                      cl_10_5_7_1_1_weld_strength(conn_plates_weld_fu=flange_weld_conn_plates_fu,
                                                  gamma_mw=self.gamma_mw_flange, t_t=self.flange_weld.throat_tk,
                                                  f_w=self.flange_weld.strength),
                      get_pass_fail(self.flange_weld.stress, self.flange_weld.strength, relation="lesser"))
                self.report_check.append(t2)
                t15 = (KEY_OUT_LONG_JOINT_WELD, long_joint_welded_req(),
                       long_joint_welded_beam_prov(plate_height=self.flange_plate.height,
                                                   l_w=self.available_long_flange_length, t_w=self.flange_weld.size,
                                                   gap=self.flange_plate.gap, t_t=self.flange_weld.throat_tk,
                                                   Tc=flange_weld_strength_kn, Tr=flange_weld_strength_red_kn), "")
                self.report_check.append(t15)
                t5 = (KEY_OUT_DISP_RED_WELD_STRENGTH, flange_weld_stress_kn, flange_weld_strength_red_kn,
                      get_pass_fail(flange_weld_stress_kn, flange_weld_strength_red_kn,
                                    relation="lesser"))
                self.report_check.append(t5)

            if self.preference == "Outside":
                self.min_height_required = 50
                self.min_length_required_flange = 2*self.section.flange_width
                t1 = ('SubSection', 'Flange Plate Dimension Check - Outside', '|p{3.5cm}|p{4.5cm}|p{6cm}|p{1.5cm}|')
                self.report_check.append(t1)
                t1 = (DISP_MIN_FLANGE_PLATE_HEIGHT, self.min_height_required,
                      height_of_flange_cover_plate(B=self.section.flange_width, sp=self.flangespace,
                                                   b_fp=self.flange_plate.height),
                      get_pass_fail(self.min_height_required, self.flange_plate.height, relation="lesser"))
                self.report_check.append(t1)
                t1 = (DISP_MAX_FLANGE_PLATE_HEIGHT,
                      height_of_flange_cover_plate(B=self.section.flange_width, sp=self.flangespace,
                                                   b_fp=self.flange_plate.height), self.flange_plate.height,
                      get_pass_fail(self.flange_plate.height, self.flange_plate.height, relation="leq"))
                self.report_check.append(t1)
                t1 = (DISP_MIN_FLANGE_PLATE_LENGTH, self.min_length_required_flange,
                      plate_Length_req(l_w=self.flange_weld.length, t_w=self.flange_weld.size, g=self.flange_plate.gap,
                                       l_fp=self.flange_plate.length, conn="Flange"),
                      get_pass_fail(self.min_length_required_flange, self.flange_plate.length, relation="leq"))
                self.report_check.append(t1)

                t2 = (DISP_MIN_FLANGE_PLATE_THICK, display_prov(self.section.flange_thickness, "T"),
                      display_prov(self.flange_plate.thickness_provided, "t_{fp}"),
                      get_pass_fail(self.section.flange_thickness, self.flange_plate.thickness_provided,
                                    relation="lesser"))
                self.report_check.append(t2)

                self.Recheck_flange_pt_area_o = (self.flange_plate.height) * \
                                                self.flange_plate.thickness_provided
                t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area, 2),
                                                          flange_web_area=round(self.Ap, 2)),
                      plate_recheck_area_weld(outerwidth=self.flange_plate.height,
                                              f_tp=self.flange_plate.thickness_provided, conn="flange",
                                              pref="Outside"),
                      get_pass_fail(self.Ap, self.Recheck_flange_pt_area_o, relation="leq"))
                self.report_check.append(t2)
            else:
                t1 = ('SubSection', 'Flange Plate Dimension Check - Outside/Inside', '|p{3cm}|p{5.5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                self.min_height_required = 50
                self.min_length_required_flange = 2*self.section.flange_width
                ###Outside####
                t1 = (DISP_MIN_FLANGE_PLATE_HEIGHT, self.min_height_required,
                      height_of_flange_cover_plate(B=self.section.flange_width, sp=self.flangespace,
                                                   b_fp=self.flange_plate.height),
                      get_pass_fail(self.min_height_required, self.flange_plate.height, relation="lesser"))
                self.report_check.append(t1)
                t1 = (DISP_MAX_FLANGE_PLATE_HEIGHT,
                      height_of_flange_cover_plate(B=self.section.flange_width, sp=self.flangespace,
                                                   b_fp=self.flange_plate.height), self.flange_plate.height,
                      get_pass_fail(self.flange_plate.height, self.flange_plate.height, relation="leq"))
                self.report_check.append(t1)
                t1 = (DISP_MIN_FLANGE_PLATE_LENGTH,   self.min_length_required_flange,
                      plate_Length_req(l_w=self.flange_weld.length, t_w=self.flange_weld.size, g=self.flange_plate.gap,
                                       l_fp=self.flange_plate.length, conn="Flange"),
                      get_pass_fail(  self.min_length_required_flange, self.flange_plate.length, relation="lesser"))
                self.report_check.append(t1)
                ####Inside###
                # min_inner_height_weld = int(
                #     (self.section.flange_width - self.section.web_thickness - (self.section.root_radius * 2)) / 2)
                min_inner_ht_req = 50
                t1 = (DISP_MIN_PLATE_INNERHEIGHT, '>=50',
                      self.flange_plate.Innerheight,
                      get_pass_fail(min_inner_ht_req, self.flange_plate.Innerheight, relation="leq"))
                self.report_check.append(t1)
                t1 = (DISP_MAX_PLATE_INNERHEIGHT,
                      inner_plate_height_weld(B=self.section.flange_width, sp=self.flangespace,
                                              t=self.section.web_thickness, r_1=self.section.root_radius,
                                              b_ifp=self.flange_plate.Innerheight), self.flange_plate.Innerheight,
                      get_pass_fail(self.flange_plate.Innerheight, self.flange_plate.Innerheight, relation="leq"))
                self.report_check.append(t1)
                t1 = (DISP_MIN_PLATE_INNERLENGTH, self.min_length_required_flange,
                      plate_Length_req(l_w=self.flange_weld.inner_length, t_w=self.flange_weld.size,
                                       g=self.flange_plate.gap, l_fp=self.flange_plate.Innerlength, conn="Flange"),
                      get_pass_fail(self.min_length_required_flange, self.flange_plate.Innerlength, relation="lesser"))
                self.report_check.append(t1)
                t2 = (DISP_MIN_FLANGE_PLATE_THICK, display_prov(self.section.flange_thickness / 2, "T"),
                      display_prov(self.flange_plate.thickness_provided, "t_{fp}"),
                      get_pass_fail(self.section.flange_thickness / 2, self.flange_plate.thickness_provided,
                                    relation="lesser"))
                self.report_check.append(t2)
                # flange_plate_crs_sec_area = (self.outerwidth + (2 * self.innerwidth)) * self.thick_f
                self.Recheck_flange_pt_area_oi = (self.flange_plate.height + (2 * self.flange_plate.Innerheight)) * \
                                                 self.flange_plate.thickness_provided
                t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area, 2),
                                                          flange_web_area=round(self.Ap, 2)),
                      plate_recheck_area_weld(outerwidth=self.flange_plate.height,
                                              innerwidth=self.flange_plate.Innerheight,
                                              f_tp=self.flange_plate.thickness_provided, t_wp=None, conn="flange",
                                              pref="Outside+Inside"),
                      get_pass_fail(self.Ap, self.Recheck_flange_pt_area_oi, relation="leq"))
                self.report_check.append(t2)

        #######################################################Web design###########################################################

        if self.initial_pt_thk_status == True and self.initial_pt_thk_status_web == True and self.web_plate_weld_status == True:
            self.web_weld_connecting_plates = [self.section.web_thickness, self.web_plate.thickness_provided]
            self.web_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(self.section.web_thickness,
                                                                          self.web_plate.thickness_provided)
            self.web_weld_conn_plates_fu = [self.section.fu, self.web_plate.fu]
            self.gamma_mw_web = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.web_weld.fabrication]
            t1 = ('SubSection', 'Web Weld Design ', '|p{3cm}|p{6.5cm}|p{4.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t2 = (DISP_MIN_WEB_PLATE_THICK, display_prov(self.section.web_thickness / 2, "t"),
                  display_prov(self.web_plate.thickness_provided, "t_{wp}"),
                  get_pass_fail(self.section.web_thickness / 2, self.web_plate.thickness_provided, relation="lesser"))
            self.report_check.append(t2)
            t2 = (DISP_MIN_WELD_SIZE, cl_10_5_2_3_min_fillet_weld_size_required(conn_plates_weld=self.web_weld_connecting_plates,
                                                                                min_weld_size=self.web_weld_size_min),
                  display_prov(self.web_weld.size, "t_w"),
                  get_pass_fail(self.web_weld_size_min, self.web_weld.size, relation="leq"))
            self.report_check.append(t2)
            t2 = (DISP_MAX_WELD_SIZE, cl_10_5_3_1_max_weld_size(conn_plates_weld=self.web_weld_connecting_plates,
                                                                max_weld_size=self.min_web_platethk),
                  display_prov(self.web_weld.size, "t_w"),
                  get_pass_fail(self.min_web_platethk, self.web_weld.size, relation="geq"))
            self.report_check.append(t2)
            t1 = (DISP_EFF, "",
                  eff_len_prov(l_w=self.web_weld.length, b_fp=self.web_plate.height, t_w=self.web_weld.size,
                               l_eff=self.l_req_weblength, con="web"), "")
            self.report_check.append(t1)
            t2 = (KEY_DISP_CLEARANCE, spacing(sp=self.webspace, t_w=self.web_weld.size),
                  display_prov(self.webspace, "sp"),
                  get_pass_fail(self.min_web_platethk, self.web_weld.size, relation="geq"))
            self.report_check.append(t2)
            t1 = (DISP_THROAT, cl_10_5_3_1_throat_thickness_req(), cl_10_5_3_1_throat_thickness_weld(self.web_weld.size, self.Kt),
                  get_pass_fail(3.0, self.web_weld.size, relation="leq"))
            self.report_check.append(t1)
            t10 = (KEY_OUT_REQ_MOMENT_DEMAND_BOLT, '',
                   moment_demand_req_bolt_force(shear_load=round((self.fact_shear_load / 1000) / 2, 2),
                                                web_moment=round((self.moment_web / 1000000) / 2, 2),
                                                ecc=round(self.ecc, 2),
                                                moment_demand=round(self.weld_twist / 1000000, 2)), '')
            self.report_check.append(t10)

            t2 = (KEY_WEB_DISP_WELD_STRENGTH, weld_strength_stress(V_u=round((self.fact_shear_load / 2), 2),
                                                                   A_w=round((self.axial_force_w / 2), 2),
                                                                   M_d=round(self.weld_twist, 2),
                                                                   Ip_w=round(self.Ip_weld, 2),
                                                                   y_max=round(self.y_max, 2),
                                                                   x_max=round(self.x_max, 2),
                                                                   l_eff=self.l_req_weblength,
                                                                   R_w=web_weld_stress_kn),
                  cl_10_5_7_1_1_weld_strength(conn_plates_weld_fu=self.web_weld_conn_plates_fu, gamma_mw=self.gamma_mw_web,
                                              t_t=self.web_weld.throat_tk, f_w=web_weld_strength_kn),
                  get_pass_fail(web_weld_stress_kn, web_weld_strength_kn, relation="lesser"))
            self.report_check.append(t2)

            t15 = (KEY_OUT_LONG_JOINT_WELD, long_joint_welded_req(),
                   long_joint_welded_beam_prov(plate_height=self.web_plate.height,
                                               l_w=self.available_long_web_length, t_w=self.web_weld.size,
                                               gap=self.flange_plate.gap, t_t=self.web_weld.throat_tk,
                                               Tc=web_weld_strength_kn, Tr=web_weld_strength_red_kn), "")
            self.report_check.append(t15)
            t5 = (KEY_OUT_DISP_RED_WELD_STRENGTH, web_weld_stress_kn, web_weld_strength_red_kn,
                get_pass_fail(web_weld_stress_kn, web_weld_strength_red_kn,
                              relation="lesser"))
            self.report_check.append(t5)

            t1 = ('SubSection', 'Web Plate Dimension Check', '|p{3cm}|p{4.5cm}|p{6.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            self.min_web_plate_height = round(self.section.min_plate_height(), 2)
            self.min_length_required_web = self.section.flange_width
            t1 = (DISP_MIN_WEB_PLATE_HEIGHT, min_plate_ht_req(D=self.section.depth, min_req_width=self.min_web_plate_height, r_r=self.section.root_radius,
                                                              t_f=self.section.flange_thickness)
            , height_of_web_cover_plate(D=self.section.depth, sp=self.webspace, b_wp=self.web_plate.height,
                                        T=self.section.flange_thickness, R_1=self.section.root_radius),
                  get_pass_fail(self.min_height_required, self.web_plate.height, relation="lesser"))
            self.report_check.append(t1)
            t1 = (DISP_MIN_WEB_PLATE_LENGTH, self.min_length_required_web, plate_Length_req(l_w=self.web_weld.length,
                                                                                        t_w=self.web_weld.size,
                                                                                        g=self.web_plate.gap,
                                                                                        l_fp=self.web_plate.length,
                                                                                        conn="web"),
                  get_pass_fail(self.min_length_required_web, self.web_plate.length, relation="lesser"))
            self.report_check.append(t1)
            t2 = (DISP_MIN_WEB_PLATE_THICK, display_prov(self.section.web_thickness / 2, "t"),
                  display_prov(self.web_plate.thickness_provided, "t_{wp}"),
                  get_pass_fail(self.section.web_thickness / 2, self.web_plate.thickness_provided, relation="lesser"))
            self.report_check.append(t2)
            self.Recheck_web_pt_area_o = (2 * self.web_plate.height) * \
                                         self.web_plate.thickness_provided
            t2 = (KEY_DISP_AREA_CHECK, plate_area_req(round(self.web_crs_area, 2),
                                                      flange_web_area=round(self.Wp, 2)),
                  plate_recheck_area_weld(outerwidth=self.web_plate.height, innerwidth=None,
                                          f_tp=None, t_wp=self.web_plate.thickness_provided, conn="web",
                                          pref=None),
                  get_pass_fail(self.Wp, self.Recheck_web_pt_area_o, relation="leq"))
            self.report_check.append(t2)

        ####################################### Member Capacities##############################################################
        ###################
        ### Flange Check ###
        if self.flange_plate_weld_status == True and self.flange_plate_capacity_axial_status == True:
            t1 = ('SubSection', 'Member Check', '|p{3cm}|p{4cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)
            gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

            t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE, '', cl_6_2_tension_yield_capacity_member(self.section.flange_width,
                                                                                               self.section.flange_thickness,
                                                                                               self.section.fy, gamma_m0,
                                                                                               round(
                                                                                 self.section.tension_yielding_capacity / 1000,
                                                                                 2), 1), '')
            self.report_check.append(t1)
            gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

            # t1 = (KEY_DISP_TENSIONRUPTURECAP_FLANGE, '', tension_rupture_welded_prov(w_p=self.section.flange_width,
            #                                                                          t_p=self.section.flange_thickness,
            #                                                                          fu=self.section.fu,
            #                                                                          gamma_m1=gamma_m1, T_dn=round(
            #         (self.section.tension_rupture_capacity / 1000), 2), multiple=1), '')
            #
            # self.report_check.append(t1)
            t1 = (KEY_DISP_FLANGE_TEN_CAPACITY, display_prov(round(self.flange_force / 1000, 2), "F_f"),
                  cl_6_1_tension_capacity_member(round(self.section.tension_yielding_capacity / 1000, 2),
                                                 0),
                  get_pass_fail(round(self.flange_force / 1000, 2),
                                round(self.section.tension_capacity_flange / 1000, 2), relation="lesser"))
            self.report_check.append(t1)

        ### web Check ###
        if self.web_plate_capacity_axial_status == True and self.web_plate_capacity_shear_status == True:
            gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
            # A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
            webheight = round((self.section.depth - 2 * self.section.flange_thickness), 2)
            t1 = (KEY_DISP_TENSIONYIELDINGCAP_WEB, '', cl_6_2_tension_yield_capacity_member(webheight,
                                                                                            self.section.web_thickness,
                                                                                            self.section.fy, gamma_m0,
                                                                                            round(
                                                                              self.section.tension_yielding_capacity_web / 1000,
                                                                              2), 1), '')
            self.report_check.append(t1)
            gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
            # t1 = (KEY_DISP_TENSIONRUPTURECAP_WEB, '', tension_rupture_welded_prov(w_p=webheight,
            #                                                                       t_p=self.section.web_thickness,
            #                                                                       fu=self.section.fu,
            #                                                                       gamma_m1=gamma_m1,
            #                                                                       T_dn=round(
            #                                                                           self.section.tension_rupture_capacity_web / 1000,
            #                                                                           2), multiple=1), '')
            # self.report_check.append(t1)
            t1 = (KEY_DISP_BLOCKSHEARCAP_WEB, '',
                  cl_6_4_blockshear_capacity_member(Tdb=round(self.section.block_shear_capacity_web / 1000, 2)), '')
            self.report_check.append(t1)
            t1 = (KEY_DISP_WEB_TEN_CAPACITY, display_prov(round(self.axial_force_w / 1000, 2), "A_w"),
                  cl_6_1_tension_capacity_member(round(self.section.tension_yielding_capacity_web / 1000, 2),
                                                 0,
                                                 round(self.section.block_shear_capacity_web / 1000, 2)),
                  get_pass_fail(round(self.axial_force_w / 1000, 2),
                                round(self.section.tension_capacity_web / 1000, 2), relation="lesser"))
            self.report_check.append(t1)

        ####################### Flange plate Capacities check########################
        ###################
        # if self.flange_plate_capacity_axial == True:
        if self.flange_plate_weld_status == True:
            if self.preference == "Outside":
                t1 = ('SubSection', 'Flange Plate Capacity Check for Axial Load - Outside', '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
                self.report_check.append(t1)
                gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

                t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE_PLATE, '', cl_6_2_tension_yield_capacity_member(self.flange_plate.height,
                                                                                                         self.flange_plate.thickness_provided,
                                                                                                         self.flange_plate.fy,
                                                                                                         gamma_m0,
                                                                                                         round(
                                                                                           self.flange_plate.tension_yielding_capacity / 1000,
                                                                                           2), 1), '')
                self.report_check.append(t1)
                gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

                # t1 = (KEY_DISP_TENSIONRUPTURECAP_FLANGE_PLATE, '',
                #       tension_rupture_welded_prov(w_p=self.flange_plate.height,
                #                                   t_p=self.flange_plate.thickness_provided,
                #                                   fu=self.flange_plate.fu,
                #                                   gamma_m1=gamma_m1,
                #                                   T_dn=round(self.flange_plate.tension_rupture_capacity / 1000,
                #                                              2), multiple=1), '')
                # self.report_check.append(t1)
                t1 = (KEY_DISP_FLANGE_PLATE_TEN_CAP, display_prov(round(self.flange_force / 1000, 2), "F_f"),
                      cl_6_1_tension_capacity_member(round(self.flange_plate.tension_yielding_capacity / 1000, 2),
                                                     0),
                      get_pass_fail(round(self.flange_force / 1000, 2),
                                    round(self.flange_plate.tension_capacity_flange_plate / 1000, 2),
                                    relation="lesser"))
                self.report_check.append(t1)
            else:
                t1 = ('SubSection', 'Flange Plate Capacity Check for Axial Load - Outside/Inside ',
                      '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
                self.report_check.append(t1)

                gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
                total_height = self.flange_plate.height + (2 * self.flange_plate.Innerheight)

                t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE_PLATE, '', cl_6_2_tension_yield_capacity_member(total_height,
                                                                                                         self.flange_plate.thickness_provided,
                                                                                                         self.flange_plate.fy,
                                                                                                         gamma_m0,
                                                                                                         round(
                                                                                           self.flange_plate.tension_yielding_capacity / 1000,
                                                                                           2), 1), '')
                self.report_check.append(t1)

                gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
                #
                # t1 = (KEY_DISP_TENSIONRUPTURECAP_FLANGE_PLATE, '', tension_rupture_welded_prov(w_p=total_height,
                #                                                                                t_p=self.flange_plate.thickness_provided,
                #                                                                                fu=self.flange_plate.fu,
                #                                                                                gamma_m1=gamma_m1,
                #                                                                                T_dn=round(
                #                                                                                    self.flange_plate.tension_rupture_capacity / 1000,
                #                                                                                    2), multiple=1),
                #       '')
                # self.report_check.append(t1)

                t1 = (KEY_DISP_FLANGE_PLATE_TEN_CAP, display_prov(round(self.flange_force / 1000, 2), "F_f"),
                      cl_6_1_tension_capacity_member(round(self.flange_plate.tension_yielding_capacity / 1000, 2),
                                                     0),
                      get_pass_fail(round(self.flange_force / 1000, 2),
                                    round(self.flange_plate.tension_capacity_flange_plate / 1000, 2),
                                    relation="lesser"))
                self.report_check.append(t1)

        # Web plate Capacities check axial
        ###################
        if self.recheck_flange_capacity_axial_status == True:
            t1 = ('SubSection', 'Web Plate Capacity Check for Axial Load', '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)
            gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
            t1 = (KEY_DISP_TENSION_YIELDCAPACITY_WEB_PLATE, '', cl_6_2_tension_yield_capacity_member(self.web_plate.height,
                                                                                                     self.web_plate.thickness_provided,
                                                                                                     self.web_plate.fy,
                                                                                                     gamma_m0,
                                                                                                     round(
                                                                                       self.web_plate.tension_yielding_capacity / 1000,
                                                                                       2), 2), '')
            self.report_check.append(t1)
            gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
            # t1 = (KEY_DISP_TENSION_RUPTURECAPACITY_WEB_PLATE, '', tension_rupture_welded_prov(self.web_plate.height,
            #                                                                                   self.web_plate.thickness_provided,
            #                                                                                   self.web_plate.fu,
            #                                                                                   gamma_m1,
            #                                                                                   round(
            #                                                                                       self.web_plate.tension_rupture_capacity / 1000,
            #                                                                                       2), 2), '')
            # self.report_check.append(t1)
            t1 = (KEY_DISP_WEB_PLATE_CAPACITY, display_prov(round(self.axial_force_w / 1000, 2), "A_w"),
                  cl_6_1_tension_capacity_member(round(self.web_plate.tension_yielding_capacity / 1000, 2),
                                                 0),
                  get_pass_fail(round(self.axial_force_w / 1000, 2),
                                round(self.web_plate.tension_capacity_web_plate / 1000, 2), relation="lesser"))
            self.report_check.append(t1)

        # Web plate Capacities check Shear
        ###################
        if self.web_plate_capacity_axial_status == True:
            t1 = ('SubSection', 'Web Plate Capacity Check for Shear Load', '|p{4cm}|p{3cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t1 = (KEY_DISP_SHEARYIELDINGCAP_WEB_PLATE, '',
                  cl_8_4_shear_yielding_capacity_member(self.web_plate.height, self.web_plate.thickness_provided,
                                                        self.web_plate.fy, gamma_m0,
                                                        round(self.web_plate.shear_yielding_capacity / 1000 / 0.6, 2), 2), '')
            self.report_check.append(t1)

            initial_shear_capacity = round(self.web_plate.shear_yielding_capacity / 1000 / 0.6, 2)
            reduced_shear_capacity = round(self.web_plate.shear_yielding_capacity / 1000, 2)
            t1 = (KEY_DISP_ALLOW_SHEAR, display_prov(self.load.shear_force, "V"),
                  allow_shear_capacity(initial_shear_capacity, reduced_shear_capacity),
                  get_pass_fail(self.load.shear_force, reduced_shear_capacity, relation="lesser"))
            self.report_check.append(t1)
            # if self.shear_yielding_status == True:
            #     t1 = (KEY_DISP_SHEAR_RUP, '',
            #           shear_Rupture_prov_weld(self.web_plate.height, self.web_plate.thickness_provided,
            #                                   self.web_plate.fu,
            #                                   round(self.web_plate.shear_rupture_capacity / 1000, 2), gamma_m1, 2), '')
            #     self.report_check.append(t1)
            t1 = (KEY_DISP_WEBPLATE_SHEAR_CAPACITY_PLATE, display_prov(round(self.fact_shear_load / 1000, 2), "V_u"),
                  cl_8_4_shear_capacity_member(V_dy=round(self.web_plate.shear_yielding_capacity / 1000, 2),
                                               V_dn=00,
                                               V_db=00),
                  get_pass_fail(round(self.fact_shear_load / 1000, 2),
                                round(self.web_plate.shear_capacity_web_plate / 1000, 2), relation="lesser"))
            self.report_check.append(t1)

        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_2d_image, Disp_3D_image, module=self.module)
