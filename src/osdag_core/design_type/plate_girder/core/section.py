
from ....utils.common.is800_2007 import IS800_2007
from ....Common import *

class Section:
    def __init__(self):
        self.tf = self.tw = self.bf = self.D = self.tf_top = self.tf_bot = self.bf_top = self.bf_bot = self.c = self.t_stiff = None

def calc_yj(Bf_top, tf_top, Bf_bot, tf_bot, D):
    """
    Calculate yj per IS 800:2007 Clause E.3.2.2. Returns 0 for symmetric sections.
    """
    if Bf_top == Bf_bot and tf_top == tf_bot:
        return 0  # symmetric section
    h = D - (tf_top + tf_bot)
    Ift = (Bf_top * tf_top**3) / 12
    Ifc = (Bf_bot * tf_bot**3) / 12
    beta_f = Ifc / (Ifc + Ift)
    alpha = 0.8 if beta_f > 0.5 else 1.0
    yj= alpha * (2 * beta_f - 1) * h / 2
    return yj

def shear_stress_unsym_I(V_ed, b_ft, t_ft, b_fb, t_fb, t_w, h_w):
    # Part areas [mm^2]
    A_t = b_ft * t_ft
    A_b = b_fb * t_fb
    A_w = t_w * h_w

    # Section total depth & area
    D = t_fb + h_w + t_ft
    A = A_t + A_b + A_w

    # Centroid y‐coords from bottom of bottom flange [mm]
    y_b = t_fb / 2
    y_w = t_fb + h_w / 2
    y_t = t_fb + h_w + t_ft / 2

    # Neutral axis from bottom [mm]
    y_na = (A_b * y_b + A_w * y_w + A_t * y_t) / A

    # Second moment I_z [mm^4]
    I_b = b_fb * t_fb ** 3 / 12 + A_b * (y_b - y_na) ** 2
    I_w = t_w * h_w ** 3 / 12 + A_w * (y_w - y_na) ** 2
    I_t = b_ft * t_ft ** 3 / 12 + A_t * (y_t - y_na) ** 2
    I_z = I_b + I_w + I_t

    # First moments Q [mm^3]
    Q_bot = A_b * abs(y_na - y_b)
    Q_top = A_t * abs(y_t - y_na)

    # Shear flows q = V*Q / I  [kN·mm^3 / mm^4 = kN/mm]
    q_bot = V_ed * Q_bot / I_z
    q_top = V_ed * Q_top / I_z

    return {
        'y_na_mm': y_na, 'I_z_mm4': I_z,
        'Q_top_mm3': Q_top, 'Q_bot_mm3': Q_bot,
        'q_top_kN_per_mm': q_top,
        'q_bot_kN_per_mm': q_bot,
    }

def classify_section(top_flange_width, top_flange_thickness, bottom_flange_width, bottom_flange_thickness, total_depth, web_thickness, fy, web_philosophy):
    # IS 800:2007 Table 2, Sr. No. (i): Outstanding element of compression flange
    # For welded I-sections, outstand b = (B - tw)/2 where B = total flange width, tw = web thickness
    # This measures from the web face to the flange tip, not from centerline
    outstand_top = (top_flange_width - web_thickness) / 2
    outstand_bottom = (bottom_flange_width - web_thickness) / 2
    
    flange_class_top = IS800_2007.Table2_i(outstand_top, top_flange_thickness, fy, 'Welded')[0]
    flange_class_bottom = IS800_2007.Table2_i(outstand_bottom, bottom_flange_thickness, fy, 'Welded')[0]
    web_class = IS800_2007.Table2_iii((total_depth - top_flange_thickness - bottom_flange_thickness), web_thickness, fy)
    
    section_class = None
    if flange_class_bottom == "Slender" or web_class == "Slender" or flange_class_top == 'Slender':
        section_class = "Slender"
    else:
        if flange_class_top == KEY_Plastic:
            if web_class == KEY_Plastic:
                if flange_class_bottom == KEY_Plastic:
                    section_class = KEY_Plastic
                elif flange_class_bottom == KEY_Compact:
                    section_class = KEY_Compact
                else:  # SemiCompact
                    section_class = KEY_SemiCompact
            elif web_class == KEY_Compact:
                if flange_class_bottom in [KEY_Plastic, KEY_Compact]:
                    section_class = KEY_Compact
                else:  # SemiCompact
                    section_class = KEY_SemiCompact
            else:  # web SemiCompact
                section_class = KEY_SemiCompact

        elif flange_class_top == KEY_Compact:
            if web_class == KEY_Plastic:
                if flange_class_bottom in [KEY_Plastic, KEY_Compact]:
                    section_class = KEY_Compact
                else:  # SemiCompact
                    section_class = KEY_SemiCompact
            elif web_class == KEY_Compact:
                if flange_class_bottom in [KEY_Plastic, KEY_Compact]:
                    section_class = KEY_Compact
                else:  # SemiCompact
                    section_class = KEY_SemiCompact
            else:  # web SemiCompact
                section_class = KEY_SemiCompact

        else:  # flange_class_top == SemiCompact
            section_class = KEY_SemiCompact
    
    # Slender sections are not allowed for plate girders per IS 800:2007 Table 2
    # This applies regardless of web philosophy
    if section_class == 'Slender':
        return section_class, False
    else:
        return section_class, True

