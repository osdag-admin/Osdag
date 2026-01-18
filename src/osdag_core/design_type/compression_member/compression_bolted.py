"""
Started on 28th December, 2025.

@author: Manas Budhiraja

Module: Compression Member Bolted Design (Struts Bolted to End Gusset)

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel Structures by N. Subramanian (Fifth impression, 2019)
"""

from ..member import Member
from ...Common import *
from ...utils.common.component import *
from ...utils.common.common_calculation import *
from ...utils.common.load import Load
from ...utils.common.Section_Properties_Calculator import BBAngle_Properties, SAngle_Properties, BBChannel_Properties
from ...utils.common.material import *
from ...Report_functions import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...custom_logger import CustomLogger
from ...utils.common import is800_2007
from ...utils.common.is800_2007 import IS800_2007
from pylatex.utils import NoEscape
from pathlib import Path
from importlib.resources import files
import math
import numpy as np
import logging
import sys
import os
import os
import shutil
import time
import sys


class Compression_bolted(Member):

    def __init__(self):
        print(f'Entering Compression_bolted')
        super(Compression_bolted, self).__init__()
        self.design_status = False
        self.hover_dict = {}
        self.mainmodule = KEY_DISP_STRUT_BOLTED_END_GUSSET

    @staticmethod
    def module_name():
        return KEY_DISP_STRUT_BOLTED_END_GUSSET

    def set_osdaglogger(self, key, id):
        """
        Function to set Logger for Compression Bolted Module
        """
        # Set Custom logger
        logging.setLoggerClass(CustomLogger)

        # Create unique logger name per instance
        unique_logger_name = 'Osdag_struts_bolted_end_gusset_compress_member'
        self.logger = logging.getLogger(f"{unique_logger_name}_{id}")

        if not isinstance(self.logger, CustomLogger):
            logging.getLogger(unique_logger_name).manager.loggerDict.pop(unique_logger_name, None)
            self.logger = logging.getLogger(f"{unique_logger_name}_{id}")
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG)
        
        # Shared formatter for all handlers
        formatter = logging.Formatter(
            fmt='%(asctime)s - Osdag - %(levelname)s - %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # ---------- CONSOLE HANDLER ----------
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # ---------- FILE HANDLER (CLEAR & RESTART LOG) ----------
        log_dir = Path("ResourceFiles") / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file_path = log_dir / f"{unique_logger_name}.log"
        
        file_handler = logging.FileHandler(
            log_file_path,
            mode="w",          # clears previous log
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # ---------- GUI HANDLER ----------
        if key is not None:
            gui_handler = OurLog(key)
            gui_handler.setFormatter(formatter)
            self.logger.addHandler(gui_handler)

        # Initialize components for the design
        self.plate = Plate(thickness=[0.0], material_grade="E 250 (Fe 410 W)A")
        self.bolt = Bolt(grade=[0.0], diameter=[0.0], bolt_type="", bolt_hole_type="Standard",
                         edge_type="Sheared or hand flame cut", mu_f=0.3, corrosive_influences=True)

    def tab_list(self):
        """
        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        """
        tabs = []
        t1 = (DISP_TITLE_ANGLE, TYPE_TAB_1, self.tab_angle_section)
        tabs.append(t1)
        t2 = (DISP_TITLE_CHANNEL, TYPE_TAB_1, self.tab_channel_section)
        tabs.append(t2)
        t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        tabs.append(t6)
        t3 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t3)
        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)
        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)
        return tabs

    def tab_channel_section(self, input_dictionary):
        """Override parent method to handle non-numeric plate thickness values"""
        # Check if plate thickness is a valid number before calling parent
        if input_dictionary and KEY_PLATETHK in input_dictionary:
            plate_thk_data = input_dictionary[KEY_PLATETHK]
            if isinstance(plate_thk_data, list) and len(plate_thk_data) > 0:
                try:
                    float(plate_thk_data[0])
                except (ValueError, TypeError):
                    # If plate thickness is not numeric, set a default value
                    input_dictionary[KEY_PLATETHK] = [10.0]  # Default plate thickness
        
        # Call parent implementation
        return super().tab_channel_section(input_dictionary)

    def tab_angle_section(self, input_dictionary):
        """Override parent method to handle non-numeric plate thickness values"""
        # Check if plate thickness is a valid number before calling parent
        if input_dictionary and KEY_PLATETHK in input_dictionary:
            plate_thk_data = input_dictionary[KEY_PLATETHK]
            if isinstance(plate_thk_data, list) and len(plate_thk_data) > 0:
                try:
                    float(plate_thk_data[0])
                except (ValueError, TypeError):
                    # If plate thickness is not numeric, set a default value
                    input_dictionary[KEY_PLATETHK] = [10.0]  # Default plate thickness
        
        # Call parent implementation
        return super().tab_angle_section(input_dictionary)


    def tab_value_changed(self):
        """
        :return: This function is used to update the values of the keys in design preferences,
         which are dependent on other inputs.
        """
        change_tab = []
        
        t1 = (DISP_TITLE_ANGLE, [KEY_SECSIZE, KEY_SEC_MATERIAL, 'Label_0'],
              [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5',
               'Label_7', 'Label_8', 'Label_9',
               'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17',
               'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23', 'Label_24', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_new_angle_section_properties)
        change_tab.append(t1)

        t2 = (DISP_TITLE_ANGLE, ['Label_1', 'Label_2', 'Label_3','Label_0'],
              ['Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15',
               'Label_16', 'Label_17', 'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23',
               KEY_IMAGE],
              TYPE_TEXTBOX, self.get_Angle_sec_properties)
        change_tab.append(t2)

        t3 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE, KEY_SEC_MATERIAL,'Label_0'],
              [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14',
               'Label_4', 'Label_5',
               'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17',
               'Label_19', 'Label_20', 'Label_21',
               'Label_22', 'Label_23', 'Label_26','Label_27', KEY_IMAGE], TYPE_TEXTBOX, self.get_new_channel_section_properties)
        change_tab.append(t3)

        t4 = (DISP_TITLE_CHANNEL, ['Label_1', 'Label_2', 'Label_3', 'Label_13','Label_14'],
              ['Label_9', 'Label_10','Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17','Label_19', 'Label_20', 'Label_21', 'Label_22','Label_26','Label_27', KEY_IMAGE], TYPE_TEXTBOX, self.get_Channel_sec_properties)
        change_tab.append(t4)
        
        t5 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t5)

        t6 = (DISP_TITLE_ANGLE, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        t7 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

        return change_tab

    def input_dictionary_design_pref(self):
        """
        :return: This function is used to choose values of design preferences to be saved to design dictionary.
        """
        design_input = []
        
        # Use actual tab names like tension_bolted.py does
        t1 = (DISP_TITLE_ANGLE, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t1)

        t1a = (DISP_TITLE_CHANNEL, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t1a)

        t2 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        design_input.append(t2)

        t4 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
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
        design dictionary if design preference is never opened by user.
        """
        design_input = []
        
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DETAILING_GAP,
                     KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """
        :return: This function returns list of tuples which has keys that needs to be updated,
         on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)
        """
        add_buttons = []

        t2 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              VALUES_SEC_PROFILE_2, Profile_name_1)
        add_buttons.append(t2)

        return add_buttons


    def fn_profile_section(self, arg=None):
        if arg is None or len(arg) == 0:
            return []
        profile = arg[0]
        # Return appropriate section sizes based on profile type
        if profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return connectdb("Angles", call_type="popup")
        elif profile in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type="popup")
        return []

    def fn_conn_type(self, args):
        """Function to populate location based on the type of section"""
        if args is None or len(args) == 0:
            return VALUES_LOCATION_1
        conn = args[0]
        if conn in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return VALUES_LOCATION_1
        elif conn in ["Channels", "Back to Back Channels"]:
            return VALUES_LOCATION_2
        return VALUES_LOCATION_1

    def fn_conn_image(self, args):
        if args is None or len(args) == 0:
            return VALUES_IMG_TENSIONBOLTED[0]
        img = args[0]
        if img == VALUES_SEC_PROFILE_2[0]: # Angles
            return VALUES_IMG_TENSIONBOLTED[0]
        elif img == VALUES_SEC_PROFILE_2[1]: # Back to Back Angles
            return VALUES_IMG_TENSIONBOLTED[1]
        elif img == VALUES_SEC_PROFILE_2[2]: # Star Angles
            return VALUES_IMG_TENSIONBOLTED[2]
        elif img == VALUES_SEC_PROFILE_2[3]: # Channels
            return VALUES_IMG_TENSIONBOLTED[3]
        else:
            return VALUES_IMG_TENSIONBOLTED[4]

    def out_bolt_bearing(self, args):
        """Returns True to hide bolt bearing output when bolt type is not bearing"""
        bolt_type = args[0]
        if bolt_type != TYP_BEARING:
            return True
        else:
            return False

    def fn_end1_end2(self, arg):
        """Function to populate End 2 options based on End 1 selection"""
        end1 = arg[0]
        if end1 == 'Fixed':
            return VALUES_STRUT_END2
        elif end1 == 'Free':
            return ['Fixed']
        elif end1 == 'Hinged':
            return ['Fixed', 'Hinged']
        elif end1 == 'Roller':
            return ['Fixed', 'Hinged']
        return VALUES_STRUT_END2

    def fn_end1_image(self, arg):
        """Function to return image path based on End 1 condition"""
        if arg == 'Fixed':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
        elif arg == 'Free':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
        elif arg == 'Hinged':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRFstrut.png"))
        elif arg == 'Roller':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
        return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))

    def fn_end2_image(self, arg):
        """Function to return image path based on End 1 and End 2 conditions"""
        end1 = arg[0]
        end2 = arg[1]

        if end1 == 'Fixed':
            if end2 == 'Fixed':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
            elif end2 == 'Free':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
            elif end2 == 'Hinged':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RFRFstrut.png"))
            elif end2 == 'Roller':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
        elif end1 == 'Free':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
        elif end1 == 'Hinged':
            if end2 == 'Fixed':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRFstrut.png"))
            elif end2 == 'Hinged':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RFRFstrut.png"))
            elif end2 == 'Roller':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
        elif end1 == 'Roller':
            if end2 == 'Fixed':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
            elif end2 == 'Hinged':
                return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))
        
        return str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png"))

    def out_intermittent(self, args):
        """Returns True to hide intermittent connection fields for single sections"""
        sec_type = args[0]
        if sec_type in ['Back to Back Angles', 'Star Angles', 'Back to Back Channels']:
            return False
        else:
            return True

    def customized_input(self):
        """Function to populate combobox based on the option selected"""
        c_lst = []

        t1 = (KEY_SECSIZE, self.fn_profile_section)
        c_lst.append(t1)
        t2 = (KEY_GRD, self.grdval_customized)
        c_lst.append(t2)
        t3 = (KEY_D, self.diam_bolt_customized)
        c_lst.append(t3)
        t4 = (KEY_PLATETHK, self.plate_thick_customized)
        c_lst.append(t4)

        return c_lst

    def input_values(self, existingvalues={}):
        '''
        Function to return a list of tuples to be displayed as the UI.(Input Dock)
        '''
        self.module = KEY_DISP_STRUT_BOLTED_END_GUSSET
        self.mainmodule = 'Member'
        
        options_list = []

        t1 = (KEY_MODULE, KEY_DISP_STRUT_BOLTED_END_GUSSET, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t1)

        t1 = (None, KEY_SECTION_DATA, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, VALUES_SEC_PROFILE_2, True, 'No Validator')
        options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, VALUES_IMG_TENSIONBOLTED[0], True, 'No Validator')
        options_list.append(t3)

        t3 = (KEY_LOCATION, KEY_DISP_LOCATION, TYPE_COMBOBOX, VALUES_LOCATION_1, True, 'No Validator')
        options_list.append(t3)
        
        # New Input: Loaded through one leg
        t_load = ('is_leg_loaded', 'Loaded through one leg', TYPE_COMBOBOX, ['Yes', 'No'], True, 'No Validator')
        options_list.append(t_load)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator')
        options_list.append(t4)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_LENGTH, KEY_DISP_LENGTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)
        
        # New Inputs: End Conditions
        t9 = (None, 'End Conditions', TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)
        
        t10 = (KEY_END1, 'End 1 Condition', TYPE_COMBOBOX, VALUES_STRUT_END1, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_END2, 'End 2 Condition', TYPE_COMBOBOX, VALUES_STRUT_END2, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_IMAGE_two, None, TYPE_IMAGE_COMPRESSION, str(files("osdag_core.data.ResourceFiles.images").joinpath("RRRRstrut.png")), True, 'No Validator')
        options_list.append(t12)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL_STAR, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t8)

        t8 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t8)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK, True, 'No Validator')
        options_list.append(t14)

        return options_list

    def safe_log(self, level, message):
        """
        Safely log a message, catching RuntimeError if the Qt widget handler
        has been deleted (e.g., log window was closed).
        """
        try:
            if level == 'info':
                self.logger.info(message)
            elif level == 'warning':
                self.logger.warning(message)
            elif level == 'error':
                self.logger.error(message)
        except RuntimeError:
            # Qt widget handler was deleted - ignore silently
            pass


    def output_values(self, flag):
        '''
        Function to return a list of tuples to be displayed as the UI.(Output Dock)
        '''
        out_list = []

        t1 = (None, DISP_TITLE_STRUT_SECTION, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_DESIGNATION, KEY_DISP_DESIGNATION, TYPE_TEXTBOX,
              self.section_size_1.designation if flag else '', True)
        out_list.append(t2)
        
        # Effective Length (KL) - Calculated as K * L
        t_eff = ('KEY_EFFECTIVE_LENGTH', 'Effective Length, KL (mm)', TYPE_TEXTBOX,
                 self.effective_length if flag else '', True)
        out_list.append(t_eff)

        # Design Compressive Stress (fcd) - IS 800 Cl 7.1.2.1
        t_fcd = ('KEY_FCD', 'Design Compressive Stress, fcd (MPa)', TYPE_TEXTBOX,
                 self.f_cd if flag else '', True)
        out_list.append(t_fcd)

        # Compression Capacity (calculated in member_check)
        t3 = (KEY_TENSION_CAPACITY, KEY_DISP_DESIGN_STRENGTH_COMPRESSION, TYPE_TEXTBOX,
              round((self.section_size_1.compression_capacity/1000), 2) if flag else '', True)
        out_list.append(t3)

        t6 = (KEY_SLENDER, KEY_DISP_SLENDER, TYPE_TEXTBOX,
              self.section_size_1.slenderness if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_EFFICIENCY, KEY_DISP_EFFICIENCY, TYPE_TEXTBOX,
              self.efficiency if flag else '', True)
        out_list.append(t7)

        t8 = (None, DISP_TITLE_END_CONNECTION, TYPE_TITLE, None, True)
        out_list.append(t8)

        t8 = (None, DISP_TITLE_BOLTD, TYPE_TITLE, None, True)
        out_list.append(t8)

        t9 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,
              int(self.bolt.bolt_diameter_provided) if flag else '', True)
        out_list.append(t9)

        t10 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX,
               self.bolt.bolt_grade_provided if flag else '', True)
        out_list.append(t10)

        t11 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
               round(self.bolt.bolt_shear_capacity/1000, 2) if flag else '', True)
        out_list.append(t11)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
            else:
                bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX,
              bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t5)

        t5 = (KEY_REDUCTION_LONG_JOINT, KEY_DISP_REDUCTION_LONG_JOINT, TYPE_TEXTBOX,
              round(self.plate.beta_lj, 2) if flag else '', True)
        out_list.append(t5)

        t5 = (KEY_REDUCTION_LARGE_GRIP, KEY_DISP_REDUCTION_LARGE_GRIP, TYPE_TEXTBOX,
              round(self.plate.beta_lg, 2) if flag else '', True)
        out_list.append(t5)

        t13 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
               round(self.plate.bolt_capacity_red/1000, 2) if flag else '', True)
        out_list.append(t13)

        t14 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX,
               round(self.plate.bolt_force / 1000, 2) if flag else '', True)
        out_list.append(t14)

        t17 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON,
               ['Spacing Details', self.spacing], True)
        out_list.append(t17)

        t18 = (None, DISP_TITLE_GUSSET_PLATE, TYPE_TITLE, None, True)
        out_list.append(t18)

        t19 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX,
               int(round(self.plate.thickness_provided, 0)) if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_MIN_HEIGHT, TYPE_TEXTBOX,
               int(round(self.plate.height, 0)) if flag else '', True)
        out_list.append(t20)

        t21 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_MIN_LENGTH, TYPE_TEXTBOX,
               int(round(self.plate.length, 0)) if flag else '', True)
        out_list.append(t21)
        
        t22 = (KEY_OUT_PLATE_YIELD, KEY_DISP_TENSION_YIELDCAPACITY, TYPE_TEXTBOX,
               (round(self.plate.tension_yielding_capacity / 1000, 2)) if flag else '', True)
        out_list.append(t22)

        t23 = (KEY_OUT_PLATE_RUPTURE, KEY_DISP_TENSION_RUPTURECAPACITY, TYPE_TEXTBOX,
               (round(self.plate.tension_rupture_capacity/ 1000, 2)) if flag else '', True)
        out_list.append(t23)

        t24 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_DISP_TENSION_BLOCKSHEARCAPACITY, TYPE_TEXTBOX,
               (round(self.plate.block_shear_capacity/ 1000, 2)) if flag else '', True)
        out_list.append(t24)

        t17 = (KEY_OUT_PATTERN_2, KEY_OUT_DISP_PATTERN, TYPE_OUT_BUTTON, ['Shear Pattern ', self.plate_pattern], True)
        out_list.append(t17)

        # Intermittent Connection Details (only for built-up sections)
        t18_inter = (None, DISP_TITLE_INTERMITTENT, TYPE_TITLE, None, False)
        out_list.append(t18_inter)

        t8_inter = (None, DISP_TITLE_CONN_DETAILS, TYPE_TITLE, None, False)
        out_list.append(t8_inter)

        t21_inter = (KEY_OUT_INTERCONNECTION, KEY_OUT_DISP_INTERCONNECTION, TYPE_TEXTBOX,
               int(round(self.inter_conn, 0)) if flag else '', False)
        out_list.append(t21_inter)

        t21_spacing = (KEY_OUT_INTERSPACING, KEY_OUT_DISP_INTERSPACING, TYPE_TEXTBOX,
               (round(self.inter_memb_length, 2)) if flag else '', False)
        out_list.append(t21_spacing)

        t18_bolt = (None, DISP_TITLE_BOLTD, TYPE_TITLE, None, False)
        out_list.append(t18_bolt)

        t9_inter = (KEY_OUT_INTER_D_PROVIDED, KEY_OUT_DISP_INTER_D_PROVIDED, TYPE_TEXTBOX, int(self.inter_dia) if flag else '', False)
        out_list.append(t9_inter)

        t10_inter = (KEY_OUT_INTER_GRD_PROVIDED, KEY_OUT_DISP_INTER_GRD_PROVIDED, TYPE_TEXTBOX, self.inter_grade if flag else '', False)
        out_list.append(t10_inter)

        t15_inter = (KEY_OUT_INTER_BOLT_LINE, KEY_OUT_DISP_INTER_BOLT_LINE, TYPE_TEXTBOX, self.inter_bolt_line if flag else '', False)
        out_list.append(t15_inter)

        t16_inter = (KEY_OUT_INTER_BOLTS_ONE_LINE, KEY_OUT_DISP_INTER_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.inter_bolt_one_line if flag else '', False)
        out_list.append(t16_inter)

        t18_plate = (None, DISP_TITLE_PLATED, TYPE_TITLE, None, False)
        out_list.append(t18_plate)

        t20_inter = (KEY_OUT_INTER_PLATE_HEIGHT, KEY_OUT_DISP_INTER_PLATE_HEIGHT, TYPE_TEXTBOX, int(round(self.inter_plate_height, 0)) if flag else '', False)
        out_list.append(t20_inter)

        t21_inter_plate = (KEY_OUT_INTER_PLATE_LENGTH, KEY_OUT_DISP_INTER_PLATE_LENGTH, TYPE_TEXTBOX, int(round(self.inter_plate_length, 0)) if flag else '', False)
        out_list.append(t21_inter_plate)

        if flag and hasattr(self, 'hover_dict'):
             if hasattr(self, 'section_size_1'):
                 self.hover_dict["Member"] = f"Member: {self.section_size_1.designation}"
             if hasattr(self, 'plate'):
                 self.hover_dict["Plate"] = f"Plate: {self.plate.length}x{self.plate.height}x{self.plate.thickness_provided}"
             if hasattr(self, 'bolt'):
                 self.hover_dict["Bolt"] = f"Bolt: {self.bolt.bolt_diameter_provided}mm dia, Grade {self.bolt.bolt_grade}"
        
        return out_list

    def spacing(self, status):
        """Spacing details for bolt arrangement popup"""
        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Spacing Details based on member's depth \n (root radius not included in edge distance)")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
               [str(files("osdag_core.data.ResourceFiles.images").joinpath("spacing_1.png")), 400, 278, "3 x 3 pattern considered"])
        spacing.append(t99)

        t16 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX,
               self.plate.bolts_one_line if status else '')
        spacing.append(t16)

        t15 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX,
               self.plate.bolt_line if status else '')
        spacing.append(t15)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX,
              self.plate.pitch_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX,
               self.plate.end_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX,
               self.plate.gauge_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX,
               self.plate.edge_dist_provided if status else '')
        spacing.append(t12)

        # Calculate member depth for diagram
        member_depth = 0.0
        if status:
            if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
                if self.loc == "Long Leg":
                    member_depth = self.section_size.max_leg
                else:
                    member_depth = self.section_size.min_leg
            elif self.sec_profile in ['Channels', 'Back to Back Channels']:
                member_depth = self.section_size.depth
                
        t_depth = ('Member.Depth', 'Member Depth', TYPE_TEXTBOX, member_depth)
        spacing.append(t_depth)

        return spacing

    def memb_pattern(self, status):
        """Failure pattern due to compression/tension in member"""
        if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
            image = str(files("osdag_core.data.ResourceFiles.images").joinpath("L.png"))
            x, y = 400, 202
        else:
            image = str(files("osdag_core.data.ResourceFiles.images").joinpath("U.png"))
            x, y = 400, 202

        pattern = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern")
        pattern.append(t00)

        t99 = (None, 'Failure Pattern due to Compression in Member', TYPE_IMAGE,
               [image, x, y, "Member Block Shear Pattern"])
        pattern.append(t99)

        return pattern

    def plate_pattern(self, status):
        """Failure pattern due to tension in plate"""
        pattern = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern")
        pattern.append(t00)

        t99 = (None, 'Failure Pattern due to Tension in Plate', TYPE_IMAGE,
               [str(files("osdag_core.data.ResourceFiles.images").joinpath("L.png")), 400, 202, "Plate Block Shear Pattern"])
        pattern.append(t99)

        return pattern

    def input_value_changed(self):
        """
        Function calling the methods relative to each key of the UI.
        """
        lst = []

        t1 = ([KEY_SEC_PROFILE], KEY_LOCATION, TYPE_COMBOBOX, self.fn_conn_type)
        lst.append(t1)

        t2 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t2)

        t3 = ([KEY_SEC_PROFILE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t3)

        t4 = ([KEY_TYP], KEY_OUT_BOLT_BEARING, TYPE_OUT_DOCK, self.out_bolt_bearing)
        lst.append(t4)

        t5 = ([KEY_TYP], KEY_OUT_BOLT_BEARING, TYPE_OUT_LABEL, self.out_bolt_bearing)
        lst.append(t5)

        t6 = ([KEY_END1], KEY_END2, TYPE_COMBOBOX, self.fn_end1_end2)
        lst.append(t6)

        t7 = ([KEY_END1, KEY_END2], KEY_IMAGE_two, TYPE_IMAGE, self.fn_end2_image)
        lst.append(t7)

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        t9 = ([KEY_SECSIZE], KEY_SECSIZE, TYPE_CUSTOM_SECTION, self.new_material)
        lst.append(t9)

        # Intermittent connection visibility
        t10 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_D_PROVIDED, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t10)

        t11 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_D_PROVIDED, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t11)

        t12 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_GRD_PROVIDED, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t12)

        t13 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_GRD_PROVIDED, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t13)

        t14 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_BOLT_LINE, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t14)

        t15 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_BOLT_LINE, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t15)

        t16 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_BOLTS_ONE_LINE, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t16)

        t17 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_BOLTS_ONE_LINE, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t17)

        t18 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_PLATE_HEIGHT, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t18)

        t19 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_PLATE_HEIGHT, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t19)

        t20 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_PLATE_LENGTH, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t20)

        t21 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_PLATE_LENGTH, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t21)

        t22 = ([KEY_SEC_PROFILE], KEY_OUT_INTERCONNECTION, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t22)

        t23 = ([KEY_SEC_PROFILE], KEY_OUT_INTERCONNECTION, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t23)

        t24 = ([KEY_SEC_PROFILE], KEY_OUT_INTERSPACING, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t24)

        t25 = ([KEY_SEC_PROFILE], KEY_OUT_INTERSPACING, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t25)

        return lst

    def func_for_validation(self, design_dictionary):
        all_errors = []
        self.design_status = False
        flag = False
        flag1 = False
        flag2 = False

        option_list = self.input_values(self)
        missing_fields_list = []

        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
                else:
                    if option[0] == KEY_LENGTH:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True
                    if option[0] == KEY_AXIAL:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag2 = True
            else:
                pass

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(missing_fields_list)
            all_errors.append(error)
        else:
            flag = True

        if flag and flag1 and flag2:
            self.set_input_values(design_dictionary)
        else:
            return all_errors

    def warn_text(self):
        """
        Function to give logger warning when any old value is selected from Column and Beams table.
        """
        red_list = red_list_function()
        if self.supported_section.designation in red_list or self.supporting_section.designation in red_list:
            self.logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            self.logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def set_input_values(self, design_dictionary):
        "initialisation of components required to design a compression member along with connection"
        super(Compression_bolted, self).set_input_values(design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.sizelist = design_dictionary[KEY_SECSIZE]
        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]
        self.loc = design_dictionary[KEY_LOCATION]
        self.material = design_dictionary[KEY_SEC_MATERIAL]
        self.length = float(design_dictionary[KEY_LENGTH])
        self.load = Load(shear_force="", axial_force=design_dictionary.get(KEY_AXIAL))
        self.main_material = design_dictionary.get(KEY_MATERIAL, design_dictionary[KEY_SEC_MATERIAL])
        self.load_type = design_dictionary.get(KEY_ALLOW_LOAD, 'Concentric Load')
        
        # Compression specific inputs
        self.end_1 = design_dictionary.get(KEY_END1, 'Fixed')
        self.end_2 = design_dictionary.get(KEY_END2, 'Fixed')
        self.is_leg_loaded = design_dictionary.get('is_leg_loaded', 'Yes') == 'Yes'
        
        # Calculate Effective Length Factor (K) based on Table 11 of IS 800:2007
        self.K = self.get_effective_length_factor(self.end_1, self.end_2)
        
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL])

        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        
        self.count = 0
        self.member_design_status = False
        self.max_limit_status_1 = False
        self.max_limit_status_2 = False
        self.bolt_design_status = False
        self.plate_design_status = False
        self.thk_count = 0
        self.efficiency = 0.0
        
        print("The input values are set. Performing preliminary member check(s).")
        
        # Initialize intermittent connection variables
        self.inter_conn = 0.0
        self.inter_memb_length = 0.0
        self.inter_dia = 0.0
        self.inter_grade = 0.0
        self.inter_bolt_one_line = 0.0
        self.inter_bolt_line = 0.0
        self.inter_plate_length = 0.0
        self.inter_plate_height = 0.0
        
        # Safety factors as per IS 800:2007 Table 5
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        self.gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']


        
        self.initial_member_capacity(design_dictionary)

    def get_effective_length_factor(self, end1, end2):
        """
        Determine effective length factor (K) based on IS 800:2007 Table 11
        Note: Exact string matching depends on VALUES_STRUT_END1/2 definitions.
        Assuming standard descriptions or simplified keys.
        """
        # Mapping simplified for common cases. 
        # Ideally this should match the exact strings in Common.py
        
        # Fixed = "Restrained against translation and rotation"
        # Hinged = "Restrained against translation but not rotation"
        # Free = "Free"
        # Roller = "Restrained against rotation but not translation"
        
        # Combination logic (simplified representation):
        # Fixed-Fixed -> 0.65
        # Fixed-Hinged -> 0.8
        # Hinged-Hinged -> 1.0
        # Fixed-Free -> 2.0
        # Fixed-Roller -> 1.2
        # Hinged-Roller -> 2.0
        
        # Normalizing inputs to lower case for check (safe fallback)
        e1 = end1.lower()
        e2 = end2.lower()
        
        cond = sorted([e1, e2]) # Sort to handle order independence
        
        # Standard values from Table 11
        if any("translation" in x and "rotation" in x for x in cond): 
             # Full description matching logic would go here if strings are long
             # For now defaulting to 1.0 if not explicit short codes
             pass
             
        # HEURISTIC: Check for keywords if explicit values aren't known
        # 1. Fixed (Restrained T & R)
        if "fixed" in e1: e1_type = "fixed"
        elif "hinged" in e1 or "pinned" in e1: e1_type = "hinged"
        elif "roller" in e1: e1_type = "roller"
        elif "free" in e1: e1_type = "free"
        else: e1_type = "hinged" # Conservative default

        if "fixed" in e2: e2_type = "fixed"
        elif "hinged" in e2 or "pinned" in e2: e2_type = "hinged"
        elif "roller" in e2: e2_type = "roller"
        elif "free" in e2: e2_type = "free"
        else: e2_type = "hinged"

        pair = tuple(sorted([e1_type, e2_type]))
        
        k_map = {
            ('fixed', 'fixed'): 0.65,
            ('fixed', 'hinged'): 0.80,
            ('hinged', 'hinged'): 1.00,
            ('fixed', 'free'): 2.00,
            ('fixed', 'roller'): 1.20,
            ('hinged', 'roller'): 2.00, 
            ('hinged', 'free'): 2.0  # Unstable ideally, but theoretical
        }
        
        return k_map.get(pair, 1.0)

    def calculate_slenderness(self, L, K, r_min):
        """
        Calculate slenderness ratio for compression member.
        IS 800:2007 Cl 7.1.2 - Lambda = (K * L) / r_min
        
        Args:
            L: Unsupported length (mm)
            K: Effective length factor
            r_min: Minimum radius of gyration (mm)
        
        Returns:
            Slenderness ratio (dimensionless)
        """
        if r_min <= 0:
            return 999.0  # Return high value for invalid r_min
        return (K * L) / r_min

    def select_section(self, design_dictionary, selectedsize):
        "selecting components class based on the section passed"
        if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles', 'Star Angles']:
            self.section_size = Angle(designation=selectedsize, material_grade=design_dictionary[KEY_SEC_MATERIAL])
        elif design_dictionary[KEY_SEC_PROFILE] in ['Channels', 'Back to Back Channels']:
            self.section_size = Channel(designation=selectedsize, material_grade=design_dictionary[KEY_SEC_MATERIAL])
        else:
            pass
        return self.section_size

    def max_section(self, design_dictionary, sizelist):
        # Implementation of max section selection (logic similar to tension_bolted)
        # Needs to fill self.max_area, self.max_gyr, self.depth_max
        sec_area = {}
        sec_gyr = {}
        sec_depth = []
        for section in sizelist:
            if design_dictionary[KEY_SEC_PROFILE] in ['Angles']:
                self.section = Angle(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL])
                self.min_rad_gyration_calc(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL], 
                                           key=design_dictionary[KEY_SEC_PROFILE],
                                           subkey=design_dictionary[KEY_LOCATION], D_a=self.section.a,
                                           B_b=self.section.b, T_t=self.section.thickness)
                sec_gyr[self.section.designation] = self.min_radius_gyration
                if self.loc == "Long Leg":
                    sec_depth.append(self.section.max_leg)
                else:
                    sec_depth.append(self.section.min_leg)

            elif design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Angles', 'Star Angles']:
                self.section = Angle(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL])
                self.min_rad_gyration_calc(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL],
                                           key=design_dictionary[KEY_SEC_PROFILE],
                                           subkey=design_dictionary[KEY_LOCATION], D_a=self.section.a,
                                           B_b=self.section.b, T_t=self.section.thickness)
                sec_gyr[self.section.designation] = self.min_radius_gyration
                if self.loc == "Long Leg":
                    sec_depth.append(self.section.max_leg)
                else:
                    sec_depth.append(self.section.min_leg)

            else:
                self.section = Channel(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL])
                self.min_rad_gyration_calc(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL],
                                           key=design_dictionary[KEY_SEC_PROFILE],
                                           subkey=design_dictionary[KEY_LOCATION], D_a=self.section.depth,
                                           B_b=self.section.flange_width, T_t=self.section.flange_thickness,
                                           t=self.section.web_thickness)
                sec_gyr[self.section.designation] = self.min_radius_gyration
                sec_depth.append(self.section.depth)
            sec_area[self.section.designation] = self.section.area

        if len(sec_area) >= 2:
            self.max_area = max(sec_area, key=sec_area.get)
        else:
            self.max_area = self.section.designation

        if len(sec_gyr) >= 2:
            self.max_gyr = max(sec_gyr, key=sec_gyr.get)
        else:
            self.max_gyr = self.section.designation

        if len(sec_depth) >= 2:
            self.depth_max = max(sec_depth)
        else:
            self.depth_max = max(sec_depth) if sec_depth else 0.0

        return self.max_area, self.max_gyr, self.depth_max

    def max_force_length(self, section):
        # Calculate max force (compression) and length based on section
        # Adapted from tension logic but for compression yielding/buckling
        if self.sec_profile == 'Angles':
            self.section_size_max = Angle(designation=section, material_grade=self.material)
            # Calculate compression capacity
            r_min_max = min(self.section_size_max.rad_of_gy_u, self.section_size_max.rad_of_gy_v)
            buckling_class = 'c'
            imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
            # Use max slenderness of 180 for compression
            temp_slen = 180
            results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.section_size_max.fy, self.gamma_m0, temp_slen, 
                imperfection_factor, 200000, check_type='Concentric')
            f_cd_max = results[5]
            self.max_member_force = self.section_size_max.area * f_cd_max
            self.max_length = 180 * r_min_max
        elif self.sec_profile in ['Back to Back Angles', 'Star Angles']:
            self.section_size_max = Angle(designation=section, material_grade=self.material)
            self.min_rad_gyration_calc(designation=section, material_grade=self.material,
                                       key=self.sec_profile, subkey=self.loc, 
                                       D_a=self.section_size_max.a,
                                       B_b=self.section_size_max.b, 
                                       T_t=self.section_size_max.thickness)
            r_min_max = self.min_radius_gyration
            buckling_class = 'c'
            imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
            temp_slen = 180
            results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.section_size_max.fy, self.gamma_m0, temp_slen, 
                imperfection_factor, 200000, check_type='Concentric')
            f_cd_max = results[5]
            self.max_member_force = 2 * self.section_size_max.area * f_cd_max
            self.max_length = 180 * r_min_max
        elif self.sec_profile == 'Channels':
            self.section_size_max = Channel(designation=section, material_grade=self.material)
            r_min_max = min(self.section_size_max.rad_of_gy_y, self.section_size_max.rad_of_gy_z)
            buckling_class = 'c'
            imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
            temp_slen = 180
            results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.section_size_max.fy, self.gamma_m0, temp_slen, 
                imperfection_factor, 200000, check_type='Concentric')
            f_cd_max = results[5]
            self.max_member_force = self.section_size_max.area * f_cd_max
            self.max_length = 180 * r_min_max
        elif self.sec_profile == 'Back to Back Channels':
            self.section_size_max = Channel(designation=section, material_grade=self.material)
            self.min_rad_gyration_calc(designation=section, material_grade=self.material,
                                       key=self.sec_profile, subkey=self.loc, 
                                       D_a=self.section_size_max.depth,
                                       B_b=self.section_size_max.flange_width, 
                                       T_t=self.section_size_max.flange_thickness,
                                       t=self.section_size_max.web_thickness)
            r_min_max = self.min_radius_gyration
            buckling_class = 'c'
            imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
            temp_slen = 180
            results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.section_size_max.fy, self.gamma_m0, temp_slen, 
                imperfection_factor, 200000, check_type='Concentric')
            f_cd_max = results[5]
            self.max_member_force = 2 * self.section_size_max.area * f_cd_max
            self.max_length = 180 * r_min_max
        
        self.section_size_max.design_check_for_slenderness(K=self.K, L=self.length, r=r_min_max)
        
        return self.max_member_force, self.max_length, self.section_size_max.slenderness, r_min_max 

    def initial_member_capacity(self, design_dictionary, previous_size=None):
        "selection of member based on the compression capacity"
        min_capacity = 0
        
        if self.count == 0:
            self.max_section(design_dictionary, self.sizelist)
            [self.force1, self.len1, self.slen1, self.gyr1] = self.max_force_length(self.max_area)
            [self.force2, self.len2, self.slen2, self.gyr2] = self.max_force_length(self.max_gyr)
        else:
            pass
        
        self.count += 1
        
        if previous_size is None:
            pass
        else:
            if previous_size in self.sizelist:
                self.sizelist.remove(previous_size)


        print(f" self.sizelist {self.sizelist}")
        # Iterate through all available sections
        for selectedsize in self.sizelist:
            self.section_size = self.select_section(design_dictionary, selectedsize)
            
            # --- 1. Minimal Geometric Checks for Bolted Connection ---
            # (Similar to tension_bolted to ensure bolts fit)
            self.bolt_diameter_min = min(self.bolt.bolt_diameter)
            self.edge_dist_min = IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_min, self.bolt.bolt_hole_type, 'machine_flame_cut')
            self.d_0_min = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter_min, design_dictionary[KEY_DP_BOLT_HOLE_TYPE])
            self.edge_dist_min_round = round_up(self.edge_dist_min, 5)
            self.pitch_round = round_up((2.5 * self.bolt_diameter_min), 5)
            
            # Check if section leg/depth handles minimum bolt requirements
            if design_dictionary[KEY_SEC_PROFILE] in ['Channels', 'Back to Back Channels']:
                self.max_plate_height = self.section_size.max_plate_height()
                if self.max_plate_height < (self.pitch_round + 2 * self.edge_dist_min_round):
                    continue
            else:
                # Angles
                if self.loc == "Long Leg":
                    leg_dim = self.section_size.max_leg
                else:
                    leg_dim = self.section_size.min_leg
                
                # Check against root radius and thickness
                available_width = leg_dim - self.section_size.root_radius - self.section_size.thickness
                if available_width < (2 * self.edge_dist_min_round):
                    continue

                self.max_plate_height = available_width # Rough estimate for plate height compatibility

            # --- 2. Compression Member Capacity Check ---
            # Using K=1.0 roughly for initial selection or user input K
            
            # Calculate Radius of Gyration (Minimum)
            if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles', 'Star Angles']:
                # For angles, we need to consider specific configuration properties
                # But for single Angle, use min(ru, rv)
                # For now using simple object properties, refined later
                 if design_dictionary[KEY_SEC_PROFILE] == 'Angles':
                     r_min = min(self.section_size.rad_of_gy_u, self.section_size.rad_of_gy_v)
                 else:
                     # Placeholder for B2B/Star calculation - typically handled by min_rad_gyration_calc
                     # We will call the helper if available, or assume r_min from section property for single unit * factor
                     # Re-using min_rad_gyration_calc logic is better
                     self.min_rad_gyration_calc(designation=self.section_size.designation,
                                               material_grade=self.material,
                                               key=self.sec_profile, subkey=self.loc, 
                                               D_a=self.section_size.a,
                                               B_b=self.section_size.b, 
                                               T_t=self.section_size.thickness)
                     r_min = self.min_radius_gyration
            else:
                # Channels
                self.min_rad_gyration_calc(designation=self.section_size.designation,
                                           material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, 
                                           D_a=self.section_size.depth,
                                           B_b=self.section_size.flange_width, 
                                           T_t=self.section_size.flange_thickness,
                                           t=self.section_size.web_thickness)
                r_min = self.min_radius_gyration

            # Slenderness Check (KL/r)
            # Max Slenderness for Compression Member is typically 180 (Dead+Live), 250 (Wind/Seismic)
            # IS 800 Table 3.
            # Assuming 180 as safe conservative limit for initial Design
            slenderness = (self.K * self.length) / r_min if r_min > 0 else 999
            if slenderness > 180: # Strict limit for main members
                continue # Try next section

            # Capacity Calculation
            # Pd = Ae * fcd
            self.section_size.design_check_for_slenderness(K=self.K, L=self.length, r=r_min)
            # The component class (Angle/Channel) in compression.py handles compression_member_design_buckling or calc
            # In compression.py: self.section_size.compression_member_design_buckling(...)
            
            # Note: We need to ensure 'compression_member_design_buckling' exists on the section object
            # or calculate manually.
            # The 'Angle' / 'Channel' objects in 'component.py' usually have this method.
            
            # Performing capacity check
            # For class 4 sections, effective area is calculated. This is handled inside component check usually.
            
            # We assume section_size has compression_capacity updated after 'design_check_for_slenderness' 
            # or we need to call it explicitly.
            # In 'compression.py', 'design_check_for_slenderness' updates slenderness.
            # We need to call compression capacity calculation.
            
            # Using the logic from 'compression.py':
            # It seems it calculates fcd and Pd.
            
            if hasattr(self.section_size, 'compression_capacity'):
                 # It might be calculated in __init__ or we need to trigger it
                 pass
            
            # Force calculation trigger (approximate for selection):
            # We need fcd.
            # IS 800 Cl 7.1.2.1
            
            # Let's rely on the method 'design_check_for_slenderness' to return/set values if possible 
            # OR better, call 'compression_member_design_buckling' if available.
            
            # In osdag_core, component.py -> Member -> ...
            # Let's assume we need to calculate it.
            
            # For now, let's assume we proceed if slenderness is OK, 
            # and calculate capacity properly in 'member_check' or 'select_bolt_dia'
            # But we need to skip sections that are too weak.
            
            # Calculate compression capacity for this section
            # Using IS 800:2007 Cl 7.1.2.1 (Design Compressive Stress)
            # Buckling class 'c' assumed for hot-rolled Angles/Channels about any axis
            # Ref: IS 800:2007 Table 10 - conservative assumption for general design
            buckling_class = 'c'
            imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
            
            # Calculate slenderness for capacity check
            temp_slenderness = (self.K * self.length) / r_min if r_min > 0 else 999
            
            # --- IS 800:2007 Cl 7.5.1.2 Single Angle Strut Loaded Through One Leg ---
            if self.load_type == "Leg Load" and design_dictionary[KEY_SEC_PROFILE] == 'Angles':
                # Angle loaded through one leg
                # Calculate equivalent slenderness ratio lambda_e
                
                # Constants for >= 2 bolts (Fixed behavior assumed for initial selection)
                k1 = 0.20
                k2 = 0.35
                k3 = 20.0
                
                # Dimensions
                b1 = self.section_size.a
                b2 = self.section_size.b 
                t = self.section_size.thickness
                r_vv = self.section_size.rad_of_gy_v
                
                if r_vv > 0:
                    lambda_vv = (self.length / r_vv) 
                    lambda_phi = (b1 + b2) / (2 * t)
                    
                    lambda_e = math.sqrt(k1 + k2 * lambda_vv**2 + k3 * lambda_phi**2)
                    
                    # Use lambda_e for design stress calculation
                    temp_slenderness = lambda_e
                    # Note: buckling_class 'c' is still appropriate for angles (Table 10)

            results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.section_size.fy, self.gamma_m0, temp_slenderness, 
                imperfection_factor, 200000, check_type='Concentric')
            
            f_cd_temp = results[5]
            compression_capacity_temp = self.section_size.area * f_cd_temp  # N
            
            # Condition for capacity and slenderness check
            if (compression_capacity_temp >= self.load.axial_force * 1000) and temp_slenderness <= 180:
                min_capacity_current = compression_capacity_temp
                self.member_design_status = True
                if min_capacity == 0:
                    min_capacity = min_capacity_current
                    self.section_size_1 = self.select_section(design_dictionary, selectedsize)
                    # Recalculate for selected section
                    if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles', 'Star Angles']:
                        if design_dictionary[KEY_SEC_PROFILE] == 'Angles':
                            r_min_1 = min(self.section_size_1.rad_of_gy_u, self.section_size_1.rad_of_gy_v)
                        else:
                            self.min_rad_gyration_calc(designation=self.section_size_1.designation,
                                                       material_grade=self.material,
                                                       key=self.sec_profile, subkey=self.loc, 
                                                       D_a=self.section_size_1.a,
                                                       B_b=self.section_size_1.b, 
                                                       T_t=self.section_size_1.thickness)
                            r_min_1 = self.min_radius_gyration
                    else:
                        self.min_rad_gyration_calc(designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, 
                                                   D_a=self.section_size_1.depth,
                                                   B_b=self.section_size_1.flange_width, 
                                                   T_t=self.section_size_1.flange_thickness,
                                                   t=self.section_size_1.web_thickness)
                        r_min_1 = self.min_radius_gyration
                    
                    self.min_rad_gyration = r_min_1
                    self.section_size_1.design_check_for_slenderness(K=self.K, L=self.length, r=r_min_1)
                    
                    # Calculate and store compression capacity for later use
                    buckling_class = 'c'
                    imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
                    results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                        self.section_size_1.fy, self.gamma_m0, self.section_size_1.slenderness, 
                        imperfection_factor, 200000, check_type='Concentric')
                    f_cd = results[5]
                    self.section_size_1.compression_capacity = self.section_size_1.area * f_cd
                    
                elif min_capacity_current < min_capacity:
                    min_capacity = min_capacity_current
                    self.section_size_1 = self.select_section(design_dictionary, selectedsize)
                    # Recalculate for selected section
                    if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles', 'Star Angles']:
                        if design_dictionary[KEY_SEC_PROFILE] == 'Angles':
                            r_min_1 = min(self.section_size_1.rad_of_gy_u, self.section_size_1.rad_of_gy_v)
                        else:
                            self.min_rad_gyration_calc(designation=self.section_size_1.designation,
                                                       material_grade=self.material,
                                                       key=self.sec_profile, subkey=self.loc, 
                                                       D_a=self.section_size_1.a,
                                                       B_b=self.section_size_1.b, 
                                                       T_t=self.section_size_1.thickness)
                            r_min_1 = self.min_radius_gyration
                    else:
                        self.min_rad_gyration_calc(designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, 
                                                   D_a=self.section_size_1.depth,
                                                   B_b=self.section_size_1.flange_width, 
                                                   T_t=self.section_size_1.flange_thickness,
                                                   t=self.section_size_1.web_thickness)
                        r_min_1 = self.min_radius_gyration
                    
                    self.min_rad_gyration = r_min_1
                    self.section_size_1.design_check_for_slenderness(K=self.K, L=self.length, r=r_min_1)
                    
                    # Calculate and store compression capacity for later use
                    buckling_class = 'c'
                    imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
                    
                    slenderness_for_design = self.section_size_1.slenderness 
                    
                    # --- IS 800:2007 Cl 7.5.1.2 Single Angle Strut Loaded Through One Leg ---
                    if self.load_type == "Leg Load" and design_dictionary[KEY_SEC_PROFILE] == 'Angles':
                        # Constants for >= 2 bolts (Fixed behavior assumed for selection)
                        k1 = 0.20
                        k2 = 0.35
                        k3 = 20.0
                        
                        b1 = self.section_size_1.a
                        b2 = self.section_size_1.b
                        t = self.section_size_1.thickness
                        r_vv = self.section_size_1.rad_of_gy_v
                        
                        if r_vv > 0:
                            lambda_vv = (self.length / r_vv) 
                            lambda_phi = (b1 + b2) / (2 * t)
                            lambda_e = math.sqrt(k1 + k2 * lambda_vv**2 + k3 * lambda_phi**2)
                            slenderness_for_design = lambda_e

                    results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                        self.section_size_1.fy, self.gamma_m0, slenderness_for_design, 
                        imperfection_factor, 200000, check_type='Concentric')
                    f_cd = results[5]
                    self.section_size_1.compression_capacity = self.section_size_1.area * f_cd
                
                # Condition to limit loop based on max force derived from max available size
                elif (self.load.axial_force * 1000 > self.force1):
                    self.max_limit_status_1 = True
                    self.logger.warning(" : The factored compression force ({} kN) exceeds the compression capacity ({} kN) with respect to the maximum available "
                                   "member size {}.".format(round(self.load.axial_force, 2), round(self.force1/1000, 2), self.max_area))
                    self.logger.info(" : Define member(s) with a higher cross sectional area.")
                    break
                    
                    # Condition to limit loop based on max length derived from max available size
                elif self.length > self.len2:
                    self.max_limit_status_2 = True
                    self.logger.warning(" : The member length ({} mm) exceeds the maximum allowable length ({} mm) with respect to the maximum available "
                                   "member size {}.".format(self.length, round(self.len2, 2), self.max_gyr))
                    self.logger.info(" : Select member(s) with a higher radius of gyration value.")
                    break
                else:
                    pass
            
        if self.member_design_status:

            self.design_status = True # Provisional
            self.select_bolt_dia(design_dictionary)
        else:
            self.design_status = False
            self.logger.warning(" : The available depth of the member cannot accommodate the minimum available bolt diameter of {} mm considering the "
                           "minimum spacing limit [Ref. Cl. 10.2, IS 800:2007].".format(self.bolt_diameter_min))
            self.logger.info(" : Reduce the bolt diameter or increase the member depth and re-design.")
            self.logger.error(": Design is unsafe. \n ")
            self.logger.info(" :=========End Of design===========")


    def select_bolt_dia(self, design_dictionary, dia_remove=None):
        """Selection of bolt (dia) from the available list of bolts based on the spacing limits and capacity"""
        
        # Remove diameters that failed previous checks
        if dia_remove is not None:
            if dia_remove in self.bolt.bolt_diameter:
                self.bolt.bolt_diameter.remove(dia_remove)

        if len(self.bolt.bolt_diameter) == 0:
            self.design_status = False
            self.logger.warning(" : No bolt diameter found that satisfies design requirements.")
            self.logger.error(": Design is unsafe. \n ")
            self.logger.info(" :=========End Of design===========")
            return

        print(self.section_size_1.designation)
        
        # Calculate plate height limits based on section profile
        if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
            self.min_plate_height = self.section_size_1.min_plate_height()
            self.max_plate_height = self.section_size_1.max_plate_height()
        elif design_dictionary[KEY_LOCATION] == 'Long Leg':
            self.min_plate_height = self.section_size_1.max_leg - self.section_size_1.root_radius - self.section_size_1.thickness
            self.max_plate_height = self.section_size_1.max_leg - self.section_size_1.root_radius - self.section_size_1.thickness
        elif design_dictionary[KEY_LOCATION] == 'Short Leg':
            self.min_plate_height = self.section_size_1.min_leg - self.section_size_1.root_radius - self.section_size_1.thickness
            self.max_plate_height = self.section_size_1.min_leg - self.section_size_1.root_radius - self.section_size_1.thickness

        # Calculate res_force (design force for connection) - uses compression_capacity for compression members
        self.res_force = max((self.load.axial_force * 1000), (0.3 * self.section_size_1.compression_capacity))

        # Calculate member and plate thicknesses based on section profile
        if design_dictionary[KEY_SEC_PROFILE] == "Channels":
            bolts_required_previous = 2
            self.thick_plate = (self.res_force * 1.1) / (self.section_size_1.depth * self.plate.fy)
            self.thick = self.section_size_1.web_thickness

        elif design_dictionary[KEY_SEC_PROFILE] == 'Back to Back Channels':
            bolts_required_previous = 2
            self.thick = 2 * self.section_size_1.web_thickness
            self.thick_plate = (self.res_force * 1.1) / (self.section_size_1.depth * self.plate.fy)

        elif design_dictionary[KEY_SEC_PROFILE] == 'Star Angles':
            bolts_required_previous = 1
            self.thick = self.section_size_1.thickness
            if self.loc == "Long Leg":
                self.thick_plate = (self.res_force * 1.1) / (2 * self.section_size_1.max_leg * self.plate.fy)
            else:
                self.thick_plate = (self.res_force * 1.1) / (2 * self.section_size_1.min_leg * self.plate.fy)

        else:  # Angles, Back to Back Angles
            bolts_required_previous = 1
            if self.sec_profile == "Back to Back Angles":
                self.thick = 2 * self.section_size_1.thickness
            else:
                self.thick = self.section_size_1.thickness
            if self.loc == "Long Leg":
                self.thick_plate = (self.res_force * 1.1) / (self.section_size_1.max_leg * self.plate.fy)
            else:
                self.thick_plate = (self.res_force * 1.1) / (self.section_size_1.min_leg * self.plate.fy)

        # Initial plate thickness selection
        if self.thk_count == 0:
            thickness_provided = [i for i in self.plate.thickness if i > self.thick_plate or i == max(self.plate.thickness)]
            if len(thickness_provided) >= 2:
                self.plate.thickness_provided = min(thickness_provided)
            else:
                self.plate.thickness_provided = thickness_provided[0] if thickness_provided else self.plate.thickness[0]

        # Determine number of shear planes
        if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Angles', 'Star Angles']:
            self.planes = 1
        else:
            self.planes = 2

        # Set up bolt connection plate properties
        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((self.thick, self.section_size_1.fu, self.section_size_1.fy))
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))

        # Initialize tracking variables
        bolt_diameter_previous = self.bolt.bolt_diameter[-1]
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        bolt_min = min(self.bolt.bolt_diameter)
        count = 0
        bolt_design_status_1 = False
        bolt_force_previous = 0.0

        # Filter bolt diameters based on grip length check [Ref. Cl.10.3.3.2, IS 800:2007]
        self.bolt_diameter_possible = []
        for d in self.bolt.bolt_diameter:
            if 8 * d < (self.plate.thickness_provided + self.thick):
                continue
            else:
                self.bolt_diameter_possible.append(d)

        if len(self.bolt_diameter_possible) == 0:
            self.design_status = False
            self.logger.warning(" : The combined thickness ({} mm) exceeds the allowable large grip limit check (of {} mm) for the minimum available "
                           "bolt diameter of {} mm [Ref. Cl.10.3.3.2, IS 800:2007]."
                           .format((self.plate.thickness_provided + self.thick), (8 * self.bolt.bolt_diameter[-1]), self.bolt.bolt_diameter[-1]))
            self.logger.error(": Design is unsafe. \n ")
            self.logger.info(" :=========End Of design===========")
        else:
            self.bolt_design_status = False
            # Iterate through diameters in reverse (largest to smallest) for optimization
            for self.bolt.bolt_diameter_provided in reversed(self.bolt_diameter_possible):

                self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                        conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy, n=self.planes)

                self.bolt.min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(
                    self.bolt.bolt_diameter_provided, self.bolt.bolt_hole_type, 'machine_flame_cut'), 2)
                self.bolt.min_edge_dist_round = round_up(self.bolt.min_edge_dist, 5)

                self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                  bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                  conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                                  n_planes=self.planes, e=self.bolt.min_end_dist_round,
                                                  p=self.bolt.min_pitch_round)

                # Get plate details based on section profile
                if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
                    self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                                     web_plate_h_min=self.min_plate_height,
                                                     web_plate_h_max=self.max_plate_height,
                                                     bolt_capacity=self.bolt.bolt_capacity,
                                                     min_edge_dist=self.bolt.min_edge_dist_round,
                                                     min_gauge=self.bolt.min_gauge_round,
                                                     max_spacing=self.bolt.max_spacing_round,
                                                     max_edge_dist=self.bolt.max_edge_dist_round,
                                                     shear_load=0, axial_load=self.res_force, gap=self.plate.gap,
                                                     shear_ecc=False, min_bolts_one_line=2, min_bolt_line=2,
                                                     beta_lg=self.bolt.beta_lg, min_end_dist=self.bolt.min_end_dist_round)
                else:
                    if design_dictionary[KEY_SEC_PROFILE] == "Star Angles":
                        self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                                         web_plate_h_min=self.min_plate_height,
                                                         web_plate_h_max=self.max_plate_height,
                                                         bolt_capacity=self.bolt.bolt_capacity,
                                                         min_edge_dist=self.bolt.min_edge_dist_round,
                                                         min_gauge=self.bolt.min_gauge_round,
                                                         max_spacing=self.bolt.max_spacing_round,
                                                         max_edge_dist=self.bolt.max_edge_dist_round,
                                                         shear_load=0, axial_load=self.res_force / 2,
                                                         gap=self.plate.gap,
                                                         shear_ecc=False, min_bolts_one_line=1, min_bolt_line=2,
                                                         beta_lg=self.bolt.beta_lg, min_end_dist=self.bolt.min_end_dist_round)
                    else:
                        self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                                         web_plate_h_min=self.min_plate_height,
                                                         web_plate_h_max=self.max_plate_height,
                                                         bolt_capacity=self.bolt.bolt_capacity,
                                                         min_edge_dist=self.bolt.min_edge_dist_round,
                                                         min_gauge=self.bolt.min_gauge_round,
                                                         max_spacing=self.bolt.max_spacing_round,
                                                         max_edge_dist=self.bolt.max_edge_dist_round,
                                                         shear_load=0, axial_load=self.res_force,
                                                         gap=self.plate.gap,
                                                         shear_ecc=False, min_bolts_one_line=1, min_bolt_line=2,
                                                         beta_lg=self.bolt.beta_lg, min_end_dist=self.bolt.min_end_dist_round)

                # Check plate design status and optimize bolt selection
                if self.plate.design_status is True:
                    if self.plate.bolts_required > bolts_required_previous and count >= 1:
                        self.bolt.bolt_diameter_provided = bolt_diameter_previous
                        self.plate.bolts_required = bolts_required_previous
                        self.plate.bolt_force = bolt_force_previous
                        self.bolt_design_status = self.plate.design_status
                        break
                    bolts_required_previous = self.plate.bolts_required
                    bolt_diameter_previous = self.bolt.bolt_diameter_provided
                    bolt_force_previous = self.plate.bolt_force
                    count += 1
                    self.bolt_design_status = self.plate.design_status
                else:
                    pass
            bolt_capacity_req = self.bolt.bolt_capacity

        # Handle design status after loop
        if self.plate.design_status == False and self.bolt_design_status != True:
            self.design_status = False
        else:
            self.bolt.bolt_diameter_provided = bolt_diameter_previous
            self.plate.bolts_required = bolts_required_previous
            self.plate.bolt_force = bolt_force_previous

        # Call get_bolt_grade if bolt design succeeded
        if self.bolt_design_status == True:
            self.design_status = True
            print("bolt ok")
            self.get_bolt_grade(design_dictionary)
        else:
            self.design_status = False
            if hasattr(self.plate, 'reason') and self.plate.reason != "":
                self.logger.warning(self.plate.reason)
            self.logger.error(": Design is unsafe. \n ")
            self.logger.info(" :=========End Of design===========")

    def get_bolt_grade(self, design_dictionary):
        """Selection of bolt (grade) from the available list based on spacing limits and capacity"""
        
        bolt_grade_previous = self.bolt.bolt_grade[-1]
        bolts_required_previous = self.plate.bolts_required if hasattr(self.plate, 'bolts_required') else 0
        
        # Set up bolt connection plate properties
        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((self.thick, self.section_size_1.fu, self.section_size_1.fy))
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
        
        # Iterate through grades in reverse (highest to lowest) to find optimal (lowest sufficient) grade
        for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
            count = 1
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy, n=self.planes)
            
            self.bolt.min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(
                self.bolt.bolt_diameter_provided, self.bolt.bolt_hole_type, 'machine_flame_cut'), 2)
            self.bolt.min_edge_dist_round = round_up(self.bolt.min_edge_dist, 5)
            
            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=self.planes, e=self.bolt.min_end_dist_round,
                                              p=self.bolt.min_pitch_round)
            
            # Check reduced bolt capacity (for long joints / large grip)
            bolt_capacity_reduced = self.plate.get_bolt_red(
                self.plate.bolts_one_line if hasattr(self.plate, 'bolts_one_line') else 1,
                self.plate.gauge_provided if hasattr(self.plate, 'gauge_provided') else self.bolt.min_gauge_round,
                self.plate.bolt_line if hasattr(self.plate, 'bolt_line') else 1,
                self.plate.pitch_provided if hasattr(self.plate, 'pitch_provided') else self.bolt.min_pitch_round,
                self.bolt.bolt_capacity,
                self.bolt.bolt_diameter_provided,
                beta_lg=self.bolt.beta_lg)
            
            bolt_force = self.plate.bolt_force if hasattr(self.plate, 'bolt_force') else self.res_force
            
            if bolt_capacity_reduced < bolt_force and count >= 1:
                self.bolt.bolt_grade_provided = bolt_grade_previous
                break
            
            bolts_required_previous = self.plate.bolts_required if hasattr(self.plate, 'bolts_required') else 0
            bolt_grade_previous = self.bolt.bolt_grade_provided
            count += 1
        
        # Recalculate with final selected grade
        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy, n=self.planes)
        
        self.bolt.min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(
            self.bolt.bolt_diameter_provided, self.bolt.bolt_hole_type, 'machine_flame_cut'), 2)
        self.bolt.min_edge_dist_round = round_up(self.bolt.min_edge_dist, 5)
        
        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt.bolt_grade_provided,
                                          conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                          n_planes=self.planes, 
                                          e=self.plate.end_dist_provided if hasattr(self.plate, 'end_dist_provided') else self.bolt.min_end_dist_round,
                                          p=self.plate.pitch_provided if hasattr(self.plate, 'pitch_provided') else self.bolt.min_pitch_round)
        
        # Get plate details with final bolt configuration
        if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
            self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                             web_plate_h_min=self.min_plate_height,
                                             web_plate_h_max=self.max_plate_height,
                                             bolt_capacity=self.bolt.bolt_capacity,
                                             min_edge_dist=self.bolt.min_edge_dist_round,
                                             min_gauge=self.bolt.min_gauge_round,
                                             max_spacing=self.bolt.max_spacing_round,
                                             max_edge_dist=self.bolt.max_edge_dist_round,
                                             shear_load=0, axial_load=self.res_force, gap=self.plate.gap,
                                             shear_ecc=False, min_bolts_one_line=2, min_bolt_line=2,
                                             beta_lg=self.bolt.beta_lg, min_end_dist=self.bolt.min_end_dist_round)
        else:
            if design_dictionary[KEY_SEC_PROFILE] == "Star Angles":
                self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                                 web_plate_h_min=self.min_plate_height,
                                                 web_plate_h_max=self.max_plate_height,
                                                 bolt_capacity=self.bolt.bolt_capacity,
                                                 min_edge_dist=self.bolt.min_edge_dist_round,
                                                 min_gauge=self.bolt.min_gauge_round,
                                                 max_spacing=self.bolt.max_spacing_round,
                                                 max_edge_dist=self.bolt.max_edge_dist_round,
                                                 shear_load=0, axial_load=self.res_force / 2,
                                                 gap=self.plate.gap,
                                                 shear_ecc=False, min_bolts_one_line=1, min_bolt_line=2,
                                                 beta_lg=self.bolt.beta_lg, min_end_dist=self.bolt.min_end_dist_round)
            else:
                self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                                 web_plate_h_min=self.min_plate_height,
                                                 web_plate_h_max=self.max_plate_height,
                                                 bolt_capacity=self.bolt.bolt_capacity,
                                                 min_edge_dist=self.bolt.min_edge_dist_round,
                                                 min_gauge=self.bolt.min_gauge_round,
                                                 max_spacing=self.bolt.max_spacing_round,
                                                 max_edge_dist=self.bolt.max_edge_dist_round,
                                                 shear_load=0, axial_load=self.res_force,
                                                 gap=self.plate.gap,
                                                 shear_ecc=False, min_bolts_one_line=1, min_bolt_line=2,
                                                 beta_lg=self.bolt.beta_lg, min_end_dist=self.bolt.min_end_dist_round)
        
        # Update edge distance provided
        self.plate.edge_dist_provided = round(((self.max_plate_height - ((self.plate.bolts_one_line - 1) * self.plate.gauge_provided)) / 2), 2)
        print(self.plate.bolt_line)
        
        # Call member_check for final compression capacity verification
        self.member_check(design_dictionary)

    def member_check(self, design_dictionary):
        try:
            print("Entering member_check")  # Debug
            # 1. Calculate Member Compression Capacity (Buckling) with detailed properties
            # This acts as the final verification of the member.
            # Determine if section is angle-based or channel-based
            is_angle_profile = self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']
            print(f"is_angle_profile: {is_angle_profile}, sec_profile: {self.sec_profile}")  # Debug
            
            min_rad = self.min_rad_gyration_calc(designation=self.section_size_1.designation,
                                                 material_grade=self.material,
                                                 key=self.sec_profile, subkey=self.loc,
                                                 D_a=self.section_size_1.a if is_angle_profile else self.section_size_1.depth,
                                                 B_b=self.section_size_1.b if is_angle_profile else self.section_size_1.flange_width,
                                                 T_t=self.section_size_1.thickness if is_angle_profile else self.section_size_1.flange_thickness,
                                                 t=self.section_size_1.web_thickness if hasattr(self.section_size_1, 'web_thickness') else 0.0)
            print(f"min_rad_gyration_calc done, min_rad={self.min_radius_gyration}")  # Debug
                                                 
            # Note: min_rad_gyration_calc stores result in self.min_radius_gyration
            
            self.section_size_1.design_check_for_slenderness(self.K, self.length, self.min_radius_gyration)
            print(f"slenderness check done, slenderness={self.section_size_1.slenderness}")  # Debug
            
            # Calculate buckling strength P_d
            # Manually calculating P_d using IS 800:2007 Cl 7.1.2.1
            # Buckling class 'c' assumed for hot-rolled Angles/Channels about any axis
            # Ref: IS 800:2007 Table 10 - conservative assumption for general design
            buckling_class = 'c'
            imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
            print(f"imperfection_factor={imperfection_factor}")  # Debug
            
            results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.section_size_1.fy, self.gamma_m0, self.section_size_1.slenderness, 
                imperfection_factor, 200000, check_type='Concentric') # E=200000
            print(f"design_compressisive_stress results: {results}")  # Debug
                
            # --- IS 800:2007 Cl 7.5.1.2 Single Angle Strut Loaded Through One Leg ---
            # For struts bolted to end gusset, single angles are inherently loaded through one leg
            # Apply this calculation automatically for Single Angles profile
            if is_angle_profile and design_dictionary[KEY_SEC_PROFILE] == 'Angles':
                # Note: Double Angles (Back to Back) connected to opposite sides of gusset 
                # are treated as concentrically loaded (modified KL/r) - Cl 7.5.2.1
                # So this block applies to Single Angles only.
                
                # Constants for >= 2 bolts (Fixed assumed for capacity check before bolt calc)
                k1 = 0.20
                k2 = 0.35
                k3 = 20.0
                
                b1 = self.section_size_1.a
                b2 = self.section_size_1.b
                t = self.section_size_1.thickness
                r_vv = self.section_size_1.rad_of_gy_v
                
                if r_vv > 0:
                    lambda_vv = (self.length / r_vv)
                    lambda_phi = (b1 + b2) / (2 * t)
                    lambda_e = math.sqrt(k1 + k2 * lambda_vv**2 + k3 * lambda_phi**2)
                    
                    # Recalculate stress with lambda_e
                    results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                        self.section_size_1.fy, self.gamma_m0, lambda_e, 
                        imperfection_factor, 200000, check_type='Concentric')
                    
                    # Update slenderness for reporting/output?
                    # Ideally self.section_size_1.slenderness should reflect lambda_e for consistency in reports
                    self.section_size_1.slenderness = lambda_e
                
            f_cd = results[5] # Design compressive stress
            print(f"f_cd={f_cd}")  # Debug
            
            # Store for output display
            self.f_cd = round(f_cd, 2)  # Design Compressive Stress (MPa)
            self.effective_length = round(self.K * self.length, 2)  # Effective Length (mm)
            
            # Effective Area check (Class 4?)
            # For rolled sections (Angle/Channel), usually Class 1-3. 
            # Assuming Ag for now (conservative for standard hot rolled)
            # Verify Class in real implementation.
            
            self.section_size_1.compression_capacity = self.section_size_1.area * f_cd # N
            print(f"compression_capacity={self.section_size_1.compression_capacity}")  # Debug
            
            if self.section_size_1.compression_capacity < self.load.axial_force * 1000:
                self.design_status = False
                self.logger.warning(" : Compression Capacity ({} kN) < Applied Load ({} kN)".format(
                    round(self.section_size_1.compression_capacity/1000, 2), self.load.axial_force))
                self.logger.info(" : Select member(s) with a higher cross sectional area.")
                self.logger.error(": Design is unsafe. \n ")
                self.logger.info(" :=========End Of design===========")
                return
            
            self.efficiency = round(self.load.axial_force * 1000 / self.section_size_1.compression_capacity, 2)
            print(f"efficiency={self.efficiency}, calling member_recheck")  # Debug
            
            # Call member_recheck to handle capacity verification and plate thickness
            self.member_recheck(design_dictionary)
        except Exception as e:
            print(f"EXCEPTION in member_check: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            self.design_status = False
            self.logger.error(f": Internal error in member_check: {e}")
            self.logger.info(" :=========End Of design===========")

    def get_plate_thickness(self, design_dictionary):
        """Select gusset plate thickness that satisfies bearing and yielding checks."""
        # Select plate thickness that satisfies:
        # 1. Bearing strength (Bolt on Plate)
        # 2. Yield Strength of Plate (Compression)
        # 3. Bolt Capacity (Shear/Friction) with Reduction Factors
        
        available_thickness = [t for t in self.plate.thickness if t >= 6.0]  # Min 6mm
        
        if not available_thickness:
            available_thickness = self.plate.thickness  # Fallback to all available
        
        # Bolt properties
        bolt_dia = self.bolt.bolt_diameter_provided
        bolt_hole_type = self.bolt.bolt_hole_type
        
        # Calculate pitch and edge distances (min)
        min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(
                bolt_dia, bolt_hole_type, 'machine_flame_cut'), 2)
        min_edge = round_up(min_edge_dist, 5)
        min_pitch = round_up((2.5 * bolt_dia), 5)
        
        # Use user pitch/edge if provided/valid? For now defaulting to safe min or optimal
        e = 1.5 * (bolt_dia + 2) # Heuristic for end distance
        p = 2.5 * bolt_dia # Pitch
        
        # Max pitch check (Cl 10.2.5) - Compression 12t or 200mm, Tension 16t...
        
        for t_p in available_thickness:
            self.plate.thickness_provided = t_p
            self.plate.connect_to_database_to_get_fy_fu(self.plate.material, t_p)
            
            # --- 1. Bolt Capacity Calculation (Iterative for Reduction Factors) ---
            # Initial guess: Beta factors = 1.0
            beta_lj = 1.0
            beta_lg = 1.0
            
            # Member thickness
            if self.sec_profile in ["Angles", "Back to Back Angles", "Star Angles"]:
                t_member = self.section_size_1.thickness
            else:
                t_member = self.section_size_1.web_thickness if hasattr(self.section_size_1, 'web_thickness') else self.section_size_1.flange_thickness
            
            # Grip Length
            l_grip = t_p + t_member # Sum of partial thicknesses
            
            # Check Large Grip Reduction (Cl 10.3.3.2)
            # if l_grip > 5 * d: beta_lg = 8d / (3d + l_grip)
            if l_grip > 5 * bolt_dia:
                beta_lg = (8 * bolt_dia) / (3 * bolt_dia + l_grip)
                if beta_lg > beta_lj: beta_lg = beta_lj # "beta_lg shall not be greater than beta_lj" - IS 800 text
                # Logic: calc beta_lj first or simultaneously? 
                # beta_lj depends on number of bolts (length of joint). beta_lg depends on thickness.
                # So beta_lg is constant for this thickness.
            else:
                beta_lg = 1.0
                
            # Convergence Loop for Number of Bolts
            n_bolts = 1
            prev_n_bolts = 0
            
            # Max iterations
            for _ in range(10):
                if n_bolts == prev_n_bolts:
                    break
                prev_n_bolts = n_bolts
                
                # Calculate Length of Joint
                # Assuming single line of bolts for simplicity in 1D
                # l_j = (n - 1) * p
                l_j = (n_bolts - 1) * p
                
                # Long Joint Reduction (Cl 10.3.3.1)
                # if l_j > 15d: beta_lj = 1.075 - l_j / (200d)
                if l_j > 15 * bolt_dia:
                    beta_lj = 1.075 - l_j / (200 * bolt_dia)
                    if beta_lj < 0.75: beta_lj = 0.75
                    if beta_lj > 1.0: beta_lj = 1.0
                else:
                    beta_lj = 1.0
                
                # Check beta_lg constraint again (as it limits to beta_lj)
                real_beta_lg = min(beta_lg, beta_lj) if l_grip > 5 * bolt_dia else 1.0
                
                # --- Bolt Shear Capacity (Vdsb) ---
                if self.bolt.bolt_type == 'Bearing Bolt':
                     grade = str(self.bolt.bolt_grade_provided)
                     f_ub = float(grade.split('.')[0]) * 100
                     A_nb = 0.78 * 3.14159 * bolt_dia * bolt_dia / 4
                     
                     # Nominal shear
                     V_nsb = (f_ub / math.sqrt(3)) * A_nb # Single shear plane assumed
                     # Note: Double shear if back-to-back? For now assuming single shear (gusset to member)
                     # If B2B/Star, might be double shear.
                     n_shear_planes = 1 # Update logic for Double Angles if needed
                     
                     V_dsb = V_nsb / 1.25 # gamma_mb
                     
                     # Apply Reduction Factors
                     V_dsb_reduced = V_dsb * beta_lj * real_beta_lg
                     
                     # --- Bolt Bearing Capacity (Vdpb) ---
                     # kb = min(e/3d0, p/3d0 - 0.25, fub/fu, 1.0)
                     d0 = bolt_dia + 2
                     
                     kb = min(e / (3 * d0), p / (3 * d0) - 0.25, 1.0)
                     
                     # On Plate
                     V_npb_plate = 2.5 * kb * bolt_dia * t_p * self.plate.fu
                     V_dpb_plate = V_npb_plate / 1.25
                     
                     # On Member
                     V_npb_member = 2.5 * kb * bolt_dia * t_member * self.section_size_1.fu
                     V_dpb_member = V_npb_member / 1.25
                     
                     bolt_value = min(V_dsb_reduced, V_dpb_plate, V_dpb_member)
                     
                     # Storing capacity
                     self.bolt.bolt_shear_capacity = V_dsb_reduced
                     self.bolt.bolt_bearing_capacity = min(V_dpb_plate, V_dpb_member)
                     
                else: # Friction Grip (HSFG)
                     # Vdsf = Vnsf / gamma_mf
                     # Vnsf = mu_f * ne * Kh * F0
                     mu_f = self.bolt.mu_f # Slip factor
                     n_e = 1 # Number of effective interfaces
                     K_h = 1.0 # Standard holes
                     
                     # Proof Load F0 = Anb * f0
                     grade = str(self.bolt.bolt_grade_provided)
                     f_ub = float(grade.split('.')[0]) * 100
                     f0 = 0.70 * f_ub
                     A_nb = 0.78 * 3.14159 * bolt_dia * bolt_dia / 4
                     F0 = A_nb * f0
                     
                     V_nsf = mu_f * n_e * K_h * F0
                     
                     if self.bolt.bolt_type == "Friction Grip Bolt":
                         gamma_mf = 1.25  # Ultimate load design (standard/usually 1.25)
                     else:
                         gamma_mf = 1.10 # Service load?
                     
                     # Osdag usually designs at Ultimate Load
                     V_dsf = V_nsf / gamma_mf
                     
                     # Determine nominal bearing check requirements (Cl 10.4.4)
                     # "Design capacity at ultimate load may be calculated as per bearing type connection"
                     # So we basically check Bearing Limit as well? 
                     # Checking simple slip resistance first.
                     
                     # Code says: Vdb = min(Vdsf, Vdpb) ?? 
                     # Actually HSFG design is usually governed by Slip at Service or Ultimate.
                     # Cl 10.4.3 is Slip Resistance.
                     # Cl 10.4.4: "Bearing resistance... checked at Ultimate Load."
                     
                     # We will take bolt_value = Vdsf (Slip) but ensure Bearing is not exceeded?
                     # Osdag implementation often treats Bolt Capacity = Vdsf for HSFG.
                     
                     # Reduction factors (Long Joint) applicable to HSFG too? 
                     # Image 3 / Cl 10.4.3.1: "Long joint reduction factor is also applicable to friction grip"
                     V_dsf_reduced = V_dsf * beta_lj
                     
                     # Beta_lg? Not mentioned for HSFG explicitly in summary, but assumed for large grip.
                     
                     bolt_value = V_dsf_reduced
                     self.bolt.bolt_shear_capacity = V_dsf_reduced # Using field for slip
                     self.bolt.bolt_bearing_capacity = 999999 # Not governing usually
                
                self.bolt.bolt_capacity = bolt_value
                n_bolts = math.ceil(self.load.axial_force * 1000 / bolt_value)
                
                # Check min bolts (2)
                if n_bolts < 2: n_bolts = 2
                
                # Calculate Length of Joint
                l_j = (n_bolts - 1) * p
                
                # Validate Max Pitch and Gauge
                # Compression Max Pitch (Cl 10.2.3.2): min(12t, 200mm)
                max_pitch = min(12 * min(t_p, t_member), 200.0)
                if p > max_pitch:
                    # If current pitch is too large, we should technically reduce it, 
                    # but p is typically set to 2.5d_min. If 2.5d > max_pitch, we have a geometry clash.
                    # Usually 2.5d is much smaller than 200mm.
                    pass
            
            # --- Detail Checks (Plate Height) ---
            # Eq 2.30: hp = Depth of Section + 15mm + 15mm
            # Eq 2.30: hp = Depth of Section + 15mm + 15mm
            if self.sec_profile in ["Angles", "Back to Back Angles", "Star Angles"]:
                # For Angle, Depth is usually the connected leg length if connected to gusset?
                # Or Max Leg? Osdag usually aligns centroid or specific leg.
                # Assuming Depth refers to the overall extent. 
                # If "Strut Bolted to End Gusset", likely connected by one leg.
                # Depth = Connected Leg Length?
                # Using max_leg as safer proxy or 'depth' if available in properties
                if self.loc == "Long Leg":
                    depth_sec = self.section_size_1.max_leg
                else:
                    depth_sec = self.section_size_1.min_leg
            else:
                depth_sec = self.section_size_1.depth
                
            h_plate = depth_sec + 30.0 # 15 + 15 mm
            
            # --- 2. Plate Checks (Yielding, Rupture, Block Shear) ---
            
            # A. Yielding of Gross Section (Cl 6.2)
            # Tdg = Ag * fy / gamma_m0
            # Width of plate?
            # Assuming effective width or full height of plate is engaged?
            # Conventional practice: Width approx h_plate at critical section?
            # Or Whitmore section? 
            # Osdag simplified: Check yield on full h_plate.
            plate_yield_cap = h_plate * t_p * self.plate.fy / self.gamma_m0
            
            # B. Rupture of Critical Section (Cl 6.3)
            # Tdn = 0.9 * An * fu / gamma_m1
            # An = (Width - n_holes * d0) * t
            # Number of bolts in a row at critical section? Assuming 1 for single line.
            # If multiple lines, update logic.
            # bolt_line = number of columns? 
            # In current logic, single line (column) -> 1 bolt per row?
            # Wait, 1D array of bolts -> 1 column. 
            n_row = 1
            d_hole = bolt_dia + 2 # Clearance
            An = (h_plate - n_row * d_hole) * t_p
            plate_rupture_cap = 0.9 * An * self.plate.fu / self.gamma_m1
            
            # C. Block Shear (Cl 6.4)
            # Tdb = min(Tdb1, Tdb2)
            # Avg, Avn (Shear area - parallel to load)
            # Atg, Atn (Tension area - perp to load)
            # Layout: Single line of n_bolts
            # Shear Plane Length = (n-1)*p + e
            # Tension Plane Width = e (distance from last bolt to edge perpendicular?)
            # Or 30mm/edge min?
            # For End Gusset:
            # Failure path: Shear along line of bolts + Tension to edge.
            # L_v = (n_bolts - 1) * p + e
            # L_t = e (Simple block shear for single line)
            
            Avg = l_j + e
            Avg = Avg * t_p
            Avn = (l_j + e - (n_bolts - 0.5) * d_hole) * t_p
            
            Atg = e * t_p # Perp distance
            Atn = (e - 0.5 * d_hole) * t_p # Perp net
            
            Tdb1 = (Avg * self.plate.fy / (math.sqrt(3) * self.gamma_m0) + 
                    0.9 * Atn * self.plate.fu / self.gamma_m1)
            
            Tdb2 = (0.9 * Avn * self.plate.fu / (math.sqrt(3) * self.gamma_m1) + 
                    Atg * self.plate.fy / self.gamma_m0)
            
            plate_block_shear_cap = min(Tdb1, Tdb2)
            
            # Minimal Capacity Check
            plate_cap = min(plate_yield_cap, plate_rupture_cap, plate_block_shear_cap)
            
            if plate_cap < self.load.axial_force * 1000:
                continue # Try next thickness
            
            # All capacity checks passed - save design and call status_pass
            self.plate.height = h_plate
            self.plate.length = l_j + 2 * e
            
            # Store specific capacities for reporting
            self.plate.shear_capacity = plate_block_shear_cap
            self.plate.block_shear_capacity = plate_block_shear_cap
            self.plate.tension_yielding_capacity = plate_yield_cap
            self.plate.tension_rupture_capacity = plate_rupture_cap
            
            # For output display
            self.plate_tension_capacity = plate_cap 
            
            # Update bolt object with final calc properties
            self.bolt.bolt_capacity = bolt_value
            self.efficiency = round(self.load.axial_force * 1000 / min(bolt_value * n_bolts, plate_cap), 2)
            
            # Bolt Layout Update
            self.plate.bolts_one_line = n_bolts
            self.plate.bolt_line = 1
            
            # Call status_pass (handles plate length check like tension_bolted)
            self.status_pass(design_dictionary)
            # status_pass handles all logging (success or plate length failure)
            # Break here - status_pass already logged appropriate message
            return  # Exit function entirely - no post-loop logging needed
            
        # If we reach here, no plate thickness passed capacity checks
        # Only log if status_pass was never called
        self.design_status = False
        self.plate.reason = "Gusset Plate / Bolt Design Failed. Possible causes: plate thickness too small or grip exceeds limit."
        self.logger.warning(": Gusset Plate / Bolt Design Failed.")
        self.logger.info(": Possible causes: plate thickness too small or grip exceeds limit.")
        self.logger.error(": Design is unsafe. \n ")
        self.logger.info(" :=========End Of design===========")

    def status_pass(self, design_dictionary):
        """
        Final status check and logging matching tension_bolted style.
        Checks plate length and logs success/failure accordingly.
        """
        if (2 * self.plate.length) > self.length:
            self.design_status = False
            self.plate.reason = ": The plate length of {} mm is larger than the member length of {} mm.".format(
                2 * self.plate.length, self.length)
            self.logger.warning(": The plate length of {} mm is larger than the member length of {} mm.".format(
                2 * self.plate.length, self.length))
            self.logger.info(": Try a bolt of larger diameter and/or increase the member length.")
            self.logger.error(": Design is unsafe. \n ")
            self.logger.info(" :=========End Of design===========")
        else:
            self.plate_design_status = True
            self.design_status = True
            self.intermittent_bolt(design_dictionary)
            self.logger.info(": In the case of reverse loading, the slenderness value shall be less than 180 [Ref. Table 3, IS 800:2007].")
            if self.sec_profile not in ["Angles", "Channels"] and self.length > 1000:
                self.logger.info(": In the case of reverse loading for double sections, spacing of the intermittent connection shall be less than 1000 "
                            "[Ref. Cl. 10.2.5.4, IS 800:2007].")
            self.logger.info(": To reduce the quantity of bolts, define a list of diameter, plate thickness and/or member size higher than the "
                        "one currently defined.")

            if self.load.axial_force < (self.res_force / 1000):
                self.logger.info(": The minimum design force based on the member size is used for performing the connection design, i.e. {} kN "
                            "[Ref. Cl. 10.7, IS 800:2007].".format(round(self.res_force / 1000, 2)))

            self.logger.info(": Overall bolted compression member design is safe. \n")
            self.logger.info(": =========End Of design===========")

            if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
                self.min_rad_gyration_calc(designation=self.section_size_1.designation,
                                           material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, 
                                           D_a=self.section_size_1.a,
                                           B_b=self.section_size_1.b, 
                                           T_t=self.section_size_1.thickness)
            else:
                self.min_rad_gyration_calc(designation=self.section_size_1.designation,
                                           material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, 
                                           D_a=self.section_size_1.depth,
                                           B_b=self.section_size_1.flange_width, 
                                           T_t=self.section_size_1.flange_thickness,
                                           t=self.section_size_1.web_thickness)

    def intermittent_bolt(self, design_dictionary):
        """
        Calculate intermittent connection details for built-up sections.
        Based on IS 800:2007 Cl 10.2.5.4 - Maximum spacing <= 1000mm for compression members.
        """
        # Calculate intermediate length (length between end connections)
        # For compression, we need to account for end plate connections
        if hasattr(self.plate, 'end_dist_provided') and hasattr(self.plate, 'bolt_line'):
            self.inter_length = self.length - 2 * (self.plate.end_dist_provided + (self.plate.bolt_line - 1) * self.plate.pitch_provided)
        else:
            # Fallback if plate details not available
            self.inter_length = self.length - 2 * 50.0  # Assume 50mm end distance
        
        if design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Angles', 'Star Angles', 'Back to Back Channels']:
            # Calculate minimum radius of gyration for individual component
            if design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Angles', 'Star Angles']:
                # For angles, use single angle properties
                self.inter_memb = Angle(designation=self.section_size_1.designation, 
                                      material_grade=design_dictionary[KEY_SEC_MATERIAL])
                min_gyration = min(self.inter_memb.rad_of_gy_u, self.inter_memb.rad_of_gy_v)
            elif design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Channels']:
                self.inter_memb = Channel(designation=self.section_size_1.designation,
                                        material_grade=design_dictionary[KEY_SEC_MATERIAL])
                min_gyration = min(self.inter_memb.rad_of_gy_y, self.inter_memb.rad_of_gy_z)
            
            # IS 800:2007 Cl 10.2.5.4 - Maximum spacing for compression members: 1000mm
            # Also check individual component slenderness: lambda <= 50 or 0.7 * lambda_whole
            # For compression: spacing <= 400 * r_min (or 1000mm max)
            if self.inter_length > 1000:
                self.inter_memb_length = 400 * min_gyration
                
                if self.inter_memb_length > 1000:
                    # If calculated spacing > 1000mm, use 1000mm max
                    ratio = round_up(self.inter_length / 1000, 1)
                else:
                    ratio = round_up(self.inter_length / self.inter_memb_length, 1)
                
                self.inter_memb_length = self.inter_length / ratio
                self.inter_conn = ratio - 1
                
                # Use same bolt details as end connection
                self.inter_bolt_one_line = self.plate.bolts_one_line
                self.inter_bolt_line = 1
                
                # Plate dimensions for intermittent connection
                if hasattr(self.plate, 'end_dist_provided'):
                    self.inter_plate_length = 2 * self.plate.end_dist_provided
                else:
                    self.inter_plate_length = 100.0  # Default
                
                # Plate height based on section profile and location
                if self.sec_profile == "Star Angles":
                    if self.loc == "Long Leg":
                        self.inter_plate_height = 2 * self.section_size_1.max_leg
                    else:
                        self.inter_plate_height = 2 * self.section_size_1.max_leg
                elif self.sec_profile == "Back to Back Angles":
                    if self.loc == "Long Leg":
                        self.inter_plate_height = self.section_size_1.max_leg
                    else:
                        self.inter_plate_height = self.section_size_1.max_leg
                else:  # Back to Back Channels
                    self.inter_plate_height = self.section_size_1.depth
                
                self.inter_dia = self.bolt.bolt_diameter_provided
                self.inter_grade = self.bolt.bolt_grade_provided
                

            else:
                # No intermittent connections needed
                self.inter_conn = 0.0
                self.inter_bolt_one_line = 0.0
                self.inter_bolt_line = 0.0
                self.inter_plate_length = 0.0
                self.inter_plate_height = 0.0
                self.inter_memb_length = 0.0
                self.inter_dia = 0.0
                self.inter_grade = 0.0
        else:
            # Single sections don't need intermittent connections
            self.inter_conn = 0.0
            self.inter_bolt_one_line = 0.0
            self.inter_bolt_line = 0.0
            self.inter_plate_length = 0.0
            self.inter_plate_height = 0.0
            self.inter_memb_length = 0.0
            self.inter_dia = 0.0
            self.inter_grade = 0.0        

    def min_rad_gyration_calc(self, designation, material_grade, key, subkey, D_a=0.0, B_b=0.0, T_t=0.0, t=0.0):

        if key == "Channels" and subkey == "Web":
            Channel_attributes = Channel(designation, material_grade)
            rad_y = Channel_attributes.rad_of_gy_y
            rad_z = Channel_attributes.rad_of_gy_z
            min_rad = min(rad_y, rad_z)

        elif key == 'Back to Back Channels' and subkey == "Web":
            BBChannel_attributes = BBChannel_Properties()
            BBChannel_attributes.data(designation, material_grade)
            rad_y = BBChannel_attributes.calc_RogY(f_w=B_b, f_t=T_t, w_h=D_a, w_t=t) * 10
            rad_z = BBChannel_attributes.calc_RogZ(f_w=B_b, f_t=T_t, w_h=D_a, w_t=t) * 10
            min_rad = min(rad_y, rad_z)

        elif key == "Back to Back Angles" and subkey == 'Long Leg':
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            rad_y = BBAngle_attributes.calc_RogY(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            min_rad = min(rad_y, rad_z)

        elif key == 'Back to Back Angles' and subkey == 'Short Leg':
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            rad_y = BBAngle_attributes.calc_RogY(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            min_rad = min(rad_y, rad_z)

        elif key == 'Star Angles' and subkey == 'Long Leg':
            SAngle_attributes = SAngle_Properties()
            SAngle_attributes.data(designation, material_grade)
            rad_y = SAngle_attributes.calc_RogY(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_z = SAngle_attributes.calc_RogZ(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_u = SAngle_attributes.calc_RogU(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_v = SAngle_attributes.calc_RogV(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            min_rad = min(rad_y, rad_z, rad_u, rad_v)

        elif key == 'Star Angles' and subkey == 'Short Leg':
            SAngle_attributes = SAngle_Properties()
            SAngle_attributes.data(designation, material_grade)
            rad_y = SAngle_attributes.calc_RogY(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_z = SAngle_attributes.calc_RogZ(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_u = SAngle_attributes.calc_RogU(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_v = SAngle_attributes.calc_RogV(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            min_rad = min(rad_y, rad_z, rad_u, rad_v)

        elif key == 'Angles' and (subkey == 'Long Leg' or subkey == 'Short Leg'):
            Angle_attributes = Angle(designation, material_grade)
            rad_u = Angle_attributes.rad_of_gy_u
            rad_v = Angle_attributes.rad_of_gy_v
            min_rad = min(rad_u, rad_v)

        else:
            min_rad = 0.0

        self.min_radius_gyration = min_rad

    def member_recheck(self, design_dictionary):
        """Comparing applied force and compression capacity and if failed, 
        it returns to initial member selection which selects member of higher area"""
        try:
            print("Entering member_recheck")  # Debug
            
            if self.section_size_1.compression_capacity >= self.load.axial_force * 1000:
                self.design_status = True
                self.efficiency = round((self.load.axial_force * 1000 / self.section_size_1.compression_capacity), 2)
                print(f"Calling get_plate_thickness, efficiency={self.efficiency}")  # Debug
                self.get_plate_thickness(design_dictionary)
                print("get_plate_thickness completed")  # Debug

            else:
                if len(self.sizelist) >= 2:
                    size = self.section_size_1.designation
                    print("recheck", size)
                    self.initial_member_capacity(design_dictionary, size)
                else:
                    self.design_status = False
                    self.logger.warning(" : The factored compression force ({} kN) exceeds the compression capacity ({} kN) with respect to the maximum available "
                                   "member size {}."
                                   .format(round(self.load.axial_force, 2), round(self.section_size_1.compression_capacity/1000, 2), self.max_area))
                    self.logger.info(" : Select member(s) with a higher cross sectional area.")
                    self.logger.error(": Design is unsafe. \n ")
                    self.logger.info(" :=========End Of design===========")
        except Exception as e:
            print(f"EXCEPTION in member_recheck: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            self.design_status = False
            self.logger.error(f": Internal error in member_recheck: {e}")
            self.logger.info(" :=========End Of design===========")

    def results_to_test(self, filename):
        """Output design results to test file"""
        test_out_list = {KEY_DISP_DESIGNATION: self.section_size_1.designation,
                         KEY_DISP_DESIGN_STRENGTH_COMPRESSION: self.section_size_1.compression_capacity,
                         KEY_DISP_SLENDER: self.section_size_1.slenderness,
                         KEY_DISP_EFFICIENCY: self.efficiency,
                         KEY_OUT_DISP_D_PROVIDED: self.bolt.bolt_diameter_provided,
                         KEY_OUT_DISP_GRD_PROVIDED: self.bolt.bolt_grade_provided,
                         KEY_OUT_DISP_BOLT_SHEAR: self.bolt.bolt_shear_capacity,
                         KEY_OUT_DISP_BOLT_BEARING: self.bolt.bolt_bearing_capacity,
                         KEY_OUT_DISP_BOLT_CAPACITY: self.bolt.bolt_capacity,
                         KEY_OUT_DISP_BOLT_LINE: self.plate.bolt_line,
                         KEY_OUT_DISP_BOLTS_ONE_LINE: self.plate.bolts_one_line,
                         KEY_OUT_DISP_PLATETHK: self.plate.thickness_provided,
                         KEY_OUT_DISP_PLATE_MIN_HEIGHT: self.plate.height,
                         KEY_OUT_DISP_PLATE_MIN_LENGTH: self.plate.length}
        f = open(filename, "w")
        f.write(str(test_out_list))
        f.close()

    def save_design(self, popup_summary):
        """
        Save the design results and generate the design report.
        Based on tension_bolted.py but adapted for compression members.
        """
        # Determine section for report
        if self.member_design_status == True:
            section_size = self.section_size_1
            depth_max = round(self.max_plate_height, 2) if hasattr(self, 'max_plate_height') else 0.0
        else:
            if self.max_limit_status_2 == True:
                if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
                    section_size = Angle(designation=self.max_gyr, material_grade=self.material)
                else:
                    section_size = Channel(designation=self.max_gyr, material_grade=self.material)
            else:
                if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
                    section_size = Angle(designation=self.max_area, material_grade=self.material)
                else:
                    section_size = Channel(designation=self.max_area, material_grade=self.material)
            depth_max = round(self.max_depth, 2) if hasattr(self, 'max_depth') else 0.0

        # Determine image and connecting plates based on section profile
        if self.sec_profile in ["Channels", "Back to Back Channels"]:
            if self.sec_profile == "Back to Back Channels":
                connecting_plates = [self.plate.thickness_provided, section_size.web_thickness]
                if section_size.flange_slope == 90:
                    image = "Parallel_BBChannel"
                else:
                    image = "Slope_BBChannel"
            else:
                connecting_plates = [self.plate.thickness_provided, section_size.web_thickness]
                if section_size.flange_slope == 90:
                    image = "Parallel_Channel"
                else:
                    image = "Slope_Channel"
            min_gauge = self.pitch_round if hasattr(self, 'pitch_round') else 0.0
            row_limit = "Row~Limit~(rl)~=~2"
            row = 2
            depth = 2 * (self.edge_dist_min_round if hasattr(self, 'edge_dist_min_round') else 30) + (self.pitch_round if hasattr(self, 'pitch_round') else 40)
        elif section_size.max_leg == section_size.min_leg:
            # Equal angles
            if self.sec_profile == "Back to Back Angles":
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]
                if self.loc == "Long Leg":
                    image = "bblequaldp"
                else:
                    image = "bbsequaldp"
            elif self.sec_profile == "Star Angles":
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]
                if self.loc == "Long Leg":
                    image = "salequaldp"
                else:
                    image = "sasequaldp"
            else:
                image = "equaldp"
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]
            min_gauge = 0.0
            row_limit = "Row~Limit~(rl)~=~1"
            row = 1
            depth = 2 * (self.edge_dist_min_round if hasattr(self, 'edge_dist_min_round') else 30)
        else:
            # Unequal angles
            if self.sec_profile == "Back to Back Angles":
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]
                if self.loc == "Long Leg":
                    image = "bblunequaldp"
                else:
                    image = "bbsunequaldp"
            elif self.sec_profile == "Star Angles":
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]
                if self.loc == "Long Leg":
                    image = "salunequaldp"
                else:
                    image = "sasunequaldp"
            else:
                image = "unequaldp"
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]
            min_gauge = 0.0
            row_limit = "Row~Limit~(rl)~=~1"
            row = 1
            depth = 2 * (self.edge_dist_min_round if hasattr(self, 'edge_dist_min_round') else 30)

        # Gamma values for bolts
        if self.member_design_status == True:
            if self.bolt.bolt_type == TYP_BEARING:
                variable = KEY_DISP_GAMMA_MB
                value = cl_5_4_1_table_4_5_gamma_value(self.bolt.gamma_mb, "mb")
            else:
                variable = KEY_DISP_GAMMA_MF
                value = cl_5_4_1_table_4_5_gamma_value(self.bolt.gamma_mf, "mf")
        else:
            variable = KEY_DISP_GAMMA_MF
            value = cl_5_4_1_table_4_5_gamma_value(1.25, "mf")

        # Member capacity for report - COMPRESSION SPECIFIC
        if self.member_design_status == True:
            compression_capacity_kn = round(section_size.compression_capacity / 1000, 2)
            slenderness = section_size.slenderness
            gyration = self.min_radius_gyration
        else:
            if hasattr(self, 'max_limit_status_2') and self.max_limit_status_2 == True:
                [force_temp, l_temp, slenderness, gyration] = self.max_force_length(self.max_gyr)
                compression_capacity_kn = round(force_temp / 1000, 2)
            else:
                [force_temp, l_temp, slenderness, gyration] = self.max_force_length(self.max_area)
                compression_capacity_kn = round(force_temp / 1000, 2)

        # Section report data based on profile
        if self.sec_profile == "Channels":
            self.report_supporting = {
                KEY_DISP_SEC_PROFILE: image,
                KEY_DISP_SECSIZE: (section_size.designation, self.sec_profile),
                KEY_DISP_MATERIAL: section_size.material,
                KEY_REPORT_MASS: round(section_size.mass, 2),
                KEY_REPORT_AREA: round(section_size.area, 2),
                KEY_REPORT_DEPTH: round(section_size.depth, 2),
                KEY_REPORT_WIDTH: round(section_size.flange_width, 2),
                KEY_REPORT_WEB_THK: round(section_size.web_thickness, 2),
                KEY_REPORT_FLANGE_THK: round(section_size.flange_thickness, 2),
                KEY_DISP_FLANGE_S_REPORT: round(section_size.flange_slope, 2),
                KEY_REPORT_R1: round(section_size.root_radius, 2),
                KEY_REPORT_R2: round(section_size.toe_radius, 2),
                KEY_REPORT_CY: round(section_size.Cy, 2),
                KEY_REPORT_IZ: round(section_size.mom_inertia_z * 1e-4, 2),
                KEY_REPORT_IY: round(section_size.mom_inertia_y * 1e-4, 2),
                KEY_REPORT_RZ: round(section_size.rad_of_gy_z * 1e-1, 2),
                KEY_REPORT_RY: round(section_size.rad_of_gy_y * 1e-1, 2),
                KEY_REPORT_ZEZ: round(section_size.elast_sec_mod_z * 1e-3, 2),
                KEY_REPORT_ZEY: round(section_size.elast_sec_mod_y * 1e-3, 2),
                KEY_REPORT_ZPZ: round(section_size.plast_sec_mod_z * 1e-3, 2),
                KEY_REPORT_ZPY: round(section_size.elast_sec_mod_y * 1e-3, 2),
                KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)
            }
            thickness = section_size.web_thickness
            text = "C"

        elif self.sec_profile == "Back to Back Channels":
            BBChannel = BBChannel_Properties()
            BBChannel.data(section_size.designation, section_size.material)
            self.report_supporting = {
                KEY_DISP_SEC_PROFILE: image,
                KEY_DISP_SECSIZE: (section_size.designation, self.sec_profile),
                KEY_DISP_MATERIAL: section_size.material,
                KEY_REPORT_MASS: round(2 * section_size.mass, 2),
                KEY_REPORT_AREA: round(2 * section_size.area, 2),
                KEY_REPORT_DEPTH: round(section_size.depth, 2),
                KEY_REPORT_WIDTH: round(section_size.flange_width, 2),
                KEY_REPORT_WEB_THK: round(section_size.web_thickness, 2),
                KEY_REPORT_FLANGE_THK: round(section_size.flange_thickness, 2),
                '$T_p$ (mm)': round(self.plate.thickness_provided, 2),
                KEY_DISP_FLANGE_S_REPORT: round(section_size.flange_slope, 2),
                KEY_REPORT_R1: round(section_size.root_radius, 2),
                KEY_REPORT_R2: round(section_size.toe_radius, 2),
                KEY_REPORT_IZ: round((BBChannel.calc_MomentOfAreaZ(section_size.flange_width, section_size.flange_thickness, section_size.depth, section_size.web_thickness) * 10000) * 1e-4, 2),
                KEY_REPORT_IY: round((BBChannel.calc_MomentOfAreaY(section_size.flange_width, section_size.flange_thickness, section_size.depth, section_size.web_thickness) * 10000) * 1e-4, 2),
                KEY_REPORT_RZ: round((BBChannel.calc_RogZ(section_size.flange_width, section_size.flange_thickness, section_size.depth, section_size.web_thickness) * 10) * 1e-1, 2),
                KEY_REPORT_RY: round((BBChannel.calc_RogY(section_size.flange_width, section_size.flange_thickness, section_size.depth, section_size.web_thickness) * 10) * 1e-1, 2),
                KEY_REPORT_ZEZ: round((BBChannel.calc_ElasticModulusZz(section_size.flange_width, section_size.flange_thickness, section_size.depth, section_size.web_thickness) * 1000) * 1e-3, 2),
                KEY_REPORT_ZEY: round((BBChannel.calc_ElasticModulusZy(section_size.flange_width, section_size.flange_thickness, section_size.depth, section_size.web_thickness) * 1000) * 1e-3, 2),
                KEY_REPORT_ZPZ: round((BBChannel.calc_PlasticModulusZpz(section_size.flange_width, section_size.flange_thickness, section_size.depth, section_size.web_thickness) * 1000) * 1e-3, 2),
                KEY_REPORT_ZPY: round((BBChannel.calc_PlasticModulusZpy(section_size.flange_width, section_size.flange_thickness, section_size.depth, section_size.web_thickness) * 1000) * 1e-3, 2),
                KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)
            }
            thickness = section_size.web_thickness
            text = "C"

        elif self.sec_profile == "Angles":
            self.report_supporting = {
                KEY_DISP_SEC_PROFILE: image,
                KEY_DISP_SECSIZE: (section_size.designation, self.sec_profile),
                KEY_DISP_MATERIAL: section_size.material,
                KEY_REPORT_MASS: round(section_size.mass, 2),
                KEY_REPORT_AREA: round(section_size.area, 2),
                KEY_REPORT_MAX_LEG_SIZE: round(section_size.max_leg, 2),
                KEY_REPORT_MIN_LEG_SIZE: round(section_size.min_leg, 2),
                KEY_REPORT_ANGLE_THK: round(section_size.thickness, 2),
                KEY_REPORT_R1: round(section_size.root_radius, 2),
                KEY_REPORT_R2: round(section_size.toe_radius, 2),
                KEY_REPORT_CY: round(section_size.Cy, 2),
                KEY_REPORT_CZ: round(section_size.Cz, 2),
                KEY_REPORT_IZ: round(section_size.mom_inertia_z * 1e-4, 2),
                KEY_REPORT_IY: round(section_size.mom_inertia_y * 1e-4, 2),
                KEY_REPORT_IU: round(section_size.mom_inertia_u * 1e-4, 2),
                KEY_REPORT_IV: round(section_size.mom_inertia_v * 1e-4, 2),
                KEY_REPORT_RZ: round(section_size.rad_of_gy_z * 1e-1, 2),
                KEY_REPORT_RY: round(section_size.rad_of_gy_y * 1e-1, 2),
                KEY_REPORT_RU: round(section_size.rad_of_gy_u * 1e-1, 2),
                KEY_REPORT_RV: round(section_size.rad_of_gy_v * 1e-1, 2),
                KEY_REPORT_ZEZ: round(section_size.elast_sec_mod_z * 1e-3, 2),
                KEY_REPORT_ZEY: round(section_size.elast_sec_mod_y * 1e-3, 2),
                KEY_REPORT_ZPZ: round(section_size.plast_sec_mod_z * 1e-3, 2),
                KEY_REPORT_ZPY: round(section_size.plast_sec_mod_y * 1e-3, 2),
                KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)
            }
            thickness = section_size.thickness
            text = "A"

        elif self.sec_profile == "Back to Back Angles":
            Angle_attributes = BBAngle_Properties()
            Angle_attributes.data(section_size.designation, section_size.material)
            if self.loc == "Long Leg":
                Cz = round((Angle_attributes.calc_Cz(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc) * 10), 2)
                Cy = "N/A"
            else:
                Cy = round((Angle_attributes.calc_Cy(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc) * 10), 2)
                Cz = "N/A"

            self.report_supporting = {
                KEY_DISP_SEC_PROFILE: image,
                KEY_DISP_SECSIZE: (section_size.designation, self.sec_profile),
                KEY_DISP_MATERIAL: section_size.material,
                KEY_REPORT_MASS: round(2 * section_size.mass, 2),
                KEY_REPORT_AREA: round(2 * section_size.area, 2),
                KEY_REPORT_MAX_LEG_SIZE: round(section_size.max_leg, 2),
                KEY_REPORT_MIN_LEG_SIZE: round(section_size.min_leg, 2),
                KEY_REPORT_ANGLE_THK: round(section_size.thickness, 2),
                '$T$ (mm)': round(self.plate.thickness_provided, 2),
                KEY_REPORT_R1: round(section_size.root_radius, 2),
                KEY_REPORT_R2: round(section_size.toe_radius, 2),
                KEY_REPORT_CY: Cy,
                KEY_REPORT_CZ: Cz,
                KEY_REPORT_IZ: round((Angle_attributes.calc_MomentOfAreaZ(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc) * 10000) * 1e-4, 2),
                KEY_REPORT_IY: round((Angle_attributes.calc_MomentOfAreaY(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc) * 10000) * 1e-4, 2),
                KEY_REPORT_RZ: round(Angle_attributes.calc_RogZ(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_RY: round(Angle_attributes.calc_RogY(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_ZEZ: round(Angle_attributes.calc_ElasticModulusZz(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_ZEY: round(Angle_attributes.calc_ElasticModulusZy(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_ZPZ: round(Angle_attributes.calc_PlasticModulusZpz(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_ZPY: round(Angle_attributes.calc_PlasticModulusZpy(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)
            }
            thickness = section_size.thickness
            text = "A"

        else:  # Star Angles
            Angle_attributes = SAngle_Properties()
            Angle_attributes.data(section_size.designation, section_size.material)
            self.report_supporting = {
                KEY_DISP_SEC_PROFILE: image,
                KEY_DISP_SECSIZE: (section_size.designation, self.sec_profile),
                KEY_DISP_MATERIAL: section_size.material,
                KEY_REPORT_MASS: round(2 * section_size.mass, 2),
                KEY_REPORT_AREA: round(2 * section_size.area, 2),
                KEY_REPORT_MAX_LEG_SIZE: round(section_size.max_leg, 2),
                KEY_REPORT_MIN_LEG_SIZE: round(section_size.min_leg, 2),
                KEY_REPORT_ANGLE_THK: round(section_size.thickness, 2),
                '$T$ (mm)': round(self.plate.thickness_provided, 2),
                KEY_REPORT_R1: round(section_size.root_radius, 2),
                KEY_REPORT_R2: round(section_size.toe_radius, 2),
                KEY_REPORT_IZ: round(Angle_attributes.calc_MomentOfAreaZ(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_IY: round(Angle_attributes.calc_MomentOfAreaY(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_IU: round(Angle_attributes.calc_MomentOfAreaU(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_IV: round(Angle_attributes.calc_MomentOfAreaV(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_RZ: round(Angle_attributes.calc_RogZ(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_RY: round(Angle_attributes.calc_RogY(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_RU: round(Angle_attributes.calc_RogU(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_RV: round(Angle_attributes.calc_RogV(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_ZEZ: round(Angle_attributes.calc_ElasticModulusZz(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_ZEY: round(Angle_attributes.calc_ElasticModulusZy(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_ZPZ: round(Angle_attributes.calc_PlasticModulusZpz(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_ZPY: round(Angle_attributes.calc_PlasticModulusZpy(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc), 2),
                KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)
            }
            thickness = section_size.thickness
            text = "A"

        # Report Input section
        self.report_input = {
            KEY_MODULE: self.module,
            KEY_DISP_AXIAL_STAR: self.load.axial_force,
            KEY_DISP_LENGTH: self.length,
            "Selected Section Details": self.report_supporting,
            KEY_DISP_SEC_PROFILE: self.sec_profile,
            KEY_DISP_SECSIZE: str(self.sizelist),
            "Section Material": section_size.material,
            KEY_DISP_ULTIMATE_STRENGTH_REPORT: round(section_size.fu, 2),
            KEY_DISP_YIELD_STRENGTH_REPORT: round(section_size.fy, 2),
            "Bolt Details - Input and Design Preference": "TITLE",
            KEY_DISP_D: str([int(d) for d in self.bolt.bolt_diameter]),
            KEY_DISP_GRD: str([float(d) for d in self.bolt.bolt_grade]),
            KEY_DISP_TYP: self.bolt.bolt_type,
            KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
            KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
            KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM: self.bolt.corrosive_influences,
            "Plate Details - Input and Design Preference": "TITLE",
            KEY_DISP_PLATETHK: str([int(d) for d in self.plate.thickness]),
            KEY_DISP_MATERIAL: self.plate.material,
            KEY_DISP_ULTIMATE_STRENGTH_REPORT + " (Plate)": round(self.plate.fu, 2),
            KEY_DISP_YIELD_STRENGTH_REPORT + " (Plate)": round(self.plate.fy, 2),
        }
        
        if self.bolt.bolt_type == TYP_FRICTION_GRIP:
            self.report_input[KEY_DISP_DP_BOLT_SLIP_FACTOR_REPORT] = self.bolt.mu_f

        # Report check list
        self.report_check = []
        self.load.shear_force = 0.0

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        
        if self.sec_profile in ["Back to Back Angles", "Star Angles", "Back to Back Channels"]:
            multiple = 2
        else:
            multiple = 1

        t1 = ('Selected', 'Selected Member Data', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
        self.report_check.append(t1)

        if self.member_design_status == True:

            # =========================================================================
            # SECTION 1: BUCKLING CLASS & IMPERFECTION FACTOR
            # =========================================================================
            t1 = ('SubSection', 'Buckling Class & Imperfection Factor', 
                '|p{5cm}|p{4.5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            # Get imperfection factor (should be calculated in member_check)
            imperfection_factor = self.imperfection_factor if hasattr(self, 'imperfection_factor') else 0.49
            bucklingclass = 'c'  # Conservative assumption for angles/channels (Table 10, IS 800:2007)

            t1 = ('Buckling Curve Classification', 
                '',
                NoEscape(f'{bucklingclass}'+'\\newline'+f'[Ref.~IS~800:2007,~Table~10]'),
                '')
            self.report_check.append(t1)

            t1 = (r'Imperfection Factor ($\alpha$)',
                '',
                NoEscape(f'{str(imperfection_factor)}'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~7.1.2.2]'),
                '')
            self.report_check.append(t1)

            # =========================================================================
            # SECTION 2: SECTION CLASSIFICATION
            # =========================================================================
            t1 = ('SubSection', 'Section Classification', 
                '|p{5cm}|p{4.5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            epsilon = math.sqrt(250 / section_size.fy)

            if self.sec_profile in ["Angles", "Back to Back Angles", "Star Angles"]:
                # For angles
                b = section_size.min_leg
                d = section_size.max_leg
                t = section_size.thickness

                b_t_ratio = round(b / t, 2)
                d_t_ratio = round(d / t, 2)
                bd_t_ratio = round((b + d) / (2 * t), 2)

                limit_1 = round(15.7 * epsilon, 2)
                limit_2 = round(25 * epsilon, 2)

                t1 = ('Outstanding element', 
                    NoEscape(r'$\dfrac{b}{t} \leq 15.7\varepsilon$'),
                    NoEscape(f'$\\dfrac{{{b}}}{{{t}}} = {b_t_ratio} \\leq {limit_1}$'),
                    get_pass_fail(limit_1, b_t_ratio, relation='geq'))
                self.report_check.append(t1)

                t1 = ('Outstanding element', 
                    NoEscape(r'$\dfrac{d}{t} \leq 15.7\varepsilon$'),
                    NoEscape(f'$\\dfrac{{{d}}}{{{t}}} = {d_t_ratio} \\leq {limit_1}$'),
                    get_pass_fail(limit_1, d_t_ratio, relation='geq'))
                self.report_check.append(t1)

                t1 = ('Axial Compression', 
                    NoEscape(r'$\dfrac{(b+d)}{2t} \leq 25\varepsilon$'),
                    NoEscape(f'$\\dfrac{{{b + d}}}{{2 \\times {t}}} = {bd_t_ratio} \\leq {limit_2}$'),
                    get_pass_fail(limit_2, bd_t_ratio, relation='geq'))
                self.report_check.append(t1)

            elif self.sec_profile in ["Channels", "Back to Back Channels"]:
                # For channels
                b_tf = section_size.flange_width / 2
                tf = section_size.flange_thickness
                d_web = section_size.depth - 2 * section_size.flange_thickness
                tw = section_size.web_thickness

                b_tf_ratio = round(b_tf / tf, 2)
                d_tw_ratio = round(d_web / tw, 2)

                limit_flange = round(10.5 * epsilon, 2)
                limit_web = round(42 * epsilon, 2)

                t1 = ('Flange (Outstanding)', 
                    NoEscape(r'$\dfrac{b/2}{t_f} \leq 10.5\varepsilon$'),
                    NoEscape(f'$\\dfrac{{{round(b_tf, 2)}}}{{{tf}}} = {b_tf_ratio} \\leq {limit_flange}$'),
                    get_pass_fail(limit_flange, b_tf_ratio, relation='geq'))
                self.report_check.append(t1)

                t1 = ('Web (Internal)', 
                    NoEscape(r'$\dfrac{d}{t_w} \leq 42\varepsilon$'),
                    NoEscape(f'$\\dfrac{{{round(d_web, 2)}}}{{{tw}}} = {d_tw_ratio} \\leq {limit_web}$'),
                    get_pass_fail(limit_web, d_tw_ratio, relation='geq'))
                self.report_check.append(t1)

            t1 = ('Note', '', 
                'All above criteria should be satisfied', 
                '')
            self.report_check.append(t1)

            section_class = "Semi-Compact"  # Conservative for compression members
            t1 = ('Section Class', 
                '',
                NoEscape(f'{section_class}'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~3.7]'), 
                '')
            self.report_check.append(t1)

            # =========================================================================
            # SECTION 3: EFFECTIVE SLENDERNESS RATIO
            # =========================================================================
            t1 = ('SubSection', 'Effective Slenderness Ratio', 
                '|p{5cm}|p{4.5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            K = self.K
            L = self.length
            r_min = self.min_radius_gyration
            lambda_e = round(section_size.slenderness, 2)

            if self.sec_profile == "Angles" and hasattr(self, 'k1'):
                # For angles loaded through one leg - show detailed calculation
                k1 = self.k1 if hasattr(self, 'k1') else 0.2
                k2 = self.k2 if hasattr(self, 'k2') else 0.35
                k3 = self.k3 if hasattr(self, 'k3') else 20.0

                t1 = ('Formula',
                    '',
                    NoEscape(r'$\lambda_e = \sqrt{k_1 + k_2\lambda_{vv}^2 + k_3\lambda_\psi^2}$'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~7.5.1.2]'),
                    '')
                self.report_check.append(t1)

                # Show constants based on fixity and number of bolts
                fixity_str = 'Hinged' if not hasattr(self, 'fixity') else self.fixity
                bolts_str = '2' if not hasattr(self, 'num_bolts') else str(self.num_bolts)

                t1 = (r'Constants', 
                    f'{bolts_str}~bolts,~{fixity_str}',
                    NoEscape(f'$k_1 = {k1},~k_2 = {k2},~k_3 = {k3}$'),
                    '')
                self.report_check.append(t1)

                if hasattr(self, 'lambda_vv'):
                    t1 = (r'$\lambda_{vv}$', 
                        '',
                        NoEscape(f'$\\lambda_{{vv}} = \\dfrac{{L}}{{r_v}} \\sqrt{{\\dfrac{{f_y}}{{2\\pi^2 E}}}} = {round(self.lambda_vv, 2)}$'),
                        '')
                    self.report_check.append(t1)

                if hasattr(self, 'lambda_psi'):
                    t1 = (r'$\lambda_\psi$', 
                        '',
                        NoEscape(f'$\\lambda_\\psi = \\dfrac{{b_1 + b_2}}{{2t}} \\sqrt{{\\dfrac{{f_y}}{{2\\pi^2 E}}}} = {round(self.lambda_psi, 2)}$'),
                        '')
                    self.report_check.append(t1)

                t1 = (r'$\lambda_e$', 
                    '',
                    NoEscape(f'$\\lambda_e = {lambda_e}$'),
                    '')
                self.report_check.append(t1)
            else:
                # For other sections or concentrically loaded
                t1 = ('Effective Length Factor', '', f'$K = {K}$', '')
                self.report_check.append(t1)

                t1 = ('Unsupported Length', '', f'$L = {L}$ mm', '')
                self.report_check.append(t1)

                t1 = ('Minimum Radius of Gyration', '', 
                    NoEscape(f'$r_{{min}} = {round(r_min, 2)}$ mm'), '')
                self.report_check.append(t1)

                t1 = ('Effective Slenderness', 
                    '',
                    NoEscape(f'$\\lambda_e = \\dfrac{{KL}}{{r_{{min}}}} = \\dfrac{{{K} \\times {L}}}{{{round(r_min, 2)}}} = {lambda_e}$'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~7.1.2]'),
                    '')
                self.report_check.append(t1)

            # Slenderness check
            t1 = ('Slenderness Limit', 
                '',
                NoEscape(f'$\\lambda_e = {lambda_e} \\leq 180$'+'\\newline'+f'[Ref.~IS~800:2007,~Table~3]'),
                get_pass_fail(180, lambda_e, relation='geq'))
            self.report_check.append(t1)

            # =========================================================================
            # SECTION 4: CHECKS FOR STRENGTH
            # =========================================================================
            t1 = ('SubSection', 'Checks for Strength', 
                '|p{5cm}|p{4.5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            # Euler Buckling Stress
            E = 200000  # MPa
            f_cc = round((math.pi**2 * E) / (lambda_e**2), 2) if lambda_e > 0 else 999999

            t1 = ('Euler Buckling Stress', 
                '',
                NoEscape(f'$f_{{cc}} = \\dfrac{{\\pi^2 E}}{{\\lambda_e^2}} = \\dfrac{{\\pi^2 \\times {E}}}{{{lambda_e}^2}} = {f_cc}$ MPa'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~7.1.2.1]'),
                '')
            self.report_check.append(t1)

            # Non-dimensional slenderness
            f_y = section_size.fy
            lambda_bar = round(math.sqrt(f_y / f_cc), 3) if f_cc > 0 else 0

            t1 = (r'Non-dimensional slenderness', 
                '',
                NoEscape(f'$\\bar{{\\lambda}} = \\sqrt{{\\dfrac{{f_y}}{{f_{{cc}}}}}} = \\sqrt{{\\dfrac{{{f_y}}}{{{f_cc}}}}} = {lambda_bar}$'),
                '')
            self.report_check.append(t1)

            # Phi calculation
            alpha = imperfection_factor
            phi = round(0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2), 3)

            t1 = (r'$\phi$ factor',
                '',
                NoEscape(f'$\\phi = 0.5[1 + \\alpha(\\bar{{\\lambda}} - 0.2) + \\bar{{\\lambda}}^2]$' + '\\newline'+
                        f'$= 0.5[1 + {alpha} \\times ({lambda_bar} - 0.2) + {lambda_bar}^2]$' + '\\newline' + f'$  = {phi}$'),
                '')
            self.report_check.append(t1)

            # Stress reduction factor (chi)
            chi = round(1 / (phi + math.sqrt(phi**2 - lambda_bar**2)), 3) if phi**2 >= lambda_bar**2 else 1.0
            chi = min(chi, 1.0)  # Chi cannot exceed 1.0

            t1 = (r'Stress reduction factor',
                '',
                NoEscape((f'$\\chi = \\dfrac{{1}}{{\\phi + \\sqrt{{\\phi^2 - \\bar{{\\lambda}}^2}}}}$') + '\\newline' +
                         (f'$= \\dfrac{{1}}{{{phi} + \\sqrt{{{phi}^2 - {lambda_bar}^2}}}}$' + '\\newline' + f'$  = {chi}$')),
                '')
            self.report_check.append(t1)

            # Design compressive stress
            f_cd = round(chi * f_y / gamma_m0, 2)

            t1 = (r'Design Compressive Stress',
                '',
                NoEscape(f'$f_{{cd}} = \\dfrac{{\\chi f_y}}{{\\gamma_{{m0}}}} = \\dfrac{{{chi} \\times {f_y}}}{{{gamma_m0}}} = {f_cd}$ N/mm$^2$'+'\\newline'+
                f'[Ref.~IS~800:2007,~Cl.~7.1.2]'),
                '')
            self.report_check.append(t1)

            # Design Compressive Strength
            if self.sec_profile in ['Angles', "Channels"]:
                A_e = round(section_size.area, 2)
            else:
                A_e = round(2 * section_size.area, 2)

            P_d = round((A_e * f_cd) / 1000, 2)  # kN
            P_applied = self.load.axial_force

            t1 = (r'Design Compressive Strength', 
                '',
                NoEscape(f'$P_d = A_e \\times f_{{cd}} = {A_e} \\times {f_cd} \\times 10^{{-3}} = {P_d}$ kN'),
                '')
            self.report_check.append(t1)

            t1 = ('Capacity Check', 
                NoEscape(r'$P \leq P_d$'),
                NoEscape(f'${P_applied} \\leq {P_d}$'),
                get_pass_fail(P_applied, P_d, relation='leq'))
            self.report_check.append(t1)

            # Efficiency
            efficiency = round(P_applied / P_d, 3) if P_d > 0 else 999
            t1 = ('Efficiency', 
                NoEscape(r'$\eta < 1.0$'),
                NoEscape(f'$\\eta = \\dfrac{{P}}{{P_d}} = \\dfrac{{{P_applied}}}{{{P_d}}} = {efficiency}$'),
                get_pass_fail(1.0, efficiency, relation='geq'))
            self.report_check.append(t1)

            # =========================================================================
            # SECTION 5: BOLT DESIGN (Enhanced)
            # =========================================================================
            t7 = ('SubSection', 'Design of Bolts', 
                '|p{5cm}|p{4.5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t7)

            # Bolt Properties
            t1 = ('Bolt Type', '', self.bolt.bolt_type, '')
            self.report_check.append(t1)

            t6 = (KEY_OUT_DISP_D_PROVIDED, '',
                display_prov(int(self.bolt.bolt_diameter_provided), "d"), '')
            self.report_check.append(t6)

            t8 = (KEY_DISP_BOLT_HOLE, '', 
                display_prov(int(self.bolt.d_0), "d_0"), '')
            self.report_check.append(t8)

            t8 = (KEY_OUT_DISP_GRD_PROVIDED, '', 
                self.bolt.bolt_grade_provided, '')
            self.report_check.append(t8)

            f_ub = round(self.bolt.bolt_fu, 2)
            t8 = (KEY_DISP_DP_BOLT_FU, '',
                display_prov(f_ub, "f_{u_{b}}"), '')
            self.report_check.append(t8)

            # Bolt Areas
            A_nb = self.bolt.bolt_net_area if hasattr(self.bolt, 'bolt_net_area') else 0
            A_sb = self.bolt.bolt_shank_area if hasattr(self.bolt, 'bolt_shank_area') else A_nb

            t8 = (KEY_DISP_BOLT_AREA, 
                '',
                NoEscape(f'$A_{{n_b}} = {round(A_nb, 2)}$ mm$^2$'+'\\newline'+f'[Ref.~IS~1367-3~(2002)]'),
                '')
            self.report_check.append(t8)

            # Bolt Capacity Calculations
            if self.bolt.bolt_type == TYP_BEARING:
                # Shear Capacity
                gamma_mb = 1.25
                n_s = 1  # Number of shear planes (single shear for end plate connection)
                n_n = 1  # Planes with threads

                # Calculate nominal shear capacity
                V_nsb = round((f_ub / math.sqrt(3)) * ((n_n * A_nb) + (n_s - n_n) * A_sb), 2)
                V_dsb = round(V_nsb / gamma_mb, 2)
                V_dsb_kn = round(V_dsb / 1000, 2)

                t1 = ('Bolt Shear Capacity',
                    '',
                    NoEscape(f'$V_{{nsb}} = \\dfrac{{f_{{ub}}}}{{\\sqrt{{3}}}}(n_n A_{{nb}} + n_s A_{{sb}})$' + '\\newline'+
                            f'$= \\dfrac{{{f_ub}}}{{\\sqrt{{3}}}}({n_n} \\times {round(A_nb, 2)} + {n_s} - {n_n} \\times {round(A_sb, 2)})$'+ '\\newline'+ f'$= {V_nsb}$ N'
                            + '\\newline' + f'[Ref.~IS~800:2007,~Cl.~10.3.3]'),
                    '')
                self.report_check.append(t1)

                # Bearing Capacity
                if hasattr(self.bolt, 'bolt_bearing_capacity'):
                    bolt_bearing_capacity_kn = round(self.bolt.bolt_bearing_capacity / 1000, 2)

                    # Calculate k_b factor
                    d = self.bolt.bolt_diameter_provided
                    d_0 = self.bolt.d_0
                    e_provided = self.plate.end_dist_provided if hasattr(self.plate, 'end_dist_provided') else 1.5 * d_0
                    p_provided = self.plate.pitch_provided if hasattr(self.plate, 'pitch_provided') else 3 * d_0

                    k_b_e = round(e_provided / (3 * d_0), 3)
                    k_b_p = round(p_provided / (3 * d_0) - 0.25, 3)
                    k_b_fu = round(self.bolt.bolt_fu / self.plate.fu, 3) if hasattr(self.plate, 'fu') else 1.0
                    k_b = min(k_b_e, k_b_p, k_b_fu, 1.0)

                    t2 = ('Bearing Factor', 
                        '',
                        NoEscape(f'$k_b = \\min\\left(\\dfrac{{e}}{{3d_0}}, \\dfrac{{p}}{{3d_0}} - 0.25, \\dfrac{{f_{{ub}}}}{{f_u}}, 1.0\\right) = {round(k_b, 2)}$'),
                        '')
                    self.report_check.append(t2)

                    t2 = ('Bolt Bearing Capacity', 
                        '',
                        NoEscape(f'$V_{{dpb}} = \\dfrac{{2.5 k_b d t f_u}}{{\\gamma_{{mb}}}} = {bolt_bearing_capacity_kn}$ kN'+'\\newline'+
                        f'[Ref.~IS~800:2007,~Cl.~10.3.4]'),
                        '')
                    self.report_check.append(t2)

                # Long Joint Reduction Factor
                if hasattr(self.bolt, 'beta_lj') and self.bolt.beta_lj < 1.0:
                    beta_lj = round(self.bolt.beta_lj, 3)
                    l_j = (self.plate.bolts_one_line - 1) * self.plate.pitch_provided if hasattr(self.plate, 'pitch_provided') else 0

                    t3 = ('Long Joint Reduction', 
                        '',
                        NoEscape(f'$\\beta_{{lj}} = 1.075 - \\dfrac{{l_j}}{{200d}}$'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~10.3.3.1]'),
                        '')
                    self.report_check.append(t3)

                    t3 = ('', 
                        f'$l_j = {l_j}$ mm',
                        NoEscape(f'$\\beta_{{lj}} = 1.075 - \\dfrac{{{l_j}}}{{200 \\times {d}}} = {beta_lj}$'),
                        '')
                    self.report_check.append(t3)

                    V_dsb_reduced = round(V_dsb * beta_lj / 1000, 2)
                    t4 = ('Reduced Shear Capacity', 
                        '',
                        NoEscape(f'$V\'_{{dsb}} = \\beta_{{lj}} V_{{dsb}} = {beta_lj} \\times {V_dsb_kn} = {V_dsb_reduced}$ kN'),
                        '')
                    self.report_check.append(t4)

                # Large Grip Reduction Factor
                if hasattr(self.bolt, 'beta_lg') and self.bolt.beta_lg < 1.0:
                    beta_lg = round(self.bolt.beta_lg, 3)
                    l_g = self.plate.thickness_provided + section_size.thickness if self.sec_profile in ["Angles", "Back to Back Angles", "Star Angles"] else self.plate.thickness_provided + section_size.web_thickness

                    t3 = ('Large Grip Reduction', 
                        '',
                        NoEscape(f'$\\beta_{{lg}} = \\dfrac{{8d}}{{3d + l_g}}$, $l_g = {round(l_g, 2)}$ mm'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~10.3.3.2]'),
                        '')
                    self.report_check.append(t3)

                    t3 = ('', 
                        '',
                        NoEscape(f'$\\beta_{{lg}} = \\dfrac{{8 \\times {d}}}{{3 \\times {d} + {round(l_g, 2)}}} = {beta_lg}$'),
                        '')
                    self.report_check.append(t3)

                # Final Bolt Capacity
                bolt_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2) if self.bolt.bolt_capacity else 0.0
                bolt_shear_capacity_kn = round(self.bolt.bolt_shear_capacity / 1000, 2) if hasattr(self.bolt, 'bolt_shear_capacity') else 0.0
                bolt_bearing_capacity_kn = round(self.bolt.bolt_bearing_capacity / 1000, 2) if hasattr(self.bolt, 'bolt_bearing_capacity') else 999

                t3 = ('Bolt Capacity', '',
                    NoEscape(f'$V_{{db}} = \\min(V_{{dsb}}, V_{{dpb}}) = \\min({bolt_shear_capacity_kn}, {bolt_bearing_capacity_kn}) = {bolt_capacity_kn}$ kN'),
                    '')
                self.report_check.append(t3)

            elif self.bolt.bolt_type == TYP_FRICTION:
                # Slip Resistance for HSFG bolts
                mu_f = self.bolt.mu_f if hasattr(self.bolt, 'mu_f') else 0.55
                n_e = 1  # Number of friction interfaces
                K_h = 1.0  # Hole factor (1.0 for standard holes)
                f_0 = 0.7 * f_ub
                F_0 = round(A_nb * f_0, 2)

                gamma_mf = 1.25
                V_nsf = round(mu_f * n_e * K_h * F_0, 2)
                V_dsf = round(V_nsf / gamma_mf, 2)
                V_dsf_kn = round(V_dsf / 1000, 2)

                t1 = ('Proof Load', 
                    '',
                    NoEscape(f'$F_0 = 0.7 f_{{ub}} A_{{nb}} = 0.7 \\times {f_ub} \\times {round(A_nb, 2)} \\times 10^{{-3}} = {round(F_0/1000, 2)}$ kN'),
                    '')
                self.report_check.append(t1)

                t1 = ('Slip Coefficient', '', f'$\\mu_f = {mu_f}$', '[Ref.~IS~800:2007,~Table~20]')
                self.report_check.append(t1)

                t1 = ('Slip Resistance', 
                    '[Ref.~IS~800:2007,~Cl.~10.4.3]',
                    NoEscape(f'$V_{{nsf}} = \\mu_f n_e K_h F_0 = {mu_f} \\times {n_e} \\times {K_h} \\times {round(F_0/1000, 2)} = {round(V_nsf/1000, 2)}$ kN'),
                    '')
                self.report_check.append(t1)

                t1 = ('Design Slip Resistance', 
                    '',
                    NoEscape(f'$V_{{dsf}} = \\dfrac{{V_{{nsf}}}}{{\\gamma_{{mf}}}} = \\dfrac{{{round(V_nsf/1000, 2)}}}{{{gamma_mf}}} = {V_dsf_kn}$ kN'),
                    '')
                self.report_check.append(t1)

                bolt_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2) if self.bolt.bolt_capacity else V_dsf_kn

            # Number of Bolts Required
            n_bolts = self.plate.bolts_required if hasattr(self.plate, 'bolts_required') else self.plate.bolts_one_line
            n_bolts_calc = math.ceil(P_applied / bolt_capacity_kn) if bolt_capacity_kn > 0 else 2

            t5 = ('Number of Bolts Required', '',
                NoEscape(f'$n = \\left\\lceil \\dfrac{{P}}{{V_{{db}}}} \\right\\rceil = \\left\\lceil \\dfrac{{{P_applied}}}{{{bolt_capacity_kn}}} \\right\\rceil = {n_bolts}$'),
                '')
            self.report_check.append(t5)

            t6 = (DISP_NUM_OF_COLUMNS, '', 
                display_prov(self.plate.bolt_line if hasattr(self.plate, 'bolt_line') else 1, "n_c"), '')
            self.report_check.append(t6)

            t7 = (DISP_NUM_OF_ROWS, '', 
                display_prov(self.plate.bolts_one_line if hasattr(self.plate, 'bolts_one_line') else 1, "n_r"), '')
            self.report_check.append(t7)

            # =====================================================================
            # SECTION 6: DETAILING CHECKS
            # =====================================================================
            t1 = ('SubSection', 'Detailing Checks', 
                  '|p{5cm}|p{4.5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            d = self.bolt.bolt_diameter_provided
            d_0 = self.bolt.d_0
            t_plate = self.plate.thickness_provided

            # Pitch checks
            p_provided = self.plate.pitch_provided if hasattr(self.plate, 'pitch_provided') else 0
            p_min = round(2.5 * d, 2)
            p_max = round(min(32 * t_plate, 300), 2)

            t1 = (DISP_MIN_PITCH, 
                  cl_10_2_2_min_spacing(d),
                  f'{p_provided} mm',
                  get_pass_fail(p_min, p_provided, relation='leq'))
            self.report_check.append(t1)

            t1 = (DISP_MAX_PITCH,
                  cl_10_2_3_1_max_spacing(connecting_plates),
                  f'{p_provided} mm',
                  get_pass_fail(p_max, p_provided, relation='geq'))
            self.report_check.append(t1)

            # Gauge checks (if applicable)
            if self.plate.bolt_line > 1:
                g_provided = self.plate.gauge_provided if hasattr(self.plate, 'gauge_provided') else 0
                g_min = p_min
                g_max = p_max

                t2 = (DISP_MIN_GAUGE,
                      cl_10_2_2_min_spacing(d),
                      f'{g_provided} mm',
                      get_pass_fail(g_min, g_provided, relation="leq"))
                self.report_check.append(t2)

                t2 = (DISP_MAX_GAUGE,
                      cl_10_2_3_1_max_spacing(connecting_plates),
                      f'{g_provided} mm',
                      get_pass_fail(g_max, g_provided, relation="geq"))
                self.report_check.append(t2)

            # Edge distance checks
            e_provided = self.plate.edge_dist_provided if hasattr(self.plate, 'edge_dist_provided') else 0
            edge_type = self.bolt.edge_type if hasattr(self.bolt, 'edge_type') else 'machine_flame_cut'
            e_min = round(1.5 * d_0, 2) if edge_type == 'machine_flame_cut' else round(1.7 * d_0, 2)
            e_max = round(12 * t_plate * epsilon, 2)

            t3 = (DISP_MIN_EDGE,
                  cl_10_2_4_2_min_edge_end_dist(d_0, edge_type),
                  f'{e_provided} mm',
                  get_pass_fail(e_min, e_provided, relation='leq'))
            self.report_check.append(t3)

            t3 = (DISP_MAX_EDGE,
                  NoEscape(f'$\\leq 12t\\varepsilon = {e_max}$ mm'),
                  f'{e_provided} mm',
                  get_pass_fail(e_max, e_provided, relation='geq'))
            self.report_check.append(t3)

            # End distance checks
            end_provided = self.plate.end_dist_provided if hasattr(self.plate, 'end_dist_provided') else 0
            end_min = e_min
            end_max = e_max

            t3 = (DISP_MIN_END,
                  cl_10_2_4_2_min_edge_end_dist(d_0, edge_type),
                  f'{end_provided} mm',
                  get_pass_fail(end_min, end_provided, relation='leq'))
            self.report_check.append(t3)

            t3 = (DISP_MAX_END,
                  NoEscape(f'$\\leq 12t\\varepsilon = {end_max}$ mm'),
                  f'{end_provided} mm',
                  get_pass_fail(end_max, end_provided, relation='geq'))
            self.report_check.append(t3)

            # =========================================================================
            # SECTION 7: GUSSET PLATE DESIGN (Enhanced)
            # =========================================================================
            if self.bolt_design_status == True:
                t7 = ('SubSection', 'Design of Gusset Plate', 
                    '|p{5cm}|p{4.5cm}|p{5cm}|p{1.5cm}|')
                self.report_check.append(t7)

                # Plate Geometry
                h_p = int(self.plate.height) if hasattr(self.plate, 'height') else 0
                l_p = int(self.plate.length) if hasattr(self.plate, 'length') else 0
                t_p = self.plate.thickness_provided

                t1 = ('Plate Thickness', '', 
                    display_prov(t_p, "t_p"), '')
                self.report_check.append(t1)

                t3 = ('Plate Height', '', 
                    NoEscape(f'$h_p = {h_p}$ mm'), '')
                self.report_check.append(t3)

                t4 = ('Plate Length', '', 
                    NoEscape(f'$l_p = {l_p}$ mm'), '')
                self.report_check.append(t4)

                # Check plate length vs member length
                t4 = (KEY_OUT_DISP_MEMB_MIN_LENGTH, 
                    NoEscape(r'$2l_p \leq L_{member}$'),
                    NoEscape(f'$2 \\times {l_p} = {2 * l_p} \\leq {self.length}$'),
                    get_pass_fail(2 * l_p, self.length, relation="leq"))
                self.report_check.append(t4)

                # Material Properties
                f_y_plate = round(self.plate.fy, 2) if hasattr(self.plate, 'fy') else 250
                f_u_plate = round(self.plate.fu, 2) if hasattr(self.plate, 'fu') else 410

                t1 = ('Plate Material', '', 
                    self.plate.material if hasattr(self.plate, 'material') else 'E250', 
                    '')
                self.report_check.append(t1)

                t1 = ('Plate Yield Strength', '', 
                    NoEscape(f'$f_{{y,p}} = {f_y_plate}$ MPa'), '')
                self.report_check.append(t1)

                t1 = ('Plate Ultimate Strength', '', 
                    NoEscape(f'$f_{{u,p}} = {f_u_plate}$ MPa'), '')
                self.report_check.append(t1)

                # Tension Yielding Capacity (Tdg)
                A_g = h_p * t_p
                T_dg = round((A_g * f_y_plate) / gamma_m0, 2)
                T_dg_kN = round(T_dg / 1000, 2)

                t2 = ('Gross Area', '', 
                    NoEscape(f'$A_g = h_p \\times t_p = {h_p} \\times {t_p} = {A_g}$ mm$^2$'),
                    '')
                self.report_check.append(t2)

                t2 = ('Tension Yielding Capacity', 
                    '',
                    NoEscape(f'$T_{{dg}} = \\dfrac{{A_g f_{{y,p}}}}{{\\gamma_{{m0}}}}$' +
                             f'$= \\dfrac{{{A_g} \\times {f_y_plate}}}{{{gamma_m0}}} \\times 10^{{-3}} = {T_dg_kN}$ kN'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~6.2]'),
                    '')
                self.report_check.append(t2)

                # Tension Rupture Capacity (Tdn)
                n_bolts_plate = self.plate.bolts_one_line
                A_nc = A_g - n_bolts_plate * d_0 * t_p
                T_dn = round((0.9 * A_nc * f_u_plate) / gamma_m1, 2)
                T_dn_kN = round(T_dn / 1000, 2)

                t1 = ('Net Area', 
                    '',
                    NoEscape(f'$A_{{nc}} = A_g - n \\times d_0 \\times t_p = {A_g} - {n_bolts_plate} \\times {d_0} \\times {t_p} = {round(A_nc, 2)}$ mm$^2$'),
                    '')
                self.report_check.append(t1)

                t1 = ('Tension Rupture Capacity', 
                    '',
                    NoEscape(f'$T_{{dn}} = \\dfrac{{0.9 A_{{nc}} f_{{u,p}}}}{{\\gamma_{{m1}}}}$'+
                             f'$= \\dfrac{{0.9 \\times {round(A_nc, 2)} \\times {f_u_plate}}}{{{gamma_m1}}} \\times 10^{{-3}} = {T_dn_kN}$ kN'+'\\newline'+f'[Ref.~IS~800:2007,~Cl.~6.3]'),
                    '')
                self.report_check.append(t1)

                # Block Shear Capacity (Tdb)
                p = self.plate.pitch_provided if hasattr(self.plate, 'pitch_provided') else 0
                e = self.plate.end_dist_provided if hasattr(self.plate, 'end_dist_provided') else 0
                l_j = (n_bolts_plate - 1) * p

                A_vg = l_j * t_p
                A_vn = (l_j - (n_bolts_plate - 0.5) * d_0) * t_p
                A_tg = e * t_p
                A_tn = (e - 0.5 * d_0) * t_p

                T_db1 = round((A_vg * f_y_plate / (math.sqrt(3) * gamma_m0)) + (0.9 * A_tn * f_u_plate / gamma_m1), 2)
                T_db2 = round((0.9 * A_vn * f_u_plate / (math.sqrt(3) * gamma_m1)) + (A_tg * f_y_plate / gamma_m0), 2)
                T_db = min(T_db1, T_db2)
                T_db_kN = round(T_db / 1000, 2)

                t4 = ('Block Shear Areas', 
                    '',
                    NoEscape(f'$A_{{vg}} = {round(A_vg, 2)}$ mm$^2$,'+'\\newline'+ f'$A_{{vn}} = {round(A_vn, 2)}$ mm$^2$'+ '\\newline'+
                             f'$A_{{tg}} = {round(A_tg, 2)}$ mm$^2$,'+'\\newline'+ f'$A_{{tn}} = {round(A_tn, 2)}$ mm$^2$'),
                    '')
                self.report_check.append(t4)


                t4 = ('Block Shear Capacity', 
                    '',
                    NoEscape(f'$T_{{db1}} = \\dfrac{{A_{{vg}} f_y}}{{\\sqrt{{3}}\\gamma_{{m0}}}} + \\dfrac{{0.9 A_{{tn}} f_u}}{{\\gamma_{{m1}}}} = {round(T_db1/1000, 2)}$ kN'+ '\\newline'+
                             f'$T_{{db2}} = \\dfrac{{0.9 A_{{vn}} f_u}}{{\\sqrt{{3}}\\gamma_{{m1}}}} + \\dfrac{{A_{{tg}} f_y}}{{\\gamma_{{m0}}}} = {round(T_db2/1000, 2)}$ kN'+ '\\newline'+
                             f'$T_{{db}} = \\min(T_{{db1}}, T_{{db2}}) = {T_db_kN}$ kN'+ '\\newline'+ f'[Ref.~IS~800:2007,~Cl.~6.4]'),
                    '')
                self.report_check.append(t4)

                # Design Tension Capacity (Td)
                T_d = min(T_dg, T_dn, T_db)
                T_d_kN = round(T_d / 1000, 2)

                t1 = ('Design Tension Capacity', '',
                    NoEscape(f'$T_d = \\min(T_{{dg}}, T_{{dn}}, T_{{db}})$'+'\\newline'+f'$T_d = \\min({T_dg_kN}, {T_dn_kN}, {T_db_kN}) = {T_d_kN}$ kN'),
                    '')
                self.report_check.append(t1)

                # Plate Capacity Check
                t1 = ('Plate Capacity Check', 
                    NoEscape(r'$P \leq T_d$'),
                    NoEscape(f'${P_applied} \\leq {T_d_kN}$'),
                    get_pass_fail(P_applied, T_d_kN, relation='leq'))
                self.report_check.append(t1)

        # Intermittent Connection Section
        if self.plate_design_status == True and self.sec_profile not in ["Angles", "Channels"] and hasattr(self, 'inter_length') and self.inter_length > 1000:
            t7 = ('SubSection', 'Intermittent Connection', '|p{5cm}|p{4.5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t7)

            t5 = (KEY_OUT_DISP_INTERCONNECTION, " ", self.inter_conn if hasattr(self, 'inter_conn') else 0, "")
            self.report_check.append(t5)

            t5 = (KEY_OUT_DISP_INTERSPACING, 1000, round(self.inter_memb_length, 2) if hasattr(self, 'inter_memb_length') else 0,
                  get_pass_fail(1000, self.inter_memb_length if hasattr(self, 'inter_memb_length') else 0, relation="geq"))
            self.report_check.append(t5)

            t6 = (KEY_OUT_DISP_D_PROVIDED, "", int(self.inter_dia) if hasattr(self, 'inter_dia') else 0, '')
            self.report_check.append(t6)

            t8 = (KEY_OUT_DISP_GRD_PROVIDED, "", self.inter_grade if hasattr(self, 'inter_grade') else 0, '')
            self.report_check.append(t8)

            t3 = (KEY_OUT_DISP_PLATE_MIN_HEIGHT, '', int(self.inter_plate_height) if hasattr(self, 'inter_plate_height') else 0, "")
            self.report_check.append(t3)

            t4 = (KEY_OUT_DISP_PLATE_MIN_LENGTH, "", int(self.inter_plate_length) if hasattr(self, 'inter_plate_length') else 0, "")
            self.report_check.append(t4)

        # Update overall design status
        if self.bolt_design_status and self.plate_design_status:
             self.design_status = True

        # Populate hover_dict for 3D model tooltips
        self.hover_dict["Member"] = f"Member: {self.section_size_1.designation}"
        self.hover_dict["Plate"] = f"Plate: {self.plate.length}x{self.plate.height}x{self.plate.thickness_provided}"
        self.hover_dict["Bolt"] = f"Bolt: {self.bolt.bolt_diameter_provided}mm dia, Grade {self.bolt.bolt_grade}"
        
        # Generate LaTeX report
        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"

        rel_path = str(sys.path[0])
        rel_path = os.path.abspath(".")
        rel_path = rel_path.replace("\\", "/")

        fname_no_ext = popup_summary['filename']

        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_2d_image, Disp_3D_image, module=self.module)

    def min_plate_height_calc(self):
        pass

    def max_plate_height_calc(self):
        pass


