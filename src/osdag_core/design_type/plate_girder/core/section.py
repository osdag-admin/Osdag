
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

def classify_section(top_flange_width, top_flange_thickness, bottom_flange_width, bottom_flange_thickness, total_depth, web_thickness, fy, web_philosophy, has_longitudinal_stiffener=False, debug=False):
    """
    Classify plate girder section per IS 800:2007.
    
    For plate girders, the web slenderness limits are governed by Clause 8.6.1.2:
    - d/tw <= 200ε: Valid with transverse stiffeners only
    - d/tw <= 250ε: Valid with transverse + longitudinal stiffeners
    
    This is DIFFERENT from Table 2 limits (126ε for Semi-Compact) which apply
    to unstiffened sections for moment capacity calculations.
    
    Flanges must always satisfy Table 2 limits (not slender).
    
    Args:
        top_flange_width: Width of top flange (mm)
        top_flange_thickness: Thickness of top flange (mm)
        bottom_flange_width: Width of bottom flange (mm)
        bottom_flange_thickness: Thickness of bottom flange (mm)
        total_depth: Total depth of plate girder (mm)
        web_thickness: Web thickness (mm)
        fy: Yield strength (MPa)
        web_philosophy: 'Thick Web without ITS' or 'Thin Web with ITS'
        has_longitudinal_stiffener: Whether longitudinal stiffener is provided
    
    Returns:
        tuple: (section_class, is_valid) where section_class is the classification
               and is_valid indicates if the section can be used
    """
    import math
    
    # Calculate epsilon per IS 800:2007
    epsilon = math.sqrt(250 / fy)
    
    # IS 800:2007 Table 2, Sr. No. (i): Outstanding element of compression flange
    # For welded I-sections, outstand b = (B - tw)/2
    outstand_top = (top_flange_width - web_thickness) / 2
    outstand_bottom = (bottom_flange_width - web_thickness) / 2
    
    flange_class_top = IS800_2007.Table2_i(outstand_top, top_flange_thickness, fy, 'Welded')[0]
    flange_class_bottom = IS800_2007.Table2_i(outstand_bottom, bottom_flange_thickness, fy, 'Welded')[0]
    if debug:
        print(f"DEBUG: Section Classification -> Top Flange Outstand={outstand_top:.2f}, Bottom Flange Outstand={outstand_bottom:.2f}")
        print(f"DEBUG: Flange Classes -> Top: {flange_class_top}, Bottom: {flange_class_bottom}")
    
    # Calculate web d/tw ratio
    web_depth = total_depth - top_flange_thickness - bottom_flange_thickness
    d_tw = web_depth / web_thickness
    
    # Web classification per Table 2 (used for thick webs and moment capacity)
    web_class = IS800_2007.Table2_iii(web_depth, web_thickness, fy)
    if debug:
        print(f"DEBUG: Web Classification -> d={web_depth:.2f}, tw={web_thickness:.2f}, d/tw={d_tw:.2f}")
        print(f"DEBUG: Web Class (Table 2): {web_class}, Limit (Semi-Compact): {126 * epsilon:.2f}")
    
    # Check if flanges are slender (never allowed)
    flanges_slender = (flange_class_top == "Slender" or flange_class_bottom == "Slender")
    
    if flanges_slender:
        # Flanges are slender - not allowed regardless of web philosophy
        if debug:
            print("DEBUG: Classification Result -> FAILED (Slender Flanges)")
        return "Slender", False
    
    if web_philosophy == 'Thin Web with ITS':
        # For stiffened plate girders, use Clause 8.6.1.2 limits
        # These are MORE RELAXED than Table 2 limits
        if has_longitudinal_stiffener:
            # With transverse + longitudinal stiffeners: d/tw <= 250ε
            max_d_tw = 250 * epsilon
        else:
            # With transverse stiffeners only: d/tw <= 200ε
            max_d_tw = 200 * epsilon
        
        if debug:
            print(f"DEBUG: Thin Web Philosophy -> Limit d/tw={max_d_tw:.2f}")
        if d_tw > max_d_tw:
            # Web exceeds even the plate girder limits
            if debug:
                print(f"DEBUG: Classification Result -> FAILED (Web d/tw {d_tw:.2f} > {max_d_tw:.2f})")
            return "Slender", False
        else:
            # Web is valid per Cl. 8.6.1.2
            # Classify section based on flanges for moment capacity
            section_class = determine_section_class_from_flanges(flange_class_top, flange_class_bottom)
            if debug:
                print(f"DEBUG: Classification Result -> PASSED (Class based on flanges: {section_class})")
            return section_class, True
    else:
        # Thick Web without ITS: Use Table 2 limits
        # Both web and flanges must be non-slender per Table 2
        if web_class == "Slender":
            if debug:
                print(f"DEBUG: Classification Result -> FAILED (Slender Web per Table 2)")
            return "Slender", False
        else:
            section_class = determine_overall_section_class(flange_class_top, flange_class_bottom, web_class)
            if debug:
                print(f"DEBUG: Classification Result -> PASSED (Overall Class: {section_class})")
            return section_class, True


def determine_section_class_from_flanges(flange_class_top, flange_class_bottom):
    """
    Determine section class based on flanges only (for stiffened webs).
    The section class is the most restrictive of the two flanges.
    """
    class_order = [KEY_Plastic, KEY_Compact, KEY_SemiCompact]
    
    top_idx = class_order.index(flange_class_top) if flange_class_top in class_order else 2
    bot_idx = class_order.index(flange_class_bottom) if flange_class_bottom in class_order else 2
    
    return class_order[max(top_idx, bot_idx)]


def determine_overall_section_class(flange_class_top, flange_class_bottom, web_class):
    """
    Determine overall section class based on all elements (web and flanges).
    The section class is the most restrictive of all elements.
    """
    class_order = [KEY_Plastic, KEY_Compact, KEY_SemiCompact]
    
    top_idx = class_order.index(flange_class_top) if flange_class_top in class_order else 2
    bot_idx = class_order.index(flange_class_bottom) if flange_class_bottom in class_order else 2
    web_idx = class_order.index(web_class) if web_class in class_order else 2
    
    return class_order[max(top_idx, bot_idx, web_idx)]

