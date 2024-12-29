"""
Main module: Design of Compression Member
Sub-module:  Design of column (loaded axially)

@author: Rutvik Joshi, N swaroop, Adnan Abdullah (Project interns, 2021)
         Danish Ansari

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)

"""
import logging
import math
import numpy as np
from ...Common import *
from ..connection.moment_connection import MomentConnection
from ...utils.common.material import *
from ...utils.common.load import Load
from ...utils.common.component import ISection, Material
from ...utils.common.component import *
from ..member import Member
from ...Report_functions import *
from ...design_report.reportGenerator_latex import CreateLatex
from pylatex.utils import NoEscape

class ColumnDesign(Member):

    def __init__(self):
        # print(f"Here10")
        super(ColumnDesign, self).__init__()

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

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_section)
        tabs.append(t1)

        # t2 = (DISP_TITLE_CHANNEL, TYPE_TAB_1, self.tab_channel_section)
        # tabs.append(t2)
        
        t2 = ("Optimization", TYPE_TAB_2, self.optimization_tab_column_design)
        tabs.append(t2)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):
        """

        :return: This function is used to update the values of the keys in design preferences,
         which are dependent on other inputs.
         It returns list of tuple which contains, tab name, keys whose values will be changed,
         function to change the values and arguments for the function.

         [Tab Name, [Argument list], [list of keys to be updated], input widget type of keys, change_function]

         Here Argument list should have only one element.
         Changing of this element,(either changing index or text depending on widget type),
         will update the list of keys (this can be more than one).
         TODO: input widget type of keys (3rd element) is no longer required. needs to be removed

         """
        change_tab = []

        t1 = (KEY_DISP_COLSEC, [KEY_SEC_MATERIAL], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX, self.get_fu_fy_I_section)
        change_tab.append(t1)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_COLSEC, ['Label_HS_1', 'Label_HS_2', 'Label_HS_3'],
              ['Label_HS_11', 'Label_HS_12', 'Label_HS_13', 'Label_HS_14', 'Label_HS_15', 'Label_HS_16', 'Label_HS_17', 'Label_HS_18',
               'Label_HS_19', 'Label_HS_20', 'Label_HS_21', 'Label_HS_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_SHS_RHS_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, ['Label_CHS_1', 'Label_CHS_2', 'Label_CHS_3'],
              ['Label_CHS_11', 'Label_CHS_12', 'Label_CHS_13', 'Label_HS_14', 'Label_HS_15', 'Label_HS_16', 'Label_21', 'Label_22',
               KEY_IMAGE], TYPE_TEXTBOX, self.get_CHS_properties)
        change_tab.append(t6)

        t6 = (KEY_DISP_COLSEC, [KEY_SECSIZE], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        # t3 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE, KEY_SEC_MATERIAL,'Label_0'],
        #       [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14',
        #        'Label_4', 'Label_5',
        #        'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17',
        #        'Label_19', 'Label_20', 'Label_21',
        #        'Label_22', 'Label_23', 'Label_26','Label_27', KEY_IMAGE], TYPE_TEXTBOX, self.get_new_channel_section_properties)
        # change_tab.append(t3)


        # t4 = (DISP_TITLE_CHANNEL, ['Label_1', 'Label_2', 'Label_3', 'Label_13','Label_14'],
        #       ['Label_9', 'Label_10','Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17','Label_19', 'Label_20', 'Label_21', 'Label_22','Label_26','Label_27', KEY_IMAGE], TYPE_TEXTBOX, self.get_Channel_sec_properties)

        # change_tab.append(t4)

        # t7 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        # change_tab.append(t7)

        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
                Not required for this module but empty list should be passed"""
        return []

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        # t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, ['Label_8', KEY_SEC_MATERIAL])
        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])#Need to check
        design_input.append(t1)

        # t2 = (DISP_TITLE_CHANNEL, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        # design_input.append(t2)

        # t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY, 'Label_21'])
        t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY])
        design_input.append(t1)

        t2 = ("Optimization", TYPE_TEXTBOX, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA]) #, KEY_STEEL_COST
        design_input.append(t2)

        # t2 = ("Optimization", TYPE_COMBOBOX, [KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS1, KEY_ALLOW_CLASS2, KEY_ALLOW_CLASS3, KEY_ALLOW_CLASS4])
        # design_input.append(t2)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        return design_input

    def input_dictionary_without_design_pref(self):
        """
        This is declared in ui_template.py line 557

        :return: This function is used to choose values of design preferences to be saved to
        design dictionary if design preference is never opened by user. It sets are design preference values to default.
        If any design preference value needs to be set to input dock value, tuple shall be written as:

        (Key of input dock, [List of Keys from design prefernce], 'Input Dock')

        eg: input_dp_conn_list [('Material', ['Member.Material'], 'Input Dock'), (None, ['Optimum.AllowUR', 'Effective.Area_Para', 'Optimum.Para', 'Optimum.Class1', 'Optimum.Class2', 'Optimum.Class3', 'Optimum.Class4', 'Steel.Cost', 'Design.Design_Method'], '')]

        If the values needs to be set to default,

        (None, [List of Design Prefernce Keys], '')

         """
        design_input = []

        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA,  KEY_DP_DESIGN_METHOD], '') #KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS1, KEY_ALLOW_CLASS2, KEY_ALLOW_CLASS3, KEY_ALLOW_CLASS4, KEY_STEEL_COST,

        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

        :return: This function returns list of tuples which has keys that needs to be updated,
         on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

         [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
        """
        add_buttons = []

        t2 = (KEY_DISP_COLSEC, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE, None, None, "Columns")
        add_buttons.append(t2)

        # t2 = (DISP_TITLE_CHANNEL, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
        #       ['Channels', 'Back to Back Channels'], "Channels")
        # add_buttons.append(t2)

        return add_buttons

    def get_values_for_design_pref(self, key, design_dictionary):
        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            material = Material(design_dictionary[KEY_MATERIAL], 41)
            fu = material.fu
            fy = material.fy
        else:
            fu = ''
            fy = ''

        val = {
            KEY_ALLOW_UR: '1.0',
            KEY_EFFECTIVE_AREA_PARA: '1.0',
            KEY_OPTIMIZATION_PARA: 'Utilization Ratio',
            # KEY_STEEL_COST: '50',
            # KEY_ALLOW_CLASS1: 'Yes',
            # KEY_ALLOW_CLASS2: 'Yes',
            # KEY_ALLOW_CLASS3: 'Yes',
            # KEY_ALLOW_CLASS4: 'Yes',
            KEY_DP_DESIGN_METHOD: "Limit State Design",
        }[key]

        return val

    ####################################
    # Design Preference Functions End
    ####################################

    # Setting up logger and Input and Output Docks
    ####################################
    def module_name(self):
        return KEY_DISP_COMPRESSION_COLUMN

    def set_osdaglogger(key):
        """
        Set logger for Column Design Module.
        """
        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def customized_input(self):

        c_lst = []

        t1 = (KEY_SECSIZE, self.fn_profile_section)
        c_lst.append(t1)

        return c_lst

    def input_values(self):
        """ 
        Function declared in ui_template.py line 566

        Fuction to return a list of tuples to be displayed as the UI (Input Dock)
        
        eg:[(None, 'Section Property', 'Title', None, True, 'No Validator'), ('Module', 'Pure Axial Column Design', 'Window Title', None, True, 'No Validator'), ('Member.Profile', 'Section Profile*', 'ComboBox', ['Beams', 'Columns', 'RHS', 'SHS', 'CHS', 'Angles', 'Back to Back Angles', 'Channels', 'Back to Back Channels'], True, 'No Validator'), ('Member.Designation', 'Section Size*', 'ComboBox_Customized', ['All', 'Customized'], True, 'No Validator'), ('Material', 'Material', 'ComboBox', ['E 165 (Fe 290)', 'E 250 (Fe 410 W)A', 'E 250 (Fe 410 W)B', 'E 250 (Fe 410 W)C', 'E 300 (Fe 440)', 'E 350 (Fe 490)', 'E 410 (Fe 540)', 'E 450 (Fe 570)D', 'E 450 (Fe 590) E', 'Cus_400_500_600_1400', 'Custom'], True, 'No Validator'), (None, 'Section Data', 'Title', None, True, 'No Validator'), ('Actual.Length_zz', 'Actual Length (z-z), mm', 'TextBox', None, True, 'Int Validator'), ('Actual.Length_yy', 'Actual Length (y-y), mm', 'TextBox', None, True, 'Int Validator'), (None, 'End Condition', 'Title', None, True, 'No Validator'), ('End_1', 'End 1', 'ComboBox', ['Fixed', 'Free', 'Hinged', 'Roller'], True, 'No Validator'), ('End_2', 'End 2', 'ComboBox', ['Fixed', 'Free', 'Hinged', 'Roller'], True, 'No Validator'), ('Image', None, 'Image_compression', str(files("osdag.data.ResourceFiles.images").joinpath("6.RRRR.PNG")), True, 'No Validator'), (None, 'Factored Loads', 'Title', None, True, 'No Validator'), ('Load.Axial', 'Axial Force (kN)', 'TextBox', None, True, 'Int Validator')]
        """

        self.module = KEY_DISP_COMPRESSION_COLUMN
        options_list = []

        t1 = (None, KEY_SECTION_PROPERTY, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t1 = (KEY_MODULE, KEY_DISP_COMPRESSION_COLUMN, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, VALUES_SEC_PROFILE, True, 'No Validator')
        options_list.append(t2)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator')
        options_list.append(t4)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)

        t1 = (None, KEY_SECTION_DATA, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t5 = (KEY_UNSUPPORTED_LEN_ZZ, KEY_DISP_UNSUPPORTED_LEN_ZZ, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)

        t6 = (KEY_UNSUPPORTED_LEN_YY, KEY_DISP_UNSUPPORTED_LEN_YY, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t6)

        t9 = (None, KEY_DISP_END_CONDITION, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_END1, KEY_DISP_END1, TYPE_COMBOBOX, VALUES_END1, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_END2, KEY_DISP_END2, TYPE_COMBOBOX, VALUES_END2, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_IMAGE, None, TYPE_IMAGE_COMPRESSION, str(files("osdag.data.ResourceFiles.images").joinpath("6.RRRR.PNG")), True, 'No Validator')
        options_list.append(t12)

        t13 = (None, KEY_DISP_END_CONDITION_2, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_END1_Y, KEY_DISP_END1_Y, TYPE_COMBOBOX, VALUES_END1_Y, True, 'No Validator')
        options_list.append(t14)

        t15 = (KEY_END2_Y, KEY_DISP_END2_Y, TYPE_COMBOBOX, VALUES_END2_Y, True, 'No Validator')
        options_list.append(t15)

        t16 = (KEY_IMAGE_Y, None, TYPE_IMAGE_COMPRESSION, str(files("osdag.data.ResourceFiles.images").joinpath("6.RRRR.PNG")), True, 'No Validator')
        options_list.append(t16)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t8)

        return options_list

    def fn_profile_section(self):

        profile = self[0]
        if profile == 'Beams and Columns':
            res1 = connectdb("Beams", call_type="popup")
            res2 = connectdb("Columns", call_type="popup")
            return list(set(res1 + res2))
        elif profile == 'RHS and SHS':
            res1 = connectdb("RHS", call_type="popup")
            res2 = connectdb("SHS", call_type="popup")
            return list(set(res1 + res2))
        elif profile == 'CHS':
            return connectdb("CHS", call_type="popup")
        elif profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return connectdb('Angles', call_type= "popup")
        elif profile in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type= "popup")
 
    def fn_end1_end2(self):

        end1 = self[0]
        print("end1 is {}".format(end1))
        if end1 == 'Fixed':
            return VALUES_END2
        elif end1 == 'Free':
            return ['Fixed']
        elif end1 == 'Hinged':
            return ['Fixed', 'Hinged', 'Roller']
        elif end1 == 'Roller':
            return ['Fixed', 'Hinged']

    def fn_end1_image(self):

        if self == 'Fixed':
            return str(files("osdag.data.ResourceFiles.images").joinpath("6.RRRR.PNG"))
        elif self == 'Free':
            return str(files("osdag.data.ResourceFiles.images").joinpath("1.RRFF.PNG"))
        elif self == 'Hinged':
            return str(files("osdag.data.ResourceFiles.images").joinpath("5.RRRF.PNG"))
        elif self == 'Roller':
            return str(files("osdag.data.ResourceFiles.images").joinpath("4.RRFR.PNG"))

    def fn_end2_image(self):

        end1 = self[0]
        end2 = self[1]
        print("end 1 and end 2 are {}".format(end1, end2))

        if end1 == 'Fixed':
            if end2 == 'Fixed':
                return str(files("osdag.data.ResourceFiles.images").joinpath("6.RRRR.PNG"))
            elif end2 == 'Free':
                return str(files("osdag.data.ResourceFiles.images").joinpath("1.RRFF_rotated.PNG"))
            elif end2 == 'Hinged':
                return str(files("osdag.data.ResourceFiles.images").joinpath("5.RRRF_rotated.PNG"))
            elif end2 == 'Roller':
                return str(files("osdag.data.ResourceFiles.images").joinpath("4.RRFR_rotated.PNG"))
        elif end1 == 'Free':
            return str(files("osdag.data.ResourceFiles.images").joinpath("1.RRFF.PNG"))
        elif end1 == 'Hinged':
            if end2 == 'Fixed':
                return str(files("osdag.data.ResourceFiles.images").joinpath("5.RRRF.PNG"))
            elif end2 == 'Hinged':
                return str(files("osdag.data.ResourceFiles.images").joinpath("3.RFRF.PNG"))
            elif end2 == 'Roller':
                return str(files("osdag.data.ResourceFiles.images").joinpath("2.FRFR_rotated.PNG"))
        elif end1 == 'Roller':
            if end2 == 'Fixed':
                return str(files("osdag.data.ResourceFiles.images").joinpath("4.RRFR.PNG"))
            elif end2 == 'Hinged':
                return str(files("osdag.data.ResourceFiles.images").joinpath("2.FRFR.PNG"))

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t1)

        t2 = ([KEY_END1], KEY_END2, TYPE_COMBOBOX, self.fn_end1_end2)
        lst.append(t2)

        t3 = ([KEY_END1, KEY_END2], KEY_IMAGE, TYPE_IMAGE, self.fn_end2_image)
        lst.append(t3)

        t4 = ([KEY_END1_Y], KEY_END2_Y, TYPE_COMBOBOX, self.fn_end1_end2)
        lst.append(t4)

        t5 = ([KEY_END1_Y, KEY_END2_Y], KEY_IMAGE_Y, TYPE_IMAGE, self.fn_end2_image)
        lst.append(t5)

        t3 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t3)

        # t4 = (KEY_END2, KEY_IMAGE, TYPE_IMAGE, self.fn_end2_image)
        # lst.append(t4)

        return lst

    def output_values(self, flag):

        out_list = []

        t1 = (None, DISP_TITLE_OPTIMUM_SECTION, TYPE_TITLE, None, True)
        out_list.append(t1)

        t1 = (KEY_TITLE_OPTIMUM_DESIGNATION, KEY_DISP_TITLE_OPTIMUM_DESIGNATION, TYPE_TEXTBOX, self.result_designation if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_OPTIMUM_UR_COMPRESSION, KEY_DISP_OPTIMUM_UR_COMPRESSION, TYPE_TEXTBOX, self.result_UR if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_OPTIMUM_SC, KEY_DISP_OPTIMUM_SC, TYPE_TEXTBOX, self.result_section_class if flag else '', True)
        out_list.append(t1)

        t2 = (KEY_EFF_SEC_AREA_ZZ, KEY_DISP_EFF_SEC_AREA_ZZ, TYPE_TEXTBOX, round(self.result_effective_area, 2) if flag else '', True)
        out_list.append(t2)

        t1 = (None, DISP_TITLE_ZZ, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_EFF_LEN_ZZ, KEY_DISP_EFF_LEN_ZZ, TYPE_TEXTBOX, round(self.result_eff_len_zz * 1e-3, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_EULER_BUCKLING_STRESS_ZZ, KEY_DISP_EULER_BUCKLING_STRESS_ZZ, TYPE_TEXTBOX, round(self.result_ebs_zz, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_BUCKLING_CURVE_ZZ, KEY_DISP_BUCKLING_CURVE_ZZ, TYPE_TEXTBOX, self.result_bc_zz if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_IMPERFECTION_FACTOR_ZZ, KEY_DISP_IMPERFECTION_FACTOR_ZZ, TYPE_TEXTBOX, round(self.result_IF_zz, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_SR_FACTOR_ZZ, KEY_DISP_SR_FACTOR_ZZ, TYPE_TEXTBOX, round(self.result_srf_zz, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_NON_DIM_ESR_ZZ, KEY_DISP_NON_DIM_ESR_ZZ, TYPE_TEXTBOX, round(self.result_nd_esr_zz, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_COMP_STRESS_ZZ, KEY_DISP_COMP_STRESS_ZZ, TYPE_TEXTBOX, round(self.result_fcd_1_zz, 2) if flag else '', True)
        out_list.append(t2)

        # t2 = (
        #     KEY_DESIGN_STRENGTH_ZZ, KEY_DISP_DESIGN_STRENGTH_ZZ, TYPE_TEXTBOX, round(self.pd_zz, 2) if flag else '',
        #     True)
        # out_list.append(t2)

        t10 = (None, DISP_TITLE_YY, TYPE_TITLE, None, True)
        out_list.append(t10)

        t2 = (KEY_EFF_LEN_YY, KEY_DISP_EFF_LEN_YY, TYPE_TEXTBOX, round(self.result_eff_len_yy * 1e-3, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_EULER_BUCKLING_STRESS_YY, KEY_DISP_EULER_BUCKLING_STRESS_YY, TYPE_TEXTBOX, round(self.result_ebs_yy, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_BUCKLING_CURVE_YY, KEY_DISP_BUCKLING_CURVE_YY, TYPE_TEXTBOX, self.result_bc_yy if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_IMPERFECTION_FACTOR_YY, KEY_DISP_IMPERFECTION_FACTOR_YY, TYPE_TEXTBOX, round(self.result_IF_yy, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_SR_FACTOR_YY, KEY_DISP_SR_FACTOR_YY, TYPE_TEXTBOX, round(self.result_srf_yy, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_NON_DIM_ESR_YY, KEY_DISP_NON_DIM_ESR_YY, TYPE_TEXTBOX, round(self.result_nd_esr_yy, 2) if flag else '', True)
        out_list.append(t2)

        # t2 = (KEY_EFF_SEC_AREA_YY, KEY_DISP_EFF_SEC_AREA_YY, TYPE_TEXTBOX, round(self.effective_area, 2) if flag else '', True)
        # out_list.append(t2)

        t2 = (KEY_COMP_STRESS_YY, KEY_DISP_COMP_STRESS_YY, TYPE_TEXTBOX, round(self.result_fcd_1_yy, 2) if flag else '', True)
        out_list.append(t2)

        # t2 = (
        # KEY_COMP_STRESS_YY, KEY_DISP_COMP_STRESS_YY, TYPE_TEXTBOX, round(self.result_fcd_1_yy, 2) if flag else '', True)
        # out_list.append(t2)

        # t2 = (
        # KEY_DESIGN_STRENGTH_YY, KEY_DISP_DESIGN_STRENGTH_YY, TYPE_TEXTBOX, round(self.pd_yy, 2) if flag else '', True)
        # out_list.append(t2)

        t1 = (None, KEY_DESIGN_COMPRESSION, TYPE_TITLE, None, True)
        out_list.append(t1)

        t1 = (KEY_MIN_DESIGN_COMP_STRESS, KEY_MIN_DESIGN_COMP_STRESS_VAL, TYPE_TEXTBOX,
              round(min(self.result_fcd_1_yy, self.result_fcd_1_zz), 2) if flag else
              '', True)
        out_list.append(t1)

        t1 = (KEY_MAT_STRESS, KEY_DISP_MAT_STRESS, TYPE_TEXTBOX, round(self.f_cd_2, 2) if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_FCD, KEY_DISP_FCD, TYPE_TEXTBOX, round(self.result_fcd, 2) if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_DESIGN_STRENGTH_COMPRESSION, TYPE_TEXTBOX,
              round(self.result_capacity * 1e-3, 2) if flag else '', True)
        out_list.append(t1)

        return out_list

    def func_for_validation(self, design_dictionary):
        print(f"func_for_validation here")
        all_errors = []
        self.design_status = False
        flag = False
        option_list = self.input_values(self)
        missing_fields_list = []
        #print(f'func_for_validation option_list {option_list}')
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
                    print(option[1], option[2], option[0], design_dictionary[option[0]])
            elif option[2] == TYPE_COMBOBOX and option[0] not in [KEY_SEC_PROFILE, KEY_END1, KEY_END2, KEY_END1_Y, KEY_END2_Y]:
                val = option[3]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])
                    print(option[1], option[2], option[0], design_dictionary[option[0]])

        if len(missing_fields_list) > 0:
            print(design_dictionary)
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        if flag:
            print(f"\n design_dictionary{design_dictionary}")
            self.set_input_values(self, design_dictionary)
            if self.design_status ==False and len(self.failed_design_dict)>0:
                logger.error(
                    "Design Failed, Check Design Report"
                )
                return # ['Design Failed, Check Design Report'] @TODO
            elif self.design_status:
                pass
            else:
                logger.error(
                    "Design Failed. Slender Sections Selected"
                )
                return # ['Design Failed. Slender Sections Selected']
        else:
            return all_errors

    def get_3d_components(self):

        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        # t3 = ('Column', self.call_3DColumn)
        # components.append(t3)

        return components

    # warn if a beam of older version of IS 808 is selected
    def warn_text(self):
        """ give logger warning when a beam from the older version of IS 808 is selected """
        global logger
        red_list = red_list_function()

        if (self.sec_profile == VALUES_SEC_PROFILE[0]):  # Beams and Columns
            for section in self.sec_list:
                if section in red_list:
                    logger.warning(" : You are using a section ({}) (in red color) that is not available in latest version of IS 808".format(section))

    # Setting inputs from the input dock GUI
    def set_input_values(self, design_dictionary):
        super(ColumnDesign, self).set_input_values(self, design_dictionary)

        # section properties
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = 'Columns with known support conditions'
        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]
        self.sec_list = design_dictionary[KEY_SECSIZE]
        self.material = design_dictionary[KEY_SEC_MATERIAL]

        # section user data
        self.length_zz = float(design_dictionary[KEY_UNSUPPORTED_LEN_ZZ])
        self.length_yy = float(design_dictionary[KEY_UNSUPPORTED_LEN_YY])

        # end condition
        self.end_1_z = design_dictionary[KEY_END1]
        self.end_2_z = design_dictionary[KEY_END2]

        self.end_1_y = design_dictionary[KEY_END1_Y]
        self.end_2_y = design_dictionary[KEY_END2_Y]

        # factored loads
        self.load = Load(axial_force=design_dictionary[KEY_AXIAL], shear_force="", moment="", moment_minor="", unit_kNm=True)

        # design preferences
        self.allowable_utilization_ratio = float(design_dictionary[KEY_ALLOW_UR])
        self.effective_area_factor = float(design_dictionary[KEY_EFFECTIVE_AREA_PARA])

        #TODO: @danish this should be handeled dynamically at run-time
        try:
            self.optimization_parameter = design_dictionary[KEY_OPTIMIZATION_PARA]
        except:
            self.optimization_parameter = 'Utilization Ratio'
        # self.allow_class1 = design_dictionary[KEY_ALLOW_CLASS1]
        # self.allow_class2 = design_dictionary[KEY_ALLOW_CLASS2]
        # self.allow_class3 = design_dictionary[KEY_ALLOW_CLASS3]
        # self.allow_class4 = design_dictionary[KEY_ALLOW_CLASS4]
        try:
            self.steel_cost_per_kg = float(design_dictionary[KEY_STEEL_COST])
        except:
            self.steel_cost_per_kg = 50

        self.allowed_sections = ['Plastic', 'Compact', 'Semi-Compact', 'Slender']

        #TODO: @danish check this part if it is needed here
        # if self.allow_class1 == "Yes":
        #     self.allowed_sections.append('Plastic')
        # if self.allow_class2 == "Yes":
        #     self.allowed_sections.append('Compact')
        # if self.allow_class3 == "Yes":
        #     self.allowed_sections.append('Semi-Compact')
        # if self.allow_class4 == "Yes":
        #     self.allowed_sections.append('Slender')

        print(self.allowed_sections)

        print("==================")
        print(self.module)
        print(self.sec_list)
        print(self.sec_profile)
        print(self.material)
        print(self.length_yy)
        print(self.length_zz)
        print(self.load)
        print(self.end_1_z, self.end_2_z)
        print(self.end_1_y, self.end_2_y)
        print("==================")

        # safety factors
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        # print(f"Here[Column/set_input_values/self.gamma_m0{self.gamma_m0}]")
        # material property
        self.material_property = Material(material_grade=self.material, thickness=0)

        # initialize the design status
        self.design_status_list = []
        self.design_status = False
        self.failed_design_dict = {}
        flag = self.section_classification(self)
        print(flag)
        if flag:
            self.design_column(self)
            self.results(self)
        print(f"Here[Column/set_input_values]")

    # Simulation starts here
    def section_classification(self):
        """ Classify the sections based on Table 2 of IS 800:2007 """
        local_flag = True
        self.input_section_list = []
        self.input_section_classification = {} 

        for section in self.sec_list:
            trial_section = section.strip("'")

            # fetching the section properties
            if self.sec_profile == VALUES_SEC_PROFILE[0]:  # Beams and columns
                try:
                    result = Beam(designation=trial_section, material_grade=self.material)
                except:
                    result = Column(designation=trial_section, material_grade=self.material)
                self.section_property = result
            elif self.sec_profile == VALUES_SEC_PROFILE[1]:  # RHS and SHS
                try:
                    result = RHS(designation=trial_section, material_grade=self.material)
                except:
                    result = SHS(designation=trial_section, material_grade=self.material)
                self.section_property = result
            elif self.sec_profile == VALUES_SEC_PROFILE[2]:  # CHS
                self.section_property = CHS(designation=trial_section, material_grade=self.material)
            else:
                self.section_property = Column(designation=trial_section, material_grade=self.material)

            # updating the material property based on thickness of the thickest element
            self.material_property.connect_to_database_to_get_fy_fu(self.material,
                                                                    max(self.section_property.flange_thickness, self.section_property.web_thickness))

            # section classification
            if (self.sec_profile == VALUES_SEC_PROFILE[0]):  # Beams and Columns

                if self.section_property.type == 'Rolled':
                    self.flange_class = IS800_2007.Table2_i((self.section_property.flange_width / 2), self.section_property.flange_thickness,
                                                            self.material_property.fy, self.section_property.type)[0]
                else:
                    self.flange_class = IS800_2007.Table2_i(((self.section_property.flange_width / 2) - (self.section_property.web_thickness / 2)),
                                                            self.section_property.flange_thickness, self.section_property.fy,
                                                            self.section_property.type)[0]

                self.web_class = IS800_2007.Table2_iii((self.section_property.depth - (2 * self.section_property.flange_thickness)),
                                                       self.section_property.web_thickness, self.material_property.fy,
                                                       classification_type='Axial compression')
                web_ratio = (self.section_property.depth - 2 * (
                            self.section_property.flange_thickness + self.section_property.root_radius)) / self.section_property.web_thickness
                flange_ratio = self.section_property.flange_width / 2 / self.section_property.flange_thickness

            elif (self.sec_profile == VALUES_SEC_PROFILE[1]):  # RHS and SHS
                self.flange_class = IS800_2007.Table2_iii((self.section_property.depth - (2 * self.section_property.flange_thickness)),
                                                          self.section_property.flange_thickness, self.material_property.fy,
                                                          classification_type='Axial compression')
                self.web_class = self.flange_class
                web_ratio = (self.section_property.depth - 2 * (
                            self.section_property.flange_thickness + self.section_property.root_radius)) / self.section_property.web_thickness
                flange_ratio = self.section_property.flange_width / 2 / self.section_property.flange_thickness

            elif self.sec_profile == VALUES_SEC_PROFILE[2]:  # CHS
                self.flange_class = IS800_2007.Table2_x(self.section_property.out_diameter, self.section_property.flange_thickness,
                                                        self.material_property.fy, load_type='axial compression')
                self.web_class = self.flange_class  #Why?
                web_ratio = (self.section_property.depth - 2 * (
                            self.section_property.flange_thickness + self.section_property.root_radius)) / self.section_property.web_thickness
                flange_ratio = self.section_property.flange_width / 2 / self.section_property.flange_thickness
                # print(f"self.web_class{self.web_class}")
            
            if self.flange_class == 'Slender' or self.web_class == 'Slender':
                self.section_class = 'Slender'
            else:
                if self.flange_class == 'Plastic' and self.web_class == 'Plastic':
                    self.section_class = 'Plastic'
                elif self.flange_class == 'Plastic' and self.web_class == 'Compact':
                    self.section_class = 'Compact'
                elif self.flange_class == 'Plastic' and self.web_class == 'Semi-Compact':
                    self.section_class = 'Semi-Compact'
                elif self.flange_class == 'Compact' and self.web_class == 'Plastic':
                    self.section_class = 'Compact'
                elif self.flange_class == 'Compact' and self.web_class == 'Compact':
                    self.section_class = 'Compact'
                elif self.flange_class == 'Compact' and self.web_class == 'Semi-Compact':
                    self.section_class = 'Semi-Compact'
                elif self.flange_class == 'Semi-Compact' and self.web_class == 'Plastic':
                    self.section_class = 'Semi-Compact'
                elif self.flange_class == 'Semi-Compact' and self.web_class == 'Compact':
                    self.section_class = 'Semi-Compact'
                elif self.flange_class == 'Semi-Compact' and self.web_class == 'Semi-Compact':
                    self.section_class = 'Semi-Compact'

            # 2.2 - Effective length
            self.effective_length_zz = IS800_2007.cl_7_2_2_effective_length_of_prismatic_compression_members(
                self.length_zz,
                end_1=self.end_1_z,
                end_2=self.end_2_z)

            # self.effective_length_yy = temp_yy * IS800_2007.cl_7_2_4_effective_length_of_truss_compression_members(
            #     self.length_yy,
            #     self.sec_profile) / self.length_yy  # mm
            # print(f"self.effective_length {self.effective_length_yy} ")

            self.effective_length_yy = IS800_2007.cl_7_2_2_effective_length_of_prismatic_compression_members(
                self.length_yy,
                end_1=self.end_1_y,
                end_2=self.end_2_y)

            # self.effective_length_zz = temp_yy * IS800_2007.cl_7_2_4_effective_length_of_truss_compression_members(
            #     self.length_yy,
            #     self.sec_profile) / self.length_yy  # mm
            # print(f"self.effective_length {self.effective_length_zz} ")

            # print("+++++++++++++++++++++++++++++++++++++++++++++++")
            # print(self.end_1_z)
            # print(self.end_2_z)
            # print(self.end_1_y)
            # print(self.end_2_y)
            #
            # print(f"factor y-y {self.effective_length_yy/self.length_yy}")
            # print(f"factor z-z {self.effective_length_yy / self.length_yy}")
            # print("+++++++++++++++++++++++++++++++++++++++++++++++")

            # 2.3 - Effective slenderness ratio
            self.effective_sr_zz = self.effective_length_zz / self.section_property.rad_of_gy_z
            self.effective_sr_yy = self.effective_length_yy / self.section_property.rad_of_gy_y

            limit = IS800_2007.cl_3_8_max_slenderness_ratio(1)
            if self.effective_sr_zz > limit and self.effective_sr_yy > limit:
                logger.warning("Length provided is beyond the limit allowed. [Reference: Cl 3.8, IS 800:2007]")
                logger.error("Cannot compute. Given Length does not pass.")
                local_flag = False
            #else:
            #    logger.info("Length provided is within the limit allowed. [Reference: Cl 3.8, IS 800:2007]")
                

            # if len(self.allowed_sections) == 0:
            #     logger.warning("Select at-least one type of section in the design preferences tab.")
            #     logger.error("Cannot compute. Selected section classification type is Null.")
            #     self.design_status = False
            #     self.design_status_list.append(self.design_status)

            #TODO: @danish check this part
            if self.section_class in self.allowed_sections:
                self.input_section_list.append(trial_section)
                self.input_section_classification.update({trial_section: [self.section_class, self.flange_class, self.web_class, flange_ratio, web_ratio]})
            # print(f"self.section_class{self.section_class}")


        return local_flag

    def design_column(self):
        """ Perform design of column """
        # checking DP inputs
        if (self.allowable_utilization_ratio <= 0.10) or (self.allowable_utilization_ratio > 1.0):
            logger.warning("The defined value of Utilization Ratio in the design preferences tab is out of the suggested range.")
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default value of 1.0.")
            self.allowable_utilization_ratio = 1.0
            self.design_status = False
            self.design_status_list.append(self.design_status)

        if (self.effective_area_factor <= 0.10) or (self.effective_area_factor > 1.0):
            logger.warning("The defined value of Effective Area Factor in the design preferences tab is out of the suggested range.")
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default value of 1.0.")
            self.effective_area_factor = 1.0
            self.design_status = False
            self.design_status_list.append(self.design_status)

        # if (self.steel_cost_per_kg == 0.10) or (self.effective_area_factor > 1.0):
        #     logger.warning("The defined value of the cost of steel (in INR) in the design preferences tab is out of the suggested range.")
        #     logger.info("Provide an appropriate input and re-design.")
        #     logger.info("Assuming a default rate of 50 (INR/kg).")
        #     self.steel_cost_per_kg = 50
        #     self.design_status = False
        #     self.design_status_list.append(self.design_status)
        self.epsilon = math.sqrt(250 / self.material_property.fy)
        #if len(self.input_section_list) > 0:

        # initializing lists to store the optimum results based on optimum UR and cost

        # 1- Based on optimum UR
        self.optimum_section_ur_results = {}
        self.optimum_section_ur = []

        # 2 - Based on optimum cost
        self.optimum_section_cost_results = {}
        self.optimum_section_cost = []
        self.flag = self.section_classification(self)

        print('self.flag:',self.flag)
        # reduction of the area based on the connection requirements (input from design preferences)
        if self.effective_area_factor < 1.0:
            self.effective_area = round(self.effective_area * self.effective_area_factor, 2)

            #logger.warning("Reducing the effective sectional area as per the definition in the Design Preferences tab.")
            #logger.info("The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".
            #            format(round((self.effective_area / self.effective_area_factor), 2), self.effective_area))
        #else:
            #if self.section_class != 'Slender':
            #    logger.info("The effective sectional area is taken as 100% of the cross-sectional area [Reference: Cl. 7.3.2, IS 800:2007].")

        #print('self.input_section_list:',self.input_section_list)
        if self.flag:
            for section in self.input_section_list:  # iterating the design over each section to find the most optimum section

                # fetching the section properties of the selected section
                if self.sec_profile == VALUES_SEC_PROFILE[0]:  # Beams and columns
                    try:
                        result = Beam(designation=section, material_grade=self.material)
                    except:
                        result = Column(designation=section, material_grade=self.material)
                    self.section_property = result
                elif self.sec_profile == VALUES_SEC_PROFILE[1]:  # RHS and SHS
                    try:
                        result = RHS(designation=section, material_grade=self.material)
                    except:
                        result = SHS(designation=section, material_grade=self.material)
                    self.section_property = result

                elif self.sec_profile == VALUES_SEC_PROFILE[2]:  # CHS
                    self.section_property = CHS(designation=section, material_grade=self.material)
                else:   #Why?
                    self.section_property = Column(designation=section, material_grade=self.material)

                self.material_property.connect_to_database_to_get_fy_fu(self.material, max(self.section_property.flange_thickness,
                                                                                        self.section_property.web_thickness))

                

                # initialize lists for updating the results dictionary
                self.list_zz = []
                self.list_yy = []

                self.list_zz.append(section)
                self.list_yy.append(section)

                # Step 1 - computing the effective sectional area
                self.section_class = self.input_section_classification[section][0]

                if self.section_class == 'Slender':
                    #logger.warning("The trial section ({}) is Slender. Computing the Effective Sectional Area as per Sec. 9.7.2, "
                    #            "Fig. 2 (B & C) of The National Building Code of India (NBC), 2016.".format(section))

                    if (self.sec_profile == VALUES_SEC_PROFILE[0]):  # Beams and Columns
                        self.effective_area = (2 * ((31.4 * self.epsilon * self.section_property.flange_thickness) *
                                                    self.section_property.flange_thickness)) + \
                                            (2 * ((21 * self.epsilon * self.section_property.web_thickness) * self.section_property.web_thickness))
                    elif (self.sec_profile == VALUES_SEC_PROFILE[1]):
                        self.effective_area = (2 * 21 * self.epsilon * self.section_property.flange_thickness) * 2
                else:
                    self.effective_area = self.section_property.area  # mm2
                    # print(f"self.effective_area{self.effective_area}")

                self.list_zz.append(self.section_class)
                self.list_yy.append(self.section_class)

                self.list_zz.append(self.effective_area)
                self.list_yy.append(self.effective_area)

                # Step 2 - computing the design compressive stress

                # 2.1 - Buckling curve classification and Imperfection factor
                if (self.sec_profile == VALUES_SEC_PROFILE[0]):  # Beams and Columns

                    if self.section_property.type == 'Rolled':
                        self.buckling_class_zz = IS800_2007.cl_7_1_2_2_buckling_class_of_crosssections(self.section_property.flange_width,
                                                                                                    self.section_property.depth,
                                                                                                    self.section_property.flange_thickness,
                                                                                                    cross_section='Rolled I-sections',
                                                                                                    section_type='Hot rolled')['z-z']
                        self.buckling_class_yy = IS800_2007.cl_7_1_2_2_buckling_class_of_crosssections(self.section_property.flange_width,
                                                                                                    self.section_property.depth,
                                                                                                    self.section_property.flange_thickness,
                                                                                                    cross_section='Rolled I-sections',
                                                                                                    section_type='Hot rolled')['y-y']
                    else:
                        self.buckling_class_zz = IS800_2007.cl_7_1_2_2_buckling_class_of_crosssections(self.section_property.flange_width,
                                                                                                    self.section_property.depth,
                                                                                                    self.section_property.flange_thickness,
                                                                                                    cross_section='Welded I-section',
                                                                                                    section_type='Hot rolled')['z-z']
                        self.buckling_class_yy = IS800_2007.cl_7_1_2_2_buckling_class_of_crosssections(self.section_property.flange_width,
                                                                                                    self.section_property.depth,
                                                                                                    self.section_property.flange_thickness,
                                                                                                    cross_section='Welded I-section',
                                                                                                    section_type='Hot rolled')['y-y']
                else:
                    self.buckling_class_zz = 'a'
                    self.buckling_class_yy = 'a'

                self.imperfection_factor_zz = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class=self.buckling_class_zz)
                self.imperfection_factor_yy = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class=self.buckling_class_yy)

                self.list_zz.append(self.buckling_class_zz)
                self.list_yy.append(self.buckling_class_yy)

                self.list_zz.append(self.imperfection_factor_zz)
                self.list_yy.append(self.imperfection_factor_yy)

                # 2.2 - Effective length
                self.effective_length_zz = IS800_2007.cl_7_2_2_effective_length_of_prismatic_compression_members(self.length_zz ,
                                                                                                                end_1=self.end_1_z,
                                                                                                                end_2=self.end_2_z)  # mm
                self.effective_length_yy = IS800_2007.cl_7_2_2_effective_length_of_prismatic_compression_members(self.length_yy ,
                                                                                                                end_1=self.end_1_y,
                                                                                                                end_2=self.end_2_y)  # mm

                self.list_zz.append(self.effective_length_zz)
                self.list_yy.append(self.effective_length_yy)

                # 2.3 - Effective slenderness ratio
                self.effective_sr_zz = self.effective_length_zz / self.section_property.rad_of_gy_z
                self.effective_sr_yy = self.effective_length_yy / self.section_property.rad_of_gy_y

                self.list_zz.append(self.effective_sr_zz)
                self.list_yy.append(self.effective_sr_yy)

                # 2.4 - Euler buckling stress
                self.euler_bs_zz = (math.pi ** 2 * self.section_property.modulus_of_elasticity) / self.effective_sr_zz ** 2
                self.euler_bs_yy = (math.pi ** 2 * self.section_property.modulus_of_elasticity) / self.effective_sr_yy ** 2

                self.list_zz.append(self.euler_bs_zz)
                self.list_yy.append(self.euler_bs_yy)

                # 2.5 - Non-dimensional effective slenderness ratio
                self.non_dim_eff_sr_zz = math.sqrt(self.material_property.fy / self.euler_bs_zz)
                self.non_dim_eff_sr_yy = math.sqrt(self.material_property.fy / self.euler_bs_yy)
                # print(f"self.non_dim_eff_sr_zz{self.non_dim_eff_sr_yy},self.phi_yy{self.non_dim_eff_sr_yy}/n")

                self.list_zz.append(self.non_dim_eff_sr_zz)
                self.list_yy.append(self.non_dim_eff_sr_yy)

                # 2.5 - phi
                self.phi_zz = 0.5 * (1 + (self.imperfection_factor_zz * (self.non_dim_eff_sr_zz - 0.2)) + self.non_dim_eff_sr_zz ** 2)
                self.phi_yy = 0.5 * (1 + (self.imperfection_factor_yy * (self.non_dim_eff_sr_yy - 0.2)) + self.non_dim_eff_sr_yy ** 2)
                # print(f"self.phi_zz{self.phi_zz},self.phi_yy{self.phi_yy}, self.imperfection_factor_zz{self.imperfection_factor_zz}")

                self.list_zz.append(self.phi_zz)
                self.list_yy.append(self.phi_yy)

                # 2.6 - Design compressive stress
                self.stress_reduction_factor_zz = 1 / (self.phi_zz + (self.phi_zz ** 2 - self.non_dim_eff_sr_zz ** 2) ** 0.5)
                self.stress_reduction_factor_yy = 1 / (self.phi_yy + (self.phi_yy ** 2 - self.non_dim_eff_sr_yy ** 2) ** 0.5)

                self.list_zz.append(self.stress_reduction_factor_zz)
                self.list_yy.append(self.stress_reduction_factor_yy)

                self.f_cd_1_zz = (self.stress_reduction_factor_zz * self.material_property.fy) / self.gamma_m0
                self.f_cd_1_yy = (self.stress_reduction_factor_yy * self.material_property.fy) / self.gamma_m0
                self.f_cd_2 = self.material_property.fy / self.gamma_m0

                self.f_cd_zz = min(self.f_cd_1_zz, self.f_cd_2)
                self.f_cd_yy = min(self.f_cd_1_yy, self.f_cd_2)

                self.f_cd = min(self.f_cd_zz, self.f_cd_yy)

                self.list_zz.append(self.f_cd_1_zz)
                self.list_yy.append(self.f_cd_1_yy)

                self.list_zz.append(self.f_cd_2)
                self.list_yy.append(self.f_cd_2)

                self.list_zz.append(self.f_cd_zz)
                self.list_yy.append(self.f_cd_yy)

                self.list_zz.append(self.f_cd)
                self.list_yy.append(self.f_cd)

                # 2.7 - Capacity of the section

                self.section_capacity = self.f_cd * self.effective_area  # N

                self.list_zz.append(self.section_capacity)
                self.list_yy.append(self.section_capacity)

                # 2.8 - UR
                self.ur = round(self.load.axial_force / self.section_capacity, 3)

                self.list_zz.append(self.ur)
                self.list_yy.append(self.ur)
                self.optimum_section_ur.append(self.ur)

                # 2.9 - Cost of the section in INR
                self.cost = (self.section_property.unit_mass * self.section_property.area * 1e-4) * min(self.length_zz, self.length_yy) * \
                            self.steel_cost_per_kg

                self.list_zz.append(self.cost)
                self.list_yy.append(self.cost)
                self.optimum_section_cost.append(self.cost)
                # print(f"list_zz{list_zz},list_yy{list_yy} ")

                # Step 3 - Storing the optimum results to a list in descending order

                list_1 = ['Designation', 'Section class', 'Effective area', 'Buckling_curve_zz', 'IF_zz', 'Effective_length_zz', 'Effective_SR_zz',
                        'EBS_zz', 'ND_ESR_zz', 'phi_zz', 'SRF_zz', 'FCD_1_zz', 'FCD_2', 'FCD_zz', 'FCD', 'Capacity', 'UR', 'Cost', 'Designation',
                        'Section class', 'Effective area', 'Buckling_curve_yy', 'IF_yy', 'Effective_length_yy', 'Effective_SR_yy', 'EBS_yy',
                        'ND_ESR_yy', 'phi_yy', 'SRF_yy', 'FCD_1_yy', 'FCD_2', 'FCD_yy', 'FCD', 'Capacity', 'UR', 'Cost']

                # 1- Based on optimum UR
                self.optimum_section_ur_results[self.ur] = {}

                list_2 = self.list_zz + self.list_yy
                for j in list_1:
                    # k = 0
                    for k in list_2:
                        self.optimum_section_ur_results[self.ur][j] = k
                        # k += 1
                        list_2.pop(0)
                        break

                # 2- Based on optimum cost
                self.optimum_section_cost_results[self.cost] = {}

                list_2 = self.list_zz + self.list_yy                                  #Why?
                for j in list_1:
                    for k in list_2:
                        self.optimum_section_cost_results[self.cost][j] = k
                        list_2.pop(0)
                        break
        #else:
        #    logger.warning("The section(s) defined for performing the column design is/are not selected based on the selected Inputs and/or "
        #                   "Design Preferences")
        #    logger.error("Cannot compute!")
        #    logger.info("Change the inputs provided and re-design.")
        #    self.design_status = False
        #    self.design_status_list.append(self.design_status)
            # print(f"design_status_list{self.design_status_list}")

    def results(self):
        """ """
        _ = [i for i in self.optimum_section_ur if i > 1.0]
        print( '_ ',_)
        if len(_)==1:
            temp = _[0]
        elif len(_)==0:
            temp = None
        else:
            temp = sorted(_)[0]
        self.failed_design_dict = self.optimum_section_ur_results[temp] if temp is not None else None
        print('self.failed_design_dict ',self.failed_design_dict)
        
        # results based on UR
        if self.optimization_parameter == 'Utilization Ratio':
            filter_UR = filter(lambda x: x <= min(self.allowable_utilization_ratio, 1.0), self.optimum_section_ur)
            self.optimum_section_ur = list(filter_UR)

            self.optimum_section_ur.sort()
            print(f"self.optimum_section_ur{self.optimum_section_ur} \n self.optimum_section_ur_results{self.optimum_section_ur_results}")
            
            # print(f"self.result_UR{self.result_UR}")

            # selecting the section with most optimum UR
            if len(self.optimum_section_ur) == 0:  # no design was successful
                logger.warning("The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                               "criteria")
                logger.error("The solver did not find any adequate section from the defined list.")
                logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                self.design_status = False
                if len(self.failed_design_dict)>0:
                    logger.info(
                    "The details for the best section provided is being shown"
                )
                    self.result_UR = self.failed_design_dict['UR'] #temp  
                    self.common_result(
                        self,
                        list_result=self.failed_design_dict,
                        result_type=None,
                    )
                    logger.warning(
                    "Re-define the list of sections or check the Design Preferences option and re-design."
                )
                    return
                #self.design_status_list.append(self.design_status)

            else:
                self.failed_design_dict = None
                self.result_UR = self.optimum_section_ur[
                    -1
                ]  # optimum section which passes the UR check
                print(f"self.result_UR{self.result_UR}")
                self.design_status = True
                self.common_result(
                    self,
                    list_result=self.optimum_section_ur_results,
                    result_type=self.result_UR,
                )

        else:  # results based on cost
            self.optimum_section_cost.sort()

            # selecting the section with most optimum cost
            self.result_cost = self.optimum_section_cost[0]
            self.design_status = True
        # print results
        #if len(self.optimum_section_ur) == 0:
        #    logger.warning(
        #        "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
        #        "criteria")
        #    logger.error("The solver did not find any adequate section from the defined list.")
        #    logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
        #    self.design_status = False
        #    self.design_status_list.append(self.design_status)
        #    pass
        #else:
        #    if self.optimization_parameter == 'Utilization Ratio':
        #        self.result_designation = self.optimum_section_ur_results[self.result_UR]['Designation']
        #        logger.info("The flange of the section ({}) is {} and web is {}. The section is {} [Reference: Cl 3.7, IS 800:2007].".
        #           format(self.result_designation, 
        #                  self.input_section_classification[self.result_designation][1], round(self.input_section_classification[self.result_designation][3],2), 
        #                  self.input_section_classification[self.result_designation][2], round(self.input_section_classification[self.result_designation][4],2), 
        #                  self.input_section_classification[self.result_designation][0]))
        #        
        #        self.result_section_class = self.optimum_section_ur_results[self.result_UR]['Section class']
        #        self.result_effective_area = self.optimum_section_ur_results[self.result_UR]['Effective area']

        #       self.result_bc_zz = self.optimum_section_ur_results[self.result_UR]['Buckling_curve_zz']
        #        self.result_bc_yy = self.optimum_section_ur_results[self.result_UR]['Buckling_curve_yy']

        #        self.result_IF_zz = self.optimum_section_ur_results[self.result_UR]['IF_zz']
        #        self.result_IF_yy = self.optimum_section_ur_results[self.result_UR]['IF_yy']

        #        self.result_eff_len_zz = self.optimum_section_ur_results[self.result_UR]['Effective_length_zz']
        #        self.result_eff_len_yy = self.optimum_section_ur_results[self.result_UR]['Effective_length_yy']

        #        self.result_eff_sr_zz = self.optimum_section_ur_results[self.result_UR]['Effective_SR_zz']
        #        self.result_eff_sr_yy = self.optimum_section_ur_results[self.result_UR]['Effective_SR_yy']

        #        self.result_ebs_zz = self.optimum_section_ur_results[self.result_UR]['EBS_zz']
        #        self.result_ebs_yy = self.optimum_section_ur_results[self.result_UR]['EBS_yy']

        #        self.result_nd_esr_zz = self.optimum_section_ur_results[self.result_UR]['ND_ESR_zz']
        #        self.result_nd_esr_yy = self.optimum_section_ur_results[self.result_UR]['ND_ESR_yy']

        #        self.result_phi_zz = self.optimum_section_ur_results[self.result_UR]['phi_zz']
        #        self.result_phi_yy = self.optimum_section_ur_results[self.result_UR]['phi_yy']

        #        self.result_srf_zz = self.optimum_section_ur_results[self.result_UR]['SRF_zz']
        #        self.result_srf_yy = self.optimum_section_ur_results[self.result_UR]['SRF_yy']

        #        self.result_fcd_1_zz = self.optimum_section_ur_results[self.result_UR]['FCD_1_zz']
        #        self.result_fcd_1_yy = self.optimum_section_ur_results[self.result_UR]['FCD_1_yy']

        #        self.result_fcd_2 = self.optimum_section_ur_results[self.result_UR]['FCD_2']

        #        self.result_fcd_zz = self.optimum_section_ur_results[self.result_UR]['FCD_zz']
        #        self.result_fcd_yy = self.optimum_section_ur_results[self.result_UR]['FCD_yy']

        #        self.result_fcd = self.optimum_section_ur_results[self.result_UR]['FCD']
        #        self.result_capacity = self.optimum_section_ur_results[self.result_UR]['Capacity']
        #        self.result_cost = self.optimum_section_ur_results[self.result_UR]['Cost']
        #    else:
        #        self.result_UR = self.optimum_section_cost_results[self.result_cost]['UR']

                # checking if the selected section based on cost satisfies the UR
        #        if self.result_UR > min(self.allowable_utilization_ratio, 1.0):

        #            trial_cost = []
        #            for cost in self.optimum_section_cost:
        #                self.result_UR = self.optimum_section_cost_results[cost]['UR']
        #                if self.result_UR <= min(self.allowable_utilization_ratio, 1.0):
        #                    trial_cost.append(cost)

        #            trial_cost.sort()

        #            if len(trial_cost) == 0:  # no design was successful
        #                logger.warning("The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
        #                               "criteria")
        #                logger.error("The solver did not find any adequate section from the defined list.")
        #                logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
        #                self.design_status = False
        #                self.design_status_list.append(self.design_status)
        #                print(f"design_status_list{self.design_status} \n")
        #            else:
        #                self.result_cost = trial_cost[0]  # optimum section based on cost which passes the UR check
        #                self.design_status = True

                # results
        #        self.result_designation = self.optimum_section_cost_results[self.result_cost]['Designation']
        #        self.result_section_class = self.optimum_section_cost_results[self.result_cost]['Section class']
        #        self.result_effective_area = self.optimum_section_cost_results[self.result_cost]['Effective area']

        #        self.result_bc_zz = self.optimum_section_cost_results[self.result_cost]['Buckling_curve_zz']
        #        self.result_bc_yy = self.optimum_section_cost_results[self.result_cost]['Buckling_curve_yy']

        #        self.result_IF_zz = self.optimum_section_cost_results[self.result_cost]['IF_zz']
        #        self.result_IF_yy = self.optimum_section_cost_results[self.result_cost]['IF_yy']

        #        self.result_eff_len_zz = self.optimum_section_cost_results[self.result_cost]['Effective_length_zz']
        #        self.result_eff_len_yy = self.optimum_section_cost_results[self.result_cost]['Effective_length_yy']

        #        self.result_eff_sr_zz = self.optimum_section_cost_results[self.result_cost]['Effective_SR_zz']
        #        self.result_eff_sr_yy = self.optimum_section_cost_results[self.result_cost]['Effective_SR_yy']

        #        self.result_ebs_zz = self.optimum_section_cost_results[self.result_cost]['EBS_zz']
        #        self.result_ebs_yy = self.optimum_section_cost_results[self.result_cost]['EBS_yy']

        #        self.result_nd_esr_zz = self.optimum_section_cost_results[self.result_cost]['ND_ESR_zz']
        #        self.result_nd_esr_yy = self.optimum_section_cost_results[self.result_cost]['ND_ESR_yy']

        #        self.result_phi_zz = self.optimum_section_cost_results[self.result_cost]['phi_zz']
        #        self.result_phi_yy = self.optimum_section_cost_results[self.result_cost]['phi_yy']

        #        self.result_srf_zz = self.optimum_section_cost_results[self.result_cost]['SRF_zz']
        #        self.result_srf_yy = self.optimum_section_cost_results[self.result_cost]['SRF_yy']

        #        self.result_fcd_1_zz = self.optimum_section_cost_results[self.result_cost]['FCD_1_zz']
        #        self.result_fcd_1_yy = self.optimum_section_cost_results[self.result_cost]['FCD_1_yy']

        #        self.result_fcd_2 = self.optimum_section_cost_results[self.result_cost]['FCD_2']

        #        self.result_fcd_zz = self.optimum_section_cost_results[self.result_cost]['FCD_zz']
        #        self.result_fcd_yy = self.optimum_section_cost_results[self.result_cost]['FCD_yy']

        #        self.result_fcd = self.optimum_section_cost_results[self.result_cost]['FCD']
        #        self.result_capacity = self.optimum_section_cost_results[self.result_cost]['Capacity']

        #        print(f"design_status_list2{self.design_status}")
        #
        # end of the design simulation
        # overall design status
        for status in self.design_status_list:
            if status is False:
                self.design_status = False
                break
            else:
                self.design_status = True

        if self.design_status:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall Column design is SAFE")
            logger.info(": ========== End Of Design ============")
        else:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall Column design is UNSAFE")
            logger.info(": ========== End Of Design ============")

    ### start writing save_design from here!
    """def save_design(self, popup_summary):

        if self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                select_section_img = 'SHS'
            elif self.dp_column_designation[1:4] == 'RHS':
                select_section_img = 'RHS'
            else:
                select_section_img = 'CHS'
        else:
            if self.column_properties.flange_slope != 90:
                select_section_img = "Slope_Beam"
            else:
                select_section_img = "Parallel_Beam" """
    
    def common_result(self, list_result, result_type):
        
        self.result_designation = list_result[result_type]['Designation']
        self.section_class = self.input_section_classification[self.result_designation][0]

        if self.section_class == 'Slender':
            logger.warning("The trial section ({}) is Slender. Computing the Effective Sectional Area as per Sec. 9.7.2, "
                        "Fig. 2 (B & C) of The National Building Code of India (NBC), 2016.".format(self.result_designation))
        if self.effective_area_factor < 1.0:
            self.effective_area = round(self.effective_area * self.effective_area_factor, 2)

            logger.warning("Reducing the effective sectional area as per the definition in the Design Preferences tab.")
            logger.info("The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".
                        format(round((self.effective_area / self.effective_area_factor), 2), self.effective_area))
        else:
            if self.section_class != 'Slender':
                logger.info("The effective sectional area is taken as 100% of the cross-sectional area [Reference: Cl. 7.3.2, IS 800:2007].")
        logger.info(
            "The section is {}. The {} section  has  {} flange({}) and  {} web({}).  [Reference: Cl 3.7, IS 800:2007].".format(
                self.input_section_classification[self.result_designation][0] ,
                self.result_designation,
                self.input_section_classification[self.result_designation][1], round(self.input_section_classification[self.result_designation][3],2),
                self.input_section_classification[self.result_designation][2], round(self.input_section_classification[self.result_designation][4],2)
            ))
        
        self.result_section_class = list_result[result_type]['Section class']
        self.result_effective_area = list_result[result_type]['Effective area']
       
        self.result_bc_zz = list_result[result_type]['Buckling_curve_zz'] 
        self.result_bc_yy = list_result[result_type]['Buckling_curve_yy']
    
        self.result_IF_zz = list_result[result_type]['IF_zz']
        self.result_IF_yy = list_result[result_type]['IF_yy']
        
        self.result_eff_len_zz = list_result[result_type]['Effective_length_zz']
        self.result_eff_len_yy = list_result[result_type]['Effective_length_yy']
    
        self.result_eff_sr_zz = list_result[result_type]['Effective_SR_zz']
        self.result_eff_sr_yy = list_result[result_type]['Effective_SR_yy']
        
        self.result_ebs_zz = list_result[result_type]['EBS_zz']
        self.result_ebs_yy = list_result[result_type]['EBS_yy']
    
        self.result_nd_esr_zz = list_result[result_type]['ND_ESR_zz']
        self.result_nd_esr_yy = list_result[result_type]['ND_ESR_yy']
        
        self.result_phi_zz = list_result[result_type]['phi_zz']
        self.result_phi_yy = list_result[result_type]['phi_yy']
        
        self.result_srf_zz = list_result[result_type]['SRF_zz']
        self.result_srf_yy = list_result[result_type]['SRF_yy']
  
        self.result_fcd_1_zz = list_result[result_type]['FCD_1_zz']
        self.result_fcd_1_yy = list_result[result_type]['FCD_1_yy']
        self.result_fcd_2 = list_result[result_type]['FCD_2']
        self.result_fcd_zz = list_result[result_type]['FCD_zz']
        self.result_fcd_yy = list_result[result_type]['FCD_yy']
        self.result_fcd = list_result[result_type]['FCD']

        self.result_capacity = list_result[result_type]['Capacity']
        self.result_cost = list_result[result_type]['Cost']
        

    def save_design(self, popup_summary):

        if (self.design_status and self.failed_design_dict is None) or (not self.design_status and len(self.failed_design_dict)>0):
            if self.sec_profile=='Columns' or self.sec_profile=='Beams' or self.sec_profile == VALUES_SEC_PROFILE[0]:
                self.report_column = {KEY_DISP_SEC_PROFILE: "ISection",
                                    KEY_DISP_SECSIZE: (self.section_property.designation, self.sec_profile),
                                    KEY_DISP_COLSEC_REPORT: self.section_property.designation,
                                    KEY_DISP_MATERIAL: self.section_property.material,
    #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                    KEY_REPORT_MASS: self.section_property.mass,
                                    KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                    KEY_REPORT_DEPTH: self.section_property.depth,
                                    KEY_REPORT_WIDTH: self.section_property.flange_width,
                                    KEY_REPORT_WEB_THK: self.section_property.web_thickness,
                                    KEY_REPORT_FLANGE_THK: self.section_property.flange_thickness,
                                    KEY_DISP_FLANGE_S_REPORT: self.section_property.flange_slope,
                                    KEY_REPORT_R1: self.section_property.root_radius,
                                    KEY_REPORT_R2: self.section_property.toe_radius,
                                    KEY_REPORT_IZ: round(self.section_property.mom_inertia_z * 1e-4, 2),
                                    KEY_REPORT_IY: round(self.section_property.mom_inertia_y * 1e-4, 2),
                                    KEY_REPORT_RZ: round(self.section_property.rad_of_gy_z * 1e-1, 2),
                                    KEY_REPORT_RY: round(self.section_property.rad_of_gy_y * 1e-1, 2),
                                    KEY_REPORT_ZEZ: round(self.section_property.elast_sec_mod_z * 1e-3, 2),
                                    KEY_REPORT_ZEY: round(self.section_property.elast_sec_mod_y * 1e-3, 2),
                                    KEY_REPORT_ZPZ: round(self.section_property.plast_sec_mod_z * 1e-3, 2),
                                    KEY_REPORT_ZPY: round(self.section_property.plast_sec_mod_y * 1e-3, 2)}
            else:
                #Update for section profiles RHS and SHS, CHS by making suitable elif condition.
                self.report_column = {KEY_DISP_COLSEC_REPORT: self.section_property.designation,
                                    KEY_DISP_MATERIAL: self.section_property.material,
                                    #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                    KEY_REPORT_MASS: self.section_property.mass,
                                    KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                    KEY_REPORT_DEPTH: self.section_property.depth,
                                    KEY_REPORT_WIDTH: self.section_property.flange_width,
                                    KEY_REPORT_WEB_THK: self.section_property.web_thickness,
                                    KEY_REPORT_FLANGE_THK: self.section_property.flange_thickness,
                                    KEY_DISP_FLANGE_S_REPORT: self.section_property.flange_slope}


            self.report_input = \
                {#KEY_MAIN_MODULE: self.mainmodule,
                KEY_MODULE: self.module, #"Axial load on column "
                    KEY_DISP_AXIAL: self.load.axial_force * 10 ** -3,
                    KEY_DISP_ACTUAL_LEN_ZZ: self.length_zz,
                    KEY_DISP_ACTUAL_LEN_YY: self.length_yy,
                    KEY_DISP_SEC_PROFILE: self.sec_profile,
                    KEY_DISP_SECSIZE: self.result_section_class,
                    KEY_DISP_END1: self.end_1_z,
                    KEY_DISP_END2: self.end_2_z,
                    KEY_DISP_END1_Y: self.end_1_y,
                    KEY_DISP_END2_Y: self.end_2_y,
                    "Column Section - Mechanical Properties": "TITLE",
                KEY_MATERIAL: self.material,
                    KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.material_property.fu,
                    KEY_DISP_YIELD_STRENGTH_REPORT: self.material_property.fy,
                    KEY_DISP_EFFECTIVE_AREA_PARA: self.effective_area_factor, #To Check
                    KEY_DISP_SECSIZE:  str(self.sec_list),
                    "Selected Section Details": self.report_column,
                }

            self.report_check = []
            t1 = ('Selected', 'Selected Member Data', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
            self.report_check.append(t1)

            self.h = (self.section_property.depth - 2 * (self.section_property.flange_thickness + self.section_property.root_radius))
            self.h_bf_ratio = self.h / self.section_property.flange_width


            # 2.2 CHECK: Buckling Class - Compatibility Check
            t1 = ('SubSection', 'Buckling Class - Compatibility Check', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{2cm}|')
            self.report_check.append(t1)

            # YY axis row
            t1 = (
                "h/bf and tf for YY Axis", 
                comp_column_class_section_check_required(self.h, self.section_property.flange_width, self.section_property.flange_thickness, "YY"),  
                comp_column_class_section_check_provided(self.h, self.section_property.flange_width, self.section_property.flange_thickness, round(self.h_bf_ratio, 2), "YY"), 'Compatible'  
            )
            self.report_check.append(t1)

            # ZZ axis row
            t1 = (
                "h/bf and tf for ZZ Axis", 
                comp_column_class_section_check_required(self.h, self.section_property.flange_width, self.section_property.flange_thickness, "ZZ"), 
                comp_column_class_section_check_provided(self.h, self.section_property.flange_width, self.section_property.flange_thickness, round(self.h_bf_ratio, 2), "ZZ"), 'Compatible'  
            )
            self.report_check.append(t1)

            t1 = ('SubSection', 'Section Classification', '|p{3cm}|p{3.5cm}|p{8.5cm}|p{1cm}|')
            self.report_check.append(t1)
            t1 = ('Web Class', 'Axial Compression',
                    cl_3_7_2_section_classification_web(round(self.h, 2), round(self.section_property.web_thickness, 2), round(self.input_section_classification[self.result_designation][4], 2),
                                            self.epsilon, self.section_property.type,
                                            self.input_section_classification[self.result_designation][2]),
                    ' ')
            self.report_check.append(t1)
            t1 = ('Flange Class', self.section_property.type,
                    cl_3_7_2_section_classification_flange(round(self.section_property.flange_width/2, 2),
                                                        round(self.section_property.flange_thickness, 2),
                                round(self.input_section_classification[self.result_designation][3], 2),
                                                        self.epsilon,
                                                        self.input_section_classification[self.result_designation][1]),
                    ' ')
            self.report_check.append(t1)
            t1 = ('Section Class', ' ',
                    cl_3_7_2_section_classification(
                                                        self.input_section_classification[self.result_designation][0]),
                    ' ')
            self.report_check.append(t1)
            

            t1 = ('NewTable', 'Imperfection Factor', '|p{3cm}|p{5 cm}|p{5cm}|p{3 cm}|')
            self.report_check.append(t1)

            t1 = (
                'YY',
                self.list_yy[3].upper(),
                self.list_yy[4], ''
            )
            self.report_check.append(t1)

            t1 = (
                'ZZ',
                self.list_zz[3].upper(),
                self.list_zz[4], ''
            )
            self.report_check.append(t1)


            K_yy = self.result_eff_len_yy / self.length_yy
            K_zz= self.result_eff_len_zz / self.length_zz
            t1 = ('SubSection', 'Slenderness Ratio', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
            self.report_check.append(t1)
            t1 = ("Effective Slenderness Ratio (For YY Axis)", ' ',
                                cl_7_1_2_effective_slenderness_ratio(K_yy,self.length_yy, self.section_property.rad_of_gy_y, round(self.result_eff_sr_yy, 2)),
                                ' ')
            self.report_check.append(t1)
            t1 = ("Effective Slenderness Ratio (For ZZ Axis)", ' ',
                                cl_7_1_2_effective_slenderness_ratio(K_zz,self.length_zz, self.section_property.rad_of_gy_z, round(self.result_eff_sr_zz, 2)),
                                ' ')
            self.report_check.append(t1)



            t1 = ('SubSection', 'Checks', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
            self.report_check.append(t1)
                            
            t1 = (r'$\phi_{yy}$', ' ',
                cl_8_7_1_5_phi(self.result_IF_yy, round(self.non_dim_eff_sr_yy, 2), round(self.result_phi_yy, 2)),
                ' ')
            self.report_check.append(t1)

            t1 = (r'$\phi_{zz}$', ' ',
                cl_8_7_1_5_phi(self.result_IF_zz, round(self.non_dim_eff_sr_zz, 2), round(self.result_phi_zz, 2)),
                ' ')
            self.report_check.append(t1)

            t1 = (r'$F_{cd,yy} \, \left( \frac{N}{\text{mm}^2} \right)$', ' ',
                cl_8_7_1_5_Buckling(self.material_property.fy, self.gamma_m0, round(self.non_dim_eff_sr_yy, 2), round(self.result_phi_yy, 2), round(self.result_fcd_2, 2), round(self.result_fcd_yy, 2)),
                ' ')
            self.report_check.append(t1)

            t1 = (r'$F_{cd,zz} \, \left( \frac{N}{\text{mm}^2} \right)$', ' ',
                cl_8_7_1_5_Buckling(self.material_property.fy, self.gamma_m0, round(self.non_dim_eff_sr_zz, 2), round(self.result_phi_zz, 2), round(self.result_fcd_2, 2), round(self.result_fcd_zz, 2)),
                ' ')
            self.report_check.append(t1)

            t1 = (r'Design Compressive Strength (\( P_d \)) (For the most critical value of \( F_{cd} \))', self.load.axial_force * 10 ** -3,
                        cl_7_1_2_design_compressive_strength(round(self.result_capacity / 1000, 2), self.section_property.area, round(self.result_fcd, 2),self.load.axial_force * 10 ** -3),
                        get_pass_fail(self.load.axial_force * 10 ** -3, round(self.result_capacity, 2), relation="leq"))
            self.report_check.append(t1)

        else:
            self.report_input = \
                {#KEY_MAIN_MODULE: self.mainmodule,
                KEY_MODULE: self.module, #"Axial load on column "
                    KEY_DISP_AXIAL: self.load.axial_force * 10 ** -3,
                    KEY_DISP_ACTUAL_LEN_ZZ: self.length_zz,
                    KEY_DISP_ACTUAL_LEN_YY: self.length_yy,
                    KEY_DISP_SEC_PROFILE: self.sec_profile,
                    KEY_DISP_SECSIZE:  str(self.sec_list),
                    #KEY_DISP_SECSIZE: self.result_section_class,
                    KEY_DISP_END1: self.end_1_z,
                    KEY_DISP_END2: self.end_2_z,
                    KEY_DISP_END1_Y: self.end_1_y,
                    KEY_DISP_END2_Y: self.end_2_y,
                    "Column Section - Mechanical Properties": "TITLE",
                KEY_MATERIAL: self.material,
                    KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.material_property.fu,
                    KEY_DISP_YIELD_STRENGTH_REPORT: self.material_property.fy,
                    KEY_DISP_EFFECTIVE_AREA_PARA: self.effective_area_factor, #To Check
                    
                    # "Failed Section Details": self.report_column,
                }
            self.report_check = []

            t1 = ('Selected', 'All Members Failed', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
            self.report_check.append(t1)


        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"

        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = os.path.abspath(".") # TEMP
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                              rel_path, Disp_2d_image, Disp_3D_image, module=self.module) 
        