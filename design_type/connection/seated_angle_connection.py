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
        # self.seated_angle = Angle(designation=seated_angle_section, material=self.material)
        # self.top_angle = Angle(designation=top_angle_section, material=self.material)

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

        if KEY_CLEATSEC in existingvalues:
            existingvalue_key_cleatsec = existingvalues[KEY_CLEATSEC]
        else:
            existingvalue_key_cleatsec = ''

        if KEY_SEATEDANGLE in existingvalues:
            existingvalue_key_seatedangle = existingvalues[KEY_SEATEDANGLE]
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

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, None, None, True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, VALUES_COLSEC, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, VALUES_BEAMSEC, True, 'No Validator')
        options_list.append(t5)

        t6 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t6)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None, True, 'No Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t13 = (None,DISP_TITLE_ANGLE, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_SEATEDANGLE, KEY_DISP_SEATEDANGLE, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_seatedangle, VALUES_ANGLESEC, True, 'No Validator')
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
            # QMessageBox.information(window, "Information",
            #                         generate_missing_fields_error_string(missing_fields_list))
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

    def set_input_values(self, design_dictionary):
        super(SeatedAngleConnection,self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.seated_list = design_dictionary[KEY_SEATEDANGLE]
        self.topangle_list = design_dictionary[KEY_TOPANGLE]
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_MATERIAL], gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.material_grade = design_dictionary[KEY_MATERIAL]
        # self.weld = Weld(material_grade=design_dictionary[KEY_MATERIAL], material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O], fabrication=design_dictionary[KEY_DP_WELD_FAB])
        # self.weld = Weld(size=10, length= 100, material_grade=design_dictionary[KEY_MATERIAL])
        print("input values are set. Doing preliminary member checks")
        self.member_capacity(self)

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.build)
        if self.supported_section.type == "Rolled":
            length = self.supported_section.depth
        else:
            length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # For Built-up section

        self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)

        if self.supported_section.shear_yielding_capacity > self.load.shear_force :
            print("preliminary member check is satisfactory. Checking available angle thickness")
            self.design_status = True
            self.select_angle_thickness(self)
        else:
            self.design_status = False
            logger.error(" : shear yielding capacity {} is less than applied load, Please select larger sections or decrease loads"
                            .format(self.supported_section.shear_yielding_capacity))
            print("failed in preliminary member checks. Select larger sections or decrease loads")

    def select_angle_thickness(self):
        self.plate.angle_thickness = []
        self.seated_angle.width = self.supported_section.flange_width

        for designation in self.seated_list:
            seated = Angle(designation=designation, material_grade=self.material_grade)
            # length of bearing required at the root line of beam (b) = R*gamma_m0/t_w*f_yw
            # Rearranged equation from cl. 8.7.4
            b1 = IS800_2007.cl_8_7_1_3_stiff_bearing_length(self.load.shear_force,
                                                            self.supported_section.web_thickness,
                                                            self.supported_section.flange_thickness,
                                                            self.supported_section.root_radius,
                                                            self.supported_section.fy)
            # Distance from the end of bearing on cleat to root angle OR A TO B in Fig 5.31 in Subramanian's book
            b2 = max(b1 + self.plate.gap - seated.thickness - seated.root_radius, 0)
            # self.seated_angle.width = self.supported_section.flange_width
            [self.plate.moment_demand, self.plate.moment_capacity] = \
                self.check_moment_capacity(self.load.shear_force, seated.thickness,self.seated_angle.width,
                                           b1,b2,self.material.fy)
            area = self.seated_angle.width * seated.thickness
            self.plate.shear_capacity = IS800_2007.cl_8_4_design_shear_strength(area, self.material.fy)
            if self.plate.moment_capacity < self.plate.moment_demand or self.plate.shear_capacity < self.load.shear_force:
                self.seated_list.pop()
                print("popped", designation)
            else:
                if seated.thickness not in self.plate.angle_thickness:
                    self.plate.angle_thickness.append(seated.thickness)
                    print("added", designation, self.plate.angle_thickness)

        if self.plate.angle_thickness:
            logger.info("Required Seated Angle thickness available. Getting angle leg size")
            self.get_bolt_details(self)
        else:
            logger.error("Increase Seated Angle thickness")

    @staticmethod
    def check_moment_capacity(self, shear, thickness, width, b1, b2, fy):
        if b1 <= b2:
            moment_at_root_angle = round(float(shear) * (b2 - b1 / 2), 3)
        else:
            moment_at_root_angle = round(float(shear) * (b2 / b1) * (b2 / 2), 3)

        Z_p = width * thickness ** 2 / 4
        Z_e = width * thickness ** 2 / 6
        plate_moment_capacity = IS800_2007.cl_8_2_1_2_design_moment_strength(Z_e, Z_p, fy, 'plastic')

        return moment_at_root_angle, plate_moment_capacity

    def get_bolt_details(self):
        print(self.design_status)
        for self.plate.angle_thickness_provided in sorted(self.plate.angle_thickness):
            # TO GET BOLT BEARING CAPACITY CORRESPONDING TO PLATE THICKNESS AND Fu AND Fy #
            self.bolt_conn_plates_t_fu_fy = []
            self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
            if self.connectivity == VALUES_CONN_1[1]:
                self.bolt_conn_plates_t_fu_fy.append(
                    (self.supporting_section.flange_thickness, self.supporting_section.fu, self.supporting_section.fy))
            else:
                self.bolt_conn_plates_t_fu_fy.append(
                    (self.supporting_section.web_thickness, self.supporting_section.fu, self.supporting_section.fy))
            bolts_required_previous = 2
            bolt_diameter_previous = self.bolt.bolt_diameter[-1]
            bolt_dia_possible =[]
            count =0
            for self.bolt.bolt_diameter_provided in reversed(self.bolt.bolt_diameter):
                self.bolt.bolt_grade_provided = max(self.bolt.bolt_grade)
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

                self.bolt.number = round_up(float(self.load.shear_force) / self.bolt.bolt_capacity, 1)
                min_bolts_one_line = 2
                if self.connectivity == VALUES_CONN_1[0]:
                    self.seated_angle.width = (self.seated_angle.width - self.supporting_section.web_thickness-
                                              self.supporting_section.root_radius)/2
                    self.bolt.number = round_up(float(self.bolt.number)/2, 1)
                    min_bolts_one_line = 1

                [bolt_line, bolts_one_line, web_plate_h] = \
                    self.plate.get_web_plate_l_bolts_one_line(self.seated_angle.width, self.seated_angle.width,
                                                              self.bolt.number, self.bolt.min_end_dist_round,
                                                              self.bolt.min_gauge_round, min_bolts_one_line)
                if 2 >= bolt_line >= 1:
                    bolt_dia_possible.append(self.bolt.bolt_diameter_provided)
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
                    continue
            if bolt_dia_possible:
                print("provided bolt diameter: ", self.bolt.bolt_diameter_provided)
            else:
                logger.error("Decrease bolt diameter")












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
        t2 = (KEY_SEATEDANGLE, self.seated_angle_customized)
        list1.append(t2)
        t3 = (KEY_TOPANGLE, self.top_angle_customized)
        list1.append(t3)
        t4 = (KEY_D, self.diam_bolt_customized)
        list1.append(t4)
        return list1

    def fn_conn_suptngsec_lbl(self):

        if self in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        # elif self in VALUES_CONN_2:
        #     return KEY_DISP_PRIBM
        else:
            return ''

    def fn_conn_suptdsec_lbl(self):

        if self in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        # elif self in VALUES_CONN_2:
        #     return KEY_DISP_SECBM
        else:
            return ''

    def fn_conn_suptngsec(self):

        if self in VALUES_CONN_1:
            return VALUES_COLSEC
        # elif self in VALUES_CONN_2:
        #     return VALUES_PRIBM
        else:
            return []

    def fn_conn_suptdsec(self):

        if self in VALUES_CONN_1:
            return VALUES_BEAMSEC
        # elif self in VALUES_CONN_2:
        #     return VALUES_SECBM
        else:
            return []

    def fn_conn_image(self):
        if self == VALUES_CONN[0]:
            return './ResourceFiles/images/fin_cf_bw.png'
        elif self == VALUES_CONN[1]:
            return './ResourceFiles/images/fin_cw_bw.png'
        # elif self in VALUES_CONN_2:
        #     return './ResourceFiles/images/fin_beam_beam.png'
        else:
            return ''

    def input_value_changed(self):

        lst = []

        t1 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_LABEL, self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_SUPTNGSEC, TYPE_COMBOBOX,self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = (KEY_CONN, KEY_SUPTDSEC, TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = (KEY_CONN, KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = (KEY_CONN, KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        return lst

    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair
        print(flag)

        out_list = []

        # TODO: Seated Angle properties: Start

        t13 = (None, KEY_DISP_SEATED_ANGLE, TYPE_TITLE, None, True)
        out_list.append(t13)

        t14 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.output[0][3] if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.output[0][4] if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_WIDTH, TYPE_TEXTBOX, self.output[0][5] if flag else '', True)
        out_list.append(t16)

        t22 = (KEY_OUT_PLATE_CAPACITIES, KEY_OUT_DISP_PLATE_CAPACITIES, TYPE_OUT_BUTTON, ['Capacity Details', self.capacities], True)
        out_list.append(t22)

        # TODO: Seated Angle Properties: End

        # TODO: Top Angle properties: Start

        t24 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t24)

        t25 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX, self.output[0][23] if flag else '', True)
        out_list.append(t25)

        t26 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX, self.output[0][25] if flag else '', True)
        out_list.append(t26)

        t27 = (KEY_OUT_WELD_STRESS, KEY_OUT_DISP_WELD_STRESS, TYPE_TEXTBOX, self.output[0][24] if flag else '', True)
        out_list.append(t27)

        # TODO: Top Angle Properties: End

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
        #
        # bolt_bearing_capacity_disp = ''
        # if flag is True:
        #     if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
        #         bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
        #         pass
        #     else:
        #         bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, self.output[0][8] if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX, self.output[0][6] if flag else '', True)
        out_list.append(t6)

        t21 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_SHEAR_FORCE, TYPE_TEXTBOX, self.output[0][10] if flag else '', True)
        out_list.append(t21)

        t23 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t23)

        # TODO: 'Bolt Properties: End'

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

    def to_get_d(my_d):
        print(my_d)
