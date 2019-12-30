from utils.common.material import Material
from utils.common.is800_2007 import IS800_2007
import sqlite3
import math


class Component(object):

    def __init__(self, material=Material()):
        self.material = material
        self.path_to_database = "ResourceFiles/Database/Intg_osdag.sqlite"

class Bolt(Component):

    def __init__(self, grade=0.0, diameter=0.0, bolt_type="", length=0.0, material=Material()):
        super(Bolt, self).__init__(material)
        self.grade = grade
        self.diameter = diameter
        self.bolt_type = bolt_type
        self.length = length
        self.shear_capacity = 0.0
        self.bearing_capacity = 0.0
        self.bolt_capacity = 0.0
        self.no_of_bolts = 0
        self.bolt_group_capacity = 0.0


    def __repr__(self):
        repr = "Bolt\n"
        repr += "Diameter: {}\n".format(self.diameter)
        repr += "Type: {}\n".format(self.bolt_type)
        repr += "Grade: {}\n".format(self.grade)
        repr += "Length: {}".format(self.length)
        return repr

    def calculate_bolt_shear_capacity(self, bolt_diameter):
        # self.shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity()
        # TODO : Bolt shear capacity functions
        pass


class Nut(Component):

    def __init__(self, diameter=0.0, material=Material()):
        self.diameter = diameter
        super(Nut, self).__init__(material)

    def __repr__(self):
        repr = "Nut\n"
        repr += "Diameter: {}".format(self.diameter)
        return repr


class Section(Component):

    def __init__(self, designation, material=Material()):
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
        super(Section, self).__init__(material)

    def __repr__(self):
        repr = "Section\n"
        repr += "Designation: {}".format(self.designation)
        return repr

    def connect_to_database_update_other_attributes(self, table, designation):
        conn = sqlite3.connect(self.path_to_database)
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


class Beam(Section):

    def __init__(self, designation, material=Material()):
        super(Beam, self).__init__(designation, material)
        self.connect_to_database_update_other_attributes("Beams", designation)


class Column(Section):

    def __init__(self, designation, material=Material()):
        super(Column, self).__init__(designation, material)
        self.connect_to_database_update_other_attributes("Columns", designation)


class Weld(Component):

    def __init__(self, size=0.0, length=0.0, material=Material()):
        self.size = size
        self.length = length
        super(Weld, self).__init__(material)

    def __repr__(self):
        repr = "Weld\n"
        repr += "Size: {}\n".format(self.size)
        repr += "Length: {}".format(self.length)
        return repr


class Plate(Component):

    def __init__(self, thickness=0.0, height=0.0, width=0.0, material=Material()):
        self.thickness = thickness
        self.height = height
        self.width = width
        super(Plate, self).__init__(material)

    def __repr__(self):
        repr = "Plate\n"
        repr += "Thickness: {}".format(self.thickness)
        return repr


class Angle(Component):

    def __init__(self, designation, material=Material()):
        self.designation = designation

        self.leg_a_length = 0.0
        self.leg_b_length = 0.0
        self.thickness = 0.0

        self.connect_to_database_update_other_attributes(designation)

        self.length = 0.0
        super(Angle, self).__init__(material)

    def __repr__(self):
        repr = "Angle\n"
        repr += "Designation: {}".format(self.designation)
        return repr

    def connect_to_database_update_other_attributes(self, designation):
        conn = sqlite3.connect(self.path_to_database)
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
