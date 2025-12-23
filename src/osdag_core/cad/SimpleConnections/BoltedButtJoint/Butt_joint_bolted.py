import numpy
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BOPAlgo import BOPAlgo_Builder
from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN,Quantity_NOC_GRAY,Quantity_NOC_BLUE1,Quantity_NOC_RED,Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_STEEL
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
# Import the component classes
from ...items.bolt import Bolt
from ...items.nut import Nut
from ...items.plate import Plate



def create_bolted_butt_joint(plate1_thickness = 4, plate2_thickness = 4,cover_thickness=3, plate_width = 100, bolt_dia = 16,
                            bolt_rows=3,bolt_cols=7,pitch=20,gauge=20,edge=12,end=13.6,number_bolts=7):

    # --- Top Alignment Logic ---
    # We want the TOP surfaces of both plates to be at the same level.
    # Let's define the "Reference Top Level" relative to the global origin Z=0.
    # If the thickest plate is centered at Z=0 (from -MAX/2 to MAX/2), its top is at MAX/2.
    # So, Reference Top = MAX_THICKNESS / 2.0.
    
    MAX_THICKNESS = max(plate1_thickness, plate2_thickness)
    reference_top_z = MAX_THICKNESS / 2.0
    
    plate_length = 1.5*plate_width
    
    nut_thickness = 3.0
    # Bolt parameters
    bolt_head_radius = bolt_dia/2
    bolt_head_thickness = 3.0
    # Bolt length must encompass the thickest path: Max(T) + Cover + Head + Nut
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
    
    # Create Cover Plate
    # Sits ON TOP of the reference top level.
    # Center Z = Reference Top + Cover_Thickness / 2
    cover_center_z = reference_top_z + (cover_thickness / 2.0)
    
    origin3 = numpy.array([0.0, plate_length / 2.0, cover_center_z])
    uDir3 = numpy.array([0.0, 0.0, 1.0])
    wDir3 = numpy.array([1.0, 0.0, 0.0])
    
    platec = Plate(plate_length, plate_width, cover_thickness)
    platec.place(origin3, uDir3, wDir3)
    platec_model = platec.create_model()

    # --- Calculate Bolt Positions ---
    bolt_positions = []
    count = 0
    exit_loops = False
    
    # Bolt Head Z Origin = Top of Cover Plate = Reference Top + Cover Thickness
    bolt_z_origin = reference_top_z + cover_thickness

    for col in range(bolt_cols):
        for row in range(bolt_rows):
            bolt_positions.append(( 
                edge + (row * gauge),
                end + (col * pitch), 
                bolt_z_origin
            ))
            count += 1

            if count == number_bolts and row == bolt_rows - 1:  
                exit_loops = True
                break
        if exit_loops:
            break

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
        # Determine Z based on which plate it is under.
        # We need the bottom surface of the respective plate.
        # Bottom Z1 = Top - T1 = reference_top_z - plate1_thickness
        # Bottom Z2 = Top - T2 = reference_top_z - plate2_thickness
        
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
    
    return assembly, plate1_model, plate2_model,platec_model, bolts_models, nuts_models


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