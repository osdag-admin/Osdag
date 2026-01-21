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
                            bolt_rows=5,bolt_cols=7,pitch=20,gauge=20,edge=12,end=13.6,number_bolts=7):

    plate_length = 1.5*plate_width
    
    
    nut_thickness = 3.0
    # Bolt parameters
    bolt_head_radius = bolt_dia/2
    bolt_head_thickness = 3.0
    bolt_length = plate1_thickness + plate2_thickness + cover_thickness + bolt_head_thickness  # Enough to go through both plates
    bolt_shaft_radius = 1.5
    
    # Nut parameters
    nut_radius = bolt_head_radius
    
    nut_height = bolt_head_radius
    nut_inner_radius = bolt_shaft_radius
    
    # Create the first plate
    # Position it at the origin
    origin1 = numpy.array([0.0, 0.0, 0.0]) # Global origin lies at midpoint of plate 1
    uDir1 = numpy.array([0.0, 0.0, 1.0])  # Points along Z axis (height)
    wDir1 = numpy.array([1.0, 0.0, 0.0])  # Points along X axis (length)
    
    plate1 = Plate(plate_length, plate_width, plate1_thickness)
    plate1.place(origin1, uDir1, wDir1)
    plate1_model = plate1.create_model()
    
    # Create the second plate 
    # Position it so that it properly overlaps with the first plate
    # The second plate is elevated by plate1_thickness and offset in Y direction

    origin2 = numpy.array([0.0,plate_length, 0])
    uDir2 = numpy.array([0.0, 0.0, 1.0])
    wDir2 = numpy.array([1.0, 0.0, 0.0])
    
    plate2 = Plate(plate_length, plate_width, plate2_thickness)
    plate2.place(origin2, uDir2, wDir2)
    plate2_model = plate2.create_model()
    
    origin3 = numpy.array([0.0, (plate_width*1.5)/2, max(plate1_thickness, plate2_thickness)]) # Global origin lies at midpoint of plate 1
    uDir3 = numpy.array([0.0, 0.0, 1.0])  # Points along Z axis (height)
    wDir3 = numpy.array([1.0, 0.0, 0.0])  # Points along X axis (length)
    
    platec = Plate(plate_length, plate_width, plate1_thickness)
    platec.place(origin3, uDir3, wDir3)
    platec_model = platec.create_model()
    
    

    # --- Calculate Bolt Positions ---
    bolt_positions = []
    count = 0
    exit_loops = False

    for col in range(bolt_cols):
        for row in range(bolt_rows):
            bolt_positions.append(( 
                edge + (row * gauge),
                end + (col * pitch), 
                (max(plate1_thickness, plate2_thickness))/2 + cover_thickness
            ))
            count += 1

            # Exit after completing current column
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

    for pos in bolt_positions:
        # Bolt
        bolt = Bolt(bolt_head_radius, bolt_head_thickness, bolt_length, bolt_shaft_radius)
        bolt.place(pos, bolt_uDir, bolt_shaftDir)
        bolt_model = bolt.create_model()
        bolts_models.append(bolt_model)

        # Nut
        nut_origin = numpy.array([pos[0], pos[1],-0.5*plate1_thickness])
        nut_uDir = numpy.array([1.0, 0.0, 0.0])
        nut_wDir = numpy.array([0.0, 0.0, -1.0])

        nut = Nut(nut_radius, nut_thickness, nut_height, nut_inner_radius)
        nut.place(nut_origin, nut_uDir, nut_wDir)
        nut_model = nut.create_model()
        nuts_models.append(nut_model)
    
     # Use BOPAlgo_Builder for assembly
    builder = BOPAlgo_Builder()
    
    # Add all parts to the builder
    builder.AddArgument(plate1_model)
    builder.AddArgument(plate2_model)
    
    for bolt_model in bolts_models:
        builder.AddArgument(bolt_model)
    
    for nut_model in nuts_models:
        builder.AddArgument(nut_model)
    
    # Perform the boolean operation
    builder.Perform()
    
    # Get the resulting assembly
    assembly = builder.Shape()
    
    return assembly, plate1_model, plate2_model,platec_model, bolts_models, nuts_models


# Main execution
if __name__ == "__main__":
    # Create the bolted lap joint
    butt_joint, plate1, plate2,platec,bolts,nuts = create_bolted_butt_joint()

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
    
    #display.DisplayShape(nut, color=Quantity_NOC_SADDLEBROWN, update=True)
    # Highlight the global origin (0,0,0)
    origin_point = BRepPrimAPI_MakeSphere(1).Shape()  # Small sphere to mark origin
    display.DisplayShape(origin_point, color=Quantity_NOC_RED, update=True)
    
    # Alternative: display the full assembly as a single shape
    # display.DisplayShape(lap_joint, update=True)
    display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])
    
    display.DisableAntiAliasing()
    display.FitAll()
    start_display()