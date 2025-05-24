"""
Design and Detailing Checklist for Welded Butt Joint (DDCL-WBJ)
Implementation as per IS 800:2007 and welding standards

This module implements a comprehensive welded butt joint design system covering:
- Design of Cover Plates (Section 3.1)
- Design of Weld (Section 3.2) 
- Weld Strength Calculations (Section 3.3)
- Base Metal Strength Check (Section 3.4)
- Weld Length Calculations (Section 3.5)
- Detailing Checklist (Section 3.6)
- Detailing Process (Section 3.7)
"""

import math
import logging
import numpy
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2
from .moment_connection import MomentConnection
from ...Common import *
from ...utils.common.component import Plate, Weld
from ...utils.common.material import Material
from ...utils.common import is800_2007
from ...cad.items.plate import Plate as PlateCAD
from ...cad.items.groove_weld import GrooveWeld as GrooveWeldCAD
from ...cad.items.filletweld import FilletWeld as FilletWeldCAD
from ...Report_functions import *

# Define global logger instance at module level
logger = logging.getLogger("osdag")

class CoverPlate:
    """Cover plate component for welded butt joints."""
    def __init__(self, thickness=0.0, length=0.0, width=0.0, material_grade=""):
        self.thickness = thickness
        self.length = length
        self.width = width
        self.material_grade = material_grade
        self.status = False
        self.design_capacity = 0.0

class WeldedButtJoint(MomentConnection):
    """
    Welded Butt Joint design class implementing DDCL-WBJ algorithm.
    
    This class provides comprehensive welded butt joint design covering:
    - Cover plate design and dimensioning
    - Weld design (complete/partial penetration, fillet welds)  
    - Strength calculations per IS 800:2007
    - Base metal strength verification
    - Detailing checklist implementation
    - 3D CAD model generation
    """
    
    def __init__(self):
        super().__init__()
        # Initialize all design parameters and result variables
        self.plate1_thickness = 0.0
        self.plate2_thickness = 0.0
        self.plate1_width = 0.0
        self.plate1_material_grade = None
        self.plate2_material_grade = None
        self.tensile_force = 0.0
        self.weld_butt_type = None
        self.edge_prep_type = None
        self.bevel_angle = 0.0
        self.root_gap = 0.0
        self.coverplate_thickness_input = 0.0
        self.coverplate_material_grade = None
        self.weld_fabrication = None
        self.design_preferences = {}
        self.plate1 = None
        self.plate2 = None
        self.cover_plate = CoverPlate()
        self.butt_weld = None
        self.cover_fillet_weld_1 = None
        self.cover_fillet_weld_2 = None
        self.num_cover_plates = 0
        self.cover_plate_thickness = 0.0
        self.cover_plate_length = 0.0
        self.cover_plate_width = 0.0
        self.cover_plate_status = False
        self.packing_plate_thickness = 0.0
        self.butt_weld_model = None
        self.cover_plate_model = None
        self.fillet_weld_1_model = None
        self.fillet_weld_2_model = None
        self.plate1_model = None
        self.plate2_model = None
        self.plate1_tensile_strength = 0.0
        self.plate2_tensile_strength = 0.0
        self.plate1_yield_strength = 0.0
        self.plate2_yield_strength = 0.0
        self.base_metal_capacity = 0.0
        self.required_weld_length = 0.0
        self.effective_weld_length = 0.0
        self.detailing_checklist = {}
        self.detailing_status = False
        self.connection_length = 0.0
        self.connection_width = 0.0
        self.overall_thickness = 0.0
        self.total_capacity = 0.0
        self.utilization_ratio = 0.0
        self.design_status = False
        self.mainmodule = "Welded Butt Joint Connection"
        self.module = KEY_DISP_WELDEDBUTTJOINT

    def module_name(self):
        return KEY_DISP_WELDEDBUTTJOINT

    def input_values(self):
        """
        Define the input parameters for the Welded Butt Joint connection.
        
        Returns:
            list: List of input parameter tuples defining the UI elements
        """
        input_values = [
            (KEY_MODULE, KEY_DISP_WELDEDBUTTJOINT, TYPE_MODULE, None, True, 'No Validator'),
            (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator'),
            
            # Main Plates
            (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, 
             VALUES_PLATETHK_CUSTOMIZED, True, 'No Validator'),
            (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None, True, 'No Validator'),
            (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator'),
            (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, 
             VALUES_PLATETHK_CUSTOMIZED, True, 'No Validator'),
             
            # Loading
            (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator'),
            (KEY_TENSILE_FORCE, KEY_DISP_TENSILE_FORCE, TYPE_TEXTBOX, None, True, 'No Validator'),
            
            # Weld Configuration
            (None, DISP_TITLE_WELD_DETAILS, TYPE_TITLE, None, True, 'No Validator'),
            (KEY_WELD_BUTT_TYPE, KEY_DISP_WELD_BUTT_TYPE, TYPE_COMBOBOX, 
             VALUES_WELD_BUTT_TYPE, True, 'No Validator'),
            (KEY_EDGE_PREP_TYPE, KEY_DISP_EDGE_PREP_TYPE, TYPE_COMBOBOX, 
             VALUES_EDGE_PREP_TYPE, True, 'No Validator'),
            (KEY_BEVEL_ANGLE, KEY_DISP_BEVEL_ANGLE, TYPE_TEXTBOX, None, True, 'No Validator'),
            (KEY_ROOT_GAP, KEY_DISP_ROOT_GAP, TYPE_TEXTBOX, None, True, 'No Validator'),
            
            # Cover Plate Details (conditionally visible)
            (KEY_COVERPLATE_THICKNESS, KEY_DISP_COVERPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, 
             VALUES_PLATETHK_CUSTOMIZED, True, 'No Validator'),
            (KEY_CONNECTOR_MATERIAL, KEY_DISP_CONNECTOR_MATERIAL, TYPE_COMBOBOX, 
             VALUES_MATERIAL, True, 'No Validator'),
        ]
        return input_values

    def output_values(self, flag):
        """
        Define the output parameters for the Welded Butt Joint connection.
        
        Args:
            flag (bool): True to show calculated values, False to show empty
            
        Returns:
            list: List of output parameter tuples
        """
        out_list = []
        
        # Joint Configuration
        t1 = (None, "Joint Configuration", TYPE_TITLE, None, True)
        out_list.append(t1)
        
        t2 = ("joint_type", "Joint Type", TYPE_TEXTBOX, 
              getattr(self, 'weld_butt_type', '') if flag else '', True)
        out_list.append(t2)
        
        t3 = ("edge_prep", "Edge Preparation", TYPE_TEXTBOX, 
              getattr(self, 'edge_prep_type', '') if flag else '', True)
        out_list.append(t3)
        
        # Cover Plate Design (if applicable)
        if hasattr(self, 'cover_plate') and self.cover_plate and flag:
            t4 = (None, "Cover Plate Design", TYPE_TITLE, None, True)
            out_list.append(t4)
            
            t5 = ("cover_plate_thickness", "Cover Plate Thickness (mm)", TYPE_TEXTBOX, 
                  round(getattr(self.cover_plate, 'thickness', 0), 2) if flag else '', True)
            out_list.append(t5)
            
            t6 = ("cover_plate_length", "Cover Plate Length (mm)", TYPE_TEXTBOX, 
                  round(getattr(self, 'cover_plate_length', 0), 2) if flag else '', True)
            out_list.append(t6)
            
            t7 = ("cover_plate_width", "Cover Plate Width (mm)", TYPE_TEXTBOX, 
                  round(getattr(self, 'cover_plate_width', 0), 2) if flag else '', True)
            out_list.append(t7)
        
        # Weld Design
        t8 = (None, "Weld Design", TYPE_TITLE, None, True)
        out_list.append(t8)
        
        if hasattr(self, 'butt_weld') and self.butt_weld:
            t9 = ("butt_weld_size", "Butt Weld Size (mm)", TYPE_TEXTBOX, 
                  round(getattr(self.butt_weld, 'size', 0), 2) if flag else '', True)
            out_list.append(t9)
            
            t10 = ("butt_weld_capacity", "Butt Weld Capacity (kN)", TYPE_TEXTBOX, 
                   round(getattr(self.butt_weld, 'capacity', 0), 2) if flag else '', True)
            out_list.append(t10)
        
        if hasattr(self, 'cover_fillet_weld_1') and self.cover_fillet_weld_1:
            t11 = ("fillet_weld_size", "Fillet Weld Size (mm)", TYPE_TEXTBOX, 
                   round(getattr(self.cover_fillet_weld_1, 'size', 0), 2) if flag else '', True)
            out_list.append(t11)
            
            t12 = ("fillet_weld_length", "Fillet Weld Length (mm)", TYPE_TEXTBOX, 
                   round(getattr(self, 'effective_weld_length', 0), 2) if flag else '', True)
            out_list.append(t12)
        
        # Design Verification
        t13 = (None, "Design Verification", TYPE_TITLE, None, True)
        out_list.append(t13)
        
        t14 = ("joint_capacity", "Joint Capacity (kN)", TYPE_TEXTBOX, 
               round(getattr(self, 'total_capacity', 0), 2) if flag else '', True)
        out_list.append(t14)
        
        t15 = ("utilization", "Design Utilization", TYPE_TEXTBOX, 
               round(getattr(self, 'utilization_ratio', 0), 3) if flag else '', True)
        out_list.append(t15)
        
        t16 = ("design_status", "Design Status", TYPE_TEXTBOX, 
               "PASS" if flag and getattr(self, 'design_status', False) else "FAIL" if flag else '', True)
        out_list.append(t16)
        
        return out_list
        
        t3 = ("edge_prep", "Edge Preparation", TYPE_TEXTBOX, 
              getattr(self, 'edge_prep_type', '') if flag else '', True)
        out_list.append(t3)
        
        # Cover Plate Design (if applicable)
        if hasattr(self, 'cover_plate') and self.cover_plate and flag:
            t4 = (None, "Cover Plate Design", TYPE_TITLE, None, True)
            out_list.append(t4)
            
            t5 = ("cover_thickness", "Thickness (mm)", TYPE_TEXTBOX, 
                  round(getattr(self.cover_plate, 'thickness', 0), 2) if flag else '', True)
            out_list.append(t5)
            
            t6 = ("cover_length", "Length (mm)", TYPE_TEXTBOX, 
                  round(getattr(self, 'cover_plate_length', 0), 2) if flag else '', True)
            out_list.append(t6)
            
            if getattr(self, 'packing_plate_thickness', 0) > 0:
                t7 = ("packing_thickness", "Packing Plate Thickness (mm)", TYPE_TEXTBOX, 
                      round(self.packing_plate_thickness, 2) if flag else '', True)
                out_list.append(t7)
        
        # Weld Design
        t8 = (None, "Weld Design", TYPE_TITLE, None, True)
        out_list.append(t8)
        
        if hasattr(self, 'butt_weld') and self.butt_weld:
            t9 = ("butt_throat", "Butt Weld Throat Thickness (mm)", TYPE_TEXTBOX, 
                  round(getattr(self.butt_weld, 'throat_thickness', 0), 2) if flag else '', True)
            out_list.append(t9)
            
            t10 = ("butt_strength", "Butt Weld Strength (N/mm)", TYPE_TEXTBOX, 
                   round(getattr(self.butt_weld, 'strength_stress', 0), 2) if flag else '', True)
            out_list.append(t10)
        
        if hasattr(self, 'cover_fillet_weld_1') and self.cover_fillet_weld_1:
            t11 = ("fillet_size", "Fillet Weld Size (mm)", TYPE_TEXTBOX, 
                   round(getattr(self.cover_fillet_weld_1, 'size', 0), 2) if flag else '', True)
            out_list.append(t11)
            
            t12 = ("fillet_strength", "Fillet Weld Strength (N/mm)", TYPE_TEXTBOX, 
                   round(getattr(self.cover_fillet_weld_1, 'strength_stress', 0), 2) if flag else '', True)
            out_list.append(t12)
        
        # Design Verification
        t13 = (None, "Design Verification", TYPE_TITLE, None, True)
        out_list.append(t13)
        
        t14 = ("joint_capacity", "Joint Capacity (kN)", TYPE_TEXTBOX, 
               round(getattr(self, 'total_capacity', 0), 2) if flag else '', True)
        out_list.append(t14)
        
        t15 = ("utilization", "Design Utilization", TYPE_TEXTBOX, 
               round(getattr(self, 'utilization_ratio', 0), 3) if flag else '', True)
        out_list.append(t15)
        
        t16 = ("design_status", "Design Status", TYPE_TEXTBOX, 
               "PASS" if flag and getattr(self, 'design_status', False) else "FAIL" if flag else '', True)
        out_list.append(t16)
        
        return out_list

    def customized_input(self):
        """
        Returns customized input field configurations.
        
        Returns:
            list: List of tuples mapping keys to value provider methods
        """
        list1 = []
        t1 = (KEY_PLATE1_THICKNESS, self.get_plate_thickness_values)
        list1.append(t1)
        t2 = (KEY_PLATE2_THICKNESS, self.get_plate_thickness_values)
        list1.append(t2)
        t3 = (KEY_COVERPLATE_THICKNESS, self.get_plate_thickness_values)
        list1.append(t3)
        return list1
        list1.append(t3)
        return list1

    @staticmethod
    def get_plate_thickness_values():
        """Return available plate thickness values."""
        return VALUES_PLATETHK_CUSTOMIZED

    ###############################################
    # Design Preference Functions
    ###############################################
    def tab_list(self):
        """Define design preference tabs."""
        tabs = []
        tabs.append(("Weld", TYPE_TAB_2, self.weld_values))
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
        return tabs

    def weld_values(self, input_dictionary):
        """Define UI elements for the Weld design preference tab."""
        current_weld_fab = input_dictionary.get(KEY_DP_WELD_FAB, KEY_DP_FAB_SHOP)
        
        weld_prefs = []
        # Weld fabrication (Shop/Field)
        t1 = (KEY_DP_WELD_FAB, KEY_DISP_DP_WELD_FAB, TYPE_COMBOBOX,
              VALUES_WELD_FABRICATION, current_weld_fab)
        weld_prefs.append(t1)
        
        # Weld material grade override
        current_weld_material = input_dictionary.get(KEY_DP_WELD_MATERIAL_G_O, '')
        t2 = (KEY_DP_WELD_MATERIAL_G_O, KEY_DISP_DP_WELD_MATERIAL_G_O, TYPE_TEXTBOX,
              None, current_weld_material)
        weld_prefs.append(t2)
        
        return weld_prefs

    def detailing_values(self, input_dictionary):
        """Define UI elements for the Detailing design preference tab."""
        detailing_prefs = []
        
        # Edge preparation method
        current_edge_type = input_dictionary.get(KEY_DP_DETAILING_EDGE_TYPE, 'Sheared or hand flame cut')
        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX,
              ['Sheared or hand flame cut', 'Rolled, machine-flame cut, sawn and planed'],
              current_edge_type)
        detailing_prefs.append(t1)
        
        # Gap tolerance
        current_gap = input_dictionary.get(KEY_DP_DETAILING_GAP, '3')
        t2 = (KEY_DP_DETAILING_GAP, 'Gap Tolerance (mm)', TYPE_TEXTBOX,
              None, current_gap)
        detailing_prefs.append(t2)
        
        # Corrosive environment
        current_corrosive = input_dictionary.get(KEY_DP_DETAILING_CORROSIVE_INFLUENCES, 'No')
        t3 = (KEY_DP_DETAILING_CORROSIVE_INFLUENCES, 'Corrosive Environment', TYPE_COMBOBOX,
              ['Yes', 'No'], current_corrosive)
        detailing_prefs.append(t3)
        
        return detailing_prefs

    def tab_value_changed(self):
        """Define tab value dependencies."""
        return []

    def edit_tabs(self):
        """Define editable tabs."""
        return []

    def input_dictionary_design_pref(self):
        """Define design preference input dictionary structure."""
        design_input = []
        
        design_input.append(("Weld", TYPE_COMBOBOX, [
            KEY_DP_WELD_FAB,
            KEY_DP_WELD_MATERIAL_G_O
        ]))
        
        design_input.append(("Detailing", TYPE_COMBOBOX, [
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DP_DETAILING_GAP,
            KEY_DP_DETAILING_CORROSIVE_INFLUENCES
        ]))
        
        return design_input

    def input_dictionary_without_design_pref(self):
        """Define input dictionary without design preferences."""
        design_input = []
        
        design_input.append((None, [
            KEY_DP_WELD_FAB,
            KEY_DP_WELD_MATERIAL_G_O,
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DP_DETAILING_GAP,
            KEY_DP_DETAILING_CORROSIVE_INFLUENCES
        ], ''))
        
        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):
        """Get default values for design preferences."""
        # Get material fu for weld material default
        if design_dictionary.get(KEY_MATERIAL, '') != 'Select Material':
            try:
                material_obj = Material(design_dictionary[KEY_MATERIAL], 41)
                fu = str(material_obj.fu)
            except:
                fu = '410'  # Default fu value
        else:
            fu = '410'
        
        defaults = {
            KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP,
            KEY_DP_WELD_MATERIAL_G_O: fu,
            KEY_DP_DETAILING_EDGE_TYPE: 'Sheared or hand flame cut',
            KEY_DP_DETAILING_GAP: '3',
            KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No'
        }
        return defaults.get(key, '')

    def new_material(self, material_key=""):
        """Handle material changes."""
        # This method is called when material selection changes
        # Can be used to update dependent fields or validations
        pass

    def input_value_changed(self):
        """Define input value change handlers."""
        lst = []
        # Add material change handlers if needed
        return lst

    def set_input_values(self, design_dictionary):
        """
        Initialize instance variables from the design dictionary and run the complete DDCL-WBJ algorithm.
        """
        super().set_input_values(design_dictionary)
        self.mainmodule = "Welded Butt Joint Connection"
        self.module = design_dictionary.get(KEY_MODULE, self.module_name())

        # Extract input values
        self.plate1_thickness = float(design_dictionary.get(KEY_PLATE1_THICKNESS, 0))
        self.plate1_width = float(design_dictionary.get(KEY_PLATE_WIDTH, 0))
        self.plate1_material_grade = design_dictionary.get(KEY_MATERIAL)
        self.plate2_thickness = float(design_dictionary.get(KEY_PLATE2_THICKNESS, 0))
        self.tensile_force = float(design_dictionary.get(KEY_TENSILE_FORCE, 0))
        self.weld_butt_type = design_dictionary.get(KEY_WELD_BUTT_TYPE)
        self.edge_prep_type = design_dictionary.get(KEY_EDGE_PREP_TYPE)
        self.bevel_angle = float(design_dictionary.get(KEY_BEVEL_ANGLE, 0)) if design_dictionary.get(KEY_BEVEL_ANGLE) else 0
        self.root_gap = float(design_dictionary.get(KEY_ROOT_GAP, 0)) if design_dictionary.get(KEY_ROOT_GAP) else 0
        self.coverplate_thickness_input = float(design_dictionary.get(KEY_COVERPLATE_THICKNESS, 0)) \
            if design_dictionary.get(KEY_COVERPLATE_THICKNESS) else 0
        self.coverplate_material_grade = design_dictionary.get(KEY_CONNECTOR_MATERIAL)
        
        # Extract design preferences
        self.weld_fabrication = design_dictionary.get(KEY_DP_WELD_FAB, KEY_DP_FAB_SHOP)
        self.design_preferences = {
            KEY_DP_WELD_FAB: self.weld_fabrication,
            KEY_DP_WELD_MATERIAL_G_O: design_dictionary.get(KEY_DP_WELD_MATERIAL_G_O, '410'),
            KEY_DP_DETAILING_EDGE_TYPE: design_dictionary.get(KEY_DP_DETAILING_EDGE_TYPE, 'Sheared or hand flame cut'),
            KEY_DP_DETAILING_GAP: design_dictionary.get(KEY_DP_DETAILING_GAP, '3'),
            KEY_DP_DETAILING_CORROSIVE_INFLUENCES: design_dictionary.get(KEY_DP_DETAILING_CORROSIVE_INFLUENCES, 'No')
        }

        # Initialize Plate objects
        self.plate1 = Plate(thickness=self.plate1_thickness, material_grade=self.plate1_material_grade, width=self.plate1_width)
        self.plate2 = Plate(thickness=self.plate2_thickness, material_grade=self.plate1_material_grade, width=self.plate1_width)

        # Initialize Weld objects
        self.butt_weld = Weld(material_grade=self.plate1.material_grade.fy, fabrication=self.weld_fabrication)

        # Initialize cover plate components if needed
        if self.weld_butt_type in [VALUES_WELD_BUTT_TYPE[1], VALUES_WELD_BUTT_TYPE[2]]:
            # Create cover plate object (dimensions will be calculated later)
            if self.coverplate_material_grade:
                self.cover_plate = Plate(thickness=0, material_grade=self.coverplate_material_grade, width=self.plate1_width)
            else:
                self.cover_plate = Plate(thickness=0, material_grade=self.plate1_material_grade, width=self.plate1_width)
            
            # Initialize fillet welds (properties will be set during design)
            self.cover_fillet_weld_1 = Weld(material_grade=self.cover_plate.material_grade.fy, fabrication=self.weld_fabrication)
            if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[2]:  # Double cover
                self.cover_fillet_weld_2 = Weld(material_grade=self.cover_plate.material_grade.fy, fabrication=self.weld_fabrication)
            else:
                self.cover_fillet_weld_2 = None
        else:
            self.cover_plate = None
            self.cover_fillet_weld_1 = None
            self.cover_fillet_weld_2 = None

        # Run the complete DDCL-WBJ algorithm
        logger.info("Input values set. Running DDCL-WBJ design algorithm...")
        try:
            self.design_connection()
        except Exception as e:
            logger.error(f"Design algorithm failed: {str(e)}")
            self.design_status = False

    # ===================================
    # DDCL-WBJ Algorithm Implementation
    # ===================================
    
    def calculate_cover_plate_dims(self):
        """
        Section 3.1: Design of Cover Plates
        Calculate cover plate dimensions based on weld type and loading.
        """
        logger.info("=== Section 3.1: Design of Cover Plates ===")
        
        if self.weld_butt_type not in [VALUES_WELD_BUTT_TYPE[1], VALUES_WELD_BUTT_TYPE[2]]:
            logger.info("No cover plates required for complete penetration butt weld")
            self.num_cover_plates = 0
            self.cover_plate_status = True
            return
            
        # Determine number of cover plates
        if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[1]:  # Single cover
            self.num_cover_plates = 1
        else:  # Double cover  
            self.num_cover_plates = 2
            
        logger.info(f"Number of cover plates required: {self.num_cover_plates}")
        
        # Calculate cover plate thickness (Section 3.1.2)
        # Cover plate thickness should be >= 75% of thicker plate thickness
        thicker_plate_thickness = max(self.plate1_thickness, self.plate2_thickness)
        min_cover_thickness = 0.75 * thicker_plate_thickness
        
        if self.coverplate_thickness_input > 0:
            # User provided thickness
            self.cover_plate_thickness = self.coverplate_thickness_input
            if self.cover_plate_thickness < min_cover_thickness:
                logger.warning(f"Cover plate thickness {self.cover_plate_thickness}mm is less than recommended minimum {min_cover_thickness:.1f}mm")
        else:
            # Auto-calculate thickness
            available_thicknesses = self.get_plate_thickness_values()
            self.cover_plate_thickness = next((t for t in available_thicknesses if t >= min_cover_thickness), 
                                            available_thicknesses[-1])
            
        logger.info(f"Cover plate thickness: {self.cover_plate_thickness}mm")
        
        # Calculate cover plate dimensions (Section 3.1.3)
        # Width: Same as main plates
        self.cover_plate_width = self.plate1_width
        
        # Length: Based on required weld length + end extensions
        # Minimum lap length = 4 * weld size (assumed 6mm initially)
        assumed_weld_size = 6.0
        min_lap_length = 4 * assumed_weld_size
        end_extension = 2 * assumed_weld_size  # Extension beyond weld
        
        self.cover_plate_length = max(min_lap_length + 2 * end_extension, 150.0)  # Minimum 150mm
        
        logger.info(f"Cover plate dimensions: {self.cover_plate_length}mm x {self.cover_plate_width}mm x {self.cover_plate_thickness}mm")
        
        # Update cover plate object
        if self.cover_plate:
            self.cover_plate.thickness = self.cover_plate_thickness
            self.cover_plate.length = self.cover_plate_length
            self.cover_plate.width = self.cover_plate_width
            
        self.cover_plate_status = True
        
    def design_welds(self):
        """
        Section 3.2: Design of Weld
        Design the appropriate weld type based on joint configuration.
        """
        logger.info("=== Section 3.2: Design of Weld ===")
        
        if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[0]:  # Complete penetration
            self.design_complete_penetration_weld()
        elif self.weld_butt_type == VALUES_WELD_BUTT_TYPE[1]:  # Single cover
            self.design_partial_penetration_weld()
            self.design_cover_plate_fillet_welds()
        else:  # Double cover
            self.design_partial_penetration_weld() 
            self.design_cover_plate_fillet_welds()
            
    def design_complete_penetration_weld(self):
        """
        Section 3.2.1: Complete Penetration Butt Weld Design
        """
        logger.info("Designing complete penetration butt weld")
        
        # Throat thickness = minimum of the two plate thicknesses
        self.butt_weld.throat_thickness = min(self.plate1_thickness, self.plate2_thickness)
        
        # Edge preparation requirements
        thicker_plate = max(self.plate1_thickness, self.plate2_thickness)
        if thicker_plate <= 6:
            recommended_prep = "Square Edge (no preparation required)"
        elif thicker_plate <= 20:
            recommended_prep = "Single V-Groove or Single U-Groove"
        else:
            recommended_prep = "Double V-Groove or Double U-Groove"
            
        logger.info(f"Recommended edge preparation for {thicker_plate}mm thickness: {recommended_prep}")
        
        if self.edge_prep_type and thicker_plate > 20 and "Single" in self.edge_prep_type:
            logger.warning(f"Single groove preparation selected for thick plate ({thicker_plate}mm). Consider double groove preparation.")
            
        # Set weld properties
        self.butt_weld.size = self.butt_weld.throat_thickness
        self.butt_weld.effective_length = self.plate1_width
        
        logger.info(f"Butt weld throat thickness: {self.butt_weld.throat_thickness}mm")
        logger.info(f"Butt weld effective length: {self.butt_weld.effective_length}mm")
        
    def design_partial_penetration_weld(self):
        """
        Section 3.2.2: Partial Penetration Butt Weld Design
        """
        logger.info("Designing partial penetration butt weld")
        
        # Throat thickness based on preparation type and penetration
        min_plate_thickness = min(self.plate1_thickness, self.plate2_thickness)
        
        # For partial penetration, throat thickness is typically 70-80% of thinner plate
        penetration_factor = 0.75  # Conservative value
        self.butt_weld.throat_thickness = penetration_factor * min_plate_thickness
        
        # Set weld properties
        self.butt_weld.size = self.butt_weld.throat_thickness / 0.7  # Approximate leg size
        self.butt_weld.effective_length = self.plate1_width
        
        logger.info(f"Partial penetration butt weld throat thickness: {self.butt_weld.throat_thickness}mm")
        logger.info(f"Partial penetration butt weld effective length: {self.butt_weld.effective_length}mm")
        
    def design_cover_plate_fillet_welds(self):
        """
        Section 3.2.3: Cover Plate Fillet Weld Design
        """
        logger.info("Designing cover plate fillet welds")
        
        # Determine minimum weld size based on thickest part
        max_thickness = max(self.plate1_thickness, self.plate2_thickness, self.cover_plate_thickness)
        
        # Minimum fillet weld size as per Table 21, IS 800:2007
        if max_thickness <= 10:
            min_weld_size = 3
        elif max_thickness <= 20:
            min_weld_size = 5
        elif max_thickness <= 32:
            min_weld_size = 6
        elif max_thickness <= 50:
            min_weld_size = 8
        else:
            min_weld_size = 10
            
        # Maximum weld size = 0.7 * thickness of thinner part being joined
        thinner_thickness = min(self.cover_plate_thickness, min(self.plate1_thickness, self.plate2_thickness))
        max_weld_size = 0.7 * thinner_thickness
        
        # Select weld size
        available_sizes = [3, 4, 5, 6, 8, 10, 12, 16, 20, 25]
        suitable_sizes = [s for s in available_sizes if min_weld_size <= s <= max_weld_size]
        
        if suitable_sizes:
            selected_weld_size = suitable_sizes[0]  # Use minimum suitable size
        else:
            selected_weld_size = min_weld_size
            logger.warning(f"Selected weld size {selected_weld_size}mm may not satisfy maximum size constraint")
            
        # Set fillet weld properties
        self.cover_fillet_weld_1.size = selected_weld_size
        self.cover_fillet_weld_1.throat_thickness = 0.7 * selected_weld_size
        self.cover_fillet_weld_1.effective_length = self.cover_plate_length
        
        if self.cover_fillet_weld_2:  # Double cover plate
            self.cover_fillet_weld_2.size = selected_weld_size
            self.cover_fillet_weld_2.throat_thickness = 0.7 * selected_weld_size
            self.cover_fillet_weld_2.effective_length = self.cover_plate_length
            
        logger.info(f"Cover plate fillet weld size: {selected_weld_size}mm")
        logger.info(f"Cover plate fillet weld throat thickness: {self.cover_fillet_weld_1.throat_thickness}mm")
        
    def calculate_weld_strength(self):
        """
        Section 3.3: Weld Strength Calculations
        Calculate design strength of welds as per IS 800:2007.
        """
        logger.info("=== Section 3.3: Weld Strength Calculations ===")

        # Get material properties
        fu_weld = float(self.design_preferences.get(KEY_DP_WELD_MATERIAL_G_O, '410'))

        # Partial safety factor for welds based on fabrication type
        if self.weld_fabrication_type.lower() == 'shop':
            gamma_mw = 1.25
        else:
            gamma_mw = 1.50

        logger.info(f"Weld material ultimate strength: {fu_weld} MPa")
        logger.info(f"Partial safety factor (γmw): {gamma_mw}")

        # Calculate butt weld strength (Eq. 3.6)
        if self.weld_butt_type in [VALUES_WELD_BUTT_TYPE[0], VALUES_WELD_BUTT_TYPE[1], VALUES_WELD_BUTT_TYPE[2]]:
            self.butt_weld.design_strength = (fu_weld / (3**0.5 * gamma_mw)) * self.butt_weld.throat_thickness * self.butt_weld.effective_length / 1000  # kN

        # Calculate fillet weld strength (if applicable)
        if self.cover_fillet_weld_1:
            fillet_strength_stress = (fu_weld / (3**0.5 * gamma_mw)) * 0.707 * self.cover_fillet_weld_1.size
            self.cover_fillet_weld_1.design_strength = fillet_strength_stress * self.cover_fillet_weld_1.effective_length / 1000  # kN

            if self.cover_fillet_weld_2:
                self.cover_fillet_weld_2.design_strength = fillet_strength_stress * self.cover_fillet_weld_2.effective_length / 1000  # kN

            logger.info(f"Fillet weld design strength stress: {fillet_strength_stress:.2f} MPa")
            logger.info(f"Fillet weld design strength: {self.cover_fillet_weld_1.design_strength:.2f} kN each")
            
    def calculate_base_metal_strength(self):
        """
        Section 3.4: Base Metal Strength Check
        Calculate tensile strength and local yielding of base metals.
        """
        logger.info("=== Section 3.4: Base Metal Strength Check ===")
        
        # Tensile strength of plates (Eq. 3.14)
        self.plate1_tensile_strength = (0.9 * self.plate1.fu * self.plate1_thickness * self.plate1_width) / (1.25 * 1000)  # kN
        self.plate2_tensile_strength = (0.9 * self.plate2.fu * self.plate2_thickness * self.plate2_width) / (1.25 * 1000)  # kN
        
        # Local yielding check (Eq. 3.15)
        self.plate1_yield_strength = (self.plate1.fy * self.plate1_thickness * self.plate1_width) / (1.1 * 1000)  # kN
        self.plate2_yield_strength = (self.plate2.fy * self.plate2_thickness * self.plate2_width) / (1.1 * 1000)  # kN
        
        # Overall base metal capacity
        self.base_metal_capacity = min(self.plate1_tensile_strength, self.plate2_tensile_strength,
                                     self.plate1_yield_strength, self.plate2_yield_strength)
        
        logger.info(f"Plate 1 tensile strength: {self.plate1_tensile_strength:.2f} kN")
        logger.info(f"Plate 2 tensile strength: {self.plate2_tensile_strength:.2f} kN")
        logger.info(f"Plate 1 yield strength: {self.plate1_yield_strength:.2f} kN")
        logger.info(f"Plate 2 yield strength: {self.plate2_yield_strength:.2f} kN")
        logger.info(f"Governing base metal capacity: {self.base_metal_capacity:.2f} kN")
        
    def calculate_weld_lengths(self):
        """
        Section 3.5: Weld Length Calculations
        Calculate required and effective weld lengths.
        """
        logger.info("=== Section 3.5: Weld Length Calculations ===")
        
        # Calculate required weld length based on applied load
        if hasattr(self.butt_weld, 'design_strength') and self.butt_weld.design_strength > 0:
            required_weld_strength = self.tensile_force
            
            if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[0]:  # Complete penetration
                # Full width of plate is effective
                self.required_weld_length = self.plate1_width
                self.effective_weld_length = self.plate1_width
                
            else:  # Partial penetration with cover plates
                # Calculate required length for butt weld component
                butt_strength_per_mm = (self.butt_weld.strength_stress * self.butt_weld.throat_thickness) / 1000
                required_butt_length = self.tensile_force / butt_strength_per_mm if butt_strength_per_mm > 0 else self.plate1_width
                
                # Add fillet weld contribution
                total_fillet_strength = 0
                if self.cover_fillet_weld_1:
                    total_fillet_strength += self.cover_fillet_weld_1.design_strength
                if self.cover_fillet_weld_2:
                    total_fillet_strength += self.cover_fillet_weld_2.design_strength
                    
                # Required length considering both butt and fillet contributions
                self.required_weld_length = max(required_butt_length, self.plate1_width)
                self.effective_weld_length = self.plate1_width
                
            # Check minimum effective length requirements (Eq. 3.17)
            min_effective_length = 40.0  # mm
            if self.effective_weld_length < min_effective_length:
                logger.warning(f"Effective weld length {self.effective_weld_length}mm is less than minimum {min_effective_length}mm")
                
            logger.info(f"Required weld length: {self.required_weld_length:.1f}mm")
            logger.info(f"Effective weld length: {self.effective_weld_length:.1f}mm")
            
    def implement_detailing_checklist(self):
        """
        Section 3.6: Detailing Checklist
        Implement comprehensive detailing requirements.
        """
        logger.info("=== Section 3.6: Detailing Checklist ===")
        
        # Initialize detailing status
        self.detailing_checklist = {
            'weld_size_check': False,
            'edge_preparation': False,
            'effective_length': False,
            'end_returns': False,
            'gap_tolerance': False,
            'packing_plates': False
        }
        
        # 3.6.1: Minimum and Maximum Weld Sizes
        self.check_weld_size_limits()
        
        # 3.6.2: Edge Preparation Requirements
        self.check_edge_preparation()
        
        # 3.6.3: Effective Length Requirements
        self.check_effective_length_requirements()
        
        # 3.6.4: End Returns (for fillet welds)
        self.check_end_returns()
        
        # 3.6.5: Gap Tolerance
        self.check_gap_tolerance()
        
        # 3.6.6: Packing Plates (if required)
        self.check_packing_plates()
        
        # Overall detailing status
        self.detailing_status = all(self.detailing_checklist.values())
        
        if self.detailing_status:
            logger.info("All detailing requirements satisfied")
        else:
            failed_checks = [k for k, v in self.detailing_checklist.items() if not v]
            logger.warning(f"Detailing requirements not satisfied: {failed_checks}")
            
    def check_weld_size_limits(self):
        """Check minimum and maximum weld size requirements."""
        logger.info("Checking weld size limits...")
        
        # For butt welds
        if hasattr(self.butt_weld, 'throat_thickness'):
            min_throat = min(self.plate1_thickness, self.plate2_thickness)
            if self.butt_weld.throat_thickness >= min_throat * 0.7:
                self.detailing_checklist['weld_size_check'] = True
                logger.info("Butt weld size acceptable")
            else:
                logger.warning("Butt weld throat thickness insufficient")
                
        # For fillet welds
        if self.cover_fillet_weld_1:
            max_thickness = max(self.plate1_thickness, self.plate2_thickness, self.cover_plate_thickness)
            thinner_thickness = min(self.cover_plate_thickness, min(self.plate1_thickness, self.plate2_thickness))
            
            # Check minimum size (Table 21, IS 800:2007)
            min_size = 3 if max_thickness <= 10 else (5 if max_thickness <= 20 else 6)
            max_size = 0.7 * thinner_thickness
            
            if min_size <= self.cover_fillet_weld_1.size <= max_size:
                self.detailing_checklist['weld_size_check'] = True
                logger.info("Fillet weld size within acceptable limits")
            else:
                logger.warning(f"Fillet weld size {self.cover_fillet_weld_1.size}mm outside limits [{min_size}-{max_size:.1f}]mm")
                
    def check_edge_preparation(self):
        """Check edge preparation requirements."""
        logger.info("Checking edge preparation requirements...")
        
        edge_type = self.design_preferences.get(KEY_DP_DETAILING_EDGE_TYPE, 'Sheared or hand flame cut')
        
        if 'machine-flame cut' in edge_type.lower() or 'rolled' in edge_type.lower():
            logger.info("Edge preparation meets high quality standards")
            self.detailing_checklist['edge_preparation'] = True
        else:
            logger.info("Standard edge preparation specified")
            self.detailing_checklist['edge_preparation'] = True  # Both are acceptable
            
        # Log specific requirements based on weld type
        if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[0]:
            logger.info("Detailing Note: Ensure proper root opening and backing for complete penetration")
        
    def check_effective_length_requirements(self):
        """Check effective length requirements."""
        logger.info("Checking effective length requirements...")
        
        min_length = 40.0  # mm
        
        if hasattr(self, 'effective_weld_length') and self.effective_weld_length >= min_length:
            self.detailing_checklist['effective_length'] = True
            logger.info(f"Effective weld length {self.effective_weld_length}mm meets minimum requirement")
        else:
            logger.warning("Effective weld length below minimum requirement")
            
    def check_end_returns(self):
        """Check end return requirements for fillet welds."""
        logger.info("Checking end return requirements...")
        
        if self.cover_fillet_weld_1:
            # End returns recommended for fillet welds
            return_length = 2 * self.cover_fillet_weld_1.size
            logger.info(f"Detailing Note: Provide end returns of {return_length}mm for fillet welds")
            
        self.detailing_checklist['end_returns'] = True
        logger.info("Detailing Note: Ensure termination of butt welds meets IS 800:2007 Cl. 10.5.5")
        
    def check_gap_tolerance(self):
        """Check gap tolerance requirements."""
        logger.info("Checking gap tolerance...")
        
        specified_gap = float(self.design_preferences.get(KEY_DP_DETAILING_GAP, '3'))
        max_gap = 3.0  # mm typical maximum
        
        if specified_gap <= max_gap:
            self.detailing_checklist['gap_tolerance'] = True
            logger.info(f"Root gap {specified_gap}mm within acceptable limits")
        else:
            logger.warning(f"Root gap {specified_gap}mm exceeds maximum {max_gap}mm")
            
    def check_packing_plates(self):
        """Check if packing plates are required."""
        logger.info("Checking packing plate requirements...")
        
        thickness_diff = abs(self.plate1_thickness - self.plate2_thickness)
        
        if thickness_diff > 3.0:  # mm
            # Packing plates may be required for large thickness differences
            self.packing_plate_thickness = thickness_diff / 2
            logger.info(f"Consider packing plates of {self.packing_plate_thickness}mm thickness")
        else:
            self.packing_plate_thickness = 0
            
        self.detailing_checklist['packing_plates'] = True
        
    def detailing_process(self):
        """
        Section 3.7: Detailing Process
        Complete detailing workflow and documentation.
        """
        logger.info("=== Section 3.7: Detailing Process ===")
        
        # 3.7.1: Joint Configuration Selection
        self.document_joint_configuration()
        
        # 3.7.2: Dimension Calculations
        self.calculate_final_dimensions()
        
        # 3.7.3: Quality Requirements
        self.specify_quality_requirements()
        
        # 3.7.4: Geometric Tolerances
        self.specify_geometric_tolerances()
        
    def document_joint_configuration(self):
        """Document the selected joint configuration."""
        logger.info("Documenting joint configuration...")
        
        config_summary = f"""
        Joint Configuration:
        - Type: {self.weld_butt_type}
        - Plate 1: {self.plate1_thickness}mm x {self.plate1_width}mm
        - Plate 2: {self.plate2_thickness}mm x {self.plate1_width}mm
        - Applied Load: {self.tensile_force} kN
        """
        
        if self.cover_plate:
            config_summary += f"""
        - Cover Plates: {self.num_cover_plates} @ {self.cover_plate_thickness}mm
        - Cover Plate Dimensions: {self.cover_plate_length}mm x {self.cover_plate_width}mm
        """
            
        logger.info(config_summary)
        
    def calculate_final_dimensions(self):
        """Calculate final connection dimensions."""
        logger.info("Calculating final dimensions...")
        
        # Connection length
        if self.cover_plate:
            self.connection_length = self.cover_plate_length
        else:
            self.connection_length = self.plate1_width  # For butt welds, length = width
            
        # Connection width
        self.connection_width = self.plate1_width
        
        # Overall thickness
        if self.num_cover_plates == 2:
            self.overall_thickness = max(self.plate1_thickness, self.plate2_thickness) + 2 * self.cover_plate_thickness
        elif self.num_cover_plates == 1:
            self.overall_thickness = max(self.plate1_thickness, self.plate2_thickness) + self.cover_plate_thickness
        else:
            self.overall_thickness = max(self.plate1_thickness, self.plate2_thickness)
            
        logger.info(f"Final connection dimensions: {self.connection_length}mm x {self.connection_width}mm")
        logger.info(f"Overall thickness: {self.overall_thickness}mm")
        
    def specify_quality_requirements(self):
        """Specify welding quality requirements."""
        logger.info("Specifying quality requirements...")
        
        # Welding standard
        welding_standard = "IS 816:1969 or AWS D1.1"
        
        # Inspection requirements
        if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[0]:
            inspection_level = "100% Radiographic Testing"
        else:
            inspection_level = "Visual + 10% Radiographic Testing"
            
        # Welding procedure
        corrosive_env = self.design_preferences.get(KEY_DP_DETAILING_CORROSIVE_INFLUENCES, 'No')
        if corrosive_env.lower() == 'yes':
            special_requirements = "Corrosion resistant electrodes required"
        else:
            special_requirements = "Standard structural electrodes acceptable"
            
        logger.info(f"Welding Standard: {welding_standard}")
        logger.info(f"Inspection Level: {inspection_level}")
        logger.info(f"Special Requirements: {special_requirements}")
        
    def specify_geometric_tolerances(self):
        """Specify geometric tolerances for the connection."""
        logger.info("Specifying geometric tolerances...")
        
        # Standard tolerances as per IS 800:2007
        tolerances = {
            'plate_thickness': '±0.5mm',
            'plate_width': '±2.0mm',
            'weld_size': '±1.0mm',
            'root_gap': '±1.0mm',
            'angular_deviation': '±2°'
        }
        
        for param, tolerance in tolerances.items():
            logger.info(f"{param.replace('_', ' ').title()}: {tolerance}")
            
    def design_connection(self):
        """
        Main method implementing the complete DDCL-WBJ algorithm.
        Orchestrates all design steps in proper sequence.
        """
        logger.info("Starting DDCL-WBJ design algorithm...")
        
        try:
            # Section 3.1: Design of Cover Plates
            self.calculate_cover_plate_dims()
            
            # Section 3.2: Design of Weld
            self.design_welds()
            
            # Section 3.3: Weld Strength Calculations
            self.calculate_weld_strength()
            
            # Section 3.4: Base Metal Strength Check
            self.calculate_base_metal_strength()
            
            # Section 3.5: Weld Length Calculations
            self.calculate_weld_lengths()
            
            # Section 3.6: Detailing Checklist
            self.implement_detailing_checklist()
            
            # Section 3.7: Detailing Process
            self.detailing_process()
            
            # Overall capacity verification
            self.verify_overall_capacity()
            
            # Generate design summary
            self.generate_design_summary()
            
            logger.info("DDCL-WBJ design algorithm completed successfully")
            
        except Exception as e:
            logger.error(f"Design algorithm failed: {str(e)}")
            self.design_status = False
            raise
            
    def verify_overall_capacity(self):
        """
        Verify overall connection capacity against applied loads.
        """
        logger.info("=== Overall Capacity Verification ===")
        
        # Calculate total connection capacity
        if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[0]:  # Complete penetration
            self.total_capacity = min(self.butt_weld.design_strength, self.base_metal_capacity)
        else:  # With cover plates
            weld_capacity = self.butt_weld.design_strength if hasattr(self.butt_weld, 'design_strength') else 0
            
            if self.cover_fillet_weld_1:
                weld_capacity += self.cover_fillet_weld_1.design_strength
            if self.cover_fillet_weld_2:
                weld_capacity += self.cover_fillet_weld_2.design_strength
                
            self.total_capacity = min(weld_capacity, self.base_metal_capacity)
            
        # Calculate utilization ratio
        self.utilization_ratio = self.tensile_force / self.total_capacity if self.total_capacity > 0 else float('inf')
        
        # Check adequacy
        if self.utilization_ratio <= 1.0:
            self.design_status = True
            logger.info(f"Design SAFE - Utilization ratio: {self.utilization_ratio:.3f}")
        else:
            self.design_status = False
            logger.error(f"Design UNSAFE - Utilization ratio: {self.utilization_ratio:.3f}")
            
        logger.info(f"Applied load: {self.tensile_force:.2f} kN")
        logger.info(f"Total capacity: {self.total_capacity:.2f} kN")
        
    def generate_design_summary(self):
        """
        Generate comprehensive design summary.
        """
        logger.info("=== Design Summary ===")
        
        summary = f"""
        WELDED BUTT JOINT DESIGN SUMMARY
        ================================

        Input Parameters:
        - Plate 1 Thickness: {self.plate1_thickness} mm
        - Plate 2 Thickness: {self.plate2_thickness} mm
        - Plate Width: {self.plate1_width} mm
        - Material Grade: {self.plate1_material_grade}
        - Applied Tensile Force: {self.tensile_force} kN
        - Edge Preparation Method: {self.edge_preparation_method}
        - Weld Fabrication Type: {self.weld_fabrication_type}
        - Material Grade Overwrite: {self.material_grade_overwrite}

        Design Results:
        - Number of Cover Plates: {getattr(self, 'num_cover_plates', 0)}
        - Cover Plate Thickness: {getattr(self, 'cover_plate_thickness', 'N/A')} mm
        - Cover Plate Length: {getattr(self, 'cover_plate_length', 'N/A')} mm
        - Weld Size: {getattr(self.butt_weld, 'size', 'N/A')} mm
        - Effective Weld Length: {getattr(self, 'effective_weld_length', 'N/A')} mm
        - Connection Length: {getattr(self, 'connection_length', 'N/A')} mm
        - Packing Plate Thickness: {getattr(self, 'packing_plate_thickness', 0)} mm
        - Strength of Weld: {getattr(self.butt_weld, 'design_strength', 'N/A')} kN

        Capacity Check:
        - Total Capacity: {getattr(self, 'total_capacity', 'N/A')} kN
        - Utilization Ratio: {getattr(self, 'utilization_ratio', 'N/A')}
        - Design Status: {'SAFE' if getattr(self, 'design_status', False) else 'UNSAFE'}
        """
        
        logger.info(summary)
        
    ###############################################
    # Additional Required Methods
    ###############################################
    
    @staticmethod
    def func_for_validation(instance, design_inputs):
        """
        Validate the design inputs for the Welded Butt Joint connection.

        Args:
            instance (WeldedButtJoint): The instance of the WeldedButtJoint class.
            design_inputs (dict): The design input parameters.

        Returns:
            str: Error message if validation fails, otherwise an empty string.
        """
        # Ensure the instance has the required attributes
        if not hasattr(instance, 'plate1_thickness'):
            return "Error: 'plate1_thickness' attribute is missing in the instance."

        if instance.plate1_thickness <= 0:
            return "Error: Plate 1 thickness must be greater than 0."

        # Add more validation checks as needed
        return ""

    def create_3d_model(self):
        """
        Create 3D CAD model of the welded butt joint.
        """
        try:
            # Create plate models
            self.create_plate_models()
            
            # Create weld models
            self.create_weld_models()
            
            # Create cover plate models (if applicable)
            if self.cover_plate:
                self.create_cover_plate_models()
                
            logger.info("3D CAD model created successfully")
            
        except Exception as e:
            logger.error(f"3D model creation failed: {str(e)}")
            
    def create_plate_models(self):
        """Create 3D models for main plates."""
        # Plate 1
        self.plate1_model = PlateCAD(L=200, W=self.plate1_width, T=self.plate1_thickness)
        
        # Plate 2 (positioned with gap)
        gap = float(self.design_preferences.get(KEY_DP_DETAILING_GAP, '3'))
        self.plate2_model = PlateCAD(L=200, W=self.plate1_width, T=self.plate2_thickness)
        
    def create_weld_models(self):
        """Create 3D models for welds."""
        if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[0]:  # Complete penetration
            self.butt_weld_model = GrooveWeldCAD(
                b=self.butt_weld.throat_thickness,
                h=10,  # Height for visualization
                L=self.butt_weld.effective_length
            )
        else:  # Partial penetration
            self.butt_weld_model = GrooveWeldCAD(
                b=self.butt_weld.throat_thickness,
                h=8,   # Reduced height for partial penetration
                L=self.butt_weld.effective_length
            )
            
    def create_cover_plate_models(self):
        """Create 3D models for cover plates and fillet welds."""
        if not self.cover_plate:
            return
            
        # Cover plate model
        self.cover_plate_model = PlateCAD(
            L=self.cover_plate_length,
            W=self.cover_plate_width,
            T=self.cover_plate_thickness
        )
        
        # Fillet weld models
        if self.cover_fillet_weld_1:
            self.fillet_weld_1_model = FilletWeldCAD(
                h=self.cover_fillet_weld_1.size,
                b=self.cover_fillet_weld_1.size,
                L=self.cover_fillet_weld_1.effective_length
            )
            
        if self.cover_fillet_weld_2:
            self.fillet_weld_2_model = FilletWeldCAD(
                h=self.cover_fillet_weld_2.size,
                b=self.cover_fillet_weld_2.size,
                L=self.cover_fillet_weld_2.effective_length
            )
            
    def get_3d_components(self):
        """
        Returns a list of 3D CAD model components for visualization in the Osdag GUI.
        """
        components = []
        # Main model (full connection)
        components.append(('Model', self.create_3d_model))
        # Individual components if needed (optional, for more granular control)
        # components.append(('Plate1', self.create_plate_models))
        # components.append(('Weld', self.create_weld_models))
        # components.append(('Cover Plate', self.create_cover_plate_models))
        return components
    
    @staticmethod
    def set_osdaglogger(logger_widget):
        """
        Set the Osdag logger for this module (required by Osdag GUI).
        """
        global logger
        try:
            logger.handlers.clear()
        except Exception:
            pass
        handler = logging.StreamHandler(logger_widget)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info("Osdag logger initialized for WeldedButtJoint.")
