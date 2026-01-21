"""
Module: butt_joint_welded.py
roushan
Author: Aman, Tanu Singh, Nishi Kant Mandal, Roushan Raj
=======
Author: Aman, Tanu Singh, Nishi Kant Mandal
FinalSimpleConnection
Date: 2025-06-12

Description:
    ButtJointWelded is a moment connection module that represents a welded butt joint connection.
    It inherits from MomentConnection and follows the same structure and design logic as other
    connection modules (e.g., BeamCoverPlate, ColumnCoverPlate) used in Osdag.
    
Reference:
    - Osdag software guidelines and connection module structure documentation
"""

import os
import traceback
from .moment_connection import MomentConnection
from ...utils.common.component import *
from ...utils.common.is800_2007 import IS800_2007
from ...utils.common.is800_2007 import *
from ...Common import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...Report_functions import *
from ...utils.common.load import Load
from ...custom_logger import CustomLogger
import logging

import math

from PyQt5.QtCore import Qt

class ButtJointWelded(MomentConnection):
    def __init__(self):
        super(ButtJointWelded, self).__init__()
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
        tabs.append((("Weld", TYPE_TAB_2, self.weld_values))) # added this line t.s.
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
        design_input.append(("Weld", TYPE_COMBOBOX, [
            KEY_DP_WELD_TYPE,
            KEY_DP_WELD_MATERIAL_G_O
        ]))
        design_input.append(("Detailing", TYPE_COMBOBOX, [
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DP_DETAILING_PACKING_PLATE
        ]))
        design_input.append(("Design", TYPE_COMBOBOX, [KEY_DESIGN_FOR]))
        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        design_input.append((None, [
            KEY_DP_WELD_TYPE,
            KEY_DP_WELD_MATERIAL_G_O,
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DP_DETAILING_PACKING_PLATE,
            KEY_DESIGN_FOR
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
            KEY_DP_DETAILING_PACKING_PLATE: "Yes",
            KEY_DESIGN_FOR: "Tension"
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
            KEY_DP_DETAILING_PACKING_PLATE: 'Yes',
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

        t49 = (KEY_DP_DETAILING_PACKING_PLATE, KEY_DISP_DP_DETAILING_PACKING_PLATE, TYPE_COMBOBOX,
               ['Yes', 'No'], values[KEY_DP_DETAILING_PACKING_PLATE])
        detailing.append(t49)

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

    # added weld function

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

    def set_osdaglogger(self, key, id):
        """
        Function to set Logger for FinPlate Module
        """
        # @author Arsil Zunzunia

        # Set Custom logger
        logging.setLoggerClass(CustomLogger)

        # Create unique logger name per instance
        unique_logger_name = 'Osdag_butt_joint_welded_simple_conn'
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
    # not sure about this function no changes done here -t.s.

    def input_values(self):
        options_list = []
        
        t16 = (KEY_MODULE, KEY_DISP_BUTTJOINTWELDED, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t5 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t5)

        t31 = (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t31)

        t34 = (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t34)

        t35 = (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None, True, 'Float Validator')
        options_list.append(t35)

        t6 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t6)

        t36 = (KEY_COVER_PLATE, KEY_DISP_COVER_PLT, TYPE_COMBOBOX, VALUES_COVER_PLATE, True, 'No Validator')
        options_list.append(t36)

        t18 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t18)

        t20 = (KEY_WELD_SIZE, KEY_DISP_WELD_SIZE, TYPE_COMBOBOX_CUSTOMIZED, VALUES_ALL_CUSTOMIZED, True, 'No Validator')
        options_list.append(t20)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t17 = (KEY_AXIAL_FORCE, KEY_DISP_AXIAL_FORCE, TYPE_TEXTBOX, None, True, 'Float Validator')
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

        t111 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t111)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def output_values(self, flag):
        out_list=[]
        # Cover plate details
        t44 = (None, DISP_TITLE_COVER_PLATE, TYPE_TITLE, None, True)
        out_list.append(t44)

        t22 = (KEY_OUT_UTILISATION_RATIO, KEY_OUT_DISP_UTILISATION_RATIO, TYPE_TEXTBOX,
               round(self.utilization_ratio, 3) if flag else '', True)
        out_list.append(t22)

        # Calculate cover_type based on planes attribute
        cover_type = ''
        if flag and hasattr(self, 'planes'):
            cover_type = "Double" if self.planes == 2 else "Single"
            
        t13 = (KEY_OUT_NO_COVER_PLATE, KEY_OUT_DISP_NO_COVER_PLATE, TYPE_TEXTBOX,
               cover_type if flag else '', True)
        out_list.append(t13)

        t38 = (KEY_OUT_WIDTH_COVER_PLATE, KEY_OUT_DISP_WIDTH_COVER_PLATE, TYPE_TEXTBOX,
               self.plates_width if flag else '', True)
        out_list.append(t38)

        t28 = (KEY_OUT_LENGTH_COVER_PLATE, KEY_OUT_DISP_LENGTH_COVER_PLATE, TYPE_TEXTBOX,
               round(self.weld_length_provided, 1) if flag else '', True)
        out_list.append(t28)

        t47 = (KEY_OUT_THICKNESS_COVER_PLATE, KEY_OUT_DISP_THICKNESS_COVER_PLATE, TYPE_TEXTBOX,
               self.calculated_cover_plate_thickness if flag else '', True)
        out_list.append(t47)

        if hasattr(self, 'packing_thickness') and self.packing_thickness > 0:
            t15 = (KEY_PK_PLTHK, KEY_DISP_PK_PLTHK, TYPE_TEXTBOX,
                  round(self.packing_thickness, 1) if flag else '', True)
            out_list.append(t15)
        
        # Weld details
        t21 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t21)

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

        t27 = (KEY_OUT_BOLT_CONN_LEN, KEY_OUT_DISP_BOLT_CONN_LEN, TYPE_TEXTBOX,
               round(self.weld_length_provided, 1) if flag else '', True)
        out_list.append(t27)

        t29 = (KEY_OUT_DESIGN_FOR, KEY_OUT_DISP_DESIGN_FOR, TYPE_TEXTBOX,
               self.design_for if flag else '', True)
        out_list.append(t29)

        # Populate Hover Dict (Butt Joint Welded) with actual dimensions
        plate_length = getattr(self, 'weld_length_provided', 0)
        plate_width = getattr(self, 'plates_width', 0)
        plate1_thk = float(self.plate1.thickness[0]) if hasattr(self, 'plate1') and self.plate1 and self.plate1.thickness else 0
        plate2_thk = float(self.plate2.thickness[0]) if hasattr(self, 'plate2') and self.plate2 and self.plate2.thickness else 0
        cover_thk = getattr(self, 'calculated_cover_plate_thickness', 0)
        packing_thk = getattr(self, 'packing_plate_thickness', 0)
        
        self.hover_dict["Plate 1"] = (
            f"<b>Plate 1</b><br>"
            f"Width: {round(float(plate_width), 2) if flag and plate_width else ''} mm<br>"
            f"Thickness: {round(float(plate1_thk), 2) if flag and plate1_thk else ''} mm"
        )

        self.hover_dict["Plate 2"] = (
            f"<b>Plate 2</b><br>"
            f"Width: {round(float(plate_width), 2) if flag and plate_width else ''} mm<br>"
            f"Thickness: {round(float(plate2_thk), 2) if flag and plate2_thk else ''} mm"
        )

        self.hover_dict["Cover Plate"] = (
            f"<b>Cover Plate</b><br>"
            f"Width: {round(float(plate_width), 2) if flag and plate_width else ''} mm<br>"
            f"Thickness: {round(float(cover_thk), 2) if flag and cover_thk else ''} mm"
        )

        # Packing plate - only show if thickness > 0
        if flag and packing_thk > 0:
            self.hover_dict["Packing Plate"] = (
                f"<b>Packing Plate</b><br>"
                f"Width: {round(float(plate_width), 2)} mm<br>"
                f"Thickness: {round(float(packing_thk), 2)} mm"
            )
        else:
            self.hover_dict["Packing Plate"] = (
                f"<b>Packing Plate</b><br>"
                f"Not required for this configuration"
            )

        self.hover_dict["Weld"] = (
            f"<b>Fillet Weld</b><br>"
            f"Size: {round(float(self.weld_size), 1) if flag and self.weld_size else ''} mm<br>"
            f"Type: {'Shop weld' if flag else ''}<br>"
            f"Effective Length: {round(float(self.weld_length_effective), 1) if flag and hasattr(self, 'weld_length_effective') and self.weld_length_effective else ''} mm"
        )

        return out_list

    @staticmethod
    def module_name():
        return KEY_DISP_BUTTJOINTWELDED

    def get_3d_components(self):
        """Get 3D components for visualization"""
        components = []
        t1 = ('Model', self.call_3DModel)
        components.append(t1)
        t2 = ('Plate 1', self.call_3DPlate1)
        components.append(t2)
        t3 = ('Plate 2', self.call_3DPlate2)
        components.append(t3)
        t4 = ('Cover Plate', self.call_3DCoverPlate)
        components.append(t4)
        t5 = ('Welds', self.call_3DWeld)
        components.append(t5)
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
    
    def call_3DCoverPlate(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Cover Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel('Cover Plate', bgcolor)

    def call_3DWeld(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Welds':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel('Welds', bgcolor)

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

                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value for Axial Force must be a positive value."
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

        print(f'flag = {flag}, flag1 = {flag1}, flag2 = {flag2}')
        if flag  and flag1 and flag2:
            self.set_input_values(design_dictionary)
        else:
            return all_errors

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
        super(ButtJointWelded, self).set_input_values(design_dictionary_with_defaults)
        print(design_dictionary,"input values are set. Doing preliminary member checks")
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Butt Joint Welded Connection"
        
        # self.plate_thickness = [3,4,6,8,10,12,14,16,20,22,24,25,26,28,30,32,36,40,45,50,56,63,80]
        self.main_material = design_dictionary[KEY_MATERIAL]
        # Design mode: default to Tension if not provided
        self.design_for = design_dictionary.get(KEY_DESIGN_FOR, 'Tension')
        # Axial force: prefer KEY_AXIAL_FORCE, fallback to KEY_AXIAL, then KEY_TENSILE_FORCE
        axial_kN_str = design_dictionary.get(KEY_AXIAL_FORCE,
                design_dictionary.get(KEY_AXIAL,
                design_dictionary.get(KEY_TENSILE_FORCE, 0)))
        self.axial_force = abs(float(axial_kN_str)) * 1000  # N, always positive magnitude
        # Maintain backward compatibility: many methods use tensile_force name
        self.tensile_force = self.axial_force
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

        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        Tmin = min(plate1_thk, plate2_thk)
        cover_plate_type_str = design_dictionary[KEY_COVER_PLATE]
        self.cover_plate_type = cover_plate_type_str  # Store for CAD generation

        # Cover plate and packing plate logic as per documentation
        available_thicknesses = [float(thk) for thk in PLATE_THICKNESS_SAIL]
        if "double" in cover_plate_type_str.lower():
            self.planes = 2
            Tcp = math.ceil((9.0 / 16.0) * Tmin)  # Double cover plate thickness as per Eq. 3.2
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )

            # Packing plate logic as per Cl. 10.3.3.2
            if abs(plate1_thk - plate2_thk) > 0.001:
                self.packing_plate_thickness = abs(plate1_thk - plate2_thk)
            else:
                self.packing_plate_thickness = 0.0

        elif "single" in cover_plate_type_str.lower():
            self.planes = 1
            Tcp = math.ceil((5.0 / 8.0) * Tmin)  # Single cover plate thickness as per Eq. 3.1
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )
            self.packing_plate_thickness = 0.0

        else:
            self.planes = 1
            Tcp = Tmin
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )
            self.packing_plate_thickness = 0.0

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
        self.design_of_weld(design_dictionary)
    
    #========================DESIGN OF WELD==================================================================
    def design_of_weld(self, design_dictionary):
        """Design sequence for welded butt joint"""
        self.logger.info(": ===========  Design for Welded Butt Joint  ===========")
        self.logger.info(": Design Approach - IS 800:2007 Clause 10")

        # Track individual utilization ratios
        self.utilization_ratios = {}

        # Get the raw weld size input
        weld_size = design_dictionary[KEY_WELD_SIZE]

        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        Tmin = min(plate1_thk, plate2_thk)
        s_min = IS800_2007.cl_10_5_2_3_min_weld_size(plate1_thk, plate2_thk)
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
            self.logger.error(": weld_size is not set. Cannot proceed with weld design.")
            self.design_status = False
            self.logger.error(": Design status: UNSAFE due to missing or invalid weld size.")
            self.logger.info(": =========End Of Design===========")
            return

        # Return the selected weld size for output if needed
        self.selected_weld_size = self.weld_size

        self.effective_throat_thickness = 0.707 * self.weld_size
        self.fu = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])
        weld_type = design_dictionary[KEY_DP_WELD_TYPE]
        if weld_type == "Shop weld":
            self.gamma_mw = 1.25
        else:
            self.gamma_mw = 1.50
        self.weld_design_strength = self.fu / (math.sqrt(3) * self.gamma_mw)
        self.weld_length(design_dictionary)
        self.weld_strength_verification(design_dictionary)
        self.long_joint_reduction_factor()
        self.check_base_metal_strength(design_dictionary)
        self.calculate_final_utilization_ratio()

    def weld_length(self, design_dictionary):
        self.plates_width = float(design_dictionary[KEY_PLATE_WIDTH])
        # Use the weld_size that was already processed in design_of_weld
        # self.weld_size = float(design_dictionary[KEY_WELD_SIZE])  # This line is no longer needed
        self.cover_plate = design_dictionary[KEY_COVER_PLATE]
        # Dictionary to store output values for UI display
        self.output_values_dict = {}
        self.material = design_dictionary[KEY_MATERIAL]
        self.fu = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])
        self.weld_type = design_dictionary[KEY_DP_WELD_TYPE]
        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])

        # Calculate minimum and maximum weld sizes
        self.s_min = IS800_2007.cl_10_5_2_3_min_weld_size(plate1_thk, plate2_thk)
        Tmin = min(plate1_thk, plate2_thk)
        self.s_max = Tmin - 1.5

        # Check weld size constraints
        #self.logger.info(": Checking weld size requirements as per IS 800:2007")
        #self.logger.info(": Minimum weld size required (s_min) = {} mm [Ref. Table 21, Cl.10.5.2.3]".format(self.s_min))
        #self.logger.info(": Maximum allowed weld size (s_max) = {} mm [Ref. Cl.10.5.3.1]".format(self.s_max))
        #self.logger.info(": Selected weld size = {} mm".format(self.weld_size))

        if self.weld_size < self.s_min or self.weld_size > self.s_max:
            self.design_status = False
            if self.weld_size < self.s_min:
                self.logger.error(": Weld size fails: Size {} mm is less than minimum required {} mm".format(
                    self.weld_size, self.s_min))
                self.logger.info(": Design action required: Increase the weld size to at least {} mm".format(self.s_min))
            else:
                self.logger.error(": Weld size fails: Size {} mm exceeds maximum allowed {} mm".format(
                    self.weld_size, self.s_max))
                self.logger.info(": Design action required: Decrease the weld size to at most {} mm".format(self.s_max))
            self.logger.error(": Design status: UNSAFE")
            self.logger.info(": =========End Of Design===========")
            return
        
        # Calculate weld length since size is acceptable
        if "shop weld" in self.weld_type.lower():
            self.gamma_mw = 1.25
        else:
            self.gamma_mw = 1.50

        self.f_w = self.fu / (math.sqrt(3) * self.gamma_mw)  # Design strength of weld

        if "single" in self.cover_plate.lower():
            self.N_f = 1  # Number of welds
        else:
            self.N_f = 2  # Double cover plate means two weld interfaces

                # Calculate required weld length 
        self.L_req = self.tensile_force / (self.N_f * 0.707 * self.weld_size * self.f_w)
            
        # Check if straight weld is sufficient
        if self.L_req <= self.plates_width:
            self.logger.info(": Straight weld will be provided as required length is less than plate width")
            self.weld_length_provided = self.plates_width
            self.weld_length_effective = self.weld_length_provided
            self.weld_angle = 0
            self.side_weld_length = 0

        else:
            # Calculate skewed weld parameters
            L_target = self.L_req / self.N_f  # Required length per weld line
        
            # Calculate skew angle
            self.weld_angle = math.degrees(math.atan((L_target - self.plates_width)/(2 * self.plates_width)))

            # Constrain angle between 20-60 degrees
            if self.weld_angle < 20:
                self.weld_angle = 20
            elif self.weld_angle > 60:
                self.weld_angle = 60

            # Calculate provided length per weld line with skew
            L_provided_line = self.plates_width + 2 * self.plates_width * math.tan(math.radians(self.weld_angle))
            L_provided_total = self.N_f * L_provided_line

            # Check if side welds are needed
            if L_provided_total < self.L_req:
                # Calculate required side weld length
                L_side = (self.L_req - L_provided_total) / self.N_f

                # Calculate minimum return weld length
                min_return = max(2 * self.weld_size, 10)  # As per IS 800:2007 Cl 10.5.10.2
                L_side = max(L_side, min_return)

                self.side_weld_length = L_side
            else:
                self.side_weld_length = 0

            self.weld_length_provided = L_provided_total
            self.weld_length_effective = L_provided_total + (2 * self.side_weld_length * self.N_f)

            self.logger.info(": Skewed weld will be provided with angle {:.2f} degrees".format(self.weld_angle))
            
        # Update output values for UI display
        self.output_values_dict[KEY_OUT_WELD_LENGTH] = self.weld_length_effective
    
    def weld_strength_verification(self, design_dictionary):
        """Verify weld strength and calculate utilization"""
        self.logger.info(": =========== Checking Weld Strength ===========")
        
        # Use the weld_size that was already processed in design_of_weld
        # self.weld_size = float(design_dictionary[KEY_WELD_SIZE])  # This line is no longer needed
        
        # Ensure we have weld_length_provided from previous calculation
        if not hasattr(self, 'weld_length_provided'):
            self.logger.error(": Weld length must be calculated before strength verification")
            self.design_status = False
            return
            
        # Calculate effective length by subtracting 2 times weld size from provided length
        self.weld_length_effective = self.weld_length_provided - (2 * self.weld_size)
        
        self.logger.info(": Checking minimum length requirements...")
        # Check if effective length meets minimum requirement of 4 times weld size
        min_length = 4 * self.weld_size
        if self.weld_length_effective < min_length:
            self.design_status = False
            self.logger.error(": Effective weld length {} mm is less than minimum required length {} mm [Ref. Cl.10.5.4, IS 800:2007]".format(
                round(self.weld_length_effective, 2), round(min_length, 2)))
            self.logger.info(": Increase the weld length or size")
            return
        else:
            self.logger.info(": Minimum length requirement satisfied")
            
        # Calculate weld strength 
        self.weld_strength = self.f_w * 0.707 * self.weld_size * self.weld_length_effective * self.N_f
        
        # Calculate weld utilization ratio
        weld_utilization = self.axial_force / self.weld_strength
        self.utilization_ratios['weld'] = weld_utilization
        
        #self.logger.info(": Weld Strength Calculation Results:")
        #self.logger.info(": Design strength of weld (f_w) = {} N/mm²".format(round(self.f_w, 2)))
        #self.logger.info(": Effective throat thickness = {} mm".format(round(0.707 * self.weld_size, 2)))
        #self.logger.info(": Weld size = {} mm".format(self.weld_size))
        #self.logger.info(": Effective length = {} mm".format(round(self.weld_length_effective, 2)))
        #self.logger.info(": Number of weld interfaces = {}".format(self.N_f))
        #self.logger.info(": Calculated weld strength = {} kN".format(round(self.weld_strength/1000, 2)))
        #self.logger.info(": Required tensile force = {} kN".format(round(self.tensile_force/1000, 2)))
        #self.logger.info(": Weld utilization ratio = {}".format(round(weld_utilization, 3)))
        
        if weld_utilization > 1:
            self.logger.error(": Weld strength is insufficient")
            self.logger.info(": Increase weld size or length")
        else:
            self.logger.info(": Weld strength is adequate")
    
    def long_joint_reduction_factor(self):
        """Calculate reduction factor for long joints according to IS 800:2007 Cl. 10.5.7.1(b)"""
        
        # Calculate effective throat thickness
        a = 0.707 * self.weld_size
        
        # Check if reduction is needed
        if self.weld_length_effective <= 150 * a:
            self.beta_L = 1.0
            self.logger.info(": No reduction for long joints required as length is less than 150 times throat thickness")
            return
            
        # Calculate reduction factor
        self.beta_L = 1.2 - (0.2 * self.weld_length_effective)/(150 * a)
        
        # Ensure minimum value of 0.8
        self.beta_L = max(0.8, self.beta_L)
        
        # Adjust weld design strength and recalculate utilization
        self.f_w_adjusted = self.f_w * self.beta_L
        
        # Recalculate weld strength with reduction factor
        self.weld_strength_reduced = self.f_w_adjusted * 0.707 * self.weld_size * self.weld_length_effective * self.N_f
        
        # Update weld utilization with reduced strength
        weld_utilization_reduced = self.axial_force / self.weld_strength_reduced
        self.utilization_ratios['weld'] = weld_utilization_reduced  # Update the utilization ratio
        
        #self.logger.info(": Long joint reduction check results:")
        #self.logger.info(": Long joint reduction factor βL = {}".format(round(self.beta_L, 2)))
        #self.logger.info(": Original weld design strength = {} N/mm²".format(round(self.f_w, 2)))
        #self.logger.info(": Adjusted weld design strength = {} N/mm²".format(round(self.f_w_adjusted, 2)))
        #self.logger.info(": Updated weld utilization ratio = {}".format(round(weld_utilization_reduced, 3)))

    def check_base_metal_strength(self, design_dictionary):
        """Check strength of base metal according to IS 800:2007.
        Tension: yielding and rupture (Cl. 6). Compression: gross yielding (Cl. 7).
        """
        
        # Extract material properties and handle material grade strings
        material_grade = design_dictionary[KEY_MATERIAL]
        # Extract numeric value from material grade string (e.g. "E 165 (Fe 290)" -> 165)
        try:
            # Extract the number after 'E' (e.g. "E 165" -> 165)
            self.fy = float(material_grade.split('(')[0].strip().split()[-1])
            
            # For custom grades, try direct conversion
            if material_grade.startswith('Custom'):
                self.fy = float(material_grade.split('_')[1])
        except (ValueError, IndexError):
            self.logger.error(f": Invalid material grade format: {material_grade}")
            self.design_status = False
            return

        self.fu = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])
        
        # Partial safety factors
        self.gamma_m0 = 1.10  # For yielding
        self.gamma_m1 = 1.25  # For rupture
        
        # Calculate areas
        Tmin = min(float(design_dictionary[KEY_PLATE1_THICKNESS]), 
                   float(design_dictionary[KEY_PLATE2_THICKNESS]))
        self.A_g = Tmin * self.plates_width
        self.A_n = self.A_g  # For welded joints, net area equals gross area
        
        if self.design_for == 'Compression':
            # Compression: use gross area yielding (buckling is member-level, not joint)
            self.T_db = self.A_g * self.fy / self.gamma_m0
            base_metal_utilization = self.axial_force / self.T_db
        else:
            # Tension: yielding and rupture, take minimum
            T_dy = self.A_g * self.fy / self.gamma_m0
            T_du = 0.9 * self.A_n * self.fu / self.gamma_m1
            self.T_db = min(T_dy, T_du)
            base_metal_utilization = self.axial_force / self.T_db
        self.utilization_ratios['base_metal'] = base_metal_utilization
        
        #self.logger.info(": Base Metal Strength Results:")
        #self.logger.info(": Material yield strength (fy) = {} N/mm²".format(round(self.fy, 2)))
        #self.logger.info(": Material ultimate strength (fu) = {} N/mm²".format(round(self.fu, 2)))
        #self.logger.info(": Gross section area = {} mm²".format(round(self.A_g, 2)))
        #self.logger.info(": Net section area = {} mm".format(round(self.A_n, 2)))
        #self.logger.info(": Tensile strength - Yielding = {} kN".format(round(T_dy/1000, 2)))
        #self.logger.info(": Tensile strength - Rupture = {} kN".format(round(T_du/1000, 2)))
        #self.logger.info(": Design strength of base metal = {} kN".format(round(self.T_db/1000, 2)))
        #self.logger.info(": Required tensile force = {} kN".format(round(self.tensile_force/1000, 2)))
        #self.logger.info(": Base metal utilization ratio = {}".format(round(base_metal_utilization, 3)))
        
        if base_metal_utilization > 1:
            if self.design_for == 'Compression':
                self.logger.error(": Base metal strength in compression is insufficient [cl. 7, IS 800:2007]")
            else:
                self.logger.error(": Base metal strength in tension is insufficient [cl. 6, IS 800:2007]")
        else:
            if self.design_for == 'Compression':
                self.logger.info(": Base metal strength in compression is adequate")
            else:
                self.logger.info(": Base metal strength in tension is adequate")
    
    def calculate_final_utilization_ratio(self):
        """Calculate final utilization ratio and set design status after all component checks"""
        self.logger.info(": =========== Final Design Check ===========")
        
        if not hasattr(self, 'utilization_ratios'):
            self.logger.error(": Cannot calculate final utilization ratio - component checks incomplete")
            self.design_status = False
            return
            
        # Get maximum utilization ratio across all components
        self.utilization_ratio = max(self.utilization_ratios.values())
        
        #self.logger.info(": Design Status Summary:")
        #self.logger.info(": Weld utilization ratio: {}".format(round(self.utilization_ratios['weld'], 3)))
        #self.logger.info(": Base metal utilization ratio: {}".format(round(self.utilization_ratios['base_metal'], 3)))
        #self.logger.info(": Overall utilization ratio: {}".format(round(self.utilization_ratio, 3)))
        
        # Design is safe only if all utilization ratios are < 1.0
        if self.utilization_ratio > 1.0:
            self.design_status = False
            self.logger.error(": =========== Design is UNSAFE ===========")
            
            # Log which component caused the failure
            critical_component = max(self.utilization_ratios.items(), key=lambda x: x[1])[0]
            self.logger.error(": {} utilization ratio ({:.3f}) exceeds allowable limit of 1.0".format(
                critical_component.title(), self.utilization_ratio))
            
            recommendations = {
                'weld': ": Consider increasing weld size or length",
                'base_metal': ": Consider increasing plate dimensions or using higher grade material"
            }
            self.logger.info(recommendations[critical_component])
        else:
            self.design_status = True
            self.logger.info(": =========== Design is SAFE ===========")
            self.logger.info(": All utilization ratios are within acceptable limits")
        
        self.logger.info(": ==========End Of Design===========\n")
    
    def save_design(self, popup_summary):
        """
        Generate the LaTeX design report for Welded Butt Joint Connection
        per IS 800:2007 following DDCL structure.
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
            module = g('module', 'Butt Joint Welded Connection')
            mainmodule = 'Simple Connection'
            design_for = g('design_for', 'Tension').strip()
            is_comp = design_for.lower().startswith('c')
            edge_type = g('edgetype', 'Sheared or hand flame cut')

            # Plate properties
            plate1_thk = f2(self.plate1.thickness[0] if isinstance(self.plate1.thickness, list) else self.plate1.thickness, 0.0)
            plate2_thk = f2(self.plate2.thickness[0] if isinstance(self.plate2.thickness, list) else self.plate2.thickness, 0.0)
            plate_thk_min = min(plate1_thk, plate2_thk)
            width = f2(g('width', g('plates_width', 0.0)), 0.0)
            fy = f2(self.plate1.fy if hasattr(self, 'plate1') else 250, 250)
            fu = f2(self.plate1.fu if hasattr(self, 'plate1') else 410, 410)

            # Use stored values for strength calculation variables
            fu_weld = g('fu', float(g('weld.fu', 410)))
            
            # Load
            axial_force_N = f2(g('axial_force', g('axialforce', g('tensileforce', 0.0))), 0.0)
            axial_kN = f2(axial_force_N / 1000, 0.0)

            # Cover plate
            cover_plate_str = g('cover_plate', g('cover_plate_type', 'Single-Cover'))
            N_f = 2 if "double" in cover_plate_str.lower() else 1
            cover_thk = f2(g('calculated_cover_plate_thickness', 0.0), 0.0)
            packing_thk = f2(g('packing_plate_thickness', g('packing_thickness', 0.0)), 0.0)

            # Weld properties
            weld_size = f2(g('weld_size', g('weldsize', 0.0)), 0.0)
            weld_type = g('weld.type', 'Shop weld')
            weld_fabrication = g('weld.fabrication', 'Shop Weld')
            gamma_mw = 1.25 if 'shop' in weld_type.lower() else 1.50

            # Effective throat thickness
            effective_throat = f2(g('effective_throat_thickness', 0.707 * weld_size), 0.0)

            # Weld lengths - get from object attributes
            L_req = f2(g('L_req', 0.0), 0.0)
            L_eff_provided = f2(g('weld_length_effective', 0.0), 0.0)
            L_provided_line = f2(g('weld_length_provided', 0.0), 0.0)  # Per weld line
            L_eff_min = f2(max(4 * weld_size, 40), 0.0)
            
            # Skew angle and side welds
            skew_angle = f2(g('weld_angle', 0.0), 0.0)
            side_weld_len = f2(g('side_weld_length', 0.0), 0.0)
            
            # Calculate L_target per weld line
            L_target = f2(L_req / N_f if N_f > 0 else L_req, 0.0)

            # Long joint reduction factor
            beta_L = f2(g('beta_L', g('betalw', 1.0)), 1.0)

            # Base metal capacity - FIXED: Now calculates both Tdg and Tdn
            Ag = plate_thk_min * width
            gamma_m0 = 1.10
            gamma_m1 = 1.25

            # Always calculate both for tension case
            Tdg = f2((Ag * fy / gamma_m0) / 1000, 0.0)
            Tdn = f2((0.9 * Ag * fu / gamma_m1) / 1000, 0.0)
            
            if is_comp:
                base_metal_capacity_kN = Tdg  # Only yielding for compression
            else:
                base_metal_capacity_kN = f2(min(Tdg, Tdn), 0.0)

            # Weld strength - should use f_w_adjusted if beta_L applied
            f_w = fu_weld / (math.sqrt(3) * gamma_mw)
            f_w_adjusted = f2(f_w * beta_L, 0.0)
            
            # Weld capacity using adjusted strength
            weld_strength_N = f2(f_w_adjusted * effective_throat * L_eff_provided * N_f, 0.0)
            weld_strength_kN = f2(weld_strength_N / 1000, 0.0)

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
                KEY_DISP_COVER_PLT: cover_plate_str,
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
            # SECTION 3.1: COVER PLATE DESIGN
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Cover Plate Design", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            # FIXED ISSUE 1: Correct fraction display
            if N_f == 2:  # Double cover
                tcp_numerator = 9
                tcp_denominator = 16
                tcp_req = f2((9.0 / 16.0) * plate_thk_min, 0.0)
            else:  # Single cover
                tcp_numerator = 5
                tcp_denominator = 8
                tcp_req = f2((5.0 / 8.0) * plate_thk_min, 0.0)

            tcp_calc = Math(inline=True)
            tcp_calc.append(NoEscape(r'\begin{aligned}'))
            tcp_calc.append(NoEscape(r'T_{cp} &\geq \frac{' + str(tcp_numerator) + r'}{' + str(tcp_denominator) + r'} \times T_{min}\\'))
            tcp_calc.append(NoEscape(r'&\geq \frac{' + str(tcp_numerator) + r'}{' + str(tcp_denominator) + r'} \times ' + str(plate_thk_min) + r'\\'))
            tcp_calc.append(NoEscape(r'&\geq ' + str(tcp_req) + r' \text{ mm}\\'))
            tcp_calc.append(NoEscape(r'\end{aligned}'))

            tcp_prov = Math(inline=True)
            tcp_prov.append(NoEscape(r'T_{cp} = ' + str(cover_thk) + r' \text{ mm}'))

            tcp_status = "PASS" if cover_thk >= tcp_req else "FAIL"
            self.report_check.append(["Cover Plate Thickness", tcp_calc, tcp_prov, tcp_status])

            # Packing plate requirement (if applicable)
            if abs(plate1_thk - plate2_thk) > 0.001 and N_f == 2:
                packing_calc = Math(inline=True)
                packing_calc.append(NoEscape(r'\begin{aligned}'))
                packing_calc.append(NoEscape(r'T_{pack} &= |t_1 - t_2|\\'))
                packing_calc.append(NoEscape(r'&= |' + str(plate1_thk) + r' - ' + str(plate2_thk) + r'|\\'))
                packing_calc.append(NoEscape(r'&= ' + str(packing_thk) + r' \text{ mm}\\'))
                packing_calc.append(NoEscape(r'\end{aligned}'))

                packing_prov = Math(inline=True)
                packing_prov.append(NoEscape(str(packing_thk) + r' \text{ mm}'))

                self.report_check.append(["Packing Plate", packing_calc, packing_prov, "PASS"])

            # ==========================================================================
            # SECTION 3.2: WELD DESIGN
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Weld Design", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            # Minimum and maximum weld size
            s_min = IS800_2007.cl_10_5_2_3_min_weld_size(plate1_thk, plate2_thk)
            s_max = f2(plate_thk_min - 1.5, 0.0)

            size_check_req = Math(inline=True)
            size_check_req.append(NoEscape(r'\begin{aligned}'))
            size_check_req.append(NoEscape(r's_{min} &= ' + str(s_min) + r' \text{ mm}\\'))
            size_check_req.append(NoEscape(r'&[\text{Table 21, IS 800:2007}]\\'))
            size_check_req.append(NoEscape(r's_{max} &= T_{min} - 1.5\\'))
            size_check_req.append(NoEscape(r'&= ' + str(plate_thk_min) + r' - 1.5\\'))
            size_check_req.append(NoEscape(r'&= ' + str(s_max) + r' \text{ mm}\\'))
            size_check_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.2.3, 10.5.2.4}]'))
            size_check_req.append(NoEscape(r'\end{aligned}'))

            size_check_prov = Math(inline=True)
            size_check_prov.append(NoEscape(r's = ' + str(weld_size) + r' \text{ mm}'))

            size_status = "PASS" if (s_min <= weld_size <= s_max) else "FAIL"
            self.report_check.append(["Weld Size Check", size_check_req, size_check_prov, size_status])

            # Effective throat thickness
            throat_calc = Math(inline=True)
            throat_calc.append(NoEscape(r'\begin{aligned}'))
            throat_calc.append(NoEscape(r'a &= 0.707 \times s\\'))
            throat_calc.append(NoEscape(r'&= 0.707 \times ' + str(weld_size) + r'\\'))
            throat_calc.append(NoEscape(r'&= ' + str(effective_throat) + r' \text{ mm}\\'))
            throat_calc.append(NoEscape(r'\end{aligned}'))

            self.report_check.append(["Effective Throat", "", throat_calc, ""])

            # Design strength of weld
            weld_strength_calc = Math(inline=True)
            weld_strength_calc.append(NoEscape(r'\begin{aligned}\\'))
            weld_strength_calc.append(NoEscape(r'f_{wd} &= \frac{f_u}{\sqrt{3} \times \gamma_{mw}}\\\\'))
            weld_strength_calc.append(NoEscape(r'&= \frac{' + str(f2(fu_weld)) + r'}{\sqrt{3} \times ' + str(gamma_mw) + r'}\\\\'))
            weld_strength_calc.append(NoEscape(r'&= ' + f'{f_w:.2f}' + r' \text{ N/mm}^2\\'))
            weld_strength_calc.append(NoEscape(r'\end{aligned}'))

            self.report_check.append(["Design Strength", "", weld_strength_calc, ""])

            # ==========================================================================
            # SECTION 3.3: REQUIRED WELD LENGTH
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Required Weld Length", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            # Calculate Lreq in Required column, check condition in Provided column
            length_req_calc = Math(inline=True)
            length_req_calc.append(NoEscape(r'\begin{aligned}\\'))
            length_req_calc.append(NoEscape(r'L_{req} &= \frac{P_N}{f_{wd} \times a \times n_f}\\\\'))
            length_req_calc.append(NoEscape(r'&= \frac{' + str(int(axial_force_N)) + r'}{' + f'{f_w:.2f}' + r' \times ' + str(effective_throat) + r' \times ' + str(N_f) + r'}\\\\'))
            length_req_calc.append(NoEscape(r'&= ' + str(L_req) + r' \text{ mm}\\\\'))
            length_req_calc.append(NoEscape(r'&[\text{Ref. Section 3.3, DDCL}]'))
            length_req_calc.append(NoEscape(r'\end{aligned}'))

            # Condition check in Provided column
            length_condition = Math(inline=True)
            length_condition.append(NoEscape(r'\begin{aligned}'))
            length_condition.append(NoEscape(r'L_{req} &\leq w\\'))
            length_condition.append(NoEscape(r'' + str(L_req) + r' &\leq ' + str(width) + r'\\'))
            if L_req <= width:
                length_condition.append(NoEscape(r'&\text{Straight weld is sufficient}'))
                req_status = "PASS"
            else:
                length_condition.append(NoEscape(r'&\text{Proceed to Section 3.4}'))
                req_status = ""
            length_condition.append(NoEscape(r'\end{aligned}'))

            self.report_check.append(["Required Length", length_req_calc, length_condition, req_status])


            # ==========================================================================
            # SECTION 3.4: WELD LENGTH EXTENSION
            # ==========================================================================
            if L_req > width:
                self.report_check.append([
                    "SubSection", "Weld Length Extension", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
                ])

                # 3.4.1: Skew Angle Method - show full calculation
                skew_calc_detail = Math(inline=True)
                skew_calc_detail.append(NoEscape(r'\begin{aligned}'))
                skew_calc_detail.append(NoEscape(r'L_{target} &= \frac{L_{req}}{n_f}\\'))
                skew_calc_detail.append(NoEscape(r'&= \frac{' + str(L_req) + r'}{' + str(N_f) + r'}\\'))
                skew_calc_detail.append(NoEscape(r'&= ' + str(L_target) + r' \text{ mm}\\'))
                skew_calc_detail.append(NoEscape(r'&[\text{Ref. Section 3.4.1, Step 1}]'))
                skew_calc_detail.append(NoEscape(r'\end{aligned}'))
                
                self.report_check.append(["Target Length/Line", "", skew_calc_detail, ""])

                # Calculate skew angle
                if skew_angle > 0:
                    skew_angle_calc = Math(inline=True)
                    skew_angle_calc.append(NoEscape(r'\begin{aligned}'))
                    skew_angle_calc.append(NoEscape(r'\alpha &= \arctan\left(\frac{L_{target} - w}{2w}\right)\\'))
                    skew_angle_calc.append(NoEscape(r'&= \arctan\left(\frac{' + str(L_target) + r' - ' + str(width) + r'}{2 \times ' + str(width) + r'}\right)\\'))
                    skew_angle_calc.append(NoEscape(r'&= ' + f'{skew_angle:.1f}' + r'^\circ\\'))
                    
                    # Check constraints 20° ≤ α ≤ 60°
                    if skew_angle < 20:
                        skew_angle_calc.append(NoEscape(r'&\text{Since } \alpha < 20^\circ, \text{ set } \alpha = 20^\circ\\'))
                    elif skew_angle > 60:
                        skew_angle_calc.append(NoEscape(r'&\text{Since } \alpha > 60^\circ, \text{ set } \alpha = 60^\circ\\'))
                        skew_angle_calc.append(NoEscape(r'&\text{(Proceed to Section 3.4.3)}\\'))
                    
                    skew_angle_calc.append(NoEscape(r'&[\text{Ref. Section 3.4.1, Steps 3-4}]'))
                    skew_angle_calc.append(NoEscape(r'\end{aligned}'))

                    self.report_check.append(["Skew Angle", skew_angle_calc, f'{skew_angle:.1f}°', ""])

                    # 3.4.2: Provided weld length per line
                    L_prov_line_calc = Math(inline=True)
                    L_prov_line_calc.append(NoEscape(r'\begin{aligned}'))
                    L_prov_line_calc.append(NoEscape(r'L_{provided\_line} &= w + 2w \times \tan(\alpha)\\'))
                    L_prov_line_calc.append(NoEscape(r'&= ' + str(width) + r' + 2 \times ' + str(width) + r' \times \tan(' + f'{skew_angle:.1f}' + r'^\circ)\\'))
                    L_prov_line_calc.append(NoEscape(r'&= ' + str(L_provided_line) + r' \text{ mm}\\'))
                    L_prov_line_calc.append(NoEscape(r'&[\text{Ref. Section 3.4.2, Step 1}]'))
                    L_prov_line_calc.append(NoEscape(r'\end{aligned}'))

                    self.report_check.append(["Provided Length/Line", "", L_prov_line_calc, ""])

                # 3.4.3: Side weld extension (if needed)
                if side_weld_len > 0:
                    L_provided_total = L_provided_line * N_f
                    
                    side_calc = Math(inline=True)
                    side_calc.append(NoEscape(r'\begin{aligned}'))
                    side_calc.append(NoEscape(r'L_{side} &= \frac{L_{req} - L_{provided}}{n_f}\\'))
                    side_calc.append(NoEscape(r'&= \frac{' + str(L_req) + r' - ' + str(L_provided_total) + r'}{' + str(N_f) + r'}\\'))
                    side_calc.append(NoEscape(r'&= ' + str(side_weld_len) + r' \text{ mm}\\'))
                    
                    # Minimum return weld
                    min_return = max(2 * weld_size, 10)
                    side_calc.append(NoEscape(r'\text{Min. return} &= \max(2s, 10) = ' + str(min_return) + r' \text{ mm}\\'))
                    side_calc.append(NoEscape(r'&[\text{Ref. Cl. 10.5.10.2}]'))
                    side_calc.append(NoEscape(r'\end{aligned}'))

                    self.report_check.append(["Side Weld Length", side_calc, f'{side_weld_len:.1f} mm', ""])

            # ==========================================================================
            # SECTION 3.5: WELD STRENGTH VERIFICATION
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Weld Strength Verification", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            # Effective length calculation (Section 3.5, Step 1)
            eff_len_calc_detail = Math(inline=True)
            eff_len_calc_detail.append(NoEscape(r'\begin{aligned}'))
            eff_len_calc_detail.append(NoEscape(r'L_{eff} &= L_{provided\_line} - 2a\\'))
            eff_len_calc_detail.append(NoEscape(r'&= ' + str(L_provided_line) + r' - 2 \times ' + str(effective_throat) + r'\\'))
            eff_len_calc_detail.append(NoEscape(r'&= ' + str(L_eff_provided) + r' \text{ mm}\\'))
            eff_len_calc_detail.append(NoEscape(r'\end{aligned}'))

            self.report_check.append(["Effective Length", "", eff_len_calc_detail, ""])

            # ==========================================================================
            # SECTION 3.6: LONG JOINT REDUCTION FACTOR
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Long Joint Reduction Factor", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            # Check condition: Leff > 150a
            if L_eff_provided > 150 * effective_throat:
                beta_req = Math(inline=True)
                beta_req.append(NoEscape(r'\begin{aligned}'))
                beta_req.append(NoEscape(r'\text{Since } L_{eff} &> 150 \times a\\'))
                beta_req.append(NoEscape(r'' + str(L_eff_provided) + r' &> 150 \times ' + str(effective_throat) + r'\\'))
                beta_req.append(NoEscape(r'' + str(L_eff_provided) + r' &> ' + f'{150 * effective_throat:.1f}' + r'\\'))
                beta_req.append(NoEscape(r'\beta_L &= 1.2 - \frac{0.2 \times L_{eff}}{150 \times a}\\'))
                beta_req.append(NoEscape(r'&= 1.2 - \frac{0.2 \times ' + str(L_eff_provided) + r'}{150 \times ' + str(effective_throat) + r'}\\'))
                beta_calc_val = 1.2 - (0.2 * L_eff_provided) / (150 * effective_throat)
                beta_req.append(NoEscape(r'&= ' + f'{beta_calc_val:.3f}' + r'\\'))
                beta_req.append(NoEscape(r'&\text{(Ensure } \beta_L \geq 0.8\text{)}\\'))
                beta_req.append(NoEscape(r'\beta_L &= ' + f'{beta_L:.2f}' + r'\\'))
                beta_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.7.1(b)}]'))
                beta_req.append(NoEscape(r'\end{aligned}'))
                beta_status = "PASS" if beta_L >= 0.8 else "FAIL"
            else:
                beta_req = Math(inline=True)
                beta_req.append(NoEscape(r'\begin{aligned}'))
                beta_req.append(NoEscape(r'\text{Since } L_{eff} &\leq 150 \times a\\'))
                beta_req.append(NoEscape(r'' + str(L_eff_provided) + r' &\leq 150 \times ' + str(effective_throat) + r'\\'))
                beta_req.append(NoEscape(r'' + str(L_eff_provided) + r' &\leq ' + f'{150 * effective_throat:.1f}' + r'\\'))
                beta_req.append(NoEscape(r'\beta_L &= 1.0\\'))
                beta_req.append(NoEscape(r'&[\text{Ref. Cl. 10.5.7.1(b)}]'))
                beta_req.append(NoEscape(r'\end{aligned}'))
                beta_status = "PASS"

            beta_prov = Math(inline=True)
            beta_prov.append(NoEscape(r'\beta_L = ' + f'{beta_L:.2f}'))

            self.report_check.append(["Reduction Factor", beta_req, beta_prov, beta_status])

            # Weld capacity with reduction factor (Section 3.6, Equation 3.1)
            weld_cap_calc = Math(inline=True)
            weld_cap_calc.append(NoEscape(r'\begin{aligned}\\'))
            weld_cap_calc.append(NoEscape(r'C_w &= f_{wd}^{adj} \times a \times L_{eff} \times n_f\\\\'))
            weld_cap_calc.append(NoEscape(r'&= (\beta_L \times f_{wd}) \times a \times L_{eff} \times n_f\\\\'))
            weld_cap_calc.append(NoEscape(r'&= (' + f'{beta_L:.2f}' + r' \times ' + f'{f_w:.2f}' + r') \times ' + str(effective_throat) + r' \times ' + str(L_eff_provided) + r' \times ' + str(N_f) + r'\\\\'))
            weld_cap_calc.append(NoEscape(r'&= ' + str(weld_strength_kN) + r' \text{ kN}\\'))
            weld_cap_calc.append(NoEscape(r'\end{aligned}'))

            self.report_check.append(["Weld Capacity", "", weld_cap_calc, ""])

            # ==========================================================================
            # SECTION 3.7: BASE METAL STRENGTH CHECK
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Base Metal Strength Check", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            if is_comp:
                # For compression - only yielding check
                comp_calc_req = Math(inline=True)
                comp_calc_req.append(NoEscape(r'\begin{aligned}\\'))
                comp_calc_req.append(NoEscape(r'T_{db} &= \frac{A_g \times f_y}{\gamma_{m0}}\\'))
                comp_calc_req.append(NoEscape(r'T_{db} &= \frac{' + f'{Ag:.1f}' + r' \times ' + str(fy) + r'}{' + str(gamma_m0) + r'}\\'))
                comp_calc_req.append(NoEscape(r'&= ' + str(base_metal_capacity_kN) + r' \text{ kN}\\'))
                comp_calc_req.append(NoEscape(r'&[\text{Ref. Section 3.7, Cl. 7.1.2}]'))
                comp_calc_req.append(NoEscape(r'\end{aligned}'))
                
                comp_status = "PASS" if base_metal_capacity_kN >= axial_kN else "FAIL"
                self.report_check.append(["Base Metal Capacity", axial_kN, comp_calc_req, comp_status])
            else:
                # For tension - show both calculations and take min
                ten_calc_req = Math(inline=True)
                ten_calc_req.append(NoEscape(r'\begin{aligned}\\'))
                ten_calc_req.append(NoEscape(r'T_{db} &= \min\left(\frac{A_g f_y}{\gamma_{m0}}, \frac{0.9 A_n f_u}{\gamma_{m1}}\right)\\'))
                ten_calc_req.append(NoEscape(r'&= \min\left(\frac{' + f'{Ag:.1f}' + r' \times ' + str(fy) + r'}{' + str(gamma_m0) + r'}, \frac{0.9 \times ' + f'{Ag:.1f}' + r' \times ' + str(fu) + r'}{' + str(gamma_m1) + r'}\right)\\'))
                ten_calc_req.append(NoEscape(r'&= \min(' + str(Tdg) + r', ' + str(Tdn) + r')\\'))
                ten_calc_req.append(NoEscape(r'&= ' + str(base_metal_capacity_kN) + r' \text{ kN}\\'))
                ten_calc_req.append(NoEscape(r'&[\text{Ref. Section 3.7, Cl. 6.2, 6.3}]'))
                ten_calc_req.append(NoEscape(r'\end{aligned}'))
                
                ten_status = "PASS" if base_metal_capacity_kN >= axial_kN else "FAIL"
                self.report_check.append(["Base Metal Capacity", axial_kN , ten_calc_req, ten_status])


            # ==========================================================================
            # SECTION 3.8: DETAILING CHECKLIST
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Detailing Checklist", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            # Check 1: Minimum effective weld length
            detail_check_1 = Math(inline=True)
            detail_check_1.append(NoEscape(r'\begin{aligned}'))
            detail_check_1.append(NoEscape(r'L_{eff} &\geq 4s\\'))
            detail_check_1.append(NoEscape(r'' + str(L_eff_provided) + r' &\geq ' + str(4 * weld_size)))
            detail_check_1.append(NoEscape(r'\end{aligned}'))
            detail_status_1 = "PASS" if L_eff_provided >= 4 * weld_size else "FAIL"
            self.report_check.append(["Min. Eff. Length", detail_check_1, "", detail_status_1])

            # Check 2: Minimum weld size
            detail_check_2 = Math(inline=True)
            detail_check_2.append(NoEscape(r'\begin{aligned}'))
            detail_check_2.append(NoEscape(r's &\geq s_{min}\\'))
            detail_check_2.append(NoEscape(r'' + str(weld_size) + r' &\geq ' + str(s_min)))
            detail_check_2.append(NoEscape(r'\end{aligned}'))
            detail_status_2 = "PASS" if weld_size >= s_min else "FAIL"
            self.report_check.append(["Min. Weld Size", detail_check_2, "", detail_status_2])

            # Check 3: Maximum weld size
            detail_check_3 = Math(inline=True)
            detail_check_3.append(NoEscape(r'\begin{aligned}'))
            detail_check_3.append(NoEscape(r's &\leq T_{min} - 1.5\\'))
            detail_check_3.append(NoEscape(r'' + str(weld_size) + r' &\leq ' + str(s_max)))
            detail_check_3.append(NoEscape(r'\end{aligned}'))
            detail_status_3 = "PASS" if weld_size <= s_max else "FAIL"
            self.report_check.append(["Max. Weld Size", detail_check_3, "", detail_status_3])

            # Check 4: Skew angle constraints (if applicable)
            if skew_angle > 0:
                detail_check_4 = Math(inline=True)
                detail_check_4.append(NoEscape(r'\begin{aligned}'))
                detail_check_4.append(NoEscape(r'20^\circ &\leq \alpha \leq 60^\circ\\'))
                detail_check_4.append(NoEscape(r'20^\circ &\leq ' + f'{skew_angle:.1f}' + r'^\circ \leq 60^\circ'))
                detail_check_4.append(NoEscape(r'\end{aligned}'))
                detail_status_4 = "PASS" if 20 <= skew_angle <= 60 else "FAIL"
                self.report_check.append(["Skew Angle Range", detail_check_4, "", detail_status_4])

            # Check 5: Packing plate requirement
            if N_f == 2:
                if abs(plate1_thk - plate2_thk) > 0.001:
                    detail_check_5 = NoEscape(r'\text{Required: } |t_1 - t_2| > 0')
                    detail_prov_5 = f"Provided: {packing_thk} mm"
                    detail_status_5 = "PASS"
                else:
                    detail_check_5 = NoEscape(r'\text{Not required: } t_1 = t_2')
                    detail_prov_5 = "N/A"
                    detail_status_5 = "PASS"
                self.report_check.append(["Packing Plate", detail_check_5, detail_prov_5, detail_status_5])

            # ==========================================================================
            # SECTION 3.9: DETAILING
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Detailing", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            # Length of connection
            conn_len_detail = Math(inline=True)
            conn_len_detail.append(NoEscape(r'\begin{aligned}'))
            conn_len_detail.append(NoEscape(r'L_{provided} &= n_f \times L_{provided\_line}\\'))
            conn_len_detail.append(NoEscape(r'&= ' + str(N_f) + r' \times ' + str(L_provided_line) + r'\\'))
            L_provided_total = f2(N_f * L_provided_line, 0.0)
            conn_len_detail.append(NoEscape(r'&= ' + str(L_provided_total) + r' \text{ mm}'))
            conn_len_detail.append(NoEscape(r'\end{aligned}'))
            self.report_check.append(["Connection Length", "", conn_len_detail, ""])

            # Length of cover plate (with clearance)
            end_clearance = 25  # mm, as per Section 3.8
            L_cover_plate = f2(L_provided_total + 2 * end_clearance, 0.0)
            cover_len_detail = Math(inline=True)
            cover_len_detail.append(NoEscape(r'\begin{aligned}'))
            cover_len_detail.append(NoEscape(r'L_{cp} &= L_{provided} + 2 \times (\text{end clearance})\\'))
            cover_len_detail.append(NoEscape(r'&= ' + str(L_provided_total) + r' + 2 \times ' + str(end_clearance) + r'\\'))
            cover_len_detail.append(NoEscape(r'&= ' + str(L_cover_plate) + r' \text{ mm}'))
            cover_len_detail.append(NoEscape(r'\end{aligned}'))
            self.report_check.append(["Cover Plate Length", "", cover_len_detail, ""])

            # ==========================================================================
            # UTILIZATION RATIO
            # ==========================================================================
            self.report_check.append([
                "SubSection", "Utilization Ratio", "|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|"
            ])

            overall_capacity_kN = min(weld_strength_kN, base_metal_capacity_kN)
            utilization_ratio = f2(axial_kN / overall_capacity_kN if overall_capacity_kN > 0 else 0, 0.0)

            ur_calc = Math(inline=True)
            ur_calc.append(NoEscape(r'\begin{aligned}'))
            ur_calc.append(NoEscape(r'UR &= \frac{P_N}{\min(C_w, T_{db})}\\'))
            ur_calc.append(NoEscape(r'&= \frac{' + str(axial_kN) + r'}{\min(' + str(weld_strength_kN) + r', ' + str(base_metal_capacity_kN) + r')}\\'))
            ur_calc.append(NoEscape(r'&= \frac{' + str(axial_kN) + r'}{' + str(overall_capacity_kN) + r'}\\'))
            ur_calc.append(NoEscape(r'&= ' + str(utilization_ratio) + r'\\'))
            ur_calc.append(NoEscape(r'&[\text{Ref. IS 800:2007}]'))
            ur_calc.append(NoEscape(r'\end{aligned}'))

            ur_status = "PASS" if utilization_ratio <= 1.0 else "FAIL"
            self.report_check.append(["Utilization Ratio", f"{axial_kN:.2f} kN", ur_calc, ur_status])

            # ==========================================================================
            # GENERATE LATEX REPORT
            # ==========================================================================
            Disp_2d_image = []
            Disp_3D_image = "/ResourceFiles/images/3d.png"
            rel_path = os.path.abspath(".").replace("\\", "/")
            fname_no_ext = popup_summary.get("filename", "ButtJointWeldedReport")
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