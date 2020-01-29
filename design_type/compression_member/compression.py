from main import Main
from Common import *
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QMessageBox


class Compression(Main):

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
        handler = OurLog(key)
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def customized_input(self):
        return []

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

        t3 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, existingvalue_key_sec_size, connectdb("Beams"))
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
            return connectdb("Beams")
        elif self == 'Columns':
            return connectdb("Columns")
        elif self in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return connectdb("Angles")
        elif self in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels")

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

        t1 = (KEY_SEC_PROFILE, KEY_SECSIZE, TYPE_COMBOBOX, self.fn_profile_section)
        lst.append(t1)

        t2 = (KEY_END1, KEY_END2, TYPE_COMBOBOX, self.fn_end1_end2)
        lst.append(t2)

        t3 = (KEY_END1, KEY_IMAGE, TYPE_IMAGE, self.fn_end1_image)
        lst.append(t3)

        t4 = (KEY_END2, KEY_IMAGE, TYPE_IMAGE, self.fn_end2_image)
        lst.append(t4)

        return lst

    def func_for_validation(self, window, design_dictionary):
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
            QMessageBox.information(window, "Information",
                                    self.generate_missing_fields_error_string(self, missing_fields_list))
            # flag = False
        else:
            flag = True

        if flag:
            # self.set_input_values(self, design_dictionary)
            print(design_dictionary)
        else:
            pass

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

    def output_values(self, flag):
        return []