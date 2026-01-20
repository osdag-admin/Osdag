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
    
    # Create the first plate (Left Side)
    # Position it at the origin
    # Align along X-axis (Length) and Y-axis (Width)
    # Joint connection at X=0
    
    # Plate 1: from X = -plate_length to 0
    origin1 = numpy.array([-plate_length, -plate_width/2, 0.0]) 
    uDir1 = numpy.array([1.0, 0.0, 0.0])  # Points along X axis (Length)
    wDir1 = numpy.array([0.0, 1.0, 0.0])  # Points along Y axis (Width)
    
    plate1 = Plate(plate_length, plate_width, plate1_thickness)
    plate1.place(origin1, uDir1, wDir1)
    plate1_model = plate1.create_model()
    
    # Create the second plate (Right Side)
    # Plate 2: from X = 0 + gap to plate_length + gap (Assuming 0 gap for now as per previous logic)
    gap = 2 # Small gap for visualization
    origin2 = numpy.array([gap, -plate_width/2, 0.0])
    uDir2 = numpy.array([1.0, 0.0, 0.0])
    wDir2 = numpy.array([0.0, 1.0, 0.0])
    
    plate2 = Plate(plate_length, plate_width, plate2_thickness)
    plate2.place(origin2, uDir2, wDir2)
    plate2_model = plate2.create_model()
    
    # Top Cover Plate
    # Spans across both plates
    # Length = 2 * (end + (cols-1)*pitch + edge_of_cover) 
    # Usually cover plate length is calculated based on bolt layout
    # Let's assume cover plate is centered at X = gap/2
    
    # Calculate required cover plate length based on bolts
    # Bolts outermost position from center = end + (cols-1)*pitch
    # Cover plate needs 'edge' distance beyond that.
    # So half_length = end + (cols-1)*pitch + edge (or end, depending on which is which)
    # Usually: Pitch is spacing between cols. End is dist from plate end to first bolt. Edge is dist from cover end to last bolt.
    # Let's use the parameters passed (assuming they are for the main plate).
    # For cover plate, the 'End' distance of main plate becomes 'Edge' distance? 
    # Let's approximate cover plate length to cover all bolts with some margin.
    
    cover_len_half = end + (bolt_cols-1)*pitch + end # Using 'end' as margin for cover plate too
    cover_length = 2 * cover_len_half + gap
    
    origin3 = numpy.array([-cover_len_half + gap/2, -plate_width/2, max(plate1_thickness, plate2_thickness)]) 
    uDir3 = numpy.array([1.0, 0.0, 0.0])  
    wDir3 = numpy.array([0.0, 1.0, 0.0])  
    
    platec = Plate(cover_length, plate_width, cover_thickness)
    platec.place(origin3, uDir3, wDir3)
    platec_model = platec.create_model()
    
    

    # --- Calculate Bolt Positions ---
    bolt_positions = []
    
    # Calculate Y-coordinates (Rows)
    # Centered on width
    # If 1 row: at 0 (relative to center) -> 0 absolute if width extends -w/2 to w/2
    # If multiple rows: distributed with 'gauge' spacing
    # First row at: - ((rows-1) * gauge) / 2
    
    # Check if edge distance is sufficient
    # total_width_required = (bolt_rows - 1) * gauge + 2 * edge
    
    start_y = -((bolt_rows - 1) * gauge) / 2
    
    # Calculate X-coordinates (Cols)
    # Starts at 'end' distance from the gap
    # Left side: - (end + col * pitch)
    # Right side: gap + end + col * pitch
    
    gap_center = gap / 2.0
    
    bolt_z = max(plate1_thickness, plate2_thickness) + cover_thickness # Head on top of cover plate
    
    # Left Side Bolts
    for c in range(bolt_cols):
        x_pos = - (end + c * pitch)
        for r in range(bolt_rows):
            y_pos = start_y + r * gauge
            bolt_positions.append((x_pos, y_pos, bolt_z))

    # Right Side Bolts
    for c in range(bolt_cols):
        x_pos = gap + (end + c * pitch)
        for r in range(bolt_rows):
            y_pos = start_y + r * gauge
            bolt_positions.append((x_pos, y_pos, bolt_z))

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
        # Nut is at bottom of plates (z = 0 or -plate_thickness?)
        # Base plate is at Z=0 to T.
        # So nut should be at Z=0.
        # Wait, plate1 goes from Z=0 to T1.
        # So nut top face is at Z=0. Nut extends downwards.
        
        nut_origin = numpy.array([pos[0], pos[1], 0.0])
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