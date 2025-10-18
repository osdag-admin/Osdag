"""
Module: butt_joint_bolted.py
Author: Tarandeep
Date: 2025-02-26

Description:
    ButtJointBolted is a moment connection module that represents a bolted butt joint connection.
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
import os
from importlib.resources import files


class ButtJointBolted(MomentConnection):
    def __init__(self):
        super(ButtJointBolted, self).__init__()
        self.design_status = False
        self.design_for = 'Tension'
        self.axial_force_kN = 0.0
        self.axial_force = 0.0
        self.base_metal_capacity_kN = None
        self.utilization_breakdown = {}
        self.design_error = ''
        self.spacing = None
        self.packing_plate_thickness = 0.0
        self.beta_pkg = 1.0
        self.calculated_cover_plate_thickness = 0.0
        # Create placeholder files on initialization
        self.create_placeholder_files()

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []
        # Bolt, Detailing, and Design tabs
        tabs.append(("Bolt", TYPE_TAB_2, self.bolt_values))
        tabs.append(("Detailing", TYPE_TAB_2, self.detailing_values))
        tabs.append(("Design", TYPE_TAB_2, self.design_values))
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
            KEY_DP_DETAILING_EDGE_TYPE,KEY_DP_DETAILING_PACKING_PLATE
        ], ''))

        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):
        # Default values as per requirements
        defaults = {
            KEY_DP_BOLT_TYPE: "Non Pre-tensioned",
            KEY_DP_BOLT_HOLE_TYPE: "Standard",
            KEY_DP_BOLT_SLIP_FACTOR: "0.3",
            KEY_DP_DETAILING_EDGE_TYPE: "Sheared or hand flame cut",
            KEY_DP_DETAILING_PACKING_PLATE: "Yes"
        }
        return defaults.get(key)

    def detailing_values(self, input_dictionary):
        values = {
            KEY_DP_DETAILING_EDGE_TYPE: 'Sheared or hand flame cut',
            # KEY_DP_DETAILING_PACKING_PLATE: 'Yes',  # Commented out packing plate preference
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

        # Commented out packing plate design preference
        # t3 = (KEY_DP_DETAILING_PACKING_PLATE, KEY_DISP_DP_DETAILING_PACKING_PLATE, TYPE_COMBOBOX,
        #       ['Yes', 'No'], values[KEY_DP_DETAILING_PACKING_PLATE])
        # detailing.append(t3)

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
    def design_values(self, input_dictionary):
        values = {
            KEY_DESIGN_FOR: 'Tension'
        }

        if input_dictionary and KEY_DESIGN_FOR in input_dictionary:
            values[KEY_DESIGN_FOR] = input_dictionary[KEY_DESIGN_FOR]

        design = []
        t1 = (KEY_DESIGN_FOR, KEY_DISP_DESIGN_FOR, TYPE_COMBOBOX,
              ['Tension', 'Compression'], values[KEY_DESIGN_FOR])
        design.append(t1)

        return design

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

        t16 = (KEY_MODULE, KEY_DISP_BUTTJOINTBOLTED, TYPE_MODULE, None, True, 'No Validator')
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

        t36 = (KEY_COVER_PLATE, KEY_DISP_COVER_PLATE, TYPE_COMBOBOX, VALUES_COVER_PLATE, True, 'No Validator')
        options_list.append(t36)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_AXIAL_FORCE, KEY_DISP_AXIAL_FORCE, TYPE_TEXTBOX, None, True, 'Float Validator')
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
        t5 = (KEY_PLATE1_THICKNESS, self.plate_thick_customized)
        list1.append(t5)
        t6 = (KEY_PLATE2_THICKNESS, self.plate_thick_customized)
        list1.append(t6)
        return list1

    def spacing(self, status):
        spacing = []

        t00 = (None, "", TYPE_NOTE, "Representative Image for Spacing Details - 3 x 3 pattern considered")
        spacing.append(t00)

        # Use a default image path that exists in the project
        t99 = (None, 'Spacing Details', TYPE_SECTION,
            [str(files("osdag.data.ResourceFiles.images").joinpath("ButtJointBolted.png")), 400, 277, ""])  # [image, width, height, caption]
        spacing.append(t99)

        t9 = (KEY_OUT_PITCH, KEY_OUT_DISP_PITCH, TYPE_TEXTBOX, self.plate.gauge_provided if status else '')
        spacing.append(t9)

        t10 = (KEY_OUT_END_DIST, KEY_OUT_DISP_END_DIST, TYPE_TEXTBOX, self.plate.edge_dist_provided if status else '')
        spacing.append(t10)

        t11 = (KEY_OUT_GAUGE, KEY_OUT_DISP_GAUGE, TYPE_TEXTBOX, self.plate.pitch_provided if status else '')
        spacing.append(t11)

        t12 = (KEY_OUT_EDGE_DIST, KEY_OUT_DISP_EDGE_DIST, TYPE_TEXTBOX, self.plate.end_dist_provided if status else '')
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
               self.bolt.bolt_type if flag else '', True)
        out_list.append(t31)

        t8 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
               self.bolt.bolt_shear_capacity if flag else '', True)
        out_list.append(t8)

        t4 = (KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX,
               self.bolt.bolt_bearing_capacity if flag else '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
               self.bolt.bolt_capacity if flag else '', True)
        out_list.append(t5)

        t17 = (None, DISP_TITLE_BOLTDS, TYPE_TITLE, None, True)
        out_list.append(t17)
        t17 = (KEY_OUT_TOT_NO_BOLTS, KEY_OUT_DISP_TOT_NO_BOLTS, TYPE_TEXTBOX,
               self.number_bolts if flag else '', True)
        out_list.append(t17)

        t11 = (KEY_PK_PLTHK, KEY_DISP_PK_PLTHK, TYPE_TEXTBOX,
               self.packing_plate_thickness if flag else '', True)
        out_list.append(t11)

        t18 = (KEY_OUT_ROW_PROVIDED, KEY_OUT_DISP_ROW_PROVIDED, TYPE_TEXTBOX,
               self.rows if flag else '', True)
        out_list.append(t18)

        t19 = (KEY_OUT_COL_PROVIDED, KEY_OUT_DISP_COL_PROVIDED, TYPE_TEXTBOX,
               self.cols if flag else '', True)
        out_list.append(t19)

        t29 = (KEY_UTILIZATION_RATIO, KEY_DISP_UTILIZATION_RATIO, TYPE_TEXTBOX,
               self.utilization_ratio if flag else '', True)
        out_list.append(t29)

        t30 = (KEY_OUT_DESIGN_FOR, KEY_OUT_DISP_DESIGN_FOR, TYPE_TEXTBOX, self.design_for if flag else '', True)
        out_list.append(t30)

        t31 = (KEY_OUT_BASE_METAL_CAPACITY, KEY_OUT_DISP_BASE_METAL_CAPACITY, TYPE_TEXTBOX,
                round(self.base_metal_capacity_kN, 2) if flag and self.base_metal_capacity_kN is not None else '', True)
        out_list.append(t31)

        t32 = (KEY_OUT_BASE_METAL_UTILIZATION, KEY_OUT_DISP_BASE_METAL_UTILIZATION, TYPE_TEXTBOX,
                self.utilization_breakdown.get('base_metal') if flag and self.utilization_breakdown else '', True)
        out_list.append(t32)

        t33 = (KEY_OUT_BOLT_UTILIZATION, KEY_OUT_DISP_BOLT_UTILIZATION, TYPE_TEXTBOX,
                self.utilization_breakdown.get('bolt') if flag and self.utilization_breakdown else '', True)
        out_list.append(t33)

        t20 = (KEY_OUT_BOLT_CONN_LEN, KEY_OUT_DISP_BOLT_CONN_LEN, TYPE_TEXTBOX,
               self.len_conn if flag else '', True)
        out_list.append(t20)

        return out_list

    def module_name(self):

        return KEY_DISP_BUTTJOINTBOLTED

    def call_3DColumn(self, ui, bgcolor):
        # Temporarily disabled 3D functionality
        pass
        # if ui.chkBxCol.isChecked():
        #     ui.btn3D.setChecked(Qt.Unchecked)
        #     ui.chkBxCol.setChecked(Qt.Unchecked)
        #     ui.mytabWidget.setCurrentIndex(0)
        # ui.commLogicObj.display_3DModel("Column", bgcolor)

    @staticmethod
    def get_3d_components(main=None):
        """Get 3D components for visualization"""
        # Create placeholder files if they don't exist
        ButtJointBolted.create_placeholder_files()

        # Return empty components list for now
        components = []

        # t1 = ('Model', self.call_3DModel)
        # components.append(t1)

        # t3 = ('Plate1', self.call_3DColumn)
        # components.append(t3)

        # t4 = ('Plate2', self.call_3DPlate)
        # components.append(t4)


        return components

    @staticmethod
    def create_placeholder_files():
        """Create placeholder files for 3D visualization if they don't exist"""
        try:
            # Get the absolute path of the current directory
            current_dir = os.path.abspath(os.path.dirname(__file__))
            images_dir = os.path.join(current_dir, '..', '..', '..', 'ResourceFiles', 'images')

            # Create directory if it doesn't exist
            os.makedirs(images_dir, exist_ok=True)

            # Create empty files
            image_files = ['3d.png', 'top.png', 'front.png', 'side.png']
            for filename in image_files:
                filepath = os.path.join(images_dir, filename)
                if not os.path.exists(filepath):
                    with open(filepath, 'w') as f:
                        pass
                    print(f"Created placeholder file: {filepath}")

        except Exception as e:
            print(f"Warning: Could not create placeholder files: {str(e)}")


    # def call_3DPlate(self, ui, bgcolor):
    #     from PyQt5.QtWidgets import QCheckBox
    #     from PyQt5.QtCore import Qt
    #     for chkbox in ui.frame.children():
    #         if chkbox.objectName() == 'Cover Plate':
    #             continue
    #         if isinstance(chkbox, QCheckBox):
    #             chkbox.setChecked(Qt.Unchecked)
    #     ui.commLogicObj.display_3DModel("Cover Plate", bgcolor)

    def get_3d_image_path(self):
        image_path = "./ResourceFiles/images/3d.png"
        fallback_image = str(files("osdag.data.ResourceFiles.images").joinpath("ButtJointBolted.png"))
        if not os.path.exists(image_path):
            return fallback_image
        return image_path

    def call_3DPlate(self, ui, bgcolor):
        # Temporarily disabled 3D functionality
        pass
        # from PyQt5.QtWidgets import QCheckBox
        # from PyQt5.QtCore import Qt
        # for chkbox in ui.frame.children():
        #     if chkbox.objectName() == 'Cover Plate':
        #         continue
        #     if isinstance(chkbox, QCheckBox):
        #         chkbox.setChecked(Qt.Unchecked)
        # ui.commLogicObj.display_3DModel("Cover Plate", bgcolor)

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
        """Initialize components required for butt joint design as per IS 800:2007"""

        design_dictionary_with_defaults = design_dictionary.copy()
        for key in (KEY_SHEAR, KEY_AXIAL, KEY_MOMENT):
            if key not in design_dictionary_with_defaults:
                design_dictionary_with_defaults[key] = 0.0

        super(ButtJointBolted, self).set_input_values(self, design_dictionary_with_defaults)

        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = "Butt Joint Bolted Connection"
        self.main_material = design_dictionary[KEY_MATERIAL]

        self.design_for = design_dictionary.get(KEY_DESIGN_FOR, 'Tension')
        axial_input = design_dictionary.get(
            KEY_AXIAL_FORCE,
            design_dictionary.get(KEY_AXIAL,
                                  design_dictionary.get(KEY_TENSILE_FORCE, 0)))
        axial_value = float(axial_input)
        if axial_value < 0 and KEY_DESIGN_FOR not in design_dictionary:
            self.design_for = 'Compression'
        self.axial_force_kN = abs(axial_value)
        self.axial_force = self.axial_force_kN * 1000.0
        # Legacy naming issue
        self.tensile_force = self.axial_force_kN  # legacy naming in downstream methods

        self.width = design_dictionary[KEY_PLATE_WIDTH]

        # Initialize plates with material properties
        self.plate1 = Plate(thickness=[design_dictionary[KEY_PLATE1_THICKNESS]],
                        material_grade=design_dictionary[KEY_MATERIAL],
                        width=design_dictionary[KEY_PLATE_WIDTH])
        self.plate2 = Plate(thickness=[design_dictionary[KEY_PLATE2_THICKNESS]],
                            material_grade=design_dictionary[KEY_MATERIAL],
                            width=design_dictionary[KEY_PLATE_WIDTH])

        # Initialize bolt with properties
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD],
                        diameter=design_dictionary[KEY_D],
                        bolt_type=design_dictionary[KEY_TYP],
                        bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                        edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                        mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None))

        # Calculate cover plate thickness as per Cl. 10.2.4.2
        plate1_thk = float(design_dictionary[KEY_PLATE1_THICKNESS])
        plate2_thk = float(design_dictionary[KEY_PLATE2_THICKNESS])
        Tmin = min(plate1_thk, plate2_thk)
        cover_plate_type_str = design_dictionary[KEY_COVER_PLATE]

        # Cover plate and packing plate logic as per documentation
        available_thicknesses = [float(thk) for thk in PLATE_THICKNESS_SAIL]
        if "double" in cover_plate_type_str.lower():
            self.planes = 2
            Tcp = math.ceil((9.0 / 8.0) * Tmin)  # Double cover plate thickness as per Eq. 3.2
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )

            # Packing plate logic as per Cl. 10.3.3.2
            if abs(plate1_thk - plate2_thk) > 0.001:
                self.packing_plate_thickness = abs(plate1_thk - plate2_thk)
                if self.packing_plate_thickness > 6.0:
                    # βpkg calculation as per Eq. 3.3
                    self.beta_pkg = (1.0 - 0.0125 * self.packing_plate_thickness)
                else:
                    self.beta_pkg = 1.0
            else:
                self.packing_plate_thickness = 0.0
                self.beta_pkg = 1.0

        elif "single" in cover_plate_type_str.lower():
            self.planes = 1
            Tcp = math.ceil((5.0 / 8.0) * Tmin)  # Single cover plate thickness as per Eq. 3.1
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )
            self.packing_plate_thickness = 0.0
            self.beta_pkg = 1.0

        else:
            self.planes = 1
            Tcp = Tmin
            self.calculated_cover_plate_thickness = min(
                [thk for thk in available_thicknesses if thk >= Tcp],
                default=Tcp
            )
            self.packing_plate_thickness = 0.0
            self.beta_pkg = 1.0

        # Initialize other parameters
        self.count = 0
        self.slip_res = None
        self.yield_stress = None
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
        self.cover_plate = design_dictionary[KEY_COVER_PLATE]

        # Start bolt selection process
        self.select_bolt_dia_and_grade(self,design_dictionary)

    def select_bolt_dia_and_grade(self,design_dictionary):
        self.dia_available = False
        self.bolt_dia_grade_status = False

        if not self.bolt.bolt_diameter or not self.bolt.bolt_grade:
            logger.error("No customized bolt diameters or grades provided.")
            self.design_status = False
            return

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

        # Add maximum iterations to prevent infinite loops
        max_diameter_iterations = len(self.bolt.bolt_diameter)
        max_grade_iterations = len(self.bolt.bolt_grade)
        diameter_iterations = 0
        grade_iterations = 0

        for self.bolt.bolt_diameter_provided in self.bolt.bolt_diameter:
            diameter_iterations += 1
            if diameter_iterations > max_diameter_iterations:
                logger.error("Maximum diameter iterations reached. No suitable bolt diameter found.")
                self.design_status = False
                return

            if 8 * float(self.bolt.bolt_diameter_provided) > (float(self.plate1thk) + float(self.plate2thk)):
                self.dia_available = True

                for self.bolt.bolt_grade_provided in self.bolt.bolt_grade:
                    grade_iterations += 1
                    if grade_iterations > max_grade_iterations:
                        logger.error("Maximum grade iterations reached. No suitable bolt grade found.")
                        self.design_status = False
                        return

                    try:
                        self.bolt.calculate_bolt_spacing_limits(bolt_diameter_provided=float(self.bolt.bolt_diameter_provided),
                                                            conn_plates_t_fu_fy=self.bolt_conn_plates_t_fu_fy,n=self.planes)

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
                        
                        #if num_bolts <= 2:
                        #    self.bolt_dia_grade_status = True
                        #    break
                        # Accept any valid combination, not just those with <= 2 bolts
                        self.bolt_dia_grade_status = True
                        break   

                    except Exception as e:
                        logger.error(f"Error in bolt calculations: {str(e)}")
                        continue

                if self.bolt_dia_grade_status == True:
                    break

        if self.dia_available == False:
            self.design_status = False
            logger.warning(" : The combined thickness ({} mm) exceeds the allowable large grip limit check (of {} mm) for the minimum available "
                           "bolt diameter of {} mm [Ref. Cl.10.3.3.2, IS 800:2007]."
                           .format((float(self.plate1thk) + float(self.plate2thk)),(8*self.bolt.bolt_diameter[-1]),self.bolt.bolt_diameter[-1]))
            logger.error(": Design is not safe. \n ")
            logger.info(" :=========End Of design===========")
            return

        if not self.bolt_dia_grade_status:
            self.design_status = False
            logger.error(": No suitable bolt diameter and grade combination found for the given requirements.")
            logger.info(" :=========End Of design===========")
            return

        self.design_status = True
        if self.bolt.bolt_type == 'Bearing Bolt':
            self.bolt.bolt_bearing_capacity = round(float(self.bolt.bolt_bearing_capacity),2)
        self.bolt.bolt_shear_capacity = round(float(self.bolt.bolt_shear_capacity),2)
        self.bolt.bolt_capacity = round(float(self.bolt.bolt_capacity),2)
        self.number_r_c_bolts(self, design_dictionary,0,0)

    def number_r_c_bolts(self,design_dictionary,count=0,hit=0):
        # Add maximum iteration limit
        MAX_ITERATIONS = 100
        iteration_count = 0

        bolt_cap = self.bolt.bolt_capacity
        if self.bolt.bolt_type == TYP_BEARING:
            self.slip_res = 'N/A'
        else:
            self.slip_res = self.bolt.bolt_capacity
            self.bolt.bolt_bearing_capacity = 'N/A'
            self.bolt.bolt_shear_capacity = 'N/A'

        if hit == 0:
            self.number_bolts = float(self.tensile_force) /( bolt_cap / 1000)
        else:
            self.number_bolts += 1

        self.number_bolts = math.ceil(self.number_bolts)
        if self.number_bolts < 2:
            self.number_bolts = 2

        def check_no_cols(numbolts):
            if (2 * self.bolt.min_end_dist_round) + ((numbolts - 1 )*self.bolt.min_pitch_round) >= float(self.width):
                return True
            else:
                return False

        self.cols = 1
        self.rows = self.number_bolts
        temp_rows = self.rows

        # Add safety check for minimum width
        min_required_width = 2 * self.bolt.min_end_dist_round
        if float(self.width) < min_required_width:
            self.design_status = False
            logger.error(f": Width ({self.width} mm) is too small. Minimum required width is {min_required_width} mm")
            logger.info(" :=========End Of design===========")
            return

        while iteration_count < MAX_ITERATIONS:
            iteration_count += 1
            if check_no_cols(temp_rows):
                temp_rows = math.ceil(self.rows/(self.cols + 1))
                self.cols += 1
            else:
                break

        if iteration_count >= MAX_ITERATIONS:
            self.design_status = False
            logger.error(": Could not find valid bolt arrangement within maximum iterations")
            logger.info(" :=========End Of design===========")
            return

        self.rows = math.ceil(self.rows/self.cols)

        if self.cols>1:
            self.len_conn = (self.cols - 1)*self.bolt.min_pitch_round + 2*self.bolt.min_end_dist_round
        else:
            self.len_conn = self.bolt.min_pitch_round + 2*self.bolt.min_end_dist_round

        if self.number_bolts >= 2 and count == 0:
            self.design_status = True
            self.check_capacity_reduction_1(self, design_dictionary)
        elif self.number_bolts>=2 and count == 1:
            self.design_status = True
            self.final_formatting(self,design_dictionary)
        else:
            self.design_status = False
            logger.error(": Number of min bolts not satisfied. \n ")
            logger.info(" :=========End Of design==========")

    def check_capacity_reduction_1(self,design_dictionary):
        """Long joint reduction as per Cl. 10.3.3.1 of IS 800:2007"""
        if self.number_bolts > 2:
            lj = (self.rows - 1)*self.bolt.min_pitch_round
            if lj > 15 * self.bolt.bolt_diameter_provided:
                # βlj calculation as per Eq. 3.7
                self.bij = 1.075 - (lj / (200 * self.bolt.bolt_diameter_provided))
                self.bij = max(0.75, min(1.0, self.bij))

        if self.bij >= 0.75 and self.bij <= 1.0:
            self.cap_red = True
            self.bolt.bolt_shear_capacity = self.bolt.bolt_shear_capacity * self.bij
            if self.bolt.bolt_type == TYP_BEARING:
                self.bolt.bolt_capacity = min(self.bolt.bolt_shear_capacity, self.bolt.bolt_bearing_capacity)
            else:
                self.slip_res = self.bolt.bolt_shear_capacity
                self.bolt.bolt_capacity = self.slip_res

        self.design_status = True
        self.check_capacity_reduction_2(self,design_dictionary)

    def check_capacity_reduction_2(self,design_dictionary):
        """Large grip reduction as per Cl. 10.3.3.2 of IS 800:2007"""
        self.cap_red = False

        lg = self.plate1thk + self.plate2thk
        if lg > 5 * self.bolt.bolt_diameter_provided:
            # βlg calculation as per Eq. 3.8
            self.blg = 8 / (3 + (lg/self.bolt.bolt_diameter_provided))
            self.blg = max(0.0, min(1.0, self.blg))

        if self.blg < self.bij and self.blg != 0:
            self.cap_red = True
            self.bolt.bolt_shear_capacity = self.bolt.bolt_shear_capacity * self.blg
            if self.bolt.bolt_type == TYP_BEARING:
                self.bolt.bolt_capacity = min(self.bolt.bolt_shear_capacity, self.bolt.bolt_bearing_capacity)
            else:
                self.slip_res = self.bolt.bolt_shear_capacity
                self.bolt.bolt_capacity = self.slip_res

            # Continue design with reduced capacity - recursion limit handled in number_r_c_bolts
            self.number_r_c_bolts(self,design_dictionary,1,0)
        else:
            self.design_status = True
            self.final_formatting(self,design_dictionary)

    def final_formatting(self,design_dictionary):
        """Final checks and formatting as per IS 800:2007"""
        # Handle single row case
        if self.rows <= 1:
            self.final_gauge = 0  # No gauge distance needed for single row
            self.final_pitch = self.bolt.min_pitch_round
            self.final_end_dist = self.bolt.min_end_dist_round
            self.final_edge_dist = self.bolt.min_edge_dist_round
        else:
            # Calculate gauge distance as per Cl. 10.2.2
            gauge_dist = (float(self.width) - 2*self.bolt.min_end_dist_round)/(self.rows - 1)

            # Check maximum pitch and gauge as per Cl. 10.2.3.1
            if gauge_dist > self.max_gauge_round:
                self.final_gauge = self.max_gauge_round
                self.final_pitch = self.bolt.min_pitch_round

                enddist = (float(self.width) - ((self.rows - 1)*self.final_gauge))/2
                if enddist > self.bolt.max_end_dist_round:
                    self.design_status = False
                    self.number_r_c_bolts(self,design_dictionary,0,1)
                else:
                    self.final_end_dist = enddist
                    self.final_edge_dist = enddist
                    self.design_status = True
            else:
                self.final_gauge = gauge_dist
                self.final_pitch = self.bolt.min_pitch_round
                enddist = (float(self.width) - ((self.rows - 1)*self.final_gauge))/2
                if enddist > self.bolt.max_end_dist_round:
                    self.design_status = False
                    self.number_r_c_bolts(self,design_dictionary,0,1)
                else:
                    self.final_end_dist = enddist
                    self.final_edge_dist = enddist
                    self.design_status = True

        if self.design_status:
            # Convert capacities to kN
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

            # Calculate utilization ratio
            bolt_capacity_kN = self.bolt.bolt_capacity
            bolt_capacity_total = bolt_capacity_kN * self.number_bolts if bolt_capacity_kN else 0.0
            if bolt_capacity_total <= 0:
                logger.error(": Bolt capacity is zero. Increase bolt size/grade or adjust layout.")
                self.design_status = False
                self.design_error = "Bolt capacity is zero."
                return
            bolt_util = self.axial_force_kN / bolt_capacity_total

            if not self.check_base_metal_strength():
                return

            if not self.base_metal_capacity_kN or self.base_metal_capacity_kN <= 0:
                logger.error(": Base metal capacity is zero or undefined. Check plate selection.")
                self.design_status = False
                self.design_error = "Base metal capacity is zero or undefined."
                return

            base_util = self.axial_force_kN / self.base_metal_capacity_kN

            def _format_util(value, decimals=3):
                if math.isinf(value) or math.isnan(value):
                    return 'Inf'
                return round(value, decimals)

            overall_util = max(bolt_util, base_util)
            self.utilization_breakdown = {
                'bolt': _format_util(bolt_util),
                'base_metal': _format_util(base_util)
            }

            if math.isinf(overall_util) or math.isnan(overall_util):
                self.utilization_ratio = 'Inf'
            else:
                self.utilization_ratio = round(overall_util, 2)

            # Check if utilization ratio is less than 1 for valid design
            if overall_util >= 1:
                self.design_status = False
                logger.error(": Utilization ratio is greater than or equal to 1. Design is not safe.")
                logger.info(" :=========End Of design===========")
                return

            # Round final values
            self.final_gauge = round(self.final_gauge,0)
            self.final_pitch = round(self.final_pitch,0)
            print("FINAL FINAL",self.bolt)
            print("Final Edge/End/Gauge/Pitch",self.final_edge_dist,self.final_end_dist,self.final_gauge,self.final_pitch)
            print("Max and min end edge dist ",self.bolt.max_end_dist_round, self.bolt.min_end_dist_round, self.bolt.max_edge_dist_round, self.bolt.min_edge_dist_round)
            print("Max min gauge pitch dist",self.max_gauge_round,self.bolt.min_gauge_round, self.max_pitch_round, self.bolt.min_pitch_round)


    def check_base_metal_strength(self):
        global logger
        try:
            logger
        except NameError:
            logger = logging.getLogger('Osdag')

        logger.info(": ============== Base Metal Strength Check ==============")

        plate_thk_min = min(float(self.plate1thk), float(self.plate2thk))
        fy = min(self.plate1.fy, self.plate2.fy)
        fu = min(self.plate1.fu, self.plate2.fu)

        self.gamma_m0 = 1.10
        self.gamma_m1 = 1.25

        self.A_g = plate_thk_min * float(self.width)

        if self.design_for == 'Compression':
            self.T_db = self.A_g * fy / self.gamma_m0
            logger.info(f": Design strength of plate in compression = {self.T_db / 1000:.2f} kN [Cl.7.1.2]")
        else:
            n_holes = max(self.rows, 1)
            hole_dia = self.bolt.dia_hole if hasattr(self.bolt, 'dia_hole') else 0.0
            net_width = float(self.width) - n_holes * hole_dia

            if net_width <= 0:
                logger.error(": Net width becomes zero/negative after deducting bolt holes. Increase plate width or reduce rows.")
                self.design_status = False
                self.design_error = "Net width insufficient for bolt holes."
                return False

            self.A_n = plate_thk_min * net_width
            shear_lag_factor = 0.7  # IS 800:2007 Cl.6.3.3 for butt joints

            T_dg = self.A_g * fy / self.gamma_m0
            T_dn = 0.9 * self.A_n * fu * shear_lag_factor / self.gamma_m1
            self.T_dg = T_dg
            self.T_dn = T_dn
            self.T_db = min(T_dg, T_dn)

            # Calculate block shear strength
            A_vg = plate_thk_min * ((self.rows - 1) * self.final_gauge + self.final_edge_dist)
            A_vn = plate_thk_min * ((self.rows - 1) * self.final_gauge + self.final_edge_dist - (self.rows - 0.5) * hole_dia)
            A_tg = plate_thk_min * self.final_end_dist
            A_tn = plate_thk_min * (self.final_end_dist - 0.5 * hole_dia)

            T_db_block = IS800_2007.cl_6_4_1_block_shear_strength(A_vg, A_vn, A_tg, A_tn, fu, fy)
            self.T_db = min(self.T_db, T_db_block)
            logger.info(f": Design strength of plate in tension = {self.T_db / 1000:.2f} kN [Cl.6.2.2, 6.2.3, 6.3.3]")

        if self.T_db <= 0:
            logger.error(": Plate design strength is non-positive. Check input dimensions/material.")
            self.design_status = False
            self.design_error = "Plate design strength is non-positive."
            return False

        self.base_metal_capacity_kN = self.T_db / 1000.0
        return True


    def save_design(self, popup_summary):
        """
        Generate design report for Bolted Butt Joint Connection as per IS 800:2007
        Follows tension bolted module reporting style with explicit, step-by-step calculations
        """

        try:
            # Build report_input dictionary - Input Parameters Section (like tension bolted)
            self.report_input = {
                KEY_MODULE: getattr(self, 'module', 'Butt Joint Bolted'),
                KEY_MAIN_MODULE: getattr(self, 'mainmodule', 'Butt Joint Bolted Connection'),

                # Applied Load - Input
                KEY_DISP_TENSILE_FORCE: float(getattr(self, 'tensile_force', 0)),

                # Connection Details - Input
                "Connection Details": "TITLE",
                KEY_DISP_MATERIAL: getattr(self, 'main_material', 'N/A'),
                KEY_DISP_PLATE1_THICKNESS: float(getattr(self, 'plate1thk', 0)),
                KEY_DISP_PLATE2_THICKNESS: float(getattr(self, 'plate2thk', 0)),
                KEY_DISP_PLATE_WIDTH: float(getattr(self, 'width', 0)),
                KEY_DISP_COVER_PLATE: getattr(self, 'cover_plate', 'Both Sides'),

                # Material Properties
                "Material Properties": "TITLE",
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: round(getattr(self.plate1, 'fu', 0), 1) if hasattr(self, 'plate1') else 0,
                KEY_DISP_YIELD_STRENGTH_REPORT: round(getattr(self.plate1, 'fy', 0), 1) if hasattr(self, 'plate1') else 0,

                # Bolt Details - Input and Design Preference (show full lists like tension bolted)
                "Bolt Details - Input and Design Preference": "TITLE",
                KEY_DISP_D: str([int(d) for d in getattr(self.bolt, 'bolt_diameter', [])]) if hasattr(self, 'bolt') else "[]",
                KEY_DISP_GRD: str([float(d) for d in getattr(self.bolt, 'bolt_grade', [])]) if hasattr(self, 'bolt') else "[]",
                KEY_DISP_TYP: getattr(self.bolt, 'bolt_type', 'N/A') if hasattr(self, 'bolt') else 'N/A',
                KEY_DISP_DP_BOLT_HOLE_TYPE: getattr(self.bolt, 'bolt_hole_type', 'Standard') if hasattr(self, 'bolt') else 'Standard',

                # Detailing - Design Preference
                "Detailing - Design Preference": "TITLE",
                KEY_DISP_DP_DETAILING_EDGE_TYPE: getattr(self.bolt, 'edge_type', 'Sheared or hand flame cut') if hasattr(self, 'bolt') else 'Sheared or hand flame cut',
                KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM: getattr(self.bolt, 'corrosive_influences', 'Corrosive') if hasattr(self, 'bolt') else 'Corrosive',
            }

            # Add bolt-type specific inputs (only if friction grip)
            if hasattr(self, 'bolt') and getattr(self.bolt, 'bolt_type', '') == TYP_FRICTION_GRIP:
                self.report_input[KEY_DISP_DP_BOLT_SLIP_FACTOR_REPORT] = getattr(self.bolt, 'mu_f', 0.3) if hasattr(self.bolt, 'mu_f') else 0.3

            # Build report_check list - Design Verification (like tension bolted structure)
            self.report_check = []

            if getattr(self, 'design_status', False):
                # Extract values for calculations
                bolt_diameter_provided = float(getattr(self.bolt, 'bolt_diameter_provided', 0)) if hasattr(self, 'bolt') else 0.0
                bolt_grade = getattr(self.bolt, 'bolt_grade_provided', 0) if hasattr(self, 'bolt') else 0
                bolt_fu = getattr(self.bolt, 'bolt_fu', 0) if hasattr(self, 'bolt') else 0
                bolt_fy = getattr(self.bolt, 'bolt_fy', 0) if hasattr(self, 'bolt') else 0
                bolt_net_area = getattr(self.bolt, 'bolt_net_area', 0) if hasattr(self, 'bolt') else 0
                connecting_plates = [getattr(self, 'plate1thk', 0), getattr(self, 'plate2thk', 0)]

                # Spacing values
                final_pitch = float(getattr(self, 'final_pitch', 0))
                final_gauge = float(getattr(self, 'final_gauge', 0))
                final_edge_dist = float(getattr(self, 'final_edge_dist', 0))
                final_end_dist = float(getattr(self, 'final_end_dist', 0))

                # Bolt layout
                rows = getattr(self, 'rows', 1)
                cols = getattr(self, 'cols', 1)
                number_bolts = int(getattr(self, 'number_bolts', 0))
                tensile_force = float(getattr(self, 'tensile_force', 0))

                # SECTION 1: Spacing Check (like tension bolted)
                t7 = ('SubSection', 'Spacing Check as per Cl. 10.2 of IS 800:2007', '|p{2.5cm}|p{7.5cm}|p{3cm}|p{2.5cm}|')
                self.report_check.append(t7)

                t8 = (DISP_MIN_PITCH, cl_10_2_2_min_spacing(bolt_diameter_provided),
                      display_prov(final_pitch, "p", "mm"),
                      get_pass_fail(2.5 * bolt_diameter_provided, final_pitch, relation='leq'))
                self.report_check.append(t8)

                t9 = (DISP_MAX_PITCH, cl_10_2_3_1_max_spacing(connecting_plates),
                      display_prov(final_pitch, "p", "mm"),
                      get_pass_fail(final_pitch, 32 * min(connecting_plates), relation='leq'))
                self.report_check.append(t9)

                if final_gauge > 0:  # Only show for multi-row arrangements
                    t10 = (DISP_MIN_GAUGE, cl_10_2_2_min_spacing(bolt_diameter_provided),
                           display_prov(final_gauge, "g", "mm"),
                           get_pass_fail(2.5 * bolt_diameter_provided, final_gauge, relation="leq"))
                    self.report_check.append(t10)

                    t11 = (DISP_MAX_GAUGE, cl_10_2_3_1_max_spacing(connecting_plates),
                           display_prov(final_gauge, "g", "mm"),
                           get_pass_fail(final_gauge, 32 * min(connecting_plates), relation="leq"))
                    self.report_check.append(t11)

                edge_type_str = getattr(self.bolt, 'edge_type', 'Sheared or hand flame cut') if hasattr(self, 'bolt') else 'Sheared or hand flame cut'

                t12 = (DISP_MIN_END, cl_10_2_4_2_min_edge_end_dist(bolt_diameter_provided, edge_type_str),
                       display_prov(final_end_dist, "e_{end}", "mm"),
                       get_pass_fail(1.2 * bolt_diameter_provided, final_end_dist, relation='leq'))
                self.report_check.append(t12)

                t13 = (DISP_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(bolt_diameter_provided, edge_type_str),
                       display_prov(final_edge_dist, "e", "mm"),
                       get_pass_fail(1.2 * bolt_diameter_provided, final_edge_dist, relation='leq'))
                self.report_check.append(t13)

                # SECTION 3: Bolt Design (like tension bolted)
                t14 = ('SubSection', 'Bolt Design as per Cl. 10.3 of IS 800:2007', '|p{2.5cm}|p{5.5cm}|p{6.5cm}|p{1cm}|')
                self.report_check.append(t14)

                # Bolt capacity calculations
                bolt_type = getattr(self.bolt, 'bolt_type', '') if hasattr(self, 'bolt') else ''
                planes = getattr(self, 'planes', 1)
                bolt_shear_capacity = getattr(self.bolt, 'bolt_shear_capacity', 0) if hasattr(self, 'bolt') else 0
                bolt_bearing_capacity = getattr(self.bolt, 'bolt_bearing_capacity', 0) if hasattr(self, 'bolt') else 0
                bolt_capacity = getattr(self.bolt, 'bolt_capacity', 0) if hasattr(self, 'bolt') else 0

                # Convert to kN for display
                bolt_shear_capacity_kn = round(bolt_shear_capacity / 1000, 2) if bolt_shear_capacity > 1000 else bolt_shear_capacity
                bolt_bearing_capacity_kn = round(bolt_bearing_capacity / 1000, 2) if bolt_bearing_capacity > 1000 else bolt_bearing_capacity
                bolt_capacity_kn = round(bolt_capacity / 1000, 2) if bolt_capacity > 1000 else bolt_capacity

                if bolt_type == TYP_BEARING:
                    t15 = (KEY_OUT_DISP_BOLT_SHEAR, '',
                           cl_10_3_3_bolt_shear_capacity(bolt_fu, planes, bolt_net_area, 1.25, bolt_shear_capacity_kn), '')
                    self.report_check.append(t15)

                    kb = getattr(self.bolt, 'kb', 0) if hasattr(self, 'bolt') else 0
                    bolt_conn_plates_t_fu_fy = getattr(self, 'bolt_conn_plates_t_fu_fy', []) if hasattr(self, 'bolt_conn_plates_t_fu_fy') else []

                    t16 = (KEY_OUT_DISP_BOLT_BEARING, '',
                           cl_10_3_4_bolt_bearing_capacity(kb, bolt_diameter_provided, bolt_conn_plates_t_fu_fy, 1.25, bolt_bearing_capacity_kn), '')
                    self.report_check.append(t16)

                    t17 = (KEY_OUT_DISP_BOLT_CAPACITY, '',
                           cl_10_3_2_bolt_capacity(bolt_shear_capacity_kn, bolt_bearing_capacity_kn, bolt_capacity_kn), '')
                    self.report_check.append(t17)
                else:
                    # HSFG bolt
                    mu_f = float(getattr(self.bolt, 'mu_f', 0.3)) if hasattr(self, 'bolt') else 0.3
                    slip_res = getattr(self, 'slip_res', 0)
                    slip_res_kn = round(slip_res / 1000, 2) if slip_res > 1000 else slip_res
                    bolt_capacity_kn = slip_res_kn

                    t15 = (KEY_OUT_DISP_BOLT_SLIP_DR, '',
                           cl_10_4_3_HSFG_bolt_capacity(mu_f, planes, 1.0, bolt_fu, bolt_net_area, 1.25, slip_res_kn), '')
                    self.report_check.append(t15)

                # Number of bolts required
                t18 = (DISP_NUM_OF_BOLTS, '', display_prov(number_bolts, "n"), '')
                self.report_check.append(t18)

                # Note: class variables are self.cols (transverse) and self.rows (longitudinal)
                t19 = (DISP_NUM_OF_COLUMNS, '', display_prov(self.cols, "n_{c}"), '')
                self.report_check.append(t19)

                t20 = (DISP_NUM_OF_ROWS, '', display_prov(self.rows, "n_{r}"), '')
                self.report_check.append(t20)

                # Long joint and large grip checks (only if conditions are met)
                # Long joint check - must match exact calculation logic from design method
                if self.number_bolts > 2 and self.rows > 1:
                    # Use exact same calculation as in check_capacity_reduction_1
                    # Note: self.rows is longitudinal direction, cols is transverse
                    lj = (self.rows - 1) * self.bolt.min_pitch_round
                    if lj > 15 * bolt_diameter_provided:
                        bij = self.bij  # Use class variable directly
                        # Only show if reduction was actually calculated and applied
                        # bij will be 0 if no reduction, or 0.75-1.0 if reduction applied
                        if bij >= 0.75 and bij <= 1.0:
                            t21 = (KEY_OUT_LONG_JOINT, '',
                                   cl_10_3_3_1_long_joint_reduction_factor(lj, bolt_diameter_provided, bij),
                                   get_pass_fail(bij, 0.75, relation='geq'))
                            self.report_check.append(t21)

                # Large grip check - must match exact calculation logic from design method
                lg = self.plate1thk + self.plate2thk
                if lg > 5 * bolt_diameter_provided:
                    blg = self.blg  # Use class variable directly
                    # Only show if reduction was actually calculated and applied
                    # blg will be 0 if no reduction, or calculated value if reduction applied
                    if blg > 0 and blg <= 1.0:
                        # Large grip reduction should pass if it's calculated and applied
                        t22 = (KEY_OUT_LARGE_GRIP, '',
                               cl_10_3_3_2_large_grip_reduction_factor(lg, bolt_diameter_provided, blg),
                               get_pass_fail(blg, 0.0, relation='gt'))  # Pass if blg > 0
                        self.report_check.append(t22)

                # SECTION 4: Connection Verification (like tension bolted)
                t23 = ('SubSection', 'Connection Verification', '|p{2.5cm}|p{5.5cm}|p{6.5cm}|p{1cm}|')
                self.report_check.append(t23)

                # Use utilization ratio from class variable
                utilization_ratio = getattr(self, 'utilization_ratio', 0)

                # Show utilization ratio without formula
                t24 = (KEY_DISP_UTILIZATION_RATIO, 'Utilization ratio should be ≤ 1.0',
                       display_prov(utilization_ratio, "U.R."),
                       get_pass_fail(utilization_ratio, 1.0, relation='leq'))
                self.report_check.append(t24)

            else:
                # Design not completed
                t1 = ('SubSection', 'Design Status', '|p{2.5cm}|p{7.5cm}|p{3cm}|p{2.5cm}|')
                self.report_check.append(t1)

                t2 = ('Design Status',
                      'Design not completed successfully. Check input parameters and design constraints.',
                      'Review inputs and try again',
                      'FAIL')
                self.report_check.append(t2)

            # Generate LaTeX report
            Disp_2d_image = []
            Disp_3D_image = "/ResourceFiles/images/3d.png"

            import sys
            import os
            rel_path = str(sys.path[0])
            rel_path = os.path.abspath(".")
            rel_path = rel_path.replace("\\", "/")
            fname_no_ext = popup_summary['filename']

            CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                                   rel_path, Disp_2d_image, Disp_3D_image, module=self.module)

        except Exception as e:
            # Create minimal error report if save_design fails
            logger.error(f"Error in save_design: {str(e)}")
            self.report_input = {
                KEY_MODULE: "Butt Joint Bolted",
                KEY_MAIN_MODULE: "Butt Joint Bolted Connection",
                "Error Report": "TITLE",
                "Error Details": f"Report generation failed: {str(e)}"
            }
            self.report_check = [
                ('SubSection', 'Error Report', '|p{2.5cm}|p{7.5cm}|p{3cm}|p{2.5cm}|'),
                ('Error', f'Report generation failed: {str(e)}', 'Check design status and inputs', 'FAIL')
            ]

            # Generate minimal error report
            try:
                Disp_2d_image = []
                Disp_3D_image = "/ResourceFiles/images/3d.png"

                import sys
                import os
                rel_path = str(sys.path[0])
                rel_path = os.path.abspath(".")
                rel_path = rel_path.replace("\\", "/")
                fname_no_ext = popup_summary.get('filename', 'error_report')

                CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                                       rel_path, Disp_2d_image, Disp_3D_image, module=self.module)
            except Exception as e2:
                logger.error(f"Critical error in save_design: {str(e2)}")
                raise

