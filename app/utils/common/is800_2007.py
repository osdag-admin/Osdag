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

    # Table 5 Partial Safety Factores for Materials, gamma_m
    cl_5_4_1_Table_5 = {"gamma_m0": {'Yielding': 1.10, 'Buckling': 1.10},
                        "gamma_m1": {'Ultimate_stress': 1.25},
                        "gamma_mf": {'Shop': 1.25, 'Field': 1.25},
                        "gamma_mb": {'Shop': 1.25, 'Field': 1.25},
                        "gamma_mr": {'Shop': 1.25, 'Field': 1.25},
                        "gamma_mw": {'Shop': 1.25, 'Field': 1.50}
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
    # -------------------------------------------------------------
    #   10.3 Bearing Type Bolts
    # -------------------------------------------------------------


    @staticmethod
    def cl_10_3_2(Vsb, Vdsb, Vdpb):
        """Determine condition for bolt subjected to shear force

        Args:
            Vsb - Factored shear force in bearing bolt in N (float)
            Vdb - Design strength of bearing bolt in N (float)

        Returns:
            Boolean - True or False

        Note:
            Reference:
            IS 800:2007,  cl 10.3.2
            AMENDMENT NO. 1 (JANUARY 2012) to IS 800:2007

        """
        Vdb = min(Vdsb, Vdpb)
        return Vsb <= Vdb


    @staticmethod
    def cl_10_3_3(fu, Anb, Asb, nn, ns=0, fabrication='Field'):
        #TODO : Add Table 5 and take gamma_mb from there
        """Calculate design shear strength of bearing bolt

        Args:
            fu - Uitimate tensile strength of a bolt in N (float)
            Anb - Net shear area of the bolt at threads in sq. mm  (float)
            Asb - Nominal plain shank area of the bolt in sq. mm  (float)
            nn - Number of shear planes with threads intercepting the shear plane (int)
            ns -  Number of shear planes without threads intercepting the shear plane (int)

        Returns:
            Vdsb - Design shear strength of bearing bolt in N

        Note:
            Reference:
            IS 800:2007,  cl 10.3.3

        """
        Vnsb = fu / math.sqrt(3) * (nn * Anb + ns * Asb)
        gamma_mb = IS800_2007.cl_5_4_1_Table_5['gamma_mb'][fabrication]
        Vdsb = Vnsb/gamma_mb
        return Vdsb

    # -------------------------------------------------------------
    #   10.4 Friction Grip Type Bolting
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    #   10.5 Welds and Welding
    # -------------------------------------------------------------

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

        if thicker_part_thickness <= 10:
            min_weld_size = 3
        elif thicker_part_thickness <= 20:
            min_weld_size = 5
        elif thicker_part_thickness <= 32:
            min_weld_size = 6
        elif thicker_part_thickness <= 50:
            min_weld_size = 10
        #TODO else:
        if min_weld_size > thinner_part_thickness:
            min_weld_size = thinner_part_thickness
        return min_weld_size

    @staticmethod
    def compute_max_weld_thickness(part1_thickness, part2_thickness):
        return min(part1_thickness, part2_thickness)
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
