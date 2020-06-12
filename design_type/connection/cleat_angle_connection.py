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
        self.sptng_leg_length = 0.0
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

        t3 = ("Bolt", TYPE_TEXTBOX, [KEY_DP_BOLT_MATERIAL_G_O])
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

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_MATERIAL_G_O, KEY_DP_BOLT_SLIP_FACTOR,
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

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        if "36" in c: c.remove("36")
        return c

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

    def sptng_spacing(self, status):

        sptng_spacing = []

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.sptng_leg.pitch_provided if status else '')
        sptng_spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.sptng_leg.end_dist_provided if status else '')
        sptng_spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.sptng_leg.gauge_provided if status else '')
        sptng_spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.sptng_leg.edge_dist_provided if status else '')
        sptng_spacing.append(t12)

        return sptng_spacing

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

        t12 = (None, DISP_OUT_TITLE_SPTNGLEG, TYPE_TITLE, None, True)
        out_list.append(t12)

        t13 = (KEY_OUT_SPTNG_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
              round(self.sptng_bolt.bolt_shear_capacity / 1000, 2) if flag else '', True)
        out_list.append(t13)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not 'N/A':
                bolt_bearing_capacity_disp = round(self.sptng_bolt.bolt_bearing_capacity / 1000, 2)
            else:
                bolt_bearing_capacity_disp = self.sptng_bolt.bolt_bearing_capacity

        t14 = (KEY_OUT_SPTNG_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_SPTNG_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
              round(self.sptng_bolt.bolt_capacity / 1000, 2) if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_SPTNG_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX,
              round(self.sptng_leg.bolt_force / 1000, 2) if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_SPTNG_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.sptng_leg.bolt_line if flag else '', True)
        out_list.append(t17)

        t18 = (
        KEY_OUT_SPTNG_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.sptng_leg.bolts_one_line if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_SPTNG_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.sptng_spacing], True)
        out_list.append(t19)

        t20 = (None, DISP_OUT_TITLE_CLEAT, TYPE_TITLE, None, True)
        out_list.append(t20)

        t15 = (KEY_OUT_CLEAT_HEIGHT, KEY_OUT_DISP_CLEAT_HEIGHT, TYPE_TEXTBOX, self.sptd_leg.height if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_CLEAT_SPTDLEG, KEY_OUT_DISP_CLEAT_SPTDLEG, TYPE_TEXTBOX, self.cleat.leg_a_length if flag else '', True)
        out_list.append(t16)

        t16 = (KEY_OUT_CLEAT_SPTNGLEG, KEY_OUT_DISP_CLEAT_SPTNGLEG, TYPE_TEXTBOX, self.cleat.leg_b_length if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_CLEAT_SHEAR, KEY_OUT_DISP_CLEAT_SPTNGLEG, TYPE_TEXTBOX, round(self.sptd_leg.shear_yielding_capacity,2) if flag else '', True)
        out_list.append(t17)

        t18 = (KEY_OUT_CLEAT_BLK_SHEAR, KEY_DISP_BLK_SHEAR, TYPE_TEXTBOX, round(self.sptd_leg.block_shear_capacity,2) if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_CLEAT_BLK_SHEAR, KEY_DISP_MOM_DEMAND, TYPE_TEXTBOX, round(self.sptd_leg.moment_demand/1000000,2) if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_CLEAT_MOM_CAPACITY, KEY_DISP_MOM_CAPACITY, TYPE_TEXTBOX, round(self.sptd_leg.moment_capacity,2) if flag else '', True)
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
        # self.sptng_leg = self.sptd_leg


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
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.type == "Rolled":
                length = self.supported_section.depth
            else:
                length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        else:
            length = self.supported_section.depth - 50.0  # TODO: Subtract notch height for beam-beam connection

        self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)

        print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
              self.supported_section.tension_yielding_capacity, self.load.axial_force)

        if self.supported_section.shear_yielding_capacity > self.load.shear_force:
            logger.info("preliminary member check is satisfactory. Checking if possible Bolt Diameters are available")
            self.select_bolt_dia(self)

        else:
            self.design_status = False
            logger.error(" : shear yielding capacity {} is less "
                         "than applied loads, Please select larger sections or decrease loads"
                            .format(self.supported_section.shear_yielding_capacity))
            print("failed in preliminary member checks. Select larger sections or decrease loads")

    def select_bolt_dia(self):

        self.min_plate_height = self.supported_section.min_plate_height()
        self.max_plate_height = self.supported_section.max_plate_height(self.connectivity, 50.0)


        self.sptd_leg.thickness_provided = min(self.sptd_leg.thickness)

        bolts_required_previous = 2
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        count = 0

        self.sptd_bolt_conn_plates_t_fu_fy = []
        self.sptd_bolt_conn_plates_t_fu_fy.append((2*self.sptd_leg.thickness_provided, self.sptd_leg.fu, self.sptd_leg.fy))
        self.sptd_bolt_conn_plates_t_fu_fy.append((self.supported_section.web_thickness, self.supported_section.fu, self.supported_section.fy))

        bolt_prev = self.bolt
        sptd_leg_prev = self.sptd_leg
        # while considering eccentricity, distance from bolt line to supporting member will be,
        # end_dist+gap or end_dist+root_radius+cleat_thickness
        # since we don't have root radius and thickness values we are considering r_r = thickness
        # since final thickness may be more than assumed minimum thickness,
        # we are assuming r_r + cleat thickness = 3*min available cleat thickness

        self.end_to_sptng = max((self.sptd_leg.gap, self.sptd_leg.thickness_provided * 3))

        available_length = (self.supporting_section.flange_width - self.supported_section.web_thickness) / 2
        for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy)

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                              n_planes=2)

            self.sptd_leg.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                             web_plate_h_min=self.min_plate_height,
                                             web_plate_h_max=self.max_plate_height,
                                             bolt_capacity=self.bolt.bolt_capacity,
                                             min_edge_dist=self.bolt.min_edge_dist_round,
                                             min_gauge=self.bolt.min_gauge_round,
                                             max_spacing=self.bolt.max_spacing_round,
                                             max_edge_dist=self.bolt.max_edge_dist_round,
                                             shear_load=self.load.shear_force * 1000,
                                             gap=self.end_to_sptng,
                                             shear_ecc=True, bolt_line_limit=3)
            if self.connectivity in VALUES_CONN_1:
                if self.sptd_leg.length > available_length:
                    logger.info(": {}rows {}columns {}mm diameter bolts needs leg length of {}"
                                .format(self.sptd_leg.bolts_one_line,self.sptd_leg.bolt_line,
                                        self.bolt.bolt_diameter_provided,self.sptd_leg.length))
                    logger.info(": Available width on flange side is {}".format(available_length))
                    count = 0
                    continue
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
        if self.sptd_leg.length > available_length:
            self.sptd_leg.reason = (": Req leg length is {} and Available width on flange side is {}"
                                    .format(self.sptd_leg.length,available_length))
            self.sptd_leg.design_status = False

        if self.sptd_leg.design_status is False:
            self.design_status = False
            logger.error(self.sptd_leg.reason)

        else:
            self.get_bolt_grade(self)

    def get_bolt_grade(self):
        print(self.design_status, "Getting bolt grade")
        bolt_prev = self.bolt
        for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
            count = 1

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.sptd_bolt_conn_plates_t_fu_fy,
                                              n_planes=2)

            print(self.bolt.bolt_grade_provided, self.bolt.bolt_capacity, self.sptd_leg.bolt_force)

            bolt_capacity_reduced = self.sptd_leg.get_bolt_red(self.sptd_leg.bolts_one_line,
                                                            self.sptd_leg.gauge_provided, self.sptd_leg.bolt_line,
                                                               self.sptd_leg.pitch_provided,self.bolt.bolt_capacity,
                                                            self.bolt.bolt_diameter_provided)

            if bolt_capacity_reduced < self.sptd_leg.bolt_force and count >= 1:
                self.bolt = bolt_prev
                break
            bolt_prev = self.bolt
            count += 1

        self.bolt.design_status = True
        self.sptd_leg_length = self.sptd_leg.length + self.end_to_sptng
        print(self.cleat_list,self.sptd_leg.length)
        self.cleat_list = get_available_cleat_list(self.cleat_list, min_leg_length=self.sptd_leg.length,position="inner")
        print(self.sptd_leg)
        if self.cleat_list:
            print(self.design_status, "getting supporting leg details")
            self.get_sptng_leg_details(self)
        else:
            self.design_status = False
            logger.error(" : min required leg length is {}".format(self.sptd_leg_length))

    def get_sptng_leg_details(self):

        self.sptng_bolt_conn_plates_t_fu_fy = []
        if self.connectivity in VALUES_CONN_1:
            self.sptng_bolt_conn_plates_t_fu_fy.append((self.sptd_leg.thickness_provided, self.sptd_leg.fu, self.sptd_leg.fy))
            self.sptng_bolt_conn_plates_t_fu_fy.append((self.supporting_section.flange_thickness, self.supporting_section.fu, self.supporting_section.fy))
        else:
            self.sptng_bolt_conn_plates_t_fu_fy.append((self.sptd_leg.thickness_provided, self.sptd_leg.fu, self.sptd_leg.fy))
            self.sptd_bolt_conn_plates_t_fu_fy.append((self.supporting_section.web_thickness, self.supporting_section.fu, self.supporting_section.fy))
        self.sptng_bolt = self.bolt
        self.sptng_leg = self.sptd_leg
        self.end_to_sptd = self.sptng_leg.thickness_provided * 3
        if self.cleat_list:
            self.sptng_bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.sptng_bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.sptng_bolt_conn_plates_t_fu_fy)

            self.sptng_bolt.calculate_bolt_capacity(bolt_diameter_provided=self.sptng_bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.sptng_bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.sptng_bolt_conn_plates_t_fu_fy,
                                              n_planes=1)

            self.sptng_leg.get_web_plate_details(bolt_dia=self.sptng_bolt.bolt_diameter_provided,
                                                web_plate_h_min=self.sptd_leg.height,
                                                web_plate_h_max=self.sptd_leg.height,
                                                bolt_capacity=self.sptng_bolt.bolt_capacity,
                                                min_edge_dist=self.sptng_bolt.min_edge_dist_round,
                                                min_gauge=self.sptng_bolt.min_gauge_round,
                                                max_spacing=self.sptng_bolt.max_spacing_round,
                                                max_edge_dist=self.sptng_bolt.max_edge_dist_round,
                                                shear_load=self.load.shear_force * 1000/2,
                                                gap=self.end_to_sptd,
                                                shear_ecc=True, bolt_line_limit=3)


        if self.sptng_leg.design_status is False:
            self.design_status = False
            logger.error(self.sptng_leg.reason)

        else:
            self.sptng_leg_length = self.sptng_leg.length + self.end_to_sptng
            print(self.cleat_list,self.sptng_leg.length)
            self.cleat_list = get_available_cleat_list(self.cleat_list, min_leg_length=self.sptng_leg.length,position="inner")
            if not self.cleat_list:
                self.design_status = False
                logger.error(" : min required leg length is {}".format(self.sptng_leg_length))
            else:
                self.select_cleat_angle(self)

    def select_cleat_angle(self):
        self.min_plate_height = self.supported_section.min_plate_height()
        self.max_plate_height = self.supported_section.max_plate_height()
        for self.cleat_angle_selected in self.cleat_list:

            self.cleat = Angle(designation=self.cleat_angle_selected, material_grade=self.cleat_material_grade)





        designation_angle = self.cleat_list[0]
        self.cleat = Angle(designation=designation_angle, material_grade=self.cleat_material_grade)
        self.for_3D_view(self)

    def for_3D_view(self):
        self.design_status = True
        self.cleat.gauge_sptd = self.sptd_leg.gauge_provided
        self.cleat.pitch_sptd = self.sptd_leg.pitch_provided
        self.cleat.edge_sptd = self.sptd_leg.edge_dist_provided
        self.cleat.end_sptd = self.sptd_leg.end_dist_provided
        self.cleat.bolt_lines_sptd = self.sptd_leg.bolt_line
        self.cleat.bolt_one_line_sptd = self.sptd_leg.bolts_one_line

        self.cleat.gauge_sptng = self.sptng_leg.gauge_provided
        self.cleat.pitch_sptng = self.sptng_leg.pitch_provided
        self.cleat.edge_sptng = self.sptng_leg.edge_dist_provided
        self.cleat.end_sptng = self.sptng_leg.end_dist_provided
        self.cleat.bolt_lines_sptng = self.sptng_leg.bolt_line
        self.cleat.bolt_one_line_sptng = self.sptng_leg.bolts_one_line

        self.cleat.height = max(self.sptng_leg.height,self.sptd_leg.height)
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
        # self.cleat.gauge_sptng = 60.0
        # self.cleat.pitch_sptng = 0.0
        # self.cleat.edge_sptng = 44.0
        # self.cleat.end_sptng = 44.0
        # self.cleat.bolt_lines_sptng = 1
        # self.cleat.bolt_one_line_sptng = 3
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    folder = r'C:\Users\Deepthi\Desktop\OsdagWorkspace'
    # # folder_path = r'C:\Users\Win10\Desktop'
    # folder_path = r'C:\Users\pc\Desktop'
    # window = MainController(Ui_ModuleWindow, FinPlateConnection, folder_path)
    from gui.ui_template import Ui_ModuleWindow
    ui2 = Ui_ModuleWindow()
    ui2.setupUi(ui2, CleatAngleConnection, folder)
    ui2.show()
    # app.exec_()
    # sys.exit(app.exec_())
    try:
        sys.exit(app.exec_())
    except BaseException as e:
        print("ERROR", e)
