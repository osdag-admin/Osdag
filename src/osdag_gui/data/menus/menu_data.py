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
        (":/vectors/info_default.svg", ":/vectors/info_hover.svg", "   Info"),
        (":/vectors/resources_default.svg", ":/vectors/resources_hover.svg", "Resources"),
        (":/vectors/plugin_default.svg", ":/vectors/plugin_hover.svg", "Plugins"),
        (":/vectors/load_default.svg", ":/vectors/load_hover.svg", " Import"),
    ]

    Projects = [
        {"project_name": "Cleat Angle", "last_date": "04-06-2025", "sub_module": "ProjectA_R01_MB350-MB400_CleatAngle"},
        {"project_name": "End Plate", "last_date": "03-06-2025", "sub_module": "ProjectB_R01_MB300-MB350_EndPlate"},
        {"project_name": "Fin Plate", "last_date": "02-06-2025", "sub_module": "ProjectC_R01_MB250-MB300_FinPlate"},
        {"project_name": "Welded Connection", "last_date": "01-06-2025", "sub_module": "ProjectD_R01_MB200-MB250_WeldedConnection"},
        {"project_name": "Base Plate", "last_date": "31-05-2025", "sub_module": "ProjectE_R01_MB150-MB200_BasePlate"},
        {"project_name": "Moment Connection", "last_date": "30-05-2025", "sub_module": "ProjectF_R01_MB100-MB150_MomentConnection"},
        {"project_name": "Splice Plate", "last_date": "29-05-2025", "sub_module": "ProjectG_R01_MB50-MB100_SplicePlate"},
        {"project_name": "Bracket", "last_date": "28-05-2025", "sub_module": "ProjectH_R01_MB0-MB50_Bracket"},
        {"project_name": "Gusset Plate", "last_date": "27-05-2025", "sub_module": "ProjectI_R01_MB-50-MB0_GussetPlate"},
        {"project_name": "Stiffener", "last_date": "26-05-2025", "sub_module": "ProjectJ_R01_MB-100-MB-50_Stiffener"},
        {"project_name": "Cleat Angle", "last_date": "25-05-2025", "sub_module": "ProjectK_R01_MB-150-MB-100_CleatAngle"},
        {"project_name": "End Plate", "last_date": "24-05-2025", "sub_module": "ProjectL_R01_MB-200-MB-150_EndPlate"},
        {"project_name": "Fin Plate", "last_date": "23-05-2025", "sub_module": "ProjectM_R01_MB-250-MB-200_FinPlate"},
    ]
    Modules = [
        {"sub_module": "Connections", "date_created": "04-06-2025", "module_name": "Endplate Connection "},
        {"sub_module": "Connections", "date_created": "04-06-2025", "module_name": "Endplate Connection"},
        {"sub_module": "Tension Member", "date_created": "04-06-2025", "module_name": "Bolted Tension Member"},
        {"sub_module": "Beam Design", "date_created": "03-06-2025", "module_name": "Simply Supported Beam"},
        {"sub_module": "Column Design", "date_created": "02-06-2025", "module_name": "Axially Loaded Column"},
        {"sub_module": "Plate Girder", "date_created": "01-06-2025", "module_name": "Welded Plate Girder"},
        {"sub_module": "Base Plate", "date_created": "31-05-2025", "module_name": "Moment Base Plate"},
        {"sub_module": "Truss Design", "date_created": "30-05-2025", "module_name": "2D Truss Analysis"},
        {"sub_module": "Bracing", "date_created": "29-05-2025", "module_name": "Lateral Bracing System"},
        {"sub_module": "Portal Frame", "date_created": "28-05-2025", "module_name": "Single Bay Portal"},
        {"sub_module": "Composite Beam", "date_created": "27-05-2025", "module_name": "Slab Composite Beam"},
    ]

    def recent_projects(self):
        return self.Projects
    
    def recent_modules(self):
        return self.Modules

