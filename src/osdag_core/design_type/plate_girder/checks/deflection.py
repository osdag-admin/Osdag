from ....utils.common.Unsymmetrical_Section_Properties import Unsymmetrical_I_Section_Properties
from ....Common import *

def deflection_from_moment_kNm_mm(M_kNm, L_mm, E, I, case):
    """
    Compute max mid-span deflection from bending moment.
    
    Unit System (consistent mm units):
    - M_kNm: Bending moment in kN·m (converted to N·mm internally)
    - L_mm: Span length in mm
    - E: Young's modulus in MPa (N/mm²)
    - I: Second moment of area in mm⁴
    - Result: Deflection in mm

    Parameters
    ----------
    M_kNm : float
        Max bending moment in kN·m.
    L_mm : float
        Span length in mm.
    E : float
        Young's modulus in MPa (N/mm²).
    I : float
        Second moment of area in mm⁴.
    case : str
        Loading case constant from constants.py.

    Returns
    -------
    delta : float
        Mid-span deflection in mm.
    
    Note:
        Deflection formula derivation:
        For simply supported beam with UDL: δ = 5wL⁴/(384EI)
        Since M_max = wL²/8 for UDL, w = 8M/L²
        Substituting: δ = 5(8M/L²)L⁴/(384EI) = 5ML²/(48EI)
        
        The factor 1.5 in original formula was incorrect.
        Correct formula uses: pref = M * L² / (E * I)
    """
    # Convert M from kN·m to N·mm (1 kN·m = 10^6 N·mm)
    M = M_kNm * 1e6  # N·mm
    
    # Base term: M * L² / (E * I) with consistent mm units
    # M: N·mm, L: mm, E: N/mm², I: mm⁴
    # Result: (N·mm × mm²) / (N/mm² × mm⁴) = mm [Correct!]
    pref = M * L_mm ** 2 / (E * I)
    
    # Deflection coefficients based on loading case
    # IS 800:2007 Table 6 / Standard beam deflection formulas
    if case == KEY_DISP_UDL_PIN_PIN_PG:
        # Simply supported with UDL: δ = 5ML²/(48EI)
        return (5 / 48) * pref
    elif case == KEY_DISP_UDL_FIX_FIX_PG:
        # Fixed-fixed with UDL: δ = ML²/(32EI)  
        return (1 / 32) * pref
    elif case == KEY_DISP_PL_PIN_PIN_PG:
        # Simply supported with point load at center: δ = ML²/(12EI)
        return (1 / 12) * pref
    elif case == KEY_DISP_PL_FIX_FIX_PG:
        # Fixed-fixed with point load at center: δ = ML²/(24EI)
        return (1 / 24) * pref
    else:
        raise ValueError(
            f"Unknown loading case: {case}. Expected one of: "
            f"{KEY_DISP_UDL_PIN_PIN_PG}, {KEY_DISP_UDL_FIX_FIX_PG}, "
            f"{KEY_DISP_PL_PIN_PIN_PG}, {KEY_DISP_PL_FIX_FIX_PG}"
        )

def evaluate_deflection_kNm_mm(M_kNm, L, E, case, criteria, total_depth, top_flange_width, bottom_flange_width, web_thickness, top_flange_thickness, bottom_flange_thickness):
    """
    Calculate deflection and compare against serviceability limits.
    
    Parameters
    ----------
    M_kNm : float
        Bending moment in kN·m
    L : float
        Span length in mm
    E : float
        Young's modulus in MPa (N/mm²)
    case : str
        Loading case constant
    criteria : float or str
        Deflection limit as L/n (e.g., 600 means L/600)
    total_depth : float
        Overall depth of section (mm)
    top_flange_width : float
        Width of top flange (mm)
    bottom_flange_width : float
        Width of bottom flange (mm)
    web_thickness : float
        Thickness of web (mm)
    top_flange_thickness : float
        Thickness of top flange (mm)
    bottom_flange_thickness : float
        Thickness of bottom flange (mm)
    
    Returns
    -------
    tuple : (is_safe, deflection_ratio)
        is_safe: bool - True if deflection within allowable
        deflection_ratio: float - actual/allowable deflection ratio
    """
    # Calculate moment of inertia about major axis (mm⁴)
    I = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaZ(
        total_depth, top_flange_width, bottom_flange_width, 
        web_thickness, top_flange_thickness, bottom_flange_thickness
    )
    
    # Calculate actual deflection in mm
    delta = deflection_from_moment_kNm_mm(M_kNm, L, E, I, case)
    
    # Calculate allowable deflection per IS 800:2007 Table 6
    n = float(criteria)
    allowable = L / n  # mm
    
    # Check serviceability
    is_safe = (delta <= allowable)
    deflection_ratio = delta / allowable if allowable > 0 else float('inf')
    
    # Debug print statements for deflection check (commented out)
    # print(f"\n========== DEFLECTION CHECK (IS 800:2007 Table 6) ==========")
    # print(f"  --- Input Parameters ---")
    # print(f"  Bending Moment (M): {M_kNm:.2f} kN·m")
    # print(f"  Span Length (L): {L:.2f} mm")
    # print(f"  Modulus of Elasticity (E): {E:.2f} MPa")
    # print(f"  Moment of Inertia (I): {I:.2f} mm⁴ ({I/1e8:.4f} cm⁴)")
    # print(f"  Loading Case: {case}")
    # print(f"  --- Deflection Calculation ---")
    # print(f"  Calculated Deflection (δ): {delta:.4f} mm")
    # print(f"  Deflection Limit Criteria: L/{n:.0f}")
    # print(f"  Allowable Deflection: {allowable:.4f} mm")
    # print(f"  Deflection Ratio (δ/allowable): {deflection_ratio:.4f}")
    # if is_safe:
    #     print(f"  >>> DEFLECTION CHECK PASSED (δ ≤ L/{n:.0f}) <<<")
    # else:
    #     print(f"  >>> DEFLECTION CHECK FAILED (δ > L/{n:.0f}) <<<")
    #     print(f"  Required Moment of Inertia for L/{n:.0f}: {I * deflection_ratio:.2f} mm⁴")
    # print(f"=============================================================\n")
    
    return is_safe, deflection_ratio

