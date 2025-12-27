import math
import logging

def check_web_crippling(shear_force, b1, tw, fy, d, gamma_m0, logger, debug=False):
    """
    Check web crippling as per IS 800:2007 Section 8.7.2.
    Returns: (is_safe, P_w) where P_w is the web crippling capacity
    """
    if logger is None:
        unique_logger_name = 'Osdag_plate_girder_flexure'
        logger = logging.getLogger(unique_logger_name)

    try:
        # Input validation with IS code specific checks
        if any(val <= 0 for val in [b1, tw, fy, d]):
            logger.warning("Invalid input parameters for web crippling check")
            return False, 0

        # As per IS 800:2007 Section 8.7.2
        # Constants for end bearing condition
        k1 = 3.25  # For end reactions (Clause 8.7.2.1)
        k2 = 0.15  # For end reactions (Clause 8.7.2.1)
        
        # Get E from material properties (default 2 x 10^5 MPa forSteel per IS 800)
        E = 2e5
        
        # Calculate web crippling resistance as per IS 800:2007 Clause 8.7.2.1
        # P_w = (k1 * k2 * tw^2 * sqrt(fy * E)) * (1 + (N/d))
        # where N = bearing length, d = clear depth of web
        P_w = (k1 * k2 * tw * tw * math.sqrt(fy * E)) * (1 + (b1/d))
        
        # Apply partial safety factor (γm0) as per IS 800:2007 Table 5 (Clause 5.4.1)
        # For strength, γm0 = 1.10 is used as per IS 800:2007
        P_w = P_w / gamma_m0  

        # Additional checks as per IS 800:2007
        if d/tw > 200:  # Slender web condition
            logger.warning("Web slenderness ratio (d/tw) exceeds 200. Additional stiffening may be required.")
        
        # Compare with factored load as per IS 800:2007
        is_safe = P_w >= shear_force
        if debug:
            print(f"[DEBUG] Web Crippling: b1={b1}, tw={tw}, d={d}, Fy={fy}, P_w={P_w:.2f}, Applied={shear_force:.2f}, Ratio={shear_force/P_w if P_w > 0 else 100:.4f}")
        if not is_safe:
            logger.warning(f"Web crippling resistance ({P_w:.2f} N) is less than factored load ({shear_force:.2f} N)")
        
        return is_safe, P_w
            
    except Exception as e:
        logger.error(f"Error in web crippling calculation: {str(e)}")
        return False, 0

def web_crippling_laterally_supported_thick_web(Fy, gamma_m0, tw, tf_top, b1, total_depth, bottom_flange_thickness, top_flange_thickness, E, shear_force, logger):
    web_height = total_depth - top_flange_thickness - bottom_flange_thickness
    # Use the IS 800:2007 compliant check_web_crippling method
    return check_web_crippling(shear_force, b1, tw, Fy, web_height, gamma_m0, logger)
