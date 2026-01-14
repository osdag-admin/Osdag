import logging
import math
import numpy as np
from PySide6.QtWidgets import QDialog

from ....Common import *
from ....utils.common.material import *
from ....utils.common.load import Load
from ....utils.common.component import ISection, Material, Plate
from ...member import Member
from ....Report_functions import *
from ....utils.common.common_calculation import *
from ...tension_member import *
from ....utils.common.Section_Properties_Calculator import BBAngle_Properties
from ....utils.common import is800_2007
from ....utils.common.Unsymmetrical_Section_Properties import Unsymmetrical_I_Section_Properties

# New imports
from ....Common import *
from ..gui.dialogs import RangeInputDialog, PopupDialog
from ..gui.widgets import My_ListWidget, My_ListWidgetItem
from .section import Section, calc_yj, shear_stress_unsym_I, classify_section
from .pso_optimizer import GlobalBestPSO
from ..optimization.intelligent_pso import IntelligentPSO
from .utils import ceil_to_nearest, get_K_from_warping_restraint

# ==============================================================================
# OPTIMIZATION & DEBUG CONFIGURATION
# ==============================================================================
USE_INTELLIGENT_PSO = True  # Set False to use legacy PSO
DEBUG_MODE = True          # Set True to enable detail printing
# ==============================================================================
from ..checks.shear import *
from ..checks.web_buckling import *
from ..checks.web_crippling import *
from ..checks.welds import *
from ..checks.moment import *
from ..checks.moment import *
from ..checks.deflection import evaluate_deflection_kNm_mm
from ..checks import SKIP_DEFLECTION
from ..checks.web_thickness import min_web_thickness_thick_web
from ..report.latex_report import save_design
from ....custom_logger import CustomLogger

scale = 1

class PlateGirderWelded(Member):
    int_thicklist = []
    long_thicklist = []
    # Class-level warning flags for optimization methods
    _flange_warning_logged = False
    _dimension_warning_logged = False
    _web_crippling_warning_logged = False

    def __init__(self):
        super(PlateGirderWelded, self).__init__()
        self.design_status = False
        self.calculated_deflection = 'N/A'
        self.deflection_limit = 'N/A'
        self.deflection_skipped = False
        self.hover_dict = {}  # Required for CAD display tooltips
        self.mainmodule = 'PLATE GIRDER'  # Required for CommonDesignLogic routing
        
        # Configuration control
        self.debug = DEBUG_MODE
        self.use_intelligent_pso = USE_INTELLIGENT_PSO
        
        # Instance-level warning flags
        self.flange_warning_logged = False  # Flag to log b/tf warnings only once per session
        self.dimension_warning_logged = False  # Flag to log dimension warnings only once per session
        self.web_crippling_warning_logged = False  # Flag to log web crippling warnings only once per session
        
        # Initialize output-related attributes (needed for output_values before design runs)
        self.result_designation = 'N/A'
        self.section_classification_val = 'N/A'
        self.result_UR = 0
        self.effectivearea = 'N/A'
        self.web_thickness = 0
        self.top_flange_thickness = 0
        self.bottom_flange_thickness = 0
        self.betab = 'N/A'
        self.warping_cnst = 'N/A'
        self.torsion_cnst = 'N/A'
        self.critical_moment = 'N/A'
        self.design_moment = 'N/A'
        self.V_d = 0
        self.V_cr = 0
        self.F_q = 0
        self.x = 'N/A'  # Shear buckling method
        self.end_panel_stiffener_thickness = 'N/A'
        self.intstiffener_thk = 'N/A'
        self.intstiffener_spacing = 'N/A'
        self.longstiffener_thk = 'N/A'
        self.longstiffener_no = 'N/A'
        self.x1 = 0
        self.x2 = 0
        
        # Defining default Bounds
        self.bounds_map = {
            'tf': (6, 100),
            'tf_top': (6, 100),
            'tf_bot': (6, 100), 
            'tw': (6, 40),
            'bf': (100, 1000),
            'bf_top': (100, 1000, 10), # width of top flange
            'bf_bot': (100, 1000, 10), # width of bottom flange
            'D': (200, 2000, 25), # total depth
            'c': (100, 6000), # IS 800: 0.5d (min 100) to 3d (max 6000)
            't_stiff': (6, 50) # IS 800: d/50 (max 40) + margin
        }        
        # to save bound input widgets
        self.bound_widgets = {}

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        tabs = []

        t1 = (KEY_DISP_GIRDERSEC, TYPE_TAB_1, self.tab_girder_sec)
        tabs.append(t1)

        t5 = ("Optimisation", TYPE_TAB_2, self.optimization_tab_welded_plate_girder_design)
        tabs.append(t5)

        t1 = ("Stiffeners", TYPE_TAB_2, self.Stiffener_design)
        tabs.append(t1)

        t1 = ("Additional Girder Data", TYPE_TAB_2, self.girder_geometry)
        tabs.append(t1)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        t6 = ("Deflection"  , TYPE_TAB_2, self.deflection_values)
        tabs.append(t6)

        return tabs
    
    def tab_value_changed(self):
        change_tab = []

        # Include Label_7 (web thickness) to get correct thickness-dependent Fy values
        t1 = (KEY_DISP_GIRDERSEC, [KEY_SEC_MATERIAL, 'Label_7'], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX, self.get_fu_fy_I_section_plate_girder)
        change_tab.append(t1)

        t4 = (KEY_DISP_GIRDERSEC, ['Label_6', 'Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11',KEY_SEC_FY],
              ['Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22','Label_23'], TYPE_TEXTBOX, self.Unsymm_I_Section_properties)
        change_tab.append(t4)

        t9 = ("Deflection", [KEY_STR_TYPE], [KEY_MEMBER_OPTIONS], TYPE_COMBOBOX, self.member_options_change)
        change_tab.append(t9)
        t9 = ("Deflection", [KEY_MEMBER_OPTIONS], [KEY_SUPPORTING_OPTIONS], TYPE_COMBOBOX, self.supp_options_change)
        change_tab.append(t9)
        t9 = ("Deflection", [KEY_STR_TYPE,KEY_DESIGN_LOAD,KEY_MEMBER_OPTIONS,KEY_SUPPORTING_OPTIONS], [KEY_MAX_DEFL], TYPE_TEXTBOX, self.max_defl_change)
        change_tab.append(t9)
        t10 = ("Stiffeners", [KEY_IntermediateStiffener_thickness], [KEY_IntermediateStiffener_thickness_val], TYPE_COMBOBOX, self.Int_stiffener_thickness_customized)
        change_tab.append(t10)
        t11 = ("Stiffeners", [KEY_LongitudnalStiffener_thickness], [KEY_LongitudnalStiffener_thickness_val], TYPE_COMBOBOX, self.Long_stiffener_thickness_customized)
        change_tab.append(t11)

        return change_tab

    def edit_tabs(self):
        return []

    def input_dictionary_design_pref(self):
        design_input = []

        t1 = (KEY_DISP_GIRDERSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t1)
        
        t1 = (KEY_DISP_GIRDERSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY])
        design_input.append(t1)

        t2 = ("Optimisation", TYPE_TEXTBOX, [KEY_EFFECTIVE_AREA_PARA, KEY_LENGTH_OVERWRITE])
        design_input.append(t2)

        t2 = ("Optimisation", TYPE_COMBOBOX, [KEY_ALLOW_CLASS, KEY_LOAD])
        design_input.append(t2)

        t2 = ("Stiffeners", TYPE_COMBOBOX, [KEY_IntermediateStiffener,KEY_LongitudnalStiffener,KEY_IntermediateStiffener_thickness,KEY_LongitudnalStiffener_thickness])
        design_input.append(t2)

        t2 = ("Stiffeners", TYPE_TEXTBOX, [KEY_IntermediateStiffener_spacing])
        design_input.append(t2)

        t2 = ("Stiffeners", TYPE_COMBOBOX, [KEY_ShearBucklingOption,KEY_IntermediateStiffener_thickness_val,KEY_LongitudnalStiffener_thickness_val])
        design_input.append(t2)

        t2 = ("Additional Girder Data", TYPE_COMBOBOX, [KEY_IS_IT_SYMMETRIC])
        design_input.append(t2)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Deflection",TYPE_COMBOBOX, [KEY_STR_TYPE,KEY_DESIGN_LOAD,KEY_MEMBER_OPTIONS,KEY_SUPPORTING_OPTIONS]) 
        design_input.append(t7)
        t7 = ("Deflection",TYPE_TEXTBOX, [KEY_MAX_DEFL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        """
        This function is used to choose values of design preferences to be saved to
        design dictionary if design preference is never opened by user. It sets all design 
        preference values to default.
        
        If any design preference value needs to be set to input dock value, tuple shall be:
        (Key of input dock, [List of Keys from design preference], 'Input Dock')
        
        If the values needs to be set to default:
        (None, [List of Design Preference Keys], '')
        """
        design_input = []

        # Synchronize design preference material with input dock material
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_ALLOW_CLASS, KEY_EFFECTIVE_AREA_PARA, KEY_LENGTH_OVERWRITE, KEY_LOAD, KEY_DP_DESIGN_METHOD, KEY_STR_TYPE, KEY_DESIGN_LOAD, KEY_MEMBER_OPTIONS, KEY_MAX_DEFL,
                     KEY_SUPPORTING_OPTIONS, KEY_ShearBucklingOption, KEY_IntermediateStiffener_spacing, KEY_IntermediateStiffener, KEY_LongitudnalStiffener, KEY_IntermediateStiffener_thickness_val, KEY_LongitudnalStiffener_thickness_val,
                     KEY_IntermediateStiffener_thickness, KEY_LongitudnalStiffener_thickness, KEY_IS_IT_SYMMETRIC], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        add_buttons = []
        return add_buttons

    def get_values_for_design_pref(self, key, design_dictionary):
        val = {
            KEY_ALLOW_CLASS: 'Yes',
            KEY_EFFECTIVE_AREA_PARA: '1.0',
            KEY_LENGTH_OVERWRITE: 'NA',
            KEY_LOAD: 'Normal',
            KEY_DP_DESIGN_METHOD: "Limit State Design",
            KEY_ShearBucklingOption: KEY_DISP_SB_Option[0],
            KEY_IS_IT_SYMMETRIC: 'Symmetrical',
            KEY_IntermediateStiffener_spacing:'NA',
            KEY_IntermediateStiffener: 'No',
            KEY_IntermediateStiffener_thickness:'All',
            KEY_LongitudnalStiffener: 'No',
            KEY_LongitudnalStiffener_thickness:'All',
            KEY_STR_TYPE:'Highway Bridge',
            KEY_DESIGN_LOAD:'Live Load',
            KEY_MEMBER_OPTIONS :'Simple Span',
            KEY_SUPPORTING_OPTIONS: 'NA',
            KEY_MAX_DEFL : 600,
            KEY_IntermediateStiffener_thickness_val : VALUES_STIFFENER_THICKNESS,
            KEY_LongitudnalStiffener_thickness_val : VALUES_STIFFENER_THICKNESS
        }[key]
        return val

    def member_options_change(self, arg):
        if arg[0] == KEY_DISP_STR_TYP3:
            return {KEY_MEMBER_OPTIONS : VALUES_MEMBER_OPTIONS[1]}
        elif arg[0] == KEY_DISP_STR_TYP4:
            return {KEY_MEMBER_OPTIONS :VALUES_MEMBER_OPTIONS[2]}
        else:
            return {KEY_MEMBER_OPTIONS : VALUES_MEMBER_OPTIONS[0]}
        
    def supp_options_change(self, arg):
        if arg[0] in ['Purlin and Girts', 'Simple span', 'Cantilever span']:
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_PSC}
        elif arg[0]  == 'Rafter Supporting':
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_RS}
        elif arg[0]  == 'Gantry':
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_GNT}
        elif arg[0] in  ['Floor and roof', 'Cantilever']:
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_FRC}
        else:
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_DEF}

    def max_defl_change(self, arg):
        if arg[0] in ['Highway Bridge','Railway Bridge']:
            if arg[2] == 'Simple Span':
                if arg[1] == 'Live load':
                    return {KEY_MAX_DEFL :VALUES_MAX_DEFL[0]}
                elif arg[1] == 'Dead load':
                    return  {KEY_MAX_DEFL : VALUES_MAX_DEFL[1]}
                else:
                    return {KEY_MAX_DEFL : 'NA'}
            else:
                if arg[1] == 'Live load':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[2]}
                elif arg[1] == 'Dead load':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[1]}
                else:
                    return {KEY_MAX_DEFL : 'NA'}
        elif arg[0] == 'Other Building':
            if arg[1] == 'Live load':
                if arg[2] == 'Floor and roof':
                    if arg[3] == 'Elements not susceptible to cracking':
                        return {KEY_MAX_DEFL : VALUES_MAX_DEFL[3]}
                    else:
                        return {KEY_MAX_DEFL : VALUES_MAX_DEFL[4]}
                else:
                    if arg[3] == 'Elements not susceptible to cracking':
                        return {KEY_MAX_DEFL : VALUES_MAX_DEFL[5]}
                    else:
                        return {KEY_MAX_DEFL : VALUES_MAX_DEFL[6]}
            else:
                return {KEY_MAX_DEFL : 'NA'}
        else:
            if arg[2] == 'Purlin and Girts' and arg[1] == 'Live load':
                if arg[3] == 'Elastic cladding':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[5]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[6]}
            elif arg[2] == 'Simple span' and arg[1] == 'Live load':
                if arg[3] == 'Elastic cladding':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[7]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[3]}
            elif arg[2] == 'Cantilever span' and arg[1] == 'Live load':
                if arg[3] == 'Elastic cladding':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[8]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[5]}
            elif arg[2] == 'Rafter Supporting' and arg[1] == 'Live load':
                if arg[3] == 'Profiled Metal sheeting':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[6]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[7]}
            elif arg[2] == 'Gantry' and arg[1] == 'Live load':
                if arg[1] == 'Crane Load(Manual operation)':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[9]}
                elif arg[1] == 'Crane load(Electric operation up to 50t)':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[10]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[11]}
            else:
                return {KEY_MAX_DEFL : 'NA'}
            
    def Int_stiffener_thickness_customized(self, arg):
        selected_items = []
        if arg[0] == 'All':
            return {KEY_IntermediateStiffener_thickness_val : VALUES_STIFFENER_THICKNESS}
        else:
            popup = PopupDialog()
            popup.listWidget.addItems(VALUES_STIFFENER_THICKNESS)
            if popup.exec_() == QDialog.Accepted:
                selected_items = popup.get_selected_items()
            PlateGirderWelded.int_thicklist = selected_items
            return {KEY_IntermediateStiffener_thickness_val : selected_items}                                 
            
    def Long_stiffener_thickness_customized(self, arg):
        selected_items2 = []
        if arg[0] == 'All':
            return {KEY_LongitudnalStiffener_thickness_val : VALUES_STIFFENER_THICKNESS}
        else:
            popup = PopupDialog()
            popup.listWidget.addItems(VALUES_STIFFENER_THICKNESS)
            if popup.exec_() == QDialog.Accepted:
                selected_items2 = popup.get_selected_items()
            PlateGirderWelded.long_thicklist = selected_items2
            return {KEY_LongitudnalStiffener_thickness_val : selected_items2}

    def module_name(self):
        return KEY_DISP_PLATE_GIRDER_WELDED

    def set_osdaglogger(self, key):
        """
        Function to set Logger for FinPlate Module
        """
        # @author Arsil Zunzunia

        # Set Custom logger
        logging.setLoggerClass(CustomLogger)

        # Create unique logger name per instance
        unique_logger_name = 'Osdag_plate_girder_flexure'
        self.logger = logging.getLogger(unique_logger_name)

        if not isinstance(self.logger, CustomLogger):
            logging.getLogger(unique_logger_name).manager.loggerDict.pop(unique_logger_name, None)
            self.logger = logging.getLogger(unique_logger_name)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG)
        
        # Shared formatter for all handlers
        formatter = logging.Formatter(
            fmt='%(asctime)s - Osdag - %(levelname)s - %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # ---------- CONSOLE HANDLER ----------
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # ---------- FILE HANDLER (CLEAR & RESTART LOG) ----------
        log_dir = Path("ResourceFiles") / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file_path = log_dir / f"{unique_logger_name}.log"
        
        file_handler = logging.FileHandler(
            log_file_path,
            mode="w",          # clears previous log
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # ---------- GUI HANDLER ----------
        if key is not None:
            gui_handler = OurLog(key)
            gui_handler.setFormatter(formatter)
            self.logger.addHandler(gui_handler)

    def customized_input(self):
        c_lst = []
        return c_lst

    def input_values(self):
        self.module = KEY_DISP_PLATE_GIRDER_WELDED
        options_list = []
        t1 = (None, KEY_DISP_PG_SectionDetail, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)
        t1 = (KEY_MODULE, KEY_DISP_PLATE_GIRDER_WELDED, TYPE_MODULE, None, True, "No Validator")
        options_list.append(t1)
        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)
        t2 = (KEY_OVERALL_DEPTH_PG_TYPE, KEY_DISP_OVERALL_DEPTH_PG_TYPE, TYPE_COMBOBOX, VALUES_DEPTH_PG, True, 'No Validator')
        options_list.append(t2)
        t33 = (KEY_OVERALL_DEPTH_PG, KEY_DISP_OVERALL_DEPTH_PG, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t33)
        t4 = (KEY_WEB_THICKNESS_PG, KEY_DISP_WEB_THICKNESS_PG, TYPE_COMBOBOX, VALUES_PLATETHK, True, 'Int Validator')
        options_list.append(t4)
        t2 = (KEY_TOP_Bflange_PG, KEY_DISP_TOP_Bflange_PG, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t2)
        t4 = (KEY_TOP_FLANGE_THICKNESS_PG, KEY_DISP_TOP_FLANGE_THICKNESS_PG, TYPE_COMBOBOX, VALUES_PLATETHK, True, 'Int Validator')
        options_list.append(t4)
        t22 = (KEY_BOTTOM_Bflange_PG, KEY_DISP_BOTTOM_Bflange_PG, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t22)
        t4 = (KEY_BOTTOM_FLANGE_THICKNESS_PG, KEY_DISP_BOTTOM_FLANGE_THICKNESS_PG, TYPE_COMBOBOX, VALUES_PLATETHK, True, 'No Validator')
        options_list.append(t4)
        t2 = (KEY_LENGTH, KEY_DISP_LENGTH, TYPE_TEXTBOX ,None, True, 'No Validator')
        options_list.append(t2)
        t1 = (None, KEY_DISP_SECTION_DATA_PG, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)
        t2 = (KEY_DESIGN_TYPE_FLEXURE, KEY_BEAM_SUPP_TYPE, TYPE_COMBOBOX, VALUES_SUPP_TYPE_temp, True, "No Validator")
        options_list.append(t2)
        t5 = (KEY_SUPPORT_WIDTH, KEY_DISP_SUPPORT_WIDTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)
        t4 = (KEY_WEB_PHILOSOPHY, KEY_DISP_WEB_PHILOSOPHY, TYPE_COMBOBOX, WEB_PHILOSOPHY_list, True, 'No Validator')
        options_list.append(t4)
        t10 = (KEY_TORSIONAL_RES, DISP_TORSIONAL_RES, TYPE_COMBOBOX, Torsion_Restraint_list, True, 'No Validator')
        options_list.append(t10)
        t11 = (KEY_WARPING_RES, DISP_WARPING_RES, TYPE_COMBOBOX, Warping_Restraint_list, True, 'No Validator')
        options_list.append(t11)
        t7 = (None, KEY_LOADING, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)
        t8 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)
        t8 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)
        t8= (KEY_BENDING_MOMENT_SHAPE, KEY_DISP_BENDING_MOMENT_SHAPE, TYPE_COMBOBOX, Bending_moment_shape_list, True, 'No Validator' )
        options_list.append(t8)
        return options_list

    def fn_torsion_warping(self, arg):
        if arg[0] == Torsion_Restraint1:
            return Warping_Restraint_list
        elif arg[0] == Torsion_Restraint2:
            return [Warping_Restraint5]
        else:
            return [Warping_Restraint5]

    def axis_bending_change(self, arg):
        if arg[0] == KEY_DISP_DESIGN_TYPE_FLEXURE:
            return ['NA']
        else:
            return VALUES_BENDING_TYPE
        
    def fn_conn_image(self, arg):
        img = arg[0]
        if img == Bending_moment_shape_list[0]:
            return VALUES_IMAGE_PLATEGIRDER[0]
        elif img ==Bending_moment_shape_list[1]:
            return VALUES_IMAGE_PLATEGIRDER[1]
        elif img ==Bending_moment_shape_list[2]:
            return VALUES_IMAGE_PLATEGIRDER[2]
        elif img ==Bending_moment_shape_list[3]:
            return VALUES_IMAGE_PLATEGIRDER[3]
        else:
            return VALUES_IMAGE_PLATEGIRDER[4]
        
    def customized_dims(self, arg):
        conn = arg[0]
        if conn == "Customized":
            return True
        else:
            return False
    
    def customize_combo_dims(self, arg):
        conn = arg[0]
        if conn == "Customized":
            return VALUES_PLATETHK_CUSTOMIZED
        else:
            return VALUES_PLATETHK

    def input_value_changed(self):
        lst = []
        t3 = ([KEY_TORSIONAL_RES], KEY_WARPING_RES, TYPE_COMBOBOX, self.fn_torsion_warping)
        lst.append(t3)
        t45 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_OVERALL_DEPTH_PG, TYPE_TEXTBOX, self.customized_dims)
        lst.append(t45)
        t3 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_TOP_Bflange_PG, TYPE_TEXTBOX, self.customized_dims)
        lst.append(t3)
        t24 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_BOTTOM_Bflange_PG, TYPE_TEXTBOX, self.customized_dims)
        lst.append(t24)
        
        t25 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_WEB_THICKNESS_PG, TYPE_COMBOBOX, self.customize_combo_dims)
        lst.append(t25)
        t26 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_TOP_FLANGE_THICKNESS_PG, TYPE_COMBOBOX, self.customize_combo_dims)
        lst.append(t26)
        t27 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_BOTTOM_FLANGE_THICKNESS_PG, TYPE_COMBOBOX, self.customize_combo_dims)
        lst.append(t27)
        
        t3 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t3)
        t18 = ([KEY_DESIGN_TYPE_FLEXURE], KEY_T_constatnt, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)
        t18 = ([KEY_DESIGN_TYPE_FLEXURE], KEY_T_constatnt, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)
        t18 = ([KEY_DESIGN_TYPE_FLEXURE], KEY_W_constatnt, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)
        t18 = ([KEY_DESIGN_TYPE_FLEXURE], KEY_W_constatnt, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)
        t18 = ([KEY_DESIGN_TYPE_FLEXURE], KEY_Elastic_CM, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)
        t18 = ([KEY_DESIGN_TYPE_FLEXURE], KEY_Elastic_CM, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)
        t19 = ([KEY_WEB_PHILOSOPHY],KEY_IntermediateStiffener_thickness,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t19)
        t20 = ([KEY_WEB_PHILOSOPHY],KEY_IntermediateStiffener_thickness,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t20)
        t21 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudnalStiffener_thickness,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t21)
        t22 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudnalStiffener_thickness,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t22)
        t23 = ([KEY_WEB_PHILOSOPHY],KEY_IntermediateStiffener_spacing,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t23)
        t24 = ([KEY_WEB_PHILOSOPHY],KEY_IntermediateStiffener_spacing,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t24)
        t25 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudnalStiffener_numbers,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t25)
        t26 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudnalStiffener_numbers,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t26)
        t27 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudinalStiffener1_pos,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t27)
        t27 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudinalStiffener1_pos,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t27)
        t27 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudinalStiffener2_pos,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t27)
        t27 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudinalStiffener2_pos,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t27)
        return lst

    def warning_majorbending(self, arg):
        if arg[0] == VALUES_SUPP_TYPE_temp[2]:
            return True
        else:
            return False

    def output_modifier(self, arg):
        if arg[0] == VALUES_SUPP_TYPE_temp[2]:
            return False
        else:
            return True
        
    def output_modifier_long_stiffener(self, arg):
        if arg[0] == 'Thin we':
            return False
        else:
            return True
        
    def output_modifier2(self, arg):
        if arg[0] == 'Thin Web with ITS':
            return False
        else:
            return True

    def output_values(self, flag):
        out_list = []
        
        # 1. Section Details
        t0 = (None, KEY_DISP_PG_SectionDetail, TYPE_TITLE, None, True)
        out_list.append(t0)
        
        t1 = (KEY_TITLE_OPTIMUM_DESIGNATION, KEY_DISP_TITLE_OPTIMUM_DESIGNATION, TYPE_TEXTBOX,
              self.result_designation if flag else '', True)
        out_list.append(t1)
        
        t2 = (KEY_OPTIMUM_SC, KEY_DISP_OPTIMUM_SC, TYPE_TEXTBOX, self.section_classification_val if flag else '', True)
        out_list.append(t2)
        
        t3 = (KEY_OPTIMUM_UR_COMPRESSION, KEY_DISP_OPTIMUM_UR_COMPRESSION, TYPE_TEXTBOX, round(self.result_UR,3) if flag else '', True)
        out_list.append(t3)
        
        t4 = (KEY_EFF_SEC_AREA, KEY_DISP_EFF_SEC_AREA, TYPE_TEXTBOX, self.effectivearea if flag else '', True)
        out_list.append(t4)
        
        t_web = (KEY_WEB_THICKNESS_PG, KEY_DISP_WEB_THICKNESS_PG, TYPE_TEXTBOX,
                 self.web_thickness if flag else '', True)
        out_list.append(t_web)
        
        t_tf_top = (KEY_TOP_FLANGE_THICKNESS_PG, KEY_DISP_TOP_FLANGE_THICKNESS_PG, TYPE_TEXTBOX,
                    self.top_flange_thickness if flag else '', True)
        out_list.append(t_tf_top)
        
        t_tf_bot = (KEY_BOTTOM_FLANGE_THICKNESS_PG, KEY_DISP_BOTTOM_FLANGE_THICKNESS_PG, TYPE_TEXTBOX,
                    self.bottom_flange_thickness if flag else '', True)
        out_list.append(t_tf_bot)

        # 2. Moment Design Details
        t0 = (None, DISP_TITLE_MOMENT_DESIGN, TYPE_TITLE, None, True)
        out_list.append(t0)
        
        t_beta = (KEY_betab_constatnt, KEY_DISP_betab_constatnt, TYPE_TEXTBOX,
                  self.betab if flag else '', True)
        out_list.append(t_beta)
        
        t_warp = (KEY_W_constatnt, KEY_DISP_W_constatnt, TYPE_TEXTBOX, self.warping_cnst if flag else '', True)
        out_list.append(t_warp)
        
        t_tor = (KEY_T_constatnt, KEY_DISP_T_constatnt, TYPE_TEXTBOX,
              self.torsion_cnst if flag else '', True)
        out_list.append(t_tor)
        
        # Mcr
        t_mcr = (KEY_Elastic_CM, KEY_DISP_Elastic_CM, TYPE_TEXTBOX, self.critical_moment if flag else '', True)
        out_list.append(t_mcr)
        
        t_md = (KEY_MOMENT_STRENGTH, KEY_DISP_DESIGN_BENDING_STRENGTH, TYPE_TEXTBOX,
              self.design_moment if flag else '', True)
        out_list.append(t_md)

        # 3. Shear Design Details
        t0 = (None, DISP_TITLE_SHEAR_DESIGN, TYPE_TITLE, None, True)
        out_list.append(t0)
        
        # Shear Capacity (Vd)
        if not hasattr(self, 'V_d') or self.V_d is None: self.V_d = 0
        t_vd = (KEY_SHEAR_STRENGTH, "Shear Capacity (kN)", TYPE_TEXTBOX, round(self.V_d/1000, 2) if flag else '', True)
        out_list.append(t_vd)
        
        # Shear Buckling Resistance (Vcr)
        if not hasattr(self, 'V_cr') or self.V_cr is None: self.V_cr = 0
        t_vcr = (KEY_BUCKLING_STRENGTH, "Shear Buckling Resistance (kN)", TYPE_TEXTBOX, round(self.V_cr/1000, 2) if flag else '', True)
        out_list.append(t_vcr)
        
        # Web Crippling (Fq)
        if not hasattr(self, 'F_q') or self.F_q is None: self.F_q = 0
        t_fq = (KEY_WEB_CRIPPLING, "Web Crippling Strength (kN)", TYPE_TEXTBOX, round(self.F_q/1000, 2) if flag else '', True)
        out_list.append(t_fq)

        # 4. Stiffener Design
        t0 = (None, KEY_DISP_DESIGN_STIFFER, TYPE_TITLE, None, True)
        out_list.append(t0)
        
        # Capacity based on Method
        # Assuming user means the method used? or the capacity? 
        # I'll display the Method Name for now as "Capacity based on..." is ambiguous if value is Vd.
        method_name = "N/A"
        if hasattr(self, 'x'): method_name = self.x # self.x stores the method ('Simple Post...' or 'Tension Field')
        t_method = ('ShearBucklingMethod', "Method", TYPE_TEXTBOX, method_name if flag else '', True)
        out_list.append(t_method)
        
        t_end_thk = (KEY_EndpanelStiffener_thickness, "End Panel Stiffener Thickness (mm)", TYPE_TEXTBOX, self.end_panel_stiffener_thickness if flag else '', True)
        out_list.append(t_end_thk)
        
        # Number of End Panel Stiffeners
        # Default to 2 (Pair) if designed? 
        if flag:
            num_end = "2 (Pair)" if (self.end_panel_stiffener_thickness != "N/A" and self.end_panel_stiffener_thickness != 0) else "0"
        else:
            num_end = ''
        t_end_no = ('EndPanelStiffenerNo', "Number of End Panel Stiffeners", TYPE_TEXTBOX, num_end, True)
        out_list.append(t_end_no)
        
        t_int_thk = (KEY_IntermediateStiffener_thickness, KEY_DISP_IntermediateStiffener_thickness, TYPE_TEXTBOX,
              self.intstiffener_thk if flag else '', True)
        out_list.append(t_int_thk)
        
        t_int_space = (KEY_IntermediateStiffener_spacing, "Intermediate Stiffener Spacing (mm)", TYPE_TEXTBOX,
              self.intstiffener_spacing if flag else '', True)
        out_list.append(t_int_space)
        
        t_long_thk = (KEY_LongitudnalStiffener_thickness, KEY_DISP_LongitudnalStiffener_thickness, TYPE_TEXTBOX,
              self.longstiffener_thk if flag else '', True)
        out_list.append(t_long_thk)
        
        t_long_no = (KEY_LongitudnalStiffener_numbers, KEY_DISP_LongitudnalStiffener_numbers, TYPE_TEXTBOX, self.longstiffener_no if flag else '', True)
        out_list.append(t_long_no)
        
        # Stiffener positions
        t_x1 = (KEY_LongitudinalStiffener1_pos, "Stiffener 1 Pos. from Comp. Flange (mm)", TYPE_TEXTBOX, self.x1 if flag else '',True)
        out_list.append(t_x1)
        t_x2 = (KEY_LongitudinalStiffener2_pos, "Stiffener 2 Pos. from Comp. Flange (mm)", TYPE_TEXTBOX, self.x2 if flag else '',True)
        out_list.append(t_x2)

        # 5. Deflection Check
        t0 = (None, DISP_TITLE_DEFLECTION, TYPE_TITLE, None, True)
        out_list.append(t0)
        
        t_def = (KEY_MAX_DEFL, 'Calculated Deflection (mm)', TYPE_TEXTBOX, self.calculated_deflection if flag else '', True)
        out_list.append(t_def)
        
        t_def_limit = ('DeflectionLimit', 'Permissible Deflection (mm)', TYPE_TEXTBOX, self.deflection_limit if flag else '', True)
        out_list.append(t_def_limit)
        
        # 6. Weld Details
        t0 = (None, "Weld Details", TYPE_TITLE, None, True)
        out_list.append(t0)
        
        # Web-to-Top Flange Weld
        if not hasattr(self, 'atop') or self.atop is None: self.atop = 0
        t_weld_top = ('WeldTopFlange', "Web-to-Top Flange Weld Size (mm)", TYPE_TEXTBOX, round(self.atop, 1) if flag else '', True)
        out_list.append(t_weld_top)
        
        # Web-to-Bottom Flange Weld
        if not hasattr(self, 'abot') or self.abot is None: self.abot = 0
        t_weld_bot = ('WeldBotFlange', "Web-to-Bottom Flange Weld Size (mm)", TYPE_TEXTBOX, round(self.abot, 1) if flag else '', True)
        out_list.append(t_weld_bot)
        
        # Stiffener Weld
        if not hasattr(self, 'weld_stiff') or self.weld_stiff is None: self.weld_stiff = 0
        t_weld_stiff = ('WeldStiffener', "Stiffener Weld Size (mm)", TYPE_TEXTBOX, round(self.weld_stiff, 1) if flag and self.weld_stiff else 'N/A', True)
        out_list.append(t_weld_stiff)
        
        return out_list

    def spacing(self, status):
        spacing = []
        t2 = (KEY_T_constatnt, KEY_DISP_T_constatnt, TYPE_TEXTBOX,
              self.result_tc if status else '', False)
        spacing.append(t2)
        t2 = (KEY_W_constatnt, KEY_DISP_W_constatnt, TYPE_TEXTBOX, self.result_wc if status else '', False)
        spacing.append(t2)
        t2 = (KEY_IMPERFECTION_FACTOR_LTB, KEY_DISP_IMPERFECTION_FACTOR, TYPE_TEXTBOX, self.result_IF_lt if status else '', False)
        spacing.append(t2)
        t2 = (KEY_SR_FACTOR_LTB, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, self.result_srf_lt if status else '', False)
        spacing.append(t2)
        t2 = (KEY_NON_DIM_ESR_LTB, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, self.result_nd_esr_lt if status else '', False)
        spacing.append(t2)
        t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_COMP_STRESS, TYPE_TEXTBOX,
              self.result_fcd__lt if status else '', False)
        spacing.append(t1)
        t2 = (KEY_Elastic_CM, KEY_DISP_Elastic_CM, TYPE_TEXTBOX, self.result_mcr if status else '', False)
        spacing.append(t2)

    def func_for_validation(self, design_dictionary):
        if self.debug:
            print("\n" + "-"*40)
            print("DEBUG: PLATE GIRDER - func_for_validation")
            print(f"DEBUG: design_dictionary keys count: {len(design_dictionary)}")
        
        all_errors = []
        self.design_status = False
        flag = False
        self.output_values(flag)
        flag1 = False
        flag2 = False
        flag3 = False
        option_list = self.input_values()
        if self.debug:
            print(f"DEBUG: Checking {len(option_list)} options for validation")
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX or option[0] == KEY_LENGTH or option[0] == KEY_SHEAR or option[0] == KEY_MOMENT:
                try:
                    if design_dictionary[option[0]] == '':
                        if design_dictionary['Total.Design_Type'] == 'Optimized':
                            if design_dictionary[KEY_OVERALL_DEPTH_PG] == '' or design_dictionary[KEY_TOP_Bflange_PG] == '' or design_dictionary[KEY_BOTTOM_Bflange_PG] == '':
                                pass
                            else:
                                missing_fields_list.append(option[1])
                                continue
                        else:
                            missing_fields_list.append(option[1])
                            continue
                    if option[0] == KEY_LENGTH:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True
                    elif option[0] == KEY_SHEAR:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag2 = True
                    elif option[0] == KEY_MOMENT:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag3 = True
                except:
                        error = "Input value(s) are not valid"
                        all_errors.append(error)

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(missing_fields_list)
            all_errors.append(error)
            if self.debug:
                print(f"DEBUG: Validation FAILED - Missing fields: {missing_fields_list}")
        else:
            flag = True
        
        if self.debug:
            print(f"DEBUG: Validation flags -> flag(fields):{flag}, flag1(length):{flag1}, flag2(shear):{flag2}, flag3(moment):{flag3}")
        
        if flag and flag1 and flag2 and flag3:
            if self.debug:
                print("DEBUG: Validation PASSED - Calling set_input_values")
            self.set_input_values(design_dictionary)
        else:
            if self.debug:
                print(f"DEBUG: Validation FAILED - Errors: {all_errors}")
            return all_errors
        if self.debug:
            print("-"*40 + "\n")

    def get_3d_components(self):
        components = []
        t1 = ('Model', self.call_3DModel)
        components.append(t1)
        t2 = ('Web', self.call_3DWeb)
        components.append(t2)
        t3 = ('Top Flange', self.call_3DTopFlange)
        components.append(t3)
        t4 = ('Bottom Flange', self.call_3DBottomFlange)
        components.append(t4)
        t5 = ('Stiffeners', self.call_3DStiffeners)
        components.append(t5)
        t6 = ('Welds', self.call_3DWelds)
        components.append(t6)
        return components

    def call_3DWeb(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Web':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Web", bgcolor)

    def call_3DTopFlange(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Top Flange':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Top Flange", bgcolor)

    def call_3DBottomFlange(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Bottom Flange':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Bottom Flange", bgcolor)

    def call_3DStiffeners(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Stiffeners':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Stiffeners", bgcolor)

    def call_3DWelds(self, ui, bgcolor):
        from PySide6.QtWidgets import QCheckBox
        for chkbox in ui.cad_comp_widget.children():
            if chkbox.objectName() == 'Welds':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(False)
        ui.commLogicObj.display_3DModel("Welds", bgcolor)

    def warn_text(self):
        red_list = red_list_function()
        if (self.sec_profile == VALUES_SEC_PROFILE[0]) or (self.sec_profile == VALUES_SEC_PROFILE[1]):
            for section in self.sec_list:
                if section in red_list:
                    self.logger.warning(" : You are using a section ({}) (in red color) that is not available in latest version of IS 808".format(section))

    def set_input_values(self, design_dictionary):
        if self.debug:
            print("\n" + "="*60)
            print("DEBUG: PLATE GIRDER - set_input_values")
            print("DEBUG: Input Dictionary (Sorted Keys):")
            for key in sorted(design_dictionary.keys()):
                print(f"  {key}: {design_dictionary[key]}")
            print("="*60 + "\n")
        
        self.module = design_dictionary[KEY_MODULE]
        self.mainmodule = 'PLATE GIRDER'
        self.design_type = design_dictionary[KEY_OVERALL_DEPTH_PG_TYPE]
        self.section_class = None
        if self.design_type == 'Optimized':
            self.total_depth = 1
            if design_dictionary[KEY_WEB_THICKNESS_PG] == 'All':
                self.web_thickness_list = VALUES_PLATETHK_CUSTOMIZED
                self.web_thickness = float(VALUES_PLATETHK_CUSTOMIZED[0])
            else:
                self.web_thickness_list = [design_dictionary[KEY_WEB_THICKNESS_PG]]
                self.web_thickness = float(design_dictionary[KEY_WEB_THICKNESS_PG])

            self.top_flange_width = 1
            if design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG] == 'All':
                self.top_flange_thickness_list = VALUES_PLATETHK_CUSTOMIZED
                self.top_flange_thickness = float(VALUES_PLATETHK_CUSTOMIZED[0])
            else:
                self.top_flange_thickness_list = [design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG]]
                self.top_flange_thickness = float(design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG])

            self.bottom_flange_width = 1
            if design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG] == 'All':
                self.bottom_flange_thickness_list = VALUES_PLATETHK_CUSTOMIZED
                self.bottom_flange_thickness = float(VALUES_PLATETHK_CUSTOMIZED[0])
            else:
                self.bottom_flange_thickness_list = [design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG]]
                self.bottom_flange_thickness = float(design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG])

        else:
            self.total_depth = float(design_dictionary[KEY_OVERALL_DEPTH_PG])
            if design_dictionary[KEY_WEB_THICKNESS_PG] == 'All':
                self.web_thickness_list = VALUES_PLATETHK_CUSTOMIZED
                self.web_thickness = float(VALUES_PLATETHK_CUSTOMIZED[0])
            else:
                self.web_thickness_list = [design_dictionary[KEY_WEB_THICKNESS_PG]]
                self.web_thickness = float(design_dictionary[KEY_WEB_THICKNESS_PG])

            self.top_flange_width = float(design_dictionary[KEY_TOP_Bflange_PG])
            if design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG] == 'All':
                self.top_flange_thickness_list = VALUES_PLATETHK_CUSTOMIZED
                self.top_flange_thickness = float(VALUES_PLATETHK_CUSTOMIZED[0])
            else:
                self.top_flange_thickness_list = [design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG]]
                self.top_flange_thickness = float(design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG])

            self.bottom_flange_width = float(design_dictionary[KEY_BOTTOM_Bflange_PG])
            if design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG] == 'All':
                self.bottom_flange_thickness_list = VALUES_PLATETHK_CUSTOMIZED
                self.bottom_flange_thickness = float(VALUES_PLATETHK_CUSTOMIZED[0])
            else:
                self.bottom_flange_thickness_list = [design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG]]
                self.bottom_flange_thickness = float(design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG])

        thickness_for_mat = max(self.web_thickness,self.top_flange_thickness, self.bottom_flange_thickness)
        self.eff_depth = self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness
        self.IntStiffnerwidth = min(self.top_flange_width,self.bottom_flange_width) - self.web_thickness/2 - 10
        self.material = Material(design_dictionary[KEY_MATERIAL],thickness_for_mat)
        if self.debug:
            print(f"DEBUG: Material Created -> Grade: {design_dictionary[KEY_MATERIAL]}, Thickness: {thickness_for_mat}mm, fy={self.material.fy} MPa, fu={self.material.fu} MPa")
        self.eff_width_longitudnal = min(self.top_flange_width,self.bottom_flange_width) - self.web_thickness/2 - 10
        
        if design_dictionary[KEY_IntermediateStiffener_thickness] == 'Customized':
            design_dictionary[KEY_IntermediateStiffener_thickness_val] = PlateGirderWelded.int_thicklist
        else:
            design_dictionary[KEY_IntermediateStiffener_thickness_val] = VALUES_STIFFENER_THICKNESS
        
        self.int_thickness_list = design_dictionary[KEY_IntermediateStiffener_thickness_val]

        if design_dictionary[KEY_LongitudnalStiffener_thickness] == 'Customized':
            design_dictionary[KEY_LongitudnalStiffener_thickness_val] = PlateGirderWelded.long_thicklist
        else:
            design_dictionary[KEY_LongitudnalStiffener_thickness_val] = VALUES_STIFFENER_THICKNESS

        self.long_thickness_list = design_dictionary[KEY_LongitudnalStiffener_thickness_val]
        self.deflection_criteria= design_dictionary[KEY_MAX_DEFL]
        self.support_condition = 'Simply Supported'
        self.loading_case = design_dictionary[KEY_BENDING_MOMENT_SHAPE]
        self.shear_type = None
        self.support_type = design_dictionary[KEY_DESIGN_TYPE_FLEXURE]
        self.loading_condition = design_dictionary[KEY_LOAD]
        self.torsional_res = design_dictionary[KEY_TORSIONAL_RES]
        self.warping = design_dictionary[KEY_WARPING_RES]
        self.length = float(design_dictionary[KEY_LENGTH])

        # Calculate effective length for lateral-torsional buckling
        # lefactor depends on support type: 0.7 for laterally supported, 1.0 for unsupported
        if design_dictionary[KEY_DESIGN_TYPE_FLEXURE] == 'Major Laterally Supported':
            self.lefactor = 0.7
        else:
            self.lefactor = 1.0
        self.effective_length = self.length * self.lefactor
        self.allow_class = design_dictionary[KEY_ALLOW_CLASS]
        self.loading_case = design_dictionary[KEY_BENDING_MOMENT_SHAPE]
        self.beta_b_lt = None
        self.web_philosophy = design_dictionary[KEY_WEB_PHILOSOPHY]
        self.epsilon = math.sqrt(250 / self.material.fy)  # IS 800:2007: ε = √(250/fy), fy in MPa
        self.b1 = float(design_dictionary[KEY_SUPPORT_WIDTH])
        self.c = design_dictionary[KEY_IntermediateStiffener_spacing]
        self.Is = None
        self.IntStiffThickness = float(self.int_thickness_list[0])
        self.LongStiffThickness = float(self.long_thickness_list[0])
        self.x1= 0
        self.x2 = 0
        self.V_cr = None
        self.V_d = None
        self.V_tf = None
        self.long_Stiffner = design_dictionary[KEY_LongitudnalStiffener]
        self.load = Load(shear_force=design_dictionary[KEY_SHEAR],axial_force="",moment=design_dictionary[KEY_MOMENT],unit_kNm=True,)
        # Imperfection factor per IS 800:2007 Table 10 for welded I-sections
        # tf <= 40mm: Curve c (alpha_lt = 0.49), tf > 40mm: Curve d (alpha_lt = 0.76)
        max_tf = max(self.top_flange_thickness, self.bottom_flange_thickness)
        if max_tf <= 40:
            self.alpha_lt = 0.49  # Curve c for welded sections with tf <= 40mm
        else:
            self.alpha_lt = 0.76  # Curve d for welded sections with tf > 40mm
        self.phi_lt = None
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        self.X_lt = None
        self.fbd_lt = None
        self.Md = None
        # Note: lefactor is already calculated earlier along with effective_length
        self.M_cr = None
        self.F_q = None
        self.Critical_buckling_load = None
        self.shear_ratio = 0
        self.endshear_ratio = 0
        self.moment_ratio = 0
        self.deflection_ratio = 0
        self.It = None
        self.Iw = None
        self.torsion_cnst = None
        self.warping_cnst = None
        self.critical_moment = None
        self.fcd = None
        self.end_stiffthickness = 0
        self.stiffener_type = None
        self.end_panel_stiffener_thickness = None
        self.end_stiffwidth = min(self.top_flange_width,self.bottom_flange_width)/2 - self.web_thickness/2 - 10
        self.design_status = False

        self.shear_force_optimal = False
        self.moment_optimal = False
        self.min_mass = False  
        if self.design_type == 'Optimized':
            is_thick_web = False
            is_symmetric = False
            if self.web_philosophy == 'Thick Web without ITS':
                is_thick_web = True
            else:
                is_thick_web = False

            if design_dictionary[KEY_IS_IT_SYMMETRIC] == 'Symmetric Girder':
                is_symmetric = True
            else:
                is_symmetric = False
            self.optimized_method(design_dictionary, is_thick_web, is_symmetric, 
                                   viz_callback=getattr(self, '_viz_callback', None))
        else:
            self.design_check(design_dictionary)

    def calculate_stiffener_spacing_IS800(self):
        """
        Calculate intermediate stiffener spacing 'c' per IS 800:2007.
        
        Reference Clauses:
        - Cl. 8.6.1.1 & 8.6.1.2: Minimum web thickness requirements based on c
        - Cl. 8.7.2.4: Stiffener spacing limits
        - Cl. 8.4.2.2: Shear buckling strength with K_v based on c/d ratio
        
        IS 800:2007 Guidelines:
        - For efficient shear resistance: c ≤ 1.5d (where d = effective depth)
        - For buckling control: c ≥ d for most cases
        - Minimum practical spacing: c ≥ 0.5d
        - Maximum spacing without needing special design: c ≤ 3d
        
        Returns:
            float: Calculated stiffener spacing 'c' in mm
        """
        d = self.eff_depth  # Effective depth of web
        tw = self.web_thickness
        fy = self.material.fy  # Yield strength in MPa
        E = self.material.modulus_of_elasticity
        shear_force = self.load.shear_force
        
        # Web slenderness ratio
        web_slenderness = d / tw
        
        # Determine c based on web slenderness and IS 800:2007 limits
        # For transverse stiffeners only (Cl. 8.6.1.2):
        # d/tw ≤ 200ε for c ≥ 1.5d
        # d/tw ≤ 270ε for c < 0.74d
        
        slenderness_limit_200 = 200 * self.epsilon
        slenderness_limit_270 = 270 * self.epsilon
        
        # Calculate Avw (shear area of web)
        A_vw = d * tw
        
        # Design shear strength without stiffeners (Cl. 8.4.1)
        V_p = (fy / math.sqrt(3)) * A_vw / self.gamma_m0
        
        if web_slenderness <= 67 * self.epsilon:
            # Thick web - no stiffeners needed for shear buckling
            # Use maximum spacing (essentially single panel)
            c = 3 * d
            self.logger.info(f"Thick web (d/tw = {web_slenderness:.2f} ≤ {67 * self.epsilon:.2f}ε), c = 3d = {c:.2f} mm")
        elif shear_force <= 0.6 * V_p:
            # Low shear - larger spacing acceptable
            c = min(1.5 * d, 3 * d)
            self.logger.info(f"Low shear condition, c = 1.5d = {c:.2f} mm")
        else:
            # High shear - need to calculate c for required shear buckling resistance
            # Target K_v value for shear buckling check (Cl. 8.4.2.2)
            # Starting with c = d (optimal spacing for most cases)
            
            if web_slenderness <= slenderness_limit_200:
                # Can use spacing c ≥ 1.5d
                c = 1.5 * d
            else:
                # Need closer spacing for higher web slenderness
                # Use c = d as a good starting point
                c = d
                
                # For very slender webs, may need closer spacing
                if web_slenderness > slenderness_limit_270:
                    # Need c < 0.74d for very slender webs
                    c = 0.74 * d
                    self.logger.warning(f"Very slender web (d/tw = {web_slenderness:.2f}), using c = 0.74d = {c:.2f} mm")
        
        # Apply practical limits per IS 800 Cl. 8.7.2.4
        # Minimum spacing: 0.5d for practical fabrication and stiffener design
        c = max(c, 0.5 * d)
        # Maximum spacing: 3d (beyond which stiffeners have limited effect)
        c = min(c, 3 * d)
        
        # Round to nearest 25 mm for practical dimensions
        c = math.ceil(c / 25) * 25
        
        return c

    def section_classification(self,design_dictionary):
        self.design_status = False
        # Check if longitudinal stiffener is provided (affects web slenderness limits per Cl. 8.6.1.2)
        has_long_stiff = self.long_Stiffner in ['Yes and 1 stiffener', 'Yes and 2 stiffeners']
        self.section_class, is_valid = classify_section(
            self.top_flange_width, self.top_flange_thickness, 
            self.bottom_flange_width, self.bottom_flange_thickness, 
            self.total_depth, self.web_thickness, 
            self.material.fy, self.web_philosophy, 
            has_longitudinal_stiffener=has_long_stiff,
            debug=self.debug
        )
        return is_valid

    def design_check(self,design_dictionary):
        if self.debug:
            print("\n" + "="*50)
            print("DEBUG: Starting design_check")
            print(f"DEBUG: Input D={self.total_depth}, tw={self.web_thickness}, bf_top={self.top_flange_width}, tf_top={self.top_flange_thickness}")
            print(f"DEBUG: Input bf_bot={self.bottom_flange_width}, tf_bot={self.bottom_flange_thickness}")
            print(f"DEBUG: Load: V={self.load.shear_force}, M={self.load.moment}")
        
        self.design_flag = False
        self.design_flag2 = False
        self.shearflag1 = False
        self.shearflag2 = False
        self.shearflag3 = False
        self.shearchecks = False
        self.momentchecks = False
        self.defl_check = False
        self.long_check = False
        self.design_flag = self.section_classification(design_dictionary)
        print(f"DEBUG: section_classification result: {self.design_flag} (Class: {self.section_class})")
        if self.design_flag == False:
            print(f"DEBUG: !!! DESIGN REJECTED: Section is Slender. Classify parameters: D={self.total_depth}, tw={self.web_thickness}, bf_top={self.top_flange_width}, tf_top={self.top_flange_thickness}")
            self.logger.error("slender section not allowed")
        else:
            if not hasattr(self, 'flange_warning_logged'):
                self.flange_warning_logged = False
            if not hasattr(self, 'dimension_warning_logged'):
                self.dimension_warning_logged = False
            # Design efficiency check: warn if b/tf is too small (flanges too thick for their width)
            # NOTE: This is NOT an IS 800:2007 requirement. IS 800 Table 2 has MAXIMUM b/tf limits only.
            # The 7.4ε threshold is an engineering guideline to avoid material waste.
            min_b_tf = 7.4 * self.epsilon
            b_tf_top = (self.top_flange_width - self.web_thickness) / (2 * self.top_flange_thickness)
            if b_tf_top < min_b_tf and not self.flange_warning_logged:
                self.logger.warning(f"Top flange b/tf ratio ({b_tf_top:.2f}) is below efficiency guideline ({min_b_tf:.2f}), consider using thinner flanges")
                self.flange_warning_logged = True
            
            b_tf_bot = (self.bottom_flange_width - self.web_thickness) / (2 * self.bottom_flange_thickness)
            if b_tf_bot < min_b_tf and not self.flange_warning_logged:
                self.logger.warning(f"Bottom flange b/tf ratio ({b_tf_bot:.2f}) is less than minimum ({min_b_tf:.2f}), flanges may be too thick")
                self.flange_warning_logged = True
            
            if self.bottom_flange_width < self.top_flange_width and not self.dimension_warning_logged:
                self.logger.warning(f"Bottom flange width ({self.bottom_flange_width:.2f} mm) is less than top flange width ({self.top_flange_width:.2f} mm)")
                self.dimension_warning_logged = True
            
            if self.bottom_flange_thickness < self.top_flange_thickness and not self.dimension_warning_logged:
                self.logger.warning(f"Bottom flange thickness ({self.bottom_flange_thickness:.2f} mm) is less than top flange thickness ({self.top_flange_thickness:.2f} mm)")
                self.dimension_warning_logged = True
            
            # self.beta_value(design_dictionary,self.section_class) # TODO: Extract beta_value logic if needed, or use section_class directly

            # Calculate section properties needed for moment capacity checks
            from ....utils.common.Unsymmetrical_Section_Properties import Unsymmetrical_I_Section_Properties
            
            # Check for Minor Axis Design
            if 'Minor' in self.support_type:
                self.logger.info("Design Type is Minor Axis: Using Zpy and Zey properties")
                self.plast_sec_mod_z = Unsymmetrical_I_Section_Properties.calc_PlasticModulusY(
                    self.total_depth, self.top_flange_width, self.bottom_flange_width,
                    self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, debug=self.debug)
                self.elast_sec_mod_z = Unsymmetrical_I_Section_Properties.calc_ElasticModulusZy(
                    self.total_depth, self.top_flange_width, self.bottom_flange_width,
                    self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, debug=self.debug
                )
            else:
                self.plast_sec_mod_z = Unsymmetrical_I_Section_Properties.calc_PlasticModulusZ(
                    self.total_depth, self.top_flange_width, self.bottom_flange_width,
                    self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness,
                    self.epsilon, debug=self.debug)
                self.elast_sec_mod_z = Unsymmetrical_I_Section_Properties.calc_ElasticModulusZz(
                    self.total_depth, self.top_flange_width, self.bottom_flange_width,
                    self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, debug=self.debug
                )
            if self.debug:
                print(f"\n========== PLATE GIRDER DESIGN VALUES ==========")
                print(f"Plastic Modulus (Zp): {self.plast_sec_mod_z:.2f} mm³")
                print(f"Elastic Modulus (Ze): {self.elast_sec_mod_z:.2f} mm³")
                print(f"Section Classification: {self.section_class}")
                print(f"=================================================\n")

            if self.web_philosophy == 'Thick Web without ITS':
                self.design_flag2 = min_web_thickness_thick_web(self.eff_depth,self.web_thickness,self.epsilon,"no_stiffener",0, debug=self.debug)
                if self.debug:
                    print(f"[DEBUG] Thick Web Philosophy: d/tw={self.eff_depth/self.web_thickness:.2f}, thickness_ok={self.design_flag2}")
                if self.design_flag2 == True:
                    # Print input values for debugging
                    if self.debug:
                        print(f"\n--- Input Values for Design Checks ---")
                        print(f"  Shear Force: {self.load.shear_force:.2f} N")
                        print(f"  Yield Strength (Fy): {self.material.fy:.2f} MPa")
                        print(f"  Gamma_m0: {self.gamma_m0}")
                        print(f"  Total Depth (D): {self.total_depth:.2f} mm")
                        print(f"  Web Thickness (tw): {self.web_thickness:.2f} mm")
                        print(f"  Top Flange Thickness: {self.top_flange_thickness:.2f} mm")
                        print(f"  Bottom Flange Thickness: {self.bottom_flange_thickness:.2f} mm")
                        print(f"  Effective Depth (d): {self.eff_depth:.2f} mm")
                        print(f"--------------------------------------\n")
                    
                    # Correct argument order: (Fy, gamma_m0, D, tw, tf_top, tf_bot, shear_force)
                    is_safe, self.V_d, self.shear_ratio = shear_capacity_laterally_supported_thick_web(self.material.fy, self.gamma_m0, self.total_depth, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, self.load.shear_force, debug=self.debug)
                    
                    # Determine low shear or high shear condition (IS 800:2007 Cl. 9.2.1)
                    low_shear_limit = 0.6 * self.V_d
                    if self.load.shear_force <= low_shear_limit:
                        self.shear_type = 'Low'
                        if self.debug:
                            print(f"\n========== SHEAR CAPACITY CHECK ==========")
                            print(f"  Design Shear Capacity (V_d): {self.V_d:.2f} N")
                            print(f"  Low Shear Limit (0.6 × V_d): {low_shear_limit:.2f} N")
                            print(f"  Applied Shear Force: {self.load.shear_force:.2f} N")
                            print(f"  >>> LOW SHEAR CONDITION (V ≤ 0.6 × V_d) <<<")
                            print(f"============================================\n")
                    else:
                        self.shear_type = 'High'
                        if self.debug:
                            print(f"\n========== SHEAR CAPACITY CHECK ==========")
                            print(f"  Design Shear Capacity (V_d): {self.V_d:.2f} N")
                            print(f"  Low Shear Limit (0.6 × V_d): {low_shear_limit:.2f} N")
                            print(f"  Applied Shear Force: {self.load.shear_force:.2f} N")
                            print(f"  >>> HIGH SHEAR CONDITION (V > 0.6 × V_d) <<<")
                            print(f"============================================\n")
                    if is_safe:
                        self.shearflag1 = True
                        self.logger.info("Shear Check passed")
                    else:
                        self.shearflag1 = False
                        self.logger.error("Shear Check failed")

                    is_safe, self.V_cr = web_buckling_laterally_supported_thick_web(self.material.fy, self.gamma_m0, self.total_depth, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, self.material.modulus_of_elasticity, self.b1, self.load.shear_force, debug=self.debug)
                    if self.debug:
                        print(f"Buckling Resistance (V_cr): {self.V_cr:.2f} N")
                    if is_safe:
                        self.shearflag2 = True
                        self.logger.info("Web Buckling Check passed")
                    else:
                        self.shearflag2 = False
                        self.logger.error("Web Buckling Check failed")
                    
                    web_height = self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness
                    is_safe, self.F_q = check_web_crippling(self.load.shear_force, self.b1, self.web_thickness, self.material.fy, web_height, self.gamma_m0, self.logger, debug=self.debug)
                    if self.debug:
                        print(f"Crippling Resistance (F_q): {self.F_q:.2f} N")
                    if is_safe:
                        self.shearflag3 = True
                        self.logger.info("Web Crippling Check passed")
                    else:
                        self.shearflag3 = False
                        self.logger.error("Web Crippling Check failed")
                    
                    if self.shearflag1 == True and self.shearflag2 == True and self.shearflag3 == True:
                        self.shearchecks = True
                    else:
                        self.shearchecks = False
                    
                    if self.support_type == 'Major Laterally Supported':
                        is_safe, self.Md, self.moment_ratio, self.V_d = moment_capacity_laterally_supported(self.load.shear_force,self.plast_sec_mod_z,self.elast_sec_mod_z,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.section_class, self.support_condition, self.load.moment, debug=self.debug)
                        if self.debug:
                            print(f"Moment Capacity (Md / design_moment): {self.Md:.2f} N-mm")
                        if is_safe:
                            self.momentchecks = True
                            self.logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            self.logger.error("Moment Check failed")
                    else: 
                        is_safe, self.Md, self.moment_ratio, self.V_d, self.M_cr, self.lambda_lt, self.phi_lt, self.X_lt, self.fbd_lt, self.It, self.Iw = moment_capacity_laterally_unsupported(self.material.modulus_of_elasticity,self.effective_length,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.loading_case,self.gamma_m0,self.material.fy,self.load.shear_force, self.warping, self.load.moment, self.plast_sec_mod_z, self.elast_sec_mod_z, self.section_class, self.alpha_lt, debug=self.debug)
                        if self.debug:
                            print(f"Moment Capacity (Md / design_moment): {self.Md:.2f} N-mm")
                        if is_safe:
                            self.momentchecks = True
                            self.logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            self.logger.error("Moment Check failed")
                    if self.debug:
                        print(f"=================================================\n")
                else:
                    self.logger.error("Increase the web thickness")

            else: #thin web condition
                self.shear_ratio= 0
                if self.long_Stiffner == 'Yes and 1 stiffener':
                    self.stiffener_type = "transverse_and_one_longitudinal_compression"
                elif self.long_Stiffner == 'Yes and 2 stiffeners':
                    self.stiffener_type = "transverse_and_two_longitudinal_neutral"
                else:
                    self.stiffener_type = "transverse_only"
                if self.stiffener_type != "transverse_only":
                    second_stiffener = False
                    if self.stiffener_type == "transverse_and_two_longitudinal_neutral":
                        second_stiffener = True
                    
                    # Longitudinal stiffener design per IS 800:2007 Cl. 8.7.13
                    # Position: First at 0.2d from compression flange, second at 0.5d (neutral axis) if needed
                    num_long_stiff = 1
                    if self.stiffener_type == "transverse_and_two_longitudinal_neutral":
                        num_long_stiff = 2
                    self.longstiffener_no = num_long_stiff
                    
                    # Use stiffener spacing if available, otherwise design_longitudinal_stiffener handles default
                    c_input = self.c
                    
                    is_safe_long, t_long_sel, b_long_sel, x1, x2, I_req1, I_prov1, I_req2, I_prov2 = design_longitudinal_stiffener(
                        self.eff_depth, self.web_thickness, c_input, num_long_stiff, 
                        self.long_thickness_list, self.web_philosophy, self.epsilon, 
                        self.gamma_m0, self.material.fy, debug=self.debug
                    )
                    
                    if is_safe_long:
                        self.long_check = True
                        self.longstiffener_thk = t_long_sel
                        self.x1 = round(x1, 2)
                        if num_long_stiff == 2:
                            self.x2 = round(x2, 2)
                        else:
                            self.x2 = 0
                        self.logger.info(f"Longitudinal Stiffener Check passed (t={t_long_sel}mm)")
                    else:
                        self.long_check = False
                        self.logger.error("Longitudinal Stiffener Check failed (available thickness insufficient)")

                if self.c == 'NA':
                    # Calculate c per IS 800:2007 Cl. 8.6.1.1, 8.6.1.2 and 8.7
                    # For thin webs with intermediate transverse stiffeners:
                    # The spacing c should satisfy web slenderness limits and provide adequate shear buckling resistance
                    self.c = self.calculate_stiffener_spacing_IS800()
                    self.logger.info(f"Calculated stiffener spacing (c) per IS 800:2007: {self.c:.2f} mm")
                else:
                    self.c = float(self.c)
                
                self.design_flag2 = min_web_thickness_thick_web(self.eff_depth,self.web_thickness,self.epsilon,self.stiffener_type,self.c, debug=self.debug)
                if self.design_flag2 == True:
                    self.x= design_dictionary[KEY_ShearBucklingOption]

                    if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':
                        is_safe, self.V_d, self.shear_ratio = shear_buckling_check_simple_postcritical(self.eff_depth, self.total_depth, self.top_flange_thickness, self.bottom_flange_thickness, self.web_thickness, self.load.shear_force, self.web_philosophy, self.material.modulus_of_elasticity, self.material.fy, self.load.shear_force, self.c, debug=self.debug)
                        if is_safe:
                            self.shearflag1 = True
                            self.logger.info("Shear Check passed")
                        else:
                            self.logger.info("Shear Check Failed, add end stiffeners")
                            result = end_panel_stiffener_calc(self.top_flange_width, self.bottom_flange_width,
                                                             self.web_thickness, self.end_stiffthickness,
                                                             self.material.fy, self.gamma_m0, self.eff_depth,
                                                             self.top_flange_thickness, self.total_depth,
                                                             self.effective_length, self.bottom_flange_thickness,
                                                             self.material.modulus_of_elasticity, self.epsilon, self.c, self.web_philosophy, self.load.moment, self.load.shear_force,
                                                             self.int_thickness_list, self.end_stiffwidth, self.end_stiffthickness, self.logger, debug=self.debug)
                            is_safe_end = result[0]
                            self.end_stiffwidth = result[1]
                            self.end_stiffthickness = result[2]
                            if is_safe_end:
                                self.logger.info("End Panel Stiffener Check passed")
                            else:
                                self.logger.error("End Panel Stiffener Check failed")
                    
                        is_safe_int, Pd, _, self.IntStiffnerwidth, self.V_cr_new = shear_buckling_check_intermediate_stiffener(self.eff_depth, self.web_thickness, self.c, self.epsilon, self.IntStiffThickness, self.IntStiffnerwidth, self.load.shear_force, self.gamma_m0, self.material.fy, self.material.modulus_of_elasticity, self.web_philosophy, self.lefactor, self.load.shear_force, debug=self.debug)
                        if self.V_cr_new is not None:
                             self.V_cr = self.V_cr_new

                        if is_safe_int:
                            self.shearflag2 = True
                            self.logger.info("Shear Buckling Check passed with intermediate stiffeners")
                        else:
                            self.shearflag2 = False
                            self.logger.error("Shear Buckling Check failed with intermediate stiffeners, increase stiffener thickness")

                        # Web Crippling Check (Added for Thin Web with ITS/Simple Post Critical)
                        web_height = self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness
                        is_safe_crip, self.F_q = check_web_crippling(self.load.shear_force, self.b1, self.web_thickness, self.material.fy, web_height, self.gamma_m0, self.logger, debug=self.debug)
                        if is_safe_crip:
                            self.shearflag3 = True
                            self.logger.info("Web Crippling Check passed")
                        else:
                            self.shearflag3 = False
                            self.logger.error("Web Crippling Check failed")
                            

                    
                    else: #tension field
                        is_safe_tf, self.V_tf, self.shear_ratio, self.V_cr = shear_buckling_check_tension_field(self.eff_depth, self.total_depth, self.top_flange_thickness, self.bottom_flange_thickness, self.web_thickness, self.c, self.web_philosophy, self.material.modulus_of_elasticity, self.material.fy, self.load.shear_force, self.load.moment, self.top_flange_width, self.top_flange_thickness, self.bottom_flange_width, self.bottom_flange_thickness, self.gamma_m0, debug=self.debug)
                        if is_safe_tf:
                            self.shearflag1 = True
                            self.logger.info("Shear Buckling Check passed")
                        else:
                            self.logger.error("Shear Buckling Check failed, provide end panel stiffeners")
                            result_tf = tension_field_end_stiffener(self.eff_depth, self.web_thickness, self.material.fy,
                                                              self.load.shear_force, self.load.moment,
                                                              self.c, self.web_philosophy, self.material.modulus_of_elasticity,
                                                              self.top_flange_thickness, self.bottom_flange_thickness,
                                                              self.top_flange_width, self.bottom_flange_width,
                                                              self.gamma_m0, self.int_thickness_list, self.IntStiffnerwidth, self.IntStiffThickness, self.epsilon, self.lefactor, debug=self.debug)
                            is_safe_end_tf = result_tf[0]
                            self.end_stiffthickness = result_tf[5] if len(result_tf) > 5 else 0
                            if is_safe_end_tf:
                                self.shearflag1 = True
                                self.logger.info("Tension Field Check passed with stiffeners")
                            else:
                                self.shearflag1 = False
                                self.logger.error("Tension Field Check failed, increase stiffener thickness")

                        is_safe_int_tf, self.V_tf, _, self.IntStiffnerwidth, self.V_cr_new = tension_field_intermediate_stiffener(self.eff_depth, self.web_thickness, self.c, self.epsilon, self.IntStiffThickness, self.IntStiffnerwidth, self.load.shear_force, self.gamma_m0, self.material.fy, self.material.modulus_of_elasticity, self.web_philosophy, self.lefactor, self.load.shear_force, debug=self.debug)
                        if self.V_cr_new is not None:
                             self.V_cr = self.V_cr_new
                        
                        if is_safe_int_tf:
                            self.shearflag2 = True
                            self.logger.info("Shear Buckling Check passed with intermediate stiffeners")
                        else:
                            self.shearflag2 = False
                            self.logger.error("Shear Buckling Check failed, increase stiffener thickness")

                        # Web Crippling Check (Added for Thin Web with ITS/Tension Field)
                        web_height = self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness
                        is_safe_crip, self.F_q = check_web_crippling(self.load.shear_force, self.b1, self.web_thickness, self.material.fy, web_height, self.gamma_m0, self.logger, debug=self.debug)
                        if is_safe_crip:
                            self.shearflag3 = True
                            self.logger.info("Web Crippling Check passed")
                        else:
                            self.shearflag3 = False
                            self.logger.error("Web Crippling Check failed")

                    if self.shearflag1 == True and self.shearflag2 == True and self.shearflag3 == True:
                        self.shearchecks = True
                    else:
                        self.shearchecks = False

                    if self.support_type == 'Major Laterally Supported':
                        is_safe, self.Md, self.moment_ratio, self.V_d = moment_capacity_laterally_supported(self.load.shear_force,self.plast_sec_mod_z,self.elast_sec_mod_z,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.section_class, self.support_condition, self.load.moment, debug=self.debug)
                        if self.debug:
                            print(f"Moment Capacity (Md / design_moment): {self.Md:.2f} N-mm")
                        if is_safe:
                            self.momentchecks = True
                            self.logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            self.logger.error("Moment Check failed")
                    else:
                        is_safe, self.Md, self.moment_ratio, self.V_d, self.M_cr, self.lambda_lt, self.phi_lt, self.X_lt, self.fbd_lt, self.It, self.Iw = moment_capacity_laterally_unsupported(self.material.modulus_of_elasticity,self.effective_length,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.loading_case,self.gamma_m0,self.material.fy,self.load.shear_force, self.warping, self.load.moment, self.plast_sec_mod_z, self.elast_sec_mod_z, self.section_class, self.alpha_lt, debug=self.debug)
                        if is_safe:
                            self.momentchecks = True
                            self.logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            self.logger.error("Moment Check failed")

                else:
                    pass

        # Deflection checks per IS 800:2007 Table 6
        if not SKIP_DEFLECTION:
            # Note: self.load.moment is in N·mm, but evaluate_deflection_kNm_mm expects kN·m
            moment_kNm = self.load.moment / 1e6  # Convert N·mm to kN·m
            is_safe, self.deflection_ratio, delta, allowable = evaluate_deflection_kNm_mm(
                moment_kNm, self.length, self.material.modulus_of_elasticity,
                self.loading_case, self.deflection_criteria, self.total_depth,
                self.top_flange_width, self.bottom_flange_width, self.web_thickness,
                self.top_flange_thickness, self.bottom_flange_thickness,
                debug=self.debug
            )
            self.calculated_deflection = round(delta, 2)
            self.deflection_limit = round(allowable, 2)
            
            if is_safe:
                self.defl_check = True
                self.logger.info("Deflection Check passed")
            else:
                self.defl_check = False
                self.logger.error("Deflection Check failed")
        else:
            self.defl_check = True
            self.deflection_ratio = 0.0
            self.calculated_deflection = "Skipped"
            self.deflection_limit = "Skipped"
            self.logger.info("Deflection Check skipped (SKIP_DEFLECTION=True)")

        if self.design_flag == True and self.design_flag2 == True and self.defl_check == True and self.shearchecks == True and self.momentchecks == True:
            self.design_status = True
        else:
            self.design_status = False
        self.final_format(design_dictionary)

        self.flange_warning_logged = False
        self.dimension_warning_logged = False

    def save_design(self, popup_summary):
        """
        Generate design report for plate girder
        """
        from ..report.latex_report import save_design
        popup_summary['plate_girder_object'] = self
        save_design(popup_summary)

    def generate_missing_fields_error_string(self, missing_fields_list):
        error_string = "Please provide input for the following fields:\n"
        for field in missing_fields_list:
            error_string += f"- {field}\n"
        return error_string

    def generate_first_particle(self,L, M, fy,is_thick_web, is_symmetric,k=67):
        D_empirical = L  / 25       # span in mm
        d_opt = ((M * k) / fy) ** (1/3)    # mm
        D_final = max(D_empirical, d_opt)

        bf_top = 0.3 * D_final
        bf_bot = 0.3 * D_final
        bf = 0.3 * D_final

        e = math.sqrt(250 / fy)
        tf_top = max(bf_top / 24 , bf_top / 8.4 * e )
        tf_bot = max(bf_bot / 24 , bf_bot / 8.4 * e)
        tf = max(bf / 24, bf_bot / 8.4 * e)


        d = D_final - 2 * tf
        if is_thick_web:
            tw = max(d / 200, d  /( 84 * e ), 8)
        else:
            tw = max( d / 200, d / ( 105 * e ), 8)


        c = 200     # min panel length (if used)
        t_stiff = 6 # min stiffener thickness (if used)
        # Order must match your variable list below
        varlst = []
        if is_symmetric:
            if is_thick_web:
                varlst += [tf,tw,bf,D_final]
            else:
                varlst += [tf,tw,bf,D_final,c,t_stiff]
        else:
            if is_thick_web:
                varlst  += [tf_top,tf_bot,tw,bf_top,bf_bot,D_final]
            else:
                varlst += [tf_top,tf_bot,tw,bf_top,bf_bot,D_final,c,t_stiff]
        print(varlst)
        return varlst

    # 2. Build the list of variables
    def build_variable_structure(self, is_thick_web=True, is_symmetric=True):
        variables = []
        if is_symmetric:
            # tf, tw, bf, D
            variables += ['tf', 'tw', 'bf', 'D']
        else:
            variables += ['tf_top', 'tf_bot', 'tw', 'bf_top', 'bf_bot', 'D']

        if not is_thick_web:
            variables += ['c', 't_stiff']

        return variables

    # 3. Create bounds array
    def get_bounds(self,variable_list):
        lower = [self.bounds_map[v][0] for v in variable_list]
        upper = [self.bounds_map[v][1] for v in variable_list]
        return (np.array(lower), np.array(upper))

    
    # 4. Assign a particle vector to your section object
    def assign_particle_to_section(self,particle, variable_list, section):
        for name, value in zip(variable_list, particle):
            setattr(section, name, value)
        
        # handle symmetric naming if needed
        print("Particle",particle)
        print("Variable list",variable_list)
        if 'tf' in variable_list:
            section.tf_top = section.tf_bot = section.tf
            section.bf_top     = section.bf_bot     = section.bf
        
        self.top_flange_thickness = section.tf_top
        self.bottom_flange_thickness = section.tf_bot
        self.web_thickness = section.tw
        self.top_flange_width = section.bf_top
        self.bottom_flange_width = section.bf_bot
        self.total_depth = section.D
        self.eff_depth = section.D - section.tf_top - section.tf_bot
        self.IntStiffnerwidth = min(self.top_flange_width,self.bottom_flange_width) - self.web_thickness/2 - 10
        self.end_stiffwidth = self.IntStiffnerwidth
        # Only update c and t_stiff if they were in the variable list (thin web case)
        if section.c is not None:
            self.c = section.c
        if section.t_stiff is not None:
            self.IntStiffThickness = section.t_stiff

    def _calc_particle_area(self, particle, variable_list):
        """
        Calculate cross-sectional area (in cm²) from particle position.
        Used for weight calculation in visualization.
        
        Args:
            particle: Particle position array
            variable_list: List of variable names corresponding to particle dimensions
            
        Returns:
            Cross-sectional area in cm²
        """
        # Extract dimensions from particle based on variable list
        var_dict = dict(zip(variable_list, particle))
        
        # Get dimensions, handling symmetric vs asymmetric cases
        if 'tf' in var_dict:
            tf_top = tf_bot = var_dict['tf']
            bf_top = bf_bot = var_dict.get('bf', 200)
        else:
            tf_top = var_dict.get('tf_top', 10)
            tf_bot = var_dict.get('tf_bot', 10)
            bf_top = var_dict.get('bf_top', 200)
            bf_bot = var_dict.get('bf_bot', 200)
        
        tw = var_dict.get('tw', 8)
        D = var_dict.get('D', 1000)
        
        # Web height
        d_web = D - tf_top - tf_bot
        
        # Area in mm²
        area_mm2 = (tf_top * bf_top) + (tf_bot * bf_bot) + (tw * d_web)
        
        # Convert to cm²
        area_cm2 = area_mm2 / 100
        
        return area_cm2


    def evaluate_particle_cost(self, particle, variable_list, design_dictionary, is_symmetric, is_thick_web):
        sec = Section()
        self.assign_particle_to_section(particle, variable_list, sec)
        # Only call optimized version for PSO iterations (design_check has side effects)
        max_ratio, slender_ok, thickness_ok = self.design_check_optimized_version(design_dictionary)

        area = ((self.top_flange_thickness * self.top_flange_width) +
                (self.bottom_flange_thickness * self.bottom_flange_width) +
                (self.web_thickness * (self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness)))
        volume = area * self.length  # mm³
        mass = volume * 7.85e-6  # kg
        P = 1e6  # penalty coefficient (tune as needed)
        penalty = 0.0

        # Section classification failure (slender sections not allowed)
        if not slender_ok:
            penalty += 2.0  # Heavy penalty for slender section
        
        # Web thickness check failure
        if not thickness_ok:
            penalty += 1.5  # Penalty for web thickness violation

        # Shear capacity (shear_ratio > 1.0 means failure)
        if self.shear_ratio > 1.0:
            penalty += (self.shear_ratio - 1.0)

        # Moment capacity (moment_ratio > 1.0 means failure)
        if self.moment_ratio > 1.0:
            penalty += (self.moment_ratio - 1.0)

        # Web buckling & crippling (shearchecks==False means any web failure)
        if not self.shearchecks:
            penalty += 1.0

        # Deflection serviceability
        if not self.defl_check:
            penalty += 1.0

        # --- DDCL Constraint Penalties for Thin Web / Stiffeners ---
        if not is_thick_web:
            # 1. Stiffener Spacing Limits (IS 800 Cl. 8.7.2.4)
            # 0.5d <= c <= 3d
            eff_d = self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness
            min_c = 0.5 * eff_d
            max_c = 3.0 * eff_d
            
            if self.c < min_c: 
                penalty += 1.0 + (min_c - self.c)/100.0  # Proportional penalty
            elif self.c > max_c:
                penalty += 1.0 + (self.c - max_c)/100.0

            # 2. Stiffener Thickness Limit (IS 800 Cl. 8.7.1.3)
            # t >= d/50
            min_t = eff_d / 50.0
            if self.IntStiffThickness < min_t:
                penalty += 1.0 + (min_t - self.IntStiffThickness) # Strong penalty

        # 5) Return penalized objective
        final_cost = mass + P * penalty
        if self.debug:
            print(f"[PSO] dims: D={self.total_depth}, tw={self.web_thickness}, bf={self.top_flange_width}, tf={self.top_flange_thickness}, c={ getattr(self, 'c', 'NA') } | Mass={mass:.2f}, Penalty={penalty:.4f} (S:{self.shear_ratio:.2f}, M:{self.moment_ratio:.2f}, B:{not self.shearchecks}, D:{not self.defl_check}), Cost={final_cost:.2e}")
        return final_cost

    def design_check_optimized_version(self,design_dictionary):
        self.design_flag = False
        self.design_flag2 = False
        self.shearflag1 = False
        self.shearflag2 = False
        self.shearflag3 = False
        self.shearchecks = False
        self.momentchecks = False
        self.defl_check = False
        self.long_check = False
        self.design_flag = self.section_classification(design_dictionary)
        if self.design_flag == False:
            print(f"[DEBUG] Slender Section Detected: D={self.total_depth}, tw={self.web_thickness}")
            pass
            # self.logger.error("slender section not allowed")
            
        else:
            # Ensure flange warning flag is initialized
            if not hasattr(self, 'flange_warning_logged'):
                self.flange_warning_logged = False
            if not hasattr(self, 'dimension_warning_logged'):
                self.dimension_warning_logged = False
            # Design efficiency check: warn if b/tf is too small (flanges too thick for their width)
            # NOTE: This is NOT an IS 800:2007 requirement. IS 800 Table 2 has MAXIMUM b/tf limits only.
            min_b_tf = 7.4 * self.epsilon
            b_tf_top = (self.top_flange_width - self.web_thickness) / (2 * self.top_flange_thickness)
            if b_tf_top < min_b_tf and not self.flange_warning_logged:
                self.logger.warning(f"Top flange b/tf ratio ({b_tf_top:.2f}) is below efficiency guideline ({min_b_tf:.2f}), consider using thinner flanges")
                self.flange_warning_logged = True
            
            b_tf_bot = (self.bottom_flange_width - self.web_thickness) / (2 * self.bottom_flange_thickness)
            if b_tf_bot < min_b_tf and not self.flange_warning_logged:
                self.logger.warning(f"Bottom flange b/tf ratio ({b_tf_bot:.2f}) is less than minimum ({min_b_tf:.2f}), flanges may be too thick")
                self.flange_warning_logged = True
            
            # Check that bottom flange dimensions are not less than top flange dimensions
            if self.bottom_flange_width < self.top_flange_width and not self.dimension_warning_logged:
                self.logger.warning(f"Bottom flange width ({self.bottom_flange_width:.2f} mm) is less than top flange width ({self.top_flange_width:.2f} mm)")
                self.dimension_warning_logged = True
            
            if self.bottom_flange_thickness < self.top_flange_thickness and not self.dimension_warning_logged:
                self.logger.warning(f"Bottom flange thickness ({self.bottom_flange_thickness:.2f} mm) is less than top flange thickness ({self.top_flange_thickness:.2f} mm)")
                self.dimension_warning_logged = True
            
            # self.beta_value(design_dictionary,self.section_class)

            # Calculate section properties needed for moment capacity checks
            # CRITICAL: Must recalculate for each particle in PSO optimization
            from ....utils.common.Unsymmetrical_Section_Properties import Unsymmetrical_I_Section_Properties
            self.plast_sec_mod_z = Unsymmetrical_I_Section_Properties.calc_PlasticModulusZ(
                self.total_depth, self.top_flange_width, self.bottom_flange_width,
                self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness,
                self.epsilon, debug=self.debug)
            self.elast_sec_mod_z = Unsymmetrical_I_Section_Properties.calc_ElasticModulusZz(
                self.total_depth, self.top_flange_width, self.bottom_flange_width,
                self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, debug=self.debug
            )

            if self.web_philosophy == 'Thick Web without ITS':
                print('THICK WEB')
                self.design_flag2 = min_web_thickness_thick_web(self.eff_depth,self.web_thickness,self.epsilon,"no_stiffener",0, debug=self.debug)
                
                if self.design_flag2 == True:
                    
                    #shear check - Correct argument order: (Fy, gamma_m0, D, tw, tf_top, tf_bot, shear_force)
                    is_safe, self.V_d, self.shear_ratio = shear_capacity_laterally_supported_thick_web(self.material.fy, self.gamma_m0, self.total_depth, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, self.load.shear_force)
                    if is_safe:
                        self.shearflag1 = True
                        # self.logger.info("Shear Check passed")
                        
                    else:
                        self.shearflag1 = False
                        # self.logger.error("Shear Check failed")

                    
                    #web buckling check
                    is_safe, self.V_cr = web_buckling_laterally_supported_thick_web(self.material.fy, self.gamma_m0, self.total_depth, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, self.material.modulus_of_elasticity, self.b1, self.load.shear_force, debug=self.debug)
                    if is_safe:
                        self.shearflag2 = True
                        # self.logger.info("Web Buckling Check passed")
                    else:
                        self.shearflag2 = False
                        # self.logger.error("Web Buckling Check failed")
                    
                    #web crippling check
                    web_height = self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness
                    is_safe, self.F_q = check_web_crippling(self.load.shear_force, self.b1, self.web_thickness, self.material.fy, web_height, self.gamma_m0, self.logger, debug=self.debug)
                    if is_safe:
                        self.shearflag3 = True  # Fixed from False to True
                        # self.logger.info("Web Crippling Check passed")
                    else:
                        self.shearflag3 = False
                        # self.logger.error("Web Crippling Check failed")
                    
                    if self.shearflag1 == True and self.shearflag2 == True and self.shearflag3 == True:
                        self.shearchecks = True
                    else:
                        self.shearchecks = False
                    
                    #support type supp or unsupp
                    if self.support_type == 'Major Laterally Supported':

                        #moment check supp
                        is_safe, self.Md, self.moment_ratio, self.V_d = moment_capacity_laterally_supported(self.load.shear_force,self.plast_sec_mod_z,self.elast_sec_mod_z,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.section_class, self.support_condition, self.load.moment)
                        if self.debug:
                            print(f"[DEBUG] Moment Check (PSO): Md={self.Md:.2e}, Ratio={self.moment_ratio:.4f}")
                        if is_safe:
                            self.momentchecks = True
                            # self.logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            # self.logger.error("Moment Check failed")
                    
                    else:  #unsupp

                        #moment check unspp
                        is_safe, self.Md, self.moment_ratio, self.V_d, self.M_cr, self.lambda_lt, self.phi_lt, self.X_lt, self.fbd_lt, self.It, self.Iw = moment_capacity_laterally_unsupported(self.material.modulus_of_elasticity,self.effective_length,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.loading_case,self.gamma_m0,self.material.fy,self.load.shear_force, self.warping, self.load.moment, self.plast_sec_mod_z, self.elast_sec_mod_z, self.section_class, self.alpha_lt)
                        if is_safe:
                            self.momentchecks = True
                            # self.logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            # self.logger.error("Moment Check failed")
                else:
                    # self.logger.error("Increase the web thickness")
                    pass

            else: #thin web condition
                self.shear_ratio = 0
                if self.long_Stiffner == 'Yes and 1 stiffener':
                    self.stiffener_type = "transverse_and_one_longitudinal_compression"
                elif self.long_Stiffner == 'Yes and 2 stiffeners':
                    self.stiffener_type = "transverse_and_two_longitudinal_neutral"
                else:
                    self.stiffener_type = "transverse_only"
                if self.stiffener_type != "transverse_only":
                    second_stiffener = False
                    if self.stiffener_type == "transverse_and_two_longitudinal_neutral":
                        second_stiffener = True
                    # Placeholder for longitudinal stiffener check
                    pass 
                
                if self.c == 'NA':
                    # Calculate c per IS 800:2007 when not provided
                    self.c = self.calculate_stiffener_spacing_IS800()
                else:
                    self.c = float(self.c)
                self.design_flag2 = min_web_thickness_thick_web(self.eff_depth,self.web_thickness,self.epsilon,self.stiffener_type,self.c, debug=self.debug)
                print('DESIGN FLAG2',self.design_flag2)
                if self.design_flag2 == True:

                    if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':
                        #shear check
                        is_safe, self.V_d, self.shear_ratio = shear_buckling_check_simple_postcritical(self.eff_depth, self.total_depth, self.top_flange_thickness, self.bottom_flange_thickness, self.web_thickness, self.load.shear_force, self.web_philosophy, self.material.modulus_of_elasticity, self.material.fy, self.load.shear_force, self.c)
                        if is_safe:
                            self.shearflag1 = True

                            # self.logger.info("Shear Check passed")
                        else:

                            result = end_panel_stiffener_calc(self.top_flange_width, self.bottom_flange_width,
                                                             self.web_thickness, self.end_stiffthickness,
                                                             self.material.fy, self.gamma_m0, self.eff_depth,
                                                             self.top_flange_thickness, self.total_depth,
                                                             self.effective_length, self.bottom_flange_thickness,
                                                             self.material.modulus_of_elasticity, self.epsilon, self.c, self.web_philosophy, self.load.moment, self.load.shear_force,
                                                             self.int_thickness_list, self.end_stiffwidth, self.end_stiffthickness, self.logger)
                            is_safe_end = result[0]
                            self.end_stiffwidth = result[1]
                            self.end_stiffthickness = result[2]
                            if is_safe_end:
                                self.shearflag1 = True
                            else:

                                self.shearflag1 = False
                               # self.logger.error("End Panel Stiffener Check failed")
                    
                        is_safe_int, self.V_cr, _, self.IntStiffnerwidth, _ = shear_buckling_check_intermediate_stiffener(self.eff_depth, self.web_thickness, self.c, self.epsilon, self.IntStiffThickness, self.IntStiffnerwidth, self.load.shear_force, self.gamma_m0, self.material.fy, self.material.modulus_of_elasticity, self.web_philosophy, self.lefactor, self.load.shear_force)
                        if is_safe_int:
                            self.shearflag2 = True

                            # self.logger.info("Shear Buckling Check passed").
                        else:

                            self.shearflag2 = False
                            # self.logger.error("Shear Buckling Check failed")
                    
                    else: #tension field

                        is_safe_tf, self.V_tf, self.shear_ratio, self.V_cr = shear_buckling_check_tension_field(self.eff_depth, self.total_depth, self.top_flange_thickness, self.bottom_flange_thickness, self.web_thickness, self.c, self.web_philosophy, self.material.modulus_of_elasticity, self.material.fy, self.load.shear_force, self.load.moment, self.top_flange_width, self.top_flange_thickness, self.bottom_flange_width, self.bottom_flange_thickness, self.gamma_m0)
                        if is_safe_tf:
                            self.shearflag1 = True
                            # self.logger.info("Shear Buckling Check passed")
                        else:
                            result_tf = tension_field_end_stiffener(self.eff_depth, self.web_thickness, self.material.fy,
                                                             self.load.shear_force, self.load.moment,
                                                             self.c, self.web_philosophy, self.material.modulus_of_elasticity,
                                                             self.top_flange_thickness, self.bottom_flange_thickness,
                                                             self.top_flange_width, self.bottom_flange_width,
                                                             self.gamma_m0, self.int_thickness_list, self.IntStiffnerwidth, self.IntStiffThickness, self.epsilon, self.lefactor)
                            is_safe_end_tf = result_tf[0]
                            self.end_stiffthickness = result_tf[5] if len(result_tf) > 5 else 0
                            if is_safe_end_tf:
                                self.shearflag1 = True
                            else:
                                self.shearflag1 = False
                                # self.logger.error("Tension Field Check failed, increase stiffener thickness")
                        is_safe_int_tf, self.V_tf, _, self.IntStiffnerwidth, _ = tension_field_intermediate_stiffener(self.eff_depth, self.web_thickness, self.c, self.epsilon, self.IntStiffThickness, self.IntStiffnerwidth, self.load.shear_force, self.gamma_m0, self.material.fy, self.material.modulus_of_elasticity, self.web_philosophy, self.lefactor, self.load.shear_force)
                        if is_safe_int_tf:
                            self.shearflag2 = True
                        else:
                            self.shearflag2 = False

                    if self.shearflag1 == True and self.shearflag2 == True:
                        self.shearchecks = True
                    else:
                        self.shearchecks = False

                    # support type supp or unsupp
                    if self.support_type == 'Major Laterally Supported':
                        #moment check supp
                        is_safe, self.Md, self.moment_ratio, self.V_d = moment_capacity_laterally_supported(self.load.shear_force,self.plast_sec_mod_z,self.elast_sec_mod_z,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.section_class, self.support_condition, self.load.moment)
                        if is_safe:
                            self.momentchecks = True

                            # self.logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False

                            # self.logger.error("Moment Check failed")
                    
                    else:  #unsupp

                        #moment check unspp
                        is_safe, self.Md, self.moment_ratio, self.V_d, self.M_cr, self.lambda_lt, self.phi_lt, self.X_lt, self.fbd_lt, self.It, self.Iw = moment_capacity_laterally_unsupported(self.material.modulus_of_elasticity,self.effective_length,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.loading_case,self.gamma_m0,self.material.fy,self.load.shear_force, self.warping, self.load.moment, self.plast_sec_mod_z, self.elast_sec_mod_z, self.section_class, self.alpha_lt)
                        if is_safe:
                            self.momentchecks = True

                            # self.logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False

                            # self.logger.error("Moment Check failed")

                else:
                    # self.logger.error("Increase the web thickness")
                    pass

        # Deflection checks
        if not SKIP_DEFLECTION:
            # Note: self.load.moment is in N·mm, but evaluate_deflection_kNm_mm expects kN·m
            moment_kNm = self.load.moment / 1e6  # Convert N·mm to kN·m
            is_safe, self.deflection_ratio, delta, allowable = evaluate_deflection_kNm_mm(moment_kNm, self.length, self.material.modulus_of_elasticity, self.loading_case, self.deflection_criteria, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
            self.calculated_deflection = round(delta, 2)
            self.deflection_limit = round(allowable, 2)
            if is_safe:
                self.defl_check = True
            else:
                self.defl_check = False
        else:
            self.defl_check = True
            self.deflection_ratio = 0.0
            self.calculated_deflection = "Skipped"
            self.deflection_limit = "Skipped"

        #in pso check for self.moment_checks and self.shearchecks

        #for customized
        print(f"RATIOS  moment {self.moment_ratio} shear {self.shear_ratio} deflection {self.deflection_ratio}")
        return max(self.moment_ratio,self.shear_ratio,self.deflection_ratio),self.design_flag,self.design_flag2

    def optimized_method(self, design_dictionary, is_thick_web, is_symmetric, viz_callback=None):
        """
        Perform PSO optimization to find optimal plate girder dimensions.
        
        Args:
            design_dictionary: Design input dictionary
            is_thick_web: True if thick web design
            is_symmetric: True if symmetric flanges
            viz_callback: Optional callback(depth, ur, weight, iteration, particle_idx)
                         for real-time visualization
        """
        variable_list = self.build_variable_structure(is_thick_web, is_symmetric)
        lb, ub = self.get_bounds(variable_list)
        
        # Get index of 'D' (depth) in variable list for visualization
        depth_idx = variable_list.index('D') if 'D' in variable_list else -1
        
        # Create PSO progress callback for visualization
        def pso_progress_callback(iteration, particle_idx, position, cost):
            if viz_callback and depth_idx >= 0:
                # Extract depth from particle position
                depth = position[depth_idx]
                
                # Get current utilization ratio - use max of all constraint ratios
                # This matches how result_UR is calculated in final_format()
                moment_r = getattr(self, 'moment_ratio', 0) or 0
                shear_r = getattr(self, 'shear_ratio', 0) or 0
                defl_r = getattr(self, 'deflection_ratio', 0) or 0
                ur = max(moment_r, shear_r, defl_r)
                
                # Calculate weight: Area (cm²→m²) × 7850 kg/m³ × Length (mm→m)
                area_cm2 = self._calc_particle_area(position, variable_list)
                area_m2 = area_cm2 / 10000  # cm² to m²
                length_m = self.length / 1000  # mm to m
                weight_kg = area_m2 * 7850 * length_m
                
                # Emit to visualization
                # Pass full position, variable names, and BOUNDS for accurate Parallel Coordinates
                viz_callback(depth, ur, weight_kg, iteration, particle_idx, list(position), variable_list, list(lb), list(ub))
        
        if self.use_intelligent_pso:
            # Prepare discrete lists for Intelligent PSO
            discrete_map = {}
            for i, var in enumerate(variable_list):
                if var in ['tf', 'tf_top', 'tf_bot']:
                    discrete_map[i] = [float(x) for x in self.top_flange_thickness_list] # Assuming top/bot lists are same or merged
                elif var == 'tw':
                    discrete_map[i] = [float(x) for x in self.web_thickness_list]
                elif var == 't_stiff':
                    discrete_map[i] = [float(x) for x in self.int_thickness_list] # Assuming stiff lists are available
                # Dimensions like Depth (D) and Width (bf) could be continuous or step-based.
                # For now, let's keep them continuous or snapped to 5mm?
                # User did not specify standard lists for D/B, only thicknesses usually matter heavily for stock.
            
            optimizer = IntelligentPSO(
                n_particles=50,
                dimensions=len(variable_list),
                options={'c1': 1.5, 'c2': 1.5, 'w': 0.4, 'debug': self.debug},
                bounds=(lb, ub),
                discrete_lists=discrete_map
            )
        else:
            optimizer = GlobalBestPSO(
                n_particles=50,
                dimensions=len(variable_list),
                options={'c1': 1.5, 'c2': 1.5, 'w': 0.4},
                bounds=(lb, ub)
            )
        
        fp = self.generate_first_particle(float(self.length), float(self.load.moment), float(self.material.fy),is_thick_web,is_symmetric)
        
        # Debug: Log PSO input parameters
        self.logger.info(f"PSO Input - Length: {self.length} mm, Moment: {self.load.moment} N-mm, Fy: {self.material.fy} MPa")
        self.logger.info(f"PSO Bounds - Lower: {lb}, Upper: {ub}")
        self.logger.info(f"PSO First Particle (before clip): {fp}")
        
        # Inject knowledge (first particle)
        if self.use_intelligent_pso:
             optimizer.X[0] = np.clip(fp, lb, ub)
             self.logger.info(f"PSO First Particle (after clip): {optimizer.X[0]}")
        else:
             optimizer.swarm.position[0] = np.clip(fp, lb, ub)
             self.logger.info(f"PSO First Particle (after clip): {optimizer.swarm.position[0]}")


        best_cost, best_pos = optimizer.optimize(
            objective_func=lambda particle: self.objective_function(particle, variable_list, design_dictionary, is_symmetric, is_thick_web),
            iters=100,
            debug=self.debug,
            progress_callback=pso_progress_callback
        )

        self.logger.info("PSO calculation successfully completed")
        if self.debug:
            print(f"\n[PSO RESULT] Best Cost (Mass + Penalty): {best_cost:.2f}")
        
        best_design_var = dict(zip(variable_list, best_pos))
        
        if self.debug:
            print(f"[PSO RESULT] Best Dimensions: {best_design_var}")
        
        if is_symmetric:
            self.bottom_flange_thickness = self.top_flange_thickness = float(best_design_var['tf'])
            for i in self.bottom_flange_thickness_list:
                if float(i) > self.bottom_flange_thickness:
                    self.bottom_flange_thickness = float(i)
                    self.top_flange_thickness = float(i)
                    break
            self.web_thickness = float(best_design_var['tw'])
            for i in self.web_thickness_list:
                if float(i) > self.web_thickness:
                    self.web_thickness = float(i)
                    break

            self.top_flange_width = self.bottom_flange_width = round(float(best_design_var['bf']),0)
            self.top_flange_width = self.bottom_flange_width = ceil_to_nearest(self.top_flange_width,25)
            self.total_depth = round(float(best_design_var['D']),0)
            self.total_depth =  ceil_to_nearest(self.total_depth,25)


        else:
            self.bottom_flange_thickness = float(best_design_var['tf_bot'])
            for i in self.bottom_flange_thickness_list:
                if float(i) > self.bottom_flange_thickness:
                    self.bottom_flange_thickness = float(i)
                    break
            self.top_flange_thickness = float(best_design_var['tf_top'])
            for i in self.top_flange_thickness_list:
                if float(i) > self.top_flange_thickness:
                    self.top_flange_thickness = float(i)
                    break
            self.web_thickness = float(best_design_var['tw'])
            for i in self.web_thickness_list:
                if float(i) > self.web_thickness:
                    self.web_thickness = float(i)
                    break

            self.bottom_flange_width = round(float(best_design_var['bf_bot']),0)
            self.bottom_flange_width = ceil_to_nearest(self.bottom_flange_width,25)
            self.top_flange_width = round(float(best_design_var['bf_top']),0)
            self.top_flange_width = ceil_to_nearest(self.top_flange_width,25)
            self.total_depth = round(float(best_design_var['D']),0)
            self.total_depth =  ceil_to_nearest(self.total_depth,25)
            
        self.eff_depth = self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness

        if not is_thick_web:
            # Enforce IS 800 Cl. 8.7.1.3: t_stiff >= d/50
            min_t_stiff = self.eff_depth / 50.0
            
            self.IntStiffThickness = float(best_design_var['t_stiff'])
            
            # Start search from the discrete list closest to optim result or min_t_stiff
            start_thickness = max(self.IntStiffThickness, min_t_stiff)
            
            found_thickness = False
            for i in self.int_thickness_list:
                if float(i) >= start_thickness:  # strictly >= min_t_stiff
                    self.IntStiffThickness = float(i)
                    found_thickness = True
                    break
            
            # If no thickness in list satisfies d/50, take the largest available
            if not found_thickness and len(self.int_thickness_list) > 0:
                 self.IntStiffThickness = float(self.int_thickness_list[-1])

            # Enforce IS 800 Cl. 8.7.2.4: 0.5d <= c <= 3d
            min_c = 0.5 * self.eff_depth
            max_c = 3.0 * self.eff_depth
            
            raw_c = round(float(best_design_var['c']), 0)
            
            # Clamp c to valid range
            self.c = max(min_c, min(raw_c, max_c))
            self.c = ceil_to_nearest(self.c, 25)
        
        self.logger.info(f"Optimized values : Flange width top and bottom {self.top_flange_width} {self.bottom_flange_width} flange thickness top and bottom {self.top_flange_thickness} { self.bottom_flange_thickness} web_thickness  {self.web_thickness} total depth { self.total_depth} C value {self.c} thickness stiffener { self.IntStiffThickness}")
        
        # Print Plastic Modulus for PSO optimization
        from ....utils.common.Unsymmetrical_Section_Properties import Unsymmetrical_I_Section_Properties
        pso_plastic_modulus = Unsymmetrical_I_Section_Properties.calc_PlasticModulusZ(
            self.total_depth, self.top_flange_width, self.bottom_flange_width,
            self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness,
            self.epsilon, debug=self.debug)
        pso_elastic_modulus = Unsymmetrical_I_Section_Properties.calc_ElasticModulusZz(
            self.total_depth, self.top_flange_width, self.bottom_flange_width,
            self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness, debug=self.debug
        )
        if self.debug:
            print(f"\n========== PSO OPTIMIZED SECTION PROPERTIES ==========")
            print(f"  Total Depth (D): {self.total_depth:.2f} mm")
            print(f"  Web Thickness (tw): {self.web_thickness:.2f} mm")
            print(f"  Top Flange Width: {self.top_flange_width:.2f} mm")
            print(f"  Top Flange Thickness: {self.top_flange_thickness:.2f} mm")
            print(f"  Bottom Flange Width: {self.bottom_flange_width:.2f} mm")
            print(f"  Bottom Flange Thickness: {self.bottom_flange_thickness:.2f} mm")
            print(f"  Stiffener Spacing (c): {self.c} mm")
            print(f"  Intermediate Stiffener Thickness: {self.IntStiffThickness} mm")
            print(f"  ---")
            print(f"  Plastic Modulus (Zp): {pso_plastic_modulus:.2f} mm³")
            print(f"  Elastic Modulus (Ze): {pso_elastic_modulus:.2f} mm³")
            print(f"======================================================\n")

        self.design_check(design_dictionary)

    # 5. Objective function
    def objective_function(self, particle, variable_list, design_dictionary, is_symmetric, is_thick_web):
        """
        particle: 1D array of design variables for a single particle
        returns: scalar cost
        """
        cost = self.evaluate_particle_cost(particle, variable_list, design_dictionary, is_symmetric, is_thick_web)
        return cost
    
    def final_format(self,design_dictionary):
        
        # Format: "D x tw x Bf_bot x tf_bot x Bf_top x tf_top" with dimension labels for clarity
        self.result_designation = f"PG {int(self.total_depth)}x{int(self.web_thickness)}x{int(self.bottom_flange_width)}x{int(self.bottom_flange_thickness)}x{int(self.top_flange_width)}x{int(self.top_flange_thickness)}"
        if self.moment_ratio == None:
            self.moment_ratio = 0
        if self.shear_ratio == None:
            self.shear_ratio = 0
        
        self.result_UR = max(self.moment_ratio,self.shear_ratio, self.deflection_ratio)
        self.section_classification_val = self.section_class
        
        # Fix: Beta value should be 1.0 for Plastic/Compact sections
        if self.beta_b_lt is None or self.beta_b_lt == 0:
            if self.section_class == KEY_Plastic or self.section_class == KEY_Compact:
                self.beta_b_lt = 1.0
            elif self.section_class == KEY_SemiCompact:
                # Assuming Ze and Zp are available
                if hasattr(self, 'elast_sec_mod_z') and hasattr(self, 'plast_sec_mod_z') and self.plast_sec_mod_z > 0:
                    self.beta_b_lt = self.elast_sec_mod_z / self.plast_sec_mod_z
                else:
                    self.beta_b_lt = 1.0 # Fallback
            else:
                 self.beta_b_lt = 1.0 # Fallback
                 
        self.betab = round(self.beta_b_lt,2)
        
        # Area already divided by 100 in logic, just need to ensure unit label in Common.py is correct (cm^2)
        # Note: Unsymmetrical_I_Section_Properties.calc_area returns mm^2. Division by 100 gives cm^2? No, mm^2 to cm^2 is /100.
        self.effectivearea = round(Unsymmetrical_I_Section_Properties.calc_area(self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)/100, 2)
        
        if self.Md == None:
            self.Md = 0

        if self.M_cr == None:
            self.M_cr = 0
        if self.V_cr == None:
            self.V_cr = 0
        if self.It == None:
            self.It = 0
        if self.Iw == None:
            self.Iw = 0

        if self.shear_type == 'Low':
            self.design_moment = round(self.Md/1000000,1)
        else:
            self.design_moment = round(self.Md/1000000,1)
        
        self.critical_moment = 'N/A'
        self.torsion_cnst = 'N/A'
        self.warping_cnst = 'N/A'
        if self.support_type == 'Major Laterally Unsupported' or self.support_type == 'Minor Laterally Unsupported':
            self.critical_moment = round(self.M_cr/1000000,1)   
            self.torsion_cnst = round(self.It/10000,1)
            self.warping_cnst = round(self.Iw/1000000,1)
            
        # Stiffener Logic Fixes
        if self.web_philosophy == 'Thick Web without ITS':
             self.intstiffener_thk = "N/A"
             self.longstiffener_thk = "N/A"
             self.intstiffener_spacing = "N/A"
             self.end_panel_stiffener_thickness = "N/A"
             self.x1 = "N/A"
             self.x2 = "N/A"
        else:
             self.intstiffener_thk = self.IntStiffThickness
             self.longstiffener_thk = self.LongStiffThickness
             self.intstiffener_spacing = self.c
             
             # End panel stiffener logic
             if self.end_panel_stiffener_thickness is None or self.end_panel_stiffener_thickness == 0:
                 if self.end_stiffthickness == 0:
                      self.end_panel_stiffener_thickness = self.IntStiffThickness # Fallback to min
                 else:
                      self.end_panel_stiffener_thickness = self.end_stiffthickness
             else:
                 pass # already set correctly
             
             if isinstance(self.end_panel_stiffener_thickness, (int, float)):
                 self.end_panel_stiffener_thickness = round(self.end_panel_stiffener_thickness, 2)

        # Longitudinal Stiffener Position Calculation per IS 800:2007 Cl. 8.7.13 / DDCL 1.5.3
        # Automatically determine if stiffeners are required based on d/tw ratio limits
        num_long_required, x1_auto, x2_auto, long_reason = check_longitudinal_stiffener_required(
            self.eff_depth, self.web_thickness, self.c, self.epsilon, debug=self.debug
        )
        
        # Log the automatic check result
        self.logger.info(f"Longitudinal Stiffener Check: {long_reason}")
        
        # Get user preference
        user_num = 0
        if self.long_Stiffner == 'Yes and 1 stiffener':
            user_num = 1
        elif self.long_Stiffner == 'Yes and 2 stiffeners':
            user_num = 2
        
        # Respect user preference, but warn if codal requirements differ
        if user_num == 0 and num_long_required > 0:
            self.logger.warning(f"User selected 'No' for longitudinal stiffener, but IS 800:2007 Cl. 8.7.13 requires {num_long_required} stiffener(s) for d/tw = {self.eff_depth/self.web_thickness:.1f}")
            self.longstiffener_no = "Not Required"
            self.longstiffener_thk = "Not Required"
            self.x1 = "Not Required"
            self.x2 = "Not Required"
        elif user_num == 0 and num_long_required == 0:
            # User selected No and code also says not required
            self.logger.info("Longitudinal stiffener not required per IS 800:2007 Cl. 8.7.13")
            self.longstiffener_no = "Not Required"
            self.longstiffener_thk = "Not Required"
            self.x1 = "Not Required"
            self.x2 = "Not Required"
        elif user_num >= 1:
            # User explicitly requested stiffeners
            self.longstiffener_no = user_num
            # First stiffener at 0.2d from compression flange per Cl. 8.7.13
            self.x1 = x1_auto if x1_auto is not None else round(0.2 * self.eff_depth, 2)
            if user_num >= 2:
                # Second stiffener at neutral axis (0.5d) per Cl. 8.7.13
                self.x2 = x2_auto if x2_auto is not None else round(0.5 * self.eff_depth, 2)
                self.logger.info(f"Longitudinal stiffeners provided: x1={self.x1}mm (0.2d), x2={self.x2}mm (0.5d)")
            else:
                self.x2 = "Not Required"
                self.logger.info(f"Longitudinal stiffener provided: x1={self.x1}mm (0.2d from compression flange)")
             
        # Redundant safety for calculated_deflection in case missed
        if not hasattr(self, 'calculated_deflection'):
             self.calculated_deflection = "Skipped"
        if not hasattr(self, 'deflection_limit'):
             self.deflection_limit = "Skipped"

        self.atop= 0
        self.abot= 0
        self.weld_stiff= None
        self.atop, self.abot= design_welds_with_strength_web_to_flange(self.load.shear_force, self.top_flange_width, self.top_flange_thickness, self.bottom_flange_width, self.bottom_flange_thickness, self.web_thickness, self.eff_depth, [self.material.fu], debug=self.debug)
        self.weld_stiff = weld_for_end_stiffener(self.end_stiffthickness if self.end_stiffthickness > 0 else self.IntStiffThickness, self.end_stiffwidth, self.load.shear_force, self.V_d, self.total_depth, self.top_flange_thickness, self.bottom_flange_thickness, self.web_thickness, [self.material.fu])
        