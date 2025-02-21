"""
Module: lap_joint_bolted.py
Author: Aman
Date: 2025-02-18

Description:
    LapJointBolted is a moment connection module that represents a bolted lap joint connection.
    It inherits from MomentConnection and follows the same structure and design logic as other
    connection modules (e.g., BeamCoverPlate, ColumnCoverPlate) used in Osdag.
    
Reference:
    - Osdag software guidelines and connection module structure documentation
"""

from .moment_connection import MomentConnection
from ...utils.common.component import *
from ...utils.common.is800_2007 import *
from ...Common import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...Report_functions import *
from ...utils.common.load import Load
import logging

import math

class LapJointBolted(MomentConnection):
    def __init__(self):
        super(LapJointBolted, self).__init__()
        self.design_status = False

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

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_supporting_section)
        tabs.append(t1)

        # t1 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_supported_section)
        # tabs.append(t1)

        # t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        # tabs.append(t6)

        t2 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t2)

        # t2 = ("Weld", TYPE_TAB_2, self.weld_values)
        # tabs.append(t2)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

        # t5 = ("Design", TYPE_TAB_2, self.design_values)
        # tabs.append(t5)

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

        t1 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC_MATERIAL], [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY], TYPE_TEXTBOX,
        self.get_fu_fy_I_section_suptng)
        change_tab.append(t1)

        # t2 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC_MATERIAL], [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY], TYPE_TEXTBOX,
        # self.get_fu_fy_I_section_suptd)
        # change_tab.append(t2)

        # t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
        #                                               KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)

        # change_tab.append(t3)


        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20','Label_21','Label_22',KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        # t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4','Label_5'],
        #       ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
        #        'Label_19', 'Label_20','Label_21','Label_22',KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        # change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        # t7 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        # change_tab.append(t7)

        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
                Not required for this module but empty list should be passed"""
        return []

    # def list_for_fu_fy_validation(self):
    #     """ This function is no longer required"""
    #
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

        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SUPTNGSEC_MATERIAL])
        design_input.append(t1)

        # t2 = (KEY_DISP_BEAMSEC, TYPE_COMBOBOX, [KEY_SUPTDSEC_MATERIAL])
        # design_input.append(t2)



        t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        design_input.append(t3)

        # t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        # design_input.append(t4)

        # t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        # design_input.append(t4)

        t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        design_input.append(t5)

        t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        design_input.append(t5)

        # t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        # design_input.append(t6)

        # t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        # design_input.append(t7)

        return design_input


    def input_dictionary_without_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to
        design dictionary if design preference is never opened by user. It sets are design preference values to default.
        If any design preference value needs to be set to input dock value, tuple shall be written as:

        (Key of input dock, [List of Keys from design prefernce], 'Input Dock')

        If the values needs to be set to default,

        (None, [List of Design Prefernce Keys], '')

         """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SUPTNGSEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_GAP,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES], '')
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

        # if design_dictionary[KEY_MATERIAL] != 'Select Material':
        #     fu = Material(design_dictionary[KEY_MATERIAL],41).fu
        # else:
        #     fu = ''

        val = {KEY_DP_BOLT_TYPE: "Pretensioned",
               KEY_DP_BOLT_HOLE_TYPE: "Standard",
               KEY_DP_BOLT_SLIP_FACTOR: str(0.3),
            #    KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP,
               KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
               KEY_DP_DETAILING_GAP: '3',
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No',
            #    KEY_DP_DESIGN_METHOD: "Limit State Design",
            #    KEY_CONNECTOR_MATERIAL: str(design_dictionary[KEY_MATERIAL])
               }[key]

        return val
    
    

    def out_bolt_bearing(self):

        bolt_type = self[0]
        if bolt_type != TYP_BEARING:
            return True
        else:
            return False

    def preference_type(self):

        pref_type = self[0]
        if pref_type == VALUES_FLANGEPLATE_PREFERENCES[0]:
            return True
        else:
            return False
    ####################################
    # Design Preference Functions End
    ####################################

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


    def input_value_changed(self):

        lst = []

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        return lst


    def input_values(self):

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_LAPJOINTBOLTED, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t31 = (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_FLANGEPLATE_THICKNESS, True, 'Float Validator')
        options_list.append(t31)

        t34 = (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_FLANGEPLATE_THICKNESS, True, 'Float Validator')
        options_list.append(t34)

        t35 = (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None, True, 'Float Validator')
        options_list.append(t35)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_TENSILE_FORCE, KEY_DISP_TENSILE_FORCE, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        return options_list

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        t5 = (KEY_PLATE1_THICKNESS, self.plate_thick_customized)
        list1.append(t5)
        t6 = (KEY_PLATE2_THICKNESS, self.plate_thick_customized)
        list1.append(t6)
        
        return list1

    def output_values(self, flag):

        out_list = []
        t4 = (None, DISP_TITLE_BOLTD, TYPE_TITLE, None, True)
        out_list.append(t4)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,
              '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX,
              '', True)
        out_list.append(t3)

        t31 = (KEY_OUT_TYP_PROVIDED, KEY_OUT_DISP_TYP_PROVIDED, TYPE_TEXTBOX,
              '', True)
        out_list.append(t31)

        t8 = (KEY_OUT_BOLT_SHEAR,KEY_OUT_DISP_BOLT_SHEAR , TYPE_TEXTBOX, '', True)
        out_list.append(t8)

        t4 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
              '', True)
        out_list.append(t5)

        t17 = (None, DISP_TITLE_BOLTDS, TYPE_TITLE, None, True)
        out_list.append(t17)
        t17 = (KEY_OUT_TOT_NO_BOLTS, KEY_OUT_DISP_TOT_NO_BOLTS, TYPE_TEXTBOX, '', True)
        out_list.append(t17)
        t18 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX,'', True)
        out_list.append(t18)

        t19 = (KEY_OUT_COL_PROVIDED, KEY_OUT_DISP_COL_PROVIDED, TYPE_TEXTBOX,'', True)
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_LENGTH, TYPE_TEXTBOX,'', True)
        out_list.append(t20)

        return out_list

    def module_name(self):

        return KEY_DISP_LAPJOINTBOLTED

    def call_3DColumn(self, ui, bgcolor):
        # status = self.resultObj['Bolt']['status']
        # if status is True:
        #     self.ui.chkBx_beamSec1.setChecked(Qt.Checked)
        if ui.chkBxCol.isChecked():
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
        # self.display_3DModel("Beam", bgcolor)
        ui.commLogicObj.display_3DModel("Column", bgcolor)

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

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


    ################################ Outlist Dict #####################################################################################

    

    ################################ Design Report #####################################################################################

