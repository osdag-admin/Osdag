"""Module for Indian Standard, IS 800 : 2007

Started on 01 - Nov - 2018

@author: ajmalbabums
"""
import math
from Common import *
# from Common import KEY_DP_FAB_SHOP


class IS800_2007(object):
    """Perform calculations on steel design as per IS 800:2007

    """

    # ==========================================================================
    """    SECTION  1     GENERAL   """
    # ==========================================================================
    """    SECTION  2     MATERIALS   """
    # -------------------------------------------------------------
    #   5.4 Strength
    # -------------------------------------------------------------

    # Clause 3.7 - Classification of cross-section, Table 2, Limiting width to thickness ratio
    @staticmethod
    def Table2_web_OfI_H_box_section(depth, web_thickness, f_y, axial_load, load_type='Compression', section_class='Plastic'):
        """ Calculate the limiting width to thickness ratio; for web of an I, H or Box section in accordance to Table 2

        Args:
            depth: depth of the web in mm (float or int)
            web_thickness: thickness of the web in mm (float or int)
            f_y: yield stress of the section material in N/MPa (float or int)
            axial_load: Axial load (Tension or Compression) acting on the member (i.e. web) in N (float or int)
            load_type: Type of axial load (Tension or Compression) (string)
            section_class: Class of the section (Class1 - Plastic, Class2 - Compact or Class3 - Semi-compact) (string)

        Returns:
            Results of the checks; 1. Neutral axis at mid-depth, 2. Generally (when there is axial tension or compression force acting on the section),
            and 3. Axial compression, in the form of (list)
            'Pass', if the section qualifies as the required section_class, 'Fail' if it does not

        Reference: Table 2 and Cl.3.7.2, IS 800:2007

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        epsilon = math.sqrt(250 / f_y)

        ratio = depth / web_thickness  # ratio of the web/component

        # Check 1: Neutral axis at mid-depth
        if section_class == 'Plastic':
            if ratio <= (84 * epsilon):
                check_1 = 'Pass'
            else:
                check_1 = 'Fail'
        elif section_class == 'Compact':
            if ratio <= (105 * epsilon):
                check_1 = 'Pass'
            else:
                check_1 = 'Fail'
        else:  # 'Semi-compact'
            if ratio <= (126 * epsilon):
                check_1 = 'Pass'
            else:
                check_1 = 'Fail'

        # Check 2: Generally (when there is axial tension or compression force acting on the section)
        actual_avg_stress = axial_load / (depth * web_thickness)  # N/mm^2 or MPa
        design_compressive_stress = f_y / gamma_m0  # N/mm^2 or MPa, design compressive stress only of web (cl. 7.1.2.1, IS 800:2007)
        r_1 = actual_avg_stress / design_compressive_stress  # stress ratio

        if load_type == 'Compression':
            r_1 = r_1
        else:
            r_1 = - r_1  # r_1 is negative for axial tension

        if section_class == 'Plastic':
            if ratio <= (min(((84 * epsilon) / (1 + r_1)), 42 * epsilon)):
                check_2 = 'Pass'
            else:
                check_2 = 'Fail'
        elif section_class == 'Compact':
            if r_1 < 0:
                if ratio <= ((105 * epsilon) / (1 + r_1)):
                    check_2 = 'Pass'
                else:
                    check_2 = 'Fail'
            else:
                if ratio <= (min(((105 * epsilon) / (1 + (1.5 * r_1))), 42 * epsilon)):
                    check_2 = 'Pass'
                else:
                    check_2 = 'Fail'
        else:  # 'Semi-compact'
            if ratio <= (min(((126 * epsilon) / (1 + (2 * r_1))), 42 * epsilon)):
                check_2 = 'Pass'
            else:
                check_2 = 'Fail'

        # Check 3: Axial compression
        if section_class == 'Semi-compact':
            if ratio <= (42 * epsilon):
                check_3 = 'Pass'
            else:
                check_3 = 'Fail'
        else:
            check_3 = 'Pass'  # Not-applicable to Plastic and Compact sections (hence, Pass)

        return [check_1, check_2, check_3]

    @staticmethod
    def Table2_hollow_tube(diameter, thickness, f_y, load='Axial Compression', section_class='Plastic'):
        """ Calculate the limiting width to thickness ratio; for a hollow tube section in accordance to Table 2

        Args:
            diameter: diameter of the tube in mm (float or int)
            thickness: thickness of the tube in mm (float or int)
            f_y: yield stress of the section material in N/MPa (float or int)
            load: Type of load ('Axial Compression' or 'Moment') (string)
            section_class: Class of the section (Class1 - Plastic, Class2 - Compact or Class3 - Semi-compact) (string)

        Returns:
            Results of the section classification check(s)
            'Pass', if the section qualifies as the required section_class, 'Fail' if it does not

        Reference: Table 2 and Cl.3.7.2, IS 800:2007

        """
        epsilon = math.sqrt(250 / f_y)

        ratio = diameter / thickness  # ratio of the web/component

        # Check 1: If the load acting is Moment
        if load == 'Moment':

            if section_class == 'Plastic':
                if ratio <= (42 * epsilon ** 2):
                    check = 'Pass'
                else:
                    check = 'Fail'
            elif section_class == 'Compact':
                if ratio <= (52 * epsilon ** 2):
                    check = 'Pass'
                else:
                    check = 'Fail'
            else:
                if ratio <= (146 * epsilon ** 2):
                    check = 'Pass'
                else:
                    check = 'Fail'

        # Check 1: If the load acting is Axial Compression
        elif load == 'Axial Compression':

            if section_class == 'Plastic':
                check = 'Pass'
            elif section_class == 'Compact':
                check = 'Pass'
            else:
                if ratio <= (88 * epsilon ** 2):
                    check = 'Pass'
                else:
                    check = 'Fail'
        else:
            pass

        return check

    @staticmethod
    def Table2_i(width, thickness, f_y, section_type='Rolled'):
        """ Calculate the limiting width to thickness ratio as per Table 2 for;
                sr. no i) Outstanding element of compression flange

        Args:
            width: width of the element in mm (float or int)
            thickness: thickness of the element in mm (float or int)
            f_y: yield stress of the section material in MPa (float or int)
            section_type: Type of section ('Rolled' or 'Welded') (string)

        Returns:
            A list of values with;
            1- The class of the section as Plastic, Compact, Semi-compact or Slender on account of the flange
            2- Ratio

            ['Section Class', 'Ratio']

        Reference: Table 2 and Cl.3.7.2, IS 800:2007

        """
        epsilon = math.sqrt(250 / f_y)
        
        ratio = width / thickness

        if section_type == 'Rolled':
            if ratio <= (9.4 * epsilon):
                section_class = 'Plastic'
            elif ratio <= (10.5 * epsilon):
                section_class = 'Compact'
            elif ratio <= (15.7 * epsilon):
                section_class = 'Semi-Compact'
            else:
                section_class = 'Slender'
        else:
            if ratio <= (8.4 * epsilon):
                section_class = 'Plastic'
            elif ratio <= (9.4 * epsilon):
                section_class = 'Compact'
            elif ratio <= (13.6 * epsilon):
                section_class = 'Semi-Compact'
            else:
                section_class = 'Slender'
        print(f" flange_class"
                    f" width {width}"
                    f" thickness {thickness}"
                    f" epsilon {epsilon}"
                    )
        print(f" section_type {section_type}"
              f" section_class {section_class}")
        return [section_class, ratio]

    @staticmethod
    def Table2_iii(depth, thickness, f_y, classification_type='Neutral axis at mid-depth'):
        """ Calculate the limiting width to thickness ratio as per Table 2 for;
                sr. no iii) Web of an I, H or box section for axial compression

        Args:
            depth: width of the element in mm (float or int)
            thickness: thickness of the element in mm (float or int)
            f_y: yield stress of the section material in MPa (float or int)
            classification_type: Type of classification required (Neutral axis at mid-depth, Generaly, Axial Compression) (string)

        Returns:
            The class of the section as Plastic, Compact, Semi-compact or Slender on account of the web

        Reference: Table 2 and Cl.3.7.2, IS 800:2007

        """
        epsilon = math.sqrt(250 / f_y)

        ratio = depth / thickness

        print(f" web_class \n" 
              f" depth {depth} \n"
              f" thickness {thickness} \n"
              f" epsilon {epsilon} \n"
               f" classification_type {classification_type}\n"
              )

        if classification_type == 'Neutral axis at mid-depth':
            if ratio < (84 * epsilon):
                section_class = KEY_Plastic
            elif ratio < (105 * epsilon):
                section_class = KEY_Compact
            elif ratio < (126 * epsilon):
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'

        elif classification_type == 'Generally':
            pass
        elif classification_type == 'Axial compression':
            if ratio > (42 * epsilon):
                section_class = 'Slender'
            else:
                section_class = 'Semi-Compact'
        print(f" section_class {section_class}")

        return section_class

    @staticmethod
    def Table2_iv(depth, thickness_web, f_y):
        """ Calculate the limiting width to thickness ratio as per Table 2 for;
                sr. no i) Members subjected to Axial Compression
                sr. no ii)Members subjected to Compression due to bending

        Args:
            width(b): width of the element in mm (float or int)
            depth(d): depth of the element in mm (float or int)
            thickness(t): thickness of the element in mm (float or int)
            f_y: yield stress of the section material in MPa (float or int)
            force_type: Type of failure in member ('Axial') ('Compression')
            section_type: Type of section ('Angle') (string)

        Returns:
            A list of values with;
            1- The class of the section as Semi-compact or Slender on account of the
             b/t, d/t, (b+d)/t Ratio

            ['Section Class', 'Ratio']

        Reference: Table 2 and Cl.3.7.2, IS 800:2007

        """
        epsilon = math.sqrt(250 / int(f_y))
        d_t = depth / thickness_web

        if d_t <= (42 * epsilon) :
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'

        return [section_class, d_t]

    @staticmethod
    def Table2_vi(width, depth, thickness, f_y, force_type = "Axial Compression"):
        """ Calculate the limiting width to thickness ratio as per Table 2 for;
                sr. no i) Members subjected to Axial Compression
                sr. no ii)Members subjected to Compression due to bending

        Args:
            width(b): width of the element in mm (float or int)
            depth(d): depth of the element in mm (float or int)
            thickness(t): thickness of the element in mm (float or int)
            f_y: yield stress of the section material in MPa (float or int)
            force_type: Type of failure in member ('Axial') ('Compression')
            section_type: Type of section ('Angle') (string)

        Returns:
            A list of values with;
            1- The class of the section as Semi-compact or Slender on account of the 
             b/t, d/t, (b+d)/t Ratio

            ['Section Class', 'Ratio']

        Reference: Table 2 and Cl.3.7.2, IS 800:2007

        """
        epsilon = math.sqrt(250 / int(f_y))

        b_t = width / thickness
        d_t = depth / thickness
        bd_t = (width + depth) / thickness


        if force_type == 'Axial Compression':
            if b_t <= (15.7 * epsilon) and d_t<= (15.7 * epsilon) and  bd_t<= (25 * epsilon):
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'
        else:
            if b_t <= (9.4 * epsilon) and d_t<= (9.4 * epsilon):
                section_class = KEY_Plastic
            elif b_t <= (10.5 * epsilon) and d_t<= (10.5 * epsilon):
                section_class = KEY_Compact
            elif b_t <= (15.7 * epsilon) and d_t<= (15.7 * epsilon):
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'

        return [section_class, b_t,d_t, bd_t ]

    @staticmethod
    def Table2_vii(width, depth, thickness, f_y, force_type = "Axial Compression"):
        """ Calculate the limiting width to thickness ratio as per Table 2 for;
                sr. no i) Members subjected to Axial Compression
                sr. no ii)Members subjected to Compression due to bending

        Args:
            width(b): width of the element in mm (float or int)
            depth(d): depth of the element in mm (float or int)
            thickness(t): thickness of the element in mm (float or int)
            f_y: yield stress of the section material in MPa (float or int)
            force_type: Type of failure in member ('Axial') ('Compression')
            section_type: Type of section ('Angle') (string)

        Returns:
            A list of values with;
            1- The class of the section as Semi-compact or Slender on account of the
             b/t, d/t, (b+d)/t Ratio

            ['Section Class', 'Ratio']

        Reference: Table 2 and Cl.3.7.2, IS 800:2007

        """
        epsilon = math.sqrt(250 / int(f_y))

        b_t = width / thickness
        d_t = depth / thickness
        bd_t = (width + depth) / thickness

        if force_type == 'Axial Compression':
            if d_t<= (15.7 * epsilon) :
                '''When adding more cases, you need to modify Strut angle'''
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'
        else:
            if b_t <= (9.4 * epsilon) and d_t<= (9.4 * epsilon):
                section_class = KEY_Plastic
            elif b_t <= (10.5 * epsilon) and d_t<= (10.5 * epsilon):
                section_class = KEY_Compact
            elif b_t <= (15.7 * epsilon) and d_t<= (15.7 * epsilon):
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'

        return [section_class, b_t,d_t, bd_t ]


    @staticmethod
    def Table2_x(outer_diameter, tube_thickness, f_y, load_type='axial compression'):
        """ Calculate the limiting width to thickness ratio as per Table 2 for;
                sr. no x) Circular hollow tube

        Args:
            outer_diameter: outer diameter of the tube in mm (float or int)
            tube_thickness: thickness of the tube in mm (float or int)
            f_y: yield stress of the section material in MPa (float or int)
            load_type: Type of loading (moment, axial compression) (string)

        Returns:
            The class of the section as Plastic, Compact, Semi-compact or Slender

        Reference: Table 2 and Cl.3.7.2, IS 800:2007

        """
        epsilon = math.sqrt(250 / f_y)

        ratio = outer_diameter / tube_thickness

        print(f"outer_diameter{outer_diameter},tube_thickness{tube_thickness}")

        if load_type == 'axial compression':
            if ratio > (88 * epsilon**2):
                section_class = 'Slender'
            else:
                section_class = 'Semi-Compact'
        else:
            if ratio <= (42 * epsilon**2):
                section_class = 'Plastic'
            elif (ratio > (42 * epsilon**2)) and (ratio <= (52 * epsilon**2)):
                section_class = 'Compact'
            elif ratio <= (146 * epsilon**2):
                section_class = 'Semi-Compact'
            else:
                section_class = 'Slender'

        return section_class
    

    # ==========================================================================
    """    SECTION  3     GENERAL DESIGN REQUIREMENTS   """

    @staticmethod
    def cl_3_8_max_slenderness_ratio(Type = 1):
        """
            1)  A member carrying compressive loads
                resulting from dead loads and imposed
                loads
            2)  A tension member in which a reversal
                of direct stress occurs due to loads other
                than wind or seismic forces
            3)  A member subjected to compression
                forces resulting only from combination
                with wind/earthquake actions, provided
                the deformation of such member does
                not adversely affect tbe stress in any
                part of the structure
            4)  Compression flange of a beam against
                lateral torsional buckling
            5)  A member normally acting m a tie in a
                roof truss or a bracing system not
                considered effective when subject to
                possible reversal of stress into
                compression resulting from the action
                of wind or earthquake forces]]
            6)  Members always under tension’) (other
                than pre-tensioned members)
        """
        if Type == 1:
            return 180
        elif Type == 2:
            return 180
        elif Type == 3:
            return 180
        elif Type == 4:
            return 180
        elif Type == 5:
            return 180
        elif Type == 6:
            return 180
    # ==========================================================================
    """    SECTION  4     METHODS OF STRUCTURAL ANALYSIS   """
    # ==========================================================================
    """    SECTION  5     LIMIT STATE DESIGN   """
    # -------------------------------------------------------------
    #   5.4 Strength
    # -------------------------------------------------------------

    # Table 5 Partial Safety Factors for Materials, gamma_m (dict)
    cl_5_4_1_Table_5 = {"gamma_m0": {'yielding': 1.10, 'buckling': 1.10},
                        "gamma_m1": {'ultimate_stress': 1.25},
                        "gamma_mf": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
                        "gamma_mb": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
                        "gamma_mr": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.25},
                        "gamma_mw": {KEY_DP_FAB_SHOP: 1.25, KEY_DP_FAB_FIELD: 1.50}
                        }

    # ==========================================================================
    """    SECTION  6     DESIGN OF TENSION MEMBERS   """

    # ------------------------------------------------------------
    #   6.2 Design Strength Due to Yielding of Gross Section
    # -------------------------------------------------------------

    @staticmethod
    def cl_6_2_tension_yielding_strength(A_g, f_y):
        """Calcualte the tension rupture capacity of plate as per clause 6.3.1
        :param A_g: gross area of cross section
        :param f_y: yield stress of the material
        :return: design strength in tension yielding
        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        T_dg = A_g * f_y / gamma_m0
        return T_dg
    # ------------------------------------------------------------
    #   6.3 Design Strength Due to Rupture of Critical Section
    # -------------------------------------------------------------

    # cl.6.3.1 Plates
    @staticmethod
    def cl_6_3_1_tension_rupture_strength(A_n,f_u):
        """Calcualte the tension rupture capacity of plate as per clause 6.3.1
        :param A_n: net effective area of member
        :param f_u: ultimate stress of the material
        :return: design strength in tension rupture
        """
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_dn = 0.9*A_n*f_u/gamma_m1
        return T_dn
    #   6.4 Design Strength Due to Block Shear
    # -------------------------------------------------------------

    # cl. 6.4.1 Block shear strength of bolted connections
    @staticmethod
    def cl_6_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1

        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)

        Return:
            block shear strength of bolted connection in N (float)

        Note:
            Reference:
            IS 800:2007, cl. 6.4.1

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        return min(T_db1, T_db2)

    # ==========================================================================
    """    SECTION  7     DESIGN OF COMPRESS1ON MEMBERS   """

    # -------------------------------------------------------------
    #   7.4 Column Bases
    # -------------------------------------------------------------

    # cl. 7.4.1, General
    @staticmethod
    def cl_7_4_1_bearing_strength_concrete(concrete_grade):
        """
        Args:
            concrete_grade: grade of concrete used for pedestal/footing (str).

        Returns:
            maximum permissible bearing strength of concrete pedestal/footing (float).

        Note:
            cl 7.4.1 suggests the maximum bearing strength equal to 0.60 times f_ck,
            but, the value is amended to 0.45 times f_ck (f_ck is the characteristic strength of concrete)
        """
        f_ck = {
            'M10': 10,
            'M15': 15,
            'M20': 20,
            'M25': 25,
            'M30': 30,
            'M35': 35,
            'M40': 40,
            'M45': 45,
            'M50': 50,
            'M55': 55,
        }[str(concrete_grade)]

        bearing_strength = 0.45 * f_ck  # MPa (N/mm^2)
        return bearing_strength

    # cl. 7.1, Design strength
    @staticmethod
    def cl_7_1_2_design_compressisive_strength_member( effective_area , design_compressive_stress , axial_load ):
        """
        Args:
            effective_area:effective sectional area as defined in 7.3.2                             (float)
            design_compressive_stress:design compressive stress, obtained as per 7.1.2.1            (float)
            axial_load:Load acting on column                                                        (float)

        Returns:
            Design compressive strength
           'Pass', if the section qualifies as the required section_class, 'Fail' if it does not

        Note:
            Reference: IS 800 pg34
            @author:Rutvik Joshi
        """
        design_compressive_strength= effective_area * design_compressive_stress                     #area in mm2,stress in kN/mm2
        if axial_load < design_compressive_strength:                                                #kN
            check = 'pass'
        else:
            check = 'fail'
        return check                                                                                #str

    # cl. 7.2.2 Effective Length of Prismatic Compression Members
    @staticmethod
    def cl_7_2_2_effective_length_of_prismatic_compression_members(unsupported_length, end_1='Fixed', end_2='Fixed'):
        """
        Calculate the effective length of the member as per Cl. 7.2.2 (Table 11) of IS 800:2007

        Args:
            unsupported_length: unsupported length of the member about any axis in mm (float)
            end_1: End condition at end 1 of the member (string)
            end_2: End condition at end 2 of the member (string)

        Returns:
            Effective length in mm
        """

        if end_1 == 'Fixed' and end_2 == 'Fixed':
            effective_length = 0.65 * unsupported_length
        elif end_1 == 'Fixed' and end_2 == 'Hinged':
            effective_length = 0.8 * unsupported_length
        elif end_1 == 'Fixed' and end_2 == 'Roller':
            effective_length = 1.2 * unsupported_length
        elif end_1 == 'Hinged' and end_2 == 'Hinged':
            effective_length = 1.0 * unsupported_length
        elif end_1 == 'Hinged' and end_2 == 'Roller':
            effective_length = 2.0 * unsupported_length
        elif end_1 == 'Fixed' and end_2 == 'Free':
            effective_length = 2.0 * unsupported_length
        else:
            effective_length = 2.0 * unsupported_length

        return effective_length

    @staticmethod
    def cl_7_2_4_effective_length_of_truss_compression_members(length, section_profile = 'Angles'):
        """
        Calculate the effective length of the member as per Cl. 7.5.2.1 (Table 11) of IS 800:2007

        Args:
            unsupported_length: actual length of the member about any axis in mm (float)
            end_1: End condition at end 1 of the member (string)
            end_2: End condition at end 2 of the member (string)

        Returns:
            Effective length in mm
        """

        if section_profile == 'Angles':
            effective_length = 1 * length
        elif section_profile == 'Back to Back Angles':
            effective_length = 0.85 * length
        elif section_profile == 'Channels':
            print('NEED TO CHECK AGAIN')
            effective_length = 1 * length
        elif section_profile == 'Back to Back Channels':
            print('NEED TO CHECK AGAIN')
            effective_length = 0.85 * length
        else:
            effective_length = 1 * length

        return effective_length

    # cl. 7.1.2.1, Design stress
    @staticmethod
    def cl_7_1_2_1_design_compressisive_stress(f_y, gamma_mo, effective_slenderness_ratio , imperfection_factor, modulus_of_elasticity, check_type ):
        """
        Args:
            f_y:Yield stress                                                                        (float)
            gamma_mo:Effective length of member                                                        (float)
            effective_slenderness_ratio:Euler buckling class                                                       (float)
            imperfection_factor
            modulus_of_elasticity

        Returns:
            list of euler_buckling_stress, nondimensional_effective_slenderness_ratio, phi, stress_reduction_factor, design_compressive_stress_fr .design_compressive_stress, design_compressive_stress_min
        Note:
            Reference: IS 800 pg34
            @author:Rutvik Joshi
        """
        # 2.4 - Euler buckling stress
        euler_buckling_stress = (math.pi ** 2 * modulus_of_elasticity) / effective_slenderness_ratio ** 2
        if 'Concentric' in check_type:
            # 2.5 - Non-dimensional effective slenderness ratio
            nondimensional_effective_slenderness_ratio = math.sqrt(f_y / euler_buckling_stress)
        elif 'Leg' in check_type:
            nondimensional_effective_slenderness_ratio = check_type[1]
        phi = 0.5 * (1 + imperfection_factor * (nondimensional_effective_slenderness_ratio - 0.2) + nondimensional_effective_slenderness_ratio ** 2)
        # 2.6 - Design compressive stress
        stress_reduction_factor = 1/(phi + math.sqrt(phi**2 - nondimensional_effective_slenderness_ratio**2))
        design_compressive_stress_fr = f_y * stress_reduction_factor / gamma_mo
        design_compressive_stress_max = f_y / gamma_mo
        design_compressive_stress = min(design_compressive_stress_fr , design_compressive_stress_max)
        return [euler_buckling_stress, nondimensional_effective_slenderness_ratio, phi, stress_reduction_factor,design_compressive_stress_fr, design_compressive_stress, design_compressive_stress_max]                                                                                  #kN/cm2

    # Cl. 7.1.1, Cl.7.1.2.1, Imperfection Factor
    @staticmethod
    def cl_7_1_2_1_imperfection_factor(buckling_class=''):
        """
        Determine the Imperfection Factor of the cross-section as per Cl 7.1.1, Cl.7.1.2.1 (Table 7) of IS 800:2007

        Args:
            buckling_class (string)

        Returns: Imperfection factor value (string)
        """
        imperfection_factor = {
            'a': 0.21,
            'b': 0.34,
            'c': 0.49,
            'd': 0.76
        }[buckling_class]

        return imperfection_factor

    # cl. 7.1.2.1, Buckling Class of Cross-Sections
    @staticmethod
    def cl_7_1_2_2_buckling_class_of_crosssections(b, h, t_f, cross_section='Rolled I-sections', section_type='Hot rolled'):
        """
        Determine the buckling class of the cross-section as per Cl 7.1.2.2 (Table 10) of IS 800:2007

        Args:
            b: width of the flange
            h: depth of the section
            t_f: thickness of the flange
            cross_section: type of cross-section
            section_type: Hot rolled or Cold formed

        Returns: Buckling class values about z-z and y-y axis (dictionary)
        """

        if cross_section == 'Rolled I-sections':
            if h / b > 1.2:
                if t_f <= 40:
                    buckling_class = {
                        'z-z': 'a',
                        'y-y': 'b'
                    }
                elif 40 <= t_f <= 100:
                    buckling_class = {
                        'z-z': 'b',
                        'y-y': 'c'
                    }
                else:  # this case if not derived from the code (for t_f >100mm, buckling class d is assumed about both the axis)
                    buckling_class = {
                        'z-z': 'd',
                        'y-y': 'd'
                    }
            elif h / b <= 1.2:
                if t_f <= 100:
                    buckling_class = {
                        'z-z': 'b',
                        'y-y': 'c'
                    }
                if t_f > 100:
                    buckling_class = {
                        'z-z': 'd',
                        'y-y': 'd'
                    }

        elif cross_section == 'Welded I-section':
            if t_f <= 40:
                buckling_class = {
                    'z-z': 'b',
                    'y-y': 'c'
                }
            if t_f > 40:
                buckling_class = {
                    'z-z': 'c',
                    'y-y': 'd'
                }

        elif cross_section == 'Hollow Section':
            if section_type == 'Hot rolled':
                buckling_class = {
                    'z-z': 'a',
                    'y-y': 'a'
                }
            else:
                buckling_class = {
                    'z-z': 'b',
                    'y-y': 'b'
                }

        return buckling_class

    @staticmethod
    def cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(length, r_min, b1, b2, t, f_y, bolt_no = 2, fixity = 'Fixed'):
        """
        Calculate the equivalent slenderness ratio of the member as per Cl. 7.5.1.2 (Table 12) of IS 800:2007

        Args:
            length: actual length of the member about any axis in mm (float)
            end_1: End condition at end 1 of the member (string)
            end_2: End condition at end 2 of the member (string)
            r_min: minimum radius of gyration of the section(angle)
            b1: leg of section(angle) (float)
            b2: another leg of section(angle) (float)
            t : thickness (float)
            f_y: yield strength (float)
            bolt_no: number of bolt in the connection (float)
            fixity = depends on end_1 and end_2 (string)

        Returns:
            list of
            equivalent_slenderness_ratio
            lambda_vv, lambda_psi defined in clause
            k1, k2, k3
        """
        e = math.sqrt(250/f_y )
        E = 2 * 10 ** 5
        if bolt_no >= 2:
            if fixity == 'Fixed':
                k1 = 0.2
                k2 = 0.35
                k3 = 20
            elif fixity == 'Hinged':
                k1 = 0.7
                k2 = 0.6
                k3 = 5
            elif fixity == 'Partial':
                temp = cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(length, r_min, b1, b2, t, f_y, bolt_no , fixity = 'Fixed')
                temp2 = cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(length, r_min, b1, b2, t, f_y, bolt_no , fixity = 'Hinged')
                k1 = (temp[3] +temp2[3]) /2
                k2 = (temp[4] +temp2[4]) /2
                k3 = (temp[5] +temp2[5]) /2

        elif bolt_no == 1:
            if fixity == 'Fixed':
                k1 = 0.75
                k2 = 0.35
                k3 = 20
            elif fixity == 'Hinged':
                k1 = 1.25
                k2 = 0.5
                k3 = 60
            elif fixity == 'Partial':
                temp = cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(length,
                                                                                                           r_min, b1,
                                                                                                           b2, t, f_y,
                                                                                                           bolt_no,
                                                                                                           fixity='Fixed')
                temp2 = cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(length,
                                                                                                            r_min, b1,
                                                                                                            b2, t, f_y,
                                                                                                            bolt_no,
                                                                                                            fixity='Hinged')
                k1 = (temp[3] + temp2[3]) / 2
                k2 = (temp[4] + temp2[4]) / 2
                k3 = (temp[5] + temp2[5]) / 2

        lambda_vv = (length/ r_min)/(e* math.sqrt(math.pi**2 * E/250))
        lambda_psi = ((b1 + b2)/(2 * t) )/(e* math.sqrt(math.pi**2 * E/250))
        equivalent_slenderness_ratio = math.sqrt(k1 + k2 * lambda_vv **2 + k3 * lambda_psi**2)
        return [equivalent_slenderness_ratio, lambda_vv, lambda_psi, k1, k2, k3]
    # ==========================================================================
    """    SECTION  8     DESIGN OF MEMBERS SUBJECTED TO BENDING   """

    # -------------------------------------------------------------
    #   8.4 Shear
    # -------------------------------------------------------------
    @staticmethod
    def cl_8_2_1_web_buckling(d, tw, e):
        d_tw = d / tw
        if d_tw <= 67*e:
            return False
        return True

    @staticmethod
    def cl_8_2_1_2_design_bending_strength(section_class, Zp, Ze, fy, gamma_mo, support):
        beta_b = 1.0 if section_class == KEY_Plastic or KEY_Compact else Ze/Zp
        Md = beta_b * Zp * fy / gamma_mo
        if support == KEY_DISP_SUPPORT1 :
            if Md < 1.2 * Ze * fy / gamma_mo:
                return Md
            else:
                return 1.2 * Ze * fy / gamma_mo
        elif support == KEY_DISP_SUPPORT2 :
            if Md < 1.5 * Ze * fy / gamma_mo:
                return Md
            else:
                return 1.5 * Ze * fy / gamma_mo


    @staticmethod
    def cl_8_2_1_2_high_shear_check(V, Vd):
        if V > 0.6 * Vd :
            print('High shear')
            return True
        else:
            print('Low shear')
            return False

    @staticmethod
    def cl_8_2_1_4_holes_tension_zone(Anf_Agf, fy, fu, gamma_mo, gamma_m1):
        if Anf_Agf > (fy/fu) * (gamma_m1/gamma_mo) / 0.9 :
            return Anf_Agf
        else :
            return (fy/fu) * (gamma_m1/gamma_mo) / 0.9

    @staticmethod
    def cl_8_2_1_5_shear_lag(b0,b1, L0, type):
        if type == 'outstand':
            if b0<= L0/20 :
                return b0
            else :
                return L0/20
        else:
            if b1<= L0/10 :
                return b1
            else :
                return L0/10

    @staticmethod
    def cl_8_2_2_Unsupported_beam_bending_strength(Zp, Ze, fcd, section_class):
        if section_class == KEY_Plastic or section_class == KEY_Compact:
            return Zp * fcd
        else:
            return Ze * fcd

    @staticmethod
    def cl_8_2_2_Unsupported_beam_bending_compressive_stress(X_lt, fy, gamma_mo):
        return X_lt * fy / gamma_mo

    @staticmethod
    def cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(phi_lt, lambda_lt):
        si = 1 / ( phi_lt + (phi_lt **2 - lambda_lt **2) ** 0.5)
        if si > 1.0:
            si = 1.0
        return si

    @staticmethod
    def cl_8_2_2_Unsupported_beam_bending_phi_lt(alpha_lt, lambda_lt):
        a = 0.5 * ( 1 + alpha_lt * ( lambda_lt - 0.2) + lambda_lt ** 2)
        print(alpha_lt, lambda_lt, a)
        return a

    @staticmethod
    def cl_8_2_2_Unsupported_beam_bending_non_slenderness( E, meu,Iy, It, Iw, Llt,beta_b, Zp, hf,ry, tf):
        ''' Author : Rutvik Joshi
        Clauses: 8.2.2.1 and Annex E
        '''
        G = E/(2+2*meu)
        fcrb = (1.1 * math.pi**2 * E/(Llt/ry)**2) * math.sqrt(1 + (((Llt/ry)/(hf/tf))**2) / 20)
        _ = math.sqrt((math.pi**2 * E * Iy/Llt**2)*(G *It + (math.pi**2 * E * Iw/Llt**2) ))
        __ = beta_b * Zp * fcrb
        ___ = (math.pi**2 * E * Iy * hf/Llt**2)/2 * math.sqrt(1 + (((Llt/ry)/(hf/tf))**2) / 20 )
        return [min(_,__,___), fcrb]

    @staticmethod
    def cl_8_2_2_Unsupported_beam_bending_fcrb(E, Llt_ry, hf_tf):
        ''' Author : Rutvik Joshi
        Clauses: 8.2.2.1 and Annex E
        '''
        fcrb = 1.1 * math.pi**2 * E * (1 + (Llt_ry/hf_tf)**2/20)**0.5 / Llt_ry
        return fcrb
    @staticmethod
    def cl_8_2_2_1_elastic_buckling_moment(betab, Zp, Ze, fy, Mcr, fcrb = 0):
        if (betab * Zp * fy / Mcr) ** 0.5 <= (1.2 * Ze * fy / Mcr) ** 0.5:
            return (betab * Zp * fy / Mcr) ** 0.5
        else:
            return (1.2 * Ze * fy / Mcr) ** 0.5

    @staticmethod
    def cl_8_2_2_1_elastic_buckling_moment_fcrb( fy, fcrb=0):

        return math.sqrt(fy/fcrb)
    @staticmethod
    def cl_8_3_1_EffLen_Simply_Supported(Torsional, Warping, length, depth, load) :
        """ Calculate the Effective Length for Simply Supported Beams as per Table 15 Cl 8.3.1

        Args:
            Torsional Restraint: Type of Restraint (string)
            Warping Restraint: Type of Restraint (string)
            depth(d): depth of the element in mm (float or int)
            length(l): length of span in mm (float or int)
            f_y: yield stress of the section material in MPa (float or int)
            load: Type of load in member ('Normal') ('Destabilizing')


        Returns:
            Effective length (float)

        Reference: Table 15 Cl 8.3.1, IS 800:2007

        """
        if load == KEY_DISP_LOAD1:
            if Torsional == Torsion_Restraint1:
                if Warping == Warping_Restraint1 :
                    length = 0.80 * length
                elif Warping == Warping_Restraint2 :
                    length = 0.75 * length
                # elif Warping ==Warping_Restraint1 :
                #     length = 0.80 * length
                elif Warping ==Warping_Restraint4 :
                    length = 0.85 * length
                elif Warping ==Warping_Restraint5 :
                    length = 1.00 * length
            elif Torsional == Torsion_Restraint2 and Warping == Warping_Restraint5 :
                length = length + 2* depth /1000
            elif Torsional == Torsion_Restraint3 and Warping == Warping_Restraint5 :
                length = 1.2 * length + 2 *depth /1000
        elif load == KEY_DISP_LOAD2:
            if Torsional == Torsion_Restraint1:
                if Warping ==Warping_Restraint1 :
                    length = 0.85 * length
                if Warping ==Warping_Restraint2 :
                    length = 0.9 * length
                if Warping ==Warping_Restraint1 :
                    length = 0.95 * length
                if Warping ==Warping_Restraint4 :
                    length = 1.00 * length
                if Warping ==Warping_Restraint5 :
                    length = 1.20 * length
            elif Torsional == Torsion_Restraint2 and Warping == Warping_Restraint5 :
                length = 1.2 *length + 2* depth /1000
            elif Torsional == Torsion_Restraint3 and Warping == Warping_Restraint5 :
                length = 1.4 * length + 2 *depth /1000
        return length

    @staticmethod
    def cl_8_3_3_EffLen_Cantilever(Support, Top, length, load) -> float:
        """ Calculate the Effective Length for Simply Supported Beams as per Table 16 Cl 8.3.3

        Args:
            Support Restraint: Type of Restraint (string)
            Warping Restraint: Type of Restraint (string)
            depth(d): depth of the element in mm (float or int)
            length(l): length of span in mm (float or int)
            f_y: yield stress of the section material in MPa (float or int)
            load: Type of load in member ('Normal') ('Destabilizing')


        Returns:
            Effective length (float)

        Reference: Table 15 Cl 8.3.1, IS 800:2007

        """
        if load == KEY_DISP_LOAD1:
            if Support == Support1:
                if Top == Top1:
                    length = 3.00 * length
                if Top == Top2:
                    length = 2.7 * length
                if Top == Top3:
                    length = 2.40 * length
                if Top == Top4:
                    length = 2.1 * length

            elif Support == Support2:
                if Top == Top1:
                    length = 2.00 * length
                if Top == Top2:
                    length = 1.8 * length
                if Top == Top3:
                    length = 1.60 * length
                if Top == Top4:
                    length = 1.4 * length


            elif Support == Support3:

                if Top == Top1:
                    length = 1.00 * length

                if Top == Top2:
                    length = 0.9 * length

                if Top == Top3:
                    length = 0.80 * length

                if Top == Top4:
                    length = 0.7 * length

            elif Support == Support4:
                if Top == Top1:
                    length = 0.80 * length
                if Top == Top2:
                    length = 0.7 * length
                if Top == Top3:
                    length = 0.6 * length
                if Top == Top4:
                    length = 0.5 * length
        elif load == KEY_DISP_LOAD2:
            if Support == Support1:
                if Top == Top1:
                    length = 7.50 * length
                if Top == Top2:
                    length = 7.5 * length
                if Top == Top3:
                    length = 4.50 * length
                if Top == Top4:
                    length = 3.6 * length

            elif Support == Support2:
                if Top == Top1:
                    length = 5.00 * length
                if Top == Top2:
                    length = 5 * length
                if Top == Top3:
                    length = 3.0 * length
                if Top == Top4:
                    length = 2.4 * length


            elif Support == Support3:

                if Top == Top1:
                    length = 2.50 * length

                if Top == Top2:
                    length = 2.5 * length

                if Top == Top3:
                    length = 1.50 * length

                if Top == Top4:
                    length = 1.2 * length

            elif Support == Support4:
                if Top == Top1:
                    length = 1.40 * length
                if Top == Top2:
                    length = 1.4 * length
                if Top == Top3:
                    length = 0.6 * length
                if Top == Top4:
                    length = 0.5 * length
        return length
    # cl. 8.4.1 shear strength of bolted connections
    @staticmethod
    def cl_8_4_design_shear_strength(A_vg, f_y):
        """ Calculate the design shear strength in yielding as per cl. 8.4

        Args:
             A_vg: Gross area of the component in square mm (float)
             f_y: Yield stress of the component material in MPa (float)

        Returns:
             Design shear strength in yielding of the component in N

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        V_d = ((A_vg * f_y) / (math.sqrt(3) * gamma_m0))  # N

        return V_d

    # cl 8.2.1.2 design bending strength of the cross-section
    @staticmethod
    def cl_8_2_1_2_design_moment_strength(Z_e, Z_p, f_y, section_class=''):
        """ Calculate the design bending strength as per cl. 8.2.1.2
        Args:
            Z_e: Elastic section modulus of the cross-section in cubic mm (float)
            Z_p: Plastic section modulus of the cross-section in cubic mm (float)
            f_y: Yield stress of the component material in MPa (float)
            section_class: Classification of the section (plastic, compact or semi-compact) as per Table 2 (str)
        Returns:
            Design bending strength of the cross-section in N-mm (float)
        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

        if section_class == 'semi-compact':
            M_d = (Z_e * f_y) / gamma_m0  # N-mm
        else:  # 'compact'
            M_d = (1.0 * Z_p * f_y) / gamma_m0  # N-mm

        return M_d

    @staticmethod
    def cl_8_4_2_1_web_buckling_stiff(d, tw, e,type = 1, kv = None):
        '''nominal shear strength, Vn,of webs with or without
        intermediate stiffeners as governed by buckling

        Author: Rutvik Joshi    '''
        d_tw = d / tw
        if type == 1 and d_tw <= 67 * e:
            return False
        elif type == 2 and d_tw <= 67 * e * math.sqrt(kv/5.35):
            return False
        return True

    # @staticmethod
    # def cl_8_4_2_2_ShearBuckling_Simple_postcritical(d, tw,c,mu,fyw,A_v,support):
    #     '''based on the shear
    #         buckling strength can be used for webs of Isection
    #         girders, with or without intermediate
    #         transverse stiffener, provided that the web has
    #         transverse stiffeners at the supports.
    #
    #     Author: Rutvik Joshi    '''

    @staticmethod
    def cl_8_4_2_2_K_v_Simple_postcritical(support, c = 0, d = 1):

        if support == 'only support':
            K_v = 5.35
        else:
            if c/d < 1:
                K_v = 4 + 5.35/(c/d)**2
            else:
                K_v = 5.35 + 4/(c/d)**2
        return K_v

    @staticmethod
    def cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E,mu, d, tw):
        print('K_v',K_v,'\n E',E,'\nmu',mu,' d',d,' tw',tw)
        tau_crc = (K_v * math.pi**2 * E)/(12*(1-mu**2)*(d/tw)**2)

        return tau_crc

    @staticmethod
    def cl_8_4_2_2_lambda_w_Simple_postcritical(fyw, tau_crc):
        print('fyw',fyw,'\n tau_crc',tau_crc)

        lambda_w = math.sqrt(fyw/(math.sqrt(3) * tau_crc))

        return lambda_w

    @staticmethod
    def cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fyw):
        print('fyw',fyw,' lambda_w',lambda_w)
        if lambda_w <= 0.8:
            tau_b = fyw / math.sqrt(3)
        elif lambda_w < 1.2 and lambda_w > 0.8:
            tau_b = (1 - 0.8*(lambda_w - 0.8)) * fyw / math.sqrt(3)
        elif lambda_w >= 1.2:
            tau_b = fyw / (math.sqrt(3) * lambda_w ** 2)

        return tau_b

    @staticmethod
    def cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_v):
        print('tau_b',tau_b,'\n A_v',A_v)

        V_cr = A_v * tau_b

        return V_cr

    @staticmethod
    def cl_8_4_2_2_Mfr_TensionField(bf, tf, fyf, Nf, gamma_mo):
        '''based on the post-shear buckling
            strength, may be used for webs with
            intermediate transverse stiffeners, in addition
            to the transverse stiffeners at supports, provided
            the panels adjacent to the panel under tension
            field action, or the end posts provide anchorage
            for the tension fields

        Author: Rutvik Joshi    '''

        M_fr = 0.25 * bf * tf ** 2 * fyf * (1 - (Nf / (bf * tf * fyf / gamma_mo)) ** 2)
        print(M_fr, 'M_fr')
        return  M_fr
    @staticmethod
    def cl_8_4_2_2_TensionField( c, d, tw, fyw, bf,tf, fyf,Nf, gamma_mo, A_v,tau_b,V_p):
        '''based on the post-shear buckling
            strength, may be used for webs with
            intermediate transverse stiffeners, in addition
            to the transverse stiffeners at supports, provided
            the panels adjacent to the panel under tension
            field action, or the end posts provide anchorage
            for the tension fields

        Author: Rutvik Joshi    '''

        phi = math.atan(d/c) * 180/math.pi
        M_fr = 0.25 * bf * tf**2 * fyf*(1-(Nf/(bf * tf * fyf / gamma_mo))**2)
        print('phi',phi,'\n Nf',Nf,M_fr,'M_fr',phi*math.pi/180)
        s = 2 * math.sqrt(M_fr / (fyw * tw)) / math.sin(phi*math.pi/180)
        if s <= c:
            pass
        else:
            s == c
        w_tf = d * math.cos(phi*math.pi/180) + (c-2*s)*math.sin(phi*math.pi/180)
        sai = 1.5 * tau_b * math.sin(2*phi*math.pi/180)
        fv = math.sqrt(fyw**2 - 3 * tau_b**2 + sai**2) - sai
        V_tf = A_v * tau_b + 0.9 * w_tf * tw * fv * math.sin(phi*math.pi/180)/ 10 ** 3
        if V_tf <= V_p:
            pass
        else:
            V_tf == V_p
            print('phi',phi,'\n M_fr',M_fr,'\n s',s, '\n c',c, '\n w_tf', w_tf, '\n sai',sai,'\n fv',fv,'\n V_tf',V_tf,'\n V_p',V_p)
        return phi,M_fr,s, w_tf,sai,fv,V_tf

    @staticmethod
    def cl_8_5_1_EndPanel(c, d, tw, fyw, bf, tf, fyf, Nf, gamma_mo, A_v, tau_b, V_p):
        '''The design of end panels in girders in which the interior
        panel (panel A) is designed using tension field action
        shall be carried in accordance with the provisions given
        herein.
        only simple post critical method design
        Author: Rutvik Joshi    '''

        phi = math.atan(d / c) * 180 / math.pi
        M_fr = 0.25 * bf * tf ** 3 * fyf * (1 - (Nf / (bf * tf * fyf / gamma_mo)) ** 2)
        print('phi', phi, '\n Nf', Nf, M_fr, 'M_fr', phi * math.pi / 180)
        s = 2 * math.sqrt(M_fr / (fyw * tw)) / math.sin(phi * math.pi / 180)
        if s <= c:
            pass
        else:
            s == c
        w_tf = d * math.cos(phi * math.pi / 180) + (c - 2 * s) * math.sin(phi * math.pi / 180)
        sai = 1.5 * tau_b * math.sin(2 * phi * math.pi / 180)
        fv = math.sqrt(fyw ** 2 - 3 * tau_b ** 2 + sai ** 2) - sai
        V_tf = A_v * tau_b + 0.9 * w_tf * tw * fv * math.sin(phi * math.pi / 180) / 10 ** 3
        if V_tf <= V_p:
            pass
        else:
            V_tf == V_p
        return phi, M_fr, s, w_tf, sai, fv, V_tf
    # ==========================================================================
    """    SECTION  9     MEMBER SUBJECTED TO COMBINED FORCES   """

    @staticmethod
    def cl_9_2_2_high_shear_moment(Md, Mfd, b, Ze, fy, gamma_mo):
        Mdv=Md - b(Md-Mfd)
        if Mdv <= 1.2*Ze*fy/gamma_mo:
            return Mdv
        else:
            print('Reduced elastic buckling moment error')
            return 0
    # ==========================================================================
    """   SECTION  10    CONNECTIONS    """

    # -------------------------------------------------------------
    #   10.1 General
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.2 Location Details of Fasteners
    # -------------------------------------------------------------

    # cl. 10.2.1 Clearances for Holes for Fasteners

    @staticmethod
    def cl_8_7_1_3_stiff_bearing_length(shear_force, web_thickness, flange_thickness, root_radius, fy):
        #     This function returns the stiff bearing length, b1 for web local yielding and web crippling check
        #     Minimum value of b1 is not defined in IS 800, reference has been made to AISC for such cases (CL. J10-2)
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']
        bearing_length = round((float(shear_force) * 1000) * gamma_m0 / web_thickness / fy, 3)
        b1_req = bearing_length - (flange_thickness + root_radius)
        k = flange_thickness + root_radius
        b1 = max(b1_req, k)
        return b1

    # ==========================================================================
    """    SECTION  9     MEMBER SUBJECTED TO COMBINED FORCES   """
    # ==========================================================================
    """   SECTION  10    CONNECTIONS    """

    # -------------------------------------------------------------
    #   10.1 General
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.2 Location Details of Fasteners
    # -------------------------------------------------------------

    # cl. 10.2.1 Clearances for Holes for Fasteners
    @staticmethod
    def cl_10_2_1_bolt_hole_size(d, bolt_hole_type='Standard'):
        """Calculate bolt hole diameter as per Table 19 of IS 800:2007
        Args:
             d - Nominal diameter of fastener in mm (float)
             bolt_hole_type - Either 'Standard' or 'Over-sized' or 'short_slot' or 'long_slot' (str)
        Returns:
            bolt_hole_size -  Diameter of the bolt hole in mm (float)
        Note:
            Reference:
            IS 800, Table 19 (Cl 10.2.1)
        TODO:ADD KEY_DISP for for Standard/oversize etc and replace these strings
        """
        table_19 = {
            "12-14": {'Standard': 1.0, 'Over-sized': 3.0, 'short_slot': 4.0, 'long_slot': 2.5},
            "16-22": {'Standard': 2.0, 'Over-sized': 4.0, 'short_slot': 6.0, 'long_slot': 2.5},
            "24": {'Standard': 2.0, 'Over-sized': 6.0, 'short_slot': 8.0, 'long_slot': 2.5},
            "24+": {'Standard': 3.0, 'Over-sized': 8.0, 'short_slot': 10.0, 'long_slot': 2.5}
        }
        import re
        # d = str(re.sub("[^0-9]", "", str(d)))
        d = int(d)

        if d < 12:
            clearance = 0
        elif d <= 14:
            clearance = table_19["12-14"][bolt_hole_type]
        elif d <= 22:
            clearance = table_19["16-22"][bolt_hole_type]
        elif d <= 24:
            clearance = table_19["24"][bolt_hole_type]
        else:
            clearance = table_19["24+"][bolt_hole_type]
        if bolt_hole_type == 'long_slot':
            bolt_hole_size = (clearance + 1) * d
        else:
            bolt_hole_size = clearance + d
        return bolt_hole_size

    # cl. 10.2.2 Minimum Spacing
    @staticmethod
    def cl_10_2_2_min_spacing(d):
        """Calculate minimum distance between centre of fasteners
        Args:
             d - Nominal diameter of fastener in mm (float)
        Returns:
            Minimum distance between centre of fasteners in mm (float)
        Note:
            Reference:
            IS 800:2007, cl. 10.2.2
        """
        return 2.5 * d

    # cl. 10.2.3.1 Maximum Spacing
    @staticmethod
    def cl_10_2_3_1_max_spacing(plate_thicknesses):
        """Calculate maximum distance between centre of fasteners
        Args:
             plate_thicknesses- List of thicknesses in mm of connected plates (list or tuple)
        Returns:
            Maximum distance between centres of adjacent fasteners in mm (float)
        Note:
            Reference:
            IS 800:2007, cl. 10.2.3.1
        """
        # print(plate_thicknesses)
        t = min(plate_thicknesses)
        return min(32 * t, 300.0)

    # cl. 10.2.3.2 Maximum pitch in tension and compression members
    @staticmethod
    def cl_10_2_3_2_max_pitch_tension_compression(d, plate_thicknesses, member_type):
        """Calculate maximum pitch between centre of fasteners lying in the direction of stress
        Args:
             d - Nominal diameter of fastener in mm (float)
             plate_thicknesses - List of thicknesses in mm of connected plates (list or tuple)
             member_type - Either 'tension' or 'compression' or 'compression_butting' (str)
        Returns:
            Maximum distance between centres of adjacent fasteners in mm (float)
        Note:
            Reference:
            IS 800:2007, cl. 10.2.3.2
        """
        t = min(plate_thicknesses)
        if member_type == 'tension':
            return min(16 * t, 200.0)
        elif member_type == 'compression':
            return min(12 * t, 200.0)
        else:
            # TODO compression members wherein forces are transferred through butting faces is given in else
            return 4.5 * d

    # cl. 10.2.4.2  Minimum Edge and End Distances
    @staticmethod
    def cl_10_2_4_2_min_edge_end_dist(d, bolt_hole_type='Standard', edge_type='Sheared or hand flame cut'):
        """Calculate minimum end and edge distance
        Args:
             d - Nominal diameter of fastener in mm (float)
             edge_type - Either 'hand_flame_cut' or 'machine_flame_cut' (str)
        Returns:
                Minimum edge and end distances from the centre of any hole to the nearest edge of a plate in mm (float)
        Note:
            Reference:
            IS 800:2007, cl. 10.2.4.2
        """

        d_0 = IS800_2007.cl_10_2_1_bolt_hole_size(d, bolt_hole_type)
        if edge_type == 'Sheared or hand flame cut':
            return 1.7 * d_0
        else:
            # TODO : bolt_hole_type == 'machine_flame_cut' is given in else
            return 1.5 * d_0

    # cl. 10.2.4.3  Maximum Edge Distance
    @staticmethod
    def cl_10_2_4_3_max_edge_dist(conn_plates_t_fu_fy, corrosive_influences=False):
        """Calculate maximum end and edge distance
        Args:
             conn_plates_t_fu_fy - List of tuples with plate thicknesses in mm, fu in MPa, fy in MPa (list of tuples)
                                example:- [ (12, 410, 250), (10, 440, 300) ]
             corrosive_influences - Whether the members are exposed to corrosive influences or not (Boolean)
        Returns:
            Maximum edge distance to the nearest line of fasteners from an edge of any un-stiffened part in mm (float)
        Note:
            Reference:
            IS 800:2007, cl. 10.2.4.3
        """
        # TODO : Differentiate outer plates and connected plates.
        t_epsilon_considered = conn_plates_t_fu_fy[0][0] * math.sqrt(250 / float(conn_plates_t_fu_fy[0][2]))
        t_considered = conn_plates_t_fu_fy[0][0]
        t_min = t_considered
        for i in conn_plates_t_fu_fy:
            t = i[0]
            f_y = i[2]
            if f_y > 0:
                epsilon = math.sqrt(250 / f_y)
                if t * epsilon <= t_epsilon_considered:
                    t_epsilon_considered = t * epsilon
                    t_considered = t
                if t < t_min:
                    t_min = t

         # epsilon = math.sqrt(250 / f_y)

        if corrosive_influences is True:
            return 40.0 + (4 * t_min)
        else:
            return 12 * t_epsilon_considered

    # -------------------------------------------------------------
    #   10.3 Bearing Type Bolts
    # -------------------------------------------------------------

    # cl. 10.3.2 Design strength of bearing type bolt
    @staticmethod
    def cl_10_3_2_bolt_design_strength(V_dsb, V_dpb):
        """Calculate design strength of bearing type bolt
        Args:
            V_dsb - Design shear strength of bearing bolt in N (float)
            V_dpb - Design bearing strength of bolt on the plate in N (float)
        Returns:
            V_db - Design strength of bearing bolt in N (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.3.2
        """
        V_db = min(V_dsb, V_dpb)
        return V_db

    # cl. 10.3.3 Shear Capacity of Bearing Bolt

    @staticmethod
    def cl_10_3_3_bolt_shear_capacity(f_ub, A_nb, A_sb, n_n, n_s=0, safety_factor_parameter=None):
        """Calculate design shear strength of bearing bolt
        Args:
            f_ub - Ultimate tensile strength of the bolt in MPa (float)
            A_nb - Net shear area of the bolt at threads in sq. mm  (float)
            A_sb - Nominal plain shank area of the bolt in sq. mm  (float)
            n_n - Number of shear planes with threads intercepting the shear plane (int)
            n_s -  Number of shear planes without threads intercepting the shear plane (int)
            safety_factor_parameter - Either 'field' or 'shop' (str)
        return:
            V_dsb - Design shear strength of bearing bolt in N (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.3.3
        """
        V_nsb = f_ub / math.sqrt(3) * (n_n * A_nb + n_s * A_sb)
        gamma_mb = IS800_2007.cl_5_4_1_Table_5['gamma_mb'][KEY_DP_FAB_SHOP]
        V_dsb = V_nsb / gamma_mb
        return V_dsb

    # cl. 10.3.3.1 Long joints
    @staticmethod
    def cl_10_3_3_1_bolt_long_joint(d, l_j):
        """ Calculate reduction factor for long joints.
        Args:
            l_j = Length of joint of a splice or end connection as defined in cl. 10.3.3.1 (float)
            d = Nominal diameter of the fastener (float)
        Return:
            beta_lj  = Reduction factor for long joints (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.3.3.1
        """
        beta_lj = 1.075 - 0.005 * l_j / d
        if beta_lj <= 0.75:
            beta_lj = 0.75
        elif beta_lj >= 1.0:
            beta_lj = 1.0
        if l_j >= 15.0 * d:
            return beta_lj
        else:
            return 1.0

    # 10.3.3.2 Large grip lengths
    @staticmethod
    def cl_10_3_3_2_bolt_large_grip(d, l_g, l_j=0.0):
        """ Calculate reduction factor for large grip lengths.
        Args:
            l_g = Grip length equal to the total thickness of the connected plates as defined in cl. 10.3.3.2 (float)
            d = Nominal diameter of the fastener (float)
        Return:
            beta_lg = Reduction factor for large grip lengths (float) if applicable
        Note:
            Reference:
            IS 800:2007,  cl 10.3.3.2
        """
        beta_lg = 8.0 / (3.0 + l_g / d)
        if l_j != 0.0:
            if beta_lg >= IS800_2007.cl_10_3_3_1_bolt_long_joint(d, l_j):
                beta_lg = IS800_2007.cl_10_3_3_1_bolt_long_joint(d, l_j)
        else:
            pass
        if l_g <= 5.0 * d:
            beta_lg = 1.0
        # TODO: Check the maximum limit of 8d in each individual modules
        # elif l_g > 8.0 * d:
        #     return "GRIP LENGTH TOO LARGE"
        return round(beta_lg,2)

    # 10.3.3.3 Packing Plates
    @staticmethod
    def cl_10_3_3_3_packing_plates(t=0.0):
        """ Calculate reduction factor for packing plates.
        Args:
            t = thickness of the thickest packing plate, in mm
        Return:
            beta_pk = Reduction factor for packing plates (float) if applicable
        Note:
            Reference:
            IS 800:2007,  cl 10.3.3.3
        """
        if t > 6.0:
            beta_pk = (1.0 - 0.0125 * t)
        else:
            beta_pk = 1.0
        return beta_pk

    # cl. 10.3.4 Bearing Capacity of the Bolt
    @staticmethod
    def cl_10_3_4_bolt_bearing_capacity(f_u, f_ub, t, d, e, p, bolt_hole_type='Standard',
                                        safety_factor_parameter=KEY_DP_FAB_FIELD):

        """Calculate design bearing strength of a bolt on any plate.
        Args:
            f_u     - Ultimate tensile strength of the plate in MPa (float)
            f_ub    - Ultimate tensile strength of the bolt in MPa (float)
            t       - Summation of thicknesses of the connected plates in mm as defined in cl. 10.3.4 (float)
            d       - Diameter of the bolt in mm (float)
            e       - End distance of the fastener along bearing direction in mm (float)
            p       - Pitch distance of the fastener along bearing direction in mm (float)
            bolt_hole_type - Either 'Standard' or 'Over-sized' or 'short_slot' or 'long_slot' (str)
            safety_factor_parameter - Either 'Field' or 'Shop' (str)
        return:
            V_dpb - Design bearing strength of bearing bolt in N (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.3.4
        """
        d_0 = IS800_2007.cl_10_2_1_bolt_hole_size(d, bolt_hole_type)

        if p > 0.0:
            k_b = min(e / (3.0 * d_0), p / (3.0 * d_0) - 0.25, f_ub / f_u, 1.0)
        else:
            k_b = min(e / (3.0 * d_0), f_ub / f_u, 1.0)  # calculate k_b when there is no pitch (p = 0)

        k_b = round(k_b, 2)
        V_npb = 2.5 * k_b * d * t * f_u
        gamma_mb = IS800_2007.cl_5_4_1_Table_5['gamma_mb'][safety_factor_parameter]
        V_dpb = V_npb / gamma_mb

        if bolt_hole_type == 'Over-sized' or bolt_hole_type == 'short_slot':
            V_dpb *= 0.7
        elif bolt_hole_type == 'long_slot':
            V_dpb *= 0.5

        return V_dpb

    @staticmethod
    def cl_10_3_5_bearing_bolt_tension_resistance(f_ub, f_yb, A_sb, A_n, safety_factor_parameter=KEY_DP_FAB_FIELD):
        """Calculate design tensile strength of bearing bolt
        Args:
            f_ub - Ultimate tensile strength of the bolt in MPa (float)
            f_yb - Yield strength of the bolt in MPa (float)
            A_sb - Shank area of bolt in sq. mm  (float)
            A_n - Net tensile stress area of the bolts as per IS 1367 in sq. mm  (float)
        return:
            T_db - Design tensile strength of bearing bolt in N (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.3.5
        """
        gamma_mb = IS800_2007.cl_5_4_1_Table_5['gamma_mb'][safety_factor_parameter]
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']
        T_nb = min(0.90 * f_ub * A_n, f_yb * A_sb * gamma_mb / gamma_m0)
        return T_nb / gamma_mb

        # cl. 10.3.6 Bolt subjected to combined shear and tension of bearing bolts

    @staticmethod
    def cl_10_3_6_bearing_bolt_combined_shear_and_tension(V_sb, V_db, T_b, T_db):
        """Check for bolt subjected to combined shear and tension
        Args:
            V_sb - factored shear force acting on the bolt,
            V_db - design shear capacity,
            T_b - factored tensile force acting on the bolt,
            T_db - design tension capacity.
        return: combined shear and friction value
        Note:
            Reference:
            IS 800:2007,  cl 10.3.6
        """
        return (V_sb / V_db) ** 2 + (T_b / T_db) ** 2

    # -------------------------------------------------------------
    #   10.4 Friction Grip Type Bolting
    # -------------------------------------------------------------

    # cl. 10.4.3 Slip Resistance
    @staticmethod
    def cl_10_4_3_bolt_slip_resistance(f_ub, A_nb, n_e, mu_f, bolt_hole_type='Standard', slip_resistance='ultimate_load'):
        # TODO : Ensure default slip_resistance = 'service_load' or 'ultimate_load'
        """Calculate design shear strength of friction grip bolt as governed by slip
        Args:
            f_ub - Ultimate tensile strength of the bolt in MPa (float)
            A_nb - Net area of the bolt at threads in sq. mm  (float)
            n_e - Number of  effective interfaces offering  frictional resistance to slip (int)
            mu_f - coefficient of friction (slip factor) as specified in Table 20
            bolt_hole_type - Either 'Standard' or 'Over-sized' or 'short_slot' or 'long_slot' (str)
            slip_resistance - whether slip resistance is required at service load or ultimate load
                              Either 'service_load' or 'ultimate_load' (str)
        return:
            V_dsf - Design shear strength of friction grip bolt as governed by slip in N (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.4.3
            AMENDMENT NO. 1 (JANUARY 2012) to IS 800:2007
        """
        f_0 = 0.70 * f_ub
        F_0 = A_nb * f_0
        if slip_resistance == 'service_load':
            gamma_mf = 1.10
        else:
            # TODO : slip _resistance for 'ultimate_load' is given in else
            gamma_mf = 1.25
        if bolt_hole_type == 'Standard':
            K_h = 1.0
        elif bolt_hole_type == 'Over-sized' or bolt_hole_type == 'short_slot' or bolt_hole_type == 'long_slot':
            K_h = 0.85
        else:
            # TODO : long_slot bolt loaded parallel to slot is given in else
            K_h = 0.7
        if mu_f >= 0.55:
            mu_f = 0.55
        V_nsf = mu_f * n_e * K_h * F_0
        V_dsf = V_nsf / gamma_mf
        return V_dsf, K_h, gamma_mf

    # Table 20 Typical Average Values for Coefficient of Friction, mu_f (list)
    cl_10_4_3_Table_20 = [0.20, 0.50, 0.10, 0.25, 0.30, 0.52, 0.30, 0.30, 0.50, 0.33, 0.48, 0.1]

    # cl. 10.4.5 Tension Resistance
    @staticmethod
    def cl_10_4_5_friction_bolt_tension_resistance(f_ub, f_yb, A_sb, A_n,
                                                   safety_factor_parameter=KEY_DP_FAB_FIELD):
        """Calculate design tensile strength of friction grip bolt
        Args:
            f_ub - Ultimate tensile strength of the bolt in MPa (float)
            f_yb - Yield strength of the bolt in MPa (float)
            A_sb - Shank area of bolt in sq. mm  (float)
            A_n - Net tensile stress area of the bolts as per IS 1367 in sq. mm  (float)
        return:
            T_df - Design tensile strength of friction grip bolt in N (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.4.5
            AMENDMENT NO. 1 (JANUARY 2012) to IS 800:2007
        """
        gamma_mf = IS800_2007.cl_5_4_1_Table_5['gamma_mf'][safety_factor_parameter]
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5['gamma_m1']['ultimate_stress']

        T_nf = min(0.9 * f_ub * A_n, f_yb * A_sb * gamma_m1 / gamma_m0)
        return T_nf / gamma_mf

    # cl. 10.4.6 Combined shear and Tension for friction grip bolts
    @staticmethod
    def cl_10_4_6_friction_bolt_combined_shear_and_tension(V_sf, V_df, T_f, T_df):
        """Calculate combined shear and tension of friction grip bolt
                Args:
                   V_sf - applied factored shear at design load
                   V_df - design shear strength
                   T_f - externally applied factored tension at design load
                   T_df - design tension strength
                return:
                    combined shear and friction value
                Note:
                    Reference:
                    IS 800:2007,  cl 10.4.6
        """
        return (V_sf / V_df) ** 2 + (T_f / T_df) ** 2

    @staticmethod
    def cl_10_4_7_bolt_prying_force(T_e, l_v, f_o, b_e, t, f_y, end_dist, pre_tensioned='', eta=1.5):
        """Calculate prying force of friction grip bolt
                       Args:
                          2 * T_e - Force in 2 bolts on either sides of the web/plate
                          l_v - distance from the bolt centre line to the toe of the fillet weld or to half
                                the root radius for a rolled section,
                          beta - 2 for non pre-tensioned bolt and 1 for pre-tensioned bolt
                          eta - 1.5
                          b_e - effective width of flange per pair of bolts
                          f_o - proof stress in consistent units
                          t - thickness of the end plate
                       return:
                           Prying force of friction grip bolt
                       Note:
                           Reference:
                           IS 800:2007,  cl 10.4.7
        """
        if pre_tensioned == 'Pre-tensioned':
            beta = 1
        else:
            beta = 2

        le_1 = end_dist
        le_2 = (1.1 * t) * math.sqrt((beta * f_o) / f_y)  # here f_o is taken as N/mm^2
        l_e = min(le_1, le_2)

        # # Note: In the below equation of Q, f_o is taken as kN since the value of T_e is in kN
        # Q = (l_v / (2 * l_e)) * (T_e - ((beta * eta * f_o * b_e * 1e-3 * t ** 4) / (27 * l_e * l_v ** 2)))  # kN

        # All Calculations are in N-mm. Please pass arguments accordingly.
        Q = (l_v / (2 * l_e)) * (T_e - ((beta * eta * f_o * b_e * t ** 4) / (27 * l_e * l_v ** 2)))  # N

        if Q < 0:
            Q = 0.0

        return round(Q, 2)  # N

    # -------------------------------------------------------------
    #   10.5 Welds and Welding
    # -------------------------------------------------------------

    # cl. 10.5.2.3 Minimum Size of First Run or of a Single Run Fillet Weld
    @staticmethod
    def cl_10_5_2_3_min_weld_size(part1_thickness, part2_thickness):
        """Calculate minimum size of fillet weld as per Table 21 of IS 800:2007
        Args:
            part1_thickness - Thickness of either plate element being welded in mm (float)
            part2_thickness - Thickness of other plate element being welded in mm (float)
        Returns:
            min_weld_size - Minimum size of first run or of a single run fillet weld in mm (float)
        Note:
            Reference:
            IS 800, Table 21 (Cl 10.5.2.3) : Minimum Size of First Run or of a Single Run Fillet Weld
        """
        thicker_part_thickness = max(part1_thickness, part2_thickness)
        thinner_part_thickness = min(part1_thickness, part2_thickness)

        if thicker_part_thickness <= 10.0:
            min_weld_size = 3
        elif thicker_part_thickness <= 20.0:
            min_weld_size = 5
        elif thicker_part_thickness <= 32.0:
            min_weld_size = 6
        else:  # thicker_part_thickness <= 50.0:
            min_weld_size = 10
        # TODO else:
        if min_weld_size > thinner_part_thickness:
            min_weld_size = thinner_part_thickness
        return min_weld_size

    @staticmethod
    def cl_10_5_3_1_max_weld_throat_thickness(part1_thickness, part2_thickness, special_circumstance=False):

        """Calculate maximum effective throat thickness of fillet weld
        Args:
            part1_thickness - Thickness of either plate element being welded in mm (float)
            part2_thickness - Thickness of other plate element being welded in mm (float)
            special_circumstance - (Boolean)
        Returns:
            maximum effective throat thickness of fillet weld in mm (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.5.3.1
        """

        if special_circumstance is True:
            return min(part1_thickness, part2_thickness)
        else:
            return 0.7 * min(part1_thickness, part2_thickness)

    @staticmethod
    def cl_10_5_3_2_factor_for_throat_thickness(fusion_face_angle=90):

        table_22 = {'60-90': 0.70, '91-100': 0.65, '101-106': 0.60, '107-113': 0.55, '114-120': 0.50}
        fusion_face_angle = int(round(fusion_face_angle))
        if 60 <= fusion_face_angle <= 90:
            K = table_22['60-90']
        elif 91 <= fusion_face_angle <= 100:
            K = table_22['91-100']
        elif 101 <= fusion_face_angle <= 106:
            K = table_22['101-106']
        elif 107 <= fusion_face_angle <= 113:
            K = table_22['107-113']
        elif 114 <= fusion_face_angle <= 120:
            K = table_22['114-120']
        else:
            K = "NOT DEFINED"
        try:
            K = float(K)
        except ValueError:
            return

        return K


    @staticmethod
    def cl_10_5_3_2_fillet_weld_effective_throat_thickness(fillet_size, fusion_face_angle=90):

        """Calculate effective throat thickness of fillet weld for stress calculation
        Args:
            fillet_size - Size of fillet weld in mm (float)
            fusion_face_angle - Angle between fusion faces in degrees (int)
        Returns:
            Effective throat thickness of fillet weld for stress calculation in mm (float)
        Note:
            Reference:

            IS 800:2007,  cl 10.5.3.2

        """
        K = IS800_2007.cl_10_5_3_2_factor_for_throat_thickness(fusion_face_angle)

        throat = max(round((K * fillet_size),2), 3)

        return throat

    @staticmethod
    def cl_10_5_3_2_fillet_weld_effective_throat_thickness_constant(fusion_face_angle=90):

        """Calculate effective throat thickness of fillet weld for stress calculation

        Args:
            fusion_face_angle - Angle between fusion faces in degrees (int)

        Returns:
            Effective throat thickness of fillet weld constant

        Note:
            Reference:
            IS 800:2007,  cl 10.5.3.2zzz

        """
        table_22 = {'60-90': 0.70, '91-100': 0.65, '101-106': 0.60, '107-113': 0.55, '114-120': 0.50}
        fusion_face_angle = int(round(fusion_face_angle))
        if 60 <= fusion_face_angle <= 90:
            K = table_22['60-90']
        elif 91 <= fusion_face_angle <= 100:
            K = table_22['91-100']
        elif 101 <= fusion_face_angle <= 106:
            K = table_22['101-106']
        elif 107 <= fusion_face_angle <= 113:
            K = table_22['107-113']
        elif 114 <= fusion_face_angle <= 120:
            K = table_22['114-120']
        else:
            K = "NOT DEFINED"
        try:
            K = float(K)
        except ValueError:
            return

        return K

        # Cl. 10.5.3.3 Effective throat size of groove (butt) welds

    @staticmethod
    def cl_10_5_3_3_groove_weld_effective_throat_thickness(*args):

        """Calculate effective throat thickness of complete penetration butt welds
        *args:
            Thicknesses of each plate element being welded in mm (tuple of float)
        Returns:
            Effective throat thickness of CJP butt weld in mm (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.5.3.3
        """
        return min(*args)

    @staticmethod
    def cl_10_5_4_1_fillet_weld_effective_length(fillet_size, available_length):

        """Calculate effective length of fillet weld from available length to weld in practice
        Args:
            #fillet_size - Size of fillet weld in mm (float)
            available_length - Available length in mm to weld the plates in practice (float)
        Returns:
            Effective length of fillet weld in mm (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.5.4.1
        """
        if available_length <= 4 * fillet_size:
            effective_length = 0
        else:
            effective_length = available_length - 2 * fillet_size
        return effective_length

    # cl. 10.5.7.1.1 Design stresses in fillet welds
    @staticmethod
    def cl_10_5_7_1_1_fillet_weld_design_stress(ultimate_stresses, fabrication=KEY_DP_FAB_SHOP):

        """Calculate the design strength of fillet weld
        Args:
            ultimate_stresses - Ultimate stresses of weld and parent metal in MPa (list or tuple)
            fabrication - Either 'shop' or 'field' (str)
        Returns:
            Design strength of fillet weld in MPa (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.5.7.1.1
        """
        f_u = min(ultimate_stresses)
        f_wn = (f_u / math.sqrt(3))
        gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][fabrication]
        f_wd = f_wn / gamma_mw
        return f_wd

    # cl. 10.5.7.3 Long joints
    @staticmethod
    def cl_10_5_7_3_weld_long_joint(l_j, t_t):

        """Calculate the reduction factor for long joints in welds
        Args:
            l_j - length of joints in the direction of force transfer in mm (float)
            t_t - throat size of the weld in mm (float)
        Returns:
             Reduction factor, beta_lw for long joints in welds (float)
        Note:
            Reference:
            IS 800:2007,  cl 10.5.7.3
        """
        if l_j <= 150 * t_t:
            return 1.0
        beta_lw = 1.2 - ((0.2 * l_j) / (150 * t_t))
        if beta_lw >= 1.0:
            beta_lw = 1.0
        elif beta_lw <= 0.6:
            beta_lw = 0.6
        return beta_lw


    # -------------------------------------------------------------
    #   10.6 Design of Connections
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.7 Minimum Design Action on Connection
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.8 Intersections
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.9 Choice of Fasteners
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.10 Connection Components
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.11 Analysis of a Bolt/Weld Group
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.12 Lug Angles
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # ==========================================================================
    """    SECTION  11    WORKING STRESS DESIGN   """
    # ==========================================================================
    """    SECTION  12    DESIGN AND DETAILING FOR EARTHQUAKE   """
    # ==========================================================================
    """    SECTION  13    FATIGUE   """
    # ==========================================================================
    """    SECTION  14    DESIGN ASSISTED BY TESTING   """
    # ==========================================================================
    """    SECTION  15    DURABILITY   """
    # ==========================================================================
    """    SECTION  16    FIRE RESISTANCE   """
    # ==========================================================================
    """    SECTION  17    FABRICATION AND ERECTION   """
    # ==========================================================================
    """    ANNEX  A       LIST OF REFERRED INDIAN STANDARDS   """
    # ==========================================================================
    """    ANNEX  B       ANALYSIS AND DESIGN METHODS   """
    # ==========================================================================
    """    ANNEX  C       DESIGN AGAINST FLOOR VIBRATION   """
    # ==========================================================================
    """    ANNEX  D       DETERMINATION OF EFFECTIVE LENGTH OF COLUMNS   """
    # ==========================================================================
    """    ANNEX  E       ELASTIC LATERAL TORSIONAL BUCKLING   """
    # ==========================================================================
    """    ANNEX  F       CONNECTIONS   """
    # ==========================================================================
    """    ANNEX  G       GENERAL RECOMMENDATIONS FOR STEELWORK TENDERS AND CONTRACTS   """
    # ==========================================================================
    """    ANNEX  H       PLASTIC PROPERTIES OF BEAMS   """
    # ==========================================================================
    """     ------------------END------------------     """