from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column, ISection
from utils.common.Section_Properties_Calculator import Single_Angle_Properties
from Common import *
from utils.common.load import Load
from utils.common.material import Material
from utils.common.common_calculation import *
from utils.common.is800_2007 import IS800_2007


class ShearConnection(Connection):
    def __init__(self):
        super(ShearConnection, self).__init__()

    ############################
    # Design Preferences functions
    ############################

    def tab_angle_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "
        "In design preference, it shows other properties of section used "
        if not input_dictionary or input_dictionary[KEY_ANGLE_LIST] == [] or \
                input_dictionary[KEY_MATERIAL] == 'Select Material':
            designation = ''
            material_grade = ''
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
            torsion_const=''
            source = 'Custom'
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            image = ''
        else:
            designation = str(input_dictionary[KEY_ANGLE_LIST][0])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            Angle_attributes = Angle(designation,material_grade)
            Angle_attributes.connect_to_database_update_other_attributes(designation, material_grade)
            source = str(Angle_attributes.source)
            fu = str(Angle_attributes.fu)
            fy = str(Angle_attributes.fy)
            a = str(Angle_attributes.a)
            b = str(Angle_attributes.b)
            thickness = str(Angle_attributes.thickness)
            root_radius = str(Angle_attributes.root_radius)
            toe_radius = str(Angle_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
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
            torsion_const = str(round((Angle_attributes.It / 10000), 2))

            if a == b:
                image = VALUES_IMG_TENSIONBOLTED_DF01[0]
            else:
                image = VALUES_IMG_TENSIONBOLTED_DF02[0]


        if KEY_CONNECTOR_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_CONNECTOR_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        section = []

        if input_dictionary:
            designation_list = input_dictionary[KEY_ANGLE_LIST]
        else:
            designation_list = []

        t0 = (KEY_ANGLE_LIST, KEY_DISP_DESIGNATION, TYPE_COMBOBOX, designation_list, designation)
        section.append(t0)

        t1 = (KEY_ANGLE_SELECTED, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_CONNECTOR_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        section.append(t34)

        t3 = (KEY_CONNECTOR_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        section.append(t3)

        t4 = (KEY_CONNECTOR_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        section.append(t4)

        t15 = ('Label_27', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_28', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        section.append(t16)

        t31 = ('Label_25', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_26', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        section.append(t32)

        t14 = ('Label_6', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
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

        t27 = ('Label_23', KEY_DISP_It, TYPE_TEXTBOX, None, torsion_const)
        section.append(t27)

        return section

    def get_Angle_sec_properties(self):
        # print(self,profile,"shxv")
        # print(self, "shxv")
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
            l = None

            sec_prop = Single_Angle_Properties()
            mass = sec_prop.calc_Mass(a,b,t,l)
            area = sec_prop.calc_Area(a,b,t,l)
            Cz = sec_prop.calc_Cz(a,b,t,l)
            Cy = sec_prop.calc_Cy(a,b,t,l)
            moa_z = sec_prop.calc_MomentOfAreaZ(a,b,t,l)
            moa_y = sec_prop.calc_MomentOfAreaY(a,b,t,l)
            moa_u = sec_prop.calc_MomentOfAreaU(a,b,t,l)
            moa_v = sec_prop.calc_MomentOfAreaV(a,b,t,l)
            rog_z = sec_prop.calc_RogZ(a,b,t,l)
            rog_y = sec_prop.calc_RogY(a,b,t,l)
            rog_u = sec_prop.calc_RogU(a,b,t,l)
            rog_v = sec_prop.calc_RogV(a,b,t,l)
            em_z = sec_prop.calc_ElasticModulusZz(a,b,t,l)
            em_y = sec_prop.calc_ElasticModulusZy(a,b,t,l)
            pm_z = sec_prop.calc_PlasticModulusZpz(a,b,t,l)
            pm_y = sec_prop.calc_PlasticModulusZpy(a,b,t,l)
            I_t = sec_prop.calc_TorsionConstantIt(a,b,t,l)
            if a == b:
                image = VALUES_IMG_TENSIONBOLTED_DF01[0]
            else:
                image = VALUES_IMG_TENSIONBOLTED_DF02[0]



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
             'Label_23': str(I_t),
             KEY_IMAGE: image
             }

        return d

    def get_new_angle_section_properties(self):

        designation = self[0]
        material_grade = self[1]


        Angle_attributes = Angle(designation, material_grade)
        Angle_attributes.connect_to_database_update_other_attributes(designation, material_grade)
        source = str(Angle_attributes.source)
        Type= str(Angle_attributes.type)
        fu = str(Angle_attributes.fu)
        fy = str(Angle_attributes.fy)
        a = str(Angle_attributes.leg_a_length)
        b = str(Angle_attributes.leg_b_length)
        thickness = str(Angle_attributes.thickness)
        root_radius = str(Angle_attributes.root_radius)
        toe_radius = str(Angle_attributes.toe_radius)

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
        torsion_const = str(round((Angle_attributes.It / 10000), 2))

        if a == b:
            image = VALUES_IMG_TENSIONBOLTED_DF01[0]
        else:
            image = VALUES_IMG_TENSIONBOLTED_DF02[0]

        d = {
            KEY_ANGLE_SELECTED:designation,
            KEY_CONNECTOR_MATERIAL: material_grade,
            KEY_CONNECTOR_FY:fy,
            KEY_CONNECTOR_FU:fu,
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
            'Label_23':torsion_const,
            'Label_24':source,
            KEY_IMAGE: image

        }
        return d


    def get_values_for_design_pref(self, key, design_dictionary):

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            fu = Material(design_dictionary[KEY_MATERIAL],41).fu
        else:
            fu = ''

        val = {KEY_DP_BOLT_TYPE: "Pretensioned",
               KEY_DP_BOLT_HOLE_TYPE: "Standard",
               KEY_DP_BOLT_SLIP_FACTOR: str(0.3),
               KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
               KEY_DP_DETAILING_GAP: '10',
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No',
               KEY_DP_DESIGN_METHOD: "Limit State Design",
               KEY_CONNECTOR_MATERIAL: str(design_dictionary[KEY_MATERIAL])
               }[key]

        return val

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

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t2 = (KEY_PLATETHK, self.pltthk_customized)
        list1.append(t2)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        return list1

    def fn_conn_suptngsec_lbl(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        elif conn in VALUES_CONN_2:
            return KEY_DISP_PRIBM
        else:
            return ''

    def fn_conn_suptdsec_lbl(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        elif conn in VALUES_CONN_2:
            return KEY_DISP_SECBM
        else:
            return ''

    def fn_conn_suptngsec(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return connectdb("Columns")
        elif conn in VALUES_CONN_2:
            return connectdb("Beams")
        else:
            return []

    def fn_conn_suptdsec(self):

        conn = self[0]
        if conn in VALUES_CONN:
            return connectdb("Beams")
        else:
            return []

    def fn_conn_image(self):

        conn = self[0]
        if conn == VALUES_CONN[0]:
            return './ResourceFiles/images/fin_cf_bw.png'
        elif conn == VALUES_CONN[1]:
            return './ResourceFiles/images/fin_cw_bw.png'
        elif conn in VALUES_CONN_2:
            return './ResourceFiles/images/fin_beam_beam.png'
        else:
            return ''

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_CONN], KEY_SUPTNGSEC, TYPE_LABEL, self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = ([KEY_CONN], KEY_SUPTNGSEC, TYPE_COMBOBOX, self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = ([KEY_CONN], KEY_SUPTDSEC, TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = ([KEY_CONN], KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = ([KEY_CONN], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        # t6 = ([KEY_TYP], KEY_OUT_BOLT_BEARING, TYPE_OUT_DOCK, self.out_bolt_bearing)
        # lst.append(t6)
        #
        t7 = ([KEY_TYP], KEY_OUT_BOLT_BEARING, TYPE_OUT_LABEL, self.out_bolt_bearing)
        # lst.append(t7)

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        return lst

    def out_bolt_bearing(self):

        bolt_type = self[0]
        if bolt_type != TYP_BEARING:
            return True
        else:
            return False

    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from Column and Beams table.
        """

        # @author Arsil Zunzunia
        global logger
        red_list = red_list_function()
        if self.supported_section.designation in red_list or self.supporting_section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def set_input_values(self, design_dictionary):
        self.mainmodule = "Shear Connection"
        self.connectivity = design_dictionary[KEY_CONN]
        self.material = Material(material_grade=design_dictionary[KEY_MATERIAL])

        if self.connectivity in VALUES_CONN_1:
            self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_SUPTNGSEC_MATERIAL])
        else:
            self.supporting_section = Beam(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_SUPTNGSEC_MATERIAL])

        self.supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC], material_grade=design_dictionary[KEY_SUPTDSEC_MATERIAL])
        # self.supported_section.notch_ht = round_up(self.supporting_section.flange_thickness * 2, 5)
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                         bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])

        self.load = Load(shear_force=design_dictionary[KEY_SHEAR], axial_force=design_dictionary.get(KEY_AXIAL, ""))

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.type)
        self.supported_section.notch_ht = round_up(
            max(self.supporting_section.flange_thickness + self.supporting_section.root_radius + 10,
                self.supported_section.flange_thickness + self.supported_section.root_radius + 10), 5)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.type == "Rolled":
                self.supported_section.web_height = self.supported_section.depth
            else:
                self.supported_section.web_height = self.supported_section.depth - (
                            2 * self.supported_section.flange_thickness)  # -(2*self.supported_section.root_radius)
        else:

            self.supported_section.web_height = self.supported_section.depth - self.supported_section.notch_ht

        A_g = self.supported_section.web_height * self.supported_section.web_thickness
        # 0.6 is multiplied for shear yielding capacity to keep the section in low shear
        self.supported_section.shear_yielding_capacity = IS800_2007.cl_8_4_design_shear_strength(A_g,
                                                                                                       self.supported_section.fy)
        self.supported_section.tension_yielding_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g,
                                                                                                       self.supported_section.fy)

        print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
              self.supported_section.tension_yielding_capacity, self.load.axial_force)

        self.supporting_section.tension_yielding_capacity = IS800_2007.cl_6_2_tension_yielding_strength(self.supporting_section.area,
                                                                                                       self.supporting_section.fy)