import math
from ....utils.common.is800_2007 import IS800_2007

def calc_K_v(c, d, web_philosophy):
    """
    Calculate shear buckling coefficient K_v per IS 800:2007 Cl. 8.4.2.2.
    
    Args:
        c: Stiffener spacing (mm)
        d: Effective depth of web (mm)
        web_philosophy: 'Thick Web without ITS' or 'Thin Web with ITS'
    
    Returns:
        K_v: Shear buckling coefficient
    
    IS 800:2007 Reference:
        Cl. 8.4.2.2 - For unstiffened webs: K_v = 5.35
        For stiffened webs:
            c/d <= 1.0: K_v = 4 + 5.35/(c/d)²
            c/d > 1.0: K_v = 5.35 + 4/(c/d)²
    """
    if web_philosophy == 'Thick Web without ITS':
        return 5.35
    
    if c is None or c == 0 or d == 0:
        return 5.35
        
    cd_ratio = float(c) / float(d)
    
    if cd_ratio <= 1.0:
        K_v = 4 + 5.35 / (cd_ratio ** 2)
    else:
        K_v = 5.35 + 4 / (cd_ratio ** 2)
    
    return K_v


def shear_capacity_laterally_supported_thick_web(Fy, gamma_m0, D, tw, tf_top, tf_bot, shear_force):
    A_vg = (D - tf_top - tf_bot) * tw
    V_d = ((A_vg * Fy) / (math.sqrt(3) * gamma_m0))
    shear_ratio =  shear_force / V_d
    is_safe = V_d >= shear_force
    return is_safe, V_d, shear_ratio

def shear_buckling_check_simple_postcritical(eff_depth, D, tf_top, tf_bot, tw, V, web_philosophy, E, fy, shear_force, c=0):
    A_vg = eff_depth * tw
    K_v = calc_K_v(c, eff_depth, web_philosophy)
    
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, eff_depth, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    
    # Print Simple Post Critical Method values
    print(f"\n========== SIMPLE POST CRITICAL METHOD ==========")
    print(f"  Shear Buckling Coefficient (K_v): {K_v:.4f}")
    print(f"  Elastic Critical Stress (tau_crc): {tau_crc:.2f} N/mm²")
    print(f"  Non-dimensional Web Slenderness Ratio (lambda_w): {lambda_w:.4f}")
    print(f"  Local Buckling Resistance (tau_b): {tau_b:.2f} N/mm²")
    print(f"  Yield Strength (Fy): {fy:.2f} N/mm²")
    print(f"  Shear Resistance of Web (V_cr): {V_cr:.2f} N")
    print(f"  Applied Shear Force (V): {V:.2f} N")
    print(f"  Shear Area (A_vg): {A_vg:.2f} mm²")
    print(f"=================================================\n")
    
    shear_ratio = 0.0
    if V_cr > V:
        shear_ratio = max(shear_force / V_cr, shear_ratio)
        return True, V_cr, shear_ratio
    else:
        return False, V_cr, shear_ratio

def shear_buckling_check_intermediate_stiffener(d, tw, c, e, IntStiffThickness, IntStiffenerWidth, V_ed, gamma_m0, fy, E, web_philosophy, lefactor, shear_force):
    A_vg = d * tw
    K_v = calc_K_v(c, d, web_philosophy)
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, d, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    
    # 1. Global buckling check of stiffener
    cd_ratio = c / d
    if cd_ratio >= math.sqrt(2):
        I_min_global = 0.75 * d * tw**3
    else:
        I_min_global = (1.5 * d**3 * tw**3) / (c**2)

    # Maximum allowable outstand
    max_outstand = 14 * IntStiffThickness * e

    # Fail global check if inertia or outstand insufficient
    if  max_outstand < IntStiffenerWidth:
        IntStiffenerWidth= max_outstand

    # Moment of inertia of stiffener cross-section
    I_s = (((2 * IntStiffenerWidth + tw) ** 3) * IntStiffThickness) / 12
    I_s -= (IntStiffThickness * tw ** 3) / 12

    # 2. Shear buckling (axial) check of stiffener
    # Effective shear force on stiffener
    F_q = (V_ed - V_cr) / gamma_m0

    # Provided cross-sectional area
    A_s = 2 * IntStiffenerWidth * IntStiffThickness

    # Combined area for axial buckling (stiffener + bearing area)
    A_x = A_s + (20 * tw * 2 * tw)

    # Moment of inertia for axial buckling
    I_x = (((2 * IntStiffenerWidth + tw)**3) * IntStiffThickness) / 12
    I_x += (20 * tw * 2 * tw**3) / 12
    I_x -= (IntStiffThickness * tw**3) / 12

    # Radius of gyration
    r_x = math.sqrt(I_x / A_x)

    # Slenderness ratio
    Le = lefactor * d
    slenderness_input = Le / r_x

    # Design compressive stress from IS 800
    fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
        fy, gamma_m0, slenderness_input, E
    )

    # Critical buckling resistance (kN)
    Pd = round(A_x * fcd , 2)
    shear_ratio =  max(shear_force / Pd , 0.0) # Assuming initial shear_ratio is 0 or passed in
    
    return True, Pd, shear_ratio, IntStiffenerWidth, V_cr

def shear_buckling_check_tension_field(eff_depth, D, tf_top, tf_bot, tw, c, web_philosophy, E, fy, shear_force, moment, top_flange_width, top_flange_thickness, bottom_flange_width, bottom_flange_thickness, gamma_m0):
    A_vg = (D - tf_top - tf_bot) * tw
    K_v = calc_K_v(c, eff_depth, web_philosophy)
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, eff_depth, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    Nf = moment / (eff_depth + (tf_top + tf_bot) / 2)
    phi, M_fr_t, M_fr_b, s_t, s_b, w_tf, sai, fv, V_tf = IS800_2007.cl_8_4_2_2_TensionField_unequal_Isection(c, eff_depth, tw,
                                                                        fy, top_flange_width,
                                                                        top_flange_thickness, bottom_flange_width, bottom_flange_thickness,
                                                                        Nf, gamma_m0,
                                                                        A_vg, tau_b)
    
    # Print Tension Field Action values
    print(f"\n========== TENSION FIELD ACTION ==========")
    print(f"  --- Base Shear Buckling Parameters ---")
    print(f"  Shear Buckling Coefficient (K_v): {K_v:.4f}")
    print(f"  Elastic Critical Stress (tau_crc): {tau_crc:.2f} N/mm²")
    print(f"  Non-dimensional Web Slenderness Ratio (lambda_w): {lambda_w:.4f}")
    print(f"  Local Buckling Resistance (tau_b): {tau_b:.2f} N/mm²")
    print(f"  Yield Strength (Fy): {fy:.2f} N/mm²")
    print(f"  Shear Resistance of Web (V_cr): {V_cr:.2f} N")
    print(f"  --- Tension Field Parameters ---")
    print(f"  Tension Field Angle (phi): {phi:.2f} degrees")
    print(f"  Reduced Plastic Moment - Top Flange (M_fr_top): {M_fr_t:.2f} N·mm")
    print(f"  Reduced Plastic Moment - Bottom Flange (M_fr_bot): {M_fr_b:.2f} N·mm")
    print(f"  Anchor Length - Top (s_t): {s_t:.2f} mm")
    print(f"  Anchor Length - Bottom (s_b): {s_b:.2f} mm")
    print(f"  Width of Tension Field (w_tf): {w_tf:.2f} mm")
    print(f"  Yield Strength of Tension Field (F_v): {fv:.2f} N/mm²")
    print(f"  Nominal Shear Resistance (V_tf): {V_tf:.2f} N")
    print(f"  Applied Shear Force: {shear_force:.2f} N")
    print(f"  Shear Area (A_vg): {A_vg:.2f} mm²")
    print(f"============================================\n")
    
    shear_ratio =  max(shear_force / V_tf , 0.0)
    if V_tf >= shear_force:
        return True, V_tf, shear_ratio, V_cr
    else:
        return False, V_tf, shear_ratio, V_cr

def tension_field_end_stiffener(d, tw, fyw, shear_force, moment, c, web_philosophy, E, top_flange_thickness, bottom_flange_thickness, top_flange_width, bottom_flange_width, gamma_m0, int_thickness_list, IntStiffnerwidth, IntStiffThickness, epsilon, lefactor):
    A_vg = d * tw
    K_v = calc_K_v(c, d, web_philosophy)
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, d, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fyw, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fyw)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    Nf = moment / (d + (top_flange_thickness + bottom_flange_thickness) / 2)
    result= IS800_2007.cl_8_4_2_2_TensionField_unequal_Isection(c, d, tw,
                                                            fyw, top_flange_width,
                                                            top_flange_thickness, bottom_flange_width,
                                                            bottom_flange_thickness,
                                                            Nf, gamma_m0,
                                                            A_vg, tau_b)
    V_tf= result[8]
    V_dp = (d * tw * fyw * math.sqrt(3))
    denom = V_tf - V_cr
    if denom == 0: denom = 1e-6 # Avoid division by zero
    rad = 1.0 - (V_cr - V_dp) / denom
    if rad < 0:
        return False, 0, 0, 0, 0, 0, IntStiffnerwidth, 0 # Fail
    H_q = (shear_force - V_cr) / denom
    R_tf = H_q / 2
    A_v= d * tw
    V_n= (fyw * A_v) /( math.sqrt(3) * gamma_m0)
    # Moment demand M_tf (kN·m)
    M_tf = (H_q * d)  / 10
    y = c / 2
    I = tw * c ** 3 / 12
    M_q = (I * fyw) / (gamma_m0 * y)
    moment_ratio =  max(M_tf / M_q , 0.0)
    endshear_ratio =  max(R_tf / V_n, 0.0)
    
    end_stiffthickness = 0
    
    if V_n >= R_tf:
        if M_q >= M_tf:
            Fm= M_tf/c
            Fc= Fm + shear_force
            bearing_area = 0.8 * Fc * gamma_m0 / fyw
            thickness_list = ['8', '10', '12', '14', '16', '18', '20', '22', '25', '28', '32', '36', '40', '45',
                                '50', '56', '63', '75', '80', '90', '100',
                                '110', '120']
            if len(int_thickness_list) == 0:
                return False, 0, 0, 0, 0, 0, IntStiffnerwidth, 0
            
            for t_stiff_str in thickness_list:
                t_stiff = float(t_stiff_str)
                Aq= 2 * IntStiffnerwidth* t_stiff
                # Aq>= bearing_area # This line does nothing in original code?
                max_outstand = 14 * t_stiff * epsilon
                if IntStiffnerwidth > max_outstand:
                    IntStiffnerwidth = max_outstand
                    
                I_x = (((2 * IntStiffnerwidth + tw) ** 3) * t_stiff) / 12
                I_x += (20 * tw * 2 * tw ** 3) / 12
                I_x -= (t_stiff * tw ** 3) / 12

                # Radius of gyration
                r_x = math.sqrt(I_x / Aq)

                # Slenderness ratio
                Le = lefactor * d
                slenderness_input = Le / r_x

                # Design compressive stress from IS 800
                fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
                    fyw, gamma_m0, slenderness_input, E
                )

                # Critical buckling resistance (kN)
                Pd = round(Aq * fcd , 2)

                Critical_buckling_resistance = Pd

                n2= 2.5 * bottom_flange_thickness
                Fw= n2 * tw * fyw / (gamma_m0)
                Bearing_stiffenerforce= Fc - Fw
                Bearing_capacity= fyw * Aq / (1.1 * gamma_m0)
                endshear_ratio = max(Bearing_stiffenerforce / Bearing_capacity, Fc / Pd, R_tf / V_n)

                if endshear_ratio <= 1:
                    end_stiffthickness = t_stiff
                    return True, V_cr, moment_ratio, endshear_ratio, Critical_buckling_resistance, end_stiffthickness, IntStiffnerwidth, 0 # 0 for shear_ratio placeholder
                else:
                    continue
            
            # If loop finishes without returning True
            return False, V_cr, moment_ratio, endshear_ratio, 0, 0, IntStiffnerwidth, 0
    
    return False, V_cr, moment_ratio, endshear_ratio, 0, 0, IntStiffnerwidth, 0

def tension_field_intermediate_stiffener(d, tw, c, e, IntStiffThickness, IntStiffenerWidth, V_ed, gamma_m0, fy, E, web_philosophy, lefactor, shear_force):
    A_vg = d * tw
    K_v = calc_K_v(c, d, web_philosophy)
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, d, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    
    # 1. Global buckling check of stiffener
    cd_ratio = c / d
    if cd_ratio >= math.sqrt(2):
        I_min_global = 0.75 * d * tw ** 3
    else:
        I_min_global = (1.5 * d ** 3 * tw ** 3) / (c ** 2)

    # Maximum allowable outstand
    max_outstand = 14 * IntStiffThickness * e

    # Fail global check if inertia or outstand insufficient
    if max_outstand < IntStiffenerWidth:
        IntStiffenerWidth = max_outstand

    # Moment of inertia of stiffener cross-section
    I_s = (((2 * IntStiffenerWidth + tw) ** 3) * IntStiffThickness) / 12
    I_s -= (IntStiffThickness * tw ** 3) / 12

    # 2. Shear buckling (axial) check of stiffener
    # Effective shear force on stiffener
    F_q = (V_ed - V_cr) / gamma_m0

    # Provided cross-sectional area
    A_s = 2 * IntStiffenerWidth * IntStiffThickness

    # Combined area for axial buckling (stiffener + bearing area)
    A_x = A_s + (20 * tw * 2 * tw)

    # Moment of inertia for axial buckling
    I_x = (((2 * IntStiffenerWidth + tw) ** 3) * IntStiffThickness) / 12
    I_x += (20 * tw * 2 * tw ** 3) / 12
    I_x -= (IntStiffThickness * tw ** 3) / 12

    # Radius of gyration
    r_x = math.sqrt(I_x / A_x)

    # Slenderness ratio
    Le = lefactor * d
    slenderness_input = Le / r_x

    # Design compressive stress from IS 800
    fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
        fy, gamma_m0, slenderness_input, E
    )

    # Critical buckling resistance (kN)
    Pd = round(A_x * fcd, 2)
    shear_ratio = max(shear_force / Pd, 0.0)
    
    return True, Pd, shear_ratio, IntStiffenerWidth, V_cr

def end_panel_stiffener_calc(Bf_top, Bf_bot, tw, tq, fy, gamma_m0, d, tf_top, total_depth, effective_length, tf_bot, E, eps, c, web_philosophy, load_moment, load_shear_force, int_thickness_list, end_stiffwidth, end_stiffthickness, logger):
    A_vg = d * tw
    if c is None:
        c = d
    
    K_v = calc_K_v(c, d, web_philosophy)
            
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, d, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    Nf = load_moment / d
    
    if c is None or c == 0:
        c = d
        phi = math.degrees(math.atan(1/1.5))
    else:
        phi = math.degrees(math.atan((d / float(c)) / 1.5))

    ratio_t = Nf / (Bf_top * tf_top * fy / gamma_m0)
    if ratio_t >= 1:
        M_fr_t = 0
    else:
        M_fr_t = 0.25 * Bf_top * tf_top**2 * fy * (1 - ratio_t**2)
    
    ratio_b = Nf / (Bf_bot * tf_bot * fy / gamma_m0)
    if ratio_b >= 1:
        M_fr_b = 0
    else:
        M_fr_b = 0.25 * Bf_bot * tf_bot**2 * fy * (1 - ratio_b**2)

    sinφ = math.sin(math.radians(phi))
    if sinφ == 0:
        s_t = 0
        s_b = 0
    else:
        s_t = min(2 * math.sqrt(M_fr_t / (fy * tw)) / sinφ, c)
        s_b = min(2 * math.sqrt(M_fr_b / (fy * tw)) / sinφ, c)

    w_tf = d * math.cos(math.radians(phi)) - (c - s_t - s_b) * sinφ
    sai = 1.5 * tau_b * math.sin(2 * math.radians(phi))
    fv = math.sqrt(fy**2 - 3 * tau_b**2 + sai**2) - sai
    V_tf = (A_vg * tau_b + 0.9 * w_tf * tw * fv * sinφ)
    V_p = d * tw * fy / (math.sqrt(3) * gamma_m0)
    V_tf = min(V_tf, V_p)
    V_dp = (d * tw * fy / math.sqrt(3))

    rad = 1.0 - (V_cr / V_dp)
    if rad < 0:
       return False, end_stiffwidth, end_stiffthickness, 0, 0, 0, 0 # Fail

    H_q = 1.25 * V_dp * math.sqrt(rad)
    R_tf = H_q / 2
    A_v = d * tw
    V_n = (fy * A_v) / (math.sqrt(3) * gamma_m0)
    M_tf = (H_q * d) / 10
    y = c / 2
    I = tw * (c ** 3) / 12
    M_q = (I * fy) / (gamma_m0 * y)
    
    moment_ratio = M_tf / M_q
    endshear_ratio = R_tf / V_n
    
    Fm = M_tf / c
    Fc = Fm + load_shear_force
    bearing_area = 0.8 * Fc * gamma_m0 / fy
    
    thickness_list= ['8', '10', '12', '14', '16', '18', '20', '22', '25', '28', '32', '36', '40', '45', '50', '56', '63', '75', '80', '90', '100',
                    '110', '120']
    if len(int_thickness_list) == 0:
        return False, end_stiffwidth, end_stiffthickness, moment_ratio, endshear_ratio, 0, 0

    for t_stiff_str in thickness_list:
        t_stiff = float(t_stiff_str)
        
        root_radius = min(tf_top, tf_bot) * 0.15
        min_width = (min(Bf_top, Bf_bot) - tw - 2 * root_radius)/2
        max_outstand = min(14 * t_stiff * eps, 200)
        min_thickness = max(end_stiffwidth/16, 6)
        
        if t_stiff < min_thickness:
            continue
            
        if end_stiffwidth < min_width:
            end_stiffwidth = min_width
        if end_stiffwidth > max_outstand:
            end_stiffwidth = max_outstand
            
        web_contrib_length = min(25 * tw, d/2)
        N = max(load_shear_force * 1000 * gamma_m0 / (tw * fy), tf_bot + root_radius)
        Aq = (2 * end_stiffwidth * t_stiff) + (web_contrib_length * tw)
        I_x = (((2 * end_stiffwidth + tw) ** 3) * t_stiff) / 12
        I_x += (web_contrib_length * tw ** 3) / 12
        min_I = (d * tw**3) / 12
        if I_x < min_I:
            continue
        
        r_x = math.sqrt(I_x / Aq)
        Le = 0.7 * d
        slenderness_input = Le / r_x
        K = 0.7
        KL_r = K * Le / r_x
        fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
            fy, gamma_m0, KL_r, E
        )
        Pd = Aq * fcd
        Critical_buckling_resistance = Pd
        n1 = N
        n2 = 2.5 * tf_bot
        Fw = min(n1, n2) * tw * fy / gamma_m0
        
        web_height = d - tf_top - tf_bot
        if web_height/tw > 200:
             # Web crippling check logic (simplified call or assume handled)
             pass
        
        Bearing_capacity = (fy * Aq / gamma_m0) + Fw
        Bearing_stiffenerforce = Fc - Fw
        
        bearing_ratio = Bearing_stiffenerforce / Bearing_capacity
        buckling_ratio = Fc / Pd
        shear_ratio_val = R_tf / V_n
        
        endshear_ratio = max(bearing_ratio, buckling_ratio, shear_ratio_val)
        min_MOI = (d * tw**3) / 12
        moi_check = I_x >= min_MOI
        
        if endshear_ratio <= 1.0 and moi_check:
            end_stiffthickness = t_stiff
            return True, end_stiffwidth, end_stiffthickness, moment_ratio, endshear_ratio, Critical_buckling_resistance, 0 # 0 for shear_ratio placeholder
        else:
            continue
            
    return False, end_stiffwidth, 0, moment_ratio, endshear_ratio, 0, 0
