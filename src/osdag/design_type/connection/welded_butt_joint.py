"""
Module: welded_butt_joint.py
Date: 2025-05-24

Description:
    WeldedButtJoint is a connection module that represents a welded butt joint connection.
    It inherits from MomentConnection and follows the same structure and design logic as other
    connection modules (e.g., ButtJointBolted, BeamCoverPlate) used in Osdag.
    
Reference:
    - IS 800:2007, Section 10.5 and 10.6 (Welded Connections)
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

class WeldedButtJoint(MomentConnection):
    def __init__(self):
        super(WeldedButtJoint, self).__init__()
        self.design_status = False
        self.weld_throat_thickness = 0.0
        self.weld_design_strength = 0.0
        self.weld_size = 0.0
        self.effective_weld_length = 0.0
        self.provided_weld_length = 0.0
        self.required_weld_length = 0.0
        self.num_cover_plates = 0
        self.calculated_cover_plate_thickness = 0.0
        self.packing_plate_thickness = 0.0
        self.gamma_mw = 1.25  # Default for shop weld

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []
        # Only Weld and Detailing tabs
        tabs.append(("Weld", TYPE_TAB_2, self.weld_values))
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
        return tabs

    def tab_value_changed(self):
        # No tab value dependencies needed
        return []

    def edit_tabs(self):
        return []  # Keep original empty implementation

    def input_dictionary_design_pref(self):
        design_input = []
        
        # Weld preferences
        design_input.append(("Weld", TYPE_COMBOBOX, [
            KEY_DP_WELD_FAB_TYPE,  # For shop/field fabrication
            KEY_DP_MATERIAL_GRADE_OVERWRITE  # For weld material grade
        ]))
        
        # Detailing preferences
        design_input.append(("Detailing", TYPE_COMBOBOX, [
            KEY_DP_DETAILING_EDGE_TYPE,  # For edge preparation method
            KEY_DP_DETAILING_PACKING_PLATE
        ]))
        
        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        
        # Default values for weld and detailing
        design_input.append((None, [
            KEY_DP_WELD_FAB_TYPE,
            KEY_DP_MATERIAL_GRADE_OVERWRITE,
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DP_DETAILING_PACKING_PLATE
        ], ''))
        
        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):
        # Default values as per requirements
        defaults = {
            KEY_DP_WELD_FAB_TYPE: "Shop Weld",
            KEY_DP_MATERIAL_GRADE_OVERWRITE: "No",
            KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
            KEY_DP_DETAILING_PACKING_PLATE: "Yes"
        }
        return defaults.get(key)

    def weld_values(self, input_dictionary):
        values = {
            KEY_DP_WELD_FAB_TYPE: 'Shop Weld',
            KEY_DP_MATERIAL_GRADE_OVERWRITE: 'No'
        }

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        weld = []
        
        # Weld fabrication location
        t1 = (KEY_DP_WELD_FAB_TYPE, "Fabrication", TYPE_COMBOBOX,
            ['Shop Weld', 'Field Weld'],
            values[KEY_DP_WELD_FAB_TYPE])
        weld.append(t1)
        
        # Material grade overwrite option
        t2 = (KEY_DP_MATERIAL_GRADE_OVERWRITE, "Material Grade Overwrite", TYPE_COMBOBOX,
            ['Yes', 'No'],
            values[KEY_DP_MATERIAL_GRADE_OVERWRITE])
        weld.append(t2)
        
        t3 = ("textBrowser", "", TYPE_TEXT_BROWSER, WELD_DESCRIPTION, None)
        weld.append(t3)
        
        return weld

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

        # Packing plate option
        t3 = (KEY_DP_DETAILING_PACKING_PLATE, KEY_DISP_DP_DETAILING_PACKING_PLATE, TYPE_COMBOBOX,
              ['Yes', 'No'], values[KEY_DP_DETAILING_PACKING_PLATE])
        detailing.append(t3)

        t4 = ("textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION_WELDBUTT, None)
        detailing.append(t4)

        return detailing

    ####################################
    # Design Preference Functions End
    ####################################

    def set_osdaglogger(key):
        """
        Function to set Logger for Tension Module
        """
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

        # Module title
        t16 = (KEY_MODULE, KEY_DISP_WELDBUTT, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        # Material section
        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        # Material grade
        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        # Plate thicknesses
        t31 = (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t31)

        t34 = (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t34)

        # Plate width
        t35 = (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None, True, 'Float Validator')
        options_list.append(t35)

        # Cover plate type
        t36 = (KEY_COVER_PLATE, KEY_DISP_COVER_PLATE, TYPE_COMBOBOX, VALUES_COVER_PLATE, True, 'No Validator')
        options_list.append(t36)

        # Forces section
        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        # Tensile force
        t17 = (KEY_TENSILE_FORCE, KEY_DISP_TENSILE_FORCE, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)

        # Weld section
        t9 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        # Weld size
        t10 = (KEY_WELD_SIZE, KEY_DISP_WELD_SIZE, TYPE_COMBOBOX_CUSTOMIZED, VALUES_WELD_SIZE, True, 'No Validator')
        options_list.append(t10)

        # Weld type
        t11 = (KEY_WELD_TYPE, KEY_DISP_WELD_TYPE, TYPE_COMBOBOX, VALUES_WELD_TYPE, True, 'No Validator')
        options_list.append(t11)

        return options_list

    def customized_input(self):
        list1 = []
        t1 = (KEY_WELD_SIZE, self.weld_size_customized)
        list1.append(t1)
        t5 = (KEY_PLATE1_THICKNESS, self.plate_thick_customized)
        list1.append(t5)
        t6 = (KEY_PLATE2_THICKNESS, self.plate_thick_customized)
        list1.append(t6)
        return list1
    
    def weld_size_customized(self):
        weld_size = ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20', '22']
        return weld_size

    def plate_thick_customized(self):
        plt_thk = []
        for thk in PLATE_THICKNESS_SAIL:
            plt_thk.append(str(thk))
        return plt_thk

    def output_values(self, flag):
        out_list = []
        
        # Weld design title
        t4 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t4)
        
        # Weld type
        t2 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX,
              self.weld_type if flag else '', True)
        out_list.append(t2)
        
        # Weld size
        t3 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX,
              self.weld_size if flag else '', True)
        out_list.append(t3)
        
        # Weld throat thickness
        t31 = (KEY_OUT_WELD_THROAT, KEY_OUT_DISP_WELD_THROAT, TYPE_TEXTBOX,
               self.weld_throat_thickness if flag else '', True)
        out_list.append(t31)
        
        # Weld strength
        t8 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
               self.weld_design_strength if flag else '', True)
        out_list.append(t8)
        
        # Effective weld length
        t4 = (KEY_OUT_EFF_WELD_LEN, KEY_OUT_DISP_EFF_WELD_LEN, TYPE_TEXTBOX,
               self.effective_weld_length if flag else '', True)
        out_list.append(t4)
        
        # Connection design title
        t17 = (None, DISP_TITLE_CONN, TYPE_TITLE, None, True)
        out_list.append(t17)
        
        # Utilization ratio
        t29 = (KEY_UTILIZATION_RATIO, KEY_DISP_UTILIZATION_RATIO, TYPE_TEXTBOX,
               self.utilization_ratio if flag else '', True)
        out_list.append(t29)
        
        # Number of cover plates
        t17 = (KEY_OUT_NUM_COVER_PLATES, KEY_OUT_DISP_NUM_COVER_PLATES, TYPE_TEXTBOX,
               self.num_cover_plates if flag else '', True)
        out_list.append(t17)
        
        # Cover plate thickness
        t11 = (KEY_OUT_COVER_PLATE_THK, KEY_OUT_DISP_COVER_PLATE_THK, TYPE_TEXTBOX,
               self.calculated_cover_plate_thickness if flag else '', True) 
        out_list.append(t11)
        
        # Packing plate thickness
        t11 = (KEY_PK_PLTHK, KEY_DISP_PK_PLTHK, TYPE_TEXTBOX,
               self.packing_plate_thickness if flag else '', True) 
        out_list.append(t11)
        
        # Connection length
        t20 = (KEY_OUT_CONN_LEN, KEY_OUT_DISP_CONN_LEN, TYPE_TEXTBOX,
               self.width if flag else '', True)
        out_list.append(t20)
        
        return out_list

    def module_name(self):
        return KEY_DISP_WELDBUTT

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t3 = ('Plate1', self.call_3DPlate1)
        components.append(t3)

        t4 = ('Plate2', self.call_3DPlate2)
        components.append(t4)
        
        t5 = ('Weld', self.call_3DWeld)
        components.append(t5)
        
        if self.num_cover_plates > 0:
            t6 = ('Cover Plate', self.call_3DCoverPlate)
            components.append(t6)

        return components

    def call_3DModel(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Model':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Model", bgcolor)

    def call_3DPlate1(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Plate1':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Plate1", bgcolor)
        
    def call_3DPlate2(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Plate2':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Plate2", bgcolor)

    def call_3DWeld(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Weld':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Weld", bgcolor)
    
    def call_3DCoverPlate(self, ui, bgcolor):
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
        "check valid inputs and empty inputs in input dock"
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
                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_PLATE_WIDTH:
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
        else:
            flag = True

        if flag and flag1 and flag2:
            self.set_input_values(self, design_dictionary)
        else:
            return all_errors
        
    def set_input_values(self, design_dictionary):
        """Initialize components required for welded butt joint design as per IS 800:2007"""
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Welded Butt Joint Connection"
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.tensile_force = float(design_dictionary[KEY_TENSILE_FORCE])
        self.width = float(design_dictionary[KEY_PLATE_WIDTH])
        self.weld_size = float(design_dictionary[KEY_WELD_SIZE])
        self.weld_type = design_dictionary[KEY_WELD_TYPE]
        
        # Initialize plates with material properties
        self.plate1 = Plate(thickness=[design_dictionary[KEY_PLATE1_THICKNESS]],
                        material_grade=design_dictionary[KEY_MATERIAL],
                        width=design_dictionary[KEY_PLATE_WIDTH])
        self.plate2 = Plate(thickness=[design_dictionary[KEY_PLATE2_THICKNESS]],
                            material_grade=design_dictionary[KEY_MATERIAL],
                            width=design_dictionary[KEY_PLATE_WIDTH])
        
        # Set partial safety factor based on fabrication location
        self.fab_location = design_dictionary.get(KEY_DP_WELD_FAB_TYPE, "Shop Weld")
        if self.fab_location == "Shop Weld":
            self.gamma_mw = 1.25
        else:  # Field Weld
            self.gamma_mw = 1.50
        
        # Calculate cover plate and packing plate parameters
        self.cover_plate_type = design_dictionary[KEY_COVER_PLATE]
        self.calculate_cover_plate_params(design_dictionary)
        
        # Calculate weld design parameters
        self.calculate_weld_design(design_dictionary)
        
        # Calculate design capacity and utilization ratio
        self.calculate_design_capacity()
        
        if self.design_status:
            logger.info(": Design is Safe")
        else:
            logger.error(": Design is Not Safe")
        logger.info(" :=========End Of design===========")

    def calculate_cover_plate_params(self, design_dictionary):
        """Calculate cover plate thickness and packing plate parameters as per Cl. 10.2.4.2"""
        plate1_thk = float(self.plate1.thickness[0])
        plate2_thk = float(self.plate2.thickness[0])
        Tmin = min(plate1_thk, plate2_thk)
        
        # Available plate thicknesses
        available_thicknesses = [float(thk) for thk in PLATE_THICKNESS_SAIL]
        
        # Cover plate thickness calculation based on type
        if "double" in self.cover_plate_type.lower():
            self.num_cover_plates = 2
            # Eq. 3.2: Double cover plate thickness = 9/16 * Tmin
            tcp = math.ceil((9.0 / 16.0) * Tmin)
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= tcp],
                default=tcp
            )
            
            # Calculate packing plate if plates have different thickness
            if design_dictionary.get(KEY_DP_DETAILING_PACKING_PLATE, "Yes") == "Yes" and abs(plate1_thk - plate2_thk) > 0.001:
                self.packing_plate_thickness = abs(plate1_thk - plate2_thk)
            else:
                self.packing_plate_thickness = 0.0
                
        elif "single" in self.cover_plate_type.lower():
            self.num_cover_plates = 1
            # Eq. 3.1: Single cover plate thickness = 5/8 * Tmin
            tcp = math.ceil((5.0 / 8.0) * Tmin)
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= tcp],
                default=tcp
            )
            self.packing_plate_thickness = 0.0
        else:
            # Complete penetration butt joint without cover plates
            self.num_cover_plates = 0
            self.calculated_cover_plate_thickness = 0.0
            self.packing_plate_thickness = 0.0

    def calculate_weld_design(self, design_dictionary):
        """Calculate weld throat thickness and strength as per Cl. 10.5 and 10.6"""
        plate1_thk = float(self.plate1.thickness[0])
        plate2_thk = float(self.plate2.thickness[0])
        tmin = min(plate1_thk, plate2_thk)
        fu = self.plate1.fu  # Ultimate tensile strength
        
        # Calculate effective throat thickness based on weld type
        if self.weld_type == "Complete Penetration Butt Weld":
            # Eq. 3.3: For complete penetration, throat equals thinner plate
            self.weld_throat_thickness = tmin
        elif self.weld_type == "Partial Penetration Butt Weld":
            # Eq. 3.4: For partial penetration, throat equals depth - 3mm
            self.weld_throat_thickness = self.weld_size - 3
            # But not more than 0.7 * tmin
            self.weld_throat_thickness = min(self.weld_throat_thickness, 0.7 * tmin)
        else:  # Fillet Weld for cover plates
            # Eq. 3.5: For fillet welds, throat equals 0.707 * leg size
            self.weld_throat_thickness = 0.707 * self.weld_size
        
        # Design strength calculation as per Cl. 10.5.3 and 10.6
        if self.weld_type == "Complete Penetration Butt Weld":
            # Eq. 3.6: Design strength for complete penetration butt weld
            self.weld_design_strength = fu / (math.sqrt(3) * self.gamma_mw)
        elif self.weld_type == "Partial Penetration Butt Weld":
            # Eq. 3.7: Design strength for partial penetration butt weld
            self.weld_design_strength = 0.6 * fu / self.gamma_mw
        else:  # Fillet Weld
            # Eq. 3.8: Design strength for fillet weld
            self.weld_design_strength = fu / (math.sqrt(3) * self.gamma_mw)
        
        # Calculate required and effective weld length
        self.calculate_weld_length()

    def calculate_weld_length(self):
        """Calculate required and effective weld length as per detailing requirements"""
        # Required length calculation
        if self.weld_type == "Complete Penetration Butt Weld" or self.weld_type == "Partial Penetration Butt Weld":
            # Eq. 3.13: Required length for butt weld
            self.required_weld_length = self.tensile_force * 1000 / (self.weld_design_strength * self.weld_throat_thickness * self.width)
        else:  # Fillet weld for cover plates
            # Eq. 3.14: Required length for fillet weld cover plate connection
            self.required_weld_length = self.tensile_force * 1000 / (self.weld_design_strength * self.weld_throat_thickness * self.num_cover_plates)
        
        # Provided weld length equals the width of the plate
        self.provided_weld_length = self.width
        
        # Eq. 3.15/3.16: Effective length calculation
        if self.weld_type in ["Complete Penetration Butt Weld", "Partial Penetration Butt Weld"]:
            self.effective_weld_length = self.provided_weld_length
        else:  # Fillet weld
            self.effective_weld_length = self.provided_weld_length - 2 * self.weld_throat_thickness
        
        # Check for minimum effective length as per Cl. 10.5.4 of IS:800:2007
        min_length = 4 * self.weld_size if self.weld_type == "Fillet Weld" else 40
        
        if self.effective_weld_length < min_length:
            self.design_status = False
            logger.error(f": Effective weld length ({self.effective_weld_length} mm) is less than minimum required ({min_length} mm)")
        else:
            self.design_status = True
            
        # Round values for reporting
        self.weld_throat_thickness = round(self.weld_throat_thickness, 1)
        self.weld_design_strength = round(self.weld_design_strength, 1)
        self.effective_weld_length = round(self.effective_weld_length, 1)
        self.provided_weld_length = round(self.provided_weld_length, 1)
        self.required_weld_length = round(self.required_weld_length, 1)

    def calculate_design_capacity(self):
        """Calculate the design capacity and utilization ratio of the connection"""
        # Base metal strength check as per Cl. 8.2.1
        plate1_thk = float(self.plate1.thickness[0])
        plate2_thk = float(self.plate2.thickness[0])
        
        # Eq. 3.9: Tensile strength of base metal
        Ag = self.width * min(plate1_thk, plate2_thk)
        Tdb1 = Ag * self.plate1.fy / 1.10  # Yielding check
        Tdb2 = 0.9 * Ag * self.plate1.fu / 1.25  # Rupture check
        self.base_metal_capacity = min(Tdb1, Tdb2) / 1000  # Convert to kN
        
        # Weld capacity
        weld_area = self.weld_throat_thickness * self.effective_weld_length
        self.weld_capacity = self.weld_design_strength * weld_area / 1000  # Convert to kN
        
        # Design capacity is the minimum of base metal and weld capacities
        self.design_capacity = min(self.base_metal_capacity, self.weld_capacity)
        
        # Utilization ratio calculation
        self.utilization_ratio = self.tensile_force / self.design_capacity
        
        if self.utilization_ratio > 1.0:
            self.design_status = False
            logger.error(f": Utilization ratio ({self.utilization_ratio:.2f}) exceeds 1.0. Design is not safe.")
        else:
            self.design_status = True
            logger.info(f": Utilization ratio is {self.utilization_ratio:.2f}. Design is safe.")
        
        # Round for display
        self.utilization_ratio = round(self.utilization_ratio, 2)
        self.weld_capacity = round(self.weld_capacity, 2)
        self.base_metal_capacity = round(self.base_metal_capacity, 2)
        self.design_capacity = round(self.design_capacity, 2)
        
    def create_design_report(self, file_path, popup_summary):
        """
        Creates the design report for the welded butt joint
        
        Args:
            file_path: path to save the design report
            popup_summary: whether to show a summary popup
        """
        self.report_status = True
        self.file_name = file_path
        
        # Create design report instance
        design_report = CreateLatex(self.file_name, self.module, self.mainmodule)
        
        # Design summary data
        self.design_status_list = []
        status_name = "Design Status: "
        status = "Safe" if self.design_status else "Fail"
        self.design_status_list.append(status_name)
        self.design_status_list.append(status)
        
        # Call the design report
        design_report.save_design(self.main_material, self.design_status_list, self.get_design_report_data())
        
        # Display summary popup if requested
        if popup_summary:
            self.display_design_report(self.design_status)
    
    def get_design_report_data(self):
        """
        Returns data for design report
        
        Returns:
            design_report_data: Dictionary containing design data for report generation
        """
        design_report_data = {}
        
        # Input data
        design_report_data["Plate 1 thickness"] = self.plate1.thickness[0]
        design_report_data["Plate 2 thickness"] = self.plate2.thickness[0]
        design_report_data["Plate width"] = self.width
        design_report_data["Material"] = self.main_material
        design_report_data["Tensile force"] = self.tensile_force
        design_report_data["Weld type"] = self.weld_type
        design_report_data["Weld size"] = self.weld_size
        design_report_data["Cover plate type"] = self.cover_plate_type
        
        # Output data
        design_report_data["Weld throat thickness"] = self.weld_throat_thickness
        design_report_data["Weld design strength"] = self.weld_design_strength
        design_report_data["Effective weld length"] = self.effective_weld_length
        design_report_data["Weld capacity"] = self.weld_capacity
        design_report_data["Base metal capacity"] = self.base_metal_capacity
        design_report_data["Design capacity"] = self.design_capacity
        design_report_data["Utilization ratio"] = self.utilization_ratio
        design_report_data["Design status"] = "Safe" if self.design_status else "Fail"
        design_report_data["Number of cover plates"] = self.num_cover_plates
        design_report_data["Cover plate thickness"] = self.calculated_cover_plate_thickness
        design_report_data["Packing plate thickness"] = self.packing_plate_thickness
        
        return design_report_data
    
    def display_design_report(self, status):
        """
        Display design report summary dialog
        
        Args:
            status: Design status (safe/fail)
        """
        dialog = MyReport(self)
        dialog.show_name("Welded Butt Joint")
        dialog.show_logo()
        
        # Input section
        dialog.add_section("Input Parameters")
        dialog.add_parameter("Material", self.main_material)
        dialog.add_parameter("Plate 1 thickness", str(self.plate1.thickness[0]) + " mm")
        dialog.add_parameter("Plate 2 thickness", str(self.plate2.thickness[0]) + " mm")
        dialog.add_parameter("Plate width", str(self.width) + " mm")
        dialog.add_parameter("Tensile force", str(self.tensile_force) + " kN")
        dialog.add_parameter("Weld type", self.weld_type)
        dialog.add_parameter("Weld size", str(self.weld_size) + " mm")
        
        # Output section
        dialog.add_section("Design Results")
        dialog.add_parameter("Weld throat thickness", str(self.weld_throat_thickness) + " mm")
        dialog.add_parameter("Weld design strength", str(self.weld_design_strength) + " MPa")
        dialog.add_parameter("Effective weld length", str(self.effective_weld_length) + " mm")
        dialog.add_parameter("Design capacity", str(self.design_capacity) + " kN")
        dialog.add_parameter("Utilization ratio", str(self.utilization_ratio))
        dialog.add_parameter("Design status", "Safe" if status else "Fail")
        
        dialog.show()
        
    def load_comm_logic_controller(self, ui, folder, main, joint_type):
        """
        This function initializes the common logic controller for 3D CAD model visualization
        
        Args:
            ui: User interface object
            folder: Folder location for model generation
            main: Main module
            joint_type: Type of the butt joint
        """
        from ...cad.common_logic import CommonDesignLogic
        from ...cad.connections.welded_butt_joint_cad import WeldedButtJointCad
        from ...cad.items.plate import Plate
        from ...cad.items.filletweld import FilletWeld
        from ...cad.items.groove_weld import GrooveWeld
        
        ui.commLogicObj = CommonDesignLogic(ui, folder, main)
        ui.commLogicObj.ui = ui
        
        # Create component models
        plate1 = Plate(length=self.plate1.length[0], width=self.width, 
                        thickness=self.plate1.thickness[0])
        plate2 = Plate(length=self.plate2.length[0], width=self.width, 
                        thickness=self.plate2.thickness[0])
        
        # Create cover plates if needed
        cover_plates = []
        if self.num_cover_plates > 0:
            for i in range(self.num_cover_plates):
                cp = Plate(length=self.plate1.length[0] + self.plate2.length[0],
                           width=self.width, thickness=self.calculated_cover_plate_thickness)
                cover_plates.append(cp)
        
        # Create packing plate if needed
        packing_plate = None
        if self.packing_plate_thickness > 0:
            packing_plate = Plate(length=min(self.plate1.length[0], self.plate2.length[0]),
                                 width=self.width, thickness=self.packing_plate_thickness)
        
        # Create weld based on type
        if self.weld_type in ["Complete Penetration Butt Weld", "Partial Penetration Butt Weld"]:
            weld = GrooveWeld(b=self.weld_size, h=self.weld_throat_thickness, L=self.width)
        else:  # Fillet weld for cover plates
            weld = FilletWeld(b=self.weld_size, h=self.weld_throat_thickness, L=self.width)
        
        # Initialize the CAD model creator
        butt_joint_cad = WeldedButtJointCad(
            connection_type=self.weld_type,
            plate1=plate1,
            plate2=plate2,
            weld=weld,
            cover_plates=cover_plates,
            packing_plate=packing_plate
        )
        butt_joint_cad.create_3DModel()
        
        # Register components for display
        ui.commLogicObj.models = {
            "Model": butt_joint_cad.get_models(),
            "Plate1": butt_joint_cad.get_plate_models()[0],
            "Plate2": butt_joint_cad.get_plate_models()[1],
            "Weld": butt_joint_cad.get_weld_models()
        }
        
        if butt_joint_cad.get_cover_plate_models():
            ui.commLogicObj.models["Cover Plate"] = butt_joint_cad.get_cover_plate_models()
        
        if butt_joint_cad.get_packing_plate_model():
            ui.commLogicObj.models["Packing Plate"] = butt_joint_cad.get_packing_plate_model()[0]
