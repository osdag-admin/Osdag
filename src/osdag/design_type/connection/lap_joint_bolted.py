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
        
        # self.spacing = None

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
    
    ####################################
    # Design Preference Functions End
    ####################################
    def set_osdaglogger(key):

        """Function to set Logger for Tension Module"""
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

        return list1
    
    def spacing(self, status):
        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details - 3 x 3 pattern considered")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
            [str(files("osdag.data.ResourceFiles.images").joinpath("spacing_3.png")), 400, 277, ""])
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.final_gauge if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.final_end_dist if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.final_pitch if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.final_edge_dist if status else '')
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

        t8 = (KEY_OUT_BOLT_SHEAR,KEY_OUT_DISP_BOLT_SHEAR , TYPE_TEXTBOX,self.bolt.bolt_shear_capacity if flag else '', True)  #convert to kn at last of the program
        out_list.append(t8) 

        t4 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, self.bolt.bolt_bearing_capacity if flag else '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
            self.bolt.bolt_capacity if flag else '', True)
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

        t29 = (KEY_UTILIZATION_RATIO, KEY_DISP_UTILIZATION_RATIO, TYPE_TEXTBOX,self.utilization_ratio if flag else '', True)
        out_list.append(t29)
        
        t21 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t21)



        return out_list
    
    def module_name(self):

        return KEY_DISP_LAPJOINTBOLTED
    
    def func_for_validation(self, design_dictionary):

        all_errors = []
        "check valid inputs and empty inputs in input dock"
        self.design_status = False
        flag = False
        flag1 = False
        flag2 = False

        option_list = self.input_values(self)
        missing_fields_list = []

        # print(f'\n func_for_validation option list = {option_list}'
        #       f'\n  design_dictionary {design_dictionary}')

        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':

                    missing_fields_list.append(option[1])
                else:
                    if option[2] == TYPE_TEXTBOX and option[0] == KEY_PLATE_WIDTH:

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
        else:
            flag = True
        if flag  and flag1 and flag2:
            self.set_input_values(self, design_dictionary)
        else:
            return all_errors
        
    def set_input_values(self, design_dictionary):

        "initialisation of components required to design a tension member along with connection"

        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Lap Joint Bolted Connection"
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.tensile_force = design_dictionary[KEY_TENSILE_FORCE]
        self.width = design_dictionary[KEY_PLATE_WIDTH]
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
        self.planes = 1
        self.count = 0
        self.slip_res = None
        self.yield_stress = None
        # self.number_bolts = 0
        self.cap_red = False
        self.bolt_dia_grade_status = False
        self.dia_available = False
        self.final_pitch = 0
        self.final_end_dist = 0
        self.final_edge_dist = 0
        self.final_gauge = 0
        self.rows = 0
        self.cols = 0
        self.len_conn = 0
        self.max_gauge_round = 0
        self.max_pitch_round = 0
        self.utilization_ratio = 0
        self.bij = 0
        self.blg = 0
        self.select_bolt_dia_and_grade(self,design_dictionary)

    def select_bolt_dia_and_grade(self,design_dictionary):
        self.dia_available = False
        self.bolt_dia_grade_status = False

        if isinstance(self.plate1.thickness, list):
            self.plate1thk = self.plate1.thickness[0]

        if isinstance(self.plate2.thickness, list):
            self.plate2thk = self.plate2.thickness[0]

        self.bolt_conn_plates_t_fu_fy = []
        self.bolt_conn_plates_t_fu_fy.append((float(self.plate1thk), self.plate1.fu, self.plate1.fy))
        self.bolt_conn_plates_t_fu_fy.append((float(self.plate2thk), self.plate2.fu, self.plate2.fy))

        if float(self.plate1thk) < float(self.plate2thk):
            self.plate = self.plate1
            self.pltthk = float(self.plate1thk)
            self.yield_stress = self.plate1.fy
        else:
            self.plate = self.plate2
            self.pltthk = float(self.plate2thk)
            self.yield_stress = self.plate2.fy

        for self.bolt.bolt_diameter_provided in self.bolt.bolt_diameter:
            if 8 * float(self.bolt.bolt_diameter_provided) > (float(self.plate1thk) + float(self.plate2thk)):
                self.dia_available = True
                
                for self.bolt.bolt_grade_provided in self.bolt.bolt_grade:
                    
                    self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                                                        conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,n=self.planes)
                    
                    # self.max_pitch_round = self.max_gauge_round = 
                    # self.bolt.calculate_bolt_capacity(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                    #                           bolt_grade_provided=float(self.bolt.bolt_grade_provided),
                    #                           conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                    #                           n_planes=self.planes, e=float(self.bolt.min_end_dist_round),
                    #                           p=float(self.bolt.min_pitch_round))
                    # self.bolt.calculate_bolt_tension_capacity(bolt_diameter_provided=self.bolt.bolt_diameter_provided,
                    #                                               bolt_grade_provided=self.bolt.bolt_grade_provided)
                    # print("fnafnafan",self.bolt.bolt_capacity)
                    self.bolt.min_pitch_round = min(self.bolt.min_pitch_round, 2.5 * float(self.bolt.bolt_diameter_provided))
                    self.bolt.min_gauge_round = min(self.bolt.min_gauge_round, 2.5 * float(self.bolt.bolt_diameter_provided))

                    if design_dictionary[KEY_DP_DETAILING_EDGE_TYPE] == 'Sheared or hand flame cut':
                        self.bolt.min_edge_dist_round = round(max(1.7 * float(self.bolt.bolt_diameter_provided),self.bolt.min_edge_dist_round),0)
                        self.bolt.min_end_dist_round = round(max(1.7 * float(self.bolt.bolt_diameter_provided),self.bolt.min_end_dist_round),0)
                    else:
                        self.bolt.min_edge_dist_round = round(max(1.5 * float(self.bolt.bolt_diameter_provided),self.bolt.min_edge_dist_round),0)
                        self.bolt.min_end_dist_round = round(max(1.5 * float(self.bolt.bolt_diameter_provided),self.bolt.min_end_dist_round),0)

                    self.max_pitch_round = self.max_gauge_round = min(32 * self.pltthk , 300)

                    self.bolt.max_edge_dist_round = self.bolt.max_end_dist_round = round(min(self.bolt.max_edge_dist_round , 12 * self.pltthk * ((250 / self.yield_stress)** 0.5 )),0)                
                    self.bolt.calculate_bolt_capacity(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                                              bolt_grade_provided=float(self.bolt.bolt_grade_provided),
                                              conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,
                                              n_planes=self.planes, e=float(self.bolt.min_end_dist_round),
                                              p=float(self.bolt.min_pitch_round))
                    num_bolts = float(self.tensile_force) / ( self.bolt.bolt_capacity / 1000)
                    # print("num_bolts",num_bolts)    
                    
                    if num_bolts <= 2:
                        self.bolt_dia_grade_status = True
                        break
                    
                    
                if self.bolt_dia_grade_status == True:
                    break 

        if self.dia_available == False:
            self.design_status = False
            logger.warning(" : The combined thickness ({} mm) exceeds the allowable large grip limit check (of {} mm) for the minimum available "
                           "bolt diameter of {} mm [Ref. Cl.10.3.3.2, IS 800:2007]."
                           .format((float(self.plate1thk) + float(self.plate2thk)),(8*self.bolt.bolt_diameter[-1]),self.bolt.bolt_diameter[-1]))
            logger.error(": Design is not safe. \n ")
            logger.info(" :=========End Of design===========")

        # elif self.dia_available == True and self.bolt_dia_grade_status == False:
        #     self.design_status = True
        #     if self.bolt.bolt_type == 'Bearing Bolt':
        #         self.bolt.bolt_bearing_capacity = round(float(self.bolt.bolt_bearing_capacity),2)
        #     self.bolt.bolt_shear_capacity = round(float(self.bolt.bolt_shear_capacity),2)
        #     self.bolt.bolt_capacity = round(float(self.bolt.bolt_capacity),2)       
        #     print(self.bolt)
        #     self.number_r_c_bolts(self, design_dictionary)

        
        else:
            self.design_status = True
            if self.bolt.bolt_type == 'Bearing Bolt':
                self.bolt.bolt_bearing_capacity = round(float(self.bolt.bolt_bearing_capacity),2)
            self.bolt.bolt_shear_capacity = round(float(self.bolt.bolt_shear_capacity),2)
            self.bolt.bolt_capacity = round(float(self.bolt.bolt_capacity),2)       
            # print(self.bolt)
            self.number_r_c_bolts(self, design_dictionary,0,0)


    def number_r_c_bolts(self,design_dictionary,count=0,hit=0):
        
        bolt_cap = self.bolt.bolt_capacity
        if self.bolt.bolt_type == 'Bearing Bolt':
            self.slip_res = 'N/A'
        else:
            self.slip_res = self.bolt.bolt_capacity
            self.bolt.bolt_bearing_capacity = 'N/A'
            self.bolt.bolt_shear_capacity = 'N/A'
            
        # print("fafafa",bolt_cap)
        
        if hit == 0:
            self.number_bolts = float(self.tensile_force) /( bolt_cap / 1000)
        else:
            self.number_bolts += 1
        
        print("Hit",hit,self.number_bolts)
        
        self.number_bolts = math.ceil(self.number_bolts)
        if self.number_bolts < 2:
            self.number_bolts = 2

        def check_no_cols(numbolts):  #in function for recursive call
            if (2 * self.bolt.min_end_dist_round) + ((numbolts - 1 )*self.bolt.min_pitch_round) >= float(self.width):
                return True
            else:
                return False

        self.cols = 1
        self.rows = self.number_bolts
        temp_rows = self.rows
        while True:
            if check_no_cols(temp_rows):
                temp_rows = math.ceil(self.rows/(self.cols + 1))
                self.cols += 1
            else:
                break
        self.rows = math.ceil(self.rows/self.cols)  

        if self.cols>1:
            self.len_conn = (self.cols - 1)*self.bolt.min_pitch_round + 2*self.bolt.min_end_dist_round

        else:
            self.len_conn = self.bolt.min_pitch_round + 2*self.bolt.min_end_dist_round
        if self.number_bolts >= 2 and count == 0:
            self.design_status = True
            # print("Num bolts leaving",self.number_bolts)
            self.check_capacity_reduction_1(self, design_dictionary)
        elif self.number_bolts>=2 and count == 1:
            self.design_status = True
            self.final_formatting(self,design_dictionary)
        else:
            self.design_status = False
            logger.error(": Number of min bolts not satisfied. \n ")
            logger.info(" :=========End Of design===========")


    def check_capacity_reduction_1(self,design_dictionary):
        # print("Capacity red check 1")
        if self.number_bolts > 2:
            lg = (self.rows - 1)*self.bolt.min_pitch_round
            if  lg > 15 * self.bolt.bolt_diameter_provided:
                self.bij = 1.075 - (lg / (200 * self.bolt.bolt_diameter_provided))
        if self.bij >= 0.75 and self.bij <= 1.0:
            self.cap_red = True
            # print("1 cap red")
            self.bolt.bolt_shear_capacity = self.bolt.bolt_shear_capacity * self.bij
            if self.bolt.bolt_type == 'Bearing Bolt':
                self.bolt.bolt_capacity = min(self.bolt.bolt_shear_capacity, self.bolt.bolt_bearing_capacity)
            else:
                self.slip_res = self.bolt.bolt_shear_capacity
                self.bolt.bolt_capacity = self.slip_res


        self.design_status = True
        self.check_capacity_reduction_2(self,design_dictionary)

    def check_capacity_reduction_2(self,design_dictionary):
        self.cap_red = False
        # print("Capacity red check 2")
        if self.plate1thk + self.plate2thk > 5 * self.bolt.bolt_diameter_provided:
            self.blg = 8 / (3 + (self.plate1thk + self.plate2thk / self.bolt.bolt_diameter_provided))
        if self.blg < self.bij and self.blg != 0:
            self.cap_red = True
            # print("blg",self.blg)
            # print("2 cap red")
            self.bolt.bolt_shear_capacity = self.bolt.bolt_shear_capacity * self.blg
            if self.bolt.bolt_type == 'Bearing Bolt':
                self.bolt.bolt_capacity = min(self.bolt.bolt_shear_capacity, self.bolt.bolt_bearing_capacity)
            else:
                self.slip_res = self.bolt.bolt_shear_capacity
                self.bolt.bolt_capacity = self.slip_res
            
            self.number_r_c_bolts(self,design_dictionary,1,0)
        
        if self.cap_red == False:
            self.design_status = True
            # print("Going to formatting")
            # print("After checks 2 numbolts",self.number_bolts)
            self.final_formatting(self,design_dictionary)



    def final_formatting(self,design_dictionary):
        # print("I am herefa fafjafjafjafjajfjafajf")
        # print(self.bolt)

        gauge_dist = (float(self.width) - 2*self.bolt.min_end_dist_round)/(self.rows - 1)

        if gauge_dist > self.max_gauge_round:
            self.final_gauge = self.max_gauge_round
            self.final_pitch = self.bolt.min_pitch_round

            enddist = (float(self.width) - ((self.rows - 1)*self.final_gauge))/2
            if enddist > self.bolt.max_end_dist_round:
                self.design_status = False
                self.number_r_c_bolts(self,design_dictionary,0,1)
                # print("okay")
                
                # self.design_status = True
            else:
                self.final_end_dist = enddist
                self.final_edge_dist = enddist
                self.design_status = True
        else:
            self.final_gauge = gauge_dist
            self.final_pitch = self.bolt.min_pitch_round
            enddist = (float(self.width) - ((self.rows - 1)*self.final_gauge))/2
            if enddist > self.bolt.max_end_dist_round:
                # self.loop_helper_func(self,design_dictionary)
                # print("okay")
                # self.design_status = False
                self.design_status = False
                self.number_r_c_bolts(self,design_dictionary,0,1)

                
            else:
                self.final_end_dist = enddist
                self.final_edge_dist = enddist
                self.design_status = True
        # print("I got here")
        if self.bolt.bolt_type == 'Bearing Bolt':
            self.bolt.bolt_shear_capacity = self.bolt.bolt_shear_capacity/ 1000
            self.bolt.bolt_bearing_capacity = self.bolt.bolt_bearing_capacity / 1000
            self.bolt.bolt_bearing_capacity = round(self.bolt.bolt_bearing_capacity, 2)
            self.bolt.bolt_shear_capacity = round(self.bolt.bolt_shear_capacity, 2)
            self.bolt.bolt_capacity = self.bolt.bolt_capacity / 1000
            self.bolt.bolt_capacity = round(self.bolt.bolt_capacity, 2)
        else:
            self.slip_res = self.slip_res / 1000
            self.slip_res = round(self.slip_res, 2)
            self.bolt.bolt_capacity = self.bolt.bolt_capacity / 1000
            self.bolt.bolt_capacity = round(self.bolt.bolt_capacity, 2)
        
        # print("Going for util ratio")
        # print("Still here")
        # print("Numbolts",self.number_bolts)
        bltcap = self.bolt.bolt_capacity
        if bltcap < 1:
            bltcap = 1
        self.utilization_ratio = float(self.tensile_force) / (bltcap * self.number_bolts)
        self.utilization_ratio = round(self.utilization_ratio, 2)

        self.final_gauge = round(self.final_gauge,0)
        self.final_pitch = round(self.final_pitch,0)
        # print("fafafafafa",self.final_edge_dist, self.final_end_dist, self.final_pitch, self.final_gauge)
        print("FINAL FINAL",self.bolt)
        print("Final Edge/End/Gauge/Pitch",self.final_edge_dist,self.final_end_dist,self.final_gauge,self.final_pitch)

        # print(self)
        # print("faahfnafanfaf")
        print("Max and min end edge dist ",self.bolt.max_end_dist_round, self.bolt.min_end_dist_round, self.bolt.max_edge_dist_round, self.bolt.min_edge_dist_round)
        print("Max min gauge pitch dist",self.max_gauge_round,self.bolt.min_gauge_round, self.max_pitch_round, self.bolt.min_pitch_round)
        # self.design_status = True



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

    