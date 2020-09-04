"""
@Author:    Danish Ansari - Osdag Team, IIT Bombay [(P) danishdyp@gmail.com / danishansari@iitb.ac.in]

@Module - Beam-Beam End Plate Splice Connection
           - Flushed End Plate
           - Extended One Way End Plate
           - Extended Both Way End Plate


@Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) IS 2062: 2011, Hot rolled medium and high tensile structural steel - specification
               4) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               5) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

     other     6)
  references   7)

 Note: This file works with the helper file named 'end_plate_splice_helper.py' at ../Osdag/design_type/connection
"""

# Importing modules from the project directory

from design_type.connection.moment_connection import MomentConnection
from design_type.connection.end_plate_splice_helper import EndPlateSpliceHelper
from design_type.connection import end_plate_splice_helper
from design_type.connection.shear_connection import ShearConnection
from utils.common.is800_2007 import IS800_2007
from utils.common.other_standards import IS_5624_1993
from utils.common.component import *
from utils.common.material import *
from utils.common.common_calculation import *
from Common import *
from utils.common.load import Load
from utils.common.other_standards import *
from design_report.reportGenerator import save_html
from Report_functions import *
from design_report.reportGenerator_latex import CreateLatex

import logging
import math
import numpy as np


class BeamBeamEndPlateSplice(MomentConnection):

    def __init__(self):
        super(BeamBeamEndPlateSplice, self).__init__()

        self.load_moment = 0.0
        self.load_moment_effective = 0.0
        self.load_shear = 0.0
        self.load_axial = 0.0

        # self.supported_section = Beam
        self.bolt_diameter = []
        self.bolt_list = []
        self.bolt_diameter_provided = 0
        self.bolt_grade = []
        self.bolt_grade_provided = 0.0
        self.bolt_type = ""
        self.plate_thickness = []

        self.beam_shear_capa = 0.0
        self.beam_plastic_mom_capa_zz = 0.0
        self.tension_due_to_moment = 0.0
        self.tension_due_to_axial_force = 0.0
        self.load_tension_flange = 0.0
        self.bolt_tension = 0.0
        self.bolt_fu = 0.0
        self.dp_bolt_fy = 0.0
        self.proof_load = 0.0
        self.proof_stress = 0.0
        self.beta = 0

        self.pitch_distance_provided = 0.0
        self.gauge_distance_provided = self.pitch_distance_provided
        self.end_distance_provided = 0.0
        self.edge_distance_provided = self.end_distance_provided
        self.gauge_cs_distance_provided = 0.0
        self.space_available_inside_D = 0.0
        self.rows_inside_D_max = 0
        self.rows_outside_D_max = 0
        self.rows_total_max = 0
        self.rows_minimum_req = 0
        self.rows_outside_D_provided = 0
        self.rows_inside_D_provided = 0
        self.rows_near_tension_flange = (self.rows_outside_D_provided / 2) + (self.rows_inside_D_provided / 2)
        self.rows_near_web = 0
        self.rows_near_tension_flange_max = 0
        self.rows_near_web_max = 0
        self.bolt_numbers_tension_flange = 0
        self.bolt_numbers_web = 0
        self.mid_bolt_row =0
        self.bolt_column = 0
        self.bolt_row = 0
        self.bolt_numbers = 0

        self.ep_width_provided = 0.0
        self.ep_height_provided = 0.0
        self.ep_moment_capacity = 0.0
        self.ep_height_max = 0.0

        self.beam_D = 0.0
        self.beam_bf = 0.0
        self.beam_tf = 0.0
        self.beam_tw = 0.0
        self.beam_r1 = 0.0
        self.beam_r2 = 0.0
        self.beam_zp_zz = 0.0
        self.dp_beam_fu = 0.0
        self.dp_beam_fy = 0.0
        self.dp_plate_fy = 0.0
        self.dp_plate_fu = 0.0

        self.minimum_load_status_shear = False
        self.minimum_load_status_moment = False
        self.plate_design_status = False
        self.helper_file_design_status = False
        self.deep_beam_status = False
        self.design_status = False

        self.beam_properties = {}
        self.safety_factors = {}
        self.gamma_m0 = 0.0
        self.gamma_m1 = 0.0
        self.gamma_mb = 0.0
        self.gamma_mw = 0.0

        self.bolt_shear_demand = 0.0
        self.bolt_shear_capacity = 0.0
        self.bolt_bearing_capacity = 0.0
        self.bolt_capacity = 0.0
        self.tension_critical_bolt = 0.0
        self.prying_critical_bolt = 0.0
        self.tension_demand_critical_bolt = 0.0
        self.tension_capacity_critical_bolt = 0.0
        self.combined_capacity_critical_bolt = 0.0
        self.stiffener_height = 0.0
        self.stiffener_length = 0.0
        self.stiffener_thickness = 0.0
        self.weld_length_web = 0.0
        self.weld_size_web = 0.0
        self.allowable_stress = 0.0
        self.f_a = 0.0
        self.q = 0.0
        self.f_e = 0.0

        # self.func_for_validation(self, design_dictionary)

    # Set logger
    def set_osdaglogger(key):
        """ Function to set Logger for the module """
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    # set module name
    def module_name(self):
        """ display module name """
        return KEY_DISP_BB_EP_SPLICE

    # create UI for Input Dock
    def input_values(self):
        """ create a list of tuples to be displayed as the UI in Input Dock """
        self.module = KEY_DISP_BB_EP_SPLICE

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_BB_EP_SPLICE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, VALUES_CONN_SPLICE, True, 'No Validator', [1, 2])
        options_list.append(t2)

        t2 = (KEY_ENDPLATE_TYPE, KEY_DISP_ENDPLATE_TYPE, TYPE_COMBOBOX, VALUES_ENDPLATE_TYPE, True, 'No Validator')
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, "./ResourceFiles/images/flush_ep.png", True, 'No Validator')
        options_list.append(t15)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, connectdb("Beams"), True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t21 = (None, DISP_TITLE_ENDPLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t21)

        t22 = (KEY_PLATETHK, KEY_DISP_ENDPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_ENDPLATE_THICKNESS, True, 'No Validator')
        options_list.append(t22)

        t23 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t23)

        t24 = (KEY_WELD_TYPE, KEY_DISP_WELD_TYPE, TYPE_COMBOBOX, VALUES_WELD_TYPE_BB_FLUSH, True, 'No Validator')
        options_list.append(t24)

        return options_list

    # add representative images in UI
    def input_value_changed(self):
        """ """
        lst = []

        t1 = ([KEY_ENDPLATE_TYPE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t1)

        t2 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t2)

        return lst

    def fn_conn_image(self):
        """ display representative images of end plate type """
        # conn = self[0]
        ep_type = self[0]
        if ep_type == 'Flushed - Reversible Moment':
            return './ResourceFiles/images/flush_ep.png'
        elif ep_type == 'Extended One Way - Irreversible Moment':
            return './ResourceFiles/images/owe_ep.png'
        elif ep_type == 'Extended Both Ways - Reversible Moment':
            return './ResourceFiles/images/extended.png'
        else:
            return ''

    # create customized input for UI
    def customized_input(self):
        """ list of values available with customize option"""

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)

        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)

        t6 = (KEY_PLATETHK, self.endplate_thick_customized)
        list1.append(t6)
        return list1

    # create UI for Output Dock
    def output_values(self, flag):
        """ create a list of tuples to be displayed as the UI in the Output Dock """
        out_list = []

        # Critical Bolt
        t1 = (None, DISP_TITLE_CRITICAL_BOLT, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, int(self.bolt_diameter_provided) if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_PC_PROVIDED, TYPE_TEXTBOX, self.bolt_grade_provided if flag else '', True)
        out_list.append(t3)

        t12 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_DEMAND, TYPE_TEXTBOX, self.bolt_shear_demand if flag else '', True)
        out_list.append(t12)

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX, self.bolt_shear_capacity if flag else '', True)
        out_list.append(t4)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE: bolt_bearing_capacity_disp = self.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, DISP_TITLE_BOLT_CAPACITY, TYPE_TEXTBOX, self.bolt_capacity if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_OUT_BOLT_TENSION_FORCE, KEY_OUT_DISP_CRITICAL_BOLT_TENSION, TYPE_TEXTBOX, self.tension_critical_bolt if flag else '', True)
        out_list.append(t7)

        t8 = (KEY_OUT_BOLT_PRYING_FORCE, KEY_OUT_DISP_BOLT_PRYING_FORCE_EP, TYPE_TEXTBOX, self.prying_critical_bolt if flag else '', True)
        out_list.append(t8)

        t9 = (KEY_OUT_BOLT_TENSION_TOTAL, KEY_OUT_DISP_BOLT_TENSION_DEMAND, TYPE_TEXTBOX, self.tension_demand_critical_bolt if flag else '', True)
        out_list.append(t9)

        t10 = (KEY_OUT_BOLT_TENSION_CAPACITY, KEY_OUT_CRITICAL_BOLT_TENSION_CAPACITY, TYPE_TEXTBOX, self.tension_capacity_critical_bolt if flag else '', True)
        out_list.append(t10)

        t11 = (KEY_OUT_BOLT_IR, KEY_OUT_DISP_BOLT_COMBINED_CAPACITY, TYPE_TEXTBOX, self.combined_capacity_critical_bolt if flag else '', True)
        out_list.append(t11)

        # Detailing
        t12 = (None, DISP_TITLE_DETAILING, TYPE_TITLE, None, True)
        out_list.append(t12)

        t13 = (KEY_OUT_DISP_DETAILING_BOLT_NUMBERS, KEY_OUT_DISP_DETAILING_BOLT_NUMBERS_EP, TYPE_TEXTBOX, self.bolt_numbers if flag else '', True)
        out_list.append(t13)

        t14 = (KEY_OUT_DISP_DETAILING_BOLT_COLUMNS, KEY_OUT_DISP_DETAILING_BOLT_COLUMNS_EP, TYPE_TEXTBOX, self.bolt_column if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_DISP_DETAILING_BOLT_ROWS, KEY_OUT_DISP_DETAILING_BOLT_ROWS_EP, TYPE_TEXTBOX, self.bolt_row if flag else '', True)
        out_list.append(t15)

        t21 = (KEY_OUT_DETAILING_PITCH_DISTANCE, KEY_OUT_DISP_DETAILING_PITCH_DISTANCE, TYPE_TEXTBOX, self.pitch_distance_provided if flag else '', True)
        out_list.append(t21)

        t22 = (KEY_OUT_DETAILING_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX, self.gauge_distance_provided if flag else '', True)
        out_list.append(t22)

        t22 = (KEY_OUT_DETAILING_CS_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_CS_GAUGE_DISTANCE, TYPE_TEXTBOX, self.gauge_cs_distance_provided if flag else '', True)
        out_list.append(t22)

        t16 = (KEY_OUT_DETAILING_END_DISTANCE, KEY_OUT_DISP_DETAILING_END_DISTANCE, TYPE_TEXTBOX, self.end_distance_provided if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_DETAILING_EDGE_DISTANCE, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.edge_distance_provided if flag else '', True)
        out_list.append(t17)

        # End Plate
        t18 = (None, DISP_TITLE_ENDPLATE, TYPE_TITLE, None, True)
        out_list.append(t18)

        t19 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, int(self.plate_thickness) if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.ep_height_provided if flag else '', True)
        out_list.append(t20)

        t21 = (KEY_OUT_PLATE_WIDTH, KEY_OUT_DISP_PLATE_WIDTH, TYPE_TEXTBOX, self.ep_width_provided if flag else '', True)
        out_list.append(t21)

        t22 = (KEY_OUT_EP_MOM_CAPACITY, KEY_OUT_DISP_EP_MOM_CAPACITY, TYPE_TEXTBOX, self.ep_moment_capacity if flag else '', True)
        out_list.append(t22)

        # Stiffener Details
        t32 = (None, DISP_TITLE_STIFFENER_PLATE, TYPE_TITLE, None, True)
        out_list.append(t32)

        t33 = (KEY_OUT_STIFFENER_DETAILS, KEY_OUT_DISP_STIFFENER_DETAILS, TYPE_OUT_BUTTON, ['Stiffener Details', self.stiffener_details], True)
        out_list.append(t33)

        # Weld
        t23 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t23)

        t24 = (None, DISP_TITLE_WELD_WEB, TYPE_TITLE, None, True)
        out_list.append(t24)

        t25 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE_EP, TYPE_TEXTBOX, self.weld_size_web if flag else '', True)
        out_list.append(t25)

        t28 = (KEY_OUT_WELD_LENGTH, KEY_OUT_DISP_WELD_LENGTH, TYPE_TEXTBOX, self.weld_length_web if flag else '', True)
        out_list.append(t28)

        t27 = (KEY_OUT_WELD_STRESS, KEY_OUT_DISP_WELD_STRESS, TYPE_TEXTBOX, self.q if flag else '', True)
        out_list.append(t27)

        t29 = (KEY_OUT_WELD_STRESS_COMBINED, KEY_OUT_DISP_WELD_STRESS_COMBINED, TYPE_TEXTBOX, self.f_e if flag else '', True)
        out_list.append(t29)

        t26 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX, self.allowable_stress if flag else '', True)
        out_list.append(t26)

        t30 = (None, DISP_TITLE_WELD_FLANGE, TYPE_TITLE, None, True)
        out_list.append(t30)

        t31 = (KEY_OUT_WELD_DETAILS, DISP_TITLE_WELD_FLANGE, TYPE_OUT_BUTTON, ['Weld Details', self.weld_details], True)
        out_list.append(t31)

        return out_list

    # stiffener details
    def stiffener_details(self, flag):

        stiffener = []

        t28 = (KEY_OUT_STIFFENER_LENGTH, KEY_OUT_DISP_STIFFENER_LENGTH, TYPE_TEXTBOX, self.stiffener_length if flag else '', True)
        stiffener.append(t28)

        t29 = (KEY_OUT_STIFFENER_HEIGHT, KEY_OUT_DISP_STIFFENER_HEIGHT, TYPE_TEXTBOX, self.stiffener_height if flag else '', True)
        stiffener.append(t29)

        t30 = (KEY_OUT_STIFFENER_THICKNESS, KEY_OUT_DISP_STIFFENER_THICKNESS, TYPE_TEXTBOX, self.stiffener_thickness if flag else '', True)
        stiffener.append(t30)

        return stiffener

    # display weld details image
    def weld_details(self):

        weld = []

        t99 = (None, '', TYPE_IMAGE, './ResourceFiles/images/Butt_weld_double_bevel_flange.png')
        weld.append(t99)

        t99 = (None, '', TYPE_IMAGE, './ResourceFiles/images/Butt_weld_double_bevel_web.png')
        weld.append(t99)

        return weld

    # create UI for DP
    def tab_list(self):
        tabs = []

        t1 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_supported_section)
        tabs.append(t1)

        t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        tabs.append(t6)

        t2 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t2)

        t2 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t2)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def edit_tabs(self):
        return []

    def tab_value_changed(self):

        change_tab = []

        # t1 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC_MATERIAL], [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY], TYPE_TEXTBOX,
        # self.get_fu_fy_I_section_suptng)
        # change_tab.append(t1)

        t2 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC_MATERIAL], [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY], TYPE_TEXTBOX,
              self.get_fu_fy_I_section_suptd)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)

        change_tab.append(t3)

        # t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
        #       ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
        #        'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        # change_tab.append(t4)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        # t6 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        # change_tab.append(t6)

        t7 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

        return change_tab

    def refresh_input_dock(self):

        add_buttons = []

        # t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, None, None, "Columns")
        # add_buttons.append(t1)

        t2 = (KEY_DISP_BEAMSEC, KEY_SUPTDSEC, TYPE_COMBOBOX, KEY_SUPTDSEC, None, None, "Beams")
        add_buttons.append(t2)

        return add_buttons

    def input_dictionary_design_pref(self):
        design_input = []

        t2 = (KEY_DISP_BEAMSEC, TYPE_COMBOBOX, [KEY_SUPTDSEC_MATERIAL])
        design_input.append(t2)

        t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        design_input.append(t3)

        t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        design_input.append(t4)

        t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        design_input.append(t4)

        t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        design_input.append(t5)

        t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []

        t1 = (KEY_MATERIAL, [KEY_SUPTDSEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_WELD_FAB, KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_GAP,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            fu = Material(design_dictionary[KEY_MATERIAL], 41).fu
        else:
            fu = ''

        val = {KEY_DP_BOLT_TYPE: "Pre-tensioned",
               KEY_DP_BOLT_HOLE_TYPE: "Standard",
               KEY_DP_BOLT_SLIP_FACTOR: str(0.3),
               KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
               KEY_DP_DETAILING_GAP: '0',
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No',
               KEY_DP_DESIGN_METHOD: "Limit State Design",
               KEY_CONNECTOR_MATERIAL: str(design_dictionary[KEY_MATERIAL])
               }[key]

        return val

    # call individual 3D model in UI
    def get_3d_components(self):
        """ call individual 3D model in UI """
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        # t4 = ('End Plate', self.call_3DPlate)
        # components.append(t4)

        return components

    # get the input values from UI
    def set_input_values(self, design_dictionary):
        """ get the input values from UI (input dock and DP) for performing the design etc. """
        super(BeamBeamEndPlateSplice, self).set_input_values(self, design_dictionary)

        # section details
        self.mainmodule = "Moment Connection"
        self.module = KEY_DISP_BEAMENDPLATE
        self.connectivity = design_dictionary[KEY_CONN]
        self.endplate_type = design_dictionary[KEY_ENDPLATE_TYPE]
        self.material = Material(material_grade=design_dictionary[KEY_MATERIAL])

        # self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC],
        #                                      material_grade=design_dictionary[KEY_SUPTNGSEC_MATERIAL])
        self.supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC],
                                      material_grade=design_dictionary[KEY_SUPTDSEC_MATERIAL])

        # bolt details
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                         bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])

        # force details
        self.load = Load(shear_force=float(design_dictionary[KEY_SHEAR]),
                         axial_force=float(design_dictionary[KEY_AXIAL]),
                         moment=float(design_dictionary[KEY_MOMENT]), unit_kNm=True)

        # plate details
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],
                           gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.plate.design_status_capacity = False

        # weld details
        # self.top_flange_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
        #                             type=design_dictionary[KEY_DP_WELD_TYPE],
        #                             fabrication=design_dictionary[KEY_DP_WELD_FAB])
        # self.bottom_flange_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
        #                                type=design_dictionary[KEY_DP_WELD_TYPE],
        #                                fabrication=design_dictionary[KEY_DP_WELD_FAB])
        self.web_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                             type=design_dictionary[KEY_DP_WELD_TYPE], fabrication=design_dictionary[KEY_DP_WELD_FAB])

        # self.warn_text(self)

        # properties from design preferences

        # beam properties
        self.beam_D = self.supported_section.depth
        self.beam_bf = self.supported_section.flange_width
        self.beam_tf = self.supported_section.flange_thickness
        self.beam_tw = self.supported_section.web_thickness
        self.beam_r1 = self.supported_section.root_radius
        self.beam_r2 = self.supported_section.toe_radius
        self.beam_zp_zz = self.supported_section.plast_sec_mod_z

        self.dp_beam_fu = float(self.supported_section.fu)
        self.dp_beam_fy = float(self.supported_section.fy)

        # bolt
        # TODO: check if required
        if self.bolt.bolt_tensioning == 'Pretensioned':
            self.beta = 1
        else:
            self.beta = 2

        # weld
        self.dp_weld_fab = str(design_dictionary[KEY_DP_WELD_FAB])
        self.dp_weld_fu_overwrite = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])

        # safety factors (Table 5, IS 800:2007)
        self.gamma_m0 = self.cl_5_4_1_Table_5["gamma_m0"]["yielding"]  # gamma_mo = 1.10
        self.gamma_m1 = self.cl_5_4_1_Table_5["gamma_m1"]["ultimate_stress"]  # gamma_m1 = 1.25
        self.gamma_mb = self.cl_5_4_1_Table_5["gamma_mb"][self.dp_weld_fab]  # gamma_mb = 1.25
        self.gamma_mw = self.cl_5_4_1_Table_5["gamma_mw"]["Field weld"]  # gamma_mw = 1.25 for 'Shop Weld' and 1.50 for 'Field Weld'

        # initialize design status
        self.plate_design_status = False
        self.helper_file_design_status = False
        self.design_status = False

        # helper function

        self.call_helper = EndPlateSpliceHelper(load=self.load, bolt=self.bolt, ep_type=self.endplate_type,
                                                plate_design_status=False, helper_file_design_status=False)
        self.mid_bolt_row = 4

        self.set_parameters(self)
        self.design_connection(self)
        self.design_stiffener(self)
        self.design_weld(self)
        # self.hard_inputs(self)
        self.projection = 12.5

    # def hard_inputs(self):
    #     ################################Flush###################################
    #
    #     self.bolt_diameter_provided = 16
    #     self.bolt_grade_provided = 8.8
    #     self.plate.bolts_required = 48
    #     self.bolt_column = 4
    #     self.bolt_row = 8
    #     self.mid_bolt_row = 4
    #     self.plate.edge_dist_provided = 35
    #     self.plate.end_dist_provided = 35
    #     # self.out_bolt = 0
    #     # self.outside_pitch = 0
    #     self.plate.pitch_provided = 40
    #     self.plate.gauge_provided = 40
    #     # self.flange_weld.size = 4.0
    #     self.web_weld.size = 4.0
    #     self.plate.height = self.supported_section.depth + 25
    #     self.plate.width = self.supported_section.flange_width + 25
    #     self.plate.thickness_provided = 12.0
    #     self.projection = 12.5
        ################################Flush###################################

        ################################Oneway###################################
        # self.bolt.bolt_diameter_provided = 16
        # self.bolt.bolt_grade_provided = 8.8
        # self.plate.bolts_required =44
        # self.bolt_column = 4
        # self.bolt_row = 7
        # self.mid_bolt_row = 4
        # self.plate.edge_dist_provided = 35
        # self.plate.end_dist_provided = 35
        # # self.out_bolt = 0
        # # self.outside_pitch = 0
        # self.projection = 12.5
        # self.plate.pitch_provided = 40
        # self.plate.gauge_provided = 40
        # self.flange_weld.size = 4.0
        # self.web_weld.size = 4.0
        # if self.bolt_row <5:
        #     self.plate.height = self.supported_section.depth + self.projection+2*self.plate.end_dist_provided
        # else:
        #     self.plate.height = self.supported_section.depth + self.projection+2*self.plate.end_dist_provided + self.plate.pitch_provided
        #
        # self.plate.width = self.supported_section.flange_width + 25
        # self.plate.thickness_provided = 12.0
        # self.projection = 12.5

    ################################Oneway###################################

    ################################bothway###################################
    # self.bolt.bolt_diameter_provided = 16
    # self.bolt.bolt_grade_provided = 8.8
    # self.plate.bolts_required = 36
    # self.bolt_column = 2
    # self.bolt_row = 14
    # self.mid_bolt_row = 4
    # self.plate.edge_dist_provided = 35
    # self.plate.end_dist_provided = 35
    # # self.out_bolt = 0
    # # self.outside_pitch = 0
    # self.projection = 12.5
    # self.plate.pitch_provided = 40
    # self.plate.gauge_provided = 40
    # self.flange_weld.size = 4.0
    # self.web_weld.size = 4.0
    # if self.bolt_row <=6:
    #     self.plate.height = self.supported_section.depth + 4 * self.plate.end_dist_provided
    # else:
    #     self.plate.height = self.supported_section.depth + 4 * self.plate.end_dist_provided + 2 * self.plate.pitch_provided
    #
    # self.plate.width = self.supported_section.flange_width + 25
    # self.plate.thickness_provided = 12.0
    # self.projection = 12.5
    ################################bothway###################################

    # warn if a beam of older version of IS 808 is selected
    def warn_text(self):
        """ give logger warning when a beam from the older version of IS 808 is selected """
        global logger
        red_list = red_list_function()
        if self.supported_section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    # start of design simulation

    def set_parameters(self):
        """ set/initialize parameters for performing the analyses and design """

        # defining loads in appropriate units
        self.load.moment = round(self.load.moment * 1e-6, 2)  # kN-m
        self.load_shear = round(self.load.shear_force * 1e-3, 2)  # kN
        self.load_axial = round(self.load.axial_force * 1e-3, 2)  # kN

        # set minimum load (Cl. 10.7, IS 800:2007)

        # minimum shear load
        # Note: Shear force is assumed to be transferred through the web, hence Cl.10.7 point 2 is considered for minimum shear load
        self.beam_shear_capa = (((self.beam_D - (2 * self.beam_tf)) * self.beam_tw) * self.dp_beam_fy) / self.gamma_m0
        self.beam_shear_capa = round(self.beam_shear_capa * 1e-3, 2)  # kN

        if self.load_shear < min((0.15 * self.beam_shear_capa), 40):
            self.minimum_load_status_shear = True
            self.load_shear = min((0.15 * self.beam_shear_capa), 40)
            logger.warning("[Minimum Factored Load] The external factored shear force ({} kN) is less than the minimum recommended design action on "
                           "the member".format(self.load_shear))
            logger.info("The minimum factored shear force should be at least {} (0.15 times the shear capacity of the beam) or 40 kN whichever is "
                        "less [Ref. Cl. 10.7, IS 800:2007]".format(0.15 * self.beam_shear_capa))
            logger.info("Designing the connection for a factored shear load of {} kN-m".format(self.load_shear))

        # minimum moment (major axis)
        # moment capacity of beam (cl 8.2.1.2, IS 800:2007)
        self.beam_plastic_mom_capa_zz = round(((1 * self.supported_section.plast_sec_mod_z * self.supported_section.fy) / self.gamma_m0) * 1e-6, 2)  # kN-m

        if self.load.moment < (0.5 * self.beam_plastic_mom_capa_zz):
            self.minimum_load_status_moment = True
            # update moment value
            self.load_moment = round(0.5 * self.beam_plastic_mom_capa_zz, 2)  # kN

            logger.warning("[Minimum Factored Load] The external factored bending moment ({} kN-m) is less than 0.5 times the plastic moment "
                           "capacity of the beam ({} kN-m)".format(self.load.moment, self.load_moment))
            logger.info("The minimum factored bending moment should be at least 0.5 times the plastic moment capacity of the beam to qualify the "
                        "connection as rigid and transfer full moment from the spliced beam (Cl. 10.7, IS 800:2007)")
            logger.info("Designing the connection for a load of {} kN-m".format(self.load_moment))

        elif self.load.moment > self.beam_plastic_mom_capa_zz:
            self.load_moment = self.beam_plastic_mom_capa_zz  # kN
            self.minimum_load_status_moment = True
            self.design_status = False
            logger.error("[Maximum Factored Load] The external factored bending moment ({} kN-m) is greater than the plastic moment capacity of the "
                         "beam ({} kN-m)".format(self.load.moment, self.beam_plastic_mom_capa_zz))
            logger.warning("The maximum capacity of the connection is {} kN-m".format(self.beam_plastic_mom_capa_zz))
            logger.info("Define the value of factored bending moment as {} kN-m or less".format(self.beam_plastic_mom_capa_zz))
        else:
            self.design_status = True
            self.minimum_load_status_moment = False
            self.load_moment = self.load.moment  # kN-m

        # effective moment is the moment due to external factored moment plus moment due to axial force
        self.load_moment_effective = round(self.load_moment + (self.load_axial * ((self.beam_D / 2) - (self.beam_tf / 2))) * 1e-3, 2)  # kN-m

        # setting bolt ist
        self.bolt_diameter = self.bolt.bolt_diameter
        self.bolt_grade = self.bolt.bolt_grade
        self.bolt_type = self.bolt.bolt_type

        # set plate thickness list [minimum to maximum]
        # Note: minimum plate thk is at-least equal to the thk of thicker connecting element (flange thk or web thk)
        self.plate_thickness = []
        for i in self.plate.thickness:
            if i > max(self.beam_tf, self.beam_tw):
                self.plate_thickness.append(i)
            else:
                logger.warning("[End Plate] The end plate of {} mm is thinner than the thickest of the elements being connected".format(i))
                logger.info("Selecting a plate of higher thickness which is at least {} mm thick".format(max(self.beam_tf, self.beam_tw)))

        # final sorted list as per compatibility check
        self.plate_thickness = self.plate_thickness  # final list of plate thicknesses considered for simulation

        # checking if the list contains at least one plate of thk higher than the minimum required
        if len(self.plate_thickness) is 0:
            self.design_status = False
            logger.error("[End Plate] The list of plate thicknesses passed into the solver is insufficient to perform end plate design")
            logger.warning("The end plate should at least be thicker than the maximum thickness of the connecting element(s)")
            logger.info("Provide a plate/list of plates with a minimum thickness of {} mm".format(max(self.beam_tf, self.beam_tw)))

        # set bolt diameter, grade combination
        self.bolt_list = []  # this list will be used to run the iteration

        # combine each diameter with each grade
        for j in self.bolt.bolt_diameter:
            for k in self.bolt.bolt_grade:
                self.bolt_list.append(j)
                self.bolt_list.append(k)

        self.bolt_list = self.bolt_list
        logger.info("[Bolt Design] Bolt diameter and grade combination ready to perform bolt design")
        logger.info("The solver has selected {} combinations of bolt diameter and grade to perform optimum bolt design in an iterative manner "
                    .format(len(self.bolt_list)))

        # create a list of tuple with a combination of each bolt diameter with each grade for iteration
        # list is created using the approach --- minimum diameter, small grade to maximum diameter, high grade
        self.bolt_list = [x for x in zip(*[iter(self.bolt_list)] * 2)]
        logger.info("Checking the design with the following bolt diameter-grade combination {}".format(self.bolt_list))

    def design_connection(self):
        """ perform analysis and design of bolt and end plate """

        # Check 1: calculate tension due to external factored moment and axial force in the tension flange
        # Assumption: the NA is assumed at the centre of the bottom flange

        self.tension_due_to_moment = round((self.load_moment * 1e3 / (self.beam_D - self.beam_tf)), 2)  # kN
        self.tension_due_to_axial_force = round(self.load_axial / 2, 2)  # kN
        self.load_tension_flange = self.tension_due_to_moment + self.tension_due_to_axial_force  # kN

        # performing the check with minimum plate thickness and a suitable bolt dia-grade combination (thin plate - large dia approach)
        logger.info("[Optimisation] Performing the design by optimising the plate thickness, using the thin plate and large (suitable) bolt diameter "
                    "approach")
        logger.info("If you wish to optimise the bolt diameter-grade combination, pass a higher value of plate thickness using the Input Dock")

        # loop starts
        self.helper_file_design_status = False  # initialise status to False to activate the loop for first (and subsequent, if required) iteration(s)

        for i in self.plate_thickness:
            if self.helper_file_design_status is False:

                self.plate_thickness = i  # assigns plate thickness from the list

                # self.helper_file_design_status = False  # initialize helper file status as False to activate the bolt design loop

                # selecting a single dia-grade combination (from the list of a tuple) each time for performing all the checks
                for j in self.bolt_list:
                    if self.helper_file_design_status is False:

                        test_list = j  # choose a tuple from the list of bolt dia and grade - (dia, grade)
                        self.bolt_diameter_provided = test_list[0]  # select trial diameter
                        self.bolt_grade_provided = test_list[1]  # select trial grade

                        # assign bolt mechanical properties
                        bolt_fu_fy = IS1367_Part3_2002.get_bolt_fu_fy(self.bolt_grade_provided, self.bolt_diameter_provided)
                        self.bolt_fu = bolt_fu_fy[0]
                        self.dp_bolt_fy = bolt_fu_fy[1]
                        # self.proof_load = self.bolt.proof_load
                        self.proof_stress = round(0.7 * self.bolt_fu, 2)  # N/mm^2

                        # assign plate mechanical properties
                        self.plate.connect_to_database_to_get_fy_fu(grade=self.plate.material, thickness=self.plate.thickness_provided)
                        self.dp_plate_fu = self.plate.fu
                        self.dp_plate_fy = self.plate.fy

                        # Check 2: detailing checks

                        # pitch/gauge
                        self.pitch_distance_provided = self.cl_10_2_2_min_spacing(self.bolt_diameter_provided)  # mm
                        # add nut size (half on each side)
                        self.pitch_distance_provided = self.pitch_distance_provided + ((1 / 2) * IS1364Part3.nut_size(self.bolt_diameter_provided))
                        self.pitch_distance_provided = round_up(self.pitch_distance_provided, 5)
                        self.gauge_distance_provided = self.pitch_distance_provided

                        # end/edge
                        # end_distance = self.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_provided, self.bolt.bolt_hole_type, self.bolt.edge_type)
                        # end_distance = end_distance + ((1 / 2) * IS1364Part3.nut_size(self.bolt_diameter_provided))  # add nut size (half on each side)

                        self.end_distance_provided = self.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_provided, self.bolt.bolt_hole_type,
                                                                                        self.bolt.edge_type)
                        self.end_distance_provided = round_up(self.end_distance_provided, 5)  # mm
                        self.edge_distance_provided = self.end_distance_provided

                        # cross-centre gauge
                        # self.gauge_cs_distance_provided = self.beam_tw + (2 * self.beam_r1) + (2 * self.end_distance_provided)
                        self.gauge_cs_distance_provided = self.beam_tw + (2 * self.end_distance_provided)
                        self.gauge_cs_distance_provided = round_up(self.gauge_cs_distance_provided, 2)  # mm

                        # Check 3: end plate dimensions (designed for groove weld at flange only)

                        # plate width (provided and maximum are same)
                        self.ep_width_provided = self.beam_bf + 25  # mm, 12.5 mm on each side

                        # plate height (maximum) - fixing maximum two rows above and below flange for ep extending beyond the flange
                        if self.endplate_type == 'Flushed - Reversible Moment':
                            self.ep_height_max = self.beam_D + 25  # mm, 12.5 mm beyond either flanges
                        else:  # assuming two rows
                            space_available_above_flange = (2 * self.end_distance_provided) + self.pitch_distance_provided  # mm, extension on each side

                            if self.endplate_type == 'Extended One Way - Irreversible Moment':
                                self.ep_height_max = self.beam_D + space_available_above_flange  # mm
                            else:
                                self.ep_height_max = self.beam_D + (2 * space_available_above_flange)  # mm

                        # Check 4: number of rows of bolt - above and below beam depth
                        # Note: space_available_inside_D is calculated assuming minimum space available after providing minimum rows inside (i.e. 2)
                        self.space_available_inside_D = self.beam_D - (2 * self.beam_tf) - (2 * self.beam_r1) - (2 * self.end_distance_provided)
                        self.rows_inside_D_max = 2 + round_down(self.space_available_inside_D / self.pitch_distance_provided, 1)

                        if self.endplate_type == 'Extended One Way - Irreversible Moment':
                            self.rows_outside_D_max = 2
                            self.rows_total_max = self.rows_outside_D_max + self.rows_inside_D_max

                            self.rows_minimum_req = 3  # 2 near tension flange and 1 near the bottom flange
                        else:
                            if self.endplate_type == 'Flushed - Reversible Moment':
                                self.rows_outside_D_max = 0
                                self.rows_minimum_req = 2  # 2 at each flanges (inside flanges)

                            else:  # extended both way
                                self.rows_outside_D_max = 2 * 2  # 2 on outside of both the flanges
                                self.rows_minimum_req = 2 * 2  # 2 at each flanges (above and below)

                            self.rows_total_max = self.rows_outside_D_max + self.rows_inside_D_max

                        if self.rows_inside_D_max <= 0:
                            logger.error("[Detailing] The selected beam cannot accommodate at-least a single row of bolt inside it's depth")
                            logger.info("Select/Provide a beam of suitable depth")

                        # Check 5: number of columns of bolt on each side (minimum is 1, maximum is 2)

                        # checking space available to accommodate two column of bolts on each side
                        space_req_2col = self.gauge_cs_distance_provided + (2 * self.gauge_distance_provided) + (2 * self.edge_distance_provided)

                        if self.ep_width_provided >= space_req_2col:
                            self.bolt_column = 4  # two columns on each side
                            logger.info("The provided beam can accommodate two column of bolts on either side of the web [Ref. based on detailing "
                                        "requirement]")
                            logger.info("Performing the design with two column of bolts on each side")
                        else:
                            self.bolt_column = 2  # one column on each side
                            logger.info("The provided beam can accommodate a single column of bolt on either side of the web [Ref. based on "
                                        "detailing requirement]")
                            logger.info("Performing the design with a single column of bolt on each side")

                        if (self.gauge_cs_distance_provided + (2 * self.edge_distance_provided)) > self.ep_width_provided:
                            self.design_status = False
                            logger.error("[Detailing] The beam is not wide enough to accommodate a single column of bolt on either side")
                            logger.error("The defined beam is not suitable for this connection design")
                            logger.info("Please provide another beam which has sufficient width (minimum, {} mm)"
                                        .format(self.gauge_cs_distance_provided + (2 * self.edge_distance_provided)))

                        # Check 6: bolt design

                        # column and row combination for running iterations
                        if self.endplate_type == 'Extended One Way - Irreversible Moment':
                            row_list = np.arange(self.rows_minimum_req, self.rows_total_max + 1, 1).tolist()
                        else:
                            row_list = np.arange(self.rows_minimum_req, self.rows_total_max + 1, 2).tolist()
                        column_list = np.arange(2, self.bolt_column + 1, 2).tolist()

                        if self.bolt_column == 4:
                            column_list = column_list[::-1]

                        combined_list = []

                        # combine each possible row and column combination starting from minimum to maximum
                        for q in column_list:
                            for r in row_list:
                                combined_list.append(q)
                                combined_list.append(r)

                        combined_list = combined_list

                        # create a list of tuple with a combination of number of columns and rows for running the iteration
                        combined_list = [x for x in zip(*[iter(combined_list)] * 2)]
                        logger.info("Checking the design with the following number of column and rows combination {}".format(combined_list))

                        # selecting each possible combination of column and row iteratively to perform design checks
                        # starting from minimum column and row to maximum until overall bolt design status is True
                        for item in combined_list:
                            if self.helper_file_design_status is False:
                                select_list = item  # selected tuple from the list

                                self.bolt_column = select_list[0]
                                self.bolt_row = select_list[1]

                                # run the bolt and end plate check function from the helper class
                                self.design_bolt = self.call_helper.perform_bolt_design(self.endplate_type, self.supported_section, self.gamma_m0,
                                                                                        self.bolt_column, self.bolt_row, self.bolt_diameter_provided,
                                                                                        self.bolt_grade_provided, self.load_moment_effective,
                                                                                        self.end_distance_provided, self.pitch_distance_provided,
                                                                                        self.beta, self.proof_stress, self.dp_plate_fy,
                                                                                        self.plate_thickness, self.dp_plate_fu)


                                # TODO: check the round down value in the below loops
                                # checking for the maximum pitch distance of the bolts for a safe design
                                # if space is available then add rows
                                if self.call_helper.helper_file_design_status is True:
                                    # max pitch
                                    self.pitch_distance_max = self.cl_10_2_3_1_max_spacing([self.plate_thickness])

                                    # flushed or both way
                                    if self.endplate_type is VALUES_ENDPLATE_TYPE[0] or VALUES_ENDPLATE_TYPE[2]:

                                        # checking space availability
                                        if self.endplate_type is VALUES_ENDPLATE_TYPE[0]:
                                            space_available_web = self.beam_D - (2 * self.end_distance_provided) - ((self.bolt_row - 2) *
                                                                                                                self.pitch_distance_provided)
                                        else:
                                            if (self.bolt_row / 2) <= 3:
                                                rows_inside_D = self.bolt_row - 2  # one row each outside top and bottom flange
                                            else:
                                                rows_inside_D = self.bolt_row - 4  # two rows each outside top and bottom flange

                                            space_available_web = self.beam_D - (2 * self.end_distance_provided) - ((rows_inside_D - 2) *
                                                                                                                    self.pitch_distance_provided)

                                        # adding rows
                                        if space_available_web > self.pitch_distance_max:
                                            # provide the first bolt row at the centre of the beam (NA)
                                            self.bolt_row_web = 1

                                            if (space_available_web / 2) > self.pitch_distance_max:
                                                self.bolt_row_web += 2 * round_down((space_available_web / 2) / self.pitch_distance_max, 1)
                                        else:
                                            self.bolt_row_web = 0

                                    # one way connection
                                    # checking space availability
                                    elif self.endplate_type is VALUES_ENDPLATE_TYPE[1]:
                                        if self.bolt_row is 3:
                                            rows_inside_D = 2
                                        elif self.bolt_row is 4:
                                            rows_inside_D = 3
                                        else:
                                            rows_inside_D = self.bolt_row - 2

                                        space_available_web = self.beam_D - (2 * self.end_distance_provided) - ((rows_inside_D - 2) *
                                                                                                                self.pitch_distance_provided)
                                        space_available_below_na = (self.beam_D / 2) - self.beam_tf - self.end_distance_provided

                                        # adding rows
                                        if space_available_web >= space_available_below_na:
                                            # last row of tension bolts is above NA of the beam
                                            space_available_above_na = space_available_web - space_available_below_na
                                            if (space_available_above_na + space_available_below_na) >= self.pitch_distance_max:
                                                self.bolt_row_web = 1  # first row at NA

                                            # rows below NA
                                            if space_available_below_na > self.pitch_distance_max:
                                                self.bolt_row_web += round_down(space_available_below_na / self.pitch_distance_max, 1)
                                            else:
                                                self.bolt_row_web += 0

                                            # rows above NA
                                            if space_available_above_na > self.pitch_distance_max:
                                                self.bolt_row_web += round_down(space_available_above_na / self.pitch_distance_max, 1)
                                            else:
                                                self.bolt_row_web += 0

                                        else:  # space is available only below the NA
                                            if space_available_below_na > self.pitch_distance_max:
                                                self.bolt_row_web = round_down(space_available_below_na / self.pitch_distance_max, 1)
                                            else:
                                                self.bolt_row_web = 0

                                    # final number of rows
                                    self.bolt_row += self.bolt_row_web
                                else:
                                    self.design_status = False

                                # calling bolt design results

                                # shear design
                                self.bolt_shear_demand = self.call_helper.bolt_shear_demand
                                self.bolt_shear_capacity = self.call_helper.bolt_shear_capacity
                                self.bolt_bearing_capacity = self.call_helper.bolt_bearing_capacity
                                self.bolt_capacity = self.call_helper.bolt_capacity

                                # tension design
                                self.tension_critical_bolt = round(self.call_helper.t_1, 2)
                                self.prying_critical_bolt = self.call_helper.prying_force
                                self.tension_demand_critical_bolt = round(self.call_helper.bolt_tension_demand, 2)
                                self.tension_capacity_critical_bolt = self.call_helper.bolt_tension_capacity
                                self.combined_capacity_critical_bolt = self.call_helper.bolt_combined_check_UR

                                # number of bolts
                                self.bolt_numbers = self.bolt_column * self.bolt_row

                                # End Plate
                                self.ep_moment_capacity = round(self.call_helper.mp_plate * 1e-6, 2)

                                if self.endplate_type == 'Flushed - Reversible Moment':
                                    self.ep_height_provided = self.beam_D + 25

                                elif self.endplate_type == 'Extended One Way - Irreversible Moment':
                                    if self.bolt_row <= 4:  # 1 row above tension flange
                                        self.ep_height_provided = self.beam_D + 12.5 + (2 * self.end_distance_provided)
                                    else:  # 2 rows above tension flange which is maximum allowable
                                        self.ep_height_provided = self.beam_D + 12.5 + (2 * self.end_distance_provided) + self.pitch_distance_provided

                                else:
                                    if self.bolt_row < 8:  # 1 row outside tension and compressionflange
                                        self.ep_height_provided = self.beam_D + (2 * (2 * self.end_distance_provided))
                                    else:  # 2 rows outside tension and compression flange which is maximum allowable
                                        self.ep_height_provided = self.beam_D + (2 * (2 * self.end_distance_provided)) + (
                                                    2 * self.pitch_distance_provided)

                                # Log messages for helper file
                                if self.call_helper.flange_capacity_status is False:
                                    logger.error(
                                        "[Flange Strength] The reaction at the compression flange of the beam {} kN exceeds the flange capacity {} "
                                        "kN".
                                        format(round(self.call_helper.r_c, 2), self.call_helper.flange_capacity))
                                    logger.error("Reaction on the flange exceeds the flange capacity by {} kN".
                                                 format(round(self.call_helper.r_c - self.call_helper.flange_capacity, 2)))
                                    logger.warning("The beam flange can have local buckling")
                                    logger.info(
                                        "Select a different beam with more flange area or provide stiffening at the flange to increase the beam "
 
                                        "flange thickness. Re-design connection using the effective flange thickness after stiffening")
                                    logger.info("Custom beams can be defined through the Osdag Design Preferences tab")
                                else:
                                    logger.info(
                                        "[Flange Strength] The reaction at the compression flange of the beam {} kN is less than the flange capacity"
                                        " {} kN. The flange strength requirement is satisfied.".
                                        format(round(self.call_helper.r_c, 2), self.call_helper.flange_capacity))

                                if self.call_helper.plate_design_status is False:
                                    logger.error(
                                        "[End Plate] The selected trial end plate of {} mm is insufficient and fails in the moment capacity check".
                                        format(self.plate_thickness))
                                    logger.info(
                                        "The minimum required thickness of end plate is {} mm".format(round(self.call_helper.plate_thickness_req, 2)))
                                    logger.info("Re-designing the connection with a plate of available higher thickness")
                                else:
                                    logger.info(
                                        "[End Plate] The end plate of {} mm passes the moment capacity check. The end plate is checked for yielding "
                                        "due tension caused by bending moment and prying force".format(self.plate_thickness))

                                if self.call_helper.bolt_tension_design_status is False:
                                    logger.error("[Bolt Design] The bolt of {} mm diameter and {} grade fails the tension check".
                                                 format(self.bolt_diameter_provided, self.bolt_grade_provided))
                                    logger.error(
                                        "Total tension demand on bolt (due to direct tension + prying action) is {} kN and exceeds the bolt tension "
                                        "capacity ({} kN)".format(self.call_helper.bolt_tension_demand, self.call_helper.bolt_tension_capacity))
                                    logger.info("Re-designing the connection with a bolt of higher grade and/or diameter")
                                else:
                                    logger.info("[Bolt Design] The bolt of {} mm diameter and {} grade passes the tension check".
                                                format(self.bolt_diameter_provided, self.bolt_grade_provided))
                                    logger.info("Total tension demand on bolt (due to direct tension + prying action) is {} kN and the bolt tension "
                                                "capacity is ({} kN)".format(self.call_helper.bolt_tension_demand,
                                                                             self.call_helper.bolt_tension_capacity))

                                if self.call_helper.bolt_design_combined_check_status is False:
                                    logger.error("[Bolt Design] The bolt of {} mm diameter and {} grade fails the combined shear + tension check".
                                                 format(self.bolt_diameter_provided, self.bolt_grade_provided))
                                    logger.error(
                                        "The Interaction Ratio (IR) of the critical bolt is {} ".format(self.call_helper.bolt_combined_check_UR))
                                    logger.info("Re-designing the connection with a bolt of higher grade and/or diameter")
                                else:
                                    logger.info("[Bolt Design] The bolt of {} mm diameter and {} grade passes the combined shear + tension check".
                                                format(self.bolt_diameter_provided, self.bolt_grade_provided))
                                    logger.info(
                                        "The Interaction Ratio (IR) of the critical bolt is {} ".format(self.call_helper.bolt_combined_check_UR))

                                # checker for the bolt design (helper file) loop
                                if self.call_helper.helper_file_design_status is True:
                                    self.design_status = True
                                    break
                                else:
                                    self.design_status = False

                        # checker for the bolt dia-grade selection loop
                        if self.call_helper.helper_file_design_status is True:
                            self.design_status = True
                            break
                        else:
                            self.design_status = False

                # checker for the plate thickness selection loop
                if self.call_helper.helper_file_design_status is True:
                    self.design_status = True
                    break
                else:
                    self.design_status = False

    def design_stiffener(self):
        """ design stiffener for the connection """

        if self.endplate_type == 'Flushed - Reversible Moment':
            self.stiffener_height = (self.ep_width_provided - self.beam_tw) / 2  # mm
            self.stiffener_length = 2 * self.stiffener_height  # mm
        else:
            if self.endplate_type == 'Extended Both Ways - Reversible Moment':
                self.stiffener_height = (self.ep_height_provided - self.beam_D) / 2  # mm
            else:
                self.stiffener_height = self.ep_height_provided - self.beam_D - 12.5  # mm

            self.stiffener_length = round_up((self.stiffener_height / math.tan(30)), 2)  # mm

        self.stiffener_thickness = round_up(self.beam_tw, 2)  # mm

    def design_weld(self):
        """ design fillet weld at web for the connection """

        # weld size calculation
        self.weld_length_web = 2 * (self.beam_D - (2 * self.beam_tf) - (2 * self.beam_r1) - 20)  # mm, on either side of the web
        self.weld_size_web = (self.load_shear * 1e3 * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_length_web * self.web_weld.fu)  # mm

        self.web_weld.set_min_max_sizes(self.plate_thickness, self.beam_tw, special_circumstance=False, fusion_face_angle=90)

        self.weld_size_web = round_up(max(self.weld_size_web, self.web_weld.min_size), 2)  # mm

        # combination of stress check
        self.f_a = round((self.load_axial * 1e3) / (0.7 * self.weld_size_web * self.weld_length_web), 2)  # N/mm^2, stress due to axial force
        self.q = round((self.load_shear * 1e3) / (0.7 * self.weld_size_web * self.weld_length_web), 2)  # N/mm^2, stress due to shear force

        self.f_e = round(math.sqrt(self.f_a + (3 * self.q ** 2)), 2)  # N/mm^2, stress due to combined load

        self.allowable_stress = round(self.web_weld.fu / (math.sqrt(3) * self.gamma_mw), 2)  # N/mm^2, allowable stress in the weld

        # allowable stress check
        if self.f_e > self.allowable_stress:
            self.design_status = False
            logger.error("[Weld Design] The weld at web fails in the combined axial and shear design check")
            logger.info("Provide groove weld at the web")

        # end of calculation
        if self.design_status:
            logger.info(": =========================Design Status===========================")
            logger.info(": Overall beam to beam end plate splice connection design is SAFE")
            logger.info(": =========================End Of design===========================")
        else:
            logger.info(": =========================Design Status===========================")
            logger.info(": Overall beam to beam end plate splice connection design is UNSAFE")
            logger.info(": =========================End Of design===========================")

    # create design report
    def save_design(self, popup_summary):
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")

        if self.supported_section.flange_slope == 90:
            image = "Parallel_Beam"
        else:
            image = "Slope_Beam"
        self.report_supporting = {KEY_DISP_SEC_PROFILE: "ISection",
                                  KEY_DISP_BEAMSEC: self.supported_section.designation,
                                  KEY_DISP_MATERIAL: self.supported_section.material,
                                  KEY_DISP_FU: self.supported_section.fu,
                                  KEY_DISP_FY: self.supported_section.fy,
                                  'Mass': self.supported_section.mass,
                                  'Area(mm2) - A': round(self.supported_section.area, 2),
                                  'D(mm)': self.supported_section.depth,
                                  'B(mm)': self.supported_section.flange_width,
                                  't(mm)': self.supported_section.web_thickness,
                                  'T(mm)': self.supported_section.flange_thickness,
                                  'FlangeSlope': self.supported_section.flange_slope,
                                  'R1(mm)': self.supported_section.root_radius,
                                  'R2(mm)': self.supported_section.toe_radius,
                                  'Iz(mm4)': self.supported_section.mom_inertia_z,
                                  'Iy(mm4)': self.supported_section.mom_inertia_y,
                                  'rz(mm)': self.supported_section.rad_of_gy_z,
                                  'ry(mm)': self.supported_section.rad_of_gy_y,
                                  'Zz(mm3)': self.supported_section.elast_sec_mod_z,
                                  'Zy(mm3)': self.supported_section.elast_sec_mod_y,
                                  'Zpz(mm3)': self.supported_section.plast_sec_mod_z,
                                  'Zpy(mm3)': self.supported_section.elast_sec_mod_y}

        self.report_input = \
            {KEY_MODULE: self.module,
             KEY_MAIN_MODULE: self.mainmodule,
             # KEY_CONN: self.connectivity,
             KEY_DISP_MOMENT: self.load.moment,
             KEY_DISP_SHEAR: self.load.shear_force,
             KEY_DISP_AXIAL: self.load.axial_force,

             "Section": "TITLE",
             "Section Details": self.report_supporting,

             "Bolt Details": "TITLE",
             KEY_DISP_D: str(self.bolt.bolt_diameter),
             KEY_DISP_GRD: str(self.bolt.bolt_grade),
             KEY_DISP_TYP: self.bolt.bolt_type,

             KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
             KEY_DISP_DP_BOLT_SLIP_FACTOR: self.bolt.mu_f,
             KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
             KEY_DISP_GAP: self.plate.gap,
             KEY_DISP_CORR_INFLUENCES: self.bolt.corrosive_influences,
             "Plate Details": "TITLE",
             KEY_DISP_PLATETHK: str(self.plate.thickness),
             KEY_DISP_MATERIAL: self.plate.material,
             KEY_DISP_FU: self.plate.fu,
             KEY_DISP_FY: self.plate.fy,
             "Weld Details": "TITLE",
             # KEY_DISP_DP_WELD_TYPE: "Fillet",
             # KEY_DISP_DP_WELD_FAB: self.weld.fabrication,
             # KEY_DISP_DP_WELD_MATERIAL_G_O: self.weld.fu
             }

        self.report_check = []

        Disp_3D_image = "/ResourceFiles/images/3d.png"

        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")

        fname_no_ext = popup_summary['filename']

        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_3D_image)