import numpy
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BOPAlgo import BOPAlgo_Builder
from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN,Quantity_NOC_GRAY,Quantity_NOC_BLUE1,Quantity_NOC_RED
from OCC.Core.Graphic3d import *
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
# Import the component classes
from ...items.bolt import Bolt
from ...items.nut import Nut
from ...items.plate import Plate

def create_bolted_lap_joint(plate1_thickness = 16, plate2_thickness = 8, plate_width = 100, bolt_dia = 16, actual_overlap_length=50,
                            bolt_rows=4,bolt_cols=2,pitch=20,gauge=20,edge=12,end=13.6,number_bolts=7):

    plate_length = 3 * actual_overlap_length
    
    # Calculate the offset of the second plate
    plate2_offset = plate_length - actual_overlap_length
    
    nut_thickness = 3.0
    # Bolt parameters
    bolt_head_radius = bolt_dia/2
    bolt_head_thickness = 3.0
    bolt_length = (plate1_thickness + plate2_thickness) + nut_thickness   # Enough to go through both plates
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

    origin2 = numpy.array([0.0, plate2_offset, 0.5*(plate1_thickness+plate2_thickness)])
    uDir2 = numpy.array([0.0, 0.0, 1.0])
    wDir2 = numpy.array([1.0, 0.0, 0.0])
    
    plate2 = Plate(plate_length, plate_width, plate2_thickness)
    plate2.place(origin2, uDir2, wDir2)
    plate2_model = plate2.create_model()

    bolt_positions=[]

    # Calculate bolt positions 
    count = 0
    exit_loops = False  # Flag to break both loops

    for col in range(bolt_cols):
        for row in range(bolt_rows):
            if count==number_bolts:  
                exit_loops = True
                break  # Break out of the inner loop
            
            bolt_positions.append((edge + (row * gauge), 
                                plate_length / 2 - actual_overlap_length + end + (col * pitch), 
                                (0.5 * plate1_thickness) + plate2_thickness))
            count += 1
        
        if exit_loops:  # Check flag to break outer loop
            break

        
    
    # Create bolts and nuts at the calculated positions
    bolts_models = []
    nuts_models = []
    
    bolt_uDir = numpy.array([1.0, 0.0, 0.0])
    bolt_shaftDir = numpy.array([0.0, 0.0, -1.0])  # Points downward through both plates
    for pos in bolt_positions:
        # Start bolts from the top of second plate
        bolt = Bolt(bolt_head_radius, bolt_head_thickness, bolt_length, bolt_shaft_radius)
        bolt.place(pos, bolt_uDir, bolt_shaftDir)
        bolt_model = bolt.create_model()
        bolts_models.append(bolt_model)
        
        # Position nuts at the bottom of the first plate
        nut_origin = numpy.array([pos[0], pos[1], -0.5*plate1_thickness])
        nut_uDir = numpy.array([1.0, 0.0, 0.0])
        nut_wDir = numpy.array([0.0, 0.0, -1.0])  # Points downward
        
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
    
    return assembly, plate1_model, plate2_model, bolts_models, nuts_models

# Main execution
if __name__ == "__main__":
    # Create the bolted lap joint
    lap_joint, plate1, plate2, bolts, nuts = create_bolted_lap_joint()
    
    # Display the assembly
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    # Display individual components with different colors for better visualization
    display.DisplayShape(plate1, material=Graphic3d_NOM_ALUMINIUM, update=True)
    display.DisplayShape(plate2, update=True)
    
    for bolt in bolts:
        display.DisplayShape(bolt, color=Quantity_NOC_SADDLEBROWN, update=True)
    
    for nut in nuts:
        display.DisplayShape(nut, color=Quantity_NOC_SADDLEBROWN, update=True)
    # Highlight the global origin (0,0,0)
    origin_point = BRepPrimAPI_MakeSphere(1).Shape()  # Small sphere to mark origin
    display.DisplayShape(origin_point, color=Quantity_NOC_RED, update=True)
    
    # Alternative: display the full assembly as a single shape
    # display.DisplayShape(lap_joint, update=True)
    display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])
    
    display.DisableAntiAliasing()
    display.FitAll()
    start_display()


# bolt_positions = [
# # Format: (x, y, z)
# # Left side, bottom and top corners of overlap
# (edge, plate_length/2 - actual_overlap_length + end, (0.5*plate1_thickness)+plate2_thickness),
# (edge + gauge, plate_length/2 - actual_overlap_length + end, (0.5*plate1_thickness)+plate2_thickness),
# (edge, plate_length/2 - end, (0.5*plate1_thickness)+plate2_thickness),

# # Right side, bottom and top corners of overlap
# (plate_width - edge, plate_length/2 - actual_overlap_length + end, (0.5*plate1_thickness)+plate2_thickness),
# (plate_width - edge, plate_length/2 - end, (0.5*plate1_thickness)+plate2_thickness)
# ]
    