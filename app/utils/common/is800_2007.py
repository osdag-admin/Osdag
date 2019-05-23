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
    IS800_2007_cl_5_4_1_Table_5 = {"gamma_m0": {'yielding': 1.10, 'buckling': 1.10},
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
    # DESIGN OF MEMBER SUBJECTED TO BENDING

    # Effective length for cantilever Beam

    def cl_8_3_3_Table_16_Efective_length_for_cantilever_beam(L, Restraint_Condition_1, Restraint_Condition_2,
                                                              Loading_condition):
        """
            Calculate effective length for catiliver beam of projecting length L as per cl.8.3.3

            Args:
                L - Projecting Length of cantiliver beam in mm (float)
                D -  Overall depth of he beam in mm (float)

                Restrained_condition - Either "At support" or "At Top"

                Restraint_Condition_1- "At support"
                Restraint_Condition_2- "At Top"

                At_support -  Either "continous, with lateral restraint to top"
                              or "continous, with  partial torsional restraint"
                              or "continous, with lateral and tosional restraint "
                              or "Restrained laterally,torsionally and against rotation on plan "

                At_top - Either  "free"
                        or "lateral restraint to top flange"
                        or "Torsional restraint"
                        or  "Lateral and torsional restraint"

                Loading_condition - Either "Normal" or  "Destablizing"

            Returns:
                L_LT =  cl_8_3_3_Table_16_Efective_length_for_cantiliver_beam
            Note:
                References:
                IS800:2007, Table 16 (cl 8.3.3)
        """

        if Restraint_Condition_1 == "Continuous, with lateral restraint to top flage":
            if Restraint_Condition_2 == "Free":
                if Loading_condition == "Normal":
                    return 3.0 * L
                else:
                    return 7.5 * L
            if Restraint_Condition_2 == "Lateral restraint to top flage":
                if Loading_condition == "Normal":
                    return 2.7 * L
                else:
                    return 7.5 * L
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return 2.4 * L
                else:
                    return 4.5 * L
            if Restraint_Condition_2 == "Lateral and Torsional restraint":
                if Loading_condition == "Normal":
                    return 2.1 * L
                else:
                    return 3.6 * L
        if Restraint_Condition_1 == "Continuous,with partial torsional restraint":
            if Restraint_Condition_2 == "Free":
                if Loading_condition == "Normal":
                    return 2.0 * L
                else:
                    return 5.0 * L
            if Restraint_Condition_2 == "Lateral restraint to top flage":
                if Loading_condition == "Normal":
                    return 1.8 * L
                else:
                    return 5.0 * L
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return 1.6 * L
                else:
                    return 3.0 * L
                if Restraint_Condition_2 == " Lateral and Torsional restraint":
                    if Loading_condition == "Normal":
                        return 1.4 * L
                    else:
                        return 2.4 * L
        if Restraint_Condition_1 == "Continuous,with lateral and torsional restraint":
            if Restraint_Condition_2 == "Free":
                if Loading_condition == "Normal":
                    return 1.0 * L
                else:
                    return 2.5 * l
            if Restraint_Condition_2 == "Lateral restraint to top flage":
                if Loading_condition == "Normal":
                    return 0.9 * L
                else:
                    return 2.5 * L
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return 0.8 * L
                else:
                    return 1.5 * L
            if Restraint_Condition_2 == " Lateral and Torsional restraint":
                if Loading_condition == "Normal":
                    return 0.7 * L
                else:
                    return 1.2 * L
        if Restraint_Condition_1 == "Restrained laterally,torsionally and against rotation on plan":
            if Restraint_Condition_2 == "Free":
                if Loading_condition == "Normal":
                    return 0.8 * L
                else:
                    return 1.4 * L
            if Restraint_Condition_2 == "Lateral restraint to top flage":
                if Loading_condition == "Normal":
                    return 0.7 * L
                else:
                    return 1.4 * L
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return 0.6 * L
                else:
                    return 0.6 * L
            if Restraint_Condition_2 == "Lateral and Torsional restraint":
                if Loading_condition == "Normal":
                    return 0.5 * L
                else:
                    return 0.5 * L

    def cl_8_3_1_Table_15_Effective_length_for_simply_supported_beams(L, D, Restraint_Condition_1,
                                                                      Restraint_Condition_2, Loading_Condition):
        """
            Calculate effective length against lateral torsional buckling for simply supported Beams and girders
            where no lateral restraint  to the compression falnge is provided as per cl.8.3.1

            Args:
                L -  Span of simply suppotred beams and girders in mm (float)
                D -  Overall depth of he beam in mm (float)

                Restraint_Condition - Either "Torsional Restraint" or "wraping Restraint"
                Restraint_Condition_1- "Torsional Restraint"
                Restraint_Condition_2- "Warping_Restraint"

                "Torsional Restrained" - Either "Fully_resrtrained" or
                                        "Partially_restrained_by_bottom_flange_support_condition" or
                                        "Partially_restrained_by_bottom_flange_support_condition"

                "Warping_Restraint" - Either "Both_flange_fully_restrained" or
                                     "compression_flange_fully_restrained" or
                                     "Compression_flange_partially_restrained" or
                                     "Warping_not_restrained_in_both_flange"


                Loading_Condition  - Either "Normal" or " Destabilizing"
                Returns:
                L_LT  - cl_8_3_1_Effective length for simply supported Beams in mm (float)
            Note:
                    References:
                    IS800:2007, Table 15 (cl 8.3.1)

            """

        if Restraint_Condition_1 == "Fully Restrained":
            if Restraint_Condition_2 == "Both flanges partially restrained":
                if Loading_Condition == "Normal":
                    return 0.70 * L
                else:
                    return 0.85 * L
            if Restraint_Condition_2 == "Compression flange fully Restrained":
                if Loading_Condition == "Normal":
                    return 0.75 * L
                else:
                    return 0.90 * L
            if Restraint_Condition_2 == "Both flanges fully restrained":
                if Loading_Condition == "Normal":
                    return 0.80 * L
                else:
                    return 0.95 * L
            if Restraint_Condition_2 == "Compression flange partially Restrained":
                if Loading_Condition == "Normal":
                    return 0.85 * L
                else:
                    return 1.00 * L
                    if Restraint_Condition_2 == "Wraping not restrained in both flanges":
                        if Loading_Condition == "Normal":
                            return 1.00 * L
                        else:
                            return 1.20 * L
                if Restraint_Condition_1 == "Partially restrained by bottom flange support connection":
                    if Restraint_Condition_2 == "Wraping not restrained in both flages":
                        if Loading_Condition == "Normal":
                            return 1.00 * L + 2 * D
                        else:
                            return 1.20 * L + 2 * D
                if Restraint_Condition_1 == "Partially restrained by bottom flage bearing support":
                    if Restraint_Condition_2 == "Wraping not restrained in both flages":
                        if Loading_Condition == "Normal":
                            return 1.2 * L + 2 * D
                        else:
                            return 1.4 * L + 2 * D

    def cl_8_3_Effective_length_against_torsional_restraint(L, D, Beam_type, Restraint_Condition_1,
                                                            Restraint_Condition_2,
                                                            Loading_Condition):
        """
            Calculation of effective length for given type of beam type as per cl.8.3

        Args:
            L-  Span of simply suppotred beams and girders in mm (float) for
                "Simply_supported_with_no_lateral_restrained_to_the_compression_flanges",
                 Projecting Length of cantiliver beam in mm (float) for
                 "Cantilever_beam",
                 Length of relevent segment between the lateral restraint in mm (float) for
                 "Simply_supported_with_intermediate_lateral_restraints",
                 Centre-to-centre distance of the restraint member in mm (float) for
                 "Beam_provided_with_members_to_give_effective_lateral_restrain_to_compression_flange_at_interval"

            D -  Overall depth of he beam in mm (float)


            Beam_type - Either "Simply_supported_with_no_lateral_restrained_to_the_compression_flanges"
                        or "Simply_supported_with_intermediate_lateral_restraints"
                        or "Beam_provided_with_members_to_give_effective_lateral_restrain_to_compression_flange_at_interval"
                        or "Cantilever_beam"

            FOR "Simply_supported_with_no_lateral_restrained_to_the_compression_flanges"
     Restraint_Condition - Either "Torsional Restraint" or "wraping Restraint"

            Restraint_Condition_1- "Torsional Restraint"
            Restraint_Condition_2- "Warping_Restraint"

            "Torsional Restrained" - Either "Fully_resrtrained" or
                                        "Partially_restrained_by_bottom_flange_support_condition" or
                                        "Partially_restrained_by_bottom_flange_support_condition"

            "Warping_Restraint" - Either "Both_flange_fully_restrained" or
                                     "compression_flange_fully_restrained" or
                                     "Compression_flange_partially_restrained" or
                                     "Warping_not_restrained_in_both_flange"


            FOR "Cantilever_beam"

            Restrained_condition - Either "At support" or "At Top" for "Cantilever_beam"

            Restraint_Condition_1- "At support"
            Restraint_Condition_2- "At Top"

            At_support -  Either "continous, with lateral restraint to top"
                              or "continous, with  partial torsional restraint"
                              or "continous, with lateral and tosional restraint "
                              or "Restrained laterally,torsionally and against rotation on plan "

            At_top - Either  "free"
                        or "lateral restraint to top flange"
                        or "Torsional restraint"
                        or  "Lateral and torsional restraint"

            Loading_condition - Either "Normal" or  "Destablizing"



        Returns :
            L_LT - Effective_length_of_beam in m (float)

        Note:
                References:
                IS800:2007,  cl 8.3.

        """

        if Beam_type == "Simply_supported_with_no_lateral_restrained_to_the_compression_flanges":
            L_LT = cl_8_3_1_Table_15_Effective_length_for_simply_supported_beams(L, D, Restraint_Condition_1,
                                                                                 Restraint_Condition_2,
                                                                                 Loading_Condition)
        elif Beam_type == "Simply_supported_with_intermediate_lateral_restraints":
            L_LT = 1.2 * L
        elif Beam_type == "Beam_provided_with_members_to_give_effective_lateral_restrain_to_compression_flange_at_interval":
            L_LT = 1.2 * L
        else:
            L_LT = cl_8_3_3_Table_16_Efective_length_for_cantilever_beam(L, Restraint_Condition_1,
                                                                         Restraint_Condition_2, Loading_Condition)

        return L_LT

    # Design Strenth in Bending(Flexure)
    def Design_strength_in_bending(M, M_d):
        """ Calculation of design bending strength
        Args:
             M: Factored design moment in N*mm
            M_d: design bending strength of the section in N*mm
        Return:
            M_d - design bending strength of the section in N*mm
        Note:
            References:
                IS800:2007,  cl 8.2.
        """

        if M <= M_d:
            return bool(M <= M_d)

    def Design_bending_strength_of_laterally_unsupported_beam(Z_p, Z_e, f_y, V, V_d, M_dv, plastic=False,
                                                              compact=False):
        """Calucation of bending strength of laterally unsupported beam for low shear  and high shear case
            Args:
                Beta_b - 1 for plastic and compact
                         Z_e/Z_p for semi-compact
                Z_e - Elastic section modulus of the cross section in mm**3
                Z_p - Plastic section modulus of the cross section in mm**3
                f_y - yield stress of the material (in N/ mm**2 )
                V  - Factored design shear strengh in N
                V_d - Design shear stregth in N
                M_dv: Design bending strength under high shear as defined in Cl 9.2 in N*m

            Returns:
                M_d - Design Bending  strength in N*m
            Note:
                References:
                IS800:2007,  cl 8.2.1.2, cl. 8.2.1.3

        """
        Beta_b = Z_e / Z_p
        if plastic is True:
            Beta_b = 1
        if compact is True:
            Beta_b = 1
        gamma_m0 = cl_5_4_1_Table_5['gamma_m0']['yielding']
        if V <= 0.6 * V_d:
            M_d = Beta_b * Z_p * f_y / gamma_m0

        if V > 0.6 * V_d:
            M_d = M_dv

        # TODO : M_dv is referred from cl9.2

        return M_d

    # cl8.2.2 DESIGN BENDING STRENGTH OF LATERALLY UNSUPPORTED BEAMS
    # cl8.2.2.1 Elastic lateral torsional buckling moment
    def Elastic_lateral_torsional_buckling_moment(I_y, E, A_e, G, L, D, Restraint_Condition_1, Restraint_Condition_2,
                                                  Loading_Condition, section, n, b=[], t=[]):
        """
            Calculation of elastic critical moment or elastic lateral torional buckling moment
            Args:
                I_t - torsional constant
                I_w - wraping constant
                I_y - moment of inertia about weaker axis
                r_y - radius of gyration about weaker axis
                L_LT - effective length for lateral torsional buckling accordance with cl8.3
                h_f - centre-to-centre distance between flange
                t_f - thickness of the flange
                E - Youngs Modulus of elaticity
                G - modulus of rigidity
                b - breadth of the elements in a section
                t - thickness of the elemnets of the section
                A_e - Area enclosed by the section
                section - Either 'open section' or 'hollow section'

            Return:
                M_cr - Elastic lateral torsional buckling moment
            Notes:
                 Reference:
                IS 800:2007, cl. 8.2.2.1.

        """
        if section == 'open_section':
            sum_value = 0
            for i in range(n):
                sum_value += ((b[i] * t[i] ** 3) / 3)
                I_t = sum_value
        else:
            sum_value = 0
            for i in range(n):
                sum_value += (b[i] / t[i])
                I_t = 4 * A_e / sum_value

        L_LT = cl_8_3_1_Table_15_Effective_length_for_simply_supported_beams(L, D, Restraint_Condition_1,
                                                                             Restraint_Condition_2, Loading_Condition)

        M_cr = math.sqrt((pi ** 2 * E * I_y / L_LT ** 2) * (G * I_t + (pi ** 2 * E * I_w / L_LT ** 2)))

        return M_cr

    def design_bending_Strength_of_laterally_unsupported_beam(I_y, E, A_e, G, L, D, Restraint_Condition_1,
                                                              Restraint_Condition_2,
                                                              Loading_Condition, t, section, n, Z_p, Z_e, f_y, V, V_d,
                                                              M_dv, plastic=False, compact=False, *b):
        """
             Calculation of design bending strength of laterally unsupported beam
             Args:
                 Z_p - plastic section modulus with respect to extreme compression fibre
                 Z_e - elastic section modulud with respect to extreme compression fibre
                 f_y - yield stress
                 beta_b - 1.0 for plastic and compact section
                          Z_p/Z_e for semi-compact section
                 X_LT - design bending compressive stress
                 section - Either 'Rolled_steel_section' or "Welded_steel_section'
                 M_cr - elastic critical moment calculated in accordance with 8.2.2.1
                 f_cr_b - extreme fibre bending compressive stress corresponding to elastic lateral buckling momnet

             Returns:
                 M_d - Design bending strength of laterally unsupported beam

             Note:
                Reference:
                IS 800:2007, cl. 8.2.2.

        """
        beta_b = Z_p / Z_e
        if plastic is True:
            beta_b = 1
        if compact is True:
            beta_b = 1

        if section == 'Rolled_steel_section':
            alpha_LT = 0.21
        else:
            alpha_LT = 0.49

        M_cr = Elastic_lateral_torsional_buckling_moment(I_y, E, A_e, G, L, D, Restraint_Condition_1,
                                                         Restraint_Condition_2, Loading_Condition, t, section, n, *b)
        f_cr_b = M_cr / (beta_b * Z_p)
        Lambda_LT = min(math.sqrt(f_y / f_cr_b), math.sqrt(1.2 * Z_e * f_y / M_cr))
        phi_LT = 0.5 * (1 + alpha_LT * (lambda_LT - 0.2) + lambda_LT ** 2)
        X_LT = min(1.0, 1 / (phi_LT + math.sqrt(phi_LT ** 2 - lambda_LT ** 2)))
        f_bd = X_LT * f_y / gamma_m0

        if Lambda_LT < 0.4:
            M_d = Design_bending_strength_of_laterally_unsupported_beam(Z_p, Z_e, f_y, V, V_d, M_dv, plastic=False,
                                                                        compact=False)

        else:
            M_d = beta_b * Z_p * f_bd

        return M_d

    # --------------------
    # cl8.4 Shear Design
    def design_shear_strength_of_beam(V_n, V, Safety_factor):
        """
            Dsign shear strength
        Args:
            V_n -Nominal  shear strength of a cross-section
            V - Factored design shear force
            Safety_factor- Either 'Field' or 'shop'
        Return
            V_d - Design shear strength
        Note:
                Reference:
                IS 800:2007, cl. 8.4

        """
        gamma_m0 = cl_5_4_1_Table_5['gamma_m0'][safety_factor_parameter]
        V_d = V_n / gamma_mo
        if V <= V_d:
            return V_d

    def nominal_plastic_shear_resistance_under_pure_shear(A_v, f_yw):
        """
            Calculation of nominal plastic shear resistance under pure shear
            Args:
                A_v - Shear area
                f_yw - yield shear of the web

            Returns:
                V_n - Nominal plastic shear resistance under pure force

             Note:
                Reference:
                IS 800:2007, cl. 8.4
        """

        V_p = A_v * f_yw / math.sqrt(3)
        V_n = V_p
        return V_n

    def shear_area_of_different_section(A, b, d, h, t_f, t_w, section, Axis_of_Bending, load_application_axis):
        """
            Calculation of shear area of different section

            Args:
                A - cross - section area
                b - overall breadth of tubular section,breadth of I - section flange
                d - clear depth of the web between flange
                h- overll depth of teh section
                t_f - thickness of the flange
                t_w - thickness of the web
                section - Either 'I_Section' or 'Channel_section' or 'Rectangular_hollow_section_of_uniform_depth'
                          or 'Circular_hollow_tubes_of_uniform_thickness' or 'plates' or 'solid_bars'
                Load_application_axis - Either 'Loaded_parallel_to_depth(h)' or 'Loaded_parallel_to_width(b)'
                Axis_of_Bending - Either 'Major_Axis_Bending' or 'Minor_Axis_Bending'
                cross_section - Either 'Hot_Rolled' or ' Welded'

            Return:
                A_v - Shear area

            Note:
                Reference:
                IS 800:2007, cl. 8.4.1.1

        """
        if Axis_of_Bending == 'Major_Axis_Bending':
            if section == 'I_section_Hot_Rolled':
                A_v = h * t_w
                return A_v
            else:
                A_v = d * t_w
                return A_v

        if Axis_of_Bending == 'Minor_Axis_Bending':
            if Section == 'I_section_Hot_Rolled':
                A_v = 2 * b * t_f
                return A_v
            else:
                A_v = 2 * b * t_f
                return A_v

            if section == 'Rectangular_hollow_section_of_uniform_depth':
                if load_application_axis == 'Loaded_parallel_to_depth':
                    A_v = A * h / (b + h)
                    return A_v
                else:
                    A_v = A * b / (b + h)
                    return A_v

            if section == 'Circular_hollow_tubes_of_uniform_thickness':
                A_v = A
                return A_v

            if section == 'plates':
                A_v = A
            else:
                A_v = A

            return A_v

    # cl8.4.2 TODO: CHECK RESISTANCE TO SHEAR BUCKLING

    # cl8.4.2.2 Shear buckling design method
    def nominal_shear_strength(method, nu, c, E, f_yw, f_yf, position_of_transverse_shear, b_f, A, b, d, h, t_f, t_w,
                               Section, Axis_of_Bending, Load_application_axis, Section_type):
        """
            Calculation of nominal shear strength
            Args:
                 method - Either 'Simple_post_ critical_method' or 'Tension_field_method'
                 A_v - shear area defined in cl8.4.1.1
                 T_b - shear stress corresponding to web buckling
                 lambda_w - non-dimensional web slenderness ratio for shear buckling stress
                 T_cr_c - the elastic critical shear stress of the web
                 nu - poisson 's ration
                 c - spacing of transverse stiffners
                 d - depth of the web
                 E - youngs modulus of elasticity
                 t_w - thickness of web
                 f_yw - yield strenth of  the web
                 V_cr - shear force corresponding to web buckling
                 f_v - yield strength of the tension field
                 phi - inclination of the tension field
                 w_tf - the width of the tension field
                 s_c - anchorage lengths of tension field  along the compresssion flange
                 s_t - anchorage lengths of tension field  along the tension flange
                 M_fr - reduecd plastic moment capacity of the repective flange plate after accounting for axial force
                 N_f - reduecd plastic moment capacity in the flange due to overall bending and
                        any external axial force in the cross section
                 b_f - width of the relevent flange
                 t_f - thickness of the relevent flange
                 f_yt - yield stress of the flange
            Return:
                V_n - nominal shear strength
            Note:
                Reference:
                IS 800:2007, cl. 8.4.2.2.

        """

        A_v = shear_area_of_different_section(A, b, d, h, t_f, t_w, Section, Axis_of_Bending, Load_application_axis,
                                              Section_type)
        if method == 'Simple_post_ critical_method':
            if position_of_transverse_shear == 'At support':
                K_v = 5.35
            elif c / d < 1.0:
                K_v = 4.0 + (5.35 / (c / d) ** 2)
            elif c / d > 1.0:
                K_v = 5.35 + (4.0 / (c / d) ** 2)

                return K_v

            T_cr_c = (K_v * pi ** 2 * E) / (12 * (1 - nu ** 2) * (d / t_w) ** 2)
            lambda_w = math.sqrt(f_yw / (math.sqrt(3) * T_cr_c))

            if lambda_w <= 0.8:
                T_b = f_yw / math.sqrt(3)

            for lambda_w in range(0.8, 1.2):
                T_b = (1 - 0.8 * (lambda_w - 0.8)) * (f_yw / math.sqrt(3))
            else:
                T_b = f_yw / (math.sqrt(3) * lambda_w ** 2)

            V_cr = A_v * T_b
            V_n = V_cr

            return (V_n, T_b)
        gamma_m0 = cl_5_4_1_Table_5['gamma_m0'][fabrication]

        if method == 'Tension_field_method':
            phi = arctan(d / c)
            shi = 1.5 * T_b * sin(2 * phi)
            M_fr = 0.25 * b_f * t_f ** 2 * f_yf * (1 - (N_f / (b_f * t_f * f_yf / gamma_m0)) ** 2)

            s = min(c, (2 / sinphi) * math.sqrt(M_fr / f_yw * t_w))
            s_c = s
            s_t = s

            w_tf = d * cos(phi) + (c - s_c - s_t) * sin(phi)

            f_v = math.sqrt(f_yw ** 2 - 3 * T_b ** 2 + shi ** 2) - shi
            V_p = A_v * f_yw / math.sqrt(3)

            V_tf = min(V_p, (A_v * T_b + 0.9 * w_tf * t_w * f_v * sin(phi)))

            V_n = V_tf

            return V_n

    # STtiffened web Deisign
    # End plate Design
    # ..............................................................
    # cl8.5.3 Anchor forces
    # cl8.5.3 Anchor forces
    def anchor_forces(d, t, f_y, V, method, nu, c, E, t_w, f_yw, f_yf, position_of_transverse_shear, s_c, s_t, b_f,
                      t_f):
        """ Calculation of resultant longitudinal shear and moment
            Args:
                d - web depth
                t - thickness of the section
                f_y - yield stress
                V_cr - critical shear strength as defined in cl8.4.2.2.
                V_tf - basic shear strength as defined in cl8.4.2.2.
                V = actual factored shear force
            Return:
                M_tf - resultant longitudinal moment
                R_tf - resultant longitudinal shear

            Note:
                Reference:
                IS 800:2007, cl. 8.4.2.2.
        """
        V_cr = nominal_shear_strength(method, nu, c, d, E, t_w, f_yw, f_yf, position_of_transverse_shear, s_c, s_t, b_f,
                                      t_f)
        V_tf = nominal_shear_strength(method, nu, c, d, E, t_w, f_yw, f_yf, position_of_transverse_shear, s_c, s_t, b_f,
                                      t_f)
        V_p = d * t * f_y / math.sqrt(3)

        if V < V_tf:
            H_q = (V - V_cr) / (V_tf - V_p)
        else:
            H_q = 1.25 * V_p * math.sqrt(1 - V_cr / V_p)

        R_tf = H_q / 2
        M_tf = H_q * d / 10
        return (R_tf, M_tf)

    # cl8.6 Design of Beams and Plate Girders with Solid Webs
    # cl8.6.1Minimum Web Thickness
    # cl8.6.1.1 Serviceability requirement
    def cl_8_6_1_1_minimum_web_thickness(d, t_w, c, f_yw, serviceability_requirement, web_connection_to_flange):
        """
            Checking the serviceability requirment of  minimum thickness of web
            Args:
                d - web depth
                t_w - thickness of web
                c - spacing of transverse stiffner
                apsilon_w - yield stress ratio of web
                f_yw - yield stress of the web
            Return:
                True or false

            Note:
                Reference:
                IS 800:2007, cl. 8.6.1.1

        """
        apsilon_w = math.sqrt(250 / f_yw)
        if serviceability_requirement == 'transverse_stiffner_not_provided':
            if web_connection_to_flange == 'along_both_longitudinal_edges':
                d / t_w <= 200 * apsilon_w
                return bool(d / t_w)
            else:
                d / t_w <= 90 * apsilon_w
                return bool(d / t_w)

        elif serviceability_requirement == 'transverse_stiffner_not_provided':
            if d < c <= 3 * d:
                d / t_w <= 200 * apsilon_w
                return bool(d / t_w)
            elif 0.74 * d <= c < d:
                c / t_w <= 200 * apsilon_w
                return bool(d / t_w)
            elif c < 0.74 * d:
                d / t_w <= 270 * apsilon_w
                return bool(d / t_w)
            else:
                return 'web_is_considered_unstiffened'

        elif serviceability_requirement == 'transverse_and_longitudinal_stiffner_at_one_level_as_cl_8_7_13':
            if d < c <= 2.4 * d:
                d / t_w <= 250 * apsilon_w
                return bool(d / t_w)
            elif 0.74 * d <= c < d:
                c / t_w <= 250 * apsilon_w
                return bool(d / t_w)
            else:
                d / t_w <= 340 * apsilon_w
                return bool(d / t_w)

        else:
            d / t_w <= 400 * apsilon_w
            return bool(d / t_w)

    # Compression flange buckling requirement
    def web_thickness_to_aviod_buckling_of_compression_flange(d, t_w, c, f_yf, Transverse_stiffner=True):
        """
            Check for minimum web thickness to avoid bucklng of compression flange
            Args:
                d - depth of the web
                t_w - thickness of the web
                c - spacing of transverse stiffner
                apsilon_f - yield stress ratio of flange
                f_yw - yield stress of compression flange
            Return:

        """
        apsilon_f = math.sqrt(250 / f_yf)
        d / t_w <= 345 * apsilon_f ** 2

        if Transverse_stiffner is False:
            if c >= 1.5 * d:
                d / t_w <= 345 * apsilon_f ** 2
                return bool(d / t_w)
            else:
                d / t_w <= 345 * apsilon_f
                return bool(d / t_w)

    # cl8.7.1.5 Buckling resistance of stiffeners
    # Effective length for load carrying web stiffners
    def effective_length_for_load_carrying_web_stiffners(L, restrained_condition):
        """
        Calculation of Effective length for load carrying web stiffners for calculating
            buckling resistance F_xd
        Args:
            L - length of stiffner
            restrained_condition - Either 'flange_restrained_against_rotation' or
                                    'flange_not_restrained_against_rotation'
        Returns:
            K_L - effective length for load carrying web stiffners
        Note:
            Reference:
            IS 800:2007,   cl 8.7.1.5
        """
        if restrained_condition == 'flange_restrained_against_rotation':
            K_L = 0.7 * L
            return K_L
        else:
            K_L = L
            return K_L

    # Cl 8.7.2.4 Minimum stiffeners
    def I_s_for_transverse_web_Stiffners_not_subjected_to_external_load(c, d, t_w):
        """
        Calculation of second moment of area when transverse web stiffner
                not subjected to external laod
        Args:
            d - depth of thw web
            t_w - minimum required web thickness foe spacing using tension filed action ,as given in cl8.4.2.1
            c - actual stiffener spacing
        Return:
            I_s_min - second momonet of area
        Note:
            Reference:
            IS 800:2007,  cl 8.7.2.4
        """
        if c / d >= math.sqrt(2):
            I_s_min = 0.75 * d * t_w ** 3
        else:
            I_s_min = (1.5 * d ** 2 * t_w ** 3) / c ** 2

        return I_s_min

    # cl 8.7.2.5 Buckling check on intermediate transverse web stiffners
    def buckling_check_on_intermediate_transverse_web_stiffener(V, F_qd, F_x, F_xd, M_q, M_yq):
        """
            Buckling check on intermediate transverse web stiffners
        Args:
                F_qd - design resistance of the intermediate stiffners
                V -factored shear force adjacent to the stiffner
                F_qd - deign resistance of an intermediate web stiffner
                        to buckling corresponding to buckling about at
                         axis parallel to the web as in cl 8.7.1.5
                F_x - external load or reaction at the stiffner
                F_xd - design resistance of a load carrying stiffener
                        corresponding to buckling about axis parallel
                        to the web as in cl 8.7.1.5
                M_q - moment on the stiffner due to eccentrically
                        applied load anf transverse load, if any
                M_yq - yield moment capacity og the stiffner based
                        on its elastic modulus about its centriodal
                        axis parallel to the web
        Retrun:
            F_q - stiffener force

        Note:
            Reference:
            IS 800:2007,  cl 8.7.2.5

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']
        V_cr = nominal_shear_strength(method, nu, c, d, E, t_w, f_yw, f_yf, position_of_transverse_shear, s_c, s_t, b_f,
                                      t_f)
        F_q = min(V - (V_cr / gamma_m0), F_qd)
        if (F_q - F_x) / F_qd + F_x / F_xd + M_q / M_yq <= 1:
            return bool((F_q - F_x) / F_qd + F_x / F_xd + M_q / M_yq)

    # cl 8.7.2.6 Connection of intermediate stiffeners to web
    def shear_between_each_component_of_stiffener_and_web(t_w, b_s):
        """
            Calculation of minimum shear between each component of stiffener and web

            Args:
                t_w - web thickness in mm
                b_s - outstand width of the stiffeners in mm

            Returns:
                V_is_min - minimum shear between each component of stiffener and web in kN/mm

            Notes:
                Reference:
                IS 800:2007,  cl 8.7.2.6

        """
        V_is_min = t_w ** 2 / 5 * b_s
        return V_is_min

    # cl 8.7.2.6 Load Carrying stiffeners
    def area_of_cross_section_of_web(b_1, n_1, t_w):
        """
            Calculation of area of cross section of the web

            Args:
                b_1 - width of stiff bearing on the flange
                n_1 - dispersion of the load through the web
                     45 degree, to the level of half the depth
                     of the cross section
                t_w - web thickness
            Returns:
                A_w - area of cross section of the web
            Notes:
                Reference:
                IS 800:2007,  cl 8.7.3.1
        """
        A_w = (b_1 + n_1) / t_w
        return A_w

    # cl 8.7.4 Bearing Stiffeners
    def force_applied_through_flange_by_loads_(b_1, n_2, t_w, f_yw):
        """
            Calculation of force applied through a flange by load or reaction
            exceeding the local capacity of the web at its connection

            Args:
                b_1 - stiff bearing length
                n_2 - length obatined by dipersion through the flange to the web
                        junction at a slope of 1:2.5 to the plane of the flange
                t_w - thickness of the web
                f_yw - yield stress of the web

            Returns:
                F_w - force applied through flange by loads

            Notes:
                Reference:
                IS 800:2007,  cl 8.7.4

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']
        F_w = (b_1 + n_2) * t_w * f_yw / gamma_m0

        return F_w

    # cl 8.7.5 Design of load carrying stiffeners
    # cl 8.7.5.1 Buckling check
    # cl 8.7.5.2 Bearing check

    def bearing_strength_of_stiffeners(F_x, A_q, f_yq):
        """
            Calculation of bearing strength of stiffeners
        Args:
            F_x - external load or reaction
            A_q - area of the stiffeners in contact with the flange
            f_yq - yield stress of the stiffeners

        Return:
            F_psd - bearing strength of stiffeners

        Notes:
                Reference:
                IS 800:2007,  cl 8.7.4
        """

        F_psd = min(A_q * f_yq / (0.8 * gamma_m0), F_x)
        return F_psd

    # cl 8.7.9 Torsional Stiffeners
    def Second_moment_of_area_of_the_stiffener_Section(D, T_cf, L_LT, r_y):
        """
            calculation of  minimum second moment of area of the stiffener

            Args:
                D = overall depth of beam at support
                T_cf = maximum thickness of compression flange in the span under consideration
                K_L=  laterally unsupported effcetive length of the compression flange of the beam
                r_y = radius of gyration of the beam about the minor axis

            Returns:
                I_s_min = calculation of  minimum second moment of area of the stiffener

            Notes:
                Reference:
                IS 800:2007,  cl 8.7.4

        """
        if L_LT / r_y <= 50:
            alpha_s = 0.006
        elif 50 < L_LT / r_y <= 100:
            alpha_s = 0.3 / (L_LT / r_y)
        else:
            alpha_s = 30 / (L_LT / r_y)

        I_s_min = 0.3 * alpha_s * D ** 3 * T_cf

        return I_s_min

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
