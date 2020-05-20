from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column, Section
from Common import *
from utils.common.load import Load
from utils.common import common_calculation
from utils.common.is800_2007 import IS800_2007
import numpy as np

import logging


class MomentConnection(Connection, IS800_2007):
    def __init__(self):
        super(MomentConnection, self).__init__()

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
        d = VALUES_ENDPLATE_THICKNESS_CUSTOMIZED
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

    def tab_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "

        if not input_dictionary or input_dictionary[KEY_SECSIZE] == 'Select Section' or \
                input_dictionary[KEY_MATERIAL] == 'Select Material':
            designation = ''
            material_grade = ''
            source = ''
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

        else:
            designation = str(input_dictionary[KEY_SECSIZE])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            I_sec_attributes = Section(designation, material_grade)
            table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"
            Section.connect_to_database_update_other_attributes(I_sec_attributes, table, designation)
            source = str(I_sec_attributes.source)
            fu = str(I_sec_attributes.fu)
            fy = str(I_sec_attributes.fy)
            depth = str(I_sec_attributes.depth)
            flange_width = str(I_sec_attributes.flange_width)
            flange_thickness = str(I_sec_attributes.flange_thickness)
            web_thickness = str(I_sec_attributes.web_thickness)
            flange_slope = str(I_sec_attributes.flange_slope)
            root_radius = str(I_sec_attributes.root_radius)
            toe_radius = str(I_sec_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = str(I_sec_attributes.mass)
            area = str(I_sec_attributes.area)
            mom_inertia_z = str(I_sec_attributes.mom_inertia_z)
            mom_inertia_y = str(I_sec_attributes.mom_inertia_y)
            rad_of_gy_z = str(I_sec_attributes.rad_of_gy_z)
            rad_of_gy_y = str(I_sec_attributes.rad_of_gy_y)
            elast_sec_mod_z = str(I_sec_attributes.elast_sec_mod_z)
            elast_sec_mod_y = str(I_sec_attributes.elast_sec_mod_y)
            plast_sec_mod_z = str(I_sec_attributes.plast_sec_mod_z)
            plast_sec_mod_y = str(I_sec_attributes.plast_sec_mod_y)

        supporting_section = []
        t1 = ('Label_24', KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supporting_section.append(t34)

        t3 = ('Lable_26', KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        supporting_section.append(t3)

        t4 = ('Lable_27', KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        supporting_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        supporting_section.append(t5)

        t6 = ('Label_1', KEY_DISP_DEPTH, TYPE_TEXTBOX, None, depth)
        supporting_section.append(t6)

        t7 = ('Label_2', KEY_DISP_FLANGE_W, TYPE_TEXTBOX, None, flange_width)
        supporting_section.append(t7)

        t8 = ('Label_3', KEY_DISP_FLANGE_T, TYPE_TEXTBOX, None, flange_thickness)
        supporting_section.append(t8)

        t9 = ('Label_4', KEY_DISP_WEB_T, TYPE_TEXTBOX, None, web_thickness)
        supporting_section.append(t9)

        t10 = ('Label_5', KEY_DISP_FLANGE_S, TYPE_TEXTBOX, None, flange_slope)
        supporting_section.append(t10)

        t11 = ('Label_6', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
        supporting_section.append(t11)

        t12 = ('Label_7', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
        supporting_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t13)

        t14 = ('Label_8', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        supporting_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t18)

        t18 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t18)

        t15 = ('Label_9', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        supporting_section.append(t15)

        t16 = ('Label_10', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        supporting_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t17)

        t18 = ('Label_11', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        supporting_section.append(t18)

        t19 = ('Label_12', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        supporting_section.append(t19)

        t20 = ('Label_13', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        supporting_section.append(t20)

        t21 = ('Label_14', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        supporting_section.append(t21)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        supporting_section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        supporting_section.append(t23)

        t24 = ('Label_17', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
        supporting_section.append(t24)

        t25 = ('Label_18', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
        supporting_section.append(t25)

        t26 = ('Label_19', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        supporting_section.append(t26)

        t27 = ('Label_20', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        supporting_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t28)

        t29 = ('Label_21', 'Source', TYPE_TEXTBOX, None, source)
        supporting_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t30)

        t31 = ('Label_22', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        supporting_section.append(t31)

        t32 = ('Label_23', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        supporting_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None, None)
        supporting_section.append(t33)

        return supporting_section

    def get_bolt_details(self):
        pass


    def warn_text(self):
        pass
        # old_col_section = get_oldcolumncombolist()
        # old_beam_section = get_oldbeamcombolist()
        #
        # if my_d[KEY_SECSIZE] in old_beam_section or old_col_section:
        #     del_data = open('logging_text.log', 'w')
        #     del_data.truncate()
        #     del_data.close()
        #     logging.basicConfig(format='%(asctime)s %(message)s', filename='logging_text.log',level=logging.DEBUG)
        #     logging.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")
        #     with open('logging_text.log') as file:
        #         data = file.read()
        #         file.close()
        #     # file = open('logging_text.log', 'r')
        #     # # This will print every line one by one in the file
        #     # for each in file:
        #     #     print(each)
        #     key.setText(data)
        # else:
        #     key.setText("")


    def input_value_changed(self):
        pass

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
    def calculate_c(flange_width, depth, web_thickness, flange_thickness, min_area_req, anchor_hole_dia):
        """ calculate the 'projection' based on the Effective Area Method for rolled and welded columns only.

        Args:
            flange_width (float) - flange width of the column section (bf)
            depth (float) - depth of the column section (h)
            web_thickness (float) - web thickness of the column section (tw)
            flange_thickness (float) - flange thickness of the column section (tf)
            min_area_req (float) - minimum effective bearing area (A_bc)
            anchor_hole_dia (int) - diameter of the anchor hole

        Returns: projection in 'mm' (float)

        Note: 1) The following expression is used to calculate a, b and c [Ref: Design of Steel Structures,
                 N. Subramanian, 2nd. edition 2018, Example 15.2]:
                 A_bc = (bf + 2c) (h + 2c) - [{h - 2(tf + c)}(bf - tw)]

              2) Adding anchor hole diameter (half on each side) to the value of the projection to avoid punching
                 of the hole in the effective area which in turn shall avoid any stress concentration
        """
        a = 4
        b = (4 * flange_width) + (2 * depth) - (2 * web_thickness)
        c = (2 * flange_thickness * flange_width) + (depth * web_thickness) + (2 * flange_thickness * web_thickness) \
            - min_area_req

        roots = np.roots([a, b, c])  # finding roots of the equation
        r_1 = roots[0]
        r_2 = roots[1]
        r = max(r_1, r_2)  # picking the highest positive value from the roots
        r = r.real  # separating the imaginary part

        projection = common_calculation.round_up(r + anchor_hole_dia, 5)  # mm

        return projection

    @staticmethod
    def calc_weld_size_from_strength_per_unit_len(strength_unit_len, ultimate_stresses, elements_welded, fabrication=KEY_DP_WELD_FAB_SHOP):

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

