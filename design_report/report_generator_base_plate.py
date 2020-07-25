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
            KEY_DISP_SEC_PROFILE: "ISection",  # Image shall be save with this name.png in resource files
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
        # defining attributes used in the BasePlateCalculation Class
        k_b = min((self.end_distance / (3.0 * self.anchor_hole_dia)), (self.dp_anchor_fu_overwrite / self.dp_column_fu), 1.0)

        # start of checks

        # Check 1: Design Parameters
        t1 = ('SubSection', 'Design Parameters', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t7 = ('Bearing Strength of Concrete (N/mm^2)', '', bearing_strength_concrete((self.bearing_strength_concrete / 0.45),
                                                                                     self.bearing_strength_concrete), 'N/A')
        self.report_check.append(t7)

        t2 = ('Grout Thickness (mm)', '', 't_g = ' + self.grout_thk + '', 'N/A')
        self.report_check.append(t2)

        t3 = ('Plate Washer Size (mm)', '', square_washer_size(self.plate_washer_dim), 'N/A')
        self.report_check.append(t3)

        t4 = ('Plate Washer Thickness (mm)', '', square_washer_thk(self.plate_washer_thk), 'N/A')
        self.report_check.append(t4)

        t5 = ('Plate Washer Hole Diameter (mm)', '', square_washer_in_dia(self.plate_washer_inner_dia), 'N/A')
        self.report_check.append(t5)

        t6 = ('Nut (Hexagon) Thickness (mm)', '', hexagon_nut_thickness(self.nut_thk), 'N/A')
        self.report_check.append(t6)

        if self.connectivity == 'Moment Base Plate':
            t8 = ('Modular Ratio', '', modular_ratio(2 * 10 ** 5, (self.bearing_strength_concrete / 0.45), self.n), 'N/A')
            self.report_check.append(t8)

        t9 = ('Epsilon - Stiffener Plate', '', epsilon(self.stiffener_fy, self.epsilon), 'N/A')
        self.report_check.append(t9)

        # Check 2-1: Anchor Bolt Details - Outside Column Flange
        t1 = ('SubSection', 'Anchor Bolt Details - Outside Column Flange', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t2 = ('Diameter (mm)', '', self.anchor_dia_outside_flange, 'N/A')
        self.report_check.append(t2)

        t3 = ('Property Class', '', self.anchor_grade, 'N/A')
        self.report_check.append(t3)

        # Check 2-2: Anchor Bolt Details - Inside Column Flange
        t1 = ('SubSection', 'Anchor Bolt Details - Inside Column Flange', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        if self.load_axial_tension > 0:

            t2 = ('Diameter (mm)', '', self.anchor_dia_inside_flange, 'N/A')
            self.report_check.append(t2)

            t3 = ('Property Class', '', self.anchor_grade_inside_flange, 'N/A')
            self.report_check.append(t3)
        else:
            t2 = ('Diameter (mm)', 'Factored Uplift Force = 0 kN', 'N/A', 'N/A')
            self.report_check.append(t2)

            t3 = ('Property Class', 'N/A', 'N/A', 'N/A')
            self.report_check.append(t3)

        # Check 3: Detailing Checks
        t1 = ('SubSection', 'Detailing Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t2 = ('Min. End Distance (mm)', cl_10_2_4_2_min_edge_end_dist(self.anchor_hole_dia, edge_type=self.dp_detail_edge_type, parameter='end_dist'),
                                                                                self.end_distance, '')
        self.report_check.append(t2)

        t3 = ('Max. End Distance (mm)', cl_10_2_4_3_max_edge_end_dist([self.plate_thk, self.dp_bp_fu, self.dp_bp_fy], corrosive_influences=True,
                                                                      parameter='end_dist'), self.end_distance, '')
        self.report_check.append(t3)

        t4 = ('Min. Edge Distance (mm)', cl_10_2_4_2_min_edge_end_dist(self.anchor_hole_dia, edge_type=self.dp_detail_edge_type, parameter='edge_dist'),
                                                                                                self.end_distance, '')
        self.report_check.append(t4)

        t5 = ('Max. Edge Distance (mm)', cl_10_2_4_3_max_edge_end_dist([self.plate_thk, self.dp_bp_fu, self.dp_bp_fy], corrosive_influences=True,
                                                                       parameter='edge_dist'), self.end_distance, '')
        self.report_check.append(t5)

        if (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):

            t6 = ('Min. Pitch Distance (mm)', cl_10_2_2_min_spacing(self.anchor_dia_outside_flange, parameter='pitch'), self.pitch_distance, '')
            self.report_check.append(t6)

            t7 = ('Max. Pitch Distance (mm)', cl_10_2_3_1_max_spacing([self.plate_thk], parameter=None), self.pitch_distance, '')
            self.report_check.append(t7)
        else:
            t8 = ('Min. Pitch Distance (mm)', 'N/A', self.pitch_distance, 'N/A')
            self.report_check.append(t8)

            t9 = ('Max. Pitch Distance (mm)', 'N/A', self.pitch_distance, 'N/A')
            self.report_check.append(t9)

        if self.connectivity == 'Moment Base Plate':

            if self.anchors_inside_flange == 8:
                t10 = ('Min. Gauge Distance (mm) - for bolts inside column flange', cl_10_2_2_min_spacing(self.anchor_dia_inside_flange,
                                                                                                          parameter='gauge'), self.gauge_distance, '')
                self.report_check.append(t10)

                t11 = ('Max. Gauge Distance (mm) - for bolts inside column flange', cl_10_2_3_1_max_spacing([self.plate_thk], parameter=None),
                       self.gauge_distance, '')
                self.report_check.append(t11)

        # Check 4-1: Base Plate Dimensions (only for Moment Base Plate)
        if self.connectivity == 'Moment Base Plate':

            t1 = ('SubSection', 'Base Plate Dimensions', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t2 = ('Length (mm)', bp_length(self.column_D, self.end_distance, self.bp_length_min), self.bp_length_provided, '')
            self.report_check.append(t2)

            t3 = ('Width (mm)', bp_width(self.column_bf, self.edge_distance, self.bp_width_min), self.bp_width_provided, '')
            self.report_check.append(t3)

        # Check 5: Base Plate Analyses
        t1 = ('SubSection', 'Base Plate Analyses', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):

            t2 = ('Min. Area Required (mm^2)', min_area_req(self.load_axial_compression, self.bearing_strength_concrete, self.min_area_req),
                                                                                                                    self.bp_area_provided, '')
            self.report_check.append(t2)

            t3 = ('Effective Bearing Area (mm^2)', eff_bearing_area(self.column_D, self.column_bf, self.column_tf, self.column_tw), '', 'N/A')
            self.report_check.append(t3)

            t4 = ('Projection (mm)', eff_projection(self.column_D, self.column_bf, self.column_tf, self.column_tw, self.min_area_req,
                                                    self.projection, self.end_distance), self.projection, '')
            self.report_check.append(t4)

        elif self.connectivity == 'Moment Base Plate':

            t1 = ('Eccentricity - about major axis (mm)', '', eccentricity(self.load_moment_major, self.load_axial_compression, self.eccentricity_zz), 'N/A')
            self.report_check.append(t1)

            if self.moment_bp_case == 'Case1':
                t2 = ('Base Plate Type', mom_bp_case(self.moment_bp_case, self.eccentricity_zz, self.bp_length_min),
                      'Case 1: The base plate is purely under compression/bearing with no tension force acting on the anchor bolts - '
                      'outside column flange', 'N/A')
                self.report_check.append(t2)
            elif self.moment_bp_case == 'Case2':
                t2 = ('Base Plate Type', mom_bp_case(self.moment_bp_case, self.eccentricity_zz, self.bp_length_min),
                      'Case 2: The base plate is mostly under compression/bearing with a small tension force acting on the anchor bolts - '
                      'outside column flange', 'N/A')
                self.report_check.append(t2)
            elif self.moment_bp_case == 'Case3':
                t2 = ('Base Plate Type', mom_bp_case(self.moment_bp_case, self.eccentricity_zz, self.bp_length_min),
                      'Case 3: A smaller part of the base plate is under compression/bearing with a large tension force acting on the anchor bolts - '
                      'outside column flange', 'N/A')
                self.report_check.append(t2)

            if self.moment_bp_case == 'Case1':

                t10 = ('Total Tension Demand (kN)', 'P_t = 0 ', '', 'N/A')
                self.report_check.append(t10)

                t3 = ('Elastic Section Modulus of the Base Plate (mm^3)', '', bp_section_modulus(self.bp_length_provided, self.bp_width_provided,
                                                                                                 self.ze_zz), 'N/A')
                self.report_check.append(t3)

                t5 = ('Critical Section (mm)', critical_section(self.bp_length_provided, self.column_D, self.critical_xx), '', 'N/A')
                self.report_check.append(t5)

                t4 = ('Bending Stress (N/mm^2)', self.bearing_strength_concrete, bending_stress(self.load_axial_compression, self.load_moment_major, self.bp_area_provided,
                                                                    self.ze_zz, self.sigma_max_zz, self.sigma_min_zz), '')
                self.report_check.append(t4)

                t6 = ('Bending Stress - at critical section (N/mm^2)', self.bearing_strength_concrete, bending_stress_critical_sec(self.sigma_xx), '')
                self.report_check.append(t6)

                t7 = ('Bending Moment - at critical section (N-mm)', moment_critical_section(self.sigma_xx, self.sigma_max, self.critical_xx,
                                                                                             self.critical_M_xx, 0, 0, case='Case1'), '', 'N/A')
                self.report_check.append(t7)

                t8 = ('Moment Capacity of Base Plate', md_plate, '', 'N/A')
                self.report_check.append(t8)

                t9 = ('Thickness of Base Plate (mm)', 'max (' + self.column_tf + r', ' + self.column_tw + r')', plate_thk1(self.critical_M_xx,
                                                                self.plate_thk, self.gamma_m0, self.dp_bp_fy, self.bp_width_provided), '')
                self.report_check.append(t9)

            if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):

                t3 = ('k1', k1(self.eccentricity_zz, self.bp_length_provided, self.k1), '', 'N/A')
                self.report_check.append(t3)

                t4 = ('Total Area of Anchor bolt under Tension (mm^2)', total_anchor_area_tension(self.anchor_dia_outside_flange,
                                                                          (self.anchors_outside_flange / 2), self.anchor_area_tension), '', 'N/A')
                self.report_check.append(t4)

                t5 = ('Distance between centre of the Column and the C.G of the Bolt Group under Tension (mm)', calc_f(self.end_distance,
                                                                                                   self.bp_length_provided, self.f), '', 'N/A')
                self.report_check.append(t5)

                t6 = ('k2', k2(self.n, self.anchor_area_tension, self.bp_width_provided, self.f, self.eccentricity_zz, self.k2), '', 'N/A')
                self.report_check.append(t6)

                t7 = ('k3', k3(self.k2, self.bp_length_provided, self.f, self.k3), '', 'N/A')
                self.report_check.append(t7)

                t8 = ('Effective Bearing Length (mm)', y(self.k1, self.k2, self.k3, self.y), '', 'N/A')
                self.report_check.append(t8)

                t9 = ('Total Tension Demand (kN)', tension_demand_anchor(self.load_axial_compression, self.bp_length_provided, self.y,
                                                                         self.eccentricity_zz, self.f, self.tension_demand_anchor), '', 'N/A')
                self.report_check.append(t9)

                # t10 = ('Tension Demand - Anchor Bolt (kN)', tension_demand_each_anchor(self.tension_demand_anchor, (self.anchors_outside_flange / 2),
                #                               (self.tension_demand_anchor / (self.anchors_outside_flange * 0.5))), self.tension_capacity_anchor, '')
                # self.report_check.append(t10)

                t11 = ('Critical Section - Compression Side (mm)', critical_section_case_2_3(self.critical_xx, self.y), '', 'N/A')
                self.report_check.append(t11)

                t12 = ('Bending Moment - at critical section (due to bearing stress) (N-mm)', moment_critical_section(0, 0, self.critical_xx,
                                          self.critical_M_xx, self.bearing_strength_concrete, self.bp_width_provided, case='Case2&3'), '', 'N/A')
                self.report_check.append(t12)

                t13 = ('Lever Arm - distance between center of the flange and bolt group (tension side) (mm)',
                       lever_arm_tension(self.bp_length_provided, self.column_D, self.column_tf, self.end_distance, self.lever_arm), '', 'N/A')
                self.report_check.append(t13)

                t14 = ('Bending Moment - at critical section (due to tension in the anchor bolts) (N-mm)',
                       lever_arm_moment(self.tension_demand_anchor, self.lever_arm, self.moment_lever_arm), '', 'N/A')
                self.report_check.append(t14)

                t15 = ('Maximum Bending Moment (N-mm)', max_moment(self.critical_M_xx, self.moment_lever_arm), '', 'N/A')
                self.report_check.append(t15)

                t16 = ('Moment Capacity of Base Plate', md_plate, '', 'N/A')
                self.report_check.append(t16)

                t17 = ('Thickness of Base Plate (mm)', 'max (' + self.column_tf + r', ' + self.column_tw + r')', plate_thk1(self.critical_M_xx,
                                                                    self.plate_thk, self.gamma_m0, self.dp_bp_fy, self.bp_width_provided), '')
                self.report_check.append(t17)

                t18 = ('Maximum Bearing Stress on Footing (N/mm^2)', self.bearing_strength_concrete, max_bearing_stress(self.tension_demand_anchor,
                                            self.y, self.anchor_area_tension, self.n, self.bp_length_provided, self.f, self.max_bearing_stress), '')
                self.report_check.append(t18)

        # Check 4-2: Base Plate Dimensions (for Welded Column Base and Hollow/Tubular Sections)
        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):

            t1 = ('SubSection', 'Base Plate Dimensions', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t2 = ('Length (mm)', bp_length_sb(self.column_D, self.end_distance, self.bp_length_min, self.projection), self.bp_length_provided, '')
            self.report_check.append(t2)

            t3 = ('Width (mm)', bp_width(self.column_bf, self.edge_distance, self.bp_width_min), self.bp_width_provided, '')
            self.report_check.append(t3)

            t4 = ('Actual Bearing Stress (N/mm^2)', self.bearing_strength_concrete, actual_bearing_pressure(self.load_axial_compression,
                                                                                                            self.bp_area_provided, self.w), '')
            self.report_check.append(t4)

            t5 = ('Thickness (mm)', 'max (' + self.column_tf + r', ' + self.column_tw + r')', bp_thk_1(self.plate_thk, self.projection, self.w,
                                                                                                       self.gamma_m0, self.dp_bp_fy), '')
            self.report_check.append(t5)

        # Check 6: Anchor Bolt Design - Outside Column Flange
        t1 = ('SubSection', 'Anchor Bolt Design - Outside Column Flange', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t2 = (KEY_OUT_DISP_BOLT_SHEAR, '', bolt_shear_prov(self.dp_anchor_fu_overwrite, 1, self.anchor_area[1], self.gamma_mb,
                                                           self.shear_capacity_anchor), 'N/A')
        self.report_check.append(t2)

        t3 = (KEY_DISP_KB, '', kb_prov(self.end_distance, self.pitch_distance, self.anchor_hole_dia, self.dp_anchor_fu_overwrite,
                                       self.dp_column_fu), 'N/A')
        self.report_check.append(t3)

        t4 = (KEY_OUT_DISP_BOLT_BEARING, '', bolt_bearing_prov(k_b, self.anchor_dia_provided, [self.plate_thk, self.dp_bp_fu, self.dp_bp_fy],
                                                               self.gamma_mb, self.bearing_capacity_anchor), 'N/A')
        self.report_check.append(t4)

        t5 = (KEY_OUT_DISP_BOLT_CAPACITY, '', bolt_capacity_prov(self.shear_capacity_anchor, self.bearing_capacity_anchor, self.anchor_capacity), '')
        self.report_check.append(t5)

        if self.connectivity == 'Moment Base Plate':

            if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):
                t6 = ('Tension Demand - Anchor Bolt (kN)', self.tension_demand_anchor / (self.anchors_outside_flange / 2),
                                                                                        self.tension_capacity_anchor, '')
                self.report_check.append(t6)
            else:
                t6 = ('Tension Demand - Anchor Bolt (kN)', '0', self.tension_capacity_anchor, 'N/A')
                self.report_check.append(t6)

        else:
            t6 = ('Tension Demand - Anchor Bolt (kN)', '0', self.tension_capacity_anchor, 'N/A')
            self.report_check.append(t6)

        t7 = ('Anchor Length - above concrete footing (mm)', '', anchor_len_above(self.grout_thk, self.plate_thk, self.plate_washer_thk, self.nut_thk,
                                                                                  self.anchor_len_above_footing), 'N/A')
        self.report_check.append(t7)

        if self.connectivity == 'Moment Base Plate':
            if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):

                t8 = ('Anchor Length - below concrete footing (mm)', '', anchor_len_below(self.tension_capacity_anchor, self.bearing_strength_concrete,
                                                                                        self.anchor_len_below_footing), 'N/A')
                self.report_check.append(t8)
            else:
                t8 = ('Anchor Length - below concrete footing (mm)', '', 'l_{2} = ' + self.anchor_length_provided + '', 'N/A')
                self.report_check.append(t8)
        else:
            t8 = ('Anchor Length - below concrete footing (mm)', '', 'l_{2} = ' + self.anchor_length_provided + '', '')
            self.report_check.append(t8)

        t9 = ('Anchor Length (total) (mm)', anchor_range(self.anchor_length_min, self.anchor_length_max), anchor_length(self.anchor_len_above_footing,
                                                                            self.anchor_len_below_footing, self.anchor_length_provided), '')
        self.report_check.append(t9)

        # Check 7: Anchor Bolt Design - Inside Column Flange
        if self.connectivity == 'Moment Base Plate':

            if self.load_axial_tension > 0:

                t1 = ('SubSection', 'Anchor Bolt Design - Inside Column Flange', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t2 = (KEY_OUT_DISP_BOLT_SHEAR, 'The bolts are not designed to carry shear force', 'N/A', 'N/A')
                self.report_check.append(t2)

                # t3 = (KEY_DISP_KB, '', kb_prov(self.end_distance, self.pitch_distance, self.anchor_hole_dia, self.dp_anchor_fu_overwrite,
                #                                self.dp_column_fu), 'N/A')
                # self.report_check.append(t3)

                t4 = (KEY_OUT_DISP_BOLT_BEARING, 'The bolts are not designed to carry shear force', 'N/A', 'N/A')
                self.report_check.append(t4)

                t5 = (KEY_OUT_DISP_BOLT_CAPACITY, 'N/A', 'N/A', 'N/A')
                self.report_check.append(t5)

                t6 = ('Tension Demand (kN)', uplift_demand(self.load_axial_tension), '', 'N/A')
                self.report_check.append(t6)

                t7 = ('Tension Capacity (kN)', '', cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy[0], self.anchor_fu_fy[1],
                                                                self.anchor_area[0], self.anchor_area[1], self.tension_capacity_anchor_uplift,
                                                                                             safety_factor_parameter=self.dp_weld_fab), 'N/A')
                self.report_check.append(t7)

                t8 = ('Anchor Bolts Required (kN)', no_bolts_uplift(self.load_axial_tension, self.tension_capacity_anchor_uplift),
                                                                                                  self.anchors_inside_flange, '')
                self.report_check.append(t8)

                t9 = ('Anchor Length - above concrete footing (mm)', '', anchor_len_above(self.grout_thk, self.plate_thk, self.plate_washer_thk, self.nut_thk,
                                                                                          self.anchor_len_above_footing), 'N/A')
                self.report_check.append(t9)

                if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):
                    t10 = ('Anchor Length - below concrete footing (mm)', '', anchor_len_below(self.tension_capacity_anchor,
                                                                               self.bearing_strength_concrete, self.anchor_len_below_footing), 'N/A')
                    self.report_check.append(t10)
                else:
                    t10 = ('Anchor Length - below concrete footing (mm)', '', 'l_{2} = ' + self.anchor_length_provided + '', 'N/A')
                    self.report_check.append(t10)

                t11 = ('Anchor Length (total) (mm)', anchor_range(self.anchor_length_min, self.anchor_length_max),
                       anchor_length(self.anchor_len_above_footing, self.anchor_len_below_footing, self.anchor_length_provided), '')
                self.report_check.append(t11)

        # Check 8: Stiffener Design - Along Column Flange

        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Moment Base Plate'):

            if self.stiffener_along_flange == 'Yes':

                t1 = ('SubSection', 'Stiffener Design - Along Column Flange', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t2 = ('Length of Stiffener (mm)', '', stiff_len_flange(self.bp_width_provided, self.column_bf, self.stiffener_plt_len_along_flange),
                      'N/A')
                self.report_check.append(t2)

                t3 = ('Height of Stiffener (mm)', '', stiff_height_flange(self.stiffener_plt_len_along_flange, self.stiffener_plt_height_along_flange),
                      'N/A')
                self.report_check.append(t3)

                t4 = ('Thickness of Stiffener (mm)', stiff_thk_flange(self.stiffener_plt_len_along_flange, self.epsilon, self.column_tf),
                                                                                            self.stiffener_plt_thick_along_flange, '')
                self.report_check.append(t4)

                t5 = ('Max. Stress at Stiffener (N/mm^2)', self.bearing_strength_concrete, stiffener_stress_flange(self.sigma_xx), '')
                self.report_check.append(t5)

                t6 = ('Shear on Stiffener (kN)', shear_demand_stiffener(self.sigma_xx, self.stiffener_plt_len_along_flange,
                                                                        self.stiffener_plt_height_along_flange, self.shear_on_stiffener_along_flange,
                                                                        location='flange'),
                      shear_capacity_stiffener(self.stiffener_plt_thick_along_flange, self.stiffener_plt_height_along_flange, self.stiffener_fy,
                                               self.shear_capa_stiffener_along_flange, self.gamma_m0, location='flange'), '')
                self.report_check.append(t6)

                t7 = ('Plastic Section Modulus of Stiffener (mm^3)', '', zp_stiffener(self.z_p_stiffener_along_flange), 'N/A')
                self.report_check.append(t7)

                t8 = ('Moment on Stiffener (kN-m)', moment_demand_stiffener(self.sigma_xx, self.stiffener_plt_thick_along_flange,
                                                    self.stiffener_plt_len_along_flange, self.moment_on_stiffener_along_flange, location='flange'),
                      moment_capacity_stiffener(self.z_p_stiffener_along_flange, self.stiffener_fy, self.gamma_m0,
                                                self.moment_capa_stiffener_along_flange, location='flange'), '')
                self.report_check.append(t8)

            if self.stiffener_along_web == 'Yes':

                t1 = ('SubSection', 'Stiffener Design - Along Column Web', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t2 = ('Length of Stiffener (mm)', '', stiff_len_web(self.bp_length_provided, self.column_D, self.stiffener_plt_len_along_web), 'N/A')
                self.report_check.append(t2)

                t3 = ('Height of Stiffener (mm)', '', stiff_height_web(self.stiffener_plt_len_along_web, self.stiffener_plt_height_along_web), 'N/A')
                self.report_check.append(t3)

                t4 = ('Thickness of Stiffener (mm)', stiff_thk_web(self.stiffener_plt_len_along_web, self.epsilon, self.column_tw),
                                                                                            self.stiffener_plt_thick_along_web, '')
                self.report_check.append(t4)

                if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                    t5 = ('Max. Stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_web(0, 0, self.sigma_xx, 0,
                                                                                                            type='welded_hollow_bp', case='None'), '')
                    self.report_check.append(t5)

                if self.connectivity == 'Moment Base Plate':

                    if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):
                        t5 = ('Max. Stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_web(0, 0, self.sigma_max_zz,
                                                                    (self.bearing_strength_concrete / 0.45), type='moment_bp', case='Case2&3'), '')
                        self.report_check.append(t5)

                    else:
                        t5 = ('Max. Stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_web(self.sigma_max_zz, self.sigma_xx,
                                                                                                        0, 0, type='moment_bp', case='Case1'), '')
                        self.report_check.append(t5)

                t6 = ('Shear on Stiffener (kN)', shear_demand_stiffener(((self.sigma_max_zz + self.sigma_xx) / 2), self.stiffener_plt_len_along_web,
                                                                        self.stiffener_plt_height_along_web, self.shear_on_stiffener_along_web,
                                                                        location='web'),
                      shear_capacity_stiffener(self.stiffener_plt_thick_along_web, self.stiffener_plt_height_along_web, self.stiffener_fy,
                                               self.shear_capa_stiffener_along_web, self.gamma_m0, location='web'), '')
                self.report_check.append(t6)

                t7 = ('Plastic Section Modulus of Stiffener (mm^3)', '', zp_stiffener(self.z_p_stiffener_along_web), 'N/A')
                self.report_check.append(t7)

                t8 = ('Moment on Stiffener (kN-m)', moment_demand_stiffener(((self.sigma_max_zz + self.sigma_xx) / 2),
                    self.stiffener_plt_thick_along_web, self.stiffener_plt_len_along_web, self.moment_on_stiffener_along_web, location='web'),
                      moment_capacity_stiffener(self.z_p_stiffener_along_web, self.stiffener_fy, self.gamma_m0,
                                                self.moment_capa_stiffener_along_web, location='web'), '')
                self.report_check.append(t8)

            if self.stiffener_across_web == 'Yes':

                t1 = ('SubSection', 'Stiffener Design - Across Column Web', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t2 = ('Length of Stiffener (mm)', '', stiff_len_across_web(self.stiffener_plt_len_along_flange, self.stiffener_plt_len_along_web,
                                                                           self.stiffener_plt_len_across_web), 'N/A')
                self.report_check.append(t2)

                t3 = ('Height of Stiffener (mm)', '', stiff_height_across_web(self.stiffener_plt_len_across_web,
                                                                              self.stiffener_plt_height_across_web), 'N/A')
                self.report_check.append(t3)

                t4 = ('Thickness of Stiffener (mm)', stiff_thk_across_web(self.stiffener_plt_len_across_web, self.epsilon, self.column_tw),
                                                                                            self.stiffener_plt_thick_across_web, '')
                self.report_check.append(t4)

                if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                    t5 = ('Max. Stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_across_web(self.sigma_web, 0, 0,
                                                                                                                       type='welded_hollow_bp',
                                                                                                                       case='None'), '')
                    self.report_check.append(t5)

                if self.connectivity == 'Moment Base Plate':

                    if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):
                        t5 = ('Max. Stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_across_web(self.sigma_web, 0, 0,
                                                                                                                           type='moment_bp',
                                                                                                                           case='Case2&3'), '')
                        self.report_check.append(t5)

                    else:
                        t5 = ('Max. Stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_across_web(self.sigma_web,
                                                                   self.sigma_max_zz, self.sigma_min_zz, type='moment_bp', case='Case1'), '')
                        self.report_check.append(t5)

                t6 = ('Shear on Stiffener (kN)', shear_demand_stiffener(((self.sigma_max_zz + self.sigma_xx) / 2), self.stiffener_plt_len_across_web,
                                                                        self.stiffener_plt_height_across_web, self.shear_on_stiffener_across_web,
                                                                        location='across_web'),
                      shear_capacity_stiffener(self.stiffener_plt_thick_across_web, self.stiffener_plt_height_across_web, self.stiffener_fy,
                                               self.shear_capa_stiffener_across_web, self.gamma_m0, location='across_web'), '')
                self.report_check.append(t6)

                t7 = ('Plastic Section Modulus of Stiffener (mm^3)', '', zp_stiffener(self.z_p_stiffener_across_web), 'N/A')
                self.report_check.append(t7)

                t8 = ('Moment on Stiffener (kN-m)', moment_demand_stiffener(((self.sigma_max_zz + self.sigma_xx) / 2),
                self.stiffener_plt_thick_across_web, self.stiffener_plt_len_across_web, self.moment_on_stiffener_across_web, location='across_web'),
                      moment_capacity_stiffener(self.z_p_stiffener_across_web, self.stiffener_fy, self.gamma_m0,
                                                self.moment_capa_stiffener_across_web, location='across_web'), '')
                self.report_check.append(t8)

        # End of checks

        display_3D_image = "/ResourceFiles/images/BasePlate.jpeg"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']

        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext, rel_path, display_3D_image)
