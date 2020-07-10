from design_type.connection.shear_connection import ShearConnection
from design_report.reportGenerator_latex import CreateLatex
from utils.common.component import *
from utils.common.material import *
from Report_functions import *
import logging


class FinPlateConnection(ShearConnection):

    def __init__(self):
        super(FinPlateConnection, self).__init__()
        self.min_plate_height = 0.0
        self.max_plate_height = 0.0
        self.res_force = 0.0
        self.weld_connecting_plates=[]
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

        t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        tabs.append(t6)

        t2 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t2)

        t2 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t2)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):

        change_tab = []

        t1 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC_MATERIAL], [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY], TYPE_TEXTBOX,
        self.get_fu_fy_I_section_suptng)
        change_tab.append(t1)

        t2 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC_MATERIAL], [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY], TYPE_TEXTBOX,
        self.get_fu_fy_I_section_suptd)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)

        change_tab.append(t3)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20','Label_21','Label_22',KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4','Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20','Label_21','Label_22',KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC], ['Label_23'], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        t7 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC], ['Label_23'], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

        return change_tab

    def input_dictionary_design_pref(self):
        design_input = []
        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SUPTNGSEC_MATERIAL])
        design_input.append(t1)

        t2 = (KEY_DISP_BEAMSEC, TYPE_COMBOBOX, [KEY_SUPTDSEC_MATERIAL])
        design_input.append(t2)

        t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
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

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SUPTNGSEC_MATERIAL, KEY_SUPTDSEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_WELD_FAB, KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_GAP,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    ####################################
    # Design Preference Functions End
    ####################################
    # Setting up logger and Input and Output Docks
    ####################################

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """
        # @author Arsil Zunzunia
        # super(FinPlateConnection, FinPlateConnection).set_osdaglogger(key)
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
        return KEY_DISP_FINPLATE

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)

        e.g.
        t = (Key, Key_display, Type, existing_val, Current_Value, enabled/disabled, Validator_type)
        '''

        # @author: Amir, Umair
        self.module = KEY_DISP_FINPLATE

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_FINPLATE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, VALUES_CONN, True, 'No Validator')
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, "./ResourceFiles/images/fin_cf_bw.png", True, 'No Validator')
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, connectdb("Columns"), True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, connectdb("Beams"), True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK, True, 'No Validator')
        options_list.append(t14)

        return options_list

    def spacing(self, status):

        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details - 3 x 3 pattern considered")
        spacing.append(t00)


        t99 = (None, 'Spacing Details', TYPE_SECTION,
               ['./ResourceFiles/images/spacing_3.png', 400, 277, ""])  # [image, width, height, caption]
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def capacities(self, status):

        capacities = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern (Half Plate)- 2 x 3 Bolts pattern considered")
        capacities.append(t00)

        t99 = (None, 'Failure Pattern due to Shear in Plate', TYPE_SECTION,
               ['./ResourceFiles/images/L_shear1.png', 400, 210, "Block Shear Pattern"])  # [image, width, height, caption]
        capacities.append(t99)

        t17 = (KEY_OUT_PLATE_SHEAR, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX, round(self.plate.shear_yielding_capacity/1000,2) if status else '')
        capacities.append(t17)

        t18 = (KEY_OUT_PLATE_RUPTURE, KEY_OUT_DISP_PLATE_RUPTURE, TYPE_TEXTBOX, round(self.plate.shear_rupture_capacity/1000,2) if status else '')
        capacities.append(t18)

        t17 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_OUT_DISP_PLATE_BLK_SHEAR, TYPE_TEXTBOX, round(self.plate.block_shear_capacity_shear/1000,2) if status else '')
        capacities.append(t17)

        t99 = (None, 'Failure Pattern due to Tension in Plate', TYPE_SECTION,
               ['./ResourceFiles/images/U.png', 400, 202,
                "Block Shear Pattern"])  # [image, width, height, caption]
        capacities.append(t99)

        t17 = (KEY_OUT_PLATE_TENSION, KEY_OUT_DISP_PLATE_TENSION, TYPE_TEXTBOX,
               round(self.plate.tension_yielding_capacity/1000, 2) if status else '')
        capacities.append(t17)

        t18 = (KEY_OUT_PLATE_TENSION_RUP, KEY_OUT_DISP_PLATE_TENSION_RUP, TYPE_TEXTBOX,
               round(self.plate.tension_rupture_capacity/1000, 2) if status else '')
        capacities.append(t18)

        t17 = (KEY_OUT_PLATE_BLK_SHEAR_AXIAL, KEY_OUT_DISP_PLATE_BLK_SHEAR_AXIAL, TYPE_TEXTBOX,
               round(self.plate.block_shear_capacity_axial/1000, 2) if status else '')
        capacities.append(t17)

        t99 = (None, 'Section3', TYPE_SECTION, None)
        capacities.append(t99)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX, round(self.plate.moment_demand/1000000,2) if status else '')
        capacities.append(t19)

        t20 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX, round(self.plate.moment_capacity/1000000,2) if status else '')
        capacities.append(t20)

        return capacities

    def section_capacities(self, status):

        capacities = []

        t00 = (
        None, "", TYPE_NOTE, "Representative image for Failure Pattern (Half Plate)- 2 x 3 Bolts pattern considered")
        capacities.append(t00)

        t99 = (None, 'Failure Pattern due to Shear in Member', TYPE_SECTION,
               ['./ResourceFiles/images/L_shear1.png', 400, 210,
                "Block Shear Pattern"])  # [image, width, height, caption]
        capacities.append(t99)

        t17 = (KEY_SHEAR_YIELDCAPACITY, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX, round(self.supported_section.shear_yielding_capacity/1000,2) if status else '')
        capacities.append(t17)

        t18 = (KEY_SHEAR_RUPTURECAPACITY, KEY_OUT_DISP_PLATE_RUPTURE, TYPE_TEXTBOX, round(self.supported_section.shear_rupture_capacity/1000,2) if status else '')
        capacities.append(t18)

        t17 = (KEY_SHEAR_BLOCKSHEARCAPACITY, KEY_OUT_DISP_PLATE_BLK_SHEAR, TYPE_TEXTBOX, round(self.supported_section.block_shear_capacity_shear/1000,2) if status else '')
        capacities.append(t17)

        t99 = (None, 'Failure Pattern due to Tension in Member', TYPE_SECTION,
               ['./ResourceFiles/images/U.png', 400, 202,
                "Block Shear Pattern"])  # [image, width, height, caption]
        capacities.append(t99)

        t17 = (KEY_TENSION_YIELDCAPACITY, KEY_OUT_DISP_PLATE_TENSION, TYPE_TEXTBOX,
               round(self.supported_section.tension_yielding_capacity/1000, 2) if status else '')
        capacities.append(t17)

        t18 = (KEY_TENSION_RUPTURECAPACITY, KEY_OUT_DISP_PLATE_TENSION_RUP, TYPE_TEXTBOX,
               round(self.supported_section.tension_rupture_capacity/1000, 2) if status else '')
        capacities.append(t18)

        t17 = (KEY_TENSION_BLOCKSHEARCAPACITY, KEY_OUT_DISP_PLATE_BLK_SHEAR_AXIAL, TYPE_TEXTBOX,
               round(self.supported_section.block_shear_capacity_axial/1000, 2) if status else '')
        capacities.append(t17)

        t99 = (None, 'Section3', TYPE_SECTION, '')
        capacities.append(t99)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX, round(self.plate.moment_demand/1000000,2) if status else '')
        capacities.append(t19)

        t20 = (KEY_MEMBER_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX, round(self.supported_section.moment_capacity/1000000,2) if status else '')
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

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
              round(self.bolt.bolt_shear_capacity / 1000, 2) if flag else '', True)
        out_list.append(t4)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)

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

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True)
        out_list.append(t13)

        t14 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.plate.thickness_provided if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.plate.height if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_LENGTH, TYPE_TEXTBOX, self.plate.length if flag else '', True)
        out_list.append(t16)

        t22 = ('button1', KEY_OUT_DISP_PLATE_CAPACITIES, TYPE_OUT_BUTTON, ['Capacity Details', self.capacities],True)
        out_list.append(t22)

        t13 = (None, DISP_TITLE_SECTION, TYPE_TITLE, None, True)
        out_list.append(t13)

        t22 = ('button2', KEY_OUT_DISP_PLATE_CAPACITIES, TYPE_OUT_BUTTON, ['Capacity Details', self.capacities],True)
        out_list.append(t22)

        t13 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t13)

        t14 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX, self.weld.size if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX, round(self.weld.strength,2) if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_WELD_STRESS, KEY_OUT_DISP_WELD_STRESS, TYPE_TEXTBOX, round(self.weld.stress,2) if flag else '', True)
        out_list.append(t16)

        return out_list

    ####################################
    # Setting input values and start of Calculations
    ####################################
    def set_input_values(self, design_dictionary):

        # if design_dictionary[KEY_SUPTNGSEC_MATERIAL] == "Custom":
        #     design_dictionary[KEY_SUPTNGSEC_MATERIAL] = "Custom" + " " + str(design_dictionary[KEY_SUPTNGSEC_FU]) + " " \
        #                                                 + str(design_dictionary[KEY_SUPTNGSEC_FY])
        # if design_dictionary[KEY_SUPTDSEC_MATERIAL] == "Custom":
        #     design_dictionary[KEY_SUPTDSEC_MATERIAL] = "Custom" + " " + str(design_dictionary[KEY_SUPTDSEC_FU]) + " " \
        #                                                 + str(design_dictionary[KEY_SUPTDSEC_FY])

        super(FinPlateConnection,self).set_input_values(self, design_dictionary)

        self.start_time = time.time()
        self.module = design_dictionary[KEY_MODULE]

        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.plate.design_status_capacity = False
        self.weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],fabrication = design_dictionary[KEY_DP_WELD_FAB])
        print("input values are set. Doing preliminary member checks")
        self.warn_text(self)
        self.member_capacity(self)

    def member_capacity(self):
        super(FinPlateConnection,self).member_capacity(self)
        self.thickness_possible = []
        self.supported_section.low_shear_capacity = round(0.6 *self.supported_section.shear_yielding_capacity,2)
        if self.supported_section.low_shear_capacity / 1000 > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity / 1000 > self.load.axial_force:
            self.supported_section.design_status_initial = True

            if self.load.shear_force <= min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                            40.0):
                logger.warning(" : User input for shear force is very less compared to section capacity. "
                               "Setting Shear Force value to 15% of supported beam shear capacity or 40kN, whichever is less.")
                self.load.shear_force = min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                            40.0)

            print("preliminary member check is satisfactory. Checking available plate Thickness")
            self.thickness_possible = [i for i in self.plate.thickness if i >= self.supported_section.web_thickness]

            if not self.thickness_possible:
                self.plate.thickness_available = min(self.plate.thickness)
                logger.error(": Plate thickness should be greater than suppported section web thicknesss.")
            else:
                print("Selecting bolt diameter")
                self.select_bolt_dia(self)

        else:
            self.supported_section.design_status_initial = False
            logger.warning(" : shear yielding capacity (low shear case) {} and/or tension yielding capacity {} is less "
                           "than applied loads, Please select larger sections or decrease loads"
                           .format(round(self.supported_section.low_shear_capacity/1000,2),
                                   round(self.supported_section.tension_yielding_capacity/1000,2)))
            print("failed in preliminary member checks. Select larger sections or decrease loads")

    def select_bolt_dia(self):
        self.min_plate_height = self.supported_section.min_plate_height()
        self.max_plate_height = self.supported_section.max_plate_height(self.connectivity, 50.0)

        self.res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000

        self.plate.thickness_provided = min(self.thickness_possible)
        self.plate.connect_to_database_to_get_fy_fu(grade=self.plate.material,thickness=self.plate.thickness_provided)
        bolts_required_previous = 2

        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
        count = 0

        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
        self.bolt_conn_plates_t_fu_fy.append((self.supported_section.web_thickness, self.supported_section.fu, self.supported_section.fy))

        bolt_force_previous = 0.0
        bolt_dia_previous = self.bolt.bolt_diameter[-1]
        plate_height_previous = self.min_plate_height
        long_joint_factor_previous = 1.0

        for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=1)
            print("getting web plate details for dia:", self.bolt.bolt_diameter_provided, self.bolt.bolt_grade_provided, self.bolt.bolt_capacity)
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
            self.long_joint_factor = self.plate.bolt_capacity_red/self.bolt.bolt_capacity

            if self.plate.design_status is True:
                if self.plate.bolts_required > bolts_required_previous and count >= 1:
                    self.bolt.bolt_diameter_provided = bolt_dia_previous
                    self.plate.bolt_force = bolt_force_previous
                    self.plate.height = plate_height_previous
                    self.long_joint_factor = long_joint_factor_previous
                    break
                bolt_force_previous = self.plate.bolt_force
                bolt_dia_previous = self.bolt.bolt_diameter_provided
                plate_height_previous = self.plate.height
                long_joint_factor_previous = self.plate.bolt_capacity_red/self.bolt.bolt_capacity
                bolts_required_previous = self.plate.bolts_required
                count += 1
            else:
                pass
        # bolt_capacity_req = self.bolt.bolt_capacity

        if self.plate.design_status is False:
            self.design_status = False
            logger.error(self.plate.reason)
        else:
            self.get_bolt_grade(self)

    def get_bolt_grade(self):
        # print(self.design_status, "Getting bolt grade")
        bolt_grade_previous = self.bolt.bolt_grade[-1]
        # bolt_previous = self.bolt
        count = 0
        for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=1)

            print("for grade :", self.bolt.bolt_grade_provided, "capacity is:",self.bolt.bolt_capacity,"force is:", self.plate.bolt_force)

            bolt_capacity_reduced = self.long_joint_factor*self.bolt.bolt_shear_capacity
            if bolt_capacity_reduced < self.plate.bolt_force and count >= 1:
                self.bolt.bolt_grade_provided = bolt_grade_previous
                break
            bolt_grade_previous = self.bolt.bolt_grade_provided
            count += 1

        self.bolt.design_status = True
        self.get_fin_plate_details(self)

    def get_fin_plate_details(self):
        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)

        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt.bolt_grade_provided,
                                          conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                          n_planes=1)
        print("recalculating web plate details")
        self.plate.get_web_plate_details(bolt_dia=self.bolt.bolt_diameter_provided,
                                         web_plate_h_min=self.plate.height,
                                         web_plate_h_max=self.max_plate_height,
                                         bolt_capacity=self.bolt.bolt_capacity,
                                         min_edge_dist=self.bolt.min_edge_dist_round,
                                         min_gauge=self.bolt.min_gauge_round,
                                         max_spacing=self.bolt.max_spacing_round,
                                         max_edge_dist=self.bolt.max_edge_dist_round,
                                         shear_load=self.load.shear_force * 1000,
                                         axial_load=self.load.axial_force * 1000, gap=self.plate.gap,
                                         shear_ecc=True, bolt_line_limit=2)
        initial_plate_height = self.plate.height
        initial_edge_dist = self.plate.edge_dist_provided
        initial_gauge = self.plate.gauge_provided
        self.initial_plate_thk = self.plate.thickness_provided
        self.initial_bearing_capacity = self.bolt.bolt_bearing_capacity
        self.initial_kb = self.bolt.kb
        self.initial_bolt_capacity = self.bolt.bolt_capacity

        for self.plate.thickness_provided in self.thickness_possible:
            self.plate.connect_to_database_to_get_fy_fu(grade=self.plate.material,
                                                        thickness=self.plate.thickness_provided)
            print('plate_t_fy_fu', self.plate.thickness_provided,self.plate.fy,self.plate.fu)
            self.plate.height = initial_plate_height
            self.plate.gauge_provided = initial_gauge
            self.plate.edge_dist_provided = initial_edge_dist
            if self.bolt.bolt_type == TYP_BEARING:
                self.bolt.calculate_bolt_capacity(self.bolt.bolt_diameter_provided,self.bolt.bolt_grade_provided,
                                                  self.bolt_conn_plates_t_fu_fy,1,self.plate.edge_dist_provided,
                                                  p=self.plate.gauge_provided)
            self.plate.get_web_plate_details(self.bolt.bolt_diameter_provided, self.plate.height, self.plate.height,
                                             self.bolt.bolt_capacity, self.plate.edge_dist_provided,
                                             self.plate.gauge_provided,
                                             self.plate.gauge_provided, self.plate.edge_dist_provided,
                                             self.load.shear_force * 1000, self.load.axial_force * 1000, 0,
                                             self.plate.gap, True, 2,
                                             self.plate.bolts_one_line, self.plate.bolt_line, None, self.plate.pitch_provided)
            if self.connectivity in VALUES_CONN_1:
                self.weld_connecting_plates = [self.supporting_section.flange_thickness, self.plate.thickness_provided]
            else:
                self.weld_connecting_plates = [self.supporting_section.web_thickness, self.plate.thickness_provided]
            [available_welds,self.weld_size_min,self.weld_size_max] = self.get_available_welds(self,self.weld_connecting_plates)
            if available_welds:
                self.section_shear_checks(self)
                self.plate_shear_checks(self)
                self.design_weld(self, available_welds)
                while self.supported_section.design_status == False or self.plate.design_status_capacity == False or \
                        self.weld.design_status == False:
                    if self.supported_section.moment_capacity > self.plate.moment_demand and self.plate.height+10 <= self.max_plate_height:
                        self.plate.height += 10
                        h_recalc = (self.plate.gauge_provided + 5) * (self.plate.bolts_one_line - 1) + self.plate.edge_dist_provided
                        if self.plate.block_shear_capacity_axial > self.load.axial_force*1000 or \
                                self.supported_section.block_shear_capacity_axial > self.load.axial_force*1000 or \
                                self.plate.edge_dist_provided + 5 <= self.bolt.max_edge_dist:
                            self.plate.edge_dist_provided += 5

                        elif self.plate.gauge_provided + 5 <= self.bolt.max_spacing and h_recalc <= self.max_plate_height:
                            self.plate.gauge_provided += 5
                            self.plate.height = (self.plate.gauge_provided) * (self.plate.bolts_one_line - 1) + self.plate.edge_dist_provided
                            self.plate.get_web_plate_details(self.bolt.bolt_diameter_provided, self.plate.height,self.plate.height,
                                                             self.bolt.bolt_capacity,self.plate.edge_dist_provided, self.plate.gauge_provided,
                                                             self.plate.gauge_provided,self.plate.edge_dist_provided,
                                                             self.load.shear_force*1000,self.load.axial_force*1000,0,self.plate.gap,True,2,
                                                             self.plate.bolts_one_line, self.plate.bolt_line,None)

                            if self.plate.design_status is False:
                                break
                        else:
                            break
                        self.section_shear_checks(self)
                        self.plate_shear_checks(self)
                        self.design_weld(self, available_welds)
                    else:
                        break
                if self.supported_section.design_status is True and self.plate.design_status_capacity is False:
                    continue
                elif self.weld.design_status is False and \
                        self.plate.thickness_provided <= math.ceil(min(self.weld_connecting_plates))\
                        and self.weld.size != max(ALL_WELD_SIZES):
                    continue
                else:
                    break

            else:
                logger.error(": For given members and %2.2f mm thick plate, weld sizes should be of range "
                         "%2.2f mm and  %2.2f mm " %self.plate.thickness_provided % self.weld_size_min
                             % self.weld_size_max)
                logger.info(": Cannot design weld with available welds ")

            if self.plate.moment_capacity < self.plate.moment_demand:
                break

            if self.supported_section.design_status is True and self.plate.design_status_capacity is True and self.weld.design_status is True:
                self.get_design_status(self)
                break

        if self.load.shear_force*1000 > self.plate.shear_capacity:
            self.design_status = False
            logger.error(":shear capacity of the plate is less than the applied shear force, %2.2f kN [cl. 6.4.1]"
                         % self.load.shear_force)
            logger.warning(":Shear capacity of plate is {} kN" .format(round(self.plate.shear_capacity/1000,2)))
            logger.info(": Increase the plate thickness or material grade")

        if self.load.axial_force*1000 > self.plate.tension_capacity:
            self.design_status = False
            logger.error(":tensile capacity of the plate is less than the applied axial force, %2.2f kN [cl. 6.4.1]"
                         % self.load.axial_force)
            logger.warning(":tensile capacity of plate is {} kN" .format(round(self.plate.tension_capacity/1000,2)))
            logger.info(": Increase the plate thickness or material grade")

        if self.plate.moment_capacity < self.plate.moment_demand:
            self.design_status = False
            logger.error(": Plate moment capacity is less than the moment demand, {} kNm [cl. 8.2.1.2]"
                         .format(round(self.plate.moment_demand/1000000,2)))
            # print(self.plate.moment_capacity / 1000000)
            logger.warning(":Moment capacity of plate is {} kN-m".format(round(self.plate.moment_capacity/1000000,2)))
            logger.info(": Increase the plate thickness or material grade")
            logger.info(": Arranging bolts in one line will reduce moment induced")

        if self.load.shear_force*1000 > self.supported_section.shear_capacity:
            self.design_status = False
            logger.error(":shear capacity of the Beam is less than the applied shear force, %2.2f kN [cl. 6.4.1]"
                         % self.load.shear_force)
            logger.warning(":Shear capacity of Beam is {} kN".format(round(self.supported_section.shear_capacity/1000,2)))
            logger.info(": Choose a Beam of higher size or provide higher bolt diameter(if available) "
                        "So that rupture/block shear capacity increases")

        if self.load.axial_force*1000 > self.supported_section.tension_capacity:
            self.design_status = False
            logger.error(":tensile capacity of the Beam is less than the applied axial force, %2.2f kN [cl. 6.4.1]"
                         % self.load.axial_force)
            logger.warning(":tensile capacity of Beam is {} kN" .format(round(self.supported_section.tension_capacity/1000,2)))
            logger.info(": Choose a Beam of higher size or material grade")
            logger.info(": Lesser number of bolts per line increases the rupture capacity")

        if self.supported_section.moment_capacity < self.plate.moment_demand:
            self.design_status = False
            logger.error(": Beam moment capacity is less than the moment demand, {} kNm [cl. 8.2.1.2]"
                         .format(round(self.plate.moment_demand/1000000,2)))
            logger.warning(":Moment capacity of plate is {} kN-m" .format(round(self.supported_section.moment_capacity/1000000,2)))
            logger.info(": Increase the plate thickness or material grade")
            logger.info(": Arranging bolts in one line will reduce moment induced")

        if self.weld.strength < self.weld.stress:
            # t_weld_req = self.weld.size * self.weld.stress / self.weld.strength
            self.weld.design_status = False
            logger.error(": Weld thickness is not sufficient [cl. 10.5.7, IS 800:2007]")
            logger.warning(": Weld stress is {}N/mm and current weld strength is {} N/mm".format(self.weld.stress,self.weld.strength))
            logger.info(": Should increase length of weld/fin plate")
        else:
            self.weld.design_status = True

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
                                                    self.supported_section.low_shear_capacity)

        if self.supported_section.shear_capacity < self.load.shear_force * 1000:
            self.supported_section.design_status = False
            logger.warning(
                'shear capacity of section is guiding plate height, current height {} mm' .format(self.plate.height))
        else:
            self.supported_section.design_status = True

        self.supported_section.tension_rupture_capacity = IS800_2007.cl_6_3_1_tension_rupture_strength(A_vn, self.supported_section.fu)
        A_tg = ((n_row - 1) * pitch) * web_thick
        A_tn = ((n_row - 1) * pitch - (float(n_row) - 1.0) * bolt_hole_dia) * web_thick
        A_vg = 2 * ((n_col - 1) * gauge + edge) * web_thick
        A_vn = 2 * ((n_col - 1) * gauge + edge - (float(n_col) - 0.5) * bolt_hole_dia) * web_thick

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
            logger.warning(
                'tension capacity of section is guiding plate height, current height {} mm' .format(self.plate.height))
        else:
            self.supported_section.design_status = True

        self.supported_section.moment_capacity = IS800_2007.cl_8_2_1_2_design_moment_strength\
            (self.supported_section.elast_sec_mod_z, self.supported_section.plast_sec_mod_z, self.supported_section.fy, 'plastic')

        if self.supported_section.moment_capacity < self.plate.moment_demand:
            logger.warning(
                'Moment capacity of section is less than moment demand, choose bigger section or increase section material strength')
            self.supported_section.design_status = False
        else:
            self.supported_section.design_status = True

        self.supported_section.IR = round(self.plate.moment_demand / self.supported_section.moment_capacity + (
                    self.load.axial_force * 1000) / self.supported_section.tension_capacity, 2)

        if self.supported_section.IR > 1 or self.supported_section.moment_capacity < self.plate.moment_demand or\
                self.supported_section.tension_capacity < self.load.axial_force * 1000 or \
                self.supported_section.shear_capacity < self.load.shear_force * 1000:
            logger.warning(
                'Axial - Moment interaction ratio of section is guiding plate height, current height {} mm' .format(self.plate.height))
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
        self.plate.low_shear_capacity = 0.6 * self.plate.shear_yielding_capacity
        A_vn = (self.plate.height - float(n_row) * bolt_hole_dia) * p_th
        self.plate.shear_rupture_capacity = AISC.cl_j_4_2_b_shear_rupture(A_vn,self.plate.fu)

        self.plate.shear_capacity = min(self.plate.block_shear_capacity_shear, self.plate.shear_rupture_capacity,
                                        self.plate.low_shear_capacity)

        if self.plate.shear_capacity < self.load.shear_force*1000:
            self.plate.design_status_capacity = False
            logger.warning(
                'shear capacity of section is guiding plate height, current height {} mm' .format(self.plate.height))
        else:
            self.plate.design_status_capacity = True
        A_g = self.plate.height * self.plate.thickness_provided
        self.plate.tension_yielding_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g, self.plate.fy)

        A_n = (self.plate.height - self.plate.bolt_line * self.bolt.dia_hole) * self.plate.thickness_provided

        self.plate.tension_rupture_capacity = IS800_2007.cl_6_3_1_tension_rupture_strength(A_n,self.plate.fu)
        plate_A_tg = ((n_row - 1) * pitch) * p_th
        plate_A_tn = ((n_row - 1) * pitch - (float(n_row) - 1.0) * bolt_hole_dia) * p_th
        plate_A_vg = 2 * ((n_col - 1) * gauge + edge) * p_th
        plate_A_vn = 2 * ((n_col - 1) * gauge + edge - (float(n_col) - 0.5) * bolt_hole_dia) * p_th

        self.plate.block_shear_capacity_axial = IS800_2007.cl_6_4_1_block_shear_strength(plate_A_vg, plate_A_vn,
                                                                                         plate_A_tg,
                                                                                         plate_A_tn, self.plate.fu,
                                                                                         self.plate.fy)
        self.plate.tension_capacity = min(self.plate.tension_rupture_capacity, self.plate.tension_yielding_capacity,
                                          self.plate.block_shear_capacity_axial)

        if self.plate.tension_capacity < self.load.axial_force*1000:
            self.plate.design_status_capacity = False
            logger.warning(
                'tension capacity of plate is guiding plate height, current height {} mm' .format(self.plate.height))
        else:
            self.plate.design_status_capacity = True

        Z_p = self.plate.height**2 * p_th / 4
        Z_e = self.plate.height**2 * p_th / 6
        self.plate.moment_capacity = IS800_2007.cl_8_2_1_2_design_moment_strength(Z_e, Z_p, self.plate.fy, 'plastic')

        if self.plate.moment_capacity < self.plate.moment_demand:
            logger.warning(
                'Moment capacity of plate is guiding plate height, current height {} mm'.format(self.plate.height))
            self.plate.design_status_capacity = False
        else:
            self.plate.design_status_capacity = True

        self.plate.IR = round(self.plate.moment_demand/self.plate.moment_capacity + (self.load.axial_force*1000)/self.plate.tension_capacity,2)
        if self.plate.IR > 1 or self.plate.shear_capacity < self.load.shear_force*1000 or self.plate.moment_capacity < self.plate.moment_demand:
            logger.warning(
                'Moment-Axial interaction ratio of plate is guiding plate height, current height {} mm'.format(self.plate.height))
            self.plate.design_status_capacity = False
        else:
            self.plate.design_status_capacity = True

    def get_available_welds(self, connecting_members=[]):

        weld_size_max = math.ceil(min(connecting_members))
        weld_size_min = math.ceil(IS800_2007.cl_10_5_2_3_min_weld_size(connecting_members[0], connecting_members[1]))
        if 7 <= weld_size_max < max(ALL_WELD_SIZES) and weld_size_max % 2 != 0:
            weld_size_max = round_up(weld_size_max, 2)

        if weld_size_max == weld_size_min:
            logger.info("Minimum weld size given in Table 21 of IS800:2007 is greater than or equal to thickness of thinner connecting plate")
            logger.info("Thicker plate shall be adequately preheated to prevent cracking of the weld")

        available_welds = list([x for x in ALL_WELD_SIZES if (weld_size_min <= x <= weld_size_max)])
        return available_welds,weld_size_min,weld_size_max

    def design_weld(self,available_welds):

        self.weld.length = self.plate.height
        force_l = self.load.shear_force * 1000
        force_w = self.load.axial_force*1000
        force_t = self.plate.moment_demand

        for self.weld.size in available_welds:
            self.weld.eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
                fillet_size=self.weld.size, available_length=self.weld.length)
            self.weld.throat_tk = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
                fillet_size=self.weld.size, fusion_face_angle=90)
            Ip_weld = 2 * self.weld.eff_length ** 3 / 12
            y_max = self.weld.eff_length / 2
            x_max = 0
            self.weld.get_weld_strength(connecting_fu=[self.supporting_section.fu, self.plate.fu, self.weld.fu],
                                        weld_fabrication=self.weld.fabrication,
                                        t_weld=self.weld.size, weld_angle=90)
            self.weld.get_weld_stress(weld_axial=force_w, weld_shear=force_l, weld_twist=force_t, Ip_weld=Ip_weld,
                                      y_max=y_max,
                                      x_max=x_max, l_weld=2 * self.weld.eff_length)
            if self.weld.strength > self.weld.stress:
                self.weld.design_status = True
                break

        if self.weld.strength < self.weld.stress:
            self.weld.design_status = False
            logger.info('weld stress is guiding plate dimensions, current length {} mm, thickness {} mm,'
                           ' weld size {} mm'.format(self.plate.height,self.plate.thickness_provided,self.weld.size))

    def get_design_status(self):
        if self.plate.design_status is True and self.weld.design_status is True:
            self.design_status = True
            logger.info("=== End Of Design ===")

    # def h_recalc_check(self):
    #     h_recalc = (self.plate.gauge_provided + 5) * (self.plate.bolts_one_line - 1) + self.plate.edge_dist_provided
    #     v_res = self.plate.get_vres(self.plate.bolts_one_line, self.plate.pitch_provided,self.plate.gauge_provided,
    #                                 self.plate.bolt_line,self.load.shear_force*1000,self.load.axial_force*1000, )

    #############################
    # End of Calculations
    #############################
    # Function to create input output dictionary for testing
    #############################
    def results_to_test(self):
        test_in_list = {KEY_MODULE: self.module,
                        KEY_MAIN_MODULE: self.mainmodule,
                        KEY_CONN: self.connectivity,
                        KEY_MATERIAL: self.plate.material,
                        KEY_SHEAR: self.load.shear_force,
                        KEY_AXIAL:self.load.axial_force,
                        KEY_SUPTNGSEC:self.supporting_section.designation,
                        KEY_SUPTNGSEC_MATERIAL:self.supporting_section.material,
                        KEY_SUPTNGSEC_FU:self.supporting_section.fu,
                        KEY_SUPTNGSEC_FY:self.supporting_section.fy,
                        KEY_SUPTDSEC:self.supported_section.designation,
                        KEY_SUPTDSEC_MATERIAL: self.supported_section.material,
                        KEY_SUPTDSEC_FU: self.supported_section.fu,
                        KEY_SUPTDSEC_FY: self.supported_section.fy,
                        KEY_D: self.bolt.bolt_diameter,
                        KEY_GRD: self.bolt.bolt_grade,
                        KEY_TYP: self.bolt.bolt_type,
                        KEY_DP_BOLT_TYPE:self.bolt.bolt_type,
                        KEY_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
                        KEY_DP_BOLT_SLIP_FACTOR: self.bolt.mu_f,
                        KEY_PLATETHK: self.plate.thickness,
                        KEY_CONNECTOR_MATERIAL: self.plate.material,
                        KEY_CONNECTOR_FU: self.plate.fu,
                        KEY_CONNECTOR_FY_20: self.plate.fy_20,
                        KEY_CONNECTOR_FY_20_40: self.plate.fy_20_40,
                        KEY_CONNECTOR_FY_40: self.plate.fy_40,
                        KEY_DP_WELD_TYPE: 'Fillet',
                        KEY_DP_WELD_FAB: self.weld.fabrication,
                        KEY_DP_WELD_MATERIAL_G_O: self.weld.fu,
                        KEY_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
                        KEY_DP_DETAILING_GAP: self.plate.gap,
                        KEY_DP_DETAILING_CORROSIVE_INFLUENCES: self.bolt.corrosive_influences}

        test_out_list = {KEY_OUT_D_PROVIDED:self.bolt.bolt_diameter_provided,
                        KEY_OUT_GRD_PROVIDED:self.bolt.bolt_grade_provided,
                        KEY_OUT_BOLT_SHEAR:self.bolt.bolt_shear_capacity,
                        KEY_OUT_BOLT_BEARING:self.bolt.bolt_bearing_capacity,
                        KEY_OUT_BOLT_CAPACITY:self.bolt.bolt_capacity,
                        KEY_OUT_BOLT_FORCE:self.plate.bolt_force,
                        KEY_OUT_BOLT_LINE:self.plate.bolt_line,
                        KEY_OUT_BOLTS_ONE_LINE:self.plate.bolts_one_line,
                        KEY_OUT_GAUGE:self.plate.pitch_provided,
                        KEY_OUT_EDGE_DIST:self.plate.end_dist_provided,
                         KEY_OUT_PITCH: self.plate.gauge_provided,
                         KEY_OUT_END_DIST: self.plate.edge_dist_provided,
                        KEY_OUT_PLATETHK:self.plate.thickness_provided,
                        KEY_OUT_PLATE_HEIGHT:self.plate.height,
                        KEY_OUT_PLATE_LENGTH:self.plate.length,
                        KEY_OUT_PLATE_SHEAR:self.plate.low_shear_capacity,
                        KEY_OUT_PLATE_RUPTURE: self.plate.shear_rupture_capacity,
                        KEY_OUT_PLATE_BLK_SHEAR:self.plate.block_shear_capacity_shear,
                        KEY_OUT_PLATE_TENSION: self.plate.tension_yielding_capacity,
                        KEY_OUT_PLATE_TENSION_RUP: self.plate.tension_rupture_capacity,
                        KEY_OUT_PLATE_BLK_SHEAR_AXIAL: self.plate.block_shear_capacity_axial,
                        KEY_OUT_PLATE_MOM_DEMAND:self.plate.moment_demand,
                        KEY_OUT_PLATE_MOM_CAPACITY:self.plate.moment_capacity,
                         KEY_SHEAR_YIELDCAPACITY: self.supported_section.low_shear_capacity,
                         KEY_SHEAR_RUPTURECAPACITY: self.supported_section.shear_rupture_capacity,
                         KEY_SHEAR_BLOCKSHEARCAPACITY: self.supported_section.block_shear_capacity_shear,
                         KEY_TENSION_YIELDCAPACITY: self.supported_section.tension_yielding_capacity,
                         KEY_TENSION_RUPTURECAPACITY: self.supported_section.tension_rupture_capacity,
                         KEY_TENSION_BLOCKSHEARCAPACITY: self.supported_section.block_shear_capacity_axial,
                         KEY_MEMBER_MOM_CAPACITY: self.supported_section.moment_capacity,
                        KEY_OUT_WELD_SIZE:self.weld.size,
                        KEY_OUT_WELD_STRENGTH:self.weld.strength,
                        KEY_OUT_WELD_STRESS:self.weld.stress}
        return test_in_list, test_out_list

    ######################################
    # Function to create design report (LateX/PDF)
    ######################################
    def save_design(self,popup_summary):
        super(FinPlateConnection,self).save_design(self)
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")

        self.report_check = []
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

        if self.plate.design_status is False:
            t1 = ('SubSection', 'Section Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            a = self.supported_section
            h = a.web_height
            t = a.web_thickness
            t1 = (KEY_DISP_SHEAR_CAPACITY, self.load.shear_force,
                  shear_yield_prov(h, t, a.fy, gamma_m0, round(a.shear_yielding_capacity/1000,2)),
                  get_pass_fail(self.load.shear_force, round(a.shear_yielding_capacity/1000,2), relation="lesser"))
            self.report_check.append(t1)

            t1 = (KEY_DISP_ALLOW_SHEAR, self.load.shear_force,
                  allow_shear_capacity(round(a.shear_yielding_capacity/1000,2), round(a.low_shear_capacity/1000,2)),
                  get_pass_fail(self.load.shear_force, round(a.low_shear_capacity/1000,2), relation="lesser"))
            self.report_check.append(t1)

            t1 = (KEY_DISP_TENSION_CAPACITY, self.load.axial_force,
                  tension_yield_prov(h, t, a.fy, gamma_m0, round(a.tension_yielding_capacity/1000, 2)),
                  get_pass_fail(self.load.axial_force, round(a.tension_yielding_capacity/1000, 2), relation="lesser"))
            self.report_check.append(t1)

        if not self.thickness_possible and self.supported_section.design_status_initial is True:
            t1 = ('SubSection', 'Minimum Plate thickness check', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t1 = (DISP_MIN_PLATE_THICK, min_plate_thk_req(self.supported_section.web_thickness),
                  self.plate.thickness_provided,
                  get_pass_fail(self.supported_section.web_thickness, self.plate.thickness_provided,
                                relation="lesser"))
            self.report_check.append(t1)

        elif self.supported_section.design_status_initial is True:

            t1 = ('SubSection', 'Load Consideration', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            min_shear_load = min(40, round(0.15 * self.supported_section.shear_yielding_capacity / 0.6, 2))
            applied_shear_force = max(self.load.shear_force, min_shear_load)

            t1 = (KEY_DISP_APPLIED_SHEAR_LOAD, self.load.shear_force,
                  prov_shear_load(shear_input=self.load.shear_force, min_sc=min_shear_load,
                                  app_shear_load=applied_shear_force,
                                  shear_capacity_1=round(self.supported_section.shear_yielding_capacity/1000,2)), "")
            self.report_check.append(t1)

            t1 = (KEY_DISP_APPLIED_SHEAR_LOAD, self.load.axial_force, self.load.axial_force, "")
            self.report_check.append(t1)

            connecting_plates = [self.plate.thickness_provided,self.supported_section.web_thickness]
            bolt_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2)
            bolt_force_kn=round(self.plate.bolt_force/1000,2)
            bolt_capacity_red_kn=round(self.plate.bolt_capacity_red/1000,2)

            t1 = ('SubSection', 'Bolt Design Checks','|p{4cm}|p{5.5cm}|p{5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t1 = (KEY_DISP_D, '', self.bolt.bolt_diameter_provided, '')
            self.report_check.append(t1)
            t1 = (KEY_DISP_GRD, '', self.bolt.bolt_grade_provided, '')
            self.report_check.append(t1)
            t1 = (KEY_DISP_PLTHICK, min_plate_thk_req(self.supported_section.web_thickness),
                  self.plate.thickness_provided,
                  get_pass_fail(self.supported_section.web_thickness, self.plate.thickness_provided, relation="lesser"))
            self.report_check.append(t1)
            t6 = (DISP_NUM_OF_COLUMNS, '', self.plate.bolt_line, '')
            self.report_check.append(t6)
            t7 = (DISP_NUM_OF_ROWS, '', self.plate.bolts_one_line, '')
            self.report_check.append(t7)
            t1 = (DISP_MIN_PITCH, cl_10_2_2_min_spacing(self.bolt.bolt_diameter_provided),
                  self.plate.gauge_provided, get_pass_fail(self.bolt.min_pitch, self.plate.gauge_provided,relation='leq'))
            self.report_check.append(t1)
            if self.plate.design_status is True:
                t1 = (DISP_MAX_PITCH, cl_10_2_3_1_max_spacing(connecting_plates),
                      self.plate.gauge_provided, get_pass_fail(self.bolt.max_spacing, self.plate.gauge_provided,relation='geq'))
                self.report_check.append(t1)
                t2 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(self.bolt.bolt_diameter_provided),
                      self.plate.pitch_provided, get_pass_fail(self.bolt.min_gauge, self.plate.pitch_provided,relation="leq"))
                self.report_check.append(t2)
                t2 = (DISP_MAX_GAUGE, cl_10_2_3_1_max_spacing(connecting_plates),
                      self.plate.pitch_provided, get_pass_fail(self.bolt.max_spacing, self.plate.pitch_provided,relation="geq"))
                self.report_check.append(t2)
            t3 = (DISP_MIN_END, cl_10_2_4_2_min_edge_end_dist(d_0=self.bolt.dia_hole,
                                                               edge_type=self.bolt.edge_type, parameter='end_dist'),
                  self.plate.edge_dist_provided, get_pass_fail(self.bolt.min_end_dist, self.plate.edge_dist_provided,relation='leq'))
            self.report_check.append(t3)
            if self.plate.design_status is True:
                t4 = (DISP_MAX_END, cl_10_2_4_3_max_edge_end_dist(self.bolt_conn_plates_t_fu_fy, self.bolt.corrosive_influences,
                                                                  parameter='end_dist'),
                      self.plate.edge_dist_provided, get_pass_fail(self.bolt.max_end_dist, self.plate.edge_dist_provided,relation='geq'))
                self.report_check.append(t4)
                t3 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(d_0=self.bolt.dia_hole,
                                                                   edge_type=self.bolt.edge_type, parameter='edge_dist'),
                      self.plate.end_dist_provided, get_pass_fail(self.bolt.min_edge_dist, self.plate.end_dist_provided,relation='leq'))
                self.report_check.append(t3)
                t4 = (DISP_MAX_EDGE, cl_10_2_4_3_max_edge_end_dist(self.bolt_conn_plates_t_fu_fy, self.bolt.corrosive_influences,
                                                                   parameter='edge_dist'),
                      self.plate.end_dist_provided, get_pass_fail(self.bolt.max_edge_dist, self.plate.end_dist_provided,relation="geq"))
                self.report_check.append(t4)
            if self.plate.design_status is False:
                t1 = (DISP_MAX_PLATE_HEIGHT, max_plate_ht_req(self.connectivity, self.supported_section.depth,
                                                              self.supported_section.flange_thickness,
                                                              self.supported_section.root_radius,
                                                              self.supported_section.notch_ht,
                                                              self.max_plate_height), self.plate.height,
                      get_pass_fail(self.max_plate_height, self.plate.height, relation="greater"))
                self.report_check.append(t1)

            else:
                t10 = (KEY_OUT_REQ_MOMENT_DEMAND_BOLT, '', moment_demand_req_bolt_force(
                    shear_load=round(self.load.shear_force, 2),
                    web_moment=0.0, ecc=self.plate.ecc,
                    moment_demand=round(self.plate.moment_demand / 1000000, 2)), '')

                self.report_check.append(t10)

                t10 = (KEY_OUT_REQ_PARA_BOLT, parameter_req_bolt_force(bolts_one_line=self.plate.bolts_one_line
                                                                           , gauge=self.plate.gauge_provided,
                                                                           ymax=round(self.plate.ymax, 2),
                                                                           xmax=round(self.plate.xmax, 2),
                                                                           bolt_line=self.plate.bolt_line,
                                                                           pitch=self.plate.pitch_provided,
                                                                           length_avail=self.plate.length_avail,conn='fin'), '', '')
                self.report_check.append(t10)



                t10 = (KEY_OUT_BOLT_FORCE, Vres_bolts(bolts_one_line=self.plate.bolts_one_line,
                                                          ymax=round(self.plate.ymax, 2),
                                                          xmax=round(self.plate.xmax, 2),
                                                          bolt_line=self.plate.bolt_line,
                                                          shear_load=round(self.load.shear_force, 2),
                                                          axial_load=round(self.load.axial_force, 2),
                                                          moment_demand=round(self.plate.moment_demand / 1000000, 2),
                                                          r=round(self.plate.sigma_r_sq / 1000, 2),
                                                          vbv=round(self.plate.vbv / 1000, 2),
                                                          tmv=round(self.plate.tmv / 1000, 2),
                                                          tmh=round(self.plate.tmh / 1000, 2),
                                                          abh=round(self.plate.abh / 1000, 2),
                                                          vres=round(self.plate.bolt_force / 1000, 2)), '', '')
                self.report_check.append(t10)
                if self.bolt.bolt_type == TYP_BEARING:
                    bolt_shear_capacity_kn = round(self.bolt.bolt_shear_capacity / 1000, 2)
                    bolt_bearing_capacity_kn = round(self.bolt.bolt_bearing_capacity / 1000, 2)
                    t1 = (KEY_OUT_DISP_BOLT_SHEAR, '', bolt_shear_prov(self.bolt.bolt_fu,1,self.bolt.bolt_net_area,
                                                                       self.bolt.gamma_mb,bolt_shear_capacity_kn), '')
                    self.report_check.append(t1)
                    t8 = (KEY_DISP_KB, " ", kb_prov(self.plate.edge_dist_provided, self.plate.gauge_provided, self.bolt.dia_hole,
                                              self.bolt.bolt_fu, self.bolt.fu_considered), '')
                    self.report_check.append(t8)
                    t2 = (KEY_OUT_DISP_BOLT_BEARING, '', bolt_bearing_prov(self.bolt.kb,self.bolt.bolt_diameter_provided,
                                                                           self.bolt_conn_plates_t_fu_fy,self.bolt.gamma_mb,
                                                                           bolt_bearing_capacity_kn), '')
                    self.report_check.append(t2)
                    t3 = (KEY_OUT_DISP_BOLT_CAPACITY, '',
                          bolt_capacity_prov(bolt_shear_capacity_kn,bolt_bearing_capacity_kn,bolt_capacity_kn),
                          '')
                    self.report_check.append(t3)
                else:
                    kh_disp = round(self.bolt.kh, 2)
                    t4 = (KEY_OUT_DISP_BOLT_SLIP, '',
                          HSFG_bolt_capacity_prov(mu_f=self.bolt.mu_f,n_e=1,K_h=kh_disp,fub = self.bolt.bolt_fu,
                                                  Anb= self.bolt.bolt_net_area,gamma_mf=self.bolt.gamma_mf,
                                                  capacity=bolt_capacity_kn),'')
                    self.report_check.append(t4)


                t10 = (KEY_OUT_LONG_JOINT, long_joint_bolted_req(),
                       long_joint_bolted_prov(self.plate.bolt_line,self.plate.bolts_one_line,
                                              self.plate.pitch_provided,self.plate.gauge_provided,
                                              self.bolt.bolt_diameter_provided,bolt_capacity_kn,bolt_capacity_red_kn,'n_r'), "")
                self.report_check.append(t10)

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
                t1 = (DISP_MIN_PLATE_WIDTH, min_plate_length_req(self.bolt.min_pitch, self.bolt.min_end_dist,
                                                              self.plate.bolt_line,min_plate_length), self.plate.length,
                      get_pass_fail(min_plate_length, self.plate.length, relation="lesser"))
                self.report_check.append(t1)
                t1 = (DISP_MIN_PLATE_THICK, min_plate_thk_req(self.supported_section.web_thickness), self.plate.thickness_provided,
                      get_pass_fail(self.supported_section.web_thickness, self.plate.thickness_provided, relation="lesser"))
                self.report_check.append(t1)

                #######################
                # Plate and Section Capacities
                #######################
                for a in [self.plate,self.supported_section]:

                    if a == self.plate:
                        h = a.height
                        t = a.thickness_provided
                    else:
                        t1 = ('SubSection', 'Section Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                        self.report_check.append(t1)
                        h = a.web_height
                        t = a.web_thickness

                    t1 = (KEY_DISP_SHEAR_YLD, '', shear_yield_prov(h,t,a.fy, gamma_m0,
                                                                   round(a.shear_yielding_capacity / 1000, 2)),'')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_ALLOW_SHEAR, display_prov(self.load.shear_force, "V"),
                          allow_shear_capacity(round(a.shear_yielding_capacity/1000,2), round(a.low_shear_capacity/1000,2)),
                          get_pass_fail(self.load.shear_force, round(a.low_shear_capacity/1000,2), relation="lesser"))
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_SHEAR_RUP, '', shear_rupture_prov(h,t, self.plate.bolts_one_line, self.bolt.dia_hole,
                                                                     a.fu,round(a.shear_rupture_capacity / 1000, 2)),'')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_PLATE_BLK_SHEAR_SHEAR, '', blockshear_prov(Tdb=round(a.block_shear_capacity_shear/1000, 2),stress='shear'), '')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_SHEAR_CAPACITY, self.load.shear_force,
                          shear_capacity_prov(round(a.low_shear_capacity / 1000, 2),
                                              round(a.shear_rupture_capacity / 1000, 2),
                                              round(a.block_shear_capacity_shear / 1000, 2)),
                          get_pass_fail(self.load.shear_force, round(a.shear_capacity / 1000, 2), relation="lesser"))
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_TENSION_YIELDCAPACITY, '',
                          tension_yield_prov(h,t, a.fy, gamma_m0,round(a.tension_yielding_capacity / 1000, 2)), '')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '',
                          tension_rupture_bolted_prov(h,t,self.plate.bolts_one_line, self.bolt.dia_hole,
                                                      a.fu, gamma_m1,round(a.tension_rupture_capacity / 1000, 2)), '')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_PLATE_BLK_SHEAR_TENSION, '', blockshear_prov(Tdb=round(a.block_shear_capacity_axial/1000, 2),stress='axial'), '')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_TENSION_CAPACITY, self.load.axial_force,
                          tensile_capacity_prov(round(a.tension_yielding_capacity / 1000, 2),
                                                round(a.tension_rupture_capacity / 1000, 2),
                                                round(a.block_shear_capacity_axial / 1000, 2)),
                          get_pass_fail(self.load.axial_force, round(a.tension_capacity / 1000, 2), relation="lesser"))
                    self.report_check.append(t1)

                    t1 = (KEY_OUT_DISP_PLATE_MOM_CAPACITY, round(self.plate.moment_demand / 1000000, 2),
                          round(a.moment_capacity / 1000000, 2),
                          get_pass_fail(self.plate.moment_demand, a.moment_capacity, relation="lesser"))
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_IR, IR_req(IR=1),
                          IR_prov(round(self.plate.moment_demand / 1000000, 2),
                                            round(a.moment_capacity / 1000000, 2),
                                            self.load.axial_force, round(a.tension_capacity / 1000, 2), a.IR),
                          get_pass_fail(1, a.IR, relation="greater"))
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
                      get_pass_fail(self.weld_size_max, self.weld.size, relation="geq"))
                self.report_check.append(t1)
                Ip_weld = round(2 * self.weld.eff_length ** 3 / 12,2)
                weld_conn_plates_fu = [self.supporting_section.fu, self.plate.fu]
                gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.weld.fabrication]
                if Ip_weld != 0.0:
                    t1 = (DISP_WELD_STRENGTH, weld_strength_req(V=self.load.shear_force*1000,A=self.load.axial_force*1000,
                                                                M=self.plate.moment_demand,Ip_w=Ip_weld,
                                                                y_max= self.weld.eff_length/2,x_max=0.0,l_w=2*self.weld.eff_length,
                                                                R_w=self.weld.stress),
                          weld_strength_prov(weld_conn_plates_fu, gamma_mw, self.weld.throat_tk,self.weld.strength),
                          get_pass_fail(self.weld.stress, self.weld.strength, relation="lesser"))
                    self.report_check.append(t1)

        Disp_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext, rel_path, Disp_3D_image)

    ######################################
    # Function for individual component calls in 3D view
    ######################################
    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('Fin Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Fin Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Plate", bgcolor)
