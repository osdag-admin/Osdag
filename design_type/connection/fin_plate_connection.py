from design_type.connection.shear_connection import ShearConnection

import time

from utils.common.component import Bolt, Plate, Weld
# from gui.ui_summary_popup import Ui_Dialog
from design_report.reportGenerator_latex import CreateLatex
from utils.common.component import *
#from cad.common_logic import CommonDesignLogic
from utils.common.material import *
from Common import *
from utils.common.load import Load
from Report_functions import *
import logging


#from ...gui.newnew import Ui_Form
#newnew_object = Ui_Form()

# connectivity = "column_flange_beam_web"
# supporting_member_section = "HB 400"
# supported_member_section = "MB 300"
# fy = 250.0
# fu = 410.0
# shear_force = 100.0
# axial_force=100.0
# bolt_diameter = 24.0
# bolt_type = "friction_grip"
# bolt_grade = 8.8
# plate_thickness = 10.0
# weld_size = 6
# material_grade = "E 250 (Fe 410 W)B"
# material = Material(material_grade)


class FinPlateConnection(ShearConnection):

    def __init__(self):
        super(FinPlateConnection, self).__init__()
        self.min_plate_height = 0.0
        self.max_plate_height = 0.0
        self.res_force = 0.0
        self.weld_connecting_plates=[]
        self.design_status = False

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # handler.setLevel(logging.INFO)
        # formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        if key is not None:
            handler = OurLog(key)
            # handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def module_name(self):
        return KEY_DISP_FINPLATE

    def input_values(self, existingvalues={}):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)

        e.g.
        t = (Key, Key_display, Type, existing_val, Current_Value, enabled/disabled, Validator_type)
        '''

        # @author: Amir, Umair
        self.module = KEY_DISP_FINPLATE
        print('Het I am existing values', existingvalues)

        options_list = []

        if KEY_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_CONN]
        else:
            existingvalue_key_conn = ''

        if KEY_SUPTNGSEC in existingvalues:
           existingvalue_key_suptngsec = existingvalues[KEY_SUPTNGSEC]
        else:
            existingvalue_key_suptngsec = ''

        if KEY_SUPTDSEC in existingvalues:
            existingvalue_key_suptdsec = existingvalues[KEY_SUPTDSEC]
        else:
            existingvalue_key_suptdsec = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_SHEAR in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_SHEAR]
        else:
            existingvalue_key_versh = ''

        if KEY_AXIAL in existingvalues:
            existingvalue_key_axial = existingvalues[KEY_AXIAL]
        else:
            existingvalue_key_axial = ''

        if KEY_D in existingvalues:
            existingvalue_key_d = existingvalues[KEY_D]
        else:
            existingvalue_key_d = ''

        if KEY_TYP in existingvalues:
            existingvalue_key_typ = existingvalues[KEY_TYP]
        else:
            existingvalue_key_typ = ''

        if KEY_GRD in existingvalues:
            existingvalue_key_grd = existingvalues[KEY_GRD]
        else:
            existingvalue_key_grd = ''

        if KEY_PLATETHK in existingvalues:
            existingvalue_key_platethk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_platethk = ''

        t16 = (KEY_MODULE, KEY_DISP_FINPLATE, TYPE_MODULE, None, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN, True, 'No Validator')
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, "./ResourceFiles/images/fin_cf_bw.png", True, 'No Validator')
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, connectdb("Columns"), True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, connectdb("Beams"), True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t6)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None, True, 'Int Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None, True, 'Int Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK, True, 'No Validator')
        options_list.append(t14)

        return options_list

    def spacing(self, status):

        spacing = []

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def spacing_capacities(self, status):

        spacing_cap = []

        t99 = (None, 'Section', TYPE_SECTION, './ResourceFiles/images/Osdag.png')
        spacing_cap.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing_cap.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing_cap.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing_cap.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing_cap.append(t12)

        t99 = (None, 'Section2', TYPE_SECTION, './ResourceFiles/images/Osdag.png')
        spacing_cap.append(t99)

        t17 = (KEY_OUT_PLATE_SHEAR, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX,
               round(self.plate.shear_yielding_capacity, 2) if status else '')
        spacing_cap.append(t17)

        t18 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_OUT_DISP_PLATE_BLK_SHEAR, TYPE_TEXTBOX,
               round(self.plate.block_shear_capacity, 2) if status else '')
        spacing_cap.append(t18)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX,
               round(self.plate.moment_demand / 1000000, 2) if status else '')
        spacing_cap.append(t19)

        t20 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX,
               round(self.plate.moment_capacity / 1000000, 2) if status else '')
        spacing_cap.append(t20)

        return spacing_cap

    def capacities(self, status):

        capacities = []

        t17 = (KEY_OUT_PLATE_SHEAR, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX, round(self.plate.shear_yielding_capacity,2) if status else '')
        capacities.append(t17)

        t18 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_OUT_DISP_PLATE_BLK_SHEAR, TYPE_TEXTBOX, round(self.plate.block_shear_capacity,2) if status else '')
        capacities.append(t18)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX, round(self.plate.moment_demand/1000000,2) if status else '')
        capacities.append(t19)

        t20 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX, round(self.plate.moment_capacity/1000000,2) if status else '')
        capacities.append(t20)

        return capacities

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

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  round(self.bolt.bolt_shear_capacity/1000,2) if flag else '', True)
        out_list.append(t4)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
                pass
            else:
                bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX, round(self.bolt.bolt_capacity/1000,2) if flag else '', True)
        out_list.append(t6)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX, round(self.plate.bolt_force / 1000, 2) if flag else '', True)
        out_list.append(t21)

        t7 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.plate.bolt_line if flag else '', True)
        out_list.append(t7)

        t8 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.plate.bolts_one_line if flag else '', True)
        out_list.append(t8)

        t21 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t21)

        t21 = ('sample_key', 'Sample Button', TYPE_OUT_BUTTON, ['Spacing_Capacity Details', self.spacing_capacities], True)
        out_list.append(t21)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if flag else '', True)
        out_list.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if flag else '', True)
        out_list.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if flag else '', True)
        out_list.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if flag else '', True)
        out_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True)
        out_list.append(t13)

        t14 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.plate.thickness_provided if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.plate.height if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_LENGTH, TYPE_TEXTBOX, self.plate.length if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_PLATE_SHEAR, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX, round(self.plate.shear_yielding_capacity,2) if flag else '', True)
        out_list.append(t17)

        t18 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_OUT_DISP_PLATE_BLK_SHEAR, TYPE_TEXTBOX, round(self.plate.block_shear_capacity,2) if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX, round(self.plate.moment_demand/1000000,2) if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX, round(self.plate.moment_capacity/1000000,2) if flag else '', True)
        out_list.append(t20)

        # t22 = (KEY_OUT_PLATE_CAPACITIES, KEY_OUT_DISP_PLATE_CAPACITIES, TYPE_OUT_BUTTON, ['Capacity Details', self.capacities])
        # out_list.append(t22)

        t13 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t13)

        t14 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX, self.weld.size if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX, round(self.weld.strength,2) if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_WELD_STRESS, KEY_OUT_DISP_WELD_STRESS, TYPE_TEXTBOX, round(self.weld.stress,2) if flag else '', True)
        out_list.append(t16)

        return out_list

    def tab_list(self):

        tabs = []

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_column_section)
        tabs.append(t1)

        t2 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_beam_section)
        tabs.append(t2)

        t3 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t3)

        t4 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t4)

        t5 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t5)

        t6 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t6)

        t7 = ("Connector", TYPE_TAB_2, self.connector_values)
        tabs.append(t7)

        return tabs

    def func_for_validation(self, design_dictionary):
        all_errors = []
        self.design_status = False
        flag = False
        flag1 = False
        flag2=False
        option_list = self.input_values(self)
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    missing_fields_list.append(option[1])
            # elif option[2] == TYPE_MODULE:
            #     if design_dictionary[option[0]] == "Fin Plate":

        if design_dictionary[KEY_CONN] == VALUES_CONN_2[0]:
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

        elif design_dictionary[KEY_CONN] == VALUES_CONN_1[1]:
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

        selected_plate_thk = list(np.float_(design_dictionary[KEY_PLATETHK]))
        supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC],material_grade=design_dictionary[KEY_MATERIAL])
        available_plates = [i for i in selected_plate_thk if i >= supported_section.web_thickness]
        if not available_plates:
            error = "Plate thickness should be greater than suppported section web thicknesss."
            all_errors.append(error)
        else:
            flag2=True
        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        if flag and flag1 and flag2:
            self.set_input_values(self, design_dictionary)
        else:
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


    # def populate_tabs(self):
    #
    #     populate_tab_list = []
    #
    #     t1 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC, "Columns", KEY_MATERIAL], KEY_CONN, VALUES_CONN_1)
    #     populate_tab_list.append(t1)
    #
    #     t2 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC, "Beams", KEY_MATERIAL], KEY_CONN, VALUES_CONN_2)
    #     populate_tab_list.append(t2)
    #
    #     t3 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC, KEY_MATERIAL], None, None)
    #     populate_tab_list.append(t3)
    #
    #     t4 = ("Connector", [KEY_SUPTDSEC, KEY_MATERIAL], None, None)
    #     populate_tab_list.append(t4)
    #
    #     return populate_tab_list

    # def get_fu_fy(self):
    #     m = Material(self[0])
    #     fu = m.fu
    #     fy = m.fy
    #     d = {KEY_SUPTNGSEC_FU: fu,
    #          KEY_SUPTNGSEC_FY: fy,
    #          KEY_SUPTDSEC_FU: fu,
    #          KEY_SUPTDSEC_FY: fy,
    #          KEY_PLATE_FU: fu,
    #          KEY_PLATE_FY: fy}
    #
    #     return d

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

        print(design_dictionary)

        if design_dictionary[KEY_SUPTNGSEC_MATERIAL] == "Custom":
            design_dictionary[KEY_SUPTNGSEC_MATERIAL] = "Custom" + " " + str(design_dictionary[KEY_SUPTNGSEC_FU]) + " " \
                                                        + str(design_dictionary[KEY_SUPTNGSEC_FY])
        if design_dictionary[KEY_SUPTDSEC_MATERIAL] == "Custom":
            design_dictionary[KEY_SUPTDSEC_MATERIAL] = "Custom" + " " + str(design_dictionary[KEY_SUPTDSEC_FU]) + " " \
                                                        + str(design_dictionary[KEY_SUPTDSEC_FY])

        super(FinPlateConnection,self).set_input_values(self, design_dictionary)

        self.start_time = time.time()
        self.module = design_dictionary[KEY_MODULE]

        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_PLATE_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.plate.design_status_2 = False
        self.weld = Weld(material_grade=design_dictionary[KEY_MATERIAL],material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],fabrication = design_dictionary[KEY_DP_WELD_FAB])
        print("input values are set. Doing preliminary member checks")
        self.member_capacity(self)

        # if self.design_status:
        #     self.commLogicObj = CommonDesignLogic(window.display, window.folder, self.module, self.mainmodule)
        #     status = self.design_status
        #     self.commLogicObj.call_3DModel(status, FinPlateConnection)

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.type)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.type == "Rolled":
                self.supported_section.web_height = self.supported_section.depth
            else:
                self.supported_section.web_height = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        else:

            self.supported_section.web_height = self.supported_section.depth - self.supported_section.notch_ht

        A_g = self.supported_section.web_height * self.supported_section.web_thickness
        # 0.6 is multiplied for shear yielding capacity to keep the section in low shear
        self.supported_section.shear_yielding_capacity = 0.6*IS800_2007.cl_8_4_design_shear_strength(A_g,self.supported_section.fy)
        self.supported_section.tension_yielding_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g,self.supported_section.fy)

        print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
              self.supported_section.tension_yielding_capacity, self.load.axial_force)

        if self.supported_section.shear_yielding_capacity > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity > self.load.axial_force:

            print("preliminary member check is satisfactory. Checking available plate Thickness")
            self.thickness_possible = [i for i in self.plate.thickness if i >= self.supported_section.web_thickness]

            if not self.thickness_possible:
                logger.error(": Plate thickness should be greater than suppported section web thicknesss.")
            else:
                print("Selecting bolt diameter")
                self.select_bolt_dia(self)

        else:
            # self.design_status = False
            logger.warning(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
                           "than applied loads, Please select larger sections or decrease loads"
                            .format(self.supported_section.shear_yielding_capacity,
                                    self.supported_section.tension_yielding_capacity))
            print("failed in preliminary member checks. Select larger sections or decrease loads")
            self.thickness_possible = [i for i in self.plate.thickness if i >= self.supported_section.web_thickness]

            if not self.thickness_possible:
                logger.error(": Plate thickness should be greater than suppported section web thicknesss.")
            else:
                print("Selecting bolt diameter")
                self.select_bolt_dia(self)
            # self.select_bolt_dia(self)

    def select_bolt_dia(self):
        self.min_plate_height = self.supported_section.min_plate_height()
        self.max_plate_height = self.supported_section.max_plate_height(self.connectivity, 50.0)

        self.res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000

        self.plate.thickness_provided = min(self.thickness_possible)
        self.plate.connect_to_database_to_get_fy_fu(grade=self.plate.material,thickness=self.plate.thickness_provided)
        bolts_required_previous = 2
        bolt_diameter_previous = self.bolt.bolt_diameter[-1]
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        count = 0

        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
        self.bolt_conn_plates_t_fu_fy.append((self.supported_section.web_thickness, self.supported_section.fu, self.supported_section.fy))

        bolt_force_previous = 0.0


        for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=1)

            self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                             web_plate_h_min=self.min_plate_height,
                                             web_plate_h_max=self.max_plate_height,
                                             bolt_capacity=self.bolt.bolt_capacity,
                                             min_edge_dist=self.bolt.min_edge_dist_round,
                                             min_gauge=self.bolt.min_gauge_round,
                                             max_spacing=self.bolt.max_spacing_round,
                                             max_edge_dist=self.bolt.max_edge_dist_round,
                                             shear_load=self.load.shear_force * 1000,
                                             axial_load=self.load.axial_force * 1000, gap=self.plate.gap,
                                             shear_ecc=True, bolt_line_limit=2)

            # self.plate.bolts_required = max(int(math.ceil(self.res_force / self.bolt.bolt_capacity)), 2)
            # [bolt_line, bolts_one_line, web_plate_h] = \
            #     self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height, self.plate.bolts_required,
            #                                         self.bolt.min_edge_dist_round, self.bolt.min_gauge_round)
            # self.plate.bolts_required = bolt_line * bolts_one_line
            print(1, self.plate.bolt_force, self.bolt.bolt_capacity, self.bolt.bolt_diameter_provided, self.plate.bolts_required, self.plate.bolts_one_line)
            if self.plate.design_status is True:
                if self.plate.bolts_required > bolts_required_previous and count >= 1:
                    self.bolt.bolt_diameter_provided = bolt_diameter_previous
                    self.plate.bolts_required = bolts_required_previous
                    self.plate.bolt_force = bolt_force_previous
                    break
                bolts_required_previous = self.plate.bolts_required
                bolt_diameter_previous = self.bolt.bolt_diameter_provided
                bolt_force_previous = self.plate.bolt_force
                count += 1
            else:
                pass
        bolt_capacity_req = self.bolt.bolt_capacity

        if self.plate.design_status is False:
            self.design_status = False
            logger.error(self.plate.reason)
        else:
            self.get_bolt_grade(self,bolt_capacity_req)

    def get_bolt_grade(self,bolt_capacity_req):
        # print(self.design_status, "Getting bolt grade")
        bolt_grade_previous = self.bolt.bolt_grade[-1]

        for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
            count = 1
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=1)

            print(self.bolt.bolt_grade_provided, self.bolt.bolt_capacity, self.plate.bolt_force)

            bolt_capacity_reduced = self.plate.get_bolt_red(self.plate.bolts_one_line,
                                                            self.plate.gauge_provided, self.plate.bolt_line, self.plate.pitch_provided,self.bolt.bolt_capacity,
                                                            self.bolt.bolt_diameter_provided)
            if bolt_capacity_reduced < self.plate.bolt_force and count >= 1:
                self.bolt.bolt_grade_provided = bolt_grade_previous
                break
            bolts_required_previous = self.plate.bolts_required
            bolt_grade_previous = self.bolt.bolt_grade_provided
            count += 1

        self.bolt.design_status = True
        self.get_fin_plate_details(self)

    def get_fin_plate_details(self):

        # print(self.design_status,"getting fin plate details")
        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)

        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt.bolt_grade_provided,
                                          conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                          n_planes=1)

        self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                         web_plate_h_min=self.min_plate_height, web_plate_h_max=self.max_plate_height,
                                         bolt_capacity=self.bolt.bolt_capacity,
                                         min_edge_dist=self.bolt.min_edge_dist_round,
                                         min_gauge=self.bolt.min_gauge_round, max_spacing=self.bolt.max_spacing_round,
                                         max_edge_dist=self.bolt.max_edge_dist_round, shear_load=self.load.shear_force*1000,
                                         axial_load=self.load.axial_force*1000, gap=self.plate.gap,
                                         shear_ecc=True, bolt_line_limit=2)

        if self.plate.design_status is False:
            self.design_status = False
            logger.error(self.plate.reason)

        else:
            self.get_plate_thickness(self)

    def get_plate_thickness(self):
        initial_plate_height = self.plate.height
        for self.plate.thickness_provided in self.thickness_possible:
            self.plate.connect_to_database_to_get_fy_fu(grade=self.plate.material,
                                                        thickness=self.plate.thickness_provided)
            print('plate_t_fy_fu', self.plate.thickness_provided,self.plate.fy,self.plate.fu)
            self.plate.height = initial_plate_height
            if self.connectivity in VALUES_CONN_1:
                self.weld_connecting_plates = [self.supporting_section.flange_thickness, self.plate.thickness_provided]
            else:
                self.weld_connecting_plates = [self.supporting_section.web_thickness, self.plate.thickness_provided]
            [available_welds,self.weld_size_min,self.weld_size_max] = self.get_available_welds(self,self.weld_connecting_plates)
            if available_welds:
                while self.plate.height <= self.max_plate_height + 10:
                    self.section_shear_checks(self)
                    self.plate_shear_checks(self)
                    self.design_weld(self, available_welds)
                    if self.supported_section.design_status == False or \
                            self.plate.design_status_2 == False or self.weld.design_status == False:
                        self.plate.height+=10
                        [self.plate.gauge_provided, self.plate.edge_dist_provided, self.plate.height] =\
                            self.plate.get_gauge_edge_dist(web_plate_h=self.plate.height,bolts_one_line=self.plate.bolts_one_line,
                                                       edge_dist=self.plate.edge_dist_provided,max_spacing=self.bolt.max_spacing,
                                                       max_edge_dist=self.bolt.max_edge_dist)
                        ecc = (self.plate.pitch_provided * max((self.plate.bolt_line - 1.5), 0)) + self.plate.end_dist_provided + self.plate.gap
                        self.plate.bolt_force = self.plate.get_vres(bolts_one_line=self.plate.bolts_one_line,pitch=self.plate.pitch_provided,
                                            gauge=self.plate.gauge_provided,bolt_line=self.plate.bolt_line, shear_load=self.load.shear_force*1000,
                                            axial_load=self.load.axial_force, ecc = ecc)
                        self.plate.bolt_capacity_red = self.plate.get_bolt_red(bolts_one_line=self.plate.bolts_one_line,gauge=self.plate.gauge_provided,
                                                bolts_line=self.plate.bolt_line,pitch=self.plate.pitch_provided,
                                                bolt_capacity=self.bolt.bolt_capacity,bolt_dia=self.bolt.bolt_diameter_provided)
                        if self.plate.bolt_capacity_red < self.plate.bolt_force:
                            self.plate.height =initial_plate_height
                            break
                    else:
                        break

            else:
                logger.error(": For given members and %2.2f mm thick plate, weld sizes should be of range "
                         "%2.2f mm and  %2.2f mm " %self.plate.thickness_provided % self.weld_size_min
                             % self.weld_size_max)
                logger.info(": Cannot design weld with available welds ")

            if self.supported_section.design_status is False:
                break

        if self.load.shear_force*1000 > self.plate.shear_capacity:
            self.design_status = False
            logger.error(":shear capacity of the plate is less than the applied shear force, %2.2f kN [cl. 6.4.1]"
                         % self.load.shear_force)
            logger.warning(":Shear capacity of plate is %2.2f kN" % self.plate.shear_capacity/1000)
            logger.info(": Increase the plate thickness or material grade")

        if self.load.axial_force*1000 > self.plate.shear_capacity:
            self.design_status = False
            logger.error(":tensile capacity of the plate is less than the applied axial force, %2.2f kN [cl. 6.4.1]"
                         % self.load.axial_force)
            logger.warning(":tensile capacity of plate is %2.2f kN" % self.plate.tension_capacity/1000)
            logger.info(": Increase the plate thickness or material grade")

        if self.plate.moment_capacity < self.plate.moment_demand:
            self.design_status = False
            logger.error(": Plate moment capacity is less than the moment demand, %2.2f kNm [cl. 8.2.1.2]"
                         % self.plate.moment_demand)
            # print(self.plate.moment_capacity / 1000000)
            logger.warning(":Moment capacity of plate is %2.2f kN-m" % self.plate.moment_capacity)
            logger.info(": Increase the plate thickness or material grade")
            logger.info(": Arranging bolts in one line will reduce moment induced")

        if self.load.shear_force > self.supported_section.shear_capacity:
            self.design_status = False
            logger.error(":shear capacity of the Beam is less than the applied shear force, %2.2f kN [cl. 6.4.1]"
                         % self.load.shear_force)
            logger.warning(":Shear capacity of Beam is %2.2f kN" % self.supported_section.shear_capacity/1000)
            logger.info(": Choose a Beam of higher size or provide higher bolt diameter(if available) "
                        "So that rupture/block shear capacity increases")

        if self.load.axial_force > self.supported_section.tension_capacity:
            self.design_status = False
            logger.error(":tensile capacity of the Beam is less than the applied axial force, %2.2f kN [cl. 6.4.1]"
                         % self.load.axial_force)
            logger.warning(":tensile capacity of Beam is %2.2f kN" % self.supported_section.tension_capacity/1000)
            logger.info(": Choose a Beam of higher size or material grade")
            logger.info(": Lesser number of bolts per line increases the rupture capacity")

        if self.supported_section.moment_capacity < self.plate.moment_demand:
            self.design_status = False
            logger.error(": Beam moment capacity is less than the moment demand, %2.2f kNm [cl. 8.2.1.2]"
                         % self.plate.moment_demand)
            logger.warning(":Moment capacity of plate is %2.2f kN-m" % self.supported_section.moment_capacity)
            logger.info(": Increase the plate thickness or material grade")
            logger.info(": Arranging bolts in one line will reduce moment induced")

    def section_shear_checks(self):
        n_row = self.plate.bolts_one_line
        n_col = self.plate.bolt_line
        pitch = self.plate.gauge_provided
        gauge = self.plate.pitch_provided
        end = self.plate.edge_dist_provided
        web_thick = self.supported_section.web_thickness
        bolt_hole_dia = self.bolt.dia_hole
        edge = self.plate.end_dist_provided

        A_vg = ((n_row - 1) * pitch + end) * web_thick
        A_vn = ((n_row - 1) * pitch + end - (float(n_row) - 0.5) * bolt_hole_dia) * web_thick
        A_tg = ((n_col - 1) * gauge + edge) * web_thick
        A_tn = ((n_col - 1) * gauge + edge - (float(n_col) - 0.5) * bolt_hole_dia) * web_thick

        self.supported_section.block_shear_capacity_shear = IS800_2007.cl_6_4_1_block_shear_strength(A_vg,A_vn,A_tg,A_tn,
                                                                                                     self.supported_section.fu,
                                                                                                     self.supported_section.fy)

        A_vn = (self.supported_section.web_height - float(n_row) * bolt_hole_dia) * self.supported_section.web_thickness
        self.supported_section.shear_rupture_capacity = AISC.cl_j_4_2_b_shear_rupture(A_vn,self.supported_section.fu)

        self.supported_section.shear_capacity = min(self.supported_section.block_shear_capacity_shear,
                                                    self.supported_section.shear_rupture_capacity,
                                                    self.supported_section.shear_yielding_capacity)

        if self.supported_section.shear_capacity < self.load.shear_force * 1000:
            self.supported_section.design_status = False
        else:
            self.supported_section.design_status = True

        self.supported_section.tension_rupture_capacity = IS800_2007.cl_6_3_1_tension_rupture_strength(A_vn, self.plate.fu)
        A_vg = ((n_row - 1) * pitch) * web_thick
        A_vn = ((n_row - 1) * pitch + end - (float(n_row) - 1.0) * bolt_hole_dia) * web_thick
        A_tg = 2 * ((n_col - 1) * gauge + edge) * web_thick
        A_tn = 2 * ((n_col - 1) * gauge + edge - (float(n_col) - 0.5) * bolt_hole_dia) * web_thick

        self.supported_section.block_shear_capacity_axial = IS800_2007.cl_6_4_1_block_shear_strength(A_vg,
                                                                                                     A_vn,
                                                                                                     A_tg,
                                                                                                     A_tn,
                                                                                                     self.supported_section.fu,
                                                                                                     self.supported_section.fy)

        self.supported_section.tension_capacity = min(self.supported_section.tension_rupture_capacity,
                                          self.supported_section.tension_yielding_capacity,
                                          self.supported_section.block_shear_capacity_axial)

        if self.supported_section.tension_capacity < self.load.axial_force * 1000:
            self.supported_section.design_status = False
        else:
            self.supported_section.design_status = True

        Z_p = self.supported_section.web_height * self.supported_section.web_thickness ** 2 / 4
        Z_e = self.supported_section.web_height * self.supported_section.web_thickness ** 2 / 6
        self.supported_section.moment_capacity = IS800_2007.cl_8_2_1_2_design_moment_strength(Z_e, Z_p, self.plate.fy, 'plastic')

        if self.supported_section.moment_capacity < self.plate.moment_demand:
            self.supported_section.design_status = False
        else:
            self.supported_section.design_status = True

        self.supported_section.IR = round(self.plate.moment_demand / self.supported_section.moment_capacity + (
                    self.load.axial_force * 1000) / self.supported_section.tension_capacity, 2)
        if self.supported_section.IR > 1:
            self.supported_section.design_status = False
        else:
            self.supported_section.design_status = True

    def plate_shear_checks(self):
        edge_dist_rem = self.plate.edge_dist_provided + self.plate.gap
        n_row = self.plate.bolts_one_line
        n_col = self.plate.bolt_line
        pitch = self.plate.gauge_provided
        gauge = self.plate.pitch_provided
        end = self.plate.edge_dist_provided
        p_th = self.plate.thickness_provided
        bolt_hole_dia = self.bolt.dia_hole
        edge = self.plate.end_dist_provided
        plate_A_vg = ((n_row - 1) * pitch + end) * p_th
        plate_A_vn = ((n_row - 1) * pitch + end - (float(n_row) - 0.5) * bolt_hole_dia) * p_th
        plate_A_tg = ((n_col - 1) * gauge + edge) * p_th
        plate_A_tn = ((n_col - 1) * gauge + edge - (float(n_col) - 0.5)  * bolt_hole_dia) * p_th

        self.plate.block_shear_capacity_shear = IS800_2007.cl_6_4_1_block_shear_strength(plate_A_vg, plate_A_vn, plate_A_tg, plate_A_tn, self.plate.fu,
                                                                              self.plate.fy)

        A_vg = self.plate.height * self.plate.thickness_provided
        self.plate.shear_yielding_capacity = IS800_2007.cl_8_4_design_shear_strength(A_vg, self.plate.fy)
        A_vn = (self.plate.height - float(n_row) * bolt_hole_dia) * p_th
        self.plate.shear_rupture_capacity = AISC.cl_j_4_2_b_shear_rupture(A_vn,self.plate.fu)

        self.plate.shear_capacity = min(self.plate.block_shear_capacity_shear, self.plate.shear_rupture_capacity,
                                        self.plate.shear_yielding_capacity)

        if self.plate.shear_capacity < self.load.shear_force*1000:
            self.plate.design_status_2 = False
        else:
            self.plate.design_status_2 = True
        A_g = self.plate.length * self.plate.thickness_provided
        self.plate.tension_yielding_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g, self.plate.fy)

        A_n = (self.plate.length - self.plate.bolt_line * self.bolt.dia_hole) * self.plate.thickness_provided

        self.plate.tension_rupture_capacity = IS800_2007.cl_6_3_1_tension_rupture_strength(A_n,self.plate.fu)
        plate_A_vg = ((n_row - 1) * pitch) * p_th
        plate_A_vn = ((n_row - 1) * pitch + end - (float(n_row) - 1.0) * bolt_hole_dia) * p_th
        plate_A_tg = 2 * ((n_col - 1) * gauge + edge) * p_th
        plate_A_tn = 2 * ((n_col - 1) * gauge + edge - (float(n_col) - 0.5) * bolt_hole_dia) * p_th

        self.plate.block_shear_capacity_axial = IS800_2007.cl_6_4_1_block_shear_strength(plate_A_vg, plate_A_vn,
                                                                                         plate_A_tg,
                                                                                         plate_A_tn, self.plate.fu,
                                                                                         self.plate.fy)
        self.plate.tension_capacity = min(self.plate.tension_rupture_capacity, self.plate.tension_yielding_capacity,
                                          self.plate.block_shear_capacity_axial)

        if self.plate.tension_capacity < self.load.axial_force*1000:
            self.plate.design_status_2 = False
        else:
            self.plate.design_status_2 = True

        Z_p = (min(pitch, 2 * edge)) * p_th ** 2 / 4
        Z_e = (min(pitch, 2 * edge)) * p_th ** 2 / 6
        self.plate.moment_capacity = IS800_2007.cl_8_2_1_2_design_moment_strength(Z_e, Z_p, self.plate.fy, 'plastic')

        if self.plate.moment_capacity < self.plate.moment_demand:
            self.plate.design_status_2 = False
        else:
            self.plate.design_status_2 = True

        self.plate.IR = round(self.plate.moment_demand/self.plate.moment_capacity + (self.load.axial_force*1000)/self.plate.tension_capacity,2)
        if self.plate.IR > 1:
            self.plate.design_status_2 = False
        else:
            self.plate.design_status_2 = True

    def get_available_welds(self, connecting_members=[]):

        weld_size_max = min(connecting_members)

        weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(connecting_members[0], connecting_members[1])

        if weld_size_max == weld_size_min:
            logger.info("Minimum weld size given in Table 21 of IS800:2007 is greater than or equal to thickness of thinner connecting plate")
            logger.info("Thicker plate shall be adequately preheated to prevent cracking of the weld")

        available_welds = list([x for x in ALL_WELD_SIZES if (weld_size_min <= x <= weld_size_max)])
        return available_welds,weld_size_min,weld_size_max

    def design_weld(self,available_welds):
        self.weld.size = available_welds[0]
        while self.plate.height <= self.max_plate_height+10:
            self.weld.length = self.plate.height
            self.weld.throat_tk = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
                fillet_size=self.weld.size, fusion_face_angle=90)
            self.weld.eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
                fillet_size=self.weld.size, available_length=self.weld.length)
            self.weld.get_weld_strength(connecting_fu=[self.supporting_section.fu, self.weld.fu],
                                                weld_fabrication=self.weld.fabrication,

                                                t_weld=self.weld.size, weld_angle=90)
            Ip_weld = 2 * self.weld.eff_length ** 3 / 12
            y_max = self.weld.eff_length / 2
            x_max = 0
            force_l = self.load.shear_force * 1000
            force_w = self.load.axial_force*1000
            force_t = self.plate.moment_demand
            print(self.weld.strength)
            self.weld.get_weld_stress(weld_axial=force_l, weld_shear=force_w, weld_twist=force_t, Ip_weld=Ip_weld, y_max=y_max,
                                                        x_max=x_max, l_weld=2*self.weld.eff_length)
            print(self.weld.strength, self.weld.stress)
            if self.weld.strength > self.weld.stress:
                break
            else:
                t_weld_req = self.weld.size * self.weld.stress / self.weld.strength
                print("thicknessreq",t_weld_req)
                updated_weld_list = list([x for x in available_welds if (t_weld_req <= x)])
                print(updated_weld_list)
                if not updated_weld_list:
                    self.plate.height += 10
                    self.weld.size = available_welds[0]
                    logger.warning('weld stress is guiding plate height, trying with length %2.2f mm' % self.plate.height)
                else:
                    self.weld.size = updated_weld_list[0]

        print(self.weld.size, self.weld.length)
        if self.weld.strength < self.weld.stress:
            t_weld_req = self.weld.size * self.weld.stress / self.weld.strength
            self.weld.design_status = False
            logger.error(": Weld thickness is not sufficient [cl. 10.5.7, IS 800:2007]")
            logger.warning(": Minimum weld thickness required is %2.2f mm " % t_weld_req)
            logger.info(": Should increase length of weld/fin plate")
        else:
            self.weld.design_status = True

        self.recalculating_bolt_values(self)

    def recalculating_bolt_values(self):
        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu,self.plate.fy))
        self.bolt_conn_plates_t_fu_fy.append((self.supported_section.web_thickness, self.supported_section.fu,self.supported_section.fy))

        self.bolt.calculate_bolt_spacing_limits(self.bolt.bolt_diameter_provided,conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)
        self.bolt.calculate_bolt_capacity(self.bolt.bolt_diameter_provided,self.bolt.bolt_grade_provided,conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,n_planes=1)
        self.plate.get_gauge_edge_dist(web_plate_h=self.plate.height, bolts_one_line=self.plate.bolts_one_line,edge_dist=self.plate.edge_dist_provided,
                                       max_spacing=self.bolt.max_spacing,max_edge_dist=self.bolt.max_edge_dist)
        self.plate.get_bolt_red(bolts_one_line = self.plate.bolts_one_line,gauge=self.plate.gauge_provided,bolts_line=self.plate.bolt_line,
                                pitch=self.plate.gauge_provided,bolt_capacity=self.bolt.bolt_capacity,bolt_dia=self.bolt.bolt_diameter_provided)

        self.get_design_status(self)
        print("--- %s seconds ---" % (time.time() - self.start_time))

    def get_design_status(self):
        if self.plate.design_status is True and self.weld.design_status is True:
            self.design_status = True
            logger.info("=== End Of Design ===")

    def results_to_test(self, filename):
        test_out_list = {KEY_OUT_DISP_D_PROVIDED:self.bolt.bolt_diameter_provided,
                        KEY_OUT_DISP_GRD_PROVIDED:self.bolt.bolt_grade_provided,
                        KEY_OUT_DISP_BOLT_SHEAR:self.bolt.bolt_shear_capacity,
                        KEY_OUT_DISP_BOLT_BEARING:self.bolt.bolt_shear_capacity,
                        KEY_OUT_DISP_BOLT_CAPACITY:self.bolt.bolt_capacity,
                        KEY_OUT_DISP_BOLT_FORCE:self.plate.bolt_force,
                        KEY_OUT_DISP_BOLT_LINE:self.plate.bolt_line,
                        KEY_OUT_DISP_BOLTS_ONE_LINE:self.plate.bolts_one_line,
                        KEY_OUT_DISP_PITCH:self.plate.pitch_provided,
                        KEY_OUT_DISP_END_DIST:self.plate.end_dist_provided,
                        KEY_OUT_DISP_GAUGE:self.plate.gauge_provided,
                        KEY_OUT_DISP_EDGE_DIST:self.plate.edge_dist_provided,
                        KEY_OUT_DISP_PLATETHK:self.plate.thickness_provided,
                        KEY_OUT_DISP_PLATE_HEIGHT:self.plate.height,
                        KEY_OUT_DISP_PLATE_LENGTH:self.plate.length,
                        KEY_OUT_DISP_PLATE_SHEAR:self.plate.shear_yielding_capacity,
                        KEY_OUT_DISP_PLATE_BLK_SHEAR:self.plate.block_shear_capacity,
                        KEY_OUT_DISP_PLATE_MOM_DEMAND:self.plate.moment_demand,
                        KEY_OUT_DISP_PLATE_MOM_CAPACITY:self.plate.moment_capacity,
                        KEY_OUT_DISP_WELD_SIZE:self.weld.size,
                        KEY_OUT_DISP_WELD_STRENGTH:self.weld.strength,
                        KEY_OUT_DISP_WELD_STRESS:self.weld.stress}
        f = open(filename, "w")
        f.write(str(test_out_list))
        f.close()
        # return test_out_list

    # r'/ResourceFiles/images/ColumnsBeams".png'
    def save_design(self,popup_summary):
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")
        self.report_supporting = {KEY_DISP_SEC_PROFILE:"ISection",
                                  KEY_DISP_SUPTNGSEC: self.supporting_section.designation,
                                  KEY_DISP_MATERIAL: self.supporting_section.material,
                                  KEY_DISP_FU: self.supporting_section.fu,
                                  KEY_DISP_FY: self.supporting_section.fy,
                                  'Mass': self.supporting_section.mass,
                                  'Area(cm2) - A': self.supporting_section.area,
                                  'D(mm)': self.supporting_section.depth,
                                  'B(mm)': self.supporting_section.flange_width,
                                  't(mm)': self.supporting_section.web_thickness,
                                  'T(mm)': self.supporting_section.flange_thickness,
                                  'FlangeSlope': self.supporting_section.flange_slope,
                                  'R1(mm)': self.supporting_section.root_radius,
                                  'R2(mm)': self.supporting_section.toe_radius,
                                  'Iz(cm4)': self.supporting_section.mom_inertia_z,
                                  'Iy(cm4)': self.supporting_section.mom_inertia_y,
                                  'rz(cm)': self.supporting_section.rad_of_gy_z,
                                  'ry(cm)': self.supporting_section.rad_of_gy_y,
                                  'Zz(cm3)': self.supporting_section.elast_sec_mod_z,
                                  'Zy(cm3)': self.supporting_section.elast_sec_mod_y,
                                  'Zpz(cm3)': self.supporting_section.plast_sec_mod_z,
                                  'Zpy(cm3)': self.supporting_section.elast_sec_mod_y}

        self.report_supported = {
            KEY_DISP_SEC_PROFILE:"ISection", #Image shall be save with this name.png in resource files
            KEY_DISP_SUPTDSEC: self.supported_section.designation,
            KEY_DISP_MATERIAL: self.supported_section.material,
            KEY_DISP_FU: self.supported_section.fu,
            KEY_DISP_FY: self.supported_section.fy,
            'Mass': self.supported_section.mass,
            'Area(cm2) - A': round(self.supported_section.area, 2),
            'D(mm)': self.supported_section.depth,
            'B(mm)': self.supported_section.flange_width,
            't(mm)': self.supported_section.web_thickness,
            'T(mm)': self.supported_section.flange_thickness,
            'FlangeSlope': self.supported_section.flange_slope,
            'R1(mm)': self.supported_section.root_radius,
            'R2(mm)': self.supported_section.toe_radius,
            'Iz(cm4)': self.supported_section.mom_inertia_z,
            'Iy(cm4)': self.supported_section.mom_inertia_y,
            'rz(cm)': self.supported_section.rad_of_gy_z,
            'ry(cm)': self.supported_section.rad_of_gy_y,
            'Zz(cm3)': self.supported_section.elast_sec_mod_z,
            'Zy(cm3)': self.supported_section.elast_sec_mod_y,
            'Zpz(cm3)': self.supported_section.plast_sec_mod_z,
            'Zpy(cm3)': self.supported_section.elast_sec_mod_y}

        self.report_input = \
            {KEY_MODULE: self.module,
            KEY_MAIN_MODULE: self.mainmodule,
            KEY_CONN: self.connectivity,
            KEY_DISP_SHEAR: self.load.shear_force,
            "Supporting Section":"TITLE",
            "Supporting Section Details": self.report_supporting,
            "Supported Section":"TITLE",
            "Supported Section Details": self.report_supported,
            "Bolt Details":"TITLE",
            KEY_DISP_D: str(self.bolt.bolt_diameter),
            KEY_DISP_GRD: str(self.bolt.bolt_grade),
            KEY_DISP_TYP: self.bolt.bolt_type,
            KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
            KEY_DISP_DP_BOLT_SLIP_FACTOR: self.bolt.mu_f,
            KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
            KEY_DISP_DP_DETAILING_GAP: self.plate.gap,
            KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES: self.bolt.corrosive_influences,
            "Plate Details": "TITLE",
            KEY_DISP_PLATETHK: self.plate.thickness,
            KEY_DISP_MATERIAL: self.plate.material,
            KEY_DISP_FU: self.plate.fu,
            KEY_DISP_FY: self.plate.fy,
            "Weld Details":"TITLE",
            KEY_DISP_DP_WELD_TYPE: "Fillet",
            KEY_DISP_DP_WELD_FAB: self.weld.fabrication,
            KEY_DISP_DP_WELD_MATERIAL_G_O: self.weld.fu}


        self.report_check = []
        connecting_plates = [self.plate.thickness_provided,self.supported_section.web_thickness]

        bolt_shear_capacity_kn = round(self.bolt.bolt_capacity/1000,2)
        bolt_bearing_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2)
        bolt_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2)
        kb_disp= round(self.bolt.kb,2)
        kh_disp = round(self.bolt.kh, 2)
        bolt_force_kn=round(self.plate.bolt_force,2)
        bolt_capacity_red_kn=round(self.plate.bolt_capacity_red,2)

        t1 = ('SubSection', 'Bolt Design Checks','|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        if self.bolt.bolt_type == TYP_BEARING:
            t1 = (KEY_OUT_DISP_BOLT_SHEAR, '', bolt_shear_prov(self.bolt.fu,1,self.bolt.bolt_net_area,
                                                               self.bolt.gamma_mb,bolt_shear_capacity_kn), '')
            self.report_check.append(t1)
            t2 = (KEY_OUT_DISP_BOLT_BEARING, '', bolt_bearing_prov(kb_disp,self.bolt.bolt_diameter_provided,
                                                                   self.bolt_conn_plates_t_fu_fy,self.bolt.gamma_mb,
                                                                   bolt_bearing_capacity_kn), '')
            self.report_check.append(t2)
            t3 = (KEY_OUT_DISP_BOLT_CAPACITY, '',
                  bolt_capacity_prov(bolt_shear_capacity_kn,bolt_bearing_capacity_kn,bolt_capacity_kn),
                  '')
            self.report_check.append(t3)
        else:

            t4 = (KEY_OUT_DISP_BOLT_SLIP, '',
                  HSFG_bolt_capacity_prov(mu_f=self.bolt.mu_f,n_e=1,K_h=kh_disp,fub = self.bolt.fu,
                                          Anb= self.bolt.bolt_net_area,gamma_mf=self.bolt.gamma_mf,
                                          capacity=bolt_capacity_kn),'')
            self.report_check.append(t4)

        t5 = (DISP_NUM_OF_BOLTS, get_trial_bolts(self.load.shear_force,self.load.axial_force,bolt_capacity_kn), self.plate.bolts_required, '')
        self.report_check.append(t5)
        t6 = (DISP_NUM_OF_COLUMNS, '', self.plate.bolt_line, '')
        self.report_check.append(t6)
        t7 = (DISP_NUM_OF_ROWS, '', self.plate.bolts_one_line, '')
        self.report_check.append(t7)
        t1 = (DISP_MIN_PITCH, min_pitch(self.bolt.bolt_diameter_provided),
              self.plate.pitch_provided, get_pass_fail(self.bolt.min_pitch, self.plate.pitch_provided,relation='lesser'))
        self.report_check.append(t1)
        t1 = (DISP_MAX_PITCH, max_pitch(connecting_plates),
              self.plate.pitch_provided, get_pass_fail(self.bolt.max_spacing, self.plate.pitch_provided,relation='greater'))
        self.report_check.append(t1)
        t2 = (DISP_MIN_GAUGE, min_pitch(self.bolt.bolt_diameter_provided),
              self.plate.gauge_provided, get_pass_fail(self.bolt.min_gauge, self.plate.gauge_provided,relation="lesser"))
        self.report_check.append(t2)
        t2 = (DISP_MAX_GAUGE, max_pitch(connecting_plates),
              self.plate.gauge_provided, get_pass_fail(self.bolt.max_spacing, self.plate.gauge_provided,relation="greater"))
        self.report_check.append(t2)
        t3 = (DISP_MIN_END, min_edge_end(self.bolt.d_0, self.bolt.edge_type),
              self.plate.end_dist_provided, get_pass_fail(self.bolt.min_end_dist, self.plate.end_dist_provided,relation='lesser'))
        self.report_check.append(t3)
        t4 = (DISP_MAX_END, max_edge_end(self.plate.fy, self.plate.thickness_provided),
              self.plate.end_dist_provided, get_pass_fail(self.bolt.max_end_dist, self.plate.end_dist_provided,relation='greater'))
        self.report_check.append(t4)
        t3 = (DISP_MIN_EDGE, min_edge_end(self.bolt.d_0, self.bolt.edge_type),
              self.plate.edge_dist_provided, get_pass_fail(self.bolt.min_edge_dist, self.plate.edge_dist_provided,relation='lesser'))
        self.report_check.append(t3)
        t4 = (DISP_MAX_EDGE, max_edge_end(self.plate.fy, self.plate.thickness_provided),
              self.plate.edge_dist_provided, get_pass_fail(self.bolt.max_edge_dist, self.plate.edge_dist_provided,relation="greater"))
        self.report_check.append(t4)
        t5=(KEY_OUT_DISP_BOLT_CAPACITY, bolt_force_kn,bolt_capacity_red_kn,
            get_pass_fail(bolt_force_kn,bolt_capacity_red_kn,relation="lesser"))
        self.report_check.append(t5)


        t1 = ('SubSection','Plate Design Checks','|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (DISP_MIN_PLATE_HEIGHT, min_plate_ht_req(self.supported_section.depth,self.min_plate_height), self.plate.height,
              get_pass_fail(self.min_plate_height, self.plate.height,relation="lesser"))
        self.report_check.append(t1)
        t1 = (DISP_MAX_PLATE_HEIGHT, max_plate_ht_req(self.connectivity,self.supported_section.depth,
                                                      self.supported_section.flange_thickness,
                                                      self.supported_section.root_radius, self.supported_section.notch_ht,
                                                      self.max_plate_height), self.plate.height,
              get_pass_fail(self.max_plate_height, self.plate.height,relation="greater"))
        self.report_check.append(t1)
        min_plate_length = self.plate.gap +2*self.bolt.min_end_dist+(self.plate.bolt_line-1)*self.bolt.min_pitch
        t1 = (DISP_MIN_PLATE_LENGTH, min_plate_length_req(self.bolt.min_pitch, self.bolt.min_end_dist,
                                                      self.plate.bolt_line,min_plate_length), self.plate.length,
              get_pass_fail(min_plate_length, self.plate.length, relation="lesser"))
        self.report_check.append(t1)
        t1 = (DISP_MIN_PLATE_THICK, min_plate_thk_req(self.supported_section.web_thickness), self.plate.thickness_provided,
              get_pass_fail(self.supported_section.web_thickness, self.plate.thickness_provided, relation="lesser"))
        self.report_check.append(t1)
        ###################
        #Plate Shear Capacities
        ###################
        if self.plate.design_status is True:
            gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
            A_v = self.plate.height*self.plate.thickness_provided
            t1 = (KEY_DISP_SHEAR_YLD, '', shear_yield_prov(self.plate.height,self.plate.thickness_provided,
                                                               self.plate.fy,gamma_m0,round(self.plate.shear_yielding_capacity/1000,2)),
                  '')
            self.report_check.append(t1)

            t1 = (KEY_DISP_SHEAR_RUP, '', shear_rupture_prov(self.plate.height, self.plate.thickness_provided,
                                                                               self.plate.bolts_one_line, self.bolt.dia_hole,
                                                                               self.plate.fu,round(self.plate.shear_rupture_capacity/1000,2)),
                  '')
            self.report_check.append(t1)

            t1 = (KEY_DISP_PLATE_BLK_SHEAR_SHEAR, '', round(self.plate.block_shear_capacity/1000,2),'')
            self.report_check.append(t1)

            t1 = (KEY_DISP_SHEAR_CAPACITY, self.load.shear_force, shear_capacity_prov(round(self.plate.shear_yielding_capacity/1000,2),
                                                                                     round(self.plate.shear_rupture_capacity/1000,2),
                                                                                     round(self.plate.block_shear_capacity/1000,2)),
                  get_pass_fail(self.load.shear_force, round(self.plate.shear_capacity / 1000, 2), relation="lesser"))
            self.report_check.append(t1)
            ############
            # Plate Tension Capacities
            ##############
            gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
            A_g = self.plate.length * self.plate.thickness_provided
            t1 = (KEY_DISP_TENSION_YIELDCAPACITY, '', tension_yield_prov(self.plate.length,self.plate.thickness_provided, self.plate.fy, gamma_m0,
                                                                 round(self.plate.tension_yielding_capacity / 1000, 2)),'')
            self.report_check.append(t1)

            t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '', tension_rupture_bolted_prov(self.plate.length, self.plate.thickness_provided,
                                                            self.plate.bolts_one_line, self.bolt.dia_hole,
                                                            self.plate.fu,gamma_m1,
                                                            round(self.plate.tension_rupture_capacity / 1000, 2)),'')
            self.report_check.append(t1)

            t1 = (KEY_DISP_PLATE_BLK_SHEAR_TENSION, '', round(self.plate.block_shear_capacity/1000,2),'')
            self.report_check.append(t1)

            t1 = (KEY_DISP_TENSION_CAPACITY, self.load.axial_force, tensile_capacity_prov(round(self.plate.tension_yielding_capacity/1000,2),
                                                                                      round(self.plate.tension_rupture_capacity/1000,2),
                                                                                      round(self.plate.block_shear_capacity/1000,2)),
            get_pass_fail(self.load.axial_force, round(self.plate.tension_capacity / 1000, 2), relation="lesser"))
            self.report_check.append(t1)

            #############
            #Plate Moment Capacity
            ##############

            t1 = (KEY_OUT_DISP_PLATE_MOM_CAPACITY, round(self.plate.moment_demand/1000000,2),
                  round(self.plate.moment_capacity/1000000,2),
                  get_pass_fail(self.plate.moment_demand, self.plate.moment_capacity, relation="lesser"))
            self.report_check.append(t1)

            t1 = (KEY_DISP_IR, IR_req(IR = 1),
                  mom_axial_IR_prov(round(self.plate.moment_demand/1000000,2),round(self.plate.moment_capacity/1000000,2),
                                    self.load.axial_force,round(self.plate.tension_capacity/1000,2),self.plate.IR),
                  get_pass_fail(1, self.plate.IR, relation="greater"))
            self.report_check.append(t1)

            ##################
            # Weld Checks
            ##################
            t1 = ('SubSection', 'Weld Checks', '|p{4cm}|p{7.0cm}|p{3.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (DISP_MIN_WELD_SIZE, min_weld_size_req(self.weld_connecting_plates,self.weld_size_min), self.weld.size,
                  get_pass_fail(self.weld_size_min, self.weld.size, relation="leq"))
            self.report_check.append(t1)
            t1 = (DISP_MAX_WELD_SIZE, max_weld_size_req(self.weld_connecting_plates, self.weld_size_max), self.weld.size,
                  get_pass_fail(self.weld_size_min, self.weld.size, relation="geq"))
            self.report_check.append(t1)
            Ip_weld = round(2 * self.weld.eff_length ** 3 / 12,2)
            weld_conn_plates_fu = [self.supporting_section.fu, self.plate.fu]
            gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.weld.fabrication]
            t1 = (DISP_WELD_STRENGTH, weld_strength_req(V=self.load.shear_force*1000,A=self.load.axial_force*1000,
                                                        M=self.plate.moment_demand,Ip_w=Ip_weld,
                                                        y_max= self.weld.eff_length/2,x_max=0.0,l_w=2*self.weld.eff_length,
                                                        R_w=self.weld.stress),
                  weld_strength_prov(weld_conn_plates_fu, gamma_mw, self.weld.throat_tk,self.weld.strength),
                  get_pass_fail(self.weld.stress, self.weld.strength, relation="lesser"))
            self.report_check.append(t1)

        Disp_3D_image = "/ResourceFiles/images/3d.png"

        # config = configparser.ConfigParser()
        # config.read_file(open(r'Osdag.config'))
        # desktop_path = config.get("desktop_path", "path1")
        # print("desk:", desktop_path)
        #print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")

        #file_type = "PDF (*.pdf)"
        #filename = QFileDialog.getSaveFileName(QFileDialog(), "Save File As", os.path.join(str(' '), "untitled.pdf"), file_type)
        # filename = os.path.join(str(folder), "images_html", "TexReport")
        #file_name = str(filename)
        fname_no_ext = popup_summary['filename']


        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext, rel_path, Disp_3D_image)


# For Command Line


# from ast import literal_eval
#
# path = input("Enter the file location: ")
# with open(path, 'r') as f:
#     data = f.read()
#     d = literal_eval(data)
#     FinPlateConnection.set_input_values(FinPlateConnection(), d, False)
