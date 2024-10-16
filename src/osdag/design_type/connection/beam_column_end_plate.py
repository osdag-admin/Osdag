"""
@Author:    Danish Ansari - Osdag Team, IIT Bombay [(P) danishdyp@gmail.com / danishansari@iitb.ac.in]

            Note: This module was written by Ajmal Babu MS in Osdag 2, however in this version i.e. Osdag 3, @author has changed the design logic
                  and design algorithm. The results of this version might vary from that of the older ones.

@Module - Beam-Column End Plate Splice Connection
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
from design_type.connection.beam_beam_end_plate_splice import BeamBeamEndPlateSplice
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


class BeamColumnEndPlate(MomentConnection):
    def __init__(self):
        super(BeamColumnEndPlate, self).__init__()

        self.module = KEY_DISP_BCENDPLATE

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
        self.supported_section_mom_capa_m_zz = 0.0
        self.supported_section_mom_capa_m_yy = 0.0
        self.supported_section_shear_capa = 0.0
        self.supported_section_axial_capa = 0.0
        self.beam_fu = 0.0
        self.beam_fy = 0.0
        self.column_D = 0.0
        self.column_bf = 0.0
        self.column_tf = 0.0
        self.column_tw = 0.0
        self.column_r1 = 0.0
        self.column_r2 = 0.0
        self.column_zp_zz = 0.0
        self.column_fu = 0.0
        self.column_fy = 0.0
        self.epsilon_col = 1.0
        self.epsilon_beam = 1.0
        self.col_classification = ''
        self.beam_classification = ''
        self.beta_b_z = 1.0
        self.beta_b_y = 1.0
        self.beam_beta_b_z = 1.0
        self.beam_beta_b_y = 1.0
        self.M_dz = 0.0
        self.M_dy = 0.0
        self.IR_axial = 0.0
        self.IR_shear = 0.0
        self.IR_moment = 0.0
        self.sum_IR = 0.0
        self.dp_plate_fy = 0.0
        self.dp_plate_fu = 0.0

        self.column_clear_d = 0.0
        self.bc_compatibility_status = False
        self.minimum_load_status_shear = False
        self.minimum_load_status_moment = False
        self.plate_design_status = False
        self.helper_file_design_status = False
        self.deep_beam_status = False
        self.design_status = False
        self.design_status_list = []

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
        self.weld_fu = 0.0
        self.weld_length_web = 0.0
        self.weld_size_web = 0.0
        self.allowable_stress = 0.0
        self.f_a = 0.0
        self.q = 0.0
        self.f_e = 0.0

        self.cont_plate_fu = 0.0
        self.cont_plate_fy = 0.0
        self.cont_plate_epsilon = 0.0

        self.p_bf_1 = 0.0
        self.h_c = 0.0
        self.p_bf_2 = 0.0
        self.p_bf_2 = 0.0
        self.p_bf_3 = 0.0
        self.p_bf = 0.0
        self.continuity_plate_compression_flange_status = False
        self.continuity_plate_tension_flange_status = False
        self.cont_plate_area_req = 0.0
        self.notch_size = 0.0
        self.cont_plate_width = 0.0
        self.cont_plate_length_out = 0.0
        self.cont_plate_length_in = 0.0
        self.cont_plate_length = 0.0
        self.cont_plate_thk_req_1 = 0.0
        self.cont_plate_thk_req_2 = 0.0
        self.cont_plate_thk_req_3 = 0.0
        self.cont_plate_thk_req = 0.0
        self.cont_plate_thk_provided = 0.0
        self.t_bf = 0.0
        self.t_wc = 0.0
        self.web_stiffener_status = True
        self.load_diag_stiffener = 0.0
        self.diag_stiffener_area_req = 0.0
        self.diag_stiffener_length = 0.0
        self.diag_stiffener_width = 0.0
        self.web_stiffener_thk_req = 0.0
        self.web_stiffener_depth = 0.0
        self.web_stiffener_width = 0.0
        self.web_stiffener_thk_provided = 0.0
        self.p_c = 0.0
        self.web_weld_groove_status = False
        self.weld_both_side_cont_plate_status = False
        self.weld_length_cont_plate = 0.0
        self.weld_size_continuity_plate = 0.0
        self.cont_plate_groove_weld_status = False
        self.force_diag_stiffener = 0.0

        self.weld_size_web_stiffener = 0.0

        self.weld_size_diag_stiffener = 0.0
        self.weld_size_stiffener = 0.0

        self.diag_stiffener_groove_weld_status = False

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
        return KEY_DISP_BCENDPLATE

    # create UI for Input Dock
    def input_values(self):
        """ create a list of tuples to be displayed as the UI in Input Dock """
        self.module = KEY_DISP_BCENDPLATE

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_BCENDPLATE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_CONN, TYPE_COMBOBOX, VALUES_CONN_1, True, 'No Validator')
        options_list.append(t2)

        t2 = (KEY_ENDPLATE_TYPE, KEY_DISP_ENDPLATE_TYPE, TYPE_COMBOBOX, VALUES_ENDPLATE_TYPE, True, 'No Validator')
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, "./ResourceFiles/images/cf_bw_ebw.png", True, 'No Validator')
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, connectdb("Columns"), True, 'No Validator')
        options_list.append(t3)

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

        # t1 = ([KEY_CONN], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        # lst.append(t1)

        t2 = ([KEY_CONN, KEY_ENDPLATE_TYPE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t2)

        t3 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t3)

        return lst

    def fn_conn_image(self):
        """ display representative images of end plate type """
        conn = self[0]
        ep_type = self[1]

        if conn == CONN_CFBW and ep_type == VALUES_ENDPLATE_TYPE[0]:  # Flushed - Reversible Moment
            return './ResourceFiles/images/BC_CF-BW-Flush.png'
        elif conn == CONN_CFBW and ep_type == VALUES_ENDPLATE_TYPE[1]:  # Extended One Way - Irreversible Moment
            return './ResourceFiles/images/BC_CF-BW-EOW.png'
        elif conn in CONN_CFBW and ep_type == VALUES_ENDPLATE_TYPE[2]:  # Extended Both Ways - Reversible Moment
            return './ResourceFiles/images/BC_CF-BW-EBW.png'
        elif conn == CONN_CWBW and ep_type == VALUES_ENDPLATE_TYPE[0]:
            return './ResourceFiles/images/BC_CW-BW-Flush.png'
        elif conn == CONN_CWBW and ep_type == VALUES_ENDPLATE_TYPE[1]:
            return './ResourceFiles/images/BC_CW-BW-EOW.png'
        elif conn in CONN_CWBW and ep_type == VALUES_ENDPLATE_TYPE[2]:
            return './ResourceFiles/images/BC_CW-BW-EBW.png'
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

        t10 = (
            KEY_OUT_BOLT_TENSION_CAPACITY, KEY_OUT_CRITICAL_BOLT_TENSION_CAPACITY, TYPE_TEXTBOX, self.tension_capacity_critical_bolt if flag else '',
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

        t21 = (
            KEY_OUT_DETAILING_PITCH_DISTANCE, KEY_OUT_DISP_DETAILING_PITCH_DISTANCE, TYPE_TEXTBOX, self.pitch_distance_provided if flag else '', True)
        out_list.append(t21)

        if self.design_status:
            t22 = (KEY_OUT_DETAILING_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX,
                   self.gauge_distance_provided if flag and self.bolt_column == 4 else 'N/A', True)
        else:
            t22 = (KEY_OUT_DETAILING_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX,
                   self.gauge_distance_provided if flag else '', True)

        out_list.append(t22)

        t22 = (
            KEY_OUT_DETAILING_CS_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_CS_GAUGE_DISTANCE, TYPE_TEXTBOX,
            self.gauge_cs_distance_provided if flag else '',
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

        t22 = (KEY_OUT_EP_MOM_CAPACITY, KEY_OUT_DISP_EP_MOM_CAPACITY, TYPE_TEXTBOX, self.ep_moment_capacity if flag else '', True)
        out_list.append(t22)

        # Continuity Plate
        t34 = (None, DISP_TITLE_CONTINUITY_PLATE, TYPE_TITLE, None, True)
        out_list.append(t34)

        t35 = (KEY_OUT_CONTINUITY_DETAILS, KEY_OUT_DISP_CONTINUITY_PLATE_DETAILS, TYPE_OUT_BUTTON,
               ['Continuity Plate Details', self.continuity_plate_details], True)
        out_list.append(t35)

        # Column Web Stiffener Plate
        t34 = (None, DISP_TITLE_COL_WEB_STIFFENER_PLATE, TYPE_TITLE, None, True)
        out_list.append(t34)

        t35 = (KEY_OUT_COL_WEB_STIFFENER_DETAILS, KEY_OUT_DISP_WEB_STIFFENER_PLATE_DETAILS, TYPE_OUT_BUTTON,
               ['Web Stiffener Details', self.web_stiffener_plate_details], True)
        out_list.append(t35)

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

        t27 = (KEY_OUT_WELD_STRESS_NORMAL, KEY_OUT_DISP_WELD_NORMAL_STRESS, TYPE_TEXTBOX, self.f_a if flag else '', True)
        out_list.append(t27)

        t27 = (KEY_OUT_WELD_STRESS_SHEAR, KEY_OUT_DISP_WELD_SHEAR_STRESS, TYPE_TEXTBOX, self.q if flag else '', True)
        out_list.append(t27)

        t29 = (KEY_OUT_WELD_STRESS_COMBINED, KEY_OUT_DISP_WELD_STRESS_EQUIVALENT, TYPE_TEXTBOX, self.f_e if flag else '', True)
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

    # continuity plate details
    def continuity_plate_details(self, flag):
        continuity_plate = []

        if self.connectivity == VALUES_CONN_1[1]:  # CW-BW
            continuity_plate_nos = '2'
        else:  # CF-BW
            if self.continuity_plate_tension_flange_status == True and self.continuity_plate_compression_flange_status == True:
                continuity_plate_nos = '4'
            elif self.continuity_plate_tension_flange_status == True:
                continuity_plate_nos = '2'
            elif self.continuity_plate_compression_flange_status == True:
                continuity_plate_nos = '2'
            else:
                continuity_plate_nos = 'N/A'

        t31 = (KEY_OUT_CONTINUITY_PLATE_NOS, KEY_OUT_DISP_CONTINUITY_PLATE_NUMBER, TYPE_TEXTBOX, continuity_plate_nos if flag else 'NA', True)
        continuity_plate.append(t31)

        t31 = (KEY_OUT_CONTINUITY_PLATE_LENGTH, KEY_OUT_DISP_CONTINUITY_PLATE_LENGTH, TYPE_TEXTBOX, self.cont_plate_length_in if flag else 'NA', True)
        continuity_plate.append(t31)

        t32 = (KEY_OUT_CONTINUITY_PLATE_WIDTH, KEY_OUT_DISP_CONTINUITY_PLATE_WIDTH, TYPE_TEXTBOX, self.cont_plate_width if flag else 'NA', True)
        continuity_plate.append(t32)

        t33 = (KEY_OUT_CONTINUITY_PLATE_THK, KEY_OUT_DISP_CONTINUITY_PLATE_THK, TYPE_TEXTBOX, self.cont_plate_thk_provided if flag else 'NA', True)
        continuity_plate.append(t33)

        return continuity_plate

    # column web stiffener plate details
    def web_stiffener_plate_details(self, flag):
        stiffener_plate = []

        t31 = (KEY_OUT_WEB_STIFFENER_PLATE_NOS, KEY_OUT_DISP_WEB_STIFFENER_PLATE_NUMBER, TYPE_TEXTBOX, '2'
        if flag and self.web_stiffener_status == True else 'NA', True)
        stiffener_plate.append(t31)

        t31 = (KEY_OUT_WEB_STIFFENER_PLATE_LENGTH, KEY_OUT_DISP_WEB_PLATE_PLATE_DEPTH, TYPE_TEXTBOX, self.web_stiffener_depth if flag
        else 'NA', True)
        stiffener_plate.append(t31)

        t32 = (KEY_OUT_WEB_STIFFENER_PLATE_WIDTH, KEY_OUT_DISP_CONTINUITY_PLATE_WIDTH, TYPE_TEXTBOX, self.web_stiffener_width if flag
        else 'NA', True)
        stiffener_plate.append(t32)

        t33 = (KEY_OUT_WEB_STIFFENER_PLATE_THK, KEY_OUT_DISP_CONTINUITY_PLATE_THK, TYPE_TEXTBOX, self.web_stiffener_thk_provided if flag
        else 'NA', True)
        stiffener_plate.append(t33)

        return stiffener_plate

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

    # stiffener detailing
    def stiffener_detailing(self, status):

        detailing = []

        if self.connectivity == VALUES_CONN_1[1]:  # CW-BW
            if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
                detailing_path = './ResourceFiles/images/BC-CW-BW_Flush.png'
                width = 880
                height = 493
            elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
                detailing_path = './ResourceFiles/images/BC-CW-BW_EOW.png'
                width = 612
                height = 568
            else:  # Both-way
                detailing_path = './ResourceFiles/images/BC-CW-BW_EBW.png'
                width = 620
                height = 592
        else:  # CF-BW
            if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
                detailing_path = './ResourceFiles/images/BC_Stiffener_Flush.png'
                width = 938
                height = 478
            elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
                detailing_path = './ResourceFiles/images/BC_Stiffener_OWE.png'
                width = 636
                height = 562
            else:  # Both-way
                detailing_path = './ResourceFiles/images/BC_Stiffener_BWE.png'
                width = 710
                height = 550

        t1 = (None, 'Typical Stiffener Details', TYPE_IMAGE, [detailing_path, width, height, 'Typical stiffener details'])
        detailing.append(t1)

        return detailing

    # display weld details image
    def weld_details(self, status):

        weld = []

        t99 = (None, 'Weld Detail - Beam Flange to End Plate Connection', TYPE_IMAGE,
               ['./ResourceFiles/images/BB-BC-single_bevel_groove.png', 575.75, 519.4,
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

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_supporting_section)
        tabs.append(t1)

        t2 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_supported_section)
        tabs.append(t2)

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

        t1 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC_MATERIAL], [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY], TYPE_TEXTBOX,
              self.get_fu_fy_I_section_suptng)
        change_tab.append(t1)

        t2 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC_MATERIAL], [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY], TYPE_TEXTBOX,
              self.get_fu_fy_I_section_suptd)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t3)

        t3 = ("Bolt", [KEY_TYP], [KEY_DP_BOLT_TYPE], TYPE_COMBOBOX, self.get_bolt_tension_type_for_prying)
        change_tab.append(t3)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        t7 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

        return change_tab

    def refresh_input_dock(self):

        add_buttons = []

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, None, None, "Columns")
        add_buttons.append(t1)

        t2 = (KEY_DISP_BEAMSEC, KEY_SUPTDSEC, TYPE_COMBOBOX, KEY_SUPTDSEC, None, None, "Beams")
        add_buttons.append(t2)

        return add_buttons

    def input_dictionary_design_pref(self):
        design_input = []

        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SUPTNGSEC_MATERIAL])
        design_input.append(t1)

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

        t1 = (KEY_MATERIAL, [KEY_SUPTNGSEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

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

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('End Plate', self.call_3DPlate)
        components.append(t4)

        return components

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
        super(BeamColumnEndPlate, self).set_input_values(self, design_dictionary)

        self.module = KEY_DISP_BCENDPLATE
        self.mainmodule = "Moment Connection"
        self.connectivity = design_dictionary[KEY_CONN]
        self.endplate_type = design_dictionary[KEY_ENDPLATE_TYPE]
        self.material = Material(material_grade=design_dictionary[KEY_MATERIAL])

        self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC],
                                         material_grade=design_dictionary[KEY_SUPTNGSEC_MATERIAL])

        self.supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC], material_grade=design_dictionary[KEY_SUPTDSEC_MATERIAL])

        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                         bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])

        # self.load = Load(shear_force=float(design_dictionary[KEY_SHEAR]),
        #                  axial_force=float(design_dictionary[KEY_AXIAL]),
        #                  moment=float(design_dictionary[KEY_MOMENT]), unit_kNm=True)
        #
        # self.input_shear_force = float(design_dictionary[KEY_SHEAR])
        # self.input_axial_force = float(design_dictionary[KEY_AXIAL])
        # self.input_moment = float(design_dictionary[KEY_MOMENT])

        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],
                           gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.plate.design_status_capacity = False

        self.top_flange_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                                    type=design_dictionary[KEY_DP_WELD_TYPE],
                                    fabrication=design_dictionary[KEY_DP_WELD_FAB])
        self.bottom_flange_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                                       type=design_dictionary[KEY_DP_WELD_TYPE],
                                       fabrication=design_dictionary[KEY_DP_WELD_FAB])
        self.web_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                             type=design_dictionary[KEY_DP_WELD_TYPE], fabrication=design_dictionary[KEY_DP_WELD_FAB])

        self.stiffener_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                                   type=design_dictionary[KEY_DP_WELD_TYPE], fabrication=design_dictionary[KEY_DP_WELD_FAB])

        self.web_stiffener_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                                   type=design_dictionary[KEY_DP_WELD_TYPE], fabrication=design_dictionary[KEY_DP_WELD_FAB])

        self.continuity_plate_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
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
        self.beam_fu = float(self.supported_section.fu)
        self.beam_fy = float(self.supported_section.fy)

        # column properties
        self.column_D = self.supporting_section.depth
        self.column_bf = self.supporting_section.flange_width
        self.column_tf = self.supporting_section.flange_thickness
        self.column_tw = self.supporting_section.web_thickness
        self.column_r1 = self.supporting_section.root_radius
        self.column_r2 = self.supporting_section.toe_radius
        self.column_zp_zz = self.supporting_section.plast_sec_mod_z
        self.column_fu = float(self.supporting_section.fu)
        self.column_fy = float(self.supporting_section.fy)

        # plate

        # bolt
        self.beta = self.bolt.beta_prying

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

        self.call_helper = EndPlateSpliceHelper(module=self.module, supporting_section=self.supporting_section,
                                                supported_section=self.supported_section, load=self.load, bolt=self.bolt,
                                                connectivity=self.connectivity, ep_type=self.endplate_type, plate_design_status=False,
                                                helper_file_design_status=False)
        self.projection = 12.5

        # call functions for design
        self.check_compatibility(self)
        self.check_minimum_design_action(self)
        self.set_parameters(self)
        self.design_connection(self)
        self.design_continuity_plate(self)
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

        if self.supporting_section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

        ######################
        # self.hard_input(self)

    #####################hard input for cad#######################################
    def hard_input(self):
        ################################Flush###################################
        self.bolt.bolt_diameter_provided = 16
        self.bolt.bolt_grade_provided = 8.8
        self.plate.bolts_required = 4
        self.bolt_column = 2
        self.bolt_row = 2
        self.plate.edge_dist_provided = 35
        self.plate.end_dist_provided = 35
        # self.out_bolt = 0
        # self.outside_pitch = 0
        self.plate.pitch_provided = 40
        self.plate.gauge_provided = 40
        self.top_flange_weld.size = 4.0
        self.web_weld.size = 4.0
        self.plate.height = 420.0
        self.plate.width = 165.0
        self.plate.thickness_provided = 12.0
        ################################Flush###################################

        ################################Oneway###################################
        # self.bolt.bolt_diameter_provided = 24.0
        # self.bolt.bolt_grade_provided = 8.8
        # self.plate.bolts_required = 28
        # self.plate.bolt_line = 2
        # self.plate.bolts_one_line = 2
        # self.plate.edge_dist_provided = 45
        # self.plate.end_dist_provided = 45
        # self.inner_dimension = 278
        # self.out_bolt = 1
        # self.outside_pitch = 60
        # self.plate.pitch_provided = self.inner_dimension / (self.plate.bolt_line - 1)
        # self.plate.gauge_provided = 60
        # self.top_flange_weld.size = 4.0
        # self.web_weld.size = 4.0
        # self.plate.height = self.supported_section.depth + 10 + 2* self.plate.end_dist_provided + (self.out_bolt -1) * self.plate.pitch_provided
        # self.plate.width = 4 * self.plate.edge_dist_provided + self.supported_section.web_thickness + (self.plate.bolts_one_line - 2) * self.plate.gauge_provided
        # self.plate.thickness_provided = 12.0
        ################################Oneway###################################

        ################################bothway###################################
        # self.bolt.bolt_diameter_provided = 24.0
        # self.bolt.bolt_grade_provided = 8.8
        # self.plate.bolts_required = 12
        # self.plate.bolt_line = 4
        # self.plate.bolts_one_line = 2
        # self.plate.edge_dist_provided = 45
        # self.plate.end_dist_provided = 45
        # self.inner_dimension = 278
        # self.out_bolt = 2
        # self.outside_pitch = 60
        # self.plate.pitch_provided = self.inner_dimension / (self.plate.bolt_line - 1)
        # self.plate.gauge_provided = 60
        # self.top_flange_weld.size = 4.0
        # self.web_weld.size = 4.0
        # self.plate.height = self.supported_section.depth + 10 + 4 * self.plate.end_dist_provided + (
        #         self.out_bolt - 2) * self.plate.pitch_provided
        # self.plate.width = 4 * self.plate.edge_dist_provided + self.supported_section.web_thickness + (
        #         self.plate.bolts_one_line - 2) * self.plate.gauge_provided
        # self.plate.thickness_provided = 12.0
        ################################bothway###################################

    ############################################################################################
    # DESIGN STARTS
    ############################################################################################

    # Check whether the beam can be connected to the column based on compatibility

    def check_compatibility(self):
        """ """
        # Beam to Column web connectivity
        if self.connectivity == VALUES_CONN_1[1]:  # Column Web - Beam Web
            # 10 mm is the erection tolerance, 5 mm on each side
            self.column_clear_d = round(self.column_D - (2 * self.column_tf) - (2 * self.column_r1) - 10, 2)

            if (self.beam_bf + 25) > self.column_clear_d:  # 25 mm is the total extension of the end plate along its width
                self.bc_compatibility_status = False
                self.design_status = False
                self.design_status_list.append(self.design_status)
                logger.error(": The selected supporting column {} cannot accommodate the selected supported beam {}".
                             format(self.supporting_section.designation, self.supported_section.designation))
                logger.warning(": Width of the supported beam by considering the maximum end plate width (B + 25 mm), is more than the clear depth "
                               "available at the supporting column")
                logger.warning(": Width of supported beam should be less than or equal to {} mm".format(self.column_clear_d))
                logger.info(": Define a beam or a column of suitable compatibility and re-design")
            else:
                self.bc_compatibility_status = True

        else:  # Column flange connectivity
            if (self.beam_bf + 25) > self.column_bf:
                self.bc_compatibility_status = False
                self.design_status = False
                self.design_status_list.append(self.design_status)
                logger.error(": The selected supporting column {} cannot accommodate the selected supported beam {}".
                             format(self.supporting_section.designation, self.supported_section.designation))
                logger.warning(": Width of the supported beam by considering the maximum end plate width (B + 25 mm), is more than the width "
                               "available at the supporting column")
                logger.warning(": Width of the supported beam should be less than or equal to {} mm".format(self.column_bf))
                logger.info(": Define a beam or a column of suitable compatibility and re-design")
            else:
                self.bc_compatibility_status = True

    # Check for minimum Design Action (Cl. 10.7, IS 800:2007)
    def check_minimum_design_action(self):
        """ """
        # Input loads
        self.input_shear_force = self.load.shear_force
        self.input_axial_force = self.load.axial_force
        self.input_moment = self.load.moment  # about the major (z-z) axis of the beam

        # Capacities

        # 1: Moment capacity of the beam

        # 1.1: Section classification of the beam (Table 2, IS 800:2007)
        self.epsilon_beam = round(math.sqrt(250 / self.beam_fy), 2)

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
                                                                                      self.supported_section.plast_sec_mod_z, self.beam_fy,
                                                                                      section_class=section_class)
        self.supported_section_mom_capa_m_zz = round(self.supported_section_mom_capa_m_zz * 1e-6, 2)  # kNm

        # Moment capacity about the minor (y-y) axis
        self.supported_section_mom_capa_m_yy = self.cl_8_2_1_2_design_moment_strength(self.supported_section.elast_sec_mod_y,
                                                                                      self.supported_section.plast_sec_mod_y, self.beam_fy,
                                                                                      section_class=section_class)
        self.supported_section_mom_capa_m_yy = round(self.supported_section_mom_capa_m_yy * 1e-6, 2)  # kNm

        # 2: Shear capacity of the beam
        if self.supported_section.type == 'Rolled':
            # self.supported_section_shear_capa = ((self.beam_D * self.beam_tw) * self.beam_fy) / (math.sqrt(3) * self.gamma_m0)
            self.supported_section_shear_capa = (((self.beam_D - (2 * self.beam_tf)) * self.beam_tw) * self.beam_fy) / (math.sqrt(3) * self.gamma_m0)
        else:  # built-up sections
            self.supported_section_shear_capa = (((self.beam_D - (2 * self.beam_tf)) * self.beam_tw) * self.beam_fy) / (math.sqrt(3) * self.gamma_m0)

        self.supported_section_shear_capa = round(0.60 * self.supported_section_shear_capa * 1e-3, 2)  # kN, restricted to low shear

        # 3: Axial capacity of the beam
        self.supported_section_axial_capa = round((self.supported_section.area * self.beam_fy / self.gamma_m0) * 1e-3, 2)  # kN

        # Interaction ratio check for loads
        # loads are in kN
        self.IR_axial = round(self.input_axial_force / self.supported_section_axial_capa, 3)
        self.IR_shear = round(self.input_shear_force / self.supported_section_shear_capa, 3)
        self.IR_moment = round(self.input_moment / self.supported_section_mom_capa_m_zz, 3)

        self.sum_IR = round(self.IR_axial + self.IR_moment, 3)

        # Minimum load consideration check
        if self.sum_IR <= 1.0:

            if self.IR_moment < 0.5:
                self.load_moment = round(0.5 * self.supported_section_mom_capa_m_zz, 2)

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

                logger.warning("The Load(s) defined is/are less than the minimum recommended value [Ref. IS 800:2007, Cl.10.7].")
                logger.warning("[Minimum Factored Load] The external factored bending moment ({} kNm) is less than 0.5 times the plastic moment "
                               "capacity of the beam ({} kNm)".format(self.load.moment, self.supported_section_mom_capa_m_zz))
                logger.info("The minimum factored bending moment should be at least 0.5 times the plastic moment capacity of the beam to qualify the "
                            "connection as rigid connection (Annex. F-4.3.1, IS 800:2007)")
                logger.info("The value of load(s) is/are set at minimum recommended value as per Cl.10.7 and Annex. F, IS 800:2007")
                logger.info("Designing the connection for a factored moment of {} kNm".format(self.load_moment))

            # elif self.sum_IR <= 1.0 and self.IR_axial < 0.3:
            #
            #     if (0.3 - self.IR_axial) < (1 - self.sum_IR):
            #         self.load_axial = round(0.3 * self.supported_section_axial_capa, 2)
            #     else:
            #         self.load_axial = round(self.load.axial_force + ((1 - self.sum_IR) * self.supported_section_axial_capa), 2)
            #
            #     self.load_moment = round(self.supported_section_mom_capa_m_zz, 2)
            #
            #     logger.warning("The Load(s) defined is/are less than the minimum recommended value [Ref. IS 800:2007, Cl.10.7]")
            #     logger.info("The value of factored axial force ({} kN) is less than the minimum recommended value [Ref. Cl.10.7, IS 800:2007]".
            #                 format(self.input_axial_force))
            #     logger.info("The value of axial force is set at {} kN, as per the minimum recommended value by Cl.10.7".format(self.load_axial))
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
                self.load_axial = self.input_axial_force

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

        ################
        # if self.load.moment < (0.5 * self.supported_section_mom_capa_m_zz):
        #     self.minimum_load_status_moment = True
        #     # update moment value
        #     self.load_moment = round(0.5 * self.supported_section_mom_capa_m_zz, 2)  # kNm
        #
        #     logger.warning("[Minimum Factored Load] The external factored bending moment ({} kNm) is less than 0.5 times the plastic moment "
        #                    "capacity of the beam ({} kNm)".format(self.load.moment, self.load_moment))
        #     logger.info("The minimum factored bending moment should be at least 0.5 times the plastic moment capacity of the beam to qualify the "
        #                 "connection as rigid and transfer full moment from the beam to the column (Cl. 10.7, IS 800:2007)")
        #     logger.info("Designing the connection for a load of {} kNm".format(self.load_moment))
        #
        # elif self.load.moment > self.supported_section_mom_capa_m_zz:
        #     self.load_moment = self.supported_section_mom_capa_m_zz  # kNm
        #     self.minimum_load_status_moment = True
        #     self.design_status = False
        #     self.design_status_list.append(self.design_status)
        #     logger.error("[Maximum Factored Load] The external factored bending moment ({} kNm) is greater than the plastic moment capacity of the "
        #                  "beam ({} kNm)".format(self.load.moment, self.supported_section_mom_capa_m_zz))
        #     logger.warning("The maximum capacity of the connection is {} kNm".format(self.supported_section_mom_capa_m_zz))
        #     logger.info("Define the value of factored bending moment as {} kNm or less".format(self.supported_section_mom_capa_m_zz))
        # else:
        #     self.minimum_load_status_moment = False
        #     self.load_moment = self.load.moment  # kNm

        # Column check: check for input moment against the column capacity

        # 1: Section classification of the column
        self.epsilon_col = round(math.sqrt(250 / self.column_fy), 2)

        # flange b/t check
        if (self.column_bf / self.column_tf) > (10.5 * self.epsilon_col):
            self.col_classification = 'Semi-compact'
        else:
            self.col_classification = 'Compact'

        # web b/t check
        if self.col_classification == 'Compact':
            if ((self.column_D - (2 * self.column_tf)) / self.column_tw) > (42 * self.epsilon_col):
                self.col_classification = 'Semi-compact'
            else:
                self.col_classification = 'Compact'

        # 2: Bending capacity
        if self.col_classification == 'Semi-compact':
            self.beta_b_z = self.supporting_section.elast_sec_mod_z / self.supporting_section.plast_sec_mod_z
            self.beta_b_y = self.supporting_section.elast_sec_mod_y / self.supporting_section.plast_sec_mod_y
            section_class = 'semi-compact'
        else:
            self.beta_b_z = 1.0
            self.beta_b_y = 1.0
            section_class = 'Compact'

        self.M_dz = self.cl_8_2_1_2_design_moment_strength(self.supporting_section.elast_sec_mod_z, self.supporting_section.plast_sec_mod_z,
                                                           self.column_fy, section_class=section_class)
        self.M_dz = round(self.M_dz * 1e-6, 2)  # kNm

        self.M_dy = self.cl_8_2_1_2_design_moment_strength(self.supporting_section.elast_sec_mod_y, self.supporting_section.plast_sec_mod_y,
                                                           self.column_fy, section_class=section_class)
        self.M_dy = round(self.M_dy * 1e-6, 2)  # kNm

        # 3: Beam-Column compatibility check
        if self.connectivity == VALUES_CONN_1[0]:  # Column Flange - Beam Web, major axis capacity for the column
            if self.load_moment > self.M_dz:
                logger.warning("[Beam-Column Compatibility] The design factored bending moment ({} kNm) being transferred from the beam to the "
                               "column exceeds the maximum capacity of the column section ({} kNm) (acting along the major (z-z) axis)".
                               format(self.load_moment, self.M_dz))
                logger.info("Note: The maximum moment check is based on full capacity of the column section classified as {}, as per Table 2 of "
                            "IS 800:2007".format(self.col_classification))
                logger.info("The value of design bending moment is set to be equal to the maximum capacity of the column, i.e. {} kNm".
                            format(self.M_dz))
                self.load_moment = self.M_dz  # kNm

        else:  # Column Web - Beam Web, minor axis capacity for the column
            if self.load_moment > self.M_dy:
                logger.warning("[Beam-Column Compatibility] The design factored bending moment ({} kNm) being transferred from the beam to the "
                               "column exceeds the maximum capacity of the column section ({} kNm) (acting along the minor (y-y) axis)".
                               format(self.load_moment, self.M_dy))
                logger.info("Note: The maximum moment check is based on full capacity of the column section classified as {}, as per Table 2 of "
                            "IS 800:2007".format(self.col_classification))
                logger.info("The value of design bending moment is set to be equal to the maximum capacity of the column, i.e. {} kNm".
                            format(self.M_dy))
                self.load_moment = self.M_dy  # kNm

        # effective moment is the moment due to external factored moment plus moment due to axial force
        self.load_moment_effective = round(self.load_moment + (self.load_axial * ((self.beam_D / 2) - (self.beam_tf / 2))) * 1e-3, 2)  # kNm

    def set_parameters(self):
        """ set/initialize parameters for performing the analyses and design """

        # setting bolt ist
        self.bolt_diameter = self.bolt.bolt_diameter
        self.bolt_grade = self.bolt.bolt_grade
        self.bolt_type = self.bolt.bolt_type

        # set plate thickness list [minimum to maximum]
        # Note: minimum plate thk is at-least equal to the thk of thicker connecting element (flange thk or web thk)
        self.plate_thickness = []

        for i in self.plate.thickness:
            if self.connectivity == VALUES_CONN_1[0]:  # 'Column flange-Beam web'

                if i < max(self.beam_tf, self.beam_tw, self.column_tf):
                    logger.warning("[End Plate] The end plate of {} mm is thinner than the thickest of the elements being connected".format(i))
                    logger.info("Selecting a plate of higher thickness which is at least {} mm thick".format(round(max(self.beam_tf, self.beam_tw,
                                                                                                                       self.column_tf)), 2))
                else:
                    self.plate_thickness.append(i)

            else:  # 'Column web-Beam web'
                if i < max(self.beam_tf, self.beam_tw, self.column_tw):
                    self.plate_thickness.append(i)
                    logger.warning("[End Plate] The end plate of {} mm is thinner than the thickest of the elements being connected".format(i))
                    logger.info("Selecting a plate of higher thickness which is at least {} mm thick".format(round(max(self.beam_tf, self.beam_tw,
                                                                                                                       self.column_tw)), 2))
                else:
                    self.plate_thickness.append(i)

        self.plate_thickness = self.plate_thickness  # final list of plate thicknesses considered for simulation
        self.plate_thickness_list = self.plate_thickness

        # checking if the list contains at least one plate of thk higher than the minimum required
        if len(self.plate_thickness_list) == 0:
            self.design_status = False
            self.design_status_list.append(self.design_status)
            logger.error("[End Plate] The list of plate thicknesses passed into the solver is insufficient to perform end plate design")
            logger.warning("The end plate should at least be thicker than the maximum thickness of the connecting element(s)")
            logger.info("Provide a plate/list of plates with a minimum thickness of {} mm".format(max(self.beam_tf, self.beam_tw, self.column_tf,
                                                                                                      self.column_tw)))

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
                    .format(len(self.bolt_list) / 2))

        # create a list of tuple with a combination of each bolt diameter with each grade for iteration
        # list is created using the approach --- minimum diameter, small grade to maximum diameter, high grade
        self.bolt_list = [x for x in zip(*[iter(self.bolt_list)] * 2)]
        # logger.info("Checking the design with the following bolt diameter-grade combination {}".format(self.bolt_list))

    def design_connection(self):
        """ perform analysis and design of bolt and end plate """

        if self.connectivity == VALUES_CONN_1[0]:

            # Stiffener requirement at the column web (design for shear)
            self.t_wc = round((1.9 * self.load_moment_effective * 1e6) / (self.column_D * self.beam_D * self.column_fy), 2)  # mm

            if self.t_wc > self.column_tw:
                self.web_stiffener_status = True
                logger.warning("[Column Web] The web of the column is susceptible to shear bucking due to the reaction transferred by the beam to "
                               "the column")
                logger.info("The minimum required thickness of the web is {} mm".format(self.t_wc))
                logger.info("Providing stiffening to the column web")
            else:
                self.web_stiffener_status = False
                logger.warning("[Column Web] The web of the column is safe against shear bucking due to the reaction transferred by the beam "
                               "to the column")
                logger.info("The minimum required thickness of the web i.e. {} mm is satisfied".format(self.t_wc))
                logger.info("Additional stiffening of the column web is not required")

            if self.web_stiffener_status == True:

                self.web_stiffener_depth = self.beam_D - (2 * self.beam_tf) - (2 * self.beam_r1) - (2 * 10)
                self.web_stiffener_depth = round(self.web_stiffener_depth)

                self.web_stiffener_width = self.column_D - (2 * self.column_tf) - (2 * self.column_r1) - (2 * 10)
                self.web_stiffener_width = round(self.web_stiffener_width)

                self.web_stiffener_thk_req = round((self.t_wc - self.column_tw) / 2, 2)

                # choosing a suitable plate from the standard available list of plate thicknesses
                standard_plt_thk = []
                for plt in PLATE_THICKNESS_SAIL:
                    plt = int(plt)
                    standard_plt_thk.append(plt)

                sort_plate = filter(lambda x: max(standard_plt_thk[0], self.web_stiffener_thk_req) <= x <= standard_plt_thk[-1], standard_plt_thk)
                for thk in sort_plate:
                    self.web_stiffener_thk_provided = thk  # stiffener thickness provided (mm)
                    break
            else:
                self.web_stiffener_depth = 'N/A'
                self.web_stiffener_width = 'N/A'
                self.web_stiffener_thk_provided = 'N/A'

        else:  # web stiffening is not provided in col-web beam-web connectivity, the web thickness along with the plate should suffice
            self.web_stiffener_status = False
            self.web_stiffener_depth = 'N/A'
            self.web_stiffener_width = 'N/A'
            self.web_stiffener_thk_provided = 'N/A'

        # performing the check with minimum plate thickness and a suitable bolt dia-grade combination (thin plate - large dia approach)
        logger.info("[Optimisation] Performing the design by optimising the plate thickness, using the most optimum plate and a suitable bolt "
                    "diameter approach")
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
                            self.pitch_distance_provided = self.pitch_distance_provided + (
                                        (1 / 2) * IS1364Part3.nut_size(self.bolt_diameter_provided))
                            self.pitch_distance_provided = round_up(self.pitch_distance_provided, 5)
                            self.gauge_distance_provided = self.pitch_distance_provided

                            # end/edge
                            self.end_distance_provided = self.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_provided, self.bolt.bolt_hole_type,
                                                                                            self.bolt.edge_type)
                            self.end_distance_provided = round_up(self.end_distance_provided, 5)  # mm
                            self.edge_distance_provided = self.end_distance_provided

                            # cross-centre gauge
                            if self.connectivity == VALUES_CONN_1[0]:
                                if self.web_stiffener_status is True:
                                    self.gauge_cs_distance_provided = max(self.beam_tw + self.beam_r1, self.column_tw +
                                                                          (2 * self.web_stiffener_thk_provided) + self.column_r1) + \
                                                                      (2 * self.edge_distance_provided)
                                else:
                                    self.gauge_cs_distance_provided = max(self.beam_tw + self.beam_r1, self.column_tw + self.column_r1) + \
                                                                      (2 * self.edge_distance_provided)

                            else:
                                self.gauge_cs_distance_provided = self.beam_tw + self.beam_r1 + (2 * self.edge_distance_provided)

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
                            # Note: space_available_inside_D is calculated assuming minimum space available after providing minimum rows inside
                            self.space_available_inside_D = self.beam_D - (2 * self.beam_tf) - (2 * self.beam_r1) - (2 * self.end_distance_provided)
                            self.space_min_req_inside_D = (2 * self.end_distance_provided) + self.pitch_distance_provided

                            if self.space_available_inside_D < self.space_min_req_inside_D:
                                self.design_status = False
                                if (self.plate_thickness == self.plate_thickness_list[-1]) and (self.design_status is False):
                                    self.design_status_list.append(self.design_status)

                                logger.error("[Compatibility Error]: The given beam cannot accommodate at least a single row of bolt (inside top and "
                                             "bottom flange) with a trial diameter of {} mm ".format(self.bolt_diameter_provided))
                                logger.info("Re-design the connection by defining a bolt of smaller diameter or beam of a suitable depth ")
                                self.rows_inside_D_max = 0
                                self.bolt_row = 0
                                self.bolt_row_web = 0
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
                                # logger.info(
                                #     "The provided beam can accommodate two columns of bolts on either side of the web [Ref. based on the detailing "
                                #     "requirement]")
                                # logger.info("Performing the design with two column of bolts on each side")

                            if (self.ep_width_provided >= space_req_2col) and (self.ep_width_provided < space_req_4col):
                                self.bolt_column = 2  # one column on each side
                                # logger.info("The provided beam can accommodate a single column of bolt on either side of the web [Ref. based on "
                                #             "detailing requirement]")
                                # logger.info("Performing the design with a single column of bolt on each side")

                            if self.ep_width_provided < space_req_2col:
                                self.bolt_column = 0
                                self.bolt_row = 0
                                self.last_column = self.bolt_column
                                self.design_status = False
                                if (self.plate_thickness == self.plate_thickness_list[-1]) and (self.design_status is False):
                                    self.design_status_list.append(self.design_status)

                                logger.error("[Detailing] The beam is not wide enough to accommodate a single column of bolt on either side")
                                logger.error("The defined beam is not suitable for performing connection design")
                                logger.info(
                                    "Please define another beam which has sufficient width (minimum, {} mm) and re-design".format(space_req_2col))

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
                                                                                                    self.bolt_column, self.bolt_row,
                                                                                                    self.bolt_row_web,
                                                                                                    self.bolt_diameter_provided,
                                                                                                    self.bolt_grade_provided,
                                                                                                    self.load_moment_effective,
                                                                                                    self.end_distance_provided,
                                                                                                    self.pitch_distance_provided,
                                                                                                    self.pitch_distance_web,
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
                                            self.ep_height_provided = self.beam_D + 12.5 + (
                                                        2 * self.end_distance_provided) + self.pitch_distance_provided

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
                    "The minimum required thickness of end plate is {} mm".format(
                        round(self.call_helper.plate_thickness_req, 2)))
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
                    "capacity ({} kN)".format(self.call_helper.bolt_tension_demand, self.call_helper.bolt_tension_capacity))
                logger.info("Re-designing the connection with a bolt of higher grade and/or diameter")
            else:
                logger.info("[Bolt Design] The bolt of {} mm diameter and {} grade passes the tension check".
                            format(self.bolt_diameter_provided, self.bolt_grade_provided))
                logger.info(
                    "Total tension demand on bolt (due to direct tension + prying action) is {} kN and the bolt tension "
                    "capacity is ({} kN)".format(self.call_helper.bolt_tension_demand,
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
            self.tension_demand_critical_bolt = round(self.call_helper.bolt_tension_demand, 2)
            self.tension_capacity_critical_bolt = self.call_helper.bolt_tension_capacity
            self.combined_capacity_critical_bolt = self.call_helper.bolt_combined_check_UR

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

            # plate height
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

        else:
            if self.bc_compatibility_status == False or len(self.plate_thickness_list) == 0:

                if self.endplate_type == 'Flushed - Reversible Moment':
                    self.bolt_row = 2
                elif self.endplate_type == 'Extended One Way - Irreversible Moment':
                    self.bolt_row = 3
                else:
                    self.bolt_row = 4

                combined_list = []

        if len(combined_list) == 0:
            self.last_column = 0
            self.bolt_column = 0
            self.bolt_numbers = self.bolt_column * self.bolt_row

    def design_continuity_plate(self):
        """ design the continuity plate for the column flange - beam web connection """

        # mechanical properties of the continuity plate
        self.cont_plate_fu = self.plate.fu
        self.cont_plate_fy = self.plate.fy
        self.cont_plate_epsilon = math.sqrt(250 / self.cont_plate_fy)

        # column flange to beam web connectivity
        if self.connectivity == VALUES_CONN_1[0]:

            # Design 2: Continuity Plates on compression side (for all 3 types of end plate)

            # check 1: local column web yielding capacity
            self.p_bf_1 = ((self.column_fy * self.column_tw * ((5 * (self.column_tf + self.column_r1)) + self.beam_tf)) / self.gamma_m0) * 1e-3  # kN
            self.p_bf_1 = round(self.p_bf_1, 2)

            # check 2: compression buckling capacity of the column web
            self.h_c = self.column_D - (2 * (self.column_tf + self.column_r1))  # mm, clear space available between the column depth
            self.p_bf_2 = 10710 * (self.column_tw ** 3 / self.h_c) * math.sqrt(self.column_fy / self.gamma_m0) * 1e-3  # kN
            self.p_bf_2 = round(self.p_bf_2, 2)

            # check 3: column web crippling capacity (as per american code)
            self.p_bf_3 = ((300 * self.column_tw ** 2) / self.gamma_m1) * (1 + (3 * (self.beam_tf / self.column_D) *
                                                                                (self.column_tw / self.column_tf) ** 1.5)) * \
                          math.sqrt((self.column_fy * self.column_tf) / self.column_tw) * 1e-3  # kN
            self.p_bf_3 = round(self.p_bf_3, 2)

            # capacity of the web
            self.p_bf = min(self.p_bf_1, self.p_bf_2, self.p_bf_3)  # taking the lowest of the capacities

            # checking if the continuity plate is required
            if self.p_bf < self.call_helper.r_c:

                self.continuity_plate_compression_flange_status = True
                # the design of the continuity plate is same for compression and tension side for reversible moment connections
                if (self.endplate_type == VALUES_ENDPLATE_TYPE[0]) or (self.endplate_type == VALUES_ENDPLATE_TYPE[2]):  # flush and both way
                    self.continuity_plate_tension_flange_status = True
                else:
                    self.continuity_plate_tension_flange_status = False

                # continuity plate design
                self.cont_plate_area_req = ((self.call_helper.r_c - self.p_bf) * 1e3) / (self.cont_plate_fy * self.gamma_m0)  # mm^2, total req area

                if self.column_r1 > 0:
                    self.notch_size = round_up(self.column_r1 + (self.column_r1 / 2), 2)  # mm
                    self.cont_plate_width = round_down((self.column_bf - self.column_tw - (2 * self.notch_size)), 2) / 2  # mm
                else:
                    self.notch_size = 10  # mm, assumed (10 X 10)
                    self.cont_plate_width = round_down((self.column_bf - self.column_tw - (2 * self.notch_size)), 2) / 2  # mm

                # provided length of the continuity plate
                self.cont_plate_length_out = self.column_D - (2 * self.column_tf)  # at outer side connected to the flange
                self.cont_plate_length_in = self.column_D - (2 * (self.column_tf + self.notch_size))  # mm, at inner side connected to the web

                self.cont_plate_thk_req_1 = (self.cont_plate_area_req / 2) / self.cont_plate_width  # from the minimum req area criteria
                self.cont_plate_thk_req_2 = self.cont_plate_length_out / (29.3 * self.cont_plate_epsilon)  # from limiting b/t ratio criteria
                self.cont_plate_thk_req_3 = self.beam_tf  # from minimum thickness criteria

                self.cont_plate_thk_req = max(self.cont_plate_thk_req_1, self.cont_plate_thk_req_2, self.cont_plate_thk_req_3)

                # choosing a suitable plate from the standard available list of plate thicknesses
                standard_plt_thk = []
                for plt in PLATE_THICKNESS_SAIL:
                    plt = int(plt)
                    standard_plt_thk.append(plt)

                sort_plate = filter(lambda x: self.cont_plate_thk_req <= x <= standard_plt_thk[-1], standard_plt_thk)
                for thk in sort_plate:
                    self.cont_plate_thk_provided = thk  # plate thickness provided (mm)
                    break
            else:
                if (self.endplate_type == VALUES_ENDPLATE_TYPE[0]) or (self.endplate_type == VALUES_ENDPLATE_TYPE[2]):  # flush and both way
                    self.continuity_plate_compression_flange_status = False
                    self.continuity_plate_tension_flange_status = False
                    self.cont_plate_length_out = 'N/A'
                    self.cont_plate_length_in = 'N/A'
                    self.cont_plate_width = 'N/A'
                    self.cont_plate_thk_provided = 'N/A'
                else:
                    self.continuity_plate_compression_flange_status = False

            if self.column_r1 > 0:
                self.notch_size = round_up(self.column_r1 + (self.column_r1 / 2), 2)  # mm
            else:
                self.notch_size = 10  # mm, assumed (10 X 10)

            # Design 2: Continuity Plates on tension side for one way connection
            if self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # one way
                self.t_bf = round(0.4 * math.sqrt((self.beam_bf * self.beam_tf) / self.gamma_m0), 2)  # mm

                if self.t_bf > self.column_tf:
                    self.continuity_plate_tension_flange_status = True

                    if self.continuity_plate_compression_flange_status == True:
                        self.cont_plate_length_out = self.cont_plate_length_out
                        self.cont_plate_length_in = self.cont_plate_length_in
                        self.cont_plate_width = self.cont_plate_width  # provided width of the continuity plate
                        self.cont_plate_thk_provided = self.cont_plate_thk_provided
                    else:
                        if self.column_r1 > 0:
                            self.notch_size = round_up(self.column_r1 + (self.column_r1 / 2), 2)  # mm
                            self.cont_plate_width = round_down((self.column_bf - self.column_tw - (2 * self.notch_size)), 2) / 2  # mm
                        else:
                            self.notch_size = 10  # mm
                            self.cont_plate_width = round_down((self.column_bf - self.column_tw - (2 * self.notch_size)), 2) / 2  # mm

                        # provided length of the continuity plate
                        self.cont_plate_length_out = self.column_D - (2 * self.column_tf)  # at outer side connected to the flange
                        self.cont_plate_length_in = self.column_D - (2 * (self.column_tf + self.notch_size))  # mm, at inner side connected to the web

                        self.cont_plate_thk_req = self.column_tf

                        # choosing a suitable plate from the standard available list of plate thicknesses
                        standard_plt_thk = []
                        for plt in PLATE_THICKNESS_SAIL:
                            plt = int(plt)
                            standard_plt_thk.append(plt)

                        sort_plate = filter(lambda x: self.cont_plate_thk_req <= x <= standard_plt_thk[-1], standard_plt_thk)
                        for thk in sort_plate:
                            self.cont_plate_thk_provided = thk  # plate thickness provided (mm)
                            break
                else:
                    self.continuity_plate_tension_flange_status = False

        else:  # column web to beam web connectivity
            self.continuity_plate_tension_flange_status = True
            self.continuity_plate_compression_flange_status = True

            if self.column_r1 > 0:
                self.notch_size = round_up(self.column_r1 + (self.column_r1 / 2), 2)  # mm
                self.cont_plate_width = round_down((self.column_bf - self.column_tw - (2 * self.notch_size)), 2) / 2  # mm
            else:
                self.notch_size = 10  # mm, assumed (10 X 10)
                self.cont_plate_width = round_down((self.column_bf - self.column_tw - (2 * self.notch_size)), 2) / 2  # mm

            # provided length of the continuity plate
            self.cont_plate_length_out = self.column_D - (2 * self.column_tf)  # at outer side connected to the flange
            self.cont_plate_length_in = self.column_D - (2 * (self.column_tf + self.notch_size))  # mm, at inner side connected to the web

            self.cont_plate_thk_req = self.column_tw

            # choosing a suitable plate from the standard available list of plate thicknesses
            standard_plt_thk = []
            for plt in PLATE_THICKNESS_SAIL:
                plt = int(plt)
                standard_plt_thk.append(plt)

            sort_plate = filter(lambda x: self.cont_plate_thk_req <= x <= standard_plt_thk[-1], standard_plt_thk)
            for thk in sort_plate:
                self.cont_plate_thk_provided = thk  # plate thickness provided (mm)
                break

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
        """ design fillet weld at web for the connection and continuity/stiffener plates """
        if (len(self.plate_thickness_list) != 0) and (self.bolt_row != 0) and (self.bolt_column != 0):

            # weld strength
            self.weld_fu = min(self.web_weld.fu, self.plate.fu)

            # 1: design of weld for beam web and end plate connection

            # weld size calculation
            self.web_weld.set_min_max_sizes(self.plate_thickness, self.beam_tw, special_circumstance=False, fusion_face_angle=90)

            self.weld_length_web = 2 * (self.beam_D - (2 * self.beam_tf) - (2 * self.beam_r1) - 20)  # mm, available on either side of the web
            self.weld_length_web = round(self.weld_length_web - self.web_weld.max_size, 2)  # mm, available effective length on either side of the web

            self.weld_size_web = (self.load_shear * 1e3 * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_length_web * self.weld_fu)  # mm
            self.weld_size_web = round_up(self.weld_size_web, 2)
            self.weld_size_web = max(self.weld_size_web, round_up(self.web_weld.min_size, 2))  # mm

            # weld strength
            self.allowable_stress = round(self.weld_fu / (math.sqrt(3) * self.gamma_mw), 2)  # N/mm^2, allowable stress in the weld

            # combination of stress check
            self.q = round((self.load_shear * 1e3) / (0.7 * self.weld_size_web * self.weld_length_web), 2)  # N/mm^2, stress due to shear force

            if self.load_axial > 0.0:
                self.f_a = round((self.load_axial * 1e3) / (0.7 * self.weld_size_web * self.weld_length_web), 2)  # N/mm^2, stress due to axial force

                self.f_e = round(math.sqrt(self.f_a + (3 * self.q ** 2)), 2)  # N/mm^2, stress due to combined load

                # allowable stress check
                if self.f_e > self.allowable_stress:
                    self.web_weld_groove_status = True
                    logger.warning("[Weld Design] The weld at web fails in the combined axial and shear design check with the available length")
                    logger.info("Providing groove weld at the web")
                else:
                    self.web_weld_groove_status = False
            else:
                self.f_a = 'N/A'
                self.f_e = 'N/A'
                self.web_weld_groove_status = False

            # 2: design of weld for the continuity and web stiffener plates
            if self.connectivity == VALUES_CONN_1[0]:  # flange-web connectivity

                # 1. Continuity plates
                if (self.continuity_plate_compression_flange_status == True) or (self.continuity_plate_tension_flange_status == True):
                    self.p_c = self.call_helper.r_c - self.p_bf  # kN, total force carried by the continuity plate

                    self.continuity_plate_weld.set_min_max_sizes(self.cont_plate_thk_provided, self.column_tw, special_circumstance=False,
                                                          fusion_face_angle=90)

                    self.weld_length_cont_plate = self.cont_plate_length_in  # mm, total length available along the plates on each side
                    self.weld_length_cont_plate = self.weld_length_cont_plate - self.continuity_plate_weld.max_size  # mm, total effective length

                    # weld on one side of the continuity plate
                    self.weld_size_continuity_plate = ((self.p_c / 2) * 1e3 * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_length_cont_plate *
                                                                                                               self.weld_fu)  # mm
                    self.weld_size_continuity_plate = round_up(self.weld_size_continuity_plate, 2)
                    self.weld_size_continuity_plate = max(self.weld_size_continuity_plate, self.continuity_plate_weld.min_size)  # mm

                    self.weld_both_side_cont_plate_status = False

                    if self.weld_size_continuity_plate > self.continuity_plate_weld.max_size:
                        self.weld_both_side_cont_plate_status = True
                        # provide weld on both the sides of the continuity plate
                        self.weld_length_cont_plate = 2 * self.weld_length_cont_plate

                        self.weld_size_continuity_plate = ((self.p_c / 2) * 1e3 * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_length_cont_plate *
                                                                                                                   self.weld_fu)  # mm
                        self.weld_size_continuity_plate = round_up(self.weld_size_continuity_plate, 2)
                        self.weld_size_continuity_plate = max(self.weld_size_continuity_plate, self.continuity_plate_weld.min_size)  # mm

                        if self.weld_size_continuity_plate > self.continuity_plate_weld.max_size:
                            self.cont_plate_groove_weld_status = True
                        else:
                            self.cont_plate_groove_weld_status = False
                    else:
                        self.cont_plate_groove_weld_status = False
                else:
                    self.weld_size_continuity_plate = 'N/A'
                    self.weld_length_cont_plate = 'N/A'
                    # self.weld_size_continuity_plate = 6
                    # self.weld_length_cont_plate = 6
                    self.weld_both_side_cont_plate_status = False
                    self.cont_plate_groove_weld_status = False

            else:  # web-web connectivity

                # 1. Continuity plates
                if (self.continuity_plate_compression_flange_status == True) or (self.continuity_plate_tension_flange_status == True):
                    self.continuity_plate_weld.set_min_max_sizes(self.cont_plate_thk_provided, self.column_tw, special_circumstance=False,
                                                          fusion_face_angle=90)

                    self.weld_length_cont_plate = self.cont_plate_length_in  # mm, total length available along the plates on each side
                    self.weld_length_cont_plate = self.weld_length_cont_plate - self.continuity_plate_weld.max_size  # mm, total effective length

                    # weld on one side of the continuity plate
                    self.weld_size_continuity_plate = round_up(self.continuity_plate_weld.min_size, 2)
                    self.weld_both_side_cont_plate_status = False
                    self.cont_plate_groove_weld_status = False

                else:
                    self.weld_size_continuity_plate = 'N/A'
                    self.weld_length_cont_plate = 'N/A'
                    # self.weld_size_continuity_plate = 6
                    # self.weld_length_cont_plate = 6
                    self.weld_both_side_cont_plate_status = False
                    self.cont_plate_groove_weld_status = False

            # 2. Web stiffener plates
            if self.web_stiffener_status == True:
                self.web_stiffener_weld.set_min_max_sizes(self.web_stiffener_thk_provided, self.column_tw, special_circumstance=False,

                                                      fusion_face_angle=90)
                self.weld_size_web_stiffener = round_up(self.web_stiffener_weld.min_size, 2)

            else:
                self.weld_size_web_stiffener = 'N/A'

            # 3: design of weld for the stiffener plates
            if self.endplate_type == 'Flushed - Reversible Moment':
                self.stiffener_weld.set_min_max_sizes(max(self.plate_thickness, self.stiffener_thickness, self.beam_tw),
                                                      min(self.plate_thickness, self.stiffener_thickness, self.beam_tw),
                                                      special_circumstance=False, fusion_face_angle=90)
            else:
                self.stiffener_weld.set_min_max_sizes(max(self.plate_thickness, self.stiffener_thickness, self.beam_tf),
                                                      min(self.plate_thickness, self.stiffener_thickness, self.beam_tf),
                                                      special_circumstance=False, fusion_face_angle=90)
            self.weld_size_stiffener = round_up(self.stiffener_weld.min_size, 2)  # mm

        # end of the design simulation

        # overall design status
        for status in self.design_status_list:
            if status is False:
                self.design_status = False
                break
            else:
                self.design_status = True

        if self.design_status:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall beam to column end plate connection design is SAFE")
            logger.info(": ========== End Of Design ============")
        else:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall beam to column end plate connection design is UNSAFE")
            logger.info(": ========== End Of Design ============")

    def save_design(self, popup_summary):
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")

        if self.supported_section.flange_slope == 90:
            image = "Parallel_Beam"
        else:
            image = "Slope_Beam"
        self.report_supported = {KEY_DISP_SEC_PROFILE: "ISection",
                                 KEY_DISP_BEAMSEC_REPORT: self.supported_section.designation,
                                 KEY_DISP_MATERIAL: self.supported_section.material,
                                 KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.supported_section.fu,
                                 KEY_DISP_YIELD_STRENGTH_REPORT: self.supported_section.fy,
                                 KEY_REPORT_MASS: self.supported_section.mass,
                                  KEY_REPORT_AREA: round(self.supported_section.area * 1e-2, 2),
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

        if self.supporting_section.flange_slope == 90:
            image = "Parallel_Beam"
        else:
            image = "Slope_Beam"

        self.report_supporting = {KEY_DISP_SEC_PROFILE: "ISection",
                                  KEY_DISP_COLSEC_REPORT: self.supporting_section.designation,
                                  KEY_DISP_MATERIAL: self.supporting_section.material,
                                  KEY_DISP_FU: self.supporting_section.fu,
                                  KEY_DISP_FY: self.supporting_section.fy,
                                  KEY_REPORT_MASS: self.supporting_section.mass,
                                  KEY_REPORT_AREA: round(self.supporting_section.area * 1e-2, 2),
                                  KEY_REPORT_DEPTH: self.supporting_section.depth,
                                  KEY_REPORT_WIDTH: self.supporting_section.flange_width,
                                  KEY_REPORT_WEB_THK: self.supporting_section.web_thickness,
                                  KEY_REPORT_FLANGE_THK: self.supporting_section.flange_thickness,
                                  KEY_DISP_FLANGE_S_REPORT: self.supporting_section.flange_slope,
                                  KEY_REPORT_R1: self.supporting_section.root_radius,
                                  KEY_REPORT_R2: self.supporting_section.toe_radius,
                                  KEY_REPORT_IZ: round(self.supporting_section.mom_inertia_z * 1e-4, 2),
                                  KEY_REPORT_IY: round(self.supporting_section.mom_inertia_y * 1e-4, 2),
                                  KEY_REPORT_RZ: round(self.supporting_section.rad_of_gy_z * 1e-1, 2),
                                  KEY_REPORT_RY: round(self.supporting_section.rad_of_gy_y * 1e-1, 2),
                                  KEY_REPORT_ZEZ: round(self.supporting_section.elast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZEY: round(self.supporting_section.elast_sec_mod_y * 1e-3, 2),
                                  KEY_REPORT_ZPZ: round(self.supporting_section.plast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZPY: round(self.supporting_section.plast_sec_mod_y * 1e-3, 2)}

        self.report_input = \
            {KEY_MAIN_MODULE: self.mainmodule,
             KEY_MODULE: KEY_DISP_BCENDPLATE,
             KEY_CONN: self.connectivity,
             KEY_DISP_ENDPLATE_TYPE: self.endplate_type,
             KEY_DISP_MOMENT: self.input_moment,
             KEY_DISP_SHEAR: self.input_shear_force,
             KEY_DISP_AXIAL: self.input_axial_force,

             "Column Section - Mechanical Properties": "TITLE",
             "Section Details": self.report_supporting,

             "Beam Section - Mechanical Properties": "TITLE",
             "Section Details ": self.report_supported,

             "Plate Details - Input and Design Preference": "TITLE",
             KEY_DISP_PLATETHK: str(list(np.int_(self.plate.thickness))),
             KEY_DISP_MATERIAL: self.plate.material,
             KEY_DISP_FU: self.plate.fu,
             KEY_DISP_FY: self.plate.fy,

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
             KEY_DISP_CONTINUITY_PLATE_WELD_TYPE: "Fillet Weld",

             "Detailing - Design Preference": "TITLE",
             KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
             KEY_DISP_GAP: self.plate.gap,
             KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM: self.bolt.corrosive_influences,
             }

        self.report_check = []

        if (len(self.plate_thickness_list) != 0) and (self.bolt_row != 0):
            self.bolt_conn_plates_t_fu_fy = []
            self.bolt_conn_plates_t_fu_fy.append((self.plate_thickness, 0, 0))

        self.h = (self.beam_D - (2 * self.beam_tf))

        # CHECK: Beam to Column Compatibility Check
        t1 = ('SubSection', 'Beam to Column - Compatibility Check', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{2cm}|')
        self.report_check.append(t1)

        if self.connectivity == CONN_CFBW:  # Column Flange - Beam Web

            t1 = ("Beam Section Compatibility", bc_ep_compatibility_req(self.beam_bf, self.beam_bf + 25),
                  bc_ep_compatibility_available(0, self.column_bf, 0, 0, 0, CONN_CFBW),
                  'Compatible' if self.bc_compatibility_status is True else 'Not compatible')
            self.report_check.append(t1)
        else:
            t1 = ("Beam Section Compatibility", bc_ep_compatibility_req(self.beam_bf, self.beam_bf + 25),
                  bc_ep_compatibility_available(self.column_D, self.column_bf, self.column_tf, self.column_r1, self.column_clear_d, CONN_CWBW),
                  'Compatible' if self.bc_compatibility_status is True else 'Not compatible')
            self.report_check.append(t1)

        # CHECK 1: MEMBER CAPACITY
        t1 = ('SubSection', 'Member Capacity - Supported Section', '|p{4.5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (KEY_DISP_SHEAR_CAPACITY, '',
              cl_8_4_shear_yielding_capacity_member(h=self.h, t=self.supported_section.web_thickness, f_y=self.supported_section.fy,
                                                    gamma_m0=self.gamma_m0, V_dg=round(self.supported_section_shear_capa, 2), multiple=0.60),
              'Restricted to low shear')
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY, '',
              cl_8_2_1_2_plastic_moment_capacity(beta_b=self.beam_beta_b_z,
                                                 Z_p=self.supported_section.plast_sec_mod_z,
                                                 f_y=self.supported_section.fy,
                                                 gamma_m0=self.gamma_m0,
                                                 Pmc=round(self.supported_section_mom_capa_m_zz, 2), supporting_or_supported='Supported'),
              'V < 0.6 Vdy')
        self.report_check.append(t1)

        t1 = ('', '', '', '')
        self.report_check.append(t1)

        t1 = ('SubSection', 'Member Capacity - Supporting Section', '|p{4.5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY, '',
              cl_8_2_1_2_plastic_moment_capacity(beta_b=round(self.beta_b_z, 2), Z_p=self.supporting_section.plast_sec_mod_z,
                                                    f_y=self.supporting_section.fy, gamma_m0=self.gamma_m0, Pmc=round(self.M_dz, 2),
                                                 supporting_or_supported='Supporting'),
              self.col_classification)
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY, '',
              cl_8_2_1_2_plastic_moment_capacity_yy(beta_b=round(self.beta_b_y, 2), Z_py=self.supporting_section.plast_sec_mod_y,
                                                    f_y=self.supporting_section.fy, gamma_m0=self.gamma_m0, Pmc=round(self.M_dy, 2)),
              self.col_classification)
        self.report_check.append(t1)


        t1 = ('SubSection', 'Load Consideration', '|p{3.5cm}|p{5.3cm}|p{5.2cm}|p{1.5cm}|')
        self.report_check.append(t1)

        self.load_shear_min = min(round(0.15 * self.supported_section_shear_capa, 2), 40.0)
        self.load_moment_min = (0.5 * self.supported_section_mom_capa_m_zz)

        # t1 = (KEY_INTERACTION_RATIO, '', ir_sum_bb_cc(Al=self.input_axial_force, M=self.input_moment, A_c=self.supported_section_axial_capa,
        #                                               M_c=self.supported_section_mom_capa_m_zz, IR_axial=self.IR_axial, IR_moment=self.IR_moment,
        #                                               sum_IR=self.sum_IR),
        #       get_pass_fail(self.IR_moment, 1.0, relation='leq'))
        # self.report_check.append(t1)

        t1 = (KEY_DISP_AXIAL, '', display_prov(self.load_axial, "P_x"), "OK")
        self.report_check.append(t1)

        t1 = (KEY_DISP_SHEAR, display_prov(self.input_shear_force, "V_y"),
              prov_shear_force(shear_input=self.input_shear_force, min_sc=round(self.load_shear_min, 2),
                               app_shear_load=round(self.load_shear, 2), shear_capacity_1=self.supported_section_shear_capa),
              get_pass_fail(self.input_shear_force, self.load_shear, relation='leq'))
        self.report_check.append(t1)

        if self.connectivity == VALUES_CONN_1[0]:
            t1 = ("Bending Moment (major axis) (kNm)", display_prov(self.input_moment, "M_z"),
                  prov_moment_load(moment_input=self.input_moment, min_mc=round(self.load_moment_min, 2),
                                   app_moment_load=round(self.load_moment, 2),
                                   moment_capacity=round(self.supported_section_mom_capa_m_zz, 2), moment_capacity_supporting=self.M_dz,
                                   type='EndPlateType-BC-zz'), get_pass_fail(self.input_moment, self.load_moment, relation='leq'))
        else:
            t1 = ("Bending Moment (major axis) (kNm)", display_prov(self.input_moment, "M"),
                  prov_moment_load(moment_input=self.input_moment, min_mc=round(self.load_moment_min, 2),
                                   app_moment_load=round(self.load_moment, 2),
                                   moment_capacity=round(self.supported_section_mom_capa_m_zz, 2), moment_capacity_supporting=self.M_dy,
                                   type='EndPlateType-BC-yy'), get_pass_fail(self.input_moment, self.load_moment, relation='leq'))

        self.report_check.append(t1)

        t1 = ("Effective Bending Moment (major axis) (kNm)", '',
              effective_bending_moment_ep(self.load_moment, self.load_axial, self.load_moment_effective,
                                          self.beam_D, self.beam_tf), "OK")

        self.report_check.append(t1)

        if (len(self.plate_thickness_list) != 0) and (self.bolt_row != 0) and (self.bolt_column != 0):

            # CHECK 2: BOLT CHECKS
            t1 = ('SubSection', ' Bolt Optimization', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (
                KEY_OUT_DISP_D_PROVIDED, "Bolt Diameter Optimization", display_prov(int(self.bolt_diameter_provided), "d"),
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
                                        (max(self.beam_tf, self.beam_tw), self.supported_section.fu,
                                         self.supported_section.fy)]

            self.bolt.calculate_bolt_spacing_limits(self.bolt_diameter_provided, connected_plates_t_fu_fy, n=1)

            t1 = ('SubSection', ' Detailing', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (DISP_MIN_PITCH, cl_10_2_2_min_spacing(self.bolt_diameter_provided, parameter='pitch'),
                  self.pitch_distance_provided,
                  get_pass_fail(self.bolt.min_pitch, self.pitch_distance_provided, relation='leq'))
            self.report_check.append(t1)

            t7 = (
                DISP_MAX_PITCH, cl_10_2_3_1_max_spacing([self.plate_thickness, self.plate_thickness], parameter='pitch'),
                self.pitch_distance_provided,
                get_pass_fail(self.bolt.max_spacing, self.pitch_distance_provided, relation='geq'))
            self.report_check.append(t7)

            if self.bolt_column > 2:
                t1 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(self.bolt_diameter_provided, parameter='gauge'),
                      self.gauge_distance_provided,
                      get_pass_fail(self.bolt.min_pitch, self.gauge_distance_provided, relation='leq'))
                self.report_check.append(t1)

                t7 = (DISP_MAX_GAUGE,
                      cl_10_2_3_1_max_spacing([self.plate_thickness, self.plate_thickness], parameter='gauge'),
                      self.gauge_distance_provided,
                      get_pass_fail(self.bolt.max_spacing, self.gauge_distance_provided, relation='geq'))
                self.report_check.append(t7)

            t3 = (DISP_MIN_END,
                  cl_10_2_4_2_min_edge_end_dist(self.bolt_hole_diameter, self.bolt.edge_type, parameter='end_dist'),
                  self.end_distance_provided,
                  get_pass_fail(self.bolt.min_end_dist, self.end_distance_provided, relation='leq'))
            self.report_check.append(t3)

            t3 = (DISP_MAX_END, cl_10_2_4_3_max_edge_end_dist([(self.plate_thickness, self.plate.fu, self.plate.fy),
                                                               (self.plate_thickness, self.plate.fu, self.plate.fy)],
                                                              corrosive_influences=self.bolt.corrosive_influences,
                                                              parameter='end_dist'),
                  self.end_distance_provided,
                  get_pass_fail(self.bolt.min_edge_dist, self.end_distance_provided, relation='leq'))
            self.report_check.append(t3)

            t3 = (DISP_MIN_EDGE,
                  cl_10_2_4_2_min_edge_end_dist(self.bolt_hole_diameter, self.bolt.edge_type, parameter='edge_dist'),
                  self.edge_distance_provided,
                  get_pass_fail(self.bolt.min_end_dist, self.edge_distance_provided, relation='leq'))
            self.report_check.append(t3)

            t3 = (DISP_MAX_EDGE, cl_10_2_4_3_max_edge_end_dist([(self.plate_thickness, self.plate.fu, self.plate.fy),
                                                                (self.plate_thickness, self.plate.fu, self.plate.fy)],
                                                               corrosive_influences=self.bolt.corrosive_influences,
                                                               parameter='edge_dist'),
                  self.edge_distance_provided,
                  get_pass_fail(self.bolt.min_edge_dist, self.edge_distance_provided, relation='leq'))
            self.report_check.append(t3)

            t1 = (DISP_CS_GAUGE, '', self.gauge_cs_distance_provided, 'Pass')
            self.report_check.append(t1)

            t1 = ('SubSection', 'Critical Bolt Design', '|p{2.5cm}|p{6.7cm}|p{6.3cm}|p{1cm}|')
            self.report_check.append(t1)
            if self.bolt.bolt_type == TYP_BEARING:
                bolt_bearing_capacity_kn = round(self.bolt_bearing_capacity, 2)

                t1 = (KEY_OUT_DISP_BOLT_SHEAR, '', cl_10_3_3_bolt_shear_capacity(self.bolt_fu, 1,
                                                                                 self.bolt.bolt_net_area,
                                                                                 self.gamma_mb,
                                                                                 round(self.bolt_shear_capacity, 2)), 'OK')
                self.report_check.append(t1)

                t3 = (KEY_DISP_KB, '', cl_10_3_4_calculate_kb(self.end_distance_provided, self.pitch_distance_provided,
                                                              self.bolt_hole_diameter,
                                                              self.bolt_fu, self.supported_section.fu), 'OK')
                self.report_check.append(t3)

                t2 = (KEY_OUT_DISP_BOLT_BEARING, '', cl_10_3_4_bolt_bearing_capacity(round(self.bolt.kb, 2),
                                                                                     self.bolt_diameter_provided,
                                                                                     [(self.plate_thickness,
                                                                                       self.plate.fu, self.plate.fy),
                                                                                      (self.plate_thickness,
                                                                                       self.plate.fu, self.plate.fy)],
                                                                                     self.gamma_mb,
                                                                                     bolt_bearing_capacity_kn), 'OK')
                self.report_check.append(t2)

                t3 = ('Bolt Capacity (kN)', '',
                      cl_10_3_2_bolt_capacity(round(self.bolt_shear_capacity, 2), bolt_bearing_capacity_kn,
                                              round(self.bolt_capacity / self.call_helper.beta_lg, 2)),
                      '')
                self.report_check.append(t3)

                if self.connectivity == VALUES_CONN_1[0]:  # CF-BW
                    member_thk = self.column_tf
                else:  # CW-BW
                    member_thk = self.column_tw

                t3 = (KEY_OUT_LARGE_GRIP, '', large_grip_length(self.plate_thickness, member_thk, self.call_helper.grip_length,
                                                                           self.bolt_diameter_provided, self.call_helper.beta_lg),
                      get_pass_fail(self.call_helper.grip_length, 8 * self.bolt_diameter_provided, relation='leq'))
                self.report_check.append(t3)

                t3 = (KEY_OUT_BOLT_CAPACITY_REDUCED, '',
                      shear_capa_post_large_grip_length_red(self.call_helper.beta_lg, self.bolt_capacity),
                      'OK')
                self.report_check.append(t3)

                t3 = ('Shear Demand (per bolt) (kN)', bolt_shear_demand(V=self.load_shear, n_bolts=self.bolt_numbers,
                                                              V_sb=self.bolt_shear_demand, type='Bearing Bolt'),
                      display_prov(round(self.bolt_capacity, 2), 'V_{db}', ref=None),
                      get_pass_fail(self.bolt_shear_demand, round(self.bolt_capacity, 2), relation='leq'))
                self.report_check.append(t3)
            else:
                t4 = (KEY_OUT_DISP_BOLT_SLIP_DR, bolt_shear_demand(V=self.load_shear, n_bolts=self.bolt_numbers,
                                                                   V_sb=self.bolt_shear_demand),
                      cl_10_4_3_HSFG_bolt_capacity(mu_f=self.bolt.mu_f, n_e=1, K_h=1,
                                                   fub=self.bolt_fu,
                                                   Anb=self.bolt.bolt_net_area,
                                                   gamma_mf=self.bolt.gamma_mf,
                                                   capacity=round(self.bolt_capacity, 2)),
                      get_pass_fail(self.bolt_shear_demand, round(self.bolt_capacity, 2), relation='leq'))
                self.report_check.append(t4)

            t6 = (KEY_DISP_LEVER_ARM, lever_arm_end_plate(self.call_helper.lever_arm, self.bolt_row, ep_type=self.endplate_type), '',
                  'Pass' if self.design_status else 'Fail')
            self.report_check.append(t6)

            leverarm = self.call_helper.lever_arm

            if len(leverarm) > 0:

                r1 = leverarm[0]
                r_sum = 0
                for j in leverarm:
                    r_sum += j ** 2 / r1

                if len(leverarm) >= 3:
                    r_3 = leverarm[2]
                else:
                    r_3 = 0.0
                if len(leverarm) >= 4:
                    r_4 = leverarm[3]
                else:
                    r_4 = 0.0

                t6 = (KEY_OUT_DISP_CRITICAL_BOLT_TENSION,
                      tension_critical_bolt_prov(M=self.load_moment_effective, t_ba=round(self.tension_critical_bolt, 2),
                                                 n_c=self.bolt_column, r_1=round(r1, 2), n_r=self.bolt_row,
                                                 r_i=round(r_sum, 2), n=self.bolt_row, r_3=r_3, r_4=r_4, type=self.endplate_type),
                      "", "OK")
            else:
                t6 = (KEY_OUT_DISP_CRITICAL_BOLT_TENSION, "ERROR", "", "OK")

            self.report_check.append(t6)

            if self.bolt.bolt_tensioning == 'Pre-tensioned':
                beta = 1
            else:
                beta = 2

            l_v = round(self.call_helper.lv, 2)
            l_e = round(self.call_helper.le, 2)
            l_e2 = round(self.call_helper.le_2, 2)
            T_e = round(self.call_helper.t_1, 2)
            b_e = round(self.call_helper.b_e, 2)
            t = int(self.call_helper.plate_thickness)

            t1 = (KEY_OUT_DISP_BOLT_PRYING_FORCE_EP, cl_10_4_7_prying_force(l_v, l_e, l_e2, T_e, self.beta, self.proof_stress, b_e, t,
                                                              self.end_distance_provided,
                                                              self.beam_r1, self.dp_plate_fy, self.bolt_fu,
                                                              self.proof_stress, self.beam_bf,
                                                              self.bolt_column, self.prying_critical_bolt, eta=1.5),
                  '', 'OK' if self.design_status else 'Fail')
            self.report_check.append(t1)

            if self.bolt.bolt_type == "Bearing Bolt":
                t1 = (KEY_OUT_DISP_BOLT_TENSION_DEMAND, total_bolt_tension_force(T_ba=round(self.call_helper.t_1, 2),
                                                                      Q=round(self.prying_critical_bolt, 2),
                                                                      T_b=round(self.tension_demand_critical_bolt, 2),
                                                                      bolt_type=self.bolt.bolt_type),
                      cl_10_3_5_bearing_bolt_tension_resistance(self.bolt_fu, self.dp_bolt_fy,
                                                                self.bolt.bolt_shank_area, self.bolt.bolt_net_area,
                                                                round(self.tension_capacity_critical_bolt, 2),
                                                                fabrication=self.dp_weld_fab),
                      get_pass_fail(round(self.tension_demand_critical_bolt, 2),
                                    round(self.tension_capacity_critical_bolt, 2), relation='lesser'))
            else:
                t1 = (KEY_OUT_DISP_BOLT_TENSION_DEMAND, total_bolt_tension_force(T_ba=round(self.call_helper.t_1, 2),
                                                                      Q=round(self.prying_critical_bolt, 2),
                                                                      T_b=round(self.tension_demand_critical_bolt, 2),
                                                                      bolt_type=self.bolt.bolt_type),
                      cl_10_4_5_hsfg_bolt_tension_resistance(self.bolt_fu, self.dp_bolt_fy, self.bolt.bolt_shank_area,
                                                             self.bolt.bolt_net_area,
                                                             round(self.tension_capacity_critical_bolt, 2),
                                                             fabrication=self.dp_weld_fab),
                      get_pass_fail(round(self.tension_demand_critical_bolt, 2),
                                    round(self.tension_capacity_critical_bolt, 2), relation='lesser'))

            self.report_check.append(t1)

            if self.bolt.bolt_type == TYP_BEARING:
                t1 = ('Combined Capacity (I.R.)', required_IR_or_utilisation_ratio(IR=1),
                      cl_10_3_6_bearing_bolt_combined_shear_and_tension(round(self.bolt_shear_demand, 2),
                                                                        round(self.bolt_capacity, 2),
                                                                        round(self.tension_demand_critical_bolt, 2),
                                                                        round(self.tension_capacity_critical_bolt, 2),
                                                                        round(self.combined_capacity_critical_bolt, 2)),
                      get_pass_fail(1, round(self.combined_capacity_critical_bolt, 2), relation="geq"))
                self.report_check.append(t1)
            else:
                t1 = ('Combined Capacity, (I.R)', required_IR_or_utilisation_ratio(IR=1),
                      cl_10_4_6_friction_bolt_combined_shear_and_tension(round(self.bolt_shear_demand, 2),
                                                                         round(self.bolt_capacity, 2),
                                                                         round(self.tension_demand_critical_bolt, 2),
                                                                         round(self.tension_capacity_critical_bolt, 2),
                                                                         round(self.combined_capacity_critical_bolt,
                                                                               2)),
                      get_pass_fail(1, round(self.combined_capacity_critical_bolt, 2), relation="geq"))
                self.report_check.append(t1)

            # Check: Reaction at compression flange
            t1 = ('SubSection', 'Compression Flange Check', '|p{3.5cm}|p{4cm}|p{7.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = ('Tension in Bolt Rows (kN)', '', tension_list(self.call_helper.tension), 'OK')
            self.report_check.append(t1)

            tension_sum = sum(self.call_helper.tension)
            t1 = ('Reaction at Compression Flange (kN)', reaction_compression_flange(self.call_helper.r_c, self.bolt_column, self.bolt_row,
                                                                                     round(tension_sum, 2)),
                  compression_flange_capacity(self.beam_bf, self.beam_tf, self.supported_section.fy, self.gamma_m0, self.call_helper.flange_capacity),
                  get_pass_fail(self.call_helper.flange_capacity, self.call_helper.r_c, relation="geq"))
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

            t1 = (KEY_OUT_DISP_PLATE_WIDTH, "", bb_endplate_width_prov(B_ep=round(self.ep_width_provided, 2),
                                                                       B=self.supported_section.flange_width),
                  get_pass_fail(self.supported_section.flange_width, round(self.ep_width_provided, 2), relation="leq"))
            self.report_check.append(t1)

            t1 = ('Moment at Critical Section (kNm)', '',
                  moment_ep(t_1=round(self.call_helper.t_1, 2), lv=round(self.call_helper.lv, 2),
                            Q=round(self.call_helper.prying_force, 2), le=round(self.call_helper.le, 2),
                            mp_plate=round(self.ep_moment_capacity, 2)), "OK")

            self.report_check.append(t1)

            t1 = (KEY_DISP_PLATE_THICK,
                  end_plate_thk_req(M_ep=round(self.ep_moment_capacity, 2), b_eff=round(self.call_helper.b_e, 2),
                                    f_y=self.dp_plate_fy,
                                    gamma_m0=self.gamma_m0, t_p=self.call_helper.plate_thickness_req, t_b=0, q=0, l_e=0, l_v=0, f_o=0, b_e=0, beta=0,
                                    module='BC_EP'),
                  int(self.plate_thickness),
                  get_pass_fail(self.call_helper.plate_thickness_req, self.plate_thickness, relation="leq"))
            self.report_check.append(t1)

            t1 = (KEY_DISP_MOM_CAPACITY, round(self.ep_moment_capacity, 2),
                  end_plate_moment_capacity(M_ep=round(self.call_helper.plate_moment_capacity, 2),
                                            b_eff=round(self.call_helper.b_e, 2),
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
                                        D=self.supported_section.depth, h_sp=self.stiffener_height, type=self.endplate_type),
                  self.stiffener_height, 'Pass')
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_STIFFENER_LENGTH, ' ', stiffener_length_prov(h_sp=self.stiffener_height,
                                                                            l_sp=self.stiffener_length,
                                                                            type=self.endplate_type), 'Pass')
            self.report_check.append(t1)

            t1 = (KEY_OUT_DISP_STIFFENER_THICKNESS, display_prov(self.beam_tw, "t"),
                  display_prov(self.stiffener_thickness, "t_{st}"), 'Pass')
            self.report_check.append(t1)

            t1 = (DISP_WELD_SIZE, round(self.stiffener_weld.min_size), display_prov(self.weld_size_stiffener, 't_w'), 'Pass')
            self.report_check.append(t1)

            # ##################
            # # Weld Checks
            # ##################
            weld_conn_plates_fu = [self.dp_plate_fu, self.supported_section.fu, self.web_weld.fu]
            weld_conn_plates_tk = [self.plate_thickness, self.supported_section.web_thickness]

            t1 = (
                'SubSection', 'Weld Design - Beam Web to End Plate Connection', '|p{3.5cm}|p{5.3cm}|p{6.5cm}|p{1.2cm}|')
            self.report_check.append(t1)

            t1 = (DISP_WELD_STRENGTH_MPA, weld_fu(self.web_weld.fu, self.plate.fu), weld_fu_provided(self.weld_fu),
                  get_pass_fail(max(self.web_weld.fu, self.plate.fu), self.weld_fu, relation="geq"))
            self.report_check.append(t1)

            t1 = ('Total Weld Length (mm)', "", weld_length_web_prov(beam_D=self.supported_section.depth,
                                                                     beam_tf=self.supported_section.flange_thickness,
                                                                     beam_r1=self.supported_section.root_radius,
                                                                     L_weld=round(self.weld_length_web, 2)), "OK")
            self.report_check.append(t1)

            self.weld_size_web1 = round(
                (self.load_shear * 1e3 * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_length_web * self.weld_fu),
                2)  # mm

            t1 = (DISP_WELD_SIZE, weld_size_ep_web_req(load_shear=self.load_shear, gamma_mw=self.gamma_mb,
                                                         weld_length_web=round(self.weld_length_web, 2),
                                                         fu=self.weld_fu, weld_size_web=self.weld_size_web1),
                  self.weld_size_web,
                  get_pass_fail(self.weld_size_web1, self.weld_size_web, relation="leq"))
            self.report_check.append(t1)

            t1 = (DISP_MIN_WELD_SIZE,
                  cl_10_5_2_3_table_21_min_fillet_weld_size_required([self.plate_thickness, self.beam_tw],
                                                                     self.web_weld.min_size),
                  min_weld_size_ep_web_prov(weld_size_web=self.weld_size_web1,
                                            weld_size_web_provided=self.weld_size_web, min_size=self.web_weld.min_size),
                  get_pass_fail(max(self.weld_size_web1, self.web_weld.min_size), self.weld_size_web, relation="leq"))
            self.report_check.append(t1)

            t1 = (DISP_MAX_WELD_SIZE,
                  cl_10_5_3_1_max_weld_size_v2([self.plate_thickness, self.beam_tw], round(self.web_weld.max_size, 2)),
                  max_weld_size_ep_web_prov(weld_size_web=self.weld_size_web, max_size=round(self.web_weld.max_size, 2)),
                  get_pass_fail(self.web_weld.max_size, self.weld_size_web, relation="geq"))
            self.report_check.append(t1)

            if self.load_axial > 0.0:
                t1 = (KEY_OUT_DISP_WELD_NORMAL_STRESS, "",
                      f_a_stress_due_to_axial_force(A_f=self.load_axial, t_w=self.weld_size_web,
                                                    L_weld=self.weld_length_web,
                                                    f_a=round(self.f_a, 2)), "")
                self.report_check.append(t1)

                t1 = (KEY_OUT_DISP_WELD_SHEAR_STRESS, "",
                      q_stress_due_to_shear_force(V=self.load_shear, t_w=self.weld_size_web, L_weld=self.weld_length_web,
                                                  q=self.q), "")
                self.report_check.append(t1)

                # self.conn_plates_weld_fu1 = [self.web_weld.fu, self.web_weld.fu]  # todo trial
                t1 = (
                    KEY_OUT_DISP_WELD_STRESS_EQUIVALENT, f_e_weld_stress_due_to_combined_load(f_a=self.f_a, f_e=self.f_e, q=self.q),
                    cl_10_5_7_1_1_weld_strength(conn_plates_weld_fu=[self.weld_fu], gamma_mw=self.gamma_mb, t_t=1,
                                                f_w=round(self.allowable_stress, 2),
                                                type="end_plate"),
                    get_pass_fail(self.f_e, self.allowable_stress, relation="leq"))
                self.report_check.append(t1)

            # CHECK 3: Continuity Plate - Compression Flange CHECKS #

            if self.connectivity == VALUES_CONN_1[0]:

                if self.endplate_type == VALUES_ENDPLATE_TYPE[1]:
                    t1 = ('SubSection', 'Continuity Plate Check - Compression Flange', '|p{3.5cm}|p{4cm}|p{7.8cm}|p{1.2cm}|')
                else:
                    t1 = ('SubSection', 'Continuity Plate Check - Compression/Tension Flange', '|p{3.5cm}|p{4cm}|p{7.8cm}|p{1.2cm}|')
                self.report_check.append(t1)

                self.k = round(self.column_tf + self.column_r1, 2)
                self.f_wc = round(self.column_fy * self.column_tw, 2)

                t1 = ('Local Web Yielding Capacity (kN)', '', local_web_yielding(f_wc=self.f_wc, k=self.k, t_fb=self.beam_tf,
                                                                                 gamma_mo=self.gamma_m0, column_tf=self.column_tf,
                                                                                 column_r1=self.column_r1, column_fy=self.column_fy,
                                                                                 column_tw=self.column_tw, P_bf_1=self.p_bf_1), 'OK',)
                self.report_check.append(t1)

                t1 = ('Web Compression Buckling Capacity (kN)', '', compression_buckling_of_web(t_c=self.column_tw,
                                                                                                        fy_c=self.column_fy,
                                                                                                        h_c=self.h_c,
                                                                                                        k=self.k, gamma_mo=self.gamma_m0,
                                                                                                        D_c=self.column_D,
                                                                                                        P_cw_2=self.p_bf_2), 'OK')
                self.report_check.append(t1)

                t1 = ('Web Crippling Capacity (kN)', '', web_cripling(t_c=self.column_tw,
                                                                      fy_c=self.column_fy,
                                                                      T_b=self.beam_tf,
                                                                      gamma_m1=self.gamma_m1,
                                                                      D_c=self.column_D,
                                                                      P_cw_3=self.p_bf_3,
                                                                      T_c=self.column_tf), 'OK')
                self.report_check.append(t1)

                t1 = (KEY_OUT_DISP_COMP_STRENGTH, '', compressioncheck(P_cw_1=self.p_bf_1,
                                                                       P_cw_3=self.p_bf_3,
                                                                       P_cw_2=self.p_bf_2,
                                                                       P_bf=self.p_bf), 'OK')
                self.report_check.append(t1)

                if self.call_helper.r_c > self.p_bf:
                    remark = 'Yes'
                else:
                    remark = 'No'
                t1 = (KEY_OUT_DISP_CONT_PLATE_REQ, continuity_plate_req_1(self.call_helper.r_c),
                      continuity_plate_req_2(self.call_helper.r_c, self.p_bf), remark)
                self.report_check.append(t1)

                if self.continuity_plate_compression_flange_status == True:

                    if self.endplate_type == VALUES_ENDPLATE_TYPE[1]:
                        t1 = ('SubSection', 'Continuity Plate Design - Compression Flange ', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
                    else:
                        t1 = ('SubSection', 'Continuity Plate Design - Compression/Tension Flange ', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_AREA_REQ, Area_req_cont_plate(A_cp=round(self.cont_plate_area_req, 2),
                                                                        R_c=round(self.call_helper.r_c, 2),
                                                                        p_cw=round(self.p_bf, 2),
                                                                        f_ycp=self.cont_plate_fy,
                                                                        gamma_m0=self.gamma_m0), '', 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_NOTCH_SIZE, '', display_prov(self.notch_size, "n"), 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_LENGTH, '', comp_plate_length(l_cp1=self.cont_plate_length_out,
                                                                                      l_cp2=self.cont_plate_length_in,
                                                                                      D_c=self.column_D,
                                                                                      T_c=self.column_tf, n=self.notch_size), 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_WIDTH, '', comp_plate_width(column_bf=self.column_bf,
                                                                                    column_tw=self.column_tw,
                                                                                    notch_size=self.notch_size,
                                                                                    w_cp=self.cont_plate_width), 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_THK, comp_plate_thk_p(A_cp=round(self.cont_plate_area_req, 2), w_cp=self.cont_plate_width,
                                                                              l_cp=self.cont_plate_length_out,
                                                                              t_cp1=round(self.cont_plate_thk_req_1, 2),
                                                                              f_ycp=self.cont_plate_fy, t_cp2=round(self.cont_plate_thk_req_2, 2),
                                                                              t_cp3=round(self.cont_plate_thk_req_3, 2),
                                                                              epsilon_cp=round(self.cont_plate_epsilon, 2),
                                                                              t_cp=round(self.cont_plate_thk_req, 2), beam_tf=self.beam_tf),
                          self.cont_plate_thk_provided,
                          get_pass_fail(max(self.cont_plate_thk_req_1, self.cont_plate_thk_req_2, self.cont_plate_thk_req_3),
                                        self.cont_plate_thk_provided, relation="leq"))
                    self.report_check.append(t1)

                if self.endplate_type == VALUES_ENDPLATE_TYPE[1]:
                    t1 = ('SubSection', 'Continuity Plate Check - Tension Flange ', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
                    self.report_check.append(t1)

                    if self.t_bf > self.column_tf:
                        remark_1 = 'Yes'
                    else:
                        remark_1 = 'No'
                    t1 = (KEY_OUT_DISP_CONT_PLATE_REQ, check_tension_flange(beam_bf=self.beam_bf, beam_tf=self.beam_tf, gamma_m0=self.gamma_m0,
                                                                            t_bf=self.t_bf),
                          display_prov(self.column_tf, "T_c"), remark_1)
                    self.report_check.append(t1)

                    if self.continuity_plate_tension_flange_status == True:
                        t1 = ('SubSection', 'Continuity Plate Design - Tension Flange ', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
                        self.report_check.append(t1)

                        # if self.continuity_plate_compression_flange_status == False:
                        #     t1 = (KEY_OUT_DISP_AREA_REQ, Area_req_cont_plate(A_cp=round(self.cont_plate_area_req, 2),
                        #                                                         R_c=round(self.call_helper.r_c, 2),
                        #                                                         p_cw=round(self.p_bf, 2),
                        #                                                         f_ycp=self.cont_plate_fy,
                        #                                                         gamma_m0=self.gamma_m0), '', 'OK')
                        #     self.report_check.append(t1)

                        t1 = (KEY_OUT_DISP_NOTCH_SIZE, '', display_prov(self.notch_size, "n"), 'OK')
                        self.report_check.append(t1)

                        t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_LENGTH, '', comp_plate_length(l_cp1=self.cont_plate_length_out,
                                                                                          l_cp2=self.cont_plate_length_in,
                                                                                          D_c=self.column_D,
                                                                                          T_c=self.column_tf, n=self.notch_size), 'OK')
                        self.report_check.append(t1)
                        t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_WIDTH, '', comp_plate_width(column_bf=self.column_bf,
                                                                                        column_tw=self.column_tw,
                                                                                        notch_size=self.notch_size,
                                                                                        w_cp=self.cont_plate_width), 'OK')
                        self.report_check.append(t1)

                        if self.continuity_plate_compression_flange_status == False:
                            t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_THK, ten_plate_thk_p(A_cp=0.0, w_cp=0.0, t_cp1=0.0, t_cp2=self.beam_tf,
                                                                                     t_cp=round(self.cont_plate_thk_req, 2),
                                                                                     compression_cont_status=
                                                                                     self.continuity_plate_compression_flange_status),
                                  self.cont_plate_thk_provided,
                                  get_pass_fail(self.beam_tf, self.cont_plate_thk_provided, relation="leq"))
                        else:
                            t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_THK, ten_plate_thk_p(A_cp=round(self.cont_plate_area_req, 2),
                                                                                     w_cp=self.cont_plate_width,
                                                                                     t_cp1=round(self.cont_plate_thk_req_1, 2),
                                                                                     t_cp2=self.beam_tf,
                                                                                     t_cp=round(self.cont_plate_thk_req, 2),
                                                                                     compression_cont_status=
                                                                                     self.continuity_plate_compression_flange_status),
                                  self.cont_plate_thk_provided,
                                  get_pass_fail(max(self.cont_plate_thk_req_1, self.cont_plate_thk_req_3), self.cont_plate_thk_provided,
                                                relation="leq"))

                        self.report_check.append(t1)

                # Continuity plate weld design
                if (self.continuity_plate_compression_flange_status == True) or (self.continuity_plate_tension_flange_status == True):
                    t1 = ('SubSection', 'Weld Design - Continuity Plate', '|p{3.5cm}|p{6.3cm}|p{5.5cm}|p{1.2cm}|')
                    self.report_check.append(t1)

                    t1 = (DISP_WELD_STRENGTH_MPA, weld_fu_cp(self.continuity_plate_weld.fu, self.plate.fu), weld_fu_provided(self.weld_fu),
                          get_pass_fail(max(self.continuity_plate_weld.fu, self.plate.fu), self.weld_fu, relation="geq"))
                    self.report_check.append(t1)

                    t1 = (
                        'Total (effective) Weld Length (mm)', "",
                        weld_length_cp(self.weld_length_cont_plate, self.weld_both_side_cont_plate_status),
                        "OK")
                    self.report_check.append(t1)

                    weld_size_cp = ((self.p_c / 2) * 1e3 * math.sqrt(3) * self.gamma_mw) / (
                                0.7 * self.weld_length_cont_plate * self.weld_fu)  # mm

                    if self.continuity_plate_compression_flange_status == True:
                        t1 = (
                            DISP_WELD_SIZE,
                            weld_size_cp_req(self.call_helper.r_c, self.p_bf, self.gamma_mw, self.weld_length_cont_plate, self.weld_fu,
                                             round(weld_size_cp, 2)),
                            self.weld_size_continuity_plate,
                            get_pass_fail(weld_size_cp, self.weld_size_continuity_plate, relation="leq"))
                    else:
                        t1 = (DISP_WELD_SIZE, self.weld_size_continuity_plate, self.weld_size_continuity_plate, 'Pass')

                    self.report_check.append(t1)

                    if weld_size_cp <= 0:
                        weld_size_cp = self.weld_size_continuity_plate

                    t1 = (DISP_MIN_WELD_SIZE,
                          cl_10_5_2_3_table_21_min_fillet_weld_size_required([self.cont_plate_thk_provided, self.column_tw],
                                                                             self.continuity_plate_weld.min_size),
                          min_weld_size_ep_web_prov(weld_size_web=round(weld_size_cp, 2),
                                                    weld_size_web_provided=self.weld_size_continuity_plate,
                                                    min_size=self.continuity_plate_weld.min_size),
                          get_pass_fail(max(weld_size_cp, self.continuity_plate_weld.min_size), self.weld_size_continuity_plate, relation="leq"))
                    self.report_check.append(t1)

                    t1 = (DISP_MAX_WELD_SIZE,
                          cl_10_5_3_1_max_weld_size_v2([self.cont_plate_thk_provided, self.column_tw], round(self.continuity_plate_weld.max_size)),
                          max_weld_size_ep_web_prov(weld_size_web=self.weld_size_continuity_plate, max_size=round(self.continuity_plate_weld.max_size)),
                          get_pass_fail(self.continuity_plate_weld.max_size, weld_size_cp, relation="geq"))
                    self.report_check.append(t1)

            else:
                if (self.continuity_plate_compression_flange_status == True) or (self.continuity_plate_tension_flange_status == True):
                    t1 = ('SubSection', 'Continuity Plate Design', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_NOTCH_SIZE, '', display_prov(self.notch_size, "n"), 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_LENGTH, '', comp_plate_length(l_cp1=self.cont_plate_length_out,
                                                                                      l_cp2=self.cont_plate_length_in,
                                                                                      D_c=self.column_D,
                                                                                      T_c=self.column_tf, n=self.notch_size), 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_WIDTH, '', comp_plate_width(column_bf=self.column_bf,
                                                                                    column_tw=self.column_tw,
                                                                                    notch_size=self.notch_size,
                                                                                    w_cp=self.cont_plate_width), 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_THK, 'tc = ' + str(self.column_tw), self.cont_plate_thk_provided,
                          get_pass_fail(self.column_tw, self.cont_plate_thk_provided, relation="leq"))
                    self.report_check.append(t1)

                    # Continuity plate weld design
                    t1 = ('SubSection', 'Weld Design - Continuity Plate', '|p{3.5cm}|p{6.3cm}|p{5.5cm}|p{1.2cm}|')
                    self.report_check.append(t1)

                    t1 = (DISP_WELD_STRENGTH_MPA, weld_fu_cp(self.continuity_plate_weld.fu, self.plate.fu), weld_fu_provided(self.weld_fu),
                          get_pass_fail(max(self.continuity_plate_weld.fu, self.plate.fu), self.weld_fu, relation="geq"))
                    self.report_check.append(t1)

                    t1 = (
                    'Total (effective) Weld Length (mm)', "", weld_length_cp(self.weld_length_cont_plate, self.weld_both_side_cont_plate_status),
                    "OK")
                    self.report_check.append(t1)

                    t1 = (DISP_WELD_SIZE, round(self.continuity_plate_weld.min_size), self.weld_size_continuity_plate, 'Pass')
                    self.report_check.append(t1)

                    t1 = (DISP_MIN_WELD_SIZE,
                          cl_10_5_2_3_table_21_min_fillet_weld_size_required([self.cont_plate_thk_provided, self.column_tw],
                                                                             self.continuity_plate_weld.min_size),
                          min_weld_size_ep_web_prov(weld_size_web=round(self.weld_size_continuity_plate, 2),
                                                    weld_size_web_provided=self.weld_size_continuity_plate, min_size=self.continuity_plate_weld.min_size),
                          get_pass_fail(max(self.weld_size_continuity_plate, self.continuity_plate_weld.min_size), self.weld_size_continuity_plate,
                                        relation="leq"))
                    self.report_check.append(t1)

                    t1 = (DISP_MAX_WELD_SIZE,
                          cl_10_5_3_1_max_weld_size_v2([self.cont_plate_thk_provided, self.column_tw], round(self.continuity_plate_weld.max_size)),
                          max_weld_size_ep_web_prov(weld_size_web=self.weld_size_continuity_plate, max_size=round(self.continuity_plate_weld.max_size)),
                          get_pass_fail(self.continuity_plate_weld.max_size, self.weld_size_continuity_plate, relation="geq"))
                    self.report_check.append(t1)

            # CHECK WEB STIFFENER
            if self.connectivity == VALUES_CONN_1[0]:  # Column Flange - Beam Web
                t1 = ('SubSection', 'Column Web Shear Check', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                if self.web_stiffener_status == True:
                    remark_1 = 'Yes'
                else:
                    remark_1 = 'No'

                t1 = (KEY_OUT_DISP_DIAG_PLATE_REQ,
                      checkdiagonal_plate(M=self.load_moment_effective,
                                          D_c=self.column_D,
                                          D_b=self.beam_D,
                                          fyc=self.column_fy,
                                          t_req=self.t_wc),
                      display_prov(self.column_tw, "t_c"), remark_1)
                self.report_check.append(t1)

                if self.web_stiffener_status == True:

                    t1 = ('SubSection', 'Column Web Stiffener Plate Design', '|p{3.5cm}|p{4cm}|p{7cm}|p{1.5cm}|')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_DIAGONAL_PLATE_DEPTH, '', web_stiffener_plate_depth(depth=self.web_stiffener_depth, D_b=self.beam_D,
                                                                                  T_b=self.beam_tf, r1_b=self.beam_r1), 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_DIAGONAL_PLATE_WIDTH, '', web_stiffener_plate_width(width=self.web_stiffener_width, D_c=self.column_D,
                                                                                           T_c=self.column_tf, r1_c=self.column_r1), 'OK')
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_CONTINUITY_PLATE_THK, web_stiffener_plate_thk(self.t_wc, self.column_tw, self.web_stiffener_thk_req),
                          self.web_stiffener_thk_provided,
                          get_pass_fail(self.web_stiffener_thk_req, self.web_stiffener_thk_provided, relation="leq"))
                    self.report_check.append(t1)

                    t1 = (DISP_WELD_SIZE, self.web_stiffener_weld.min_size, self.weld_size_web_stiffener, 'Pass')

                    self.report_check.append(t1)
        else:
            if self.bolt_row == 0:

                # CHECK 2: BOLT CHECKS
                t1 = ('SubSection', ' Bolt Optimization', '|p{3.5cm}|p{6cm}|p{5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t1 = (
                    KEY_OUT_DISP_D_PROVIDED, "Bolt Diameter Optimization", display_prov(int(self.bolt_diameter_provided), "d"),
                    'Pass' if self.design_status else 'Fail')
                self.report_check.append(t1)

                t1 = (
                KEY_OUT_DISP_GRD_PROVIDED, "Bolt Property Class Optimization", self.bolt_grade_provided, 'Pass' if self.design_status else 'Fail')
                self.report_check.append(t1)

                t1 = (KEY_DISP_BOLT_HOLE, " ", display_prov(self.bolt_hole_diameter, "d_0"), 'OK')
                self.report_check.append(t1)

                t6 = (DISP_NUM_OF_COLUMNS, '', display_prov(self.bolt_column, "n_c"), 'Pass' if self.design_status else 'Fail')
                self.report_check.append(t6)

                t7 = (DISP_NUM_OF_ROWS, '', display_prov(self.bolt_row, "n_r"), 'Pass' if self.design_status else 'Fail')
                self.report_check.append(t7)

                t1 = (KEY_OUT_DISP_NO_BOLTS, '', display_prov(self.bolt_numbers, "n = n_r X n_c"), 'Pass' if self.design_status else 'Fail')
                self.report_check.append(t1)

        # End of design report

        if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
            path_detailing = '/ResourceFiles/images/Detailing-Flush.png'
        elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
            path_detailing = '/ResourceFiles/images/Detailing-OWE.png'
        else:  # Both-way
            path_detailing = '/ResourceFiles/images/Detailing-BWE.png'

        if self.connectivity == VALUES_CONN_1[1]:  # CW-BW
            if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
                path_stiffener = '/ResourceFiles/images/BC-CW-BW_Flush.png'
            elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
                path_stiffener = '/ResourceFiles/images/BC-CW-BW_EOW.png'
            else:  # Both-way
                path_stiffener = '/ResourceFiles/images/BC-CW-BW_EBW.png'
        else:  # CF-BW
            if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:  # Flush EP
                path_stiffener = '/ResourceFiles/images/BC_Stiffener_Flush.png'
            elif self.endplate_type == VALUES_ENDPLATE_TYPE[1]:  # One-way
                path_stiffener = '/ResourceFiles/images/BC_Stiffener_OWE.png'
            else:  # Both-way
                path_stiffener = '/ResourceFiles/images/BC_Stiffener_BWE.png'

        path_weld = "/ResourceFiles/images/BB-BC-single_bevel_groove.png"

        Disp_2d_image = [path_weld, path_detailing, path_stiffener]
        Disp_3d_image = "/ResourceFiles/images/3d.png"
        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")

        fname_no_ext = popup_summary['filename']

        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_2d_image, Disp_3d_image, module=self.module)
