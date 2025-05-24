import math
import logging
import numpy
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2
from .moment_connection import MomentConnection
from ....Common import *
from ....utils.common.component import Plate, Weld # Bolt, Angle, Section (already there but commented out if not used)
from ....utils.common.material import Material
from ....utils.common import is800_2007
from ....cad.items.plate import Plate as PlateCAD
from ....cad.items.groove_weld import GrooveWeld as GrooveWeldCAD
from ....cad.items.fillet_weld import FilletWeld as FilletWeldCAD
# from ....cad.items.nut_bolt_array import NutBoltArray as NutBoltArrayCAD # Not used yet

# Global logger instance
logger = logging.getLogger("osdag")

class WeldedButtJoint(MomentConnection):
    """
    Welded Butt Joint class.
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self.plate1_thickness = None
        self.plate1_width = None
        self.plate1_material_grade = None # Renamed from self.plate1_material
        self.plate2_thickness = None
        # self.plate2_width = None # Assuming same width as plate1 for now
        # self.plate2_material_grade = None # Assuming same material as plate1 for now
        self.tensile_force = None
        self.weld_butt_type = None
        self.edge_prep_type = None
        self.bevel_angle = None
        self.root_gap = None
        self.coverplate_thickness_input = None # Renamed from self.coverplate_thickness
        self.coverplate_material_grade = None # Renamed from self.coverplate_material

        self.plate1 = None
        self.plate2 = None
        self.cover_plate = None
        self.butt_weld = None
        self.cover_fillet_weld_1 = None
        self.cover_fillet_weld_2 = None
        self.packing_plate_thickness = 0.0
        self.packing_plate_width = 0.0
        self.fillet_weld_leg_size_cover = 6 # Default/assumed fillet leg size for cover plate welds
        self.logger = None # Initialize logger instance variable
        self.list_of_cad_objects = [] # For storing CAD model components

    def set_osdaglogger(self,key):
        """
        Set up the logger for the Welded Butt Joint module.
        """
        global logger
        logger = logging.getLogger('Osdag')
        
        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self.logger = logger # Assign to instance variable

    def module_name(self):
        """
        Return a unique key for this module.
        """
        return KEY_DISP_WELDEDBUTTJOINT

    def input_values(self):
        """
        Define the input parameters for the Welded Butt Joint.
        """
        input_values = [
            (KEY_MODULE, KEY_DISP_WELDEDBUTTJOINT, TYPE_MODULE, None, True),
            (None, DISP_TITLE_CM, TYPE_TITLE, None),
            # Plate 1
            (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK_CUSTOMIZED),
            (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None),
            (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL),
            # Plate 2
            (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK_CUSTOMIZED),
            # Loads
            (None, DISP_TITLE_FSL, TYPE_TITLE, None),
            (KEY_TENSILE_FORCE, KEY_DISP_TENSILE_FORCE, TYPE_TEXTBOX, None),
            # Weld Details
            (None, DISP_TITLE_WELD_DETAILS, TYPE_TITLE, None),
            (KEY_WELD_BUTT_TYPE, KEY_DISP_WELD_BUTT_TYPE, TYPE_COMBOBOX, VALUES_WELD_BUTT_TYPE),
            (KEY_EDGE_PREP_TYPE, KEY_DISP_EDGE_PREP_TYPE, TYPE_COMBOBOX, VALUES_EDGE_PREP_TYPE),
            (KEY_BEVEL_ANGLE, KEY_DISP_BEVEL_ANGLE, TYPE_TEXTBOX, None),
            (KEY_ROOT_GAP, KEY_DISP_ROOT_GAP, TYPE_TEXTBOX, None),
            # Cover Plate Details (conditionally visible)
            (KEY_COVERPLATE_THICKNESS, KEY_DISP_COVERPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK_CUSTOMIZED),
            (KEY_CONNECTOR_MATERIAL, KEY_DISP_CONNECTOR_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL),
        ]
        return input_values

    def output_values(self, flag):
        """
        Return an empty list for now.
        """
        return []

    def set_input_values(self, design_dictionary):
        """
        Initialize instance variables from the design dictionary.
        """
        super().set_input_values(design_dictionary)
        self.plate1_thickness = float(design_dictionary.get(KEY_PLATE1_THICKNESS, 0))
        self.plate1_width = float(design_dictionary.get(KEY_PLATE_WIDTH, 0))
        self.plate1_material_grade = design_dictionary.get(KEY_MATERIAL)
        self.plate2_thickness = float(design_dictionary.get(KEY_PLATE2_THICKNESS, 0))
        self.tensile_force = float(design_dictionary.get(KEY_TENSILE_FORCE, 0))
        self.weld_butt_type = design_dictionary.get(KEY_WELD_BUTT_TYPE)
        self.edge_prep_type = design_dictionary.get(KEY_EDGE_PREP_TYPE)
        self.bevel_angle = float(design_dictionary.get(KEY_BEVEL_ANGLE, 0)) if design_dictionary.get(KEY_BEVEL_ANGLE) else 0
        self.root_gap = float(design_dictionary.get(KEY_ROOT_GAP, 0)) if design_dictionary.get(KEY_ROOT_GAP) else 0
        self.coverplate_thickness_input = float(design_dictionary.get(KEY_COVERPLATE_THICKNESS,0)) \
            if design_dictionary.get(KEY_COVERPLATE_THICKNESS) else 0
        self.coverplate_material_grade = design_dictionary.get(KEY_CONNECTOR_MATERIAL)

        # Initialize Plate objects
        self.plate1 = Plate(thickness=self.plate1_thickness, material_grade=self.plate1_material_grade, width=self.plate1_width)
        self.plate2 = Plate(thickness=self.plate2_thickness, material_grade=self.plate1_material_grade, width=self.plate1_width) # Assuming same material and width for plate2

        if self.weld_butt_type in [VALUES_WELD_BUTT_TYPE[1], VALUES_WELD_BUTT_TYPE[2]]: # Single or Double Cover
            self.cover_plate = Plate(material_grade=self.coverplate_material_grade, width=self.plate1_width) # Thickness to be calculated

        # Initialize Weld objects
        # TODO: Get weld fabrication from design preferences (KEY_DP_WELD_FAB)
        assumed_weld_fabrication = KEY_DP_FAB_SHOP # Defaulting to shop weld
        self.butt_weld = Weld(material_grade=self.plate1.material_grade, fabrication=assumed_weld_fabrication)

        if self.cover_plate:
            self.cover_fillet_weld_1 = Weld(material_grade=self.cover_plate.material_grade, fabrication=assumed_weld_fabrication)
            if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[2]: # Double Cover
                self.cover_fillet_weld_2 = Weld(material_grade=self.cover_plate.material_grade, fabrication=assumed_weld_fabrication)

        # Perform calculations
        self.calculate_cover_plate_dims()
        self.calculate_throat_thickness()
        self.calculate_weld_strength()
        # Call check methods
        self.check_weld_sizes()
        self.check_min_effective_weld_length()
        self.log_edge_preparation_guidance() # For Doc Section 3.6.2 & 3.6.4 related notes
        self.create_3d_model() # Create CAD models


    def calculate_cover_plate_dims(self):
        """
        Calculates dimensions for cover plates if applicable. (Doc Section 3.1 & 3.6.5)
        """
        if self.weld_butt_type in [VALUES_WELD_BUTT_TYPE[1], VALUES_WELD_BUTT_TYPE[2]]: # Partial Penetration with Cover
            t_min = min(self.plate1.thickness, self.plate2.thickness)
            if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[1]: # Single Cover
                tcp = 1.2 * t_min # Eq 3.1
            else: # Double Cover
                tcp = 0.7 * t_min # Eq 3.2
            
            # TODO: Round Tcp to higher available plate thickness. For now, using calculated.
            self.cover_plate.thickness_provided = tcp 
            self.cover_plate.thickness = tcp # Also set the 'thickness' attribute
            self.cover_plate.width = self.plate1.width # Assuming cover plate width matches main plate

            if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[2] and self.plate1.thickness != self.plate2.thickness:
                self.packing_plate_thickness = abs(self.plate1.thickness - self.plate2.thickness) # Doc 3.6.5
                self.packing_plate_width = self.plate1.width # Set packing plate width
                if self.packing_plate_thickness > 6.0 and self.logger:
                    self.logger.info(f"Packing plate thickness ({self.packing_plate_thickness} mm) > 6mm. "
                                     f"Additional considerations for fabrication are required as per IS 800:2007 Cl. 10.5.6.")
            
    def calculate_throat_thickness(self):
        """
        Calculates throat thickness for butt and fillet welds. (Doc Section 3.2)
        """
        # Butt Weld
        if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[0]: # Complete Penetration
            self.butt_weld.throat_thickness = min(self.plate1.thickness, self.plate2.thickness) # Eq 3.3
        else: # Partial Penetration (either with or without cover)
            # Assuming a_butt = 0.7 * t_min as penetration_depth is not an input yet.
            # This is a simplification based on the constraint a <= 0.7 * t_min.
            # Ideally, penetration_depth should be based on edge prep and inputs.
            # For partial penetration with cover, this butt weld is between main plates.
            self.butt_weld.throat_thickness = 0.7 * min(self.plate1.thickness, self.plate2.thickness) # Simplified from Eq 3.4
            # If self.weld_butt_type involves cover plates, the throat for the butt weld between main plates
            # might still follow this, or it might be a specific depth if partial penetration is only for main plates.
            # The document isn't perfectly clear if the "partial penetration" in the type refers to main plates or overall joint.
            # Assuming it refers to the weld between main plates.

        # Fillet Welds for Cover Plates
        if self.cover_plate and self.cover_fillet_weld_1:
            # Assume self.fillet_weld_leg_size_cover is set (e.g., in __init__ or from DP)
            # For now, using the default value from __init__
            s_fillet = self.fillet_weld_leg_size_cover
            self.cover_fillet_weld_1.size = s_fillet # Store leg size
            self.cover_fillet_weld_1.throat_thickness = 0.707 * s_fillet # Eq 3.5
            if self.cover_fillet_weld_2:
                self.cover_fillet_weld_2.size = s_fillet
                self.cover_fillet_weld_2.throat_thickness = 0.707 * s_fillet

    def calculate_weld_strength(self):
        """
        Calculates design strength stress for welds. (Doc Section 3.3)
        """
        # TODO: Get gamma_mw from Design Preferences (KEY_DP_WELD_FAB)
        # For now, assuming shop weld
        gamma_mw = 1.25 # IS 800:2007 Table 5, shop weld

        # Butt Weld Strength Stress
        if self.butt_weld:
            if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[0]: # Complete Penetration
                # Assuming plate1 material properties govern if different.
                # Or use the weaker of the two plates if materials can differ.
                self.butt_weld.strength_stress = self.plate1.fu / (math.sqrt(3) * gamma_mw) # Eq 3.6
            else: # Partial Penetration
                self.butt_weld.strength_stress = (0.6 * self.plate1.fu) / gamma_mw # Eq 3.7

        # Fillet Weld Strength Stress for Cover Plates
        if self.cover_plate and self.cover_fillet_weld_1:
            # Using fy of parent metal (cover plate) as per Doc 3.3 for fillet welds.
            # Ensure cover_plate.fy is available (Plate object should handle this via its Material object)
            if self.cover_plate.material and hasattr(self.cover_plate.material, 'fy') and self.cover_plate.material.fy:
                 self.cover_fillet_weld_1.strength_stress = self.cover_plate.fy / (math.sqrt(3) * gamma_mw) # Eq 3.8
                 if self.cover_fillet_weld_2:
                    self.cover_fillet_weld_2.strength_stress = self.cover_plate.fy / (math.sqrt(3) * gamma_mw)
            elif self.logger:
                self.logger.error("Cover plate material FY not available for fillet weld strength calculation.")


    def check_weld_sizes(self):
        """
        Checks minimum and maximum weld sizes as per Doc Section 3.6.1.
        """
        if not self.logger: # Ensure logger is available
            self.set_osdaglogger(None) # Initialize with a default if not set by UI

        # Partial Penetration Butt Welds
        if self.weld_butt_type != VALUES_WELD_BUTT_TYPE[0] and self.butt_weld: # Not Complete Penetration
            amin_butt = 3.0  # mm
            if self.butt_weld.throat_thickness < amin_butt:
                self.logger.error(f"Butt weld throat thickness ({self.butt_weld.throat_thickness} mm) is less than minimum required ({amin_butt} mm).")
            
            t_min_plates = min(self.plate1.thickness, self.plate2.thickness)
            amax_butt = 0.7 * t_min_plates
            if self.butt_weld.throat_thickness > amax_butt:
                 self.logger.warning(f"Butt weld throat thickness ({self.butt_weld.throat_thickness} mm) exceeds recommended max ({amax_butt} mm) for partial penetration based on 0.7*t_min.")

        # Fillet Welds for Cover Plates
        if self.cover_plate and self.cover_fillet_weld_1:
            # Determine the thinner part being joined by the fillet weld
            # If packing plate is present, its thickness might also need consideration depending on detail.
            # Assuming fillet weld connects cover plate to main plate (plate1 or plate2).
            # The check should be against the thickness of the parts being joined by *this specific* fillet weld.
            # If cover plate is welded to plate1:
            thinner_part_at_fillet = min(self.cover_plate.thickness, self.plate1.thickness) 
                                        
            min_leg_size_fillet = is800_2007.cl_10_5_2_3_min_weld_size(self.cover_plate.thickness, self.plate1.thickness)
            if self.cover_fillet_weld_1.size < min_leg_size_fillet:
                self.logger.error(f"Cover fillet weld leg size ({self.cover_fillet_weld_1.size} mm) is less than minimum required ({min_leg_size_fillet} mm) based on IS 800 Table 21.")

            # Max leg size for fillet weld (Cl. 10.5.3.1)
            # For a square edge, max size = thickness of the thinner plate - 1.5 mm
            max_leg_size_fillet = thinner_part_at_fillet - 1.5 
            if self.cover_fillet_weld_1.size > max_leg_size_fillet:
                self.logger.warning(f"Cover fillet weld leg size ({self.cover_fillet_weld_1.size} mm) may exceed maximum recommended ({max_leg_size_fillet} mm) for a square edge on the thinner part.")
            
            if self.cover_fillet_weld_2: # Repeat for second fillet weld if it exists
                 min_leg_size_fillet_2 = is800_2007.cl_10_5_2_3_min_weld_size(self.cover_plate.thickness, self.plate2.thickness) # Assuming plate2 for the other side
                 if self.cover_fillet_weld_2.size < min_leg_size_fillet_2:
                    self.logger.error(f"Second cover fillet weld leg size ({self.cover_fillet_weld_2.size} mm) is less than minimum required ({min_leg_size_fillet_2} mm).")
                 thinner_part_at_fillet_2 = min(self.cover_plate.thickness, self.plate2.thickness)
                 max_leg_size_fillet_2 = thinner_part_at_fillet_2 - 1.5
                 if self.cover_fillet_weld_2.size > max_leg_size_fillet_2:
                    self.logger.warning(f"Second cover fillet weld leg size ({self.cover_fillet_weld_2.size} mm) may exceed maximum recommended ({max_leg_size_fillet_2} mm).")


    def check_min_effective_weld_length(self):
        """
        Checks minimum effective length of welds. (Doc Section 3.6.3)
        """
        if not self.logger: self.set_osdaglogger(None)

        # Butt Welds
        if self.butt_weld and self.plate1:
            self.butt_weld.effective_length = self.plate1.width # Eq. 3.16
            min_L_eff_butt = 40.0 # mm, as per good practice/general code stipulation (though not explicitly in IS 800 for butt weld length in this context, often taken from fillet weld min length)
                                  # Or 4 * throat thickness if we adapt fillet weld rule. Let's stick to 40mm for now as a general minimum.
            if self.butt_weld.effective_length < min_L_eff_butt:
                self.logger.warning(f"Butt weld effective length ({self.butt_weld.effective_length} mm) is less than recommended minimum ({min_L_eff_butt} mm).")

        # Fillet Welds for Cover Plates
        if self.cover_plate and self.cover_fillet_weld_1 and hasattr(self.cover_plate, 'length'):
            # Assuming self.cover_plate.length is determined (e.g., based on strength requirements not yet implemented)
            # For now, let's assume cover_plate.length might be similar to plate width for a simple scenario, or slightly longer.
            # This part needs cover_plate.length to be defined.
            # If not defined, this check cannot be fully performed.
            # As a placeholder, if length is not yet designed, we can't do the end return deduction.
            # Let's assume cover_plate.length would be at least plate1.width for this check to be illustrative.
            # A more robust implementation would ensure cover_plate.length is designed first.
            
            # Placeholder: If cover_plate.length is not explicitly designed, assume it's at least the width for this check.
            # This is a simplification. Proper design would calculate required cover plate length.
            cover_plate_length_for_check = getattr(self.cover_plate, 'length', self.plate1.width) 

            L_eff_fillet = cover_plate_length_for_check - 2 * self.cover_fillet_weld_1.size # Eq. 3.15 (deducting end returns)
            self.cover_fillet_weld_1.effective_length = L_eff_fillet
            
            min_L_eff_fillet_cl_10_5_4_1 = 4 * self.cover_fillet_weld_1.size # Eq 3.12 / IS 800 Cl. 10.5.4.1
            if L_eff_fillet < min_L_eff_fillet_cl_10_5_4_1:
                self.logger.error(f"Cover fillet weld effective length ({L_eff_fillet} mm) is less than minimum required ({min_L_eff_fillet_cl_10_5_4_1} mm).")
            
            if self.cover_fillet_weld_2:
                L_eff_fillet_2 = cover_plate_length_for_check - 2 * self.cover_fillet_weld_2.size
                self.cover_fillet_weld_2.effective_length = L_eff_fillet_2
                min_L_eff_fillet_2_cl_10_5_4_1 = 4 * self.cover_fillet_weld_2.size
                if L_eff_fillet_2 < min_L_eff_fillet_2_cl_10_5_4_1:
                    self.logger.error(f"Second cover fillet weld effective length ({L_eff_fillet_2} mm) is less than minimum ({min_L_eff_fillet_2_cl_10_5_4_1} mm).")
        elif self.cover_plate and self.logger:
             self.logger.info("Cover plate length not yet determined; effective fillet weld length check deferred/simplified.")
    
    def log_edge_preparation_guidance(self):
        """
        Logs guidance related to edge preparation and end returns. (Doc 3.6.2, 3.6.4)
        """
        if not self.logger: self.set_osdaglogger(None)

        if self.edge_prep_type == VALUES_EDGE_PREP_TYPE[0]: # Single V-Groove
            thicker_plate = max(self.plate1.thickness, self.plate2.thickness)
            if thicker_plate > 20.0: # As per doc guideline
                self.logger.info(f"Single V-Groove selected for plate thickness ({thicker_plate} mm) > 20mm. "
                                 f"Consider Double V-Groove for better economy and reduced distortion.")
        
        # Doc 3.6.4 End Returns - general note, actual implementation is in detailing.
        self.logger.info("Detailing Note: Ensure end returns for fillet welds are provided as per IS 800:2007 Cl. 10.5.4.2.")
        self.logger.info("Detailing Note: Ensure termination of butt welds meets IS 800:2007 Cl. 10.5.5 requirements (e.g., use of run-on/run-off tabs).")


    def tab_list(self):
        """
        Return an empty list for now.
        """
        return []

    def get_3d_components(self):
        """
        Return a list of CAD component names and their display methods.
        """
        components = []
        if self.plate1_cad and self.plate2_cad:
            components.append(('Plates', self.call_3D_Plates))
        if hasattr(self, 'butt_weld_cad') and self.butt_weld_cad:
            components.append(('Butt Weld', self.call_3D_ButtWeld))
        if hasattr(self, 'cover_plate_cad_top') and self.cover_plate_cad_top:
            components.append(('Cover Plates', self.call_3D_CoverPlates))
        if hasattr(self, 'packing_plate_cad') and self.packing_plate_cad:
            components.append(('Packing Plate', self.call_3D_PackingPlate))
        if hasattr(self, 'fillet_welds_cad') and self.fillet_welds_cad:
            components.append(('Fillet Welds', self.call_3D_FilletWelds))
        return components
    
    def call_3D_Plates(self, ui, bgcolor):
        """Displays the main plates in the CAD model."""
        if ui.commLogicObj.checkbox_Plates.isChecked():
            ui.commLogicObj.display_3DModel([self.plate1_cad, self.plate2_cad], bgcolor)
        else:
            ui.commLogicObj.hide_shape([self.plate1_cad, self.plate2_cad])

    def call_3D_ButtWeld(self, ui, bgcolor):
        """Displays the butt weld in the CAD model."""
        if hasattr(self, 'butt_weld_cad') and self.butt_weld_cad:
            if ui.commLogicObj.checkbox_Butt_Weld.isChecked(): # Assuming checkbox name
                ui.commLogicObj.display_3DModel([self.butt_weld_cad], bgcolor)
            else:
                ui.commLogicObj.hide_shape([self.butt_weld_cad])
                
    def call_3D_CoverPlates(self, ui, bgcolor):
        """Displays the cover plates in the CAD model."""
        cover_plates_to_display = []
        if hasattr(self, 'cover_plate_cad_top') and self.cover_plate_cad_top:
            cover_plates_to_display.append(self.cover_plate_cad_top)
        if hasattr(self, 'cover_plate_cad_bottom') and self.cover_plate_cad_bottom:
            cover_plates_to_display.append(self.cover_plate_cad_bottom)
        
        if cover_plates_to_display:
            if ui.commLogicObj.checkbox_Cover_Plates.isChecked(): # Assuming checkbox name
                ui.commLogicObj.display_3DModel(cover_plates_to_display, bgcolor)
            else:
                ui.commLogicObj.hide_shape(cover_plates_to_display)

    def call_3D_PackingPlate(self, ui, bgcolor):
        """Displays the packing plate in the CAD model."""
        if hasattr(self, 'packing_plate_cad') and self.packing_plate_cad:
            if ui.commLogicObj.checkbox_Packing_Plate.isChecked(): # Assuming checkbox name
                ui.commLogicObj.display_3DModel([self.packing_plate_cad], bgcolor)
            else:
                ui.commLogicObj.hide_shape([self.packing_plate_cad])
                
    def call_3D_FilletWelds(self, ui, bgcolor):
        """Displays the fillet welds in the CAD model."""
        if hasattr(self, 'fillet_welds_cad') and self.fillet_welds_cad:
            if ui.commLogicObj.checkbox_Fillet_Welds.isChecked(): # Assuming checkbox name
                ui.commLogicObj.display_3DModel(self.fillet_welds_cad, bgcolor)
            else:
                ui.commLogicObj.hide_shape(self.fillet_welds_cad)

    def call_3DModel(self, ui, bgcolor):
        """Displays all CAD components based on their checkbox states."""
        self.call_3D_Plates(ui, bgcolor)
        self.call_3D_ButtWeld(ui, bgcolor)
        self.call_3D_CoverPlates(ui, bgcolor)
        self.call_3D_PackingPlate(ui, bgcolor)
        self.call_3D_FilletWelds(ui, bgcolor)
        # For a general display of all objects if individual checkboxes are not used:
        # ui.commLogicObj.display_3DModel(self.list_of_cad_objects, bgcolor)


    def create_3d_model(self):
        """
        Creates the 3D CAD model of the welded butt joint.
        """
        self.list_of_cad_objects = [] # Reset the list
        self.plate1_cad = None
        self.plate2_cad = None
        self.butt_weld_cad = None
        self.cover_plate_cad_top = None
        self.cover_plate_cad_bottom = None
        self.packing_plate_cad = None
        self.fillet_welds_cad = []

        # Define a visual length for the plates (e.g., 200mm or half width)
        visual_plate_length = 200.0 
        visual_cover_plate_length = 250.0 # Placeholder length for cover plates

        # Plate 1
        if self.plate1:
            origin_p1 = numpy.array([-visual_plate_length / 2.0 - (self.root_gap or 0)/2.0 , -self.plate1.width / 2.0, -self.plate1.thickness / 2.0])
            u_dir_p1 = numpy.array([1.0, 0.0, 0.0])
            w_dir_p1 = numpy.array([0.0, 0.0, 1.0])
            self.plate1_cad = PlateCAD(L=visual_plate_length, W=self.plate1.width, T=self.plate1.thickness,
                                       color='blue', name="Plate1")
            self.plate1_cad.place(origin_p1, u_dir_p1, w_dir_p1)
            self.list_of_cad_objects.append(self.plate1_cad)

        # Plate 2
        if self.plate2:
            origin_p2 = numpy.array([(self.root_gap or 0) / 2.0, -self.plate2.width / 2.0, -self.plate2.thickness / 2.0])
            u_dir_p2 = numpy.array([1.0, 0.0, 0.0])
            w_dir_p2 = numpy.array([0.0, 0.0, 1.0])
            self.plate2_cad = PlateCAD(L=visual_plate_length, W=self.plate2.width, T=self.plate2.thickness,
                                       color='green', name="Plate2")
            self.plate2_cad.place(origin_p2, u_dir_p2, w_dir_p2)
            self.list_of_cad_objects.append(self.plate2_cad)

        # Butt Weld
        if self.butt_weld and self.butt_weld.throat_thickness > 0 and self.plate1 and self.plate2:
            weld_L_along_joint = self.plate1.width 
            weld_T_depth = min(self.plate1.thickness, self.plate2.thickness) 
            weld_B_visual_width = self.root_gap if self.root_gap > 0 else self.butt_weld.throat_thickness 
            if weld_B_visual_width < 2: weld_B_visual_width = 2 # Min visual width for the bead

            # Origin for butt weld centered in the gap, at the bottom-left-front corner of the weld block
            origin_weld = numpy.array([-weld_B_visual_width / 2.0, 
                                       -weld_L_along_joint / 2.0, 
                                       -weld_T_depth / 2.0])
            u_dir_weld = numpy.array([1.0, 0.0, 0.0]) # Along the bead width (gap direction)
            w_dir_weld = numpy.array([0.0, 0.0, 1.0]) # Along the plate thickness (weld depth)
            
            # GrooveWeldCAD(b, h, L) -> (visual_width_across_gap, length_along_joint, depth_of_weld)
            self.butt_weld_cad = GrooveWeldCAD(b=weld_B_visual_width, h=weld_L_along_joint, L=weld_T_depth, color='red', name="ButtWeld")
            self.butt_weld_cad.place(origin_weld, u_dir_weld, w_dir_weld)
            self.list_of_cad_objects.append(self.butt_weld_cad)

        # Cover Plates, Packing Plates, and Fillet Welds
        if self.cover_plate and self.plate1 and self.plate2:
            cp_l = visual_cover_plate_length # Using placeholder length
            cp_w = self.cover_plate.width
            cp_t = self.cover_plate.thickness

            # Top Cover Plate
            origin_cp_top = numpy.array([-cp_l / 2.0, -cp_w / 2.0, self.plate1.thickness / 2.0]) # Initial position on plate1
            if self.packing_plate_thickness > 0 and self.plate1.thickness < self.plate2.thickness: # Packing on plate1
                origin_cp_top[2] += self.packing_plate_thickness
            
            self.cover_plate_cad_top = PlateCAD(L=cp_l, W=cp_w, T=cp_t, color='cyan', name="CoverPlateTop")
            self.cover_plate_cad_top.place(origin_cp_top, numpy.array([1.0,0,0]), numpy.array([0,0,1.0]))
            self.list_of_cad_objects.append(self.cover_plate_cad_top)

            # Fillet welds for Top Cover Plate
            if self.cover_fillet_weld_1 and self.cover_fillet_weld_1.size > 0:
                s = self.cover_fillet_weld_1.size
                # Weld 1: Plate1 side, front edge
                fw_origin1 = numpy.array([-cp_l/2.0, -cp_w/2.0, self.plate1.thickness/2.0])
                self.fillet_welds_cad.append(FilletWeldCAD(b=s, h=s, L=cp_l, color='magenta', name="FilletTopP1Front").place(fw_origin1, numpy.array([0,1,0]), numpy.array([0,0,1.0]))) # Check orientation
                # Weld 2: Plate1 side, back edge
                fw_origin2 = numpy.array([-cp_l/2.0, cp_w/2.0 - s, self.plate1.thickness/2.0]) # Adjusted for weld geo
                self.fillet_welds_cad.append(FilletWeldCAD(b=s, h=s, L=cp_l, color='magenta', name="FilletTopP1Back").place(fw_origin2, numpy.array([0,-1,0]), numpy.array([0,0,1.0])))
                # Weld 3 & 4 on Plate2 side would need similar logic, potentially adjusting for root_gap. This part gets complex quickly due to precise positioning.
                # For now, only adding two illustrative fillet welds per cover plate.

            # Bottom Cover Plate (if double cover)
            if self.weld_butt_type == VALUES_WELD_BUTT_TYPE[2]:
                origin_cp_bottom = numpy.array([-cp_l / 2.0, -cp_w / 2.0, -self.plate1.thickness / 2.0 - cp_t])
                if self.packing_plate_thickness > 0 and self.plate1.thickness < self.plate2.thickness: # Packing on plate1
                     origin_cp_bottom[2] -= self.packing_plate_thickness

                self.cover_plate_cad_bottom = PlateCAD(L=cp_l, W=cp_w, T=cp_t, color='cyan', name="CoverPlateBottom")
                self.cover_plate_cad_bottom.place(origin_cp_bottom, numpy.array([1.0,0,0]), numpy.array([0,0,1.0]))
                self.list_of_cad_objects.append(self.cover_plate_cad_bottom)
                # Add fillet welds for bottom cover plate similarly...

            # Packing Plate
            if self.packing_plate_thickness > 0:
                pp_l = cp_l # Assume same length as cover plate
                pp_w = self.packing_plate_width
                pp_t = self.packing_plate_thickness
                
                if self.plate1.thickness < self.plate2.thickness: # Packing needed on plate1 side
                    # Top packing plate
                    origin_pp_top = numpy.array([-pp_l / 2.0, -pp_w / 2.0, self.plate1.thickness / 2.0])
                    self.packing_plate_cad = PlateCAD(L=pp_l, W=pp_w, T=pp_t, color='yellow', name="PackingPlateTop")
                    self.packing_plate_cad.place(origin_pp_top, numpy.array([1.0,0,0]), numpy.array([0,0,1.0]))
                    self.list_of_cad_objects.append(self.packing_plate_cad)
                    # If double cover, a bottom packing plate might also be needed or the logic adjusted.
                    # Current logic places one packing plate where needed for the top cover.
                elif self.plate2.thickness < self.plate1.thickness: # Packing needed on plate2 side
                    # This scenario's packing plate positioning relative to centered cover plate needs careful thought.
                    # For simplicity, assuming packing is primarily for matching the top surface for the top cover.
                    # A more complex packing might be needed for overall symmetry if that's a design goal.
                    pass # Deferring detailed packing for plate2 side for now.
            
            self.list_of_cad_objects.extend(self.fillet_welds_cad)
