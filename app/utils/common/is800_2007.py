import math

class IS800_2007(object):
    """Perform calculations on steel design as per IS 800:2007

    """

    # ==========================================================================
    """    SECTION  1     GENERAL   """
    # ==========================================================================
    """    SECTION  2     MATERIALS   """
    # ==========================================================================
    """    SECTION  3     GENERAL DESIGN REQUIREMENTS   """
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
                        "gamma_mf": {'shop': 1.25, 'field': 1.25},
                        "gamma_mb": {'shop': 1.25, 'field': 1.25},
                        "gamma_mr": {'shop': 1.25, 'field': 1.25},
                        "gamma_mw": {'shop': 1.25, 'field': 1.50}
                        }

    # ==========================================================================
    """    SECTION  6     DESIGN OF TENSION MEMBERS   """
    # ==========================================================================
    """    SECTION  7     DESIGN OF COMPRESS1ON MEMBERS   """
    # ==========================================================================
    """    SECTION  8     DESIGN OF MEMBERS SUBJECTED TO BENDING   """
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
    def cl_10_2_1(d, bolt_hole_type='standard'):
        """Calculate bolt hole diameter as per Table 19 of IS 800:2007

        Args:
             d - Nominal diameter of fastener in mm (float)
             bolt_hole_type - Either 'standard' or 'over_size' or 'short_slot' or 'long_slot' (str)

        Returns:
            bolt_hole_size -  Diameter of the bolt hole in mm (float)

        Note:
            Reference:
            IS 800, Table 19 (Cl 10.2.1)

        """
        table_19 = {
            "12-14": {'standard': 1.0, 'over_size': 3.0, 'short_slot': 4.0, 'long_slot': 2.5},
            "16-22": {'standard': 2.0, 'over_size': 4.0, 'short_slot': 6.0, 'long_slot': 2.5},
            "24"   : {'standard': 2.0, 'over_size': 6.0, 'short_slot': 8.0, 'long_slot': 2.5},
            "24+"  : {'standard': 3.0, 'over_size': 8.0, 'short_slot': 10.0, 'long_slot': 2.5}
        }

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
    def cl_10_2_2(d):
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
    def cl_10_2_3_1(plate_thicknesses):
        """Calculate maximum distance between centre of fasteners

        Args:
             plate_thicknesses- List of thicknesses in mm of connected plates (list or tuple)

        Returns:
            Maximum distance between centres of adjacent fasteners in mm (float)

        Note:
            Reference:
            IS 800:2007, cl. 10.2.3.1

        """
        t = min(plate_thicknesses)
        return min(32*t, 300.0)

    # cl. 10.2.3.2 Maximum pitch in tension and compression members
    @staticmethod
    def cl_10_2_3_2(d, plate_thicknesses, member_type):
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
            return min(16*t, 200.0)
        elif member_type == 'compression':
            return min(12*t, 200.0)
        else:
            # TODO compression members wherein forces are transferred through butting faces is given in else
            return 4.5 * d

    # cl. 10.2.4.2  Minimum Edge and End Distances
    @staticmethod
    def cl_10_2_4_2(d, bolt_hole_type='standard', edge_type='hand_flame_cut'):
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

        d_0 = IS800_2007.cl_10_2_1(d, bolt_hole_type)
        if edge_type == 'hand_flame_cut':
            return 1.7 * d_0
        else:
            # TODO : bolt_hole_type == 'machine_flame_cut' is given in else
            return 1.5 * d_0

    # cl. 10.2.4.3  Maximum Edge Distance
    @staticmethod
    def cl_10_2_4_3(plate_thicknesses, f_y, corrosive_influences=False):
        """Calculate maximum end and edge distance

        Args:
             plate_thicknesses - List of thicknesses in mm of outer plates (list or tuple)
             f_y - Yield strength of plate material in MPa (float)
             corrosive_influences - Whether the members are exposed to corrosive influences or not (Boolean)

        Returns:
            Maximum edge distance to the nearest line of fasteners from an edge of any un-stiffened part in mm (float)

        Note:
            Reference:
            IS 800:2007, cl. 10.2.4.3

        """
        # TODO : Differentiate outer plates and connected plates.
        t = min(plate_thicknesses)
        epsilon = math.sqrt(250 / f_y)
        if corrosive_influences is True:
            return 40.0 + 4 * t
        else:
            return 12 * t * epsilon

    # -------------------------------------------------------------
    #   10.3 Bearing Type Bolts
    # -------------------------------------------------------------

    # cl. 10.3.2 Design strength of bearing type bolt
    @staticmethod
    def cl_10_3_2(V_dsb, V_dpb):
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
    def cl_10_3_3(f_u, A_nb, A_sb, n_n, n_s=0, safety_factor_parameter='field'):
        """Calculate design shear strength of bearing bolt

        Args:
            f_u - Ultimate tensile strength of the bolt in MPa (float)
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
        V_nsb = f_u / math.sqrt(3) * (n_n * A_nb + n_s * A_sb)
        gamma_mb = IS800_2007.cl_5_4_1_Table_5['gamma_mb'][safety_factor_parameter]
        V_dsb = V_nsb/gamma_mb
        return V_dsb

    # cl. 10.3.3.1 Long joints
    @staticmethod
    def cl_10_3_3_1(d, l_j):
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
    def cl_10_3_3_2(d, l_g, l_j=0):
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
        if beta_lg >= IS800_2007.cl_10_3_3_1(d, l_j):
            beta_lg = IS800_2007.cl_10_3_3_1(d, l_j)
        if l_g <= 5.0 * d:
            beta_lg = 1
        elif l_g > 8.0 * d:
            return "GRIP LENGTH TOO LARGE"
        return beta_lg

    # cl. 10.3.4 Bearing Capacity of the Bolt
    @staticmethod
    def cl_10_3_4(f_u, f_ub, t, d, e, p, bolt_hole_type='standard', safety_factor_parameter='field'):

        """Calculate design bearing strength of a bolt on any plate.

        Args:
            f_u     - Ultimate tensile strength of the plate in MPa (float)
            f_ub    - Ultimate tensile strength of the bolt in MPa (float)
            t       - Summation of thicknesses of the connected plates in mm as defined in cl. 10.3.4 (float)
            d       - Diameter of the bolt in mm (float)
            e       - End distance of the fastener along bearing direction in mm (float)
            p       - Pitch distance of the fastener along bearing direction in mm (float)
            bolt_hole_type - Either 'standard' or 'over_size' or 'short_slot' or 'long_slot' (str)
            safety_factor_parameter - Either 'field' or 'shop' (str)

        return:
            V_dpb - Design bearing strength of bearing bolt in N (float)

        Note:
            Reference:
            IS 800:2007,  cl 10.3.4

        """
        d_0 = IS800_2007.cl_10_2_1(d, bolt_hole_type)
        k_b = min(e/(3.0*d_0), p/(3.0*d_0)-0.25, f_ub/f_u, 1.0)
        V_npb = 2.5 * k_b * d * t * f_u
        gamma_mb = IS800_2007.cl_5_4_1_Table_5['gamma_mb'][safety_factor_parameter]
        V_dpb = V_npb/gamma_mb
        if bolt_hole_type == 'over_size' or 'short_slot':
            V_dpb *= 0.7
        elif bolt_hole_type == 'long_slot':
            V_dpb *= 0.5
        return V_dpb

    # -------------------------------------------------------------
    #   10.4 Friction Grip Type Bolting
    # -------------------------------------------------------------

    # cl. 10.4.3 Slip Resistance
    @staticmethod
    def cl_10_4_3(f_ub, A_nb, n_e, mu_f, bolt_hole_type='standard', slip_resistance='service_load'):
        #TODO : Ensure default slip_resistance = 'service_load' or ultimate_load'
        """Calculate design shear strength of friction grip bolt as governed by slip

        Args:
            f_ub - Ultimate tensile strength of the bolt in MPa (float)
            A_nb - Net area of the bolt at threads in sq. mm  (float)
            n_e - Number of  effective interfaces offering  frictional resistance to slip (int)
            mu_f - coefficient of friction (slip factor) as specified in Table 20
            bolt_hole_type - Either 'standard' or 'over_size' or 'short_slot' or 'long_slot' (str)
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
        if bolt_hole_type == 'standard':
            K_h = 1.0
        elif bolt_hole_type == 'over_size' or 'short_slot' or 'long_slot':
            K_h = 0.85
        else:
            # TODO : long_slot bolt loaded parallel to slot is given in else
            K_h = 0.7
        if mu_f >= 0.55:
            mu_f = 0.55
        V_nsf = mu_f * n_e * K_h * F_0
        V_dsf = V_nsf / gamma_mf
        return V_dsf

    # Table 20 Typical Average Values for Coefficient of Friction, mu_f (list)
    cl_10_4_3_Table_20 = [0.20, 0.50, 0.10, 0.25, 0.30, 0.52, 0.30, 0.30, 0.50, 0.33, 0.48, 0.1]


    # -------------------------------------------------------------
    #   10.5 Welds and Welding
    # -------------------------------------------------------------

    # cl. 10.5.2.3 Minimum Size of First Run or of a Single Run Fillet Weld
    @staticmethod
    def cl_10_5_2_3(part1_thickness, part2_thickness):
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
        elif thicker_part_thickness <= 50.0:
            min_weld_size = 10
        #TODO else:
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
