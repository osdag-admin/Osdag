"""
Design report generator for the Base Plate Connection Module

@Author:    Danish Ansari - Osdag Team, IIT Bombay

 Module - Base Plate Connection
           - Pinned Base Plate (welded and bolted) [Axial + Shear]
           - Gusseted Base Plate [Moment (major and minor axis) + Axial + Shear]
           - Base Plate for hollow sections [Moment (major and minor axis) + Axial + Shear]


 Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) IS 2062: 2011, Hot rolled medium and high tensile structural steel - specification
               4) IS 5624: 1993, Foundation bolts
               5) IS 456: 2000, Plain and reinforced concrete - code of practice
               6) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               7) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

     other     8)  Column Bases - Omer Blodgett (chapter 3)
  references   9) AISC Design Guide 1 - Base Plate and Anchor Rod Design

  Note: This file refers to the BasePlateConnection class of the base_plate_connection file

"""

# Import modules and classes
from design_type.connection.base_plate_connection import BasePlateConnection
# from design_type.connection.base_plate_connection import *
from Common import *
from Report_functions import *
from design_report.reportGenerator_latex import CreateLatex
self = BasePlateConnection


# Start of the design report
class SaveDesignBP(BasePlateConnection):

    def __init__(self):
        super().__init__()

        self.report_input = {
            KEY_MODULE: self.module,
            KEY_MAIN_MODULE: self.mainmodule,
            KEY_CONN: self.connectivity,
            KEY_DISP_AXIAL: self.load_axial,
            # KEY_DISP_AXIAL: self.load_axial_tension,
            KEY_DISP_MOMENT_MAJOR: self.load_moment_major,
            KEY_DISP_MOMENT_MINOR: self.load_moment_minor,
            KEY_DISP_SHEAR: self.load_shear,
            # "Supporting Section": "TITLE",
            # "Supporting Section Details": self.report_supporting,
            "Supported Section": "TITLE",
            "Supported Section Details": self.report_supported,

            "Bolt Details": "TITLE",
            KEY_DISP_D: str(self.anchor_dia),
            KEY_DISP_GRD: str(self.anchor_grade),
            KEY_DISP_TYP: self.anchor_type,
            KEY_DISP_DP_BOLT_HOLE_TYPE: self.dp_anchor_hole,
            KEY_DISP_DP_ANCHOR_BOLT_FRICTION: self.dp_anchor_friction,
            KEY_DISP_DP_DETAILING_EDGE_TYPE: self.dp_detail_edge_type,
            KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES: self.dp_detail_is_corrosive,

            "Weld Details": "TITLE",
            KEY_DISP_DP_WELD_TYPE: self.weld_type,
            KEY_DISP_DP_WELD_FAB: self.dp_weld_fab,
            KEY_DISP_DP_WELD_MATERIAL_G_O: self.dp_weld_fu_overwrite
        }

        self.report_supported = {
            KEY_DISP_SEC_PROFILE: "ISection",  #Image shall be save with this name.png in resource files
            KEY_DISP_SUPTDSEC: self.dp_column_designation,
            KEY_DISP_MATERIAL: self.dp_column_material,
            KEY_DISP_FU: self.dp_column_fu,
            KEY_DISP_FY: self.dp_column_fy,
            'Mass': self.column_properties.mass,
            'Area(cm2) - A': round(self.column_properties.area, 3),
            'D(mm)': self.column_D,
            'B(mm)': self.column_bf,
            't(mm)': self.column_tw,
            'T(mm)': self.column_tf,
            'FlangeSlope': self.column_properties.flange_slope,
            'R1(mm)': self.column_r1,
            'R2(mm)': self.column_r2,
            'Iz(cm4)': self.column_properties.mom_inertia_z,
            'Iy(cm4)': self.column_properties.mom_inertia_y,
            'rz(cm)': self.column_properties.rad_of_gy_z,
            'ry(cm)': self.column_properties.rad_of_gy_y,
            'Zz(cm3)': self.column_properties.elast_sec_mod_z,
            'Zy(cm3)': self.column_properties.elast_sec_mod_y,
            'Zpz(cm3)': self.column_properties.plast_sec_mod_z,
            'Zpy(cm3)': self.column_properties.elast_sec_mod_y
        }

        self.report_check = []

    def save_design(self, popup_summary):
        """ create design report for the base plate module

        Args:
            self
            popup_summary

        Returns:

        """
        # defining attributes used in the BasePlateCaculation Class
        k_b = min((self.end_distance / (3.0 * self.anchor_hole_dia)), (self.dp_anchor_fu_overwrite / self.dp_column_fu), 1.0)

        # start of checks

        # Check 1: Anchor Bolt Design Checks
        t1 = ('SubSection', 'Anchor Bolt Design Checks','|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_D_PROVIDED, '', self.anchor_dia_provided, 'N/A')
        self.report_check.append(t1)

        t2 = (KEY_OUT_DISP_PC_PROVIDED, '', self.anchor_grade, 'N/A')
        self.report_check.append(t2)

        t3 = (KEY_DISP_DP_ANCHOR_BOLT_LENGTH, '', self.anchor_length_provided, 'N/A')
        self.report_check.append(t3)

        t4 = (KEY_OUT_DISP_BOLT_SHEAR, '', bolt_shear_prov(self.dp_anchor_fu_overwrite, 1, self.anchor_area[1], self.gamma_mb,
                                                           self.shear_capacity_anchor), '')
        self.report_check.append(t4)

        t5 = (KEY_OUT_DISP_BOLT_BEARING, '', bolt_bearing_prov(k_b, self.anchor_dia_provided, [self.plate_thk, self.dp_bp_fu, self.dp_bp_fy],
                                                               self.gamma_mb, self.bearing_capacity_anchor), '')
        self.report_check.append(t5)

        t6 = (KEY_OUT_DISP_BOLT_CAPACITY, '', bolt_capacity_prov(self.shear_capacity_anchor, self.bearing_capacity_anchor, self.anchor_capacity), '')
        self.report_check.append(t6)

        t7 = (KEY_OUT_DISP_ANCHOR_BOLT_COMBINED, '', cl_10_3_6_bearing_bolt_combined_shear_and_tension(self.v_sb, self.v_db, self.t_b, self.t_db,
                                                                                                       self.combined_capacity_anchor), '')
        self.report_check.append(t7)

        # Check 2: Anchor Bolt for Uplift - Design Checks (optional: will be called only when there is uplift load defined by the user)
        t1 = ('SubSection', 'Anchor Bolt for Uplift - Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_D_PROVIDED, '', self.anchor_dia_tension, 'N/A')
        self.report_check.append(t1)

        t2 = (KEY_OUT_DISP_PC_PROVIDED, '', self.anchor_grade_tension, 'N/A')
        self.report_check.append(t2)

        t3 = (KEY_DISP_DP_ANCHOR_BOLT_LENGTH, '', self.anchor_length_provided, 'N/A')
        self.report_check.append(t3)

        t4 = (KEY_OUT_DISP_ANCHOR_BOLT_TENSION, '', cl_10_3_5_bearing_bolt_tension_resistance(self.dp_anchor_fu_overwrite,
                                                                                              self.dp_anchor_fu_overwrite, self.anchor_area[0],
                                                                                              self.anchor_area[1], self.dp_weld_fab), '')
        self.report_check.append(t4)

        # Check 3: Base Plate - Design Checks
        t1 = ('SubSection', 'Base Plate - Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_BASEPLATE_THICKNNESS, '', self.plate_thk, '')
        self.report_check.append(t1)

        t2 = (KEY_OUT_DISP_BASEPLATE_LENGTH, '', self.bp_length_provided, '')
        self.report_check.append(t2)

        t3 = (KEY_OUT_DISP_BASEPLATE_WIDTH, '', self.bp_width_provided, '')
        self.report_check.append(t3)

        # Check 4: Base Plate - Detailing Checks
        t1 = ('SubSection', 'Base Plate - Detailing Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_DETAILING_NO_OF_ANCHOR_BOLT, '', self.anchor_nos_provided + self.anchor_nos_tension, '')
        self.report_check.append(t1)

        t2 = (KEY_OUT_DISP_DETAILING_PITCH_DISTANCE, cl_10_2_2_min_spacing(self.anchor_dia_provided, parameter='pitch'), 'N/A', '')
        self.report_check.append(t2)

        t3 = (KEY_OUT_DISP_DETAILING_PITCH_DISTANCE, cl_10_2_3_1_max_spacing(self.plate_thk, parameter='pitch'), 'N/A', '')
        self.report_check.append(t3)

        t4 = (KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, cl_10_2_2_min_spacing(self.anchor_dia_provided, parameter='gauge'), 'N/A', '')
        self.report_check.append(t4)

        t5 = (KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, cl_10_2_3_1_max_spacing(self.plate_thk, parameter='gauge'), 'N/A', '')
        self.report_check.append(t5)

        bolt_hole = d_0 = IS800_2007.cl_10_2_1_bolt_hole_size(self.anchor_dia_provided, self.dp_anchor_hole)
        t6 = (KEY_OUT_DISP_DETAILING_END_DISTANCE, cl_10_2_4_2_min_edge_end_dist(bolt_hole, self.dp_detail_edge_type,
                                                                                 parameter='end_dist'), self.end_distance, '')
        self.report_check.append(t6)

        # t7 = (KEY_OUT_DISP_DETAILING_END_DISTANCE, cl_10_2_4_3_max_edge_dist_old([self.plate_thk], self.dp_bp_fy, self.dp_detail_is_corrosive,
        #                                                                          parameter='end_dist'), 'N/A', '')

        t_fu_fy = [(self.plate_thk, self.dp_bp_fu,self.dp_bp_fy)]
        t7 = (KEY_OUT_DISP_DETAILING_END_DISTANCE, cl_10_2_4_3_max_edge_end_dist(t_fu_fy, self.dp_detail_is_corrosive,
                                                                                 parameter='end_dist'), 'N/A', '')
        self.report_check.append(t7)

        t8 = (KEY_OUT_DISP_DETAILING_EDGE_DISTANCE, cl_10_2_4_2_min_edge_end_dist(bolt_hole,self.dp_detail_edge_type,
                                                                                  parameter='edge_dist'), self.end_distance, '')
        self.report_check.append(t8)

        # t9 = (KEY_OUT_DISP_DETAILING_EDGE_DISTANCE, cl_10_2_4_3_max_edge_dist_old([self.plate_thk], self.dp_bp_fy, self.dp_detail_is_corrosive,
        #                                                                           parameter='edge_dist'), 'N/A', '')
        t9 = (KEY_OUT_DISP_DETAILING_EDGE_DISTANCE, cl_10_2_4_3_max_edge_end_dist(t_fu_Fy, self.dp_detail_is_corrosive,
                                                                                  parameter='edge_dist'), 'N/A', '')
        self.report_check.append(t9)

        if self.connectivity == 'Welded-Slab Base':
            t10 = (KEY_OUT_DISP_DETAILING_PROJECTION, '', self.projection, 'N/A')
            self.report_check.append(t10)
        else:
            pass

        # Check 5: Stiffener Plate Along Flange - Design Checks
        t1 = ('SubSection', 'Stiffener Plate Along Flange - Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        # Check 6: Stiffener Plate Along Web - Design Checks
        t1 = ('SubSection', 'Stiffener Plate Along Flange - Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        # Check 7: Stiffener Plate Across Web - Design Checks
        t1 = ('SubSection', 'Stiffener Plate Along Flange - Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        # Check 8: Stiffener Plate Inside Flange - Design Checks
        t1 = ('SubSection', 'Stiffener Plate Along Flange - Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        # Check 9: Weld Design
        t1 = ('SubSection', 'Weld Design', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_WELD_SIZE_FLANGE, '', self.weld_size_flange, '')
        self.report_check.append(t1)

        t2 = (KEY_OUT_DISP_WELD_SIZE_WEB, '', self.weld_size_web, '')
        self.report_check.append(t2)

        t3 = (KEY_OUT_DISP_WELD_SIZE_STIFFENER, '', self.weld_size_stiffener, '')
        self.report_check.append(t3)

        t4 = (KEY_OUT_DISP_WELD_SIZE_STIFFENER, '', self.weld_size_vertical_flange, '')
        self.report_check.append(t4)

        t5 = (KEY_OUT_DISP_WELD_SIZE_STIFFENER, '', self.weld_size_vertical_web, '')
        self.report_check.append(t5)

        # End of checks

        display_3D_image = "/ResourceFiles/images/BasePlate.jpeg"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']

        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext, rel_path, display_3D_image)
