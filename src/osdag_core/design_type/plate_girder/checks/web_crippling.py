import math
import logging


def check_web_crippling_IS800(shear_force, b1, tw, fy, d, tf, gamma_m0, logger, debug=False):
    """
    Check web crippling (local web yielding) as per IS 800:2007 Cl. 8.7.4.
    
    This is the CORRECTED implementation using DDCL Eq 2.45:
    P_crip = (b1 + n2) * tw * fyw / gamma_m0
    
    Where:
        b1 = stiff bearing length at support (mm)
        n2 = dispersion length through web = 2.5 * tf for thick flanges (Cl. 8.7.4)
        tw = web thickness (mm)
        fyw = yield strength of web (MPa)
        gamma_m0 = partial safety factor
    
    Args:
        shear_force: Applied shear/reaction force (N)
        b1: Stiff bearing length (mm)
        tw: Web thickness (mm)
        fy: Yield strength of web (MPa)
        d: Clear depth of web (mm)
        tf: Flange thickness (mm) - for n2 calculation
        gamma_m0: Partial safety factor (typically 1.10)
        logger: Logger instance
        debug: Enable debug output
    
    Returns:
        tuple: (is_safe, P_crip) where P_crip is web crippling capacity (N)
    
    Reference:
        IS 800:2007 Cl. 8.7.4
        DDCL Section 2.4.10, Eq. 2.45
    """
    if logger is None:
        unique_logger_name = 'Osdag_plate_girder_flexure'
        logger = logging.getLogger(unique_logger_name)

    try:
        # Input validation
        if any(val <= 0 for val in [b1, tw, fy, d, tf]):
            logger.warning("Invalid input parameters for web crippling check")
            return False, 0

        # IS 800:2007 Cl. 8.7.4 - Dispersion length n2
        # For thick flanges: n2 = 2.5 * tf
        n2 = 2.5 * tf
        
        # DDCL Eq 2.45: P_crip = (b1 + n2) * tw * fyw / gamma_m0
        P_crip = (b1 + n2) * tw * fy / gamma_m0
        
        # Additional slenderness warning
        if d/tw > 200:
            logger.warning("Web slenderness ratio (d/tw) exceeds 200. Additional stiffening may be required.")
        
        # Safety check
        is_safe = P_crip >= shear_force
        
        if debug:
            print(f"[DEBUG] Web Crippling (IS 800 Cl. 8.7.4):")
            print(f"[DEBUG]   b1={b1:.2f}, n2={n2:.2f}, tw={tw:.2f}, fy={fy:.2f}")
            print(f"[DEBUG]   P_crip = ({b1:.2f} + {n2:.2f}) * {tw:.2f} * {fy:.2f} / {gamma_m0} = {P_crip:.2f} N")
            print(f"[DEBUG]   Applied={shear_force:.2f} N, Ratio={shear_force/P_crip if P_crip > 0 else 100:.4f}")
        
        if not is_safe:
            logger.warning(f"Web crippling resistance ({P_crip:.2f} N) is less than factored load ({shear_force:.2f} N)")
        
        return is_safe, P_crip
            
    except Exception as e:
        logger.error(f"Error in web crippling calculation: {str(e)}")
        return False, 0


def check_web_crippling(shear_force, b1, tw, fy, d, gamma_m0, logger, debug=False):
    """
    Backward compatible wrapper - uses tf = tw as approximation for flange thickness.
    For more accurate results, use check_web_crippling_IS800 directly.
    """
    # Use tw as approximation for tf if not provided
    tf = tw  # Conservative assumption
    return check_web_crippling_IS800(shear_force, b1, tw, fy, d, tf, gamma_m0, logger, debug)


def web_crippling_laterally_supported_thick_web(Fy, gamma_m0, tw, tf_top, b1, total_depth, bottom_flange_thickness, top_flange_thickness, E, shear_force, logger, debug=False):
    """
    Web crippling check for thick web plate girders using IS 800:2007 formula.
    """
    web_height = total_depth - top_flange_thickness - bottom_flange_thickness
    # Use average flange thickness for n2 calculation
    tf_avg = (top_flange_thickness + bottom_flange_thickness) / 2
    return check_web_crippling_IS800(shear_force, b1, tw, Fy, web_height, tf_avg, gamma_m0, logger, debug)
