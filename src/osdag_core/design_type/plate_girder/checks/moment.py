import math
from ....utils.common.is800_2007 import IS800_2007
from ....utils.common.Unsymmetrical_Section_Properties import Unsymmetrical_I_Section_Properties
from ..core.utils import get_K_from_warping_restraint
from ..core.section import calc_yj
from ....Common import *

def corrected_design_bending_strength(section_class, Zp, Ze, Fy, gamma_m0, support_condition):
    """
    Corrected implementation of IS 800:2007 Cl. 8.2.1.2 design bending strength.
    
    This is a workaround for the bug in IS800_2007.cl_8_2_1_2_design_bending_strength()
    where the beta_b calculation has a logic error:
        beta_b = 1.0 if section_class == KEY_Plastic or KEY_Compact else Ze/Zp
    The above always evaluates to 1.0 because 'KEY_Compact' is truthy.
    
    Correct logic per IS 800:2007 Cl. 8.2.1.2:
        - Plastic/Compact sections: beta_b = 1.0
        - Semi-Compact sections: beta_b = Ze/Zp
    
    Args:
        section_class: 'Plastic', 'Compact', or 'Semi-Compact'
        Zp: Plastic section modulus (mm³)
        Ze: Elastic section modulus (mm³)
        Fy: Yield strength (MPa)
        gamma_m0: Partial safety factor
        support_condition: KEY_DISP_SUPPORT1 or KEY_DISP_SUPPORT2
    
    Returns:
        Md: Design bending strength (N·mm)
    """
    # Correct beta_b calculation
    if section_class == KEY_Plastic or section_class == KEY_Compact:
        beta_b = 1.0
    else:  # Semi-Compact
        beta_b = Ze / Zp if Zp > 0 else 0
    
    Md = beta_b * Zp * Fy / gamma_m0
    
    # Apply limit based on support condition
    if support_condition == KEY_DISP_SUPPORT1:
        Md_limit = 1.2 * Ze * Fy / gamma_m0
    elif support_condition == KEY_DISP_SUPPORT2:
        Md_limit = 1.5 * Ze * Fy / gamma_m0
    else:
        Md_limit = 1.2 * Ze * Fy / gamma_m0  # Default
    
    return min(Md, Md_limit)


def calc_Mdv(V, Vd, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot):
    """
    Calculate Mdv for high shear conditions.
    """
    # Calculating beta
    beta = (2 * V / Vd - 1) ** 2

    # Calculating Aw and Zfd
    d = D - (tf_top + tf_bot)
    Aw = d * tw
    Zfd = Zp - (Aw * D / 4)

    # Calculating Mfd
    Mfd = Zfd * Fy / gamma_m0

    # Calculating Md (Plastic Design Moment)
    Md = Zp * Fy / gamma_m0

    # Calculating Mdv
    Mdv = Md - beta * (Md - Mfd)

    # IS 800 Cl. 9.2.2: ...but not less than the plastic resistance of the flanges alone, Mfd
    Mdv = max(Mdv, Mfd, 0.0)

    # Limiting value as per the provided formula
    Mdv_limit = (1.2 * Ze * Fy) / gamma_m0

    return round(min(Mdv, Mdv_limit), 2)

def calc_Mdv_lat_unsupported(V, Vd, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot, Md):
    """
    Calculate Mdv for high shear conditions (Laterally Unsupported).
    """
    # Calculating beta
    beta = (2 * V / Vd - 1) ** 2

    # Calculating Aw and Zfd
    d = D - (tf_top + tf_bot)
    Aw = d * tw
    Zfd = Zp - (Aw * D / 4)
    
    # Calculating Mfd
    Mfd = Zfd * Fy / gamma_m0

    # Calculating Mdv
    Mdv = Md - beta * (Md - Mfd)
    
    # Ensure Mdv is not negative and at least Mfd if Md > Mfd
    if Md > Mfd:
        Mdv = max(Mdv, Mfd)
    Mdv = max(Mdv, 0.0)

    # Limiting value as per the provided formula
    Mdv_limit = (1.2 * Ze * Fy) / gamma_m0
    
    return round(min(Mdv, Mdv_limit), 2)

def moment_capacity_laterally_supported(V, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot, section_class, support_condition, load_moment, debug=False):
    A_vg = (D - tf_top - tf_bot) * tw
    V_d = ((A_vg * Fy) / (math.sqrt(3) * gamma_m0))
    
    if V > 0.6 * V_d: # high shear
        Md = calc_Mdv(V, V_d, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot)
        if debug:
            print(f"[DEBUG] High Shear: V={V:.2f} > 0.6*V_d={0.6*V_d:.2f}. Mdv={Md:.2f}")
    else: # low shear
        # Use corrected function instead of buggy IS800_2007 version
        Md = corrected_design_bending_strength(section_class, Zp, Ze, Fy, gamma_m0, support_condition)
        if debug:
            print(f"[DEBUG] Low Shear: V={V:.2f} <= 0.6*V_d={0.6*V_d:.2f}. Md={Md:.2f}")
    
    if debug:
        print(f"[DEBUG] Supported Moment Check: Zp={Zp:.2f}, Ze={Ze:.2f}, Md={Md/1e6:.2f} kNm, Applied={load_moment/1e6:.2f} kNm")
        
    if Md > 1.0: # avoid division by zero or negative capacity
        moment_ratio = load_moment / Md
    else:
        moment_ratio = 1e6 # Assign very high ratio for essentially zero capacity
        
    is_safe = Md >= load_moment and Md > 0
    return is_safe, Md, moment_ratio, V_d

def bending_check_lat_unsupported(beta_b_lt, plast_sec_mod_z, elast_sec_mod_z, fy, M_cr, section_class, gamma_m0):
    lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment(beta_b_lt, plast_sec_mod_z, elast_sec_mod_z, fy, M_cr)
    alpha_lt = 0.21 # Imperfection factor for rolled sections, 0.49 for welded? 
    # Note: Original code uses self.alpha_lt which is set elsewhere. 
    # Plate girders are usually welded, so alpha_lt might be 0.49 (Curve c) or 0.76 (Curve d).
    # IS 800 Table 10: Welded I section, t_f <= 40mm -> Curve c (0.49), t_f > 40mm -> Curve d (0.76).
    # But original code uses self.alpha_lt. I should pass it as argument.
    # I'll add alpha_lt to arguments.
    
    # For now, I'll assume it's passed or calculated. 
    # Let's check where alpha_lt comes from in original code.
    # It's set in `input_values` or `design_check`.
    # I'll add it to arguments.
    pass 

def bending_check_lat_unsupported_with_alpha(beta_b_lt, plast_sec_mod_z, elast_sec_mod_z, fy, M_cr, section_class, gamma_m0, alpha_lt):
    lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment(beta_b_lt, plast_sec_mod_z, elast_sec_mod_z, fy, M_cr)
    phi_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_phi_lt(alpha_lt, lambda_lt)
    X_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(phi_lt, lambda_lt)
    fbd_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_compressive_stress(X_lt, fy, gamma_m0)
    Md = IS800_2007.cl_8_2_2_Unsupported_beam_bending_strength(plast_sec_mod_z, elast_sec_mod_z, fbd_lt, section_class)
    return round(Md, 2), lambda_lt, phi_lt, X_lt, fbd_lt

def moment_capacity_laterally_unsupported(E, LLT, D, tf_top, tf_bot, Bf_top, Bf_bot, tw, LoadingCase, gamma_m0, Fy, shear_force, warping_condition, load_moment, plast_sec_mod_z, elast_sec_mod_z, section_class, alpha_lt, debug=False):
    if Bf_top == Bf_bot and tf_top == tf_bot:
        yj_val = 0
    else:
        yj_val = calc_yj(Bf_top, tf_top, Bf_bot, tf_bot, D)
        
    h = D - (tf_top + tf_bot)
    Ift = (Bf_top * tf_top ** 3) / 12
    Ifc = (Bf_bot * tf_bot ** 3) / 12
    beta_f = Ifc / (Ifc + Ift)
    
    G = 0.769 * 10 ** 5
    Kw = get_K_from_warping_restraint(warping_condition)
    
    # We need Iy, It, Iw. These should be passed or calculated.
    # I'll calculate them here using Unsymmetrical_I_Section_Properties
    Iy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(D, Bf_top, Bf_bot, tw, tf_top, tf_bot, debug=debug)
    It = Unsymmetrical_I_Section_Properties.calc_TorsionConstantIt(D, Bf_top, Bf_bot, tw, tf_top, tf_bot, debug=debug)
    Iw = Unsymmetrical_I_Section_Properties.calc_WarpingConstantIw(D, Bf_top, Bf_bot, tw, tf_top, tf_bot, debug=debug)
    
    # Mcr calc
    yg = D / 2
    K_value = 0
    c1, c2, c3 = 0, 0, 0
    
    if LoadingCase == KEY_DISP_UDL_PIN_PIN_PG:
        K_value = 1.0
        c1, c2, c3 = 1.132, 0.459, 0.525
    elif LoadingCase == KEY_DISP_UDL_FIX_FIX_PG:
        K_value = 0.5
        c1, c2, c3 = 0.712, 0.652, 1.070
    elif LoadingCase == KEY_DISP_PL_PIN_PIN_PG:
        K_value = 1.0
        c1, c2, c3 = 1.365, 0.553, 1.780
    elif LoadingCase == KEY_DISP_PL_FIX_FIX_PG:
        K_value = 0.5
        c1, c2, c3 = 0.938, 0.715, 4.800
    else:
        raise ValueError("Invalid Loading Case.")

    # Symmetric section (Eq 2.20)
    if Bf_top == Bf_bot and tf_top == tf_bot:
        term1 = (math.pi ** 2 * E * Iy) / (LLT ** 2)
        term2 = (Iw / Iy)
        term3 = (G * It * LLT ** 2) / (math.pi ** 2 * E * Iy)
        M_cr = term1 * math.sqrt(term2 + term3)
    else:
        # Unsymmetric case (Annex E full formula)
        term1 = (math.pi ** 2 * E * Iy) / (LLT ** 2)
        bracket = ((K_value / Kw) ** 2 * (Iw / Iy) +
                    (G * It * LLT ** 2) / (math.pi ** 2 * E * Iy) +
                    (c2 * yg - c3 * yj_val) ** 2)
        M_cr = c1 * term1 * math.sqrt(bracket) - term1 * (c2 * yg - c3 * yj_val)

    A_vg = (D - tf_top - tf_bot) * tw
    V_d = ((A_vg * Fy) / (math.sqrt(3) * gamma_m0))
    
    if section_class == KEY_Plastic or section_class == KEY_Compact:
        beta_b_lt = 1.0
    else:
        beta_b_lt = (elast_sec_mod_z/ plast_sec_mod_z)
        
    Md, lambda_lt, phi_lt, X_lt, fbd_lt = bending_check_lat_unsupported_with_alpha(beta_b_lt, plast_sec_mod_z, elast_sec_mod_z, Fy, M_cr, section_class, gamma_m0, alpha_lt)
    
    if shear_force > 0.6 * V_d:  # high shear
        Md = calc_Mdv_lat_unsupported(shear_force, V_d, plast_sec_mod_z, elast_sec_mod_z, Fy, gamma_m0, D, tw, tf_top, tf_bot, Md)
        if debug:
            print(f"[DEBUG] High Shear (Unsupp): V={shear_force:.2f} > 0.6*V_d={0.6*V_d:.2f}. Mdv={Md:.2f}")

    if debug:
        print(f"[DEBUG] Unsupported Moment Check: Zp={plast_sec_mod_z:.2f}, Ze={elast_sec_mod_z:.2f}, M_cr={M_cr/1e6:.2f} kNm, X_lt={X_lt:.4f}, fbd_lt={fbd_lt:.2f}, Md={Md/1e6:.2f} kNm, Applied={load_moment/1e6:.2f} kNm")
    
    if Md > 1.0:
        moment_ratio = load_moment / Md
    else:
        moment_ratio = 1e6
        
    is_safe = Md >= load_moment and Md > 0
    
    return is_safe, Md, moment_ratio, V_d, M_cr, lambda_lt, phi_lt, X_lt, fbd_lt, It, Iw
