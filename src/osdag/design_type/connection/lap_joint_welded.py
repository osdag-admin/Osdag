"""
Module: lap_joint_welded.py
Author: Aman, Nishi Kant Mandal, Tanu Singh
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
import logging

import math

from PyQt5.QtCore import Qt

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

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []
        tabs.append((("Weld", TYPE_TAB_2, self.weld_values)))
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
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
        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        design_input.append((None, [
            KEY_DP_WELD_TYPE,
            KEY_DP_WELD_MATERIAL_G_O,
            KEY_DP_DETAILING_EDGE_TYPE,
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

    def set_osdaglogger(key):
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
        t17 = (KEY_TENSILE_FORCE, KEY_DISP_TENSILE_FORCE, TYPE_TEXTBOX, None, True, 'Int Validator')
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
        return out_list

    def module_name(self):
        return KEY_DISP_LAPJOINTWELDED

    def call_3DColumn(self, ui, bgcolor):
        if ui.chkBxCol.isChecked():
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
        ui.commLogicObj.display_3DModel("Column", bgcolor)

    def get_3d_components(self):
        components = []
        t1 = ('Model', self.call_3DModel)
        components.append(t1)
        t3 = ('Plate1', self.call_3DColumn)
        components.append(t3)
        t4 = ('Plate2', self.call_3DPlate)
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
                    if option[0] == KEY_PLATE_WIDTH:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True
                    elif option[0] == KEY_TENSILE_FORCE:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag2 = True
            else:
                pass

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
        else:
            flag = True

        if flag and flag1 and flag2:
            self.set_input_values(self, design_dictionary)
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

        super(LapJointWelded, self).set_input_values(self, design_dictionary_with_defaults)
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Lap Joint Welded Connection"
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.tensile_force = float(design_dictionary[KEY_TENSILE_FORCE]) * 1000
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
        self.design_of_weld(self, design_dictionary)

    def design_of_weld(self, design_dictionary):
        logger.info(": =========== Design of Lap Joint Welded Connection ==========")
        logger.info(": Design Approach: IS 800:2007 Clause 10.5")
        self.utilization_ratios = {}

        if not self.weld_size_check(self, design_dictionary):
            return

        self.calculate_weld_strength(self, design_dictionary)
        self.calculate_weld_length(self)
        self.check_long_joint(self)
        self.check_base_metal_strength(self, design_dictionary)
        self.calculate_final_utilization_ratio(self)

    def weld_size_check(self, design_dictionary):
        logger.info(": =============== Weld Size Check ===============")
        weld_size = design_dictionary[KEY_WELD_SIZE]
        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        Tmin = min(plate1_thk, plate2_thk)
        s_min = IS800_2007.cl_10_5_2_3_min_weld_size(plate1_thk, plate2_thk)
        s_max = Tmin - 1.5 if Tmin >= 10 else Tmin

        logger.info(f": Minimum weld size required (s_min) = {s_min} mm [Ref. Table 21, Cl.10.5.2.3]")
        logger.info(f": Maximum allowed weld size (s_max) = {s_max} mm [Ref. Cl.10.5.3.1]")

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
            logger.error(": Selected weld size is not suitable.")
            self.design_status = False
            return False

        self.weld_size = selected_size
        logger.info(f": Selected weld size = {self.weld_size} mm (Pass)")
        return True

    def calculate_weld_strength(self, design_dictionary):
        logger.info(": ============== Weld Strength Calculation ==============")
        # IS800:2007 Cl.10.5.3.2: Throat thickness a = K * s, where K depends on angle
        # For fillet welds, K = sin(θ), θ = weld angle (default 45° if not specified)
        weld_angle = design_dictionary.get('weld_angle', 45)
        if not isinstance(weld_angle, (int, float)):
            try:
                weld_angle = float(weld_angle)
            except Exception:
                weld_angle = 45
        # K = sin(angle)
        K = round(math.sin(math.radians(weld_angle)), 3)
        if K <= 0:
            logger.error(f": Invalid weld angle {weld_angle}°. Using default K=0.7 (45°)")
            K = 0.7
        self.effective_throat_thickness = K * self.weld_size  # Cl.10.5.3.2
        logger.info(f": Effective throat thickness (a) = {self.effective_throat_thickness:.2f} mm [Cl.10.5.3.2, K={K}, θ={weld_angle}°]")
        self.fu = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])
        self.gamma_mw = 1.25 if design_dictionary[KEY_DP_WELD_TYPE] == "Shop weld" else 1.50  # Cl.10.5.7.1
        self.weld_design_strength = (self.fu * self.effective_throat_thickness) / (math.sqrt(3) * self.gamma_mw)  # Cl.10.5.7.1
        self.parent_design_strength = 0.6 * self.fu * self.effective_throat_thickness / self.gamma_mw  # Cl.10.5.7.2
        self.fillet_weld_design_strength = min(self.weld_design_strength, self.parent_design_strength)
        logger.info(f": Design strength of fillet weld = {self.fillet_weld_design_strength:.2f} N/mm^2 [Cl.10.5.7]")
        # Weld stress check (Cl.10.5.7):
        self.weld_stress = self.tensile_force / (2 * self.effective_throat_thickness * self.l_eff) if hasattr(self, 'l_eff') and self.l_eff else 0
        if self.weld_stress > self.fillet_weld_design_strength:
            logger.error(f": Weld stress {self.weld_stress:.2f} N/mm^2 exceeds design strength {self.fillet_weld_design_strength:.2f} N/mm^2 [Cl.10.5.7]")
            self.design_status = False
            raise ValueError("Weld stress exceeds design strength.")

    def calculate_weld_length(self):
        logger.info(": ============== Weld Length Calculation ==============")
        # Required effective weld length (Cl.10.5.4.1)
        self.weld_length_required = self.tensile_force / (2 * self.fillet_weld_design_strength)
        self.leff_min = max(4 * self.weld_size, 40)  # Cl.10.5.4.1
        self.leff_max = 70 * self.weld_size  # Cl.10.5.4.1
        logger.info(f": Required effective weld length = {self.weld_length_required:.2f} mm")
        logger.info(f": Minimum effective weld length = {self.leff_min} mm [Cl.10.5.4.1]")
        logger.info(f": Maximum effective weld length = {self.leff_max} mm [Cl.10.5.4.1]")
        # Check min/max
        if self.weld_length_required < self.leff_min:
            self.l_eff = self.leff_min
            logger.warning(f": Required length is less than minimum, using l_eff = {self.l_eff} mm [Cl.10.5.4.1]")
        elif self.weld_length_required > self.leff_max:
            logger.error(": Required weld length exceeds maximum allowed. Increase weld size. [Cl.10.5.4.1]")
            self.design_status = False
            raise ValueError("Required weld length exceeds maximum allowed.")
        else:
            self.l_eff = self.weld_length_required
            logger.info(": Required weld length is within limits (Pass)")
        # Detailing: Minimum spacing between parallel fillet welds (Cl.10.5.4.2)
        # Not implemented here, but should be checked in GUI or input validation

    def check_long_joint(self):
        logger.info(": ============== Long Joint Check ==============")
        # IS800:2007 Cl.10.5.7.3: Long joint reduction factor
        self.beta_lw = 1.0
        if self.l_eff > 150 * self.effective_throat_thickness:
            self.beta_lw = 1.2 - 0.2 * (self.l_eff / (150 * self.effective_throat_thickness))
            self.beta_lw = max(0.6, min(self.beta_lw, 1.0))
            logger.info(f": Joint is long, reduction factor beta_lw = {self.beta_lw:.3f} [Cl.10.5.7.3]")
        else:
            logger.info(": No reduction for long joint required (Pass)")
        # Modified required length
        l_req_modified = self.l_eff / self.beta_lw
        if l_req_modified < self.leff_min:
            logger.warning(f": Modified required weld length {l_req_modified:.2f} mm is less than minimum effective length {self.leff_min} mm [Cl.10.5.4.1]")
            self.l_eff = self.leff_min
        elif l_req_modified > self.leff_max:
            logger.error(": Modified required weld length exceeds maximum allowed. Increase weld size. [Cl.10.5.4.1]")
            self.design_status = False
            raise ValueError("Modified required weld length exceeds maximum allowed.")
        else:
            self.l_eff = l_req_modified
        # End return length (Cl.10.5.4.5): min(2*s, 12mm)
        self.end_return_length = max(2 * self.weld_size, 12)  # Cl.10.5.4.5
        logger.info(f": End return length = {self.end_return_length} mm [Cl.10.5.4.5]")
        # Overlap length (Cl.10.5.4.3): min overlap = 4*s or 40mm, whichever is more
        self.overlap_length = max(4 * self.weld_size, 40)
        logger.info(f": Overlap length = {self.overlap_length} mm [Cl.10.5.4.3]")
        self.connection_length = self.l_eff + 2 * self.end_return_length
        # Design capacity (Cl.10.5.7.3):
        self.design_capacity = 2 * self.l_eff * self.fillet_weld_design_strength * self.beta_lw
        # Weld stress check (Cl.10.5.7):
        self.weld_stress = self.tensile_force / (2 * self.effective_throat_thickness * self.l_eff) if self.l_eff else 0
        if self.weld_stress > self.fillet_weld_design_strength:
            logger.error(f": Weld stress {self.weld_stress:.2f} N/mm^2 exceeds design strength {self.fillet_weld_design_strength:.2f} N/mm^2 [Cl.10.5.7]")
            self.design_status = False
            raise ValueError("Weld stress exceeds design strength.")
        self.utilization_ratios['weld'] = self.tensile_force / self.design_capacity if self.design_capacity > 0 else float('inf')
        logger.info(f": Provided effective length = {self.l_eff:.2f} mm")
        logger.info(f": Design capacity of weld = {self.design_capacity/1000:.2f} kN")

    def check_base_metal_strength(self, design_dictionary):
        logger.info(": ============== Base Metal Strength Check ==============")
        # IS800:2007 Cl.6.2.2, 6.2.3, 6.3 (shear lag)
        Tmin = min(float(design_dictionary[KEY_PLATE1_THICKNESS]), float(design_dictionary[KEY_PLATE2_THICKNESS]))
        self.A_g = Tmin * self.width
        self.gamma_m0 = 1.10
        self.gamma_m1 = 1.25
        # Shear lag factor (Cl.6.3.3):
        # For lap joints, net section efficiency = 0.7 (if not otherwise calculated)
        shear_lag_factor = 0.7
        T_dg = self.A_g * self.plate1.fy / self.gamma_m0  # Gross section yielding (Cl.6.2.2)
        T_dn = 0.9 * self.A_g * self.plate1.fu * shear_lag_factor / self.gamma_m1  # Net section rupture (Cl.6.2.3, 6.3.3)
        self.T_db = min(T_dg, T_dn)
        self.utilization_ratios['base_metal'] = self.tensile_force / self.T_db if self.T_db > 0 else float('inf')
        logger.info(f": Design strength of plate = {self.T_db/1000:.2f} kN [Cl.6.2.2, 6.2.3, 6.3.3]")

    def calculate_final_utilization_ratio(self):
        logger.info(": ============== Final Check ==============")
        # Eccentricity check (IS800:2007 Cl.10.5.7.4):
        # For lap joints, if eccentricity exists, reduce design strength accordingly (not implemented, placeholder)
        # TODO: Implement eccentricity reduction if required
        self.utilization_ratio = max(self.utilization_ratios.values())
        logger.info(f": Weld utilization ratio = {self.utilization_ratios['weld']:.3f}")
        logger.info(f": Base metal utilization ratio = {self.utilization_ratios['base_metal']:.3f}")
        logger.info(f": Overall utilization ratio = {self.utilization_ratio:.3f}")
        if self.utilization_ratio > 1.0:
            logger.error(": Design is UNSAFE. Utilization ratio exceeds 1.0.")
            self.design_status = False
            raise ValueError("Utilization ratio exceeds 1.0. Design is unsafe.")
        else:
            logger.info(": Design is SAFE.")
            self.design_status = True
        self.weld_strength = self.design_capacity
        self.weld_length_effective = self.l_eff

    def save_design(self, popup_summary):
        self.report_input = {
            KEY_MODULE: self.module,
            KEY_MAIN_MODULE: self.mainmodule,
            KEY_DISP_AXIAL: round(self.tensile_force / 1000, 2),
            "Connecting Members": "TITLE",
            KEY_DISP_PLATETHK: str([int(d) for d in [self.plate1.thickness[0], self.plate2.thickness[0]]]),
            KEY_DISP_MATERIAL: self.main_material,
            KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.plate1.fu,
            KEY_DISP_YIELD_STRENGTH_REPORT: self.plate1.fy,
            KEY_DISP_PLATE_WIDTH: self.width,
            "Weld Details - Input and Design Preference": "TITLE",
            KEY_DISP_DP_WELD_TYPE: self.weld.type,
            KEY_DISP_DP_WELD_FAB: self.weld.fabrication,
            KEY_DISP_DP_WELD_MATERIAL_G_O_REPORT: self.weld.fu,
            KEY_DISP_WELD_SIZE: self.weld_size,
            "Safety Factors": "TITLE",
            KEY_DISP_GAMMA_MW: self.gamma_mw,
            "Weld Angle (deg)": getattr(self, 'weld_angle', 45),
            "Effective Throat Thickness (mm)": getattr(self, 'effective_throat_thickness', None),
            "Long Joint Reduction Factor β_lw": getattr(self, 'beta_lw', 1.0),
            "End Return Length (mm)": getattr(self, 'end_return_length', None),
            "Overlap Length (mm)": getattr(self, 'overlap_length', None),
            "Shear Lag Factor": 0.7,
        }
        self.report_check = []
        if self.design_status:
            t1 = ('SubSection', 'Weld Design', '|p{3cm}|p{6.5cm}|p{5cm}|p{1cm}|')
            self.report_check.append(t1)
            t1 = (DISP_WELD_STRENGTH,
                  f"Required: {self.tensile_force / 1000:.2f} kN",
                  f"Provided: {self.design_capacity / 1000:.2f} kN",
                  "Pass" if self.design_capacity >= self.tensile_force else "Fail")
            self.report_check.append(t1)
            t1 = ('Overall Utilization Ratio',
                  "<= 1.0",
                  f"{self.utilization_ratio:.3f}",
                  "Pass" if self.utilization_ratio <= 1.0 else "Fail")
            self.report_check.append(t1)
        else:
            t1 = ('SubSection', 'Design Status', '|p{3.5cm}|p{4.5cm}|p{6cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t1 = ('Design Status', '', 'Design Fails', 'Fail')
            self.report_check.append(t1)
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary,
                             fname_no_ext, os.path.abspath(".").replace("\\", "/"), [], "/ResourceFiles/images/3d.png", module=self.module)