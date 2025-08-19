from .shear_connection import ShearConnection
from ...utils.common.component import *
from ...utils.common.component import Bolt, Plate, Weld
from ...Common import *
import sys
from ...Report_functions import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...utils.common.load import Load
import logging
from importlib.resources import files

class CleatAngleConnection(ShearConnection):

    def __init__(self):
        super(CleatAngleConnection, self).__init__()
        self.sptd_leg_length = 0.0
        self.sptIng_leg_length = 0.0
        self.design_status = False

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_supporting_section)
        tabs.append(t1)

        t1 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_supported_section)
        tabs.append(t1)

        t6 = (DISP_TITLE_CLEAT, TYPE_TAB_1, self.tab_angle_section)
        tabs.append(t6)

        t2 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t2)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):
        change_tab = []

        t1 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC_MATERIAL], [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY],
              TYPE_TEXTBOX, self.get_fu_fy_I_section_suptng)
        change_tab.append(t1)

        t2 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC_MATERIAL], [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY],
              TYPE_TEXTBOX, self.get_fu_fy_I_section_suptd)
        change_tab.append(t2)

        t5 = (DISP_TITLE_CLEAT, ['Label_1', 'Label_2','Label_3'],
              ['Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15',
               'Label_16', 'Label_17', 'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23', KEY_IMAGE],
              TYPE_TEXTBOX, self.get_Angle_sec_properties)
        change_tab.append(t5)

        t6 = (DISP_TITLE_CLEAT, [KEY_ANGLE_LIST, KEY_CONNECTOR_MATERIAL],
              [KEY_ANGLE_SELECTED, KEY_CONNECTOR_FY, KEY_CONNECTOR_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5', 'Label_7',
               'Label_8', 'Label_9','Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17',
               'Label_18','Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23','Label_24', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_new_angle_section_properties)
        change_tab.append(t6)


        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20','Label_21','Label_22',KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20','Label_21','Label_22',KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        t7 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

        t8 = (DISP_TITLE_CLEAT, [KEY_ANGLE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t8)

        return change_tab

    def input_dictionary_design_pref(self):
        design_input = []
        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SUPTNGSEC_MATERIAL])
        design_input.append(t1)

        # t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY])
        # design_input.append(t1)

        t2 = (KEY_DISP_BEAMSEC, TYPE_COMBOBOX, [KEY_SUPTDSEC_MATERIAL])
        design_input.append(t2)

        # t2 = (KEY_DISP_BEAMSEC, TYPE_TEXTBOX, [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY])
        # design_input.append(t2)
        t2 = (DISP_TITLE_CLEAT, TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t2)

        t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        design_input.append(t3)

        t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        design_input.append(t5)

        t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SUPTNGSEC_MATERIAL, KEY_SUPTDSEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_GAP,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

         :return: This function returns list of tuples which has keys that needs to be updated,
          on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

          [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
         """

        add_buttons = []

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, KEY_CONN, VALUES_CONN_1, "Columns")
        add_buttons.append(t1)

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, KEY_CONN, VALUES_CONN_2, "Beams")
        add_buttons.append(t1)

        t2 = (KEY_DISP_BEAMSEC, KEY_SUPTDSEC, TYPE_COMBOBOX, KEY_SUPTDSEC, None, None, "Beams")
        add_buttons.append(t2)

        t2 = (DISP_TITLE_CLEAT, KEY_ANGLE_LIST, TYPE_COMBOBOX_CUSTOMIZED, KEY_ANGLE_SELECTED, None, None, "Angles")
        add_buttons.append(t2)

        return add_buttons

    ####################################
    # Design Preference Functions End
    ####################################

    def input_values(self):

        self.module = KEY_DISP_CLEATANGLE

        options_list = []

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, VALUES_CONN, True, 'No Validator')
        options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, str(files("osdag.data.ResourceFiles.images").joinpath("fin_cf_bw.png")), True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, VALUES_COLSEC, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, VALUES_SECBM, True, 'No Validator')
        options_list.append(t5)

        t6 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t6)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t13 = (None, DISP_TITLE_CLEAT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t13)

        t15 = (KEY_ANGLE_LIST, KEY_DISP_CLEATSEC, TYPE_COMBOBOX_CUSTOMIZED, VALUES_ANGLESEC, True, 'No Validator')
        options_list.append(t15)

        t16 = (KEY_MODULE, KEY_DISP_CLEATANGLE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        return options_list

    @staticmethod
    def cleatsec_customized():
        a = VALUES_CLEAT_CUSTOMIZED
        return a

    # @staticmethod
    # def diam_bolt_customized():
    #     c = connectdb1()
    #     if "36" in c: c.remove("36")
    #     return c

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t2 = (KEY_ANGLE_LIST, self.cleatsec_customized)
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
            return VALUES_COLSEC
        elif conn in VALUES_CONN_2:
            return VALUES_PRIBM
        else:
            return []

    def fn_conn_suptdsec(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return VALUES_SECBM
        elif conn in VALUES_CONN_2:
            return VALUES_SECBM
        else:
            return []

    def fn_conn_image(self):

        conn = self[0]
        if conn == VALUES_CONN[0]:
            return str(files("osdag.data.ResourceFiles.images").joinpath("fin_cf_bw.png"))
        elif conn == VALUES_CONN[1]:
            return str(files("osdag.data.ResourceFiles.images").joinpath("fin_cw_bw.png"))
        elif conn in VALUES_CONN_2:
            return str(files("osdag.data.ResourceFiles.images").joinpath("fin_beam_beam.png"))
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

        t6 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t6)

        return lst

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('Cleat Angle', self.call_3DCleat)
        components.append(t4)

        return components

    def call_3DCleat(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Cleat Angle':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("cleatAngle", bgcolor)

    def output_values(self, flag):
        """
        Function to return a list of tuples to be displayed as the UI.(Output Dock)
        """

        # @author: Umair

        out_list = []
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """      Cleat Angle Properties: Start        """

        t20 = (None, DISP_OUT_TITLE_CLEAT, TYPE_TITLE, None, True)
        out_list.append(t20)

        t21 = (KEY_OUT_CLEAT_SECTION, KEY_OUT_DISP_CLEAT_SECTION, TYPE_TEXTBOX, self.cleat.designation if flag else '', True)
        out_list.append(t21)

        t15 = (KEY_OUT_CLEAT_HEIGHT, KEY_OUT_DISP_CLEAT_HEIGHT, TYPE_TEXTBOX, self.sptd_leg.height if flag else '', True)
        out_list.append(t15)

        t17 = (KEY_OUT_CLEAT_SHEAR, KEY_DISP_SHEAR_YLD, TYPE_TEXTBOX, round(self.sptd_leg.cleat_shear_capacity / 1000, 2) if flag else '', True)
        out_list.append(t17)

        t18 = (KEY_OUT_CLEAT_BLK_SHEAR, KEY_DISP_BLK_SHEAR, TYPE_TEXTBOX, round(self.sptd_leg.block_shear_capacity / 1000, 2) if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_CLEAT_MOM_DEMAND, KEY_DISP_MOM_DEMAND, TYPE_TEXTBOX, round(self.sptd_leg.moment_demand / 1000000, 2) if flag else '', True)
        out_list.append(t19)
        #
        t20 = (KEY_OUT_CLEAT_MOM_CAPACITY, KEY_DISP_MOM_CAPACITY, TYPE_TEXTBOX, round(self.sptd_leg.cleat_moment_capacity / 1000000, 2) if flag else '', True)
        out_list.append(t20)

        """     Cleat Angle Properties: End                       """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """     Bolt Properties: Start                            """

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_diameter_provided if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_PC_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_PC_provided if flag else '', True)
        out_list.append(t3)

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """     Bolt Properties- Supported leg: Start             """

        t4 = (None, DISP_OUT_TITLE_SPTDLEG, TYPE_TITLE, None, True)
        out_list.append(t4)

        t9 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.sptd_leg.bolt_line if flag else '', True)
        out_list.append(t9)

        t10 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.sptd_leg.bolts_one_line if flag else '', True)
        out_list.append(t10)

        t8 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX, round(self.sptd_leg.bolt_force / 1000, 2) if flag else '', True)
        out_list.append(t8)

        t6 = (KEY_OUT_BOLT_CAPACITY_SPTD, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.bolt_capacity_disp_sptd if flag else '', True)
        out_list.append(t6)

        t3_2 = (KEY_OUT_BOLT_IR_DETAILS_SPTD, KEY_OUT_DISP_BOLT_IR_DETAILS, TYPE_OUT_BUTTON, ['Details', self.bolt_capacity_details_supported], True)
        out_list.append(t3_2)

        t11 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t11)

        """     Bolt Properties- Supported leg: End                """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """     Bolt Properties- Supporting leg: Start             """

        t12 = (None, DISP_OUT_TITLE_SPTINGLEG, TYPE_TITLE, None, True)
        out_list.append(t12)

        t17 = (KEY_OUT_SPTING_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.spting_leg.bolt_line if flag else '', True)
        out_list.append(t17)

        t18 = (KEY_OUT_SPTING_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.spting_leg.bolts_one_line if flag else '', True)
        out_list.append(t18)

        t16 = (KEY_OUT_SPTING_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX, round(self.spting_leg.bolt_force / 1000, 2) if flag else '', True)
        out_list.append(t16)

        t6 = (KEY_OUT_BOLT_CAPACITY_SPTING, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.bolt_capacity_disp_spting if flag else '', True)
        out_list.append(t6)

        t3_2 = (KEY_OUT_BOLT_IR_DETAILS_SPTING, KEY_OUT_DISP_BOLT_IR_DETAILS, TYPE_OUT_BUTTON, ['Details', self.bolt_capacity_details_suporting], True)
        out_list.append(t3_2)

        t19 = (KEY_OUT_SPTING_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spting_spacing], True)
        out_list.append(t19)

        """      Bolt Properties- Supporting leg: End        """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""

        return out_list

    def bolt_capacity_details_supported(self, flag):

        bolt_details_sptd = []

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX, round(self.bolt.bolt_shear_capacity/1000,2) if flag else '', True)
        bolt_details_sptd.append(t4)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            print("wats this",self.bolt.bolt_bearing_capacity)
            if self.bolt.bolt_bearing_capacity != 'N/A':
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
            else:
                bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        bolt_details_sptd.append(t5)

        t5_1 = (KEY_OUT_BETA_LJ, KEY_OUT_DISP_BETA_LJ, TYPE_TEXTBOX, round(self.beta_lj_sptd, 3) if flag else 'N/A', True)
        bolt_details_sptd.append(t5_1)

        t5_2 = (KEY_OUT_BETA_LG, KEY_OUT_DISP_BETA_LG, TYPE_TEXTBOX, round(self.beta_lg_sptd, 3) if flag and self.bolt.bolt_type == TYP_BEARING else 'N/A', True)
        bolt_details_sptd.append(t5_2)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.bolt_capacity_disp_sptd if flag else '', True)
        bolt_details_sptd.append(t6)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_FORCE, TYPE_TEXTBOX, round(self.sptd_leg.bolt_force / 1000, 2) if flag else '', True)
        bolt_details_sptd.append(t21)

        return bolt_details_sptd

    def bolt_capacity_details_suporting(self, flag):

        bolt_details_spting = []

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX, round(self.bolt2.bolt_shear_capacity / 1000, 2) if flag else '', True)
        bolt_details_spting.append(t4)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity != 'N/A':
                bolt_bearing_capacity_disp = round(self.bolt2.bolt_bearing_capacity / 1000, 2)
            else:
                bolt_bearing_capacity_disp = self.bolt2.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        bolt_details_spting.append(t5)

        t5_1 = (KEY_OUT_BETA_LJ, KEY_OUT_DISP_BETA_LJ, TYPE_TEXTBOX, round(self.beta_lj_spting, 3) if flag else 'N/A', True)
        bolt_details_spting.append(t5_1)

        t5_2 = (KEY_OUT_BETA_LG, KEY_OUT_DISP_BETA_LG, TYPE_TEXTBOX, round(self.beta_lg_spting, 3) if flag and self.bolt.bolt_type == TYP_BEARING else 'N/A', True)
        bolt_details_spting.append(t5_2)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.bolt_capacity_disp_spting if flag else '', True)
        bolt_details_spting.append(t6)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_FORCE, TYPE_TEXTBOX, round(self.spting_leg.bolt_force / 1000, 2) if flag else '', True)
        bolt_details_spting.append(t21)

        return bolt_details_spting

    def spacing(self, status):

        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
               [str(files("osdag.data.ResourceFiles.images").joinpath("cleat_beam.png")), 400, 277, ""])  # [image, width, height, caption]
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.sptd_leg.gauge_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.sptd_leg.edge_dist_provided if status else '')
        spacing.append(t10)

        gauge1 = (max(self.cleat.thickness + self.cleat.root_radius, self.sptd_leg.gap) + self.sptd_leg.end_dist_provided)

        t11 = (KEY_OUT_GAUGE1, KEY_OUT_DISP_GAUGE1, TYPE_TEXTBOX, gauge1 if status else '')
        spacing.append(t11)

        t11 = (KEY_OUT_GAUGE2, KEY_OUT_DISP_GAUGE2, TYPE_TEXTBOX, self.sptd_leg.pitch_provided if status else '')
        spacing.append(t11)

        edge = (self.cleat.leg_a_length - self.sptd_leg.pitch_provided * (self.sptd_leg.bolt_line - 1) - gauge1)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, edge if status else '')
        spacing.append(t12)

        return spacing

    def spting_spacing(self, status):

        spting_spacing = []
        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details")
        spting_spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
               [str(files("osdag.data.ResourceFiles.images").joinpath("cleat.png")), 400, 277, ""])  # [image, width, height, caption]
        spting_spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.spting_leg.gauge_provided if status else '')
        spting_spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.spting_leg.edge_dist_provided if status else '')
        spting_spacing.append(t10)

        gauge1 = (self.cleat.thickness + self.cleat.root_radius + self.spting_leg.end_dist_provided)

        t11 = (KEY_OUT_GAUGE1, KEY_OUT_DISP_GAUGE1, TYPE_TEXTBOX, gauge1 if status else '')
        spting_spacing.append(t11)

        t11 = (KEY_OUT_GAUGE2, KEY_OUT_DISP_GAUGE2, TYPE_TEXTBOX, self.spting_leg.pitch_provided if status else '')
        spting_spacing.append(t11)

        edge = (self.cleat.leg_a_length - self.spting_leg.pitch_provided * (self.spting_leg.bolt_line - 1) - gauge1)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, edge if status else '')
        spting_spacing.append(t12)

        return spting_spacing

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def module_name(self):
        return KEY_DISP_CLEATANGLE

    def set_input_values(self, design_dictionary):
        print(design_dictionary)

        super(CleatAngleConnection,self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.cleat_list = design_dictionary[KEY_ANGLE_LIST]
        self.cleat_material_grade = design_dictionary[KEY_CONNECTOR_MATERIAL]
        print(self.cleat_list)
        self.bolt2 = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                         bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])

        self.sptd_leg = Plate(material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.spting_leg = Plate(material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],gap=design_dictionary[KEY_DP_DETAILING_GAP])

        # logger.info("Input values are set. Checking if angle of required thickness is available")

        self.check_available_cleat_thk(self)

    def check_available_cleat_thk(self):
        self.thickness_list = []
        self.cleat_list_thk = []
        self.leg_lengths = []
        min_thickness = self.supported_section.web_thickness / 2
        if self.connectivity == VALUES_CONN_1[0]:
            self.available_length = (self.supporting_section.flange_width - self.supported_section.web_thickness )/2
        elif self.connectivity == VALUES_CONN_1[1]:
            self.available_length = (self.supporting_section.depth - 2 * self.supporting_section.flange_thickness -
                                2 * self.supporting_section.root_radius - self.supported_section.web_thickness) / 2
        else:
            self.available_length = math.inf

        for designation in self.cleat_list:
            cleat = Angle(designation=designation, material_grade=self.cleat_material_grade)
            if cleat.thickness*2 >= self.supported_section.web_thickness and cleat.leg_a_length <= self.available_length:
                self.cleat_list_thk.append(designation)
                print("added", designation)
                print(self.cleat_list_thk)
            else:
                if cleat.thickness not in self.thickness_list:
                    self.thickness_list.append(cleat.thickness)
                    print("added", designation, self.thickness_list)
                if cleat.leg_a_length not in self.leg_lengths:
                    self.leg_lengths.append(cleat.leg_a_length)
                    print("added", designation, self.leg_lengths)

        # self.cleat_list_leg = []
        if self.cleat_list_thk:
            # logger.info("Required cleat thickness available. Doing preliminary member checks")
            self.member_capacity(self)
        else:
            if self.connectivity in VALUES_CONN_1:
                logger.error("Cleat Angle should have minimum thickness of {} and maximum leg length of {}."
                             .format(min_thickness,round(self.available_length,2)))
            else:
                logger.error(
                    "Cleat Angle should have minimum thickness of %2.2f." % min_thickness)
    def member_capacity(self):
        super(CleatAngleConnection, self).member_capacity(self)
        self.supported_section.low_shear_capacity = round(0.6 * self.supported_section.shear_yielding_capacity, 2)

        if self.supported_section.low_shear_capacity / 1000 > self.load.shear_force and \
                    self.supporting_section.tension_yielding_capacity / 1000 > self.load.axial_force:

            if self.load.shear_force <= min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                            40.0):
                logger.warning(" : User input for shear force is very less compared to section capacity. "
                               "Setting Shear Force value to 15% of supported beam shear capacity or 40kN, whichever is less.")
                self.load.shear_force = min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                            40.0)

            print("preliminary member check is satisfactory. Checking available Bolt Diameters")
            self.supported_section.design_status = True
            self.select_bolt_dia_beam(self)

        else:
            self.design_status = False
            logger.warning(
                " : The shear yielding capacity (low shear case) {} and/or tension yielding capacity {} is less "
                "than the applied load. Define a large/larger section(s) or decrease the load."
                .format(round(self.supported_section.low_shear_capacity / 1000, 2),
                        round(self.supported_section.tension_yielding_capacity / 1000, 2)))
            print(
                "The preliminary member check(s) have failed. Select a large/larger section(s) or decrease load and re-design.")

    def select_bolt_dia_beam(self):

        self.output = []
        self.beta_lj_sptd = 1.0
        self.beta_lg_sptd = 1.0
        trial = 0

        self.min_plate_height = self.supported_section.min_plate_height()
        print(self.min_plate_height, "is min height")
        self.max_plate_height = self.supported_section.max_plate_height(self.connectivity,
                                                                              self.supported_section.notch_ht)



        for self.cleatangle in self.cleat_list_thk:
            self.cleat = Angle(designation=self.cleatangle, material_grade=self.cleat_material_grade)
            # self.sptd_leg.thickness_provided = self.cleat.thickness
            bolts_required_previous = 2
            self.bolt.bolt_PC_provided = self.bolt.bolt_grade[-1]
            count = 0

            self.sptd_bolt_conn_plates_t_fu_fy = []
            self.sptd_bolt_conn_plates_t_fu_fy.append((2*self.cleat.thickness, self.sptd_leg.fu, self.sptd_leg.fy))
            self.sptd_bolt_conn_plates_t_fu_fy.append((self.supported_section.web_thickness, self.supported_section.fu, self.supported_section.fy))

            """
            # while considering eccentricity, distance from bolt line to supporting member will be,
            # end_dist+gap or end_dist+root_radius+cleat_thickness, whichever is maximum
            #
            """

            self.end_to_sptd = max(self.sptd_leg.gap, self.cleat.thickness + self.cleat.root_radius)

            for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
                self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                        conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,n=2)

                self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                  bolt_grade_provided=self.bolt.bolt_PC_provided,
                                                  conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                                  n_planes=2)
                print("Suptd bolt capacity: ", self.bolt.bolt_capacity)

                self.l_j_sptd = self.sptd_leg.gauge_provided * (self.sptd_leg.bolts_one_line - 1)
                self.t_sum_sptd = self.supported_section.web_thickness + 2 * self.cleat.thickness

                self.beta_lj_sptd = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided,
                                                                           self.l_j_sptd)
                if self.bolt.bolt_type == TYP_BEARING:
                    self.beta_lg_sptd = IS800_2007.cl_10_3_3_2_bolt_large_grip(self.bolt.bolt_diameter_provided,
                                                                               self.t_sum_sptd, self.l_j_sptd)
                else:
                    self.beta_lg_sptd = 1.0
                print(self.min_plate_height,"is another min_height")
                self.sptd_leg.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                                 web_plate_h_min=self.min_plate_height,
                                                 web_plate_h_max=self.max_plate_height,
                                                 bolt_capacity=self.bolt.bolt_capacity,
                                                 min_edge_dist=self.bolt.min_edge_dist_round,
                                                 min_gauge=self.bolt.min_gauge_round,
                                                 max_spacing=self.bolt.max_spacing_round,
                                                 max_edge_dist=self.bolt.max_edge_dist_round,
                                                 shear_load=self.load.shear_force * 1000,
                                                 gap=self.end_to_sptd,
                                                 shear_ecc=True, bolt_line_limit=2,
                                                 beta_lg=self.beta_lg_sptd)
                # if self.connectivity in VALUES_CONN_1:
                if self.bolt.bolt_type == TYP_BEARING:
                    if 8 * self.bolt.bolt_diameter_provided < self.t_sum_sptd:
                        self.sptd_leg.grip_status = False
                        self.sptd_leg.design_status = False
                if self.sptd_leg.length > self.cleat.leg_a_length or self.sptd_leg.design_status == False or self.sptd_leg.grip_status == False:
                    self.sptd_leg.design_status = False
                    count = 0
                    continue
                else:
                    # self.cleat_angle_check(self)
                    self.sptd_leg.design_status = True
                print(1, self.sptd_leg.bolt_force, self.bolt.bolt_capacity, self.bolt.bolt_diameter_provided,
                      self.sptd_leg.bolts_required, self.sptd_leg.bolts_one_line)
                if self.sptd_leg.design_status is True:
                    if self.sptd_leg.bolts_required > bolts_required_previous and count >= 1:
                        self.bolt.bolt_diameter_provided = bolt_dia_previous
                        self.sptd_leg.length = length_previous
                        self.sptd_leg.height = height_previous
                        self.sptd_leg.bolt_line = bolt_line_previous
                        self.sptd_leg.bolts_one_line = bolts_one_line_previous
                        self.sptd_leg.bolts_required = bolts_required_previous
                        self.sptd_leg.bolt_capacity_red = bolt_capacity_red_previous
                        self.sptd_leg.bolt_force = vres_previous
                        self.sptd_leg.moment_demand = moment_demand_previous
                        self.sptd_leg.pitch_provided = pitch_previous
                        self.sptd_leg.gauge_provided = gauge_previous
                        self.sptd_leg.edge_dist_provided = edge_dist_previous
                        self.sptd_leg.end_dist_provided = end_dist_previous
                        self.beta_lj_sptd = beta_lj_sptd_previous
                        self.beta_lg_sptd = beta_lg_sptd_previous
                        break
                    bolt_dia_previous = self.bolt.bolt_diameter_provided
                    length_previous = self.sptd_leg.length
                    height_previous = self.sptd_leg.height
                    bolt_line_previous = self.sptd_leg.bolt_line
                    bolts_one_line_previous = self.sptd_leg.bolts_one_line
                    bolts_required_previous = self.sptd_leg.bolts_required
                    bolt_capacity_red_previous = self.sptd_leg.bolt_capacity_red
                    vres_previous = self.sptd_leg.bolt_force
                    moment_demand_previous = self.sptd_leg.moment_demand
                    pitch_previous = self.sptd_leg.pitch_provided
                    gauge_previous = self.sptd_leg.gauge_provided
                    edge_dist_previous = self.sptd_leg.edge_dist_provided
                    end_dist_previous = self.sptd_leg.end_dist_provided
                    beta_lj_sptd_previous = self.beta_lj_sptd
                    beta_lg_sptd_previous = self.beta_lg_sptd

                    count += 1
                else:
                    pass
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,n=2)

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_PC_provided,
                                              conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                              n_planes=2)
            if self.sptd_leg.length <= self.cleat.leg_a_length and self.sptd_leg.design_status == True:
                # self.spting_leg.end_dist_provided = self.cleat.leg_a_length - self.cleat.thickness - self.cleat.root_radius - \
                #                             self.spting_leg.end_dist_provided
                self.sptd_leg.cleat_angle_check(self.sptd_leg.height, self.cleat.thickness, self.sptd_leg.bolts_one_line,
                                       self.sptd_leg.bolt_line, self.sptd_leg.gauge_provided,
                                       self.sptd_leg.edge_dist_provided, self.sptd_leg.pitch_provided,
                                       self.sptd_leg.end_dist_provided, self.bolt.dia_hole, self.sptd_leg.fu,
                                       self.sptd_leg.fy, self.sptd_leg.moment_demand, self.max_plate_height,
                                       self.load.shear_force * 1000)
                print("supd_des_st:", self.sptd_leg.design_status)
            else:
                # if self.sptd_leg.reason == "":
                #     self.sptd_leg.reason = (": Req leg length is {} and Available width on flange side is {}"
                #                             .format(self.sptd_leg.length, self.cleat.leg_a_length))
                self.sptd_leg.design_status = False

            if self.sptd_leg.design_status is False:
                self.design_status = False
                # logger.error(self.sptd_leg.reason)
                supporting_leg_check = False


            else:
                supporting_leg_check = self.select_bolt_dia_supporting(self)

            if supporting_leg_check:
                trial += 1
                self.total_bolts_sptd = self.sptd_leg.bolts_one_line * self.sptd_leg.bolt_line
                self.total_bolts_spting = self.spting_leg.bolts_one_line * self.spting_leg.bolt_line

                ##### O U T P U T   D I C T I O N A R Y   F O R M A T #####
                row = [int(self.bolt.bolt_diameter_provided),   # 0-Bolt Diameter
                       self.bolt.bolt_PC_provided,              # 1-Bolt Grade
                       self.cleat.designation,                  # 2-Cleat Angle designation
                       self.cleat.thickness,                    # 3-Cleat Angle Thickness
                       self.cleat.leg_a_length,                 # 4-Cleat angle leg size
                       self.sptd_leg.bolts_one_line,            # 5-Bolt rows on cleat angle supported leg
                       self.sptd_leg.bolt_line,                 # 6-Bolt columns on cleat angle supported leg
                       self.sptd_leg.height,                    # 7-Length of the cleat angle
                       self.sptd_leg.bolt_force,                # 8-Bolt Force on supported leg
                       self.spting_leg.bolts_one_line,          # 9-Bolt rows on cleat angle supporting leg
                       self.spting_leg.bolt_line,               # 10-Bolt columns on cleat angle supporting leg
                       self.spting_leg.height,                  # 11-Length of the cleat angle
                       self.spting_leg.bolt_force,              # 12-Bolt Force on supporting leg
                       self.total_bolts_sptd,                   # 13-Total bolts on supported leg
                       self.total_bolts_spting,                 # 14-Total bolts on supporting leg
                       self.sptd_leg.pitch_provided,            # 15-Pitch provided on the supported leg
                       self.sptd_leg.gauge_provided,            # 16-Gauge provided on the supported leg
                       self.sptd_leg.end_dist_provided,         # 17-End Distance provided on the supported leg
                       self.sptd_leg.edge_dist_provided,        # 18-Edge Distance provided on the supported leg
                       self.spting_leg.pitch_provided,          # 19-Pitch provided on the supporting leg
                       self.spting_leg.gauge_provided,          # 20-Gauge provided on the supporting leg
                       self.spting_leg.end_dist_provided,       # 21-End Distance provided on the supporting leg
                       self.spting_leg.edge_dist_provided,      # 22-Edge Distance provided on the supporting leg
                       self.bolt.bolt_shear_capacity,           # 23-Bolt shear capacity on the supported leg
                       self.bolt.bolt_bearing_capacity,         # 24-Bolt bearing capacity on the supported leg
                       self.bolt2.bolt_shear_capacity,          # 25-Bolt shear capacity on the supporting leg
                       self.bolt2.bolt_bearing_capacity,        # 26-Bolt bearing capacity on the supporting leg
                       self.cleat.root_radius,                  # 27-Cleat angle root radius
                       self.sptd_leg.block_shear_capacity,      # 28-Cleat angle block shear capacity
                       self.sptd_leg.cleat_shear_capacity,      # 29-Cleat angle shear yielding capacity
                       self.sptd_leg.cleat_moment_capacity,     # 30-Cleat angle moment capacity
                       self.sptd_leg.moment_demand,             # 31-Cleat angle moment demand

                       trial]
                self.output.append(row)
                print("********* Trial {} ends here *************".format(trial))

        if self.output == []:
            self.design_status = False
            if self.sptd_leg.design_status is False:
                self.bolt_capacity_disp_sptd = round(
                    (self.bolt.bolt_capacity * self.beta_lj_sptd * self.beta_lg_sptd) / 1000, 2)
                if self.sptd_leg.grip_status == False:
                    self.sptd_leg.reason = "Fails in grip length on supported side."
                if self.sptd_leg.reason == "":
                    logger.info("{}rows {}columns {}mm diameter bolts needs leg length of {}"
                                .format(self.sptd_leg.bolts_one_line, self.sptd_leg.bolt_line,
                                        self.bolt.bolt_diameter_provided, self.sptd_leg.length))
                    logger.info("Available width is {}".format(min(self.cleat.leg_a_length,self.available_length)))
                else:
                    logger.error(self.sptd_leg.reason)
            elif self.spting_leg.design_status is False:
                self.bolt_capacity_disp_sptd = round(
                    (self.bolt.bolt_capacity * self.beta_lj_sptd * self.beta_lg_sptd) / 1000, 2)
                self.bolt_capacity_disp_spting = round(
                    (self.bolt2.bolt_capacity * self.beta_lj_spting * self.beta_lg_spting) / 1000, 2)
                if self.spting_leg.grip_status == False:
                    self.spting_leg.reason = "Fails in grip length on supporting side."
                logger.error(self.spting_leg.reason)

            logger.error("The connection cannot be designed with provided bolt diameters or cleat angle list")
        else:
            self.select_optimum(self)
            # print("why repeat",self.bolt.bolt_diameter_provided,self.cleat.designation)
            self.for_3D_view(self)
            self.design_status = True
            self.sptd_leg.design_status = True
            self.spting_leg.design_status = True
            self.sptd_leg.grip_status = True
            self.spting_leg.grip_status = True

    def select_optimum(self):
        """This function sorts the list of available options and selects the combination with least leg size or
        thickness or number of bolts"""
        self.output.sort(key=lambda x: (x[4], x[3], x[13]))
        # print(self.output)
        print(self.output[0])

        self.bolt.bolt_diameter_provided = self.output[0][0]
        self.bolt.bolt_PC_provided = self.output[0][1]
        self.cleat.designation = self.output[0][2]
        self.cleat.thickness = self.output[0][3]
        self.cleat.leg_a_length = self.output[0][4]
        self.cleat.leg_b_length = self.output[0][4]
        self.sptd_leg.bolts_one_line = self.output[0][5]
        self.sptd_leg.bolt_line = self.output[0][6]
        self.sptd_leg.height = self.output[0][7]
        self.sptd_leg.bolt_force = self.output[0][8]
        self.spting_leg.bolts_one_line = self.output[0][9]
        self.spting_leg.bolt_line = self.output[0][10]
        self.spting_leg.height = self.output[0][11]
        self.spting_leg.bolt_force = self.output[0][12]
        self.total_bolts_sptd = self.output[0][13]
        self.total_bolts_spting = self.output[0][14]
        self.sptd_leg.pitch_provided = self.output[0][15]
        self.sptd_leg.gauge_provided = self.output[0][16]
        self.sptd_leg.end_dist_provided = self.output[0][17]
        self.sptd_leg.edge_dist_provided = self.output[0][18]
        self.spting_leg.pitch_provided = self.output[0][19]
        self.spting_leg.gauge_provided = self.output[0][20]
        self.spting_leg.end_dist_provided = self.output[0][21]
        self.spting_leg.edge_dist_provided = self.output[0][22]
        self.bolt.bolt_shear_capacity = self.output[0][23]
        self.bolt.bolt_bearing_capacity = self.output[0][24]
        self.bolt2.bolt_shear_capacity = self.output[0][25]
        self.bolt2.bolt_bearing_capacity = self.output[0][26]
        self.cleat.root_radius = self.output[0][27]
        self.sptd_leg.block_shear_capacity = self.output[0][28]
        self.sptd_leg.cleat_shear_capacity = self.output[0][29]
        self.sptd_leg.cleat_moment_capacity = self.output[0][30]
        self.sptd_leg.moment_demand = self.output[0][31]

        self.get_bolt_PC(self)

    def select_bolt_dia_supporting(self):

        self.supporting_leg_check = False

        self.spting_bolt_conn_plates_t_fu_fy = []
        self.spting_bolt_conn_plates_t_fu_fy.append((self.cleat.thickness, self.sptd_leg.fu, self.sptd_leg.fy))
        if self.connectivity == VALUES_CONN_1[0]:
            self.spting_bolt_conn_plates_t_fu_fy.append((self.supporting_section.flange_thickness,
                                                       self.supporting_section.fu, self.supporting_section.fy))
        else:
            self.spting_bolt_conn_plates_t_fu_fy.append((self.supporting_section.web_thickness,
                                                       self.supporting_section.fu, self.supporting_section.fy))

        """
        # while considering eccentricity, distance from bolt line to supporting member will be,
        # end_dist+gap or end_dist+root_radius+cleat_thickness
        #
        """

        self.end_to_spting = self.cleat.thickness + self.cleat.root_radius
        # print(self.bolt.bolt_shear_capacity)
        self.bolt2.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,n=1)
        self.bolt2.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt.bolt_PC_provided,
                                          conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,
                                          n_planes=1)

        self.l_j_spting = self.spting_leg.gauge_provided * (self.spting_leg.bolts_one_line - 1)
        if self.connectivity == VALUES_CONN_1[0]:
            self.t_sum_spting = self.supporting_section.flange_thickness + self.cleat.thickness
        else:
            self.t_sum_spting = self.supporting_section.web_thickness + self.cleat.thickness

        self.beta_lj_spting = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided,
                                                                     self.l_j_spting)


        if self.bolt.bolt_type == TYP_BEARING:
            self.beta_lg_spting = IS800_2007.cl_10_3_3_2_bolt_large_grip(self.bolt.bolt_diameter_provided,
                                                                         self.t_sum_spting, self.l_j_spting)
        else:
            self.beta_lg_spting = 1.0

        self.spting_leg.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                              web_plate_h_min=self.sptd_leg.height,
                                              web_plate_h_max=self.sptd_leg.height,
                                              bolt_capacity=self.bolt2.bolt_capacity,
                                              min_edge_dist=self.sptd_leg.edge_dist_provided,
                                              min_gauge=self.sptd_leg.gauge_provided,
                                              max_spacing=self.sptd_leg.gauge_provided,
                                              max_edge_dist=self.sptd_leg.edge_dist_provided,
                                              shear_load=self.load.shear_force * 1000 / 2,
                                              gap=self.end_to_spting,
                                              shear_ecc=True, bolt_line_limit=2,
                                              min_bolts_one_line=self.sptd_leg.bolts_one_line,
                                              min_bolt_line=1,
                                              beta_lg=self.beta_lg_spting,
                                              min_end_dist=self.bolt.min_end_dist_round)
        # if self.spting_leg.length > self.cleat.leg_a_length:
            # logger.info(": {}rows {}columns {}mm diameter bolts needs leg length of {}"
            #             .format(self.spting_leg.bolts_one_line, self.spting_leg.bolt_line,
            #                     self.bolt2.bolt_diameter_provided, self.spting_leg.length))
            # logger.info(": Available width of selected cleat angle leg is {}".format(self.cleat.leg_a_length))
            # count = 0
            # continue
        print("Supporting leg side: ", self.spting_leg.design_status, self.spting_leg.bolt_force, self.bolt2.bolt_capacity,
              self.bolt2.bolt_diameter_provided, self.spting_leg.bolts_required, self.spting_leg.bolts_one_line)

        if self.bolt.bolt_type == TYP_BEARING:
            if 8 * self.bolt.bolt_diameter_provided < self.t_sum_spting:
                self.spting_leg.grip_status = False
                self.spting_leg.design_status = False

        if self.spting_leg.design_status is False and self.cleat_list_thk and self.spting_leg.grip_status is True:
            self.cleat_list_thk = [x for x in self.cleat_list_thk if x != self.cleat.designation]
            # if not self.cleat_list_thk:
            #     self.design_status = False
            # else:
            #     self.select_bolt_dia_beam(self)
            self.design_status = False
        else:
            pass

        if self.spting_leg.length <= self.cleat.leg_a_length and self.spting_leg.design_status is True:
            # self.spting_leg.end_dist_provided = self.cleat.leg_a_length - self.cleat.thickness - self.cleat.root_radius - \
            #                                     self.spting_leg.end_dist_provided
            self.spting_leg.cleat_angle_check(self.spting_leg.height, self.cleat.thickness, self.spting_leg.bolts_one_line,
                                   self.spting_leg.bolt_line, self.spting_leg.gauge_provided,
                                   self.spting_leg.edge_dist_provided, self.spting_leg.pitch_provided,
                                   self.spting_leg.end_dist_provided, self.bolt2.dia_hole, self.spting_leg.fu,
                                   self.spting_leg.fy, self.spting_leg.moment_demand, self.max_plate_height,
                                   self.load.shear_force * 1000)
        else:
            if self.spting_leg.reason == "":
                self.spting_leg.reason = (": Req leg length is {} and available leg size of cleat angle is {}"
                                        .format(self.spting_leg.length, self.cleat.leg_a_length))
            self.spting_leg.design_status = False

        if self.spting_leg.design_status is False:
            self.design_status = False
            # logger.error(self.spting_leg.reason)

        else:
            self.design_status = True
            self.supporting_leg_check = True

        return self.supporting_leg_check

    def get_bolt_PC(self):
        print(self.design_status, "Getting bolt grade")
        self.sptd_bolt_conn_plates_t_fu_fy = []
        self.sptd_bolt_conn_plates_t_fu_fy.append((2 * self.cleat.thickness, self.sptd_leg.fu, self.sptd_leg.fy))
        self.sptd_bolt_conn_plates_t_fu_fy.append(
            (self.supported_section.web_thickness, self.supported_section.fu, self.supported_section.fy))

        self.spting_bolt_conn_plates_t_fu_fy = []
        self.spting_bolt_conn_plates_t_fu_fy.append((self.cleat.thickness, self.sptd_leg.fu, self.sptd_leg.fy))
        if self.connectivity == VALUES_CONN_1[0]:
            self.spting_bolt_conn_plates_t_fu_fy.append((self.supporting_section.flange_thickness,
                                                         self.supporting_section.fu, self.supporting_section.fy))
        else:
            self.spting_bolt_conn_plates_t_fu_fy.append((self.supporting_section.web_thickness,
                                                         self.supporting_section.fu, self.supporting_section.fy))


        self.l_j_sptd = self.sptd_leg.gauge_provided * (self.sptd_leg.bolts_one_line - 1)
        self.t_sum_sptd = self.supported_section.web_thickness + 2 * self.cleat.thickness
        self.l_j_spting = self.spting_leg.gauge_provided * (self.spting_leg.bolts_one_line - 1)
        if self.connectivity == VALUES_CONN_1[0]:
            self.t_sum_spting = self.supporting_section.flange_thickness + self.cleat.thickness
        else:
            self.t_sum_spting = self.supporting_section.web_thickness + self.cleat.thickness

        self.beta_lj_sptd = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided, self.l_j_sptd)

        self.beta_lj_spting = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided,
                                                                     self.l_j_spting)
        if self.bolt.bolt_type == TYP_BEARING:
            self.beta_lg_sptd = IS800_2007.cl_10_3_3_2_bolt_large_grip(self.bolt.bolt_diameter_provided,
                                                                       self.t_sum_sptd, self.l_j_sptd)
            self.beta_lg_spting = IS800_2007.cl_10_3_3_2_bolt_large_grip(self.bolt.bolt_diameter_provided,
                                                                         self.t_sum_spting, self.l_j_spting)
        else:
            self.beta_lg_sptd = 1.0
            self.beta_lg_spting = 1.0
        bolt_PC_previous = self.bolt.bolt_PC_provided
        for self.bolt.bolt_PC_provided in reversed(self.bolt.bolt_grade):
            # print(self.bolt.bolt_grade)
            self.bolt2.bolt_PC_provided = self.bolt.bolt_PC_provided
            # print(self.bolt2.bolt_PC_provided)
            count = 1
            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_PC_provided,
                                              conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                              n_planes=2, e=self.sptd_leg.edge_dist_provided, p=self.sptd_leg.gauge_provided)


            self.bolt2.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                               bolt_grade_provided=self.bolt.bolt_PC_provided,
                                               conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,
                                               n_planes=1, e=self.spting_leg.edge_dist_provided, p=self.spting_leg.gauge_provided)
            # print(self.bolt.bolt_capacity, self.sptd_leg.bolt_force, self.bolt2.bolt_capacity, self.spting_leg.bolt_force)

            if (self.bolt.bolt_capacity * self.beta_lj_sptd * self.beta_lg_sptd < self.sptd_leg.bolt_force
                    or self.bolt2.bolt_capacity * self.beta_lj_spting * self.beta_lg_spting < self.spting_leg.bolt_force):
                self.bolt.bolt_PC_provided = bolt_PC_previous
                self.bolt2.bolt_PC_provided = bolt_PC_previous
                self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                  bolt_grade_provided=self.bolt.bolt_PC_provided,
                                                  conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                                  n_planes=2, e=self.sptd_leg.edge_dist_provided, p=self.sptd_leg.gauge_provided)
                self.bolt2.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                   bolt_grade_provided=self.bolt.bolt_PC_provided,
                                                   conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,
                                                   n_planes=1, e=self.spting_leg.edge_dist_provided, p=self.spting_leg.gauge_provided)
                break
            bolt_PC_previous = self.bolt.bolt_PC_provided
            count += 1
        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,n=2)
        self.bolt2.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,n=1)
        self.bolt_capacity_disp_sptd = round((self.bolt.bolt_capacity * self.beta_lj_sptd * self.beta_lg_sptd)/1000, 2)
        self.bolt_capacity_disp_spting = round((self.bolt2.bolt_capacity * self.beta_lj_spting * self.beta_lg_spting)/1000, 2)


    def for_3D_view(self):
        self.design_status = True
        self.cleat = Angle(designation=self.cleat.designation,material_grade=self.cleat_material_grade)
        self.cleat.gauge_sptd = self.sptd_leg.gauge_provided
        self.cleat.pitch_sptd = self.sptd_leg.pitch_provided
        self.cleat.edge_sptd = self.sptd_leg.edge_dist_provided
        # self.cleat.end_sptd = self.sptd_leg.end_dist_provided
        print(self.sptd_leg.gap, self.cleat.thickness +self.cleat.root_radius)
        self.cleat.end_sptd =self.cleat.leg_a_length - max(self.sptd_leg.gap, self.cleat.thickness +self.cleat.root_radius)\
                             - self.sptd_leg.end_dist_provided - self.cleat.gauge_sptd*(self.sptd_leg.bolt_line-1)
        self.cleat.bolt_lines_sptd = self.sptd_leg.bolt_line
        self.cleat.bolt_one_line_sptd = self.sptd_leg.bolts_one_line

        self.cleat.gauge_spting = self.spting_leg.gauge_provided
        self.cleat.pitch_spting = self.spting_leg.pitch_provided
        self.cleat.edge_spting = self.spting_leg.edge_dist_provided
        # self.cleat.end_spting = self.spting_leg.end_dist_provided
        self.cleat.end_spting = self.cleat.leg_a_length - self.cleat.thickness - self.cleat.root_radius - \
                                self.spting_leg.end_dist_provided - self.cleat.gauge_spting*(self.spting_leg.bolt_line-1)
        self.cleat.bolt_lines_spting = self.spting_leg.bolt_line
        self.cleat.bolt_one_line_spting = self.spting_leg.bolts_one_line

        self.cleat.height = max(self.spting_leg.height, self.sptd_leg.height)
        self.cleat.gap = self.sptd_leg.gap
        logger.debug("=== End Of Design ===")

    def save_design(self, popup_summary):
        super(CleatAngleConnection, self).save_design(self)
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")
        if self.cleat_list_thk:
            self.report_cleat_angle = {KEY_DISP_SEC_PROFILE: "equaldp",
                                       # Image shall be save with this name.png in resource files
                                       KEY_DISP_SECSIZE_REPORT: self.cleat.designation,
                                       KEY_DISP_MATERIAL: self.cleat.material,
                                       KEY_DISP_FU: round(self.cleat.fu, 2),
                                       KEY_DISP_FY: round(self.cleat.fy, 2),
                                      KEY_REPORT_MASS: round(self.cleat.mass, 2),
                                       KEY_REPORT_AREA: round((self.cleat.area / 100), 2),
                                       KEY_REPORT_MAX_LEG_SIZE: round(self.cleat.max_leg, 2),
                                       KEY_REPORT_MIN_LEG_SIZE: round(self.cleat.min_leg, 2),
                                       KEY_REPORT_ANGLE_THK: round(self.cleat.thickness, 2),
                                       KEY_REPORT_R1: round(self.cleat.root_radius, 2),
                                       KEY_REPORT_R2: round(self.cleat.toe_radius, 2),
                                       KEY_REPORT_CY: round(self.cleat.Cy, 2),
                                       KEY_REPORT_CZ: round(self.cleat.Cz, 2),
                                       KEY_REPORT_IZ: round(self.cleat.mom_inertia_z / 10000, 2),
                                       KEY_REPORT_IY: round(self.cleat.mom_inertia_y / 10000, 2),
                                       KEY_REPORT_IU: round(self.cleat.mom_inertia_u / 10000, 2),
                                       KEY_REPORT_IV: round(self.cleat.mom_inertia_v / 10000, 2),
                                       KEY_REPORT_RZ: round(self.cleat.rad_of_gy_z / 10, 2),
                                       KEY_REPORT_RY: round((self.cleat.rad_of_gy_y) / 10, 2),
                                       KEY_REPORT_RU: round((self.cleat.rad_of_gy_u) / 10, 2),
                                       KEY_REPORT_RV: round((self.cleat.rad_of_gy_v) / 10, 2),
                                       KEY_REPORT_ZEZ: round(self.cleat.elast_sec_mod_z / 1000, 2),
                                       KEY_REPORT_ZEY: round(self.cleat.elast_sec_mod_y / 1000, 2),
                                       KEY_REPORT_ZPZ: round(self.cleat.plast_sec_mod_z / 1000, 2),
                                       KEY_REPORT_ZPY: round(self.cleat.elast_sec_mod_y / 1000, 2)}
        else:
            self.report_cleat_angle = {}

        self.report_input = \
            {KEY_MAIN_MODULE: self.mainmodule,
            KEY_MODULE: self.module,
             KEY_CONN: self.connectivity,
             KEY_DISP_SHEAR: self.load.shear_force,
             "Supporting Section - Mechanical Properties": "TITLE",
             "Supporting Section Details": self.report_supporting,

             "Supported Section - Mechanical Properties": "TITLE",
             "Supported Section Details": self.report_supported,

             "Bolt Details - Input and Design Preference": "TITLE",
             KEY_DISP_D: str([int(d) for d in self.bolt.bolt_diameter]),
             KEY_DISP_GRD: str([float(d) for d in self.bolt.bolt_grade]),
             KEY_DISP_TYP: self.bolt.bolt_type,
             KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
             KEY_DISP_DP_BOLT_SLIP_FACTOR_REPORT: self.bolt.mu_f,

             "Detailing - Design Preference": "TITLE",
             KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
             KEY_DISP_GAP: self.sptd_leg.gap,
             KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM: self.bolt.corrosive_influences,
             KEY_DISP_CLEAT_ANGLE_LIST: str(self.cleat_list),
             "Selected Section Details": self.report_cleat_angle
             }
        if not self.cleat_list_thk:
            self.report_input.pop("Selected Section Details")
        self.report_check = []

        t1 = ('Selected', 'Selected Member Data', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
        self.report_check.append(t1)

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']



        if not self.cleat_list_thk:
            t1 = ('SubSection', 'Minimum Plate Thickness Check', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t1 = (DISP_MIN_PLATE_THICK, min_plate_thk_req(self.supported_section.web_thickness),
                  self.thickness_list,'Fail')
            self.report_check.append(t1)
            t1 = ('Available Length on Supporting Section', self.available_length,
                  self.leg_lengths, 'Fail')
            self.report_check.append(t1)

        elif self.supported_section.design_status is True:
            t1 = ('SubSection', 'Initial Section Check', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            a = self.supported_section
            h = a.web_height
            t = a.web_thickness
            t1 = (KEY_DISP_SHEAR_YLD, self.load.shear_force,
                  cl_8_4_shear_yielding_capacity_member(h, t, a.fy, gamma_m0,
                                                        round(a.shear_yielding_capacity / 1000, 2)),
                  get_pass_fail(self.load.shear_force, round(a.shear_yielding_capacity / 1000, 2), relation="lesser"))
            self.report_check.append(t1)

            t1 = (KEY_DISP_ALLOW_SHEAR, self.load.shear_force,
                  allow_shear_capacity(round(a.shear_yielding_capacity / 1000, 2),
                                       round(a.low_shear_capacity / 1000, 2)),
                  get_pass_fail(self.load.shear_force, round(a.low_shear_capacity / 1000, 2), relation="lesser"))
            self.report_check.append(t1)

            t1 = ('SubSection', 'Load Consideration', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            min_shear_load = min(40, round(0.15 * self.supported_section.shear_yielding_capacity / 0.6, 2))
            applied_shear_force = max(self.load.shear_force, min_shear_load)

            t1 = (KEY_DISP_APPLIED_SHEAR_LOAD, self.load.shear_force,
                  prov_shear_load(shear_input=self.load.shear_force, min_sc=min_shear_load,
                                  app_shear_load=applied_shear_force,
                                  shear_capacity_1=round(self.supported_section.shear_yielding_capacity / 1000, 2)), "")
            self.report_check.append(t1)


            for leg in [self.sptd_leg, self.spting_leg]:
                if self.sptd_leg.design_status == False and leg == self.spting_leg:
                    continue
                if leg == self.sptd_leg:
                    t1 = ('SubSection', 'Bolt Design - Connected to Beam', '|p{3cm}|p{5.5cm}|p{6cm}|p{1.5cm}|')
                    connecting_plates = [self.cleat.thickness, self.supported_section.web_thickness]
                    all_connecting_plates_tk = [i[0] for i in self.sptd_bolt_conn_plates_t_fu_fy]
                    bolt=self.bolt
                    bolt_shear_capacity_kn = round(self.bolt.bolt_shear_capacity / 1000, 2)
                    if self.bolt.bolt_type == "Bearing Bolt":
                        bolt_bearing_capacity_kn = round(self.bolt.bolt_bearing_capacity / 1000, 2)
                    bolt_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2)
                    bolt_force_kn = round(self.sptd_leg.bolt_force / 1000, 2)
                    bolt_capacity_red_kn = self.bolt_capacity_disp_sptd
                    n_planes=2
                    beta_lj = self.beta_lj_sptd
                    beta_lg = self.beta_lg_sptd
                else:
                    t1 = ('SubSection', 'Bolt Design - Connected to Column', '|p{3.5cm}|p{5cm}|p{6cm}|p{1.5cm}|')
                    if self.connectivity == VALUES_CONN_2[0]:
                        connecting_plates = [self.cleat.thickness, self.supporting_section.web_thickness]
                    else:
                        connecting_plates = [self.cleat.thickness, self.supporting_section.flange_thickness]
                    bolt=self.bolt2
                    all_connecting_plates_tk = [i[0] for i in self.spting_bolt_conn_plates_t_fu_fy]
                    bolt_shear_capacity_kn = round(self.bolt2.bolt_shear_capacity / 1000, 2)
                    if self.bolt2.bolt_bearing_capacity != 'N/A':
                        bolt_bearing_capacity_kn = round(self.bolt2.bolt_bearing_capacity / 1000, 2)

                    bolt_capacity_kn = round(self.bolt2.bolt_capacity / 1000, 2)
                    bolt_force_kn = round(self.spting_leg.bolt_force / 1000, 2)
                    bolt_capacity_red_kn = self.bolt_capacity_disp_spting
                    n_planes=1
                    beta_lj = self.beta_lj_spting
                    beta_lg = self.beta_lg_spting
                self.report_check.append(t1)
                t1 = (KEY_DISP_D, '', bolt.bolt_diameter_provided, '')
                self.report_check.append(t1)
                t1 = (KEY_DISP_GRD, '', bolt.bolt_grade_provided, '')
                self.report_check.append(t1)
                t1 = (KEY_DISP_CLEATANGLE, '',self.cleat.designation,'')
                self.report_check.append(t1)
                t6 = (DISP_NUM_OF_COLUMNS, '', leg.bolt_line, '')
                self.report_check.append(t6)
                t7 = (DISP_NUM_OF_ROWS, '', leg.bolts_one_line, '')
                self.report_check.append(t7)
                t1 = (DISP_MIN_PITCH, cl_10_2_2_min_spacing(bolt.bolt_diameter_provided,'pitch'),
                      leg.gauge_provided,
                      get_pass_fail(bolt.min_pitch, leg.gauge_provided, relation='leq'))
                self.report_check.append(t1)
                # if leg.design_status is True:
                t1 = (DISP_MAX_PITCH, cl_10_2_3_1_max_spacing(connecting_plates,'pitch'),
                      leg.gauge_provided,
                      get_pass_fail(bolt.max_spacing, leg.gauge_provided, relation='geq'))
                self.report_check.append(t1)
                t2 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(bolt.bolt_diameter_provided,'gauge'),
                      leg.pitch_provided if leg.pitch_provided > 0 else 'N/A',
                      get_pass_fail(bolt.min_gauge, leg.pitch_provided, relation="leq"))
                self.report_check.append(t2)
                t2 = (DISP_MAX_GAUGE, cl_10_2_3_1_max_spacing(connecting_plates,'gauge'),
                      leg.pitch_provided if leg.pitch_provided > 0 else 'N/A',
                      get_pass_fail(bolt.max_spacing, leg.pitch_provided, relation="geq"))
                self.report_check.append(t2)
                t3 = (DISP_MIN_END, cl_10_2_4_2_min_edge_end_dist(d_0=bolt.dia_hole,
                                                                  edge_type=bolt.edge_type, parameter='end_dist'),
                      leg.edge_dist_provided,
                      get_pass_fail(bolt.min_end_dist, leg.edge_dist_provided, relation='leq'))
                self.report_check.append(t3)
                if leg == self.sptd_leg:
                    t4 = (DISP_MAX_END,
                          cl_10_2_4_3_max_edge_end_dist(self.bolt.single_conn_plates_t_fu_fy, bolt.corrosive_influences,
                                                        parameter='end_dist'),
                          leg.edge_dist_provided,
                          get_pass_fail(bolt.max_end_dist, leg.edge_dist_provided, relation='geq'))
                    self.report_check.append(t4)
                else:
                    t4 = (DISP_MAX_END,
                          cl_10_2_4_3_max_edge_end_dist(self.bolt2.single_conn_plates_t_fu_fy, bolt.corrosive_influences,
                                                        parameter='end_dist'),
                          leg.edge_dist_provided,
                          get_pass_fail(bolt.max_end_dist, leg.edge_dist_provided, relation='geq'))
                    self.report_check.append(t4)
                t3 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(d_0=bolt.dia_hole,
                                                                   edge_type=bolt.edge_type,
                                                                   parameter='edge_dist'),
                      leg.end_dist_provided,
                      get_pass_fail(bolt.min_edge_dist, leg.end_dist_provided, relation='leq'))
                self.report_check.append(t3)
                if leg == self.sptd_leg:
                    t4 = (DISP_MAX_EDGE,
                          cl_10_2_4_3_max_edge_end_dist(self.bolt.single_conn_plates_t_fu_fy, bolt.corrosive_influences,
                                                        parameter='edge_dist'),
                          leg.end_dist_provided,
                          get_pass_fail(bolt.max_edge_dist, leg.end_dist_provided, relation="geq"))
                else:
                    t4 = (DISP_MAX_EDGE,
                          cl_10_2_4_3_max_edge_end_dist(self.bolt2.single_conn_plates_t_fu_fy,
                                                        bolt.corrosive_influences,
                                                        parameter='edge_dist'),
                          leg.end_dist_provided,
                          get_pass_fail(bolt.max_edge_dist, leg.end_dist_provided, relation="geq"))
                self.report_check.append(t4)


                if self.sptd_leg.reason == "Minimum end/edge distance is greater than max end/edge distance." or\
                        self.sptd_leg.reason == "Can't fit two bolts in one line. Select lower diameter." or \
                        self.sptd_leg.reason == "Minimum pitch/gauge distance is greater than max pitch/gauge distance.":
                    pass
                else:
                    if leg == self.sptd_leg:
                        ecc = max(self.sptd_leg.gap, self.cleat.thickness + self.cleat.root_radius) + \
                              self.sptd_leg.end_dist_provided+self.sptd_leg.pitch_provided*(self.sptd_leg.bolt_line-1)/2

                        leg.get_vres(leg.bolts_one_line, leg.pitch_provided, leg.gauge_provided, leg.bolt_line,
                                     self.load.shear_force, self.load.axial_force,
                                     ecc=ecc, web_moment=0.0)
                        t10 = (KEY_OUT_REQ_MOMENT_DEMAND_BOLT, '', moment_demand_req_bolt_force(
                            shear_load=round(self.load.shear_force, 2),
                            web_moment=0.0, ecc=leg.ecc,
                            moment_demand=round(leg.moment_demand, 2)), '')
                    else:
                        print("ecc",self.spting_leg.end_dist_provided + self.cleat.thickness + self.cleat.root_radius)
                        ecc = self.spting_leg.end_dist_provided + self.cleat.thickness + self.cleat.root_radius + \
                              self.spting_leg.pitch_provided * (self.spting_leg.bolt_line-1)/2
                        leg.get_vres(leg.bolts_one_line, leg.pitch_provided, leg.gauge_provided, leg.bolt_line,
                                     self.load.shear_force/2, self.load.axial_force/2,
                                     ecc=ecc, web_moment=0.0)
                        t10 = (KEY_OUT_REQ_MOMENT_DEMAND_BOLT, '', moment_demand_req_bolt_force(
                            shear_load=round(self.load.shear_force/2, 2),
                            web_moment=0.0, ecc=leg.ecc,
                            moment_demand=round(leg.moment_demand, 2)), '')

                    self.report_check.append(t10)

                    t10 = (KEY_OUT_REQ_PARA_BOLT, parameter_req_bolt_force(bolts_one_line=leg.bolts_one_line
                                                                           , gauge=leg.gauge_provided,
                                                                           ymax=round(leg.ymax, 2),
                                                                           xmax=round(leg.xmax, 2),
                                                                           bolt_line=leg.bolt_line,
                                                                           pitch=leg.pitch_provided,
                                                                           length_avail=leg.length_avail,
                                                                           conn='fin'), '', '')
                    self.report_check.append(t10)

                    t10 = (KEY_OUT_BOLT_FORCE, Vres_bolts(bolts_one_line=leg.bolts_one_line,
                                                          ymax=round(leg.ymax, 2),
                                                          xmax=round(leg.xmax, 2),
                                                          bolt_line=leg.bolt_line,
                                                          shear_load=round(self.load.shear_force, 2),
                                                          axial_load=round(self.load.axial_force, 2),
                                                          moment_demand=round(leg.moment_demand, 2),
                                                          r=round(leg.sigma_r_sq / 1000, 2),
                                                          vbv=round(leg.vbv, 2),
                                                          tmv=round(leg.tmv, 2),
                                                          tmh=round(leg.tmh, 2),
                                                          abh=round(leg.abh, 2),
                                                          vres=round(leg.bolt_force / 1000, 2)), '', '')
                    self.report_check.append(t10)
                    # else:
                    #     t3 = (KEY_OUT_BOLT_FORCE, force_in_bolt_due_to_load(P=round(self.load.shear_force, 2),
                    #                                                                 n=leg.bolts_one_line*leg.bolt_line,
                    #                                                                 T_ba=round(leg.bolt_force / 1000, 2),
                    #                                                                 load='shear'),'','')
                    #     self.report_check.append(t3)
                    if bolt.bolt_type == TYP_BEARING:

                        t1 = (KEY_OUT_DISP_BOLT_SHEAR, '',
                              cl_10_3_3_bolt_shear_capacity(bolt.bolt_fu, n_planes, bolt.bolt_net_area,
                                                            bolt.gamma_mb, bolt_shear_capacity_kn), '')
                        self.report_check.append(t1)
                        t8 = (KEY_DISP_KB, " ",
                              cl_10_3_4_calculate_kb(leg.edge_dist_provided, leg.gauge_provided,
                                                     bolt.dia_hole,
                                                     bolt.bolt_fu, bolt.fu_considered), '')
                        self.report_check.append(t8)
                        t2 = (KEY_OUT_DISP_BOLT_BEARING, '',
                              cl_10_3_4_bolt_bearing_capacity(bolt.kb, bolt.bolt_diameter_provided,
                                                              self.sptd_bolt_conn_plates_t_fu_fy, bolt.gamma_mb,
                                                              bolt_bearing_capacity_kn), '')
                        self.report_check.append(t2)
                        t3 = (KEY_OUT_DISP_BOLT_CAPACITY, '',
                              cl_10_3_2_bolt_capacity(bolt_shear_capacity_kn, bolt_bearing_capacity_kn, bolt_capacity_kn),
                              '')
                        self.report_check.append(t3)
                    else:
                        kh_disp = round(bolt.kh, 2)
                        t4 = (KEY_OUT_DISP_BOLT_SLIP, '',
                              cl_10_4_3_HSFG_bolt_capacity(mu_f=bolt.mu_f, n_e=1, K_h=kh_disp, fub=bolt.bolt_fu,
                                                           Anb=bolt.bolt_net_area, gamma_mf=bolt.gamma_mf,
                                                           capacity=bolt_capacity_kn), '')
                        self.report_check.append(t4)


                    t10 = (KEY_OUT_LONG_JOINT, '',
                           cl_10_3_3_1_long_joint_bolted_prov(leg.bolt_line, leg.bolts_one_line,
                                                              leg.pitch_provided, leg.gauge_provided,
                                                              bolt.bolt_diameter_provided, bolt_capacity_kn,
                                                              bolt_capacity_red_kn, 'n_r'), "")
                    self.report_check.append(t10)
                    if self.bolt.bolt_type == TYP_BEARING:
                        if leg.grip_status == True:
                            grip_remarks = "Pass"
                        else:
                            grip_remarks = "Fail"
                    else:
                        grip_remarks = "N/A"
                    t10 = (KEY_OUT_LARGE_GRIP, '',
                           cl_10_3_3_2_large_grip_bolted_prov(sum(all_connecting_plates_tk),self.bolt.bolt_diameter_provided, beta_lg), grip_remarks)
                    self.report_check.append(t10)
                    if leg.grip_status == True:
                        t13 = (KEY_OUT_BOLT_CAPACITY_REDUCED, '',bolt_red_capacity_prov(beta_lj, beta_lg,bolt_capacity_kn,
                                                                                        bolt_capacity_red_kn,'b'),
                               "")
                        self.report_check.append(t13)

                        t5 = (KEY_OUT_DISP_BOLT_CAPACITY, bolt_force_kn, bolt_capacity_red_kn,
                              get_pass_fail(bolt_force_kn, bolt_capacity_red_kn, relation="lesser"))
                        self.report_check.append(t5)

            # if self.sptd_leg.design_status == True:
            ###################
            # Cleat angle checks
            ###################

            if self.sptd_leg.grip_status== True and self.spting_leg.grip_status == True:
                t1 = ('SubSection', 'Cleat Angle Check', '|p{3.5cm}|p{7.0cm}|p{4.5cm}|p{1cm}|')
                self.report_check.append(t1)

                t1 = (DISP_MIN_CLEAT_HEIGHT, min_plate_ht_req(self.supported_section.depth, self.supported_section.root_radius,
                                                              self.supported_section.flange_thickness,self.min_plate_height),
                      self.sptd_leg.height,
                      get_pass_fail(self.min_plate_height, self.sptd_leg.height, relation="leq"))
                self.report_check.append(t1)
                if self.connectivity == VALUES_CONN_1:
                    t1 = (DISP_MAX_CLEAT_HEIGHT, max_plate_ht_req(self.connectivity, self.supported_section.depth,
                                                                  self.supported_section.flange_thickness,
                                                                  self.supported_section.root_radius,
                                                                  self.supported_section.notch_ht,
                                                                  self.max_plate_height), self.sptd_leg.height,
                          get_pass_fail(self.max_plate_height, self.sptd_leg.height, relation="greater"))
                    self.report_check.append(t1)
                else:
                    t1 = (DISP_MAX_CLEAT_HEIGHT, max_plate_ht_req(self.connectivity, self.supporting_section.depth,
                                                                  self.supporting_section.flange_thickness,
                                                                  self.supporting_section.root_radius,
                                                                  0.0,
                                                                  self.max_plate_height), self.sptd_leg.height,
                          get_pass_fail(self.max_plate_height, self.sptd_leg.height, relation="greater"))
                    self.report_check.append(t1)
                additional_length = max(self.sptd_leg.gap, self.cleat.thickness+self.cleat.root_radius)
                min_plate_length = additional_length + 2 * self.bolt.min_end_dist + \
                                   (self.sptd_leg.bolt_line - 1) * self.bolt.min_pitch
                t1 = (DISP_MIN_LEG_LENGTH + ' (on supported leg)', min_angle_leg_length(self.bolt.min_pitch, self.bolt.min_end_dist,self.sptd_leg.gap,
                                                                                     self.cleat.thickness,self.cleat.root_radius,
                                                                 self.sptd_leg.bolt_line, min_plate_length),
                      self.cleat.leg_a_length,
                      get_pass_fail(min_plate_length, self.cleat.leg_a_length, relation="lesser"))
                self.report_check.append(t1)
                min_plate_length = max(min_plate_length,2 * self.bolt2.min_end_dist + \
                                   (self.spting_leg.bolt_line - 1) * self.bolt2.min_pitch)
                t1 = (DISP_MIN_LEG_LENGTH + ' (on supporting leg)', min_angle_leg_length(self.bolt.min_pitch, self.bolt.min_end_dist,0.0,
                                                                                     self.cleat.thickness,self.cleat.root_radius,
                                                                 max(1,self.spting_leg.bolt_line), min_plate_length),
                      self.cleat.leg_a_length,
                      get_pass_fail(min_plate_length, self.cleat.leg_a_length, relation="lesser"))
                self.report_check.append(t1)

                t1 = (DISP_MIN_CLEAT_THK, min_plate_thk_req(self.supported_section.web_thickness,0.5),
                      self.cleat.thickness,
                      get_pass_fail(self.supported_section.web_thickness*0.5, self.cleat.thickness,
                                    relation="lesser"))
                self.report_check.append(t1)

                if self.sptd_leg.design_status == True:
                    if self.design_status == True:
                        h = self.cleat.height
                        t = self.cleat.thickness
                    elif self.spting_leg.height > 0 and self.spting_leg.thickness_provided > 0:
                        h = max(self.sptd_leg.height, self.spting_leg.height)
                        t = max(self.sptd_leg.thickness_provided,self.spting_leg.thickness_provided)
                    else:
                        h = self.sptd_leg.height
                        t = self.sptd_leg.thickness_provided
                    cleat_plastic_section_modulus = 2 * h ** 2 * t / 4
                    t1 = (KEY_DISP_SHEAR_YLD, '', cl_8_4_shear_yielding_capacity_member(h, t, self.cleat.fy, gamma_m0,
                                                                                        round(self.sptd_leg.cleat_shear_capacity/1000,2),2), '')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_PLATE_BLK_SHEAR_SHEAR, '',
                          cl_6_4_blockshear_capacity_member(Tdb=round(self.sptd_leg.block_shear_capacity / 1000, 2),
                                                            stress='shear'), '')
                    self.report_check.append(t1)
                    cleat_shear_capacity = min(self.sptd_leg.cleat_shear_capacity,self.sptd_leg.block_shear_capacity)
                    t1 = (KEY_DISP_SHEAR_CAPACITY, self.load.shear_force,
                          cl_8_4_shear_capacity_member(round(self.sptd_leg.cleat_shear_capacity / 1000,2),
                                                       0.0,
                                                       round(self.sptd_leg.block_shear_capacity / 1000, 2),'full'),
                          get_pass_fail(self.load.shear_force, round(cleat_shear_capacity / 1000, 2), relation="lesser"))
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_PLATE_MOM_CAPACITY, round(self.sptd_leg.moment_demand/1000, 2),
                          cl_8_2_1_2_plastic_moment_capacity_member(beta_b=1.0, Z_p=round(cleat_plastic_section_modulus, 2),
                                                                    f_y=self.cleat.fy,
                                                                    gamma_m0=gamma_m0,
                                                                    Pmc=round(self.sptd_leg.cleat_moment_capacity/1000000,2)),
                          get_pass_fail(self.sptd_leg.moment_demand, self.sptd_leg.cleat_moment_capacity, relation="lesser"))
                    self.report_check.append(t1)

        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = str(sys.path[0])
        rel_path = os.path.abspath(".") # TEMP
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_2d_image, Disp_3D_image, module=self.module)
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     folder = r'C:\Users\Deepthi\Desktop\OsdagWorkspace'
#     # # folder_path = r'C:\Users\Win10\Desktop'
#     # folder_path = r'C:\Users\pc\Desktop'
#     # window = MainController(Ui_ModuleWindow, FinPlateConnection, folder_path)
#     from ...gui.ui_template import Ui_ModuleWindow
#     ui2 = Ui_ModuleWindow()
#     ui2.setupUi(ui2, CleatAngleConnection, folder)
#     ui2.show()
#     # app.exec_()
#     # sys.exit(app.exec_())
#     try:
#         sys.exit(app.exec_())
#     except BaseException as e:
#         print("ERROR", e)
