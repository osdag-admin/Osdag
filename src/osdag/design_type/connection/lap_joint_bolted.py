"""
Module: lap_joint_bolted.py
Author: Aman
Date: 2025-02-18

Description:
    LapJointBolted is a moment connection module that represents a bolted lap joint connection.
    It inherits from MomentConnection and follows the same structure and design logic as other
    connection modules (e.g., BeamCoverPlate, ColumnCoverPlate) used in Osdag.
    
Reference:
    - Osdag software guidelines and connection module structure documentation
"""

from .moment_connection import MomentConnection
from ...utils.common.component import *
from ...utils.common.is800_2007 import *
from ...Common import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...Report_functions import *
from ...utils.common.load import Load
import logging

import math

class LapJointBolted(MomentConnection):
    def __init__(self):
        super(LapJointBolted, self).__init__()
        self.design_status = False
        self.spacing = None 
        # self.bolt_type = None

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []
        # Only Bolt and Detailing tabs
        tabs.append(("Bolt", TYPE_TAB_2, self.bolt_values))
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
        return tabs

    def tab_value_changed(self):
        # No tab value dependencies needed for bolt and detailing
        return []

    def edit_tabs(self):
        return []  # Keep original empty implementation

    def input_dictionary_design_pref(self):
        design_input = []
        
        # Bolt preferences
        design_input.append(("Bolt", TYPE_COMBOBOX, [
            KEY_DP_BOLT_TYPE,  # For pretensioned/non-pretensioned
            KEY_DP_BOLT_HOLE_TYPE,  # For standard/oversized
            KEY_DP_BOLT_SLIP_FACTOR  # For slip factor as per Table 20
        ]))
        
        # Detailing preferences
        design_input.append(("Detailing", TYPE_COMBOBOX, [
            KEY_DP_DETAILING_EDGE_TYPE  # For edge preparation method
        ]))
        
        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        
        # Default values for bolt and detailing
        design_input.append((None, [
            KEY_DP_BOLT_TYPE,
            KEY_DP_BOLT_HOLE_TYPE, 
            KEY_DP_BOLT_SLIP_FACTOR,
            KEY_DP_DETAILING_EDGE_TYPE
        ], ''))
        
        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):
        # Default values as per requirements
        defaults = {
            KEY_DP_BOLT_TYPE: "Non Pre-tensioned",
            KEY_DP_BOLT_HOLE_TYPE: "Standard",
            KEY_DP_BOLT_SLIP_FACTOR: "0.3",
            KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut"
        }
        return defaults.get(key)

    def detailing_values(self, input_dictionary):
        values = {
            KEY_DP_DETAILING_EDGE_TYPE: 'Sheared or hand flame cut'
        }

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        detailing = []
        
        # Edge preparation method as per Cl. 10.2.4 of IS:800:2007
        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX,
            ['Sheared or hand flame cut', 'Rolled, machine-flame cut, sawn and planed'],
            values[KEY_DP_DETAILING_EDGE_TYPE])
        detailing.append(t1)
        t4 = ("textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION_LAPJOINT, None)
        detailing.append(t4)

        return detailing

    # def bolt_values(self, input_dictionary):
    #     values = {
    #         KEY_DP_BOLT_TYPE: 'Non Pre-tensioned',
    #         KEY_DP_BOLT_HOLE_TYPE: 'Standard',
    #         KEY_DP_BOLT_SLIP_FACTOR: '0.3'
    #     }

    #     for key in values.keys():
    #         if key in input_dictionary.keys():
    #             values[key] = input_dictionary[key]

    #     bolt = []
        
    #     # Bolt type selection
    #     t1 = (KEY_DP_BOLT_TYPE, "Type", TYPE_COMBOBOX,
    #         ['Non Pre-tensioned', 'Pre-tensioned'],
    #         values[KEY_DP_BOLT_TYPE])
    #     bolt.append(t1)
        
    #     # Bolt hole type
    #     t2 = (KEY_DP_BOLT_HOLE_TYPE, "Bolt Hole", TYPE_COMBOBOX,
    #         ['Standard', 'Over-sized'],
    #         values[KEY_DP_BOLT_HOLE_TYPE])
    #     bolt.append(t2)
        
    #     # Slip factor as per Table 20 of IS 800
    #     t3 = (KEY_DP_BOLT_SLIP_FACTOR, "Slip Factor", TYPE_COMBOBOX,
    #         ['0.3', '0.45', '0.5'],
    #         values[KEY_DP_BOLT_SLIP_FACTOR])
    #     bolt.append(t3)

    #     return bolt


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
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)


    def input_value_changed(self):

        lst = []

        t8 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t8)

        return lst


    def input_values(self):

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_LAPJOINTBOLTED, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t31 = (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t31)

        t34 = (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t34)

        t35 = (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None, True, 'Float Validator')
        options_list.append(t35)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_TENSILE_FORCE, KEY_DISP_TENSILE_FORCE, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        return options_list

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        # t5 = (KEY_PLATE1_THICKNESS, self.plate_thick_customized)
        # list1.append(t5)
        # t6 = (KEY_PLATE2_THICKNESS, self.plate_thick_customized)
        # list1.append(t6)
        
        return list1
    
    def spacing(self, status):
        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details - 3 x 3 pattern considered")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
            [str(files("osdag.data.ResourceFiles.images").joinpath("spacing_3.png")), 400, 277, ""])  # [image, width, height, caption]
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.bolt.min_gauge_round if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.bolt.min_end_dist_round if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.bolt.min_pitch_round if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.bolt.min_edge_dist_round if status else '')
        spacing.append(t12)

        return spacing

    def output_values(self, flag):

        out_list = []
        t4 = (None, DISP_TITLE_BOLTD, TYPE_TITLE, None, True)
        out_list.append(t4)

        t2 = (KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX,
             self.bolt.bolt_diameter_provided if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX,
              self.bolt.bolt_grade_provided if flag else '', True)
        out_list.append(t3)

        t31 = (KEY_OUT_TYP_PROVIDED, KEY_OUT_DISP_TYP_PROVIDED, TYPE_TEXTBOX,
              self.bolt.bolt_type if flag else '' , True)
        out_list.append(t31)

        t8 = (KEY_OUT_BOLT_SHEAR,KEY_OUT_DISP_BOLT_SHEAR , TYPE_TEXTBOX,float(self.bolt.bolt_shear_capacity)/1000 if flag else '', True)
        out_list.append(t8) 

        t4 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, float(self.bolt.bolt_bearing_capacity)/1000 if flag else '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
             float(self.bolt.bolt_capacity)/1000 if flag else '', True)
        out_list.append(t5)

        t500 = (KEY_OUT_BOLT_SLIP, KEY_OUT_DISP_BOLT_SLIP, TYPE_TEXTBOX,
              self.slip_res if flag else '', True)
        out_list.append(t500)

        t17 = (None, DISP_TITLE_BOLTDS, TYPE_TITLE, None, True)
        out_list.append(t17)
        t17 = (KEY_OUT_TOT_NO_BOLTS, KEY_OUT_DISP_TOT_NO_BOLTS, TYPE_TEXTBOX, self.number_bolts if flag else '', True)
        out_list.append(t17)
        t18 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX,self.rows if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_COL_PROVIDED, KEY_OUT_DISP_COL_PROVIDED, TYPE_TEXTBOX,self.cols if flag else '', True)
        out_list.append(t19)

        t20 = (KEY_OUT_BOLT_CONN_LEN, KEY_OUT_DISP_BOLT_CONN_LEN, TYPE_TEXTBOX, self.len_conn if flag else '', True)
        out_list.append(t20)

        t29 = (KEY_UTILIZATION_RATIO, KEY_DISP_UTILIZATION_RATIO, TYPE_TEXTBOX,'', True)
        out_list.append(t29)
        
        t21 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t21)



        return out_list

    def module_name(self):

        return KEY_DISP_LAPJOINTBOLTED
    
    def func_for_validation(self, design_dictionary):

        all_errors = []
        "check valid inputs and empty inputs in input dock"
        # print(design_dictionary,'djsgggggggggggggggggggggggggggggggggggggggggggggggggggggggg')
        self.design_status = False

        flag = False
        flag1 = False
        flag2 = False
        # self.include_status = True

        option_list = self.input_values(self)
        missing_fields_list = []

        print(f'\n func_for_validation option list = {option_list}'
              f'\n  design_dictionary {design_dictionary}')

        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':

                    print(f"\n option {option}")

                    missing_fields_list.append(option[1])
                else:
                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_PLATE_WIDTH:
                        # val = option[4]
                        # print(design_dictionary[option[0]], "jhvhj")
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True

                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_TENSILE_FORCE:

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
        if flag  and flag1 and flag2:
            self.set_input_values(self, design_dictionary)
            # print("DESIGN DICT" + str(design_dictionary))
            # print("succsess")
        else:
            return all_errors


    def set_input_values(self, design_dictionary):

        "initialisation of components required to design a tension member along with connection"

        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Lap Joint Bolted Connection"
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.tensile_force = design_dictionary[KEY_TENSILE_FORCE]
        self.width = design_dictionary[KEY_PLATE_WIDTH]
        # self.bolt_type = design_dictionary[KEY_TYP]
        self.plate1 = Plate(thickness=[design_dictionary[KEY_PLATE1_THICKNESS]],
                           material_grade=design_dictionary[KEY_MATERIAL],width=design_dictionary[KEY_PLATE_WIDTH])
        self.plate2 = Plate(thickness=[design_dictionary[KEY_PLATE2_THICKNESS]],
                            material_grade=design_dictionary[KEY_MATERIAL],width=design_dictionary[KEY_PLATE_WIDTH])
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         )
        # self.load = Load(axial_force=self.tensile_force)
        print("The input values are set. Performing preliminary member check(s).")
        self.planes = 1
        self.bolt_design_status = False
        self.count = 0
        # self.bolt_grade = [np.float64(design_dictionary[KEY_GRD])]
        # self.bolt_diameter = [np.float64(design_dictionary[KEY_D])]
        self.slip_res = None
        self.number_bolts = None
        self.bolt_grade_status = False
        self.rows = None
        self.cols = None
        self.len_conn = 0

        # self.i = 0
        # print("passed \n")
        # print(self.bolt)
        # print(self.plate1thk_provided)
        # print(self.plate1thk)
        self.select_bolt_dia(self,design_dictionary,dia_remove =None)


    def select_bolt_dia(self,design_dictionary,dia_remove =None):
        "Selection of bolt (dia) from te available list of bolts based on the spacing limits and capacity"
        "Loop checking each member from sizelist based on yield capacity"
        if (dia_remove) == None:
            pass
        else:
            if dia_remove in self.bolt.bolt_diameter:
                self.bolt.bolt_diameter.remove(dia_remove)
            else:
                pass

        self.res_force = self.tensile_force*1000

        if isinstance(self.plate1.thickness, list):
            self.plate1thk = self.plate1.thickness[0]

        if isinstance(self.plate2.thickness, list):
            self.plate2thk = self.plate2.thickness[0]

        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((float(self.plate1thk), self.plate1.fu, self.plate1.fy))
        self.bolt_conn_plates_t_fu_fy.append((float(self.plate2thk), self.plate2.fu, self.plate2.fy))
        self.bolt.bolt_grade_provided = self.bolt.bolt_grade[-1]

        self.bolt_diameter_possible=[]
        for d in self.bolt.bolt_diameter:
            if 8 * d < (float(self.plate1thk) + float(self.plate2thk)):
                continue
            else:
                self.bolt_diameter_possible.append(d)
        if float(self.plate1thk) < float(self.plate2thk):
            self.plate = self.plate1
            self.pltthk = float(self.plate1thk)
        else:
            self.plate = self.plate2
            self.pltthk = float(self.plate2thk)

        if len(self.bolt_diameter_possible) ==0.0:
            self.design_status = False
            logger.warning(" : The combined thickness ({} mm) exceeds the allowable large grip limit check (of {} mm) for the minimum available "
                           "bolt diameter of {} mm [Ref. Cl.10.3.3.2, IS 800:2007]."
                           .format((float(self.plate1thk) + float(self.plate2thk)),(8*self.bolt.bolt_diameter[-1]),self.bolt.bolt_diameter[-1]))
            logger.error(": Design is not safe. \n ")
            logger.info(" :=========End Of design===========")

        else:
            self.bolt_design_status = False
            for self.bolt.bolt_diameter_provided in reversed(self.bolt_diameter_possible):

                # print(self.bolt.bolt_diameter_provided)
                self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                        conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,n=self.planes)

                self.bolt.min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt.bolt_diameter_provided, self.bolt.bolt_hole_type,
                                                             'machine_flame_cut'), 2)
                self.bolt.min_edge_dist_round = round_up(self.bolt.min_edge_dist, 5)

                print("HEELEELEE",self.bolt.min_edge_dist_round,self.bolt.min_edge_dist,self.bolt_conn_plates_t_fu_fy,self.bolt.min_pitch_round)

                # self.bolt.max_edge_dist = round(IS800_2007.cl_10_2_4_3_max_edge_dist(self.bolt_conn_plates_t_fu_fy, corrosive_influences=False),2)

                # self.bolt.max_edge_dist_round = round_up(self.bolt.max_edge_dist, 5)


                self.bolt.calculate_bolt_capacity(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=self.planes, e=float(self.bolt.min_end_dist_round),
                                              p=float(self.bolt.min_pitch_round))

                self.bolt_design_status = True


        if self.bolt_design_status  == True:
            self.design_status = True
            print("bolt ok")
            self.get_bolt_grade(self, design_dictionary)

        else:
            self.design_status = False
            logger.error(": Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")
        # print("CHKPOINT 1")
        # print(self.bolt)
        # print(self.plate)



    def get_bolt_grade(self, design_dictionary):
        bolt_grade_previous = self.bolt.bolt_grade[0]
        bolts_required_previous = 2
        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((float(self.plate1thk), float(self.plate1.fu), float(self.plate1.fy)))
        self.bolt_conn_plates_t_fu_fy.append((float(self.plate2thk), float(self.plate2.fu), float(self.plate2.fy)))

        for self.bolt.bolt_grade_provided in self.bolt.bolt_grade:
            count = 1
            self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                    conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,n=self.planes)

            self.bolt.min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt.bolt_diameter_provided, self.bolt.bolt_hole_type,
                                                         'machine_flame_cut'), 2)

            self.bolt.min_edge_dist_round = round_up(self.bolt.min_edge_dist, 5)

            # self.bolt.max_edge_dist = round(IS800_2007.cl_10_2_4_3_max_edge_dist(self.bolt_conn_plates_t_fu_fy, corrosive_influences=False),2)

            # self.bolt.max_edge_dist_round = round_up(self.bolt.max_edge_dist, 5)

            # self.bolt.max_edge_dist_round = 15
            # self.bolt.max_end_dist_round = 15
            # self.bolt.max_spacing_round = 250

            self.bolt.calculate_bolt_capacity(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=self.planes, e=float(self.bolt.min_end_dist_round),
                                              p=float(self.bolt.min_pitch_round))
            
            #reduced capacity code part

            bolt_capacity_reduced = self.plate.get_bolt_red(bolts_one_line=1,
                                                            gauge=self.bolt.min_gauge_round,bolts_line=2,
                                                            pitch=self.bolt.min_pitch_round,bolt_capacity=float(self.bolt.bolt_capacity),
                                                            bolt_dia=self.bolt.bolt_diameter_provided,end_dist=float(self.bolt.min_end_dist_round),beta_lg=self.bolt.beta_lg,edge_dist=float(self.bolt.min_edge_dist_round),web_thickness=float(self.pltthk))
            
            self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                                  bolt_grade_provided=self.bolt.bolt_grade_provided)
            if bolt_capacity_reduced < float(self.tensile_force * 1000) and count >= 1:
                self.bolt.bolt_grade_provided = bolt_grade_previous
                self.bolt_grade_status = True
                break
            bolts_required_previous = self.plate.bolts_required
            bolt_grade_previous = self.bolt.bolt_grade_provided
            # bolt_capacity_previous
            count += 1

        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                                                conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,n=self.planes)

        self.bolt.min_edge_dist = round(IS800_2007.cl_10_2_4_2_min_edge_end_dist(self.bolt.bolt_diameter_provided, self.bolt.bolt_hole_type,
                                                     'machine_flame_cut'), 2)

        self.bolt.min_edge_dist_round = round_up(self.bolt.min_edge_dist, 5)
        # print(self.bolt.min_edge_dist_round,self.bolt.max_end_dist,"hfhh")

        # print(self.bolt.min_edge_dist_round,self.bolt.min_edge_dist, "gbfhgfbdhhbdg")





        self.bolt.calculate_bolt_capacity(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                                              bolt_grade_provided=self.bolt.bolt_grade_provided,
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=self.planes, e=float(self.bolt.min_end_dist_round),
                                              p=float(self.bolt.min_pitch_round))
        

        
        if self.bolt.bolt_type == 'Bearing Bolt':
            self.bolt.bolt_bearing_capacity = round(float(self.bolt.bolt_bearing_capacity),2)
        
        self.bolt.bolt_shear_capacity = round(float(self.bolt.bolt_shear_capacity),2)
        self.bolt.bolt_capacity = round(float(self.bolt.bolt_capacity),2)
        

        if self.bolt_grade_status == True:
            self.design_status = True
            # print("CHKPOINT 2")
            # print(self.bolt)
            self.count_bolts(self, design_dictionary)
        else:
            self.design_status = False
            logger.error(": Design is unsafe. \n ")
            logger.info(" :=========End Of design===========")

    

    
    def count_bolts(self, design_dictionary):
        
        bolt_cap = float(self.bolt.bolt_capacity)
        if self.bolt.bolt_type == 'Bearing Bolt':
            self.slip_res = 'N/A'
        else:
            self.slip_res = self.bolt.bolt_capacity
            self.bolt.bolt_bearing_capacity = 'N/A'
            self.bolt.bolt_shear_capacity = 'N/A'
            
        
        self.number_bolts = float(self.tensile_force) /( bolt_cap / 1000)
        if self.number_bolts < 2:
            self.number_bolts = 2
            #change to bolt capacity as cant get the value for bearing cap
        self.number_bolts = math.ceil(self.number_bolts)

        def check_no_cols(numbolts):
            if (2 * self.bolt.min_end_dist_round) + ((numbolts - 1 )*self.bolt.min_pitch_round) > float(self.width):
                return True
            else:
                return False

        
        self.cols = 1
        self.rows = self.number_bolts
        # print("VALUUUEUE", (2 * self.bolt.min_end_dist_round) + ((self.rows - 1 )*self.bolt.min_pitch_round))
        temp = self.rows
        while True:
            if check_no_cols(temp):
                temp = math.ceil(self.rows/(self.cols + 1))
                self.cols += 1
            else:
                break
        self.rows = math.ceil(self.rows/self.cols)  
        # self.rows = math.ceil((float(self.width) - (2 * float(self.bolt.min_end_dist_round)))/float(self.bolt.min_pitch_round))

        
        if self.cols>1:
            self.len_conn = (self.cols - 1)*self.bolt.min_pitch_round + 2*self.bolt.min_end_dist_round

        else:
            self.len_conn = self.bolt.min_pitch_round + 2*self.bolt.min_end_dist_round
        if self.number_bolts >= 2:
            self.design_status = True
            self.reduce_capacity(self, design_dictionary)
        else:
            self.design_status = False
            logger.error(": Number of min bolts not satisfied. \n ")
            logger.info(" :=========End Of design===========")


    def reduce_capacity(self, design_dictionary):
        bij = 0
        if self.rows > 2:
            lg = (self.rows - 1)*self.bolt.min_pitch_round
            if  lg > 15 * self.bolt.bolt_diameter_provided:
                bij = 1.075 - (lg / (200 * self.bolt.bolt_diameter_provided))
        if bij >= 0.75 and bij <= 1.0:
            print("Fahfjafajf",bij)


                
        self.design_status = True



    def call_3DColumn(self, ui, bgcolor):
        # status = self.resultObj['Bolt']['status']
        # if status is True:
        #     self.ui.chkBx_beamSec1.setChecked(Qt.Checked)
        if ui.chkBxCol.isChecked():
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
        # self.display_3DModel("Beam", bgcolor)
        ui.commLogicObj.display_3DModel("Column", bgcolor)

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t3 = ('Plate1', self.call_3DColumn)
        components.append(t3)

        t4 = ('Plate2', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Cover Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Cover Plate", bgcolor)
    
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


    ################################ Outlist Dict #####################################################################################

    # def results_to_test(self, filename):
    #     test_out_list = {KEY_OUT_DISP_D_PROVIDED:'',
    #                      KEY_OUT_DISP_GRD_PROVIDED:'',
    #                      KEY_OUT_DISP_TYP_PROVIDED:self.bolt_type,
    #                         KEY_OUT_DISP_BOLT_SHEAR:'',
    #                         KEY_OUT_DISP_BOLT_BEARING:'',
    #                         KEY_OUT_DISP_BOLT_CAPACITY:'',
    #                         KEY_OUT_DISP_BOLT_SLIP:'',
    #                         KEY_OUT_DISP_TOT_NO_BOLTS:'',
    #                         KEY_OUT_DISP_ROW_PROVIDED:'',
    #                         KEY_OUT_DISP_COL_PROVIDED:'',
    #                         KEY_OUT_DISP_BOLT_CONN_LEN:'',
    #                         KEY_DISP_UTILIZATION_RATIO:'',
    #                         KEY_OUT_DISP_SPACING:'',
    #                         KEY_OUT_DISP_PITCH:'',
    #                         KEY_OUT_DISP_END_DIST:'',
    #                         KEY_OUT_DISP_GAUGE:'',
    #                         KEY_OUT_DISP_EDGE_DIST:'',

    #                      }
    #     f = open(filename, "w")
    #     f.write(str(test_out_list))
    #     f.close()
    #     return test_out_list

    ################################ Design Report #####################################################################################


    ### UTILIZATION RATIO, LEN OF CONNECTION AND LOOK INTO WEIRD VALUES FOR BOLTS ROWS AND TOTAL BOLTS