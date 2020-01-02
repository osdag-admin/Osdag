from utils.common.is800_2007 import IS800_2007
from utils.common.material import *
from utils.common.other_standards import *
from Common import *
import sqlite3
import math
import numpy as np

class Bolt(Material):

    def __init__(self, grade=0.0, diameter=0.0, bolt_type="", material_grade="", bolt_hole_type="",
                 edge_type="",connecting_plates_tk=[], mu_f=0.0, corrosive_influences=True):
        super(Bolt, self).__init__(material_grade)
        self.bolt_grade = float(grade)
        self.bolt_diameter = float(diameter)
        self.bolt_type = bolt_type
        self.bolt_hole_type = bolt_hole_type
        self.edge_type = edge_type
        self.mu_f = float(mu_f)
        self.connecting_plates_tk = list(np.float_(connecting_plates_tk))
        self.bolt_shear_capacity = 0.0
        self.bolt_bearing_capacity = 0.0
        self.bolt_capacity = 0.0
        self.no_of_bolts = 0
        self.bolt_group_capacity = 0.0
        self.bolt_fu = 0.0
        self.bolt_fy = 0.0
        if corrosive_influences == "Yes":
            self.corrosive_influences = True
        else:
            self.corrosive_influences = False
        [self.bolt_shank_area, self.bolt_net_area] = IS1367_Part3_2002.bolt_area(self.bolt_diameter)
        self.min_pitch = IS800_2007.cl_10_2_2_min_spacing(self.bolt_diameter)
        self.min_gauge = IS800_2007.cl_10_2_2_min_spacing(self.bolt_diameter)
        self.min_edge_dist = IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter, self.bolt_hole_type, self.edge_type)
        self.min_end_dist = self.min_edge_dist
        self.max_spacing = IS800_2007.cl_10_2_3_1_max_spacing(self.connecting_plates_tk)
        self.max_edge_dist = IS800_2007.cl_10_2_4_3_max_edge_dist(self.connecting_plates_tk, self.fy, self.corrosive_influences)
        self.max_end_dist = self.max_edge_dist
        self.dia_hole = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter, self.bolt_hole_type)


    def __repr__(self):
        repr = "Bolt\n"
        repr += "Diameter: {}\n".format(self.bolt_diameter)
        repr += "Type: {}\n".format(self.bolt_type)
        repr += "Grade: {}\n".format(self.bolt_grade)
        repr += "Bolt Shear Capacity: {}\n".format(self.bolt_shear_capacity)
        repr += "Bolt Bearing Capacity: {}\n".format(self.bolt_bearing_capacity)
        repr += "Bolt Capacity: {}\n".format(self.bolt_capacity)
        return repr

    def calculate_bolt_shear_capacity(self, n_planes):
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

        [self.bolt_fu, self.bolt_fy] = IS1367_Part3_2002.get_bolt_fu_fy(self.bolt_grade)
        if self.bolt_type == "Bearing Bolt":
            self.bolt_shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity(
                f_u=self.bolt_fu, A_nb=self.bolt_net_area, A_sb=self.bolt_shank_area, n_n=n_planes, n_s=0)
            self.bolt_bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
                f_u=self.fu, f_ub=self.bolt_fu, t=min(self.connecting_plates_tk), d=self.bolt_diameter,
                e=self.min_edge_dist, p=self.min_pitch, bolt_hole_type=self.bolt_hole_type)
            self.bolt_capacity = [self.bolt_shear_capacity, self.bolt_bearing_capacity]

        elif self.bolt_type == "Friction Grip Bolt":
            self.bolt_shear_capacity = IS800_2007.cl_10_4_3_bolt_slip_resistance(
                f_ub=self.bolt_fu, A_nb=self.bolt_net_area, n_e=n_planes, mu_f=self.mu_f, bolt_hole_type=self.bolt_hole_type)
            self.bolt_bearing_capacity = 'N/A'
            self.bolt_capacity = [self.bolt_shear_capacity, self.bolt_bearing_capacity]

        return self.bolt_capacity, self.bolt_fu, self.bolt_fy
        pass


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
        super(Section, self).__init__(material_grade)
        self.designation = designation
        self.mass = 0.0
        self.area = 0.0
        self.depth = 0.0
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
        self.source = 0.0

    def connect_to_database_update_other_attributes(self, table, designation):
        conn = sqlite3.connect(PATH_TO_DATABASE)
        db_query = "SELECT * FROM " + table + " WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()
        self.mass = row[2]
        self.area = row[3]
        self.depth = row[4]
        self.flange_width = row[5]
        self.web_thickness = row[6]
        self.flange_thickness = row[7]
        self.flange_slope = row[18]
        self.root_radius = row[8]
        self.toe_radius = row[9]
        self.mom_inertia_z = row[10]
        self.mom_inertia_y = row[11]
        self.rad_of_gy_z = row[12]
        self.rad_of_gy_y = row[13]
        self.elast_sec_mod_z = row[14]
        self.elast_sec_mod_y = row[15]
        self.plast_sec_mod_z = row[16]
        self.plast_sec_mod_y = row[17]
        self.source = row[19]

        conn.close()

    def __repr__(self):
        repr = "Section\n"
        repr += "Designation: {}\n".format(self.designation)
        repr += "fy: {}\n".format(self.fy)
        repr += "fu: {}\n".format(self.fu)
        return repr

class Beam(Section):

    def __init__(self, designation, material_grade):
        super(Beam, self).__init__(designation, material_grade)
        self.connect_to_database_update_other_attributes("Beams", designation)


class Column(Section):

    def __init__(self, designation, material_grade):
        super(Column, self).__init__(designation, material_grade)
        self.connect_to_database_update_other_attributes("Columns", designation)


class Weld(Material):

    def __init__(self, size=0.0, length=0.0, material_grade=""):
        self.size = size
        self.length = length
        super(Weld, self).__init__(material_grade)

    def __repr__(self):
        repr = "Weld\n"
        repr += "Size: {}\n".format(self.size)
        repr += "Length: {}\n".format(self.length)
        return repr


class Plate(Material):

    def __init__(self, thickness=0.0, height=0.0, width=0.0, material_grade=""):
        super(Plate, self).__init__(material_grade)
        self.thickness = thickness
        self.height = height
        self.width = width

    def __repr__(self):
        repr = "Plate\n"
        repr += "Thickness: {}\n".format(self.thickness)
        return repr


class Angle(Material):

    def __init__(self, designation, material_grade):
        super(Angle, self).__init__(material_grade)
        self.designation = designation

        self.leg_a_length = 0.0
        self.leg_b_length = 0.0
        self.thickness = 0.0

        self.connect_to_database_update_other_attributes(designation)

        self.length = 0.0

    def __repr__(self):
        repr = "Angle\n"
        repr += "Designation: {}\n".format(self.designation)
        return repr

    def connect_to_database_update_other_attributes(self, designation):
        conn = sqlite3.connect(PATH_TO_DATABASE)
        db_query = "SELECT AXB, t FROM Angles WHERE Designation = ?"
        cur = conn.cursor()
        cur.execute(db_query, (designation,))
        row = cur.fetchone()

        axb = row[0]
        axb = axb.lower()
        self.leg_a_length = float(axb.split("x")[0])
        self.leg_b_length = float(axb.split("x")[1])
        self.thickness = row[1]

        conn.close()

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
