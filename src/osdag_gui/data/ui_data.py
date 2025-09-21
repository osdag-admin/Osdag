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
        "connection": ["connection_button.svg", "connection_button_clicked.svg"],
        "tension_member": ["tension_member_button.svg", "tension_member_button_clicked.svg"],
        "compression_member": ["compression_member_button.svg", "compression_member_button_clicked.svg"],
        "flexural_member": ["flexural_member_button.svg", "flexural_member_button_clicked.svg"],
        "beam_column": ["beam_column_button.svg", "beam_column_button_clicked.svg"],
        "truss": ["truss_button.svg", "truss_button_clicked.svg"],
        "2d_frame": ["2d_frame_button.svg", "2d_frame_button_clicked.svg"],
        "3d_frame": ["3d_frame_button.svg", "3d_frame_button_clicked.svg"],
        "group_design": ["group_design_button.svg", "group_design_button_clicked.svg"],
    }

    FLOATING_NAVBAR = [
        (
            ":/vectors/info_default.svg",
            ":/vectors/info_hover.svg",
            "   Info",
            ["Ask Us a Question", "About Osdag", "Check For Update"]
        ),
        (
            ":/vectors/resources_default.svg",
            ":/vectors/resources_hover.svg",
            "Resources",
            ["Video Tutorials", "Osi File", "Design Examples", "Databases"]
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

