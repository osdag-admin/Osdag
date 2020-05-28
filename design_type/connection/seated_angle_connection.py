"""
Started on 21st April, 2020.

@author: sourabhdas


Module: Seated angle connection

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel structures by Dr. N Subramanian (chapter 5 and 6)
            3) Fundamentals of Structural steel design by M.L Gambhir
            4) AISC Design Examples V14



ASCII diagram


            +-+-------------+-+   +-------------------------+
            | |             | |   |-------------------------|
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |-------------------------|
            | |             | |   +-------------------------+
            | |             | |+-----------+
            | |             | || +---------+
            | |             | || |
            | |         +---|-||-|---+
            | |         +---|-||-|---+
            | |             | || |
            | |         +---|-||-|---+
            | |         +---|-||-|---+
            | |             | ||_|
            | |             | |
            | |             | |
            +-+-------------+-+



"""

from design_type.connection.shear_connection import ShearConnection
from utils.common.component import *
from utils.common.material import *
from utils.common.component import Bolt, Plate, Weld
from Common import *
from utils.common.load import Load
import logging


class SeatedAngleConnection(ShearConnection):

    def __init__(self):

        super(SeatedAngleConnection, self).__init__()
        self.design_status = False

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        """

        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        Tab Title : Text which is displayed as Title of Tab,
        Type of Tab: There are Three types of tab layouts.
            Type_TAB_1: This have "Add", "Clear", "Download xlsx file" "Import xlsx file"
            TYPE_TAB_2: This contains a Text box for side note.
            TYPE_TAB_3: This is plain layout
        function for tab content: All the values like labels, input widgets can be passed as list of tuples,
        which will be displayed in chosen tab layout

        """

        tabs = []

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_supporting_section)
        tabs.append(t1)

        t1 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_supported_section)
        tabs.append(t1)

        t6 = (KEY_DISP_SEATED_ANGLE, TYPE_TAB_1, self.tab_angle_section)
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

        t5 = (KEY_DISP_SEATED_ANGLE, ['Label_1', 'Label_3'],
              ['Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14',
               'Label_15',
               'Label_16', 'Label_17', 'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22'],
              TYPE_TEXTBOX, self.get_Angle_sec_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_SEATED_ANGLE, [KEY_ANGLE_LIST, KEY_CONNECTOR_MATERIAL],
              [KEY_ANGLE_SELECTED, KEY_CONNECTOR_FY, KEY_CONNECTOR_FU, 'Label_1', 'Label_3', 'Label_4', 'Label_5',
               'Label_7',
               'Label_8', 'Label_9',
               'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17',
               'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23'], TYPE_TEXTBOX,
              self.get_new_angle_section_properties)
        change_tab.append(t6)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20'], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20'], TYPE_TEXTBOX, self.get_I_sec_properties)
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
        t2 = (KEY_DISP_SEATED_ANGLE, TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
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
        return KEY_DISP_SEATED_ANGLE

    def input_values(self, existingvalues={}):
        self.module = KEY_DISP_SEATED_ANGLE
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

        # if KEY_CLEATSEC in existingvalues:
        #     existingvalue_key_cleatsec = existingvalues[KEY_CLEATSEC]
        # else:
        #     existingvalue_key_cleatsec = ''

        if KEY_ANGLE_LIST in existingvalues:
            existingvalue_key_seatedangle = existingvalues[KEY_ANGLE_LIST]
        else:
            existingvalue_key_seatedangle = ''

        if KEY_TOPANGLE in existingvalues:
            existingvalue_key_topangle = existingvalues[KEY_TOPANGLE]
        else:
            existingvalue_key_topangle = ''

        t16 = (KEY_MODULE, KEY_DISP_SEATED_ANGLE, TYPE_MODULE, None, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN_1, True, 'No Validator')
        options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, None, './ResourceFiles/images/fin_cf_bw.png', True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, VALUES_COLSEC, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, VALUES_BEAMSEC, True, 'No Validator')
        options_list.append(t5)

        t6 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t6)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None, True, 'Int Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_PC, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t13 = (None,DISP_TITLE_ANGLE, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_ANGLE_LIST, KEY_DISP_SEATEDANGLE, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_seatedangle, VALUES_ANGLESEC, True, 'No Validator')
        options_list.append(t14)

        t15 = (KEY_TOPANGLE, KEY_DISP_TOPANGLE, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_topangle, VALUES_ANGLESEC, True, 'No Validator')
        options_list.append(t15)

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

        if design_dictionary[KEY_CONN] == VALUES_CONN_1[1]:
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
            # QMessageBox.information(window, "Information",
            #                         generate_missing_fields_error_string(missing_fields_list))
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
        # global logger
        red_list = red_list_function()
        if self.supported_section.designation in red_list or self.supporting_section.designation in red_list:
            logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")
            # logger.info(" : You are using a section (in red color) that is not available in latest version of IS 808")

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
        super(SeatedAngleConnection,self).set_input_values(self, design_dictionary)
        self.seated_angle = Angle(designation= design_dictionary[KEY_ANGLE_LIST][0], material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL])
        self.top_angle = Angle(designation= design_dictionary[KEY_ANGLE_LIST][0], material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL])
        self.module = design_dictionary[KEY_MODULE]
        self.seated_list = design_dictionary[KEY_ANGLE_LIST]
        self.topangle_list = design_dictionary[KEY_TOPANGLE]
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.material_grade = design_dictionary[KEY_MATERIAL]
        self.material_grade_connector = design_dictionary[KEY_CONNECTOR_MATERIAL]
        # self.weld = Weld(material_grade=design_dictionary[KEY_MATERIAL], material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O], fabrication=design_dictionary[KEY_DP_WELD_FAB])
        # self.weld = Weld(size=10, length= 100, material_grade=design_dictionary[KEY_MATERIAL])
        # print("input values are set. Doing preliminary member checks")
        self.warn_text(self)
        self.member_capacity(self)

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        if self.supported_section.type == "Rolled":
            length = self.supported_section.depth
        else:
            length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # For Built-up section

        # self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.shear_yielding_capacity = round(IS800_2007.cl_8_4_design_shear_strength(
            length * self.supported_section.web_thickness, self.supported_section.fy) / 1000, 2)
        if self.supported_section.shear_yielding_capacity > self.load.shear_force :
            # print("preliminary member check is satisfactory. Checking available angle thickness")
            self.design_status = True
            self.select_angle_thickness(self)
        else:
            self.design_status = False
            logger.error(" : shear yielding capacity {} is less than applied load, Please select larger sections or decrease loads"
                            .format(self.supported_section.shear_yielding_capacity))
            # print("failed in preliminary member checks. Select larger sections or decrease loads")

    def select_angle_thickness(self):
        self. plate.thickness = []
        self.seated_angle.width = self.supported_section.flange_width

        for designation in self.seated_list:
            # print(self.seated_list)
            # print(designation)
            self.seated = Angle(designation=designation, material_grade=self.material_grade)
            self.check_capacity(self, self.seated)
            self.seated_angle.leg_a_length_min = self.b1 + self.plate.gap

            if self.plate.moment_capacity > self.plate.moment_demand and \
                    self.plate.shear_capacity > self.load.shear_force and \
                    self.seated.leg_a_length > self.seated_angle.leg_a_length_min:
                if self.seated.thickness not in self.plate.thickness:
                    self.plate.thickness.append(self.seated.thickness)
                # print("added", designation, self. plate.thickness)
            else:
                self.seated_list = [x for x in self.seated_list if x != designation]
                # print("popped", designation)

        if self.plate.thickness:
            logger.info("Required Seated Angle thickness available. Getting angle leg size")
            self.get_bolt_details(self)
        else:
            self.design_status = False
            logger.error("Increase Seated Angle thickness")

    def check_capacity(self, seated):
        self.b1 = IS800_2007.cl_8_7_1_3_stiff_bearing_length(self.load.shear_force,
                                                        self.supported_section.web_thickness,
                                                        self.supported_section.flange_thickness,
                                                        self.supported_section.root_radius,
                                                        self.supported_section.fy)
        # Distance from the end of bearing on seated angle horizontal leg to root angle OR A TO B in Fig 5.31 in Prof N. Subramanian's book
        self.b2 = max(self.b1 + self.plate.gap - seated.thickness - seated.root_radius,
                      self.supported_section.flange_thickness + self.supported_section.root_radius)

        if self.b1 <= self.b2:
            self.plate.moment_demand = round(float(self.load.shear_force) * (self.b2 - self.b1 / 2) / 1E3, 3)
        else:
            self.plate.moment_demand = round(float(self.load.shear_force) * (self.b2 / self.b1) * (self.b2 / 2) / 1E3, 3)

        Z_p = self.seated_angle.width * seated.thickness ** 2 / 4
        Z_e = self.seated_angle.width * seated.thickness ** 2 / 6
        self.plate.moment_capacity = round(float(IS800_2007.cl_8_2_1_2_design_moment_strength(Z_e, Z_p, seated.fy, 'plastic'))/ 1E6, 3)

        area = self.seated_angle.width * seated.thickness
        self.plate.shear_capacity = round(float(IS800_2007.cl_8_4_design_shear_strength(area, seated.fy)) / 1E3, 3)

        # return moment_at_root_angle, plate_moment_capacity, self.plate.shear_capacity, b1

    def get_bolt_details(self):
        # print(self.design_status)
        self.output = []
        trial = 0
        [min_bolts_one_line, n] = self.get_seated_width_min_max(self)

        for self.plate.thickness_provided in sorted(self.plate.thickness):
            self.plate.connect_to_database_to_get_fy_fu(self.plate.material, self.plate.thickness_provided)
            # TO GET BOLT BEARING CAPACITY CORRESPONDING TO PLATE THICKNESS AND Fu AND Fy #
            self.get_plate_thk_bolt_bearing(self)
            bolts_required_previous = 2
            bolt_diameter_previous = self.bolt.bolt_diameter[-1]
            self.bolt_dia_possible = []
            count = 0

            for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
                self.bolt.bolt_PC_provided = self.bolt.bolt_grade[-1]

                self.bolt_placement_check(self)
                self.bolt_dia_check(self)
                if self.bolt.design_status is False:
                    # print("Sufficient space is not available for bolt diameter: ", self.bolt.bolt_diameter_provided)
                    continue

                self.get_bolt_capacity(self)

                self.bolt.number = round_up(float(self.load.shear_force * 1000) / self.bolt.bolt_capacity, 1)
                if self.connectivity == VALUES_CONN_1[0]:
                    self.bolt.number = round_up(float(self.bolt.number) / n, 1)

                [bolt_line, bolts_one_line, web_plate_h] = \
                    self.plate.get_web_plate_l_bolts_one_line(self.seated_angle.width_max, self.seated_angle.width_min,
                                                              self.bolt.number, self.bolt.min_edge_dist_round,
                                                              self.bolt.min_gauge_round, min_bolts_one_line)
                self.bolt.bolt_row = bolt_line
                self.bolt.bolt_col = bolts_one_line * n
                if self.connectivity == VALUES_CONN_1[0]:
                    self.seated_angle.width = round_up(web_plate_h * 2 + self.supporting_section.web_thickness + \
                                              self.supporting_section.root_radius * 2, 1)
                else:
                    self.seated_angle.width = web_plate_h
                self.bolt.bolts_required = bolts_one_line*bolt_line*n

                if 2 >= bolt_line >= 1:
                    self.bolt.bolt_force = self.load.shear_force / self.bolt.bolts_required
                    self.bolt_dia_possible.append(self.bolt.bolt_diameter_provided)
                    if self.bolt.bolts_required > bolts_required_previous and count >= 1:
                        self.bolt.bolt_diameter_provided = bolt_diameter_previous
                        self.bolt.bolts_required = bolts_required_previous
                        self.bolt.bolt_row = bolt_row_prev
                        self.bolt.bolt_col = bolt_col_prev
                        # self.bolt.bolt_force = bolt_force_previous
                        break
                    bolts_required_previous = self.bolt.bolts_required
                    bolt_diameter_previous = self.bolt.bolt_diameter_provided
                    # TODO: set bolt row and column prev value
                    bolt_row_prev = self.bolt.bolt_row
                    bolt_col_prev = self.bolt.bolt_col
                    # bolt_force_previous = self.bolt.bolt_force
                    count += 1
                else:
                    self.bolt.bolt_force = self.load.shear_force / self.bolt.number
                    continue
            if self.bolt_dia_possible:
                # print("bolt diameter: ", self.bolt_dia_possible)
                # print("provided bolt diameter: ", self.bolt.bolt_diameter_provided)
                self.check_leg_size(self, bolt_line)
                print(self.plate.design_status)

                if self.plate.design_status is True:
                    trial += 1

                    ##### O U T P U T   D I C T I O N A R Y   F O R M A T #####
                    row = [int(self.bolt.bolt_diameter_provided),           # 0-Bolt Diameter
                           self.bolt.bolt_PC_provided,                      # 1-Bolt Grade
                           self.seated_angle.designation,                   # 2-Seated Angle designation
                           int(self.plate.thickness_provided),              # 3-Seated Angle Thickness
                           self.seated_angle.leg_a_length,                  # 4-Seated angle leg size
                           self.bolt.bolt_row,                              # 5-Bolt rows on seated angle vertical leg
                           self.bolt.bolt_col,                              # 6-Bolt columns on seat angle vertical leg
                           self.seated_angle.width,                         # 7-Length of the seated angle
                           self.bolt.bolts_required,                        # 8-Total no of bolts
                           self.bolt.min_gauge_round,                       # 9-Gauge distance
                           self.bolt.min_edge_dist_round,                   # 10-Edge Distance
                           self.bolt.min_pitch_round,                       # 11-Pitch
                           self.bolt.min_end_dist_round,                    # 12-End Distance
                           self.bolt.bolt_force,                            # 13-Bolt Force

                           'INSERT_HERE',  # XX- EMPTY
                           trial]
                    self.output.append(row)
                    print("********* Trial {} ends here *************".format(trial))
                else:
                    continue
            else:
                continue

        if self.bolt_dia_possible and self.plate.design_status is True:
            print("No of effective trials: ", trial)
            print(self.output)
            self.select_optimum(self)

            self.top_angle_section(self)
            logger.info("=== End Of Design ===")
        else:
            self.design_status = False
            # logger.error("Decrease bolt diameter")
            logger.error("Sufficient space not available to arrange bolts, " +
                         "either decrease bolt diameter or increase angle leg size.")

    def select_optimum(self):
        """This function sorts the list of available options and selects the combination with least leg size"""
        self.output.sort(key=lambda x: (x[4], x[3], x[5]))
        self.bolt.bolt_diameter_provided = self.output[0][0]
        self.bolt.bolt_PC_provided = self.output[0][1]
        self.seated_angle.designation = self.output[0][2]
        self.plate.thickness_provided = self.output[0][3]
        self.seated_angle.leg_a_length = self.output[0][4]
        self.bolt.bolt_row = self.output[0][5]
        self.bolt.bolt_col = self.output[0][6]
        self.seated_angle.width = self.output[0][7]
        self.bolt.bolts_required = self.output[0][8]
        self.bolt.min_gauge_round = self.output[0][9]
        self.bolt.min_edge_dist_round = self.output[0][10]
        self.bolt.min_pitch_round = self.output[0][11]
        self.bolt.min_end_dist_round = self.output[0][12]
        self.bolt.bolt_force = self.output[0][13]

        self.set_final_values(self)

    def set_final_values(self):
        # self.seated_angle = Angle(designation=self.seated_angle.designation, material_grade=self.material_grade)
        self.seated = Angle(designation=self.seated_angle.designation, material_grade=self.material_grade)
        self.seated_angle_bolt_details(self)
        if self.connectivity == VALUES_CONN_1[0]:
            self.bolt.gauge = self.bolt.min_gauge_round
            self.bolt.sa_length = self.seated_angle.width
        else:
            self.bolt.gauge = self.bolt.seated_angle_gauge_column
        self.plate.thickness_provided = self.seated.thickness
        self.get_plate_thk_bolt_bearing(self)
        self.bolt.bolt_force = self.load.shear_force / self.bolt.bolts_required
        self.bolt_PC(self)
        # self.get_bolt_capacity(self)
        # self.get_bolt_capacity_updated(self)
        self.check_capacity(self, self.seated)

    def bolt_PC(self):
        bolt_PC_previous = self.bolt.bolt_grade[-1]
        for self.bolt.bolt_PC_provided in reversed(self.bolt.bolt_grade):
            count = 1
            self.bolt_placement_check(self)
            self.get_bolt_capacity_updated(self)

            if self.bolt.bolt_capacity < self.bolt.bolt_force * 1000 and count >= 1:
                self.bolt.bolt_PC_provided = bolt_PC_previous
                break
            bolt_PC_previous = self.bolt.bolt_PC_provided
            count += 1

    def get_seated_width_min_max(self):
        """This function sets the max and min limits of seated angle length"""
        if self.connectivity == VALUES_CONN_1[0]:
            if self.supporting_section.flange_width > self.supported_section.flange_width:
                self.seated_angle.width_min = (self.supported_section.flange_width -
                                    self.supporting_section.web_thickness -2 * self.supporting_section.root_radius) / 2
                self.seated_angle.width_max = (self.supporting_section.flange_width -
                                    self.supporting_section.web_thickness - 2 * self.supporting_section.root_radius) / 2
            else:
                self.seated_angle.width_min = (self.supporting_section.flange_width -
                                    self.supporting_section.web_thickness - 2 * self.supporting_section.root_radius) / 2
                self.seated_angle.width_max = self.seated_angle.width_min + 20
                # self.seated_angle.width_min = (self.supporting_section.flange_width -
                #                   self.supporting_section.web_thickness - 2 * self.supporting_section.root_radius) / 2
                # self.seated_angle.width_max = (self.supported_section.flange_width -
                #                   self.supporting_section.web_thickness - 2 * self.supporting_section.root_radius) / 2
            min_bolts_one_line = 1
            n = 2
        else:
            self.seated_angle.width_min = self.supported_section.flange_width
            self.seated_angle.width_max = (self.supporting_section.depth -
                                2 * self.supporting_section.flange_thickness - 2 * self.supporting_section.root_radius)
            min_bolts_one_line = 2
            n = 1

        return min_bolts_one_line, n

    def get_plate_thk_bolt_bearing(self):
        """This function sets the thickness and material propert combination of connected elements"""
        # TO GET BOLT BEARING CAPACITY CORRESPONDING TO PLATE THICKNESS AND Fu AND Fy #
        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.seated.fu, self.seated.fy))
        if self.connectivity == VALUES_CONN_1[1]:
            self.bolt_conn_plates_t_fu_fy.append(
                (self.supporting_section.flange_thickness, self.supporting_section.fu, self.supporting_section.fy))
        else:
            self.bolt_conn_plates_t_fu_fy.append(
                (self.supporting_section.web_thickness, self.supporting_section.fu, self.supporting_section.fy))

    def bolt_placement_check(self):
        """This function calculates minimum bolt spacing limits"""
        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)
        self.bolt.min_end_dist_round = round_up(IS800_2007.cl_10_2_4_2_min_edge_end_dist(
            self.bolt.bolt_diameter_provided, self.bolt.bolt_hole_type, 'machine_flame_cut'), 5)

    def get_bolt_capacity(self):
        """This function calculates minimum bolt capacities"""
        self.bolt_bearing_end_dist = self.bolt.min_end_dist_round
        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt.bolt_PC_provided,
                                          conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy, n_planes=1,
                                          seatedangle_e= self.bolt_bearing_end_dist)
        if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
            self.bolt.bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
        else:
            self.bolt.bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        self.bolt.bolt_shear_capacity_disp = round(self.bolt.bolt_shear_capacity/1000, 1)
        self.bolt.bolt_capacity_disp = round(self.bolt.bolt_capacity/1000, 1)

    def get_bolt_capacity_updated(self):
        """This function updates bolt capacities"""
        self.bolt_bearing_end_dist = self.bolt.min_end_dist_round + self.seated.thickness + self.seated.root_radius
        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                          bolt_grade_provided=self.bolt.bolt_PC_provided,
                                          conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy, n_planes=1,
                                          seatedangle_e=self.bolt_bearing_end_dist)
        if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
            self.bolt.bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
        else:
            self.bolt.bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        self.bolt.bolt_shear_capacity_disp = round(self.bolt.bolt_shear_capacity / 1000, 1)
        self.bolt.bolt_capacity_disp = round(self.bolt.bolt_capacity / 1000, 1)


    def bolt_dia_check(self):
        """This function checks if the selected bolt diameter can be placed within the available flange width"""
        self.beam_space_min = (self.supported_section.flange_width -
                          self.supported_section.web_thickness - 2 * self.supported_section.root_radius) / 2
        self.col_space_min = (self.supporting_section.flange_width -
                          self.supporting_section.web_thickness - 2 * self.supporting_section.root_radius) / 2
        if self.connectivity == VALUES_CONN_1[0]:
            if self.beam_space_min >= 2*self.bolt.min_end_dist_round and self.col_space_min >= 2*self.bolt.min_end_dist_round:
                self.bolt.design_status = True
            else:
                self.bolt.design_status = False
        else:
            if self.beam_space_min >= 2 * self.bolt.min_end_dist_round:
                self.bolt.design_status = True
            else:
                self.bolt.design_status = False

    def check_leg_size(self, bolt_line):
        min_leg_length = (2 * self.bolt.min_end_dist_round + (bolt_line - 1) * self.bolt.min_pitch_round)
        min_leg_b_length = (self.bolt.min_end_dist_round + self.plate.gap + self.bolt.min_edge_dist_round)
        # min_leg_length = max(2*self.bolt.min_end_dist_round + (bolts_one_line - 1) * self.bolt.min_pitch_round, self.seated_angle.leg_a_length_min)
        print("min_leg_length", min_leg_length)
        print(self.plate.gap)
        print("min_leg_b_length", min_leg_b_length)
        self.seated_list_same_thickness = self.seated_angle.get_available_seated_list(self.seated_list,
            max_leg_length = math.inf, min_leg_length = min_leg_length, position = "inner", t_min = self.plate.thickness_provided)

        if self.seated_list_same_thickness is []:
            self.plate.design_status = False
        else:
            for self.seated_angle.designation in self.seated_list_same_thickness:
                [leg_a_length, leg_b_length, t, r_r] = get_leg_lengths(self.seated_angle.designation)
                print(leg_a_length, leg_b_length)
                if (leg_a_length - t - r_r) >= min_leg_length and leg_b_length >= min_leg_b_length:
                    self.seated_angle.leg_a_length = leg_a_length
                    self.plate.design_status = True
                    print(leg_a_length, leg_b_length)
                    break
                else:
                    self.plate.design_status = False

    # def check_leg_b_size(self):
    #     min_leg_b_length = (self.bolt.min_end_dist_round + self.plate.gap + self.bolt.min_edge_dist_round)
    #     print("min_leg_b_length", min_leg_b_length)
    #     self.seated_list_leg_b = self.seated_list_same_thickness.get_available_seated_list(self.seated_list,
    #         max_leg_length=math.inf, min_leg_length=min_leg_b_length, position="outer", t_min=self.plate.thickness_provided)
    #     for self.seated_angle.designation in self.seated_list_leg_b:
    #         [leg_a_length, leg_b_length, t, r_r] = get_leg_lengths(self.seated_angle.designation)
    #         if leg_a_length >= min_leg_b_length:
    #             self.seated_angle.leg_a_length = leg_a_length
    #             self.plate.design_status = True
    #             break
    #         else:
    #             self.plate.design_status = False
    #
    #     if self.seated_list_leg_b is []:
    #         self.plate.design_status = False
    #     else:
    #         self.plate.design_status = True

    def top_angle_section(self):
        """Identify appropriate top angle size based on beam depth.
        Note:
            Assumptions:
                Calculating top angle dimensions based on thumb rules:
                    top_angle_side = beam_depth/4
                    top_angle_thickness = top_angle_side/10 with a minimum of 6mm
                Select the nearest available equal angle as the top angle.
                Equal angles satisfying both these thumb rules are selected for this function from steel tables
        """
        # minimum length of leg of top angle is twice edge distance + angle thickness + root_radius.
        # as the side length is rounded up in the next step, ignoring angle thickness while calculating
        # minimum length of side

        for top in self.topangle_list:
            # print(self.topangle_list)
            # print(top)
            topclip = Angle(designation=top, material_grade=self.material_grade)
            top_angle_side_minimum = max(2 * self.bolt.min_end_dist_round + topclip.root_radius + topclip.thickness,
                                         self.bolt.min_end_dist_round + self.plate.gap + self.bolt.min_edge_dist_round)
            top_angle_side = max(float(self.supported_section.depth) / 4, top_angle_side_minimum, 50)
            top_angle_thickness_min = max(round_up(float(topclip.leg_a_length) / 10, 1), 6)
            # print(topclip.thickness, top_angle_thickness_min)
            if topclip.leg_a_length >= top_angle_side and topclip.thickness >= top_angle_thickness_min:
                self.top_angle = Angle(designation=top, material_grade=self.material_grade)
                self.top_angle.design_status = True
                break
            else:
                self.top_angle.design_status = False

        if self.top_angle.design_status is False:
            for top in self.topangle_list:
                # print(self.topangle_list)
                # print(top)
                topclip = Angle(designation=top, material_grade=self.material_grade)
                top_angle_side_minimum = max(2 * self.bolt.min_end_dist_round + topclip.root_radius + topclip.thickness,
                                             self.bolt.min_end_dist_round + self.plate.gap + self.bolt.min_edge_dist_round)
                top_angle_side = max(top_angle_side_minimum, 50)
                top_angle_thickness_min = max(round_up(float(topclip.leg_a_length) / 10, 1), 6)
                if topclip.leg_a_length >= top_angle_side and topclip.thickness >= top_angle_thickness_min:
                    self.top_angle = Angle(designation=top, material_grade=self.material_grade)
                    self.top_angle.design_status = True
                    break
                else:
                    self.top_angle.design_status = False

        if self.top_angle.design_status is False:
            for top in self.topangle_list:
                # print(self.topangle_list)
                # print(top)
                topclip = Angle(designation=top, material_grade=self.material_grade)
                top_angle_side_minimum = max(2 * self.bolt.min_end_dist_round + topclip.root_radius + topclip.thickness,
                                             self.bolt.min_end_dist_round + self.plate.gap + self.bolt.min_edge_dist_round)
                top_angle_side = max(top_angle_side_minimum, 50)
                top_angle_thickness_min = 6
                if topclip.leg_a_length >= top_angle_side and topclip.thickness >= top_angle_thickness_min:
                    self.top_angle = Angle(designation=top, material_grade=self.material_grade)
                    self.top_angle.design_status = True
                    break
                else:
                    self.top_angle.design_status = False

        top_angle_thickness_min = max(round_up(float(topclip.leg_a_length) / 10, 1), 6)
        if self.top_angle.design_status is True:
            self.top_angle_bolt_details(self)
            # print("provided top angle", self.top_angle.designation)
            logger.info(": Based on thumb rules, a minimum top angle leg size of {} mm and a thickness of {} mm "
                        "is required to provide stability to {} ".format(top_angle_side, top_angle_thickness_min,
                                                                         self.supported_section.designation))
            self.design_status = True
        else:
            logger.error(": Sufficient leg length is not available for Top Angle. ")
            self.design_status = False

    def top_angle_bolt_details(self):
        if self.connectivity == VALUES_CONN_1[0]:
            self.top_angle.width = max(min(self.supported_section.flange_width + 20, self.supporting_section.flange_width + 20),

                                       round_up((self.supporting_section.web_thickness+self.supporting_section.root_radius * 2 +
                                       self.bolt.min_end_dist_round * 2 + self.bolt.min_edge_dist_round * 2), 1),

                                       round_up((self.supported_section.web_thickness + self.supported_section.root_radius * 2 +
                                       self.bolt.min_end_dist_round * 2 + self.bolt.min_edge_dist_round * 2), 1) )

            if self.top_angle.width < self.supporting_section.flange_width:
                self.bolt.top_angle_gauge_column = round_up((self.top_angle.width -
                            self.supporting_section.root_radius * 2 - self.supporting_section.web_thickness) / 2 +
                            self.supporting_section.root_radius * 2 + self.supporting_section.web_thickness, 1)
                self.bolt.top_angle_edge_column = round((self.top_angle.width - self.bolt.top_angle_gauge_column) / 2, 1)
                # self.top_angle.width = self.bolt.top_angle_gauge_column + 2 * self.bolt.top_angle_edge_column
            else:
                self.bolt.top_angle_gauge_column = round_up((self.supporting_section.flange_width -
                            self.supporting_section.root_radius * 2 - self.supporting_section.web_thickness) / 2 +
                            self.supporting_section.root_radius * 2 + self.supporting_section.web_thickness, 1)
                self.bolt.top_angle_edge_column = round((self.top_angle.width - self.bolt.top_angle_gauge_column) / 2, 1)
                # self.top_angle.width = self.bolt.top_angle_gauge_column + 2 * self.bolt.top_angle_edge_column

            if self.top_angle.width < self.supported_section.flange_width:
                # self.bolt.top_angle_gauge_beam = round_up((self.top_angle.width - self.bolt.min_edge_dist_round * 2), 1)
                self.bolt.top_angle_gauge_beam = round_up((self.top_angle.width -
                            self.supported_section.root_radius * 2 - self.supported_section.web_thickness) / 2 +
                            self.supported_section.root_radius * 2 + self.supported_section.web_thickness, 1)
                self.bolt.top_angle_edge_beam = round((self.top_angle.width - self.bolt.top_angle_gauge_beam) / 2, 1)

            else:
                self.bolt.top_angle_gauge_beam = round_up((self.supported_section.flange_width -
                            self.supported_section.root_radius * 2 - self.supported_section.web_thickness) / 2 +
                            self.supported_section.root_radius * 2 + self.supported_section.web_thickness, 1)
                self.bolt.top_angle_edge_beam = round((self.top_angle.width - self.bolt.top_angle_gauge_beam) / 2, 1)

        else:
            self.top_angle.width = max(round_up(self.supported_section.flange_width + 20, 1),

                                       round_up((self.supported_section.web_thickness + self.supported_section.root_radius * 2 +
                                                self.bolt.min_end_dist_round * 2 + self.bolt.min_edge_dist_round * 2), 1) )

            self.bolt.top_angle_gauge_beam = round_up((self.supported_section.flange_width -
                            self.supported_section.root_radius * 2 - self.supported_section.web_thickness) / 2 +
                            self.supported_section.root_radius * 2 + self.supported_section.web_thickness, 1)
            self.bolt.top_angle_edge_beam = round((self.top_angle.width - self.bolt.top_angle_gauge_beam) / 2, 1)
            self.bolt.top_angle_gauge_column = self.bolt.top_angle_gauge_beam
            self.bolt.top_angle_edge_column = round((self.top_angle.width - self.bolt.top_angle_gauge_column) / 2, 1)

        self.bolt.top_angle_end = round_up(min((self.top_angle.leg_a_length - self.top_angle.thickness - self.top_angle.root_radius) / 2,
                                           self.top_angle.leg_a_length- self.plate.gap- self.bolt.min_edge_dist_round), 1)

    def seated_angle_bolt_details(self):
        if self.connectivity == VALUES_CONN_1[0]:
            # self.seated_angle.width = max(min(self.supported_section.flange_width, self.supporting_section.flange_width),
            #
            #                            round_up((self.supporting_section.web_thickness+self.supporting_section.root_radius * 2 +
            #                            self.bolt.min_end_dist_round * 2 + self.bolt.min_edge_dist_round * 2), 1),
            #
            #                            round_up((self.supported_section.web_thickness + self.supported_section.root_radius * 2 +
            #                            self.bolt.min_end_dist_round * 2 + self.bolt.min_edge_dist_round * 2), 1) )
            # TODO: Recalculate bolt row and column to minimize seated angle width
            self.recalculate_bolt_row_col(self)
            if self.seated_angle.width < self.supporting_section.flange_width:
                # print("seated angle width: ", self.seated_angle.width)
                self.bolt.seated_angle_gauge_column = round_up((self.seated_angle.width - self.bolt.min_edge_dist_round * 2 -
                                                                (self.bolt.bolt_col - 2) * self.bolt.min_gauge_round), 1)

            else:
                self.bolt.seated_angle_gauge_column = round_up((self.supporting_section.flange_width -
                                                                self.bolt.min_end_dist_round * 2 -
                                                                (self.bolt.bolt_col - 2) * self.bolt.min_gauge_round), 1)

            self.bolt.seated_angle_gauge_beam = round_up((self.supported_section.flange_width -
                                    self.supported_section.root_radius * 2 - self.supported_section.web_thickness)/2 +
                                    self.supported_section.root_radius * 2 + self.supported_section.web_thickness, 1)
            self.bolt.seated_angle_edge_beam = round((self.seated_angle.width - self.bolt.seated_angle_gauge_beam) / 2, 1)
            self.bolt.seated_angle_end_column = round_up((self.seated.leg_a_length - self.seated.thickness -
                                                          self.seated.root_radius - self.bolt.min_end_dist_round -
                                                          self.bolt.min_pitch_round * (self.bolt.bolt_row - 1)), 1)
            self.bolt.seated_angle_edge_column = round((self.seated_angle.width - self.bolt.seated_angle_gauge_column -
                                                          (self.bolt.bolt_col - 2) * self.bolt.min_gauge_round) / 2, 1)

        else:
            self.seated_angle.width = max(self.supported_section.flange_width + 20,

                   round_up((self.supported_section.web_thickness + self.supported_section.root_radius * 2 +
                            self.bolt.min_end_dist_round * 2 + (self.bolt.bolt_col - 1) * self.bolt.min_gauge_round), 1) )

            self.bolt.seated_angle_gauge_beam = round_up((self.supported_section.flange_width -
                                    self.supported_section.root_radius * 2 + self.supported_section.web_thickness)/2 +
                                    self.supported_section.root_radius * 2 + self.supported_section.web_thickness, 1)
            self.bolt.seated_angle_edge_beam = round((self.seated_angle.width - self.bolt.seated_angle_gauge_beam) / 2, 1)
            self.bolt.seated_angle_gauge_column = round_up((self.seated_angle.width - self.bolt.min_edge_dist_round * 2)/
                                                            (self.bolt.bolt_col - 1), 1)
            self.bolt.seated_angle_end_column = round_up((self.seated.leg_a_length - self.seated.thickness -
                                                          self.seated.root_radius - self.bolt.min_end_dist_round -
                                                          self.bolt.min_pitch_round * (self.bolt.bolt_row - 1)), 1)
            self.bolt.seated_angle_edge_column = round((self.seated_angle.width - (self.bolt.bolt_col - 1) *
                                                           self.bolt.seated_angle_gauge_column) / 2, 1)
        # self.bolt.seated_angle_end_beam = round_up((self.seated.leg_a_length - self.seated.thickness - self.seated.root_radius) / 2, 1)
        self.bolt.seated_angle_end_beam = round_up(min((self.seated.leg_a_length - self.seated.thickness - self.seated.root_radius) / 2,
                                           self.seated.leg_a_length- self.plate.gap- self.bolt.min_edge_dist_round), 1)

    def recalculate_bolt_row_col(self):
        """This Function recalculates bolt row and columns to reduce seated angle width"""
        if self.bolt.bolt_col/2 >= 2 and self.bolt.bolt_row == 1 and self.seated_angle.width > self.supported_section.flange_width:
            if (self.seated.leg_a_length - self.seated.thickness - self.seated.root_radius -
                                                    2 * self.bolt.min_end_dist_round) / self.bolt.min_pitch_round >= 1:
                self.bolt.bolt_col = 2 * round_up(self.bolt.bolt_col/4, 1)
                self.bolt.bolt_row = self.bolt.bolt_row * 2
                self.bolt.bolts_required = self.bolt.bolt_col * self.bolt.bolt_row
                self.seated_angle.width = max(round_up(self.supported_section.flange_width + 20, 1),
                            round_up((self.supporting_section.web_thickness + self.supporting_section.root_radius * 2 +
                                self.bolt.min_end_dist_round * 2 + (self.bolt.bolt_col - 2) * self.bolt.min_gauge_round
                                + self.bolt.min_edge_dist_round * 2), 1))
        else:
            self.seated_angle.width = max(round_up(self.supported_section.flange_width + 20, 1), self.seated_angle.width)

    @staticmethod
    def seated_angle_customized():
        sa = VALUES_CLEAT_CUSTOMIZED
        return sa

    @staticmethod
    def top_angle_customized():
        ta = VALUES_CLEAT_CUSTOMIZED
        return ta

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
        t2 = (KEY_ANGLE_LIST, self.seated_angle_customized)
        list1.append(t2)
        t3 = (KEY_TOPANGLE, self.top_angle_customized)
        list1.append(t3)
        t4 = (KEY_D, self.diam_bolt_customized)
        list1.append(t4)
        return list1

    def fn_conn_suptngsec_lbl(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        # elif self in VALUES_CONN_2:
        #     return KEY_DISP_PRIBM
        else:
            return ''

    def fn_conn_suptdsec_lbl(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        # elif self in VALUES_CONN_2:
        #     return KEY_DISP_SECBM
        else:
            return ''

    def fn_conn_suptngsec(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return VALUES_COLSEC
        # elif self in VALUES_CONN_2:
        #     return VALUES_PRIBM
        else:
            return []

    def fn_conn_suptdsec(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return VALUES_BEAMSEC
        # elif self in VALUES_CONN_2:
        #     return VALUES_SECBM
        else:
            return []

    def fn_conn_image(self):

        conn = self[0]
        if conn == VALUES_CONN[0]:
            return './ResourceFiles/images/fin_cf_bw.png'
        elif conn == VALUES_CONN[1]:
            return './ResourceFiles/images/fin_cw_bw.png'
        # elif self in VALUES_CONN_2:
        #     return './ResourceFiles/images/fin_beam_beam.png'
        else:
            return ''

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_CONN], KEY_SUPTNGSEC, TYPE_LABEL, self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = ([KEY_CONN], KEY_SUPTNGSEC, TYPE_COMBOBOX,self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = ([KEY_CONN], KEY_SUPTDSEC, TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = ([KEY_CONN], KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = ([KEY_CONN], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        return lst

    def output_values(self, flag):
        """
        Function to return a list of tuples to be displayed as the UI.(Output Dock)
        """

        # @author: Umair
        # print(flag)

        out_list = []
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """      Bolt Properties: Start        """

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_diameter_provided if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_PC_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_PC_provided if flag else '', True)
        out_list.append(t3)

        t3_1 = (KEY_OUT_TOT_NO_BOLTS, KEY_OUT_DISP_TOT_NO_BOLTS, TYPE_TEXTBOX, self.bolt.bolts_required if flag else '', True)
        out_list.append(t3_1)

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX, self.bolt.bolt_shear_capacity_disp if flag else '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, self.bolt.bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.bolt.bolt_capacity_disp if flag else '', True)
        out_list.append(t6)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_FORCE, TYPE_TEXTBOX, round(self.bolt.bolt_force, 2) if flag else '', True)
        out_list.append(t21)

        """      Bolt Properties: End        """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """     Seated Angle Properties: Start     """

        t13 = (None, KEY_DISP_SEATED_ANGLE, TYPE_TITLE, None, True)
        out_list.append(t13)

        t13_1 = (KEY_OUT_SEATED_ANGLE_DESIGNATION, KEY_OUT_DISP_ANGLE_DESIGNATION, TYPE_TEXTBOX, self.seated_angle.designation if flag else '', True)
        out_list.append(t13_1)
        #
        # t14 = (KEY_OUT_SEATED_ANGLE_THICKNESS, KEY_OUT_DISP_SEATED_ANGLE_THICKNESS, TYPE_TEXTBOX, self.plate.thickness_provided if flag else '', True)
        # out_list.append(t14)
        #
        # t15 = (KEY_OUT_SEATED_ANGLE_LEGLENGTH, KEY_OUT_DISP_SEATED_ANGLE_LEGLENGTH, TYPE_TEXTBOX, self.seated_angle.leg_a_length if flag else '', True)
        # out_list.append(t15)

        t16 = (KEY_OUT_SEATED_ANGLE_WIDTH, KEY_OUT_DISP_ANGLE_WIDTH, TYPE_TEXTBOX, self.seated_angle.width if flag else '', True)
        out_list.append(t16)

        t22 = (KEY_OUT_PLATE_CAPACITIES, KEY_OUT_DISP_PLATE_CAPACITIES, TYPE_OUT_BUTTON, ['Capacity Details', self.capacities], True)
        out_list.append(t22)

        t22_1 = (KEY_OUT_SEATED_ANGLE_BOLT_COL, KEY_OUT_DISP_SEATED_ANGLE_BOLT_COL, TYPE_OUT_BUTTON, ['on Column', self.seated_spacing_col], True)
        out_list.append(t22_1)

        t22_2 = (KEY_OUT_SEATED_ANGLE_BOLT_BEAM, KEY_OUT_DISP_SEATED_ANGLE_BOLT_BEAM, TYPE_OUT_BUTTON, ['on Beam', self.seated_spacing_beam], True)
        out_list.append(t22_2)

        """     Seated Angle Properties: End     """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        """     Top Angle Properties: Start     """

        t24 = (None, KEY_DISP_TOP_ANGLE, TYPE_TITLE, None, True)
        out_list.append(t24)

        t25 = (KEY_OUT_TOP_ANGLE_DESIGNATION, KEY_OUT_DISP_ANGLE_DESIGNATION, TYPE_TEXTBOX, self.top_angle.designation if flag else '', True)
        out_list.append(t25)

        t25_1 = (KEY_OUT_TOP_ANGLE_WIDTH, KEY_OUT_DISP_ANGLE_WIDTH, TYPE_TEXTBOX, self.top_angle.width if flag else '', True)
        out_list.append(t25_1)

        t26 = (KEY_OUT_TOP_ANGLE_BOLT_COL, KEY_OUT_DISP_TOP_ANGLE_BOLT_COL, TYPE_OUT_BUTTON, ['on Column', self.top_spacing_col], True)
        out_list.append(t26)

        t27 = (KEY_OUT_TOP_ANGLE_BOLT_BEAM, KEY_OUT_DISP_TOP_ANGLE_BOLT_BEAM, TYPE_OUT_BUTTON, ['on Beam', self.top_spacing_beam], True)
        out_list.append(t27)

        """     Top Angle Properties: End     """
        """"""""""""""""""""""""""""""""""""""""""""""""""""""

        return out_list

    def top_spacing_col(self, flag):

        top_spacing_col = []

        t9 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX, 1 if flag else '')
        top_spacing_col.append(t9)

        t9_1 = (KEY_OUT_COL_PROVIDED, KEY_OUT_DISP_COL_PROVIDED, TYPE_TEXTBOX, 2 if flag else '')
        top_spacing_col.append(t9_1)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.bolt.top_angle_end if flag else '')
        top_spacing_col.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.bolt.top_angle_gauge_column if flag else '')
        top_spacing_col.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.bolt.top_angle_edge_column if flag else '')
        top_spacing_col.append(t12)

        return top_spacing_col

    def top_spacing_beam(self, flag):

        top_spacing_beam = []

        t9 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX, 1 if flag else '')
        top_spacing_beam.append(t9)

        t9_1 = (KEY_OUT_COL_PROVIDED, KEY_OUT_DISP_COL_PROVIDED, TYPE_TEXTBOX, 2 if flag else '')
        top_spacing_beam.append(t9_1)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.bolt.top_angle_end if flag else '')
        top_spacing_beam.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.bolt.top_angle_gauge_beam if flag else '')
        top_spacing_beam.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.bolt.top_angle_edge_beam if flag else '')
        top_spacing_beam.append(t12)

        return top_spacing_beam

    def seated_spacing_col(self, flag):

        seated_spacing_col = []

        t9 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_row if flag else '')
        seated_spacing_col.append(t9)

        t9_1 = (KEY_OUT_COL_PROVIDED, KEY_OUT_DISP_COL_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_col if flag else '')
        seated_spacing_col.append(t9_1)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.bolt.seated_angle_end_column if flag else '')
        seated_spacing_col.append(t10)

        if self.bolt.bolt_row > 1:
            t10_1 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.bolt.min_pitch_round if flag else '')
            seated_spacing_col.append(t10_1)

        if self.bolt.bolt_col > 2 and self.connectivity == VALUES_CONN_1[0]:
            t11 = (KEY_OUT_GAUGE_CENTRAL, KEY_OUT_DISP_GAUGE_CENTRAL, TYPE_TEXTBOX, self.bolt.seated_angle_gauge_column if flag else '')
            seated_spacing_col.append(t11)

            t11_1 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.bolt.min_gauge_round if flag else '')
            seated_spacing_col.append(t11_1)
        else:
            t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.bolt.seated_angle_gauge_column if flag else '')
            seated_spacing_col.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.bolt.seated_angle_edge_column if flag else '')
        seated_spacing_col.append(t12)

        return seated_spacing_col

    def seated_spacing_beam(self, flag):

        seated_spacing_beam = []

        t9 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX, 1 if flag else '')
        seated_spacing_beam.append(t9)

        t9_1 = (KEY_OUT_COL_PROVIDED, KEY_OUT_DISP_COL_PROVIDED, TYPE_TEXTBOX, 2 if flag else '')
        seated_spacing_beam.append(t9_1)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.bolt.seated_angle_end_beam if flag else '')
        seated_spacing_beam.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.bolt.seated_angle_gauge_beam if flag else '')
        seated_spacing_beam.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.bolt.seated_angle_edge_beam if flag else '')
        seated_spacing_beam.append(t12)

        return seated_spacing_beam

    def capacities(self, flag):

        capacities = []

        t18 = (KEY_OUT_PLATE_SHEAR_DEMAND, KEY_OUT_DISP_PLATE_SHEAR_DEMAND, TYPE_TEXTBOX, self.load.shear_force if flag else '')
        capacities.append(t18)

        t17 = (KEY_OUT_PLATE_SHEAR, KEY_OUT_DISP_PLATE_SHEAR, TYPE_TEXTBOX, self.plate.shear_capacity if flag else '')
        capacities.append(t17)

        t19 = (KEY_OUT_PLATE_MOM_DEMAND, KEY_OUT_DISP_PLATE_MOM_DEMAND, TYPE_TEXTBOX, self.plate.moment_demand if flag else '')
        capacities.append(t19)

        t20 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX, self.plate.moment_capacity if flag else '')
        capacities.append(t20)

        return capacities

    # def to_get_d(my_d):
    #     print(my_d)

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('Seated Angle', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Seated Angle':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("SeatAngle", bgcolor)