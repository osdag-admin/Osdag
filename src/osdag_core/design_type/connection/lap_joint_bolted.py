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
from ...custom_logger import CustomLogger
import logging

import math
import os
from pylatex.utils import NoEscape

class LapJointBolted(MomentConnection):
    def __init__(self):
        super(LapJointBolted, self).__init__()
        self.design_status = False
        self.design_for = 'Tension'
        self.axial_force_kN = 0.0
        self.axial_force = 0.0
        self.base_metal_capacity_kN = None
        self.utilization_breakdown = {}
        self.design_error = ''
        self.hover_dict = {}
        
        # Initialize bolt placeholder - will be replaced in set_input_values
        self.bolt = None
        # Initialize attributes needed for output_values before design runs
        self.rows = 0
        self.cols = 0
        self.number_bolts = 0
        self.len_conn = 0
        self.slip_res = None
        self.utilization_ratio = 0
        # NOTE: Don't initialize self.spacing = None here - it would shadow the spacing() method!
        # Initialize plate placeholders for output_values hover dict
        self.plate1 = None
        self.plate2 = None

    ###############################################
    # Design Preference Functions Start
    ###############################################

    def tab_list(self):
        tabs = []
        # Only Bolt and Detailing tabs
        tabs.append(("Bolt", TYPE_TAB_2, self.bolt_values))
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
        tabs.append(("Design", TYPE_TAB_2, self.design_values))
        return tabs

    def tab_value_changed(self):
        # No tab value dependencies needed for bolt and detailing
        return []

    def edit_tabs(self):
        return []  # Keep original empty implementation

    def input_dictionary_design_pref(self):
        design_input = []
        
        # Bolt preferences
        design_input.append(("Bolt", TYPE_COMBOBOX, [
            KEY_DP_BOLT_TYPE,  # For pretensioned/non-pretensioned
            KEY_DP_BOLT_HOLE_TYPE,  # For standard/oversized
            KEY_DP_BOLT_SLIP_FACTOR  # For slip factor as per Table 20
        ]))
        
        # Detailing preferences
        design_input.append(("Detailing", TYPE_COMBOBOX, [
            KEY_DP_DETAILING_EDGE_TYPE  # For edge preparation method
        ]))

        # Design preferences
        design_input.append(("Design", TYPE_COMBOBOX, [
            KEY_DESIGN_FOR
        ]))
        
        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        
        # Default values for bolt and detailing
        design_input.append((None, [
            KEY_DP_BOLT_TYPE,
            KEY_DP_BOLT_HOLE_TYPE, 
            KEY_DP_BOLT_SLIP_FACTOR,
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DESIGN_FOR
        ], ''))
        
        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):
        # Default values as per requirements
        defaults = {
            KEY_DP_BOLT_TYPE: "Non Pre-tensioned",
            KEY_DP_BOLT_HOLE_TYPE: "Standard",
            KEY_DP_BOLT_SLIP_FACTOR: "0.3",
            KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
            KEY_DESIGN_FOR: 'Tension'
        }
        return defaults.get(key)

    def design_values(self, input_dictionary):
        values = {
            KEY_DESIGN_FOR: 'Tension'
        }

        if input_dictionary and KEY_DESIGN_FOR in input_dictionary:
            values[KEY_DESIGN_FOR] = input_dictionary[KEY_DESIGN_FOR]

        design = []
        t1 = (KEY_DESIGN_FOR, KEY_DISP_DESIGN_FOR, TYPE_COMBOBOX,
              ['Tension', 'Compression'], values[KEY_DESIGN_FOR])
        design.append(t1)

        return design

    def detailing_values(self, input_dictionary):
        values = {
            KEY_DP_DETAILING_EDGE_TYPE: 'Sheared or hand flame cut'
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
    
    ####################################
    # Design Preference Functions End
    ####################################

    def set_osdaglogger(self, key, id):
        """
        Function to set Logger for FinPlate Module
        """
        # @author Arsil Zunzunia

        # Set Custom logger
        logging.setLoggerClass(CustomLogger)

        # Create unique logger name per instance
        unique_logger_name = 'Osdag_lap_joint_bolted_simple_conn'
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

        t16 = (KEY_MODULE, KEY_DISP_LAPJOINTBOLTED, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t31 = (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t31)

        t34 = (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t34)

        t35 = (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None, True, 'Float Validator')
        options_list.append(t35)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_AXIAL_FORCE, KEY_DISP_AXIAL_FORCE, TYPE_TEXTBOX, None, True, 'Float Validator')
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

        return list1
    
    def spacing(self, status):
        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details - 3 x 3 pattern considered")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
            [str(files("osdag.data.ResourceFiles.images").joinpath("spacing_3.png")), 400, 277, ""])
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.final_gauge if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.final_end_dist if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.final_pitch if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.final_edge_dist if status else '')
        spacing.append(t12)

        return spacing
    
    def output_values(self, flag):
        """
        Return output field definitions for the Output Dock.
        Uses safe access pattern for attributes that may not exist before design runs.
        """
        out_list = []
        t4 = (None, DISP_TITLE_BOLTD, TYPE_TITLE, None, True)
        out_list.append(t4)

        # Safe access: check both flag and that self.bolt exists
        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,
             self.bolt.bolt_diameter_provided if flag and self.bolt else '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX,
              self.bolt.bolt_grade_provided if flag and self.bolt else '', True)
        out_list.append(t3)

        t31 = (KEY_OUT_TYP_PROVIDED, KEY_OUT_DISP_TYP_PROVIDED, TYPE_TEXTBOX,
              self.bolt.bolt_type if flag and self.bolt else '', True)
        out_list.append(t31)

        t8 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
              self.bolt.bolt_shear_capacity if flag and self.bolt else '', True)
        out_list.append(t8) 

        t4 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX,
              self.bolt.bolt_bearing_capacity if flag and self.bolt else '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
            self.bolt.bolt_capacity if flag and self.bolt else '', True)
        out_list.append(t5)

        t500 = (KEY_OUT_BOLT_SLIP, KEY_OUT_DISP_BOLT_SLIP, TYPE_TEXTBOX,
              self.slip_res if flag else '', True)
        out_list.append(t500)

        t17 = (None, DISP_TITLE_BOLTDS, TYPE_TITLE, None, True)
        out_list.append(t17)
        t17 = (KEY_OUT_TOT_NO_BOLTS, KEY_OUT_DISP_TOT_NO_BOLTS, TYPE_TEXTBOX,
               self.number_bolts if flag else '', True)
        out_list.append(t17)
        t18 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX,
               self.rows if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_COL_PROVIDED, KEY_OUT_DISP_COL_PROVIDED, TYPE_TEXTBOX,
               self.cols if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_BOLT_CONN_LEN, KEY_OUT_DISP_BOLT_CONN_LEN, TYPE_TEXTBOX,
               self.len_conn if flag else '', True)
        out_list.append(t20)

        t29 = (KEY_UTILIZATION_RATIO, KEY_DISP_UTILIZATION_RATIO, TYPE_TEXTBOX,
               self.utilization_ratio if flag else '', True)
        out_list.append(t29)

        t30 = (KEY_OUT_DESIGN_FOR, KEY_OUT_DISP_DESIGN_FOR, TYPE_TEXTBOX,
               self.design_for if flag else '', True)
        out_list.append(t30)

        t31 = (KEY_OUT_BASE_METAL_CAPACITY, KEY_OUT_DISP_BASE_METAL_CAPACITY, TYPE_TEXTBOX,
                round(self.base_metal_capacity_kN, 2) if flag and self.base_metal_capacity_kN is not None else '', True)
        out_list.append(t31)

        t32 = (KEY_OUT_BASE_METAL_UTILIZATION, KEY_OUT_DISP_BASE_METAL_UTILIZATION, TYPE_TEXTBOX,
                self.utilization_breakdown.get('base_metal') if flag and self.utilization_breakdown else '', True)
        out_list.append(t32)

        t33 = (KEY_OUT_BOLT_UTILIZATION, KEY_OUT_DISP_BOLT_UTILIZATION, TYPE_TEXTBOX,
                self.utilization_breakdown.get('bolt') if flag and self.utilization_breakdown else '', True)
        out_list.append(t33)
        
        t21 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t21)

        # Populate Hover Dict (Lap Joint Bolted)
        self.hover_dict["Plate 1"] = (
            f"<b>Plate 1</b><br>"
            f"Width: {round(float(self.plate1.height), 2) if flag and self.plate1 and self.plate1.height else ''} mm<br>"
            f"Thickness: {round(float(self.plate1.thickness_provided), 2) if flag and self.plate1 and self.plate1.thickness_provided else ''} mm"
        )

        self.hover_dict["Plate 2"] = (
            f"<b>Plate 2</b><br>"
            f"Width: {round(float(self.plate2.height), 2) if flag and self.plate2 and self.plate2.height else ''} mm<br>"
            f"Thickness: {round(float(self.plate2.thickness_provided), 2) if flag and self.plate2 and self.plate2.thickness_provided else ''} mm"
        )

        self.hover_dict["Bolt"] = (
            f"<b>Bolts</b><br>"
            f"Grade: {self.bolt.bolt_grade_provided if flag and self.bolt else ''}<br>"
            f"Diameter: {int(self.bolt.bolt_diameter_provided) if flag and self.bolt else ''} mm<br>"
            f"No. of Bolts: {self.number_bolts if flag else ''}"
        )

        return out_list
    
    @staticmethod
    def module_name():
        return KEY_DISP_LAPJOINTBOLTED
    
    def func_for_validation(self, design_dictionary):

        all_errors = []
        "check valid inputs and empty inputs in input dock"
        self.design_status = False
        flag = False
        flag1 = False
        flag2 = False

        option_list = self.input_values()
        missing_fields_list = []

        # print(f'\n func_for_validation option list = {option_list}'
        #       f'\n  design_dictionary {design_dictionary}')

        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':

                    missing_fields_list.append(option[1])
                else:
                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_PLATE_WIDTH:

                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True

                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_AXIAL_FORCE:
                        axial_val = float(design_dictionary[option[0]])
                        if math.isclose(axial_val, 0.0, abs_tol=1e-9):
                            error = "Input value for Axial Force must be non-zero."
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
        if flag  and flag1 and flag2:
            self.set_input_values(design_dictionary)
        else:
            return all_errors
        
    def set_input_values(self, design_dictionary):

        "initialisation of components required to design a lap joint for axial load (tension/compression)"

        design_dictionary_with_defaults = design_dictionary.copy()
        for key in (KEY_SHEAR, KEY_AXIAL, KEY_MOMENT):
            if key not in design_dictionary_with_defaults:
                design_dictionary_with_defaults[key] = 0.0

        super(LapJointBolted, self).set_input_values(design_dictionary_with_defaults)

        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Lap Joint Bolted Connection"
        self.main_material = design_dictionary[KEY_MATERIAL]

        self.design_for = design_dictionary.get(KEY_DESIGN_FOR, 'Tension')
        axial_input = design_dictionary.get(
            KEY_AXIAL_FORCE,
            design_dictionary.get(KEY_AXIAL,
                                  design_dictionary.get(KEY_TENSILE_FORCE, 0)))
        axial_value = float(axial_input)
        if axial_value < 0 and KEY_DESIGN_FOR not in design_dictionary:
            self.design_for = 'Compression'
        self.axial_force_kN = abs(axial_value)
        self.axial_force = self.axial_force_kN * 1000.0
        # Legacy naming issue
        self.tensile_force = self.axial_force_kN  # legacy naming in downstream methods

        self.width = float(design_dictionary[KEY_PLATE_WIDTH])
        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        self.plate1 = Plate(thickness=[plate1_thk],
                            material_grade=design_dictionary[KEY_MATERIAL], width=self.width)
        self.plate2 = Plate(thickness=[plate2_thk],
                            material_grade=design_dictionary[KEY_MATERIAL], width=self.width)
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         )
        self.planes = 1
        self.count = 0
        self.slip_res = None
        self.yield_stress = None
        self.number_bolts = 0  # Initialize to prevent AttributeError if design fails early
        self.cap_red = False
        self.bolt_dia_grade_status = False
        self.dia_available = False
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
        self.base_metal_capacity_kN = None
        self.utilization_breakdown = {}
        self.design_error = ''
        self.select_bolt_dia_and_grade(design_dictionary)

    def select_bolt_dia_and_grade(self,design_dictionary):
        self.dia_available = False
        self.bolt_dia_grade_status = False

        if isinstance(self.plate1.thickness, list):
            self.plate1thk = self.plate1.thickness[0]

        if isinstance(self.plate2.thickness, list):
            self.plate2thk = self.plate2.thickness[0]

        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((float(self.plate1thk), self.plate1.fu, self.plate1.fy))
        self.bolt_conn_plates_t_fu_fy.append((float(self.plate2thk), self.plate2.fu, self.plate2.fy))

        if float(self.plate1thk) < float(self.plate2thk):
            self.plate = self.plate1
            self.pltthk = float(self.plate1thk)
            self.yield_stress = self.plate1.fy
        else:
            self.plate = self.plate2
            self.pltthk = float(self.plate2thk)
            self.yield_stress = self.plate2.fy

        for self.bolt.bolt_diameter_provided in self.bolt.bolt_diameter:
            if 8 * float(self.bolt.bolt_diameter_provided) > (float(self.plate1thk) + float(self.plate2thk)):
                self.dia_available = True
                
                for self.bolt.bolt_grade_provided in self.bolt.bolt_grade:
                    
                    self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                                                        conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,n=self.planes)
                    
                    # self.max_pitch_round = self.max_gauge_round = 
                    # self.bolt.calculate_bolt_capacity(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                    #                           bolt_grade_provided=float(self.bolt.bolt_grade_provided),
                    #                           conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                    #                           n_planes=self.planes, e=float(self.bolt.min_end_dist_round),
                    #                           p=float(self.bolt.min_pitch_round))
                    # self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                    #                                               bolt_grade_provided=self.bolt.bolt_grade_provided)
                    # print("fnafnafan",self.bolt.bolt_capacity)
                    # NOTE: calculate_bolt_spacing_limits() already correctly implements IS 800:2007:
                    # - Cl. 10.2.2: min_pitch = 2.5 × d
                    # - Cl. 10.2.4.2: min_edge/end_dist = 1.7 × d₀ (sheared) or 1.5 × d₀ (machine cut)
                    # where d₀ = hole diameter (not bolt diameter)
                    # No manual overrides needed - the IS800_2007 utility functions are correct.

                    # Maximum pitch per Cl. 10.2.3.1: min(32t, 300mm)
                    self.max_pitch_round = self.max_gauge_round = min(32 * self.pltthk, 300)

                    # Maximum edge/end distance per Cl. 10.2.4.3: 12tε where ε = √(250/fy)
                    epsilon = math.sqrt(250 / self.yield_stress)
                    self.bolt.max_edge_dist_round = self.bolt.max_end_dist_round = round(
                        min(self.bolt.max_edge_dist_round, 12 * self.pltthk * epsilon), 0)                
                    self.bolt.calculate_bolt_capacity(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                                              bolt_grade_provided=float(self.bolt.bolt_grade_provided),
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=self.planes, e=float(self.bolt.min_end_dist_round),
                                              p=float(self.bolt.min_pitch_round))
                    num_bolts = float(self.tensile_force) / ( self.bolt.bolt_capacity / 1000)
                    # print("num_bolts",num_bolts)    
                    
                    if num_bolts <= 2:
                        self.bolt_dia_grade_status = True
                        break
                    
                    
                if self.bolt_dia_grade_status == True:
                    break 

        if self.dia_available == False:
            self.design_status = False
            self.logger.warning(" : The combined thickness ({} mm) exceeds the allowable large grip limit check (of {} mm) for the minimum available "
                           "bolt diameter of {} mm [Ref. Cl.10.3.3.2, IS 800:2007]."
                           .format((float(self.plate1thk) + float(self.plate2thk)),(8*self.bolt.bolt_diameter[-1]),self.bolt.bolt_diameter[-1]))
            self.logger.error(": Design is not safe. \n ")
            self.logger.info(" :=========End Of design===========")

        # elif self.dia_available == True and self.bolt_dia_grade_status == False:
        #     self.design_status = True
        #     if self.bolt.bolt_type == 'Bearing Bolt':
        #         self.bolt.bolt_bearing_capacity = round(float(self.bolt.bolt_bearing_capacity),2)
        #     self.bolt.bolt_shear_capacity = round(float(self.bolt.bolt_shear_capacity),2)
        #     self.bolt.bolt_capacity = round(float(self.bolt.bolt_capacity),2)       
        #     print(self.bolt)
        #     self.number_r_c_bolts(self, design_dictionary)

        
        else:
            self.design_status = True
            if self.bolt.bolt_type == 'Bearing Bolt':
                self.bolt.bolt_bearing_capacity = round(float(self.bolt.bolt_bearing_capacity),2)
            self.bolt.bolt_shear_capacity = round(float(self.bolt.bolt_shear_capacity),2)
            self.bolt.bolt_capacity = round(float(self.bolt.bolt_capacity),2)       
            # print(self.bolt)
            self.number_r_c_bolts(design_dictionary,0,0)


    def number_r_c_bolts(self, design_dictionary, count=0, hit=0):
        """
        Calculate bolt layout (rows x cols) using deterministic algorithm.
        
        Per IS 800:2007:
        - min_pitch/gauge: Cl. 10.2.2 (2.5d)
        - min_end_dist: Cl. 10.2.4.2 (1.7d₀ or 1.5d₀)
        - max_pitch: Cl. 10.2.3.1 (min(32t, 300mm))
        - max_end_dist: Cl. 10.2.4.3 (12tε)
        """
        bolt_cap = self.bolt.bolt_capacity
        if self.bolt.bolt_type == 'Bearing Bolt':
            self.slip_res = 'N/A'
        else:
            self.slip_res = self.bolt.bolt_capacity
            self.bolt.bolt_bearing_capacity = 'N/A'
            self.bolt.bolt_shear_capacity = 'N/A'

        # Calculate required number of bolts
        if hit == 0:
            self.number_bolts = float(self.tensile_force) / (bolt_cap / 1000)
        else:
            self.number_bolts += 1

        self.number_bolts = math.ceil(self.number_bolts)
        if self.number_bolts < 2:
            self.number_bolts = 2

        # === DETERMINISTIC LAYOUT ALGORITHM ===
        # Step 1: Calculate available width for bolts (after deducting end distances)
        min_end_dist = self.bolt.min_end_dist_round
        min_gauge = self.bolt.min_gauge_round
        max_gauge = self.max_gauge_round
        max_end_dist = self.bolt.max_end_dist_round
        plate_width = float(self.width)

        available_width = plate_width - 2 * min_end_dist

        # Step 2: Check if plate width is sufficient
        if available_width < 0:
            self.design_status = False
            self.logger.error(f": Design Failed - Plate width ({plate_width} mm) is too small. "
                            f"Minimum required = {2 * min_end_dist} mm (2 × min_end_dist per Cl. 10.2.4.2)")
            self.logger.info(" :=========End Of design===========")
            self.design_error = "Plate width is too small for bolt arrangement."
            return

        # Step 3: Calculate maximum bolts that can fit in one row (gauge direction)
        if available_width >= min_gauge:
            max_bolts_per_row = int(available_width / min_gauge) + 1
        else:
            # Only one bolt can fit per row
            max_bolts_per_row = 1

        # Step 4: Calculate optimal rows and columns
        if self.number_bolts <= max_bolts_per_row:
            # All bolts fit in one row
            self.rows = self.number_bolts
            self.cols = 1
        else:
            # Need multiple columns (pitch direction)
            self.rows = max_bolts_per_row
            self.cols = math.ceil(self.number_bolts / self.rows)
            # Rebalance to minimize empty spaces
            self.rows = math.ceil(self.number_bolts / self.cols)

        # Ensure minimum of 2 bolts
        if self.rows * self.cols < 2:
            self.rows = 2
            self.cols = 1

        # Step 5: Calculate actual gauge distance
        if self.rows > 1:
            actual_gauge = available_width / (self.rows - 1)
        else:
            actual_gauge = 0

        # Step 6: Validate gauge against maximum spacing (Cl. 10.2.3.1)
        if actual_gauge > max_gauge and self.rows > 1:
            # Need more bolts per row to reduce gauge
            required_rows = math.ceil(available_width / max_gauge) + 1
            if required_rows > self.rows:
                self.rows = required_rows
                self.cols = math.ceil(self.number_bolts / self.rows)
                self.number_bolts = self.rows * self.cols
                actual_gauge = available_width / (self.rows - 1) if self.rows > 1 else 0

        # Step 7: Calculate actual end distance
        if self.rows > 1:
            actual_end_dist = (plate_width - (self.rows - 1) * min_gauge) / 2
        else:
            actual_end_dist = plate_width / 2

        # Step 8: Validate end distance against maximum (Cl. 10.2.4.3)
        if actual_end_dist > max_end_dist:
            self.logger.warning(f": End distance ({actual_end_dist:.1f} mm) exceeds maximum "
                               f"({max_end_dist} mm) per Cl. 10.2.4.3. Adding more bolts.")
            # Add more bolts to reduce end distance
            required_rows = math.ceil((plate_width - 2 * max_end_dist) / min_gauge) + 1
            if required_rows > self.rows:
                self.rows = required_rows
                self.cols = math.ceil(self.number_bolts / self.rows)
                self.number_bolts = self.rows * self.cols

        # Calculate connection length
        if self.cols > 1:
            self.len_conn = (self.cols - 1) * self.bolt.min_pitch_round + 2 * self.bolt.min_end_dist_round
        else:
            self.len_conn = self.bolt.min_pitch_round + 2 * self.bolt.min_end_dist_round

        # Continue to capacity reduction checks
        if self.number_bolts >= 2 and count == 0:
            self.design_status = True
            self.check_capacity_reduction_1(design_dictionary)
        elif self.number_bolts >= 2 and count == 1:
            self.design_status = True
            self.final_formatting(design_dictionary)
        else:
            self.design_status = False
            self.logger.error(": Number of min bolts not satisfied. \n ")
            self.logger.info(" :=========End Of design===========")


    def check_capacity_reduction_1(self,design_dictionary):
        # print("Capacity red check 1")
        if self.number_bolts > 2:
            lg = (self.rows - 1)*self.bolt.min_pitch_round
            if  lg > 15 * self.bolt.bolt_diameter_provided:
                self.bij = 1.075 - (lg / (200 * self.bolt.bolt_diameter_provided))
        if self.bij >= 0.75 and self.bij <= 1.0:
            self.cap_red = True
            # print("1 cap red")
            self.bolt.bolt_shear_capacity = self.bolt.bolt_shear_capacity * self.bij
            if self.bolt.bolt_type == 'Bearing Bolt':
                self.bolt.bolt_capacity = min(self.bolt.bolt_shear_capacity, self.bolt.bolt_bearing_capacity)
            else:
                self.slip_res = self.bolt.bolt_shear_capacity
                self.bolt.bolt_capacity = self.slip_res


        self.design_status = True
        self.check_capacity_reduction_2(design_dictionary)

    def check_capacity_reduction_2(self,design_dictionary):
        self.cap_red = False
        # print("Capacity red check 2")
        if self.plate1thk + self.plate2thk > 5 * self.bolt.bolt_diameter_provided:
            self.blg = 8 / (3 + (self.plate1thk + self.plate2thk / self.bolt.bolt_diameter_provided))
        if self.blg < self.bij and self.blg != 0:
            self.cap_red = True
            # print("blg",self.blg)
            # print("2 cap red")
            self.bolt.bolt_shear_capacity = self.bolt.bolt_shear_capacity * self.blg
            if self.bolt.bolt_type == 'Bearing Bolt':
                self.bolt.bolt_capacity = min(self.bolt.bolt_shear_capacity, self.bolt.bolt_bearing_capacity)
            else:
                self.slip_res = self.bolt.bolt_shear_capacity
                self.bolt.bolt_capacity = self.slip_res
            
            self.number_r_c_bolts(design_dictionary,1,0)
        
        if self.cap_red == False:
            self.design_status = True
            # print("Going to formatting")
            # print("After checks 2 numbolts",self.number_bolts)
            self.final_formatting(design_dictionary)



    def final_formatting(self,design_dictionary):
        gauge_divisor = max(self.rows - 1, 1)
        gauge_dist = (float(self.width) - 2 * self.bolt.min_end_dist_round) / gauge_divisor

        if gauge_dist > self.max_gauge_round:
            self.final_gauge = self.max_gauge_round
            self.final_pitch = self.bolt.min_pitch_round

            enddist = (float(self.width) - ((self.rows - 1) * self.final_gauge)) / 2
            if enddist > self.bolt.max_end_dist_round:
                self.design_status = False
                self.number_r_c_bolts(design_dictionary, 0, 1)
                return
            else:
                self.final_end_dist = enddist
                self.final_edge_dist = enddist
                self.design_status = True
        else:
            self.final_gauge = gauge_dist
            self.final_pitch = self.bolt.min_pitch_round
            enddist = (float(self.width) - ((self.rows - 1) * self.final_gauge)) / 2
            if enddist > self.bolt.max_end_dist_round:
                self.design_status = False
                self.number_r_c_bolts(design_dictionary, 0, 1)
                return
            else:
                self.final_end_dist = enddist
                self.final_edge_dist = enddist
                self.design_status = True

        if self.bolt.bolt_type == 'Bearing Bolt':
            self.bolt.bolt_shear_capacity = round(self.bolt.bolt_shear_capacity / 1000, 2)
            self.bolt.bolt_bearing_capacity = round(self.bolt.bolt_bearing_capacity / 1000, 2)
            self.bolt.bolt_capacity = round(self.bolt.bolt_capacity / 1000, 2)
        else:
            self.slip_res = round(self.slip_res / 1000, 2)
            self.bolt.bolt_capacity = round(self.bolt.bolt_capacity / 1000, 2)

        bolt_capacity_kN = self.bolt.bolt_capacity
        bolt_capacity_total = bolt_capacity_kN * self.number_bolts if bolt_capacity_kN else 0.0
        if bolt_capacity_total <= 0:
            self.logger.error(": Bolt capacity is zero. Increase bolt size/grade or adjust layout.")
            self.design_status = False
            self.design_error = "Bolt capacity is zero."
            return
        bolt_util = self.axial_force_kN / bolt_capacity_total

        if not self.check_base_metal_strength():
            return

        if not self.base_metal_capacity_kN or self.base_metal_capacity_kN <= 0:
            self.logger.error(": Base metal capacity is zero or undefined. Check plate selection.")
            self.design_status = False
            self.design_error = "Base metal capacity is zero or undefined."
            return

        base_util = self.axial_force_kN / self.base_metal_capacity_kN

        def _format_util(value, decimals=3):
            if math.isinf(value) or math.isnan(value):
                return 'Inf'
            return round(value, decimals)

        overall_util = max(bolt_util, base_util)
        self.utilization_breakdown = {
            'bolt': _format_util(bolt_util),
            'base_metal': _format_util(base_util)
        }

        if math.isinf(overall_util) or math.isnan(overall_util):
            self.utilization_ratio = 'Inf'
        else:
            self.utilization_ratio = round(overall_util, 2)

        self.final_gauge = round(self.final_gauge, 0)
        self.final_pitch = round(self.final_pitch, 0)
        self.final_end_dist = round(self.final_end_dist, 0)
        self.final_edge_dist = round(self.final_edge_dist, 0)

        print("FINAL FINAL", self.bolt)
        print("Final Edge/End/Gauge/Pitch", self.final_edge_dist, self.final_end_dist, self.final_gauge, self.final_pitch)
        print("Max and min end edge dist ", self.bolt.max_end_dist_round, self.bolt.min_end_dist_round, self.bolt.max_edge_dist_round, self.bolt.min_edge_dist_round)
        print("Max min gauge pitch dist", self.max_gauge_round, self.bolt.min_gauge_round, self.max_pitch_round, self.bolt.min_pitch_round)

        # Set plate dimensions for hover_dict display
        # plate length = connection length (along the bolt pitch direction)
        # plate height = plate width (perpendicular to pitch direction)
        plate_length = self.len_conn
        plate_width = float(self.width)
        
        # Plate 1 dimensions
        self.plate1.length = plate_length
        self.plate1.height = plate_width
        self.plate1.thickness_provided = float(self.plate1thk)
        
        # Plate 2 dimensions
        self.plate2.length = plate_length
        self.plate2.height = plate_width
        self.plate2.thickness_provided = float(self.plate2thk)
        
        # Store spacing values on main plate for output compatibility
        self.plate.pitch_provided = self.final_pitch
        self.plate.gauge_provided = self.final_gauge
        self.plate.edge_dist_provided = self.final_edge_dist
        self.plate.end_dist_provided = self.final_end_dist
        
    def check_base_metal_strength(self):
        
        try:
            self.logger
        except NameError:
            self.logger = logging.getLogger('Osdag')

        self.logger.info(": ============== Base Metal Strength Check ==============")

        plate_thk_min = min(float(self.plate1thk), float(self.plate2thk))
        fy = min(self.plate1.fy, self.plate2.fy)
        fu = min(self.plate1.fu, self.plate2.fu)

        self.gamma_m0 = 1.10
        self.gamma_m1 = 1.25

        self.A_g = plate_thk_min * float(self.width)

        if self.design_for == 'Compression':
            self.T_db = self.A_g * fy / self.gamma_m0
            self.logger.info(f": Design strength of plate in compression = {self.T_db / 1000:.2f} kN [Cl.7.1.2]")
        else:
            n_holes = max(self.rows, 1)
            hole_dia = self.bolt.dia_hole if hasattr(self.bolt, 'dia_hole') else 0.0
            net_width = float(self.width) - n_holes * hole_dia

            if net_width <= 0:
                self.logger.error(": Net width becomes zero/negative after deducting bolt holes. Increase plate width or reduce rows.")
                self.design_status = False
                self.design_error = "Net width insufficient for bolt holes."
                return False

            self.A_n = plate_thk_min * net_width
            shear_lag_factor = 0.7  # IS 800:2007 Cl.6.3.3 for lap joints

            T_dg = self.A_g * fy / self.gamma_m0
            T_dn = 0.9 * self.A_n * fu * shear_lag_factor / self.gamma_m1
            self.T_dg = T_dg
            self.T_dn = T_dn
            self.T_db = min(T_dg, T_dn)

            # Calculate block shear strength
            A_vg = plate_thk_min * ((self.rows - 1) * self.final_gauge + self.final_edge_dist)
            A_vn = plate_thk_min * ((self.rows - 1) * self.final_gauge + self.final_edge_dist - (self.rows - 0.5) * hole_dia)
            A_tg = plate_thk_min * self.final_end_dist
            A_tn = plate_thk_min * (self.final_end_dist - 0.5 * hole_dia)

            T_db_block = IS800_2007.cl_6_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, fu, fy)
            self.T_db = min(self.T_db, T_db_block)
            self.logger.info(f": Design strength of plate in tension = {self.T_db / 1000:.2f} kN [Cl.6.2.2, 6.2.3, 6.3.3]")

        if self.T_db <= 0:
            self.logger.error(": Plate design strength is non-positive. Check input dimensions/material.")
            self.design_status = False
            self.design_error = "Plate design strength is non-positive."
            return False

        self.base_metal_capacity_kN = self.T_db / 1000.0
        return True

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Plate 1', self.call_3DPlate1)
        components.append(t2)

        t3 = ('Plate 2', self.call_3DPlate2)
        components.append(t3)

        t4 = ('Bolts', self.call_3DBolt)
        components.append(t4)

        return components

    def call_3DPlate1(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Plate 1':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Plate 1", bgcolor)

    def call_3DPlate2(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Plate 2':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Plate 2", bgcolor)
    
    def call_3DBolt(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Bolts':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Bolts", bgcolor)
    
    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from Column and Beams table.
        """

        # @author Arsil Zunzunia
        red_list = red_list_function()
        if self.supported_section.designation in red_list or self.supporting_section.designation in red_list:
            self.logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            self.logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def save_design(self, popup_summary):
        """
        Generate the LaTeX design report for Lap Joint Bolted Connection (Tension/Compression)
        per IS 800:2007.
        """
        try:
            def g(attr, default=None):
                v = getattr(self, attr, default)
                return default if v is None else v

            def f2(x, default=0.0):
                try:
                    return round(float(x), 2)
                except (TypeError, ValueError):
                    return default

            def as_int(x, default=0):
                try:
                    return int(round(float(x)))
                except (TypeError, ValueError):
                    return default

            if not getattr(self, 'design_status', False):
                self.report_input = {
                    KEY_MODULE: "Lap Joint Bolted Connection",
                    KEY_MAIN_MODULE: "Simple Connection",
                    "Design Status": "TITLE",
                    "Status": "Design not completed successfully.",
                }
                self.report_check = []
                self.report_check.append([
                    "SubSection", "Design Status", "|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|"
                ])
                self.report_check.append(["Design", "Design not completed successfully.", "", "FAIL"])
                
                Disp_2d_image = []
                Disp_3D_image = "/ResourceFiles/images/3d.png"
                rel_path = os.path.abspath(".").replace("\\", "/")
                fname_no_ext = popup_summary.get("filename", "LapJointBoltedReport")
                folder = popup_summary.get('folder', './reports')
                os.makedirs(folder, exist_ok=True)
                
                CreateLatex.save_latex(
                    CreateLatex(), self.report_input, self.report_check,
                    popup_summary, fname_no_ext, rel_path, Disp_2d_image, Disp_3D_image,
                    module=getattr(self, 'module', 'Lap Joint Bolted')
                )
                return True

            self.module = g('module', 'Lap Joint Bolted')
            self.mainmodule = 'Simple Connection'
            design_for = str(g('design_for', 'Tension')).strip()
            is_comp = design_for.lower().startswith('c')
            
            plate1_thk = f2(g('plate1thk', g('pltthk', 0.0)), 0.0)
            plate2_thk = f2(g('plate2thk', g('pltthk', 0.0)), 0.0)
            width = f2(g('width', 0.0), 0.0)
            axial_kN = f2(g('axial_force_kN', g('tensile_force', 0.0)), 0.0)
            
            edge_type = getattr(self.bolt, 'edgetype', 'Sheared or hand flame cut')
            bolt_dia_prov = f2(getattr(self.bolt, 'bolt_diameter_provided', 0.0) if hasattr(self, 'bolt') else 0.0, 0.0)
            bolt_grade_prov = f2(getattr(self.bolt, 'bolt_grade_provided', 0.0) if hasattr(self, 'bolt') else 0.0, 0.0)
            bolt_type = getattr(self.bolt, 'bolt_type', VALUE_NOT_APPLICABLE) if hasattr(self, 'bolt') else VALUE_NOT_APPLICABLE
            
            bolt_shear_kN = f2(getattr(self.bolt, 'bolt_shear_capacity', 0.0) if hasattr(self, 'bolt') else 0.0, 0.0)
            bolt_bearing_kN = f2(getattr(self.bolt, 'bolt_bearing_capacity', 0.0) if hasattr(self, 'bolt') else 0.0, 0.0)
            bolt_final_cap = f2(getattr(self.bolt, 'bolt_capacity', 0.0) if hasattr(self, 'bolt') else 0.0, 0.0)
            
            rows = as_int(g('rows', 0), 0)
            cols = as_int(g('cols', 0), 0)
            n_bolts = as_int(g('number_bolts', 0), 0)
            pitch = f2(g('final_pitch', 0.0), 0.0)
            gauge = f2(g('final_gauge', 0.0), 0.0)
            e_dist = f2(g('final_edge_dist', 0.0), 0.0)
            
            t_fu_fy_list = getattr(self, 'bolt_conn_plates_t_fu_fy', [])
            if t_fu_fy_list and len(t_fu_fy_list) > 0:
                fu = t_fu_fy_list[0][1] if len(t_fu_fy_list[0]) > 1 else 0
                fy = t_fu_fy_list[0][2] if len(t_fu_fy_list[0]) > 2 else 0
            else:
                fy = g('yield_stress', 0)
                fu = 0

            base_metal_capacity_kN = f2(g('base_metal_capacity_kN', 0.0), 0.0)
            
            A_g = f2(g('A_g', 0.0), 0.0)
            T_dg = f2(g('T_dg', 0.0), 0.0)
            T_dn = f2(g('T_dn', 0.0), 0.0)
            T_db = f2(g('T_db', 0.0), 0.0)
            
            overall_ur = round(g('utilization_ratio', 0.0), 3)

            self.report_input = {
                KEY_MODULE: "Lap Joint Bolted Connection",
                KEY_MAIN_MODULE: "Simple Connection",
                KEY_DISP_DESIGN_FOR: design_for,
                "Thickness of Plate-1 (mm) *": plate1_thk,
                "Thickness of Plate-2 (mm) *": plate2_thk,
                "Width of Plate (mm) *": width,
                "Material *": getattr(self, 'main_material', VALUE_NOT_APPLICABLE),
                "Diameter (mm) *": bolt_dia_prov,
                "Property Class *": bolt_grade_prov,
                "Type *": bolt_type,
                f"{'Tensile' if not is_comp else 'Axial'} Force (kN) *": axial_kN,
                "Additional inputs": "TITLE",
                "Bolt Hole Type": getattr(self.bolt, 'boltholetype', 'Standard'),
                "Slip Factor (μf)": getattr(self.bolt, 'mu_f', 'N/A'),
                "Edge Preparation Method": edge_type
            }

            self.report_check = []

            #=============================================================
            #=========== SECTION 2.1: CALCULATING BOLT STRENGTH ==========
            #=============================================================
            self.report_check.append([
                "SubSection", "Calculating Bolt Strength", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            d = float(self.bolt.bolt_diameter_provided)
            bolt_grade = float(self.bolt.bolt_grade_provided)
            f_ub = int(bolt_grade * 100)
            
            plate1_thk_raw = float(self.plate1.thickness[0]) if isinstance(self.plate1.thickness, list) else float(self.plate1.thickness)
            plate2_thk_raw = float(self.plate2.thickness[0]) if isinstance(self.plate2.thickness, list) else float(self.plate2.thickness)
            
            bolt_shank_area = f2(math.pi * d**2 / 4, 0.0)
            
            if hasattr(self.bolt, 'bolt_net_area_provided'):
                bolt_net_area = f2(self.bolt.bolt_net_area_provided, 0.0)
            else:
                bolt_net_area = f2(math.pi * (d - 0.9382 * math.sqrt(d))**2 / 4, 0.0)
            
            gamma_mb = 1.25

            if self.bolt.bolt_type != "Bearing Bolt":
                # ========== FRICTION GRIP TYPE BOLTING (Cl. 10.4.3) ==========
                f_0 = 0.7 * f_ub
                F_o = bolt_net_area * f_0
                mu = float(self.bolt.mu_f) if hasattr(self.bolt, 'mu_f') else 0.3
                n_e = 1  # Number of effective interfaces (single lap joint)
                
                bolt_hole_type_str = str(self.bolt.bolt_hole_type) if hasattr(self.bolt, 'bolt_hole_type') else "Standard"
                d_0 = IS800_2007.cl_10_2_1_bolt_hole_size(d, bolt_hole_type_str)
                
                hole_type_lower = bolt_hole_type_str.lower()
                if "standard" in hole_type_lower:
                    K_h = 1.0
                elif "over" in hole_type_lower or "short" in hole_type_lower:
                    K_h = 0.85
                else:  # long slotted
                    K_h = 0.7

                V_nsf = mu * n_e * K_h * F_o
                gamma_mf = 1.25  # For ultimate load
                V_dsf_theoretical = V_nsf / gamma_mf
                V_dsf_kN_theoretical = V_dsf_theoretical / 1000
                
                slip_req = Math(inline=True)
                slip_req.append(NoEscape(r'\begin{aligned}'))
                slip_req.append(NoEscape(r'V_{dsf} &= \frac{V_{nsf}}{\gamma_{mf}}\\'))
                slip_req.append(NoEscape(r'V_{nsf} &= \mu \cdot n_e \cdot K_h \cdot F_o\\'))
                slip_req.append(NoEscape(r'\mu &= ' + f'{mu:.2f}' + r' \text{ (slip factor)}\\'))
                slip_req.append(NoEscape(r'n_e &= ' + str(n_e) + r' \text{ (interfaces)}\\'))
                slip_req.append(NoEscape(r'K_h &= ' + f'{K_h:.2f}' + r' \text{ (hole factor)}\\'))
                slip_req.append(NoEscape(r'f_0 &= 0.7 f_{ub} = ' + f'{f_0:.1f}' + r' \text{ MPa}\\'))
                slip_req.append(NoEscape(r'A_{nb} &= ' + f'{bolt_net_area:.2f}' + r' \text{ mm}^2\\'))
                slip_req.append(NoEscape(r'F_o &= A_{nb} \times f_0 = ' + f'{F_o:.2f}' + r' \text{ N}\\'))
                slip_req.append(NoEscape(r'V_{nsf} &= ' + f'{mu:.2f}' + r' \times ' + str(n_e) + r' \times ' + f'{K_h:.2f}' + r' \times ' + f'{F_o:.2f}' + r'\\'))
                slip_req.append(NoEscape(r'&= ' + f'{V_nsf:.2f}' + r' \text{ N}\\'))
                slip_req.append(NoEscape(r'V_{dsf} &= \frac{' + f'{V_nsf:.2f}' + r'}{' + str(gamma_mf) + r'} = ' + f'{V_dsf_kN_theoretical:.2f}' + r' \text{ kN}\\'))
                slip_req.append(NoEscape(r'&[\text{Ref. Cl. 10.4.3}]'))
                slip_req.append(NoEscape(r'\end{aligned}'))
                
                self.report_check.append(["Slip Resistance", "", slip_req, ""])

            else:  # Bearing Bolt
                # ========== SHEAR CAPACITY (Cl. 10.3.3) ==========
                V_dsb_kN = bolt_shear_kN
                V_nsb = V_dsb_kN * gamma_mb
                
                n_n = 1  # Threads intercepting shear plane
                n_s = 0  # No threads without shear
                
                shear_req = Math(inline=True)
                shear_req.append(NoEscape(r'\begin{aligned}\\'))
                shear_req.append(NoEscape(r'V_{dsb} &= \frac{V_{nsb}}{\gamma_{mb}}\\\\'))
                shear_req.append(NoEscape(r'V_{nsb} &= \frac{f_{ub}}{\sqrt{3}} \cdot (n_n \cdot A_{nb} + n_s \cdot A_{sb})\\'))
                shear_req.append(NoEscape(r'&= \frac{' + str(f_ub) + r'}{\sqrt{3}} \times (1 \times ' + f'{bolt_net_area:.2f}' + r')\\'))
                shear_req.append(NoEscape(r'&= ' + f'{V_nsb:.2f}' + r' \text{ kN}\\\\'))
                shear_req.append(NoEscape(r'V_{dsb} &= \frac{' + f'{V_nsb:.2f}' + r'}{' + str(gamma_mb) + r'}\\'))
                shear_req.append(NoEscape(r'&= ' + f'{V_dsb_kN:.2f}' + r' \text{ kN}\\'))
                shear_req.append(NoEscape(r'&[\text{Ref. Cl. 10.3.3}]'))
                shear_req.append(NoEscape(r'\end{aligned}'))
                
                self.report_check.append(["Shear Capacity", "", shear_req, ""])

                # ========== BEARING CAPACITY (Cl. 10.3.4) ==========
                V_dpb_kN = bolt_bearing_kN 
                V_npb = V_dpb_kN * gamma_mb 
                
                t_min = min(plate1_thk_raw, plate2_thk_raw)
                f_u_plate = min(self.plate1.fu, self.plate2.fu)
                
                bolt_hole_type_str = str(self.bolt.bolt_hole_type) if hasattr(self.bolt, 'bolt_hole_type') else "Standard"
                d_0 = IS800_2007.cl_10_2_1_bolt_hole_size(d, bolt_hole_type_str)
                
                e = float(self.final_end_dist) if hasattr(self, 'final_end_dist') and self.final_end_dist > 0 else float(self.bolt.min_end_dist_round)
                p = float(self.final_pitch) if hasattr(self, 'final_pitch') and self.final_pitch > 0 else float(self.bolt.min_pitch_round)
                
                # Calculate kb factor components (always calculate for report display)
                if p > 0:
                    kb_1 = e / (3.0 * d_0)
                    kb_2 = p / (3.0 * d_0) - 0.25
                    kb_3 = f_ub / f_u_plate
                    kb_4 = 1.0
                    kb_calc = min(kb_1, kb_2, kb_3, kb_4)
                else:
                    kb_1 = e / (3.0 * d_0)
                    kb_2 = float('inf')  # Not applicable
                    kb_3 = f_ub / f_u_plate
                    kb_4 = 1.0
                    kb_calc = min(kb_1, kb_3, kb_4)

                if hasattr(self.bolt, 'kb') and self.bolt.kb is not None:
                    k_b = f2(self.bolt.kb, 1.0)
                else:
                    k_b = f2(kb_calc, 1.0)
                
                kb_req = Math(inline=True)
                kb_req.append(NoEscape(r'\begin{aligned}\\'))
                kb_req.append(NoEscape(r'k_b &= \min\left(\frac{e}{3d_0}, \frac{p}{3d_0}-0.25, \frac{f_{ub}}{f_u}, 1.0\right)\\\\'))
                kb_req.append(NoEscape(r'&= \min\left(\frac{' + f'{e:.1f}' + r'}{3 \times ' + f'{d_0:.1f}' + r'}, \frac{' + f'{p:.1f}' + r'}{3 \times ' + f'{d_0:.1f}' + r'}-0.25, \frac{' + str(f_ub) + r'}{' + str(f_u_plate) + r'}, 1.0\right)\\\\'))
                
                if p > 0:
                    kb_req.append(NoEscape(r'&= \min(' + f'{kb_1:.2f}' + r', ' + f'{kb_2:.2f}' + r', ' + f'{kb_3:.2f}' + r', 1.0)\\\\'))
                else:
                    kb_req.append(NoEscape(r'&= \min(' + f'{kb_1:.2f}' + r', ' + f'{kb_3:.2f}' + r', 1.0)\\\\'))
                
                kb_req.append(NoEscape(r'&= ' + f'{k_b:.2f}'))
                kb_req.append(NoEscape(r'\end{aligned}'))
                self.report_check.append(["Bearing Factor", "", kb_req, ""])
                
                bearing_req = Math(inline=True)
                bearing_req.append(NoEscape(r'\begin{aligned}'))
                bearing_req.append(NoEscape(r'V_{dpb} &= \frac{V_{npb}}{\gamma_{mb}}\\\\'))
                bearing_req.append(NoEscape(r'V_{npb} &= 2.5 \cdot k_b \cdot d \cdot t \cdot f_u\\'))
                bearing_req.append(NoEscape(r'&= 2.5 \times ' + f'{k_b:.3f}' + r' \times ' + f'{d:.1f}' + r' \times ' + f'{t_min:.1f}' + r' \times ' + str(f_u_plate) + r'\\'))
                bearing_req.append(NoEscape(r'&= ' + f'{V_npb:.2f}' + r' \text{ kN}\\\\'))
                bearing_req.append(NoEscape(r'V_{dpb} &= \frac{' + f'{V_npb:.2f}' + r'}{' + f'{gamma_mb:.2f}' + r'}\\'))
                bearing_req.append(NoEscape(r'&= ' + f'{V_dpb_kN:.2f}' + r' \text{ kN}\\'))
                bearing_req.append(NoEscape(r'&[\text{Ref. Cl. 10.3.4}]'))
                bearing_req.append(NoEscape(r'\end{aligned}'))
                
                self.report_check.append(["Bearing Capacity", "", bearing_req, ""])

                V_db_kN = bolt_final_cap
                
                cap_req = Math(inline=True)
                cap_req.append(NoEscape(r'\begin{aligned}'))
                cap_req.append(NoEscape(r'V_{db} &= \min(' + f'{bolt_shear_kN:.2f}' + r', ' + f'{bolt_bearing_kN:.2f}' + r')'+r'\\'))
                cap_req.append(NoEscape(r'&= ' + f'{V_db_kN:.2f}' + r' \text{ kN}'+r'\\'))
                cap_req.append(NoEscape(r'&[\text{Ref. Cl. 10.3.2, IS 800:2007}]'))
                cap_req.append(NoEscape(r'\end{aligned}'))
                
                self.report_check.append(["Bolt Design Capacity", "", cap_req, ""])

            #=======================================================
            #=========== SECTION 2.2: REDUCTION FACTORS ============
            #=======================================================
            self.report_check.append([
                "SubSection", "Reduction Factors", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            l_j = (self.rows - 1) * self.final_pitch if self.rows > 1 else 0
            d = self.bolt.bolt_diameter_provided
            
            lj_req = Math(inline=True)
            lj_req.append(NoEscape(r'\begin{aligned}'))
            
            if l_j > 15 * d:
                beta_lj = 1.075 - (l_j / (200 * d))
                beta_lj = max(0.75, min(beta_lj, 1.0))
                lj_req.append(NoEscape(r'\text{Since } l_j &> 15d\\'))
                lj_req.append(NoEscape(r'l_j &= ' + str(l_j) + r' \text{ mm}, \quad 15d = ' + str(15 * d) + r' \text{ mm}\\'))
                lj_req.append(NoEscape(r'\beta_{lj} &= 1.075 - \frac{l_j}{200 \cdot d}\\'))
                lj_req.append(NoEscape(r'&= 1.075 - \frac{' + str(l_j) + r'}{200 \times ' + str(d) + r'}\\'))
                lj_req.append(NoEscape(r'&= ' + f'{1.075 - (l_j / (200 * d)):.3f}' + r'\\'))
                lj_req.append(NoEscape(r'&\text{(but } 0.75 \leq \beta_{lj} \leq 1.0\text{)}\\'))
                lj_req.append(NoEscape(r'\beta_{lj} &= ' + f'{beta_lj:.2f}' + r'\\'))
                lj_status = ""
            else:
                beta_lj = 1.0
                lj_req.append(NoEscape(r'\text{Since } l_j &\leq 15d\\'))
                lj_req.append(NoEscape(r'l_j &= ' + str(l_j) + r' \text{ mm}, \quad 15d = ' + str(15 * d) + r' \text{ mm}\\'))
                lj_req.append(NoEscape(r'\beta_{lj} &= 1.0 \text{ (No reduction)}\\'))
                lj_status = "PASS"
            
            lj_req.append(NoEscape(r'&[\text{Ref. Cl. 10.3.3.1}]'))
            lj_req.append(NoEscape(r'\end{aligned}'))
            
            lj_prov = Math(inline=True)
            lj_prov.append(NoEscape(r'\beta_{lj} = ' + f'{beta_lj:.2f}'))
            
            self.report_check.append(["Long Joint Factor", '', lj_prov, ''])

            l_g = plate1_thk_raw + plate2_thk_raw
            
            lg_req = Math(inline=True)
            lg_req.append(NoEscape(r'\begin{aligned}'))
            
            if l_g > 5 * d:
                beta_lg = (8 * d) / (3 * d + l_g)
                beta_lg = min(beta_lg, beta_lj) if beta_lj else beta_lg
                lg_req.append(NoEscape(r'\text{Since } l_g &> 5d\\'))
                lg_req.append(NoEscape(r'l_g &= ' + str(l_g) + r' \text{ mm}, \quad 5d = ' + str(5 * d) + r' \text{ mm}\\'))
                lg_req.append(NoEscape(r'\beta_{lg} &= \frac{8d}{3d + l_g}\\'))
                lg_req.append(NoEscape(r'&= \frac{8 \times ' + str(d) + r'}{3 \times ' + str(d) + r' + ' + str(l_g) + r'}\\'))
                lg_req.append(NoEscape(r'&= ' + f'{(8 * d) / (3 * d + l_g):.3f}' + r'\\'))
                lg_req.append(NoEscape(r'\beta_{lg} &\leq \beta_{lj}\\'))
                lg_req.append(NoEscape(r'\beta_{lg} &= ' + f'{beta_lg:.2f}' + r'\\'))
                lg_status = ""
            else:
                beta_lg = 1.0
                lg_req.append(NoEscape(r'\text{Since } l_g &\leq 5d\\'))
                lg_req.append(NoEscape(r'l_g &= ' + str(l_g) + r' \text{ mm}, \quad 5d = ' + str(5 * d) + r' \text{ mm}\\'))
                lg_req.append(NoEscape(r'\beta_{lg} &= 1.0 \text{ (No reduction)}\\'))
                lg_status = "PASS"
            
            lg_req.append(NoEscape(r'&[\text{Ref. Cl. 10.3.3.2}]'))
            lg_req.append(NoEscape(r'\end{aligned}'))
            
            lg_prov = Math(inline=True)
            lg_prov.append(NoEscape(r'\beta_{lg} = ' + f'{beta_lg:.2f}'))
            
            self.report_check.append(["Large Grip Factor", '', lg_prov, ''])

            if self.bolt.bolt_hole_type != "Standard":
                hole_req = Math(inline=True)
                hole_req.append(NoEscape(r'\begin{aligned}'))
                hole_req.append(NoEscape(r'\text{Hole Type: }' + self.bolt.bolt_hole_type + r'\\'))
                if "oversized" in self.bolt.bolt_hole_type.lower() or "short" in self.bolt.bolt_hole_type.lower():
                    hole_factor = 0.7
                else:  # long-slotted
                    hole_factor = 0.5
                hole_req.append(NoEscape(r'\text{Reduction Factor} &= ' + str(hole_factor) + r'\\'))
                hole_req.append(NoEscape(r'&[\text{Ref. Cl. 10.3.4}]'))
                hole_req.append(NoEscape(r'\end{aligned}'))
                self.report_check.append(["Hole Type Reduction", hole_req, "", ""])

            #=====================================
            # Section 2.3: Detailing Requirements
            #=====================================
            self.report_check.append([
                "SubSection", "Detailing Requirements", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            # 2.3.1 Minimum Spacing (Cl. 10.2.2)
            p_min = as_int(2.5 * bolt_dia_prov, 0)
            g_min = as_int(2.5 * bolt_dia_prov, 0)
            
            spacing_req = Math(inline=True)
            spacing_req.append(NoEscape(r'\begin{aligned}'))
            spacing_req.append(NoEscape(r'p_{\text{min}} &= 2.5 \cdot d\\'))
            spacing_req.append(NoEscape(r'&= 2.5 \times ' + str(bolt_dia_prov) + r'\\'))
            spacing_req.append(NoEscape(r'&= ' + str(p_min) + r' \text{ mm}\\'))
            spacing_req.append(NoEscape(r'g_{\text{min}} &= 2.5 \cdot d\\'))
            spacing_req.append(NoEscape(r'&= 2.5 \times ' + str(bolt_dia_prov) + r'\\'))
            spacing_req.append(NoEscape(r'&= ' + str(g_min) + r' \text{ mm}\\ \\'))
            spacing_req.append(NoEscape(r'&[\text{Ref. Cl. 10.2.2}]'))
            spacing_req.append(NoEscape(r'\end{aligned}'))
            
            spacing_prov = Math(inline=True)
            spacing_prov.append(NoEscape(r'\begin{aligned}'))
            spacing_prov.append(NoEscape(r'p_{\text{prov}} &= ' + str(pitch) + r' \text{ mm}\\'))
            spacing_prov.append(NoEscape(r'g_{\text{prov}} &= ' + str(gauge) + r' \text{ mm}'))
            spacing_prov.append(NoEscape(r'\end{aligned}'))
            
            spacing_status = "PASS" if (pitch >= p_min and gauge >= g_min) else "FAIL"
            self.report_check.append(["Minimum Spacing", spacing_req, spacing_prov, spacing_status])

            # 2.3.2 Maximum Spacing (Cl. 10.2.3.1)
            plate_thk_min = min(plate1_thk_raw, plate2_thk_raw)
            p_max = as_int(min(32 * plate_thk_min, 300), 0)
            g_max = as_int(min(32 * plate_thk_min, 300), 0)
            
            max_spacing_req = Math(inline=True)
            max_spacing_req.append(NoEscape(r'\begin{aligned}'))
            max_spacing_req.append(NoEscape(r'p_{\text{max}} &= \min(32 \cdot t, 300 \text{ mm})\\'))
            max_spacing_req.append(NoEscape(r'&= \min(32 \times ' + str(plate_thk_min) + r', 300)\\'))
            max_spacing_req.append(NoEscape(r'&= ' + str(p_max) + r' \text{ mm}\\'))
            max_spacing_req.append(NoEscape(r'g_{\text{max}} &= \min(32 \cdot t, 300 \text{ mm})\\'))
            max_spacing_req.append(NoEscape(r'&= \min(32 \times ' + str(plate_thk_min) + r', 300)\\'))
            max_spacing_req.append(NoEscape(r'&= ' + str(g_max) + r' \text{ mm}\\ \\'))
            max_spacing_req.append(NoEscape(r'&[\text{Ref. Cl. 10.2.3.1}]'))
            max_spacing_req.append(NoEscape(r'\end{aligned}'))
            
            max_spacing_prov = Math(inline=True)
            max_spacing_prov.append(NoEscape(r'\begin{aligned}'))
            max_spacing_prov.append(NoEscape(r'p_{\text{prov}} &= ' + str(pitch) + r' \text{ mm}\\'))
            max_spacing_prov.append(NoEscape(r'g_{\text{prov}} &= ' + str(gauge) + r' \text{ mm}'))
            max_spacing_prov.append(NoEscape(r'\end{aligned}'))
            
            max_spacing_status = "PASS" if (pitch <= p_max and gauge <= g_max) else "FAIL"
            self.report_check.append(["Maximum Spacing", max_spacing_req, max_spacing_prov, max_spacing_status])

            # 2.3.3 Edge Distance (Cl. 10.2.4)
            bolt_hole_type_str = str(self.bolt.bolt_hole_type) if hasattr(self.bolt, 'bolt_hole_type') else "Standard"
            d_hole = IS800_2007.cl_10_2_1_bolt_hole_size(d, bolt_hole_type_str)
            
            if "Sheared" in edge_type or "hand flame cut" in edge_type:
                e_min_calc = f2(1.7 * d_hole, 0.0)
                e_min_multiplier = 1.7
            else:  # Rolled, machine-flame cut, sawn and planed
                e_min_calc = f2(1.5 * d_hole, 0.0)
                e_min_multiplier = 1.5
            
            epsilon = math.sqrt(250 / fy)
            e_max_calc = f2(12 * plate_thk_min * epsilon, 0.0)
            
            edge_req = Math(inline=True)
            edge_req.append(NoEscape(r'\begin{aligned}'))
            edge_req.append(NoEscape(r'e_{\min} &= ' + str(e_min_multiplier) + r' \cdot d_0\\'))
            edge_req.append(NoEscape(r'&= ' + str(e_min_multiplier) + r' \times ' + f'{d_hole:.1f}' + r' = ' + f'{e_min_calc:.1f}' + r' \text{ mm}\\'))
            edge_req.append(NoEscape(r'e_{\text{max}} &= 12 \cdot t \cdot \varepsilon\\'))
            edge_req.append(NoEscape(r'&= 12 \times ' + str(plate_thk_min) + r' \times ' + f'{epsilon:.2f}' + r'\\'))
            edge_req.append(NoEscape(r'&= ' + str(e_max_calc) + r' \text{ mm}\\ \\'))
            edge_req.append(NoEscape(r'&[\text{Ref. Cl. 10.2.4}]'))
            edge_req.append(NoEscape(r'\end{aligned}'))
            
            edge_prov = Math(inline=True)
            edge_prov.append(NoEscape(r'e_{\text{prov}} = ' + str(e_dist) + r' \text{ mm}'))
            
            edge_status = "PASS" if (e_dist >= e_min_calc and e_dist <= e_max_calc) else "FAIL"
            self.report_check.append(["Edge Distance", edge_req, edge_prov, edge_status])

            #===============================
            # Section 2.4: Number of Bolts
            #===============================
            self.report_check.append([
                "SubSection", "Number of Bolts Required", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            bolts_req_initial = math.ceil(axial_kN / bolt_final_cap) if bolt_final_cap > 0 else 0
            
            bolts_eq = Math(inline=True)
            bolts_eq.append(NoEscape(r'\begin{aligned}\\'))
            bolts_eq.append(NoEscape(r'n &= \frac{P}{V_{db}}\\\\'))
            bolts_eq.append(NoEscape(r'&= \frac{' + str(axial_kN) + r'}{' + str(bolt_final_cap) + r'}\\\\'))
            bolts_eq.append(NoEscape(r'&= ' + str(bolts_req_initial) + r' \text{ nos.}\\'))
            bolts_eq.append(NoEscape(r'\end{aligned}'))
            
            self.report_check.append(["Bolts Required", f" {axial_kN:.2f} kN", bolts_eq, ""])

            #===============================
            # Section 2.5: Bolt Arrangement
            #===============================
            self.report_check.append([
                "SubSection", "Bolt Arrangement", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])
            
            self.report_check.append([
                "Bolt Pattern", "2", f"Arrangement: {rows} rows × {cols} columns", ""
            ])

            #================================
            # Section 2.6: Base Metal Strength
            #================================
            self.report_check.append([
                "SubSection", "Base Metal Strength", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            if is_comp:
                base_req = Math(inline=True)
                base_req.append(NoEscape(r'\begin{aligned}\\'))
                base_req.append(NoEscape(r'P_d &= \frac{A_g \cdot f_y}{\gamma_{m0}}\\\\'))
                base_req.append(NoEscape(r'&= \frac{' + str(A_g) + r' \times ' + str(fy) + r'}{1.10}\\\\'))
                base_req.append(NoEscape(r'&= ' + f'{base_metal_capacity_kN:.2f}' + r' \text{ kN}\\'))
                base_req.append(NoEscape(r'&[\text{Ref. Cl. 7.1.2}]'))
                base_req.append(NoEscape(r'\end{aligned}'))
                
                base_status = "PASS" if base_metal_capacity_kN >= axial_kN else "FAIL"
                self.report_check.append(["Plate Tension Capacity", "", base_req, base_status])
            else:
                # 1. Gross Section Yielding
                yield_req = Math(inline=True)
                yield_req.append(NoEscape(r'\begin{aligned}\\'))
                yield_req.append(NoEscape(r'T_{dg} &= \frac{A_g \cdot f_y}{\gamma_{m0}}\\\\'))
                yield_req.append(NoEscape(r'&= \frac{' + str(A_g) + r' \times ' + str(fy) + r'}{1.10}\\\\'))
                yield_req.append(NoEscape(r'&= ' + f'{T_dg:.2f}' + r' \text{ kN}\\'))
                yield_req.append(NoEscape(r'&[\text{Ref. Cl. 6.2}]'))
                yield_req.append(NoEscape(r'\end{aligned}'))
                self.report_check.append(["Gross Section Yield", "", yield_req, ""])

                # 2. Net Section Rupture
                rup_req = Math(inline=True)
                rup_req.append(NoEscape(r'\begin{aligned}'))
                rup_req.append(NoEscape(r'T_{dn} &= \frac{0.9 A_n f_u}{\gamma_{m1}}\\'))
                rup_req.append(NoEscape(r'&= ' + f'{T_dn:.2f}' + r' \text{ kN}\\'))
                rup_req.append(NoEscape(r'&[\text{Ref. Cl. 6.3}]'))
                rup_req.append(NoEscape(r'\end{aligned}'))
                self.report_check.append(["Net Section Rupture", "", rup_req, ""])

                # 3. Block Shear (Cl 6.4)
                # Recalculate areas for report clarity
                # Note: We use the same logic as the solver's check_base_metal_strength
                n_r = self.rows
                p = self.final_pitch
                g_val = self.final_gauge
                e_val = self.final_end_dist
                dia_hole = IS800_2007.cl_10_2_1_bolt_hole_size(d, str(self.bolt.bolt_hole_type))
                
                t_min = min(plate1_thk_raw, plate2_thk_raw)
                
                Avg = t_min * ((n_r - 1) * g_val + e_val)
                Avn = t_min * ((n_r - 1) * g_val + e_val - (n_r - 0.5) * dia_hole)
                Atg = t_min * e_val
                Atn = t_min * (e_val - 0.5 * dia_hole)
                
                Tdb1 = (Avg * fy / (math.sqrt(3) * 1.10) + 0.9 * Atn * fu / 1.25) / 1000
                Tdb2 = (0.9 * Avn * fu / (math.sqrt(3) * 1.25) + Atg * fy / 1.10) / 1000
                Tdb = min(Tdb1, Tdb2)

                block_req = Math(inline=True)
                block_req.append(NoEscape(r'\begin{aligned}'))
                block_req.append(NoEscape(r'A_{vg} &= ' + f'{Avg:.0f}' + r' \text{ mm}^2, \quad A_{vn} = ' + f'{Avn:.0f}' + r' \text{ mm}^2\\'))
                block_req.append(NoEscape(r'A_{tg} &= ' + f'{Atg:.0f}' + r' \text{ mm}^2, \quad A_{tn} = ' + f'{Atn:.0f}' + r' \text{ mm}^2\\'))
                block_req.append(NoEscape(r'T_{db1} &= \frac{A_{vg} f_y}{\sqrt{3} \gamma_{m0}} + \frac{0.9 A_{tn} f_u}{\gamma_{m1}} = ' + f'{Tdb1:.2f}' + r' \text{ kN}\\'))
                block_req.append(NoEscape(r'T_{db2} &= \frac{0.9 A_{vn} f_u}{\sqrt{3} \gamma_{m1}} + \frac{A_{tg} f_y}{\gamma_{m0}} = ' + f'{Tdb2:.2f}' + r' \text{ kN}\\'))
                block_req.append(NoEscape(r'T_{db} &= \min(T_{db1}, T_{db2}) = ' + f'{Tdb:.2f}' + r' \text{ kN}\\'))
                block_req.append(NoEscape(r'&[\text{Ref. Cl. 6.4.1}]'))
                block_req.append(NoEscape(r'\end{aligned}'))
                self.report_check.append(["Block Shear", "", block_req, ""])

                # Governing Strength
                base_req = Math(inline=True)
                base_req.append(NoEscape(r'\begin{aligned}'))
                base_req.append(NoEscape(r'T_d &= \min(T_{dg}, T_{dn}, T_{db})\\'))
                base_req.append(NoEscape(r'&= ' + f'{base_metal_capacity_kN:.2f}' + r' \text{ kN}\\'))
                base_req.append(NoEscape(r'\end{aligned}'))
                
                base_status = "PASS" if base_metal_capacity_kN >= axial_kN else "FAIL"
                self.report_check.append(["Plate Tension Capacity", "", base_req, base_status])

            #=============================
            # Section 2.7: Design Summary
            #=============================
            self.report_check.append([
                "SubSection", "Design Summary", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            bolt_capacity_total = f2(bolt_final_cap * n_bolts, 0.0)
            bolt_ur = axial_kN / bolt_capacity_total if bolt_capacity_total > 0 else 999.0
            
            plate_ur = axial_kN / base_metal_capacity_kN if base_metal_capacity_kN > 0 else 999.0
            
            # Overall UR is max of both
            overall_ur_val = max(bolt_ur, plate_ur)
            overall_ur = round(overall_ur_val, 3)

            ur_req = Math(inline=True)
            ur_req.append(NoEscape(r'\begin{aligned}\\'))
            ur_req.append(NoEscape(r'\text{Bolt Capacity} &= ' + str(bolt_capacity_total) + r' \text{ kN}\\'))
            ur_req.append(NoEscape(r'\text{Plate Capacity} &= ' + str(base_metal_capacity_kN) + r' \text{ kN}\\\\'))
            ur_req.append(NoEscape(r'\text{UR}_{\text{bolt}} &= \frac{' + str(axial_kN) + r'}{' + str(bolt_capacity_total) + r'}\\'))
            ur_req.append(NoEscape(r'&= ' + f'{bolt_ur:.3f}' + r'\\\\'))
            ur_req.append(NoEscape(r'\text{UR}_{\text{plate}} &= \frac{' + str(axial_kN) + r'}{' + str(base_metal_capacity_kN) + r'}\\'))
            ur_req.append(NoEscape(r'&= ' + f'{plate_ur:.3f}' + r'\\\\'))
            ur_req.append(NoEscape(r'\text{UR}_{\text{final}} &= \max(\text{UR}_{\text{bolt}}, \text{UR}_{\text{plate}})\\'))
            ur_req.append(NoEscape(r'&= ' + str(overall_ur) + r'\end{aligned}'))
            
            util_prov = Math(inline=True)
            util_prov.append(NoEscape(str(overall_ur) + r' \leq 1.0'))
        
            util_status = "PASS" if overall_ur_val <= 1.0 else "FAIL"
            self.report_check.append(["Utilization Ratio", f"{axial_kN:.2f} kN", ur_req, util_status])

            Disp_2d_image = []
            Disp_3D_image = "/ResourceFiles/images/3d.png"
            rel_path = os.path.abspath(".").replace("\\", "/")
            fname_no_ext = popup_summary.get("filename", "LapJointBoltedReport")
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
