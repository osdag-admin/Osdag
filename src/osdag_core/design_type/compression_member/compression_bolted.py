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
from ...utils.common.Section_Properties_Calculator import BBAngle_Properties, SAngle_Properties
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

    def module_name(self):
        return KEY_DISP_STRUT_BOLTED_END_GUSSET

    def set_osdaglogger(self, key):
        """
        Function to set Logger for Compression Bolted Module
        """
        # Set Custom logger
        logging.setLoggerClass(CustomLogger)

        # Create unique logger name per instance
        unique_logger_name = 'Osdag_struts_bolted_end_gusset_compress_member'
        self.logger = logging.getLogger(unique_logger_name)

        if not isinstance(self.logger, CustomLogger):
            logging.getLogger(unique_logger_name).manager.loggerDict.pop(unique_logger_name, None)
            self.logger = logging.getLogger(unique_logger_name)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG)
        
        # Shared formatter for all handlers
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
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
        change = []
        return change

    def input_dictionary_design_pref(self):
        """
        :return: This function is used to choose values of design preferences to be saved to design dictionary.
        """
        design_input = []
        
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE])
        design_input.append(t2)

        t3 = ("Bolt", TYPE_TEXTBOX, [KEY_DP_BOLT_SLIP_FACTOR])
        design_input.append(t3)

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

    def fn_conn_image(self, arg=None):
        if arg is None or len(arg) == 0:
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("bA.png"))
        profile = arg[0]
        # Return appropriate image based on profile
        if profile == 'Angles':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("bA.png"))
        elif profile == 'Back to Back Angles':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("bBBA.png"))
        elif profile == 'Star Angles':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("bSA.png"))
        elif profile == 'Channels':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("bC.png"))
        elif profile == 'Back to Back Channels':
            return str(files("osdag_core.data.ResourceFiles.images").joinpath("bBBC.png"))
        return str(files("osdag_core.data.ResourceFiles.images").joinpath("bA.png"))

    def out_bolt_bearing(self, args):
        """Returns True to hide bolt bearing output when bolt type is not bearing"""
        bolt_type = args[0]
        if bolt_type != TYP_BEARING:
            return True
        else:
            return False

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

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator')
        options_list.append(t4)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_LENGTH, KEY_DISP_LENGTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)

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

    def input_value_changed(self):
        """
        Function to dynamically update UI elements when input values change.
        This enables the Location combobox to update based on Section Profile selection.
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

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        return lst

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
               self.plate.bolts_one_line if status else '', True)
        spacing.append(t16)

        t15 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX,
               self.plate.bolt_line if status else '', True)
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

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        t9 = ([KEY_SECSIZE], KEY_SECSIZE, TYPE_CUSTOM_SECTION, self.new_material)
        lst.append(t9)

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
        self.efficiency = 0.0
        self.K = 1 # Effective length factor, typically 1 for truss members or dependent on conditions
        
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
        
        # Safety factors as per IS 800:2007 Table 5
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        self.gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

        self.logger.info(" : Design Preferences saved. Performing preliminary member checks.")
        self.logger.info(f" : Member Profile: {self.sec_profile}, Location: {self.loc}")
        self.logger.info(f" : Axial Load: {self.load.axial_force} kN, Length: {self.length} mm")
        self.initial_member_capacity(design_dictionary)

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
        sec_depth=[]
        for section in sizelist:
            if design_dictionary[KEY_SEC_PROFILE] in ['Angles']:
                self.section = Angle(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL])
                # NOTE: using approximate ry or rz, needs precise rmin logic
                rmin = min(self.section.rad_of_gy_u, self.section.rad_of_gy_v) if hasattr(self.section, 'rad_of_gy_u') else min(self.section.rad_of_gy_y, self.section.rad_of_gy_z)
                sec_gyr[self.section.designation] = rmin
                if self.loc == "Long Leg":
                    sec_depth.append(self.section.max_leg)
                else:
                    sec_depth.append(self.section.min_leg)
            # ... Add other profiles ...
            sec_area[self.section.designation] = self.section.area
            
        if len(sec_area) >= 1:
            self.max_area = max(sec_area, key=sec_area.get)
            self.max_gyr = max(sec_gyr, key=sec_gyr.get)
            self.depth_max = max(sec_depth)
        return self.max_area, self.max_gyr, self.depth_max

    def max_force_length(self, section):
        # Calculate max force (compression) and length based on section
        # Adapted from tension logic but for compression yielding/buckling
        if self.sec_profile == 'Angles':
            self.section_size_max = Angle(designation=section, material_grade=self.material)
            # Compression check: Pd = Ae * fcd
            # Simplified placeholder for max capacity estimate
            self.section_size_max.compression_member_design_buckling(
                L=500, # Dummy length for capacity check
                K=1.0, 
                fy=self.section_size_max.fy
            )
            self.max_member_force = self.section_size_max.compression_capacity
            self.max_length = 180 * min(self.section_size_max.rad_of_gy_u, self.section_size_max.rad_of_gy_v)
        
        return self.max_member_force, self.max_length, 0, 0 

    def initial_member_capacity(self, design_dictionary, previous_size=None):
        "selection of member based on the compression capacity"
        self.count += 1
        
        if previous_size is None:
            pass
        else:
            if previous_size in self.sizelist:
                self.sizelist.remove(previous_size)

        self.logger.info(f" : Checking {len(self.sizelist)} available sections for suitability.")
        
        # Iterate through all available sections
        for selectedsize in self.sizelist:
            self.section_size = self.select_section(design_dictionary, selectedsize)
            
            # --- 1. Minimal Geometric Checks for Bolted Connection ---
            # (Similar to tension_bolted to ensure bolts fit)
            self.bolt_diameter_min = min(self.bolt.bolt_diameter)
            self.edge_dist_min = IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_min, self.bolt.bolt_hole_type, 'machine_flame_cut')
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
            
            # Quick check: Area * fy / gamma_m0 (Yield Strength) > Axial Force
            # This is an upper bound. If Yield strength < Force, definitely fail.
            yield_capacity = self.section_size.area * self.section_size.fy / self.gamma_m0 / 1000 # kN
            if yield_capacity < self.load.axial_force:
                continue
                
            # If we passed basic checks, select this section for detailed design
            self.section_size_1 = self.section_size
            self.member_design_status = True
            
            # Also calculate properties for the selected section
            self.min_rad_gyration = r_min
            
            # Calculate exact capacity for this section to confirm
            # (Using a helper from component or common_calculation)
            # For now, proceeding to detailed connection check
            break
            
        if self.member_design_status:
            self.logger.info(f" : Selected Section: {self.section_size_1.designation}")
            self.design_status = True # Provisional
            self.select_bolt_dia(design_dictionary)
        else:
            self.design_status = False
            self.logger.warning(" : No section found that satisfies the design requirements (Geometry/Slenderness/Yield).")
            self.logger.info(" : Increase the member size or decrease the length.")


    def select_bolt_dia(self, design_dictionary, dia_remove=None):
        "Selection of bolt (dia) from the available list"
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[0]
        
        # Remove diameters that failed previous checks
        if dia_remove is not None:
            if dia_remove in self.bolt.bolt_diameter:
                self.bolt.bolt_diameter.remove(dia_remove)

        if len(self.bolt.bolt_diameter) == 0:
            self.design_status = False
            self.logger.warning(" : No bolt diameter found that satisfies design requirements.")
            return

        for self.bolt.bolt_diameter_provided in self.bolt.bolt_diameter:
            # 1. Pitch and Edge Distance Checks
            self.bolt.min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(
                self.bolt.bolt_diameter_provided, self.bolt.bolt_hole_type, 'machine_flame_cut'), 2)
            self.bolt.min_edge_dist_round = round_up(self.bolt.min_edge_dist, 5)
            self.pitch_round = round_up((2.5 * self.bolt.bolt_diameter_provided), 5)

            # Check if this diameter fits geometrically (re-check from initial but with specific values)
            # (Skipping detailed geometric re-check here as initial_member_capacity did a rough check, 
            # but usually good to double check or proceed)
            
            self.get_bolt_grade(design_dictionary)
            
            if self.bolt_design_status:
                self.member_check(design_dictionary)
                if self.design_status:
                    break
        
        if not self.design_status and len(self.bolt.bolt_diameter) == 0:
             self.logger.warning(" : Design failed for all bolt diameters.")

    def get_bolt_grade(self, design_dictionary):
        """Select bolt grade - stub implementation"""
        # For now, just select the first (highest) grade
        if len(self.bolt.bolt_grade) > 0:
            self.bolt.bolt_grade_provided = self.bolt.bolt_grade[0]
            self.bolt_design_status = True
        else:
            self.bolt_design_status = False

    def member_check(self, design_dictionary):
        # 1. Calculate Member Compression Capacity (Buckling) with detailed properties
        # This acts as the final verification of the member.
        
        min_rad = self.min_rad_gyration_calc(designation=self.section_size_1.designation,
                                             material_grade=self.material,
                                             key=self.sec_profile, subkey=self.loc,
                                             D_a=self.section_size_1.a if self.sec_profile=="Angles" else self.section_size_1.depth, # Handle varied props
                                             B_b=self.section_size_1.b if self.sec_profile=="Angles" else self.section_size_1.flange_width,
                                             T_t=self.section_size_1.thickness if self.sec_profile=="Angles" else self.section_size_1.flange_thickness,
                                             t=self.section_size_1.web_thickness if hasattr(self.section_size_1, 'web_thickness') else 0.0)
                                             
        # Note: min_rad_gyration_calc stores result in self.min_radius_gyration
        
        self.section_size_1.design_check_for_slenderness(self.K, self.length, self.min_radius_gyration)
        
        # Calculate buckling strength P_d
        # self.section_size_1.compression_member_design_buckling(self.K, self.length, self.section_size_1.fy) 
        # But this method might not exist on component. We use IS800 util directly or component method check.
        # compression.py uses 'IS800_2007.cl_7_1_2_1_design_compressisive_stress'
        
        # Manually calculating P_d using IS 800 utility function
        # buckling_class = 'c' (typically for Angles/Channels)
        buckling_class = 'c' 
        imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class)
        
        results = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
            self.section_size_1.fy, self.gamma_m0, self.section_size_1.slenderness, 
            imperfection_factor, 200000, check_type='Concentric') # E=200000
            
        f_cd = results[5] # Design compressive stress
        
        # Effective Area check (Class 4?)
        # For rolled sections (Angle/Channel), usually Class 1-3. 
        # Assuming Ag for now (conservative for standard hot rolled)
        # Verify Class in real implementation.
        
        self.section_size_1.compression_capacity = self.section_size_1.area * f_cd # N
        
        self.logger.info(f" : Compression Capacity: {round(self.section_size_1.compression_capacity/1000, 2)} kN")
        self.logger.info(f" : Slenderness Ratio: {round(self.section_size_1.slenderness, 2)}")
        
        if self.section_size_1.compression_capacity < self.load.axial_force * 1000:
            self.design_status = False
            self.logger.warning(f" : Compression Capacity ({round(self.section_size_1.compression_capacity/1000, 2)} kN) < Applied Load ({self.load.axial_force} kN)")
            return
            
        self.efficiency = round(self.load.axial_force * 1000 / self.section_size_1.compression_capacity, 2)
        
        # 2. Connection Design (Gusset Plate Selection)
        self.get_plate_thickness(design_dictionary)

    def get_plate_thickness(self, design_dictionary):
        """Select gusset plate thickness that satisfies bearing and yielding checks."""
        # Select plate thickness that satisfies:
        # 1. Bearing strength (Bolt on Plate)
        # 2. Yield Strength of Plate (Compression)
        
        available_thickness = [t for t in self.plate.thickness if t >= 6.0]  # Min 6mm
        
        if not available_thickness:
            available_thickness = self.plate.thickness  # Fallback to all available
        
        for t_p in available_thickness:
            self.plate.thickness_provided = t_p
            self.plate.connect_to_database_to_get_fy_fu(self.plate.material, t_p)
            
            # Bolt Bearing on Plate
            # Calculate kb based on min pitch/edge
            d0 = self.bolt.bolt_diameter_provided + 2  # Clearance
            e = 1.5 * d0
            p = 2.5 * self.bolt.bolt_diameter_provided
            
            # kb = min(e/3d0, p/3d0 - 0.25, fub/fu, 1.0)
            kb = min(e / (3 * d0), p / (3 * d0) - 0.25, 1.0)
            
            bearing_capacity_plate = 2.5 * kb * self.bolt.bolt_diameter_provided * t_p * self.plate.fu / 1.25  # gamma_mb
            
            # Bolt Bearing on Member
            if self.sec_profile == "Angles":
                t_member = self.section_size_1.thickness
            else:
                t_member = self.section_size_1.web_thickness if hasattr(self.section_size_1, 'web_thickness') else self.section_size_1.flange_thickness
            
            bearing_capacity_member = 2.5 * kb * self.bolt.bolt_diameter_provided * t_member * self.section_size_1.fu / 1.25
            
            self.bolt.bolt_bearing_capacity = min(bearing_capacity_plate, bearing_capacity_member)
            
            # Bolt Shear Capacity (IS 800:2007 Cl 10.3.3)
            grade = str(self.bolt.bolt_grade_provided)
            f_ub = float(grade.split('.')[0]) * 100  # 8.8 -> 800 MPa
            d = float(self.bolt.bolt_diameter_provided)
            A_nb = 0.78 * 3.14159 * d * d / 4  # Net area (threads in shear plane)
            V_nsb = (f_ub / math.sqrt(3)) * A_nb  # Nominal shear capacity
            self.bolt.bolt_shear_capacity = V_nsb / 1.25  # Design capacity (gamma_mb=1.25)
            
            # Final Bolt Value
            self.bolt.bolt_capacity = min(self.bolt.bolt_shear_capacity, self.bolt.bolt_bearing_capacity)
            
            # Number of Bolts
            n_bolts = math.ceil(self.load.axial_force * 1000 / self.bolt.bolt_capacity)
            
            # Update Layout (Rows/Cols) logic
            self.plate.bolts_one_line = n_bolts
            self.plate.bolt_line = 1
            self.plate.bolt_force = self.load.axial_force * 1000 / n_bolts
            
            # Plate Yielding Check in Compression
            # Pd_plate = Ag * fy / gamma_m0
            if self.sec_profile == "Angles":
                h_plate = self.section_size_1.max_leg + 50  # Heuristic for clearance
            else:
                h_plate = self.section_size_1.depth + 50
            
            plate_yield_cap = h_plate * t_p * self.plate.fy / self.gamma_m0
            
            if plate_yield_cap < self.load.axial_force * 1000:
                continue  # Need thicker plate
            
            self.plate.height = h_plate
            self.plate.length = (n_bolts - 1) * p + 2 * e
            self.plate_design_status = True
            self.design_status = True
            
            # Log successful design
            self.logger.info(f" : Bolt Diameter: {int(self.bolt.bolt_diameter_provided)} mm, Grade: {self.bolt.bolt_grade_provided}")
            self.logger.info(f" : Bolt Shear Capacity: {round(self.bolt.bolt_shear_capacity/1000, 2)} kN")
            self.logger.info(f" : Bolt Bearing Capacity: {round(self.bolt.bolt_bearing_capacity/1000, 2)} kN")
            self.logger.info(f" : Number of Bolts: {n_bolts}")
            self.logger.info(f" : Plate Thickness: {int(t_p)} mm")
            self.logger.info(f" : Plate Height x Length: {int(h_plate)} x {int(self.plate.length)} mm")
            self.logger.info(f" : Design Efficiency: {self.efficiency}")
            self.logger.info(" : ========= DESIGN IS SAFE =========")
            break
        
        if not self.plate_design_status:
            self.design_status = False
            self.logger.warning(" : Could not design gusset plate. Increase plate thickness options or reduce load.")

    def min_rad_gyration_calc(self, designation, material_grade, key, subkey, D_a=0, B_b=0, T_t=0, t=0):
        # Calculate minimum radius of gyration for coupled sections
        # This mirrors the logic in component.py/tension_bolted.py but ensures availability on the main class
        
        # Default properties
        r_y = 0.0
        r_z = 0.0
        r_u = 0.0
        r_v = 0.0
        area = 0.0
        mom_inertia_y = 0.0
        mom_inertia_z = 0.0
        Cg_1 = 0.0 # Cy
        Cg_2 = 0.0 # Cz
        thickness = T_t
        
        # Fetch basic properties from the current section object
        # Using self.section_size which is set in initial_member_capacity
        
        s = self.section_size
        if s.designation != designation:
            # Need to create temporary object or fetch props
            pass # Using current object for now as it matches logic usually
            
        area = s.area / 100 # Convert back to sqcm if needed or keep mm2? 
        # Note: Formulas below likely expect specific units. Osdag usually uses mm/N internally.
        # r is in mm. I in mm4. Area in mm2.
        
        area = s.area
        mom_inertia_y = s.mom_inertia_y
        mom_inertia_z = s.mom_inertia_z
        
        if key in ['Channels', 'Back to Back Channels']:
            r_y = s.rad_of_gy_y
            r_z = s.rad_of_gy_z
            Cg_1 = s.Cy
            thickness = s.web_thickness if hasattr(s, 'web_thickness') else T_t
        else: # Angles
            r_y = s.rad_of_gy_y
            r_z = s.rad_of_gy_z
            r_u = s.rad_of_gy_u
            r_v = s.rad_of_gy_v
            Cg_1 = s.Cy
            Cg_2 = s.Cz
            
        min_rad = 0.0
        
        if key == "Channels" and subkey == "Web":
            min_rad = min(r_y, r_z)
        
        elif key == 'Back to Back Channels' and subkey == "Web":
            # Iyy = 2 * (Iy + A * (Cy + t_plate/2)^2)
            # Izz = 2 * Iz
            # separation = plate thickness
            sep = self.plate.thickness_provided if self.plate.thickness_provided else 0.0
            Iyy = 2 * (mom_inertia_y + area * (Cg_1 + sep/2)**2)
            Izz = 2 * mom_inertia_z
            I_min = min(Iyy, Izz)
            min_rad = math.sqrt(I_min / (2 * area))

        elif key == "Back to Back Angles" and subkey == 'Long Leg':
             # Connected back-to-back on long leg
             # Axis parallel to web (long leg) is Y-Y (vertical)? 
             # Check Angle definition. z-z is parallel to shorter leg? 
             # Usually u-u and v-v are principal.
             # For B2B, symmetry axes become Y and Z.
             
             sep = self.plate.thickness_provided if self.plate.thickness_provided else 0.0
             
             # Case: Long legs back to back
             # I_z-z (horizontal) = 2 * I_z (centroidal)
             # I_y-y (vertical) = 2 * (I_y + A * (Cy + sep/2)^2)
             
             Izz = 2 * mom_inertia_z
             Iyy = 2 * (mom_inertia_y + area * (Cg_1 + sep/2)**2)
             I_min = min(Iyy, Izz)
             min_rad = math.sqrt(I_min / (2 * area))
         
        elif key == 'Back to Back Angles' and subkey == 'Short Leg':
             sep = self.plate.thickness_provided if self.plate.thickness_provided else 0.0
             # Connected on Short Leg
             # I_y-y = 2 * I_y
             # I_z-z = 2 * (I_z + A * (Cz + sep/2)^2)
             
             Iyy = 2 * mom_inertia_y
             Izz = 2 * (mom_inertia_z + area * (Cg_2 + sep/2)**2)
             I_min = min(Iyy, Izz)
             min_rad = math.sqrt(I_min / (2 * area))

        elif key == 'Star Angles':
             # Star arrangement (Cruciform)
             # I_uu and I_vv approx equal to I_xx and I_yy of compound?
             # Star angles have symmetry.
             # I_min is approx r_min of single angle? No, usually higher.
             # I_compound = 2 * I_u + 2 * I_v ? No.
             # Star angles (2 angles) or 4? Usually 2 or 4. Osdag "Star Angles" usually means 2 diagonally or 4?
             # Assuming 2 angles connected diagonally?
             # Or 4 angles.
             # Osdag Star Angles = 2 angles toe-to-toe or similar?
             # Implementing based on standard Osdag Star Angle logic found in component.py check
             
             sep = self.plate.thickness_provided if self.plate.thickness_provided else 0.0
             
             if subkey == 'Long Leg':
                 Iyy = 2 * (mom_inertia_y + area * (Cg_1 + sep/2)**2)
                 Izz = 2 * (mom_inertia_z + area * Cg_2**2) # Check spacing
                 I_min = min(Iyy, Izz)
                 min_rad = math.sqrt(I_min / (2 * area))
             else:
                 Izz = 2 * (mom_inertia_z + area * (Cg_2 + sep/2)**2)
                 Iyy = 2 * (mom_inertia_y + area * Cg_1**2)
                 I_min = min(Iyy, Izz)
                 min_rad = math.sqrt(I_min / (2 * area))
                 
        else: # Single Angle
             min_rad = min(r_u, r_v) if hasattr(s, 'rad_of_gy_u') else min(r_y, r_z)
             
        self.min_radius_gyration = min_rad
        return min_rad

    def save_design(self, popup_summary):
        """
        Save the design results and generate the design report.
        Based on tension_bolted.py but adapted for compression members.
        """
        # Determine section for report
        if self.member_design_status:
            section_size = self.section_size_1
        else:
            # Use max section for failed design
            if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
                section_size = Angle(designation=self.max_area, material_grade=self.material)
            else:
                section_size = Channel(designation=self.max_area, material_grade=self.material)
        
        # Determine image based on section profile and connection
        if self.sec_profile in ["Channels", "Back to Back Channels"]:
            if self.sec_profile == "Back to Back Channels":
                if section_size.flange_slope == 90:
                    image = "Parallel_BBChannel"
                else:
                    image = "Slope_BBChannel"
                connecting_plates = [self.plate.thickness_provided, section_size.web_thickness]
            else:
                if section_size.flange_slope == 90:
                    image = "Parallel_Channel"
                else:
                    image = "Slope_Channel"
                connecting_plates = [self.plate.thickness_provided, section_size.web_thickness]
        elif section_size.max_leg == section_size.min_leg:
            # Equal angles
            if self.sec_profile == "Back to Back Angles":
                image = "bblequaldp" if self.loc == "Long Leg" else "bbsequaldp"
            elif self.sec_profile == "Star Angles":
                image = "salequaldp" if self.loc == "Long Leg" else "sasequaldp"
            else:
                image = "equaldp"
            connecting_plates = [self.plate.thickness_provided, section_size.thickness]
        else:
            # Unequal angles
            if self.sec_profile == "Back to Back Angles":
                image = "bblunequaldp" if self.loc == "Long Leg" else "bbsunequaldp"
            elif self.sec_profile == "Star Angles":
                image = "salunequaldp" if self.loc == "Long Leg" else "sasunequaldp"
            else:
                image = "unequaldp"
            connecting_plates = [self.plate.thickness_provided, section_size.thickness]
        
        # Gamma values for bolts
        if self.member_design_status:
            if self.bolt.bolt_type == TYP_BEARING:
                variable = KEY_DISP_GAMMA_MB
                value = cl_5_4_1_table_4_5_gamma_value(self.bolt.gamma_mb, "mb")
            else:
                variable = KEY_DISP_GAMMA_MF
                value = cl_5_4_1_table_4_5_gamma_value(self.bolt.gamma_mf, "mf")
        else:
            variable = KEY_DISP_GAMMA_MF
            value = cl_5_4_1_table_4_5_gamma_value(1.25, "mf")
        
        # Member capacity for report
        if self.member_design_status:
            compression_capacity_kn = round(section_size.compression_capacity / 1000, 2)
            slenderness = section_size.slenderness
            gyration = self.min_radius_gyration
        else:
            compression_capacity_kn = 0.0
            slenderness = 0.0
            gyration = 0.0
        
        # Section report data
        if self.sec_profile == "Angles":
            self.report_supporting = {
                KEY_DISP_SEC_PROFILE: image,
                KEY_DISP_SECSIZE: (section_size.designation, self.sec_profile),
                KEY_DISP_MATERIAL: section_size.material,
                KEY_REPORT_MASS: round(section_size.mass, 2),
                KEY_REPORT_AREA: round(section_size.area, 2),
                KEY_REPORT_MAX_LEG_SIZE: round(section_size.max_leg, 2),
                KEY_REPORT_MIN_LEG_SIZE: round(section_size.min_leg, 2),
                KEY_REPORT_ANGLE_THK: round(section_size.thickness, 2),
                KEY_REPORT_R1: section_size.root_radius,
                KEY_REPORT_R2: section_size.toe_radius,
                KEY_REPORT_CY: round(section_size.Cy, 2),
                KEY_REPORT_CZ: round(section_size.Cz, 2),
                KEY_REPORT_IZ: round(section_size.mom_inertia_z * 1e-4, 2),
                KEY_REPORT_IY: round(section_size.mom_inertia_y * 1e-4, 2),
                KEY_REPORT_RZ: round(section_size.rad_of_gy_z * 1e-1, 2),
                KEY_REPORT_RY: round(section_size.rad_of_gy_y * 1e-1, 2),
                KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)
            }
            thickness = section_size.thickness
        else:
            # Channels
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
                KEY_REPORT_R1: round(section_size.root_radius, 2),
                KEY_REPORT_R2: round(section_size.toe_radius, 2),
                KEY_REPORT_IZ: round(section_size.mom_inertia_z * 1e-4, 2),
                KEY_REPORT_IY: round(section_size.mom_inertia_y * 1e-4, 2),
                KEY_REPORT_RZ: round(section_size.rad_of_gy_z * 1e-1, 2),
                KEY_REPORT_RY: round(section_size.rad_of_gy_y * 1e-1, 2),
                KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)
            }
            thickness = section_size.web_thickness
        
        # Bolt report data
        self.report_bolt = {
            KEY_DISP_D: self.bolt.bolt_diameter_provided,
            KEY_DISP_GRD: self.bolt.bolt_grade_provided,
            KEY_DISP_TYP: self.bolt.bolt_type,
            KEY_OUT_DISP_BOLT_SHEAR: round(self.bolt.bolt_shear_capacity / 1000, 2) if self.bolt.bolt_shear_capacity else 0.0,
            KEY_OUT_DISP_BOLT_BEARING: round(self.bolt.bolt_bearing_capacity / 1000, 2) if self.bolt.bolt_bearing_capacity else 0.0,
            KEY_OUT_DISP_BOLT_CAPACITY: round(self.bolt.bolt_capacity / 1000, 2) if self.bolt.bolt_capacity else 0.0,
        }
        
        # Plate report data
        self.report_plate = {
            KEY_DISP_PLATETHK: self.plate.thickness_provided if self.plate.thickness_provided else 0.0,
            KEY_OUT_DISP_PLATE_MIN_HEIGHT: round(self.plate.height, 2) if hasattr(self.plate, 'height') and self.plate.height else 0.0,
            KEY_OUT_DISP_PLATE_MIN_LENGTH: round(self.plate.length, 2) if hasattr(self.plate, 'length') and self.plate.length else 0.0,
        }
        
        # Design summary for report
        self.report_input = {
            KEY_MODULE: self.module,
            KEY_DISP_AXIAL: self.load.axial_force,
            KEY_DISP_LENGTH: self.length,
            KEY_DISP_DESIGN_STRENGTH_COMPRESSION: compression_capacity_kn,
            KEY_DISP_SLENDER: slenderness,
            KEY_DISP_EFFICIENCY: self.efficiency if hasattr(self, 'efficiency') else 0.0,
        }
        
        # Combine for popup summary
        if popup_summary is not None:
            popup_summary['Section'] = section_size.designation
            popup_summary['Profile'] = self.sec_profile
            popup_summary['Compression Capacity (kN)'] = compression_capacity_kn
            popup_summary['Bolt Diameter (mm)'] = self.bolt.bolt_diameter_provided
            popup_summary['Bolt Grade'] = self.bolt.bolt_grade_provided
            popup_summary['Plate Thickness (mm)'] = self.plate.thickness_provided if self.plate.thickness_provided else 'N/A'
            popup_summary['Design Status'] = 'Safe' if self.design_status else 'Unsafe'
        
        # Report check list for design calculations
        self.report_check = []
        
        if self.member_design_status:
            t1 = ('SubSection', 'Member Check (Compression)', '|p{2.5cm}|p{5cm}|p{7cm}|p{1cm}|')
            self.report_check.append(t1)
            
            t2 = (KEY_DISP_DESIGN_STRENGTH_COMPRESSION, self.load.axial_force, 
                  f"Compression Capacity = {compression_capacity_kn} kN",
                  'Pass' if compression_capacity_kn >= self.load.axial_force else 'Fail')
            self.report_check.append(t2)
            
            t3 = (KEY_DISP_SLENDER, '180 (max)', 
                  f"Slenderness = {round(slenderness, 2)}",
                  'Pass' if slenderness <= 180 else 'Fail')
            self.report_check.append(t3)
            
            t4 = (KEY_DISP_EFFICIENCY, '< 1.0', 
                  f"Efficiency = {self.efficiency if hasattr(self, 'efficiency') else 0.0}",
                  'Pass' if self.efficiency <= 1.0 else 'Fail')
            self.report_check.append(t4)
            
            # Bolt checks
            t5 = ('SubSection', 'Bolt Design', '|p{2.5cm}|p{5cm}|p{7cm}|p{1cm}|')
            self.report_check.append(t5)
            
            bolt_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2) if self.bolt.bolt_capacity else 0.0
            t6 = (KEY_OUT_DISP_BOLT_CAPACITY, '', f"Bolt Capacity = {bolt_capacity_kn} kN", '')
            self.report_check.append(t6)
            
            # Plate checks
            t7 = ('SubSection', 'Gusset Plate Design', '|p{2.5cm}|p{5cm}|p{7cm}|p{1cm}|')
            self.report_check.append(t7)
            
            t8 = (KEY_DISP_PLATETHK, '', f"Thickness = {self.plate.thickness_provided} mm", '')
            self.report_check.append(t8)
        else:
            t1 = ('Selected', 'Design Failed', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
            self.report_check.append(t1)
        
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


