from ....utils.common.is800_2007 import IS800_2007

def web_buckling_laterally_supported_thick_web(Fy, gamma_m0, D, tw, tf_top, tf_bot, E, b1, shear_force):
    eff_depth = D - (tf_bot + tf_top)
    n1 = eff_depth / 2
    Ac = (b1 + n1) * tw
    slenderness_input = 2.5 * eff_depth / tw
    fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(Fy, gamma_m0, slenderness_input, E)
    Critical_buckling_load = round(Ac * fcd, 2)
    # web_buckling_ratio = shear_force / Critical_buckling_load
    # shear_ratio =  max(shear_force / Critical_buckling_load , shear_ratio)
    is_safe = Critical_buckling_load >= shear_force
    return is_safe, Critical_buckling_load
