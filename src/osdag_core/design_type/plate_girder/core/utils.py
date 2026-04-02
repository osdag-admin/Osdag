
import math

def ceil_to_nearest(x, multiple):
    return float(math.ceil(x / multiple) * multiple)

def get_K_from_warping_restraint(warping_condition):
    """
    Return effective length factor K based on exact warping restraint description (IS 800:2007, Clause E.1).
    """
    if warping_condition == "Both flanges fully restrained":
        return 0.5
    elif warping_condition == "Compression flange fully restrained":
        return 0.7
    elif warping_condition == "Compression flange partially restrained":
        return 0.85
    elif warping_condition == "Warping not restrained in both flanges":
        return 1.0
    else:
        raise ValueError("Invalid warping restraint. Use one of the four standard conditions.")

def get_effective_length_factor(torsional_res, warping_res, load_type):
    """
    Calculate Effective Length Factor (k) and depth offset for Lateral Torsional Buckling
    Based on IS 800:2007 Table 15 (Effective Length for Simply Supported Beams, LLT)
    
    Effective Length LLT = k * L + d_mult * D
    where:
        L = span length
        D = total depth of section
        k = length multiplier factor
        d_mult = depth offset multiplier (0 for most cases, 2 for partial restraints)
    
    Returns:
        tuple: (k_factor, d_multiplier)
            k_factor: multiplier for span L
            d_multiplier: multiplier for depth D (to add as offset, e.g., 2 means add 2D)
    """
    # Keys from Common.py
    # Torsional Restraint
    TR_FULL = 'Fully Restrained'
    TR_PARTIAL_CONN = 'Partially Restrained-support connection'
    TR_PARTIAL_BEARING = 'Partially Restrained-bearing support'
    
    # Warping Restraint
    WR_BOTH_FULL = 'Both flanges fully restrained'
    WR_COMP_FULL = 'Compression flange fully restrained'
    WR_COMP_PARTIAL = 'Compression flange partially restrained'
    WR_NONE = 'Warping not restrained in both flanges'
    
    # Loading Condition
    LOAD_NORMAL = 'Normal'
    LOAD_DESTAB = 'Destabilizing'
    
    k = 1.0  # Default length factor
    d_mult = 0  # Default depth offset multiplier (no +2D term)
    
    if torsional_res == TR_FULL:
        # Fully restrained torsion - no +2D term
        d_mult = 0
        if warping_res == WR_BOTH_FULL:
            k = 0.70 if load_type == LOAD_NORMAL else 0.85
        elif warping_res == WR_COMP_FULL:
            k = 0.75 if load_type == LOAD_NORMAL else 0.90
        elif warping_res == WR_COMP_PARTIAL:
            k = 0.85 if load_type == LOAD_NORMAL else 1.00
        elif warping_res == WR_NONE:
            k = 1.00 if load_type == LOAD_NORMAL else 1.20
            
    elif torsional_res == TR_PARTIAL_CONN:
        # Partially restrained by bottom flange support connection
        # LLT = L + 2D (Normal) or 1.2L + 2D (Destabilizing)
        if warping_res == WR_NONE:
            k = 1.0 if load_type == LOAD_NORMAL else 1.2
            d_mult = 2  # Add 2D offset
        else:
            # For other warping conditions with partial torsion, use fully restrained values
            k = 1.0 if load_type == LOAD_NORMAL else 1.20
            d_mult = 0
             
    elif torsional_res == TR_PARTIAL_BEARING:
        # Partially restrained by bottom flange bearing support
        # LLT = 1.2L + 2D (Normal) or 1.4L + 2D (Destabilizing)
        if warping_res == WR_NONE:
            k = 1.2 if load_type == LOAD_NORMAL else 1.4
            d_mult = 2  # Add 2D offset
        else:
            # For other warping conditions with partial torsion, use conservative values
            k = 1.2 if load_type == LOAD_NORMAL else 1.4
            d_mult = 0
            
    return (k, d_mult)
