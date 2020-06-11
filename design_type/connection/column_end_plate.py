from design_type.connection.moment_connection import MomentConnection
from design_report.reportGenerator_latex import CreateLatex

from utils.common.component import *
from utils.common.material import *
from Common import *
from Common import *
from Report_functions import *

import logging
from utils.common.load import Load


class ColumnEndPlate(MomentConnection):

    def __init__(self):
        super(ColumnEndPlate, self).__init__()
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

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_section)
        tabs.append(t1)

        t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        tabs.append(t6)

        t2 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t2)

        t2 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t2)

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

        t2 = (
        KEY_DISP_COLSEC, [KEY_SEC_MATERIAL], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX, self.get_fu_fy_I_section)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t3)

        t5 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20','Label_21','Label_22'], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
                Not required for this module but empty list should be passed"""
        return []

    # def list_for_fu_fy_validation(self):
    #     """ This function is no longer required"""
    #     fu_fy_list = []
    #
    #     t2 = (KEY_SEC_MATERIAL, KEY_SEC_FU, KEY_SEC_FY)
    #     fu_fy_list.append(t2)
    #
    #     t3 = (KEY_CONNECTOR_MATERIAL, KEY_CONNECTOR_FU, KEY_CONNECTOR_FY)
    #     fu_fy_list.append(t3)
    #
    #     return fu_fy_list

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        t2 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        # t2 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY])
        # design_input.append(t2)

        t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        design_input.append(t3)

        t3 = ("Bolt", TYPE_TEXTBOX, [KEY_DP_BOLT_MATERIAL_G_O])
        design_input.append(t3)

        t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        design_input.append(t4)

        t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        design_input.append(t4)

        t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        design_input.append(t5)

        t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to
        design dictionary if design preference is never opened by user. It sets are design preference values to default.
        If any design preference value needs to be set to input dock value, tuple shall be written as:

        (Key of input dock, [List of Keys from design preference], 'Input Dock')

        If the values needs to be set to default,

        (None, [List of Design Preference Keys], '')

         """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_MATERIAL_G_O, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_GAP,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
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

        return add_buttons

    ####################################
    # Design Preference Functions End
    ####################################

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """
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
        return KEY_DISP_COLUMNENDPLATE

    def input_values(self):
        """"
        Function to set input values
        """
        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_COLUMNENDPLATE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, connectdb("Columns"), True, 'No Validator')
        options_list.append(t4)

        t8 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, VALUES_CONN_3, True, 'No Validator')
        options_list.append(t8)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, True, 'No Validator')
        options_list.append(t15)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t21 = (None, DISP_TITLE_ENDPLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t21)

        t22 = (KEY_PLATETHK, KEY_DISP_ENDPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_ENDPLATE_THICKNESS, True, 'No Validator')
        options_list.append(t22)

        # t13 = (KEY_CONN_PREFERENCE, KEY_DISP_CONN_PREFERENCE, TYPE_COMBOBOX, existingvalue_design_pref, VALUES_CONN_PREFERENCE)
        # options_list.append(t13)

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


    def detailing(self, flag):
        detailing = []

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.pitch if flag else '')
        detailing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.end_dist if flag else '')
        detailing.append(t10)

        t8 = (KEY_OUT_NO_BOLTS_WEB, KEY_OUT_DISP_NO_BOLTS_WEB, TYPE_TEXTBOX, self.n_bw * 2 if flag else '')
        detailing.append(t8)

        t9 = (KEY_OUT_NO_BOLTS_FLANGE, KEY_OUT_DISP_NO_BOLTS_FLANGE, TYPE_TEXTBOX,self.n_bf + 4 if flag else '')
        detailing.append(t9)

        t10 = (KEY_OUT_NO_BOLTS, KEY_OUT_DISP_NO_BOLTS, TYPE_TEXTBOX, self.no_bolts if flag else '')
        detailing.append(t10)

        return detailing

    def stiffener_details(self, flag):
        stiff_details = []

        if 2*self.end_dist < 50 and self.h_s < 100:
            pass
        elif 2*self.end_dist >= 50 and self.h_s >= 100:
            t1 = (KEY_OUT_STIFFENER_HEIGHT,KEY_OUT_DISP_STIFFENER_HEIGHT,TYPE_TEXTBOX,self.t_s if flag else '', True)
            stiff_details.append(t1)
            t2 = (KEY_OUT_STIFFENER_WIDTH,KEY_OUT_DISP_STIFFENER_WIDTH,TYPE_TEXTBOX,self.stiff_wt if flag else '', True)
            stiff_details.append(t2)
            t3 = (KEY_OUT_STIFFENER_THICKNESS,KEY_OUT_DISP_STIFFENER_THICKNESS,TYPE_TEXTBOX,self.t_s if flag else '',True)
            stiff_details.append(t3)
            t4 = (KEY_OUT_WELD_TYPE,KEY_OUT_DISP_WELD_TYPE,TYPE_TEXTBOX,self.weld_type if flag else '', True)
            stiff_details.append(t4)
            return stiff_details
        else:
            pass

    def output_values(self, flag):

        out_list = []

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_D, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,self.bolt_diam_provided if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_GRD, KEY_DISP_GRD, TYPE_TEXTBOX,self.bolt_grade_provided if flag else '', True)
        out_list.append(t3)

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
              round(self.bolt.bolt_shear_capacity / 1000, 2) if flag else '', True)
        out_list.append(t4)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)
                pass
            else:
                bolt_bearing_capacity_disp = self.bolt.bolt_bearing_capacity

        t5 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_VALUE, TYPE_TEXTBOX,
              round(self.bolt.bolt_capacity / 1000, 2) if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_OUT_BOLT_TENSION_CAPACITY, KEY_OUT_DISP_BOLT_TENSION_CAPACITY, TYPE_TEXTBOX,
              round(self.bolt.bolt_tension_capacity / 1000, 2) if flag else '', True)
        out_list.append(t7)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.pitch if flag else '', True)
        out_list.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.end_dist if flag else '', True)
        out_list.append(t10)

        t8 = (KEY_OUT_NO_BOLTS_WEB, KEY_OUT_DISP_NO_BOLTS_WEB, TYPE_TEXTBOX, self.n_bw_prov * 2 if flag else '', True)
        out_list.append(t8)

        t9 = (KEY_OUT_NO_BOLTS_FLANGE, KEY_OUT_DISP_NO_BOLTS_FLANGE, TYPE_TEXTBOX, self.no_bolts_flange if flag else '', True)
        out_list.append(t9)

        t11 = (KEY_OUT_NO_BOLTS, KEY_OUT_DISP_NO_BOLTS, TYPE_TEXTBOX, self.no_bolts_prov if flag else '', True)
        out_list.append(t11)

        # t21 = (KEY_BOLT_DETAILS, KEY_DISP_BOLT_DETAILS, TYPE_OUT_BUTTON, ['Bolt detailing', self.detailing])
        # out_list.append(t21)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True)
        out_list.append(t13)

        t14 = (KEY_OUT_PLATETHK, KEY_OUT_DISP_PLATETHK, TYPE_TEXTBOX, self.plate_thickness_provided if flag else '', True)
        out_list.append(t14)

        t15 = (KEY_OUT_PLATE_HEIGHT, KEY_OUT_DISP_PLATE_HEIGHT, TYPE_TEXTBOX, self.plate_height if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_PLATE_LENGTH, KEY_OUT_DISP_PLATE_LENGTH, TYPE_TEXTBOX, self.plate_width if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_PLATE_MOM_CAPACITY, KEY_OUT_DISP_PLATE_MOM_CAPACITY, TYPE_TEXTBOX, round(self.m_dp/1000000,2) if flag else '', True)
        out_list.append(t17)

        # if 2*self.end_dist < 50 and self.h_s < 100:
        #     pass
        # elif 2*self.end_dist >= 50 and self.h_s >= 100:

        # if flag is True:
        #     if self.connection == "Extended Both Ways":
        #         t33 = (None, KEY_OUT_DISP_STIFFENER_DETAILS, TYPE_TITLE, None, True)
        #         out_list.append(t33)
        #
        #         t21 = (KEY_OUT_STIFFENER_HEIGHT,KEY_OUT_DISP_STIFFENER_HEIGHT,TYPE_TEXTBOX,self.stiff_ht if flag else '', True)
        #         out_list.append(t21)
        #         t22 = (KEY_OUT_STIFFENER_WIDTH,KEY_OUT_DISP_STIFFENER_WIDTH,TYPE_TEXTBOX,self.stiff_wt if flag else '', True)
        #         out_list.append(t22)
        #         t23 = (KEY_OUT_STIFFENER_THICKNESS,KEY_OUT_DISP_STIFFENER_THICKNESS,TYPE_TEXTBOX,self.t_s if flag else '',True)
        #         out_list.append(t23)
        #         t24 = (KEY_OUT_WELD_TYPE,KEY_OUT_DISP_WELD_TYPE,TYPE_TEXTBOX,self.weld_type if flag else '', True)
        #         out_list.append(t24)
        #     else:
        #         t33 = (None, KEY_OUT_DISP_STIFFENER_DETAILS, TYPE_TITLE, None, False)
        #         out_list.append(t33)
        #         t21 = (KEY_OUT_STIFFENER_HEIGHT, KEY_OUT_DISP_STIFFENER_HEIGHT, TYPE_TEXTBOX, self.stiff_ht if flag else '',False)
        #         out_list.append(t21)
        #         t22 = (KEY_OUT_STIFFENER_WIDTH, KEY_OUT_DISP_STIFFENER_WIDTH, TYPE_TEXTBOX, self.stiff_wt if flag else '',False)
        #         out_list.append(t22)
        #         t23 = (KEY_OUT_STIFFENER_THICKNESS, KEY_OUT_DISP_STIFFENER_THICKNESS, TYPE_TEXTBOX, self.t_s if flag else '',False)
        #         out_list.append(t23)
        #         t24 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX, self.weld_type if flag else '', False)
        #         out_list.append(t24)
        #         pass

        t33 = (KEY_OUT_STIFFENER_TITLE, KEY_OUT_DISP_STIFFENER_DETAILS, TYPE_TITLE, None, True)
        out_list.append(t33)
        t21 = (KEY_OUT_STIFFENER_HEIGHT, KEY_OUT_DISP_STIFFENER_HEIGHT, TYPE_TEXTBOX, self.stiff_ht if flag else '', True)
        out_list.append(t21)
        t22 = (KEY_OUT_STIFFENER_WIDTH, KEY_OUT_DISP_STIFFENER_WIDTH, TYPE_TEXTBOX, self.stiff_wt if flag else '', True)
        out_list.append(t22)
        t23 = (KEY_OUT_STIFFENER_THICKNESS, KEY_OUT_DISP_STIFFENER_THICKNESS, TYPE_TEXTBOX, self.t_s if flag else '', True)
        out_list.append(t23)
        t24 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX, self.weld_type if flag else '', True)
        out_list.append(t24)
        # t22 = (KEY_OUT_STIFFENER_DETAILS,KEY_OUT_DISP_STIFFENER_DETAILS,TYPE_OUT_BUTTON, ['Stiffener Details',self.stiffener_details], True)
        # out_list.append(t22)

        return out_list

    def input_value_changed(self):
        lst = []
        # t6 = ([KEY_CONN], KEY_OUT_STIFFENER_TITLE, TYPE_LABEL, self.out_stiffener)
        # lst.append(t6)
        t6 = ([KEY_CONN], KEY_OUT_STIFFENER_HEIGHT, TYPE_OUT_DOCK, self.out_stiffener)
        lst.append(t6)
        t6 = ([KEY_CONN], KEY_OUT_STIFFENER_WIDTH, TYPE_OUT_DOCK, self.out_stiffener)
        lst.append(t6)
        t6 = ([KEY_CONN], KEY_OUT_STIFFENER_THICKNESS, TYPE_OUT_DOCK, self.out_stiffener)
        lst.append(t6)
        t6 = ([KEY_CONN], KEY_OUT_WELD_TYPE, TYPE_OUT_DOCK, self.out_stiffener)
        lst.append(t6)
        t6 = ([KEY_CONN], KEY_OUT_STIFFENER_HEIGHT, TYPE_OUT_LABEL, self.out_stiffener)
        lst.append(t6)
        t6 = ([KEY_CONN], KEY_OUT_STIFFENER_WIDTH, TYPE_OUT_LABEL, self.out_stiffener)
        lst.append(t6)
        t6 = ([KEY_CONN], KEY_OUT_STIFFENER_THICKNESS, TYPE_OUT_LABEL, self.out_stiffener)
        lst.append(t6)
        t6 = ([KEY_CONN], KEY_OUT_WELD_TYPE, TYPE_OUT_LABEL, self.out_stiffener)
        lst.append(t6)

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        return lst

    def out_stiffener(self):
        conn_type = self[0]
        if conn_type != 'Extended Both Ways':
            return True
        else:
            return False

    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from Column and Beams table.
        """
        global logger
        red_list = red_list_function()
        if self.section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def set_input_values(self, design_dictionary):

        print(design_dictionary)

        super(ColumnEndPlate, self).set_input_values(self, design_dictionary)

        self.section = Column(designation=design_dictionary[KEY_SECSIZE],
                              material_grade=design_dictionary[KEY_SEC_MATERIAL])

        self.start_time = time.time()

        self.module = design_dictionary[KEY_MODULE]
        self.connection = design_dictionary[KEY_CONN]
        # self.design_pref = design_dictionary[KEY_CONN_PREFERENCE]

        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None), material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL])
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary[KEY_DP_BOLT_SLIP_FACTOR],
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        # if self.design_status:
        #     self.commLogicObj = CommonDesignLogic(window.display, window.folder, self.module, self.mainmodule)
        #     status = self.design_status
        #     self.commLogicObj.call_3DModel(status, ColumnEndPlate)
        print("Input values are set. Doing preliminary member checks")
        self.member_capacity(self)

    def member_capacity(self):
        """"
        This function is used to update the axial, shear and moment loads provided
        by user according to miminum member capacity and also provides an error if
        exceeds full capacity of member
        """
    #########  Axial capacity   ##########################
        gamma_m0 = 1.1
        # Axial Capacity
        self.axial_capacity = (self.section.area * self.section.fy) / gamma_m0  # N
        self.min_axial_load = 0.3 * self.axial_capacity
        # self.factored_axial_load = max(self.load.axial_force * 1000, self.min_axial_load)  # N
        if self.load.axial_force * 1e3 < self.min_axial_load:
            self.factored_axial_load = self.min_axial_load
            self.design_status = True
        elif self.load.axial_force * 1e3> self.min_axial_load and self.load.axial_force * 1e3 < self.axial_capacity:
            self.factored_axial_load = self.load.axial_force * 1e3
            self.design_status = True

        else:
            self.design_status = False
            logger.error(":The axial force {} acting is higher than axial capacity {} of member".format(self.load.axial_force,self.axial_capacity/1000))
            logger.info("Increase member size or decrease axial load")
        # self.load.axial_force = self.factored_axial_load  # N
        print("factored_axial_load", self.factored_axial_load)
    ###############################################################

    ##################   Shear Capacity  ######################
        self.shear_capacity = ((self.section.depth - (2 * self.section.flange_thickness)) * self.section.web_thickness * self.section.fy) / (
                                 math.sqrt(3) * gamma_m0)  # N # A_v: Total cross sectional area in shear in mm^2 (float)
        self.min_shear_load = 0.6 * self.shear_capacity  # N
        self.fact_shear_load = max(self.min_shear_load, self.load.shear_force * 1000)  # N
        if self.load.shear_force * 1e3 < self.min_shear_load:
            self.factored_shear_load = self.min_shear_load
            self.design_status = True
        elif self.load.shear_force * 1e3 > self.min_shear_load and self.load.shear_force * 1e3 < self.shear_capacity:
            self.factored_shear_load = self.load.shear_force * 1e3
            self.design_status = True
        else:
            self.design_status = False
            logger.error(":The shear force {} acting is higher than shear capacity {} of member".format(self.load.shear_force,self.shear_capacity/1000))
            logger.info("Increase member size or decrease shear load")
        print("factored_shear_load", self.factored_shear_load)
    ###############################################################

    ################  Moment Capacity  ############################
        if self.section.type == "Rolled":
            self.limitwidththkratio_flange = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                           column_t_w=self.section.web_thickness,
                                                                           column_d=self.section.depth,
                                                                           column_b=self.section.flange_width,
                                                                           column_fy=self.section.fy,
                                                                           factored_axial_force=self.load.shear_force,
                                                                           column_area=self.section.area,
                                                                           compression_element="External",
                                                                           section="Rolled")
            print("limitwidththkratio_flange", self.limitwidththkratio_flange)
        else:
            pass

        if self.section.type2 == "generally":
            self.limitwidththkratio_web = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                        column_t_w=self.section.web_thickness,
                                                                        column_d=self.section.depth,
                                                                        column_b=self.section.flange_width,
                                                                        column_fy=self.section.fy,
                                                                        factored_axial_force=self.load.shear_force,
                                                                        column_area=self.section.area,
                                                                        compression_element="Web of an I-H",
                                                                        section="generally")
            print("limitwidththkratio_flange", self.limitwidththkratio_web)

        else:
            pass

        # if self.load.shear_force < (0.6 * self.shear_capacity):
        self.Z_p = float((self.section.web_thickness * (self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 4)  # mm3
        self.Z_e = float((self.section.web_thickness * (self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 6)  # mm3

        self.class_of_section = int(max(self.limitwidththkratio_flange, self.limitwidththkratio_web))
        print("class of section",self.class_of_section)
        # if self.class_of_section == 1 or self.class_of_section == 2:
        #     Z_w = self.Z_p
        # elif self.class_of_section == 3:
        #     Z_w = self.Z_e

        if self.class_of_section == 1 or self.class_of_section == 2:
            beta_b = 1
        elif self.class_of_section == 3:
            beta_b = self.Z_e / self.Z_p
        else:
            pass

        if self.load.shear_force < 0.6 * self.shear_capacity:
            # self.moment_capacity = self.section.plastic_moment_capacty(beta_b=beta_b, Z_p=self.Z_p, fy=self.section.fy)
            self.moment_capacity = beta_b * self.Z_p * self.section.fy / gamma_m0
        else:
            if self.class_of_section == 1 or self.class_of_section == 2:
                m_d = self.Z_p * self.section.fy / gamma_m0
                beta = ((2 * self.load.shear_force / self.shear_capacity) - 1) ** 2
                m_fd = (self.Z_p - (self.section.depth ** 2 * self.section.web_thickness / 4)) * self.section.fy / gamma_m0
                self.moment_capacity = m_d - beta(m_d - m_fd)
            else:
                self.moment_capacity = self.Z_e * self.section.fy / gamma_m0

        self.min_moment = 0.5 * self.moment_capacity
        if self.load.moment * 1e6 < float(self.min_moment):
            self.factored_moment = self.min_moment
            self.design_status = True
        elif self.load.moment * 1e6 > self.min_moment and self.load.moment * 1e6 < self.moment_capacity:
            self.factored_moment = self.load.moment * 1e6
            self.design_status = True
        else:
            self.design_status = False
            logger.error(":The moment {} acting is higher than moment capacity {} of member".format(self.load.moment, self.moment_capacity))
            logger.info("Increase member size or decrease shear load")
        print("factored_moment", self.factored_moment)

       ###############################
        if self.design_status == True:
            print("Preliminary member check is satisfactory. Doing bolt checks")
            self.get_bolt_diam(self)
        else:
            logger.error("Either decrease the loads or increase member size")

    #############################################################################################
    ## Function to get bolt diam ##
    ############################################################################################

    def get_bolt_diam(self, previous_size = None):
        """"
        Each diam size selected by user goes in a loop and gives no of bolts based on pitch, end dist and
        section size, the bolt diam which gives minimum bolt numbers is selected
        """
        self.lst1 = []
        self.lst2 = []

        for x in self.bolt.bolt_diameter:
            self.pitch = IS800_2007.cl_10_2_2_min_spacing(x)
            self.end_dist = round_up(IS800_2007.cl_10_2_4_2_min_edge_end_dist(x,self.bolt.bolt_hole_type,self.bolt.edge_type),5)
            print("Bolt diam: ", x,"Pitch: ",self.pitch,"End-dist: ",self.end_dist)

        ########## no of bolts along each side of web and flange  ##################
            self.n_bw = int(math.floor(((self.section.depth - (2 * self.section.flange_thickness + (2 * self.end_dist))) / self.pitch) + 1))
            self.n_bf = int(math.ceil((((self.section.flange_width / 2) - ((self.section.web_thickness / 2) + (2 * self.end_dist))) / self.pitch) - 2))

            if self.n_bf <= 0:
                self.n_bf = 1
            elif self.n_bf > 0:
                self.n_bf = self.n_bf + 2
            print("no bolts web",self.n_bw, "no bolts flange",self.n_bf)

            if self.connection == 'Flush End Plate':
                if self.n_bf == 1:
                    self.no_bolts = self.n_bw * 2
                elif self.n_bf > 1:
                    self.no_bolts = self.n_bw * 2 + (self.n_bf-1) * 4
            else:
                if self.n_bf == 1:
                    self.no_bolts = self.n_bw * 2 + 4
                elif self.n_bf > 1:
                    self.no_bolts = self.n_bw * 2 + (self.n_bf-1) * 4 + self.n_bf*4
            print("no of bolts", self.no_bolts)

        ######### pitch 2 along web  ##################
            if self.n_bw % 2 == 0:
                self.p_2_web = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.end_dist) - ((self.n_bw - 2) * self.pitch)
            else:
                self.p_2_web = (self.section.depth - (2 * self.section.flange_thickness) - (2 * self.end_dist) - ((self.n_bw - 3) * self.pitch))/2
            print("p_2_web",self.p_2_web)

        ######### pitch 2 along flange  ################
            if self.n_bf % 2 == 0:
                if self.n_bf == 2:
                    self.p_2_flange = (self.section.flange_width/2) - (self.section.web_thickness/2) - (2 * self.end_dist)
                else:
                    self.p_2_flange = (self.section.flange_width/2) - (self.section.web_thickness/2) - (2 * self.end_dist) - ((self.n_bf-2) * self.pitch)
            else:
                if self.n_bf == 3:
                    ((self.section.flange_width / 2) - (self.section.web_thickness / 2) - (2 * self.end_dist))/2
                else:
                    self.p_2_flange = ((self.section.flange_width/2) - (self.section.web_thickness/2) - (2 * self.end_dist) - ((self.n_bf - 3) * self.pitch))/2

            if self.p_2_flange < 0:
                self.p_2_flange = 0.0
            else:
                pass
            print("p_2_flange",self.p_2_flange)
            # self.x = (self.section.flange_width / 2) - (self.section.web_thickness / 2) - self.end_dist - (self.n_bf * self.pitch)

        ############# y_max and y square ################
            if self.connection == 'Flush End Plate':
                self.y_max = self.section.depth - 3/2 * self.section.flange_thickness - self.end_dist
            else:
                self.y_max = self.section.depth - self.section.flange_thickness/2 + self.end_dist
            print("y_max",self.y_max)

            if self.connection == 'Flush End Plate':
                if self.n_bw % 2 == 0:
                    if self.n_bw == 2:
                        self.y_sqr1 = (self.section.flange_thickness/2 + self.end_dist)**2
                        self.y_sqr2 = (self.section.flange_thickness/2 + self.end_dist + self.p_2_web)**2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                    else:
                        self.y_sqr1 = (self.section.flange_thickness/2 + self.end_dist)**2
                        print("y_sqr1",self.y_sqr1)

                        self.y_sqr2 = 0
                        for i in range(1,int(self.n_bw/2)):
                            self.y_sq2 = (self.section.flange_thickness/2 + self.end_dist + i * self.pitch)**2
                            self.y_sqr2 = self.y_sqr2 + self.y_sq2
                        # return self.y_sqr2
                        print("y_sqr2",self.y_sqr2)

                        self.y_sqr3 = (self.section.flange_thickness/2 + self.end_dist + ((self.n_bw/2)-1) * self.pitch + self.p_2_web)**2
                        print("y_sqr3",self.y_sqr3)

                        self.y_sqr4 = 0
                        for i in range(1,int(self.n_bw/2)):
                            self.y_sq4 = (self.section.flange_thickness/2 + self.end_dist + ((self.n_bw/2)-1) * self.pitch + self.p_2_web + i * self.pitch)**2
                            self.y_sqr4 = self.y_sqr4 + self.y_sq4
                        print("y_sqr4",self.y_sqr4)

                        self.y_sqr = self.y_sqr1 + self.y_sqr2 + self.y_sqr3 + self.y_sqr4
                    print("y_sqr",self.y_sqr)
                else:
                    if self.n_bw == 3:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + 2 * self.p_2_web) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                    else:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        print("y_sqr1",self.y_sqr1)

                        self.y_sqr2 = 0
                        for i in range(1,int(self.n_bw/2 - 0.5)):
                            self.y_sq2 = (self.section.flange_thickness / 2 + self.end_dist + i * self.pitch) ** 2
                            self.y_sqr2 = self.y_sqr2 + self.y_sq2
                        print("y_sqr2", self.y_sqr2)

                        self.y_sqr3 = (self.section.flange_thickness / 2 + self.end_dist + ((self.n_bw / 2) - 1.5) * self.pitch + self.p_2_web) ** 2
                        print("y_sqr3", self.y_sqr3)

                        self.y_sqr4 = (self.section.flange_thickness / 2 + self.end_dist + ((self.n_bw / 2) - 1.5) * self.pitch + 2 * self.p_2_web) ** 2
                        print("y_sqr4", self.y_sqr4)

                        self.y_sqr5 = 0
                        for i in range(1,int(self.n_bw/2 - 0.5)):
                            self.y_sq5 = (self.section.flange_thickness/2 + self.end_dist + ((self.n_bw/2)-1.5) * self.pitch + 2 * self.p_2_web + i * self.pitch)**2
                            self.y_sqr5 = self.y_sqr5 + self.y_sq5
                        print("y_sqr5",self.y_sqr5)

                        self.y_sqr = self.y_sqr1 + self.y_sqr2 + self.y_sqr3 + self.y_sqr4 + self.y_sqr5
                    print("y_sqr",self.y_sqr)
            else:
                if self.n_bw % 2 == 0:
                    if self.n_bw == 2:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + self.p_2_web) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                    else:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        print("y_sqr1", self.y_sqr1)

                        self.y_sqr2 = 0
                        for i in range(1, int(self.n_bw / 2)):
                            self.y_sq2 = (self.section.flange_thickness / 2 + self.end_dist + i * self.pitch) ** 2
                            self.y_sqr2 = self.y_sqr2 + self.y_sq2
                        print("y_sqr2", self.y_sqr2)

                        self.y_sqr3 = (self.section.flange_thickness / 2 + self.end_dist + (
                                    (self.n_bw / 2) - 1) * self.pitch + self.p_2_web) ** 2
                        print("y_sqr3", self.y_sqr3)

                        self.y_sqr4 = 0
                        for i in range(1, int(self.n_bw / 2)):
                            self.y_sq4 = (self.section.flange_thickness / 2 + self.end_dist + (
                                        (self.n_bw / 2) - 1) * self.pitch + self.p_2_web + i * self.pitch) ** 2
                            self.y_sqr4 = self.y_sqr4 + self.y_sq4
                        print("y_sqr4", self.y_sqr4)

                        self.y_sqr5 = (1.5 * self.section.flange_thickness + 3 * self.end_dist + (self.n_bw - 2)*self.pitch + self.p_2_web) ** 2

                        self.y_sqr = self.y_sqr1 + self.y_sqr2 + self.y_sqr3 + self.y_sqr4 + self.y_sqr5
                    print("y_sqr", self.y_sqr)
                else:
                    if self.n_bw == 3:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + 2 * self.p_2_web) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                    else:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        print("y_sqr1", self.y_sqr1)

                        self.y_sqr2 = 0
                        for i in range(1, int(self.n_bw / 2 - 0.5)):
                            self.y_sq2 = (self.section.flange_thickness / 2 + self.end_dist + i * self.pitch) ** 2
                            self.y_sqr2 = self.y_sqr2 + self.y_sq2
                        print("y_sqr2", self.y_sqr2)

                        self.y_sqr3 = (self.section.flange_thickness / 2 + self.end_dist + (
                                    (self.n_bw / 2) - 1.5) * self.pitch + self.p_2_web) ** 2
                        print("y_sqr3", self.y_sqr3)

                        self.y_sqr4 = (self.section.flange_thickness / 2 + self.end_dist + (
                                    (self.n_bw / 2) - 1.5) * self.pitch + 2 * self.p_2_web) ** 2
                        print("y_sqr4", self.y_sqr4)

                        self.y_sqr5 = 0
                        for i in range(1, int(self.n_bw / 2 - 0.5)):
                            self.y_sq5 = (self.section.flange_thickness / 2 + self.end_dist + (
                                        (self.n_bw / 2) - 1.5) * self.pitch + 2 * self.p_2_web + i * self.pitch) ** 2
                            self.y_sqr5 = self.y_sqr5 + self.y_sq5
                        print("y_sqr5", self.y_sqr5)

                        self.y_sqr6 = (1.5 * self.section.flange_thickness + 3 * self.end_dist + (self.n_bw - 3)*self.pitch + 2 * self.p_2_web) ** 2

                        self.y_sqr = self.y_sqr1 + self.y_sqr2 + self.y_sqr3 + self.y_sqr4 + self.y_sqr5 + self.y_sqr6
                    print("y_sqr", self.y_sqr)


            self.t_b = round((self.factored_axial_load / self.no_bolts) + (self.factored_moment * self.y_max) / self.y_sqr,2)

            self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=x,
                                                      # bolt_grade_provided=self.bolt.bolt_grade[y]
                                                      bolt_grade_provided=(self.bolt.bolt_grade[-1]))

            print("T_b: ",self.t_b,"Bolt tension capacity: ",self.bolt.bolt_tension_capacity)
            if self.t_b < self.bolt.bolt_tension_capacity:
                # self.lst1.append(x)
                # self.lst2.append(self.no_bolts)
                if previous_size is None:
                    self.lst1.append(x)
                    self.lst2.append(self.no_bolts)
                    print("List1, List2",self.lst1,self.lst2)
                else:
                    # self.prev_dia = (previous_size)
                    if previous_size != x and previous_size > x:
                        self.lst1.append(x)
                        self.lst2.append(self.no_bolts)
                        print("after prev size, lst1, lst2",self.lst1,self.lst2)
                        print("excluded diam",previous_size)
                        print(self.lst1)
                        # self.lst1.pop(self.prev_dia)
                    else:
                        pass

                # if previous_size in self.lst1:
                # self.lst1.pop(previous_size)

                # self.lst2.append(y)
                # self.lst1.append(x)
                # self.lst2.append(self.no_bolts)
                self.res = dict(zip(self.lst1, self.lst2))
            else:
                pass

                # if self.t_b > self.bolt.bolt_tension_capacity:
                #     self.design_status = False
                #     logger.error("tension capacity and moment capacity of member is less than applied axial force and momemt")
                # elif self.v_sb > self.bolt.bolt_capacity:
                #     self.design_status = False
                #     logger.error("shear capacity of member is less than applied shear")

        if len(self.lst1) != 0:
            # if self.design_pref == "Bolt Oriented":
            # print (self.design_pref)
            # if previous_size is None:
            #     pass
            # else:
            #     for a in self.lst1:
            #         if (previous_size) == 36.0:
            #             print("prev size",previous_size)
            #             self.lst1 = self.lst1[1:a]
            #         else:
            #             pass

                # self.prev_dia = (previous_size)
                # if self.prev_dia in self.lst1:
                #     print("excluded diam",self.prev_dia)
                #     print(self.lst1)
                #     self.lst1.pop(self.prev_dia)
                # else:
                #     pass
            key_min = min(self.res, key=self.res.get)
            self.bolt_diam_provided = key_min
            # return self.bolt_diam_provided
            print("diam list", self.lst1)
            print("no of bolts list", self.lst2)
            print("dict", self.res)
            print("Bolt diam prov", self.bolt_diam_provided)
            print("Selecting bolt grade")
            # self.get_bolt_grade(self)
            self.design_status = True
            self.get_bolt_grade(self)
            # else:
            #     key_max = max(self.res, key=self.res.get)
            #     print (self.design_pref)
            #     self.bolt_diam_provided = key_max
            #     # return self.bolt_diam_provided
            #     print("diam list", self.lst1)
            #     print("no of bolts list", self.lst2)
            #     print("dict", self.res)
            #     print("Bolt diam prov", self.bolt_diam_provided)
            #     print("Selecting bolt grade")
            #     # self.get_bolt_grade(self)
            #     self.design_status = True
            #     self.get_bolt_grade(self)

        else:
            if KEY_D == 'Customized':
                self.design_status = False
                logger.error("Try Different bolt diam")

            elif self.connection == "Flush End Plate":
                self.design_status = False
                logger.error("Try Different material or Try Extended both ways Connection")

    #############################################################################################################
    ## Function to get Bolt grade ##
    ###############################################################################################################

    def get_bolt_grade(self):
        """"
        Bolt size selected in upper function is checked with each bolt grade and the minimum
        bolt grade which passes the chech is selected
        """
        self.lst3 = []
        # self.lst2 = []
        # for (x,y) in (self.bolt.bolt_diameter,self.bolt.bolt_grade):
        for x in self.bolt.bolt_grade:
            self.pitch = IS800_2007.cl_10_2_2_min_spacing(self.bolt_diam_provided)
            self.end_dist = round_up(IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt_diam_provided,self.bolt.bolt_hole_type,self.bolt.edge_type),5)
            print("Bolt diam: ", self.bolt_diam_provided,"Pitch: ",self.pitch,"End-dist: ",self.end_dist)

            ########## no of bolts along each side of web and flange  ##################
            self.n_bw_prov = int(math.floor(
                ((self.section.depth - (2 * self.section.flange_thickness + (2 * self.end_dist))) / self.pitch) + 1))
            # print("n_bw",self.n_bw)
            self.n_bf_prov = int(math.ceil((((self.section.flange_width / 2) - (
                        (self.section.web_thickness / 2) + (2 * self.end_dist))) / self.pitch) - 2))
            # print("n_bf",self.n_bf)
            print("In bolt grade loop")
            if self.n_bf_prov <= 0:
                self.n_bf_prov = 1
            # elif self.n_bf == 0:
            #     self.n_bf = 1
            elif self.n_bf_prov > 0:
                self.n_bf_prov = self.n_bf_prov + 2
            print("no bolts web", self.n_bw_prov, "no bolts flange", self.n_bf_prov)

            if self.connection == "Flush End Plate":
                self.no_bolts_flange = self.n_bf_prov *4
            else:
                self.no_bolts_flange = self.n_bf_prov * 8

            if self.connection == 'Flush End Plate':
                if self.n_bf_prov == 1:
                    self.no_bolts_prov = self.n_bw_prov * 2
                elif self.n_bf_prov > 1:
                    self.no_bolts_prov = self.n_bw_prov * 2 + (self.n_bf_prov-1) * 4
            else:
                if self.n_bf_prov == 1:
                    self.no_bolts_prov = self.n_bw_prov * 2 + 4
                elif self.n_bf_prov > 1:
                    self.no_bolts_prov = self.n_bw_prov * 2 + (self.n_bf_prov-1) * 4 + self.n_bf_prov*4
            print("no of bolts", self.no_bolts_prov)

            ######### pitch 2 along web  ##################
            if self.n_bw_prov % 2 == 0:
                self.p_2_web_prov = self.section.depth - (2 * self.section.flange_thickness) - (2 * self.end_dist) - ((self.n_bw_prov - 2) * self.pitch)
            else:
                self.p_2_web_prov = (self.section.depth - (2 * self.section.flange_thickness) - (2 * self.end_dist) - ((self.n_bw_prov - 3) * self.pitch))/2
            print("p_2_web",self.p_2_web_prov)

            ######### pitch 2 along flange  ################
            if self.n_bf_prov % 2 == 0:
                if self.n_bf_prov == 2:
                    self.p_2_flange_prov = (self.section.flange_width / 2) - (self.section.web_thickness / 2) - (2 * self.end_dist)
                else:
                    self.p_2_flange_prov = (self.section.flange_width / 2) - (self.section.web_thickness / 2) - (2 * self.end_dist) - ((self.n_bf_prov -2) * self.pitch)
            else:
                if self.n_bf_prov == 3:
                    self.p_2_flange_prov = ((self.section.flange_width / 2) - (self.section.web_thickness / 2) - (2 * self.end_dist))/2
                else:
                    self.p_2_flange_prov = ((self.section.flange_width / 2) - (self.section.web_thickness / 2) - (2 * self.end_dist) - ((self.n_bf_prov - 3) * self.pitch))/2
            # print("p_2_flange",self.p_2_flange)

            if self.p_2_flange_prov < 0:
                self.p_2_flange_prov = 0.0
            else:
                pass
            print("p_2_flange",self.p_2_flange_prov)

            # self.x = (self.section.flange_width / 2) - (self.section.web_thickness / 2) - self.end_dist - (self.n_bf * self.pitch)

            ############# y_max and y square ################
            if self.connection == 'Flush End Plate':
                self.y_max = self.section.depth - 3 / 2 * self.section.flange_thickness - self.end_dist
            else:
                self.y_max = self.section.depth - self.section.flange_thickness / 2 + self.end_dist
            # print("y_max", self.y_max)

            if self.connection == 'Flush End Plate':
                if self.n_bw_prov % 2 == 0:
                    if self.n_bw_prov == 2:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + self.p_2_web_prov) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                    else:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        # print("y_sqr1", self.y_sqr1)

                        for i in range(1, int(self.n_bw_prov / 2)):
                            self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + i * self.pitch) ** 2
                        # print("y_sqr2", self.y_sqr2)

                        self.y_sqr3 = (self.section.flange_thickness / 2 + self.end_dist + (
                                    (self.n_bw_prov / 2) - 1) * self.pitch + self.p_2_web_prov) ** 2
                        # print("y_sqr3", self.y_sqr3)

                        for i in range(1, int(self.n_bw_prov / 2)):
                            self.y_sqr4 = (self.section.flange_thickness / 2 + self.end_dist + (
                                        (self.n_bw_prov / 2) - 1) * self.pitch + self.p_2_web_prov + i * self.pitch) ** 2
                        # print("y_sqr4", self.y_sqr4)

                        self.y_sqr = self.y_sqr1 + self.y_sqr2 + self.y_sqr3 + self.y_sqr4
                    # print("y_sqr", self.y_sqr)
                else:
                    if self.n_bw_prov == 3:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + 2 * self.p_2_web_prov) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                    else:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        # print("y_sqr1", self.y_sqr1)

                        for i in range(1, int(self.n_bw_prov / 2 - 0.5)):
                            self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + i * self.pitch) ** 2
                        # print("y_sqr2", self.y_sqr2)

                        self.y_sqr3 = (self.section.flange_thickness / 2 + self.end_dist + (
                                    (self.n_bw_prov / 2) - 1.5) * self.pitch + self.p_2_web_prov) ** 2
                        # print("y_sqr3", self.y_sqr3)

                        self.y_sqr4 = (self.section.flange_thickness / 2 + self.end_dist + (
                                    (self.n_bw_prov / 2) - 1.5) * self.pitch + 2 * self.p_2_web_prov) ** 2
                        # print("y_sqr4", self.y_sqr4)

                        for i in range(1, int(self.n_bw_prov / 2 - 0.5)):
                            self.y_sqr5 = (self.section.flange_thickness / 2 + self.end_dist + (
                                        (self.n_bw_prov / 2) - 1.5) * self.pitch + 2 * self.p_2_web_prov + i * self.pitch) ** 2
                        # print("y_sqr5", self.y_sqr5)

                        self.y_sqr = self.y_sqr1 + self.y_sqr2 + self.y_sqr3 + self.y_sqr4 + self.y_sqr5
                    # print("y_sqr", self.y_sqr)
            else:
                if self.n_bw_prov % 2 == 0:
                    if self.n_bw_prov == 2:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + self.p_2_web_prov) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                    else:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        # print("y_sqr1", self.y_sqr1)

                        for i in range(1, int(self.n_bw_prov / 2)):
                            self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + i * self.pitch) ** 2
                        # print("y_sqr2", self.y_sqr2)

                        self.y_sqr3 = (self.section.flange_thickness / 2 + self.end_dist + (
                                (self.n_bw_prov / 2) - 1) * self.pitch + self.p_2_web_prov) ** 2
                        # print("y_sqr3", self.y_sqr3)

                        for i in range(1, int(self.n_bw_prov / 2)):
                            self.y_sqr4 = (self.section.flange_thickness / 2 + self.end_dist + (
                                    (self.n_bw_prov / 2) - 1) * self.pitch + self.p_2_web_prov + i * self.pitch) ** 2
                        # print("y_sqr4", self.y_sqr4)

                        self.y_sqr5 = (1.5 * self.section.flange_thickness + 3 * self.end_dist + (
                                    self.n_bw_prov - 2) * self.pitch + self.p_2_web_prov) ** 2

                        self.y_sqr = self.y_sqr1 + self.y_sqr2 + self.y_sqr3 + self.y_sqr4 + self.y_sqr5
                    # print("y_sqr", self.y_sqr)
                else:
                    if self.n_bw_prov == 3:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + 2 * self.p_2_web_prov) ** 2
                        self.y_sqr = self.y_sqr1 + self.y_sqr2
                    else:
                        self.y_sqr1 = (self.section.flange_thickness / 2 + self.end_dist) ** 2
                        # print("y_sqr1", self.y_sqr1)

                        for i in range(1, int((self.n_bw_prov / 2) - 0.5)):
                            self.y_sqr2 = (self.section.flange_thickness / 2 + self.end_dist + i * self.pitch) ** 2
                        # print("y_sqr2", self.y_sqr2)

                        self.y_sqr3 = (self.section.flange_thickness / 2 + self.end_dist + (
                                (self.n_bw_prov / 2) - 1.5) * self.pitch + self.p_2_web_prov) ** 2
                        # print("y_sqr3", self.y_sqr3)

                        self.y_sqr4 = (self.section.flange_thickness / 2 + self.end_dist + (
                                (self.n_bw_prov / 2) - 1.5) * self.pitch + 2 * self.p_2_web_prov) ** 2
                        # print("y_sqr4", self.y_sqr4)

                        for i in range(1, int((self.n_bw_prov / 2) - 0.5)):
                            self.y_sqr5 = (self.section.flange_thickness / 2 + self.end_dist + (
                                    (self.n_bw / 2) - 1.5) * self.pitch + 2 * self.p_2_web_prov + i * self.pitch) ** 2
                        # print("y_sqr5", self.y_sqr5)

                        self.y_sqr6 = (1.5 * self.section.flange_thickness + 3 * self.end_dist + (
                                    self.n_bw_prov - 3) * self.pitch + 2 * self.p_2_web_prov) ** 2

                        self.y_sqr = self.y_sqr1 + self.y_sqr2 + self.y_sqr3 + self.y_sqr4 + self.y_sqr5 + self.y_sqr6
                    print("y_sqr", self.y_sqr)

            self.t_b = round(
                (self.factored_axial_load / self.no_bolts_prov) + (self.factored_moment * self.y_max) / self.y_sqr, 2)
            # self.t_b = 0

            # self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt_diam_provided,
            #                                   bolt_grade_provided=x,
            #                                   # bolt_grade_provided=12.9,
            #                                   conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
            #                                   n_planes=1)
            self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt_diam_provided,
                                                      bolt_grade_provided=x)
                                                      # bolt_grade_provided=12.9)

        #
        #     if self.design_status:
        #         self.lst3.append(x)
        #         # self.lst2.append(y)
        # self.bolt_grade_provided = min(self.lst3)
            print("T_b: ", self.t_b, "Bolt tension capacity: ", self.bolt.bolt_tension_capacity)
            if self.t_b < self.bolt.bolt_tension_capacity:
                self.lst3.append(x)
            else:
                pass

        if len(self.lst3) != 0:
            self.bolt_grade_provided = min(self.lst3)
            # return self.bolt_diam_provided
            print("bolt grade", self.bolt_grade_provided)
            # self.get_bolt_grade(self)
            self.design_status = True
            self.plate_details(self)

        else:
            self.design_status = False
            logger.error("failed in bolt grade selection")


    # def bolt_capacities(self):
    #     self.lst_4 = []
    #     # self.bolt_conn_plates_t_fu_fy = []
    #     # self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
    #     for x in self.lst_pl:
    #         self.bolt_conn_plates_t_fu_fy = []
    #         self.bolt_conn_plates_t_fu_fy.append((x, self.plate.fu, self.plate.fy))
    #         self.bolt_conn_plates_t_fu_fy.append((x, self.plate.fu, self.plate.fy))
    #         self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt_diam_provided,
    #                                           bolt_grade_provided=self.bolt_grade_provided,
    #                                           # bolt_grade_provided=12.9,
    #                                           conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
    #                                           n_planes=1)
    #         # self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt_diam_provided,
    #         #                                           bolt_grade_provided=self.bolt_grade_provided)
    #         self.v_sb = self.factored_shear_load / (2 * self.n_bw)
    #         print("V_sb: ",self.v_sb,"Bolt capacity: ",self.bolt.bolt_capacity)
    #         if self.v_sb < self.bolt.bolt_capacity:
    #             self.lst_4.append(x)
    #         else:
    #             pass
    #
    #     if len(self.lst_4) != 0:
    #         self.plate_thickness_provided = min(self.lst_4)
    #         # return self.bolt_diam_provided
    #         print("Plate thickness prov", self.plate_thickness_provided)
    #         # self.get_bolt_grade(self)
    #         self.design_status = True
    #         # self.plate_details(self)
    #
    #     else:
    #         self.design_status = False
    #         logger.error("Plate thickness provided is not satisfied")

        # bolt_grade_provided=12.9)

    ########################################################################################################

    ########################################################################################################
    ## Function to get plate thickness ##
    #########################################################################################################
    def plate_details(self):
        if self.connection == 'Flush End Plate':
            self.plate_height = self.section.depth
        else:
            self.plate_height = self.section.depth + 4 * self.end_dist
        self.plate_width = self.section.flange_width
        self.y_2 = self.y_max - self.end_dist
        self.t_b2 = self.factored_axial_load / self.no_bolts + self.factored_moment * self.y_2 / self.y_sqr

        if self.connection == 'Flush End Plate':
            if self.n_bf <= 1:
                self.m_ep = max(0.5 * self.t_b * self.end_dist, self.t_b2 * self.end_dist)
            else:
                self.m_ep = self.t_b * self.end_dist

        else:
            self.m_ep = self.t_b * self.end_dist
        print("m_ep: ",self.m_ep)

        if self.pitch >= self.end_dist*2:
            self.b_eff = self.end_dist
        elif self.pitch < self.end_dist*2:
            self.b_eff = self.pitch

        gamma_m0 = 1.1
        self.lst_pl = []

        for x in self.plate.thickness:
            self.m_dp = self.b_eff * x**2 * self.plate.fy / (4 * gamma_m0)
            print("m_dp: ",self.m_dp)
            if self.m_dp > self.m_ep:
                self.lst_pl.append(x)
                print("plate list",self.lst_pl)
            else:
                pass
                # self.design_status = False
                # logger.error('Plate thickness provided is not sufficient')
                # logger.info('Please select higher tplate thickness')
        # self.bolt_capacities(self)
        self.lst_4 = []
        # self.bolt_conn_plates_t_fu_fy = []
        # self.bolt_conn_plates_t_fu_fy.append((self.plate.thickness_provided, self.plate.fu, self.plate.fy))
        for x in self.lst_pl:
            self.bolt_conn_plates_t_fu_fy = []
            self.bolt_conn_plates_t_fu_fy.append((x, self.plate.fu, self.plate.fy))
            self.bolt_conn_plates_t_fu_fy.append((x, self.plate.fu, self.plate.fy))
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt_diam_provided,conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)
            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=self.bolt_diam_provided,
                                              bolt_grade_provided=self.bolt_grade_provided,
                                              # bolt_grade_provided=12.9,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=1)
            # self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt_diam_provided,
            #                                           bolt_grade_provided=self.bolt_grade_provided)
            if self.connection == 'Flush End Plate':
                self.v_sb = self.factored_shear_load / (2 * self.n_bw)
            else:
                self.v_sb = self.factored_shear_load / ((2 * self.n_bw) + 4)

            print("V_sb: ", self.v_sb, "Bolt capacity: ", self.bolt.bolt_capacity)

            if self.v_sb < self.bolt.bolt_capacity:
                self.lst_4.append(x)
            else:
                pass

        if len(self.lst_4) != 0:
            self.plate_thickness_provided = min(self.lst_4)
            # return self.bolt_diam_provided
            print("Plate thickness prov", self.plate_thickness_provided)
            # self.get_bolt_grade(self)
            if self.connection == 'Flush End Plate':
                self.stiff_ht = 0.0
                self.stiff_wt = 0.0
                self.t_s = 0.0
                self.weld_type = "None"
                if self.design_status:
                    logger.info(": Overall Column end plate connection design is safe \n")
                    logger.debug(" :=========End Of design===========")
                else:
                    logger.error(": Design is not safe \n ")
                    logger.debug(" :=========End Of design===========")
            else:
                # if 2 * self.end_dist >= 50:
                self.stiffener_details(self)
                # else:
                #     self.stiff_ht = 0.0
                #     self.stiff_wt = 0.0
                #     self.t_s = 0.0
                #     self.weld_type = "None"
            # self.design_status = True
            # self.plate_details(self)

        else:
            previous_diam = (self.bolt_diam_provided)
            print(type(self.bolt_diam_provided))
            self.get_bolt_diam(self,previous_diam)
            # self.design_status = False
            # logger.error("Plate thickness provided is not satisfied")

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('End Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'End Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Connector", bgcolor)

##########################################################################################
             ####   Stiffener details   ####
##########################################################################################
    def stiffener_details(self):
        gamma_m0 = 1.1
        gamma_mw = 1.25
        k = 0.7

        self.m_s = self.t_b * self.end_dist

        self.n = 10

        self.a = 196
        self.b = -25 * self.n
        self.c = self.n ** 2
        self.d = (self.t_b * self.end_dist * 4 * gamma_m0)/self.plate.fy

        coeff = [self.a,self.b,self.c,self.d]

        self.t_s = np.roots(coeff)
        self.t_s = math.ceil(np.amax(self.t_s))

        self.h_s = 14 * self.t_s

        flange_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(self.section.flange_thickness, self.t_s)
        flange_weld_throat_size = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=flange_weld_size_min, fusion_face_angle=90)
        flange_weld_throat_max = IS800_2007.cl_10_5_3_1_max_weld_throat_thickness(self.section.flange_thickness,
                                                                                  self.t_s)

        self.weld_length_avail = 2 * self.h_s - 2 * self.n

        self.weld_force_shear = (self.factored_shear_load/1000)/(2 * flange_weld_throat_size * self.weld_length_avail)

        self.weld_force_moment = (self.factored_moment/1000)/((self.weld_length_avail ** 3 * flange_weld_throat_size)/6)

        # capacity_unit_flange is the capacity of weld of unit throat thickness
        capacity_unit_flange = (k * self.section.fu) / (math.sqrt(3) * gamma_mw)  # N/mm**2 or MPa

        self.resultant = math.sqrt(self.weld_force_shear ** 2 + self.weld_force_moment ** 2)

        self.weld_size = self.resultant/capacity_unit_flange


        if 2*self.end_dist < 50:
            self.stiff_ht = 0.0
            self.stiff_wt = 0.0
            self.t_s = 0.0
            self.weld_type = "None"
            print("< 50 loop")
        else:
            if self.h_s < 100:
                self.h_s = 100
            else:
                self.h_s = self.h_s

            if self.weld_size <= 16:
                self.weld_size_prov = self.weld_size
                self.weld_type = "FILLET"
                self.t_s = self.t_s
                self.stiff_wt = 2 * self.end_dist
                self.stiff_ht = self.h_s
                print(">50, fillet loop")
            else:
                self.t_s = self.t_s
                self.stiff_wt = 2 * self.end_dist
                self.stiff_ht = self.h_s
                self.weld_type = "GROOVE"
                print(">50, groove loop")

        if self.design_status:
            logger.info(": Overall Column end plate connection design is safe \n")
            logger.debug(" :=========End Of design===========")
        else:
            logger.error(": Design is not safe \n ")
            logger.debug(" :=========End Of design===========")

#####################################################################
    ###   Output Dict   ###
#####################################################################

    def results_to_test(self):
        test_input = {KEY_MODULE : self.module,
                      KEY_MAIN_MODULE: self.mainmodule,
                      KEY_DISP_SEC_PROFILE: "ISection",
                      KEY_DISP_BEAMSEC: self.section.designation,
                      KEY_MATERIAL: self.section.material,
                      KEY_SEC_FU: self.section.fu,
                      KEY_SEC_FY: self.section.fy,
                      KEY_D: self.bolt.bolt_diameter,
                      KEY_GRD: self.bolt.bolt_grade,
                      KEY_TYP: self.bolt.bolt_type,
                      KEY_PLATETHK: self.plate.thickness,
                      KEY_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
                      KEY_DP_BOLT_SLIP_FACTOR: self.bolt.mu_f,
                      KEY_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
                      KEY_DP_DETAILING_GAP: self.plate.gap,
                      KEY_DP_DETAILING_CORROSIVE_INFLUENCES: self.bolt.corrosive_influences}

        test_output = {KEY_MEMBER_MOM_CAPACITY: round(self.moment_capacity / 1000000, 2),
                       KEY_MEMBER_SHEAR_CAPACITY: round(self.shear_capacity / 1000, 2),
                       KEY_MEMBER_AXIALCAPACITY: round(self.axial_capacity / 1000, 2),

                       # applied loads
                       KEY_DISP_APPLIED_AXIAL_FORCE: round(self.factored_axial_load / 1000, 2),
                       KEY_DISP_APPLIED_SHEAR_LOAD: round(self.factored_shear_load / 1000, 2),
                       KEY_DISP_APPLIED_MOMENT_LOAD: round(self.factored_moment / 1000000, 2),

                       # bolt_capacity
                       KEY_OUT_BOLT_SHEAR: round(self.bolt.bolt_shear_capacity / 1000, 2),
                       KEY_OUT_BOLT_BEARING: round(self.bolt.bolt_bearing_capacity / 1000, 2),
                       KEY_OUT_BOLT_CAPACITY: round(self.bolt.bolt_capacity / 1000, 2),
                       KEY_OUT_BOLT_TENSION_CAPACITY: round(self.bolt.bolt_tension_capacity / 1000, 2),
                       KEY_Y_SQR: round(self.y_sqr,2),
                       KEY_BOLT_TENSION: round(self.t_b,2),
                       KEY_BOLT_SHEAR: round(self.v_sb,2),

                       # detailng
                       KEY_D: self.bolt_diam_provided,
                       KEY_GRD: self.bolt_grade_provided,
                       KEY_OUT_PITCH: self.pitch,
                       KEY_OUT_END_DIST: self.end_dist,
                       KEY_OUT_NO_BOLTS_WEB: (self.n_bw),
                       KEY_OUT_NO_BOLTS_FLANGE: (self.n_bf),
                       KEY_OUT_NO_BOLTS: round(self.no_bolts),
                       KEY_P2_WEB: self.p_2_web,
                       KEY_P2_FLANGE: self.p_2_flange,

                       # plate
                       KEY_OUT_PLATETHK: self.plate_thickness_provided,
                       KEY_OUT_PLATE_HEIGHT: self.plate_height,
                       KEY_OUT_PLATE_LENGTH: self.plate_width,
                       KEY_OUT_PLATE_MOM_CAPACITY: round(self.m_dp/1000000,2),
                       KEY_PLATE_MOMENT: round(self.m_ep/1000000,2),

                       #stiffener
                       KEY_OUT_STIFFENER_HEIGHT: self.stiff_ht,
                       KEY_OUT_STIFFENER_WIDTH: self.stiff_wt,
                       KEY_OUT_STIFFENER_THICKNESS: self.t_s,
                       KEY_OUT_WELD_TYPE: self.weld_type}
        return test_input, test_output

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    @staticmethod
    def endplate_thick_customized():
        d = VALUES_COLUMN_ENDPLATE_THICKNESS_CUSTOMIZED
        return d

    @staticmethod
    def limiting_width_thk_ratio(column_f_t, column_t_w, column_d, column_b, column_fy, factored_axial_force,
                                 column_area, compression_element, section):

        epsilon = float(math.sqrt(250 / column_fy))
        axial_force_w = int(
            ((column_d - 2 * (column_f_t)) * column_t_w * factored_axial_force) / (column_area))  # N

        des_comp_stress_web = column_fy
        des_comp_stress_section = column_fy
        avg_axial_comp_stress = axial_force_w / ((column_d - 2 * column_f_t) * column_t_w)
        r1 = avg_axial_comp_stress / des_comp_stress_web
        r2 = avg_axial_comp_stress / des_comp_stress_section
        a = column_b / column_f_t
        # compression_element=["External","Internal","Web of an I-H" ,"box section" ]
        # section=["rolled","welded","compression due to bending","generally", "Axial compression" ]
        # section = "rolled"
        if compression_element == "External" or compression_element == "Internal":
            if section == "Rolled":
                if column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 10.5 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 15.7 * epsilon:
                #     class_of_section1 = "semi-compact"
                else:
                      class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
                # print("class_of_section", class_of_section )
            elif section == "welded":
                if column_b * 0.5 / column_f_t <= 8.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 13.6 * epsilon:
                #     class_of_section1 = "semi-compact"
                else:
                      class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            elif section == "compression due to bending":
                if column_b * 0.5 / column_f_t <= 29.3 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 33.5 * epsilon:
                    class_of_section1 = "compact"
                # elif column_b * 0.5 / column_f_t <= 42 * epsilon:
                #     class_of_section1 = "semi-compact"
                else:
                      class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            # else:
            #     pass

        elif compression_element == "Web of an I-H" or compression_element == "box section":
            if section == "generally":
                if r1 < 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= (max(105 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "compact"
                    # elif column_d / column_t_w <= max((126 * epsilon / (1 + 2 * r1)), column_d / column_t_w >= (
                    #         42 * epsilon)):
                    #     class_of_section1 = "semi-compact"
                    else:
                        class_of_section1 = "semi-compact"
                    # else:
                    #     print('fail')
                    # print("class_of_section3", class_of_section)
                elif r1 > 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= max((105 * epsilon / (1 + (r1 * 1.5))), (
                            42 * epsilon)):
                        class_of_section1 = "compact"
                    else:
                        class_of_section1 = "semi-compact"
                    # elif column_d / column_t_w <= max((126 * epsilon / (1 + 2 * r1)), (
                    #                     #         42 * epsilon)):
                    #                     #     class_of_section1 = "semi-compact"
                    # else:
                    #     self.design_status ==False
                    #     # print(self.design_status,"reduce Axial Force")
                    #     logger.warning(
                    #         ": Reduce Axial Force, web is slender under given forces")
                    # else:
                    #     print('fail')
                    # print("class_of_section4", class_of_section)
            elif section == "Axial compression":
                if column_d / column_t_w <= (42 * epsilon):
                    class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "N/A"
        #     else:
        #         print('fail')
        # else:
        #     pass
        print("class_of_section", class_of_section1)
        if class_of_section1 == "plastic":
            class_of_section1 = 1
        elif class_of_section1 == "compact":
            class_of_section1 = 2
        elif class_of_section1 == "semi-compact":
            class_of_section1 = 3
        # else:
        #     print('fail')
        print("class_of_section2", class_of_section1)

        return class_of_section1

        # print("class_of_section1", class_of_section1)

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        t6 = (KEY_PLATETHK, self.endplate_thick_customized)
        list1.append(t6)
        return list1
        ################################ Design Report #####################################################################################


# def save_design(self, popup_summary):
    def save_design(self, popup_summary):

        self.report_supporting = {KEY_DISP_SEC_PROFILE: "ISection",
                                  KEY_DISP_BEAMSEC: self.section.designation,
                                  KEY_DISP_MATERIAL: self.section.material,
                                  KEY_DISP_FU: self.section.fu,
                                  KEY_DISP_FY: self.section.fy,
                                  'Mass': self.section.mass,
                                  'Area(mm2) - A': round(self.section.area, 2),
                                  'D(mm)': self.section.depth,
                                  'B(mm)': self.section.flange_width,
                                  't(mm)': self.section.web_thickness,
                                  'T(mm)': self.section.flange_thickness,
                                  'FlangeSlope': self.section.flange_slope,
                                  'R1(mm)': self.section.root_radius,
                                  'R2(mm)': self.section.toe_radius,
                                  'Iz(mm4)': self.section.mom_inertia_z,
                                  'Iy(mm4)': self.section.mom_inertia_y,
                                  'rz(mm)': self.section.rad_of_gy_z,
                                  'ry(mm)': self.section.rad_of_gy_y,
                                  'Zz(mm3)': self.section.elast_sec_mod_z,
                                  'Zy(mm3)': self.section.elast_sec_mod_y,
                                  'Zpz(mm3)': self.section.plast_sec_mod_z,
                                  'Zpy(mm3)': self.section.elast_sec_mod_y}

        self.report_input = \
            {KEY_MODULE: self.module,
             KEY_MAIN_MODULE: self.mainmodule,
             # KEY_CONN: self.connectivity,
             KEY_DISP_MOMENT: self.load.moment,
             KEY_DISP_SHEAR: self.load.shear_force,
             KEY_DISP_AXIAL: self.load.axial_force,

             "Section": "TITLE",
             "Section Details": self.report_supporting,

             "Bolt Details": "TITLE",
             KEY_DISP_D: str(self.bolt.bolt_diameter),
             KEY_DISP_GRD: str(self.bolt.bolt_grade),
             KEY_DISP_TYP: self.bolt.bolt_type,


             KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
             KEY_DISP_DP_BOLT_SLIP_FACTOR: self.bolt.mu_f,
             KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
             KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES: self.bolt.corrosive_influences}

        self.report_check = []

        bolt_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2)
        bolt_shear_capacity_kn = round(self.bolt.bolt_shear_capacity / 1000, 2)
        kb_disp = round(self.bolt.kb, 2)

        t1 = ('SubSection', 'Member Capacity', '|p{4cm}|p{4cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        t1 = (KEY_OUT_DISP_AXIAL_CAPACITY, '', axial_capacity(area=self.section.area,
                                                              fy=self.section.fy,
                                                              gamma_m0=gamma_m0,
                                                              axial_capacity=round(self.axial_capacity / 1000, 2)), '')
        self.report_check.append(t1)
        h = (self.section.depth - (2 * self.section.flange_thickness))
        t1 = (KEY_OUT_DISP_SHEAR_CAPACITY, '', shear_capacity(h=h, t=self.section.web_thickness,
                                                              f_y=self.section.fy, gamma_m0=gamma_m0,
                                                              shear_capacity=round(self.shear_capacity / 1000 ,2)), '')
        self.report_check.append(t1)
        if self.class_of_section == 1 or self.class_of_section == 2:

            t1 = (KEY_OUT_DISP_MOMENT_CAPACITY, '', moment_cap(beta=1,m_d=round(self.moment_capacity /1000,2),f_y=self.section.fy,
                                                           gamma_m0=gamma_m0,m_fd=round(self.factored_moment/1000,2),
                                                           mom_cap=round(self.moment_capacity/1000,2)),'')
            self.report_check.append(t1)
        else:
            t1 = (KEY_OUT_DISP_MOMENT_CAPACITY, '', moment_CAP( m_d=round(self.moment_capacity/1000,2), f_y=self.section.fy,
                                                               gamma_m0=gamma_m0,Z_e=self.Z_e,
                                                                mom_cap=round(self.moment_capacity/1000,2)), '')
            self.report_check.append(t1)

        t1 = ('SubSection', 'Load Considered', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        t1 = (KEY_DISP_APPLIED_AXIAL_FORCE, min_max_axial_capacity(axial_capacity=round(self.axial_capacity / 1000, 2),
                                                                  min_ac=round(self.min_axial_load / 1000, 2)),
             prov_axial_load(axial_input=self.load.axial_force,
                             min_ac=round(self.min_axial_load / 1000, 2),
                             app_axial_load=round(self.factored_axial_load / 1000, 2)),
             get_pass_fail(self.min_axial_load / 1000,
                           self.factored_axial_load / 1000, relation="leq"))
        self.report_check.append(t1)
        t1 = (KEY_DISP_APPLIED_SHEAR_LOAD, min_max_shear_capacity(shear_capacity=round(self.shear_capacity / 1000, 2),
                                                                 min_sc=round(self.min_shear_load / 1000, 2)),
             prov_shear_load(shear_input=self.load.shear_force,
                             min_sc=round( self.min_shear_load / 1000, 2),
                             app_shear_load=round(self.fact_shear_load / 1000, 2)),
             get_pass_fail(self.min_shear_load  / 1000,
                           self.fact_shear_load / 1000, relation="leq"))
        self.report_check.append(t1)

        t1 = (KEY_DISP_APPLIED_MOMENT_LOAD,
             min_max_moment_capacity(moment_capacity=round(self.moment_capacity / 1000000, 2),
                                     min_mc=round(self.min_moment / 1000000, 2)),
             prov_moment_load(moment_input=self.load.moment,
                              min_mc=round(self.min_moment / 1000000, 2),
                              app_moment_load=round(self.factored_moment / 1000000, 2)),
             get_pass_fail(round(self.min_moment / 1000000, 2),
                           round(self.load.moment / 1000000, 2), relation="leq"))
        self.report_check.append(t1)



        t1 = ('SubSection', ' Bolt Checks', '|p{4cm}|p{6.5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_D_PROVIDED, "Bolt Quantity Optimisation", display_prov(self.bolt_diam_provided, "d"), '')
        self.report_check.append(t1)

        t1 = (KEY_OUT_DISP_GRD_PROVIDED, "Bolt Grade Optimisation", self.bolt_grade_provided, '')
        self.report_check.append(t1)

        t1 = (KEY_DISP_BOLT_HOLE, " ", display_prov(self.bolt.dia_hole, "d_0"), '')
        self.report_check.append(t1)


        if self.bolt.bolt_type == TYP_BEARING:
             bolt_bearing_capacity_kn = round(self.bolt.bolt_bearing_capacity / 1000, 2)
             t1 = (KEY_OUT_DISP_BOLT_SHEAR, '', bolt_shear_prov(self.bolt.bolt_fu, 1,
                                                                          self.bolt.bolt_net_area,
                                                                          self.bolt.gamma_mb,
                                                                          bolt_shear_capacity_kn), '')
             self.report_check.append(t1)
             t2 = (KEY_OUT_DISP_BOLT_BEARING, '', bolt_bearing_prov(kb_disp,
                                                                              self.bolt.bolt_diameter_provided,
                                                                              self.bolt_conn_plates_t_fu_fy,
                                                                              self.bolt.gamma_mb,
                                                                              bolt_bearing_capacity_kn), '')
             self.report_check.append(t2)
             t3 = (KEY_OUT_DISP_BOLT_CAPACITY, '', bolt_capacity_prov(bolt_shear_capacity_kn,
                                                                                bolt_bearing_capacity_kn,
                                                                                bolt_capacity_kn), '')
             self.report_check.append(t3)
        else:

             t4 = (KEY_OUT_DISP_BOLT_SLIP, '', HSFG_bolt_capacity_prov(mu_f=self.bolt.mu_f, n_e=1,
                                                                                 K_h=0.3,
                                                                                 fub=self.bolt.bolt_fu,
                                                                                 Anb=self.bolt.bolt_net_area,
                                                                                 gamma_mf=self.bolt.gamma_mf,
                                                                                 capacity=bolt_capacity_kn), '')
             self.report_check.append(t4)
        t1 = (KEY_OUT_BOLT_TENSION_CAPACITY, tension_in_bolt_due_to_axial_load_n_moment(P=round(self.factored_axial_load /1000,2),
                                                                                        n=self.no_bolts,
                                                                                        M=round(self.factored_moment/1000,2),
                                                                                        y_max=self.y_max,
                                                                                        y_sqr=round(self.y_sqr ,2),T_b=round(self.t_b/1000 ,2)) ,
               tension_capacity_of_bolt(f_ub=self.bolt.bolt_fu,A_nb=self.bolt.bolt_net_area,T_db=round(self.bolt.bolt_tension_capacity /1000 ,2)),
               get_pass_fail(self.t_b,self.bolt.bolt_tension_capacity,relation='leq'))
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_BOLT_SHEAR,shear_force_in_bolts_near_web(V=round(self.factored_shear_load /1000 ,2),n_wb=self.n_bw,V_sb=round(self.v_sb /1000, 2)),
                 round(self.bolt.bolt_capacity /1000,2),
                 get_pass_fail(round(self.v_sb/1000,2) , round(self.bolt.bolt_capacity/1000, 2) , relation='leq'))
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_NO_BOLTS_WEB, no_of_bolts_along_web(D=self.section.depth,T_f=self.section.flange_thickness,e=self.end_dist,
                                                               p=self.pitch,n_bw=self.n_bw),
                self.n_bw,

                get_pass_fail(self.n_bw,self.n_bw,relation='leq'))
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_NO_BOLTS_FLANGE,
              no_of_bolts_along_flange(b=self.section.flange_width, T_w=self.section.web_thickness, e=self.end_dist,
                                    p=self.pitch, n_bf=self.n_bf),
              self.n_bf,

              get_pass_fail(self.n_bf, self.n_bf, relation='leq'))
        self.report_check.append(t1)

        t1 = (DISP_MIN_PITCH, min_pitch(self.bolt.bolt_diameter_provided),
              self.pitch,
              get_pass_fail(self.bolt.min_pitch, self.pitch, relation='lesser'))
        self.report_check.append(t1)
        t1 = (DISP_MAX_PITCH ,max_pitch(self.plate.thickness),
              self.pitch,
              get_pass_fail(self.bolt.max_spacing, self.pitch, relation='greater'))
        self.report_check.append(t1)
        t3 = (DISP_MIN_END, min_edge_end(self.bolt.dia_hole, self.bolt.edge_type),
              self.end_dist,
              get_pass_fail(self.bolt.min_end_dist, self.end_dist,
                            relation='lesser'))
        self.report_check.append(t3)
        t4 = (DISP_MAX_END, max_edge_end(self.plate.fy, self.plate_thickness_provided),
              self.end_dist,
              get_pass_fail(self.bolt.max_end_dist, self.end_dist,
                            relation='greater'))
        self.report_check.append(t4)
        t1 = ('SubSection', '  End plate Checks', '|p{4cm}|p{6cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        if self.connection == "Flush End Plate":

              t1 = (DISP_MIN_PLATE_LENGTH,self.section.depth,
                  self.plate_height,
                  get_pass_fail(self.section.depth, self.plate_height, relation="leq"))
              self.report_check.append(t1)
        else:

              t1 = (DISP_MIN_PLATE_LENGTH, end_plate_ht_req(D=self.section.depth, e=self.end_dist, h_p=self.plate_height),
                  self.plate_height,
                  get_pass_fail(self.plate_height, self.plate_height, relation="leq"))
              self.report_check.append(t1)
        t1 = (DISP_MIN_PLATE_HEIGHT, self.section.flange_width,
                                            self.plate_width,
              get_pass_fail(self.section.flange_width, self.plate_width, relation="leq"))
        self.report_check.append(t1)
        t1 = (DISP_MIN_PLATE_THICK,end_plate_thk_req(M_ep=round(self.m_ep ,2),b_eff=self.b_eff,f_y=self.plate.fy,gamma_m0=gamma_m0,t_p=self.plate_thickness_provided),
               self.plate_thickness_provided,
               get_pass_fail(self.plate.thickness_provided,  self.plate_thickness_provided, relation="leq"))
        self.report_check.append(t1)
        if self.pitch >= 2*self.end_dist:

            t1=(KEY_OUT_DISP_PLATE_MOM_CAPACITY,moment_acting_on_end_plate(M_ep=round(self.m_ep, 2), b_eff=2*self.end_dist, f_y=self.plate.fy, gamma_m0=gamma_m0,
                              t_p=self.plate_thickness_provided),
              design_capacity_of_end_plate(M_dp=round(self.m_dp, 2), b_eff=self.b_eff, f_y=self.plate.fy, gamma_m0=gamma_m0,
                              t_p=self.plate_thickness_provided),
                get_pass_fail(self.m_ep, self.m_dp, relation="leq"))


            self.report_check.append(t1)
        else:
            t1 = (KEY_OUT_DISP_PLATE_MOM_CAPACITY,moment_acting_on_end_plate(M_ep=round(self.m_ep, 2), b_eff=self.pitch, f_y=self.plate.fy, gamma_m0=gamma_m0,
                              t_p=self.plate_thickness_provided),
              design_capacity_of_end_plate(M_dp=round(self.m_dp, 2), b_eff=self.b_eff, f_y=self.plate.fy, gamma_m0=gamma_m0,
                              t_p=self.plate_thickness_provided),
                get_pass_fail(self.m_ep, self.m_dp, relation="leq"))

            self.report_check.append(t1)

        if self.connection == "Extended Both Ways":

               t1 = ('SubSection', '   Stiffener Checks', '|p{4cm}|p{6cm}|p{5.5cm}|p{1.5cm}|')
               self.report_check.append(t1)
               t1 = (KEY_OUT_DISP_STIFFENER_HEIGHT,self.section.depth,
                       self.stiff_ht,
               get_pass_fail(self.section.depth, self.stiff_ht, relation="geq"))
               self.report_check.append(t1)
               t1 = (KEY_OUT_DISP_STIFFENER_WIDTH,end_plate_ht_req(D=self.section.depth, e=self.end_dist, h_p=self.plate_height),

                     self.stiff_wt,
                     get_pass_fail(self.plate_height, self.stiff_wt, relation="geq"))
               self.report_check.append(t1)
               t1 = ( KEY_OUT_DISP_STIFFENER_THICKNESS, '',  self.t_s,'')
               self.report_check.append(t1)
               t1 = (KEY_OUT_DISP_WELD_TYPE, '', self.weld_type, '')
               self.report_check.append(t1)

        else:
               pass

        Disp_3d_image = "/ResourceFiles/images/3d.png"

        # config = configparser.ConfigParser()
        # config.read_file(open(r'Osdag.config'))
        # desktop_path = config.get("desktop_path", "path1")
        # print("desk:", desktop_path)
        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")

        fname_no_ext = popup_summary['filename']

        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                                   rel_path, Disp_3d_image)


# def save_latex(self, uiObj, Desigxn_Check, reportsummary, filename, rel_path, Disp_3d_image):
