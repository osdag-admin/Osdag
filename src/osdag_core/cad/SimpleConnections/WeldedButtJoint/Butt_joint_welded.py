
import numpy
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BOPAlgo import BOPAlgo_Builder
from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN,Quantity_NOC_GRAY,Quantity_NOC_BLUE1,Quantity_NOC_RED,Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_STEEL
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere

# Import the component classes
import sys
import os

try:
    from ...items.plate import Plate
    from ...items.filletweld import FilletWeld
except ImportError:
    # Fallback for when running the script directly
    # We need to add the 'src' directory to sys.path
    # Path: src/osdag_core/cad/SimpleConnections/WeldedButtJoint/Butt_joint_welded.py
    # Up 4 levels: src
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
    if src_path not in sys.path:
        sys.path.append(src_path)
        
    from osdag_core.cad.items.plate import Plate
    from osdag_core.cad.items.filletweld import FilletWeld

def create_welded_butt_joint(plate1_thickness=4, plate2_thickness=4, cover_thickness=3, plate_width=100, weld_size=6, cover_type="Single-Cover"):

    # --- Top Alignment Logic ---
    MAX_THICKNESS = max(plate1_thickness, plate2_thickness)
    reference_top_z = MAX_THICKNESS / 2.0
    
    plate_length = 1.5 * plate_width
    
    # Create Plate 1
    center_z1 = reference_top_z - (plate1_thickness / 2.0)
    origin1 = numpy.array([0.0, 0.0, center_z1]) 
    uDir1 = numpy.array([0.0, 0.0, 1.0])
    wDir1 = numpy.array([1.0, 0.0, 0.0])
    
    plate1 = Plate(plate_length, plate_width, plate1_thickness)
    plate1.place(origin1, uDir1, wDir1)
    plate1_model = plate1.create_model()
    
    # Create Plate 2
    center_z2 = reference_top_z - (plate2_thickness / 2.0)
    origin2 = numpy.array([0.0, plate_length, center_z2])
    uDir2 = numpy.array([0.0, 0.0, 1.0])
    wDir2 = numpy.array([1.0, 0.0, 0.0])
    
    plate2 = Plate(plate_length, plate_width, plate2_thickness)
    plate2.place(origin2, uDir2, wDir2)
    plate2_model = plate2.create_model()
    
    # --- Cover Plate(s) Logic ---
    
    plates_models = [plate1_model, plate2_model]
    platec_model = None
    platec2_model = None
    packing_plate1_model = None  # Initialize packing plates as None
    packing_plate2_model = None
    
    # 1. Top Cover (Always present)
    # Center Z = Reference Top + Cover_Thickness / 2
    cover_top_center_z = reference_top_z + (cover_thickness / 2.0)
    
    origin3 = numpy.array([0.0, plate_length / 2.0, cover_top_center_z])
    uDir3 = numpy.array([0.0, 0.0, 1.0])
    wDir3 = numpy.array([1.0, 0.0, 0.0])
    
    platec = Plate(plate_length, plate_width, cover_thickness)
    platec.place(origin3, uDir3, wDir3)
    platec_model = platec.create_model()
    plates_models.append(platec_model)
    
    # 2. Bottom Cover (Only if Double-Cover)
    if cover_type == "Double-Cover":
        # Bottom of the main assembly is defined by the thickest plate
        # Reference Top = MAX_THICKNESS / 2.0
        # Reference Bottom = Reference Top - MAX_THICKNESS = -MAX_THICKNESS / 2.0
        reference_bottom_z = reference_top_z - MAX_THICKNESS
        
        # Bottom Cover sits below this level
        # Center Z = Reference Bottom - (Cover_Thickness / 2)
        cover_bottom_center_z = reference_bottom_z - (cover_thickness / 2.0)
        
        origin4 = numpy.array([0.0, plate_length / 2.0, cover_bottom_center_z])
        uDir4 = numpy.array([0.0, 0.0, 1.0])
        wDir4 = numpy.array([1.0, 0.0, 0.0])
        
        platec2 = Plate(plate_length, plate_width, cover_thickness)
        platec2.place(origin4, uDir4, wDir4)
        platec2_model = platec2.create_model()
        plates_models.append(platec2_model)
        
        # --- Create Packing Plates to fill gaps ---
        # A packing plate is needed when a main plate doesn't reach the bottom cover
        # Gap = MAX_THICKNESS - plate_thickness
        
        # Packing plate for Plate 1 side (if plate1 is thinner than MAX_THICKNESS)
        gap1 = MAX_THICKNESS - plate1_thickness
        if gap1 > 0.1:  # Only create if there's a meaningful gap
            packing1_center_z = reference_bottom_z + (gap1 / 2.0)
            
            origin_pack1 = numpy.array([0.0, 0.0, packing1_center_z])
            uDir_pack1 = numpy.array([0.0, 0.0, 1.0])
            wDir_pack1 = numpy.array([1.0, 0.0, 0.0])
            
            # Packing plate has same length and width as the corresponding main plate
            packing1 = Plate(plate_length, plate_width, gap1)
            packing1.place(origin_pack1, uDir_pack1, wDir_pack1)
            packing_plate1_model = packing1.create_model()
            plates_models.append(packing_plate1_model)
        
        # Packing plate for Plate 2 side (if plate2 is thinner than MAX_THICKNESS)
        gap2 = MAX_THICKNESS - plate2_thickness
        if gap2 > 0.1:  # Only create if there's a meaningful gap
            packing2_center_z = reference_bottom_z + (gap2 / 2.0)
            
            origin_pack2 = numpy.array([0.0, plate_length, packing2_center_z])
            uDir_pack2 = numpy.array([0.0, 0.0, 1.0])
            wDir_pack2 = numpy.array([1.0, 0.0, 0.0])
            
            packing2 = Plate(plate_length, plate_width, gap2)
            packing2.place(origin_pack2, uDir_pack2, wDir_pack2)
            packing_plate2_model = packing2.create_model()
            plates_models.append(packing_plate2_model)
    else:
        # Single-Cover: Only Top Cover is created (platec)
        pass

    # --- Create Welds ---
    # We use FilletWeld
    # The FilletWeld class creates a prism. The 'place' Method sets:
    # sec_origin: The corner point of the weld triangle (at the 90 degree vertex)
    # uDir: Direction of the 'b' leg
    # wDir: Direction of the extrude length (L)
    # The 'h' leg is automatically computed as cross(wDir, uDir) * h ? No, let's check class usage.
    # FilletWeld class:
    # vDir = cross(wDir, uDir)
    # a1 = origin
    # a2 = origin + b * uDir
    # a3 = origin + h * vDir
    # So vDir is the 'h' leg direction.
    
    welds_models = []

    # --- Top Welds (Associated with platec) ---
    
    # Weld 1: Transverse weld at the start of Cover Plate (y=0) on Plate 1
    # Location: y=0, z=reference_top_z
    # uDir (Base): -Y (Along plate 1)
    # wDir (Length): -X (From W to 0) -> This gives vDir = +Z
    
    weld1_origin = numpy.array([plate_width, 0.0, reference_top_z])
    weld1_uDir = numpy.array([0.0, -1.0, 0.0]) 
    weld1_wDir = numpy.array([-1.0, 0.0, 0.0]) 
    
    weld1 = FilletWeld(weld_size, weld_size, plate_width)
    weld1.place(weld1_origin, weld1_uDir, weld1_wDir)
    weld1_model = weld1.create_model()
    welds_models.append(weld1_model)

    # Weld 2: Transverse weld at the end of Cover Plate (y=plate_length) on Plate 2
    # Location: y=plate_length, z=reference_top_z
    # uDir (Base): +Y (Along plate 2)
    # wDir (Length): +X (From 0 to W) -> This gives vDir = +Z
    
    weld2_origin = numpy.array([0.0, plate_length, reference_top_z])
    weld2_uDir = numpy.array([0.0, 1.0, 0.0]) 
    weld2_wDir = numpy.array([1.0, 0.0, 0.0]) 
    
    weld2 = FilletWeld(weld_size, weld_size, plate_width)
    weld2.place(weld2_origin, weld2_uDir, weld2_wDir)
    weld2_model = weld2.create_model()
    welds_models.append(weld2_model)
    
    # --- Bottom Welds (Associated with platec2) ---
    if cover_type == "Double-Cover":
        reference_bottom_z = reference_top_z - MAX_THICKNESS
        
        # Weld 3: Transverse weld at start of Bottom Cover (y=0) on Plate 1
        # Location: y=0, z=reference_bottom_z
        # uDir (Base): -Y
        # wDir (Length): +X -> This gives vDir = -Z
        
        weld3_origin = numpy.array([0.0, 0.0, reference_bottom_z])
        weld3_uDir = numpy.array([0.0, -1.0, 0.0])
        weld3_wDir = numpy.array([1.0, 0.0, 0.0])
        
        weld3 = FilletWeld(weld_size, weld_size, plate_width)
        weld3.place(weld3_origin, weld3_uDir, weld3_wDir)
        weld3_model = weld3.create_model()
        welds_models.append(weld3_model)
        
        # Weld 4: Transverse weld at end of Bottom Cover (y=plate_length) on Plate 2
        # Location: y=plate_length, z=reference_bottom_z
        # uDir (Base): +Y
        # wDir (Length): -X -> This gives vDir = -Z
        
        weld4_origin = numpy.array([plate_width, plate_length, reference_bottom_z])
        weld4_uDir = numpy.array([0.0, 1.0, 0.0])
        weld4_wDir = numpy.array([-1.0, 0.0, 0.0])
        
        weld4 = FilletWeld(weld_size, weld_size, plate_width)
        weld4.place(weld4_origin, weld4_uDir, weld4_wDir)
        weld4_model = weld4.create_model()
        welds_models.append(weld4_model)
    else:
        # Single-Cover: No bottom welds
        pass


    # --- Assembly ---
    builder = BOPAlgo_Builder()
    for model in plates_models:
        builder.AddArgument(model)
    
    for weld_model in welds_models:
        builder.AddArgument(weld_model)
    
    builder.Perform()
    assembly = builder.Shape()
    
    return assembly, plate1_model, plate2_model, platec_model, platec2_model, welds_models, packing_plate1_model, packing_plate2_model

if __name__ == "__main__":
    # Test Single Cover
    assembly, plate1, plate2, platec, platec2, welds = create_welded_butt_joint(
        plate1_thickness=14,
        plate2_thickness=14,
        cover_thickness=5,
        plate_width=200,
        weld_size=6,
        cover_type="Double-Cover"
    )

    display, start_display, add_menu, add_function_to_menu = init_display()
    
    display.DisplayShape(plate1, update=True)
    display.DisplayShape(plate2, material=Graphic3d_NOM_ALUMINIUM, update=True)
    display.DisplayShape(platec, material=Graphic3d_NOM_STEEL, update=True)
    
    if platec2:
        display.DisplayShape(platec2, material=Graphic3d_NOM_STEEL, update=True)
    
    for weld in welds:
        display.DisplayShape(weld, color=Quantity_Color(Quantity_NOC_RED), update=True)

    origin_point = BRepPrimAPI_MakeSphere(1).Shape()
    display.DisplayShape(origin_point, color=Quantity_NOC_RED, update=True)
    
    display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])
    display.DisableAntiAliasing()
    display.FitAll()
    start_display()
