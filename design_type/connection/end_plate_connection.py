"""
Started on 1st February, 2020.

@author: sourabhdas

Module: Shear End plate connection

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel structures by Dr. N Subramanian (chapter 5 and 6)
            3) Fundamentals of Structural steel design by M.L Gambhir
            4) AISC Design Examples V14

ASCII diagram

            +-+-------------+-+
            | |             | |
            | |             | |
            | |             | |
            | |             | |   +-------------------------+
            | |             | |   |-------------------------|
            | |             | |   |
            | |             | | _ |
            | |             | || ||
            | |         +---|-||-||--+
            | |         +---|-||-||--+
            | |             | || ||
            | |         +---|-||-||--+
            | |         +---|-||-||--+
            | |             | || ||
            | |         +---|-||-||--+
            | |         +---|-||-||--+
            | |             | ||_||
            | |             | |   |
            | |             | |   |
            | |             | |   |-------------------------|
            | |             | |   +-------------------------+
            | |             | |
            | |             | |
            +-+-------------+-+

"""
from design_type.connection.shear_connection import ShearConnection
from utils.common.component import *
from utils.common.material import *
from Common import *
from design_report.reportGenerator_latex import CreateLatex
from Report_functions import *
import logging


class EndPlateConnection(ShearConnection):

    def __init__(self,):
        super(EndPlateConnection, self).__init__()
        # self.plate = Plate(thickness=self.plate.thickness_provided, height=plate_height, width=plate_width, material=self.material)
        # self.weld = Weld(material_grade=design_dictionary[KEY_MATERIAL], fabrication=design_dictionary[KEY_DP_WELD_TYPE])
        self.weld_size_list = []
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
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        t7 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

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

    def get_values_for_design_pref(self, key, design_dictionary):

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            fu = Material(design_dictionary[KEY_MATERIAL],41).fu
        else:
            fu = ''

        val = {KEY_DP_BOLT_TYPE: "Pretensioned",
               KEY_DP_BOLT_HOLE_TYPE: "Standard",
               KEY_DP_BOLT_SLIP_FACTOR: str(0.3),
               KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
               KEY_DP_DETAILING_GAP: '0',
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No',
               KEY_DP_DESIGN_METHOD: "Limit State Design",
               KEY_CONNECTOR_MATERIAL: str(design_dictionary[KEY_MATERIAL])
               }[key]

        return val
    ####################################
    # Design Preference Functions End
    ####################################

    def set_osdaglogger(key):
        """
        Function to set Logger for End Plate Module
        """
        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            # handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def module_name(self):
        return KEY_DISP_ENDPLATE

    def input_values(self):

        """
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        """

        # @author: Amir, Umair
        self.module = KEY_DISP_ENDPLATE
        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_ENDPLATE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, VALUES_CONN, True, 'No Validator')
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, './ResourceFiles/images/fin_cf_bw.png', True, 'No Validator')
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, VALUES_COLSEC, True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, VALUES_BEAMSEC, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_ALL_CUSTOMIZED, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_PC, TYPE_COMBOBOX_CUSTOMIZED, VALUES_ALL_CUSTOMIZED, True, 'No Validator')
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, VALUES_ALL_CUSTOMIZED, True, 'No Validator')
        options_list.append(t14)

        return options_list

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
        super(EndPlateConnection,self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O], fabrication=design_dictionary[KEY_DP_WELD_FAB])
        # self.weld = Weld(size=10, length= 100, material_grade=design_dictionary[KEY_MATERIAL])
        print("Input values set to perform preliminary member check(s).")
        self.member_capacity(self)

    def member_capacity(self):
        super(EndPlateConnection, self).member_capacity(self)
        if self.connectivity == VALUES_CONN_2[0]:
            if self.supported_section.shear_yielding_capacity / 1000 > self.load.shear_force and \
                    self.supported_section.tension_yielding_capacity / 1000 > self.load.axial_force:

                if self.load.shear_force <= min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                                40.0):
                    logger.warning(" : The value of factored shear force is less than the minimum recommended value. "
                                   "Setting shear force value to 15% of supported beam shear capacity or 40 kN, whichever is lesser"
                                   "[Ref. IS 800:2007, Cl.10.7].")
                    self.load.shear_force = min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                                40.0)

                print("Preliminary member check(s) have passed. Checking available bolt diameter(s).")
                self.select_bolt_plate_arrangement(self)

            else:
                self.design_status = False
                if self.supported_section.shear_yielding_capacity / 1000 < self.load.shear_force:
                    logger.error(" : The shear yielding capacity of the supported section, ({} kN) is less "
                                 "than the factored shear force. Please select a larger section or decrease load."
                                 .format(round(self.supported_section.shear_yielding_capacity/1000, 2)))
                else:  # self.supported_section.tension_yielding_capacity / 1000 < self.load.axial_force:
                    logger.error(" : The tension yielding capacity of the supported section, ({} kN) is less "
                                 "than the factored axial force. Please select a larger section or decrease load."
                                 .format(round(self.supported_section.tension_yielding_capacity/1000, 2)))
                print("The preliminary member check(s) have failed. Select a large/larger section(s) or decrease load and re-design.")
        else:
            if self.supported_section.shear_yielding_capacity / 1000 > self.load.shear_force and \
                    self.supported_section.tension_yielding_capacity / 1000 > self.load.axial_force and \
                    self.supporting_section.tension_yielding_capacity / 1000 > self.load.shear_force:

                if self.load.shear_force <= min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                                40.0):
                    logger.warning(" : The value of factored shear force is less than the minimum recommended value. "
                                   "Setting the value of the shear force to 15% of the supported beam shear capacity or 40 kN, whichever is lesser "
                                   "[Ref. IS 800:2007, Cl.10.7].")
                    self.load.shear_force = min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                                40.0)
                print("Preliminary member check(s) have passed. Checking available bolt diameter(s).")
                self.select_bolt_plate_arrangement(self)

            else:
                self.design_status = False
                if self.supported_section.shear_yielding_capacity / 1000 < self.load.shear_force:
                    logger.error(" : The shear yielding capacity of the supported section, ({} kN) is less "
                                 "than the factored shear force. Please select a larger section or decrease load."
                                 .format(round(self.supported_section.shear_yielding_capacity/1000, 2)))
                if self.supported_section.tension_yielding_capacity / 1000 < self.load.axial_force:
                    logger.error(" : The tension yielding capacity of the supported section, ({} kN) is less "
                                 "than the factored axial force. Please select a larger section or decrease load."
                                 .format(round(self.supported_section.tension_yielding_capacity/1000, 2)))
                if self.supporting_section.tension_yielding_capacity / 1000 < self.load.shear_force:
                    logger.error(" : The axial yielding capacity of the supporting section, ({} kN) is less "
                                 "than the factored shear force. Please select a larger section or decrease load."
                                 .format(round(self.supporting_section.tension_yielding_capacity / 1000, 2)))
                print("The preliminary member check(s) have failed. Select a large/larger section(s) or decrease load and re-design.")

    def select_bolt_plate_arrangement(self):
        self.output = []
        self.failed_output_plate = []
        self.failed_output_bolt = []
        plate_width = 0.0
        pitch = 0.0
        gauge = 0.0
        end_dist =0.0
        weld_size_max = 0.0
        weld_size_min = 0.0
        count = 0
        self.beta_lj = 1.0
        self.beta_lg = 1.0
        self.beta_pk = 1.0
        plate_cost = 7850e-9 # considered: Rs 1 per kg TODO: take input from user
        bolt_cost = 1 # considered: Rs 1 per unit TODO: take input from user
        for self.plate.thickness_provided in sorted(self.plate.thickness):
            self.plate.connect_to_database_to_get_fy_fu(self.plate.material, self.plate.thickness_provided)
            self.design_status_plate = True
            self.design_status_plate_tk = True
            self.min_plate_height = self.supported_section.min_plate_height()
            self.supported_section.notch_ht = max((round_up(self.supporting_section.flange_thickness
                                                           + self.supporting_section.root_radius, 5) + 10),
                                                  (round_up(self.supported_section.flange_thickness
                                                           + self.supported_section.root_radius, 5) + 10))
            # print("Notch Height:", self.supported_section.notch_ht)
            self.max_plate_height = round(self.supported_section.max_plate_height(self.connectivity, self.supported_section.notch_ht),2)
            print("Max plate height: ", self.max_plate_height)
            # self.res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000
            # if self.connectivity == VALUES_CONN_1[1]:
            self.plate.thickness_check = max(min(self.plate.thickness), math.ceil(self.supported_section.web_thickness))

            if self.plate.thickness_check > max(self.plate.thickness):
                self.design_status_plate_tk = False
                self.design_status = False
                logger.error(" : Select plate(s) of higher thickness and re-design.")
                break

            for t in self.plate.thickness:
                if t >= self.plate.thickness_check:
                    self.plate.thickness_check = t
                    break

            if self.plate.thickness_provided < self.plate.thickness_check:
                self.design_status_plate_tk = False

            # TO GET BOLT BEARING CAPACITY CORRESPONDING TO PLATE THICKNESS AND Fu AND Fy #
            self.bolt_conn_plates_t_fu_fy = []
            self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
            if self.connectivity == VALUES_CONN_1[0]:
                self.bolt_conn_plates_t_fu_fy.append(
                    (self.supporting_section.flange_thickness, self.supporting_section.fu, self.supporting_section.fy))
            else:
                self.bolt_conn_plates_t_fu_fy.append(
                    (self.supporting_section.web_thickness, self.supporting_section.fu, self.supporting_section.fy))

            t_sum = self.plate.gap
            for i in self.bolt_conn_plates_t_fu_fy:
                t_sum = t_sum + i[0]
            print(t_sum)
            self.bolt.bolt_diameter_possible = []
            self.bolt.bolt_diameter_not_possible = []
            for d in self.bolt.bolt_diameter:
                if 8*d >= t_sum:
                    self.bolt.bolt_diameter_possible.append(d)
                else:
                    self.bolt.bolt_diameter_not_possible.append(d)
                    print("Removed bolt dia ", d, " mm from available bolt list for plate thickness ", self.plate.thickness_provided, " mm")
            # if self.connectivity == VALUES_CONN_1[1]:
            #     self.connecting_plates_tk = [self.plate.thickness_provided, self.supported_section.flange_thickness]
            # else:
            #  'FOR WELD CHECK (WELD BETWEEN END PLATE AND SUPPORTED SECTION WEB) #
            self.connecting_plates_tk = [self.plate.thickness_provided, self.supported_section.web_thickness]

            # res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000
            # self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]
            # bolt_diameter_previous = self.bolt.bolt_diameter[-1]
            # count = 0
            # bolts_one_line = 1

            if self.design_status_plate_tk is True and self.bolt.bolt_diameter_possible:
                for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter_possible):
                    bolts_required_initial = 4

                    for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
                        self.design_status_bolt = True
                        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                            conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)
                        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                      bolt_grade_provided=self.bolt.bolt_grade_provided,
                                                      conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                                      n_planes=1)
                        if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
                            bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
                            pass
                        else:
                            bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

                        self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                      bolt_grade_provided=self.bolt.bolt_grade_provided)
                    # print("Bolt tension capacity:", self.bolt.bolt_tension_capacity)
                    # print("Shear force:", self.load.shear_force)

                    #     self.bolts_required = bolts_required_initial
                        [available_welds, weld_size_min, weld_size_max] = self.get_available_welds(self, self.connecting_plates_tk)
                        col_g = (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius + self.bolt.min_end_dist_round)
                        beam_g = (self.supported_section.web_thickness / 2 + weld_size_min + self.bolt.min_end_dist_round)
                        if col_g > beam_g:
                            l_v = col_g - (self.supported_section.web_thickness / 2 + weld_size_min)
                        else:
                            l_v = self.bolt.min_edge_dist_round
                        b_e = min(self.bolt.min_pitch_round, 2 * l_v)
                        [self.bolt.bolt_shear,self.bolt.bolt_tension,self.bolt.bolt_tension_prying,
                            self.bolts_required_IR_LT1] = self.get_bolt_IR(self, self.bolt.bolt_capacity,
                                self.bolt.bolt_tension_capacity, bolts_required_initial, b_e, l_v,
                                self.bolt.min_pitch_round, 1.0, 1.0, 1.0)

                        print("Bolts required:", self.bolts_required_IR_LT1)

                    # return self.bolts_required
                        bolt_rows = self.bolts_required_IR_LT1/2

                        [bolt_line, bolts_one_line, web_plate_h] = \
                            self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height,
                                                                      bolt_rows, self.bolt.min_end_dist_round,
                                                                      self.bolt.min_gauge_round)

                        if bolt_rows > bolts_one_line:
                            self.design_status_bolt = False
                        # print("Dia of bolt:", self.bolt.bolt_diameter_provided)
                        # bolts_required_previous = self.bolts_required
                        # bolt_diameter_previous = self.bolt.bolt_diameter_provided
                        # print("Bolts diameter:", bolt_diameter_previous)

                        pitch = self.bolt.min_pitch_round
                        end_dist = self.bolt.min_end_dist_round

                        if web_plate_h > ((bolt_rows-1)*pitch + 2*end_dist):
                            [pitch, end_dist, web_plate_h] = self.plate.get_gauge_edge_dist(web_plate_h,
                                                bolt_rows, self.bolt.min_end_dist_round, self.max_plate_height,
                                                self.bolt.max_edge_dist_round)
                        elif web_plate_h < ((bolt_rows-1)*pitch + 2*end_dist):
                            web_plate_h = ((bolt_rows-1)*pitch + 2*end_dist)
                        # Updating bolt bearing capacity

                        if self.bolt.bolt_type == TYP_BEARING:
                            bolt_bearing_capacity_disp = self.get_bolt_bearing_updated(self, end_dist, pitch, bolt_rows, weld_size_min)

                        if self.connectivity == VALUES_CONN_1[0] and available_welds and\
                                (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius) > \
                                (self.supported_section.web_thickness / 2 + min(available_welds)):
                              self.bolt_dist_to_weld = (self.supporting_section.web_thickness / 2 +
                                                        self.supporting_section.root_radius +
                                                        self.bolt.min_edge_dist_round -
                                                        (self.supported_section.web_thickness / 2 + min(available_welds)))
                        else:
                            self.bolt_dist_to_weld = self.bolt.min_edge_dist_round

                        self.plate.height = web_plate_h
                        self.plate.plate_moment = self.bolt_dist_to_weld * self.bolt.bolt_tension
                        self.plate.plate_shear = self.load.shear_force

                        [self.plate.plate_moment_capacity, self.plate.shear_capacity,
                         self.plate.plate_block_shear_capacity] = \
                            self.get_plate_capacity(self, self.plate.thickness_provided, self.plate.height, pitch,
                                                    self.bolt_dist_to_weld, end_dist,
                                                    bolt_rows, self.bolt.dia_hole)
                        # print("plate_moment:", self.plate.plate_moment)
                        # print("plate_shear:", self.plate.plate_shear)
                        # print("plate_moment_capacity:", self.plate.plate_moment_capacity)
                        # print("shear_capacity:", self.plate.shear_capacity)

                        if self.plate.plate_moment > self.plate.plate_moment_capacity or \
                                self.plate.plate_shear > self.plate.shear_capacity:
                            self.design_status_plate = False
                            [bolt_rows, pitch, end_dist, self.design_status_plate] = self.plate_check(self, bolt_rows,
                                                                                pitch, end_dist, self.design_status_plate)
                        else:
                            self.design_status_plate = True

                        if self.design_status_bolt is True and self.design_status_plate is True:
                            [available_welds, weld_size_min, weld_size_max] = self.get_available_welds(self,
                                                                                        self.connecting_plates_tk)
                            print(available_welds)
                            if available_welds:
                                self.design_weld(self, available_welds)
                                # if self.weld.design_status is True:
                                #      break
                            # # else:
                            # #     #TODO: Check logger message
                            # #     logger.error(
                            # #         ": For given members and %2.2f mm thick plate, weld sizes should be of range %2.2f mm and  %2.2f mm "
                            # #         % self.plate.thickness_provided % weld_size_min % weld_size_max)
                            # #     logger.info(": Cannot design weld with available welds ")
                            print("Weld Status: ", self.weld.design_status)
                            # if self.weld.design_status is True:
                            plate_width = round_up(self.weld.size * 2 + self.bolt_dist_to_weld * 2 +
                                self.bolt.min_edge_dist_round * 2 + self.supported_section.web_thickness, 2)
                            self.plate_width_check(self, plate_width)

                            if self.plate.height >= web_plate_h:
                                [pitch, end_dist, self.plate.height, bolt_rows] = self.get_pitch_end_dist(self, self.plate.height,
                                                                                                bolt_rows,
                                                                                                self.bolt.min_end_dist_round,
                                                                                                self.bolt.max_spacing_round,
                                                                                                self.bolt.max_edge_dist_round,
                                                                                                self.weld.size)

                            if self.connectivity == VALUES_CONN_1[0] and min(available_welds) < self.weld.size and \
                                    (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius) > \
                                    (self.supported_section.web_thickness / 2 + self.weld.size):
                                self.bolt_dist_to_weld = (self.supporting_section.web_thickness / 2 +
                                                          self.supporting_section.root_radius +
                                                          self.bolt.min_edge_dist_round -
                                                          (self.supported_section.web_thickness / 2 + self.weld.size))
                            self.plate.plate_moment = self.bolt_dist_to_weld * self.bolt.bolt_tension
                            [self.plate.plate_moment_capacity, self.plate.shear_capacity,
                             self.plate.plate_block_shear_capacity] = \
                                self.get_plate_capacity(self, self.plate.thickness_provided, self.plate.height, pitch,
                                                        self.bolt_dist_to_weld, end_dist,
                                                        bolt_rows, self.bolt.dia_hole)

                            if self.plate.design_status is True and self.weld.design_status is True and self.plate.plate_moment < self.plate.plate_moment_capacity:
                                count += 1
                                gauge = round_up(self.weld.size * 2 +
                                    self.bolt_dist_to_weld * 2 + self.supported_section.web_thickness, 2)
                                plate_width = round_up(self.weld.size * 2 + self.bolt_dist_to_weld * 2 +
                                                       self.bolt.min_edge_dist_round * 2 + self.supported_section.web_thickness,
                                                       2)

                                # TRIAL FUNCTION #
                                # total_cost = self.plate.height*plate_width*self.plate.thickness_provided*plate_cost + \
                                #              bolt_rows*bolt_cost*self.bolt.bolt_diameter_provided*self.bolt.bolt_grade_provided/100
                                # trial function for cost optimisation
                                # todo: Finalize optimisation function
                                # print("plate cost:", self.plate.height*plate_width*self.plate.thickness_provided*plate_cost)
                                # print("bolt cost:", bolt_rows*bolt_cost*self.bolt.bolt_diameter_provided*self.bolt.bolt_grade_provided/100)

                                ##### O U T P U T   D I C T I O N A R Y   F O R M A T #####
                                row = [int(bolt_rows),                                                  # 0-Rows of Bolts
                                       int(self.bolt.bolt_diameter_provided),                           #1-Bolt Diameter
                                       self.bolt.bolt_grade_provided,                                   #2-Bolt Grade
                                       int(self.plate.thickness_provided),                              #3-Plate Thickness
                                       int(self.plate.height),                                          #4-Plate Height
                                       plate_width,                                                     #5-Plate Width
                                       round(self.bolt.bolt_capacity/1000, 2),                          #6-Bolt Shear Strength
                                       round(self.bolt.bolt_shear_capacity/1000, 2),                    #7-Bolt Shear Capacity
                                       bolt_bearing_capacity_disp,                                      #8-Bolt Bearing Capacity
                                       round(self.bolt.bolt_tension_capacity/1000, 2),                  #9-Bolt Tension Capacity
                                       round(self.bolt.bolt_shear/1000, 2),                             #10-Bolt Shear Force
                                       round(self.bolt.bolt_tension/1000, 2),                           #11-Bolt Tension Force
                                       self.bolts_required_IR_LT1,                                      #12-Total Number of Bolts
                                       pitch,                                                           #13-Pitch
                                       gauge,                                                           #14-Gauge
                                       end_dist,                                                        #15-End Distance
                                       self.bolt.min_edge_dist_round,                                   #16-Edge Distance
                                       round(self.bolt.bolt_tension_prying/1000, 2),                    #17-Bolt Prying Force
                                       round(self.plate.plate_shear, 2),                                #18-Plate Shear
                                       round(self.plate.plate_moment/1000000, 3),                       #19-Plate Moment
                                       round(self.plate.shear_capacity, 2),                             #20-Plate Shear Capacity
                                       round(self.plate.plate_block_shear_capacity/1000, 2),            #21-Plate Block Shear Capacity
                                       round(self.plate.plate_moment_capacity/1000000, 3),              #22-Plate Moment Capacity
                                       self.weld.size,                                                  #23-Weld Size
                                       round(self.weld.stress, 2),                                      #24-Weld Stress
                                       round(self.weld.strength, 2),                                    #25-Weld Strength
                                       weld_size_max,                                                   #26-Weld Size max
                                       weld_size_min,                                                   #27-Weld size min
                                       self.beta_lj,                                                    #28-Beta_lj
                                       self.beta_lg,                                                    #29-Beta_lg
                                       self.beta_pk,                                                    #30-Beta_pk
                                       self.comb_bolt_ir,                                               #31-Bolt_IR
                                       t_sum,                                                           #32-Sum of plate thickness
                                       'INSERT_HERE',                                                   #XX- EMPTY
                                       # total_cost,
                                       count]
                                self.output.append(row)
                                print("********* Trial {} ends here *************".format(count))
                            else:
                                row = [int(bolt_rows),  # 0-Rows of Bolts
                                       int(self.bolt.bolt_diameter_provided),  # 1-Bolt Diameter
                                       self.bolt.bolt_grade_provided,  # 2-Bolt Grade
                                       int(self.plate.thickness_provided),  # 3-Plate Thickness
                                       int(self.plate.height),  # 4-Plate Height
                                       plate_width,  # 5-Plate Width
                                       round(self.bolt.bolt_capacity / 1000, 2),
                                       # 6-Bolt Shear Strength
                                       round(self.bolt.bolt_shear_capacity / 1000, 2),
                                       # 7-Bolt Shear Capacity
                                       bolt_bearing_capacity_disp,  # 8-Bolt Bearing Capacity
                                       round(self.bolt.bolt_tension_capacity / 1000, 2),
                                       # 9-Bolt Tension Capacity
                                       round(self.bolt.bolt_shear / 1000, 2),  # 10-Bolt Shear Force
                                       round(self.bolt.bolt_tension / 1000, 2),  # 11-Bolt Tension Force
                                       self.bolts_required_IR_LT1,  # 12-Total Number of Bolts
                                       pitch,  # 13-Pitch
                                       gauge,  # 14-Gauge
                                       end_dist,  # 15-End Distance
                                       self.bolt.min_edge_dist_round,  # 16-Edge Distance
                                       round(self.bolt.bolt_tension_prying / 1000, 2),
                                       # 17-Bolt Prying Force
                                       round(self.plate.plate_shear, 2),  # 18-Plate Shear
                                       round(self.plate.plate_moment / 1000000, 3),  # 19-Plate Moment
                                       round(self.plate.shear_capacity, 2),  # 20-Plate Shear Capacity
                                       round(self.plate.plate_block_shear_capacity / 1000, 2),
                                       # 21-Plate Block Shear Capacity
                                       round(self.plate.plate_moment_capacity / 1000000, 3),
                                       # 22-Plate Moment Capacity
                                       self.weld.size,  # 23-Weld Size
                                       round(self.weld.stress, 2),  # 24-Weld Stress
                                       round(self.weld.strength, 2),  # 25-Weld Strength
                                       weld_size_max,  # 26-Weld Size max
                                       weld_size_min,  # 27-Weld size min
                                       self.beta_lj,  # 28-Beta_lj
                                       self.beta_lg,  # 29-Beta_lg
                                       self.beta_pk,  # 30-Beta_pk
                                       self.comb_bolt_ir,  #31-Bolt_IR
                                       t_sum,                                                           #32-Sum of plate thickness
                                       'INSERT_HERE',  # XX- EMPTY
                                       # total_cost,
                                       count]
                                self.failed_output_plate.append(row)
                        else:

                            row = [int(bolt_rows),  # 0-Rows of Bolts
                                   int(self.bolt.bolt_diameter_provided),  # 1-Bolt Diameter
                                   self.bolt.bolt_grade_provided,  # 2-Bolt Grade
                                   int(self.plate.thickness_provided),  # 3-Plate Thickness
                                   int(self.plate.height),  # 4-Plate Height
                                   0.0,  # 5-Plate Width
                                   round(self.bolt.bolt_capacity / 1000, 2),  # 6-Bolt Shear Strength
                                   round(self.bolt.bolt_shear_capacity / 1000, 2),
                                   # 7-Bolt Shear Capacity
                                   bolt_bearing_capacity_disp,  # 8-Bolt Bearing Capacity
                                   round(self.bolt.bolt_tension_capacity / 1000, 2),
                                   # 9-Bolt Tension Capacity
                                   round(self.bolt.bolt_shear / 1000, 2),  # 10-Bolt Shear Force
                                   round(self.bolt.bolt_tension / 1000, 2),  # 11-Bolt Tension Force
                                   self.bolts_required_IR_LT1,  # 12-Total Number of Bolts
                                   pitch,  # 13-Pitch
                                   0.0,  # 14-Gauge
                                   end_dist,  # 15-End Distance
                                   self.bolt.min_edge_dist_round,  # 16-Edge Distance
                                   round(self.bolt.bolt_tension_prying / 1000, 2),
                                   # 17-Bolt Prying Force
                                   round(self.plate.plate_shear, 2),  # 18-Plate Shear
                                   round(self.plate.plate_moment / 1000000, 3),  # 19-Plate Moment
                                   round(self.plate.shear_capacity, 2),  # 20-Plate Shear Capacity
                                   round(self.plate.plate_block_shear_capacity / 1000, 2),
                                   # 21-Plate Block Shear Capacity
                                   round(self.plate.plate_moment_capacity / 1000000, 3),
                                   # 22-Plate Moment Capacity
                                   self.weld.size,  # 23-Weld Size
                                   round(self.weld.stress, 2),  # 24-Weld Stress
                                   round(self.weld.strength, 2),  # 25-Weld Strength
                                   weld_size_max,  # 26-Weld Size max
                                   weld_size_min,  # 27-Weld size min
                                   self.beta_lj,  # 28-Beta_lj
                                   self.beta_lg,  # 29-Beta_lg
                                   self.beta_pk,  # 30-Beta_pk
                                   self.comb_bolt_ir,  # 31-Bolt_IR

                                   t_sum,  # 32-Sum of plate thickness
                                   'INSERT_HERE',  # XX- EMPTY
                                   # total_cost,
                                   count]
                            self.failed_output_bolt.append(row)

                    if bolts_one_line <= 1 and self.bolt.bolt_diameter_provided == min(self.bolt.bolt_diameter_possible) \
                            and self.bolt.bolt_grade_provided == min(self.bolt.bolt_grade) \
                            and self.plate.thickness_provided == sorted(self.plate.thickness)[-1]:
                        self.design_status = False
                        self.design_status_bolt = False
                        # logger.error(" : Select bolt of lower diameter, sufficient plate height/ width not available to arrange bolts")
                    if not self.bolt.bolt_diameter_possible:
                        self.design_status = False
                        self.design_status_bolt = False
        if not self.bolt.bolt_diameter_possible and len(self.output) == 0:
            self.design_status = False
            self.design_status_bolt = False
            logger.error(" : Checking plate thickness of {} mm and bolt diameter of {} mm".format(
                self.plate.thickness_provided, max(self.bolt.bolt_diameter_not_possible)))
            logger.error(" : Total thickness of connecting elements, including packing plate in gap, is more than "
                         "8 times bolt diameter, please select higher bolt diameter or lower plate thickness")
            logger.error(" : It fails in bolt grip length check as per Cl. 10.3.3.2 of IS 800:2007")
        if self.design_status_plate_tk is False:
            self.design_status = False
            logger.error(" : Select plate(s) of higher thickness")
        elif len(self.output) > 0:
            self.design_status = True
            self.design_status_bolt = True
            self.design_status_plate= True
            self.weld.design_status = True
            self.output.sort(key=lambda x: (x[3], x[0], x[1], x[2]))
            self.set_values_to_class(self)
            print("No of effective trials: ", count)
            print(self.output[0])
            if self.output[0][26] == self.output[0][27]:
                logger.info("The minimum weld size is greater than or equal to the thickness of the thinner connecting plate [Ref. Table 21, "
                            "IS800:2007].")
                logger.info("Thicker plate shall be adequately preheated to prevent cracking of the weld.")
            if self.output[0][23] in (3,4):
                logger.info(": The minimum recommended weld throat thickness suggested by IS 800:2007 is 3 mm, as per " +
                            "cl. 10.5.3.1. Weld throat thickness is not considered as per cl. 10.5.3.2. Please take " +
                            "necessary detailing precautions at site accordingly.")
            self.get_design_status(self)
        elif len(self.failed_output_plate) > 0:
            self.design_status = False
            self.design_status_bolt = True
            self.design_status_plate= False
            self.weld.design_status = False
            self.set_values_to_class(self)
            logger.error(" : Plate moment/shear capacity is insufficient. Choose higher thickness/grade.")
            logger.error(" : (Or) Required plate width is greater than available width.")
            logger.error(": (Or) Weld thickness is not sufficient [Ref. Cl. 10.5.7, IS 800:2007].")
            # logger.warning(": Minimum weld thickness required is %2.2f mm " % self.weld.t_weld_req)
            logger.info(": Increase the length of the weld/end plate.")
        elif len(self.failed_output_bolt) >0:
            self.design_status = False
            self.design_status_bolt = False
            self.design_status_plate = False
            self.weld.design_status = False
            self.set_values_to_class(self)
            logger.error(" : Select a bolt of higher capacity, sufficient plate width/height is not available to accommodate the defined bolts.")
        # elif count == 0:
        #     self.design_status = False
        #     # print(self.design_status)
        #     # return self.design_status
        #     self.set_values_to_class(self)
        #     if self.design_status_plate is False:
        #         logger.error(" : Select plate of higher thickness")
        # elif self.design_status_plate is False:
        #     self.design_status = False
        #     self.set_values_to_class(self)
        #     logger.error(" : Plate moment/shear capacity is insufficient. Choose higher thickness/grade")
        # elif self.plate.design_status is False:
        #     self.design_status = False
        #     self.set_values_to_class(self)
        #     logger.error(" : Required plate width is greater than available width")
        # elif self.weld.design_status is False:
        #     # TODO: Check logger message
        #     self.design_status = False
        #     self.set_values_to_class(self)
        #     logger.error(": Weld thickness is not sufficient [cl. 10.5.7, IS 800:2007]")
        #     #logger.warning(": Minimum weld thickness required is %2.2f mm " % self.weld.t_weld_req)
        #     logger.info(": Should increase length of weld/End plate")
        #     # logger.error(
        #     #   ": For given members and %2.2f mm thick plate, weld sizes should be of range %2.2f mm and  %2.2f mm "
        #     #   % self.plate.thickness_provided % weld_size_min % weld_size_max)#
        #     logger.info(": Cannot design weld with available welds ")
        # else:
        #     # self.get_design_status(self)
        #     self.output.sort(key=lambda x: (x[3], x[0], x[1], x[2]))
        #     self.set_values_to_class(self)
        #     print("No of effective trials: ", count)
        #     print(self.output[0])
        #     if self.output[0][26] == self.output[0][27]:
        #         logger.info("Minimum weld size given in Table 21 of IS800:2007 is greater than or equal to thickness "
        #                     "of thinner connecting plate")
        #         logger.info("Thicker plate shall be adequately preheated to prevent cracking of the weld")
        #     self.get_design_status(self)

    def set_values_to_class(self):
        if self.design_status is True:
            a = self.output
        elif self.design_status_bolt is False or self.design_status_plate_tk is False or self.design_status_plate is False:
            self.failed_output_bolt.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
            a = self.failed_output_bolt
        elif self.plate.design_status is False or self.weld.design_status is False:
            self.failed_output_plate.sort(key=lambda x: (x[3], x[0], x[1], x[2]))
            a = self.failed_output_plate
        self.plate.bolt_line = 2  # only one line of bolts provided on each side of web
        self.plate.bolts_one_line = a[0][0]
        self.plate.bolts_required = self.plate.bolt_line * self.plate.bolts_one_line
        self.bolt.bolt_diameter_provided = a[0][1]
        self.bolt.bolt_grade_provided = a[0][2]

        self.plate.thickness_provided = a[0][3]
        self.plate.height = a[0][4]
        self.plate.width = a[0][5]

        self.bolt.bolt_capacity = a[0][6]
        self.bolt.bolt_shear_capacity = a[0][7]
        self.bolt.bolt_bearing_capacity_disp = a[0][8]
        self.bolt.bolt_tension_capacity = a[0][9]
        self.bolt.bolt_shear = a[0][10]
        self.bolt.bolt_tension = a[0][11]
        self.bolt.bolt_tension_prying = a[0][17]

        self.beta_lj = round(a[0][28], 3)
        self.beta_lg = round(a[0][29], 3)
        self.beta_pk = round(a[0][30], 3)
        self.comb_bolt_ir = round(a[0][31], 3)
        self.bolt_capacity = round(self.bolt.bolt_capacity*self.beta_lj*self.beta_lg*self.beta_pk, 2)
        self.bolt_tension = round(self.bolt.bolt_tension + self.bolt.bolt_tension_prying, 3)
        self.t_sum = a[0][32]

        self.plate.pitch_provided = a[0][13]
        self.plate.gauge_provided = a[0][14]
        self.plate.end_dist_provided = a[0][15]
        self.plate.edge_dist_provided = a[0][16]

        self.plate.plate_shear = a[0][18]
        self.plate.plate_moment = a[0][19]
        self.plate.shear_capacity = a[0][20]
        self.plate.plate_block_shear_capacity = a[0][21]
        self.plate.plate_moment_capacity = a[0][22]

        self.weld.length = a[0][4]
        self.weld.size = a[0][23]
        self.weld.stress = a[0][24]
        self.weld.strength = a[0][25]
        self.weld.weld_size_max = a[0][26]
        self.weld.weld_size_min = a[0][27]
        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
        if self.connectivity == VALUES_CONN_1[0]:
            self.bolt_conn_plates_t_fu_fy.append(
                (self.supporting_section.flange_thickness, self.supporting_section.fu, self.supporting_section.fy))
        else:
            self.bolt_conn_plates_t_fu_fy.append(
                (self.supporting_section.web_thickness, self.supporting_section.fu, self.supporting_section.fy))
        # print("bear cap",self.bolt.bolt_bearing_capacity)
        self.bolt.calculate_bolt_capacity(self.bolt.bolt_diameter_provided, self.bolt.bolt_grade_provided,
                                          self.bolt_conn_plates_t_fu_fy, 1, e=self.plate.end_dist_provided,p=self.plate.pitch_provided)
        # print("bear cap 2", self.bolt.bolt_bearing_capacity)
        self.bolt.calculate_bolt_spacing_limits(self.bolt.bolt_diameter_provided,self.bolt_conn_plates_t_fu_fy,1)
        col_g = (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius + self.plate.edge_dist_provided)
        beam_g = (self.supported_section.web_thickness / 2 + self.weld.size + self.plate.edge_dist_provided)
        if col_g > beam_g:
            l_v = col_g - (self.supported_section.web_thickness / 2 + self.weld.size)
        else:
            l_v = self.bolt.min_edge_dist_round
        b_e = min(self.plate.pitch_provided, 2 * l_v)
        no_bolt = self.plate.bolt_line * self.plate.bolts_one_line
        self.plate.connect_to_database_to_get_fy_fu(self.plate.material, self.plate.thickness_provided)
        self.bolt.bolt_shear = self.load.shear_force * 1000 / no_bolt  # N
        print("bolt_shear", self.bolt.bolt_shear)
        self.bolt.bolt_tension = self.load.axial_force * 1000 / no_bolt  # N
        print("bolt_tension", self.bolt.bolt_tension)
        if self.bolt.bolt_type == TYP_FRICTION_GRIP:
            self.bolt.bolt_tensioning = 'Pretensioned'
        # TODO: check available effective width per pair of bolts (b_e)
        self.bolt.bolt_tension_prying = IS800_2007.cl_10_4_7_bolt_prying_force(self.bolt.bolt_tension, l_v,
                                                                               0.7 * self.bolt.bolt_fu, b_e,
                                                                               self.plate.thickness_provided,
                                                                               self.plate.fy,
                                                                               self.bolt.min_end_dist_round,
                                                                               self.bolt.bolt_tensioning)
        print("bolt_tension_prying", self.bolt.bolt_tension_prying)
        self.comb_bolt_ir = (self.bolt.bolt_shear / (self.bolt.bolt_capacity)) ** 2 + \
                            ((self.bolt.bolt_tension + self.bolt.bolt_tension_prying) / self.bolt.bolt_tension_capacity) ** 2
        print(self.comb_bolt_ir)
        self.plate.Z_p = self.plate.height * self.plate.thickness_provided ** 2 / 4
        self.plate.Z_e = self.plate.height * self.plate.thickness_provided ** 2 / 6
        # [self.bolt.bolt_shear, self.bolt.bolt_tension, self.bolt.bolt_tension_prying,
        #  self.bolts_required_IR_LT1] = self.get_bolt_IR(self, self.bolt.bolt_capacity,
        #                                                 self.bolt.bolt_tension_capacity, bolts_required_initial, b_e,
        #                                                 l_v,
        #                                                 self.bolt.min_pitch_round, 1.0, 1.0, 1.0)




    def get_bolt_bearing_updated(self, end_dist, pitch, bolts_one_line, weld_size):
        t_fu_prev = self.bolt_conn_plates_t_fu_fy[0][0] * self.bolt_conn_plates_t_fu_fy[0][1]
        thk_considered = self.bolt_conn_plates_t_fu_fy[0][0]
        fu_considered = self.bolt_conn_plates_t_fu_fy[0][1]
        for i in self.bolt_conn_plates_t_fu_fy:
            t_fu = i[0] * i[1]
            if t_fu <= t_fu_prev:
                thk_considered = i[0]
                fu_considered = i[1]
        self.bolt.bolt_bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
            f_u=fu_considered, f_ub=self.bolt.bolt_fu, t=thk_considered,
            d=self.bolt.bolt_diameter_provided, e=end_dist, p=pitch,
            bolt_hole_type=self.bolt.bolt_hole_type)
        self.bolt.bolt_capacity = min(self.bolt.bolt_bearing_capacity, self.bolt.bolt_shear_capacity)
        bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
        if self.bolt.bolt_type == TYP_BEARING:
            l_j = pitch * (bolts_one_line - 1)
            t_sum = self.plate.gap
            for i in self.bolt_conn_plates_t_fu_fy:
                t_sum = t_sum + i[0]
            self.beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided, l_j)
            self.beta_lg = IS800_2007.cl_10_3_3_2_bolt_large_grip(self.bolt.bolt_diameter_provided, t_sum, l_j)
            self.beta_pk = IS800_2007.cl_10_3_3_3_packing_plates(self.plate.gap)
        else:
            self.beta_lj = 1.0
            self.beta_lg = 1.0
            self.beta_pk = 1.0
        print("beta_lj", self.beta_lj)
        col_g = (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius + self.bolt.min_end_dist_round)
        beam_g = (self.supported_section.web_thickness / 2 + weld_size + self.bolt.min_end_dist_round)
        if col_g > beam_g:
            l_v = col_g - (self.supported_section.web_thickness / 2 + weld_size)
        else:
            l_v = self.bolt.min_edge_dist_round
        b_e = min(pitch, 2 * l_v)

        [self.bolt.bolt_shear, self.bolt.bolt_tension, self.bolt.bolt_tension_prying, bolts_n] = \
            self.get_bolt_IR(self, self.bolt.bolt_capacity, self.bolt.bolt_tension_capacity,
                             bolts_one_line * 2, b_e, l_v, pitch, self.beta_lj, self.beta_lg, self.beta_pk)
        return bolt_bearing_capacity_disp

    def plate_check(self, bolt_rows, pitch, end_dist, design_status_plate):
        [available_welds, weld_size_min, weld_size_max] = self.get_available_welds(self, self.connecting_plates_tk)
        while self.plate.height <= self.max_plate_height:
            design_status_plate = False
            self.max_bolts_one_line = int(
                ((self.plate.height - (2 * self.bolt.min_end_dist_round)) /
                 self.bolt.min_gauge_round) + 1)
            print("max_bolts_one_line: ", self.max_bolts_one_line)
            print(bolt_rows, "bolt_rows init")
            while bolt_rows <= self.max_bolts_one_line:

                [pitch, end_dist, self.plate.height, bolt_rows] = \
                    self.get_pitch_end_dist(self, self.plate.height, bolt_rows,
                                            self.bolt.min_end_dist_round,
                                            self.bolt.max_spacing_round,
                                            self.bolt.max_edge_dist_round,
                                            weld_size_min)
                print(bolt_rows, "bolt_rows")
                [self.plate.plate_moment_capacity, self.plate.shear_capacity,
                 self.plate.plate_block_shear_capacity] = \
                    self.get_plate_capacity(self, self.plate.thickness_provided, self.plate.height, pitch,
                                            self.bolt_dist_to_weld, end_dist,
                                            bolt_rows, self.bolt.dia_hole)
                self.plate.plate_moment = self.bolt_dist_to_weld * self.bolt.bolt_tension
                # self.plate.plate_shear = self.load.shear_force * 1000
                if self.plate.plate_moment > self.plate.plate_moment_capacity or \
                        self.plate.plate_shear > self.plate.shear_capacity:
                    design_status_plate = False
                    if (self.max_plate_height - self.plate.height) >= self.bolt.min_pitch_round:
                        bolt_rows += 1
                    else:
                        break
                else:
                    design_status_plate = True
                    break
            print("design_status_plate: ", design_status_plate)
            if design_status_plate is False:
                self.plate.height += self.bolt.min_pitch_round
            else:
                break
        return bolt_rows, pitch, end_dist, design_status_plate

    def get_pitch_end_dist(self, plate_h, bolts_one_line, edge_dist, max_spacing, max_edge_dist, weld_size):
        """
        :param web_plate_l: height of plate
        :param min_end_dist_round: minimum end distance
        :param bolts_one_line: bolts in one line
        :param max_spacing_round: maximum pitch
        :param max_end_dist_round: maximum end distance
        :return: pitch, end distance, height of plate (false if applicable)
        """
        pitch = 0
        while True:
            if bolts_one_line > 1:
                pitch = round_up((plate_h - (2 * edge_dist)) / (bolts_one_line - 1), multiplier=5)

            plate_h = pitch * (bolts_one_line - 1) + edge_dist * 2
            print(plate_h, "plate_h web")
            if self.bolt.bolt_type == TYP_BEARING:
                l_j = pitch * (bolts_one_line - 1)
                t_sum = self.plate.gap
                for i in self.bolt_conn_plates_t_fu_fy:
                    t_sum = t_sum + i[0]
                self.beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided, l_j)
                self.beta_lg = IS800_2007.cl_10_3_3_2_bolt_large_grip(self.bolt.bolt_diameter_provided, t_sum, l_j)
                self.beta_pk = IS800_2007.cl_10_3_3_3_packing_plates(self.plate.gap)
            else:
                self.beta_lj = 1.0
                self.beta_lg = 1.0
                self.beta_pk = 1.0
            # print("beta_lj", self.beta_lj, self.beta_lg, self.beta_pk)
            if self.bolt.bolt_type == TYP_BEARING:
                bolt_bearing_capacity_disp = self.get_bolt_bearing_updated(self, edge_dist, pitch, bolts_one_line, weld_size)

            col_g = (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius + self.bolt.min_end_dist_round)
            beam_g = (self.supported_section.web_thickness / 2 + weld_size + self.bolt.min_end_dist_round)
            if col_g > beam_g:
                l_v = col_g - (self.supported_section.web_thickness / 2 + weld_size)
            else:
                l_v = self.bolt.min_edge_dist_round
            b_e = min(pitch, 2 * l_v)
            [self.bolt.bolt_shear, self.bolt.bolt_tension, self.bolt.bolt_tension_prying, bolts_n]=\
                self.get_bolt_IR(self, self.bolt.bolt_capacity, self.bolt.bolt_tension_capacity,
                             bolts_one_line * 2, b_e, l_v, pitch, self.beta_lj, self.beta_lg, self.beta_pk)

            if (self.max_plate_height - plate_h) >= self.bolt.min_pitch_round:
                if bolts_n/2 > bolts_one_line:
                    bolts_one_line = bolts_n/2
                    continue
                elif pitch > max_spacing:
                    pitch, edge_dist = self.plate.get_spacing_adjusted(pitch, edge_dist, max_spacing)
                    if edge_dist >= max_edge_dist:
                        edge_dist = max_edge_dist
                        bolts_one_line += 1
                else:
                    break
            else:
                break

        print("web", pitch, edge_dist, plate_h)
        return pitch, edge_dist, plate_h, bolts_one_line

    def get_bolt_IR(self, bolt_shear_capacity, bolt_tension_capacity, no_bolt, b_e, l_v, pitch, beta_lj=1.0,
                    beta_lg=1.0, beta_pk=1.0):
        while True:
            self.bolt.bolt_shear = self.load.shear_force * 1000 / no_bolt  # N
            print("bolt_shear", self.bolt.bolt_shear)
            self.bolt.bolt_tension = self.load.axial_force * 1000 / no_bolt  # N
            print("bolt_tension", self.bolt.bolt_tension)
            if self.bolt.bolt_type == TYP_FRICTION_GRIP:
                self.bolt.bolt_tensioning = 'Pretensioned'
            # TODO: check available effective width per pair of bolts (b_e)
            self.bolt.bolt_tension_prying = IS800_2007.cl_10_4_7_bolt_prying_force(self.bolt.bolt_tension, l_v,
                                        0.7*self.bolt.bolt_fu, b_e, self.plate.thickness_provided,
                                        self.plate.fy, self.bolt.min_end_dist_round, self.bolt.bolt_tensioning)
            print("bolt_tension_prying", self.bolt.bolt_tension_prying)
            self.comb_bolt_ir = (self.bolt.bolt_shear / (bolt_shear_capacity*beta_lj*beta_lg*beta_pk)) ** 2 + \
                           ((self.bolt.bolt_tension + self.bolt.bolt_tension_prying)/bolt_tension_capacity) ** 2
            print(self.comb_bolt_ir)
            if self.comb_bolt_ir > 1:
                no_bolt += 2
                if self.bolt.bolt_type == TYP_BEARING:
                    l_j = (no_bolt/2 - 1) * pitch
                    t_sum = self.plate.gap
                    for i in self.bolt_conn_plates_t_fu_fy:
                        t_sum = t_sum + i[0]
                    self.beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided, l_j)
                    self.beta_lg = IS800_2007.cl_10_3_3_2_bolt_large_grip(self.bolt.bolt_diameter_provided, t_sum, l_j)
                    self.beta_pk = IS800_2007.cl_10_3_3_3_packing_plates(self.plate.gap)
                else:
                    self.beta_lj = 1.0
                    self.beta_lg = 1.0
                    self.beta_pk = 1.0
                beta_lj = self.beta_lj
                beta_lg = self.beta_lg
                beta_pk = self.beta_pk
            else:
                break
        return self.bolt.bolt_shear, self.bolt.bolt_tension, self.bolt.bolt_tension_prying, no_bolt

    def get_plate_capacity(self, p_th, p_h, pitch, bolt_dist, end, n_row, bolt_hole_dia):
        # plate_moment = min_edge_dist * bolt_tension
        self.plate.Z_p = (min(pitch, 2 * bolt_dist)) * p_th **2 /4
        self.plate.Z_e = (min(pitch, 2 * bolt_dist)) * p_th **2 /6
        plate_moment_capacity = IS800_2007.cl_8_2_1_2_design_moment_strength(self.plate.Z_e, self.plate.Z_p, self.plate.fy, 'plastic')
        A_v = p_h* p_th
        plate_shear_yielding_capacity = IS800_2007.cl_8_4_design_shear_strength(A_v, self.plate.fy)

        A_vg = ((n_row-1) * pitch + end) * p_th
        A_vn = ((n_row-1) * pitch + end - (float(n_row)-0.5) * bolt_hole_dia) * p_th
        A_tg = 2 * self.bolt.min_edge_dist_round * p_th
        A_tn = 2 * (self.bolt.min_edge_dist_round - 0.5 * bolt_hole_dia) * p_th

        plate_block_shear_capacity = IS800_2007.cl_6_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, self.plate.fu, self.plate.fy)
        plate_shear_capacity = round((min(plate_shear_yielding_capacity, plate_block_shear_capacity) )/ 1000, 2)

        return plate_moment_capacity, plate_shear_capacity, plate_block_shear_capacity

    def get_available_welds(self, connecting_members=[]):
        weld_size_max = math.ceil(min(connecting_members))
        weld_size_min = math.ceil(IS800_2007.cl_10_5_2_3_min_weld_size(connecting_members[0], connecting_members[1]))
        if 7<= weld_size_max < max(ALL_WELD_SIZES) and weld_size_max%2 != 0:
            weld_size_max = round_up(weld_size_max,2)
        available_welds = list([x for x in ALL_WELD_SIZES if (weld_size_min <= x <= weld_size_max)])
        # if available_welds == [] and weld_size_min < max(ALL_WELD_SIZES):
        #     available_welds = [weld_size_min]
        return available_welds,weld_size_min,weld_size_max

    def design_weld(self,available_welds):
        self.weld.design_status = False
        self.weld.size = available_welds[0]
        while self.plate.height <= self.max_plate_height:
            self.weld.length = self.plate.height
            self.weld.throat_tk = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
                fillet_size=self.weld.size, fusion_face_angle=90)
            self.weld.eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
                fillet_size=self.weld.size, available_length=self.weld.length)
            self.weld.get_weld_strength(connecting_fu=[self.plate.fu, self.supported_section.fu,self.weld.fu],
                                                weld_fabrication=self.weld.fabrication,
                                                t_weld=self.weld.size, weld_angle=90)
            self.beta_lw = IS800_2007.cl_10_5_7_3_weld_long_joint(self.weld.eff_length, self.weld.throat_tk)
            self.weld.strength = self.weld.strength * self.beta_lw
            force_h = self.load.shear_force * 1000
            force_l = self.load.axial_force * 1000
            # force_t = self.plate.moment_demand
            self.weld.get_weld_stress(force_h, force_l, l_weld=2*self.weld.eff_length, weld_twist= 0.0, Ip_weld=0.0, y_max=0.0,
                                                        x_max=0.0)
            if self.weld.strength > self.weld.stress:
                break
            else:
                t_weld_req = self.weld.size * self.weld.stress / self.weld.strength
                print(t_weld_req)
                available_welds_updated = list([x for x in available_welds if (t_weld_req <= x)])
                print(available_welds_updated)
                if not available_welds_updated:
                    self.plate.height += 10
                    self.weld.size = available_welds[0]
                    logger.warning('Weld stress is guiding plate height, trying with a length of %2.2f mm' % self.plate.height)
                else:
                    self.weld.size = available_welds_updated[0]
        print(self.weld.size, self.weld.length)
        if self.weld.strength < self.weld.stress:
            self.weld.t_weld_req = self.weld.size * self.weld.stress / self.weld.strength
            self.weld.design_status = False
            # logger.error(": Weld thickness is not sufficient [cl. 10.5.7, IS 800:2007]")
            # logger.warning(": Minimum weld thickness required is %2.2f mm " % t_weld_req)
            # logger.info(": Should increase length of weld/End plate")
        else:
            self.weld.design_status = True

    def get_design_status(self):
        if self.weld.design_status is True:
            self.design_status = True
            logger.info("End plate is designed with minimum possible plate thickness.")
            logger.info("Bolt columns are limited to two (one on each side) in shear end plate.")
            logger.info("=== End Of Design ===")

    def plate_width_check(self, plate_width):
        if self.connectivity == VALUES_CONN_1[0]:
            clear_width = self.supporting_section.flange_width
            if clear_width <= plate_width:
                self.plate.design_status = False
            else:
                self.plate.design_status = True
        elif self.connectivity == VALUES_CONN_1[1]:
            clear_depth = self.supporting_section.depth - 2 * self.supporting_section.flange_thickness - \
                          2 * self.supporting_section.root_radius
            if clear_depth <= plate_width:
                self.plate.design_status = False
            else:
                self.plate.design_status = True
        else:
            self.plate.design_status = True

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('End Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'End Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Plate", bgcolor)

    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair
        print(flag)

        out_list = []

        # TODO: 'Bolt Properties: Start'

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.output[0][1] if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_PC_PROVIDED, TYPE_TEXTBOX, self.output[0][2] if flag else '', True)
        out_list.append(t3)

        t3_1 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX, self.output[0][0] if flag else '', True)
        out_list.append(t3_1)

        # t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  self.output[0][7] if flag else '', True)
        # out_list.append(t4)
        #
        # t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, self.output[0][8] if flag else '', True)
        # out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.bolt_capacity if flag else '', True)
        out_list.append(t6)

        t6_1 = (KEY_OUT_BOLT_TENSION_CAPACITY, KEY_OUT_DISP_BOLT_TENSION_CAPACITY, TYPE_TEXTBOX, self.output[0][9] if flag else '', True)
        out_list.append(t6_1)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_FORCE, TYPE_TEXTBOX, self.output[0][10] if flag else '', True)
        out_list.append(t21)

        t21_1 = (KEY_OUT_BOLT_TENSION_FORCE, KEY_OUT_DISP_BOLT_TENSION_FORCE, TYPE_TEXTBOX, self.bolt_tension if flag else '', True)
        out_list.append(t21_1)

        # t21_2 = (KEY_OUT_BOLT_PRYING_FORCE, KEY_OUT_DISP_BOLT_PRYING_FORCE, TYPE_TEXTBOX, self.output[0][17] if flag else '', True)
        # out_list.append(t21_2)

        t3_2 = (KEY_OUT_BOLT_IR_DETAILS, KEY_OUT_DISP_BOLT_IR_DETAILS, TYPE_OUT_BUTTON, ['Details', self.bolt_capacity_details], True)
        out_list.append(t3_2)

        t23 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t23)

        # TODO: 'Bolt Properties: End'

        # TODO: Plate properties: Start

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True)
        out_list.append(t13)

        t14 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.output[0][3] if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.output[0][4] if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_WIDTH, TYPE_TEXTBOX, self.output[0][5] if flag else '', True)
        out_list.append(t16)

        t22 = (KEY_OUT_PLATE_CAPACITIES, KEY_OUT_DISP_PLATE_CAPACITIES, TYPE_OUT_BUTTON, ['Capacity Details', self.capacities], True)
        out_list.append(t22)

        # TODO: Plate Properties: End

        # TODO: Weld properties: Start

        t24 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t24)

        t25 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX, self.output[0][23] if flag else '', True)
        out_list.append(t25)

        t26 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX, self.output[0][25] if flag else '', True)
        out_list.append(t26)

        t27 = (KEY_OUT_WELD_STRESS, KEY_OUT_DISP_WELD_STRESS, TYPE_TEXTBOX, self.output[0][24] if flag else '', True)
        out_list.append(t27)

        # TODO: Weld Properties: End
        return out_list

    def bolt_capacity_details(self, flag):

        bolt_details = []

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX, self.output[0][7] if flag else '', True)
        bolt_details.append(t4)

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, self.output[0][8] if flag else '', True)
        bolt_details.append(t5)

        t5_1 = (KEY_OUT_BETA_LJ, KEY_OUT_DISP_BETA_LJ, TYPE_TEXTBOX, self.beta_lj if flag and self.bolt.bolt_type == TYP_BEARING else 'N/A', True)
        bolt_details.append(t5_1)

        t5_2 = (KEY_OUT_BETA_LG, KEY_OUT_DISP_BETA_LG, TYPE_TEXTBOX, self.beta_lg if flag and self.bolt.bolt_type == TYP_BEARING else 'N/A', True)
        bolt_details.append(t5_2)

        t5_3 = (KEY_OUT_BETA_PK, KEY_OUT_DISP_BETA_PK, TYPE_TEXTBOX, self.beta_pk if flag and self.bolt.bolt_type == TYP_BEARING else 'N/A', True)
        bolt_details.append(t5_3)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.bolt_capacity if flag else '', True)
        bolt_details.append(t6)

        t6_1 = (KEY_OUT_BOLT_TENSION_CAPACITY, KEY_OUT_DISP_BOLT_TENSION_CAPACITY, TYPE_TEXTBOX, self.output[0][9] if flag else '', True)
        bolt_details.append(t6_1)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_FORCE, TYPE_TEXTBOX, self.output[0][10] if flag else '', True)
        bolt_details.append(t21)

        t21_1 = (KEY_OUT_BOLT_TENSION_FORCE, KEY_OUT_DISP_BOLT_TENSION_FORCE, TYPE_TEXTBOX, self.output[0][11] if flag else '', True)
        bolt_details.append(t21_1)

        t21_2 = (KEY_OUT_BOLT_PRYING_FORCE, KEY_OUT_DISP_BOLT_PRYING_FORCE, TYPE_TEXTBOX, self.output[0][17] if flag else '', True)
        bolt_details.append(t21_2)

        t21_3 = (KEY_OUT_BOLT_TENSION_TOTAL, KEY_OUT_DISP_BOLT_TENSION_TOTAL, TYPE_TEXTBOX, self.bolt_tension if flag else '', True)
        bolt_details.append(t21_3)

        t21_4 = (KEY_OUT_BOLT_IR, KEY_OUT_DISP_BOLT_IR, TYPE_TEXTBOX, round(self.comb_bolt_ir/1000000,2) if flag else '', True)
        bolt_details.append(t21_4)

        return bolt_details

    def spacing(self, flag):

        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
               ['./ResourceFiles/images/ep_shear.png', 400, 277, ""])  # [image, width, height, caption]
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.output[0][13] if flag else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.output[0][15] if flag else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.output[0][14] if flag else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.output[0][16] if flag else '')
        spacing.append(t12)

        return spacing

    def capacities(self, flag):

        capacities = []

        t17 = (KEY_OUT_PLATE_SHEAR, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX, self.output[0][20] if flag else '')
        capacities.append(t17)

        t18 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_OUT_DISP_PLATE_BLK_SHEAR, TYPE_TEXTBOX, self.output[0][21] if flag else '')
        capacities.append(t18)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND_SEP, TYPE_TEXTBOX, self.output[0][19] if flag else '')
        capacities.append(t19)

        t20 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY_SEP, TYPE_TEXTBOX, self.output[0][22] if flag else '')
        capacities.append(t20)

        return capacities

    ######################################
    # Function to create design report (LateX/PDF)
    ######################################
    def save_design(self, popup_summary):
        super(EndPlateConnection, self).save_design(self)
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

        self.report_check = []
        #######################
        # Section Capacities
        #######################

        t1 = ('SubSection', 'Section Design Check', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        a = self.supported_section
        h = a.web_height
        t = a.web_thickness

        t1 = (KEY_DISP_SHEAR_CAPACITY, self.load.shear_force,
              cl_8_4_shear_yielding_capacity_member(h, t, a.fy, gamma_m0, a.shear_yielding_capacity),
              get_pass_fail(self.load.shear_force, round(a.shear_yielding_capacity/1000,2), relation="lesser"))
        self.report_check.append(t1)

        t1 = (KEY_DISP_TENSION_CAPACITY, self.load.axial_force,
              cl_6_2_tension_yield_capacity_member(h, t, a.fy, gamma_m0, round(a.tension_yielding_capacity, 2)),
              get_pass_fail(self.load.axial_force, round(a.tension_yielding_capacity/1000, 2), relation="lesser"))
        self.report_check.append(t1)

        if self.design_status_plate_tk is False:
            t1 = ('SubSection', 'Minimum Plate Thickness Check', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t1 = (DISP_MIN_PLATE_THICK, min_plate_thk_req(self.supported_section.web_thickness),
                  self.plate.thickness_provided,
                  get_pass_fail(self.supported_section.web_thickness, self.plate.thickness_provided,
                                relation="lesser"))
            self.report_check.append(t1)

        if self.supported_section.design_status is True and self.design_status_plate_tk is True:
            t1 = ('SubSection', 'Bolt Design', '|p{3cm}|p{6cm}|p{6.6cm}|p{1.2cm}|')
            self.report_check.append(t1)
            t1 = (KEY_DISP_D, '', self.bolt.bolt_diameter_provided, '')
            self.report_check.append(t1)
            t1 = (KEY_DISP_GRD, '', self.bolt.bolt_grade_provided, '')
            self.report_check.append(t1)
            t1 = (KEY_DISP_PLTHICK, '', self.plate.thickness_provided,'')
            self.report_check.append(t1)
            t6 = (DISP_NUM_OF_COLUMNS, 2, self.plate.bolt_line, get_pass_fail(2, self.plate.bolt_line, relation='leq'))
            self.report_check.append(t6)
            t7 = (DISP_NUM_OF_ROWS, '', self.plate.bolts_one_line, get_pass_fail(2, self.plate.bolts_one_line, relation='leq'))
            self.report_check.append(t7)
            t1 = (DISP_MIN_PITCH, cl_10_2_2_min_spacing(self.bolt.bolt_diameter_provided),
                  self.plate.pitch_provided,
                  get_pass_fail(self.bolt.min_pitch, self.plate.pitch_provided, relation='leq'))
            self.report_check.append(t1)
            t1 = (DISP_MAX_PITCH, cl_10_2_3_1_max_spacing(self.connecting_plates_tk), self.plate.pitch_provided,
                  get_pass_fail(self.bolt.max_spacing, self.plate.pitch_provided, relation='geq'))
            self.report_check.append(t1)

            t3 = (DISP_MIN_END, cl_10_2_4_2_min_edge_end_dist(self.bolt.d_0, self.bolt.edge_type), self.plate.edge_dist_provided,
                  get_pass_fail(self.bolt.min_end_dist, self.plate.end_dist_provided, relation='leq'))
            self.report_check.append(t3)
            t4 = (DISP_MAX_END, cl_10_2_4_3_max_edge_end_dist(self.bolt_conn_plates_t_fu_fy, self.bolt.corrosive_influences),
                  self.plate.edge_dist_provided,
                  get_pass_fail(self.bolt.max_end_dist, self.plate.end_dist_provided, relation='geq'))
            self.report_check.append(t4)
            t3 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(self.bolt.d_0, self.bolt.edge_type,parameter='edge_dist'),
                  self.plate.end_dist_provided,
                  get_pass_fail(self.bolt.min_edge_dist, self.plate.edge_dist_provided, relation='leq'))
            self.report_check.append(t3)
            t4 = (DISP_MAX_EDGE, cl_10_2_4_3_max_edge_end_dist(self.bolt_conn_plates_t_fu_fy,
                                                               self.bolt.corrosive_influences,parameter='edge_dist'),
                  self.plate.end_dist_provided,
                  get_pass_fail(self.bolt.max_edge_dist, self.plate.edge_dist_provided, relation="geq"))
            self.report_check.append(t4)

            g1 = 2 * (self.bolt.min_end_dist + self.weld.size) + self.supported_section.web_thickness
            if self.connectivity == VALUES_CONN_1[0]:
                g2 = round(2 * (self.bolt.min_end_dist + self.supporting_section.root_radius)
                           + self.supporting_section.web_thickness,2)
                g_min = max(g1, g2)
            else:
                g_min=g1

            t1 = (DISP_MIN_GAUGE, end_plate_gauge(self.connectivity,self.bolt.min_end_dist, self.weld.size,
                                                  self.supported_section.web_thickness,
                                                  self.supporting_section.web_thickness,
                                                  self.supporting_section.root_radius),
                  self.plate.gauge_provided,
                  get_pass_fail(g_min, self.plate.gauge_provided, relation='leq'))
            self.report_check.append(t1)
            V_b = round(self.bolt.bolt_shear/1000, 2)
            bolt_shear_capacity_disp = round(self.bolt.bolt_shear_capacity / 1000, 2)
            bolt_capacity_disp = round(self.bolt.bolt_capacity / 1000, 2)
            if self.bolt.bolt_type == TYP_BEARING:
                t1 = (KEY_OUT_DISP_BOLT_SHEAR, '', cl_10_3_3_bolt_shear_capacity(self.bolt.bolt_fu, 1, self.bolt.bolt_net_area,
                                                                                 self.bolt.gamma_mb, bolt_shear_capacity_disp), '')
                self.report_check.append(t1)
                t8 = (KEY_DISP_KB, " ",
                      cl_10_3_4_calculate_kb(self.plate.end_dist_provided, self.plate.pitch_provided, self.bolt.dia_hole,
                                             self.bolt.bolt_fu, self.bolt.fu_considered), '')
                self.report_check.append(t8)
                # kb = self.bolt.calculate_kb(self.plate.end_dist_provided, self.plate.pitch_provided, self.bolt.dia_hole,
                #               self.bolt.bolt_fu, self.bolt.fu_considered)
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
                t2 = (
                    KEY_OUT_DISP_BOLT_BEARING, '', cl_10_3_4_bolt_bearing_capacity(self.bolt.kb, self.bolt.bolt_diameter_provided,
                                                                                   self.bolt_conn_plates_t_fu_fy, self.bolt.gamma_mb,
                                                                                   bolt_bearing_capacity_disp), '')
                self.report_check.append(t2)

                t3 = (KEY_OUT_DISP_BOLT_CAPACITY, force_in_bolt_due_to_load(P=round(self.load.shear_force, 2),
                                                                               n=self.plate.bolts_required,
                                                                            T_ba=V_b,load='shear'),
                      cl_10_3_2_bolt_capacity(bolt_shear_capacity_disp, bolt_bearing_capacity_disp, self.bolt.bolt_capacity),
                      '')
                self.report_check.append(t3)
            else:
                kh_disp = round(self.bolt.kh, 2)
                t4 = (KEY_OUT_DISP_BOLT_SLIP_DR, '',
                      cl_10_4_3_HSFG_bolt_capacity(mu_f=self.bolt.mu_f, n_e=1, K_h=kh_disp, fub=self.bolt.bolt_fu,
                                                   Anb=self.bolt.bolt_net_area, gamma_mf=self.bolt.gamma_mf,
                                                   capacity=self.bolt.bolt_capacity), '')
                self.report_check.append(t4)

                t3 = (KEY_OUT_DISP_BOLT_CAPACITY, force_in_bolt_due_to_load(P=round(self.load.shear_force, 2),
                                                                            n=self.plate.bolts_required, T_ba=V_b,
                                                                            load='shear'),self.bolt.bolt_capacity,
                      '')
                self.report_check.append(t3)
            if self.bolt.bolt_type == TYP_BEARING:
                l_j = self.plate.pitch_provided * (self.plate.bolts_one_line - 1)
                beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided, l_j)
                beta_lg = IS800_2007.cl_10_3_3_2_bolt_large_grip(self.bolt.bolt_diameter_provided, self.t_sum, l_j)
                beta_pk = IS800_2007.cl_10_3_3_3_packing_plates(self.plate.gap)
            else:
                beta_lj = 1.0
                beta_lg = 1.0
                beta_pk = 1.0
            bolt_capacity_red = round(self.bolt.bolt_capacity * beta_lj*beta_lg*beta_pk/1000, 2)

            t10 = (KEY_OUT_LONG_JOINT, '',
                   cl_10_3_3_1_long_joint_bolted_prov(self.plate.bolt_line, self.plate.bolts_one_line,
                                                      self.plate.gauge_provided, self.plate.pitch_provided,
                                                      self.bolt.bolt_diameter_provided, self.bolt.bolt_capacity, bolt_capacity_red, direction='n_r'),
                   "")
            self.report_check.append(t10)

            t11 = (KEY_OUT_LARGE_GRIP, '',
                   cl_10_3_3_2_large_grip_bolted_prov(self.t_sum, self.bolt.bolt_diameter_provided, beta_lj),
                   "")
            self.report_check.append(t11)

            t12 = (KEY_OUT_PACKING_PLATE, '',
                   packing_plate_bolted_prov(self.plate.gap),
                   "")
            self.report_check.append(t12)

            t13 = (KEY_OUT_BOLT_CAPACITY_REDUCED, str(V_b),
                   bolt_capacity_reduced_prov(beta_lj, beta_lg, beta_pk, bolt_capacity_disp),
                   "")
            self.report_check.append(t13)

            T_e = round(self.bolt.bolt_tension/1000,2)

            t1 = (KEY_OUT_DISP_BOLT_TENSION_FORCE,force_in_bolt_due_to_load(P=round(self.load.axial_force, 2),
                                                             n=self.plate.bolts_required, T_ba=T_e,load='tension'),
                  '','')
            self.report_check.append(t1)

            if self.bolt.bolt_tensioning == 'Pretensioned':
                beta = 1
            else:
                beta = 2
            t = self.plate.thickness_provided
            f_o = round(0.7 * self.bolt.bolt_fu,2)
            l_e2= round(1.1 * t * math.sqrt(beta * f_o / self.plate.fy),2)
            l_e = round(min(self.plate.end_dist_provided, 1.1 * t * math.sqrt(beta * f_o / self.plate.fy)),2)
            col_g = (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius + self.plate.end_dist_provided)
            beam_g = (self.supported_section.web_thickness / 2 + self.weld.size + self.plate.end_dist_provided)
            # if col_g > beam_g:
            #     l_v = round(col_g - (self.supported_section.web_thickness / 2 + self.weld.size),2)
            # else:
            #     l_v = round(self.bolt.min_edge_dist_round,2)
            l_v = round(self.output[0][14]/2 - self.supported_section.web_thickness/2 - self.output[0][23], 2)
            b_e = min(self.output[0][13], 2 * l_v)
            Q = round(self.bolt.bolt_tension_prying/1000,2)

            t1 = (KEY_OUT_DISP_BOLT_PRYING_FORCE, cl_10_4_7_prying_force(l_v, l_e, l_e2, T_e, beta, f_o, b_e, t,
                                                                         self.plate.end_dist_provided, self.supported_section.root_radius,
                                                                         self.plate.fy, self.bolt.bolt_fu,
                                                                         f_o, self.supported_section.flange_width, self.plate.bolt_line,
                                                                         Q,eta=1.5),'','')
            self.report_check.append(t1)

            T_b = round(T_e+Q,2)

            t1 = (KEY_OUT_DISP_BOLT_TENSION_FORCE, total_bolt_tension_force(T_ba=T_e,
                                                                            Q=Q,
                                                                            T_b = T_b),
                  cl_10_3_5_bearing_bolt_tension_resistance(self.bolt.bolt_fu, self.bolt.bolt_fu,
                                                            self.bolt.bolt_shank_area, self.bolt.bolt_net_area,
                                                            self.bolt.bolt_tension_capacity),
                  get_pass_fail(T_b, self.bolt.bolt_tension_capacity, relation='leq'))
            self.report_check.append(t1)

            comb_bolt_ir = round((V_b / bolt_capacity_red) ** 2 + \
                           ((T_e + Q) / self.bolt.bolt_tension_capacity) ** 2,2)

            t1 = (KEY_DISP_IR, required_IR_or_utilisation_ratio(IR=1),
                  cl_10_3_6_bearing_bolt_combined_shear_and_tension(V_b, bolt_capacity_red, T_b, self.bolt.bolt_tension_capacity, comb_bolt_ir),
                  get_pass_fail(1, comb_bolt_ir, relation="greater"))
            self.report_check.append(t1)

            #
            t1 = ('SubSection', 'Plate Design', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (DISP_MIN_PLATE_HEIGHT, min_plate_ht_req(self.supported_section.depth, self.supported_section.root_radius,
                                                          self.supported_section.flange_thickness,self.min_plate_height),
                  self.plate.height,
                  get_pass_fail(self.min_plate_height, self.plate.height, relation="leq"))
            self.report_check.append(t1)
            t1 = (DISP_MAX_PLATE_HEIGHT, max_plate_ht_req(self.connectivity, self.supported_section.depth,
                                                          self.supported_section.flange_thickness,
                                                          self.supported_section.root_radius,
                                                          self.supported_section.notch_ht,
                                                          self.max_plate_height), self.plate.height,
                  get_pass_fail(self.max_plate_height, self.plate.height, relation="geq"))
            self.report_check.append(t1)

            t1 = (DISP_MIN_PLATE_THICK, min_plate_thk_req(self.supported_section.web_thickness),
                  self.plate.thickness_provided,
                  get_pass_fail(self.supported_section.web_thickness, self.plate.thickness_provided,
                                relation="lesser"))
            self.report_check.append(t1)

            if self.design_status_bolt is True:
                self.min_plate_width = round(self.plate.gauge_provided+2*self.bolt.min_edge_dist, 2)


                t1 = (DISP_MIN_PLATE_WIDTH, ep_min_plate_width_req(self.plate.gauge_provided,self.bolt.min_edge_dist,
                                                                   self.min_plate_width),
                      self.plate.width,
                      get_pass_fail(self.min_plate_width, self.plate.width, relation="leq"))
                self.report_check.append(t1)

                if self.connectivity == VALUES_CONN_1[0]:
                    self.max_plate_width = self.supporting_section.flange_width
                elif self.connectivity == VALUES_CONN_1[1]:
                    self.max_plate_width = self.supporting_section.depth - 2 * self.supporting_section.flange_thickness - \
                              2 * self.supporting_section.root_radius
                else:
                    self.max_plate_width = 'N/A'

                t1 = (DISP_MAX_PLATE_WIDTH, ep_max_plate_width_avail(self.connectivity,self.supporting_section.depth,
                                                                  self.supporting_section.flange_thickness,
                                                                  self.supporting_section.root_radius,self.supporting_section.flange_width,self.max_plate_width),
                      self.plate.width,
                      get_pass_fail(self.max_plate_width, self.plate.width, relation="geq"))
                self.report_check.append(t1)

                #######################
                # Plate Capacities
                #######################

                a = self.plate
                h = a.height
                t = a.thickness_provided

                t1 = (KEY_DISP_SHEAR_YLD, '', cl_8_4_shear_yielding_capacity_member(h, t, a.fy, gamma_m0, a.shear_capacity), '')
                self.report_check.append(t1)
                t1 = (
                    KEY_DISP_PLATE_BLK_SHEAR_SHEAR, '', cl_6_4_blockshear_capacity_member(Tdb=round(a.plate_block_shear_capacity, 2), stress='shear'), '')
                self.report_check.append(t1)
                t1 = (KEY_DISP_SHEAR_CAPACITY, self.load.shear_force,
                      cl_8_4_shear_capacity_member(a.shear_capacity, 0.0, a.plate_block_shear_capacity),
                      get_pass_fail(self.load.shear_force, a.shear_capacity, relation="lesser"))
                self.report_check.append(t1)

                ecc = round(self.bolt_dist_to_weld, 2)
                T_w = self.supporting_section.web_thickness
                R_r = self.supporting_section.root_radius
                e = self.bolt.min_edge_dist_round
                t_w = self.supported_section.web_thickness
                g = self.plate.gauge_provided
                s = self.weld.size
                M = self.plate.plate_moment

                t1 = (KEY_OUT_DISP_PLATE_MOM_CAPACITY, end_plate_moment_demand(self.connectivity,g,T_w,R_r,t_w,s, T_e, M),
                      cl_8_2_1_2_plastic_moment_capacity_member(beta_b=1.0, Z_p=round(self.plate.Z_p, 2), f_y=self.plate.fy,
                                                                gamma_m0=gamma_m0, Pmc=self.plate.plate_moment_capacity),
                      get_pass_fail(self.plate.plate_moment, self.plate.plate_moment_capacity, relation="lesser"))
                self.report_check.append(t1)

            ##################
            # Weld Checks
            ##################
            plate_status = self.get_plate_status(self)

            if self.design_status_bolt is True and plate_status is True:
                weld_conn_plates_fu = [self.plate.fu, self.supported_section.fu, self.weld.fu]
                weld_conn_plates_tk = [self.plate.thickness_provided,self.supported_section.web_thickness]
                [available_welds,weld_min,weld_max] = self.get_available_welds(self,weld_conn_plates_tk)
                t1 = ('SubSection', 'Weld Design', '|p{4cm}|p{5.5cm}|p{5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t1 = (DISP_MIN_WELD_SIZE, cl_10_5_2_3_min_fillet_weld_size_required(weld_conn_plates_tk, weld_min),
                      self.weld.size,
                      get_pass_fail(weld_min, self.weld.size, relation="leq"))
                self.report_check.append(t1)
                t1 = (DISP_MAX_WELD_SIZE, cl_10_5_3_1_max_weld_size(weld_conn_plates_tk, weld_max),
                      self.weld.size,
                      get_pass_fail(weld_max, self.weld.size, relation="geq"))
                self.report_check.append(t1)
                initial_weld_Strength = round(self.weld.strength/self.beta_lw,2)
                gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.weld.fabrication]
                t1 = (DISP_WELD_STRENGTH,
                      weld_strength_req(V=self.load.shear_force * 1000, A=self.load.axial_force * 1000,
                                        M=0.0, Ip_w=0.0,
                                        y_max=self.weld.eff_length / 2, x_max=0.0, l_w=2 * self.weld.eff_length,
                                        R_w=self.weld.stress),
                      cl_10_5_7_1_1_weld_strength(weld_conn_plates_fu, gamma_mw, self.weld.throat_tk,
                                                  initial_weld_Strength), '')
                self.report_check.append(t1)

                t15 = (KEY_OUT_LONG_JOINT_WELD, long_joint_welded_req(),
                       cl_10_5_7_3_weld_strength_post_long_joint(h=self.plate.height, l=0.0, t_t=self.weld.throat_tk,
                                                                 ws=initial_weld_Strength, wsr=self.weld.strength, direction='height'), "")
                self.report_check.append(t15)

                t5 = (
                    KEY_OUT_DISP_RED_WELD_STRENGTH, self.weld.stress, self.weld.strength,
                    get_pass_fail(self.weld.stress, self.weld.strength, relation="lesser"))
                self.report_check.append(t5)

        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_2d_image, Disp_3D_image, module=self.module)

    def get_plate_status(self):
        if self.plate.plate_moment < self.plate.plate_moment_capacity \
            and self.plate.plate_shear < self.plate.shear_capacity and self.max_plate_height >= self.plate.height >= self.min_plate_height and \
                self.plate.width >= self.min_plate_width:
            if self.connectivity in VALUES_CONN_2:
                return True
            else:
                if self.plate.width <= self.max_plate_width:
                    return True
                else:
                    return False

