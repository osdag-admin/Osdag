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
            ("Simply Supported Beam", ":/vectors/ss_beam_flexural_mem.svg"),
            ("Cantilever Beam", ":/vectors/cantilever_beam_flexural_mem.svg"),
            ("Simply Supported Beam", ":/vectors/ss_beam_flexural_mem.svg"),
            ("Cantilever Beam", ":/vectors/cantilever_beam_flexural_mem.svg")
        ],
        "Beam Column": 
        [],
        "Plate Girder": 
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
        "plate_girder": ["plate_girder_button.svg", "plate_girder_button_clicked.svg"],
        "truss": ["truss_button.svg", "truss_button_clicked.svg"],
        "2d_frame": ["2d_frame_button.svg", "2d_frame_button_clicked.svg"],
        "3d_frame": ["3d_frame_button.svg", "3d_frame_button_clicked.svg"],
        "group_design": ["group_design_button.svg", "group_design_button_clicked.svg"],
    }

    FLOATING_NAVBAR = [
        (":/vectors/info_default.svg", ":/vectors/info_hover.svg", "   Help"),
        (":/vectors/resources_default.svg", ":/vectors/resources_hover.svg", "Resources"),
        (":/vectors/plugin_default.svg", ":/vectors/plugin_hover.svg", "Plugin"),
        (":/vectors/load_default.svg", ":/vectors/load_hover.svg", "   Load"),
    ]

    Projects = [
        {"sub_module": "Cleat Angle", "last_date": "04-06-2025", "project_name": "ProjectA_R01_MB350-MB400_CleatAngle"},
        {"sub_module": "End Plate", "last_date": "03-06-2025", "project_name": "ProjectB_R01_MB300-MB350_EndPlate"},
        {"sub_module": "Fin Plate", "last_date": "02-06-2025", "project_name": "ProjectC_R01_MB250-MB300_FinPlate"},
        {"sub_module": "Welded Connection", "last_date": "01-06-2025", "project_name": "ProjectD_R01_MB200-MB250_WeldedConnection"},
        {"sub_module": "Base Plate", "last_date": "31-05-2025", "project_name": "ProjectE_R01_MB150-MB200_BasePlate"},
        {"sub_module": "Moment Connection", "last_date": "30-05-2025", "project_name": "ProjectF_R01_MB100-MB150_MomentConnection"},
        {"sub_module": "Splice Plate", "last_date": "29-05-2025", "project_name": "ProjectG_R01_MB50-MB100_SplicePlate"},
        {"sub_module": "Bracket", "last_date": "28-05-2025", "project_name": "ProjectH_R01_MB0-MB50_Bracket"},
        {"sub_module": "Gusset Plate", "last_date": "27-05-2025", "project_name": "ProjectI_R01_MB-50-MB0_GussetPlate"},
        {"sub_module": "Stiffener", "last_date": "26-05-2025", "project_name": "ProjectJ_R01_MB-100-MB-50_Stiffener"},
        {"sub_module": "Cleat Angle", "last_date": "25-05-2025", "project_name": "ProjectK_R01_MB-150-MB-100_CleatAngle"},
        {"sub_module": "End Plate", "last_date": "24-05-2025", "project_name": "ProjectL_R01_MB-200-MB-150_EndPlate"},
        {"sub_module": "Fin Plate", "last_date": "23-05-2025", "project_name": "ProjectM_R01_MB-250-MB-200_FinPlate"},
    ]
    Modules = [
        {"module_name": "Connections", "date_created": "04-06-2025", "sub_module": "Shear Connection - Endplate"},
        {"module_name": "Connections", "date_created": "04-06-2025", "sub_module": "Shear Connection - Endplate"},
        {"module_name": "Tension Member", "date_created": "04-06-2025", "sub_module": "Bolted Tension Member"},
        {"module_name": "Beam Design", "date_created": "03-06-2025", "sub_module": "Simply Supported Beam"},
        {"module_name": "Column Design", "date_created": "02-06-2025", "sub_module": "Axially Loaded Column"},
        {"module_name": "Plate Girder", "date_created": "01-06-2025", "sub_module": "Welded Plate Girder"},
        {"module_name": "Base Plate", "date_created": "31-05-2025", "sub_module": "Moment Base Plate"},
        {"module_name": "Truss Design", "date_created": "30-05-2025", "sub_module": "2D Truss Analysis"},
        {"module_name": "Bracing", "date_created": "29-05-2025", "sub_module": "Lateral Bracing System"},
        {"module_name": "Portal Frame", "date_created": "28-05-2025", "sub_module": "Single Bay Portal"},
        {"module_name": "Composite Beam", "date_created": "27-05-2025", "sub_module": "Slab Composite Beam"},
    ]

    def recent_projects(self):
        return self.Projects
    
    def recent_modules(self):
        return self.Modules

