import unittest
import math
from ....Common import * # Import all KEY_ constants
from ..welded_butt_joint import WeldedButtJoint
# Assuming Plate, Weld, Material classes are accessible if needed for type checking,
# but direct interaction might be through WeldedButtJoint's attributes.

# Mock logger for capturing log messages if required by tests later
import logging
from io import StringIO
# For now, we will focus on calculated values and assume logger works as intended.

# Capture Osdag logger output for tests
osdag_logger = logging.getLogger("osdag") # Should match the name used in WeldedButtJoint
# To prevent log messages from appearing in the console during tests,
# and to have a fresh logger for each test run or class setup.
# If not already configured by Osdag's main entry point, we might need basicConfig.
# However, usually, we just add a handler to the existing logger.

class TestWeldedButtJoint(unittest.TestCase):

    def setUp(self):
        """
        Set up a logger for each test to capture log messages.
        """
        self.log_stream = StringIO()
        self.test_handler = logging.StreamHandler(self.log_stream)
        self.test_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        
        # It's important to get the correct logger instance that the module uses.
        # Assuming WeldedButtJoint uses a logger named 'Osdag' or 'osdag' as per its set_osdaglogger
        self.logger_to_test = logging.getLogger('Osdag') # Match the name in WeldedButtJoint's set_osdaglogger
        
        # Clear existing handlers on this specific logger for test isolation, if any were added by other tests/setups
        # Or, be careful if a global config adds handlers that shouldn't be removed.
        # For now, let's assume we manage handlers per test or test class.
        self.original_handlers = self.logger_to_test.handlers[:]
        self.logger_to_test.handlers = [] # Clear them for this test
        self.logger_to_test.addHandler(self.test_handler)
        self.logger_to_test.setLevel(logging.DEBUG) # Capture all levels for checking

    def tearDown(self):
        """
        Clean up the logger after each test.
        """
        self.logger_to_test.removeHandler(self.test_handler)
        self.test_handler.close()
        # Restore original handlers
        self.logger_to_test.handlers = self.original_handlers


    def test_complete_penetration_butt_weld_safe_design(self):
        """
        Test Case 1: Complete Penetration Butt Weld - Safe Design.
        Verifies throat thickness, weld strength stress, effective length, and logs.
        """
        design_dict = {
            KEY_MODULE: KEY_DISP_WELDEDBUTTJOINT,
            # Plate 1
            KEY_PLATE1_THICKNESS: "12.0", # t1
            KEY_PLATE_WIDTH: "150.0",    # B
            KEY_MATERIAL: "E 250 (Fe 410 W)A", # fy = 250, fu = 410
            # Plate 2
            KEY_PLATE2_THICKNESS: "10.0", # t2
            # Loads
            KEY_TENSILE_FORCE: "100.0", # P (kN)
            # Weld Details
            KEY_WELD_BUTT_TYPE: VALUES_WELD_BUTT_TYPE[0], # 'Complete Penetration Butt Weld'
            KEY_EDGE_PREP_TYPE: VALUES_EDGE_PREP_TYPE[0], # 'Single V-Groove' (t_thicker=12 <= 20mm)
            KEY_BEVEL_ANGLE: "30.0", # Example value
            KEY_ROOT_GAP: "2.0",     # Example value
            # Cover Plate Details (not applicable for this test)
            KEY_COVERPLATE_THICKNESS: "", 
            KEY_CONNECTOR_MATERIAL: ""    
        }

        wb_joint = WeldedButtJoint()
        wb_joint.set_osdaglogger(self.logger_to_test) # Pass the test logger
        wb_joint.set_input_values(design_dict)

        # Verification
        # 1. Butt weld throat thickness (a_butt = min(t1, t2))
        expected_throat_thickness = min(float(design_dict[KEY_PLATE1_THICKNESS]), float(design_dict[KEY_PLATE2_THICKNESS]))
        self.assertAlmostEqual(wb_joint.butt_weld.throat_thickness, expected_throat_thickness, places=3)

        # 2. Butt weld strength stress (fwd_butt based on Eq. 3.6: fu / (sqrt(3)*gamma_mw))
        # Assuming shop weld (gamma_mw = 1.25) and plate1 material for fu
        fu_plate1 = wb_joint.plate1.fu # Should be 410 MPa for E250
        gamma_mw = 1.25 
        expected_fwd_butt = fu_plate1 / (math.sqrt(3) * gamma_mw)
        self.assertAlmostEqual(wb_joint.butt_weld.strength_stress, expected_fwd_butt, places=3)

        # 3. Effective butt weld length (Eq. 3.16: plate width)
        expected_eff_weld_length = float(design_dict[KEY_PLATE_WIDTH])
        self.assertAlmostEqual(wb_joint.butt_weld.effective_length, expected_eff_weld_length, places=3)
        
        # 4. Min effective butt weld length check (>= 40mm)
        # This is implicitly checked by not logging an error/warning.
        # For explicit check, we'd need to check logger output or a status flag.
        # For now, we assume if the above are correct, this internal check also passes for valid inputs.
        self.assertTrue(wb_joint.butt_weld.effective_length >= 40.0)

        # Check logs for edge preparation guidance
        log_contents = self.log_stream.getvalue()
        # Since plate thickness (12mm) is not > 20mm, the specific warning about Single V for thick plates should NOT be present.
        self.assertNotIn("Single V-Groove selected for plate thickness", log_contents)
        self.assertIn("Detailing Note: Ensure termination of butt welds meets IS 800:2007 Cl. 10.5.5", log_contents)
        # No end returns for butt welds themselves, but the general note on fillet end returns might still be there.
        # self.assertIn("Detailing Note: Ensure end returns for fillet welds are provided", log_contents) # This is for fillet welds.

        # TODO: Add assertions for Base Metal Tensile Strength (Tdb) once calculated in main class.
        # TODO: Add assertions for Overall Design Verification (P vs. Capacities) once implemented.

    def test_partial_penetration_double_cover_safe_design_with_packing(self):
        """
        Test Case 2: Partial Penetration Butt Weld with Double Cover Plates - Safe Design, with Packing.
        """
        design_dict = {
            KEY_MODULE: KEY_DISP_WELDEDBUTTJOINT,
            KEY_PLATE1_THICKNESS: "20.0", # t1
            KEY_PLATE_WIDTH: "200.0",    # B
            KEY_MATERIAL: "E 250 (Fe 410 W)A", # Main plate material
            KEY_PLATE2_THICKNESS: "12.0", # t2 (t1 != t2, so packing is needed)
            KEY_TENSILE_FORCE: "150.0", 
            KEY_WELD_BUTT_TYPE: VALUES_WELD_BUTT_TYPE[2], # 'Partial Penetration Butt Weld (Double Cover)'
            KEY_EDGE_PREP_TYPE: VALUES_EDGE_PREP_TYPE[1], # 'Double V-Groove'
            KEY_BEVEL_ANGLE: "45.0",
            KEY_ROOT_GAP: "3.0",
            KEY_COVERPLATE_THICKNESS: "8.0", # Input for cover plate thickness (user might specify or it's calculated)
                                             # The current main code uses a calculated Tcp based on t_min, let's test against that logic.
            KEY_CONNECTOR_MATERIAL: "E 250 (Fe 410 W)A" # Cover plate material
        }
        
        wb_joint = WeldedButtJoint()
        wb_joint.set_osdaglogger(self.logger_to_test)
        wb_joint.fillet_weld_leg_size_cover = 6.0 # Assume a 6mm fillet weld for cover plates
        wb_joint.set_input_values(design_dict)

        t_min_main_plates = min(float(design_dict[KEY_PLATE1_THICKNESS]), float(design_dict[KEY_PLATE2_THICKNESS])) # 12.0mm

        # 1. Cover plate thickness (Tcp from Eq. 3.2: 0.7 * t_min for double cover)
        expected_tcp = 0.7 * t_min_main_plates
        self.assertAlmostEqual(wb_joint.cover_plate.thickness_provided, expected_tcp, places=3)
        self.assertAlmostEqual(wb_joint.cover_plate.thickness, expected_tcp, places=3)

        # 2. Packing plate thickness
        expected_packing_thickness = abs(float(design_dict[KEY_PLATE1_THICKNESS]) - float(design_dict[KEY_PLATE2_THICKNESS]))
        self.assertAlmostEqual(wb_joint.packing_plate_thickness, expected_packing_thickness, places=3)
        if expected_packing_thickness > 0:
            self.assertAlmostEqual(wb_joint.packing_plate_width, float(design_dict[KEY_PLATE_WIDTH]), places=3)
        
        # 3. Packing plate log check (20mm - 12mm = 8mm > 6mm)
        log_contents = self.log_stream.getvalue()
        if expected_packing_thickness > 6.0:
            self.assertIn(f"Packing plate thickness ({expected_packing_thickness} mm) > 6mm.", log_contents)
        
        # 4. Partial penetration butt weld throat thickness (Simplified: 0.7 * t_min_main_plates)
        expected_butt_throat = 0.7 * t_min_main_plates
        self.assertAlmostEqual(wb_joint.butt_weld.throat_thickness, expected_butt_throat, places=3)

        # 5. Partial penetration butt weld strength stress (fwd_butt based on Eq. 3.7: 0.6 * fu / gamma_mw)
        fu_plate1 = wb_joint.plate1.fu
        gamma_mw = 1.25 # Assuming shop weld
        expected_fwd_butt_partial = (0.6 * fu_plate1) / gamma_mw
        self.assertAlmostEqual(wb_joint.butt_weld.strength_stress, expected_fwd_butt_partial, places=3)

        # 6. Fillet weld throat thickness for cover plates (Eq. 3.5: 0.707 * s_fillet)
        s_fillet = wb_joint.fillet_weld_leg_size_cover
        expected_fillet_throat = 0.707 * s_fillet
        self.assertAlmostEqual(wb_joint.cover_fillet_weld_1.throat_thickness, expected_fillet_throat, places=3)
        if wb_joint.cover_fillet_weld_2:
             self.assertAlmostEqual(wb_joint.cover_fillet_weld_2.throat_thickness, expected_fillet_throat, places=3)

        # 7. Fillet weld strength for cover plates (fwd_fillet based on Eq. 3.8: fy_cover / (sqrt(3)*gamma_mw))
        fy_cover = wb_joint.cover_plate.fy
        expected_fwd_fillet = fy_cover / (math.sqrt(3) * gamma_mw)
        self.assertAlmostEqual(wb_joint.cover_fillet_weld_1.strength_stress, expected_fwd_fillet, places=3)
        if wb_joint.cover_fillet_weld_2:
            self.assertAlmostEqual(wb_joint.cover_fillet_weld_2.strength_stress, expected_fwd_fillet, places=3)
            
        # 8. Min/max fillet weld size checks (IS 800 Table 21, t_thinner - 1.5)
        # Fillet joins cover plate (Tcp) to main plate (t1 or t2).
        # For top cover to plate1 (20mm): thinner is Tcp (8.4mm for 12mm t_min)
        # For top cover to plate2 (12mm): thinner is Tcp (8.4mm for 12mm t_min)
        thinner_part_top_vs_p1 = min(wb_joint.cover_plate.thickness, wb_joint.plate1.thickness)
        min_leg_top_p1 = is800_2007.cl_10_5_2_3_min_weld_size(wb_joint.cover_plate.thickness, wb_joint.plate1.thickness)
        self.assertTrue(s_fillet >= min_leg_top_p1)
        max_leg_top_p1 = thinner_part_top_vs_p1 - 1.5
        self.assertTrue(s_fillet <= max_leg_top_p1) # This might fail if s_fillet=6 and Tcp=8.4, max_leg = 6.9

        # 9. Min effective length for fillet welds (4 * s_fillet)
        # Assuming cover_plate.length is set to plate1.width for now (as per current create_3d_model placeholder)
        # or more accurately, the visual_cover_plate_length if that's what fillet weld refers to.
        # The check_min_effective_weld_length uses getattr(self.cover_plate, 'length', self.plate1.width)
        # Let's assume cover_plate.length is not yet explicitly designed for strength, so it defaults to plate1.width
        # A better test would be after cover plate length design is implemented.
        # For now, let's check the log for the info message about deferred check if length isn't set.
        # Or, we can set a mock length for testing this part.
        mock_cover_plate_length_for_test = float(design_dict[KEY_PLATE_WIDTH]) # Use plate width as placeholder
        wb_joint.cover_plate.length = mock_cover_plate_length_for_test # Manually set for test
        
        # Re-run the check after setting length for more direct assertion (or check log if it was deferred)
        # The check is done in set_input_values. To re-check, we'd call it again or make it a standalone callable by tests.
        # For simplicity, let's assume the initial call in set_input_values used the placeholder logic.
        # The log check for "Cover plate length not yet determined" is more robust if length isn't set.
        if not hasattr(wb_joint.cover_plate, 'length_designed_for_strength'): # Imaginary flag
            self.assertIn("Cover plate length not yet determined", log_contents)
        
        # If length *was* set (e.g. to plate width by default in CAD for visual)
        if hasattr(wb_joint.cover_fillet_weld_1, 'effective_length'):
            self.assertTrue(wb_joint.cover_fillet_weld_1.effective_length >= 4 * s_fillet)

    def test_error_insufficient_fillet_weld_size(self):
        """
        Test Case 3: Error for insufficient fillet weld size (violates IS 800 Table 21).
        """
        design_dict = {
            KEY_MODULE: KEY_DISP_WELDEDBUTTJOINT,
            KEY_PLATE1_THICKNESS: "10.0", # Cover plate will be welded to this
            KEY_PLATE_WIDTH: "100.0",
            KEY_MATERIAL: "E 250 (Fe 410 W)A",
            KEY_PLATE2_THICKNESS: "10.0", # Other main plate
            KEY_TENSILE_FORCE: "50.0",
            KEY_WELD_BUTT_TYPE: VALUES_WELD_BUTT_TYPE[1], # Single Cover
            KEY_EDGE_PREP_TYPE: VALUES_EDGE_PREP_TYPE[0],
            KEY_COVERPLATE_THICKNESS: "8.0", # Cover plate thickness itself
            KEY_CONNECTOR_MATERIAL: "E 250 (Fe 410 W)A"
        }
        
        wb_joint = WeldedButtJoint()
        wb_joint.set_osdaglogger(self.logger_to_test)
        # For a 10mm plate, min fillet weld size from Table 21 is 3mm.
        # For an 8mm cover plate welded to a 10mm main plate, the thicker part is 10mm. Min weld is 3mm.
        # If we set fillet_weld_leg_size_cover to 2mm, it should trigger an error.
        wb_joint.fillet_weld_leg_size_cover = 2.0 
        wb_joint.set_input_values(design_dict)

        log_contents = self.log_stream.getvalue()
        self.assertIn("Cover fillet weld leg size (2.0 mm) is less than minimum required (3.0 mm)", log_contents)
        self.assertIn("[ERROR]", log_contents) # Check if it was logged as an ERROR

    def test_error_partial_penetration_butt_weld_throat_too_small(self):
        """
        Test Case 4: Error for partial penetration butt weld throat thickness < 3mm.
        This occurs if 0.7 * min_plate_thickness < 3mm.
        """
        design_dict = {
            KEY_MODULE: KEY_DISP_WELDEDBUTTJOINT,
            KEY_PLATE1_THICKNESS: "4.0", # t1
            KEY_PLATE_WIDTH: "100.0",
            KEY_MATERIAL: "E 250 (Fe 410 W)A",
            KEY_PLATE2_THICKNESS: "4.0", # t2
            KEY_TENSILE_FORCE: "20.0",
            KEY_WELD_BUTT_TYPE: VALUES_WELD_BUTT_TYPE[1], # Partial Penetration (Single Cover, but cover details don't affect this specific check)
            KEY_EDGE_PREP_TYPE: VALUES_EDGE_PREP_TYPE[0],
            KEY_COVERPLATE_THICKNESS: "5.0", # Need some value for cover plate logic to run
            KEY_CONNECTOR_MATERIAL: "E 250 (Fe 410 W)A"
        }

        wb_joint = WeldedButtJoint()
        wb_joint.set_osdaglogger(self.logger_to_test)
        wb_joint.set_input_values(design_dict)

        # Expected throat for partial penetration = 0.7 * min(4,4) = 2.8mm
        # This is < 3mm, so an error should be logged.
        log_contents = self.log_stream.getvalue()
        self.assertIn("Butt weld throat thickness (2.8 mm) is less than minimum required (3.0 mm)", log_contents)
        self.assertIn("[ERROR]", log_contents)

    def test_warning_edge_prep_for_thick_plate_single_v(self):
        """
        Test Case 5: Warning for Single V-Groove on thick plates.
        """
        design_dict = {
            KEY_MODULE: KEY_DISP_WELDEDBUTTJOINT,
            KEY_PLATE1_THICKNESS: "22.0", # t1 > 20mm
            KEY_PLATE_WIDTH: "150.0",    
            KEY_MATERIAL: "E 250 (Fe 410 W)A", 
            KEY_PLATE2_THICKNESS: "22.0", # t2
            KEY_TENSILE_FORCE: "200.0", 
            KEY_WELD_BUTT_TYPE: VALUES_WELD_BUTT_TYPE[0], # Complete Penetration
            KEY_EDGE_PREP_TYPE: VALUES_EDGE_PREP_TYPE[0], # 'Single V-Groove'
            KEY_BEVEL_ANGLE: "30.0",
            KEY_ROOT_GAP: "2.0",     
            KEY_COVERPLATE_THICKNESS: "", 
            KEY_CONNECTOR_MATERIAL: ""    
        }
        wb_joint = WeldedButtJoint()
        wb_joint.set_osdaglogger(self.logger_to_test)
        wb_joint.set_input_values(design_dict)

        log_contents = self.log_stream.getvalue()
        self.assertIn("Single V-Groove selected for plate thickness (22.0 mm) > 20mm.", log_contents)
        self.assertIn("[INFO]", log_contents) # This was logged as INFO in main code

if __name__ == '__main__':
    unittest.main()
