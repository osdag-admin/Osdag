from main import Main
from Common import *
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QMessageBox


class Compression(Main):

    def module_name(self):
        return KEY_DISP_COMPRESSION

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

    def customized_input(self):

        c_lst = []

        t1 = (KEY_SECSIZE, self.fn_profile_section)
        c_lst.append(t1)

        return c_lst

    def input_values(self, existingvalues={}):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair

        options_list = []

        if KEY_SEC_PROFILE in existingvalues:
            existingvalue_key_sec_profile = existingvalues[KEY_SEC_PROFILE]
        else:
            existingvalue_key_sec_profile = ''

        if KEY_SECSIZE in existingvalues:
            existingvalue_key_sec_size = existingvalues[KEY_SECSIZE]
        else:
            existingvalue_key_sec_size = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_LENZZ in existingvalues:
            existingvalue_key_len_zz = existingvalues[KEY_LENZZ]
        else:
            existingvalue_key_len_zz = ''

        if KEY_LENYY in existingvalues:
            existingvalue_key_len_yy = existingvalues[KEY_LENYY]
        else:
            existingvalue_key_len_yy = ''

        if KEY_AXIAL in existingvalues:
            existingvalue_key_axial = existingvalues[KEY_AXIAL]
        else:
            existingvalue_key_axial = ''

        if KEY_END1 in existingvalues:
            existingvalue_key_end1 = existingvalues[KEY_END1]
        else:
            existingvalue_key_end1 = ''

        if KEY_END2 in existingvalues:
            existingvalue_key_end2 = existingvalues[KEY_END2]
        else:
            existingvalue_key_end2 = ''

        t1 = (KEY_MODULE, KEY_DISP_COMPRESSION, TYPE_MODULE, None, None)
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, existingvalue_key_sec_profile, VALUES_SEC_PROFILE)
        options_list.append(t2)

        t3 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_sec_size, ['All', 'Customized'])
        options_list.append(t3)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t4)

        t5 = (KEY_LENZZ, KEY_DISP_LENZZ, TYPE_TEXTBOX, existingvalue_key_len_zz, None)
        options_list.append(t5)

        t6 = (KEY_LENYY, KEY_DISP_LENYY, TYPE_TEXTBOX, existingvalue_key_len_yy, None)
        options_list.append(t6)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None)
        options_list.append(t8)

        t9 = (None, DISP_TITLE_SC, TYPE_TITLE, None, None)
        options_list.append(t9)

        t10 = (KEY_END1, KEY_DISP_END1, TYPE_COMBOBOX, existingvalue_key_end1, VALUES_END1)
        options_list.append(t10)

        t11 = (KEY_END2, KEY_DISP_END2, TYPE_COMBOBOX, existingvalue_key_end2, VALUES_END2)
        options_list.append(t11)

        t12 = (KEY_IMAGE, None, TYPE_IMAGE_COMPRESSION, None, "./ResourceFiles/images/6.RRRR.PNG")
        options_list.append(t12)

        return options_list

    def fn_profile_section(self):
        if self == 'Beams':
            return connectdb("Beams", call_type="popup")
        elif self == 'Columns':
            return connectdb("Columns", call_type="popup")
        elif self in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return connectdb("Angles", call_type="popup")
        elif self in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type="popup")

    def fn_end1_end2(self):

        if self == 'Fixed':
            return VALUES_END2
        elif self == 'Free':
            return ['Fixed']
        elif self == 'Hinged':
            return ['Fixed', 'Hinged', 'Roller']
        elif self == 'Roller':
            return ['Fixed', 'Hinged']

    def fn_end1_image(self):

        if self == 'Fixed':
            return "./ResourceFiles/images/6.RRRR.PNG"
        elif self == 'Free':
            return "./ResourceFiles/images/1.RRFF.PNG"
        elif self == 'Hinged':
            return "./ResourceFiles/images/5.RRRF.PNG"
        elif self == 'Roller':
            return "./ResourceFiles/images/4.RRFR.PNG"

    def fn_end2_image(self, end1):

        if end1 == 'Fixed':
            if self == 'Fixed':
                return "./ResourceFiles/images/6.RRRR.PNG"
            elif self == 'Free':
                return "./ResourceFiles/images/1.RRFF_rotated.PNG"
            elif self == 'Hinged':
                return "./ResourceFiles/images/5.RRRF_rotated.PNG"
            elif self == 'Roller':
                return "./ResourceFiles/images/4.RRFR_rotated.PNG"
        elif end1 == 'Free':
            return "./ResourceFiles/images/1.RRFF.PNG"
        elif end1 == 'Hinged':
            if self == 'Fixed':
                return "./ResourceFiles/images/5.RRRF.PNG"
            elif self == 'Hinged':
                return "./ResourceFiles/images/3.RFRF.PNG"
            elif self == 'Roller':
                return "./ResourceFiles/images/2.FRFR_rotated.PNG"
        elif end1 == 'Roller':
            if self == 'Fixed':
                return "./ResourceFiles/images/4.RRFR.PNG"
            elif self == 'Hinged':
                return "./ResourceFiles/images/2.FRFR.PNG"

    def input_value_changed(self):

        lst = []

        t1 = (KEY_SEC_PROFILE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t1)

        t2 = (KEY_END1, KEY_END2, TYPE_COMBOBOX, self.fn_end1_end2)
        lst.append(t2)

        t3 = (KEY_END1, KEY_IMAGE, TYPE_IMAGE, self.fn_end1_image)
        lst.append(t3)

        t4 = (KEY_END2, KEY_IMAGE, TYPE_IMAGE, self.fn_end2_image)
        lst.append(t4)

        return lst

    def func_for_validation(self, window, design_dictionary):

        all_errors = []
        self.design_status = False
        flag = False
        option_list = self.input_values(self)
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] not in [KEY_SEC_PROFILE, KEY_END1, KEY_END2]:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) > 0:

            error = self.generate_missing_fields_error_string(self,missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        if flag:
            # self.set_input_values(self, design_dictionary)
            print(design_dictionary)
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

    # def supporting_section_values(self):
    #
    #     supporting_section = []
    #     t1 = (KEY_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_DESIGNATION, TYPE_TEXTBOX, None)
    #     supporting_section.append(t1)
    #
    #     t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
    #     supporting_section.append(t2)
    #
    #     t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None)
    #     supporting_section.append(t3)
    #
    #     t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t4)
    #
    #     t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
    #     supporting_section.append(t5)
    #
    #     t6 = (KEY_SUPTNGSEC_DEPTH, KEY_DISP_SUPTNGSEC_DEPTH, TYPE_TEXTBOX, None)
    #     supporting_section.append(t6)
    #
    #     t7 = (KEY_SUPTNGSEC_FLANGE_W, KEY_DISP_SUPTNGSEC_FLANGE_W, TYPE_TEXTBOX, None)
    #     supporting_section.append(t7)
    #
    #     t8 = (KEY_SUPTNGSEC_FLANGE_T, KEY_DISP_SUPTNGSEC_FLANGE_T, TYPE_TEXTBOX, None)
    #     supporting_section.append(t8)
    #
    #     t9 = (KEY_SUPTNGSEC_WEB_T, KEY_DISP_SUPTNGSEC_WEB_T, TYPE_TEXTBOX, None)
    #     supporting_section.append(t9)
    #
    #     t10 = (KEY_SUPTNGSEC_FLANGE_S, KEY_DISP_SUPTNGSEC_FLANGE_S, TYPE_TEXTBOX, None)
    #     supporting_section.append(t10)
    #
    #     t11 = (KEY_SUPTNGSEC_ROOT_R, KEY_DISP_SUPTNGSEC_ROOT_R, TYPE_TEXTBOX, None)
    #     supporting_section.append(t11)
    #
    #     t12 = (KEY_SUPTNGSEC_TOE_R, KEY_DISP_SUPTNGSEC_TOE_R, TYPE_TEXTBOX, None)
    #     supporting_section.append(t12)
    #
    #     t13 = (None, None, TYPE_BREAK, None)
    #     supporting_section.append(t13)
    #
    #     t14 = (KEY_SUPTNGSEC_TYPE, KEY_DISP_SUPTNGSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
    #     supporting_section.append(t14)
    #
    #     t18 = (None, None, TYPE_ENTER, None)
    #     supporting_section.append(t18)
    #
    #     t15 = (KEY_SUPTNGSEC_MOD_OF_ELAST, KEY_SUPTNGSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
    #     supporting_section.append(t15)
    #
    #     t16 = (KEY_SUPTNGSEC_MOD_OF_RIGID, KEY_SUPTNGSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
    #     supporting_section.append(t16)
    #
    #     t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
    #     supporting_section.append(t17)
    #
    #     t18 = (KEY_SUPTNGSEC_MASS, KEY_DISP_SUPTNGSEC_MASS, TYPE_TEXTBOX, None)
    #     supporting_section.append(t18)
    #
    #     t19 = (KEY_SUPTNGSEC_SEC_AREA, KEY_DISP_SUPTNGSEC_SEC_AREA, TYPE_TEXTBOX, None)
    #     supporting_section.append(t19)
    #
    #     t20 = (KEY_SUPTNGSEC_MOA_LZ, KEY_DISP_SUPTNGSEC_MOA_LZ, TYPE_TEXTBOX, None)
    #     supporting_section.append(t20)
    #
    #     t21 = (KEY_SUPTNGSEC_MOA_LY, KEY_DISP_SUPTNGSEC_MOA_LY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t21)
    #
    #     t22 = (KEY_SUPTNGSEC_ROG_RZ, KEY_DISP_SUPTNGSEC_ROG_RZ, TYPE_TEXTBOX, None)
    #     supporting_section.append(t22)
    #
    #     t23 = (KEY_SUPTNGSEC_ROG_RY, KEY_DISP_SUPTNGSEC_ROG_RY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t23)
    #
    #     t24 = (KEY_SUPTNGSEC_EM_ZZ, KEY_DISP_SUPTNGSEC_EM_ZZ, TYPE_TEXTBOX, None)
    #     supporting_section.append(t24)
    #
    #     t25 = (KEY_SUPTNGSEC_EM_ZY, KEY_DISP_SUPTNGSEC_EM_ZY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t25)
    #
    #     t26 = (KEY_SUPTNGSEC_PM_ZPZ, KEY_DISP_SUPTNGSEC_PM_ZPZ, TYPE_TEXTBOX, None)
    #     supporting_section.append(t26)
    #
    #     t27 = (KEY_SUPTNGSEC_PM_ZPY, KEY_DISP_SUPTNGSEC_PM_ZPY, TYPE_TEXTBOX, None)
    #     supporting_section.append(t27)
    #
    #     t28 = (None, None, TYPE_BREAK, None)
    #     supporting_section.append(t28)
    #
    #     t29 = (KEY_SUPTNGSEC_SOURCE, KEY_DISP_SUPTNGSEC_SOURCE, TYPE_TEXTBOX, None)
    #     supporting_section.append(t29)
    #
    #     t30 = (None, None, TYPE_ENTER, None)
    #     supporting_section.append(t30)
    #
    #     t31 = (KEY_SUPTNGSEC_POISSON_RATIO, KEY_DISP_SUPTNGSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
    #     supporting_section.append(t31)
    #
    #     t32 = (KEY_SUPTNGSEC_THERMAL_EXP, KEY_DISP_SUPTNGSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
    #     supporting_section.append(t32)
    #
    #     t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
    #     supporting_section.append(t33)
    #
    #     return supporting_section
    #
    # def supported_section_values(self):
    #
    #     supported_section = []
    #
    #     t1 = (KEY_SUPTDSEC_DESIGNATION, KEY_DISP_SUPTDSEC_DESIGNATION, TYPE_TEXTBOX, None)
    #     supported_section.append(t1)
    #
    #     t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
    #     supported_section.append(t2)
    #
    #     t3 = (KEY_SUPTDSEC_FU, KEY_DISP_SUPTDSEC_FU, TYPE_TEXTBOX, None)
    #     supported_section.append(t3)
    #
    #     t4 = (KEY_SUPTDSEC_FY, KEY_DISP_SUPTDSEC_FY, TYPE_TEXTBOX, None)
    #     supported_section.append(t4)
    #
    #     t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
    #     supported_section.append(t5)
    #
    #     t6 = (KEY_SUPTDSEC_DEPTH, KEY_DISP_SUPTDSEC_DEPTH, TYPE_TEXTBOX, None)
    #     supported_section.append(t6)
    #
    #     t7 = (KEY_SUPTDSEC_FLANGE_W, KEY_DISP_SUPTDSEC_FLANGE_W, TYPE_TEXTBOX, None)
    #     supported_section.append(t7)
    #
    #     t8 = (KEY_SUPTDSEC_FLANGE_T, KEY_DISP_SUPTDSEC_FLANGE_T, TYPE_TEXTBOX, None)
    #     supported_section.append(t8)
    #
    #     t9 = (KEY_SUPTDSEC_WEB_T, KEY_DISP_SUPTDSEC_WEB_T, TYPE_TEXTBOX, None)
    #     supported_section.append(t9)
    #
    #     t10 = (KEY_SUPTDSEC_FLANGE_S, KEY_DISP_SUPTDSEC_FLANGE_S, TYPE_TEXTBOX, None)
    #     supported_section.append(t10)
    #
    #     t11 = (KEY_SUPTDSEC_ROOT_R, KEY_DISP_SUPTDSEC_ROOT_R, TYPE_TEXTBOX, None)
    #     supported_section.append(t11)
    #
    #     t12 = (KEY_SUPTDSEC_TOE_R, KEY_DISP_SUPTDSEC_TOE_R, TYPE_TEXTBOX, None)
    #     supported_section.append(t12)
    #
    #     t13 = (None, None, TYPE_BREAK, None)
    #     supported_section.append(t13)
    #
    #     t14 = (KEY_SUPTDSEC_TYPE, KEY_DISP_SUPTDSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
    #     supported_section.append(t14)
    #
    #     t18 = (None, None, TYPE_ENTER, None)
    #     supported_section.append(t18)
    #
    #     t15 = (KEY_SUPTDSEC_MOD_OF_ELAST, KEY_SUPTDSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
    #     supported_section.append(t15)
    #
    #     t16 = (KEY_SUPTDSEC_MOD_OF_RIGID, KEY_SUPTDSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
    #     supported_section.append(t16)
    #
    #     t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
    #     supported_section.append(t17)
    #
    #     t18 = (KEY_SUPTDSEC_MASS, KEY_DISP_SUPTDSEC_MASS, TYPE_TEXTBOX, None)
    #     supported_section.append(t18)
    #
    #     t19 = (KEY_SUPTDSEC_SEC_AREA, KEY_DISP_SUPTDSEC_SEC_AREA, TYPE_TEXTBOX, None)
    #     supported_section.append(t19)
    #
    #     t20 = (KEY_SUPTDSEC_MOA_LZ, KEY_DISP_SUPTDSEC_MOA_LZ, TYPE_TEXTBOX, None)
    #     supported_section.append(t20)
    #
    #     t21 = (KEY_SUPTDSEC_MOA_LY, KEY_DISP_SUPTDSEC_MOA_LY, TYPE_TEXTBOX, None)
    #     supported_section.append(t21)
    #
    #     t22 = (KEY_SUPTDSEC_ROG_RZ, KEY_DISP_SUPTDSEC_ROG_RZ, TYPE_TEXTBOX, None)
    #     supported_section.append(t22)
    #
    #     t23 = (KEY_SUPTDSEC_ROG_RY, KEY_DISP_SUPTDSEC_ROG_RY, TYPE_TEXTBOX, None)
    #     supported_section.append(t23)
    #
    #     t24 = (KEY_SUPTDSEC_EM_ZZ, KEY_DISP_SUPTDSEC_EM_ZZ, TYPE_TEXTBOX, None)
    #     supported_section.append(t24)
    #
    #     t25 = (KEY_SUPTDSEC_EM_ZY, KEY_DISP_SUPTDSEC_EM_ZY, TYPE_TEXTBOX, None)
    #     supported_section.append(t25)
    #
    #     t26 = (KEY_SUPTDSEC_PM_ZPZ, KEY_DISP_SUPTDSEC_PM_ZPZ, TYPE_TEXTBOX, None)
    #     supported_section.append(t26)
    #
    #     t27 = (KEY_SUPTDSEC_PM_ZPY, KEY_DISP_SUPTDSEC_PM_ZPY, TYPE_TEXTBOX, None)
    #     supported_section.append(t27)
    #
    #     t28 = (None, None, TYPE_BREAK, None)
    #     supported_section.append(t28)
    #
    #     t29 = (KEY_SUPTDSEC_SOURCE, KEY_DISP_SUPTDSEC_SOURCE, TYPE_TEXTBOX, None)
    #     supported_section.append(t29)
    #
    #     t30 = (None, None, TYPE_ENTER, None)
    #     supported_section.append(t30)
    #
    #     t31 = (KEY_SUPTDSEC_POISSON_RATIO, KEY_DISP_SUPTDSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
    #     supported_section.append(t31)
    #
    #     t32 = (KEY_SUPTDSEC_THERMAL_EXP, KEY_DISP_SUPTDSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
    #     supported_section.append(t32)
    #
    #     t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
    #     supported_section.append(t33)
    #
    #     return supported_section


    def output_values(self, flag):
        return []

    @staticmethod
    def tab_column_section():
        supporting_section = []

        t34 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, [])
        supporting_section.append(t34)

        t1 = (KEY_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_DESIGNATION, TYPE_TEXTBOX, None)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
        supporting_section.append(t2)

        t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None)
        supporting_section.append(t3)

        t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None)
        supporting_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
        supporting_section.append(t5)

        t6 = (KEY_SUPTNGSEC_DEPTH, KEY_DISP_SUPTNGSEC_DEPTH, TYPE_TEXTBOX, None)
        supporting_section.append(t6)

        t7 = (KEY_SUPTNGSEC_FLANGE_W, KEY_DISP_SUPTNGSEC_FLANGE_W, TYPE_TEXTBOX, None)
        supporting_section.append(t7)

        t8 = (KEY_SUPTNGSEC_FLANGE_T, KEY_DISP_SUPTNGSEC_FLANGE_T, TYPE_TEXTBOX, None)
        supporting_section.append(t8)

        t9 = (KEY_SUPTNGSEC_WEB_T, KEY_DISP_SUPTNGSEC_WEB_T, TYPE_TEXTBOX, None)
        supporting_section.append(t9)

        t10 = (KEY_SUPTNGSEC_FLANGE_S, KEY_DISP_SUPTNGSEC_FLANGE_S, TYPE_TEXTBOX, None)
        supporting_section.append(t10)

        t11 = (KEY_SUPTNGSEC_ROOT_R, KEY_DISP_SUPTNGSEC_ROOT_R, TYPE_TEXTBOX, None)
        supporting_section.append(t11)

        t12 = (KEY_SUPTNGSEC_TOE_R, KEY_DISP_SUPTNGSEC_TOE_R, TYPE_TEXTBOX, None)
        supporting_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None)
        supporting_section.append(t13)

        t35 = (None, None, TYPE_ENTER, None)
        supporting_section.append(t35)

        t14 = (KEY_SUPTNGSEC_TYPE, KEY_DISP_SUPTNGSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
        supporting_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None)
        supporting_section.append(t18)

        t15 = (KEY_SUPTNGSEC_MOD_OF_ELAST, KEY_SUPTNGSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
        supporting_section.append(t15)

        t16 = (KEY_SUPTNGSEC_MOD_OF_RIGID, KEY_SUPTNGSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
        supporting_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
        supporting_section.append(t17)

        t18 = (KEY_SUPTNGSEC_MASS, KEY_DISP_SUPTNGSEC_MASS, TYPE_TEXTBOX, None)
        supporting_section.append(t18)

        t19 = (KEY_SUPTNGSEC_SEC_AREA, KEY_DISP_SUPTNGSEC_SEC_AREA, TYPE_TEXTBOX, None)
        supporting_section.append(t19)

        t20 = (KEY_SUPTNGSEC_MOA_LZ, KEY_DISP_SUPTNGSEC_MOA_LZ, TYPE_TEXTBOX, None)
        supporting_section.append(t20)

        t21 = (KEY_SUPTNGSEC_MOA_LY, KEY_DISP_SUPTNGSEC_MOA_LY, TYPE_TEXTBOX, None)
        supporting_section.append(t21)

        t22 = (KEY_SUPTNGSEC_ROG_RZ, KEY_DISP_SUPTNGSEC_ROG_RZ, TYPE_TEXTBOX, None)
        supporting_section.append(t22)

        t23 = (KEY_SUPTNGSEC_ROG_RY, KEY_DISP_SUPTNGSEC_ROG_RY, TYPE_TEXTBOX, None)
        supporting_section.append(t23)

        t24 = (KEY_SUPTNGSEC_EM_ZZ, KEY_DISP_SUPTNGSEC_EM_ZZ, TYPE_TEXTBOX, None)
        supporting_section.append(t24)

        t25 = (KEY_SUPTNGSEC_EM_ZY, KEY_DISP_SUPTNGSEC_EM_ZY, TYPE_TEXTBOX, None)
        supporting_section.append(t25)

        t26 = (KEY_SUPTNGSEC_PM_ZPZ, KEY_DISP_SUPTNGSEC_PM_ZPZ, TYPE_TEXTBOX, None)
        supporting_section.append(t26)

        t27 = (KEY_SUPTNGSEC_PM_ZPY, KEY_DISP_SUPTNGSEC_PM_ZPY, TYPE_TEXTBOX, None)
        supporting_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None)
        supporting_section.append(t28)

        t36 = (None, None, TYPE_ENTER, None)
        supporting_section.append(t36)

        t29 = (KEY_SUPTNGSEC_SOURCE, KEY_DISP_SUPTNGSEC_SOURCE, TYPE_TEXTBOX, None)
        supporting_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None)
        supporting_section.append(t30)

        t31 = (KEY_SUPTNGSEC_POISSON_RATIO, KEY_DISP_SUPTNGSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
        supporting_section.append(t31)

        t32 = (KEY_SUPTNGSEC_THERMAL_EXP, KEY_DISP_SUPTNGSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
        supporting_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        supporting_section.append(t33)

        return supporting_section

    @staticmethod
    def tab_beam_section():
        supported_section = []

        t34 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, [])
        supported_section.append(t34)

        t1 = (KEY_SUPTDSEC_DESIGNATION, KEY_DISP_SUPTDSEC_DESIGNATION, TYPE_TEXTBOX, None)
        supported_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
        supported_section.append(t2)

        t3 = (KEY_SUPTDSEC_FU, KEY_DISP_SUPTDSEC_FU, TYPE_TEXTBOX, None)
        supported_section.append(t3)

        t4 = (KEY_SUPTDSEC_FY, KEY_DISP_SUPTDSEC_FY, TYPE_TEXTBOX, None)
        supported_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
        supported_section.append(t5)

        t6 = (KEY_SUPTDSEC_DEPTH, KEY_DISP_SUPTDSEC_DEPTH, TYPE_TEXTBOX, None)
        supported_section.append(t6)

        t7 = (KEY_SUPTDSEC_FLANGE_W, KEY_DISP_SUPTDSEC_FLANGE_W, TYPE_TEXTBOX, None)
        supported_section.append(t7)

        t8 = (KEY_SUPTDSEC_FLANGE_T, KEY_DISP_SUPTDSEC_FLANGE_T, TYPE_TEXTBOX, None)
        supported_section.append(t8)

        t9 = (KEY_SUPTDSEC_WEB_T, KEY_DISP_SUPTDSEC_WEB_T, TYPE_TEXTBOX, None)
        supported_section.append(t9)

        t10 = (KEY_SUPTDSEC_FLANGE_S, KEY_DISP_SUPTDSEC_FLANGE_S, TYPE_TEXTBOX, None)
        supported_section.append(t10)

        t11 = (KEY_SUPTDSEC_ROOT_R, KEY_DISP_SUPTDSEC_ROOT_R, TYPE_TEXTBOX, None)
        supported_section.append(t11)

        t12 = (KEY_SUPTDSEC_TOE_R, KEY_DISP_SUPTDSEC_TOE_R, TYPE_TEXTBOX, None)
        supported_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None)
        supported_section.append(t13)

        t35 = (None, None, TYPE_ENTER, None)
        supported_section.append(t35)

        t14 = (KEY_SUPTDSEC_TYPE, KEY_DISP_SUPTDSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
        supported_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None)
        supported_section.append(t18)

        t15 = (KEY_SUPTDSEC_MOD_OF_ELAST, KEY_SUPTDSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
        supported_section.append(t15)

        t16 = (KEY_SUPTDSEC_MOD_OF_RIGID, KEY_SUPTDSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
        supported_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
        supported_section.append(t17)

        t18 = (KEY_SUPTDSEC_MASS, KEY_DISP_SUPTDSEC_MASS, TYPE_TEXTBOX, None)
        supported_section.append(t18)

        t19 = (KEY_SUPTDSEC_SEC_AREA, KEY_DISP_SUPTDSEC_SEC_AREA, TYPE_TEXTBOX, None)
        supported_section.append(t19)

        t20 = (KEY_SUPTDSEC_MOA_LZ, KEY_DISP_SUPTDSEC_MOA_LZ, TYPE_TEXTBOX, None)
        supported_section.append(t20)

        t21 = (KEY_SUPTDSEC_MOA_LY, KEY_DISP_SUPTDSEC_MOA_LY, TYPE_TEXTBOX, None)
        supported_section.append(t21)

        t22 = (KEY_SUPTDSEC_ROG_RZ, KEY_DISP_SUPTDSEC_ROG_RZ, TYPE_TEXTBOX, None)
        supported_section.append(t22)

        t23 = (KEY_SUPTDSEC_ROG_RY, KEY_DISP_SUPTDSEC_ROG_RY, TYPE_TEXTBOX, None)
        supported_section.append(t23)

        t24 = (KEY_SUPTDSEC_EM_ZZ, KEY_DISP_SUPTDSEC_EM_ZZ, TYPE_TEXTBOX, None)
        supported_section.append(t24)

        t25 = (KEY_SUPTDSEC_EM_ZY, KEY_DISP_SUPTDSEC_EM_ZY, TYPE_TEXTBOX, None)
        supported_section.append(t25)

        t26 = (KEY_SUPTDSEC_PM_ZPZ, KEY_DISP_SUPTDSEC_PM_ZPZ, TYPE_TEXTBOX, None)
        supported_section.append(t26)

        t27 = (KEY_SUPTDSEC_PM_ZPY, KEY_DISP_SUPTDSEC_PM_ZPY, TYPE_TEXTBOX, None)
        supported_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None)
        supported_section.append(t28)

        t36 = (None, None, TYPE_ENTER, None)
        supported_section.append(t36)

        t29 = (KEY_SUPTDSEC_SOURCE, KEY_DISP_SUPTDSEC_SOURCE, TYPE_TEXTBOX, None)
        supported_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None)
        supported_section.append(t30)

        t31 = (KEY_SUPTDSEC_POISSON_RATIO, KEY_DISP_SUPTDSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
        supported_section.append(t31)

        t32 = (KEY_SUPTDSEC_THERMAL_EXP, KEY_DISP_SUPTDSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
        supported_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        supported_section.append(t33)

        return supported_section

    @staticmethod
    def tab_angle_section():
        angle_section = []

        t34 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, [])
        angle_section.append(t34)

        t1 = (KEY_ANGLE_DESIGNATION, KEY_DISP_ANGLE_DESIGNATION, TYPE_TEXTBOX, None)
        angle_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
        angle_section.append(t2)

        t3 = (KEY_ANGLE_FU, KEY_DISP_ANGLE_FU, TYPE_TEXTBOX, None)
        angle_section.append(t3)

        t4 = (KEY_ANGLE_FY, KEY_DISP_ANGLE_FY, TYPE_TEXTBOX, None)
        angle_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
        angle_section.append(t5)

        t6 = (KEY_ANGLE_DEPTH, KEY_DISP_ANGLE_DEPTH, TYPE_TEXTBOX, None)
        angle_section.append(t6)

        t7 = (KEY_ANGLE_FLANGE_W, KEY_DISP_ANGLE_FLANGE_W, TYPE_TEXTBOX, None)
        angle_section.append(t7)

        t8 = (KEY_ANGLE_FLANGE_T, KEY_DISP_ANGLE_FLANGE_T, TYPE_TEXTBOX, None)
        angle_section.append(t8)

        t9 = (KEY_ANGLE_WEB_T, KEY_DISP_ANGLE_WEB_T, TYPE_TEXTBOX, None)
        angle_section.append(t9)

        t10 = (KEY_ANGLE_FLANGE_S, KEY_DISP_ANGLE_FLANGE_S, TYPE_TEXTBOX, None)
        angle_section.append(t10)

        t11 = (KEY_ANGLE_ROOT_R, KEY_DISP_ANGLE_ROOT_R, TYPE_TEXTBOX, None)
        angle_section.append(t11)

        t12 = (KEY_ANGLE_TOE_R, KEY_DISP_ANGLE_TOE_R, TYPE_TEXTBOX, None)
        angle_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None)
        angle_section.append(t13)

        t35 = (None, None, TYPE_ENTER, None)
        angle_section.append(t35)

        t14 = (KEY_ANGLE_TYPE, KEY_DISP_ANGLE_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
        angle_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None)
        angle_section.append(t18)

        t15 = (KEY_ANGLE_MOD_OF_ELAST, KEY_ANGLE_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
        angle_section.append(t15)

        t16 = (KEY_ANGLE_MOD_OF_RIGID, KEY_ANGLE_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
        angle_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
        angle_section.append(t17)

        t18 = (KEY_ANGLE_MASS, KEY_DISP_ANGLE_MASS, TYPE_TEXTBOX, None)
        angle_section.append(t18)

        t19 = (KEY_ANGLE_SEC_AREA, KEY_DISP_ANGLE_SEC_AREA, TYPE_TEXTBOX, None)
        angle_section.append(t19)

        t20 = (KEY_ANGLE_MOA_LZ, KEY_DISP_ANGLE_MOA_LZ, TYPE_TEXTBOX, None)
        angle_section.append(t20)

        t21 = (KEY_ANGLE_MOA_LY, KEY_DISP_ANGLE_MOA_LY, TYPE_TEXTBOX, None)
        angle_section.append(t21)

        t22 = (KEY_ANGLE_ROG_RZ, KEY_DISP_ANGLE_ROG_RZ, TYPE_TEXTBOX, None)
        angle_section.append(t22)

        t23 = (KEY_ANGLE_ROG_RY, KEY_DISP_ANGLE_ROG_RY, TYPE_TEXTBOX, None)
        angle_section.append(t23)

        t24 = (KEY_ANGLE_EM_ZZ, KEY_DISP_ANGLE_EM_ZZ, TYPE_TEXTBOX, None)
        angle_section.append(t24)

        t25 = (KEY_ANGLE_EM_ZY, KEY_DISP_ANGLE_EM_ZY, TYPE_TEXTBOX, None)
        angle_section.append(t25)

        t26 = (KEY_ANGLE_PM_ZPZ, KEY_DISP_ANGLE_PM_ZPZ, TYPE_TEXTBOX, None)
        angle_section.append(t26)

        t27 = (KEY_ANGLE_PM_ZPY, KEY_DISP_ANGLE_PM_ZPY, TYPE_TEXTBOX, None)
        angle_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None)
        angle_section.append(t28)

        t36 = (None, None, TYPE_ENTER, None)
        angle_section.append(t36)

        t29 = (KEY_ANGLE_SOURCE, KEY_DISP_ANGLE_SOURCE, TYPE_TEXTBOX, None)
        angle_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None)
        angle_section.append(t30)

        t31 = (KEY_ANGLE_POISSON_RATIO, KEY_DISP_ANGLE_POISSON_RATIO, TYPE_TEXTBOX, None)
        angle_section.append(t31)

        t32 = (KEY_ANGLE_THERMAL_EXP, KEY_DISP_ANGLE_THERMAL_EXP, TYPE_TEXTBOX, None)
        angle_section.append(t32)

        # t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        # angle_section.append(t33)

        return angle_section

    @staticmethod
    def tab_channel_section():
        #Channel Tab method for adding tab elements
        channel_section=[]
        # sample fields added
        t1 = (KEY_ANGLE_DESIGNATION, KEY_DISP_ANGLE_DESIGNATION, TYPE_TEXTBOX, None)
        channel_section.append(t1)

        return channel_section

    def tab_list(self):

        tabs = []

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_column_section)
        tabs.append(t1)

        t2 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_beam_section)
        tabs.append(t2)

        t3 = (DISP_TITLE_ANGLE, TYPE_TAB_1, self.tab_angle_section)
        tabs.append(t3)

        t4 = ("Channel", TYPE_TAB_1, self.tab_channel_section)
        tabs.append(t4)

        t5 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t5)

        t6 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t6)

        t7 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t7)

        t8 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t8)

        t9 = ("Connector", TYPE_TAB_2, self.connector_values)
        tabs.append(t9)
        return tabs

    @staticmethod
    def bolt_values():

        bolt = []

        t1 = (KEY_DP_BOLT_TYPE, KEY_DISP_TYP, TYPE_COMBOBOX, ['Pretensioned', 'Non-pretensioned'])
        bolt.append(t1)

        t2 = (KEY_DP_BOLT_HOLE_TYPE, KEY_DISP_DP_BOLT_HOLE_TYPE, TYPE_COMBOBOX, ['Standard', 'Over-sized'])
        bolt.append(t2)

        t3 = (KEY_DP_BOLT_MATERIAL_G_O, KEY_DISP_DP_BOLT_MATERIAL_G_O, TYPE_TEXTBOX, '410')
        bolt.append(t3)

        t4 = (None, None, TYPE_ENTER, None)
        bolt.append(t4)

        t5 = (None, KEY_DISP_DP_BOLT_DESIGN_PARA, TYPE_TITLE, None)
        bolt.append(t5)

        t6 = (KEY_DP_BOLT_SLIP_FACTOR, KEY_DISP_DP_BOLT_SLIP_FACTOR, TYPE_COMBOBOX, ['0.2', '0.5', '0.1', '0.25', '0.3',
                                                                                     '0.33', '0.48', '0.52', '0.55'])
        bolt.append(t6)

        t7 = (None, None, TYPE_ENTER, None)
        bolt.append(t7)

        t8 = (None, "NOTE : If slip is permitted under the design load, design the bolt as"
                    "<br>a bearing bolt and select corresponding bolt grade.", TYPE_NOTE, None)
        bolt.append(t8)

        t9 = ["textBrowser", "", TYPE_TEXT_BROWSER, BOLT_DESCRIPTION]
        bolt.append(t9)

        return bolt

    @staticmethod
    def weld_values():

        weld = []

        t1 = (KEY_DP_WELD_FAB, KEY_DISP_DP_WELD_FAB, TYPE_COMBOBOX, KEY_DP_WELD_FAB_VALUES)
        weld.append(t1)

        t2 = (KEY_DP_WELD_MATERIAL_G_O, KEY_DISP_DP_WELD_MATERIAL_G_O, TYPE_TEXTBOX, '410')
        weld.append(t2)

        t3 = ["textBrowser", "", TYPE_TEXT_BROWSER, WELD_DESCRIPTION]
        weld.append(t3)

        return weld

    @staticmethod
    def detailing_values():
        detailing = []

        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX, [
            'a - Sheared or hand flame cut', 'b - Rolled, machine-flame cut, sawn and planed'])
        detailing.append(t1)

        t2 = (KEY_DP_DETAILING_GAP, KEY_DISP_DP_DETAILING_GAP, TYPE_TEXTBOX, '10')
        detailing.append(t2)

        t3 = (KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES, TYPE_COMBOBOX,
              ['No', 'Yes'])
        detailing.append(t3)

        t4 = ["textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION]
        detailing.append(t4)

        return detailing

    @staticmethod
    def design_values():

        design = []

        t1 = (KEY_DP_DESIGN_METHOD, KEY_DISP_DP_DESIGN_METHOD, TYPE_COMBOBOX, ['Limit State Design',
                                                                               'Limit State (Capacity based) Design',
                                                                               'Working Stress Design'])
        design.append(t1)

        return design
    @staticmethod
    def connector_values():
        connector = []

        material = connectdb("Material", call_type="popup")
        material.append('Custom')
        t1 = (KEY_PLATE_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material)
        connector.append(t1)

        t2 = (KEY_PLATE_FU, KEY_DISP_PLATE_FU, TYPE_TEXTBOX, None)
        connector.append(t2)

        t3 = (KEY_PLATE_FY, KEY_DISP_PLATE_FY, TYPE_TEXTBOX, None)
        connector.append(t3)

        return connector
