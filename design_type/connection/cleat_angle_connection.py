from design_type.connection.shear_connection import ShearConnection
from utils.common.component import *
from utils.common.component import Bolt, Plate, Weld
from Common import *
import sys

from utils.common.load import Load
import logging

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

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, './ResourceFiles/images/fin_cf_bw.png', True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, VALUES_COLSEC, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, VALUES_BEAMSEC, True, 'No Validator')
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
            return VALUES_BEAMSEC
        elif conn in VALUES_CONN_2:
            return VALUES_SECBM
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

        t6 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t6)

        return lst


    def spacing(self, status):

        spacing = []

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.sptd_leg.pitch_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.sptd_leg.end_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.sptd_leg.gauge_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.sptd_leg.edge_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def spting_spacing(self, status):

        spting_spacing = []

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.spting_leg.pitch_provided if status else '')
        spting_spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.spting_leg.end_dist_provided if status else '')
        spting_spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.spting_leg.gauge_provided if status else '')
        spting_spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.spting_leg.edge_dist_provided if status else '')
        spting_spacing.append(t12)

        return spting_spacing

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
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair

        out_list = []

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_diameter_provided if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_grade_provided if flag else '', True)

        out_list.append(t3)

        t4 = (None, DISP_OUT_TITLE_SPTDLEG, TYPE_TITLE, None, True)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  round(self.bolt.bolt_shear_capacity/1000,2) if flag else '', True)
        out_list.append(t5)
        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not 'N/A':
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
            else:
                bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t6 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX, round(self.bolt.bolt_capacity/1000,2) if flag else '', True)
        out_list.append(t7)

        t8 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX, round(self.sptd_leg.bolt_force / 1000, 2) if flag else '', True)
        out_list.append(t8)

        t9 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.sptd_leg.bolt_line if flag else '', True)
        out_list.append(t9)

        t10 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.sptd_leg.bolts_one_line if flag else '', True)
        out_list.append(t10)

        t11 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t11)

        t12 = (None, DISP_OUT_TITLE_SPTINGLEG, TYPE_TITLE, None, True)
        out_list.append(t12)

        t13 = (KEY_OUT_SPTING_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
              round(self.bolt2.bolt_shear_capacity / 1000, 2) if flag else '', True)
        out_list.append(t13)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not 'N/A':
                bolt_bearing_capacity_disp = round(self.bolt2.bolt_bearing_capacity / 1000, 2)
            else:
                bolt_bearing_capacity_disp = self.bolt2.bolt_bearing_capacity

        t14 = (KEY_OUT_SPTING_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_SPTING_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
              round(self.bolt2.bolt_capacity / 1000, 2) if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_SPTING_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX,
              round(self.spting_leg.bolt_force / 1000, 2) if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_SPTING_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.spting_leg.bolt_line if flag else '', True)
        out_list.append(t17)

        t18 = (
        KEY_OUT_SPTING_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.spting_leg.bolts_one_line if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_SPTING_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spting_spacing], True)
        out_list.append(t19)

        t20 = (None, DISP_OUT_TITLE_CLEAT, TYPE_TITLE, None, True)
        out_list.append(t20)

        t15 = (KEY_OUT_CLEAT_HEIGHT, KEY_OUT_DISP_CLEAT_HEIGHT, TYPE_TEXTBOX, self.sptd_leg.height if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_CLEAT_SPTDLEG, KEY_OUT_DISP_CLEAT_SPTDLEG, TYPE_TEXTBOX, self.cleat.leg_a_length if flag else '', True)
        out_list.append(t16)

        t16 = (KEY_OUT_CLEAT_SPTINGLEG, KEY_OUT_DISP_CLEAT_SPTINGLEG, TYPE_TEXTBOX, self.cleat.leg_b_length if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_CLEAT_SHEAR, KEY_OUT_DISP_CLEAT_SPTINGLEG, TYPE_TEXTBOX, round(self.sptd_leg.shear_yielding_capacity,2) if flag else '', True)
        out_list.append(t17)

        t18 = (KEY_OUT_CLEAT_BLK_SHEAR, KEY_DISP_BLK_SHEAR, TYPE_TEXTBOX, round(self.sptd_leg.block_shear_capacity,2) if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_CLEAT_BLK_SHEAR, KEY_DISP_MOM_DEMAND, TYPE_TEXTBOX, round(self.sptd_leg.moment_demand/1000000,2) if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_CLEAT_MOM_CAPACITY, KEY_DISP_MOM_CAPACITY, TYPE_TEXTBOX, round(self.sptd_leg.cl_8_2_moment_capacity_member, 2) if flag else '', True)
        out_list.append(t20)

        return out_list


    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
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

        self.sptd_leg = Plate(material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.spting_leg = Plate(material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],gap=design_dictionary[KEY_DP_DETAILING_GAP])

        logger.info("Input values are set. Checking if angle of required thickness is available")

        self.check_available_cleat_thk(self)


    def check_available_cleat_thk(self):
        self.sptd_leg.thickness = []

        min_thickness = self.supported_section.web_thickness / 2
        for designation in self.cleat_list:
            cleat = Angle(designation=designation,material_grade=self.cleat_material_grade)
            if cleat.thickness*2 <= self.supported_section.web_thickness:
                self.cleat_list.pop()
                print("popped", designation)
                print(self.cleat_list)
            else:
                if cleat.thickness not in self.sptd_leg.thickness:
                    self.sptd_leg.thickness.append(cleat.thickness)
                    print("added", designation,self.sptd_leg.thickness)

        if self.cleat_list:
            logger.info("Required cleat thickness available. Doing preliminary member checks")
            self.member_capacity(self)
        else:
            logger.error("Cleat Angle should have minimum thickness of %2.2f" % min_thickness)

    def member_capacity(self):
        super(CleatAngleConnection, self).member_capacity(self)

        if self.supported_section.shear_yielding_capacity / 1000 > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity / 1000 > self.load.axial_force:

            if self.load.shear_force <= min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                            40.0):
                logger.warning(" : User input for shear force is very less compared to section capacity. "
                               "Setting Shear Force value to 15% of supported beam shear capacity or 40kN, whichever is less.")
                self.load.shear_force = min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                            40.0)

            print("preliminary member check is satisfactory. Checking available Bolt Diameters")
            self.select_bolt_dia_beam(self)

        else:
            self.design_status = False
            if self.supported_section.shear_yielding_capacity / 1000 < self.load.shear_force:
                logger.error(" : Shear yielding capacity, {} kN is less "
                             "than shear force, Please select larger sections or decrease loads"
                             .format(round(self.supported_section.shear_yielding_capacity/1000, 2)))
            else:
                logger.error(" : Tension yielding capacity, {} kN is less "
                             "than axial force, Please select larger sections or decrease loads"
                             .format(round(self.supported_section.tension_yielding_capacity/1000, 2)))
            print("failed in preliminary member checks. Select larger sections or decrease loads")

    def select_bolt_dia_beam(self):
        self.supported_section.notch_ht = max((round_up(self.supporting_section.flange_thickness
                                                        + self.supporting_section.root_radius, 5) + 10),
                                              (round_up(self.supported_section.flange_thickness
                                                        + self.supported_section.root_radius, 5) + 10))
        self.min_plate_height = self.supported_section.min_plate_height()
        self.max_plate_height = round(self.supported_section.max_plate_height(self.connectivity,
                                                                              self.supported_section.notch_ht),2)

        if self.connectivity == VALUES_CONN_1[0]:
            available_length = (self.supporting_section.flange_width - self.supported_section.web_thickness) / 2
        else:
            available_length = (self.supporting_section.depth - 2 * self.supporting_section.flange_thickness -
                                2 * self.supporting_section.root_radius - self.supported_section.web_thickness) / 2

        for designation in self.cleat_list:
            cleat = Angle(designation=designation,material_grade=self.cleat_material_grade)
            if cleat.leg_a_length > available_length:
                self.cleat_list.pop()
                # print("popped", designation)
                # print(self.cleat_list)
            # else:
            #     if cleat.thickness not in self.sptd_leg.thickness:
            #         self.sptd_leg.thickness.append(cleat.thickness)
            #         print("added", designation,self.sptd_leg.thickness)

        for self.cleatAngle in self.cleat_list:
            self.cleat = Angle(designation=self.cleatAngle, material_grade=self.cleat_material_grade)
            # self.sptd_leg.thickness_provided = min(self.sptd_leg.thickness)
            self.sptd_leg.thickness_provided = self.cleat.thickness
            bolts_required_previous = 2
            self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
            count = 0

            self.sptd_bolt_conn_plates_t_fu_fy = []
            self.sptd_bolt_conn_plates_t_fu_fy.append((2*self.sptd_leg.thickness_provided, self.sptd_leg.fu, self.sptd_leg.fy))
            self.sptd_bolt_conn_plates_t_fu_fy.append((self.supported_section.web_thickness, self.supported_section.fu, self.supported_section.fy))

            bolt_prev = self.bolt
            sptd_leg_prev = self.sptd_leg

            """
            # while considering eccentricity, distance from bolt line to supporting member will be,
            # end_dist+gap or end_dist+root_radius+cleat_thickness
            # 
            """

            self.end_to_sptd = max(self.sptd_leg.gap, self.cleat.thickness + self.cleat.root_radius)

            for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
                self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                        conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy)

                self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                  bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                  conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                                  n_planes=2)
                print("Suptd bolt capacity: ", self.bolt.bolt_capacity)
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
                                                 shear_ecc=True, bolt_line_limit=2)
                if self.connectivity in VALUES_CONN_1:
                    if self.sptd_leg.length > self.cleat.leg_a_length:
                        self.sptd_leg.design_status = False
                        logger.info(": {}rows {}columns {}mm diameter bolts needs leg length of {}"
                                    .format(self.sptd_leg.bolts_one_line, self.sptd_leg.bolt_line,
                                            self.bolt.bolt_diameter_provided, self.sptd_leg.length))
                        logger.info(": Available width on flange side is {}".format(self.cleat.leg_a_length))
                        count = 0
                        continue
                    else:
                        self.sptd_leg.design_status = True
                print(1, self.sptd_leg.bolt_force, self.bolt.bolt_capacity, self.bolt.bolt_diameter_provided,
                      self.sptd_leg.bolts_required, self.sptd_leg.bolts_one_line)
                if self.sptd_leg.design_status is True:
                    if self.sptd_leg.bolts_required > bolts_required_previous and count >= 1:
                        self.bolt = bolt_prev
                        self.sptd_leg = sptd_leg_prev
                        break
                    sptd_leg_prev = self.sptd_leg
                    bolt_prev = self.bolt
                    count += 1
                else:
                    pass
            if self.sptd_leg.length > self.cleat.leg_a_length:
                self.sptd_leg.reason = (": Req leg length is {} and Available width on flange side is {}"
                                        .format(self.sptd_leg.length, self.cleat.leg_a_length))
                self.sptd_leg.design_status = False

        if self.sptd_leg.design_status is False:
            self.design_status = False
            logger.error(self.sptd_leg.reason)

        else:
            self.select_bolt_dia_supporting(self)

    def select_bolt_dia_supporting(self):

        self.sptd_leg.thickness_provided_supporting = self.cleat.thickness

        # bolts_required_previous = self.sptd_leg.bolts_required
        # count = 0

        self.spting_bolt_conn_plates_t_fu_fy = []
        self.spting_bolt_conn_plates_t_fu_fy.append((self.cleat.thickness, self.sptd_leg.fu, self.sptd_leg.fy))
        if self.connectivity == VALUES_CONN_1[0]:
            self.spting_bolt_conn_plates_t_fu_fy.append((self.supporting_section.flange_thickness,
                                                       self.supporting_section.fu, self.supporting_section.fy))
        else:
            self.spting_bolt_conn_plates_t_fu_fy.append((self.supporting_section.web_thickness,
                                                       self.supporting_section.fu, self.supporting_section.fy))

        # bolt_prev = self.bolt
        # spting_leg_prev = self.sptd_leg
        """     
        # while considering eccentricity, distance from bolt line to supporting member will be,
        # end_dist+gap or end_dist+root_radius+cleat_thickness
        #
        """

        self.end_to_spting = self.cleat.thickness + self.cleat.root_radius

        if self.connectivity == VALUES_CONN_1[0]:
            available_length = (self.supporting_section.flange_width - self.supported_section.web_thickness) / 2
        else:
            available_length = (self.supporting_section.depth - 2 * self.supporting_section.flange_thickness -
                                2 * self.supporting_section.root_radius - self.supported_section.web_thickness) / 2

        self.bolt2 = Bolt()
        self.bolt2 = self.bolt
        self.bolt2.bolt_grade_provided = self.bolt.bolt_grade_provided
        self.bolt2.bolt_diameter_provided = self.bolt.bolt_diameter_provided
        self.bolt2.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt2.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy)
        print("Bolt Prop: ", self.bolt2.bolt_diameter_provided, self.bolt2.bolt_grade_provided, self.spting_bolt_conn_plates_t_fu_fy)
        self.bolt2.calculate_bolt_capacity(bolt_diameter_provided=self.bolt2.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt2.bolt_grade_provided,
                                          conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,
                                          n_planes=1)
        print("Supting bolt capacity: ", self.bolt2.bolt_capacity, self.sptd_leg.bolts_one_line, self.sptd_leg.bolt_line)
        self.spting_leg.get_web_plate_details(bolt_dia=self.bolt2.bolt_diameter_provided,
                                         web_plate_h_min=self.min_plate_height,
                                         web_plate_h_max=self.max_plate_height,
                                         bolt_capacity=self.bolt2.bolt_capacity,
                                         min_edge_dist=self.bolt2.min_edge_dist_round,
                                         min_gauge=self.bolt2.min_gauge_round,
                                         max_spacing=self.bolt2.max_spacing_round,
                                         max_edge_dist=self.bolt2.max_edge_dist_round,
                                         shear_load=self.load.shear_force * 1000 / 2,
                                         gap=self.end_to_spting,
                                         shear_ecc=True, bolt_line_limit=2,
                                         min_bolts_one_line=self.sptd_leg.bolts_one_line,
                                         min_bolt_line=self.sptd_leg.bolt_line)
        if self.spting_leg.length > self.cleat.leg_a_length:
            logger.info(": {}rows {}columns {}mm diameter bolts needs leg length of {}"
                        .format(self.spting_leg.bolts_one_line, self.spting_leg.bolt_line,
                                self.bolt2.bolt_diameter_provided, self.spting_leg.length))
            logger.info(": Available width of selected cleat angle leg is {}".format(self.cleat.leg_a_length))
            count = 0
            # continue
        print("Supporting leg side: ", self.spting_leg.design_status, self.spting_leg.bolt_force, self.bolt2.bolt_capacity,
              self.bolt2.bolt_diameter_provided, self.spting_leg.bolts_required, self.spting_leg.bolts_one_line)
        if self.spting_leg.design_status is False and self.cleat_list:
            self.cleat_list = [x for x in self.cleat_list if x != self.cleat.designation]
            if not self.cleat_list:
                self.design_status = False
            else:
                self.select_bolt_dia_beam(self)
            # if self.sptd_leg.bolts_required > bolts_required_previous and count >= 1:
            #     self.bolt2 = bolt_prev
            #     self.spting_leg = spting_leg_prev
                # break
            # spting_leg_prev = self.spting_leg
            # bolt_prev = self.bolt2
            # count += 1
        # elif not self.cleat_list:
        #     self.design_status = False
        else:
            pass

        if self.spting_leg.length > self.cleat.leg_a_length:
            self.spting_leg.reason = (": Req leg length is {} and available leg size of cleat angle is {}"
                                    .format(self.spting_leg.length, self.cleat.leg_a_length))
            self.spting_leg.design_status = False

        if self.spting_leg.design_status is False:
            self.design_status = False
            logger.error(self.spting_leg.reason)

        else:
            self.design_status = True
            self.get_bolt_grade(self)

    def get_bolt_grade(self):
        print(self.design_status, "Getting bolt grade")
        # bolt_prev = self.bolt

        bolt_PC_previous = self.bolt.bolt_grade[-1]
        for self.bolt.bolt_PC_provided in reversed(self.bolt.bolt_grade):
            print(self.bolt.bolt_grade)
            self.bolt2.bolt_PC_provided = self.bolt.bolt_PC_provided
            print(self.bolt2.bolt_PC_provided)
            count = 1
            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_PC_provided,
                                              conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                              n_planes=2)
            self.bolt2.calculate_bolt_capacity(bolt_diameter_provided=self.bolt2.bolt_diameter_provided,
                                               bolt_grade_provided=self.bolt2.bolt_PC_provided,
                                               conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,
                                               n_planes=1)
            print(self.bolt.bolt_capacity, self.sptd_leg.bolt_force, self.bolt2.bolt_capacity, self.spting_leg.bolt_force)
            if self.bolt.bolt_capacity < self.sptd_leg.bolt_force \
                    or self.bolt2.bolt_capacity < self.spting_leg.bolt_force:
                self.bolt.bolt_PC_provided = bolt_PC_previous
                self.bolt2.bolt_PC_provided = bolt_PC_previous
                self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                  bolt_grade_provided=self.bolt.bolt_PC_provided,
                                                  conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                                  n_planes=2)
                self.bolt2.calculate_bolt_capacity(bolt_diameter_provided=self.bolt2.bolt_diameter_provided,
                                                   bolt_grade_provided=self.bolt2.bolt_PC_provided,
                                                   conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,
                                                   n_planes=1)
                break
            bolt_PC_previous = self.bolt.bolt_PC_provided
            count += 1

        #
        #
        #
        #
        # for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
        #     count = 1
        #
        #     self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
        #                                       bolt_grade_provided=self.bolt.bolt_grade_provided,
        #                                       conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
        #                                       n_planes=2)
        #
        #     print(self.bolt.bolt_grade_provided, self.bolt.bolt_capacity, self.sptd_leg.bolt_force)
        #
        #     bolt_capacity_reduced = self.sptd_leg.get_bolt_red(self.sptd_leg.bolts_one_line,
        #                                                     self.sptd_leg.gauge_provided, self.sptd_leg.bolt_line,
        #                                                        self.sptd_leg.pitch_provided,self.bolt.bolt_capacity,
        #                                                     self.bolt.bolt_diameter_provided)
        #
        #     if bolt_capacity_reduced < self.sptd_leg.bolt_force and count >= 1:
        #         self.bolt = bolt_prev
        #         break
        #     bolt_prev = self.bolt
        #     count += 1
        #
        # self.bolt.design_status = True
        # self.sptd_leg_length = self.sptd_leg.length + self.end_to_spting
        # print(self.cleat_list,self.sptd_leg.length)
        # self.cleat_list = get_available_cleat_list(self.cleat_list, min_leg_length=self.sptd_leg.length,position="inner")
        # print(self.sptd_leg)
        # if self.cleat_list:
        #     print(self.design_status, "getting supporting leg details")
        #     self.get_spting_leg_details(self)
        # else:
        #     self.design_status = False
        #     logger.error(" : min required leg length is {}".format(self.sptd_leg_length))

    # def get_spting_leg_details(self):
    #
    #     self.spting_bolt_conn_plates_t_fu_fy = []
    #     if self.connectivity in VALUES_CONN_1:
    #         self.spting_bolt_conn_plates_t_fu_fy.append((self.sptd_leg.thickness_provided, self.sptd_leg.fu, self.sptd_leg.fy))
    #         self.spting_bolt_conn_plates_t_fu_fy.append((self.supporting_section.flange_thickness, self.supporting_section.fu, self.supporting_section.fy))
    #     else:
    #         self.spting_bolt_conn_plates_t_fu_fy.append((self.sptd_leg.thickness_provided, self.sptd_leg.fu, self.sptd_leg.fy))
    #         self.sptd_bolt_conn_plates_t_fu_fy.append((self.supporting_section.web_thickness, self.supporting_section.fu, self.supporting_section.fy))
    #     self.spting_bolt = self.bolt
    #     self.spting_leg = self.sptd_leg
    #     self.end_to_sptd = self.spting_leg.thickness_provided * 3
    #     if self.cleat_list:
    #         self.bolt2.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt2.bolt_diameter_provided,
    #                                                 conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy)
    #
    #         self.bolt2.calculate_bolt_capacity(bolt_diameter_provided=self.bolt2.bolt_diameter_provided,
    #                                           bolt_grade_provided=self.bolt2.bolt_grade_provided,
    #                                           conn_plates_t_fu_fy=self.spting_bolt_conn_plates_t_fu_fy,
    #                                           n_planes=1)
    #
    #         self.spting_leg.get_web_plate_details(bolt_dia=self.bolt2.bolt_diameter_provided,
    #                                             web_plate_h_min=self.sptd_leg.height,
    #                                             web_plate_h_max=self.sptd_leg.height,
    #                                             bolt_capacity=self.bolt2.bolt_capacity,
    #                                             min_edge_dist=self.bolt2.min_edge_dist_round,
    #                                             min_gauge=self.bolt2.min_gauge_round,
    #                                             max_spacing=self.bolt2.max_spacing_round,
    #                                             max_edge_dist=self.bolt2.max_edge_dist_round,
    #                                             shear_load=self.load.shear_force * 1000/2,
    #                                             gap=self.end_to_sptd,
    #                                             shear_ecc=True, bolt_line_limit=3)
    #
    #
    #     if self.spting_leg.design_status is False:
    #         self.design_status = False
    #         logger.error(self.spting_leg.reason)
    #
    #     else:
    #         self.spting_leg_length = self.spting_leg.length + self.end_to_spting
    #         print(self.cleat_list,self.spting_leg.length)
    #         self.cleat_list = get_available_cleat_list(self.cleat_list, min_leg_length=self.spting_leg.length,position="inner")
    #         if not self.cleat_list:
    #             self.design_status = False
    #             logger.error(" : min required leg length is {}".format(self.spting_leg_length))
    #         else:
    #             self.select_cleat_angle(self)
    #
    # def select_cleat_angle(self):
    #     self.min_plate_height = self.supported_section.min_plate_height()
    #     self.max_plate_height = self.supported_section.max_plate_height()
    #     for self.cleat_angle_selected in self.cleat_list:
    #
    #         self.cleat = Angle(designation=self.cleat_angle_selected, material_grade=self.cleat_material_grade)
    #
    #
    #
    #
    #
    #     designation_angle = self.cleat_list[0]
    #     self.cleat = Angle(designation=designation_angle, material_grade=self.cleat_material_grade)
        self.for_3D_view(self)

    def for_3D_view(self):
        self.design_status = True
        self.cleat.gauge_sptd = self.sptd_leg.gauge_provided
        self.cleat.pitch_sptd = self.sptd_leg.pitch_provided
        self.cleat.edge_sptd = self.sptd_leg.edge_dist_provided
        self.cleat.end_sptd = self.cleat.leg_a_length - self.cleat.thickness - self.cleat.root_radius - self.sptd_leg.end_dist_provided
        self.cleat.bolt_lines_sptd = self.sptd_leg.bolt_line
        self.cleat.bolt_one_line_sptd = self.sptd_leg.bolts_one_line

        self.cleat.gauge_spting = self.spting_leg.gauge_provided
        self.cleat.pitch_spting = self.spting_leg.pitch_provided
        self.cleat.edge_spting = self.spting_leg.edge_dist_provided
        self.cleat.end_spting = self.cleat.leg_a_length - self.cleat.thickness - self.cleat.root_radius - self.spting_leg.end_dist_provided
        self.cleat.bolt_lines_spting = self.spting_leg.bolt_line
        self.cleat.bolt_one_line_spting = self.spting_leg.bolts_one_line

        self.cleat.height = max(self.spting_leg.height,self.sptd_leg.height)
        # self.cleat.leg_a_length = 100.0
        # self.cleat.leg_b_length = 150.0
        # self.cleat.thickness = 8.0
        # self.cleat.r1 = 8.5
        # self.cleat.r2 = 4.5
        # self.bolt.bolt_diameter_provided = 12.0
        self.cleat.gap = 10.0
        # self.design_status = True
        # self.cleat.gauge_sptd = 60.0
        # self.cleat.pitch_sptd = 0.0
        # self.cleat.edge_sptd = 44.0
        # self.cleat.end_sptd = 44.0
        # self.cleat.bolt_lines_sptd = 1
        # self.cleat.bolt_one_line_sptd = 3
        #
        # self.cleat.gauge_spting = 60.0
        # self.cleat.pitch_spting = 0.0
        # self.cleat.edge_spting = 44.0
        # self.cleat.end_spting = 44.0
        # self.cleat.bolt_lines_spting = 1
        # self.cleat.bolt_one_line_spting = 3
        #
        # self.cleat.height = 208.0
        # self.cleat.leg_a_length = 100.0
        # self.cleat.leg_b_length = 150.0
        #
        # self.cleat.thickness = 8.0
        # self.cleat.r1 = 8.5
        # self.cleat.r2 = 4.5
        # self.bolt.bolt_diameter_provided = 12.0
        # self.cleat.gap = 10.0

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     folder = r'C:\Users\Deepthi\Desktop\OsdagWorkspace'
#     # # folder_path = r'C:\Users\Win10\Desktop'
#     # folder_path = r'C:\Users\pc\Desktop'
#     # window = MainController(Ui_ModuleWindow, FinPlateConnection, folder_path)
#     from gui.ui_template import Ui_ModuleWindow
#     ui2 = Ui_ModuleWindow()
#     ui2.setupUi(ui2, CleatAngleConnection, folder)
#     ui2.show()
#     # app.exec_()
#     # sys.exit(app.exec_())
#     try:
#         sys.exit(app.exec_())
#     except BaseException as e:
#         print("ERROR", e)
