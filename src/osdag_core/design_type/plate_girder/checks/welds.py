import math
from ....utils.common.is800_2007 import IS800_2007
from ....utils.common.common_calculation import round_up
from ..core.section import shear_stress_unsym_I

def weld_leg_from_q_with_cl10(q_kN_per_mm, ultimate_stresses):
    """
    Compute fillet‐weld leg a [mm] from shear flow,
    using f_wd from cl.10.5.7.1.1.
    """
    # 1) get f_wd in MPa → convert to N/mm²
    f_wd = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
        ultimate_stresses
    )  # MPa

    # 2) convert q to N/mm
    q_N_per_mm = q_kN_per_mm

    # 3) throat thickness t = q / f_wd  [mm]
    t_throat = q_N_per_mm / f_wd

    # 4) leg size a = t·√2
    return t_throat * math.sqrt(2)

def design_welds_with_strength_web_to_flange(V_ed, b_ft, t_ft, b_fb, t_fb, t_w, h_w, ultimate_stresses, debug=False):
    # compute shear flows
    sf = shear_stress_unsym_I(V_ed, b_ft, t_ft, b_fb, t_fb, t_w, h_w)
    min_weld_legtop = IS800_2007.cl_10_5_2_3_min_weld_size(t_ft, t_w)
    min_weld_legbot = IS800_2007.cl_10_5_2_3_min_weld_size(t_fb, t_w)
    max_weld_legtop = IS800_2007.cl_10_5_3_1_max_weld_throat_thickness(t_ft, t_w)
    max_weld_legbot = IS800_2007.cl_10_5_3_1_max_weld_throat_thickness(t_fb, t_w)
    
    # Calculate required weld size from shear flow
    a_top_calc = weld_leg_from_q_with_cl10(sf['q_top_kN_per_mm'], ultimate_stresses)
    a_bot_calc = weld_leg_from_q_with_cl10(sf['q_bot_kN_per_mm'], ultimate_stresses)
    
    # Clamp to min and max: max(min_size, min(calculated, max_size))
    a_top = round_up(max(min_weld_legtop, min(a_top_calc, max_weld_legtop)), 1)
    a_bot = round_up(max(min_weld_legbot, min(a_bot_calc, max_weld_legbot)), 1)

    if debug:
        print(f"[DEBUG] Welds: q_top={sf['q_top_kN_per_mm']:.2f}, q_bot={sf['q_bot_kN_per_mm']:.2f}, calc_top={a_top_calc:.2f}, calc_bot={a_bot_calc:.2f}, min_top={min_weld_legtop}, max_top={max_weld_legtop}, top_leg={a_top}, bot_leg={a_bot}")
    return a_top, a_bot


def weld_for_end_stiffener(t_st, b_st, V_ed, V_unstf, D, t_ft, t_fb, tw, ultimate_stresses):
    """
    t_st : thickness of stiffener
    b_st : width of stiffener
    V_ed : design shear force
    V_unstf : unstiffened shear force
    D : depth of section
    t_ft : thickness of top flange
    t_fb : thickness of bottom flange
    tw : thickness of web
    """
    # 0) available weld length
    L_weld = D - t_ft - t_fb

    # 1) min weld per side
    q1 = tw ** 2 / (5 * b_st)

    # 2) stiffener shear per unit length
    if V_unstf is None:
        V_unstf = 0  # If unstiffened capacity wasn't calculated, assume 0
    delta_V = max(V_ed - V_unstf, 0)
    q2 = delta_V / L_weld

    # 3) total on one side
    q_tot = q1 + q2

    # 4) split into two welds (each face)
    q_each = q_tot / 2

    min_weld_legtop = IS800_2007.cl_10_5_2_3_min_weld_size(t_st, tw)

    max_weld_legtop = IS800_2007.cl_10_5_3_1_max_weld_throat_thickness(t_st, tw)

    # weld legs using cl.10 strength
    weld_stiff = weld_leg_from_q_with_cl10(q_each, ultimate_stresses)
    
    if weld_stiff < min_weld_legtop:
        weld_stiff = min_weld_legtop
    if weld_stiff > max_weld_legtop:
        weld_stiff = max_weld_legtop
    
    return weld_stiff
