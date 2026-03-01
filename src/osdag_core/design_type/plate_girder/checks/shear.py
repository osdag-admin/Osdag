import math
from ....utils.common.is800_2007 import IS800_2007


def tension_field_unequal_I_corrected(c, d, tw, fyw, bf_top, tf_top, bf_bot, tf_bot, Nf, gamma_m0, A_v, tau_b):
    """
    Corrected Tension Field method per IS 800:2007 Cl. 8.4.2.2 / DDCL Eq 1.30.
    
    This is a LOCAL corrected version that fixes issues in IS800_2007.cl_8_4_2_2_TensionField_unequal_Isection:
    1. phi angle: DDCL uses arctan(d/c), NOT arctan((d/c)/1.5)
    2. w_tf formula: DDCL uses '+' for the second term, NOT '-'
    
    Parameters match IS800_2007 version for drop-in replacement.
    
    Returns:
        tuple: (phi, Mfr_top, Mfr_bot, s_top, s_bot, w_tf, psi, fv, V_tf)
    """
    # 1) Tension‐field angle φ - CORRECTED per DDCL Eq 1.30
    # DDCL: φ = tan⁻¹(d/c)  (NOT divided by 1.5)
    if c == 0:
        phi = 90.0
    else:
        phi = math.degrees(math.atan(d / c))  # Corrected: removed /1.5

    # 2) Reduced plastic moment of each flange
    def Mfr(bf, tf):
        Mp = 0.25 * bf * tf**2 * fyw
        ratio = Nf / (bf * tf * fyw / gamma_m0)
        if ratio >= 1:
            return 0
        else:
            return Mp * (1 - ratio**2)

    Mfr_t = Mfr(bf_top, tf_top)
    Mfr_b = Mfr(bf_bot, tf_bot)

    # 3) s‐values for each flange, limited to c
    sinφ = math.sin(math.radians(phi))
    if sinφ == 0:
        s_t = 0
        s_b = 0
    else:
        s_t = min(2 * math.sqrt(Mfr_t / (fyw * tw)) / sinφ, c) if Mfr_t > 0 else 0
        s_b = min(2 * math.sqrt(Mfr_b / (fyw * tw)) / sinφ, c) if Mfr_b > 0 else 0

    # 4) Width of the tension field w_tf - CORRECTED per DDCL Eq 1.30
    # DDCL: w_tf = d·cos(φ) + (c - s_c - s_t)·sin(φ)  (note the PLUS sign)
    cosφ = math.cos(math.radians(phi))
    w_tf = d * cosφ + (c - s_t - s_b) * sinφ  # Corrected: changed - to +

    # 5) Field yield strength f_v
    psi = 1.5 * tau_b * math.sin(2 * math.radians(phi))
    fv = math.sqrt(fyw**2 - 3 * tau_b**2 + psi**2) - psi

    # 6) Nominal shear resistance V_tf
    V_tf = (A_v * tau_b + 0.9 * w_tf * tw * fv * sinφ)
    V_p = d * tw * fyw / (math.sqrt(3) * gamma_m0)  # Plastic shear strength
    V_tf = min(V_tf, V_p)

    return phi, Mfr_t, Mfr_b, s_t, s_b, w_tf, psi, fv, V_tf


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


def shear_capacity_laterally_supported_thick_web(Fy, gamma_m0, D, tw, tf_top, tf_bot, shear_force, debug=False):
    A_vg = (D - tf_top - tf_bot) * tw
    V_d = ((A_vg * Fy) / (math.sqrt(3) * gamma_m0))
    shear_ratio =  shear_force / V_d
    is_safe = V_d >= shear_force
    if debug:
        print(f"[DEBUG] Thick Web Shear: A_vg={A_vg:.2f}, V_d={V_d:.2f}, Applied={shear_force:.2f}, Ratio={shear_ratio:.4f}")
    return is_safe, V_d, shear_ratio

def shear_buckling_check_simple_postcritical(eff_depth, D, tf_top, tf_bot, tw, V, web_philosophy, E, fy, shear_force, c=0, debug=False):
    A_vg = eff_depth * tw
    K_v = calc_K_v(c, eff_depth, web_philosophy)
    
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, eff_depth, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    
    # Print Simple Post Critical Method values
    if debug:
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

def shear_buckling_check_intermediate_stiffener(d, tw, c, e, IntStiffThickness, IntStiffenerWidth, V_ed, gamma_m0, fy, E, web_philosophy, lefactor, shear_force, debug=False):
    A_vg = d * tw
    K_v = calc_K_v(c, d, web_philosophy)
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, d, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    
    # Check minimum stiffener thickness (IS 800 Cl 8.7.1.3)
    if IntStiffThickness < d / 50.0:
        if debug:
            print(f"[DEBUG] Stiffener thickness {IntStiffThickness} < d/50 ({d/50.0}). FAILED.")
        return False, 0.0, 100.0, IntStiffenerWidth, V_cr
    
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

    # Critical buckling resistance (N)
    Pd = round(A_x * fcd , 2)
    
    # DDCL Eq 2.31: Check F_q = (V - V_cr)/gamma_m0 against stiffener capacity Pd
    # NOT the total shear force V (which was the previous incorrect implementation)
    F_q = max((V_ed - V_cr) / gamma_m0, 0.0)  # Stiffener force per DDCL
    stiffener_ratio = F_q / Pd if Pd > 0 else 1e6
    
    if debug:
        print(f"[DEBUG] Intermediate Stiffener Buckling: I_min_global={I_min_global:.2e}, I_s={I_s:.2e}")
        print(f"[DEBUG]   V_ed={V_ed:.2f}, V_cr={V_cr:.2f}, F_q={F_q:.2f}, Pd={Pd:.2f}, Ratio={stiffener_ratio:.4f}")
    
    is_safe = (F_q <= Pd) and (I_s >= I_min_global)
    return is_safe, Pd, stiffener_ratio, IntStiffenerWidth, V_cr

def shear_buckling_check_tension_field(eff_depth, D, tf_top, tf_bot, tw, c, web_philosophy, E, fy, shear_force, moment, top_flange_width, top_flange_thickness, bottom_flange_width, bottom_flange_thickness, gamma_m0, debug=False):
    A_vg = (D - tf_top - tf_bot) * tw
    K_v = calc_K_v(c, eff_depth, web_philosophy)
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, eff_depth, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    Nf = moment / (eff_depth + (tf_top + tf_bot) / 2)
    phi, M_fr_t, M_fr_b, s_t, s_b, w_tf, sai, fv, V_tf = tension_field_unequal_I_corrected(c, eff_depth, tw,
                                                                        fy, top_flange_width,
                                                                        top_flange_thickness, bottom_flange_width, bottom_flange_thickness,
                                                                        Nf, gamma_m0,
                                                                        A_vg, tau_b)
    
    # Print Tension Field Action values
    if debug:
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

def tension_field_end_stiffener(d, tw, fyw, shear_force, moment, c, web_philosophy, E, top_flange_thickness, bottom_flange_thickness, top_flange_width, bottom_flange_width, gamma_m0, int_thickness_list, IntStiffnerwidth, IntStiffThickness, epsilon, lefactor, debug=False):
    A_vg = d * tw
    K_v = calc_K_v(c, d, web_philosophy)
    mu = 0.3
    tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, d, tw)
    lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fyw, tau_crc)
    tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fyw)
    V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
    Nf = moment / (d + (top_flange_thickness + bottom_flange_thickness) / 2)
    result= tension_field_unequal_I_corrected(c, d, tw,
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
    
    if debug:
        print(f"[DEBUG] Tension Field End Stiffener: M_tf={M_tf:.2f}, M_q={M_q:.2f}, R_tf={R_tf:.2f}, V_n={V_n:.2f}")
    
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
                    if debug:
                        print(f"[DEBUG] End Stiffener Found: t={t_stiff}, Ratio={endshear_ratio:.4f}, Pd={Pd:.2f}")
                    return True, V_cr, moment_ratio, endshear_ratio, Critical_buckling_resistance, end_stiffthickness, IntStiffnerwidth, 0 # 0 for shear_ratio placeholder
                else:
                    continue
            
            # If loop finishes without returning True
            return False, V_cr, moment_ratio, endshear_ratio, 0, 0, IntStiffnerwidth, 0
    
    return False, V_cr, moment_ratio, endshear_ratio, 0, 0, IntStiffnerwidth, 0

def tension_field_intermediate_stiffener(d, tw, c, e, IntStiffThickness, IntStiffenerWidth, V_ed, gamma_m0, fy, E, web_philosophy, lefactor, shear_force, debug=False):
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
    
    if debug:
        print(f"[DEBUG] Tension Field Intermediate Stiffener: Pd={Pd:.2f}, Ratio={shear_ratio:.4f}")
    return True, Pd, shear_ratio, IntStiffenerWidth, V_cr

def end_panel_stiffener_calc(Bf_top, Bf_bot, tw, tq, fy, gamma_m0, d, tf_top, total_depth, effective_length, tf_bot, E, eps, c, web_philosophy, load_moment, load_shear_force, int_thickness_list, end_stiffwidth, end_stiffthickness, logger, debug=False):
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
        phi = math.degrees(math.atan(1))  # DDCL: φ = arctan(d/c), when c=d, φ=45°
    else:
        phi = math.degrees(math.atan(d / float(c)))  # DDCL Eq 1.29: φ = arctan(d/c), NOT /1.5

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

    w_tf = d * math.cos(math.radians(phi)) + (c - s_t - s_b) * sinφ  # DDCL Eq 1.30: PLUS sign, not minus
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
    
    if debug:
        print(f"[DEBUG] end_panel_stiffener_calc: M_tf={M_tf:.2f}, M_q={M_q:.2f}, R_tf={R_tf:.2f}, V_n={V_n:.2f}")
    
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
            if debug:
                print(f"[DEBUG] End Panel Stiffener Found: t={t_stiff}, Ratio={endshear_ratio:.4f}, Pd={Pd:.2f}")
            return True, end_stiffwidth, end_stiffthickness, moment_ratio, endshear_ratio, Critical_buckling_resistance, 0 # 0 for shear_ratio placeholder
        else:
            continue
            
    return False, end_stiffwidth, 0, moment_ratio, endshear_ratio, 0, 0

def check_longitudinal_stiffener_required(d, tw, c, epsilon, debug=False):
    """
    Determine if longitudinal stiffeners are required per IS 800:2007 Cl. 8.7.13 / DDCL 1.5.3.1.
    
    Per IS 800:2007 Clause 8.7.13:
    - First stiffener at 0.2d (1/5 distance from compression flange) required when d/tw exceeds limits
    - Second stiffener at neutral axis (0.5d) required when d/tw > 400εw
    
    Args:
        d: Web depth (mm)
        tw: Web thickness (mm) 
        c: Transverse stiffener spacing (mm), or 'NA'/None if not applicable
        epsilon: √(250/fy) - yield stress ratio
        debug: Enable debug output
        
    Returns:
        tuple: (num_required, x1_pos, x2_pos, reason)
            - num_required: 0, 1, or 2 stiffeners required
            - x1_pos: Position of first stiffener from compression flange (mm) or None
            - x2_pos: Position of second stiffener from compression flange (mm) or None
            - reason: String explaining why stiffeners are/aren't required
    """
    import math
    
    # Handle c value
    if c is None or c == 'NA' or c == 0:
        c_val = 3.0 * d  # Conservative large value if undefined
    else:
        c_val = float(c)
    
    d_tw_ratio = d / tw
    
    # Calculate slenderness limits per IS 800:2007 Cl. 8.6.1.2 / DDCL Eq 1.35-1.37
    # First stiffener limit depends on c/d ratio
    c_d_ratio = c_val / d
    
    if c_d_ratio >= 1.0 and c_d_ratio <= 2.4:
        # d/tw <= 250εw (Eq 1.35)
        first_limit = 250 * epsilon
    elif c_d_ratio >= 0.74 and c_d_ratio < 1.0:
        # c/tw <= 250εw (Eq 1.36) - use c instead of d
        first_limit = 250 * epsilon * (c_val / d)
    elif c_d_ratio < 0.74:
        # d/tw <= 340εw (Eq 1.37)
        first_limit = 340 * epsilon
    else:
        # c/d > 2.4 - conservative: use 250εw
        first_limit = 250 * epsilon
    
    # Second stiffener limit: d/tw <= 400εw (Eq 1.38)
    second_limit = 400 * epsilon
    
    num_required = 0
    x1_pos = None
    x2_pos = None
    reason = ""
    
    if debug:
        print(f"[DEBUG] Longitudinal Stiffener Check: d/tw={d_tw_ratio:.2f}, c/d={c_d_ratio:.2f}")
        print(f"[DEBUG] First limit (250-340εw): {first_limit:.2f}, Second limit (400εw): {second_limit:.2f}")
    
    # Check if first stiffener is required
    if d_tw_ratio > first_limit:
        num_required = 1
        x1_pos = round(0.2 * d, 2)  # 1/5 distance from compression flange per Cl. 8.7.13
        reason = f"d/tw ({d_tw_ratio:.1f}) > {first_limit:.1f}εw - First stiffener at 0.2d from compression flange"
        
        # Check if second stiffener is also required
        if d_tw_ratio > second_limit:
            num_required = 2
            x2_pos = round(0.5 * d, 2)  # At neutral axis per Cl. 8.7.13
            reason += f"; d/tw > {second_limit:.1f}εw - Second stiffener at neutral axis (0.5d)"
    else:
        reason = f"d/tw ({d_tw_ratio:.1f}) <= {first_limit:.1f}εw - No longitudinal stiffener required"
    
    if debug:
        print(f"[DEBUG] Result: {num_required} stiffener(s) required. x1={x1_pos}, x2={x2_pos}")
        print(f"[DEBUG] Reason: {reason}")
    
    return num_required, x1_pos, x2_pos, reason


def design_longitudinal_stiffener(d, tw, c, num_stiffeners, thickness_list, web_philosophy, epsilon, gamma_m0, fy, debug=False):
    """
    Design longitudinal stiffeners per IS 800:2007 Clause 8.7.13.
    Matches DDCL Section 1.5.3 logic.

    Args:
        d: Web depth (mm) - typically clear distance between flanges
        tw: Web thickness (mm)
        c: Transverse stiffener spacing (mm) (or 'NA'/'None' if not applicable)
        num_stiffeners: 1 or 2
        thickness_list: List of available plate thicknesses
        web_philosophy: 'Thick Web without ITS' or 'Thin Web with ITS'
        epsilon: yield stress ratio
        gamma_m0: Partial safety factor (not used in Is check but good to have)
        fy: Yield strength (MPa)
        debug: boolean

    Returns:
        tuple: (is_safe, selected_thickness, selected_width, x1, x2, I_required_1, I_provided_1, I_required_2, I_provided_2)
    """
    import math
    
    if debug:
        print(f"[DEBUG] Designing Longitudinal Stiffener: d={d}, tw={tw}, c={c}, num={num_stiffeners}")

    # Handle 'NA' or None c (though Longitudinal usually implies Thin Web with ITS)
    # If c is None or large, d/c ratio check handles it.
    if c is None or c == 'NA' or c == 0:
        c_val = 3.0 * d # Use large value if undefined
    else:
        c_val = float(c)

    # 1. First Stiffener (at 0.2 d from compression flange)
    # IS 800 Cl. 8.7.13.2 / DDCL 1.5.3.2 Eq 1.39-1.41
    
    # Calculate Required MoI for First Stiffener
    # Eq 1.39: Is >= 4 c tw^3
    I_req_1 = 4 * c_val * tw**3 
    
    if d / c_val >= math.sqrt(2):
        # Eq 1.40
        I_req_1_b = 0.75 * d * tw**3
    else:
        # Eq 1.41
        I_req_1_b = (1.5 * (d**3) * (tw**3)) / (c_val**2)
    
    # Enforce max of applicable limits for safety
    I_req_1 = max(I_req_1, I_req_1_b)
    
    # Second Stiffener (at Neutral Axis - 0.5 d)
    # Eq 1.42: Is >= d2 * tw^3 -> Is >= d * tw^3.
    
    I_req_2 = 0
    if num_stiffeners == 2:
        I_req_2 = d * tw**3

    selected_thickness = 0.0
    selected_width = 0.0
    
    I_provided_1 = 0
    I_provided_2 = 0
    
    # Positions per IS 800:2007 Cl. 8.7.13
    x1 = round(0.2 * d, 2)  # 1/5 distance from compression flange
    x2 = round(0.5 * d, 2)  # At neutral axis

    # Convert thickness list to floats
    t_list = [float(x) for x in thickness_list]
    t_list.sort()

    for t_stiff in t_list:
        if t_stiff <= 0: continue
            
        # Determine minimum required width b based on I_req_1
        # I_prov = t * b^3 / 3 >= I_req
        # b >= (3 * I_req / t)^(1/3)
        
        # Check First Stiffener Requirement
        b_req_1 = (3 * I_req_1 / t_stiff) ** (1/3)
        
        # Check Second Stiffener Requirement (if applicable)
        b_req_2 = 0
        if num_stiffeners == 2:
            b_req_2 = (3 * I_req_2 / t_stiff) ** (1/3)
            
        b_req = max(b_req_1, b_req_2)
        
        # Round up to nearest 5 or 10 mm
        b_stiff = math.ceil(b_req / 5) * 5
        
        # Check Limits
        # Max outstand: 20 * t * epsilon (Cl. 8.7.1.2)
        max_b = 20 * t_stiff * epsilon
        
        # Practical min width check (e.g., related to thickness or web)
        min_b = 50 # minimal practical width?
        
        if b_stiff <= max_b:
            if b_stiff < min_b: b_stiff = min_b # Enforce min width
            if b_stiff > max_b: continue # Cannot satisfy both min and max

            # Found a valid size!
            selected_thickness = t_stiff
            selected_width = b_stiff
            
            # Calculate Provided
            I_provided_1 = t_stiff * b_stiff**3 / 3
            I_provided_2 = I_provided_1 
            
            safe_1 = (I_provided_1 >= I_req_1)
            safe_2 = True
            if num_stiffeners == 2:
                safe_2 = (I_provided_2 >= I_req_2)
            
            if safe_1 and safe_2:
                 return True, selected_thickness, selected_width, x1, x2, I_req_1, I_provided_1, I_req_2, I_provided_2
            else:
                 continue
        else:
            continue

    return False, selected_thickness, selected_width, x1, x2, I_req_1, I_provided_1, I_req_2, I_provided_2

