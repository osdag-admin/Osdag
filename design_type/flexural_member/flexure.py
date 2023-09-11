# noinspection PyInterpreter
from design_type.member import Member
from Common import *
from utils.common.component import ISection, Material
from utils.common.common_calculation import *
from utils.common.load import Load
from design_type.tension_member import *
from utils.common.Section_Properties_Calculator import BBAngle_Properties
import math
import numpy as np
from utils.common import is800_2007
from utils.common.component import *



class Flexure(Member):

    def __init__(self):
        print(f"Here Flexure")
        super(Flexure, self).__init__()

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
        which will be displayed in chosen tab layoutGusset Plate Details

        """
        tabs = []

        t1 = (DISP_TITLE_ISECTION, TYPE_TAB_1, self.tab_section)
        tabs.append(t1)

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
              ['Label_HS_11', 'Label_HS_12', 'Label_HS_13', 'Label_HS_14', 'Label_HS_15', 'Label_HS_16', 'Label_HS_17',
               'Label_HS_18',
               'Label_HS_19', 'Label_HS_20', 'Label_HS_21', 'Label_HS_22', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_SHS_RHS_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, ['Label_CHS_1', 'Label_CHS_2', 'Label_CHS_3'],
              ['Label_CHS_11', 'Label_CHS_12', 'Label_CHS_13', 'Label_HS_14', 'Label_HS_15', 'Label_HS_16', 'Label_21',
               'Label_22',
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
        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])  # Need to check
        design_input.append(t1)

        t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY])
        design_input.append(t1)

        t2 = ("Optimization", TYPE_TEXTBOX, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA])  # , KEY_STEEL_COST
        design_input.append(t2)
        # t2 = (DISP_TITLE_ANGLE, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        # design_input.append(t2)
        #
        # t2 = ("Optimization", TYPE_TEXTBOX, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA, KEY_Buckling_Out_plane, KEY_Buckling_In_plane, KEY_BOLT_Number ]) #KEY_ALLOW_UR, , KEY_STEEL_COST
        # design_input.append(t2)
        #
        # t2 = ("Optimization", TYPE_COMBOBOX, [ KEY_ALLOW_LOAD, Load_type2, Load_type1, KEY_PLATETHK ]) # KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS,
        # design_input.append(t2)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        return design_input

    def input_dictionary_without_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to
        design dictionary if design preference is never opened by user. It sets are design preference values to default.
        If any design preference value needs to be set to input dock value, tuple shall be written as:

        (Key of input dock, [List of Keys from design prefernce], 'Input Dock')

        If the values needs to be set to default,

        (None, [List of Design Prefernce Keys], '')

         """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA, KEY_DP_DESIGN_METHOD],
              '')  # KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS1, KEY_ALLOW_CLASS2, KEY_ALLOW_CLASS3, KEY_ALLOW_CLASS4, KEY_STEEL_COST,

        design_input.append(t2)
        # t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        # design_input.append(t1)
        #
        # t2 = (None, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA, KEY_Buckling_Out_plane, KEY_Buckling_In_plane,
        #              KEY_DP_DESIGN_METHOD, KEY_ALLOW_LOAD, KEY_BOLT_Number, KEY_PLATETHK
        #              ], '')#, KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS, KEY_STEEL_COST, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_EDGE_TYPE,KEY_DP_DETAILING_GAP,
        #              # KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_CONNECTOR_MATERIAL , KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
        # design_input.append(t2)

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

        # t2 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
        #       VALUES_SEC_PROFILE_Compression_Strut , Profile_name_1)
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
            KEY_DP_DESIGN_METHOD: "Limit State Design",
            # KEY_ALLOW_UR: '1.0',
            # KEY_EFFECTIVE_AREA_PARA: '1.0',
            # KEY_Buckling_Out_plane: '1.0',
            # KEY_Buckling_In_plane: '1.0',
            # KEY_ALLOW_LOAD: Load_type1,
            # KEY_BOLT_Number: '1.0',
            # KEY_ALLOW_LOAD: 'Concentric Load',
            # KEY_DP_DESIGN_METHOD: "Limit State Design",
            # KEY_PLATETHK : '8'
        }[key]

        return val

    ####################################
    # Design Preference Functions End
    ####################################

    def module_name(self):
        return KEY_DISP_FLEXURE

    def set_osdaglogger(key):

        """
        Function to set Logger for Strut design Module
        """

        # @author Rutvik J
        global logger
        logger = logging.getLogger('Osdag')

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

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair
        self.module = KEY_DISP_FLEXURE
        options_list = []

        t1 = (KEY_MODULE, KEY_DISP_FLEXURE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t1)

        t1 = (None, KEY_BEAM_SUPP_TYPE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_SUPP_TYPE, KEY_BEAM_SUPP_TYPE, TYPE_COMBOBOX, VALUES_SUPP_TYPE, True, 'No Validator')
        options_list.append(t2)

        # t3 = (KEY_IMAGE, None, TYPE_IMAGE, VALUES_IMG_STRUT[0], True, 'No Validator')
        # options_list.append(t3)

        t3 = (KEY_SUPPORT, KEY_DISP_SUPPORT, TYPE_COMBOBOX, KEY_DISP_SUPPORT_LIST, True, 'No Validator')
        options_list.append(t3)


        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator')
        options_list.append(t4)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_LENGTH, KEY_DISP_LENGTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)

        t9 = (None, DISP_TITLE_STRUT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_END1, KEY_DISP_END1, TYPE_COMBOBOX, VALUES_STRUT_END1, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_END2, KEY_DISP_END2, TYPE_COMBOBOX, VALUES_STRUT_END2, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_IMAGE_two, None, TYPE_IMAGE_COMPRESSION, "./ResourceFiles/images/6.RRRR.PNG", True, 'No Validator')
        options_list.append(t12)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        return options_list

    # def spacing(self, status):
    #
    #     spacing = []
    #
    #     t00 = (None, "", TYPE_NOTE, "Representative image for Spacing Details based on member's depth \n (root radius not included in edge distance)")
    #     spacing.append(t00)
    #
    #     t99 = (None, 'Spacing Details', TYPE_SECTION,
    #            ['./ResourceFiles/images/spacing_1.png', 400, 278, "3 x 3 pattern considered"])  # [image, width, height, caption]
    #     spacing.append(t99)
    #
    #     if self.sec_profile == 'Star Angles':
    #         t16 = (KEY_OUT_BOLTS_ONE_LINE_S, KEY_OUT_DISP_BOLTS_ONE_LINE_S, TYPE_TEXTBOX,
    #                int(self.plate.bolts_one_line/2) if status else '', True)
    #         spacing.append(t16)
    #     else:
    #         pass
    #
    #     t16 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.plate.bolts_one_line if status else '',True)
    #     spacing.append(t16)
    #
    #     t15 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.plate.bolt_line if status else '', True)
    #     spacing.append(t15)
    #
    #     t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
    #     spacing.append(t9)
    #
    #     t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
    #     spacing.append(t10)
    #
    #     t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
    #     spacing.append(t11)
    #
    #     t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
    #     spacing.append(t12)
    #
    #     return spacing

    # def memb_pattern(self, status):
    #
    #     if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
    #         image = './ResourceFiles/images/L.png'
    #         x, y = 400, 202
    #
    #     else:
    #         image = './ResourceFiles/images/U.png'
    #         x, y = 400, 202
    #
    #
    #     pattern = []
    #
    #     t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
    #     pattern.append(t00)
    #
    #     t99 = (None, 'Failure Pattern due to Tension in Member', TYPE_IMAGE,
    #            [image, x, y, "Member Block Shear Pattern"])  # [image, width, height, caption]
    #     pattern.append(t99)
    #
    #     return pattern

    # def plate_pattern(self, status):
    #
    #     pattern = []
    #
    #     t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
    #     pattern.append(t00)
    #
    #     t99 = (None, 'Failure Pattern due to Tension in Plate', TYPE_IMAGE,
    #            ['./ResourceFiles/images/L.png',400,202, "Plate Block Shear Pattern"])  # [image, width, height, caption]
    #     pattern.append(t99)
    #
    #     return pattern

    def fn_end1_end2(self):

        end1 = self[0]
        if end1 == 'Fixed':
            return VALUES_STRUT_END2
        elif end1 == 'Free':
            return ['Fixed']
        elif end1 == 'Hinged':
            return ['Fixed', 'Hinged']
        elif end1 == 'Roller':
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

    def fn_end2_image(self):

        end1 = self[0]
        end2 = self[1]

        if end1 == 'Fixed':
            if end2 == 'Fixed':
                return "./ResourceFiles/images/6.RRRR.PNG"
            elif end2 == 'Free':
                return "./ResourceFiles/images/1.RRFF_rotated.PNG"
            elif end2 == 'Hinged':
                return "./ResourceFiles/images/5.RRRF_rotated.PNG"
            elif end2 == 'Roller':
                return "./ResourceFiles/images/4.RRFR_rotated.PNG"
        elif end1 == 'Free':
            return "./ResourceFiles/images/1.RRFF.PNG"
        elif end1 == 'Hinged':
            if end2 == 'Fixed':
                return "./ResourceFiles/images/5.RRRF.PNG"
            elif end2 == 'Hinged':
                return "./ResourceFiles/images/3.RFRF.PNG"
            elif end2 == 'Roller':
                return "./ResourceFiles/images/2.FRFR_rotated.PNG"
        elif end1 == 'Roller':
            if end2 == 'Fixed':
                return "./ResourceFiles/images/4.RRFR.PNG"
            elif end2 == 'Hinged':
                return "./ResourceFiles/images/2.FRFR.PNG"

    def fn_conn_image(self):

        "Function to populate section images based on the type of section "
        img = self[0]
        if img == VALUES_SEC_PROFILE_Compression_Strut[0]:
            return VALUES_IMG_STRUT[0]
        elif img ==VALUES_SEC_PROFILE_Compression_Strut[1]:
            return VALUES_IMG_STRUT[1]
        elif img == VALUES_SEC_PROFILE_Compression_Strut[2]:
            return VALUES_IMG_STRUT[2]
        elif img == VALUES_SEC_PROFILE_Compression_Strut[3]:
            print(' fn_conn_image error')
            return VALUES_IMG_TENSIONBOLTED[3]
        else:
            return VALUES_IMG_TENSIONBOLTED[4]


    def fn_profile_section(self):
        print(f"fn_profile_section self {self}")
        profile = self[0]
        print(f'profile = {self[0]}'
              f'VALUES_SEC_PROFILE_Compression_Strut {VALUES_SEC_PROFILE_Compression_Strut}')
        if profile == 'Beams':
            return connectdb("Beams", call_type="popup")
        elif profile == 'Columns':
            return connectdb("Columns", call_type="popup")
        elif profile == 'RHS':
            return connectdb("RHS", call_type="popup")
        elif profile == 'SHS':
            return connectdb("SHS", call_type="popup")
        elif profile == 'CHS':
            return connectdb("CHS", call_type="popup")
        elif profile in VALUES_SEC_PROFILE_Compression_Strut :
            print('done')
            return connectdb("Angles", call_type="popup")
        elif profile in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type="popup")


    def input_value_changed(self):

        lst = []

        t1 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t1)

        # if self[0] == 'Back to Back Angles':

        t3 = ([KEY_SEC_PROFILE], KEY_LOCATION, TYPE_COMBOBOX, self.fn_conn_type)
        lst.append(t3)

        t3 = ([KEY_SEC_PROFILE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t3)

        t2 = ([KEY_END1], KEY_END2, TYPE_COMBOBOX, self.fn_end1_end2)
        lst.append(t2)

        t3 = ([KEY_END1, KEY_END2], KEY_IMAGE_two, TYPE_IMAGE, self.fn_end2_image)
        lst.append(t3)

        return lst

    def output_values(self,flag):
        #flag for design status
        out_list = []
        optimisation = ''
        # if flag is True:
        #     if self.input_values is not VALUE_NOT_APPLICABLE:
        #         # print(f"input_values is not VALUE_NOT_APPLICABLE")
        #     else:
        #         # print(f"input_values is VALUE_NOT_APPLICABLE")
        t1 = (None, DISP_TITLE_STRUT_SECTION, TYPE_TITLE, None, True)

        out_list.append(t1)

        t1 = (KEY_TITLE_OPTIMUM_DESIGNATION, KEY_DISP_TITLE_OPTIMUM_DESIGNATION, TYPE_TEXTBOX, self.result_designation if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_OPTIMUM_UR_COMPRESSION, KEY_DISP_OPTIMUM_UR_COMPRESSION, TYPE_TEXTBOX, self.result_UR if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_OPTIMUM_SC, KEY_DISP_OPTIMUM_SC, TYPE_TEXTBOX, self.result_section_class if flag else '', True)
        out_list.append(t1)

        t2 = (KEY_EFF_SEC_AREA, KEY_DISP_EFF_SEC_AREA, TYPE_TEXTBOX, round(self.result_effective_area, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_EFF_LEN, KEY_DISP_EFF_LEN, TYPE_TEXTBOX, round(self.result_eff_len, 2) if flag else '',
        True)
        out_list.append(t2)

        t2 = (KEY_ESR, KEY_DISP_ESR, TYPE_TEXTBOX, round(self.result_eff_sr, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_SR_lambdavv, KEY_DISP_SR_lambdavv, TYPE_TEXTBOX, self.result_lambda_vv if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_SR_lambdapsi, KEY_DISP_SR_lambdapsi, TYPE_TEXTBOX, self.result_lambda_psi if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_EULER_BUCKLING_STRESS, KEY_DISP_EULER_BUCKLING_STRESS, TYPE_TEXTBOX, round(self.result_ebs, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_BUCKLING_CURVE, KEY_DISP_BUCKLING_CURVE, TYPE_TEXTBOX, self.result_bc if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_IMPERFECTION_FACTOR, KEY_DISP_IMPERFECTION_FACTOR, TYPE_TEXTBOX, round(self.result_IF, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_SR_FACTOR, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, round(self.result_srf, 2) if flag else '', True)
        out_list.append(t2)

        #
        # t2 = (KEY_SR_FACTOR, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, round(self.result_srf, 2) if flag else '', True)
        # out_list.append(t2)

        t2 = (KEY_NON_DIM_ESR, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, round(self.result_nd_esr, 2) if flag else '', True)
        out_list.append(t2)

        t1 = (None, KEY_DESIGN_COMPRESSION, TYPE_TITLE, None, True)
        out_list.append(t1)

        t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_DESIGN_STRENGTH_COMPRESSION, TYPE_TEXTBOX, round(self.result_capacity * 1e-3, 2) if flag else
        '', True)
        out_list.append(t1)

        t19 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX,
               int(round(22.02, 0)) if flag else '', True)
        out_list.append(t19)

        t8 = (None, DISP_TITLE_END_CONNECTION, TYPE_TITLE, None, True)
        out_list.append(t8)

        t8 = (None, DISP_TITLE_BOLTD, TYPE_TITLE, None, True)
        out_list.append(t8)

        # t9 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,
        #       int(self.bolt.bolt_diameter_provided) if flag else '', True)
        # out_list.append(t9)
        #
        # t10 = (
        # KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_grade_provided if flag else '',
        # True)
        # out_list.append(t10)
        #
        # t11 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
        #        round(self.bolt.bolt_shear_capacity / 1000, 2) if flag else '', True)
        # out_list.append(t11)
        #
        # bolt_bearing_capacity_disp = ''
        # if flag is True:
        #     if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
        #         bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
        #
        #         pass
        #     else:
        #         bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity
        #
        # t5 = (
        # KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        # out_list.append(t5)
        #
        # t5 = (KEY_REDUCTION_LONG_JOINT, KEY_DISP_REDUCTION_LONG_JOINT, TYPE_TEXTBOX,
        #       round(self.plate.beta_lj, 2) if flag else '', True)
        # out_list.append(t5)
        #
        # t5 = (KEY_REDUCTION_LARGE_GRIP, KEY_DISP_REDUCTION_LARGE_GRIP, TYPE_TEXTBOX,
        #       round(self.plate.beta_lg, 2) if flag else '', True)
        # out_list.append(t5)
        #
        # t13 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
        #        round(self.plate.bolt_capacity_red / 1000, 2) if flag else '', True)
        # out_list.append(t13)
        #
        # t14 = (KEY_OUT_BOLT_FORCE, KEY_OUT_DISP_BOLT_FORCE, TYPE_TEXTBOX,
        #        round(self.plate.bolt_force / 1000, 2) if flag else '', True)
        # out_list.append(t14)
        #
        # t17 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        # out_list.append(t17)
        #
        # t18 = (None, DISP_TITLE_GUSSET_PLATE, TYPE_TITLE, None, True)
        # out_list.append(t18)
        #
        # t19 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX,
        #        int(round(self.plate.thickness_provided, 0)) if flag else '', True)
        # out_list.append(t19)
        #
        # t20 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_MIN_HEIGHT, TYPE_TEXTBOX,
        #        int(round(self.plate.height, 0)) if flag else '', True)
        # out_list.append(t20)
        #
        # t21 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_MIN_LENGTH, TYPE_TEXTBOX,
        #        int(round(self.plate.length, 0)) if flag else '', True)
        # out_list.append(t21)
        #
        # t21 = (KEY_OUT_PLATE_YIELD, KEY_DISP_TENSION_YIELDCAPACITY, TYPE_TEXTBOX,
        #        (round(self.plate.tension_yielding_capacity / 1000, 2)) if flag else '', True)
        # out_list.append(t21)
        #
        # t21 = (KEY_OUT_PLATE_RUPTURE, KEY_DISP_TENSION_RUPTURECAPACITY, TYPE_TEXTBOX,
        #        (round(self.plate.tension_rupture_capacity / 1000, 2)) if flag else '', True)
        # out_list.append(t21)
        #
        # t21 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_DISP_TENSION_BLOCKSHEARCAPACITY, TYPE_TEXTBOX,
        #        (round(self.plate.block_shear_capacity / 1000, 2)) if flag else '', True)
        # out_list.append(t21)
        #
        # t17 = (KEY_OUT_PATTERN_2, KEY_OUT_DISP_PATTERN, TYPE_OUT_BUTTON, ['Shear Pattern ', self.plate_pattern], True)
        # out_list.append(t17)
        #
        # t21 = (KEY_OUT_PLATE_CAPACITY, KEY_DISP_TENSION_CAPACITY, TYPE_TEXTBOX,
        #        (round(self.plate_tension_capacity / 1000, 2)) if flag else '', True)
        # out_list.append(t21)
        #
        # # if KEY_SEC_PROFILE in ['Back to Back Angles', 'Star Angles','Back to Back Channels']:
        #
        # t18 = (None, DISP_TITLE_INTERMITTENT, TYPE_TITLE, None, False)
        # out_list.append(t18)
        #
        # t8 = (None, DISP_TITLE_CONN_DETAILS, TYPE_TITLE, None, False)
        # out_list.append(t8)
        #
        # t21 = (KEY_OUT_INTERCONNECTION, KEY_OUT_DISP_INTERCONNECTION, TYPE_TEXTBOX,
        #        int(round(self.inter_conn, 0)) if flag else '', False)
        # out_list.append(t21)
        #
        # t21 = (KEY_OUT_INTERSPACING, KEY_OUT_DISP_INTERSPACING, TYPE_TEXTBOX,
        #        (round(self.inter_memb_length, 2)) if flag else '', False)
        # out_list.append(t21)
        #
        # t18 = (None, DISP_TITLE_BOLTD, TYPE_TITLE, None, False)
        # out_list.append(t18)
        #
        # t9 = (
        # KEY_OUT_INTER_D_PROVIDED, KEY_OUT_DISP_INTER_D_PROVIDED, TYPE_TEXTBOX, int(self.inter_dia) if flag else '',
        # False)
        # out_list.append(t9)
        #
        # t10 = (
        # KEY_OUT_INTER_GRD_PROVIDED, KEY_OUT_DISP_INTER_GRD_PROVIDED, TYPE_TEXTBOX, self.inter_grade if flag else '',
        # False)
        # out_list.append(t10)
        #
        # t15 = (
        # KEY_OUT_INTER_BOLT_LINE, KEY_OUT_DISP_INTER_BOLT_LINE, TYPE_TEXTBOX, self.inter_bolt_line if flag else '',
        # False)
        # out_list.append(t15)
        #
        # t16 = (KEY_OUT_INTER_BOLTS_ONE_LINE, KEY_OUT_DISP_INTER_BOLTS_ONE_LINE, TYPE_TEXTBOX,
        #        self.inter_bolt_one_line if flag else '', False)
        # out_list.append(t16)
        #
        # t18 = (None, DISP_TITLE_PLATED, TYPE_TITLE, None, False)
        # out_list.append(t18)
        #
        # t20 = (KEY_OUT_INTER_PLATE_HEIGHT, KEY_OUT_DISP_INTER_PLATE_HEIGHT, TYPE_TEXTBOX,
        #        int(round(self.inter_plate_height, 0)) if flag else '', False)
        # out_list.append(t20)
        #
        # t21 = (KEY_OUT_INTER_PLATE_LENGTH, KEY_OUT_DISP_INTER_PLATE_LENGTH, TYPE_TEXTBOX,
        #        int(round(self.inter_plate_length, 0)) if flag else '', False)
        # out_list.append(t21)


        return out_list
    def func_for_validation(self, design_dictionary):
        '''Need to check'''
        all_errors = []
        self.design_status = False
        flag = False
        flag1 = False
        flag2 = False
        option_list = self.input_values(self)
        print(f'\n func_for_validation option list = {option_list}'
              f'\n  design_dictionary {design_dictionary}')
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                # print(f"\n option {option}")
                if design_dictionary[option[0]] == '' and option[0] is not KEY_AXIAL:
                    # print(f'option, design_dictionary[option[0] = {option[0]},{design_dictionary[option[0]]}')
                    # if design_dictionary[KEY_AXIAL] == '':
                    #     continue
                    # else:
                    missing_fields_list.append(option[1])
                elif design_dictionary[option[0]] == '' and option[0] is KEY_AXIAL:
                    flag2 = True
                else:
                    if option[0] == KEY_LENGTH :
                        if float(design_dictionary[option[0]]) <= 0.0:
                            print("Input value(s) cannot be equal or less than zero.")
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True
                    elif option[0] == KEY_AXIAL :
                        if float(design_dictionary[option[0]]) <= 0.0:
                            print("Input value(s) cannot be equal or less than zero.")
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag2 = True
            elif option[2] == TYPE_COMBOBOX and option[0] not in [KEY_SEC_PROFILE, KEY_END1, KEY_END2, KEY_LOCATION, KEY_TYP]:
                val = option[3]
                if design_dictionary[option[0]] == val[0]:
                    # print(f'option[0] = {option[0]}')
                    missing_fields_list.append(option[1])
        # print(missing_fields_list)
        if len(missing_fields_list) > 0:

            error = self.generate_missing_fields_error_string(self,missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        print(f'flag = {flag}')
        if flag and flag1 and flag2:
            self.set_input_values(self, design_dictionary)
            # print(design_dictionary)
        else:
            return all_errors
        print(f"func_for_validation done")

    def fn_conn_type(self):

        "Function to populate section size based on the type of section "
        conn = self[0]
        if conn in VALUES_SEC_PROFILE_Compression_Strut:
            return VALUES_LOCATION_1
        else:
            print(f" chevk fn_conn_type ")

    # Setting inputs from the input dock GUI

    def set_input_values(self, design_dictionary):
        super(Flexure,self).set_input_values(self, design_dictionary)
        #self.sizelist == self.sec_list
        # section properties
        self.module = design_dictionary[KEY_MODULE]
        self.sizelist = design_dictionary[KEY_SECSIZE]

        self.design_type = KEY_DISP_DESIGN_TYPE_FLEXURE # or KEY_DISP_DESIGN_TYPE2_FLEXURE
        # self.design_type = design_dictionary[KEY_DESIGN_TYPE_FLEXURE]
        if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
            self.bending_type = KEY_DISP_BENDING1 # or KEY_DISP_BENDING2
            # self.bending_type = design_dictionary[KEY_BENDING]
            if self.bending_type == KEY_DISP_BENDING2:
                self.design_type = KEY_DISP_DESIGN_TYPE_FLEXURE
            elif self.bending_type == KEY_DISP_BENDING1 :
                self.lambda_lt = self.lambda_lt_check_member_type
                if self.lambda_lt <0.4:
                    self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE

        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]
        self.sec_list = design_dictionary[KEY_SECSIZE]
        self.length = float(design_dictionary[KEY_LENGTH])
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.material = design_dictionary[KEY_SEC_MATERIAL]

        #'support'
        self.support = design_dictionary[KEY_SUPPORT]

        # factored loads
        self.load = Load(shear_force=design_dictionary[KEY_SHEAR], axial_force='',moment=design_dictionary[KEY_MOMENT],unit_kNm=True)

        # design preferences
        # self.allowable_utilization_ratio = float(design_dictionary[KEY_ALLOW_UR])
        self.effective_area_factor = float(design_dictionary[KEY_EFFECTIVE_AREA_PARA])
        self.optimization_parameter = 'Utilization Ratio'
        self.allow_class = design_dictionary[KEY_ALLOW_CLASS] #if 'Semi-Compact' is available

        self.steel_cost_per_kg = 50
        '''Need to check'''
        if self.allow_class == 'Yes':
            self.allowed_sections == 'Semi-Compact'
        print(f"self.allowed_sections {self.allowed_sections}")
        print("==================")
        print(f"self.load_type {self.load_type}")

        print(f"self.module{self.module}")
        print(f"self.sec_list {self.sec_list}")
        print(f"self.material {self.material}")
        print(f"self.length {self.length}")
        print(f"self.load {self.load}")
        print(f"self.end_1,2 {self.end_1}, {self.end_2}")
        print("==================")

        # safety factors
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        self.gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]["yielding"]
        # material property
        self.material_property = Material(material_grade=self.material, thickness=0)
        print(f"self.material_property {self.material_property}]")


        # initialize the design status
        self.design_status_list = []
        self.design_status = False

        #initial properties of section
        self.sec_prop_initial_dict = {}

        # self.results(self)

        "Unknown keys"
        # if self.sec_profile == Profile_name_1 :
        self.K = self.in_plane * self.out_plane
        # elif self.sec_profile == 'Back to Back Angles':
        #     self.K = 0.85
        # elif self.sec_profile == 'Channels':
        #     print("========Unknown keys==========")
        #     self.K = 0.85
        # elif self.sec_profile == 'Back to Back Channels':
        #     print("========Unknown keys==========")
        #     self.K = 0.85

        # self.count = 0
        # self.member_design_status = False
        # self.max_limit_status_1 = False
        # self.max_limit_status_2 = False
        # self.bolt_design_status = False
        # self.plate_design_status = False
        # self.inter_status = False
        # self.thk_count =0

        print("K = {}.The input values are set. Performing preliminary member check(s).".format(self.K))
        # self.i = 0
        # checking input values
        # print(flag)
        # if flag:
        self.design(self, design_dictionary)
        self.results(self, design_dictionary)



    def select_section(self, selectedsize, design_dictionary):

        "selecting components class based on the section passed "
        print(f" \n select_section started \n")

        if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles']:
            # print(f"\n selectedsize {selectedsize},\n design_dictionary[KEY_SEC_MATERIAL]{design_dictionary[KEY_SEC_MATERIAL]}")
            self.section_size = Angle(designation=selectedsize, material_grade=design_dictionary[KEY_SEC_MATERIAL])
        else:
            pass
        print(f"\n select_section done \n")

        return self.section_size
        print(self.selectedsize)

    def get_3d_components(self):

        components = []
        return components

    def lambda_lt_check_member_type(self, Mcr = 0, fcrb= 0, Zp = 0, f_y = 0, Ze = 0, beta_b = 0):
        lambda_lt_1 = math.sqrt(beta_b * Zp * f_y / Mcr)
        lambda_lt_2 = math.sqrt(f_y/fcrb)
        lambda_lt_check = math.sqrt(1.2 * Ze * f_y / Mcr)
        if lambda_lt_1 == lambda_lt_2 :
            if lambda_lt_1 <= lambda_lt_check:
                return lambda_lt_1
        logger.warning(' Issues with the non-dimensional slenderness ratio Lambda_lt')

    def effective_length_beam(self, design_dictionary, length):
        if self.support == KEY_DISP_SUPPORT1:
            self.Torsional_res = design_dictionary[KEY_SUPPORT1]
            self.Warping = design_dictionary[KEY_SUPPORT2]
            self.Loading = design_dictionary[KEY_LOAD] #'Normal'or 'Destabilizing'
            self.length = IS800_2007.cl_8_3_1_EffLen_Simply_Supported(Torsional= self.Torsional_res, Warping= self.Warping,length=self.length, depth= self.section_property.depth, load = self.Loading)
        elif self.support == KEY_DISP_SUPPORT2:
            self.Support = design_dictionary[KEY_SUPPORT_TYPE]
            self.Top = design_dictionary[KEY_SUPPORT_TYPE2]
            self.Loading = design_dictionary[KEY_LOAD]  # 'Normal'or 'Destabilizing'
            self.length = IS800_2007.cl_8_3_3_EffLen_Cantilever(Support=self.Support, Top=self.Top,
                                                                 length=self.length, load=self.Loading)
        return length

    def input_modifier(self):
        """ Classify the sections based on Table 2 of IS 800:2007 """
        # print(f"Inside section_classification")
        local_flag = True
        self.input_mpdified = []
        self.input_section_list = []
        # self.input_section_classification = {}

        for section in self.sec_list:
            section = section.strip("'")
            self.section_property = self.section_conect_database(self, section)
            if self.allow_class:
                Zp_req =  self.load.moment * self.gamma_m0 / (self.material_property.fy * self.section_property.elast_sec_mod_z / self.section_property.plast_sec_mod_z)
            else:
                Zp_req = self.load.moment * self.gamma_m0 / self.material_property.fy

            if self.section_property.plast_sec_mod_z >= Zp_req:
                self.input_mpdified.append(section)


    def section_classification(self, trial_section = ''):
        """ Classify the sections based on Table 2 of IS 800:2007 """
        # print(f"Inside section_classification")
        local_flag = True
        self.input_section_list = []
        self.input_section_classification = {}

        for trial_section in self.input_mpdified:
            self.section_property = self.section_conect_database(self, trial_section)
            print(f"Type of section{self.section_property.designation}")

            # if self.section_property.elast_sec_mod_z >= Zp_req:
                # section classification
            if self.sec_profile != '':  # Angles or Back to Back or 'Star Angle'

                # updating the material property based on thickness of the thickest element
                # self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.thickness)
                if self.section_property.type == 'Rolled':
                    # print(f"\n \n \n self.material_property.fy {self.material_property.fy} \n \n \n")
                    web_class = IS800_2007.Table2_iii(self.section_property.depth, self.section_property.web_thickness, self.material_property.fy)
                    flange_class = IS800_2007.Table2_i(self.section_property.flange_width/2, self.section_property.web_thickness, self.material_property.fy)[0]

                else:
                    '''Need to check below formula '''
                    flange_class = IS800_2007.Table2_i(
                        ((self.section_property.flange_width / 2) - (self.section_property.web_thickness / 2)),
                        self.section_property.flange_thickness, self.section_property.fy,
                        self.section_property.type)[0]

                    web_class = IS800_2007.Table2_iii(
                        (self.section_property.depth - (2 * self.section_property.flange_thickness)),
                        self.section_property.web_thickness, self.material_property.fy,
                        classification_type='Axial compression')

            if flange_class == 'Slender' or web_class == 'Slender':
                self.section_class = 'Slender'
            else:
                if flange_class == 'Plastic' and web_class == 'Plastic':
                    self.section_class = 'Plastic'
                elif flange_class == 'Plastic' and web_class == 'Compact':
                    self.section_class = 'Compact'
                elif flange_class == 'Plastic' and web_class == 'Semi-Compact':
                    self.section_class = 'Semi-Compact'
                elif flange_class == 'Compact' and web_class == 'Plastic':
                    self.section_class = 'Compact'
                elif flange_class == 'Compact' and web_class == 'Compact':
                    self.section_class = 'Compact'
                elif flange_class == 'Compact' and web_class == 'Semi-Compact':
                    self.section_class = 'Semi-Compact'
                elif flange_class == 'Semi-Compact' and web_class == 'Plastic':
                    self.section_class = 'Semi-Compact'
                elif flange_class == 'Semi-Compact' and web_class == 'Compact':
                    self.section_class = 'Semi-Compact'
                elif flange_class == 'Semi-Compact' and web_class == 'Semi-Compact':
                    self.section_class = 'Semi-Compact'

            logger.info(
                "The section is {}. The b/tf of the trial section ({}) is {} and d/tw is {} and (b+d)/t is {}.  [Reference: Cl 3.7, IS 800:2007].".format(
                    self.section_class, trial_section, round(flange_class, 2),
                    round_up(web_class, 2)))



            if self.allow_class :
                if self.section_class == 'Semi-Compact' or  self.section_class == 'Compact' or  self.section_class == 'Plastic':
                    self.input_section_list.append(trial_section)
                elif self.section_class == 'Slender':
                    logger.warning(f"The section.{trial_section} is Slender. Ignoring")
            else:
                if self.section_class == 'Compact' or  self.section_class == 'Plastic':
                    self.input_section_list.append(trial_section)
                elif self.section_class == 'Slender':
                    logger.warning(f"The section.{trial_section} is Slender. Ignoring")
                    self.design_status = False
                    self.design_status_list.append(self.design_status)
                elif self.section_class == 'Semi-Compact':
                    logger.warning(f"The section.{trial_section} is Semi-Compact. Ignoring")
                    self.design_status = False
                    self.design_status_list.append(self.design_status)


        if len(self.input_section_list) == 0:
            local_flag = False
        else:
            local_flag = True
        return local_flag
            # print(f"self.section_class{self.section_class}")
    def bending_strength(self):
        # 4 - design bending strength -preliminary
        M_d = IS800_2007.cl_8_2_1_2_design_bending_strength(self.section_class,
                                                            self.section_property.plast_sec_mod_z,
                                                            self.section_property.elast_sec_mod_z,
                                                            self.material_property.fy,
                                                            self.gamma_m0, self.support)
        if self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE :
            if self.high_shear_check:
                if self.section_class == 'Plastic' or self.section_class == 'Compact':
                    self.bending_strength_section = self.bending_strength_reduction(M_d)
                else:
                    self.bending_strength_section = self.section_property.elast_sec_mod_z * self.material_property.fy * self.gamma_m0
            else:
                self.bending_strength_section = M_d
        else:
            It = (2 * self.section_property.flange_width * self.section_property.flange_thickness**3)/3 + ((self.section_property.depth - self.section_property.flange_thickness) * self.section_property.web_thickness**3) /3
            hf = self.section_property.depth - self.section_property.flange_thickness
            Iw = 0.5**2 * self.section_property.mom_inertia_y * hf**2
            M_cr = IS800_2007.cl_8_2_2_Unsupported_beam_bending_non_slenderness(self.material_property.modulus_of_elasticity,
                                                                                0.3,
                                                                                self.section_property.mom_inertia_y,
                                                                                It,
                                                                                Iw,
                                                                                self.effective_length)
            if self.section_class == 'Plastic' or self.section_class == 'Compact':
                beta_b = 1.0
            else:
                beta_b = self.section_property.elast_sec_mod_z/self.section_property.plast_sec_mod_z
            if self.section_property.type == 'Rolled':
                alpha_lt = 0.21
            else:
                alpha_lt = 0.49
            lambda_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_non_slenderness(beta_b,self.section_property.plast_sec_mod_z, self.section_property.elast_sec_mod_z, self.material_property.fy, M_cr)
            phi_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_phi_lt(alpha_lt, lambda_lt)
            X_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(phi_lt, lambda_lt)
            fcd = IS800_2007.cl_8_2_2_Unsupported_beam_bending_compressive_stress(X_lt, self.material_property.fy, self.gamma_m0)
            self.bending_strength_section = IS800_2007.cl_8_2_2_Unsupported_beam_bending_strength(self.section_property.plast_sec_mod_z, self.section_property.elast_sec_mod_z, fcd= fcd, section_class=self.section_class)
            if self.high_shear_check:
                if self.section_class == 'Plastic' or self.section_class == 'Compact':

                    self.bending_strength_section = self.bending_strength_reduction(self.bending_strength_section, )
                else:
                    self.bending_strength_section = self.section_property.elast_sec_mod_z * self.material_property.fy * self.gamma_m0

    def bending_strength_reduction(self, Md):
        Zfd = self.section_property.plast_sec_mod_z - (self.section_property.depth**2 * self.section_property.web_thickness)/4
        Mfd = Zfd * self.material_property.fy / self.gamma_m0
        beta = ((2 * self.load.shear_force / self.V_d) - 1)**2
        Mdv = Md - beta(Md - Mfd)
        if Mdv <= 1.2*self.section_property.plast_sec_mod_z * self.material_property.fy / self.gamma_m0:
            return Mdv
        else:
            return 1.2*self.section_property.plast_sec_mod_z * self.material_property.fy / self.gamma_m0

    #  ======Calculations start here====== #
    def optimization_tab_check(self):

        if (self.effective_area_factor <= 0.10) or (self.effective_area_factor > 1.0):
            logger.warning(
                "The defined value of Effective Area Factor in the design preferences tab is out of the suggested range.")
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default value of 1.0.")
            self.effective_area_factor = 1.0
            self.design_status = False
            self.design_status_list.append(self.design_status)

        elif (self.steel_cost_per_kg < 0.10) or (self.effective_area_factor > 1.0):
            # No suggested range in Description
            logger.warning(
                "The defined value of the cost of steel (in INR) in the design preferences tab is out of the suggested range.")
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default rate of 50 (INR/kg).")
            self.steel_cost_per_kg = 50
            self.design_status = False
            self.design_status_list.append(self.design_status)
        else:
            if self.effective_area_factor >= self.material_property.fy* self.gamma_m0 /(self.material_property.fu * 0.9 * self.gamma_m1) :
                pass
            else:
                self.effective_area_factor = self.material_property.fy* self.gamma_m0 /(self.material_property.fu * 0.9 * self.gamma_m1)
                logger.info(f"The effect of holes in the tension flange is considered on the design bending strength. The ratio of net to gross area of the flange in tension is considered {self.effective_area_factor}")

            logger.info("Provided appropriate design preference, now checking input.")

    def section_conect_database(self, section):
        print(f"Working correct here{section}")
        print(section)
        print(self.sec_profile)
        if self.sec_profile == VALUES_SECTYPE[1] or self.sec_profile == VALUES_SECTYPE[2] or self.sec_profile == 'I-section':  # I-section
            self.section_property = ISection(designation = section, material_grade = self.material)
            self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.web_thickness)
            self.epsilon = math.sqrt(250 / self.material_property.fy)
        return self.section_property

    def common_checks_1(self, section, step = 1, list_result = [], list_1 = []):
        if step == 1:
            pass

            # print(f"Working correct here")
        elif step == 2:
            if self.section_class == 'Slender':
                logger.warning("The trial section ({}) is Slender. Ignoring section.".format(section))


            # reduction of the area based on the connection requirements (input from design preferences)
            if self.effective_area_factor < 1.0:
                self.effective_area = round(self.effective_area * self.effective_area_factor, 2)

                logger.warning(
                    "Reducing the effective sectional area as per the definition in the Design Preferences tab.")
                logger.info(
                    "The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".
                    format(round((self.effective_area / self.effective_area_factor), 2), self.effective_area))
            else:
                if self.section_class != 'Slender':
                    logger.info(
                        "The effective sectional area is taken as 100% of the cross-sectional area [Reference: Cl. 7.3.2, IS 800:2007].")
        elif step == 3:
            # 2.1 - Buckling curve classification and Imperfection factor
            if (self.sec_profile in VALUES_SEC_PROFILE_Compression_Strut[:3]):
                self.buckling_class = 'c'
            else:
                print("section not valid")

            self.imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class=self.buckling_class)


        elif step == 4:
            print(f"\n data sent "
                  f" self.material_property.fy {self.material_property.fy}"
                  f"self.gamma_m0 {self.gamma_m0}"
                  f"self.slenderness {self.slenderness}"
                  f" self.imperfection_factor {self.imperfection_factor}"
                  f"self.section_property.modulus_of_elasticity {self.section_property.modulus_of_elasticity}")

            list_cl_7_1_2_1_design_compressisive_stress = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.material_property.fy, self.gamma_m0, self.slenderness, self.imperfection_factor,
                self.section_property.modulus_of_elasticity, check_type= list_result)
            for x in list_cl_7_1_2_1_design_compressisive_stress:
                print(f"x {x} ")
            self.euler_buckling_stress = list_cl_7_1_2_1_design_compressisive_stress[0]
            self.nondimensional_effective_slenderness_ratio = list_cl_7_1_2_1_design_compressisive_stress[1]
            self.phi = list_cl_7_1_2_1_design_compressisive_stress[2]
            self.stress_reduction_factor = list_cl_7_1_2_1_design_compressisive_stress[3]
            self.design_compressive_stress_fr = list_cl_7_1_2_1_design_compressisive_stress[4]
            self.design_compressive_stress = list_cl_7_1_2_1_design_compressisive_stress[5]
            self.design_compressive_stress_max = list_cl_7_1_2_1_design_compressisive_stress[6]
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
            print(f"\n self.optimum_section_cost_results {self.optimum_section_cost_results}"
                  f"\n self.optimum_section_ur_results {self.optimum_section_ur_results}")
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
        # elif step == 7:
        #     if self.section_property.thickness < 20:
        #         self.fy == self.section_property.fy_20
        #     elif self.section_property.thickness >= 20 and self.section_property.thickness < 40:
        #         self.fy = self.section_property.fy_20_40
        #     elif self.section_property.thickness >= 40:
        #         self.fy = self.section_property.fy_40
            # initial check


    def common_result(self, list_result,result_type, flag = 1):
            self.result_designation = list_result[result_type]['Designation']
            self.result_section_class = list_result[result_type]['Section class']
            self.result_effective_area = list_result[result_type]['Effective area']

            self.result_bc = list_result[result_type]['Buckling_class']
            # self.result_bc_yy = list_result[result_type]['Buckling_curve_yy']

            self.result_IF = list_result[result_type]['IF']
            # self.result_IF_yy = list_result[result_type]['IF_yy']

            self.result_eff_len = list_result[result_type]['Effective_length']
            # self.result_eff_len_yy = list_result[result_type]['Effective_length_yy']

            self.result_eff_sr = list_result[result_type]['Effective_SR']
            # self.result_eff_sr_yy = list_result[result_type]['Effective_SR_yy']
            self.result_lambda_vv = list_result[result_type]['lambda_vv']

            self.result_lambda_psi = list_result[result_type]['lambda_psi']


            self.result_ebs = list_result[result_type]['EBS']
            # self.result_ebs_yy = list_result[result_type]['EBS_yy']

            self.result_nd_esr = list_result[result_type]['ND_ESR']
#                 self.result_nd_esr_yy = list_result[result_type]['ND_ESR_yy']

            self.result_phi_zz = list_result[result_type]['phi']
#                 self.result_phi_yy = list_result[result_type]['phi_yy']

            self.result_srf = list_result[result_type]['SRF']
#                 self.result_srf_yy = list_result[result_type]['SRF_yy']

            self.result_fcd_1_zz = list_result[result_type]['FCD_formula']
#                 self.result_fcd_1_yy = list_result[result_type]['FCD_1_yy']

            self.result_fcd_2 = list_result[result_type]['FCD_max']

            # self.result_fcd_zz = list_result[result_type]['FCD_zz']
            # self.result_fcd_yy = list_result[result_type]['FCD_yy']

            self.result_fcd = list_result[result_type]['FCD']
            self.result_capacity = list_result[result_type]['Capacity']
            self.result_cost = list_result[result_type]['Cost']

    def design(self, design_dictionary , flag = 0):
        # flag = self.section_classification(self)
        # print(flag)
        """ Perform design of struct """
        # checking DP inputs
        self.optimization_tab_check(self)
        self.input_modifier(self)

        #
        # if design_dictionary[KEY_AXIAL] == '' and len(self.input_section_list) == 1 :
        #     self.single_result = {}
        #     logger.info("Provided appropriate input and starting design.")
        #
        #     self.strength_of_strut(self)
        # elif design_dictionary[KEY_AXIAL] != '' :
        #     if len(self.input_section_list) > 1 :
        #         logger.info("Provided appropriate input and starting design.")
        #
        #         self.design_beam(self)
        #     else:
        #         logger.warning(
        #             "No need for load input.")
        #         # logger.error("Cannot compute!")
        #         logger.info(" Ignoring load and starting design.")
        #         design_dictionary[KEY_AXIAL] = ''
        #
        #         self.strength_of_strut(self)
        #
        # else:
        #     # logger.warning(
        #     #     "More than 1 section given as input without giving Load")
        #     logger.warning("Cannot compute!")
        #     design_dictionary[KEY_AXIAL] == 1
        #     logger.info(" Taking load of 1 kN.")

            # logger.info("Give 1 section as Inputs and/or "
            #             "Give load and re-design.")
            # self.design_status = False
        if len(self.input_mpdified) != 0:
            self.design_beam(self, design_dictionary)


    def design_beam(self, design_dictionary):

        # initializing lists to store the optimum results based on optimum UR and cost
        # 1- Based on optimum UR
        self.optimum_section_ur_results = {}
        self.optimum_section_ur = []

        # 2 - Based on optimum cost
        self.optimum_section_cost_results = {}
        self.optimum_section_cost = []

        # 1 - section classification
        flag = self.section_classification(self)

        if flag:
            for section in self.input_section_list:
                # initialize lists for updating the results dictionary
                self.section_property = self.section_conect_database(self, section)

                # 2 - Effective length
                self.effective_length = self.effective_length_beam(design_dictionary=design_dictionary,
                                                                   length=self.length)  # mm
                print(f"self.effective_length {self.effective_length} ")

                # 3 - web buckling under shear
                web_buckling = IS800_2007.cl_8_2_1_web_buckling(d=self.section_property.depth,
                                                                tw=self.section_property.web_thickness, e=self.epsilon)

                if web_buckling:
                    logger.warning("Thin web [Reference: Cl 8.2.1.1, IS 800:2007]")
                else:

                    self.V_d = IS800_2007.cl_8_4_design_shear_strength(self.section_property.depth*self.section_property.web_thickness, self.material_property.fy)

                    self.high_shear_check = IS800_2007.cl_8_2_1_2_high_shear_check(self.load.shear_force, V_d)
                    # 4 -  design bending strength
                    self.bending_strength_section = self.bending_strength(self)



                list_result = []
                list_result.append(section)
                print(f"Common checks"
                      f"list_result {list_result}")

                # Step 1 - computing the effective sectional area
                self.section_class = self.input_section_classification[section][0]

                self.common_checks_1(self,section,step =2)
                # if self.loc == "Long Leg":
                #     self.max_depth =self.section_size_max.max_leg - self.section_size_max.thickness - self.section_size_max.root_radius
                # else:
                #     self.max_depth =self.section_size_max.min_leg - self.section_size_max.thickness - self.section_size_max.root_radius

                list_result.extend([self.section_class, self.effective_area])

                # Step 2 - computing the design compressive stress
                self.common_checks_1(self,section,step=3)
                list_result.extend([self.buckling_class, self.imperfection_factor, self.effective_length])



                if self.load_type == 'Concentric Load':
                    print(f"step == 4"
                          f"list_result {list_result}")
                    self.lambda_vv = 'NA'
                    self.lambda_psi = 'NA'
                    #step == 4
                    self.common_checks_1(self, section, step=4, list_result=['Concentric'])
                else:
                    # self.min_radius_gyration = min(self.section_property.rad_of_gy_y, self.section_property.rad_of_gy_z)
                    returned_list = IS800_2007.cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(
                        self.length, self.min_radius_gyration, self.section_property.leg_a_length,
                        self.section_property.leg_b_length, self.section_property.thickness, self.material_property.fy, 2, self.fixity)

                    self.equivalent_slenderness = returned_list[0]
                    self.lambda_vv =  round(returned_list[1],2)
                    self.lambda_psi =  round(returned_list[2],2)
                    self.k1 =  returned_list[3]
                    self.k2 =  returned_list[4]
                    self.k3 =  returned_list[5]
                    print(f"self.equivalent_slenderness {self.equivalent_slenderness} "
                          f" \n self.slenderness {self.slenderness} "
                          f" \n self.lambda_vv {self.lambda_vv} "
                          f" \n self.lambda_psi {self.lambda_psi} "
                          f" \n self.k1 {self.k1} "
                          f" \n self.k2 {self.k2} "
                          f" \n self.k3 {self.k3} ")
                    self.common_checks_1(self, section, step=4, list_result=['Leg', self.equivalent_slenderness])



                # 2.7 - Capacity of the section
                self.section_capacity = self.design_compressive_stress * self.effective_area  # N

                # 2.8 - UR
                self.ur = round(self.load.axial_force / self.section_capacity, 3)
                self.optimum_section_ur.append(self.ur)

                # 2.9 - Cost of the section in INR
                self.cost = (self.section_property.unit_mass * self.section_property.area * 1e-4) * self.length * \
                            self.steel_cost_per_kg
                self.optimum_section_cost.append(self.cost)

                list_result.extend([self.slenderness, self.euler_buckling_stress,
                                    self.lambda_vv, self.lambda_psi,
                                    self.nondimensional_effective_slenderness_ratio,
                                    self.phi, self.stress_reduction_factor,
                                    self.design_compressive_stress_fr,
                                    self.design_compressive_stress_max,
                                    self.design_compressive_stress,
                                    self.section_capacity, self.ur, self.cost]
                                   )

                # Step 3 - Storing the optimum results to a list in a descending order

                list_1 = ['Designation','Section class', 'Effective area', 'Buckling_class', 'IF',
                          'Effective_length', 'Effective_SR', 'EBS', 'lambda_vv', 'lambda_psi', 'ND_ESR', 'phi', 'SRF',
                          'FCD_formula', 'FCD_max', 'FCD', 'Capacity', 'UR', 'Cost']

                # step ==5
                #if len(self.input_section_list) != 1:
                # step ==5
                # else
                # step ==6
                self.common_checks_1(self, section, 5, list_result, list_1)
                # if len(self.input_section_list) != 1:
                #     pass
            #
            # else:
            #     self.common_checks_1(self, section, 6, list_result, list_1)
            #     break

        # else:
        #     logger.warning("The section(s) defined for performing the column design is/are not selected based on the selected Inputs and/or "
        #                    "Design Preferences")
        #     logger.error("Cannot compute!")
        #     logger.info("Change the Inputs and/or "
        #                    "Design Preferences provided and re-design.")
        #     self.design_status = False
        #     self.design_status_list.append(self.design_status)
        #     # print(f"design_status_list{self.design_status_list}")
    def strength_of_strut(self):
        # iterating the design over each section to find the most optimum section
        section = self.input_section_list[0]
        self.single_result = {}
        # Yield strength of steel
        # self.common_checks_1(self,section, step=7)

        # Common checks
        self.common_checks_1(self, section)
        # initialize lists for updating the results dictionary
        list_result = []
        list_result.append(section)
        print(f"Common checks"
              f"list_result {list_result}")

        # Step 1 - computing the effective sectional area
        self.section_class = self.input_section_classification[section]

        self.common_checks_1(self, section, 2)
        # if self.loc == "Long Leg":
        #     self.max_depth =self.section_size_max.max_leg - self.section_size_max.thickness - self.section_size_max.root_radius
        # else:
        #     self.max_depth =self.section_size_max.min_leg - self.section_size_max.thickness - self.section_size_max.root_radius

        list_result.extend([self.section_class, self.effective_area])

        # Step 2 - computing the design compressive stress
        self.common_checks_1(self, section, 3)
        list_result.extend([self.buckling_class, self.imperfection_factor, self.effective_length])

        # 2.3 - slenderness ratio
        self.min_radius_gyration = min(self.section_property.rad_of_gy_u, self.section_property.rad_of_gy_v)
        self.slenderness = self.effective_length / self.min_radius_gyration
        print(f"self.min_radius_gyration {self.min_radius_gyration}"
              f"self.slenderness {self.slenderness}")
        if self.load_type == 'Concentric Load':
            print(f"step == 4"
                  f"list_result {list_result}")
            self.lambda_vv = 'NA'
            self.lambda_psi = 'NA'
            # step == 4
            self.common_checks_1(self, section, step=4, list_result=['Concentric'])
        else:
            # self.min_radius_gyration = min(self.section_property.rad_of_gy_y, self.section_property.rad_of_gy_z)
            returned_list = IS800_2007.cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(
                self.length, self.min_radius_gyration, self.section_property.leg_a_length,
                self.section_property.leg_b_length, self.section_property.thickness, self.material_property.fy, 2,
                self.fixity)

            self.equivalent_slenderness = returned_list[0]
            self.lambda_vv = round(returned_list[1], 2)
            self.lambda_psi = round(returned_list[2], 2)
            self.k1 = returned_list[3]
            self.k2 = returned_list[4]
            self.k3 = returned_list[5]
            print(f"self.equivalent_slenderness {self.equivalent_slenderness} "
                  f" \n self.slenderness {self.slenderness} "
                  f" \n self.lambda_vv {self.lambda_vv} "
                  f" \n self.lambda_psi {self.lambda_psi} "
                  f" \n self.k1 {self.k1} "
                  f" \n self.k2 {self.k2} "
                  f" \n self.k3 {self.k3} ")
            self.common_checks_1(self, section, step=4, list_result=['Leg', self.equivalent_slenderness])

        # 2.7 - Capacity of the section
        self.section_capacity = self.design_compressive_stress * self.effective_area  # N

        # 2.9 - Cost of the section in INR
        self.cost = (self.section_property.unit_mass * self.section_property.area * 1e-4) * self.length * \
                    self.steel_cost_per_kg

        list_result.extend([self.slenderness, self.euler_buckling_stress,
                                self.lambda_vv, self.lambda_psi,
                                self.nondimensional_effective_slenderness_ratio,
                                self.phi, self.stress_reduction_factor,
                                self.design_compressive_stress_fr,
                                self.design_compressive_stress_max,
                                self.design_compressive_stress,
                                self.section_capacity,"NA", self.cost]
                           )
        print(f"list_result {list_result}")
        # Step 3 - Storing the optimum results to a list in a descending order

        list_1 = ['Designation', 'Section class', 'Effective area', 'Buckling_class', 'IF',
                  'Effective_length', 'Effective_SR', 'EBS', 'lambda_vv', 'lambda_psi', 'ND_ESR', 'phi', 'SRF',
                  'FCD_formula', 'FCD_max', 'FCD', 'Capacity', 'UR', 'Cost']

        self.common_checks_1(self, section, step = 6, list_result= list_result, list_1= list_1)
        #     break

    def results(self,design_dictionary):
        """ """
        # sorting results from the dataset
        if len(self.input_section_list) > 1 :
            if design_dictionary[KEY_AXIAL] != '':
                # results based on UR
                if self.optimization_parameter == 'Utilization Ratio':
                    filter_UR = filter(lambda x: x <= min(self.allowable_utilization_ratio, 1.0), self.optimum_section_ur)
                    self.optimum_section_ur = list(filter_UR)

                    self.optimum_section_ur.sort()
                    # print(f"self.optimum_section_ur{self.optimum_section_ur}")
                    #print(f"self.result_UR{self.result_UR}")

                    # selecting the section with most optimum UR
                    if len(self.optimum_section_ur) == 0:  # no design was successful
                        logger.warning("The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                                        "criteria")
                        logger.error("The solver did not find any adequate section from the defined list.")
                        logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                        self.design_status = False
                        self.design_status_list.append(self.design_status)

                    else:
                        self.result_UR = self.optimum_section_ur[-1]  # optimum section which passes the UR check
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
                        "criteria")
                    logger.error("The solver did not find any adequate section from the defined list.")
                    logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                    self.design_status = False
                    self.design_status_list.append(self.design_status)
                    pass
                else:
                    if self.optimization_parameter == 'Utilization Ratio':
                        self.common_result(self, list_result=self.optimum_section_ur_results, result_type=self.result_UR)
                    else:
                        self.result_UR = self.optimum_section_cost_results[self.result_cost]['UR']

                        # checking if the selected section based on cost satisfies the UR
                        if self.result_UR > min(self.allowable_utilization_ratio, 1.0):

                            trial_cost = []
                            for cost in self.optimum_section_cost:
                                self.result_UR = self.optimum_section_cost_results[cost]['UR']
                                if self.result_UR <= min(self.allowable_utilization_ratio, 1.0):
                                    trial_cost.append(cost)

                            trial_cost.sort()

                            if len(trial_cost) == 0:  # no design was successful
                                logger.warning("The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                                                "criteria")
                                logger.error("The solver did not find any adequate section from the defined list.")
                                logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                                self.design_status = False
                                self.design_status_list.append(self.design_status)
                                print(f"design_status_list{self.design_status} \n")
                            else:
                                self.result_cost = trial_cost[0]  # optimum section based on cost which passes the UR check
                                self.design_status = True

                        # results
                        self.common_result(self, list_result=self.optimum_section_cost_results, result_type=self.result_cost)

                        print(f"design_status_list2{self.design_status}")
                for status in self.design_status_list:
                    if status is False:
                        self.design_status = False
                        break
                    else:
                        self.design_status = True
            else:
                logger.warning(
                    "More than 1 section given as input without giving Load")
                logger.error("Cannot compute!")
                logger.info("Give 1 section as Inputs and/or "
                            "Give load and re-design.")
                self.design_status = False
                self.design_status_list.append(self.design_status)
            if self.design_status:
                logger.info(": ========== Design Status ============")
                logger.info(": Overall Column design is SAFE")
                logger.info(": ========== End Of Design ============")
            else:
                logger.info(": ========== Design Status ============")
                logger.info(": Overall Column design is UNSAFE")
                logger.info(": ========== End Of Design ============")
        else:

            print(f"self.single_result {self.single_result}"
                  )
            self.common_result(self, list_result=self.single_result,result_type= self.sec_profile, flag= 1)
            self.design_status = True
            self.result_UR = self.single_result[self.sec_profile]['UR']
            if self.design_status:
                logger.info(": ========== Capacity Status ============")
                logger.info(": Section satisfies input")
                logger.info(": Section strength found")
                logger.info(": ========== End Of Status ============")
            else:
                logger.info(": ========== Capacity Status ============")
                logger.info(": Section does not satisfies input")
                logger.info(": Section strength NOT found")
                logger.info(": ========== End Of Status ============")
        # end of the design simulation
        # overall design status




    ### start writing save_design from here!
    def save_design(self, popup_summary):

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
                select_section_img = "Parallel_Beam"

            # column section properties
        if self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                section_type = 'Square Hollow Section (SHS)'
            elif self.dp_column_designation[1:4] == 'RHS':
                section_type = 'Rectangular Hollow Section (RHS)'
            else:
                section_type = 'Circular Hollow Section (CHS)'
        else:
            section_type = 'I Section'


        if self.section_property=='Columns' or self.section_property=='Beams':
            self.report_column = {KEY_DISP_SEC_PROFILE: "ISection",
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
            {KEY_MAIN_MODULE: self.mainmodule,
                KEY_MODULE: self.module, #"Axial load on column "
                KEY_DISP_SECTION_PROFILE: self.sec_profile,
                KEY_MATERIAL: self.material,
                KEY_DISP_ACTUAL_LEN_ZZ: self.length_zz,
                KEY_DISP_ACTUAL_LEN_YY: self.length_yy,
                KEY_DISP_END1: self.end_1,
                KEY_DISP_END2: self.end_2,
                KEY_DISP_AXIAL: self.load,
                KEY_DISP_SEC_PROFILE: self.sec_profile,
                KEY_DISP_SECSIZE: self.result_section_class,
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.euler_bs_yy,
                KEY_DISP_YIELD_STRENGTH_REPORT: self.result_bc_yy,


                "Column Section - Mechanical Properties": "TITLE",
                "Section Details": self.report_column,
                }

        self.report_check = []

        self.h = (self.beam_D - (2 * self.beam_tf))

        #1.1 Input sections display
        t1 = ('SubSection', 'List of Input Sections',self.input_section_list),
        self.report_check.append(t1)

        # 2.2 CHECK: Buckling Class - Compatibility Check
        t1 = ('SubSection', 'Buckling Class - Compatibility Check', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{2cm}|')
        self.report_check.append(t1)

        t1 = ("h/bf , tf ", comp_column_class_section_check_required(self.bucklingclass, self.h, self.bf),
                comp_column_class_section_check_provided(self.bucklingclass, self.h, self.bf, self.tf, self.var_h_bf),
                'Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        self.report_check.append(t1)

        # 2.3 CHECK: Cross-section classification
        t1 = ('SubSection', 'Cross-section classification', '|p{4.5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = ("b/tf and d/tw ", cross_section_classification_required(self.section),
                cross_section_classification_provided(self.tf, self.b1, self.epsilon, self.section, self.b1_tf,
                                                    self.d1_tw, self.ep1, self.ep2, self.ep3, self.ep4),
                'b = bf / 2,d = h – 2 ( T + R1),έ = (250 / Fy )^0.5,Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        self.report_check.append(t1)

        # 2.4 CHECK : Member Check
        t1 = ("Slenderness", cl_7_2_2_slenderness_required(self.KL, self.ry, self.lamba),
                cl_7_2_2_slenderness_provided(self.KL, self.ry, self.lamba), 'PASS')
        self.report_check.append(t1)

        t1 = (
        "Design Compressive stress (fcd)", cl_7_1_2_1_fcd_check_required(self.gamma_mo, self.f_y, self.f_y_gamma_mo),
        cl_7_1_2_1_fcd_check_provided(self.facd), 'PASS')
        self.report_check.append(t1)

        t1 = ("Design Compressive strength (Pd)", cl_7_1_2_design_comp_strength_required(self.axial),
                cl_7_1_2_design_comp_strength_provided(self.Aeff, self.facd, self.A_eff_facd), "PASS")
        self.report_check.append(t1)

        t1 = ('', '', '', '')
        self.report_check.append(t1)
        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                                rel_path, module=self.module)

    # def memb_pattern(self, status):
    #
    #     if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
    #         image = './ResourceFiles/images/L.png'
    #         x, y = 400, 202
    #
    #     else:
    #         image = './ResourceFiles/images/U.png'
    #         x, y = 400, 202
    #
    #
    #     pattern = []
    #
    #     t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
    #     pattern.append(t00)
    #
    #     t99 = (None, 'Failure Pattern due to Tension in Member', TYPE_IMAGE,
    #            [image, x, y, "Member Block Shear Pattern"])  # [image, width, height, caption]
    #     pattern.append(t99)
    #
    #     return pattern
    #
    # def plate_pattern(self, status):
    #
    #     pattern = []
    #
    #     t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
    #     pattern.append(t00)
    #
    #     t99 = (None, 'Failure Pattern due to Tension in Plate', TYPE_IMAGE,
    #            ['./ResourceFiles/images/L.png',400,202, "Plate Block Shear Pattern"])  # [image, width, height, caption]
    #     pattern.append(t99)
    #
    #     return pattern