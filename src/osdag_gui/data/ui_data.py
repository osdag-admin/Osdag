"""
Menu data for Osdag GUI.
Provides static data for modules, navigation, and recent projects.
"""
from osdag_core.Common import (KEY_DISP_FINPLATE, KEY_DISP_ENDPLATE, KEY_DISP_CLEATANGLE, KEY_DISP_SEATED_ANGLE, KEY_DISP_BEAMCOVERPLATE,
                               KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_BB_EP_SPLICE, KEY_DISP_COLUMNCOVERPLATE, KEY_DISP_COLUMNCOVERPLATEWELD,
                               KEY_DISP_COLUMNENDPLATE, KEY_DISP_BCENDPLATE, KEY_DISP_LAPJOINTBOLTED, KEY_DISP_LAPJOINTWELDED, KEY_DISP_BUTTJOINTBOLTED,
                               KEY_DISP_BUTTJOINTWELDED, KEY_DISP_BASE_PLATE, KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED, KEY_DISP_STRUT_WELDED_END_GUSSET,
                               KEY_DISP_STRUT_BOLTED_END_GUSSET, KEY_DISP_COMPRESSION_COLUMN, KEY_DISP_FLEXURE, KEY_DISP_FLEXURE2, KEY_DISP_FLEXURE4, KEY_DISP_PLATE_GIRDER_WELDED)

class Data:
    # Empty List means "Under Development"
    MODULES = {
        "Home": [""], # Just to suggest that it is not under development
        "Connection" :
        {
            "Plated Connection":
            [
                (KEY_DISP_LAPJOINTBOLTED, "Lap Joint — Bolted",  ":/images/modules/lap_joint_bolted_simple_connec.png"),
                (KEY_DISP_LAPJOINTWELDED, "Lap Joint — Welded",  ":/images/modules/lap_joint_welded_simple_connec.png"),
                (KEY_DISP_BUTTJOINTBOLTED, "Butt Joint — Bolted", ":/images/modules/butt_joint_bolted_simple_connec.png"),
                (KEY_DISP_BUTTJOINTWELDED, "Butt Joint — Welded", ":/images/modules/butt_joint_welded_simple_connec.png")
            ],
            "Shear Connection":
            [
                (KEY_DISP_FINPLATE, "Fin Plate",":/images/modules/shear_fin_plate_connec.png"),
                (KEY_DISP_CLEATANGLE, "Cleat Angle", ":/images/modules/shear_cleat_angle_connec.png"),
                (KEY_DISP_ENDPLATE, "Header Plate", ":/images/modules/header_plate_connec.png"),
                (KEY_DISP_SEATED_ANGLE, "Seated Angle", ":/images/modules/seated_angle_connec.png")
            ],
            "Moment Connection": 
                {   
                    "Column Splices": 
                    [
                        (KEY_DISP_COLUMNCOVERPLATE, "Cover Plate — Bolted", ":/images/modules/cover_plate_bolted_ctc_moment_connec.png"),
                        (KEY_DISP_COLUMNCOVERPLATEWELD, "Cover Plate — Welded", ":/images/modules/cover_plate_welded_ctc_moment_connec.png"),
                        (KEY_DISP_COLUMNENDPLATE, "End Plate", ":/images/modules/end_plate_ctc_moment_connec.png")
                    ],
                    "Beam Splices":
                    [
                        (KEY_DISP_BEAMCOVERPLATE, "Cover Plate — Bolted", ":/images/modules/cover_plate_bolted_btb_moment_connec.png"),
                        (KEY_DISP_BEAMCOVERPLATEWELD, "Cover Plate — Welded", ":/images/modules/cover_plate_welded_btb_moment_connec.png"),
                        (KEY_DISP_BB_EP_SPLICE, "End Plate", ":/images/modules/end_plate_btb_moment_connec.png")
                    ],
                    "Beam to Column": 
                    [
                        (KEY_DISP_BCENDPLATE, "End Plate", ":/images/modules/end_plate_btc_moment_connec.png")
                    ],
                    "Beam Splices":
                    [
                        (KEY_DISP_BEAMCOVERPLATE, "Cover Plate — Bolted", ":/images/modules/cover_plate_bolted_btb_moment_connec.png"),
                        (KEY_DISP_BEAMCOVERPLATEWELD, "Cover Plate — Welded", ":/images/modules/cover_plate_welded_btb_moment_connec.png"),
                        (KEY_DISP_BB_EP_SPLICE, "End Plate", ":/images/modules/end_plate_btb_moment_connec.png")
                    ],
                    "PEB": [""]
                },
            "Base Plate":
            [
                (KEY_DISP_BASE_PLATE, "Slab and Gusseted Bases", ":/images/modules/base_plate_connec.png")
            ],
            "Truss Connection": [""]
        },
        "Tension Member": 
        [
            (KEY_DISP_TENSION_BOLTED, "Bolted to End Gusset", ":/images/modules/bolted_tension_member.png"),
            (KEY_DISP_TENSION_WELDED, "Welded to End Gusset", ":/images/modules/welded_tension_member.png")
        ],
        "Compression Member": 
        [
            (KEY_DISP_STRUT_BOLTED_END_GUSSET, "Struts Bolted to End Gusset", ":/images/modules/struts_bolt_end_gusset.png"),
            (KEY_DISP_STRUT_WELDED_END_GUSSET, "Struts Welded to End Gusset", ":/images/modules/struts_weld_end_gusset.png"),
            (KEY_DISP_COMPRESSION_COLUMN, "Axially Loaded Column", ":/images/modules/column_design_compression_mem.png"),
        ],
        "Flexural Member": 
        [
            (KEY_DISP_FLEXURE, "Simply Supported Beam", ":/images/modules/ss_beam_flexural_mem.png"),
            (KEY_DISP_FLEXURE2, "Cantilever Beam", ":/images/modules/cantilever_beam_flexural_mem.png"),
            (KEY_DISP_PLATE_GIRDER_WELDED, "Plate Girder", ":/images/modules/plate_girder_flexural_mem.png"),
            # (KEY_DISP_FLEXURE4, "Purlin", ":/images/modules/purlin_flexure_member.png"),
        ],
        "Beam Column": 
        [],
        "Truss": 
        [],
        "2D Frame": 
        [],
        "3D Frame": 
        []
    }
    
    NAVBAR_ICONS = {
        "Home": [":/vectors/nav_icons/home_default.svg", ":/vectors/nav_icons/home_clicked.svg"],
        "Connection": [":/vectors/nav_icons/connection.svg", ":/vectors/nav_icons/connection_dark.svg"],
        "Tension Member": [":/vectors/nav_icons/tension_member.svg", ":/vectors/nav_icons/tension_member_dark.svg"],
        "Compression Member": [":/vectors/nav_icons/compression_member.svg", ":/vectors/nav_icons/compression_member_dark.svg"],
        "Flexural Member": [":/vectors/nav_icons/flexural_member.svg", ":/vectors/nav_icons/flexural_member_dark.svg"],
        "Beam Column": [":/vectors/nav_icons/beam_column.svg", ":/vectors/nav_icons/beam_column_dark.svg"],
        "Truss": [":/vectors/nav_icons/truss.svg", ":/vectors/nav_icons/truss_dark.svg"],
        "2D Frame": [":/vectors/nav_icons/2d_frame.svg", ":/vectors/nav_icons/2d_frame_dark.svg"],
        "3D Frame": [":/vectors/nav_icons/3d_frame.svg", ":/vectors/nav_icons/3d_frame_dark.svg"],
        # "Group Design": [":/vectors/nav_icons/group_design.svg", ":/vectors/nav_icons/group_design_dark.svg"],
    }

    FLOATING_NAVBAR = [
        (
            ":/vectors/info_default.svg",
            ":/vectors/info_hover.svg",
            "   Info",
            ["About Osdag", "Ask us a question", "Check for Update"]
        ),
        (
            ":/vectors/resources_default.svg",
            ":/vectors/resources_hover.svg",
            "Resources",
            ["Design Examples", "Databases (IS 808:2021)", "Databases (IS 4923:2017)", "Databases (IS 1161:2014)", "Custom Database"]
        ),
        (
            ":/vectors/plugin_default.svg",
            ":/vectors/plugin_hover.svg",
            "Plugins",
            None
        ),
        (
            ":/vectors/load_default.svg",
            ":/vectors/load_hover.svg", 
            " Import",
            None
        ),
    ]

