from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column, Section
from Common import *
from utils.common.load import Load
from utils.common.material import Material
from utils.common.common_calculation import *



class ShearConnection(Connection):
    def __init__(self):
        super(ShearConnection, self).__init__()

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

        return lst

    def set_input_values(self, design_dictionary):
        self.mainmodule = "Shear Connection"
        self.connectivity = design_dictionary[KEY_CONN]
        self.material = Material(material_grade=design_dictionary[KEY_MATERIAL])

        if self.connectivity in VALUES_CONN_1:
            self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_MATERIAL])
        else:
            self.supporting_section = Beam(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_MATERIAL])

        self.supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC], material_grade=design_dictionary[KEY_MATERIAL])
        self.supported_section.notch_ht = round_up(self.supporting_section.flange_thickness * 2, 5)
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         material_grade=design_dictionary[KEY_MATERIAL],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                         bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])

        self.load = Load(shear_force=design_dictionary[KEY_SHEAR], axial_force=design_dictionary.get(KEY_AXIAL, None))

    def tab_supporting_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "

        if not input_dictionary or input_dictionary[KEY_DISP_SUPTNGSEC] == 'Select Section' or input_dictionary[
            KEY_MATERIAL] == 'Select Material':
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
            designation = str(input_dictionary[KEY_SUPTNGSEC])
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
        t34 = (KEY_SUPTNGSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supporting_section.append(t34)

        t3 = ('Lable_26', KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None, fu)
        supporting_section.append(t3)

        t4 = ('Lable_27', KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None, fy)
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

    def tab_supported_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "

        if not input_dictionary or input_dictionary[KEY_SUPTDSEC] == 'Select Section' or input_dictionary[
            KEY_MATERIAL] == 'Select Material':
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
            designation = str(input_dictionary[KEY_SUPTDSEC])
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
        t34 = (KEY_SUPTDSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supporting_section.append(t34)

        t3 = ('Lable_26', KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None, fu)
        supporting_section.append(t3)

        t4 = ('Lable_27', KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None, fy)
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