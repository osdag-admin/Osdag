from design_type.connection.moment_connection import MomentConnection
from utils.common.component import *
from Common import *
from utils.common.load import Load
import logging


class BeamColumnEndPlate(MomentConnection):

    def __init__(self):
        super(BeamColumnEndPlate, self).__init__()


    ###############################################
    # Design Preference Functions Start
    ###############################################

    def tab_list(self):
        tabs = []

        t1 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_supporting_section)
        tabs.append(t1)

        t1 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_supported_section)
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

    def edit_tabs(self):
        return []

    def tab_value_changed(self):

        change_tab = []

        t1 = (KEY_DISP_COLSEC, [KEY_SUPTNGSEC_MATERIAL], [KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY], TYPE_TEXTBOX,
        self.get_fu_fy_I_section_suptng)
        change_tab.append(t1)

        t2 = (KEY_DISP_BEAMSEC, [KEY_SUPTDSEC_MATERIAL], [KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY], TYPE_TEXTBOX,
        self.get_fu_fy_I_section_suptd)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)

        change_tab.append(t3)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20','Label_21','Label_22'], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20','Label_21','Label_22'], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        return change_tab

    def refresh_input_dock(self):

        add_buttons = []

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, None, None, "Columns")
        add_buttons.append(t1)

        t2 = (KEY_DISP_BEAMSEC, KEY_SUPTDSEC, TYPE_COMBOBOX, KEY_SUPTDSEC, None, None, "Beams")
        add_buttons.append(t2)

        return add_buttons

    def input_dictionary_design_pref(self):
        design_input = []
        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, [KEY_SUPTNGSEC_MATERIAL])
        design_input.append(t1)

        t2 = (KEY_DISP_BEAMSEC, TYPE_COMBOBOX, [KEY_SUPTDSEC_MATERIAL])
        design_input.append(t2)

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
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SUPTNGSEC_MATERIAL, KEY_SUPTDSEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_MATERIAL_G_O, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_WELD_FAB, KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_GAP,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    ####################################
    # Design Preference Functions End
    ####################################
    # Setting up logger and Input and Output Docks
    ####################################

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """
        # @author Arsil Zunzunia
        # super(FinPlateConnection, FinPlateConnection).set_osdaglogger(key)
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

    def module_name(self):
        return KEY_DISP_BCENDPLATE

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)

        e.g.
        t = (Key, Key_display, Type, Current_Value, enabled/disabled, Validator_type)
        '''

        # @author: Amir, Umair
        self.module = KEY_DISP_BCENDPLATE

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_FINPLATE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, VALUES_CONN, True, 'No Validator')
        options_list.append(t2)

        t2 = (KEY_ENDPLATE_TYPE, KEY_DISP_ENDPLATE_TYPE, TYPE_COMBOBOX, VALUES_ENDPLATE_TYPE, True, 'No Validator')
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, "./ResourceFiles/images/cf_bw_flush.png", True, 'No Validator')
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, connectdb("Columns"), True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, connectdb("Beams"), True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None,True, 'Int Validator')
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

        t23 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t23)

        t24 = (KEY_WELD_TYPE, KEY_DISP_WELD_TYPE, TYPE_COMBOBOX, VALUES_WELD_TYPE_EP, True, 'No Validator')
        options_list.append(t24)

        return options_list

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_CONN, KEY_ENDPLATE_TYPE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t1)

        t2 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t2)

        return lst

    def fn_conn_image(self):
        conn = self[0]
        ep_type = self[1]
        if conn == 'Column flange-Beam web' and ep_type == 'Flush End Plate':
            return './ResourceFiles/images/cf_bw_flush.png'
        elif conn == 'Column flange-Beam web' and ep_type == 'Extended One Way':
            return './ResourceFiles/images/cf_bw_eow.png'
        elif conn in 'Column flange-Beam web' and ep_type == 'Extended Both Ways':
            return './ResourceFiles/images/cf_bw_ebw.png'
        elif conn == 'Column web-Beam web' and ep_type == 'Flush End Plate':
            return './ResourceFiles/images/cw_bw_flush.png'
        elif conn == 'Column web-Beam web' and ep_type == 'Extended One Way':
            return './ResourceFiles/images/cw_bw_eow.png'
        elif conn in 'Column web-Beam web' and ep_type == 'Extended Both Ways':
            return './ResourceFiles/images/cw_bw_ebw.png'
        else:
            return ''

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        t6 = (KEY_PLATETHK, self.endplate_thick_customized)
        list1.append(t6)
        return list1

    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair

        out_list = []
        return []

    def set_input_values(self, design_dictionary):
        self.mainmodule = "Moment Connection"
        self.connectivity = design_dictionary[KEY_CONN]
        self.material = Material(material_grade=design_dictionary[KEY_MATERIAL])

        self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC],
                                             material_grade=design_dictionary[KEY_SUPTNGSEC_MATERIAL])

        self.supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC],
                                      material_grade=design_dictionary[KEY_SUPTDSEC_MATERIAL])
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                         bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])

        self.load = Load(shear_force=design_dictionary[KEY_SHEAR],
                         axial_force=design_dictionary[KEY_AXIAL],moment=design_dictionary[KEY_MOMENT])

        self.plate = Plate(thickness=design_dictionary.get(KEY_PLATETHK, None),
                           material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],
                           gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.plate.design_status_capacity = False
        self.top_flange_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                         fabrication=design_dictionary[KEY_DP_WELD_FAB])     # TODO: Add weld type in design dictionary
        self.bottom_flange_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                                     fabrication=design_dictionary[
                                         KEY_DP_WELD_FAB])  # TODO: Add weld type in design dictionary
        self.web_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                         fabrication=design_dictionary[KEY_DP_WELD_FAB])
        print("input values are set. Doing preliminary member checks")
        self.warn_text()
        # self.member_capacity()
    ############################################################################################
    # DESIGN STARTS
    ############################################################################################

    # TODO: Do I need to check moment capacity of beam. It will be complete beam design.
    '''
    def member_capacity(self):
        """Check for the moment carrying capacity of beam"""
        
        # Rolled beam
        if self.supported_section.type == "Rolled":
            length = self.supported_section.depth
        # Welded beam
        else:
            length = self.supported_section.depth - (2*self.supported_section.flange_thickness)    # -(2*self.supported_section.root_radius)
        
        # self.supported_section.shear_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.shear_yielding_capacity = round(IS800_2007.cl_8_4_design_shear_strength(
            length*self.supported_section.web_thickness, self.supported_section.fy) / 1000, 2)
        # self.supported_section.tension_yielding(length=length, thickness=self.supported_section.web_thickness, fy=self.supported_section.fy)
        self.supported_section.tension_yielding_capacity = round(IS800_2007.cl_6_2_tension_yielding_strength(
            length*self.supported_section.web_thickness, self.supported_section.fy) / 1000, 2)
        if self.load.shear_force <= min(0.15 * self.supported_section.shear_yielding_capacity, 40.0):
            logger.warning(" : User input for shear force is very less compared to section capacity. "
                "Setting Shear Force value to 15% of supported beam shear capacity or 40kN, whichever is less.")
            self.load.shear_force = min(0.15 * self.supported_section.shear_yielding_capacity, 40.0)

        if self.supported_section.shear_yielding_capacity > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity > self.load.axial_force:
            print("preliminary member check is satisfactory. Doing bolt checks")
            self.design_status = True
            self.select_bolt_plate_arrangement(self)
        else:
            self.design_status = False
            logger.error(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
                           "than applied loads, Please select larger sections or decrease loads"
                            .format(self.supported_section.shear_yielding_capacity,
                                    self.supported_section.tension_yielding_capacity))
            print("failed in preliminary member checks. Select larger sections or decrease loads")
        '''

    # Check for minimum Design Action (Cl. 10.7, IS 800:2007) #TODO:  Correction for plastic moment capacity
    def check_minimum_design_action(self):
        beam_moment = 1.2 * self.supported_section.plast_sec_mod_z * self.supported_section.fy / 1.10 #TODO use predefined function
        min_connection_moment = 0.5 * beam_moment #TODO use predefined function
        if self.load.moment < min_connection_moment:
            min_connection_moment_kNm = round((min_connection_moment/1e6), 3)
            # logger.warning(": The connection is designed for %s kNm (Cl. 10.7, IS 800:2007)" % min_connection_moment_kNm) #TODO
            self.load.moment = min_connection_moment

    def check_compatibility(self):

        # Column web connectivity
        column_clear_d = self.supporting_section.depth - 2*self.supporting_section.flange_thickness \
                         - 2*self.supporting_section.root_radius    # TODO Make it clear depth:
        if self.connectivity is VALUES_CONN_1[1]:
            if self.supported_section.flange_width > column_clear_d:
                self.design_status = False  #TODO Check self.design_status
                logger.error(": Beam is wider than column clear depth")
                logger.warning(": Width of beam should be less than %s mm" % column_clear_d)
                logger.info(": Currently, Osdag doesn't design such connections")

        # Column flange connectivity
        else:
            if self.supported_section.flange_width > self.supporting_section.flange_width:
                self.design_status = False
                logger.error(": Beam is wider than column width")
                logger.warning(": Width of beam should be less than %s mm" % self.supporting_section.flange_width)
                logger.info(": Currently, Osdag doesn't design such connections")

    def compression_flange(self):
        # Strength of flange under compression or tension TODO: Get function from IS 800

        A_f = beam_B * beam_tf  # area of beam flange
        capacity_beam_flange = (beam_fy / gamma_m0) * A_f
        force_flange = max(t_bf, p_bf)

        if capacity_beam_flange < force_flange:
            # design_status = False
            logger.error(": Forces in the beam flange is greater than its load carrying capacity")
            logger.warning(": The maximum allowable force on beam flange of selected section is %2.2f kN"
                           % (round(capacity_beam_flange / 1000, 3)))
            logger.info(": Use a higher beam section with wider and/or thicker flange")


    def find_bolt_conn_plates_t_fu_fy(self):
        self.bolt_conn_plates_t_fu_fy = [(self.plate.thickness_provided, self.plate.fu, self.plate.fy)]
        # Column web connectivity
        if self.connectivity is VALUES_CONN_1[1]:
            self.bolt_conn_plates_t_fu_fy.append(
                (self.supported_section.web_thickness, self.supported_section.fu, self.supported_section.fy))
        else:
            self.bolt_conn_plates_t_fu_fy.append(
                (self.supported_section.flange_thickness, self.supported_section.fu, self.supported_section.fy))

    def bolt_design(self):
        #######################################################################
        # Calculate bolt capacities

        if bolt_type == "Friction Grip Bolt":
            bolt_slip_capacity = IS800_2007.cl_10_4_3_bolt_slip_resistance(
                f_ub=bolt_fu, A_nb=bolt_net_area, n_e=1, mu_f=mu_f, bolt_hole_type=bolt_hole_type)
            bolt_tension_capacity = IS800_2007.cl_10_4_5_friction_bolt_tension_resistance(
                f_ub=bolt_fu, f_yb=bolt_fy, A_sb=bolt_shank_area, A_n=bolt_net_area)
            bearing_capacity = 0.0
            bolt_shear_capacity = 0.0
            bolt_capacity = bolt_slip_capacity

        else:
            bolt_shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity(
                f_u=bolt_fu, A_nb=bolt_net_area, A_sb=bolt_shank_area, n_n=1, n_s=0)
            bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
                f_u=min(column_fu, end_plate_fu), f_ub=bolt_fu, t=sum(bolt_plates_tk), d=bolt_dia, e=edge_dist,
                p=pitch_dist, bolt_hole_type=bolt_hole_type)
            bolt_slip_capacity = 0.0
            bolt_capacity = min(bolt_shear_capacity, bearing_capacity)
            bolt_tension_capacity = IS800_2007.cl_10_3_5_bearing_bolt_tension_resistance(
                f_ub=bolt_fu, f_yb=bolt_fy, A_sb=bolt_shank_area, A_n=bolt_net_area)

        #######################################################################

        # Calculation for number of bolts around tension flange
        flange_tension = factored_moment / (beam_d - beam_tf) + factored_axial_load / 2
        no_tension_side_rqd = flange_tension / (0.80 * bolt_tension_capacity)
        no_tension_side = round_up(no_tension_side_rqd, multiplier=2, minimum_value=2)

        b_e = beam_B / 2
        prying_force = IS800_2007.cl_10_4_7_bolt_prying_force(
            T_e=flange_tension / 4, l_v=l_v, f_o=0.7 * bolt_fu, b_e=b_e, t=end_plate_thickness, f_y=end_plate_fy,
            end_dist=end_dist, pre_tensioned=False)

        # Detailing
        bolt_combined_status = False
        detailing_status = True
        while bolt_combined_status is False:

            if endplate_type == 'flush':
                number_of_bolts = 2 * no_tension_side

                if no_tension_side == 2:
                    no_rows = {'out_tension_flange': 0, 'in_tension_flange': 1,
                               'out_compression_flange': 0, 'in_compression_flange': 1}
                    if beam_d - 2 * beam_tf - 2 * l_v < pitch_dist:
                        detailing_status = False

                elif no_tension_side == 4:
                    no_rows = {'out_tension_flange': 0, 'in_tension_flange': 2,
                               'out_compression_flange': 0, 'in_compression_flange': 2}
                    if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # # logger.warning()
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                        # TODO Re-detail the connection
                        # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                        #            'out_compression_flange': 2, 'in_compression_flange': 1}

                elif no_tension_side == 6:
                    no_rows = {'out_tension_flange': 0, 'in_tension_flange': 3,
                               'out_compression_flange': 0, 'in_compression_flange': 3}
                    if beam_d - 2 * beam_tf - 2 * l_v < 5 * pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                        #  Re-detail the connection
                        # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
                        #            'out_compression_flange': 3, 'in_compression_flange': 1}

                else:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")
                    no_rows = {'out_tension_flange': (no_tension_side - 6) / 2, 'in_tension_flange': 2,
                               'out_compression_flange': (no_tension_side - 6) / 2, 'in_compression_flange': 2}

                # #######################################################################

            elif endplate_type == 'one_way':
                number_of_bolts = no_tension_side + 2
                if no_tension_side <= 4:
                    no_tension_side = 4
                    number_of_bolts = no_tension_side + 2
                    no_rows = {'out_tension_flange': 1, 'in_tension_flange': 1,
                               'out_compression_flange': 0, 'in_compression_flange': 1}
                    if beam_d - 2 * beam_tf - 2 * l_v < pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # # logger.warning()
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                        #  Re-detail the connection
                        # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                        #            'out_compression_flange': 0, 'in_compression_flange': 1}

                elif no_tension_side == 6:
                    no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
                               'out_compression_flange': 0, 'in_compression_flange': 1}
                    if beam_d - 2 * beam_tf - 2 * l_v < 2 * pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # # logger.warning()
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                        #  Re-detail the connection
                        # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                        #            'out_compression_flange': 0, 'in_compression_flange': 1}

                elif no_tension_side == 8:
                    no_rows = {'out_tension_flange': 1, 'in_tension_flange': 3,
                               'out_compression_flange': 0, 'in_compression_flange': 1}
                    if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                        #  Re-detail the connection
                        # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
                        #            'out_compression_flange': 0, 'in_compression_flange': 1}
                elif no_tension_side == 10:
                    no_rows = {'out_tension_flange': 2, 'in_tension_flange': 3,
                               'out_compression_flange': 0, 'in_compression_flange': 1}
                    if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                else:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")
                    no_rows = {'out_tension_flange': (no_tension_side - 6) / 2, 'in_tension_flange': 2,
                               'out_compression_flange': (no_tension_side - 6) / 2, 'in_compression_flange': 2}

                # #######################################################################

            else:  # endplate_type == "both_way":
                number_of_bolts = 2 * no_tension_side

                if no_tension_side <= 4:
                    no_tension_side = 4
                    number_of_bolts = 2 * no_tension_side
                    no_rows = {'out_tension_flange': 1, 'in_tension_flange': 1,
                               'out_compression_flange': 1, 'in_compression_flange': 1}
                    if beam_d - 2 * beam_tf - 2 * l_v < pitch_dist:
                        detailing_status = False

                elif no_tension_side == 6:
                    no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
                               'out_compression_flange': 1, 'in_compression_flange': 2}
                    if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # # logger.warning()
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                        #  Re-detail the connection
                        # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                        #            'out_compression_flange': 2, 'in_compression_flange': 1}

                elif no_tension_side == 8:
                    no_rows = {'out_tension_flange': 1, 'in_tension_flange': 3,
                               'out_compression_flange': 1, 'in_compression_flange': 3}
                    if beam_d - 2 * beam_tf - 2 * l_v < 5 * pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                        #  Re-detail the connection
                        # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
                        #            'out_compression_flange': 3, 'in_compression_flange': 1}
                elif no_tension_side == 10:
                    no_rows = {'out_tension_flange': 2, 'in_tension_flange': 3,
                               'out_compression_flange': 2, 'in_compression_flange': 3}
                    if beam_d - 2 * beam_tf - 2 * l_v < 5 * pitch_dist:
                        detailing_status = False
                        # logger.error("Large number of bolts are required for the connection")
                        # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                else:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")
                    no_rows = {'out_tension_flange': (no_tension_side - 6) / 2, 'in_tension_flange': 2,
                               'out_compression_flange': (no_tension_side - 6) / 2, 'in_compression_flange': 2}

                # #######################################################################

                # Plate height and width
                ''' tens_plate_no_pitch : projection of end plate beyond the beam flange excluding the 
                                            distances b/w bolts on tension side '''
            if no_rows['out_tension_flange'] == 0:
                tens_plate_outer = flange_projection
            else:
                tens_plate_outer = end_dist + l_v + (no_rows['out_tension_flange'] - 1) * pitch_dist
            if no_rows['out_compression_flange'] == 0:
                comp_plate_outer = flange_projection
            else:
                comp_plate_outer = end_dist + l_v + (no_rows['out_compression_flange'] - 1) * pitch_dist

            plate_height = beam_d + comp_plate_outer + tens_plate_outer
            plate_width = g_1 + 2 * edge_dist
            while plate_width < beam_B:
                edge_dist += 5
                plate_width = g_1 + 2 * edge_dist
                if edge_dist > edge_dist_max:
                    edge_dist -= 5
                    g_1 += 5
                    plate_width = g_1 + 2 * edge_dist
                    # TODO: Apply max limit for g_1, design fails

            if plate_width > plate_width_max:
                design_status = False
                logger.error(": Required plate width is more than the available width")
                logger.warning(": Width of plate should be less than %s mm" % plate_width_max)
                logger.info(": Currently, Osdag doesn't design such connections")

            # Tension in bolts
            axial_tension = factored_axial_load / number_of_bolts
            if no_rows['out_tension_flange'] == 0:
                extreme_bolt_dist = beam_d - beam_tf * 3 / 2 - l_v
            else:
                extreme_bolt_dist = beam_d - beam_tf / 2 + l_v + (no_rows['out_tension_flange'] - 1) * pitch_dist
            sigma_yi_sq = 0
            for bolt_row in range(int(no_rows['out_tension_flange'])):
                print("out_tension_flange", bolt_row, beam_d - beam_tf / 2 + l_v + bolt_row * pitch_dist)
                sigma_yi_sq += (beam_d - beam_tf / 2 + l_v + bolt_row * pitch_dist) ** 2

            for bolt_row in range(int(no_rows['in_tension_flange'])):
                print("in_tension_flange", bolt_row, beam_d - 3 * beam_tf / 2 - l_v - bolt_row * pitch_dist)
                sigma_yi_sq += (beam_d - 3 * beam_tf / 2 - l_v - bolt_row * pitch_dist) ** 2

            for bolt_row in range(int(no_rows['in_compression_flange'])):
                print("in_compression_flange", bolt_row, beam_tf / 2 + l_v + bolt_row * pitch_dist)
                sigma_yi_sq += (beam_tf / 2 + l_v + bolt_row * pitch_dist) ** 2

            moment_tension = factored_moment * extreme_bolt_dist / sigma_yi_sq / 2
            tension_in_bolt = axial_tension + moment_tension + prying_force
            shear_in_bolt = factored_shear_load / number_of_bolts

            # Check for combined tension and shear
            if bolt_type == "Friction Grip Bolt":
                combined_capacity = IS800_2007.cl_10_4_6_friction_bolt_combined_shear_and_tension(
                    V_sf=shear_in_bolt, V_df=bolt_capacity, T_f=tension_in_bolt, T_df=bolt_tension_capacity)
            else:
                combined_capacity = IS800_2007.cl_10_3_6_bearing_bolt_combined_shear_and_tension(
                    V_sb=shear_in_bolt, V_db=bolt_capacity, T_b=tension_in_bolt, T_db=bolt_tension_capacity)
            bolt_combined_status = combined_capacity <= 1.0

            if bolt_combined_status is False:
                no_tension_side += 2
            if detailing_status is False:
                design_status = False
                logger.error("Large number of bolts are required for the connection")
                logger.info(": Re-design the connection using bolt of higher grade or diameter")
                break

            # Prying force

            print("prying force:", prying_force)
            # toe_of_weld_moment = abs(flange_tension/4 * l_v - prying_force * end_dist)
            toe_of_weld_moment = abs(tension_in_bolt * l_v - prying_force * end_dist)
            end_plate_thickness_min = math.sqrt(toe_of_weld_moment * 1.10 * 4 / (end_plate_fy * b_e))

            # End Plate Thickness
            if end_plate_thickness < max(column_tf, end_plate_thickness_min):
                end_plate_thickness_min = math.ceil(max(column_tf, end_plate_thickness_min))
                design_status = False
                logger.error(": Chosen end plate thickness is not sufficient")
                logger.warning(": Minimum required thickness of end plate is %2.2f mm " % end_plate_thickness_min)
                logger.info(": Increase the thickness of end plate ")
        #######################################################################

    def assign_weld_sizes(self):
        """Assign minimum required weld sizes to flange and web welds and update throat sizes"""

        # Find minimum sizes
        flange_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(
        self.supported_section.flange_thickness, self.plate.thickness_provided)
        web_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(
        self.supported_section.web_thickness, self.plate.thickness_provided)

        # Assign minimum sizes
        self.top_flange_weld.size = choose_higher_value(flange_weld_size_min, ALL_WELD_SIZES)
        self.bottom_flange_weld.size = choose_higher_value(flange_weld_size_min, ALL_WELD_SIZES)
        self.web_weld.size = choose_higher_value(web_weld_size_min, ALL_WELD_SIZES)
        return

    def assign_throat_tk(self):
        # Throat thickness
        self.top_flange_weld.throat_tk = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=self.top_flange_weld.size)
        self.bottom_flange_weld.throat_tk = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=self.bottom_flange_weld.size)
        self.web_weld.throat_tk = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=self.web_weld.size)
        return

    def assign_weld_lengths(self):
        """Available and effective weld lengths are found and multiplied with long joint reduction factors"""

        # Available lengths
        self.top_flange_weld.length = self.supported_section.flange_width
        self.bottom_flange_weld.length = (
            self.supported_section.flange_width - self.supported_section.web_thickness -
            2*self.supported_section.root_radius - 2*self.supported_section.toe_radius) / 2
        self.web_weld.length = self.supported_section.depth - 2 * (self.supported_section.flange_thickness +
                                                                        self.supported_section.root_radius)

        # Effective lengths
        self.top_flange_weld.eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
            fillet_size=self.top_flange_weld.size, available_length=self.top_flange_weld.length)
        self.bottom_flange_weld.eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
            fillet_size=self.bottom_flange_weld.size, available_length=self.bottom_flange_weld.length)
        self.web_weld.eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
            fillet_size=self.web_weld.size, available_length=self.web_weld.length)

        # long joint factors
        self.top_flange_weld.lj_factor = IS800_2007.cl_10_5_7_3_weld_long_joint(
            l_j=self.top_flange_weld.eff_length, t_t=self.top_flange_weld.throat_tk)
        self.bottom_flange_weld.lj_factor = IS800_2007.cl_10_5_7_3_weld_long_joint(
            l_j=self.bottom_flange_weld.eff_length, t_t=self.bottom_flange_weld.throat_tk)
        self.web_weld.lj_factor = IS800_2007.cl_10_5_7_3_weld_long_joint(
            l_j=self.web_weld.eff_length, t_t=self.web_weld.throat_tk)

    def assign_weld_strength(self):
        self.top_flange_weld.strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses=[self.supported_section.fu, self.top_flange_weld.fu],
            fabrication=self.top_flange_weld.fabrication)
        self.bottom_flange_weld.strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses=[self.supported_section.fu, self.bottom_flange_weld.fu],
            fabrication=self.bottom_flange_weld.fabrication)
        self.web_weld.strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses=[self.supported_section.fu, self.web_weld.fu],
            fabrication=self.web_weld.fabrication)
        return

    def weld_design(self):
        #  Design forces per unit length of welds due to applied loads
        # """





        weld_force_axial = self.load.axial_force / (
                2 * (self.top_flange_weld.eff_length * self.top_flange_weld.lj_factor +
                    2 * self.bottom_flange_weld.eff_length * self.bottom_flange_weld.lj_factor +
                    self.web_weld.eff_length * self.web_weld.lj_factor))

        flange_tension_moment = self.load.moment / (beam_d - beam_tf)
        weld_force_moment = flange_tension_moment / (self.top_flange_weld.eff_length +
                                                             2 * self.bottom_flange_weld.eff_length)
        weld_force_shear = self.load.shear_force / (2 * self.web_weld.eff_length * self.web_weld.lj_factor)

        # check for weld strength

        flange_weld_stress = (weld_force_moment + weld_force_axial) / self.top_flange_weld.throat_tk
        flange_weld_throat_reqd = round((weld_force_moment + weld_force_axial) / self.top_flange_weld.strength, 3)
        flange_weld_size_reqd = round(flange_weld_throat_reqd / 0.7, 3)

        web_weld_stress = math.sqrt(weld_force_axial ** 2 + weld_force_shear ** 2) / self.web_weld.throat_tk
        web_weld_throat_reqd = round(math.sqrt(weld_force_axial ** 2 + weld_force_shear ** 2) / self.web_weld.strength, 3)
        web_weld_size_reqd = round(web_weld_throat_reqd / 0.7, 3)

        # """
        """
        axial force is taken by flange and web welds = P/(2*lw+ltf+lbf)
        shear force is taken by web welds only = V/(2*lw)
        moment is taken by both flange and web welds = M/Z 
        z = ltf*lw/2 + lbf*lw/2 + d^2/3 

        Stress for axial load in beam=Axial load/sum of (individual weld length *corresponding weld throat thickness)
        Total length for flange weld = 2* self.top_flange_weld.eff_length + 4* self.bottom_flange_weld.eff_length
        Weld throat thickness for flange = self.top_flange_weld.throat_tk
        Total length for web weld = 2* self.web_weld.eff_length
        Weld throat thickness for flange = self.web_weld.throat_tk
        """

        weld_force_axial = self.load.axial_force / \
                            (self.top_flange_weld.eff_length * self.top_flange_weld.lj_factor +
                            self.bottom_flange_weld.eff_length * self.bottom_flange_weld.lj_factor +
                            2 *self.web_weld.eff_length * self.web_weld.lj_factor)
        # """
        weld_force_axial_stress = self.load.axial_force / ( \
                    2 * self.top_flange_weld.eff_length * self.top_flange_weld.lj_factor * self.top_flange_weld.throat_tk + \
                    4 * self.bottom_flange_weld.eff_length * self.bottom_flange_weld.lj_factor * self.top_flange_weld.throat_tk + \
                    2 * self.web_weld.eff_length * self.web_weld.lj_factor * self.web_weld.throat_tk)

        # flange_tension_moment = self.load.moment / (beam_d - beam_tf)
        # weld_force_moment = flange_tension_moment / (
        #         self.top_flange_weld.eff_length * self.top_flange_weld.lj_factor * self.web_weld.eff_length / 2 +
        #         self.bottom_flange_weld.eff_length * self.bottom_flange_weld.lj_factor * self.web_weld.eff_length / 2 +
        #         self.web_weld.eff_length**2/3)

        # Stresses in extreme weld (top flange) due to applied moment

        weld_Iz = (2 * (self.web_weld.eff_length ** 3) / 12) * self.web_weld.throat_tk + \
                  (2 * self.top_flange_weld.eff_length * (beam_d / 2) ** 2 + \
                   4 * self.bottom_flange_weld.eff_length * (beam_d / 2 - beam_tf) ** 2) * self.top_flange_weld.throat_tk

        flange_weld_Z = weld_Iz / (beam_d / 2)
        web_weld_Z = weld_Iz / (beam_d / 2 - beam_tf - beam_R1)

        flange_weld_stress = self.load.moment / flange_weld_Z + weld_force_axial_stress

        weld_force_shear = self.load.shear_force / (
                    2 * self.web_weld.eff_length * self.web_weld.throat_tk * self.web_weld.lj_factor)

        # calculation of required weld size is not accurate since Iz has different web and flange sizes
        # but to get required throat thickness either flange or weld size is multiplied
        flange_weld_throat_reqd = round(flange_weld_stress * self.top_flange_weld.throat_tk / self.top_flange_weld.strength, 3)
        flange_weld_size_reqd = round(flange_weld_throat_reqd / 0.7, 3)

        web_weld_stress = math.sqrt((self.load.moment / web_weld_Z + weld_force_axial_stress) ** 2 + \
                                    weld_force_shear ** 2)

        web_weld_throat_reqd = round(web_weld_stress * self.web_weld.throat_tk /
                                     self.web_weld.strength, 3)
        web_weld_size_reqd = round(web_weld_throat_reqd / 0.7, 3)

        if flange_weld_stress >= self.top_flange_weld.strength:
            design_status = False
            logger.error(": The weld size at beam flange is less than required")
            if flange_weld_size_reqd > flange_weld_size_max:
                logger.warning(": The connection can not be possible with fillet weld")
                logger.info(": Use groove welds to connect beam and end plate")
            else:
                logger.warning(": The minimum required size of weld at flanges is %s mm" % flange_weld_size_reqd)
                logger.info(": Increase the size of weld at beam flanges")

        if web_weld_stress >= self.web_weld.strength:
            design_status = False
            logger.error(": The weld size at beam web is less than required")
            if web_weld_size_reqd > web_weld_size_max and flange_weld_size_reqd < flange_weld_size_max:
                logger.warning(": The connection can not be possible with fillet weld")
                logger.info(": Use groove welds to connect beam and end plate")
            else:
                logger.warning(": The minimum required size of weld at web is %s mm" % web_weld_size_reqd)
                logger.info(": Increase the size of weld at beam web")

    def groove_weld(self):
        # weld_method == 'groove'
        groove_weld_size_flange = IS800_2007.cl_10_5_3_3_groove_weld_effective_throat_thickness(
            beam_tf, end_plate_thickness)
        groove_weld_size_web = IS800_2007.cl_10_5_3_3_groove_weld_effective_throat_thickness(
            beam_tw, end_plate_thickness)

    def find_end_plate_spacing(self):
        #######################################################################
        # l_v = Distance from the edge of flange to the centre of the nearer bolt (mm) [AISC design guide 16]
        # g_1 = Gauge 1 distance (mm) (also known as cross-centre gauge, Steel designers manual, pp733, 6th edition - 2003)
        endplate_type = ""
        if endplate_type == 'flush':
            l_v = 45.0
            g_1 = 90.0
        elif endplate_type == 'one_way':
            l_v = 50.0
            g_1 = 100.0
        else:  # endplate_type == 'both_ways':
            l_v = 50.0
            g_1 = 100.0

        if self.flange_weld.type is KEY_DP_WELD_TYPE_FILLET:
            flange_projection = round_up(value=self.top_flange_weld.size + 2, multiplier=5, minimum_value=5)
        else:  # 'groove'
            flange_projection = 5

    def continuity_plaste(self):
        # Continuity Plates
        cont_plate_fu = beam_fu
        cont_plate_fy = beam_fy
        cont_plate_e = math.sqrt(250 / cont_plate_fy)
        gamma_m0 = 1.10
        gamma_m1 = 1.10

        # Continuity Plates on compression side
        p_bf = factored_moment / (beam_d - beam_tf) - factored_axial_load  # Compressive force at beam flanges
        cont_plate_comp_length = column_d - 2 * column_tf
        cont_plate_comp_width = (column_B - column_tw) / 2
        notch_cont_comp = round_up(value=column_R1, multiplier=5, minimum_value=5)
        available_cont_comp_width = cont_plate_comp_width - notch_cont_comp
        available_cont_comp_length = cont_plate_comp_length - 2 * notch_cont_comp

        col_web_capacity_yielding = column_tw * (5 * column_tf + 5 * column_R1 + beam_tf) * column_fy / gamma_m0
        col_web_capacity_crippling = ((300 * column_tw ** 2) / gamma_m1) * (
                1 + 3 * (beam_tf / column_d) * (column_tw / column_tf) ** 1.5) * math.sqrt(
            column_fy * column_tf / column_tw)
        col_web_capacity_buckling = (10710 * (column_tw ** 3) / column_d) * math.sqrt(column_fy / gamma_m0)
        col_web_capacity = min(col_web_capacity_yielding, col_web_capacity_crippling, col_web_capacity_buckling)
        cont_plate_comp_tk_local_buckling = cont_plate_comp_width / (9.4 * cont_plate_e)
        cont_plate_comp_tk_min = max(cont_plate_comp_tk_local_buckling, beam_tf,
                                     (p_bf - col_web_capacity) / (cont_plate_comp_width * cont_plate_fy / gamma_m0))
        cont_plate_comp_tk = cont_plate_comp_tk_min
        available_plates = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 32, 34, 35, 36, 40, 45, 50, 55, 60]
        for plate_tk in available_plates:
            if plate_tk >= cont_plate_comp_tk_min:
                cont_plate_comp_tk = plate_tk
                break

        # Continuity Plates on tension side
        t_bf = factored_moment / (beam_d - beam_tf) + factored_axial_load  # Tensile force at beam flanges
        cont_plate_tens_length = column_d - 2 * column_tf
        cont_plate_tens_width = (column_B - column_tw) / 2
        notch_cont_tens = round_up(value=column_R1, multiplier=5, minimum_value=5)
        available_cont_tens_width = cont_plate_tens_width - notch_cont_tens
        available_cont_tens_length = cont_plate_tens_length - 2 * notch_cont_tens

        col_flange_tens_capacity = (column_tf ** 2) * beam_fy / (0.16 * gamma_m0)
        cont_plate_tens_tk_min = (t_bf - col_flange_tens_capacity) / (cont_plate_tens_width * cont_plate_fy / gamma_m0)
        cont_plate_tens_tk = cont_plate_tens_tk_min
        for plate_tk in available_plates:
            if plate_tk >= cont_plate_tens_tk_min:
                cont_plate_tens_tk = plate_tk
                break

        # conisering both plates thickness as same for practical reasons
        if cont_plate_comp_tk > cont_plate_tens_tk:
            cont_plate_tens_tk = cont_plate_comp_tk
        else:
            cont_plate_comp_tk = cont_plate_tens_tk

        welds_sizes = [3, 4, 5, 6, 8, 10, 12, 14, 16]
        # continuity plate weld design on compression side
        # same is assumed for tension side
        cont_web_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(cont_plate_comp_tk, column_tw)
        cont_web_weld_size_max = min(beam_tw, cont_plate_comp_tk)
        available_welds = list([x for x in welds_sizes if (cont_web_weld_size_min <= x <= cont_web_weld_size_max)])
        for cont_web_weld_size in available_welds:
            cont_web_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
                fillet_size=cont_web_weld_size, fusion_face_angle=90)
            cont_web_weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
                fillet_size=cont_web_weld_size, available_length=available_cont_comp_length)
            if (max(p_bf, t_bf) / 2) / (2 * cont_web_weld_eff_length * cont_web_weld_throat) <= \
                    IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                        ultimate_stresses=(weld_fu, column_fu, cont_plate_fu)):
                break

        cont_flange_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(cont_plate_comp_tk, column_tf)
        cont_flange_weld_size_max = max(column_tf, cont_plate_comp_tk)
        available_welds = list(
            [x for x in welds_sizes if (cont_flange_weld_size_min <= x <= cont_flange_weld_size_max)])
        for cont_flange_weld_size in available_welds:
            cont_flange_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
                fillet_size=cont_flange_weld_size, fusion_face_angle=90)
            cont_flange_Weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
                fillet_size=cont_flange_weld_size, available_length=available_cont_comp_width)
            cont_axial_stress = (max(p_bf, t_bf) / 2) / (4 * cont_flange_Weld_eff_length * cont_flange_weld_throat)
            cont_moment_stress = (max(p_bf, t_bf) / 2) * (l_v + beam_tw / 2) / (
                    cont_plate_comp_length * cont_flange_weld_throat * 4 * cont_flange_Weld_eff_length)
            if math.sqrt(
                    cont_axial_stress ** 2 + cont_moment_stress ** 2) <= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                ultimate_stresses=(weld_fu, column_fu, cont_plate_fu)):
                break
        # same weld size is considered for flange and web connectivity of continuity plates
        # TODO: Should we recalculate stresses for common weld thickness?
        # TODO: what if this maximum size exceeds limits of one connection?

        cont_weld_size = max(cont_flange_weld_size, cont_web_weld_size)

        # continuity plate warnings
        if math.sqrt(
                cont_axial_stress ** 2 + cont_moment_stress ** 2) >= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses=(weld_fu, column_fu, cont_plate_fu)):
            logger.warning("weld between column flange and continuity plates is not safe")

        if (max(p_bf, t_bf) / 2) / (2 * cont_web_weld_eff_length * cont_web_weld_throat) >= \
                IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                    ultimate_stresses=(weld_fu, column_fu, cont_plate_fu)):
            logger.warning("weld between column web and continuity plates is not safe")

        # Note: for more number of iteration more numbers of  available size should be provided

    def stiffener(self):
        # Beam stiffeners
        st_status = False
        if endplate_type == 'flush':
            st_number = 0
        elif endplate_type == 'one_way':
            st_number = 1
            if number_of_bolts >= 12:
                st_status = True
        else:
            st_number = 2
            if number_of_bolts >= 20:
                st_status = True

        st_fu = beam_fu
        st_fy = beam_fy
        st_height = l_v + pitch_dist + end_dist
        # for plate_tk in available_plates:
        #     if plate_tk >= beam_tw:
        #         st_thickness = plate_tk
        #         break
        available_thickness = list([x for x in available_plates if (beam_tw <= x <= max(available_plates))])
        st_thickness = min(available_thickness)
        st_length_min = st_height + 100.0
        st_notch_top = 50.0
        st_notch_bottom = round_up(value=weld_thickness_flange, multiplier=5, minimum_value=5)

        st_force = 4 * tension_in_bolt
        st_moment = st_force * (l_v + pitch_dist / 2)
        st_length = st_length_min
        st_beam_weld = 3.0
        if st_status is True:
            # stiffener plate design
            for st_thickness in available_thickness:
                print(st_thickness)
                while st_length <= float(int(beam_d / 100) * 100):
                    st_eff_length = st_length - st_notch_bottom
                    st_shear_capacity = st_eff_length * st_thickness * st_fy / (math.sqrt(3) * gamma_m0)
                    st_moment_capacity = st_eff_length ** 2 * st_thickness * st_fy / (4 * gamma_m0)
                    print(st_thickness, st_length, st_shear_capacity, st_moment_capacity, st_force, st_moment)
                    if st_moment <= st_moment_capacity and st_force <= st_shear_capacity:
                        break
                    else:
                        st_length += 20
                if st_moment <= st_moment_capacity and st_force <= st_shear_capacity:
                    break
                else:
                    st_length = st_length_min

            # Stiffener Weld Design
            st_beam_weld_min = IS800_2007.cl_10_5_2_3_min_weld_size(st_thickness, beam_tf)
            st_beam_weld_max = max(beam_tf, st_thickness)

            available_welds = list([x for x in welds_sizes if (st_beam_weld_min <= x <= st_beam_weld_max)])
            for st_beam_weld in available_welds:
                if st_beam_weld <= st_beam_weld_min:
                    st_beam_weld = st_beam_weld_min
                st_beam_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
                    fillet_size=st_beam_weld, fusion_face_angle=90)
                st_beam_weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
                    fillet_size=st_beam_weld, available_length=st_eff_length)
                st_weld_shear_stress = st_force / (2 * st_beam_weld_eff_length * st_beam_weld_throat)
                st_weld_moment_stress = st_moment / (2 * st_beam_weld * st_beam_weld_eff_length ** 2 / 4)
                st_eq_weld_stress = math.sqrt(st_weld_shear_stress ** 2 + st_weld_moment_stress ** 2)
                if st_eq_weld_stress <= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                        ultimate_stresses=(weld_fu, beam_fu, st_fu)):
                    break
            # stiffener warnings

            if st_moment >= st_moment_capacity:
                logger.warning("stiffener cannot take moment, current stiffener length %2.2f" % st_length)
            if st_force >= st_shear_capacity:
                logger.warning("stiffener cannot take shear force, current stiffener length %2.2f" % st_length)
            if st_eq_weld_stress >= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                    ultimate_stresses=(weld_fu, beam_fu, st_fu)):
                logger.warning(
                    "stiffener weld cannot take stiffener loads, current weld thickness is %2.2f" % st_beam_weld)

        # Strength of flange under compression or tension TODO: Get function from IS 800

        A_f = beam_B * beam_tf  # area of beam flange
        capacity_beam_flange = (beam_fy / gamma_m0) * A_f
        force_flange = max(t_bf, p_bf)

    def trial_design(self):
        self.set_osdaglogger()
        bolt_dia = max(self.bolt.bolt_diameter)
        bolt_grade = max(self.bolt.bolt_grade)
        end_plate_thickness = min(self.plate.thickness)

        self.check_minimum_design_action()
        self.check_compatibility()

        # Weld design
        self.assign_weld_sizes()
        self.assign_throat_tk()
        self.assign_weld_lengths()
        self.assign_weld_strength()

        self.find_bolt_conn_plates_t_fu_fy()
        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=bolt_dia,
                                                conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy)




















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

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.type)
        self.supported_section.notch_ht = round_up(
            max(self.supporting_section.flange_thickness + self.supporting_section.root_radius + 10,
                self.supported_section.flange_thickness + self.supported_section.root_radius + 10), 5)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.type == "Rolled":
                self.supported_section.web_height = self.supported_section.depth
            else:
                self.supported_section.web_height = self.supported_section.depth - (
                            2 * self.supported_section.flange_thickness)  # -(2*self.supported_section.root_radius)
        else:

            self.supported_section.web_height = self.supported_section.depth - self.supported_section.notch_ht

        A_g = self.supported_section.web_height * self.supported_section.web_thickness
        # 0.6 is multiplied for shear yielding capacity to keep the section in low shear
        self.supported_section.shear_yielding_capacity = 0.6 * IS800_2007.cl_8_4_design_shear_strength(A_g,
                                                                                                       self.supported_section.fy)
        self.supported_section.tension_yielding_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g,
                                                                                                       self.supported_section.fy)
        if self.supported_section.shear_yielding_capacity / 1000 > self.load.shear_force and \
                self.supported_section.tension_yielding_capacity / 1000 > self.load.axial_force:

            if self.load.shear_force <= min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                            40.0):
                logger.warning(" : User input for shear force is very less compared to section capacity. "
                               "Setting Shear Force value to 15% of supported beam shear capacity or 40kN, whichever is less.")
                self.load.shear_force = min(round(0.15 * self.supported_section.shear_yielding_capacity / 1000, 0),
                                            40.0)

            print("preliminary member check is satisfactory. Checking available plate Thickness")
            self.thickness_possible = [i for i in self.plate.thickness if i >= self.supported_section.web_thickness]

            if not self.thickness_possible:
                logger.error(": Plate thickness should be greater than suppported section web thicknesss.")
            else:
                print("Selecting bolt diameter")
                self.get_endplate_details(self)

        else:
            # self.design_status = False
            logger.warning(" : shear yielding capacity {} and/or tension yielding capacity {} is less "
                           "than applied loads, Please select larger sections or decrease loads"
                           .format(self.supported_section.shear_yielding_capacity,
                                   self.supported_section.tension_yielding_capacity))
            print("failed in preliminary member checks. Select larger sections or decrease loads")

    def get_endplate_details(self):
        self.design_status = False
        print(self.supporting_section)
        print(self.supported_section)
        print(self.bolt)
        print(self.plate)

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        # t4 = ('End Plate', self.call_3DPlate)
        # components.append(t4)

        return components

