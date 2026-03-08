"""
Web thickness checks for plate girders per IS 800:2007 Cl. 8.6.1
"""

def min_web_thickness_thick_web(eff_depth, web_thickness, epsilon, stiffener_type, c_value, debug=False):
    """
    Check minimum web thickness requirements for thick web plate girders.
    Per IS 800:2007 Cl. 8.6.1.1 and 8.6.1.2, this validates web slenderness limits.
    
    Args:
        eff_depth: Effective depth of web (mm)
        web_thickness: Web thickness (mm)
        epsilon: Material factor sqrt(250/fy)
        stiffener_type: Type of stiffener ("no_stiffener", "transverse_only", 
                        "transverse_and_one_longitudinal_compression", 
                        "transverse_and_two_longitudinal_neutral")
        c_value: Stiffener spacing (mm), can be 0 or 'NA' for no stiffeners
    
    Returns:
        bool: True if web thickness is adequate per IS 800:2007
    
    IS 800:2007 Reference:
        Cl. 8.6.1.1 - Without transverse stiffeners: d/tw <= 200ε
        Cl. 8.6.1.2 - With transverse stiffeners:
            - c >= 1.5d: d/tw <= 200ε
            - c <= 0.74d: d/tw <= 270ε  
            - Intermediate c: interpolate between limits
        Cl. 8.6.1.2 - With longitudinal stiffeners: d/tw <= 345ε
    """
    if web_thickness <= 0 or eff_depth <= 0:
        return False
        
    slenderness = eff_depth / web_thickness
    
    # Check for longitudinal stiffeners first (highest limit)
    if stiffener_type in ["transverse_and_one_longitudinal_compression", 
                          "transverse_and_two_longitudinal_neutral"]:
        limit = 345 * epsilon
        return slenderness <= limit
    
    # No stiffeners case
    if stiffener_type == "no_stiffener":
        limit = 200 * epsilon
        return slenderness <= limit
    
    # Transverse stiffeners only - limit depends on c/d ratio per Cl. 8.6.1.2
    if c_value == 'NA' or c_value == 0 or c_value is None:
        # If no spacing provided, use conservative limit
        limit = 200 * epsilon
    else:
        c = float(c_value)
        cd_ratio = c / eff_depth
        
        if cd_ratio >= 1.5:
            # Widely spaced stiffeners
            limit = 200 * epsilon
        elif cd_ratio <= 0.74:
            # Closely spaced stiffeners
            limit = 270 * epsilon
        else:
            # Intermediate spacing - linear interpolation between limits
            # High: 270ε at cd=0.74, Low: 200ε at cd=1.5
            limit = 200 * epsilon + (270 - 200) * epsilon * (1.5 - cd_ratio) / (1.5 - 0.74)
    
    if debug:
        print(f"[DEBUG] Web Thickness Check: d/tw={slenderness:.2f}, limit={limit:.2f}, type={stiffener_type}, ok={slenderness <= limit}")
    return slenderness <= limit

