"""
Menu data for Osdag GUI.
Provides static data for modules, navigation, and recent projects.
"""
class Data:
    # Empty List means "Under Development"
    MODULES = {
        "Home": [],
        "Connection" : 
        {
            "Shear Connection":
            [
                ("Fin Plate",":/vectors/shear_fin_plate_connec.svg"),
                ("Cleat Angle", ":/vectors/shear_cleat_angle_connec.svg"),
                ("End Plate", ":/vectors/end_plate_connec.svg"),
                ("Seated Angle", ":/vectors/seated_angle_connec.svg")
            ],
            "Moment Connection": 
                {   "Beam to Beam Splice":
                    [
                        ("Cover Plate Bolted", ":/vectors/cover_plate_bolted_btb_moment_connec.svg"),
                        ("Cover Plate Welded", ":/vectors/cover_plate_welded_btb_moment_connec.svg"),
                        ("End Plate", ":/vectors/end_plate_btb_moment_connec.svg")
                    ],
                    "Beam to Column": 
                    [
                        ("End Plate", ":/vectors/end_plate_btc_moment_connec.svg")
                    ],
                    "Column to Column": 
                    [
                        ("Cover Plate Bolted", ":/vectors/cover_plate_bolted_ctc_moment_connec.svg"),
                        ("Cover Plate Welded", ":/vectors/cover_plate_welded_ctc_moment_connec.svg"),
                        ("End Plate", ":/vectors/end_plate_ctc_moment_connec.svg")
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
            ("Struts in Trusses", ":/vectors/struts_in_trusses_compression_mem.svg")
        ],
        "Flexural Member": 
        [
            ("Simply Supported Beam", ":/vectors/ss_beam_flexural_mem.svg"),
            ("Cantilever Beam", ":/vectors/cantilever_beam_flexural_mem.svg"),
            ("Plate Girder", ":/vectors/ss_beam_flexural_mem.svg"),
        ],
        "Beam Column": 
        [],
        "Truss": 
        [],
        "2D Frame": 
        [],
        "3D Frame": 
        [],
        "Group Design": 
        []
    }
    
    NAVBAR_ICONS = {
        "Home": [":/images/home.png", ":/images/home_clicked.png"],
        "Connection": [":/images/connection.png", ":/images/connection_clicked.png"],
        "Tension Member": [":/images/tension_member.png", ":/images/tension_member_clicked.png"],
        "Compression Member": [":/images/compression_member.png", ":/images/compression_member_clicked.png"],
        "Flexural Member": [":/images/flexural_member.png", ":/images/flexural_member_clicked.png"],
        "Beam Column": [":/images/beam_column.png", ":/images/beam_column_clicked.png"],
        "Truss": [":/images/truss.png", ":/images/truss_clicked.png"],
        "2D Frame": [":/images/2d_frame.png", ":/images/2d_frame_clicked.png"],
        "3D Frame": [":/images/3d_frame.png", ":/images/3d_frame_clicked.png"],
        "Group Design": [":/images/group_design.png", ":/images/group_design_clicked.png"],
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

