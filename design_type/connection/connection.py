from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from utils.common.load import Load
from utils.common.component import Section,I_sectional_Properties, Material
from main import Main
from Common import *


class Connection(Main):

    # def supporting_section_values(self):
    #
    #     supporting_section = []
    #     t1 = (KEY_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_DESIGNATION, TYPE_TEXTBOX, None)
    #     supporting_section.append(t1)
    #
    #     t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
    #     supporting_section.append(t2)
    #
    #     t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None)
    #     supporting_section.append(t3)
    #
    #     t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t4)
    #
    #     t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
    #     supporting_section.append(t5)
    #
    #     t6 = (KEY_SUPTNGSEC_DEPTH, KEY_DISP_SUPTNGSEC_DEPTH, TYPE_TEXTBOX, None)
    #     supporting_section.append(t6)
    #
    #     t7 = (KEY_SUPTNGSEC_FLANGE_W, KEY_DISP_SUPTNGSEC_FLANGE_W, TYPE_TEXTBOX, None)
    #     supporting_section.append(t7)
    #
    #     t8 = (KEY_SUPTNGSEC_FLANGE_T, KEY_DISP_SUPTNGSEC_FLANGE_T, TYPE_TEXTBOX, None)
    #     supporting_section.append(t8)
    #
    #     t9 = (KEY_SUPTNGSEC_WEB_T, KEY_DISP_SUPTNGSEC_WEB_T, TYPE_TEXTBOX, None)
    #     supporting_section.append(t9)
    #
    #     t10 = (KEY_SUPTNGSEC_FLANGE_S, KEY_DISP_SUPTNGSEC_FLANGE_S, TYPE_TEXTBOX, None)
    #     supporting_section.append(t10)
    #
    #     t11 = (KEY_SUPTNGSEC_ROOT_R, KEY_DISP_SUPTNGSEC_ROOT_R, TYPE_TEXTBOX, None)
    #     supporting_section.append(t11)
    #
    #     t12 = (KEY_SUPTNGSEC_TOE_R, KEY_DISP_SUPTNGSEC_TOE_R, TYPE_TEXTBOX, None)
    #     supporting_section.append(t12)
    #
    #     t13 = (None, None, TYPE_BREAK, None)
    #     supporting_section.append(t13)
    #
    #     t14 = (KEY_SUPTNGSEC_TYPE, KEY_DISP_SUPTNGSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
    #     supporting_section.append(t14)
    #
    #     t18 = (None, None, TYPE_ENTER, None)
    #     supporting_section.append(t18)
    #
    #     t15 = (KEY_SUPTNGSEC_MOD_OF_ELAST, KEY_SUPTNGSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
    #     supporting_section.append(t15)
    #
    #     t16 = (KEY_SUPTNGSEC_MOD_OF_RIGID, KEY_SUPTNGSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
    #     supporting_section.append(t16)
    #
    #     t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
    #     supporting_section.append(t17)
    #
    #     t18 = (KEY_SUPTNGSEC_MASS, KEY_DISP_SUPTNGSEC_MASS, TYPE_TEXTBOX, None)
    #     supporting_section.append(t18)
    #
    #     t19 = (KEY_SUPTNGSEC_SEC_AREA, KEY_DISP_SUPTNGSEC_SEC_AREA, TYPE_TEXTBOX, None)
    #     supporting_section.append(t19)
    #
    #     t20 = (KEY_SUPTNGSEC_MOA_LZ, KEY_DISP_SUPTNGSEC_MOA_LZ, TYPE_TEXTBOX, None)
    #     supporting_section.append(t20)
    #
    #     t21 = (KEY_SUPTNGSEC_MOA_LY, KEY_DISP_SUPTNGSEC_MOA_LY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t21)
    #
    #     t22 = (KEY_SUPTNGSEC_ROG_RZ, KEY_DISP_SUPTNGSEC_ROG_RZ, TYPE_TEXTBOX, None)
    #     supporting_section.append(t22)
    #
    #     t23 = (KEY_SUPTNGSEC_ROG_RY, KEY_DISP_SUPTNGSEC_ROG_RY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t23)
    #
    #     t24 = (KEY_SUPTNGSEC_EM_ZZ, KEY_DISP_SUPTNGSEC_EM_ZZ, TYPE_TEXTBOX, None)
    #     supporting_section.append(t24)
    #
    #     t25 = (KEY_SUPTNGSEC_EM_ZY, KEY_DISP_SUPTNGSEC_EM_ZY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t25)
    #
    #     t26 = (KEY_SUPTNGSEC_PM_ZPZ, KEY_DISP_SUPTNGSEC_PM_ZPZ, TYPE_TEXTBOX, None)
    #     supporting_section.append(t26)
    #
    #     t27 = (KEY_SUPTNGSEC_PM_ZPY, KEY_DISP_SUPTNGSEC_PM_ZPY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t27)
    #
    #     t28 = (None, None, TYPE_BREAK, None)
    #     supporting_section.append(t28)
    #
    #     t29 = (KEY_SUPTNGSEC_SOURCE, KEY_DISP_SUPTNGSEC_SOURCE, TYPE_TEXTBOX, None)
    #     supporting_section.append(t29)
    #
    #     t30 = (None, None, TYPE_ENTER, None)
    #     supporting_section.append(t30)
    #
    #     t31 = (KEY_SUPTNGSEC_POISSON_RATIO, KEY_DISP_SUPTNGSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
    #     supporting_section.append(t31)
    #
    #     t32 = (KEY_SUPTNGSEC_THERMAL_EXP, KEY_DISP_SUPTNGSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
    #     supporting_section.append(t32)
    #
    #     t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
    #     supporting_section.append(t33)
    #
    #     return supporting_section
    #
    # def supported_section_values(self):
    #
    #     supported_section = []
    #
    #     t1 = (KEY_SUPTDSEC_DESIGNATION, KEY_DISP_SUPTDSEC_DESIGNATION, TYPE_TEXTBOX, None)
    #     supported_section.append(t1)
    #
    #     t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
    #     supported_section.append(t2)
    #
    #     t3 = (KEY_SUPTDSEC_FU, KEY_DISP_SUPTDSEC_FU, TYPE_TEXTBOX, None)
    #     supported_section.append(t3)
    #
    #     t4 = (KEY_SUPTDSEC_FY, KEY_DISP_SUPTDSEC_FY, TYPE_TEXTBOX, None)
    #     supported_section.append(t4)
    #
    #     t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
    #     supported_section.append(t5)
    #
    #     t6 = (KEY_SUPTDSEC_DEPTH, KEY_DISP_SUPTDSEC_DEPTH, TYPE_TEXTBOX, None)
    #     supported_section.append(t6)
    #
    #     t7 = (KEY_SUPTDSEC_FLANGE_W, KEY_DISP_SUPTDSEC_FLANGE_W, TYPE_TEXTBOX, None)
    #     supported_section.append(t7)
    #
    #     t8 = (KEY_SUPTDSEC_FLANGE_T, KEY_DISP_SUPTDSEC_FLANGE_T, TYPE_TEXTBOX, None)
    #     supported_section.append(t8)
    #
    #     t9 = (KEY_SUPTDSEC_WEB_T, KEY_DISP_SUPTDSEC_WEB_T, TYPE_TEXTBOX, None)
    #     supported_section.append(t9)
    #
    #     t10 = (KEY_SUPTDSEC_FLANGE_S, KEY_DISP_SUPTDSEC_FLANGE_S, TYPE_TEXTBOX, None)
    #     supported_section.append(t10)
    #
    #     t11 = (KEY_SUPTDSEC_ROOT_R, KEY_DISP_SUPTDSEC_ROOT_R, TYPE_TEXTBOX, None)
    #     supported_section.append(t11)
    #
    #     t12 = (KEY_SUPTDSEC_TOE_R, KEY_DISP_SUPTDSEC_TOE_R, TYPE_TEXTBOX, None)
    #     supported_section.append(t12)
    #
    #     t13 = (None, None, TYPE_BREAK, None)
    #     supported_section.append(t13)
    #
    #     t14 = (KEY_SUPTDSEC_TYPE, KEY_DISP_SUPTDSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
    #     supported_section.append(t14)
    #
    #     t18 = (None, None, TYPE_ENTER, None)
    #     supported_section.append(t18)
    #
    #     t15 = (KEY_SUPTDSEC_MOD_OF_ELAST, KEY_SUPTDSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
    #     supported_section.append(t15)
    #
    #     t16 = (KEY_SUPTDSEC_MOD_OF_RIGID, KEY_SUPTDSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
    #     supported_section.append(t16)
    #
    #     t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
    #     supported_section.append(t17)
    #
    #     t18 = (KEY_SUPTDSEC_MASS, KEY_DISP_SUPTDSEC_MASS, TYPE_TEXTBOX, None)
    #     supported_section.append(t18)
    #
    #     t19 = (KEY_SUPTDSEC_SEC_AREA, KEY_DISP_SUPTDSEC_SEC_AREA, TYPE_TEXTBOX, None)
    #     supported_section.append(t19)
    #
    #     t20 = (KEY_SUPTDSEC_MOA_LZ, KEY_DISP_SUPTDSEC_MOA_LZ, TYPE_TEXTBOX, None)
    #     supported_section.append(t20)
    #
    #     t21 = (KEY_SUPTDSEC_MOA_LY, KEY_DISP_SUPTDSEC_MOA_LY, TYPE_TEXTBOX, None)
    #     supported_section.append(t21)
    #
    #     t22 = (KEY_SUPTDSEC_ROG_RZ, KEY_DISP_SUPTDSEC_ROG_RZ, TYPE_TEXTBOX, None)
    #     supported_section.append(t22)
    #
    #     t23 = (KEY_SUPTDSEC_ROG_RY, KEY_DISP_SUPTDSEC_ROG_RY, TYPE_TEXTBOX, None)
    #     supported_section.append(t23)
    #
    #     t24 = (KEY_SUPTDSEC_EM_ZZ, KEY_DISP_SUPTDSEC_EM_ZZ, TYPE_TEXTBOX, None)
    #     supported_section.append(t24)
    #
    #     t25 = (KEY_SUPTDSEC_EM_ZY, KEY_DISP_SUPTDSEC_EM_ZY, TYPE_TEXTBOX, None)
    #     supported_section.append(t25)
    #
    #     t26 = (KEY_SUPTDSEC_PM_ZPZ, KEY_DISP_SUPTDSEC_PM_ZPZ, TYPE_TEXTBOX, None)
    #     supported_section.append(t26)
    #
    #     t27 = (KEY_SUPTDSEC_PM_ZPY, KEY_DISP_SUPTDSEC_PM_ZPY, TYPE_TEXTBOX, None)
    #     supported_section.append(t27)
    #
    #     t28 = (None, None, TYPE_BREAK, None)
    #     supported_section.append(t28)
    #
    #     t29 = (KEY_SUPTDSEC_SOURCE, KEY_DISP_SUPTDSEC_SOURCE, TYPE_TEXTBOX, None)
    #     supported_section.append(t29)
    #
    #     t30 = (None, None, TYPE_ENTER, None)
    #     supported_section.append(t30)
    #
    #     t31 = (KEY_SUPTDSEC_POISSON_RATIO, KEY_DISP_SUPTDSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
    #     supported_section.append(t31)
    #
    #     t32 = (KEY_SUPTDSEC_THERMAL_EXP, KEY_DISP_SUPTDSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
    #     supported_section.append(t32)
    #
    #     t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
    #     supported_section.append(t33)
    #
    #     return supported_section

        ###################
    def tab_column_section(self, input_dictionary):
        if not input_dictionary or 'Select Section' in [input_dictionary[KEY_SUPTNGSEC] if
            KEY_SUPTNGSEC in input_dictionary.keys() else input_dictionary[KEY_SECSIZE], input_dictionary[KEY_MATERIAL]]:
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
            if KEY_SUPTNGSEC in input_dictionary.keys():
                designation = str(input_dictionary[KEY_SUPTNGSEC])
            else:
                designation = str(input_dictionary[KEY_SECSIZE])

            material_grade = str(input_dictionary[KEY_MATERIAL])
            col_attributes = Section(designation, material_grade)
            Section.connect_to_database_update_other_attributes(
                col_attributes, "Beams" if designation in connectdb("Beams", "popup") else "Columns", designation)
            source = str(col_attributes.source)
            fu = str(col_attributes.fu)
            fy = str(col_attributes.fy)
            depth = str(col_attributes.depth)
            flange_width = str(col_attributes.flange_width)
            flange_thickness = str(col_attributes.flange_thickness)
            web_thickness = str(col_attributes.web_thickness)
            flange_slope = str(col_attributes.flange_slope)
            root_radius = str(col_attributes.root_radius)
            toe_radius = str(col_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = str(col_attributes.mass)
            area = str(col_attributes.area)
            mom_inertia_z = str(col_attributes.mom_inertia_z)
            mom_inertia_y = str(col_attributes.mom_inertia_y)
            rad_of_gy_z = str(col_attributes.rad_of_gy_z)
            rad_of_gy_y = str(col_attributes.rad_of_gy_y)
            elast_sec_mod_z = str(col_attributes.elast_sec_mod_z)
            elast_sec_mod_y = str(col_attributes.elast_sec_mod_y)
            plast_sec_mod_z = str(col_attributes.plast_sec_mod_z)
            plast_sec_mod_y = str(col_attributes.plast_sec_mod_y)

        supporting_section = []
        t1 = (KEY_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_DESIGNATION, TYPE_TEXTBOX, None, designation)
        supporting_section.append(t1)

        t2 = (None, 'Mechanical Properties', TYPE_TITLE, None, None)
        supporting_section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SUPTNGSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supporting_section.append(t34)

        t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None, fu)
        supporting_section.append(t3)

        t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None, fy)
        supporting_section.append(t4)

        t5 = (None, 'Dimensions', TYPE_TITLE, None, None)
        supporting_section.append(t5)

        t6 = ('Label_1', 'Depth, D (mm)*', TYPE_TEXTBOX, None, depth)
        supporting_section.append(t6)

        t7 = ('Label_2', 'Flange width, B (mm)*', TYPE_TEXTBOX, None, flange_width)
        supporting_section.append(t7)

        t8 = ('Label_3', 'Flange thickness, T (mm)*', TYPE_TEXTBOX, None, flange_thickness)
        supporting_section.append(t8)

        t9 = ('Label_4', 'Web thickness, t (mm)*', TYPE_TEXTBOX, None, web_thickness)
        supporting_section.append(t9)

        t10 = ('Label_5', 'Flange Slope, a (deg.)*', TYPE_TEXTBOX, None, flange_slope)
        supporting_section.append(t10)

        t11 = ('Label_6', 'Root radius, R1 (mm)*', TYPE_TEXTBOX, None, root_radius)
        supporting_section.append(t11)

        t12 = ('Label_7', 'Toe radius, R2 (mm)*', TYPE_TEXTBOX, None, toe_radius)
        supporting_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t13)

        t14 = ('Label_8', 'Type', TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        supporting_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t18)

        t18 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t18)

        t15 = ('Label_9', 'Modulus of elasticity, E (GPa)', TYPE_TEXTBOX, None, m_o_e)
        supporting_section.append(t15)

        t16 = ('Label_10', 'Modulus of rifidity, G (GPa)', TYPE_TEXTBOX, None, m_o_r)
        supporting_section.append(t16)

        t17 = (None, 'Sectional Properties', TYPE_TITLE, None, None)
        supporting_section.append(t17)

        t18 = ('Label_11', 'Mass, M (Kg/m)', TYPE_TEXTBOX, None, mass)
        supporting_section.append(t18)

        t19 = ('Label_12', 'Sectional area, a (mm<sup>2</sup>)', TYPE_TEXTBOX, None, area)
        supporting_section.append(t19)

        t20 = ('Label_13', '2nd Moment of area, l<sub>z</sub> (cm<sup>4</sup>)', TYPE_TEXTBOX, None, mom_inertia_z)
        supporting_section.append(t20)

        t21 = ('Label_14', '2nd Moment of area, l<sub>y</sub> (cm<sup>4</sup>)', TYPE_TEXTBOX, None, mom_inertia_y)
        supporting_section.append(t21)

        t22 = ('Label_15', 'Radius of gyration, r<sub>z</sub> (cm)', TYPE_TEXTBOX, None, rad_of_gy_z)
        supporting_section.append(t22)

        t23 = ('Label_16', 'Radius of gyration, r<sub>y</sub> (cm)', TYPE_TEXTBOX, None, rad_of_gy_y)
        supporting_section.append(t23)

        t24 = ('Label_17', 'Elastic modulus, Z<sub>z</sub> (cm<sup>3</sup>)', TYPE_TEXTBOX, None, elast_sec_mod_z)
        supporting_section.append(t24)

        t25 = ('Label_18', 'Elastic modulus, Z<sub>y</sub> (cm<sup>3</sup>)', TYPE_TEXTBOX, None, elast_sec_mod_y)
        supporting_section.append(t25)

        t26 = ('Label_19', 'Plastic modulus, Z<sub>pz</sub> (cm<sup>3</sup>)', TYPE_TEXTBOX, None, plast_sec_mod_z)
        supporting_section.append(t26)

        t27 = ('Label_20', 'Plastic modulus, Z<sub>py</sub> (cm<sup>3</sup>)', TYPE_TEXTBOX, None, plast_sec_mod_y)
        supporting_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t28)

        t29 = ('Label_21', 'Source', TYPE_TEXTBOX, None, source)
        supporting_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t30)

        t31 = ('Label_22', 'Poissons ratio, v', TYPE_TEXTBOX, None, p_r)
        supporting_section.append(t31)

        t32 = ('Label_23', 'Thermal expansion coeff.a <br>(x10<sup>-6</sup>/ <sup>0</sup>C)', TYPE_TEXTBOX, None, t_e)
        supporting_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None, None)
        supporting_section.append(t33)

        return supporting_section

    def tab_beam_section(self, input_dictionary):

        if not input_dictionary or 'Select Section' in [input_dictionary[KEY_SUPTDSEC] if
            KEY_SUPTDSEC in input_dictionary.keys() else input_dictionary[KEY_SECSIZE], input_dictionary[KEY_MATERIAL]]:
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
            if KEY_SUPTDSEC in input_dictionary.keys():
                designation = str(input_dictionary[KEY_SUPTDSEC])
            else:
                designation = str(input_dictionary[KEY_SECSIZE])

            material_grade = str(input_dictionary[KEY_MATERIAL])
            col_attributes = Section(designation, material_grade)
            Section.connect_to_database_update_other_attributes(col_attributes, "Beams", designation)
            source = str(col_attributes.source)
            fu = str(col_attributes.fu)
            fy = str(col_attributes.fy)
            depth = str(col_attributes.depth)
            flange_width = str(col_attributes.flange_width)
            flange_thickness = str(col_attributes.flange_thickness)
            web_thickness = str(col_attributes.web_thickness)
            flange_slope = str(col_attributes.flange_slope)
            root_radius = str(col_attributes.root_radius)
            toe_radius = str(col_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = str(col_attributes.mass)
            area = str(col_attributes.area)
            mom_inertia_z = str(col_attributes.mom_inertia_z)
            mom_inertia_y = str(col_attributes.mom_inertia_y)
            rad_of_gy_z = str(col_attributes.rad_of_gy_z)
            rad_of_gy_y = str(col_attributes.rad_of_gy_y)
            elast_sec_mod_z = str(col_attributes.elast_sec_mod_z)
            elast_sec_mod_y = str(col_attributes.elast_sec_mod_y)
            plast_sec_mod_z = str(col_attributes.plast_sec_mod_z)
            plast_sec_mod_y = str(col_attributes.plast_sec_mod_y)

        supported_section = []

        t1 = (KEY_SUPTDSEC_DESIGNATION, KEY_DISP_SUPTDSEC_DESIGNATION, TYPE_TEXTBOX, None, designation)
        supported_section.append(t1)

        t2 = (None, 'Mechanical Properties', TYPE_TITLE, None, None)
        supported_section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SUPTDSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supported_section.append(t34)

        t3 = (KEY_SUPTDSEC_FU, KEY_DISP_SUPTDSEC_FU, TYPE_TEXTBOX, None, fu)
        supported_section.append(t3)

        t4 = (KEY_SUPTDSEC_FY, KEY_DISP_SUPTDSEC_FY, TYPE_TEXTBOX, None, fy)
        supported_section.append(t4)

        t5 = (None, 'Dimensions', TYPE_TITLE, None, None)
        supported_section.append(t5)

        t6 = ('Label_1', 'Depth, D (mm)*', TYPE_TEXTBOX, None, depth)
        supported_section.append(t6)

        t7 = ('Label_2', 'Flange width, B (mm)*', TYPE_TEXTBOX, None, flange_width)
        supported_section.append(t7)

        t8 = ('Label_3', 'Flange thickness, T (mm)*', TYPE_TEXTBOX, None, flange_thickness)
        supported_section.append(t8)

        t9 = ('Label_4', 'Web thickness, t (mm)*', TYPE_TEXTBOX, None, web_thickness)
        supported_section.append(t9)

        t10 = ('Label_5', 'Flange Slope, a (deg.)*', TYPE_TEXTBOX, None, flange_slope)
        supported_section.append(t10)

        t11 = ('Label_6', 'Root radius, R1 (mm)*', TYPE_TEXTBOX, None, root_radius)
        supported_section.append(t11)

        t12 = ('Label_7', 'Toe radius, R2 (mm)*', TYPE_TEXTBOX, None, toe_radius)
        supported_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None, None)
        supported_section.append(t13)

        t14 = ('Label_8', 'Type', TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        supported_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None, None)
        supported_section.append(t18)

        t18 = (None, None, TYPE_ENTER, None, None)
        supported_section.append(t18)

        t15 = ('Label_9', 'Modulus of elasticity, E (GPa)', TYPE_TEXTBOX, None, m_o_e)
        supported_section.append(t15)

        t16 = ('Label_10', 'Modulus of rifidity, G (GPa)', TYPE_TEXTBOX, None, m_o_r)
        supported_section.append(t16)

        t17 = (None, 'Sectional Properties', TYPE_TITLE, None, None)
        supported_section.append(t17)

        t18 = ('Label_11', 'Mass, M (Kg/m)', TYPE_TEXTBOX, None, mass)
        supported_section.append(t18)

        t19 = ('Label_12', 'Sectional area, a (mm<sup>2</sup>)', TYPE_TEXTBOX, None, area)
        supported_section.append(t19)

        t20 = ('Label_13', '2nd Moment of area, l<sub>z</sub> (cm<sup>4</sup>)', TYPE_TEXTBOX, None, mom_inertia_z)
        supported_section.append(t20)

        t21 = ('Label_14', '2nd Moment of area, l<sub>y</sub> (cm<sup>4</sup>)', TYPE_TEXTBOX, None, mom_inertia_y)
        supported_section.append(t21)

        t22 = ('Label_15', 'Radius of gyration, r<sub>z</sub> (cm)', TYPE_TEXTBOX, None, rad_of_gy_z)
        supported_section.append(t22)

        t23 = ('Label_16', 'Radius of gyration, r<sub>y</sub> (cm)', TYPE_TEXTBOX, None, rad_of_gy_y)
        supported_section.append(t23)

        t24 = ('Label_17', 'Elastic modulus, Z<sub>z</sub> (cm<sup>3</sup>)', TYPE_TEXTBOX, None, elast_sec_mod_z)
        supported_section.append(t24)

        t25 = ('Label_18', 'Elastic modulus, Z<sub>y</sub> (cm<sup>3</sup>)', TYPE_TEXTBOX, None, elast_sec_mod_y)
        supported_section.append(t25)

        t26 = ('Label_19', 'Plastic modulus, Z<sub>pz</sub> (cm<sup>3</sup>)', TYPE_TEXTBOX, None, plast_sec_mod_z)
        supported_section.append(t26)

        t27 = ('Label_20', 'Plastic modulus, Z<sub>py</sub> (cm<sup>3</sup>)', TYPE_TEXTBOX, None, plast_sec_mod_y)
        supported_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None, None)
        supported_section.append(t28)

        t29 = ('Label_21', 'Source', TYPE_TEXTBOX, None, source)
        supported_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        supported_section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        supported_section.append(t30)

        t31 = ('Label_22', 'Poissons ratio, v', TYPE_TEXTBOX, None, p_r)
        supported_section.append(t31)

        t32 = ('Label_23', 'Thermal expansion coeff.a <br>(x10<sup>-6</sup>/ <sup>0</sup>C)', TYPE_TEXTBOX, None, t_e)
        supported_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None, None)
        supported_section.append(t33)

        return supported_section

    def bolt_values(self, input_dictionary):

        if not input_dictionary or 'Select Section' in [input_dictionary[KEY_MATERIAL]]:
            material_g_o = ''
        else:
            material_g_o = Material(input_dictionary[KEY_MATERIAL]).fu

        bolt = []

        t1 = (KEY_DP_BOLT_TYPE, KEY_DISP_TYP, TYPE_COMBOBOX, ['Pretensioned', 'Non-pretensioned'], 'Pretensioned')
        bolt.append(t1)

        t2 = (KEY_DP_BOLT_HOLE_TYPE, KEY_DISP_DP_BOLT_HOLE_TYPE, TYPE_COMBOBOX, ['Standard', 'Over-sized'], 'Standard')
        bolt.append(t2)

        t3 = (KEY_DP_BOLT_MATERIAL_G_O, KEY_DISP_DP_BOLT_MATERIAL_G_O, TYPE_TEXTBOX, None, material_g_o)
        bolt.append(t3)

        t4 = (None, None, TYPE_ENTER, None, None)
        bolt.append(t4)

        t5 = (None, KEY_DISP_DP_BOLT_DESIGN_PARA, TYPE_TITLE, None, None)
        bolt.append(t5)

        t6 = (KEY_DP_BOLT_SLIP_FACTOR, KEY_DISP_DP_BOLT_SLIP_FACTOR, TYPE_COMBOBOX,
              ['0.2', '0.5', '0.1', '0.25', '0.3', '0.33', '0.48', '0.52', '0.55'], '0.3')
        bolt.append(t6)

        t7 = (None, None, TYPE_ENTER, None, None)
        bolt.append(t7)

        t8 = (None, "NOTE : If slip is permitted under the design load, design the bolt as"
                    "<br>a bearing bolt and select corresponding bolt grade.", TYPE_NOTE, None, None)
        bolt.append(t8)

        t9 = ("textBrowser", "", TYPE_TEXT_BROWSER, BOLT_DESCRIPTION, None)
        bolt.append(t9)

        return bolt

    def weld_values(self, input_dictionary):

        if not input_dictionary or 'Select Section' in [input_dictionary[KEY_MATERIAL]]:
            material_g_o = ''
        else:
            material_g_o = Material(input_dictionary[KEY_MATERIAL]).fu

        weld = []

        t1 = (KEY_DP_WELD_FAB, KEY_DISP_DP_WELD_FAB, TYPE_COMBOBOX, KEY_DP_WELD_FAB_VALUES, KEY_DP_WELD_FAB_SHOP)
        weld.append(t1)

        t2 = (KEY_DP_WELD_MATERIAL_G_O, KEY_DISP_DP_WELD_MATERIAL_G_O, TYPE_TEXTBOX, None, material_g_o)
        weld.append(t2)

        t3 = ("textBrowser", "", TYPE_TEXT_BROWSER, WELD_DESCRIPTION, None)
        weld.append(t3)

        return weld

    def detailing_values(self, input_dictionary):

        detailing = []

        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX,
              ['a - Sheared or hand flame cut', 'b - Rolled, machine-flame cut, sawn and planed'],
              'a - Sheared or hand flame cut')
        detailing.append(t1)

        t2 = (KEY_DP_DETAILING_GAP, KEY_DISP_DP_DETAILING_GAP, TYPE_TEXTBOX, None, '10')
        detailing.append(t2)

        t3 = (KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES, TYPE_COMBOBOX,
              ['No', 'Yes'], 'No')
        detailing.append(t3)

        t4 = ("textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION, None)
        detailing.append(t4)

        return detailing

    def design_values(self, input_dictionary):

        design = []

        t1 = (KEY_DP_DESIGN_METHOD, KEY_DISP_DP_DESIGN_METHOD, TYPE_COMBOBOX,
              ['Limit State Design', 'Limit State (Capacity based) Design', 'Working Stress Design'],
              'Limit State Design')
        design.append(t1)

        return design

    def connector_values(self, input_dictionary):

        if not input_dictionary or 'Select Section' in [input_dictionary[KEY_MATERIAL]]:
            material_grade = 'Custom'
            fu = ''
            fy = ''
        else:
            material_grade = input_dictionary[KEY_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        connector = []

        material = connectdb("Material", call_type="popup")
        t1 = (KEY_PLATE_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        connector.append(t1)

        t2 = (KEY_PLATE_FU, KEY_DISP_PLATE_FU, TYPE_TEXTBOX, None, fu)
        connector.append(t2)

        t3 = (KEY_PLATE_FY, KEY_DISP_PLATE_FY, TYPE_TEXTBOX, None, fy)
        connector.append(t3)

        return connector


    def tab_value_changed(self):

        change_tab = []

        t1 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC_MATERIAL], [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t1)

        t2 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC_MATERIAL], [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_PLATE_MATERIAL], [KEY_PLATE_FU, KEY_PLATE_FY], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t3)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20'], TYPE_TEXTBOX, self.get_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20'], TYPE_TEXTBOX, self.get_sec_properties)
        change_tab.append(t5)

        return change_tab

    def get_sec_properties(self):

        if '' in self:
            mass = ''
            area = ''
            moa_z = ''
            moa_y = ''
            rog_z = ''
            rog_y = ''
            em_z = ''
            em_y = ''
            pm_z = ''
            pm_y = ''

        else:
            D = float(self[0])
            B = float(self[1])
            t_w = float(self[2])
            t_f = float(self[3])

            sec_prop = I_sectional_Properties()
            mass = sec_prop.calc_Mass(D, B, t_w, t_f)
            area = sec_prop.calc_Area(D, B, t_w, t_f)
            moa_z = sec_prop.calc_MomentOfAreaZ(D, B, t_w, t_f)
            moa_y = sec_prop.calc_MomentOfAreaY(D, B, t_w, t_f)
            rog_z = sec_prop.calc_RogZ(D, B, t_w, t_f)
            rog_y = sec_prop.calc_RogY(D, B, t_w, t_f)
            em_z = sec_prop.calc_ElasticModulusZz(D, B, t_w, t_f)
            em_y = sec_prop.calc_ElasticModulusZy(D, B, t_w, t_f)
            pm_z = sec_prop.calc_PlasticModulusZpz(D, B, t_w, t_f)
            pm_y = sec_prop.calc_PlasticModulusZpy(D, B, t_w, t_f)

        d = {'Label_11': str(mass),
             'Label_12': str(area),
             'Label_13': str(moa_z),
             'Label_14': str(moa_y),
             'Label_15': str(rog_z),
             'Label_16': str(rog_y),
             'Label_17': str(em_z),
             'Label_18': str(em_y),
             'Label_19': str(pm_z),
             'Label_20': str(pm_y),
            }

        return d

    def get_fu_fy(self):
        m = Material(self[0])
        fu = m.fu
        fy = m.fy
        d = {KEY_SUPTNGSEC_FU: fu,
             KEY_SUPTNGSEC_FY: fy,
             KEY_SUPTDSEC_FU: fu,
             KEY_SUPTDSEC_FY: fy,
             KEY_PLATE_FU: fu,
             KEY_PLATE_FY: fy,
             KEY_BASE_PLATE_FU: fu,
             KEY_BASE_PLATE_FY: fy}

        return d

    def edit_tabs(self):

        edit_list = []

        t1 = (KEY_DISP_COLSEC, KEY_CONN, TYPE_CHANGE_TAB_NAME, self.get_column_tab_name)
        edit_list.append(t1)

        t1 = (KEY_DISP_BEAMSEC, KEY_CONN, TYPE_CHANGE_TAB_NAME, self.get_beam_tab_name)
        edit_list.append(t1)

        return edit_list

    def get_column_tab_name(self):
        if self in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        else:
            return KEY_DISP_PRIBM

    def get_beam_tab_name(self):
        if self in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        else:
            return KEY_DISP_SECBM

    def list_for_fu_fy_validation(self):

        fu_fy_list = []

        t1 = (KEY_SUPTNGSEC_MATERIAL, KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY)
        fu_fy_list.append(t1)

        t2 = (KEY_SUPTDSEC_MATERIAL, KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY)
        fu_fy_list.append(t2)

        t3 = (KEY_PLATE_MATERIAL, KEY_PLATE_FU, KEY_PLATE_FY)
        fu_fy_list.append(t3)

        return fu_fy_list

    def input_dictionary_design_pref(self):
        design_input = []
        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SUPTNGSEC_MATERIAL])
        design_input.append(t1)

        t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY])
        design_input.append(t1)

        t2 = (KEY_DISP_BEAMSEC, TYPE_COMBOBOX, [KEY_SUPTDSEC_MATERIAL])
        design_input.append(t2)

        t2 = (KEY_DISP_BEAMSEC, TYPE_TEXTBOX, [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY])
        design_input.append(t2)

        t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        design_input.append(t3)

        t3 = ("Bolt", TYPE_TEXTBOX, [KEY_DP_BOLT_MATERIAL_G_O])
        design_input.append(t3)

        t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        design_input.append(t4)

        t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        design_input.append(t4)

        t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        design_input.append(t5)

        t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_PLATE_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SUPTNGSEC_MATERIAL, KEY_SUPTDSEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_MATERIAL_G_O, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_WELD_FAB, KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_GAP,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_PLATE_MATERIAL], '')
        design_input.append(t2)

        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):

        fu = Material(design_dictionary[KEY_MATERIAL]).fu

        val = {KEY_DP_BOLT_TYPE: "Pretensioned",
               KEY_DP_BOLT_HOLE_TYPE: "Standard",
               KEY_DP_BOLT_MATERIAL_G_O: str(fu),
               KEY_DP_BOLT_SLIP_FACTOR: str(0.3),
               KEY_DP_WELD_FAB: KEY_DP_WELD_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "a - Sheared or hand flame cut",
               KEY_DP_DETAILING_GAP: '10',
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No',
               KEY_DP_DESIGN_METHOD: "Limit State Design",
               KEY_PLATE_MATERIAL: str(design_dictionary[KEY_MATERIAL])
               }[key]

        return val

    def refresh_input_dock(self):

        add_buttons = []

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC_DESIGNATION, KEY_CONN, VALUES_CONN_1, "Columns")
        add_buttons.append(t1)

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC_DESIGNATION, KEY_CONN, VALUES_CONN_2, "Beams")
        add_buttons.append(t1)

        t2 = (KEY_DISP_BEAMSEC, KEY_SUPTDSEC, TYPE_COMBOBOX, KEY_SUPTDSEC_DESIGNATION, None, None, "Beams")
        add_buttons.append(t2)

        return add_buttons

    def output_values(self, flag):
        return []

    def generate_missing_fields_error_string(self, missing_fields_list):
        """
        Args:
            missing_fields_list: list of fields that are not selected or entered
        Returns:
            error string that has to be displayed
        """
        # The base string which should be displayed
        information = "Please input the following required field"
        if len(missing_fields_list) > 1:
            # Adds 's' to the above sentence if there are multiple missing input fields
            information += "s"
        information += ": "
        # Loops through the list of the missing fields and adds each field to the above sentence with a comma

        for item in missing_fields_list:
            information = information + item + ", "

        # Removes the last comma
        information = information[:-2]
        information += "."

        return information

if __name__ == "__main__":
    connection = Connection()
    connection.test()
    connection.design()
