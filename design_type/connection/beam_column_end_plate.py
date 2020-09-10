"""
@Author:    Danish Ansari - Osdag Team, IIT Bombay [(P) danishdyp@gmail.com / danishansari@iitb.ac.in]

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
        self.mid_bolt_row = 0
        self.bolt_column = 0
        self.bolt_row = 0

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
        self.supported_section_shear_capa = 0.0
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

        self.dp_plate_fy = 0.0
        self.dp_plate_fu = 0.0

        self.bc_compatibility_status = False
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

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, VALUES_CONN_1, True, 'No Validator')
        options_list.append(t2)

        t2 = (KEY_ENDPLATE_TYPE, KEY_DISP_ENDPLATE_TYPE, TYPE_COMBOBOX, VALUES_ENDPLATE_TYPE, True, 'No Validator')
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, "./ResourceFiles/images/webflush.png", True, 'No Validator')
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

        t1 = ([KEY_ENDPLATE_TYPE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t1)

        t2 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t2)

        return lst

    def fn_conn_image(self):
        """ display representative images of end plate type """
        conn = self[0]
        ep_type = self[1]

        if conn == 'Column Flange - Beam Web' and ep_type == 'Flushed - Reversible Moment':
            return './ResourceFiles/images/cf_bw_flush.png'
        elif conn == 'Column Flange - Beam Web' and ep_type == 'Extended One Way - Irreversible Moment':
            return './ResourceFiles/images/cf_bw_eow.png'
        elif conn in 'Column Flange - Beam Web' and ep_type == 'Extended Both Ways - Reversible Moment':
            return './ResourceFiles/images/cf_bw_ebw.png'
        elif conn == 'Column Web - Beam Web' and ep_type == 'Flushed - Reversible Moment':
            return './ResourceFiles/images/cw_bw_flush.png'
        elif conn == 'Column Web - Beam Web' and ep_type == 'Extended One Way - Irreversible Moment':
            return './ResourceFiles/images/cw_bw_eow.png'
        elif conn in 'Column Web - Beam Web' and ep_type == 'Extended Both Ways - Reversible Moment':
            return './ResourceFiles/images/cw_bw_ebw.png'
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

        t22 = (KEY_OUT_DETAILING_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX, self.gauge_distance_provided if flag else '', True)
        out_list.append(t22)

        t22 = (KEY_OUT_DETAILING_CS_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_CS_GAUGE_DISTANCE, TYPE_TEXTBOX, self.gauge_cs_distance_provided if flag else '',
        True)
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

        self.load = Load(shear_force=float(design_dictionary[KEY_SHEAR]),
                         axial_force=float(design_dictionary[KEY_AXIAL]),
                         moment=float(design_dictionary[KEY_MOMENT]), unit_kNm=True)

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

        self.call_helper = EndPlateSpliceHelper(supported_section=self.supported_section, load=self.load,
                                                bolt=self.bolt, ep_type=self.endplate_type,
                                                plate_design_status=False, helper_file_design_status=False)

        # call functions for design
        self.check_compatibility(self)
        self.check_minimum_design_action(self)
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

        ######################
        self.hard_input(self)
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
        if self.connectivity is VALUES_CONN_1[1]:  # Column Web - Beam Web
            column_clear_d = self.column_D - (2 * self.column_tf) - (2 * self.column_r1) - 10  # 10 mm is the erection tolerance, 5 mm on each side

            if (self.beam_bf + 25) > column_clear_d:  # 25 mm is the total extension of the end plate along its width
                self.bc_compatibility_status = False
                self.design_status = False
                logger.error(": The selected supporting column {} cannot accommodate the selected supported beam {}".
                             format(self.supporting_section.designation, self.supported_section.designation))
                logger.warning(": Width of the supported beam by considering the maximum end plate width (B + 25 mm), is more than the clear depth "
                               "available at the supporting column")
                logger.warning(": Width of supported beam should be less than or equal to {} mm".format(column_clear_d))
                logger.info(": Define a beam or a column of suitable compatibility and re-design")
            else:
                self.bc_compatibility_status = True

        else:  # Column flange connectivity
            if (self.beam_bf + 25) > self.column_bf:
                self.bc_compatibility_status = False
                self.design_status = False
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
        self.load.moment = round(self.load.moment * 1e-6, 2)  # kN-m
        self.load_shear = self.load.shear_force * 1e-3  # kN
        self.load_axial = round(max(self.load.axial_force, 1) * 1e-3, 2)  # kN

        # moment capacity of the beam
        self.supported_section_mom_capa_m_zz = round(((1 * self.beam_zp_zz * self.beam_fy) / self.gamma_m0) * 1e-6, 2)  # kN-m

        if self.load.moment < (0.5 * self.supported_section_mom_capa_m_zz):
            self.minimum_load_status_moment = True
            # update moment value
            self.load_moment = round(0.5 * self.supported_section_mom_capa_m_zz, 2)  # kN

            logger.warning("[Minimum Factored Load] The external factored bending moment ({} kN-m) is less than 0.5 times the plastic moment "
                           "capacity of the beam ({} kN-m)".format(self.load.moment, self.load_moment))
            logger.info("The minimum factored bending moment should be at least 0.5 times the plastic moment capacity of the beam to qualify the "
                        "connection as rigid and transfer full moment from the beam to the column (Cl. 10.7, IS 800:2007)")
            logger.info("Designing the connection for a load of {} kN-m".format(self.load_moment))

        elif self.load.moment > self.supported_section_mom_capa_m_zz:
            self.load_moment = self.supported_section_mom_capa_m_zz  # kN
            self.minimum_load_status_moment = True
            self.design_status = False
            logger.error("[Maximum Factored Load] The external factored bending moment ({} kN-m) is greater than the plastic moment capacity of the "
                         "beam ({} kN-m)".format(self.load.moment, self.supported_section_mom_capa_m_zz))
            logger.warning("The maximum capacity of the connection is {} kN-m".format(self.supported_section_mom_capa_m_zz))
            logger.info("Define the value of factored bending moment as {} kN-m or less".format(self.supported_section_mom_capa_m_zz))
        else:
            self.minimum_load_status_moment = False
            self.load_moment = self.load.moment  # kN-m

        # Note: Shear force is transferred to the column through the web, hence Cl.10.7 point 2 is considered for minimum shear load
        if self.supported_section.type == 'Rolled':
            self.supported_section_shear_capa = ((self.beam_D * self.beam_tw) * self.beam_fy) / self.gamma_m0
        else:  # built-up sections
            self.supported_section_shear_capa = (((self.beam_D - (2 * self.beam_tf)) * self.beam_tw) * self.beam_fy) / self.gamma_m0
        self.supported_section_shear_capa = round(self.supported_section_shear_capa * 1e-3, 2)  # kN

        if self.load_shear < min((0.15 * self.supported_section_shear_capa), 40):
            self.minimum_load_status_shear = True
            self.load_shear = min((0.15 * self.supported_section_shear_capa), 40)
            logger.warning("[Minimum Factored Load] The external factored shear force ({} kN) is less than the minimum recommended design action on "
                           "the member".format(self.load_shear))
            logger.info("The minimum factored shear force should be at least {} (0.15 times the shear capacity of the beam) or 40 kN whichever is "
                        "less [Ref. Cl. 10.7, IS 800:2007]".format(0.15 * self.supported_section_shear_capa))
            logger.info("Designing the connection for a factored shear load of {} kN-m".format(self.load_shear))
        elif self.load_shear > self.supported_section_shear_capa:
            self.load_shear = self.supported_section_shear_capa  # kN
            self.minimum_load_status_moment = True
            self.design_status = False
            logger.error("[Maximum Factored Load] The external factored shear force ({} kN) is greater than the shear capacity of the "
                         "beam ({} kN)".format(self.load_shear, self.supported_section_shear_capa))
            logger.warning("The maximum capacity of the connection is {} kN".format(self.supported_section_shear_capa))
            logger.info("Define the value of factored shear force as {} kN or less".format(self.supported_section_shear_capa))
        else:
            self.minimum_load_status_shear = False

        # effective moment is the moment due to external factored moment plus moment due to axial force
        self.load_moment_effective = round(self.load_moment + (self.load_axial * ((self.beam_D / 2) - (self.beam_tf / 2))) * 1e-3, 2)  # kN-m

        # TODO: check if the moment from the beam can be taken by the defined column (beam-column presizing check)

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
            if self.connectivity is VALUES_CONN_1[1]:  # 'Column flange-Beam web'

                if i > max(self.beam_tf, self.beam_tw, self.column_tf):
                    self.plate_thickness.append(i)
                    logger.warning("[End Plate] The end plate of {} mm is thinner than the thickest of the elements being connected".format(i))
                    logger.info("Selecting a plate of higher thickness which is at least {} mm thick".format(max(self.beam_tf, self.beam_tw,
                                                                                                                 self.column_tf)))

            else:  # 'Column web-Beam web'
                if i > max(self.beam_tf, self.beam_tw, self.column_tw):
                    self.plate_thickness.append(i)
                    logger.warning("[End Plate] The end plate of {} mm is thinner than the thickest of the elements being connected".format(i))
                    logger.info("Selecting a plate of higher thickness which is at least {} mm thick".format(max(self.beam_tf, self.beam_tw,
                                                                                                                 self.column_tw)))

        self.plate_thickness = self.plate_thickness  # final list of plate thicknesses considered for simulation

        # checking if the list contains at least one plate of thk higher than the minimum required
        if len(self.plate_thickness) == 0:
            self.design_status = False
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
            if self.helper_file_design_status == False:

                self.plate_thickness = i  # assigns plate thickness from the list

                # self.helper_file_design_status = False  # initialize helper file status as False to activate the bolt design loop

                # selecting a single dia-grade combination (from the list of a tuple) each time for performing all the checks
                for j in self.bolt_list:
                    if self.helper_file_design_status == False:

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
                        if self.connectivity == VALUES_CONN_1[1]:  # 'Column flange-Beam web'
                            self.gauge_cs_distance_provided = max(self.beam_tw, self.column_tw) + (2 * self.end_distance_provided)
                        else:
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
                        self.space_min_req_inside_D = (2 * self.end_distance_provided) + self.pitch_distance_provided

                        if self.space_available_inside_D < self.space_min_req_inside_D:
                            self.design_status = False
                            logger.error("[Compatibility Error]: The given beam cannot accommodate at least a single row of bolt (inside top and "
                                         "bottom flange) with a trial diameter of {} mm ".format(self.bolt_diameter_provided))
                            logger.info("Re-design the connection by defining a bolt of smaller diameter or beam of a suitable depth ")
                            self.rows_inside_D_max = 0
                        else:
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
                        # logger.info("Checking the design with the following number of column and rows combination {}".format(combined_list))

                        # selecting each possible combination of column and row iteratively to perform design checks
                        # starting from minimum column and row to maximum until overall bolt design status is True
                        for item in combined_list:
                            if self.helper_file_design_status == False:
                                select_list = item  # selected tuple from the list

                                self.bolt_column = select_list[0]
                                self.bolt_row = select_list[1]

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
                                                                                        self.plate_thickness, self.dp_plate_fu)

                                # checking for the maximum pitch distance of the bolts for a safe design
                                # if space is available then add rows
                                if self.call_helper.helper_file_design_status == True:

                                    # step 1: max pitch distance
                                    self.pitch_distance_max = self.cl_10_2_3_1_max_spacing([self.plate_thickness])
                                    print("PITCH MAX {}".format(self.pitch_distance_max))

                                    # step 2: checking space availability to accommodate extra rows based on maximum pitch criteria
                                    if self.endplate_type == VALUES_ENDPLATE_TYPE[0] or VALUES_ENDPLATE_TYPE[2]:  # flushed or both way

                                        if self.endplate_type == VALUES_ENDPLATE_TYPE[0]:
                                            self.space_available_web = self.call_helper.lever_arm[-2] - self.call_helper.lever_arm[-1]

                                        else:
                                            if (self.bolt_row / 2) <= 3:
                                                rows_inside_D = self.bolt_row - 2  # one row each outside top and bottom flange
                                            else:
                                                rows_inside_D = self.bolt_row - 4  # two rows each outside top and bottom flange

                                            self.space_available_web = self.beam_D - (2 * self.beam_tf) - (2 * self.end_distance_provided) - \
                                                                       ((rows_inside_D - 2) * self.pitch_distance_provided)
                                    else:  # one way connection
                                        if self.bolt_row <= 4:
                                            rows_inside_D = self.bolt_row - 1
                                        else:
                                            rows_inside_D = self.bolt_row - 2

                                        self.space_available_web = self.beam_D - (2 * self.beam_tf) - (2 * self.end_distance_provided) - \
                                                                   ((rows_inside_D - 2) * self.pitch_distance_provided)

                                    print("SPACE AVAILABLE IS {}".format(self.space_available_web))

                                    # step 3: adding rows to satisfy detailing criteria
                                    if self.space_available_web > self.pitch_distance_max:
                                        self.bolt_row_web = round_up(self.space_available_web / self.pitch_distance_max, 1) - 1
                                    else:
                                        self.bolt_row_web = 0

                                    # step 4: re-design the connection if more rows are added
                                    if self.bolt_row_web >= 1:

                                        self.pitch_distance_web = self.space_available_web / (self.bolt_row_web + 1)
                                        print("ACTUAL PITCH {}".format(self.pitch_distance_web))

                                        # run the bolt and end plate check function from the helper class
                                        self.design_bolt = self.call_helper.perform_bolt_design(self.endplate_type, self.supported_section,
                                                                                                self.gamma_m0,
                                                                                                self.bolt_column, self.bolt_row, self.bolt_row_web,
                                                                                                self.bolt_diameter_provided,
                                                                                                self.bolt_grade_provided, self.load_moment_effective,
                                                                                                self.end_distance_provided,
                                                                                                self.pitch_distance_provided, self.pitch_distance_web,
                                                                                                self.beta, self.proof_stress, self.dp_plate_fy,
                                                                                                self.plate_thickness, self.dp_plate_fu)

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
                                self.bolt_numbers = self.bolt_column * self.bolt_row
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
                                        "capacity ({} kN)".format(self.call_helper.bolt_tension_demand, self.call_helper.bolt_tension_capacity))
                                    logger.info("Re-designing the connection with a bolt of higher grade and/or diameter")
                                else:
                                    logger.info("[Bolt Design] The bolt of {} mm diameter and {} grade passes the tension check".
                                                format(self.bolt_diameter_provided, self.bolt_grade_provided))
                                    logger.info("Total tension demand on bolt (due to direct tension + prying action) is {} kN and the bolt tension "
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

        # results of overall safe design

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
        self.bolt_row = self.call_helper.bolt_row
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
            if self.bolt_row < 8:  # 1 row outside tension and compression flange
                self.ep_height_provided = self.beam_D + (2 * (2 * self.end_distance_provided))
            else:  # 2 rows outside tension and compression flange which is maximum allowable
                self.ep_height_provided = self.beam_D + (2 * (2 * self.end_distance_provided)) + (
                        2 * self.pitch_distance_provided)

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
        self.weld_size_web = round_up(self.weld_size_web, 2)

        self.web_weld.set_min_max_sizes(self.plate_thickness, self.beam_tw, special_circumstance=False, fusion_face_angle=90)

        self.weld_size_web = max(self.weld_size_web, self.web_weld.min_size)  # mm

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
            logger.error(": Overall beam to beam end plate splice connection design is UNSAFE")
            logger.info(": =========================End Of design===========================")

    # def compression_flange(self):
    #     # Strength of flange under compression or tension TODO: Get function from IS 800
    #
    #     A_f = self.supported_section.flange_width * self.supported_section.flange_thickness  # area of beam flange
    #     capacity_beam_flange = (self.supported_section.fy / gamma_m0) * A_f
    #     force_flange = max(t_bf, p_bf)
    #
    #     if capacity_beam_flange < force_flange:
    #         # design_status = False
    #         logger.error(": Forces in the beam flange is greater than its load carrying capacity")
    #         logger.warning(": The maximum allowable force on beam flange of selected section is %2.2f kN"
    #                        % (round(capacity_beam_flange / 1000, 3)))
    #         logger.info(": Use a higher beam section with wider and/or thicker flange")
    #
    # # Weld design
    # def assign_weld_sizes(self):
    #     """Assign minimum required weld sizes to flange and web welds and update throat sizes, eff. lengths,
    #     long joint factors"""
    #
    #     print("Assigning minimum required weld sizes to flange and web welds")
    #     # Find minimum and maximum weld sizes
    #     self.top_flange_weld.set_min_max_sizes(part1_thickness=self.supported_section.flange_thickness,
    #                                            part2_thickness=self.plate.thickness_provided)
    #     self.bottom_flange_weld.set_min_max_sizes(part1_thickness=self.supported_section.flange_thickness,
    #                                               part2_thickness=self.plate.thickness_provided)
    #     self.web_weld.set_min_max_sizes(part1_thickness=self.supported_section.web_thickness,
    #                                     part2_thickness=self.plate.thickness_provided)
    #
    #     # Assign minimum sizes
    #     top_flange_weld_size = choose_higher_value(self.top_flange_weld.min_size, ALL_WELD_SIZES)
    #     bottom_flange_weld_size = choose_higher_value(self.bottom_flange_weld.min_size, ALL_WELD_SIZES)
    #     web_weld_size = choose_higher_value(self.web_weld.min_size, ALL_WELD_SIZES)
    #
    #     self.top_flange_weld.set_size(weld_size=top_flange_weld_size)
    #     self.bottom_flange_weld.set_size(weld_size=bottom_flange_weld_size)
    #     self.web_weld.set_size(weld_size=web_weld_size)
    #     return
    #
    # def assign_weld_lengths(self):
    #     """Available and effective weld lengths are found and multiplied with long joint reduction factors"""
    #
    #     # Available lengths
    #     self.top_flange_weld.length = self.supported_section.flange_width
    #     self.bottom_flange_weld.length = (
    #         self.supported_section.flange_width - self.supported_section.web_thickness -
    #         2*self.supported_section.root_radius - 2*self.supported_section.toe_radius) / 2
    #     self.web_weld.length = self.supported_section.depth - 2 * (self.supported_section.flange_thickness +
    #                                                                     self.supported_section.root_radius)
    #
    # def assign_weld_strength(self):
    #     # TODO: Move this method to weld class
    #     self.top_flange_weld.strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #         ultimate_stresses=[self.supported_section.fu, self.top_flange_weld.fu],
    #         fabrication=self.top_flange_weld.fabrication)
    #     self.bottom_flange_weld.strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #         ultimate_stresses=[self.supported_section.fu, self.bottom_flange_weld.fu],
    #         fabrication=self.bottom_flange_weld.fabrication)
    #     self.web_weld.strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #         ultimate_stresses=[self.supported_section.fu, self.web_weld.fu],
    #         fabrication=self.web_weld.fabrication)
    #     return
    #
    # def check_fillet_weld1(self):
    #     """
    #     axial force is taken by flange and web welds = P/(2*lw+ltf+lbf)
    #     shear force is taken by web welds only = V/(2*lw)
    #     moment is taken by flange welds only M/(d-tf) / (ltf+lbf)
    #     """
    #     print("Checking the weld size provided assuming axial force is taken by flange and web welds,"
    #           " shear force is taken by web welds only and moment is taken by flange welds only")
    #     # Design forces per unit length of welds due to applied loads
    #     # Applied axial force acting on unit length of weld group [flange+web welds]
    #     weld_force_axial = self.load.axial_force / (
    #             2 * (self.top_flange_weld.eff_length * self.top_flange_weld.lj_factor +
    #                  2 * self.bottom_flange_weld.eff_length * self.bottom_flange_weld.lj_factor +
    #                  self.web_weld.eff_length * self.web_weld.lj_factor))
    #
    #     # Applied moment acting on unit length of weld group [flange welds]
    #     flange_tension_moment = self.load.moment / (self.supported_section.depth -
    #                                                 self.supported_section.flange_thickness)
    #     weld_force_moment = flange_tension_moment / (self.top_flange_weld.eff_length +
    #                                                  2 * self.bottom_flange_weld.eff_length)
    #
    #     # Applied shear force acting on unit length of weld group [web welds]
    #     weld_force_shear = self.load.shear_force / (2 * self.web_weld.eff_length * self.web_weld.lj_factor)
    #
    #     # check for weld strength
    #     flange_weld_stress = (weld_force_moment + weld_force_axial) / self.top_flange_weld.throat_tk
    #     # flange_weld_throat_reqd = round((weld_force_moment + weld_force_axial) / self.top_flange_weld.strength, 3)
    #     # flange_weld_size_reqd = round(flange_weld_throat_reqd / 0.7, 3)
    #
    #     web_weld_stress = math.sqrt(weld_force_axial ** 2 + weld_force_shear ** 2) / self.web_weld.throat_tk
    #     # web_weld_throat_reqd = round(math.sqrt(weld_force_axial ** 2 + weld_force_shear ** 2) /
    #     #                              self.web_weld.strength, 3)
    #     # web_weld_size_reqd = round(web_weld_throat_reqd / 0.7, 3)
    #     if self.top_flange_weld.strength < flange_weld_stress:
    #         self.top_flange_weld.design_status = False
    #     if self.bottom_flange_weld.strength < flange_weld_stress:
    #         self.bottom_flange_weld.design_status = False
    #     if self.web_weld.strength < web_weld_stress:
    #         self.web_weld.design_status = False
    #
    # def check_fillet_weld2(self):
    #     """
    #     axial force is taken by flange and web welds = P/(2*lw+ltf+lbf)
    #     shear force is taken by web welds only = V/(2*lw)
    #     moment is taken by both flange and web welds = M/Z
    #     z = ltf*lw/2 + lbf*lw/2 + d^2/3
    #
    #     Stress for axial load in beam=Axial load/sum of (individual weld length *corresponding weld throat thickness)
    #     Total length for flange weld = 2* self.top_flange_weld.eff_length + 4* self.bottom_flange_weld.eff_length
    #     Weld throat thickness for flange = self.top_flange_weld.throat_tk
    #     Total length for web weld = 2* self.web_weld.eff_length
    #     Weld throat thickness for flange = self.web_weld.throat_tk
    #     """
    #     print("Checking the weld size provided assuming axial force is taken by flange and web welds,"
    #           " shear force is taken by web welds only and moment is taken by both flange and web welds")
    #
    #     # Stresses on weld due to applied axial force TODO: Check if this method is correct
    #     weld_force_axial_stress = self.load.axial_force / (
    #             2 * self.top_flange_weld.eff_length * self.top_flange_weld.lj_factor * self.top_flange_weld.throat_tk +
    #             4 * self.bottom_flange_weld.eff_length * self.bottom_flange_weld.lj_factor *
    #                                                                                 self.top_flange_weld.throat_tk +
    #             2 * self.web_weld.eff_length * self.web_weld.lj_factor * self.web_weld.throat_tk)
    #
    #     # Stresses in extreme weld (top flange) due to applied moment
    #     weld_Iz = (2 * (self.web_weld.eff_length ** 3) / 12) * self.web_weld.throat_tk +\
    #               (2 * self.top_flange_weld.eff_length * (self.supported_section.depth / 2) ** 2 +
    #                4 * self.bottom_flange_weld.eff_length * (
    #                        self.supported_section.depth / 2 -
    #                        self.supported_section.flange_thickness) ** 2) * self.top_flange_weld.throat_tk
    #
    #     flange_weld_Z = weld_Iz / (self.supported_section.depth / 2)
    #     web_weld_Z = weld_Iz / (self.supported_section.depth / 2 - self.supported_section.flange_thickness -
    #                             self.supported_section.root_radius)
    #
    #     flange_weld_stress = self.load.moment / flange_weld_Z + weld_force_axial_stress
    #
    #     weld_force_shear = self.load.shear_force / (
    #                 2 * self.web_weld.eff_length * self.web_weld.throat_tk * self.web_weld.lj_factor)
    #
    #     # calculation of required weld size is not accurate since Iz has different web and flange sizes
    #     # but to get required throat thickness either flange or weld size is multiplied
    #     # flange_weld_throat_reqd = round(flange_weld_stress * self.top_flange_weld.throat_tk /
    #     #                                 self.top_flange_weld.strength, 3)
    #     # flange_weld_size_reqd = round(flange_weld_throat_reqd / 0.7, 3)
    #
    #     web_weld_stress = math.sqrt((self.load.moment / web_weld_Z + weld_force_axial_stress) ** 2 +
    #                                 weld_force_shear ** 2)
    #
    #     # web_weld_throat_reqd = round(web_weld_stress * self.web_weld.throat_tk /
    #     #                              self.web_weld.strength, 3)
    #     # web_weld_size_reqd = round(web_weld_throat_reqd / 0.7, 3)
    #
    #     if self.top_flange_weld.strength < flange_weld_stress:
    #         self.top_flange_weld.design_status = False
    #     if self.bottom_flange_weld.strength < flange_weld_stress:
    #         self.bottom_flange_weld.design_status = False
    #     if self.web_weld.strength < web_weld_stress:
    #         self.web_weld.design_status = False
    #
    # def groove_weld(self):
    #     # TODO: Incomplete.
    #     self.top_flange_weld.throat_tk = IS800_2007.cl_10_5_3_3_groove_weld_effective_throat_thickness(
    #         self.supported_section.flange_thickness, self.plate.thickness_provided)
    #     self.top_flange_weld.size = self.top_flange_weld.throat_tk
    #
    #     self.web_weld.throat_tk = IS800_2007.cl_10_5_3_3_groove_weld_effective_throat_thickness(
    #         self.supported_section.web_thickness, self.plate.thickness_provided)
    #     self.web_weld.size = self.web_weld.throat_tk
    #
    # def weld_design(self):
    #     print("Designing weld between beam and end plate")
    #     if self.web_weld.type == KEY_DP_WELD_TYPE_FILLET:
    #         self.assign_weld_strength()
    #         self.assign_weld_lengths()
    #         self.assign_weld_sizes()
    #         self.check_fillet_weld1()
    #         while (self.top_flange_weld.design_status and self.bottom_flange_weld.design_status) is False:
    #             print("Updating weld size for flange welds")
    #             current_flange_weld_size = min(self.top_flange_weld.size, self.bottom_flange_weld.size)
    #             next_flange_weld_size = choose_next_value(current_value=current_flange_weld_size,
    #                                                       available_values=ALL_WELD_SIZES,
    #                                                       max_value=self.top_flange_weld.max_size)
    #             if next_flange_weld_size is None:
    #                 print("flange weld size can not be attained")
    #                 break   # TODO: exit with, design status = False and message "weld size can not be attained"
    #             self.top_flange_weld.set_size(next_flange_weld_size)
    #             self.bottom_flange_weld.set_size(next_flange_weld_size)
    #             self.check_fillet_weld1()
    #         while self.web_weld.design_status is False:
    #             print("Updating weld size web welds")
    #             next_web_weld_size = choose_next_value(current_value=self.web_weld.size,
    #                                                    available_values=ALL_WELD_SIZES,
    #                                                    max_value=self.web_weld.max_size)
    #             if next_web_weld_size is None:
    #                 print("web weld size can not be attained")
    #                 break   # TODO: exit with, design status = False and message "weld size can not be attained"
    #             self.web_weld.set_size(next_web_weld_size)
    #             self.check_fillet_weld1()
    #
    #     else:
    #         pass
    #
    # def find_bolt_conn_plates_t_fu_fy(self):
    #     self.bolt_conn_plates_t_fu_fy = [(self.plate.thickness_provided, self.plate.fu, self.plate.fy)]
    #     # Column web connectivity
    #     if self.connectivity is VALUES_CONN_1[1]:
    #         self.bolt_conn_plates_t_fu_fy.append(
    #             (self.supported_section.web_thickness, self.supported_section.fu, self.supported_section.fy))
    #     else:
    #         self.bolt_conn_plates_t_fu_fy.append(
    #             (self.supported_section.flange_thickness, self.supported_section.fu, self.supported_section.fy))
    #
    # def bolt_design(self):
    #     #######################################################################
    #
    #     if self.bolt.bolt_type == "Friction Grip Bolt":
    #         bolt_slip_capacity = IS800_2007.cl_10_4_3_bolt_slip_resistance(
    #             f_ub=self.bolt.bolt_fu, A_nb=self.bolt.bolt_net_area, n_e=1, mu_f=self.bolt.mu_f, bolt_hole_type=self.bolt.bolt_hole_type)
    #         bolt_tension_capacity = IS800_2007.cl_10_4_5_friction_bolt_tension_resistance(
    #             f_ub=self.bolt.bolt_fu, f_yb=self.bolt.bolt_fy, A_sb=self.bolt.bolt_shank_area, A_n=self.bolt.bolt_net_area)
    #         bearing_capacity = 0.0
    #         bolt_shear_capacity = 0.0
    #         bolt_capacity = bolt_slip_capacity
    #
    #     else:
    #         bolt_shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity(
    #             f_u=self.bolt.bolt_fu, A_nb=self.bolt.bolt_net_area, A_sb=self.bolt.bolt_shank_area, n_n=1, n_s=0)
    #         bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
    #             f_u=min(self.supporting_section.fu, self.plate.fu), f_ub=self.bolt.bolt_fu, t=sum(bolt_plates_tk), d=self.bolt.bolt_diameter_provided, e=self.bolt.edge_dist,
    #             p=self.bolt.pitch, bolt_hole_type=self.bolt.bolt_hole_type)
    #         bolt_slip_capacity = 0.0
    #         bolt_capacity = min(bolt_shear_capacity, bearing_capacity)
    #         bolt_tension_capacity = IS800_2007.cl_10_3_5_bearing_bolt_tension_resistance(
    #             f_ub=self.bolt.bolt_fu, f_yb=self.bolt.bolt_fy, A_sb=self.bolt.bolt_shank_area, A_n=self.bolt.bolt_net_area)
    #
    #     #######################################################################
    #
    #     # Calculation for number of bolts around tension flange
    #     flange_tension = self.load.moment / (self.supported_section.depth - self.supported_section.flange_thickness) + self.load.axial_force / 2
    #     no_tension_side_rqd = flange_tension / (0.80 * bolt_tension_capacity)
    #     no_tension_side = round_up(no_tension_side_rqd, multiplier=2, minimum_value=2)
    #
    #     b_e = self.supported_section.flange_width / 2
    #     prying_force = IS800_2007.cl_10_4_7_bolt_prying_force(
    #         T_e=flange_tension / 4, l_v=l_v, f_o=0.7 * self.bolt.bolt_fu, b_e=b_e, t=self.plate.thickness_provided, f_y=self.plate.fy,
    #         end_dist=self.bolt.end_dist, pre_tensioned=False)
    #
    #     # Detailing
    #     bolt_combined_status = False
    #     detailing_status = True
    #     while bolt_combined_status is False:
    #
    #         if self.endplate_type == 'flush':
    #             number_of_bolts = 2 * no_tension_side
    #
    #             if no_tension_side == 2:
    #                 no_rows = {'out_tension_flange': 0, 'in_tension_flange': 1,
    #                            'out_compression_flange': 0, 'in_compression_flange': 1}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < self.bolt.pitch:
    #                     detailing_status = False
    #
    #             elif no_tension_side == 4:
    #                 no_rows = {'out_tension_flange': 0, 'in_tension_flange': 2,
    #                            'out_compression_flange': 0, 'in_compression_flange': 2}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < 3 * self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # # logger.warning()
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #                     # TODO Re-detail the connection
    #                     # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
    #                     #            'out_compression_flange': 2, 'in_compression_flange': 1}
    #
    #             elif no_tension_side == 6:
    #                 no_rows = {'out_tension_flange': 0, 'in_tension_flange': 3,
    #                            'out_compression_flange': 0, 'in_compression_flange': 3}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < 5 * self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #                     #  Re-detail the connection
    #                     # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
    #                     #            'out_compression_flange': 3, 'in_compression_flange': 1}
    #
    #             else:
    #                 detailing_status = False
    #                 # logger.error("Large number of bolts are required for the connection")
    #                 # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #                 no_rows = {'out_tension_flange': (no_tension_side - 6) / 2, 'in_tension_flange': 2,
    #                            'out_compression_flange': (no_tension_side - 6) / 2, 'in_compression_flange': 2}
    #
    #             # #######################################################################
    #
    #         elif self.endplate_type == 'one_way':
    #             number_of_bolts = no_tension_side + 2
    #             if no_tension_side <= 4:
    #                 no_tension_side = 4
    #                 number_of_bolts = no_tension_side + 2
    #                 no_rows = {'out_tension_flange': 1, 'in_tension_flange': 1,
    #                            'out_compression_flange': 0, 'in_compression_flange': 1}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # # logger.warning()
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #                     #  Re-detail the connection
    #                     # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
    #                     #            'out_compression_flange': 0, 'in_compression_flange': 1}
    #
    #             elif no_tension_side == 6:
    #                 no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
    #                            'out_compression_flange': 0, 'in_compression_flange': 1}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < 2 * self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # # logger.warning()
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #                     #  Re-detail the connection
    #                     # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
    #                     #            'out_compression_flange': 0, 'in_compression_flange': 1}
    #
    #             elif no_tension_side == 8:
    #                 no_rows = {'out_tension_flange': 1, 'in_tension_flange': 3,
    #                            'out_compression_flange': 0, 'in_compression_flange': 1}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < 3 * self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #                     #  Re-detail the connection
    #                     # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
    #                     #            'out_compression_flange': 0, 'in_compression_flange': 1}
    #             elif no_tension_side == 10:
    #                 no_rows = {'out_tension_flange': 2, 'in_tension_flange': 3,
    #                            'out_compression_flange': 0, 'in_compression_flange': 1}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < 3 * self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #             else:
    #                 detailing_status = False
    #                 # logger.error("Large number of bolts are required for the connection")
    #                 # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #                 no_rows = {'out_tension_flange': (no_tension_side - 6) / 2, 'in_tension_flange': 2,
    #                            'out_compression_flange': (no_tension_side - 6) / 2, 'in_compression_flange': 2}
    #
    #             # #######################################################################
    #
    #         else:  # self.endplate_type == "both_way":
    #             number_of_bolts = 2 * no_tension_side
    #
    #             if no_tension_side <= 4:
    #                 no_tension_side = 4
    #                 number_of_bolts = 2 * no_tension_side
    #                 no_rows = {'out_tension_flange': 1, 'in_tension_flange': 1,
    #                            'out_compression_flange': 1, 'in_compression_flange': 1}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < self.bolt.pitch:
    #                     detailing_status = False
    #
    #             elif no_tension_side == 6:
    #                 no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
    #                            'out_compression_flange': 1, 'in_compression_flange': 2}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < 3 * self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # # logger.warning()
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #                     #  Re-detail the connection
    #                     # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
    #                     #            'out_compression_flange': 2, 'in_compression_flange': 1}
    #
    #             elif no_tension_side == 8:
    #                 no_rows = {'out_tension_flange': 1, 'in_tension_flange': 3,
    #                            'out_compression_flange': 1, 'in_compression_flange': 3}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < 5 * self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #                     #  Re-detail the connection
    #                     # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
    #                     #            'out_compression_flange': 3, 'in_compression_flange': 1}
    #             elif no_tension_side == 10:
    #                 no_rows = {'out_tension_flange': 2, 'in_tension_flange': 3,
    #                            'out_compression_flange': 2, 'in_compression_flange': 3}
    #                 if self.supported_section.depth - 2 * self.supported_section.flange_thickness - 2 * l_v < 5 * self.bolt.pitch:
    #                     detailing_status = False
    #                     # logger.error("Large number of bolts are required for the connection")
    #                     # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #
    #             else:
    #                 detailing_status = False
    #                 # logger.error("Large number of bolts are required for the connection")
    #                 # logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #                 no_rows = {'out_tension_flange': (no_tension_side - 6) / 2, 'in_tension_flange': 2,
    #                            'out_compression_flange': (no_tension_side - 6) / 2, 'in_compression_flange': 2}
    #
    #             # #######################################################################
    #
    #             # Plate height and width
    #             ''' tens_plate_no_pitch : projection of end plate beyond the beam flange excluding the
    #                                         distances b/w bolts on tension side '''
    #         if no_rows['out_tension_flange'] == 0:
    #             tens_plate_outer = flange_projection
    #         else:
    #             tens_plate_outer = self.bolt.end_dist + l_v + (no_rows['out_tension_flange'] - 1) * self.bolt.pitch
    #         if no_rows['out_compression_flange'] == 0:
    #             comp_plate_outer = flange_projection
    #         else:
    #             comp_plate_outer = self.bolt.end_dist + l_v + (no_rows['out_compression_flange'] - 1) * self.bolt.pitch
    #
    #         plate_height = self.supported_section.depth + comp_plate_outer + tens_plate_outer
    #         self.plate.width = g_1 + 2 * self.bolt.edge_dist
    #         while self.plate.width < self.supported_section.flange_width:
    #             self.bolt.edge_dist += 5
    #             self.plate.width = g_1 + 2 * self.bolt.edge_dist
    #             if self.bolt.edge_dist > self.bolt.max_edge_dist:
    #                 self.bolt.edge_dist -= 5
    #                 g_1 += 5
    #                 self.plate.width = g_1 + 2 * self.bolt.edge_dist
    #                 # TODO: Apply max limit for g_1, design fails
    #
    #         if self.plate.width > self.plate.width_max:
    #             design_status = False
    #             logger.error(": Required plate width is more than the available width")
    #             logger.warning(": Width of plate should be less than %s mm" % self.plate.width_max)
    #             logger.info(": Currently, Osdag doesn't design such connections")
    #
    #         # Tension in bolts
    #         axial_tension = self.load.axial_force / number_of_bolts
    #         if no_rows['out_tension_flange'] == 0:
    #             extreme_bolt_dist = self.supported_section.depth - self.supported_section.flange_thickness * 3 / 2 - l_v
    #         else:
    #             extreme_bolt_dist = self.supported_section.depth - self.supported_section.flange_thickness / 2 + l_v + (no_rows['out_tension_flange'] - 1) * self.bolt.pitch
    #         sigma_yi_sq = 0
    #         for bolt_row in range(int(no_rows['out_tension_flange'])):
    #             print("out_tension_flange", bolt_row, self.supported_section.depth - self.supported_section.flange_thickness / 2 + l_v + bolt_row * self.bolt.pitch)
    #             sigma_yi_sq += (self.supported_section.depth - self.supported_section.flange_thickness / 2 + l_v + bolt_row * self.bolt.pitch) ** 2
    #
    #         for bolt_row in range(int(no_rows['in_tension_flange'])):
    #             print("in_tension_flange", bolt_row, self.supported_section.depth - 3 * self.supported_section.flange_thickness / 2 - l_v - bolt_row * self.bolt.pitch)
    #             sigma_yi_sq += (self.supported_section.depth - 3 * self.supported_section.flange_thickness / 2 - l_v - bolt_row * self.bolt.pitch) ** 2
    #
    #         for bolt_row in range(int(no_rows['in_compression_flange'])):
    #             print("in_compression_flange", bolt_row, self.supported_section.flange_thickness / 2 + l_v + bolt_row * self.bolt.pitch)
    #             sigma_yi_sq += (self.supported_section.flange_thickness / 2 + l_v + bolt_row * self.bolt.pitch) ** 2
    #
    #         moment_tension = self.load.moment * extreme_bolt_dist / sigma_yi_sq / 2
    #         tension_in_bolt = axial_tension + moment_tension + prying_force
    #         shear_in_bolt = self.load.shear_force / number_of_bolts
    #
    #         # Check for combined tension and shear
    #         if self.bolt.bolt_type == "Friction Grip Bolt":
    #             combined_capacity = IS800_2007.cl_10_4_6_friction_bolt_combined_shear_and_tension(
    #                 V_sf=shear_in_bolt, V_df=bolt_capacity, T_f=tension_in_bolt, T_df=bolt_tension_capacity)
    #         else:
    #             combined_capacity = IS800_2007.cl_10_3_6_bearing_bolt_combined_shear_and_tension(
    #                 V_sb=shear_in_bolt, V_db=bolt_capacity, T_b=tension_in_bolt, T_db=bolt_tension_capacity)
    #         bolt_combined_status = combined_capacity <= 1.0
    #
    #         if bolt_combined_status is False:
    #             no_tension_side += 2
    #         if detailing_status is False:
    #             design_status = False
    #             logger.error("Large number of bolts are required for the connection")
    #             logger.info(": Re-design the connection using bolt of higher grade or diameter")
    #             break
    #
    #         # Prying force
    #
    #         print("prying force:", prying_force)
    #         # toe_of_weld_moment = abs(flange_tension/4 * l_v - prying_force * self.bolt.end_dist)
    #         toe_of_weld_moment = abs(tension_in_bolt * l_v - prying_force * self.bolt.end_dist)
    #         end_plate_thickness_min = math.sqrt(toe_of_weld_moment * 1.10 * 4 / (self.plate.fy * b_e))
    #
    #         # End Plate Thickness
    #         if self.plate.thickness_provided < max(self.supporting_section.flange_thickness, end_plate_thickness_min):
    #             end_plate_thickness_min = math.ceil(max(self.supporting_section.flange_thickness, end_plate_thickness_min))
    #             design_status = False
    #             logger.error(": Chosen end plate thickness is not sufficient")
    #             logger.warning(": Minimum required thickness of end plate is %2.2f mm " % end_plate_thickness_min)
    #             logger.info(": Increase the thickness of end plate ")
    #     #######################################################################
    #
    # def find_end_plate_spacing(self):
    #     #######################################################################
    #     # l_v = Distance from the edge of flange to the centre of the nearer bolt (mm) [AISC design guide 16]
    #     # g_1 = Gauge 1 distance (mm) (also known as cross-centre gauge, Steel designers manual, pp733, 6th edition - 2003)
    #     self.endplate_type = ""
    #     if self.endplate_type == 'flush':
    #         l_v = 45.0
    #         g_1 = 90.0
    #     elif self.endplate_type == 'one_way':
    #         l_v = 50.0
    #         g_1 = 100.0
    #     else:  # self.endplate_type == 'both_ways':
    #         l_v = 50.0
    #         g_1 = 100.0
    #
    #     if self.top_flange_weld.type is KEY_DP_WELD_TYPE_FILLET:
    #         flange_projection = round_up(value=self.top_flange_weld.size + 2, multiplier=5, minimum_value=5)
    #     else:  # 'groove'
    #         flange_projection = 5
    #
    # def continuity_plaste(self):
    #     # Continuity Plates
    #     cont_plate_fu = self.supported_section.fu
    #     cont_plate_fy = self.supported_section.fy
    #     cont_plate_e = math.sqrt(250 / cont_plate_fy)
    #     gamma_m0 = 1.10
    #     gamma_m1 = 1.10
    #
    #     # Continuity Plates on compression side
    #     p_bf = self.load.moment / (self.supported_section.depth - self.supported_section.flange_thickness) - self.load.axial_force  # Compressive force at beam flanges
    #     cont_plate_comp_length = self.supporting_section.depth - 2 * self.supporting_section.flange_thickness
    #     cont_plate_comp_width = (self.supporting_section.flange_width - self.supporting_section.web_thickness) / 2
    #     notch_cont_comp = round_up(value=self.supporting_section.root_radius, multiplier=5, minimum_value=5)
    #     available_cont_comp_width = cont_plate_comp_width - notch_cont_comp
    #     available_cont_comp_length = cont_plate_comp_length - 2 * notch_cont_comp
    #
    #     col_web_capacity_yielding = self.supporting_section.web_thickness * (5 * self.supporting_section.flange_thickness + 5 * self.supporting_section.root_radius + self.supported_section.flange_thickness) * self.supporting_section.fy / gamma_m0
    #     col_web_capacity_crippling = ((300 * self.supporting_section.web_thickness ** 2) / gamma_m1) * (
    #             1 + 3 * (self.supported_section.flange_thickness / self.supporting_section.depth) * (self.supporting_section.web_thickness / self.supporting_section.flange_thickness) ** 1.5) * math.sqrt(
    #         self.supporting_section.fy * self.supporting_section.flange_thickness / self.supporting_section.web_thickness)
    #     col_web_capacity_buckling = (10710 * (self.supporting_section.web_thickness ** 3) / self.supporting_section.depth) * math.sqrt(self.supporting_section.fy / gamma_m0)
    #     col_web_capacity = min(col_web_capacity_yielding, col_web_capacity_crippling, col_web_capacity_buckling)
    #     cont_plate_comp_tk_local_buckling = cont_plate_comp_width / (9.4 * cont_plate_e)
    #     cont_plate_comp_tk_min = max(cont_plate_comp_tk_local_buckling, self.supported_section.flange_thickness,
    #                                  (p_bf - col_web_capacity) / (cont_plate_comp_width * cont_plate_fy / gamma_m0))
    #     cont_plate_comp_tk = cont_plate_comp_tk_min
    #     available_plates = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 32, 34, 35, 36, 40, 45, 50, 55, 60]
    #     for plate_tk in available_plates:
    #         if plate_tk >= cont_plate_comp_tk_min:
    #             cont_plate_comp_tk = plate_tk
    #             break
    #
    #     # Continuity Plates on tension side
    #     t_bf = self.load.moment / (self.supported_section.depth - self.supported_section.flange_thickness) + self.load.axial_force  # Tensile force at beam flanges
    #     cont_plate_tens_length = self.supporting_section.depth - 2 * self.supporting_section.flange_thickness
    #     cont_plate_tens_width = (self.supporting_section.flange_width - self.supporting_section.web_thickness) / 2
    #     notch_cont_tens = round_up(value=self.supporting_section.root_radius, multiplier=5, minimum_value=5)
    #     available_cont_tens_width = cont_plate_tens_width - notch_cont_tens
    #     available_cont_tens_length = cont_plate_tens_length - 2 * notch_cont_tens
    #
    #     col_flange_tens_capacity = (self.supporting_section.flange_thickness ** 2) * self.supported_section.fy / (0.16 * gamma_m0)
    #     cont_plate_tens_tk_min = (t_bf - col_flange_tens_capacity) / (cont_plate_tens_width * cont_plate_fy / gamma_m0)
    #     cont_plate_tens_tk = cont_plate_tens_tk_min
    #     for plate_tk in available_plates:
    #         if plate_tk >= cont_plate_tens_tk_min:
    #             cont_plate_tens_tk = plate_tk
    #             break
    #
    #     # conisering both plates thickness as same for practical reasons
    #     if cont_plate_comp_tk > cont_plate_tens_tk:
    #         cont_plate_tens_tk = cont_plate_comp_tk
    #     else:
    #         cont_plate_comp_tk = cont_plate_tens_tk
    #
    #     welds_sizes = [3, 4, 5, 6, 8, 10, 12, 14, 16]
    #     # continuity plate weld design on compression side
    #     # same is assumed for tension side
    #     cont_web_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(cont_plate_comp_tk, self.supporting_section.web_thickness)
    #     cont_web_weld_size_max = min(self.supported_section.web_thickness, cont_plate_comp_tk)
    #     available_welds = list([x for x in welds_sizes if (cont_web_weld_size_min <= x <= cont_web_weld_size_max)])
    #     for cont_web_weld_size in available_welds:
    #         cont_web_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
    #             fillet_size=cont_web_weld_size, fusion_face_angle=90)
    #         cont_web_weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
    #             fillet_size=cont_web_weld_size, available_length=available_cont_comp_length)
    #         if (max(p_bf, t_bf) / 2) / (2 * cont_web_weld_eff_length * cont_web_weld_throat) <= \
    #                 IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #                     ultimate_stresses=(weld_fu, self.supporting_section.fu, cont_plate_fu)):
    #             break
    #
    #     cont_flange_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(cont_plate_comp_tk, self.supporting_section.flange_thickness)
    #     cont_flange_weld_size_max = max(self.supporting_section.flange_thickness, cont_plate_comp_tk)
    #     available_welds = list(
    #         [x for x in welds_sizes if (cont_flange_weld_size_min <= x <= cont_flange_weld_size_max)])
    #     for cont_flange_weld_size in available_welds:
    #         cont_flange_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
    #             fillet_size=cont_flange_weld_size, fusion_face_angle=90)
    #         cont_flange_Weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
    #             fillet_size=cont_flange_weld_size, available_length=available_cont_comp_width)
    #         cont_axial_stress = (max(p_bf, t_bf) / 2) / (4 * cont_flange_Weld_eff_length * cont_flange_weld_throat)
    #         cont_moment_stress = (max(p_bf, t_bf) / 2) * (l_v + self.supported_section.web_thickness / 2) / (
    #                 cont_plate_comp_length * cont_flange_weld_throat * 4 * cont_flange_Weld_eff_length)
    #         if math.sqrt(
    #                 cont_axial_stress ** 2 + cont_moment_stress ** 2) <= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #             ultimate_stresses=(weld_fu, self.supporting_section.fu, cont_plate_fu)):
    #             break
    #     # same weld size is considered for flange and web connectivity of continuity plates
    #     # TODO: Should we recalculate stresses for common weld thickness?
    #     # TODO: what if this maximum size exceeds limits of one connection?
    #
    #     cont_weld_size = max(cont_flange_weld_size, cont_web_weld_size)
    #
    #     # continuity plate warnings
    #     if math.sqrt(
    #             cont_axial_stress ** 2 + cont_moment_stress ** 2) >= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #         ultimate_stresses=(weld_fu, self.supporting_section.fu, cont_plate_fu)):
    #         logger.warning("weld between column flange and continuity plates is not safe")
    #
    #     if (max(p_bf, t_bf) / 2) / (2 * cont_web_weld_eff_length * cont_web_weld_throat) >= \
    #             IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #                 ultimate_stresses=(weld_fu, self.supporting_section.fu, cont_plate_fu)):
    #         logger.warning("weld between column web and continuity plates is not safe")
    #
    #     # Note: for more number of iteration more numbers of  available size should be provided
    #
    # def stiffener(self):
    #     # Beam stiffeners
    #     st_status = False
    #     if self.endplate_type == 'flush':
    #         st_number = 0
    #     elif self.endplate_type == 'one_way':
    #         st_number = 1
    #         if number_of_bolts >= 12:
    #             st_status = True
    #     else:
    #         st_number = 2
    #         if number_of_bolts >= 20:
    #             st_status = True
    #
    #     st_fu = self.supported_section.fu
    #     st_fy = self.supported_section.fy
    #     st_height = l_v + self.bolt.pitch + self.bolt.end_dist
    #     # for plate_tk in available_plates:
    #     #     if plate_tk >= self.supported_section.web_thickness:
    #     #         st_thickness = plate_tk
    #     #         break
    #     available_thickness = list([x for x in available_plates if (self.supported_section.web_thickness <= x <= max(available_plates))])
    #     st_thickness = min(available_thickness)
    #     st_length_min = st_height + 100.0
    #     st_notch_top = 50.0
    #     st_notch_bottom = round_up(value=weld_thickness_flange, multiplier=5, minimum_value=5)
    #
    #     st_force = 4 * tension_in_bolt
    #     st_moment = st_force * (l_v + self.bolt.pitch / 2)
    #     st_length = st_length_min
    #     st_beam_weld = 3.0
    #     if st_status is True:
    #         # stiffener plate design
    #         for st_thickness in available_thickness:
    #             print(st_thickness)
    #             while st_length <= float(int(self.supported_section.depth / 100) * 100):
    #                 st_eff_length = st_length - st_notch_bottom
    #                 st_shear_capacity = st_eff_length * st_thickness * st_fy / (math.sqrt(3) * gamma_m0)
    #                 st_moment_capacity = st_eff_length ** 2 * st_thickness * st_fy / (4 * gamma_m0)
    #                 print(st_thickness, st_length, st_shear_capacity, st_moment_capacity, st_force, st_moment)
    #                 if st_moment <= st_moment_capacity and st_force <= st_shear_capacity:
    #                     break
    #                 else:
    #                     st_length += 20
    #             if st_moment <= st_moment_capacity and st_force <= st_shear_capacity:
    #                 break
    #             else:
    #                 st_length = st_length_min
    #
    #         # Stiffener Weld Design
    #         st_beam_weld_min = IS800_2007.cl_10_5_2_3_min_weld_size(st_thickness, self.supported_section.flange_thickness)
    #         st_beam_weld_max = max(self.supported_section.flange_thickness, st_thickness)
    #
    #         available_welds = list([x for x in welds_sizes if (st_beam_weld_min <= x <= st_beam_weld_max)])
    #         for st_beam_weld in available_welds:
    #             if st_beam_weld <= st_beam_weld_min:
    #                 st_beam_weld = st_beam_weld_min
    #             st_beam_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
    #                 fillet_size=st_beam_weld, fusion_face_angle=90)
    #             st_beam_weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
    #                 fillet_size=st_beam_weld, available_length=st_eff_length)
    #             st_weld_shear_stress = st_force / (2 * st_beam_weld_eff_length * st_beam_weld_throat)
    #             st_weld_moment_stress = st_moment / (2 * st_beam_weld * st_beam_weld_eff_length ** 2 / 4)
    #             st_eq_weld_stress = math.sqrt(st_weld_shear_stress ** 2 + st_weld_moment_stress ** 2)
    #             if st_eq_weld_stress <= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #                     ultimate_stresses=(weld_fu, self.supported_section.fu, st_fu)):
    #                 break
    #         # stiffener warnings
    #
    #         if st_moment >= st_moment_capacity:
    #             logger.warning("stiffener cannot take moment, current stiffener length %2.2f" % st_length)
    #         if st_force >= st_shear_capacity:
    #             logger.warning("stiffener cannot take shear force, current stiffener length %2.2f" % st_length)
    #         if st_eq_weld_stress >= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
    #                 ultimate_stresses=(weld_fu, self.supported_section.fu, st_fu)):
    #             logger.warning(
    #                 "stiffener weld cannot take stiffener loads, current weld thickness is %2.2f" % st_beam_weld)
    #
    #     # Strength of flange under compression or tension TODO: Get function from IS 800
    #
    #     A_f = self.supported_section.flange_width * self.supported_section.flange_thickness  # area of beam flange
    #     capacity_beam_flange = (self.supported_section.fy / gamma_m0) * A_f
    #     force_flange = max(t_bf, p_bf)
    #
    # def trial_design(self):
    #     self.set_osdaglogger()
    #     bolt_dia = max(self.bolt.bolt_diameter)
    #     bolt_grade = max(self.bolt.bolt_grade)
    #     self.plate.thickness_provided = min(self.plate.thickness)
    #
    #     self.check_minimum_design_action()
    #     self.check_compatibility()
    #
    #     # Weld design
    #     self.weld_design()
    #
    #     self.find_bolt_conn_plates_t_fu_fy()
    #     self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=bolt_dia,
    #                                             conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)


    # def member_capacity(self):
    #     # print(KEY_CONN,VALUES_CONN_1,self.supported_section.type)
    #     self.supported_section.notch_ht = round_up(
    #         max(self.supporting_section.flange_thickness + self.supporting_section.root_radius + 10,
    #             self.supported_section.flange_thickness + self.supported_section.root_radius + 10), 5)
    #     if self.connectivity in VALUES_CONN_1:
    #         if self.supported_section.type == "Rolled":
    #             self.supported_section.web_height = self.supported_section.depth
    #         else:
    #             self.supported_section.web_height = self.supported_section.depth - (
    #                         2 * self.supported_section.flange_thickness)  # -(2*self.supported_section.root_radius)
    #     else:
    #
    #         self.supported_section.web_height = self.supported_section.depth - self.supported_section.notch_ht
    #
    #     A_g = self.supported_section.web_height * self.supported_section.web_thickness
    #     # 0.6 is multiplied for shear yielding capacity to keep the section in low shear
    #     self.supported_section.shear_yielding_capacity = 0.6 * IS800_2007.cl_8_4_design_shear_strength(A_g,
    #                                                                                                    self.supported_section.fy)
    #     self.supported_section.tension_yielding_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g,
    #                                                                                                    self.supported_section.fy)
    #     if self.supported_section.shear_yielding_capacity / 1000 > self.load.shear_force and \
    #             self.supported_section.tension_yielding_capacity / 1000 > self.load.axial_force:
    #
    #         if self.load.shear_force <= min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
    #                                         40.0):
    #             logger.warning(" : User input for shear force is very less compared to section capacity. "
    #                            "Setting Shear Force value to 15% of supported beam shear capacity or 40kN, whichever is less.")
    #             self.load.shear_force = min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
    #                                         40.0)
    #
    #         print("preliminary member check is satisfactory. Checking available plate Thickness")
    #         self.thickness_possible = [i for i in self.plate.thickness if i >= self.supported_section.web_thickness]
    #
    #         if not self.thickness_possible:
    #             logger.error(": Plate thickness should be greater than suppported section web thicknesss.")
    #         else:
    #             print("Selecting bolt diameter")
    #             self.get_endplate_details(self)
    #
    #     else:
    #         # self.design_status = False
    #         logger.warning(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
    #                        "than applied loads, Please select larger sections or decrease loads"
    #                        .format(self.supported_section.shear_yielding_capacity,
    #                                self.supported_section.tension_yielding_capacity))
    #         print("failed in preliminary member checks. Select larger sections or decrease loads")
    #
    # def get_endplate_details(self):
    #     self.design_status = False
    #     print(self.supporting_section)
    #     print(self.supported_section)
    #     print(self.bolt)
    #     print(self.plate)
    #
    #     def get_3d_components(self):
    #         components = []
    #
    #         t1 = ('Model', self.call_3DModel)
    #         components.append(t1)
    #
    #         t2 = ('Beam', self.call_3DBeam)
    #         components.append(t2)
    #
    #         t3 = ('Column', self.call_3DColumn)
    #         components.append(t3)
    #
    #         # t4 = ('End Plate', self.call_3DPlate)
    #         # components.append(t4)
    #
    #         return components
    #
