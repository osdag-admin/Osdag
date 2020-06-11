from utils.common.is800_2007 import IS800_2007, KEY_DP_WELD_FAB_SHOP
from utils.common.material import *
from utils.common.other_standards import *
from Common import *
import sqlite3
import logging
from utils.common.material import Material
from builtins import str
from Common import *
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
from pylatex.utils import italic, NoEscape



import math
import numpy as np
from utils.common.common_calculation import *


class Bolt:

    def __init__(self, grade=None, diameter=None, bolt_type="", bolt_hole_type="Standard",
                 edge_type="a - Sheared or hand flame cut", mu_f=0.3, corrosive_influences=True, bolt_tensioning="Pretensioned"):

        if grade is not None:
            self.bolt_grade = list(np.float_(grade))
            self.bolt_grade.sort(key=float)
        if diameter is not None:
            self.bolt_diameter = list(np.float_(diameter))
            self.bolt_diameter.sort(key=float)
        self.bolt_type = bolt_type
        self.bolt_hole_type = bolt_hole_type
        self.edge_type = edge_type
        self.mu_f = float(mu_f)
        self.bolt_tensioning = bolt_tensioning

        self.d_0 = 0.0
        self.kb = 0.0

        self.kh= 0.0

        self.gamma_mb=0.0
        self.gamma_mf=0.0
        self.connecting_plates_tk = None

        self.bolt_grade_provided = 0.0
        self.bolt_diameter_provided = 0.0

        self.bolt_shank_area = 0.0
        self.bolt_net_area = 0.0

        self.bolt_shear_capacity = 0.0
        self.bolt_shear_capacity = 0.0
        self.bolt_shear_capacity = 0.0
        self.bolt_bearing_capacity = 0.0
        self.bolt_capacity = 0.0
        self.ymax = 0.0
        self.xmax = 0.0
        self.sigma_r_sq =0.0
        self.moment_demand = 0.0
        self.vres = 0.0
        self.length_avail = 0.0
        self.ecc = 0.0
        self.vbv = 0.0
        self.tmh = 0.0
        self.abh = 0.0
        self.tmv = 0.0
        self.vres = 0.0

        # self.bolt_shear_capacity_disp =round(self.bolt_shear_capacity/1000, 2)
        # self.bolt_bearing_capacity_disp = round(self.bolt_bearing_capacity/1000, 2)
        # self.bolt_capacity_disp = round(self.bolt_capacity/1000, 2)


        self.bolt_fu = 0.0
        self.bolt_fy = 0.0
        self.fu_considered = 0.0
        self.thk_considered = 0.0


        if corrosive_influences == "Yes":
            self.corrosive_influences = True
        else:
            self.corrosive_influences = False

        self.min_pitch = 0.0
        self.min_gauge = 0.0
        self.min_edge_dist = 0.0
        self.min_end_dist = 0.0
        self.max_spacing = 0.0
        self.max_edge_dist= 0.0
        self.max_end_dist = 0.0
        self.dia_hole = 0.0
        self.min_pitch_round = round_up(self.min_pitch, 5)
        self.min_gauge_round = round_up(self.min_gauge, 5)
        self.min_edge_dist_round = round_up(self.min_edge_dist, 5)
        self.min_end_dist_round = round_up(self.min_end_dist, 5)
        self.max_spacing_round = round_down(self.max_spacing, 5)
        self.max_edge_dist_round = round_down(self.max_edge_dist, 5)
        self.max_end_dist_round = round_down(self.max_end_dist, 5)

    def __repr__(self):
        repr = "Bolt\n"
        repr += "Type: {}\n".format(self.bolt_type)
        repr += "Diameter: {}\n".format(self.bolt_diameter)
        repr += "Grade: {}\n".format(self.bolt_grade)
        repr += "Diameter Provided: {}\n".format(self.bolt_diameter_provided)
        repr += "Grade Provided: {}\n".format(self.bolt_grade_provided)

        repr += "Diameter of Hole: {}\n".format(self.dia_hole)
        repr += "Minimum Pitch: {}\n".format(self.min_pitch_round)
        repr += "Minimum Gauge: {}\n".format(self.min_gauge_round)
        repr += "Minimum Edge Distance: {}\n".format(self.min_edge_dist)
        repr += "Minimum Edge Distance: {}\n".format(self.min_edge_dist)


        repr += "Minimum Edge Distance: {}\n".format(self.min_edge_dist)


        repr += "Minimum End Distance: {}\n".format(self.min_end_dist)
        repr += "Maximum Edge Distance: {}\n".format(self.max_edge_dist)
        repr += "Maximum End Distance: {}\n".format(self.max_end_dist)
        repr += "Maximum Spacing: {}\n".format(self.max_spacing)
        repr += "Bolt Shear Capacity: {}\n".format(self.bolt_shear_capacity)
        repr += "Bolt Bearing Capacity: {}\n".format(self.bolt_bearing_capacity)
        repr += "Bolt Capacity: {}\n".format(self.bolt_capacity)

        return repr

    def calculate_bolt_capacity(self, bolt_diameter_provided, bolt_grade_provided, conn_plates_t_fu_fy, n_planes,e=None,
                                p=None, seatedangle_e = 0.0):
        """

        :param bolt_type: bearing or friction grip bolt
        :param bolt_grade: grade of bolt
        :param member_fu: ultimate strength of member
        :param plate_fu: ultimate strength of plate (This is taken same as member strength)
        :param bolt_hole_type: standard or over-sized
        :param bolt_dia: diameter of bolt
        :param n_planes: number of shear planes
        :param edge_type: shear or hand flame cut
        :param connecting_plates_tk: thickness of connecting plates
        :param mu_f: slip factor for friction grip bolts
        :param member_fy: yield strength of member
        :param plate_fy: yield strength of plate
        :param corrosive_influences: yes or no
        :return: capacity of bolt (shear and bearing), ultimate strength of bolt and yield strength of bolt
        """
        if e is None:
            e = self.min_edge_dist_round
        if p is None:
            p = self.min_gauge_round

        self.bolt_diameter_provided = bolt_diameter_provided
        self.bolt_grade_provided = bolt_grade_provided
        [self.bolt_shank_area, self.bolt_net_area] = IS1367_Part3_2002.bolt_area(self.bolt_diameter_provided)
        [self.bolt_fu, self.bolt_fy] = IS1367_Part3_2002.get_bolt_fu_fy(self.bolt_grade_provided, self.bolt_diameter_provided)

        t_fu_prev = conn_plates_t_fu_fy[0][0] * conn_plates_t_fu_fy[0][1]
        thk_considered = conn_plates_t_fu_fy[0][0]
        fu_considered = conn_plates_t_fu_fy[0][1]
        for i in conn_plates_t_fu_fy:
            t_fu = i[0] * i[1]
            if t_fu <= t_fu_prev:
                thk_considered = i[0]
                fu_considered = i[1]
        self.d_0 = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter_provided, self.bolt_hole_type)
        if self.bolt_type == "Bearing Bolt":
            self.bolt_shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity(
                f_ub=self.bolt_fu, A_nb=self.bolt_net_area, A_sb=self.bolt_shank_area, n_n=n_planes, n_s=0)
            if seatedangle_e > 0.0:
                self.bolt_bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
                    f_u=fu_considered, f_ub=self.bolt_fu, t=thk_considered, d=self.bolt_diameter_provided,
                    e=seatedangle_e, p=p, bolt_hole_type=self.bolt_hole_type)
            else:
                self.bolt_bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
                    f_u=fu_considered, f_ub=self.bolt_fu, t=thk_considered, d=self.bolt_diameter_provided,
                    e=e, p=p, bolt_hole_type=self.bolt_hole_type)
            self.bolt_capacity = min(self.bolt_shear_capacity, self.bolt_bearing_capacity)
            self.fu_considered = fu_considered
            self.thk_considered = thk_considered

            # Since field or shop both is 1.25 we are not taking safety_factor_parameter as input
            self.gamma_mb = 1.25
            if p > 0.0:
                self.kb = min(e / (3.0 * self.d_0), p / (3.0 * self.d_0) - 0.25, self.bolt_fu / fu_considered, 1.0)
            else:
                self.kb = min(e / (3.0 * self.d_0), self.bolt_fu / fu_considered, 1.0)  # calculate k_b when there is no pitch (p = 0)

        elif self.bolt_type == "Friction Grip Bolt":
            self.bolt_shear_capacity,self.kh,self.gamma_mf = IS800_2007.cl_10_4_3_bolt_slip_resistance(
                f_ub=self.bolt_fu, A_nb=self.bolt_net_area, n_e=n_planes, mu_f=self.mu_f, bolt_hole_type=self.bolt_hole_type)
            self.bolt_bearing_capacity = VALUE_NOT_APPLICABLE
            self.bolt_capacity = self.bolt_shear_capacity

    def calculate_kb(self, e,p,d_0,f_ub,f_u):

        if p > 0.0:
            kb = min(e / (3.0 * d_0), p / (3.0 * d_0) - 0.25, f_ub / f_u, 1.0)
        else:
            kb = min(e / (3.0 * d_0), f_ub / f_u, 1.0)  # calculate k_b when there is no pitch (p = 0)

        return kb


    def calculate_bolt_tension_capacity(self, bolt_diameter_provided, bolt_grade_provided):
        """
        :param bolt_grade: grade of bolt
        :param member_fu: ultimate strength of member
        :param bolt_dia: diameter of bolt

        :return: capacity of bolt (tension), bolt_grade
        """
        self.bolt_diameter_provided = bolt_diameter_provided
        self.bolt_grade_provided = bolt_grade_provided


        [self.bolt_shank_area, self.bolt_net_area] = IS1367_Part3_2002.bolt_area(self.bolt_diameter_provided)
        [self.bolt_fu, self.bolt_fy] = IS1367_Part3_2002.get_bolt_fu_fy(self.bolt_grade_provided, self.bolt_diameter_provided)

        if self.bolt_type == "Bearing Bolt":
            self.bolt_tension_capacity = IS800_2007.cl_10_3_5_bearing_bolt_tension_resistance(
                f_ub=self.bolt_fu, f_yb=self.bolt_fy, A_sb=self.bolt_shank_area, A_n=self.bolt_net_area)

        elif self.bolt_type == "Friction Grip Bolt":
            self.bolt_tension_capacity = IS800_2007.cl_10_4_5_friction_bolt_tension_resistance(
                f_ub=self.bolt_fu, f_yb=self.bolt_fy, A_sb=self.bolt_shank_area, A_n=self.bolt_net_area)


    def calculate_bolt_spacing_limits(self, bolt_diameter_provided, conn_plates_t_fu_fy):

        self.connecting_plates_tk = [i[0] for i in conn_plates_t_fu_fy]
        self.bolt_diameter_provided = bolt_diameter_provided


        self.min_pitch = round(IS800_2007.cl_10_2_2_min_spacing(self.bolt_diameter_provided),2)
        self.min_gauge = round(IS800_2007.cl_10_2_2_min_spacing(self.bolt_diameter_provided),2)
        self.min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_provided, self.bolt_hole_type,
                                                                            self.edge_type),2)
        self.min_end_dist = self.min_edge_dist
        self.max_spacing = round(IS800_2007.cl_10_2_3_1_max_spacing(self.connecting_plates_tk),2)
        self.max_edge_dist = round(IS800_2007.cl_10_2_4_3_max_edge_dist(conn_plates_t_fu_fy,
                                                                        self.corrosive_influences),2)

        self.max_end_dist = self.max_edge_dist
        self.min_pitch_round = round_up(self.min_pitch, 5)
        self.min_gauge_round = round_up(self.min_gauge, 5)
        self.min_edge_dist_round = round_up(self.min_edge_dist, 5)
        self.min_end_dist_round = round_up(self.min_end_dist, 5)
        self.max_spacing_round = round_down(self.max_spacing, 5)
        self.max_edge_dist_round = round_down(self.max_edge_dist, 5)
        self.max_end_dist_round = round_down(self.max_end_dist, 5)
        self.dia_hole = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter_provided, self.bolt_hole_type)


class Nut(Material):

    def __init__(self, diameter=0.0, material_grade=""):
        self.diameter = diameter
        super(Nut, self).__init__(material_grade)


    def __repr__(self):
        repr = "Nut\n"
        repr += "Diameter: {}\n".format(self.diameter)
        return repr


class Section(Material):

    def __init__(self, designation, material_grade=""):


        self.design_status = True
        self.designation = designation
        self.type = "Rolled"
        self.type2 = "generally"
        self.notch_ht = 0.0

        self.mass = 0.0
        self.area = 0.0
        self.depth = 0.0
        # web_height for for rolled section without notches (considered as default)
        self.web_height = self.depth
        self.flange_width = 0.0
        self.web_thickness = 0.0
        self.flange_thickness = 0.0
        self.flange_slope = 0.0
        self.root_radius = 0.0
        self.toe_radius = 0.0
        self.mom_inertia_z = 0.0
        self.mom_inertia_y = 0.0
        self.rad_of_gy_z = 0.0
        self.rad_of_gy_y = 0.0
        self.elast_sec_mod_z = 0.0
        self.elast_sec_mod_y = 0.0
        self.plast_sec_mod_z = 0.0
        self.plast_sec_mod_y = 0.0
        self.It = 0.0
        self.Iw = 0.0
        self.source = 0.0

        self.tension_yielding_capacity = 0.0
        self.tension_rupture_capacity = 0.0
        self.shear_yielding_capacity = 0.0
        self.shear_rupture_capacity = 0.0
        self.block_shear_capacity_shear = 0.0
        self.block_shear_capacity_axial = 0.0
        self.block_shear_capacity = 0.0

        # self.shear_yielding_capacity = 0.0
        # self.shear_rupture_capacity = 0.0

        self.tension_capacity_flange = 0.0
        self.shear_capacity_flange = 0.0
        self.tension_capacity_web = 0.0
        self.shear_capacity_web = 0.0
        self.tension_yielding_capacity_web=0.0
        self.tension_rupture_capacity_web=0.0
        self.block_shear_capacity_web=0.0

        self.block_shear_capacity_axial = 0.0
        self.block_shear_capacity_shear = 0.0

        self.moment_capacity = 0.0
        self.plastic_moment_capactiy =0.0
        self.moment_d_def_criteria =0.0

        self.tension_capacity = 0.0
        self.slenderness = 0.0
        self.min_radius_gyration = 0.0
        self.beta =0.0
        self.IR = 1.0
        # self.min_rad_gyration_bbchannel = 0.0

        # self.member_yield_eqn =0.0
        # self.member_rup_eqn = 0.0
        # self.member_block_eqn = 0.0


    def connect_to_database_update_other_attributes(self, table, designation,material_grade = ""):
        conn = sqlite3.connect(PATH_TO_DATABASE)
        db_query = "SELECT * FROM " + table + " WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()
        self.mass = row[2]
        self.area = row[3] *100
        self.depth = row[4]
        self.flange_width = row[5]
        self.web_thickness = row[6]
        self.flange_thickness = row[7]
        max_thickness = max(self.flange_thickness,self.web_thickness)
        super(Section, self).__init__(material_grade,max_thickness)
        self.flange_slope = row[8]
        self.root_radius = row[9]
        self.toe_radius = row[10]
        self.mom_inertia_z = row[11]*10000
        self.mom_inertia_y = row[12] *10000
        self.rad_of_gy_z = row[13]* 10
        self.rad_of_gy_y = row[14] *10
        self.elast_sec_mod_z = row[15] *1000
        self.elast_sec_mod_y = row[16] *1000
        self.plast_sec_mod_z = row[17]
        if self.plast_sec_mod_z is None:  # Todo: add in database
            self.plast_sec_mod_z = I_sectional_Properties().calc_PlasticModulusZpz(self.depth,self.flange_width,
                                                                                   self.web_thickness,self.flange_thickness)*1000
        else:
            self.plast_sec_mod_z = row[17] *1000

        self.plast_sec_mod_y = row[18]
        if self.plast_sec_mod_y is None:  # Todo: add in database
            self.plast_sec_mod_y = I_sectional_Properties().calc_PlasticModulusZpy(self.depth,self.flange_width,
                                                                                   self.web_thickness,self.flange_thickness)*1000
        else:
            self.plast_sec_mod_y = row[17] * 1000


        self.It = I_sectional_Properties().calc_torsion_const(self.depth,self.flange_width,
                                                                                   self.web_thickness,self.flange_thickness)*10**4\
            if row[19] is None else row[19] * 10**4
        self.Iw = I_sectional_Properties().calc_warping_const(self.depth,self.flange_width,
                                                                                   self.web_thickness,self.flange_thickness)*10**6 \
            if row[20] is None else row[20] * 10**4
        self.source = row[21]
        self.type = 'Rolled' if row[22] is None else row[22]


        conn.close()

    def shear_yielding(self, length, thickness, fy):
        '''
        Args:
            length (float) length of member in direction of shear load
            thickness(float) thickness of member resisting shear
            beam_fy (float) Yeild stress of section material
        Returns:
            Capacity of section in shear yeiding
        '''

        A_v = length * thickness
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        # V_p = (0.6 * A_v * fy) / (math.sqrt(3) * gamma_m0 * 1000)  # kN
        V_p = (A_v * fy) / (math.sqrt(3) * gamma_m0 * 1000)  # kN

        self.shear_yielding_capacity = round(V_p,2)

    def tension_yielding(self, length, thickness, fy):
        '''
        Args:
            length (float) length of member in direction of tension load
            thickness(float) thickness of member resisting tension
            beam_fy (float) Yeild stress of section material
        Returns:
            Capacity of section in tension yeiding
        '''
        A_v = length * thickness
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        # A_v = height * thickness
        tdg = (A_v * fy) / (gamma_m0 * 1000)
        self.tension_yielding_capacity = round(tdg,2)

    def tension_member_yielding(self, A_g, F_y):
        "design strength of members under axial tension,T_dg,as governed by yielding of gross section"
        "A_g = gross area of cross-section"
        "gamma_m0 = partial safety factor for failure in tension by yielding"
        "F_y = yield stress of the material"
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        T_dg = (A_g* F_y / gamma_m0)
        # Ag = str(A_g)
        # fy = str(F_y)
        # gamma_m0 = str(gamma_m0)
        # memb_yield = str(round((T_dg/1000),2))
        # logger.warning(
        #     " : You are using a section (in red color) that is not available in latest version of IS 808")
        # member_yield_eqn = Math(inline=True)
        # member_yield_eqn.append(NoEscape(r'\begin{aligned}T_{dg} &= \frac{A_g ~ f_y}{\gamma_{m0}}\\'))
        # member_yield_eqn.append(NoEscape(r'&= \frac{' + Ag + '*' + fy + '}{' + gamma_m0 + r'}\\'))
        # member_yield_eqn.append(NoEscape(r'&= ' + memb_yield + r'\end{aligned}'))

        self.tension_yielding_capacity = round(T_dg,2)
        # self.member_yield_eqn = member_yield_eqn
        # logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")

    def tension_rupture(self, A_n, F_u):
        "preliminary design strength,T_pdn,as governed by rupture at net section"
        "A_n = net area of the total cross-section"
        "F_u = Ultimate Strength of material"

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_pdn = 0.9 * A_n * F_u / gamma_m1

        self.tension_rupture_capacity = round(T_pdn,2)

    def tension_member_design_due_to_rupture_of_critical_section(self, A_nc, A_go, F_u, F_y, L_c, w, b_s, t):
        "design strength,T_dn,as governed by rupture at net section"
        "A_n = net area of the total cross-section"
        "A_nc = net area of the connected leg"
        "A_go = gross area of the outstanding leg"
        "alpha_b,alpha_w = 0.6 - two bolts, 0.7 - three bolts or 0.8 - four or more bolts/welded"
        "gamma_m1 = partial safety factor for failure in tension by ultimate stress"
        "F_u = Ultimate Strength of material"
        "w = outstanding leg width"
        "b_s = shear lag width"
        "t = thickness of the leg"
        "L_c = length of the end connection"
        "gamma_m0 = partial safety factor for failure in tension by yielding"
        "F_y = yield stress of the material"

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

        if L_c == 0:
            self.beta = 1.4
        else:
            self.beta = float(1.4 - (0.076 * float(w) / float(t) * float(F_y) / (0.9 * float(F_u)) * float(b_s) / float(L_c)))

        if self.beta <= (F_u * gamma_m0 / F_y * gamma_m1) and self.beta >= 0.7:
            self.beta = self.beta
        else:
            self.beta = 0.7

        self.beta = round(self.beta,2)

        T_dn = (0.9 * A_nc * F_u / gamma_m1) + (self.beta * A_go * F_y / gamma_m0)
        # w = str(w)
        # t = str(t)
        # fy = str(F_y)
        # fu = str(F_u)
        # b_s = str(b_s)
        # L_c = str(L_c)
        # A_nc = str(A_nc)
        # A_go = str(A_go)
        # gamma_m0 = str(gamma_m0)
        # gamma_m1 = str(gamma_m1)
        # member_rup_eqn = Math(inline=True)
        # member_rup_eqn.append(NoEscape(r'\begin{aligned}\beta &= 1.4 - 0.076 \frac{w}{t}*\frac{f_{y}}{f_{u}}*\frac{b_s}{L_c}\leq\frac{0.9*f_{u}*\gamma_{m0}}{f_{y}*\gamma_{m1}} \geq 0.7 \end{aligned}'))
        # member_rup_eqn.append(NoEscape(r'\begin{aligned}&\beta &= 1.4-0.076(w/t)(f_{y}/f_{u})(b_s/L_c)\leq(0.9f_{u}\gamma_{m0}/f_{y}\gamma_{m1}) \geq 0.7\\'))
        # member_rup_eqn.append(NoEscape(r'&= 1.4 -0.76 \frac {' + w + '}{' + t + '} \frac {' + F_y + '}{' + F_u + '} \frac {' + bs + '}{' + L_c + '} +'\leq'+ \frac {' +0.9 + '*'+ F_u +'}{'+ F_y +'\gamma_{m1}'+ '}\geq 0.7 \\'))
        # member_rup_eqn.append(NoEscape(r'\begin{aligned}T_{dg} &= \frac{A_g ~ f_y}{\gamma_{m0}}\\'))
        # member_rup_eqn.append(NoEscape(r'&= \frac{' + Ag + '*' + fy + '}{' + gamma_m0 + r'}\\'))
        # member_rup_eqn.append(NoEscape(r'&= ' + memb_yield + r'\end{aligned}'))

        # self.member_rup_eqn = member_rup_eqn

        self.tension_rupture_capacity = round((T_dn) , 2)


    def tension_blockshear(self, numrow, numcol, pitch, gauge, thk, end_dist, edge_dist, dia_hole, fy, fu):
        '''

        Args:
            numrow (str) Number of row(s) of bolts
            dia_hole (int) diameter of hole (Ref. Table 5.6 Subramanian's book, page: 340)
            fy (float) Yeild stress of material
            fu (float) Ultimate stress of material
            edge_dist (float) edge distance based on diameter of hole
            end_dist (float) end distance based on diameter of hole
            pitch (float) pitch distance based on diameter of bolt
            thk (float) thickness of plate or beam web

        Returns:
            Capacity of fin plate under block shear

        '''

        Avg = thk * ((numrow - 1) * gauge + edge_dist)
        Avn = thk * ((numrow - 1) * gauge + edge_dist - (numrow - 0.5) * dia_hole)
        Atg = thk * (pitch * (numcol - 1) + end_dist)
        Atn = thk * (pitch * (numcol - 1) + end_dist - (numcol - 0.5) * dia_hole)
        Tdb1 = (Avg * fy / (math.sqrt(3) * 1.1) + 0.9 * Atn * fu / 1.25)
        Tdb2 = (0.9 * Avn * fu / (math.sqrt(3) * 1.25) + Atg * fy / 1.1)
        Tdb = min(Tdb1, Tdb2)
        Tdb = round(Tdb, 3)
        self.block_shear_capacity_axial = round(Tdb,2)

    def tension_blockshear_area_input(self,A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1

        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)

        Return:
            block shear strength of bolted connection in N (float)

        Note:
            Reference:
            IS 800:2007, cl. 6.4.1

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        Tdb = min(T_db1, T_db2)
        # Tdb = round(Tdb, 3)
        # A_vg = str(A_vg)
        # A_vn = str(A_vn)
        # A_tg = str(A_tg)
        # A_tn = str(A_tn)
        # f_y = str(f_y)
        # f_u = str(f_u)
        # gamma_m1 = str(gamma_m1)
        # gamma_m0 = str(gamma_m0)

        # member_block_eqn = Math(inline=True)
        # member_block_eqn.append(NoEscape(r'\begin{aligned}T_{db1} &= \frac{A_{vg} f_y}{\sqrt{3} \gamma_{m0}} + \frac{0.9 A_{tn} f_u}{\gamma_{m1}} \end{aligned}'))

        # member_block_eqn.append(NoEscape(r'&= \frac{' + A_vg + '*' + f_y + '}{" 1.732*' + gamma_m0 + 'r'} + &+ +'\frac{"0.9*" + A_vn + '*' + f_u + '}{'+1.732+'*' + gamma_m0 + r'} '\\'))
        # member_block_eqn.append(NoEscape(r'&= ' + memb_yield + r'\end{aligned}'))



        # self.member_block_eqn =member_block_eqn
        self.block_shear_capacity_axial = round(Tdb,2)

    def tension_capacity_calc(self, tension_member_yielding, tension_rupture, tension_blockshear):

        Tc = min(tension_member_yielding, tension_rupture, tension_blockshear)

        self.tension_capacity = Tc

    def min_rad_gyration_calc(self,key,subkey,mom_inertia_y,mom_inertia_z, area,rad_y, rad_z, rad_u =0.0, rad_v=0.0, Cg_1=0,Cg_2 =0, thickness=0.0):

        if key == "Channels" and subkey == "Web":
            min_rad = min(rad_y, rad_z)

        elif key == 'Back to Back Channels' and subkey == "Web":
            Iyy = (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
            Izz = 2 * mom_inertia_z
            I = min(Iyy, Izz)
            min_rad= math.sqrt(I / (2*area))

        elif key == "Back to Back Angles" and subkey == 'Long Leg':
            Iyy = (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
            Izz = 2 * mom_inertia_z
            I = min(Iyy, Izz)
            min_rad= math.sqrt(I / (2*area))

        elif key == 'Back to Back Angles' and subkey == 'Short Leg':
            Izz = (mom_inertia_z + (area * (Cg_2 + thickness) * (Cg_2 + thickness))) * 2
            Iyy = 2 * mom_inertia_y
            I = min(Iyy, Izz)
            min_rad= math.sqrt(I / (2*area))

        elif key == 'Star Angles' and subkey == 'Long Leg':
            Iyy = (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
            Izz = (mom_inertia_z + (area * Cg_2 * Cg_2)) * 2
            I = min(Iyy, Izz)
            min_rad= math.sqrt(I / (2*area))

        elif key == 'Star Angles' and subkey == 'Short Leg':
            Izz = (mom_inertia_z + (area * (Cg_2 + thickness) * (Cg_2 + thickness))) * 2
            Iyy = (mom_inertia_y + (area * Cg_1 * Cg_1)) * 2
            I = min(Iyy, Izz)
            min_rad= math.sqrt(I / (2*area))

        elif key == 'Angles' and (subkey == 'Long Leg' or subkey == 'Short Leg'):
            min_rad = min(rad_u, rad_v)

        self.min_radius_gyration = min_rad


    def design_check_for_slenderness(self, K, L, r):
        "KL= effective length of member"
        "r = radius of gyration of member"

        slender = (float(K) * float(L)) / float(r)

        self.slenderness = round(slender,2)

    def plastic_moment_capacty(self, beta_b, Z_p, fy):
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        self.plastic_moment_capactiy = beta_b * Z_p * fy / (gamma_m0)  # Nm # for section

    def moment_d_deformation_criteria(self, fy, Z_e):
        """
        considering cantilever section
        """
        self.moment_d_def_criteria = 1.5 * (fy / 1.1) * (Z_e) # Nm
        # moment_capacity_sec = self.flange_plate.moment_capacity


    def __repr__(self):
        repr = "Section\n"
        repr += "Designation: {}\n".format(self.designation)
        repr += "fy: {}\n".format(self.fy)
        repr += "fu: {}\n".format(self.fu)

        # repr += "shear yielding capacity: {}\n".format(self.shear_yielding_capacity)
        repr += "tension yielding capacity: {}\n".format(self.tension_yielding_capacity)

        repr += "tension_capacity_flange: {}\n".format(self.tension_capacity_flange)
        repr += "tension_capacity_web: {}\n".format( self.tension_capacity_web)
        repr += "shear_capacity_flange: {}\n".format( self.shear_capacity_flange)
        repr += "shear_capacity_web: {}\n".format(self.shear_capacity_web)
        return repr

class Beam(Section):

    def __init__(self, designation, material_grade):
        super(Beam, self).__init__(designation, material_grade)

        self.connect_to_database_update_other_attributes("Beams", designation,material_grade)

    def min_plate_height(self):
        return 0.6 * self.depth

    def max_plate_height(self, connectivity=None, notch_height = 0.0):
        if connectivity in VALUES_CONN_1 or connectivity == None:
            clear_depth = self.depth - 2*self.flange_thickness - 2*self.root_radius
        else:
            clear_depth = self.depth - notch_height
        return clear_depth

class Column(Section):

    def __init__(self, designation, material_grade):
        super(Column, self).__init__(designation, material_grade)

        self.connect_to_database_update_other_attributes("Columns", designation,material_grade)


    def min_plate_height(self):
        return 0.6 * self.depth

    def max_plate_height(self):

        clear_depth = self.depth - 2*self.flange_thickness - 2*self.root_radius
        return clear_depth

class Channel(Section):

    def __init__(self, designation, material_grade):
        super(Channel, self).__init__(material_grade)
        self.connect_to_database_update_other_attributes_channels(designation, material_grade)
        # self.length =0.0

    def connect_to_database_update_other_attributes_channels(self, designation, material_grade):
        conn = sqlite3.connect(PATH_TO_DATABASE)
        db_query = "SELECT * FROM Channels WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()
        self.designation = designation
        self.mass = row[2]
        self.area = row[3] *100
        self.depth = row[4]
        self.flange_width = row[5]
        self.web_thickness = row[6]
        self.flange_thickness = row[7]
        max_thickness = max(self.web_thickness,self.flange_thickness)
        super(Section, self).__init__(material_grade,max_thickness)
        self.flange_slope = row[8]
        self.root_radius = row[9]
        self.toe_radius = row[10]
        self.Cy = row[11] * 10
        self.mom_inertia_z = row[12] * 10000
        self.mom_inertia_y = row[13] * 10000
        self.rad_of_gy_z = row[14] * 10
        self.rad_of_gy_y = row[15] * 10
        self.elast_sec_mod_z = row[16] * 1000
        self.elast_sec_mod_y = row[17] * 1000
        try:
            self.plast_sec_mod_z = row[18] * 1000
            self.plast_sec_mod_y = row[19] * 1000
        except:
            self.plast_sec_mod_z = self.elast_sec_mod_z
            self.plast_sec_mod_y = self.elast_sec_mod_y


        self.It = Single_Channel_Properties().calc_torsion_const_It(self.depth, self.flange_width,
                                                                  self.web_thickness, self.flange_thickness) * 10 ** 4 \
            if row[20] is None else row[20] * 10 ** 4
        self.Iw = Single_Channel_Properties().calc_warping_const_Iw(self.depth, self.flange_width,
                                                                  self.web_thickness, self.flange_thickness) * 10 ** 6 \
            if row[21] is None else row[21] * 10 ** 6
        self.source = row[22]
        self.type = 'Rolled' if row[23] is None else row[24]

        conn.close()

    def min_plate_height(self):
        return 0.6 * self.depth

    def max_plate_height(self):

        clear_depth = self.depth - 2*self.flange_thickness - 2*self.root_radius
        return clear_depth


class Weld:

    def __init__(self, material_g_o="",type=KEY_DP_WELD_TYPE_FILLET, fabrication=KEY_DP_WELD_FAB_SHOP):
        self.design_status = True
        self.type = type
        self.fabrication = fabrication

        self.size = 0.0
        self.length = 0.0
        self.eff_length = 0.0
        self.inner_length = 0.0
        self.effective = 0.0
        self.height = 0.0
        self.inner_height = 0.0
        self.strength = 0.0
        self.strength_red = 0.0
        self.throat = 0.0
        self.stress = 0.0
        self.inner_strength = 0.0
        self.inner_stress = 0.0

        self.fu = float(material_g_o)
        self.throat_tk = 0.0
        self.reason = 0.0

    def __repr__(self):
        repr = "Weld\n"
        repr += "Size: {}\n".format(self.size)
        repr += "Length: {}\n".format(self.length)
        repr += "Stress: {}\n".format(self.stress)
        repr += "Strength: {}\n".format(self.strength)
        repr += "throattk: {}\n".format(self.throat_tk )
        return repr

    def get_weld_strength(self, connecting_fu, weld_fabrication, t_weld, weld_angle):
        # connecting_fu.append(self.fu)
        f_wd = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(connecting_fu, weld_fabrication)
        self.throat_tk = \
            round(IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness \
                (t_weld, weld_angle),2)

        weld_strength = round(f_wd * self.throat_tk,2)
        self.strength = weld_strength

    def get_weld_strength_lj(self, connecting_fu, weld_fabrication, t_weld, weld_angle, lenght):
        f_wd = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(connecting_fu, weld_fabrication)
        self.throat_tk = \
            round(IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness \
                (t_weld, weld_angle),2)

        weld_strength = round(f_wd * self.throat_tk,2)
        self.strength = weld_strength

    def get_weld_stress(self,weld_shear, weld_axial, l_weld, weld_twist=0.0, Ip_weld=None, y_max=0.0, x_max=0.0):
        if weld_twist != 0.0:
            T_wh = weld_twist * y_max/Ip_weld
            T_wv = weld_twist * x_max/Ip_weld
        else:
            T_wh = 0.0
            T_wv = 0.0
        V_wv = weld_shear/l_weld

        A_wh = weld_axial/l_weld
        weld_stress = round(math.sqrt((T_wh+A_wh)**2 + (T_wv+V_wv)**2),2)
        self.stress = weld_stress

    def weld_size(self, plate_thickness, member_thickness, edge_type = "Square"):

        max_weld_thickness = (min(plate_thickness, member_thickness))
        if plate_thickness<=10:
            min_weld_thickness = 3
        elif plate_thickness>=10 and plate_thickness<=20:
            min_weld_thickness = 5
        elif plate_thickness>=20 and plate_thickness<=30:
            min_weld_thickness = 6
        else:
            min_weld_thickness = 10

        if edge_type == "Square":
            red = 1.5
        else:
            red = 0.25 * max_weld_thickness

        weld_thickness = round_down((max_weld_thickness - red), 1, 3)
        if weld_thickness < min_weld_thickness:
            weld_thickness = int(min(plate_thickness, member_thickness))
            weld_reason = " Preheating of thicker plate is required (IS 800:2007 Table 21)."
        else:
            weld_reason = "Size of weld is calculated based on the edge type i.e. square edge or round edge (IS 800:2007 Clause 10.5)). "
            pass

        if weld_thickness > 16 :
            weld_thickness =16
        else:
            pass
        self.size = weld_thickness
        self.reason = weld_reason
        self.red = red
        self.min_weld = min_weld_thickness

    def get_weld_red(self,t_t,strength, height=0.0 , length =0.0):
        """Calculate the reduction factor for long joints in welds and reduced strength
                Args:
                    l_j - maximum length of joints in the direction of force transfer in mm (float)
                    t_t - throat size of the weld in mm (float)
                    strength - Actual strength of weld
                Returns:
                     Reduction factor, beta_lw for long joints in welds (float)
                Note:
                    Reference:
                    IS 800:2007,  cl 10.5.7.3
                """
        lj = max(height,length)
        beta_lw = IS800_2007.cl_10_5_7_3_weld_long_joint(lj, t_t)

        self.beta_lw = round(beta_lw,2)

        self.strength_red = round(self.beta_lw * strength,2)




class Plate(Material):
    def __init__(self, thickness=[], height=0.0,Innerheight=0.0, length=0.0,Innerlength=0.0, gap=0.0, material_grade=""):
        super(Plate, self).__init__(material_grade=material_grade)
        self.design_status = False
        self.design_status_capacity = False
        self.reason = ""
        if thickness:
            self.thickness = list(np.float_(thickness))
            self.thickness.sort(key=float)
        else:
            self.thickness = 0.0
        self.thickness_provided = 0.0
        super(Plate, self).__init__(material_grade, self.thickness_provided)
        self.height = height
        self.length = length
        self.gap = float(gap)
        self.Innerlength = Innerlength
        self.Innerheight = Innerheight

        self.bolts_required = 0
        self.bolt_capacity_red = 0.0
        self.bolt_line = 0.0
        self.bolts_one_line = 0.0
        self.bolt_force = 0.0

        self.moment_demand = 0.0
        self.thickness_provided = 0.0
        self.pitch_provided = 0.0
        self.gauge_provided = 0.0
        self.midgauge =0.0
        self.midpitch = 0.0
        self.edge_dist_provided = 0.0
        self.end_dist_provided = 0.0

        self.block_shear_capacity = 0.0
        self.tension_yielding_capacity = 0.0
        self.tension_rupture_capacity = 0.0
        self.tension_capacity = 0.0
        self.shear_yielding_capacity = 0.0
        self.shear_rupture_capacity = 0.0
        self.shear_capacity = 0.0


        self.shear_capacity_web_plate=0.0
        self.tension_capacity_web_plate = 0.0
        self.tension_capacity_flange_plate = 0.0
        self.block_shear_capacity_shear = 0.0
        self.block_shear_capacity_axial = 0.0
        self.moment_capacity = 0.0
        self.IR = 1.0

        self.ymax = 0.0
        self.xmax = 0.0
        self.sigma_r_sq = 0.0
        self.moment_demand = 0.0
        self.vres = 0.0
        self.length_avail = 0.0
        self.ecc = 0.0
        self.vbv = 0.0
        self.tmh = 0.0
        self.abh = 0.0
        self.tmv = 0.0
        self.vres = 0.0
        self.spacing_status =0.0

        # self.moment_demand_disp = round(self.moment_demand/1000000, 2)
        # self.block_shear_capacity_disp = round(self.block_shear_capacity/1000, 2)
        # self.shear_yielding_capacity_disp = round(self.shear_yielding_capacity/1000, 2)
        # self.shear_rupture_capacity_disp = round(self.shear_rupture_capacity/1000, 2)
        # self.tension_yielding_capacity_disp = round(self.tension_yielding_capacity/1000, 2)
        # self.moment_capacity_disp = round(self.moment_capacity/1000000, 2)

    def get_web_plate_h_req(self, bolts_one_line, gauge, edge_dist):
        web_plate_h_req = float((bolts_one_line - 1) * gauge + 2 * edge_dist)
        return web_plate_h_req


    def get_flange_plate_h_req(self, bolts_one_line, gauge, edge_dist,web_thickness,root_radius): #todo-anjali
        flange_plate_h_req = 2*float(((bolts_one_line/2 - 1) * gauge) + (2 * edge_dist) + web_thickness/2 + root_radius)
        return flange_plate_h_req

    def get_spacing_adjusted(self, gauge_pitch, edge_end, max_spacing):
        while gauge_pitch > max_spacing:
            edge_end += 5
            gauge_pitch -= 10
        return gauge_pitch, edge_end


    def get_web_plate_l_bolts_one_line(self, web_plate_h_max, web_plate_h_min,bolts_required,edge_dist, gauge,min_bolts_one_line=2,min_bolt_line=1):

        max_bolts_one_line = int(((web_plate_h_max - (2 * edge_dist)) / gauge) + 1)
        if max_bolts_one_line >= min_bolts_one_line:
            bolt_line = max(int(math.ceil((float(bolts_required) / float(max_bolts_one_line)))), min_bolt_line)
            bolts_one_line = max(int(math.ceil(float(bolts_required) / float(bolt_line))),min_bolts_one_line)
            height = max(web_plate_h_min, self.get_web_plate_h_req (bolts_one_line, gauge, edge_dist))
            self.spacing_status = True
            return bolt_line, bolts_one_line, height
        else:
            bolt_line = 0
            bolts_one_line = 0
            height = 0
            return bolt_line, bolts_one_line, height


    def get_flange_plate_l_bolts_one_line(self, flange_plate_h_max, flange_plate_h_min, bolts_required, edge_dist, gauge,web_thickness,root_radius):# todo anjalinew

        # max_bolts_one_line = int(((flange_plate_h_max - (2 * edge_dist)) / gauge) + 1)
        # print("max_bolts_one_line", max_bolts_one_line)
        possible_bolt = (flange_plate_h_max/2 - web_thickness/2 - 2 *edge_dist)-root_radius
        if possible_bolt > 0:
            bolt_one_side = int(possible_bolt/gauge  +1)
            max_bolts_one_line = 2*bolt_one_side
            print("max bolt one line",max_bolts_one_line)


            if max_bolts_one_line >= 2:
                print("bolts_required",bolts_required)
                bolt_line = max(int(math.ceil((float(bolts_required) / float(max_bolts_one_line)))),1)
                bolts_one_line = min(round_up(int(math.ceil(float(bolts_required) / float(bolt_line))),2,2),max_bolts_one_line)
                print("bbbb1", bolt_line, bolts_one_line)
                # if bolts_one_line % 2 == 1:
                #     bolts_one_line = bolts_one_line-1
                #     bolt_line =bolt_line  +1
                # else:
                #     pass

                height =flange_plate_h_max
                print("bbbb",bolt_line, bolts_one_line, height)
                #     self.get_flange_plate_h_req(self.bolts_one_line, gauge, edge_dist, web_thickness, root_radius))
                return bolt_line, bolts_one_line, height
            # if max_bolts_one_line >= 2:
            #     bolts_one_line = int(math.ceil(float(bolts_required) / float(max_bolts_one_line)))
            #     bolt_line = max(int(math.ceil((float(bolts_required) / float( bolts_one_line)))), 1)
            #     height = flange_plate_h_max
            #     # (
            #     #     self.get_flange_plate_h_req(self.bolts_one_line, gauge, edge_dist, web_thickness, root_radius))
            #     return bolt_line, bolts_one_line, height
            else:
                bolt_line = 0
                bolts_one_line = 0
                height = 0
                return bolt_line, bolts_one_line, height
        else:
            self.design_status = False
            bolt_line = 0
            bolts_one_line = 0
            height = 0
            return bolt_line, bolts_one_line, height

    def get_gauge_edge_dist(self, web_plate_h, bolts_one_line, edge_dist, max_spacing, max_edge_dist):
        """

        :param web_plate_l: height of plate
        :param min_end_dist_round: minimum end distance
        :param bolts_one_line: bolts in one line
        :param max_spacing_round: maximum pitch
        :param max_end_dist_round: maximum end distance
        :return: pitch, end distance, height of plate (false if applicable)
        """
        gauge = 0
        if bolts_one_line > 1:
            gauge = round_up((web_plate_h - (2 * edge_dist)) / (bolts_one_line - 1), multiplier=5)

        web_plate_h = gauge * (bolts_one_line - 1) + edge_dist * 2

        if gauge > max_spacing:
            gauge, edge_dist = self.get_spacing_adjusted(gauge, edge_dist, max_spacing)
            if edge_dist >= max_edge_dist:
                # TODO: add maximum plate height limit
                # TODO: add one more bolt to satisfy spacing criteria?? Its better to give false as output,
                #  so coder can decide if they want to add a bolt for spacing criteria.
                #  This logic is in function get_web_plate_details
                web_plate_h = False
        elif gauge == 0:
            edge_dist = web_plate_h/2
            if edge_dist >= max_edge_dist:
                web_plate_h = False
        return gauge, edge_dist, web_plate_h


    def get_gauge_edge_dist_flange(self, flange_plate_h,
                                   bolts_one_line, edge_dist, max_spacing, max_edge_dist,web_thickness,root_radius): #todo anjali
        """

        :param web_plate_l: height of plate
        :param min_end_dist_round: minimum end distance
        :param bolts_one_line: bolts in one line
        :param max_spacing_round: maximum pitch
        :param max_end_dist_round: maximum end distance
        :return: pitch, end distance, height of plate (false if applicable)
        """
        if bolts_one_line > 2:
            """
            gauge is the distance between bolts along bolt line on either side of the web thickness
            """
            gauge = (int((flange_plate_h/2 - web_thickness/2 - (2 * edge_dist)-root_radius) / (bolts_one_line/2 - 1))) #
            edge_dist =  round(float((flange_plate_h/2 - web_thickness/2 - root_radius - ((bolts_one_line/2 - 1)*gauge))/2),2)
        else:
            gauge = 0.
            edge_dist = round(float((flange_plate_h / 2 - web_thickness / 2 - root_radius - ((bolts_one_line / 2 - 1) * gauge)) / 2),2)


        # multiplier=5)
        # web_plate_h = gauge*(bolts_one_line - 1) + edge_dist*2
        if gauge > max_spacing:
            gauge, edge_dist = self.get_spacing_adjusted(gauge, edge_dist, max_spacing)
            if edge_dist >= max_edge_dist:
                # TODO: add one more bolt to satisfy spacing criteria
                flange_plate_h = False
        else:
            pass
        return gauge, edge_dist, flange_plate_h

    def get_vres(self, bolts_one_line, pitch, gauge, bolt_line, shear_load, axial_load, ecc,web_moment=0.0):
        """1000

        :param bolts_one_line: number of bolts in one line
        :param pitch: pitch
        :param gauge: gauge
        :param bolt_line: number of bolt lines
        :param shear_load: shear load
        :param ecc: eccentricity
        :return: resultant load on bolt due to eccentricity of shear force
        """
        length_avail = (bolts_one_line - 1) * gauge
        ymax = length_avail / 2
        xmax = pitch * (bolt_line - 1) / 2
        r_sq = 0
        n = float(bolts_one_line) / 2.0 - 0.5
        b = float((bolt_line - 1)) / 2
        for x in np.arange(b, -b - 1, -1):
            for y in np.arange(-n, n + 1, 1):
                r_sq = r_sq + ((pitch * x) ** 2 + (abs(y) * gauge) ** 2)
        sigma_r_sq = r_sq

        vbv = shear_load / (bolts_one_line * bolt_line)
        moment_demand = round((shear_load * ecc + web_moment), 3)
        tmh = moment_demand * ymax / sigma_r_sq
        tmv = moment_demand * xmax / sigma_r_sq
        abh = axial_load / (bolts_one_line * bolt_line)
        vres = math.sqrt((vbv + tmv) ** 2 + (tmh+abh) ** 2)
        print('rsq,vres',sigma_r_sq,vres)
        self.ymax = ymax
        self.xmax = xmax
        self.sigma_r_sq = sigma_r_sq
        self.moment_demand = moment_demand
        self.length_avail =length_avail
        self.vbv = vbv
        self.tmh = tmh
        self.abh = abh
        self.tmv = tmv
        self.ecc = ecc
        self.vres =vres
        return vres

    def get_bolt_red(self, bolts_one_line , gauge ,bolts_line ,
                     pitch, bolt_capacity, bolt_dia,end_dist=0.0,gap=0.0,edge_dist =0.0,root_radius =0.0,web_thickness =0.0):
        """
        :param bolts_one_line: bolts in one line
        :param gauge: gauge
        :param bolt_capacity: capacity of bolt
        :param bolt_dia: diameter of bolt
        :return: reduced bolt capacity if long joint condition is met
        """
        if end_dist==0.0 and gap==0.0:
            length_avail = max(((bolts_one_line - 1) * gauge),((bolts_line - 1) * pitch))
            if length_avail > 15 * bolt_dia:
                beta_lj = 1.075 - length_avail / (200 * bolt_dia)
                print('long joint case')
                if beta_lj >1:
                    beta_lj =1
                elif beta_lj<0.75:
                    beta_lj = 0.75
                else:
                    beta_lj = beta_lj
                bolt_capacity_red = round(beta_lj,2) * bolt_capacity
            else:
                bolt_capacity_red = bolt_capacity
        else:
            if web_thickness == 0.0:
                length_avail = max((2 * (((bolts_line-1) * pitch) + end_dist) + (2 * gap)), ((bolts_one_line - 1) * gauge))
            else:
                midgauge = 2 * (edge_dist + root_radius) + web_thickness
                length_avail = max((2 * (((bolts_line-1) * pitch) + end_dist) + (2 * gap)),
                                   (((bolts_one_line / 2 - 1) * gauge) + midgauge))
            if length_avail > 15 * bolt_dia:
                beta_lj = 1.075 - length_avail / (200 * bolt_dia)
                if beta_lj > 1:
                    beta_lj = 1
                elif beta_lj < 0.75:
                    beta_lj = 0.75
                else:
                    beta_lj = beta_lj
                bolt_capacity_red = round(beta_lj,2) * bolt_capacity
                print('beta',round(beta_lj, 2))
            else:
                bolt_capacity_red = bolt_capacity

        return bolt_capacity_red

    def get_web_plate_details(self, bolt_dia, web_plate_h_min, web_plate_h_max, bolt_capacity, min_edge_dist, min_gauge,
                              max_spacing, max_edge_dist, shear_load=0.0, axial_load=0.0, web_moment =0.0, gap=0.0,
                              shear_ecc=False, bolt_line_limit=math.inf, min_bolts_one_line=2, min_bolt_line=1,joint =None,min_pitch=None):


        """

        :param bolt_dia: diameter of bolt
        :param end_dist: minimum end distance
        :param pitch: minimum pitch
        :param web_plate_h_min: minimum plate height
        :param web_plate_h_max: maximum plate height
        :param bolt_capacity: capacity of bolt
        :param bolt_line_limit: maximum number of bolt lines allowed
        :param shear_load: load along the height (bolt_line)
        :param axial_load: load along the length
        :param gap: gap between members which adds up to eccentricity
        :param shear_ecc: if eccentricity effect needs to be considered this value should be passed as "True"
        :return: web_plate_h, bolt_line, bolts_one_line, bolts_required, bolt_capacity_red, vres, moment_demand, \
               pitch, gauge, edge_dist, end_dist, a.min_edge_dist_round, a.min_pitch_round, a.max_spacing_round, a.max_edge_dist_round
        """

        # initialising values to start the loop
        length =0.0
        count =0.0
        resultant_force = math.sqrt(shear_load ** 2 + axial_load ** 2)
        bolts_required = max(int(math.ceil(resultant_force / bolt_capacity)), min_bolt_line*min_bolts_one_line)
        [bolt_line, bolts_one_line, web_plate_h] = \
            self.get_web_plate_l_bolts_one_line(web_plate_h_max, web_plate_h_min, bolts_required
                                                , min_edge_dist, min_gauge, min_bolts_one_line,min_bolt_line)
        count = 0

        if bolts_one_line < min_bolts_one_line:
            self.design_status = False
            self.reason = "Can't fit two bolts in one line. Select lower diameter."
        elif bolt_line < min_bolt_line:
            self.design_status = False
            self.reason = "Can't fit two bolts in one line. Select lower diameter."
        elif bolt_line > bolt_line_limit:
            self.design_status = False
            self.reason = "Bolt line limit is reached. Select higher grade/Diameter or choose different connection."
        else:
            [gauge, edge_dist, web_plate_h] = self.get_gauge_edge_dist(web_plate_h, bolts_one_line,min_edge_dist,max_spacing, max_edge_dist)
            if bolt_line == 1:
                pitch = 0.0
            elif min_pitch != None:
                pitch = min_pitch
            else:
                pitch = min_gauge
            end_dist = min_edge_dist

            if shear_ecc is True:
                # If check for shear eccentricity is true, resultant force in bolt is calculated
                ecc = (pitch * max((bolt_line - 1.5), 0)) + end_dist + gap
                moment_demand = shear_load * ecc + web_moment
                vres = self.get_vres(bolts_one_line, pitch,
                                     gauge, bolt_line, shear_load, axial_load, ecc,web_moment)
            else:
                moment_demand = 0.0
                vres = resultant_force / (bolt_line * bolts_one_line)


            if joint == None:

                bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                                                      gauge, bolt_line, pitch, bolt_capacity,
                                                      bolt_dia)
            else:
                bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                                                      gauge, bolt_line, pitch, bolt_capacity,
                                                      bolt_dia, end_dist, gap)

            while bolt_line <= bolt_line_limit and vres > bolt_capacity_red:
                print("entered web plate details loop for bolt force:",vres,"bolt capaity reduced:", bolt_capacity_red)
                [gauge, edge_dist, web_plate_h_recalc] = self.get_gauge_edge_dist(web_plate_h+10, bolts_one_line, min_edge_dist,
                                                                           max_spacing, max_edge_dist)
                if web_plate_h_recalc <= web_plate_h_max and shear_ecc is True and gauge!=0:
                # gauge is recalculated only if there is shear ecc or else increase in bolt is the only option
                    web_plate_h += 10

                # If height cannot be increased number of bolts is increased by 1 and loop is repeated
                else:
                    bolts_required = bolt_line * bolts_one_line
                    bolts_required += 1
                    [bolt_line, bolts_one_line, web_plate_h] = \
                        self.get_web_plate_l_bolts_one_line(web_plate_h_max, web_plate_h_min, bolts_required,
                                                            min_edge_dist, min_gauge, min_bolts_one_line)
                [gauge, edge_dist, web_plate_h] = self.get_gauge_edge_dist(web_plate_h, bolts_one_line,min_edge_dist, max_spacing, max_edge_dist)

                while web_plate_h is False:
                    bolts_required += 1
                    [bolt_line, bolts_one_line, web_plate_h] = \
                        self.get_web_plate_l_bolts_one_line(web_plate_h_max, web_plate_h_min, bolts_required,
                                                            min_edge_dist, min_gauge, min_bolts_one_line)
                    [gauge, edge_dist, web_plate_h] = self.get_gauge_edge_dist(web_plate_h, bolts_one_line,
                                                                               min_edge_dist, max_spacing,
                                                                               max_edge_dist)

                if bolt_line == 1:
                    pitch = 0.0
                else:
                    pitch = min_gauge

                if shear_ecc is True:
                    # If check for shear eccentricity is true, resultant force in bolt is calculated
                    ecc = (pitch * max((bolt_line - 1.5), 0)) + end_dist + gap
                    moment_demand = shear_load * ecc + web_moment
                    vres = self.get_vres(bolts_one_line, pitch,
                                         gauge, bolt_line, shear_load, axial_load, ecc,web_moment)
                else:
                    moment_demand = 0.0
                    vres = resultant_force / (bolt_line * bolts_one_line)

                if joint == None:
                    bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                                                  gauge, bolt_line, pitch, bolt_capacity,
                                                  bolt_dia)
                else:
                    bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                                                          gauge, bolt_line, pitch, bolt_capacity,
                                                          bolt_dia,end_dist,gap)


            if vres > bolt_capacity_red:
                self.design_status = False
                self.reason = "Bolt line limit is reached. Select higher grade/Diameter or choose different connection"
            else:
                print("passed the web plate details loop for bolt force:", vres, "bolt capaity reduced:",
                      bolt_capacity_red, "no. of bolts:", bolt_line*bolts_one_line, "height", web_plate_h)
                self.design_status = True

            self.length = gap + end_dist * 2 + pitch * (bolt_line - 1)
            self.height = web_plate_h
            self.bolt_line = bolt_line
            self.bolts_one_line = bolts_one_line
            self.bolts_required = bolt_line * bolts_one_line
            self.bolt_capacity_red = bolt_capacity_red
            self.bolt_force = vres
            self.moment_demand = moment_demand
            self.pitch_provided = pitch
            self.gauge_provided = gauge
            self.edge_dist_provided = edge_dist
            self.end_dist_provided = end_dist


    def get_flange_plate_details(self, bolt_dia, flange_plate_h_min, flange_plate_h_max, bolt_capacity, min_edge_dist, min_gauge, max_spacing, max_edge_dist,web_thickness, root_radius,
                              shear_load=0.0, axial_load=0.0, gap=0.0,  bolt_line_limit=math.inf,joint =None):
    #todo anjali
        """

        :param bolt_dia: diameter of bolt
        :param end_dist: minimum end distance
        :param pitch: minimum pitch
        :param flange_plate_h_min: minimum plate height
        :param flange_plate_h_max: maximum plate height
        :param bolt_capacity: capacity of bolt
        :param bolt_line_limit: maximum number of bolt lines allowed
        :param shear_load: load along the height (bolt_line)
        :param axial_load: load along the length
        :param gap: gap between members which adds up to eccentricity
        :param shear_ecc: if eccentricity effect needs to be considered this value should be passed as "True"
        :return: web_plate_h, bolt_line, bolts_one_line, bolts_required, bolt_capacity_red, vres, moment_demand, \
               pitch, gauge, edge_dist, end_dist, a.min_edge_dist_round, a.min_pitch_round, a.max_spacing_round, a.max_edge_dist_round
        """

        # initialising values to start the loop
        res_force = math.sqrt(shear_load ** 2 + axial_load ** 2)
        bolts_required = max(int(math.ceil(res_force / bolt_capacity)), 2)

        [bolt_line, bolts_one_line, flange_plate_h] = self.get_flange_plate_l_bolts_one_line(flange_plate_h_max, flange_plate_h_min, bolts_required, min_edge_dist, min_gauge,
                                           web_thickness, root_radius)
        print("flange",bolt_line, bolts_one_line)

        print("boltdetails0", bolt_line, bolts_one_line, flange_plate_h)


        if bolts_one_line == 1 or bolts_one_line ==0:
            self.design_status = False
            self.reason = "Can't fit two bolts in one line. Select lower diameter."
        elif bolt_line > bolt_line_limit:
            self.design_status = False
            self.reason = "Bolt line limit is reached. Select higher grade/Diameter or choose different connection."
        else:
            print("boltdetails", bolt_line, bolts_one_line,flange_plate_h)
            [gauge, edge_dist, flange_plate_h] = \
                self.get_gauge_edge_dist_flange(flange_plate_h, bolts_one_line, min_edge_dist, max_spacing,
                                                max_edge_dist, web_thickness,root_radius)
            print("boltdetails2", bolt_line, bolts_one_line,flange_plate_h)
            if bolt_line == 1:
                pitch = 0.0
            else:
                pitch = min_gauge
            end_dist = min_edge_dist
            moment_demand = 0.0
            vres = res_force / (bolt_line*bolts_one_line)
            if joint == None:
                bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                                                      gauge, bolt_line, pitch, bolt_capacity,
                                                      bolt_dia)
            else:
                bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                                                      gauge, bolt_line, pitch, bolt_capacity,
                                                      bolt_dia, end_dist, gap,edge_dist,root_radius,web_thickness)

            # while bolt_line <= bolt_line_limit and vres > bolt_capacity_red:
                # [gauge, edge_dist, flange_plate_h] = \
                #     self.get_gauge_edge_dist_flange(flange_plate_h, bolts_one_line, min_edge_dist, max_spacing,
                #                                     max_edge_dist, web_thickness, root_radius)
            while bolt_line <= bolt_line_limit and vres > bolt_capacity_red:
                bolts_required = bolt_line  * bolts_one_line
                bolts_required += 1
                [bolt_line, bolts_one_line, flange_plate_h] = \
                    self.get_flange_plate_l_bolts_one_line(flange_plate_h_max, flange_plate_h_min, bolts_required,
                                                           min_edge_dist, min_gauge,
                                                           web_thickness, root_radius) #

                [gauge, edge_dist, flange_plate_h] = self.get_gauge_edge_dist_flange(flange_plate_h, bolts_one_line,
                                                                                  min_edge_dist, max_spacing,
                                                                                  max_edge_dist,web_thickness,root_radius)
                print("boltdetailsasaa", bolt_line, bolts_one_line, flange_plate_h)
                if bolt_line == 1:
                    pitch = 0.0
                else:
                    pitch = min_gauge
                vres = res_force / (bolt_line * bolts_one_line)
                if joint == None:
                    bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                                                          gauge, bolt_line, pitch, bolt_capacity,
                                                          bolt_dia)
                else:
                    bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                                                          gauge, bolt_line, pitch, bolt_capacity,
                                                          bolt_dia, end_dist, gap,edge_dist,root_radius,web_thickness)
                print("boltforce", vres, bolt_capacity_red)
                # convergence = bolt_capacity_red - vres
                #
                # if convergence < 0:
                #     if count == 0:
                #         initial_convergence = convergence
                #         count = count + 1
                #     else:
                #         if initial_convergence <= convergence:
                #             initial_convergence = convergence
                #         else:
                #             break
                # else:
                #     pass
            #
                # bolt_capacity_red = self.get_bolt_red(bolts_one_line,
                #                                       gauge, bolt_line, pitch, bolt_capacity,
                #                                       bolt_dia, end_dist, gap)
            if vres > bolt_capacity_red:
                self.design_status = False
                self.reason = "Bolt line limit is reached. Select higher grade/Diameter or choose different connection."
            else:
                self.design_status = True

            self.length = gap+ end_dist * 2 + pitch * (bolt_line - 1)
            self.height = flange_plate_h
            self.bolt_line = bolt_line
            self.bolts_one_line = bolts_one_line
            self.bolts_required = bolt_line * bolts_one_line
            self.bolt_capacity_red = bolt_capacity_red
            self.bolt_force = vres
            self.moment_demand = moment_demand
            self.pitch_provided = pitch
            self.gauge_provided = gauge
            self.edge_dist_provided = edge_dist
            self.end_dist_provided = end_dist


    # Function for block shear capacity calculation
    def blockshear(self, numrow, numcol, pitch, gauge, thk, end_dist, edge_dist, dia_hole, fy, fu):
        '''

        Args:
            numrow (str) Number of row(s) of bolts
            dia_hole (int) diameter of hole (Ref. Table 5.6 Subramanian's book, page: 340)
            fy (float) Yeild stress of material
            fu (float) Ultimate stress of material
            edge_dist (float) edge distance based on diameter of hole
            end_dist (float) end distance based on diameter of hole
            pitch (float) pitch distance based on diameter of bolt
            thk (float) thickness of plate or beam web

        Returns:
            Capacity of fin plate under block shear

        '''

        Avg = thk * ((numrow - 1) * gauge + edge_dist)
        Avn = thk * ((numrow - 1) * gauge + edge_dist - (numrow - 0.5) * dia_hole)
        Atg = thk * (pitch * (numcol - 1) + end_dist)
        Atn = thk * (pitch * (numcol - 1) + end_dist - (numcol - 0.5) * dia_hole)
        Tdb1 = (Avg * fy / (math.sqrt(3) * 1.1) + 0.9 * Atn * fu / 1.25)
        Tdb2 = (0.9 * Avn * fu / (math.sqrt(3) * 1.25) + Atg * fy / 1.1)
        Tdb = min(Tdb1, Tdb2)
        Tdb = round(Tdb, 3)
        self.block_shear_capacity = Tdb

    def tension_blockshear_area_input(self,A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1

        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)

        Return:
            block shear strength of bolted connection in N (float)

        Note:
            Reference:
            IS 800:2007, cl. 6.4.1

        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        Tdb = min(T_db1, T_db2)
        # Tdb = round(Tdb, 3)
        self.block_shear_capacity = round(Tdb,2)

    # Check for shear yielding ###
    def shear_yielding(self, length, thickness, fy):
        '''
        Args:
            length (float) length of member in direction of shear load
            thickness(float) thickness of member resisting shear
            beam_fy (float) Yeild stress of section material
        Returns:
            Capacity of section in shear yeiding
        '''
        A_v = length * thickness
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        V_p = (0.6 * A_v * fy) / (math.sqrt(3) * gamma_m0)  # N
        self.shear_yielding_capacity = round(V_p,2)

    def tension_yielding(self, length, thickness, fy):
        '''
        Args:
            length (float) length of member in direction of tension load
            thickness(float) thickness of member resisting tension
            beam_fy (float) Yeild stress of section material
        Returns:
            Capacity of section in tension yeiding
        '''
        A_v = length * thickness
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        # A_v = height * thickness
        tdg = (A_v * fy) / (gamma_m0)
        self.tension_yielding_capacity = round(tdg,2)
        return tdg

    def tension_rupture(self, A_n, F_u):
        "preliminary design strength,T_pdn,as governed by rupture at net section"
        "A_n = net area of the total cross-section"
        "F_u = Ultimate Strength of material"

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_pdn = 0.9 * A_n * F_u / gamma_m1

        self.tension_rupture_capacity = round(T_pdn, 2)

    # Check for shear rupture ###

    # TODO: This formula based on AISC guidelines, check if this should be included
    def shear_rupture_b(self, length, thickness, bolts_one_line, dia_hole, fu):
        '''
        Args:
            A_vn (float) Net area under shear
            beam_fu (float) Ultimate stress of beam material
        Returns:
            Capacity of beam web in shear rupture
        '''
        A_vn = (length - bolts_one_line * dia_hole) * thickness
        R_n = (0.75 * fu * A_vn)
        self.shear_rupture_capacity = round(R_n,2)

    def get_moment_cacacity(self, fy, plate_tk, plate_len):
        self.moment_capacity = 1.2 * (fy / 1.1) * (plate_tk * plate_len ** 2) / 6


    def __repr__(self):
        repr = "Plate\n"
        repr += "Thickness Provided: {}\n".format(self.thickness_provided)
        repr += "Height: {}\n".format(self.height)
        repr += "Length: {}\n".format(self.length)
        repr += "Bolt Lines: {}\n".format(self.bolt_line)
        repr += "Bolts in One Line: {}\n".format(self.bolts_one_line)
        repr += "Bolts Required: {}\n".format(self.bolts_required)
        repr += "Bolt Capacity Reduced: {}\n".format(self.bolt_capacity_red)
        repr += "Bolt Force: {}\n".format(self.bolt_force)
        repr += "Moment Demand: {}\n".format(self.moment_demand)
        repr += "Pitch Provided: {}\n".format(self.pitch_provided)

        repr += "Gauge Provided: {}\n".format(self.gauge_provided)
        repr += "Edge Distance Provided: {}\n".format(self.edge_dist_provided)
        repr += "End Distance Provided: {}\n".format(self.end_dist_provided)

        repr += "Block Shear Capacity: {}\n".format(self.block_shear_capacity)
        repr += "Shear Yielding Capacity: {}\n".format(self.shear_yielding_capacity)
        repr += "Shear Rupture Capacity: {}\n".format(self.shear_rupture_capacity)

        repr += "shear_capacity_web_plate: {}\n".format(self.shear_capacity_web_plate)
        repr += "tension_capacity_web plate: {}\n".format( self.tension_capacity_web_plate)
        repr += "tension_capacity_flange_plate: {}\n".format( self.tension_capacity_flange_plate)

        repr += "Moment Capacity: {}\n".format(self.moment_capacity)
        return repr


class Angle(Section):

    def __init__(self, designation, material_grade):
        super(Angle, self).__init__(material_grade)

        self.designation = designation
        self.leg_a_length = 0.0
        self.leg_b_length = 0.0
        self.thickness = 0.0
        # max_thickness = max(self.flange_thickness, self.web_thickness)

        self.gap = 0.0

        self.connect_to_database_update_other_attributes_angles(designation,material_grade)

        # self.length = 0.0

    def __repr__(self):
        repr = "Angle\n"
        repr += "Designation: {}\n".format(self.designation)
        repr += "rad: {}\n".format(self.rad_of_gy_z)
        return repr

    def connect_to_database_update_other_attributes_angles(self, designation,material_grade):
        conn = sqlite3.connect(PATH_TO_DATABASE)
        # db_query = "SELECT AXB, t FROM Angles WHERE Designation = ?"
        db_query = "SELECT * FROM Angles WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()

        self.mass = row[2]
        self.area = row[3] * 100
        self.a = row[4]
        self.b = row[5]
        self.leg_a_length = self.a
        self.leg_b_length = self.b
        self.max_leg = max(self.leg_a_length,self.leg_b_length)
        self.min_leg = min(self.leg_a_length, self.leg_b_length)
        self.thickness = row[6]
        super(Section, self).__init__(material_grade,self.thickness)
        self.root_radius = row[7]
        self.toe_radius = row[8]
        # if self.leg_a_length != self.leg_b_length:
        #     self.Cz = row[8]*10
        #     self.Cy = row[9]*10
        # else:
        self.Cz = row[9] * 10
        self.Cy = row[10] * 10

        self.mom_inertia_z = row[11] * 10000
        self.mom_inertia_y = row[12] * 10000
        self.alpha = row[13]
        self.mom_inertia_u = row[14] * 10000
        self.mom_inertia_v = row[15] * 10000
        self.rad_of_gy_z = row[16] * 10
        self.rad_of_gy_y = row[17] * 10
        self.rad_of_gy_u = row[18] * 10
        self.rad_of_gy_v = row[19] * 10
        self.elast_sec_mod_z = row[20] * 1000
        self.elast_sec_mod_y = row[21] * 1000
        self.plast_sec_mod_z = row[22] * 1000
        self.plast_sec_mod_y = row[23] * 1000

        self.It = Single_Angle_Properties().calc_TorsionConstantIt(self.leg_a_length,self.leg_b_length,self.thickness) * 10 ** 4 \
            if row[24] is None else row[24] * 10 ** 4
        self.source = row[25]
        self.type = 'Rolled' if row[26] is None else row[26]

        conn.close()


    def angle_weld_length(self, weld_strength, depth_weld, force, C, depth):

        "Function to calculate weld length for angles based on the force transfer pattern"

        f2 = weld_strength * depth_weld
        f3 = force * (1 - C / depth) - f2 / 2
        l3 = f3 / weld_strength

        return l3

    def get_available_seated_list(self, input_angle_list, max_leg_length=math.inf, min_leg_length=0.0, position="outer", t_min = 0.0):
        available_angles = []
        for designation in input_angle_list:
            leg_a_length, leg_b_length, t, r_r = get_leg_lengths(designation)
            if position == "inner":
                min_leg_length_outer = min_leg_length + t + r_r
                max_leg_length_outer = max_leg_length + t + r_r
            else:
                min_leg_length_outer = min_leg_length
                max_leg_length_outer = max_leg_length

            if operator.le(max(leg_a_length, leg_b_length), max_leg_length_outer) and operator.ge(
                    min(leg_a_length, leg_b_length), min_leg_length_outer) and leg_a_length == leg_b_length\
                    and operator.eq(t, t_min):
                # print("appended", designation)
                available_angles.append(designation)
            else:
                print("popped", designation)
        return available_angles



class I_sectional_Properties(object):

    def calc_Mass(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.A = ((2 * B * t_f) + ((D - 2 * t_f) * t_w)) / 100
        self.M = 7850 * self.A / 10000
        return round(self.M,1)

    def calc_Area(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.A = ((2*B*t_f) + ((D-2*t_f)*t_w))/100
        return round(self.A,1)

    def calc_MomentOfAreaZ(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.I_zz = ((D - 2*t_f)**3 * t_w /12 + (B*t_f**3)/6+(B/2*t_f*(D-t_f)**2))/10000
        return round(self.I_zz,1)

    def calc_MomentOfAreaY(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.I_yy = ((D-2*t_f)*t_w**3 /12 + B**3*t_f/6)/10000
        return round(self.I_yy,1)

    def calc_RogZ(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.A = ((2*B*t_f) + ((D-2*t_f)*t_w))/100
        self.I_zz = ((D - 2*t_f)**3 * t_w /12 + (B*t_f**3)/6+(B/2*t_f*(D-t_f)**2))/10000
        self.r_z = math.sqrt(self.I_zz / self.A)
        return round(self.r_z,2)

    def calc_RogY(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.A = ((2*B*t_f) + ((D-2*t_f)*t_w))/100
        self.I_yy = ((D-2*t_f)*t_w**3 /12 + B**3*t_f/6)/10000
        self.r_y = math.sqrt(self.I_yy / self.A)
        return round(self.r_y,2)

    def calc_ElasticModulusZz(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.I_zz = ((D - 2*t_f)**3 * t_w /12 + (B*t_f**3)/6+(B/2*t_f*(D-t_f)**2))/10000
        self.Z_ez = (self.I_zz * 2*10) / (D)
        return round(self.Z_ez,1)

    def calc_ElasticModulusZy(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.I_yy = ((D-2*t_f)*t_w**3 /12 + B**3*t_f/6)/10000
        self.Z_ey = (self.I_yy * 2*10) / (B)
        return round(self.Z_ey,1)

    def calc_PlasticModulusZpz(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.A = ((2*B*t_f) + ((D-2*t_f)*t_w))/100
        self.y_p = (((D - 2*t_f)**2*t_w/8 + B*t_f*(D-t_f)/2) / ((D-t_f)/2*t_w + B*t_f ))/10
        self.Z_pz =(2 * (self.A / 2 * self.y_p))
        return round(self.Z_pz,1)

    def calc_PlasticModulusZpy(self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        self.A = ((2*B*t_f) + ((D-2*t_f)*t_w))/100
        self.z_p = ((((D-2*t_f)*t_w**2)/8 + (B*t_f*B)/4)/((D-2*t_f)*t_w/2 + (B*t_f)))
        self.Z_py = 2 * (self.A / 2 * self.z_p)
        return round(self.Z_py,1)

    #TODO:add formula
    def calc_torsion_const (self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        return 0.0

    def calc_warping_const (self,D,B,t_w,t_f,alpha=90,r_1=0,r_2=0):
        return 0.0


class Single_Angle_Properties(object):

    "return in cm "

    def calc_Mass(self,a,b,t,l):
        self.A = t * (a+b-t)
        self.M = 7850 * self.A / 1000000
        return self.M

    def calc_Area(self,a,b,t,l):
        self.A = t * (a+b-t)
        return round(self.A/100,2)

    def calc_Cy(self,a,b,t,l):
        self.A = t * (a + b - t)
        self.Cy=((0.5 * (b*a**2))-(0.5*(b-t)*(a**2 - t**2)))/self.A
        return round(self.Cy/10,2)

    def calc_Cz(self,a,b,t,l):
        self.A = t * (a + b - t)
        self.Cz = ((0.5 * (b**2) * a) - (0.5 * (b**2 - t**2) * (a - t))) / self.A
        return round(self.Cz/10, 2)

    def calc_MomentOfAreaZ(self,a,b,t,l):
        Cya = self.calc_Cy(a,b,t,l) *10
        self.I_zz = (a**3*b)/12 - ((b-t)*(a-t)**3)/12 + (a*b*(a/2-Cya)**2) - ((a-t)*(b-t)*((a+t)/2-Cya)**2)
        return round(self.I_zz/10000, 2)

    def calc_MomentOfAreaY(self,a,b,t,l):
        Cza = self.calc_Cz(a, b, t,l) *10
        self.I_yy = (b ** 3 * a) / 12 - ((a - t) * (b - t) ** 3) / 12 + (a * b * (b / 2 - Cza) ** 2) - (
                    (a - t) * (b - t) * ((b + t) / 2 - Cza)**2)
        return round(self.I_yy/10000, 2)

    def calc_MomentOfAreaYZ(self,a,b,t,l):
        Cza = self.calc_Cz(a, b, t,l)*10
        Cya = self.calc_Cy(a, b, t,l)*10
        self.I_yz = a*b*(a/2-Cya) * (b/2-Cza) - ((a-t)*(b-t)*(0.5*(a+t)-Cya)*(0.5*(b+t)-Cza))
        # self.I_yz = 1.000
        return round(self.I_yz/10000, 2)

    def calc_MomentOfAreaU(self,a,b,t,l):
        I_zza = self.calc_MomentOfAreaZ(a, b, t,l)
        I_yya = self.calc_MomentOfAreaY( a, b, t,l)
        I_yza = self.calc_MomentOfAreaYZ( a, b, t,l)
        self.I_u = 0.5*(I_zza + I_yya) + math.sqrt(0.25 * (I_zza - I_yya)**2 + I_yza**2 )
        return round(self.I_u, 2)

    def calc_MomentOfAreaV(self,a,b,t,l):
        I_zza = self.calc_MomentOfAreaZ(a, b, t,l)
        I_yya = self.calc_MomentOfAreaY(a, b, t,l)
        I_yza = self.calc_MomentOfAreaYZ(a, b, t,l)
        self.I_v = 0.5*(I_zza + I_yya) - math.sqrt(0.25 * (I_zza - I_yya) ** 2 + I_yza ** 2)
        return round(self.I_v, 2)

    def calc_RogZ(self,a,b,t,l):
        I_zza = self.calc_MomentOfAreaZ(a, b, t,l)
        Aa = self.calc_Area(a, b, t,l)
        self.r_z = math.sqrt(I_zza/Aa)

        return round(self.r_z, 2)

    def calc_RogY(self,a,b,t,l):
        I_yya = self.calc_MomentOfAreaY(a, b, t,l)
        Aa = self.calc_Area( a, b, t,l)
        self.r_y = math.sqrt(I_yya / Aa)

        return round(self.r_y, 2)

    def calc_RogU(self,a,b,t,l):
        I_ua = self.calc_MomentOfAreaU(a, b, t,l)
        Aa = self.calc_Area(a, b, t,l)
        self.r_u = math.sqrt(I_ua / Aa)

        return round(self.r_u, 2)

    def calc_RogV(self,a,b,t,l):
        I_va = self.calc_MomentOfAreaV(a, b, t,l)
        Aa = self.calc_Area(a, b, t,l)
        self.r_v = math.sqrt(I_va/ Aa)

        return round(self.r_v, 2)

    def calc_ElasticModulusZz(self,a,b,t,l):
        I_zza = self.calc_MomentOfAreaZ(a, b, t,l)
        Cya = self.calc_Cy(a, b, t,l)
        self.Z_zz = I_zza/(a/10-Cya)
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self,a,b,t,l):
        I_yya = self.calc_MomentOfAreaY(a, b, t,l)
        Cza = self.calc_Cz(a, b, t,l)
        self.Z_yy = I_yya / (b/10 - Cza)
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self,a,b,t,l):
        Aa = self.calc_Area(a, b, t,l)*100
        self.Z_pz = t * (b-t) * (a- (0.5* Aa/t)-0.5*t) + 0.5* t*(a**2 + (Aa/t)**2 - a*(Aa/t))
        # self.Z_pz = t * (b-t) * (a- 0.5* Aa/t-0.5*t)

        # self.Z_pz = 1.000
        return round(self.Z_pz/1000, 2)

    def calc_PlasticModulusZpy(self,a,b,t,l):
        Aa = self.calc_Area(a, b, t,l)*100
        self.Z_py = t * (a - t) * (b - 0.5 * Aa / t - 0.5 * t) + 0.5 * t*(b ** 2 + (Aa / t) ** 2 - b * (Aa / t))
        # self.Z_py = t * (a - t) * (b - 0.5 * Aa / t - 0.5 * t)

        # self.Z_py = 1.000
        return round(self.Z_py/1000, 2)

    def calc_TorsionConstantIt(self,a,b,t,l):

        self.I_t = ((b*(t**3))/3) + ((a-t)*(t**3)/3)
        return round(self.I_t/10000, 2)

class BBAngle_Properties():
    "return in cm "

    def __init__(self):
        self.db = False

    def data(self,designation, material_grade):
        self.Angle_attributes = Angle(designation, material_grade)
        self.Angle_attributes.connect_to_database_update_other_attributes_angles(designation, material_grade)
        self.db = True

    def calc_Mass(self,a,b,t,l):
        self.A = self.calc_Area(a,b,t,l)
        self.M = 7850 * self.A / 10000
        return self.M

    def calc_Area(self,a,b,t,l):
        if self.db == False:
            self.A = 2 * t * (a + b - t)
        else:
            self.A = 2 * self.Angle_attributes.area
        return round(self.A/100,2)

    def calc_Cy(self,a,b,t,l):
        if self.db == False:
            self.A = t * (a + b - t)
            self.Cy = ((0.5 * (b * a ** 2)) - (0.5 * (b - t) * (a ** 2 - t ** 2))) / self.A
        else:
            self.Cy = self.Angle_attributes.Cy
        return round(self.Cy / 10, 2)

    def calc_Cz(self,a,b,t,l):
        if self.db == False:
            self.A = t * (a + b - t)
            self.Cz = ((0.5 * (b ** 2) * a) - (0.5 * (b ** 2 - t ** 2) * (a - t))) / self.A
        else:
            self.Cz = self.Angle_attributes.Cz
        return round(self.Cz / 10, 2)

    def calc_MomentOfAreaZ(self,a,b,t,l):
        if self.db == False:
            if l == "Long Leg":
                self.I_zz = 2* Single_Angle_Properties.calc_MomentOfAreaZ(self,a,b,t,l) *10000
            else:
                mom_inertia_z = Single_Angle_Properties.calc_MomentOfAreaZ(self,a,b,t,l) *10000
                area = Single_Angle_Properties.calc_Area(self,a,b,t,l)*100
                Cg_1 = self.calc_Cz(a,b,t,l)*10
                thickness = 0
                self.I_zz = (mom_inertia_z + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
        else:
            if l == "Long Leg":
                self.I_zz =  2 * self.Angle_attributes.mom_inertia_z
            else:
                mom_inertia_z = self.Angle_attributes.mom_inertia_z
                area = self.Angle_attributes.area
                Cg_1 = self.calc_Cz(a,b,t,l)*10
                thickness = 0
                self.I_zz = (mom_inertia_z + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
        return round(self.I_zz/10000, 2)

    def calc_MomentOfAreaY(self,a,b,t,l):
        if self.db == False:
            if l == "Long Leg":
                mom_inertia_y = Single_Angle_Properties.calc_MomentOfAreaY(self,a, b, t, l) * 10000
                area = Single_Angle_Properties.calc_Area(self,a, b, t, l) * 100
                Cg_1 = self.calc_Cy(a, b, t, l) * 10
                thickness = 0
                self.I_yy= (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
            else:
                self.I_yy = 2 * Single_Angle_Properties.calc_MomentOfAreaY(self, a, b, t, l) * 10000

        else:
            if l == "Long Leg":
                mom_inertia_y = self.Angle_attributes.mom_inertia_y
                area = self.Angle_attributes.area
                Cg_1 = self.Angle_attributes.Cy
                thickness = 0
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
            else:
                self.I_yy = 2* self.Angle_attributes.mom_inertia_y
        return round(self.I_yy/10000, 2)

    def calc_RogZ(self,a,b,t,l):

        mom_inertia_z = self.calc_MomentOfAreaZ(a, b, t, l)
        area = self.calc_Area(a,b,t,l)
        self.r_z = math.sqrt(mom_inertia_z/area)

        return round(self.r_z, 2)

    def calc_RogY(self,a,b,t,l):
        mom_inertia_y = self.calc_MomentOfAreaY(a, b, t, l)
        area = self.calc_Area(a,b,t,l)
        self.r_y = math.sqrt(mom_inertia_y / area)

        return round(self.r_y , 2)

    def calc_ElasticModulusZz(self,a,b,t,l):
        mom_inertia_z = self.calc_MomentOfAreaZ(a, b, t, l)
        if l == "Long Leg":
            self.Z_zz = 1000
        else:
            self.Z_zz = mom_inertia_z/(a/10)
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self,a,b,t,l):
        mom_inertia_y = self.calc_MomentOfAreaY(a, b, t, l)
        if l == "Long Leg":
            self.Z_yy = mom_inertia_y/(b/10)
        else:
            self.Z_yy = 1000
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self,a,b,t,l):
        Aa = self.calc_Area(a, b, t,l)
        self.Z_pz = 1
        # self.Z_pz = t * (b-t) * (a- 0.5* Aa/t-0.5*t)

        # self.Z_pz = 1.000
        return round(self.Z_pz, 2)

    def calc_PlasticModulusZpy(self,a,b,t,l):
        Aa = self.calc_Area(a, b, t,l)
        self.Z_py = 1
        # self.Z_py = t * (a - t) * (b - 0.5 * Aa / t - 0.5 * t)

        # self.Z_py = 1.000
        return round(self.Z_py, 2)

    def calc_TorsionConstantIt(self,a,b,t,l):

        self.I_t = 1
        return round(self.I_t, 2)

class SAngle_Properties(object):

    def __init__(self):
        self.db = False

    def data(self,designation, material_grade):
        self.Angle_attributes = Angle(designation, material_grade)
        self.Angle_attributes.connect_to_database_update_other_attributes_angles(designation, material_grade)
        self.db = True

    def calc_Mass(self, a, b, t, l):
        self.A = self.calc_Area(a, b, t, l)
        self.M = 7850 * self.A / 10000
        return self.M

    def calc_Area(self, a, b, t, l):
        if self.db == False:
            self.A = 2 * t * (a + b - t)
        else:
            self.A = 2 * self.Angle_attributes.area
        return round(self.A / 100, 2)

    def calc_Cy(self, a, b, t, l):
        if self.db == False:
            self.A = t * (a + b - t)
            self.Cy = ((0.5 * (b * a ** 2)) - (0.5 * (b - t) * (a ** 2 - t ** 2))) / self.A
        else:
            self.Cy = self.Angle_attributes.Cy
        return round(self.Cy / 10, 2)

    def calc_Cz(self, a, b, t, l):
        if self.db == False:
            self.A = t * (a + b - t)
            self.Cz = ((0.5 * (b ** 2) * a) - (0.5 * (b ** 2 - t ** 2) * (a - t))) / self.A
        else:
            self.Cz = self.Angle_attributes.Cz
        return round(self.Cz / 10, 2)

    def calc_MomentOfAreaZ(self, a, b, t, l):
        if self.db == False:
            if l == "Long Leg":
                mom_inertia_z = Single_Angle_Properties.calc_MomentOfAreaZ(self, a, b, t, l) * 10000
                area = Single_Angle_Properties.calc_Area(self, a, b, t, l) * 100
                Cg_1 = self.calc_Cz(a, b, t, l) * 10
                self.I_zz = (mom_inertia_z + (area * (Cg_1 ) * (Cg_1 ))) * 2
            else:
                mom_inertia_z = Single_Angle_Properties.calc_MomentOfAreaZ(self, a, b, t, l) * 10000
                area = Single_Angle_Properties.calc_Area(self, a, b, t, l) * 100
                Cg_1 = self.calc_Cz(a, b, t, l) * 10
                thickness = 0
                self.I_zz = (mom_inertia_z + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2

        else:
            if l == "Long Leg":
                mom_inertia_z = self.Angle_attributes.mom_inertia_z
                area = self.Angle_attributes.area
                Cg_1 = self.calc_Cz(a, b, t, l) * 10
                self.I_zz = (mom_inertia_z + (area * (Cg_1 ) * (Cg_1 ))) * 2
            else:
                mom_inertia_z = self.Angle_attributes.mom_inertia_z
                area = self.Angle_attributes.area
                Cg_1 = self.calc_Cz(a, b, t, l) * 10
                thickness = 0
                self.I_zz = (mom_inertia_z + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
        return round(self.I_zz / 10000, 2)

    def calc_MomentOfAreaY(self,a,b,t,l):
        if self.db == False:
            if l == "Long Leg":
                mom_inertia_y = Single_Angle_Properties.calc_MomentOfAreaY(self, a, b, t, l) * 10000
                area = Single_Angle_Properties.calc_Area(self, a, b, t, l) * 100
                Cg_1 = self.calc_Cy(a, b, t, l) * 10
                thickness = 0
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
            else:
                mom_inertia_y = Single_Angle_Properties.calc_MomentOfAreaY(self, a, b, t, l) * 10000
                area = Single_Angle_Properties.calc_Area(self, a, b, t, l) * 100
                Cg_1 = self.calc_Cy(a, b, t, l) * 10
                self.I_yy = (mom_inertia_y + (area * (Cg_1) * (Cg_1 ))) * 2

        else:
            if l == "Long Leg":
                mom_inertia_y = self.Angle_attributes.mom_inertia_y
                area = self.Angle_attributes.area
                Cg_1 = self.calc_Cy(a, b, t, l) * 10
                thickness = 0
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2

            else:
                mom_inertia_y = self.Angle_attributes.mom_inertia_y
                area = self.Angle_attributes.area
                Cg_1 = self.calc_Cy(a, b, t, l) * 10
                self.I_yy = (mom_inertia_y + (area * (Cg_1) * (Cg_1 ))) * 2

        return round(self.I_yy / 10000, 2)

    def calc_RogZ(self,a,b,t,l):
        mom_inertia_z = self.calc_MomentOfAreaZ(a, b, t, l)
        area = self.calc_Area(a, b, t, l)
        self.r_z = math.sqrt(mom_inertia_z / area)

        return round(self.r_z, 2)

    def calc_RogY(self,a,b,t,l):
        mom_inertia_y = self.calc_MomentOfAreaY(a, b, t, l)
        area = self.calc_Area(a, b, t, l)
        self.r_y = math.sqrt(mom_inertia_y / area)

        return round(self.r_y, 2)

    def calc_ElasticModulusZz(self,a,b,t,l):
        mom_inertia_z = self.calc_MomentOfAreaZ(a, b, t, l)
        # if l == "Long Leg":
        self.Z_zz = mom_inertia_z / (a / 10)
        # else:
        #     self.Z_zz = mom_inertia_z / (a / 10)
        return round(self.Z_zz, 2)


    def calc_ElasticModulusZy(self,a,b,t,l):
        mom_inertia_y = self.calc_MomentOfAreaY(a, b, t, l)
        # if l == "Long Leg":
        self.Z_yy = mom_inertia_y / (b / 10)
        # else:
        #     self.Z_zz = mom_inertia_z / (a / 10)
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self,a,b,t,l):
        Aa = self.calc_Area(a, b, t,l)
        self.Z_pz = 2
        # self.Z_pz = t * (b-t) * (a- 0.5* Aa/t-0.5*t)

        # self.Z_pz = 1.000
        return round(self.Z_pz, 2)

    def calc_PlasticModulusZpy(self,a,b,t,l):
        Aa = self.calc_Area(a, b, t,l)
        self.Z_py = 2
        # self.Z_py = t * (a - t) * (b - 0.5 * Aa / t - 0.5 * t)

        # self.Z_py = 1.000
        return round(self.Z_py, 2)

    def calc_TorsionConstantIt(self,a,b,t,l):

        self.I_t = 2
        return round(self.I_t, 2)


class Single_Channel_Properties(object):

    def calc_Mass(self,f_w,f_t,w_h,w_t):
        print(f_w,f_t,w_h,w_t)
        Ac = self.calc_Area(f_w,f_t,w_h,w_t)
        self.M = 7850 * Ac / 10000
        return round(self.M,2)

    def calc_Area(self,f_w,f_t,w_h,w_t):
        self.A = f_w * w_h - (w_h - 2 * f_t) * (f_w - w_t)
        return round(self.A/100,2)

    def calc_C_y(self,f_w,f_t,w_h,w_t):
        Ac = self.calc_Area(f_w, f_t, w_h, w_t) *100
        # self.Cy = ((f_w * (w_h**2)/2) - ((f_w - w_t)**2 * (w_h - (2 * f_t))/2))/Ac
        self.Cy = ((w_h * (f_w ** 2) / 2) - (f_w - w_t) * (w_h - (2 * f_t)) * (w_t+(f_w-w_t)/2))/ Ac
        return round(self.Cy/10,2)

    def calc_MomentOfAreaZ(self,f_w,f_t,w_h,w_t):
        self.I_zz = (f_w * w_h**3)/12 - ((f_w -w_t)*(w_h - 2 * f_t)**3)/12
        print(self.I_zz,"duvbdf")
        return round(self.I_zz/10000,2)

    def calc_MomentOfAreaY(self,f_w,f_t,w_h,w_t):
        Cyc = self.calc_C_y(f_w,f_t,w_h,w_t)*10
        # Cyc = 13.2
        # self.I_yy = (w_h * (f_w**3)/12) + (f_w * w_h * (Cyc - (f_w/2))**2) - (((w_h - (2 * f_t)) * ((f_w - w_t)**3)/12) - ((w_h - (2 * f_t)) * (f_w - w_t) * (Cyc - ((f_w+w_t)/2))**2))
        self.I_yy = ((w_h * f_w ** 3) / 12) + w_h * f_w * (Cyc - (f_w / 2))** 2 - (((w_h - 2 * f_t) * (f_w - w_t)**3) / 12) - (
                    w_h - 2 * f_t) * (f_w - w_t) * (Cyc - ((f_w + w_t) / 2))** 2
        return round(self.I_yy/10000, 2)

    def calc_RogZ(self,f_w,f_t,w_h,w_t):
        Ac = self.calc_Area(f_w, f_t, w_h, w_t)
        I_zzc = self.calc_MomentOfAreaZ(f_w,f_t,w_h,w_t)
        self.R_zz = math.sqrt(I_zzc/Ac)
        return round(self.R_zz, 2)

    def calc_RogY(self,f_w,f_t,w_h,w_t):
        Ac = self.calc_Area(f_w, f_t, w_h, w_t)
        I_yyc = self.calc_MomentOfAreaY(f_w, f_t, w_h, w_t)
        self.R_yy = math.sqrt(I_yyc/Ac)
        return round(self.R_yy, 2)

    def calc_ElasticModulusZz(self,f_w,f_t,w_h,w_t):
        I_zzc = self.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t)
        self.Z_zz = I_zzc/(0.5 * (w_h/10))
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self,f_w,f_t,w_h,w_t):
        Cyc = self.calc_C_y(f_w, f_t, w_h, w_t)
        I_yyc = self.calc_MomentOfAreaY(f_w, f_t, w_h, w_t)
        self.Z_yy = I_yyc / ((f_w/10) - Cyc)
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self,f_w,f_t,w_h,w_t):
        self.Z_pz = f_w * (w_h**2)/4  - (f_w - w_t) * ((w_h - 2 * f_t)**2)/4
        return round(self.Z_pz/1000, 2)

    def calc_PlasticModulusZpy(self,f_w,f_t,w_h,w_t):

        Ac = self.calc_Area(f_w, f_t, w_h, w_t) * 100
        self.Z_py = f_t * (Ac/4 * f_t)**2 + f_t * (f_w - w_t -(Ac/4*f_t))**2 + w_h * w_t * (f_w - 0.5 * w_t - Ac/4 * f_t)**2
        return round(self.Z_py/1000, 2)

    def calc_torsion_const_It(self,f_w,f_t,w_h,w_t):
        a = 0.0
        return a

    def calc_warping_const_Iw(self,f_w,f_t,w_h,w_t):
        a = 0.0
        return a

class BBChannel_Properties(object):

    def __init__(self):
        self.db = False

    def data(self,designation, material_grade):
        self.Channel_attributes = Channel(designation, material_grade)
        self.Channel_attributes.connect_to_database_update_other_attributes_channels(designation, material_grade)
        self.db = True

    def calc_Mass(self,f_w,f_t,w_h,w_t):
        self.A = self.calc_Area(f_w,f_t,w_h,w_t)
        self.M = 7850 * self.A / 10000
        return self.M

    def calc_Area(self,f_w,f_t,w_h,w_t):
        if self.db == False:
            self.A = 2 * (f_w * w_h - (w_h - 2 * f_t) * (f_w - w_t))
        else:
            self.A = 2 * self.Channel_attributes.area
        return round(self.A / 100, 2)
    #
    def calc_C_y(self,f_w,f_t,w_h,w_t):
        if self.db == False:
            Ac = Single_Channel_Properties.calc_Area(self,f_w, f_t, w_h, w_t)*100
            self.Cy = ((w_h * (f_w ** 2) / 2) - (f_w - w_t) * (w_h - (2 * f_t)) * (w_t + (f_w - w_t) / 2)) / Ac
        else:
            self.Cy = self.Channel_attributes.Cy
        return round(self.Cy / 10, 2)

    def calc_MomentOfAreaZ(self,f_w,f_t,w_h,w_t):
        if self.db == False:
            self.I_zz = 2* Single_Channel_Properties.calc_MomentOfAreaZ(self,f_w, f_t, w_h, w_t) * 10000
        else:
            self.I_zz = 2 * self.Channel_attributes.mom_inertia_z

        return round(self.I_zz / 10000, 2)

    def calc_MomentOfAreaY(self,f_w,f_t,w_h,w_t):
        if self.db == False:
            mom_inertia_y = Single_Channel_Properties.calc_MomentOfAreaY(self,f_w, f_t, w_h, w_t)
            area = Single_Channel_Properties.calc_Area(self,f_w, f_t, w_h, w_t)
            Cg_1 = self.calc_C_y(f_w,f_t,w_h,w_t)
            thickness = 0
            self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2
        else:
            mom_inertia_y = self.Channel_attributes.mom_inertia_y/10000
            area = self.Channel_attributes.area/100
            Cg_1 = self.calc_C_y(f_w,f_t,w_h,w_t)
            thickness = 0
            self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness) * (Cg_1 + thickness))) * 2

        return round(self.I_yy, 2)


    def calc_RogZ(self,f_w,f_t,w_h,w_t):
        mom_inertia_z = self.calc_MomentOfAreaZ(f_w,f_t,w_h,w_t)
        area = self.calc_Area(f_w,f_t,w_h,w_t)
        self.r_z = math.sqrt(mom_inertia_z / area)

        return round(self.r_z, 2)

    def calc_RogY(self,f_w,f_t,w_h,w_t):
        mom_inertia_y = self.calc_MomentOfAreaY(f_w, f_t, w_h, w_t)
        area = self.calc_Area(f_w, f_t, w_h, w_t)
        self.r_y = math.sqrt(mom_inertia_y/ area)

        return round(self.r_y, 2)

    def calc_ElasticModulusZz(self,f_w,f_t,w_h,w_t):
        I_zzc = self.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t)
        self.Z_zz = I_zzc / (0.5 * (w_h/10))
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self,f_w,f_t,w_h,w_t):
        I_yyc = self.calc_MomentOfAreaY(f_w, f_t, w_h, w_t)
        self.Z_yy = I_yyc / (f_w/10)
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self,f_w,f_t,w_h,w_t):
        self.Z_pz = 2*f_w * (w_h ** 2) / 4 - 2*((f_w - w_t) * ((w_h - 2 * f_t) ** 2) / 4)
        return round(self.Z_pz / 1000, 2)

    def calc_PlasticModulusZpy(self,f_w,f_t,w_h,w_t):
        self.Z_py = 2 * w_h * ((2*f_w) ** 2) / 4 - 2 * ((w_h - 2 * f_t) * ((f_w - w_t) ** 2)/4)
        return round(self.Z_py / 1000, 2)

    def calc_torsion_const_It(self,f_w,f_t,w_h,w_t):
        a = 0.0
        return a

    def calc_warping_const_Iw(self,f_w,f_t,w_h,w_t):
        a = 0.0
        return a