
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
    Calculate Effective Length Factor (k) for Lateral Torsional Buckling
    Based on IS 800:2007 Table 15 (Effective Length for Simply Supported Beams, LLT)
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
    
    k = 1.0 # Default
    
    if torsional_res == TR_FULL:
        if warping_res == WR_BOTH_FULL:
            k = 0.7 if load_type == LOAD_NORMAL else 0.85
        elif warping_res == WR_COMP_FULL:
            k = 0.75 if load_type == LOAD_NORMAL else 0.90
        elif warping_res == WR_COMP_PARTIAL: # Assuming matches "Both flanges partially restrained" or similar intermediate case
             # Table 15: Compression flange partially restrained -> 0.85 (Normal), 1.00 (Destab)
             # Wait, Table 15 row 3 is "Both flanges fully restrained" (0.8), row 4 "Compression flange partially restrained" (0.85)
             # Let's map strictly to DDCL/Table 15 rows:
             # 1. Fully, Both Full -> 0.7
             # 2. Fully, Comp Full -> 0.75
             # 3. Fully, Both Partial -> 0.8 (Not in Common.py options usually? Let's check Common.py)
             # 4. Fully, Comp Partial -> 0.85
             # 5. Fully, None -> 1.0
             k = 0.85 if load_type == LOAD_NORMAL else 1.00
        elif warping_res == WR_NONE:
            k = 1.00 if load_type == LOAD_NORMAL else 1.20
            
    elif torsional_res == TR_PARTIAL_CONN:
        if warping_res == WR_NONE:
             k = 1.0 if load_type == LOAD_NORMAL else 1.2
             # Note: Table 15 Row 6 says "Partially restrained by bottom flange support connection" + "Warping not restrained" -> 1.0L / 1.2L
             
    elif torsional_res == TR_PARTIAL_BEARING:
        if warping_res == WR_NONE:
            k = 1.2 if load_type == LOAD_NORMAL else 1.4
            
    return k
