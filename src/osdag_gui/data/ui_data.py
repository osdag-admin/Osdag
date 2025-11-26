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
                ("Lap Joint Bolted",  ":/vectors/lap_joint_bolted_simple_connec.svg"),
                ("Lap Joint Welded",  ":/vectors/lap_joint_welded_simple_connec.svg"),
                ("Butt Joint Bolted", ":/vectors/butt_joint_bolted_simple_connec.svg"),
                ("Butt Joint Welded", ":/vectors/butt_joint_welded_simple_connec.svg")
            ],
            "Shear Connection":
            [
                ("Fin Plate",":/vectors/shear_fin_plate_connec.svg"),
                ("Cleat Angle", ":/vectors/shear_cleat_angle_connec.svg"),
                ("Header Plate", ":/vectors/end_plate_connec.svg"),
                ("Seated Angle", ":/vectors/seated_angle_connec.svg")
            ],
            "Moment Connection": 
                {   "Beam to Beam Splice":
                    [
                        ("Cover Plate Bolted", ":/vectors/cover_plate_bolted_btb_moment_connec.svg"),
                        ("Cover Plate Welded", ":/vectors/cover_plate_welded_btb_moment_connec.svg"),
                        ("Beam Beam End Plate", ":/vectors/end_plate_btb_moment_connec.svg")
                    ],
                    "Beam to Column": 
                    [
                        ("End Plate", ":/vectors/end_plate_btc_moment_connec.svg")
                    ],
                    "Column to Column": 
                    [
                        ("Column Cover Plate Bolted", ":/vectors/cover_plate_bolted_ctc_moment_connec.svg"),
                        ("Column Cover Plate Welded", ":/vectors/cover_plate_welded_ctc_moment_connec.svg"),
                        ("Column End Plate", ":/vectors/end_plate_ctc_moment_connec.svg")
                    ],
                    "PEB": []
                },
            "Base Plate":
            [
                ("Base Plate Connection", ":/vectors/base_plate_connec.svg")
            ],
            "Truss Connection": []
        },
        "Tension Member": 
        [
            ("Bolted to End Gusset", ":/vectors/bolted_tension_member.svg"),
            ("Welded to End Gusset", ":/vectors/welded_tension_member.svg")
        ],
        "Compression Member": 
        [
            ("Struts in Trusses", ":/vectors/struts_in_trusses_compression_mem.svg"),
            ("Column", ":/vectors/column_design_compression_mem.svg"),
        ],
        "Flexural Member": 
        [
            ("Simply Supported Beam", ":/vectors/ss_beam_flexural_mem.svg"),
            ("Cantilever Beam", ":/vectors/cantilever_beam_flexural_mem.svg"),
            ("Plate Girder", ":/vectors/simple_supported_plate_girder.svg"),
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
        "Home": [":/vectors/home_default.svg", ":/vectors/home_clicked.svg", ":/vectors/home_default.svg"],
        "Connection": [":/images/connection.svg", ":/images/connection_clicked.svg", ":/images/connection_dark.svg"],
        "Tension Member": [":/images/tension_member.svg", ":/images/tension_member_clicked.svg", ":/images/tension_member_dark.svg"],
        "Compression Member": [":/images/compression_member.svg", ":/images/compression_member_clicked.svg", ":/images/compression_member_dark.svg"],
        "Flexural Member": [":/images/flexural_member.svg", ":/images/flexural_member_clicked.svg", ":/images/flexural_member_dark.svg"],
        "Beam Column": [":/images/beam_column.svg", ":/images/beam_column_clicked.svg", ":/images/beam_column_dark.svg"],
        "Truss": [":/images/truss.svg", ":/images/truss_clicked.svg", ":/images/truss_dark.svg"],
        "2D Frame": [":/images/2d_frame.svg", ":/images/2d_frame_clicked.svg", ":/images/2d_frame_dark.svg"],
        "3D Frame": [":/images/3d_frame.svg", ":/images/3d_frame_clicked.svg", ":/images/3d_frame_dark.svg"],
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

