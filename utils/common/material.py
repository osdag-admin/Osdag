import sqlite3
from Common import *
import logging
from utils.common.is800_2007 import IS800_2007


class Material(object):

    def __init__(self, material_grade='', thickness=41):

        self.fy_20 = 0.0
        self.fy_20_40 = 0.0
        self.fy_40 = 0.0
        self.fu = 0.0
        self.fy = 0.0
        # if material_grade not in ["Select Material", "Custom"] and "Custom" not in material_grade:
        self.connect_to_database_to_get_fy_fu(grade=material_grade, thickness=thickness)
        self.material = material_grade
        # if material_grade.split(" ")[0] == "Custom":
        #     material = material_grade.split(" ")
        #     if len(material) == 3:
        #         self.material = material[0]
        #         self.fu = float(material[1])
        #         self.fy = float(material[2])

    def __repr__(self):
        repr = "Material:\n"
        repr += "fy_20: {}\n".format(self.fy_20)
        repr += "fy_20_40: {}\n".format(self.fy_20_40)
        repr += "fy_40: {}\n".format(self.fy_40)
        repr += "fu: {}\n".format(self.fu)
        return repr

    def connect_to_database_to_get_fy_fu(self, grade, thickness):
        conn = sqlite3.connect(PATH_TO_DATABASE)
        db_query = "SELECT * FROM Material WHERE Grade = ?"
        cur = conn.cursor()
        cur.execute(db_query, (grade,))
        row = cur.fetchone()
        if row:
            self.fy_20 = row[1]
            self.fy_20_40 = row[2]
            self.fy_40 = row[3]
            if thickness != '':
                if thickness < 20:
                    self.fy = self.fy_20
                elif 20 <= thickness <= 40:
                    self.fy = self.fy_20_40
                else:
                    self.fy = self.fy_40
            else:
                self.fy = min(self.fy_20, self.fy_20_40, self.fy_40)
            self.fu = row[4]
        conn.close()

    # def tension_member_yielding(self, A_g, F_y):
    #     "design strength of members under axial tension,T_dg,as governed by yielding of gross section"
    #     "A_g = gross area of cross-section"
    #     "gamma_m0 = partial safety factor for failure in tension by yielding"
    #     "F_y = yield stress of the material"
    #     gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
    #     T_dg = (A_g * F_y / gamma_m0) / 1000
    #     # logger.warning(
    #     #     " : You are using a section (in red color) that is not available in latest version of IS 808")
    #
    #     self.tension_yielding_capacity = round(T_dg, 2)
    #     # logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")
    #
    # def tension_rupture(self, A_n, F_u):
    #     "preliminary design strength,T_pdn,as governed by rupture at net section"
    #     "A_n = net area of the total cross-section"
    #     "F_u = Ultimate Strength of material"
    #
    #     gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
    #     T_pdn = 0.9 * A_n * F_u / gamma_m1 / 1000
    #
    #     self.tension_rupture_capacity = round(T_pdn, 2)
    #
    # def tension_blockshear_area_input(self,A_vg, A_vn, A_tg, A_tn, f_u, f_y):
    #     """Calculate the block shear strength of bolted connections as per cl. 6.4.1
    #
    #     Args:
    #         A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
    #         A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
    #         A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
    #                        end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
    #         A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
    #                        end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
    #         f_u: Ultimate stress of the plate material in MPa (float)
    #         f_y: Yield stress of the plate material in MPa (float)
    #
    #     Return:
    #         block shear strength of bolted connection in N (float)
    #
    #     Note:
    #         Reference:
    #         IS 800:2007, cl. 6.4.1
    #
    #     """
    #     gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
    #     gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
    #     T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
    #     T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
    #     Tdb = min(T_db1, T_db2)
    #     # Tdb = round(Tdb, 3)
    #     self.block_shear_capacity_axial = round(Tdb/1000,2)

    def set_osdaglogger(key):

        """
        Function to set Logger for Tension Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # handler.setLevel(logging.INFO)
        # formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        handler = OurLog(key)
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

