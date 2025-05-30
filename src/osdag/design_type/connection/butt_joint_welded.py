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
from ...utils.common.is800_2007 import *
from ...Common import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...Report_functions import *
from ...utils.common.load import Load
import logging

import math

from PyQt5 import Qt

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
        self.utilization_ratio = None

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
               f"{self.utilization_ratio:.2f}", True)
        out_list.append(t22)

        cover_type = "Double" if self.planes == 2 else "Single"
        t13 = (KEY_OUT_NO_COVER_PLATE, KEY_OUT_DISP_NO_COVER_PLATE, TYPE_TEXTBOX,
               cover_type, True)
        out_list.append(t13)

        t38 = (KEY_OUT_WIDTH_COVER_PLATE, KEY_OUT_DISP_WIDTH_COVER_PLATE, TYPE_TEXTBOX,
               f"{self.width:.2f}", True)
        out_list.append(t38)

        t28 = (KEY_OUT_LENGTH_COVER_PLATE, KEY_OUT_DISP_LENGTH_COVER_PLATE, TYPE_TEXTBOX,
               f"{self.connection_length:.2f}", True)
        out_list.append(t28)

        t47 = (KEY_OUT_THICKNESS_COVER_PLATE, KEY_OUT_DISP_THICKNESS_COVER_PLATE, TYPE_TEXTBOX,
               f"{self.Tcp:.2f}", True)
        out_list.append(t47)

        if self.packing_thickness > 0:
            t15 = (KEY_PK_PLTHK, KEY_DISP_PK_PLTHK, TYPE_TEXTBOX,
                  f"{self.packing_thickness:.2f}", True)
            out_list.append(t15)

        # Weld details
        t21 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t21)

        t23 = (KEY_OUT_WELD_TYPE, KEY_OUT_DISP_WELD_TYPE, TYPE_TEXTBOX,
               "Fillet", True)
        out_list.append(t23)

        t24 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX,
               f"{self.weld_size:.2f}", True)
        out_list.append(t24)

        t25 = (KEY_OUT_WELD_STRENGTH, KEY_OUT_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
               f"{self.weld_strength:.2f}", True)
        out_list.append(t25)

        t26 = (KEY_OUT_WELD_LENGTH_EFF, KEY_OUT_DISP_WELD_LENGTH_EFF, TYPE_TEXTBOX,
               f"{self.weld_length_effective:.2f}", True)
        out_list.append(t26)

        t27 = (KEY_OUT_BOLT_CONN_LEN, KEY_OUT_DISP_BOLT_CONN_LEN, TYPE_TEXTBOX,
               f"{self.connection_length:.2f}", True)
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
        """Initialize components required for butt joint design as per flowchart"""
        # Initialize basic parameters
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Butt Joint Welded Connection"
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.tensile_force = float(design_dictionary[KEY_TENSILE_FORCE])
        self.width = float(design_dictionary[KEY_PLATE_WIDTH])
        self.cover_plate = design_dictionary[KEY_COVER_PLATE]
        
        # Initialize plates with material properties
        self.plate1 = Plate(thickness=[design_dictionary[KEY_PLATE1_THICKNESS]],
                        material_grade=design_dictionary[KEY_MATERIAL],
                        width=design_dictionary[KEY_PLATE_WIDTH])
        self.plate2 = Plate(thickness=[design_dictionary[KEY_PLATE2_THICKNESS]],
                        material_grade=design_dictionary[KEY_MATERIAL],
                        width=design_dictionary[KEY_PLATE_WIDTH])
        
        # Initialize weld with properties
        self.weld = Weld(size=design_dictionary[KEY_WELD_SIZE], 
                        weld_type=design_dictionary[KEY_DP_WELD_TYPE],
                        edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE])
        
        # Start design process
        self.design_procedure()

    def design_procedure(self):
        """Main design procedure following IS 800:2007 code requirements"""
        
        # Initialize safety factors as per Table 5 (Cl. 5.4.1)
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']  # 1.10
        self.gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['ultimate_stress']  # 1.25
        self.gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.weld.fabrication]  # 1.25 for shop, 1.5 for field
        
        # Get plate thicknesses and minimum thickness
        self.t1 = float(self.plate1.thickness[0])
        self.t2 = float(self.plate2.thickness[0])
        self.Tmin = min(self.t1, self.t2)
        
        # Calculate cover plate thickness based on type
        self.calculate_cover_plate_thickness()
        
        # Get weld size and check limits as per Cl. 10.5.2.3
        self.weld_size = float(self.weld.size)
        
        # value of a eq. 3.4
        self.effective_throat_thickness = 0.707 * self.weld_size
        
        # f_wd calculated from eq. 3.5
        self.f_y = self.plate1.fy
        self.f_u = self.plate1.fu
        self.f_wd = self.f_u / (math.sqrt(3) * self.gamma_mw)  
        
        min_weld_size = self.get_min_weld_size()
        max_weld_size = self.Tmin - 1.5
        
        if self.weld_size < min_weld_size:
            self.design_status = False
            logger.error(f": Weld size {self.weld_size}mm is less than minimum required size {min_weld_size}mm as per Table 21")
            return
        
        if self.weld_size > max_weld_size:
            self.design_status = False
            logger.error(f": Weld size {self.weld_size}mm exceeds maximum allowed size {max_weld_size}mm")
            return
        
        # Convert from kN to N
        self.tensile_force_N = self.tensile_force * 1000
        
        self.L_req = self.tensile_force_N / (self.f_wd * self.effective_throat_thickness * self.planes)
        
        if self.L_req <= self.width:
            # Use straight welds
            self.L_provided = self.width
            self.alpha = 0
            self.L_side = 0
        else:
            self.extend_weld_length()
        
        self.L_eff = self.L_provided - 2 * self.effective_throat_thickness
        
        # Check if L_eff ≥ 4s
        if self.L_eff < 4 * self.weld_size:
            self.design_status = False
            logger.error(": Effective weld length is less than minimum required length")
            logger.error(": Error: Increase weld size or length")
            return
        else:
            # Calculate weld capacity C_w
            self.weld_capacity = self.f_wd * self.effective_throat_thickness * self.L_eff * self.planes
            
            # Check if P_N < C_w
            if self.tensile_force_N > self.weld_capacity:
                self.design_status = False
                logger.error(": Weld strength is insufficient")
                logger.error(": Error: Revise weld size or overlap")
                return
            else:
                # Base metal strength check
                self.A_g = self.width * self.Tmin  
                self.A_n = self.A_g 
                
                
                self.T_db = min(
                    (self.A_g * self.f_y) / self.gamma_m0,
                    (0.9 * self.A_n * self.f_u) / self.gamma_m1
                )
                
                # Check if P_N ≤ T_db
                if self.tensile_force_N > self.T_db:
                    self.design_status = False
                    logger.error(": Base metal strength is insufficient")
                    logger.error(": Error: Revise section")
                    return
                else:
                    # Design is successful - Output detailing values
                    self.design_status = True
                    self.connection_length = self.L_provided + 2 * 25  # L_cp = L_provided + 2×clearance
                    self.utilization_ratio = max(
                        self.tensile_force_N / self.weld_capacity,
                        self.tensile_force_N / self.T_db
                    )
                    logger.info(": Design is safe")
                    return True

    def calculate_cover_plate_thickness(self):
        if "double" in self.cover_plate.lower():
            self.Tcp = (9.0/16.0) * self.Tmin
            self.planes = 2
        else:
            self.Tcp = (5.0/8.0) * self.Tmin
            self.planes = 1
        
        available_thicknesses = [float(thk) for thk in PLATE_THICKNESS_SAIL]
        self.Tcp = min([t for t in available_thicknesses if t >= self.Tcp], default=self.Tcp)

        # Add packing plate if needed
        if self.t1 != self.t2:
            self.packing_thickness = abs(self.t1 - self.t2)
        else:
            self.packing_thickness = 0

    def extend_weld_length(self):
        self.L_tgt = self.L_req / self.planes
        
        # Calculate skew angle
        self.alpha = math.degrees(math.atan((self.L_tgt - self.width)/(2 * self.width)))
        
        # Check angle limits
        if self.alpha < 20:
            self.alpha = 20
        elif self.alpha > 60:
            self.alpha = 60
        
        self.L_provided_line = self.width + 2 * self.width * math.tan(math.radians(self.alpha))
        self.L_provided = self.planes * self.L_provided_line
        
        # check this logic
        if self.alpha == 60:
            self.L_side = (self.L_req - self.L_provided) / self.planes
        else:
            self.L_side = 0

    def get_min_weld_size(self):
        thicker_part = max(float(self.plate1.thickness[0]), float(self.plate2.thickness[0]))
        
        if thicker_part <= 10:
            return 3
        elif thicker_part <= 20:
            return 5
        elif thicker_part <= 32:
            return 6
        elif thicker_part <= 50:
            return 8
        else:
            return 10

    ################################ Outlist Dict #####################################################################################