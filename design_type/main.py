from Common import *
from utils.common.load import Load
from utils.common.component import *
from utils.common.Section_Properties_Calculator import *

class Main():

    def __init__(self):
        pass

    #########################################
    # Design Preferences Functions Start
    #########################################

    def bolt_values(self, input_dictionary):

        if not input_dictionary or input_dictionary[KEY_TYP] == 'Bearing Bolt':
            bolt_tension_type = 'Non pre-tensioned'
        else:
            bolt_tension_type = 'Pre-tensioned'

        if KEY_DP_BOLT_TYPE in input_dictionary.keys():
            bolt_tension_type = input_dictionary[KEY_DP_BOLT_TYPE]

        values = {KEY_DP_BOLT_TYPE: bolt_tension_type, KEY_DP_BOLT_HOLE_TYPE: 'Standard',
                  KEY_DP_BOLT_SLIP_FACTOR: '0.3'}

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        bolt = []

        t1 = (KEY_DP_BOLT_TYPE, KEY_DISP_TYP, TYPE_COMBOBOX, ['Pre-tensioned', 'Non pre-tensioned'], values[KEY_DP_BOLT_TYPE])
        bolt.append(t1)

        t2 = (KEY_DP_BOLT_HOLE_TYPE, KEY_DISP_DP_BOLT_HOLE_TYPE, TYPE_COMBOBOX, ['Standard', 'Over-sized'], values[KEY_DP_BOLT_HOLE_TYPE])
        bolt.append(t2)

        t4 = (None, None, TYPE_ENTER, None, None)
        bolt.append(t4)

        t5 = (None, KEY_DISP_DP_BOLT_DESIGN_PARA, TYPE_TITLE, None, None)
        bolt.append(t5)

        t6 = (KEY_DP_BOLT_SLIP_FACTOR, KEY_DISP_DP_BOLT_SLIP_FACTOR, TYPE_COMBOBOX,
              ['0.2', '0.5', '0.1', '0.25', '0.3', '0.33', '0.48', '0.52', '0.55'], values[KEY_DP_BOLT_SLIP_FACTOR])
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

        values = {KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP, KEY_DP_WELD_MATERIAL_G_O: ''}

        if not input_dictionary or input_dictionary[KEY_MATERIAL] == 'Select Material':
            pass
        else:
            values[KEY_DP_WELD_MATERIAL_G_O] = Material(input_dictionary[KEY_MATERIAL]).fu
            # material_g_o = Material(input_dictionary[KEY_MATERIAL]).fu

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        weld = []

        t1 = (KEY_DP_WELD_FAB, KEY_DISP_DP_WELD_FAB, TYPE_COMBOBOX, KEY_DP_WELD_FAB_VALUES, values[KEY_DP_WELD_FAB])
        weld.append(t1)

        t2 = (KEY_DP_WELD_MATERIAL_G_O, KEY_DISP_DP_WELD_MATERIAL_G_O, TYPE_TEXTBOX, None, values[KEY_DP_WELD_MATERIAL_G_O])
        weld.append(t2)

        t3 = ("textBrowser", "", TYPE_TEXT_BROWSER, WELD_DESCRIPTION, None)
        weld.append(t3)

        return weld

    def detailing_values(self, input_dictionary):

        values = {KEY_DP_DETAILING_EDGE_TYPE: 'Sheared or hand flame cut',
                  KEY_DP_DETAILING_GAP: '10',
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

    def design_values(self, input_dictionary):

        values = {KEY_DP_DESIGN_METHOD: 'Limit State Design'}

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        design = []

        t1 = (KEY_DP_DESIGN_METHOD, KEY_DISP_DP_DESIGN_METHOD, TYPE_COMBOBOX,
              ['Limit State Design', 'Limit State (capacity based) Design', 'Working Stress Design'],
              values[KEY_DP_DESIGN_METHOD])
        design.append(t1)

        return design

    def plate_connector_values(self, input_dictionary):

        if not input_dictionary or input_dictionary[KEY_MATERIAL] == 'Select Material':
            material_grade = ''
            fu = ''
            fy_20 = ''
            fy_20_40 = ''
            fy_40 = ''
        else:
            material_grade = input_dictionary[KEY_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy_20 = material_attributes.fy_20
            fy_20_40 = material_attributes.fy_20_40
            fy_40 = material_attributes.fy_40

        if KEY_CONNECTOR_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_CONNECTOR_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy_20 = material_attributes.fy_20
            fy_20_40 = material_attributes.fy_20_40
            fy_40 = material_attributes.fy_40

        connector = []

        material = connectdb("Material", call_type="popup")
        t1 = (KEY_CONNECTOR_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        connector.append(t1)

        t2 = (KEY_CONNECTOR_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        connector.append(t2)

        t3 = (KEY_CONNECTOR_FY_20, KEY_DISP_FY_20, TYPE_TEXTBOX, None, fy_20)
        connector.append(t3)

        t3 = (KEY_CONNECTOR_FY_20_40, KEY_DISP_FY_20_40, TYPE_TEXTBOX, None, fy_20_40)
        connector.append(t3)

        t3 = (KEY_CONNECTOR_FY_40, KEY_DISP_FY_40, TYPE_TEXTBOX, None, fy_40)
        connector.append(t3)

        return connector


    # def get_def_I_sec_properties(self):
    #
    #     if 'default' in self:
    #         mass = ''
    #         area = ''
    #         moa_z = ''
    #         moa_y = ''
    #         rog_z = ''
    #         rog_y = ''
    #         em_z = ''
    #         em_y = ''
    #         pm_z = ''
    #         pm_y = ''
    #         I_t = ''
    #         I_w = ''
    #         image = VALUES_IMG_BEAM[0]
    #     d = {'Label_11': str(mass),
    #          'Label_12': str(area),
    #          'Label_13': str(moa_z),
    #          'Label_14': str(moa_y),
    #          'Label_15': str(rog_z),
    #          'Label_16': str(rog_y),
    #          'Label_17': str(em_z),
    #          'Label_18': str(em_y),
    #          'Label_19': str(pm_z),
    #          'Label_20': str(pm_y),
    #          'Label_21': str(I_t),
    #          'Label_22': str(I_w),
    #          KEY_IMAGE: image
    #          }
    #
    #     return d


    def get_I_sec_properties(self):

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
            I_t = ''
            I_w = ''
            image = ''

        else:
            D = float(self[0])
            B = float(self[1])
            t_w = float(self[2])
            t_f = float(self[3])
            sl = float(self[4])

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
            I_t = sec_prop.calc_TorsionConstantIt(D,B,t_w,t_f)
            I_w = sec_prop.calc_WarpingConstantIw(D,B,t_w, t_f)
            if sl != 90:
                image = VALUES_IMG_BEAM[0]
            else:
                image = VALUES_IMG_BEAM[1]

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
             'Label_21': str(I_t),
             'Label_22': str(I_w),
             KEY_IMAGE: image
            }

        return d

    def get_SHS_RHS_properties(self):

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
            I_t = ''
            I_w = ''
            image = ''

        else:
            D = float(self[0])
            B = float(self[1])
            t_w = float(self[2])
            t_f = float(self[2])
            sl = 0.0

            sec_prop = SHS_RHS_Properties()
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
            I_t = sec_prop.calc_TorsionConstantIt(D,B,t_w,t_f)
            I_w = sec_prop.calc_WarpingConstantIw(D,B,t_w, t_f)
            if D == B:
                image = VALUES_IMG_HOLLOWSECTION[0]
            else:
                image = VALUES_IMG_HOLLOWSECTION[1]

        d = {'Label_HS_11': str(mass),
             'Label_HS_12': str(area),
             'Label_HS_13': str(moa_z),
             'Label_HS_14': str(moa_y),
             'Label_HS_15': str(rog_z),
             'Label_HS_16': str(rog_y),
             'Label_HS_17': str(em_z),
             'Label_HS_18': str(em_y),
             'Label_HS_19': str(pm_z),
             'Label_HS_20': str(pm_y),
             'Label_HS_21': str(I_t),
             'Label_HS_22': str(I_w),
             KEY_IMAGE: image
            }

        return d

    def get_CHS_properties(self):

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
            I_t = ''
            I_w = ''
            image = ''

        else:
            D = float(self[1])
            B = float(self[1])
            t_w = float(self[2])
            t_f = float(self[2])
            sl = 0.0

            sec_prop = CHS_Properties()
            mass = sec_prop.calc_Mass(D, B, t_w, t_f)
            area = sec_prop.calc_Area(D, B, t_w, t_f)
            internal_vol = 0.0
            moa_z = sec_prop.calc_MomentOfAreaZ(D, B, t_w, t_f)
            moa_y = sec_prop.calc_MomentOfAreaY(D, B, t_w, t_f)
            rog_z = sec_prop.calc_RogZ(D, B, t_w, t_f)
            rog_y = sec_prop.calc_RogY(D, B, t_w, t_f)
            em_z = sec_prop.calc_ElasticModulusZz(D, B, t_w, t_f)
            em_y = sec_prop.calc_ElasticModulusZy(D, B, t_w, t_f)
            pm_z = sec_prop.calc_PlasticModulusZpz(D, B, t_w, t_f)
            pm_y = sec_prop.calc_PlasticModulusZpy(D, B, t_w, t_f)
            I_t = sec_prop.calc_TorsionConstantIt(D,B,t_w,t_f)
            I_w = sec_prop.calc_WarpingConstantIw(D,B,t_w, t_f)
            image = VALUES_IMG_HOLLOWSECTION[2]

        d = {'Label_CHS_11': str(mass),
             'Label_CHS_12': str(area),
             'Label_CHS_13': str(internal_vol),
             'Label_HS_14': str(moa_z),
             # 'Label_HS_14': str(moa_y),
             'Label_HS_15': str(rog_z),
             # 'Label_16': str(rog_y),
             'Label_HS_16': str(em_z),
             # 'Label_18': str(em_y),
             # 'Label_19': str(pm_z),
             # 'Label_20': str(pm_y),
             'Label_21': str(I_t),
             'Label_22': str(I_w),
             KEY_IMAGE: image
            }

        return d

    def change_source(self):

        designation = self[0]
        source = 'Custom'
        if designation in connectdb("Columns", call_type="dropdown"):
            source = get_source("Columns", designation)
        elif designation in connectdb("Beams", call_type="dropdown"):
            source = get_source("Beams", designation)
        elif designation in connectdb("Angles", call_type="dropdown"):
            source = get_source("Angles", designation)
        elif designation in connectdb("Channels", call_type="dropdown"):
            source = get_source("Channels", designation)

        d = {KEY_SOURCE: str(source)}
        return d


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

    def set_input_values(self, design_dictionary):
        pass

    def call_3DModel(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Model':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Model", bgcolor)
