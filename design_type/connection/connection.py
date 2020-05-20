from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column
from utils.common.load import Load
from utils.common.component import Section,I_sectional_Properties, Material
from main import Main
from Common import *


class Connection(Main):

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
