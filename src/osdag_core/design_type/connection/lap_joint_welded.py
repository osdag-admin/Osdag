"""
Module: lap_joint_welded.py
Author: Aman, Nishi Kant Mandal, Tanu Singh, Roushan Raj
Date: 2025-07-14

Description:
    LapJointWelded is a moment connection module that represents a welded lap joint connection.
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
from ...custom_logger import CustomLogger
import logging

import math

import os
from pylatex.utils import NoEscape
from pylatex import Math

class LapJointWelded(MomentConnection):
    def __init__(self):
        super(LapJointWelded, self).__init__()
        self.design_status = False
        self.weld_size = None
        self.weld_length_provided = None
        self.weld_strength = None
        self.weld_thickness = None
        self.plate_width = None
        self.plate_length = None
        self.plate_thickness = None
        self.weld_type = None
        self.weld_material = None
        self.weld_fabrication = None
        self.weld_angle = None
        self.weld_length_effective = None
        self.hover_dict = {}

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []
        tabs.append((("Weld", TYPE_TAB_2, self.weld_values)))
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
        tabs.append(("Design", TYPE_TAB_2, self.design_values))  # Add design tab
        return tabs

    def tab_value_changed(self):
        return []

    def edit_tabs(self):
        return []

    def input_dictionary_design_pref(self):
        design_input = []
        design_input.append(("Weld", TYPE_COMBOBOX, [
            KEY_DP_WELD_TYPE,
            KEY_DP_WELD_MATERIAL_G_O
        ]))
        design_input.append(("Detailing", TYPE_COMBOBOX, [
            KEY_DP_DETAILING_EDGE_TYPE,
        ]))
        design_input.append(("Design", TYPE_COMBOBOX, [KEY_DESIGN_FOR]))  # Add design preference
        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        design_input.append((None, [
            KEY_DP_WELD_TYPE,
            KEY_DP_WELD_MATERIAL_G_O,
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DESIGN_FOR  # Add design preference
        ], ''))
        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):
        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            fu = Material(design_dictionary[KEY_MATERIAL], 41).fu
        else:
            fu = ''

        defaults = {
            KEY_DP_WELD_TYPE: "Shop weld",
            KEY_DP_WELD_MATERIAL_G_O: str(fu),
            KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
        }
        return defaults.get(key)
    
    def design_values(self, input_dictionary):
        """Content of the 'Design' tab in Design Preferences."""
        values = {
                KEY_DESIGN_FOR: 'Tension',
        }
        if input_dictionary and KEY_DESIGN_FOR in input_dictionary:
                values[KEY_DESIGN_FOR] = input_dictionary[KEY_DESIGN_FOR]

        design_tab_content = []
        t1 = (KEY_DESIGN_FOR, KEY_DISP_DESIGN_FOR, TYPE_COMBOBOX,
             ['Tension', 'Compression'], values[KEY_DESIGN_FOR])
        design_tab_content.append(t1)
        return design_tab_content

    def detailing_values(self, input_dictionary):
        values = {
            KEY_DP_DETAILING_EDGE_TYPE: 'Sheared or hand flame cut',
        }

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        detailing = []

        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX,
            ['Sheared or hand flame cut', 'Rolled, machine-flame cut, sawn and planed'],
            values[KEY_DP_DETAILING_EDGE_TYPE])
        detailing.append(t1)

        t4 = ("textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION_LAPJOINT, None)
        detailing.append(t4)

        return detailing

    def weld_values(self, input_dictionary):
        fu = ''
        if input_dictionary and KEY_MATERIAL in input_dictionary:
            if input_dictionary[KEY_MATERIAL] != 'Select Material':
                fu = Material(input_dictionary[KEY_MATERIAL], 41).fu

        values = {
            KEY_DP_WELD_TYPE: 'Shop weld',
            KEY_DP_WELD_MATERIAL_G_O: str(fu) if fu else '410',
        }

        for key in values.keys():
            if input_dictionary and key in input_dictionary:
                values[key] = input_dictionary[key]

        weld = []

        t3 = (KEY_DP_WELD_TYPE, "Type", TYPE_COMBOBOX,
            ['Shop weld', 'Field weld'],
            values[KEY_DP_WELD_TYPE])
        weld.append(t3)

        t2 = (KEY_DP_WELD_MATERIAL_G_O, "Material Grade Overwrite, Fu (MPa)", TYPE_TEXTBOX,
            None,
            values[KEY_DP_WELD_MATERIAL_G_O])
        weld.append(t2)
        return weld

    def set_osdaglogger(self, key, id):
        """
        Function to set Logger for FinPlate Module
        """
        # @author Arsil Zunzunia

        # Set Custom logger
        logging.setLoggerClass(CustomLogger)

        # Create unique logger name per instance
        unique_logger_name = 'Osdag_lap_joint_welded_simple_conn'
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

    def input_value_changed(self):
        lst = []
        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)
        return lst

    def input_values(self):
        options_list = []
        t16 = (KEY_MODULE, KEY_DISP_LAPJOINTWELDED, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)
        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)
        t31 = (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t31)
        t34 = (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t34)
        t35 = (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None, True, 'Float Validator')
        options_list.append(t35)
        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)
        t18 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t18)
        t20 = (KEY_WELD_SIZE, KEY_DISP_WELD_SIZE, TYPE_COMBOBOX_CUSTOMIZED, VALUES_ALL_CUSTOMIZED, True, 'No Validator')
        options_list.append(t20)
        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)
        # Replace tensile force with axial force
        t17 = (KEY_AXIAL_FORCE, KEY_DISP_AXIAL_FORCE, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)
        return options_list

    def customized_input(self):
        list1 = []
        t11 = (KEY_WELD_SIZE, self.weld_size_customized)
        list1.append(t11)
        return list1

    @staticmethod
    def weld_size_customized():
        return [str(size) for size in WELD_SIZES]

    def output_values(self, flag):
        out_list = []
        t21 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t21)
        t22 = (KEY_OUT_UTILISATION_RATIO, KEY_OUT_DISP_UTILISATION_RATIO, TYPE_TEXTBOX,
               round(self.utilization_ratio, 3) if flag and hasattr(self, 'utilization_ratio') and self.utilization_ratio is not None else '', True)
        out_list.append(t22)
        t23 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX,
               "Fillet" if flag else '', True)
        out_list.append(t23)
        t24 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX,
               round(self.weld_size, 1) if flag and self.weld_size is not None else '', True)
        out_list.append(t24)
        t25 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH_kN, TYPE_TEXTBOX,
               round(self.weld_strength / 1000, 2) if flag and hasattr(self, 'weld_strength') and self.weld_strength is not None else '', True)
        out_list.append(t25)
        t26 = (KEY_OUT_WELD_LENGTH_EFF, KEY_OUT_DISP_WELD_LENGTH_EFF, TYPE_TEXTBOX,
               round(self.weld_length_effective, 1) if flag and self.weld_length_effective is not None else '', True)
        out_list.append(t26)
        t27 = (KEY_OUT_WELD_CONN_LEN, KEY_OUT_DISP_WELD_CONN_LEN, TYPE_TEXTBOX,
               round(self.connection_length, 1) if flag and hasattr(self, 'connection_length') and self.connection_length is not None else '', True)
        out_list.append(t27)
        t29 = (KEY_OUT_DESIGN_FOR, KEY_OUT_DISP_DESIGN_FOR, TYPE_TEXTBOX,
               self.design_for if flag and hasattr(self, 'design_for') else '', True)
        out_list.append(t29)

        # Hover Dictionary
        plate_length = getattr(self, 'connection_length', 0)
        plate_width = float(self.width) if hasattr(self, 'width') else 0
        plate1_thk = float(self.plate1.thickness[0]) if hasattr(self, 'plate1') and self.plate1 and self.plate1.thickness else 0
        plate2_thk = float(self.plate2.thickness[0]) if hasattr(self, 'plate2') and self.plate2 and self.plate2.thickness else 0
        
        # Store dimensions on plate objects
        if hasattr(self, 'plate1') and self.plate1:
            self.plate1.length = plate_length
            self.plate1.height = plate_width
            self.plate1.thickness_provided = plate1_thk
        if hasattr(self, 'plate2') and self.plate2:
            self.plate2.length = plate_length
            self.plate2.height = plate_width
            self.plate2.thickness_provided = plate2_thk

        self.hover_dict["Plate 1"] = (
            f"<b>Plate 1</b><br>"
            f"Width: {round(float(self.plate1.height), 2) if flag and self.plate1.height else ''} mm<br>"
            f"Thickness: {round(float(self.plate1.thickness_provided), 2) if flag and self.plate1.thickness_provided else ''} mm"
        )
        self.hover_dict["Plate 2"] = (
            f"<b>Plate 2</b><br>"
            f"Width: {round(float(self.plate2.height), 2) if flag and self.plate2.height else ''} mm<br>"
            f"Thickness: {round(float(self.plate2.thickness_provided), 2) if flag and self.plate2.thickness_provided else ''} mm"
        )
        self.hover_dict["Weld"] = (
            f"<b>Fillet Weld</b><br>"
            f"Size: {round(float(self.weld_size), 1) if flag and self.weld_size else ''} mm<br>"
            f"Type: {getattr(self.weld, 'type', 'Fillet') if flag else ''}<br>"
            f"Effective Length: {round(float(self.weld_length_effective), 1) if flag and self.weld_length_effective else ''} mm"
        )

        return out_list

    @staticmethod
    def module_name():
        return KEY_DISP_LAPJOINTWELDED

    def func_for_validation(self, design_dictionary):
        all_errors = []
        self.design_status = False
        flag = False
        flag1 = False
        flag2 = False

        option_list = self.input_values()
        missing_fields_list = []

        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
                else:
                    if option[0] == KEY_PLATE_WIDTH:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True
                    # Change from KEY_TENSILE_FORCE to KEY_AXIAL_FORCE
                    elif option[0] == KEY_AXIAL_FORCE:
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

    def set_input_values(self, design_dictionary):
        design_dictionary_with_defaults = design_dictionary.copy()
        if KEY_SHEAR not in design_dictionary_with_defaults:
            design_dictionary_with_defaults[KEY_SHEAR] = 0.0
        if KEY_AXIAL not in design_dictionary_with_defaults:
            design_dictionary_with_defaults[KEY_AXIAL] = 0.0
        if KEY_MOMENT not in design_dictionary_with_defaults:
            design_dictionary_with_defaults[KEY_MOMENT] = 0.0

        super(LapJointWelded, self).set_input_values(design_dictionary_with_defaults)
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Lap Joint Welded Connection"
        self.main_material = design_dictionary[KEY_MATERIAL]
        
        # Design mode: default to Tension if not provided
        self.design_for = design_dictionary.get(KEY_DESIGN_FOR, 'Tension')
        
        # Use axial force instead of tensile force
        axial_kN_str = design_dictionary.get(KEY_AXIAL_FORCE, 
                 design_dictionary.get(KEY_AXIAL,
                 design_dictionary.get(KEY_TENSILE_FORCE, 0)))
                 
        self.axial_force = abs(float(axial_kN_str)) * 1000  # N, always positive magnitude
        # Maintain backward compatibility: many methods use tensile_force name
        self.tensile_force = self.axial_force
        
        self.width = float(design_dictionary[KEY_PLATE_WIDTH])
        self.plate1 = Plate(thickness=[design_dictionary[KEY_PLATE1_THICKNESS]],
                        material_grade=design_dictionary[KEY_MATERIAL],
                        width=design_dictionary[KEY_PLATE_WIDTH])
        self.plate2 = Plate(thickness=[design_dictionary[KEY_PLATE2_THICKNESS]],
                            material_grade=design_dictionary[KEY_MATERIAL],
                            width=design_dictionary[KEY_PLATE_WIDTH])
        self.weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                         type=design_dictionary[KEY_DP_WELD_TYPE],
                         fabrication=design_dictionary.get(KEY_DP_FAB_SHOP, KEY_DP_FAB_SHOP))
        self.weld.size = design_dictionary[KEY_WELD_SIZE]
        self.weld.size = design_dictionary[KEY_WELD_SIZE]
        self.design_of_weld(design_dictionary)

    def design_of_weld(self, design_dictionary):
        self.logger.info(": =========== Design of Lap Joint Welded Connection ==========")
        self.logger.info(": Design Approach: IS 800:2007 Clause 10.5")
        self.utilization_ratios = {}

        if not self.weld_size_check(design_dictionary):
            return

        self.calculate_weld_strength(design_dictionary)
        self.calculate_weld_length()
        self.check_long_joint()
        self.check_base_metal_strength(design_dictionary)
        self.calculate_final_utilization_ratio()

    def weld_size_check(self, design_dictionary):
        self.logger.info(": =============== Weld Size Check ===============")
        weld_size = design_dictionary[KEY_WELD_SIZE]
        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        Tmin = min(plate1_thk, plate2_thk)
        s_min = IS800_2007.cl_10_5_2_3_min_weld_size(plate1_thk, plate2_thk)
        s_max = Tmin - 1.5 if Tmin >= 10 else Tmin

        self.logger.info(f": Minimum weld size required (s_min) = {s_min} mm [Ref. Table 21, Cl.10.5.2.3]")
        self.logger.info(f": Maximum allowed weld size (s_max) = {s_max} mm [Ref. Cl.10.5.3.1]")

        selected_size = None
        if isinstance(weld_size, str) and weld_size.lower() == 'all':
            valid_sizes = [s for s in ALL_WELD_SIZES if s_min <= s <= s_max]
            if valid_sizes:
                selected_size = float(valid_sizes[0])
        else:
            try:
                size_val = float(weld_size[0] if isinstance(weld_size, list) else weld_size)
                if s_min <= size_val <= s_max:
                    selected_size = size_val
            except (ValueError, IndexError):
                pass

        if selected_size is None:
            self.logger.error(": Selected weld size is not suitable.")
            self.design_status = False
            return False

        self.weld_size = selected_size
        self.logger.info(f": Selected weld size = {self.weld_size} mm (Pass)")
        return True

    def calculate_weld_strength(self, design_dictionary):
        self.logger.info(": ============== Weld Strength Calculation ==============")
        # IS800:2007 Cl.10.5.3.2: Throat thickness a = K * s, where K depends on angle
        # For fillet welds, K = sin(θ), θ = weld angle (default 45° if not specified)
        weld_angle = design_dictionary.get('weld_angle', 45)
        # IS 800:2007 Cl.10.5.3.2 Table 22:
        # For Angle between fusion faces 60-90 degrees, K = 0.7.
        # Lap Joint fusion faces are at 90 degrees.
        # Previous code used sin(45) = 0.707 which caused discrepancy with standard report values (0.7).
        K = 0.7
        
        self.effective_throat_thickness = K * self.weld_size  # Cl.10.5.3.2
        self.logger.info(f": Effective throat thickness (a) = {self.effective_throat_thickness:.2f} mm [Cl.10.5.3.2, K={K}, Fusion Angle=90°]")
        
        self.fu_weld = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])
        self.fu_parent = min(self.plate1.fu, self.plate2.fu) # Use stronger/weaker? Strength governed by weaker parent.

        self.gamma_mw = 1.25 if design_dictionary.get(KEY_DP_WELD_TYPE, "Shop weld") == "Shop weld" else 1.50  # Cl.10.5.7.1
        
        # P_wd (Weld Metal Strength per unit length)
        self.weld_design_strength = (self.fu_weld * self.effective_throat_thickness) / (math.sqrt(3) * self.gamma_mw)  # Cl.10.5.7.1
        
        # P_md (Parent Metal Strength per unit length)
        self.parent_design_strength = 0.6 * self.fu_parent * self.effective_throat_thickness / self.gamma_mw  # Cl.10.5.7.2
        
        self.fillet_weld_design_strength = min(self.weld_design_strength, self.parent_design_strength)
        self.logger.info(f": Design strength of fillet weld = {self.fillet_weld_design_strength:.2f} N/mm [Cl.10.5.7]")


    def calculate_weld_length(self):
        self.logger.info(": ============== Weld Length Calculation ==============")
        # Required effective weld length (Cl.10.5.4.1)
        self.weld_length_required = self.tensile_force / (2 * self.fillet_weld_design_strength)
        self.leff_min = max(4 * self.weld_size, 40)  # Cl.10.5.4.1
        self.leff_max = 70 * self.weld_size  # Cl.10.5.4.1
        self.logger.info(f": Required effective weld length = {self.weld_length_required:.2f} mm")
        self.logger.info(f": Minimum effective weld length = {self.leff_min} mm [Cl.10.5.4.1]")
        self.logger.info(f": Maximum effective weld length = {self.leff_max} mm [Cl.10.5.4.1]")
        # Check min/max
        if self.weld_length_required < self.leff_min:
            self.l_eff = self.leff_min
            self.logger.warning(f": Required length is less than minimum, using l_eff = {self.l_eff} mm [Cl.10.5.4.1]")
        elif self.weld_length_required > self.leff_max:
            self.logger.error(": Required weld length exceeds maximum allowed. Increase weld size. [Cl.10.5.4.1]")
            self.design_status = False
            raise ValueError("Required weld length exceeds maximum allowed.")
        else:
            self.l_eff = self.weld_length_required
            self.logger.info(": Required weld length is within limits (Pass)")
        # Detailing: Minimum spacing between parallel fillet welds (Cl.10.5.4.2)
        # Not implemented here, but should be checked in GUI or input validation

    def check_long_joint(self):
        self.logger.info(": ============== Long Joint Check ==============")
        # IS800:2007 Cl.10.5.7.3: Long joint reduction factor
        self.beta_lw = 1.0
        if self.l_eff > 150 * self.effective_throat_thickness:
            self.beta_lw = 1.2 - 0.2 * (self.l_eff / (150 * self.effective_throat_thickness))
            self.beta_lw = max(0.6, min(self.beta_lw, 1.0))
            self.logger.info(f": Joint is long, reduction factor beta_lw = {self.beta_lw:.3f} [Cl.10.5.7.3]")
        else:
            self.logger.info(": No reduction for long joint required (Pass)")
        # Modified required length
        l_req_modified = self.l_eff / self.beta_lw
        if l_req_modified < self.leff_min:
            self.logger.warning(f": Modified required weld length {l_req_modified:.2f} mm is less than minimum effective length {self.leff_min} mm [Cl.10.5.4.1]")
            self.l_eff = self.leff_min
        elif l_req_modified > self.leff_max:
            self.logger.error(": Modified required weld length exceeds maximum allowed. Increase weld size. [Cl.10.5.4.1]")
            self.design_status = False
            raise ValueError("Modified required weld length exceeds maximum allowed.")
        else:
            self.l_eff = l_req_modified
        # End return length (Cl.10.5.4.5): min(2*s, 12mm)
        self.end_return_length = max(2 * self.weld_size, 12)  # Cl.10.5.4.5
        self.logger.info(f": End return length = {self.end_return_length} mm [Cl.10.5.4.5]")
        # Overlap length (Cl.10.5.4.3): min overlap = 4*s or 40mm, whichever is more
        min_overlap = max(4 * self.weld_size, 40)
        
        self.connection_length = self.l_eff + 2 * self.end_return_length
        
        # Overlap must accommodate connection length plus clearances (assuming 10mm each side)
        self.overlap_length = max(min_overlap, self.connection_length + 20) 
        
        self.logger.info(f": Overlap length = {self.overlap_length} mm [Cl.10.5.4.3]")

        # Design capacity (Cl.10.5.7.3):
        self.design_capacity = 2 * self.l_eff * self.fillet_weld_design_strength * self.beta_lw
        
        self.utilization_ratios['weld'] = self.tensile_force / self.design_capacity if self.design_capacity > 0 else float('inf')
        self.logger.info(f": Provided effective length = {self.l_eff:.2f} mm")
        self.logger.info(f": Design capacity of weld = {self.design_capacity/1000:.2f} kN")

    def check_base_metal_strength(self, design_dictionary):
        self.logger.info(": ============== Base Metal Strength Check ==============")
        # IS800:2007 Cl.6.2.2, 6.2.3, 6.3 (shear lag), Cl.7.1.2 (compression)
        Tmin = min(float(design_dictionary[KEY_PLATE1_THICKNESS]), float(design_dictionary[KEY_PLATE2_THICKNESS]))
        self.A_g = Tmin * self.width
        self.gamma_m0 = 1.10
        self.gamma_m1 = 1.25
        
        if self.design_for == 'Compression':
            # Compression: use gross area yielding (Cl.7.1.2)
            self.T_db = self.A_g * self.plate1.fy / self.gamma_m0
            self.logger.info(f": Design strength of plate in compression = {self.T_db/1000:.2f} kN [Cl.7.1.2]")
        else:
            # Tension: yielding and rupture, take minimum (Cl.6.2.2, 6.2.3, 6.3.3)
            # Shear lag factor (Cl.6.3.3): For lap joints, net section efficiency = 0.7
            shear_lag_factor = 0.7
            T_dg = self.A_g * self.plate1.fy / self.gamma_m0  # Gross section yielding (Cl.6.2.2)
            T_dn = 0.9 * self.A_g * self.plate1.fu * shear_lag_factor / self.gamma_m1  # Net section rupture (Cl.6.2.3, 6.3.3)
            self.T_db = min(T_dg, T_dn)
            self.logger.info(f": Design strength of plate in tension = {self.T_db/1000:.2f} kN [Cl.6.2.2, 6.2.3, 6.3.3]")
        
        self.utilization_ratios['base_metal'] = self.axial_force / self.T_db if self.T_db > 0 else float('inf')

    def calculate_final_utilization_ratio(self):
        self.logger.info(": ============== Final Check ==============")
        # Eccentricity check (IS800:2007 Cl.10.5.7.4):
        # For lap joints, if eccentricity exists, reduce design strength accordingly (not implemented, placeholder)
        # TODO: Implement eccentricity reduction if required
        self.utilization_ratio = max(self.utilization_ratios.values())
        self.logger.info(f": Weld utilization ratio = {self.utilization_ratios['weld']:.3f}")
        self.logger.info(f": Base metal utilization ratio = {self.utilization_ratios['base_metal']:.3f}")
        self.logger.info(f": Overall utilization ratio = {self.utilization_ratio:.3f}")
        if self.utilization_ratio > 1.0:
            error_msg = "Design is UNSAFE. Utilization ratio exceeds 1.0."
            self.logger.error(": " + error_msg)
            print("[Osdag ERROR]", error_msg)
            self.design_status = False
            self.design_error = "Utilization ratio exceeds 1.0. Design is unsafe."
            return
        else:
            self.logger.info(": Design is SAFE.")
            self.design_status = True
        self.weld_strength = self.design_capacity
        self.weld_length_effective = self.l_eff

    def save_design(self, popup_summary):
        """
        Generate the LaTeX design report for Lap Joint Welded Connection (Tension/Compression)
        per IS 800:2007.
        """
        try:
            #=======================================
            #=========== HELPER FUNCTIONS ==========
            #=======================================
            def g(attr, default=None):
                """Get attribute value with default"""
                v = getattr(self, attr, default)
                return default if v is None else v
            
            def f2(x, default=0.0):
                """Format to 2 decimal places"""
                try:
                    return round(float(x), 2)
                except (TypeError, ValueError):
                    return default

            #================================================
            #=========== EXTRACT ALL DESIGN VALUES ==========
            #================================================
            module = g('module', 'Lap Joint Welded')
            mainmodule = 'Simple Connection'
            design_for = g('design_for', 'Tension').strip()
            is_comp = design_for.lower().startswith('c')
            
            edge_type = g('edgetype', 'Sheared or hand flame cut')
            
            # Plate properties
            plate1_thk = f2(self.plate1.thickness[0] if isinstance(self.plate1.thickness, list) else self.plate1.thickness, 0.0)
            plate2_thk = f2(self.plate2.thickness[0] if isinstance(self.plate2.thickness, list) else self.plate2.thickness, 0.0)
            plate_thk_min = min(plate1_thk, plate2_thk)
            width = f2(g('width', 0.0), 0.0)
            fy = f2(self.plate1.fy if hasattr(self, 'plate1') else 250, 250)
            fu = f2(self.plate1.fu if hasattr(self, 'plate1') else 410, 410)
            
            # Use stored values for strength calculation variables to match Dock exactly
            fu_weld = g('fu_weld', float(g('weld.fu', 410)))
            fu_parent = g('fu_parent', min(self.plate1.fu, self.plate2.fu) if hasattr(self, 'plate1') else 410)
            
            # Load
            axial_force_N = f2(g('axial_force', g('axialforce', g('tensileforce', 0.0))), 0.0)
            axial_kN = f2(axial_force_N / 1000, 0.0)
            
            # Weld properties
            weld_size = f2(g('weld_size', g('weldsize', 0.0)), 0.0)
            weld_type = g('weld.type', 'Shop weld')
            weld_fabrication = g('weld.fabrication', 'Shop Weld')
            gamma_mw = 1.25 if 'shop' in weld_type.lower() else 1.50
            
            # Effective throat thickness
            effective_throat = f2(g('effective_throat_thickness', 0.7 * weld_size), 0.0)
            
            # Weld lengths
            l_eff = f2(g('l_eff', g('weld_length_effective', g('weldlengtheffective', 0.0))), 0.0)
            l_eff_min = f2(max(4 * weld_size, 40), 0.0)
            l_eff_max = f2(70 * weld_size, 0.0)
            
            # Long joint reduction factor
            beta_lw = f2(g('beta_lw', g('betalw', 1.0)), 1.0)
            
            # End return and connection length
            end_return = f2(g('end_return_length', max(2 * weld_size, 12)), 0.0)
            
            # Overlap: Use calculated value if available to capture clearance logic
            min_overlap_req = max(4 * weld_size, 40)
            overlap_length = f2(g('overlap_length', min_overlap_req), 0.0)
            
            conn_length = f2(g('connection_length', l_eff + 2 * end_return), 0.0)
            
            # Base metal capacity
            Ag = plate_thk_min * width
            gamma_m0 = 1.10
            gamma_m1 = 1.25
            
            if is_comp:
                base_metal_capacity_kN = f2((Ag * fy / gamma_m0) / 1000, 0.0)
            else:
                Tdg = (Ag * fy / gamma_m0) / 1000
                Tdn = (0.9 * Ag * fu * 0.7 / gamma_m1) / 1000
                base_metal_capacity_kN = f2(min(Tdg, Tdn), 0.0)

            # Retrieve calculated unit design strengths to match Dock
            P_wd_val = g('weld_design_strength', (fu_weld * effective_throat) / (math.sqrt(3) * gamma_mw))
            P_md_val = g('parent_design_strength', 0.6 * fu_parent * effective_throat / gamma_mw)
            P_d_val = g('fillet_weld_design_strength', min(P_wd_val, P_md_val))

            #====================================================
            #=========== BUILD REPORT INPUT DICTIONARY ==========
            #====================================================
            self.report_input = {
                KEY_MODULE: module,
                KEY_MAIN_MODULE: mainmodule,
                KEY_DISP_DESIGN_FOR: design_for,
                f"Thickness of Plate-1 (mm) *": plate1_thk,
                f"Thickness of Plate-2 (mm) *": plate2_thk,
                KEY_DISP_PLATE_WIDTH: width,
                KEY_DISP_MATERIAL: g('main_material', g('mainmaterial', 'N/A')),
                KEY_DISP_WELD_SIZE: weld_size,
                f"{'Tensile' if not is_comp else 'Axial'} Force (kN) *": axial_kN,
                
                "Additional inputs": "TITLE",
                "Edge Preparation Method": edge_type,
                KEY_DISP_DP_WELD_TYPE: weld_fabrication,
                KEY_DISP_DP_WELD_MATERIAL_G_O_REPORT: f2(fu_weld, 410),
            }
            
            # ========== BUILD REPORT CHECK ==========
            self.report_check = []

            # ==========================================================================
            # SECTION 3.1: CALCULATING WELD STRENGTH
            # ==========================================================================
            # 3.2.1 Weld Size Requirements
            self.report_check.append([
                "SubSection", "Weld Size Check", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])
            
            s_min = IS800_2007.cl_10_5_2_3_min_weld_size(plate1_thk, plate2_thk)
            if plate_thk_min >= 10:
                s_max = plate_thk_min - 1.5
            else:
                s_max = plate_thk_min
            s_max = f2(s_max, 0.0)
            
            size_check_req = Math(inline=True)
            size_check_req.append(NoEscape(r'\begin{aligned}'))
            size_check_req.append(NoEscape(r's_{\text{min}} &= ' + str(s_min) + r' \text{ mm}\\'))
            size_check_req.append(NoEscape(r'&[\text{As per Table 21, IS 800:2007}]\\'))
            size_check_req.append(NoEscape(r's_{\text{max}} &= ' + str(s_max) + r' \text{ mm}\\'))
            size_check_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.2.3, 10.5.2.4}]'))
            size_check_req.append(NoEscape(r'\end{aligned}'))
            
            size_check_prov = Math(inline=True)
            size_check_prov.append(NoEscape(r's = ' + str(weld_size) + r' \text{ mm}'))
            
            size_status = "PASS" if (s_min <= weld_size <= s_max) else "FAIL"
            self.report_check.append(["Weld Size", size_check_req, size_check_prov, size_status])

            # 3.1.1 Fillet Weld (Strength Calculation + Throat Thickness)
            self.report_check.append([
                "SubSection", "Weld Strength Calculation", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])
            
            # Effective Throat Thickness (Eq 3.2/3.3)
            throat_req = Math(inline=True)
            throat_req.append(NoEscape(r'\begin{aligned}'))
            throat_req.append(NoEscape(r't_t &= K \times s\\'))
            throat_req.append(NoEscape(r'&= 0.7 \times ' + str(weld_size) + r'\\'))
            throat_req.append(NoEscape(r'&= ' + str(effective_throat) + r' \text{ mm}\\'))
            throat_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.3.2}]'))
            throat_req.append(NoEscape(r'\end{aligned}'))
            self.report_check.append(["Throat Thickness", "", throat_req, ""])

            # Weld Metall Strength (Pwd) (Eq 3.1)
            weld_metal_req = Math(inline=True)
            weld_metal_req.append(NoEscape(r'\begin{aligned}\\'))
            weld_metal_req.append(NoEscape(r'P_{wd} &= \frac{f_u}{\sqrt{3}} \cdot \frac{t_t}{\gamma_{mw}}\\\\'))
            weld_metal_req.append(NoEscape(r'&= \frac{' + str(f2(fu_weld)) + r'}{\sqrt{3}} \times \frac{' + str(effective_throat) + r'}{' + str(gamma_mw) + r'}\\\\'))
            weld_metal_req.append(NoEscape(r'&= ' + f'{P_wd_val:.2f}' + r' \text{ N/mm}\\'))
            weld_metal_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.7.1.1}]'))
            weld_metal_req.append(NoEscape(r'\end{aligned}'))
            self.report_check.append(["Weld Metal Strength", "", weld_metal_req, ""])
            
            # Parent Metal Strength (Pmd) (Eq 3.4)
            parent_metal_req = Math(inline=True)
            parent_metal_req.append(NoEscape(r'\begin{aligned}\\'))
            parent_metal_req.append(NoEscape(r'P_{md} &= 0.6 \cdot f_u \cdot \frac{t_t}{\gamma_{mw}}\\\\'))
            parent_metal_req.append(NoEscape(r'&= 0.6 \times ' + str(f2(fu_parent)) + r' \times \frac{' + str(effective_throat) + r'}{' + str(gamma_mw) + r'}\\\\'))
            parent_metal_req.append(NoEscape(r'&= ' + f'{P_md_val:.2f}' + r' \text{ N/mm}\\'))
            parent_metal_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.7.1.2}]'))
            parent_metal_req.append(NoEscape(r'\end{aligned}'))
            self.report_check.append(["Parent Metal Strength", "", parent_metal_req, ""])
            
            # Governing Design Strength (Pd) (Eq 3.5)
            design_strength_eq = Math(inline=True)
            design_strength_eq.append(NoEscape(r'\begin{aligned}'))
            design_strength_eq.append(NoEscape(r'P_d &= \min(P_{wd}, P_{md})\\'))
            design_strength_eq.append(NoEscape(r'&= \min(' + f'{P_wd_val:.2f}' + r', ' + f'{P_md_val:.2f}' + r')\\'))
            design_strength_eq.append(NoEscape(r'&= ' + f'{P_d_val:.2f}' + r' \text{ N/mm}\\'))
            design_strength_eq.append(NoEscape(r'&[\text{Ref. Cl. 10.5.7.1}]'))
            design_strength_eq.append(NoEscape(r'\end{aligned}'))
            self.report_check.append(["Design Strength", "", design_strength_eq, ""])

            # 3.1.2 Reduction Factors (Long Weld)
            self.report_check.append([
                "SubSection", "Long Joint Reduction Factor", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])

            if l_eff > 150 * effective_throat:
                beta_req = Math(inline=True)
                beta_req.append(NoEscape(r'\begin{aligned}'))
                beta_req.append(NoEscape(r'\text{Since } l_w &> 150 \times t_t\\'))
                beta_req.append(NoEscape(r'\beta_{lw} &= 1.2 - 0.2 \times \frac{l_w}{150 \times t_t}\\'))
                beta_req.append(NoEscape(r'&= 1.2 - 0.2 \times \frac{' + str(l_eff) + r'}{150 \times ' + str(effective_throat) + r'}\\'))
                beta_calc = 1.2 - 0.2 * (l_eff / (150 * effective_throat))
                beta_req.append(NoEscape(r'&= ' + f'{beta_calc:.3f}' + r'\\'))
                beta_req.append(NoEscape(r'&\text{(but } 0.6 \leq \beta_{lw} \leq 1.0\text{)}\\'))
                # Use stored beta_lw which should match
                beta_req.append(NoEscape(r'\beta_{lw} &= ' + f'{beta_lw:.2f}' + r'\\'))
                beta_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.7.2}]'))
                beta_req.append(NoEscape(r'\end{aligned}'))
                beta_status = ""
            else:
                beta_req = Math(inline=True)
                beta_req.append(NoEscape(r'\begin{aligned}'))
                beta_req.append(NoEscape(r'\text{Since } l_w &\leq 150 \times t_t\\'))
                beta_req.append(NoEscape(r'\beta_{lw} &= 1.0\\'))
                beta_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.7.2}]'))
                beta_req.append(NoEscape(r'\end{aligned}'))
                beta_status = "PASS"

            beta_prov = Math(inline=True)
            beta_prov.append(NoEscape(r'\beta_{lw} = ' + f'{beta_lw:.1f}'))
            self.report_check.append(["Long Joint Factor", beta_req, beta_prov, beta_status])

            # ==========================================================================
            # SECTION 3.2: DETAILING CHECKLIST
            # ==========================================================================

            # 3.2.2 Effective Length of Weld (Limits)
            self.report_check.append([
                "SubSection", "Effective Length Limits", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])
            
            eff_len_req = Math(inline=True)
            eff_len_req.append(NoEscape(r'\begin{aligned}'))
            eff_len_req.append(NoEscape(r'l_{\text{eff,min}} &= \max(4s, 40)\\'))  # Step 1: Formula
            eff_len_req.append(NoEscape(r'&= \max(4 \times ' + str(weld_size) + r', 40)\\'))  # Step 2: Substitution
            eff_len_req.append(NoEscape(r'&= ' + str(l_eff_min) + r' \text{ mm}\\'))  # Step 3: Result
            eff_len_req.append(NoEscape(r'l_{\text{eff,max}} &= 70s\\'))
            eff_len_req.append(NoEscape(r'&= 70 \times ' + str(weld_size) + r'\\'))
            eff_len_req.append(NoEscape(r'&= ' + str(l_eff_max) + r' \text{ mm}\\'))
            eff_len_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.3}]'))
            eff_len_req.append(NoEscape(r'\end{aligned}'))
            
            eff_len_prov = Math(inline=True)
            eff_len_prov.append(NoEscape(r'l_{\text{eff}} = ' + str(l_eff) + r' \text{ mm}'))
            
            eff_status = "PASS" if (l_eff_min <= l_eff <= l_eff_max) else "FAIL"
            self.report_check.append(["Length Limits", eff_len_req, eff_len_prov, eff_status])

            # 3.2.3 End Returns
            self.report_check.append([
                "SubSection", "End Returns", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])
            
            return_req = Math(inline=True)
            return_req.append(NoEscape(r'\begin{aligned}'))
            return_req.append(NoEscape(r'\text{Min. Length} &= \max(2s, 12)\\'))
            return_req.append(NoEscape(r'&= \max(2 \times ' + str(weld_size) + r', 12)\\'))
            return_req.append(NoEscape(r'&= ' + str(end_return) + r' \text{ mm}\\'))
            return_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.4.5}]'))
            return_req.append(NoEscape(r'\end{aligned}'))
            
            return_prov = Math(inline=True)
            return_prov.append(NoEscape(str(end_return) + r' \text{ mm}'))
            
            self.report_check.append(["End Returns", return_req, return_prov, "PASS"])

            # ==========================================================================
            # SECTION 3.3: DETAILING
            # ==========================================================================

            # 3.3.1 Calculating Required Weld Length
            self.report_check.append([
                "SubSection", "Required Weld Length", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])
            
            # Required Length Calculation (Eq 3.15)
            # Use P_d_val from object to be consistent
            l_req_base = axial_force_N / (2 * P_d_val) if P_d_val > 0 else 9999
            l_req_disp = f2(l_req_base, 0.0)
            
            length_req_calc = Math(inline=True)
            length_req_calc.append(NoEscape(r'\begin{aligned}\\'))
            length_req_calc.append(NoEscape(r'l_{\text{req}} &= \frac{P}{2 \cdot P_d}\\\\'))
            length_req_calc.append(NoEscape(r'&= \frac{' + str(int(axial_force_N)) + r'}{2 \times ' + f'{P_d_val:.2f}' + r'}\\\\'))
            length_req_calc.append(NoEscape(r'&= ' + str(l_req_disp) + r' \text{ mm}\\\\'))
            if beta_lw < 1.0:
                l_req_final = l_req_base / beta_lw
                length_req_calc.append(NoEscape(r'l_{\text{req,mod}} &= \frac{l_{\text{req}}}{\beta_{lw}} = \frac{' + str(l_req_disp) + r'}{' + str(beta_lw) + r'} = ' + f'{l_req_final:.1f}' + r' \text{ mm}\\'))
            else:
                length_req_calc.append(NoEscape(r'&\text{No long joint reduction.}\\'))
            length_req_calc.append(NoEscape(r'\end{aligned}'))
            
            self.report_check.append(["Required Length", "", length_req_calc, ""])

            # 3.3.2 Determining Connection Configuration
            self.report_check.append([
                "SubSection", "Connection Configuration", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])
            
            config_calc = Math(inline=True)
            config_calc.append(NoEscape(r'\begin{aligned}'))
            config_calc.append(NoEscape(r'L_{\text{conn}} &= l_{\text{eff}} + 2 \times l_{\text{return}}\\' ))
            config_calc.append(NoEscape(r'&= ' + str(l_eff) + r' + 2 \times ' + str(end_return) + r'\\'))
            config_calc.append(NoEscape(r'&= ' + str(conn_length) + r' \text{ mm}\\'))
            config_calc.append(NoEscape(r'\end{aligned}'))
            
            self.report_check.append(["Configuration", "", config_calc, ""])

            # ==========================================================================
            # ADDITIONAL CHECKS
            # ==========================================================================

            # Base Metal Strength
            self.report_check.append([
                "SubSection", "Base Metal Strength", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])
            
            if is_comp:
                comp_req = Math(inline=True)
                comp_req.append(NoEscape(r'\begin{aligned}\\'))
                comp_req.append(NoEscape(r'P_d &= \frac{A_g \times f_y}{\gamma_{m0}}\\\\'))
                comp_req.append(NoEscape(r'&= \frac{' + f'{Ag:.1f}' + r' \times ' + str(fy) + r'}{' + str(gamma_m0) + r'}\\\\'))
                comp_req.append(NoEscape(r'&= ' + str(base_metal_capacity_kN) + r' \text{ kN}\\'))
                comp_req.append(NoEscape(r'&[\text{Ref. Cl. 7.1.2}]'))
                comp_req.append(NoEscape(r'\end{aligned}'))
                comp_status = "PASS" if base_metal_capacity_kN >= axial_kN else "FAIL"
                self.report_check.append(["Plate Tension Capacity", f"{axial_kN:.2f} kN", comp_req, comp_status])
            else:
                ten_req = Math(inline=True)
                ten_req.append(NoEscape(r'\begin{aligned}'))
                ten_req.append(NoEscape(r'T_{dg} &= \frac{A_g f_y}{\gamma_{m0}} = ' + f'{Tdg:.2f}' + r' \text{ kN}\\'))
                ten_req.append(NoEscape(r'T_{dn} &= \frac{0.9 A_g f_u \beta}{\gamma_{m1}} = ' + f'{Tdn:.2f}' + r' \text{ kN}\\'))
                ten_req.append(NoEscape(r'T_d &= \min(T_{dg}, T_{dn}) = ' + str(base_metal_capacity_kN) + r' \text{ kN}\\'))
                ten_req.append(NoEscape(r'&[\text{Ref. Cl. 6.2, 6.3}]'))
                ten_req.append(NoEscape(r'\end{aligned}'))
                ten_status = "PASS" if base_metal_capacity_kN >= axial_kN else "FAIL"
                self.report_check.append(["Plate Tension Capacity", f"{axial_kN:.2f} kN", ten_req, ten_status])

            # ==========================================================================
            # UTILIZATION RATIO
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Utilization Ratio", "|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|"
            ])
            
            n = 2
            # Use stored capacity from design capacity if available to be exact
            weld_capacity_val = g('design_capacity', 2 * l_eff * P_d_val * beta_lw)
            weld_capacity_kN = f2(weld_capacity_val / 1000, 0.0)
            
            # Use stored UR if available
            utilization_ratio_val = g('utilization_ratio', axial_kN / weld_capacity_kN if weld_capacity_kN > 0 else 0.0)
            utilization_ratio = f2(utilization_ratio_val, 0.0)

            util_req = Math(inline=True)
            util_req.append(NoEscape(r'\begin{aligned}'))
            util_req.append(NoEscape(r'P_{\text{capacity}} &= n \times l_{\text{eff}} \times P_d \times \beta_{lw}\\'))
            util_req.append(NoEscape(r'&= ' + str(n) + r' \times ' + str(l_eff) + r' \times ' + f'{P_d_val:.2f}' + r' \times ' + str(beta_lw) + r'\\'))
            util_req.append(NoEscape(r'&= ' + str(weld_capacity_kN) + r' \text{ kN}\\\\'))
            util_req.append(NoEscape(r'\text{UR} &= \frac{P}{P_{\text{capacity}}}\\\\'))
            util_req.append(NoEscape(r'&= \frac{' + str(axial_kN) + r'}{' + str(weld_capacity_kN) + r'}\\\\'))
            util_req.append(NoEscape(r'&= ' + str(utilization_ratio) + r'\\'))
            util_req.append(NoEscape(r'\end{aligned}'))

            util_prov = Math(inline=True)
            util_prov.append(NoEscape(str(utilization_ratio) + r' \leq 1.0'))

            util_status = "PASS" if utilization_ratio <= 1.0 else "FAIL"
            self.report_check.append(["Utilization", f"{axial_kN:.2f} kN", util_req, util_status])

            #==========================================
            #=========== GENERATE PDF REPORT ==========
            #==========================================
            Disp_2d_image = []
            Disp_3D_image = "/ResourceFiles/images/3d.png"
            rel_path = os.path.abspath(".").replace("\\", "/")
            fname_no_ext = popup_summary.get("filename", "LapJointWeldedReport")
            folder = popup_summary.get('folder', './reports')
            os.makedirs(folder, exist_ok=True)

            CreateLatex.save_latex(
                CreateLatex(), self.report_input, self.report_check,
                popup_summary, fname_no_ext, rel_path, Disp_2d_image, Disp_3D_image,
                module=self.module
            )
            self.logger.info(f"Report generated successfully: {fname_no_ext}.pdf")
            return True

        except Exception as e:
            print(f"WARNING in save_design(): {e}")
            import traceback
            traceback.print_exc()
            return False


    def get_3d_components(self):
        components = []
        t1 = ('Model', self.call_3DModel)
        components.append(t1)
        t2 = ('Plate 1', self.call_3DPlate1)
        components.append(t2)
        t3 = ('Plate 2', self.call_3DPlate2)
        components.append(t3)
        t4 = ('Welds', self.call_3DWeld)
        components.append(t4)
        return components

    def call_3DModel(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Model':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Model", bgcolor)

    def call_3DPlate1(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Plate 1':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel('Plate 1', bgcolor)

    def call_3DPlate2(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Plate 2':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel('Plate 2', bgcolor)

    def call_3DWeld(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Welds':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel('Welds', bgcolor)