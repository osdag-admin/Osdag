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
        self.seated_angle = Angle(designation=seated_angle_section, material=self.material)
        self.top_angle = Angle(designation=top_angle_section, material=self.material)

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


        t16 = (KEY_MODULE, KEY_DISP_SEATED_ANGLE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN_1)
        options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        options_list.append(t3)

        t4 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, VALUES_COLSEC)
        options_list.append(t4)

        t5 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, VALUES_BEAMSEC)
        options_list.append(t5)

        t6 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t6)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t7)

        t8 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None)
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None)
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX, existingvalue_key_d, VALUES_D)
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX, existingvalue_key_grd, VALUES_GRD)
        options_list.append(t12)

        t13 = (None,DISP_TITLE_ANGLE, TYPE_TITLE, None, None)
        options_list.append(t13)

        t14 = (KEY_SEATEDANGLE, KEY_DISP_SEATEDANGLE, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_seatedangle, VALUES_ANGLESEC)
        options_list.append(t14)

        t15 = (KEY_TOPANGLE, KEY_DISP_TOPANGLE, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_topangle, VALUES_ANGLESEC)
        options_list.append(t15)

        return options_list

    def func_for_validation(self, window, design_dictionary):

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

        if design_dictionary[KEY_CONN] == 'Column web-Beam web':
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
            QMessageBox.information(window, "Information",
                                    generate_missing_fields_error_string(missing_fields_list))
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
            print("preliminary member check is satisfactory. Doing bolt checks")
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

            if seated.thickness * 2 <= self.supported_section.web_thickness:
                self.seated_list.pop()
                print("popped", designation)
            else:
                if seated.thickness not in self.plate.angle_thickness:
                    self.plate.angle_thickness.append(seated.thickness)
                    print("added", designation, self.plate.angle_thickness)

        if self.plate.angle_thickness:
            logger.info("Required Seated Angle thickness available. Doing preliminary member checks")
            self.member_capacity(self)
        else:
            logger.error("Increase Seated Angle thickness")

        self.seated_angle.width = self.supported_section.flange_width





        return self.seated_angle.thickness

    def check_moment_capacity(self, shear, thickness, width, b1, b2, fy):
        if b1<=b2:
            moment_at_root_angle = round(float(shear) * (b2 - b1 / 2), 3)
        else:
            moment_at_root_angle = round(float(shear) * (b2 / b1) * (b2 / 2), 3)

        moment_capacity = width * thickness **2 * fy/ 4

















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
        t2 = (KEY_SEATEDANGLE, SeatedAngleConnection.seated_angle_customized)
        list1.append(t2)
        t3 = (KEY_TOPANGLE, SeatedAngleConnection.top_angle_customized)
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

    def to_get_d(my_d):
        print(my_d)
