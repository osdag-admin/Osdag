import numpy
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.BOPAlgo import BOPAlgo_Builder
from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN,Quantity_NOC_GRAY,Quantity_NOC_BLUE1,Quantity_NOC_RED,Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_STEEL
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
# Import the component classes
from ...items.bolt import Bolt
from ...items.nut import Nut
from ...items.plate import Plate



def create_bolted_butt_joint(plate1_thickness = 4, plate2_thickness = 4,cover_thickness=3, plate_width = 100, bolt_dia = 16,
                            bolt_rows=3,bolt_cols=7,pitch=20,gauge=20,edge=12,end=13.6,number_bolts=7, cover_type="Single-Cover"):

    # --- Top Alignment Logic ---
    # We want the TOP surfaces of both plates to be at the same level.
    # Let's define the "Reference Top Level" relative to the global origin Z=0.
    # If the thickest plate is centered at Z=0 (from -MAX/2 to MAX/2), its top is at MAX/2.
    # So, Reference Top = MAX_THICKNESS / 2.0.
    
    MAX_THICKNESS = max(plate1_thickness, plate2_thickness)
    reference_top_z = MAX_THICKNESS / 2.0
    
    # Calculate cover plate length based on the formula: 2 * [(2*end) + (cols-1)*pitch]
    # bolt_cols is the number of columns on ONE side of the joint
    cover_plate_length = 2 * ((2 * end) + (bolt_cols - 1) * pitch)
    
    plate_length =  1.25 * cover_plate_length  #initially i had set it as 2 * cover_plate_length
    
    nut_thickness = 3.0
    # Bolt parameters
    bolt_head_radius = bolt_dia/2
    bolt_head_thickness = 3.0
    # Bolt length must encompass the thickest path:
    # Single-Cover: Max(T) + Cover + Head + Nut
    # Double-Cover: Max(T) + 2*Cover + Head + Nut (bolt goes through both cover plates)
    if cover_type == "Double-Cover":
        bolt_length = MAX_THICKNESS + (2 * cover_thickness) + bolt_head_thickness + nut_thickness + 10.0
    else:
        bolt_length = MAX_THICKNESS + cover_thickness + bolt_head_thickness + nut_thickness + 10.0
    bolt_shaft_radius = 1.5
    
    # Nut parameters
    nut_radius = bolt_head_radius
    nut_height = bolt_head_radius
    nut_inner_radius = bolt_shaft_radius
    
    # Create Plate 1
    # Top surface must be at reference_top_z.
    # Plate 1 extends from (Top - T1) to Top.
    # Center Z1 = Top - T1/2.
    center_z1 = reference_top_z - (plate1_thickness / 2.0)
    
    origin1 = numpy.array([0.0, 0.0, center_z1]) 
    uDir1 = numpy.array([0.0, 0.0, 1.0])
    wDir1 = numpy.array([1.0, 0.0, 0.0])
    
    plate1 = Plate(plate_length, plate_width, plate1_thickness)
    plate1.place(origin1, uDir1, wDir1)
    plate1_model = plate1.create_model()
    
    # Create Plate 2
    # Top surface must be at reference_top_z.
    # Center Z2 = Top - T2/2.
    center_z2 = reference_top_z - (plate2_thickness / 2.0)
    
    origin2 = numpy.array([0.0, plate_length, center_z2])
    uDir2 = numpy.array([0.0, 0.0, 1.0])
    wDir2 = numpy.array([1.0, 0.0, 0.0])
    
    plate2 = Plate(plate_length, plate_width, plate2_thickness)
    plate2.place(origin2, uDir2, wDir2)
    plate2_model = plate2.create_model()
    
    # Create Cover Plate (Top)
    # Sits ON TOP of the reference top level.
    # Center Z = Reference Top + Cover_Thickness / 2
    platec2_model = None  # Initialize bottom cover plate as None
    
    cover_center_z = reference_top_z + (cover_thickness / 2.0)
    
    origin3 = numpy.array([0.0, plate_length / 2.0, cover_center_z])
    uDir3 = numpy.array([0.0, 0.0, 1.0])
    wDir3 = numpy.array([1.0, 0.0, 0.0])
    
    platec = Plate(cover_plate_length, plate_width, cover_thickness)
    platec.place(origin3, uDir3, wDir3)
    platec_model = platec.create_model()
    
    # Create Bottom Cover Plate (Only if Double-Cover)
    packing_plate1_model = None  # Initialize packing plates as None
    packing_plate2_model = None
    
    if cover_type == "Double-Cover":
        reference_bottom_z = reference_top_z - MAX_THICKNESS
        cover_bottom_center_z = reference_bottom_z - (cover_thickness / 2.0)
        
        origin4 = numpy.array([0.0, plate_length / 2.0, cover_bottom_center_z])
        uDir4 = numpy.array([0.0, 0.0, 1.0])
        wDir4 = numpy.array([1.0, 0.0, 0.0])
        
        platec2 = Plate(cover_plate_length, plate_width, cover_thickness)
        platec2.place(origin4, uDir4, wDir4)
        platec2_model = platec2.create_model()
        
        # --- Create Packing Plates to fill gaps ---
        # A packing plate is needed when a main plate doesn't reach the bottom cover
        # The bottom of main plates should align with bottom cover top (reference_bottom_z)
        # Plate bottom = reference_top_z - plate_thickness
        # Gap = (reference_top_z - plate_thickness) - reference_bottom_z
        #     = reference_top_z - plate_thickness - (reference_top_z - MAX_THICKNESS)
        #     = MAX_THICKNESS - plate_thickness
        
        # Packing plate for Plate 1 side (if plate1 is thinner than MAX_THICKNESS)
        gap1 = MAX_THICKNESS - plate1_thickness
        if gap1 > 0.1:  # Only create if there's a meaningful gap
            # Packing plate sits on top of bottom cover, under Plate 1
            # Top of packing plate = bottom of Plate 1 = reference_top_z - plate1_thickness
            # Bottom of packing plate = top of bottom cover = reference_bottom_z
            packing1_center_z = reference_bottom_z + (gap1 / 2.0)
            
            # Origin for packing plate 1 (same Y as Plate 1 origin)
            origin_pack1 = numpy.array([0.0, 0.0, packing1_center_z])
            uDir_pack1 = numpy.array([0.0, 0.0, 1.0])
            wDir_pack1 = numpy.array([1.0, 0.0, 0.0])
            
            # Packing plate has same length and width as the corresponding main plate
            packing1 = Plate(plate_length, plate_width, gap1)
            packing1.place(origin_pack1, uDir_pack1, wDir_pack1)
            packing_plate1_model = packing1.create_model()
        
        # Packing plate for Plate 2 side (if plate2 is thinner than MAX_THICKNESS)
        gap2 = MAX_THICKNESS - plate2_thickness
        if gap2 > 0.1:  # Only create if there's a meaningful gap
            packing2_center_z = reference_bottom_z + (gap2 / 2.0)
            
            # Origin for packing plate 2 (same Y as Plate 2 origin)
            origin_pack2 = numpy.array([0.0, plate_length, packing2_center_z])
            uDir_pack2 = numpy.array([0.0, 0.0, 1.0])
            wDir_pack2 = numpy.array([1.0, 0.0, 0.0])
            
            packing2 = Plate(plate_length, plate_width, gap2)
            packing2.place(origin_pack2, uDir_pack2, wDir_pack2)
            packing_plate2_model = packing2.create_model()

    # --- Calculate Bolt Positions ---
    # In a butt joint, the SAME bolt pattern should be on BOTH sides of the joint line
    # Place bolts on Plate 1 side, then mirror them on Plate 2 side
    bolt_positions = []
    
    # Joint line is at y = plate_length / 2 (center of cover plate)
    joint_line_y = plate_length / 2.0
    
    # Bolt Head Z Origin = Top of Cover Plate = Reference Top + Cover Thickness
    bolt_z_origin = reference_top_z + cover_thickness
    
    print(f"DEBUG BOLT: bolt_rows={bolt_rows}, bolt_cols={bolt_cols}, joint_line_y={joint_line_y}")
    print(f"DEBUG BOLT: end={end}, pitch={pitch}")
    
    # Calculate bolt positions for Plate 1 side (y < joint_line)
    # These bolts go from the joint towards Plate 1
    plate1_count = 0
    for col in range(bolt_cols):
        for row in range(bolt_rows):
            # Place bolts on Plate 1 side - starting from joint line going towards Plate 1
            bolt_y = joint_line_y - end - (col * pitch)
            bolt_positions.append((
                edge + (row * gauge),
                bolt_y,
                bolt_z_origin
            ))
            plate1_count += 1
    print(f"DEBUG BOLT: Plate 1 side bolts created: {plate1_count}")
    
    # Mirror the same pattern on Plate 2 side (y > joint_line)
    # These bolts go from the joint towards Plate 2
    plate2_count = 0
    for col in range(bolt_cols):
        for row in range(bolt_rows):
            # Place bolts on Plate 2 side - mirror of Plate 1 positions
            bolt_y = joint_line_y + end + (col * pitch)
            bolt_positions.append((
                edge + (row * gauge),
                bolt_y,
                bolt_z_origin
            ))
            plate2_count += 1
    print(f"DEBUG BOLT: Plate 2 side bolts created: {plate2_count}")
    print(f"DEBUG BOLT: Total bolt positions: {len(bolt_positions)}")

    # --- Create and Place Bolts & Nuts ---
    bolts_models = []
    nuts_models = []
    bolt_uDir = numpy.array([1.0, 0.0, 0.0])
    bolt_shaftDir = numpy.array([0.0, 0.0, -1.0])

    # Joint line for nut decision
    joint_line_y = plate_length / 2.0

    for pos in bolt_positions:
        # Bolt
        bolt = Bolt(bolt_head_radius, bolt_head_thickness, bolt_length, bolt_shaft_radius)
        bolt.place(pos, bolt_uDir, bolt_shaftDir)
        bolt_model = bolt.create_model()
        bolts_models.append(bolt_model)

        # Nut
        # Determine Z based on which plate it is under and cover_type.
        # For Single-Cover: nut is at bottom of main plate
        # For Double-Cover: nut is below the bottom cover plate
        
        if cover_type == "Double-Cover":
            # For double cover, nut goes below the bottom cover plate
            # Bottom cover plate bottom = reference_top_z - MAX_THICKNESS - cover_thickness
            nut_z = reference_top_z - MAX_THICKNESS - cover_thickness
        else:
            # For single cover, nut goes below the respective main plate
            if pos[1] <= joint_line_y:
                # Under Plate 1
                nut_z = reference_top_z - plate1_thickness
            else:
                # Under Plate 2
                nut_z = reference_top_z - plate2_thickness

        nut_origin = numpy.array([pos[0], pos[1], nut_z])
        nut_uDir = numpy.array([1.0, 0.0, 0.0])
        nut_wDir = numpy.array([0.0, 0.0, -1.0])

        nut = Nut(nut_radius, nut_thickness, nut_height, nut_inner_radius)
        nut.place(nut_origin, nut_uDir, nut_wDir)
        nut_model = nut.create_model()
        nuts_models.append(nut_model)
    
    # --- Cut Bolt Holes in Plates ---
    # Hole radius slightly larger than bolt shaft for clearance
    hole_radius = (bolt_dia / 2.0) * 0.7 # Exact fit with bolt
    
    # Plate 1: Y from 0 to plate_length (centered at plate_length/2 origin is 0)
    # Plate 1 spans Y from -plate_length/2 to +plate_length/2 (relative to origin1 at y=0)
    plate1_y_min = -plate_width / 2.0
    plate1_y_max = plate_width / 2.0
    plate1_z_bottom = reference_top_z - plate1_thickness
    plate1_z_top = reference_top_z
    
    # Plate 2: origin2 at y=plate_length, spans y from plate_length - plate_width/2 to plate_length + plate_width/2
    plate2_y_min = plate_length - plate_width / 2.0
    plate2_y_max = plate_length + plate_width / 2.0
    plate2_z_bottom = reference_top_z - plate2_thickness
    plate2_z_top = reference_top_z
    
    # Cover plate: origin3 at y=plate_length/2, spans y from 0 to plate_length
    cover_y_min = 0.0
    cover_y_max = plate_length
    cover_z_bottom = reference_top_z
    cover_z_top = reference_top_z + cover_thickness
    
    # Cut holes in each plate at bolt positions that pass through it
    for pos in bolt_positions:
        bolt_x, bolt_y, _ = pos
        
        # Cut hole in Plate 1 (bolts near joint line - y close to plate_length/2)
        # Plate 1 spans from y=0 to y=plate_length (in absolute coords), so need bolts with y < plate_length/2 + tolerance
        if bolt_y <= plate_length / 2.0 + 10.0:  # Add tolerance for bolts near joint
            axis1 = gp_Ax2(gp_Pnt(bolt_x, bolt_y, plate1_z_bottom - 5), gp_Dir(0, 0, 1))
            hole1 = BRepPrimAPI_MakeCylinder(axis1, hole_radius, plate1_thickness + 10).Shape()
            plate1_model = BRepAlgoAPI_Cut(plate1_model, hole1).Shape()
        
        # Cut hole in Plate 2 (bolts near joint line - y close to plate_length/2)
        if bolt_y >= plate_length / 2.0 - 10.0:  # Add tolerance for bolts near joint
            axis2 = gp_Ax2(gp_Pnt(bolt_x, bolt_y, plate2_z_bottom - 5), gp_Dir(0, 0, 1))
            hole2 = BRepPrimAPI_MakeCylinder(axis2, hole_radius, plate2_thickness + 10).Shape()
            plate2_model = BRepAlgoAPI_Cut(plate2_model, hole2).Shape()
        
        # Cut hole in Cover Plate (all bolts go through cover plate)
        axis_cover = gp_Ax2(gp_Pnt(bolt_x, bolt_y, cover_z_bottom - 5), gp_Dir(0, 0, 1))
        hole_cover = BRepPrimAPI_MakeCylinder(axis_cover, hole_radius, cover_thickness + 10).Shape()
        platec_model = BRepAlgoAPI_Cut(platec_model, hole_cover).Shape()
        
        # Cut hole in Bottom Cover Plate (if exists)
        if platec2_model is not None:
            bottom_cover_z_top = reference_top_z - MAX_THICKNESS
            bottom_cover_z_bottom = bottom_cover_z_top - cover_thickness
            axis_bottom = gp_Ax2(gp_Pnt(bolt_x, bolt_y, bottom_cover_z_bottom - 5), gp_Dir(0, 0, 1))
            hole_bottom = BRepPrimAPI_MakeCylinder(axis_bottom, hole_radius, cover_thickness + 10).Shape()
            platec2_model = BRepAlgoAPI_Cut(platec2_model, hole_bottom).Shape()
        
        # Cut holes in Packing Plates (if they exist)
        if packing_plate1_model is not None and bolt_y <= plate_length / 2.0 + 10.0:
            gap1 = MAX_THICKNESS - plate1_thickness
            pack1_z_bottom = reference_top_z - MAX_THICKNESS
            axis_pack1 = gp_Ax2(gp_Pnt(bolt_x, bolt_y, pack1_z_bottom - 5), gp_Dir(0, 0, 1))
            hole_pack1 = BRepPrimAPI_MakeCylinder(axis_pack1, hole_radius, gap1 + 10).Shape()
            packing_plate1_model = BRepAlgoAPI_Cut(packing_plate1_model, hole_pack1).Shape()
        
        if packing_plate2_model is not None and bolt_y >= plate_length / 2.0 - 10.0:
            gap2 = MAX_THICKNESS - plate2_thickness
            pack2_z_bottom = reference_top_z - MAX_THICKNESS
            axis_pack2 = gp_Ax2(gp_Pnt(bolt_x, bolt_y, pack2_z_bottom - 5), gp_Dir(0, 0, 1))
            hole_pack2 = BRepPrimAPI_MakeCylinder(axis_pack2, hole_radius, gap2 + 10).Shape()
            packing_plate2_model = BRepAlgoAPI_Cut(packing_plate2_model, hole_pack2).Shape()
    
    # Use BOPAlgo_Builder for assembly
    builder = BOPAlgo_Builder()
    
    builder.AddArgument(plate1_model)
    builder.AddArgument(plate2_model)
    
    for bolt_model in bolts_models:
        builder.AddArgument(bolt_model)
    
    for nut_model in nuts_models:
        builder.AddArgument(nut_model)
    
    builder.Perform()
    
    assembly = builder.Shape()
    
    return assembly, plate1_model, plate2_model, platec_model, platec2_model, bolts_models, nuts_models, packing_plate1_model, packing_plate2_model


# Main execution
if __name__ == "__main__":
    # Create the bolted butt joint
    # Added these values for debugging the model, since UI is not working
    butt_joint, plate1, plate2, platec, bolts, nuts = create_bolted_butt_joint(
        plate1_thickness=8,
        plate2_thickness=14,
        cover_thickness=5,
        plate_width=200,
        bolt_dia=10,
        bolt_rows=4,
        bolt_cols=6,
        pitch=50,
        gauge=40,
        edge=30,
        end=30,
        number_bolts=24
    )

    redd=Quantity_Color(0.28, 0, 0, Quantity_TOC_RGB)   

    # Display the assembly
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    # Display individual components with different colors for better visualization
    display.DisplayShape(plate1, update=True)
    display.DisplayShape(plate2,material=Graphic3d_NOM_ALUMINIUM, update=True)
    display.DisplayShape(platec, material=Graphic3d_NOM_STEEL, update=True)
    
    # --- Display Bolts and Nuts ---
    for bolt_model in bolts:
        display.DisplayShape(bolt_model, color=redd, update=True)

    for nut_model in nuts:
        display.DisplayShape(nut_model,  color=redd, update=True)
    
    #Highlight the global origin (0,0,0)
    origin_point = BRepPrimAPI_MakeSphere(1).Shape()  # Small sphere to mark origin
    display.DisplayShape(origin_point, color=Quantity_NOC_RED, update=True)
    
    # Alternative: display the full assembly as a single shape
    # display.DisplayShape(lap_joint, update=True)
    display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])
    
    display.DisableAntiAliasing()
    display.FitAll()
    start_display()