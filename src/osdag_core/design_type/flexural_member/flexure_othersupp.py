"""

@Author:    Rutvik Joshi - Osdag Team, IIT Bombay [(P) rutvikjoshi63@gmail.com / 30005086@iitb.ac.in]

@Module - Beam Design - Other Supports
           - Laterally Supported Beam [Moment + Shear]
           - Laterally Unsupported Beam [Moment + Shear]


@Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               4) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

other          8)
references     9)

"""
import logging
import math
import numpy as np
from ...Common import *
# from ..connection.moment_connection import MomentConnection
from ...utils.common.material import *
from ...utils.common.load import Load
from ...utils.common.component import ISection, Material
from ...utils.common.component import *
from ..member import Member
from ...Report_functions import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...utils.common.common_calculation import *
from ..tension_member import *
from ...utils.common.Section_Properties_Calculator import BBAngle_Properties
from ...utils.common import is800_2007
from ...utils.common.component import *


class Flexure_Misc(Member):

    def __init__(self):
        # print(f"Here10")
        super(Flexure_Misc, self).__init__()

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

        t2 = ("Optimization", TYPE_TAB_2, self.optimization_tab_flexure_design)
        tabs.append(t2)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):
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

        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])#Need to check
        design_input.append(t1)

        t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY])
        design_input.append(t1)

        t2 = ("Optimization", TYPE_TEXTBOX, [ KEY_EFFECTIVE_AREA_PARA, KEY_LENGTH_OVERWRITE, KEY_BEARING_LENGTH]) #, KEY_STEEL_COST
        design_input.append(t2)

        t2 = ("Optimization", TYPE_COMBOBOX, [KEY_ALLOW_CLASS, KEY_LOAD, KEY_ShearBucklingOption]) #, KEY_STEEL_COST
        design_input.append(t2)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        return design_input

    def input_dictionary_without_design_pref(self):

        design_input = []

        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_ALLOW_CLASS, KEY_EFFECTIVE_AREA_PARA, KEY_LENGTH_OVERWRITE,KEY_BEARING_LENGTH, KEY_LOAD, KEY_DP_DESIGN_METHOD, KEY_ShearBucklingOption], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):

        add_buttons = []

        t2 = (KEY_DISP_COLSEC, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE, None, None, "Columns")
        add_buttons.append(t2)

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
            KEY_ALLOW_CLASS: 'Yes',
            KEY_EFFECTIVE_AREA_PARA: '1.0',
            KEY_LENGTH_OVERWRITE :'NA',
            KEY_BEARING_LENGTH : 'NA',
            KEY_LOAD : 'Normal',
            KEY_DP_DESIGN_METHOD: "Limit State Design",
            KEY_ShearBucklingOption: KEY_DISP_SB_Option[0],
        }[key]

        return val

    ####################################
    # Design Preference Functions End
    ####################################

    # Setting up logger and Input and Output Docks
    ####################################
    def module_name(self):
        return KEY_DISP_FLEXURE3

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
        '''
        TODO : Make seperate sub-functions to add??
            At support & At Top restraints should be inactive
            Depending on Support Conditions : if cantilever  then active and Torsional &
            Warping Restraint be inactive.

        '''

        self.module = KEY_DISP_FLEXURE3
        options_list = []

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t1 = (KEY_MODULE, KEY_DISP_FLEXURE3, TYPE_MODULE, None, True, "No Validator")
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, VALUES_SEC_PROFILE3, True, 'No Validator') #'Beam and Column'
        options_list.append(t2)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator')
        options_list.append(t4)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)

        t1 = (None, KEY_SECTION_DATA, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (
            KEY_DESIGN_TYPE_FLEXURE,
            KEY_BEAM_SUPP_TYPE,
            TYPE_COMBOBOX,
            VALUES_SUPP_TYPE_temp,
            True,
            "No Validator",
        )
        options_list.append(t2)

        #
        # t3 = (KEY_BENDING, KEY_DISP_BENDING, TYPE_COMBOBOX, VALUES_BENDING_TYPE, False, 'No Validator')
        # options_list.append(t3)
        #
        #
        t4 = (KEY_SUPPORT, KEY_DISP_SUPPORT, TYPE_NOTE,KEY_DISP_SUPPORT2, True, 'No Validator')
        options_list.append(t4)

        t12 = (KEY_IMAGE, None, TYPE_IMAGE, Simply_Supported_img, True, 'No Validator')
        options_list.append(t12)

        t10 = (KEY_TORSIONAL_RES, DISP_TORSIONAL_RES, TYPE_COMBOBOX, Torsion_Restraint_list, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_WARPING_RES, DISP_WARPING_RES, TYPE_COMBOBOX, Warping_Restraint_list, True, 'No Validator')
        options_list.append(t11)

        t11 = (KEY_SUPPORT_TYPE, DISP_SUPPORT_RES, TYPE_COMBOBOX, Supprt_Restraint_list, True, 'No Validator')
        options_list.append(t11)

        t11 = (KEY_SUPPORT_TYPE2, DISP_TOP_RES, TYPE_COMBOBOX, Top_Restraint_list, False, 'No Validator')
        options_list.append(t11)

        t5 = (KEY_LENGTH, KEY_DISP_LENGTH_BEAM, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        t8 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)



        return options_list

    def fn_profile_section(self):

        profile = self[0]
        if profile == 'Beams': #Beam and Column
            return connectdb("Beams", call_type="popup")
            profile2 = connectdb("Columns", call_type="popup")
        if profile == 'Columns': #Beam and Column
            return connectdb("Columns", call_type="popup")
            # profile2 = connectdb("Columns", call_type="popup")
        # return list(set(profile1 + profile2))


    def fn_supp_image(self):
        print( 'Inside fn_supp_image', self)
        if self[0] == KEY_DISP_SUPPORT1:
            return Simply_Supported_img
        else:
            return Cantilever_img

    def axis_bending_change(self):
        design = self[0]
        print( 'Inside fn_supp_image', self)
        if self[0] == KEY_DISP_DESIGN_TYPE_FLEXURE:
            return ['NA']
        else:
            return VALUES_BENDING_TYPE

    # def show_error_message(self):
    #     QMessageBox.about(self, 'information', "Your message!")
    def input_value_changed(self):

        lst = []

        t1 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t1)

        # t3 = ([KEY_SUPPORT], KEY_IMAGE, TYPE_IMAGE, self.fn_supp_image)
        # lst.append(t3)

        # t3 = ([KEY_DESIGN_TYPE_FLEXURE], KEY_BENDING, TYPE_COMBOBOX, self.axis_bending_change)
        # lst.append(t3)

        t3 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t3)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               'After checking Non-dimensional slenderness ratio for given section, some sections maybe be ignored by Osdag.[Ref IS 8.2.2] ', TYPE_WARNING, self.major_bending_warning)
        lst.append(t18)

        return lst

    def major_bending_warning(self):

        if self[0] == VALUES_SUPP_TYPE_temp[2]:
            return True
        else:
            return False

    def output_values(self, flag):

        out_list = []

        t1 = (None, DISP_TITLE_STRUT_SECTION, TYPE_TITLE, None, True)

        out_list.append(t1)

        t1 = (KEY_TITLE_OPTIMUM_DESIGNATION, KEY_DISP_TITLE_OPTIMUM_DESIGNATION, TYPE_TEXTBOX,
              self.result_designation if flag else '', True)
        out_list.append(t1)

        t1 = (
        KEY_OPTIMUM_UR_COMPRESSION, KEY_DISP_OPTIMUM_UR_COMPRESSION, TYPE_TEXTBOX, self.result_UR if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_OPTIMUM_SC, KEY_DISP_OPTIMUM_SC, TYPE_TEXTBOX, self.result_section_class if flag else '', True)
        out_list.append(t1)


        t2 = (KEY_betab_constatnt, KEY_DISP_betab_constatnt, TYPE_TEXTBOX,
              self.result_betab if flag else '', True)
        out_list.append(t2)


        t2 = (
        KEY_EFF_SEC_AREA, KEY_DISP_EFF_SEC_AREA, TYPE_TEXTBOX, self.result_effective_area if flag else '',
        True)
        out_list.append(t2)

        t2 = (KEY_EFF_LEN, KEY_DISP_EFF_LEN, TYPE_TEXTBOX, self.result_eff_len if flag else '',
              True)
        out_list.append(t2)

        t1 = (None, KEY_DESIGN_COMPRESSION, TYPE_TITLE, None, True)
        out_list.append(t1)

        t1 = (KEY_SHEAR_STRENGTH, KEY_DISP_DESIGN_STRENGTH_SHEAR, TYPE_TEXTBOX,
              self.result_shear  if flag else
              '', True)
        out_list.append(t1)
        #
        t1 = (KEY_MOMENT_STRENGTH, KEY_DISP_DESIGN_STRENGTH_MOMENT, TYPE_TEXTBOX,
              self.result_bending  if flag else
              '', True)
        out_list.append(t1)

        t1 = (KEY_BUCKLING_STRENGTH, KEY_DISP_BUCKLING_STRENGTH, TYPE_TEXTBOX,
              self.result_capacity if flag else
              '', True)
        out_list.append(t1)
        t1 = (KEY_WEB_CRIPPLING, KEY_DISP_CRIPPLING_STRENGTH, TYPE_TEXTBOX,
              self.result_crippling if flag else
              '', True)
        out_list.append(t1)

        t1 = (KEY_HIGH_SHEAR, KEY_DISP_HIGH_SHEAR, TYPE_TEXTBOX,
              self.result_high_shear if flag else
              '', True)
        out_list.append(t1)


        t1 = (None, KEY_DISP_LTB, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_T_constatnt, KEY_DISP_T_constatnt, TYPE_TEXTBOX,
              self.result_tc if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_W_constatnt, KEY_DISP_W_constatnt, TYPE_TEXTBOX, self.result_wc if flag else '', True)
        out_list.append(t2)

        t2 = (
            KEY_IMPERFECTION_FACTOR_LTB, KEY_DISP_IMPERFECTION_FACTOR, TYPE_TEXTBOX, self.result_IF_lt if flag else '',
            True)
        out_list.append(t2)

        t2 = (KEY_SR_FACTOR_LTB, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, self.result_srf_lt if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_NON_DIM_ESR_LTB, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, self.result_nd_esr_lt if flag else '', True)
        out_list.append(t2)

        t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_COMP_STRESS, TYPE_TEXTBOX,
              self.result_nd_esr_lt if flag else
              '', True)
        out_list.append(t1)

        t2 = (KEY_Elastic_CM, KEY_DISP_Elastic_CM, TYPE_TEXTBOX, self.result_mcr if flag else '', True)
        out_list.append(t2)

        t1 = (None, KEY_WEB_BUCKLING, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_ESR, KEY_DISP_ESR, TYPE_TEXTBOX, self.result_eff_sr if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_EULER_BUCKLING_STRESS, KEY_DISP_EULER_BUCKLING_STRESS, TYPE_TEXTBOX,
              self.result_ebs if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_BUCKLING_CURVE, KEY_DISP_BUCKLING_CURVE, TYPE_TEXTBOX, self.result_bc if flag else '', True)
        out_list.append(t2)

        t2 = (
        KEY_IMPERFECTION_FACTOR, KEY_DISP_IMPERFECTION_FACTOR, TYPE_TEXTBOX, self.result_IF if flag else '',
        True)
        out_list.append(t2)

        t2 = (KEY_SR_FACTOR, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, self.result_srf if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_NON_DIM_ESR, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, self.result_nd_esr if flag else '', True)
        out_list.append(t2)



        return out_list

    def func_for_validation(self, design_dictionary):
        print(f"func_for_validation here")
        all_errors = []
        self.design_status = False
        flag = False
        flag1 = False
        flag2 = False
        flag3 = False
        option_list = self.input_values(self)
        missing_fields_list = []
        print(f'func_for_validation option_list {option_list}'
            f"\n  design_dictionary {design_dictionary}"
              )
        for option in option_list:
            if option[2] == TYPE_TEXTBOX or option[0] == KEY_LENGTH or option[0] == KEY_SHEAR or option[0] == KEY_MOMENT:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
                    continue
                if option[0] == KEY_LENGTH:
                    if float(design_dictionary[option[0]]) <= 0.0:
                        print("Input value(s) cannot be equal or less than zero.")
                        error = "Input value(s) cannot be equal or less than zero."
                        all_errors.append(error)
                    else:
                        flag1 = True
                elif option[0] == KEY_SHEAR:
                    if float(design_dictionary[option[0]]) <= 0.0:
                        print("Input value(s) cannot be equal or less than zero.")
                        error = "Input value(s) cannot be equal or less than zero."
                        all_errors.append(error)
                    else:
                        flag2 = True
                elif option[0] == KEY_MOMENT:
                    if float(design_dictionary[option[0]]) <= 0.0:
                        print("Input value(s) cannot be equal or less than zero.")
                        error = "Input value(s) cannot be equal or less than zero."
                        all_errors.append(error)
                    else:
                        flag3 = True
            # elif option[2] == TYPE_COMBOBOX and option[0] not in [KEY_SEC_PROFILE, KEY_END1, KEY_END2, KEY_DESIGN_TYPE_FLEXURE, KEY_BENDING, KEY_SUPPORT]:
            #     val = option[3]
            #     if design_dictionary[option[0]] == val[0]:
            #         missing_fields_list.append(option[1])


        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
        else:
            flag = True

        if flag and flag1 and flag2 and flag3:
            print(f"\n design_dictionary{design_dictionary}")
            self.set_input_values(self, design_dictionary)
        else:
            return all_errors

    def get_3d_components(self):

        components = []

        # t3 = ('Column', self.call_3DColumn)
        # components.append(t3)

        return components

    # warn if a beam of older version of IS 808 is selected
    def warn_text(self):
        """ give logger warning when a beam from the older version of IS 808 is selected """
        global logger
        red_list = red_list_function()

        if (self.sec_profile == VALUES_SEC_PROFILE[0]) or (self.sec_profile == VALUES_SEC_PROFILE[1]):  # Beams or Columns
            for section in self.sec_list:
                if section in red_list:
                    logger.warning(" : You are using a section ({}) (in red color) that is not available in latest version of IS 808".format(section))

    # Setting inputs from the input dock GUI
    def set_input_values(self, design_dictionary):
        '''
        TODO
                self.bending_type == KEY_DISP_BENDING1:
                self.lambda_lt = self.lambda_lt_check_member_type
                if self.lambda_lt < 0.4:
                    self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE
        '''
        super(Flexure_Misc, self).set_input_values(self, design_dictionary)

        # section properties
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = 'Flexure Member'
        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]
        self.sec_list = design_dictionary[KEY_SECSIZE]
        print(f"\n Inside set_input_values{self.sec_profile}")
        print(f"\n sec_profile{self.sec_list}")
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.material = design_dictionary[KEY_SEC_MATERIAL]

        # design type
        self.design_type_temp = design_dictionary[KEY_DESIGN_TYPE_FLEXURE]  # or KEY_DISP_DESIGN_TYPE2_FLEXURE
        self.latex_design_type = design_dictionary[KEY_DESIGN_TYPE_FLEXURE]  # or KEY_DISP_DESIGN_TYPE2_FLEXURE
        if self.design_type_temp == VALUES_SUPP_TYPE_temp[0]:
            self.design_type = VALUES_SUPP_TYPE[0]  # or KEY_DISP_DESIGN_TYPE2_FLEXURE
            self.support_cndition_shear_buckling = design_dictionary[KEY_ShearBucklingOption]
        elif self.design_type_temp == VALUES_SUPP_TYPE_temp[1]:
            self.design_type = VALUES_SUPP_TYPE[0]
            # self.bending_type = KEY_DISP_BENDING2 #if design_dictionary[KEY_BENDING] != 'Disabled' else 'NA'
        elif self.design_type_temp == VALUES_SUPP_TYPE_temp[2]:
            self.design_type = VALUES_SUPP_TYPE[1]
            self.bending_type = KEY_DISP_BENDING1

        # section user data
        self.length = float(design_dictionary[KEY_LENGTH])

        # end condition
        self.support = design_dictionary[KEY_SUPPORT]

        # factored loads
        self.load = Load(
            shear_force=design_dictionary[KEY_SHEAR],
            axial_force="",
            moment=design_dictionary[KEY_MOMENT],
            unit_kNm=True,
        )

        # design preferences
        # self.allowable_utilization_ratio = float(design_dictionary[KEY_ALLOW_UR])
        self.latex_efp = design_dictionary[KEY_LENGTH_OVERWRITE]
        self.effective_area_factor = float(design_dictionary[KEY_EFFECTIVE_AREA_PARA])
        self.allowable_utilization_ratio = 1.0
        self.optimization_parameter = "Utilization Ratio"
        self.allow_class = design_dictionary[KEY_ALLOW_CLASS]  # if 'Semi-Compact' is available
        self.steel_cost_per_kg = 50
        # Step 2 - computing the design compressive stress for web_buckling & web_crippling
        self.bearing_length = design_dictionary[KEY_BEARING_LENGTH]
        #TAKE from Design Dictionary
        self.allowed_sections = []
        if self.allow_class == "Yes":
            self.allowed_sections == "Semi-Compact"

        print(f"self.allowed_sections {self.allowed_sections}")
        print("==================")
        # print(f"self.load_type {self.load_type}")

        print(f"self.module{self.module}")
        print(f"self.sec_list {self.sec_list}")
        print(f"self.material {self.material}")
        print(f"self.length {self.length}")
        print(f"self.load {self.load}")
        print("==================")

        # safety factors
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        self.gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]["ultimate_stress"]
        self.material_property = Material(material_grade=self.material, thickness=0)
        self.fyf = self.material_property.fy
        self.fyw = self.material_property.fy

        print(f"self.material_property {self.material_property}]")
        # print( "self.material_property",self.material_property.fy)
        # initialize the design status
        self.design_status_list = []
        self.design_status = False
        self.sec_prop_initial_dict = {}

        self.design(self, design_dictionary)
        if len(self.input_modified) != 0:
            self.results(self, design_dictionary)


    # Simulation starts here
    def design(self, design_dictionary, flag=0):
        '''
        TODO optimimation_tab_check changes to include self.material_property = Material(material_grade=self.material, thickness=0)
            for each section
        '''
        # flag = self.section_classification(self)
        print(f"\n Inside design")
        # self.show_error_message(self)
        """Perform design of struct"""
        # checking DP inputs

        self.optimization_tab_check(self)
        # print( "self.material_property",self.material_property.fy)
        self.input_modifier(self)
        # print( "self.material_property",self.material_property.fy)
        if len(self.input_modified) != 0:
            self.design_beam(self, design_dictionary)

    def optimization_tab_check(self):
        '''
        TODO add button to give user option to take Tension holes or not
        '''
        print(f"\n Inside optimization_tab_check")
        if (self.effective_area_factor <= 0.10) or (self.effective_area_factor > 1.0):
            logger.error(
                "The defined value of Effective Area Factor in the design preferences tab is out of the suggested range."
            )
            logger.info("Provide an appropriate input and re-design.")
            logger.warning("Assuming a default value of 1.0.")
            self.effective_area_factor = 1.0
            # self.design_status = False
            # self.design_status_list.append(self.design_status)
            self.optimization_tab_check(self)
        elif (self.steel_cost_per_kg < 0.10) or (self.effective_area_factor > 1.0):
            # No suggested range in Description
            logger.warning(
                "The defined value of the cost of steel (in INR) in the design preferences tab is out of the suggested range."
            )
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default rate of 50 (INR/kg).")
            self.steel_cost_per_kg = 50
            self.design_status = False
            self.design_status_list.append(self.design_status)
        else:
            if self.effective_area_factor >= (self.material_property.fy * self.gamma_m0 / (self.material_property.fu * 0.9 * self.gamma_m1)):
                pass
            else:
                self.effective_area_factor = (
                    self.material_property.fy
                    * self.gamma_m0
                    / (self.material_property.fu * 0.9 * self.gamma_m1)
                )
                logger.info(
                    f"The effect of holes in the tension flange is considered on the design bending strength. The ratio of net to gross area of the flange in tension is considered {self.effective_area_factor}"
                )

            logger.info("Provided appropriate design preference, now checking input.")

    def input_modifier(self):
        """Classify the sections based on Table 2 of IS 800:2007"""
        print(f"Inside input_modifier")
        local_flag = True
        self.input_modified = []
        self.input_section_list = []
        # self.input_section_classification = {}

        for section in self.sec_list:
            section = section.strip("'")
            self.section_property = self.section_conect_database(self, section)

            Zp_req = self.load.moment * self.gamma_m0 / self.material_property.fy
            print('Inside input_modifier not allow_class',self.allow_class,self.load.moment, self.gamma_m0, self.material_property.fy)
            if self.section_property.plast_sec_mod_z >= Zp_req:
                self.input_modified.append(section)
                # logger.info(
                #     f"Required Zp_req = {round(Zp_req * 10**-3,2)} x 10^3 mm^3 and Zp of section {self.section_property.designation} = {round(self.section_property.plast_sec_mod_z* 10**-3,2)} x 10^3 mm^3.Section satisfy Min Zp_req value")
            else:
                pass
                # logger.warning(
                #     f"Required Zp_req = {round(Zp_req* 10**-3,2)} x 10^3 mm^3 and Zp of section {self.section_property.designation} = {round(self.section_property.plast_sec_mod_z* 10**-3,2)} x 10^3 mm^3.Section dosen't satisfy Min Zp_req value")
        print("self.input_modified", self.input_modified)

    def section_conect_database(self, section):
        print(f"section_conect_database{section}")
        print(section)
        # print(self.sec_profile)
        if (
            self.sec_profile == VALUES_SECTYPE[1]
            or self.sec_profile == VALUES_SECTYPE[2]
            or self.sec_profile == "I-section"
        ):  # I-section
            self.section_property = ISection(
                designation=section, material_grade=self.material
            )
            self.material_property.connect_to_database_to_get_fy_fu(
                self.material, max(self.section_property.flange_thickness, max(self.section_property.web_thickness, self.section_property.flange_thickness))
            )
            print(f"section_conect_database material_property.fy{self.material_property.fy}")
            self.epsilon = math.sqrt(250 / self.material_property.fy)
        return self.section_property

    def design_beam(self, design_dictionary):
        print(f"Inside design_beam")
        # 1- Based on optimum UR
        self.optimum_section_ur_results = {}
        self.optimum_section_ur = []

        # 2 - Based on optimum cost
        self.optimum_section_cost_results = {}
        self.optimum_section_cost = []

        # 1 - section classification
        flag = self.section_classification(self)
        if self.effective_area_factor < 1.0:
            logger.warning(
                "Reducing the effective sectional area as per the definition in the Design Preferences tab."
            )
        else:
            logger.info(
                "The effective sectional area is taken as 100% of the cross-sectional area [Reference: Cl. 7.3.2, IS 800:2007]."
            )
        # 2 - Effective length
        self.effective_length_beam(self, design_dictionary, self.length)  # mm
        print(
            f"self.effective_length {self.effective_length} \n self.input_section_classification{self.input_section_classification} ")

        if flag:
            for section in self.input_section_list:
                # initialize lists for updating the results dictionary
                self.section_property = self.section_conect_database(self, section)

                # Step 1.1 - computing the effective sectional area
                self.effective_area = self.section_property.area
                self.common_checks_1(self, section, step=2)


                list_result = []
                list_1 = []
                list_result.append(section)
                self.section_class = self.input_section_classification[section][0]

                if self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE:
                    self.laterally_supported(self)
                    if self.web_buckling_check:
                        continue
                else:
                    self.web_not_buckling_steps(self)
                print(f"Common result {list_result, self.section_class, self.V_d, self.high_shear_check, self.bending_strength_section}")

                # 2.8 - UR
                self.ur = round(
                    max((self.load.moment / self.bending_strength_section * 10 ** -6),(self.load.shear_force / self.V_d * 10 ** -3)),
                    2)  # ( +  round(self.load.axial_force / self.section_capacity, 3)
                print("UR", self.ur)
                # 2.9 - Cost of the section in INR
                self.cost = (
                        (
                                self.section_property.unit_mass
                                * self.section_property.area
                                * 1e-4
                        )
                        * self.length
                        * self.steel_cost_per_kg
                )
                self.optimum_section_cost.append(self.cost)



                if self.bearing_length != 'NA': #and self.web_crippling
                    print(f"Check for Web Buckling")
                    try:
                        self.bearing_length = float(design_dictionary[KEY_BEARING_LENGTH])
                        self.web_buckling = True #WEB BUCKLING
                        I_eff_web = self.bearing_length * self.section_property.web_thickness ** 3 / 12
                        A_eff_web = self.bearing_length * self.section_property.web_thickness
                        r = math.sqrt(I_eff_web / A_eff_web)
                        d_red = (self.section_property.depth - 2*(self.section_property.flange_thickness + self.section_property.root_radius))
                        self.slenderness = 0.7 * d_red / r
                        self.common_checks_1(self, section, step=3)
                        # step == 4
                        self.common_checks_1(
                            self, section, step=4, list_result=["Concentric"]
                        )
                        # 2.7 - Capacity of the section for web_buckling
                        self.section_capacity = (
                                self.design_compressive_stress * (self.bearing_length + self.section_property.depth / 2) * self.section_property.web_thickness
                                * 10**-3)  # N
                        print(self.design_compressive_stress, self.bearing_length, self.section_property.depth, self.section_property.web_thickness)

                        print(self.bending_strength_section, self.V_d, self.section_capacity)

                        self.F_wb = (self.bearing_length + 2.5 * (self.section_property.root_radius + self.section_property.flange_thickness)) * self.section_property.web_thickness * self.material_property.fy / (self.gamma_m0 * 10**3)
                        if self.bending_strength_section > self.load.moment* 10**-6 and self.V_d > self.load.shear_force * 10**-3 and self.section_capacity > self.load.shear_force * 10**-3 and self.F_wb > self.load.shear_force* 10**-3:
                            list_result, list_1 = self.list_changer(self,change='Web Buckling',check=True,list=list_result, list_name=list_1)
                            self.optimum_section_ur.append(self.ur)
                            # Step 3 - Storing the optimum results to a list in a descending order
                            self.common_checks_1(self, section, 5, list_result, list_1)
                    except:
                        logger.warning('Bearing length is invalid.')
                        logger.info('Ignoring web Buckling and Crippling check')
                        self.web_buckling = False
                        # 2.8 - UR
                        print(self.bending_strength_section, self.V_d)
                        if self.bending_strength_section > self.load.moment * 10 ** -6 and self.V_d > self.load.shear_force * 10 ** -3:
                            list_result, list_1 = self.list_changer(self, change='', check=True,list=list_result, list_name=list_1)
                            self.optimum_section_ur.append(self.ur)


                            # Step 3 - Storing the optimum results to a list in a descending order
                            self.common_checks_1(self, section, 5, list_result, list_1)
                else:
                    self.web_buckling = False
                    # 2.8 - UR
                    print(self.bending_strength_section, self.V_d)
                    if self.bending_strength_section > self.load.moment * 10**-6 and self.V_d > self.load.shear_force * 10**-3:

                        self.optimum_section_ur.append(self.ur)
                        list_result, list_1 = self.list_changer(self, change=' ', check=True, list=list_result, list_name=list_1)

                        # Step 3 - Storing the optimum results to a list in a descending order
                        self.common_checks_1(self, section, 5, list_result, list_1)

    def laterally_supported(self):

        print(f"Working laterally_supported")
        # 3 - web buckling under shear
        self.web_buckling_check = IS800_2007.cl_8_2_1_web_buckling(
            d=self.section_property.depth,
            tw=self.section_property.web_thickness,
            e=self.epsilon,
        )
        print(self.web_buckling_check)
        if self.web_buckling_check:
            self.web_buckling_steps(self)
            return
        else:
            self.web_not_buckling_steps(self)
    def web_buckling_steps(self):
        print(f"Working web_buckling_steps")
        # web_buckling_message = 'Thin web'
        logger.warning("Thin web [Reference: Cl 8.2.1.1, IS 800:2007]")

        logger.info(f"Considering  {self.support_cndition_shear_buckling}")
        # 5 - Web Buckling check(when high shear) -If user wants then only
        # if web_buckling:
        #     b1 = input('Enter bearing')
        #     self.web_buckling_strength = self.section_property.web_thickness * (b1 + 1.25 * self.section_property.depth)
        # self.V_d = pass
    def web_not_buckling_steps(self):
        print(f"Working web_not_buckling_steps")
        self.V_d = IS800_2007.cl_8_4_design_shear_strength(
            self.section_property.depth
            * self.section_property.web_thickness,
            self.material_property.fy
        ) / 10 ** 3

        self.high_shear_check = IS800_2007.cl_8_2_1_2_high_shear_check(
            self.load.shear_force / 1000, self.V_d
        )
        print(f"self.V_d {self.V_d},{self.section_property.depth* self.section_property.web_thickness}, {self.material_property.fy}")
        # 4 -  design bending strength
        self.bending_strength_section = self.bending_strength(self) / 10 ** 6



    def bending_strength(self):
        print('Inside bending_strength ')
        # 4 - design bending strength -preliminary
        M_d = IS800_2007.cl_8_2_1_2_design_bending_strength(
            self.section_class,
            self.section_property.plast_sec_mod_z,
            self.section_property.elast_sec_mod_z,
            self.material_property.fy,
            self.gamma_m0,
            self.support,
        )
        if self.section_class == 'plastic' or 'compact' :
            self.beta_b_lt = 1
        else :
            self.beta_b_lt = self.section_property.elast_sec_mod_z/self.section_property.plast_sec_mod_z
        self.M_d = M_d
        if self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE:
            if self.high_shear_check:
                if self.section_class == "Plastic" or self.section_class == "Compact":
                    bending_strength_section = self.bending_strength_reduction(self, M_d)
                else:
                    bending_strength_section = (
                        self.section_property.elast_sec_mod_z
                        * self.material_property.fy
                        * self.gamma_m0
                    )
            else:
                bending_strength_section = M_d
            print('Inside bending_strength 1', M_d, self.high_shear_check, bending_strength_section)
        else:
            It = (
                2
                * self.section_property.flange_width
                * self.section_property.flange_thickness**3
            ) / 3 + (
                (self.section_property.depth - self.section_property.flange_thickness)
                * self.section_property.web_thickness**3
            ) / 3
            hf = self.section_property.depth - self.section_property.flange_thickness
            Iw = 0.5**2 * self.section_property.mom_inertia_y * hf**2
            M_cr = IS800_2007.cl_8_2_2_Unsupported_beam_bending_non_slenderness(
                self.material_property.modulus_of_elasticity,
                0.3,
                self.section_property.mom_inertia_y,
                It,
                Iw,
                self.effective_length * 1e3
            )

            if self.section_class == "Plastic" or self.section_class == "Compact":
                self.beta_b_lt = 1.0
            else:
                self.beta_b_lt = (
                    self.section_property.elast_sec_mod_z
                    / self.section_property.plast_sec_mod_z
                )
            if self.section_property.type == "Rolled":
                alpha_lt = 0.21
            else:
                alpha_lt = 0.49
            lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment(
                self.beta_b_lt,
                self.section_property.plast_sec_mod_z,
                self.section_property.elast_sec_mod_z,
                self.material_property.fy,
                M_cr
            )
            phi_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_phi_lt(
                alpha_lt, lambda_lt
            )
            X_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(
                phi_lt, lambda_lt
            )
            fbd = IS800_2007.cl_8_2_2_Unsupported_beam_bending_compressive_stress(
                X_lt, self.material_property.fy, self.gamma_m0
            )
            bending_strength_section = IS800_2007.cl_8_2_2_Unsupported_beam_bending_strength(
                    self.section_property.plast_sec_mod_z,
                    self.section_property.elast_sec_mod_z,
                    fcd=fbd,
                    section_class=self.section_class
                )
            self.It = It
            self.Iw = Iw
            # self.beta_b_lt = beta_b
            self.alpha_lt = alpha_lt
            self.lambda_lt = lambda_lt
            self.phi_lt = phi_lt
            self.X_lt = X_lt
            self.fbd_lt = fbd
            self.lateral_tb = M_cr * 10**-6
            print('Inside bending_strength 2.1', fbd, self.section_property.plast_sec_mod_z )
            if self.high_shear_check:
                if self.section_class == "Plastic" or self.section_class == "Compact":
                    bending_strength_section = self.bending_strength_reduction(self,Md=bending_strength_section
                    )
                else:
                    bending_strength_section = (
                        self.beta_b_lt
                        * self.section_property.plast_sec_mod_z
                        * fbd
                    )
            print('Inside bending_strength 2',It,hf,Iw,M_cr ,self.beta_b_lt,alpha_lt,lambda_lt,phi_lt,X_lt,fbd,bending_strength_section)
        self.bending_strength_section_reduced = bending_strength_section
        return bending_strength_section
    def bending_strength_reduction(self, Md):
        Zfd = (
            self.section_property.plast_sec_mod_z
            - (self.section_property.depth**2 * self.section_property.web_thickness / 4)
        )
        Mfd = Zfd * self.material_property.fy / self.gamma_m0
        beta = ((2 * self.load.shear_force / (self.V_d * 10**3)) - 1) ** 2
        Mdv = (Md - beta * (Md - Mfd))
        print('Inside bending_strength_reduction',Mdv, Md, beta, Mfd, Zfd)
        self.bending_strength_section_reducedby = Mfd
        self.beta_reduced = beta
        if (
            Mdv
            <= 1.2
            * self.section_property.plast_sec_mod_z
            * self.material_property.fy
            / self.gamma_m0
        ):
            return Mdv
        else:
            return (
                1.2
                * self.section_property.plast_sec_mod_z
                * self.material_property.fy
                / self.gamma_m0
            )


    def section_classification(self, trial_section=""):
        """Classify the sections based on Table 2 of IS 800:2007"""
        print(f"Inside section_classification")
        local_flag = True
        self.input_section_list = []
        self.input_section_classification = {}

        for trial_section in self.input_modified:
            self.section_property = self.section_conect_database(self, trial_section)
            print(f"Type of section{self.section_property.designation}")
            if self.section_property.type == "Rolled":
                web_class = IS800_2007.Table2_iii(
                    self.section_property.depth - 2*(self.section_property.flange_thickness + self.section_property.root_radius),
                    self.section_property.web_thickness,
                    self.material_property.fy,
                )
                flange_class = IS800_2007.Table2_i(
                    self.section_property.flange_width / 2,
                    self.section_property.flange_thickness,
                    self.material_property.fy,
                )[0]
                web_ratio = (self.section_property.depth - 2*(self.section_property.flange_thickness + self.section_property.root_radius)) / self.section_property.web_thickness
                flange_ratio = self.section_property.flange_width / 2  /self.section_property.flange_thickness
            else:
                """Need to check below formula"""
                flange_class = IS800_2007.Table2_i(
                    (
                        (self.section_property.flange_width / 2)
                        # - (self.section_property.web_thickness / 2)
                    ),
                    self.section_property.flange_thickness,
                    self.section_property.fy,
                    self.section_property.type,
                )[0]

                web_class = IS800_2007.Table2_iii(
                    (
                        self.section_property.depth - 2*(self.section_property.flange_thickness + self.section_property.root_radius)
                    ),
                    self.section_property.web_thickness,
                    self.material_property.fy,
                    classification_type="Axial compression",
                )
                web_ratio = (self.section_property.depth - 2 * (
                            self.section_property.flange_thickness + self.section_property.root_radius)) / self.section_property.web_thickness
                flange_ratio = self.section_property.flange_width / 2 / self.section_property.flange_thickness
            print(f"\n \n \n flange_class {flange_class} \n web_class{web_class} \n \n")
            if flange_class == "Slender" or web_class == "Slender":
                self.section_class = "Slender"
            else:
                if flange_class == "Plastic" and web_class == "Plastic":
                    self.section_class = "Plastic"
                elif flange_class == "Plastic" and web_class == "Compact":
                    self.section_class = "Compact"
                elif flange_class == "Plastic" and web_class == "Semi-Compact":
                    self.section_class = "Semi-Compact"
                elif flange_class == "Compact" and web_class == "Plastic":
                    self.section_class = "Compact"
                elif flange_class == "Compact" and web_class == "Compact":
                    self.section_class = "Compact"
                elif flange_class == "Compact" and web_class == "Semi-Compact":
                    self.section_class = "Semi-Compact"
                elif flange_class == "Semi-Compact" and web_class == "Plastic":
                    self.section_class = "Semi-Compact"
                elif flange_class == "Semi-Compact" and web_class == "Compact":
                    self.section_class = "Semi-Compact"
                elif flange_class == "Semi-Compact" and web_class == "Semi-Compact":
                    self.section_class = "Semi-Compact"

            # logger.info(
            #     "The section is {}. The {} section  has  {} flange({}) and  {} web({}).  [Reference: Cl 3.7, IS 800:2007].".format(
            #         self.section_class,
            #         trial_section,
            #         flange_class, round(flange_ratio,2),
            #         web_class, round(web_ratio,2)
            #     )
            # )
            print( 'self.allow_class', self.allow_class)
            if self.allow_class != 'No':
                if (
                    self.section_class == "Semi-Compact"
                    or self.section_class == "Compact"
                    or self.section_class == "Plastic"
                ):
                    self.input_section_list.append(trial_section)
                    self.input_section_classification.update({trial_section: [self.section_class, flange_class, web_class, flange_ratio, web_ratio]})
                elif self.section_class == "Slender":
                    logger.warning(f"The section.{trial_section} is Slender. Ignoring")
            else:
                if self.section_class == "Compact" or self.section_class == "Plastic":
                    self.input_section_list.append(trial_section)
                    self.input_section_classification.update({trial_section: [self.section_class, flange_class, web_class, flange_ratio, web_ratio]})
                elif self.section_class == "Slender":
                    logger.warning(f"The section.{trial_section} is Slender. Ignoring")
                    self.design_status = False
                    self.design_status_list.append(self.design_status)
                elif self.section_class == "Semi-Compact":
                    logger.warning(
                        f"The section.{trial_section} is Semi-Compact. Ignoring"
                    )
                    self.design_status = False
                    self.design_status_list.append(self.design_status)

        if len(self.input_section_list) == 0:
            local_flag = False
        else:
            local_flag = True
        return local_flag

    def effective_length_beam(self, design_dictionary, length):
        print(f"Inside effective_length_beam")
        self.Loading = design_dictionary[KEY_LOAD]  # 'Normal'or 'Destabilizing'
        if design_dictionary[KEY_LENGTH_OVERWRITE] == 'NA':
            if self.support == KEY_DISP_SUPPORT1:
                self.Torsional_res = design_dictionary[KEY_TORSIONAL_RES]
                self.Warping = design_dictionary[KEY_WARPING_RES]
                self.effective_length = IS800_2007.cl_8_3_1_EffLen_Simply_Supported(
                    Torsional=self.Torsional_res,
                    Warping=self.Warping,
                    length=length,
                    depth=self.section_property.depth,
                    load=self.Loading,
                )
                print(f"Working 1 {self.effective_length}")
            elif self.support == KEY_DISP_SUPPORT2:
                self.Support = design_dictionary[KEY_SUPPORT_TYPE]
                self.Top = design_dictionary[KEY_SUPPORT_TYPE2]
                self.effective_length = IS800_2007.cl_8_3_3_EffLen_Cantilever(
                    Support=self.Support,
                    Top=self.Top,
                    length=length,
                    load=self.Loading,
                )
                print(f"Working 2 {self.effective_length}")
        else:
            try:
                if float(design_dictionary[KEY_LENGTH_OVERWRITE]) <= 0:
                    design_dictionary[KEY_LENGTH_OVERWRITE] = 'NA'
                length = length * float(design_dictionary[KEY_LENGTH_OVERWRITE])
                self.effective_length = length
                print(f"Working 3 {self.effective_length}")
            except:
                print(f"Inside effective_length_beam",type(design_dictionary[KEY_LENGTH_OVERWRITE]))
                logger.warning("Invalid Effective Length Parameter.")
                logger.info('Effective Length Parameter is set to default: 1.0')
                design_dictionary[KEY_LENGTH_OVERWRITE] = '1.0'
                self.effective_length_beam(self, design_dictionary, length)
                print(f"Working 4 {self.effective_length}")
        print(f"Inside effective_length_beam",self.effective_length, design_dictionary[KEY_LENGTH_OVERWRITE])


    def lambda_lt_check_member_type(self, Mcr=0, fcrb=0, Zp=0, f_y=0, Ze=0, beta_b=0):
        lambda_lt_1 = math.sqrt(beta_b * Zp * f_y / Mcr)
        lambda_lt_2 = math.sqrt(f_y / fcrb)
        lambda_lt_check = math.sqrt(1.2 * Ze * f_y / Mcr)
        if lambda_lt_1 == lambda_lt_2:
            if lambda_lt_1 <= lambda_lt_check:
                return lambda_lt_1
        logger.warning(" Issues with the non-dimensional slenderness ratio Lambda_lt")

    def common_checks_1(self, section, step=1, list_result=[], list_1=[]):
        if step == 1:
            print(f"Working correct here")
        elif step == 2:
            # reduction of the area based on the connection requirements (input from design preferences)
            if self.effective_area_factor < 1.0:
                self.effective_area = round(
                    self.effective_area * self.effective_area_factor, 2
                )


        elif step == 3:
            # 2.1 - Buckling curve classification and Imperfection factor
            if self.section_property.type == 'Rolled':
                self.buckling_class = 'c'
            self.imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(
                                                                                    buckling_class=self.buckling_class
                                                                                )
        elif step == 4:
            # self.slenderness = self.effective_length / min(self.section_property.rad_of_gy_z, self.section_property.rad_of_gy_y) * 1000
            print(
                f"\n data sent "
                f" self.material_property.fy {self.material_property.fy}"
                f"self.gamma_m0 {self.gamma_m0}"
                f"self.slenderness {self.slenderness}"
                f" self.imperfection_factor {self.imperfection_factor}"
                f"self.section_property.modulus_of_elasticity {self.section_property.modulus_of_elasticity}"
            )

            list_cl_7_1_2_1_design_compressisive_stress = (
                IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                    self.material_property.fy,
                    self.gamma_m0,
                    self.slenderness,
                    self.imperfection_factor,
                    self.section_property.modulus_of_elasticity,
                    check_type=list_result,
                )
            )
            for x in list_cl_7_1_2_1_design_compressisive_stress:
                print(f"x {x} ")
            self.euler_buckling_stress = list_cl_7_1_2_1_design_compressisive_stress[0]
            self.nondimensional_effective_slenderness_ratio = (
                list_cl_7_1_2_1_design_compressisive_stress[1]
            )
            self.phi = list_cl_7_1_2_1_design_compressisive_stress[2]
            self.stress_reduction_factor = list_cl_7_1_2_1_design_compressisive_stress[
                3
            ]
            self.design_compressive_stress_fr = (
                list_cl_7_1_2_1_design_compressisive_stress[4]
            )
            self.design_compressive_stress = (
                list_cl_7_1_2_1_design_compressisive_stress[5]
            )
            self.design_compressive_stress_max = (
                list_cl_7_1_2_1_design_compressisive_stress[6]
            )
        elif step == 5:
            # 1- Based on optimum UR
            self.optimum_section_ur_results[self.ur] = {}
            list_2 = list_result.copy()
            for j in list_1:
                # k = 0
                for k in list_2:
                    self.optimum_section_ur_results[self.ur][j] = k
                    # k += 1
                    list_2.pop(0)
                    break

            # 2- Based on optimum cost
            self.optimum_section_cost_results[self.cost] = {}

            list_2 = list_result.copy()  # Why?
            for j in list_1:
                for k in list_2:
                    self.optimum_section_cost_results[self.cost][j] = k
                    list_2.pop(0)
                    break
            print(
                f"\n self.optimum_section_cost_results {self.optimum_section_cost_results}"
                f"\n self.optimum_section_ur_results {self.optimum_section_ur_results}"
            )
        elif step == 6:
            self.single_result[self.sec_profile] = {}
            list_2 = list_result.copy()
            for j in list_1:
                # k = 0
                for k in list_2:
                    self.single_result[self.sec_profile][j] = k
                    # k += 1
                    list_2.pop(0)
                    break
            print(f"\n self.single_result {self.single_result}")

    def list_changer(self, change, list,list_name, check = True):
        list_name.extend([
            "Designation"])
        if self.high_shear_check:
            list.extend(
                [self.bending_strength_section_reducedby, self.beta_reduced, self.M_d])
            list_name.extend([
                "Mfd",
                "Beta_reduced",
                'M_d'
            ])

        list.extend(
            [self.section_class, self.effective_area, self.V_d, self.high_shear_check,
             self.bending_strength_section, self.effective_length, self.ur,
             self.cost, self.beta_b_lt])
        list_name.extend([

            "Section class",
            "Effective area",
            "Shear Strength",
            "High Shear check",
            "Bending Strength",
            "Effective_length",
            "UR",
            "Cost",
            "Beta_b"
        ])
        if change == 'Web Buckling':
            list.extend([self.buckling_class,
                            self.imperfection_factor,
                            self.slenderness,
                            self.euler_buckling_stress,
                            self.nondimensional_effective_slenderness_ratio,
                            self.phi,
                            self.stress_reduction_factor,
                            self.design_compressive_stress_fr,
                            self.design_compressive_stress_max,
                            self.design_compressive_stress,
                            self.section_capacity,
                            self.F_wb])

            list_name.extend ([
                "Buckling_class",
                "IF",
                "Effective_SR",
                "EBS",
                "ND_ESR",
                "phi",
                "SRF",
                "FCD_formula",
                "FCD_max",
                "FCD",
                "Capacity",
                "Web_crippling"
            ])
        if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
            list.extend([self.It,
                            self.Iw,
                            self.alpha_lt,
                            self.lambda_lt,
                            self.phi_lt,
                            self.X_lt,
                            self.fbd_lt,
                            self.lateral_tb])

            list_name.extend([
                "It",
                "Iw",
                "IF_lt",
                "ND_ESR_lt",
                "phi_lt",
                "SRF_lt",
                "FCD_lt",
                "Mcr"
            ])
        return  list,list_name

    def results(self, design_dictionary):

        # sorting results from the dataset
        # if len(self.input_section_list) > 1:
        # results based on UR
        if self.optimization_parameter == "Utilization Ratio":
            filter_UR = filter(
                lambda x: x <= min(self.allowable_utilization_ratio, 1.0),
                self.optimum_section_ur
            )
            self.optimum_section_ur = list(filter_UR)

            self.optimum_section_ur.sort()
            # print(f"self.optimum_section_ur{self.optimum_section_ur}")
            # print(f"self.result_UR{self.result_UR}")

            # selecting the section with most optimum UR
            if len(self.optimum_section_ur) == 0:  # no design was successful
                logger.warning(
                    "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                    "criteria"
                )
                logger.error(
                    "The solver did not find any adequate section from the defined list."
                )
                logger.info(
                    "Re-define the list of sections or check the Design Preferences option and re-design."
                )
                self.design_status = False
                self.design_status_list.append(self.design_status)

            else:
                self.result_UR = self.optimum_section_ur[
                    -1
                ]  # optimum section which passes the UR check
                print(f"self.result_UR{self.result_UR}")
                self.design_status = True

        else:  # results based on cost
            self.optimum_section_cost.sort()

            # selecting the section with most optimum cost
            self.result_cost = self.optimum_section_cost[0]

        # print results
        if len(self.optimum_section_ur) == 0:
            logger.warning(
                "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                "criteria"
            )
            logger.error(
                "The solver did not find any adequate section from the defined list."
            )
            logger.info(
                "Re-define the list of sections or check the Design Preferences option and re-design."
            )
            self.design_status = False
            self.design_status_list.append(self.design_status)
            pass
        else:
            if self.optimization_parameter == "Utilization Ratio":
                self.common_result(
                    self,
                    list_result=self.optimum_section_ur_results,
                    result_type=self.result_UR,
                )
            else:
                self.result_UR = self.optimum_section_cost_results[
                    self.result_cost
                ]["UR"]

                # checking if the selected section based on cost satisfies the UR
                if self.result_UR > min(self.allowable_utilization_ratio, 1.0):
                    trial_cost = []
                    for cost in self.optimum_section_cost:
                        self.result_UR = self.optimum_section_cost_results[
                            cost
                        ]["UR"]
                        if self.result_UR <= min(
                            self.allowable_utilization_ratio, 1.0
                        ):
                            trial_cost.append(cost)

                    trial_cost.sort()

                    if len(trial_cost) == 0:  # no design was successful
                        logger.warning(
                            "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                            "criteria"
                        )
                        logger.error(
                            "The solver did not find any adequate section from the defined list."
                        )
                        logger.info(
                            "Re-define the list of sections or check the Design Preferences option and re-design."
                        )
                        self.design_status = False
                        self.design_status_list.append(self.design_status)
                        print(f"design_status_list{self.design_status} \n")
                    else:
                        self.result_cost = trial_cost[
                            0
                        ]  # optimum section based on cost which passes the UR check
                        self.design_status = True

                # results
                self.common_result(
                    self,
                    list_result=self.optimum_section_cost_results,
                    result_type=self.result_cost,
                )

                print(f"design_status_list2{self.design_status}")
        for status in self.design_status_list:
            if status is False:
                self.design_status = False
                break
            else:
                self.design_status = True

    def common_result(self, list_result, result_type, flag=1):
        self.result_designation = list_result[result_type]["Designation"]
        logger.info(
            "The section is {}. The {} section  has  {} flange({}) and  {} web({}).  [Reference: Cl 3.7, IS 800:2007].".format(
                self.input_section_classification[self.result_designation][0] ,
                self.result_designation,
                self.input_section_classification[self.result_designation][1], round(self.input_section_classification[self.result_designation][3],2),
                self.input_section_classification[self.result_designation][2], round(self.input_section_classification[self.result_designation][4],2)
            )
        )

        self.result_section_class = list_result[result_type]["Section class"]
        self.result_effective_area = round(list_result[result_type]["Effective area"],2)
        if self.effective_area_factor < 1.0:
            logger.info(
                "The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".format(
                    round((self.result_effective_area / self.effective_area_factor), 2),
                    self.result_effective_area,
                )
            )

        self.result_shear = round(list_result[result_type]["Shear Strength"], 2)
        self.result_high_shear = list_result[result_type]["High Shear check"]
        self.result_bending = round(list_result[result_type]["Bending Strength"], 2)
        self.result_eff_len = round(list_result[result_type]["Effective_length"], 2)
        self.result_cost = list_result[result_type]["Cost"]
        self.result_betab = list_result[result_type]["Beta_b"]

        if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE :
            self.result_mcr = round(list_result[result_type]['Mcr'], 2)
            self.result_IF_lt = round(list_result[result_type]["IF_lt"], 2)
            self.result_tc = round(list_result[result_type]["It"], 2)
            self.result_wc = round(list_result[result_type]["Iw"], 2)
            self.result_nd_esr_lt = round(list_result[result_type]["ND_ESR_lt"], 2)
            self.result_phi_lt = round(list_result[result_type]["phi_lt"], 2)
            self.result_srf_lt = round(list_result[result_type]["SRF_lt"], 2)
            self.result_fcd__lt = round(list_result[result_type]["FCD_lt"], 2)
        else:
            self.result_mcr = 'NA'
            self.result_IF_lt = 'NA'
            self.result_tc = 'NA'
            self.result_wc = 'NA'
            self.result_nd_esr_lt = 'NA'
            self.result_phi_lt = 'NA'
            self.result_srf_lt = 'NA'
            self.result_fcd__lt = 'NA'

        if self.web_buckling :
            self.result_bc = list_result[result_type]['Buckling_class']
            self.result_IF = round(list_result[result_type]["IF"], 2)
            self.result_eff_sr = round(list_result[result_type]["Effective_SR"], 2)
            self.result_ebs = round(list_result[result_type]["EBS"], 2)
            self.result_nd_esr = round(list_result[result_type]["ND_ESR"], 2)
            self.result_phi_zz = round(list_result[result_type]["phi"], 2)
            self.result_srf = round(list_result[result_type]["SRF"], 2)
            self.result_fcd_1_zz = round(list_result[result_type]["FCD_formula"], 2)
            self.result_fcd_2 = round(list_result[result_type]["FCD_max"], 2)
            self.result_fcd = round(list_result[result_type]["FCD"], 2)
            self.result_capacity = round(list_result[result_type]["Capacity"], 2)
            self.result_crippling = round(list_result[result_type]["Web_crippling"], 2)
        else:
            self.result_bc = 'NA'
            self.result_IF = 'NA'
            self.result_eff_sr = 'NA'
            self.result_lambda_vv = 'NA'
            self.result_lambda_psi = 'NA'
            self.result_ebs = 'NA'
            self.result_nd_esr = 'NA'
            self.result_phi_zz = 'NA'
            self.result_srf = 'NA'
            self.result_fcd_1_zz = 'NA'
            self.result_fcd_2 = 'NA'
            self.result_fcd = 'NA'
            self.result_capacity = 'NA'
            self.result_crippling = 'NA'
        if self.result_high_shear:
            self.result_mfd = list_result[result_type]["Mfd"]
            self.result_beta_reduced = list_result[result_type]["Beta_reduced"]
            self.result_Md= list_result[result_type]["M_d"]

    ### start writing save_design from here!
    def save_design(self, popup_summary):
        self.section_property = self.section_conect_database(self, self.result_designation)

        if self.design_status:
            if self.sec_profile=='Columns' or self.sec_profile=='Beams':
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



            self.report_input = \
                {#KEY_MAIN_MODULE: self.mainmodule,
                 KEY_MODULE: self.module, #"Axial load on column "
                    KEY_DISP_SHEAR: self.load.shear_force * 10 ** -3,
                    KEY_DISP_BEAM_MOMENT_Latex: self.load.moment * 10 ** -6,
                    KEY_DISP_LENGTH_BEAM: self.length,
                    KEY_DISP_SEC_PROFILE: self.sec_profile,
                    KEY_DISP_SECSIZE: str(self.sec_list),
                 KEY_MATERIAL: self.material,
                    "Selected Section Details": self.report_column,
                    KEY_BEAM_SUPP_TYPE: self.latex_design_type,
                }

            # if self.latex_design_type == VALUES_SUPP_TYPE_temp[0]:
            #     self.report_input.update({
            #         KEY_DISP_BENDING: self.bending_type})
            # elif self.latex_design_type == VALUES_SUPP_TYPE_temp[1]:
            #     self.report_input.update({
            #         KEY_BEAM_SUPP_TYPE_DESIGN: self.support,
            #         # KEY_DISP_BENDING: self.bending_type,
            #     })
            self.report_input.update({
                KEY_DISP_SUPPORT : self.support,
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.material_property.fu,
                KEY_DISP_YIELD_STRENGTH_REPORT: self.material_property.fy,
                "End Conditions - " + str(self.support): "TITLE",
            })

            if self.support == KEY_DISP_SUPPORT1:
                self.report_input.update({
                    DISP_TORSIONAL_RES: self.Torsional_res,
                    DISP_WARPING_RES:self.Warping })
            else:
                self.report_input.update({
                    DISP_SUPPORT_RES: self.Support,
                    DISP_TOP_RES: self.Top})
            self.report_input.update({
                "Design Preference" : "TITLE",
                KEY_DISP_EFFECTIVE_AREA_PARA: self.effective_area_factor,
                KEY_DISP_CLASS: self.allow_class,
                KEY_DISP_LOAD: self.Loading,
                KEY_DISPP_LENGTH_OVERWRITE: self.latex_efp,
                KEY_DISP_BEARING_LENGTH + ' (mm)': self.bearing_length,

            })
            # self.report_input.update({
            #      # KEY_DISP_SEC_PROFILE: self.sec_profile,
            #      "I Section - Mechanical Properties": "TITLE",
            #      })
            self.report_input.update()
            self.report_check = []

            t1 = ('Selected', 'Selected Member Data', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
            self.report_check.append(t1)

            t1 = ('SubSection', 'Shear Strength Results', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
            self.report_check.append(t1)

            t1 = (KEY_DISP_DESIGN_STRENGTH_SHEAR, self.load.shear_force * 10 ** -3,
                  cl_8_4_shear_yielding_capacity_member(self.section_property.depth,
                                                        self.section_property.web_thickness, self.material_property.fy,
                                                        self.gamma_m0, round(self.result_shear, 2)),
                  get_pass_fail(self.load.shear_force * 10 ** -3, round(self.result_shear, 2), relation="lesser"))
            self.report_check.append(t1)

            t1 = (KEY_DISP_ALLOW_SHEAR, ' ',
                  cl_8_2_1_2_shear_check(round(self.result_shear,2), round(0.6 * self.result_shear,2), self.result_high_shear,self.load.shear_force*10**-3),
                  get_pass_fail(self.load.shear_force*10**-3, round(0.6 * self.result_shear,2), relation="Warn",M1='High Shear',M2='Low Shear'))
            self.report_check.append(t1)

            t1 = ('SubSection', 'Moment Strength Results', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            if self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE:
                if self.result_high_shear:
                    t1 = (KEY_DISP_Bending_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_9_2_2_combine_shear_bending_md_init(
                              self.section_property.elast_sec_mod_z,
                              self.section_property.plast_sec_mod_z,
                              self.material_property.fy, self.support,
                              self.gamma_m0, round(self.result_betab, 2),
                              round(self.result_Md * 10 ** -6, 2), self.result_section_class
                          ),
                          ' ')
                    self.report_check.append(t1)
                    t1 = (KEY_DISP_PLASTIC_STRENGTH_MOMENT,' ',
                          cl_9_2_2_combine_shear_bending_mfd(
                                                         self.section_property.plast_sec_mod_z,
                                                         self.section_property.depth,
                                                         self.section_property.web_thickness,
                                                         self.material_property.fy,
                                                         self.gamma_m0,
                                                         round(self.result_mfd * 10 ** -6, 2)),
                          ' ')
                    self.report_check.append(t1)

                    # temp = cl_8_2_1_2_plastic_moment_capacity_member(self.result_betab,
                    #                                           self.section_property.plast_sec_mod_z,
                    #                                           self.material_property.fy, self.gamma_m0,
                    #                                           round(self.result_bending, 2))
                    # print('tempt',temp)
                    t1 = (KEY_DISP_DESIGN_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_9_2_2_combine_shear_bending(round(self.result_bending,2),self.section_property.elast_sec_mod_z,
                                                         self.material_property.fy,self.result_section_class,self.load.shear_force*10**-3, round(self.result_shear,2),
                                                         self.gamma_m0, round(self.result_betab,2),round(self.result_Md*10**-6,2),round(self.result_mfd*10**-6,2)),
                          get_pass_fail(self.load.moment*10**-6, round(self.result_bending, 2), relation="lesser"))
                    self.report_check.append(t1)

                else:
                    t1 = (KEY_DISP_DESIGN_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_8_2_1_2_plastic_moment_capacity_member(round(self.result_betab,2),
                                                                    self.section_property.plast_sec_mod_z,
                                                                    self.material_property.fy, self.gamma_m0,
                                                                    round(self.result_bending, 2)),
                          get_pass_fail(self.load.moment*10**-6, round(self.result_bending, 2), relation="lesser"))
                    self.report_check.append(t1)
            elif self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
                if self.result_high_shear:
                    t1 = (KEY_DISP_LTB_Bending_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_9_2_2_combine_shear_bending_md_init(
                              self.section_property.elast_sec_mod_z,
                              self.section_property.plast_sec_mod_z,
                              self.material_property.fy, self.support,
                              self.gamma_m0, round(self.result_betab, 2),
                              round(self.result_Md * 10 ** -6, 2), self.result_section_class
                          ),
                          ' ')
                    self.report_check.append(t1)
                    t1 = (KEY_DISP_PLASTIC_STRENGTH_MOMENT,' ',
                          cl_9_2_2_combine_shear_bending_mfd(
                                                         self.section_property.plast_sec_mod_z,
                                                         self.section_property.depth,
                                                         self.section_property.web_thickness,
                                                         self.material_property.fy,
                                                         self.gamma_m0,
                                                         round(self.result_mfd * 10 ** -6, 2)),
                          ' ')
                    self.report_check.append(t1)

                    # temp = cl_8_2_1_2_plastic_moment_capacity_member(self.result_betab,
                    #                                           self.section_property.plast_sec_mod_z,
                    #                                           self.material_property.fy, self.gamma_m0,
                    #                                           round(self.result_bending, 2))
                    # print('tempt',temp)
                    t1 = (KEY_DISP_REDUCE_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_9_2_2_combine_shear_bending(round(self.result_bending,2),self.section_property.elast_sec_mod_z,
                                                         self.material_property.fy,self.result_section_class,self.load.shear_force*10**-3, round(self.result_shear,2),
                                                         self.gamma_m0, round(self.result_betab,2),round(self.result_Md*10**-6,2),round(self.result_mfd*10**-6,2)),
                          get_pass_fail(self.load.moment*10**-6, round(self.result_bending, 2), relation="lesser"))
                    self.report_check.append(t1)

                else:
                    t1 = (KEY_DISP_LTB_Bending_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_8_2_1_2_plastic_moment_capacity_member(round(self.result_betab,2),
                                                                    self.section_property.plast_sec_mod_z,
                                                                    self.material_property.fy, self.gamma_m0,
                                                                    round(self.result_bending, 2)),
                          get_pass_fail(self.load.moment*10**-6, round(self.result_bending, 2), relation="lesser"))
                    self.report_check.append(t1)

        # else:
        #     t1 = (KEY_DISP_ALLOW_SHEAR, self.load.shear_force,
        #           allow_shear_capacity(round(self.result_shear, 2), round(0.6 * self.result_shear, 2)),
        #           get_pass_fail(self.load.shear_force))
        # self.report_check.append(t1)



        # self.h = (self.beam_D - (2 * self.beam_tf))
        #
        # 1.1 Input sections display
        # t1 = ('SubSection', 'List of Input Sections',self.sec_list),
        # self.report_check.append(t1)
        #
        # # 2.2 CHECK: Buckling Class - Compatibility Check
        # t1 = ('SubSection', 'Buckling Class - Compatibility Check', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{2cm}|')
        # self.report_check.append(t1)
        #
        # t1 = ("Section Class ", comp_column_class_section_check_required(self.result_section_class, self.h, self.bf),
        #       comp_column_class_section_check_provided(self.bucklingclass, self.h, self.bf, self.tf, self.var_h_bf),
        #       'Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        # self.report_check.append(t1)

        # t1 = ("h/bf , tf ", comp_column_class_section_check_required(self.bucklingclass, self.h, self.bf),
        #       comp_column_class_section_check_provided(self.bucklingclass, self.h, self.bf, self.tf, self.var_h_bf),
        #       'Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        # self.report_check.append(t1)
        #
        # # 2.3 CHECK: Cross-section classification
        # t1 = ('SubSection', 'Cross-section classification', '|p{4.5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
        # self.report_check.append(t1)
        #
        # t1 = ("b/tf and d/tw ", cross_section_classification_required(self.section),
        #       cross_section_classification_provided(self.tf, self.b1, self.epsilon, self.section, self.b1_tf,
        #                                             self.d1_tw, self.ep1, self.ep2, self.ep3, self.ep4),
        #       'b = bf / 2,d = h – 2 ( T + R1),έ = (250 / Fy )^0.5,Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        # self.report_check.append(t1)
        #
        # # 2.4 CHECK : Member Check
        # t1 = ("Slenderness", cl_7_2_2_slenderness_required(self.KL, self.ry, self.lamba),
        #       cl_7_2_2_slenderness_provided(self.KL, self.ry, self.lamba), 'PASS')
        # self.report_check.append(t1)
        #
        # t1 = (
        # "Design Compressive stress (fcd)", cl_7_1_2_1_fcd_check_required(self.gamma_mo, self.f_y, self.f_y_gamma_mo),
        # cl_7_1_2_1_fcd_check_provided(self.facd), 'PASS')
        # self.report_check.append(t1)
        #
        # t1 = ("Design Compressive strength (Pd)", cl_7_1_2_design_comp_strength_required(self.axial),
        #       cl_7_1_2_design_comp_strength_provided(self.Aeff, self.facd, self.A_eff_facd), "PASS")
        # self.report_check.append(t1)
        #
        # t1 = ('', '', '', '')
        # self.report_check.append(t1)


        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"

        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = os.path.abspath(".") # TEMP
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                              rel_path, Disp_2d_image, Disp_3D_image, module=self.module) #
