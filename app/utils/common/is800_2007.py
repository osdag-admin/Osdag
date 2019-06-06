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
    # -------------------------------------------------------------
    # Table 2 Limiting width to thickness ratio
    """ calculating class using Limiting width to thickness ratio
            Args:
                 b - width of element (float)
                 d - depth of web (float)
                 t - thickness of element (float)
                 tf - thickness of flange (float)
                 tw - thickness of web (float)
                 D - outer diameter of element (float)
                 r1 - actual average stress/design compressive stress of web alone (float) 
                 r2 - actual average stress/design compressive stress of overall section (float)
                 f_y - Yield stress of the plate material in MPa (float)
                 e = sqrt(250/f_y)
                 """

    def null(self, b, tf, d, tw, t, D):

        cl_3_7_Table_2 = {
            "Compression_elements": {
                "outstanding_elements_compression_flange": {"rolled": b / tf, "welded": b / tf},
                "internal_elements_compression_flange": {"compression_due_to_bending": b / tf,
                                                         "axial_compression": b / tf},
                "web_of_a_channel": d / tw,
                "angle_compression_due_to_bending": {b / t, d / t},
                "single_angles_or_double_angles_with_seperated_elements_axial_compression": {b / t, d / t, (b + d) / t},
                "outstanding_leg_in_back_to_back_in_a_double_angle_member": d / t,
                "outstanding_leg_of_an_angle_with_its_back_in_cont_contact_with_another_component": d / t,
                "stem_of_tsection_rolled_or_cut_from_a_rolled_IorH_section": D / tf,
                "circular_hollow_tube_including_welded_tube_subjected_to": {"moment": D / t,
                                                                            "axial_compression": D / t},
                "web_of_an_I_or_H_section": {"general": d / tw, "axial_compression": d / tw}
            }
        }

    def cl_3_7_3_class(self, cl_3_7_Table_2, e, r1):
        """ Gives class of cross sections using table 2
        Args:
             b - width of element (float)
             d - depth of web (float)
             t - thickness of element (float)
             tf - thickness of flange (float)
             tw - thickness of web (float)
             D - outer diameter of element (float)
             r1 - actual average stress/design compressive stress of web alone (float)
             r2 - actual average stress/design compressive stress of overall section (float)
             f_y - Yield stress of the plate material in MPa (float)
             e = sqrt(250/f_y)
        Return:
            Class - type of the cross section (string)
        Note:
            Reference: IS 800:2007, cl 3.7.2
        """
        if cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["rolled"] <= 9.4 * e:
            return "class1"
        elif cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["rolled"] > 9.4 * e and cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["rolled"] <= 10.5 * e:
            return "class2"
        elif cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["rolled"] > 10.5 * e and cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["rolled"] < 15 * e:
            return "class3"
        elif cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["welded"] <= 8.4 * e:
            return "class1"
        elif cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["welded"] > 8.4 * e and cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["welded"] <= 9.4 * e:
            return "class2"
        elif cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["welded"] > 9.4 * e and \
                cl_3_7_Table_2[0]["outstanding_elements_compression_flange"]["welded"] >= 13.6 * e:
            return "class3"
        elif cl_3_7_Table_2[0]["internal_elements_compression_flange"]["compression_due_to_bending"] <= 29.3 * e:
            return "class1"
        elif cl_3_7_Table_2[0]["internal_elements_compression_flange"]["compression_due_to_bending"] > 29.3 * e and \
                cl_3_7_Table_2[0]["internal_elements_compression_flange"]["compression_due_to_bending"] <= 33.5 * e:
            return "class2"
        elif cl_3_7_Table_2[0]["internal_elements_compression_flange"]["compression_due_to_bending"] > 33.5 * e and \
                cl_3_7_Table_2[0]["internal_elements_compression_flange"]["compression_due_to_bending"] <= 42 * e:
            return "class3"
        elif cl_3_7_Table_2[0]["internal_elements_compression_flange"]["axial_compression"] >= 42 * e:
            return "class3"
        elif cl_3_7_Table_2[0]["web_of_a_channel"] <= 42 * e:
            return "class1 or class2 or class3"
        elif cl_3_7_Table_2[0]["angle_compression_due_to_bending"][0] <= 9.4 * e and \
                cl_3_7_Table_2[1]["angle_compression_due_to_bending"][0] <= 9.4 * e:
            return "class1"
        elif cl_3_7_Table_2[0]["angle_compression_due_to_bending"][0] > 9.4 * e and \
                cl_3_7_Table_2[0]["angle_compression_due_to_bending"][0] <= 10.5 * e and \
                cl_3_7_Table_2[0]["angle_compression_due_to_bending"][1] > 9.4 * e and \
                cl_3_7_Table_2[0]["angle_compression_due_to_bending"][1] <= 10.5 * e:
            return "class2"
        elif cl_3_7_Table_2[0]["angle_compression_due_to_bending"][0] > 10.5 * e and \
                cl_3_7_Table_2[0]["angle_compression_due_to_bending"][0] <= 15.7 * e and \
                cl_3_7_Table_2[0]["angle_compression_due_to_bending"][1] > 10.5 * e and \
                cl_3_7_Table_2[0]["angle_compression_due_to_bending"][1] <= 15.7 * e:
            return "class3"
        elif cl_3_7_Table_2[0]["single_angles_or_double_angles_with_seperated_elements_axial_compression"][
            0] <= 15.7 * e and \
                cl_3_7_Table_2[0]["single_angles_or_double_angles_with_seperated_elements_axial_compression"][
                    1] <= 15.7 * e and \
                cl_3_7_Table_2[0]["single_angles_or_double_angles_with_seperated_elements_axial_compression"][
                    2] <= 25 * e:
            return "class3"
        elif cl_3_7_Table_2[0]["outstanding_leg_in_back_to_back_in_a_double_angle_member"] <= 9.4 * e:
            return "class1"
        elif cl_3_7_Table_2[0]["outstanding_leg_in_back_to_back_in_a_double_angle_member"] > 9.4 * e and \
                cl_3_7_Table_2[0]["outstanding_leg_in_back_to_back_in_a_double_angle_member"] <= 10.5 * e:
            return "class2"
        elif cl_3_7_Table_2[0]["outstanding_leg_in_back_to_back_in_a_double_angle_member"] > 10.5 * e and \
                cl_3_7_Table_2[0]["outstanding_leg_in_back_to_back_in_a_double_angle_member"] <= 15.7 * e:
            return "class3"
        elif cl_3_7_Table_2[0][
            "outstanding_leg_of_an_angle_with_its_back_in_cont_contact_with_another_component"] <= 9.4 * e:
            return "class1"
        elif cl_3_7_Table_2[0][
            "outstanding_leg_of_an_angle_with_its_back_in_cont_contact_with_another_component"] > 9.4 * e and \
                cl_3_7_Table_2[0][
                    "outstanding_leg_of_an_angle_with_its_back_in_cont_contact_with_another_component"] <= 10.5 * e:
            return "class2"
        elif cl_3_7_Table_2[0][
            "outstanding_leg_of_an_angle_with_its_back_in_cont_contact_with_another_component"] > 10.5 * e and \
                cl_3_7_Table_2[0][
                    "outstanding_leg_of_an_angle_with_its_back_in_cont_contact_with_another_component"] <= 15.7 * e:
            return "class3"
        elif cl_3_7_Table_2[0]["stem_of_tsection_rolled_or_cut_from_a_rolled_IorH_section"] <= 8.4 * e:
            return "class1"
        elif cl_3_7_Table_2[0]["stem_of_tsection_rolled_or_cut_from_a_rolled_IorH_section"] > 8.4 * e and \
                cl_3_7_Table_2[0]["stem_of_tsection_rolled_or_cut_from_a_rolled_IorH_section"] <= 9.4 * e:
            return "class2"
        elif cl_3_7_Table_2[0]["stem_of_tsection_rolled_or_cut_from_a_rolled_IorH_section"] > 9.4 * e and \
                cl_3_7_Table_2[0]["stem_of_tsection_rolled_or_cut_from_a_rolled_IorH_section"] <= 18.9 * e:
            return "class3"
        elif cl_3_7_Table_2[0]["circular_hollow_tube_including_welded_tube_subjected_to"][0] <= 42 * e * e:
            return "class1"
        elif cl_3_7_Table_2[0]["circular_hollow_tube_including_welded_tube_subjected_to"][0] > 42 * e * e and \
                cl_3_7_Table_2[0]["circular_hollow_tube_including_welded_tube_subjected_to"][0] <= 52 * e * e:
            return "class2"
        elif cl_3_7_Table_2[0]["circular_hollow_tube_including_welded_tube_subjected_to"][0] > 52 * e * e and \
                cl_3_7_Table_2[0]["circular_hollow_tube_including_welded_tube_subjected_to"][0] <= 146 * e * e:
            return "class3"
        elif cl_3_7_Table_2[0]["circular_hollow_tube_including_welded_tube_subjected_to"][1] <= 88 * e * e:
            return "class3"
        elif cl_3_7_Table_2[0]["web_of_an_I_or_H_section"]["general"] <= 84 * e / (1 + r1):
            return "class1"
        elif r1 < 0 and cl_3_7_Table_2[0]["web_of_an_I_or_H_section"]["general"] <= 105 * e / (1 + r1) and \
                cl_3_7_Table_2[0]["web_of_an_I_or_H_section"]["general"] > 84 * e / (1 + r1):
            return "class2"
        elif r1 > 0 and cl_3_7_Table_2[0]["web_of_an_I_or_H_section"]["general"] <= 105 * e / (1 + 1.5 * r1) and \
                cl_3_7_Table_2[0]["web_of_an_I_or_H_section"]["general"] > 84 * e / (1 + r1):
            return "class2"
        elif cl_3_7_Table_2[0]["web_of_an_I_or_H_section"]["general"] <= 126 * e / (1 + 2 * r1) and \
                cl_3_7_Table_2[0]["web_of_an_I_or_H_section"]["general"] > 105 * e / (1 + r1):
            return "class3"
        elif cl_3_7_Table_2[0]["web_of_an_I_or_H_section"]["axial_compression"] <= 42 * e:
            return "class3"


    # Table 3 Maximum slendernesss ratio
    """ Table 5 gives the maximum effective slenderness ratio (KL/r) according to member type 
           Slenderness ratio=KL/r
           KL:effective length of the member
           r:appropriate radius of gyration based on effective section
           Member types relating cases:
           case1:A member carrying compressive loads from dead loads and imposed loads
           case2:A tension member in which a reversal of direct stress occur dueto loads other than wind or seismic loads
           case3:A member subjected to compression forces resulting only from combination with wind/earthquake actions,
                 provided deformations does not adversely affect the stress in any part of the structure
           case4:Compression flange of a beam  against lateral torsional buckling
           case5:A member normally acting as tie in a roof truss or a bracing system not considered effective when
                 when subjected to possible reversal of stress into compression resulting from action of wind or earthquake 
                  forces
           case6:Members always under tension(other than pre-tensioned members)"""

    cl_3_8_Table_3 = {"case1": 180,
                      "case2": 180,
                      "case3": 250,
                      "case4": 300,
                      "case5": 350,
                      "case6": 400}
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


    # DESIGN OF TENSION MEMBER
    # cl 6.1 Tension
    @staticmethod
    def cl_6_1_Design_strength_of_tesion_member(T_dg, T_dn, T_db):
        """
            Calculation of Design Strength of the member as per cl.6.1
        Args:
            T_dg - design strength due to yielding of gross section in N (float),
            T_dn - design rupture strength of critical section in N (float),
            T_db - design strength due to block shear in N (float)

        Return:
            T_d -   design strength of the number under axial tension in N (float),
        Note:
            References:
            IS800:2007,cl.6.1
        """
        T_d = min(T_dg, T_dn, T_db)
        return T_d


    #cl.6.2 Design Strength due to yielding of Gross Section
    @staticmethod
    def cl_6_2_Design_strength_of_member_due_to_yielding_of_gross_section(A_g, f_y):
        """
            Calculate the design strength due to yielding of gross section as per cl.6.2
        Args:
            A_g- Gross area of cross section[in sq.mm](float)
            f_y- Yield stress of the material in Mpa (float)

        Return:
            T_dg - Design strength of member due to yielding of gross section in N(float)


        Note:
            Reference:
            IS 800:2007, cl.6.2
        """

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        T_dg = A_g * f_y / gamma_m0
        return T_dg


    # cl.6.3 Design Strength Due to Rupture of Critical Section
    # cl.6.3.1 Plates
    @staticmethod
    def cl_6_3_1_design_strength_in_tension(b, n, d_h, p_s, g, f_u, t):
        """
            Calculate the design strength in tension of a plate as per cl.6.3.1
        Args:
            A_n- net effective area of the member[in sq.mm](float)
            f_u- ultimate stress of the material in Mpa(float)
            b,t- width and thickness of the plate,respectively[in mm](float)
            d_h- diameter of the bolt hole[2mm in addition to the diameter of the hole,
                    in case the directly punched holes[in mm](float)
            g-  gauge length between the bolt holes[in mm](float list)
            p_s- staggered pitch length between line of bolt holes[in mm](float list)
            n- number of bolt holes in the critical section (int)

        Return:
            T_dn - design strength in tension of a plate in N(float)

        Note:
            Reference:
            IS 800:2007, cl.6.3.1
        """

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        sum_value = 0
        for i in range(n - 1):
            sum_value += (p_s[i] * p_s[i]) / (4 * g[i])

        A_n = (b - n * d_h + sum_value) * t
        T_dn = 0.9 * A_n * f_u / gamma_m1
        return T_dn


    # cl.6.3.2 Threaded Rods
    @staticmethod
    def cl_6_3_2_design_strength_of_threaded_rods_in_tension(A_n, f_u):
        """
            Calculate the design strength of threaded rods in tension as per cl.6.3.2

        Args:
            A_n- net root area at the threaded section [in sq.mm](float)
            f_u- ultimate stress of the material in Mpa(float)

        Return:
               T_dn - design strength of threaded rods in tension in N(float)

        Note:
            Reference:
            IS800:2007, cl.6.3.2
        """

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_dn = 0.9 * A_n * f_u / gamma_m1
        return T_dn


    # cl.6.3.3 Single Angles
    @staticmethod
    def cl_6_3_3_design_strength_of_an_angle_connected_through_one_leg(A_nc, f_u, w, t, f_y, b_s, L_c, A_go):
        """
            Calculation of design strength of an angle connected through one leg as per cl.6.3.3

        Args:
            w -   outstanding leg width in mm(float)
            b_s -  shear lag width in mm(float)
            L_c - length of the end connection, that is the distance between the outermost
                    bolts in the end joint measured along the load direction or length of the weld
                    along the load direction in mm(float)
            A_nc - net area of the connected leg[in sq. mm](float)
            A_go - gross area of the outstanding leg[in sq. mm](float)
            t -    thickness of the leg in mm(float)
            f_u-  ultimate strength of material in Mpa(float)

        Return:
            T_dn - design strength of an angle connected through onw leg in N(float)

        Note:
            Reference:
            IS800:2007, cl.6.3.3

        """

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

        X = max(0.7, f_u * gamma_m0 / f_y * gamma_m1)
        beta = min(X, 1.4 - 0.076 * (w / t) * (f_y / f_u) * (b_s / L_c))
        T_dn = (0.9 * A_nc * f_u / gamma_m1) / (beta * A_go * f_y / gamma_m0)
        return T_dn


    # cl 6.3.3 For preliminary sizing
    @staticmethod
    def cl_6_3_3_1_design_strength_of_net_section(n, A_n, f_u):
        """
        Calculation of rupture strength of net section for preliminary sizing as per cl.6.3.3

        Args:
            A_n - net area of the total cross-section[in sq.mm](float)
            f_u - ultimate tensile strength pf material in Mpa(float)
            n  -  number of bolts (int)

        Return:
            T_dn - design strength of net section for preliminary sizing in N(float)

        Note:
            Reference:
            IS800:2007 cl.6.3.3
        """
        if n in [1, 2]:
            alpha = 0.6
        else:
            if n == 3:
                alpha = 0.7
            else:
                alpha = 0.8

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_dn = alpha * A_n * f_u / gamma_m1
        return T_dn


    #cl.6.3.4 Other Section
    #cl.6.4.1 Block shear strength of bolted connections
    @staticmethod
    def cl_6_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """
            Calculation of the block shear strength of bolted connection as per cl.6.4.1

        Args:
            A_vg - Minimum gross in shear along bolt line parallel to external force [in sq.mm](float)
            A_vn - Minimum net area in shear along bolt line parallel to external force[in sq.mm](float)
            A_tg - Minimum gross area in tension from the bolt hole to the toe of the angle,
                    end bolt line, perpendicular to the line of force, respectively [ in sq.mm](float)
            A_tn - Minimum net area in tension from the bolt hole to the toe of the angle,
                    end bolt line, perpendicular to the line of force, respectively [in sq.mm]
            f_u -  Ultimate stress of the plate ,material in Mpa(float)
            f_y -  Yield stress of the plate material in Mpa(float)

        Return:
            T_db - block shear strength of bolted connection in N (float)

        Note:
            Reference:
            IS800:2007, cl.6.4.1
        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1

        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        T_db = min(T_db1, T_db2)

        return T_db

    # ==========================================================================
    """    SECTION  7     DESIGN OF COMPRESS1ON MEMBERS   """

    # cl 7.1 Design Strength
    # cl.7.1.2
    @staticmethod
    def cl_7_1_2_design_copmressive_strength_of_a_member(A_c, f_cd):
        """
            Calculation of design compressive strength
        Args:
            A_c - Effective sectional area (in square mm)
            f_cd - Design Compressive stress(in N)

        Return:
            P_d - Design  Compressive Strength of a member (in N)

        Note:
            References:
            IS800:2007 cl.7.2
        """

        P_d = f_cd * A_c
        return P_d
        
    
    # cl 7.1.2.1 design compressive stress of axially loaded member
    @staticmethod
    def cl_7_1_2_1_design_compressive_stress(K_L,alpha,E,f_y,r,gamma_m0):
        """
            Calculation of design compressive stress
        Args:
                K_L  - Effective length of compression member in mm
                alpha - Imperfection factor
                E - Young's Modulus of Elasticity in N/mm**2
                f_y - Yield Stress in N/mm**2
                r - radius of gyration in mm

            Return:
                f_cd - Design  strength of compression member in N/mm**2

            Note:
                Reference:
                IS 800:2007, cl.7.1.2.1
        """
        
        f_cc = (math.pi ** 2 * E) / (K_L / r) ** 2  #euler buckling stress
        lambda_ = math.sqrt(f_y / f_cc)  #non-dimensional slenderness ratio
        phi = 0.5 * (1 + alpha * (lambda_ - 0.2) + lambda_ **2)
        srf = 1 / (phi + math.sqrt(phi ** 2 - lambda_ ** 2))  #stress reduction factor,kai
        f_cd = min( f_y / gamma_m0 * srf, f_y / gamma_m0)
        return f_cd


    # cl 7.1.2.2 Calculation of buckling class of given cross-section
    @staticmethod
    def cl_7_1_2_2_Table_10_Buckling_class_of_cross_section(Cross_section,t_f,t_w,h,b_f):
        """
            Defining Buckling Class of Cross-Section
        Args:
            Cross_section - Either 'Rolled_I_Section' or 'Welded_I_Section'
                            or 'Hot_rolled_hollow' or 'cold_Formed_hollow' or 'Welded_Box_Section'
                            or 'Channel,Angle,T,Solid Section' or 'Built_up_Member'

            h- Depth of the section in mm
            b_f - width of flange or width of section in case of welded box section(mm)
            t_f - Thickness of flange in mm
            t_w - Thickness of web in mm

        Return:
            Dictionary of Buckling axis and Buckling class with Buckling axis as key

        Note:
            Reference:
            IS 800:2007, cl.7.1.2.2, Table_10
        """
        if Cross_section == "Rolled_I_Section":
            if h / b_f > 1.2 :
                if t_f <= 40:
                    return {'z-z': 'a','y-y': 'b'}

                if t_f>40 and t_f<=100:
                    return {'z-z': 'b','y-y': 'c'}

            if h / b_f <= 1.2:
                if t_f <= 100:
                    return {'z-z': 'b','y-y': 'c'}

                if t_f>100:
                    return {'z-z': 'd','y-y': 'd'}

        if Cross_section == "Welded_I_Section":
            if t_f <= 40:
                return {'z-z': 'b','y-y': 'c'}
            if t_f>40:
                return {'z-z': 'c','y-y': 'd'}

        if Cross_section == "Hot_rolled_hollow":
            return {'z-z': 'a','y-y': 'a'}

        if Cross_section == "cold_Formed_hollow":
            return {'z-z': 'b','y-y': 'b'}

        if Cross_section == "Welded_Box_Section":
            Buckling_Class_1 = 'b'
            Buckling_Class_2 = 'b'
            
            if b_f / t_f < 30:
                Buckling_Class_1 = "c"
                
            if h / t_w < 30:
                Buckling_Class_2 = "c"
            
            return {'z-z': Buckling_Class_1,'y-y': Buckling_Class_2}
            
        if Cross_section == "Channel_Angle_T_Solid_Section" or Cross_section == "Built_up_Member":
            return {'z-z': 'c','y-y': 'c'}
            

    #Imperfection Factor, alpha
    # alpha for a given buckling class,'a','b','c' or 'd'
    cl_7_1_Table_7_alpha = {
        'a': 0.21,
        'b': 0.34,
        'c': 0.49,
        'd': 0.76,
    }

    #Table 11 Effective Length of Prismatic Compression Members
    @staticmethod
    def cl_7_2_2_table11_effective_length_of_prismatic_compression_members(L,BC=[]):

        """
            Effective length of Prismatic Compression Member when the boundary conditions in the plane of buckling
            can be assessed

        Args:
            BC - linked list of Boundary Conditions
                 =[BC_translation_end1,BC_rotation_end1,BC_translation_end2,BC_rotation_end2]
            L -  Length of the Compression member in mm

        Return:
            K_L - Effective length of Compression Member in mm

        Note:
            Reference:
            IS 800:2007, cl.7.2.2, Table_11
        """

        if BC == ['Restrained','Restrained','Free','Free'] or BC == ['Restrained','Free','Free','Restrained']:K_L = 2.0 * L
        elif BC == ['Restrained','Free','Restrained','Free']:K_L = L            
        elif BC == ['Restrained','Restrained','Free','Restrained']:K_L = 1.2 * L 
        elif BC == ['Restrained','Restrained','Restrained','Free']:K_L = 0.8 * L
        elif BC == ['Restrained','Restrained','Restrained','Restrained']:K_L = 0.65 * L
        return K_L


    # cl 7.1.2.1 design compressive stress of axially loaded member
    @staticmethod
    def design_compressive_stress(f_y, r ):

        """
            Calculation of design compressive stress
            Args:
                K_L  - Effective length of compression member in mm
                alpha - Imperfection factor
                E - Young's Modulus of Elasticity in N/mm**2
                f_y - Yield Stress in N/mm**2
                r - radius of gyration of the section in mm

            Return:
                f_cd - Design  strength of compression member in N/mm**2

            Note:
                Reference:
                IS 800:2007, cl.7.1.2.1
        """
        Buckling_Class = cl_7_1_2_2_Table_10_Buckling_class_of_cross_section(Cross_section, h, b_f, t_f)
        alpha = cl_7_1_Table_7_alpha["Buckling_Class"]["alpha"]
        K_L = cl_7_2_2_effective_length_of_prismatic_Compression_members(At_one_end_Translation, At_one_end_Rotation,
                                                                         At_other_end_Translation,
                                                                         At_other_end_Rotation, L)
        f_cc = (pi * pi * E) / (K_L / r) ** 2
        lambda_c = math.sqrt(f_y / f_cc)
        phi = 0.5 * (1 + (alpha * (lambda_c - 0.2)) + (lambda_c * lamda_c))
        srf = 1 / (phi + math.sqrt(phi ** 2 - lambda_c ** 2))
        f_cd = min(((f_y / gamma_m0) * srf), f_y / gamma_m0)
        return f_cd


    # Design of Column Base
    #cl.7.4.3 thickness of column base
    @staticmethod
    def cl_7_4_3_1_Calculation_of_thickness_of_column_base(w,a,b,t_f,f_y):

        """
            Calculation of thickenss of Column base
        Args:
            w - uniform pressure from below on the slab base in mm
            a - Larger Projection in mm
            b - Smaller Projection in mm
            f_y - Yield Stress in N/mm**2
            t_f - Thickness of flange of Compression member in mm

        Return:
            t_f - thickness of rectangular slab column base in mm

        Note:
            Reference:
            IS 800:2007  cl.7.4.3.1,


        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yield_stress']
        t_s = max(t_f, math.sqrt(2.5 * w * (a ** 2 - 0.3 * b ** 2) * gamma_m0 / f_y))
        return t_s
        
    #cl.7.5.1.2 Loaded through one angle
    #Table 12 - evaluation of constants K1,K2,K3 for effective slenderness ratio
    @staticmethod
    def cl_7_5_1_2_table12_constant_K_1_K_2_K_3(No_of_Bolts_at_Each_End_Connection, Connecting_member_Fixity):

        """Value of constant K_1,K_2, K_3
        Args:
            No_of_Bolts_at_Each_End_Connection -  Either more than 2 or 1,
            Fixity - Either Fixed or Hinged.

        Return:
            [K_1,K_2,K_3]

        Note:
            Reference:
            IS 800:2007 cl.7.5.1.2


        """

        if No_of_Bolts_at_Each_End_Connection >= 2:
            if Connecting_member_Fixity == "Fixed":
                K_1 = 0.20
                K_2 = 0.35
                K_3 = 20
                
            elif Connecting_member_Fixity == "Hinged":
                K_1 = 0.70
                K_2 = 0.60
                K_3 = 5

        if No_of_Bolts_at_Each_End_Connection == 1:
            if Connecting_member_Fixity == "Fixed":
                K_1 = 0.75
                K_2 = 0.35
                K_3 = 20

            if Connecting_member_Fixity == "Hinged":
                K_1 = 1.25
                K_2 = 0.50
                K_3 = 60
                
        return [K_1,K_2,K_3]

    #cl.7.5.1.2.Design strength of angle strut loaded through one leg
    @staticmethod
    def cl_7_5_1_2_Calculation_of_design_strength_of_single_angle_strut_loaded_through_one_leg(L, b_1, b_2, f_y, r_vv, t, E,K_list):
        """
            Calculation of design strength of single angle strut loaded through one leg

        Args:
            L - Length of Angle section in mm
            b_1,b_2 - width of legs of angle section in mm
            f_y - yield stress in N/mm**2
            r_vv - radius of gyration about minor axis in mm
            t - thickness of the leg in mm
            E - Young's Modulus of elasticity in N/mm***2
            epsilon  -  yield stress ratio

        Return:
            f_cd - Design compressive strength of the section

        Note:
            Reference:
            IS 800:2007  cl.7.5.1.2

        """
        [K_1,K_2,K_3] = K_list
        
        alpha = 0.49 #according to ammendment 1

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        epsilon = math.sqrt(250 / f_y)

        lambda_vv = (L / r_vv) / (epsilon * math.sqrt(math.pi ** 2 * E / 250))

        lambda_phi = (b_1 + b_2) / (2 * t * epsilon * math.sqrt(math.pi * math.pi * E / 250))

        lambda_e = math.sqrt(K_1 + (K_2 * lambda_vv ** 2) + (K_3 * lambda_phi ** 2))

        phi = 0.5 * (1 + alpha * (lambda_e - 0.2) + lambda_e ** 2)
        f_cd = min(f_y / (gamma_m0 * (phi + math.sqrt(phi ** phi - lambda_e ** 2))), f_y / gamma_m0)

        return f_cd
        
    #cl7.6 Laced column
    #cl 7.6.1.5.Effective slenderness ratiion of lacing member
    @staticmethod
    def effective_slenderness_ratio_of_lacing_member(K_L, r_min):
        """
            Calculation of Effective slenderness ratio of lacing member
            to account for shear deformation
        Args:
            K_L -effective length of column in mm
            r_min - radius of gyration of column member in mm
            SR_0 - actual maximum slenderness ration of column
        Returns:
            SR_eff - effective slenderness ratio of lacing
        Note:
            Reference:
            IS 800:2007  cl 7.6.1.5
        """

        SR_0 = K_L/r_min
        SR_eff = 1.05*SR_0
        return SR_eff

    #cl 7.6.2 Width of Lacing  Bars
    @staticmethod
    def cl_7_6_2_width_of_lacing_bars(d):
        """
        Calculation of min width of Lacing  Bars
        Args:
            d - nominal bolt/rivet diameter
        Returns:
            w_min - min Width of Lacing  Bars
        Note:
            Reference:
            IS 800:2007, cl 7.6.2
        """

        w_min = 3*d
        return w_min

    #cl 7.6.3 Thickness of Lacing Bars
    @staticmethod
    def cl_7_6_3_minimum_thickness_of_lacing_bars(lacing_type,L_eff):
        """
            Calculation of  min Thickness of Lacing Bars
        Args:
            Lacing_type - either 'single_lacing' or 'double_lacing'
            L_eff - effective length of lacing bars
        Returns:
            t_min - minimum thickness of Lacing Bars
        Note:
            Reference:
            IS 800:2007, cl 7.6.3
        """
        if lacing_type == 'single_lacing':
            t_min = 1/40 *L_eff

        else:
            t_min = 1 / 60 * L_eff

        return t_min

    #Cl7.6.6 Design of lacing
    #7.6.6.1 Transverse shear in the lacing bar
    @staticmethod
    def cl_7_6_6_1_transverse_shear_in_the_lacing_bar(P):
        """
            Calculation of Transverse shear in the lacing bar
        Args:
            P  -  axial load on column in N
        Returns:
            V_t_min - minimum design transverse shear in N
        Note:
            Reference:
            IS 800:2007 cl 7.6.6.1
        """
        V_t_min = 2.5/100 * P
    
        return V_t_min


    # cl7.7  Batten plate
    # cl7.7.1.4 effective slenderness ratio of batten plate
    @staticmethod
    def Cl_7_7_1_4_effective_slenderness_ratio_of_batten_plate(K_L,r_min):
        """
        Calculation of effective slenderness ratio
        Args:
            K_L -effective length of column in mm
            r_min - minimum radius of gyration(r_x,r_y,r_z) of column member in mm
        Returns:
            SR_eff - effective slenderness ratio of lacing
        Note:
            Reference:
            IS 800:2007, cl 7.6.1.5

        """
        SR_eff = 1.1 * (K_L / r_min)
        return SR_eff

    # Design of Battens
    # Battens
    @staticmethod
    def cl_7_7_2_1_longitudinal_shear_transverse_shear_and_moment_at_connection(P, S, C, N):
        """
            Calculation of longitudinal shear, transverse shear and moment at connetion
            Args:
                P - total axial force on column in N
                S - minimum transverse distance between the centroid of the rivet/bolt
                    group/welding connecting the batten to the main member in mm
                N  -number of parallel planes of battens
                C  -  distance between centre -to- centre of battens in mm
            Returns:
                V_t - transverse shear force in N
                V_b - longitudinal shear force along column axis in N
                M - moment at connection in N*mm
            Note:
                Reference:
                IS 800:2007, cl.7.7.2.1
        """

        V_t = 2.5 / 100 * P
        V_b = V_t * C / (N * S)
        M = V_t * C / (N * 2)
        return (V_t, V_b, M)

    # ==========================================================================
    """    SECTION  8     DESIGN OF MEMBERS SUBJECTED TO BENDING   """
    # -------------------------------------------------------------
    # DESIGN OF MEMBER SUBJECTED TO BENDING

    # cl 8.3.3 Effective length for cantilever Beam
    @staticmethod
    def cl_8_3_3_Table_16_Effective_length_for_cantilever_beam(L, Restraint_Condition_1, Restraint_Condition_2,
                                                              Loading_condition):
        """
            Calculate effective length for cantilever beam of projecting length L as per cl.8.3.3

            Args:
                L - Projecting Length of cantilever beam in mm (float)

        Args:
            L - Projecting Length of cantilever beam in mm (float)
            D -  Overall depth of he beam in mm (float)

            Restrained_condition - Either "At support" or "At Top"
            Restraint_Condition_1- "At support"
            Restraint_Condition_2- "At Top"

                At_support -  Either "Continuous, with lateral restraint to top"
                              or "Continuous, with  partial torsional restraint"
                              or "Continuous, with lateral and torsional restraint "
                              or "Restrained laterally,torsionally and against rotation on plan "

                At_top - Either  "Free"
                        or "Lateral restraint to top flange"
                        or "Torsional restraint"
                        or  "Lateral and torsional restraint"

                Loading_condition - Either "Normal" or  "Destabilizing"

            Returns:
                L_LT =  cl_8_3_3_Table_16_Effective_length_for_cantilever_beam
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
            if Restraint_Condition_2 == "Lateral restraint to top flange":
                if Loading_condition == "Normal":
                    return 1.8 * L
                else:
                    return 5.0 * L
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return 1.6 * L
                else:
                    return 3.0 * L
            if Restraint_Condition_2 == "Lateral and Torsional restraint":
                if Loading_condition == "Normal":
                    return 1.4 * L
                else:
                    return 2.4 * L
        if Restraint_Condition_1 == "Continuous,with lateral and torsional restraint":
            if Restraint_Condition_2 == "Free":
                if Loading_condition == "Normal":
                    return 1.0 * L
                else:
                    return 2.5 * L
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
            if Restraint_Condition_2 == "Lateral and Torsional restraint":
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


    @staticmethod
    def cl_8_3_1_Table_15_Effective_length_for_simply_supported_beams(L,D, Restraint_Condition_1,
                                                                      Restraint_Condition_2, Loading_Condition):
        """
            Calculate effective length against lateral torsional buckling for simply supported Beams and girders
            where no lateral restraint  to the compression flange is provided as per cl.8.3.1

            Args:
                L -  Span of simply supported beams and girders in mm (float)
                D -  Overall depth of he beam in mm (float)

                Restraint_Condition - Either "Torsional Restraint" or "warping Restraint"
                Restraint_Condition_1- "Torsional Restraint"
                Restraint_Condition_2- "Warping Restraint"

                "Torsional Restrained" - Either "Fully restrained" or
                                        "Partially restrained by bottom flange support connection" or
                                        "Partially restrained by bottom flange bearing support"

                "Warping_Restraint" - Either "Both flanges fully restrained" or
                                     "Both flanges partially restrained" or
                                     "Compression flange fully restrained" or
                                     "Compression flange partially restrained" or
                                     "Warping not restrained in both flange"


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

            if Restraint_Condition_2 == "Warping not restrained in both flanges":
                if Loading_Condition == "Normal":
                    return 1.00 * L
                else:
                    return 1.20 * L
        if Restraint_Condition_1 == "Partially restrained by bottom flange support connection":
                if Restraint_Condition_2 == "Warping not restrained in both flanges":
                    if Loading_Condition == "Normal":
                        return 1.00 * L + 2 * D
                    else:
                        return 1.20 * L + 2 * D
        if Restraint_Condition_1 == "Partially restrained by bottom flange bearing support":
                if Restraint_Condition_2 == "Warping not restrained in both flanges":
                    if Loading_Condition == "Normal":
                        return 1.2 * L + 2 * D
                    else:
                        return 1.4 * L + 2 * D


    @staticmethod
    def cl_8_3_Effective_length_against_torsional_restraint(L, D, Beam_type, Restraint_Condition_1,
                                                            Restraint_Condition_2,
                                                            Loading_Condition):
        """
            Calculation of effective length for given type of beam type as per cl.8.3

        Args:

            L-  Span of simply supported beams and girders in mm (float) for
                "Simply_supported_with_no_lateral_restrained_to_the_compression_flanges",
                 Projecting Length of cantilever beam in mm (float) for
                 "Cantilever_beam",
                 Length of relevant segment between the lateral restraint in mm (float) for
                 "Simply_supported_with_intermediate_lateral_restraints",
                 Centre-to-centre distance of the restraint member in mm (float) for
                 'Beam provided with members to give effective lateral restraint to compression flange at interval'

            Beam_type - Either "Simply_supported_with_no_lateral_restrained_to_the_compression_flanges"
                        or "Simply_supported_with_intermediate_lateral_restraints"
                        or "Beam_provided_with_members_to_give_effective_lateral_restrain_to_compression_flange_at_interval"
                        or "Cantilever_beam"

            FOR "Simply_supported_with_no_lateral_restrained_to_the_compression_flanges"
            Restraint_Condition - Either "Torsional Restraint" or "warping Restraint"

            Restraint_Condition - Either "Torsional Restraint" or "Warping Restraint"
            Restraint_Condition_1- "Torsional Restraint"
            Restraint_Condition_2- "Warping Restraint"


            "Torsional Restrained" - Either "Fully restrained" or
                                        "Partially restrained by bottom flange support connection" or
                                        "Partially restrained by bottom flange bearing support"

            "Warping_Restraint" - Either "Both flange fully restrained" or
                                     "Compression flange fully restrained" or
                                     "Compression flange partially restrained" or
                                     "Warping not restrained in both flange"


            FOR "Cantilever_beam":

            Restrained_condition - Either "At support" or "At Top" for "Cantilever_beam"

            Restraint_Condition_1- "At support"
            Restraint_Condition_2- "At Top"

            At_support -  Either "Continuous, with lateral restraint to top"
                              or "Continuous, with  partial torsional restraint"
                              or "Continuous, with lateral and torsional restraint "
                              or "Restrained laterally,torsionally and against rotation on plan "

            At_top - Either "free"
                        or "lateral restraint to top flange"
                        or "Torsional restraint"
                        or  "Lateral and torsional restraint"

            Loading_condition - Either "Normal" or  "Destabilizing"



        Returns :
            L_LT - effective_length_of_beam in mm (float)

        Note:
            References:
            IS800:2007,  cl 8.3.

        """

        if Beam_type == "Simply_supported_with_no_lateral_restrained_to_the_compression_flanges":
            L_LT = IS800_2007.cl_8_3_1_Table_15_Effective_length_for_simply_supported_beams(L, D, Restraint_Condition_1,
                                                                                 Restraint_Condition_2,
                                                                                 Loading_Condition)
        elif Beam_type == 'Simply supported with intermediate lateral restraints':
            L_LT = 1.2 * L

        elif Beam_type == "Beam_provided_with_members_to_give_effective_lateral_restrain_to_compression_flange_at_interval":
            L_LT = 1.2 * L #TODO:doubt-check
        else:
            L_LT = IS800_2007.cl_8_3_3_Table_16_Efective_length_for_cantilever_beam(L, Restraint_Condition_1,
                                                                         Restraint_Condition_2, Loading_Condition)

        return L_LT

    # Design Strenth in Bending(Flexure)
    @staticmethod
    def cl_8_2_Design_strength_in_bending(M, M_d):
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

        return bool(M <= M_d)


    @staticmethod
    def cl_8_2_Design_bending_strength_of_laterally_unsupported_beam(z_p, z_e, f_y, v, v_d, m_dv, plastic=False,
                                                              compact=False):
        """Calculation of bending strength of laterally unsupported beam for low shear  and high shear case
            Args:
                beta_b - 1 for plastic and compact
                         Z_e/Z_p for semi-compact
                z_e - Elastic section modulus of the cross section in mm**3
                z_p - Plastic section modulus of the cross section in mm**3
                f_y - yield stress of the material (in N/ mm**2 )
                v  - Factored design shear strength in N
                v_d - Design shear strength in N
                m_dv - Design bending strength under high shear as defined in Cl 9.2 in N*m
                plastic - True if beam is plastic else False
                compact - True for compact section else False

            Returns:
                m_d - Design Bending  strength in N*m
            Note:
                References:
                IS800:2007,  cl 8.2.1.2, cl. 8.2.1.3

        """
        beta_b = z_e / z_p #semi-compact section
        if plastic is True:
            beta_b = 1
        if compact is True:
            beta_b = 1
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        if v <= 0.6 * v_d:
            m_d = beta_b * z_p * f_y / gamma_m0


        if v > 0.6 * v_d:
            m_d = m_dv
        return m_d

    # cl8.2.2 DESIGN BENDING STRENGTH OF LATERALLY UNSUPPORTED BEAMS
    # cl8.2.2.1 Elastic lateral torsional buckling moment
    @staticmethod
    def cl_8_2_2_1_Elastic_lateral_torsional_buckling_moment_doubly_symmetric(I_t, I_w, I_y, E, G, L_LT):
        """
            Calculation of elastic critical moment of lateral torsional buckling for simply supported, prismatic members
            with symmetric c/s
            Args:

                I_t - torsional constant
                I_w - warping constant
                I_y - moment of inertia about weaker axis
                E - Young's Modulus of Elasticity
                G - modulus of rigidity
                L_LT - effective length for lateral torsional buckling
            Return:
                M_cr - Elastic lateral torsional buckling moment in N*mm
            Notes:
                Reference:
                IS 800:2007, cl. 8.2.2.1.

        """


        M_cr = math.sqrt((math.pi ** 2 * E * I_y / L_LT ** 2) * (G * I_t + math.pi ** 2 * E * I_w / L_LT ** 2))

        return M_cr


    @staticmethod
    def cl_8_2_2_design_bending_strength_of_laterally_unsupported_beam(Z_p, Z_e, L_LT, f_y, I_y,  I_t, I_w,  E, G,section,plastic=False, compact=False):
        """
             Calculation of design bending strength of laterally unsupported beam
             Args:
                 Z_p - plastic section modulus with respect to extreme compression fibre
                 Z_e - elastic section modulud with respect to extreme compression fibre
                 L_LT - effective length for lateral torsional buckling
                 I_y - moment of inertia about minor axis of c/s
                 f_y - yield stress
                 I_t - torsional constant
                 I_w - warping constant
                 E - modulus of elasticity
                 G - modulus of rigidity
                 plastic - boolean True if section is plastic
                 compact - boolean True if section is compact
                 section - Either 'Rolled_steel_section' or "Welded_steel_section'

            Returns:
                M_d - Design bending strength of laterally unsupported beam in N*mm

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
        elif section == 'Welded_steel_Connection':
            alpha_LT = 0.49

        M_cr = IS800_2007.cl_8_2_2_1_Elastic_lateral_torsional_buckling_moment_doubly_symmetric(I_t, I_w, I_y, E, G, L_LT)
        f_cr_b = M_cr / (beta_b * Z_p)
        Lambda_LT = min(math.sqrt(f_y / f_cr_b), math.sqrt(1.2 * Z_e * f_y / M_cr))
        phi_LT = 0.5 * (1 + alpha_LT * (Lambda_LT - 0.2) + Lambda_LT ** 2)
        X_LT = min(1.0, 1 / (phi_LT + math.sqrt(phi_LT ** 2 - Lambda_LT ** 2)))


        if Lambda_LT < 0.4:
           X_LT = 1


        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

        f_bd = X_LT * f_y / gamma_m0

        M_d = beta_b * Z_p * f_bd

        return M_d


    # cl8.4 Shear Design
    @staticmethod
    def cl_8_4_design_shear_strength_of_beam(V_n):
        """
            Design shear strength
        Args:
            V_n -Nominal  shear strength of a cross-section
        Return
            V_d - Design shear strength in N
        Note:
            Reference:
            IS 800:2007, cl. 8.4

        """

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        V_d = V_n / gamma_m0
        return V_d


    @staticmethod
    def cl_8_4_1_nominal_plastic_shear_resistance_under_pure_shear(A_v, f_yw):
        """
            Calculation of nominal plastic shear resistance under pure shear

            Args:

                A_v - Shear area
                f_yw - yield shear of the web
            Returns:
                V_n - Nominal plastic shear resistance under pure shear
            Note:
                Reference:
                IS 800:2007, cl. 8.4.1
        """

        V_n = A_v * f_yw / math.sqrt(3)
        return V_n



    def cl_8_4_1_1_shear_area_of_different_section(A, b, d, h, t_f, t_w, section, Axis_of_Bending, load_application_axis,
                                               cross_section):
        """
            Calculation of shear area of different section

            Args:
                A - cross section area in mm**2
                b - overall breadth of tubular section,breadth of I - section flange in mm
                d - clear depth of the web between flange in mm
                h- overall depth of the section in mm
                t_f - thickness of the flange in mm
                t_w - thickness of the web in mm
                section - Either 'I section ' and 'Channel Section' or 'Rectangular hollow section of uniform depth'
                        or 'Circular hollow tubes of uniform thickness' or 'plates' or 'solid bars'
                Load_application_axis - Either 'Loaded parallel to depth' or 'Loaded parallel to width(b)'
                Axis_of_Bending - Either 'Major Axis Bending' or 'Minor Axis Bending'
                cross_section - Either 'Hot Rolled' or ' Welded'


            Return:
                A_v - Shear area in mm*mm

            Note:
                Reference:
                IS 800:2007, cl. 8.4.1.1

        """
        if section == 'I section' or section == 'Channel Section':
            if Axis_of_Bending == 'Major Axis Bending':
                if cross_section == 'Hot-Rolled':
                    A_v = h * t_w
                else:
                    A_v = d * t_w
            return A_v

        if Axis_of_Bending == 'Minor Axis Bending':
            if cross_section == 'Hot-Rolled' or cross_section == 'Welded':
                A_v = 2 * b * t_f
            return A_v
        if section == 'Rectangular hollow section of uniform depth':
            if load_application_axis == 'Loaded parallel to depth':
                A_v = A * h / (b + h)
            else:
                A_v = A * b / (b + h)
            return A_v

        if section == 'Circular hollow tubes of uniform thickness':
            A_v = A
            return A_v

        if section == 'plates' or section == 'solid':
            A_v = A
            return A_v


    # cl8.4.2 TODO: CHECK RESISTANCE TO SHEAR BUCKLING
    # cl8.4.2.1 Check for resistance to shear buckling
    @staticmethod
    def cl_8_4_2_shear_buckling_check(d, t_w, k_v, fy, stiffeners):
        """
            Check for resistance against shear buckling
            Args:
                d - clear depth of web between flanges
                t_w - thickness of web
                k_v -shear buckling coefficient
                fy - yield stress in N/mm^2
                stiffeners - True if web has stiffeners else False
            Return:
                check - True if check is satisfied else false
            Note:
                Reference:
                IS 800:2007, cl. 8.4.2.1
        """
        epsilon = math.sqrt(250/fy)
        if not stiffeners:
            val = 67 * epsilon

        else:
            val = 67 * epsilon * math.sqrt(k_v/5.35)
        if d / t_w > val :
            check = True
        else:
            check = False

        return check

    # cl8.4.2.2 Shear buckling design method
    @staticmethod
    def cl_8_4_shear_buckling_coeff_Kv(only_at_support, c=None, d=None):
        """
        Args:
            only_at_support - True if transverse stiffeners are provided only at support
                              else False
            c -  spacing of transverse stiffeners
            d -  depth of web
        Returns:
            k_v - shear buckling coefficient
        Note:
              Reference - IS800_2007 cl.8.4.2.1 and cl.8.4.2.2
        """
        if only_at_support:
            k_v = 5.35
        elif c / d < 1:
            k_v = 4 + 5.35 / (c / d) ** 2
        else:
            k_v = 5.35 + 4 / (c / d) ** 2
        return k_v

    @staticmethod
    def cl_8_4_2_2_nominal_shear_post_critical(A_v,k_v,mu,E,d,t_w,f_yw):
        """
        Calculates nominal shear strength as governed by buckling using simple post critical method
        Args:
            A_v - shear area defined in cl 8.4.1.1
            k_v - shear buckling coefficient
            mu - poisson's ratio
            E - modulus of elasticity
            d - depth of web
            t_w - thickness of web
            f_yw - characteristic yield stress of web material
        Return:
            V_n - nominal shear strength
        Note:
             Reference: IS800:2007 cl.8.4.2.2
        """
        T_cr_c = (k_v * math.pi ** 2 * E) / (12 * (1 - mu ** 2) * (d / t_w) ** 2)
        lambda_w = math.sqrt(f_yw / (math.sqrt(3) * T_cr_c))

        if lambda_w < 0.8:
            T_b =  (f_yw / math.sqrt(3))
        elif 0.8<lambda_w < 1.2:
            T_b = (1 - 0.8 * max((lambda_w - 0.8),0)) * (f_yw / math.sqrt(3))
        else:
            T_b = f_yw / (math.sqrt(3) * lambda_w ** 2)

        V_cr = A_v * T_b
        V_n = V_cr
        return V_n

    @staticmethod
    def cl_8_4_2_2_nominal_shear_tension_field(A_v,d,t_w,t_f,b_f,f_yw,c,f_yf,N_f):
        """
        Calculates nominal shear strength as governed by buckling using tension field method
        Args:
            A_v - shear area defined in cl 8.4.1.1
            k_v - shear buckling coefficient
            mu - poisson's ratio
            E - modulus of elasticity
            d - depth of web
            t_w - thickness of web
            t_f - thickness of flange
            b_f - width of flange
            f_yw - characteristic yield stress of web material
            c - spacing of stiffeners in web
            f_yf - characteristic yield stress of flange material
            N_f - axial force in flange due to to overall bending and external axial force
        Return:
            Note: Reference - IS800:2007 cl.8.4.2.2
        """
        if c/d < 1.0:
            return 'error : c/d must be greater than or equal to 1'

        phi = math.atan(d / c) / 1.5
        psi = 1.5 * T_b * math.sin(2 * phi)

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        M_fr = 0.25 * b_f * t_f ** 2 * f_yf * (1 - (N_f / (b_f * t_f * f_yf / gamma_m0)) ** 2)

        s = min(c, (2 / math.sin(phi) * math.sqrt(M_fr / f_yw * t_w)))
        s_c = s
        s_t = s
        w_tf = d * math.cos(phi) - (c - s_c - s_t) * math.sin(phi)
        f_v = math.sqrt(f_yw ** 2 - 3 * T_b ** 2 + psi ** 2) - psi
        V_p = A_v * f_yw / math.sqrt(3)
        V_tf = min(V_p, (A_v * T_b + 0.9 * w_tf * t_w * f_v * math.sin(phi)))
        V_tf = V_n
        return V_n



    # Stiffened web Panels
    # End plate Design
    # cl8.5.3 Anchor forces
    @staticmethod
    def cl_8_5_3_anchor_forces(d, t, f_y, V, V_cr, V_tf):
        """ Calculation of resultant longitudinal shear and moment
            Args:
                d - web depth in mm
                t - thickness of the section in mm
                f_y - yield stress in N/mm**2
                V_cr - critical shear strength as defined in cl8.4.2.2.
                V_tf - basic shear strength as defined in cl8.4.2.2.

                V - actual factored shear force
            Return:
                M_tf - resultant longitudinal moment in N*mm
                R_tf - resultant longitudinal shear in N*mm

            Note:
                Reference:
                IS 800:2007, cl. 8.5.3
        """

        V_p = d * t * f_y / math.sqrt(3)

        H_q = 1.25 * V_p * math.sqrt(1 - V_cr / V_p)

        if V < V_tf:
            H_q *= (V - V_cr) / (V_tf - V_cr)


        R_tf = H_q / 2
        M_tf = H_q * d / 10

        return (R_tf, M_tf)

    # cl8.6 Design of Beams and Plate Girders with Solid Webs
    # cl8.6.1Minimum Web Thickness
    # cl8.6.1.1 Serviceability requirement
    @staticmethod
    def cl_8_6_1_1_minimum_web_thickness(d, t_w, c, f_yw, serviceability_requirement, web_connection_to_flange):
        """
            Checking the serviceability requirement of  minimum thickness of web
            Args:
                d - web depth in mm
                t_w - thickness of web in mm
                c - spacing of transverse stiffener in mm
                epsilon_w - yield stress ratio of web
                f_yw - yield stress of the web in N/mm**2
                serviceability_requirement - 'transverse_stiffener_not_provided',
                                             'only_transverse_stiffeners_provided_in_web_flange_connection_along_both_longitudinal_edges'
                                             'transverse_and_longitudinal_stiffener_at_one_level_as_cl_8_7_13'
                                             'second_longitudinal_stiffener_provided_at_NA'
                web_connection_to_flange - 'along_both_longitudinal_edges'
                                           'along_one_longitudinal_edge'
>
            Return:
                True, if safety condition is satisfied else False
            Note:
                Reference:
                IS 800:2007, cl. 8.6.1.1

        """
        epsilon_w = math.sqrt(250 / f_yw)

        if serviceability_requirement == 'transverse_stiffener_not_provided':
            if web_connection_to_flange == 'along_both_longitudinal_edges':
                return d/t_w <= 200 * epsilon_w
            elif web_connection_to_flange == 'along_one_longitudinal_edge':
                return d/t_w <= 90 * epsilon_w
        elif serviceability_requirement == 'only_transverse_stiffeners_provided_in_web_flange_connection_along_both_longitudinal_edges':
            if 3 * d >= c >= d:
                return d / t_w <= 200 * epsilon_w
            elif 0.74 * d <= c < d:
                return c / t_w <= 200 * epsilon_w
            elif c < 0.74 * d:
                return d / t_w <= 270 * epsilon_w
            else:
                return 'web_is_unstiffened'

        elif serviceability_requirement == 'transverse_and_longitudinal_stiffener_at_one_level_as_cl_8_7_13':
            if d < c <= 2.4 * d:
                return bool(d / t_w <= 250 * epsilon_w)
            elif 0.74 * d <= c < d:
                return bool(c / t_w <= 250 * epsilon_w)
            else:
                return bool(d / t_w <= 340 * epsilon_w)

        else:
            return bool( d / t_w <= 400 * epsilon_w)

    # cl 8.6.1.2 Compression flange buckling requirement
    def cl_8_6_1_2_web_thickness_to_avoid_buckling_of_compression_flange(d, t_w, c, f_yf, Transverse_stiffener):
        """
            Check for minimum web thickness to avoid buckling of compression flange
            Args:
                d - depth of the web in mm
                t_w - thickness of the web in mm
                c - spacing of transverse stiffener in mm
                epsilon_f - yield stress ratio of flange
                f_yw - yield stress of compression flange in N/mm**2
                Transverse_stiffener - either 'provided' or 'not provided'
            Return:
                True or False
            Note:
                Reference:
                IS 800:2007, cl. 8.6.1.1

        """
        epsilon_f = math.sqrt(250 / f_yf)
        if Transverse_stiffener == 'not provided':
           return bool( d / t_w <= 345 * epsilon_f ** 2)
        else:
            if c >= 1.5 * d:
                return bool(d / t_w <= 345 * epsilon_f ** 2)
            else:
                return bool(d / t_w <= 345 * epsilon_f)

    # cl8.7.1.5 Buckling resistance of stiffeners
    # Effective length for load carrying web stiffeners
    @staticmethod
    def cl_8_7_1_5_effective_length_for_load_carrying_web_stiffeners(L, restrained_condition):
        """
            Calculation of Effective length for load carrying web stiffeners for calculating
            buckling resistance F_xd
            Args:
                L - length of stiffener in mm
                restrained_condition - Either 'flange_restrained_against_rotation' or
                                    'flange_not_restrained_against_rotation'
            Returns:
                K_L - effective length for load carrying web stiffeners in mm
            Note:
                Reference:
                IS 800:2007,   cl 8.7.1.5
        """


        if restrained:
            K_L = 0.7 * L
            return K_L
        else:
            K_L = L
            return K_L

    # Cl 8.7.2.4 Minimum stiffeners
    @staticmethod
    def cl_8_7_2_4_I_s_for_transverse_web_Stiffeners_not_subjected_to_external_load(c, d, t_w):
        """
            Calculation of second moment of area when transverse web stiffener
                not subjected to external load
            Args:
                d - depth of thw web in mm
                t_w - minimum required web thickness foe spacing using tension filed action ,as given in cl8.4.2.1 in mm
                c - actual stiffener spacing in mm
            Return:
                I_s_min - second moment of area in mm**4
            Note:
                Reference:
                IS 800:2007,  cl 8.7.2.4
        """
        if c / d >= math.sqrt(2):
            I_s_min = 0.75 * d * t_w ** 3
        else:
            I_s_min = 1.5 * d ** 2 * t_w ** 3 / c ** 2

        return I_s_min

    # cl 8.7.2.5 Buckling check on intermediate transverse web stiffeners
    def cl_8_7_2_5_buckling_check_on_intermediate_transverse_web_stiffener(V, F_qd, F_x, F_xd, M_q, M_yq,V_cr):
        """
            Buckling check on intermediate transverse web stiffeners
        Args:
                F_qd - design resistance of the intermediate stiffeners in N
                V -factored shear force adjacent to the stiffener in N
                F_qd - deign resistance of an intermediate web stiffener
                        to buckling corresponding to buckling about at
                         axis parallel to the web as in cl 8.7.1.5 in N
                F_x - external load or reaction at the stiffener in N
                F_xd - design resistance of a load carrying stiffener
                        corresponding to buckling about axis parallel
                        to the web as in cl 8.7.1.5 in N
                M_q - moment on the stiffener due to eccentrically
                        applied load anf transverse load, if any in N*mm
                M_yq - yield moment capacity og the stiffener based
                        on its elastic modulus about its centroidal
                        axis parallel to the web in N*mm
        Return:
            F_q - stiffener force in N

        Note:
            Reference:
            IS 800:2007,  cl 8.7.2.5, cl.8.7.3

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        F_q = min(V - V_cr / gamma_m0, F_qd)
        if (F_q - F_x) / F_qd + F_x / F_xd + M_q / M_yq <= 1:
            return F_q
        else:
            return 'cl.8.7.2.5.warning:buckling check on intermediate transverse web stiffener not satisfied'


    # cl 8.7.2.6 Connection of intermediate stiffeners to web
    @staticmethod
    def cl_8_7_2_6_shear_between_each_component_of_stiffener_and_web(t_w, b_s,s_e):

        """
            Calculation of minimum allowable shear between each component of stiffener and web
            Args:
                t_w - web thickness in mm
                b_s - outstanding  width of the stiffeners in mm

            Returns:
                V_is_min - minimum shear between each component of stiffener and web in N/mm


               Notes:
                Reference:
                IS 800:2007,  cl 8.7.2.6

        """
        V = t_w ** 2 / 5 * b_s + s_e
        return V


    # cl 8.7.3 Load Carrying stiffeners
    # cl 8.7.3.1 Web Checking
    @staticmethod
    def cl_8_7_3_1_area_of_cross_section_of__web(b_1, n_1, t_w):
        """
            Calculation of area of cross section of the web
            Args:
                b_1 - width of stiff bearing on the flange in mm
                n_1 - dispersion of the load through the web
                     45 degree, to the level of half the depth
                     of the cross section
                t_w - web thickness in mm
                      45 degrees, to the level of half the depth
                      of the cross section
            Returns:
                A_w - area of cross section of the web in mm**2
            Notes:
                Reference:
                IS 800:2007,  cl 8.7.3.1
        """
        A_w = (b_1 + n_1) / t_w
        return A_w

    # cl 8.7.4 Bearing Stiffeners

    @staticmethod
    def cl_8_7_4_force_applied_through_flange_by_loads_(b_1, n_2, t_w, f_yw):
        """
            Calculation of force applied through a flange by load or reaction
            exceeding the local capacity of the web at its connection

            Args:
                b_1 - stiff bearing length in mm
                n_2 - length obtained by dispersion through the flange to the web
                        junction at a slope of 1:2.5 to the plane of the flange  in mm
                t_w - thickness of the web in mm
                f_yw - yield stress of the web in N/mm**2

            Returns:
                F_w - force applied through flange by loads  in N

            Notes:
                Reference:
                IS 800:2007,  cl 8.7.4

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        F_w = (b_1 + n_2) * t_w * f_yw / gamma_m0
        return F_w

    # cl 8.7.5 Design of load carrying stiffeners
    # cl 8.7.5.1 Buckling check
    # cl 8.7.5.2 Bearing check

    @staticmethod
    def cl_8_7_5_2_bearing_strength_of_stiffeners(F_x, A_q, f_yq):
        """
            Calculation of bearing strength of stiffeners

            Args:
                F_x - external load or reaction in N
                A_q - area of the stiffeners in contact with the flange in mm
                f_yq - yield stress of the stiffeners in N/mm**2

            Return:
                F_psd - bearing strength of stiffeners in N

            Notes:
                Reference:
                IS 800:2007,  cl 8.7.4
        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        F_psd = max(A_q * f_yq / (0.8 * gamma_m0), F_x)
        return F_psd

    # cl 8.7.9 Torsional Stiffeners
    @staticmethod
    def cl_8_7_9_minimum_second_moment_of_area_of_the_stiffener_section(D, T_cf, L_LT, r_y):
        """
            calculation of  minimum second moment of area of the stiffener

            Args:
                D = overall depth of beam at support in mm
                T_cf = maximum thickness of compression flange in the span under consideration in mm
                K_L=  laterally unsupported effective length of the compression flange of the beam in mm
                r_y = radius of gyration of the beam about the minor axis in mm

            Returns:
                I_s_min = calculation of  minimum second moment of area of the stiffener in mm**4


            Notes:
                Reference:
                IS 800:2007,  cl 8.7.4
        """
        if L_LT / r_y <= 50:
            alpha_s = 0.006
        elif 50 < L_LT / r_y <= 100:
            alpha_s = 0.3 / (L_LT / r_y)
        else:
            alpha_s = 30 / (L_LT / r_y) ** 2

        I_s_min = 0.34 * alpha_s * D ** 3 * T_cf

        return I_s_min

    # ==========================================================================
    """    SECTION  9     MEMBER SUBJECTED TO COMBINED FORCES   """
    # --------------------------------------------------------------------------

    # cl 9.2 Combined Shear and Bending
    def cl_9_2_2_moment_capacity_for_high_shear(M_d, V, V_d, M_fd, Z_e, section_type, f_y):
        """
            To calculate change in Moment Carrying Capacity due to shear force
            Args:
                M_d - plastic design moment of whole section disregarding shear force
                 effect considering web buckling effects in N*mm
                V - factored applied shear force in N
                V_d - design shear strength in N
                M_fd - plastic design strength of c/s excluding shear area considering
                        gamma_m0 in N*mm
                Ze - elastic section modulus in mm**3
                section_type - 'plastic','compact' or 'semi_compact'
                f_y - yield strength in N/mm**2
                gamma_m0 - partial safety factor
            Returns:
                M_dv - Moment Carrying Capacity under action of high shear force in N*mm

            Note:
                Reference:
                IS 800:2007, cl.9.2
        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']
        if V > 0.6 * V_d:  # cl.9.2.2
            if section_type == 'plastic' or section_type == 'compact':
                beta = (2 * V / V_d - 1) ** 2
                M_dv = min(M_d - beta * (M_d - M_fd), 1.2 * Z_e * f_y / gamma_m0)
            elif section_type == 'semi_compact':
                M_dv = Z_e * f_y / gamma_m0
            else:
                return 'enter section type in valid format'
        else:
            M_dv = M_d


        return M_dv

    #cl.9.3 Combined Axial Force and Bending Moment
    #Section Strength
    #cl.9.3.1.1  Plastic and Compact Sections

    def cl_9_3_1_1_criteria_for_combines_shear_and_bending(My, Mz, Mndy, Mndz, N, Nd, section_type):
        """
            Safety check for reduced flexural strength under combined axial force and
            respective uniaxial bending moment acting alone
        Args:
            My - factored applied moments about minor axis of c/s in N*mm
            Mz - factored applied moments about major axis of c/s N*mm
            Mndy - reduced flexural strength along minor axis N*mm
            Mndz - reduced flexural strength along major axis in N*mm
            N - factored applied axial force in N
            Nd - design strength in compression or tension in N
            section_type - 'plates' , 'Welded_I' or 'H_section' , 'standard_I'  or H_section' , 'rectangular hollow
                            section and welded box section'
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

    #conservative criteria for section under combines axial force and bending moment
    @staticmethod
    def cl_9_3_1_1_cons(My, Mz, Mdy, Mdz, N, Nd):
        """Safety check for reduced flexural strength under combined axial force and
            respective uniaxial bending moment acting alone
            using a more conservative formula
            Args:
                My - factored applied moments about minor axis of c/s in N*mm
                Mz - factored applied moments about major axis of c/s in N*mm
                Mndy - reduced flexural strength along minor axis in N*mm
                Mndz - reduced flexural strength along major axis in N*mm
                N - factored applied axial force in N
                Nd - design strength in compression or tension in N
            Returns:
                'OK' - If condition is satisfied
                else 'Warning : Reduced flexural strength does not satisfy cl.9.3.1.1'
            Note:
                Reference:
                    IS 800:2007, cl.9.3.1.1
        """
        if (N / Nd + My / Mdy + Mz / Mdz) <= 1:
            return 'OK'
        else:
            return 'Warning : Design reduced flexural strength not sufficient cl.9.3.1.1'

    # cl.9.3.1.2 Combined Axial Force and Bending - Approximate Section Strength Calculation- Plastic and Compact Sections
    # without bolt holes
    def cl9_3_1_2_design_reduced_flexure_strength(M_d, N, N_d, A, b, t_f, M_dy, M_dz, t_w, section):
            n = N / N_d
            if section == 'Plates':
                M_nd = M_d * (1 - n ** 2)
                return M_nd
            elif section == 'Welded_1' or 'H_section':
                a = min((A - 2 * b * t_f) / A, 0.5)
                if n >= a:
                    M_ndy = min(M_dy * (1 - ((n - a) / (1 - a)) ** 2), M_dy)
                else:
                    M_ndy = M_dy

                M_ndz = min(M_dz * (1 - n) / (1 - 0.5 * a), M_dz)
                return (M_ndy, M_ndz)

            elif section == 'standard_I' or 'H_section':
                a = min((A - 2 * b * t_f) / A, 0.5)
                if n <= 0.2:
                    M_ndy = M_dy
                else:
                    M_ndy = min(M_dy * (1 - ((n - a) / (1 - a)) ** 2), M_dy)
                    M_ndz = min(M_dz * (1 - n) / (1 - 0.5 * a), M_dz)

                return (M_ndy, M_ndz)

            elif section == 'Rectangular hollow section' and 'welded box section':
                a_w = min((A - 2 * b * t_f) / A, 0.5)
                a_f = min((A - 2 * h * t_w) / A, 0.5)
                M_ndy = min(M_dy * (1 - n) / (1 - 0.5 * a_f), M_dy)
                M_ndz = min(M_dz * (1 - n) / (1 - 0.5 * a_w), M_dz)
                return (M_ndy, M_ndz)
            else:
                M_nd = min(1.04 * M_d * (1 - n ** 1.7), M_d)
                return M_nd

    # 9.3.1.3 Semi - compact section
    def cl_9_3_1_3_criteria_for_absence_of_high_shear_in_semi_compact_section(f_y, f_x, N, Nd, My, Mdy, Mz, Mdz,
                                                                   compact_section):

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']
        if compact_section == 'with_hole':
            return bool(f_x <= f_y / gamma_m0)
        else:
            return bool(N / Nd + My / Mdy + Mz / Mdz <= 1)

    # cl 9.3.2 Overall Member Strength - Check for overall buckling failure for combined axial force and bending moment
    # cl 9.3.2.1 Bending and axial tension
    def cl_9_3_2_1_reduced_effective_moment_under_tension_and_banding(M_d, M, T, Z_ec, A, T_and_M_vary_independently=True):
        """
            Calculates and checks if reduced effective moment under tension and bending exceeds bending strength
                due to lateral torsional buckling.
                Args:
                    M_d - Strength due to lateral torsional buckling in  N*mm
                    M,T - factored applied moment in N*mm
                    T = factored applied tension in N
                    Z_ec - elastic section modulus w.r.t extreme compression fibre in mm**3
                    A - area of c/s in mm**2
                    N - factored applied axial force in N
                    N_d - design strength in compression or tension in N
                    psi_check - 'True' if T & M are independent else 'False'
                Returns:
                    If (criteria is satisfied):
                        M_eff - reduced effective moment under tenion and bucling
                    else:
                        'Warning : reduced effective moment under tension and bending exceeds bending strength
                         due to lateral torsional buckling'
                Note:
                    Reference:
                        IS 800:2007, cl.9.3.2.1
            """

        psi = 0.8
        if T_and_M_vary_independently is False:
            psi = 1.0
        M_eff = min(M - psi * T * Z_ec / A, M_d)

        return M_eff
    #cl 9.3.2.2 Bending and axial compression
    def cl_9_3_2_2_table18_Equivalent_Uniform_Moment_Factor(loading_type, psi, M_h, M_s=None):
        """
            Evaluates and returns equivalent moment factor
            Args:
                loading_type - True if loading is uniform, False if load is concentrated
                psi - ratio of BM at the end with higher BM to that of the other end
                M_h - BM at end with greater BM
                M_s - BM at point of zero shear, takes a default value of None (if Load is linearly varying)
            Return:
                C_m - equivalent uniform moment factor
            Note:
                Reference:
                    IS 800:2007, Table 18 (cl9.3.2.2)
        """
        if abs(psi) > 1: return 'warning: psi must be between -1 and 1'
        if M_s is None:
            C_m = max(0.6 + 0.4 * psi, 0.4)
        elif abs(M_s) < abs(M_h):
            alpha_s = M_s / M_h
            if alpha_s >= 0:
                C_m = max(0.2 + 0.8 * alpha_s, 0.4)
            else:
                if loading_type == True:
                    C_m = max((0.1 * max(1 - psi, 1) - 0.8 * alpha_s), 0.4)
                else:
                    C_m = max((0.2 * max(-psi, 0) - 0.8 * alpha_s), 0.4)
        elif abs(M_s) > abs(M_h):
            alpha_h = M_h / M_s
            if alpha_h >= 0:
                if loading_type == True:
                    C_m = 0.95 - 0.05 * alpha_h
                else:
                    C_m = 0.90 + 0.10 * alpha_h
            else:
                if loading_type == True:
                    C_m = 0.95 + 0.05 * alpha_h * min(1 + 2 * psi, 1)
                else:
                    C_m = 0.90 + 0.1 * alpha_h * min(1 + 2 * psi, 1)
        else:
            return 'Warning:Ms cannot be equal to Mh,but can be NULL'

        return C_m

    @staticmethod
    #cl9.3.2.2 Bending and axial compression
    def cl_9_3_2_2_main(P, P_d=[], M=[], M_h=[], M_d=[], N=[], N_d=[], loading_type=[], psi=[], lambda_=[],
                            M_s=[None, None, None]):
        """
            Checks safety criteria for members subjected to combined axial compresssion and biaxial bending
            Args:
                P - applied axial compression under factored load in N
                loading_type[0],loading_type[1],loading_type[2] - loading type(True if uniform,False if concentrated)
                                                                  for y,z axes and lateral torsion
                psi[0],psi[1],psi[2] - psi values for y/Z and lateral torsion
                M[0]=M_y,M[1]=M_z - max factored applied bending moments about y and z axes of member in N*mm
                M[2]=Mmlt - max factored applied bending moment for lateral torsion in N*mm
                M_h[0]=M_hy,M_h[1]=Mhz - factored applied bending moments about y and z axes
                                            of member at point of zero shear in N*mm
                M_h[2]=Mhmlt - factored applied bending moment for lateral torsion at point of zero shear in N*mm
                P_d[0]=P_dy,P_d[1]=P_dz - design strength under axial compression as governed by
                                            buckling about y and z axes resp in N
                M_d[0]=M_dy,M_d[1]=M_dz - design bending strength about y and z axes considering
                                            laterally unsupported length of c/s in N*mm
                N[0]=N_y,N[1]=N_z - factored applied axial force about y/z axes resp.
                N_d[0]=N_dy,N_d[1]=N_dz - design strength in compression about y/z axes resp.
                lambda[0]=lambda_y,lambda[1]=lambda_z,lambda[3]=lambda_Lt - slenderness ratio about y/z axes
                                                                                and that for lateral torsion
                M_s[] - BM @ point of zero shear in N*mm
            Returns:
                'OK' - If criteria is satisfied
                else -'Warning : Member does not satisfy safety criteria of cl.9.3.2.2'
            Note:
                Reference:
                    IS 800:2007, cl.9.3.2.2
            """
        C_my = IS800_2007()
        C_mz = IS800_2007()
        C_mLt = IS800_2007()
        C_m = [C_my.cl_9_3_2_2_table18(loading_type[0], psi[0], M_h[0], M_s[0]),
               C_mz.cl_9_3_2_2_table18(loading_type[1], psi[1], M_h[1], M_s[1]),
               C_mLt.cl_9_3_2_2_table18(loading_type[2], psi[2], M_h[2], M_s[2])]

        K_y = min(1 + (lambda_[0] - 0.2) * N[0] / N_d[0], 1 + 0.8 * N[0] / N_d[0])
        K_z = min(1 + (lambda_[1] - 0.2) * N[1] / N_d[1], 1 + 0.8 * N[1] / N_d[1])
        K_LT = max(1 - (0.1 * lambda_[3] * (N[0] / N_d[0])) / (C_m[3] - 0.25),
                       1 - (0.1 * N[0] / N_d[0]) / (C_m[3] - 0.25))

        if ((P / P_d[0] + (K_y * C_m[0] * M[0]) / M_d[0] + (K_LT * M[1]) / M_d[1] <= 1) and (
                P / P_d[1] + (0.6 * K_y * C_m[0] * M[0]) / M_d[0] + (K_z * C_m[1] * M[1]) / M_d[1] <= 1)):
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

    # CALCULATION OF EFFECTIVE LENGTH AGAINST LATERAL TORSIONAL BUCKLING.
    def cl_8_3_1_Effective_length_for_simply_supported_beams(L, D, Restraint_Condition_1, Restraint_Condition_2,
                                                             Loading_Condition):

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
            if Restraint_Condition_2 == "Both flanges fully restrained":
                if Loading_Condition == "Normal":
                    return 0.70 * L
                else:
                    return 0.85 * L
            if Restraint_Condition_2 == "Compression flange fully Restrained":
                if Loading_Condition == "Normal":
                    return 0.75 * L
                else:
                    return 0.90 * L
            if Restraint_Condition_2 == "Both flanges partially restrained":
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

    # Effective length for cantilever Beam

    def cl_8_3_3_Table_16_Efective_length_for_cantilever_beam(L, D, Restraint_Condition_1, Restraint_Condition_2,
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
                    return (3.0 * L + 0 * D)
                else:
                    return (7.5 * L + 0 * D)
            if Restraint_Condition_2 == "Lateral restraint to top flage":
                if Loading_condition == "Normal":
                    return (2.7 * L + 0 * D)
                else:
                    return (7.5 * L + 0 * D)
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return (2.4 * L + 0 * D)
                else:
                    return (4.5 * L + 0 * D)
            if Restraint_Condition_2 == "Lateral and Torsional restraint":
                if Loading_condition == "Normal":
                    return (2.1 * L + 0 * D)
                else:
                    return (3.6 * L + 0 * D)
        if Restraint_Condition_1 == "Continuous,with partial torsional restraint":
            if Restraint_Condition_2 == "Free":
                if Loading_condition == "Normal":
                    return (2.0 * L + 0 * D)
                else:
                    return (5.0 * L + 0 * D)
            if Restraint_Condition_2 == "Lateral restraint to top flage":
                if Loading_condition == "Normal":
                    return (1.8 * L + 0 * D)
                else:
                    return (5.0 * L + 0 * D)
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return (1.6 * L + 0 * D)
                else:
                    return (3.0 * L + 0 * D)
                if Restraint_Condition_2 == " Lateral and Torsional restraint":
                    if Loading_condition == "Normal":
                        return (1.4 * L + 0 * D)
                    else:
                        return (2.4 * L + 0 * D)
        if Restraint_Condition_1 == "Continuous,with lateral and torsional restraint":
            if Restraint_Condition_2 == "Free":
                if Loading_condition == "Normal":
                    return (1.0 * L + 0 * D)
                else:
                    return (2.5 * l + 0 * D)
            if Restraint_Condition_2 == "Lateral restraint to top flage":
                if Loading_condition == "Normal":
                    return (0.9 * L + 0 * D)
                else:
                    return (2.5 * L + 0 * D)
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return (0.8 * L + 0 * D)
                else:
                    return (1.5 * L + 0 * D)
            if Restraint_Condition_2 == " Lateral and Torsional restraint":
                if Loading_condition == "Normal":
                    return (0.7 * L + 0 * D)
                else:
                    return (1.2 * L + 0 * D)
        if Restraint_Condition_1 == "Restrained laterally,torsionally and against rotation on plan":
            if Restraint_Condition_2 == "Free":
                if Loading_condition == "Normal":
                    return (0.8 * L + 0 * D)
                else:
                    return (1.4 * L + 0 * D)
            if Restraint_Condition_2 == "Lateral restraint to top flage":
                if Loading_condition == "Normal":
                    return (0.7 * L + 0 * D)
                else:
                    return (1.4 * L + 0 * D)
            if Restraint_Condition_2 == "Torsional restraint":
                if Loading_condition == "Normal":
                    return (0.6 * L + 0 * D)
                else:
                    return (0.6 * L + 0 * D)
            if Restraint_Condition_2 == "Lateral and Torsional restraint":
                if Loading_condition == "Normal":
                    return (0.5 * L + 0 * D)
                else:
                    return (0.5 * L + 0 * D)

    def cl_8_3_Effective_length_against_torsional_restraint(L, D, Beam_type, Restraint_Condition_1,
                                                            Restraint_Condition_2, Loading_Condition):
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
            L_LT = cl_8_3_1_Effective_length_for_simply_supported_beams(L, D, Restraint_Condition_1,
                                                                        Restraint_Condition_2, Loading_Condition)
        elif Beam_type == "Simply_supported_with_intermediate_lateral_restraints":
            L_LT = 1.2 * L
        elif Beam_type == "Beam_provided_with_members_to_give_effective_lateral_restrain_to_compression_flange_at_interval":
            L_LT = 1.2 * L
        else:
            L_LT = cl_8_3_3_Table_16_Efective_length_for_cantilever_beam(L, D, Restraint_Condition_1,
                                                                         Restraint_Condition_2, Loading_Condition)

        return L_LT

        # E-1 ELASTIC CRITICAL MOMENT

    # E-1.1 General
    # TODO:Calculate L_LT = L_LT = cl_8_3_Effective_length_against_lateral_torsional_buckling(L,D,Beam_type,Restraint_Condition_1,Restraint_Condition_2,Loading_Condition)

    def Annex_E_1_1_elastic_critical_moment_corresponding_to_lateral_torsional_buckling_of_doubly_symmetric_prismatic_beam(
            I_y, I_w, I_t, G, E, L_LT):

        """
            Calculate the elastic critical moment corresponding to lateral
                torsional buckling of a doubly symmetric prismatic beam subjected to uniform
                moment in the unsupported length and torsionally restraining lateral supports as per Annex E-1.1

            Args:
                I_y - Moment of inertia about the minor axis (in quartic mm) (float)
                I_w - Warping constant of the cross- section (mm**4)(float)
                I_t - St. Venants torsion constant of the cross-section (mm**4)(float)
                G -   Modulus of rigidity (float)
                L_LT = cl_8_3_Effective_length_against_lateral_torsional_buckling(L,D,Beam_type,Restraint_Condition_1,Restraint_Condition_2,Loading_Condition)


            Returns:
                M_cr - Elastic critical moment corresponding to lateral torsional
                        buckling of doubly symmetric prismatic beam ( in N*mm) (float)


            Note:
                Reference:
                IS800:2007, Annex - E-1.1

        """

        sum_value = (I_w / I_y) + (G * I_t * L_LT * L_LT) / (pi * pi * E * I_y)

        M_cr = ((pi * pi * E * I_y) / (L_LT * L_LT)) * ((sum_value) ** 0.5)

        return M_cr

    def Annex_E_Table_42_constant_c_1_c_2_c_3(Loading_and_Support_condition, si, K):
        """
            Calculate Value of constant c_1,c_2,c_3 as per Table_42 Annex-E
            Args:
                Loading_and_Support_condition - Either "Simply supported with ends moments (M,si*M)"
                                                or "simply Supported beam with UDL"
                                                or "Fixed support with UDL"
                                                or "Simply Supported beam with point load at centre"
                                                or "Fixed Supported beam with point load at centre"
                                                or "Simply Supported beam with point at L/4 distance from both ends"

                Bending_Moment_diagram- BMD for "Simply supported with ends moments (M,si*M)" by varying value of 'si' as-
                                                si - [ +1,+3/4,+1/2,+1/4,0,-1/4,-1/2,-3/4,-1 ]
                                        BMD for "simply Supported beam with UDL"
                                        si - 0 (Assumed value)
                                        BMD for "Fixed support with UDL"
                                        si - 0 (Assumed value)
                                        BMD for "Simply Supported beam with point load at centre"
                                        si - 0 (Assumed value)
                                        BMD for "Fixed Supported beam with point load at centre"
                                        si - 0 (Assumed value)
                                        BMD for "Simply Supported beam with point at L/4 distance from both ends"
                                        si - 0 (Assumed value)

                K - [1.0,0.7,0.5]

            Returns:
                Value of constant c_1,c_2,c_3

            Note:
                References:
                IS800:2007,Table 42,cl E-1.2
        """

        if Loading_and_Support_condition == "Simply supported with ends moments (M,si*M)":
            if si == 1:
                if K == 1.0:
                    return {"c1": 1.000, "c2": 0, "c3": 1.000}
                if K == 0.7:
                    return {"c1": 1.000, "c2": 0, "c3": 1.113}
                if K == 0.5:
                    return {"c1": 1.000, "c2": 0, "c3": 1.144}
            if si == +3 / 4:
                if K == 1.0:
                    return {"c1": 1.141, "c2": 0, "c3": 0.998}
                if K == 0.7:
                    return {"c1": 1.270, "c2": 0, "c3": 1.565}
                if K == 0.5:
                    return {"c1": 1.305, "c2": 0, "c3": 2.283}
            if si == +1 / 2:
                if K == 1.0:
                    return {"c1": 1.323, "c2": 0, "c3": 0.992}
                if K == 0.7:
                    return {"c1": 1.473, "c2": 0, "c3": 1.556}
                if K == 0.5:
                    return {"c1": 1.514, "c2": 0, "c3": 2.271}
            if si == +1 / 4:
                if K == 1.0:
                    return {"c1": 1.879, "c2": 0, "c3": 0.939}
                if K == 0.7:
                    return {"c1": 2.092, "c2": 0, "c3": 1.473}
                if K == 0.5:
                    return {"c1": 2.150, "c2": 0, "c3": 2.150}
            if si == 0:
                if K == 1.0:
                    return {"c1": 1.563, "c2": 0, "c3": 0.977}
                if K == 0.7:
                    return {"c1": 1.739, "c2": 0, "c3": 1.531}
                if K == 0.5:
                    return {"c1": 1.788, "c2": 0, "c3": 2.235}
            if si == -1 / 4:
                if K == 1.0:
                    return {"c1": 2.281, "c2": 0, "c3": 0.855}
                if K == 0.7:
                    return {"c1": 2.538, "c2": 0, "c3": 1.340}
                if K == 0.5:
                    return {"c1": 2.609, "c2": 0, "c3": 1.957}
            if si == -1 / 2:
                if K == 1.0:
                    return {"c1": 2.704, "c2": 0, "c3": 0.676}
                if K == 0.7:
                    return {"c1": 3.009, "c2": 0, "c3": 1.059}
                if K == 0.5:
                    return {"c1": 3.093, "c2": 0, "c3": 1.546}
            if si == -3 / 4:
                if K == 1.0:
                    return {"c1": 2.927, "c2": 0, "c3": 0.366}
                if K == 0.7:
                    return {"c1": 3.009, "c2": 0, "c3": 0.575}
                if K == 0.5:
                    return {"c1": 3.093, "c2": 0, "c3": 0.837}
            if si == -1:
                if k == 1.0:
                    return {"c1": 2.752, "c2": 0, "c3": 0}
                if k == 0.7:
                    return {"c1": 3.063, "c2": 0, "c3": 0}
                if k == 0.5:
                    return {"c1": 3.149, "c2": 0, "c3": 0}
        if Loading_and_Support_condition == "simply Supported beam with UDL":
            if si == 0:
                if K == 1.0:
                    return {"c1": 1.132, "c2": 0.459, "c3": 0.525}
                if K == 0.5:
                    return {"c1": 0.972, "c2": 0.304, "c3": 0.980}
        if Loading_and_Support_condition == "Fixed support with UDL":
            if si == 0:
                if K == 1.0:
                    return {"c1": 1.285, "c2": 1.562, "c3": 0.753}
                if K == 0.5:
                    return {"c1": 0.712, "c2": 0.652, "c3": 1.070}
        if Loading_and_Support_condition == "Simply Supported beam with point load at centre":
            if si == 0:
                if K == 1.0:
                    return {"c1": 1.365, "c2": 0.553, "c3": 1.780}
                if K == 0.5:
                    return {"c1": 1.070, "c2": 0.432, "c3": 3.050}
        if Loading_and_Support_condition == "Fixed Supported beam with point load at centre":
            if si == 0:
                if K == 1.0:
                    return {"c1": 1.565, "c2": 1.257, "c3": 2.640}
                if K == 0.5:
                    return {"c1": 0.938, "c2": 0.715, "c3": 4.800}
        if Loading_and_Support_condition == "Simply Supported beam with point at L/4 distance from both ends":
            if si == 0:
                if K == 1.0:
                    return {"c1": 1.046, "c2": 0.430, "c3": 1.120}
                if K == 0.5:
                    return {"c1": 1.010, "c2": 0.410, "c3": 1.390}

    # E-1.2 Elastic Critical Moment of a Section Symmetrical About Minor Axis
    # TODO: Calculate c_1,c_2,c_3 = Annex_E_Table_42_constant_c_1_c_2_c_3(Loading_and_Support_condition,si,K)
    def Elastic_critical_moment_of_a_section_symmetrical_about_minor_axis(L_LT, c_1, c_2, c_3, E, K, K_w, y_g, A_e, b,
                                                                          t, I_fc, I_ft, I_y, G, h, h_L, h_y, n,
                                                                          I_section=True, Open_section=True,
                                                                          Plain_flange=False):
        """
            Calculate the elastic critical moment for lateral torsional buckling for beam which is
            symmetrical only about the minor axis, and bending about major axis as per Annex E-1.2

            Args:
                c_1,c_2,c_3- Annex_E_Table_42_constant_c_1_c_2_c_3(Loading_and_Support_condition,si,K)
                K -  Effective length factors of the unsupported length accounting for boundry condition
                     at the end letral supports. It is analogus to the effective length factirs for
                     compression members with end rotational restraint.
                K_w -Warping restraint factor.
                y_g -y distance between the point of application of the load and the shear centre of
                     the cross-section and is positive when the load is acting towards the shear
                     centre from the point of application.
                y_s-  co-ordinate of the shear centre with respect to centriod,positive when the shear
                        centre is on the compression side of the centriod.
                y,z-  co-ordinate of the elemental area with respect to centriod of the section
                E -   Youngs modulus of elasticity  ( N per sq.mm)(float)
                G-     Modulus of regidity (float)
                I_y  - Moment of inertia about minor axis (in mm**4)(float)
                I_fc - Moment of inertia of the compression flange about minor axis of the entire section (in mm**4)(float)
                I_ft - Moment of inertia of the tension flange about minor axis of the entire section (in mm**4)(float)
                I_w  - The wraping constant either for "I_section_mono_symmetric_about_weak_axis" or for
                                                        "Angle,Tee,narrow_rectangle_section and approximetly for hollow_section"
                I_t - Torsion constant either "for open_section" or "hollow_section"
                A_e - Area encloed by the section (in sq mm)(float)
                b -   Breadth of the elements of the section(mm)(float)
                t -   Thickness of the elements of the section (mm)(float)
                h_L-  Height of the lip in mm(float)
                h-    overall height of the section in  mm(float)
                h_y - Distance between shear centre of the two flange of the cross-section in mm (float)
                Flange type - Either "Plain_flange" or "Lipped_flange"
                L_LT = cl_8_3_Effective_length_against_lateral_torsional_buckling(L,D,Beam_type,Restraint_Condition_1,Restraint_Condition_2,Loading_Condition)
            Returns:
                M_cr- Elastic_critical_moment_of_a_section_symmetrical_about_minor_axis (in N*mm)(float)

            Note:
                References:
                IS800:2007,cl E-1.2
        """

        beta_f = I_fc / (I_ft + I_fc)

        if I_section is True:
            I_w = (1 - beta_f) * beta_f * I_y * h_y * h_y
        else:
            I_w = 0

        if Plain_flange is True:
            if beta_f > 0.5:
                y_j = 0.8 * (2 * beta_f - 1) * h_y / 2.0
            else:
                y_j = 1.0 * (2 * beta_f - 1) * h_y / 2.0
        else:
            if beta_f > 0.5:
                y_j = 0.8 * (2 * beta_f - 1) * (1 + h_L / h_) * h_y / 2.0
            else:
                y_j = (2 * beta_f - 1) * (1 + h_L / h) * h_y / 2

        if Open_section is True:
            sum_value = 0
            for i in range(n - 1):
                sum_value += (b * t * t * t) / 3
                I_t = sum_value
        else:
            sum_value = 0
            for i in range(n - 1):
                sum_value += (b / t)

        I_t = 4 * A_e / sum_value

        T_1 = c_1 * (pi * pi * E * I_y) / (L_LT)
        T_2 = (K / K_w) ** 2 * (I_w / I_y)
        T_3 = (G * I_t * L_LT * L_LT) / (pi * pi * E * I_y)
        T_4 = ((c_2 * y_g) - (c_3 * y_j)) ** 2
        T_5 = ((c_2 * y_g) - (c_3 * y_j))

        M_cr = T_1 * (((T_2 + T_3 + T_4) ** 0.5) - T_5)

        return M_cr
    # ==========================================================================
    """    ANNEX  F       CONNECTIONS   """
    # ==========================================================================
    """    ANNEX  G       GENERAL RECOMMENDATIONS FOR STEELWORK TENDERS AND CONTRACTS   """
    # ==========================================================================
    """    ANNEX  H       PLASTIC PROPERTIES OF BEAMS   """
    # ==========================================================================
    """     ------------------END------------------     """
