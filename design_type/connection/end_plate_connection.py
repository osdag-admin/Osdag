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
import time
start_time = time.clock()

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

        t6 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC], ['Label_23'], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        t7 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC], ['Label_23'], TYPE_TEXTBOX, self.change_source)
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

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SUPTNGSEC_MATERIAL, KEY_SUPTDSEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_MATERIAL_G_O, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_WELD_FAB, KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_GAP,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    ####################################
    # Design Preference Functions End
    ####################################

    def set_osdaglogger(key):
        """
        Function to set Logger for End Plate Module
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

        if key is not None:
            handler = OurLog(key)
            # handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
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
        print("input values are set. Doing preliminary member checks")
        self.member_capacity(self)

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.type == "Rolled":
                self.supported_section.length = self.supported_section.depth
            else:
                self.supported_section.length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        else:
            self.supported_section.notch_ht = round_up(self.supporting_section.flange_thickness + self.supporting_section.root_radius + 5, 5)
            # length = self.supported_section.depth - self.supported_section.notch_ht
            if self.supported_section.type == "Rolled":
                self.supported_section.length = self.supported_section.depth - self.supported_section.notch_ht
            else:
                self.supported_section.length = self.supported_section.depth - (self.supported_section.flange_thickness + self.supported_section.notch_ht)    # -(2*self.supported_section.root_radius)

            # length = self.supported_section.depth - round_up((2*self.supporting_section.flange_thickness),5)  # TODO: Subtract notch height for beam-beam connection

        # self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.shear_yielding_capacity = round(IS800_2007.cl_8_4_design_shear_strength(
            self.supported_section.length*self.supported_section.web_thickness, self.supported_section.fy) / 1000, 2)
        self.supported_section.shear_capacity = self.supported_section.shear_yielding_capacity
        # self.supported_section.tension_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.tension_yielding_capacity = round(IS800_2007.cl_6_2_tension_yielding_strength(
            self.supported_section.length*self.supported_section.web_thickness, self.supported_section.fy) / 1000, 2)
        self.supported_section.tension_capacity = self.supported_section.tension_yielding_capacity
        if self.load.shear_force <= min(0.15 * self.supported_section.shear_yielding_capacity, 40.0):
            logger.warning(" : User input for shear force is very less compared to section capacity. "
                "Setting Shear Force value to 15% of supported beam shear capacity or 40kN, whichever is less.")
            self.load.shear_force = min(0.15 * self.supported_section.shear_yielding_capacity, 40.0)

        if self.supported_section.shear_yielding_capacity > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity > self.load.axial_force:
            print("preliminary member check is satisfactory. Doing bolt checks")
            self.design_status = True
            self.select_bolt_plate_arrangement(self)
        else:
            self.design_status = False
            logger.error(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
                           "than applied loads, Please select larger sections or decrease loads"
                            .format(self.supported_section.shear_yielding_capacity,
                                    self.supported_section.tension_yielding_capacity))
            print("failed in preliminary member checks. Select larger sections or decrease loads")

    def select_bolt_plate_arrangement(self):
        self.output = []
        count = 0
        plate_cost = 7850e-9 # considered: Rs 1 per kg TODO: take input from user
        bolt_cost = 1 # considered: Rs 1 per unit TODO: take input from user
        for self.plate.thickness_provided in sorted(self.plate.thickness):
            self.plate.connect_to_database_to_get_fy_fu(self.plate.material, self.plate.thickness_provided)
            design_status_plate = True
            self.min_plate_height = self.supported_section.min_plate_height()
            self.supported_section.notch_ht = max((round_up(self.supporting_section.flange_thickness
                                                           + self.supporting_section.root_radius, 5) + 5),
                                                  (round_up(self.supported_section.flange_thickness
                                                           + self.supported_section.root_radius, 5) + 5))
            # print("Notch Height:", self.supported_section.notch_ht)
            self.max_plate_height = self.supported_section.max_plate_height(self.connectivity, self.supported_section.notch_ht)
            # self.res_force = math.sqrt(self.load.shear_force ** 2 + self.load.axial_force ** 2) * 1000
            # if self.connectivity == VALUES_CONN_1[1]:
            self.plate.thickness_check = max(min(self.plate.thickness), math.ceil(self.supported_section.web_thickness))

            if self.plate.thickness_check > max(self.plate.thickness):
                design_status_plate = False
                self.design_status = False
                logger.error(" : Select plate of higher thickness")
                break

            for t in self.plate.thickness:
                if t >= self.plate.thickness_check:
                    self.plate.thickness_check = t
                    break

            if self.plate.thickness_provided < self.plate.thickness_check:
                design_status_plate = False

            # TO GET BOLT BEARING CAPACITY CORRESPONDING TO PLATE THICKNESS AND Fu AND Fy #
            self.bolt_conn_plates_t_fu_fy = []
            self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
            if self.connectivity == VALUES_CONN_1[1]:
                self.bolt_conn_plates_t_fu_fy.append(
                    (self.supporting_section.flange_thickness, self.supporting_section.fu, self.supporting_section.fy))
            else:
                self.bolt_conn_plates_t_fu_fy.append(
                    (self.supporting_section.web_thickness, self.supporting_section.fu, self.supporting_section.fy))

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

            if design_status_plate is True:
                for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
                    bolts_required_initial = 4

                    for self.bolt.bolt_grade_provided in reversed(self.bolt.bolt_grade):
                        design_status_bolt = True
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

                    # comb_bolt_ir=2
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
                                self.bolt.bolt_tension_capacity, bolts_required_initial, b_e, l_v, 1.0)

                        print("Bolts required:", self.bolts_required_IR_LT1)

                    # return self.bolts_required
                        bolt_rows = self.bolts_required_IR_LT1/2

                        [bolt_line, bolts_one_line, web_plate_h] = \
                            self.plate.get_web_plate_l_bolts_one_line(self.max_plate_height, self.min_plate_height,
                                                                      bolt_rows, self.bolt.min_end_dist_round,
                                                                      self.bolt.min_gauge_round)

                        if bolt_rows > bolts_one_line:
                            design_status_bolt = False
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
                        # Updating bolt bearing capacity

                        if self.bolt.bolt_type == "Bearing Bolt":
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
                            self.get_plate_capacity(self, self.plate.thickness_provided, self.plate.height,
                                                    self.max_plate_height, pitch,
                                                    self.bolt_dist_to_weld, end_dist,
                                                    bolt_rows, self.bolt.dia_hole)
                        # print("plate_moment:", self.plate.plate_moment)
                        # print("plate_shear:", self.plate.plate_shear)
                        # print("plate_moment_capacity:", self.plate.plate_moment_capacity)
                        # print("shear_capacity:", self.plate.shear_capacity)

                        if self.plate.plate_moment > self.plate.plate_moment_capacity or \
                                self.plate.plate_shear > self.plate.shear_capacity:
                            design_status_plate = False
                            [bolt_rows, pitch, end_dist, design_status_plate] = self.plate_check(self, bolt_rows,
                                                                                pitch, end_dist, design_status_plate)
                        else:
                            design_status_plate = True

                        if design_status_bolt is True and design_status_plate is True:
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

                            if self.weld.design_status is True:
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
                                self.get_plate_capacity(self, self.plate.thickness_provided, self.plate.height,
                                                        self.max_plate_height, pitch,
                                                        self.bolt_dist_to_weld, end_dist,
                                                        bolt_rows, self.bolt.dia_hole)

                            if self.plate.design_status is True:
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
                                       int(self.bolt.bolt_diameter_provided),                      #1-Bolt Diameter
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

                                       'INSERT_HERE',                                                   #XX- EMPTY
                                       # total_cost,
                                       count]
                                self.output.append(row)
                                print("********* Trial {} ends here *************".format(count))

                    if bolts_one_line <= 1 and self.bolt.bolt_diameter_provided == min(self.bolt.bolt_diameter) \
                            and self.bolt.bolt_grade_provided == min(self.bolt.bolt_grade) \
                            and self.plate.thickness_provided == sorted(self.plate.thickness)[-1]:
                        self.design_status = False
                        design_status_bolt = False
                        logger.error(" : Select bolt of lower diameter, sufficient plate height/ width not available to arrange bolts")

        if count == 0 and self.plate.design_status == False:
            self.design_status = False
            logger.error(" : Select bolt of lower diameter, sufficient plate width/ height is not available to arrange bolts")
        elif count == 0:
            self.design_status = False
            # print(self.design_status)
            # return self.design_status
            if design_status_plate is False:
                logger.error(" : Select plate of higher thickness")

            if self.weld.design_status is False:
                # TODO: Check logger message
                logger.error(": Weld thickness is not sufficient [cl. 10.5.7, IS 800:2007]")
                #logger.warning(": Minimum weld thickness required is %2.2f mm " % self.weld.t_weld_req)
                logger.info(": Should increase length of weld/End plate")
                # logger.error(
                #   ": For given members and %2.2f mm thick plate, weld sizes should be of range %2.2f mm and  %2.2f mm "
                #   % self.plate.thickness_provided % weld_size_min % weld_size_max)#
                logger.info(": Cannot design weld with available welds ")
        else:
            # self.get_design_status(self)
            self.output.sort(key=lambda x: (x[3], x[0], x[1], x[2]))
            self.set_values_to_class(self)
            print("No of effective trials: ", count)
            print(self.output[0])
            if self.output[0][26] == self.output[0][27]:
                logger.info("Minimum weld size given in Table 21 of IS800:2007 is greater than or equal to thickness "
                            "of thinner connecting plate")
                logger.info("Thicker plate shall be adequately preheated to prevent cracking of the weld")
            self.get_design_status(self)

    def set_values_to_class(self):
        self.plate.bolt_line = 2  # only one line of bolts provided on each side of web
        self.plate.bolts_one_line = self.output[0][0]
        self.plate.bolts_required = self.plate.bolt_line * self.plate.bolts_one_line
        self.bolt.bolt_diameter_provided = self.output[0][1]
        self.bolt.bolt_grade_provided = self.output[0][2]

        self.plate.thickness_provided = self.output[0][3]
        self.plate.height = self.output[0][4]
        self.plate.width = self.output[0][5]

        self.bolt.bolt_capacity = self.output[0][6]
        self.bolt.bolt_shear_capacity = self.output[0][7]
        self.bolt.bolt_bearing_capacity_disp = self.output[0][8]
        self.bolt.bolt_tension_capacity = self.output[0][9]
        self.bolt.bolt_shear = self.output[0][10]
        self.bolt.bolt_tension = self.output[0][11]
        self.bolt.bolt_tension_prying = self.output[0][17]

        self.plate.pitch_provided = self.output[0][13]
        self.plate.gauge_provided = self.output[0][14]
        self.plate.end_dist_provided = self.output[0][15]
        self.plate.edge_dist_provided = self.output[0][16]

        self.plate.plate_shear = self.output[0][18]
        self.plate.plate_moment = self.output[0][19]
        self.plate.shear_capacity = self.output[0][20]
        self.plate.plate_block_shear_capacity = self.output[0][21]
        self.plate.plate_moment_capacity = self.output[0][22]

        self.weld.length = self.output[0][4]
        self.weld.size = self.output[0][23]
        self.weld.stress = self.output[0][24]
        self.weld.strength = self.output[0][25]
        self.weld.weld_size_max = self.output[0][26]
        self.weld.weld_size_min = self.output[0][27]

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
        l_j = pitch * (bolts_one_line - 1)
        beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided, l_j)
        print("beta_lj", beta_lj)
        col_g = (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius + self.bolt.min_end_dist_round)
        beam_g = (self.supported_section.web_thickness / 2 + weld_size + self.bolt.min_end_dist_round)
        if col_g > beam_g:
            l_v = col_g - (self.supported_section.web_thickness / 2 + weld_size)
        else:
            l_v = self.bolt.min_edge_dist_round
        b_e = min(pitch, 2 * l_v)

        [self.bolt.bolt_shear, self.bolt.bolt_tension, self.bolt.bolt_tension_prying, bolts_n] = \
            self.get_bolt_IR(self, self.bolt.bolt_capacity, self.bolt.bolt_tension_capacity,
                             bolts_one_line * 2, b_e, l_v, beta_lj)
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
                    self.get_plate_capacity(self, self.plate.thickness_provided, self.plate.height,
                                            self.max_plate_height, pitch,
                                            self.bolt_dist_to_weld, end_dist,
                                            bolt_rows, self.bolt.dia_hole)
                self.plate.plate_moment = self.bolt_dist_to_weld * self.bolt.bolt_tension
                # self.plate.plate_shear = self.load.shear_force * 1000
                if self.plate.plate_moment > self.plate.plate_moment_capacity or \
                        self.plate.plate_shear > self.plate.shear_capacity:
                    design_status_plate = False
                    bolt_rows += 1
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
            l_j = pitch * (bolts_one_line - 1)
            beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided, l_j)
            print("beta_lj", beta_lj)
            if self.bolt.bolt_type == "Bearing Bolt":
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
                             bolts_one_line * 2, b_e, l_v, beta_lj)

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

        print("web", pitch, edge_dist, plate_h)
        return pitch, edge_dist, plate_h, bolts_one_line

    def get_bolt_IR(self, bolt_shear_capacity, bolt_tension_capacity, no_bolt, b_e, l_v, beta_lj = 1.0):
        while True:
            self.bolt.bolt_shear = self.load.shear_force * 1000 / no_bolt  # N
            print("bolt_shear", self.bolt.bolt_shear)
            self.bolt.bolt_tension = self.load.axial_force * 1000 / no_bolt  # N
            print("bolt_tension", self.bolt.bolt_tension)
            # TODO: check available effective width per pair of bolts (b_e)
            self.bolt.bolt_tension_prying = IS800_2007.cl_10_4_7_bolt_prying_force(self.bolt.bolt_tension, l_v,
                                        0.7*self.bolt.bolt_fu, b_e, self.plate.thickness_provided,
                                        self.plate.fy, self.bolt.min_end_dist_round, self.bolt.bolt_tensioning)
            print("bolt_tension_prying", self.bolt.bolt_tension_prying)
            comb_bolt_ir = (self.bolt.bolt_shear / (bolt_shear_capacity*beta_lj)) ** 2 + \
                           ((self.bolt.bolt_tension + self.bolt.bolt_tension_prying)/bolt_tension_capacity) ** 2
            print(comb_bolt_ir)
            if comb_bolt_ir > 1:
                no_bolt += 2
            else:
                break
        return self.bolt.bolt_shear, self.bolt.bolt_tension, self.bolt.bolt_tension_prying, no_bolt

    def get_plate_capacity(self, p_th, p_h, p_h_max, pitch, bolt_dist, end, n_row, bolt_hole_dia):
        # plate_moment = min_edge_dist * bolt_tension
        Z_p = (min(pitch, 2 * bolt_dist)) * p_th **2 /4
        Z_e = (min(pitch, 2 * bolt_dist)) * p_th **2 /6
        plate_moment_capacity = IS800_2007.cl_8_2_1_2_design_moment_strength(Z_e, Z_p, self.plate.fy, 'plastic')
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
        available_welds = list([x for x in ALL_WELD_SIZES if (weld_size_min <= x <= weld_size_max)])
        # if available_welds == [] and weld_size_min < max(ALL_WELD_SIZES):
        #     available_welds = [weld_size_min]
        return available_welds,weld_size_min,weld_size_max

    def design_weld(self,available_welds):
        self.weld.design_status = False
        self.weld.size = available_welds[0]
        while self.plate.height <= self.max_plate_height:
            self.weld.length = self.plate.height
            weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
                fillet_size=self.weld.size, fusion_face_angle=90)
            weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
                fillet_size=self.weld.size, available_length=self.weld.length)
            self.weld.get_weld_strength(connecting_fu=[self.supporting_section.fu, self.weld.fu],
                                                weld_fabrication=self.weld.fabrication,
                                                t_weld=self.weld.size, weld_angle=90)
            beta_lw = IS800_2007.cl_10_5_7_3_weld_long_joint(weld_eff_length, weld_throat)
            self.weld.strength = self.weld.strength * beta_lw
            force_h = self.load.shear_force * 1000
            force_l = self.load.axial_force * 1000
            # force_t = self.plate.moment_demand
            self.weld.get_weld_stress(force_h, force_l, l_weld=2*weld_eff_length, weld_twist= 0.0, Ip_weld=0.0, y_max=0.0,
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
                    logger.warning('weld stress is guiding plate height, trying with length %2.2f mm' % self.plate.height)
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

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  self.output[0][7] if flag else '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, self.output[0][8] if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.output[0][6] if flag else '', True)
        out_list.append(t6)

        t6_1 = (KEY_OUT_BOLT_TENSION_CAPACITY, KEY_OUT_DISP_BOLT_TENSION_CAPACITY, TYPE_TEXTBOX, self.output[0][9] if flag else '', True)
        out_list.append(t6_1)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_FORCE, TYPE_TEXTBOX, self.output[0][10] if flag else '', True)
        out_list.append(t21)

        t21_1 = (KEY_OUT_BOLT_TENSION_FORCE, KEY_OUT_DISP_BOLT_TENSION_FORCE, TYPE_TEXTBOX, self.output[0][11] if flag else '', True)
        out_list.append(t21_1)

        t21_2 = (KEY_OUT_BOLT_PRYING_FORCE, KEY_OUT_DISP_BOLT_PRYING_FORCE, TYPE_TEXTBOX, self.output[0][17] if flag else '', True)
        out_list.append(t21_2)

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

    def spacing(self, flag):

        spacing = []

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
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")
        self.report_supporting = {KEY_DISP_SEC_PROFILE: "ISection",
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
            KEY_DISP_SEC_PROFILE: "ISection",  # Image shall be save with this name.png in resource files
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
             "Supporting Section": "TITLE",
             "Supporting Section Details": self.report_supporting,
             "Supported Section": "TITLE",
             "Supported Section Details": self.report_supported,
             "Bolt Details": "TITLE",
             KEY_DISP_D: str(self.bolt.bolt_diameter),
             KEY_DISP_GRD: str(self.bolt.bolt_grade),
             KEY_DISP_TYP: self.bolt.bolt_type,
             KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
             KEY_DISP_DP_BOLT_SLIP_FACTOR: self.bolt.mu_f,
             KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
             KEY_DISP_GAP: self.plate.gap,
             KEY_DISP_CORR_INFLUENCES: self.bolt.corrosive_influences,
             "Plate Details": "TITLE",
             KEY_DISP_PLATETHK: str(self.plate.thickness),
             KEY_DISP_MATERIAL: self.plate.material,
             KEY_DISP_FU: self.plate.fu,
             KEY_DISP_FY: self.plate.fy}

        self.report_check = []
        if self.plate.design_status is True:

            t1 = ('SubSection', 'Bolt Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t1 = (KEY_DISP_D, '', self.bolt.bolt_diameter_provided, '')
            self.report_check.append(t1)
            t1 = (KEY_DISP_GRD, '', self.bolt.bolt_grade_provided, '')
            self.report_check.append(t1)
            t1 = (KEY_DISP_PLTHICK, '', self.plate.thickness_provided,'')
            self.report_check.append(t1)
            t6 = (DISP_NUM_OF_COLUMNS, 2, self.plate.bolt_line, get_pass_fail(2, self.plate.bolt_line, relation='leq'))
            self.report_check.append(t6)
            t7 = (DISP_NUM_OF_ROWS, 2, self.plate.bolts_one_line, get_pass_fail(2, self.plate.bolts_one_line, relation='leq'))
            self.report_check.append(t7)
            t1 = (DISP_MIN_PITCH, min_pitch(self.bolt.bolt_diameter_provided),
                  self.plate.gauge_provided,
                  get_pass_fail(self.bolt.min_pitch, self.plate.gauge_provided, relation='lesser'))
            self.report_check.append(t1)
            t1 = (DISP_MAX_PITCH, max_pitch(self.connecting_plates_tk),self.plate.gauge_provided,
                  get_pass_fail(self.bolt.max_spacing, self.plate.gauge_provided, relation='greater'))
            self.report_check.append(t1)
            t2 = (DISP_MIN_GAUGE, min_pitch(self.bolt.bolt_diameter_provided),
                  self.plate.pitch_provided,
                  get_pass_fail(self.bolt.min_gauge, self.plate.pitch_provided, relation="lesser"))
            self.report_check.append(t2)
            t2 = (DISP_MAX_GAUGE, max_pitch(self.connecting_plates_tk),self.plate.pitch_provided,
                  get_pass_fail(self.bolt.max_spacing, self.plate.pitch_provided, relation="greater"))
            self.report_check.append(t2)
            t3 = (DISP_MIN_END, min_edge_end(self.bolt.d_0, self.bolt.edge_type),self.plate.edge_dist_provided,
                  get_pass_fail(self.bolt.min_end_dist, self.plate.edge_dist_provided, relation='lesser'))
            self.report_check.append(t3)
            t4 = (DISP_MAX_END, max_edge_end_new(self.bolt_conn_plates_t_fu_fy, self.bolt.corrosive_influences),
                  self.plate.edge_dist_provided,
                  get_pass_fail(self.bolt.max_end_dist, self.plate.edge_dist_provided, relation='greater'))
            self.report_check.append(t4)
            t3 = (DISP_MIN_EDGE, min_edge_end(self.bolt.d_0, self.bolt.edge_type),
                  self.plate.end_dist_provided,
                  get_pass_fail(self.bolt.min_edge_dist, self.plate.end_dist_provided, relation='lesser'))
            self.report_check.append(t3)
            t4 = (DISP_MAX_EDGE, max_edge_end_new(self.bolt_conn_plates_t_fu_fy, self.bolt.corrosive_influences),
                  self.plate.end_dist_provided,
                  get_pass_fail(self.bolt.max_edge_dist, self.plate.end_dist_provided, relation="greater"))
            self.report_check.append(t4)

            if self.bolt.bolt_type == TYP_BEARING:
                t1 = (KEY_OUT_DISP_BOLT_SHEAR, '', bolt_shear_prov(self.bolt.bolt_fu, 1, self.bolt.bolt_net_area,
                                                                   self.bolt.gamma_mb, self.bolt.bolt_shear_capacity), '')
                self.report_check.append(t1)
                t8 = (KEY_DISP_KB, " ",
                      kb_prov(self.plate.end_dist_provided, self.plate.pitch_provided, self.bolt.dia_hole,
                              self.bolt.bolt_fu, self.bolt.fu_considered), '')
                self.report_check.append(t8)
                kb = self.bolt.calculate_kb(self.plate.end_dist_provided, self.plate.pitch_provided, self.bolt.dia_hole,
                              self.bolt.bolt_fu, self.bolt.fu_considered)
                t2 = (
                KEY_OUT_DISP_BOLT_BEARING, '', bolt_bearing_prov(kb, self.bolt.bolt_diameter_provided,
                                                                 self.bolt_conn_plates_t_fu_fy, self.bolt.gamma_mb,
                                                                 self.bolt.bolt_bearing_capacity), '')
                self.report_check.append(t2)
                t3 = (KEY_OUT_DISP_BOLT_CAPACITY, '',
                      bolt_capacity_prov(self.bolt.bolt_shear_capacity, self.bolt.bolt_bearing_capacity, self.bolt.bolt_capacity),
                      '')
                self.report_check.append(t3)
            else:
                kh_disp = round(self.bolt.kh, 2)
                t4 = (KEY_OUT_DISP_BOLT_SLIP, '',
                      HSFG_bolt_capacity_prov(mu_f=self.bolt.mu_f, n_e=1, K_h=kh_disp, fub=self.bolt.bolt_fu,
                                              Anb=self.bolt.bolt_net_area, gamma_mf=self.bolt.gamma_mf,
                                              capacity=self.bolt.bolt_capacity), '')
                self.report_check.append(t4)

            l_j = self.plate.pitch_provided * (self.plate.bolts_one_line - 1)
            beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(self.bolt.bolt_diameter_provided, l_j)
            bolt_capacity_red = self.bolt.bolt_capacity * beta_lj

            t10 = (KEY_OUT_LONG_JOINT, long_joint_bolted_req(),
                   long_joint_bolted_prov(self.plate.bolt_line, self.plate.bolts_one_line,
                                          self.plate.gauge_provided, self.plate.pitch_provided,
                                          self.bolt.bolt_diameter_provided, self.bolt.bolt_capacity, bolt_capacity_red),
                   "")
            self.report_check.append(t10)

            t1 = (KEY_OUT_DISP_BOLT_TENSION_FORCE+r',~$T_{ba}$',tension_in_bolt_due_to_axial(P=round(self.load.axial_force, 2),
                                                             n=self.plate.bolts_required, T_ba=self.bolt.bolt_tension),
                  '','')
            self.report_check.append(t1)
            T_e = self.bolt.bolt_tension

            if self.bolt.bolt_tensioning == 'Pretensioned':
                beta = 1
            else:
                beta = 2
            t = self.plate.thickness_provided
            f_o = 0.7 * self.bolt.bolt_fu

            l_e = round(min(self.plate.end_dist_provided, 1.1 * t * math.sqrt(beta * f_o / self.plate.fy)),2)
            col_g = (self.supporting_section.web_thickness / 2 + self.supporting_section.root_radius + self.plate.end_dist_provided)
            beam_g = (self.supported_section.web_thickness / 2 + self.weld.size + self.plate.end_dist_provided)
            if col_g > beam_g:
                l_v = col_g - (self.supported_section.web_thickness / 2 + self.weld.size)
            else:
                l_v = self.bolt.min_edge_dist_round
            b_e = min(self.plate.pitch_provided, 2 * l_v)
            Q = self.bolt.bolt_tension_prying

            t1 = (KEY_OUT_DISP_BOLT_PRYING_FORCE+',~Q', tension_in_bolt_due_to_prying(T_e, l_v, f_o, b_e, t, self.plate.fy,
                                                                                self.bolt.min_end_dist_round,
                                                                                self.bolt.bolt_tensioning,
                                                                                beta,Q,l_e,eta=1.5),'','')
            self.report_check.append(t1)

            T_b = self.bolt.bolt_tension + self.bolt.bolt_tension_prying
            t1 = (KEY_OUT_DISP_BOLT_TENSION_FORCE+r',~$T_b$', total_bolt_tension_force(T_ba=self.bolt.bolt_tension,
                                                                            Q=self.bolt.bolt_tension_prying,
                                                                            T_b = T_b),
                  tension_capacity_of_bolt(f_ub=self.bolt.bolt_fu, A_nb=self.bolt.bolt_net_area,
                                           T_db=self.bolt.bolt_tension_capacity),
                  get_pass_fail(T_b, self.bolt.bolt_tension_capacity, relation='leq'))
            self.report_check.append(t1)

            comb_bolt_ir = (self.bolt.bolt_shear / (self.bolt.bolt_capacity * beta_lj)) ** 2 + \
                           ((self.bolt.bolt_tension + self.bolt.bolt_tension_prying) / self.bolt.bolt_tension_capacity) ** 2

            t1 = (KEY_DISP_IR, IR_req(IR=1),
                  IR_prov(bolt_capacity_red,self.load.shear_force, T_b,self.load.axial_force,comb_bolt_ir),
                  get_pass_fail(1, comb_bolt_ir, relation="greater"))
            self.report_check.append(t1)

            #
            t1 = ('SubSection', 'Plate Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            #
            # t1 = (DISP_MIN_PLATE_HEIGHT, min_plate_ht_req(self.supported_section.depth, self.min_plate_height),
            #       self.plate.height,
            #       get_pass_fail(self.min_plate_height, self.plate.height, relation="lesser"))
            # self.report_check.append(t1)
            # t1 = (DISP_MAX_PLATE_HEIGHT, max_plate_ht_req(self.connectivity, self.supported_section.depth,
            #                                               self.supported_section.flange_thickness,
            #                                               self.supported_section.root_radius,
            #                                               self.supported_section.notch_ht,
            #                                               self.max_plate_height), self.plate.height,
            #       get_pass_fail(self.max_plate_height, self.plate.height, relation="greater"))
            # self.report_check.append(t1)
            # min_plate_length = self.plate.gap + 2 * self.bolt.min_end_dist + (
            #             self.plate.bolt_line - 1) * self.bolt.min_pitch
            # t1 = (DISP_MIN_PLATE_LENGTH, min_plate_length_req(self.bolt.min_pitch, self.bolt.min_end_dist,
            #                                                   self.plate.bolt_line, min_plate_length),
            #       self.plate.length,
            #       get_pass_fail(min_plate_length, self.plate.length, relation="lesser"))
            # self.report_check.append(t1)
            # t1 = (DISP_MIN_PLATE_THICK, min_plate_thk_req(self.supported_section.web_thickness),
            #       self.plate.thickness_provided,
            #       get_pass_fail(self.supported_section.web_thickness, self.plate.thickness_provided,
            #                     relation="lesser"))
            # self.report_check.append(t1)

            #######################
            # Section Capacities
            #######################
            for a in [self.plate, self.supported_section]:
            # for a in [self.supported_section]:
                gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
                gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
                if a == self.plate:
                    h = a.height
                    t = a.thickness_provided
                else:
                    t1 = ('SubSection', 'Section Design Checks', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                    self.report_check.append(t1)
                    h = a.length
                    t = a.web_thickness

                t1 = (KEY_DISP_SHEAR_YLD, '', shear_yield_prov(h, t, a.fy, gamma_m0, a.shear_capacity), '')
                self.report_check.append(t1)

                t1 = (KEY_DISP_SHEAR_CAPACITY, self.load.shear_force,
                      shear_capacity_prov(a.shear_capacity, 0.00, 0.00),
                      get_pass_fail(self.load.shear_force, a.shear_capacity, relation="lesser"))
                self.report_check.append(t1)

                # t1 = (KEY_OUT_DISP_PLATE_MOM_CAPACITY, self.plate.plate_moment, a.moment_capacity,
                #       get_pass_fail(self.plate.plate_moment, a.moment_capacity, relation="lesser"))
                # self.report_check.append(t1)

            #######################
            # Plate Capacities
            #######################
                if a == self.plate:
                    t1 = (KEY_OUT_DISP_PLATE_MOM_CAPACITY, self.plate.plate_moment, self.plate.plate_moment_capacity,
                          get_pass_fail(self.plate.plate_moment, self.plate.plate_moment_capacity, relation="lesser"))
                    self.report_check.append(t1)

        Disp_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_3D_image)