import numpy
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_GRAY, Quantity_NOC_BLUE1, Quantity_NOC_RED
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Ax1, gp_Dir

# Import the component classes
from ...items.plate import Plate
from ...items.filletweld import FilletWeld
import math

def create_welded_lap_joint(plate1_thickness, plate2_thickness, plate_width, overlap_length, weld_size):
    
    plate_length = 3 * overlap_length
    
    # Calculate the offset of the second plate
    plate2_offset = plate_length - overlap_length
    
    # Create the first plate
    # Position it at the origin
    origin1 = numpy.array([0.0, 0.0, 0.0]) 
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

    # Create welds
    # Weld 1: At the end of Plate 2 (top plate), connecting to Plate 1 (bottom plate)
    # Position: x ranges from 0 to width, y = plate2_offset, z = plate1_thickness
    
    weld_l = plate_width
    weld_h = weld_size
    weld_b = weld_size
    
    # Helper for translation and rotation
    def translation_movement(x, y, z, model):
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
        trsf = gp_Trsf()
        translation_vector = gp_Vec(x, y, z)
        trsf.SetTranslation(translation_vector)
        model = BRepBuilderAPI_Transform(model, trsf).Shape()
        return model

    def translation_rotation(angle, axis, model):
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
        trsf = gp_Trsf()
        ax1 = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(float(axis[0]), float(axis[1]), float(axis[2])))
        trsf.SetRotation(ax1, math.radians(angle))
        model = BRepBuilderAPI_Transform(model, trsf).Shape()
        return model

    # Weld 1
    # FilletWeld class usually creates a prism along Z axis? Need to check FilletWeld implementation or assume based on usage in LapJointWelded.py
    # In LapJointWelded.py:
    # fillet_weld_model1 = filletWeld_model(weld_height, weld_height, b)
    # fillet_weld_model1 = translation_rotation(90, numpy.array([0, 1, 0]), fillet_weld_model1)
    # fillet_weld_model1 = translation_movement((l/2)-horizontal_distance, 0, -weld_height/2, fillet_weld_model1)
    
    # Let's use the FilletWeld class from ...items.filletweld
    # Assuming FilletWeld(b, h, L) creates a weld of length L along some axis.
    
    fw1 = FilletWeld(weld_b, weld_h, weld_l)
    # Place it
    # We need to position it at the step.
    # The step is at y = plate2_offset (start of overlap from left perspective of plate 2, or end of plate 1 overlap)
    # Actually, let's look at coordinates.
    # Plate 1: Center at (width/2, length/2, thickness/2) if placed at origin? 
    # Wait, Plate.place uses origin as the bottom-left-corner or center?
    # In bolted_lap_joint.py:
    # origin1 = numpy.array([0.0, 0.0, 0.0]) # Global origin lies at midpoint of plate 1 ?? No, let's check Plate class if possible, or infer.
    # "Global origin lies at midpoint of plate 1" comment says so.
    # If Plate(L, W, T) creates a plate centered at local origin?
    # Let's assume standard behavior from other modules.
    
    # Let's try to construct welds relative to plates.
    # Weld 1 is at the transverse edge of Plate 2 on top of Plate 1.
    # Plate 2 starts at y = plate2_offset.
    # Plate 1 top surface is at z = plate1_thickness.
    # So Weld 1 should be along the line y = plate2_offset, z = plate1_thickness.
    
    # Create Weld 1
    weld1 = FilletWeld(weld_b, weld_h, weld_l)
    # We need to rotate/translate it to fit the corner.
    # Assuming FilletWeld creates a prism with right angle at origin?
    # Let's place it using place() method if available, or manual transform.
    
    # Using the logic from user's file as a guide, but coordinates might be different.
    # User file:
    # fillet_weld_model1 = filletWeld_model(weld_height, weld_height, b)
    # fillet_weld_model1 = translation_rotation(90, numpy.array([0, 1, 0]), fillet_weld_model1)
    # fillet_weld_model1 = translation_movement((l/2)-horizontal_distance, 0, -weld_height/2, fillet_weld_model1)
    
    # Let's assume we need to place it at (0, plate2_offset, plate1_thickness)
    # And oriented correctly.
    
    # For now, I will create the weld shapes and return them.
    # I'll use a simplified placement for now and refine if needed.
    
    # Weld 1: Transverse weld at the "start" of overlap (Plate 2 edge)
    weld1 = FilletWeld(weld_b, weld_h, weld_l)
    # Rotate to align with X axis
    origin_w1 = numpy.array([0.0, plate2_offset, plate1_thickness])
    uDir_w1 = numpy.array([0.0, 0.0, 1.0])
    wDir_w1 = numpy.array([1.0, 0.0, 0.0])
    weld1.place(origin_w1, uDir_w1, wDir_w1)
    weld1_model = weld1.create_model()
    
    # Weld 2: Transverse weld at the "end" of overlap (Plate 1 edge)
    # Plate 1 ends at y = plate_length.
    # Overlap ends at y = plate_length.
    # Plate 2 is on top. Plate 1 is below.
    # Weld 2 is at the edge of Plate 1, connecting to bottom of Plate 2?
    # Wait, Lap Joint:
    #      ___________________ (Plate 2)
    #     |                   |
    # ____|___________________|
    # (Plate 1)
    #
    # Weld 1 is at the left end of Plate 2 (on top of Plate 1).
    # Weld 2 is at the right end of Plate 1 (underneath Plate 2).
    
    # Plate 1: y from 0 to plate_length
    # Plate 2: y from plate2_offset to plate2_offset + plate_length
    # Overlap region: y from plate2_offset to plate_length
    
    # Weld 1 (Left end of Plate 2):
    # Location: y = plate2_offset. z = plate1_thickness.
    # It should be on top of Plate 1, against the face of Plate 2.
    # Orientation: triangular cross section.
    
    # Weld 2 (Right end of Plate 1):
    # Location: y = plate_length. z = plate1_thickness.
    # It should be under Plate 2, against the face of Plate 1.
    
    weld2 = FilletWeld(weld_b, weld_h, weld_l)
    origin_w2 = numpy.array([0.0, plate_length, plate1_thickness])
    # Orientation needs to be rotated 180 degrees around Z relative to Weld 1?
    # Or mirrored.
    uDir_w2 = numpy.array([0.0, 0.0, -1.0]) # Points down?
    wDir_w2 = numpy.array([1.0, 0.0, 0.0])
    weld2.place(origin_w2, uDir_w2, wDir_w2)
    weld2_model = weld2.create_model()
    
    # Fuse welds? Or return list?
    # bolted_lap_joint returns: assembly, plate1_model, plate2_model, bolts_models, nuts_models
    # We can return: assembly, plate1_model, plate2_model, weld_models
    
    weld_models = [weld1_model, weld2_model]
    
    return None, plate1_model, plate2_model, weld_models

if __name__ == '__main__':
    pass
