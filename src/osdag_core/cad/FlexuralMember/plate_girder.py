"""
Plate Girder CAD Module

This module creates a 3D CAD model of a welded plate girder.
Refactored to accept parameters from the Osdag UI.

Author: Refactored for Osdag integration
"""

import math
import numpy
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Ax1, gp_Dir, gp_Ax3
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound

# Import Osdag component classes
from ..items.plate import Plate
from ..items.filletweld import FilletWeld


def fuse_models(models):
    """Combine multiple TopoDS shapes into a compound."""
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)
    for model in models:
        builder.Add(compound, model)
    return compound


def translation_movement(x, y, z, model):
    """Translate a model by the given x, y, z offsets."""
    trsf = gp_Trsf()
    translation_vector = gp_Vec(x, y, z)
    trsf.SetTranslation(translation_vector)
    model = BRepBuilderAPI_Transform(model, trsf).Shape()
    return model


def translation_rotation(angle, axis, model):
    """Rotate a model around the given axis by the specified angle in degrees."""
    trsf = gp_Trsf()
    trsf.SetRotation(axis, math.radians(angle))
    model = BRepBuilderAPI_Transform(model, trsf).Shape()
    return model


def create_plate_model(origin, length, width, thickness):
    """
    Create a plate shape at the given origin.
    
    Args:
        origin: numpy array [x, y, z] for the center of the plate
        length: plate length (along X direction after placement)
        width: plate width (along Y direction after placement)
        thickness: plate thickness (along Z direction after placement)
    
    Returns:
        TopoDS_Shape: The plate shape
    """
    plate_uDir = numpy.array([0., 0., 1.])
    plate_wDir = numpy.array([0., 1., 0.])
    plate = Plate(length, width, thickness)
    plate.place(origin, plate_uDir, plate_wDir)
    plate.compute_params()
    return plate.create_model()


def create_weld_model(thickness, width, position, direction):
    """
    Create a fillet weld model.
    
    Args:
        thickness: weld thickness (size)
        width: weld length
        position: numpy array [x, y, z] for weld origin
        direction: 'x', 'y', or 'z' for weld orientation
    
    Returns:
        TopoDS_Shape: The weld shape
    """
    origin = position
    
    if direction == 'y':
        uDir = numpy.array([0., 0., 1.])
        shaftDir = numpy.array([0., 1., 0.])
    elif direction == 'x':
        uDir = numpy.array([0., 0., 1.])
        shaftDir = numpy.array([1., 0., 0.])
    elif direction == 'z':
        uDir = numpy.array([1., 0., 0.])
        shaftDir = numpy.array([0., 0., 1.])
    else:
        raise ValueError("Direction must be 'x', 'y', or 'z'")

    FWeld = FilletWeld(thickness, thickness, width)
    FWeld.place(origin, uDir, shaftDir)
    FWeld.compute_params()
    prism = FWeld.create_model(0)
    return prism


def create_stiffener_plate(position, width, height, thickness, chamfer_length, direction):
    """
    Create a stiffener plate with chamfered corners.
    
    Args:
        position: numpy array [x, y, z] for the center of the stiffener
        width: horizontal width of the stiffener (b)
        height: vertical height of the stiffener (a) 
        thickness: plate thickness
        chamfer_length: size of the corner chamfers
        direction: 'left' or 'right'
    
    Returns:
        TopoDS_Shape: The stiffener plate shape
    """
    c = chamfer_length
    x, y, z = map(float, position)
    y -= thickness / 2

    # Define 2D profile in local coordinates
    if direction == "right":
        p1 = gp_Pnt(0, 0, (height/2) - c)
        p2 = gp_Pnt(c, 0, height/2)
        p3 = gp_Pnt(width, 0, height/2)
        p4 = gp_Pnt(width, 0, -height/2)
        p5 = gp_Pnt(c, 0, -height/2)
        p6 = gp_Pnt(0, 0, (-height/2) + c)
    elif direction == "left":
        # Clockwise order (Down -> Left -> Up -> Right) to ensure +Y normal
        p1 = gp_Pnt(0, 0, (height/2) - c)    # Top Inner
        p2 = gp_Pnt(0, 0, (-height/2) + c)   # Bot Inner
        p3 = gp_Pnt(-c, 0, -height/2)        # Bot Chamfer Start
        p4 = gp_Pnt(-width, 0, -height/2)    # Bot Outer
        p5 = gp_Pnt(-width, 0, height/2)     # Top Outer
        p6 = gp_Pnt(-c, 0, height/2)         # Top Chamfer Start
    else:
        raise ValueError("Direction must be 'left' or 'right'")

    # Make wire
    wire_maker = BRepBuilderAPI_MakeWire()
    for p_start, p_end in [(p1, p2), (p2, p3), (p3, p4), (p4, p5), (p5, p6), (p6, p1)]:
        wire_maker.Add(BRepBuilderAPI_MakeEdge(p_start, p_end).Edge())
    wire = wire_maker.Wire()

    # Make face and extrude
    face = BRepBuilderAPI_MakeFace(wire).Face()
    extrude_vec = gp_Vec(0, thickness, 0)
    solid = BRepPrimAPI_MakePrism(face, extrude_vec).Shape()

    # Apply placement using transformation
    origin = gp_Pnt(0, 0, 0)
    target_origin = gp_Pnt(x, y, z)
    uDir = gp_Dir(0, 1, 0)
    wDir = gp_Dir(0, 0, 1)
    local_ax3 = gp_Ax3(origin, wDir, uDir)
    global_ax3 = gp_Ax3(target_origin, wDir, uDir)

    trsf = gp_Trsf()
    trsf.SetDisplacement(local_ax3, global_ax3)
    transformed_shape = BRepBuilderAPI_Transform(solid, trsf, True).Shape()
    
    return transformed_shape


def create_vertical_weld(weld_height, length):
    """
    Create a vertical weld between stiffener plate and web.
    
    Args:
        weld_height: height/size of the weld
        length: length of the weld
    
    Returns:
        TopoDS_Shape: The weld shape
    """
    p1 = gp_Pnt(0, 0, 0)
    p2 = gp_Pnt(weld_height, 0, 0)
    p3 = gp_Pnt(0, -weld_height, 0)
    edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
    wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    extrude_vec = gp_Vec(0, 0, length)
    solid = BRepPrimAPI_MakePrism(face, extrude_vec).Shape()
    return solid


def create_fillet_weld_model(b, h, l, y, D, tw, T_is, chamfer_length, position):
    """
    Create fillet weld models for stiffener to flange connection.
    
    Args:
        b, h: weld dimensions
        l: weld length
        y: Y position along girder length
        D: total girder depth
        tw: web thickness
        T_is: stiffener thickness
        chamfer_length: chamfer size
        position: 'left' or 'right'
    
    Returns:
        TopoDS_Shape: Combined weld shape
    """
    origin = numpy.array([0., 0., 0.])
    uDir = numpy.array([0., 0., 1.])
    shaftDir = numpy.array([1., 0., 0.])
    FWeld = FilletWeld(b, h, l)
    FWeld.place(origin, uDir, shaftDir)
    FWeld.compute_params()
    prism = FWeld.create_model(0)
    
    axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0))
    x = 0
    
    if position == "right":
        x = tw // 2 + chamfer_length
    elif position == "left":
        x = (-tw // 2) - l - chamfer_length

    # Front weld - down
    trsf = gp_Trsf()
    trsf.SetRotation(axis, math.radians(0))
    prism_down = BRepBuilderAPI_Transform(prism, trsf).Shape()

    # Front weld - up
    trsf = gp_Trsf()
    trsf.SetRotation(axis, math.radians(90))
    prism_up = BRepBuilderAPI_Transform(prism, trsf).Shape()
    
    # Translation
    prism_up = translation_movement(x, y - T_is // 2, D // 2, prism_up)
    prism_down = translation_movement(x, y - T_is // 2, -(D // 2), prism_down)

    weld_fused_forward = BRepAlgoAPI_Fuse(prism_up, prism_down).Shape()

    # Behind weld - down
    trsf = gp_Trsf()
    trsf.SetRotation(axis, math.radians(270))
    prism_down = BRepBuilderAPI_Transform(prism, trsf).Shape()

    # Behind weld - up
    trsf = gp_Trsf()
    trsf.SetRotation(axis, math.radians(180))
    prism_up = BRepBuilderAPI_Transform(prism, trsf).Shape()
    
    # Translation
    prism_up = translation_movement(x, y + T_is // 2, D // 2, prism_up)
    prism_down = translation_movement(x, y + T_is // 2, -D // 2, prism_down)

    weld_fused_behind = BRepAlgoAPI_Fuse(prism_up, prism_down)
    if weld_fused_behind.IsDone():
        weld_fused_behind = weld_fused_behind.Shape()

    weld_fused = BRepAlgoAPI_Fuse(weld_fused_forward, weld_fused_behind)
    if weld_fused.IsDone():
        weld_fused = weld_fused.Shape()

    return weld_fused


def create_plate_girder(
    D=750,                  # Total depth
    tw=14,                  # Web thickness
    length=15000,           # Length along Y axis
    T_ft=20,                # Top flange thickness
    T_fb=20,                # Bottom flange thickness
    B_ft=400,               # Top flange width
    B_fb=400,               # Bottom flange width
    stiffener_spacing=750,  # Space between each stiffener plate
    T_is=15,                # Stiffener thickness
    chamfer_length=30,      # Triangular chamfer length
    weld_size=15,           # Weld size (b = h)
    include_horizontal_plate=False,  # Whether to include horizontal plate
    horizontal_plate_offset_ratio=0.1,  # Position of horizontal plate as ratio of D from top
    T_hp=15,                # Horizontal plate thickness
    reference_axis_y_ratio=0.5, # Y-position of reference axis (0.5 = mid-depth)
    include_end_stiffeners=False,  # Whether to include end stiffeners
    T_es=15,                # End stiffener thickness
    include_intermediate_stiffeners=True # Whether to include intermediate stiffeners
):
    """
    Create a 3D CAD model of a welded plate girder.
    
    Args:
        D: Total depth of the girder (mm)
        tw: Web thickness (mm)
        length: Length of the girder along Y axis (mm)
        T_ft: Top flange thickness (mm)
        T_fb: Bottom flange thickness (mm)
        B_ft: Top flange width (mm)
        B_fb: Bottom flange width (mm)
        stiffener_spacing: Space between stiffener plates (mm)
        T_is: Intermediate stiffener thickness (mm)
        chamfer_length: Size of stiffener corner chamfers (mm)
        weld_size: Fillet weld size (mm)
        include_horizontal_plate: Whether to include a horizontal plate
        horizontal_plate_offset_ratio: Position of horizontal plate from top as ratio of D
        T_hp: Horizontal plate thickness (mm)
    
    Returns:
        dict: Dictionary containing all component shapes:
            - 'web_plate': Web/center plate shape
            - 'top_flange': Top flange plate shape
            - 'bottom_flange': Bottom flange plate shape
            - 'horizontal_plate': Horizontal plate shape (if included)
            - 'stiffener_plates': Compound of all stiffener plates
            - 'longitudinal_welds': Compound of web-to-flange welds
            - 'stiffener_welds': Compound of all stiffener welds
            - 'model': Complete fused model
    """
    # Calculate derived dimensions
    L_top = length
    L_bottom = length
    L = (min(B_ft, B_fb) - tw) / 2  # Stiffener width
    eff_depth = D - T_ft - T_fb  # Effective depth (web height)
    weld_l = L - chamfer_length  # Weld length
    
    # Create main plates
    web_plate = create_plate_model(
        numpy.array([0., 0., 0.]),
        tw, length, D
    )
    
    top_flange = create_plate_model(
        numpy.array([0., 0., (D + T_ft) / 2]),
        B_ft, L_top, T_ft
    )
    
    bottom_flange = create_plate_model(
        numpy.array([0., 0., -(D + T_fb) / 2]),
        B_fb, L_bottom, T_fb
    )
    
    # Horizontal plate (optional)
    horizontal_plate = None
    horizontal_plate_z = 0
    if include_horizontal_plate:
        horizontal_plate_offset = horizontal_plate_offset_ratio * D
        horizontal_plate_z = (D / 2) - horizontal_plate_offset - (T_hp / 2)
        B_hp = B_ft
        horizontal_plate = create_plate_model(
            numpy.array([0., 0., horizontal_plate_z]),
            B_hp, length, T_hp
        )
    
    # Create I-section by fusing main plates
    ISection_model = BRepAlgoAPI_Fuse(bottom_flange, top_flange).Shape()
    if horizontal_plate is not None:
        ISection_model = BRepAlgoAPI_Fuse(ISection_model, horizontal_plate).Shape()
    
    # Create longitudinal welds (web to flange connections)
    weld_thickness = 0.5 * chamfer_length
    
    # Bottom welds
    right_bottom_weld = create_weld_model(weld_thickness, length, numpy.array([tw // 2, 0., (-D // 2)]), "y")
    left_bottom_weld = create_weld_model(weld_thickness, length, numpy.array([-tw // 2, 0., (-D // 2)]), "y")
    axis = gp_Ax1(gp_Pnt(-tw // 2, 0., (-D // 2)), gp_Dir(0, 1, 0))
    trsf = gp_Trsf()
    trsf.SetRotation(axis, math.radians(-90))
    left_bottom_weld = BRepBuilderAPI_Transform(left_bottom_weld, trsf).Shape()
    
    # Top welds
    right_top_weld = create_weld_model(weld_thickness, length, numpy.array([tw // 2, 0., (D // 2)]), "y")
    axis = gp_Ax1(gp_Pnt(tw // 2, 0., (D // 2)), gp_Dir(0, 1, 0))
    trsf = gp_Trsf()
    trsf.SetRotation(axis, math.radians(90))
    right_top_weld = BRepBuilderAPI_Transform(right_top_weld, trsf).Shape()
    
    left_top_weld = create_weld_model(weld_thickness, length, numpy.array([-tw // 2, 0., (D // 2)]), "y")
    axis = gp_Ax1(gp_Pnt(-tw // 2, 0., (D // 2)), gp_Dir(0, 1, 0))
    trsf = gp_Trsf()
    trsf.SetRotation(axis, math.radians(180))
    left_top_weld = BRepBuilderAPI_Transform(left_top_weld, trsf).Shape()
    
    longitudinal_weld_list = [right_bottom_weld, left_bottom_weld, right_top_weld, left_top_weld]
    
    # Horizontal plate welds (if present)
    if horizontal_plate is not None:
        right_hp_weld = create_weld_model(weld_thickness, length, numpy.array([tw // 2, 0., horizontal_plate_z]), "y")
        axis_hp_r = gp_Ax1(gp_Pnt(tw // 2, 0., horizontal_plate_z), gp_Dir(0, 1, 0))
        trsf_hp = gp_Trsf()
        trsf_hp.SetRotation(axis_hp_r, math.radians(90))
        right_hp_weld = BRepBuilderAPI_Transform(right_hp_weld, trsf_hp).Shape()
        
        left_hp_weld = create_weld_model(weld_thickness, length, numpy.array([-tw // 2, 0., horizontal_plate_z]), "y")
        axis_hp_l = gp_Ax1(gp_Pnt(-tw // 2, 0., horizontal_plate_z), gp_Dir(0, 1, 0))
        trsf_hp_l = gp_Trsf()
        trsf_hp_l.SetRotation(axis_hp_l, math.radians(180))
        left_hp_weld = BRepBuilderAPI_Transform(left_hp_weld, trsf_hp_l).Shape()
        
        longitudinal_weld_list.extend([right_hp_weld, left_hp_weld])
    
    longitudinal_welds = fuse_models(longitudinal_weld_list)
    
    # Create vertical weld template for stiffeners
    vertical_weld_height = 0.5 * chamfer_length
    stiffener_vertical_weld_template = create_vertical_weld(vertical_weld_height, D - (2 * chamfer_length))
    
    # Create stiffener plates and welds
    stiffener_plate_list = []
    stiffener_horizontal_weld_list = []
    right_vertical_weld_list = []
    left_vertical_weld_list = []
    
    if include_intermediate_stiffeners:
        start_y = 0.0
        end_y = length
        
        if include_end_stiffeners:
            end_stiffener_gap = (T_es / 2.0) + weld_size
            # The inner stiffener of the end pair is at gap + 50.0
            start_y = end_stiffener_gap + 50.0
            end_y = length - (end_stiffener_gap + 50.0)

        effective_length = end_y - start_y
        
        if effective_length > 0:
            target_spacing = float(stiffener_spacing)
            if target_spacing <= 0: target_spacing = effective_length 
            
            # Calculate number of panels
            # User Change: If spacing > length, place at half length (2 panels)
            if target_spacing + 700> effective_length:
                num_panels = 2
            else:
                num_panels = max(1, round(effective_length / target_spacing))
                
            actual_spacing = effective_length / num_panels
            
            for i in range(1, num_panels):
                y = start_y + (i * actual_spacing)

                # Right and left stiffener plates
                right_stiffener = create_stiffener_plate(
                    numpy.array([tw / 2, y, 0]), L, D, T_is, chamfer_length, "right"
                )
                left_stiffener = create_stiffener_plate(
                    numpy.array([-tw / 2, y, 0]), L, D, T_is, chamfer_length, "left"
                )
                
                # Horizontal welds (stiffener to flange)
                right_horizontal_weld = create_fillet_weld_model(
                    weld_size, weld_size, weld_l, y, D, tw, T_is, chamfer_length, "right"
                )
                left_horizontal_weld = create_fillet_weld_model(
                    weld_size, weld_size, weld_l, y, D, tw, T_is, chamfer_length, "left"
                )
                
                # Vertical welds (stiffener to web)
                right_vertical_front = translation_movement(
                    tw / 2, y, (-D / 2) + chamfer_length, stiffener_vertical_weld_template
                )
                right_vertical_rear = translation_rotation(
                    90, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffener_vertical_weld_template
                )
                right_vertical_rear = translation_movement(
                    tw / 2, y + (T_is / 2), (-D / 2) + chamfer_length, right_vertical_rear
                )
                
                left_vertical_front = translation_rotation(
                    -90, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffener_vertical_weld_template
                )
                left_vertical_front = translation_movement(
                    -tw / 2, y, (-D / 2) + chamfer_length, left_vertical_front
                )
                left_vertical_rear = translation_rotation(
                    -180, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffener_vertical_weld_template
                )
                left_vertical_rear = translation_movement(
                    (-tw / 2), y + (T_is / 2), (-D / 2) + chamfer_length, left_vertical_rear
                )
                
                stiffener_plate_list.extend([right_stiffener, left_stiffener])
                stiffener_horizontal_weld_list.extend([right_horizontal_weld, left_horizontal_weld])
                right_vertical_weld_list.extend([right_vertical_front, right_vertical_rear])
                left_vertical_weld_list.extend([left_vertical_front, left_vertical_rear])

    # End Stiffeners
    if include_end_stiffeners:
        # Calculate gap to ensure weld stays within girder length
        # Stiffener is at y. Weld extends 'weld_size' from face (y +/- T_es/2).
        # Inner limit: 0. Outer limit: Length.
        # Min y = T_es/2 + weld_size
        end_stiffener_gap = (T_es / 2.0) + weld_size
        
        # Create two pairs at each end: one at min gap, one at gap + 50mm
        end_positions = [
            end_stiffener_gap, 
            end_stiffener_gap + 50.0,
            length - (end_stiffener_gap + 50.0),
            length - end_stiffener_gap
        ]
        
        for y in end_positions:
            # Right and left end stiffener plates
            right_stiffener = create_stiffener_plate(
                numpy.array([tw / 2, y, 0]), L, D, T_es, chamfer_length, "right"
            )
            left_stiffener = create_stiffener_plate(
                numpy.array([-tw / 2, y, 0]), L, D, T_es, chamfer_length, "left"
            )
            
            # Horizontal welds (stiffener to flange)
            right_horizontal_weld = create_fillet_weld_model(
                weld_size, weld_size, weld_l, y, D, tw, T_es, chamfer_length, "right"
            )
            left_horizontal_weld = create_fillet_weld_model(
                weld_size, weld_size, weld_l, y, D, tw, T_es, chamfer_length, "left"
            )
            
            # Vertical welds (ends might need adjustment if thickness T_es != T_is)
            position = y
            # We can reuse stiffener_vertical_weld_template because it depends on weld_height which is chamfer/2, and D.
            # It does NOT depend on stiffener thickness.
            # However, the placement logic DOES depend on thickness for the REAR weld.
            
            # Right Vertical Welds
            right_vertical_front = translation_movement(
                tw / 2, position, (-D / 2) + chamfer_length, stiffener_vertical_weld_template
            )
            right_vertical_rear = translation_rotation(
                90, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffener_vertical_weld_template
            )
            right_vertical_rear = translation_movement(
                tw / 2, position + (T_es / 2), (-D / 2) + chamfer_length, right_vertical_rear
            )
            
            # Left Vertical Welds
            left_vertical_front = translation_rotation(
                -90, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffener_vertical_weld_template
            )
            left_vertical_front = translation_movement(
                -tw / 2, position, (-D / 2) + chamfer_length, left_vertical_front
            )
            left_vertical_rear = translation_rotation(
                -180, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffener_vertical_weld_template
            )
            left_vertical_rear = translation_movement(
                (-tw / 2), position + (T_es / 2), (-D / 2) + chamfer_length, left_vertical_rear
            )
            
            stiffener_plate_list.extend([right_stiffener, left_stiffener])
            stiffener_horizontal_weld_list.extend([right_horizontal_weld, left_horizontal_weld])
            right_vertical_weld_list.extend([right_vertical_front, right_vertical_rear])
            left_vertical_weld_list.extend([left_vertical_front, left_vertical_rear])
    
    # Combine stiffener welds
    all_stiffener_welds = (stiffener_horizontal_weld_list + 
                          right_vertical_weld_list + 
                          left_vertical_weld_list)
    
    stiffener_plates = fuse_models(stiffener_plate_list) if stiffener_plate_list else None
    stiffener_welds = fuse_models(all_stiffener_welds) if all_stiffener_welds else None
    
    # Create complete model
    complete_model = ISection_model
    if stiffener_plates is not None:
        complete_model = BRepAlgoAPI_Fuse(complete_model, stiffener_plates).Shape()
    
    # Return all components
    result = {
        'web_plate': web_plate,
        'top_flange': top_flange,
        'bottom_flange': bottom_flange,
        'horizontal_plate': horizontal_plate,
        'stiffener_plates': stiffener_plates,
        'longitudinal_welds': longitudinal_welds,
        'stiffener_welds': stiffener_welds,
        'model': complete_model,
    }
    
    return result


# Main execution for standalone testing
if __name__ == "__main__":
    from OCC.Display.SimpleGui import init_display
    from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM
    from OCC.Core.Quantity import Quantity_NOC_SADDLEBROWN
    
    print("Generating plate girder model...")
    
    # Create plate girder with default parameters
    components = create_plate_girder(
        D=750,
        tw=14,
        length=15000,
        T_ft=20,
        T_fb=20,
        B_ft=400,
        B_fb=400,
        stiffener_spacing=750,
        T_is=15,
        chamfer_length=30,
        weld_size=15,
        include_horizontal_plate=True,
    )
    
    # Initialize display
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.set_bg_gradient_color([51, 51, 102], [150, 150, 170])
    
    # Display components
    display.DisplayShape(components['model'], update=True)
    display.DisplayShape(components['web_plate'], update=True)
    display.DisplayShape(components['stiffener_plates'], material=Graphic3d_NOM_ALUMINIUM, update=True)
    display.DisplayShape(components['longitudinal_welds'], color=Quantity_NOC_SADDLEBROWN, update=True)
    if components['stiffener_welds'] is not None:
        display.DisplayShape(components['stiffener_welds'], color=Quantity_NOC_SADDLEBROWN, update=True)
    
    print("Model generated successfully!")
    
    display.FitAll()
    start_display()