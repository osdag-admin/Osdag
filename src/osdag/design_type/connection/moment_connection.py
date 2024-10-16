from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column, ISection, RHS, SHS, CHS
from Common import *
from utils.common.load import Load
from utils.common.material import Material
from utils.common import common_calculation
from utils.common.is800_2007 import IS800_2007
import numpy as np

import logging


class MomentConnection(Connection, IS800_2007):
    def __init__(self):
        super(MomentConnection, self).__init__()

    ###################################
    # Design Preference Functions
    ###################################

    def tab_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "

        if not input_dictionary or input_dictionary[KEY_SECSIZE] == 'Select Section' or \
                input_dictionary[KEY_MATERIAL] == 'Select Material':
            designation = ''
            material_grade = ''
            source = 'Custom'
            fu = ''
            fy = ''
            depth = ''
            flange_width = ''
            flange_thickness = ''
            web_thickness = ''
            flange_slope = ''
            root_radius = ''
            toe_radius = ''
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = ''
            area = ''
            mom_inertia_z = ''
            mom_inertia_y = ''
            rad_of_gy_z = ''
            rad_of_gy_y = ''
            elast_sec_mod_z = ''
            elast_sec_mod_y = ''
            plast_sec_mod_z = ''
            plast_sec_mod_y = ''
            torsion_const = ''
            warping_const = ''
            image = VALUES_IMG_BEAM[0]
        else:
            designation = str(input_dictionary[KEY_SECSIZE])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            image = VALUES_IMG_BEAM[0]
            if designation in connectdb("RHS", call_type="popup"):
                RHS_sec_attributes = RHS(designation, material_grade)
                fu = str(RHS_sec_attributes.fu)
                fy = str(RHS_sec_attributes.fy)
                source = str(RHS_sec_attributes.source)
                depth = str(RHS_sec_attributes.depth)
                width = str(RHS_sec_attributes.flange_width)
                thickness = str(RHS_sec_attributes.flange_thickness)
                flange_slope = 0
                mass = str(RHS_sec_attributes.mass)
                area = str(round((RHS_sec_attributes.area / 10 ** 2), 2))
                mom_inertia_z = str(round((RHS_sec_attributes.mom_inertia_z / 10 ** 4), 2))
                mom_inertia_y = str(round((RHS_sec_attributes.mom_inertia_y / 10 ** 4), 2))
                rad_of_gy_z = str(round((RHS_sec_attributes.rad_of_gy_z / 10), 2))
                rad_of_gy_y = str(round((RHS_sec_attributes.rad_of_gy_y / 10), 2))
                elast_sec_mod_z = str(round((RHS_sec_attributes.elast_sec_mod_z / 10 ** 3), 2))
                elast_sec_mod_y = str(round((RHS_sec_attributes.elast_sec_mod_y / 10 ** 3), 2))
                plast_sec_mod_z = str(round((RHS_sec_attributes.plast_sec_mod_z / 10 ** 3), 2))
                plast_sec_mod_y = str(round((RHS_sec_attributes.plast_sec_mod_y / 10 ** 3), 2))
                image = VALUES_IMG_HOLLOWSECTION[1]
            elif designation in connectdb("SHS", call_type="popup"):
                SHS_sec_attributes = SHS(designation, material_grade)
                fu = str(SHS_sec_attributes.fu)
                fy = str(SHS_sec_attributes.fy)
                source = str(SHS_sec_attributes.source)
                depth = str(SHS_sec_attributes.depth)
                width = str(SHS_sec_attributes.flange_width)
                thickness = str(SHS_sec_attributes.flange_thickness)
                flange_slope = 0
                mass = str(SHS_sec_attributes.mass)
                area = str(round((SHS_sec_attributes.area / 10 ** 2), 2))
                mom_inertia_z = str(round((SHS_sec_attributes.mom_inertia_z / 10 ** 4), 2))
                mom_inertia_y = str(round((SHS_sec_attributes.mom_inertia_y / 10 ** 4), 2))
                rad_of_gy_z = str(round((SHS_sec_attributes.rad_of_gy_z / 10), 2))
                rad_of_gy_y = str(round((SHS_sec_attributes.rad_of_gy_y / 10), 2))
                elast_sec_mod_z = str(round((SHS_sec_attributes.elast_sec_mod_z / 10 ** 3), 2))
                elast_sec_mod_y = str(round((SHS_sec_attributes.elast_sec_mod_y / 10 ** 3), 2))
                plast_sec_mod_z = str(round((SHS_sec_attributes.plast_sec_mod_z / 10 ** 3), 2))
                plast_sec_mod_y = str(round((SHS_sec_attributes.plast_sec_mod_y / 10 ** 3), 2))
                image = VALUES_IMG_HOLLOWSECTION[0]
            elif designation in connectdb("CHS", call_type="popup"):
                CHS_sec_attributes = CHS(designation, material_grade)
                fu = str(CHS_sec_attributes.fu)
                fy = str(CHS_sec_attributes.fy)
                source = str(CHS_sec_attributes.source)
                nominal_bore = str(CHS_sec_attributes.nominal_bore)
                out_diameter = str(CHS_sec_attributes.out_diameter)
                thickness = str(CHS_sec_attributes.flange_thickness)
                flange_slope = 0
                mass = str(CHS_sec_attributes.mass)
                area = str(round((CHS_sec_attributes.area / 10 ** 2), 2))
                internal_vol = str(CHS_sec_attributes.internal_vol)
                mom_inertia = str(CHS_sec_attributes.mom_inertia)
                rad_of_gy = str(round((CHS_sec_attributes.rad_of_gy / 10), 2))
                elast_sec_mod = str(round((CHS_sec_attributes.elast_sec_mod / 10 ** 3), 2))
                image = VALUES_IMG_HOLLOWSECTION[2]
            else:
                I_sec_attributes = ISection(designation)
                table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"
                I_sec_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
                source = str(I_sec_attributes.source)
                fu = str(I_sec_attributes.fu)
                fy = str(I_sec_attributes.fy)
                depth = str(I_sec_attributes.depth)
                flange_width = str(I_sec_attributes.flange_width)
                flange_thickness = str(I_sec_attributes.flange_thickness)
                web_thickness = str(I_sec_attributes.web_thickness)
                flange_slope = float(I_sec_attributes.flange_slope)
                root_radius = str(I_sec_attributes.root_radius)
                toe_radius = str(I_sec_attributes.toe_radius)
                mass = str(I_sec_attributes.mass)
                area = str(round((I_sec_attributes.area / 10 ** 2), 2))
                mom_inertia_z = str(round((I_sec_attributes.mom_inertia_z / 10 ** 4), 2))
                mom_inertia_y = str(round((I_sec_attributes.mom_inertia_y / 10 ** 4), 2))
                rad_of_gy_z = str(round((I_sec_attributes.rad_of_gy_z / 10), 2))
                rad_of_gy_y = str(round((I_sec_attributes.rad_of_gy_y / 10), 2))
                elast_sec_mod_z = str(round((I_sec_attributes.elast_sec_mod_z / 10 ** 3), 2))
                elast_sec_mod_y = str(round((I_sec_attributes.elast_sec_mod_y / 10 ** 3), 2))
                plast_sec_mod_z = str(round((I_sec_attributes.plast_sec_mod_z / 10 ** 3), 2))
                plast_sec_mod_y = str(round((I_sec_attributes.plast_sec_mod_y / 10 ** 3), 2))
                torsion_const = str(round((I_sec_attributes.It / 10 ** 4), 2))
                warping_const = str(round((I_sec_attributes.Iw / 10 ** 6), 2))
                if flange_slope != 90:
                    image = VALUES_IMG_BEAM[0]
                else:
                    image = VALUES_IMG_BEAM[1]

        if KEY_SEC_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_SEC_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        section = []
        t1 = (KEY_SECSIZE, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        section.append(t34)

        t3 = (KEY_SEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        section.append(t3)

        t4 = (KEY_SEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        section.append(t4)

        t15 = ('Label_9', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_10', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        section.append(t16)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_23', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        section.append(t32)

        t14 = ('Label_8', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        section.append(t14)

        t29 = (KEY_SOURCE, KEY_DISP_SOURCE, TYPE_TEXTBOX, None, source)
        section.append(t29)

        t13 = (None, None, TYPE_BREAK, None, None)
        section.append(t13)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        section.append(t5)

        if designation in connectdb("RHS", call_type="popup") or designation in connectdb("SHS", call_type="popup"):

            t6 = ('Label_HS_1', KEY_DISP_DEPTH, TYPE_TEXTBOX, None, depth)
            section.append(t6)

            t7 = ('Label_HS_2', KEY_DISP_WIDTH, TYPE_TEXTBOX, None, width)
            section.append(t7)

            t8 = ('Label_HS_3', KEY_DISP_THICKNESS, TYPE_TEXTBOX, None, thickness)
            section.append(t8)

        elif designation in connectdb("CHS", call_type="popup"):

            t6 = ('Label_CHS_1', KEY_DISP_NB, TYPE_TEXTBOX, None, nominal_bore)
            section.append(t6)

            t7 = ('Label_CHS_2', KEY_DISP_OD, TYPE_TEXTBOX, None, out_diameter)
            section.append(t7)

            t8 = ('Label_CHS_3', KEY_DISP_THICKNESS, TYPE_TEXTBOX, None, thickness)
            section.append(t8)

        else:

            t6 = ('Label_1', KEY_DISP_DEPTH, TYPE_TEXTBOX, None, depth)
            section.append(t6)

            t7 = ('Label_2', KEY_DISP_FLANGE_W, TYPE_TEXTBOX, None, flange_width)
            section.append(t7)

            t8 = ('Label_3', KEY_DISP_FLANGE_T, TYPE_TEXTBOX, None, flange_thickness)
            section.append(t8)

            t9 = ('Label_4', KEY_DISP_WEB_T, TYPE_TEXTBOX, None, web_thickness)
            section.append(t9)

            t10 = ('Label_5', KEY_DISP_FLANGE_S, TYPE_TEXTBOX, None, flange_slope)
            section.append(t10)

            t11 = ('Label_6', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
            section.append(t11)

            t12 = ('Label_7', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
            section.append(t12)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        if designation in connectdb("RHS", call_type="popup") or designation in connectdb("SHS", call_type="popup"):

            t18 = ('Label_HS_11', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
            section.append(t18)

            t19 = ('Label_HS_12', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
            section.append(t19)

            t20 = ('Label_HS_13', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
            section.append(t20)

            t21 = ('Label_HS_14', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
            section.append(t21)

            t22 = ('Label_HS_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
            section.append(t22)

            t23 = ('Label_HS_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
            section.append(t23)

            t24 = ('Label_HS_17', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
            section.append(t24)

            t25 = ('Label_HS_18', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
            section.append(t25)

            t28 = (None, None, TYPE_BREAK, None, None)
            section.append(t28)

            t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, image)
            section.append(t33)

            t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
            section.append(t17)

            t26 = ('Label_HS_19', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
            section.append(t26)

            t27 = ('Label_HS_20', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
            section.append(t27)

        elif designation in connectdb("CHS", call_type="popup"):

            t18 = ('Label_CHS_11', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
            section.append(t18)

            t19 = ('Label_CHS_12', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
            section.append(t19)

            t20 = ('Label_CHS_13', KEY_DISP_IV, TYPE_TEXTBOX, None, internal_vol)
            section.append(t20)

            t21 = ('Label_HS_14', KEY_DISP_MOA, TYPE_TEXTBOX, None, mom_inertia)
            section.append(t21)

            t23 = ('Label_HS_15', KEY_DISP_ROG, TYPE_TEXTBOX, None, rad_of_gy)
            section.append(t23)

            t24 = ('Label_HS_16', KEY_DISP_SM, TYPE_TEXTBOX, None, elast_sec_mod)
            section.append(t24)

            t28 = (None, None, TYPE_BREAK, None, None)
            section.append(t28)

            t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, image)
            section.append(t33)

        else:

            t18 = ('Label_11', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
            section.append(t18)

            t19 = ('Label_12', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
            section.append(t19)

            t20 = ('Label_13', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
            section.append(t20)

            t21 = ('Label_14', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
            section.append(t21)

            t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
            section.append(t22)

            t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
            section.append(t23)

            t24 = ('Label_17', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
            section.append(t24)

            t25 = ('Label_18', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
            section.append(t25)

            t28 = (None, None, TYPE_BREAK, None, None)
            section.append(t28)

            t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, image)
            section.append(t33)

            t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
            section.append(t17)

            t26 = ('Label_19', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
            section.append(t26)

            t27 = ('Label_20', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
            section.append(t27)

            t26 = ('Label_21', KEY_DISP_It, TYPE_TEXTBOX, None, torsion_const)
            section.append(t26)

            t27 = ('Label_22', KEY_DISP_Iw, TYPE_TEXTBOX, None, warping_const)
            section.append(t27)

        return section

    def get_fu_fy_I_section(self):
        material_grade = self[0]
        designation = self[1][KEY_SECSIZE]

        fu = ''
        fy = ''

        if material_grade != "Select Material" and designation != "Select Section":

            if designation[1:4] == "CHS":
                table = "CHS" if designation in connectdb("CHS", "popup") else ""
                CHS_attributes = CHS(designation, material_grade)
                CHS_attributes.connect_to_database_update_other_attributes(designation, material_grade)
                fu = str(CHS_attributes.fu)
                fy = str(CHS_attributes.fy)

            elif designation[1:4] == "RHS":
                table = "RHS" if designation in connectdb("RHS", "popup") else ""
                RHS_attributes = RHS(designation, material_grade)
                RHS_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
                fu = str(RHS_attributes.fu)
                fy = str(RHS_attributes.fy)

            elif designation[1:4] == "SHS":
                table = "SHS" if designation in connectdb("SHS", "popup") else ""
                SHS_attributes = SHS(designation, material_grade)
                SHS_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
                fu = str(SHS_attributes.fu)
                fy = str(SHS_attributes.fy)

            else:
                table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"
                I_sec_attributes = ISection(designation)
                I_sec_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
                fu = str(I_sec_attributes.fu)
                fy = str(I_sec_attributes.fy)
        else:
            pass

        d = {KEY_SUPTNGSEC_FU: fu,
             KEY_SUPTNGSEC_FY: fy,
             KEY_SUPTDSEC_FU: fu,
             KEY_SUPTDSEC_FY: fy,
             KEY_SEC_FU: fu,
             KEY_SEC_FY: fy}

        return d

    ###########################################
    # Design Preferences Functions End
    ###########################################

    @staticmethod
    def pltthk_customized():
        a = VALUES_PLATETHK_CUSTOMIZED
        return a

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    @staticmethod
    def plate_thick_customized():
        f = VALUES_PLATETHICKNESS_CUSTOMIZED
        return f

    @staticmethod
    def endplate_thick_customized():
        d = PLATE_THICKNESS_SAIL
        return d

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        t4 = (KEY_WEBPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t4)
        t5 = (KEY_FLANGEPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t5)
        return list1

    def set_input_values(self, design_dictionary):
        self.mainmodule = "Moment Connection"
        self.load = Load(shear_force=design_dictionary[KEY_SHEAR], axial_force=design_dictionary.get(KEY_AXIAL, None),
                         moment=design_dictionary[KEY_MOMENT])




    def input_value_changed(self):

        lst = []

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        return lst

    def web_force(column_d, column_f_t, column_t_w, factored_axial_force, column_area):
        pass

    def block_shear_strength_plate(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        pass

    def block_shear_strength_section(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        pass

    def tension_member_design_due_to_yielding_of_gross_section(A_v, fy):
        pass

    def tension_member_design_due_to_rupture_of_critical_section(A_vn, fu):
        pass

    # Base Plate module
    @staticmethod
    def calculate_c(flange_width, depth, web_thickness, flange_thickness, min_area_req, anchor_hole_dia, section_type='I-section'):
        """ calculate the 'projection' based on the Effective Area Method for rolled and welded columns only.

        Args:
            flange_width (float) - flange width of the column section (bf)
            depth (float) - depth of the column section (h)
            web_thickness (float) - web thickness of the column section (tw)
            flange_thickness (float) - flange thickness of the column section (tf)
            min_area_req (float) - minimum effective bearing area (A_bc)
            anchor_hole_dia (int) - diameter of the anchor hole
            section_type (str) - type of section used as column ['I-section' or 'SHS' or 'RHS' or 'CHS']

        Returns: effective projection from the face of the column in 'mm' (float)

        Note: 1) The following expression is used to calculate a, b and c [Ref: Design of Steel Structures,
                 N. Subramanian, 2nd. edition 2018, Example 15.2]:

                    For I -section: A_bc = (bf + 2c) (h + 2c) - [{h - 2(tf + c)}(bf - tw)]
                    For Hollow SHS & RHS: A_bc = (D + 2c) (B + 2c)  [D = Depth, B = Width]
                    For Hollow CHS: A_bc = (3.14/4) * (OD + 2c)^2  [OD = outside diameter of the tube]

                    c is the effective projection from the outer face of the respective column section

              2) Adding anchor hole diameter (half on each side) to the value of the projection to avoid punching of the hole
                 (for anchor bolts) in the effective area which in turn shall avoid any stress concentration at holes
        """
        a = 4
        if section_type == 'I-section':
            b = (4 * flange_width) + (2 * depth) - (2 * web_thickness)
            c = (2 * flange_thickness * flange_width) + (depth * web_thickness) + (2 * flange_thickness * web_thickness) \
                - min_area_req

        if section_type == 'CHS':
            b = 4 * depth  # for CHS, depth = OD (outside diameter)
            c = depth ** 2 - ((4 * min_area_req) / math.pi)
        else:
            b = 2 * (depth + flange_width)  # for SHS & RHS, depth = D and flange_width = B
            c = (depth * flange_width) - min_area_req

        roots = np.roots([a, b, c])  # finding roots of the equation
        r_1 = roots[0]
        r_2 = roots[1]
        r = max(r_1, r_2)  # picking the highest positive value from the roots
        r = r.real  # separating the imaginary part (r in mm)

        if r < 0:
            return -r
        else:
            return r

    @staticmethod
    def calc_weld_size_from_strength_per_unit_len(strength_unit_len, ultimate_stresses, elements_welded, fabrication=KEY_DP_FAB_SHOP):

        """Calculate the size of fillet weld

        Args:
            strength_unit_len - Strength of weld per/unit length in MPa (float)
            ultimate_stresses - Ultimate stresses of weld and parent metal in MPa (list or tuple)
            elements_welded - List of thicknesses of the two elements being welded in mm (list or tuple)
            fabrication - Either 'shop' or 'field' (str)

        Returns:
            Size of the weld (float)

        Note:
            Reference:
            IS 800:2007,  cl 10.5.7.1.1

        """
        f_u = min(ultimate_stresses)
        gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][fabrication]
        weld_size = (strength_unit_len / (0.7 * f_u)) * math.sqrt(3) * gamma_mw

        weld_size_minimum = IS800_2007.cl_10_5_2_3_min_weld_size(elements_welded[0], elements_welded[1])

        # rounding up the weld size to a higher multiple of 2 with a minimum value of the weld size being
        # as per Table 21 of IS 800:2007
        weld_size = common_calculation.round_up(weld_size, 2, weld_size_minimum)  # mm

        return weld_size

