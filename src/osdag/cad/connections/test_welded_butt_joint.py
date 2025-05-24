"""
Test module for welded butt joint to verify 3D model generation
"""

from ...utils.common.component import Plate
from ...utils.common.material import Material
from ..items.filletweld import FilletWeld
from ..items.groove_weld import GrooveWeld
from .welded_butt_joint_cad import WeldedButtJointCad
import numpy

from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import Quantity_NOC_BLUE1, Quantity_NOC_RED, Quantity_NOC_GREEN

def test_welded_butt_joint_3d():
    """
    Test function to create and display 3D models of different types of welded butt joints
    """
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    # Test case 1: Complete Penetration Butt Weld
    def test_complete_penetration():
        # Create plates
        plate1 = Plate(L=200, W=100, T=12)
        plate2 = Plate(L=200, W=100, T=12)
        
        # Create weld
        weld = GrooveWeld(b=12, h=12, L=100)
        
        # Create CAD model
        butt_joint = WeldedButtJointCad("Complete Penetration Butt Weld", plate1, plate2, weld)
        butt_joint.create_3DModel()
        
        # Get models for display
        plates = butt_joint.get_plate_models()
        welds = butt_joint.get_weld_models()
        
        # Display models
        for plate in plates:
            display.DisplayShape(plate, color=Quantity_NOC_BLUE1, update=True)
        
        for weld in welds:
            display.DisplayShape(weld, color=Quantity_NOC_RED, update=True)
        
        display.FitAll()
        
    # Test case 2: Double Cover Plate Butt Joint with Fillet Welds
    def test_double_cover_plate():
        # Create plates
        plate1 = Plate(L=200, W=100, T=10)
        plate2 = Plate(L=200, W=100, T=12)
        
        # Create cover plates
        cover_plate_top = Plate(L=400, W=100, T=8)
        cover_plate_bottom = Plate(L=400, W=100, T=8)
        
        # Create packing plate
        packing_plate = Plate(L=10, W=100, T=2)
        
        # Create weld
        weld = FilletWeld(b=6, h=6, L=100)
        
        # Create CAD model
        butt_joint = WeldedButtJointCad("Cover Plate Butt Joint", plate1, plate2, weld, 
                                        [cover_plate_top, cover_plate_bottom], packing_plate)
        butt_joint.create_3DModel()
        
        # Get models for display
        plates = butt_joint.get_plate_models()
        welds = butt_joint.get_weld_models()
        cover_plates = butt_joint.get_cover_plate_models()
        packing_plate = butt_joint.get_packing_plate_model()
        
        # Display models
        for plate in plates:
            display.DisplayShape(plate, color=Quantity_NOC_BLUE1, update=True)
        
        for weld in welds:
            display.DisplayShape(weld, color=Quantity_NOC_RED, update=True)
            
        for cp in cover_plates:
            display.DisplayShape(cp, color=Quantity_NOC_GREEN, update=True)
            
        for pp in packing_plate:
            display.DisplayShape(pp, color=Quantity_NOC_BLUE1, update=True)
        
        display.FitAll()
    
    # Add menu items for the test cases
    add_menu('Welded Butt Joint Tests')
    add_function_to_menu('Welded Butt Joint Tests', test_complete_penetration)
    add_function_to_menu('Welded Butt Joint Tests', test_double_cover_plate)
    
    start_display()

if __name__ == '__main__':
    test_welded_butt_joint_3d()
