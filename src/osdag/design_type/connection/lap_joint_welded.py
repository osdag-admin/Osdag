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

from PyQt5.QtCore import Qt

class LapJointWelded(MomentConnection):
    def __init__(self):
        super(LapJointWelded, self).__init__()
        self.design_status = False
        self.spacing = None 

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []
        # Only Bolt and Detailing tabs
        tabs.append((("Weld", TYPE_TAB_2, self.weld_values)))
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
        return tabs

    def tab_value_changed(self):
        # No tab value dependencies needed for bolt and detailing
        return []

    def edit_tabs(self):
        return []  # Keep original empty implementation

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
        # Get fu value from selected material
        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            fu = Material(design_dictionary[KEY_MATERIAL], 41).fu
        else:
            fu = ''

        # Default values as per requirements
        defaults = {
            KEY_DP_WELD_TYPE: "Shop weld",
            KEY_DP_WELD_MATERIAL_G_O: str(fu),  # Set weld material grade to fu of selected material
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
        
        # Edge preparation method as per Cl. 10.2.4 of IS:800:2007
        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX,
            ['Sheared or hand flame cut', 'Rolled, machine-flame cut, sawn and planed'],
            values[KEY_DP_DETAILING_EDGE_TYPE])
        detailing.append(t1)

        t4 = ("textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION_LAPJOINT, None)
        detailing.append(t4)

        return detailing

    # def bolt_values(self, input_dictionary):
    #     values = {
    #         KEY_DP_BOLT_TYPE: 'Non Pre-tensioned',
    #         KEY_DP_BOLT_HOLE_TYPE: 'Standard',
    #         KEY_DP_BOLT_SLIP_FACTOR: '0.3'
    #     }

    #     for key in values.keys():
    #         if key in input_dictionary.keys():
    #             values[key] = input_dictionary[key]

    #     bolt = []
        
    #     # Bolt type selection
    #     t1 = (KEY_DP_BOLT_TYPE, "Type", TYPE_COMBOBOX,
    #         ['Non Pre-tensioned', 'Pre-tensioned'],
    #         values[KEY_DP_BOLT_TYPE])
    #     bolt.append(t1)
        
    #     # Bolt hole type
    #     t2 = (KEY_DP_BOLT_HOLE_TYPE, "Bolt Hole", TYPE_COMBOBOX,
    #         ['Standard', 'Over-sized'],
    #         values[KEY_DP_BOLT_HOLE_TYPE])
    #     bolt.append(t2)
        
    #     # Slip factor as per Table 20 of IS 800
    #     t3 = (KEY_DP_BOLT_SLIP_FACTOR, "Slip Factor", TYPE_COMBOBOX,
    #         ['0.3', '0.45', '0.5'],
    #         values[KEY_DP_BOLT_SLIP_FACTOR])
    #     bolt.append(t3)

    #     return bolt

    def weld_values(self, input_dictionary):
        # Get fu value from selected material if available
        fu = ''
        if input_dictionary and KEY_MATERIAL in input_dictionary:
            if input_dictionary[KEY_MATERIAL] != 'Select Material':
                fu = Material(input_dictionary[KEY_MATERIAL], 41).fu

        values = {
            KEY_DP_WELD_TYPE: 'Shop weld',
            KEY_DP_WELD_MATERIAL_G_O: str(fu) if fu else '410',  # Default to 410 if no material selected
        }

        # Update values from input dictionary if available
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
        
    
    def spacing(self, status):
        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details - 3 x 3 pattern considered")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
            [str(files("osdag.data.ResourceFiles.images").joinpath("spacing_3.png")), 400, 277, ""])  # [image, width, height, caption]
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def output_values(self, flag):
        out_list=[]
        # Cover plate details
        # Calculate cover_type based on planes attribute
        t21 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t21)

        t22 = (KEY_OUT_UTILISATION_RATIO, KEY_OUT_DISP_UTILISATION_RATIO, TYPE_TEXTBOX,
               round(self.utilization_ratio, 3) if flag else '', True)
        out_list.append(t22)

        t23 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX,
               "Fillet" if flag else '', True)
        out_list.append(t23)

        t24 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX,
               round(self.weld_size, 1) if flag else '', True)
        out_list.append(t24)

        t25 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH_kN, TYPE_TEXTBOX,
               round(self.weld_strength/1000, 2) if flag else '', True)  # Convert to kN
        out_list.append(t25)

        t26 = (KEY_OUT_WELD_LENGTH_EFF, KEY_OUT_DISP_WELD_LENGTH_EFF, TYPE_TEXTBOX,
               round(self.weld_length_effective, 1) if flag else '', True)
        out_list.append(t26)

        t27 = (KEY_OUT_WELD_CONN_LEN, KEY_OUT_DISP_WELD_CONN_LEN, TYPE_TEXTBOX,
               round(self.connection_length, 1) if flag else '', True)
        out_list.append(t27)

        return out_list

    def module_name(self):

        return KEY_DISP_LAPJOINTBOLTED
    
    def func_for_validation(self, design_dictionary):

        all_errors = []
        "check valid inputs and empty inputs in input dock"
        # print(design_dictionary,'djsgggggggggggggggggggggggggggggggggggggggggggggggggggggggg')
        self.design_status = False

        flag = False
        flag1 = False
        flag2 = False
        # self.include_status = True

        option_list = self.input_values(self)
        missing_fields_list = []

        print(f'\n func_for_validation option list = {option_list}'
              f'\n  design_dictionary {design_dictionary}')

        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':

                    print(f"\n option {option}")

                    missing_fields_list.append(option[1])
                else:
                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_PLATE_WIDTH:
                        # val = option[4]
                        # print(design_dictionary[option[0]], "jhvhj")
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True

                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_TENSILE_FORCE:

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
            # flag = False
        else:
            flag = True
        if flag  and flag1 and flag2:
            # self.set_input_values(self, design_dictionary)
            # print("DESIGN DICT" + str(design_dictionary))
            print("succsess")
        else:
            return all_errors


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
    
    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from Column and Beams table.
        """

        # @author Arsil Zunzunia
        global logger
        red_list = red_list_function()
        if self.supported_section.designation in red_list or self.supporting_section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")


    def set_input_values(self, design_dictionary):
        "initialisation of components required to design a butt joint welded along with connection"
        # Call parent class's set_input_values with default values if not provided
        design_dictionary_with_defaults = design_dictionary.copy()
        if KEY_SHEAR not in design_dictionary_with_defaults:
            design_dictionary_with_defaults[KEY_SHEAR] = 0.0  # Default shear value if not provided
        if KEY_AXIAL not in design_dictionary_with_defaults:
            design_dictionary_with_defaults[KEY_AXIAL] = 0.0  # Default axial value if not provided
        if KEY_MOMENT not in design_dictionary_with_defaults:
            design_dictionary_with_defaults[KEY_MOMENT] = 0.0  # Default moment value if not provided
        
        # Call parent class method correctly
        super(LapJointWelded, self).set_input_values(self,design_dictionary_with_defaults)
        print(design_dictionary,"input values are set. Doing preliminary member checks")
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Lap Joint Welded Connection"
        
        # self.plate_thickness = [3,4,6,8,10,12,14,16,20,22,24,25,26,28,30,32,36,40,45,50,56,63,80]
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.tensile_force = float(design_dictionary[KEY_TENSILE_FORCE])*1000
        self.width = design_dictionary[KEY_PLATE_WIDTH]

        # print(self.sizelist)
        self.efficiency = 0.0
        self.K = 1
        self.count = 0
        self.plate1 = Plate(thickness=[design_dictionary[KEY_PLATE1_THICKNESS]],
                        material_grade=design_dictionary[KEY_MATERIAL],
                        width=design_dictionary[KEY_PLATE_WIDTH])
        self.plate2 = Plate(thickness=[design_dictionary[KEY_PLATE2_THICKNESS]],
                            material_grade=design_dictionary[KEY_MATERIAL],
                            width=design_dictionary[KEY_PLATE_WIDTH])
        
        self.weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                         type=design_dictionary[KEY_DP_WELD_TYPE],
                         fabrication=design_dictionary.get(KEY_DP_FAB_SHOP, KEY_DP_FAB_SHOP))
        # Set weld size after creating the weld object
        self.weld.size = design_dictionary[KEY_WELD_SIZE]
        # Start design process
        print("input values are set. Doing preliminary member checks")
        self.member_design_status = False
        self.max_limit_status_1 = False
        self.max_limit_status_2 = False
        self.weld_design_status = False
        self.thick_design_status = False
        self.plate_design_status = False


        self.leg_size = 0
        self.yield_strength = 0
        self.partial_safety_factor = 0
        self.max_weld_size = 0
        #change from here
        self.final_pitch = 0
        self.final_end_dist = 0
        self.final_edge_dist = 0
        self.final_gauge = 0
        self.rows = 0
        self.cols = 0
        self.len_conn = 0
        self.max_gauge_round = 0
        self.max_pitch_round = 0
        self.utilization_ratio = 0
        self.bij = 0
        self.blg = 0
        self.cover_plate = design_dictionary[KEY_COVER_PLATE]
        
        # Start design process
        self.design_of_weld(self,design_dictionary)
    
    #========================DESIGN OF WELD==================================================================
    def design_of_weld(self, design_dictionary):
        """Design sequence for welded butt joint"""
        logger.info(": ===========  Design for Welded Butt Joint  ===========")
        logger.info(": Design Approach - IS 800:2007 Clause 10")

        if not self._select_and_validate_weld_size(design_dictionary):
            return
        self._calculate_weld_strengths(design_dictionary)
        if not self._calculate_and_validate_weld_length():
            return
        if not self._apply_long_joint_reduction_and_check():
            return

    def _select_and_validate_weld_size(self, design_dictionary):
        weld_size = design_dictionary[KEY_WELD_SIZE]
        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        Tmin = min(plate1_thk, plate2_thk)
        s_min = IS800_2007.cl_10_5_2_3_min_weld_size(plate1_thk, plate2_thk)
        # Set s_max as per IS 800:2007 Cl. 10.5.2.4
        if Tmin < 10:
            s_max = Tmin
        else:
            s_max = Tmin - 1.5

        # If 'all' is selected, pick the first valid weld size as per IS 800:2007
        if isinstance(weld_size, str) and weld_size.lower() == 'all':
            valid_sizes = [s for s in ALL_WELD_SIZES if s_min <= s <= s_max]
            if valid_sizes:
                self.weld_size = float(valid_sizes[0])
            else:
                self.weld_size = None
        else:
            # Customized selection: could be a list of My_ListWidgetItem or direct value
            values_to_process = weld_size
            float_weld_sizes = []
            if isinstance(values_to_process, list):
                for item in values_to_process:
                    try:
                        # Handle My_ListWidgetItem or similar objects
                        if hasattr(item, 'text') and callable(item.text):
                            text_val = item.text()
                            float_weld_sizes.append(float(text_val))
                        elif isinstance(item, (str, int, float)):
                            float_weld_sizes.append(float(item))
                    except Exception:
                        continue
                # Use the first valid customized value within IS limits
                valid_custom = [s for s in float_weld_sizes if s_min <= s <= s_max]
                if valid_custom:
                    self.weld_size = float(valid_custom[0])
                else:
                    self.weld_size = None
            else:
                # Single value (customized)
                try:
                    if hasattr(values_to_process, 'text') and callable(values_to_process.text):
                        self.weld_size = float(values_to_process.text())
                    else:
                        self.weld_size = float(values_to_process)
                    # Check IS limits
                    if not (s_min <= self.weld_size <= s_max):
                        self.weld_size = None
                except Exception:
                    self.weld_size = None

        # Ensure weld_size is set before using it
        if self.weld_size is None:
            logger.error(": weld_size is not set. Cannot proceed with weld design.")
            self.design_status = False
            logger.error(": Design status: UNSAFE due to missing or invalid weld size.")
            logger.info(": =========End Of Design===========")
            return False
        logger.info(f"Selected Weld Size: {self.weld_size} (min: {s_min}, max: {s_max})")
        return True

    def _calculate_weld_strengths(self, design_dictionary):
        self.effective_throat_thickness = 0.7 * self.weld_size
        self.fu = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])
        weld_type = design_dictionary[KEY_DP_WELD_TYPE]
        if weld_type == "Shop weld":
            self.gamma_mw = 1.25
        else:
            self.gamma_mw = 1.50
        self.weld_design_strength = (self.fu * self.effective_throat_thickness) / (math.sqrt(3) * self.gamma_mw)
        self.parent_design_strength = 0.6 * self.fu * self.effective_throat_thickness / (self.gamma_mw)
        self.fillet_weld_design_strength = min(self.weld_design_strength, self.parent_design_strength)
        logger.info(f"Effective Throat Thickness: {self.effective_throat_thickness}")
        logger.info(f"Weld Material Strength (fu): {self.fu}")
        logger.info(f"Gamma_mw: {self.gamma_mw}")
        logger.info(f"Weld Design Strength: {self.weld_design_strength}")
        logger.info(f"Parent Design Strength: {self.parent_design_strength}")
        logger.info(f"Fillet Weld Design Strength (used): {self.fillet_weld_design_strength}")

    def _calculate_and_validate_weld_length(self):
        self.weld_length_effective = self.tensile_force / (2 * self.fillet_weld_design_strength)
        self.leff_min = max(4 * self.weld_size, 40)
        self.leff_max = 70 * self.weld_size
        l_req = self.weld_length_effective
        l_eff_min = self.leff_min
        l_eff_max = self.leff_max
        t_t = self.effective_throat_thickness
        logger.info(f"Weld Length Effective: {self.weld_length_effective}")
        logger.info(f"leff_min: {self.leff_min}, leff_max: {self.leff_max}")
        # Decision: Is l_req >= l_eff_min?
        if l_req >= l_eff_min:
            # Is l_req <= l_eff_max?
            if l_req <= l_eff_max:
                l_eff = l_req
            else:
                logger.error(": Required weld length exceeds maximum allowed. Increase weld size.")
                self.design_status = False
                return False
        else:
            l_eff = l_eff_min
        self.l_eff = l_eff
        self._l_req = l_req
        self._l_eff_max = l_eff_max
        self._t_t = t_t
        return True

    def _apply_long_joint_reduction_and_check(self):
        l_eff = self.l_eff
        l_req = self._l_req
        l_eff_max = self._l_eff_max
        t_t = self._t_t
        logger.info(f"l_eff: {l_eff}, l_req: {l_req}, l_eff_max: {l_eff_max}, t_t: {t_t}")
        if l_eff > 150 * t_t:
            beta_lw = 1.2 - 0.2 * (l_eff / (150 * t_t))
            beta_lw = max(0.6, min(beta_lw, 1.0))  # Subject to 0.6 ≤ β_lw ≤ 1.0
            logger.info(f"Long Joint Reduction beta_lw: {beta_lw}")
            if beta_lw < 1.0:
                l_req_modified = l_req / beta_lw
                logger.info(f"l_req_modified (after beta_lw): {l_req_modified}")
                if l_req_modified <= l_eff_max:
                    l_eff = l_req_modified
                    self.l_eff = l_eff
                    self.beta_lw = beta_lw
                    self.end_return_length = max(2 * self.weld_size, 12)
                    self.connection_length = self.l_eff + 2 * self.end_return_length
                    clearance = 0  # Update if clearance is required
                    self.overlap_length = self.connection_length + clearance
                    self.design_capacity = 2 * self.l_eff * self.fillet_weld_design_strength * self.beta_lw
                    self.utilization_ratio = self.tensile_force / self.design_capacity if self.design_capacity > 0 else float('inf')
                    if self.utilization_ratio >= 1.0:
                        logger.error(": Design Unsafe. Increase weld size or length.")
                        self.design_status = False
                        return False
                    else:
                        self.design_status = True
                        logger.info(f"Connection Length: {self.connection_length}")
                        logger.info(f"Design Capacity: {self.design_capacity}")
                        logger.info(f"Utilization Ratio: {self.utilization_ratio}")
                else:
                    logger.error(": Modified required weld length exceeds maximum allowed. Increase weld size.")
                    self.design_status = False
                    return False
            else:
                self.beta_lw = 1.0
                self.end_return_length = max(2 * self.weld_size, 12)
                self.connection_length = self.l_eff + 2 * self.end_return_length
                clearance = 0
                self.overlap_length = self.connection_length + clearance
                self.design_capacity = 2 * self.l_eff * self.fillet_weld_design_strength * self.beta_lw
                self.utilization_ratio = self.tensile_force / self.design_capacity if self.design_capacity > 0 else float('inf')
                if self.utilization_ratio >= 1.0:
                    logger.error(": Design Unsafe. Increase weld size or length.")
                    self.design_status = False
                    return False
                else:
                    self.design_status = True
                    logger.info(f"Connection Length: {self.connection_length}")
                    logger.info(f"Design Capacity: {self.design_capacity}")
                    logger.info(f"Utilization Ratio: {self.utilization_ratio}")
        else:
            self.beta_lw = 1.0
            self.end_return_length = max(2 * self.weld_size, 12)
            self.connection_length = self.l_eff + 2 * self.end_return_length
            clearance = 0
            self.overlap_length = self.connection_length + clearance
            self.design_capacity = 2 * self.l_eff * self.fillet_weld_design_strength * self.beta_lw
            self.utilization_ratio = self.tensile_force / self.design_capacity if self.design_capacity > 0 else float('inf')
            if self.utilization_ratio >= 1.0:
                logger.error(": Design Unsafe. Increase weld size or length.")
                self.design_status = False
                return False
            else:
                self.design_status = True
                logger.info(f"Connection Length: {self.connection_length}")
                logger.info(f"Design Capacity: {self.design_capacity}")
                logger.info(f"Utilization Ratio: {self.utilization_ratio}")
        return True

    
    ################################ Outlist Dict #####################################################################################

    

    ################################ Design Report #####################################################################################