from utils.common.is800_2007 import *
from pylatex import Math
from pylatex.utils import NoEscape


def cl_3_7_2_section_classification(class_of_section=None):
    """
    Find class of the section
    Args:
         class_of_section:
    Returns:
    Note:
        Reference:
        [Ref: Table 2, cl. 3.7.2 and 3.7.4 IS 800:2007]

    """

    section_classification_eqn = Math(inline=True)
    if class_of_section == int(1):
        section_classification_eqn.append(NoEscape(r'\begin{aligned} & \text{Plastic} \\ \\'))
        section_classification_eqn.append(NoEscape(r' & [\text{Ref: Table 2, Cl.3.7.2 and 3.7.4, IS 800:2007}] \end{aligned}'))
    elif class_of_section == int(2):
        section_classification_eqn.append(NoEscape(r'\begin{aligned} & \text{Compact} \\ \\'))
        section_classification_eqn.append(NoEscape(r' & [\text{Ref: Table 2, Cl.3.7.2 and 3.7.4, IS 800:2007}] \end{aligned}'))
    else:
        section_classification_eqn.append(NoEscape(r'\begin{aligned} & \text{Semi-Compact} \\ \\'))
        section_classification_eqn.append(NoEscape(r' & [\text{Ref: Table 2, Cl.3.7.2 and 3.7.4, IS 800:2007}] \end{aligned}'))
    return section_classification_eqn


def cl_5_4_1_table_4_5_gamma_value(v, t):
    """
    Calculate gamma value

    Args:
        v:value of the gamma (float)
        t:subscript (str)
    Returns:
        gamma value
    """

    v = str(v)
    gamma = Math(inline=True)
    gamma.append(NoEscape(r'\begin{aligned}\gamma_{' + t + '}&=' + v + r'\end{aligned}'))

    return gamma


def cl_6_1_tension_capacity_member(T_dg, T_dn=0.0, T_db=0.0):
    """
    Calculate Design strength of member
    Args:
         T_dg:Yeiding capacity of member
         T_dn: Rupture capacity of member
         T_db: Block shear capacity of member
    Returns:
          Design strength of member min of( Yeiding ,Rupture  and Block shear capacity)
    Note:
            Reference:
            IS 800:2007,  cl 6.1

    """

    tension_capacity_eqn = Math(inline=True)
    if T_db != 0.0 and T_dn != 0.0:
        T_d = min(T_dg, T_dn, T_db)
        T_d = str(T_d)
        T_dg = str(T_dg)
        T_dn = str(T_dn)
        T_db = str(T_db)
        tension_capacity_eqn.append(NoEscape(r'\begin{aligned} T_{\text{d}} &= \min(T_{\text{dg}},~T_{\text{dn}},~T_{\text{db}})\\'))
        tension_capacity_eqn.append(NoEscape(r'&= \min(' + T_dg + ',' + T_dn + ',' + T_db + r')\\'))
    elif T_db == 0.0 and T_dn != 0.0:
        T_d = min(T_dg, T_dn)
        T_dg = str(T_dg)
        T_dn = str(T_dn)
        T_d = str(T_d)
        tension_capacity_eqn.append(NoEscape(r'\begin{aligned} T_{\text{d}} &= \min(T_{\text{dg}},~T_{\text{dn}})\\'))
        tension_capacity_eqn.append(NoEscape(r'&= \min(' + T_dg + ',' + T_dn + r')\\'))
    elif T_db != 0.0 and T_dn == 0.0:
        T_d = min(T_dg, T_db)
        T_d = str(T_d)
        T_dg = str(T_dg)
        T_db = str(T_db)
        tension_capacity_eqn.append(NoEscape(r'\begin{aligned} T_{\text{d}} &= \min(T_{\text{dg}},~T_{\text{db}})\\'))
        tension_capacity_eqn.append(NoEscape(r'&= \min(' + T_dg + ',' + T_db + r')\\'))
    else:
        T_d = T_dg
        # T_dg = str(T_dg)
        T_d = str(T_d)
        tension_capacity_eqn.append(NoEscape(r'\begin{aligned} T_{\text{d}} &= T_{\text{dg}}\\'))
        # tension_capacity_eqn.append(NoEscape(r'&= min(' + T_dg + ',' + T_dn + r')\\'))
    tension_capacity_eqn.append(NoEscape(r'&=' + T_d + r'\\ \\'))
    tension_capacity_eqn.append(NoEscape(r'& [\text{Ref.IS 800:2007, Cl.6.1}] \end{aligned}'))

    return tension_capacity_eqn


def cl_6_2_tension_yield_capacity_member(l, t, f_y, gamma, T_dg, multiple=None, area=None):
    """
    Calculate tension yielding capacity of provided plate under axial tension
    Args:
        l: Height of  provided plate in mm (float)
        t: Thickness of  provided plate in mm (float)
        f_y:Yield stress of material in N/mm square (float)
        gamma:Partial safety factor for failure in the tension by yielding (float)
        T_dg: Tension yieldung capacity of provided plate under axial tension in N (float)
        multiple:1  (int)
    Returns:
          Tension yieldung capacity of provided plate under axial tension

    Note:
            Reference:
            IS 800:2007,  cl 6.2


    """
    if l is not None and t is not None:
        area = str(round(l * t, 2))
        l = str(l)
        t = str(t)
    else:
        area = str(area)
    f_y = str(f_y)
    gamma = str(gamma)
    T_dg = str(T_dg)
    tension_yield_eqn = Math(inline=True)
    tension_yield_eqn.append(NoEscape(r'\begin{aligned} T_{\text{dg}} &= \frac{A_g f_y}{\gamma_{m0}}\\ \\'))
    if l is not None and t is not None:
        if multiple is None or multiple == 1:
            tension_yield_eqn.append(NoEscape(r'A_{g} &= l t =' + l + r'\times' + t + r'\\'))
        else:
            multiple = str(multiple)
            tension_yield_eqn.append(NoEscape(r'A_{g} &=' + multiple + r' l t =' + multiple +
                                              r'\times' + l + r'\times' + t + r'\\'))

    tension_yield_eqn.append(NoEscape(r'&=\frac{' + area + r'\times' + f_y + '}{' + gamma + r'\times 10^3}\\'))
    tension_yield_eqn.append(NoEscape(r'&=' + T_dg + r'\\ \\'))
    tension_yield_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.6.2}] \end{aligned}'))
    return tension_yield_eqn


def cl_6_3_1_tension_rupture_plate(w_p, t_p, n_c, d_o, fu, gamma_m1, T_dn, multiple=1):
    """
    Calculate design in tension as governed by rupture of net
         cross-sectional area in case of bolted connection
    Args:
         w_p: Width of given section in mm (float)
         t_p: Thikness of given section in mm (float)
         n_c: No. of bolt holes in critical section (int)
         d_o: Diameter of bolt hole in mm (int)
         fu: Ultimate stress of material in N/mm square (float)
         gamma_m1:Partial safety factor for failure at ultimate stress  (float)
         T_dn: Rupture strength of net cross-sectional area in N (float)
         multiple: 1
    Returns:
         design in tension as governed by rupture of net cross-sectional area
    Note:
            Reference:
            IS 800:2007,  cl 6.3

    """

    w_p = str(w_p)
    t_p = str(t_p)
    n_c = str(n_c)
    d_o = str(d_o)
    f_u = str(fu)
    T_dn = str(T_dn)
    gamma_m1 = str(gamma_m1)
    multiple = str(multiple)
    Tensile_rup_eqnb = Math(inline=True)

    Tensile_rup_eqnb.append(NoEscape(r'\begin{aligned} T_{\text{dn}} &= \frac{0.9 A_{n} f_u}{\gamma_{m1}}\\'))
    Tensile_rup_eqnb.append(NoEscape(
        r'&=\frac{' + multiple + r'\times~0.9\times (' + w_p + '-' + n_c + r'\times' + d_o + r')\times' + t_p + r'\times' + f_u + r'}{' + gamma_m1 + r'}\\'))
    Tensile_rup_eqnb.append(NoEscape(r'&=' + T_dn + r'\\ \\'))
    Tensile_rup_eqnb.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.6.3.1}] \end{aligned}'))

    return Tensile_rup_eqnb


def cl_6_3_3_tension_rupture_member(A_nc, A_go, F_u, F_y, L_c, w, b_s, t, gamma_m0, gamma_m1, beta, member_rup, multiple=1):
    """
    Calculate design strength due to rupture of critical section
    Args:
          A_nc:Net area of connected leg in mm square (float)
          A_go:Gross area of outstanding leg in mm square (float)
          F_u:Ultimate stress of the material in N/mm square (float)
          F_y:Yield stess of the material in mm N/square (float)
          L_c:Length of the end connection in mm  (float)
          w:Outstanding leg width in mm  (float)
          b_s:Shear lag width in mm  (float)
          t:thickness of the leg in mm  (float)
          gamma_m0:partial safety factor for failure in tension by yeilding (float)
          gamma_m1:partial safety factor for failure at ultimate stress (float)
          beta:as per section 6.3.3 (float)
          member_rup:design strength due to rupture of critical section (float)
          multiple:1
    Returns:
           design strength due to rupture of critical section
    Note:
              Reference:
              IS 800:2007,  cl 6.3


    """
    w = str(w)
    t = str(t)
    fy = str(F_y)
    fu = str(F_u)
    b_s = str(b_s)
    L_c = str(L_c)
    A_nc = str(A_nc)
    A_go = str(A_go)
    gamma_m0 = str(gamma_m0)
    gamma_m1 = str(gamma_m1)
    beta = str(round(beta, 2))
    member_rup = str(member_rup)
    multiple = str(multiple)
    member_rup_eqn = Math(inline=True)
    member_rup_eqn.append(NoEscape(r'\begin{aligned}\beta &= 1.4 - 0.076 \times \frac{w}{t}\times\frac{f_{y}}{0.9 f_{u}}\times\frac{b_s}{L_c}\\'))
    member_rup_eqn.append(NoEscape(r'&\leq\frac{0.9 f_{u} \gamma_{m0}}{f_{y} \gamma_{m1}} \geq 0.7 \\ \\'))

    member_rup_eqn.append(NoEscape(
        r'&= 1.4 - 0.076 \times \frac{' + w + '}{' + t + r'}\times\frac{' + fy + r'}{0.9\times' + fu + r'}\times\frac{' + b_s + '}{' + L_c + r' }\\'))
    member_rup_eqn.append(NoEscape(r'&\leq\frac{0.9\times' + fu + r'\times' + gamma_m0 + '}{' + fy + r'\times' + gamma_m1 + r'} \geq 0.7 \\ \\'))
    member_rup_eqn.append(NoEscape(r'&= ' + beta + r'\\ \\'))

    member_rup_eqn.append(
        NoEscape(r'T_{\text{dn}} &= ' + multiple + r'\times \Bigg(\frac{0.9 A_{nc}f_{u}}{\gamma_{m1}} + \frac{\beta A_{go} f_{y}}{\gamma_{m0}} \Bigg)\\'))
    member_rup_eqn.append(NoEscape(
        r'&= ' + multiple + r'\times \Bigg(\frac{0.9\times' + A_nc + r'\times' + fu + '}{' + gamma_m1 + r'} + \frac{' + beta + r'\times' + A_go + r'\times' + fy + '}{' + gamma_m0 + r'} \Bigg)\\'))
    member_rup_eqn.append(NoEscape(r'&= ' + member_rup + r'\\ \\'))

    member_rup_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.6.3.3}] \end{aligned}'))
    return member_rup_eqn


def cl_6_4_blockshear_capacity_member(Tdb, A_vg=None, A_vn=None, A_tg=None, A_tn=None, f_u=None, f_y=None, gamma_m0=None, gamma_m1=None, stress=None):
    """
    Calculate block shear strength of the plate or member

    Args:

        Tdb:block shear strength of the plate or member in N (float)
        A_vg:gross area of plate attached to web in shear along bolt line parallel to y axis in mm square (float)
        A_vn:net area of web cover plate attached to web in shear along bolt line parallel to y axis in mm square (float)
        A_tg:minimum gross area in tension along bolt line parallel to x-axis in mm square (float)
        A_tn:minimum net area in tension along bolt line perpendicular to shear load in mm square (float)
        f_u:ultimate stress of material in N/mm square (float)
        f_y:yield stress of material in N/mm square (float)
        gamma_m0:partial safety factor for failure in tension by yielding (float)
        gamma_m1:partial safety factor for failure at ultimate stress (float)
    Returns:
        block shear strength of the plate or member
    Note:
              Reference:
              IS 800:2007,  cl 6.4

    """

    Tdb = str(Tdb)
    A_vg = str(A_vg)
    A_vn = str(A_vn)
    A_tg = str(A_tg)
    A_tn = str(A_tn)
    f_y = str(f_y)
    f_u = str(f_u)
    gamma_m1 = str(gamma_m1)
    gamma_m0 = str(gamma_m0)

    member_block_eqn = Math(inline=True)

    if stress == "shear":
        member_block_eqn.append(
            NoEscape(r'\begin{aligned}V_{\text{dbl1}} &= \frac{A_{\text{vg}} f_{y}}{\sqrt{3} \gamma_{m0}} + \frac{0.9 A_{tn} f_{u}}{\gamma_{m1}}\\ \\'))
        member_block_eqn.append(NoEscape(r'V_{\text{dbl2}} &= \frac{0.9A_{vn} f_{u}}{\sqrt{3} \gamma_{m1}} + \frac{A_{tg} f_{y}}{\gamma_{m0}}\\ \\'))
        member_block_eqn.append(NoEscape(r'V_{\text{db}} &= \min(V_{db1},~ V_{db2})= ' + Tdb + r'\\ \\'))
        member_block_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.6.4}] \end{aligned}'))
    else:
        member_block_eqn.append(
            NoEscape(r'\begin{aligned}T_{\text{dbl1}} &= \frac{A_{\text{vg}} f_{y}}{\sqrt{3} \gamma_{m0}} + \frac{0.9 A_{tn} f_{u}}{\gamma_{m1}}\\ \\'))
        member_block_eqn.append(NoEscape(r'T_{\text{dbl2}} &= \frac{0.9A_{vn} f_{u}}{\sqrt{3} \gamma_{m1}} + \frac{A_{tg} f_{y}}{\gamma_{m0}}\\ \\'))
        member_block_eqn.append(NoEscape(r'T_{\text{db}} &= \min(T_{db1},~ T_{db2})= ' + Tdb + r'\\ \\'))
        member_block_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.6.4}] \end{aligned}'))

    return member_block_eqn


def slenderness_req():
    """
    :return:
    """

    slenderlimit_eqn = Math(inline=True)
    slenderlimit_eqn.append(NoEscape(r'\begin{aligned}\frac{K L}{r} &\leq 400\end{aligned}'))

    return slenderlimit_eqn


def cl_7_1_2_effective_slenderness_ratio(K, L, r, slender):
    """
    Calculate effective selenderness ratio

    Args:

         K:Constant according to the end condition (float)
         L:Actual length of the section in mm (float)
         r:Radius of gyration  in mm (float)
         slender:  effective selenderness ratio (float)
    Returns:
        effective selenderness ratio
    Note:
              Reference:
              IS 800:2007,  cl 7.1.2

    """
    K = str(K)
    L = str(L)
    r = str(r)
    slender = str(slender)

    slender_eqn = Math(inline=True)
    slender_eqn.append(NoEscape(r'\begin{aligned}\frac{K L}{r} &= \frac{' + K + r'\times' + L + '}{' + r + r'}\\'))
    slender_eqn.append(NoEscape(r'&= ' + slender + r'\\ \\'))
    slender_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.7.1.2}] \end{aligned}'))
    return slender_eqn


def cl_8_2_moment_capacity_member(Pmc, Mdc, M_c):
    """
    Calculate moment capacity of the section
    Args:
         Pmc:Plastic moment capacity of the member in  N-mm (float)
         Mdc:Moment deformation capacity of the member in  N-mm (float)
         M_c: Moment capacity of the section in  N-mm (float)
    Returns:
         moment capacity of the section
    Note:
              Reference:
              IS 800:2007,  cl 8.2


    """
    Pmc = str(Pmc)
    Mdc = str(Mdc)
    M_c = str(M_c)
    M_c_eqn = Math(inline=True)
    M_c_eqn.append(NoEscape(r'\begin{aligned} {M_{d}}_{\text{z}} &= \min({M_{d}}_{\text{z}},~ M_{d_c})\\'))
    M_c_eqn.append(NoEscape(r'&= \min(' + Pmc + ',' + Mdc + r')\\'))
    M_c_eqn.append(NoEscape(r'&=' + M_c + r'\\ \\'))
    M_c_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2}] \end{aligned}'))
    return M_c_eqn


def cl_8_2_1_2_plastic_moment_capacity_member(beta_b, Z_p, f_y, gamma_m0, Pmc):  # same as #todo anjali
    """
    Calculate member design moment capacity
    Args:

          beta_b:1 for plastic and compact sections & Ze/Zp for semi compact section (int)
          Z_p:Plastic section modulus of cross section mm^3 (float)
          f_y:Yield stress of the material in N/mm square  (float)
          gamma_m0:partial safety factor (float)
          Pmc:Plastic moment capacity in  N-mm (float)
    Returns:
        Plastic moment capacity in  N-mm (float)

    Note:
              Reference:
              IS 800:2007,  cl 8.2.1.2

    """

    beta_b = str(beta_b)
    Z_p = str(Z_p)
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)
    Pmc = str(Pmc)
    Pmc_eqn = Math(inline=True)
    Pmc_eqn.append(NoEscape(r'\begin{aligned} {M_{d}}_{\text{z}} &= \frac{\beta_b Z_p fy}{\gamma_{m0} \times 10^6}\\'))
    Pmc_eqn.append(NoEscape(r'&=\frac{' + beta_b + r'\times' + Z_p + r'\times' + f_y + r'}{' + gamma_m0 + r' \times 10^6}\\'))
    Pmc_eqn.append(NoEscape(r'&=' + Pmc + r'\\ \\'))
    Pmc_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2.1.2}] \end{aligned}'))

    return Pmc_eqn


def cl_8_2_1_2_plastic_moment_capacity(beta_b, Z_p, f_y, gamma_m0, Pmc, supporting_or_supported=''):
    """
    Calculate member design moment capacity
    Args:

          beta_b:1 for plastic and compact sections & Ze/Zp for semi compact section (int)
          Z_p:Plastic section modulus of cross section mm^3 (float)
          f_y:Yield stress of the material in N/mm square  (float)
          gamma_m0:partial safety factor (float)
          Pmc:Plastic moment capacity in  N-mm (float)
    Returns:
        Plastic moment capacity in  N-mm (float)

    Note:
              Reference:
              IS 800:2007,  cl 8.2.1.2

    """

    beta_b = str(beta_b)
    Z_p = str(Z_p)
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)
    Pmc = str(Pmc)
    Pmc_eqn = Math(inline=True)
    Pmc_eqn.append(NoEscape(r'\begin{aligned} {M_{d}}_{\text{z}} &= \frac{ \beta_b Z_{p_z} fy } { \gamma_{m0} }\\'))
    Pmc_eqn.append(NoEscape(r'&=\frac{' + beta_b + r'\times' + Z_p + r'\times' + f_y + r'}{' + gamma_m0 + r' \times 10^6}\\'))
    Pmc_eqn.append(NoEscape(r'&=' + Pmc + r' \\ \\'))

    if supporting_or_supported == 'Supporting':
        Pmc_eqn.append(NoEscape(r' & \text{Note: ~ The~capacity~of~the~section~is~not} \\'))
        Pmc_eqn.append(NoEscape(r' & \text{based~on~the~beam-colum~or~column~ design.} \\'))
        Pmc_eqn.append(NoEscape(r' & \text{The~actual~capacity~might~vary.} \\ \\'))

    Pmc_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2.1.2}] \end{aligned}'))

    return Pmc_eqn


def cl_8_2_1_2_plastic_moment_capacity_yy(beta_b, Z_py, f_y, gamma_m0, Pmc):

    Pmc_eqn = Math(inline=True)

    Pmc_eqn.append(NoEscape(r'\begin{aligned} {M_{d}}_{\text{y}} &= \frac{ \beta_b Z_{py} fy } { \gamma_{m0} } \\'))
    Pmc_eqn.append(NoEscape(r'&=\frac{' + str(beta_b) + r'\times' + str(Z_py) + r'\times' + str(f_y) + r'}{' + str(gamma_m0) + r' \times 10^6}\\'))
    Pmc_eqn.append(NoEscape(r'&=' + str(Pmc) + r' \\ \\'))

    Pmc_eqn.append(NoEscape(r' & \text{Note: ~ The~capacity~of~the~section~is~not} \\'))
    Pmc_eqn.append(NoEscape(r' & \text{based~on~the~beam-colum~or~column~ design.} \\'))
    Pmc_eqn.append(NoEscape(r' & \text{The~actual~capacity~might~vary.} \\ \\'))

    Pmc_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2.1.2}] \end{aligned}'))

    return Pmc_eqn


def cl_8_2_1_2_deformation_moment_capacity_member(fy, Z_e, Mdc):
    """
    Calculate moment deformation capacity
    Args:
         fy:Yield stress of the material in  N/mm square (float)
         Z_e:Elastic section modulus of cross section in  mm^3 (float)
         Mdc:Moment deformation capacity in  N-mm (float)
    Note:
              Reference:
              IS 800:2007,  cl 8.2.1.2
    Returns:
         moment deformation capacity
    """
    fy = str(fy)
    Z_e = str(Z_e)
    Mdc = str(Mdc)
    Mdc_eqn = Math(inline=True)
    Mdc_eqn.append(NoEscape(r'\begin{aligned} M_{dc} &= \frac{1.5 Z_e fy}{\gamma_{m0} \times 10^6}\\'))
    Mdc_eqn.append(NoEscape(r'&= \frac{1.5 \times' + Z_e + r'\times' + fy + r'}{1.1\times 10^6}\\'))
    Mdc_eqn.append(NoEscape(r'&= ' + Mdc + r'\\ \\'))
    Mdc_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2.1.2}] \end{aligned}'))
    return Mdc_eqn


def cl_8_4_shear_capacity_member(V_dy, V_dn, V_db=0.0, shear_case='low'):
    """
    Calculate shear capacity of member

    Args:
        V_dy: yielding capacity of plate
        V_dn: rupture capacity of plate
        V_db: block shear capacity of plate
    Returns:
         shear capacity of member
    Note:
              Reference:
              IS 800:2007,  cl 6.1

    """
    shear_capacity_eqn = Math(inline=True)
    if V_db != 0.0 and V_dn != 0.0:
        V_d = min(V_dy, V_dn, V_db)
        V_d = str(V_d)
        V_dy = str(V_dy)
        V_dn = str(V_dn)
        V_db = str(V_db)

        shear_capacity_eqn.append(NoEscape(r'\begin{aligned} V_d &= \min(S_c,~V_{d_n},~V_{d_b})\\'))
        shear_capacity_eqn.append(NoEscape(r'&= \min(' + V_dy + ',~' + V_dn + ',~' + V_db + r')\\'))

    elif V_db == 0.0 and V_dn == 0.0:
        V_d = V_dy
        V_d = str(V_d)
        V_dy = str(V_dy)
        shear_capacity_eqn.append(NoEscape(r'\begin{aligned} V_d &= S_c\\'))
        # shear_capacity_eqn.append(NoEscape(r'&=' + V_dy + r'\\'))

    elif V_db == 0.0 and V_dn != 0.0:
        V_d = min(V_dy, V_dn)
        V_d = str(V_d)
        V_dy = str(V_dy)
        V_dn = str(V_dn)
        shear_capacity_eqn.append(NoEscape(r'\begin{aligned} V_d &= \min(S_c,~V_{d_n})\\'))
        shear_capacity_eqn.append(NoEscape(r'&= \min(' + V_dy + ',~' + V_dn + r')\\'))
    elif V_db != 0.0 and V_dn == 0.0:
        V_d = min(V_dy, V_db)
        V_d = str(V_d)
        V_dy = str(V_dy)
        V_db = str(V_db)
        if shear_case == 'full':
            shear_capacity_eqn.append(NoEscape(r'\begin{aligned} V_d &= \min(V_{d_y},~V_{d_b})\\'))
        else:
            shear_capacity_eqn.append(NoEscape(r'\begin{aligned} V_d &= \min(S_c,~V_{d_b})\\'))
        shear_capacity_eqn.append(NoEscape(r'&= \min(' + V_dy + ',' + V_db + r')\\'))

    shear_capacity_eqn.append(NoEscape(r'&=' + V_d + r'\\ \\'))
    shear_capacity_eqn.append(NoEscape(r'& [\text{ Ref. IS 800:2007, Cl.6.1}] \end{aligned}'))

    return shear_capacity_eqn


def cl_8_4_shear_yielding_capacity_member(h, t, f_y, gamma_m0, V_dg, multiple=1):
    """
    Calculate shear yielding capacity of  plate (provided)
    Args:
        h:  Plate ht in mm (float)
        t:  Plate thickness in mm (float)
        f_y:Yeild strength of  plate material in N/mm square (float)
        gamma: IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']  (float)
        V_dg: Shear yeilding capacity of  plate in N (float)
        multiple:2 (int)
    Returns:
         Shear yielding capacity of  plate
     Note:
            Reference:
            IS 800:2007,  cl 10.4.3
    """

    h = str(h)
    t = str(t)
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)

    V_dg = str(V_dg)

    shear_yield_eqn = Math(inline=True)
    shear_yield_eqn.append(NoEscape(r'\begin{aligned} V_{d_y} &= \frac{A_vf_y}{\sqrt{3}\gamma_{m0}}\\'))
    if multiple == 1:
        shear_yield_eqn.append(NoEscape(r'&=\frac{' + h + r'\times' + t + r'\times' + f_y + r'}{\sqrt{3} \times' + gamma_m0 + r' \times 1000}\\'))
    else:
        multiple = str(multiple)
        shear_yield_eqn.append(
            NoEscape(r'&=\frac{' + multiple + r'\times' + h + r'\times' + t + r'\times' + f_y + r'}{\sqrt{3} \times' + gamma_m0 + r' \times 1000} \\'))
    shear_yield_eqn.append(NoEscape(r'&=' + V_dg + r' \\ \\'))
    shear_yield_eqn.append(NoEscape(r'& [\text{Ref. IS ~800:2007,~Cl.10.4.3}] \end{aligned}'))
    return shear_yield_eqn


def cl_8_4_1_plastic_shear_resistance(h, t, f_y, gamma_m0, V_dg, multiple=1):
    """
    Calculate shear yielding capacity of  plate (provided)
    Args:
        h:  Plate ht in mm (float)
        t:  Plate thickness in mm (float)
        f_y:Yeild strength of  plate material in N/mm square (float)
        gamma: IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']  (float)
        V_dg: Shear yeilding capacity of  plate in N (float)
        multiple:2 (int)
    Returns:
         Shear yielding capacity of  plate
     Note:
            Reference:
            IS 800:2007,  cl 10.4.3
    """

    h = str(h)
    t = str(t)
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)

    V_dg = str(V_dg)

    shear_yield_eqn = Math(inline=True)
    shear_yield_eqn.append(NoEscape(r'\begin{aligned} V_{p} &= \frac{A_v f_{y_w}}{\sqrt{3} \gamma_{m0}} \\'))
    if multiple == 1:
        shear_yield_eqn.append(NoEscape(r'&=\frac{' + h + r'\times' + t + r'\times' + f_y + r'}{\sqrt{3} \times' + gamma_m0 + r'}\\'))
    else:
        multiple = str(multiple)
        shear_yield_eqn.append(
            NoEscape(r'&=\frac{' + multiple + r'\times' + h + r'\times' + t + r'\times' + f_y + r'}{\sqrt{3} \times' + gamma_m0 + r'}\\'))

    shear_yield_eqn.append(NoEscape(r'&=' + V_dg + r'\\ \\'))
    shear_yield_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.4.1}] \end{aligned}'))
    return shear_yield_eqn


def AISC_J4_shear_rupture_capacity_member(h, t, n_r, d_o, fu, v_dn, gamma_m1=1.25, multiple=1):
    """
     Calculate shear rupture capacity of  plate (provided)
     Args:
          h: Height of  plate in mm (float)
          t:Thickness of  plate in mm (float)
          n_r:No of bolts provided in one line (float)
          d_o:Nominal diameter of bolt provide in plate in mm (float)
          fu: Ultimate strength of  plate material in N/mm square (float)
          v_dn: Shear rupture of plate in KN (float)
          gamma_m1: material factor of safety at ultimate load
          multiple: 1 (int)
    Returns:
          shear rupture capacity of  plate
    Note:
        Reference:
                    AISC  Sect.J4
    """
    h = str(h)
    t = str(t)
    n_r = str(n_r)
    d_o = str(d_o)
    f_u = str(fu)
    v_dn = str(v_dn)
    gamma_m1 = str(gamma_m1)
    multiple = str(multiple)
    shear_rup_eqn = Math(inline=True)
    shear_rup_eqn.append(NoEscape(r'\begin{aligned} V_{d_n} &= \frac{0.75 A_{v_n} f_u}{\sqrt{3} \gamma_{m1}}\\'))
    if multiple == 1:
        shear_rup_eqn.append(NoEscape(
            r'&=' + r'\times \frac{(' + h + '-(' + n_r + r'\times' + d_o + r'))\times' + t + r'\times' + f_u + r'}{\sqrt{3}\times' + gamma_m1 + r'}\\'))
    else:
        shear_rup_eqn.append(NoEscape(
            r'&=' + multiple + r'\times \frac{(' + h + '-(' + n_r + r'\times' + d_o + r'))\times' + t + r'\times' + f_u + r'}{\sqrt{3}\times' + gamma_m1 + r'}\\'))
    shear_rup_eqn.append(NoEscape(r'&=' + v_dn + r'\\ \\'))
    shear_rup_eqn.append(NoEscape(r'& [\text{ Ref. AISC, sect. J4}] \end{aligned}'))

    return shear_rup_eqn


def cl_9_3_combined_moment_axial_IR_section(M, M_d, N, N_d, IR, type=None):
    """
    Calculate
    Args:
         M: Moment acting on section in KN-mm (float)
         M_d:Moment capacity of the section in KN-mm (float)
         N: Axial force acting on section in KN (float)
         N_d:Tension capacity of the plate in KN (float)
         IR: Interaction ratio for combined moment and axial load (no units)
    Returns:
        mom_axial_IR_eqn: Equation to calculate IR
    Note:
            Reference:
            IS 800:2007,  cl 9.3


    """
    M = str(M)
    M_d = str(M_d)
    N = str(N)
    N_d = str(N_d)
    IR = str(IR)
    mom_axial_IR_eqn = Math(inline=True)

    if type == None:
        mom_axial_IR_eqn.append(NoEscape(r'\begin{aligned} &\frac{' + M + '}{' + M_d + r'}+\frac{' + N + '}{' + N_d + '}=' + IR + r'\\ \\'))
        mom_axial_IR_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.7}] \end{aligned}'))
    elif type == 'squared':
        mom_axial_IR_eqn.append(NoEscape(r'\begin{aligned} &(\frac{' + M + '}{' + M_d + r'})^2+(\frac{' + N + '}{' + N_d + '})^2=' + IR + r'\\ \\'))
        mom_axial_IR_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.7}] \end{aligned}'))
    return mom_axial_IR_eqn


def cl_10_2_2_min_spacing(d, parameter='pitch'):  # Todo:write condition for pitch and gauge

    """
    Calculate the min pitch distance
    Args:
      d:Diameter of provided bolt in mm (float)
    Returns:
       Minimum pitch distance in mm (float)
    Note:
        Reference:
        IS 800:2007,  cl. 10.2.2

    """
    min_pitch = 2.5 * d
    d = str(d)
    min_pitch = str(min_pitch)

    min_pitch_eqn = Math(inline=True)

    if parameter == 'pitch':
        min_pitch_eqn.append(NoEscape(r'\begin{aligned}p_{\min}&= 2.5 d\\'))
    elif parameter == 'gauge':
        min_pitch_eqn.append(NoEscape(r'\begin{aligned} g_{\min}&= 2.5 d\\'))
    else:
        min_pitch_eqn.append(NoEscape(r'\begin{aligned} p/g_{\min}&= 2.5 d\\'))
    min_pitch_eqn.append(NoEscape(r'&=2.5 \times' + d + r'\\&=' + min_pitch + r'\\ \\'))

    min_pitch_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.2.2}] \end{aligned}'))

    return min_pitch_eqn


def cl_10_2_3_1_max_spacing(t, parameter=''):  # TODO:write condition for pitch and gauge
    """
     Calculate the maximum pitch distance
     Args:
         t: Thickness of thinner plate in mm (float)
     Returns:
           Max pitch in mm (float)
     Note:
            Reference:
            IS 800:2007,  cl. 10.2.3
    """
    t1 = str(t[0])
    t2 = str(t[1])
    max_pitch_1 = 32 * min(t)
    max_pitch_2 = 300
    max_pitch = min(max_pitch_1, max_pitch_2)
    t = str(min(t))
    max_pitch = str(max_pitch)
    max_pitch_eqn = Math(inline=True)
    if parameter == 'pitch':
        max_pitch_eqn.append(NoEscape(r'\begin{aligned}p_{\max}&=\min(32t,~300)\\'))
    elif parameter == 'gauge':
        max_pitch_eqn.append(NoEscape(r'\begin{aligned}g_{\max}&=\min(32t,~300)\\'))
    else:
        max_pitch_eqn.append(NoEscape(r'\begin{aligned}p/g_{\max}&=\min(32t,~300)\\'))

    max_pitch_eqn.append(NoEscape(r'&=\min(32\times' + t + r',~ 300) \\'))
    max_pitch_eqn.append(NoEscape(r'&=\min(' + str(max_pitch_1) + r',~ 300) \\'))
    max_pitch_eqn.append(NoEscape(r'&=' + max_pitch + r' \\ \\'))

    max_pitch_eqn.append(NoEscape(r'\text{Where},~t &= \min(' + t1 + ',' + t2 + r')\\ \\'))

    max_pitch_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.2.3}] \end{aligned}'))

    return max_pitch_eqn


# def cl_10_2_4_2_min_edge_end_dist(d_0, edge_type='Sheared or hand flame cut', parameter='end_dist'):
#     """
#     Calculate minimum end and edge distance
#     Args:
#          d - Nominal diameter of fastener in mm (float)
#          bolt_hole_type - Either 'Standard', 'Over-sized', 'Short Slot' or 'Long Slot' (str)
#          edge_type - Either 'hand_flame_cut' or 'machine_flame_cut' (str)
#          parameter - edge or end distance required to return the specific equation (str)
#     Returns:
#             Equation for minimum end and edge distance from the centre of any hole to the nearest edge of a plate in mm (float)
#     Note:
#         Reference:
#         IS 800:2007, cl. 10.2.4.2
#     """
#     if edge_type == 'Sheared or hand flame cut':
#         end_edge_multiplier = 1.7
#     else:
#         # TODO : bolt_hole_type == 'machine_flame_cut' is given in else
#         end_edge_multiplier = 1.5
#
#     min_end_edge_dist = round(end_edge_multiplier * d_0, 2)
#
#     d_0 = str(d_0)
#     end_edge_multiplier = str(end_edge_multiplier)
#     min_end_edge_dist = str(min_end_edge_dist)
#
#     end_edge_eqn = Math(inline=True)
#     if parameter == 'end_dist':
#         end_edge_eqn.append(NoEscape(r'\begin{aligned}e_{min} &= ' + end_edge_multiplier + r'~d_0 \\'))
#     elif parameter == 'edge_dist':
#         end_edge_eqn.append(NoEscape(r'\begin{aligned}e`_{min} &= ' + end_edge_multiplier + r'~d_0 \\'))
#     else:
#         end_edge_eqn.append(NoEscape(r'\begin{aligned}e/e`_{min} &= ' + end_edge_multiplier + r'~d_0 \\'))
#
#     end_edge_eqn.append(NoEscape(r'&= ' + end_edge_multiplier + r'\times' + d_0 + r'\\'))
#     end_edge_eqn.append(NoEscape(r'&=' + min_end_edge_dist + r'\\'))
#     end_edge_eqn.append(NoEscape(r'& [Ref.~IS~800:2007,~Cl.~10.2.4.2] \end{aligned}'))
#     return end_edge_eqn

def cl_10_2_4_2_min_edge_end_dist(d_0, edge_type='Sheared or hand flame cut', parameter='end_dist'):
    """
    Calculate minimum end and edge distance
    Args:
         d - Nominal diameter of fastener in mm (float)
         bolt_hole_type - Either 'Standard', 'Over-sized', 'Short Slot' or 'Long Slot' (str)
         edge_type - Either 'hand_flame_cut' or 'machine_flame_cut' (str)
         parameter - edge or end distance required to return the specific equation (str)
    Returns:
            Equation for minimum end and edge distance from the centre of any hole to the nearest edge of a plate in mm (float)
    Note:
        Reference:
        IS 800:2007, cl. 10.2.4.2
    """
    if edge_type == 'Sheared or hand flame cut':
        end_edge_multiplier = 1.7
    else:
        # TODO : bolt_hole_type == 'machine_flame_cut' is given in else
        end_edge_multiplier = 1.5

    min_end_edge_dist = round(end_edge_multiplier * d_0, 2)

    d_0 = str(d_0)
    end_edge_multiplier = str(end_edge_multiplier)
    min_end_edge_dist = str(min_end_edge_dist)

    end_edge_eqn = Math(inline=True)
    if parameter == 'end_dist':
        end_edge_eqn.append(NoEscape(r'\begin{aligned}e_{\min} &= ' + end_edge_multiplier + r' d_0 \\'))
    elif parameter == 'edge_dist':
        end_edge_eqn.append(NoEscape(r'\begin{aligned}e\textquotesingle_{\min} &= ' + end_edge_multiplier + r' d_0 \\'))
    else:
        end_edge_eqn.append(NoEscape(r'\begin{aligned}e/e\textquotesingle_{\min} &= ' + end_edge_multiplier + r' d_0 \\'))

    end_edge_eqn.append(NoEscape(r'&= ' + end_edge_multiplier + r'\times' + d_0 + r'\\'))
    end_edge_eqn.append(NoEscape(r'&=' + min_end_edge_dist + r'\\ \\'))

    end_edge_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.2.4.2}] \end{aligned}'))
    return end_edge_eqn


# def cl_10_2_4_3_max_edge_end_dist(t_fu_fy, corrosive_influences=False, parameter='end_dist'):
#     """
#     Calculate maximum end and edge distance(new)
#      Args:
#
#          t_fu_fy: List of tuples with thickness fu fy of each connecting member.
#                     ex: [(thickness_plate_1, fu_plate_1, fy_plate_1),(thickness_plate_1, fu_plate_1, fy_plate_1)]
#          corrosive_influences: Whether the members are exposed to corrosive influences or not (Boolean)
#
#     Returns:
#          Maximum edge distance to the nearest line of fasteners from an edge of any un-stiffened part in mm (float)
#
#     Note:
#             Reference:
#             IS 800:2007, cl. 10.2.4.3
#     """
#     t_epsilon_considered = t_fu_fy[0][0] * math.sqrt(250 / float(t_fu_fy[0][2]))
#     t_considered = t_fu_fy[0][0]
#     t_min = t_considered
#     for i in t_fu_fy:
#         t = i[0]
#         f_y = i[2]
#         if f_y > 0:
#             epsilon = math.sqrt(250 / f_y)
#             if t * epsilon <= t_epsilon_considered:
#                 t_epsilon_considered = t * epsilon
#                 t_considered = t
#             if t < t_min:
#                 t_min = t
#
#     if corrosive_influences is True:
#         max_edge_dist = round(40.0 + 4 * t_min, 2)
#     else:
#         max_edge_dist = round(12 * t_epsilon_considered, 2)
#
#     max_edge_dist = str(max_edge_dist)
#     t1=str(t_fu_fy[0][0])
#     t2=str(t_fu_fy[1][0])
#     fy1 = str(t_fu_fy[0][2])
#     fy2 = str(t_fu_fy[1][2])
#     max_end_edge_eqn = Math(inline=True)
#
#     if corrosive_influences is False:
#         if parameter == 'end_dist':
#             max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e_{max} &= 12~ t~ \varepsilon ;~\varepsilon = \sqrt{\frac{250}{f_y}}\\'))
#         else: #'edge_dist'
#             max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e`_{max} &= 12~ t~ \varepsilon ;~\varepsilon = \sqrt{\frac{250}{f_y}}\\'))
#         # max_end_edge_eqn.append(NoEscape(r'\varepsilon &= \sqrt{\frac{250}{f_y}}\\'))
#         max_end_edge_eqn.append(NoEscape(r'e1 &= 12 \times ' + t1 + r'\times \sqrt{\frac{250}{' + fy1 + r'}}\\'))
#         max_end_edge_eqn.append(NoEscape(r'e2 &= 12 \times' + t2 + r'\times\sqrt{\frac{250}{' + fy2 + r'}}\\'))
#         if parameter == 'end_dist':
#             max_end_edge_eqn.append(NoEscape(r'e_{max}&=min(e1,e2)=' + max_edge_dist +r'\\'))
#         else: #'edge_dist'
#             max_end_edge_eqn.append(NoEscape(r'e`_{max}&=min(e1,e2)=' + max_edge_dist +r'\\'))
#         # max_end_edge_eqn.append(NoEscape(r' &=' + max_edge_dist + r'\\'))
#         max_end_edge_eqn.append(NoEscape(r'& [Ref.~IS~800:2007,~Cl.~10.2.4.3] \end{aligned}'))
#
#     else:
#         max_end_edge_eqn.append(NoEscape(r'\begin{aligned} Member(s) exposed to corrosive influences = True \\'))
#         if parameter == 'end_dist':
#             max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e_{max}&=40 + 4t\\'))
#         else: #'edge_dist'
#             max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e`_{max}&=40 + 4t\\'))
#
#         if int(t2) > 0:
#             max_end_edge_eqn.append(NoEscape(r'Where,~ t&= min(' + t1 +','+t2+r')\\'))
#         else:
#             max_end_edge_eqn.append(NoEscape(r'Where,~ t&= ' + t1 + r')\\'))
#
#         if parameter == 'end_dist':
#             max_end_edge_eqn.append(NoEscape(r'e_{max}&='+max_edge_dist+r'\\'))
#         else: #'edge_dist'
#             max_end_edge_eqn.append(NoEscape(r'e`_{max}&='+max_edge_dist+r'\\'))
#
#         max_end_edge_eqn.append(NoEscape(r'& [Ref.~IS~800:2007,~Cl.~10.2.4.3] \end{aligned}'))
#
#     return max_end_edge_eqn


def cl_10_2_4_3_max_edge_end_dist(t_fu_fy, corrosive_influences=False, parameter='end_dist'):
    """
    Calculate maximum end and edge distance(new)
     Args:
         t_fu_fy: List of tuples with thickness fu fy of each connecting member.
                    ex: [(thickness_plate_1, fu_plate_1, fy_plate_1),(thickness_plate_1, fu_plate_1, fy_plate_1)]
         corrosive_influences: Whether the members are exposed to corrosive influences or not (Boolean)
    Returns:
         Maximum edge distance to the nearest line of fasteners from an edge of any un-stiffened part in mm (float)
    Note:
            Reference:
            IS 800:2007, cl. 10.2.4.3
    """
    # t_epsilon_considered = t_fu_fy[0][0] * math.sqrt(250 / float(t_fu_fy[0][2]))
    # t_considered = t_fu_fy[0][0]
    # t_min = t_considered
    # for i in t_fu_fy:
    #     t = i[0]
    #     f_y = i[2]
    #     if f_y > 0:
    #         epsilon = math.sqrt(250 / f_y)
    #         if t * epsilon <= t_epsilon_considered:
    #             t_epsilon_considered = t * epsilon
    #             t_considered = t
    #         if t < t_min:
    #             t_min = t
    #
    # if corrosive_influences is True:
    #     max_edge_dist = round(40.0 + 4 * t_min, 2)
    # else:
    #     max_edge_dist = round(12 * t_epsilon_considered, 2)

    # max_edge_dist = str(max_edge_dist)
    e1 = round(12*t_fu_fy[0][0]*math.sqrt(250/t_fu_fy[0][2]),2)
    e2 = round(12 * t_fu_fy[1][0] * math.sqrt(250 / t_fu_fy[1][2]),2)
    max_edge_dist = str(min(e1,e2))
    e1 = str(e1)
    e2 = str(e2)
    t1 = str(t_fu_fy[0][0])
    t2 = str(t_fu_fy[1][0])
    fy1 = str(t_fu_fy[0][2])
    fy2 = str(t_fu_fy[1][2])

    max_end_edge_eqn = Math(inline=True)

    if corrosive_influences is False:
        if parameter == 'end_dist':
            max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e_{\max} &= 12 t \varepsilon ;~\varepsilon = \sqrt{\frac{250}{f_y}}\\'))
        else:  # 'edge_dist'
            max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e\textquotesingle_{\max} &= 12 t \varepsilon ;~\varepsilon = \sqrt{\frac{250}{f_y}}\\'))
        # max_end_edge_eqn.append(NoEscape(r'\varepsilon &= \sqrt{\frac{250}{f_y}}\\'))
        max_end_edge_eqn.append(NoEscape(r'e_1 &= 12 \times ' + t1 + r'\times \sqrt{\frac{250}{' + fy1 + r'}} = ' + e1 + r'\\'))
        max_end_edge_eqn.append(NoEscape(r'e_2 &= 12 \times' + t2 + r'\times\sqrt{\frac{250}{' + fy2 + r'}} = ' + e2 + r'\\'))
        if parameter == 'end_dist':
            max_end_edge_eqn.append(NoEscape(r'e_{\max}&=\min(e_1,~e_2)=' + max_edge_dist + r' \\ \\'))
        else:  # 'edge_dist'
            max_end_edge_eqn.append(NoEscape(r'e\textquotesingle_{\max}&=min(e_1,~e_2)=' + max_edge_dist + r' \\ \\'))
        # max_end_edge_eqn.append(NoEscape(r' &=' + max_edge_dist + r'\\'))

        max_end_edge_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.2.4.3}] \end{aligned}'))

    else:
        if parameter == 'end_dist':
            max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e_{\max}&=40 + 4t\\'))
        else:  # 'edge_dist'
            max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e\textquotesingle_{\max}&=40 + 4t\\'))

        if int(float(t2)) <= 0.0:  # for cases where only a single plate is present
            max_end_edge_eqn.append(NoEscape(r'\text{Where},~ t&= ' + t1 + r'\\'))
        else:
            max_end_edge_eqn.append(NoEscape(r'\text{Where}, t&= \min(' + t1 + ',' + t2 + r')\\'))

        if int(float(t2)) <= 0.0:  # for cases where only a single plate is present
            min_t = t1
        else:
            min_t = min(int(float(t1)), int(float(t2)))

        max_edge_dist = str(round(40.0 + 4 * min_t, 2))
        min_t = str(min_t)
        if parameter == 'end_dist':
            max_end_edge_eqn.append(NoEscape(r'&= 40 + (4 \times ' + min_t + r') \\'))
            max_end_edge_eqn.append(NoEscape(r'e_{\max}&=' + max_edge_dist + r' \\\\ '))
        else:  # 'edge_dist'
            max_end_edge_eqn.append(NoEscape(r'&= 40 + (4 \times ' + min_t + r') \\'))
            max_end_edge_eqn.append(NoEscape(r'e\textquotesingle_{\max}&=' + max_edge_dist + r'\\ \\'))

        max_end_edge_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.2.4.3}] \end{aligned}'))

    return max_end_edge_eqn


def cl_10_3_2_bolt_capacity(bolt_shear_capacity, bolt_bearing_capacity, bolt_capacity):
    """
    Calculate bolt  capacity (min of bearing and shearing)

    Args:
         bolt_shear_capacity: Bolt shearing capacity in KN (float)

         bolt_bearing_capacity: Bolt bearing capacity in KN (float)

         bolt_capacity: Bolt  capacity (min of bearing and shearing) in KN (float)

    Returns:
            Capacity  of bolt (min of bearing and shearing) in KN (float)
    Note:
            Reference:
            IS 800:2007, cl. 10.3.2


    """
    bolt_shear_capacity = str(bolt_shear_capacity)
    bolt_bearing_capacity = str(bolt_bearing_capacity)
    bolt_capacity = str(bolt_capacity)
    bolt_capacity_eqn = Math(inline=True)
    bolt_capacity_eqn.append(NoEscape(r'\begin{aligned} V_{\text{db}} &= \min~ (V_{\text{dsb}},~ V_{\text{dpb}})\\'))
    bolt_capacity_eqn.append(NoEscape(r'&= \min~ (' + bolt_shear_capacity + ',~' + bolt_bearing_capacity + r')\\'))
    bolt_capacity_eqn.append(NoEscape(r'&=' + bolt_capacity + r'\\ \\'))
    bolt_capacity_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.2}] \end{aligned}'))

    return bolt_capacity_eqn


def cl_10_3_3_bolt_shear_capacity(f_ub, n_n, a_nb, gamma_mb, bolt_shear_capacity):
    """
    Calculate bolt shearing capacity
    Args:
         f_ub: Ultimate tensile strength of the bolt in MPa (float)
         n_n: Number of shear planes with threads intercepting the shear plane (int)

         a_nb: Net Shear area of the bolt at threads in sq. mm  (float)

         gamma_mb: Partial safety factor =1.25 [Ref: Table 5, cl.5.4.1,IS 800:2007]
         bolt_shear_capacity: Bolt shear capacity in KN  (float)
    Returns:
            Shear capacity of bolt(provided ) in KN  (float)
    Note:
            Reference:
            IS 800:2007, cl. 10.3.3

    """
    f_ub = str(f_ub)
    n_n = str(n_n)
    a_nb = str(a_nb)
    gamma_mb = str(gamma_mb)
    bolt_shear_capacity = str(bolt_shear_capacity)
    bolt_shear_eqn = Math(inline=True)
    bolt_shear_eqn.append(NoEscape(r'\begin{aligned}V_{\text{dsb}} &= \frac{f_{ub} n_n A_{nb}}{\sqrt{3} \gamma_{mb}}\\'))
    bolt_shear_eqn.append(NoEscape(r'&= \frac{' + f_ub + r'\times' + n_n + r'\times' + a_nb + r'}{1000\times\sqrt{3}~\times~' + gamma_mb + r'}\\'))
    bolt_shear_eqn.append(NoEscape(r'&= ' + bolt_shear_capacity + r'\\ \\'))
    bolt_shear_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.3}] \end{aligned}'))

    return bolt_shear_eqn


# def cl_10_3_3_2_large_grip_req():
#     """
#      Returns:
#         Reduced bolt capacity  in KN (float)
#     Note:
#               Reference:
#               IS 800:2007,  cl 10.3.3.2
#     """
#     large_grip_eqn = Math(inline=True)
#     large_grip_eqn.append(NoEscape(r'\begin{aligned} &if~l_g \geq 5 * d~then~\beta_{lg} = 8/(3+l_g/d)\\'))
#     large_grip_eqn.append(NoEscape(r' &if~l_g \leq 5 * d~then~\beta_{lg} = 1\\'))
#     large_grip_eqn.append(NoEscape(r'& where,\\'))
#     large_grip_eqn.append(NoEscape(r'&  l_g ~=~plate.thk~+~member.thk \\'))
#     large_grip_eqn.append(NoEscape(r'& if~\beta_{lg} \geq \beta_{lj}~then~\beta_{lg} = \beta_{lj} \\'))
#     large_grip_eqn.append(NoEscape(r'& V_{\text{rd}} = \beta_{lg} * V_{\text{db}} \\'))
#     large_grip_eqn.append(NoEscape(r'&[Ref.~IS~800:2007,~Cl.~10.3.3.2]\end{aligned}'))
#     return large_grip_eqn
#
#
# def cl_10_3_3_2_large_grip_check(d, pt, mt, blj, blg):
#
#     l_g = pt + mt
#     l_g1 = str(l_g)
#     pt1 = str(pt)
#     mt1 = str(mt)
#     blj1 = str(blj)
#     blg1 = str(blg)
#     d1= str(d)
#     d2 = str((5*d))
#
#
#     large_grip_eqn = Math(inline=True)
#     # long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~l\leq 15 * d~then~V_{\text{rd}} = \beta_{lj} * V_{\text{db}} \\'))
#     # long_joint_bolted_eqn.append(NoEscape(r'& where,\\'))
#
#     if l_g > 5 * d :
#         large_grip_eqn.append(NoEscape(r'\begin{aligned} l_g & = ~plate.thk~+~member.thk \\'))
#         large_grip_eqn.append(NoEscape(r' &= '+pt1+'+'+mt1+ '='+l_g1+ r'\\'))
#         large_grip_eqn.append(NoEscape(r'&5~*~d= 5 \times'+d1+r' ='+d2+r' \\'))
#         large_grip_eqn.append(NoEscape(r'&since,~l_g \geq 5 * d~then~\beta_{lg} = 8/(3+l_g/d)\\'))
#         large_grip_eqn.append(NoEscape(r'&\beta_{lg}= 8/(3+ '+l_g1+'/'+d1+r') = '+blg1+r'\\'))
#         if blg>blj:
#             large_grip_eqn.append(NoEscape(r'&since,~\beta_{lg} \geq \beta_{lj},\beta_{lg} = '+blj1+r' \\'))
#         else:
#             large_grip_eqn.append(NoEscape(r'&since,~\beta_{lg} \leq \beta_{lj},\beta_{lg} = ' + blg1 + r' \\'))
#
#     else:
#         large_grip_eqn.append(NoEscape(r'\begin{aligned} l_g & = ~plate.thk~+~member.thk \\'))
#         large_grip_eqn.append(NoEscape(r' &= ' + pt1 + '+' + mt1 + '=' + l_g1 + r'\\'))
#         large_grip_eqn.append(NoEscape(r'&5~*~d~= 5 \times' + d1 + r' \\'))
#         large_grip_eqn.append(NoEscape(r'&since,~l_g \leq 5 * d~then~\beta_{lg} = 1.0\\'))
#     large_grip_eqn.append(NoEscape(r'&[Ref.~IS~800:2007,~Cl.~10.3.3.2]\end{aligned}'))
#
#     return large_grip_eqn


def cl_10_3_4_calculate_kb(e, p, d, fub, fu):
    """
    Calculate kb provided to find bearing capacity of bolt
    Args:
        e:End distance of the fastener along bearing direction in mm (float)
        p:Pitch distance of the fastener along bearing direction in mm (float)
        d: diameter of the bolt in mm (float)
        fub: Ultimate tensile strength of the bolt in MPa (float)
        fu:Ultimate tensile strength of the plate in MPa (float)

    Returns:
         kb  to find bearing capacity of bolt
    Note:
            Reference:
            IS 800:2007,  cl 10.3.4

    """

    kb1 = round((e / (3.0 * d)), 2)
    kb2 = round((p / (3.0 * d) - 0.25), 2)
    kb3 = round((fub / fu), 2)
    kb4 = 1.0
    kb_1 = min(kb1, kb2, kb3, kb4)
    kb_2 = min(kb1, kb3, kb4)
    pitch = p
    e = str(e)
    p = str(p)
    d = str(d)
    fub = str(fub)
    fu = str(fu)
    kb1 = str(kb1)
    kb2 = str(kb2)
    kb3 = str(kb3)
    kb4 = str(kb4)
    kb_1 = str(kb_1)
    kb_2 = str(kb_2)
    kb_eqn = Math(inline=True)
    if pitch != 0:
        kb_eqn.append(NoEscape(r'\begin{aligned} k_b & = \min \Bigg(\frac{e}{3d_0},~\frac{p}{3d_0}-0.25,~\frac{f_{ub}}{f_u},~1.0 \Bigg) \\'))
        kb_eqn.append(NoEscape(
            r'& = \min \Bigg(\frac{' + e + r'}{3\times' + d + r'},~\frac{' + p + r'}{3\times' + d + r'}-0.25,~\frac{' + fub + '}{' + fu + r'},~1.0 \Bigg)\\'))
        kb_eqn.append(NoEscape(r'& = \min(' + kb1 + ',' + kb2 + ',' + kb3 + ',' + kb4 + r')\\'))
        kb_eqn.append(NoEscape(r'& = ' + kb_1 + r'\\ \\'))
        kb_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.4}] \end{aligned}'))

    else:
        kb_eqn.append(NoEscape(r'\begin{aligned} k_b &= \min\Bigg(\frac{e}{3d_0},~\frac{f_{ub}}{f_u},~1.0 \Bigg)\\'))
        kb_eqn.append(NoEscape(r'& = \min \Bigg(\frac{' + e + r'}{3\times' + d + r'},~\frac{' + fub + '}{' + fu + r'},~1.0 \Bigg)\\'))
        kb_eqn.append(NoEscape(r'& = \min(' + kb1 + ',~' + kb3 + ',~' + kb4 + r')\\'))
        kb_eqn.append(NoEscape(r'& = ' + kb_2 + r'\\ \\'))
        kb_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.4}] \end{aligned}'))

    return kb_eqn


def cl_10_3_4_bolt_bearing_capacity(k_b, d, conn_plates_t_fu_fy, gamma_mb, bolt_bearing_capacity, hole_type =''):
    """
    Calculate bolt bearing capacity of bolt

    Args:
        k_b:  min(e/(3.0*d_0), p/(3.0*d_0)-0.25, f_ub/f_u, 1.0)

        d: Diameter of bolt in mm (float)
        conn_plates_t_fu_fy: Ultimate tensile strength of the plate in MPa (float)
        gamma_mb:Partial safety factor =1.25 [Ref: Table 5, cl.5.4.1,IS 800:2007]
        bolt_bearing_capacity: Bolt bearing capacity in KN (float)
        hole_type: type of bolt hole (str)
    Returns:
            Bearing capacity of bolt(provided ) in KN  (float)
    Note:
            Reference:
            IS 800:2007, cl. 10.3.4


    """
    t_fu_prev = conn_plates_t_fu_fy[0][0] * conn_plates_t_fu_fy[0][1]
    t = conn_plates_t_fu_fy[0][0]
    f_u = conn_plates_t_fu_fy[0][1]
    for i in conn_plates_t_fu_fy:
        t_fu = i[0] * i[1]
        if i[0] or i[1] or i[2] > 0:
            if t_fu <= t_fu_prev:
                t = i[0]
                f_u = i[1]

    k_b = str(round(k_b, 2))
    d = str(d)
    t = str(t)
    f_u = str(f_u)
    gamma_mb = str(gamma_mb)

    bolt_bearing_eqn = Math(inline=True)
    bolt_bearing_eqn.append(NoEscape(r'\begin{aligned}V_{\text{dpb}} &= \frac{2.5 k_b d t f_u}{\gamma_{mb}}\\'))
    bolt_bearing_eqn.append(NoEscape(r'&= \frac{2.5 \times ' + k_b + r'\times' + d + r'\times' + t + r'\times' + f_u + r'}{1000\times' + gamma_mb + r'}\\'))

    if str(hole_type) == 'Over-sized' or str(hole_type) == 'short_slot':
        bolt_bearing_eqn.append(NoEscape(r'&=' + str(round(bolt_bearing_capacity / 0.7, 2)) + r'\\'))
        bolt_bearing_eqn.append(NoEscape(r'&= 0.7 \times' + str(round(bolt_bearing_capacity / 0.7, 2)) + r'\\'))
        bolt_bearing_eqn.append(NoEscape(r'&=' + str(bolt_bearing_capacity) + r'\\ \\'))

        bolt_bearing_eqn.append(NoEscape(r'& \text{Note: The bearing capacity is reduced} \\'))
        bolt_bearing_eqn.append(NoEscape(r'& \text{since the hole type is Over-sized} \\'))
        bolt_bearing_eqn.append(NoEscape(r'& \text{or Short-slotted.} \\ \\'))

    elif str(hole_type) == 'long_slot':
        bolt_bearing_eqn.append(NoEscape(r'&=' + str(round(bolt_bearing_capacity / 0.5, 2)) + r'\\'))
        bolt_bearing_eqn.append(NoEscape(r'&= 0.5 \times' + str(round(bolt_bearing_capacity / 0.5, 2)) + r'\\'))
        bolt_bearing_eqn.append(NoEscape(r'&=' + str(bolt_bearing_capacity) + r'\\ \\'))

        bolt_bearing_eqn.append(NoEscape(r'& \text{Note: The bearing capacity is reduced} \\'))
        bolt_bearing_eqn.append(NoEscape(r'& \text{since the hole type is Long-slotted.} \\'))
    else:
        bolt_bearing_eqn.append(NoEscape(r'&=' + str(bolt_bearing_capacity) + r'\\ \\'))

    bolt_bearing_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.4}] \end{aligned}'))

    return bolt_bearing_eqn


def no_bolts(no_of_bolts, location='out'):
    """ """
    no_of_bolts = str(no_of_bolts)

    number = Math(inline=True)
    if location == 'out':
        number.append(NoEscape(r'\begin{aligned} n_{\text{out}} = ' + no_of_bolts + r' \end{aligned}'))
    else:  # location == 'in'
        number.append(NoEscape(r'\begin{aligned} n_{\text{in}} = ' + no_of_bolts + r' \end{aligned}'))

    return number


def tension_demand_per_bolt(total_tension_demand, no_of_bolts):
    """ """
    tension_per_bolt = round((total_tension_demand / no_of_bolts), 2)
    tension_per_bolt = str(tension_per_bolt)
    total_tension_demand = str(total_tension_demand)

    tension_demand = Math(inline=True)
    tension_demand.append(NoEscape(r'\begin{aligned} T_{\text{b}} &= \frac{P_{t}}{n_{\text{out}} / 2} \\'))
    tension_demand.append(NoEscape(r' &= \frac{' + total_tension_demand + r'}{' + str(2 * no_of_bolts) + r'/ 2} \\'))
    tension_demand.append(NoEscape(r' &= \frac{' + total_tension_demand + r'}{' + str(no_of_bolts) + r'} \\'))
    tension_demand.append(NoEscape(r' &= ' + tension_per_bolt + r' \end{aligned}'))

    return tension_demand


def cl_10_3_5_bearing_bolt_tension_resistance(f_ub, f_yb, A_sb, A_n, tension_capacity, fabrication=KEY_DP_FAB_FIELD):
    """
    Calculate design tensile strength of bearing bolt
    Args:
        f_ub - Ultimate tensile strength of the bolt in MPa (float)
        f_yb - Yield strength of the bolt in MPa (float)
        A_sb - Shank area of bolt in sq. mm  (float)
        A_n - Net tensile stress area of the bolts as per IS 1367 in sq. mm  (float)
        tension_capacity - Tension resistance/capacity of a bolt in KN (float)
    return:
        T_db - Design tensile strength of bearing bolt in N (float)
    Note:
        Reference:
        IS 800:2007,  cl 10.3.5
    """
    gamma_mb = IS800_2007.cl_5_4_1_Table_5['gamma_mb'][fabrication]
    gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']

    tension_capacity_1 = round((0.9 * f_ub * A_n * 10 ** -3) / gamma_mb, 2)
    tension_capacity_1 = str(tension_capacity_1)
    tension_capacity_2 = round(f_yb * A_sb * (gamma_mb / gamma_m0) * 10 ** -3, 2)
    tension_capacity_2 = str(tension_capacity_2)
    f_ub = str(f_ub)
    f_yb = str(f_yb)
    A_sb = str(A_sb)
    A_n = str(A_n)
    gamma_mb = str(gamma_mb)
    gamma_m0 = str(gamma_m0)

    tension_capacity = str(tension_capacity)
    tension_resistance = Math(inline=True)
    tension_resistance.append(NoEscape(r'\begin{aligned} T_{\text{db}} &= 0.90 f_{ub} A_n~/~\gamma_{mb} \\'))
    tension_resistance.append(NoEscape(r'&  ~<~ f_{yb} A_{sb} (\gamma_{mb}~/~\gamma_{m0}) \\'))
    tension_resistance.append(NoEscape(r'&= \min \Big(0.90' + r'\times' + f_ub + r'\times' + A_n + r'~/~' + gamma_mb + r',~ \\'))
    tension_resistance.append(NoEscape(r'& ~~~~~~~~~~' + f_yb + r'\times' + A_sb + r'\times(' + gamma_mb + '/' + gamma_m0 + r') \Big) \\'))
    tension_resistance.append(NoEscape(r'&= \min (' + tension_capacity_1 + r',~ ' + tension_capacity_2 + r') \\'))
    tension_resistance.append(NoEscape(r'&= ' + tension_capacity + r'\\ \\'))
    tension_resistance.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.3.5}] \end{aligned}'))

    return tension_resistance


def cl_10_4_5_hsfg_bolt_tension_resistance(f_ub, f_yb, A_sb, A_n, tension_capacity, fabrication=KEY_DP_FAB_FIELD):
    """
    Calculate design tensile strength of friction grip bolt
    Args:
        f_ub - Ultimate tensile strength of the bolt in MPa (float)
        f_yb - Yield strength of the bolt in MPa (float)
        A_sb - Shank area of bolt in sq. mm  (float)
        A_n - Net tensile stress area of the bolts as per IS 1367 in sq. mm  (float)
        tension_capacity - Tension resistance/capacity of a bolt in KN (float)
    return:
        T_db - Design tensile strength of bearing bolt in N (float)
    Note:
        Reference:
        IS 800:2007,  cl 10.3.5
    """
    gamma_mf = IS800_2007.cl_5_4_1_Table_5['gamma_mf'][fabrication]
    gamma_m1 = IS800_2007.cl_5_4_1_Table_5['gamma_m1']['ultimate_stress']
    gamma_m0 = IS800_2007.cl_5_4_1_Table_5['gamma_m0']['yielding']

    tension_capacity_1 = round((0.9 * f_ub * A_n * 10 ** -3) / gamma_mf, 2)
    tension_capacity_1 = str(tension_capacity_1)

    tension_capacity_2 = round(f_yb * A_sb * (gamma_m1 / gamma_m0) * 10 ** -3, 2)
    tension_capacity_2 = str(tension_capacity_2)

    f_ub = str(f_ub)
    f_yb = str(f_yb)
    A_sb = str(A_sb)
    A_n = str(A_n)
    gamma_mf = str(gamma_mf)
    gamma_m1 = str(gamma_m1)
    gamma_m0 = str(gamma_m0)

    tension_capacity = str(tension_capacity)
    tension_resistance = Math(inline=True)
    tension_resistance.append(NoEscape(r'\begin{aligned} T_{f} &= 0.90 f_{ub} A_n~/~\gamma_{mf} \\'))
    tension_resistance.append(NoEscape(r'&  ~<~ f_{yb} A_{sb} (\gamma_{m1}~/~\gamma_{m0}) \\'))
    tension_resistance.append(NoEscape(r'&= \min \Big(0.90' + r'\times' + f_ub + r'\times' + A_n + r'~/~' + gamma_mf + r',~ \\'))
    tension_resistance.append(NoEscape(r'& ~~~~~~~~~~' + f_yb + r'\times' + A_sb + r'\times(' + gamma_m1 + '/' + gamma_m0 + r') \Big) \\'))
    tension_resistance.append(NoEscape(r'&= \min (' + tension_capacity_1 + r',~ ' + tension_capacity_2 + r') \\'))
    tension_resistance.append(NoEscape(r'&= ' + tension_capacity + r'\\ \\'))
    tension_resistance.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.5}] \end{aligned}'))

    return tension_resistance


def cl_10_3_6_bearing_bolt_combined_shear_and_tension(V_sb, V_db, T_b, T_db, value):  # Todo:not done
    """
    Check for bolt subjected to combined shear and tension
    Args:
        V_sb - factored shear force acting on the bolt,
        V_db - design shear capacity,
        T_b - factored tensile force acting on the bolt,
        T_db - design tension capacity.
    Returns:
        combined shear and friction value
    Note:
        Reference:
        IS 800:2007,  cl 10.3.6
    """
    V_sb = str(V_sb)
    V_db = str(V_db)
    T_b = str(T_b)
    T_db = str(T_db)
    value = str(value)

    combined_capacity_eqn = Math(inline=True)
    combined_capacity_eqn.append(NoEscape(r'\begin{aligned}\bigg(\frac{V_{sb}}{V_{\text{db}}}\bigg)^2 &+ \bigg(\frac{T_{\text{b}}}{T_{\text{db}}}\bigg)^2  \leq 1.0\\'))
    combined_capacity_eqn.append(NoEscape(r'\bigg(\frac{' + V_sb + '}{' + V_db + r'}\bigg)^2 &+ \bigg(\frac{' + T_b + '}{' + T_db + r'}\bigg)^2 = '
                                          + value + r'\\ \\'))
    combined_capacity_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.6}] \end{aligned}'))

    return combined_capacity_eqn


def cl_10_4_3_HSFG_bolt_capacity(mu_f, n_e, K_h, fub, Anb, gamma_mf, capacity):
    """
    Calculate design shear strength of friction grip bolt as governed by slip
 
    Args:
         mu_f:Coefficient of friction (slip factor) as specified in Table 20 , IS 800:2007
           
         n_e:Number of  effective interfaces offering  frictional resistance to slip (int)
         K_h:1 for bolts in clearence holes and 0.85 for bolts in oversized holes
         fub: Ultimate tensile strength of the bolt in KN (float)
           
         Anb: Net area of bolt in mm square
         gamma_mf:Partial safety factor  [Ref: Table 5, cl.5.4.1,IS 800:2007]
         capacity: Design shear strength of friction grip bolt as governed by slip in N (float)

    Returns:
           Design shear strength of friction grip bolt as governed by slip in N (float)

    Note:
            Reference:
            IS 800:2007,  cl 10.4.3

    """
    mu_f = str(mu_f)
    n_e = str(n_e)
    K_h = str(K_h)
    fub = str(fub)
    Anb = str(Anb)
    gamma_mf = str(gamma_mf)
    capacity = str(capacity)

    HSFG_bolt_capacity_eqn = Math(inline=True)
    HSFG_bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{dsf} & = \frac{\mu_f n_e  K_h F_o}{\gamma_{mf}}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r' \text{Where}~&, F_o = 0.7f_{ub} A_{nb} \\ \\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'V_{dsf} & = \frac{' + mu_f + r'\times' + n_e + r'\times' + K_h + r'\times 0.7 \times' + fub + r'\times'
                                           + Anb + r'}{' + gamma_mf + r' \times 10^{3}}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'& =' + capacity + r'\\ \\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.4.3}]\end{aligned}'))

    return HSFG_bolt_capacity_eqn


def cl_10_4_7_tension_in_bolt_due_to_prying(T_e, l_v, f_o, b_e, t, f_y, end_dist, pre_tensioned, beta, Q, l_e, eta=1.5):
    """Calculate prying force of friction grip bolt
                   Args:
                      2 * T_e - Tension Force in 2 bolts on either sides of the web/plate
                      l_v - distance from the bolt centre line to the toe of the fillet weld or to half
                            the root radius for a rolled section,
                      b_e - effective width of flange per pair of bolts
                      f_o - proof stress in consistent units
                      t - thickness of the end plate
                      f_y - yield strength of end plate
                      end_dist - end distance of bolt
                      pre_tensioned: 'Pretensioned' if bolt is pretension None if it is not
                      beta - 2 for non pre-tensioned bolt and 1 for pre-tensioned bolt
                      Q - Prying force
                      l_e - min(e, 1.1~t~\sqrt{\frac{\beta~f_o}{f_y}})
                      eta - 1.5
                   return:
                       equation for Prying force of friction grip bolt
                   Note:
                       Reference:
                       IS 800:2007,  cl 10.4.7
    """
    T_e = str(T_e)
    l_v = str(l_v)
    f_o = str(f_o)
    b_e = str(b_e)
    t = str(t)
    f_y = str(f_y)
    l_e = str(l_e)
    end_dist = str(end_dist)
    pre_tensioned = str(pre_tensioned)
    beta = str(beta)
    eta = str(eta)
    # le_2 = str(le_2)
    tension_in_bolt_due_to_prying = Math(inline=True)
    tension_in_bolt_due_to_prying.append(NoEscape(
        r'\begin{aligned} Q &= \frac{l_v}{2\times l_e} \Bigg[T_e - \frac{\beta \times  \eta \times f_o \times b_e \times t^4}'
        r'{27 \times l_e \times l_v^2}\Bigg] \\ \\'))

    if pre_tensioned == 'Pretensioned':
        tension_in_bolt_due_to_prying.append(NoEscape(r'\beta &= 1 ~(pre-tensioned~ bolt) \\ '))
    else:
        tension_in_bolt_due_to_prying.append(NoEscape(r'\beta &= 2 ~(non~ pre-tensioned~bolt) \\'))

    tension_in_bolt_due_to_prying.append(NoEscape(r'l_e &= min\Bigg(e, 1.1~t~\sqrt{\frac{\beta~f_o}{f_y}}\Bigg) \\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r' &= min\Bigg(' + end_dist + r', 1.1\times' + t + r'\times\sqrt{\frac{' + beta + r'\times'
                                                  + f_o + r'}{' + f_y + r'}}\Bigg) \\'))

    tension_in_bolt_due_to_prying.append(NoEscape(r' &= min(' + end_dist + ',' + l_e + r') \\')) #todo please add  le2 as a parameter  whoever is using this function

    tension_in_bolt_due_to_prying.append(NoEscape(r' &= ' + l_e + r' \\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r'l_v &= ' + l_v + r' \\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r'b_e &= ' + b_e + r' \\'))
    tension_in_bolt_due_to_prying.append(
        NoEscape(r'Q &=\frac{' + l_v + r'}{2\times' + l_e + r'}\times\\'))
    tension_in_bolt_due_to_prying.append(NoEscape(
        r'&\Bigg[' + T_e + r'- \frac{' + beta + r' \times' + eta + r'\times' + f_o + r'\times' + b_e + r'\times' + t + r'^4}{27 \times' + l_e + r'\times' + l_v + r'^2}\Bigg]\\'))
    if Q <= 0.0:
        tension_in_bolt_due_to_prying.append(NoEscape(r'Q &= 0.0 \\'))
    else:
        Q = str(Q)
        tension_in_bolt_due_to_prying.append(NoEscape(r'Q &= ' + Q + r'\\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r'[Ref.~IS~&800:2007,~Cl.~10.4.7]\end{aligned}'))
    return tension_in_bolt_due_to_prying


def cl_10_4_7_prying_force(l_v, l_e, l_e2, T_e, beta, f_o, b_e, t, end_dist, beam_R1, plate_fy, bolt_fu, bolt_proof_stress, beam_B, bolt_column, Q,
                           eta=1.5, connection = None):
    """Calculate prying force of friction grip bolt
                   Args:
                      2 * T_e - Tension Force in 2 bolts on either sides of the web/plate
                      l_v - distance from the bolt centre line to the toe of the fillet weld or to half
                            the root radius for a rolled section,
                      b_e - effective width of flange per pair of bolts
                      f_o - proof stress in consistent units
                      t - thickness of the end plate
                      f_y - yield strength of end plate
                      end_dist - end distance of bolt
                      pre_tensioned: 'Pretensioned' if bolt is pretension None if it is not
                      beta - 2 for non pre-tensioned bolt and 1 for pre-tensioned bolt
                      Q - Prying force
                      l_e - min(e, 1.1~t~\sqrt{\frac{\beta~f_o}{f_y}})
                      eta - 1.5
                   return:
                       equation for Prying force of friction grip bolt
                   Note:
                       Reference:
                       IS 800:2007,  cl 10.4.7
    """

    tension_in_bolt_due_to_prying = Math(inline=True)
    tension_in_bolt_due_to_prying.append(NoEscape(
        r'\begin{aligned} Q &= \frac{l_v}{2 l_e} \Bigg[T_e - \frac{\beta  \eta  f_o  b_e  t^4}'
        r'{27  l_e  l_v^2}\Bigg] \\ \\'))

    # l_v
    if connection == 'column_end_plate':
        tension_in_bolt_due_to_prying.append(NoEscape(r'l_v &= e~-~ t_w \\'))
        tension_in_bolt_due_to_prying.append(NoEscape(r'&= '+str(end_dist)+r'~-~ 0'+' = ' + str(l_v) + r'~ \text{mm} \\ \\'))

    else:
        tension_in_bolt_due_to_prying.append(NoEscape(r'l_v &= e~-~ \frac{R_1}{2} \\'))
        tension_in_bolt_due_to_prying.append(NoEscape(r'&= ' + str(end_dist) + r'~-~ \frac{' + str(beam_R1) + r'}{2}' + ' = ' + str(l_v) + r'~ \text{mm} \\ \\'))

    # f_o
    tension_in_bolt_due_to_prying.append(NoEscape(r' f_{o} &= 0.7 f_{ub} \\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r' &= 0.7 \times '+ str(bolt_fu) + r' \\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r' &= '+ str(bolt_proof_stress) + r' ~ \text{N/mm}^2 \\ \\'))

    # l_e
    tension_in_bolt_due_to_prying.append(NoEscape(r'l_e &= \min\Bigg(e, 1.1 t \sqrt{\frac{\beta f_o}{f_y}}\Bigg) \\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r' &= \min\Bigg('+str(end_dist)+r', 1.1\times'+str(t)+r'\times\sqrt{\frac{'+str(beta)+r'\times'
                                                  +str(f_o)+r'}{'+str(plate_fy)+r'}}\Bigg) \\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r' &= \min('+str(end_dist)+r',~'+str(l_e2)+r') = '+str(l_e)+r'~ \text{mm} \\ \\'))

    # beta
    if beta == 1:
        tension_in_bolt_due_to_prying.append(NoEscape(r'\beta &= 1 ~ \text{(pre-tensioned bolt)} \\'))
    else:
        tension_in_bolt_due_to_prying.append(NoEscape(r'\beta &= 2 ~ \text{(non pre-tensioned bolt)} \\'))

    # eta
    tension_in_bolt_due_to_prying.append(NoEscape(r'\eta &= 1.5 \\ \\'))

    # be
    tension_in_bolt_due_to_prying.append(NoEscape(r'b_e &= \frac{B}{n_c}\\'))
    tension_in_bolt_due_to_prying.append(NoEscape(r'&= \frac{'+str(beam_B)+'}{'+str(bolt_column)+r'} = '+ str(b_e) + r'~ \text{mm} \\ \\'))

    # Q
    tension_in_bolt_due_to_prying.append(
        NoEscape(r'Q &=\frac{' + str(l_v) + r'}{2\times' + str(l_e) + r'} \times \\'))
    tension_in_bolt_due_to_prying.append(NoEscape(
        r'&\Bigg[' + str(T_e) + r'- \Bigg( \frac{' + str(beta) + r' \times' + str(eta) + r'\times' + str(f_o) + r'\times' + str(b_e) + r'\times'
        + str(t) + r'^4}{27 \times' + str(l_e) + r'\times' + str(l_v) + r'^2} \Bigg) \times 10^{-3} \Bigg]\\'))

    if Q <= 0.0:
        tension_in_bolt_due_to_prying.append(NoEscape(r'Q &= 0.0 \\ \\'))
        tension_in_bolt_due_to_prying.append(NoEscape(r' Note:&~ The~ end~ plate~ is~ sufficiently~ thick~ to \\'))
        tension_in_bolt_due_to_prying.append(NoEscape(r' & prevent~ yielding~of~ the~ plate.~Thus,~ Q~=~0 \\'))
    else:
        tension_in_bolt_due_to_prying.append(NoEscape(r'Q &= ' + str(Q) + r'\\ \\'))

    tension_in_bolt_due_to_prying.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.4.7}] \end{aligned}'))

    return tension_in_bolt_due_to_prying


# TODO: DARSHAN, Keep only one of the following Ans: Use the one with weld thickness reduction
def cl_10_5_2_3_min_fillet_weld_size_required(conn_plates_weld, min_weld_size, red=0.0):
    """
    Calculate minimum size of fillet weld,to avoid the
        risk of cracking in the absence of preheating
    Args:
        conn_plates_weld:Thickness of either plate element being welded in mm (float
        Thickness of other plate element being welded in mm (float)

        red:reduce the thickness of thicker part according to given size range
        min_weld_size:minimum size of the weld
    Returns:
        minimum size of the weld
    Note:
            Reference:
            IS 800, Table 21 (Cl 10.5.2.3) : Minimum Size of First Run or of a Single Run Fillet Weld


    """
    # t1 = str(conn_plates_weld[0])
    # t2 = str(conn_plates_weld[0])
    tmax = min(conn_plates_weld)
    tmin = int(tmax - red)
    tmin = str(tmin)
    tmax = str(int(tmax))
    weld_min = str(min_weld_size)

    min_weld_size_eqn = Math(inline=True)
    min_weld_size_eqn.append(NoEscape(r'\begin{aligned} & t_{w_{\text{min}}}~ \text{based on thinner part} \\'))
    min_weld_size_eqn.append(NoEscape(r'& = \max (' + tmax + ',~ ' + tmin + r') \\ \\'))
    # min_weld_size_eqn.append(NoEscape(r'& IS800:2007~cl.10.5.2.3~Table 21\\ \\'))

    min_weld_size_eqn.append(NoEscape(r'& s_{\text{min}}~ \text{based on thicker part} =' + weld_min + r'\\ \\'))

    min_weld_size_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Table 21, Cl.10.5.2.3}] \end{aligned}'))
    return min_weld_size_eqn


def cl_10_5_2_3_table_21_min_fillet_weld_size_required(conn_plates_thk, min_weld_size):
    """ """

    thicker_plate = max(conn_plates_thk)
    thinner_plate = min(conn_plates_thk)

    min_weld_size_eqn = Math(inline=True)
    min_weld_size_eqn.append(NoEscape(r'\begin{aligned} 1)~~ {t_{w}}_{\min} - & ~ \text{based on thickness of the} \\'))
    min_weld_size_eqn.append(NoEscape(r' & \text{thicker part} \\ \\'))
    min_weld_size_eqn.append(NoEscape(r' t_{\text{thicker}} & =~ \max(' + str(conn_plates_thk[0]) + r',~ ' + str(conn_plates_thk[1]) + r') \\'))
    min_weld_size_eqn.append(NoEscape(r'             & =' + str(thicker_plate) + r' \\'))
    min_weld_size_eqn.append(NoEscape(r' {t_{w}}_{\min} & =' + str(min_weld_size) + r' \\ \\'))

    min_weld_size_eqn.append(NoEscape(r' 2)~~ {t_{w}}_{\min} - & ~ \text{based on thickness of the} \\'))
    min_weld_size_eqn.append(NoEscape(r' & \text{thinner part} \\ \\'))
    min_weld_size_eqn.append(NoEscape(r' t_{\text{thinner}} & =~ \min(' + str(conn_plates_thk[0]) + r',~ ' + str(conn_plates_thk[1]) + r') \\'))
    min_weld_size_eqn.append(NoEscape(r'             & =' + str(thinner_plate) + r' \\'))
    min_weld_size_eqn.append(NoEscape(r' {t_{w}}_{\min} & \leq ~ \min(' + str(min_weld_size) + r',~ ' + str(thinner_plate) + r') \\ \\'))

    min_weld_size_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Table 21, Cl 10.5.2.3}] \end{aligned}'))

    return min_weld_size_eqn


# def cl_10_5_2_3_min_fillet_weld_size_required(conn_plates_weld, min_weld_size):
#     """
#     Calculate minimum size of fillet weld as per Table 21 of IS 800:2007
#     Args:
#
#         conn_plates_weld:Thickness of either plate element being welded in mm (float)
#                              Thickness of other plate element being welded in mm (float)
#
#          min_weld_size: Minimum size of first run or of a single run fillet weld in mm (float)
#
#     Returns:
#           minimum size of fillet weld
#     Note:
#             Reference:
#             IS 800, Table 21 (Cl 10.5.2.3) : Minimum Size of First Run or of a Single Run Fillet Weld
#
#     """
#
#     t1 = str(conn_plates_weld[0])
#     t2 = str(conn_plates_weld[1])
#     tmax = str(max(conn_plates_weld))
#     weld_min = str(min_weld_size)
#
#     min_weld_size_eqn = Math(inline=True)
#     min_weld_size_eqn.append(NoEscape(r'\begin{aligned} &Thickness~of~Thicker~part\\'))
#     min_weld_size_eqn.append(NoEscape(r'\noindent &=max('+t1+','+t2+r')\\'))
#     min_weld_size_eqn.append(NoEscape(r'&='+tmax+r'\\'))
#     min_weld_size_eqn.append(NoEscape(r'&[Ref.IS~800:2007~Cl.10.5.2.3~Table ~21],\\'))
#     min_weld_size_eqn.append(NoEscape(r' &s_{min}=' + weld_min + r'\\'))
#     min_weld_size_eqn.append(NoEscape(r'& [Ref.~IS~800:2007,~Table ~21~ (Cl. 10.5.2.3)]\end{aligned}'))
#
#
#     return min_weld_size_eqn


def cl_10_5_3_1_max_weld_size(conn_plates_weld, max_weld_size):
    """
    Calculate maximum weld size of fillet weld
    Args:

        conn_plates_weld: Thickness of either plate element being welded in mm (float)
                            Thickness of other plate element being welded in mm (float)

         max_weld_size: Maximum weld size of fillet weld
    Returns:
          Maximum weld size of fillet weld
    Note:
            Reference:
            IS 800:2007,  cl 10.5.3.1


    """
    t1 = str(conn_plates_weld[0])
    t2 = str(conn_plates_weld[1])
    t_min = str(min(conn_plates_weld))
    weld_max = str(max_weld_size)

    max_weld_size_eqn = Math(inline=True)
    max_weld_size_eqn.append(NoEscape(r'\begin{aligned} & \text{Thickness of thinner part} \\'))
    max_weld_size_eqn.append(NoEscape(r'&= \text{min} (' + t1 + ',~' + t2 + r')=' + t_min + r'\\'))
    max_weld_size_eqn.append(NoEscape(r'&s_{\text{max}} =' + weld_max + r'\\ \\'))
    max_weld_size_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.3.1}] \end{aligned}'))

    return max_weld_size_eqn


def cl_10_5_3_1_max_weld_size_v2(conn_plates_thk, max_weld_size):
    """
    Calculate maximum weld size of fillet weld
    Args:

        conn_plates_weld: Thickness of either plate element being welded in mm (float)
                            Thickness of other plate element being welded in mm (float)

         max_weld_size: Maximum weld size of fillet weld
    Returns:
          Maximum weld size of fillet weld
    Note:
            Reference:
            IS 800:2007,  cl 10.5.3.1


    """
    thicker_plate = max(conn_plates_thk)
    thinner_plate = min(conn_plates_thk)

    max_weld_size_eqn = Math(inline=True)
    max_weld_size_eqn.append(NoEscape(r'\begin{aligned}  {t_{w}}_{\max} & ~ \text{based on thickness of the} \\'))
    max_weld_size_eqn.append(NoEscape(r' & \text{thinner part} \\ \\'))
    max_weld_size_eqn.append(NoEscape(r' t_{\text{thinner}} & =~ \min(' + str(conn_plates_thk[0]) + r',~ ' + str(conn_plates_thk[1]) + r') \\'))
    max_weld_size_eqn.append(NoEscape(r'             & =' + str(thinner_plate) + r' \\'))
    max_weld_size_eqn.append(NoEscape(r' {t_{w}}_{\max} & = ' + str(max_weld_size) + r' \\ \\'))
    max_weld_size_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.5.3.1}] \end{aligned}'))

    return max_weld_size_eqn


def cl_10_5_3_1_throat_thickness_req():
    """
    Note:
              Reference:
              IS 800:2007,  cl 10.5.3.1
    """
    throat_eqn = Math(inline=True)
    throat_eqn.append(NoEscape(r'\begin{aligned} t_t &\geq 3 \\ \\'))
    throat_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.3.1}] &\end{aligned}'))

    return throat_eqn


def cl_10_5_3_1_throat_thickness_weld(tw, f):
    """
    Calculate effective throat thickness of fillet weld for stress calculation

    Args:
         tw:Fillet weld size in mm (float)
         f:Constant depending upon the angle between  fusion faces  (float)
    Returns:
        Throat thickness in mm (float)
    Note:
              Reference:
              IS 800:2007,  cl 10.5.3.1

    """
    tt = tw * f
    t_t = max(tt, 3)
    tw = str(round(tw, 2))
    f = str(round(f, 2))
    tt = str(round(tt, 2))
    t_t = str(round(t_t, 2))

    throat_eqn = Math(inline=True)
    throat_eqn.append(NoEscape(r'\begin{aligned} t_t & = ' + f + r't_w 'r'\\'))
    throat_eqn.append(NoEscape(r' & = ' + f + r'\times' + tw + r'\\'))
    throat_eqn.append(NoEscape(r' & = ' + t_t + r'\\ \\'))
    throat_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.5.3.1}] \end{aligned}'))
    return throat_eqn


def cl_10_5_7_1_1_weld_strength(conn_plates_weld_fu, gamma_mw, t_t, f_w, type=None):
    """
    Calculate the design strength of fillet weld
    Args:
         conn_plates_weld_fu:Ultimate stresses of weld and parent metal in MPa (list or tuple) in N/mm square(float)
         gamma_mw: 1.25(for shop weld);1.5(site weld)  (float)
         t_t:Throat thickness in mm (float)
         f_w:Design strength of fillet weld in N/mm (float)
    Returns:
        Design strength of fillet weld
    Note:
            Reference:
            IS 800:2007,  cl 10.5.7.1.1

    """

    f_u = str(min(conn_plates_weld_fu))
    t_t = str(t_t)
    gamma_mw = str(gamma_mw)
    f_w = str(f_w)
    weld_strength_eqn = Math(inline=True)
    if type=="end_plate":
        weld_strength_eqn.append(NoEscape(r'\begin{aligned} f_w &=\frac{f_u}{\sqrt{3} \gamma_{mw}}\\'))
        weld_strength_eqn.append(NoEscape(r'&=\frac{' + f_u + r'}{\sqrt{3}\times' + gamma_mw + r'}\\'))
    else:
        weld_strength_eqn.append(NoEscape(r'\begin{aligned} f_w &=\frac{t_t f_u}{\sqrt{3} \gamma_{mw}}\\'))
        weld_strength_eqn.append(NoEscape(r'&=\frac{' + t_t + r'\times' + f_u + r'}{\sqrt{3}\times' + gamma_mw + r'}\\'))
    weld_strength_eqn.append(NoEscape(r'&=' + f_w + r'\\ \\'))
    weld_strength_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.5.7.1.1}] \end{aligned}'))
    return weld_strength_eqn


def cl_10_5_7_3_weld_strength_post_long_joint(h, l, t_t, ws, wsr, direction=None):
    """
    Calculate Reduced flange weld strength  in case of long joint (welded connection)

    Args:

         h: plate height in mm (float)
         l: plate length in mm (float)
         t_t: weld throat thickness  in mm (float)
         ws: weld strength  in KN (float)
         wsr:reduced weld strength  in KN (float)
    Returns:
        reduced weld strength
    Note:
              Reference:
              IS 800:2007,  cl 10.5.7.3

    """
    lj = max(h, l)
    lt = 150 * t_t
    B = 1.2 - ((0.2 * lj) / (150 * t_t))
    if B <= 0.6:
        B = 0.6
    elif B >= 1:
        B = 1
    else:
        B = B
    Bi = str(round(B, 2))
    t_t = str(t_t)
    lt_str = str(lt)
    h = str(h)
    l = str(l)
    ws = str(ws)
    wsr = str(wsr)
    ljs = str(lj)

    long_joint_welded_prov = Math(inline=True)
    # if conn =="web":

    if direction == 'height':
        long_joint_welded_prov.append(NoEscape(r'\begin{aligned} l_w ~&= h\\'))
        long_joint_welded_prov.append(NoEscape(r' &=' + h + r'\\ \\'))
    else:
        long_joint_welded_prov.append(NoEscape(r'\begin{aligned} l ~&= \text{plate length or height} \\'))
        long_joint_welded_prov.append(NoEscape(r' l_l &= \max(' + h + ',' + l + r') \\'))
        long_joint_welded_prov.append(NoEscape(r' &=' + ljs + r' \\ \\'))
    long_joint_welded_prov.append(NoEscape(r'& 150 t_t =150 \times' + t_t + ' = ' + lt_str + r' \\ \\'))

    if lj < lt:
        long_joint_welded_prov.append(NoEscape(r'& \text{since},~l < 150 t_t~\\&then~f_{\text{wrd}} = f_{\text{w}} \\'))
        long_joint_welded_prov.append(NoEscape(r' f_{\text{wrd}} &= ' + ws + r' \\ \\'))
        long_joint_welded_prov.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.7.3.}] \end{aligned}'))
    else:
        long_joint_welded_prov.append(NoEscape(r'& \text{since},~l \geq 150 t_t~ \\&then~V_{\text{rd}} = \beta_{lw} V_{\text{db}} \\'))
        long_joint_welded_prov.append(NoEscape(r'\beta_{l_w}& = 1.2 - (0.2\times' + lj + r')/(150\times' + t_t + r')\\& =' + Bi + r'\\'))
        long_joint_welded_prov.append(NoEscape(r' f_{\text{wrd}}& = ' + Bi + r' \times' + ws + '=' + wsr + r' \\ \\'))
        long_joint_welded_prov.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.7.3.}] \end{aligned}'))

    return long_joint_welded_prov


##################
# TODO: DARSHAN arrange all reduction factors of bolted and welded (I dont think req functions are required.
# TODO Ans: User will not require to see the code and gives better understanding.
# TODO: DARSHAN Refactor functions as per clause no
#################

def cl_10_3_3_1_long_joint_bolted_req():
    """
     Returns:
        Long joint reduction factor
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3.1
    """
    long_joint_bolted_eqn = Math(inline=True)
    long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} & \text{if} ~l_j\geq 15 d~\text{then}~V_{\text{rd}} = \beta_{lj} V_{\text{db}} \\ \\'))

    long_joint_bolted_eqn.append(NoEscape(r'& \text{if}~l_j < 15 d~\text{then}~V_{\text{rd}} = V_{\text{db}} \\ \\'))

    long_joint_bolted_eqn.append(NoEscape(r'& \text{where},\\'))
    long_joint_bolted_eqn.append(NoEscape(r'& l_j = ((nc~\text{or}~nr) - 1) \times (p~\text{or}~g) \\ \\'))

    long_joint_bolted_eqn.append(NoEscape(r'& \beta_{lj} = 1.075 - l/(200 d) \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& \text{but}~0.75\leq\beta_{lj}\leq1.0 \\ \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.3.1}] \end{aligned}'))
    return long_joint_bolted_eqn


#
def cl_10_3_3_1_long_joint_bolted_prov(nc, nr, p, g, d, Tc, Tr, direction=None):
    """
    Calculate reduced bolt capacity in case of long joint

    Args:
         nc:No. of row of bolts in one line (int)
         nr:No. of  bolts in one line (int)
         p:Pitch distance of the plate in mm (float)
         g:Gauge distance of the plate in mm (float)
         d:Diameter of the bolt in mm (float)
         Tc:Bolt capacity  in KN (float)
         Tr: Reduced bolt capacity  in KN (float)
         direction: n_r or None(string)
    Returns:
        Long joint reduction factor
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3.1
              If direction is n_r it will calculate long joint for no. of rows
              else max of rows and column length will be considered

    """
    lc = (nc - 1) * p
    lr = (nr - 1) * g
    l = max(lc, lr)
    lt = 15 * d
    B = 1.075 - (l / (200 * d))
    Bi = round(B, 2)
    nc = str(nc)
    nr = str(nr)
    g = str(g)
    p = str(p)
    d = str(d)
    Tc = str(Tc)
    Tr = str(Tr)
    if B <= 0.75:
        B = 0.75
    elif B >= 1:
        B = 1
    else:
        B = B
    B = str(round(B, 2))
    Bi = str(Bi)
    lc_str = str(lc)
    lr_str = str(lr)
    l_str = str(l)
    lt_str = str(lt)
    long_joint_bolted_eqn = Math(inline=True)
    # long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~l\leq 15 * d~then~V_{\text{rd}} = \beta_{lj} * V_{\text{db}} \\'))
    # long_joint_bolted_eqn.append(NoEscape(r'& where,\\'))

    if direction == 'n_r':
        long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} l_j &= (n_r - 1) \times  p \\'))
        long_joint_bolted_eqn.append(NoEscape(r' &= (' + nr + r' - 1) \times ' + g + '=' + lr_str + r'\\ \\'))
    else:
        long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} l_j &= ((n_c~\text{or}~n_r) - 1) \times  (p~\text{or}~g) \\ '))
        long_joint_bolted_eqn.append(NoEscape(r' &= (' + nc + r' - 1) \times  ' + p + '=' + lc_str + r'\\'))
        long_joint_bolted_eqn.append(NoEscape(r' &= (' + nr + r' - 1) \times  ' + g + '=' + lr_str + r'\\ \\'))

    long_joint_bolted_eqn.append(NoEscape(r' l&= ' + l_str + r'\\'))
    long_joint_bolted_eqn.append(NoEscape(r' 15 \times d &= 15 \times ' + d + ' = ' + lt_str + r' \\ \\'))

    if l < (lt):
        long_joint_bolted_eqn.append(NoEscape(r'& \text{since},~l_j < 15 \times d~\text{then}~\beta_{lj} = 1.0 \\ \\'))
        # long_joint_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = '+Tc+r' \\'))
        long_joint_bolted_eqn.append(NoEscape(r'&[ \text{Ref. IS 800:2007, Cl.10.3.3.1}] \end{aligned}'))
    else:
        long_joint_bolted_eqn.append(NoEscape(r'& \text{since},~l_j \geq 15~d~\text{then}~V_{\text{rd}} = \beta_{lj}~V_{\text{db}} \\'))
        long_joint_bolted_eqn.append(NoEscape(r'& \beta_{lj} = 1.075 - ' + l_str + r'/(200~\times' + d + ') =' + Bi + r'\\ \\'))
        # long_joint_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = '+B+' * '+Tc+'='+Tr+ r' \\'))
        long_joint_bolted_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.3.1}] \end{aligned}'))

    return long_joint_bolted_eqn


def cl_10_3_3_2_large_grip_bolted_req():
    """
     Returns:
        Large grip reduction factor
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3.2
    """
    large_grip_bolted_eqn = Math(inline=True)
    large_grip_bolted_eqn.append(NoEscape(r'\begin{aligned} & \text{if}~l_g\geq 5d,~\text{then}~V_{\text{rd}} = \beta_{lg} V_{\text{db}} \\ \\'))

    large_grip_bolted_eqn.append(NoEscape(r'& \text{if}~l_g < 5d~\text{then}~V_{\text{rd}} = V_{\text{db}} \\ \\'))

    large_grip_bolted_eqn.append(NoEscape(r'& l_g \leq 8d \\'))
    large_grip_bolted_eqn.append(NoEscape(r'& \text{where},\\'))
    large_grip_bolted_eqn.append(NoEscape(r'& l_g = \Sigma (t_{\text{ep}}+t_{\text{member}}) \\ \\'))

    large_grip_bolted_eqn.append(NoEscape(r'& \beta_{lg} = 8d/(3d + l_g) \\'))
    large_grip_bolted_eqn.append(NoEscape(r'& \text{but}~\beta_{lg}\leq \beta_{lj} \\ \\'))

    large_grip_bolted_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.3.2}] \end{aligned}'))
    return large_grip_bolted_eqn


def cl_10_3_3_2_large_grip_bolted_prov(t_sum, d, beta_lj=1.0):
    """
    Calculate reduced bolt capacity in case of large grip

    Args:
         t_sum : Sum of thickness of the connected plates
         d:Diameter of the bolt in mm (float)
    Returns:
        Large grip reduction factor
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3.2

    """
    lg = t_sum
    B = 8 * d / (3 * d + lg)
    Bi = round(B, 2)
    #
    # Tc = str(Tc)
    # Tr = str(Tr)
    if lg <= 5 * d:
        B = 1.0
    # elif B>=beta_lj:
    #     B = beta_lj
    else:
        B = B
    max_lg = 8 * d
    d5_str = str(5 * d)
    d8_str = str(8*d)
    d_str = str(d)
    # B = str(round(B,3))
    Bi = str(Bi)
    lg_str = str(lg)
    t_sum_str = str(t_sum)
    beta_lj_str = str(round(beta_lj, 2))

    large_grip_bolted_eqn = Math(inline=True)
    # large_grip_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~l\leq 15 * d~then~V_{\text{rd}} = \beta_{ij} * V_{\text{db}} \\'))
    # large_grip_bolted_eqn.append(NoEscape(r'& where,\\'))

    large_grip_bolted_eqn.append(NoEscape(r'\begin{aligned} l_g &= \Sigma~ (t_{p}+t_{\text{member}}) \\'))
    # large_grip_bolted_eqn.append(NoEscape(r' &= ' + t_sum_str + r'\\'))
    large_grip_bolted_eqn.append(NoEscape(r' &= ' + t_sum_str + r'\\'))
    large_grip_bolted_eqn.append(NoEscape(r' 5d &= ' + d5_str + r'\\'))
    large_grip_bolted_eqn.append(NoEscape(r' 8d &= ' + d8_str + r'\\'))
    if lg <= 5 * d:
        large_grip_bolted_eqn.append(NoEscape(r'& \text{since},~l_g < 5d~;~\beta_{lg} = 1.0 \\'))
        # large_grip_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = V_{\text{db}} \\'))
        large_grip_bolted_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.3.3.2}] \end{aligned}'))
    elif lg > 8*d:
        large_grip_bolted_eqn.append(NoEscape(r'& \text{since},~l_g > 8d~;~\text{exceeds limit} \\'))
        # large_grip_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = V_{\text{db}} \\'))
        large_grip_bolted_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.3.3.2}] \end{aligned}'))
    else:
        large_grip_bolted_eqn.append(NoEscape(r'& \text{since},~l_g \geq 5d~;~V_{\text{rd}} = \beta_{lg}~V_{\text{db}} \\'))
        large_grip_bolted_eqn.append(NoEscape(r'& \beta_{lg} = 8d/(3d + l_g) \\'))
        large_grip_bolted_eqn.append(NoEscape(r'& \beta_{lg} = 8\times' + d_str + r'/(3\times' + d_str + ' + ' + lg_str + ') =' + Bi + r'\\ \\'))
        if B > beta_lj:
            large_grip_bolted_eqn.append(NoEscape(r'& \text{since},~\beta_{lg} \geq \beta_{lj}~;~\beta_{lg} = \beta_{lj} \\'))
            large_grip_bolted_eqn.append(NoEscape(r'& \beta_{lg} = ' + beta_lj_str + r'\\'))
        # large_grip_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = '+B+' * '+Tc+'='+Tr+ r' \\'))
        large_grip_bolted_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.3.2}] \end{aligned}'))

    return large_grip_bolted_eqn


def packing_plate_bolted_req():
    """
     Returns:
        Packing plate reduction factor
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3.3
    """
    packing_plate_bolted_eqn = Math(inline=True)
    packing_plate_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~t_{pk}\geq 6 mm~then~V_{\text{rd}} = \beta_{pk}V_{\text{db}} \\'))
    packing_plate_bolted_eqn.append(NoEscape(r'& if~t_{pk} < 6 mm~then~V_{\text{rd}} = V_{\text{db}} \\'))
    packing_plate_bolted_eqn.append(NoEscape(r'& where,\\'))
    packing_plate_bolted_eqn.append(NoEscape(r'& t_{pk} = packing~plate~thickness \\'))
    packing_plate_bolted_eqn.append(NoEscape(r'& \beta_{pk} = 1.0 - 0.0125~t_{pk} \\'))
    packing_plate_bolted_eqn.append(NoEscape(r'&[Ref.~IS~800:2007,~Cl.~10.3.3.3]\end{aligned}'))
    return packing_plate_bolted_eqn


def large_grip_length(t_p, t_member, l_g, bolt_dia, beta_lg):
    """ """
    large_grip_length_eqn = Math(inline=True)

    large_grip_length_eqn.append(NoEscape(r'\begin{aligned} l_{g} &= \sum~ \big(t_{p} + t_\text{member} \big) \\'))
    large_grip_length_eqn.append(NoEscape(r'                      &= \sum~ \big(' + str(t_p) + ' + ' + str(t_member) + r' \big) \\'))
    large_grip_length_eqn.append(NoEscape(r'                      &= ' + str(l_g) + r' ~ \text{mm} \\ \\'))

    large_grip_length_eqn.append(NoEscape(r'      5d &= 5 \times ' + str(bolt_dia) + r' = ' + str(round(5 * bolt_dia, 2)) + r' \\ '))
    large_grip_length_eqn.append(NoEscape(r'      8d &= 8 \times ' + str(bolt_dia) + r' = ' + str(round(8 * bolt_dia, 2)) + r' \\ \\'))

    if l_g > (5 * bolt_dia):

        if l_g > (8 * bolt_dia):
            large_grip_length_eqn.append(NoEscape(r' l_{g} &> 8d \\'))
        else:
            large_grip_length_eqn.append(NoEscape(r' \text{Since},& ~5d < ~l_{g} \leq 8d \\'))
            large_grip_length_eqn.append(NoEscape(r' \beta_{lg} &= 8 / (3 + l_{g}/d) \\'))
            large_grip_length_eqn.append(NoEscape(r'  &= \frac{8}{3 + ' + str(l_g) + r'/' + str(bolt_dia) + r'} \\'))
            large_grip_length_eqn.append(NoEscape(r'  &= ' + str(beta_lg) + r' \\ \\'))
    else:
        large_grip_length_eqn.append(NoEscape(r'\text{Since},& ~l_{g} < 5d \\'))
        large_grip_length_eqn.append(NoEscape(r'\beta_{lg} &= 1.0 \\ \\'))

    large_grip_length_eqn.append(NoEscape(r'[Ref.~& IS~800:2007,~Cl.~10.3.3.2] \end{aligned}'))

    return large_grip_length_eqn


def shear_capa_post_large_grip_length_red(beta_lg, shear_capacity):
    """ """
    large_grip_length_eqn = Math(inline=True)

    large_grip_length_eqn.append(NoEscape(r'\begin{aligned} V_{\text{db}} &= V_{\text{db}} \beta_{lg} \\'))
    large_grip_length_eqn.append(NoEscape(r'  &= ' + str(round(shear_capacity / beta_lg, 2)) + r' \times ' + str(beta_lg) + r' \\'))
    large_grip_length_eqn.append(NoEscape(r'  &= ' + str(round(shear_capacity, 2)) + r' \\ \\'))

    large_grip_length_eqn.append(NoEscape(r'[Ref.~& IS~800:2007,~Cl.~10.3.3.2] \end{aligned}'))

    return large_grip_length_eqn


def packing_plate_bolted_prov(gap):
    """
    Calculate reduced bolt capacity in case of large grip

    Args:
         gap: Gap between connector plate and the supporting element
    Returns:
        Packing plate reduction factor
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3.3

    """
    tpk = gap
    B = 1 - 0.0125 * tpk
    Bi = round(B, 3)

    if tpk <= 6:
        B = 1.0
    # elif B>=beta_lj:
    #     B = beta_lj
    else:
        B = B
    tpk_str = str(tpk)
    # B = str(round(B,3))
    Bi = str(Bi)
    packing_plate_bolted_eqn = Math(inline=True)
    # packing_plate_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~l\leq 15 * d~then~V_{\text{rd}} = \beta_{ij} * V_{\text{db}} \\'))
    # packing_plate_bolted_eqn.append(NoEscape(r'& where,\\'))

    packing_plate_bolted_eqn.append(NoEscape(r'\begin{aligned} t_{pk}&= \text{gap} \\'))
    packing_plate_bolted_eqn.append(NoEscape(r' &= ' + tpk_str + r' \text{mm} \\ \\'))
    if tpk <= 6:
        packing_plate_bolted_eqn.append(NoEscape(r'& \text{since},~t_{pk} ~\leq~ 6 \text{mm}, ~\text{then}~V_{\text{rd}} = V_{\text{db}}\\ \\'))
        # packing_plate_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = '+Tc+r' \\'))
        packing_plate_bolted_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.3.3.3}] \end{aligned}'))
    else:
        packing_plate_bolted_eqn.append(NoEscape(r'& \text{since},~t_{pk} \geq 6 \text{mm},~\text{then}~V_{\text{rd}} = \beta_{pk}~V_{\text{db}} \\'))
        packing_plate_bolted_eqn.append(NoEscape(r'& \beta_{pk} = 1.0 - 0.0125 \times ' + tpk_str + ' =' + Bi + r'\\ \\'))

        # packing_plate_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = '+B+' \times '+Tc+'='+Tr+ r' \\'))
        packing_plate_bolted_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.3.3}] \end{aligned}'))

    return packing_plate_bolted_eqn


def bolt_capacity_reduced_req():
    """
     Returns:
        Bolt capacity post reduction factors
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3
    """
    bolt_capacity_reduced_eqn = Math(inline=True)
    bolt_capacity_reduced_eqn.append(NoEscape(r'\begin{aligned} V_{\text{rd}} &= \beta_{lj}~\beta_{lg}~\beta_{pk}~V_{\text{db}} \\'))

    return bolt_capacity_reduced_eqn


def bolt_capacity_reduced_prov(beta_lj, beta_lg, beta_pk, Vdb):
    """
    Calculate reduced bolt capacity

    Args:
         beta_lj : Long joint reduction factor
         beta_lg : Large grip reduction factor
         beta_pk : Packing plate reduction factor
         V_{\text{db}} : Original Bolt Capacity
    Returns:
        Reduced bolt capacity
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3

    """
    Blj = beta_lj
    Blg = beta_lg
    Bpk = beta_pk
    Vred = Blj * Blg * Bpk * Vdb
    Vdb = round(Vdb, 2)
    Vred = round(Vred, 2)
    Blj_str = str(round(Blj, 3))
    Blg_str = str(round(Blg, 3))
    Bpk_str = str(round(Bpk, 3))
    Vdb_str = str(round(Vdb, 2))
    Vred_str = str(Vred)

    bolt_capacity_reduced_eqn = Math(inline=True)
    # packing_plate_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~l\leq 15 * d~then~V_{\text{rd}} = \beta_{ij} * V_{\text{db}} \\'))
    # packing_plate_bolted_eqn.append(NoEscape(r'& where,\\'))
    bolt_capacity_reduced_eqn.append(
        NoEscape(r'\begin{aligned} V_{\text{rd}} &= \beta_{lj}~\beta_{lg} \beta_{pk} V_{\text{db}} \\'))
    bolt_capacity_reduced_eqn.append(
        NoEscape(r' &= ' + Blj_str + r' \times ' + Blg_str + r' \times ' + Bpk_str + r' \times ' + Vdb_str + r'\\'))

    bolt_capacity_reduced_eqn.append(NoEscape(r' &= ' + Vred_str + r'\\ \\'))

    bolt_capacity_reduced_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.3.3}] \end{aligned}'))

    return bolt_capacity_reduced_eqn


def long_joint_bolted_beam(nc, nr, p, g, d, Tc, Tr, joint, end_dist, gap, edge_dist, web_thickness, root_radius, conn=None):
    """
    Calculate reduced bolt capacity in case of long joint

    Args:

        nc:No. of row of bolts in one line (int)
        nr:No. of  bolts in one line (int)
        p:Pitch distance of the plate in mm (float)
        g:Gauge distance of the plate in mm (float)
        d:Diameter of the bolt in mm (float)
        Tc:Bolt capacity  in KN (float)
        Tr: Reduced bolt capacity  in KN (float)
        joint:Flange or web (str)
        end_dist: flange plate end distance in mm (float)
        gap:gap between flange plate in mm (float)
        edge_dist: flane plate edge distance in mm (float)
        web_thickness: web thickness in mm (float)
        root_radius: root radius of the section in mm (float)
    Returns:
        reduced bolt capacity in case of long joint
    Note:
              Reference:
              IS 800:2007,  cl 10.3.3.1

    """

    if joint == 'web':
        lc = round(2 * ((nc / 2 - 1) * p + end_dist) + gap, 2)
        lr = round((nr - 1) * g, 2)
    else:
        lc = round(2 * ((nc / 2 - 1) * p + end_dist) + gap, 2)
        lr = round(2 * ((nr / 2 - 1) * g + edge_dist + root_radius) + web_thickness, 2)

    l = round(max(lc, lr), 2)

    lt = 15 * d
    B = 1.075 - (l / (200 * d))
    # Bi = round(B,2)
    nc = str(nc)
    nr = str(nr)
    g = str(g)
    p = str(p)
    d = str(d)
    Tc = str(Tc)
    Tr = str(Tr)
    if B <= 0.75:
        B = 0.75
    elif B >= 1:
        B = 1
    else:
        B = B
    B = round(B, 2)
    Bi = str(B)
    lc_str = str(lc)
    lr_str = str(lr)
    l_str = str(l)
    lt_str = str(lt)
    end_dist = str(end_dist)

    edge_dist = str(edge_dist)
    web_thickness = str(web_thickness)
    gap = str(gap)
    root_radius = str(root_radius)
    long_joint_bolted_eqn = Math(inline=True)
    # long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~l\leq 15 * d~then~V_{\text{rd}} = \beta_{lj} * V_{\text{db}} \\'))
    # long_joint_bolted_eqn.append(NoEscape(r'& where,\\'))
    if l < (lt):

        if joint == 'web':
            long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} l&= ((n_c~ \text{or} ~n_r) - 1) \times (p~ \text{or} ~g) \\ \\'))
            if conn == "beam_beam":
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_r &= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(r' l_c &= (' + nr + r' - 1) \times ' + g + '=' + lr_str + r'\\ \\'))
            elif conn == "col_col":
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_c &= 2 \times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(r' l_r &= (' + nr + r' - 1) \times ' + g + '=' + lr_str + r'\\ \\'))
            else:
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_c &= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(r' l_r &= (' + nr + r' - 1) \times ' + g + '=' + lr_str + r'\\ \\'))

            long_joint_bolted_eqn.append(NoEscape(r' l &= ' + l_str + r'\\ '))
            long_joint_bolted_eqn.append(NoEscape(r'& 15d = 15 \times ' + d + ' = ' + lt_str + r' \\ \\'))
            long_joint_bolted_eqn.append(NoEscape(r'& \text{since},~l < 15d~\\& \text{then}, ~V_{\text{rd}} = V_{\text{db}} \\'))
            long_joint_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = ' + Tc + r' \\ \\'))
            long_joint_bolted_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.3.1}] \end{aligned}'))
        else:
            long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} l~&= ((n_c~\text{or}~n_r) - 1) \times (p~\text{or}~g) \\ \\'))
            if conn == "beam_beam":
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_r&= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(
                    r' l_c &= 2\times \Bigg( \Big(\frac{' + nr + r'}{2} - 1 \Big) \times ' + g + '+' + edge_dist + r' \Bigg) \\& +' + root_radius + ')+ ' + web_thickness + '=' + lr_str + r'\\ \\'))
            elif conn == "col_col":
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_c &= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(
                    r' l_r &= 2\times \Bigg( \Big(\frac{' + nr + r'}{2} - 1 \Big) \times ' + g + '+' + edge_dist + r' \Bigg) \\& +' + root_radius + ')+ ' + web_thickness + '=' + lr_str + r'\\ \\'))
            else:
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_c &= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(
                    r' l_r&= 2\times \Bigg( \Big(\frac{' + nr + r'}{2} - 1 \Big) \times ' + g + '+' + edge_dist + r' \Bigg) \\& +' + root_radius + ')+ ' + web_thickness + '=' + lr_str + r'\\ \\'))

            long_joint_bolted_eqn.append(NoEscape(r' l~&= ' + l_str + r'\\'))
            long_joint_bolted_eqn.append(NoEscape(r'& 15d = 15 \times ' + d + ' = ' + lt_str + r' \\ \\'))
            long_joint_bolted_eqn.append(NoEscape(r'& \text{since},~l < 15d~ \\& \text{then} ~V_{\text{rd}} = V_{\text{db}} \\'))
            long_joint_bolted_eqn.append(NoEscape(r'& V_{\text{rd}} = ' + Tc + r' \\ \\'))
            long_joint_bolted_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl. 10.3.3.1}] \end{aligned}'))
    else:
        if joint == 'web':
            long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} l&= ((n_c~\text{or}~n_r) - 1) \times (p~\text{or}~g) \\ \\'))
            if conn == "beam_beam":
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_r&= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(r' l_c &= (' + nr + r' - 1) \times' + g + '=' + lr_str + r'\\ \\'))
            elif conn == "col_col":
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_c &= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(r' l_r &= (' + nr + r' - 1) \times ' + g + '=' + lr_str + r'\\ \\'))
            else:
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_c &= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(r' l_r &= (' + nr + r' - 1) \times ' + g + '=' + lr_str + r'\\ \\'))

            long_joint_bolted_eqn.append(NoEscape(r' l&= ' + l_str + r'\\'))
            long_joint_bolted_eqn.append(NoEscape(r'& 15d = 15 \times' + d + ' = ' + lt_str + r' \\ \\'))
            long_joint_bolted_eqn.append(NoEscape(r'&\text{since},~l \geq 15d~ \\&\text{then}~V_{\text{rd}} = \beta_{lj} \times V_{\text{db}} \\'))
            long_joint_bolted_eqn.append(NoEscape(r'\beta_{lj} &= 1.075 - ' + l_str + r'/(200 \times' + d + r') \\&=' + Bi + r'\\'))
            long_joint_bolted_eqn.append(NoEscape(r'V_{\text{rd}} &= ' + Bi + r' \times' + Tc + '=' + Tr + r' \\ \\'))
            long_joint_bolted_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.3.3.1}] &\end{aligned}'))
        else:
            long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} l~&= ((n_c~\text{or}~n_r) - 1) \times (p~\text{or}~g) \\ \\'))
            if conn == "beam_beam":
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_r&= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(
                    r' l_c&= 2\times \Bigg( \Big(\frac{' + nr + r'}{2} - 1 \Big) \times ' + g + '+' + edge_dist + r' \Bigg) \\& +' + root_radius + ')+ ' + web_thickness + '=' + lr_str + r'\\ \\'))
            elif conn == "col_col":
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_c&= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(
                    r' l_r&= 2\times \Bigg( \Big(\frac{' + nr + r'}{2} - 1 \Big) \times ' + g + '+' + edge_dist + r' \Bigg) \\& +' + root_radius + ')+ ' + web_thickness + '=' + lr_str + r'\\ \\'))
            else:
                long_joint_bolted_eqn.append(
                    NoEscape(r' l_c &= 2\times \Bigg( \Big(\frac{' + nc + r'}{2} - 1 \Big) \times ' + p + '+' + end_dist + ' \Bigg)+ ' + gap + r'\\&=' + lc_str + r'\\ \\'))
                long_joint_bolted_eqn.append(NoEscape(
                    r' l_r &= 2\times \Bigg( \Big(\frac{' + nr + r'}{2} - 1 \Big) \times ' + g + '+' + edge_dist + r' \Bigg) \\& +' + root_radius + ')+ ' + web_thickness + '=' + lr_str + r'\\ \\'))

            long_joint_bolted_eqn.append(NoEscape(r' l~&= ' + l_str + r'\\'))
            long_joint_bolted_eqn.append(NoEscape(r'&15d = 15 \times' + d + ' = ' + lt_str + r' \\ \\'))
            long_joint_bolted_eqn.append(NoEscape(r'&\text{since},~l \geq 15d~\\ &\text{then}~V_{\text{rd}} = \beta_{lj} \times V_{\text{db}} \\'))
            long_joint_bolted_eqn.append(NoEscape(r'\beta_{lj} &= 1.075 - ' + l_str + r'/(200\times' + d + r')\\& =' + Bi + r'\\'))
            long_joint_bolted_eqn.append(NoEscape(r' V_{\text{rd}}& = ' + Bi + r' \times ' + Tc + '=' + Tr + r' \\ \\'))
            long_joint_bolted_eqn.append(NoEscape(r' & [ \text{Ref. IS 800:2007, Cl.10.3.3.1}] &\end{aligned}'))
    return long_joint_bolted_eqn


def long_joint_welded_req():
    long_joint_bolted_eqn = Math(inline=True)
    long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} &\text{if}~l\geq 150 t_t,~\text{then}~V_{\text{rd}} = \beta_{l_w} V_{\text{db}} \\ \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& \text{if}~l < 150 t_t,~then~V_{\text{rd}} = V_{\text{db}} \\ \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& \text{where},\\'))
    long_joint_bolted_eqn.append(NoEscape(r'&  l ~= \text{plate length or height} \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& \beta_{l_w} = 1.2 - \frac{(0.2 l )}{(150 t_t)}  \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& \text{but},~0.6\leq\beta_{l_w}\leq1.0 \\ \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.7.3}] \end{aligned}'))
    return long_joint_bolted_eqn


def long_joint_welded_beam_prov(plate_height, l_w, t_w, gap, t_t, Tc, Tr):
    """
    Calculate Reduced flange weld strength  in case of long joint

    Args:
         plate_height:flange plate height in mm (float)
         l_w:available long flane length in mm (float)
         t_w:flange weld size in mm (float)
         gap:flange plate gap  in mm (float)
         t_t:flange weld throat thickness in mm (float)
         Tc:flange weld strength in KN (float)
         Tr:reduced flange weld strength in KN/mm (float)
    Returns:
        reduced flange weld strength in KN/mm (float)
    Note:
              Reference:
              IS 800:2007,  cl 10.5.7.3

    """
    ll = round(2 * (l_w + (2 * t_w)) + gap, 2)
    lh = plate_height
    l = round(max(ll, lh), 2)
    lt = 150 * t_t
    B = 1.2 - ((0.2 * l) / (150 * t_t))
    if B <= 0.6:
        B = 0.6
    elif B >= 1:
        B = 1
    else:
        B = B
    Bi = str(round(B, 2))
    t_t = str(t_t)
    # l =str(l)
    l_str = str(l)
    # lt = str(lt)
    lt_str = str(lt)

    # B = str(round(B, 2))
    # Bi = str(Bi)
    t_t = str(t_t)
    ll_str = str(ll)
    lh_str = str(lh)
    plate_height = str(plate_height)
    Tc = str(Tc)
    Tr = str(Tr)
    l_w = str(l_w)

    t_w = str(t_w)
    l_w = str(l_w)
    gap = str(gap)
    long_joint_welded_beam_prov = Math(inline=True)
    # if conn =="web":
    if l < lt:
        long_joint_welded_beam_prov.append(NoEscape(r'\begin{aligned} l ~&= \text{plate length or height} \\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r' l_l &= 2(' + l_w + r'+(2\times' + t_w + '))+' + gap + r' \\'))
        long_joint_welded_beam_prov.append(NoEscape(r' &=' + ll_str + r' \\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r'l_h& =' + lh_str + r' \\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r' l~&= ' + l_str + r'\\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r'& 150 \times t_t =150 \times' + t_t + ' = ' + lt_str + r' \\'))
        long_joint_welded_beam_prov.append(NoEscape(r'& \text{since},~l < 150 \times t_t~\\&\text{then}~V_{\text{rd}} = V_{\text{db}} \\'))
        long_joint_welded_beam_prov.append(NoEscape(r' V_{\text{rd}} &= ' + Tc + r' \\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.5.7.3}] &\end{aligned}'))
    else:
        long_joint_welded_beam_prov.append(NoEscape(r'\begin{aligned} l~&= \text{plate length or height} \\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r' l_l &= 2(' + l_w + r'+(2\times' + t_w + '))+' + gap + r' \\'))
        long_joint_welded_beam_prov.append(NoEscape(r' &=' + ll_str + r' \\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r' l_h& =' + lh_str + r' \\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r' l~&= ' + l_str + r'\\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r'& 150 \times t_t =150 \times' + t_t + ' = ' + lt_str + r' \\'))
        long_joint_welded_beam_prov.append(NoEscape(r'& \text{since},~l \geq 150 \times t_t~ \\& \text{then} ~V_{\text{rd}} = \beta_{lw} \times V_{\text{db}} \\'))
        long_joint_welded_beam_prov.append(NoEscape(r'\beta_{l_w}& = 1.2 - (0.2\times' + l_str + r')/(150\times' + t_t + r')\\& =' + Bi + r'\\'))
        long_joint_welded_beam_prov.append(NoEscape(r' V_{\text{rd}}& = ' + Bi + r' \times' + Tc + '=' + Tr + r' \\ \\'))

        long_joint_welded_beam_prov.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.7.3}] \end{aligned}'))

    return long_joint_welded_beam_prov


def bolt_red_capacity_prov(blj, blg, V, Vrd, type):
    blj = str(round(blj,2))
    blg = str(round(blg,2))
    V = str(V)
    Vrd = str(Vrd)
    bolt_capacity_eqn = Math(inline=True)
    if type == "b":
        bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{\text{rd}} &= \beta_{lj} \beta_{lg} V_{\text{db}} \\'))
        bolt_capacity_eqn.append(NoEscape(r' &= ' + blj + r'\times' + blg + r'\times' + V + r'\\'))
        bolt_capacity_eqn.append(NoEscape(r'& = ' + Vrd + r'\end{aligned}'))
    else:
        bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{\text{rd}} &= \beta_{lj} V_{\text{db}} \\'))
        bolt_capacity_eqn.append(NoEscape(r' &= ' + blj + r'\times' + V + r'\\'))
        bolt_capacity_eqn.append(NoEscape(r'& = ' + Vrd + r'\end{aligned}'))

    return bolt_capacity_eqn


########################################
# End of IS Code functions
##########################################
# Minimum loads functions
##########################################


def ir_sum_bb_cc(Al, M, A_c, M_c, IR_axial, IR_moment, sum_IR):
    """

    :param Al:
    :param M:
    :param A_c:
    :param M_c:
    :param IR_axial:
    :param IR_moment:
    :param sum_IR:
    :return:
    """
    IR_axial = str(IR_axial)
    IR_moment = str(IR_moment)
    Al = str(Al)
    M = str(M)
    A_c = str(A_c)
    M_c = str(M_c)
    sum_IR = str(sum_IR)
    ir_sum_bb_cc_eqn = Math(inline=True)
    ir_sum_bb_cc_eqn.append(NoEscape(r'\begin{aligned} \text{ I.R. axial} ~~~~&= P_{\text{x}} / T_{\text{dg}} \\'))
    ir_sum_bb_cc_eqn.append(NoEscape(r'& =' + Al + '/' + A_c + r' \\'))
    ir_sum_bb_cc_eqn.append(NoEscape(r'& =' + IR_axial + r' \\ \\'))

    ir_sum_bb_cc_eqn.append(NoEscape(r' \text{I.R. moment} &= M_{\text{z}} / {M_{d}}_{\text{z}} \\'))
    ir_sum_bb_cc_eqn.append(NoEscape(r'& =' + M + '/' + M_c + r' \\'))
    ir_sum_bb_cc_eqn.append(NoEscape(r'& =' + IR_moment + r' \\ \\'))

    ir_sum_bb_cc_eqn.append(NoEscape(r' \text{I.R. sum} ~~~~~ &= \text{I.R. axial + I.R. moment}  \\'))
    ir_sum_bb_cc_eqn.append(NoEscape(r'&= ' + IR_axial + '+ ' + IR_moment + r' \\'))
    ir_sum_bb_cc_eqn.append(NoEscape(r'& =' + sum_IR + r'\end{aligned}'))
    return ir_sum_bb_cc_eqn


def IR_base_plate(P, P_c, M, M_d, IR_axial, IR_moment, sum_IR):

    IR_base_plate_eqn = Math(inline=True)
    IR_base_plate_eqn.append(NoEscape(r'\begin{aligned} \text{I.R. axial} ~~~~ &= P_{\text{x}} / P_{\text{d}} \\'))
    IR_base_plate_eqn.append(NoEscape(r'& =' + str(P) + '/' + str(P_c) + r' \\'))
    IR_base_plate_eqn.append(NoEscape(r'& =' + str(IR_axial) + r' \\ \\'))

    IR_base_plate_eqn.append(NoEscape(r'\text{I.R. moment} ~~~~ &= M_{\text{z}} / {M_{d}}_{\text{z}} \\'))
    IR_base_plate_eqn.append(NoEscape(r'& =' + str(M) + '/' + str(M_d) + r' \\'))
    IR_base_plate_eqn.append(NoEscape(r'& =' + str(IR_moment) + r' \\ \\'))

    IR_base_plate_eqn.append(NoEscape(r'\text{I.R. sum } &= \text{I.R. axial + I.R. moment}  \\'))
    IR_base_plate_eqn.append(NoEscape(r'&= ' + str(IR_axial) + ' + ' + str(IR_moment) + r' \\'))
    IR_base_plate_eqn.append(NoEscape(r'& =' + str(sum_IR) + r' \end{aligned}'))

    return IR_base_plate_eqn


def min_loads_required(conn):
    """

    :param conn:
    :return:
    """
    min_loads_required_eqn = Math(inline=True)
    min_loads_required_eqn.append(NoEscape(r'\begin{aligned}  & \text{if I.R. axial} < 0.3 ~ \text{and I.R. moment} < 0.5 \\'))
    min_loads_required_eqn.append(NoEscape(r' &~~~{P_{\text{x}}}_{\text{min}} = 0.3 T_{\text{dg}}\\'))
    min_loads_required_eqn.append(NoEscape(r' &~~~{M_{\text{z}}}_{\text{min}}= 0.5 {M_{d}}_{\text{z}}\\ \\'))

    if conn == "beam_beam":
        min_loads_required_eqn.append(NoEscape(r' & \text{elif sum I.R.} <= 1.0 ~ \text{and I.R. moment} < 0.5\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~\text{if}~~ (0.5 - \text{I.R. moment}) < (1 - \text{sum I.R.})\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~~~~{M_{\text{z}}}_{\text{min}} = 0.5 \times {M_{d}}_{\text{z}}\\'))
        min_loads_required_eqn.append(NoEscape(r'& ~~~\text{else}\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~~~~{M_{\text{z}}}_{\text{min}} = M_{\text{z}} + ((1 - \text{sum I.R.}) \times {M_{d}}_{\text{z}})\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~{P_{\text{x}}}_{\text{min}} = P_{\text{x}} \\ \\'))

        min_loads_required_eqn.append(NoEscape(r'&\text{elif}~~ \text{sum I.R.} <= 1.0~ \text{and I.R. axial} < 0.3\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~\text{if}~~ (0.3 - \text{I.R. axial}) < (1 -  \text{sum I.R.})\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~~~~{P_{\text{x}}}_{\text{min}} = 0.3 T_{\text{dg}} \\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~\text{else}~~\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~~~~{P_{\text{x}}}_{\text{min}} = P_{\text{x}} + ((1 - \text{sum I.R.}) \times T_{\text{dg}})\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~{M_{\text{z}}}_{\text{min}} = M_{\text{z}} \\ \\'))
    else:
        min_loads_required_eqn.append(NoEscape(r'&\text{elif}~~ \text{sum I.R.} <= 1.0~ and~ \text{I.R. axial} < 0.3\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~\text{if}~~ (0.3 - \text{I.R. axial}) < (1 - \text{sum I.R.})\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~~~~Ac_{\text{min}} = 0.3 A_c\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~\text{else}~~\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~~~~Ac_{\text{min}} = \text{AL} + ((1 - \text{sum I.R.}) \times A_c)\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~{M_{u}}_{\text{min}} = M \\ \\'))

        min_loads_required_eqn.append(NoEscape(r' &\text{elif}~~ \text{sum I.R.} <= 1.0 ~ \text{and I.R. moment} < 0.5\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~ \text{if} ~~ (0.5 - \text{I.R. moment}) < (1 - \text{sum I.R.})\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~~~~{M_{u}}_{\text{min}} = 0.5 {M_{d}}_{\text{z}}\\'))
        min_loads_required_eqn.append(NoEscape(r'& ~~~\text{else}\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~~~~{M_{u}}_{\text{min}} = M + ((1 - \text{sum I.R.}) \times {M_{d}}_{\text{z}})\\'))
        min_loads_required_eqn.append(NoEscape(r'&~~~Ac_{\text{min}} = \text{AL} \\ \\'))

    min_loads_required_eqn.append(NoEscape(r'&\text{else}~~\\'))
    min_loads_required_eqn.append(NoEscape(r'&~~~{P_{\text{x}}}_{\text{min}} = P_{\text{x}} \\'))
    min_loads_required_eqn.append(NoEscape(r'&~~~{M_{\text{z}}}_{\text{min}} = M_{\text{z}} \\ \\'))

    min_loads_required_eqn.append(NoEscape(r'& \text{Note: AL is the user input for load} \end{aligned}'))
    return min_loads_required_eqn


def min_loads_provided(min_ac, min_mc, conn):
    """

    :param min_ac:
    :param min_mc:
    :param conn:
    :return: minimum moment (kNm) and axial(kN)
     Note:
            Reference:
            IS 800:2007,  cl 10.7
    """
    min_ac = str(min_ac)
    min_mc = str(min_mc)

    if conn == "beam_beam":
        min_loads_provided_eqn = Math(inline=True)
        min_loads_provided_eqn.append(NoEscape(r'\begin{aligned} & {M_{\text{z}}}_{\text{min}} =' + min_mc + r'\\'))
        min_loads_provided_eqn.append(NoEscape(r'& {P_{\text{x}}}_{\text{min}} =' + min_ac + r'\\ \\'))
        min_loads_provided_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.7}] \end{aligned}'))
    else:
        min_loads_provided_eqn = Math(inline=True)
        min_loads_provided_eqn.append(NoEscape(r'\begin{aligned} & Ac_{\text{min}} =' + min_ac + r'\\'))
        min_loads_provided_eqn.append(NoEscape(r'& {M_{u}}_{\text{min}} =' + min_mc + r'\\ \\'))
        min_loads_provided_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.7}] \end{aligned}'))
    return min_loads_provided_eqn


def axial_capacity_req(axial_capacity, min_ac):
    """
    Calculate minimum  required axial capacity of member
    Args:
         axial_capacity:Axial capacity of member in KN
         min_ac: Minimum axial capacity of member in KN
    Returns:
         Minimum axial capacity of member in KN

    Note:
              Reference:
              IS 800:2007,  cl 10.7

    """

    min_ac = str(min_ac)
    axial_capacity = str(axial_capacity)
    ac_req_eqn = Math(inline=True)
    ac_req_eqn.append(NoEscape(r'\begin{aligned} {A_{\text{c}}}_{\text{min}} &= 0.3A_c\\'))
    ac_req_eqn.append(NoEscape(r'&= 0.3 \times' + axial_capacity + r'\\'))
    ac_req_eqn.append(NoEscape(r'&=' + min_ac + r'\\ \\'))

    ac_req_eqn.append(NoEscape(r'{A_{\text{c}}}_{\text{max}} &=' + axial_capacity + r'\\ \\'))

    ac_req_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.7}] \end{aligned}'))

    return ac_req_eqn


def prov_axial_load(axial_input, min_ac, app_axial_load, axial_capacity):
    """
    Calculate load axial force for column end plate
    Args:
         axial_input:Axial load in KN (float)
         min_ac:Minimum axial load in KN (float)
         app_axial_load:Factored axial load in KN (float)
    Returns:
        Factored axial load
    Note:
              Reference:
              IS 800:2007,  cl 10.7

    """
    min_ac = str(min_ac)
    axial_input = str(axial_input)
    app_axial_load = str(app_axial_load)

    prov_axial_load_eqn = Math(inline=True)
    prov_axial_load_eqn.append(NoEscape(r'\begin{aligned} P_{u} ~~ &= \text{max}(P_{\text{x}},~ {P_{\text{x}}}_{\text{min}})\\'))
    prov_axial_load_eqn.append(NoEscape(r'&= \text{max}( ' + axial_input + ',' + min_ac + r')\\'))
    prov_axial_load_eqn.append(NoEscape(r'&=' + app_axial_load + r'\end{aligned}'))

    return prov_axial_load_eqn


def prov_shear_load(shear_input, min_sc, app_shear_load, shear_capacity_1):
    """
    Calculate maximum shear force
    Args:

        shear_input factored input shear force
        min_sc:Minimum shear force
        app_shear_load:Maximum of factored input shear force and minimum shear force
    Returns:
        maximum shear force
    Note:
              Reference:
              IS 800:2007,  cl 10.7


    """
    min_sc = str(min_sc)
    shear_input = str(shear_input)
    app_shear_load = str(app_shear_load)
    shear_capacity_1 = str(shear_capacity_1)
    app_shear_load_eqn = Math(inline=True)
    app_shear_load_eqn.append(NoEscape(r'\begin{aligned} {V_{y}}_{\text{min}} &=  \min(0.15 V_{d_y},~ 40.0)\\'))
    app_shear_load_eqn.append(NoEscape(r'& =  \min(0.15 \times' + shear_capacity_1 + r',~ 40.0)\\'))
    app_shear_load_eqn.append(NoEscape(r'&=' + min_sc + r'\\ \\'))

    app_shear_load_eqn.append(NoEscape(r' V_u~~ &= \max(V_{y},~ {V_{y}}_{\text{min}})\\'))
    app_shear_load_eqn.append(NoEscape(r'&=  \max(' + shear_input + ',' + min_sc + r')\\'))
    app_shear_load_eqn.append(NoEscape(r'&=' + app_shear_load + r'\\ \\'))

    app_shear_load_eqn.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.7}] \end{aligned}'))

    return app_shear_load_eqn


def prov_shear_force(shear_input, min_sc, app_shear_load, shear_capacity_1):
    """
    Calculate maximum shear force
    Args:

        shear_input factored input shear force
        min_sc:Minimum shear force
        app_shear_load:Maximum of factored input shear force and minimum shear force
    Returns:
        maximum shear force
    Note:
              Reference:
              IS 800:2007,  cl 10.7


    """
    min_sc_1 = str(round(0.15 * shear_capacity_1, 2))
    min_sc = str(min_sc)
    shear_input = str(shear_input)
    app_shear_load = str(app_shear_load)
    shear_capacity_1 = str(shear_capacity_1)

    app_shear_load_eqn = Math(inline=True)
    app_shear_load_eqn.append(NoEscape(r'\begin{aligned} {V_{y}}_{\min} &=  \min(0.15 V_{d_y}, ~40.0) \\'))
    app_shear_load_eqn.append(NoEscape(r'& =  \min(0.15 \times' + shear_capacity_1 + r',~ 40.0) \\'))
    app_shear_load_eqn.append(NoEscape(r'& =  \min(' + min_sc_1 + r',~ 40.0) \\'))
    app_shear_load_eqn.append(NoEscape(r'&=' + min_sc + r' \\ \\'))

    app_shear_load_eqn.append(NoEscape(r' V_{u} &= \max(V_{y},~{V_{y}}_{\min}) \\'))
    app_shear_load_eqn.append(NoEscape(r' \text{but},~ & \leq V_{dy} \\'))
    app_shear_load_eqn.append(NoEscape(r'&=  \max(' + shear_input + ',~' + min_sc + r') \\'))
    app_shear_load_eqn.append(NoEscape(r' \text{but},~ & \leq ' + shear_capacity_1 + r' \\ \\'))

    app_shear_load_eqn.append(NoEscape(r'&=' + app_shear_load + r' \\ \\'))

    app_shear_load_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.7}] \end{aligned}'))

    return app_shear_load_eqn


def allow_shear_capacity(V_d, S_c):
    V_d = str(V_d)
    S_c = str(S_c)
    allow_shear_capacity_eqn = Math(inline=True)
    allow_shear_capacity_eqn.append(NoEscape(r'\begin{aligned} V_{d} &= 0.6~V_{dy}\\'))
    allow_shear_capacity_eqn.append(NoEscape(r'&=0.6 \times' + V_d + r'\\'))
    allow_shear_capacity_eqn.append(NoEscape(r'&=' + S_c + r'\\ \\'))
    allow_shear_capacity_eqn.append(NoEscape(r'& [\text{Limited to low shear}] \end{aligned}'))
    return allow_shear_capacity_eqn


def prov_moment_load(moment_input, min_mc, app_moment_load, moment_capacity, moment_capacity_supporting, type=None):
    """
    Calculate max moment load of input moment and min moment of the section
    Args:

         moment_input:Factored input moment in KN (float)
         min_mc:Min moment of the section in KN (float)
         app_moment_load:Factored moment max of input moment and min moment of the section in KN (float)
    Returns:
         max moment load of input moment and min moment of the section
    Note:
              Reference:
              IS 800:2007,  cl 8.2.1.2

    """

    min_mc = str(min_mc)
    moment_input = str(moment_input)
    app_moment_load = str(app_moment_load)
    moment_capacity = str(moment_capacity)

    app_moment_load_eqn = Math(inline=True)

    if type == 'EndPlateType' or type == 'EndPlateType-BC-zz' or type == 'EndPlateType-BC-yy':
        app_moment_load_eqn.append(NoEscape(r'\begin{aligned} {M_{\text{z}}}_{\min} &= 0.5 {M_{d}}_{\text{z}} \\'))
        app_moment_load_eqn.append(NoEscape(r'&= 0.5 \times' + moment_capacity + r' \\'))
        app_moment_load_eqn.append(NoEscape(r'&=' + min_mc + r' \\ \\'))

        app_moment_load_eqn.append(NoEscape(r'M_{u} &= \max(M_{\text{z}},~{M_{\text{z}}}_{\min}) \\'))

        if type == 'EndPlateType-BC-zz':
            app_moment_load_eqn.append(NoEscape(r'\text{but},~ & \leq {M_{d}}_{\text{z}} ~\text{of~the~column~section} \\'))
        elif type == 'EndPlateType-BC-yy':
            app_moment_load_eqn.append(NoEscape(r'\text{but},~ & \leq {M_{d}}_{y} ~\text{of~the~column~section} \\'))
        elif type == 'EndPlateType':
            app_moment_load_eqn.append(NoEscape(r'\text{but},~ & \leq {M_{d}}_{\text{z}} \\'))

        app_moment_load_eqn.append(NoEscape(r'&= \max(' + moment_input + r',' + min_mc + r') \\'))

        if type == 'EndPlateType-BC-zz' or type == 'EndPlateType-BC-yy':
            app_moment_load_eqn.append(NoEscape(r'& \leq ' + str(moment_capacity_supporting) + r' \\ \\'))
        elif type == 'EndPlateType':
            app_moment_load_eqn.append(NoEscape(r'& \leq ' + str(moment_capacity) + r' \\ \\'))

        app_moment_load_eqn.append(NoEscape(r'&=' + app_moment_load + r' \\ \\'))
        app_moment_load_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2.1.2}] \end{aligned}'))

    else:
        # app_moment_load_eqn = Math(inline=True)
        # app_moment_load_eqn.append(NoEscape(r'\begin{aligned} {M_{u}}_{min} &= 0.5 * {M_{d}}_{zz}\\'))
        # app_moment_load_eqn.append(NoEscape(r'&= 0.5 \times' + moment_capacity + r'\\'))
        # app_moment_load_eqn.append(NoEscape(r'&=' + min_mc + r'\\'))
        app_moment_load_eqn.append(NoEscape(r' \begin{aligned} M_{u} &= \max(M_{\text{z}},~{M_{\text{z}}}_{\min} )\\'))
        app_moment_load_eqn.append(NoEscape(r'&= \max(' + moment_input + r',~' + min_mc + r')\\'))
        app_moment_load_eqn.append(NoEscape(r'&=' + app_moment_load + r'\\ \\'))
        app_moment_load_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2.1.2}] \end{aligned}'))
    return app_moment_load_eqn


def effective_bending_moment_ep(bending_moment, axial_load, effective_moment, beam_D, beam_T):

    effective_moment_eqn = Math(inline=True)
    effective_moment_eqn.append(NoEscape(r'\begin{aligned} M_{ue} &= M_{u} ~+~ P_{\text{x}} \times \Bigg(\frac{D}{2} - \frac{T}{2} \Bigg) \times 10^{-3} \\ \\'))
    effective_moment_eqn.append(NoEscape(r' &= ' + str(bending_moment) + r' ~+ \\'))
    effective_moment_eqn.append(NoEscape(r' & ' + str(axial_load) + r' \times \Bigg(\frac{'
                                         + str(beam_D) + r'}{2} - \frac{' + str(beam_T) + r'}{2}\Bigg) \times 10^{-3} \\'))
    effective_moment_eqn.append(NoEscape(r' &= ' + str(effective_moment) + r' \end{aligned}'))

    return effective_moment_eqn


##################################
# End of Min load functions
###################################
# Other bolt functions
###################################

def force_in_bolt_due_to_load(P, n, T_ba, load='tension'):
    P = str(P)
    n = str(n)
    T_ba = str(T_ba)
    tension_in_bolt_due_to_axial_load_n_moment = Math(inline=True)
    if load == 'tension':
        tension_in_bolt_due_to_axial_load_n_moment.append(NoEscape(r'\begin{aligned} T_{ba} &= \frac{P}{\ n}\\'))
        tension_in_bolt_due_to_axial_load_n_moment.append(NoEscape(r'&=\frac{' + P + '}{' + n + r'}\\'))
    else:
        tension_in_bolt_due_to_axial_load_n_moment.append(NoEscape(r'\begin{aligned} V_{bv} &= \frac{V}{\ n}\\'))
        tension_in_bolt_due_to_axial_load_n_moment.append(NoEscape(r'&=\frac{' + P + '}{' + n + r'}\\'))
    tension_in_bolt_due_to_axial_load_n_moment.append(NoEscape(r'&= ' + T_ba + r'\end{aligned}'))
    return tension_in_bolt_due_to_axial_load_n_moment


def total_bolt_tension_force(T_ba, Q, T_b, bolt_type=''):
    T_ba = str(T_ba)
    Q = str(Q)
    T_b = str(T_b)

    total_tension_in_bolt = Math(inline=True)
    if bolt_type == "Bearing Bolt":
        total_tension_in_bolt.append(NoEscape(r'\begin{aligned} T_b &= T_{1} + Q \\'))
    else:
        total_tension_in_bolt.append(NoEscape(r'\begin{aligned} T_f &= T_{1} + Q \\'))
    total_tension_in_bolt.append(NoEscape(r'&=' + T_ba + '+' + Q + r' \\'))
    total_tension_in_bolt.append(NoEscape(r'&=' + T_b + r' \end{aligned}'))

    return total_tension_in_bolt


def tension_in_bolt_due_to_axial_load_n_moment(P, n, M, y_max, y_sqr, T_b):
    """
    Calculate tension in bolt due to axial load n moment

    Args:
          P: external axial load in KN (float)
          n: no. of bolts (int)
          M:external moment in KN-mm (float)
          y_max:vertical distance of farthest bolt from center of flange in mm (float)
          y_sqr: distance of each bolt from center of flange in mm square (float)
          T_b: tension in bolt due to axial load n moment in KN (float)
    Returns:
          tension in bolt due to axial load n moment
    """
    P = str(P)
    n = str(n)
    M = str(M)
    y_max = str(y_max)
    y_sqr = str(y_sqr)
    T_b = str(T_b)
    tension_in_bolt_due_to_axial_load_n_moment = Math(inline=True)
    tension_in_bolt_due_to_axial_load_n_moment.append(NoEscape(r'\begin{aligned} T_1 &= \frac{P}{\ n} + \frac{M \times y_{max}}{\ y_{sqr}}\\'))
    tension_in_bolt_due_to_axial_load_n_moment.append(
        NoEscape(r'&=\frac{' + P + r'\times 10^3}{' + n + r'} + \frac{' + M + r'\times 10^6\times' + y_max + r'}{' + y_sqr + r'}\\'))
    tension_in_bolt_due_to_axial_load_n_moment.append(NoEscape(r'&= ' + T_b + r'\end{aligned}'))
    return tension_in_bolt_due_to_axial_load_n_moment


def design_capacity_of_end_plate(M_dp, b_eff, f_y, gamma_m0, t_p):
    """
    Calculate design capacity of end plate
    Args:
         M_dp:Design capacity of end plate in N-mm (float)
         b_eff:Effective width for load dispersion
         f_y:Yeild strength of  plate material in N/mm square (float)
         gamma_m0: IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']  (float)
         t_p:Thickness of end plate
    Returns:
        design capacity of end plate

    """

    M_dp = str(M_dp)
    t_p = str(t_p)
    b_eff = str(b_eff)
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)

    design_capacity_of_end_plate = Math(inline=True)

    design_capacity_of_end_plate.append(NoEscape(r'\begin{aligned}  M_{dp} & = { \frac{ b_{\text{eff}} t_p^2 f_y}{ 4 \gamma_{m0}}}\\'))

    design_capacity_of_end_plate.append(
        NoEscape(r'&={\frac{' + b_eff + r'\times' + t_p + r'^2' + r' \times' + f_y + r'}{4\times' + gamma_m0 + r'}}\\'))
    design_capacity_of_end_plate.append(NoEscape(r'&=' + M_dp + r'\end{aligned}'))

    return design_capacity_of_end_plate


#####################################
# End of other bolt functions
#####################################
# common utility functions
#####################################

def required_IR_or_utilisation_ratio(IR):
    """
    :param IR:
    :return:
    """
    IR = str(IR)
    IR_req_eqn = Math(inline=True)
    IR_req_eqn.append(NoEscape(r'\begin{aligned} \leq' + IR + '\end{aligned}'))
    return IR_req_eqn


def display_prov(v, t, ref=None):
    """
    Args:
          v: value of t (float or int)
          t: typically a notation (string) (float)
          ref: unit of the value (ex: mm, kN)
                (can be none if it has no units)
    Returns:
          equation in form of t = v

    """

    v = str(v)
    display_eqn = Math(inline=True)
    if ref is not None:
        display_eqn.append(NoEscape(r'\begin{aligned} ' + t + ' &=' + v + '~(' + ref + r') \end{aligned}'))
    else:
        display_eqn.append(NoEscape(r'\begin{aligned} ' + t + ' &=' + v + r' \end{aligned}'))

    return display_eqn


def lever_arm_end_plate(lever_arm, bolt_row, ep_type=''):

    display_eqn = Math(inline=True)

    display_eqn.append(NoEscape(r'\begin{aligned} r &=' + str(lever_arm) + r' \\ \\'))

    if ep_type == 'Flushed - Reversible Moment':
        display_eqn.append(NoEscape(r'  & \text{Note: } r_{1} \text{ is the first row inside tension/top flange, }  \\'))
        display_eqn.append(NoEscape(r'  & r_{2} \text{ is the first row inside compression/bottom flange.}  \\'))
        display_eqn.append(NoEscape(r'  & \text{Further row(s) are added in a symmetrical manner} \\'))
        display_eqn.append(NoEscape(r'  & \text{with odd rows placed near the tension/top flange}  \\'))
        display_eqn.append(NoEscape(r'  & \text{and even row placed near the compression/bottom}  \\'))
        display_eqn.append(NoEscape(r'  & \text{flange respectively.}  \\ \\'))

    elif ep_type == 'Extended One Way - Irreversible Moment':
        if bolt_row == 3:
            display_eqn.append(NoEscape(r' & \text{Note: } r_{1} \text{is the first row outside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{2} \text{ is the first row inside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{3} \text{ is the first row inside compression/bottom flange,}  \\'))
            display_eqn.append(NoEscape(r' & \text{row(s) } r_{4} \text{ and beyond are rows inside the flange.}  \\ \\'))
        elif bolt_row == 4:
            display_eqn.append(NoEscape(r' & \text{Note: } r_{1} \text{is the first row outside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{2} \text{ is the first row inside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{3} \text{ is the first row inside compression/bottom flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{4} \text{ is the second row inside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & \text{row(s) } r_{5} \text{ and beyond are rows inside the flange.}  \\ \\'))
        elif bolt_row == 5:
            display_eqn.append(NoEscape(r' & \text{Note: } r_{1} \text{is the first row outside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{2} \text{ is the first row inside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{3} \text{ is the first row inside compression/bottom flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{4} \text{ is the second row inside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{5} \text{ is the second row outside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & \text{row(s) } r_{6} \text{ and beyond are rows inside the flange.}  \\ \\'))
        else:
            display_eqn.append(NoEscape(r' & \text{Note: } r_{1} \text{is the first row outside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{2} \text{ is the first row inside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{3} \text{ is the first row inside compression/bottom flange,}  \\'))
            display_eqn.append(NoEscape(r' & r_{4}~ is ~the~ second~ row ~inside~ tension/top~ flange  \\'))
            display_eqn.append(NoEscape(r' & r_{5} \text{ is the second row outside tension/top flange,}  \\'))
            display_eqn.append(NoEscape(r' & \text{row(s) } r_{6} \text{ and beyond are rows inside the flange.}  \\ \\'))

    elif ep_type == 'Extended Both Ways - Reversible Moment':
        display_eqn.append(NoEscape(r' & \text{Note: } r_{1} \text{ and } r_{2} \text{ are the first rows outside} \\'))
        display_eqn.append(NoEscape(r' & \text{and inside the tension/top flange.}    \\'))
        display_eqn.append(NoEscape(r' & r_{3} \text{ and } r_{4} \text{ are the first rows outside} \\'))
        display_eqn.append(NoEscape(r' & \text{and inside the compression/bottom flange.}    \\'))

        if bolt_row == 4:
            display_eqn.append(NoEscape(r' & \text{row(s) } r_{5} \text{ and beyond are the rows inside the flange,} \\'))
            display_eqn.append(NoEscape(r' & \text{placed in a symmetrical manner.} \\ \\'))

        elif bolt_row == 6:
            display_eqn.append(NoEscape(r' & r_{5} \text{ is the second row inside tension/top flange,} \\'))
            display_eqn.append(NoEscape(r' & \text{and } r_{6} \text{ is the second row inside the compression/bottom flange.} \\'))
            display_eqn.append(NoEscape(r' & \text{row(s) } r_{7}  \text{ and beyond are the rows inside the flange,} \\'))
            display_eqn.append(NoEscape(r' & \text{placed in a symmetrical manner.} \\ \\'))

        elif bolt_row >= 8:
            display_eqn.append(NoEscape(r' & r_{5} \text{ is the second row outside tension/top flange,} \\'))
            display_eqn.append(NoEscape(r' & \text{and, } r_{6}  \text{ is the second row inside the tension/top flange.} \\'))
            display_eqn.append(NoEscape(r' & r_{7} \text{ is the second row outside compression/bottom flange,} \\'))
            display_eqn.append(NoEscape(r' & \text{and, } r_{8} \text{ is the second row inside the compression/bottom flange.} \\'))
            display_eqn.append(NoEscape(r' & \text{row(s) } r_{9} \text{ and beyond are the rows inside the flange,}] \\'))
            display_eqn.append(NoEscape(r' & \text{placed in a symmetrical manner.} \\ \\'))

    display_eqn.append(NoEscape(r' & \text{Note: The lever arm is computed by considering} \\'))
    display_eqn.append(NoEscape(r' & \text{the N.A at the centre of the bottom flange.} \\'))
    display_eqn.append(NoEscape(r' & \text{Rows with identical lever arm values} \\'))
    display_eqn.append(NoEscape(r' & \text{mean they are considered acting as bolt} \\'))
    display_eqn.append(NoEscape(r' & \text{group near the tension or compression flange.} \end{aligned}'))

    return display_eqn


def get_pass_fail(required, provided, relation=''):
    if provided == 0 or required == 'N/A' or provided == 'N/A' or required == 0:
        return ''
    else:
        if relation == 'greater':
            if required > provided:
                return 'Pass'
            else:
                return 'Fail'
        elif relation == 'geq':
            if required >= provided:
                return 'Pass'
            else:
                return 'Fail'
        elif relation == 'leq':
            if required <= provided:
                return 'Pass'
            else:
                return 'Fail'
        else:
            if required < provided:
                return 'Pass'
            else:
                return 'Fail'


def min_prov_max(min, provided, max):
    """
    Calculate min and maximum axial capacity (provided)
    Args:
        min:0.3*tension yeilding caapcity of the section
        provided:resisting force
        max:tension yeilding caapcity of the section
    Returns:
        min and maximum axial capacity (provided)
    """
    min = float(min)
    provided = float(provided)
    max = float(max)
    if provided == 0:
        return 'N/A'
    else:
        if (max >= provided and min <= provided) or (min >= provided and max <= provided):
            return 'Pass'
        else:
            return 'Fail'


#####################################
# End of common utility functions
#####################################

def end_plate_gauge(connection, e_min, s, t_w, T_w, R_r, module='None'):
    g1 = round(2 * (e_min + s) + t_w, 2)
    g2 = round(2 * (e_min + R_r) + T_w, 2)
    g_min = round(max(g1, g2), 2)
    g1 = str(g1)
    g2 = str(g2)
    g_min = str(g_min)
    e_min = str(e_min)
    s = str(s)
    t_w = str(t_w)
    T_w = str(T_w)
    R_r = str(R_r)
    end_plate_gauge = Math(inline=True)
    if connection == VALUES_CONN_1[0]:
        end_plate_gauge.append(NoEscape(r'\begin{aligned}g_1 &= 2(e`_{min}+s)+t_w\\'))
        end_plate_gauge.append(NoEscape(r'&= 2(' + e_min + '+' + s + ')+' + t_w + r'\\'))
        end_plate_gauge.append(NoEscape(r'&=' + g1 + r'\\'))
        end_plate_gauge.append(NoEscape(r'g_2 &= 2(e`_{min}+R_r)+T_w\\'))
        end_plate_gauge.append(NoEscape(r'&= 2(' + e_min + '+' + R_r + ')+' + T_w + r'\\'))
        end_plate_gauge.append(NoEscape(r'&=' + g2 + r'\\'))
        end_plate_gauge.append(NoEscape(r'g_{min}&= max(g_1,g_2)\\'))
        end_plate_gauge.append(NoEscape(r'&=' + g_min + r' \end{aligned}'))
    else:
        end_plate_gauge.append(NoEscape(r'\begin{aligned}g_{min} &= 2(e`_{min}+s)+t_w\\'))
        end_plate_gauge.append(NoEscape(r'&= 2(' + e_min + '+' + s + ')+' + t_w + r'\\'))
        end_plate_gauge.append(NoEscape(r'&=' + g1 + r' \end{aligned}'))

    return end_plate_gauge


def row_col_limit(min=1, max=None, parameter="rows"):
    min = str(min)
    max = str(max)
    row_col_limit_eqn = Math(inline=True)
    if max != None and parameter == "rows":
        row_col_limit_eqn.append(NoEscape(r'\begin{aligned}' + min + r' \leq n_r \leq' + max + r' \end{aligned}'))
    elif max == None and parameter == "rows":
        row_col_limit_eqn.append(NoEscape(r'\begin{aligned} n_r \geq' + min + r' \end{aligned}'))
    elif max != None and parameter == "cols":
        row_col_limit_eqn.append(NoEscape(r'\begin{aligned}' + min + r' \leq n_c \leq' + max + r' \end{aligned}'))
    elif max == None and parameter == "cols":
        row_col_limit_eqn.append(NoEscape(r'\begin{aligned} n_c \geq' + min + r' \end{aligned}'))
    else:
        return None

    return row_col_limit_eqn


def get_trial_bolts(V_u, A_u, bolt_capacity, multiple=1, conn=None):
    """
    Calculate Total no. of bolts required for both side of web/ flange splices

    Args:
        V_u:Actual  shear force acting on the bolt(direct shear+ force due to eccentricity) in KN
        A_u: Axial force acting on the bolt in KN
        bolt_capacity: Capacity of  web/flange bolt  in KN
        multiple: 2 for web ,4 for flange  (int)
    Returns:
          Total no. of bolts required for both side of web/ flange splices
    """

    res_force = math.sqrt(V_u ** 2 + A_u ** 2)
    trial_bolts = multiple * math.ceil(res_force / bolt_capacity)
    V_u = str(V_u)
    A_u = str(A_u)
    bolt_capacity = str(bolt_capacity)
    trial_bolts = str(trial_bolts)
    trial_bolts_eqn = Math(inline=True)
    trial_bolts_eqn.append(NoEscape(r'\begin{aligned}R_{u} &= \sqrt{V_u^2+A_u^2}\\ \\'))

    trial_bolts_eqn.append(NoEscape(r'n_{\text{trial}} &= R_u/ V_{bolt}\\ \\'))

    if conn == "flange_web":
        trial_bolts_eqn.append(NoEscape(r'R_{u} &= \frac{2 \times \sqrt{' + V_u + r'^2+' + A_u + r'^2}}{' + bolt_capacity + r'}\\'))
    else:
        trial_bolts_eqn.append(NoEscape(r'R_{u} &= \frac{\sqrt{' + V_u + r'^2+' + A_u + r'^2}}{' + bolt_capacity + r'}\\'))
    trial_bolts_eqn.append(NoEscape(r'&=' + trial_bolts + r'\end{aligned}'))
    return trial_bolts_eqn


def parameter_req_bolt_force(bolts_one_line, gauge, ymax, xmax, bolt_line, pitch, length_avail, conn=None):
    """
    Calculate xmax and ymax
    Args:
        bolts_one_line: No. of bolts in one row (float)
        gauge: Gauge distance in mm (float)
        ymax: Vertical distance of farthest bolt from center of rotation of bolt group in mm (float)
        xmax: :Horizontal distance of farthest bolt from center of rotation of bolt group in mm (float)
        bolt_line: No. of row of bolts (float)
        pitch: Pitch distance in mm (float)
        length_avail: Length available in mm  (float)
        conn:Connection type (str)
    Returns:
         xmax and ymax

    """

    bolts_one_line = str(bolts_one_line)
    ymax = str(ymax)
    xmax = str(xmax)
    gauge = str(gauge)
    pitch = str(pitch)
    bolt_line = str(bolt_line)
    length_avail = str(length_avail)

    parameter_req_bolt_force_eqn = Math(inline=True)
    parameter_req_bolt_force_eqn.append(NoEscape(r'\begin{aligned} l_n~~~ &= \text{length available} \\'))
    if conn == 'fin':
        parameter_req_bolt_force_eqn.append(NoEscape(r' l_n~~~ &= p~(n_r - 1)\\'))
    elif conn == 'beam_beam':
        parameter_req_bolt_force_eqn.append(NoEscape(r' l_n~~~ &= g~(n_r - 1)\\'))
    elif conn == 'col_col':
        parameter_req_bolt_force_eqn.append(NoEscape(r' l_n~~~ &= g~(n_c - 1)\\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' &= ' + gauge + r' \times (' + bolts_one_line + r' - 1)\\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' & =' + length_avail + r'\\ \\'))

    parameter_req_bolt_force_eqn.append(NoEscape(r' y_{\text{max}} &= l_n / 2\\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' &= ' + length_avail + r' / 2 \\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' & =' + ymax + r'\\ \\'))

    if conn == 'fin':
        parameter_req_bolt_force_eqn.append(NoEscape(r'x_{\text{max}} &= g(n_c - 1)/2 \\'))
        parameter_req_bolt_force_eqn.append(NoEscape(r' &= ' + pitch + r' \times (' + bolt_line + r' - 1) / 2 \\'))
    elif conn == 'col_col':
        parameter_req_bolt_force_eqn.append(NoEscape(r'x_{\text{max}} &= p(\frac{n_r}{2} - 1) / 2 \\'))
        parameter_req_bolt_force_eqn.append(NoEscape(r' &= ' + pitch + r' \times (\frac{' + bolt_line + r'}{2} - 1) / 2 \\'))
    else:
        parameter_req_bolt_force_eqn.append(NoEscape(r'x_{\text{max}} &= p(\frac{n_c}{2} - 1) / 2 \\'))
        parameter_req_bolt_force_eqn.append(NoEscape(r' &= ' + pitch + r' \times (\frac{' + bolt_line + r'}{2} - 1) / 2 \\'))

    parameter_req_bolt_force_eqn.append(NoEscape(r' & =' + xmax + r'\end{aligned}'))

    return parameter_req_bolt_force_eqn


def moment_demand_req_bolt_force(shear_load, web_moment, moment_demand, ecc):
    """
     Calculate moment demand on web section
     Args:
          shear_load: Factored shear force acting on member in KN (float)
          web_moment: Moment in web in KN-m (float)
          moment_demand: Moment demand by section in N-mm (float)
          ecc:Distance between bolt center line toface of connected supporting section in mm (float)
    Returns:
          Moment demand on  web section in N-mm (float)

    """

    ecc = str(ecc)
    web_moment = str(web_moment)
    moment_demand = str(moment_demand)
    shear_load = str(shear_load)
    loads_req_bolt_force_eqn = Math(inline=True)

    loads_req_bolt_force_eqn.append(NoEscape(r'\begin{aligned}  M_d &= (V_u \times \text{ecc} + M_w)\\ \\'))
    loads_req_bolt_force_eqn.append(NoEscape(r'& \text{ecc = eccentricity} \\'))
    loads_req_bolt_force_eqn.append(NoEscape(r'& M_w = \text{external moment acting on web} \\ \\'))
    loads_req_bolt_force_eqn.append(
        NoEscape(r' &= \frac{(' + shear_load + r' \times 10^3 \times' + ecc + ' + ' + web_moment + r'\times10^6)}{10^6}\\'))
    loads_req_bolt_force_eqn.append(NoEscape(r' & =' + moment_demand + r'\end{aligned}'))
    return loads_req_bolt_force_eqn


def Vres_bolts(bolts_one_line, ymax, xmax, bolt_line, axial_load, moment_demand, r, vbv, tmv, tmh, abh, vres, shear_load, conn=None):
    """
    Calculte resultant shear load on each bolt
    Args:
         bolts_one_line: No. of bolts provided in one row (int)
         ymax: Vertical distance of farthest bolt from center of rotation of bolt group in mm (float)
         xmax:Horizontal   distance of farthest bolt from center of rotation of bolt group in mm (float)
         bolt_line: NO. of row of bolts (int)
         axial_load: Axial compressive force due to factored loads in KN (float)
         moment_demand:Moment demand on  web section in KN-mm (float)
         r: Distance of each bolt from center of rotation of each group in mm (float)
         vbv: Horizontal force acting on each bolt in KN (float)
         tmv:Vertical shear force acting on each bolt due to moment devloped by ecentricity in KN (float)
         tmh: Horizontal shear force acting on each bolt due to moment devloped by ecentricity in KN (float)
         abh: Vertical force acting on each bolt in KN (float)
         vres: Resultant sher load on  each bolt in KN (float)
         shear_load: Factored shear force acting on member in KN (float)
    Returns:
          Resultant shear load on bolt in KN (float)

    """

    bolts_one_line = str(bolts_one_line)
    ymax = str(ymax)
    xmax = str(xmax)
    bolt_line = str(bolt_line)

    r = str(r)
    moment_demand = str(moment_demand)
    axial_load = str(axial_load)
    shear_load = str(shear_load)
    vbv = str(vbv)
    tmv = str(tmv)
    tmh = str(tmh)
    abh = str(abh)
    vres = str(vres)
    Vres_bolts_eqn = Math(inline=True)
    if conn == "beam_beam":
        Vres_bolts_eqn.append(NoEscape(r'\begin{aligned} vbv~~ &= V_u / (n_r \times (n_c/2))\\'))
        Vres_bolts_eqn.append(NoEscape(r' &= \frac{' + shear_load + '}{ (' + bolts_one_line + r'\times(' + bolt_line + r'/2))}\\'))
    elif conn == "col_col":
        Vres_bolts_eqn.append(NoEscape(r'\begin{aligned} vbv~~ &= V_u / ((n_r/2) \times n_c)\\'))
        Vres_bolts_eqn.append(NoEscape(r' &= \frac{' + shear_load + '}{ (' + bolts_one_line + r'\times(' + bolt_line + r'/2))}\\'))
    else:
        Vres_bolts_eqn.append(NoEscape(r'\begin{aligned} vbv~~ &= V_u / (n_r \times n_c)\\'))
        Vres_bolts_eqn.append(NoEscape(r' &= \frac{' + shear_load + '}{ (' + bolts_one_line + r'\times' + bolt_line + r')}\\'))

    Vres_bolts_eqn.append(NoEscape(r' & =' + vbv + r'\\ \\'))
    Vres_bolts_eqn.append(NoEscape(r'tmh~ &= \frac{M_d \times y_{\text{max}} }{ \Sigma r_i^2} \\'))
    Vres_bolts_eqn.append(NoEscape(r' &= \frac{' + moment_demand + r'\times' + ymax + '}{' + r + r'}\\'))
    Vres_bolts_eqn.append(NoEscape(r' & =' + tmh + r'\\ \\'))

    Vres_bolts_eqn.append(NoEscape(r' tmv ~&= \frac{M_d \times x_{\text{max}}}{\Sigma r_i^2}\\'))
    Vres_bolts_eqn.append(NoEscape(r'&= \frac{' + moment_demand + r'\times ' + xmax + '}{' + r + r'}\\'))
    Vres_bolts_eqn.append(NoEscape(r' & =' + tmv + r'\\ \\'))
    if conn == "beam_beam":
        Vres_bolts_eqn.append(NoEscape(r' abh~ & = \frac{A_u }{(n_r \times n_c/2)}\\'))
        Vres_bolts_eqn.append(NoEscape(r'  & =\frac{' + axial_load + '}{ (' + bolts_one_line + r' \times(' + bolt_line + r'/2))}\\'))
    elif conn == "col_col":
        Vres_bolts_eqn.append(NoEscape(r' abh~ & = \frac{A_u }{((n_r/2) \times n_c)}\\'))
        Vres_bolts_eqn.append(NoEscape(r'  & =\frac{' + axial_load + '}{ (' + bolts_one_line + r' \times(' + bolt_line + r'/2))}\\'))
    else:
        Vres_bolts_eqn.append(NoEscape(r' abh~ & = \frac{A_u }{(n_r \times n_c)}\\'))
        Vres_bolts_eqn.append(NoEscape(r'  & =\frac{' + axial_load + '}{ (' + bolts_one_line + r' \times' + bolt_line + r')}\\'))

    Vres_bolts_eqn.append(NoEscape(r' & =' + abh + r'\\ \\'))
    Vres_bolts_eqn.append(NoEscape(r' v_{\text{res}} &=\sqrt{(vbv +tmv) ^ 2 + (tmh+abh) ^ 2}\\'))
    # Vres_bolts_eqn.append(NoEscape(r' vres &= \sqrt((vbv + tmv) ^ 2 + (tmh + abh) ^ 2)\\'))
    Vres_bolts_eqn.append(NoEscape(r'  &= \sqrt{(' + vbv + ' +' + tmv + ') ^2 + (' + tmh + '+' + abh + r') ^ 2}\\'))
    Vres_bolts_eqn.append(NoEscape(r' & =' + vres + r'\end{aligned}'))

    return Vres_bolts_eqn


def forces_in_web(Au, T, A, t, D, Zw, Mu, Z, Mw, Aw):
    """
    Calculate axial force in web and moment in web
    Args:
         Au: Gross area of web cover plate in mm^2 (float)
         T: Thickness of flaNGE in mm (float)
         A: Total area of smaller column in mm square (float)
         t: Thickness of web in mm (float)
         D: Depth of the column in mm (float)
         Zw: Section modules of web in mm^4 (float)
         Mu: Factored bending moment in N-mm (float)
         Z: Section modules of section in mm^4 (float)
         Mw:Moment in web in N-mm (float)
         Aw: Vertical compression force carried by web of the section
    Returns:
          Web axial force and moment in web
    """
    Au = str(Au)
    T = str(T)
    A = str(A)
    t = str(t)
    D = str(D)
    Zw = str(Zw)
    Mu = str(Mu)
    Z = str(Z)
    Mw = str(Mw)
    Aw = str(Aw)
    forcesinweb_eqn = Math(inline=True)

    forcesinweb_eqn.append(NoEscape(r'\begin{aligned}A_w &= \text{Axial force in web}  \\'))
    forcesinweb_eqn.append(NoEscape(r'  &= \frac{(D- 2T) t Au }{A} \\'))
    forcesinweb_eqn.append(NoEscape(r'&= \frac{(' + D + r'- 2 \times' + T + r')\times' + t + r'\times' + Au + ' }{' + A + r'} \\'))
    forcesinweb_eqn.append(NoEscape(r'&=' + Aw + r'~ \text{kN} \\ \\'))

    forcesinweb_eqn.append(NoEscape(r'M_w &= \text{Moment in web}  \\'))
    forcesinweb_eqn.append(NoEscape(r' &= \frac{Z_w Mu}{Z} \\'))
    forcesinweb_eqn.append(NoEscape(r'&= \frac{' + Zw + r' \times ' + Mu + '}{' + Z + r'} \\'))
    forcesinweb_eqn.append(NoEscape(r'&=' + Mw + r'~{\text{kNm}} \end{aligned}'))
    return forcesinweb_eqn


def forces_in_flange(Au, B, T, A, D, Mu, Mw, Mf, Af, ff):
    """
    Calculate forces in flange and flange moment
    Args:
         Au: Factored axial force in KN (float)
         B: Width of flange in mm (float)
         T: Thikness of flange in mm (float)
         A: Total area of smaller column in mm square (float)
         D: Depth of column in mm (float)
         Mu: Factored bending moment in KN-mm (float)
         Mw: Moment in web in KN-mm (float)
         Mf: Moment in flange in KN-mm (float)
         Af: Axial force in flange in KN (float)
         ff: Force in each cover plate due to moment in KN (float)
    Returns:
          Flange moment,force in each cover plate due to moment,Axial and flange force

    """
    Au = str(Au)
    B = str(B)
    T = str(T)
    A = str(A)
    D = str(D)
    Mu = str(Mu)
    Mw = str(Mw)
    Mf = str(Mf)
    Af = str(Af)
    ff = str(ff)
    forcesinflange_eqn = Math(inline=True)
    forcesinflange_eqn.append(NoEscape(r'\begin{aligned} A_f&= \text{Axial force in flange}  \\'))
    forcesinflange_eqn.append(NoEscape(r'&= \frac{Au B T}{A} \\'))
    forcesinflange_eqn.append(NoEscape(r'&= \frac{' + Au + r' \times ' + B + r'\times' + T + '}{' + A + r'} \\'))
    forcesinflange_eqn.append(NoEscape(r'&=' + Af + r'~ \text{kN}\\ \\'))

    forcesinflange_eqn.append(NoEscape(r'M_f& =\text{Moment in flange} \\'))
    forcesinflange_eqn.append(NoEscape(r' & = Mu - M_w\\'))
    forcesinflange_eqn.append(NoEscape(r'&= ' + Mu + '-' + Mw + r'\\'))
    forcesinflange_eqn.append(NoEscape(r'&=' + Mf + r'~ \text{kNm}\\ \\'))

    forcesinflange_eqn.append(NoEscape(r' F_f& = \text{flange force}  \\'))
    forcesinflange_eqn.append(NoEscape(r'& = \frac{M_f \times10^3}{D-T} + A_f \\'))
    forcesinflange_eqn.append(NoEscape(r'&= \frac{' + Mf + r'\times 10^3}{' + D + '-' + T + '} +' + Af + r' \\'))
    forcesinflange_eqn.append(NoEscape(r'&=' + ff + r'~ \text{kN} \end{aligned}'))

    return forcesinflange_eqn


# def min_plate_ht_req(beam_depth,r_r,t_f,min_plate_ht):
#     """
#     Calculate min plate height required
#     Args:
#         beam_depth: Depth of section in mm (float)
#         min_plate_ht:Min plate height required in mm (float)
#     Returns:
#           Min plate height required
#     Note:
#             Reference:
#             INSDAG - Chapter 5, Section 5.2.3
#
#     """
#     beam_depth = str(beam_depth)
#     r_r = str(r_r)
#     t_f = str(t_f)
#     min_plate_ht = str(round(min_plate_ht, 2))
#     min_plate_ht_eqn = Math(inline=True)
#     min_plate_ht_eqn.append(NoEscape(r'\begin{aligned}0.6 \times &(d_b - 2 \times t_f - 2 \times r_r)\\'))
#     min_plate_ht_eqn.append(NoEscape(r'&= 0.6 \times (' + beam_depth +r'- 2 \times'+t_f+r'- 2 \times'+r_r+r')\\'))
#     min_plate_ht_eqn.append(NoEscape(r'&=' + min_plate_ht + r'\\ \\'))
#     min_plate_ht_eqn.append(NoEscape(r'&[Ref.~ INSDAG-Chpt.5,~Sect. 5.2.3]\end{aligned}'))
#
#     return min_plate_ht_eqn


def min_flange_plate_ht_req(beam_width, min_flange_plate_ht):  ## when only outside plate is considered
    """
    Calculate  Min flane plate height
    Args:
           beam_width: Width of section in mm (float)
           min_flange_plate_ht:Min flange plate height in mm (float)
    Returns:
           Required min flange plate height in mm (float)
    """
    beam_width = str(beam_width)
    min_flange_plate_ht = str(min_flange_plate_ht)
    min_flange_plate_ht_eqn = Math(inline=True)
    min_flange_plate_ht_eqn.append(NoEscape(r'\begin{aligned} & \text{min.  flange plate height = beam width} \\'))
    min_flange_plate_ht_eqn.append(NoEscape(r'&=' + min_flange_plate_ht + r'\end{aligned}'))

    return min_flange_plate_ht_eqn


def min_inner_flange_plate_ht_req(beam_width, web_thickness, root_radius,
                                  min_inner_flange_plate_ht):  ## when inside and outside plate is considered #todo
    """
    Calculate minimum inner flange plate height
    Args:
        beam_width: Width of section in mm (float)
        web_thickness: Web thickness in mm (float)
        root_radius: Root radius in mm (float)
        min_inner_flange_plate_ht: Min inner flange plate height  in mm (float)
    Returns:
         Minimum inner flange plate height
    """
    beam_width = str(beam_width)  ### same function used for max height
    min_inner_flange_plate_ht = str(min_inner_flange_plate_ht)
    web_thickness = str(web_thickness)
    root_radius = str(root_radius)
    min_inner_flange_plate_ht_eqn = Math(inline=True)
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'\begin{aligned}&= \frac{B -t- (2R1)}{2}\\'))
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'&=\frac{' + beam_width + r' -' + web_thickness + r' - 2\times' + root_radius + r'}{2}\\'))
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'&=' + min_inner_flange_plate_ht + r'\end{aligned}'))

    return min_inner_flange_plate_ht_eqn


def max_plate_ht_req(connectivity, beam_depth, beam_f_t, beam_r_r, notch, max_plate_h):
    """
    Calculate maximum height for fin plate
    Args:
          connectivity:
          beam_depth:Section depth in mm (float)
          beam_f_t: Flange thickness in mm  (float)
          beam_r_r:Root radius in mm  (float)
          notch: Supported section notch height in mm  (float)
          max_plate_h: Fin plate of max height in mm  (float)
    Returns:
          Maximum height for Fin plate
    """
    beam_depth = str(beam_depth)
    beam_f_t = str(beam_f_t)
    beam_r_r = str(beam_r_r)
    max_plate_h = str(max_plate_h)
    notch = str(notch)
    max_plate_ht_eqn = Math(inline=True)
    if connectivity in VALUES_CONN_1:
        max_plate_ht_eqn.append(NoEscape(r'\begin{aligned} &d_b - 2 (t_{bf} + r_{b1} + \text{gap})\\'))
        max_plate_ht_eqn.append(NoEscape(r'&=' + beam_depth + r'- 2\times (' + beam_f_t + '+' + beam_r_r + r'+ 10)\\'))
    else:
        max_plate_ht_eqn.append(NoEscape(r'\begin{aligned} &d_b - t_{bf} + r_{b1} - notch_h\\'))
        max_plate_ht_eqn.append(NoEscape(r'&=' + beam_depth + '-' + beam_f_t + '+' + beam_r_r + '-' + notch + r'\\'))
    max_plate_ht_eqn.append(NoEscape(r'&=' + max_plate_h + '\end{aligned}'))
    return max_plate_ht_eqn


def ep_min_plate_width_req(g, e_min, wp_min):
    g = str(g)
    e_min = str(e_min)
    wp_min = str(wp_min)
    ep_min_plate_w_eqn = Math(inline=True)
    ep_min_plate_w_eqn.append(NoEscape(r'\begin{aligned} w_{p_{\text{min}}} &= g` + e`_{\text{min}}~2 \\'))
    ep_min_plate_w_eqn.append(NoEscape(r'&=' + g + '+' + e_min + r'\times2\\'))
    ep_min_plate_w_eqn.append(NoEscape(r'&=' + wp_min + r'\end{aligned}'))
    return ep_min_plate_w_eqn


def ep_max_plate_width_avail(conn, D, T_w, R_r, T_f, wp_max):
    conn = str(conn)
    D = str(D)
    T_w = str(T_w)
    R_r = str(R_r)
    T_f = str(T_f)
    wp_max = str(wp_max)
    ep_max_plate_w_eqn = Math(inline=True)
    if conn == VALUES_CONN_1[0]:
        ep_max_plate_w_eqn.append(NoEscape(r'\begin{aligned} w_{p_{\text{max}}} &= T_f \\'))
        ep_max_plate_w_eqn.append(NoEscape(r'&=' + wp_max + '\end{aligned}'))
    elif conn == VALUES_CONN_1[1]:
        ep_max_plate_w_eqn.append(NoEscape(r'\begin{aligned} w_{p_{\text{max}}} &= D - 2T_f - 2R_r \\'))
        ep_max_plate_w_eqn.append(NoEscape(r'&=' + D + r'-2\times' + T_f + r'-2\times' + R_r + r'\\'))
        ep_max_plate_w_eqn.append(NoEscape(r'&=' + wp_max + '\end{aligned}'))
    else:
        ep_max_plate_w_eqn.append(NoEscape(r'\begin{aligned} N/A \end{aligned}'))
    return ep_max_plate_w_eqn


# TODO: YASH --- Try using ep_min_plate_width_req
def end_plate_ht_req(D, e, h_p):
    """Calculate end plate height foe column end plate connection
    Args:
         D:section depth in mm (float)
         e: End distance in mm (float)
         h_p:End plate height in mm (float)
    Returns:
         End plate height
    """

    D = str(D)
    h_p = str(h_p)
    e = str(e)
    end_plate_ht_eqn = Math(inline=True)

    end_plate_ht_eqn.append(NoEscape(r'\begin{aligned} &D + 4e \\'))
    end_plate_ht_eqn.append(NoEscape(r'&=' + D + '+' + r' 4 \times' + e + r'\\'))
    end_plate_ht_eqn.append(NoEscape(r'&=' + h_p + '\end{aligned}'))
    return end_plate_ht_eqn


def end_plate_thk_req(M_ep, b_eff, f_y, gamma_m0, t_p, t_b, q, l_e, l_v, f_o, b_e, beta, module=''):
    """
    Calculate end plate thickness
     Args:
         M_ep:Moment acting on the end plate in N-mm (float)
         b_eff:Effective width for load dispersion
         f_y:Yeild strength of  plate material in N/mm square (float)
         gamma_m0: IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']  (float)
         t_p:Thickness of end plate
    Returns:
        end plate thickness
    """

    M_ep = str(M_ep)
    t_p = str(t_p)
    b_eff = str(int(b_eff))
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)
    t_b = str(t_b)
    q = str(q)
    l_e = str(l_e)
    l_v = str(l_v)
    f_o = str(f_o)
    b_e = str(b_e)
    beta = str(beta)

    end_plate_thk_eqn = Math(inline=True)

    if module == 'BC_EP' or module == 'BB_EP':
        end_plate_thk_eqn.append(NoEscape(r'\begin{aligned} t_p &=  \sqrt{\frac{4 M_{cr}} {b_{e} (f_{y} / \gamma_{m0})} } \\'))
        end_plate_thk_eqn.append(NoEscape(r'&=  \sqrt{\frac{4 \times ' + M_ep + r' \times 10^{6}} {' + b_eff + r' \times (' + f_y + r' / '
                                          + gamma_m0 + r')} } \\'))

    if module == 'Column_EP':
        end_plate_thk_eqn.append(NoEscape(r'\begin{aligned} t_p &=  max\Bigg(\sqrt{\frac{4 M_{cr}} {b_{eff} (f_{y} / \gamma_{m0})} }, ~ \\'))
        end_plate_thk_eqn.append(NoEscape(r'& \sqrt[4]{\Bigg(T_1 - \frac{2 Q l_e}{l_v}\Bigg) \times '
                                          r'\Bigg(\frac{27 l_e l_v^{2}}{\beta \eta f_o b_e}\Bigg) }~ \Bigg) \\ \\'))

        end_plate_thk_eqn.append(NoEscape(r' &=  max\Bigg(\sqrt{\frac{4 \times ' + M_ep + r' \times 10^{6}} {' + b_eff + r' \times ('
                                          + f_y + r' / ' + gamma_m0 + r')} }, ~ \\'))
        end_plate_thk_eqn.append(NoEscape(r'& \sqrt[4]{\Bigg(' + t_b + r' - \frac{2 \times ' + q + r' \times ' + l_e + r'}{'
                                          + l_v + r'}\Bigg) \times '
                                          r'\Bigg(\frac{27 \times ' + l_e + r' \times ' + l_v + r'^{2}}{' + beta + r' \times 1.5 \times '
                                          + f_o + r' \times ' + b_e + r'}\Bigg) }~ \Bigg) \\ \\'))

    end_plate_thk_eqn.append(NoEscape(r'&=' + t_p + r' \end{aligned}'))

    return end_plate_thk_eqn


def end_plate_moment_capacity(M_ep, b_eff, f_y, gamma_m0, t_p):
    """
    Calculate end plate moment capacity
     Args:
         M_ep:Moment acting on the end plate in N-mm (float)
         b_eff:Effective width for load dispersion
         f_y:Yeild strength of  plate material in N/mm square (float)
         gamma_m0: IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']  (float)
         t_p:Thickness of end plate
    Returns:
        end plate M_p
    """

    M_ep = str(M_ep)
    t_p = str(int(t_p))
    b_eff = str(int(b_eff))
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)

    moment_capacity = Math(inline=True)

    moment_capacity.append(NoEscape(r'\begin{aligned} M_{p} &=  \Big( \frac{b_{e} t_{p}^{2}} {4} \Big) \times \frac{f_{y}}{\gamma_{m0}} \\'))
    moment_capacity.append(NoEscape(r'&=  \frac{' + b_eff + r' \times ' + t_p + r'^{2}} {4} \times \frac{' + f_y + r'}{'
                                    + gamma_m0 + r'} \times 10^{-6} \\'))
    moment_capacity.append(NoEscape(r'&=' + M_ep + ' \end{aligned}'))

    return moment_capacity


def moment_acting_on_end_plate(M_ep, t_b, e):
    """  Calculate moment acting on the  end plate
    Args:
         M_ep:  moment acting on the  end plate in N-mm (float)
         b_eff:Effective width for load dispersion
         f_y:Yeild strength of  plate material in N/mm square (float)
         gamma_m0: IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']  (float)
         t_p:Thickness of end plate
    Returns:
         moment acting on the end plate

    """

    M_ep = str(M_ep)
    t_b = str(t_b)
    e = str(e)

    # gamma_m0= str(gamma_m0)

    moment_acting_on_end_plate = Math(inline=True)

    moment_acting_on_end_plate.append(NoEscape(r'\begin{aligned}  M_{ep}&= \text{Tension in bolt X end distance} \\'))
    moment_acting_on_end_plate.append(NoEscape(r'&= T_b \times e\\'))

    moment_acting_on_end_plate.append(NoEscape(r'&=' + t_b + r'\times' + e + r'\\'))
    moment_acting_on_end_plate.append(NoEscape(r'&=' + M_ep + '\end{aligned}'))
    return moment_acting_on_end_plate


def moment_acting_on_end_plate_flush(M_ep, t_b, e, tb_2):
    """  Calculate moment acting on the  end plate
    Args:
         M_ep:  moment acting on the  end plate in N-mm (float)
         b_eff:Effective width for load dispersion
         f_y:Yeild strength of  plate material in N/mm square (float)
         gamma_m0: IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']  (float)
         t_p:Thickness of end plate
    Returns:
         moment acting on the end plate

    """

    M_ep = str(M_ep)
    t_b = str(t_b)
    tb_2 = str(tb_2)
    e = str(e)

    # gamma_m0= str(gamma_m0)

    moment_acting_on_end_plate = Math(inline=True)

    moment_acting_on_end_plate.append(NoEscape(r'\begin{aligned}  M_{ep}&= \text{max (0.5 X Tension in first bolt X end distance, } \\'))
    moment_acting_on_end_plate.append(NoEscape(r'& \text{Tension in second bolt X end distance)} \\'))
    moment_acting_on_end_plate.append(NoEscape(r'&= \max(0.5  T_b1  e, ~ T_b2  e)\\'))

    moment_acting_on_end_plate.append(NoEscape(r'&= \max(0.5  \times  ' + t_b + r'\times' + e + ',~' + tb_2 + r'\times' + e + r'\\'))
    moment_acting_on_end_plate.append(NoEscape(r'&=' + M_ep + '\end{aligned}'))
    return moment_acting_on_end_plate


def ht_of_stiff(t_s):
    t_s = str(t_s)
    stiff_ht = Math(inline=True)
    stiff_ht.append(NoEscape(r'\begin{aligned}  h_{s}&= 14~ts \\'))
    stiff_ht.append(NoEscape(r'&=' + t_s + '\end{aligned}'))
    return stiff_ht


def ht_of_stiff1(t_s):
    t_s = str(t_s)
    stiff_ht = Math(inline=True)
    stiff_ht.append(NoEscape(r'\begin{aligned}  h_{s}&= 14~ts \\'))
    stiff_ht.append(NoEscape(r'& if~<~100~mm\\'))
    stiff_ht.append(NoEscape(r'&=' + t_s + '\end{aligned}'))
    return stiff_ht


def wt_of_stiff(w_s, e):
    w_s = str(w_s)
    e = str(e)
    stiff_wt = Math(inline=True)
    stiff_wt.append(NoEscape(r'\begin{aligned}  w_{s}&= 2~e \\'))
    stiff_wt.append(NoEscape(r'&= 2 \times' + e + r'\\'))
    stiff_wt.append(NoEscape(r'&=' + w_s + '\end{aligned}'))
    return stiff_wt


def min_plate_length_req(min_pitch, min_end_dist, bolt_line, min_length):
    """
    Calculate minimum length of fin plate
     Args:

        min_pitch: minimum pitch distance in mm (float)
        min_end_dist: minimum end distance in mm (float)
        bolt_line: no. of rows of bolts in fin plate (int)
        min_length: minimum length of fin plate in  mm (float)
    Returns:
           minimum length of fin plate
    """

    min_pitch = str(min_pitch)
    min_end_dist = str(min_end_dist)
    bolt_line = str(bolt_line)
    min_length = str(min_length)
    min_plate_length_eqn = Math(inline=True)
    min_plate_length_eqn.append(NoEscape(r'\begin{aligned} &2e_{\text{min}} + (n_c-1) p_{\text{min}})\\'))
    min_plate_length_eqn.append(NoEscape(r'&=2\times' + min_end_dist + '+(' + bolt_line + r'-1)  \times  ' + min_pitch + r'\\'))
    min_plate_length_eqn.append(NoEscape(r'&=' + min_length + '\end{aligned}'))
    return min_plate_length_eqn


def min_angle_leg_length(min_pitch, min_end_dist, gap, angle_thickness, root_radius, bolt_line, min_leg_length):
    min_pitch = str(min_pitch)
    min_end_dist = str(min_end_dist)
    bolt_line = str(bolt_line)
    angle_thickness = str(angle_thickness)
    root_radius = str(root_radius)
    min_leg_length = str(min_leg_length)
    min_plate_length_eqn = Math(inline=True)
    if gap > 0.0:
        gap = str(gap)
        min_plate_length_eqn.append(NoEscape(
            r'\begin{aligned} & \text{max} \bigg(\text{gap},~ t_{\text{cleat}}+r_{r_{\text{angle}}} + 2e\textquotesingle_{\text{min}} + (n_c-1) g_{\text{min}} \bigg) \\'))
        min_plate_length_eqn.append(NoEscape(r'&= \text{max} \bigg(' + gap + ',~' + angle_thickness + '+' + root_radius + '' + r'+2\times' +
                                             min_end_dist + '+(' + bolt_line + r'-1)  \times  ' + min_pitch + r' \bigg)\\'))
    else:
        min_plate_length_eqn.append(NoEscape(
            r'\begin{aligned} &t_{\text{cleat}}+r_{r_{\text{angle}}} + 2e\textquotesingle_{\text{min}} + (n_c-1) g_{\text{min}}\\'))
        min_plate_length_eqn.append(
            NoEscape(r'&=' + angle_thickness + '+' + root_radius + r' +2\times' + min_end_dist +
                     '+(' + bolt_line + r'-1)  \times  ' + min_pitch + r'\\'))
    min_plate_length_eqn.append(NoEscape(r'&=' + min_leg_length + '\end{aligned}'))
    return min_plate_length_eqn


def min_flange_plate_length_req(min_pitch, min_end_dist, bolt_line, min_length, gap, sec=None):
    """
    Calculate minimum flange plate length required
    Args:

        min_pitch:Min pitch distance of flange bolt in mm (float)
        min_end_dist: Min end distance of flange bolt in mm (float)
        bolt_line: No. of bolts provided in one line in mm (int)
        min_length: Flange plate of minimum lenght in mm (float)
        gap: Gap between flange plate in mm (float)
        sec: Beam or Column (str)
    Returns:
        minimum flange plate length required
    """

    min_pitch = str(min_pitch)
    min_end_dist = str(min_end_dist)
    bolt_line = str(bolt_line)
    min_length = str(min_length)
    gap = str(gap)
    min_flange_plate_length_eqn = Math(inline=True)
    if sec == "column":
        min_flange_plate_length_eqn.append(NoEscape(r'\begin{aligned} & 2 \times [2e_{\text{min}} + ({\frac{n_r}{2}}-1)p_{\text{min}})]\\'))
        min_flange_plate_length_eqn.append(NoEscape(r'& +\frac{\text{gap}}{2}]\\ \\'))

        min_flange_plate_length_eqn.append(
            NoEscape(r'&=2 \times [(2\times' + min_end_dist + r' + (\frac{' + bolt_line + r'}{2}' + r'-1)  \times  ' + min_pitch + r'\\'))
        min_flange_plate_length_eqn.append(NoEscape(r'&= + \frac{' + gap + r'}{2}]\\ \\'))

        min_flange_plate_length_eqn.append(NoEscape(r'&=' + min_length + '\end{aligned}'))
    else:
        min_flange_plate_length_eqn.append(NoEscape(r'\begin{aligned} & 2 \times [2e_{min} + ({\frac{n_c}{2}}-1)  \times  p_{min})]\\'))
        min_flange_plate_length_eqn.append(NoEscape(r'& +\frac{gap}{2}]\\ \\'))

        min_flange_plate_length_eqn.append(
            NoEscape(r'&=2 \times [(2\times' + min_end_dist + r' + (\frac{' + bolt_line + r'}{2}' + r'-1)  \times  ' + min_pitch + r'\\'))
        min_flange_plate_length_eqn.append(NoEscape(r'&= + \frac{' + gap + r'}{2}]\\ \\'))

        min_flange_plate_length_eqn.append(NoEscape(r'&=' + min_length + ' \end{aligned}'))
    return min_flange_plate_length_eqn

def min_plate_thk_req(t_w,multiplier=1.0):
    """
    Calculate min thickness of the fin plate
    Args:
        t_w:Web thickness in mm (float)
    Returns:
        min thickness of the fin plate
    """
    t_eff = str(round(multiplier * t_w,2))
    t_w = str(t_w)
    min_plate_thk_eqn = Math(inline=True)
    if multiplier == 1.0:
        min_plate_thk_eqn.append(NoEscape(r'\begin{aligned} t_w=' + t_w + '\end{aligned}'))
    else:
        multiplier = str(multiplier)
        min_plate_thk_eqn.append(NoEscape(r'\begin{aligned} t_w=' +multiplier+ r' \times '+ t_w + ' = '+t_eff+r'\end{aligned}'))
    return min_plate_thk_eqn


def vres_cap_bolt_check(V_u, A_u, bolt_capacity, bolt_req, multiple=1, conn=None):
    """
    Calculate no. of bolts required for flange and web
    Args:

         V_u:Shear force  in KN (float)
         A_u:Axial force  in KN (float)
         bolt_capacity:Bolt capacity  in KN (float)
         bolt_req:no. of bolts required (int)
         multiple:1
         conn:
    Returns:
         no. of bolts required (int)
    """

    res_force = math.sqrt(V_u ** 2 + A_u ** 2)
    trial_bolts = multiple * math.ceil(res_force / bolt_req)
    V_u = str(V_u)
    A_u = str(A_u)
    bolt_req = str(bolt_req)
    bolt_capacity = str(bolt_capacity)
    trial_bolts = str(trial_bolts)
    trial_bolts_eqn = Math(inline=True)

    if conn == "flange_web":
        trial_bolts_eqn.append(NoEscape(r' \begin{aligned} V_{res} &= \frac{2~\sqrt{V_u^2+A_u^2}} {bolts_{\text{req}}}\\'))
        trial_bolts_eqn.append(NoEscape(r' &= \frac{2 \times \sqrt{' + V_u + r'^2+' + A_u + r'^2}}{' + bolt_req + r'}\\'))
    else:
        trial_bolts_eqn.append(NoEscape(r' \begin{aligned} V_{res} &= \frac{\sqrt{V_u^2+A_u^2}} {bolt_{req}}\\'))
        trial_bolts_eqn.append(NoEscape(r' &= \frac{\sqrt{' + V_u + r'^2+' + A_u + r'^2}}{' + bolt_req + r'}\\'))
    trial_bolts_eqn.append(NoEscape(r'&=' + bolt_capacity + r'\end{aligned}'))
    return trial_bolts_eqn


def height_of_flange_cover_plate(B, sp, b_fp):  # weld
    """
    Calculate height of falnge cover plate
    Args:
        B:Width of  flange section in mm (float)
        sp: Spacing between flange plate in mm (float)
        b_fp: Height of flange cover plate in mm (float)
    Returns:
          Height of flange cover plate in mm (float)
    """
    B = str(B)
    sp = str(sp)
    b_fp = str(b_fp)
    height_for_flange_cover_plate_eqn = Math(inline=True)

    height_for_flange_cover_plate_eqn.append(NoEscape(r'\begin{aligned} B_{fp} &= {B - 2sp} \\'))
    height_for_flange_cover_plate_eqn.append(NoEscape(r'&= {' + B + r' - 2  \times  ' + sp + r'} \\'))

    height_for_flange_cover_plate_eqn.append(NoEscape(r'&=' + b_fp + r'\end{aligned}'))
    return height_for_flange_cover_plate_eqn


def height_of_web_cover_plate(D, sp, b_wp, T, R_1):  # weld
    """
    Calculate height of web cover plate
    Args:
        D: Depth of the section in mm (float)
        sp: Space between web plate in mm (float)
        b_wp: Height of web cover plate in mm (float)
        T: Thickness of flange in mm (float)
        R_1: Root radius in mm (float)
    Returns:
         Height of web cover plate in mm (float)
    """
    D = str(D)
    sp = str(sp)
    b_wp = str(b_wp)
    R_1 = str(R_1)
    T = str(T)
    height_for_web_cover_plate_eqn = Math(inline=True)

    height_for_web_cover_plate_eqn.append(NoEscape(r'\begin{aligned} W_{wp} &= {D-2T -2R1- 2sp} \\'))
    height_for_web_cover_plate_eqn.append(NoEscape(r'&= {' + D + r' - 2  \times  ' + T + r'- (2 \times' + R_1 + r')- 2 \times' + sp + r'} \\'))

    height_for_web_cover_plate_eqn.append(NoEscape(r'&=' + b_wp + '\end{aligned}'))
    return height_for_web_cover_plate_eqn


def inner_plate_height_weld(B, sp, t, r_1, b_ifp):  # weld
    """
    Calculate inner flange plate height for beam welded
    Args:

        B:Width of flange in mm (float)
        sp: Spacing between flange plate in mm (float)
        t: Web thickness in mm (float)
        r_1: Root radius in mm (float)
        b_ifp: Height of inner flange plate in mm (float)
    Returns:
         Height of inner flange plate in mm (float)
    """
    B = str(B)
    sp = str(sp)
    t = str(t)
    r_1 = str(r_1)
    b_ifp = str(b_ifp)
    inner_plate_height_weld_eqn = Math(inline=True)
    inner_plate_height_weld_eqn.append(NoEscape(r'\begin{aligned} B_{ifp} &= \frac{B - 4sp - t- 2R1}{2} \\'))
    inner_plate_height_weld_eqn.append(NoEscape(r'&= \frac{' + B + r'- 4\times' + sp + '-' + t + r'- 2\times' + r_1 + r'} {2} \\'))
    inner_plate_height_weld_eqn.append(NoEscape(r'&=' + b_ifp + '\end{aligned}'))
    return inner_plate_height_weld_eqn


def plate_Length_req(l_w, t_w, g, l_fp, conn=None):  # weld
    """
    Calculate minimum flange plate length
    Args:
       l_w: Weld length of flange in mm (float)
       t_w:Flange weld size in mm (float)
       g: Gap between flange plate in mm (float)
       l_fp: Minimum flange plate length in mm (float)
       conn: Flange or web (str)
    Returns:
          Minimum flange plate length  in mm (float)
    """
    l_w = str(l_w)
    t_w = str(t_w)
    g = str(g)
    l_fp = str(l_fp)
    min_plate_Length_eqn = Math(inline=True)
    if conn == "Flange":
        min_plate_Length_eqn.append(NoEscape(r'\begin{aligned} L_{fp} & = [2 \times(l_{w} + 2\times t_w) + g]\\'))
        min_plate_Length_eqn.append(NoEscape(r'&= [2\times(' + l_w + r'+2\times' + t_w + ') +' + g + r']\\'))
        min_plate_Length_eqn.append(NoEscape(r'&=' + l_fp + '\end{aligned}'))
    else:
        min_plate_Length_eqn.append(NoEscape(r'\begin{aligned} L_{wp} & = [2\times(l_{w} + 2\times t_w) + g]\\'))
        min_plate_Length_eqn.append(NoEscape(r'&= [2\times(' + l_w + r'+2\times' + t_w + ') +' + g + r']\\'))
        min_plate_Length_eqn.append(NoEscape(r'&=' + l_fp + '\end{aligned}'))

    return min_plate_Length_eqn


# TODO: DARSHAN, ANJALI (Tension rupture for welded is not required)
# def tension_rupture_welded_prov(w_p, t_p, fu,gamma_m1,T_dn,multiple =1):
#     """
#     Calculate design in tension as governed by rupture of net
#          cross-sectional area in case of welded connection
#     Args:
#          w_p: Width of given section in mm (float)
#          t_p: Thikness of given section in mm (float)
#          fu: Ultimate stress of material in N/mm square (float)
#          gamma_m1:Partial safety factor for failure at ultimate stress  (float)
#          T_dn: rupture strength of net cross-sectional area in N (float)
#          multiple: 1 (int)
#     Returns:
#           design in tension as governed by rupture of net cross-sectional area
#     Note:
#             Reference:
#             IS 800:2007,  cl 6.3
#
#
#     """
#     w_p = str(w_p)
#     t_p = str(t_p)
#     f_u = str(fu)
#     T_dn = str(T_dn)
#     gamma_m1 = str(gamma_m1)
#     multiple = str(multiple)
#     T_dn = str(T_dn)
#     gamma_m1 = str(gamma_m1)
#     Tensile_rup_eqnw = Math(inline=True)
#     Tensile_rup_eqnw.append(NoEscape(r'\begin{aligned} T_{\text{dn}} &= \frac{0.9 A_{n}~f_u}{\gamma_{m1}}\\'))
#     # Tensile_rup_eqnw.append(NoEscape(r'&=\frac{0.9\times'+w_p+'\times'+t_p+'\times'+f_u+'}{'+gamma_m1+r'}\\'))
#     Tensile_rup_eqnw.append(NoEscape(r'&=\frac{' + multiple + r'\times 0.9 \times' + w_p + r'\times' + t_p + r'\times' + f_u + '}{' + gamma_m1 + r'}\\'))
#     Tensile_rup_eqnw.append(NoEscape(r'&=' + T_dn +r'\\'))
#     Tensile_rup_eqnw.append(NoEscape(r'[Ref&.~IS~800:2007,~Cl.~6.3]\end{aligned}'))
#
#     return Tensile_rup_eqnw


def spacing(sp, t_w):
    """
    Calculate spacing
    Args:
        sp:Spacing required in mm (float)
        t_w:Size of weld in mm (float)
    Returns:
        Required spacing (float)
    """

    # sp = max(15,s+5)
    sp = str(sp)
    t_w = str(t_w)
    space_provided_eqn = Math(inline=True)
    space_provided_eqn.append(NoEscape(r'\begin{aligned} sp &= \text{max}(15,~(t_w+5))\\'))
    space_provided_eqn.append(NoEscape(r'&= \text{max} (15,~(' + t_w + r'+5))\\'))
    space_provided_eqn.append(NoEscape(r'&=' + sp + r'\end{aligned}'))
    return space_provided_eqn


# TODO: ANJALI, Keep only one of the following if possible
def weld_strength_req(V, A, M, Ip_w, y_max, x_max, l_w, R_w):
    # def weld_strength_stress(V_u, A_w, M_d, Ip_w, y_max, x_max, l_eff, R_w):

    """
    Calculate resultant stress on weld
    Args:
        V:Factored shear force acting on the member in KN (float)
        A:Vertical compression force carried by web of the section in KN (float)

        M:Moment devloped by ecentricity in KN/mm(float)
        Ip_w:Polar moment inertia of the web group in mm^4 (float)
        y_max:Vertical distance of farthest point in weld group from shear center of the weld group in mm (float)
        x_max:Horizontal distance of farthest point in weld group from shear center of the weld group in mm (float)

        l_w:Required effective web weld length in mm (float)
        R_w:Resultant stress on the weld in KN/mm (float)
    Returns:
         Resultant stress on the weld
    Note:
            Reference:
            Subramanyan (TODO: add page number)


    """

    V_wv = str(round(V / l_w, 2))
    A_wh = str(round(A / l_w, 2))

    V = str(V)
    A = str(A)
    l_w = str(l_w)
    R_w = str(R_w)

    if M > 0.0:
        T_wh = str(round(M * y_max / Ip_w, 2))
        T_wv = str(round(M * x_max / Ip_w, 2))
        y_max = str(y_max)
        x_max = str(x_max)
        Ip_w = str(Ip_w)
        M = str(M)

        weld_stress_eqn = Math(inline=True)
        weld_stress_eqn.append(NoEscape(r'\begin{aligned} R_{\text{w}} &=\sqrt{(T_{\text{wh}}+A_{\text{wh}})^2 + (T_{\text{wv}}+V_{\text{wv}})^2}\\ \\'))
        weld_stress_eqn.append(NoEscape(r'T_{\text{wh}}&=\frac{M\times y_{\text{max}}}{I_{pw}}=\frac{' + M + r'\times' + y_max + '}{' + Ip_w + r'}\\'))
        weld_stress_eqn.append(NoEscape(r'T_{\text{wv}}&=\frac{M\times x_{\text{max}}}{I_{pw}}=\frac{' + M + r'\times' + x_max + '}{' + Ip_w + r'}\\'))
        weld_stress_eqn.append(NoEscape(r'V_{\text{wv}}&=\frac{V}{l_w}=\frac{' + V + '}{' + l_w + r'}\\'))
        weld_stress_eqn.append(NoEscape(r'A_{\text{wh}}&=\frac{A}{l_w}=\frac{' + A + '}{' + l_w + r'}\\ \\'))
        weld_stress_eqn.append(NoEscape(r'R_{\text{w}}&=\sqrt{(' + T_wh + '+' + A_wh + r')^2 + (' + T_wv + '+' + V_wv + r')^2}\\ '))
        weld_stress_eqn.append(NoEscape(r'&=' + R_w + r'\end{aligned}'))
    else:
        weld_stress_eqn = Math(inline=True)
        weld_stress_eqn.append(NoEscape(r'\begin{aligned} R_{\text{w}}&=\sqrt{(A_{\text{wh}})^2 + (V_{\text{wv}})^2}\\ \\'))
        weld_stress_eqn.append(NoEscape(r'V_{\text{wv}}&=\frac{V}{l_w}=\frac{' + V + '}{' + l_w + r'}\\'))
        weld_stress_eqn.append(NoEscape(r'A_{\text{wh}}&=\frac{A}{l_w}=\frac{' + A + '}{' + l_w + r'}\\ \\'))
        weld_stress_eqn.append(NoEscape(r'R_{\text{w}}&=\sqrt{(' + A_wh + r')^2 + (' + V_wv + r')^2}\\'))
        weld_stress_eqn.append(NoEscape(r'&=' + R_w + r'\end{aligned}'))

    return weld_stress_eqn


def weld_strength_stress(V_u, A_w, M_d, Ip_w, y_max, x_max, l_eff, R_w):
    """
    Calculate resultant stress on weld
    Args:
          V_u:factored shear force acting on the member in KN (float)
          A_w:vertical compression force carried by web of the section in KN (float)
          M_d:moment devloped by ecentricity in KN/mm(float)
          Ip_w:moment devloped by ecentricity in KN/mm(float)
          y_max:moment devloped by ecentricity in KN/mm(float)
          x_max:horizontal distance of farthest point in weld group from shear center of the weld group in mm (float)
          l_eff:required effective web weld length in mm (float)
          R_w:resultant stress on the weld in KN/mm (float)
    Returns:
          resultant stress on the weld
    Note:
            Reference:
            Subramanyan (TODO: add page number)



    """
    T_wh = str(round(M_d * y_max / Ip_w, 2))
    T_wv = str(round(M_d * x_max / Ip_w, 2))
    V_wv = str(round(V_u / l_eff, 2))
    A_wh = str(round(A_w / l_eff, 2))

    V_u = str(V_u)
    A_w = str(A_w)
    M_d = str(M_d)
    Ip_w = str(Ip_w)
    y_max = str(y_max)
    x_max = str(x_max)
    l_eff = str(l_eff)
    R_w = str(R_w)
    weld_stress_eqn = Math(inline=True)
    weld_stress_eqn.append(NoEscape(r'\begin{aligned} R_{\text{w}}&=\sqrt{(T_{\text{wh}}+A_{\text{wh}})^2 + (T_{\text{wv}}+V_{\text{wv}})^2}\\ \\'))

    weld_stress_eqn.append(NoEscape(r'T_{\text{wh}}&=\frac{M_d\times y_{\text{max}}}{I{pw}}\\'))
    weld_stress_eqn.append(NoEscape(r'&=\frac{' + M_d + r'\times' + y_max + '}{' + Ip_w + r'}\\ \\'))

    weld_stress_eqn.append(NoEscape(r'T_{\text{wv}}&=\frac{M_d \times x_{\text{max}}}{I{pw}}\\'))
    weld_stress_eqn.append(NoEscape(r'&=\frac{' + M_d + r'\times' + x_max + '}{' + Ip_w + r'}\\ \\'))

    weld_stress_eqn.append(NoEscape(r'V_{\text{wv}}&=\frac{V_u}{ l_{_\text{eff}} }\\ '))
    weld_stress_eqn.append(NoEscape(r'&=\frac{' + V_u + '}{' + l_eff + r'}\\ \\'))

    weld_stress_eqn.append(NoEscape(r'A_{\text{wh}}&=\frac{A_u}{ l_{_\text{eff}} }\\'))
    weld_stress_eqn.append(NoEscape(r'&=\frac{' + A_w + '}{' + l_eff + r'}\\ \\'))

    weld_stress_eqn.append(NoEscape(r'R_{\text{w}}&=\sqrt{(' + T_wh + '+' + A_wh + r')^2 + (' + T_wv + '+' + V_wv + r')^2}\\'))
    weld_stress_eqn.append(NoEscape(r'&=' + R_w + r'\end{aligned}'))

    return weld_stress_eqn


# TODO: ANJALI Shear rupture check is not required for weld
def shear_Rupture_prov_weld(h, t, fu, v_dn, gamma_m1, multiple=1):  # weld

    """
      Calculate design strength in tension due to rupture of critical section in case of welded connection
      Args:
           h:Height of the flange in mm (float)
           t:Thickness of the flange in mm (float)
           fu:Ultimate stress of the material N/ mm square (float)
           v_dn:Design strength due to ruoture in N (float)
           gamma_m1:Partial safety factor for failure at ultimate stress (float)
           multiple:1
      Returns:
          design strength in tension due to rupture of critical section in case of welded connection

      Note:
                Reference:
                IS 800:2007,  cl 6.3

      """

    h = str(h)
    t = str(t)
    gamma_m1 = str(gamma_m1)
    f_u = str(fu)
    v_dn = str(v_dn)
    multiple = str(multiple)

    shear_rup_eqn = Math(inline=True)
    shear_rup_eqn.append(NoEscape(r'\begin{aligned} V_{dn} &= \frac{0.75\times A_{vn}~f_u}{\sqrt{3}~\gamma_{m1}}\\'))
    shear_rup_eqn.append(
        NoEscape(r'&=\frac{' + multiple + r'\times 0.75\times' + h + r'\times' + t + r'\times' + f_u + r'}{\sqrt{3}\times' + gamma_m1 + r'}\\'))
    shear_rup_eqn.append(NoEscape(r'&=' + v_dn + r'\\'))
    shear_rup_eqn.append(NoEscape(r'[Ref.&~IS~800:2007,~Cl.~6.3]\end{aligned}'))
    return shear_rup_eqn


def flange_weld_stress(F_f, l_eff, F_ws):
    """
    Calculate flange weld stress

    Args:

        F_f:flange force in KN (float)
        l_eff:available effective length in mm (float)
        F_ws:flange weld stress in N/mm (float)
    Returns:
        flange weld stress
    """
    F_f = str(F_f)
    l_eff = str(l_eff)
    F_ws = str(F_ws)
    flange_weld_stress_eqn = Math(inline=True)
    flange_weld_stress_eqn.append(NoEscape(r'\begin{aligned} \text{Stress} &= \frac{F_f\times10^3}{l_{\text{eff}}}\\'))
    flange_weld_stress_eqn.append(NoEscape(r' &= \frac{' + F_f + r'\times10^3}{' + l_eff + r'}\\'))
    flange_weld_stress_eqn.append(NoEscape(r'&= ' + F_ws + r'\end{aligned}'))

    return flange_weld_stress_eqn


def no_of_bolts_along_web(D, T_f, e, p, n_bw):
    """
    Calculate no. of bolts along web

    Args:
        D: section depth in mm  (float)
        T_f:flange thickness in mm  (float)
        e: end distance in mm  (float)
        p:pitch distance in mm  (float)
        n_bw: no. of bolts along web (int)
    Returns:
         no. of bolts along web
    """

    D = str(D)
    e = str(e)
    p = str(p)
    T_f = str(T_f)
    n_bw = str(n_bw)
    no_of_bolts_along_web = Math(inline=True)
    no_of_bolts_along_web.append(NoEscape(r'\begin{aligned} n_{bw} &= 2 \times ( \frac{D -(2\times T_f) -(2\times e)}{\ p}  + 1 )\\'))
    no_of_bolts_along_web.append(NoEscape(r'&= 2 \times (\frac{' + D + r' -(2\times' + T_f + r')-(2\times' + e + r')}{' + p + r'} +1 ) \\'))
    no_of_bolts_along_web.append(NoEscape(r'&= ' + n_bw + r'\end{aligned}'))
    return no_of_bolts_along_web


def no_of_bolts_along_flange(b, T_w, e, p, n_bf):
    """
    Calculate no of bolts along flange

    Args:
          b:flange width in mm  (float)
          T_w:web thickness in mm  (float)
          e: end distance in mm  (float)
          p: pitch distance in mm  (float)
          n_bf: no. of bolts along flange (int)
    Returns:
          no. of bolts along flange
    """
    b = str(b)
    e = str(e)
    p = str(p)
    T_w = str(T_w)
    n_bf = str(n_bf)
    no_of_bolts_along_flange = Math(inline=True)
    no_of_bolts_along_flange.append(NoEscape(r'\begin{aligned} n_{bf} &= 2 \times ( \frac{b/2 -(T_w / 2) -(2\times e)}{\ p}  + 1 )\\'))
    no_of_bolts_along_flange.append(NoEscape(r'&= 2 \times (\frac{' + b + r'/2 -(0.5\times' + T_w + r')-(2\times' + e + r')}{' + p + r'} +1 )\\'))
    no_of_bolts_along_flange.append(NoEscape(r'&= ' + n_bf + r'\end{aligned}'))
    return no_of_bolts_along_flange


def shear_force_in_bolts_near_web(V, n_wb, V_sb):
    """
    Calculate shear force in each bolts near web

    Args:
           V: factored shear load in KN (float)
           n_wb: no. of bolts in web (int)
           V_sb:shear force in each bolts near web in KN (float)
    Returns:
        shear force in bolts near web
    """
    V = str(V)
    n_wb = str(n_wb)
    V_sb = str(V_sb)
    shear_force_in_bolts_near_web = Math(inline=True)
    shear_force_in_bolts_near_web.append(NoEscape(r'\begin{aligned} V_{sb} &= \frac{V}{\ n_{wb}} \\'))
    shear_force_in_bolts_near_web.append(NoEscape(r'&=\frac{' + V + '}{' + n_wb + r'} \\'))
    shear_force_in_bolts_near_web.append(NoEscape(r'&= ' + V_sb + r'\end{aligned}'))
    return shear_force_in_bolts_near_web


def depth_req(e, g, row, sec=None):
    """
    Calculate depth required for web spacing check

    Args:
        e:edge distance for web plate in mm (float)
        g:gauge distance for web plate in mm (float)
        row: row (float)
        sec:coulmn or beam (str)
    Returns:
        depth required for web spacing check
    """

    d = 2 * e + (row - 1) * g
    depth = d
    depth = str(depth)
    e = str(e)
    g = str(g)
    row = str(row)

    depth_eqn = Math(inline=True)
    if sec == "C":
        depth_eqn.append(NoEscape(r'\begin{aligned} \text{depth} & = 2~e + (rl -1)~g \\'))
        depth_eqn.append(NoEscape(r'& = 2\times ' + e + '+(' + row + r'-1) \times' + g + r' \\'))
        depth_eqn.append(NoEscape(r'& = ' + depth + r'\end{aligned}'))
    elif sec == "column":
        depth_eqn.append(NoEscape(r'\begin{aligned} \text{depth} & = 2~e + (c_l -1)~g\\'))
        depth_eqn.append(NoEscape(r'& = 2 \times ' + e + '+(' + row + r'-1)\times' + g + r'\\'))
        depth_eqn.append(NoEscape(r'& = ' + depth + r'\end{aligned}'))
    elif sec == "beam":
        depth_eqn.append(NoEscape(r'\begin{aligned} \text{depth} & = 2~e + (r_l -1)~g\\'))
        depth_eqn.append(NoEscape(r'& = 2 \times ' + e + '+(' + row + r'-1)\times' + g + r'\\'))
        depth_eqn.append(NoEscape(r'& = ' + depth + r'\end{aligned}'))
    else:
        depth_eqn.append(NoEscape(r'\begin{aligned} \text{depth} & = 2~e + (r_l -1)~g\\'))
        depth_eqn.append(NoEscape(r'& = 2 \times ' + e + '+(' + row + r'-1)\times' + g + r'\\'))
        depth_eqn.append(NoEscape(r'& = ' + depth + r'\end{aligned}'))

    return depth_eqn


def end_plate_moment_demand(connectivity, g, T_w, R_r, t_w, s, T_e, M):
    ecc1 = round(g / 2 - t_w / 2 - s, 2)
    ecc2 = round(g / 2 - T_w / 2 - R_r, 2)
    ecc = max(ecc1, ecc2)
    T_e = str(T_e)
    M = str(M)
    ecc1 = str(ecc1)
    ecc2 = str(ecc2)
    ecc = str(ecc)

    EP_Mom = Math(inline=True)
    EP_Mom.append(NoEscape(r'\begin{aligned}M &= T_e \times \text{ecc} \\ \\'))
    if connectivity == VALUES_CONN_1[0]:
        EP_Mom.append(NoEscape(r'ecc_1 &=\frac{g}{2}-\frac{t_w}{2}-s &=' + ecc1 + r'\\'))
        EP_Mom.append(NoEscape(r'ecc_2 &=\frac{g}{2}-\frac{T_w}{2}-R_r &=' + ecc2 + r'\\'))
        EP_Mom.append(NoEscape(r'& \text{max} (ecc_1,~ecc_2) &=' + ecc + r'\\ \\'))
    else:
        EP_Mom.append(NoEscape(r'ecc &=\frac{g}{2}-\frac{t_w}{2}-s &=' + ecc1 + r'\\ \\'))
    EP_Mom.append(NoEscape(r'M&=' + T_e + r'\times' + ecc + r'\times10^{-3} &=' + M + r'\end{aligned}'))
    return EP_Mom


def gusset_ht_prov(beam_depth, clearance, height, mul=1):
    """
    Calculate gusset plate height
    Args:
         beam_depth:Section depth in mm (float)
         clearance:clearence between gusset plates in mm (float)
         height:Height of the gusset plate in mm (float)
         mul:
    Returns:
         gusset plate height
    """
    beam_depth = str(beam_depth)
    clearance = str(clearance)
    height = str(height)
    mul = str(mul)
    plate_ht_eqn = Math(inline=True)
    plate_ht_eqn.append(
        NoEscape(r'\begin{aligned} H &= ' + mul + r'\times \text{Depth + Clearance} 'r'\\'))
    plate_ht_eqn.append(
        NoEscape(r'&=(' + mul + r'\times' + beam_depth + ')+' + clearance + r'\\'))
    plate_ht_eqn.append(NoEscape(r'&= ' + height + r'\end{aligned}'))
    return plate_ht_eqn


def gusset_lt_b_prov(nc, p, e, length):
    """
    Calculate length of the gusset plate in case of bolted connection

    Args:

        nc:No. of row of bolts (int)
        p: pitch distance of the gusset plate in mm (float)
        e:Edge distance of the gusset plate in mm (float)
        length:length of the gusset plate in mm (float)
    Returns:
        length of the gusset plate in case of bolted connection
    """
    nc = str(nc)
    p = str(p)
    e = str(e)
    length = str(length)
    length_htb_eqn = Math(inline=True)
    length_htb_eqn.append(
        NoEscape(r'\begin{aligned} L &= (nc -1) p + 2  e\\'))
    length_htb_eqn.append(
        NoEscape(r'&= (' + nc + r'-1) \times' + p + r'+ (2 \times' + e + r')\\'))
    length_htb_eqn.append(NoEscape(r'&= ' + length + r'\end{aligned}'))
    return length_htb_eqn


def gusset_lt_w_prov(weld, cls, length):
    """
    Calculate length of the gusset plate in case of welded connection

    Args:
          weld:weld length in mm (float)
          cls:clearance in mm (float)
          length:plate length in mm (float)
    Returns:
        length of the gusset plate in case of welded connection

    """
    weld = str(weld)
    cls = str(cls)
    length = str(length)
    length_htw_eqn = Math(inline=True)
    length_htw_eqn.append(
        NoEscape(r'\begin{aligned} L &= \text{Flange weld + Clearance} 'r'\\'))
    length_htw_eqn.append(
        NoEscape(r'&= ' + weld + '+' + cls + r'\\'))
    length_htw_eqn.append(NoEscape(r'&= ' + length + r'\end{aligned}'))
    return length_htw_eqn


def bearing_length(V, t_w, t_f, r_r, f_y, gamma_m0, t, r_ra, gap):
    bearing_length = round((float(V) * 1000) * gamma_m0 / t_w / f_y, 3)
    b1_req = round(bearing_length - (t_f + r_r), 2)
    k = round(t_f + r_r, 2)
    b1 = round(max(b1_req, k), 2)
    b2 = round(max(b1 + gap - t - r_ra, 0.0), 2)

    b1_req = str(b1_req)
    k = str(k)
    b1 = str(b1)
    V = str(V)
    t_w = str(t_w)
    t_f = str(t_f)
    gamma_m0 = str(gamma_m0)
    r_r = str(r_r)
    b2 = str(b2)
    f_y = str(f_y)
    gap = str(gap)
    t = str(t)
    r_ra = str(r_ra)

    bearing_length = Math(inline=True)
    bearing_length.append(NoEscape(r'\begin{aligned} b_{l_{\text{req}}} &= \frac{V \gamma_m0}{t_w  f_y} - t_f - r_r \\'))
    bearing_length.append(NoEscape(r'&= \frac{' + V + r'\times' + gamma_m0 + '}{' + t_w + r'\times' + f_y + '} - ' + t_f + '-' + r_r + r' \\'))
    bearing_length.append(NoEscape(r'&=' + b1_req + r' \\ \\'))

    bearing_length.append(NoEscape(r'k &= t_f +r_r \\'))
    bearing_length.append(NoEscape(r'k &=' + t_f + '+' + r_r + '=' + k + r'\\ \\'))

    bearing_length.append(NoEscape(r'b_1&= \text{max} (b_{1_{\text{req}}},~k)=' + b1 + r'\\ \\'))

    bearing_length.append(NoEscape(r'b_2 &= b_1+\text{gap}-t-r_{r_{a}}\\'))
    bearing_length.append(NoEscape(r'b_2 &=' + b1 + '+' + gap + '-' + t + '-' + r_ra + r'\\'))
    bearing_length.append(NoEscape(r'b_2&= \text{max} (b_2,~0)=' + b2 + r'\end{aligned}'))
    return bearing_length

def moment_demand_SA(b_1, b_2, V, M):
    if b_2 == 0.0:
        ecc = 0.0
    elif b_2 <= b_1:
        ecc = round((b_2 / b_1) * (b_2 / 2), 2)
    else:
        ecc = round((b_2 - b_1 / 2), 2)

    V = str(V)
    b_1 = str(round(b_1,2))
    b_2 = str(round(b_2,2))
    M = str(M)
    ecc = str(ecc)

    moment_demand_eqn = Math(inline=True)
    moment_demand_eqn.append(NoEscape(r'\begin{aligned} M &= V \times ecc \\ \\'))
    if float(b_2) == 0.0:
        moment_demand_eqn.append(NoEscape(r'\text{if} ~b_2 = 0,~ &ecc = 0 \\'))
        moment_demand_eqn.append(NoEscape(r'M = 0 \\ \\'))
    elif float(b_2) <= float(b_1):
        moment_demand_eqn.append(NoEscape(r'\text{if}~b_2 \leq b_1, ~ecc &= \frac{b_2}{b_1}\times\frac{b_2}{2} \\'))
        moment_demand_eqn.append(NoEscape(r'ecc &=\frac{' + b_2 + '}{' + b_1 + r'}\times\frac{' + b_2 + r'}{2}\\'))
        moment_demand_eqn.append(NoEscape(r'&=' + ecc + r'\\ \\'))
    else:
        moment_demand_eqn.append(NoEscape(r'\text{if} ~b_2 > b_1, ~ecc &= \frac{b_2-b_1}{2} \\'))
        moment_demand_eqn.append(NoEscape(r'ecc &=\frac{' + b_2 + '-' + b_1 + r'}{2}\\'))
        moment_demand_eqn.append(NoEscape(r'&=' + ecc + r'\\ \\'))

    moment_demand_eqn.append(NoEscape(r'M &=' + V + r'\times' + ecc + r'\times10^{-3}\\'))
    moment_demand_eqn.append(NoEscape(r' &=' + M + r'\end{aligned}'))
    return moment_demand_eqn


def efficiency_prov(F, Td, eff):
    """
    Calculate efficiency of the tension member(provided)

    Args:
         F:axial force on the member in KN (float)
         Td:tension capacity of the section in KN (float)
         eff:efficiency of the tension member  (float)
    Returns:
        efficiency of the tension member
    """
    F = str(F)
    Td = str(round(Td / 1000, 2))
    eff = str(eff)
    eff_eqn = Math(inline=True)
    eff_eqn.append(NoEscape(r'\begin{aligned} \text{Utilization Ratio} &= \frac{F}{T_d}&=\frac{' + F + '}{' + Td + r'}\\'))
    eff_eqn.append(NoEscape(r'&= ' + eff + r'\end{aligned}'))

    return eff_eqn


def moment_cap(beta, m_d, f_y, gamma_m0, m_fd, mom_cap):
    """
     Calculate  moment capacity of the column when (class_of_section == 1 or self.class_of_section == 2)

     Args:
             beta: value according to the class of section
             m_d: bending moment acting on the column
             f_y: yield strength of material
             gamma_m0: partial safety factor
             m_fd:factored bending moment acting on the column
             mom_cap: moment capacity of the column
    Returns:
             moment capacity of the column
    """
    # todo reference
    beta = str(beta)
    m_d = str(m_d)
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)
    m_fd = str(m_fd)
    mom_cap = str(mom_cap)
    moment_cap = Math(inline=True)

    moment_cap.append(NoEscape(r'\begin{aligned} M_{c} &=  m_d - \beta(m_d -m_{fd})  \\'))
    moment_cap.append(NoEscape(r'&= ' + m_d + r'-' + beta + r'(' + m_d + r'-' + m_fd + r') \\'))
    moment_cap.append(NoEscape(r'&= ' + mom_cap + r'\end{aligned}'))
    return moment_cap


def eff_len_prov(l_eff, b_fp, t_w, l_w, con=None):
    """
    Calculate required flange length

    Args:
        l_eff:required flange length in mm (float)
        b_fp:flange plate height in mm (float)
        t_w:flange weld size in mm (float)
        l_w:flange weld length in mm (float)
        con:flange or web (str)
    Returns:
         required flange length
    """
    l_eff = str(l_eff)
    l_w = str(l_w)
    b_fp = str(b_fp)
    t_w = str(t_w)
    eff_len_eqn = Math(inline=True)
    if con == "Flange":
        eff_len_eqn.append(NoEscape(r'\begin{aligned} l_{\text{eff}} &= (2 l_w) + B_{fp} - 2 t_w\\'))
        eff_len_eqn.append(NoEscape(r'&= (2\times' + l_w + ') +' + b_fp + r' - 2\times' + t_w + r'\\'))
        eff_len_eqn.append(NoEscape(r'& = ' + l_eff + r'\end{aligned}'))
    else:
        eff_len_eqn.append(NoEscape(r'\begin{aligned} l_{\text{eff}} &= (2 l_w) + W_{wp} - 2 t_w\\'))
        eff_len_eqn.append(NoEscape(r'&= (2\times' + l_w + ') +' + b_fp + r' - 2\times' + t_w + r'\\'))
        eff_len_eqn.append(NoEscape(r'& = ' + l_eff + r'\end{aligned}'))

    return eff_len_eqn


def eff_len_prov_out_in(l_eff, b_fp, b_ifp, t_w, l_w):
    """
    Calculate effective length provided on outside

    Args:
           l_eff:required length of flange in mm (float)
           b_fp:flange plate height in mm (float)
           b_ifp:flange plate inner height in mm (float)
           t_w:flange weld size in mm (float)
           l_w:flange weld length in mm (float)
    Returns:
          effective length provided on outside
    """
    l_eff = str(l_eff)
    l_w = str(l_w)
    b_fp = str(b_fp)
    b_ifp = str(b_ifp)
    t_w = str(t_w)
    eff_len_prov_out_in_eqn = Math(inline=True)
    eff_len_prov_out_in_eqn.append(NoEscape(r'\begin{aligned} l_{eff} &= (6\times l_w) + B_{fp} + (2 \times B_{ifp})- 6\times t_w\\'))
    eff_len_prov_out_in_eqn.append(NoEscape(r'&= (6\times' + l_w + ') +' + b_fp + r'+ 2\times' + b_ifp + r'- 6\times' + t_w + r'\\'))
    eff_len_prov_out_in_eqn.append(NoEscape(r'& = ' + l_eff + r'\end{aligned}'))

    return eff_len_prov_out_in_eqn


def plate_area_req(crs_area, flange_web_area):
    """
    Calculate plate area required

    Args:
         crs_area:cross sectional area of plate in mm square (float)
         flange_web_area:combined area of flange and web in mm square (float)
    Returns:
         plate area required
     Note:
         [Ref: cl.8.6.3.2 IS 800:2007]
    """

    crs_area = str(crs_area)
    flange_web_area = str(flange_web_area)

    plate_crs_sec_area_eqn = Math(inline=True)
    plate_crs_sec_area_eqn.append(NoEscape(r'\begin{aligned} & \text{plate area} >= \\ & \text{1.05 X connected member area} \\'))
    # plate_crs_sec_area_eqn.append(NoEscape(r'& = '+crs_area+ r' * 1.05 \\'))
    plate_crs_sec_area_eqn.append(NoEscape(r' &= ' + flange_web_area + r'\\ \\'))
    plate_crs_sec_area_eqn.append(NoEscape(r' & [ \text{Ref: Cl.8.6.3.2, IS 800:2007}] \end{aligned}'))
    return plate_crs_sec_area_eqn


def width_pt_chk(B, t, r_1, pref):
    """
    Check the plate width

    Args:
          B:flange width in mm (float)
          t:web thickness in mm  (float)
          r_1:root radius in mm  (float)
          pref:"Outside" or "Outside +Inside" (str)
    Returns:
         the plate width
    """
    if pref == "Outside":
        outerwidth = round(B - (2 * 21), 2)
        outerwidth = str(outerwidth)
    else:
        innerwidth = round((B - t - (2 * r_1) - (4 * 21)) / 2, 2)
        innerwidth = str(innerwidth)

    B = str(B)
    t = str(t)
    r_1 = str(r_1)
    Innerwidth_pt_chk_eqn = Math(inline=True)
    if pref == "Outside":
        Innerwidth_pt_chk_eqn.append(NoEscape(r'\begin{aligned} B_{fp} &= B-(2 \times 21)\\'))
        Innerwidth_pt_chk_eqn.append(NoEscape(r'&=' + B + r'-(2 \times 21)\\'))
        Innerwidth_pt_chk_eqn.append(NoEscape(r'&= ' + outerwidth + r'\end{aligned}'))
    else:
        Innerwidth_pt_chk_eqn.append(NoEscape(r'\begin{aligned} B_{ifp} &= \frac{B-t-(2 \times R1)-(4 \times 21)}{2}\\'))
        Innerwidth_pt_chk_eqn.append(NoEscape(r'&=\frac{' + B + '-' + t + r'-(2 \times' + r_1 + r')-(4 \times 21)}{2}\\'))
        Innerwidth_pt_chk_eqn.append(NoEscape(r'&= ' + innerwidth + r'\end{aligned}'))
    return Innerwidth_pt_chk_eqn


def width_pt_chk_bolted(B, t, r_1):
    """
    Check the width of plate (bolted connection)

    Args:
           B:flange width
           t:web thickness
           r_1:root radius
    Returns:
          width of plate
    """
    innerwidth = round((B - t - (2 * r_1)) / 2, 2)
    B = str(B)
    t = str(t)
    r_1 = str(r_1)
    innerwidth = str(innerwidth)
    width_pt_chk_bolted_eqn = Math(inline=True)

    width_pt_chk_bolted_eqn.append(NoEscape(r'\begin{aligned} B_{fp} &= \frac{B-t-(2 \times R1)}{2}\\'))
    width_pt_chk_bolted_eqn.append(NoEscape(r'&=\frac{' + B + '-' + t + r'-(2 \times' + r_1 + r')}{2}\\'))
    width_pt_chk_bolted_eqn.append(NoEscape(r'&= ' + innerwidth + r'\end{aligned}'))
    return width_pt_chk_bolted_eqn


def web_width_chk_bolt(pref, D, tk, T, R_1, webplatewidth, webclearance=None):
    """
    Calculate web plate width

    Args:
          pref:prefference (outside or outside+inside) (str)
          D:Section depth in mm (float)
          tk:flange plate thickness (provided) in mm (float)
          T:flange thickness in mm (float)
          R_1: root radius in mm (float)
          webplatewidth: web width in mm (float)
          webclearance: web clearance in mm (float)
    Returns:
          web plate width
    """
    T = str(T)
    tk = str(tk)
    R_1 = str(R_1)
    webplatewidth = str(webplatewidth)
    webclearance = str(webclearance)
    web_width_chk_bolt_eqn = Math(inline=True)
    if pref == "Outside":
        D = str(D)
        web_width_chk_bolt_eqn.append(NoEscape(r'\begin{aligned} W_{wp} &= D - (2 \times T) - (2 \times R1)\\'))
        web_width_chk_bolt_eqn.append(NoEscape(r' &= ' + D + r' - (2 \times' + T + r') - (2 \times' + R_1 + r')\\'))
        web_width_chk_bolt_eqn.append(NoEscape(r' &=' + webplatewidth + r'\end{aligned}'))
    else:

        if D > 600.00:
            web_width_chk_bolt_eqn.append(NoEscape(r'\begin{aligned} C~~ &= max((R1, t_{ifp}) + 25) \\'))
            web_width_chk_bolt_eqn.append(NoEscape(r'&= max((' + R_1 + ',' + tk + r') + 25) \\'))
            web_width_chk_bolt_eqn.append(NoEscape(r'&= ' + webclearance + r' \\'))

        else:
            web_width_chk_bolt_eqn.append(NoEscape(r'\begin{aligned} C~~ &= max((R1, t_{ifp}) + 10) \\'))
            web_width_chk_bolt_eqn.append(NoEscape(r'&= max((' + R_1 + ',' + tk + r') +10) \\'))
            web_width_chk_bolt_eqn.append(NoEscape(r'&= ' + webclearance + r' \\'))
        D = str(D)
        web_width_chk_bolt_eqn.append(NoEscape(r' W_{wp} &= D - (2 \times T) - (2 \times C)\\'))
        web_width_chk_bolt_eqn.append(NoEscape(r' &= ' + D + r' - (2 \times ' + T + r') - (2 \times' + webclearance + r')\\'))
        web_width_chk_bolt_eqn.append(NoEscape(r' &=' + webplatewidth + r'\end{aligned}'))

    return web_width_chk_bolt_eqn


def web_width_chk_weld(D, tk, R_1, webplatewidth):
    """
    Calculate web plate height in case of beam_beam welded connection

     Args:
         D:Section depth in mm (float)
         tk:flange thickness in mm (float)
         R_1:root radius of the section in mm (float)
         webplatewidth:web plate height in mm (float)
    Returns:
         web plate height
    """
    tk = str(tk)
    R_1 = str(R_1)
    D = str(D)
    webplatewidth = str(webplatewidth)
    web_width_chk_weld_eqn = Math(inline=True)
    web_width_chk_weld_eqn.append(NoEscape(r'\begin{aligned} W_{wp} &= D - (2 \times T) - (2 \times R1)- (2\times21)\\'))
    web_width_chk_weld_eqn.append(NoEscape(r' &= ' + D + r' - (2 \times ' + tk + r') - (2 \times' + R_1 + r')- (2\times21)\\'))
    web_width_chk_weld_eqn.append(NoEscape(r' &=' + webplatewidth + r'\end{aligned}'))
    return web_width_chk_weld_eqn

def width_req_sptng_seated(edge,t_w,r_r,bolt_col,gauge,width_req_sptng):
    e = str(edge)
    r_r = str(r_r)
    t_w = str(t_w)
    n_c = str(bolt_col)
    g = str(gauge)
    width_req_sptng = str(width_req_sptng)
    width_req_sptng_seated_eqn = Math(inline=True)
    width_req_sptng_seated_eqn.append(
        NoEscape(r'\begin{aligned}4 \times e\textquotesingle &+ t_w + 2 \times r_r + \Big(\frac{n_{c}}{2} - 1 \Big) \times g\\'))
    width_req_sptng_seated_eqn.append(NoEscape(
        r'&= 4 \times' + e + '+' + t_w + '+' + r'2 \times' + r_r + r' + \Big(\frac{' + n_c + r'}{2} - 1 \Big) \times' + g + r'\\'))
    width_req_sptng_seated_eqn.append(NoEscape(r'&=' + width_req_sptng + r'\\ \end{aligned}'))
    return width_req_sptng_seated_eqn

def width_req_sptd_seated(edge_dist,t_w,r_r,width_req_sptd):
    e = str(edge_dist)
    r_r = str(r_r)
    t_w = str(t_w)
    width_req_sptd = str(width_req_sptd)
    width_req_sptd_seated_eqn = Math(inline=True)
    width_req_sptd_seated_eqn.append(NoEscape(r'\begin{aligned}4 \times e\textquotesingle& + t_w + 2 \times r_r \\'))
    width_req_sptd_seated_eqn.append(NoEscape(r'&= 4 \times' + e + '+' + t_w + '+' + r'2 \times' + r_r + r'\\'))
    width_req_sptd_seated_eqn.append(NoEscape(r'&=' + width_req_sptd + r'\\ \end{aligned}'))
    return width_req_sptd_seated_eqn

def length_req_sptng_seated(end_dist,n_r,pitch,t,r_r,length_req_spting):
    e = str(end_dist)
    r_r = str(r_r)
    t = str(t)
    n_r = str(n_r)
    p = str(pitch)
    length_req_spting = str(length_req_spting)
    length_req_eqn = Math(inline=True)
    length_req_eqn.append(NoEscape(r'\begin{aligned}2 \times e\textquotesingle &+ t + r_{ra} + (n_r - 1) \times p \\'))
    length_req_eqn.append(NoEscape(r'&= 2 \times' + e + '+' + t + '+' + r_r + r'+(' + n_r +r'- 1) \times' + p + r'\\'))
    length_req_eqn.append(NoEscape(r'&=' + length_req_spting + r'\\ \end{aligned}'))
    return length_req_eqn

def min_plate_ht_req(D, r_r, t_f, min_req_width):
    """
    Calculate minimum web plate height

    Args:
         D:Section depth in mm (float)
         min_req_width:minimum web plate height in mm (float)
    Returns:
         minimum web plate height
     Note:
           [Ref: INSDAG - Chapter 5, Sect. 5.2.3]
    """

    beam_depth = str(D)
    r_r = str(r_r)
    t_f = str(t_f)
    min_plate_ht = str(round(min_req_width, 2))
    web_width_min_eqn = Math(inline=True)
    web_width_min_eqn.append(NoEscape(r'\begin{aligned} & 0.6 \times (d_b - 2 \times t_f - 2 \times r_r)\\'))
    web_width_min_eqn.append(
        NoEscape(r'&= 0.6 \times (' + beam_depth + r'- 2 \times' + t_f + r'- 2 \times' + r_r + r')\\'))
    web_width_min_eqn.append(NoEscape(r'&=' + min_plate_ht + r'\\ \\'))
    web_width_min_eqn.append(NoEscape(r'& [\text{Ref. INSDAG, Ch.5, sec.5.2.3}] \end{aligned}'))
    return web_width_min_eqn


def flange_plate_area_prov(B, pref, y, outerwidth, fp_area, t, r_1, innerwidth=None):
    """
    Calculate flange plate area

    Args:
         B:Width of the section in mm (float)
         pref:Outside or OUtside +inside (str)
         y:flange thickness in mm (float)
         outerwidth:over width in mm (float)
         fp_area:flange plate area in mm square (float)
         t:web thickness in mm (float)
         r_1:root radius in mm (float)
         innerwidth:Innerwidth in mm (float)
    Returns:
         flange plate area
    """

    outerwidth = str(outerwidth)
    B = str(B)
    fp_area = str(fp_area)
    t = str(t)
    r_1 = str(r_1)
    innerwidth = str(innerwidth)
    y = str(y)
    flangeplate_crs_sec_area_eqn = Math(inline=True)

    if pref == "Outside":
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'\begin{aligned} B_{fp} &= B - (2 \times 21)\\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'&= ' + B + r' - (2 \times 21)\\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'&= ' + outerwidth + r' \\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r' pt.area &= ' + y + r' \times' + outerwidth + r'\\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'&= ' + fp_area + r'\end{aligned}'))
    else:
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'\begin{aligned} B_{fp} &= B-(2 \times 21)\\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'&=' + B + r'-(2 \times 21)\\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'&= ' + outerwidth + r' \\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'B_{ifp}&= \frac{B-t-(2 \times R1)-(4 \times 21)}{2}\\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'&=\frac{' + B + '-' + t + r'-(2 \times ' + r_1 + r')-(4 \times 21)}{2}\\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'&= ' + innerwidth + r' \\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r' pt.area &=(' + outerwidth + r'+(2 \times' + innerwidth + r')) \times' + y + r'\\'))
        flangeplate_crs_sec_area_eqn.append(NoEscape(r'&= ' + fp_area + r'\end{aligned}'))

    return flangeplate_crs_sec_area_eqn


def plate_recheck_area_weld(outerwidth, innerwidth=None, f_tp=None, t_wp=None, conn=None, pref=None):
    """
    Re-check plate area

    Args:
          flange_plate_area: area of the flange plate in mm square (float)
          web_plate_area:area of the web plate in mm square (float)
          outerwidth: flange plate height in mm  (float)
          innerwidth: flange plate Innerheight  in mm  (float)
          f_tp: flange plate thickness provided  in mm  (float)
          t_wp:None
          conn:"flange" or "web" (str)
          pref: "Outside+Inside" or "outside" (str)
    Returns:
          plate area
    """

    if conn == "flange":
        if pref == "Outside":
            flange_plate_area = (outerwidth * f_tp)

        else:
            flange_plate_area = (outerwidth + (2 * innerwidth)) * f_tp
            # flange_plate_area = str(flange_plate_area)
    else:
        web_plate_area = (2 * outerwidth * t_wp)
        # web_plate_area = str(web_plate_area)
    outerwidth = str(outerwidth)
    innerwidth = str(innerwidth)
    f_tp = str(f_tp)
    t_wp = str(t_wp)
    # flange_plate_area  = str(flange_plate_area)
    # web_plate_area  = str(web_plate_area)
    plate_recheck_area_weld_eqn = Math(inline=True)
    if conn == "flange":
        if pref == "Outside":
            flange_plate_area = str(flange_plate_area)
            plate_recheck_area_weld_eqn.append(NoEscape(r'\begin{aligned}  \text{plate area} &=B_{fp} \times t_{ifp}\\'))
            plate_recheck_area_weld_eqn.append(NoEscape(r' &=' + outerwidth + r'\times' + f_tp + r'\\'))
            plate_recheck_area_weld_eqn.append(NoEscape(r'&= ' + flange_plate_area + r'\end{aligned}'))
        else:
            flange_plate_area = str(flange_plate_area)
            plate_recheck_area_weld_eqn.append(NoEscape(r'\begin{aligned}  \text{plate area} &=(B_{fp} +(2\times B_{ifp}))\times  t_{ifp}  \\'))
            plate_recheck_area_weld_eqn.append(NoEscape(r' &=(' + outerwidth + r'+(2\times' + innerwidth + r'))\times' + f_tp + r'\\'))
            plate_recheck_area_weld_eqn.append(NoEscape(r'&= ' + flange_plate_area + r'\end{aligned}'))
    else:
        web_plate_area = str(web_plate_area)
        plate_recheck_area_weld_eqn.append(NoEscape(r'\begin{aligned}  \text{plate area} &=2\times W_{wp} \times t_{wp}  \\'))
        plate_recheck_area_weld_eqn.append(NoEscape(r' &=2\times' + outerwidth + r' \times' + t_wp + r'\\'))
        plate_recheck_area_weld_eqn.append(NoEscape(r'&= ' + web_plate_area + r'\end{aligned}'))
    return plate_recheck_area_weld_eqn


def flange_plate_area_prov_bolt(B, pref, y, outerwidth, fp_area, t, r_1, innerwidth=None):
    """
     Calculate the flange plate area for column-column bolted connection

     Args:

          B:flange width of the section in mm (float)
          pref:outside or (outside +inside) (string)
          y: web thickness in mm (float)
          outerwidth: outerwidth of flange width in mm (float)
          fp_area:area of flange plate in mm square (float)
          t: flange thickness in mm (float)
          r_1:root radius of the section in mm (float)
          innerwidth:innerwidth of flange plate in mm (float)
     Returns:
          flange plate area
    """
    outerwidth = str(outerwidth)
    B = str(B)
    fp_area = str(fp_area)
    t = str(t)
    r_1 = str(r_1)
    innerwidth = str(innerwidth)
    y = str(y)
    flangeplate_crs_sec_area_bolt_eqn = Math(inline=True)
    if pref == "Outside":

        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'\begin{aligned} B_{fp} &= B\\'))
        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'&= ' + outerwidth + r'\\'))

        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r' pt.area &= ' + y + r' \times ' + outerwidth + r'\\'))
        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'&= ' + fp_area + r'\end{aligned}'))
    else:

        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'\begin{aligned} B_{fp} &= B\\'))
        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'&= ' + outerwidth + r' \\'))
        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'B_{ifp} &= \frac{B-t-(2 \times R1)}{2}\\'))
        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'&=\frac{' + B + '-' + t + r'-(2 \times' + r_1 + r')}{2}\\'))
        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'&= ' + innerwidth + r' \\'))
        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r' pt.area &=(' + outerwidth + r'+(2 \times' + innerwidth + r')) \times' + y + r'\\'))
        flangeplate_crs_sec_area_bolt_eqn.append(NoEscape(r'&= ' + fp_area + r'\end{aligned}'))

    return flangeplate_crs_sec_area_bolt_eqn


def web_plate_area_prov(D, y, webwidth, wp_area, T, r_1):
    """
    Calculate   area of provided plate for web in case of welded connection

    Args:
           D:section depth in mm (float)
           y:thickness of web in mm (float)
           webwidth:width of web section  in mm (float)
           wp_area:  area of provided plate for web in mm square (float)
           T: flange thickness  in mm (float)
           r_1:  section root radius in mm (float)

    Returns:
          area of provided plate for web
    """
    D = str(D)
    T = str(T)
    r_1 = str(r_1)
    webwidth = str(webwidth)
    wp_area = str(wp_area)
    y = str(y)

    web_plate_area_prov = Math(inline=True)
    # web_plate_area_prov.append(NoEscape(r'\begin{aligned} W_{wp}&= D-(2*T)-(2*R1)-(2*21)\\'))
    # web_plate_area_prov.append(NoEscape(r'&='+D+'-(2\times'+T+')-(2\times'+r_1+r')-(2*21)\\'))
    # web_plate_area_prov.append(NoEscape(r'&= ' + webwidth + r' \\'))
    web_plate_area_prov.append(NoEscape(r'\begin{aligned} pt.area &= t_{wp} \times 2 \times W_{wp}\\'))
    web_plate_area_prov.append(NoEscape(r'  &= ' + y + r'\times 2 \times ' + webwidth + r'\\'))
    web_plate_area_prov.append(NoEscape(r'&= ' + wp_area + r'\end{aligned}'))
    return web_plate_area_prov


def web_plate_area_prov_bolt(D, y, webwidth, wp_area, T, r_1):
    """
    Calculate   area of provided plate for web

    Args:
          D:section depth in mm (float)
          y:thickness of web in mm (float)
          webwidth:width of web section  in mm (float)
          wp_area:  area of provided plate for web in mm square (float)
          T: flange thickness  in mm (float)
          r_1: root radius in mm (float)
    Returns:
         area of provided plate for web
    """
    D = str(D)
    T = str(T)
    r_1 = str(r_1)
    webwidth = str(webwidth)
    wp_area = str(wp_area)
    y = str(y)

    web_plate_area_prov = Math(inline=True)
    # web_plate_area_prov.append(NoEscape( W_{wp}&= D-(2*T)-(2*R1)\\'))
    # web_plate_area_prov.append(NoEscape(r'&=' + D + '-(2\times' + T + ')-(2\times' + r_1 + r')\\'))
    # web_plate_area_prov.append(NoEscape(r'&= ' + webwidth + r' \\'))
    web_plate_area_prov.append(NoEscape(r'\begin{aligned}pt.area &= t_{wp} \times 2 \times  W_{wp} \\'))
    web_plate_area_prov.append(NoEscape(r'&= ' + y + r'\times 2 \times' + webwidth + r'\\'))
    web_plate_area_prov.append(NoEscape(r'&= ' + wp_area + r'\end{aligned}'))
    return web_plate_area_prov

def seated_width_req(width_req):
    width_req = str(width_req)
    seated_width_req = Math(inline=True)
    seated_width_req.append(NoEscape(r'\begin{aligned}4 \times e\textquotesingle+ 2 \times R_1 + t = ' + str(width_req)
                                         +r'\end{aligned}'))
    return seated_width_req

def seated_width_prov(width_prov):
    width_prov = str(width_prov)
    seated_width_prov = Math(inline=True)
    seated_width_prov.append(NoEscape(r'\begin{aligned}B = ' + str(width_prov)
                                         +r'\end{aligned}'))
    return seated_width_prov

def min_angle_leg_length_bearing(b1,gap):
    min_leg = str(round(b1+gap,2))
    b1 = str(b1)
    gap = str(gap)
    leg_req_bearing = Math(inline=True)
    leg_req_bearing.append(NoEscape(r'\begin{aligned}b_1 + \text{gap} = ' + min_leg + r'\end{aligned}'))
    return leg_req_bearing

# functions for base plate


def square_washer_size(side):
    """ equation for the size of square plate washer """
    side = str(side)

    washer_dim = Math(inline=True)
    washer_dim.append(NoEscape(r'\begin{aligned} & \text{Square} - ' + side + r'  X ' + side + r' \\ \\'))
    washer_dim.append(NoEscape(r'& [\text{Ref. IS 6649:1985, Table 2}] \end{aligned}'))

    return washer_dim


def square_washer_thk(thickness):
    """ equation for the thickness of square plate washer """
    thickness = str(thickness)

    washer_thk = Math(inline=True)
    washer_thk.append(NoEscape(r'\begin{aligned} t_{w} &= ' + thickness + r' \\ \\'))
    washer_thk.append(NoEscape(r'&[\text{Ref. IS 6649:1985, Table 2}] \end{aligned}'))

    return washer_thk


def square_washer_in_dia(dia):
    """ equation for the hole diameter of square plate washer """
    dia = str(dia)

    washer_in_dia = Math(inline=True)
    washer_in_dia.append(NoEscape(r'\begin{aligned} d_{h} &= ' + dia + r' \\ \\'))
    washer_in_dia.append(NoEscape(r'&[\text{Ref. IS 6649:1985, Table 2}] \end{aligned}'))

    return washer_in_dia


def hexagon_nut_thickness(nut_thick):
    """ equation for the thickness of the hexagon nut """
    nut_thick = str(nut_thick)

    nut_thickness = Math(inline=True)
    nut_thickness.append(NoEscape(r'\begin{aligned} t_{n} &= ' + nut_thick + r' \\ \\'))
    nut_thickness.append(NoEscape(r'&[\text{Ref. IS 1364-3:2002, Table 1}] \end{aligned}'))

    return nut_thickness


def anchor_len_above_footing(length):
    """ equation for the length of the anchor bolt above footing """
    length = str(length)

    anchor_len = Math(inline=True)
    anchor_len.append(NoEscape(r'\begin{aligned} grout thickness + thickness of base plate + thickness of plate washer +nut thickness + 20 \\'))
    anchor_len.append(NoEscape(r' &= ' + length + r' \end{aligned}'))

    return anchor_len


def bp_length(col_depth, end_distance, pitch_distance, length, bolt_column):
    """ equation for the min length of the base plate"""
    col_depth = str(col_depth)
    end_distance = str(end_distance)
    pitch_distance = str(pitch_distance)
    length = str(length)

    bp_length_min = Math(inline=True)
    if bolt_column == 1:
        bp_length_min.append(NoEscape(r'\begin{aligned} L &= D ~+~2 ~ (e~+~e) \\'))
        bp_length_min.append(NoEscape(r'   &= ' + col_depth + r' ~+~2 \times (' + end_distance + r'~+~' + end_distance + r') \\'))
    else:
        bp_length_min.append(NoEscape(r'\begin{aligned} L &= D ~+~2 ~ (e~+~e) ~+~2~p \\'))
        bp_length_min.append(NoEscape(r'   &= ' + col_depth + r' ~+~2 \times (' + end_distance + r'~+~' + end_distance + r') + 2 \times '
                                      + pitch_distance + r' \\'))
    bp_length_min.append(NoEscape(r'   &= ' + length + r' \\ \\'))
    bp_length_min.append(NoEscape(r'&[\text{Ref. based on detailing requirement}] \end{aligned}'))

    return bp_length_min


def bp_length_sb(col_depth, end_distance, length, projection, col_type=''):
    """ equation for the min length of the welded slab base/base plate for hollow/tubular sections"""
    col_depth = str(col_depth)
    end_distance = str(end_distance)
    length = str(length)
    projection = str(projection)

    bp_length_min = Math(inline=True)
    if col_type == 'CHS':
        bp_length_min.append(NoEscape(r'\begin{aligned} L &= OD ~+~2~(c~+~e) \\'))
    else:
        bp_length_min.append(NoEscape(r'\begin{aligned} L &= D ~+~2~(c~+~e) \\'))
    bp_length_min.append(NoEscape(r'   &= ' + col_depth + r' ~+~2 \times ~(' + projection + r'~+~' + end_distance + r') \\'))
    bp_length_min.append(NoEscape(r'   &= ' + length + r' \\ \\'))
    bp_length_min.append(NoEscape(r'&[\text{Ref. based on detailing requirement}] \end{aligned}'))

    return bp_length_min


def bp_width_case1(load_axial, bp_min_len, bearing_strength, bp_width, min_req_width):
    """ """
    load_axial = str(load_axial * 10 ** -3)
    bp_min_len = str(bp_min_len)
    bearing_strength = str(bearing_strength)
    bp_width = str(bp_width)

    bp_length_min = Math(inline=True)
    bp_length_min.append(NoEscape(r'\begin{aligned} W &= \frac{2P_{u}} {\sigma_{\text{br}} ~ L} \\'))
    bp_length_min.append(
        NoEscape(r'   &= \frac{2 \times ' + load_axial + r' \times 10^{3}} {' + bearing_strength + r' \times ' + bp_min_len + r'} \\'))
    bp_length_min.append(NoEscape(r'   &= ' + str(min_req_width) + r' \\'))
    bp_length_min.append(NoEscape(r'   &= ' + bp_width + r' \end{aligned}'))

    return bp_length_min


def bp_width(flange_width, edge_distance, width, designation, projection, bp_type='welded_moment_bp', mom_bp_case='None'):
    """ equation for the min length of the base plate"""
    flange_width = str(flange_width)
    edge_distance = str(edge_distance)
    width = str(width)

    bp_width_min = Math(inline=True)

    if bp_type == 'welded_moment_bp':
        if mom_bp_case == 'Case1':
            bp_width_min.append(NoEscape(r'\begin{aligned} W &= (0.85 B) ~+~2~(e\textquotesingle ~+~e\textquotesingle) \\'))
            bp_width_min.append(NoEscape(r'    &= (0.85 \times' + flange_width + r') ~+~2 \times (' + edge_distance + r'~+~' + edge_distance + r') \\'))
        else:
            bp_width_min.append(NoEscape(r'\begin{aligned} W &= (0.85 B) ~+~2 ~(e\textquotesingle ~+~e\textquotesingle) \\'))
            bp_width_min.append(NoEscape(r'    &= (0.85 \times ' + flange_width + r') ~+~2 \times (' + edge_distance + r'~+~' + edge_distance + r') \\'))
    else:
        if designation[1:4] == 'CHS':
            bp_width_min.append(NoEscape(r'\begin{aligned} W &= OD ~+~2~ (c~+~e\textquotesingle) \\'))
            bp_width_min.append(NoEscape(r' &= ' + flange_width + r' ~+~2 \times (' + str(projection) + r'~+~' + edge_distance + r') \\'))
        else:
            bp_width_min.append(NoEscape(r'\begin{aligned} W &= B ~+~2~ (c~+~e\textquotesingle) \\'))
            bp_width_min.append(NoEscape(r' &= ' + flange_width + r' ~+~2 \times (' + str(projection) + r'~+~' + edge_distance + r') \\'))

    bp_width_min.append(NoEscape(r'    &= ' + width + r' \\ \\'))
    bp_width_min.append(NoEscape(r'&[\text{Ref. based on detailing requirement}] \end{aligned}'))

    return bp_width_min


def bearing_strength_concrete(concrete_grade, bearing_strength_value):
    """ equation for the bearing strength of concrete"""
    concrete_grade = str(concrete_grade)
    bearing_strength_value = str(bearing_strength_value)

    bearing_strength = Math(inline=True)
    bearing_strength.append(NoEscape(r'\begin{aligned} \sigma_{\text{br}} &= 0.45 f_{ck} \\'))
    bearing_strength.append(NoEscape(r' &= 0.45 \times ' + concrete_grade + r' \\'))
    bearing_strength.append(NoEscape(r' &= ' + bearing_strength_value + r' \\ \\'))
    bearing_strength.append(NoEscape(r' &[\text{Ref. IS 456:2000, Cl.34.4}] \end{aligned}'))

    return bearing_strength


def actual_bearing_pressure(axial_load, bp_area_provided, bearing_pressure):
    """ """
    axial_load = str(axial_load * 10 ** -3)
    bp_area_provided = str(round(bp_area_provided * 10 ** -3, 2))
    bearing_pressure = str(round(bearing_pressure, 2))

    bp_bearing_pressure = Math(inline=True)
    bp_bearing_pressure.append(NoEscape(r'\begin{aligned} {\sigma_{\text{br}}}_{\text{actual}} &= \frac{P_{u}}{A_{\text{provided}}} \\'))
    bp_bearing_pressure.append(
        NoEscape(r'                        &= \frac{' + axial_load + r'\times 10^{3}}{' + bp_area_provided + r'\times 10^{3}} \\'))
    bp_bearing_pressure.append(NoEscape(r'                        &= ' + bearing_pressure + r' \end{aligned}'))

    return bp_bearing_pressure


def bp_allowable_thk(connecting_thk1, connecting_thk2, maximum_thk):
    """ """
    connecting_thk1 = str(connecting_thk1)
    connecting_thk2 = str(connecting_thk2)
    maximum_thk = str(maximum_thk)

    thk_allowable = Math(inline=True)
    thk_allowable.append(NoEscape(r'\begin{aligned} (T, ~t) &< t_p \leq ' + maximum_thk + r' \\'))
    thk_allowable.append(NoEscape(r' (' + connecting_thk1 + r', ~' + connecting_thk2 + r') &< t_p \leq ' + maximum_thk + r' \end{aligned}'))

    return thk_allowable


def bp_thk_1(plate_thk, plate_thk_provided, projection, actual_bearing_stress, gamma_m0, fy_plate):
    """ """
    plate_thk = str(plate_thk)
    plate_thk_provided = str(plate_thk_provided)
    projection = str(projection)
    actual_bearing_stress = str(round(actual_bearing_stress, 2))
    gamma_m0 = str(gamma_m0)
    fy_plate = str(fy_plate)

    thk = Math(inline=True)
    thk.append(NoEscape(r'\begin{aligned} t_p &= c~\Bigg[\frac{2.5~{\sigma_{\text{br}}}_{\text{actual}}~\gamma_{m0}}{ {f_{y}}_{\text{plate}} }\Bigg]^{0.5} \\'))
    thk.append(NoEscape(r'      &= ' + projection + r' \times \Bigg[\frac{2.5~\times ' + actual_bearing_stress + r'\times ~' + gamma_m0 + r' }{'
                        + fy_plate + r'}\Bigg]^{0.5} \\'))
    thk.append(NoEscape(r'     &= ' + plate_thk + r' \\ '))
    thk.append(NoEscape(r'     &= ' + plate_thk_provided + r' \\ \\'))
    thk.append(NoEscape(r' & [\text{Ref. IS 800:2007, Cl.7.4.3.1}] \end{aligned}'))

    return thk


def minimum_load(action_load, zp_column, fy_column, gamma_m0, axis='major'):
    """ calculate eccentricity along the major axis"""
    action_load = str(round(action_load, 2))
    zp_column = str(round(zp_column, 2))
    fy_column = str(fy_column)
    gamma_m0 = str(gamma_m0)

    load = Math(inline=True)
    if axis == 'major':
        load.append(NoEscape(r'\begin{aligned} M_{zz} &= 0.5 \times M_{d} \\'))
        load.append(NoEscape(r'        &= 0.5 \times \beta_{b} Z_{pz} f_y / \gamma_{m0} \\'))
    else:
        load.append(NoEscape(r'\begin{aligned} M_{yy} &= 0.5 \times M_{d} \\'))
        load.append(NoEscape(r'        &= 0.5 \times \beta_{b} Z_{py} f_y / \gamma_{m0} \\'))

    load.append(NoEscape(r'        &= 0.5 \times 1 \times ' + zp_column + r'\times 10^{3} \times ' + fy_column + r'~ /~ ' + gamma_m0 + r' \\'))
    load.append(NoEscape(r'        &= ' + action_load + r' \\'))
    load.append(NoEscape(r' & [Ref.~IS~800:2007,~Cl.8.2.1.2] \end{aligned}'))

    return load


def eccentricity(moment, axial_load, eccentricity_zz):
    """ calculate eccentricity along the major axis"""
    moment = str(moment)
    axial_load = str(axial_load)
    eccentricity_zz = str(round(eccentricity_zz, 2))

    ecc_zz = Math(inline=True)
    ecc_zz.append(NoEscape(r'\begin{aligned} e_{\text{zz}} &= \frac{{M_{u}}_{\text{z}}}{P_{u}} \\'))
    ecc_zz.append(NoEscape(r'        &= \frac{' + moment + r'\times 10^{6}}{' + axial_load + r'\times 10^{3}} \\'))
    ecc_zz.append(NoEscape(r'        &= ' + eccentricity_zz + r' \end{aligned}'))

    return ecc_zz


def k1(ecc_zz, bp_length, k1_value):
    """ calculate k1

    Args:
        ecc_zz (e) - end distance in mm (float)
        bp_length (L) - length of the base plate in mm (float)
        k1_value - value of k1 (float)

    Returns:
        k1 [k1 = 3 * (e - L/2)] (float)
    """
    ecc_zz = str(ecc_zz)
    bp_length = str(bp_length)
    k1_value = str(round(k1_value, 2))

    k1 = Math(inline=True)
    k1.append(NoEscape(r'\begin{aligned} k_{1} &= 3~\Big(e_{\text{zz}} ~-~\frac{L}{2}\Big) \\'))
    k1.append(NoEscape(r'       &= 3~\Big(' + ecc_zz + r'~-~\frac{' + bp_length + r'}{2}\Big) \\'))
    k1.append(NoEscape(r'       &= ' + k1_value + r' \\ \\'))
    k1.append(NoEscape(r'& [\text{Ref. Design of Welded Structures,} \\ '))
    k1.append(NoEscape(r'& \text{Omer W Blodgett, section 3.3.}] \end{aligned}'))

    return k1


def modular_ratio(E_s, f_ck, modular_ratio):
    """ calculate modular ratio

    """
    E_s = str(E_s)
    E_c = round((5000 * math.sqrt(f_ck)), 3)
    E_c = str(E_c)
    f_ck = str(f_ck)
    modular_ratio = str(modular_ratio)

    n = Math(inline=True)
    n.append(NoEscape(r'\begin{aligned} E_s &= 2 \times 10 ^ {5}~(\text{N/mm}^{2}) \\'))
    n.append(NoEscape(r' E_c &= 5000~\sqrt{f_{ck}}~(\text{N/mm}^{2}) \\'))
    n.append(NoEscape(r' &= 5000~\times \sqrt{' + f_ck + r'}~=~' + E_c + r' \\ \\'))
    n.append(NoEscape(r' n &= \frac{E_{s}}{E_{c}} \\'))
    n.append(NoEscape(r' n &= \frac{' + E_s + r'}{' + E_c + r'} \\'))
    n.append(NoEscape(r' &=  ' + modular_ratio + r'\\ \\'))
    n.append(NoEscape(r' &[\text{Ref. IS 800:2007, IS 456:2000}] \end{aligned}'))
    # n.append(NoEscape(r' & [Ref.~Design~of~Welded~Structures~- \\'))
    # n.append(NoEscape(r' & Omer~W~Blodgett~(section~3.3)] \end{aligned}'))

    return n


def epsilon(yield_stress, epsilon_value):
    """ """
    yield_stress = str(yield_stress)
    epsilon_value = str(epsilon_value)

    value = Math(inline=True)
    value.append(NoEscape(r'\begin{aligned} \epsilon_{\text{st}} &= \sqrt{\frac{250}{ {f_{y}}_{\text{st}} }} \\'))
    value.append(NoEscape(r'&= \sqrt{\frac{250}{' + yield_stress + r'}} \\'))
    value.append(NoEscape(r'&= ' + epsilon_value + r' \\ \\'))
    value.append(NoEscape(r'& [\text{Ref. IS 800:2007, Table2}] \end{aligned}'))

    return value


def total_anchor_area_tension(anchor_dia, anchor_nos_tension, anchor_area_tension):
    """

    """
    anchor_dia = str(anchor_dia)
    anchor_nos_tension = str(anchor_nos_tension)
    anchor_area_tension = str(anchor_area_tension)

    total_anchor_area = Math(inline=True)
    total_anchor_area.append(NoEscape(r'\begin{aligned} A_{s} &= n \times~\Big(\frac{\pi}{4}\Big)~d^{2} \\'))
    total_anchor_area.append(NoEscape(r'&       = ' + anchor_nos_tension + r' \times~\Big(\frac{\pi}{4}\Big)~ \times'
                                      + anchor_dia + r'^{2} \\'))
    total_anchor_area.append(NoEscape(r'& = ' + anchor_area_tension + r'\end{aligned}'))

    return total_anchor_area


def calc_f(end_distance, bp_length, f):
    """

    """
    end_distance = str(end_distance)
    bp_length = str(bp_length)
    f = str(f)

    dist_f = Math(inline=True)
    dist_f.append(NoEscape(r'\begin{aligned} f &= \Big(\frac{L}{2} - e\Big) \\'))
    dist_f.append(NoEscape(r'&   = \Big(\frac{' + bp_length + r'}{2} - ' + end_distance + r'\Big) \\'))
    dist_f.append(NoEscape(r'&   = ' + f + r' \\ \\'))
    dist_f.append(NoEscape(r'& [\text{Ref. Design of Welded Structures,} \\ '))
    dist_f.append(NoEscape(r'& \text{Omer W Blodgett, section 3.3}] \end{aligned}'))

    return dist_f


def k2(n, anchor_area_tension, bp_width, f, e, k2_value):
    """ calculate k2

    Args:
        n - modular ratio (float)
        anchor_area_tension (A_s) - total area of the anchor hold down bolts under tension (float)
        bp_width (B) - width of the base plate in mm (float)
        f = distance between the centre of the base plate and the centre of the anchor bolt(s) under tension (float)
        e = eccentricity (float)
        k2_value (float)

    Returns:
        k2 [k2 = (6*n*A_s / W) * (f + e) ] (float)
    """
    n = str(n)
    anchor_area_tension = str(anchor_area_tension)
    bp_width = str(bp_width)
    f = str(f)
    e = str(e)
    k2_value = str(round(k2_value, 2))

    k2 = Math(inline=True)
    k2.append(NoEscape(r'\begin{aligned} k_2 &= \frac{6~n~A_s}{W}~\Big(f~+~e_{\text{zz}}\Big) \\'))
    k2.append(
        NoEscape(r'&     = \frac{6~ \times' + n + r'~\times' + anchor_area_tension + r'}{' + bp_width + r'}~\times \Big(' + f + r'~+~' + e + r'\Big) \\'))
    k2.append(NoEscape(r'&     = ' + k2_value + r' \\ \\'))

    k2.append(NoEscape(r'& \text{Note: } n \text{ is the modular ratio.} \\ \\ '))
    k2.append(NoEscape(r'& [\text{Ref. Design of Welded Structures,} \\ '))
    k2.append(NoEscape(r'& \text{Omer W Blodgett, section 3.3}] \end{aligned}'))

    return k2


def k3(k2_value, bp_length, f, k3_value):
    """ calculate k3 """
    k2_value = str(round(k2_value, 2))
    bp_length = str(bp_length)
    f = str(f)
    k3_value = str(round(k3_value, 2))

    k3 = Math(inline=True)
    k3.append(NoEscape(r'\begin{aligned} k_3 &= - ~k_2~\Big(\frac{L}{2}~+~f\Big) \\'))
    k3.append(NoEscape(r'&     = - ~' + k2_value + r'~\Big(\frac{' + bp_length + r'}{2}~+~' + f + r'\Big) \\'))
    k3.append(NoEscape(r'&     = ' + k3_value + r' \\ \\'))
    k3.append(NoEscape(r'& [\text{Ref. Design of Welded Structures,} \\ '))
    k3.append(NoEscape(r'& \text{Omer W Blodgett, section 3.3}] \end{aligned}'))

    return k3


def y(k1_value, k2_value, k3_value, y_value):
    """ calculate the distance (y) of the base plate under compression"""
    k1_value = round(k1_value, 2)
    if k1_value > 0:
        k1_value = '+ ' + str(k1_value)
    else:
        k1_value = str(k1_value)

    k2_value = round(k2_value, 2)
    if k2_value > 0:
        k2_value = '+ ' + str(k2_value)
    else:
        k2_value = str(k2_value)

    k3_value = round(k3_value, 2)
    if k3_value > 0:
        k3_value = '+ ' + str(k3_value)
    else:
        k3_value = str(k3_value)

    y_value = str(y_value)

    y = Math(inline=True)
    y.append(NoEscape(r'\begin{aligned} & y^{3}~+~k_{1}~y^{2}~+~k_{2}~y~+~k_{3} = 0 \\'))
    y.append(NoEscape(r' & y^{3}~' + k1_value + r'\times y^{2}~' + k2_value + r'\times y~' + k3_value + r' = 0 \\'))
    y.append(NoEscape(r'& y = ' + y_value + r' \\ \\'))
    y.append(NoEscape(r'& [\text{Ref. Design of Welded Structures,} \\ '))
    y.append(NoEscape(r'& \text{Omer W Blodgett, section 3.3}] \end{aligned}'))

    return y


def tension_demand_anchor(axial_load, bp_length, dist_y, ecc_zz, f, anchor_tension):
    """ calculate total tension demand on the hold down bolt(s)"""
    axial_load = str(axial_load)
    bp_length = str(bp_length)
    dist_y = str(dist_y)
    ecc_zz = str(ecc_zz)
    f = str(f)
    anchor_tension = str(anchor_tension)

    tension_total = Math(inline=True)
    tension_total.append(NoEscape(r'\begin{aligned} P_t &= -~P_{u}~\Bigg[\frac{\frac{L}{2}-\frac{y}{3}-e_{\text{zz}}}{\frac{L}{2}-\frac{y}{3}+f}\Bigg] \\'))
    tension_total.append(
        NoEscape(r'&     = -~' + axial_load + r'\times ~\Bigg[\frac{\frac{' + bp_length + r'}{2}-\frac{' + dist_y + r'}{3}-' + ecc_zz + r'}'
                                                                                                                                        r'{\frac{' + bp_length + r'}{2}-\frac{' + dist_y + r'}{3}+' + f + r'}\Bigg] \\'))
    tension_total.append(NoEscape(r'&     = ' + anchor_tension + r' \\ \\'))
    tension_total.append(NoEscape(r'& [\text{Ref. Design of Welded Structures,} \\ '))
    tension_total.append(NoEscape(r'& \text{Omer W Blodgett, section 3.3}] \end{aligned}'))

    return tension_total


def tension_demand_each_anchor(total_tension_demand, anchor_nos, tension_each_anchor):
    """ """
    total_tension_demand = str(total_tension_demand)
    anchor_nos = str(anchor_nos)
    tension_each_anchor = str(tension_each_anchor)

    tension_total = Math(inline=True)
    tension_total.append(NoEscape(r'\begin{aligned} T_{d} = \frac{P_{t}}{n} \\'))
    tension_total.append(NoEscape(r'&       = \frac{' + total_tension_demand + r'}{' + anchor_nos + r'} \\'))
    tension_total.append(NoEscape(r'&       = ' + tension_each_anchor + r'\end{aligned}'))

    return tension_total


def eff_bearing_area(col_depth, col_flange_width, col_flange_thk, col_web_thk, col_type='I-section'):
    """ calculate min area req for base plate (only for axial loads)"""
    col_depth = str(col_depth)
    col_flange_width = str(col_flange_width)
    col_flange_thk = str(col_flange_thk)
    col_web_thk = str(col_web_thk)

    area = Math(inline=True)

    if col_type == 'I-section':
        area.append(NoEscape(r'\begin{aligned} {A_{\text{br}}}_{\text{eff}} &= (D~+~2 c) (B~+~2 c) - \Big[ \big(D - 2(T~+~c)\big) \big(B - t\big) \Big] \\ \\'))
        area.append(NoEscape(r'&                = (' + col_depth + r' ~+~2 c) (' + col_flange_width + r' ~+~2 c)~ - \\'))
        area.append(NoEscape(r'& \Big[ \big(' + col_depth + r' - 2 \times (' + col_flange_thk + r'~+~c)\big) \big(' + col_flange_width + r' - '
                                                                                                                                 r'' + col_web_thk + r'\big) \Big] \\ \\'))
    if col_type == 'SHS&RHS':
        area.append(NoEscape(r'\begin{aligned} {A_{\text{br}}}_{\text{eff}} &= (D~+~2 c) (B~+~2 c) \\ \\'))
        area.append(NoEscape(r'&                = (' + col_depth + r' ~+~2 c) (' + col_flange_width + r' ~+~2 c) \\ '))
    if col_type == 'CHS':
        area.append(NoEscape(r'\begin{aligned} {A_{\text{br}}}_{\text{eff}} &= \frac{\pi}{4} \times (OD~+~2 c)^{2} \\ '))
        area.append(NoEscape(r'&                = \frac{\pi}{4} \times (' + col_depth + r' ~+~2 c)^{2} \\ \\'))

    area.append(NoEscape(r'& \text{Note: } c \text{ is the projection beyond the face of the column.} \\ \\'))
    area.append(NoEscape(r'& [\text{Reference: Design of Steel Structures,} \\'))
    area.append(NoEscape(r'& \text{ by N.Subramanian, (2019 edition)}] \end{aligned} '))

    return area


def eff_projection(col_depth, col_flange_width, col_flange_thk, col_web_thk, min_area, projection, end_distance, col_type='I-section'):
    """ calculate min area req for base plate (only for axial loads)"""
    col_depth = str(col_depth)
    col_flange_width = str(col_flange_width)
    col_flange_thk = str(col_flange_thk)
    col_web_thk = str(col_web_thk)
    min_area = str(round(min_area * 10 ** -3, 2))
    projection_val = max(projection, end_distance)
    projection_val = str(projection_val)
    projection = str(round(projection, 2))
    end_distance = str(end_distance)

    c = Math(inline=True)
    c.append(NoEscape(r'\begin{aligned} {A_{\text{br}}}_{\text{eff}} &= {A_{\text{req}}}_{\text{min}} \\'))
    c.append(NoEscape(r'&                = ' + min_area + r' \times 10^{3} \\ \\'))

    if col_type == 'I-section':
        c.append(NoEscape(r' \text{Therefore},&~(' + col_depth + r' ~+~2 c) (' + col_flange_width + r' ~+~2 c)~- \\'))
        c.append(NoEscape(r'& \Big[ \big(' + col_depth + r' - 2(' + col_flange_thk +
                          r'~+~c)\big) \big(' + col_flange_width + r' - ' + col_web_thk + r'\big) \Big] \\ '))
        c.append(NoEscape(r'& = ' + min_area + r' \times 10^{3} \\ '))

    if col_type == 'SHS&RHS':
        c.append(NoEscape(r' \text{Therefore},&~(' + col_depth + r' ~+~2 c) (' + col_flange_width + r' ~+~2 c)~ =~ ' + min_area + r' \times 10^{3} \\'))

    if col_type == 'CHS':
        c.append(NoEscape(r'\text{Therefore},&~ \frac{\pi}{4} \times (' + col_depth + r'~+~2 c)^{2}~=~ ' + min_area + r' \times 10^{3} \\'))

    c.append(NoEscape(r'              c &  = ' + projection + r' \\ \\'))

    c.append(NoEscape(r' \text{projection} &= \text{ max(c, e)} \\'))
    c.append(NoEscape(r'            &= \max(' + projection + r',~' + end_distance + r') \\'))
    c.append(NoEscape(r'&            = ' + projection_val + r' \\ \\'))

    c.append(NoEscape(r'& [\text{Reference: Design of Steel Structures,} \\'))
    c.append(NoEscape(r'& \text{by N.Subramanian, (2019 edition)}] \end{aligned} '))

    return c


def min_area_req(axial_load, bearing_strength, bp_min_area):
    """ calculate min area req for base plate (only for axial loads)"""
    axial_load = str(axial_load * 10 ** -3)
    bearing_strength = str(bearing_strength)
    bp_min_area = str(round(bp_min_area * 10 ** -3, 2))

    area = Math(inline=True)
    area.append(NoEscape(r'\begin{aligned} {A_{\text{req}}}_{\text{min}} &= \frac{P_{u}}{\sigma_{\text{br}}} \\'))
    area.append(NoEscape(r'&                 = \frac{' + axial_load + r' \times 10^{3}}{' + bearing_strength + r'} \\'))
    area.append(NoEscape(r'&        = ' + bp_min_area + r'\times 10^{3} \end{aligned}'))

    return area


def min_area_provided(bp_area_provided, bp_len, bp_w):
    """ area provided for base plate (only for axial loads)"""
    bp_len = str(bp_len)
    bp_w = str(bp_w)
    bp_area_provided = str(round(bp_area_provided * 10 ** -3, 2))

    area_prov = Math(inline=True)
    area_prov.append(NoEscape(r'\begin{aligned} A_{\text{provided}} &= L \times W \\'))
    area_prov.append(NoEscape(r'  &= ' + bp_len + r' \times ' + bp_w + r' \\'))
    area_prov.append(NoEscape(r' &= ' + bp_area_provided + r'\times 10^{3} \end{aligned}'))

    return area_prov


def mom_bp_case(case, eccentricity, bp_length):
    """ """
    case = str(case)
    eccentricity = str(round(eccentricity, 2))

    bp_case = Math(inline=True)

    if case == 'Case1':
        bp_length = round(bp_length, 2)
        value = round(bp_length / 6, 2)
        value = str(value)
        bp_length = str(bp_length)

        bp_case.append(NoEscape(r'\begin{aligned} e_{\text{zz}} & \leq \frac{L_{\text{min}}}{6} \\'))
        bp_case.append(NoEscape(r' ' + eccentricity + r' & \leq \frac{' + bp_length + r'}{6} \\'))
        bp_case.append(NoEscape(r' ' + eccentricity + r' & \leq ' + value + r' \end{aligned}'))
    elif case == 'Case2':
        bp_length = round(bp_length, 2)
        value1 = round(bp_length / 6, 2)
        value2 = round(bp_length / 3, 2)
        value1 = str(value1)
        value2 = str(value2)
        bp_length = str(bp_length)

        bp_case.append(NoEscape(r'\begin{aligned} \frac{L_{\text{min}}}{6} & < e_{\text{zz}} < \frac{L_{\text{min}}}{3} \\'))
        bp_case.append(NoEscape(r' \frac{' + bp_length + r'}{6} & < ' + eccentricity + r' < \frac{' + bp_length + r'}{3} \\'))
        bp_case.append(NoEscape(r' ' + value1 + r' & < ' + eccentricity + r' < ' + value2 + r'\end{aligned}'))

    elif case == 'Case3':
        bp_length = round(bp_length, 2)
        value = round(bp_length / 3, 2)
        value = str(value)
        bp_length = str(bp_length)

        bp_case.append(NoEscape(r'\begin{aligned} e_{\text{zz}} & \geq \frac{L_{\text{min}}}{3} \\'))
        bp_case.append(NoEscape(r' ' + eccentricity + r' & \geq \frac{' + bp_length + r'}{3} \\'))
        bp_case.append(NoEscape(r' ' + eccentricity + r' & \geq ' + value + r'\end{aligned}'))

    return bp_case


def bp_section_modulus(bp_length, bp_width, section_modulus):
    """ """
    bp_length = str(bp_length)
    bp_width = str(bp_width)
    section_modulus = str(round(section_modulus * 10 ** -3, 2))

    ze_zz = Math(inline=True)
    ze_zz.append(NoEscape(r'\begin{aligned} {z_{e}}_{\text{plate}} &= \frac{W L^{2}}{6} \\'))
    ze_zz.append(NoEscape(r'&                 = \frac{' + bp_width + r' \times ' + bp_length + r'^{2}}{6} \\'))
    ze_zz.append(NoEscape(r'&                 = ' + section_modulus + r'\times 10^{3} \end{aligned}'))

    return ze_zz


def bending_stress(axial_load, moment_major, bp_length, bp_width, bp_area, section_modulus, sigma_max, sigma_min):
    """ """
    axial_load = str(axial_load)
    moment_major = str(round(moment_major, 2))
    bp_length = str(bp_length)
    bp_width = str(bp_width)
    bp_area = str(round(bp_area, 2))
    section_modulus = str(round(section_modulus * 10 ** -3, 2))
    sigma_max = str(round(sigma_max, 2))
    sigma_min = str(round(sigma_min, 2))

    sigma = Math(inline=True)
    sigma.append(NoEscape(r'\begin{aligned} {\sigma_{b}}_{max} &= \frac{P_{u}}{A}~+~\frac{ {M_{u}}_{\text{z}} }{{z_{e}}_{\text{plate}}} \\'))
    sigma.append(NoEscape(r'&                    = \frac{' + axial_load + r' \times 10^{3}}{' + bp_length + r' \times '
                          + bp_width + r'}~+~'r'\frac{' + moment_major + r' \times 10^{6}}{' + section_modulus + r' \times 10^{3}} \\'))

    sigma.append(NoEscape(r'&            = \frac{' + axial_load + r'\times 10^{3}}{' + bp_area + r'}~+~\frac{' + moment_major + r' \times 10^{6}}{' +
                          section_modulus + r' \times 10^{3}} \\'))
    sigma.append(NoEscape(r'&                 = ' + sigma_max + r' \\ \\'))

    sigma.append(NoEscape(r' {\sigma_{b}}_{min} &= \frac{P_{u}}{A}~-~\frac{{M_{u}}_{\text{z}}}{{z_{e}}_{\text{plate}}} \\'))
    sigma.append(NoEscape(r'&                    = \frac{' + axial_load + r' \times 10^{3}}{' + bp_length + r' \times '
                          + bp_width + r'}~-~' r'\frac{' + moment_major + r' \times 10^{6}}{' + section_modulus + r' \times 10^{3}} \\'))
    sigma.append(NoEscape(r'&         = \frac{' + axial_load + r'\times 10^{3}}{' + bp_area + r'}~-~\frac{' + moment_major + r' \times 10^{6}}{' +
                          section_modulus + r' \times 10^{3}} \\'))
    sigma.append(NoEscape(r'&                 = ' + sigma_min + r'\end{aligned}'))

    return sigma


def critical_section(bp_length, col_depth, critical_len):
    """ """
    bp_length = str(bp_length)
    col_depth = str(col_depth)
    critical_len = str(critical_len)

    length = Math(inline=True)
    length.append(NoEscape(r'\begin{aligned} y_{\text{critical}} &= \frac{L ~- ~(0.95D)}{2} \\'))
    length.append(NoEscape(r'&              = \frac{' + bp_length + r' ~- ~(0.95 \times ' + col_depth + r')}{2} \\'))
    length.append(NoEscape(r'&              = ' + critical_len + r'\end{aligned}'))

    return length


def critical_section_case_2_3(critical_xx, y, bp_length, column_D):
    """ """
    critical_len = Math(inline=True)

    critical_len.append(NoEscape(r'\begin{aligned} y_{\text{critical}} &= \frac{L - 0.95D}{2} \\'))
    critical_len.append(NoEscape(r'                             &= \frac{' + str(bp_length) + r' - (0.95 \times ' + str(column_D) + r')}{2} \\'))
    critical_len.append(NoEscape(r'                             &= ' + str(critical_xx) + r' \\ \\'))

    if y > critical_xx:
        critical_xx = str(critical_xx)
        y = str(y)
        critical_len.append(NoEscape(r' y~ &> ~y_{\text{critical}}~~~ (' + y + r'~ > ~' + critical_xx + r') \\'))
        critical_len.append(NoEscape(r'& \text{Therefore},~ y_{\text{critical}} = ' + critical_xx + r'\\ \\'))
    else:
        critical_xx = str(critical_xx)
        y = str(y)
        critical_len.append(NoEscape(r' y~ &< ~y_{\text{critical}}~~~ (' + y + r'~ < ~' + critical_xx + r') \\'))
        critical_len.append(NoEscape(r' \text{Therefore},&~ y_{\text{critical}} = ' + y + r'\\ \\'))

    critical_len.append(NoEscape(r' & \text{Note: The critical section lies at } 0.95D \\'))
    critical_len.append(NoEscape(r' & \text{of the column section.} \end{aligned}'))

    return critical_len


def bending_stress_critical_sec(bending_stress_critical):
    """ """
    bending_stress_critical = str(round(bending_stress_critical, 2))

    stress = Math(inline=True)
    stress.append(NoEscape(r'\begin{aligned} {\sigma_{b}}_{critical} = ' + bending_stress_critical + r'\end{aligned}'))

    return stress


def moment_critical_section(sigma_x, sigma_max, critical_len, moment, concrete_bearing_stress, bp_width, case='Case1'):
    """ """
    sigma_x = str(round(sigma_x, 2))
    sigma_max = str(round(sigma_max, 2))
    critical_len = str(critical_len)
    concrete_bearing_stress = str(concrete_bearing_stress)
    bp_width = str(bp_width)

    critical_moment = Math(inline=True)

    if case == 'Case1':
        moment = str(round(moment * 10 ** -6, 2))
        critical_moment.append(NoEscape(r'\begin{aligned} M_{\text{critical}} &= \Bigg[ \bigg( {\sigma_{b}}_{critical} \times y_{\text{critical}} \times '
                                        r'\frac{y_{\text{critical}}} {2} \bigg)~ + \\ '))
        critical_moment.append(NoEscape(r' & \bigg( \frac{1}{2} \times y_{\text{critical}} \times '
                                        r'\big({\sigma_{b}}_{max} - {\sigma_{b}}_{critical} \big) \times \\'))
        critical_moment.append(NoEscape(r' & \frac{2}{3} \times y_{\text{critical}} \bigg) \Bigg] \times W \\ \\'))

        critical_moment.append(NoEscape(r' &= \Bigg[ \bigg( ' + sigma_x + r' \times ' + critical_len + r' \times '
                                        r'\frac{' + critical_len + r'} {2} \bigg)~ + \\ '))
        critical_moment.append(NoEscape(r' & \bigg( \frac{1}{2} \times ' + critical_len + r' \times '
                                        r'\big(' + sigma_max + r' - ' + sigma_x + r' \big) \times \\'))
        critical_moment.append(NoEscape(r' & \frac{2}{3} \times ' + critical_len + r' \bigg) \Bigg] \times ' + bp_width + r' \\ \\'))

        critical_moment.append(NoEscape(r'&              = ' + moment + r'\times 10 ^ {6} \end{aligned}'))
    else:
        moment = str(round(moment * 10 ** -6, 2))
        critical_moment.append(
            NoEscape(r'\begin{aligned} {M_{\text{critical}}}_{1} &= 0.45f_{ck} W y_{\text{critical}}\times\bigg(\frac{y_{\text{critical}}}{2}\bigg) \\'))
        critical_moment.append(NoEscape(r'  &= 0.45 \times ' + concrete_bearing_stress + r'\times' + bp_width + r'\times'
                                        + critical_len + r'\times\bigg(\frac{' + critical_len + r'}{2}\bigg) \\'))
        critical_moment.append(NoEscape(r'&                    = ' + moment + r'\times 10 ^ {6} \end{aligned}'))

    return critical_moment


def lever_arm_tension(bp_len, column_D, column_T, end_distance, lever_arm):
    """ """
    bp_len = str(bp_len)
    column_D = str(column_D)
    column_T = str(column_T)
    end_distance = str(end_distance)
    lever_arm = str(round(lever_arm, 2))

    dist = Math(inline=True)
    dist.append(NoEscape(r'\begin{aligned} l &= \frac{L}{2}-\frac{D}{2}+\frac{T}{2}-e \\'))
    dist.append(NoEscape(r'&   = \frac{' + bp_len + r'}{2}-\frac{' + column_D + r'}{2}+\frac{' + column_T + r'}{2}-'
                         + end_distance + r' \\'))
    dist.append(NoEscape(r'&  = ' + lever_arm + r'\end{aligned}'))

    return dist


def lever_arm_moment(tension_demand, lever_arm, moment):
    """ """
    tension_demand = str(round(tension_demand, 2))
    lever_arm = str(round(lever_arm, 2))

    moment_critical = Math(inline=True)
    moment_critical.append(NoEscape(r'\begin{aligned} {M_{\text{critical}}}_{2} &= P_{t}~l \\'))
    moment_critical.append(NoEscape(r'&   = ' + tension_demand + r'\times 1000 \times ' + lever_arm + r' \\'))
    if moment <= 1e6:
        moment = round(moment * 1e-3, 2)
        moment_critical.append(NoEscape(r'&  = ' + str(moment) + r'\times 10 ^ {3} \end{aligned}'))
    else:
        moment = round(moment * 10 ** -6, 2)
        moment_critical.append(NoEscape(r'&  = ' + str(moment) + r'\times 10 ^ {6} \end{aligned}'))

    return moment_critical


def max_moment(critical_mom_1, critical_mom_2):
    """ """
    moment = max(critical_mom_1, critical_mom_2)
    moment = str(round(moment * 10 ** -6, 2))
    critical_mom_1 = str(round(critical_mom_1 * 10 ** -6, 2))

    moment_critical = Math(inline=True)
    moment_critical.append(NoEscape(r'\begin{aligned} M_{\text{critical}} &= \max~\big({M_{\text{critical}}}_{1}, ~{M_{\text{critical}}}_{2}\big) \\'))

    if critical_mom_2 > 1e6:
        critical_mom_2 = round(critical_mom_2 * 1e-6, 2)
        moment_critical.append(NoEscape(r'&              = \max~\big(' + critical_mom_1 + r'\times 10 ^{6}, ~'
                                    + str(critical_mom_2) + r'\times 10 ^{6} \big) \\'))
    else:
        critical_mom_2 = round(critical_mom_2 * 1e-3, 2)
        moment_critical.append(NoEscape(r'&              = \max~\big(' + critical_mom_1 + r'\times 10 ^{6}, ~'
                                        + str(critical_mom_2) + r'\times 10 ^{3} \big) \\'))

    moment_critical.append(NoEscape(r'&              = ' + moment + r'\times 10 ^{6} \end{aligned}'))

    return moment_critical


def md_plate():
    """ """
    moment_demand = Math(inline=True)
    moment_demand.append(NoEscape(r'\begin{aligned} {z_{e}}_{\text{plate}} &= \frac{W {t_{p}}^{2}} {6} \\ \\'))

    moment_demand.append(NoEscape(r' {M_{d}}_{\text{plate}} &= 1.5 {z_{e}}_{\text{plate}} {f_{y}}_{p}~ / ~ \gamma_{m0} \\'))
    moment_demand.append(NoEscape(r'                 &= \frac{ 1.5~ \bigg( \frac{W\times t_p^{2}} {6} \bigg) ~{f_{y}}_{p} } {\gamma_{m0}} \\ \\'))

    moment_demand.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2.1.2}] \end{aligned}'))

    return moment_demand


def plate_thk_required(flange_thk, web_thk, key1, key1_thk, key2, key2_thk, maximum_thk):
    """ """
    thk_required = Math(inline=True)

    if (key1 == 'Yes') and (key2 == 'Yes'):
        if flange_thk == web_thk:
            thk_required.append(NoEscape(r'\begin{aligned} (t,~t_1,~t_2) &< t_p \leq ' + str(maximum_thk) + r' \\'))
            thk_required.append(NoEscape(r' (' + str(flange_thk) + r',~' + str(key1_thk) + r',~'
                                         + str(key2_thk) + r') &< t_p \leq ' + str(maximum_thk) + r' \\ \\'))
        else:
            thk_required.append(NoEscape(r'\begin{aligned} (T,~t,~t_1,~t_2) &< t_p \leq ' + str(maximum_thk) + r' \\'))
            thk_required.append(NoEscape(r' (' + str(flange_thk) + r',~' + str(web_thk) + r',~' + str(key1_thk) + r',~'
                                         + str(key2_thk) + r') &< t_p \leq ' + str(maximum_thk) + r' \\ \\'))
        thk_required.append(NoEscape(r' [Note: ~t_1~and~t_2~ & is~the~thickness~of~shear~key] \end{aligned}'))

    elif key1 == 'Yes':
        if flange_thk == web_thk:
            thk_required.append(NoEscape(r'\begin{aligned} (t,~t_1) &< t_p \leq ' + str(maximum_thk) + r' \\'))
            thk_required.append(NoEscape(r' (' + str(flange_thk) + r',~' + str(key1_thk) + r') &< t_p \leq '
                                         + str(maximum_thk) + r' \\ \\'))
        else:
            thk_required.append(NoEscape(r'\begin{aligned} (T,~t,~t_1) &< t_p \leq ' + str(maximum_thk) + r' \\'))
            thk_required.append(NoEscape(r' (' + str(flange_thk) + r',~' + str(web_thk) + r',~' + str(key1_thk) + r') &< t_p \leq '
                                         + str(maximum_thk) + r' \\ \\'))
        thk_required.append(NoEscape(r' [Note: ~t_1~ & is~the~thickness~of~shear~key] \end{aligned}'))

    elif key2 == 'Yes':
        if flange_thk == web_thk:
            thk_required.append(NoEscape(r'\begin{aligned} (t,~t_2) &< t_p \leq ' + str(maximum_thk) + r' \\'))
            thk_required.append(NoEscape(r' (' + str(flange_thk) + r',~' + str(key2_thk) + r') &< t_p \leq '
                                         + str(maximum_thk) + r' \\ \\'))
        else:
            thk_required.append(NoEscape(r'\begin{aligned} (T,~t,~t_2) &< t_p \leq ' + str(maximum_thk) + r' \\'))
            thk_required.append(NoEscape(r' (' + str(flange_thk) + r',~' + str(web_thk) + r',~' + str(key2_thk) + r') &< t_p \leq '
                                         + str(maximum_thk) + r' \\ \\'))
        thk_required.append(NoEscape(r' [Note: ~t_2~ & is~the~thickness~of~shear~key] \end{aligned}'))

    else:
        if flange_thk == web_thk:
            thk_required.append(NoEscape(r'\begin{aligned} t &< t_p \leq ' + str(maximum_thk) + r' \\'))
            thk_required.append(NoEscape(r' ' + str(flange_thk) + r' &< t_p \leq ' + str(maximum_thk) + r' \end{aligned}'))
        else:
            thk_required.append(NoEscape(r'\begin{aligned} (T,~t) &< t_p \leq ' + str(maximum_thk) + r' \\'))
            thk_required.append(NoEscape(r' (' + str(flange_thk) + r',~' + str(web_thk) + r') &< t_p \leq ' + str(maximum_thk) + r' \end{aligned}'))

    return thk_required


def plate_thk1(critical_mom, plate_thk, plate_thk_provided, gamma_m0, f_y_plate, bp_width, case='Case1'):
    """ """
    plate_thk = str(plate_thk)
    plate_thk_provided = str(plate_thk_provided)
    gamma_m0 = str(gamma_m0)
    f_y_plate = str(f_y_plate)
    bp_width = str(bp_width)

    thk = Math(inline=True)
    thk.append(NoEscape(r'\begin{aligned} {M_{d}}_{\text{plate}} &= M_{\text{critical}} \\'))
    thk.append(NoEscape(r' t_{p} &= \bigg[\frac{4~M_{\text{critical}}} { W~ ({f_{y}}_{p} / \gamma_{m0}) }\bigg]^{0.5}  \\'))
    if case == 'Case1':
        critical_mom = str(round(critical_mom * 10 ** -6, 2))
        thk.append(NoEscape(r' t_{p} &= \bigg[\frac{4 \times~' + critical_mom + r'\times 10 ^{6}} { ' + bp_width + r' \times~ ('
                            + f_y_plate + r' / ' + gamma_m0 + r') }\bigg]^{0.5}  \\'))
    else:  # 'Case2&3'
        critical_mom = str(round(critical_mom * 10 ** -6, 2))
        thk.append(NoEscape(r' t_{p} &= \bigg[\frac{4~ \times' + critical_mom + r'\times 10 ^{6}} { ' + bp_width + r' \times ~ ('
                            + f_y_plate + r' / ' + gamma_m0 + r') }\bigg]^{0.5}  \\'))

    thk.append(NoEscape(r'&       = ' + plate_thk + r' \\'))
    thk.append(NoEscape(r'&       = ' + plate_thk_provided + r'\end{aligned}'))

    return thk


def sigma_allowalbe(concrete_bearing_strength):
    """ """
    concrete_bearing_strength = str(concrete_bearing_strength)

    sigma_allowable = Math(inline=True)
    sigma_allowable.append(NoEscape(r'\begin{aligned} {\sigma_{c}}_{_{{\text{allowable}}}} &= \sigma_{\text{br}}  \\'))
    sigma_allowable.append(NoEscape(r'&       = ' + concrete_bearing_strength + r'\end{aligned}'))

    return sigma_allowable


def max_bearing_stress(tension_demand, y, area_anchor_tension, n, bp_length, f, sigma_c):
    """ """
    tension_demand = str(tension_demand)
    y = str(y)
    area_anchor_tension = str(area_anchor_tension)
    n = str(n)
    bp_length = str(bp_length)
    f = str(f)
    y = str(y)
    sigma_c = str(round(sigma_c, 2))

    sigma_max = Math(inline=True)
    sigma_max.append(NoEscape(r'\begin{aligned} {\sigma_{c}}_{_{{max}}} &= \frac{P_{t}~y}{A_{s}~n~\bigg(\frac{L}{2} - y + f\bigg)}  \\'))
    sigma_max.append(
        NoEscape(r'&                         = \frac{' + tension_demand + r'\times 10^{3} \times' + y + r'}{' + area_anchor_tension + r'\times'
                 + n + r' \times \bigg| \bigg(\frac{' + bp_length + r'}{2} - ' + y + r' + ' + f + r'\bigg) \bigg| } \\'))
    sigma_max.append(NoEscape(r'&       = ' + sigma_c + r'\end{aligned}'))

    return sigma_max


def anchor_len_above(grout_thk, plate_thk, plate_washer_thk, nut_thk, len):
    """ """
    grout_thk = str(grout_thk)
    plate_thk = str(plate_thk)
    plate_washer_thk = str(plate_washer_thk)
    nut_thk = str(nut_thk)
    len = str(len)

    length = Math(inline=True)
    length.append(NoEscape(r'\begin{aligned} l_{1} &= t_{g}~+~t_{p}~+~t_{w}~+~t_{n}~+~20 \\'))
    length.append(NoEscape(r'&       = ' + grout_thk + r'~+~' + plate_thk + r'~+~' + plate_washer_thk + r'~+~' + nut_thk + r'~+~20 \\'))
    length.append(NoEscape(r'&       = ' + len + r' \end{aligned}'))

    return length


def anchor_len_below(bolt_tension, bearing_strength, len, anchor_len_calculated_out, anchor_provided_out, anchor_len_min_out, nut_thk,
                     connectivity='Moment Base Plate', case='Case2&3'):
    """ """
    bolt_tension = str(bolt_tension)
    bearing_strength = str(bearing_strength)
    len = str(len)

    length = Math(inline=True)
    if connectivity == 'Moment Base Plate' and case == 'Case2&3':
        length.append(NoEscape(r'\begin{aligned} l_{2} &= \Bigg[\frac{T_{\text{db}}}{15.5\sqrt{f_{ck}}}\Bigg]^{0.67} \\'))
        length.append(NoEscape(r' &= \Bigg[\frac{' + bolt_tension + r' \times 10^{3}}{15.5 \times \sqrt{' + bearing_strength + r'}}\Bigg]^{0.67} \\'))
        length.append(NoEscape(r' &= ' + str(anchor_len_calculated_out) + r' \\'))
        length.append(NoEscape(r' &= ' + str(anchor_provided_out) + r' \\'))

        length.append(NoEscape(r' &= \max(' + str(anchor_provided_out) + r',~' + str(anchor_len_min_out) + r') \\'))
        anchor_len = max(anchor_provided_out, anchor_len_min_out)
        length.append(NoEscape(r' &= ' + str(anchor_len) + r' \\ \\'))

        length.append(NoEscape(r' &= ' + str(anchor_len) + r' + t_{n} + 20 \\'))
        length.append(NoEscape(r' &= ' + str(anchor_len) + r' + ' + str(nut_thk) + r' + 20 \\'))
        length.append(NoEscape(r' &= ' + str(len) + r' \\ \\'))

        length.append(NoEscape(r'& [\text{Reference: Design of Steel Structures} \\'))
        length.append(NoEscape(r'& \text{by N.Subramanian, (2019 edition).}] \end{aligned}'))
    else:
        length.append(NoEscape(r'\begin{aligned} l_{2} &= ' + len + r' \\ \\'))
        length.append(NoEscape(r'& [\text{Reference: IS 5624:1993, Table 1.}] \end{aligned}'))

    return length


def anchor_range(anchor_len_min, anchor_len_max):
    """ """
    anchor_len_min = str(anchor_len_min)
    anchor_len_max = str(anchor_len_max)

    len_range = Math(inline=True)
    len_range.append(NoEscape(r'\begin{aligned} & ' + anchor_len_min + r' \leq ~l_{a}~\leq ' + anchor_len_max + r' \\ \\'))
    len_range.append(NoEscape(r'&[\text{Reference: IS 5624:1993, Table 1}] \end{aligned}'))

    return len_range


def anchor_length(anchor_len_above, anchor_len_below, anchor_len_total):
    """ """
    anchor_len_above = str(anchor_len_above)
    anchor_len_below = str(anchor_len_below)
    anchor_len_total = str(anchor_len_total)

    length = Math(inline=True)
    length.append(NoEscape(r'\begin{aligned} l_{a} &= l_{1}~+~l_{2} \\'))
    length.append(NoEscape(r'&            = ' + anchor_len_above + r' ~+~' + anchor_len_below + r' \\'))
    length.append(NoEscape(r'&            = ' + anchor_len_total + r' \end{aligned}'))

    return length


def uplift_demand(uplift_tension):
    """ """
    uplift_tension = str(uplift_tension)

    tension = Math(inline=True)
    tension.append(NoEscape(r'\begin{aligned} P_{\text{uplift}} = ' + uplift_tension + r' \end{aligned}'))

    return tension


def no_bolts_uplift(uplift_force, tension_capa):
    """ """
    bolts = round(uplift_force / tension_capa, 2)
    bolts = str(bolts)
    uplift_force = str(uplift_force)
    tension_capa = str(tension_capa)

    n = Math(inline=True)
    n.append(NoEscape(r'\begin{aligned} n_{in} &= \frac{P_{\text{uplift}}}{T_{\text{db}}} \\'))
    n.append(NoEscape(r'&        = \frac{' + uplift_force + r'}{' + tension_capa + r'} \\'))
    n.append(NoEscape(r'&        = ' + bolts + r' \end{aligned}'))

    return n


def stiff_len_flange(bp_width, col_flange_width, stiff_length):
    """ """
    bp_width = str(bp_width)
    col_flange_width = str(col_flange_width)
    stiff_length = str(stiff_length)

    len = Math(inline=True)
    len.append(NoEscape(r'\begin{aligned} {L_{\text{st}}}_{\text{f}} &= \frac{W - B}{2} \\'))
    len.append(NoEscape(r'&              = \frac{' + bp_width + r' - ' + col_flange_width + r'}{2} \\'))
    len.append(NoEscape(r'&              = ' + stiff_length + r' \\ \\'))
    len.append(NoEscape(r'& [\text{Ref. based on detailing requirement}] \end{aligned}'))

    return len


def stiff_height_flange(stiff_length_flange, stiff_height):
    """ """
    stiff_height = str(stiff_height)
    stiff_length_flange = str(stiff_length_flange)

    height = Math(inline=True)
    height.append(NoEscape(r'\begin{aligned} {H_{\text{st}}}_{\text{f}} &= {L_{\text{st}}}_{\text{f}}~+~50 \\'))
    height.append(NoEscape(r'&              = ' + stiff_length_flange + r'~+~50 \\'))
    height.append(NoEscape(r'&              = ' + stiff_height + r' \end{aligned}'))

    return height


def stiff_thk_flange(stiff_thk, stiff_length_flange, epsilon, col_flange_thk):
    """ """
    stiff_thk = str(stiff_thk)
    stiff_length_flange = str(stiff_length_flange)
    epsilon = str(epsilon)
    col_flange_thk = str(col_flange_thk)

    thickness = Math(inline=True)
    thickness.append(NoEscape(r'\begin{aligned} {t_{\text{st}}}_{\text{f}} &= \bigg(\frac{{L_{\text{st}}}_{\text{f}}}{13.6\times \epsilon_{\text{st}}}\bigg) \geq T \\'))
    thickness.append(NoEscape(r'&        = \max \Bigg(\bigg(\frac{' + stiff_length_flange + r'}{13.6\times ' + epsilon + r'}\bigg),~ '
                              + col_flange_thk + r' \Bigg) \\'))
    thickness.append(NoEscape(r'&        = \max(' + stiff_thk + r' , ' + col_flange_thk + r') \\ \\'))

    thickness.append(NoEscape(r' & \text{Note: The stiffener is assumed as semi-compact.} \\'))
    thickness.append(NoEscape(r' & [\text{Ref. IS 800:2007, Table 2}] \end{aligned}'))

    return thickness


def stiff_len_web(bp_length, col_depth, stiff_length):
    """ """
    bp_length = str(bp_length)
    col_depth = str(col_depth)
    stiff_length = str(stiff_length)

    len = Math(inline=True)
    len.append(NoEscape(r'\begin{aligned} {L_{\text{st}}}_{\text{w}} &= \frac{L - D}{2} \\'))
    len.append(NoEscape(r'&              = \frac{' + bp_length + r' - ' + col_depth + r'}{2} \\'))
    len.append(NoEscape(r'&              = ' + stiff_length + r' \\'))
    len.append(NoEscape(r'& [\text{Ref. based on detailing requirement.}] \end{aligned}'))

    return len


def stiff_height_web(stiff_length_web, stiff_height):
    """ """
    stiff_height = str(stiff_height)
    stiff_length_web = str(stiff_length_web)

    height = Math(inline=True)
    height.append(NoEscape(r'\begin{aligned} {H_{\text{st}}}_{\text{w}} &= {L_{\text{st}}}_{\text{w}}~+~50 \\'))
    height.append(NoEscape(r'&              = ' + stiff_length_web + r'~+~50 \\'))
    height.append(NoEscape(r'&              = ' + stiff_height + r' \end{aligned}'))
    # height.append(NoEscape(r'&[Ref.~stiffener~drawing~attached~below \end{aligned}'))

    return height


def stiff_thk_web(stiff_thk, stiff_length_web, epsilon, col_web_thk, bolt_columns_outside_flange):
    """ """
    stiff_thk = str(stiff_thk)
    stiff_length_web = str(stiff_length_web)
    epsilon = str(epsilon)
    col_web_thk = str(col_web_thk)

    thickness = Math(inline=True)
    if bolt_columns_outside_flange == 1:
        thickness.append(NoEscape(r'\begin{aligned} {t_{\text{st}}}_{\text{w}} &= \bigg(\frac{{L_{\text{st}}}_{\text{w}}}{13.6\times \epsilon_{\text{st}}}\bigg) \geq t \\'))
        thickness.append(NoEscape(r'&        = \max \Bigg(\bigg(\frac{' + stiff_length_web + r'}{13.6\times ' + epsilon + r'}\bigg) , '
                                  + col_web_thk + r'\Bigg) \\'))
    else:
        thickness.append(NoEscape(r'\begin{aligned} {t_{\text{st}}}_{\text{w}} &= \bigg(\frac{{L_{\text{st}}}_{\text{w}}~ /~ 2}{13.6\times \epsilon_{\text{st}}}\bigg) \geq t \\'))
        thickness.append(NoEscape(r' &= \bigg(\frac{' + stiff_length_web + r'~ /~ 2}{13.6\times ' + epsilon + r'}\bigg) \geq '
                                  + col_web_thk + r' \\'))

    thickness.append(NoEscape(r'&        = \max(' + stiff_thk + r' , ' + col_web_thk + r') \\ \\'))
    thickness.append(NoEscape(r'&[\text{Ref. IS 800:2007, Table 2.}] \end{aligned}'))

    return thickness


def stiff_len_across_web(stiff_length_flange, stiff_length_web, stiff_length, connectivity):
    """ """
    stiff_length_flange = str(stiff_length_flange)
    stiff_length_web = str(stiff_length_web)
    stiff_length = str(stiff_length)

    len = Math(inline=True)

    if connectivity == 'Welded Column Base':
        len.append(NoEscape(r'\begin{aligned} {L_{\text{st}}}_{\text{aw}} &= ' + stiff_length + r' \end{aligned}'))
    else:
        len.append(NoEscape(r'\begin{aligned} {L_{\text{st}}}_{\text{aw}} &= \max~({L_{\text{st}}}_{\text{f}}, ~{L_{\text{st}}}_{\text{w}}) \\'))
        len.append(NoEscape(r'& \leq \frac{W - t}{2} \\'))
        len.append(NoEscape(r'&               = \max~(' + stiff_length_flange + r', ~' + stiff_length_web + r') \\'))
        len.append(NoEscape(r'&               = ' + stiff_length + r' \end{aligned}'))

    return len


def stiff_height_across_web(stiff_length_across_web, stiff_height):
    """ """
    stiff_height = str(stiff_height)
    stiff_length_across_web = str(stiff_length_across_web)

    height = Math(inline=True)
    height.append(NoEscape(r'\begin{aligned} {H_{\text{st}}}_{\text{aw}} &= {L_{\text{st}}}_{\text{aw}}~+~50 \\'))
    height.append(NoEscape(r'&              = ' + stiff_length_across_web + r'~+~50 \\'))
    height.append(NoEscape(r'&              = ' + stiff_height + r' \end{aligned}'))

    return height


def stiff_thk_across_web(stiff_thk, stiff_length_across_web, epsilon, col_web_thk, max_thk):
    """ """
    max_thk = str(max_thk)
    stiff_thk = str(stiff_thk)
    stiff_length_across_web = str(stiff_length_across_web)
    epsilon = str(epsilon)
    col_web_thk = str(col_web_thk)

    thickness = Math(inline=True)
    thickness.append(NoEscape(r'\begin{aligned} {t_{\text{st}}}_{aw} &= \bigg(\frac{{L_{\text{st}}}_{\text{aw}}}{13.6\times \epsilon_{\text{st}}}\bigg) \geq t \\'))
    thickness.append(NoEscape(r'&        = \max \Bigg(\bigg(\frac{' + stiff_length_across_web + r'}{13.6 \times ' + epsilon + r'}\bigg) ,~ '
                              + col_web_thk + r'\Bigg) \\'))
    thickness.append(NoEscape(r'&        = \max(' + stiff_thk + r' , ' + col_web_thk + r') \\ \\'))
    thickness.append(NoEscape(r'& [\text{Ref. IS 800:2007, Table 2.}] \end{aligned}'))

    return thickness


def stiffener_stress_flange(sigma_crit, max_bearing_stress, sigma_min, bp_len, col_D, y, criticall_xx, sigma_avg, sigma_lby2, connectivity, bp_case):
    """ """

    stress_along_flange = Math(inline=True)

    if connectivity == 'Welded Column Base':
        stress_along_flange.append(NoEscape(r'\begin{aligned} \sigma_{\text{st}} &= \frac{ {\sigma_{\text{c}}}_{\text{max}} + \sigma_{\text{crt}}} {2} \end{aligned}'))
    else:
        if bp_case == 'Case1':
            stress_along_flange.append(NoEscape(r'\begin{aligned} \sigma_{L/2} &= {\sigma_{\text{c}}}_{\text{min}} + \Big( \frac{ {\sigma_{\text{c}}}_{\text{max}} - '
                                                r'{\sigma_{\text{c}}}_{\text{min}} } {2} \Big) \\'))

            stress_along_flange.append(NoEscape(r' &= ' + str(sigma_min) + r' + \Big(\frac{' + str(max_bearing_stress) + r' - '
                                                r'' + str(sigma_min) + r'}{2} \Big) \\ '))

            stress_along_flange.append(NoEscape(r'  &= ' + str(sigma_lby2) + r' \\ \\'))

            stress_along_flange.append(NoEscape(r' {\sigma_{\text{st}}}_{\text{f}} &= \frac{{\sigma_{\text{c}}}_{\text{max}} + \sigma_{L/2}} {2} \\'))
            stress_along_flange.append(NoEscape(r'  &= \frac{' + str(max_bearing_stress) + r' + '
                                                + str(sigma_lby2) + r'} {2} \\ '))
            stress_along_flange.append(NoEscape(r' &= ' + str(sigma_avg) + r' \end{aligned}'))
        else:
            if y > criticall_xx:
                stress_along_flange.append(NoEscape(r'\begin{aligned} \text{Since},~ y & > y_{\text{critical}} ~~~ (' + str(y) + r' > '
                                                    + str(criticall_xx) + r') \\ \\'))

                stress_along_flange.append(NoEscape(r' {\sigma_{\text{st}}}_{\text{f}} &= \frac{{\sigma_{\text{c}}}_{\text{max}}} {2} \\'))
                stress_along_flange.append(NoEscape(r'  &= \frac{' + str(max_bearing_stress) + r'} {2} \\'))
                stress_along_flange.append(NoEscape(r'&                   = ' + str(sigma_avg) + r' \end{aligned}'))
            else:
                stress_along_flange.append(NoEscape(r'\begin{aligned} \text{Since},~ y & \leq y_{\text{critical}} ~~~ (' + str(y) + r' > '
                                                    + str(criticall_xx) + r') \\ \\'))

                stress_along_flange.append(NoEscape(r' \sigma_{\text{crt}} &= \frac{y - y_{\text{critical}}}{y} \times {\sigma_{\text{c}}}_{\text{max}} \\'))
                stress_along_flange.append(NoEscape(r'  &= \frac{' + str(y) + r' - ' + str(criticall_xx) + r'}{' + str(y) + r'} \times '
                                                    + str(max_bearing_stress) + r' \\'))
                stress_along_flange.append(NoEscape(r' &= ' + str(sigma_crit) + r' \\ \\'))

                stress_along_flange.append(NoEscape(r' {\sigma_{\text{st}}}_{\text{f}} &= \frac{{\sigma_{\text{c}}}_{\text{max}} + \sigma_{\text{crt}}} {2} \\'))
                stress_along_flange.append(NoEscape(r'  &= \frac{' + str(max_bearing_stress) + r' + ' + str(sigma_crit) + r'} {2} \\'))
                stress_along_flange.append(NoEscape(r' &= ' + str(sigma_avg) + r' \end{aligned}'))

    return stress_along_flange


def stiffener_stress_web(sigma_max, sigma_crit, sigma_val, type='welded_hollow_bp'):
    """ """

    stress_along_web = Math(inline=True)

    if type == 'welded_hollow_bp':
        stress_along_web.append(NoEscape(r'\begin{aligned} {\sigma_{\text{st}}}_{\text{w}} &= {\sigma_{\text{br}}}_{\text{actual}} \\'))
        stress_along_web.append(NoEscape(r'&                   = ' + str(sigma_val) + r' \end{aligned}'))
    else:
        stress_along_web.append(NoEscape(r'\begin{aligned} {\sigma_{\text{st}}}_{\text{w}} &= \frac{{\sigma_{\text{c}}}_{\text{max}} + \sigma_{\text{crt}}}{2} \\'))
        stress_along_web.append(NoEscape(r'&                   = \frac{' + str(sigma_max) + r' + ' + str(sigma_crit) + r'}{2} \\'))
        stress_along_web.append(NoEscape(r'&                   = ' + str(sigma_val) + r' \end{aligned}'))

    return stress_along_web


def stiffener_stress_across_web(sigma, sigma_max, sigma_min, type='welded_hollow_bp', case='None'):
    """ """
    sigma = str(round(sigma, 2))

    stress_across_web = Math(inline=True)

    if (type == 'welded_hollow_bp') and (case == 'None'):
        stress_across_web.append(NoEscape(r'\begin{aligned} {\sigma_{\text{st}}}_{aw} &= {\sigma_{\text{br}}}_{\text{actual}} \\'))
    elif (type == 'moment_bp') and (case == 'Case2&3'):
        stress_across_web.append(NoEscape(r'\begin{aligned} {\sigma_{\text{st}}}_{aw} &= {\sigma_{\text{br}}}_{\text{actual}} \\'))
    else:
        sigma_max = str(round(sigma_max, 2))
        sigma_min = str(round(sigma_min, 2))

        stress_across_web.append(NoEscape(r'\begin{aligned} {\sigma_{\text{st}}}_{aw} &= \frac{{\sigma_{b}}_{max}~ - ~{\sigma_{b}}_{min}}{2} \\'))
        stress_across_web.append(NoEscape(r'&                    = \frac{' + sigma_max + r'~ - ~' + sigma_min + r'}{2} \\'))

    stress_across_web.append(NoEscape(r'&                    = ' + sigma + r' \end{aligned}'))

    return stress_across_web


def stiffener_stress_allowable(sigma_allowable):
    """ """
    sigma_allowable = str(sigma_allowable)

    stress_allowable = Math(inline=True)
    stress_allowable.append(NoEscape(r'\begin{aligned} &= {\sigma_{\text{c}}}_{\text{allowable}} \\'))
    stress_allowable.append(NoEscape(r'&                = ' + sigma_allowable + r' \end{aligned}'))

    return stress_allowable


def shear_demand_stiffener(sigma_avg, y, y_critical, col_B, bp_len, shear, connectivity, moment_bp_case, anchors_outside_flange, stiffener_len_flange,
                           stiffener_len_web, location='flange'):
    """ """

    shear_demand = Math(inline=True)

    if location == 'flange':

        if connectivity == 'Moment Base Plate':
            if moment_bp_case == 'Case1':
                shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{f}} &=  {\sigma_{\text{st}}}_{\text{f}} \Bigg( \frac{L}{2} \times {L_{\text{st}}}_{\text{f}} \Bigg) \\'))
                shear_demand.append(NoEscape(r' &=  ' + str(sigma_avg) + r' \times \Bigg( \frac{' + str(bp_len) + r'}{2} \times '
                                             + str(stiffener_len_flange) + r' \Bigg) \times 10^{-3} \\'))
                shear_demand.append(NoEscape(r' &=  ' + str(shear) + r' \end{aligned}'))

            else:
                if anchors_outside_flange == 2 or anchors_outside_flange == 4:
                    shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{f}} &=  {\sigma_{\text{st}}}_{\text{f}}~\Big(y \times {L_{\text{st}}}_{\text{f}} \Big) \\'))
                    shear_demand.append(NoEscape(r' &=  ' + str(sigma_avg) + r' \times \Big(' + str(y) + r' \times '
                                                 + str(stiffener_len_flange) + r' \Big) \times 10^{-3} \\'))
                    shear_demand.append(NoEscape(r' &=  ' + str(shear) + r' \end{aligned}'))

                else:
                    if y > y_critical:
                        shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{f}} &=  {\sigma_{\text{st}}}_{\text{f}} \times '
                                                     r'\Bigg( \Big(y - \frac{y_{\text{critical}}}{2} \Big) \times {L_{\text{st}}}_{\text{f}} \Bigg) \\'))
                        shear_demand.append(NoEscape(r' &=  ' + str(sigma_avg) + r' \times '
                                                     r'\Bigg( \Big(' + str(y) + r' - \frac{' + str(y_critical) + r'}{2} \Big) \times '
                                                     + str(stiffener_len_flange) + r' \Bigg) \\'))
                        shear_demand.append(NoEscape(r' & \times 10^{-3} \\'))
                        shear_demand.append(NoEscape(r' &=  ' + str(shear) + r' \end{aligned}'))

                    else:
                        shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{f}} &=  {\sigma_{\text{st}}}_{\text{f}} \times \Bigg(\frac{1}{2} \times y '
                                                     r'\times {L_{\text{st}}}_{\text{f}} \Bigg) \\'))
                        shear_demand.append(NoEscape(r' &=  ' + str(sigma_avg) + r' \times \Bigg(\frac{1}{2} \times ' + str(y) + r' '
                                                     r'\times ' + str(stiffener_len_flange) + r' \Bigg) \times 10^{-3} \\'))
                        shear_demand.append(NoEscape(r' &=  ' + str(shear) + r' \end{aligned}'))
        else:
            shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{f}} &=  {\sigma_{\text{st}}}_{\text{f}} \times \Bigg(\frac{L}{2} \times {L_{\text{st}}}_{\text{f}} \Bigg) \\'))
            shear_demand.append(NoEscape(r' &=  ' + str(sigma_avg) + r' \times \Bigg(\frac{' + str(bp_len) + r'}{2} \times '
                                         + str(stiffener_len_flange) + r' \Bigg) \times 10^{-3} \\'))
            shear_demand.append(NoEscape(r' &=  ' + str(shear) + r' \end{aligned}'))

    elif location == 'web':
        if (connectivity == 'Moment Base Plate') and (moment_bp_case == 'Case3' or moment_bp_case == 'Case2'):
            if (anchors_outside_flange == 3) or (anchors_outside_flange == 6):
                shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{w}} &= {\sigma_{\text{st}}}_{\text{w}} \Bigg( y_{\text{critical}} \times '
                                             r'\frac{{L_{\text{st}}}_{\text{f}}}{2} +  \\'))
                shear_demand.append(NoEscape(r'& {L_{\text{st}}}_{\text{w}} \times \frac{B}{2} \Bigg) \\ \\'))

                shear_demand.append(NoEscape(r' &= ' + str(sigma_avg) + r' \times \Bigg( ' + str(y_critical) + r' \times '
                                             r'\frac{' + str(stiffener_len_flange) + r'}{2} + \\'))
                shear_demand.append(NoEscape(r' & ' + str(stiffener_len_web) + r' \times \frac{' + str(col_B) + r'}{2} \Bigg) \times 10^{-3} \\ \\'))
                shear_demand.append(NoEscape(r' &= ' + str(shear) + r' \end{aligned}'))
            else:
                shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{w}} &= {\sigma_{\text{st}}}_{\text{w}} \Big( B ~{L_{\text{st}}}_{\text{w}} \Big) \\'))
                shear_demand.append(NoEscape(r' &= ' + str(sigma_avg) + r' \times \Big( ' + str(col_B) + r' \times '
                                             + str(stiffener_len_web) + r' \Big) \times 10^{-3} \\'))
                shear_demand.append(NoEscape(r' &= ' + str(shear) + r'  \end{aligned}'))
        else:
            shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{w}} &= {\sigma_{\text{st}}}_{\text{w}} \Big( B~ \times {L_{\text{st}}}_{\text{w}} \Big) \\'))
            shear_demand.append(NoEscape(r' &= ' + str(sigma_avg) + r' \times \Big(' + str(col_B) + r' \times '
                                         + str(stiffener_len_web) + r' \Big) \times 10^{-3} \\'))
            shear_demand.append(NoEscape(r' &= ' + str(shear) + r'  \end{aligned}'))

    elif location == 'across_web':
        shear_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{aw}} &=  {\sigma_{\text{st}}}_{aw} \times ({L_{\text{st}}}_{\text{aw}}~{H_{\text{st}}}_{\text{aw}}) \\'))

    else:
        if moment_bp_case == 'N/A-CHS':
            shear_demand.append(NoEscape(r'\begin{aligned} V_{\text{st}} &=  \sigma_{\text{st}}~ (W ~ L_{\text{st}}) \\'))
            shear_demand.append(NoEscape(r' &=  ' + str(sigma_avg) + r' \times (' + str(bp_len) + r' \times ' + str(stiffener_len_web) + r') \\'))
            shear_demand.append(NoEscape(r' &= ' + str(shear) + r'  \end{aligned}'))

    return shear_demand


def shear_capacity_stiffener(stiff_thk, stiff_height, stiff_fy, shear_capa, gamma_m0, location='flange'):
    """ """
    stiff_thk = str(stiff_thk)
    stiff_height = str(stiff_height)
    stiff_fy = str(stiff_fy)
    shear_capa = str(shear_capa)
    gamma_m0 = str(gamma_m0)

    shear_capacity = Math(inline=True)

    if location == 'flange':
        shear_capacity.append(NoEscape(r'\begin{aligned} {V_{\text{d}}}_{\text{f}} &=  \frac{A_{\text{vg}} {f_{y}}_{\text{st}}} {\sqrt{3} \gamma_{m0}} \\'))
        shear_capacity.append(NoEscape(r'&             =  \frac{{(H_{\text{st}}}_{f}\times {t_{\text{st}}}_{\text{f}}){f_{y}}_{\text{st}}}{\sqrt{3} \gamma_{m0}} \\'))
    elif location == 'web':
        shear_capacity.append(NoEscape(r'\begin{aligned} {V_{\text{d}}}_{\text{w}} &=  \frac{A_{\text{vg}} {f_{y}}_{\text{st}}}{\sqrt{3} \gamma_{m0}} \\'))
        shear_capacity.append(NoEscape(r'&             =  \frac{{(H_{\text{st}}}_{w}\times {t_{\text{st}}}_{\text{w}}){f_{y}}_{\text{st}}}{\sqrt{3} \gamma_{m0}} \\'))
    elif location == 'across_web':
        shear_capacity.append(NoEscape(r'\begin{aligned} {V_{\text{d}}}_{\text{aw}} &=  \frac{A_{\text{vg}} {f_{y}}_{\text{st}}}{\sqrt{3} \gamma_{m0}} \\'))
        shear_capacity.append(NoEscape(r'&             =  \frac{{(H_{\text{st}}}_{aw}\times {t_{\text{st}}}_{aw}){f_{y}}_{\text{st}}}{\sqrt{3} \gamma_{m0}} \\'))
    else:
        shear_capacity.append(NoEscape(r'\begin{aligned} {V_{\text{d}}}_{\text{st}} &=  \frac{A_{\text{vg}} {f_{y}}_{\text{st}}}{\sqrt{3} \gamma_{m0}} \\'))
        shear_capacity.append(NoEscape(r'&             =  \frac{(H_{\text{st}} \times t_{\text{st}}) \times {f_{y}}_{\text{st}}} {\sqrt{3} \times \gamma_{m0}} \\'))

    shear_capacity.append(NoEscape(r'&             =  \frac{(' + stiff_height + r' \times ' + stiff_thk + r') \times ' + stiff_fy + r'}'
                                                                                r'{\sqrt{3} \times ' + gamma_m0 + r' \times 10^{3}} \\'))
    shear_capacity.append(NoEscape(r'&              =  ' + shear_capa + r' \\ \\'))

    shear_capacity.append(NoEscape(r' & \text{Note: Stiffener is not restricted to low shear.} \\'))
    shear_capacity.append(NoEscape(r'& [\text{Ref. IS 800:2007 (Cl.8.4.1)}] \end{aligned}'))

    return shear_capacity


def moment_demand_stiffener(sigma_max, sigma_x, sigma_avg, y, y_critical, bp_len, col_B, stiffener_len_flange, stiffener_len_web, moment,
                            anchors_outside_flange, connectivity, moment_bp_case, location='flange'):
    """ """

    moment_demand = Math(inline=True)

    if location == 'flange':

        if connectivity == 'Moment Base Plate':
            if moment_bp_case == 'Case1':

                moment_demand.append(NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{f}} &= {\sigma_{\text{st}}}_{\text{f}} \Bigg( \frac{L}{2} \times '
                                              r'\frac{{{L_{\text{st}}}_{\text{f}}}^{2}}{2} \Bigg) \\'))
                moment_demand.append(NoEscape(r' &= ' + str(sigma_avg) + r' \times \Bigg( \frac{' + str(bp_len) + r'}{2} \times '
                                              r'\frac{{' + str(stiffener_len_flange) + r'}^{2}}{2} \Bigg) \times 10^{-6} \\'))
                moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))

            else:
                if anchors_outside_flange == 2 or anchors_outside_flange == 4:
                    moment_demand.append(NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{f}} &= {\sigma_{\text{st}}}_{\text{f}} \Bigg( y \times '
                                                  r'\frac{{{L_{\text{st}}}_{\text{f}}}^{2}}{2} \Bigg) \\'))
                    moment_demand.append(NoEscape(r' &= ' + str(sigma_avg) + r' \times \Bigg( ' + str(y) + r' \times '
                                                                                                           r'\frac{{' + str(
                        stiffener_len_flange) + r'}^{2}}{2} \Bigg) \times 10^{-6} \\'))
                    moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))

                else:
                    if y > y_critical:
                        moment_demand.append(NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{f}} &= {\sigma_{\text{st}}}_{\text{f}} \Bigg( \Big(y - \frac{y_{\text{critical}}}{2} '
                                                      r'\Big) \times \frac{{{L_{\text{st}}}_{\text{f}}}^{2}}{2} \Bigg) \\'))
                        moment_demand.append(NoEscape(r' &= ' + str(sigma_avg) + r' \times \Bigg( \Big(' + str(y) + r' - \frac{'
                                                      + str(y_critical) + r'}{2} '
                                                      r'\Big) \times \frac{{' + str(stiffener_len_flange) + r'}^{2}}{2} \Bigg) \\'))
                        moment_demand.append(NoEscape(r' & \times 10^{-6} \\'))
                        moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))

                    else:
                        moment_demand.append(NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{f}} &= {\sigma_{\text{st}}}_{\text{f}} \Bigg(  y \times '
                                                      r'\frac{{{L_{\text{st}}}_{\text{f}}}^{2}}{4} \Bigg) \\'))
                        moment_demand.append(NoEscape(r' &= ' + str(sigma_avg) + r' \Bigg(  ' + str(y) + r' \times '
                                                      r'\frac{{' + str(stiffener_len_flange) + r'}^{2}}{4} \Bigg) \times 10^{-6} \\'))
                        moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))
        else:
            moment_demand.append(NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{f}} &= {\sigma_{\text{st}}}_{\text{f}} \Bigg( \frac{L}{2} \times '
                                          r'\frac{{{L_{\text{st}}}_{\text{f}}}^{2}}{2} \Bigg) \\'))
            moment_demand.append(NoEscape(r' &= ' + str(sigma_avg) + r' \times \Bigg( \frac{' + str(bp_len) + r'}{2} \times '
                                                                                                              r'\frac{{' + str(
                stiffener_len_flange) + r'}^{2}}{2} \Bigg) \times 10^{-6} \\'))
            moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))

    elif location == 'web':

        if connectivity == 'Moment Base Plate':
            if moment_bp_case == 'Case1':

                moment_demand.append(NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{w}} &= \Bigg(\sigma_{\text{crt}} \times B \times \frac{ {{L_{\text{st}}}_{\text{w}}}^{2} }'
                                              r' {2} \Bigg) + \\'))
                moment_demand.append(NoEscape(r' & \Bigg( \Big({\sigma_{\text{c}}}_{\text{max}} - \sigma_{\text{crt}} \Big) \times B \times '
                                              r'\frac{ {{L_{\text{st}}}_{\text{w}}}^{2} } {3} \Bigg) \\ \\'))

                moment_demand.append(NoEscape(r' &= \Bigg(' + str(sigma_x) + r' \times ' + str(col_B) + r' \times \frac{ {'
                                              + str(stiffener_len_web) + r'}^{2} }'r' {2} \Bigg) + \\'))
                moment_demand.append(NoEscape(r' & \Bigg( \Big(' + str(sigma_max) + r' - ' + str(sigma_x) + r' \Big) \times ' + str(col_B) + r' \times '
                                              r'\frac{ {' + str(stiffener_len_web) + r'}^{2} } {3} \Bigg) \times 10^{-6} \\ \\'))

                moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))

            else:
                if anchors_outside_flange == 2 or anchors_outside_flange == 4:
                    moment_demand.append(NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{w}} &= \Bigg(\sigma_{\text{crt}} \times B \times \frac{ {{L_{\text{st}}}_{\text{w}}}^{2} }'
                                                  r' {2} \Bigg) + \\'))
                    moment_demand.append(NoEscape(r' & \Bigg( \Big({\sigma_{\text{c}}}_{\text{max}} - \sigma_{\text{crt}} \Big) \times B \times '
                                                  r'\frac{ {{L_{\text{st}}}_{\text{w}}}^{2} } {3} \Bigg) \\ \\'))

                    moment_demand.append(NoEscape(r' &= \Bigg[ \Bigg(' + str(sigma_x) + r' \times ' + str(col_B) + r' \times \frac{ {'
                                                  + str(stiffener_len_web) + r'}^{2} }'r' {2} \Bigg) + \\'))
                    moment_demand.append(
                        NoEscape(r' & \Bigg( \Big(' + str(sigma_max) + r' - ' + str(sigma_x) + r' \Big) \times ' + str(col_B) + r' \times '
                                                                                                                                r'\frac{ {' + str(
                            stiffener_len_web) + r'}^{2} } {3} \Bigg) \Bigg] \times 10^{-6} \\ \\'))

                    moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))

                else:
                    if y > y_critical:
                        moment_demand.append(
                            NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{w}} &= \frac{\sigma_{\text{crt}}}{2} \Bigg( B~ {L_{\text{st}}}_{\text{w}} + '
                                     r'{L_{\text{st}}}_{\text{w}} ~{L_{\text{st}}}_{\text{f}} \Bigg) \frac{{L_{\text{st}}}_{\text{w}} }{2} ~+ \\'))
                        moment_demand.append(NoEscape(r' & \frac{\Big({\sigma_{\text{c}}}_{\text{max}} - \sigma_{\text{crt}} \Big)}{2} \Bigg( \frac{B~ '
                                                      r'{L_{\text{st}}}_{\text{w}}}{2} + {L_{\text{st}}}_{\text{w}} ~{L_{\text{st}}}_{\text{f}} \Bigg) \\'))
                        moment_demand.append(NoEscape(r' & \times\frac{2}{3} {L_{\text{st}}}_{\text{w}} \\ \\'))

                        moment_demand.append(
                            NoEscape(r' &= \frac{' + str(sigma_x) + r'}{2} \times \Bigg( ' + str(col_B) + r' \times ' + str(stiffener_len_web) + r' + '
                                     r'' + str(stiffener_len_web) + r' \times ' + str(stiffener_len_flange) + r' \Bigg) \\'))
                        moment_demand.append(NoEscape(r' & \times\frac{' + str(stiffener_len_web) + r' }{2} ~+~ \frac{\Big('
                                                      + str(sigma_max) + r' - ' + str(sigma_x) + r' \Big)}{2} \times \\'))
                        moment_demand.append(NoEscape(r' & \Bigg( \frac{'
                                                      + str(col_B) + r' \times '
                                                      r'' + str(stiffener_len_web) + r'}{2} + ' + str(stiffener_len_web) + r' \times '
                                                      + str(stiffener_len_flange) + r' \Bigg) \times \\'))
                        moment_demand.append(NoEscape(r' & \frac{2}{3} \times '
                                                      + str(stiffener_len_web) + r' \times 10^{-6} \\ \\'))

                        moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))

                    else:
                        moment_demand.append(NoEscape(r'\begin{aligned} {M_{\text{st}}}_{\text{w}} &= \frac{{\sigma_{\text{c}}}_{\text{max}}}{2} \times '
                                                      r'\Bigg( B~ {L_{\text{st}}}_{\text{w}} + {L_{\text{st}}}_{\text{w}} ~{L_{\text{st}}}_{\text{f}} \Bigg) \times\frac{{L_{\text{st}}}_{\text{w}} }{2} \\ \\'))

                        moment_demand.append(NoEscape(r' &= \frac{' + str(sigma_max) + r'}{2} \times '
                                                      r'\Bigg( ' + str(col_B) + r' \times ' + str(stiffener_len_web) + r' + '
                                                      + str(stiffener_len_web) + r' \times ' + str(stiffener_len_flange) + r' \Bigg) \times\frac{'
                                                      + str(stiffener_len_web) + r' }{2} \times 10^{-6} \\'))
                        moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))
        else:
            moment_demand.append(NoEscape(r' \begin{aligned} {M_{\text{st}}}_{\text{w}} &= {\sigma_{\text{st}}}_{\text{w}} \times (B + {L_{\text{st}}}_{\text{w}}) \times '
                                          r'\frac{{L_{\text{st}}}_{\text{w}}}{2} \\'))
            moment_demand.append(NoEscape(r' &= ' + str(sigma_max) + r' \times (' + str(col_B) + r' + '
                                          + str(stiffener_len_web) + r') \times 'r'\frac{' + str(stiffener_len_web) + r'}{2} \times 10^{-6} \\'))
            moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))

    elif location == 'across_web':
        moment_demand.append(NoEscape(r'\begin{aligned} {V_{\text{st}}}_{\text{aw}} &=  {\sigma_{\text{st}}}_{aw} \times ({L_{\text{st}}}_{\text{aw}}~{H_{\text{st}}}_{\text{aw}}) \\'))

    else:
        if moment_bp_case == 'N/A-CHS':
            moment_demand.append(NoEscape(r'\begin{aligned} M_{\text{st}} &=  V_{\text{st}} \times \frac{L_{\text{st}}} {2} \\'))
            moment_demand.append(NoEscape(r' &=  ' + str(sigma_max) + r' \times \frac{' + str(stiffener_len_web) + r'}{2} \times 10^{-3} \\'))
            moment_demand.append(NoEscape(r' &=  ' + str(moment) + r' \end{aligned}'))
        else:
            moment_demand.append(NoEscape(r'\begin{aligned} M_{\text{st}} &=  V_{\text{st}} \times \frac{L_{\text{st}}}{2} \\'))

    return moment_demand


def section_modulus_stiffener(z_val, modulus='plastic'):
    """ """
    z_val = str(round(z_val * 10 ** -3, 2))

    z = Math(inline=True)
    if modulus == 'plastic':
        z.append(NoEscape(r'\begin{aligned} {z_{\text{p}}}_{\text{st}} = ' + z_val + r' \times 10^{3} \end{aligned}'))
    else:
        z.append(NoEscape(r'\begin{aligned} {z_{\text{e}}}_{\text{st}} = ' + z_val + r' \times 10^{3} \end{aligned}'))

    return z


def moment_capacity_stiffener(zp, stiff_fy, gamma_m0, moment_capa, location='flange', modulus='elastic'):
    """ """
    zp = str(round(zp * 10 ** -3, 2))
    stiff_fy = str(stiff_fy)
    moment_capa = str(moment_capa)
    gamma_m0 = str(gamma_m0)

    moment_capacity = Math(inline=True)

    if modulus == 'plastic':
        if location == 'flange':
            moment_capacity.append(NoEscape(r'\begin{aligned} {M_{\text{d}}}_{\text{f}} &=  \frac{\beta_{b} {z_{\text{p}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}} \\'))
        elif location == 'web':
            moment_capacity.append(NoEscape(r'\begin{aligned} {M_{\text{d}}}_{\text{w}} &=  \frac{\beta_{b} {z_{\text{p}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}} \\'))
        elif location == 'across_web':
            moment_capacity.append(NoEscape(r'\begin{aligned} {M_{\text{d}}}_{\text{aw}} &=  \frac{\beta_{b} {z_{\text{p}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}} \\'))
        else:
            moment_capacity.append(NoEscape(r'\begin{aligned} {M_{\text{d}}}_{\text{st}} &=  \frac{\beta_{b} {z_{\text{e}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}} \\'))

        moment_capacity.append(NoEscape(r'&             =  \frac{1\times~ {z_{\text{p}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}}~~~~(\beta_{b} = 1) \\'))
    else:
        if location == 'flange':
            moment_capacity.append(NoEscape(r'\begin{aligned} {M_{\text{d}}}_{\text{f}} &=  \frac{\beta_{b} {z_{\text{e}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}} \\'))
        elif location == 'web':
            moment_capacity.append(NoEscape(r'\begin{aligned} {M_{\text{d}}}_{\text{w}} &=  \frac{\beta_{b} {z_{\text{e}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}} \\'))
        elif location == 'across_web':
            moment_capacity.append(NoEscape(r'\begin{aligned} {M_{\text{d}}}_{\text{aw}} &=  \frac{\beta_{b} {z_{\text{e}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}} \\'))
        else:
            moment_capacity.append(NoEscape(r'\begin{aligned} {M_{\text{d}}}_{\text{st}} &=  \frac{\beta_{b} {z_{\text{e}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}} \\'))

        moment_capacity.append(NoEscape(r'&             =  \frac{1\times {z_{\text{e}}}_{\text{st}} {f_{y}}_{\text{st}}}{\gamma_{m0}}~~~~(\beta_{b} = 1) \\'))

    moment_capacity.append(NoEscape(r'&             =  \frac{1\times~' + zp + r'\times 10^{3} \times' + stiff_fy + r'}{'
                                    + gamma_m0 + r' \times 10^{6}} \\'))
    moment_capacity.append(NoEscape(r'&              =  ' + moment_capa + r' \\ \\'))

    moment_capacity.append(NoEscape(r'&[\text{Ref. IS 800:2007 (Cl.8.2.1.2)}] \end{aligned}'))

    return moment_capacity


def continuity_plate_len_bp(len_out, len_in, col_D, col_T, notch_size):
    """ """
    len = Math(inline=True)

    len.append(NoEscape(r'\begin{aligned} l_{\text{out}} &= D - (2T) \\'))
    len.append(NoEscape(r'                       &= D - (2 \times ' + str(col_T) + r') \\'))
    len.append(NoEscape(r'                       &= ' + str(len_out) + r' \\ \\'))

    len.append(NoEscape(r'  l_{\text{in}} &= l_{\text{out}} - \text{notch} \\'))
    len.append(NoEscape(r'  &= l_{\text{out}} - ' + str(notch_size) + r' \\'))
    len.append(NoEscape(r'  &= ' + str(len_in) + r' \end{aligned}'))

    return len


def continuity_plate_width_bp(col_B, col_t, notch_size, stiffener_width):
    """ """
    len = Math(inline=True)

    len.append(NoEscape(r'\begin{aligned} W &= \frac{B - t - (2 \times \text{notch})} {2} \\'))
    len.append(NoEscape(r'                  &= \frac{' + str(col_B) + r' - ' + str(col_t) + r' - (2 \times ' + str(notch_size) + r')} {2} \\'))
    len.append(NoEscape(r'                  &= ' + str(stiffener_width) + r' \end{aligned}'))

    return len


def continuity_plate_thk_req_bp(thk_1, thk_2, col_T, stiffener_len, stiffener_thk_along_web):
    """ """
    thickness = Math(inline=True)

    thickness.append(NoEscape(r'\begin{aligned} t_{1} &= \frac{l_{\text{out}}} {29.3 \epsilon} \\'))
    thickness.append(NoEscape(r'                  &= \frac{' + str(stiffener_len) + r'} {29.3 \times 1.0} \\'))
    thickness.append(NoEscape(r'                  &= ' + str(thk_1) + r' \\ \\'))

    thickness.append(NoEscape(r' t_{2} &= \max(T,~{t_{\text{st}}}_{\text{w}}) \\'))
    thickness.append(NoEscape(r'                  &= \max(' + str(col_T) + r',~' + str(stiffener_thk_along_web) + r') \\'))
    thickness.append(NoEscape(r'                  &= ' + str(thk_2) + r' \end{aligned}'))

    return thickness


def continuity_plate_thk_prov_bp(thk):
    """ """
    thickness = Math(inline=True)

    thickness.append(NoEscape(r'\begin{aligned} t &= ' + str(thk) + r' \end{aligned}'))

    return thickness


def stiff_len_chs(bp_length, od, stiff_length):
    """ """
    bp_length = str(bp_length)
    od = str(od)
    stiff_length = str(stiff_length)

    len = Math(inline=True)

    len.append(NoEscape(r'\begin{aligned} L_{\text{st}} &= \frac{L - OD}{2} \\'))
    len.append(NoEscape(r'                       &= \frac{' + bp_length + r' - ' + od + r'}{2} \\'))
    len.append(NoEscape(r'                       &= ' + stiff_length + r' \end{aligned}'))

    return len


def stiff_len_shs_rhs(bp_length, bp_width, col_D, col_B, stiff_length_along_D, stiff_length_along_B):
    """ """
    len = Math(inline=True)

    len.append(NoEscape(r'\begin{aligned} {L_{\text{st}}}_{1} &= \frac{L - D}{2}~~~ \text{along column D} \\'))
    len.append(NoEscape(r'                             &= \frac{' + str(bp_length) + r' - ' + str(col_D) + r'}{2} \\'))
    len.append(NoEscape(r'                             &= ' + str(stiff_length_along_D) + r' \\ \\'))

    len.append(NoEscape(r'                {L_{\text{st}}}_{2} &= \frac{W - B}{2}~~~ \text{along column B} \\'))
    len.append(NoEscape(r'                             &= \frac{' + str(bp_width) + r' - ' + str(col_B) + r'}{2} \\'))
    len.append(NoEscape(r'                             &= ' + str(stiff_length_along_B) + r' \\ \end{aligned}'))

    return len


def stiff_height_chs(stiff_length, stiff_height):
    """ """

    height = Math(inline=True)

    height.append(NoEscape(r'\begin{aligned} H_{\text{st}} &= L_{\text{st}} + 50 \\'))
    height.append(NoEscape(r'                       &= ' + str(stiff_length) + r' + 50 \\'))
    height.append(NoEscape(r'                       &= ' + str(stiff_height) + r' \end{aligned}'))

    return height


def stiff_height_shs_rhs(stiff_length_D, stiff_length_B, stiff_height_D, stiff_height_B):
    """ """

    height = Math(inline=True)

    height.append(NoEscape(r'\begin{aligned} {H_{\text{st}}}_{1} &= {L_{\text{st}}}_{1} + 50 \\'))
    height.append(NoEscape(r'                       &= ' + str(stiff_length_D) + r' + 50 \\'))
    height.append(NoEscape(r'                       &= ' + str(stiff_height_D) + r' \\ \\'))

    height.append(NoEscape(r'          {H_{\text{st}}}_{2} &= {L_{\text{st}}}_{2} + 50 \\'))
    height.append(NoEscape(r'                       &= ' + str(stiff_length_B) + r' + 50 \\'))
    height.append(NoEscape(r'                       &= ' + str(stiff_height_B) + r' \end{aligned}'))

    return height


def stiff_thk_hollow(stiff_length, epsilon, stiff_thk, tube_thk):
    """ """

    thickness = Math(inline=True)

    thickness.append(NoEscape(r'\begin{aligned} t_{\text{st}} &= \bigg(\frac{L_{\text{st}}}{13.6 \times \epsilon_{\text{st}}}\bigg) \geq T \\'))
    thickness.append(NoEscape(r'&        = \bigg(\frac{' + str(stiff_length) + r'}{13.6 \times ' + str(epsilon) + r'}\bigg) \geq '
                              + str(tube_thk) + r' \\'))
    thickness.append(NoEscape(r'&        = \max(' + str(stiff_thk) + r' , ' + str(tube_thk) + r') \\ \\'))

    thickness.append(NoEscape(r'& [\text{Ref. IS 800:2007, Table 2.}] \end{aligned}'))

    return thickness


def stiffener_stress(actual_bearing_stress):
    """ """

    stress = Math(inline=True)
    stress.append(NoEscape(r'\begin{aligned} \sigma_{\text{st}} &= {\sigma_{\text{br}}}_{\text{actual}}  \\'))
    stress.append(NoEscape(r'&                    = ' + str(actual_bearing_stress) + r' \end{aligned}'))

    return stress


def high_shear_req(shear_capa_stiffener):
    """ """
    shear_req = Math(inline=True)

    shear_req.append(NoEscape(r'\begin{aligned} V_{\text{st}} &\leq  0.6 \times {V_{d}}_{st} \\'))
    shear_req.append(NoEscape(r'                       &\leq  0.6 \times ' + str(shear_capa_stiffener) + r' \\'))
    shear_req.append(NoEscape(r'                       &\leq  ' + str(round(0.6 * shear_capa_stiffener, 2)) + r' \end{aligned}'))

    return shear_req


def shear_resistance(axial_load, mu, shear_resistance_val):
    """ """
    resistance = Math(inline=True)
    resistance.append(NoEscape(r'\begin{aligned} V_{r} &= P_{u} \times \mu  \\'))
    resistance.append(NoEscape(r'&                      = ' + str(axial_load) + r' \times ' + str(mu) + r' \\'))
    resistance.append(NoEscape(r'&                      = ' + str(shear_resistance_val) + r' \end{aligned}'))

    return resistance


def shear_load(shear_load, location='L1'):
    """ """
    shear = Math(inline=True)

    if location == 'L1':
        shear.append(NoEscape(r'\begin{aligned} V_{1} &= ' + str(shear_load) + r' ~~kN \end{aligned}'))
    else:
        shear.append(NoEscape(r'\begin{aligned} V_{2} &= ' + str(shear_load) + r' ~~kN \end{aligned}'))

    return shear


def shear_resistance_check(shear_load, shear_resistance_val, remark='', location='L1'):
    """ """
    resistance_check = Math(inline=True)

    if location == 'L1':
        if remark == 'Shear key required':
            resistance_check.append(NoEscape(r'\begin{aligned} V_{1} &> V_{r}  \\'))
            resistance_check.append(NoEscape(r'  ' + str(shear_load) + r' &> ' + str(shear_resistance_val) + r'  \end{aligned}'))
        else:
            resistance_check.append(NoEscape(r'\begin{aligned} V_{1} &\leq V_{r}  \\'))
            resistance_check.append(NoEscape(r'  ' + str(shear_load) + r' &\leq ' + str(shear_resistance_val) + r'  \end{aligned}'))
    else:
        if remark == 'Shear key required':
            resistance_check.append(NoEscape(r'\begin{aligned} V_{2} &> V_{r}  \\'))
            resistance_check.append(NoEscape(r'  ' + str(shear_load) + r' &> ' + str(shear_resistance_val) + r'  \end{aligned}'))
        else:
            resistance_check.append(NoEscape(r'\begin{aligned} V_{2} &\leq V_{r}  \\'))
            resistance_check.append(NoEscape(r'  ' + str(shear_load) + r' &\leq ' + str(shear_resistance_val) + r'  \end{aligned}'))

    return resistance_check


def key_length(length, location='L1'):
    """ """
    length_eqn = Math(inline=True)

    if location == 'L1':
        length_eqn.append(NoEscape(r'\begin{aligned} L_{1} &= ' + str(length) + r' \end{aligned}'))
    else:
        length_eqn.append(NoEscape(r'\begin{aligned} L_{2} &= ' + str(length) + r' \end{aligned}'))

    return length_eqn


def key_depth(depth, location='L1'):
    """ """
    depth_eqn = Math(inline=True)

    if location == 'L1':
        depth_eqn.append(NoEscape(r'\begin{aligned} H_{1} &= ' + str(depth) + r' \end{aligned}'))
    else:
        depth_eqn.append(NoEscape(r'\begin{aligned} H_{2} &= ' + str(depth) + r' \end{aligned}'))

    return depth_eqn


def key_bearing_stress(load_shear, shear_resistance, key_length, key_depth, key_bearing_stress, location='L1'):
    """ """
    bearing_stress = Math(inline=True)

    if location == 'L1':
        bearing_stress.append(NoEscape(r'\begin{aligned} \sigma_{1} &= \frac{V_{1} - V_{r}} {L_{1} \times H_{1}} \\'))
    else:
        bearing_stress.append(NoEscape(r'\begin{aligned} \sigma_{2} &= \frac{V_{2} - V_{r}} {L_{2} \times H_{2}} \\'))

    bearing_stress.append(NoEscape(r' &= \frac{(' + str(load_shear * 1e-3) + r' - ' + str(round(shear_resistance * 1e-3, 2)) + r') \times 10^{3} } {'
                                   + str(key_length) + r' \times ' + str(key_depth) + r'} \\'))
    bearing_stress.append(NoEscape(r' &= ' + str(key_bearing_stress) + r' \end{aligned}'))

    return bearing_stress


def key_moment_demand(load_shear, shear_resistance, key_len, load_unit_len, key_depth, moment_demand, location='L1'):
    """ """
    key_md = Math(inline=True)

    if location == 'L1':
        key_md.append(NoEscape(r' \begin{aligned} w_{1} &= \frac{V_{1} - V_{r}}{L_{1}}~~~~(kN/mm) \\'))
    else:
        key_md.append(NoEscape(r' \begin{aligned} w_{2} &= \frac{V_{2} - V_{r}}{L_{2}}~~~~(kN/mm) \\'))

    key_md.append(NoEscape(r' &= \frac{' + str(load_shear * 1e-3) + r' - ' + str(round(shear_resistance * 1e-3, 2)) + r'}'r'{' + str(key_len) + r'} \\'))
    key_md.append(NoEscape(r'                       &= ' + str(round(load_unit_len * 1e-3, 2)) + r' \\ \\'))

    if location == 'L1':
        key_md.append(NoEscape(r'                {M_{\text{d}}}_{1} &= w_{1} \times \frac{{H_{1}}^{2}} {2} \\'))
    else:
        key_md.append(NoEscape(r'                {M_{\text{d}}}_{2} &= w_{2} \times \frac{{H_{2}}^{2}} {2} \\'))

    key_md.append(NoEscape(r'                            &= ' + str(round(load_unit_len * 1e-3, 2)) + r' \times \frac{{' + str(key_depth) + r'}^{2}} {2} '
                                                                                                                                  r'\times 10^{-3} \\'))
    key_md.append(NoEscape(r'                            &= ' + str(round(moment_demand * 1e-3, 2)) + r' \end{aligned}'))

    return key_md


def key_moment_capacity(key_depth, key_thk, key_fy, gamma_m0, moment_capacity, beta_b=1, location='L1'):
    """ """
    key_capacity = Math(inline=True)

    if location == 'L1':
        key_capacity.append(NoEscape(r' \begin{aligned} {M_{\text{p}}}_{1} &= \beta_{b} Z_{\text{p}} f_{y} / \gamma_{m0} \\'))
        key_capacity.append(NoEscape(r'&                           = \frac{\beta_{b} \bigg(\frac{H_{1}t_{1}^{2}} {4} \bigg) f_{y} } {\gamma_{m0}} \\'))
    else:
        key_capacity.append(NoEscape(r' \begin{aligned} {M_{\text{p}}}_{2} &= \beta_{b} Z_{\text{p}} f_{y} / \gamma_{m0} \\'))
        key_capacity.append(NoEscape(r'&                            = \frac{\beta_{b} \bigg(\frac{H_{2}t_{2}^{2}} {4} \bigg) f_{y} } {\gamma_{m0}} \\'))

    key_capacity.append(NoEscape(r'&                            = \frac{' + str(beta_b) + r' \times \bigg(\frac{' + str(key_depth) + r' \times '
                           + str(key_thk) + r'^{2}} {4} \bigg) \times ' + str(key_fy) + r' } {' + str(gamma_m0) + r' \times 10^{6} } \\'))
    key_capacity.append(NoEscape(r'&  = ' + str(moment_capacity) + r' \end{aligned}'))

    return key_capacity


def key_thk(moment_demand, gamma_m0, key_fy, key_depth, key_thk_val, column_tw, key_thk, location='L1'):
    """ """
    key_thk_eqn = Math(inline=True)

    if location == 'L1':
        key_thk_eqn.append(NoEscape(r' \begin{aligned} t_{1} &= \sqrt{\frac{4 {M_{\text{d}}}_{1}}{H_{1} (f_{y}/\gamma_{m0})}} \\'))
    else:
        key_thk_eqn.append(NoEscape(r' \begin{aligned} t_{2} &= \sqrt{\frac{4 {M_{\text{d}}}_{2}}{H_{2} (f_{y}/\gamma_{m0})}} \\'))

    key_thk_eqn.append(NoEscape(r'& = \sqrt{\frac{4 \times ' + str(round(moment_demand * 1e-6, 2)) + r' \times 10^{6}} {'
                                + str(key_depth) + r' \times (' + str(key_fy) + r'/ '+ str(gamma_m0) + r')}} \\'))
    key_thk_eqn.append(NoEscape(r'& = ' + str(round(key_thk_val, 2)) + r' \\'))

    if location == 'L1':
        key_thk_eqn.append(NoEscape(r'& = \max(t_{1},~t) \\'))
    else:
        key_thk_eqn.append(NoEscape(r'& = \max(t_{2},~t) \\'))

    key_thk_eqn.append(NoEscape(r'& = \max(' + str(round(key_thk_val, 2)) + r',~' + str(column_tw) + r') \\'))

    if location == 'L1':
        key_thk_eqn.append(NoEscape(r'& = ' + str(key_thk) + r' \end{aligned}'))
    else:
        key_thk_eqn.append(NoEscape(r'& = ' + str(key_thk) + r' \\ \\'))

        key_thk_eqn.append(NoEscape(r' & [\text{Note: If } t_{1} \text{ is provided, } t_{2} \text{ is at-least} \\'))
        key_thk_eqn.append(NoEscape(r' \text{equal to } t_{1}.] \end{aligned}'))

    return key_thk_eqn


def high_shear_provided(shear_on_stiffener):
    """ """
    shear_provided = Math(inline=True)

    shear_provided.append(NoEscape(r'\begin{aligned} V_{\text{st}} &= ' + str(shear_on_stiffener) + r' \end{aligned}'))

    return shear_provided


def bolt_shear_demand(V, n_bolts, V_sb, type = None):

    """
    Calculate bolt shear demand in each bolts

    Args:
           V: factored shear load in KN (float)
           n_bolts: no. of bolts (int)
           V_d:bolt shear demand in KN (float)
    Returns:
        shear demand in bolts
    """
    V = str(V)
    n_bolts = str(n_bolts)
    V_sb = str(V_sb)
    type = str(type)
    bolt_shear_demand = Math(inline=True)
    if type == 'Bearing Bolt':
        bolt_shear_demand.append(NoEscape(r'\begin{aligned} V_{sb} &= \frac{V_{u}}{\ n} \\'))
    else:
        bolt_shear_demand.append(NoEscape(r'\begin{aligned} V_{sf} &= \frac{V_{u}}{\ n} \\'))

    bolt_shear_demand.append(NoEscape(r'&=\frac{' + V + '}{' + n_bolts + r'} \\'))
    bolt_shear_demand.append(NoEscape(r'&= ' + V_sb + r'\end{aligned}'))
    return bolt_shear_demand


def bb_endplate_height_prov(beam_D, end_distance_provided, pitch_distance_provided, height_plate, bolt_row=None, type=None):
    beam_D = str(beam_D)
    height_plate = str(height_plate)
    end_distance_provided = str(end_distance_provided)
    pitch_distance_provided = str(pitch_distance_provided)
    bb_endplate_height_prov = Math(inline=True)

    if type == 'Flushed - Reversible Moment':
        bb_endplate_height_prov.append(NoEscape(r'\begin{aligned} H_{p} &= D + 25 \\'))
        bb_endplate_height_prov.append(NoEscape(r' &= ' + beam_D + r'+ 25 \\'))
    elif type == 'Extended One Way - Irreversible Moment':
        if bolt_row <= 4:
            bb_endplate_height_prov.append(NoEscape(r'\begin{aligned} H_{p} &= D + 12.5 + (2 \times e)\\'))
            bb_endplate_height_prov.append(NoEscape(r' &= ' + beam_D + r'+ 12.5 + (2 \times ' + end_distance_provided + r')\\'))
        else:  # 2 rows above tension flange which is maximum allowable
            bb_endplate_height_prov.append(NoEscape(r'\begin{aligned} H_{p} &= D + 12.5 + (2 \times e) + p\\'))
            bb_endplate_height_prov.append(
                NoEscape(r' &= ' + beam_D + r' + 12.5 + (2 \times ' + end_distance_provided + r') + ' + pitch_distance_provided + r'\\'))
    else:
        if bolt_row < 8:  # 1 row outside tension and compressionflange
            bb_endplate_height_prov.append(NoEscape(r'\begin{aligned} H_{p} &= D + (2 \times (2 \times e))\\'))
            bb_endplate_height_prov.append(NoEscape(r' &= ' + beam_D + r' + (2 \times (2 \times ' + end_distance_provided + r')) \\'))
        else:  # 2 rows outside tension and compression flange which is maximum allowable
            bb_endplate_height_prov.append(NoEscape(r'\begin{aligned} H_{p} &= D + (2 \times (2 \times e)) + (2 \times p)\\'))
            bb_endplate_height_prov.append(
                NoEscape(r'&= ' + beam_D + r' + (2 \times (2 \times ' + end_distance_provided + r'))+(2 \times ' + pitch_distance_provided + r') \\'))
    bb_endplate_height_prov.append(NoEscape(r'&= ' + height_plate + r'\end{aligned}'))
    return bb_endplate_height_prov


def tension_list(list_rows):

    tension_bolt_rows = Math(inline=True)
    tension_bolt_rows.append(NoEscape(r'\begin{aligned} T &= ' + str(list_rows) + r' \\ '))
    tension_bolt_rows.append(NoEscape(r' &  \end{aligned}'))

    return tension_bolt_rows


def compression_flange_capacity(beam_B, beam_T, beam_fy, gamma_m0, capacity):

    flange_capacity = Math(inline=True)
    flange_capacity.append(NoEscape(r'\begin{aligned} F_{c} &= A_{g} f_{y}~ /~\gamma_{m0} \\'))
    flange_capacity.append(NoEscape(r' &= \frac{B T  f_{y}}{\gamma_{m0}} \\'))
    flange_capacity.append(NoEscape(r' &= \frac{' + str(beam_B) + r' \times ' + str(beam_T) + r' \times ' + str(beam_fy) + r'}{'
                                    + str(gamma_m0) + r' \times 1000} \\'))
    flange_capacity.append(NoEscape(r' &= ' + str(capacity) + r' \end{aligned}'))

    return flange_capacity


def reaction_compression_flange(r_c, bolt_col, bolt_row, tension_sum):

    reaction = Math(inline=True)
    reaction.append(NoEscape(r'\begin{aligned} R_{c} &= n_{c}~ \displaystyle\sum_{n_{r} = 1} ^ {n_{r}} T_{n_{r}} \\'))
    reaction.append(NoEscape(r' &= ' + str(bolt_col) + r' \times \displaystyle\sum_{n_{r} = 1} ^ {' + str(bolt_row) + r'} T_{n_{r}} \\'))
    reaction.append(NoEscape(r' &= ' + str(bolt_col) + r' \times ' + str(tension_sum) + r' \\'))
    reaction.append(NoEscape(r' &= ' + str(r_c) + r' \end{aligned}'))

    return reaction


def bb_endplate_width_prov(B_ep, B):
    B = str(B)
    B_ep = str(B_ep)
    bb_endplate_width_prov = Math(inline=True)
    bb_endplate_width_prov.append(NoEscape(r'\begin{aligned} B_{p} &= B + 25 \\'))
    bb_endplate_width_prov.append(NoEscape(r' &= ' + B + r' + 25 \\'))
    bb_endplate_width_prov.append(NoEscape(r' &= ' + B_ep + r'\end{aligned}'))
    return bb_endplate_width_prov


def stiffener_height_prov(b_ep, t_w, h_ep, D, h_sp, type=None):
    h_ep = str(h_ep)
    b_ep = str(b_ep)
    t_w = str(t_w)
    D = str(D)
    h_sp = str(h_sp)
    stiffener_height_prov = Math(inline=True)
    if type == 'Flushed - Reversible Moment':

        stiffener_height_prov.append(NoEscape(r'\begin{aligned} W_{st} &= B_{p} - \frac{t}{2} \\'))
        stiffener_height_prov.append(NoEscape(r' &= '+b_ep+r' - \frac{'+t_w+r'}{2}\\'))

    else:
        if type == 'Extended Both Ways - Reversible Moment':
            stiffener_height_prov.append(NoEscape(r'\begin{aligned} H_{\text{st}} &= \frac{H_{p} - D} {2} \\'))
            stiffener_height_prov.append(NoEscape(r' &= \frac{' + h_ep + r' - ' + D + r'} {2} \\'))
        else:
            stiffener_height_prov.append(NoEscape(r'\begin{aligned} H_{\text{st}} &= H_{p} - D - 12.5 \\'))
            stiffener_height_prov.append(NoEscape(r' &= '+h_ep+r' - '+D +r'- 12.5 \\'))

    stiffener_height_prov.append(NoEscape(r' &= ' + h_sp + r'\end{aligned}'))

    return stiffener_height_prov


def stiffener_length_prov(h_sp, l_sp, type=None):
    h_sp = str(h_sp)
    l_sp = str(l_sp)
    stiffener_length_prov = Math(inline=True)

    if type == 'Flushed - Reversible Moment':
        stiffener_length_prov.append(NoEscape(r'\begin{aligned} L_{\text{st}} &= 2 W_{st}  \\'))
        stiffener_length_prov.append(NoEscape(r'&= 2 \times '+ h_sp +r' \\'))
    else:
        stiffener_length_prov.append(NoEscape(r'\begin{aligned} L_{\text{st}} &= \frac{H_{\text{st}}}{ \tan30 ^ {\circ} }  \\'))
        stiffener_length_prov.append(NoEscape(r'&= \frac{'+h_sp+r'} {\tan30 ^ {\circ}}  \\'))

    stiffener_length_prov.append(NoEscape(r' &= ' + l_sp + r'\end{aligned}'))

    return stiffener_length_prov


def f_a_stress_due_to_axial_force(A_f, t_w, L_weld, f_a):
    """
    t_w = weld size of the weld (mm)
    A_f = Factored Axial load (N-mm)
    L_weld = weld_length_web (mm)
    :return:
    """
    A_f = str(A_f)
    t_w = str(t_w)
    L_weld = str(L_weld)
    f_a = str(f_a)
    f_a_stress_due_to_axial_force = Math(inline=True)

    f_a_stress_due_to_axial_force.append(NoEscape(r'\begin{aligned} f_a &= \frac{H}{0.7 t_w L_{w}}\\'))
    f_a_stress_due_to_axial_force.append(NoEscape(r' &= \frac{'+A_f+r'\times 10^3}{0.7 \times '+t_w+r' \times '+L_weld+r'}\\'))
    f_a_stress_due_to_axial_force.append(NoEscape(r' &= '+f_a+r'\\ \\'))
    f_a_stress_due_to_axial_force.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.9}] \end{aligned}'))

    return f_a_stress_due_to_axial_force


def q_stress_due_to_shear_force(V, t_w, L_weld, q):
    """
    t_w = weld size of the weld (mm)
    V = Factored Shear load (N-mm)
    L_weld = weld_length_web (mm)
    :return:
    """
    V = str(V)
    t_w = str(t_w)
    L_weld = str(L_weld)
    q = str(q)
    q_stress_due_to_shear_force = Math(inline=True)

    q_stress_due_to_shear_force.append(NoEscape(r'\begin{aligned} q &= \frac{V}{0.7 t_w L_{w}}\\'))
    q_stress_due_to_shear_force.append(NoEscape(r'&= \frac{'+V+ r' \times  10^3}{0.7 \times'+t_w+r' \times '+L_weld+r'}\\'))
    q_stress_due_to_shear_force.append(NoEscape(r' &= ' + q + r'\\ \\'))
    q_stress_due_to_shear_force.append(NoEscape(r'& [ \text{Ref. IS 800:2007, Cl.10.5.9}] \end{aligned}'))
    return q_stress_due_to_shear_force


def f_e_weld_stress_due_to_combined_load(f_a, f_e, q):
    """
    t_w = weld size of the weld (mm)
    V = Factored Shear load (N-mm)
    L_weld = weld_length_web (mm)
    :return:
    """
    f_a = str(f_a)
    f_e = str(f_e)
    q = str(q)

    f_e_weld_stress_due_to_combined_load = Math(inline=True)
    f_e_weld_stress_due_to_combined_load.append(NoEscape(r'\begin{aligned} f_e  &= \sqrt{f_a^{2} + 3 q^{2}}\\'))

    f_e_weld_stress_due_to_combined_load.append(NoEscape(r' &= \sqrt{'+f_a+r'^{2}  + (3 \times'+ q+r' ^ 2)}\\'))
    f_e_weld_stress_due_to_combined_load.append(NoEscape(r' &= ' + f_e+ r' \\ \\'))
    f_e_weld_stress_due_to_combined_load.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.10.1.1}] \end{aligned}'))

    return f_e_weld_stress_due_to_combined_load


def weld_fu(weld_material_fu, plate_material_fu):
    weld_fu_eqn = Math(inline=True)

    weld_fu_eqn.append(NoEscape(r'\begin{aligned} f_{u_w} &= \min(f_{\text{w}}, ~f_{u}) \\'))
    weld_fu_eqn.append(NoEscape(r'  &= \min(' + str(weld_material_fu) + r', ~' + str(plate_material_fu) + r') \\ \\'))
    weld_fu_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.7.1.1}] \end{aligned}'))

    return weld_fu_eqn


def weld_fu_cp(weld_material_fu, cp_material_fu):
    weld_fu_eqn = Math(inline=True)

    weld_fu_eqn.append(NoEscape(r'\begin{aligned} f_{uw} &= \min(f_{\text{w}}, ~{f_{u}}_{cp}) \\'))
    weld_fu_eqn.append(NoEscape(r'  &= \min(' + str(weld_material_fu) + r', ~' + str(cp_material_fu) + r') \\ \\'))
    weld_fu_eqn.append(NoEscape(r'[Ref.&~IS~800:2007,~Cl.~10.5.7.1.1] \end{aligned}'))

    return weld_fu_eqn


def weld_length_cp(weld_length, weld_both_side):
    weld_fu_eqn = Math(inline=True)

    weld_fu_eqn.append(NoEscape(r'\begin{aligned} {L_{w}}_{cp} &= ' + str(weld_length) + r' \\ \\'))

    if weld_both_side == True:
        weld_fu_eqn.append(NoEscape(r' & \text{Note: Provide weld on both the sides}  \\'))
        weld_fu_eqn.append(NoEscape(r' & \text{of the continuity plate}  \end{aligned}'))
    else:
        weld_fu_eqn.append(NoEscape(r'& \text{Note: Provide weld on one side}  \\'))
        weld_fu_eqn.append(NoEscape(r'& \text{of the continuity plate}  \end{aligned}'))

    return weld_fu_eqn


def weld_size_cp_req(r_c, p_cw, gamma_mw, weld_length_cp, fu, weld_size_cp):

    weld_cp = Math(inline=True)
    weld_cp.append(NoEscape(r'\begin{aligned} {t_{w}}_{cp} &= \frac{ V_{cp} / 2 }{ f_{uw} k {L_{w}}_{cp} } \times \sqrt{3} \gamma_{mw} \\'))
    weld_cp.append(NoEscape(r' &= \frac{R_{c} - P_{cw}}{2 \times f_{uw} k {L_{w}}_{cp}} \times \sqrt{3} \gamma_{mw} \\'))
    weld_cp.append(NoEscape(r' &= \frac{('+str(r_c) +r' - '+str(p_cw)+r') \times 10^{3}}{2 \times '+str(fu)+r' \times 0.7 \times '
                            +str(weld_length_cp)+r'} \times \sqrt{3} \times '+str(gamma_mw)+r' \\'))
    weld_cp.append(NoEscape(r'&= ' + str(weld_size_cp) + r' \\ \\'))
    weld_cp.append(NoEscape(r'[Ref.&~IS~800:2007,~Cl.~10.5.7]\end{aligned}'))

    return weld_cp


def weld_fu_provided(weld_fu):
    weld_fu_eqn = Math(inline=True)

    weld_fu_eqn.append(NoEscape(r'\begin{aligned} f_{u_w} &= ' + str(weld_fu) + r' \end{aligned}'))
    return weld_fu_eqn


def weld_length_web_prov(beam_D, beam_tf, beam_r1, L_weld):
    beam_D = str(beam_D)
    beam_r1 = str(beam_r1)
    beam_tf = str(beam_tf)
    L_weld = str(L_weld)
    weld_length_web_prov = Math(inline=True)

    weld_length_web_prov.append(NoEscape(r'\begin{aligned} L_{w} &= 2 \times \big[D - (2 \times T) - (2 \times R1) - 20 \big] \\'))
    weld_length_web_prov.append(NoEscape(r'&= 2 \times \big['+beam_D+r' - (2 \times '+beam_tf+r') - (2 \times'+beam_r1+r') - 20 \big] \\'))
    weld_length_web_prov.append(NoEscape(r' &= ' + L_weld+ r' \\ \\'))
    weld_length_web_prov.append(NoEscape(r' & \text{Note: Weld is provided on both sides of the web} \end{aligned}'))

    return weld_length_web_prov


def tension_critical_bolt_prov(M, t_ba, n_c, r_1, n_r, r_i, n, r_3, r_4, type=''):
    M= str(M)
    t_ba = str(t_ba)
    n_c = str(n_c)
    r_1 = str(r_1)
    n_r = str(n_r)
    r_i = str(r_i)
    r_3 = str(float(r_3))
    r_4 = str(float(r_4))

    tension_critical_bolt_prov = Math(inline=True)

    if type == 'Flushed - Reversible Moment':
        tension_critical_bolt_prov.append(NoEscape(r'\begin{aligned} T_{1} &= \frac{M_{ue}} '
                                                   r'{n_c \times \Bigg(r_1 + \displaystyle\sum_{i = 2} ^ {n_r} \frac{r_i ^2}{r_1}\Bigg) }\\'))
        tension_critical_bolt_prov.append(NoEscape(r'&= \frac{'+ M + r' \times 10^{3}} '
                         r'{'+n_c+ r'\times \Bigg('+ r_1 +' + \displaystyle\sum_{i=2} ^ {'+ n_r +r'} \frac{r_i ^2}{'+ r_1 +r'}\Bigg) } \\'))

    elif type == 'Extended One Way - Irreversible Moment':
        if (n == 3) or (n == 4):
            i = 3
            i = str(i)
            tension_critical_bolt_prov.append(NoEscape(r'\begin{aligned} T_{1} &= \frac{M_{ue}}'
                                                       r'{2 \times n_c \times \Bigg(r_1 + \displaystyle\sum_{i = 3} ^ {n_r} \frac{r_i ^2}{r_1}\Bigg) }\\'))
            tension_critical_bolt_prov.append(NoEscape(r'&= \frac{' + M + r' \times 10^{3}} {2 \times'
                                                       + n_c + r'\times \Bigg(' + r_1 + ' + \displaystyle\sum_{i=' + i + '} ^ {'
                                                       + n_r + r'} \frac{r_i ^2}{' + r_1 + r'}\Bigg) }\\'))
        elif n == 5:
            multi = 4
            i = 3
            i = str(i)
            multi = str(multi)

            tension_critical_bolt_prov.append(NoEscape(r'\begin{aligned} T_{1} &= \frac{M_{ue}}{4 \times n_c \times '
                                                       r'\Bigg(r_1 + \displaystyle\sum_{i = 3} ^ {n_r = 3} \frac{r_i ^2}{r_1}\Bigg)}\\'))
            tension_critical_bolt_prov.append(NoEscape(r' &= \frac{' + M + r' \times 10^{3}}{4 \times ' + n_c + r' \times '
                                                       r'\Bigg(' + r_1 + r' + \displaystyle\sum_{i = 3} ^ {n_r = 3} \frac{r_i ^2}{'
                                                       + r_1 + r'}\Bigg)}\\'))

        elif n >= 6:
            i = 6
            i = str(i)
            r_3 = str(r_3)
            tension_critical_bolt_prov.append(NoEscape(r'\begin{aligned} T_{1} &= \frac{M_{ue}}'
                                                       r'{4 \times n_c \times \Bigg(r_1 + \frac{r_3^2}{r_1} + \displaystyle\sum_{i = 6} ^ {n_r} '
                                                       r'\frac{r_i ^2}{r_1}\Bigg) }\\'))
            tension_critical_bolt_prov.append(NoEscape(r'&= \frac{' + M + r'\times 10^{3}}{4 \times' + n_c + r'\times \Bigg(' + r_1 + r' + \frac{'
                                                       + r_3 +'^2}{'+r_1+'} +\displaystyle\sum_{i=' + i + '} ^ {' + n_r + r'} \frac{r_i ^2}{'
                                                       + r_1 + r'}\Bigg) }\\'))
    else:
        # if (n == 4) or (n == 6):
        if n < 8:
            i = 4
            i = str(i)
            tension_critical_bolt_prov.append(NoEscape(r'\begin{aligned} T_{1} &= \frac{M_{ue}}'
                                                       r'{2 \times n_c \times \Bigg(r_1 + \displaystyle\sum_{i = 4} ^ {n_r} \frac{r_i ^2}{r_1}\Bigg) }\\'))
            tension_critical_bolt_prov.append(NoEscape(r'&= \frac{' + M + r'\times 10^{3}}{2 \times' + n_c + r'\times \Bigg('
                                                       + r_1 + ' + \displaystyle\sum_{i=' + i + '} ^ {' + n_r + r'} \frac{r_i ^2}{'
                                                       + r_1 + r'}\Bigg) }\\'))
        elif n >= 8:
            i = 8
            i = str(i)
            r_3 = str(r_3)
            tension_critical_bolt_prov.append(NoEscape(r'\begin{aligned} T_{1} &= \frac{M_{ue}}{4 \times n_c \times '
                                                       r'\Bigg(r_1 + \frac{r_4^2}{r_1} + '
                                                       r'\displaystyle\sum_{i = 8} ^ {n_r}\frac{r_i ^2}{r_1}\Bigg) } \\'))
            tension_critical_bolt_prov.append(NoEscape(r' &= \frac{' + M + r'\times 10^{3}}{4 \times ' + n_c + r' \times '
                                                       r'\Bigg(' + r_1 + r' + \frac{' + r_4 + r'^2}{' + r_1 + r'} + '
                                                       r'\displaystyle\sum_{i = ' + i + r'} ^ {' + n_r + r'}\frac{r_i ^2}{' + r_1 + r'}\Bigg) }\\'))

    tension_critical_bolt_prov.append(NoEscape(r' &= ' + t_ba + r' \\ \\'))

    tension_critical_bolt_prov.append(NoEscape(r' & \text{Note: } T_{1} \text{ is the tension in the critical bolt.}  \\'))
    tension_critical_bolt_prov.append(NoEscape(r' & \text{The critical bolt is the bolt nearest} \\'))
    tension_critical_bolt_prov.append(NoEscape(r' & \text{to the tension flange.} \end{aligned}'))

    return tension_critical_bolt_prov


def req_para_end_plate(e, beam_r1, l_v, beam_bf, n_c, r_sum, b_e, bolt_fu, bolt_proof_stress):
    e = str(e)
    beam_r1 = str(beam_r1)
    l_v = str(l_v)
    beam_bf = str(beam_bf)
    n_c = str(n_c)
    r_sum = str(r_sum)
    b_e = str(b_e)
    bolt_fu = str(bolt_fu)
    bolt_proof_stress = str(bolt_proof_stress)

    req_para_end_plate = Math(inline=True)
    req_para_end_plate.append(NoEscape(r'\begin{aligned} l_v &= e~-~ \frac{R_1}{2} \\'))
    req_para_end_plate.append(NoEscape(r'&= '+e+r'~-~ \frac{'+beam_r1+r'}{2} \\'))
    req_para_end_plate.append(NoEscape(r'&= ' + l_v + r' \\ \\'))

    req_para_end_plate.append(NoEscape(r'b_e &= \frac{B}{n_c}\\'))
    req_para_end_plate.append(NoEscape(r'&= \frac{'+beam_bf+'}{'+n_c+r'}\\'))
    req_para_end_plate.append(NoEscape(r'&= '+ b_e + r' \\ \\'))

    req_para_end_plate.append(NoEscape(r' f_{o} &= 0.7 \times f_{ub} \\'))
    req_para_end_plate.append(NoEscape(r' &= 0.7 \times '+ bolt_fu + r' \\'))
    req_para_end_plate.append(NoEscape(r' &= '+ bolt_proof_stress + r' \end{aligned}'))

    return req_para_end_plate


def cl_10_4_6_friction_bolt_combined_shear_and_tension(V_sf, V_df, T_f, T_df, value):  # Todo:not done
    """
    Check for bolt subjected to combined shear and tension
    Args:
        V_sb - factored shear force acting on the bolt,
        V_db - design shear capacity,
        T_b - factored tensile force acting on the bolt,
        T_db - design tension capacity.
    Returns:
        combined shear and friction value
    Note:
        Reference:
        IS 800:2007,  cl 10.3.6
    """
    V_sf = str(V_sf)
    V_df = str(V_df)
    T_f = str(T_f)
    T_df = str(T_df)
    value = str(value)

    combined_capacity_eqn = Math(inline=True)
    combined_capacity_eqn.append(NoEscape(r'\begin{aligned} \bigg(\frac{V_{sf}}{V_{df}}\bigg)^2 & + \bigg(\frac{T_{f}}{T_{df}}\bigg)^2  \leq 1.0\\'))
    combined_capacity_eqn.append(NoEscape(r' \bigg(\frac{' + V_sf + '}{' + V_df + r'}\bigg)^2 & + \bigg(\frac{' + T_f + '}{' + T_df + r'}\bigg)^2 = '
                                          + value + r'\\ \\'))
    combined_capacity_eqn.append(NoEscape(r' & [\text{Ref. IS 800:2007, Cl.10.3.6}] \end{aligned}'))

    return combined_capacity_eqn


def moment_ep(t_1,lv,Q,le,mp_plate):
    t_1 =str(t_1)
    lv =str(lv)
    Q =str(Q)
    le =str(le)
    mp_plate =str(mp_plate)

    moment_ep_eqn = Math(inline=True)
    moment_ep_eqn.append(NoEscape(r'\begin{aligned} M_{cr} &= T_{1}~ l_{v} - Q ~l_{e} \\'))
    moment_ep_eqn.append(NoEscape(r'&= ('+t_1+ r' \times '+lv+' - '+Q+ r'\times '+le+r') \times 10^{-3} \\'))
    moment_ep_eqn.append(NoEscape(r'&= ' + mp_plate + r' \\ \\'))
    moment_ep_eqn.append(NoEscape(r'& \text{Note: The critical section is at the toe of the weld or} \\'))
    moment_ep_eqn.append(NoEscape(r'& \text{the edge of the flange from bolt center-line} \end{aligned}'))

    return moment_ep_eqn


def weld_size_ep_web_req(load_shear, gamma_mw, weld_length_web, fu, weld_size_web):
    load_shear=str(load_shear)
    gamma_mw =str(gamma_mw)
    weld_length_web =str(weld_length_web)
    fu =str(fu)
    weld_size_web=str( weld_size_web)

    weld_size_ep_web_req_eqn = Math(inline=True)
    weld_size_ep_web_req_eqn.append(NoEscape(r'\begin{aligned} t_{w} &= \frac{V_{u}}{f_{uw} k L_{w}} \times \sqrt{3}~ \gamma_{mw} \\'))
    weld_size_ep_web_req_eqn.append(NoEscape(r' &= \frac{'+load_shear+r' \times 10^{3}}{'+fu+r' \times 0.7 \times '+
                                             weld_length_web+r'} \times \sqrt{3} \times ' +gamma_mw+r' \\'))
    weld_size_ep_web_req_eqn.append(NoEscape(r'&= ' + weld_size_web + r' \\ \\'))
    weld_size_ep_web_req_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.5.7}] \end{aligned}'))

    return weld_size_ep_web_req_eqn


def max_weld_size_ep_web_prov(weld_size_web, max_size):
    weld_size_web = str(weld_size_web)
    max_size = str(max_size)

    weld_size_ep_web_prov_eqn = Math(inline=True)
    weld_size_ep_web_prov_eqn.append(NoEscape(r'\begin{aligned} t_w & \leq {t_{w}}_{\max} \\'))
    weld_size_ep_web_prov_eqn.append(NoEscape(r' ' + weld_size_web + r' & \leq ' + max_size + r' \end{aligned}'))

    return weld_size_ep_web_prov_eqn


def min_weld_size_ep_web_prov(weld_size_web, weld_size_web_provided, min_size):
    weld_size_ep_web_prov_eqn = Math(inline=True)
    weld_size_ep_web_prov_eqn.append(NoEscape(r'\begin{aligned} t_w & = \max(t_{w}, ~{t_{w}}_{\min}) \\'))
    weld_size_ep_web_prov_eqn.append(NoEscape(r' & = \max(' + str(weld_size_web) + r', ~' + str(min_size) + r') \\'))
    weld_size_ep_web_prov_eqn.append(NoEscape(r' & = ' + str(weld_size_web_provided) + r' \end{aligned}'))

    return weld_size_ep_web_prov_eqn
# >>>>>>> 1a4f41f957c3004664005ff81dea375296b3a6fd

def local_web_yielding(f_wc,k,t_fb,gamma_mo,column_tf , column_r1,column_fy,column_tw,P_bf_1):
    f_wc = str(f_wc)
    k = str(round(k, 2))
    t_fb = str(t_fb)
    gamma_mo = str(gamma_mo)
    column_tf = str(column_tf)
    column_r1 = str(column_r1)
    column_fy = str(column_fy)
    column_tw = str(column_tw)
    P_bf_1 = str(P_bf_1)

    local_web_yielding_eqn = Math(inline=True)
    local_web_yielding_eqn.append(NoEscape(r'\begin{aligned} P_{cw_1} &= \frac{f_{wc}~(5k +T_b)}{\gamma_{m0}} \\ \\'))

    local_web_yielding_eqn.append(NoEscape(r'k &= T_c  + {R_{1}}_{c}\\'))
    local_web_yielding_eqn.append(NoEscape(r' &= '+column_tf+' +' +column_r1+r'\\'))
    local_web_yielding_eqn.append(NoEscape(r' &= ' + k+ r'\\ \\'))

    local_web_yielding_eqn.append(NoEscape(r' f_{wc} &= f_{yc} t_c \\'))
    local_web_yielding_eqn.append(NoEscape(r' &= '+column_fy +r'\times' +column_tw+r' \\'))
    local_web_yielding_eqn.append(NoEscape(r' &= ' + f_wc+ r' \\ \\'))

    local_web_yielding_eqn.append(NoEscape(r' P_{cw_1}&= \frac{'+f_wc+ r' \times ((5 \times '+k+') +'+t_fb+')}{'+gamma_mo+r' \times 1000}\\'))
    local_web_yielding_eqn.append(NoEscape(r' &= ' + P_bf_1 + r' \\ \\'))
    local_web_yielding_eqn.append(NoEscape(r' & \text{Note: subscript c denotes column section, and,} \\'))
    local_web_yielding_eqn.append(NoEscape(r' & \text{subscript b denotes beam section} \end{aligned}'))

    return local_web_yielding_eqn


def compression_buckling_of_web(t_c,fy_c, h_c,k, gamma_mo, D_c , P_cw_2):
    t_c = str(t_c)
    h_c = str(h_c)
    fy_c = str(fy_c)
    gamma_mo = str(gamma_mo)
    k = str(k)
    D_c = str(D_c)
    P_cw_2 = str(P_cw_2)
    compression_buckling_of_web_eqn = Math(inline=True)
    compression_buckling_of_web_eqn.append(NoEscape(r'\begin{aligned} P_{cw_2} &= 10710 ~ \Big( \frac{t_c^3}{h_c} \Big) ~ '
                                                    r'\sqrt\frac{f_{yc}}{\gamma_{m0}} \\ \\'))

    compression_buckling_of_web_eqn.append(NoEscape(r'h_c &= D_c -(2 k)\\'))
    compression_buckling_of_web_eqn.append(NoEscape(r'&= '+D_c+ r' -(2 \times '+k+r')\\'))
    compression_buckling_of_web_eqn.append(NoEscape(r' &= ' + h_c + r'\\ \\'))

    compression_buckling_of_web_eqn.append(NoEscape(r' P_{cw_2}&= 10710 \times \frac{'+t_c+'^3}{'+h_c+r'} \times \sqrt\frac{'+fy_c+r'}{'
                                                    +gamma_mo+r'} \times 10^{-3}\\'))
    compression_buckling_of_web_eqn.append(NoEscape(r' &= ' + P_cw_2 + r'\end{aligned}'))
    return compression_buckling_of_web_eqn


def web_cripling(t_c,fy_c,T_b, gamma_m1, D_c , P_cw_3,T_c):
    t_c = str(t_c)
    T_b = str(T_b)
    fy_c = str(fy_c)
    gamma_m1 = str(gamma_m1)
    T_c = str(T_c)
    D_c = str(D_c)
    P_cw_3 = str(P_cw_3)
    web_cripling_eqn = Math(inline=True)
    web_cripling_eqn.append(NoEscape(r'\begin{aligned} P_{cw_3} &= \Bigg(\frac{300 t_c^2}{\gamma_{m1}}\Bigg) '
                                     r'\Bigg[1+ 3 \Big(T_{\text{b}} / D_{c} \Big) \Big(t_{c} / T_{c} \Big)^{1.5} \Bigg] '
                                     r'\sqrt{f_{yc} \Big(T_c / t_{c}\Big)}  \\ \\'))

    web_cripling_eqn.append(NoEscape(r' &= \Bigg(\frac{300 \times '+t_c+r'^2}{'+gamma_m1+r'}\Bigg) \times '
                                     r'\Bigg[1+ 3 \times \Big('+T_b+r' / '+D_c+r' \Big) \times \\ \\'))

    web_cripling_eqn.append(NoEscape(r' & \Big('+t_c+r' / '+T_c+r' \Big)^{1.5} \Bigg] \times \sqrt{'+fy_c+r' \times \Big('+T_c+r' / '+t_c+r'\Big)}  \times 10^{-3} \\ \\'))

    web_cripling_eqn.append(NoEscape(r' &= ' + P_cw_3 + r' \end{aligned}'))
    return web_cripling_eqn


def compressioncheck(P_cw_1,P_cw_3,P_cw_2,P_bf):
    P_cw_1 = str(P_cw_1)
    P_cw_2 = str(P_cw_2)
    P_cw_3 = str(P_cw_3)
    P_bf = str(P_bf)
    compressioncheck_eqn = Math(inline=True)
    compressioncheck_eqn.append(NoEscape(r'\begin{aligned} P_{cw} &= \min(P_{cw_1},~P_{cw_2},~P_{cw_3}) \\'))
    compressioncheck_eqn.append(NoEscape(r'  &= \min(' + P_cw_1 + r', ~' + P_cw_2 + r', ~' + P_cw_3+ r') \\'))
    compressioncheck_eqn.append(NoEscape(r' &= ' + P_bf + r'\end{aligned}'))
    return compressioncheck_eqn


def continuity_plate_req_1(R_c):
    check_1 = Math(inline=True)
    check_1.append(NoEscape(r'\begin{aligned} R_{c} &= ' + str(R_c) + r'\end{aligned}'))

    return check_1


def continuity_plate_req_2(r_c, p_cw):
    check_2 = Math(inline=True)
    check_2.append(NoEscape(r'\begin{aligned} P_{cw} &= ' + str(p_cw) + r' \end{aligned}'))

    return check_2


def comp_plate_length(l_cp1,l_cp2,D_c,T_c,n):
    l_cp1 = str(l_cp1)
    l_cp2 = str(l_cp2)
    D_c = str(D_c)
    T_c = str(T_c)
    n = str(n)
    comp_plate_length_eqn = Math(inline=True)
    comp_plate_length_eqn.append(NoEscape(r'\begin{aligned} l_{cp1} &= \text{Outer length} \\ \\'))
    comp_plate_length_eqn.append(NoEscape(r'l_{cp1} &= D_c -2 T_c\\'))
    comp_plate_length_eqn.append(NoEscape(r' &= '+D_c+ r'- (2 \times'+ T_c+r') \\'))
    comp_plate_length_eqn.append(NoEscape(r' &= ' + l_cp1  + r'\\ \\'))

    comp_plate_length_eqn.append(NoEscape(r' l_{cp2} &= \text{Inner length} \\ \\'))
    comp_plate_length_eqn.append(NoEscape(r'l_{cp2} &= D_c -2(T_c+n)\\'))
    comp_plate_length_eqn.append(NoEscape(r'&= '+D_c+r' - \big[2 \times ('+T_c+'+'+n+r')\big] \\'))
    comp_plate_length_eqn.append(NoEscape(r' &= ' + l_cp2  + r'\end{aligned}'))
    return comp_plate_length_eqn


def comp_plate_width(column_bf,column_tw,notch_size,w_cp):
    column_bf = str(column_bf)
    column_tw = str(column_tw)
    notch_size = str(notch_size)
    w_cp = str(w_cp)
    comp_plate_width_eqn = Math(inline=True)
    comp_plate_width_eqn.append(NoEscape(r'\begin{aligned} w_{cp} &= \frac{B_c - T_c - 2n}{2}\\'))
    comp_plate_width_eqn.append(NoEscape(r' &=\frac{'+column_bf+'- '+column_tw+r' - 2 \times '+notch_size+r'}{2}\\'))
    comp_plate_width_eqn.append(NoEscape(r' &= ' + w_cp + r'\end{aligned}'))
    return comp_plate_width_eqn


def comp_plate_thk_p(A_cp, w_cp, l_cp, t_cp1, f_ycp, t_cp2, t_cp3, epsilon_cp, t_cp, beam_tf):
    A_cp = str(A_cp)
    w_cp = str(w_cp)
    l_cp = str(l_cp)
    t_cp1 = str(t_cp1)
    f_ycp = str(f_ycp)
    t_cp2 = str(t_cp2)
    t_cp3 = str(t_cp3)
    epsilon_cp = str(epsilon_cp)
    t_cp = str(t_cp)
    beam_tf = str(beam_tf)

    comp_plate_thk_p_eqn = Math(inline=True)
    comp_plate_thk_p_eqn.append(NoEscape(r'\begin{aligned}  t_{cp1} &= \text{Minimum area criteria} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r'                 t_{cp1} &= \frac{A_{cp} / 2}{w_{cp}} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r'                         &= \frac{'+A_cp+r' / 2}{'+w_cp+r'} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r' &= '+t_cp1+r'\\ \\'))

    comp_plate_thk_p_eqn.append(NoEscape(r't_{cp2} &= \text{Limiting b/t ratio criteria} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r't_{cp2} &= \frac{ l_{cp1} }{29.3 ~\epsilon_{cp}} \\ \\'))

    comp_plate_thk_p_eqn.append(NoEscape(r'\epsilon_{cp} &= \sqrt\frac{250}{{f_{y}}_{cp}} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r'&= \sqrt\frac{250}{'+f_ycp+ r'} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r' &= '+epsilon_cp+ r' \\ \\'))

    comp_plate_thk_p_eqn.append(NoEscape(r' &= \frac{ '+l_cp+r' }{29.3 \times '+epsilon_cp+r'} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r' &= ' + t_cp2 + r'\\ \\'))

    comp_plate_thk_p_eqn.append(NoEscape(r't_{cp3} &= \text{Minimum thickness criteria} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r't_{cp3} &= T_{\text{b}} \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r'&= '+beam_tf+r' \\ \\'))

    comp_plate_thk_p_eqn.append(NoEscape(r't_{cp} &= \max(t_{cp1},~t_{cp2},~t_{cp3} ) \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r' &= \max('+t_cp1+','+t_cp2+','+t_cp3+ r') \\'))
    comp_plate_thk_p_eqn.append(NoEscape(r' &= ' + t_cp + r' \end{aligned}'))

    return comp_plate_thk_p_eqn


def ten_plate_thk_p(A_cp, w_cp, t_cp1,  t_cp2, t_cp, compression_cont_status):
    A_cp = str(A_cp)
    w_cp = str(w_cp)
    t_cp1 = str(t_cp1)
    # f_ycp = str(f_ycp)
    t_cp2 = str(t_cp2)
    # t_cp3 = str(t_cp3)
    # epsilon_cp = str(epsilon_cp)
    t_cp = str(t_cp)
    # beam_tf = str(beam_tf)
    ten_plate_thk_p_eqn = Math(inline=True)

    if compression_cont_status == True:
        ten_plate_thk_p_eqn.append(NoEscape(r'\begin{aligned}  t_{st1} &= \text{Minimum area criteria} \\'))
        ten_plate_thk_p_eqn.append(NoEscape(r'  t_{st1} &= \frac{A_{cp} / 2}{w_{cp}} \\'))
        ten_plate_thk_p_eqn.append(NoEscape(r' &= \frac{'+A_cp+r' / 2}{'+w_cp+r'} \\'))
        ten_plate_thk_p_eqn.append(NoEscape(r' &= ' + t_cp1 + r'\\ \\'))

        ten_plate_thk_p_eqn.append(NoEscape(r't_{st2} &= \text{Minimum thickness criteria} \\'))
        ten_plate_thk_p_eqn.append(NoEscape(r't_{st2} &= T_{\text{b}}\\'))
        ten_plate_thk_p_eqn.append(NoEscape(r' &= ' + t_cp2 + r'\\ \\'))

        ten_plate_thk_p_eqn.append(NoEscape(r't_{\text{st}} &= \max(t_{st1},~t_{st2} )\\'))
        ten_plate_thk_p_eqn.append(NoEscape(r' &= \max(' + t_cp1 + ',~' + t_cp2 + r')\\'))
        ten_plate_thk_p_eqn.append(NoEscape(r' &= ' + t_cp + r'\end{aligned}'))
    else:
        ten_plate_thk_p_eqn.append(NoEscape(r'\begin{aligned} t_{\text{st}} &= \text{Minimum thickness criteria} \\'))
        ten_plate_thk_p_eqn.append(NoEscape(r't_{\text{st}} &= T_{\text{b}}\\'))
        ten_plate_thk_p_eqn.append(NoEscape(r' &= ' + t_cp2 + r'\\ '))
        ten_plate_thk_p_eqn.append(NoEscape(r' &= ' + t_cp + r'\end{aligned}'))

    return ten_plate_thk_p_eqn


def Area_req_cont_plate(A_cp, R_c,p_cw,f_ycp,gamma_m0):
    A_cp = str(A_cp)
    R_c = str(R_c)
    p_cw = str(p_cw)
    f_ycp = str(f_ycp)
    gamma_m0 = str(gamma_m0)


    Area_req_cont_plate_eqn = Math(inline=True)
    Area_req_cont_plate_eqn.append(NoEscape(r'\begin{aligned}  A_{cp} &= \frac{R_c  - P_{cw}}{ {f_{y}}_{cp} \gamma_{m0} }\\'))
    Area_req_cont_plate_eqn.append(NoEscape(r' &= \frac{ \big('+R_c+'  - '+p_cw+r' \big) \times 10^{3}}{'+f_ycp+r'\times '+gamma_m0+r' }\\'))
    Area_req_cont_plate_eqn.append(NoEscape(r' &= ' + A_cp + r'\end{aligned}'))
    return Area_req_cont_plate_eqn


def check_tension_flange(beam_bf, beam_tf,gamma_m0,t_bf):
    beam_bf = str(beam_bf)
    beam_tf = str(beam_tf)
    gamma_m0 = str(gamma_m0)
    t_bf = str(t_bf)

    check_tension_flange_eqn = Math(inline=True)
    check_tension_flange_eqn.append(NoEscape(r'\begin{aligned} &= 0.4 \sqrt\frac{B_b T_b}{\gamma_{m0}} \\'))
    check_tension_flange_eqn.append(NoEscape(r' &= 0.4 \sqrt\frac{'+beam_bf+r' \times ' +beam_tf+r'}{' +gamma_m0+r'} \\'))
    check_tension_flange_eqn.append(NoEscape(r' &= ' + t_bf + r'\end{aligned}'))
    return check_tension_flange_eqn


def checkdiagonal_plate(M,D_c,D_b,fyc,t_req):
    M = str(M)
    D_c = str(D_c)
    D_b = str(D_b)
    fyc = str(fyc)
    t_req = str(t_req)
    checkdiagonal_plate_eqn = Math(inline=True)
    checkdiagonal_plate_eqn.append(NoEscape(r'\begin{aligned}  t_{wc} &= \frac{1.9 M_{ue}}{D_c D_b f_{yc}} \\'))
    checkdiagonal_plate_eqn.append(NoEscape(r'&= \frac{1.9 \times'+ M+'}{'+D_c +r' \times '+D_b+r' \times' + fyc+r'}\\'))
    checkdiagonal_plate_eqn.append(NoEscape(r' &= ' + t_req + r'\end{aligned}'))
    return checkdiagonal_plate_eqn


def load_diag_stiffener(M,D_c,D_b,fyc,p_st,tc,gamma):
    M = str(M)
    D_c = str(D_c)
    D_b = str(D_b)
    fyc = str(fyc)
    p_st = str(p_st)
    tc = str(tc)
    gamma = str(gamma)
    # p_st = str(p_st)
 # self.load_diag_stiffener = ((self.load_moment_effective * 1e6 / self.beam_D) - (
 #                        (self.column_fy * self.column_tw * self.column_D) /
 #                        (math.sqrt(3) * self.gamma_m0))) * 1e-3

    load_diag_stiffener_eqn = Math(inline=True)
    load_diag_stiffener_eqn.append(NoEscape(r'\begin{aligned}  p_{st} &= \frac{M \times 10^6}{D_b} - \frac{fyc \times t_c \times  D_c }{\sqrt(3) \times  \gamma_{m0}}  \times 10^{-3} \\'))
    load_diag_stiffener_eqn.append(NoEscape(r'&= \frac{'+M+ r'\times 10^6}{'+D_b+r'} - \frac{'+fyc+r' \times' +tc+ r'\times'  +D_c+r'}{\sqrt(3) \times  '+gamma+r'}  \times 10^{-3} \\'))
    load_diag_stiffener_eqn.append(NoEscape(r' &= ' +  p_st + r'\end{aligned}'))
    return load_diag_stiffener_eqn

def Area_req_dia_plate(A_st,fy_st,p_st,gamma):
    A_st = str(A_st)
    fy_st = str(fy_st)
    p_st = str(p_st)

    gamma = str(gamma)
    Area_req_dia_plate_eqn = Math(inline=True)
    Area_req_dia_plate_eqn.append(NoEscape(r'\begin{aligned}  A_{st} &= p_{st} \Big( \frac{\gamma_{m0}}{f_{yst} \times cos(45)} \Big)\\'))
    Area_req_dia_plate_eqn.append(NoEscape(r'&= '+p_st+ r'\Big( \frac{'+gamma+'}{'+fy_st+r'\times cos(45)} \Big)\\'))
    Area_req_dia_plate_eqn.append(NoEscape(r' &= ' +  A_st + r'\end{aligned}'))
    return Area_req_dia_plate_eqn


def web_stiffener_plate_depth(depth, D_b, T_b, r1_b):

    web_stiffener_plate_depth_eqn = Math(inline=True)
    web_stiffener_plate_depth_eqn.append(NoEscape(r'\begin{aligned}  D_{st} &= D_{b} - (2 T_{\text{b}}) - (2 {R_{1}}_{b}) - 20 \\'))
    web_stiffener_plate_depth_eqn.append(NoEscape(r'  &= ' + str(D_b) + r' - (2 \times ' + str(T_b) + r') - (2 \times ' + str(r1_b) + r') - 20 \\'))
    web_stiffener_plate_depth_eqn.append(NoEscape(r'  &= ' + str(depth) + r' \end{aligned}'))
    return web_stiffener_plate_depth_eqn


def bc_ep_compatibility_req(beam_B, B_req):

    compatibility_eqn = Math(inline=True)
    compatibility_eqn.append(NoEscape(r'\begin{aligned}  B_\text{req} &= B_{b} + 25 \\'))
    compatibility_eqn.append(NoEscape(r'                         &= ' + str(beam_B) + r' + 25 \\'))
    compatibility_eqn.append(NoEscape(r'                         &= ' + str(B_req) + r' \\'))
    compatibility_eqn.append(NoEscape(r'                          \end{aligned}'))

    return compatibility_eqn


def web_stiffener_plate_width(width, D_c, T_c, r1_c):

    web_stiffener_plate_width_eqn = Math(inline=True)

    web_stiffener_plate_width_eqn.append(NoEscape(r'\begin{aligned}  W_{st} &= D_{c} - (2 T_{c}) - (2 {R_{1}}_{c}) - 20 \\'))
    web_stiffener_plate_width_eqn.append(NoEscape(r'  &= ' + str(D_c) + r' - (2 \times ' + str(T_c) + r') - (2 \times ' + str(r1_c) + r') - 20 \\'))
    web_stiffener_plate_width_eqn.append(NoEscape(r'  &= ' + str(width) + r' \end{aligned}'))

    return web_stiffener_plate_width_eqn


def web_stiffener_plate_thk(t_wc, t_c, thk_req):
    web_stiffener_plate_thk_eqn = Math(inline=True)

    web_stiffener_plate_thk_eqn.append(NoEscape(r'\begin{aligned}  t_{\text{st}} &= \frac{t_{wc} - t_{c}} {2} \\'))
    web_stiffener_plate_thk_eqn.append(NoEscape(r'  &= \frac{' + str(t_wc) + r' - ' + str(t_c) + r'} {2} \\'))
    web_stiffener_plate_thk_eqn.append(NoEscape(r'  &= ' + str(thk_req) + r' \end{aligned}'))

    return web_stiffener_plate_thk_eqn



def bc_ep_compatibility_available(col_D, col_B, col_T, col_R1, space_available, connectivity):

    compatibility_eqn = Math(inline=True)

    if connectivity == CONN_CFBW:
        compatibility_eqn.append(NoEscape(r'\begin{aligned}  B_\text{available} &= B_{c} \\'))
        compatibility_eqn.append(NoEscape(r'                         &= ' + str(col_B) + r' \end{aligned}'))
    else:
        compatibility_eqn.append(NoEscape(r'\begin{aligned}  B_{available} &= D_{c} - (2 T_{c}) - (2 {R_{1}}_{c}) - 10 \\'))
        compatibility_eqn.append(NoEscape(r'                               &= ' + str(col_D) + r' - (2 \times ' + str(col_T) + r') - (2 \times '
                                          + str(col_R1) + r') - 10 \\'))
        compatibility_eqn.append(NoEscape(r'                         &= ' + str(space_available) + r' \\ \\'))
        compatibility_eqn.append(NoEscape(r'                         & \end{aligned}'))  # line left blank purposely

    return compatibility_eqn


def axial_compression_prov(P, col_capa, provided_capa):

    axial_compression_prov_eqn = Math(inline=True)
    axial_compression_prov_eqn.append(NoEscape(r'\begin{aligned}  P_{u} &= \max(P_{\text{x}},~0.3 P_{\text{d}}),~\text{but},~ \leq P_{\text{d}} \\'))
    axial_compression_prov_eqn.append(NoEscape(r'                   &= \max(' + str(P) + r',~0.3 \times ' + str(col_capa) + r') \\'))
    axial_compression_prov_eqn.append(NoEscape(r'                   &= \max(' + str(P) + r',~ ' + str(round(0.3 * col_capa, 2)) + r') \\'))
    axial_compression_prov_eqn.append(NoEscape(r'                   & \leq ' + str(col_capa) + r' \\'))
    axial_compression_prov_eqn.append(NoEscape(r'                   &= ' + str(provided_capa) + r' \\ \\'))

    axial_compression_prov_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.10.7}] \\ \\'))

    axial_compression_prov_eqn.append(NoEscape(r' \text{Note: } & P_{\text{d}} \text{ is the design axial capacity of the column} \end{aligned}'))

    return axial_compression_prov_eqn


def display_load_bp(load_val, notation=''):

    display_eqn = Math(inline=True)
    display_eqn.append(NoEscape(r'\begin{aligned} ' + str(notation) + ' &= ' + str(load_val) + r' \end{aligned}'))

    return display_eqn


def prov_moment_load_bp(moment_input, min_mc, app_moment_load, moment_capacity, axis='', classification=''):

    app_moment_load_eqn = Math(inline=True)

    if axis == 'Major':
        app_moment_load_eqn.append(NoEscape(r'\begin{aligned} {M_{\text{z}}}_{\text{min}} &= 0.5 * {M_{d}}_{\text{z}} \\'))
    else:
        app_moment_load_eqn.append(NoEscape(r'\begin{aligned} {M_{y}}_{\text{min}} &= 0.5 * {M_{d}}_{\text{y}} \\'))

    app_moment_load_eqn.append(NoEscape(r'&= 0.5 \times ' + str(moment_capacity) + r' \\'))
    app_moment_load_eqn.append(NoEscape(r'&=' + str(min_mc) + r' \\ \\'))

    if axis == 'Major':
        app_moment_load_eqn.append(NoEscape(r'{M_{u}}_{\text{z}} &= \max(M_z,~{M_{\text{z}}}_{\text{min}}),~\text{but}, \leq {M_{d}}_{\text{z}} \\'))
    else:
        app_moment_load_eqn.append(NoEscape(r'{M_{u}}_{\text{y}} &= \max(M_y,~{M_{y}}_{\text{min}}),~\text{but}, \leq {M_{d}}_{\text{y}} \\'))

    app_moment_load_eqn.append(NoEscape(r'&= \max(' + str(moment_input) + r',~' + str(min_mc) + r') \\'))
    app_moment_load_eqn.append(NoEscape(r'& \leq ' + str(moment_capacity) + r' \\'))
    app_moment_load_eqn.append(NoEscape(r'&= ' + str(app_moment_load) + r' \\ \\'))

    if classification == 'Semi-compact':
        app_moment_load_eqn.append(NoEscape(r'& \text{Note: The column is classified as semi-compact.} \\ \\'))
    else:
        app_moment_load_eqn.append(NoEscape(r'& \text{Note: The column is classified as compact.} \\ \\'))

    app_moment_load_eqn.append(NoEscape(r'& [\text{Ref. IS 800:2007, Cl.8.2.1.2}] \end{aligned}'))

    return app_moment_load_eqn
# def dia_plate_thk_provided(t_wc,)
#     t_wc
# t_wc = round((1.9 * self.load_moment_effective * 1e6) / (self.column_D * self.beam_D * self.column_fy), 2)