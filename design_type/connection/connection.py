from utils.common.component import ISection, Material, Beam
from utils.common.Section_Properties_Calculator import I_sectional_Properties
from design_type.main import Main
from Common import *
import numpy as np


class Connection(Main):

    ########################################
    # Design Preference Functions Start
    ########################################

    def tab_supporting_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "

        if not input_dictionary or input_dictionary[KEY_SUPTNGSEC] == 'Select Section' or input_dictionary[
            KEY_MATERIAL] == 'Select Material':
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
            image= VALUES_IMG_BEAM[0]
        else:
            designation = str(input_dictionary[KEY_SUPTNGSEC])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            I_sec_attributes = ISection(designation, material_grade)
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
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = str(I_sec_attributes.mass)
            area = str(round((I_sec_attributes.area/10**2),2))
            mom_inertia_z = str(round((I_sec_attributes.mom_inertia_z/10**4),2))
            mom_inertia_y = str(round((I_sec_attributes.mom_inertia_y/10**4),2))
            rad_of_gy_z = str(round((I_sec_attributes.rad_of_gy_z/10),2))
            rad_of_gy_y = str(round((I_sec_attributes.rad_of_gy_y/10),2))
            elast_sec_mod_z = str(round((I_sec_attributes.elast_sec_mod_z/10**3),2))
            elast_sec_mod_y = str(round((I_sec_attributes.elast_sec_mod_y/10**3),2))
            plast_sec_mod_z = str(round((I_sec_attributes.plast_sec_mod_z/10**3),2))
            plast_sec_mod_y = str(round((I_sec_attributes.plast_sec_mod_y/10**3),2))
            torsion_const = str(round((I_sec_attributes.It/10**4),2))
            warping_const = str(round((I_sec_attributes.Iw/10**6),2))
            if flange_slope != 90:
                image = VALUES_IMG_BEAM[0]
            else:
                image = VALUES_IMG_BEAM[1]


        if KEY_SUPTNGSEC_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_SUPTNGSEC_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        supporting_section = []
        t1 = (KEY_SUPTNGSEC, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SUPTNGSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supporting_section.append(t34)

        t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        supporting_section.append(t3)

        t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        supporting_section.append(t4)

        t15 = ('Label_9', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        supporting_section.append(t15)

        t16 = ('Label_10', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        supporting_section.append(t16)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        supporting_section.append(t31)

        t32 = ('Label_25', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        supporting_section.append(t32)

        t14 = ('Label_8', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        supporting_section.append(t14)

        t29 = (KEY_SOURCE, KEY_DISP_SOURCE, TYPE_TEXTBOX, None, source)
        supporting_section.append(t29)

        t28 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t28)

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

        t28 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t28)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, image)
        supporting_section.append(t33)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t17)

        t26 = ('Label_19', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        supporting_section.append(t26)

        t27 = ('Label_20', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        supporting_section.append(t27)

        t26 = ('Label_21', KEY_DISP_It, TYPE_TEXTBOX, None, torsion_const)
        supporting_section.append(t26)

        t27 = ('Label_22', KEY_DISP_Iw, TYPE_TEXTBOX, None, warping_const)
        supporting_section.append(t27)

        return supporting_section

    def tab_supported_section(self, input_dictionary):
        """ show properties of the supported section (beam) """

        if not input_dictionary or input_dictionary[KEY_SUPTDSEC] == 'Select Section' or input_dictionary[
            KEY_MATERIAL] == 'Select Material':
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
            designation = str(input_dictionary[KEY_SUPTDSEC])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            I_sec_attributes = ISection(designation)
            table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"

            I_sec_attributes.connect_to_database_update_other_attributes(table, designation,material_grade)
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
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
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

        if KEY_SUPTDSEC_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_SUPTDSEC_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        supporting_section = []
        t1 = (KEY_SUPTDSEC, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SUPTDSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supporting_section.append(t34)

        t3 = (KEY_SUPTDSEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        supporting_section.append(t3)

        t4 = (KEY_SUPTDSEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        supporting_section.append(t4)

        t15 = ('Label_9', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        supporting_section.append(t15)

        t16 = ('Label_10', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        supporting_section.append(t16)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        supporting_section.append(t31)

        t32 = ('Label_25', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        supporting_section.append(t32)

        t14 = ('Label_8', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        supporting_section.append(t14)

        t29 = (KEY_SOURCE, KEY_DISP_SOURCE, TYPE_TEXTBOX, None, source)
        supporting_section.append(t29)

        t28 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t28)

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

        t28 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t28)

        # if flange_slope != 90:
        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None,image)
        # else:
        #     t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, VALUES_IMG_BEAM[1])
        supporting_section.append(t33)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t17)

        t26 = ('Label_19', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        supporting_section.append(t26)

        t27 = ('Label_20', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        supporting_section.append(t27)

        t26 = ('Label_21', KEY_DISP_It, TYPE_TEXTBOX, None, torsion_const)
        supporting_section.append(t26)

        t27 = ('Label_22', KEY_DISP_Iw, TYPE_TEXTBOX, None, warping_const)
        supporting_section.append(t27)

        return supporting_section

    def get_fu_fy_I_section_suptng(self):
        material_grade = self[0]
        designation = self[1].get(KEY_SUPTNGSEC, None)
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
             KEY_SUPTNGSEC_FY: fy}

        return d

    def get_fu_fy_I_section_suptd(self):
        material_grade = self[0]
        designation = self[1].get(KEY_SUPTDSEC, None)
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

        d = {
             KEY_SUPTDSEC_FU: fu,
             KEY_SUPTDSEC_FY: fy}

        return d

    def get_fu_fy(self):
        material_grade = self[0]
        fu_conn = ''
        fy_20 = ''
        fy_20_40 = ''
        fy_40 = ''
        fu = ''
        fy = ''
        if material_grade != "Select Material":
            m_conn = Material(material_grade)
            fu_conn = m_conn.fu
            fy_20 = m_conn.fy_20
            fy_20_40 = m_conn.fy_20_40
            fy_40 = m_conn.fy_40
            fu = m_conn.fu
            fy = m_conn.fy
        else:
            pass

        d = {KEY_CONNECTOR_FU: fu_conn,
             KEY_CONNECTOR_FY_20: fy_20,
             KEY_CONNECTOR_FY_20_40: fy_20_40,
             KEY_CONNECTOR_FY_40: fy_40,
             KEY_BASE_PLATE_FU: fu,
             KEY_BASE_PLATE_FY: fy,
             KEY_ST_KEY_FU: fu,
             KEY_ST_KEY_FY: fy,
             }

        return d

    def get_bolt_tension_type_for_prying(self):
        bolt_type = self[0]

        if bolt_type == "Bearing Bolt":
            bolt_tension_type = 'Non pre-tensioned'
        else:
            bolt_tension_type = 'Pre-tensioned'

        return bolt_tension_type

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

        t3 = (KEY_CONNECTOR_MATERIAL, KEY_CONNECTOR_FU, KEY_CONNECTOR_FY)
        fu_fy_list.append(t3)

        return fu_fy_list

    def refresh_input_dock(self):

        add_buttons = []

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, KEY_CONN, VALUES_CONN_1, "Columns")
        add_buttons.append(t1)

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, KEY_CONN, VALUES_CONN_2, "Beams")
        add_buttons.append(t1)

        t2 = (KEY_DISP_BEAMSEC, KEY_SUPTDSEC, TYPE_COMBOBOX, KEY_SUPTDSEC, None, None, "Beams")
        add_buttons.append(t2)

        return add_buttons

    ########################################
    # Design Preference Functions End
    ########################################

    def func_for_validation(self, design_dictionary):
        print('input dictionary')
        print(design_dictionary)
        all_errors = []
        self.design_status = False
        flag1 = False
        flag2=True
        option_list = self.input_values(self)
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
                if design_dictionary[option[0]] == 'Select Section' or design_dictionary[option[0]] == 'Select Grade':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) == 0:
            if KEY_CONN in design_dictionary and design_dictionary[KEY_CONN] == VALUES_CONN_2[0]:
                primary = design_dictionary[KEY_SUPTNGSEC]
                secondary = design_dictionary[KEY_SUPTDSEC]
                conn = sqlite3.connect(PATH_TO_DATABASE)
                cursor = conn.execute("SELECT D FROM BEAMS WHERE Designation = ( ? ) ", (primary,))
                lst = []
                rows = cursor.fetchall()
                for row in rows:
                    lst.append(row)
                p_val = lst[0][0]
                cursor2 = conn.execute("SELECT D FROM BEAMS WHERE Designation = ( ? )", (secondary,))
                lst1 = []
                rows1 = cursor2.fetchall()
                for row1 in rows1:
                    lst1.append(row1)
                s_val = lst1[0][0]
                if p_val <= s_val:
                    error = "Secondary beam depth is higher than clear depth of primary beam web " + "\n" + "(No provision in Osdag till now)"
                    all_errors.append(error)
                else:
                    flag1 = True

            elif KEY_CONN in design_dictionary and design_dictionary[KEY_CONN] == VALUES_CONN_1[1]:
                primary = design_dictionary[KEY_SUPTNGSEC]
                secondary = design_dictionary[KEY_SUPTDSEC]
                conn = sqlite3.connect(PATH_TO_DATABASE)
                cursor = conn.execute("SELECT D, T, R1, R2 FROM COLUMNS WHERE Designation = ( ? ) ", (primary,))
                p_beam_details = cursor.fetchone()
                p_val = p_beam_details[0] - 2*p_beam_details[1] - p_beam_details[2] - p_beam_details[3]
                cursor2 = conn.execute("SELECT B FROM BEAMS WHERE Designation = ( ? )", (secondary,))

                s_beam_details = cursor2.fetchone()
                s_val = s_beam_details[0]
                #print(p_val,s_val)
                if p_val <= s_val:
                    error = "Secondary beam width is higher than clear depth of primary column web " + "\n" + "(No provision in Osdag till now)"
                    all_errors.append(error)
                else:
                    flag1 = True
            else:
                flag1 = True
            if design_dictionary[KEY_MODULE] == KEY_DISP_FINPLATE:
                selected_plate_thk = list(np.float_(design_dictionary[KEY_PLATETHK]))
                supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC],material_grade=design_dictionary[KEY_MATERIAL])
                available_plates = [i for i in selected_plate_thk if i >= supported_section.web_thickness]
                if not available_plates:
                    error = "Plate thickness should be greater than suppported section web thicknesss."
                    all_errors.append(error)
                    flag2 = False
                else:
                    flag2=True
            # if str(design_dictionary[KEY_AXIAL]).isdecimal() and str(design_dictionary[KEY_SHEAR]).isdecimal() \
            #         and str(design_dictionary[KEY_MOMENT]).isdecimal():
            #     flag2 = True
            # else:
            #     flag2 = False
            if flag1 and flag2:
                self.set_input_values(self, design_dictionary)
            else:
                return all_errors

        else:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
            return all_errors

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

    def call_3DColumn(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Column':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Column", bgcolor)

    def call_3DBeam(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Beam':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Beam", bgcolor)

    def new_material(self):

        selected_material = self[0]
        if selected_material == "Custom":
            return True
        else:
            return False

    def save_design(self):
        """ """
        if self.module == KEY_DISP_BASE_PLATE:  # base plate module
            pass
        else:
            if self.supporting_section.flange_slope != 90:
                section1 = "Slope_Beam"
            else:
                section1 = "Parallel_Beam"
            self.report_supporting = {KEY_DISP_SEC_PROFILE: section1,
                                      KEY_DISP_SUPTNGSEC: self.supporting_section.designation,
                                      KEY_DISP_MATERIAL: self.supporting_section.material,
                                      KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.supporting_section.fu,
                                      KEY_DISP_YIELD_STRENGTH_REPORT: self.supporting_section.fy,
                                      KEY_REPORT_MASS: self.supporting_section.mass,
                                      KEY_REPORT_AREA: round(self.supporting_section.area * 1e-2, 2),
                                  KEY_REPORT_DEPTH: self.supporting_section.depth,
                                  KEY_REPORT_WIDTH: self.supporting_section.flange_width,
                                  KEY_REPORT_WEB_THK: self.supporting_section.web_thickness,
                                  KEY_REPORT_FLANGE_THK: self.supporting_section.flange_thickness,
                                  KEY_DISP_FLANGE_S_REPORT: self.supporting_section.flange_slope,
                                  KEY_REPORT_R1: self.supporting_section.root_radius,
                                  KEY_REPORT_R2: self.supporting_section.toe_radius,
                                  KEY_REPORT_IZ: round(self.supporting_section.mom_inertia_z * 1e-4, 2),
                                  KEY_REPORT_IY: round(self.supporting_section.mom_inertia_y * 1e-4, 2),
                                  KEY_REPORT_RZ: round(self.supporting_section.rad_of_gy_z * 1e-1, 2),
                                  KEY_REPORT_RY: round(self.supporting_section.rad_of_gy_y * 1e-1, 2),
                                  KEY_REPORT_ZEZ: round(self.supporting_section.elast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZEY: round(self.supporting_section.elast_sec_mod_y * 1e-3, 2),
                                  KEY_REPORT_ZPZ: round(self.supporting_section.plast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZPY: round(self.supporting_section.plast_sec_mod_y * 1e-3, 2)}

            if self.supported_section.flange_slope != 90:
                section2 = "Slope_Beam"
            else:
                section2 = "Parallel_Beam"
            self.report_supported = {
                KEY_DISP_SEC_PROFILE: section2,  # Image shall be saved with this name.png in resource files
                KEY_DISP_SUPTDSEC: self.supported_section.designation,
                KEY_DISP_MATERIAL: self.supported_section.material,
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.supported_section.fu,
                                 KEY_DISP_YIELD_STRENGTH_REPORT: self.supported_section.fy,
                                 KEY_REPORT_MASS: self.supported_section.mass,
                                  KEY_REPORT_AREA: round(self.supported_section.area * 1e-2, 2),
                                  KEY_REPORT_DEPTH: self.supported_section.depth,
                                  KEY_REPORT_WIDTH: self.supported_section.flange_width,
                                  KEY_REPORT_WEB_THK: self.supported_section.web_thickness,
                                  KEY_REPORT_FLANGE_THK: self.supported_section.flange_thickness,
                                  KEY_DISP_FLANGE_S_REPORT: self.supported_section.flange_slope,
                                  KEY_REPORT_R1: self.supported_section.root_radius,
                                  KEY_REPORT_R2: self.supported_section.toe_radius,
                                  KEY_REPORT_IZ: round(self.supported_section.mom_inertia_z * 1e-4, 2),
                                  KEY_REPORT_IY: round(self.supported_section.mom_inertia_y * 1e-4, 2),
                                  KEY_REPORT_RZ: round(self.supported_section.rad_of_gy_z * 1e-1, 2),
                                  KEY_REPORT_RY: round(self.supported_section.rad_of_gy_y * 1e-1, 2),
                                  KEY_REPORT_ZEZ: round(self.supported_section.elast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZEY: round(self.supported_section.elast_sec_mod_y * 1e-3, 2),
                                  KEY_REPORT_ZPZ: round(self.supported_section.plast_sec_mod_z * 1e-3, 2),
                                  KEY_REPORT_ZPY: round(self.supported_section.plast_sec_mod_y * 1e-3, 2)}

            if self.module == KEY_DISP_FINPLATE or self.module == KEY_DISP_ENDPLATE:
                self.report_input = \
                    {KEY_MAIN_MODULE: self.mainmodule,
                     KEY_MODULE: self.module,
                     KEY_CONN: self.connectivity,
                     KEY_DISP_SHEAR: self.load.shear_force,
                     KEY_DISP_AXIAL: self.load.axial_force,
                     KEY_DISP_SUPTNGSEC_REPORT: "TITLE",
                     "Supporting Section Details": self.report_supporting,
                     KEY_DISP_SUPTDSEC_REPORT: "TITLE",
                     "Supported Section Details": self.report_supported,

                     "Bolt Details - Input and Design Preference": "TITLE",
                     KEY_DISP_D: str(list(np.int_(self.bolt.bolt_diameter))),
                     KEY_DISP_GRD: str(self.bolt.bolt_grade),
                     KEY_DISP_TYP: self.bolt.bolt_type,
                     KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
                     KEY_DISP_BOLT_PRE_TENSIONING: self.bolt.bolt_tensioning,
                     KEY_DISP_DP_BOLT_SLIP_FACTOR_REPORT: self.bolt.mu_f,

                     "Detailing - Design Preference": "TITLE",
                     KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
                     KEY_DISP_GAP: self.plate.gap,
                     KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM: self.bolt.corrosive_influences,

                     "Plate Details - Input and Design Preference": "TITLE",
                     KEY_DISP_PLATETHK: str(list(np.int_(self.plate.thickness))),
                     KEY_DISP_MATERIAL: self.plate.material,
                     KEY_DISP_FU: self.plate.fu,
                     KEY_DISP_FY: self.plate.fy,

                     "Weld Details - Input and Design Preference": "TITLE",
                     KEY_DISP_DP_WELD_TYPE: "Fillet",
                     KEY_DISP_DP_WELD_FAB: self.weld.fabrication,
                     KEY_DISP_DP_WELD_MATERIAL_G_O: self.weld.fu}


if __name__ == "__main__":
    connection = Connection()
    connection.test()
    connection.design()
