"""
Menu data for Osdag GUI.
Provides static data for modules, navigation, and recent projects.
"""
class Data:
    # Empty List means "Under Development"
    MODULES = {
        "Home": [""], # Just to suggest that it is not under development
        "Connection" :
        {
            "Simple Connection":
            [
                ("Lap Joint Bolted",  ":/images/modules/lap_joint_bolted_simple_connec.png"),
                ("Lap Joint Welded",  ":/images/modules/lap_joint_welded_simple_connec.png"),
                ("Butt Joint Bolted", ":/images/modules/butt_joint_bolted_simple_connec.png"),
                ("Butt Joint Welded", ":/images/modules/butt_joint_welded_simple_connec.png")
            ],
            "Shear Connection":
            [
                ("Fin Plate",":/images/modules/shear_fin_plate_connec.png"),
                ("Cleat Angle", ":/images/modules/shear_cleat_angle_connec.png"),
                ("Header Plate", ":/images/modules/header_plate_connec.png"),
                ("Seated Angle", ":/images/modules/seated_angle_connec.png")
            ],
            "Moment Connection": 
                {   "Beam to Beam Splice":
                    [
                        ("Cover Plate Bolted", ":/images/modules/cover_plate_bolted_btb_moment_connec.png"),
                        ("Cover Plate Welded", ":/images/modules/cover_plate_welded_btb_moment_connec.png"),
                        ("Beam Beam End Plate", ":/images/modules/end_plate_btb_moment_connec.png")
                    ],
                    "Beam to Column": 
                    [
                        ("End Plate", ":/images/modules/end_plate_btc_moment_connec.png")
                    ],
                    "Column to Column": 
                    [
                        ("Column Cover Plate Bolted", ":/images/modules/cover_plate_bolted_ctc_moment_connec.png"),
                        ("Column Cover Plate Welded", ":/images/modules/cover_plate_welded_ctc_moment_connec.png"),
                        ("Column End Plate", ":/images/modules/end_plate_ctc_moment_connec.png")
                    ],
                    "PEB": []
                },
            "Base Plate":
            [
                ("Base Plate Connection", ":/images/modules/base_plate_connec.png")
            ],
            "Truss Connection": []
        },
        "Tension Member": 
        [
            ("Bolted to End Gusset", ":/images/modules/bolted_tension_member.png"),
            ("Welded to End Gusset", ":/images/modules/welded_tension_member.png")
        ],
        "Compression Member": 
        [
            ("Struts Bolted to End Gusset", ":/images/modules/struts_bolt_end_gusset.png"),
            ("Struts Welded to End Gusset", ":/images/modules/struts_weld_end_gusset.png"),
            ("Column Design", ":/images/modules/column_design_compression_mem.png"),
        ],
        "Flexural Member": 
        [
            ("Simply Supported Beam", ":/images/modules/ss_beam_flexural_mem.png"),
            ("Cantilever Beam", ":/images/modules/cantilever_beam_flexural_mem.png"),
            ("Plate Girder", ":/images/modules/plate_girder_flexural_mem.png"),
            ("Purlin", ":/images/modules/purlin_flexure_member.png"),
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
            ["About Osdag", "Ask Us a Question", "Check For Update"]
        ),
        (
            ":/vectors/resources_default.svg",
            ":/vectors/resources_hover.svg",
            "Resources",
            ["Video Tutorials", "Osi File", "Design Examples", "Databases (IS:808)", "Custom Database"]
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

