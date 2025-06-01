"""
Module: butt_joint_welded.py
Author: Aman
Date: 2025-02-26

Description:
    ButtJointWelded is a moment connection module that represents a welded butt joint connection.
    It inherits from MomentConnection and follows the same structure and design logic as other
    connection modules (e.g., BeamCoverPlate, ColumnCoverPlate) used in Osdag.
    
Reference:
    - Osdag software guidelines and connection module structure documentation
"""

from .moment_connection import MomentConnection
from ...utils.common.component import *
from ...utils.common.is800_2007 import IS800_2007
from ...utils.common.is800_2007 import *
from ...Common import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...Report_functions import *
from ...utils.common.load import Load
import logging

import math

from PyQt5 import Qt

# Constants
KEY_SKEW_ANGLE = "SkewAngle"

class ButtJointWelded(MomentConnection):
    def __init__(self):
        super(ButtJointWelded, self).__init__()
        self.design_status = False
        self.weld_size = None
        self.weld_length_provided = None
        self.weld_strength = None
        self.weld_thickness = None
        self.plate_width = None
        self.plate_length = None
        self.plate_thickness = None
        self.weld_type = None
        self.weld_material = None
        self.weld_fabrication = None
        self.weld_angle = None
        self.weld_length_effective = None


    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []
        tabs.append((("Weld", TYPE_TAB_2, self.weld_values))) # added this line t.s.
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
        return tabs

    def tab_value_changed(self):
        # No tab value dependencies needed for bolt and detailing
        return []

    def edit_tabs(self):
        return []  # Keep original empty implementation

    def input_dictionary_design_pref(self):
        design_input = []
        design_input.append(("Weld", TYPE_COMBOBOX, [
            KEY_DP_WELD_TYPE,
            KEY_DP_WELD_MATERIAL_G_O
        ]))
        design_input.append(("Detailing", TYPE_COMBOBOX, [
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DP_DETAILING_PACKING_PLATE
        ]))
        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []
        design_input.append((None, [
            KEY_DP_WELD_TYPE,
            KEY_DP_WELD_MATERIAL_G_O,
            KEY_DP_DETAILING_EDGE_TYPE,
            KEY_DP_DETAILING_PACKING_PLATE
        ], ''))
        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):
        # Default values as per requirements
        defaults = {
            #chnged design preference values for weld fabrication and material grade t.s.
            KEY_DP_WELD_TYPE:"Shop weld",
            KEY_DP_WELD_MATERIAL_G_O:"E70XX", # not sure about what value to write in default t.s.
            KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
            KEY_DP_DETAILING_PACKING_PLATE: "Yes" 
        }
        return defaults.get(key)

    def detailing_values(self, input_dictionary):
        values = {
            KEY_DP_DETAILING_EDGE_TYPE: 'Sheared or hand flame cut',
            KEY_DP_DETAILING_PACKING_PLATE: 'Yes',
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

        t49 = (KEY_DP_DETAILING_PACKING_PLATE, KEY_DISP_DP_DETAILING_PACKING_PLATE, TYPE_COMBOBOX,
               ['Yes', 'No'], values[KEY_DP_DETAILING_PACKING_PLATE])
        detailing.append(t49)

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

    # added weld function

    def weld_values(self, input_dictionary):
        values = {
            KEY_DP_WELD_TYPE:'Shop weld',
            KEY_DP_WELD_MATERIAL_G_O:'E70XX', # not sure about what value to write in default t.s.
        }

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        weld = [] #need to check if it exists

        t3 = (KEY_DP_WELD_TYPE,"Type",TYPE_COMBOBOX,
            ['Shop weld', 'Field weld'], 
            values[KEY_DP_WELD_TYPE])
        weld.append(t3)

        t2 = (KEY_DP_WELD_MATERIAL_G_O, "Material Grade", TYPE_TEXTBOX, #taking textbox input here need to check
            None, 
            values[KEY_DP_WELD_MATERIAL_G_O])
        weld.append(t2)
        return weld

        
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
    # not sure about this function no changes done here -t.s.

    def input_values(self):
        options_list = []
        
        t16 = (KEY_MODULE, KEY_DISP_BUTTJOINTWELDED, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t5 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t5)

        t31 = (KEY_PLATE1_THICKNESS, KEY_DISP_PLATE1_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t31)

        t34 = (KEY_PLATE2_THICKNESS, KEY_DISP_PLATE2_THICKNESS, TYPE_COMBOBOX, VALUES_PLATETHK_CUSTOMIZED, True, 'Int Validator')
        options_list.append(t34)

        t35 = (KEY_PLATE_WIDTH, KEY_DISP_PLATE_WIDTH, TYPE_TEXTBOX, None, True, 'Float Validator')
        options_list.append(t35)

        t6 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t6)

        t36 = (KEY_COVER_PLATE, KEY_DISP_COVER_PLT, TYPE_COMBOBOX, VALUES_COVER_PLATE, True, 'No Validator')
        options_list.append(t36)

        t18 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t18)

        t20 = (KEY_WELD_SIZE, KEY_DISP_WELD_SIZE, TYPE_TEXTBOX, None, True, 'Float Validator')
        options_list.append(t20)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t17 = (KEY_TENSILE_FORCE, KEY_DISP_TENSILE_FORCE, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t17)

        return options_list

    #def customized_input(self):
     #   list1 = []
        #t11 = (KEY_GRD, self.grdval_customized)
        #list1.append(t11)
        #t13 = (KEY_D, self.diam_bolt_customized)
        #list1.append(t13)
        # t5 = (KEY_PLATE1_THICKNESS, self.plate_thick_customized)
        # list1.append(t5)
        # t6 = (KEY_PLATE2_THICKNESS, self.plate_thick_customized)
        # list1.append(t6)
        
       # return list1
    # removed this function bcz no need of customized input as of now t.s.
    
    
    def spacing(self, status):
        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details - 3 x 3 pattern considered")
        spacing.append(t00)

        t99 = (None, 'Spacing Details', TYPE_SECTION,
            [str(files("osdag.data.ResourceFiles.images").joinpath("spacing_3.png")), 400, 277, ""])  # [image, width, height, caption]
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t10)

        t111 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t111)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
        spacing.append(t12)

        return spacing

    def output_values(self, flag):
        """Return list of output values for display"""
        out_list = []
        
        # Cover plate details
        t44 = (None, DISP_TITLE_COVER_PLATE, TYPE_TITLE, None, True)
        out_list.append(t44)

        t22 = (KEY_OUT_UTILISATION_RATIO, KEY_OUT_DISP_UTILISATION_RATIO, TYPE_TEXTBOX,
               self.utilization_ratio if flag else '', True)
        out_list.append(t22)

        # Calculate cover_type only if flag is True and we have the planes attribute
        cover_type = ''
        if flag and hasattr(self, 'planes'):
            cover_type = "Double" if self.planes == 2 else "Single"
            
        t13 = (KEY_OUT_NO_COVER_PLATE, KEY_OUT_DISP_NO_COVER_PLATE, TYPE_TEXTBOX,
               cover_type if flag else '', True)
        out_list.append(t13)

        t38 = (KEY_OUT_WIDTH_COVER_PLATE, KEY_OUT_DISP_WIDTH_COVER_PLATE, TYPE_TEXTBOX,
               self.width if flag else '', True)
        out_list.append(t38)

        t28 = (KEY_OUT_LENGTH_COVER_PLATE, KEY_OUT_DISP_LENGTH_COVER_PLATE, TYPE_TEXTBOX,
               self.connection_length if flag else '', True)
        out_list.append(t28)

        t47 = (KEY_OUT_THICKNESS_COVER_PLATE, KEY_OUT_DISP_THICKNESS_COVER_PLATE, TYPE_TEXTBOX,
               self.Tcp if flag else '', True)
        out_list.append(t47)

        if hasattr(self, 'packing_thickness') and self.packing_thickness > 0:
            t15 = (KEY_PK_PLTHK, KEY_DISP_PK_PLTHK, TYPE_TEXTBOX,
                  self.packing_thickness if flag else '', True)
            out_list.append(t15)

        # Weld details
        t21 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t21)

        t23 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX,
               "Fillet" if flag else '', True)
        out_list.append(t23)

        t24 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX,
               self.weld_size if flag else '', True)
        out_list.append(t24)

        t25 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
               self.weld_strength if flag else '', True)
        out_list.append(t25)

        t26 = (KEY_OUT_WELD_LENGTH_EFF, KEY_OUT_DISP_WELD_LENGTH_EFF, TYPE_TEXTBOX,
               self.weld_length_effective if flag else '', True)
        out_list.append(t26)

        t27 = (KEY_OUT_BOLT_CONN_LEN, KEY_OUT_DISP_BOLT_CONN_LEN, TYPE_TEXTBOX,
               self.connection_length if flag else '', True)
        out_list.append(t27)

        return out_list

    def module_name(self):

        return KEY_DISP_BUTTJOINTWELDED

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

        t30 = ('Model', self.call_3DModel)
        components.append(t30)

        t32 = ('Plate1', self.call_3DColumn)
        components.append(t32)

        t37 = ('Plate2', self.call_3DPlate)
        components.append(t37)

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

        print(f'flag = {flag}, flag1 = {flag1}, flag2 = {flag2}')
        if flag  and flag1 and flag2:
            self.set_input_values(self, design_dictionary)
        else:
            return all_errors
        
    def set_input_values(self, design_dictionary):
        "initialisation of components required to design a butt joint welded along with connection"
        super(ButtJointWelded,self).set_input_values(self, design_dictionary)
        print(design_dictionary,"input values are set. Doing preliminary member checks")
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Butt Joint Welded Connection"
        
        # self.plate_thickness = [3,4,6,8,10,12,14,16,20,22,24,25,26,28,30,32,36,40,45,50,56,63,80]
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.tensile_force = design_dictionary[KEY_TENSILE_FORCE]
        self.width = design_dictionary[KEY_PLATE_WIDTH]

        # print(self.sizelist)
        self.efficiency = 0.0
        self.K = 1
        self.count = 0
        self.plate1 = Plate(thickness=[design_dictionary[KEY_PLATE1_THICKNESS]],
                        material_grade=design_dictionary[KEY_MATERIAL],
                        width=design_dictionary[KEY_PLATE_WIDTH])
        self.plate2 = Plate(thickness=[design_dictionary[KEY_PLATE2_THICKNESS]],
                            material_grade=design_dictionary[KEY_MATERIAL],
                            width=design_dictionary[KEY_PLATE_WIDTH])
        
        self.weld = Weld(size=design_dictionary[KEY_DP_WELD_SIZE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],
                         type=design_dictionary[KEY_DP_WELD_TYPE]
                         )
        # Start design process
        print("input values are set. Doing preliminary member checks")
        self.member_design_status = False
        self.max_limit_status_1 = False
        self.max_limit_status_2 = False
        self.weld_design_status = False
        self.thick_design_status = False
        self.plate_design_status = False
        self.initial_member_capacity(self,design_dictionary)


        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        Tmin = min(plate1_thk, plate2_thk)
        cover_plate_type_str = design_dictionary[KEY_COVER_PLATE]

        # Cover plate and packing plate logic as per documentation
        available_thicknesses = [float(thk) for thk in PLATE_THICKNESS_SAIL]
        if "double" in cover_plate_type_str.lower():
            self.planes = 2
            Tcp = math.ceil((9.0 / 16.0) * Tmin)  # Double cover plate thickness as per Eq. 3.2
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )

            # Packing plate logic as per Cl. 10.3.3.2
            if abs(plate1_thk - plate2_thk) > 0.001:
                self.packing_plate_thickness = abs(plate1_thk - plate2_thk)
            else:
                self.packing_plate_thickness = 0.0

        elif "single" in cover_plate_type_str.lower():
            self.planes = 1
            Tcp = math.ceil((5.0 / 8.0) * Tmin)  # Single cover plate thickness as per Eq. 3.1
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )
            self.packing_plate_thickness = 0.0

        else:
            self.planes = 1
            Tcp = Tmin
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )
            self.packing_plate_thickness = 0.0

        self.leg_size = 0
        self.yield_strength = 0
        self.partial_safety_factor = 0
        self.max_weld_size = 0
        #change from here
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
        self.cover_plate = design_dictionary[KEY_COVER_PLATE]
        
        # Start bolt selection process
        self.design_of_weld(self,design_dictionary)
    
    #========================DESIGN OF WELD==================================================================
    def design_of_weld(self,design_dictionary):
        self.effective_throat_thickness = float(design_dictionary[KEY_EFF_THROAT_THICKNESS])
        #might need to change this
        self.design_strength = float(design_dictionary[KEY_DESIGN_STRENGTH_WELD]) #might need to change this
        self.weld_size = float(design_dictionary[KEY_WELD_SIZE])
        self.fu = design_dictionary[KEY_DP_WELD_MATERIAL_G_O]  # Weld material grade
        # Determine weld type and set gamma_mw based on it
        weld_type = design_dictionary[KEY_DP_WELD_TYPE]
        if weld_type == "Shop weld":
            self.gamma_mw = 1.25  
        else:  
            self.gamma_mw = 1.50  
        self.weld_design_strength = self.fu / (math.sqrt(3) * self.gamma_mw)
        
        # Call the design sequence methods in order
        self.weld_length(design_dictionary)
        self.weld_strength_verification(design_dictionary)
        self.long_joint_reduction_factor()
        self.check_base_metal_strength(design_dictionary)
    
    def weld_length(self, design_dictionary):
        self.tensile_force = design_dictionary[KEY_TENSILE_FORCE]
        self.plates_width = design_dictionary[KEY_PLATE_WIDTH]
        self.weld_size = design_dictionary[KEY_WELD_SIZE]
        self.cover_plate = design_dictionary[KEY_COVER_PLATE]
        # Dictionary to store output values for UI display
        self.output_values = {}
        self.material = design_dictionary[KEY_MATERIAL]
        self.fu = design_dictionary[KEY_DP_WELD_MATERIAL_G_O]
        self.weld_type = design_dictionary[KEY_DP_WELD_TYPE]
        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        self.alpha = design_dictionary[KEY_SKEW_ANGLE]



        self.s_min = IS800_2007.cl_10_5_2_3_min_weld_size(plate1_thk, plate2_thk)
        Tmin = min(plate1_thk, plate2_thk)
        self.s_max = Tmin - 1.5
        if self.weld_size < self.s_min or self.weld_size > self.s_max:
                self.design_status = False
                if self.weld_size < self.s_min:
                    logger.error(": Weld size {} mm is less than the minimum required weld size of {} mm [Ref. Table 21, Cl.10.5.2.3, IS 800:2007].".format(
                        self.weld_size, self.s_min))
                    logger.info(": Increase the weld size.")
                else:
                    logger.error(": Weld size {} mm is greater than the maximum allowed weld size of {} mm [Ref. Cl.10.5.3.1, IS 800:2007].".format(
                        self.weld_size, self.s_max))
                    logger.info(": Decrease the weld size.")
                logger.error(": Design is unsafe. \n")
                logger.info(" :=========End Of design===========")
                return
        else:
                # Calculate weld length since size is acceptable
                if "shop weld" in self.weld_type.lower():
                    self.gamma_mw = 1.25
                else:
                    self.gamma_mw = 1.50

                self.f_w = self.fu / (math.sqrt(3) * self.gamma_mw)  # Design strength of weld

                if "single" in self.cover_plate.lower():
                    self.N_f = 1  # Number of welds
                else:
                    self.N_f = 2  # Double cover plate means two weld interfaces

                # Calculate required weld length 
                self.L_req = self.tensile_force / (self.N_f * 0.707 * self.weld_size * self.f_w)
            
        # Check if straight weld is sufficient
        if self.L_req <= self.plates_width:
            logger.info(": Straight weld will be provided as required length is less than plate width")
            self.weld_length_provided = self.plates_width
            self.weld_length_effective = self.weld_length_provided
            self.weld_angle = 0
            self.side_weld_length = 0

        else:
            # Calculate skewed weld parameters
            L_target = self.L_req / self.N_f  # Required length per weld line
        
            # Calculate skew angle
            self.alpha = math.degrees(math.atan((L_target - self.plates_width)/(2 * self.plates_width)))

            # Constrain angle between 20-60 degrees
            if self.alpha < 20:
                self.alpha = 20
            elif self.alpha > 60:
                self.alpha = 60

            # Calculate provided length per weld line with skew
            L_provided_line = self.plates_width + 2 * self.plates_width * math.tan(math.radians(self.alpha))
            L_provided_total = self.N_f * L_provided_line

            # Check if side welds are needed
            if L_provided_total < self.L_req:
                # Calculate required side weld length
                L_side = (self.L_req - L_provided_total) / self.N_f

                # Calculate minimum return weld length
                min_return = max(2 * self.weld_size, 10)  # As per IS 800:2007 Cl 10.5.10.2
                L_side = max(L_side, min_return)

                self.side_weld_length = L_side
            else:
                self.side_weld_length = 0

            self.weld_length_provided = L_provided_total
            self.weld_length_effective = L_provided_total + (2 * self.side_weld_length * self.N_f)
            self.weld_angle = self.alpha
            logger.info(": Skewed weld will be provided with angle {:.2f} degrees".format(self.weld_angle))
        # Update output values for UI display
        self.output_values[KEY_OUT_WELD_LENGTH] = self.weld_length_effective
    
    def weld_strength_verification(self, design_dictionary):
        # Extract required values from the design dictionary
        self.weld_size = design_dictionary[KEY_WELD_SIZE]
        self.tensile_force = design_dictionary[KEY_TENSILE_FORCE]
        
        # Calculate effective length by subtracting 2 times weld size from provided length
        self.weld_length_effective = self.weld_length_provided - (2 * self.weld_size)
        
        # Check if effective length meets minimum requirement of 4 times weld size
        min_length = 4 * self.weld_size
        if self.weld_length_effective < min_length:
            self.design_status = False
            logger.error(f": Effective weld length {self.weld_length_effective:.2f} mm is less than minimum required length {min_length:.2f} mm")
            logger.info(": Increase the weld length or size")
            return
            
        # Calculate weld strength
        self.weld_strength = self.f_w * 0.707 * self.weld_size * self.weld_length_effective * self.N_f
        
        # Check if weld strength is adequate
        if self.weld_strength < self.tensile_force:
            self.design_status = False
            logger.error(f": Weld strength {self.weld_strength:.2f} N is less than required force {self.tensile_force:.2f} N")
            logger.info(": Increase weld size or length")
            return
        else:
            self.design_status = True
            self.utilization_ratio = self.tensile_force / self.weld_strength
            logger.info(f": Weld strength verification successful with utilization ratio {self.utilization_ratio:.2f}")
    
    def long_joint_reduction_factor(self):
        """Calculate reduction factor for long joints according to IS 800:2007 Cl. 10.5.7.1(b)"""
        
        # Calculate effective throat thickness
        a = 0.707 * self.weld_size
        
        # Check if reduction is needed
        if self.weld_length_effective <= 150 * a:
            self.beta_L = 1.0
            logger.info(": No reduction for long joints required as length is less than 150 times throat thickness")
            return
            
        # Calculate reduction factor
        self.beta_L = 1.2 - (0.2 * self.weld_length_effective)/(150 * a)
        
        # Ensure minimum value of 0.8
        self.beta_L = max(0.8, self.beta_L)
        
        # Adjust weld design strength
        self.f_w_adjusted = self.f_w * self.beta_L
        
        logger.info(f": Long joint reduction factor βL = {self.beta_L:.2f}")
        logger.info(f": Adjusted weld design strength = {self.f_w_adjusted:.2f} N/mm²")

    def check_base_metal_strength(self, design_dictionary):
        """Check strength of base metal according to IS 800:2007"""
        
        # Extract material properties
        self.fy = float(design_dictionary[KEY_MATERIAL])
        self.fu = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])
        
        # Partial safety factors
        self.gamma_m0 = 1.10  # For yielding
        self.gamma_m1 = 1.25  # For rupture
        
        # Calculate areas
        Tmin = min(float(design_dictionary[KEY_PLATE1_THICKNESS]), 
                   float(design_dictionary[KEY_PLATE2_THICKNESS]))
        self.A_g = Tmin * self.plates_width
        self.A_n = self.A_g  # For welded joints, net area equals gross area
        
        # Calculate design strength based on yielding and rupture
        T_dy = self.A_g * self.fy / self.gamma_m0
        T_du = 0.9 * self.A_n * self.fu / self.gamma_m1
        
        # Design base metal strength is minimum of the two
        self.T_db = min(T_dy, T_du)
        
        # Check if design force is less than base metal strength
        if self.tensile_force > self.T_db:
            self.design_status = False
            logger.error(f": Base metal strength {self.T_db:.2f} N is less than required force {self.tensile_force:.2f} N")
            logger.info(": Design is unsafe. Increase plate dimensions or use higher grade material")
            return
        else:
            logger.info(f": Base metal strength check passed. Utilization ratio = {self.tensile_force/self.T_db:.2f}")