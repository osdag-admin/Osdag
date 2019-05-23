"""Module for Indian Standard, IS 800 : 2007

Started on 01 - Nov - 2018

@author: ajmalbabums
"""
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
    # -------------------------------------------------------------
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
    # ==========================================================================
    """    SECTION  8     DESIGN OF MEMBERS SUBJECTED TO BENDING   """
    # -------------------------------------------------------------
    #   8.4 Shear
    # -------------------------------------------------------------

    # cl. 8.4.1 shear strength of bolted connections
    @staticmethod
    def cl_8_4_design_shear_strength():
        # TODO
        pass

    # ==========================================================================
    """    SECTION  9     MEMBER SUBJECTED TO COMBINED FORCES   """
    # --------------------------------------------------------------------------
    # cl.9.2 Combined Shear and Bending
    @staticmethod
    def cl_9_2(Md, V, Vd, Mfd, Ze, section_type, fy, gamma_m0):
        """To calculate change in Moment Carrying Capacity due to shear force
        Args:
            Md - plastic design moment of whole section disregarding shear force
                 effect considering web buckling effects
            V - factored applied shear force
            Vd - design shear strength
            Mfd - plastic design strength of c/s excluding shear area considering
                  gamma_m0
            Ze - elastic section modulus
            section_type - 'plastic','compact' or 'semi_compact'
            fy - yeild strength
            gamma_m0 - partial safety factor
        Returns:
            Mdv - Moment Carrying Capacity under action of high shear force

        Note:
            Reference:
                IS 800:2007, cl.9.2
        """
        if (V > 0.6 * Vd):  # cl.9.2.2
            if (section_type == 'plastic' or section_type == 'compact'):
                beta = (2 * V / Vd - 1) ** 2
                Mdv = min(Md - beta * (Md - Mfd), 1.2 * Ze * fy / gamma_m0)
            elif (section_type == 'semi_compact'):
                Mdv = Ze * fy / gamma_m0
            else:
                return 'enter section type in valid format'
        else:
            Mdv = Md  # V < 0.6 * Vd.....cl 9.2.1
        return Mdv

    # cl.9.3.1.1 Combined Axial Force and Bending - Section Strength - Plastic and Compact Sections
    # for this clause there are 2 functions

    # function1
    @staticmethod
    def cl_9_3_1_1(My, Mz, Mndy, Mndz, N, Nd, section_type):
        """Safety check for reduced flexural strength under combined axial force and
        respective uniaxial bending moment acting alone
        Args:
            My - factored applied moments about minor axis of c/s
            Mz - factored applied moments about major axis of c/s
            Mndy - reduced flexural strength along minor axis
            Mndz - reduced flexural strength along major axis
            N - factored applied axial force
            Nd - design strength in compression or tension
            section_type - I/channel,Circular Tubes,Rectangular Tubes,Solid Rectangles
        Returns:
            'OK' - If condition is satisfied
            else 'Warning : Reduced flexural strength does not satisfy cl.9.3.1.1'
        Note:
            Reference:
                IS 800:2007, cl.9.3.1.1
        """
        n = N / Nd
        table_17 = {
            'I and channel': (max(5 * n, 1), 2),
            'Circular tubes': (2, 2),
            'Rectangular tubes': (min(1.66 / (1 - 1.13 * n * n), 6), min(1.66 / (1 - 1.13 * n * n), 6)),
            'Solid rectangles': (1.73 + 1.8 * n ** 3, 1.73 + 1.8 * n ** 3)
        }
        alpha_1 = table_17[section_type][0]
        alpha_2 = table_17[section_type][1]

        if (((My / Mndy) ** alpha_1 + (Mz / Mndz) ** alpha_2) <= 1):
            return 'OK'
        else:
            return 'Warning : Reduced flexural strength not sufficient cl.9.3.1.1'

    # function 2
    @staticmethod
    def cl_9_3_1_1_cons(My, Mz, Mdy, Mdz, N, Nd):
        """Safety check for reduced flexural strength under combined axial force and
        respective uniaxial bending moment acting alone
        using a more conservative formula
        Args:
            My - factored applied moments about minor axis of c/s
            Mz - factored applied moments about major axis of c/s
            Mndy - reduced flexural strength along minor axis
            Mndz - reduced flexural strength along major axis
            N - factored applied axial force
            Nd - design strength in compression or tension
        Returns:
            'OK' - If condition is satisfied
            else 'Warning : Reduced flexural strength does not satisfy cl.9.3.1.1'
        Note:
            Reference:
                IS 800:2007, cl.9.3.1.1
        """
        if ((N / Nd + My / Mdy + Mz / Mdz) <= 1):
            return 'OK'
        else:
            return 'Warning : Design reduced flexural strength not sufficient cl.9.3.1.1'

    # cl.9.3.1.2 Combined Axial Force and Bending - Approximate Section Strength Calculation- Plastic and Compact Sections
    # without bolt holes
    # 5 functions - 'plates','welded I or H section','standard I or H section','rectangular hollow sections and welded box sections',
    #              'circular hollow tubes'

    # plates
    @staticmethod
    def cl_9_3_1_2_a(Md, N, Nd):
        """Calculates reduced flexural strength for plates
        Args:
            Md - plastic design moment of whole section disregarding axial force
            N - factored applied axial force
            Nd - design strength in compression or tension
        Returns:
            'OK' - If condition is satisfied
            else 'Warning : Reduced flexural strength does not satisfy cl.9.3.1.1'
        Note:
            Reference:
                IS 800:2007, cl.9.3.1.2
        """
        n = N / Nd
        Mnd = Md * (1 - n ** 2)
        return Mnd

    # Welded I or H section
    @staticmethod
    def cl_9_3_1_2_b(Mdy, Mdz, N, Nd, tf, b, A):
        """Calculates reduced flexural strength for Welded I or H sections
        Args:
            Mdy,Mdz - design strength of section along minor and major axes respectively
                      disregarding axial force
            N - factored applied axial force
            Nd - design strength in compression or tension
            tf - thickness of flange
            b - width of flange
            A - area of c/s
        Returns:
            Mndy - reduced flexural strength along minor axis
            Mndz - reduced flexural strength along major axis
        Note:
            Reference:
                IS 800:2007, cl.9.3.1.2
        """
        n = N / Nd
        a = min((A - 2 * b * tf) / A, 0.5)
        if (n < a):
            Mndy = Mdy
        else:
            Mndy = min(Mdy * (1 - ((n - a) / (1 - a)) ** 2), Mdy)
        Mndz = min(Mdz * (1 - n) / (1 - 0.5 * a), Mdz)
        return (Mndy, Mndz)

    # Standard I or H section
    @staticmethod
    def cl_9_3_1_2_c(Mdy, Mdz, N, Nd):
        """Calculates reduced flexural strength for Welded I or H sections
        Args:
            Mdy,Mdz - design strength of section along minor and major axes respectively
                      disregarding axial force
            N - factored applied axial force
            Nd - design strength in compression or tension
        Returns:
            Mndy - reduced flexural strength along minor axis
            Mndz - reduced flexural strength along major axis
        Note:
            Reference:
                IS 800:2007, cl.9.3.1.2
        """
        n = N / Nd
        if (n <= 0.2):
            Mndy = Mdy
        else:
            Mndy = 1.56 * Mdy * (1 - n) * (n + 0.6)
        Mndz = min(1.11 * Mdz * (1 - n), Mdz)
        return (Mndy, Mndz)

    # Rectangular hollow section and welded box sections
    @staticmethod
    def cl_9_3_1_2_d(Mdy, Mdz, N, Nd, A, tf, tw, b, h):
        """Calculates reduced flexural strength for rectangular hollow section and welded box sections
        section must be symmetric
        Args:
            Mdy,Mdz - design strength of section along minor and major axes respectively
                      disregarding axial force
            N - factored applied axial force
            Nd - design strength in compression or tension
            b - width of flange
            A - Area of c/s
            tf - thickness of flange
            tw - thickness of web
            h - depth of web
        Returns:
            Mndy - reduced flexural strength along minor axis
            Mndz - reduced flexural strength along major axis
        Note:
            Reference:
                IS 800:2007, cl.9.3.1.2
        """
        n = N / Nd
        aw = min((A - 2 * b * tf) / A, 0.5)
        af = min((A - 2 * h * tw) / A, 0.5)
        Mndy = min(Mdy * (1 - n) / (1 - 0.5 * af), Mdy)
        Mndz = min(Mdz * (1 - n) / (1 - 0.5 * aw), Mdz)
        return (Mndy, Mndz)

    # Circular hollow tubes
    @staticmethod
    def cl_9_3_1_2_e(Md, N, Nd):
        """Calculates reduced flexural strength for rectangular hollow section and welded box sections
        section must be symmetric
        Args:
            Md - plastic design moment of whole section disregarding axial force
            N - factored applied axial force
            Nd - design strength in compression or tension
        Returns:
            Mnd - design reduced flexural strength
        Note:
            Reference:
                IS 800:2007, cl.9.3.1.2
        """
        n = N / Nd
        Mnd = min(1.04 * Md * (1 - n ** 1.7), Md)
        return Mnd

    # cl.9.3.1.3 Combined Axial Force and Bending - Section Strength - Semi-compact section - Safety Criteria
    # 2 functions

    # function 1 - general criteria
    @staticmethod
    def cl_9_3_1_3_a(fx, fy, gamma_m0):
        """Evaluates safety criteria for semi-compact section design(general)
        Args:
            fx - max. longitudinal stress under combined axial force and bending
            fy - yield stress
            gamma_m0 - partial safety factor
        Returns:
            'OK' - If criteria is satisfied
            else 'Warning : cl.3.1.3 - max. longitudinal stress exceeds limiting value'
        Note:
            Reference:
                IS 800:2007, cl.9.3.1.3
        """
        if (fx <= fy / gamma_m0):
            return 'OK'
        else:
            return 'Warning : cl.3.1.3 - max. longitudinal stress exceeds limiting value'

    # funtion  2 - c/s without holes
    @staticmethod
    def cl_9_3_1_3_b(N, Nd, My, Mdy, Mz, Mdz):
        """Evaluates safety criteria for semi-compact section design for c/s without holes
        Args:
            Mdy,Mdz - design strength of section along minor and major axes respectively
                      disregarding axial force
            My - factored applied moments about minor axis of c/s
            Mz - factored applied moments about major axis of c/s
            N - factored applied axial force
            Nd - design strength in compression or tension
        Returns:
            'OK' - If criteria is satisfied
            else 'Warning : cl.3.1.3 - max. longitudinal stress exceeds limiting value'
        Note:
            Reference:
                IS 800:2007, cl.9.3 'Warning : cl.9.3.1.3 - semi-comapct is not safe under given axial force and bending moment'
        """
        if ((N / Nd + My / Mdy + Mz / Mdz) <= 1):
            return 'OK'
        else:
            return 'Warning : cl.9.3.1.3 - semi-comapct is not safe under given axial force and bending moment'

    # cl.9.3.2.1 Check for safety against buckling - Combined Axial Tension Force and Bending
    @staticmethod
    def cl_9_3_2_1(Md, M, T, Zec, A, psi_check):
        """Calculates and checks if reduced effective moment under tension and bending exceeds bending strength
        due to lateral torsional buckling.
        Args:
            Md - Strength due to lateral torsional buckling
            M,T - factored applied moment and tension respectively
            Zec - elastic section modulus w.r.t extreme compression fibre
            A - area of c/s
            N - factored applied axial force
            Nd - design strength in compression or tension
            psi_check - 'True' if T & M are independent else 'False'
        Returns:
            If (criteria is satisfied):
                Meff - reduced effective moment under tenion and bucling
            else:
                'Warning : reduced effective moment under tension and bending exceeds bending strength
                 due to lateral torsional buckling'
        Note:
            Reference:
                IS 800:2007, cl.9.3.2.1
        """
        if (psi_check is True):
            psi = 0.8
        else:
            psi = 1
        Meff = M - psi * T * Zec / A
        if (Md >= Meff):
            return Meff
        else:
            return 'Warning : cl.9.3.2.1 - reduced effective moment under tension and bending exceeds bending streng due to lateral torsional buckling'

    # cl.9.3.2.2 Check for safety against buckling - Combined Axial Compression and Bending
    # 2 functions

    # function1_based on table18
    @staticmethod
    def cl_9_3_2_2_table18(loading_type, psi, Mh, Ms=None):
        """Evaluates and returns equivalent moment factor
        Args:
            loading_type - True if loading is unifrorm, False if load is concentrated
            psi - ratio of BM at the end with higher BM to that of the other end
            Mh - BM at end with greater BM
            Ms - BM at point of zero shear, takes a default value of None (if Load is linearly varying)
        Returns:
            Cm - equivalent uniform moment factor
        Note:
            Reference:
                IS 800:2007, Table 18 (cl9.3.2.2)
        """
        if (abs(psi) > 1): return 'warning: psi must be between -1 and 1'
        if (Ms == None):
            Cm = max(0.6 + 0.4 * psi, 0.4)
        elif (abs(Ms) < abs(Mh)):
            alpha_s = Ms / Mh
            if (alpha_s >= 0):
                Cm = max(0.2 + 0.8 * alpha_s, 0.4)
            else:
                if (loading_type == True):
                    Cm = max((0.1 * max(1 - psi, 1) - 0.8 * alpha_s), 0.4)
                else:
                    Cm = max((0.2 * max(-psi, 0) - 0.8 * alpha_s), 0.4)
        elif (abs(Ms) > abs(Mh)):
            alpha_h = Mh / Ms
            if (alpha_h >= 0):
                if (loading_type == True):
                    Cm = 0.95 - 0.05 * alpha_h
                else:
                    Cm = 0.90 + 0.10 * alpha_h
            else:
                if (loading_type == True):
                    Cm = 0.95 + 0.05 * alpha_h * min(1 + 2 * psi, 1)
                else:
                    Cm = 0.90 + 0.1 * alpha_h * min(1 + 2 * psi, 1)
        else:
            return 'Warning:Ms cannot be equal to Mh,but can be NULL'

        return Cm

    @staticmethod
    def cl_9_3_2_2_main(P, Pd=[], M=[], Mh=[], Md=[], N=[], Nd=[], loading_type=[], psi=[], lambda_=[],
                        Ms=[None, None, None]):
        """Checks safety criteria for members subjected to combined axial compresssion and biaxial bending
        Args:
            P - applied axial compression under factored load
            loading_type[0],loading_type[1],loading_type[2] - loading type(True if uniform,False if concentrated)
                                                              for y,z axes and lateral torsion
            psi[0],psi[1],psi[2] - psi values for y/Z aand lateral torsion
            M[0]=My,M[1]=Mz - max factored applied bending moments about y and z axes of member
            M[2]=Mmlt - max factored applied bending moment for lateral torsion
            Mh[0]=Mhy,Mh[1]=Mhz - factored applied bending moments about y and z axes of member at point of zero shear
            Mh[2]=Mhmlt - factored applied bending moment for lateral torsion at point of zero shear
            Pd[0]=Pdy,Pd[1]=Pdz - design strength under axial compression as governed by buckling about y and z axes resp
            Md[0]=Mdy,Md[1]=Mdz - design bending strength about y and z axes considering laterally unsupported length of c/s
            N[0]=Ny,N[1]=Nz - factored applied axial force about y/z axes resp.
            Nd[0]=Ndy,Nd[1]=Ndz - design strength in compression about y/z axes resp.
            lambda[0]=lambda_y,lambda[1]=lambda_z,lambda[3]=lambda_Lt - slenderness ratio about y/z axes and that for lateral torsion
            Ms[] - BM @ point of zero shear
        Returns:
            'OK' - If criteria is satisfied
            else -'Warning : Member does not satisfy safety criteria of cl.9.3.2.2'
        Note:
            Reference:
                IS 800:2007, cl.9.3.2.2
        """
        Cmy = IS800_2007()
        Cmz = IS800_2007()
        CmLt = IS800_2007()
        Cm = [Cmy.cl_9_3_2_2_table18(loading_type[0], psi[0], Mh[0], Ms[0]),
              Cmz.cl_9_3_2_2_table18(loading_type[1], psi[1], Mh[1], Ms[1]),
              CmLt.cl_9_3_2_2_table18(loading_type[2], psi[2], Mh[2], Ms[2])]

        Ky = min(1 + (lambda_[0] - 0.2) * N[0] / Nd[0], 1 + 0.8 * N[0] / Nd[0])
        Kz = min(1 + (lambda_[1] - 0.2) * N[1] / Nd[1], 1 + 0.8 * N[1] / Nd[1])
        Klt = max(1 - (0.1 * lambda_[3] * (N[0] / Nd[0])) / (Cm[3] - 0.25), 1 - (0.1 * N[0] / Nd[0]) / (Cm[3] - 0.25))

        if ((P / Pd[0] + Ky * Cm[0] * M[0] / Md[0] + Klt * M[1] / Md[1] <= 1) and (
                P / Pd[1] + 0.6 * Ky * Cm[0] * M[0] / Md[0] + Kz * Cm[1] * M[1] / Md[1] <= 1)):
            return 'OK'
        else:
            return 'warning: member does not satisfy safety criteria of cl.9.3.2.2'
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
    def cl_10_2_1_bolt_hole_size(d, bolt_hole_type='standard'):
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
        t = min(plate_thicknesses)
        return min(32*t, 300.0)

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
            return min(16*t, 200.0)
        elif member_type == 'compression':
            return min(12*t, 200.0)
        else:
            # TODO compression members wherein forces are transferred through butting faces is given in else
            return 4.5 * d

    # cl. 10.2.4.2  Minimum Edge and End Distances
    @staticmethod
    def cl_10_2_4_2_min_edge_end_dist(d, bolt_hole_type='standard', edge_type='hand_flame_cut'):
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
        if edge_type == 'hand_flame_cut':
            return 1.7 * d_0
        else:
            # TODO : bolt_hole_type == 'machine_flame_cut' is given in else
            return 1.5 * d_0

    # cl. 10.2.4.3  Maximum Edge Distance
    @staticmethod
    def cl_10_2_4_3_max_edge_dist(plate_thicknesses, f_y, corrosive_influences=False):
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
    def cl_10_3_3_bolt_shear_capacity(f_u, A_nb, A_sb, n_n, n_s=0, safety_factor_parameter='field'):
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
    def cl_10_3_3_2_bolt_large_grip(d, l_g, l_j=0):
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
        if beta_lg >= IS800_2007.cl_10_3_3_1_bolt_long_joint(d, l_j):
            beta_lg = IS800_2007.cl_10_3_3_1_bolt_long_joint(d, l_j)
        if l_g <= 5.0 * d:
            beta_lg = 1
        elif l_g > 8.0 * d:
            return "GRIP LENGTH TOO LARGE"
        return beta_lg

    # cl. 10.3.4 Bearing Capacity of the Bolt
    @staticmethod
    def cl_10_3_4_bolt_bearing_capacity(f_u, f_ub, t, d, e, p, bolt_hole_type='standard', safety_factor_parameter='field'):

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
        d_0 = IS800_2007.cl_10_2_1_bolt_hole_size(d, bolt_hole_type)
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
    def cl_10_4_3_bolt_slip_resistance(f_ub, A_nb, n_e, mu_f, bolt_hole_type='standard', slip_resistance='service_load'):
        # TODO : Ensure default slip_resistance = 'service_load' or ultimate_load'
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
        return K * fillet_size

    @staticmethod
    def cl_10_5_4_1_fillet_weld_effective_length(fillet_size, available_length):

        """Calculate effective length of fillet weld from available length to weld in practice

        Args:
            fillet_size - Size of fillet weld in mm (float)
            available_length - Available length in mm to weld the plates in practice (float)

        Returns:
            Effective length of fillet weld in mm (float)

        Note:
            Reference:
            IS 800:2007,  cl 10.5.4.1

        """
        # TODO :  if available_length >= 4 * fillet_size
        effective_length = available_length - 2 * fillet_size
        return effective_length

    # cl. 10.5.7.1.1 Design stresses in fillet welds
    @staticmethod
    def cl_10_5_7_1_1_fillet_weld_design_stress(ultimate_stresses, fabrication='shop'):

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
        f_wn = f_u / math.sqrt(3)
        gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][fabrication]
        f_wd = f_wn / gamma_mw
        return f_wd

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
