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

        self.module = KEY_DISP_BB_EP_SPLICE

        self.load_moment = 0.0
        self.load_moment_effective = 0.0
        self.load_shear = 0.0
        self.load_axial = 0.0
        self.input_shear_force = 0.0
        self.input_axial_force = 0.0
        self.input_moment = 0.0

        # self.supported_section = Beam
        self.bolt_diameter = []
        self.bolt_list = []
        self.bolt_diameter_provided = 0
        self.bolt_grade = []
        self.bolt_grade_provided = 0.0
        self.bolt_hole_diameter = 0.0
        self.bolt_type = ""
        self.plate_thickness = []
        self.plate_thickness_list = []

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
        self.pitch_distance_max = 0.0
        self.pitch_distance_web = 0.0
        self.gauge_distance_provided = self.pitch_distance_provided
        self.end_distance_provided = 0.0
        self.edge_distance_provided = self.end_distance_provided
        self.gauge_cs_distance_provided = 0.0
        self.space_available_inside_D = 0.0
        self.space_min_req_inside_D = 0.0
        self.space_available_web = 0.0
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
        self.bolt_column = 0
        self.bolt_row = 0
        self.last_column = 0

        self.bolt_row_web = 0
        self.bolt_numbers = self.bolt_column * self.bolt_row

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
        self.design_status_list = []
        self.design_status = False

        self.beam_properties = {}
        self.safety_factors = {}
        self.gamma_m0 = 0.0
        self.gamma_m1 = 0.0
        self.gamma_mb = 0.0
        self.gamma_mw = 0.0

        self.epsilon_beam = 1.0
        self.beam_classification = ''
        self.beam_beta_b_z = 1.0
        self.beam_beta_b_y = 1.0
        self.supported_section_mom_capa_m_zz = 0.0
        self.supported_section_mom_capa_m_yy = 0.0
        self.supported_section_shear_capa = 0.0
        self.supported_section_axial_capa = 0.0
        self.IR_axial = 0.0
        self.IR_shear = 0.0
        self.IR_moment = 0.0
        self.sum_IR = 0.0
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
        self.weld_fu = 0.0
        self.weld_length_web = 0.0
        self.weld_size_web = 0.0
        self.weld_size_web1 = 0.0
        self.allowable_stress = 0.0
        self.f_a = 0.0
        self.q = 0.0
        self.f_e = 0.0
        self.weld_size_stiffener = 0.0

        # self.func_for_validation(self, design_dictionary)

    # Set logger
    def set_osdaglogger(key):
        """ Function to set Logger for the module """
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
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
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

        t2 = (KEY_CONN, KEY_CONN, TYPE_COMBOBOX, VALUES_CONN_SPLICE, True, 'No Validator', [1, 2])
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

        ep_type = self[0]
        if ep_type == VALUES_ENDPLATE_TYPE[0]:
            return './ResourceFiles/images/flush_ep.png'
        elif ep_type == VALUES_ENDPLATE_TYPE[1]:
            return './ResourceFiles/images/owe_ep.png'
        elif ep_type == VALUES_ENDPLATE_TYPE[2]:
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

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, self.bolt_bearing_capacity if flag else '', True)
        out_list.append(t5)

        if self.design_status:
            t5 = (KEY_OUT_BETA_LG, KEY_OUT_DISP_BETA_LG, TYPE_TEXTBOX, self.call_helper.beta_lg if flag and self.bolt.bolt_type == "Bearing Bolt"
            else 'N/A', True)
        else:
            t5 = (KEY_OUT_BETA_LG, KEY_OUT_DISP_BETA_LG, TYPE_TEXTBOX, self.call_helper.beta_lg if flag and self.bolt.bolt_type == "Bearing Bolt"
            else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, DISP_TITLE_BOLT_CAPACITY, TYPE_TEXTBOX, self.bolt_capacity if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_OUT_BOLT_TENSION_FORCE, KEY_OUT_DISP_CRITICAL_BOLT_TENSION, TYPE_TEXTBOX, self.tension_critical_bolt if flag else '', True)
        out_list.append(t7)

        t8 = (KEY_OUT_BOLT_PRYING_FORCE, KEY_OUT_DISP_BOLT_PRYING_FORCE_EP, TYPE_TEXTBOX, self.prying_critical_bolt if flag else '', True)
        out_list.append(t8)

        t9 = (KEY_OUT_BOLT_TENSION_TOTAL, KEY_OUT_DISP_BOLT_TENSION_DEMAND, TYPE_TEXTBOX, self.tension_demand_critical_bolt if flag else '', True)
        out_list.append(t9)

        t10 = (KEY_OUT_BOLT_TENSION_CAPACITY, KEY_OUT_CRITICAL_BOLT_TENSION_CAPACITY, TYPE_TEXTBOX, self.tension_capacity_critical_bolt if flag else '',
        True)
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

        if self.design_status:
            t22 = (KEY_OUT_DETAILING_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX,
                   self.gauge_distance_provided if flag and self.bolt_column == 4 else 'N/A', True)
        else:
            t22 = (KEY_OUT_DETAILING_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX,
                   self.gauge_distance_provided if flag else '', True)
        out_list.append(t22)

        t22 = (KEY_OUT_DETAILING_CS_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_CS_GAUGE_DISTANCE, TYPE_TEXTBOX, self.gauge_cs_distance_provided if flag else '',
        True)
        out_list.append(t22)

        t16 = (KEY_OUT_DETAILING_END_DISTANCE, KEY_OUT_DISP_DETAILING_END_DISTANCE, TYPE_TEXTBOX, self.end_distance_provided if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_DETAILING_EDGE_DISTANCE, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.edge_distance_provided if flag else '', True)
        out_list.append(t17)

        t31 = (DISP_TITLE_DETAILING, DISP_TITLE_TYPICAL_DETAILING, TYPE_OUT_BUTTON, ['Details', self.detailing], True)
        out_list.append(t31)

        # End Plate
        t18 = (None, DISP_TITLE_ENDPLATE, TYPE_TITLE, None, True)
        out_list.append(t18)

        t19 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, int(self.plate_thickness) if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.ep_height_provided if flag else '', True)
        out_list.append(t20)

        t21 = (KEY_OUT_PLATE_WIDTH, KEY_OUT_DISP_PLATE_WIDTH, TYPE_TEXTBOX, self.ep_width_provided if flag else '', True)
        out_list.append(t21)

        t22 = (KEY_OUT_EP_MOM_CAPACITY, KEY_OUT_DISP_EP_MOM_CAPACITY, TYPE_TEXTBOX, self.call_helper.plate_moment_capacity if flag else '', True)
        out_list.append(t22)

        # Stiffener Details
        t32 = (None, DISP_TITLE_STIFFENER_PLATE, TYPE_TITLE, None, True)
        out_list.append(t32)

        t33 = (KEY_OUT_STIFFENER_DETAILS, KEY_OUT_DISP_STIFFENER_DIMENSIONS, TYPE_OUT_BUTTON, ['Details', self.stiffener_details], True)
        out_list.append(t33)

        t34 = (KEY_OUT_STIFFENER_SKETCH, KEY_OUT_DISP_STIFFENER_SKETCH, TYPE_OUT_BUTTON, ['Details', self.stiffener_detailing], True)
        out_list.append(t34)

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

        t26 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX, 'Groove Weld' if flag else '', True)
        out_list.append(t26)

        t31 = (KEY_OUT_WELD_DETAILS, DISP_TITLE_WELD_TYPICAL_DETAIL, TYPE_OUT_BUTTON, ['Details', self.weld_details], True)
        out_list.append(t31)

        return out_list

    # stiffener details
    def stiffener_details(self, flag):

        stiffener = []

        t28 = (KEY_OUT_STIFFENER_LENGTH, KEY_OUT_DISP_STIFFENER_LENGTH, TYPE_TEXTBOX, float(self.stiffener_length) if flag else '', True)
        stiffener.append(t28)

        t29 = (KEY_OUT_STIFFENER_HEIGHT if self.endplate_type != VALUES_ENDPLATE_TYPE[0] else KEY_OUT_STIFFENER_WIDTH,
               KEY_OUT_DISP_STIFFENER_HEIGHT if self.endplate_type != VALUES_ENDPLATE_TYPE[0] else KEY_OUT_DISP_STIFFENER_WIDTH,
               TYPE_TEXTBOX, float(self.stiffener_height) if flag else '', True)
        stiffener.append(t29)

        t30 = (KEY_OUT_STIFFENER_THICKNESS, KEY_OUT_DISP_STIFFENER_THICKNESS, TYPE_TEXTBOX, str(self.stiffener_thickness) if flag else '', True)
        stiffener.append(t30)

        return stiffener

    # stiffener detailing
    def stiffener_detailing(self, status):

        detailing = []

        if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
            detailing_path = './ResourceFiles/images/BB_Stiffener_FP.png'
            width = 979
            height = 363
        elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
            detailing_path = './ResourceFiles/images/BB_Stiffener_OWE.png'
            width = 636
            height = 562
        else:  # Both-way
            detailing_path = './ResourceFiles/images/BB_Stiffener_BWE.png'
            width = 586
            height = 579

        t1 = (None, 'Typical Stiffener Details', TYPE_IMAGE, [detailing_path, width, height, 'Typical stiffener details'])
        detailing.append(t1)

        return detailing

    # display weld details image
    def weld_details(self, status):

        weld = []

        t99 = (None, 'Weld Detail - Beam Flange to End Plate Connection', TYPE_IMAGE,
               ['./ResourceFiles/images/BB-BC-single_bevel_groove.png', 575, 520,
                'Weld Detail - beam to end plate connection'])
        weld.append(t99)

        return weld

    def detailing(self, status):

        detailing = []

        if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
            path = './ResourceFiles/images/Detailing-Flush.png'
            width = 502
            height = 551
        elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
            path = './ResourceFiles/images/Detailing-OWE.png'
            width = 437
            height = 552
        else:  # Both-way
            path = './ResourceFiles/images/Detailing-BWE.png'
            width = 387
            height = 551

        t99 = (None, 'Typical Connection Detailing', TYPE_IMAGE, [path, width, height, 'Typical connection detailing'])
        detailing.append(t99)

        return detailing

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

        t2 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC_MATERIAL], [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY], TYPE_TEXTBOX,
              self.get_fu_fy_I_section_suptd)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t3)

        t3 = ("Bolt", [KEY_TYP], [KEY_DP_BOLT_TYPE], TYPE_COMBOBOX, self.get_bolt_tension_type_for_prying)
        change_tab.append(t3)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        t7 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

        return change_tab

    def refresh_input_dock(self):

        add_buttons = []

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

        val = {KEY_DP_BOLT_TYPE: "Non pre-tensioned",
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

        # t3 = ('Column', self.call_3DColumn)
        # components.append(t3)

        t4 = ('End Plate', self.call_3DPlate)
        components.append(t4)

        return components

    # display end plate
    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'End Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Connector", bgcolor)

    # get the input values from UI and other functions
    def set_input_values(self, design_dictionary):
        """ get the input values from UI (input dock and DP) for performing the design etc. """
        super(BeamBeamEndPlateSplice, self).set_input_values(self, design_dictionary)

        self.mainmodule = "Moment Connection"
        self.module = KEY_DISP_BB_EP_SPLICE
        self.connectivity = design_dictionary[KEY_CONN]
        self.endplate_type = design_dictionary[KEY_ENDPLATE_TYPE]
        self.material = Material(material_grade=design_dictionary[KEY_MATERIAL])

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

        self.stiffener_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                             type=design_dictionary[KEY_DP_WELD_TYPE], fabrication=design_dictionary[KEY_DP_WELD_FAB])

        self.warn_text(self)

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
        if self.bolt.bolt_tensioning == 'Pre-tensioned':
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
        self.gamma_mw = self.cl_5_4_1_Table_5["gamma_mw"][self.dp_weld_fab]  # gamma_mw = 1.25 for 'Shop Weld' and 1.50 for 'Field Weld'

        # initialize design status
        self.plate_design_status = False
        self.helper_file_design_status = False
        self.design_status_list = []
        self.design_status = False

        # helper function

        self.call_helper = EndPlateSpliceHelper(module=self.module, supporting_section=self.supported_section,
                                                supported_section=self.supported_section, load=self.load, bolt=self.bolt,
                                                connectivity=self.connectivity, ep_type=self.endplate_type, plate_design_status=False,
                                                helper_file_design_status=False)
        self.projection = 12.5

        self.set_parameters(self)
        self.design_connection(self)
        self.design_stiffener(self)
        self.design_weld(self)

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
        # Input loads
        self.input_shear_force = self.load.shear_force
        self.input_axial_force = self.load.axial_force
        self.input_moment = self.load.moment  # about the major (z-z) axis of the beam

        # Capacities

        # 1: Moment capacity of the beam

        # 1.1: Section classification of the beam (Table 2, IS 800:2007)
        self.epsilon_beam = round(math.sqrt(250 / self.supported_section.fy), 2)

        # flange b/t check - outstanding element
        if self.supported_section.type == 'Rolled':

            if ((self.beam_bf / 2) / self.beam_tf) > (10.5 * self.epsilon_beam):
                self.beam_classification = 'Semi-compact'
            elif ((self.beam_bf / 2) / self.beam_tf) <= (9.4 * self.epsilon_beam):
                self.beam_classification = 'Plastic'
            else:
                self.beam_classification = 'Compact'
        else:
            if (((self.beam_bf - self.beam_tw) / 2) / self.beam_tf) > (9.4 * self.epsilon_beam):
                self.beam_classification = 'Semi-compact'
            elif ((self.beam_bf / 2) / self.beam_tf) <= (8.4 * self.epsilon_beam):
                self.beam_classification = 'Plastic'
            else:
                self.beam_classification = 'Compact'

        # 1.2: Bending capacity
        if self.beam_classification == 'Semi-compact':
            self.beam_beta_b_z = self.supported_section.elast_sec_mod_z / self.supported_section.plast_sec_mod_z
            self.beam_beta_b_y = self.supported_section.elast_sec_mod_y / self.supported_section.plast_sec_mod_y
            section_class = 'semi-compact'
        else:
            self.beam_beta_b_z = 1.0
            self.beam_beta_b_y = 1.0
            section_class = 'Compact'

        # Moment capacity about the major (z-z) axis
        self.supported_section_mom_capa_m_zz = self.cl_8_2_1_2_design_moment_strength(self.supported_section.elast_sec_mod_z,
                                                                                      self.supported_section.plast_sec_mod_z,
                                                                                      self.supported_section.fy, section_class=section_class)
        self.supported_section_mom_capa_m_zz = round(self.supported_section_mom_capa_m_zz * 1e-6, 2)  # kNm

        # Moment capacity about the minor (y-y) axis
        self.supported_section_mom_capa_m_yy = self.cl_8_2_1_2_design_moment_strength(self.supported_section.elast_sec_mod_y,
                                                                                      self.supported_section.plast_sec_mod_y,
                                                                                      self.supported_section.fy, section_class=section_class)
        self.supported_section_mom_capa_m_yy = round(self.supported_section_mom_capa_m_yy * 1e-6, 2)  # kNm

        # 2: Shear capacity of the beam
        if self.supported_section.type == 'Rolled':
            # self.supported_section_shear_capa = ((self.beam_D * self.beam_tw) * self.beam_fy) / (math.sqrt(3) * self.gamma_m0)
            self.supported_section_shear_capa = (((self.beam_D - (2 * self.beam_tf)) * self.beam_tw) * self.supported_section.fy) / \
                                                (math.sqrt(3) * self.gamma_m0)
        else:  # built-up sections
            self.supported_section_shear_capa = (((self.beam_D - (2 * self.beam_tf)) * self.beam_tw) * self.supported_section.fy) / \
                                                (math.sqrt(3) * self.gamma_m0)

        self.supported_section_shear_capa = round(0.6 * self.supported_section_shear_capa * 1e-3, 2)  # kN, restricted to low shear

        # 3: Axial capacity of the beam
        self.supported_section_axial_capa = round((self.supported_section.area * self.supported_section.fy / self.gamma_m0) * 1e-3, 2)  # kN

        # Interaction ratio check for loads
        # loads are in kN
        self.IR_axial = round(self.input_axial_force / self.supported_section_axial_capa, 3)
        self.IR_shear = round(self.input_shear_force / self.supported_section_shear_capa, 3)
        self.IR_moment = round(self.input_moment / self.supported_section_mom_capa_m_zz, 3)

        self.sum_IR = round(self.IR_axial + self.IR_moment, 3)

        # Minimum load consideration check
        if self.sum_IR <= 1.0:

            if self.IR_axial < 0.3 and self.IR_moment < 0.5:
                self.load_moment = round(0.5 * self.supported_section_mom_capa_m_zz, 2)
                self.load_axial = round(0.3 * self.supported_section_axial_capa, 2)

                logger.warning("The Load(s) defined is/are less than the minimum recommended value [Ref. IS 800:2007, Cl.10.7].")
                logger.warning("[Minimum Factored Load] The external factored bending moment ({} kNm) is less than 0.5 times the plastic moment "
                               "capacity of the beam ({} kNm)".format(self.load.moment, self.supported_section_mom_capa_m_zz))
                logger.info("The minimum factored bending moment should be at least 0.5 times the plastic moment capacity of the beam to qualify the "
                            "connection as rigid connection (Annex. F-4.3.1, IS 800:2007)")
                logger.info("The value of load(s) is/are set at minimum recommended value as per Cl.10.7 and Annex. F, IS 800:2007")
                logger.info("Designing the connection for a factored moment of {} kNm".format(self.load_moment))

            elif self.sum_IR <= 1.0 and self.IR_moment < 0.5:

                if (0.5 - self.IR_moment) < (1 - self.sum_IR):
                    self.load_moment = round(0.5 * self.supported_section_mom_capa_m_zz, 2)
                else:
                    self.load_moment = round(self.load.moment + ((1 - self.sum_IR) * self.supported_section_mom_capa_m_zz), 2)
                self.load_axial = self.load.axial_force

                logger.warning("The Load(s) defined is/are less than the minimum recommended value [Ref. IS 800:2007, Cl.10.7].")
                logger.warning("[Minimum Factored Load] The external factored bending moment ({} kNm) is less than 0.5 times the plastic moment "
                               "capacity of the beam ({} kNm)".format(self.load.moment, self.supported_section_mom_capa_m_zz))
                logger.info("The minimum factored bending moment should be at least 0.5 times the plastic moment capacity of the beam to qualify the "
                            "connection as rigid connection (Annex. F-4.3.1, IS 800:2007)")
                logger.info("The value of load(s) is/are set at minimum recommended value as per Cl.10.7 and Annex. F, IS 800:2007")
                logger.info("Designing the connection for a factored moment of {} kNm".format(self.load_moment))

            elif self.sum_IR <= 1.0 and self.IR_axial < 0.3:

                if (0.3 - self.IR_axial) < (1 - self.sum_IR):
                    self.load_axial = round(0.3 * self.supported_section_axial_capa, 2)
                else:
                    self.load_axial = round(self.load.axial_force + ((1 - self.sum_IR) * self.supported_section_axial_capa), 2)

                self.load_moment = round(self.supported_section_mom_capa_m_zz, 2)

                logger.warning("The Load(s) defined is/are less than the minimum recommended value [Ref. IS 800:2007, Cl.10.7]")
                logger.info("The value of factored axial force ({} kN) is less than the minimum recommended value [Ref. Cl.10.7, IS 800:2007]".
                            format(self.input_axial_force))
                logger.info("The value of axial force is set at {} kN, as per the minimum recommended value by Cl.10.7".format(self.load_axial))
            else:
                self.load_axial = self.input_axial_force
                self.load_moment = self.input_moment

            self.load_axial = self.input_axial_force
        else:
            # Maximum moment check
            if self.load.moment > self.supported_section_mom_capa_m_zz:
                self.load_moment = self.supported_section_mom_capa_m_zz  # kNm
                self.minimum_load_status_moment = True
                self.design_status = False
                self.design_status_list.append(self.design_status)
                logger.error("[Maximum Factored Load] The external factored bending moment ({} kNm) is greater than the plastic moment capacity of "
                             "the beam ({} kNm)".format(self.load.moment, self.supported_section_mom_capa_m_zz))
                logger.warning("The maximum moment carrying capacity of the beam is {} kNm".format(self.supported_section_mom_capa_m_zz))
                logger.info("Define the value of factored bending moment as {} kNm or less and re-design".
                            format(self.supported_section_mom_capa_m_zz))

            # Maximum axial force check
            if self.load.axial_force > self.supported_section_axial_capa:
                self.load_axial = self.supported_section_axial_capa  # kNm
                self.design_status = False
                self.design_status_list.append(self.design_status)
                logger.error("[Maximum Factored Load] The external factored axial force ({} kN) is greater than the axial capacity of "
                             "the beam ({} kN)".format(self.load.axial_force, self.supported_section_axial_capa))
                logger.warning("The maximum axial capacity of the beam is {} kN".format(self.supported_section_axial_capa))
                logger.info("Define the value of axial force as {} kN or less and re-design".format(self.supported_section_axial_capa))
            else:
                self.load_axial = self.load.axial_force

        # Shear force check
        if self.load.shear_force < min((0.15 * self.supported_section_shear_capa), 40):
            self.minimum_load_status_shear = True
            self.load_shear = min((0.15 * self.supported_section_shear_capa), 40)
            logger.warning("[Minimum Factored Load] The external factored shear force ({} kN) is less than the minimum recommended design action on "
                           "the member".format(self.load_shear))
            logger.info("The minimum factored shear force should be at least {} (0.15 times the shear capacity of the beam in low shear) or 40 kN "
                        "whichever is less [Ref. Cl. 10.7, IS 800:2007]".format(0.15 * self.supported_section_shear_capa))
            logger.info("Designing the connection for a factored shear load of {} kNm".format(self.load_shear))
        elif self.load.shear_force > self.supported_section_shear_capa:
            self.load_shear = self.supported_section_shear_capa  # kN
            self.minimum_load_status_moment = True
            self.design_status = False
            self.design_status_list.append(self.design_status)
            logger.error("[Maximum Factored Load] The external factored shear force ({} kN) is greater than the shear capacity of the "
                         "beam ({} kN)".format(self.load_shear, self.supported_section_shear_capa))
            logger.warning("The maximum shear capacity of the beam is {} kN".format(self.supported_section_shear_capa))
            logger.info("Define the value of factored shear force as {} kN or less".format(self.supported_section_shear_capa))
        else:
            self.minimum_load_status_shear = False
            self.load_shear = self.load.shear_force

        # effective moment is the moment due to external factored moment plus moment due to axial force
        self.load_moment_effective = round(self.load_moment + (self.load_axial * ((self.beam_D / 2) - (self.beam_tf / 2))) * 1e-3, 2)  # kNm

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
                logger.warning("[End Plate] The end plate of {} mm is thinner than the thickest part of the elements being connected".
                               format(round(i, 2)))
                logger.info("Selecting a plate of higher thickness which is at least {} mm thick".format(max(self.beam_tf, self.beam_tw)))

        # final sorted list as per compatibility check
        self.plate_thickness = self.plate_thickness  # final list of plate thicknesses considered for simulation
        self.plate_thickness_list = self.plate_thickness

        # checking if the list contains at least one plate of thk higher than the minimum required
        if len(self.plate_thickness) == 0:
            self.design_status = False
            self.design_status_list.append(self.design_status)
            logger.error("[End Plate] The list of plate thicknesses passed into the solver is insufficient to perform end plate design")
            logger.warning("The end plate should at least be thicker than the maximum thickness of the connecting elements")
            logger.info("Provide a plate/list of plates with a minimum thickness of {} mm".format(round_up(max(self.beam_tf, self.beam_tw), 2)))

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
                    .format(int(len(self.bolt_list) / 2)))

        # create a list of tuple with a combination of each bolt diameter with each grade for iteration
        # list is created using the approach --- minimum diameter, small grade to maximum diameter, high grade
        self.bolt_list = [x for x in zip(*[iter(self.bolt_list)] * 2)]
        # logger.info("Checking the design with the following bolt diameter-grade combination {}".format(self.bolt_list))

    def design_connection(self):
        """ perform analysis and design of bolt and end plate """

        # Check 1: calculate tension due to external factored moment and axial force in the tension flange
        # Assumption: the NA is assumed at the centre of the bottom flange

        self.tension_due_to_moment = round((self.load_moment * 1e3 / (self.beam_D - self.beam_tf)), 2)  # kN
        self.tension_due_to_axial_force = round(self.load_axial / 2, 2)  # kN
        self.load_tension_flange = self.tension_due_to_moment + self.tension_due_to_axial_force  # kN

        # performing the check with minimum plate thickness and a suitable bolt dia-grade combination (thin plate - large dia approach)
        logger.info("[Optimisation] Performing the design by optimising the plate thickness, using the most optimum plate and a suitable bolt "
                    "diameter "
                    "approach")
        logger.info("If you wish to optimise the bolt diameter-grade combination, pass a higher value of plate thickness using the Input Dock")

        # loop starts
        self.helper_file_design_status = False  # initialise status to False to activate the loop for first (and subsequent, if required) iteration(s)

        if len(self.plate_thickness_list) != 0:
            for i in self.plate_thickness:
                if self.helper_file_design_status == False:

                    self.plate_thickness = i  # assigns plate thickness from the list

                    # self.helper_file_design_status = False  # initialize helper file status as False to activate the bolt design loop

                    # selecting a single dia-grade combination (from the list of a tuple) each time for performing all the checks
                    for j in self.bolt_list:
                        if self.helper_file_design_status == False:

                            test_list = j  # choose a tuple from the list of bolt dia and grade - (dia, grade)
                            self.bolt_diameter_provided = test_list[0]  # select trial diameter
                            self.bolt_grade_provided = test_list[1]  # select trial grade
                            self.bolt_hole_diameter = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter_provided, self.bolt.bolt_hole_type)

                            # assign bolt mechanical properties
                            bolt_fu_fy = IS1367_Part3_2002.get_bolt_fu_fy(self.bolt_grade_provided, self.bolt_diameter_provided)
                            self.bolt_fu = bolt_fu_fy[0]
                            self.dp_bolt_fy = bolt_fu_fy[1]
                            # self.proof_load = self.bolt.proof_load
                            self.proof_stress = round(0.7 * self.bolt_fu, 2)  # N/mm^2

                            # assign plate mechanical properties
                            self.plate.connect_to_database_to_get_fy_fu(grade=self.plate.material, thickness=self.plate_thickness)
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
                            self.end_distance_provided = self.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_provided, self.bolt.bolt_hole_type,
                                                                                            self.bolt.edge_type)
                            self.end_distance_provided = round_up(self.end_distance_provided, 5)  # mm
                            self.edge_distance_provided = self.end_distance_provided

                            # cross-centre gauge
                            # self.gauge_cs_distance_provided = self.beam_tw + (2 * self.beam_r1) + (2 * self.end_distance_provided)
                            self.gauge_cs_distance_provided = self.beam_tw + self.beam_r1 + (2 * self.end_distance_provided)
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
                            self.space_min_req_inside_D = (2 * self.end_distance_provided) + self.pitch_distance_provided

                            if self.space_available_inside_D < self.space_min_req_inside_D:
                                logger.error("[Compatibility Error]: The given beam cannot accommodate at least a single row of bolt (inside top and "
                                             "bottom flange) with a trial diameter of {} mm ".format(self.bolt_diameter_provided))
                                logger.info("Re-design the connection by defining a bolt of smaller diameter or beam of a suitable depth ")
                                self.rows_inside_D_max = 0
                                self.bolt_row = 0
                                self.bolt_row_web = 0

                                self.design_status = False
                                if (self.plate_thickness == self.plate_thickness_list[-1]) and (self.design_status is False):
                                    self.design_status_list.append(self.design_status)
                            else:
                                self.rows_inside_D_max = 2 + round_down(self.space_available_inside_D / self.pitch_distance_provided, 1)

                            if (((self.rows_inside_D_max - 2) + 1) * self.pitch_distance_provided) > self.space_available_inside_D:
                                self.rows_inside_D_max -= 1

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

                            # Check 5: number of columns of bolt on each side (minimum is 1, maximum is 2)

                            # checking space available to accommodate one or two column of bolts (2 or 4 total) on each side
                            space_req_2col = self.gauge_cs_distance_provided + (2 * self.edge_distance_provided)
                            space_req_4col = self.gauge_cs_distance_provided + (2 * self.gauge_distance_provided) + (2 * self.edge_distance_provided)

                            if self.ep_width_provided >= space_req_4col:
                                self.bolt_column = 4  # two columns on each side
                                # logger.info("The provided beam can accommodate two columns of bolts on either side of the web [Ref. based on the "
                                #             "detailing requirement]")
                                # logger.info("Performing the design with two column of bolts on each side")

                            if (self.ep_width_provided >= space_req_2col) and (self.ep_width_provided < space_req_4col):
                                self.bolt_column = 2  # one column on each side
                                # logger.info("The provided beam can accommodate a single column of bolt on either side of the web [Ref. based on the "
                                #             "detailing requirement]")
                                # logger.info("Performing the design with a single column of bolt on each side")

                            if self.ep_width_provided < space_req_2col:
                                self.bolt_column = 0
                                self.last_column = self.bolt_column
                                self.design_status = False
                                if (self.plate_thickness == self.plate_thickness_list[-1]) and (self.design_status is False):
                                    self.design_status_list.append(self.design_status)

                                logger.error("[Detailing] The beam is not wide enough to accommodate at-least a single column of bolt on either side")
                                logger.error("The defined beam is not suitable for performing connection design for the given set of inputs")
                                logger.info("Please define another beam which has sufficient width (minimum, {} mm) and/or smaller diameter bolt "
                                            "and re-design".
                                            format(space_req_2col))

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
                            # logger.info("Checking the design with the following number of column and rows combination {}".format(combined_list))

                            # selecting each possible combination of column and row iteratively to perform design checks
                            # starting from minimum column and row to maximum until overall bolt design status is True
                            for item in combined_list:
                                if self.helper_file_design_status == False:
                                    select_list = item  # selected tuple from the list

                                    self.bolt_column = select_list[0]
                                    self.bolt_row = select_list[1]

                                    # for design report
                                    self.last_column = self.bolt_column

                                    # initialise bolt requirement near web
                                    self.bolt_row_web = 0
                                    self.pitch_distance_web = 0.0

                                    # run the bolt and end plate check function from the helper class
                                    self.design_bolt = self.call_helper.perform_bolt_design(self.endplate_type, self.supported_section, self.gamma_m0,
                                                                                            self.bolt_column, self.bolt_row, self.bolt_row_web,
                                                                                            self.bolt_diameter_provided, self.bolt_grade_provided,
                                                                                            self.load_moment_effective, self.end_distance_provided,
                                                                                            self.pitch_distance_provided, self.pitch_distance_web,
                                                                                            self.beta, self.proof_stress, self.dp_plate_fy,
                                                                                            self.plate_thickness, self.dp_plate_fu, self.load_shear)

                                    # checking for the maximum pitch distance of the bolts for a safe design
                                    # if space is available then add rows
                                    if self.call_helper.helper_file_design_status == True:

                                        # step 1: max pitch distance
                                        self.pitch_distance_max = self.cl_10_2_3_1_max_spacing([self.plate_thickness])
                                        print("PITCH MAX {}".format(self.pitch_distance_max))

                                        # step 2: checking space availability to accommodate extra rows based on maximum pitch criteria
                                        if self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # one-way
                                            if self.bolt_row <= 4:
                                                rows_inside_D = self.bolt_row - 1
                                            else:
                                                rows_inside_D = self.bolt_row - 2

                                            self.space_available_web = self.beam_D - (2 * self.beam_tf) - (2 * self.end_distance_provided) - \
                                                                       ((rows_inside_D - 2) * self.pitch_distance_provided)
                                        else:  # flushed or both way
                                            if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # flushed
                                                self.space_available_web = self.call_helper.lever_arm[-2] - self.call_helper.lever_arm[-1]
                                            else:  # both-way extended
                                                if (self.bolt_row / 2) <= 3:
                                                    rows_inside_D = self.bolt_row - 2  # one row each outside top and bottom flange
                                                else:
                                                    rows_inside_D = self.bolt_row - 4  # two rows each outside top and bottom flange

                                                self.space_available_web = self.beam_D - (2 * self.beam_tf) - (2 * self.end_distance_provided) - \
                                                                           ((rows_inside_D - 2) * self.pitch_distance_provided)

                                        # step 3: adding rows to satisfy detailing criteria
                                        if self.space_available_web > self.pitch_distance_max:
                                            self.bolt_row_web = round_up(self.space_available_web / self.pitch_distance_max, 1) - 1
                                        else:
                                            self.bolt_row_web = 0

                                        # step 4: re-design the connection if more rows are added
                                        if self.bolt_row_web >= 1:

                                            self.pitch_distance_web = self.space_available_web / (self.bolt_row_web + 1)

                                            # run the bolt and end plate check function from the helper class
                                            self.design_bolt = self.call_helper.perform_bolt_design(self.endplate_type, self.supported_section,
                                                                                                    self.gamma_m0,
                                                                                                    self.bolt_column, self.bolt_row, self.bolt_row_web,
                                                                                                    self.bolt_diameter_provided,
                                                                                                    self.bolt_grade_provided, self.load_moment_effective,
                                                                                                    self.end_distance_provided,
                                                                                                    self.pitch_distance_provided, self.pitch_distance_web,
                                                                                                    self.beta, self.proof_stress, self.dp_plate_fy,
                                                                                                    self.plate_thickness, self.dp_plate_fu,
                                                                                                    self.load_shear)

                                            # status of the helper file - bolt design check, with web bolts
                                            if self.call_helper.helper_file_design_status == True:
                                                self.design_status = True
                                                break
                                            else:
                                                self.design_status = False

                                        # if status of the helper file is True and web bolts are not required
                                        else:
                                            self.design_status = True
                                            break

                                    # status of the helper file - bolt design check, without web bolts
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

                                    # self.bolt_row_web = 2#added for 3D
                                    # self.bolt_numbers = self.bolt_column * (self.bolt_row + self.bolt_row_web)#added for 3D

                                    self.bolt_row = self.call_helper.bolt_row
                                    self.bolt_numbers = self.bolt_column * (self.bolt_row + self.bolt_row_web)
                                    # self.bolt_numbers = self.bolt_column * (self.bolt_row + self.bolt_row_web)#added for 3D

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

                                    # checker for bolt column-row selection loop
                                    if self.call_helper.helper_file_design_status == True:
                                        self.design_status = True
                                        break
                                    else:
                                        self.design_status = False

                            # checker for the bolt dia-grade combination selection loop
                            if self.call_helper.helper_file_design_status == True:
                                self.design_status = True
                                break
                            else:
                                self.design_status = False

                    # checker for the plate thickness selection loop
                    if self.call_helper.helper_file_design_status == True:
                        self.design_status = True
                        break
                    else:
                        self.design_status = False

            # design status associated with the helper status
            # self.design_status_list.append(self.design_status)
            if (i == self.plate_thickness_list[-1]) and (self.design_status == False):
                self.design_status_list.append(self.design_status)

        else:
            self.design_status = False

        # results of overall safe design

        if len(self.plate_thickness_list) != 0 and len(combined_list) != 0:

            # Log messages for helper file
            if not self.call_helper.flange_capacity_status:
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

            if not self.call_helper.plate_design_status:
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

            if not self.call_helper.bolt_tension_design_status:
                logger.error("[Bolt Design] The bolt of {} mm diameter and {} grade fails the tension check".
                             format(self.bolt_diameter_provided, self.bolt_grade_provided))
                logger.error(
                    "Total tension demand on bolt (due to direct tension + prying action) is {} kN and exceeds the bolt tension "
                    "capacity ({} kN)".format(round(self.call_helper.bolt_tension_demand, 2), self.call_helper.bolt_tension_capacity))
                logger.info("Re-designing the connection with a bolt of higher grade and/or diameter")
            else:
                logger.info("[Bolt Design] The bolt of {} mm diameter and {} grade passes the tension check".
                            format(self.bolt_diameter_provided, self.bolt_grade_provided))
                logger.info("Total tension demand on bolt (due to direct tension + prying action) is {} kN and the bolt tension "
                            "capacity is ({} kN)".format(round(self.call_helper.bolt_tension_demand, 2),
                                                         self.call_helper.bolt_tension_capacity))

            if not self.call_helper.bolt_design_combined_check_status:
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

            # shear design
            self.bolt_shear_demand = self.call_helper.bolt_shear_demand
            self.bolt_shear_capacity = self.call_helper.bolt_shear_capacity
            self.bolt_bearing_capacity = self.call_helper.bolt_bearing_capacity
            self.bolt_capacity = self.call_helper.bolt_capacity

            # tension design
            self.tension_critical_bolt = round(self.call_helper.t_1, 2)
            self.prying_critical_bolt = self.call_helper.prying_force
            if math.isnan(self.prying_critical_bolt):
                self.design_status = False
                self.design_status_list.append(self.design_status)

            self.tension_demand_critical_bolt = round(self.call_helper.bolt_tension_demand, 2)
            if math.isnan(self.tension_demand_critical_bolt):
                self.design_status = False
                self.design_status_list.append(self.design_status)

            self.tension_capacity_critical_bolt = self.call_helper.bolt_tension_capacity

            self.combined_capacity_critical_bolt = self.call_helper.bolt_combined_check_UR
            if math.isnan(self.combined_capacity_critical_bolt):
                self.design_status = False
                self.design_status_list.append(self.design_status)

            # End Plate
            self.ep_moment_capacity = round(self.call_helper.mp_plate * 1e-6, 2)
            if math.isnan(self.ep_moment_capacity):
                self.design_status = False
                self.design_status_list.append(self.design_status)

            if self.endplate_type == 'Flushed - Reversible Moment':
                self.ep_height_provided = self.beam_D + 25

            elif self.endplate_type == 'Extended One Way - Irreversible Moment':
                if self.bolt_row <= 4:  # 1 row above tension flange
                    self.ep_height_provided = self.beam_D + 12.5 + (2 * self.end_distance_provided)
                else:  # 2 rows above tension flange which is maximum allowable
                    self.ep_height_provided = self.beam_D + 12.5 + (2 * self.end_distance_provided) + self.pitch_distance_provided

            else:
                if self.bolt_row < 8:  # 1 row outside tension and compression flange
                    self.ep_height_provided = self.beam_D + (2 * (2 * self.end_distance_provided))
                else:  # 2 rows outside tension and compression flange which is maximum allowable
                    self.ep_height_provided = self.beam_D + (2 * (2 * self.end_distance_provided)) + (
                            2 * self.pitch_distance_provided)

            # number of bolts
            self.bolt_row += self.bolt_row_web
            self.bolt_numbers = self.bolt_column * self.bolt_row

            # for failed design report
            if not self.design_status:
                if self.bolt_column == 0:
                    self.bolt_column = self.last_column
                    self.bolt_numbers = self.bolt_column * self.bolt_row

        if len(self.plate_thickness_list) == 0 or len(combined_list) == 0:
            self.last_column = 0
            self.bolt_column = 0
            self.bolt_row = 0
            self.bolt_numbers = self.bolt_column * self.bolt_row

    def design_stiffener(self):
        """ design stiffener for the connection """

        if (len(self.plate_thickness_list) != 0) and (self.bolt_row != 0) and (self.bolt_column != 0):

            if self.endplate_type == 'Flushed - Reversible Moment':
                self.stiffener_height = (self.ep_width_provided - self.beam_tw) / 2  # mm
                self.stiffener_length = 2 * self.stiffener_height  # mm
            else:
                if self.endplate_type == 'Extended Both Ways - Reversible Moment':
                    self.stiffener_height = (self.ep_height_provided - self.beam_D) / 2  # mm
                else:
                    self.stiffener_height = self.ep_height_provided - self.beam_D - 12.5  # mm

                self.stiffener_length = round_up((self.stiffener_height / math.tan(math.radians(30))), 2)  # mm

            self.stiffener_thickness = round_up(self.beam_tw, 2)  # mm

    def design_weld(self):
        """ design fillet weld at web for the connection """
        if (len(self.plate_thickness_list) != 0) and (self.bolt_row != 0) and (self.bolt_column != 0):

            # weld strength
            self.weld_fu = min(self.web_weld.fu, self.plate.fu)

            # 1: Weld design for web to end plate connection
            self.weld_length_web = 2 * (self.beam_D - (2 * self.beam_tf) - (2 * self.beam_r1) - 20)  # mm, on either side of the web
            self.weld_size_web = (self.load_shear * 1e3 * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_length_web * self.weld_fu)  # mm
            self.weld_size_web = round_up(self.weld_size_web, 2)

            self.web_weld.set_min_max_sizes(self.plate_thickness, self.beam_tw, special_circumstance=False, fusion_face_angle=90)

            self.weld_size_web = max(self.weld_size_web, round_up(self.web_weld.min_size, 2))  # mm

            # combination of stress check
            self.f_a = round((self.load_axial * 1e3) / (0.7 * self.weld_size_web * self.weld_length_web), 2)  # N/mm^2, stress due to axial force
            self.q = round((self.load_shear * 1e3) / (0.7 * self.weld_size_web * self.weld_length_web), 2)  # N/mm^2, stress due to shear force

            self.f_e = round(math.sqrt(self.f_a + (3 * self.q ** 2)), 2)  # N/mm^2, stress due to combined load

            self.allowable_stress = round(self.weld_fu / (math.sqrt(3) * self.gamma_mw), 2)  # N/mm^2, allowable stress in the weld

            # allowable stress check
            if self.f_e > self.allowable_stress:
                logger.error("[Weld Design] The weld at web fails in the combined axial and shear design check")
                logger.info("Provide groove weld at the web")

            # 2: Weld design for stiffeners
            if self.endplate_type == 'Flushed - Reversible Moment':
                self.stiffener_weld.set_min_max_sizes(max(self.plate_thickness, self.stiffener_thickness, self.beam_tw),
                                                      min(self.plate_thickness, self.stiffener_thickness, self.beam_tw),
                                                      special_circumstance=False, fusion_face_angle=90)
            else:
                self.stiffener_weld.set_min_max_sizes(max(self.plate_thickness, self.stiffener_thickness, self.beam_tf),
                                                      min(self.plate_thickness, self.stiffener_thickness, self.beam_tf),
                                                      special_circumstance=False, fusion_face_angle=90)
            self.weld_size_stiffener = round_up(self.stiffener_weld.min_size, 2)  # mm

        # end of calculation

        # overall design status
        for status in self.design_status_list:
            if status is False:
                self.design_status = False
                break
            else:
                self.design_status = True

        if self.design_status:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall beam to beam end plate splice connection design is SAFE")
            logger.info(": ========== End Of Design ============")
        else:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall beam to beam end plate splice connection design is UNSAFE")
            logger.info(": ========== End Of Design ============")

        # create design report

    def save_design(self, popup_summary):
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")

        if self.supported_section.flange_slope == 90:
            image = "Parallel_Beam"
        else:
            image = "Slope_Beam"
        self.report_supporting = {KEY_DISP_SEC_PROFILE: "ISection",
                                  KEY_DISP_BEAMSEC_REPORT: self.supported_section.designation,
                                  KEY_DISP_MATERIAL: self.supported_section.material,
                                  KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.supported_section.fu,
                                  KEY_DISP_YIELD_STRENGTH_REPORT: self.supported_section.fy,
                                  KEY_REPORT_MASS: self.supported_section.mass,
                                  KEY_REPORT_AREA: round(self.supported_section.area, 2),
                                  KEY_REPORT_DEPTH: self.supported_section.depth,
                                  KEY_REPORT_WIDTH: self.supported_section.flange_width,
                                  KEY_REPORT_WEB_THK: self.supported_section.web_thickness,
                                  KEY_REPORT_FLANGE_THK: self.supported_section.flange_thickness,
                                  KEY_DISP_FLANGE_S_REPORT: self.supported_section.flange_slope,
                                  KEY_REPORT_R1: self.supported_section.root_radius,
                                  KEY_REPORT_R2: self.supported_section.toe_radius,
                                  KEY_REPORT_IZ: round(self.supported_section.mom_inertia_z * 1e-4, 2),
                                  KEY_REPORT_IY: round(self.supported_section.mom_inertia_y * 1e-4, 2),
                                  KEY_REPORT_RZ: round(self.supported_section.rad_of_gy_z * 1e-1, 2),
                                  KEY_REPORT_RY: round(self.supported_section.rad_of_gy_y * 1e-1, 2),
                                  KEY_REPORT_ZEZ: round(self.supported_section.elast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZEY: round(self.supported_section.elast_sec_mod_y * 1e-3, 2),
                                  KEY_REPORT_ZPZ: round(self.supported_section.plast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZPY: round(self.supported_section.plast_sec_mod_y * 1e-3, 2)}

        self.report_input = \
            {KEY_MAIN_MODULE: self.mainmodule,
             KEY_MODULE: KEY_DISP_BB_EP_SPLICE,
             KEY_CONN: self.connectivity,
             KEY_DISP_ENDPLATE_TYPE: self.endplate_type,
             KEY_DISP_MOMENT: self.input_moment,
             KEY_DISP_SHEAR: self.input_shear_force,
             KEY_DISP_AXIAL: self.input_axial_force,

             "Beam Section - Mechanical Properties": "TITLE",
             "Section Details": self.report_supporting,

             "Plate Details - Input and Design Preference": "TITLE",
             KEY_DISP_PLATETHK: str(list(np.int_(self.plate.thickness))),
             KEY_DISP_MATERIAL: self.plate.material,
             KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.plate.fu,
             KEY_DISP_YIELD_STRENGTH_REPORT: self.plate.fy,

             "Bolt Details - Input and Design Preference": "TITLE",
             KEY_DISP_D: str(list(np.int_(self.bolt.bolt_diameter))),
             KEY_DISP_GRD: str(self.bolt.bolt_grade),
             KEY_DISP_TYP: self.bolt.bolt_type,
             KEY_DISP_BOLT_PRE_TENSIONING: self.bolt.bolt_tensioning,
             KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
             KEY_DISP_DP_BOLT_SLIP_FACTOR_REPORT: self.bolt.mu_f,

             "Weld Details - Input and Design Preference": "TITLE",
             KEY_DISP_DP_WELD_FAB: self.web_weld.fabrication,
             KEY_DISP_DP_WELD_MATERIAL_G_O_REPORT: self.web_weld.fu,
             KEY_DISP_BEAM_FLANGE_WELD_TYPE: "Groove Weld",
             KEY_DISP_BEAM_WEB_WELD_TYPE: "Fillet Weld",
             KEY_DISP_STIFFENER_WELD_TYPE: "Fillet Weld",

             "Detailing - Design Preference": "TITLE",
             KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
             KEY_DISP_DP_DETAILING_GAP_BEAM: self.plate.gap,
             KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM: self.bolt.corrosive_influences,
             }

        self.report_check = []

        # Assiging parameters
        if (len(self.plate_thickness_list) != 0) and (self.bolt_row != 0):
            self.bolt_conn_plates_t_fu_fy = []
            self.bolt_conn_plates_t_fu_fy.append((self.plate_thickness, 0, 0))

        self.h = (self.beam_D - (2 * self.beam_tf))

        # CHECK 1: MEMBER CAPACITY
        t1 = ('SubSection', 'Member Capacity', '|p{4.5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        t1 = (KEY_DISP_SHEAR_CAPACITY, '',
              cl_8_4_shear_yielding_capacity_member(h=self.h, t=self.supported_section.web_thickness,
                                                    f_y=self.supported_section.fy, gamma_m0=self.gamma_m0,
                                                    V_dg=round(self.supported_section_shear_capa, 2), multiple=0.6),
              'Restricted to low shear')

        self.report_check.append(t1)

        # percent = 1
        if self.input_moment < self.supported_section_mom_capa_m_zz:
            percent = 0.5
        else:
            percent = 1
        t1 = (KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY, '',
              cl_8_2_1_2_plastic_moment_capacity(beta_b=1,
                                                        Z_p=self.supported_section.plast_sec_mod_z,
                                                        f_y=self.supported_section.fy,
                                                        gamma_m0=self.gamma_m0,
                                                        Pmc=round(self.supported_section_mom_capa_m_zz, 2), supporting_or_supported='NA'), 'V < 0.6 Vdy')
        self.report_check.append(t1)

        t1 = ('SubSection', 'Load Consideration', '|p{3.5cm}|p{5.2cm}|p{5.3cm}|p{1.5cm}|')
        self.report_check.append(t1)
        self.load_shear_min = min((0.15 * self.supported_section_shear_capa), 40)
        self.load_moment_min = (0.5 * self.supported_section_mom_capa_m_zz)

        t1 = (KEY_DISP_SHEAR, display_prov(self.input_shear_force, "V_y"),
              prov_shear_force(shear_input=self.input_shear_force, min_sc=round(self.load_shear_min, 2),
                              app_shear_load=round(self.load_shear, 2), shear_capacity_1=self.supported_section_shear_capa),
              get_pass_fail(self.input_shear_force, self.load_shear, relation='leq'))
        self.report_check.append(t1)

        t1 = (KEY_DISP_AXIAL, '', display_prov(self.load_axial, "P_x"), "OK")
        self.report_check.append(t1)

        t1 = (KEY_DISP_MOMENT, display_prov(self.input_moment, "M_z"),
              prov_moment_load(moment_input=self.input_moment, min_mc=round(self.load_moment_min, 2),
                               app_moment_load=round(self.load_moment, 2),
                               moment_capacity=round(self.supported_section_mom_capa_m_zz, 2), moment_capacity_supporting=0.0, type='EndPlateType'),
              get_pass_fail(self.input_moment, self.load_moment, relation='leq'))

        self.report_check.append(t1)

        t1 = ("Effective Bending Moment (kNm)", '',
              effective_bending_moment_ep(self.load_moment, self.load_axial, self.load_moment_effective, self.beam_D, self.beam_tf), "OK")

        self.report_check.append(t1)

        if (len(self.plate_thickness_list) != 0) and (self.bolt_row != 0):

            # CHECK 2: BOLT CHECKS
            t1 = ('SubSection', ' Bolt Optimization', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_D_PROVIDED, "Bolt Diameter Optimization", display_prov(int(self.bolt_diameter_provided), "d"),
                  'Pass' if self.design_status else 'Fail')
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_GRD_PROVIDED, "Bolt Property Class Optimization", self.bolt_grade_provided, 'Pass' if self.design_status else 'Fail')
            self.report_check.append(t1)

            t1 = (KEY_DISP_BOLT_HOLE, " ", display_prov(self.bolt_hole_diameter, "d_0"), 'OK')
            self.report_check.append(t1)

            # t1 = (KEY_DISP_PLTHICK, '', int(self.plate_thickness), 'Pass')
            # self.report_check.append(t1)

            t6 = (DISP_NUM_OF_COLUMNS, '', display_prov(self.bolt_column, "n_c"), 'Pass' if self.design_status else 'Fail')
            self.report_check.append(t6)

            t7 = (DISP_NUM_OF_ROWS, '', display_prov(self.bolt_row, "n_r"), 'Pass' if self.design_status else 'Fail')
            self.report_check.append(t7)

            t1 = (KEY_OUT_DISP_NO_BOLTS, '', display_prov(self.bolt_numbers, "n = n_r X n_c"), 'Pass' if self.design_status else 'Fail')
            self.report_check.append(t1)

            # CHECK: Detailing
            connected_plates_t_fu_fy = [(self.plate_thickness, self.plate.fu, self.plate.fy),
                                        (max(self.beam_tf, self.beam_tw), self.supported_section.fu, self.supported_section.fy)]

            self.bolt.calculate_bolt_spacing_limits(self.bolt_diameter_provided, connected_plates_t_fu_fy, n=1)

            t1 = ('SubSection', ' Detailing', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (DISP_MIN_PITCH, cl_10_2_2_min_spacing(self.bolt_diameter_provided, parameter='pitch'),
                  self.pitch_distance_provided,
                  get_pass_fail(self.bolt.min_pitch, self.pitch_distance_provided, relation='leq'))
            self.report_check.append(t1)

            t7 = (DISP_MAX_PITCH, cl_10_2_3_1_max_spacing([self.plate_thickness, self.plate_thickness], parameter='pitch'), self.pitch_distance_provided,
                  get_pass_fail(self.bolt.max_spacing, self.pitch_distance_provided, relation='geq'))
            self.report_check.append(t7)

            if self.bolt_column > 2:
                t1 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(self.bolt_diameter_provided, parameter='gauge'),
                      self.gauge_distance_provided,
                      get_pass_fail(self.bolt.min_pitch, self.gauge_distance_provided, relation='leq'))
                self.report_check.append(t1)

                t7 = (DISP_MAX_GAUGE, cl_10_2_3_1_max_spacing([self.plate_thickness, self.plate_thickness], parameter='gauge'),
                      self.gauge_distance_provided,
                      get_pass_fail(self.bolt.max_spacing, self.gauge_distance_provided, relation='geq'))
                self.report_check.append(t7)

            t3 = (DISP_MIN_END, cl_10_2_4_2_min_edge_end_dist(self.bolt_hole_diameter, self.bolt.edge_type, parameter='end_dist'),
                  self.end_distance_provided,
                  get_pass_fail(self.bolt.min_end_dist, self.end_distance_provided, relation='leq'))
            self.report_check.append(t3)

            t3 = (DISP_MAX_END, cl_10_2_4_3_max_edge_end_dist([(self.plate_thickness, self.plate.fu, self.plate.fy),
                                                               (self.plate_thickness, self.plate.fu, self.plate.fy)],
                                                              corrosive_influences=self.bolt.corrosive_influences, parameter='end_dist'),
                  self.edge_distance_provided,
                  get_pass_fail(self.bolt.min_edge_dist, self.edge_distance_provided, relation='leq'))
            self.report_check.append(t3)

            t3 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(self.bolt_hole_diameter, self.bolt.edge_type, parameter='edge_dist'),
                  self.edge_distance_provided,
                  get_pass_fail(self.bolt.min_end_dist, self.edge_distance_provided, relation='leq'))
            self.report_check.append(t3)

            t3 = (DISP_MAX_EDGE, cl_10_2_4_3_max_edge_end_dist([(self.plate_thickness, self.plate.fu, self.plate.fy),
                                                               (self.plate_thickness, self.plate.fu, self.plate.fy)],
                                                               corrosive_influences=self.bolt.corrosive_influences, parameter='edge_dist'),
                  self.edge_distance_provided,
                  get_pass_fail(self.bolt.min_edge_dist, self.edge_distance_provided, relation='leq'))
            self.report_check.append(t3)

            t1 = (DISP_CS_GAUGE, '', self.gauge_cs_distance_provided, 'Pass')
            self.report_check.append(t1)

            t1 = ('SubSection', 'Critical Bolt Design', '|p{2.5cm}|p{6.7cm}|p{6.3cm}|p{1cm}|')
            self.report_check.append(t1)

            if self.bolt_column == 0:
                self.bolt_shear_demand = 'nan'

            if self.bolt.bolt_type == TYP_BEARING:
                bolt_bearing_capacity_kn = round(self.bolt_bearing_capacity, 2)

                t1 = (KEY_OUT_DISP_BOLT_SHEAR, '', cl_10_3_3_bolt_shear_capacity(self.bolt_fu, 1,
                                                                                 self.bolt.bolt_net_area,
                                                                                 self.gamma_mb,
                                                                                 round(self.bolt_shear_capacity, 2)), 'OK')
                self.report_check.append(t1)

                t3 = (KEY_DISP_KB, '', cl_10_3_4_calculate_kb(self.end_distance_provided, self.pitch_distance_provided, self.bolt_hole_diameter,
                                                              self.bolt_fu, self.supported_section.fu), 'OK')
                self.report_check.append(t3)

                t2 = (KEY_OUT_DISP_BOLT_BEARING, '', cl_10_3_4_bolt_bearing_capacity(round(self.bolt.kb, 2),
                                                                                     self.bolt_diameter_provided,
                                                                                     [(self.plate_thickness, self.plate.fu, self.plate.fy),
                                                                                      (self.plate_thickness, self.plate.fu, self.plate.fy)],
                                                                                     self.gamma_mb,
                                                                                     bolt_bearing_capacity_kn), 'OK')
                self.report_check.append(t2)

                t3 = ('Bolt Capacity (kN)', '',
                      cl_10_3_2_bolt_capacity(round(self.bolt_shear_capacity, 2), bolt_bearing_capacity_kn,
                                              round(self.bolt_capacity / self.call_helper.beta_lg, 2)),
                      '')
                self.report_check.append(t3)

                t3 = (KEY_OUT_LARGE_GRIP, '', large_grip_length(self.plate_thickness, self.plate_thickness, self.call_helper.grip_length,
                                                                           self.bolt_diameter_provided, self.call_helper.beta_lg),
                      get_pass_fail(self.call_helper.grip_length, 8 * self.bolt_diameter_provided, relation='leq'))
                self.report_check.append(t3)

                t3 = (KEY_OUT_BOLT_CAPACITY_REDUCED, '',
                      shear_capa_post_large_grip_length_red(self.call_helper.beta_lg, self.bolt_capacity),
                      'OK')
                self.report_check.append(t3)

                t3 = ('Shear Demand (kN)', bolt_shear_demand(V=self.load_shear, n_bolts=self.bolt_numbers,
                                                              V_sb=self.bolt_shear_demand, type='Bearing Bolt'),
                      'Vdb = ' + str(round(self.bolt_capacity, 2)) + '',
                      get_pass_fail(self.bolt_shear_demand, round(self.bolt_capacity, 2), relation='leq'))
                self.report_check.append(t3)
            else:
                t4 = (KEY_OUT_DISP_BOLT_SLIP_DR, bolt_shear_demand(V=self.load_shear, n_bolts=self.bolt_numbers,
                                                                    V_sb=self.bolt_shear_demand),
                      cl_10_4_3_HSFG_bolt_capacity(mu_f=self.bolt.mu_f, n_e=1,K_h=1,
                                                                               fub=self.bolt_fu,
                                                                               Anb=self.bolt.bolt_net_area,
                                                                               gamma_mf=self.bolt.gamma_mf,
                                                                               capacity=round(self.bolt_capacity, 2)),
                      'Fail' if self.bolt_column == 0 else get_pass_fail(self.bolt_shear_demand, round(self.bolt_capacity, 2), relation='leq'))
                self.report_check.append(t4)

            t6 = (KEY_DISP_LEVER_ARM, lever_arm_end_plate(self.call_helper.lever_arm, self.bolt_row, ep_type=self.endplate_type), '',
                  'Pass' if self.design_status else 'Fail')
            self.report_check.append(t6)

            leverarm = self.call_helper.lever_arm
            r1 = leverarm[0]
            r_sum = 0
            for j in leverarm:
                r_sum += j**2 / r1

            if len(leverarm) >= 3:
                r_3 = leverarm[2]
            else:
                r_3 = 0.0
            if len(leverarm) >= 4:
                r_4 = leverarm[3]
            else:
                r_4 = 0.0

            if self.bolt_column == 0:
                t_ba = 0.0
            else:
                t_ba = round(self.tension_critical_bolt, 2)

            t6 = (KEY_OUT_DISP_CRITICAL_BOLT_TENSION, tension_critical_bolt_prov(M=self.load_moment_effective, t_ba=t_ba,
                                                                           n_c=self.bolt_column, r_1=round(r1, 2), n_r=self.bolt_row,
                                                                           r_i=round(r_sum, 2), n=self.bolt_row, r_3=r_3, r_4=r_4,
                                                                           type=self.endplate_type),
                  "", 'Fail' if self.bolt_column == 0 else "OK")
            self.report_check.append(t6)

            if self.bolt.bolt_tensioning == 'Pretensioned':
                beta = 1
            else:
                beta = 2

            l_v = round(self.call_helper.lv, 2)
            l_e = round(self.call_helper.le, 2)
            l_e2 = round(self.call_helper.le_2, 2)
            T_e = round(self.call_helper.t_1, 2)
            b_e = round(self.call_helper.b_e, 2)
            t = int(self.call_helper.plate_thickness)

            t1 = (KEY_OUT_DISP_BOLT_PRYING_FORCE_EP, cl_10_4_7_prying_force(l_v, l_e, l_e2, T_e, self.beta, self.proof_stress, b_e, t, self.end_distance_provided,
                                                              self.beam_r1, self.dp_plate_fy, self.bolt_fu, self.proof_stress, self.beam_bf,
                                                              self.bolt_column, self.prying_critical_bolt, eta=1.5), '',
                  'OK' if self.design_status else 'Fail')
            self.report_check.append(t1)

            if self.bolt.bolt_type == "Bearing Bolt":
                t1 = (KEY_OUT_DISP_BOLT_TENSION_DEMAND, total_bolt_tension_force(T_ba=round(self.call_helper.t_1, 2), Q=round(self.prying_critical_bolt, 2),
                                                                      T_b=round(self.tension_demand_critical_bolt, 2), bolt_type=self.bolt.bolt_type),
                      cl_10_3_5_bearing_bolt_tension_resistance(self.bolt_fu, self.dp_bolt_fy, self.bolt.bolt_shank_area, self.bolt.bolt_net_area,
                                                                round(self.tension_capacity_critical_bolt, 2), fabrication=self.dp_weld_fab),
                      get_pass_fail(round(self.tension_demand_critical_bolt, 2), round(self.tension_capacity_critical_bolt, 2), relation='lesser'))
            else:
                t1 = (KEY_OUT_DISP_BOLT_TENSION_DEMAND, total_bolt_tension_force(T_ba=round(self.call_helper.t_1, 2), Q=round(self.prying_critical_bolt, 2),
                                                                      T_b=round(self.tension_demand_critical_bolt, 2), bolt_type=self.bolt.bolt_type),
                      cl_10_4_5_hsfg_bolt_tension_resistance(self.bolt_fu, self.dp_bolt_fy, self.bolt.bolt_shank_area, self.bolt.bolt_net_area,
                                                                round(self.tension_capacity_critical_bolt, 2), fabrication=self.dp_weld_fab),
                      get_pass_fail(round(self.tension_demand_critical_bolt, 2), round(self.tension_capacity_critical_bolt, 2), relation='lesser'))

            self.report_check.append(t1)

            if self.bolt.bolt_type == TYP_BEARING:
                t1 = ('Combined Capacity, (I.R)', required_IR_or_utilisation_ratio(IR=1),
                      cl_10_3_6_bearing_bolt_combined_shear_and_tension( round(self.bolt_shear_demand,2) ,
                                                                        round(self.bolt_capacity,2),
                                                                         round(self.tension_demand_critical_bolt,2),
                                                                         round(self.tension_capacity_critical_bolt,2),
                                                                         round(self.combined_capacity_critical_bolt,2)),
                get_pass_fail(1, round(self.combined_capacity_critical_bolt,2) , relation="greater"))
                self.report_check.append(t1)
            else:
                t1 = ('Combined Capacity, (I.R.)', required_IR_or_utilisation_ratio(IR=1),
                cl_10_4_6_friction_bolt_combined_shear_and_tension(round(self.bolt_shear_demand, 2),
                                                                  round(self.bolt_capacity, 2),
                                                                  round(self.tension_demand_critical_bolt, 2),
                                                                  round(self.tension_capacity_critical_bolt, 2),
                                                                  round(self.combined_capacity_critical_bolt, 2)),
                get_pass_fail(1, round(self.combined_capacity_critical_bolt, 2), relation="greater"))
                self.report_check.append(t1)

            # Check: Reaction at compression flange
            t1 = ('SubSection', 'Compression Flange Check', '|p{3.5cm}|p{4cm}|p{7.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = ('Tension in Bolt Rows (kN)', '', tension_list(self.call_helper.tension), 'OK')
            self.report_check.append(t1)

            tension_sum = sum(self.call_helper.tension)
            if self.bolt_column == 0:
                r_c = 0.0
            else:
                r_c = self.call_helper.r_c

            t1 = ('Reaction at Compression Flange (kN)', reaction_compression_flange(r_c, self.bolt_column, self.bolt_row, round(tension_sum, 2)),
                  compression_flange_capacity(self.beam_bf, self.beam_tf, self.supported_section.fy, self.gamma_m0, self.call_helper.flange_capacity),
                  get_pass_fail(self.call_helper.flange_capacity, r_c, relation="geq"))
            self.report_check.append(t1)

            # CHECK 2: END PLATE CHECKS #
            t1 = ('SubSection', '  End Plate Checks', '|p{3.5cm}|p{4cm}|p{7.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t1 = (KEY_OUT_DISP_PLATE_HEIGHT, '', bb_endplate_height_prov(beam_D=self.supported_section.depth,
                                                                         end_distance_provided=self.end_distance_provided,
                                                                         pitch_distance_provided=self.pitch_distance_provided,
                                                                         height_plate=round(self.ep_height_provided, 2),
                                                                         bolt_row=self.bolt_row,
                                                                         type=self.endplate_type),
                  get_pass_fail(self.supported_section.depth, round(self.ep_height_provided, 2), relation="leq"))
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_PLATE_WIDTH, "", bb_endplate_width_prov(B_ep= round(self.ep_width_provided,2),
                                                                       B=self.supported_section.flange_width),
                  get_pass_fail(self.supported_section.flange_width, round(self.ep_width_provided,2), relation="leq"))
            self.report_check.append(t1)

            t1 = ('Moment at Critical Section (kNm)', '', moment_ep(t_1=round(self.call_helper.t_1, 2), lv=round(self.call_helper.lv, 2),
                                                          Q=round(self.call_helper.prying_force, 2), le=round(self.call_helper.le, 2),
                                                          mp_plate=round(self.ep_moment_capacity, 2)), "OK")

            self.report_check.append(t1)

            t1 = (KEY_DISP_PLATE_THICK,
                  end_plate_thk_req(M_ep=round(self.ep_moment_capacity,2), b_eff=round(self.call_helper.b_e, 2), f_y=self.dp_plate_fy,
                                    gamma_m0=self.gamma_m0, t_p=self.call_helper.plate_thickness_req, t_b=0, q=0, l_e=0, l_v=0, f_o=0, b_e=0, beta=0,
                                    module='BB_EP'),
                  int(self.plate_thickness),
                  get_pass_fail(self.call_helper.plate_thickness_req, self.plate_thickness, relation="leq"))
            self.report_check.append(t1)

            t1 = (KEY_DISP_MOM_CAPACITY, round(self.ep_moment_capacity, 2),
                  end_plate_moment_capacity(M_ep=round(self.call_helper.plate_moment_capacity, 2), b_eff=round(self.call_helper.b_e, 2),
                                            f_y=self.dp_plate_fy, gamma_m0=self.gamma_m0, t_p=self.plate_thickness),
                  get_pass_fail(self.ep_moment_capacity, self.call_helper.plate_moment_capacity, relation="leq"))
            self.report_check.append(t1)

            # CHECK 2: STIFFENER CHECKS #
            if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:
                t1 = ('SubSection', 'Longitudinal Stiffener Design', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
            else:
                t1 = ('SubSection', 'Stiffener Design', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_STIFFENER_WIDTH if self.endplate_type == VALUES_ENDPLATE_TYPE[0] else KEY_OUT_DISP_STIFFENER_HEIGHT, ' ',
                  stiffener_height_prov(b_ep=self.ep_width_provided, t_w=self.supported_section.web_thickness, h_ep=self.ep_height_provided,
                                        D=self.supported_section.depth, h_sp=round_down(self.stiffener_height, 2), type=self.endplate_type), 'Pass')
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_STIFFENER_LENGTH, ' ', stiffener_length_prov(h_sp=round_down(self.stiffener_height, 2),
                                                                            l_sp=round_down(self.stiffener_length, 2),
                                                                            type=self.endplate_type), 'Pass')
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_STIFFENER_THICKNESS, display_prov(self.beam_tw, "t"), display_prov(self.stiffener_thickness, "t_{st}"), 'Pass')
            self.report_check.append(t1)

            t1 = (DISP_WELD_SIZE, round(self.stiffener_weld.min_size), 'tw = ' + str(self.weld_size_stiffener) + '', 'Pass')
            self.report_check.append(t1)

            # ##################
            # # Weld Checks
            # ##################
            weld_conn_plates_fu = [self.dp_plate_fu, self.supported_section.fu, self.web_weld.fu]
            weld_conn_plates_tk = [self.plate_thickness, self.supported_section.web_thickness]

            t1 = ('SubSection', 'Weld Design - Beam Web to End Plate Connection', '|p{3.5cm}|p{5.3cm}|p{6.5cm}|p{1.2cm}|')
            self.report_check.append(t1)

            t1 = (DISP_WELD_STRENGTH_MPA, weld_fu(self.web_weld.fu, self.plate.fu), weld_fu_provided(self.weld_fu),
                  get_pass_fail(max(self.web_weld.fu, self.plate.fu), self.weld_fu, relation="geq"))
            self.report_check.append(t1)

            t1 = ('Total Weld Length (mm)', "", weld_length_web_prov(beam_D=self.supported_section.depth, beam_tf=self.supported_section.flange_thickness,
                                                                     beam_r1=self.supported_section.root_radius,
                                                                     L_weld=round_down(self.weld_length_web, 2)), "")
            self.report_check.append(t1)

            self.weld_size_web1 = round((self.load_shear * 1e3 * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_length_web * self.weld_fu), 2)  # mm

            t1 = (DISP_WELD_SIZE, weld_size_ep_web_req(load_shear=self.load_shear, gamma_mw=self.gamma_mw,
                                                       weld_length_web=round_down(self.weld_length_web, 2), fu=self.weld_fu,
                                                       weld_size_web=self.weld_size_web1), self.weld_size_web,
                  get_pass_fail(self.weld_size_web1, self.weld_size_web, relation="leq"))
            self.report_check.append(t1)

            t1 = (DISP_MIN_WELD_SIZE, cl_10_5_2_3_table_21_min_fillet_weld_size_required([self.plate_thickness, self.beam_tw],
                                                                                            round(self.web_weld.min_size, 2)),
                  min_weld_size_ep_web_prov(weld_size_web=self.weld_size_web1, weld_size_web_provided=self.weld_size_web,
                                            min_size=round(self.web_weld.min_size, 2)),
                  get_pass_fail(max(self.weld_size_web1, self.web_weld.min_size), self.weld_size_web, relation="leq"))
            self.report_check.append(t1)

            t1 = (DISP_MAX_WELD_SIZE,  cl_10_5_3_1_max_weld_size_v2([self.plate_thickness, self.beam_tw], round(self.web_weld.max_size, 2)),
                  max_weld_size_ep_web_prov(weld_size_web=self.weld_size_web, max_size=round(self.web_weld.max_size, 2)),
                  get_pass_fail(self.web_weld.max_size, self.weld_size_web, relation="geq"))
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_WELD_NORMAL_STRESS, "", f_a_stress_due_to_axial_force(A_f=self.load_axial, t_w=self.weld_size_web,
                                                                                     L_weld=round_down(self.weld_length_web, 2),
                                                                                     f_a=round(self.f_a, 2)), "OK")
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_WELD_SHEAR_STRESS, "", q_stress_due_to_shear_force(V=self.load_shear, t_w=self.weld_size_web,
                                                                                  L_weld=round_down(self.weld_length_web, 2), q=self.q), "OK")
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_WELD_STRESS_EQUIVALENT, f_e_weld_stress_due_to_combined_load(f_a=self.f_a, f_e=self.f_e, q=self.q),
                  cl_10_5_7_1_1_weld_strength(conn_plates_weld_fu=[self.weld_fu], gamma_mw=self.gamma_mb, t_t=1, f_w=round(self.allowable_stress, 2),
                                              type="end_plate"),
                  get_pass_fail(self.f_e, self.allowable_stress, relation="leq"))
            self.report_check.append(t1)

        # End of design report functions

        if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
            path_detailing = '/ResourceFiles/images/Detailing-Flush.png'
        elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
            path_detailing = '/ResourceFiles/images/Detailing-OWE.png'
        else:  # Both-way
            path_detailing = '/ResourceFiles/images/Detailing-BWE.png'

        if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
            path_stiffener = '/ResourceFiles/images/BB_Stiffener_FP.png'
        elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
            path_stiffener = '/ResourceFiles/images/BB_Stiffener_OWE.png'
        else:  # Both-way
            path_stiffener = '/ResourceFiles/images/BB_Stiffener_BWE.png'

        path_weld = "/ResourceFiles/images/BB-BC-single_bevel_groove.png"

        Disp_2d_image = [path_weld, path_detailing, path_stiffener]
        Disp_3d_image = "/ResourceFiles/images/3d.png"
        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")

        fname_no_ext = popup_summary['filename']

        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext, rel_path, Disp_2d_image,
                               Disp_3d_image, module=self.module)

        # End of design report
