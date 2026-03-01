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
    weld_l = plate_width
    weld_h = weld_size
    weld_b = weld_size
    
    # Weld 1: Transverse weld at the "start" of overlap (Plate 2 edge)
    # Use the calculated weld size from design output
    weld1 = FilletWeld(weld_size, weld_size, weld_l)
    # Origin at (0, offset - L/2, T1/2) - Interface level, start of overlap
    # uDir along +Z (Up Plate 2 face)
    # wDir along +X (Extrusion)
    # vDir will be -Y (Along Plate 1 surface)
    origin_w1 = numpy.array([0.0, plate2_offset - plate_length/2, plate1_thickness/2])
    uDir_w1 = numpy.array([0.0, 0.0, 1.0])
    wDir_w1 = numpy.array([1.0, 0.0, 0.0])
    weld1.place(origin_w1, uDir_w1, wDir_w1)
    weld1_model = weld1.create_model()
    
    # Weld 2: Transverse weld at the "end" of overlap (Plate 1 edge)
    # Use the calculated weld size from design output
    weld2 = FilletWeld(weld_size, weld_size, weld_l)
    # Origin at (0, L/2, T1/2) - Interface level, end of overlap
    # uDir along -Z (Down Plate 1 face)
    # wDir along +X (Extrusion)
    # vDir will be +Y (Along Plate 2 bottom)
    origin_w2 = numpy.array([0.0, plate_length/2, plate1_thickness/2])
    uDir_w2 = numpy.array([0.0, 0.0, -1.0]) 
    wDir_w2 = numpy.array([1.0, 0.0, 0.0])
    weld2.place(origin_w2, uDir_w2, wDir_w2)
    weld2_model = weld2.create_model()
    
    weld_models = [weld1_model, weld2_model]
    
    # Fuse the assembly for the main model
    # Note: BRepAlgoAPI_Fuse can fuse two shapes. To fuse multiple, we might need a loop or BOPAlgo_Builder.
    # For visualization, we can just return the list of components.
    # But if 'assembly' is expected to be a single shape, we might need to fuse them.
    # However, common_logic.py often handles individual components.
    # Let's return None for assembly for now, as we are returning individual models.
    
    return None, plate1_model, plate2_model, weld_models
