from builtins import str
import time
import math
from Common import *
import os
import pdfkit
import configparser
# from utils.common import component
from pylatex import Document, Section, Subsection
from pylatex.utils import italic, bold
#import pdflatex
import sys
import datetime
#from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject


from pylatex import Document, Section, Subsection, Tabular, Tabularx,MultiColumn
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic, NoEscape
#from pdflatex import PDFLaTeX
import os
from pylatex import Document, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number
from pylatex.utils import bold

def min_pitch(d):
    min_pitch = 2.5*d
    d = str(d)
    min_pitch = str(min_pitch)

    min_pitch_eqn = Math(inline=True)
    min_pitch_eqn.append(NoEscape(r'\begin{aligned}p/g_{min}&= 2.5 ~ d&\\'))
    min_pitch_eqn.append(NoEscape(r'=&2.5*' + d + r'&=' + min_pitch + r'\end{aligned}'))
    return min_pitch_eqn

def max_pitch(t):

    max_pitch_1 = 32*min(t)
    max_pitch_2 = 300
    max_pitch = max(max_pitch_1,max_pitch_2)
    t = str(min(t))
    max_pitch = str(max_pitch)


    max_pitch_eqn = Math(inline=True)
    max_pitch_eqn.append(NoEscape(r'\begin{aligned}p/g_{max} &=\min(32~t,~300~mm)&\\'))
    max_pitch_eqn.append(NoEscape(r'&=\min(32 *~' + t+ r',~ 300 ~mm)\\&='+max_pitch+r'\end{aligned}'))
    return max_pitch_eqn

def min_edge_end(d_0,edge_type):
    if edge_type == 'a - Sheared or hand flame cut':
        factor = 1.7
    else:
        factor = 1.5
    min_edge_dist = round(factor * d_0,2)

    min_edge_dist = str(min_edge_dist)

    factor = str(factor)
    d_0 = str(d_0)

    min_end_edge_eqn = Math(inline=True)
    min_end_edge_eqn.append(NoEscape(r'\begin{aligned}e/e`_{min} &=[1.5~or~ 1.7] * d_0\\'))
    min_end_edge_eqn.append(NoEscape(r'&='+factor + r'*' + d_0+r'='+min_edge_dist+r' \end{aligned}'))
    return min_end_edge_eqn

def max_edge_end(f_y,t):

    epsilon = round(math.sqrt(250/f_y),2)
    max_edge_dist = round(12*t*epsilon,2)
    max_edge_dist = str(max_edge_dist)
    t = str(t)
    f_y = str(f_y)

    max_end_edge_eqn = Math(inline=True)
    max_end_edge_eqn.append(NoEscape(r'\begin{aligned}e/e`_{max} &= 12~ t~ \varepsilon&\\'))
    max_end_edge_eqn.append(NoEscape(r'\varepsilon &= \sqrt{\frac{250}{f_y}}\\'))
    max_end_edge_eqn.append(NoEscape(r'e/e`_{max}&=12 ~*'+ t + r'*\sqrt{\frac{250}{'+f_y+r'}}\\ &='+max_edge_dist+r'\\ \end{aligned}'))
    return max_end_edge_eqn

def bolt_shear_prov(f_ub,n_n,a_nb,gamma_mb,bolt_shear_capacity):
    f_ub = str(f_ub)
    n_n = str(n_n)
    a_nb = str(a_nb)
    gamma_mb= str(gamma_mb)
    bolt_shear_capacity=str(bolt_shear_capacity)
    bolt_shear_eqn = Math(inline=True)
    bolt_shear_eqn.append(NoEscape(r'\begin{aligned}V_{dsb} &= \frac{f_{ub} ~n_n~ A_{nb}}{\sqrt{3} ~\gamma_{mb}}\\'))
    bolt_shear_eqn.append(NoEscape(r'&= \frac{'+f_ub+'*'+n_n+'*'+a_nb+'}{\sqrt{3}~*~'+ gamma_mb+r'}\\'))
    bolt_shear_eqn.append(NoEscape(r'&= '+bolt_shear_capacity+r'\end{aligned}'))
    return bolt_shear_eqn

def bolt_bearing_prov(k_b,d,conn_plates_t_fu_fy,gamma_mb,bolt_bearing_capacity):
    t_fu_prev = conn_plates_t_fu_fy[0][0] * conn_plates_t_fu_fy[0][1]
    t = conn_plates_t_fu_fy[0][0]
    f_u = conn_plates_t_fu_fy[0][1]
    for i in conn_plates_t_fu_fy:
        t_fu = i[0] * i[1]
        if t_fu <= t_fu_prev:
            t = i[0]
            f_u = i[1]
    k_b = str(k_b)
    d = str(d)
    t = str(t)
    f_u= str(f_u)
    gamma_mb=str(gamma_mb)
    bolt_bearing_capacity = str(bolt_bearing_capacity)
    bolt_bearing_eqn = Math(inline=True)
    bolt_bearing_eqn.append(NoEscape(r'\begin{aligned}V_{dpb} &= \frac{2.5~ k_b~ d~ t~ f_u}{\gamma_{mb}}\\'))
    bolt_bearing_eqn.append(NoEscape(r'&= \frac{2.5~*'+ k_b+'*'+ d+'*'+t+'*'+f_u+'}{'+gamma_mb+r'}\\'))
    bolt_bearing_eqn.append(NoEscape(r'&='+bolt_bearing_capacity+r'\end{aligned}'))

    return bolt_bearing_eqn


def bolt_capacity_prov(bolt_shear_capacity,bolt_bearing_capacity,bolt_capacity):
    bolt_shear_capacity = str(bolt_shear_capacity)
    bolt_bearing_capacity = str(bolt_bearing_capacity)
    bolt_capacity = str(bolt_capacity)
    bolt_capacity_eqn = Math(inline=True)
    bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{db} &= min~ (V_{dsb}, V_{dpb})\\'))
    bolt_capacity_eqn.append(NoEscape(r'&= min~ ('+bolt_shear_capacity+','+ bolt_bearing_capacity+r')\\'))
    bolt_capacity_eqn.append(NoEscape(r'&='+ bolt_capacity+r'\end{aligned}'))

    return bolt_capacity_eqn


def HSFG_bolt_capacity_prov(mu_f,n_e,K_h,fub,Anb,gamma_mf,capacity):
    mu_f = str(mu_f)
    n_e = str(n_e)
    K_h = str(K_h)
    fub = str(fub)
    Anb = str(Anb)
    gamma_mf = str(gamma_mf)
    capacity = str(capacity)

    HSFG_bolt_capacity_eqn = Math(inline=True)
    HSFG_bolt_capacity_eqn.append(NoEscape(r'\begin{aligned}V_{dsf} & = \frac{\mu_f~ n_e~  K_h~ F_o}{\gamma_{mf}}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'& Where, F_o = 0.7 * f_{ub} A_{nb}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'V_{dsf} & = \frac{'+ mu_f + '*' + n_e + '*' + K_h +'* 0.7 *' +fub+'*'+Anb +r'}{'+gamma_mf+r'}\\'))
    HSFG_bolt_capacity_eqn.append(NoEscape(r'& ='+capacity+r'\end{aligned}'))

    return HSFG_bolt_capacity_eqn

def get_trial_bolts(V_u, A_u,bolt_capacity,multiple=1):
    res_force = math.sqrt(V_u**2+ A_u**2)
    trial_bolts = multiple * math.ceil(res_force/bolt_capacity)
    V_u=str(V_u)
    A_u=str(A_u)
    bolt_capacity=str(bolt_capacity)
    trial_bolts=str(trial_bolts)
    trial_bolts_eqn = Math(inline=True)
    trial_bolts_eqn.append(NoEscape(r'\begin{aligned}R_{u} &= \sqrt{V_u^2+A_u^2}\\'))
    trial_bolts_eqn.append(NoEscape(r'n_{trial} &= R_u/ V_{bolt}\\'))
    trial_bolts_eqn.append(NoEscape(r'R_{u} &= \frac{\sqrt{'+V_u+r'^2+'+A_u+r'^2}}{'+bolt_capacity+ r'}\\'))
    trial_bolts_eqn.append(NoEscape(r'&='+trial_bolts+ r'\end{aligned}'))
    return trial_bolts_eqn

def parameter_req_bolt_force(bolts_one_line,gauge,ymax,xmax,bolt_line,pitch,length_avail):
    """
       bolts_one_line =n_r
       bolt_line = n_c
       """
    bolts_one_line = str(bolts_one_line)
    ymax = str(ymax)
    xmax = str(xmax)
    gauge = str(gauge)
    pitch = str(pitch)
    bolt_line = str(bolt_line)
    length_avail = str(length_avail)

    parameter_req_bolt_force_eqn = Math(inline=True)
    parameter_req_bolt_force_eqn.append(NoEscape(r'\begin{aligned} l_n~~~ &= length~available \\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' l_n~~~ &= (n_r - 1) * g\\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' &= ('+bolts_one_line+' - 1) *'+ gauge+ r'\\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' & ='+length_avail+ r'\\'))

    parameter_req_bolt_force_eqn.append(NoEscape(r' y_{max} &= l_n / 2\\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' &= '+length_avail+ r' / 2 \\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' & =' + ymax + r'\\'))

    parameter_req_bolt_force_eqn.append(NoEscape(r'x_{max} &= p * (n_c - 1) / 2 \\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' &= '+pitch+' * ('+bolt_line+ r'- 1) / 2 \\'))
    parameter_req_bolt_force_eqn.append(NoEscape(r' & =' + xmax + r'\end{aligned}'))

    return parameter_req_bolt_force_eqn

def moment_demand_req_bolt_force(bolts_one_line,bolt_line,shear_load,
               web_moment,moment_demand,ecc):
    bolts_one_line = str(bolts_one_line)
    bolt_line = str(bolt_line)
    ecc = str(ecc)
    web_moment = str(web_moment)
    moment_demand = str(moment_demand)
    shear_load = str(shear_load)
    loads_req_bolt_force_eqn = Math(inline=True)

    loads_req_bolt_force_eqn.append(NoEscape(r'\begin{aligned}  M_d~~ &= (V_u * ecc + M_w)\\'))
    loads_req_bolt_force_eqn.append(NoEscape(r' &= ('+shear_load+' * '+ecc+' + '+web_moment+r')\\'))
    loads_req_bolt_force_eqn.append(NoEscape(r' & =' + moment_demand + r'\end{aligned}'))
    return loads_req_bolt_force_eqn

def Vres_bolts(bolts_one_line,ymax,xmax,bolt_line,axial_load
               ,moment_demand,r,vbv,tmv,tmh,abh,vres,shear_load): #vres bolt web
    """
    bolts_one_line =n_r
    bolt_line = n_c
    """
    bolts_one_line =str(bolts_one_line)
    ymax =str(ymax)
    xmax =str(xmax)
    bolt_line = str(bolt_line)

    r = str(r)
    moment_demand = str(moment_demand)
    axial_load =str(axial_load)
    shear_load = str(shear_load)
    vbv =str(vbv)
    tmv =str(tmv)
    tmh =str(tmh)
    abh =str(abh)
    vres = str(vres)
    Vres_bolts_eqn = Math(inline=True)

    Vres_bolts_eqn.append(NoEscape(r'\begin{aligned} vbv~~ &= V_u / (n_r * n_c)\\'))
    Vres_bolts_eqn.append(NoEscape(r' &= \frac{'+shear_load+ '}{ ('+bolts_one_line +'*'+ bolt_line+r')}\\'))
    Vres_bolts_eqn.append(NoEscape(r' & =' + vbv + r'\\'))

    Vres_bolts_eqn.append(NoEscape(r'tmh~ &= \frac{M_d * y_{max} }{ \Sigma r_i^2} \\'))
    Vres_bolts_eqn.append(NoEscape(r' &= \frac{'+moment_demand+' *'+ ymax+'}{'+r+r'}\\'))
    Vres_bolts_eqn.append(NoEscape(r' & =' + tmh + r'\\'))

    Vres_bolts_eqn.append(NoEscape(r' tmv ~&= \frac{M_d * x_{max}}{\Sigma r_i^2}\\'))
    Vres_bolts_eqn.append(NoEscape(r'&= \frac{' +moment_demand+' * '+xmax+'}{'+r+ r'}\\'))
    Vres_bolts_eqn.append(NoEscape(r' & =' + tmv + r'\\'))

    Vres_bolts_eqn.append(NoEscape(r' abh~ & = \frac{A_u }{(n_r * n_c)}\\'))
    Vres_bolts_eqn.append(NoEscape(r'  & =\frac{'+axial_load+'}{ ('+bolts_one_line+' *' +bolt_line+r')}\\'))
    Vres_bolts_eqn.append(NoEscape(r' & =' + abh + r'\\'))
    Vres_bolts_eqn.append(NoEscape(r' vres &=\sqrt{(vbv +tmv) ^ 2 + (tmh+abh) ^ 2}\\'))
    # Vres_bolts_eqn.append(NoEscape(r' vres &= \sqrt((vbv + tmv) ^ 2 + (tmh + abh) ^ 2)\\'))
    Vres_bolts_eqn.append(NoEscape(r'  &= \sqrt{('+vbv+' +'+ tmv+') ^2 + ('+tmh +'+'+ abh+r') ^ 2}\\'))
    Vres_bolts_eqn.append(NoEscape(r' & =' + vres +  r'\end{aligned}'))

    return Vres_bolts_eqn

def forces_in_web(Au,T,A,t,D,Zw,Mu,Z,Mw,Aw):
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

    forcesinweb_eqn.append(NoEscape(r'\begin{aligned}A_w &= Axial~ force~ in~ web  \\'))
    forcesinweb_eqn.append(NoEscape(r'  &= \frac{(D- 2*T)*t* Au }{A} \\'))
    forcesinweb_eqn.append(NoEscape(r'&= \frac{(' + D + '- 2*' + T + ')*' + t + '*' + Au + ' }{' + A + r'} \\'))
    forcesinweb_eqn.append(NoEscape(r'&=' + Aw + r'\\'))
    forcesinweb_eqn.append(NoEscape( r'M_w &= Moment ~in ~web  \\'))
    forcesinweb_eqn.append(NoEscape(r' &= \frac{Z_w * Mu}{Z} \\'))
    forcesinweb_eqn.append(NoEscape(r'&= \frac{' + Zw + ' * ' + Mu + '}{' + Z + r'} \\'))
    forcesinweb_eqn.append(NoEscape(r'&=' + Mw + r'\end{aligned}'))
    return forcesinweb_eqn

def forces_in_flange(Au, B,T,A,D,Mu,Mw,Mf,Af,ff):
    Au =str(Au)
    B=str(B)
    T=str(T)
    A=str(A)
    D=str(D)
    Mu=str(Mu)
    Mw=str(Mw)
    Mf=str(Mf)
    Af=str(Af)
    ff = str(ff)
    forcesinflange_eqn= Math(inline=True)
    forcesinflange_eqn.append(NoEscape(r'\begin{aligned} A_f&= Axial~force~ in ~flange  \\'))
    forcesinflange_eqn.append(NoEscape(r'&= \frac{Au * B *T}{A} \\'))
    forcesinflange_eqn.append(NoEscape(r'&= \frac{' + Au + ' * ' + B + '*' + T + '}{' + A + r'} \\'))
    forcesinflange_eqn.append(NoEscape(r'&=' + Af + r'\\'))
    forcesinflange_eqn.append(NoEscape(r'M_f& =Moment~ in~ flange \\'))
    forcesinflange_eqn.append(NoEscape(r' & = Mu-M_w\\'))
    forcesinflange_eqn.append(NoEscape(r'&= ' + Mu + '-' + Mw + r'\\'))
    forcesinflange_eqn.append(NoEscape(r'&=' + Mf + r'\\'))
    forcesinflange_eqn.append(NoEscape(r' F_f& =flange~force  \\'))
    forcesinflange_eqn.append(NoEscape(r'& = \frac{M_f *1000}{D-T} + A_f \\'))
    forcesinflange_eqn.append(NoEscape(r'&= \frac{' + Mf + '}{' + D + '-' + T + '} +' + Af + r' \\'))
    forcesinflange_eqn.append(NoEscape(r'&=' + ff + r'\end{aligned}'))
    return forcesinflange_eqn

def min_plate_ht_req(beam_depth,min_plate_ht):
    beam_depth = str(beam_depth)
    min_plate_ht = str(min_plate_ht)
    min_plate_ht_eqn = Math(inline=True)
    min_plate_ht_eqn.append(NoEscape(r'\begin{aligned}0.6 * d_b&= 0.6 * '+ beam_depth + r'='+min_plate_ht+r'\end{aligned}'))
    return min_plate_ht_eqn

def min_flange_plate_ht_req(beam_width,min_flange_plate_ht):## when only outside plate is considered
    beam_width = str(beam_width)
    min_flange_plate_ht = str(min_flange_plate_ht)
    min_flange_plate_ht_eqn = Math(inline=True)
    min_flange_plate_ht_eqn.append(NoEscape(r'\begin{aligned}min~flange~plate~ht &= beam~width\\'))
    min_flange_plate_ht_eqn.append(NoEscape(r'&='+min_flange_plate_ht+r'\end{aligned}'))

    return min_flange_plate_ht_eqn

def min_inner_flange_plate_ht_req(beam_width, web_thickness,root_radius,min_inner_flange_plate_ht): ## when inside and outside plate is considered #todo
    beam_width = str(beam_width) ### same function used for max height
    min_inner_flange_plate_ht = str(min_inner_flange_plate_ht)
    web_thickness=str(web_thickness)
    root_radius=str(root_radius)
    min_inner_flange_plate_ht_eqn = Math(inline=True)
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'\begin{aligned}&= \frac{B -t- (2*R1)}{2}\\'))
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'&=\frac{'+beam_width+ r' -' +web_thickness+ r' - 2*'+ root_radius+r'}{2}\\'))
    min_inner_flange_plate_ht_eqn.append(NoEscape(r'&='+min_inner_flange_plate_ht+r'\end{aligned}'))

    return min_inner_flange_plate_ht_eqn


def max_plate_ht_req(connectivity,beam_depth, beam_f_t, beam_r_r, notch, max_plate_h):
    beam_depth = str(beam_depth)
    beam_f_t = str(beam_f_t)
    beam_r_r = str(beam_r_r)
    max_plate_h = str(max_plate_h)
    notch = str(notch)
    max_plate_ht_eqn = Math(inline=True)
    if connectivity in VALUES_CONN_1:
        max_plate_ht_eqn.append(NoEscape(r'\begin{aligned} &d_b - 2 (t_{bf} + r_{b1} + gap)\\'))
        max_plate_ht_eqn.append(NoEscape(r'&='+beam_depth+ '- 2* (' + beam_f_t + '+' + beam_r_r +r'+ 10)\\'))
    else:
        max_plate_ht_eqn.append(NoEscape(r'\begin{aligned} &d_b - t_{bf} + r_{b1} - notch_h\\'))
        max_plate_ht_eqn.append(NoEscape(r'&=' + beam_depth + '-' + beam_f_t + '+' + beam_r_r + '-'+ notch+ r'\\'))
    max_plate_ht_eqn.append(NoEscape(r'&=' + max_plate_h + '\end{aligned}'))
    return max_plate_ht_eqn

def min_plate_length_req(min_pitch, min_end_dist,bolt_line,min_length):
    min_pitch = str(min_pitch)
    min_end_dist = str(min_end_dist)
    bolt_line = str(bolt_line)
    min_length = str(min_length)
    min_plate_length_eqn = Math(inline=True)
    min_plate_length_eqn.append(NoEscape(r'\begin{aligned} &2*e_{min} + (n~c-1) * p_{min})\\'))
    min_plate_length_eqn.append(NoEscape(r'&=2*' + min_end_dist + '+(' + bolt_line + '-1) * ' + min_pitch + r'\\'))
    min_plate_length_eqn.append(NoEscape(r'&=' + min_length + '\end{aligned}'))
    return min_plate_length_eqn

def min_flange_plate_length_req(min_pitch, min_end_dist,bolt_line,min_length,gap):
    min_pitch = str( min_pitch)
    min_end_dist = str(min_end_dist)
    bolt_line = str(bolt_line)
    min_length = str(min_length)
    gap = str(gap)
    min_flange_plate_length_eqn = Math(inline=True)
    min_flange_plate_length_eqn.append(NoEscape(r'\begin{aligned} & 2[2*e_{min} + ({\frac{bolt~lines}{2}}-1) * p_{min})]\\'))
    min_flange_plate_length_eqn.append(NoEscape(r'& +\frac{gap}{2}]\\'))
    min_flange_plate_length_eqn.append(NoEscape(r'&=2*[(2*' + min_end_dist +r' + (\frac{'+bolt_line+r'}{2}' + r'-1) * ' + min_pitch + r'\\'))
    min_flange_plate_length_eqn.append(NoEscape(r'&= + \frac{'+gap+r'}{2}]\\'))

    min_flange_plate_length_eqn.append(NoEscape(r'&=' + min_length + '\end{aligned}'))
    return min_flange_plate_length_eqn

def min_plate_thk_req(t_w):
    t_w = str(t_w)
    min_plate_thk_eqn = Math(inline=True)
    min_plate_thk_eqn.append(NoEscape(r'\begin{aligned} t_w='+t_w+'\end{aligned}'))
    return min_plate_thk_eqn

def shear_yield_prov(h,t, f_y, gamma, V_dg):
    h = str(h)
    t = str(t)
    f_y = str(f_y)
    gamma = str(gamma)
    V_dg = str(V_dg)
    shear_yield_eqn = Math(inline=True)
    shear_yield_eqn.append(NoEscape(r'\begin{aligned} V_{dg} &= \frac{A_v*f_y}{\sqrt{3}*\gamma_{mo}}\\'))
    shear_yield_eqn.append(NoEscape(r'&=\frac{'+h+'*'+t+'*'+f_y+'}{\sqrt{3}*'+gamma+r'}\\'))
    shear_yield_eqn.append(NoEscape(r'&=' + V_dg + '\end{aligned}'))
    return shear_yield_eqn

def shear_rupture_prov(h, t, n_r, d_o, fu,v_dn,multiple =1):
    h = str(h)
    t = str(t)
    n_r = str(n_r)
    d_o = str(d_o)
    f_u = str(fu)
    v_dn = str(v_dn)
    multiple = str(multiple)
    shear_rup_eqn = Math(inline=True)
    shear_rup_eqn.append(NoEscape(r'\begin{aligned} V_{dn} &= \frac{0.75*A_{vn}*f_u}{\sqrt{3}*\gamma_{mo}}\\'))
    shear_rup_eqn.append(NoEscape(r'&='+multiple+ r'*('+h+'-('+n_r+'*'+d_o+'))*'+t+'*'+f_u+r'\\'))
    shear_rup_eqn.append(NoEscape(r'&=' + v_dn + '\end{aligned}'))
    return shear_rup_eqn

def shear_capacity_prov(V_dy, V_dn, V_db):
    V_d = min(V_dy,V_dn,V_db)
    V_d = str(V_d)
    V_dy = str(V_dy)
    V_dn = str(V_dn)
    V_db = str(V_db)
    shear_capacity_eqn = Math(inline=True)
    shear_capacity_eqn.append(NoEscape(r'\begin{aligned} V_d &= Min(V_{dy},V_{dn},V_{db})\\'))
    shear_capacity_eqn.append(NoEscape(r'&= Min('+V_dy+','+V_dn+','+V_db+r')\\'))
    shear_capacity_eqn.append(NoEscape(r'&='+V_d + '\end{aligned}'))
    return shear_capacity_eqn

def tension_yield_prov(l,t, f_y, gamma, T_dg):
    l = str(l)
    t = str(t)
    f_y = str(f_y)
    gamma = str(gamma)
    T_dg = str(T_dg)
    tension_yield_eqn = Math(inline=True)
    tension_yield_eqn.append(NoEscape(r'\begin{aligned} T_{dg} &= \frac{l*t_p*f_y}{\gamma_{mo}}\\'))
    tension_yield_eqn.append(NoEscape(r'&=\frac{'+l+'*'+t+'*'+f_y+'}{'+gamma+r'}\\'))
    tension_yield_eqn.append(NoEscape(r'&=' + T_dg + '\end{aligned}'))
    return tension_yield_eqn

def height_of_flange_cover_plate(B,sp,b_fp): #weld
    B = str(B)
    sp = str(sp)
    b_fp = str (b_fp)
    height_for_flange_cover_plate_eqn =Math(inline=True)
    height_for_flange_cover_plate_eqn.append(NoEscape(r'\begin{aligned} b_{fp} &= {B - 2*sp} \\'))
    height_for_flange_cover_plate_eqn.append(NoEscape(r'&= {' + B + ' - 2 * ' + sp + r'} \\'))
    height_for_flange_cover_plate_eqn.append(NoEscape(r'&=' + b_fp + '\end{aligned}'))
    return height_for_flange_cover_plate_eqn

def inner_plate_height_weld(B,sp,t_w,r_1, b_ifp):#weld
    B = str(B)
    sp = str(sp)
    t_w = str (t_w)
    r_1 = str(r_1)
    b_ifp = str(b_ifp)
    inner_plate_height_weld_eqn =Math(inline=True)
    inner_plate_height_weld_eqn.append(NoEscape(r'\begin{aligned} b_{ifp} &= \frac{B - 4*sp - t_w - 2*r_1}{2} \\'))
    inner_plate_height_weld_eqn.append(NoEscape(r'&= \frac{'+B +'- 4*'+sp+'-' +t_w+ '- 2*'+r_1+r'} {2} \\'))
    inner_plate_height_weld_eqn.append(NoEscape(r'&=' + b_ifp + '\end{aligned}'))
    return inner_plate_height_weld_eqn


def flange_plate_Length_req(l_w,s,g,l_fp): #weld
    l_w = str(l_w)
    s = str (s)
    g = str (g)
    l_fp = str(l_fp)
    min_flange_plate_Length_eqn = Math(inline=True)
    min_flange_plate_Length_eqn.append(NoEscape(r'\begin{aligned} l_{fp} & = [2*(l_{w} + 2*s) + g]\\'))
    min_flange_plate_Length_eqn.append(NoEscape(r'&= [2*('+ l_w + '2*'+s+') +' + g+ r']\\'))
    min_flange_plate_Length_eqn.append(NoEscape(r'&=' + l_fp + '\end{aligned}'))
    return min_flange_plate_Length_eqn

def flange_weld_stress(F_f,F_rl,F_ws):
    F_rl = str(F_rl)
    F_ws = str(F_ws)
    F_f =str(F_f)
    flange_weld_stress_eqn = Math(inline=True)
    flange_weld_stress_eqn.append(NoEscape(r'\begin{aligned} Stress &= \frac{F_f*1000}{F_{rl}}\\'))
    flange_weld_stress_eqn.append(NoEscape(r' &= \frac{' + F_f + '*1000}{' + F_rl + r'}\\'))
    flange_weld_stress_eqn.append(NoEscape(r'&= ' + F_ws + r'\end{aligned}'))

    return flange_weld_stress_eqn

def tension_rupture_bolted_prov(w_p, t_p, n_c, d_o, fu,gamma_m1,T_dn):

    w_p = str(w_p)
    t_p = str(t_p)
    n_c = str(n_c)
    d_o = str(d_o)
    f_u = str(fu)
    T_dn = str(T_dn)
    gamma_m1 = str(gamma_m1)
    Tensile_rup_eqnb = Math(inline=True)
    Tensile_rup_eqnb.append(NoEscape(r'\begin{aligned} T_{dn} &= \frac{0.9*A_{n}*f_u}{\gamma_{m1}}\\'))
    Tensile_rup_eqnb.append(NoEscape(r'&=\frac{0.9*('+w_p+'-'+n_c+'*'+d_o+')*'+t_p+'*'+f_u+r'}{'+gamma_m1+r'}\\'))
    Tensile_rup_eqnb.append(NoEscape(r'&=' + T_dn + '\end{aligned}'))
    return Tensile_rup_eqnb

def tension_rupture_welded_prov(w_p, t_p, fu,gamma_m1,T_dn):
    w_p = str(w_p)
    t_p = str(t_p)
    f_u = str(fu)
    T_dn = str(T_dn)
    gamma_m1 = str(gamma_m1)
    Tensile_rup_eqnw = Math(inline=True)
    Tensile_rup_eqnw.append(NoEscape(r'\begin{aligned} T_{dn} &= \frac{0.9*A_{n}*f_u}{\gamma_{m1}}\\'))
    Tensile_rup_eqnw.append(NoEscape(r'&=\frac{0.9*'+w_p+'*'+t_p+'*'+f_u+r'}{'+gamma_m1+r'}\\'))
    Tensile_rup_eqnw.append(NoEscape(r'&=' + T_dn + '\end{aligned}'))
    return Tensile_rup_eqnw

def tensile_capacity_prov(T_dg, T_dn, T_db =0.0):

    tension_capacity_eqn = Math(inline=True)
    if T_db != 0.0:
        T_d = min(T_dg,T_dn,T_db)
        T_d = str(T_d)
        T_dg = str(T_dg)
        T_dn = str(T_dn)
        T_db = str(T_db)
        tension_capacity_eqn.append(NoEscape(r'\begin{aligned} T_d &= Min(T_{dg},T_{dn},T_{db})\\'))
        tension_capacity_eqn.append(NoEscape(r'&= Min(' + T_dg + ',' + T_dn + ',' + T_db + r')\\'))
    else:
        T_d = min(T_dg, T_dn)
        T_dg = str(T_dg)
        T_dn = str(T_dn)
        T_d = str(T_d)
        tension_capacity_eqn.append(NoEscape(r'\begin{aligned} T_d &= Min(T_{dg},T_{dn})\\'))
        tension_capacity_eqn.append(NoEscape(r'&= Min(' + T_dg + ',' + T_dn + r')\\'))



    tension_capacity_eqn.append(NoEscape(r'&='+ T_d + '\end{aligned}'))
    return tension_capacity_eqn


def mom_axial_IR_prov(M,M_d,N,N_d,IR):
    M = str(M)
    M_d = str(M_d)
    N = str(N)
    N_d = str(N_d)
    IR = str(IR)
    mom_axial_IR_eqn = Math(inline=True)
    mom_axial_IR_eqn.append(NoEscape(r'\begin{aligned} \frac{'+M+'}{'+M_d+r'}+\frac{'+N+'}{'+N_d+'}='+IR+r'\end{aligned}'))
    return mom_axial_IR_eqn

def IR_req(IR):
    IR = str(IR)
    IR_req_eqn = Math(inline=True)
    IR_req_eqn.append(NoEscape(r'\begin{aligned} \leq'+IR+'\end{aligned}'))
    return IR_req_eqn

def min_weld_size_req(conn_plates_weld,min_weld_size):
    t1 = str(conn_plates_weld[0])
    t2 = str(conn_plates_weld[0])
    tmax = str(max(conn_plates_weld))
    weld_min = str(min_weld_size)

    min_weld_size_eqn = Math(inline=True)
    min_weld_size_eqn.append(NoEscape(r'\begin{aligned} &Thickness~of~Thicker~part\\'))
    min_weld_size_eqn.append(NoEscape(r'\noindent &=max('+t1+','+t2+r')\\'))
    min_weld_size_eqn.append(NoEscape(r'&='+tmax+r'\\'))
    min_weld_size_eqn.append(NoEscape(r'&IS800:2007~cl.10.5.2.3~Table 21,\\'))
    min_weld_size_eqn.append(NoEscape(r' &t_{w_{min}}=' + weld_min + r'\end{aligned}'))
    return min_weld_size_eqn


def min_weld_size_req_01(conn_plates_weld, red, min_weld_size):
    # t1 = str(conn_plates_weld[0])
    # t2 = str(conn_plates_weld[0])
    tmax = min(conn_plates_weld)
    tmin = int (tmax - red)
    tmin = str(tmin)
    tmax= str(int(tmax))
    weld_min = str(min_weld_size)

    min_weld_size_eqn = Math(inline=True)
    min_weld_size_eqn.append(NoEscape(r'\begin{aligned} & t_{w_{min}}~based~on~thinner~part\\'))
    min_weld_size_eqn.append(NoEscape(r'& ='+tmax+ '~or~' +tmin+ r'\\'))
    min_weld_size_eqn.append(NoEscape(r'& IS800:2007~cl.10.5.2.3~Table 21\\' ))
    min_weld_size_eqn.append(NoEscape(r'& t_{w_{min}}~based~on~thicker~part=' + weld_min + r'\end{aligned}'))
    return min_weld_size_eqn

def max_weld_size_req(conn_plates_weld,max_weld_size):
    t1 = str(conn_plates_weld[0])
    t2 = str(conn_plates_weld[1])
    t_min = str(min(conn_plates_weld))
    weld_max = str(max_weld_size)

    max_weld_size_eqn = Math(inline=True)
    max_weld_size_eqn.append(NoEscape(r'\begin{aligned} & Thickness~of~Thinner~part\\'))
    max_weld_size_eqn.append(NoEscape(r'&=Min('+t1+','+t2+r')='+t_min+r'\\'))
    max_weld_size_eqn.append(NoEscape(r'&t_{w_{max}} =' + weld_max + r'\end{aligned}'))
    return max_weld_size_eqn


def weld_strength_req(V,A,M,Ip_w,y_max,x_max,l_w,R_w):
    T_wh = str(round(M * y_max/Ip_w,2))
    T_wv = str(round(M * x_max/Ip_w,2))
    V_wv = str(round(V /l_w,2))
    A_wh = str(round(A/l_w,2))

    V = str(V)
    A = str(A)
    M = str(M)
    Ip_w = str(Ip_w)
    y_max = str(y_max)
    x_max = str(x_max)
    l_w = str(l_w)
    R_w = str(R_w)
    weld_stress_eqn = Math(inline=True)
    weld_stress_eqn.append(NoEscape(r'\begin{aligned} R_w&=\sqrt{(T_{wh}+A_{wh})^2 + (T_{wv}+V_{wv})^2}\\'))
    weld_stress_eqn.append(NoEscape(r'T_{wh}&=\frac{M*y_{max}}{I{pw}}=\frac{'+M+'*'+y_max+'}{'+Ip_w+r'}\\'))
    weld_stress_eqn.append(NoEscape(r'T_{wv}&=\frac{M*x_{max}}{I{pw}}=\frac{'+M+'*'+x_max+'}{'+Ip_w+r'}\\'))
    weld_stress_eqn.append(NoEscape(r'V_{wv}&=\frac{V}{l_w}=\frac{'+V+'}{'+l_w+r'}\\'))
    weld_stress_eqn.append(NoEscape(r'A_{wh}&=\frac{A}{l_w}=\frac{'+A+'}{'+l_w+r'}\\'))
    weld_stress_eqn.append(NoEscape(r'R_w&=\sqrt{('+T_wh+'+'+A_wh+r')^2 + ('+T_wv+'+'+V_wv+r')^2}\\'))
    weld_stress_eqn.append(NoEscape(r'&='+R_w+r'\end{aligned}'))

    return weld_stress_eqn

def weld_strength_prov(conn_plates_weld_fu,gamma_mw,t_t,f_w):

    f_u = str(min(conn_plates_weld_fu))
    t_t = str(t_t)
    gamma_mw = str(gamma_mw)
    f_w = str(f_w)
    weld_strength_eqn = Math(inline=True)
    weld_strength_eqn.append(NoEscape(r'\begin{aligned} f_w &=\frac{t_t*f_u}{\sqrt{3}*\gamma_{mw}}\\'))
    weld_strength_eqn.append(NoEscape(r'&=\frac{'+t_t+'*'+f_u+'}{\sqrt{3}*'+ gamma_mw+r'}\\'))
    weld_strength_eqn.append(NoEscape(r'&='+f_w+r'\end{aligned}'))

    return weld_strength_eqn

def axial_capacity(area,fy, gamma_m0,axial_capacity): #todo anjali
    area = str(area)
    fy=str(fy)
    gamma_m0=str(gamma_m0)
    axial_capacity = str(axial_capacity)
    axial_capacity_eqn = Math(inline=True)
    axial_capacity_eqn.append(NoEscape(r'\begin{aligned} Ac &=\frac{A*f_y}{\gamma_{m0} *1000}\\'))
    axial_capacity_eqn.append(NoEscape(r'&=\frac{'+area+'*'+fy+'}{'+ gamma_m0+r'* 1000}\\'))
    axial_capacity_eqn.append(NoEscape(r'&=' + axial_capacity + r'\end{aligned}'))
    return axial_capacity_eqn

def min_axial_capacity(axial_capacity,min_ac): #todo anjali
    min_ac = str(min_ac)
    axial_capacity = str(axial_capacity)
    min_ac_eqn = Math(inline=True)
    min_ac_eqn.append(NoEscape(r'\begin{aligned} Ac_{min} &= 0.3 * A_c\\'))
    min_ac_eqn.append(NoEscape(r'&= 0.3 *' + axial_capacity + r'\\'))
    min_ac_eqn.append(NoEscape(r'&=' + min_ac + r'\end{aligned}'))
    return min_ac_eqn

def prov_axial_load(axial_input,min_ac,app_axial_load):
    min_ac = str(min_ac)
    axial_input = str(axial_input)
    app_axial_load = str(app_axial_load)
    prov_axial_load_eqn = Math(inline=True)
    prov_axial_load_eqn.append(NoEscape(r'\begin{aligned} Au &= max(A,Ac_{min} )\\'))
    prov_axial_load_eqn.append(NoEscape(r'&= max( ' + axial_input + ',' + min_ac + r')\\'))
    prov_axial_load_eqn.append(NoEscape(r'&=' + app_axial_load + r'\end{aligned}'))
    return prov_axial_load_eqn
#
def shear_capacity(h, t,f_y, gamma_m0,shear_capacity): # same as #todo anjali

    h = str(h)
    t = str(t)
    f_y = str(f_y)
    gamma_m0 = str(gamma_m0)
    shear_capacity = str(shear_capacity)
    shear_capacity_eqn = Math(inline=True)
    shear_capacity_eqn.append(NoEscape(r'\begin{aligned} S_c &= \frac{A_v*f_y}{\sqrt{3}*\gamma_{mo} *1000}\\'))
    shear_capacity_eqn.append(NoEscape(r'&=\frac{' + h + r'*' + t + r'*' + f_y + r'}{\sqrt{3}*' + gamma_m0 + r' *1000}\\'))
    shear_capacity_eqn.append(NoEscape(r'&=' + shear_capacity + r'\end{aligned}'))
    return shear_capacity_eqn
#
#
def min_shear_capacity(shear_capacity,min_sc): #todo anjali
    min_sc = str(min_sc)
    shear_capacity = str(shear_capacity)
    min_sc_eqn = Math(inline=True)
    min_sc_eqn.append(NoEscape(r'\begin{aligned} Sc_{min} &= 0.6 * A_c\\'))
    min_sc_eqn.append(NoEscape(r'&= 0.6 *' + shear_capacity +r'\\'))
    min_sc_eqn.append(NoEscape(r'&=' + min_sc + r'\end{aligned}'))
    return min_sc_eqn

def prov_shear_load(shear_input,min_sc,app_shear_load):
    min_sc = str(min_sc)
    shear_input = str(shear_input)
    app_shear_load = str(app_shear_load)
    app_shear_load_eqn = Math(inline=True)
    app_shear_load_eqn.append(NoEscape(r'\begin{aligned} Vu &= max(V,Vc_{min})\\'))
    app_shear_load_eqn.append(NoEscape(r'&=  max(' + shear_input + ',' + min_sc + r')\\'))
    app_shear_load_eqn.append(NoEscape(r'&=' + app_shear_load + r'\end{aligned}'))
    return app_shear_load_eqn


def plastic_moment_capacty(beta_b, Z_p, f_y, gamma_m0 ,Pmc):  # same as #todo anjali

    beta_b = str(beta_b)
    Z_p = str(Z_p)
    f_y = str(f_y)
    gamma_m0 =str(gamma_m0 )
    Pmc = str(Pmc)
    Pmc_eqn = Math(inline=True)
    Pmc_eqn.append(NoEscape(r'\begin{aligned} Pmc &= \frac{\beta_b * Z_p *fy}{\gamma_{mo} * 1000000}\\'))
    Pmc_eqn.append(NoEscape(r'&=\frac{' + beta_b + r'*' +Z_p + r'*' + f_y + r'}{' + gamma_m0 + r' * 1000000}\\'))
    Pmc_eqn.append(NoEscape(r'&=' + Pmc + r'\end{aligned}'))
    return Pmc_eqn

def moment_d_deformation_criteria(fy,Z_e,Mdc):
    fy = str(fy)
    Z_e = str(Z_e)
    Mdc =str(Mdc)
    Mdc_eqn= Math(inline=True)
    Mdc_eqn.append(NoEscape(r'\begin{aligned} Mdc &= \frac{1.5 *Z_e *fy}{1.1}\\'))
    Mdc_eqn.append(NoEscape(r'&= \frac{1.5 *'+Z_e + '*' +fy +r'}{1.1}\\'))
    Mdc_eqn.append(NoEscape(r'&= ' + Mdc+ r'\end{aligned}'))
    return  Mdc_eqn

def moment_capacity (Pmc , Mdc, M_c):
    Pmc = str(Pmc)
    Mdc =str(Mdc)
    M_c = str (M_c)
    M_c_eqn = Math(inline=True)
    M_c_eqn.append(NoEscape(r'\begin{aligned} M_c &= min(Pmc,Mdc)\\'))
    M_c_eqn.append(NoEscape(r'&=min('+Pmc+','+Mdc+ r')\\'))
    M_c_eqn.append(NoEscape(r'&=' + M_c + r'\end{aligned}'))
    return M_c_eqn

def min_moment_capacity(moment_capacity,min_mc): #todo anjali
    min_mc = str(min_mc)
    moment_capacity = str(moment_capacity)
    min_mc_eqn = Math(inline=True)
    min_mc_eqn.append(NoEscape(r'\begin{aligned} Mc_{min} &= 0.5 * M_c\\'))
    min_mc_eqn.append(NoEscape(r'&= 0.5 *' + moment_capacity +r'\\'))
    min_mc_eqn.append(NoEscape(r'&=' + min_mc + r'\end{aligned}'))
    return min_mc_eqn

def prov_moment_load(moment_input,min_mc,app_moment_load):
    min_mc = str(min_mc)
    moment_input = str(moment_input)
    app_moment_load = str(app_moment_load)
    app_moment_load_eqn = Math(inline=True)
    app_moment_load_eqn.append(NoEscape(r'\begin{aligned} Mu &= max(M,Mc_{min} )\\'))
    app_moment_load_eqn.append(NoEscape(r'&= max(' + moment_input + r',' + min_mc + r')\\'))
    app_moment_load_eqn.append(NoEscape(r'&=' + app_moment_load + r'\end{aligned}'))
    return  app_moment_load_eqn

def shear_rupture_prov_beam(h, t, n_r, d_o, fu,v_dn,multiple =1):
    h = str(h)
    t = str(t)
    n_r = str(n_r)
    d_o = str(d_o)
    f_u = str(fu)
    v_dn = str(v_dn)
    multiple = str(multiple)
    shear_rup_eqn = Math(inline=True)
    shear_rup_eqn.append(NoEscape(r'\begin{aligned} V_{dn} &= \frac{0.9*A_{vn}*f_u}{\sqrt{3}*\gamma_{mo}}\\'))
    shear_rup_eqn.append(NoEscape(r'&='+multiple+ r'*('+h+'-('+n_r+'*'+d_o+'))*'+t+'*'+f_u+r'\\'))
    shear_rup_eqn.append(NoEscape(r'&=' + v_dn + '\end{aligned}'))
    return shear_rup_eqn
def get_pass_fail(required, provided,relation='greater'):
    required = float(required)
    provided = float(provided)
    if provided==0:
        return 'N/A'
    else:
        if relation == 'greater':
            if required >= provided:
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
            if required <= provided:
                return 'Pass'
            else:
                return 'Fail'

def member_yield_prov(Ag, fy, gamma_m0, member_yield,multiple = 1):
    Ag = str(round(Ag,2))
    fy = str(fy)
    gamma_m0 = str(gamma_m0)
    multiple = str(multiple)
    member_yield = str(member_yield)
    member_yield_eqn = Math(inline=True)
    member_yield_eqn.append(NoEscape(r'\begin{aligned}T_{dg} &= \frac{'+ multiple + r' * A_g ~ f_y}{\gamma_{m0}}\\'))
    member_yield_eqn.append(NoEscape(r'&= \frac{'+ multiple + '*' + Ag + '*' + fy + '}{'+ gamma_m0 + r'}\\'))
    member_yield_eqn.append(NoEscape(r'&= ' + member_yield + r'\end{aligned}'))
    return member_yield_eqn

def member_rupture_prov(A_nc, A_go, F_u, F_y, L_c, w, b_s, t,gamma_m0,gamma_m1,beta,member_rup,multiple = 1):
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
    beta = str(round(beta,2))
    member_rup = str(member_rup)
    multiple = str(multiple)
    member_rup_eqn = Math(inline=True)
    member_rup_eqn.append(NoEscape(r'\begin{aligned}\beta &= 1.4 - 0.076*\frac{w}{t}*\frac{f_{y}}{f_{u}}*\frac{b_s}{L_c}\\'))
    member_rup_eqn.append(NoEscape(r'&\leq\frac{0.9*f_{u}*\gamma_{m0}}{f_{y}*\gamma_{m1}} \geq 0.7 \\'))
    member_rup_eqn.append(NoEscape(r'&= 1.4 - 0.076*\frac{'+ w +'}{'+ t + r'}*\frac{'+ fy +'}{'+ fu + r'}*\frac{'+ b_s +'}{' + L_c + r' }\\'))
    member_rup_eqn.append(NoEscape(r'&\leq\frac{0.9* '+ fu + '*'+ gamma_m0 +'}{' +fy+'*'+gamma_m1 + r'} \geq 0.7 \\'))
    member_rup_eqn.append(NoEscape(r'&= '+ beta + r'\\'))
    member_rup_eqn.append(NoEscape(r'T_{dn} &= '+multiple+'*' r'(\frac{0.9*A_{nc}*f_{u}}{\gamma_{m1}} + \frac{\beta * A_{go} * f_{y}}{\gamma_{m0}})\\'))
    member_rup_eqn.append(NoEscape(r'&= '+multiple+ r'*(\frac{0.9* '+ A_nc +'*' + fu + '}{'+ gamma_m1 + r'} + \frac{' + beta + '*' + A_go + '*' + fy + '}{' + gamma_m0 + r'})\\'))
    member_rup_eqn.append(NoEscape(r'&= '+ member_rup + r'\end{aligned}'))

    return member_rup_eqn

def blockshear_prov(Tdb,A_vg = None, A_vn = None, A_tg = None, A_tn = None, f_u = None, f_y = None ,gamma_m0 = None ,gamma_m1 = None):
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
    member_block_eqn.append(NoEscape(r'\begin{aligned}T_{db1} &= \frac{A_{vg} f_{y}}{\sqrt{3} \gamma_{m0}} + \frac{0.9 A_{tn} f_{u}}{\gamma_{m1}}\\'))
    member_block_eqn.append(NoEscape(r'T_{db2} &= \frac{0.9*A_{vn} f_{u}}{\sqrt{3} \gamma_{m1}} + \frac{A_{tg} f_{y}}{\gamma_{m0}}\\'))
    member_block_eqn.append(NoEscape(r'T_{db} &= min(T_{db1}, T_{db2})= ' + Tdb + r'\end{aligned}'))
    # member_block_eqn.append(NoEscape(r'&= \frac{' + A_vg + '*' + f_y + '}{" 1.732*' + gamma_m0 + 'r'} + &+ +'\frac{"0.9*" + A_vn + '*' + f_u + '}{'+1.732+'*' + gamma_m0 + r'} '\\'))


    return member_block_eqn

def slenderness_req():

    slenderlimit_eqn = Math(inline=True)
    slenderlimit_eqn.append(NoEscape(r'\begin{aligned}\frac{K * L}{r} &\leq 400\end{aligned}'))

    return slenderlimit_eqn

def slenderness_prov(K, L, r, slender):
    K = str(K)
    L = str(L)
    r = str(r)
    slender = str(slender)

    slender_eqn = Math(inline=True)
    slender_eqn.append(NoEscape(r'\begin{aligned}\frac{K * L}{r} &= \frac{'+K+'*'+L+'}{'+r+ r'}\\'))
    slender_eqn.append(NoEscape(r'&= ' + slender + r'\end{aligned}'))

    return slender_eqn

def efficiency_req():
    efflimit_eqn = Math(inline=True)
    efflimit_eqn.append(NoEscape(r'\begin{aligned} Efficiency &\leq 1 \end{aligned}'))

    return efflimit_eqn

def efficiency_prov(F, Td, eff):
    F = str(F)
    Td = str(round(Td/1000,2))
    eff = str(eff)
    eff_eqn = Math(inline=True)
    eff_eqn.append(NoEscape(r'\begin{aligned} Efficiency &= \frac{F}{Td}&=\frac{'+F+'}{'+Td+r'}\\'))
    eff_eqn.append(NoEscape(r'&= ' + eff + r'\end{aligned}'))

    return eff_eqn

def gusset_ht_prov(beam_depth, clearance, height, mul = 1):
    beam_depth = str(beam_depth)
    clearance = str(clearance)
    height = str(height)
    mul = str(mul)
    plate_ht_eqn = Math(inline=True)
    plate_ht_eqn.append(
        NoEscape(r'\begin{aligned} H &= '+mul+ '* Depth + clearance 'r'\\'))
    plate_ht_eqn.append(
        NoEscape(r'&=('+mul+'*' + beam_depth + ')+' + clearance + r'\\'))
    plate_ht_eqn.append(NoEscape(r'&= '  + height + r'\end{aligned}'))
    return plate_ht_eqn

def gusset_lt_b_prov(nc,p,e,length):
    nc = str(nc)
    p = str(p)
    e = str(e)
    length = str(length)
    length_htb_eqn = Math(inline=True)
    length_htb_eqn.append(
        NoEscape(r'\begin{aligned} L &= (nc -1) * p + 2 * e\\'))
    length_htb_eqn.append(
        NoEscape(r'&= ('+nc+'-1) *'+ p + '+ (2 *'+ e + r')\\'))
    length_htb_eqn.append(NoEscape(r'&= ' + length + r'\end{aligned}'))
    return length_htb_eqn

def gusset_lt_w_prov(weld,cls,length):
    weld = str(weld)
    cls = str(cls)
    length = str(length)
    length_htw_eqn = Math(inline=True)
    length_htw_eqn.append(
        NoEscape(r'\begin{aligned} L &= Flange weld + clearance 'r'\\'))
    length_htw_eqn.append(
        NoEscape(r'&= '+ weld + '+' + cls + r'\\'))
    length_htw_eqn.append(NoEscape(r'&= ' + length + r'\end{aligned}'))
    return length_htw_eqn

def long_joint_bolted_req():
    long_joint_bolted_eqn = Math(inline=True)
    long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~l\geq 15 * d~then~V_{rd} = \beta_{ij} * V_{db} \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& if~l < 15 * d~then~V_{rd} = V_{db} \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& where,\\'))
    long_joint_bolted_eqn.append(NoEscape(r'& l = ((nc~or~nr) - 1) * (p~or~g) \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& \beta_{ij} = 1.075 - l/(200 * d) \\'))
    long_joint_bolted_eqn.append(NoEscape(r'& but~0.75\leq\beta_{ij}\leq1.0 \end{aligned}'))


    return long_joint_bolted_eqn

def long_joint_bolted_prov(nc,nr,p,g,d,Tc,Tr):
    lc = (nc - 1) * p
    lr = (nr - 1) * g
    l = max(lc,lr)
    lt = 15 * d
    B = 1.075 - (l / (200 * d))
    Bi = round(B,2)
    nc= str(nc)
    nr= str(nr)
    g= str(g)
    p = str(p)
    d = str(d)
    Tc = str(Tc)
    Tr = str(Tr)
    if B<=0.75:
        B =0.75
    elif B>=1:
        B =1
    else:
        B=B
    B = str(round(B,2))
    Bi = str(Bi)
    lc_str = str(lc)
    lr_str = str(lr)
    l_str = str(l)
    lt_str = str(lt)
    long_joint_bolted_eqn = Math(inline=True)
    # long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} &if~l\leq 15 * d~then~V_{rd} = \beta_{ij} * V_{db} \\'))
    # long_joint_bolted_eqn.append(NoEscape(r'& where,\\'))
    if l < (lt):
        long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} l&= ((nc~or~nr) - 1) * (p~or~g) \\'))
        long_joint_bolted_eqn.append(NoEscape(r' &= ('+nc+' - 1) * '+p+ '='+lc_str+ r'\\'))
        long_joint_bolted_eqn.append(NoEscape(r' &= (' + nr + ' - 1) * ' + g + '=' + lr_str + r'\\'))
        long_joint_bolted_eqn.append(NoEscape(r' l&= '+ l_str + r'\\'))
        long_joint_bolted_eqn.append(NoEscape(r'& 15 * d = 15 * '+d+' = '+lt_str +r' \\'))
        long_joint_bolted_eqn.append(NoEscape(r'& since,~l < 15 * d~then~V_{rd} = V_{db} \\'))
        long_joint_bolted_eqn.append(NoEscape(r'& V_{rd} = '+Tc+r' \end{aligned}'))
    else:
        long_joint_bolted_eqn.append(NoEscape(r'\begin{aligned} l&= ((nc~or~nr) - 1) * (p~or~g) \\'))
        long_joint_bolted_eqn.append(NoEscape(r' &= (' + nc + ' - 1) * ' + p + '=' + lc_str + r'\\'))
        long_joint_bolted_eqn.append(NoEscape(r' &= (' + nr + ' - 1) * ' + g + '=' + lr_str + r'\\'))
        long_joint_bolted_eqn.append(NoEscape(r' l&= ' + l_str + r'\\'))
        long_joint_bolted_eqn.append(NoEscape(r'& 15 * d = 15 * ' + d + ' = ' + lt_str + r' \\'))
        long_joint_bolted_eqn.append(NoEscape(r'& since,~l \geq 15 * d~then~V_{rd} = \beta_{ij} * V_{db} \\'))
        long_joint_bolted_eqn.append(NoEscape(r'& \beta_{ij} = 1.075 - '+ l_str +'/(200*'+d+') ='+Bi+r'\\'))
        long_joint_bolted_eqn.append(NoEscape(r'& V_{rd} = '+B+' * '+Tc+'='+Tr+ r' \end{aligned}'))

    return long_joint_bolted_eqn

def throat_req():
    throat_eqn = Math(inline=True)
    throat_eqn.append(NoEscape(r'\begin{aligned} t_t &\geq 3 \end{aligned}'))

    return throat_eqn

def throat_prov(tw,f):
    tt = tw * f
    t_t= max(tt,3)
    tw = str(round(tw,2))
    f= str(round(f,2))
    tt = str(round(tt,2))
    t_t = str(round(t_t,2))

    throat_eqn = Math(inline=True)
    throat_eqn.append(NoEscape(r'\begin{aligned} t_t & = '+ f+'* t_w 'r'\\'))
    throat_eqn.append(NoEscape(r'& = ' + f + '*'+ tw +'='+tt+r'\\'))
    throat_eqn.append(NoEscape(r't_t & = ' + t_t + r'\end{aligned}'))

    return throat_eqn

# def eff_len_prov(l):
#     l =str(l)
#     eff_len_eqn = Math(inline=True)
#     eff_len_eqn.append(NoEscape(r'\begin{aligned} l_w &='+l+ r' \end{aligned}'))
#
#     return eff_len_eqn
#
# def diameter_prov(d):
#     d = str(d)
#     diameter_eqn = Math(inline=True)
#     diameter_eqn.append(NoEscape(r'\begin{aligned} d &=' + d + r' \end{aligned}'))
#
#     return diameter_eqn
#
# def diahole_prov(d0):
#     d0 = str(d0)
#     diahole_eqn = Math(inline=True)
#     diahole_eqn.append(NoEscape(r'\begin{aligned} d &=' + d0 + r' \end{aligned}'))

    return diahole_eqn

def display_prov(v,t):
    v = str(v)
    display_eqn = Math(inline=True)
    display_eqn.append(NoEscape(r'\begin{aligned} '+t+' &=' + v + r' \end{aligned}'))

    return display_eqn

    # slender = (float(K) * float(L)) / float(r)
    #
    # self.slenderness = round(slender, 2)
    #
    #
    # doc.generate_pdf('report_functions', clean_tex=False)


# geometry_options = {"top": "2in", "bottom": "1in", "left": "0.6in", "right": "0.6in", "headsep": "0.8in"}
# doc = Document(geometry_options=geometry_options, indent=False)
# report_bolt_shear_check(doc)
