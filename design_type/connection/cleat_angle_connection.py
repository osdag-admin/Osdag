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

    def input_values(self, existingvalues={}):

        self.module = KEY_DISP_CLEATANGLE

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

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN)
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

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_D)
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        options_list.append(t12)

        t13 = (None, DISP_TITLE_CLEAT, TYPE_TITLE, None, None)
        options_list.append(t13)

        t15 = (KEY_CLEATSEC, KEY_DISP_CLEATSEC, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_cleatsec, VALUES_ANGLESEC)
        options_list.append(t15)

        t16 = (KEY_MODULE, KEY_DISP_CLEATANGLE, TYPE_MODULE, None, None)
        options_list.append(t16)

        return options_list

    @staticmethod
    def cleatsec_customized():
        a = VALUES_CLEAT_CUSTOMIZED
        return a

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        if "36" in c: c.remove("36")
        return c

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, CleatAngleConnection.grdval_customized)
        list1.append(t1)
        t2 = (KEY_CLEATSEC, CleatAngleConnection.cleatsec_customized)
        list1.append(t2)
        t3 = (KEY_D, CleatAngleConnection.diam_bolt_customized)
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

    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair

        out_list = []

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None)
        out_list.append(t1)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_diameter_provided if flag else '')
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_grade_provided if flag else '')

        out_list.append(t3)

        t4 = (None, DISP_OUT_TITLE_SPTDLEG, TYPE_TITLE, None)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,  round(self.bolt.bolt_shear_capacity/1000,2) if flag else '')
        out_list.append(t5)
        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not 'N/A':
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
            else:
                bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t6 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '')
        out_list.append(t6)

        t7 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX, round(self.bolt.bolt_capacity/1000,2) if flag else '')
        out_list.append(t7)

        t8 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX, round(self.sptd_leg.bolt_force / 1000, 2) if flag else '')
        out_list.append(t8)

        t9 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.sptd_leg.bolt_line if flag else '')
        out_list.append(t9)

        t10 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.sptd_leg.bolts_one_line if flag else '')
        out_list.append(t10)

        t11 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing])
        out_list.append(t11)

        t12 = (None, DISP_OUT_TITLE_SPTNGLEG, TYPE_TITLE, None)
        out_list.append(t12)

        t13 = (KEY_OUT_SPTNG_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
              round(self.sptng_bolt.bolt_shear_capacity / 1000, 2) if flag else '')
        out_list.append(t13)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not 'N/A':
                bolt_bearing_capacity_disp = round(self.sptng_bolt.bolt_bearing_capacity / 1000, 2)
            else:
                bolt_bearing_capacity_disp = self.sptng_bolt.bolt_bearing_capacity

        t14 = (KEY_OUT_SPTNG_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '')
        out_list.append(t14)

        t15 = (KEY_OUT_SPTNG_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
              round(self.sptng_bolt.bolt_capacity / 1000, 2) if flag else '')
        out_list.append(t15)

        t16 = (KEY_OUT_SPTNG_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX,
              round(self.sptng_leg.bolt_force / 1000, 2) if flag else '')
        out_list.append(t16)

        t17 = (KEY_OUT_SPTNG_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.sptng_leg.bolt_line if flag else '')
        out_list.append(t17)

        t18 = (
        KEY_OUT_SPTNG_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.sptng_leg.bolts_one_line if flag else '')
        out_list.append(t18)

        t19 = (KEY_OUT_SPTNG_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.sptng_spacing])
        out_list.append(t19)

        t20 = (None, DISP_OUT_TITLE_CLEAT, TYPE_TITLE, None)
        out_list.append(t20)

        t15 = (KEY_OUT_CLEAT_HEIGHT, KEY_OUT_DISP_CLEAT_HEIGHT, TYPE_TEXTBOX, self.sptd_leg.height if flag else '')
        out_list.append(t15)

        t16 = (KEY_OUT_CLEAT_SPTDLEG, KEY_OUT_DISP_CLEAT_SPTDLEG, TYPE_TEXTBOX, self.cleat.leg_a_length if flag else '')
        out_list.append(t16)

        t16 = (KEY_OUT_CLEAT_SPTNGLEG, KEY_OUT_DISP_CLEAT_SPTNGLEG, TYPE_TEXTBOX, self.cleat.leg_b_length if flag else '')
        out_list.append(t16)

        t17 = (KEY_OUT_CLEAT_SHEAR, KEY_OUT_DISP_CLEAT_SPTNGLEG, TYPE_TEXTBOX, round(self.sptd_leg.shear_yielding_capacity,2) if flag else '')
        out_list.append(t17)

        t18 = (KEY_OUT_CLEAT_BLK_SHEAR, KEY_DISP_BLK_SHEAR, TYPE_TEXTBOX, round(self.sptd_leg.block_shear_capacity,2) if flag else '')
        out_list.append(t18)

        t19 = (KEY_OUT_CLEAT_BLK_SHEAR, KEY_DISP_MOM_DEMAND, TYPE_TEXTBOX, round(self.sptd_leg.moment_demand/1000000,2) if flag else '')
        out_list.append(t19)

        t20 = (KEY_OUT_CLEAT_MOM_CAPACITY, KEY_DISP_MOM_CAPACITY, TYPE_TEXTBOX, round(self.sptd_leg.moment_capacity,2) if flag else '')
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
            #     if design_dictionary[option[0]] == "Fin Plate":

        if design_dictionary[KEY_CONN] == 'Beam-Beam':
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
        else:
            flag1 = True

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self,missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        if flag and flag1:
            self.set_input_values(self, design_dictionary)
        else:
            return all_errors

    def module_name(self):
        return KEY_DISP_CLEATANGLE

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
        print(design_dictionary)

        super(CleatAngleConnection,self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.cleat_list = design_dictionary[KEY_CLEATSEC]
        self.material_grade = design_dictionary[KEY_MATERIAL]
        print(self.cleat_list)

        self.sptd_leg = Plate(material_grade=design_dictionary[KEY_MATERIAL],gap=design_dictionary[KEY_DP_DETAILING_GAP])
        # self.sptng_leg = self.sptd_leg


        logger.info("Input values are set. Checking if angle of required thickness is available")

        self.check_available_cleat_thk(self)


    def check_available_cleat_thk(self):
        self.sptd_leg.thickness = []

        min_thickness = self.supported_section.web_thickness / 2
        for designation in self.cleat_list:
            cleat = Angle(designation=designation,material_grade=self.material_grade)
            if cleat.thickness*2 <= self.supported_section.web_thickness:
                self.cleat_list.pop()
                print("popped", designation)
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
            self.sptd_bolt_conn_plates_t_fu_fy.append((self.supporting_section.flange_thickness, self.supporting_section.fu, self.supporting_section.fy))
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

            self.cleat = Angle(designation=self.cleat_angle_selected, material_grade=self.material_grade)





        designation_angle = self.cleat_list[0]
        self.cleat = Angle(designation=designation_angle, material_grade=self.material_grade)
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
