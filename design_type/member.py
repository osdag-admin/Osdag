from Common import *
from utils.common.load import Load
from utils.common.component import *
from design_type.main import Main

class Member(Main):

    def __init__(self):
        pass

    ########################################
    # Design Preference Functions Start
    ########################################

    def tab_angle_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "
        "In design preference, it shows other properties of section used "
        if not input_dictionary or input_dictionary[KEY_SECSIZE] == '' or \
                input_dictionary[KEY_MATERIAL] == 'Select Material' or \
                input_dictionary[KEY_SEC_PROFILE] not in ['Angles', 'Back to Back Angles', 'Star Angles']:
            designation = ''
            material_grade = ''
            section_profile = ''
            l = ''
            fu = ''
            fy = ''
            mass = ''
            area = ''
            a = ''
            b = ''
            thickness = ''
            root_radius = ''
            toe_radius = ''
            Cz = ''
            Cy = ''
            mom_inertia_z = ''
            mom_inertia_y = ''
            mom_inertia_u = ''
            mom_inertia_v = ''
            rad_of_gy_z = ''
            rad_of_gy_y = ''
            rad_of_gy_u = ''
            rad_of_gy_v = ''
            elast_sec_mod_z = ''
            elast_sec_mod_y = ''
            plast_sec_mod_z = ''
            plast_sec_mod_y = ''
            torsional_rigidity = ''
            source = ''
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
        else:
            designation = str(input_dictionary[KEY_SECSIZE][0])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            section_profile = str(input_dictionary[KEY_SEC_PROFILE])
            l = str(input_dictionary[KEY_LOCATION])
            Angle_attributes = Angle(designation,material_grade)
            Angle_attributes.connect_to_database_update_other_attributes_angles(designation, material_grade)
            source = str(Angle_attributes.source)
            fu = str(Angle_attributes.fu)
            fy = str(Angle_attributes.fy)
            a = (Angle_attributes.a)
            b = (Angle_attributes.b)
            thickness = (Angle_attributes.thickness)
            root_radius = str(Angle_attributes.root_radius)
            toe_radius = str(Angle_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            if section_profile == "Back to Back Angles":
                print(section_profile,"hjcxhf")
                Angle_attributes = BBAngle_Properties()
                mass = Angle_attributes.calc_Mass(a, b, thickness, l)
                area = Angle_attributes.calc_Area(a, b, thickness, l)
                Cz = Angle_attributes.calc_Cz(a, b, thickness, l)
                Cy = Angle_attributes.calc_Cy(a, b, thickness, l)
                mom_inertia_z = Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l)
                mom_inertia_y = Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l)
                mom_inertia_u = Angle_attributes.calc_MomentOfAreaU(a, b, thickness, l)
                mom_inertia_v = Angle_attributes.calc_MomentOfAreaV(a, b, thickness, l)
                rad_of_gy_z = Angle_attributes.calc_RogZ(a, b, thickness, l)
                rad_of_gy_y = Angle_attributes.calc_RogY(a, b, thickness, l)
                rad_of_gy_u = Angle_attributes.calc_RogU(a, b, thickness, l)
                rad_of_gy_v = Angle_attributes.calc_RogV(a, b, thickness, l)
                elast_sec_mod_z = Angle_attributes.calc_ElasticModulusZz(a, b, thickness, l)
                elast_sec_mod_y = Angle_attributes.calc_ElasticModulusZy(a, b, thickness, l)
                plast_sec_mod_z = Angle_attributes.calc_PlasticModulusZpz(a, b, thickness, l)
                plast_sec_mod_y = Angle_attributes.calc_PlasticModulusZpy(a, b, thickness, l)
                torsional_rigidity = Angle_attributes.calc_TorsionConstantIt(a, b, thickness, l)
            elif section_profile == "Star Angles":
                Angle_attributes = SAngle_Properties()
                mass = Angle_attributes.calc_Mass(a, b, thickness, l)
                area = Angle_attributes.calc_Area(a, b, thickness, l)
                Cz = Angle_attributes.calc_Cz(a, b, thickness, l)
                Cy = Angle_attributes.calc_Cy(a, b, thickness, l)
                mom_inertia_z = Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l)
                mom_inertia_y = Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l)
                mom_inertia_u = Angle_attributes.calc_MomentOfAreaU(a, b, thickness, l)
                mom_inertia_v = Angle_attributes.calc_MomentOfAreaV(a, b, thickness, l)
                rad_of_gy_z = Angle_attributes.calc_RogZ(a, b, thickness, l)
                rad_of_gy_y = Angle_attributes.calc_RogY(a, b, thickness, l)
                rad_of_gy_u = Angle_attributes.calc_RogU(a, b, thickness, l)
                rad_of_gy_v = Angle_attributes.calc_RogV(a, b, thickness, l)
                elast_sec_mod_z = Angle_attributes.calc_ElasticModulusZz(a, b, thickness, l)
                elast_sec_mod_y = Angle_attributes.calc_ElasticModulusZy(a, b, thickness, l)
                plast_sec_mod_z = Angle_attributes.calc_PlasticModulusZpz(a, b, thickness, l)
                plast_sec_mod_y = Angle_attributes.calc_PlasticModulusZpy(a, b, thickness, l)
                torsional_rigidity = Angle_attributes.calc_TorsionConstantIt(a, b, thickness, l)
            else:

                a = str(Angle_attributes.a)
                b = str(Angle_attributes.b)
                thickness = str(Angle_attributes.thickness)
                root_radius = str(Angle_attributes.root_radius)
                toe_radius = str(Angle_attributes.toe_radius)
                mass = str(Angle_attributes.mass)
                area = str(Angle_attributes.area)
                Cz = str(Angle_attributes.Cz)
                Cy = str(Angle_attributes.Cy)
                mom_inertia_z = str(Angle_attributes.mom_inertia_z)
                mom_inertia_y = str(Angle_attributes.mom_inertia_y)
                mom_inertia_u = str(Angle_attributes.mom_inertia_u)
                mom_inertia_v = str(Angle_attributes.mom_inertia_v)
                rad_of_gy_z = str(Angle_attributes.rad_of_gy_z)
                rad_of_gy_y = str(Angle_attributes.rad_of_gy_y)
                rad_of_gy_u = str(Angle_attributes.rad_of_gy_u)
                rad_of_gy_v = str(Angle_attributes.rad_of_gy_v)
                elast_sec_mod_z = str(Angle_attributes.elast_sec_mod_z)
                elast_sec_mod_y = str(Angle_attributes.elast_sec_mod_y)
                plast_sec_mod_z = str(Angle_attributes.plast_sec_mod_z)
                plast_sec_mod_y = str(Angle_attributes.plast_sec_mod_y)
                torsional_rigidity = str(Angle_attributes.It)
            # mass = str(Angle_attributes.mass)
            # area = str(Angle_attributes.area)
            # Cz = str(Angle_attributes.Cz)
            # Cy = str(Angle_attributes.Cy)
            # mom_inertia_z = str(Angle_attributes.mom_inertia_z)
            # mom_inertia_y = str(Angle_attributes.mom_inertia_y)
            # mom_inertia_u = str(Angle_attributes.mom_inertia_u)
            # mom_inertia_v = str(Angle_attributes.mom_inertia_v)
            # rad_of_gy_z = str(Angle_attributes.rad_of_gy_z)
            # rad_of_gy_y = str(Angle_attributes.rad_of_gy_y)
            # rad_of_gy_u = str(Angle_attributes.rad_of_gy_u)
            # rad_of_gy_v = str(Angle_attributes.rad_of_gy_v)
            # elast_sec_mod_z = str(Angle_attributes.elast_sec_mod_z)
            # elast_sec_mod_y = str(Angle_attributes.elast_sec_mod_y)
            # plast_sec_mod_z = str(Angle_attributes.plast_sec_mod_z)
            # plast_sec_mod_y = str(Angle_attributes.plast_sec_mod_y)
            # torsion_const = str(Angle_attributes.It)

        if KEY_SEC_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_SEC_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        section = []

        if input_dictionary:
            designation_list = input_dictionary[KEY_SECSIZE]
        else:
            designation_list = []

        t0 = (KEY_SECSIZE, KEY_DISP_DESIGNATION, TYPE_COMBOBOX, designation_list, designation)
        section.append(t0)

        t1 = (KEY_SECSIZE_SELECTED, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        section.append(t1)

        t1 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_TEXTBOX, None, section_profile)
        section.append(t1)

        t1 = (KEY_LOCATION, KEY_DISP_LOCATION, TYPE_TEXTBOX, None, l)
        section.append(t1)


        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        section.append(t2)

        material = connectdb("Material")
        t34 = (KEY_SEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        section.append(t34)

        t3 = (KEY_SEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        section.append(t3)

        t4 = (KEY_SEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        section.append(t5)

        t6 = ('Label_1', KEY_DISP_A, TYPE_TEXTBOX, None, a)
        section.append(t6)

        t6 = ('Label_2', KEY_DISP_B, TYPE_TEXTBOX, None, b)
        section.append(t6)

        t8 = ('Label_3', KEY_DISP_LEG_THK, TYPE_TEXTBOX, None, thickness)
        section.append(t8)

        t11 = ('Label_4', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
        section.append(t11)

        t12 = ('Label_5', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
        section.append(t12)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t18 = ('Label_9', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        section.append(t18)

        t19 = ('Label_10', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        section.append(t19)

        t18 = ('Label_7', KEY_DISP_Cz, TYPE_TEXTBOX, None, Cz)
        section.append(t18)

        t19 = ('Label_8', KEY_DISP_Cz, TYPE_TEXTBOX, None, Cy)
        section.append(t19)

        t20 = ('Label_11', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        section.append(t20)

        t21 = ('Label_12', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        section.append(t21)

        t13 = (None, None, TYPE_BREAK, None, None)
        section.append(t13)

        t14 = ('Label_6', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        section.append(t14)

        t18 = (None, None, TYPE_ENTER, None, None)
        section.append(t18)

        t18 = (None, None, TYPE_ENTER, None, None)
        section.append(t18)

        t15 = ('Label_27', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_28', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        section.append(t16)

        t18 = (None, None, TYPE_ENTER, None, None)
        section.append(t18)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t22 = ('Label_13', KEY_DISP_MOA_IU, TYPE_TEXTBOX, None, mom_inertia_u)
        section.append(t22)

        t23 = ('Label_14', KEY_DISP_MOA_IV, TYPE_TEXTBOX, None, mom_inertia_v)
        section.append(t23)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        section.append(t23)

        t22 = ('Label_17', KEY_DISP_ROG_RU, TYPE_TEXTBOX, None, rad_of_gy_u)
        section.append(t22)

        t23 = ('Label_18', KEY_DISP_ROG_RV, TYPE_TEXTBOX, None, rad_of_gy_v)
        section.append(t23)

        t24 = ('Label_19', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
        section.append(t24)

        t25 = ('Label_20', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
        section.append(t25)

        t26 = ('Label_21', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        section.append(t26)

        t27 = ('Label_22', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        section.append(t27)

        t27 = ('Label_23', KEY_DISP_It, TYPE_TEXTBOX, None, torsional_rigidity)

        section.append(t27)

        t28 = (None, None, TYPE_BREAK, None, None)
        section.append(t28)

        t29 = ('Label_24', 'Source', TYPE_TEXTBOX, None, source)
        section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        section.append(t30)

        t31 = ('Label_25', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_26', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, 'ResourceFiles/images/Angles.png')
        section.append(t33)

        return section

    def tab_channel_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "
        "In design preference, it shows other properties of section used "
        if not input_dictionary or input_dictionary[KEY_SECSIZE] == '' or \
                input_dictionary[KEY_MATERIAL] == 'Select Material' or \
                input_dictionary[KEY_SEC_PROFILE] not in ['Channels', 'Back to Back Channels']:
            designation = ''
            material_grade = ''
            fu = ''
            fy = ''
            mass = ''
            area = ''
            flange_width = ''
            flange_thickness = ''
            depth = ''
            web_thickness = ''
            flange_slope = ''
            root_radius = ''
            toe_radius = ''
            C_y = ''
            mom_inertia_z = ''
            mom_inertia_y = ''
            rad_of_gy_z = ''
            rad_of_gy_y = ''
            elast_sec_mod_z = ''
            elast_sec_mod_y = ''
            plast_sec_mod_z = ''
            plast_sec_mod_y = ''
            source = ''
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            Type='Rolled'
        else:
            designation = str(input_dictionary[KEY_SECSIZE][0])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            Channel_attributes = Channel(designation,material_grade)
            Channel_attributes.connect_to_database_update_other_attributes_channels(designation, material_grade)
            source = str(Channel_attributes.source)
            fu = str(Channel_attributes.fu)
            fy = str(Channel_attributes.fy)
            flange_width = str(Channel_attributes.flange_width)
            flange_thickness = str(Channel_attributes.flange_thickness)
            depth = str(Channel_attributes.depth)
            web_thickness = str(Channel_attributes.web_thickness)
            flange_slope = str(Channel_attributes.flange_slope)
            root_radius = str(Channel_attributes.root_radius)
            toe_radius = str(Channel_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = str(Channel_attributes.mass)
            area = str(Channel_attributes.area)
            C_y = str(Channel_attributes.Cy)
            mom_inertia_z = str(Channel_attributes.mom_inertia_z)
            mom_inertia_y = str(Channel_attributes.mom_inertia_y)
            rad_of_gy_z = str(Channel_attributes.rad_of_gy_z)
            rad_of_gy_y = str(Channel_attributes.rad_of_gy_y)
            elast_sec_mod_z = str(Channel_attributes.elast_sec_mod_z)
            elast_sec_mod_y = str(Channel_attributes.elast_sec_mod_y)
            plast_sec_mod_z = str(Channel_attributes.plast_sec_mod_z)
            plast_sec_mod_y = str(Channel_attributes.plast_sec_mod_y)
            Type = str(Channel_attributes.type)

        if KEY_SEC_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_SEC_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        section = []

        if input_dictionary:
            designation_list = input_dictionary[KEY_SECSIZE]
        else:
            designation_list = []

        t0 = (KEY_SECSIZE, KEY_DISP_DESIGNATION, TYPE_COMBOBOX, designation_list, designation)
        section.append(t0)

        t1 = (KEY_SECSIZE_SELECTED, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        section.append(t2)

        material = connectdb("Material")
        t34 = (KEY_SEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        section.append(t34)

        t3 = (KEY_SEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        section.append(t3)

        t4 = (KEY_SEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        section.append(t5)

        t6 = ('Label_1', KEY_DISP_FLANGE_W, TYPE_TEXTBOX, None, flange_width)
        section.append(t6)

        t7 = ('Label_2', KEY_DISP_FLANGE_T, TYPE_TEXTBOX, None, flange_thickness)
        section.append(t7)

        t8 = ('Label_3', KEY_DISP_DEPTH, TYPE_TEXTBOX, None, depth)
        section.append(t8)

        t22 = ('Label_13', KEY_DISP_WEB_T, TYPE_TEXTBOX, None, web_thickness)
        section.append(t22)

        t23 = ('Label_14', KEY_DISP_FLANGE_S, TYPE_TEXTBOX, None, flange_slope)
        section.append(t23)

        t11 = ('Label_4', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
        section.append(t11)

        t12 = ('Label_5', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
        section.append(t12)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t18 = ('Label_9', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        section.append(t18)

        t19 = ('Label_10', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        section.append(t19)

        t20 = ('Label_17', KEY_DISP_Cy, TYPE_TEXTBOX, None, C_y)
        section.append(t20)

        t20 = ('Label_11', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        section.append(t20)

        t21 = ('Label_12', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        section.append(t21)

        t13 = (None, None, TYPE_BREAK, None, None)
        section.append(t13)

        t14 = ('Label_6', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], Type)
        section.append(t14)

        t18 = (None, None, TYPE_ENTER, None, None)
        section.append(t18)

        t18 = (None, None, TYPE_ENTER, None, None)
        section.append(t18)

        t15 = ('Label_7', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_8', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        section.append(t16)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        section.append(t23)

        t24 = ('Label_19', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
        section.append(t24)

        t25 = ('Label_20', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
        section.append(t25)

        t26 = ('Label_21', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        section.append(t26)

        t27 = ('Label_22', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        section.append(t27)

        t28 = (None, None, TYPE_BREAK, None, None)
        section.append(t28)

        t29 = ('Label_23', 'Source', TYPE_TEXTBOX, None, source)
        section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        section.append(t30)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_25', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, 'ResourceFiles\images\Channels.png')
        section.append(t33)

        return section


    def get_new_angle_section_properties(self):

        print('vvvvv')
        designation = self[0]
        material_grade = self[1]
        l = self[2]
        profile = self[3]

        Angle_attributes = Angle(designation, material_grade)
        Angle_attributes.connect_to_database_update_other_attributes_angles(designation, material_grade)
        source = str(Angle_attributes.source)
        Type= str(Angle_attributes.type)
        fu = str(Angle_attributes.fu)
        fy = str(Angle_attributes.fy)
        a = (Angle_attributes.a)
        b = (Angle_attributes.b)
        thickness = (Angle_attributes.thickness)
        root_radius = str(Angle_attributes.root_radius)
        toe_radius = str(Angle_attributes.toe_radius)

        if profile == "Back to Back Angles":
            print(profile,"555555")
            Angle_attributes = BBAngle_Properties()
            mass = Angle_attributes.calc_Mass(a, b, thickness, l)
            area = Angle_attributes.calc_Area(a, b,thickness, l)
            Cz = Angle_attributes.calc_Cz(a, b, thickness, l)
            Cy = Angle_attributes.calc_Cy(a, b, thickness, l)
            mom_inertia_z = Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l)
            mom_inertia_y = Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l)
            mom_inertia_u = Angle_attributes.calc_MomentOfAreaU(a, b, thickness, l)
            mom_inertia_v = Angle_attributes.calc_MomentOfAreaV(a, b, thickness, l)
            rad_of_gy_z = Angle_attributes.calc_RogZ(a, b, thickness, l)
            rad_of_gy_y = Angle_attributes.calc_RogY(a, b, thickness, l)
            rad_of_gy_u = Angle_attributes.calc_RogU(a, b, thickness, l)
            rad_of_gy_v = Angle_attributes.calc_RogV(a, b, thickness, l)
            elast_sec_mod_z = Angle_attributes.calc_ElasticModulusZz(a, b, thickness, l)
            elast_sec_mod_y = Angle_attributes.calc_ElasticModulusZy(a, b, thickness, l)
            plast_sec_mod_z = Angle_attributes.calc_PlasticModulusZpz(a, b, thickness, l)
            plast_sec_mod_y = Angle_attributes.calc_PlasticModulusZpy(a, b, thickness, l)
            torsional_rigidity = Angle_attributes.calc_TorsionConstantIt(a, b,thickness, l)
        elif profile == "Star Angles":
            Angle_attributes = SAngle_Properties()
            mass = Angle_attributes.calc_Mass(a, b,thickness, l)
            area = Angle_attributes.calc_Area(a, b,thickness, l)
            Cz = Angle_attributes.calc_Cz(a, b, thickness, l)
            Cy = Angle_attributes.calc_Cy(a, b,thickness, l)
            mom_inertia_z= Angle_attributes.calc_MomentOfAreaZ(a, b,thickness, l)
            mom_inertia_y = Angle_attributes.calc_MomentOfAreaY(a, b,thickness, l)
            mom_inertia_u = Angle_attributes.calc_MomentOfAreaU(a, b,thickness, l)
            mom_inertia_v = Angle_attributes.calc_MomentOfAreaV(a, b,thickness, l)
            rad_of_gy_z = Angle_attributes.calc_RogZ(a, b,thickness, l)
            rad_of_gy_y = Angle_attributes.calc_RogY(a, b,thickness, l)
            rad_of_gy_u = Angle_attributes.calc_RogU(a, b,thickness, l)
            rad_of_gy_v = Angle_attributes.calc_RogV(a, b,thickness, l)
            elast_sec_mod_z = Angle_attributes.calc_ElasticModulusZz(a, b,thickness, l)
            elast_sec_mod_y = Angle_attributes.calc_ElasticModulusZy(a, b,thickness, l)
            plast_sec_mod_z = Angle_attributes.calc_PlasticModulusZpz(a, b,thickness, l)
            plast_sec_mod_y= Angle_attributes.calc_PlasticModulusZpy(a, b,thickness, l)
            torsional_rigidity = Angle_attributes.calc_TorsionConstantIt(a, b,thickness, l)
        else:
            print(profile, "11111")
            a = str(Angle_attributes.a)
            b = str(Angle_attributes.b)
            thickness = str(Angle_attributes.thickness)
            mass = str(Angle_attributes.mass)
            area = str(Angle_attributes.area)
            Cz = str(Angle_attributes.Cz)
            Cy = str(Angle_attributes.Cy)
            mom_inertia_z = str(Angle_attributes.mom_inertia_z)
            mom_inertia_y = str(Angle_attributes.mom_inertia_y)
            mom_inertia_u = str(Angle_attributes.mom_inertia_u)
            mom_inertia_v = str(Angle_attributes.mom_inertia_v)
            rad_of_gy_z = str(Angle_attributes.rad_of_gy_z)
            rad_of_gy_y = str(Angle_attributes.rad_of_gy_y)
            rad_of_gy_u = str(Angle_attributes.rad_of_gy_u)
            rad_of_gy_v = str(Angle_attributes.rad_of_gy_v)
            elast_sec_mod_z = str(Angle_attributes.elast_sec_mod_z)
            elast_sec_mod_y = str(Angle_attributes.elast_sec_mod_y)
            plast_sec_mod_z = str(Angle_attributes.plast_sec_mod_z)
            plast_sec_mod_y = str(Angle_attributes.plast_sec_mod_y)
            torsional_rigidity = str(Angle_attributes.It)
        d = {
             KEY_SECSIZE_SELECTED:designation,
            KEY_SEC_MATERIAL: material_grade,
             KEY_SEC_FY:fy,
             KEY_SEC_FU:fu,
             'Label_1': a,
             'Label_2': b,
             'Label_3':thickness,
             'Label_4':root_radius,
             'Label_5':toe_radius,
            'Label_6':Type,
            'Label_7': Cz,
            'Label_8': Cy,
             'Label_9':mass,
             'Label_10':area,
             'Label_11':mom_inertia_z,
             'Label_12':mom_inertia_y,
             'Label_13':mom_inertia_u,
             'Label_14':mom_inertia_v,
             'Label_15':rad_of_gy_z,
             'Label_16':rad_of_gy_y,
             'Label_17':rad_of_gy_u,
             'Label_18':rad_of_gy_v,
             'Label_19':elast_sec_mod_z,
             'Label_20':elast_sec_mod_y,
             'Label_21':plast_sec_mod_z,
             'Label_22':plast_sec_mod_y,
             'Label_23':torsional_rigidity
        }
        return d


    def get_new_channel_section_properties(self):
        designation = self[0]
        material_grade = self[1]
        Channel_attributes = Channel(designation, material_grade)
        Channel_attributes.connect_to_database_update_other_attributes_channels(designation, material_grade)

        source = str(Channel_attributes.source)
        Type = str(Channel_attributes.type)
        fu = str(Channel_attributes.fu)
        fy = str(Channel_attributes.fy)
        flange_width = str(Channel_attributes.flange_width)
        flange_thickness = str(Channel_attributes.flange_thickness)
        depth = str(Channel_attributes.depth)
        web_thickness = str(Channel_attributes.web_thickness)
        flange_slope = str(Channel_attributes.flange_slope)
        root_radius = str(Channel_attributes.root_radius)
        toe_radius = str(Channel_attributes.toe_radius)
        m_o_e = "200"
        m_o_r = "76.9"
        p_r = "0.3"
        t_e = "12"
        mass = str(Channel_attributes.mass)
        area = str(Channel_attributes.area)
        Cy = str(Channel_attributes.Cy)
        mom_inertia_z = str(Channel_attributes.mom_inertia_z)
        mom_inertia_y = str(Channel_attributes.mom_inertia_y)
        rad_of_gy_z = str(Channel_attributes.rad_of_gy_z)
        rad_of_gy_y = str(Channel_attributes.rad_of_gy_y)
        elast_sec_mod_z = str(Channel_attributes.elast_sec_mod_z)
        elast_sec_mod_y = str(Channel_attributes.elast_sec_mod_y)
        plast_sec_mod_z = str(Channel_attributes.plast_sec_mod_z)
        plast_sec_mod_y = str(Channel_attributes.plast_sec_mod_y)

        d = {
            KEY_SECSIZE_SELECTED: designation,
            KEY_SEC_MATERIAL: material_grade,
            KEY_SEC_FY: fy,
            KEY_SEC_FU: fu,
            'Label_1': str(flange_width),
            'Label_2': str(flange_thickness),
            'Label_3': str(depth),
            'Label_13': str(web_thickness),
            'Label_14': str(flange_slope),
            'Label_5': str(toe_radius),
            'Label_6': str(Type),
            'Label_4': str(root_radius),
            'Label_9': str(mass),
            'Label_10': str(area),
            'Label_11': str(mom_inertia_z),
            'Label_12': str(mom_inertia_y),
            'Label_15': str(rad_of_gy_z),
            'Label_16': str(rad_of_gy_y),
            'Label_17': str(Cy),
            'Label_19': str(elast_sec_mod_z),
            'Label_20': str(elast_sec_mod_y),
            'Label_21': str(plast_sec_mod_z),
            'Label_22': str(plast_sec_mod_y),
            'Label_23': str(source)}
        return d

    def get_new_angle_section_properties(self):

        designation = self[0]
        material_grade = self[1]
        Angle_attributes = Angle(designation, material_grade)
        Angle_attributes.connect_to_database_update_other_attributes_angles(designation, material_grade)
        source = str(Angle_attributes.source)
        Type = str(Angle_attributes.type)
        fu = str(Angle_attributes.fu)
        fy = str(Angle_attributes.fy)
        a = str(Angle_attributes.leg_a_length)
        b = str(Angle_attributes.leg_b_length)
        thickness = str(Angle_attributes.thickness)
        root_radius = str(Angle_attributes.root_radius)
        toe_radius = str(Angle_attributes.toe_radius)
        mass = str(Angle_attributes.mass)
        area = str(Angle_attributes.area)
        Cz = str(Angle_attributes.Cz)
        Cy = str(Angle_attributes.Cy)
        mom_inertia_z = str(Angle_attributes.mom_inertia_z)
        mom_inertia_y = str(Angle_attributes.mom_inertia_y)
        mom_inertia_u = str(Angle_attributes.mom_inertia_u)
        mom_inertia_v = str(Angle_attributes.mom_inertia_v)
        rad_of_gy_z = str(Angle_attributes.rad_of_gy_z)
        rad_of_gy_y = str(Angle_attributes.rad_of_gy_y)
        rad_of_gy_u = str(Angle_attributes.rad_of_gy_u)
        rad_of_gy_v = str(Angle_attributes.rad_of_gy_v)
        elast_sec_mod_z = str(Angle_attributes.elast_sec_mod_z)
        elast_sec_mod_y = str(Angle_attributes.elast_sec_mod_y)
        plast_sec_mod_z = str(Angle_attributes.plast_sec_mod_z)
        plast_sec_mod_y = str(Angle_attributes.plast_sec_mod_y)
        torsion_const = str(Angle_attributes.It)
        d = {
            KEY_SECSIZE_SELECTED: designation,
            KEY_SEC_MATERIAL: material_grade,
            KEY_SEC_FY: fy,
            KEY_SEC_FU: fu,
            'Label_1': a,
            'Label_2': b,
            'Label_3': thickness,
            'Label_4': root_radius,
            'Label_5': toe_radius,
            'Label_6': Type,
            'Label_7': Cz,
            'Label_8': Cy,
            'Label_9': mass,
            'Label_10': area,
            'Label_11': mom_inertia_z,
            'Label_12': mom_inertia_y,
            'Label_13': mom_inertia_u,
            'Label_14': mom_inertia_v,
            'Label_15': rad_of_gy_z,
            'Label_16': rad_of_gy_y,
            'Label_17': rad_of_gy_u,
            'Label_18': rad_of_gy_v,
            'Label_19': elast_sec_mod_z,
            'Label_20': elast_sec_mod_y,
            'Label_21': plast_sec_mod_z,
            'Label_22': plast_sec_mod_y,
            'Label_23': torsion_const,
            'Label_24': source}
        return d

    def get_fu_fy_section(self):
        material_grade = self[0]
        designation = self[2][KEY_SECSIZE_SELECTED]
        # designation = self[1][KEY_SECSIZE][0]
        profile = self[1][KEY_SEC_PROFILE]

        if material_grade != "Select Material" and designation != "":
            if profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
                Angle_sec_attributes = Angle(designation,material_grade)
                Angle_sec_attributes.connect_to_database_update_other_attributes_angles(designation, material_grade)
                fu = str(Angle_sec_attributes.fu)
                fy = str(Angle_sec_attributes.fy)
            elif profile in ['Channels', 'Back to Back Channels']:
                Channel_Attributes = Channel(designation,material_grade)
                Channel_Attributes.connect_to_database_update_other_attributes_channels(designation, material_grade)
                fu = str(Channel_Attributes.fu)
                fy = str(Channel_Attributes.fy)
            elif profile in ['Beams']:
                table = "Beams"
                I_sec_attributes = Section(designation)
                I_sec_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
                fu = str(I_sec_attributes.fu)
                fy = str(I_sec_attributes.fy)
            else:
                table = "Columns"
                I_sec_attributes = Section(designation)
                I_sec_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
                fu = str(I_sec_attributes.fu)
                fy = str(I_sec_attributes.fy)
        else:
            fu = ''
            fy = ''

        d = {KEY_SEC_MATERIAL:material_grade,
             KEY_SUPTNGSEC_FU: fu,
             KEY_SUPTNGSEC_FY: fy,
             KEY_SUPTDSEC_FU: fu,
             KEY_SUPTDSEC_FY: fy,
             KEY_SEC_FU: fu,
             KEY_SEC_FY: fy,
             KEY_BASE_PLATE_FU: fu,
             KEY_BASE_PLATE_FY: fy}

        return d

    def get_fu_fy(self):
        material_grade = self[0]

        if material_grade != "Select Material":
            m_conn = Material(material_grade)
            fu_conn = m_conn.fu
            fy_20 = m_conn.fy_20
            fy_20_40 = m_conn.fy_20_40
            fy_40 = m_conn.fy_40
        else:
            fu_conn = ''
            fy_20 = ''
            fy_20_40 = ''
            fy_40 = ''

        d = {
             KEY_CONNECTOR_FU: fu_conn,
             KEY_CONNECTOR_FY_20: fy_20,
             KEY_CONNECTOR_FY_20_40: fy_20_40,
             KEY_CONNECTOR_FY_40: fy_40}

        return d

    def edit_tabs(self):
        """

        :return: This function is used when the whole tab is conditional i.e., to be changed based on the change in
        input dock key.
        This returns a list of tuples which contains the key whose change will decide the tab, title of the tab,
        function to get tab contents and Type of change (It can be changed(TYPE_CHANGE_TAB) or removed(TYPE_REMOVE_TAB))

        [Title of tab, Key of input dock, Type of change, function of tab]

        the function of tab has inbuilt arguments of key of input dock passed in this tuple
        the fucntion returns name of tab to be displayed. So this fucntion returns list in this format,
        [current tab name, key that may cause the change, changed/removed, new tab name]
        """

        edit_list = []

        t1 = (DISP_TITLE_ANGLE, KEY_SEC_PROFILE, TYPE_REMOVE_TAB, self.get_selected_tab)
        edit_list.append(t1)

        t1 = (DISP_TITLE_CHANNEL, KEY_SEC_PROFILE, TYPE_REMOVE_TAB, self.get_selected_tab)
        edit_list.append(t1)

        return edit_list

    def get_selected_tab(self):
        """

        :return: This function have key value passed in self. This return name of the tab selected
        based on the value of the key passed.
        """
        if self in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return DISP_TITLE_ANGLE
        elif self in [ 'Channels', 'Back to Back Channels']:
            return DISP_TITLE_CHANNEL
        elif self in['Beams']:
            return KEY_DISP_BEAMSEC
        else:
            return KEY_DISP_COLSEC

    # def list_for_fu_fy_validation(self):
    #     """
    #     This function is no longer required
    #     """
    #
    #     fu_fy_list = []
    #
    #     t1 = (KEY_SUPTNGSEC_MATERIAL, KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY)
    #     fu_fy_list.append(t1)
    #
    #     t2 = (KEY_SUPTDSEC_MATERIAL, KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY)
    #     fu_fy_list.append(t2)
    #
    #     t3 = (KEY_CONNECTOR_MATERIAL, KEY_CONNECTOR_FU, KEY_CONNECTOR_FY)
    #     fu_fy_list.append(t3)
    #
    #     return fu_fy_list

    def get_values_for_design_pref(self, key, design_dictionary):
        """
        This is used to get default values for design preferences. This is called to get design dictionary,
        when design preferences are not opened by the user. (Usually, design preferences is added to input dictionary
        when user clicks on 'save' of design preferences)
        :param key: list of keys of design preferences to be stored
        :param design_dictionary: Input dock design dictionary (since for some keys, input dock values are default)
        :return: returns a design preference dictionary which will be appended to input dock dictionary
        """

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            fu = Material(design_dictionary[KEY_MATERIAL], 41).fu
        else:
            fu = ''

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
               KEY_CONNECTOR_MATERIAL: str(design_dictionary[KEY_MATERIAL])
               }[key]

        return val

    def refresh_input_dock(self):

        add_buttons = []

        t1 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              ['Angles', 'Back to Back Angles', 'Star Angles'], "Angles")
        add_buttons.append(t1)

        t1 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              ['Channels', 'Back to Back Channels'], "Channels")
        add_buttons.append(t1)

        t1 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              ['Beams'], "Beams")
        add_buttons.append(t1)

        t1 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              ['Columns'], "Columns")
        add_buttons.append(t1)

        return add_buttons

    ########################################
    # Design Preference Functions End
    ########################################


    # def customized_input(self):
    #
    #     list1 = []
    #     t1 = (KEY_GRD, self.grdval_customized)
    #     list1.append(t1)
    #     t3 = (KEY_D, self.diam_bolt_customized)
    #     list1.append(t3)
    #     t6 = (KEY_PLATETHK, self.plate_thick_customized)
    #     list1.append(t6)
    #     # t8 = (KEY_SIZE, self.size_customized)
    #     # list1.append(t8)
    #     return list1

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
        d = VALUES_PLATETHK_CUSTOMIZED
        return d

    #
    # @staticmethod
    # def size_customized():
    #     d = VALUES_SIZE_CUSTOMIZED
    #     return d

    # def input_value_changed(self):
    #     pass

    def set_input_values(self, design_dictionary):
        pass
        # self.mainmodule = "Tension"
        # self.connectivity = design_dictionary[KEY_CONN]

        # if self.connectivity in VALUES_CONN_1:
        #     self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_MATERIAL])
        # else:
        #     self.supporting_section = Beam(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_MATERIAL])


    def new_material(self):

        selected_material = self[0]
        if selected_material == "Custom":
            return True
        else:
            return False

