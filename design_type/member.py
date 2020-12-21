from Common import *
from utils.common.load import Load
from utils.common.component import *
from utils.common.Section_Properties_Calculator import *
from design_type.main import Main

class Member(Main):

    def __init__(self):
        super(Member, self).__init__()

    ########################################
    # Design Preference Functions Start
    ########################################
    def df_conn_image(self):

        "Function to populate section size based on the type of section "
        img = self[0]
        if img == VALUES_SEC_PROFILE_2[0]:
            return VALUES_IMG_TENSIONBOLTED[0]
        elif img == VALUES_SEC_PROFILE_2[1]:
            return VALUES_IMG_TENSIONBOLTED[1]
        elif img == VALUES_SEC_PROFILE_2[2]:
            return VALUES_IMG_TENSIONBOLTED[2]
        elif img == VALUES_SEC_PROFILE_2[3]:
            return VALUES_IMG_TENSIONBOLTED[3]
        else:
            return VALUES_IMG_TENSIONBOLTED[4]


    def tab_angle_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "
        "In design preference, it shows other properties of section used "
        if not input_dictionary or input_dictionary[KEY_SECSIZE] == [] or \
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
            plate_thk = ''
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
            Type = ''
            source = 'Custom'
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            image = ''
        else:
            designation = str(input_dictionary[KEY_SECSIZE][0])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            section_profile = str(input_dictionary[KEY_SEC_PROFILE])
            l = str(input_dictionary[KEY_LOCATION])
            Angle_attributes = Angle(designation,material_grade)
            source = str(Angle_attributes.source)
            fu = str(Angle_attributes.fu)
            fy = str(Angle_attributes.fy)
            a = (Angle_attributes.a)
            b = (Angle_attributes.b)
            thickness = (Angle_attributes.thickness)
            root_radius = str(Angle_attributes.root_radius)
            toe_radius = str(Angle_attributes.toe_radius)
            plate_thk = float(input_dictionary[KEY_PLATETHK][0])
            Type = str(Angle_attributes.type)
            source = str(Angle_attributes.source)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            if section_profile == 'Angles':
                mass = str(round((Angle_attributes.mass), 2))
                area = str(round((Angle_attributes.area / 100), 2))
                Cz = str(round((Angle_attributes.Cz / 10), 2))
                Cy = str(round((Angle_attributes.Cy / 10), 2))
                mom_inertia_z = str(round((Angle_attributes.mom_inertia_z) / 10000, 2))
                mom_inertia_y = str(round((Angle_attributes.mom_inertia_y) / 10000, 2))
                mom_inertia_u = str(round((Angle_attributes.mom_inertia_u) / 10000, 2))
                mom_inertia_v = str(round((Angle_attributes.mom_inertia_v) / 10000, 2))
                rad_of_gy_z = str(round((Angle_attributes.rad_of_gy_z / 10), 2))
                rad_of_gy_y = str(round((Angle_attributes.rad_of_gy_y / 10), 2))
                rad_of_gy_u = str(round((Angle_attributes.rad_of_gy_u / 10), 2))
                rad_of_gy_v = str(round((Angle_attributes.rad_of_gy_v / 10), 2))
                elast_sec_mod_z = str(round((Angle_attributes.elast_sec_mod_z / 1000), 2))
                elast_sec_mod_y = str(round((Angle_attributes.elast_sec_mod_y / 1000), 2))
                plast_sec_mod_z = str(round((Angle_attributes.plast_sec_mod_z / 1000), 2))
                plast_sec_mod_y = str(round((Angle_attributes.plast_sec_mod_y / 1000), 2))
                torsional_rigidity = str(round((Angle_attributes.It / 10000), 2))
                if a == b:
                    image = VALUES_IMG_TENSIONBOLTED_DF01[0]
                else:
                    image = VALUES_IMG_TENSIONBOLTED_DF02[0]

            else:
                if section_profile == "Back to Back Angles":
                    print(section_profile, "hjcxhf")
                    Angle_attributes = BBAngle_Properties()
                    Angle_attributes.data(designation, material_grade)
                    if l == "Long Leg":
                        if a == b:
                            image = VALUES_IMG_TENSIONBOLTED_DF01[1]
                        else:
                            image = VALUES_IMG_TENSIONBOLTED_DF02[1]
                        Cz = str(Angle_attributes.calc_Cz(a, b,thickness, l))
                        Cy = "N/A"
                    else:
                        if a == b:
                            image = VALUES_IMG_TENSIONBOLTED_DF01[2]
                        else:
                            image = VALUES_IMG_TENSIONBOLTED_DF02[2]
                        Cy =  "N/A"
                        Cz = str(Angle_attributes.calc_Cz(a, b,thickness, l))
                    mass = str(Angle_attributes.calc_Mass(a, b, thickness, l))
                    area = str(Angle_attributes.calc_Area(a, b, thickness, l))
                    mom_inertia_z = str(Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l, plate_thk))
                    mom_inertia_y = str(Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l, plate_thk))
                    mom_inertia_u = str(Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l, plate_thk))
                    mom_inertia_v = str(Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l, plate_thk))
                    rad_of_gy_z = str(Angle_attributes.calc_RogZ(a, b, thickness, l, plate_thk))
                    rad_of_gy_y = str(Angle_attributes.calc_RogY(a, b, thickness, l, plate_thk))
                    rad_of_gy_u = str(Angle_attributes.calc_RogY(a, b, thickness, l, plate_thk))
                    rad_of_gy_v = str(Angle_attributes.calc_RogZ(a, b, thickness, l, plate_thk))
                    elast_sec_mod_z = str(Angle_attributes.calc_ElasticModulusZz(a, b, thickness, l, plate_thk))
                    elast_sec_mod_y = str(Angle_attributes.calc_ElasticModulusZy(a, b, thickness, l, plate_thk))
                    plast_sec_mod_z = str(Angle_attributes.calc_PlasticModulusZpz(a, b, thickness, l, plate_thk))
                    plast_sec_mod_y = str(Angle_attributes.calc_PlasticModulusZpy(a, b, thickness, l, plate_thk))
                    torsional_rigidity = str(Angle_attributes.calc_TorsionConstantIt(a, b, thickness, l))
                else:  # "Star Angles":
                    Angle_attributes = SAngle_Properties()
                    # Angle_attributes.data(designation, material_grade)
                    if l == "Long Leg":
                        if a == b:
                            image = VALUES_IMG_TENSIONBOLTED_DF01[3]
                        else:
                            image = VALUES_IMG_TENSIONBOLTED_DF02[3]
                    else:
                        if a == b:
                            image = VALUES_IMG_TENSIONBOLTED_DF01[4]
                        else:
                            image = VALUES_IMG_TENSIONBOLTED_DF02[4]
                    Cz = "N/A"
                    Cy = "N/A"
                    mass = str(Angle_attributes.calc_Mass(a, b,thickness, l))
                    area = str(Angle_attributes.calc_Area(a, b, thickness, l))
                    mom_inertia_z = str(Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l, plate_thk))
                    mom_inertia_y = str(Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l, plate_thk))
                    mom_inertia_u = str(Angle_attributes.calc_MomentOfAreaU(a, b, thickness, l, plate_thk))
                    mom_inertia_v = str(Angle_attributes.calc_MomentOfAreaV(a, b, thickness, l, plate_thk))
                    rad_of_gy_z = str(Angle_attributes.calc_RogZ(a, b, thickness, l, plate_thk))
                    rad_of_gy_y = str(Angle_attributes.calc_RogY(a, b, thickness, l, plate_thk))
                    rad_of_gy_u = str(Angle_attributes.calc_RogU(a, b, thickness, l, plate_thk))
                    rad_of_gy_v = str(Angle_attributes.calc_RogV(a, b, thickness, l, plate_thk))
                    elast_sec_mod_z = str(Angle_attributes.calc_ElasticModulusZz(a, b, thickness, l,plate_thk))
                    elast_sec_mod_y = str(Angle_attributes.calc_ElasticModulusZy(a, b, thickness, l,plate_thk))
                    plast_sec_mod_z = str(Angle_attributes.calc_PlasticModulusZpz(a, b, thickness, l,plate_thk))
                    plast_sec_mod_y = str(Angle_attributes.calc_PlasticModulusZpy(a, b, thickness, l,plate_thk))
                    torsional_rigidity = str(Angle_attributes.calc_TorsionConstantIt(a, b, thickness, l))

        # if KEY_SEC_MATERIAL in input_dictionary.keys():
        #     material_grade = input_dictionary[KEY_SEC_MATERIAL]
        #     material_attributes = Material(material_grade)
        #     fu = material_attributes.fu
        #     fy = material_attributes.fy

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

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        section.append(t34)

        t3 = (KEY_SEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        section.append(t3)

        t4 = (KEY_SEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        section.append(t4)

        t15 = ('Label_27', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_28', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        section.append(t16)

        t31 = ('Label_25', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_26', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        section.append(t32)

        t14 = ('Label_6', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], Type)
        section.append(t14)

        t29 = (KEY_SOURCE, KEY_DISP_SOURCE, TYPE_TEXTBOX, None, source)
        section.append(t29)

        t13 = (None, None, TYPE_BREAK, None, None)
        section.append(t13)

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

        t12 = ('Label_0', KEY_DISP_DPPLATETHK, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, plate_thk)
        section.append(t12)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t18 = ('Label_9', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        section.append(t18)

        t19 = ('Label_10', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        section.append(t19)

        t18 = ('Label_7', KEY_DISP_Cz, TYPE_TEXTBOX, None, Cz)
        section.append(t18)

        t19 = ('Label_8', KEY_DISP_Cy, TYPE_TEXTBOX, None, Cy)
        section.append(t19)

        t20 = ('Label_11', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        section.append(t20)

        t21 = ('Label_12', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        section.append(t21)

        # t13 = (None, None, TYPE_BREAK, None, None)
        # section.append(t13)
        #
        #
        # t18 = (None, None, TYPE_ENTER, None, None)
        # section.append(t18)

        # t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        # section.append(t17)

        t22 = ('Label_13', KEY_DISP_MOA_IU, TYPE_TEXTBOX, None, mom_inertia_u)
        section.append(t22)

        t23 = ('Label_14', KEY_DISP_MOA_IV, TYPE_TEXTBOX, None, mom_inertia_v)
        section.append(t23)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        section.append(t23)

        t13 = (None, None, TYPE_BREAK, None, None)
        section.append(t13)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, image)
        section.append(t33)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

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

        return section

    def tab_channel_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "
        "In design preference, it shows other properties of section used "
        if not input_dictionary or input_dictionary[KEY_SECSIZE] == [] or \
                input_dictionary[KEY_MATERIAL] == 'Select Material' or \
                input_dictionary[KEY_SEC_PROFILE] not in ['Channels', 'Back to Back Channels']:
            designation = ''
            material_grade = ''
            section_profile = ''
            l = ''
            fu = ''
            fy = ''
            mass = ''
            area = ''
            f_w = ''
            f_t = ''
            w_h = ''
            w_t = ''
            flange_slope = ''
            root_radius = ''
            toe_radius = ''
            plate_thk = ''
            C_y = ''
            mom_inertia_z = ''
            mom_inertia_y = ''
            rad_of_gy_z = ''
            rad_of_gy_y = ''
            elast_sec_mod_z = ''
            elast_sec_mod_y = ''
            plast_sec_mod_z = ''
            plast_sec_mod_y = ''
            source = 'Custom'
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            Type='Rolled'
            image = ''
            It = ""
            Iw = ""

        else:
            designation = str(input_dictionary[KEY_SECSIZE][0])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            section_profile = str(input_dictionary[KEY_SEC_PROFILE])
            l = str(input_dictionary[KEY_LOCATION])
            Channel_attributes = Channel(designation,material_grade)
            source = str(Channel_attributes.source)
            fu = str(Channel_attributes.fu)
            fy = str(Channel_attributes.fy)
            f_w = (Channel_attributes.flange_width)
            f_t = (Channel_attributes.flange_thickness)
            w_h = (Channel_attributes.depth)
            w_t = (Channel_attributes.web_thickness)
            flange_slope = float(Channel_attributes.flange_slope)
            root_radius = str(Channel_attributes.root_radius)
            toe_radius = str(Channel_attributes.toe_radius)
            plate_thk = float(input_dictionary[KEY_PLATETHK][0])
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            Type = str(Channel_attributes.type)
            if section_profile == "Channels":
                mass = str(round((Channel_attributes.mass), 2))
                area = str(round((Channel_attributes.area / 100), 2))
                C_y = str(round((Channel_attributes.Cy / 10), 2))
                mom_inertia_z = str(round((Channel_attributes.mom_inertia_z) / 10000, 2))
                mom_inertia_y = str(round((Channel_attributes.mom_inertia_y) / 10000, 2))
                rad_of_gy_z = str(round((Channel_attributes.rad_of_gy_z / 10), 2))
                rad_of_gy_y = str(round((Channel_attributes.rad_of_gy_y / 10), 2))
                elast_sec_mod_z = str(round((Channel_attributes.elast_sec_mod_z / 1000), 2))
                elast_sec_mod_y = str(round((Channel_attributes.elast_sec_mod_y / 1000), 2))
                plast_sec_mod_z = str(round((Channel_attributes.plast_sec_mod_z / 1000), 2))
                plast_sec_mod_y = str(round((Channel_attributes.plast_sec_mod_y / 1000), 2))
                if flange_slope != 90:
                    image = VALUES_IMG_TENSIONBOLTED_DF03[0]
                else:
                    image = VALUES_IMG_TENSIONBOLTED_DF03[1]
                It =  str(round((Channel_attributes.It / 10000), 2))
                Iw = str(round((Channel_attributes.Iw / 1000000), 2))
            else:
                Channel_attributes = BBChannel_Properties()
                Channel_attributes.data(designation,material_grade)
                mass = str(round(Channel_attributes.calc_Mass(f_w, f_t, w_h, w_t), 2))
                area = str(round(Channel_attributes.calc_Area(f_w, f_t, w_h, w_t), 2))
                C_y = "N/A"
                mom_inertia_z = str(round(Channel_attributes.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t,plate_thk), 2))
                mom_inertia_y = str(Channel_attributes.calc_MomentOfAreaY(f_w, f_t, w_h, w_t,plate_thk))
                rad_of_gy_z = str(Channel_attributes.calc_RogZ(f_w, f_t, w_h, w_t, plate_thk))
                rad_of_gy_y = str(Channel_attributes.calc_RogY(f_w, f_t, w_h, w_t, plate_thk))
                elast_sec_mod_z = str(Channel_attributes.calc_ElasticModulusZz(f_w, f_t, w_h, w_t,plate_thk))
                elast_sec_mod_y = str(Channel_attributes.calc_ElasticModulusZy(f_w, f_t, w_h, w_t,plate_thk))
                plast_sec_mod_z = str(Channel_attributes.calc_PlasticModulusZpz(f_w, f_t, w_h, w_t,plate_thk))
                plast_sec_mod_y = str(Channel_attributes.calc_PlasticModulusZpy(f_w, f_t, w_h, w_t,plate_thk))
                if flange_slope != 90:
                    image = VALUES_IMG_TENSIONBOLTED_DF03[2]
                else:
                    image = VALUES_IMG_TENSIONBOLTED_DF03[3]
                It = str(Channel_attributes.calc_TorsionConstantIt(f_w, f_t, w_h, w_t))
                Iw = "-"

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

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        section.append(t34)

        t3 = (KEY_SEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        section.append(t3)

        t4 = (KEY_SEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        section.append(t4)

        t15 = ('Label_7', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_8', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        section.append(t16)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_25', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        section.append(t32)

        t14 = ('Label_6', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], Type)
        section.append(t14)

        t29 = (KEY_SOURCE, KEY_DISP_SOURCE, TYPE_TEXTBOX, None, source)
        section.append(t29)

        t28 = (None, None, TYPE_BREAK, None, None)
        section.append(t28)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        section.append(t5)

        t6 = ('Label_1', KEY_DISP_FLANGE_W, TYPE_TEXTBOX, None, f_w)
        section.append(t6)

        t7 = ('Label_2', KEY_DISP_FLANGE_T, TYPE_TEXTBOX, None, f_t)
        section.append(t7)

        t8 = ('Label_3', KEY_DISP_DEPTH, TYPE_TEXTBOX, None, w_h)
        section.append(t8)

        t22 = ('Label_13', KEY_DISP_WEB_T, TYPE_TEXTBOX, None, w_t)
        section.append(t22)

        t23 = ('Label_14', KEY_DISP_FLANGE_S, TYPE_TEXTBOX, None, flange_slope)
        section.append(t23)

        t11 = ('Label_4', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
        section.append(t11)

        t12 = ('Label_5', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
        section.append(t12)

        t12 = ('Label_0', KEY_DISP_DPPLATETHK01, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, plate_thk)
        section.append(t12)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t18 = ('Label_9', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        section.append(t18)

        t19 = ('Label_10', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        section.append(t19)

        # t13 = (None, None, TYPE_BREAK, None, None)
        # section.append(t13)
        #
        #

        # t18 = (None, None, TYPE_ENTER, None, None)
        # section.append(t18)
        #
        # t18 = (None, None, TYPE_ENTER, None, None)
        # section.append(t18)



        # t18 = (None, None, TYPE_ENTER, None, None)
        # section.append(t18)

        # t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        # section.append(t17)

        t20 = ('Label_17', KEY_DISP_Cy, TYPE_TEXTBOX, None, C_y)
        section.append(t20)

        t20 = ('Label_11', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        section.append(t20)

        t21 = ('Label_12', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        section.append(t21)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        section.append(t23)

        t28 = (None, None, TYPE_BREAK, None, None)
        section.append(t28)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, image)
        section.append(t33)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t24 = ('Label_19', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
        section.append(t24)

        t25 = ('Label_20', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
        section.append(t25)

        t26 = ('Label_21', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        section.append(t26)

        t27 = ('Label_22', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        section.append(t27)

        t27 = ('Label_26', KEY_DISP_It, TYPE_TEXTBOX, None, It)
        section.append(t27)

        t27 = ('Label_27', KEY_DISP_Iw, TYPE_TEXTBOX, None, Iw)
        section.append(t27)

        return section


    def get_new_angle_section_properties(self):

        designation = self[0]
        material_grade = self[1]
        l = self[3][KEY_LOCATION]
        section_profile = self[3][KEY_SEC_PROFILE]
        plate_thk = float(self[2])
        Angle_attributes = Angle(designation, material_grade)
        source = str(Angle_attributes.source)
        fu = str(Angle_attributes.fu)
        fy = str(Angle_attributes.fy)
        a = (Angle_attributes.a)
        b = (Angle_attributes.b)
        thickness = (Angle_attributes.thickness)
        root_radius = str(Angle_attributes.root_radius)
        toe_radius = str(Angle_attributes.toe_radius)
        Type = str(Angle_attributes.type)
        m_o_e = "200"
        m_o_r = "76.9"
        p_r = "0.3"
        t_e = "12"
        if section_profile == 'Angles':
            mass = str(round((Angle_attributes.mass),2))
            area = str(round((Angle_attributes.area/100),2))
            Cz = str(round((Angle_attributes.Cz/10),2))
            Cy = str(round((Angle_attributes.Cy/10),2))
            mom_inertia_z = str(round((Angle_attributes.mom_inertia_z)/10000,2))
            mom_inertia_y = str(round((Angle_attributes.mom_inertia_y)/10000,2))
            mom_inertia_u = str(round((Angle_attributes.mom_inertia_u)/10000,2))
            mom_inertia_v = str(round((Angle_attributes.mom_inertia_v)/10000,2))
            rad_of_gy_z = str(round((Angle_attributes.rad_of_gy_z/10),2))
            rad_of_gy_y = str(round((Angle_attributes.rad_of_gy_y/10),2))
            rad_of_gy_u = str(round((Angle_attributes.rad_of_gy_u/10),2))
            rad_of_gy_v = str(round((Angle_attributes.rad_of_gy_v/10),2))
            elast_sec_mod_z = str(round((Angle_attributes.elast_sec_mod_z/1000),2))
            elast_sec_mod_y = str(round((Angle_attributes.elast_sec_mod_y/1000),2))
            plast_sec_mod_z = str(round((Angle_attributes.plast_sec_mod_z/1000),2))
            plast_sec_mod_y = str(round((Angle_attributes.plast_sec_mod_y/1000),2))
            torsional_rigidity = str(round((Angle_attributes.It/10000),2))
            if a == b:
                image = VALUES_IMG_TENSIONBOLTED_DF01[0]
            else:
                image = VALUES_IMG_TENSIONBOLTED_DF02[0]
        else:
            # Angle_attributes = Angle(designation, material_grade)
            if section_profile == "Back to Back Angles":
                print(section_profile, "hjcxhf")
                Angle_attributes = BBAngle_Properties()
                Angle_attributes.data(designation, material_grade)
                if l == "Long Leg":
                    if a == b:
                        image = VALUES_IMG_TENSIONBOLTED_DF01[1]
                    else:
                        image = VALUES_IMG_TENSIONBOLTED_DF02[1]
                    Cz = str(Angle_attributes.calc_Cz(a, b, thickness, l))
                    Cy = "N/A"
                else:
                    if a == b:
                        image = VALUES_IMG_TENSIONBOLTED_DF01[2]
                    else:
                        image = VALUES_IMG_TENSIONBOLTED_DF02[2]
                    Cy = "N/A"
                    Cz = str(Angle_attributes.calc_Cz(a, b, thickness, l))
                mass = str(Angle_attributes.calc_Mass(a, b, thickness, l))
                area = str(Angle_attributes.calc_Area(a, b, thickness, l))

                mom_inertia_z = str(Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l, plate_thk))
                mom_inertia_y = str(Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l, plate_thk))
                mom_inertia_u = str(Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l, plate_thk))
                mom_inertia_v = str(Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l, plate_thk))
                rad_of_gy_z = str(Angle_attributes.calc_RogZ(a, b, thickness, l, plate_thk))
                rad_of_gy_y = str(Angle_attributes.calc_RogY(a, b, thickness, l, plate_thk))
                rad_of_gy_u = str(Angle_attributes.calc_RogY(a, b, thickness, l, plate_thk))
                rad_of_gy_v = str(Angle_attributes.calc_RogZ(a, b, thickness, l, plate_thk))
                elast_sec_mod_z = str(Angle_attributes.calc_ElasticModulusZz(a, b, thickness, l, plate_thk))
                elast_sec_mod_y = str(Angle_attributes.calc_ElasticModulusZy(a, b, thickness, l, plate_thk))
                plast_sec_mod_z = str(Angle_attributes.calc_PlasticModulusZpz(a, b, thickness, l, plate_thk))
                plast_sec_mod_y = str(Angle_attributes.calc_PlasticModulusZpy(a, b, thickness, l, plate_thk))
                torsional_rigidity = str(Angle_attributes.calc_TorsionConstantIt(a, b, thickness, l))
            else:  #  "Star Angles":
                Angle_attributes = SAngle_Properties()
                Angle_attributes.data(designation, material_grade)
                if l == "Long Leg":
                    if a == b:
                        image = VALUES_IMG_TENSIONBOLTED_DF01[3]
                    else:
                        image = VALUES_IMG_TENSIONBOLTED_DF02[3]
                else:
                    if a == b:
                        image = VALUES_IMG_TENSIONBOLTED_DF01[4]
                    else:
                        image = VALUES_IMG_TENSIONBOLTED_DF02[4]
                Cz = "N/A"
                Cy = "N/A"
                mass = str(Angle_attributes.calc_Mass(a, b, thickness, l))
                area = str(Angle_attributes.calc_Area(a, b,thickness, l))

                mom_inertia_z = str(Angle_attributes.calc_MomentOfAreaZ(a, b, thickness, l, plate_thk))
                mom_inertia_y = str(Angle_attributes.calc_MomentOfAreaY(a, b, thickness, l, plate_thk))
                mom_inertia_u = str(Angle_attributes.calc_MomentOfAreaU(a, b, thickness, l, plate_thk))
                mom_inertia_v = str(Angle_attributes.calc_MomentOfAreaV(a, b, thickness, l, plate_thk))
                rad_of_gy_z = str(Angle_attributes.calc_RogZ(a, b, thickness, l, plate_thk))
                rad_of_gy_y = str(Angle_attributes.calc_RogY(a, b, thickness, l, plate_thk))
                rad_of_gy_u = str(Angle_attributes.calc_RogU(a, b, thickness, l, plate_thk))
                rad_of_gy_v = str(Angle_attributes.calc_RogV(a, b, thickness, l, plate_thk))
                elast_sec_mod_z = str(Angle_attributes.calc_ElasticModulusZz(a, b, thickness, l, plate_thk))
                elast_sec_mod_y = str(Angle_attributes.calc_ElasticModulusZy(a, b, thickness, l, plate_thk))
                plast_sec_mod_z = str(Angle_attributes.calc_PlasticModulusZpz(a, b, thickness, l, plate_thk))
                plast_sec_mod_y = str(Angle_attributes.calc_PlasticModulusZpy(a, b, thickness, l, plate_thk))
                torsional_rigidity = str(Angle_attributes.calc_TorsionConstantIt(a, b, thickness, l))

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
            'Label_0': plate_thk,
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
             'Label_23':torsional_rigidity,
            'Label_24':source
            ,KEY_IMAGE:image
        }
        return d

    def get_new_channel_section_properties(self):
        designation = self[0]
        material_grade = self[1]
        # sl = self[2]
        l = self[3][KEY_LOCATION]
        section_profile = self[3][KEY_SEC_PROFILE]
        plate_thk = float(self[2])
        Channel_attributes = Channel(designation, material_grade)
        source = str(Channel_attributes.source)
        Type = str(Channel_attributes.type)
        fu = str(Channel_attributes.fu)
        fy = str(Channel_attributes.fy)
        f_w = (Channel_attributes.flange_width)
        f_t = (Channel_attributes.flange_thickness)
        w_h = (Channel_attributes.depth)
        w_t = (Channel_attributes.web_thickness)
        flange_slope = (Channel_attributes.flange_slope)
        root_radius = str(Channel_attributes.root_radius)
        toe_radius = str(Channel_attributes.toe_radius)
        m_o_e = "200"
        m_o_r = "76.9"
        p_r = "0.3"
        t_e = "12"
        if section_profile == "Channels":
            mass = str(round((Channel_attributes.mass), 2))
            area = str(round((Channel_attributes.area / 100), 2))
            C_y = str(round((Channel_attributes.Cy / 10), 2))
            mom_inertia_z = str(round((Channel_attributes.mom_inertia_z) / 10000, 2))
            mom_inertia_y = str(round((Channel_attributes.mom_inertia_y) / 10000, 2))
            rad_of_gy_z = str(round((Channel_attributes.rad_of_gy_z / 10), 2))
            rad_of_gy_y = str(round((Channel_attributes.rad_of_gy_y / 10), 2))
            elast_sec_mod_z = str(round((Channel_attributes.elast_sec_mod_z / 1000), 2))
            elast_sec_mod_y = str(round((Channel_attributes.elast_sec_mod_y / 1000), 2))
            plast_sec_mod_z = str(round((Channel_attributes.plast_sec_mod_z / 1000), 2))
            plast_sec_mod_y = str(round((Channel_attributes.plast_sec_mod_y / 1000), 2))
            if flange_slope != 90:
                image = VALUES_IMG_TENSIONBOLTED_DF03[0]
            else:
                image = VALUES_IMG_TENSIONBOLTED_DF03[1]
            # if Channel_attributes.It = "N/A":
            #     It = str(Channel_attributes.It )
            # else:
            It = str(round((Channel_attributes.It / 10000), 2))
            Iw = str(round((Channel_attributes.Iw/ 1000000), 2))
        else:
            Channel_attributes = BBChannel_Properties()
            Channel_attributes.data(designation,material_grade)
            mass = str(Channel_attributes.calc_Mass(f_w, f_t, w_h, w_t))
            area = str(Channel_attributes.calc_Area(f_w, f_t, w_h, w_t))
            C_y = "N/A"
            mom_inertia_z = str(Channel_attributes.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t,plate_thk))
            mom_inertia_y = str(Channel_attributes.calc_MomentOfAreaY(f_w, f_t, w_h, w_t,plate_thk))
            rad_of_gy_z = str(Channel_attributes.calc_RogZ(f_w, f_t, w_h, w_t,plate_thk))
            rad_of_gy_y = str(Channel_attributes.calc_RogY(f_w, f_t, w_h, w_t,plate_thk))
            elast_sec_mod_z = str(Channel_attributes.calc_ElasticModulusZz(f_w, f_t, w_h, w_t,plate_thk))
            elast_sec_mod_y = str(Channel_attributes.calc_ElasticModulusZy(f_w, f_t, w_h, w_t,plate_thk))
            plast_sec_mod_z = str(Channel_attributes.calc_PlasticModulusZpz(f_w, f_t, w_h, w_t,plate_thk))
            plast_sec_mod_y = str(Channel_attributes.calc_PlasticModulusZpy(f_w, f_t, w_h, w_t,plate_thk))
            if flange_slope != 90:
                image = VALUES_IMG_TENSIONBOLTED_DF03[2]
            else:
                image = VALUES_IMG_TENSIONBOLTED_DF03[3]
            It = str(Channel_attributes.calc_TorsionConstantIt(f_w, f_t, w_h, w_t))
            Iw = "-"

        d = {
            KEY_SECSIZE_SELECTED: designation,
            KEY_SEC_MATERIAL: material_grade,
            KEY_SEC_FY: fy,
            KEY_SEC_FU: fu,
            'Label_1': str(f_w),
            'Label_2': str(f_t),
            'Label_3': str(w_h),
            'Label_13': str(w_t),
            'Label_14': str(flange_slope),
            'Label_5': str(toe_radius),
            'Label_6': str(Type),
            'Label_4': str(root_radius),
            'Label_0': str(plate_thk),
            'Label_9': str(mass),
            'Label_10': str(area),
            'Label_11': str(mom_inertia_z),
            'Label_12': str(mom_inertia_y),
            'Label_15': str(rad_of_gy_z),
            'Label_16': str(rad_of_gy_y),
            'Label_17': str(C_y),
            'Label_19': str(elast_sec_mod_z),
            'Label_20': str(elast_sec_mod_y),
            'Label_21': str(plast_sec_mod_z),
            'Label_22': str(plast_sec_mod_y),
            'Label_23': str(source),
            'Label_26': str(It),
            'Label_27': str(Iw),
            KEY_IMAGE: image
        }
        return d

    def get_Angle_sec_properties(self):
        if '' in self:
            mass = ''
            area = ''
            Cz = ''
            Cy = ''
            moa_z = ''
            moa_y = ''
            moa_u = ''
            moa_v = ''
            rog_z = ''
            rog_y = ''
            rog_u = ''
            rog_v = ''
            em_z = ''
            em_y = ''
            pm_z = ''
            pm_y = ''
            I_t = ''
            image = ''
        else:
            a = float(self[0])
            b = float(self[1])
            t = float(self[2])
            # plate_thk = float(self[3][KEY_PLATETHK][0])
            plate_thk = float(self[3])

            l = self[4][KEY_LOCATION]
            p = self[4][KEY_SEC_PROFILE]

            if p == "Angles":
                sec_prop = Single_Angle_Properties()
                mass = sec_prop.calc_Mass(a, b, t, l)
                area = sec_prop.calc_Area(a, b, t, l)
                Cz = sec_prop.calc_Cz(a, b, t, l)
                Cy = sec_prop.calc_Cy(a, b, t, l)
                moa_z = sec_prop.calc_MomentOfAreaZ(a, b, t, l)
                moa_y = sec_prop.calc_MomentOfAreaY(a, b, t, l)
                # a = sec_prop.calc_MomentOfAreaYZ(a, b, t, l)
                moa_u = sec_prop.calc_MomentOfAreaU(a, b, t, l)
                moa_v = sec_prop.calc_MomentOfAreaV(a, b, t, l)
                rog_z = sec_prop.calc_RogZ(a, b, t, l)
                rog_y = sec_prop.calc_RogY(a, b, t, l)
                rog_u = sec_prop.calc_RogU(a, b, t, l)
                rog_v = sec_prop.calc_RogV(a, b, t, l)
                em_z = sec_prop.calc_ElasticModulusZz(a, b, t, l)
                em_y = sec_prop.calc_ElasticModulusZy(a, b, t, l)
                pm_z = sec_prop.calc_PlasticModulusZpz(a, b, t, l)
                pm_y = sec_prop.calc_PlasticModulusZpy(a, b, t, l)
                I_t = sec_prop.calc_TorsionConstantIt(a, b, t, l)
                if a == b:
                    image = VALUES_IMG_TENSIONBOLTED_DF01[0]
                else:
                    image = VALUES_IMG_TENSIONBOLTED_DF02[0]

            elif p == "Back to Back Angles":
                sec_prop = BBAngle_Properties()
                mass = sec_prop.calc_Mass(a, b, t, l)
                area = sec_prop.calc_Area(a, b, t, l)
                if l == "Long Leg":
                    Cz = sec_prop.calc_Cz(a, b, t, l)
                    Cy = "N/A"
                else:
                    Cz = sec_prop.calc_Cz(a, b, t, l)
                    Cy = "N/A"
                moa_z = sec_prop.calc_MomentOfAreaZ(a, b, t, l,plate_thk)
                moa_y = sec_prop.calc_MomentOfAreaY(a, b, t, l,plate_thk)
                moa_u = sec_prop.calc_MomentOfAreaY(a, b, t, l,plate_thk)
                moa_v = sec_prop.calc_MomentOfAreaZ(a, b, t, l,plate_thk)
                rog_z = sec_prop.calc_RogZ(a, b, t, l, plate_thk)
                rog_y = sec_prop.calc_RogY(a, b, t, l, plate_thk)
                rog_u = sec_prop.calc_RogY(a, b, t, l, plate_thk)
                rog_v = sec_prop.calc_RogZ(a, b, t, l, plate_thk)
                em_z = sec_prop.calc_ElasticModulusZz(a, b, t, l,plate_thk)
                em_y = sec_prop.calc_ElasticModulusZy(a, b, t, l,plate_thk)
                pm_z = sec_prop.calc_PlasticModulusZpz(a, b, t, l,plate_thk)
                pm_y = sec_prop.calc_PlasticModulusZpy(a, b, t, l,plate_thk)
                I_t = sec_prop.calc_TorsionConstantIt(a, b, t, l)
                if l == "Long Leg":
                    if a == b:
                        image = VALUES_IMG_TENSIONBOLTED_DF01[1]
                    else:
                        image = VALUES_IMG_TENSIONBOLTED_DF02[1]
                else:
                    if a == b:
                        image = VALUES_IMG_TENSIONBOLTED_DF01[2]
                    else:
                        image = VALUES_IMG_TENSIONBOLTED_DF02[2]
            else:
                sec_prop = SAngle_Properties()
                mass = sec_prop.calc_Mass(a, b, t, l)
                area = sec_prop.calc_Area(a, b, t, l)
                Cz = "N/A"
                Cy = "N/A"
                moa_z = sec_prop.calc_MomentOfAreaZ(a, b, t, l,plate_thk)
                moa_y = sec_prop.calc_MomentOfAreaY(a, b, t, l,plate_thk)
                moa_u = sec_prop.calc_MomentOfAreaU(a, b, t, l,plate_thk)
                moa_v = sec_prop.calc_MomentOfAreaV(a, b, t, l,plate_thk)
                rog_z = sec_prop.calc_RogZ(a, b, t, l,plate_thk)
                rog_y = sec_prop.calc_RogY(a, b, t, l,plate_thk)
                rog_u = sec_prop.calc_RogU(a, b, t, l,plate_thk)
                rog_v = sec_prop.calc_RogV(a, b, t, l,plate_thk)
                em_z = sec_prop.calc_ElasticModulusZz(a, b, t, l,plate_thk)
                em_y = sec_prop.calc_ElasticModulusZy(a, b, t, l,plate_thk)
                pm_z = sec_prop.calc_PlasticModulusZpz(a, b, t, l,plate_thk)
                pm_y = sec_prop.calc_PlasticModulusZpy(a, b, t, l,plate_thk)
                I_t = sec_prop.calc_TorsionConstantIt(a, b, t, l)
                if l == "Long Leg":
                    if a == b:
                        image = VALUES_IMG_TENSIONBOLTED_DF01[3]
                    else:
                        image = VALUES_IMG_TENSIONBOLTED_DF02[3]
                else:
                    if a == b:
                        image = VALUES_IMG_TENSIONBOLTED_DF01[4]
                    else:
                        image = VALUES_IMG_TENSIONBOLTED_DF02[4]

        d = {'Label_9': str(mass),
             'Label_10': str(area),
             'Label_7': str(Cz),
             'Label_8': str(Cy),
             'Label_11': str(moa_z),
             'Label_12': str(moa_y),
             'Label_13': str(moa_u),
             'Label_14': str(moa_v),
             'Label_15': str(rog_z),
             'Label_16': str(rog_y),
             'Label_17': str(rog_u),
             'Label_18': str(rog_v),
             'Label_19': str(em_z),
             'Label_20': str(em_y),
             'Label_21': str(pm_z),
             'Label_22': str(pm_y),
             'Label_23': str(I_t)
             ,KEY_IMAGE: image
             }

        return d

    def get_Channel_sec_properties(self):

        if '' in self:
            mass = ''
            area = ''
            C_y = ''
            moa_z = ''
            moa_y = ''

            rog_z = ''
            rog_y = ''

            em_z = ''
            em_y = ''
            pm_z = ''
            pm_y = ''

            It = ''
            Iw = ''
            image =''

        else:
            f_w = float(self[0])
            f_t = float(self[1])
            w_h = float(self[2])
            w_t = float(self[3])
            sl = float(self[4])
            plate_thk = float(self[5][KEY_PLATETHK][0])
            l = self[5][KEY_LOCATION]
            p = self[5][KEY_SEC_PROFILE]

            if p =="Channels":
                sec_prop = Single_Channel_Properties()
                mass = sec_prop.calc_Mass(f_w, f_t, w_h, w_t)
                area = sec_prop.calc_Area(f_w, f_t, w_h, w_t)
                C_y = sec_prop.calc_C_y(f_w, f_t, w_h, w_t)
                moa_z = sec_prop.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t)
                moa_y = sec_prop.calc_MomentOfAreaY(f_w, f_t, w_h, w_t)

                rog_z = sec_prop.calc_RogZ(f_w, f_t, w_h, w_t)
                rog_y = sec_prop.calc_RogY(f_w, f_t, w_h, w_t)

                em_z = sec_prop.calc_ElasticModulusZz(f_w, f_t, w_h, w_t)
                em_y = sec_prop.calc_ElasticModulusZy(f_w, f_t, w_h, w_t)
                pm_z = sec_prop.calc_PlasticModulusZpz(f_w, f_t, w_h, w_t)
                pm_y = sec_prop.calc_PlasticModulusZpy(f_w, f_t, w_h, w_t)
                It = sec_prop.calc_TorsionConstantIt(f_w, f_t, w_h, w_t)
                Iw = 0
                if sl != 90:
                    image = VALUES_IMG_TENSIONBOLTED_DF03[0]
                else:
                    image = VALUES_IMG_TENSIONBOLTED_DF03[1]

            else:
                sec_prop = BBChannel_Properties()
                mass = sec_prop.calc_Mass(f_w, f_t, w_h, w_t)
                area = sec_prop.calc_Area(f_w, f_t, w_h, w_t)
                C_y = "N/A"
                moa_z = sec_prop.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t, plate_thk)
                moa_y = sec_prop.calc_MomentOfAreaY(f_w, f_t, w_h, w_t, plate_thk)

                rog_z = sec_prop.calc_RogZ(f_w, f_t, w_h, w_t,plate_thk)
                rog_y = sec_prop.calc_RogY(f_w, f_t, w_h, w_t,plate_thk)

                em_z = sec_prop.calc_ElasticModulusZz(f_w, f_t, w_h, w_t, plate_thk)
                em_y = sec_prop.calc_ElasticModulusZy(f_w, f_t, w_h, w_t, plate_thk)
                pm_z = sec_prop.calc_PlasticModulusZpz(f_w, f_t, w_h, w_t, plate_thk)
                pm_y = sec_prop.calc_PlasticModulusZpy(f_w, f_t, w_h, w_t, plate_thk)

                It = sec_prop.calc_TorsionConstantIt(f_w, f_t, w_h, w_t)
                Iw = "-"
                if sl != 90:
                    image = VALUES_IMG_TENSIONBOLTED_DF03[2]
                else:
                    image = VALUES_IMG_TENSIONBOLTED_DF03[3]


        d = {'Label_9': str(mass),
             'Label_10': str(area),
             'Label_11': str(moa_z),
             'Label_12': str(moa_y),
             'Label_15': str(rog_z),
             'Label_16': str(rog_y),
             'Label_17': str(C_y),
             'Label_19': str(em_z),
             'Label_20': str(em_y),
             'Label_21': str(pm_z),
             'Label_22': str(pm_y),
             'Label_26': str(It),
             'Label_27': str(Iw),
             KEY_IMAGE : image
             }

        return d

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

            image = ''


        else:
            designation = str(input_dictionary[KEY_SECSIZE][0])
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
                I_sec_attributes = ISection(designation)
                I_sec_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
                fu = str(I_sec_attributes.fu)
                fy = str(I_sec_attributes.fy)
            else:
                table = "Columns"
                I_sec_attributes = ISection(designation)
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
               KEY_DP_BOLT_SLIP_FACTOR: str(0.3),
               KEY_DP_WELD_MATERIAL_G_O: fu,
               KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
               KEY_DP_DETAILING_GAP: '0',
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

    def detailing_values(self, input_dictionary):

        values = {KEY_DP_DETAILING_EDGE_TYPE: 'Sheared or hand flame cut',
                  KEY_DP_DETAILING_GAP:"0",
                  KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No'}

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        detailing = []

        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX,
              ['Sheared or hand flame cut', 'Rolled, machine-flame cut, sawn and planed'],
              values[KEY_DP_DETAILING_EDGE_TYPE])
        detailing.append(t1)

        t2 = (KEY_DP_DETAILING_GAP, KEY_DISP_DP_DETAILING_GAP, TYPE_TEXTBOX, None, values[KEY_DP_DETAILING_GAP])
        detailing.append(t2)

        t3 = (KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES, TYPE_COMBOBOX,
              ['No', 'Yes'], values[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        detailing.append(t3)

        t4 = ("textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION, None)
        detailing.append(t4)

        return detailing


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
        if selected_material in ["Custom","Custom Section"]:
            return True
        else:
            return False

    ######################################
    # Function for individual component calls in 3D view
    ######################################
    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t1 = ('Member', self.call_3DMember)
        components.append(t1)

        t2 = ('Plate', self.call_3DPlate)
        components.append(t2)

        t3 = ('Endplate', self.call_3DEndplate)
        components.append(t3)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Plate", bgcolor)

    def call_3DMember(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Member':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Member", bgcolor)


    def call_3DEndplate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Endplate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Endplate", bgcolor)