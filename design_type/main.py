from Common import *
from utils.common.load import Load
from utils.common.component import *

class Main():

    def __init__(self):
        pass

    #########################################
    # Design Preferences Functions End
    #########################################

    def bolt_values(self, input_dictionary):

        values = {KEY_DP_BOLT_TYPE: 'Pretensioned', KEY_DP_BOLT_HOLE_TYPE: 'Standard',
                  KEY_DP_BOLT_MATERIAL_G_O: '', KEY_DP_BOLT_SLIP_FACTOR: '0.3'}

        if not input_dictionary or input_dictionary[KEY_MATERIAL] == 'Select Material':
            pass
            # bolt_type = 'Pretensioned'
            # hole_type = 'Standard'
            # material_g_o = ''
            # slip_factor = '0.3'
        else:
            values[KEY_DP_BOLT_MATERIAL_G_O] = Material(input_dictionary[KEY_MATERIAL]).fu
            # bolt_type = 'Pretensioned'
            # hole_type = 'Standard'
            # material_g_o = Material(input_dictionary[KEY_MATERIAL]).fu
            # slip_factor = '0.3'

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        bolt = []

        t1 = (KEY_DP_BOLT_TYPE, KEY_DISP_TYP, TYPE_COMBOBOX, ['Pretensioned', 'Non-pretensioned'], values[KEY_DP_BOLT_TYPE])
        bolt.append(t1)

        t2 = (KEY_DP_BOLT_HOLE_TYPE, KEY_DISP_DP_BOLT_HOLE_TYPE, TYPE_COMBOBOX, ['Standard', 'Over-sized'], values[KEY_DP_BOLT_HOLE_TYPE])
        bolt.append(t2)

        t3 = (KEY_DP_BOLT_MATERIAL_G_O, KEY_DISP_DP_BOLT_MATERIAL_G_O, TYPE_TEXTBOX, None, values[KEY_DP_BOLT_MATERIAL_G_O])
        bolt.append(t3)

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

        values = {KEY_DP_WELD_FAB: KEY_DP_WELD_FAB_SHOP, KEY_DP_WELD_MATERIAL_G_O: ''}

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

        values = {KEY_DP_DETAILING_EDGE_TYPE: 'a - Sheared or hand flame cut',
                  KEY_DP_DETAILING_GAP: '10',
                  KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No'}

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        detailing = []

        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX,
              ['a - Sheared or hand flame cut', 'b - Rolled, machine-flame cut, sawn and planed'],
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
              ['Limit State Design', 'Limit State (Capacity based) Design', 'Working Stress Design'],
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
            I_t = sec_prop.calc_torsion_const(D,B,t_w,t_f)
            I_w = sec_prop.calc_torsion_const(D,B,t_w, t_f)
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

        d = {'Label_23': str(source),
             'Label_24': str(source),
             'Label_21': str(source)}
        return d



# <<<<<<< HEAD
#         else:
#             a = float(self[0])
#             b = float(self[1])
#             t = float(self[2])
#             l = str(self[3])
#             p = str(self[4])
#             print(p, "shxv")
#             if p == "Angles":
#                 sec_prop = Single_Angle_Properties()
#             elif p == "Back to Back Angles":
#                 sec_prop = BBAngle_Properties()
#             else:
#                 sec_prop = SAngle_Properties()
#             # sec_prop = Single_Angle_Properties()
#             mass = sec_prop.calc_Mass(a,b,t,l)
#             area = sec_prop.calc_Area(a,b,t,l)
#             Cz = sec_prop.calc_Cz(a,b,t,l)
#             Cy = sec_prop.calc_Cy(a,b,t,l)
#             moa_z = sec_prop.calc_MomentOfAreaZ(a,b,t,l)
#             moa_y = sec_prop.calc_MomentOfAreaY(a,b,t,l)
#             moa_u = sec_prop.calc_MomentOfAreaU(a,b,t,l)
#             moa_v = sec_prop.calc_MomentOfAreaV(a,b,t,l)
#             rog_z = sec_prop.calc_RogZ(a,b,t,l)
#             rog_y = sec_prop.calc_RogY(a,b,t,l)
#             rog_u = sec_prop.calc_RogU(a,b,t,l)
#             rog_v = sec_prop.calc_RogV(a,b,t,l)
#             em_z = sec_prop.calc_ElasticModulusZz(a,b,t,l)
#             em_y = sec_prop.calc_ElasticModulusZy(a,b,t,l)
#             pm_z = sec_prop.calc_PlasticModulusZpz(a,b,t,l)
#             pm_y = sec_prop.calc_PlasticModulusZpy(a,b,t,l)
#             I_t = sec_prop.calc_TorsionConstantIt(a,b,t,l)
#
#
#         d = {'Label_9': str(mass),
#              'Label_10': str(area),
#              'Label_7': str(Cz),
#              'Label_8': str(Cy),
#              'Label_11': str(moa_z),
#              'Label_12': str(moa_y),
#              'Label_13': str(moa_u),
#              'Label_14': str(moa_v),
#              'Label_15': str(rog_z),
#              'Label_16': str(rog_y),
#              'Label_17': str(rog_u),
#              'Label_18': str(rog_v),
#              'Label_19': str(em_z),
#              'Label_20': str(em_y),
#              'Label_21': str(pm_z),
#              'Label_22': str(pm_y),
#              'Label_23': str(I_t),
#              }
#
#         return d
# =======
# >>>>>>> 1c833caa1f03444a8abe5448ebf99d46febe33ee

    # def get_BBAngle_sec_properties(self):
    #
    #     if '' in self:
    #         mass = ''
    #         area = ''
    #         Cz = ''
    #         Cy = ''
    #         moa_z = ''
    #         moa_y = ''
    #         moa_u = ''
    #         moa_v = ''
    #         rog_z = ''
    #         rog_y = ''
    #         rog_u = ''
    #         rog_v = ''
    #         em_z = ''
    #         em_y = ''
    #         pm_z = ''
    #         pm_y = ''
    #         I_t = ''
    #
    #     else:
    #         a = float(self[0])
    #         b = float(self[1])
    #         t = float(self[2])
    #         l = float(self[3])
    #
    #         sec_prop = BBAngle_Properties()
    #         mass = sec_prop.calc_Mass(a,b,t,l)
    #         area = sec_prop.calc_Area(a,b,t,l)
    #         Cz = sec_prop.calc_Cz(a,b,t,l)
    #         Cy = sec_prop.calc_Cy(a,b,t,l)
    #         moa_z = sec_prop.calc_MomentOfAreaZ(a,b,t,l)
    #         moa_y = sec_prop.calc_MomentOfAreaY(a,b,t,l)
    #         moa_u = sec_prop.calc_MomentOfAreaU(a,b,t,l)
    #         moa_v = sec_prop.calc_MomentOfAreaV(a,b,t,l)
    #         rog_z = sec_prop.calc_RogZ(a,b,t,l)
    #         rog_y = sec_prop.calc_RogY(a,b,t,l)
    #         rog_u = sec_prop.calc_RogU(a,b,t,l)
    #         rog_v = sec_prop.calc_RogV(a,b,t,l)
    #         em_z = sec_prop.calc_ElasticModulusZz(a,b,t,l)
    #         em_y = sec_prop.calc_ElasticModulusZy(a,b,t,l)
    #         pm_z = sec_prop.calc_PlasticModulusZpz(a,b,t,l)
    #         pm_y = sec_prop.calc_PlasticModulusZpy(a,b,t,l)
    #         I_t = sec_prop.calc_TorsionConstantIt(a,b,t,l)
    #
    #
    #     d = {'Label_9': str(mass),
    #          'Label_10': str(area),
    #          'Label_7': str(Cz),
    #          'Label_8': str(Cy),
    #          'Label_11': str(moa_z),
    #          'Label_12': str(moa_y),
    #          'Label_13': str(moa_u),
    #          'Label_14': str(moa_v),
    #          'Label_15': str(rog_z),
    #          'Label_16': str(rog_y),
    #          'Label_17': str(rog_u),
    #          'Label_18': str(rog_v),
    #          'Label_19': str(em_z),
    #          'Label_20': str(em_y),
    #          'Label_21': str(pm_z),
    #          'Label_22': str(pm_y),
    #          'Label_23': str(I_t),
    #          }
    #
    #     return d


# <<<<<<< HEAD
#         else:
#             f_w = float(self[0])
#             f_t = float(self[1])
#             w_h = float(self[2])
#             w_t = float(self[3])
#             l = self[4]
#             section_profile = self[5]
#             if section_profile == "Channels":
#                 sec_prop = Single_Channel_Properties()
#             else:
#                 sec_prop = BBChannel_Properties()
#             mass = sec_prop.calc_Mass(f_w, f_t, w_h, w_t)
#             area = sec_prop.calc_Area(f_w, f_t, w_h, w_t)
#             C_y = sec_prop.calc_C_y(f_w, f_t, w_h, w_t)
#             moa_z = sec_prop.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t)
#             moa_y = sec_prop.calc_MomentOfAreaY(f_w, f_t, w_h, w_t)
#
#             rog_z = sec_prop.calc_RogZ(f_w, f_t, w_h, w_t)
#             rog_y = sec_prop.calc_RogY(f_w, f_t, w_h, w_t)
#
#             em_z = sec_prop.calc_ElasticModulusZz(f_w, f_t, w_h, w_t)
#             em_y = sec_prop.calc_ElasticModulusZy(f_w, f_t, w_h, w_t)
#             pm_z = sec_prop.calc_PlasticModulusZpz(f_w, f_t, w_h, w_t)
#             pm_y = sec_prop.calc_PlasticModulusZpy(f_w, f_t, w_h, w_t)
#
#         d = {'Label_9': str(mass),
#              'Label_10': str(area),
#              'Label_11': str(moa_z),
#              'Label_12': str(moa_y),
#              'Label_15': str(rog_z),
#              'Label_16': str(rog_y),
#              'Label_17': str(C_y),
#              'Label_19': str(em_z),
#              'Label_20': str(em_y),
#              'Label_21': str(pm_z),
#              'Label_22': str(pm_y),
#              }
#
#         return d
# =======
# >>>>>>> 1c833caa1f03444a8abe5448ebf99d46febe33ee


    #########################################
    # Design Preferences Functions End
    #########################################


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




