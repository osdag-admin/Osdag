"""
Started on 1st January, 2020.

@author: Darshan Vishwakarma

Module: Tension Member Welded Design

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 6)

"""
from design_report.reportGenerator_latex import CreateLatex
from Report_functions import *
from utils.common.component import *
# from cad.common_logic import CommonDesignLogic
from Common import *
from utils.common.load import Load
from design_type.member import Member
import logging
from utils.common.Section_Properties_Calculator import *
from design_type.main import Main


class Tension_welded(Member):

    def __init__(self):
        super(Tension_welded, self).__init__()


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

        t1 = (DISP_TITLE_ANGLE, TYPE_TAB_1, self.tab_angle_section)
        tabs.append(t1)

        t2 = (DISP_TITLE_CHANNEL, TYPE_TAB_1, self.tab_channel_section)
        tabs.append(t2)

        t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        tabs.append(t6)

        t3 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t3)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

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

         """
        change_tab = []

        t1 = (DISP_TITLE_ANGLE, [KEY_SECSIZE, KEY_SEC_MATERIAL, 'Label_0'],
              [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5',
               'Label_7', 'Label_8', 'Label_9',
               'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17',
               'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23', 'Label_24', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_new_angle_section_properties)
        change_tab.append(t1)

        t2 = (DISP_TITLE_ANGLE, ['Label_1', 'Label_2', 'Label_3'],
              ['Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15',
               'Label_16', 'Label_17', 'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23',
               KEY_IMAGE],
              TYPE_TEXTBOX, self.get_Angle_sec_properties)
        change_tab.append(t2)

        t3 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE, KEY_SEC_MATERIAL, 'Label_0'],
              [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14',
               'Label_4', 'Label_5',
               'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17',
               'Label_19', 'Label_20', 'Label_21',
               'Label_22', 'Label_23', 'Label_26', 'Label_27', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_new_channel_section_properties)
        change_tab.append(t3)

        t4 = (DISP_TITLE_CHANNEL, ['Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14'],
              ['Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17', 'Label_19',
               'Label_20', 'Label_21', 'Label_22', 'Label_26', 'Label_27', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_Channel_sec_properties)

        change_tab.append(t4)

        t5 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t5)

        t6 = (DISP_TITLE_ANGLE, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        t7 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

        return change_tab

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        t2 = (DISP_TITLE_ANGLE, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        t2 = (DISP_TITLE_CHANNEL, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        # t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        # design_input.append(t3)
        #
        # t3 = ("Bolt", TYPE_TEXTBOX, [KEY_DP_BOLT_MATERIAL_G_O])
        # design_input.append(t3)

        t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        design_input.append(t4)

        t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        design_input.append(t4)
        #
        # t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        # design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)
        #
        return design_input

    def input_dictionary_without_design_pref(self):
        """

        :return: Returns list of tuples which have the design preference keys to be stored if user does not open
        design preference (since deisgn preference values are saved on click of 'save' this function is necessary'

        ([Key need to get default values, list of design prefernce values, source of key])

        TODO: list of design preference values are sufficient in this function
         since whole of input dock design dictionary is being passed anyway in ui template
        """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_WELD_FAB,KEY_DP_WELD_MATERIAL_G_O,
                     KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

         :return: This function returns list of tuples which has keys that needs to be updated,
          on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

          [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
         """

        add_buttons = []

        t2 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE_SELECTED, None, None, "Angles")
        add_buttons.append(t2)

        t2 = (DISP_TITLE_CHANNEL, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE_SELECTED, None, None, "Channels")
        add_buttons.append(t2)

        return add_buttons

    ####################################
    # Design Preference Functions End
    ####################################

    def set_osdaglogger(key):

        """
        Function to set Logger for Tension Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('Osdag')

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

    def module_name(self):

        """
        Function to call the module name
        """
        return KEY_DISP_TENSION_WELDED

    def customized_input(self):

        "Function to populate combobox based on the option selected"


        c_lst = []

        t1 = (KEY_SECSIZE, self.fn_profile_section)
        c_lst.append(t1)

        t4 = (KEY_PLATETHK, self.plate_thick_customized)
        c_lst.append(t4)
        # t2 = (KEY_GRD, self.grdval_customized)
        # c_lst.append(t2)
        # t3 = (KEY_D, self.diam_bolt_customized)
        # c_lst.append(t3)
        # t4 = (KEY_PLATETHK, self.plate_thick_customized)
        # c_lst.append(t4)
        # t5 = (KEY_SEC_PROFILE, self.fn_conn_type)
        # c_lst.append(t5)

        return c_lst

    def fn_profile_section(self):

        "Function to populate combobox based on the section type selected"
        conn = self[0]
        if conn == 'Beams':
            return connectdb("Beams", call_type="popup")
        elif conn == 'Columns':
            return connectdb("Columns", call_type= "popup")
        elif conn in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return connectdb("Angles", call_type= "popup")
        elif conn in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type= "popup")

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_SEC_PROFILE], KEY_LOCATION, TYPE_COMBOBOX, self.fn_conn_type)
        lst.append(t1)

        t2 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t2)

        t3 = ([KEY_SEC_PROFILE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t3)

        t4 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t4)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTERCONNECTION, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTERCONNECTION, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTERSPACING, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTERSPACING, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_PLATE_HEIGHT, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_PLATE_HEIGHT, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_PLATE_LENGTH, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_PLATE_LENGTH, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_WELD_SIZE, TYPE_OUT_DOCK, self.out_intermittent)
        lst.append(t5)

        t5 = ([KEY_SEC_PROFILE], KEY_OUT_INTER_WELD_SIZE, TYPE_OUT_LABEL, self.out_intermittent)
        lst.append(t5)

        return lst

    def fn_conn_type(self):
        "Function to populate section size based on the type of section "

        profile = self[0]
        if profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return VALUES_LOCATION_1
        elif profile in ["Channels", "Back to Back Channels"]:
            return VALUES_LOCATION_2

    def fn_conn_image(self):

        "Function to populate section size based on the type of section "
        img = self[0]
        if img == VALUES_SEC_PROFILE_2[0]:
            return VALUES_IMG_TENSIONWELDED[0]
        elif img ==VALUES_SEC_PROFILE_2[1]:
            return VALUES_IMG_TENSIONWELDED[1]
        elif img ==VALUES_SEC_PROFILE_2[2]:
            return VALUES_IMG_TENSIONWELDED[2]
        elif img ==VALUES_SEC_PROFILE_2[3]:
            return VALUES_IMG_TENSIONWELDED[3]
        else:
            return VALUES_IMG_TENSIONWELDED[4]


    def out_intermittent(self):

        sec_type = self[0]
        if sec_type in [VALUES_SEC_PROFILE_2[0], VALUES_SEC_PROFILE_2[3]]:
            return True
        else:
            return False

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair
        self.module = KEY_DISP_TENSION_WELDED
        self.mainmodule = 'Member'
        self.connection = "Welded"

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_TENSION_WELDED, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, VALUES_SEC_PROFILE_2, True, 'No Validator')
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, VALUES_IMG_TENSIONWELDED[0] , True, 'No Validator')

        options_list.append(t15)

        t3 = (KEY_LOCATION, KEY_DISP_LOCATION, TYPE_COMBOBOX, VALUES_LOCATION_1, True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t5 = (KEY_LENGTH, KEY_DISP_LENGTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t7 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t7)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK, True, 'No Validator')
        options_list.append(t14)



        return options_list

    def spacing(self, status):

        spacing = []

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair

        out_list = []

        t1 = (None, DISP_TITLE_TENSION_SECTION, TYPE_TITLE, None, True)
        out_list.append(t1)
        # t1 = (None, DISP_TITLE_TENSION_SECTION, TYPE_TITLE, None, True)
        # out_list.append(t1)

        t2 = (KEY_DESIGNATION, KEY_DISP_DESIGNATION, TYPE_TEXTBOX,
              self.section_size_1.designation if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_TENSION_YIELDCAPACITY, KEY_DISP_TENSION_YIELDCAPACITY, TYPE_TEXTBOX, round((self.section_size_1.tension_yielding_capacity/1000),2) if flag else '', True)
        out_list.append(t3)

        t4 = (KEY_TENSION_RUPTURECAPACITY, KEY_DISP_TENSION_RUPTURECAPACITY, TYPE_TEXTBOX,
              round((self.section_size_1.tension_rupture_capacity/1000),2) if flag else '', True)
        out_list.append(t4)

        # t1 = ("mm", DISP_TITLE_TENSION_SECTION, TYPE_TITLE, None, True)
        # out_list.append(t1)

        # t5 = (KEY_TENSION_BLOCKSHEARCAPACITY, KEY_DISP_TENSION_BLOCKSHEARCAPACITY, TYPE_TEXTBOX,
        #       round((self.section_size_1.block_shear_capacity_axial/1000),2) if flag else '', True)
        # out_list.append(t5)

        t6 = (KEY_TENSION_CAPACITY, KEY_DISP_TENSION_CAPACITY, TYPE_TEXTBOX,
              round((self.section_size_1.tension_capacity/1000),2) if flag else '', True)
        out_list.append(t6)

        t6 = (KEY_SLENDER, KEY_DISP_SLENDER, TYPE_TEXTBOX,
              self.section_size_1.slenderness if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_EFFICIENCY, KEY_DISP_EFFICIENCY, TYPE_TEXTBOX,
               self.efficiency if flag else '', True)
        out_list.append(t7)

        t8 = (None, DISP_TITLE_END_CONNECTION, TYPE_TITLE, None, True)
        out_list.append(t8)

        t8 = (None, DISP_TITLE_WELD_DETAILS, TYPE_TITLE, None, True)
        out_list.append(t8)

        t9 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX, "Fillet Weld" if flag else '', True)
        out_list.append(t9)

        t9 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX, self.weld.size if flag else '', True)
        out_list.append(t9)

        t10 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX, round(self.weld.strength,2) if flag else '', True)
        out_list.append(t10)


        t5 = (KEY_REDUCTION_LONG_JOINT, KEY_DISP_REDUCTION_LONG_JOINT, TYPE_TEXTBOX,round(self.weld.beta_lw, 2) if flag else '', True)
        out_list.append(t5)

        t10 = (KEY_OUT_WELD_STRENGTH_RED, KEY_OUT_DISP_WELD_STRENGTH_RED, TYPE_TEXTBOX, round(self.weld.strength_red, 2) if flag else '',
        True)
        out_list.append(t10)

        t11 = (KEY_OUT_WELD_STRESS, KEY_OUT_DISP_WELD_STRESS, TYPE_TEXTBOX, round(self.weld.stress,2) if flag else '', True)
        out_list.append(t11)

# <<<<<<< HEAD
#         # t5 = (KEY_OUT_WELD_LENGTH, KEY_OUT_DISP_WELD_LENGTH, TYPE_TEXTBOX, round(self.weld.length,0) if flag else '')
#         # out_list.append(t5)
#
#         t13 = (KEY_OUT_WELD_LENGTH_EFF, KEY_OUT_DISP_WELD_LENGTH_EFF, TYPE_TEXTBOX, int(round(self.weld.length,0)) if flag else '')
# =======
#         t5 = (KEY_OUT_WELD_LENGTH, KEY_OUT_DISP_WELD_LENGTH, TYPE_TEXTBOX, self.weld.length if flag else '', True)
#         out_list.append(t5)

        t13 = (KEY_OUT_WELD_LENGTH_EFF, KEY_OUT_DISP_WELD_LENGTH_EFF, TYPE_TEXTBOX, int(round(self.weld.length,0)) if flag else '', True)

        out_list.append(t13)

        t18 = (None, DISP_TITLE_GUSSET_PLATE, TYPE_TITLE, None, True)
        out_list.append(t18)


        t19 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, int(round(self.plate.thickness_provided,0)) if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_MIN_HEIGHT, TYPE_TEXTBOX, int(round(self.plate.height,0)) if flag else '', True)
        out_list.append(t20)

        t21 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_MIN_LENGTH, TYPE_TEXTBOX,int(round(self.plate.length,0)) if flag else '', True)

        out_list.append(t21)

        t21 = (KEY_OUT_PLATE_YIELD, KEY_DISP_TENSION_YIELDCAPACITY, TYPE_TEXTBOX,
               (round(self.plate.tension_yielding_capacity / 1000, 2)) if flag else '', True)
        out_list.append(t21)

        # t21 = (KEY_OUT_PLATE_RUPTURE, KEY_DISP_TENSION_RUPTURECAPACITY, TYPE_TEXTBOX,
        #        (round(self.plate.tension_rupture_capacity / 1000, 2)) if flag else '', True)
        # out_list.append(t21)

        t21 = (KEY_OUT_PLATE_BLK_SHEAR, KEY_DISP_TENSION_BLOCKSHEARCAPACITY, TYPE_TEXTBOX,
               (round(self.plate.block_shear_capacity / 1000, 2)) if flag else '', True)
        out_list.append(t21)

        t17 = (KEY_OUT_PATTERN_2, KEY_OUT_DISP_PATTERN, TYPE_OUT_BUTTON, ['Shear Pattern ', self.plate_pattern], True)
        out_list.append(t17)

        t21 = (KEY_OUT_PLATE_CAPACITY, KEY_DISP_TENSION_CAPACITY, TYPE_TEXTBOX,
               (round(self.plate_tension_capacity / 1000, 2)) if flag else '', True)

        out_list.append(t21)

        t18 = (None, DISP_TITLE_INTERMITTENT, TYPE_TITLE, None, False)
        out_list.append(t18)

        t8 = (None, DISP_TITLE_CONN_DETAILS , TYPE_TITLE, None, False)
        out_list.append(t8)

        t21 = (KEY_OUT_INTERCONNECTION, KEY_OUT_DISP_INTERCONNECTION, TYPE_TEXTBOX,
               int(round(self.inter_conn, 0)) if flag else '', False)
        out_list.append(t21)

        t21 = (KEY_OUT_INTERSPACING, KEY_OUT_DISP_INTERSPACING, TYPE_TEXTBOX,
               (round(self.inter_memb_length, 2)) if flag else '', False)
        out_list.append(t21)

        t8 = (None, DISP_TITLE_WELD_DETAILS, TYPE_TITLE, None, False)
        out_list.append(t8)

        t9 = (KEY_OUT_INTER_WELD_SIZE, KEY_OUT_DISP_INTER_WELD_SIZE, TYPE_TEXTBOX, self.inter_weld_size if flag else '', False)
        out_list.append(t9)

        t18 = (None, DISP_TITLE_PLATED, TYPE_TITLE, None, False)
        out_list.append(t18)

        t20 = (KEY_OUT_INTER_PLATE_HEIGHT, KEY_OUT_DISP_INTER_PLATE_HEIGHT, TYPE_TEXTBOX,
               int(round(self.inter_plate_height, 0)) if flag else '', False)
        out_list.append(t20)

        t21 = (KEY_OUT_INTER_PLATE_LENGTH, KEY_OUT_DISP_INTER_PLATE_LENGTH, TYPE_TEXTBOX,
               int(round(self.inter_plate_length, 0)) if flag else '', False)
        out_list.append(t21)

        return out_list

    def plate_pattern(self, status):

        pattern = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern ")
        pattern.append(t00)

        t99 = (None, 'Failure Pattern Due to Tension Force in the Plate', TYPE_SECTION,
               ['./ResourceFiles/images/Lw.png', 400, 202, "Plate Block Shear Pattern"])  # [image, width, height, caption]
        pattern.append(t99)

        t9 = (KEY_OUT_Lw, KEY_OUT_DISP_Lw, TYPE_TEXTBOX, round(int(self.plate.length-max((2 * self.weld.size),15)),2) if status else '')
        pattern.append(t9)

        t10 = (KEY_OUT_Hw, KEY_OUT_DISP_Hw, TYPE_TEXTBOX, round(int(self.plate.height-max((2 * self.weld.size),15)),2) if status else '')
        pattern.append(t10)

        return pattern

    def func_for_validation(self, design_dictionary):

        all_errors = []
        "check valid inputs and empty inputs in input dock"

        self.design_status = False

        flag = False
        flag1 = False
        flag2 = False
        option_list = self.input_values(self)
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
                else:
                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_LENGTH:
                        # val = option[4]
                        # print(design_dictionary[option[0]], "jhvhj")
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True

                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_AXIAL:

                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag2 = True
            else:
                pass

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True
        # print(all_errors, "ysdgh")
        # print(flag, flag1, flag2)
        if flag and flag1 and flag2:
            self.set_input_values(self, design_dictionary)
            # print(design_dictionary)
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

        "initialisation of components required to design a tension member along with connection"

        super(Tension_welded,self).set_input_values(self, design_dictionary)
        print(design_dictionary,"input values are set. Doing preliminary member checks")
        self.module = design_dictionary[KEY_MODULE]
        self.sizelist = design_dictionary[KEY_SECSIZE]
        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]
        self.loc = design_dictionary[KEY_LOCATION]
        # self.plate_thickness = [3,4,6,8,10,12,14,16,20,22,24,25,26,28,30,32,36,40,45,50,56,63,80]
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.material = design_dictionary[KEY_SEC_MATERIAL]

        # print(self.sizelist)
        self.length = float(design_dictionary[KEY_LENGTH])
        # print(self.bolt)
        self.load = Load(shear_force="", axial_force=design_dictionary.get(KEY_AXIAL))
        self.efficiency = 0.0
        self.K = 1
        self.count = 0
        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL])
        self.weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                         fabrication=design_dictionary[KEY_DP_WELD_FAB])

        print("input values are set. Doing preliminary member checks")
        # self.i = 0

        self.member_design_status = False
        self.max_limit_status_1 = False
        self.max_limit_status_2 = False
        self.weld_design_status = False
        self.thick_design_status = False
        self.plate_design_status = False
        self.initial_member_capacity(self,design_dictionary)


    def select_section(self, design_dictionary, selectedsize):

        "selecting components class based on the section passed "


        if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Back to Back Angles', 'Star Angles']:
            self.section_size = Angle(designation=selectedsize, material_grade=design_dictionary[KEY_SEC_MATERIAL])
        elif design_dictionary[KEY_SEC_PROFILE] in ['Channels', 'Back to Back Channels']:
            self.section_size = Channel(designation=selectedsize, material_grade=design_dictionary[KEY_SEC_MATERIAL])
        else:
            pass

        return self.section_size

    def max_section(self, design_dictionary, sizelist):

        "selecting components class based on the section passed "
        sec_area = {}
        sec_gyr = {}
        for section in sizelist:
            if design_dictionary[KEY_SEC_PROFILE] in ['Angles']:
                self.section = Angle(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL])
                self.min_rad_gyration_calc(self, designation=section,
                                           material_grade=design_dictionary[KEY_SEC_MATERIAL],
                                           key=design_dictionary[KEY_SEC_PROFILE],
                                           subkey=design_dictionary[KEY_LOCATION], D_a=self.section.a,
                                           B_b=self.section.b, T_t=self.section.thickness)
                sec_gyr[self.section.designation] = self.min_radius_gyration

            elif design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Angles', 'Star Angles']:
                self.section = Angle(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL])
                self.min_rad_gyration_calc(self, designation=section,
                                           material_grade=design_dictionary[KEY_SEC_MATERIAL],
                                           key=design_dictionary[KEY_SEC_PROFILE],
                                           subkey=design_dictionary[KEY_LOCATION], D_a=self.section.a,
                                           B_b=self.section.b, T_t=self.section.thickness)

                sec_gyr[self.section.designation] = self.min_radius_gyration

            else:
                self.section = Channel(designation=section, material_grade=design_dictionary[KEY_SEC_MATERIAL])
                self.min_rad_gyration_calc(self, designation=section,
                                           material_grade=design_dictionary[KEY_SEC_MATERIAL],
                                           key=design_dictionary[KEY_SEC_PROFILE],
                                           subkey=design_dictionary[KEY_LOCATION], D_a=self.section.depth,
                                           B_b=self.section.flange_width, T_t=self.section.flange_thickness,
                                           t=self.section.web_thickness)
                sec_gyr[self.section.designation] = self.min_radius_gyration

            sec_area[self.section.designation] = self.section.area

        print(sec_gyr)
        if len(sec_area) >= 2:
            self.max_area = max(sec_area, key=sec_area.get)
        else:
            self.max_area = self.section.designation

        if len(sec_gyr) >= 2:
            self.max_gyr = max(sec_gyr, key=sec_gyr.get)
        else:
            self.max_gyr = self.section.designation

        return self.max_area, self.max_gyr

    def max_force_length(self, section):

        "calculated max force and length based on the maximum section size avaialble for diff section type"

        if self.sec_profile == 'Angles':
            # print (Angle)

            self.section_size_max = Angle(designation=section, material_grade=self.material)
            self.section_size_max.tension_member_yielding(A_g=(self.section_size_max.area),
                                                          F_y=self.section_size_max.fy)
            self.max_member_force = self.section_size_max.tension_yielding_capacity
            self.min_rad_gyration_calc(self, designation=section, material_grade=self.material,
                                       key=self.sec_profile, subkey=self.loc, D_a=self.section_size_max.a,
                                       B_b=self.section_size_max.b, T_t=self.section_size_max.thickness)
            self.max_length = 400 * self.min_radius_gyration

        elif self.sec_profile in ['Back to Back Angles', 'Star Angles']:
            self.section_size_max = Angle(designation=section, material_grade=self.material)
            self.section_size_max.tension_member_yielding(A_g=(2 * self.section_size_max.area),
                                                          F_y=self.section_size_max.fy)
            # self.max_member_force = self.section_size_max.tension_yielding_capacity * 2
            self.min_rad_gyration_calc(self, designation=section, material_grade=self.material,
                                       key=self.sec_profile, subkey=self.loc, D_a=self.section_size_max.a,
                                       B_b=self.section_size_max.b, T_t=self.section_size_max.thickness)
            self.max_length = 400 * self.min_radius_gyration

        elif self.sec_profile == 'Channels':
            self.section_size_max = Channel(designation=section, material_grade=self.material)
            self.section_size_max.tension_member_yielding(A_g=(self.section_size_max.area),
                                                          F_y=self.section_size_max.fy)

            self.max_member_force = self.section_size_max.tension_yielding_capacity
            self.min_rad_gyration_calc(self, designation=section, material_grade=self.material,
                                       key=self.sec_profile, subkey=self.loc, D_a=self.section_size_max.depth,
                                       B_b=self.section_size_max.flange_width,
                                       T_t=self.section_size_max.flange_thickness,
                                       t=self.section_size_max.web_thickness)
            self.max_length = 400 * self.min_radius_gyration


        elif self.sec_profile == 'Back to Back Channels':
            self.section_size_max = Channel(designation=section, material_grade=self.material)
            self.section_size_max.tension_member_yielding(A_g=(2 * self.section_size_max.area),
                                                          F_y=self.section_size_max.fy)
            # self.max_member_force = 2 * self.section_size_max.tension_yielding_capacity
            self.min_rad_gyration_calc(self, designation=section, material_grade=self.material,
                                       key=self.sec_profile, subkey=self.loc, D_a=self.section_size_max.depth,
                                       B_b=self.section_size_max.flange_width,
                                       T_t=self.section_size_max.flange_thickness,
                                       t=self.section_size_max.web_thickness)
            self.max_length = 400 * self.min_radius_gyration
        self.section_size_max.design_check_for_slenderness(K=self.K, L=self.length,
                                                           r=self.min_radius_gyration)

        return self.section_size_max.tension_yielding_capacity, self.max_length, self.section_size_max.slenderness, self.min_radius_gyration

    def min_rad_gyration_calc(self, designation, material_grade, key, subkey, D_a=0.0, B_b=0.0, T_t=0.0, t=0.0):

        if key == "Channels" and subkey == "Web":
            Channel_attributes = Channel(designation, material_grade)
            rad_y = Channel_attributes.rad_of_gy_y
            rad_z = Channel_attributes.rad_of_gy_z
            min_rad = min(rad_y, rad_z)

        elif key == 'Back to Back Channels' and subkey == "Web":
            BBChannel_attributes = BBChannel_Properties()
            BBChannel_attributes.data(designation, material_grade)
            rad_y = BBChannel_attributes.calc_RogY(f_w=B_b, f_t=T_t, w_h=D_a, w_t=t) * 10
            rad_z = BBChannel_attributes.calc_RogZ(f_w=B_b, f_t=T_t, w_h=D_a, w_t=t) * 10
            min_rad = min(rad_y, rad_z)

        elif key == "Back to Back Angles" and subkey == 'Long Leg':
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            rad_y = BBAngle_attributes.calc_RogY(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            min_rad = min(rad_y, rad_z)

        elif key == 'Back to Back Angles' and subkey == 'Short Leg':
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            rad_y = BBAngle_attributes.calc_RogY(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            min_rad = min(rad_y, rad_z)

        elif key == 'Star Angles' and subkey == 'Long Leg':
            SAngle_attributes = SAngle_Properties()
            SAngle_attributes.data(designation, material_grade)
            rad_y = SAngle_attributes.calc_RogY(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_z = SAngle_attributes.calc_RogZ(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_u = SAngle_attributes.calc_RogU(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_v = SAngle_attributes.calc_RogV(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            min_rad = min(rad_y, rad_z, rad_u, rad_v)

        elif key == 'Star Angles' and subkey == 'Short Leg':
            SAngle_attributes = SAngle_Properties()
            SAngle_attributes.data(designation, material_grade)
            rad_y = SAngle_attributes.calc_RogY(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_z = SAngle_attributes.calc_RogZ(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_u = SAngle_attributes.calc_RogU(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            rad_v = SAngle_attributes.calc_RogV(a=D_a, b=B_b, t=T_t, l=subkey) * 10
            min_rad = min(rad_y, rad_z, rad_u, rad_v)

        elif key == 'Angles' and (subkey == 'Long Leg' or subkey == 'Short Leg'):
            Angle_attributes = Angle(designation, material_grade)
            rad_u = Angle_attributes.rad_of_gy_u
            rad_v = Angle_attributes.rad_of_gy_v
            min_rad = min(rad_u, rad_v)

        self.min_radius_gyration = min_rad

    def initial_member_capacity(self,design_dictionary,previous_size = None):

        "selection of member based on the yield capacity"
        min_yield = 0

        if self.count == 0:
            self.max_section(self, design_dictionary, self.sizelist)
            [self.force1, self.len1, self.slen1, self.gyr1] = self.max_force_length(self, self.max_area)
            [self.force2, self.len2, self.slen2, self.gyr2] = self.max_force_length(self, self.max_gyr)
        else:
            pass

        self.count = self.count + 1
        "Loop checking each member from sizelist based on yield capacity on recheck"
        if (previous_size) == None:
            pass
        else:
            if previous_size in self.sizelist:
                self.sizelist.remove(previous_size)
            else:
                pass

        for selectedsize in self.sizelist:
            # print(self.sizelist)
            self.section_size = self.select_section(self,design_dictionary,selectedsize)
            # print(self.section_size)

            if design_dictionary[KEY_SEC_PROFILE] =='Angles' or design_dictionary[KEY_SEC_PROFILE] =='Channels':
                self.cross_area = self.section_size.area

            else:
                self.cross_area = self.section_size.area * 2

            "excluding previous section size which failed in rupture and selecting higher section based on the cross section area "

            self.section_size.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
            self.K = 1.0
            # print(self.section_size.rad_of_gy_z)
            if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
                # print(selectedsize)
                self.min_rad_gyration_calc(self, designation=self.section_size.designation,
                                           material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, D_a=self.section_size.a,
                                           B_b=self.section_size.b, T_t=self.section_size.thickness)
            else:
                self.min_rad_gyration_calc(self, designation=self.section_size.designation,
                                           material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, D_a=self.section_size.depth,
                                           B_b=self.section_size.flange_width, T_t=self.section_size.flange_thickness,
                                           t=self.section_size.web_thickness)
            # print(design_dictionary[KEY_SEC_PROFILE], design_dictionary[KEY_LOCATION], self.section_size.min_radius_gyration)
            self.section_size.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],
                                                           r=self.min_radius_gyration)

            "condition for yield and slenderness check "

            if (self.section_size.tension_yielding_capacity >= self.load.axial_force * 1000) and self.section_size.slenderness < 400:
                min_yield_current = self.section_size.tension_yielding_capacity
                self.member_design_status = True
                if min_yield == 0:
                    min_yield = min_yield_current
                    self.section_size_1 = self.select_section(self, design_dictionary, selectedsize)
                    self.section_size_1.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
                    if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
                        self.min_rad_gyration_calc(self, designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.a,
                                                   B_b=self.section_size_1.b, T_t=self.section_size_1.thickness)

                    else:
                        self.min_rad_gyration_calc(self, designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.depth,
                                                   B_b=self.section_size_1.flange_width,
                                                   T_t=self.section_size_1.flange_thickness,
                                                   t=self.section_size_1.web_thickness)

                    self.section_size_1.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],
                                                                     r=self.min_radius_gyration)

                elif min_yield_current < min_yield:
                    min_yield = min_yield_current
                    self.section_size_1 = self.select_section(self, design_dictionary, selectedsize)
                    self.section_size_1.tension_member_yielding(A_g=self.cross_area, F_y=self.section_size.fy)
                    if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
                        self.min_rad_gyration_calc(self, designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.a,
                                                   B_b=self.section_size_1.b, T_t=self.section_size_1.thickness)
                    else:
                        self.min_rad_gyration_calc(self, designation=self.section_size_1.designation,
                                                   material_grade=self.material,
                                                   key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.depth,
                                                   B_b=self.section_size_1.flange_width,
                                                   T_t=self.section_size_1.flange_thickness,
                                                   t=self.section_size_1.web_thickness)
                    self.section_size_1.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],
                                                                     r=self.min_radius_gyration)

                # print(self.section_size_1.slenderness)
                "condition to limit loop based on max force derived from max available size"


            elif (self.load.axial_force * 1000 > self.force1):
                self.max_limit_status_1 = True
                # self.design_status = False
                logger.warning(" : The factored tension force ({} kN) exceeds the tension capacity ({} kN) with respect to the maximum available "
                               "member size {}.".format(round(self.load.axial_force,2),round(self.force1/1000,2),self.max_area))
                logger.info(" : Define member(s) with a higher cross sectional area.")
                # logge r.error(": Design is not safe. \n ")
                # logger.info(" :=========End Of design===========")
                break

                "condition to limit loop based on max length derived from max available size"


            elif self.length > self.len2:
                self.max_limit_status_2 = True
                # self.design_status = False
                logger.warning(" : The member length ({} mm) exceeds the maximum allowable length ({} mm) with respect to the maximum available "
                               "member size {}.".format(self.length,round(self.len2,2),self.max_gyr))
                logger.info(" : Select member(s) with a higher radius of gyration value.")
                break
            else:
                pass

        if self.member_design_status == False and self.max_limit_status_1 != True and self.max_limit_status_2 != True:
            logger.warning(" : The available depth of the member cannot accommodate the minimum available bolt diameter of {} mm considering the "
                           "minimum spacing limit [Ref. Cl. 10.2, IS 800:2007].".format(self.bolt_diameter_min))
            logger.info(" : Reduce the bolt diameter or increase the member depth and re-design.")
            # logger.error(": Design is not safe. \n ")
            # logger.info(" :=========End Of design===========")

        if self.member_design_status == True:
            print("pass")
            self.design_status = True
            self.initial_plate_check(self, design_dictionary)
        else:
            self.design_status = False
            logger.error(": Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")

    def initial_plate_check(self, design_dictionary):

        "Initialisation of plate thickness based on yield strength to determine weld size"
        self.res_force = max((self.load.axial_force*1000),(0.3*self.section_size_1.tension_yielding_capacity))

        # if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
        #     self.thick = self.section_size_1.web_thickness
        # else:
        #     self.thick = self.section_size_1.thickness
        # self.thickness_possible = [i for i in self.plate.thickness if i >= self.thick]
        # # self.plate_thick_weld = self.thickness_possible[-1]
        self.last_thk = self.plate.thickness[-1]

        for self.plate.thickness_provided in self.plate.thickness:
            if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
                self.plate.tension_yielding(length=self.section_size_1.depth, thickness=self.plate.thickness_provided,
                                            fy=self.plate.fy)
                self.net_area = self.section_size_1.depth * self.plate.thickness_provided

            elif design_dictionary[KEY_SEC_PROFILE] == "Star Angles" and design_dictionary[KEY_LOCATION] == 'Long Leg' :
                self.plate.tension_yielding(length=2*self.section_size_1.max_leg, thickness=self.plate.thickness_provided,
                                            fy=self.plate.fy)
                self.net_area = 2*self.section_size_1.max_leg * self.plate.thickness_provided

            elif design_dictionary[KEY_SEC_PROFILE] == "Star Angles" and design_dictionary[KEY_LOCATION] == 'Short Leg' :
                self.plate.tension_yielding(length=2*self.section_size_1.min_leg, thickness=self.plate.thickness_provided,
                                            fy=self.plate.fy)
                self.net_area = 2*self.section_size_1.min_leg * self.plate.thickness_provided


            else:
                if design_dictionary[KEY_LOCATION] == 'Long Leg':
                    self.plate.tension_yielding(length=self.section_size_1.max_leg,
                                                thickness=self.plate.thickness_provided, fy=self.plate.fy)
                    self.net_area = self.section_size_1.max_leg * self.plate.thickness_provided
                else:
                    self.plate.tension_yielding(length=self.section_size_1.min_leg,
                                                thickness=self.plate.thickness_provided, fy=self.plate.fy)
                    self.net_area = self.section_size_1.min_leg * self.plate.thickness_provided

            self.plate.tension_rupture(A_n=self.net_area, F_u=self.plate.fu)

            tension_capacity = min (self.plate.tension_yielding_capacity,self.plate.tension_rupture_capacity)

            if tension_capacity > self.res_force:
                break

        if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels',"Star Angles"]:
            self.max_tension_yield = 400*self.plate.fy*self.last_thk/1.1
        else:
            self.max_tension_yield = 200*self.plate.fy*self.last_thk/1.1

        "Increasing sectionsize to suffice the plate requirement"

        if tension_capacity >=self.res_force:
            print(self.plate.thickness_provided)
            self.thick_design_status = True
            self.design_status = True
            self.select_weld(self, design_dictionary)

        else:
            if tension_capacity < self.max_tension_yield and self.res_force < self.max_tension_yield:
                # self.initial_member_capacity(self, design_dictionary, previous_size=self.section_size_1.designation)
                if len(self.sizelist) >= 2:
                    size = self.section_size_1.designation
                    print("recheck", size)
                    self.initial_member_capacity(self, design_dictionary, size)
                else:
                    self.design_status = False
                    logger.warning(":Tension force {} kN exceeds tension capacity of {} kN for maximum available plate thickness of 80 mm.".format(
                            round(self.res_force / 1000, 2), round(self.max_tension_yield/1000,2)))

                    logger.error(":Design is not safe. \n ")
                    logger.info(":=========End Of design===========")

            else:
                self.design_status = False
                logger.warning(": The tension force ({} kN) exceeds the tension capacity of {} kN for maximum available plate thickness of 80 mm."
                    .format(round(self.res_force / 1000, 2),  round(self.max_tension_yield/1000,2)))
                logger.error(":Design is unsafe. \n ")
                logger.info(":=========End Of design===========")

    def select_weld(self,design_dictionary):

        "Selection of weld size based on the initial thickness considered"

        self.web_weld_status = True
        if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
            self.thick = self.section_size_1.web_thickness
            self.thick_1 = self.section_size_1.flange_thickness
        else:
            self.thick = self.section_size_1.thickness

        self.weld.weld_size(plate_thickness = self.plate.thickness_provided, member_thickness= self.thick , edge_type= "Rolled")

        self.get_weld_strength(self,connecting_fu= [self.section_size_1.fu,self.plate.fu,self.weld.fu], weld_fabrication = self.weld.fabrication , t_weld = self.weld.size, force = (self.res_force))
        print (self.weld.effective, "weld eff")
        self.weld_plate_length(self, design_dictionary)
        self.weld.get_weld_stress(weld_shear=0,weld_axial=self.res_force, l_weld=self.weld.length)
        # print(self.plate.length, self.weld.throat, "xfsf")
        if self.plate.length > (150 * self.weld.throat) and design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
            logger.info(" To satisfy the long joint limit, weld is provided only on the flanges.")
            self.web_weld_status = False
            self.weld.weld_size(plate_thickness=self.plate.thickness_provided, member_thickness=self.thick_1,edge_type="Rolled")
            self.get_weld_strength(self, connecting_fu=[self.section_size_1.fu, self.plate.fu, self.weld.fu],
                                   weld_fabrication=self.weld.fabrication, t_weld=self.weld.size,
                                   force=(self.res_force))
            self.weld_plate_length(self, design_dictionary,"web_weld")
            self.weld.get_weld_stress(weld_shear=0,weld_axial=self.res_force, l_weld=self.weld.length)

        # "Check for long joint"
        # if self.plate.length > (150 * self.weld.throat):
        #     logger.info(" Length of Joint is more than Long Joint Limit. Hence not possible.")
        #     logger.error(": Design is not safe. \n ")
        #     logger.info(" :=========End Of design===========")
        self.weld.strength_red = self.weld.strength
        while self.plate.length > (150 * self.weld.throat):

            self.weld.get_weld_red(t_t = self.weld.throat,strength = self.weld.strength,length = self.plate.length, height = self.plate.height)

            # self.weld.strength = self.weld.beta_lw * self.weld.strength
            # self.weld.effective = (self.load.axial_force * 1000 / self.weld.strength)
            self.weld.get_weld_stress(weld_shear=0,weld_axial = self.res_force, l_weld = self.weld.length)

            if self.weld.strength_red> self.weld.stress:
                self.weld_plate_length(self, design_dictionary)
                break
            else:
                self.weld.effective = round_up((self.res_force/self.weld.strength),100,1)
                self.weld_plate_length(self, design_dictionary)

        # if self.weld.strength < self.weld.stress and Btw <= 0.6:
        #     previous_size = self.section_size_1.designation
        #     self.initial_member_capacity(self, design_dictionary, previous_size)
        # else:
        #     pass
        if self.weld.strength_red > self.weld.stress:
            self.weld_design_status = True
            self.design_status = True
            self.member_check(self, design_dictionary)
        else:
            self.design_status = False
            logger.warning(": The member fails in long joint. \n ")
            logger.error(": Design is unsafe.\n ")
            logger.info(" :=========End Of design===========")


    def get_weld_strength(self,connecting_fu, weld_fabrication, t_weld, force, weld_angle = 90):

        "Function to calculate weld strength, effective weld length and throat thickness"

        f_wd = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(connecting_fu, weld_fabrication)
        throat_tk = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(t_weld, weld_angle)
        self.Kt = IS800_2007.cl_10_5_3_2_factor_for_throat_thickness(weld_angle)
        weld_strength = f_wd * throat_tk
        L_eff = round_up((force/weld_strength),5,100)
        self.weld.strength =  round(weld_strength,2)
        self.weld.effective = L_eff
        self.weld.throat = throat_tk

    def weld_plate_length (self,design_dictionary, web = None):

        "Function to calculate weld length, plate length and plate height"

        if design_dictionary[KEY_SEC_PROFILE] == "Channels":
            if web == None:
                self.web_weld = self.section_size_1.depth - 2 * self.weld.size
            else:
                self.web_weld = 0.0
            self.flange_weld = round_up(((self.weld.effective - self.web_weld ) / 2), 1, 50)
            self.weld.length = (self.web_weld + 2 * self.flange_weld)

        elif design_dictionary[KEY_SEC_PROFILE] == 'Back to Back Channels':
            if web == None:
                self.web_weld = 2 * (self.section_size_1.depth - 2 * self.weld.size)
            else:
                self.web_weld = 0.0
            self.flange_weld = round_up(((self.weld.effective - self.web_weld ) / 4), 1, 50)
            self.weld.length = (self.web_weld + 4 * self.flange_weld)

        elif design_dictionary[KEY_SEC_PROFILE] in ["Star Angles", "Back to Back Angles"] and design_dictionary[
            KEY_LOCATION] == "Long Leg":

            if web == None:
                self.web_weld = 2 * (self.section_size_1.max_leg - 2 * self.weld.size)
            else:
                self.web_weld = 0.0
            length_weld = self.section_size_1.angle_weld_length(self.weld.strength,self.web_weld/2,self.res_force/2,self.section_size_1.Cy,self.section_size_1.max_leg )
            self.flange_weld = round_up((length_weld), 1, 50)
            self.weld.length = (self.web_weld + 4 * self.flange_weld)

        elif design_dictionary[KEY_SEC_PROFILE] in ["Star Angles", "Back to Back Angles"] and design_dictionary[
            KEY_LOCATION] == "Short Leg":
            if web == None:
                self.web_weld = 2 * (self.section_size_1.min_leg - 2 * self.weld.size)
            else:
                self.web_weld = 0.0
            length_weld = self.section_size_1.angle_weld_length(self.weld.strength,self.web_weld/2,self.res_force/2,self.section_size_1.Cz,self.section_size_1.min_leg )
            self.flange_weld = round_up((length_weld), 1, 50)
            self.weld.length = (self.web_weld + 4 * self.flange_weld)

        elif design_dictionary[KEY_SEC_PROFILE] == "Angles" and design_dictionary[KEY_LOCATION] == "Long Leg":
            if web == None:
                self.web_weld = (self.section_size_1.max_leg - 2 * self.weld.size)
            else:
                self.web_weld = 0.0
            length_weld = self.section_size_1.angle_weld_length(self.weld.strength,self.web_weld,self.res_force,self.section_size_1.Cy,self.section_size_1.max_leg )
            self.flange_weld = round_up((length_weld), 1, 50)
            self.weld.length = (self.web_weld + 2 * self.flange_weld)

        else:
            if web == None:
                self.web_weld = (self.section_size_1.min_leg - 2 * self.weld.size)
            else:
                self.web_weld = 0.0
            length_weld = self.section_size_1.angle_weld_length(self.weld.strength,self.web_weld,self.res_force,self.section_size_1.Cz,self.section_size_1.min_leg )
            self.flange_weld = round_up((length_weld), 1, 50)
            self.weld.length = (self.web_weld + 2 * self.flange_weld)


        self.plate.length = self.flange_weld + max((4 * self.weld.size),30)
        if design_dictionary[KEY_SEC_PROFILE] == "Star Angles" and design_dictionary[KEY_LOCATION] == "Long Leg":
            self.plate.height = 2 * self.section_size_1.max_leg + max((4 * self.weld.size),30)
        elif design_dictionary[KEY_SEC_PROFILE] == "Star Angles" and design_dictionary[KEY_LOCATION] == "Short Leg":
            self.plate.height = 2 * self.section_size_1.min_leg + max((4 * self.weld.size),30)
        elif design_dictionary[KEY_SEC_PROFILE] in ["Back to Back Angles", "Angles"] and design_dictionary[KEY_LOCATION] == "Short Leg":
            self.plate.height = self.section_size_1.min_leg + max((4 * self.weld.size),30)
        elif design_dictionary[KEY_SEC_PROFILE] in ["Back to Back Angles","Angles"] and design_dictionary[KEY_LOCATION] == "Long Leg":
            self.plate.height = self.section_size_1.max_leg + max((4 * self.weld.size),30)
        else:
            self.plate.height = self.section_size_1.depth + max((4 * self.weld.size),30)

    def member_check(self,design_dictionary):

        "Checking selected section for rupture"

        if design_dictionary[KEY_LOCATION] == 'Long Leg':
            w = self.section_size_1.min_leg
            shear_lag = w
            L_c = (self.plate.length - max((2 * self.weld.size),15))
            A_go = self.section_size_1.min_leg * self.section_size_1.thickness
            A_nc = ((self.section_size_1.max_leg- self.section_size_1.thickness) * self.section_size_1.thickness)
            t = self.section_size_1.thickness

        elif design_dictionary[KEY_LOCATION] == 'Short Leg':
            w = self.section_size_1.max_leg
            shear_lag = w
            L_c = (self.plate.length - max((2 * self.weld.size),15))
            A_go = self.section_size_1.max_leg * self.section_size_1.thickness
            A_nc = ((self.section_size_1.min_leg - self.section_size_1.thickness) * self.section_size_1.thickness)
            t = self.section_size_1.thickness

        elif design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
            w = self.section_size_1.flange_width
            shear_lag = w
            L_c = (self.plate.length - max((2 * self.weld.size),15))
            A_go = self.section_size_1.flange_width * self.section_size_1.flange_thickness*2
            A_nc = ((self.section_size_1.depth - 2*self.section_size_1.flange_thickness) * self.section_size_1.web_thickness)
            t = self.section_size_1.web_thickness

        self.section_size_1.tension_member_design_due_to_rupture_of_critical_section( A_nc = A_nc , A_go = A_go, F_u = self.section_size_1.fu, F_y = self.section_size_1.fy, L_c = L_c, w = w, b_s = shear_lag, t = t)

        if design_dictionary[KEY_SEC_PROFILE] in ["Back to Back Angles", "Star Angles", "Back to Back Channels"]:
            self.section_size_1.tension_rupture_capacity = 2 * self.section_size_1.tension_rupture_capacity
        elif design_dictionary[KEY_SEC_PROFILE] in ["Angles","Channels"]:
            self.section_size_1.tension_rupture_capacity = self.section_size_1.tension_rupture_capacity
        else:
            pass

        self.w = round((w), 2)
        self.A_go = round((A_go), 2)
        self.A_nc = round((A_nc), 2)
        self.t = round((t), 2)
        self.L_c = round((L_c), 2)
        self.b_s = round((shear_lag), 2)

        # self.section_size_1.tension_blockshear_area_input (A_vg = A_vg, A_vn = A_vn, A_tg = A_tg, A_tn = A_tn, f_u = self.section_size_1.fu, f_y = self.section_size_1.fy)

        self.section_size_1.design_check_for_slenderness(K = self.K, L = design_dictionary[KEY_LENGTH], r = self.min_radius_gyration)
        self.section_size_1.tension_capacity = min (self.section_size_1.tension_yielding_capacity, self.section_size_1.tension_rupture_capacity)

        self.member_recheck(self, design_dictionary)

    def member_recheck(self,design_dictionary):

        "Comparing applied force and tension capacity and if falsed, it return to initial member selection which selects member of higher area"

        # if self.section_size_1.slenderness < 400:
        #     self.design_status = True
        # else:
        #     self.design_status = False

        if self.section_size_1.tension_capacity >= self.load.axial_force * 1000:
            self.design_status = True

            self.efficiency = round((self.load.axial_force*1000 / self.section_size_1.tension_capacity), 2)
            self.get_plate_thickness(self,design_dictionary)

        else:
            print("recheck")
            # previous_size = self.section_size_1.designation
            # self.initial_member_capacity(self, design_dictionary, previous_size)
            if len(self.sizelist) >= 2:
                size = self.section_size_1.designation
                print("recheck", size)
                self.initial_member_capacity(self, design_dictionary, size)
            else:
                self.design_status = False
                logger.warning(":The factored tension force ({} kN) exceeds the tension capacity of {} kN with respect to the maximum available "
                               "member size {}.".format(
                        round(self.load.axial_force, 2), round(self.section_size_1.tension_rupture_capacity / 1000, 2), self.max_area))
                logger.info(":Select members with a higher cross sectional area.")
                logger.error(":Design is unsafe. \n ")
                logger.info(":=========End Of design===========")

    def get_plate_thickness(self,design_dictionary):

        "Calculate plate thickness based on the tension capacity from the available list of plate thickness"

        self.plate_last = self.plate.thickness[-1]

        # self.thickness_possible = [i for i in self.plate.thickness if i >= self.thick]
        # self.plate_thick_weld = self.thickness_possible[-1]

        for self.plate.thickness_provided in self.plate.thickness:
            self.plate.connect_to_database_to_get_fy_fu(grade=self.plate.material,
                                                        thickness=self.plate.thickness_provided)
            if design_dictionary[KEY_SEC_PROFILE] in ["Channels", 'Back to Back Channels']:
                self.plate.tension_yielding(length = (self.plate.height - max((4 * self.weld.size),30)), thickness = self.plate.thickness_provided, fy = self.plate.fy)
                self.net_area = (self.plate.height - max((4 * self.weld.size),30)) * self.plate.thickness_provided

            else:
                if design_dictionary[KEY_LOCATION] == 'Long Leg':
                    self.plate.tension_yielding(length = (self.plate.height - max((4 * self.weld.size),30)), thickness = self.plate.thickness_provided, fy = self.plate.fy)
                    self.net_area = (self.plate.height - max((4 * self.weld.size),30)) * self.plate.thickness_provided
                else:
                    self.plate.tension_yielding(length = (self.plate.height - max((4 * self.weld.size),30)), thickness = self.plate.thickness_provided, fy = self.plate.fy)
                    self.net_area = (self.plate.height - max((4 * self.weld.size),30)) * self.plate.thickness_provided

            self.plate.tension_rupture(A_n = self.net_area, F_u = self.plate.fu)


            A_vg = (self.plate.length - max((2 * self.weld.size),15)) * self.plate.thickness_provided
            A_vn = A_vg
            A_tg = (self.plate.height - max((2 * self.weld.size),15))* self.plate.thickness_provided
            A_tn = A_tg


            self.plate.tension_blockshear_area_input(A_vg = A_vg, A_vn = A_vn, A_tg = A_tg, A_tn = A_tn, f_u = self.plate.fu, f_y = self.plate.fy)
            self.plate_tension_capacity = min(self.plate.tension_yielding_capacity,self.plate.tension_rupture_capacity,self.plate.block_shear_capacity)
            print (self.plate.tension_yielding_capacity, self.plate.tension_rupture_capacity,self.plate.block_shear_capacity)

            if self.plate_tension_capacity > self.res_force:
                self.design_status = True

                break

            elif (self.plate_tension_capacity < self.res_force) and self.plate.thickness_provided == self.plate_last:
                self.design_status = False
                logger.warning(": The factored tension force ({} kN) exceeds the tension capacity of {} kN with respect to the maximum available "
                               "plate thickness of {} mm.".format(
                        round(self.res_force / 1000, 2),  round(self.max_tension_yield/1000,2),self.plate_last))
                logger.error(":Design is unsafe. \n ")
                logger.info(":=========End Of design===========")
            else:
                pass
        if self.plate_tension_capacity > self.res_force:
            if (2 * self.plate.length) > self.length:
                self.design_status = False
                logger.warning(":The plate length of {} mm is higher than the member length of {} mm".format(2 * self.plate.length, self.length))
                logger.info(":Try a larger diameter of bolt and/or increase the member length.")
                logger.error(":Design is unsafe. \n ")
                logger.info(":=========End Of design===========")
            else:
                self.plate_design_status = True
                self.design_status = True
                self.intermittent_bolt(self, design_dictionary)

                logger.info(":In the case of reverse loading, slenderness value shall be less than 180 [Ref. Table 3, IS 800:2007].")
                if self.sec_profile not in ["Angles", "Channels"] and self.length > 1000:
                    logger.info(":In the case of reverse loading for double sections, spacing of the intermittent connection shall be less than 600 "
                                "[Ref. Cl. 10.2.5.5, IS 800:2007].")
                else:
                    pass
                if self.load.axial_force < (self.res_force/1000):
                    logger.info(":The minimum design force based on the member size is used for performing the connection design, i.e. {} kN "
                                "[Ref. Cl. 10.7, IS 800:2007].".format(round(self.res_force / 1000, 2)))
                else:
                    pass
                logger.info(self.weld.reason)
                logger.info(":Overall welded tension member design is safe. \n")
                logger.info(" :=========End Of design===========")

                if design_dictionary[KEY_SEC_PROFILE] in ['Angles', 'Star Angles', 'Back to Back Angles']:
                    self.min_rad_gyration_calc(self, designation=self.section_size_1.designation,
                                               material_grade=self.material,
                                               key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.a,
                                               B_b=self.section_size_1.b, T_t=self.section_size_1.thickness)
                else:
                    self.min_rad_gyration_calc(self, designation=self.section_size_1.designation,
                                               material_grade=self.material,
                                               key=self.sec_profile, subkey=self.loc, D_a=self.section_size_1.depth,
                                               B_b=self.section_size_1.flange_width,
                                               T_t=self.section_size_1.flange_thickness,
                                               t=self.section_size_1.web_thickness)

                self.section_size_1.design_check_for_slenderness(K=self.K, L=design_dictionary[KEY_LENGTH],
                                                                 r=self.min_radius_gyration)

        else:
            self.design_status = False
            logger.error(": Design is not safe. \n ")
            logger.info(" :=========End Of design===========")

    def intermittent_bolt(self, design_dictionary):

        self.inter_length = self.length - 2* self.plate.length
        if design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Angles', 'Star Angles']:
            # print (Angle)
            self.inter_memb = Angle(designation=self.section_size_1.designation, material_grade=design_dictionary[KEY_SEC_MATERIAL])
            min_gyration = min(self.inter_memb.rad_of_gy_u, self.inter_memb.rad_of_gy_v)


        elif design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Channels']:
            self.inter_memb = Channel(designation=self.section_size_1.designation,
                                    material_grade=design_dictionary[KEY_SEC_MATERIAL])
            min_gyration = min(self.inter_memb.rad_of_gy_y, self.inter_memb.rad_of_gy_z)


        # print (self.inter_memb.min_radius_gyration,"hgvsdfsdff")
        if design_dictionary[KEY_SEC_PROFILE] in ['Back to Back Angles', 'Star Angles',
                                                  'Back to Back Channels'] and self.inter_length > 1000:
            self.inter_memb_length = 400 * min_gyration

            if self.inter_memb_length > 1000:
                ratio = round_up(self.inter_length / 1000, 1)
            else:
                ratio = round_up(self.inter_length / self.inter_memb_length, 1)
            self.inter_memb_length = self.inter_length / ratio
            self.inter_conn = ratio - 1
            self.inter_plate_length = max(50, 4*self.weld.size)
            if self.loc == "Long Leg":
                if self.sec_profile == "Star Angles":
                    self.inter_plate_height = 2 * self.section_size_1.max_leg + max(30, 4*self.weld.size)
                else:
                    self.inter_plate_height = self.section_size_1.max_leg + max(30, 4*self.weld.size)
            elif self.loc == "Short Leg":
                if self.sec_profile == "Star Angles":
                    self.inter_plate_height = 2 * self.section_size_1.max_leg + max(30, 4*self.weld.size)
                else:
                    self.inter_plate_height = self.section_size_1.max_leg + max(30, 4*self.weld.size)
            else:
                self.inter_plate_height = self.section_size_1.depth + max(30, 4*self.weld.size)
            self.inter_weld_size = self.weld.size
        else:
            self.inter_conn = 0.0
            self.inter_plate_length = 0.0
            self.inter_plate_height = 0.0
            self.inter_memb_length = 0.0
            self.inter_weld_size = 0.0


    def results_to_test(self, filename):
        test_out_list = {KEY_DISP_DESIGNATION:self.section_size_1.designation,
                         KEY_DISP_TENSION_YIELDCAPACITY:self.section_size_1.tension_yielding_capacity,
                         KEY_DISP_TENSION_RUPTURECAPACITY: self.section_size_1.tension_rupture_capacity,
                         KEY_DISP_TENSION_BLOCKSHEARCAPACITY:self.section_size_1.block_shear_capacity_axial,
                         KEY_DISP_SLENDER:self.section_size_1.slenderness,
                         KEY_DISP_EFFICIENCY:self.efficiency,
                         KEY_OUT_DISP_WELD_SIZE: self.weld.size,
                         KEY_OUT_DISP_WELD_STRENGTH: self.weld.strength,
                         KEY_OUT_DISP_WELD_STRESS: self.weld.stress,
                        KEY_OUT_DISP_PLATETHK:self.plate.thickness_provided,
                        KEY_OUT_DISP_PLATE_HEIGHT:self.plate.height,
                        KEY_OUT_DISP_PLATE_LENGTH:self.plate.length}
        f = open(filename, "w")
        f.write(str(test_out_list))
        f.close()

    def save_design(self, popup_summary):
        # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")
        if self.member_design_status == True:
            section_size = self.section_size_1

        else:
            if self.max_limit_status_2 == True:
                if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
                    section_size = Angle(designation=self.max_gyr, material_grade=self.material)
                else:
                    section_size = Channel(designation=self.max_gyr, material_grade=self.material)
            else:
                if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
                    section_size = Angle(designation=self.max_area, material_grade=self.material)
                else:
                    section_size = Channel(designation=self.max_area, material_grade=self.material)

        if self.sec_profile in ["Channels", "Back to Back Channels"]:
            if self.sec_profile == "Back to Back Channels":
                connecting_plates = [self.plate.thickness_provided, 2 * section_size.web_thickness]
                if section_size.flange_slope == 90:
                    image = "Parallel_BBChannel"
                else:
                    image = "Slope_BBChannel"
            else:
                connecting_plates = [self.plate.thickness_provided, section_size.web_thickness]
                if section_size.flange_slope == 90:
                    image = "Parallel_Channel"
                else:
                    image = "Slope_Channel"
            # min_gauge = self.pitch_round
            # row_limit = "Row Limit (rl) = 2"
            # row = 2
            # depth = 2 * self.edge_dist_min_round + self.pitch_round
        elif section_size.max_leg == section_size.min_leg:
            if self.sec_profile == "Back to Back Angles":
                connecting_plates = [self.plate.thickness_provided, 2 * section_size.thickness]
                if self.loc == "Long Leg":
                    image = "bblequaldp"
                else:
                    image = "bbsequaldp"
            elif self.sec_profile == "Star Angles":
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]
                if self.loc == "Long Leg":
                    image = "salequaldp"
                else:
                    image = "sasequaldp"
            else:
                image = "equaldp"
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]

            # min_gauge = 0.0
            # row_limit = "Row Limit (rl) = 1"
            # row = 1
            # # if self.loc == "Long Leg":
            # depth = 2 * self.edge_dist_min_round

        else:
            if self.sec_profile == "Back to Back Angles":
                connecting_plates = [self.plate.thickness_provided, 2 * section_size.thickness]
                if self.loc == "Long Leg":
                    image = "bblunequaldp"
                else:
                    image = "bbsunequaldp"
            elif self.sec_profile == "Star Angles":
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]
                if self.loc == "Long Leg":
                    image = "salunequaldp"
                else:
                    image = "sasunequaldp"
            else:
                image = "unequaldp"
                connecting_plates = [self.plate.thickness_provided, section_size.thickness]

            # min_gauge = 0.0
            # row_limit = "Row Limit (rl) = 1"
            # row = 1
            # # if self.loc == "Long Leg":
            # depth = 2 * self.edge_dist_min_round
            

        # if self.sec_profile in ["Channels", "Back to Back Channels"]:
        #     image = "Channel"
        # elif section_size.max_leg == section_size.min_leg:
        #     image = "Equal"
        # else:
        #     image = "Unequal"
        gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.weld.fabrication]

        if self.member_design_status == True:
            member_yield_kn = round((section_size.tension_yielding_capacity / 1000), 2)
            plate_yield_kn = round((self.plate.tension_yielding_capacity / 1000), 2)
            slenderness = section_size.slenderness
            gyration = self.min_radius_gyration
        else:
            if self.max_limit_status_2 == True:
                [member_yield_kn, l, slenderness, gyration] = self.max_force_length(self, self.max_gyr)
                member_yield_kn = round(member_yield_kn / 1000,2)
            else:
                [member_yield_kn, l, slenderness, gyration] = self.max_force_length(self, self.max_area)
                member_yield_kn = round(member_yield_kn / 1000,2)

        if self.sec_profile == "Channels":
            self.report_supporting = {KEY_DISP_SEC_PROFILE: image,
                                      # Image shall be save with this name.png in resource files
                                      KEY_DISP_SECSIZE: (section_size.designation,self.sec_profile),
                                      KEY_DISP_MATERIAL: section_size.material,
                                      KEY_REPORT_MASS: round(section_size.mass,2),
                                      KEY_REPORT_AREA: round(section_size.area,2),
                                      KEY_REPORT_DEPTH: round(section_size.depth,2),
                                      KEY_REPORT_WIDTH: round(section_size.flange_width,2),
                                      KEY_REPORT_WEB_THK: round(section_size.web_thickness,2),
                                      KEY_REPORT_FLANGE_THK: round(section_size.flange_thickness,2),
                                      KEY_DISP_FLANGE_S_REPORT: round(section_size.flange_slope,2),
                                      KEY_REPORT_R1: round(section_size.root_radius,2),
                                      KEY_REPORT_R2:round(section_size.toe_radius,2),
                                      KEY_REPORT_CY: round(section_size.Cy,2),
                                      KEY_REPORT_IZ: round(section_size.mom_inertia_z * 1e-4,2),
                                      KEY_REPORT_IY: round(section_size.mom_inertia_y * 1e-4,2),
                                      KEY_REPORT_RZ: round(section_size.rad_of_gy_z * 1e-1,2),
                                      KEY_REPORT_RY: round(section_size.rad_of_gy_y * 1e-1,2),
                                      KEY_REPORT_ZEZ: round(section_size.elast_sec_mod_z * 1e-3,2),
                                      KEY_REPORT_ZEY: round(section_size.elast_sec_mod_y * 1e-3,2),
                                      KEY_REPORT_ZPZ: round(section_size.plast_sec_mod_z * 1e-3,2),
                                      KEY_REPORT_ZPY: round(section_size.elast_sec_mod_y * 1e-3,2),
                                      KEY_REPORT_RADIUS_GYRATION: round(gyration,2)}

            thickness = section_size.web_thickness
            text = "C"
        elif self.sec_profile == "Back to Back Channels":
            BBChannel = BBChannel_Properties()
            BBChannel.data(section_size.designation, section_size.material)
            self.report_supporting = {KEY_DISP_SEC_PROFILE: image,
                                      # Image shall be save with this name.png in resource files
                                      KEY_DISP_SECSIZE: (section_size.designation, self.sec_profile),
                                      KEY_DISP_MATERIAL: section_size.material,
                                      KEY_REPORT_MASS: round(2*section_size.mass, 2),
                                      KEY_REPORT_AREA: round(2*section_size.area, 2),
                                      KEY_REPORT_DEPTH: round(section_size.depth, 2),
                                      KEY_REPORT_WIDTH: round(section_size.flange_width, 2),
                                      KEY_REPORT_WEB_THK: round(section_size.web_thickness, 2),
                                      KEY_REPORT_FLANGE_THK: round(section_size.flange_thickness, 2),
                                      '$T_p$ (mm)': round(self.plate.thickness_provided, 2),
                                      KEY_DISP_FLANGE_S_REPORT: round(section_size.flange_slope, 2),
                                      KEY_REPORT_R1: round(section_size.root_radius, 2),
                                      KEY_REPORT_R2: round(section_size.toe_radius, 2),
                                      KEY_REPORT_IZ: round((BBChannel.calc_MomentOfAreaZ(section_size.flange_width,section_size.flange_thickness,section_size.depth,section_size.web_thickness)*10000) * 1e-4,2),
                                      KEY_REPORT_IY: round((BBChannel.calc_MomentOfAreaY(section_size.flange_width,section_size.flange_thickness,section_size.depth,section_size.web_thickness)*10000) * 1e-4,2),
                                      KEY_REPORT_RZ: round((BBChannel.calc_RogZ(section_size.flange_width,section_size.flange_thickness,section_size.depth,section_size.web_thickness)*10) * 1e-1,2),
                                      KEY_REPORT_RY: round((BBChannel.calc_RogY(section_size.flange_width,section_size.flange_thickness,section_size.depth,section_size.web_thickness)*10) * 1e-1,2),
                                      KEY_REPORT_ZEZ: round((BBChannel.calc_ElasticModulusZz(section_size.flange_width,section_size.flange_thickness,section_size.depth,section_size.web_thickness)*1000) * 1e-3,2),
                                      KEY_REPORT_ZEY: round((BBChannel.calc_ElasticModulusZy(section_size.flange_width,section_size.flange_thickness,section_size.depth,section_size.web_thickness)*1000) * 1e-3,2),
                                      KEY_REPORT_ZPZ: round((BBChannel.calc_PlasticModulusZpz(section_size.flange_width,section_size.flange_thickness,section_size.depth,section_size.web_thickness)*1000) * 1e-3,2),
                                      KEY_REPORT_ZPY: round((BBChannel.calc_PlasticModulusZpy(section_size.flange_width,section_size.flange_thickness,section_size.depth,section_size.web_thickness)*1000) * 1e-3,2),
                                      KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)}
            thickness = section_size.web_thickness
            text = "C"

        elif self.sec_profile == "Angles":
            self.report_supporting = {KEY_DISP_SEC_PROFILE: image,
                                      # Image shall be save with this name.png in resource files
                                      KEY_DISP_SECSIZE: (section_size.designation,self.sec_profile),
                                      KEY_DISP_MATERIAL: section_size.material,
                                      KEY_REPORT_MASS: round(section_size.mass,2),
                                      KEY_REPORT_AREA: round((section_size.area),2),
                                      KEY_REPORT_MAX_LEG_SIZE: round(section_size.max_leg,2),
                                      KEY_REPORT_MIN_LEG_SIZE: round(section_size.min_leg,2),
                                      KEY_REPORT_ANGLE_THK: round(section_size.thickness,2),
                                      KEY_REPORT_R1: round(section_size.root_radius,2),
                                      KEY_REPORT_R2: round(section_size.toe_radius,2),
                                      KEY_REPORT_CY: round(section_size.Cy,2),
                                      KEY_REPORT_CZ: round(section_size.Cz,2),
                                      KEY_REPORT_IZ: round(section_size.mom_inertia_z * 1e-4,2),
                                      KEY_REPORT_IY: round(section_size.mom_inertia_y * 1e-4,2),
                                      KEY_REPORT_IU: round(section_size.mom_inertia_u * 1e-4,2),
                                      KEY_REPORT_IV: round(section_size.mom_inertia_v * 1e-4,2),
                                      KEY_REPORT_RZ: round(section_size.rad_of_gy_z * 1e-1,2),
                                      KEY_REPORT_RY: round((section_size.rad_of_gy_y) * 1e-1,2),
                                      KEY_REPORT_RU: round((section_size.rad_of_gy_u) * 1e-1,2),
                                      KEY_REPORT_RV: round((section_size.rad_of_gy_v) * 1e-1,2),
                                      KEY_REPORT_ZEZ: round(section_size.elast_sec_mod_z * 1e-3,2),
                                      KEY_REPORT_ZEY: round(section_size.elast_sec_mod_y * 1e-3,2),
                                      KEY_REPORT_ZPZ: round(section_size.plast_sec_mod_z * 1e-3,2),
                                      KEY_REPORT_ZPY: round(section_size.plast_sec_mod_y * 1e-3,2),
                                      KEY_REPORT_RADIUS_GYRATION: round(gyration,2)}
            thickness = section_size.thickness
            text = "A"

        elif self.sec_profile == "Back to Back Angles":
            Angle_attributes = BBAngle_Properties()
            Angle_attributes.data(section_size.designation, section_size.material)
            if self.loc == "Long Leg":
                Cz = round((Angle_attributes.calc_Cz(section_size.max_leg, section_size.min_leg, section_size.thickness,
                                                     self.loc) * 10), 2)
                Cy = "N/A"
            else:
                Cz = round((Angle_attributes.calc_Cy(section_size.max_leg, section_size.min_leg, section_size.thickness,
                                                     self.loc) * 10), 2)
                Cy = "N/A"

            self.report_supporting = {KEY_DISP_SEC_PROFILE: image,
                                      # Image shall be save with this name.png in resource files
                                      KEY_DISP_SECSIZE: (section_size.designation,self.sec_profile),
                                      KEY_DISP_MATERIAL: section_size.material,
                                      KEY_REPORT_MASS: round(2*section_size.mass,2),
                                      KEY_REPORT_AREA: round((2*section_size.area),2),
                                      KEY_REPORT_MAX_LEG_SIZE: round(section_size.max_leg,2),
                                      KEY_REPORT_MIN_LEG_SIZE: round(section_size.min_leg,2),
                                      KEY_REPORT_ANGLE_THK: round(section_size.thickness,2),
                                      '$T$ (mm)': round(self.plate.thickness_provided, 2),
                                      KEY_REPORT_R1: round(section_size.root_radius,2),
                                      KEY_REPORT_R2: round(section_size.toe_radius,2),
                                      KEY_REPORT_CY: Cy,
                                      KEY_REPORT_CZ: Cz,
                                      KEY_REPORT_IZ: round((Angle_attributes.calc_MomentOfAreaZ(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)*10000) * 1e-4,2),
                                      KEY_REPORT_IY: round((Angle_attributes.calc_MomentOfAreaY(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)*10000) * 1e-4,2),
                                      KEY_REPORT_IU: round((Angle_attributes.calc_MomentOfAreaY(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)*10000) * 1e-4,2),
                                      KEY_REPORT_IV: round((Angle_attributes.calc_MomentOfAreaZ(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)*10000) * 1e-4,2),
                                      KEY_REPORT_RZ: round((Angle_attributes.calc_RogZ(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)),2),
                                      KEY_REPORT_RY: round((Angle_attributes.calc_RogY(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)),2),
                                      KEY_REPORT_RU: round((Angle_attributes.calc_RogY(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)), 2),
                                      KEY_REPORT_RV: round((Angle_attributes.calc_RogZ(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)), 2),
                                      KEY_REPORT_ZEZ: round((Angle_attributes.calc_ElasticModulusZz(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)),2),
                                      KEY_REPORT_ZEY: round((Angle_attributes.calc_ElasticModulusZy(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)),2),
                                      KEY_REPORT_ZPZ: round((Angle_attributes.calc_PlasticModulusZpz(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)),2),
                                      KEY_REPORT_ZPY: round((Angle_attributes.calc_PlasticModulusZpy(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)),2),
                                      KEY_REPORT_RADIUS_GYRATION: round(gyration,2)}
            thickness = section_size.thickness
            text = "A"
        else:
            Angle_attributes = SAngle_Properties()
            Angle_attributes.data(section_size.designation, section_size.material)

            self.report_supporting = {KEY_DISP_SEC_PROFILE: image,
                                      # Image shall be save with this name.png in resource files
                                      KEY_DISP_SECSIZE: (section_size.designation, self.sec_profile),
                                      KEY_DISP_MATERIAL: section_size.material,
                                      KEY_REPORT_MASS: round(2*section_size.mass, 2),
                                      KEY_REPORT_AREA: round((2*section_size.area), 2),
                                      KEY_REPORT_MAX_LEG_SIZE: round(section_size.max_leg, 2),
                                      KEY_REPORT_MIN_LEG_SIZE: round(section_size.min_leg, 2),
                                      KEY_REPORT_ANGLE_THK: round(section_size.thickness, 2),
                                      '$T$ (mm)': round(self.plate.thickness_provided, 2),
                                      KEY_REPORT_R1: round(section_size.root_radius, 2),
                                      KEY_REPORT_R2: round(section_size.toe_radius, 2),
                                      KEY_REPORT_IZ: round((Angle_attributes.calc_MomentOfAreaZ(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)), 2),
                                      KEY_REPORT_IY: round((Angle_attributes.calc_MomentOfAreaY(section_size.max_leg, section_size.min_leg,section_size.thickness,self.loc)), 2),
                                      KEY_REPORT_IU: round((Angle_attributes.calc_MomentOfAreaU(section_size.max_leg,section_size.min_leg,section_size.thickness,self.loc)), 2),
                                      KEY_REPORT_IV: round((Angle_attributes.calc_MomentOfAreaV(section_size.max_leg,section_size.min_leg,section_size.thickness, self.loc)), 2),
                                      KEY_REPORT_RZ: round((Angle_attributes.calc_RogZ(section_size.max_leg, section_size.min_leg, section_size.thickness,self.loc)), 2),
                                      KEY_REPORT_RY: round((Angle_attributes.calc_RogY(section_size.max_leg, section_size.min_leg, section_size.thickness,self.loc)), 2),
                                      KEY_REPORT_RU: round((Angle_attributes.calc_RogU(section_size.max_leg,section_size.min_leg, section_size.thickness, self.loc)), 2),
                                      KEY_REPORT_RV: round((Angle_attributes.calc_RogV(section_size.max_leg,section_size.min_leg,section_size.thickness, self.loc)), 2),
                                      KEY_REPORT_ZEZ: round((Angle_attributes.calc_ElasticModulusZz(section_size.max_leg, section_size.min_leg, section_size.thickness,  self.loc)), 2),
                                      KEY_REPORT_ZEY: round((Angle_attributes.calc_ElasticModulusZy(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc)), 2),
                                      KEY_REPORT_ZPZ: round((Angle_attributes.calc_PlasticModulusZpz(section_size.max_leg, section_size.min_leg, section_size.thickness, self.loc)), 2),
                                      KEY_REPORT_ZPY: round((Angle_attributes.calc_PlasticModulusZpy(section_size.max_leg, section_size.min_leg, section_size.thickness,self.loc)), 2),
                                      KEY_REPORT_RADIUS_GYRATION: round(gyration, 2)}
            thickness = section_size.thickness
            text = "A"

        self.report_input = \
            {KEY_MODULE: self.module,
             KEY_DISP_AXIAL: self.load.axial_force,
             KEY_DISP_LENGTH: self.length,
             # "Section": "TITLE",
             "Selected Section Details": self.report_supporting,
             # "Supported Section Details": "TITLE",
             # "Beam Details": r'/ResourceFiles/images/ColumnsBeams".png',
             KEY_DISP_SEC_PROFILE: self.sec_profile,
             KEY_DISP_SECSIZE: str(self.sizelist),

             "Plate Details - Input and Design Preference": "TITLE",
             KEY_DISP_PLATETHK: str(list(np.int_(self.plate.thickness))),
             KEY_DISP_MATERIAL: self.plate.material,
             KEY_DISP_ULTIMATE_STRENGTH_REPORT: round(self.plate.fu, 2),
             KEY_DISP_YIELD_STRENGTH_REPORT: round(self.plate.fy, 2),

             "Weld Details - Input and Design Preference": "TITLE",
             KEY_DISP_DP_WELD_TYPE: "Fillet",
             KEY_DISP_DP_WELD_FAB: self.weld.fabrication,
             KEY_DISP_DP_WELD_MATERIAL_G_O_REPORT: self.weld.fu,

             # "Safety Factors - IS 800:2007 Table 5 (Clause 5.4.1) ": "TITLE",
             # KEY_DISP_GAMMA_M0: cl_5_4_1_table_4_5_gamma_value(1.1, "m0"),
             # KEY_DISP_GAMMA_M1: cl_5_4_1_table_4_5_gamma_value(1.25, "m1"),
             # KEY_DISP_GAMMA_MW: cl_5_4_1_table_4_5_gamma_value(gamma_mw, "mw")
             }

        self.report_check = []
        # connecting_plates = [self.plate.thickness_provided, self.section_size_1.web_thickness]
        self.load.shear_force = 0.0
        # if self.member_design_status == True:
        #     member_yield_kn = round((section_size.tension_yielding_capacity / 1000), 2)
        # else:
        #     member_yield_kn = round((self.max_member_force / 1000), 2)

        if self.member_design_status == True and self.weld_design_status == True and self.thick_design_status == True:
            member_rupture_kn = round((section_size.tension_rupture_capacity / 1000), 2)
            # member_blockshear_kn = round((section_size.block_shear_capacity_axial / 1000), 2)
            plate_rupture_kn = round((self.plate.tension_rupture_capacity / 1000), 2)
            plate_blockshear_kn = round((self.plate.block_shear_capacity / 1000), 2)
        else:
            pass

        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        if self.sec_profile in ["Back to Back Angles", "Star Angles", "Back to Back Channels"]:
            multiple = 2
        else:
            multiple = 1


        # if self.plate.length > (150 * self.weld.throat) and self.sec_profile in ["Channels", 'Back to Back Channels']:
        #     self.weld_connecting_plates = [self.plate.thickness_provided,self.thick_1]
        # else:
        if self.member_design_status == True and self.thick_design_status == True:
            if self.web_weld_status == False:
                self.thick = self.thick_1


            self.weld_connecting_plates = [self.plate.thickness_provided, self.thick]

            weld_thickness = round_down((min(self.weld_connecting_plates) - self.weld.red), 1, 3)
            if weld_thickness < self.weld.min_weld:
                weld_thickness = int(min(self.weld_connecting_plates))
            else:
                pass

        t1 = ('Selected', 'Selected Member Data', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
        self.report_check.append(t1)

        if self.member_design_status == True and self.weld_design_status == True and self.thick_design_status == True:
            t1 = ('SubSection', 'Member Check', '|p{2.5cm}|p{4.5cm}|p{7.5cm}|p{1cm}|')
            self.report_check.append(t1)

            t2 = (KEY_DISP_TENSION_YIELDCAPACITY, '',
                  cl_6_2_tension_yield_capacity_member(l=None, t=None,f_y=section_size.fy,gamma=gamma_m0,
                                                       T_dg=member_yield_kn ,area=section_size.area), '')
            self.report_check.append(t2)
            t3 = (KEY_DISP_TENSION_RUPTURECAPACITY, '',
                  cl_6_3_3_tension_rupture_member(self.A_nc, self.A_go, section_size.fu, section_size.fy, self.L_c, self.w,
                                                  self.b_s, self.t, gamma_m0, gamma_m1, section_size.beta, member_rupture_kn,
                                                  multiple), '')
            self.report_check.append(t3)
            # t4 = (KEY_DISP_TENSION_BLOCKSHEARCAPACITY, '', blockshear_prov(Tdb=member_blockshear_kn), '')
            # self.report_check.append(t4)
            t8 = (KEY_DISP_TENSION_CAPACITY, self.load.axial_force, cl_6_1_tension_capacity_member(member_yield_kn, member_rupture_kn),
                  get_pass_fail(self.load.axial_force, self.section_size_1.tension_capacity, relation="lesser"))
            self.report_check.append(t8)
            t5 = (KEY_DISP_SLENDER, slenderness_req(), cl_7_1_2_effective_slenderness_ratio(1, self.length, round(gyration, 2), slenderness),
                  get_pass_fail(400, slenderness, relation="greater"))
            self.report_check.append(t5)
            t6 = (KEY_DISP_EFFICIENCY, required_IR_or_utilisation_ratio(1),
                  efficiency_prov(self.load.axial_force, section_size.tension_capacity, self.efficiency), '')
            self.report_check.append(t6)
            t1 = (KEY_DISP_AXIAL_FORCE_CON,
                  axial_capacity_req(axial_capacity=round((section_size.tension_yielding_capacity / 1000), 2),
                                     min_ac=round(((0.3 * section_size.tension_yielding_capacity) / 1000), 2)),
                  display_prov(round((self.res_force / 1000), 2), "A"),
                  min_prov_max(round(((0.3 * section_size.tension_yielding_capacity) / 1000), 2),
                               round(self.res_force / 1000, 2),
                               round((section_size.tension_yielding_capacity / 1000), 2)))
            self.report_check.append(t1)
        else:
            t1 = ('SubSection', 'Member Check', '|p{2.5cm}|p{4.5cm}|p{7.5cm}|p{1cm}|')
            self.report_check.append(t1)
            t2 = (KEY_DISP_TENSION_YIELDCAPACITY, self.load.axial_force,
                  cl_6_2_tension_yield_capacity_member(l=None, t=None, f_y=section_size.fy, gamma=gamma_m0,
                                                       T_dg=member_yield_kn , area=section_size.area),
                  get_pass_fail(self.load.axial_force, member_yield_kn, relation="lesser"))
            self.report_check.append(t2)

            t5 = (KEY_DISP_SLENDER, slenderness_req(),
                  cl_7_1_2_effective_slenderness_ratio(1, self.length, round(gyration, 2),
                                                       slenderness), get_pass_fail(400, slenderness, relation="greater"))
            self.report_check.append(t5)

        # if self.member_design_status == True:
        #
        #     # t7 = ('SubSection', 'Thickness Checks', '|p{2.5cm}|p{5cm}|p{7.5cm}|p{1cm}|')
        #     # self.report_check.append(t7)
        #
        #     if self.sec_profile in ["Channels", 'Back to Back Channels']:
        #         t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force/1000,2),tension_yield_prov(l = self.section_size.depth ,t = self.plate.thickness_provided, f_y =self.plate.fy, gamma = gamma_m0, T_dg = plate_yield_kn), get_pass_fail(round((self.res_force/1000),2), plate_yield_kn, relation="lesser"))
        #
        #     elif self.sec_profile in ["Angles", 'Back to Back Angles']:
        #         if self.loc == "Long Leg":
        #             t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force/1000,2),tension_yield_prov(l=self.section_size.max_leg, t=self.plate.thickness_provided, f_y=self.plate.fy,
        #                                      gamma=gamma_m0, T_dg =plate_yield_kn), get_pass_fail(round((self.res_force/1000),2), plate_yield_kn, relation="lesser"))
        #         else:
        #             t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force/1000,2),tension_yield_prov(l=self.section_size.min_leg, t=self.plate.thickness_provided,
        #                                      f_y=self.plate.fy,
        #                                      gamma=gamma_m0, T_dg=plate_yield_kn), get_pass_fail(round((self.res_force/1000),2), plate_yield_kn, relation="lesser"))
        #     else:
        #         if self.loc == "Long Leg":
        #             t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force/1000,2), tension_yield_prov(l=2*self.section_size.max_leg, t=self.plate.thickness_provided, f_y=self.plate.fy,
        #                                      gamma=gamma_m0, T_dg=plate_yield_kn), get_pass_fail(round((self.res_force/1000),2), plate_yield_kn, relation="lesser"))
        #
        #
        #         else:
        #             t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force/1000,2),tension_yield_prov(l=2*self.section_size.min_leg, t=self.plate.thickness_provided,
        #                                      f_y=self.plate.fy,gamma=gamma_m0, T_dg=plate_yield_kn), get_pass_fail(round((self.res_force/1000),2), plate_yield_kn, relation="lesser"))
        #
        #     self.report_check.append(t2)


        if self.thick_design_status == True:

            t7 = ('SubSection', 'Weld Design', '|p{3cm}|p{6.5 cm}|p{5cm}|p{1cm}|')
            self.report_check.append(t7)
            #TODO
            if self.weld.size == min(self.weld_connecting_plates):
                t1 = (DISP_MIN_WELD_SIZE, cl_10_5_2_3_min_fillet_weld_size_required(self.weld_connecting_plates, self.weld.min_weld ,self.weld.red), self.weld.size,
                      min_prov_max(min(self.weld_connecting_plates), self.weld.size, self.weld.min_weld))
            else:
                t1 = (DISP_MIN_WELD_SIZE,cl_10_5_2_3_min_fillet_weld_size_required(self.weld_connecting_plates, self.weld.min_weld,
                                                                self.weld.red), self.weld.size,
                      min_prov_max(min(self.weld_connecting_plates) - self.weld.red, self.weld.size,
                                   self.weld.min_weld))

            self.report_check.append(t1)

            self.weld_size_max = 16.0
            t1 = (DISP_MAX_WELD_SIZE, cl_10_5_3_1_max_weld_size(self.weld_connecting_plates, self.weld_size_max), self.weld.size,
                  get_pass_fail(self.weld_size_max, self.weld.size, relation="geq"))
            self.report_check.append(t1)

            t1 = (DISP_THROAT, cl_10_5_3_1_throat_thickness_req(), cl_10_5_3_1_throat_thickness_weld(self.weld.size, self.Kt),
                  get_pass_fail(3.0, self.weld.size, relation="leq"))
            self.report_check.append(t1)

            t1 = (DISP_EFF, "", display_prov(self.weld.length,"l_w"), "")
            self.report_check.append(t1)

            Ip_weld = 0.0
            weld_conn_plates_fu = [self.section_size.fu, self.plate.fu]

            # t1 = (DISP_WELD_STRENGTH, weld_strength_req(V=0.0, A=self.res_force,
            #                                             M=0.0, Ip_w=0.0,
            #                                             y_max=0.0, x_max=0.0,
            #                                             l_w=self.weld.length,
            #                                             R_w=self.weld.stress),
            #       weld_strength_prov(weld_conn_plates_fu, gamma_mw, self.weld.throat_tk, self.weld.strength),
            #       get_pass_fail(self.weld.stress, self.weld.strength, relation="lesser"))
            t1 = (DISP_WELD_STRENGTH, weld_strength_req(V=0.0, A=self.res_force,
                                                        M=0.0, Ip_w=1.0,
                                                        y_max=0.0, x_max=0.0,
                                                        l_w=self.weld.length,
                                                       R_w=self.weld.stress),
                  cl_10_5_7_1_1_weld_strength(weld_conn_plates_fu, gamma_mw, round((self.weld.throat), 2), round((self.weld.strength), 2)),
                  get_pass_fail(self.weld.stress, self.weld.strength, relation="lesser"))
            self.report_check.append(t1)

            t15 = (KEY_OUT_LONG_JOINT_WELD, long_joint_welded_req(),
                   cl_10_5_7_3_weld_strength_post_long_joint(h=self.plate.height, l=self.plate.length, t_t=self.weld.throat,
                                                             ws= self.weld.strength, wsr = self.weld.strength_red), "")
            self.report_check.append(t15)
            t5 = (KEY_OUT_DISP_RED_WELD_STRENGTH, self.weld.stress, self.weld.strength_red,
                get_pass_fail(self.weld.stress, self.weld.strength_red,
                              relation="lesser"))
            self.report_check.append(t5)

        if self.member_design_status == True:

            t7 = ('SubSection', 'Gusset Plate Check', '|p{2.5cm}|p{5cm}|p{7.5cm}|p{1cm}|')
            self.report_check.append(t7)

            if self.sec_profile in ["Channels", 'Back to Back Channels']:
                t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force / 1000, 2),
                      cl_6_2_tension_yield_capacity_member(l=self.section_size.depth, t=self.plate.thickness_provided, f_y=self.plate.fy,
                                                           gamma=gamma_m0, T_dg=plate_yield_kn),
                      get_pass_fail(round((self.res_force / 1000), 2), plate_yield_kn, relation="lesser"))

            elif self.sec_profile in ["Angles", 'Back to Back Angles']:
                if self.loc == "Long Leg":
                    t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force / 1000, 2),
                          cl_6_2_tension_yield_capacity_member(l=self.section_size.max_leg, t=self.plate.thickness_provided,
                                                               f_y=self.plate.fy,
                                                               gamma=gamma_m0, T_dg=plate_yield_kn),
                          get_pass_fail(round((self.res_force / 1000), 2), plate_yield_kn, relation="lesser"))
                else:
                    t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force / 1000, 2),
                          cl_6_2_tension_yield_capacity_member(l=self.section_size.min_leg, t=self.plate.thickness_provided,
                                                               f_y=self.plate.fy,
                                                               gamma=gamma_m0, T_dg=plate_yield_kn),
                          get_pass_fail(round((self.res_force / 1000), 2), plate_yield_kn, relation="lesser"))
            else:
                if self.loc == "Long Leg":
                    t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force / 1000, 2),
                          cl_6_2_tension_yield_capacity_member(l=2 * self.section_size.max_leg, t=self.plate.thickness_provided,
                                                               f_y=self.plate.fy,
                                                               gamma=gamma_m0, T_dg=plate_yield_kn),
                          get_pass_fail(round((self.res_force / 1000), 2), plate_yield_kn, relation="lesser"))


                else:
                    t2 = (KEY_DISP_TENSION_YIELDCAPACITY, round(self.res_force / 1000, 2),
                          cl_6_2_tension_yield_capacity_member(l=2 * self.section_size.min_leg, t=self.plate.thickness_provided,
                                                               f_y=self.plate.fy, gamma=gamma_m0, T_dg=plate_yield_kn),
                          get_pass_fail(round((self.res_force / 1000), 2), plate_yield_kn, relation="lesser"))

            self.report_check.append(t2)

            if self.weld_design_status == True:

                self.clearance =  max((4 * self.weld.size),30)
                if self.sec_profile in ["Channels", 'Back to Back Channels']:
                    t3 = (KEY_OUT_DISP_PLATE_MIN_HEIGHT,'',gusset_ht_prov(self.section_size.depth, self.clearance,self.plate.height,1),"")
                    # t2 = (KEY_DISP_TENSION_YIELDCAPACITY, '',
                    #       tension_yield_prov(l = self.section_size.depth ,t = self.plate.thickness_provided, f_y =self.plate.fy, gamma = gamma_m0, T_dg = plate_yield_kn), '')
                    # t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '', tension_rupture_welded_prov(self.section_size.depth, self.plate.thickness_provided,self.plate.fu, gamma_m1,plate_rupture_kn), '')

                elif self.sec_profile in ["Angles", 'Back to Back Angles']:
                    if self.loc == "Long Leg":
                        t3 = (KEY_OUT_DISP_PLATE_MIN_HEIGHT, '',
                              gusset_ht_prov(self.section_size.max_leg, self.clearance, self.plate.height, 1), "")
                        # t2 = (KEY_DISP_TENSION_YIELDCAPACITY, '',
                        #       tension_yield_prov(l=self.section_size.max_leg, t=self.plate.thickness_provided, f_y=self.plate.fy,
                        #                          gamma=gamma_m0, T_dg =plate_yield_kn), '')
                        # t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '',
                        #       tension_rupture_welded_prov(self.section_size.max_leg, self.plate.thickness_provided,
                        #                                   self.plate.fu, gamma_m1, plate_rupture_kn), '')

                    else:
                        t3 = (KEY_OUT_DISP_PLATE_MIN_HEIGHT,'',gusset_ht_prov(self.section_size.min_leg, self.clearance,self.plate.height,1),"")
                        # t2 = (KEY_DISP_TENSION_YIELDCAPACITY, '',
                        #       tension_yield_prov(l=self.section_size.min_leg, t=self.plate.thickness_provided,
                        #                          f_y=self.plate.fy,
                        #                          gamma=gamma_m0, T_dg=plate_yield_kn), '')
                        # t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '',
                        #       tension_rupture_welded_prov(self.section_size.min_leg, self.plate.thickness_provided,
                        #                                   self.plate.fu, gamma_m1, plate_rupture_kn), '')

                else:
                    if self.loc == "Long Leg":
                        t3 = (KEY_OUT_DISP_PLATE_MIN_HEIGHT,'',gusset_ht_prov(2*self.section_size.max_leg, self.clearance,self.plate.height,1),"")
                        # t2 = (KEY_DISP_TENSION_YIELDCAPACITY, '',
                        #       tension_yield_prov(l=2*self.section_size.max_leg, t=self.plate.thickness_provided, f_y=self.plate.fy,
                        #                          gamma=gamma_m0, T_dg=plate_yield_kn), '')
                        # t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '',
                        #       tension_rupture_welded_prov(2*self.section_size.max_leg, self.plate.thickness_provided,
                        #                                   self.plate.fu, gamma_m1, plate_rupture_kn), '')

                    else:
                        t3 = (KEY_OUT_DISP_PLATE_MIN_HEIGHT, '',
                              gusset_ht_prov(2*self.section_size.min_leg, self.clearance, self.plate.height, 1), "")
                        # t2 = (KEY_DISP_TENSION_YIELDCAPACITY, '',
                        #       tension_yield_prov(l=2*self.section_size.min_leg, t=self.plate.thickness_provided,
                        #                          f_y=self.plate.fy,
                        #                          gamma=gamma_m0, T_dg=plate_yield_kn), '')
                        # t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '',
                        #       tension_rupture_welded_prov(2*self.section_size.min_leg, self.plate.thickness_provided,
                        #                                   self.plate.fu, gamma_m1, plate_rupture_kn), '')

                self.report_check.append(t3)
                t4 = (KEY_OUT_DISP_PLATE_MIN_LENGTH,  '',
                      gusset_lt_w_prov(self.flange_weld, self.clearance,self.plate.length), get_pass_fail(self.length, self.plate.length, relation="greater"))
                self.report_check.append(t4)

                t4 = (KEY_OUT_DISP_MEMB_MIN_LENGTH, (2 * self.plate.length), self.length,
                      get_pass_fail((2 * self.plate.length), self.length, relation="leq"))
                self.report_check.append(t4)

                if self.sec_profile in ["Channels", "Back to Back Channels"]:
                    t5 = (KEY_OUT_DISP_PLATETHK_REP, '', display_prov(self.plate.thickness_provided, "T_p"), "")
                    self.report_check.append(t5)
                else:
                    t5 = (KEY_OUT_DISP_PLATETHK_REP, '', display_prov(self.plate.thickness_provided, "T"), "")
                    self.report_check.append(t5)

                # self.report_check.append(t2)
                self.report_check.append(t1)

                t4 = (KEY_DISP_TENSION_BLOCKSHEARCAPACITY, '', cl_6_4_blockshear_capacity_member(Tdb=plate_blockshear_kn), '')
                self.report_check.append(t4)

                t8 = (
                    KEY_DISP_TENSION_CAPACITY, display_prov(round((self.res_force/1000),2),"A"), cl_6_1_tension_capacity_member(plate_yield_kn,0, plate_blockshear_kn),
                    get_pass_fail(round((self.res_force/1000),2), self.plate_tension_capacity, relation="lesser"))
                self.report_check.append(t8)
            else:
                pass

        if self.plate_design_status == True and self.sec_profile not in ["Angles", "Channels"] and self.inter_length>1000:
            t7 = ('SubSection', 'Intermittent Connection', '|p{2.5cm}|p{5cm}|p{7.5cm}|p{1cm}|')
            self.report_check.append(t7)

            t5 = (KEY_OUT_DISP_INTERCONNECTION, " ", self.inter_conn, "")
            self.report_check.append(t5)

            t5 = (KEY_OUT_DISP_INTERSPACING, 1000, round(self.inter_memb_length, 2),
                  get_pass_fail(1000, self.inter_memb_length, relation="geq"))
            self.report_check.append(t5)

            t3 = (KEY_OUT_DISP_PLATE_MIN_HEIGHT, '', int(self.inter_plate_height), "")
            self.report_check.append(t3)

            t4 = (KEY_OUT_DISP_PLATE_MIN_LENGTH, "", int(self.inter_plate_length), "")
            self.report_check.append(t4)

        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"


        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")

        fname_no_ext = popup_summary['filename']


        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_2d_image, Disp_3D_image, module=self.module)


