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
from utils.common.component import Bolt, Plate, Weld
# from gui.ui_summary_popup import Ui_Dialog
from utils.common.component import *
# from cad.common_logic import CommonDesignLogic
from utils.common.material import *
from Common import *
from utils.common.load import Load
from design_report.reportGenerator import save_html
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
        return KEY_DISP_ENDPLATE

    def input_values(self, existingvalues={}):

        """
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        """

        # @author: Amir, Umair
        self.module = KEY_DISP_ENDPLATE
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

        t16 = (KEY_MODULE, KEY_DISP_ENDPLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN)
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, VALUES_COLSEC)
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, VALUES_BEAMSEC)
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None)
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None)
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None)
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D)
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        options_list.append(t14)

        return options_list

    def func_for_validation(self, design_dictionary):
        all_errors = []
        self.design_status = False
        flag = False
        flag1 = False
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
            #     if design_dictionary[option[0]] == "End Plate":

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
            column = design_dictionary[KEY_SUPTNGSEC]
            beam = design_dictionary[KEY_SUPTDSEC]
            conn = sqlite3.connect(PATH_TO_DATABASE)
            cursor = conn.execute("SELECT D FROM COLUMNS WHERE Designation = ( ? ) ", (column,))
            lst = []
            rows = cursor.fetchall()
            for row in rows:
                lst.append(row)
            c_val = lst[0][0]
            cursor2 = conn.execute("SELECT B FROM BEAMS WHERE Designation = ( ? )", (beam,))
            lst1 = []
            rows1 = cursor2.fetchall()
            for row1 in rows1:
                lst1.append(row1)
            b_val = lst1[0][0]
            if c_val <= b_val:
                error = "Beam width is higher than clear depth of column web " + "\n" + "(No provision in Osdag till now)"
                all_errors.append(error)
            else:
                flag1 = True
        else:
            flag1 = True

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        if flag and flag1:
            self.set_input_values(self, design_dictionary)
        else:
            return all_errors

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
        super(EndPlateConnection,self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.weld = Weld(material_grade=design_dictionary[KEY_MATERIAL], material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O], fabrication=design_dictionary[KEY_DP_WELD_FAB])
        # self.weld = Weld(size=10, length= 100, material_grade=design_dictionary[KEY_MATERIAL])
        print("input values are set. Doing preliminary member checks")
        self.member_capacity(self)

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.type == "Rolled":
                length = self.supported_section.depth
            else:
                length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        else:
            self.supported_section.notch_ht = round_up(self.supporting_section.flange_thickness*2, 5)
            # length = self.supported_section.depth - self.supported_section.notch_ht
            if self.supported_section.type == "Rolled":
                length = self.supported_section.depth - self.supported_section.notch_ht
            else:
                length = self.supported_section.depth - (self.supported_section.flange_thickness + self.supported_section.notch_ht)    # -(2*self.supported_section.root_radius)

            # length = self.supported_section.depth - round_up((2*self.supporting_section.flange_thickness),5)  # TODO: Subtract notch height for beam-beam connection

        self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.tension_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)

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
            # print("Plate thickness:", self.plate.thickness_check)
            # elif self.connectivity == VALUES_CONN_1[2]:
            #     self.plate.thickness_check = max(min(self.plate.thickness),
            #                                         math.ceil(self.supporting_section.web_thickness))
            # else:
            #     self.plate.thickness_check = max(min(self.plate.thickness), math.ceil(self.supporting_section.web_thickness))

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
                        [self.bolt.bolt_shear,self.bolt.bolt_tension,self.bolt.bolt_tension_prying,self.bolts_required_IR_LT1] = \
                            self.get_bolt_IR(self, self.bolt.bolt_capacity,self.bolt.bolt_tension_capacity, bolts_required_initial, 1.0)

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

                        self.plate.height = web_plate_h
                        self.plate.plate_moment = self.bolt.min_edge_dist_round * self.bolt.bolt_tension
                        self.plate.plate_shear = self.load.shear_force*1000

                        [self.plate.plate_moment_capacity, self.plate.plate_shear_capacity, self.plate.plate_block_shear_capacity] = \
                            self.get_plate_capacity(self, self.plate.thickness_provided, self.plate.height, pitch,
                                                    self.bolt.min_edge_dist_round, end_dist,
                                                    bolt_rows, self.bolt.dia_hole)
                        # print("plate_moment:", self.plate.plate_moment)
                        # print("plate_shear:", self.plate.plate_shear)
                        # print("plate_moment_capacity:", self.plate.plate_moment_capacity)
                        # print("plate_shear_capacity:", self.plate.plate_shear_capacity)

                        if self.plate.plate_moment > self.plate.plate_moment_capacity or \
                                self.plate.plate_shear > self.plate.plate_shear_capacity:
                            design_status_plate = False
                        else:
                            design_status_plate = True

                        if design_status_bolt is True and design_status_plate is True:
                            self.weld.design_status = False
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
                            #
                            #     print("Weld Leg Size (mm): ", self.weld.size)
                            #     print("Weld Stress (N/mm): ", self.weld.stress)
                            #     print("Weld Strength (N/mm): ", self.weld.strength)

                            if self.weld.design_status is True:
                                plate_width = round_up(self.weld.size +
                                    self.bolt.min_edge_dist_round * 4 + self.supported_section.web_thickness, 2)
                                self.plate_width_check(self, plate_width)

                            if self.plate.height > web_plate_h:
                                [pitch, end_dist, self.plate.height] = self.get_pitch_end_dist(self.plate.height,
                                                                                                bolt_rows,
                                                                                                self.bolt.min_end_dist_round,
                                                                                                self.bolt.max_spacing_round,
                                                                                                self.bolt.max_edge_dist_round)

                            if self.plate.design_status is True:
                                count += 1
                                gauge = round_up(self.weld.size +
                                    self.bolt.min_edge_dist_round * 2 + self.supported_section.web_thickness, 2)

                                # TRIAL FUNCTION #
                                # total_cost = self.plate.height*plate_width*self.plate.thickness_provided*plate_cost + \
                                #              bolt_rows*bolt_cost*self.bolt.bolt_diameter_provided*self.bolt.bolt_grade_provided/100
                                # trial function for cost optimisation
                                # todo: Finalize optimisation function
                                # print("plate cost:", self.plate.height*plate_width*self.plate.thickness_provided*plate_cost)
                                # print("bolt cost:", bolt_rows*bolt_cost*self.bolt.bolt_diameter_provided*self.bolt.bolt_grade_provided/100)

                                ##### O U T P U T   D I C T I O N A R Y   F O R M A T #####
                                row = [int(bolt_rows),                                                  # 0-Rows of Bolts
                                       str(int(self.bolt.bolt_diameter_provided)),                      #1-Bolt Diameter
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
                                       round(self.plate.plate_shear/1000, 2),                           #18-Plate Shear
                                       round(self.plate.plate_moment/1000000, 3),                       #19-Plate Moment
                                       round(self.plate.plate_shear_capacity/1000, 2),                  #20-Plate Shear Capacity
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
                        logger.error(" : Select bolt of lower diameter, sufficient plate height not available")

        if count == 0 and self.plate.design_status == False:
            self.design_status = False
            logger.error(" : Select bolt of lower diameter, sufficient plate width is not available")
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
        self.bolt.bolt_diameter_provided = self.output[0][1]
        self.plate.thickness_provided = self.output[0][3]
        self.plate.height = self.output[0][4]
        self.plate.width = self.output[0][5]
        self.plate.pitch_provided = self.output[0][13]
        self.plate.gauge_provided = self.output[0][14]
        self.plate.end_dist_provided = self.output[0][15]
        self.plate.edge_dist_provided = self.output[0][16]
        self.plate.bolts_one_line = self.output[0][0]
        self.plate.bolt_line = 2                               # only one line of bolts provided on each side of web
        self.weld.length = self.output[0][4]
        self.weld.size = self.output[0][23]

    def get_pitch_end_dist(self, plate_h, bolts_one_line, edge_dist, max_spacing, max_edge_dist):
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
            self.get_bolt_IR(self, self.bolt.bolt_capacity, self.bolt.bolt_tension_capacity,
                             bolts_one_line * 2, beta_lj)

            if pitch > max_spacing:
                pitch, edge_dist = self.plate.get_spacing_adjusted(pitch, edge_dist, max_spacing)
                if edge_dist >= max_edge_dist:
                    edge_dist = max_edge_dist
                    bolts_one_line += 1

            else:
                break

        print("web", pitch, edge_dist, plate_h)
        return pitch, edge_dist, plate_h, bolts_one_line

    def get_bolt_IR(self,bolt_shear_capacity,bolt_tension_capacity,no_bolt, beta_lj = 1.0):
        while True:
            bolt_shear = self.load.shear_force * 1000 / no_bolt  # N
            print("bolt_shear", bolt_shear)
            bolt_tension = self.load.axial_force * 1000 / no_bolt  # N
            print("bolt_tension", bolt_tension)
            # TODO: check available effective width per pair of bolts (b_e)
            bolt_tension_prying = IS800_2007.cl_10_4_7_bolt_prying_force(bolt_tension, self.bolt.min_end_dist_round,
                                        0.7*self.bolt.fu, self.bolt.min_pitch_round, self.plate.thickness_provided,
                                        self.plate.fy, self.bolt.min_end_dist_round, self.bolt.bolt_tensioning)
            print("bolt_tension_prying", bolt_tension_prying)
            comb_bolt_ir = (bolt_shear / (bolt_shear_capacity*beta_lj)) ** 2 + \
                           ((bolt_tension + bolt_tension_prying)/bolt_tension_capacity) ** 2
            print(comb_bolt_ir)
            if comb_bolt_ir > 1:
                no_bolt += 2
            else:
                break
        return bolt_shear, bolt_tension, bolt_tension_prying, no_bolt

    def get_plate_capacity(self, p_th, p_h, pitch, edge, end, n_row, bolt_hole_dia):
        # plate_moment = min_edge_dist * bolt_tension
        Z_p = pitch * p_th **2 /4
        Z_e = pitch * p_th **2 /6
        plate_moment_capacity = IS800_2007.cl_8_2_1_2_design_moment_strength(Z_e, Z_p, self.plate.fy, 'plastic')
        A_vg = p_h* p_th
        plate_shear_yielding_capacity = IS800_2007.cl_8_4_design_shear_strength(A_vg, self.plate.fy)

        A_vg = ((n_row-1)*pitch + end)*p_th
        A_vn = ((n_row-1)*pitch + end - (float(n_row)-0.5) * bolt_hole_dia) *p_th
        A_tg = 2 * edge * p_th
        A_tn = 2 * (edge - 0.5*bolt_hole_dia) * p_th

        plate_block_shear_capacity = IS800_2007.cl_6_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, self.plate.fu, self.plate.fy)
        plate_shear_capacity = min(plate_shear_yielding_capacity, plate_block_shear_capacity)
        return plate_moment_capacity, plate_shear_capacity, plate_block_shear_capacity

    def get_available_welds(self, connecting_members=[]):
        weld_size_max = min(connecting_members)
        weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(connecting_members[0], connecting_members[1])

        available_welds = list([x for x in ALL_WELD_SIZES if (weld_size_min <= x <= weld_size_max)])
        return available_welds,weld_size_min,weld_size_max

    def design_weld(self,available_welds):
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

        # self.get_design_status(self)
        # print("--- %s seconds ---" % (time.time() - self.start_time))

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

    @staticmethod
    def pltthk_customized():
        a = VALUES_PLATETHK_CUSTOMIZED
        return a

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t2 = (KEY_PLATETHK, self.pltthk_customized)
        list1.append(t2)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        return list1

    def fn_conn_suptngsec_lbl(self):

        if self in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        elif self in VALUES_CONN_2:
            return KEY_DISP_PRIBM
        else:
            return ''

    def fn_conn_suptdsec_lbl(self):

        if self in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        elif self in VALUES_CONN_2:
            return KEY_DISP_SECBM
        else:
            return ''

    def fn_conn_suptngsec(self):

        if self in VALUES_CONN_1:
            return VALUES_COLSEC
        elif self in VALUES_CONN_2:
            return VALUES_PRIBM
        else:
            return []

    def fn_conn_suptdsec(self):

        if self in VALUES_CONN_1:
            return VALUES_BEAMSEC
        elif self in VALUES_CONN_2:
            return VALUES_SECBM
        else:
            return []

    def fn_conn_image(self):
        if self == VALUES_CONN[0]:
            return './ResourceFiles/images/fin_cf_bw.png'
        elif self == VALUES_CONN[1]:
            return './ResourceFiles/images/fin_cw_bw.png'
        elif self in VALUES_CONN_2:
            return './ResourceFiles/images/fin_beam_beam.png'
        else:
            return ''

    def input_value_changed(self):

        lst = []

        t1 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_LABEL, self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_COMBOBOX, self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = (KEY_CONN, KEY_SUPTDSEC, TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = (KEY_CONN, KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = (KEY_CONN, KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        return lst

    def to_get_d(my_d):
        print(my_d)

    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair
        print(flag)

        out_list = []

        # TODO: 'Bolt Properties: Start'

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.output[0][1] if flag else '')
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_PC_PROVIDED, TYPE_TEXTBOX, self.output[0][2] if flag else '')
        out_list.append(t3)

        t3_1 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX, self.output[0][0] if flag else '')
        out_list.append(t3_1)

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  self.output[0][7] if flag else '')
        out_list.append(t4)
        #
        # bolt_bearing_capacity_disp = ''
        # if flag is True:
        #     if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
        #         bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
        #         pass
        #     else:
        #         bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, self.output[0][8] if flag else '')
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.output[0][6] if flag else '')
        out_list.append(t6)

        t6_1 = (KEY_OUT_BOLT_TENSION_CAPACITY, KEY_OUT_DISP_BOLT_TENSION_CAPACITY, TYPE_TEXTBOX, self.output[0][9] if flag else '')
        out_list.append(t6_1)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_FORCE, TYPE_TEXTBOX, self.output[0][10] if flag else '')
        out_list.append(t21)

        t21_1 = (KEY_OUT_BOLT_TENSION_FORCE, KEY_OUT_DISP_BOLT_TENSION_FORCE, TYPE_TEXTBOX, self.output[0][11] if flag else '')
        out_list.append(t21_1)

        t21_2 = (KEY_OUT_BOLT_PRYING_FORCE, KEY_OUT_DISP_BOLT_PRYING_FORCE, TYPE_TEXTBOX, self.output[0][17] if flag else '')
        out_list.append(t21_2)

        t23 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing])
        out_list.append(t23)

        # TODO: 'Bolt Properties: End'

        # TODO: Plate properties: Start

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None)
        out_list.append(t13)

        t14 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.output[0][3] if flag else '')
        out_list.append(t14)

        t15 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.output[0][4] if flag else '')
        out_list.append(t15)

        t16 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_WIDTH, TYPE_TEXTBOX, self.output[0][5] if flag else '')
        out_list.append(t16)

        t22 = (KEY_OUT_PLATE_CAPACITIES, KEY_OUT_DISP_PLATE_CAPACITIES, TYPE_OUT_BUTTON, ['Capacity Details', self.capacities])
        out_list.append(t22)

        # TODO: Plate Properties: End

        # TODO: Weld properties: Start

        t24 = (None, DISP_TITLE_WELD, TYPE_TITLE, None)
        out_list.append(t24)

        t25 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX, self.output[0][23] if flag else '')
        out_list.append(t25)

        t26 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX, self.output[0][25] if flag else '')
        out_list.append(t26)

        t27 = (KEY_OUT_WELD_STRESS, KEY_OUT_DISP_WELD_STRESS, TYPE_TEXTBOX, self.output[0][24] if flag else '')
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
# main()


print(time.clock() - start_time, "seconds")