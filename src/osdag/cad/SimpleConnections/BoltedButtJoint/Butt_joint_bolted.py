"""Utilities for creating chamfered butt-joint CAD solids with pythonOCC."""

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_Transform,
)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec


def _build_face(points):
    """Create a planar face from an ordered point loop."""
    wire = BRepBuilderAPI_MakeWire()
    for index in range(len(points)):
        wire.Add(BRepBuilderAPI_MakeEdge(points[index], points[(index + 1) % len(points)]).Edge())
    return BRepBuilderAPI_MakeFace(wire.Wire()).Face()


def create_v_plate(length, width, thickness, chamfer_depth, reverse=False):
    """Create a rectangular base plate (plate1/plate2 stay unchanged rectangles).

    The signature is intentionally preserved for compatibility with existing calls.
    ``chamfer_depth`` and ``reverse`` are ignored by design.
    """
    del chamfer_depth
    del reverse

    half_width = width / 2.0
    xy_profile = [
        (0.0, -half_width),
        (length, -half_width),
        (length, half_width),
        (0.0, half_width),
    ]

    profile_points = [gp_Pnt(x_val, y_val, 0.0) for x_val, y_val in xy_profile]
    profile_face = _build_face(profile_points)

    return BRepPrimAPI_MakePrism(profile_face, gp_Vec(0.0, 0.0, thickness)).Shape()


def create_cover_plate(length, width, thickness, chamfer_depth):
    """Create a cover plate with tapered sides and straight end lands.

    Straight end lands keep the highlighted edge lines straight on both
    top and bottom cover plates.
    """
    half_width = width / 2.0
    chamfer_depth = max(0.0, min(chamfer_depth, length / 2.0))
    land_half_width = min(width * 0.20, half_width)

    if chamfer_depth <= 0.0:
        xy_profile = [
            (0.0, -half_width),
            (length, -half_width),
            (length, half_width),
            (0.0, half_width),
        ]
    elif chamfer_depth >= (length / 2.0):
        # Apex-like short cover with straight lands on both ends.
        mid_x = length / 2.0
        xy_profile = [
            (0.0, -land_half_width),
            (mid_x, -half_width),
            (length, -land_half_width),
            (length, land_half_width),
            (mid_x, half_width),
            (0.0, land_half_width),
        ]
    else:
        xy_profile = [
            (0.0, -land_half_width),
            (chamfer_depth, -half_width),
            (length - chamfer_depth, -half_width),
            (length, -land_half_width),
            (length, land_half_width),
            (length - chamfer_depth, half_width),
            (chamfer_depth, half_width),
            (0.0, land_half_width),
        ]

    profile_points = [gp_Pnt(x_val, y_val, 0.0) for x_val, y_val in xy_profile]
    profile_face = _build_face(profile_points)

    return BRepPrimAPI_MakePrism(profile_face, gp_Vec(0.0, 0.0, thickness)).Shape()


def create_welded_butt_joint(
    plate1_thickness,
    plate2_thickness,
    cover_thickness,
    plate_width,
    weld_size,
    cover_type,
):
    """Create a chamfered butt-joint assembly compatible with Osdag return signature."""
    del weld_size

    plate_length = 300.0
    root_gap = 2.0

    # Professor rule from sketch discussion: use W/2 chamfer in plan view.
    chamfer_depth = min(plate_width / 2.0, plate_length)

    plate1_model = create_v_plate(
        plate_length,
        plate_width,
        plate1_thickness,
        chamfer_depth,
        reverse=False,
    )

    plate2_model = create_v_plate(
        plate_length,
        plate_width,
        plate2_thickness,
        chamfer_depth,
        reverse=True,
    )

    # Put each base plate around the joint mid-plane so both stay between covers.
    plate1_z_shift = gp_Trsf()
    plate1_z_shift.SetTranslation(gp_Vec(0.0, 0.0, -plate1_thickness / 2.0))
    plate1_model = BRepBuilderAPI_Transform(plate1_model, plate1_z_shift, True).Shape()

    plate2_z_shift = gp_Trsf()
    plate2_z_shift.SetTranslation(gp_Vec(0.0, 0.0, -plate2_thickness / 2.0))
    plate2_model = BRepBuilderAPI_Transform(plate2_model, plate2_z_shift, True).Shape()

    # Place second plate to the right with root gap between the two apex points.
    plate2_shift = gp_Trsf()
    plate2_shift.SetTranslation(gp_Vec(plate_length + root_gap, 0.0, 0.0))
    plate2_model = BRepBuilderAPI_Transform(plate2_model, plate2_shift, True).Shape()

    platec_model = None
    platec2_model = None

    if cover_type == "Double-Cover":
        # Keep cover plate length compact (as requested) instead of spanning both base plates.
        cover_length = plate_width
        cover_chamfer_depth = min(plate_width / 2.0, cover_length / 2.0)

        platec_model = create_cover_plate(
            cover_length,
            plate_width,
            cover_thickness,
            cover_chamfer_depth,
        )
        platec2_model = create_cover_plate(
            cover_length,
            plate_width,
            cover_thickness,
            cover_chamfer_depth,
        )

        max_plate_thickness = max(plate1_thickness, plate2_thickness)
        joint_center_x = plate_length + (root_gap / 2.0)
        cover_x_shift = joint_center_x - (cover_length / 2.0)

        # Keep top/bottom covers around the base plates (sandwich layout) and centered at joint.
        top_cover_shift = gp_Trsf()
        top_cover_shift.SetTranslation(gp_Vec(cover_x_shift, 0.0, max_plate_thickness / 2.0))
        platec_model = BRepBuilderAPI_Transform(platec_model, top_cover_shift, True).Shape()

        bottom_cover_shift = gp_Trsf()
        bottom_cover_shift.SetTranslation(
            gp_Vec(cover_x_shift, 0.0, -((max_plate_thickness / 2.0) + cover_thickness))
        )
        platec2_model = BRepBuilderAPI_Transform(platec2_model, bottom_cover_shift, True).Shape()

    assembly = BRepAlgoAPI_Fuse(plate1_model, plate2_model).Shape()

    if platec_model is not None:
        assembly = BRepAlgoAPI_Fuse(assembly, platec_model).Shape()

    if platec2_model is not None:
        assembly = BRepAlgoAPI_Fuse(assembly, platec2_model).Shape()

    welds = []
    packing1 = None
    packing2 = None

    return (
        assembly,
        plate1_model,
        plate2_model,
        platec_model,
        platec2_model,
        welds,
        packing1,
        packing2,
    )