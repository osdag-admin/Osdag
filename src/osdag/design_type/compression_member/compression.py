# noinspection PyInterpreter
from ..member import Member
from ...Common import *
from ...utils.common.component import ISection, Material
from ...utils.common.common_calculation import *
from ...utils.common.load import Load
from ..tension_member import *
from ...utils.common.Section_Properties_Calculator import BBAngle_Properties
import math
import numpy as np
from ...utils.common import is800_2007
from ...utils.common.component import *

import logging
from ..connection.moment_connection import MomentConnection
from ...utils.common.material import *
from ...Report_functions import *
from ...design_report.reportGenerator_latex import CreateLatex
from pylatex.utils import NoEscape


class Compression(Member):

    def __init__(self):
        # print(f"Here Compression")
        super(Compression, self).__init__()

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

        t1 = (DISP_TITLE_ANGLE, TYPE_TAB_1, self.tab_strut_angle_section)
        tabs.append(t1)

        # t2 = (DISP_TITLE_CHANNEL, TYPE_TAB_1, self.tab_strut_channel_section)
        # tabs.append(t2)

        t2 = ("Optimization", TYPE_TAB_2, self.optimization_tab_strut_design)
        tabs.append(t2)

        # t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)#plate_connector_values
        # tabs.append(t6)

        # t3 = ("Bolt", TYPE_TAB_2, self.bolt_strut_design)
        # tabs.append(t3)

        # t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        # tabs.append(t4)

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

        t1 = (DISP_TITLE_ANGLE, [KEY_SECSIZE, KEY_SEC_MATERIAL,'Label_0'],
              [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5',
               'Label_7', 'Label_8', 'Label_9',
               'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17',
               'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23', 'Label_24', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_strut_angle_section_properties)
        change_tab.append(t1)

        t2 = (DISP_TITLE_ANGLE, ['Label_1', 'Label_2', 'Label_3','Label_0'],
              ['Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15',
               'Label_16', 'Label_17', 'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23',
               KEY_IMAGE],
              TYPE_TEXTBOX, self.get_Strut_Angle_sec_properties)
        change_tab.append(t2)

        # t3 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE, KEY_SEC_MATERIAL, 'Label_0'],
        #       [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14',
        #        'Label_4', 'Label_5',
        #        'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17',
        #        'Label_19', 'Label_20', 'Label_21',
        #        'Label_22', 'Label_23', 'Label_26', 'Label_27', KEY_IMAGE], TYPE_TEXTBOX,
        #       self.get_new_channel_section_properties)
        # change_tab.append(t3)
        #
        # t4 = (DISP_TITLE_CHANNEL, ['Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14'],
        #       ['Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17', 'Label_19',
        #        'Label_20', 'Label_21', 'Label_22', 'Label_26', 'Label_27', KEY_IMAGE], TYPE_TEXTBOX,
        #       self.get_Channel_sec_properties)
        #
        # change_tab.append(t4)

        # t5 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
        #                                               KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        #
        # change_tab.append(t5)

        t6 = (DISP_TITLE_ANGLE, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

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

        t2 = (DISP_TITLE_ANGLE, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        # t2 = (DISP_TITLE_CHANNEL, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        # design_input.append(t2)

        t2 = ("Optimization", TYPE_TEXTBOX, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA, KEY_Buckling_Out_plane, KEY_Buckling_In_plane, KEY_BOLT_Number ]) #KEY_ALLOW_UR, , KEY_STEEL_COST
        design_input.append(t2)

        t2 = ("Optimization", TYPE_COMBOBOX, [ KEY_ALLOW_LOAD, Load_type2, Load_type1, KEY_PLATETHK ]) # KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS,
        design_input.append(t2)

        # t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        # design_input.append(t3)

        # t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        # design_input.append(t5)
        #
        # t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DETAILING_EDGE_TYPE])
        # design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        # t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        # design_input.append(t7)

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

        t2 = (None, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA, KEY_Buckling_Out_plane, KEY_Buckling_In_plane,
                     KEY_DP_DESIGN_METHOD, KEY_ALLOW_LOAD, KEY_BOLT_Number, KEY_PLATETHK
                     ], '')#, KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS, KEY_STEEL_COST, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_EDGE_TYPE,KEY_DP_DETAILING_GAP,
                     # KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_CONNECTOR_MATERIAL , KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
        design_input.append(t2)

        # t2 = (None, [KEY_DP_DESIGN_METHOD], '')
        # design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

        :return: This function returns list of tuples which has keys that needs to be updated,
         on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

         [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
        """
        add_buttons = []

        t2 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              VALUES_SEC_PROFILE_Compression_Strut , Profile_name_1)
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
            KEY_Buckling_Out_plane: '1.0',
            KEY_Buckling_In_plane: '1.0',
            KEY_ALLOW_LOAD: Load_type1,
            KEY_BOLT_Number: '1.0',
            KEY_ALLOW_LOAD: 'Concentric Load',
            KEY_DP_DESIGN_METHOD: "Limit State Design",
            KEY_PLATETHK : '8'
        }[key]

        return val

    ####################################
    # Design Preference Functions End
    ####################################

    def module_name(self):
        return KEY_DISP_COMPRESSION_Strut

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
        # t2 = (KEY_GRD, self.grdval_customized)
        # c_lst.append(t2)
        # t3 = (KEY_D, self.diam_bolt_customized)
        # c_lst.append(t3)
        # # # t3= (KEY_IMAGE, self.fn_conn_image)
        # # # c_lst.append(t3)
        # t4 = (KEY_PLATETHK, self.plate_thick_customized_IS)
        # c_lst.append(t4)

        # t4 = (KEY_PLATETHK, self.plate_thick_customized)
        # c_lst.append(t4)

        return c_lst

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair
        self.module = KEY_DISP_COMPRESSION_Strut
        options_list = []

        t1 = (KEY_MODULE, KEY_DISP_COMPRESSION_Strut, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t1)

        t1 = (None, KEY_SECTION_DATA, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, VALUES_SEC_PROFILE_Compression_Strut, True, 'No Validator')
        options_list.append(t2)

        # print(f'input_values {self},t2 :{t2} ')
        # if self[0] == 'Back to Back Angles':
        #     t2 = (KEY_SEC_TYPE, KEY_DISP_SEC_TYPE, TYPE_COMBOBOX, ['Same Side of Gusset', 'Opposite Side of Gusset'], True,
        #           'No Validator')
        #     options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, VALUES_IMG_STRUT[0], True, 'No Validator')
        options_list.append(t3)

        t3 = (KEY_LOCATION, KEY_DISP_LOCATION_STRUT, TYPE_COMBOBOX, VALUES_LOCATION_1, True, 'No Validator')
        options_list.append(t3)

        # ([KEY_SEC_PROFILE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)

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

        t12 = (KEY_IMAGE_two, None, TYPE_IMAGE_COMPRESSION, str(files("osdag.data.ResourceFiles.images").joinpath("6.RRRR.PNG")), True, 'No Validator')
        options_list.append(t12)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        # t8 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        # options_list.append(t8)
        #
        # t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        # options_list.append(t10)
        #
        # t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        # options_list.append(t11)
        #
        # t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        # options_list.append(t12)
        #
        # t13 = (None, KEY_DISP_GUSSET, TYPE_TITLE, None, True, 'No Validator')
        # options_list.append(t13)
        #
        # # try:
        # #     if self.sec_profile != 'Back to Back Angles':
        # #         t14 = (KEY_PLATETHK, KEY_GUSSET, TYPE_TEXTBOX, ' ', True, 'No Validator')
        #
        # t14 = (KEY_PLATETHK, KEY_GUSSET, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK, True, 'No Validator')
        # options_list.append(t14)

        return options_list

    def spacing(self, status):

        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Spacing Details based on member's depth \n (root radius not included in edge distance)")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
               [str(files("osdag.data.ResourceFiles.images").joinpath("spacing_1.png")), 400, 278, "3 x 3 pattern considered"])  # [image, width, height, caption]
        spacing.append(t99)

        if self.sec_profile == 'Star Angles':
            t16 = (KEY_OUT_BOLTS_ONE_LINE_S, KEY_OUT_DISP_BOLTS_ONE_LINE_S, TYPE_TEXTBOX,
                   int(self.plate.bolts_one_line/2) if status else '', True)
            spacing.append(t16)
        else:
            pass

        t16 = (KEY_OUT_BOLTS_ONE_LINE, KEY_OUT_DISP_BOLTS_ONE_LINE, TYPE_TEXTBOX, self.plate.bolts_one_line if status else '',True)
        spacing.append(t16)

        t15 = (KEY_OUT_BOLT_LINE, KEY_OUT_DISP_BOLT_LINE, TYPE_TEXTBOX, self.plate.bolt_line if status else '', True)
        spacing.append(t15)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def memb_pattern(self, status):

        if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
            image = str(files("osdag.data.ResourceFiles.images").joinpath("L.png"))
            x, y = 400, 202

        else:
            image = str(files("osdag.data.ResourceFiles.images").joinpath("U.png"))
            x, y = 400, 202


        pattern = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
        pattern.append(t00)

        t99 = (None, 'Failure Pattern due to Tension in Member', TYPE_IMAGE,
               [image, x, y, "Member Block Shear Pattern"])  # [image, width, height, caption]
        pattern.append(t99)

        return pattern

    def plate_pattern(self, status):

        pattern = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
        pattern.append(t00)

        t99 = (None, 'Failure Pattern due to Tension in Plate', TYPE_IMAGE,
               [str(files("osdag.data.ResourceFiles.images").joinpath("L.png")),400,202, "Plate Block Shear Pattern"])  # [image, width, height, caption]
        pattern.append(t99)

        return pattern

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

    def fn_conn_image(self):

        "Function to populate section images based on the type of section "
        img = self[0]
        if img == VALUES_SEC_PROFILE_Compression_Strut[0]:
            return VALUES_IMG_STRUT[0]
        elif img ==VALUES_SEC_PROFILE_Compression_Strut[1]:
            return VALUES_IMG_STRUT[2]
        elif img == VALUES_SEC_PROFILE_Compression_Strut[2]:
            return VALUES_IMG_STRUT[1]
        elif img == VALUES_SEC_PROFILE_Compression_Strut[3]:
            print(' fn_conn_image error')
            return VALUES_IMG_TENSIONBOLTED[3]
        else:
            return VALUES_IMG_TENSIONBOLTED[4]


    def fn_profile_section(self):
        #print(f"fn_profile_section self {self}")
        profile = self[0]
        # print(f'profile = {self[0]}'
        #       f'VALUES_SEC_PROFILE_Compression_Strut {VALUES_SEC_PROFILE_Compression_Strut}')
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
            # print('done')
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

        t2 = (KEY_NON_DIM_ESR, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, round(self.result_nd_esr, 2) if flag else '', True)
        out_list.append(t2)

        t1 = (None, KEY_DESIGN_COMPRESSION, TYPE_TITLE, None, True)
        out_list.append(t1)

        t1 = (KEY_COMP_STRESS, KEY_DISP_COMP_STRESS, TYPE_TEXTBOX,
              round(self.result_fcd * 1e-3, 2) if flag else
              '', True)
        out_list.append(t1)

        t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_DESIGN_STRENGTH_COMPRESSION, TYPE_TEXTBOX, round(self.result_capacity * 1e-3, 2) if flag else
        '', True)
        out_list.append(t1)

        # t19 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX,
        #        int(round(22.02, 0)) if flag else '', True)
        # out_list.append(t19)
        #
        # t8 = (None, DISP_TITLE_END_CONNECTION, TYPE_TITLE, None, True)
        # out_list.append(t8)
        #
        # t8 = (None, DISP_TITLE_BOLTD, TYPE_TITLE, None, True)
        # out_list.append(t8)

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
        print(f'\n func_for_validation ' #option list = {option_list}
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
                            # print("Input value(s) cannot be equal or less than zero.")
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True
                    elif option[0] == KEY_AXIAL :
                        if float(design_dictionary[option[0]]) <= 0.0:
                            #print("Input value(s) cannot be equal or less than zero.")
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

        #print(f'flag = {flag}')
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
        print(f"func_for_validation done")


    def get_3d_components(self):

        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        return components

    def fn_conn_type(self):

        "Function to populate section size based on the type of section "
        conn = self[0]
        if conn in VALUES_SEC_PROFILE_Compression_Strut:
            return VALUES_LOCATION_1
        else:
            print(f" chevk fn_conn_type ")

    # Setting inputs from the input dock GUI

    def set_input_values(self, design_dictionary):
        super(Compression,self).set_input_values(self, design_dictionary)
        #self.sizelist == self.sec_list
        # section properties
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = 'Struts in Trusses'
        self.sizelist = design_dictionary[KEY_SECSIZE]
        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]
        self.sec_list = design_dictionary[KEY_SECSIZE]
        self.length = float(design_dictionary[KEY_LENGTH])
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.material = design_dictionary[KEY_SEC_MATERIAL]
        # try :
        self.in_plane = float(design_dictionary[KEY_Buckling_In_plane])
        self.out_plane = float(design_dictionary[KEY_Buckling_Out_plane])
        if KEY_BOLT_Number not in design_dictionary:
            self.bolts = 0.0
        else:
            self.bolts = float(design_dictionary[KEY_BOLT_Number])

        if KEY_PLATETHK not in design_dictionary:
            self.plate_thickness = 0.0
        else:
            # Gusset plate details
            self.plate_thickness = float(design_dictionary[KEY_PLATETHK])

        # self.plate_grade = design_dictionary[KEY_SEC_MATERIAL]
        print(f"plate_thickness {self.plate_thickness} \n"
            f"self.in_plane {self.in_plane} \n"
              f"self.out_plane {self.out_plane} \n"
              f"self.bolts {self.bolts} \n"
            "========Unknown keys==========")
        print("character",[chr(code) for code in range(945,970)])


        #'Conn_Location'
        self.loc = design_dictionary[KEY_LOCATION]


        # self.load_type = 'Concentric Load'


        # end condition
        self.end_1 = design_dictionary[KEY_END1]
        self.end_2 = design_dictionary[KEY_END2]
        if self.end_1 == 'Fixed' and self.end_2 == 'Fixed':
            self.fixity = 'Fixed'
        elif (self.end_1 == 'Fixed' and self.end_2 == 'Hinged') or (self.end_1 == 'Hinged' and self.end_2 == 'Fixed') :
            self.fixity = 'Partial'
        else:
            self.fixity = 'Hinged'
            
        # factored loads
        self.load = Load(shear_force="", axial_force=design_dictionary[KEY_AXIAL],moment="",unit_kNm=True)

        # design preferences
        self.allowable_utilization_ratio = float(design_dictionary[KEY_ALLOW_UR])
        self.effective_area_factor = float(design_dictionary[KEY_EFFECTIVE_AREA_PARA])
        self.optimization_parameter = 'Utilization Ratio'
        self.allow_class = 'Semi-Compact'
        self.load_type = design_dictionary[KEY_ALLOW_LOAD]
        # ['Concentric Load', 'Leg Load']
        # if self.sec_profile == 'Angles':
        self.load_type = design_dictionary[KEY_ALLOW_LOAD]
        # else:
        #     self.load_type = 'Concentric Load'
        self.steel_cost_per_kg = 50
        self.allowed_sections = []

        # if self.allow_class == "Yes":
        self.allowed_sections.append('Semi-Compact')
            # print(f"Allowed Semi-Compact")
        '''Need to check'''
        # if self.allow_class4 == "Yes":
        #     self.allowed_sections.append('Slender')

        print(f"self.allowed_sections {self.allowed_sections} \n"
        "================== \n"
        f"self.load_type {self.load_type} \n"
        f"self.module{self.module} \n"
        f"self.sec_list {self.sec_list} \n"
        f"self.material {self.material} \n"
        f"self.length {self.length} \n"
        f"self.load {self.load} \n"
        f"self.end_1,2 {self.end_1}, {self.end_2} \n"
        "==================")

        # safety factors
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        # material property
        self.material_property = Material(material_grade=self.material, thickness=0)
        # print(f"self.material_property {self.material_property}]")


        # initialize the design status
        self.design_status_list = []
        self.design_status = False

        #initial properties of section
        self.sec_prop_initial_dict = {}

        # self.results(self)

        "Unknown keys"
        # if self.sec_profile == Profile_name_1 :
        self.K = self.in_plane * self.out_plane
        self.K = self.K * IS800_2007.cl_7_2_2_effective_length_of_prismatic_compression_members(
            self.length,
            end_1=self.end_1,
            end_2=self.end_2) / self.length

        # 2.2 - Effective length

        self.effective_length = self.K * self.length  # IS800_2007.cl_7_2_4_effective_length_of_truss_compression_members(self.length,self.sec_profile)/ self.length  # mm
        print(f"self.effective_length {self.effective_length} ")
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

        print("K = {}.\n The input values are set. Performing preliminary member check(s).".format(self.K))
        # self.i = 0
        # checking input values
        self.failed_design_dict = {}
        flag = self.section_classification(self)
        if len(self.input_section_list) == 0:
            flag == False
        if flag:
            self.design(self)
            self.results(self)


        # self.initial_member_capacity(self,design_dictionary)
        # print(f"self.sec_list {self.sec_list}")
        # for selectedsize in self.sec_list:
        #     # print(f"selectedsize{selectedsize}")
        #     self.select_section(self,selectedsize, design_dictionary)

    # def select_section(self, selectedsize, design_dictionary):
    #
    #     "selecting components class based on the section passed "
    #     print(f" \n select_section started \n")
    #
    #     if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles']:
    #         # print(f"\n selectedsize {selectedsize},\n design_dictionary[KEY_SEC_MATERIAL]{design_dictionary[KEY_SEC_MATERIAL]}")
    #         self.section_size = Angle(designation=selectedsize, material_grade=design_dictionary[KEY_SEC_MATERIAL])
    #     else:
    #         pass
    #     print(f"\n select_section done \n")
    #
    #     return self.section_size
    #     print(self.selectedsize)

    # Simulation starts here
    # def design_classification(self):
    #     """ Classify the sections based on Table 2 of IS 800:2007 """
    #     self.input_section_list = []
    #     self.input_section_classification = {}
    #
    #     print(f"self.sec_list {self.sec_list}")
    #
    #     for section in self.sec_list:
    #         trial_section = section.strip("'")
    #         # print(f"trial_section  {trial_section}")

    # def initial_member_capacity(self,design_dictionary,previous_size = None):
    #
    #     "selection of member based on the yield capacity"
    #     min_yield = 0
    #
    #     if self.count == 0:
    #         self.max_section(self,design_dictionary,self.sizelist)
    #         [self.force1, self.len1, self.slen1, self.gyr1]= self.max_force_length(self,  self.max_area)
    #         [self.force2, self.len2, self.slen2, self.gyr2] = self.max_force_length(self,  self.max_gyr)
    #     else:
    #         pass
    #
    #     self.count = self.count + 1
    #     "Loop checking each member from sizelist based on yield capacity"
    #     if (previous_size) == None:
    #         pass
    #     else:
    #         if previous_size in self.sizelist:
    #             self.sizelist.remove(previous_size)
    #         else:
    #             pass
    #     for selectedsize in self.sizelist:
    #         # print('selectedsize',self.sizelist)
    #         self.section_size = self.select_section(self,design_dictionary,selectedsize)
    #         # self.bolt_diameter_min= min(self.bolt.bolt_diameter)
    #
    #         # self.edge_dist_min = IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt_diameter_min,self.bolt.bolt_hole_type,
    #         #                                                               'machine_flame_cut')
    #         # self.d_0_min = IS800_2007.cl_10_2_1_bolt_hole_size(self.bolt_diameter_min,
    #         #                                                               design_dictionary[KEY_DP_BOLT_HOLE_TYPE])
    #
    #         # self.edge_dist_min_round = round_up(self.edge_dist_min, 5)
    #         # self.pitch_round = round_up((2.5*self.bolt_diameter_min), 5)
    #         # if design_dictionary[KEY_SEC_PROFILE] in ['Channels', 'Back to Back Channels']:
    #         #      self.max_depth = self.section_size_max.max_plate_height()
    #         # else:
    #         #     if self.loc == "Long Leg":
    #         #         self.max_depth =self.section_size_max.max_leg - self.section_size_max.thickness - self.section_size_max.root_radius
    #         #     else:
    #         #         self.max_depth =self.section_size_max.min_leg - self.section_size_max.thickness - self.section_size_max.root_radius
    #
    #
    #         "selection of minimum member size required based on the miniumum size of bolt  in bolt diameter list "
    #
    #         if design_dictionary[KEY_LOCATION] == "Long Leg":
    #             if self.section_size.max_leg < self.section_size.root_radius + self.section_size.thickness + (2 *self.edge_dist_min_round):
    #                 continue
    #         elif design_dictionary[KEY_LOCATION] == 'Short Leg':
    #             if self.section_size.min_leg < self.section_size.root_radius + self.section_size.thickness + (2 * self.edge_dist_min_round ):
    #                 continue
    #         if design_dictionary[KEY_SEC_PROFILE] =='Channels':
    #             self.max_plate_height = self.section_size.max_plate_height()
    #             if self.max_plate_height < (self.pitch_round) + (2 * self.edge_dist_min_round):
    #                 continue
    #             else:
    #                 self.cross_area = self.section_size.area
    #
    #         elif design_dictionary[KEY_SEC_PROFILE] == 'Back to Back Channels':
    #             self.max_plate_height = self.section_size.max_plate_height()
    #             if self.max_plate_height < (self.pitch_round) + (2 * self.edge_dist_min_round):
    #                 continue
    #             else:
    #                 self.cross_area = self.section_size.area * 2
    #
    #         elif design_dictionary[KEY_SEC_PROFILE] =='Angles':
    #             self.cross_area = self.section_size.area
    #
    #         else:
    #             self.cross_area = self.section_size.area * 2
    #
    #         "excluding previous section size which failed in rupture and selecting higher section based on the cross section area "
    #
    #         self.section_size.tension_member_yielding(A_g = self.cross_area , F_y =self.section_size.fy)
    #         self.K = 1.0
    #         # print(self.section_size.rad_of_gy_z)
    #         if design_dictionary[KEY_SEC_PROFILE] in ['Angles','Star Angles','Back to Back Angles']:
    #             # print(selectedsize)
    #             self.min_rad_gyration_calc(self,designation=self.section_size.designation, material_grade=self.material,
    #                                        key=self.sec_profile, subkey=self.loc, D_a=self.section_size.a,
    #                                        B_b=self.section_size.b, T_t=self.section_size.thickness)
    #         else:
    #             self.min_rad_gyration_calc(self,designation=self.section_size.designation, material_grade=self.material,
    #                                        key=self.sec_profile, subkey=self.loc, D_a=self.section_size.depth,
    #                                        B_b=self.section_size.flange_width, T_t=self.section_size.flange_thickness,
    #                                        t=self.section_size.web_thickness)
    #         # print(design_dictionary[KEY_SEC_PROFILE], design_dictionary[KEY_LOCATION], self.section_size.min_radius_gyration)
    #         self.section_size.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],r=self.min_radius_gyration)
    #         # print(self.section_size.tension_yielding_capacity)
    #
    #         "condition for yield and slenderness check "
    #
    #         if (self.section_size.tension_yielding_capacity >= self.load.axial_force*1000) and self.section_size.slenderness < 400:
    #             min_yield_current = self.section_size.tension_yielding_capacity
    #             self.member_design_status = True
    #             if min_yield == 0:
    #                 min_yield = min_yield_current
    #                 self.section_size_1 = self.select_section(self, design_dictionary, selectedsize)
    #                 self.section_size_1.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
    #                 if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
    #                     self.min_rad_gyration_calc(self,designation=self.section_size_1.designation,
    #                                                material_grade=self.material,
    #                                                key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.a,
    #                                                B_b=self.section_size_1.b, T_t=self.section_size_1.thickness)
    #
    #                 else:
    #                     self.min_rad_gyration_calc(self,designation=self.section_size_1.designation,
    #                                                material_grade=self.material,
    #                                                key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.depth,
    #                                                B_b=self.section_size_1.flange_width,
    #                                                T_t=self.section_size_1.flange_thickness,
    #                                                t=self.section_size_1.web_thickness)
    #
    #                 self.section_size_1.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],
    #                                                                  r=self.min_radius_gyration)
    #
    #             elif min_yield_current < min_yield:
    #                 min_yield = min_yield_current
    #                 self.section_size_1 = self.select_section(self, design_dictionary, selectedsize)
    #                 self.section_size_1.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
    #                 if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
    #                     self.min_rad_gyration_calc(self,designation=self.section_size_1.designation,
    #                                                material_grade=self.material,
    #                                                key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.a,
    #                                                B_b=self.section_size_1.b, T_t=self.section_size_1.thickness)
    #                 else:
    #                     self.min_rad_gyration_calc(self,designation=self.section_size_1.designation,
    #                                                material_grade=self.material,
    #                                                key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.depth,
    #                                                B_b=self.section_size_1.flange_width,
    #                                                T_t=self.section_size_1.flange_thickness,
    #                                                t=self.section_size_1.web_thickness)
    #             self.section_size_1.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],
    #                                                              r=self.min_radius_gyration)
    #
    #             # print(self.section_size_1.slenderness)
    #
    #             "condition to limit loop based on max force derived from max available size."
    #
    #         elif (self.load.axial_force*1000 > self.force1) :
    #             self.max_limit_status_1 = True
    #             # self.design_status = False
    #             logger.warning(" : The factored tension force ({} kN) exceeds the tension capacity ({} kN) with respect to the maximum available "
    #                            "member size {}.".format(round(self.load.axial_force,2),round(self.force1/1000,2),self.max_area))
    #             logger.info(" : Define member(s) with a higher cross sectional area.")
    #             # logge r.error(": Design is not safe. \n ")
    #             # logger.info(" :=========End Of design===========")
    #             break
    #
    #             "condition to limit loop based on max length derived from max available size"
    #
    #         elif self.length > self.len2:
    #             self.max_limit_status_2 = True
    #             # self.design_status = False
    #             logger.warning(" : The member length ({} mm) exceeds the maximum allowable length ({} mm) with respect to the maximum available "
    #                            "member size {}.".format(self.length,round(self.len2,2),self.max_gyr))
    #             logger.info(" : Select member(s) with a higher radius of gyration value.")
    #             # logger.error(": Design is not safe. \n ")
    #             # logger.info(" :=========End Of design===========")
    #             break
    #
    #         else:
    #             pass
    #
    #     if self.member_design_status == False and self.max_limit_status_1!=True and self.max_limit_status_2!=True:
    #         logger.warning(" : The available depth of the member cannot accommodate the minimum available bolt diameter of {} mm considering the "
    #                        "minimum spacing limit [Ref. Cl. 10.2, IS 800:2007].".format(self.bolt_diameter_min))
    #         logger.info(" : Reduce the bolt diameter or increase the member depth and re-design.")
    #         # logger.error(": Design is not safe. \n ")
    #         # logger.info(" :=========End Of design===========")
    #
    #     if self.member_design_status == True:
    #         print("pass")
    #         self.design_status = True
    #         self.select_bolt_dia(self, design_dictionary)
    #     else:
    #         self.design_status = False
    #         logger.error(": Design is unsafe. \n ")
    #         logger.info(" :=========End Of design===========")


    def section_classification(self):
        """Classify the sections based on Table 2 of IS 800:2007"""
        print(f"Inside section_classification")
        local_flag = True
        self.input_modified = []
        self.input_section_list = []
        self.input_section_classification = {}
        lambda_check = False

        for section in self.sec_list:
            trial_section = section.strip("'")
            # print(f"trial_section {trial_section}")

            # section_classification_subchecks(trial_section, self.material)

            # fetching the section properties
            self.section_property = self.section_classification_subchecks(self,trial_section)
            print(f"Type of section{type(section)}")

            # section classification
            if (self.sec_profile in VALUES_SEC_PROFILE_Compression_Strut[:3]):  # Angles or Back to Back or 'Star Angle'

                # updating the material property based on thickness of the thickest element
                self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.thickness)
                if self.section_property.type == 'Rolled':
                    if self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[0] or self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[2]:
                        list_Table2_vi= IS800_2007.Table2_vi(self.section_property.min_leg, self.section_property.max_leg, self.section_property.thickness,
                                                            self.material_property.fy, "Axial Compression")
                    elif self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[1]:
                        list_Table2_vi = IS800_2007.Table2_vii(self.section_property.min_leg,
                                                              self.section_property.max_leg,
                                                              self.section_property.thickness,
                                                              self.material_property.fy, "Axial Compression")
                    # print(f"\n \n \n self.material_property.fy {self.material_property.fy} \n \n \n")
                    self.section_property.section_class = list_Table2_vi[0]
                    self.width_thickness_ratio  = list_Table2_vi[1]
                    self.depth_thickness_ratio = list_Table2_vi[2]
                    self.width_depth_thickness_ratio = list_Table2_vi[3]
                    #print(f"DONE {self.section_property.section_class} {self.width_thickness_ratio} {self.depth_thickness_ratio} {self.width_depth_thickness_ratio}")
                    #if self.section_property.section_class == 'Slender':
                    #    logger.info(
                    #        "The section is {}. The b/t of the trial section ({}) is {} and d/t is {} and (b+d)/t is {}.  [Reference: Cl 3.7, IS 800:2007].".format(
                    #            self.section_property.section_class, trial_section,
                    #            round(self.width_thickness_ratio, 2), round_up(self.depth_thickness_ratio),
                    #            round(self.width_depth_thickness_ratio, 2)))
                    #else:
                    #    logger.warning(
                    #        "The section is {}. The b/t of the trial section ({}) is {} and d/t is {} and (b+d)/t is {}.  [Reference: Cl 3.7, IS 800:2007].".format(
                    #            self.section_property.section_class, trial_section,
                    #            round(self.width_thickness_ratio, 2), round_up(self.depth_thickness_ratio),
                    #            round(self.width_depth_thickness_ratio, 2)))
                    #    logger.warning("Ignoring section")


                else:
                    print(f"section_classification _ not done")
                    local_flag = False
            elif (self.sec_profile in ['Channels', 'Back to Back Channels']):

                # updating the material property based on thickness of the thickest element
                self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.web_thickness)

                list_Table2_iv = IS800_2007.Table2_iv(depth=self.section_property.depth, f_y=self.material_property.fy, thickness_web= self.section_property.web_thickness)
                print(f"Checking Channel Properties")
                self.section_property.section_class = list_Table2_iv[0]
                self.depth_thickness_ratio = list_Table2_iv[1]
                #logger.info("The section is {}. The d/t_web of the trial section ({}) is {}.  [Reference: Cl 3.7, IS 800:2007].".format(self.section_property.section_class, trial_section, round(self.depth_thickness_ratio,2) ))
            else:
                print(f"section_classification _ cannot do")
                local_flag = False


            # 2.3 - slenderness ratio
            # self.section_property.min_rad_gyration_calc(self, self.sec_profile)
            if self.sec_profile == Profile_name_1 or self.sec_profile == Profile_name_2 or self.sec_profile == Profile_name_3:
                min_radius_gyration, effective_area = self.min_rad_gyration_calc_strut(self,designation= self.section_property.designation, material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, D_a=self.section_property.a,
                                           B_b=self.section_property.b, T_t=self.section_property.thickness, t = self.plate_thickness)
            #     self.min_radius_gyration = min(self.section_property.rad_of_gy_u, self.section_property.rad_of_gy_v)
            # 
            # elif self.sec_profile == Profile_name_2 :
            #     BBAngle_attributes = BBAngle_Properties()
            #     BBAngle_attributes.data(trial_section, self.material)
            #     self.effective_area = BBAngle_attributes.calc_Area() * 100  # mm2
            #     if self.loc == "Long Leg":
            #         cg1 = self.section_property.Cy  # mm
            #         cg2 = self.section_property.Cz  # mm
            #     else:
            #         cg1 = self.section_property.Cz  # mm
            #         cg2 = self.section_property.Cy  # mm
            #     # mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(l=self.loc,
            #     #                                                       thickness=0) * 10 ** 4  # mm**4
            #     # mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(l=self.loc,
            #     #                                                       thickness=0) * 10 ** 4  # mm**4
            #     r_zz = BBAngle_attributes.calc_RogZ(l=self.loc, thickness=0) * 10  # mm
            #     r_yy = BBAngle_attributes.calc_RogY(l=self.loc, thickness=0) * 10  # mm
            #     self.min_radius_gyration = min(r_yy, r_zz)
            #     print(
            #         " effective_area {}\n loc {}\n cgyy {}\n cgzz {}\n mom_inertia_y {}\n mom_inertia_z {}\n r_zz{}\n r_yy{}\n min_radius_gyration{} ".format(
            #             self.effective_area, self.loc, cg1, cg2, mom_inertia_y, mom_inertia_z, r_zz, r_yy,
            #             self.min_radius_gyration))
            # 
            # elif self.sec_profile == Profile_name_3 :
            #     BBAngle_attributes = BBAngle_Properties()
            #     BBAngle_attributes.data(trial_section, self.material)
            #     self.effective_area = BBAngle_attributes.calc_Area() * 100 #mm2
            #     if self.loc == "Long Leg":
            #         cg1 = self.section_property.Cy#mm
            #         cg2 = self.section_property.Cz#mm
            #     else:
            #         cg1 = self.section_property.Cz#mm
            #         cg2 = self.section_property.Cy#mm
            #     mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(l = self.loc, thickness= self.plate_thickness) * 10**4#mm**4
            #     mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(l=self.loc, thickness= self.plate_thickness) * 10**4#mm**4
            #     r_zz = BBAngle_attributes.calc_RogZ(l=self.loc, thickness=self.plate_thickness) * 10 #mm
            #     r_yy = BBAngle_attributes.calc_RogY(l=self.loc, thickness=self.plate_thickness) * 10 #mm
            #     self.min_radius_gyration = min(r_yy, r_zz)
            #     print(" effective_area {}\n loc {}\n cgyy {}\n cgzz {}\n mom_inertia_y {}\n mom_inertia_z {}\n r_zz{}\n r_yy{}\n min_radius_gyration{} ".format(self.effective_area, self.loc, cg1 ,cg2,mom_inertia_y,mom_inertia_z , r_zz, r_yy,  self.min_radius_gyration) )
            #     # if self.loc == loc_type1 :
            #     #     if self.section_property.Cz > self.section_property.Cy :
            #     #         r_z = self.section_property.rad_of_gy_z
            #     #         I_yy = 2*(self.section_property.mom_inertia_y + Area(self.section_property.Cy + self.plate_thickness/2)**2)
            #     #         # r_y =
            #     # elif self.loc == loc_type2 :
            #     #     pass
            #     # else:
            #     #     print(f" Connection Location not defined")
            #     #     local_flag = False
            #     #     break

            slenderness = self.section_property.design_check_for_slenderness(K= self.K, L = self.length, r = min_radius_gyration)#(self.effective_length / self.min_radius_gyration)
            print(f"min_radius_gyration {min_radius_gyration}"
                  f"slenderness {slenderness}")
            limit = IS800_2007.cl_3_8_max_slenderness_ratio(1)
            if slenderness > limit:
                #logger.warning("Length provided is beyond the limit allowed. [Reference: Cl 3.8, IS 800:2007]")
                #logger.error("Cannot compute. Given Length does not pass for this section.")
                local_flag = False
                # self.sec_list.remove(self.section_property.designation )
            else:
                #logger.info("Length provided is within the limit allowed. [Reference: Cl 3.8, IS 800:2007]" )
                local_flag = True


            if len(self.allowed_sections) == 0 or len(self.sec_list) == 0:
                logger.warning("Select at-least one type of section in the design preferences tab.")
                logger.error("Cannot compute. Selected section classification type is Null.")
                self.design_status = False
                self.design_status_list.append(self.design_status)
                local_flag = False

            if self.section_property.section_class in self.allowed_sections and local_flag == True:
                self.input_section_list.append(trial_section)
                self.input_section_classification.update({trial_section: self.section_property.section_class})
                # if self.sec_profile != Profile_name_1:
                self.sec_prop_initial_dict.update({trial_section : (self.section_property.section_class, min_radius_gyration, slenderness, effective_area)}) #, self.width_thickness_ratio,self.depth_thickness_ratio,self.width_depth_thickness_ratio
        # print(f" sectopn class done {self.sec_list}")
        return local_flag
            # print(f"self.section_property.section_class{self.section_property.section_class}")
    

    #  ======Calculations start here====== #
    def optimization_tab_check(self):
        if (self.allowable_utilization_ratio <= 0.10) or (self.allowable_utilization_ratio > 1.0):
            logger.warning(
                "The defined value of Utilization Ratio in the design preferences tab is out of the suggested range.")
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default value of 1.0.")
            self.allowable_utilization_ratio = 1.0
            self.design_status = False
            self.design_status_list.append(self.design_status)

        elif (self.effective_area_factor <= 0.10) or (self.effective_area_factor > 1.0):
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
            logger.info("Provided appropriate design preference, now checking input.")

    def section_classification_subchecks(self, section):
        if self.sec_profile == Profile_name_1 or self.sec_profile == Profile_name_2 or self.sec_profile == Profile_name_3:  # Angles
            self.section_property = Angle(designation = section, material_grade = self.material)
        # elif self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[1]:  # Back to Back Angles
        #     self.section_property = Angle(designation=section, material_grade=self.material)
        elif self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[3] or self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[3]:  # Channels
            print(f"section_classification_subchecks error ")
            # self.section_property = Channel(designation=section, material_grade=self.material)
        # # elif self.sec_profile == VALUES_SEC_PROFILE[3]:  # Columns
        # #     self.section_property = SHS(designation=section, material_grade=self.material)
        # # elif self.sec_profile == VALUES_SEC_PROFILE[4]:  # CHS
        # #     self.section_property = CHS(designation=section, material_grade=self.material)
        # else:  # Why?
        #     self.section_property = Column(designation=section, material_grade=self.material)
        else:
            logger.warning(
                "The section should be either Angle or Back to Back Angle. ")
        return self.section_property

    def common_checks_1(self, section, step = 1, list_result = [], list_1 = []):
        if step == 1:
            # print(f"Working correct here{section}")
            print(section)
            print(self.sec_profile)

            # fetching the section properties of the selected section
            self.section_classification_subchecks(self, section)
            if self.sec_profile == Profile_name_1 or self.sec_profile == Profile_name_2 or self.sec_profile == Profile_name_3:
                # self.material_property(self.material, self.section_property.thickness)
                self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.thickness)
            elif self.sec_profile in ['Channels', 'Back to Back Channels']:
                self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.web_thickness)
            self.epsilon = math.sqrt(250 / self.material_property.fy)

            # print(f"Working correct here")
        elif step == 2:
            if self.section_property.section_class == 'Slender':
                logger.warning("The trial section ({}) is Slender. Ignoring section.".format(section))
                # pass
                # if (self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[0]) or (self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[1]):  # Angles or Back to Back Angle
                #     self.effective_area = (2 * ((31.4 * self.epsilon * self.section_property.flange_thickness) *
                #                                 self.section_property.flange_thickness)) + \
                #                           (2 * ((21 * self.epsilon * self.section_property.web_thickness) * self.section_property.web_thickness))
                # elif (self.sec_profile == VALUES_SEC_PROFILE[2]) or (self.sec_profile == VALUES_SEC_PROFILE[3]):
                #     self.effective_area = (2 * 21 * self.epsilon * self.section_property.flange_thickness) * 2
            elif self.section_property.section_class == 'Semi-Compact':
                if self.sec_profile == Profile_name_2 or self.sec_profile == Profile_name_3 :
                    pass#self.effective_area = 2 * self.section_property.area  # mm2
                else:
                    self.effective_area = self.section_property.area
                print(f"effective_area{self.effective_area}")
                # print(f"self.effective_area{self.effective_area}")

            # reduction of the area based on the connection requirements (input from design preferences)
            if self.effective_area_factor < 1.0:
                self.effective_area = round(self.effective_area * self.effective_area_factor, 2)

                logger.warning(
                    "Reducing the effective sectional area as per the definition in the Design Preferences tab.")
                logger.info(
                    "The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".
                    format(round((self.effective_area / self.effective_area_factor), 2), self.effective_area))
            # else:
            #     if self.section_property.section_class != 'Slender':

        elif step == 3:
            # 2.1 - Buckling curve classification and Imperfection factor
            if (self.sec_profile in VALUES_SEC_PROFILE_Compression_Strut[:3]):
                self.buckling_class = 'c'
            else:
                print("section not valid")

            self.imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class=self.buckling_class)


        elif step == 4:
            # print(f"\n data sent "
            #       f" self.material_property.fy {self.material_property.fy}"
            #       f"self.gamma_m0 {self.gamma_m0}"
            #       f"self.slenderness {self.slenderness}"
            #       f" self.imperfection_factor {self.imperfection_factor}"
            #       f"self.section_property.modulus_of_elasticity {self.section_property.modulus_of_elasticity}")

            list_cl_7_1_2_1_design_compressisive_stress = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.material_property.fy, self.gamma_m0, self.slenderness, self.imperfection_factor,
                self.section_property.modulus_of_elasticity, check_type= list_result)
            # for x in list_cl_7_1_2_1_design_compressisive_stress:
            #     print(f"x {x} ")
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

            list_2 = list_result.copy()
            for j in list_1:
                for k in list_2:
                    self.optimum_section_cost_results[self.cost][j] = k
                    list_2.pop(0)
                    break
            # print(f"\n self.optimum_section_cost_results {self.optimum_section_cost_results}"
            #       f"\n self.optimum_section_ur_results {self.optimum_section_ur_results}")
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


    def common_result(self, list_result,result_type):

            self.result_designation = list_result[result_type]["Designation"] # TODO debug
            limit = IS800_2007.cl_3_8_max_slenderness_ratio(1)
            if self.sec_prop_initial_dict[self.result_designation][2] > limit:
                logger.warning("Length provided is beyond the limit allowed. [Reference: Cl 3.8, IS 800:2007]")
                logger.error("Cannot compute. Given Length does not pass for this section.")
                # self.sec_list.remove(self.section_property.designation )
            else:
                logger.info("Length provided is within the limit allowed. [Reference: Cl 3.8, IS 800:2007]" )
            logger.info(
                            "The section is {}. The b/t of the section ({}) is {} and d/t is {} and (b+d)/t is {}.  [Reference: Cl 3.7, IS 800:2007].".format(
                               self.input_section_classification[self.result_designation], self.result_designation,
                                round(self.width_thickness_ratio, 2), round_up(self.depth_thickness_ratio),
                                round(self.width_depth_thickness_ratio, 2)))


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

            self.result_fcd = list_result[result_type]['FCD'] * 1000
            self.result_capacity = list_result[result_type]['Capacity']
            self.result_cost = list_result[result_type]['Cost']
    # def max_force_length(self,section):
    #
    #     "calculated max force and length based on the maximum section size avaialble for diff section type"
    #
    #     if self.sec_profile == 'Angles':
    #         # print (Angle)
    #
    #         self.section_size_max = Angle(designation=section, material_grade=self.material)
    #         self.section_size_max.tension_member_yielding(A_g=(self.section_size_max.area),
    #                                                       F_y=self.section_size_max.fy)
    #         self.max_member_force = self.section_size_max.tension_yielding_capacity
    #         self.min_rad_gyration_calc(self,designation=section, material_grade=self.material,
    #                                    key=self.sec_profile,subkey=self.loc, D_a=self.section_size_max.a,
    #                                    B_b=self.section_size_max.b, T_t=self.section_size_max.thickness)
    #         self.max_length = 400 * self.min_radius_gyration
    #
    #
    #     elif self.sec_profile in ['Back to Back Angles', 'Star Angles']:
    #         self.section_size_max = Angle(designation=section, material_grade=self.material)
    #         self.section_size_max.tension_member_yielding(A_g=(2*self.section_size_max.area),
    #                                                       F_y=self.section_size_max.fy)
    #         # self.max_member_force = self.section_size_max.tension_yielding_capacity * 2
    #         self.min_rad_gyration_calc(self,designation=section, material_grade=self.material,
    #                                    key=self.sec_profile, subkey=self.loc, D_a=self.section_size_max.a,
    #                                    B_b=self.section_size_max.b, T_t=self.section_size_max.thickness)
    #         self.max_length = 400 * self.min_radius_gyration
    #
    #
    #
    #
    #     elif self.sec_profile == 'Channels':
    #         self.section_size_max = Channel(designation=section, material_grade=self.material)
    #         self.section_size_max.tension_member_yielding(A_g=(self.section_size_max.area),
    #                                                       F_y=self.section_size_max.fy)
    #
    #         self.max_member_force = self.section_size_max.tension_yielding_capacity
    #         self.min_rad_gyration_calc(self,designation=section, material_grade=self.material,
    #                                    key=self.sec_profile,subkey=self.loc, D_a=self.section_size_max.depth,
    #                                    B_b=self.section_size_max.flange_width, T_t=self.section_size_max.flange_thickness,
    #                                    t=self.section_size_max.web_thickness)
    #         self.max_length = 400 * self.min_radius_gyration
    #
    #
    #     elif self.sec_profile == 'Back to Back Channels':
    #         self.section_size_max = Channel(designation=section, material_grade=self.material)
    #         self.section_size_max.tension_member_yielding(A_g=(2*self.section_size_max.area),
    #                                                       F_y=self.section_size_max.fy)
    #         # self.max_member_force = 2 * self.section_size_max.tension_yielding_capacity
    #         self.min_rad_gyration_calc(self,designation=section, material_grade=self.material,
    #                                    key=self.sec_profile, subkey=self.loc, D_a=self.section_size_max.depth,
    #                                    B_b=self.section_size_max.flange_width, T_t=self.section_size_max.flange_thickness,
    #                                    t=self.section_size_max.web_thickness)
    #         self.max_length = 400 * self.min_radius_gyration
    #     self.section_size_max.design_check_for_slenderness(K=self.K, L=self.length,
    #                                                    r=self.min_radius_gyration)
    #
    #     return self.section_size_max.tension_yielding_capacity, self.max_length, self.section_size_max.slenderness,self.min_radius_gyration

    def design(self):
        # flag = self.section_classification(self)
        # print(flag)
        """ Perform design of struct """
        # checking DP inputs
        self.optimization_tab_check(self)
        # optimization_tab_check()
        #
        # print(f"\n self.input_section_list {self.input_section_list}")
        # print(f"\n self.input_section_classification {self.input_section_classification}")
        # print(f"\n self.loc {self.loc}")

        print(f"\nSections passing initial checks {self.input_section_list}\n")
        #if design_dictionary[KEY_AXIAL] == '' and len(self.input_section_list) == 1 :
        #    self.single_result = {}
        #    logger.info("Provided appropriate input and starting design.")
        #
        #    self.strength_of_strut(self)
        #if design_dictionary[KEY_AXIAL] != '' : #TODO: Parth to confirm if this code is needed
        if len(self.input_section_list) >= 1 :
            logger.info("Provided appropriate input and starting design.")

            self.design_strut(self)
        #elif len(self.input_section_list) == 1 :
            #logger.warning(
            #    "No need for load input.")
            # logger.error("Cannot compute!")
            #logger.info(" Ignoring load and starting design.")
            #design_dictionary[KEY_AXIAL] = ''
        #    self.single_result = {}
        #    logger.info("Provided appropriate input and starting design.")
    
        #    self.strength_of_strut(self)
        else:
            # logger.warning(
            #     "More than 1 section given as input without giving Load")
            logger.warning("Cannot compute!")
            logger.info("Give 1 valid section as Inputs and/or "
                        "Change load or Length and re-design.")
            self.design_status = False
            # self.design_strut(self)
            self.design_status_list.append(self.design_status)

        #else:          #TODO: Parth to confirm if this code is needed
            # logger.warning(
            #     "More than 1 section given as input without giving Load")
        #    logger.warning("Cannot compute!")
        #    design_dictionary[KEY_AXIAL] == 1
        #    logger.info(" Taking load of 1 kN.")
            # logger.info("Give 1 section as Inputs and/or "
            #             "Give load and re-design.")
            # self.design_status = False
        #    self.design_strut(self)
            # self.design_status_list.append(self.design_status)

    def design_strut(self):

        # initializing lists to store the optimum results based on optimum UR and cost
        # 1- Based on optimum UR
        self.optimum_section_ur_results = {}
        self.optimum_section_ur = []

        # 2 - Based on optimum cost
        self.optimum_section_cost_results = {}
        self.optimum_section_cost = []
        self.flag = self.section_classification(self)

        print('self.flag:',self.flag)
        if self.effective_area_factor < 1.0:
            logger.warning(
                "Reducing the effective sectional area as per the definition in the Design Preferences tab."
            )
        else:
            logger.info(
                "The effective sectional area is taken as 100% of the cross-sectional area [Reference: Cl. 7.3.2, IS 800:2007]."
            )
        

        print('self.input_section_list:',self.input_section_list)
        if self.flag:
            for section in self.input_section_list:  # iterating the design over each section to find the most optimum section

                # Yield strength of steel
                # self.common_checks_1(self,section, step=7)

                # Common checks
                self.common_checks_1(self, section, step=1)
                # initialize lists for updating the results dictionary
                list_result = []
                list_1 = []
                list_result.append(section)
                print(f"Common checks "
                    f"list_result {list_result}")

                self.section_property.section_class = self.input_section_classification[section]

                # MIN RADIUS OF GYRATION
                self.min_radius_gyration = self.sec_prop_initial_dict[section][1]
                self.slenderness = self.sec_prop_initial_dict[section][2]
                # Step 1 - computing the effective sectional area
                self.effective_area = self.sec_prop_initial_dict[section][3]

                self.common_checks_1(self, section, step=2)

                # if self.loc == "Long Leg":
                #     self.max_depth =self.section_size_max.max_leg - self.section_size_max.thickness - self.section_size_max.root_radius
                # else:
                #     self.max_depth =self.section_size_max.min_leg - self.section_size_max.thickness - self.section_size_max.root_radius

                list_result.extend([self.section_property.section_class, self.effective_area])

                # Step 2 - computing the design compressive stress
                self.common_checks_1(self, section, step=3)
                list_result.extend([self.buckling_class, self.imperfection_factor, self.effective_length])

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
                        self.section_property.leg_b_length, self.section_property.thickness, self.material_property.fy,
                        bolt_no=self.bolts, fixity=self.fixity)

                    self.equivalent_slenderness = returned_list[0]
                    self.lambda_vv = round(returned_list[1], 2)
                    self.lambda_psi = round(returned_list[2], 2)
                    self.k1 = returned_list[3]
                    self.k2 = returned_list[4]
                    self.k3 = returned_list[5]

                    self.common_checks_1(self, section, step=4, list_result=['Leg', self.equivalent_slenderness])


                # 2.7 - Capacity of the section
                self.section_capacity = self.design_compressive_stress * self.effective_area  # N

                print("\n data sent ", self.length, self.min_radius_gyration, self.section_property.leg_a_length,
                    f" \n self.section_property.leg_b_length {self.section_property.leg_b_length}, ",
                    f"\n  self.section_property.thickness {self.section_property.thickness},",
                    f" \n self.material_property.fy {self.material_property.fy}, ",
                    f"\n self.bolts {self.bolts}, ",
                    f" \n self.fixity {self.fixity}, ",
                    f"\n self.slenderness {self.slenderness}",
                    f" \n self.slenderness {self.slenderness}", self.imperfection_factor,
                    self.section_property.modulus_of_elasticity,
                    f" \n self.euler_buckling_stress {self.euler_buckling_stress}",
                    f" \n self.nondimensional_effective_slenderness_ratio {self.nondimensional_effective_slenderness_ratio}",
                    f" \n self.phi {self.phi}",
                    f" \n self.stress_reduction_factor {self.stress_reduction_factor}",
                    f" \n self.design_compressive_stress_fr {self.design_compressive_stress_fr}",
                    f" \n self.design_compressive_stress {self.design_compressive_stress}",
                    f" \n self.design_compressive_stress_max {self.design_compressive_stress_max}"
                    f" \n self.section_capacity {self.section_capacity}", )
                if self.load_type != 'Concentric Load':
                    print(f" \n self.equivalent_slenderness {self.equivalent_slenderness} "
                        f" \n self.lambda_vv {self.lambda_vv} "
                        f" \n self.lambda_psi {self.lambda_psi} "
                        f" \n self.k1 {self.k1} "
                        f" \n self.k2 {self.k2} "
                        f" \n self.k3 {self.k3} ")
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
                print("Section result: \n",self.sec_profile, list_result)
                # Step 3 - Storing the optimum results to a list in a descending order

                list_1 = ['Designation','Section class', 'Effective area', 'Buckling_class', 'IF',
                        'Effective_length', 'Effective_SR', 'EBS', 'lambda_vv', 'lambda_psi', 'ND_ESR', 'phi', 'SRF',
                        'FCD_formula', 'FCD_max', 'FCD', 'Capacity', 'UR', 'Cost']
                self.common_checks_1(self, section, 5, list_result, list_1)
                print(f"\n self.optimum_section_cost_results {self.optimum_section_cost_results}"
                f"\n self.optimum_section_ur_results {self.optimum_section_ur_results}")

    def min_rad_gyration_calc_strut(self,designation, material_grade,key,subkey, D_a=0.0,B_b=0.0,T_t=0.0,t=0.0):
        if key == Profile_name_1 and (subkey == loc_type1 or subkey == loc_type2):
            Angle_attributes = Angle(designation, material_grade)
            effective_area = Angle_attributes.area
            rad_u = Angle_attributes.rad_of_gy_u
            rad_v = Angle_attributes.rad_of_gy_v
            min_rad = min(rad_u, rad_v)

        elif key == Profile_name_2 and subkey == loc_type1:
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            effective_area = BBAngle_attributes.calc_Area() * 100
            rad_y = BBAngle_attributes.calc_RogY(a=D_a,b=B_b,t=T_t,l=loc_type2, thickness = 0) * 10
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a,b=B_b,t=T_t,l=loc_type2, thickness = 0) * 10
            # mom_inertia_y_1 = mom_inertia_y = self.Angle_attributes.mom_inertia_y
            # mom_inertia_z_1 = mom_inertia_y = self.Angle_attributes.mom_inertia_y
            mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(a=D_a,b=B_b,t=T_t, l=loc_type2, thickness = 0)
            mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(a=D_a,b=B_b,t=T_t, l=loc_type2, thickness = 0)
            print(self.section_property.designation, '\n rad_y =',rad_y, '\n rad_z =', rad_z, '\n mom_inertia_y =',mom_inertia_y,'\n mom_inertia_z', mom_inertia_z)
            min_rad = min(rad_y, rad_z)
        elif key == Profile_name_2 and subkey == loc_type2: #match
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            effective_area = BBAngle_attributes.calc_Area() * 100
            rad_y = BBAngle_attributes.calc_RogY(a=D_a,b=B_b,t=T_t, l=loc_type1, thickness= 0) * 10
            mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(a=D_a,b=B_b,t=T_t, l=loc_type1, thickness= 0)
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a,b=B_b,t=T_t, l=loc_type1, thickness= 0) * 10
            mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(a=D_a,b=B_b,t=T_t, l=loc_type1, thickness= 0)
            print(self.section_property.designation, '\n rad_y =',rad_y, '\n rad_z =', rad_z, '\n mom_inertia_y =',mom_inertia_y,'\n mom_inertia_z', mom_inertia_z)
            min_rad = min(rad_y, rad_z)
        elif key == Profile_name_3 and subkey == loc_type1: #match
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            effective_area = BBAngle_attributes.calc_Area() * 100
            rad_y = BBAngle_attributes.calc_RogY(a=D_a,b=B_b,t=T_t, l=subkey, thickness= t) * 10
            mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(a=D_a,b=B_b,t=0, l=loc_type1, thickness= t)
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a,b=B_b,t=T_t, l=subkey, thickness= t) * 10
            mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(a=D_a,b=B_b,t=0, l=loc_type1, thickness= t)
            print(self.section_property.designation, '\n rad_y =', rad_y, '\n rad_z =', rad_z, '\n mom_inertia_y =',
                  mom_inertia_y, '\n mom_inertia_z', mom_inertia_z)
            min_rad = min(rad_y, rad_z)
        elif key == Profile_name_3 and subkey == loc_type2:
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            effective_area = BBAngle_attributes.calc_Area() * 100
            rad_y = BBAngle_attributes.calc_RogY(a=D_a,b=B_b,t=T_t, l=subkey, thickness= t) * 10
            mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(a=D_a,b=B_b,t=0, l=loc_type1, thickness= t)
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a,b=B_b,t=T_t, l=subkey, thickness= t) * 10
            mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(a=D_a,b=B_b,t=0, l=loc_type1, thickness= t)
            print(self.section_property.designation, '\n rad_y =', rad_y, '\n rad_z =', rad_z, '\n mom_inertia_y =',
                  mom_inertia_y, '\n mom_inertia_z', mom_inertia_z)
            min_rad = min(rad_y, rad_z)
        return min_rad , effective_area
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
        print(f"Common checks "
              f"section for design {list_result}")

        # Step 1 - computing the effective sectional area
        self.section_property.section_class = self.input_section_classification[section]

        # MIN RADIUS OF GYRATION
        self.min_radius_gyration = self.sec_prop_initial_dict[section][1]
        self.slenderness = self.sec_prop_initial_dict[section][2]
        # Step 1 - computing the effective sectional area
        self.effective_area = self.sec_prop_initial_dict[section][3]
        # SAME AS BEFORE

        self.common_checks_1(self, section, step=2)
        # if self.loc == "Long Leg":
        #     self.max_depth =self.section_size_max.max_leg - self.section_size_max.thickness - self.section_size_max.root_radius
        # else:
        #     self.max_depth =self.section_size_max.min_leg - self.section_size_max.thickness - self.section_size_max.root_radius

        list_result.extend([self.section_property.section_class, self.effective_area])

        # Step 2 - computing the design compressive stress
        self.common_checks_1(self, section, step=3)
        list_result.extend([self.buckling_class, self.imperfection_factor, self.effective_length])

        if self.load_type == 'Concentric Load':
            # print(f"step == 4"
            #       f"list_result {list_result}")
            self.lambda_vv = 'NA'
            self.lambda_psi = 'NA'
            # step == 4
            self.common_checks_1(self, section, step=4, list_result=['Concentric'])
        else:
            # self.min_radius_gyration = min(self.section_property.rad_of_gy_y, self.section_property.rad_of_gy_z)
            returned_list = IS800_2007.cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(
                self.length, self.min_radius_gyration, self.section_property.leg_a_length,
                self.section_property.leg_b_length, self.section_property.thickness, self.material_property.fy,
                bolt_no=self.bolts, fixity=self.fixity)

            self.equivalent_slenderness = returned_list[0]
            self.lambda_vv = round(returned_list[1], 2)
            self.lambda_psi = round(returned_list[2], 2)
            self.k1 = returned_list[3]
            self.k2 = returned_list[4]
            self.k3 = returned_list[5]


            self.common_checks_1(self, section, step=4, list_result=['Leg', self.equivalent_slenderness])

        print("\n data sent ", self.length, self.min_radius_gyration, self.section_property.leg_a_length,
              f" \n self.section_property.leg_b_length {self.section_property.leg_b_length}, ",
              f"\n  self.section_property.thickness {self.section_property.thickness},",
              f" \n self.material_property.fy {self.material_property.fy}, ",
               f"\n self.bolts {self.bolts}, ",
              f" \n self.fixity {self.fixity}, ",
               f"\n self.slenderness {self.slenderness}",
              f" \n self.imperfection_factor {self.imperfection_factor}", self.section_property.modulus_of_elasticity,
              f" \n self.euler_buckling_stress {self.euler_buckling_stress}",
              f" \n self.nondimensional_effective_slenderness_ratio {self.nondimensional_effective_slenderness_ratio}",
              f" \n self.phi {self.phi}",
              f" \n self.stress_reduction_factor {self.stress_reduction_factor}",
              f" \n self.design_compressive_stress_fr {self.design_compressive_stress_fr}",
              f" \n self.design_compressive_stress {self.design_compressive_stress}",
              f" \n self.design_compressive_stress_max {self.design_compressive_stress_max}", )
        if self.load_type != 'Concentric Load':
                  print(f" \n self.equivalent_slenderness {self.equivalent_slenderness} "
                  f" \n self.lambda_vv {self.lambda_vv} "
                  f" \n self.lambda_psi {self.lambda_psi} "
                  f" \n self.k1 {self.k1} "
                  f" \n self.k2 {self.k2} "
                  f" \n self.k3 {self.k3} ")
        # 2.7 - Capacity of the section
        self.section_capacity = self.design_compressive_stress * self.effective_area  # N

        #SAME AS BEFORE TILL HERE

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
        # sorting results from the dataset
        #if len(self.input_section_list) > 1 : #TODO: Parth to confirm if this code is needed
            #if design_dictionary[KEY_AXIAL] != '':  #TODO: Parth to confirm if this code is needed
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

        if len(self.optimum_section_ur) == 0:
            self.design_status = False
        
        else:
            if self.optimization_parameter == 'Utilization Ratio':
                print(f" self.optimum_section_ur_results {self.optimum_section_ur_results}")
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
            #else:
            #    logger.warning(
            #        "More than 1 section given as input without giving Load")
            #    logger.error("Cannot compute!")
            #    logger.info("Give 1 section as Inputs and/or "
            #                "Give load and re-design.")
            #    self.design_status = False
            #    self.design_status_list.append(self.design_status)

        if self.design_status:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall Column design is SAFE")
            logger.info(": ========== End Of Design ============")
        else:
            logger.info(": ========== Design Status ============")
            logger.info(": Overall Column design is UNSAFE")
            logger.info(": ========== End Of Design ============")
        #else: #TODO: Parth to confirm if this code is needed
        #
        #    self.single_result = {}
        #
        #    print(f"self.single_result {self.single_result}")
        #    self.common_result(self, list_result=self.single_result,result_type= self.sec_profile, flag= 1)
        #    self.design_status = True
        #    self.result_UR = self.single_result[self.sec_profile]['UR']
        #    if self.design_status:
        #        logger.info(": ========== Capacity Status ============")
        #        logger.info(": Section satisfies input")
        #        logger.info(": Section strength found")
        #        logger.info(": ========== End Of Status ============")
        #    else:
        #        logger.info(": ========== Capacity Status ============")
        #        logger.info(": Section does not satisfies input")
        #        logger.info(": Section strength NOT found")
        #        logger.info(": ========== End Of Status ============")
        # end of the design simulation
        # overall design status




    ### start writing save_design from here!
    def save_design(self, popup_summary):

        """if self.connectivity == 'Hollow/Tubular Column Base':
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
            section_type = 'I Section' """
        
        if self.section_property.max_leg == self.section_property.min_leg:
            if self.sec_profile == "Back to Back Angles":
                if self.loc == "Long Leg":
                    image = "bblequaldp"
                else:
                    image = "bbsequaldp"
            elif self.sec_profile == "Star Angles":
                if self.loc == "Long Leg":
                    image = "salequaldp"
                else:
                    image = "sasequaldp"
            else:
                image = "equaldp"

        else:
            if self.sec_profile == "Back to Back Angles":
                if self.loc == "Long Leg":
                    image = "bblunequaldp"
                else:
                    image = "bbsunequaldp"
            elif self.sec_profile == "Star Angles":
                if self.loc == "Long Leg":
                    image = "salunequaldp"
                else:
                    image = "sasunequaldp"
            else:
                image = "unequaldp"
        
        if (self.design_status and self.failed_design_dict is None) or (not self.design_status and len(self.failed_design_dict)>0):
            if self.sec_profile == "Angles" or self.sec_profile == VALUES_SEC_PROFILE_2[0]:
                self.report_column = {KEY_DISP_SEC_PROFILE: image,
                                        KEY_DISP_SECSIZE: (self.section_property.designation, self.sec_profile),
                                        KEY_DISP_MATERIAL: self.section_property.material,
        #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                        KEY_REPORT_MASS: self.section_property.mass,
                                        KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                        KEY_REPORT_MAX_LEG_SIZE: round(self.section_property.max_leg,2),
                                        KEY_REPORT_MIN_LEG_SIZE: round(self.section_property.min_leg,2),
                                        KEY_REPORT_ANGLE_THK: round(self.section_property.thickness,2),
                                        KEY_REPORT_R1: self.section_property.root_radius,
                                        KEY_REPORT_R2: self.section_property.toe_radius,
                                        KEY_REPORT_CY: round(self.section_property.Cy,2),
                                        KEY_REPORT_CZ: round(self.section_property.Cz,2),
                                        KEY_REPORT_IZ: round(self.section_property.mom_inertia_z * 1e-4, 2),
                                        KEY_REPORT_IY: round(self.section_property.mom_inertia_y * 1e-4, 2),
                                        KEY_REPORT_RZ: round(self.section_property.rad_of_gy_z * 1e-1, 2),
                                        KEY_REPORT_RY: round(self.section_property.rad_of_gy_y * 1e-1, 2),
                                        KEY_REPORT_ZEZ: round(self.section_property.elast_sec_mod_z * 1e-3, 2),
                                        KEY_REPORT_ZEY: round(self.section_property.elast_sec_mod_y * 1e-3, 2),
                                        KEY_REPORT_ZPZ: round(self.section_property.plast_sec_mod_z * 1e-3, 2),
                                        KEY_REPORT_ZPY: round(self.section_property.plast_sec_mod_y * 1e-3, 2)}
            else:
                #Update for section profiles Back to Back Angles (Same side gusset), and (Opposite side gusset) by making suitable elif condition.
                self.report_column = {KEY_DISP_COLSEC_REPORT: self.section_property.designation,
                                        KEY_DISP_MATERIAL: self.section_property.material,
                                        #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                        KEY_REPORT_MASS: self.section_property.mass,
                                        KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                        
                }


            self.report_input = \
                {#KEY_MAIN_MODULE: self.mainmodule,
                    KEY_MODULE: self.module, #"Axial load on column "
                    KEY_DISP_AXIAL: self.load.axial_force/1000,
                    KEY_DISP_LENGTH: self.length,
                    KEY_DISP_SEC_PROFILE: self.sec_profile,
                    KEY_DISP_END1: self.end_1,
                    KEY_DISP_END2: self.end_2,
                    KEY_DISP_SECSIZE: self.result_section_class,
                    "Strut Section - Mechanical Properties": "TITLE",
                    KEY_DISP_ULTIMATE_STRENGTH_REPORT: round(self.section_property.fu, 2),
                    KEY_DISP_YIELD_STRENGTH_REPORT: round(self.section_property.fy, 2),
                    KEY_MATERIAL: self.material,
                    KEY_DISP_EFFECTIVE_AREA_PARA: self.effective_area_factor,
                    KEY_DISP_SECSIZE:  str(self.sec_list),
                    "Selected Section Details": self.report_column,
                    }

            self.report_check = []

            t1 = ('Selected', 'Selected Member Data', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
            self.report_check.append(t1)


            t1 = ('SubSection', 'Buckling Class & Imperfection factor', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
            self.report_check.append(t1)
            t1 = (KEY_DISP_BUCKLING_CURVE_ZZ, ' ',
                                cl_8_7_1_5_buckling_curve(),
                                ' ')
            self.report_check.append(t1)

            t1 = (KEY_DISP_IMPERFECTION_FACTOR_ZZ + r' ($\alpha$)', ' ',
                                cl_8_7_1_5_imperfection_factor(self.result_IF),
                                ' ')
            self.report_check.append(t1)

            t1 = ('SubSection', 'Section Classification', '|p{5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
            self.report_check.append(t1)
            self.h = (self.section_property.leg_a_length - 2 * (self.section_property.thickness + self.section_property.root_radius))
            t1 = ('Single Angle',
                cl_3_7_2_section_classification_angle_required("b/t", self.section_property.section_class),
                cl_3_7_2_section_classification_angle_provided(
                    self.section_property.min_leg, self.section_property.max_leg, self.section_property.thickness,
                    round(self.width_thickness_ratio, 2), "b/t", self.epsilon, self.section_property.section_class),
                get_pass_fail(15.7 * self.epsilon, round(self.width_thickness_ratio, 2), relation="geq")
            )
            self.report_check.append(t1)

            t1 = (
                'Double Angles with the components separated',
                cl_3_7_2_section_classification_angle_required("d/t", self.section_property.section_class),
                cl_3_7_2_section_classification_angle_provided(
                    self.section_property.min_leg, self.section_property.max_leg, self.section_property.thickness,
                    round(self.depth_thickness_ratio, 2), "d/t", self.epsilon, self.section_property.section_class),
                get_pass_fail(15.7 * self.epsilon, round(self.depth_thickness_ratio, 2), relation="geq")
            )
            self.report_check.append(t1)

            t1 = (
                'Axial Compression',
                cl_3_7_2_section_classification_angle_required("(b+d)/t", self.section_property.section_class),
                cl_3_7_2_section_classification_angle_provided(
                    self.section_property.min_leg, self.section_property.max_leg, self.section_property.thickness,
                    round(self.width_depth_thickness_ratio, 2), "(b+d)/t", self.epsilon, self.section_property.section_class),
                get_pass_fail(25 * self.epsilon, round(self.width_depth_thickness_ratio, 2), relation="geq")
            )
            self.report_check.append(t1)

            t1 = ('(All the above three criteria should be satisfied)', '', '', '')
            self.report_check.append(t1)


            t1 = ('Section Class', ' ',
                            cl_3_7_2_section_classification(
                                                                self.section_property.section_class),
                            ' ')
            self.report_check.append(t1)

            t1 = ('SubSection', 'Effective Slenderness Ratio', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
            self.report_check.append(t1)
            if self.load_type == 'Concentric Load':
                K= self.result_eff_len / self.length
                t1 = ("Effective Slenderness Ratio", ' ',
                                    cl_7_1_2_effective_slenderness_ratio(K,self.length,round(self.min_radius_gyration, 2),self.result_eff_sr),
                                    ' ')
                self.report_check.append(t1)
            else:
                t1 = ("Effective Slenderness Ratio", ' ',
                                cl_7_5_1_2_effective_slenderness_ratio(self.k1,self.k2,self.k3,self.lambda_vv,self.lambda_psi,self.result_eff_sr),
                                ' ')
                self.report_check.append(t1)


            t1 = ('SubSection', 'Checks for Strength', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
            self.report_check.append(t1)
            t1 = (KEY_DISP_EULER_BUCKLING_STRESS_ZZ, ' ',
                                cl_8_7_1_5_buckling_stress(self.section_property.modulus_of_elasticity,self.result_eff_sr, round(self.result_ebs, 2)),# here need to change just the symbol to lanbdae
                                ' ')
            self.report_check.append(t1)
            
            t1 = ('$\phi$', ' ',
                                cl_8_7_1_5_phi(0.49,round(self.nondimensional_effective_slenderness_ratio, 2), round(self.phi, 2)),#need to check this as its given only for zz but rest are values wrt yy
                                ' ')
            self.report_check.append(t1)

            t1 = (r'$F_{cd} \, \left( \frac{N}{\text{mm}^2} \right)$', ' ',
                                cl_8_7_1_5_Buckling(self.material_property.fy,self.gamma_m0,round(self.nondimensional_effective_slenderness_ratio, 2),round(self.phi, 2),round(self.design_compressive_stress_max, 2),round(self.design_compressive_stress, 2)), '')
            self.report_check.append(t1)

            t1 = ('P_d', self.load.axial_force * 10 ** -3,
                                cl_7_1_2_design_compressive_strength(round(self.result_capacity * 10 ** -3, 2),round(self.result_effective_area, 2), round(self.design_compressive_stress, 2),self.load.axial_force * 10 ** -3),
                                get_pass_fail(self.load.axial_force * 10 ** -3, round(self.result_capacity * 10 ** -3, 2), relation="leq"))
            self.report_check.append(t1)

        else:
            self.report_input = \
            {#KEY_MAIN_MODULE: self.mainmodule,
                KEY_MODULE: self.module, #"Axial load on column "
                KEY_DISP_AXIAL: self.load.axial_force/1000,
                KEY_DISP_LENGTH: self.length,
                KEY_DISP_SEC_PROFILE: self.sec_profile,
                KEY_DISP_END1: self.end_1,
                KEY_DISP_END2: self.end_2,
                #KEY_DISP_SECSIZE: self.result_section_class,
                "Strut Section - Mechanical Properties": "TITLE",
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: round(self.section_property.fu, 2),
                KEY_DISP_YIELD_STRENGTH_REPORT: round(self.section_property.fy, 2),
                KEY_MATERIAL: self.material,
                KEY_DISP_EFFECTIVE_AREA_PARA: self.effective_area_factor,
                KEY_DISP_SECSIZE:  str(self.sec_list),

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
        

    # def memb_pattern(self, status):
    #
    #     if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
    #         image = str(files("osdag.data.ResourceFiles.images").joinpath("L.png"))
    #         x, y = 400, 202
    #
    #     else:
    #         image = str(files("osdag.data.ResourceFiles.images").joinpath("U.png"))
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
    #            [str(files("osdag.data.ResourceFiles.images").joinpath("L.png")),400,202, "Plate Block Shear Pattern"])  # [image, width, height, caption]
    #     pattern.append(t99)
    #
    #     return pattern
