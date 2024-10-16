"""

@Author:    Danish Ansari - Osdag Team, IIT Bombay [(P) danishdyp@gmail.com / danishansari@iitb.ac.in]

@Module - Base Plate Connection
           - Pinned Base Plate (welded and bolted) [Axial + Shear]
           - Gusseted Base Plate [Moment (major and minor axis) + Axial + Shear]
           - Base Plate for hollow sections [Moment (major and minor axis) + Axial + Shear]


@Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) IS 2062: 2011, Hot rolled medium and high tensile structural steel - specification
               4) IS 5624: 1993, Foundation bolts
               5) IS 456: 2000, Plain and reinforced concrete - code of practice
               6) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               7) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

     other     8)  Column Bases - Omer Blodgett (chapter 3)
  references   9) AISC Design Guide 1 - Base Plate and Anchor Rod Design

"""

# Importing modules from the project directory

from design_type.connection.moment_connection import MomentConnection
from utils.common.is800_2007 import IS800_2007
from utils.common.other_standards import IS_5624_1993
from utils.common.component import *
from utils.common.material import *
from utils.common.common_calculation import *
from Common import *
from utils.common.load import Load
from utils.common.other_standards import *
from design_report.reportGenerator import save_html
from Report_functions import *
from design_report.reportGenerator_latex import CreateLatex

import logging


class BasePlateConnection(MomentConnection, IS800_2007, IS_5624_1993, IS1367_Part3_2002, Column):
    """
    Perform stress analyses --> design base plate and anchor bolt--> provide connection detailing.

    Attributes:
                connectivity (str): type of base plate connection (pinned - welded, pinned - bolted,
                                    gusseted, hollow section).
                end_condition (str): assume end condition based on base plate type.
                    Assumption(s):
                                1) End condition is 'Pinned' for welded and bolted base plate.
                                2) End condition is 'Fixed' for gusseted and hollow section type base plate.

                column_section (str): column section [Ref: IS 808: 1989, and it's subsequent revision(s),
                                any new section data added by the user using the 'add section' feature from Osdag GUI.
                material (str): material grade of the column section [Ref: IS 2062: 2011, table 2].

                load_axial (float): Axial compressive load (concentric to column axis).
                load_shear (float): Shear/horizontal load.
                load_moment_major (float): Bending moment acting along the major (z-z) axis of the column.
                load_moment_minor (float): Bending moment acting along the minor (y-y) axis of the column.

                anchor_dia_out (str): diameter of the anchor bolt [Ref: IS 5624: 1993, page 5].
                anchor_type (str): type of the anchor bolt [Ref: IS 5624: 1993, Annex A, clause 4].

                footing_grade (str): grade of footing material (concrete) [Ref: IS 456: 2000, table 2].

                dp_column_designation (str): designation of the column as per IS 808.
                dp_column_type (str): type of manufacturing of the coulmn section (rolled, built-up, welded etc.).
                dp_column_source (str): source of the database of the column section.
                                        [Osdag/ResourceFiles/Database/Intg_osdag.sqite].
                dp_column_material (str): material grade of the column section [Ref: IS 2062: 2011].
                dp_column_fu (float): ultimate strength of the column section (default if not overwritten).
                dp_column_fy (float): yield strength of the column section (default if not overwritten).

                dp_bp_material (str): material grade of the base plate [Ref: IS 2062: 2011].
                dp_bp_fu (float): ultimate strength of the base plate (default if not overwritten).
                dp_bp_fy (float): yield strength of the base plate (default if not overwritten).
                    Assumption: The ultimate and yield strength values of base plare are assumed to be same as the
                                parent (column) material unless and untill overwritten in the design preferences,
                                with suitable validation.

                dp_anchor_designation_out (str): designation of the anchor bolt as per IS 5624: 1993, clause 5.
                dp_anchor_type_out (str): type of the anchor bolt [Ref: IS 5624: 1993, Annex A, clause 4].
                dp_anchor_hole_out (str): type of hole 'Standard' or 'Over-sized'.
                dp_anchor_fu_overwrite_out (float): ultimate strength of the anchor bolt corresponding to its grade.
                dp_anchor_friction (float): coefficient of friction between the anchor bolt and the footing material.

                dp_weld_fab (str): type of weld fabrication, 'Shop Weld' or 'Field Weld'.
                dp_weld_fu_overwrite (float): ultimate strength of the weld material.

                dp_detail_edge_type (str): type of edge preparation, 'a - hand flame cut' or 'b - Machine flame cut'.
                dp_detail_is_corrosive (str): is environment corrosive, 'Yes' or 'No'.

                dp_design_method (str): design philosophy used 'Limit State Design'.
                dp_bp_method (str): analysis method used for base plate 'Effective Area Method'

                gamma_m0 (float): partial safety factor for material - resistance governed by yielding or buckling.
                gamma_m1 (float): partial safety factor for material - resistance governed by ultimate stress.
                gamma_mb (float): partial safety factor for material - resistance of connection - bolts.
                gamma_mw (float): partial safety factor for material - resistance of connection - weld.

                bearing_strength_concrete (float)

    """

    def __init__(self):
        """Initialize all attributes"""
        super(BasePlateConnection, self).__init__()

        # attributes for input dock UI
        self.connectivity = ""
        self.end_condition = ""
        self.column_section = ""
        self.material = ""

        self.load_axial_compression = 0.0
        self.load_axial_input = 0.0
        self.load_axial_tension = 0.0
        # self.load_shear = 0.0
        self.load_shear_major = 0.0
        self.load_shear_minor = 0.0
        self.load_moment_major = 0.0
        self.column_axial_capacity = 0.0
        self.column_shear_capacity = 0.0
        self.epsilon_col = 0.0
        self.col_classification = ''
        self.beta_b_z = 1
        self.beta_b_y = 1
        self.M_dz = 0.0
        self.M_dy = 0.0
        self.IR_axial = 0.0
        self.IR_moment = 0.0
        self.sum_IR = 0.0
        self.moment_capacity_column_major = 0.0
        self.moment_capacity_column_minor = 0.0
        self.load_moment_major_report = 0.0
        self.load_moment_minor = 0.0
        self.load_moment_minor_report = 0.0

        self.shear_resistance = 0.0
        self.shear_key_along_ColDepth = 'No'
        self.shear_key_along_ColWidth = 'No'
        self.weld_size_shear_key = 0
        self.shear_key_stress_ColDepth = 'N/A'
        self.shear_key_stress_ColWidth = 'N/A'
        self.plate_thk = 0.0
        self.plate_thk_provided = 0.0
        self.plate_moment_capacity = 0.0

        self.shear_key_along_ColDepth = 'No'
        self.shear_key_depth_ColDepth = 0.0
        self.shear_key_w_1 = 0.0
        self.shear_key_moment_1 = 0.0
        self.fy_key_1 = 0.0
        self.moment_capacity_key1 = 0.0
        self.shear_key_thk_1 = 0.0
        self.shear_key_w_2 = 0.0
        self.shear_key_moment_2 = 0.0
        self.fy_key_2 = 0.0
        self.moment_capacity_key2 = 0.0
        self.shear_key_thk_2 = 0.0
        self.shear_key_design_status = False

        self.shear_key_along_ColWidth = 'No'
        self.shear_key_depth_ColWidth = 0.0

        self.anchor_dia_list_out = []
        self.anchor_dia_list_in = []
        self.anchor_dia_out = []
        self.anchor_dia_list = []
        self.anchor_type = ""
        self.anchor_grade_list_out = []
        self.anchor_grade_out = ''
        self.anchor_fu_fy_outside_flange = []
        self.anchor_grade_list_in = []
        self.anchor_grade_in = ''
        self.anchor_fu_fy_inside_flange = []

        self.footing_grade = 0.0

        # attributes for design preferences
        self.dp_column_designation = ""  # dp for column
        self.dp_column_type = ""
        self.dp_column_source = ""
        self.dp_column_material = ""
        self.dp_column_fu = 0.0
        self.dp_column_fy = 0.0
        self.stiffener_fy = 0.0
        self.stiffener_fy_along_flange = 0.0
        self.stiffener_fy_along_web = 0.0
        self.stiffener_fy_across_web = 0.0

        self.dp_bp_material = ""  # dp for base plate
        self.dp_bp_fu = 0.0
        self.dp_bp_fy = 0.0
        self.dp_stif_key_material = ''

        self.dp_anchor_designation_out = ""  # dp for anchor bolt
        self.dp_anchor_type_out = ""
        self.dp_anchor_galv_out = "Yes"
        self.dp_anchor_hole_out = "Over-sized"
        self.dp_anchor_length_out = 0
        self.dp_anchor_fu_overwrite_out = 0.0
        self.dp_anchor_friction = 0.0

        self.anchor_dia_in = []
        self.dp_anchor_designation_in = ""
        self.dp_anchor_type_in = ""
        self.dp_anchor_galv_in = "Yes"
        self.dp_anchor_hole_in = "Over-sized"
        self.dp_anchor_length_in = 0.0
        self.dp_anchor_fu_overwrite_in = 0.0

        self.dp_weld_fab = "Shop Weld"  # dp for weld
        self.dp_weld_fu_overwrite = 0.0

        self.dp_detail_edge_type = "b - Machine flame cut"  # dp for detailing
        self.dp_detail_is_corrosive = "Yes"

        self.dp_design_method = "Limit State Design"  # dp for design
        self.dp_bp_method = "Effective Area Method"

        # other attributes
        self.gamma_m0 = 0.0
        self.gamma_m1 = 0.0
        self.gamma_mb = 0.0
        self.gamma_mw = 0.0

        # self.column_properties = Column(designation=self.dp_column_designation, material_grade=self.dp_column_material)
        self.column_D = 0.0
        self.column_bf = 0.0
        self.column_tf = 0.0
        self.column_tw = 0.0
        self.column_r1 = 0.0
        self.column_r2 = 0.0
        self.column_t = 0.0
        self.column_area = 0.0

        self.bearing_strength_concrete = 0.0
        self.w = 0.0
        self.min_area_req = 0.0
        self.effective_bearing_area = 0.0
        self.projection = 0.0
        self.projection_dr = 0.0
        self.standard_plate_thk = []
        self.neglect_anchor_dia = []
        self.anchor_bolt = ''
        self.anchor_dia_provided_outside_flange = 'M20'
        self.anchor_dia_provided_inside_flange = []
        self.grout_thk = 50
        self.plate_washer_details = {}
        self.plate_washer_thk = 1
        self.nut_thk = 1
        self.anchor_length_min_out = 0.001
        self.anchor_length_max_out = 0.001
        self.anchor_length_min_in = 0.001
        self.anchor_length_max_in = 0.001
        self.plate_washer_details_out = {}
        self.plate_washer_dim_out = {}
        self.plate_washer_details_in = {}
        self.nut_thk_out = 0.001
        self.nut_thk_in = 0.001
        self.plate_washer_thk_out = 0.001
        self.plate_washer_thk_in = 0.001
        self.plate_washer_inner_dia_out = 0.001
        self.plate_washer_inner_dia_in = 0.001
        self.plate_washer_dim_out = 0.001
        self.plate_washer_dim_in = 0.001
        self.anchor_len_below_footing_out = 0.001
        self.anchor_len_below_footing_in = 0.001
        self.anchor_len_above_footing_out = 0.001
        self.anchor_len_above_footing_in = 0.001
        self.anchor_length_provided_out = 0.001
        self.anchor_length_provided_out_report = 0.001
        self.anchor_length_provided_in = 0.001
        self.anchor_length_provided_in_report = 0.001
        self.anchor_length_min = 1
        self.anchor_length_max = 1
        self.anchor_length_provided = 1
        self.anchor_len_below_footing = 1
        self.anchor_len_above_footing = 1
        self.anchors_outside_flange = 4
        self.anchors_inside_flange = 0
        self.anchor_nos_provided = self.anchors_outside_flange + self.anchors_inside_flange
        self.anchor_hole_dia_out = 0.0
        self.anchor_hole_dia_in = 0.0
        self.bp_length_min = 0.0
        self.bp_width_min = 0.0
        self.width_min_req = 0.0
        self.bp_length_provided = 0.0
        self.bp_width_provided = 0.0
        self.end_distance_out = 0.0
        self.edge_distance_out = self.end_distance_out
        self.end_distance_in = 0.0
        self.edge_distance_in = self.end_distance_in
        self.pitch_distance_in = 0.0
        self.gauge_distance_in = self.pitch_distance_in
        self.end_distance_max = 0.0
        self.edge_distance_out = 0.0
        self.edge_distance_max = 0.0
        self.pitch_distance_out = 0.0
        self.gauge_distance_out = 0.0
        self.bp_area_provided = 0.0

        self.shear_capacity_anchor = 0.0
        self.bearing_capacity_anchor = 0.0
        self.anchor_capacity = 0.0
        self.v_sb = 0.0
        self.v_db = 0.0
        self.t_b = 0.0
        self.t_db = 0.0
        self.combined_capacity_anchor = 0.0

        self.moment_bp_case = ''

        self.length_available_total = 0.0
        self.effective_length_flange = 0.0
        self.total_eff_len_available = 0.0
        self.effective_length_web = 0.0
        self.load_axial_flange = 0.0
        self.load_axial_web = 0.0
        self.strength_unit_len = 0.0
        self.weld_size = 0.0
        self.weld_fu = 0.0
        self.weld_size_flange_max = 0.0
        self.weld_size_web_max = 0.0
        self.weld_size_hollow = 0.0

        self.weld_len_flange = 0.0
        self.weld_len_web = 0.0
        self.weld_length = 0.0
        self.weld_bp_groove = 'No'
        self.weld_size_bp = 0.0
        self.weld_size_continuity_plate = 0.0

        self.weld_size_flange = 0.0
        self.weld_size_web = 0.0
        self.gusset_along_flange = 'No'
        self.gusset_along_web = 'No'
        self.gusset_plate_length = 0.0
        self.stiffener_plate_length = 0.0
        self.total_eff_len_gusset_available = 0.0
        self.gusset_outstand_length = 0.0
        self.stiffener_outstand_length = 0.0

        self.epsilon = 1
        self.epsilon_st_along_flange = 1
        self.epsilon_st_along_web = 1
        self.epsilon_st_across_web = 1
        self.gusset_plate_thick = 0.0
        self.stiffener_plate_thick = 0.0
        self.gusset_plate_height = 0.0
        self.stiffener_plate_height = 0.0
        self.stiffener_plt_len_along_flange = 0.0
        self.stiffener_plt_len_along_web = 0.0
        self.stiffener_plt_len_across_web = 0.0

        self.thk_req_stiffener_along_flange = 0.0
        self.thk_req_stiffener_along_web = 0.0
        self.thk_req_stiffener_across_web = 0.0
        self.stiffener_plt_thick_along_flange = 0.0
        self.stiffener_plt_thick_along_web = 0.0
        self.stiffener_plt_thick_across_web = 0.0
        self.stiffener_plt_height_along_flange = 0.0
        self.stiffener_plt_height_along_web = 0.0
        self.stiffener_plt_height_across_web = 0.0

        self.stiffener_along_flange = ''
        self.stiffener_along_web = ''
        self.stiffener_across_web = ''
        self.eff_stiffener_plt_len_along_flange = 0.0
        self.eff_stiffener_plt_len_along_web = 0.0

        self.stiffener_plt_thick_btwn_D_1 = 0.0
        self.stiffener_plt_thick_btwn_D_2 = 0.0
        self.stiffener_plt_thick_btwn_D = 0.0
        self.stiffener_plt_len_btwn_D_out = 0.0
        self.stiffener_plt_len_btwn_D_in = 0.0
        self.notch_stiffener_inside_flange = 0.0
        self.stiffener_plt_height_btwn_D = 0.0

        self.stiffener_along_D = ''
        self.stiffener_along_B = ''
        self.stiffener_plt_len_along_D = 0
        self.stiffener_plt_len_along_B = 0.0
        self.stiffener_plt_len_across_D = 0.0
        self.stiffener_plt_thk_min = 0.0
        self.stiffener_plt_thk = 0.0
        self.stiffener_plt_height = 0.0
        self.stiffener_nos = 0
        self.weld_length_stiffener_plt = 0.0
        self.weld_size_stiffener_plt = 0.0

        self.shear_on_gusset = 0.0
        self.moment_on_gusset = 0.0
        self.shear_capacity_gusset = 0.0
        self.z_e_gusset = 0.0
        self.moment_capacity_gusset = 0.0

        self.shear_on_stiffener_along_flange = 0.0
        self.shear_capa_stiffener_along_flange = 0.0
        self.moment_on_stiffener_along_flange = 0.0
        self.moment_capa_stiffener_along_flange = 0.0
        self.z_e_stiffener_along_flange = 0.0
        self.z_p_stiffener_along_flange = 0.0
        self.weld_size_stiffener_along_flange = 0.0

        self.weld_size_stiffener_along_web = 0.0
        self.shear_on_stiffener_along_web = 0.0
        self.shear_capa_stiffener_along_web = 0.0
        self.moment_on_stiffener_along_web = 0.0
        self.moment_capa_stiffener_along_web = 0.0
        self.z_e_stiffener_along_web = 0.0
        self.z_p_stiffener_along_web = 0.0

        self.weld_size_stiffener_across_web = 0.0
        self.shear_on_stiffener_across_web = 0.0
        self.shear_capa_stiffener_across_web = 0.0
        self.moment_on_stiffener_across_web = 0.0
        self.moment_capa_stiffener_across_web = 0.0
        self.z_e_stiffener_across_web = 0.0
        self.z_p_stiffener_across_web = 0.0

        self.sigma_max = 0.0
        self.shear_on_stiffener = 0.0
        self.shear_capa_stiffener = 0.0
        self.z_e_stiffener = 0.0
        self.moment_on_stiffener = 0.0
        self.moment_capa_stiffener = 0.0

        self.weld_size_gusset = 0.0
        self.weld_size_stiffener = 0.0

        self.eccentricity_zz = 0.0
        self.eccentricity_yy = 0.0
        self.moment_bp_case_yy = ''
        self.sigma_max_zz = 0.0
        self.sigma_min_zz = 0.0
        self.critical_xx = 0.0
        self.sigma_xx = 0.0
        self.sigma_web = 0.0
        self.sigma_lby2 = 0.0
        self.sigma_avg = 0.0
        self.sigma_avg_2 = 0.0
        self.ze_zz = 0.0
        self.critical_M_xx = 0.0
        self.n = 1
        self.anchor_area_tension = 0.0
        self.f = 0.0
        self.y = 0.0
        self.tension_demand_anchor = 0.0
        self.tension_demand_anchor_uplift = 0.0
        self.tension_capacity_anchor = 0.0
        self.anchors_outside_flange = 0
        self.anchor_inside_flange = 'No'
        self.stiffener_inside_flange = 'No'
        self.anchor_tension_capa = 0.0
        self.safe = True
        self.max_bearing_stress = 0.0
        self.bolt_columns_outside_flange = 1

        self.anchor_area_outside_flange = self.bolt_area(self.table1(self.anchor_dia_provided_outside_flange)[0])  # TODO check if this works
        self.anchor_area_inside_flange = 0.0
        self.gusset_fy = self.dp_column_fy
        self.stiffener_fy = 0.0
        self.tension_capacity_anchor_uplift = self.tension_capacity_anchor
        self.anchor_dia_outside_flange = self.anchor_dia_provided_outside_flange
        self.anchor_dia_inside_flange = self.anchor_dia_provided_outside_flange
        self.anchor_grade_in = []
        self.shear_key_len_ColDepth = self.column_D
        self.shear_key_len_ColWidth = self.column_bf
        if self.connectivity == 'Welded Column Base':
            self.weld_type = self.weld_type
        else:
            self.weld_type = 'Butt Weld'
        self.shear_key_thk = self.plate_thk_provided

        self.minimum_load_status_Mzz = False
        self.minimum_load_status_Myy = False
        self.min_width_check_Case1 = False

    # setting logger for the module
    def set_osdaglogger(key):
        """
        Set logger for Base Plate Module.
        """
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
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def module_name(self):
        """
        Call the Base Plate Module key for displaying the module name.
        """
        return KEY_DISP_BASE_PLATE

    # define fields for the input dock to create UI
    def input_values(self):
        """
        Return a-list of tuple, used to create the Base Plate input dock U.I in Osdag design window.
        """
        self.module = KEY_DISP_BASE_PLATE

        options_list = []

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_MODULE, KEY_DISP_BASE_PLATE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t2)

        t3 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, VALUES_CONN_BP, True, 'No Validator')
        options_list.append(t3)

        t5 = (KEY_END_CONDITION, KEY_DISP_END_CONDITION, TYPE_NOTE, 'Pinned', True, 'No Validator')
        options_list.append(t5)

        t6 = (KEY_SECSIZE, KEY_DISP_COLSEC, TYPE_COMBOBOX,
              connectdb("Columns"), True, 'No Validator')  # this might not be required
        options_list.append(t6)

        t7 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t7)

        t8 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t8)

        t9 = (KEY_AXIAL_BP, KEY_DISP_AXIAL_BP, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t9)

        t22 = (KEY_AXIAL_TENSION_BP, KEY_DISP_AXIAL_TENSION_BP, TYPE_TEXTBOX, None, False, 'Int Validator')
        options_list.append(t22)

        t10 = (KEY_SHEAR_BP, KEY_DISP_SHEAR_BP, '', None, True, 'Int Validator')
        options_list.append(t10)

        t10 = (KEY_SHEAR_MAJOR, KEY_DISP_SHEAR_MAJOR, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t10)

        t10 = (KEY_SHEAR_MINOR, KEY_DISP_SHEAR_MINOR, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t10)

        t11 = (KEY_MOMENT, KEY_DISP_MOMENT, '', None, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_MOMENT_MAJOR, KEY_DISP_MOMENT_MAJOR, TYPE_TEXTBOX, None, False, 'No Validator')
        options_list.append(t12)

        t13 = (KEY_MOMENT_MINOR, KEY_DISP_MOMENT_MINOR, TYPE_TEXTBOX, None, False, 'No Validator')
        options_list.append(t13)

        t14 = (None, DISP_TITLE_ANCHOR_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t14)

        t11 = (KEY_ANCHOR_OCF, KEY_DISP_ANCHOR_OCF, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t11)

        t15 = (KEY_DIA_ANCHOR_OCF, "- " + KEY_DISP_DIA_ANCHOR, TYPE_COMBOBOX_CUSTOMIZED, VALUES_DIA_ANCHOR, True, 'No Validator')
        options_list.append(t15)

        t17 = (KEY_GRD_ANCHOR_OCF, "- " + KEY_DISP_GRD_ANCHOR, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD_ANCHOR, True, 'No Validator')
        options_list.append(t17)

        t11 = (KEY_ANCHOR_ICF, KEY_DISP_ANCHOR_ICF, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t11)

        t15 = (KEY_DIA_ANCHOR_ICF, "- " + KEY_DISP_DIA_ANCHOR, TYPE_COMBOBOX_CUSTOMIZED, VALUES_DIA_ANCHOR, True, 'No Validator')
        options_list.append(t15)

        t17 = (KEY_GRD_ANCHOR_ICF, "- " + KEY_DISP_GRD_ANCHOR, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD_ANCHOR, True, 'No Validator')
        options_list.append(t17)

        t16 = (KEY_TYP_ANCHOR, KEY_DISP_TYP_ANCHOR, TYPE_COMBOBOX, VALUES_TYP_ANCHOR, True, 'No Validator')
        options_list.append(t16)

        t18 = (None, DISP_TITLE_FOOTING, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t18)

        t19 = (KEY_GRD_FOOTING, KEY_DISP_GRD_FOOTING, TYPE_COMBOBOX, VALUES_GRD_FOOTING, True, 'No Validator')
        options_list.append(t19)

        t20 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t20)

        t21 = (KEY_WELD_TYPE, KEY_DISP_WELD_TYPE, TYPE_COMBOBOX, [VALUES_WELD_TYPE[1]], True, 'No Validator')
        options_list.append(t21)

        return options_list

    # define fields for the output dock to create UI
    def output_values(self, flag):

        out_list = []

        t1 = (None, DISP_TITLE_ANCHOR_BOLT_OUTSIDE_CF, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_OUT_DIA_ANCHOR, KEY_DISP_OUT_DIA_ANCHOR, TYPE_TEXTBOX, self.anchor_dia_outside_flange if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_OUT_GRD_ANCHOR, KEY_DISP_OUT_GRD_ANCHOR, TYPE_TEXTBOX, self.anchor_grade_out if flag else '', True)
        out_list.append(t3)

        t4 = (KEY_OUT_ANCHOR_BOLT_NO, KEY_DISP_OUT_ANCHOR_BOLT_NO, TYPE_TEXTBOX, 2 * self.anchors_outside_flange if flag else '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_ANCHOR_BOLT_SHEAR, KEY_OUT_DISP_ANCHOR_BOLT_SHEAR, TYPE_TEXTBOX,
              self.shear_capacity_anchor if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_ANCHOR_BOLT_BEARING, KEY_OUT_DISP_ANCHOR_BOLT_BEARING, TYPE_TEXTBOX,
              self.bearing_capacity_anchor if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_OUT_ANCHOR_BOLT_CAPACITY, KEY_OUT_DISP_ANCHOR_BOLT_CAPACITY, TYPE_TEXTBOX,
              self.anchor_capacity if flag else '', True)
        out_list.append(t7)

        t8 = (KEY_OUT_ANCHOR_BOLT_TENSION_DEMAND, KEY_OUT_DISP_ANCHOR_BOLT_TENSION_DEMAND, TYPE_TEXTBOX,
              self.tension_demand_anchor if flag else '', True)
        out_list.append(t8)

        t20 = (KEY_OUT_ANCHOR_BOLT_TENSION, KEY_OUT_DISP_ANCHOR_BOLT_TENSION, TYPE_TEXTBOX,
               self.tension_capacity_anchor if flag else '', True)
        out_list.append(t20)

        t8 = (KEY_OUT_ANCHOR_BOLT_COMBINED, KEY_OUT_DISP_ANCHOR_BOLT_COMBINED, TYPE_TEXTBOX,
              self.combined_capacity_anchor if flag else '', True)
        out_list.append(t8)

        t4 = (KEY_OUT_ANCHOR_BOLT_LENGTH, KEY_DISP_OUT_ANCHOR_BOLT_LENGTH, TYPE_TEXTBOX,
              self.anchor_length_provided_out if flag else '', True)
        out_list.append(t4)

        t101 = (None, DISP_TITLE_ANCHOR_BOLT_UPLIFT, TYPE_TITLE, None, True)
        out_list.append(t101)

        t101 = (KEY_OUT_DIA_ANCHOR_UPLIFT, KEY_DISP_OUT_DIA_ANCHOR_UPLIFT, TYPE_TEXTBOX,
                self.anchor_dia_inside_flange if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] and
                                                   ((self.load_axial_tension > 0) or (self.load_moment_minor > 0)) else 'N/A', True)
        out_list.append(t101)

        t101 = (KEY_OUT_GRD_ANCHOR_UPLIFT, KEY_DISP_OUT_GRD_ANCHOR_UPLIFT, TYPE_TEXTBOX,
                self.anchor_grade_in if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] and
                                                   ((self.load_axial_tension > 0) or (self.load_moment_minor > 0)) else 'N/A', True)
        out_list.append(t101)

        t4 = (KEY_OUT_ANCHOR_UPLIFT_BOLT_NO, KEY_DISP_OUT_ANCHOR_BOLT_NO, TYPE_TEXTBOX,
              self.anchors_inside_flange if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] else 'N/A', True)
        out_list.append(t4)

        t4 = (KEY_OUT_ANCHOR_BOLT_TENSION_DEMAND_UPLIFT, KEY_OUT_DISP_ANCHOR_BOLT_TENSION_DEMAND_UPLIFT, TYPE_TEXTBOX,
              self.tension_demand_anchor_uplift if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] else 'N/A', True)
        out_list.append(t4)

        t101 = (KEY_OUT_ANCHOR_BOLT_TENSION_UPLIFT, KEY_OUT_DISP_ANCHOR_BOLT_TENSION_UPLIFT, TYPE_TEXTBOX,
                self.tension_capacity_anchor_uplift if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] and
                                                   ((self.load_axial_tension > 0) or (self.load_moment_minor > 0)) else 'N/A', True)
        out_list.append(t101)

        t101 = (KEY_OUT_ANCHOR_BOLT_LENGTH_UPLIFT, KEY_DISP_OUT_ANCHOR_BOLT_LENGTH_UPLIFT, TYPE_TEXTBOX,
                self.anchor_length_provided_in if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] else 'N/A', True)
        out_list.append(t101)

        t9 = (None, KEY_DISP_BASE_PLATE, TYPE_TITLE, None, True)
        out_list.append(t9)

        t10 = (KEY_OUT_BASEPLATE_THICKNNESS, KEY_OUT_DISP_BASEPLATE_THICKNNESS, TYPE_TEXTBOX,
               int(self.plate_thk_provided) if flag else '', True)
        out_list.append(t10)

        t11 = (KEY_OUT_BASEPLATE_LENGTH, KEY_OUT_DISP_BASEPLATE_LENGTH, TYPE_TEXTBOX,
               float(self.bp_length_provided) if flag else '', True)
        out_list.append(t11)

        t12 = (KEY_OUT_BASEPLATE_WIDTH, KEY_OUT_DISP_BASEPLATE_WIDTH, TYPE_TEXTBOX,
               float(self.bp_width_provided) if flag else '', True)
        out_list.append(t12)

        t12 = (KEY_OUT_BASEPLATE_BEARING_STRESS, KEY_OUT_DISP_BASEPLATE_BEARING_STRESS, TYPE_TEXTBOX, round(self.max_bearing_stress, 2)
        if flag else '', True)
        out_list.append(t12)

        t12 = (KEY_OUT_BASEPLATE_MOMENT_DEMAND, KEY_OUT_DISP_BASEPLATE_MOMENT_DEMAND, TYPE_TEXTBOX, round(self.critical_M_xx * 1e-6, 2)
        if flag and self.connectivity == 'Moment Base Plate' else '', True)
        out_list.append(t12)

        t12 = (KEY_OUT_BASEPLATE_MOMENT_CAPACITY, KEY_OUT_DISP_BASEPLATE_MOMENT_CAPACITY, TYPE_TEXTBOX, round(self.plate_moment_capacity, 2)
        if flag and self.connectivity == 'Moment Base Plate' else '', True)
        out_list.append(t12)

        t12 = (KEY_OUT_BP_TYPICAL_SKETCH, KEY_OUT_DISP_STIFFENER_SKETCH, TYPE_OUT_BUTTON, ['Typical Sketch', self.base_plate_sketch], True)
        out_list.append(t12)

        t13 = (None, DISP_TITLE_DETAILING_OCF, TYPE_TITLE, None, True)
        out_list.append(t13)

        t15 = (KEY_OUT_DETAILING_END_DISTANCE, KEY_OUT_DISP_DETAILING_END_DISTANCE, TYPE_TEXTBOX, self.end_distance_out if flag else 'N/A', True)
        out_list.append(t15)

        t16 = (KEY_OUT_DETAILING_EDGE_DISTANCE, KEY_OUT_DISP_DETAILING_EDGE_DISTANCE, TYPE_TEXTBOX, self.edge_distance_out if flag else 'N/A', True)
        out_list.append(t16)

        t21 = (KEY_OUT_DETAILING_PITCH_DISTANCE, KEY_OUT_DISP_DETAILING_PITCH_DISTANCE, TYPE_TEXTBOX, self.pitch_distance_out
        if flag and self.pitch_distance_out > 0.0 else 'N/A', True)
        out_list.append(t21)

        t22 = (KEY_OUT_DETAILING_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX, self.gauge_distance_out
        if flag and self.gauge_distance_out > 0.0 else 'N/A', True)
        out_list.append(t22)

        t17 = (KEY_OUT_DETAILING_PROJECTION, KEY_OUT_DISP_DETAILING_PROJECTION, TYPE_TEXTBOX,
               self.projection if flag and self.connectivity in ['Welded Column Base',
                                                                 'Hollow/Tubular Column Base'] else '', True)
        out_list.append(t17)

        t13 = (None, DISP_TITLE_DETAILING_ICF, TYPE_TITLE, None, True)
        out_list.append(t13)

        t15 = (KEY_IN_DETAILING_END_DISTANCE, KEY_IN_DISP_DETAILING_END_DISTANCE, TYPE_TEXTBOX,
               self.end_distance_in if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] and
                                         (self.load_axial_tension > 0 or self.load_moment_minor > 0) else 'N/A', True)
        out_list.append(t15)

        t16 = (KEY_IN_DETAILING_EDGE_DISTANCE, KEY_IN_DISP_DETAILING_EDGE_DISTANCE, TYPE_TEXTBOX,
               self.edge_distance_in if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] and
                                         (self.load_axial_tension > 0 or self.load_moment_minor > 0) else 'N/A', True)
        out_list.append(t16)

        t21 = (KEY_IN_DETAILING_PITCH_DISTANCE, KEY_IN_DISP_DETAILING_PITCH_DISTANCE, TYPE_TEXTBOX,
               self.pitch_distance_in if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] and
                                         (self.load_axial_tension > 0 and self.anchors_inside_flange > 2) else 'N/A', True)
        out_list.append(t21)

        t22 = (KEY_IN_DETAILING_GAUGE_DISTANCE, KEY_IN_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX,
               self.gauge_distance_in if flag and self.connectivity in ['Welded Column Base', 'Moment Base Plate'] and
                                         (self.load_axial_tension > 0 and self.anchors_inside_flange > 2) else 'N/A', True)
        out_list.append(t22)

        t23 = (None, KEY_OUT_DISP_BP_DETAILING_SKETCH, TYPE_TITLE, None, True)
        out_list.append(t23)

        t12 = (KEY_OUT_BP_TYPICAL_DETAILING, KEY_OUT_DISP_BP_DETAILING, TYPE_OUT_BUTTON, ['Typical Detailing', self.base_plate_detailing], True)
        out_list.append(t12)

        t23 = (None, DISP_TITLE_STIFFENER_PLATE_FLANGE, TYPE_TITLE, None, True)
        out_list.append(t23)

        t24 = (KEY_OUT_STIFFENER_PLATE_FLANGE, KEY_DISP_OUT_STIFFENER_PLATE_FLANGE, TYPE_OUT_BUTTON,
               ['Stiffener Details', self.stiffener_flange_details], True)
        out_list.append(t24)

        t29 = (None, DISP_TITLE_STIFFENER_PLATE_ALONG_WEB, TYPE_TITLE, None, True)
        out_list.append(t29)

        t30 = (KEY_OUT_STIFFENER_PLATE_ALONG_WEB, KEY_DISP_OUT_STIFFENER_PLATE_ALONG_WEB, TYPE_OUT_BUTTON,
               ['Stiffener Details', self.stiffener_along_web_details], True)
        out_list.append(t30)

        t29 = (None, DISP_TITLE_STIFFENER_PLATE_ACROSS_WEB, TYPE_TITLE, None, True)
        out_list.append(t29)

        t30 = (KEY_OUT_STIFFENER_PLATE_ACROSS_WEB, KEY_DISP_OUT_STIFFENER_PLATE_ACROSS_WEB, TYPE_OUT_BUTTON,
               ['Stiffener Details', self.stiffener_across_web_details], True)
        out_list.append(t30)

        t29 = (None, DISP_TITLE_STIFFENER_PLATE, TYPE_TITLE, None, True)
        out_list.append(t29)

        t30 = (DISP_OUT_TITLE_STIFFENER_PLATE, DISP_TITLE_STIFFENER_PLATE, TYPE_OUT_BUTTON,
               ['Stiffener Details', self.stiffener_hollow_details], True)
        out_list.append(t30)

        t29 = (None, DISP_TITLE_SHEAR_KEY, TYPE_TITLE, None, True)
        out_list.append(t29)

        t31 = (KEY_OUT_SHEAR_RESISTANCE, KEY_OUT_DISP_SHEAR_RESISTANCE, TYPE_TEXTBOX,
               round(self.shear_resistance * 1e-3, 2) if flag and (self.load_shear_major > 0 or self.load_shear_minor > 0) else 'N/A', True)
        out_list.append(t31)

        t32 = (KEY_OUT_SHEAR_KEY_REQ, KEY_OUT_DISP_SHEAR_KEY_REQ, TYPE_TEXTBOX,
               'Yes' if flag and (self.shear_key_along_ColDepth == 'Yes' or self.shear_key_along_ColWidth == 'Yes') else 'No', True)
        out_list.append(t32)

        t30 = (KEY_OUT_SHEAR_KEY, KEY_DISP_OUT_SHEAR_KEY, TYPE_OUT_BUTTON, ['Key Details', self.shear_key_details], True)
        out_list.append(t30)

        t30 = (KEY_OUT_SHEAR_KEY_TYPICAL_DETAILS, KEY_DISP_OUT_SHEAR_KEY_TYPICAL_DETAILS, TYPE_OUT_BUTTON, ['Sketch', self.shear_key_sketch], True)
        out_list.append(t30)

        t18 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t18)

        t20 = (KEY_OUT_WELD_SIZE_FLANGE, KEY_OUT_DISP_WELD_SIZE_FLANGE, TYPE_TEXTBOX,
               self.weld_size_flange if flag and self.weld_type != 'Groove Weld' else '', True)
        out_list.append(t20)

        t21 = (KEY_OUT_WELD_SIZE_WEB, KEY_OUT_DISP_WELD_SIZE_WEB, TYPE_TEXTBOX,
               self.weld_size_web if flag and self.weld_type != 'Groove Weld' else '', True)
        out_list.append(t21)

        t22 = (KEY_OUT_WELD_SIZE_STIFFENER, KEY_OUT_DISP_WELD_SIZE_STIFFENER, TYPE_TEXTBOX,
               self.weld_size_stiffener if flag and self.weld_type != 'Groove Weld' else '', True)
        out_list.append(t22)

        t19 = (KEY_OUT_WELD_DETAILS, DISP_TITLE_WELD, TYPE_OUT_BUTTON, ['Typical Details', self.weld_details], True)
        out_list.append(t19)

        return out_list

    def stiffener_flange_details(self, flag):

        sf = []

        t22 = (KEY_OUT_STIFFENER_PLATE_FLANGE_LENGTH, KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_LENGTH, TYPE_TEXTBOX,
               round(self.stiffener_plt_len_along_flange, 1) if flag and self.stiffener_along_flange == 'Yes' else VALUE_NOT_APPLICABLE)
        sf.append(t22)

        t23 = (KEY_OUT_STIFFENER_PLATE_FLANGE_HEIGHT, KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_HEIGHT, TYPE_TEXTBOX,
               round(self.stiffener_plt_height_along_flange, 1) if flag and self.stiffener_along_flange == 'Yes' else VALUE_NOT_APPLICABLE)
        sf.append(t23)

        t24 = (KEY_OUT_STIFFENER_PLATE_FLANGE_THICKNNESS, KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_THICKNESS, TYPE_TEXTBOX,
               self.stiffener_plt_thick_along_flange if flag and self.stiffener_along_flange == 'Yes' else VALUE_NOT_APPLICABLE)
        sf.append(t24)

        t25 = (KEY_OUT_STIFFENER_PLATE_FLANGE_SHEAR_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_SHEAR_DEMAND,
               TYPE_TEXTBOX,
               self.shear_on_stiffener_along_flange if flag and self.stiffener_along_flange == 'Yes' else VALUE_NOT_APPLICABLE)
        sf.append(t25)

        t26 = (KEY_OUT_STIFFENER_PLATE_FLANGE_SHEAR, KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_SHEAR, TYPE_TEXTBOX,
               self.shear_capa_stiffener_along_flange if flag and self.stiffener_along_flange == 'Yes' else VALUE_NOT_APPLICABLE)
        sf.append(t26)

        t27 = (KEY_OUT_STIFFENER_PLATE_FLANGE_MOMENT_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_MOMENT_DEMAND,
               TYPE_TEXTBOX,
               self.moment_on_stiffener_along_flange if flag and self.stiffener_along_flange == 'Yes' else VALUE_NOT_APPLICABLE)
        sf.append(t27)

        t28 = (KEY_OUT_STIFFENER_PLATE_FLANGE_MOMENT, KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_MOMENT, TYPE_TEXTBOX,
               self.moment_capa_stiffener_along_flange if flag and self.stiffener_along_flange == 'Yes' else VALUE_NOT_APPLICABLE)
        sf.append(t28)

        return sf

    def stiffener_along_web_details(self, flag):

        sw = []

        t28 = (KEY_OUT_STIFFENER_PLATE_ALONG_WEB_LENGTH, KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_LENGTH, TYPE_TEXTBOX,
               round(self.stiffener_plt_len_along_web, 1) if flag and self.stiffener_along_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t28)

        t29 = (KEY_OUT_STIFFENER_PLATE_ALONG_WEB_HEIGHT, KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_HEIGHT, TYPE_TEXTBOX,
               round(self.stiffener_plt_height_along_web, 1) if flag and self.stiffener_along_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t29)

        t30 = (KEY_OUT_STIFFENER_PLATE_ALONG_WEB_THICKNNESS, KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_THICKNESS, TYPE_TEXTBOX,
               self.stiffener_plt_thick_along_web if flag and self.stiffener_along_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t30)

        t31 = (KEY_OUT_STIFFENER_PLATE_ALONG_WEB_SHEAR_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_SHEAR_DEMAND, TYPE_TEXTBOX,
               self.shear_on_stiffener_along_web if flag and self.stiffener_along_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t31)

        t32 = (KEY_OUT_STIFFENER_PLATE_ALONG_WEB_SHEAR, KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_SHEAR, TYPE_TEXTBOX,
               self.shear_capa_stiffener_along_web if flag and self.stiffener_along_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t32)

        t33 = (KEY_OUT_STIFFENER_PLATE_ALONG_WEB_MOMENT_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_MOMENT_DEMAND, TYPE_TEXTBOX,
               self.moment_on_stiffener_along_web if flag and self.stiffener_along_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t33)

        t34 = (KEY_OUT_STIFFENER_PLATE_ALONG_WEB_MOMENT, KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_MOMENT, TYPE_TEXTBOX,
               self.moment_capa_stiffener_along_web if flag and self.stiffener_along_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t34)

        return sw

    def stiffener_across_web_details(self, flag):

        sw = []

        t28 = (KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_LENGTH, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_LENGTH, TYPE_TEXTBOX,
               round(self.stiffener_plt_len_across_web, 1) if flag and self.stiffener_across_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t28)

        t29 = (KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_HEIGHT, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_HEIGHT, TYPE_TEXTBOX,
               round(self.stiffener_plt_height_across_web, 1) if flag and self.stiffener_across_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t29)

        t30 = (KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_THICKNNESS, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_THICKNESS, TYPE_TEXTBOX,
               self.stiffener_plt_thick_across_web if flag and self.stiffener_across_web == 'Yes' else VALUE_NOT_APPLICABLE)
        sw.append(t30)

        return sw

    def stiffener_hollow_details(self, flag):

        st = []

        # attached to D
        t99 = (None, 'Stiffener Plate Attached to Column D (SHS/RHS)', TYPE_SECTION, '')
        st.append(t99)

        t28 = (KEY_OUT_STIFFENER_LENGTH, KEY_OUT_DISP_STIFFENER_LENGTH, TYPE_TEXTBOX,
               self.stiffener_plt_len_along_D if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t28)

        t29 = (KEY_OUT_STIFFENER_HEIGHT, KEY_OUT_DISP_STIFFENER_HEIGHT, TYPE_TEXTBOX,
               self.stiffener_plt_height if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t29)

        t30 = (KEY_OUT_STIFFENER_THICKNESS, KEY_OUT_DISP_STIFFENER_THICKNESS, TYPE_TEXTBOX,
               self.stiffener_plt_thk if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t30)

        t31 = (KEY_OUT_STIFFENER_PLATE_SHEAR_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_SHEAR_DEMAND, TYPE_TEXTBOX,
               self.shear_on_stiffener if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_SHEAR_CAPACITY, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_SHEAR, TYPE_TEXTBOX,
               self.shear_capa_stiffener if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_MOMENT_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT_DEMAND, TYPE_TEXTBOX,
               self.moment_on_stiffener if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_MOMENT_CAPACITY, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT, TYPE_TEXTBOX,
               self.moment_capa_stiffener if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t31)

        # attached to B
        t99 = (None, 'Stiffener Plate Attached to Column B (SHS/RHS)', TYPE_SECTION, '')
        st.append(t99)

        t28 = (KEY_OUT_STIFFENER_LENGTH, KEY_OUT_DISP_STIFFENER_LENGTH, TYPE_TEXTBOX,
               self.stiffener_plt_len_along_B if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t28)

        t29 = (KEY_OUT_STIFFENER_HEIGHT, KEY_OUT_DISP_STIFFENER_HEIGHT, TYPE_TEXTBOX,
               self.stiffener_plt_height if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t29)

        t30 = (KEY_OUT_STIFFENER_THICKNESS, KEY_OUT_DISP_STIFFENER_THICKNESS, TYPE_TEXTBOX,
               self.stiffener_plt_thk if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t30)

        t31 = (KEY_OUT_STIFFENER_PLATE_SHEAR_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_SHEAR_DEMAND, TYPE_TEXTBOX,
               self.shear_on_stiffener if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_SHEAR_CAPACITY, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_SHEAR, TYPE_TEXTBOX,
               self.shear_capa_stiffener if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_MOMENT_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT_DEMAND, TYPE_TEXTBOX,
               self.moment_on_stiffener if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_MOMENT_CAPACITY, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT, TYPE_TEXTBOX,
               self.moment_capa_stiffener if flag and self.dp_column_designation[1:4] == 'SHS' or self.dp_column_designation[1:4] == 'RHS'
               else VALUE_NOT_APPLICABLE)
        st.append(t31)

        # CHS
        t99 = (None, 'Stiffener Plate Attached to OD (CHS)', TYPE_SECTION, '')
        st.append(t99)

        t28 = (KEY_OUT_STIFFENER_LENGTH_CHS, KEY_OUT_DISP_STIFFENER_LENGTH, TYPE_TEXTBOX,
               round_down(self.stiffener_plt_len_across_D, 1) if flag and self.dp_column_designation[1:4] == 'CHS' else VALUE_NOT_APPLICABLE)
        st.append(t28)

        t29 = (KEY_OUT_STIFFENER_HEIGHT_CHS, KEY_OUT_DISP_STIFFENER_HEIGHT, TYPE_TEXTBOX,
               self.stiffener_plt_height if flag and self.dp_column_designation[1:4] == 'CHS' else VALUE_NOT_APPLICABLE)
        st.append(t29)

        t30 = (KEY_OUT_STIFFENER_THICKNESS_CHS, KEY_OUT_DISP_STIFFENER_THICKNESS, TYPE_TEXTBOX,
               self.stiffener_plt_thk if flag and self.dp_column_designation[1:4] == 'CHS' else VALUE_NOT_APPLICABLE)
        st.append(t30)

        t31 = (KEY_OUT_STIFFENER_PLATE_SHEAR_DEMAND_CHS, KEY_OUT_DISP_STIFFENER_PLATE_SHEAR_DEMAND, TYPE_TEXTBOX,
               self.shear_on_stiffener if flag and self.dp_column_designation[1:4] == 'CHS' else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_SHEAR_CAPACITY_CHS, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_SHEAR, TYPE_TEXTBOX,
               self.shear_capa_stiffener if flag and self.dp_column_designation[1:4] == 'CHS' else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_MOMENT_DEMAND_CHS, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT_DEMAND, TYPE_TEXTBOX,
               self.moment_on_stiffener if flag and self.dp_column_designation[1:4] == 'CHS' else VALUE_NOT_APPLICABLE)
        st.append(t31)

        t31 = (KEY_OUT_STIFFENER_PLATE_MOMENT_CAPACITY_CHS, KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT, TYPE_TEXTBOX,
               self.moment_capa_stiffener if flag and self.dp_column_designation[1:4] == 'CHS' else VALUE_NOT_APPLICABLE)
        st.append(t31)

        return st

    # base_plate_sketch
    def base_plate_sketch(self, status):

        sketch = []

        if self.connectivity == 'Moment Base Plate':
            if self.moment_bp_case == 'Case1':
                sketch_path = './ResourceFiles/images/Moment_BP.png'
                width = 870
                height = 525
            elif self.moment_bp_case == 'Case2':
                sketch_path = './ResourceFiles/images/Moment_BP_C2.png'
                width = 852
                height = 541
            elif self.moment_bp_case == 'Case3':
                sketch_path = './ResourceFiles/images/Moment_BP_C3.png'
                width = 852
                height = 541
            else:
                sketch_path = ''
                width = 852
                height = 541

        elif self.connectivity == 'Welded Column Base':
            sketch_path = './ResourceFiles/images/Welded_BP.png'
            width = 852
            height = 541

        elif self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                sketch_path = './ResourceFiles/images/SHS_BP.png'
            elif self.dp_column_designation[1:4] == 'RHS':
                sketch_path = './ResourceFiles/images/RHS_BP.png'
            elif self.dp_column_designation[1:4] == 'CHS':
                sketch_path = './ResourceFiles/images/CHS_BP.png'
            else:
                sketch_path = ''
            width = 854
            height = 545
        else:
            sketch_path = ''
            width = 854
            height = 545

        t1 = (None, 'Typical Base Plate Sketch', TYPE_IMAGE, [sketch_path, width, height, 'Typical base plate details'])
        sketch.append(t1)

        return sketch

    # base plate detailing
    def base_plate_detailing(self, status):

        detailing = []

        if self.connectivity == 'Moment Base Plate':
            detailing_path = './ResourceFiles/images/Moment_BP_Detailing.png'
            width = 702
            height = 518

        elif self.connectivity == 'Welded Column Base':
            detailing_path = './ResourceFiles/images/Welded_BP_Detailing.png'
            width = 747
            height = 552

        elif self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                detailing_path = './ResourceFiles/images/SHS_BP_Detailing.png'
                width = 670
                height = 600
            elif self.dp_column_designation[1:4] == 'RHS':
                detailing_path = './ResourceFiles/images/RHS_BP_Detailing.png'
                width = 771
                height = 570
            elif self.dp_column_designation[1:4] == 'CHS':
                detailing_path = './ResourceFiles/images/CHS_BP_Detailing.png'
                width = 644
                height = 577
            else:
                detailing_path = ''
                width = 594
                height = 380
        else:
            detailing_path = ''
            width = 594
            height = 380

        t1 = (None, 'Typical Detailing', TYPE_IMAGE, [detailing_path, width, height, 'Typical detailing'])
        detailing.append(t1)

        return detailing

    def shear_key_details(self, flag):

        sk = []

        t99 = (None, 'Shear Key Along Column Depth', TYPE_SECTION, '')
        sk.append(t99)

        t28 = (KEY_OUT_SHEAR_KEY_LENGTH, KEY_OUT_DISP_SHEAR_KEY_LENGTH, TYPE_TEXTBOX,
               self.shear_key_len_ColDepth if flag and self.shear_key_along_ColDepth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t28)

        t29 = (KEY_OUT_SHEAR_KEY_DEPTH, KEY_OUT_DISP_SHEAR_KEY_DEPTH, TYPE_TEXTBOX,
               self.shear_key_depth_ColDepth if flag and self.shear_key_along_ColDepth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t29)

        t30 = (KEY_OUT_SHEAR_KEY_THICKNESS, KEY_OUT_DISP_SHEAR_KEY_THICKNESS, TYPE_TEXTBOX,
               self.shear_key_thk if flag and self.shear_key_along_ColDepth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t30)

        t31 = (KEY_OUT_SHEAR_KEY_STRESS, KEY_OUT_DISP_SHEAR_KEY_STRESS, TYPE_TEXTBOX,
               self.shear_key_stress_ColDepth if flag and self.shear_key_along_ColDepth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t31)

        t32 = (KEY_OUT_SHEAR_KEY_MOM_DEMAND, KEY_OUT_DISP_SHEAR_KEY_MOM_DEMAND, TYPE_TEXTBOX, round(self.shear_key_moment_1 * 1e-6, 2)
               if flag and self.shear_key_along_ColDepth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t32)

        t33 = (KEY_OUT_SHEAR_KEY_MOM_CAPACITY, KEY_OUT_DISP_SHEAR_KEY_MOM_CAPACITY, TYPE_TEXTBOX, self.moment_capacity_key1
               if flag and self.shear_key_along_ColDepth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t33)

        t99 = (None, 'Shear Key Along Column Width', TYPE_SECTION, '')
        sk.append(t99)

        t28 = (KEY_OUT_SHEAR_KEY_LENGTH, KEY_OUT_DISP_SHEAR_KEY_LENGTH, TYPE_TEXTBOX,
               self.shear_key_len_ColWidth if flag and self.shear_key_along_ColWidth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t28)

        t29 = (KEY_OUT_SHEAR_KEY_DEPTH, KEY_OUT_DISP_SHEAR_KEY_DEPTH, TYPE_TEXTBOX,
               self.shear_key_depth_ColWidth if flag and self.shear_key_along_ColWidth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t29)

        t30 = (KEY_OUT_SHEAR_KEY_THICKNESS, KEY_OUT_DISP_SHEAR_KEY_THICKNESS, TYPE_TEXTBOX,
               self.shear_key_thk if flag and self.shear_key_along_ColWidth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t30)

        t31 = (KEY_OUT_SHEAR_KEY_STRESS, KEY_OUT_DISP_SHEAR_KEY_STRESS, TYPE_TEXTBOX,
               self.shear_key_stress_ColWidth if flag and self.shear_key_along_ColWidth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t31)

        t32 = (KEY_OUT_SHEAR_KEY_MOM_DEMAND, KEY_OUT_DISP_SHEAR_KEY_MOM_DEMAND, TYPE_TEXTBOX, round(self.shear_key_moment_2 * 1e-6, 2)
        if flag and self.shear_key_along_ColWidth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t32)

        t33 = (KEY_OUT_SHEAR_KEY_MOM_CAPACITY, KEY_OUT_DISP_SHEAR_KEY_MOM_CAPACITY, TYPE_TEXTBOX, self.moment_capacity_key2
        if flag and self.shear_key_along_ColWidth == 'Yes' else VALUE_NOT_APPLICABLE)
        sk.append(t33)

        return sk

    def shear_key_sketch(self, flag):

        key = []

        if self.connectivity == 'Hollow/Tubular Column Base':

            if self.dp_column_designation[1:4] == 'SHS':
                if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                    key_path = './ResourceFiles/images/Key_SHS.png'
                elif self.shear_key_along_ColDepth == 'Yes':
                    key_path = './ResourceFiles/images/Key_SHS_D.png'
                elif self.shear_key_along_ColWidth == 'Yes':
                    key_path = './ResourceFiles/images/Key_SHS_B.png'
                else:
                    key_path = ''

                width = 700
                height = 520

            elif self.dp_column_designation[1:4] == 'RHS':
                if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                    key_path = './ResourceFiles/images/Key_RHS.png'
                elif self.shear_key_along_ColDepth == 'Yes':
                    key_path = './ResourceFiles/images/Key_RHS_D.png'
                elif self.shear_key_along_ColWidth == 'Yes':
                    key_path = './ResourceFiles/images/Key_RHS_B.png'
                else:
                    key_path = ''

                width = 920
                height = 532

            elif self.dp_column_designation[1:4] == 'CHS':
                if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                    key_path = './ResourceFiles/images/Key_CHS.png'
                elif self.shear_key_along_ColDepth == 'Yes':
                    key_path = './ResourceFiles/images/Key_CHS_key1.png'
                elif self.shear_key_along_ColWidth == 'Yes':
                    key_path = './ResourceFiles/images/Key_CHS_key2.png'
                else:
                    key_path = ''

                width = 650
                height = 525

            else:
                key_path = ''
                width = 594
                height = 380

        else:
            if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                key_path = './ResourceFiles/images/shear_key.png'
            elif self.shear_key_along_ColDepth == 'Yes':
                key_path = './ResourceFiles/images/shear_key_colD.png'
            elif self.shear_key_along_ColWidth == 'Yes':
                key_path = './ResourceFiles/images/shear_key_colB.png'
            else:
                key_path = ''

            width = 972
            height = 570

        t1 = (None, 'Typical Shear Key Details', TYPE_IMAGE, [key_path, width, height, 'Typical shear key details'])
        key.append(t1)

        return key

    def weld_details(self, flag):

        weld = []

        if self.connectivity == 'Moment Base Plate':

            if self.weld_bp_groove == 'Yes':
                web_groove_weld = 'Yes'
            else:
                web_groove_weld = 'No'

            if web_groove_weld == 'No':
                if (self.shear_key_along_ColDepth == 'Yes') or (self.shear_key_along_ColWidth == 'Yes'):
                    web_groove_weld = 'Yes'
                else:
                    web_groove_weld = 'No'

            if (self.column_tf < 40.0) and (web_groove_weld == 'No'):
                weld_path = './ResourceFiles/images/Moment_BP_weld_details_1-1.png'
            elif (self.column_tf < 40.0) and (web_groove_weld == 'Yes'):
                weld_path = './ResourceFiles/images/Moment_BP_weld_details_1-2.png'
            elif self.column_tf > 40.0:
                weld_path = './ResourceFiles/images/Moment_BP_weld_details_2.png'

            width = 878
            height = 565

        elif self.connectivity == 'Welded Column Base':
            if self.weld_bp_groove == 'No':
                weld_path = './ResourceFiles/images/BP_welded_weld_details.png'
            else:
                if self.column_tf < 40.0:
                    weld_path = './ResourceFiles/images/Welded_BP_single_bevel.png'
                if self.column_tf >= 40.0:
                    weld_path = './ResourceFiles/images/Welded_BP_double_J.png'
                else:
                    weld_path = './ResourceFiles/images/BP_welded_weld_details.png'

            width = 915
            height = 545

        elif self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                if self.weld_bp_groove == 'Yes':
                    weld_path = './ResourceFiles/images/SHS_BP_groove_weld_details.png'
                else:
                    weld_path = './ResourceFiles/images/SHS_BP_weld_details.png'
                width = 890
                height = 590
            elif self.dp_column_designation[1:4] == 'RHS':
                if self.weld_bp_groove == 'Yes':
                    weld_path = './ResourceFiles/images/RHS_BP_groove_weld_details.png'
                else:
                    weld_path = './ResourceFiles/images/RHS_BP_weld_details.png'
                width = 880
                height = 470
            elif self.dp_column_designation[1:4] == 'CHS':
                if self.weld_bp_groove == 'Yes':
                    weld_path = './ResourceFiles/images/CHS_BP_groove_weld_details.png'
                else:
                    weld_path = './ResourceFiles/images/CHS_BP_weld_details.png'
                width = 785
                height = 602
            else:
                weld_path = ''
                width = 594
                height = 380
        else:
            weld_path = ''
            width = 594
            height = 380

        t1 = (None, 'Typical Weld Details', TYPE_IMAGE, [weld_path, width, height, 'Typical weld details'])
        weld.append(t1)

        return weld

    def major_minor(self):
        if self[0] in ['Moment Base Plate']:
            return True
        else:
            return False

    def stiffener_flange(self):
        if self[0] in ['Moment Base Plate']:
            return False
        else:
            return True

    def stiffener_alongweb(self):
        if self[0] in ['Moment Base Plate']:
            return False
        else:
            return True

    def stiffener_acrossweb(self):
        if self[0] in ['Moment Base Plate', 'Welded Column Base']:
            return False
        else:
            return True

    def stiffener_hollow_cs(self):
        if self[0] in ['Moment Base Plate', 'Welded Column Base']:
            return True
        else:
            return False

    def stiffener_chs_len(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def stiffener_chs_height(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def stiffener_chs_thk(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def stiffener_chs_shear_demand(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def stiffener_chs_shear_capa(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def stiffener_chs_moment_demand(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def stiffener_chs_moment_capa(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def conn_axial_tension(self):
        if self[0] == 'Moment Base Plate':
            return True
        else:
            return False

    def label_end_condition(self):
        if self[0] in ['Moment Base Plate', 'Hollow/Tubular Column Base']:
            return 'Fixed'
        else:
            return 'Pinned'

    def anchor_type_warning(self):

        if self[0] in ['IS 5624-Type A', 'IS 5624-Type B']:
            return True
        else:
            return False

    def conn_weld_type(self):
        # if self[0] in ['Welded+Bolted Column Base', 'Hollow/Tubular Column Base', 'Moment Base Plate']:
        #     return VALUES_WELD_TYPE
        # else:
        weld = []
        weld.append(VALUES_WELD_TYPE[1])
        return weld

    def out_weld(self):

        conn = self[0]
        if conn == 'Groove Weld':
            return True
        else:
            return False

    def out_anchor_tension(self):
        if self[0] in ['Hollow/Tubular Column Base', 'Welded Column Base']:
            return True
        else:
            return False

    def in_anchor(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return True
        else:
            return False

    def in_anchor_hollow(self):
        if self[0] in ['Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def out_detail_projection(self):
        if self[0] in ['Welded Column Base', 'Hollow/Tubular Column Base']:
            return False
        else:
            return True

    def detailing_in(self):
        if self[0] in ['Moment Base Plate', 'Welded Column Base']:
            return False
        else:
            return True

    def out_anchor_combined(self):
        if self[0] != 'Welded Column Base':
            return True
        else:
            return False

    def secsize_for_hollow(self):
        if self[0] == 'Hollow/Tubular Column Base':
            secsize = []
            secsize.extend(connectdb("RHS"))
            secsize.extend(connectdb("SHS", call_type="popup"))
            secsize.extend(connectdb("CHS", call_type="popup"))
            return secsize
        else:
            return connectdb("Columns")

    # define customizations when any specific input value is changed
    def input_value_changed(self):

        lst = []

        t1 = ([KEY_CONN], KEY_MOMENT_MAJOR, TYPE_TEXTBOX, self.major_minor)
        lst.append(t1)

        t2 = ([KEY_CONN], KEY_MOMENT_MINOR, TYPE_TEXTBOX, self.major_minor)
        lst.append(t2)

        t19 = ([KEY_CONN], KEY_AXIAL_TENSION_BP, TYPE_TEXTBOX, self.conn_axial_tension)
        lst.append(t19)

        t3 = ([KEY_CONN], KEY_END_CONDITION, TYPE_NOTE, self.label_end_condition)
        lst.append(t3)

        t18 = ([KEY_TYP_ANCHOR],
               'The selected anchor bolt type is not suggested by Osdag', TYPE_WARNING, self.anchor_type_warning)
        lst.append(t18)

        t20 = ([KEY_CONN], KEY_WELD_TYPE, TYPE_COMBOBOX, self.conn_weld_type)
        lst.append(t20)

        t12 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_FLANGE, TYPE_OUT_DOCK, self.out_weld)
        lst.append(t12)

        t13 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_FLANGE, TYPE_OUT_LABEL, self.out_weld)
        lst.append(t13)

        t14 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_WEB, TYPE_OUT_DOCK, self.out_weld)
        lst.append(t14)

        t15 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_WEB, TYPE_OUT_LABEL, self.out_weld)
        lst.append(t15)

        t16 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_STIFFENER, TYPE_OUT_DOCK, self.out_weld)
        lst.append(t16)

        t17 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_STIFFENER, TYPE_OUT_LABEL, self.out_weld)
        lst.append(t17)

        t8 = ([KEY_CONN], KEY_OUT_DETAILING_PROJECTION, TYPE_OUT_DOCK, self.out_detail_projection)
        lst.append(t8)

        t9 = ([KEY_CONN], KEY_OUT_DETAILING_PROJECTION, TYPE_OUT_LABEL, self.out_detail_projection)
        lst.append(t9)

        ## detailing_in

        t8 = ([KEY_CONN], KEY_IN_DETAILING_END_DISTANCE, TYPE_OUT_DOCK, self.detailing_in)
        lst.append(t8)

        t9 = ([KEY_CONN], KEY_IN_DETAILING_END_DISTANCE, TYPE_OUT_LABEL, self.detailing_in)
        lst.append(t9)

        t8 = ([KEY_CONN], KEY_IN_DETAILING_EDGE_DISTANCE, TYPE_OUT_DOCK, self.detailing_in)
        lst.append(t8)

        t9 = ([KEY_CONN], KEY_IN_DETAILING_EDGE_DISTANCE, TYPE_OUT_LABEL, self.detailing_in)
        lst.append(t9)

        t8 = ([KEY_CONN], KEY_IN_DETAILING_PITCH_DISTANCE, TYPE_OUT_DOCK, self.detailing_in)
        lst.append(t8)

        t9 = ([KEY_CONN], KEY_IN_DETAILING_PITCH_DISTANCE, TYPE_OUT_LABEL, self.detailing_in)
        lst.append(t9)

        t8 = ([KEY_CONN], KEY_IN_DETAILING_GAUGE_DISTANCE, TYPE_OUT_DOCK, self.detailing_in)
        lst.append(t8)

        t9 = ([KEY_CONN], KEY_IN_DETAILING_GAUGE_DISTANCE, TYPE_OUT_LABEL, self.detailing_in)
        lst.append(t9)

        t12 = ([KEY_CONN], KEY_OUT_DIA_ANCHOR_UPLIFT, TYPE_OUT_DOCK, self.out_anchor_tension)
        lst.append(t12)

        t13 = ([KEY_CONN], KEY_OUT_DIA_ANCHOR_UPLIFT, TYPE_OUT_LABEL, self.out_anchor_tension)
        lst.append(t13)

        t14 = ([KEY_CONN], KEY_OUT_GRD_ANCHOR_UPLIFT, TYPE_OUT_DOCK, self.out_anchor_tension)
        lst.append(t14)

        t15 = ([KEY_CONN], KEY_OUT_GRD_ANCHOR_UPLIFT, TYPE_OUT_LABEL, self.out_anchor_tension)
        lst.append(t15)

        t14 = ([KEY_CONN], KEY_OUT_ANCHOR_UPLIFT_BOLT_NO, TYPE_OUT_DOCK, self.in_anchor)
        lst.append(t14)

        t15 = ([KEY_CONN], KEY_OUT_ANCHOR_UPLIFT_BOLT_NO, TYPE_OUT_LABEL, self.in_anchor)
        lst.append(t15)

        t14 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_TENSION_DEMAND_UPLIFT, TYPE_OUT_DOCK, self.in_anchor)
        lst.append(t14)

        t15 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_TENSION_DEMAND_UPLIFT, TYPE_OUT_LABEL, self.in_anchor)
        lst.append(t15)

        t16 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_LENGTH_UPLIFT, TYPE_OUT_DOCK, self.out_anchor_tension)
        lst.append(t16)

        t17 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_LENGTH_UPLIFT, TYPE_OUT_LABEL, self.out_anchor_tension)
        lst.append(t17)

        t18 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_TENSION_UPLIFT, TYPE_OUT_DOCK, self.out_anchor_tension)
        lst.append(t18)

        t19 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_TENSION_UPLIFT, TYPE_OUT_LABEL, self.out_anchor_tension)
        lst.append(t19)

        t20 = ([KEY_CONN], KEY_SECSIZE, TYPE_COMBOBOX, self.secsize_for_hollow)
        lst.append(t20)

        t20 = ([KEY_CONN], KEY_DIA_ANCHOR_ICF, TYPE_COMBOBOX_FREEZE, self.out_anchor_tension)
        lst.append(t20)

        t20 = ([KEY_CONN], KEY_GRD_ANCHOR_ICF, TYPE_COMBOBOX_FREEZE, self.out_anchor_tension)
        lst.append(t20)

        t21 = ([KEY_CONN], KEY_OUT_STIFFENER_PLATE_FLANGE, TYPE_OUT_DOCK, self.stiffener_flange)
        lst.append(t21)

        t22 = ([KEY_CONN], KEY_OUT_STIFFENER_PLATE_FLANGE, TYPE_OUT_LABEL, self.stiffener_flange)
        lst.append(t22)

        t23 = ([KEY_CONN], KEY_OUT_STIFFENER_PLATE_ALONG_WEB, TYPE_OUT_DOCK, self.stiffener_alongweb)
        lst.append(t23)

        t24 = ([KEY_CONN], KEY_OUT_STIFFENER_PLATE_ALONG_WEB, TYPE_OUT_LABEL, self.stiffener_alongweb)
        lst.append(t24)

        t25 = ([KEY_CONN], KEY_OUT_STIFFENER_PLATE_ACROSS_WEB, TYPE_OUT_DOCK, self.stiffener_acrossweb)
        lst.append(t25)

        t26 = ([KEY_CONN], KEY_OUT_STIFFENER_PLATE_ACROSS_WEB, TYPE_OUT_LABEL, self.stiffener_acrossweb)
        lst.append(t26)

        t27 = ([KEY_CONN], DISP_OUT_TITLE_STIFFENER_PLATE, TYPE_OUT_DOCK, self.stiffener_hollow_cs)
        lst.append(t27)

        t28 = ([KEY_CONN], DISP_OUT_TITLE_STIFFENER_PLATE, TYPE_OUT_LABEL, self.stiffener_hollow_cs)
        lst.append(t28)

        return lst

    @staticmethod
    def diam_bolt_customized():
        c = connectdb2()
        return c

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    def customized_input(self):

        list1 = []
        t1 = (KEY_DIA_ANCHOR_OCF, self.diam_bolt_customized, ['M8', 'M10', 'M12', 'M16'],
              "Anchor bolts M8, M10, M12 and M16 are not available to <br>"
              "perform design. Minimum recommended diameter by Osdag is <br> M20.")
        list1.append(t1)
        t2 = (KEY_GRD_ANCHOR_OCF, self.grdval_customized)
        list1.append(t2)
        t1 = (KEY_DIA_ANCHOR_ICF, self.diam_bolt_customized, ['M8', 'M10', 'M12', 'M16'],
              "Anchor bolts M8, M10, M12 and M16 are not available to <br>"
              "perform design. Minimum recommended diameter by Osdag is <br> M20.")
        list1.append(t1)
        t2 = (KEY_GRD_ANCHOR_ICF, self.grdval_customized)
        list1.append(t2)

        return list1

    def func_for_validation(self, design_dictionary):
        all_errors = []
        self.design_status = False
        flag = False
        option_list = self.input_values(self)
        missing_fields_list = []
        if design_dictionary[KEY_CONN] == 'Welded Column Base':
            design_dictionary[KEY_MOMENT_MAJOR] = 'Disabled'
            design_dictionary[KEY_MOMENT_MINOR] = 'Disabled'
        if design_dictionary[KEY_CONN] != 'Moment Base Plate' or design_dictionary[KEY_AXIAL_TENSION_BP] == '':
            design_dictionary[KEY_AXIAL_TENSION_BP] = 'Disabled'

        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    design_dictionary[option[0]] = '0'
            elif option[2] == TYPE_COMBOBOX and option[0] in [KEY_SECSIZE, KEY_GRD_FOOTING]:
                val = option[3]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        if flag:
            print(design_dictionary)
            self.bp_parameters(self, design_dictionary)
        else:
            return all_errors

    def input_dictionary_design_pref(self):

        design_input = []

        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, ['Label_8', KEY_SEC_MATERIAL])
        design_input.append(t1)

        t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY, 'Label_21'])
        design_input.append(t1)

        t2 = ("Base Plate", TYPE_COMBOBOX, [KEY_BASE_PLATE_MATERIAL])
        design_input.append(t2)

        t7 = ("Stiffener/Shear Key", TYPE_COMBOBOX, [KEY_ST_KEY_MATERIAL])
        design_input.append(t7)

        t3 = ("Anchor Bolt", TYPE_TEXTBOX,
              [KEY_DP_ANCHOR_BOLT_LENGTH_OCF, KEY_DP_ANCHOR_BOLT_LENGTH_ICF, KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF,
               KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF, KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF,
               KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF, KEY_DP_ANCHOR_BOLT_FRICTION, KEY_DP_ANCHOR_BOLT_TYPE_OCF,
               KEY_DP_ANCHOR_BOLT_TYPE_ICF])
        design_input.append(t3)

        t3 = ("Anchor Bolt", TYPE_COMBOBOX, [KEY_DP_ANCHOR_BOLT_HOLE_TYPE_OCF, KEY_DP_ANCHOR_BOLT_HOLE_TYPE_ICF, KEY_DP_ANCHOR_BOLT_GALVANIZED_OCF,
                                             KEY_DP_ANCHOR_BOLT_GALVANIZED_ICF])
        design_input.append(t3)

        t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        design_input.append(t4)

        t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        design_input.append(t4)

        t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD, KEY_DP_DESIGN_BASE_PLATE])
        design_input.append(t6)

        return design_input

    def input_dictionary_without_design_pref(self):

        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL, KEY_BASE_PLATE_MATERIAL, KEY_ST_KEY_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (KEY_TYP_ANCHOR, [KEY_DP_ANCHOR_BOLT_TYPE_OCF, KEY_DP_ANCHOR_BOLT_TYPE_ICF], 'Input Dock')
        design_input.append(t2)

        t3 = (None, [KEY_BASE_PLATE_FU, KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF, KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF,
                     KEY_BASE_PLATE_FY, KEY_ST_KEY_FU, KEY_ST_KEY_FY, KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF, KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF,
                     KEY_DP_ANCHOR_BOLT_LENGTH_OCF, KEY_DP_ANCHOR_BOLT_LENGTH_ICF, KEY_DP_ANCHOR_BOLT_HOLE_TYPE_OCF,
                     KEY_DP_ANCHOR_BOLT_HOLE_TYPE_ICF, KEY_DP_ANCHOR_BOLT_FRICTION, KEY_DP_WELD_FAB,
                     KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES,
                     KEY_DP_DESIGN_METHOD, KEY_DP_DESIGN_BASE_PLATE, KEY_DP_ANCHOR_BOLT_GALVANIZED_OCF, KEY_DP_ANCHOR_BOLT_GALVANIZED_ICF],
              KEY_BASE_PLATE_MATERIAL, KEY_ST_KEY_MATERIAL, '')
        design_input.append(t3)

        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            material = Material(design_dictionary[KEY_MATERIAL], 41)
            fu = material.fu
            fy = material.fy
        else:
            fu = ''
            fy = ''

        if design_dictionary[KEY_MATERIAL_ST_SK] != 'Select Material':
            material = Material(design_dictionary[KEY_MATERIAL_ST_SK], 41)
            fu_st_sk = material.fu
            fy_st_sk = material.fy
        else:
            fu_st_sk = ''
            fy_st_sk = ''

        length_out = str(self.anchor_length_provided_out) if self.design_status else str(0)
        length_in = str(self.anchor_length_provided_in) if self.design_status and \
                                                           (self.load_axial_tension > 0 or self.load_moment_minor > 0) else str(0)

        val = {KEY_BASE_PLATE_FU: str(fu),
               KEY_BASE_PLATE_FY: str(fy),
               KEY_ST_KEY_FU: str(fu_st_sk),
               KEY_ST_KEY_FY: str(fy_st_sk),
               KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF: str(fu),
               KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF: str(fu),
               KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF:
                   str(str(design_dictionary[KEY_DIA_ANCHOR_OCF][0]) + "X" + length_out + " IS5624 GALV"),
               KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF:
                   str(str(design_dictionary[KEY_DIA_ANCHOR_ICF][0]) + "X" + length_in + " IS5624 GALV"),
               KEY_DP_ANCHOR_BOLT_LENGTH_OCF: str(length_out),
               KEY_DP_ANCHOR_BOLT_LENGTH_ICF: str(length_in),
               KEY_DP_ANCHOR_BOLT_HOLE_TYPE_OCF: "Over-sized",
               KEY_DP_ANCHOR_BOLT_HOLE_TYPE_ICF: "Over-sized",
               KEY_DP_ANCHOR_BOLT_GALVANIZED_OCF: "Yes",
               KEY_DP_ANCHOR_BOLT_GALVANIZED_ICF: "Yes",
               KEY_DP_ANCHOR_BOLT_FRICTION: str(0.30),
               KEY_DP_WELD_FAB: KEY_DP_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "a - Sheared or hand flame cut",
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: "Yes",
               KEY_DP_DESIGN_METHOD: "Limit State Design",
               KEY_DP_DESIGN_BASE_PLATE: "Effective Area Method"
               }[key]

        return val

    def refresh_input_dock(self):

        add_buttons = []

        t1 = (KEY_DISP_COLSEC, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE, None, None, "Columns")
        add_buttons.append(t1)

        return add_buttons

    def edit_tabs(self):
        return []

    def tab_value_changed(self):

        change_tab = []

        t1 = (KEY_DISP_COLSEC, [KEY_SEC_MATERIAL], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX,
              self.get_fu_fy_I_section)
        change_tab.append(t1)

        t2 = ("Base Plate", [KEY_BASE_PLATE_MATERIAL], [KEY_BASE_PLATE_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40, KEY_CONNECTOR_FY_40],
              TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t2)

        t2 = ("Stiffener/Shear Key", [KEY_ST_KEY_MATERIAL], [KEY_ST_KEY_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40, KEY_CONNECTOR_FY_40],
              TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t2)

        t3 = ("Anchor Bolt", [KEY_DP_ANCHOR_BOLT_LENGTH_OCF], [KEY_DP_ANCHOR_BOLT_LENGTH_OCF], TYPE_OVERWRITE_VALIDATION,
              self.anchor_length_validation)
        change_tab.append(t3)

        t3 = ("Anchor Bolt", [KEY_DP_ANCHOR_BOLT_LENGTH_ICF], [KEY_DP_ANCHOR_BOLT_LENGTH_ICF], TYPE_OVERWRITE_VALIDATION,
              self.anchor_length_validation)
        change_tab.append(t3)

        t3 = ("Anchor Bolt", [KEY_DP_ANCHOR_BOLT_HOLE_TYPE_OCF], [KEY_DP_ANCHOR_BOLT_HOLE_TYPE_OCF],
              TYPE_OVERWRITE_VALIDATION, self.anchor_hole_type_validation)
        change_tab.append(t3)

        t3 = ("Anchor Bolt", [KEY_DP_ANCHOR_BOLT_HOLE_TYPE_ICF], [KEY_DP_ANCHOR_BOLT_HOLE_TYPE_ICF],
              TYPE_OVERWRITE_VALIDATION, self.anchor_hole_type_validation)
        change_tab.append(t3)

        t3 = ("Anchor Bolt", [KEY_DP_ANCHOR_BOLT_LENGTH_OCF, KEY_DP_ANCHOR_BOLT_GALVANIZED_OCF],
              [KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF], TYPE_TEXTBOX, self.anchor_bolt_designation)
        change_tab.append(t3)

        t3 = ("Anchor Bolt", [KEY_DP_ANCHOR_BOLT_LENGTH_ICF, KEY_DP_ANCHOR_BOLT_GALVANIZED_ICF],
              [KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF], TYPE_TEXTBOX, self.anchor_bolt_designation)
        change_tab.append(t3)

        t4 = (KEY_DISP_COLSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t4)

        t5 = (KEY_DISP_COLSEC, ['Label_HS_1', 'Label_HS_2', 'Label_HS_3'],
              ['Label_HS_11', 'Label_HS_12', 'Label_HS_13', 'Label_HS_14', 'Label_HS_15', 'Label_HS_16', 'Label_HS_17', 'Label_HS_18',
               'Label_HS_19', 'Label_HS_20', 'Label_HS_21', 'Label_HS_22', KEY_IMAGE], TYPE_TEXTBOX, self.get_SHS_RHS_properties)
        change_tab.append(t5)

        t6 = (KEY_DISP_COLSEC, ['Label_CHS_1', 'Label_CHS_2', 'Label_CHS_3'],
              ['Label_CHS_11', 'Label_CHS_12', 'Label_CHS_13', 'Label_HS_14', 'Label_HS_15', 'Label_HS_16', 'Label_21', 'Label_22',
               KEY_IMAGE], TYPE_TEXTBOX, self.get_CHS_properties)
        change_tab.append(t6)

        t6 = (KEY_DISP_COLSEC, [KEY_SECSIZE], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        return change_tab

    def anchor_bolt_designation(self):

        length = str(self[0])
        galvanized = str(self[1])
        input_dictionary = self[2]
        if not input_dictionary:
            d = ''
        else:
            d = input_dictionary[KEY_DIA_ANCHOR_OCF][0]
        new_des = str(d) + 'X'

        if galvanized == 'Yes':
            new_des = str(new_des) + str(length) + ' IS5624 ' + 'GALV'
        elif galvanized == 'No':
            new_des = str(new_des) + str(length) + ' IS5624'
        else:
            new_des = ''

        d = {KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF: str(new_des),
             KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF: str(new_des)}
        return d

    def anchor_length_validation(self):

        length = str(self[0])
        status = self[2]
        valid = True
        if length == "":
            return {"Validation": [valid, ""], KEY_DP_ANCHOR_BOLT_LENGTH_OCF: length,
                    KEY_DP_ANCHOR_BOLT_LENGTH_ICF: length}
        if status:
            if not float(self.anchor_length_min) <= float(length) <= float(self.anchor_length_max):
                valid = False
                length = self.anchor_length_provided_out

        d = {"Validation": [valid, "The selected value of anchor length exceeds the recommended limit [Reference: "
                                   "IS 5624:1993, Table 1]."],
             KEY_DP_ANCHOR_BOLT_LENGTH_OCF: str(length),
             KEY_DP_ANCHOR_BOLT_LENGTH_ICF: str(length)}
        return d

    def anchor_hole_type_validation(self):

        hole_type = str(self[0])
        if hole_type == 'Standard':
            return {"Validation":
                        [False, "Over-sized hole type for anchor is recommended by Osdag for Base Plate module."]
                    }
        else:
            return {"Validation": [True, ""]}

    def list_for_fu_fy_validation(self):

        fu_fy_list = []

        t1 = (KEY_SEC_MATERIAL, KEY_SEC_FU, KEY_SEC_FY)
        fu_fy_list.append(t1)

        t2 = (KEY_BASE_PLATE_MATERIAL, KEY_BASE_PLATE_FU, KEY_BASE_PLATE_FY)
        fu_fy_list.append(t2)

        t3 = (KEY_ST_KEY_MATERIAL, KEY_ST_KEY_FU, KEY_ST_KEY_FY)
        fu_fy_list.append(t3)

        return fu_fy_list

    # define design preferences
    def tab_list(self):

        # self.design_button_status = False

        tabs = []

        t0 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_section)
        tabs.append(t0)

        t5 = ("Base Plate", TYPE_TAB_2, self.tab_bp)
        tabs.append(t5)

        t6 = ("Stiffener/Shear Key", TYPE_TAB_2, self.tab_st_sk)
        tabs.append(t6)

        t1 = ("Anchor Bolt", TYPE_TAB_2, self.anchor_bolt_values)
        tabs.append(t1)

        t2 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t2)

        t3 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t3)

        t4 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t4)

        return tabs

    def anchor_bolt_values(self, input_dictionary):

        self.input_dictionary = input_dictionary

        values = {KEY_DP_ANCHOR_BOLT_LENGTH_OCF: '', KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF: '',
                  KEY_DP_ANCHOR_BOLT_TYPE_OCF: '', KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF: '',
                  KEY_DP_ANCHOR_BOLT_LENGTH_ICF: '', KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF: '',
                  KEY_DP_ANCHOR_BOLT_TYPE_ICF: '', KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF: ''
                  }
        if not input_dictionary or input_dictionary[KEY_SECSIZE] == 'Select Section' or \
                input_dictionary[KEY_MATERIAL] == 'Select Material':
            pass
        else:
            length_out = str(self.anchor_length_provided_out if self.design_status else 0)
            length_in = str(self.anchor_length_provided_in if self.design_status and self.load_axial_tension > 0 else 0)

            designation_ocf = str(input_dictionary[KEY_DIA_ANCHOR_OCF][0]) + "X" + length_out + " IS5624 GALV"
            designation_icf = str(input_dictionary[KEY_DIA_ANCHOR_ICF][0]) + "X" + length_in + " IS5624 GALV"
            anchor_type = input_dictionary[KEY_TYP_ANCHOR]
            fu = Material(input_dictionary[KEY_MATERIAL]).fu
            values[KEY_DP_ANCHOR_BOLT_LENGTH_OCF] = length_out
            values[KEY_DP_ANCHOR_BOLT_LENGTH_ICF] = length_in
            values[KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF] = designation_ocf
            values[KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF] = designation_icf
            values[KEY_DP_ANCHOR_BOLT_TYPE_OCF] = anchor_type
            values[KEY_DP_ANCHOR_BOLT_TYPE_ICF] = anchor_type
            values[KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF] = float(self.anchor_fu_fy_outside_flange[0]) if self.design_status else 0
            values[KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF] = float(self.anchor_fu_fy_inside_flange[0]) if self.design_status else 0

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        anchor_bolt = []

        t0 = (None, KEY_DISP_ANCHOR_OCF, TYPE_TITLE, None, None)
        anchor_bolt.append(t0)

        t1 = (KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None,
              str(values[KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF]))
        anchor_bolt.append(t1)

        t2 = (KEY_DP_ANCHOR_BOLT_TYPE_OCF, KEY_DISP_DP_ANCHOR_BOLT_TYPE, TYPE_TEXTBOX, None,
              str(values[KEY_DP_ANCHOR_BOLT_TYPE_OCF]))
        anchor_bolt.append(t2)

        t3 = (KEY_DP_ANCHOR_BOLT_GALVANIZED_OCF, KEY_DISP_DP_ANCHOR_BOLT_GALVANIZED, TYPE_COMBOBOX, ['Yes', 'No'], 'Yes')
        anchor_bolt.append(t3)

        t4 = (KEY_DP_ANCHOR_BOLT_HOLE_TYPE_OCF, KEY_DISP_DP_ANCHOR_BOLT_HOLE_TYPE, TYPE_COMBOBOX,
              ['Standard', 'Over-sized'], 'Over-sized')
        anchor_bolt.append(t4)

        t5 = (KEY_DP_ANCHOR_BOLT_LENGTH_OCF, KEY_DISP_DP_ANCHOR_BOLT_LENGTH, TYPE_TEXTBOX, None,
              values[KEY_DP_ANCHOR_BOLT_LENGTH_OCF])
        anchor_bolt.append(t5)

        t6 = (KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF, KEY_DISP_DP_ANCHOR_BOLT_MATERIAL_G_O, TYPE_TEXTBOX, None,
              str(values[KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF]))
        anchor_bolt.append(t6)

        t0 = (None, KEY_DISP_ANCHOR_ICF, TYPE_TITLE, None, None)
        anchor_bolt.append(t0)

        t1 = (KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None,
              str(values[KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF]))
        anchor_bolt.append(t1)

        t2 = (KEY_DP_ANCHOR_BOLT_TYPE_ICF, KEY_DISP_DP_ANCHOR_BOLT_TYPE, TYPE_TEXTBOX, None,
              str(values[KEY_DP_ANCHOR_BOLT_TYPE_ICF]))
        anchor_bolt.append(t2)

        t3 = (KEY_DP_ANCHOR_BOLT_GALVANIZED_ICF, KEY_DISP_DP_ANCHOR_BOLT_GALVANIZED, TYPE_COMBOBOX, ['Yes', 'No'], 'Yes')
        anchor_bolt.append(t3)

        t4 = (KEY_DP_ANCHOR_BOLT_HOLE_TYPE_ICF, KEY_DISP_DP_ANCHOR_BOLT_HOLE_TYPE, TYPE_COMBOBOX,
              ['Standard', 'Over-sized'], 'Over-sized')
        anchor_bolt.append(t4)

        t5 = (KEY_DP_ANCHOR_BOLT_LENGTH_ICF, KEY_DISP_DP_ANCHOR_BOLT_LENGTH, TYPE_TEXTBOX, None,
              values[KEY_DP_ANCHOR_BOLT_LENGTH_ICF])
        anchor_bolt.append(t5)

        t6 = (KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF, KEY_DISP_DP_ANCHOR_BOLT_MATERIAL_G_O, TYPE_TEXTBOX, None,
              str(values[KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF]))
        anchor_bolt.append(t6)

        t0 = (None, KEY_DISP_ANCHOR_GENERAL, TYPE_TITLE, None, None)
        anchor_bolt.append(t0)

        t7 = (KEY_DP_ANCHOR_BOLT_FRICTION, KEY_DISP_DP_ANCHOR_BOLT_FRICTION, TYPE_TEXTBOX, None, str(0.30))
        anchor_bolt.append(t7)

        return anchor_bolt

    def tab_bp(self, input_dictionary):

        if not input_dictionary or input_dictionary[KEY_MATERIAL] == 'Select Material':
            material_grade = ''
            fu = ''
            fy_20 = ''
            fy_20_40 = ''
            fy_40 = ''
        else:
            material_grade = input_dictionary[KEY_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy_20 = material_attributes.fy_20
            fy_20_40 = material_attributes.fy_20_40
            fy_40 = material_attributes.fy_40

        if KEY_BASE_PLATE_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_BASE_PLATE_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy_20 = material_attributes.fy_20
            fy_20_40 = material_attributes.fy_20_40
            fy_40 = material_attributes.fy_40

        tab_bp = []
        material = connectdb("Material", call_type="popup")
        t1 = (KEY_BASE_PLATE_MATERIAL, KEY_DISP_BASE_PLATE_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        tab_bp.append(t1)

        t2 = (KEY_BASE_PLATE_FU, KEY_DISP_BASE_PLATE_FU, TYPE_TEXTBOX, None, fu)
        tab_bp.append(t2)

        t3 = (KEY_CONNECTOR_FY_20, KEY_DISP_FY_20, TYPE_TEXTBOX, None, fy_20)
        tab_bp.append(t3)

        t3 = (KEY_CONNECTOR_FY_20_40, KEY_DISP_FY_20_40, TYPE_TEXTBOX, None, fy_20_40)
        tab_bp.append(t3)

        t3 = (KEY_CONNECTOR_FY_40, KEY_DISP_FY_40, TYPE_TEXTBOX, None, fy_40)
        tab_bp.append(t3)

        return tab_bp

    def tab_st_sk(self, input_dictionary):

        if not input_dictionary or input_dictionary[KEY_MATERIAL_ST_SK] == 'Select Material':
            material_grade = ''
            fu = ''
            fy_20 = ''
            fy_20_40 = ''
            fy_40 = ''
        else:
            material_grade = input_dictionary[KEY_MATERIAL_ST_SK]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy_20 = material_attributes.fy_20
            fy_20_40 = material_attributes.fy_20_40
            fy_40 = material_attributes.fy_40

        if KEY_ST_KEY_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_ST_KEY_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy_20 = material_attributes.fy_20
            fy_20_40 = material_attributes.fy_20_40
            fy_40 = material_attributes.fy_40

        tab_st_sk = []

        material = connectdb("Material", call_type="popup")
        t1 = (KEY_ST_KEY_MATERIAL, KEY_DISP_ST_SK_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        tab_st_sk.append(t1)

        t2 = (KEY_ST_KEY_FU, KEY_DISP_ST_SK_FU, TYPE_TEXTBOX, None, fu)
        tab_st_sk.append(t2)

        t3 = (KEY_CONNECTOR_FY_20, KEY_DISP_FY_20, TYPE_TEXTBOX, None, fy_20)
        tab_st_sk.append(t3)

        t3 = (KEY_CONNECTOR_FY_20_40, KEY_DISP_FY_20_40, TYPE_TEXTBOX, None, fy_20_40)
        tab_st_sk.append(t3)

        t3 = (KEY_CONNECTOR_FY_40, KEY_DISP_FY_40, TYPE_TEXTBOX, None, fy_40)
        tab_st_sk.append(t3)

        return tab_st_sk

    def detailing_values(self, input_dictionary):

        values = {KEY_DP_DETAILING_EDGE_TYPE: 'a - Sheared or hand flame cut',
                  KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'Yes'}

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        detailing = []

        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX, [
            'a - Sheared or hand flame cut', 'b - Rolled, machine-flame cut, sawn and planed'],
              values[KEY_DP_DETAILING_EDGE_TYPE])
        detailing.append(t1)

        t3 = (KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES, TYPE_COMBOBOX,
              ['No', 'Yes'], values[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        detailing.append(t3)

        t4 = ("textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION)
        detailing.append(t4)

        return detailing

    def design_values(self, input_dictionary):

        values = {KEY_DP_DESIGN_METHOD: 'Limit State Design', KEY_DP_DESIGN_BASE_PLATE: 'Effective Area Method'}

        for key in values.keys():
            if key in input_dictionary.keys():
                values[key] = input_dictionary[key]

        design = []

        t1 = (KEY_DP_DESIGN_METHOD, KEY_DISP_DP_DESIGN_METHOD, TYPE_COMBOBOX, [
            'Limit State Design', 'Limit State (Capacity based) Design', 'Working Stress Design'],
              values[KEY_DP_DESIGN_METHOD])
        design.append(t1)

        t2 = (KEY_DP_DESIGN_BASE_PLATE, KEY_DISP_DP_DESIGN_BASE_PLATE, TYPE_COMBOBOX, ['Effective Area Method'],
              values[KEY_DP_DESIGN_BASE_PLATE])
        design.append(t2)

        return design

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('Base Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Base Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Connector", bgcolor)

    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from beams and Beams table.
        """
        global logger
        red_list = red_list_function()
        if self.dp_column_designation in red_list or self.dp_column_designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    # set input values to perform design
    def bp_parameters(self, design_dictionary):
        """ Initialize variables to use in calculation from input dock and design preference UI.

        Args: design dictionary based on the user inputs from the GUI

        Returns: None
        """
        self.mainmodule = "Moment Connection"
        # attributes of input dock
        self.connectivity = str(design_dictionary[KEY_CONN])
        self.end_condition = str(design_dictionary[KEY_END_CONDITION])
        self.column_section = str(design_dictionary[KEY_SECSIZE])
        self.material = str(design_dictionary[KEY_MATERIAL])

        self.load_axial_compression = float(design_dictionary[KEY_AXIAL_BP])
        self.load_axial_compression = self.load_axial_compression * 10 ** 3  # N

        self.load_axial_tension = float(design_dictionary[KEY_AXIAL_TENSION_BP] if design_dictionary[KEY_AXIAL_TENSION_BP] != 'Disabled' else 0)
        self.load_axial_tension = self.load_axial_tension * 10 ** 3  # N

        self.load_shear_major = float(design_dictionary[KEY_SHEAR_MAJOR])  # shear force acting along the major axis (i.e. depth of the column)
        self.load_shear_major = self.load_shear_major * 10 ** 3  # N

        self.load_shear_minor = float(design_dictionary[KEY_SHEAR_MINOR])  # shear force acting along the minor axis (i.e. width of the column)
        self.load_shear_minor = self.load_shear_minor * 10 ** 3  # N

        self.load_moment_major = float(design_dictionary[KEY_MOMENT_MAJOR]
                                       if design_dictionary[KEY_MOMENT_MAJOR] != 'Disabled' else 0)  # bending moment acting about the major axis
        self.load_moment_major_report = round(self.load_moment_major, 2)  # for design report (actual input)
        self.load_moment_major = self.load_moment_major * 10 ** 6  # N-mm

        self.load_moment_minor = float(design_dictionary[KEY_MOMENT_MINOR]
                                       if design_dictionary[KEY_MOMENT_MINOR] != 'Disabled' else 0)  # bending moment acting about the minor axis
        self.load_moment_minor_report = round(self.load_moment_minor, 2)  # for design report (actual input)
        self.load_moment_minor = self.load_moment_minor * 10 ** 6  # N-mm

        # checking if the user input for minor axis moment exceeds the major axis moment (practically, it shouldn't)
        if self.load_moment_major < self.load_moment_minor:
            self.load_moment_major = self.load_moment_minor  # designing for maximum moment
        else:
            pass

        # outside flange
        self.anchor_dia_out = design_dictionary[KEY_DIA_ANCHOR_OCF]
        self.anchor_grade_out = design_dictionary[KEY_GRD_ANCHOR_OCF]

        # inside flange
        self.anchor_dia_in = design_dictionary[KEY_DIA_ANCHOR_ICF]
        self.anchor_grade_in = design_dictionary[KEY_GRD_ANCHOR_ICF]

        self.anchor_type = str(design_dictionary[KEY_TYP_ANCHOR])

        self.footing_grade = str(design_dictionary[KEY_GRD_FOOTING])

        self.weld_type = str(design_dictionary[KEY_WELD_TYPE])

        # attributes of design preferences

        # column
        self.dp_column_designation = str(design_dictionary[KEY_SECSIZE])
        self.dp_column_material = str(design_dictionary[KEY_SEC_MATERIAL])

        # base plate
        self.dp_bp_material = str(design_dictionary[KEY_BASE_PLATE_MATERIAL])
        self.base_plate = Material(material_grade=self.dp_bp_material, thickness=0)  # thk is initialised to 0
        self.base_plate.connect_to_database_to_get_fy_fu(self.dp_bp_material, 0)

        # stiffener plate/ shear key
        print(design_dictionary[KEY_ST_KEY_MATERIAL])
        self.dp_stif_key_material = str(design_dictionary[KEY_ST_KEY_MATERIAL])
        self.stiff_key = Material(material_grade=self.dp_stif_key_material, thickness=0)  # thk is initialised to 0
        self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, 0)

        # anchor bolt

        # outside flange
        self.dp_anchor_designation_out = str(design_dictionary[KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF])
        self.dp_anchor_type_out = str(design_dictionary[KEY_DP_ANCHOR_BOLT_TYPE_OCF])
        self.dp_anchor_galv_out = str(design_dictionary[KEY_DP_ANCHOR_BOLT_GALVANIZED_OCF])
        self.dp_anchor_hole_out = str(design_dictionary[KEY_DP_ANCHOR_BOLT_HOLE_TYPE_OCF])
        self.dp_anchor_length_out = float(design_dictionary[KEY_DP_ANCHOR_BOLT_LENGTH_OCF])
        self.dp_anchor_fu_overwrite_out = float(design_dictionary[KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF])

        # inside flange
        self.dp_anchor_designation_in = str(design_dictionary[KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF])
        self.dp_anchor_type_in = str(design_dictionary[KEY_DP_ANCHOR_BOLT_TYPE_ICF])
        self.dp_anchor_galv_in = str(design_dictionary[KEY_DP_ANCHOR_BOLT_GALVANIZED_ICF])
        self.dp_anchor_hole_in = str(design_dictionary[KEY_DP_ANCHOR_BOLT_HOLE_TYPE_ICF])
        self.dp_anchor_length_in = float(design_dictionary[KEY_DP_ANCHOR_BOLT_LENGTH_ICF])
        self.dp_anchor_fu_overwrite_in = float(design_dictionary[KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF])

        self.dp_anchor_friction = float(design_dictionary[KEY_DP_ANCHOR_BOLT_FRICTION] if
                                        design_dictionary[KEY_DP_ANCHOR_BOLT_FRICTION] != "" else 0.30)

        # weld
        self.dp_weld_fab = str(design_dictionary[KEY_DP_WELD_FAB])
        self.dp_weld_fu_overwrite = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])

        self.weld_bp = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O], type=design_dictionary[KEY_DP_WELD_TYPE],
                                          fabrication=design_dictionary[KEY_DP_WELD_FAB])

        self.weld_stiffener_flange = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O], type=design_dictionary[KEY_DP_WELD_TYPE],
                                          fabrication=design_dictionary[KEY_DP_WELD_FAB])
        self.weld_stiffener_web = self.weld_stiffener_flange
        self.weld_stiffener_across_web = self.weld_stiffener_flange
        self.weld_stiffener_key = self.weld_stiffener_flange

        self.weld_stiffener_SHS = self.weld_stiffener_flange
        self.weld_stiffener_RHS = self.weld_stiffener_flange
        self.weld_stiffener_CHS = self.weld_stiffener_flange

        # detailing
        self.dp_detail_edge_type = str(design_dictionary[KEY_DP_DETAILING_EDGE_TYPE])
        self.dp_detail_is_corrosive = str(design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        # method
        self.dp_design_method = str(design_dictionary[KEY_DP_DESIGN_METHOD])
        self.dp_bp_method = str(design_dictionary[KEY_DP_DESIGN_BASE_PLATE])

        # properties of the column sections

        # Rolled sections
        if self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                self.column_properties = SHS(designation=self.dp_column_designation, material_grade=self.dp_column_material)
                self.dp_column_type = "Rolled"
            elif self.dp_column_designation[1:4] == 'RHS':
                self.column_properties = RHS(designation=self.dp_column_designation, material_grade=self.dp_column_material)
                self.dp_column_type = "Rolled"
            elif self.dp_column_designation[1:4] == 'CHS':
                self.column_properties = CHS(designation=self.dp_column_designation, material_grade=self.dp_column_material)
                self.dp_column_type = "Rolled"
                self.column_Z_pz = self.column_properties.elast_sec_mod  # mm^3
                self.column_Z_py = self.column_properties.elast_sec_mod  # mm^3
                self.column_Z_ez = self.column_properties.elast_sec_mod  # mm^3
                self.column_Z_ey = self.column_properties.elast_sec_mod  # mm^3
        else:
            self.column_properties = Column(designation=self.dp_column_designation, material_grade=self.dp_column_material)
            self.dp_column_type = str(self.column_properties.type)
            self.column_Z_pz = self.column_properties.plast_sec_mod_z  # mm^3
            self.column_Z_py = self.column_properties.plast_sec_mod_y  # mm^3
            self.column_Z_ez = self.column_properties.elast_sec_mod_z  # mm^3
            self.column_Z_ey = self.column_properties.elast_sec_mod_y  # mm^3

        if self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] != 'CHS':
                self.column_Z_pz = self.column_properties.plast_sec_mod_z  # mm^3
                self.column_Z_py = self.column_properties.plast_sec_mod_y  # mm^3
                self.column_Z_ez = self.column_properties.elast_sec_mod_z  # mm^3
                self.column_Z_ey = self.column_properties.elast_sec_mod_y  # mm^3

        self.dp_column_source = str(self.column_properties.source)
        self.dp_column_fu = float(self.column_properties.fu)
        self.dp_column_fy = float(self.column_properties.fy)

        self.column_D = self.column_properties.depth  # mm
        self.column_bf = self.column_properties.flange_width  # mm
        self.column_tf = self.column_properties.flange_thickness  # mm
        self.column_tw = self.column_properties.web_thickness  # mm
        self.column_r1 = self.column_properties.root_radius  # mm
        self.column_r2 = self.column_properties.toe_radius  # mm
        self.column_area = self.column_properties.area  # mm2

        # other attributes

        self.anchors_outside_flange = 4
        self.anchors_inside_flange = 0
        self.anchor_nos_provided = self.anchors_outside_flange + self.anchors_inside_flange

        self.gamma_m0 = self.cl_5_4_1_Table_5["gamma_m0"]["yielding"]  # gamma_mo = 1.10
        self.gamma_m1 = self.cl_5_4_1_Table_5["gamma_m1"]["ultimate_stress"]  # gamma_m1 = 1.25
        self.gamma_mb = self.cl_5_4_1_Table_5["gamma_mb"][self.dp_weld_fab]  # gamma_mb = 1.25
        self.gamma_mw = self.cl_5_4_1_Table_5["gamma_mw"][self.dp_weld_fab]  # gamma_mw = 1.25 for 'Shop Weld' and 1.50 for 'Field Weld'
        self.safe = True
        self.min_width_check_Case1 = False

        self.stiffener_plt_thick_along_flange = 0.0
        self.stiffener_plt_thick_along_web = 0.0
        self.stiffener_plt_thick_across_web = 0.0
        self.stiffener_plt_height_along_flange = 0.0
        self.stiffener_plt_height_along_web = 0.0
        self.stiffener_plt_height_across_web = 0.0

        self.shear_on_stiffener_along_flange = 0.0
        self.shear_capa_stiffener_along_flange = 0.0
        self.moment_on_stiffener_along_flange = 0.0
        self.moment_capa_stiffener_along_flange = 0.0
        self.z_e_stiffener_along_flange = 0.0
        self.z_p_stiffener_along_flange = 0.0

        self.shear_on_stiffener_along_web = 0.0
        self.shear_capa_stiffener_along_web = 0.0
        self.moment_on_stiffener_along_web = 0.0
        self.moment_capa_stiffener_along_web = 0.0
        self.z_e_stiffener_along_web = 0.0
        self.z_p_stiffener_along_web = 0.0

        self.weld_size_flange = 0.0
        self.weld_size_web = 0.0
        self.gusset_along_flange = 'No'
        self.gusset_along_web = 'No'
        self.gusset_plate_length = 0.0
        self.stiffener_plate_length = 0.0
        self.total_eff_len_gusset_available = 0.0
        self.gusset_outstand_length = 0.0
        self.stiffener_outstand_length = 0.0
        self.gusset_fy = self.dp_column_fy
        self.stiffener_fy = 0.0
        self.epsilon = 1
        self.gusset_plate_thick = 0.0
        self.stiffener_plate_thick = 0.0
        self.gusset_plate_height = 0.0
        self.stiffener_plate_height = 0.0
        self.stiffener_plt_len_along_flange = 0.0
        self.stiffener_plt_len_along_web = 0.0
        self.stiffener_plt_len_across_web = 0.0

        self.weld_size_gusset = 0.0
        self.weld_size_stiffener = 0.0

        self.stiffener_plt_thick_across_web = 0
        self.shear_on_stiffener_across_web = 0
        self.shear_capa_stiffener_across_web = 0
        self.moment_on_stiffener_across_web = 0
        self.moment_capa_stiffener_across_web = 0

        self.plate_thk = 0
        self.plate_thk_provided = 0.0
        self.shear_key_thk = self.plate_thk_provided

        self.design_status_list = []
        self.load_status = True

        self.bp_analyses_parameters(self)
        print('bp_analyses_parameters done')
        self.bp_analyses(self)
        print('bp_analyses done')
        self.anchor_bolt_design(self)
        print('anchor_bolt_design done')
        self.design_weld(self)
        print('design_weld done')
        self.design_stiffeners(self)
        print('design_stiffeners done')
        self.additional_calculations(self)
        print('additional_calculations done')

    def bp_analyses_parameters(self):
        """ initialize detailing parameters like the end/edge/pitch/gauge distances, anchor bolt diameter and grade,
         length and width of the base plate. These parameters are used to run the first iteration of the analyses and improvise accordingly.

        Args:

        Returns:
        """
        # 1: Anchor Bolt Diameter:

        # initialise anchor bolt diameter and grade [Reference: based on design experience, field conditions  and sample calculations]
        # the following list of anchor diameters are neglected due its practical non acceptance/unavailability - 'M8', 'M10', 'M12', 'M16'

        # 1.1: Anchor outside flange
        self.anchor_dia_list_out = [int(a[-2:]) for a in self.anchor_dia_out]  # list of anchor dia provided as input, (int) [20, 24, 30, ...]

        sort_bolt = filter(lambda x: 'M20' <= x <= self.anchor_dia_out[-1], self.anchor_dia_out)

        for i in sort_bolt:
            self.anchor_bolt = i  # anchor dia provided (str)
            break

        # select anchor diameter
        self.anchor_dia_provided_outside_flange = self.table1(self.anchor_bolt)[0]  # mm, anchor dia provided (int)
        self.anchor_dia_outside_flange = self.anchor_dia_provided_outside_flange  # mm, anchor dia provided outside the column flange (int)
        self.anchor_area_outside_flange = self.bolt_area(self.anchor_dia_provided_outside_flange)  # list of areas [shank area, thread area] mm^2

        # 1.2: Anchor inside flange
        self.anchor_dia_list_in = [int(a[-2:]) for a in self.anchor_dia_in]  # list of anchor dia provided as input, (int) [20, 24, 30, ...]

        sort_bolt = filter(lambda x: 'M20' <= x <= self.anchor_dia_in[-1], self.anchor_dia_in)

        for i in sort_bolt:
            self.anchor_bolt = i  # anchor dia provided (str)
            break

        # select anchor diameter
        self.anchor_dia_provided_inside_flange = self.table1(self.anchor_bolt)[0]  # mm (int)
        self.anchor_dia_inside_flange = self.anchor_dia_provided_inside_flange  # mm (int)
        self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)  # list of areas [shank area, thread area] mm^2

        # 2: Anchor Hole Diameter:

        # 2.1: Outside flange
        self.anchor_hole_dia_out = self.cl_10_2_1_bolt_hole_size(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out)  # mm
        # 2.2: Inside flange
        self.anchor_hole_dia_in = self.cl_10_2_1_bolt_hole_size(self.anchor_dia_provided_inside_flange, self.dp_anchor_hole_in)  # mm

        # 3: Anchor Grade Selection:
        # assign anchor grade from the selected list
        # trying the design with the highest selected grade

        # 3.1: Anchor outside flange
        self.anchor_grade_list_out = self.anchor_grade_out
        self.anchor_grade_out = list(reversed(self.anchor_grade_out))
        for i in self.anchor_grade_out:
            self.anchor_grade_out = i  # outside flange
            break

        # strength values - [bolt_fu, bolt_fy] (list)
        self.anchor_fu_fy_outside_flange = self.get_bolt_fu_fy(self.anchor_grade_out, self.anchor_dia_provided_outside_flange)

        # 3.2: Anchor inside flange (Note: Grade - '3.6' is ignored due to its non availability)
        # self.anchor_grade_in = list(reversed(self.anchor_grade_in))
        self.anchor_grade_list_in = self.anchor_grade_in
        for i in self.anchor_grade_in:
            self.anchor_grade_in = i
            break

        self.anchor_grade_in = self.anchor_grade_in
        self.anchor_fu_fy_inside_flange = self.get_bolt_fu_fy(self.anchor_grade_in, self.anchor_dia_inside_flange)

        # 4: Number of Anchor Bolts:
        # anchor bolts outside the column flange (provided to resist tension due to moment or as minimum requirement)
        self.anchors_outside_flange = self.anchors_outside_flange  # minimum is 4 bolts

        # anchor bolts inside the column flange (provided to resist tension due to axial uplift force)
        self.anchors_inside_flange = self.anchors_inside_flange

        # total number of anchor bolts provided (bolts outside + inside, the column flange)
        self.anchor_nos_provided = self.anchors_outside_flange + self.anchors_inside_flange

        # 5: Plate Washer (square) Details for Anchor Bolts:

        # 5.1: Washer plate outside flange - dictionary {inner diameter, side dimension, washer thickness}
        self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_outside_flange)  # outside flange
        self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

        # 5.2: Washer plate inside flange
        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
            self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)
            self.plate_washer_dim_in = self.plate_washer_details_in['side']  # inside flange, mm

        # 6: Detailing Checks
        # Note: end distance is along the depth, whereas, the edge distance is along the flange width, of the column section

        # 6.1: Outside flange

        # 6.1.1: end distance [Reference: Clause 10.2.4.2 and 10.2.4.3, IS 800:2007]
        self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                   self.dp_detail_edge_type)
        self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)  # mm, adding 50% extra to end distance to incorporate weld etc.

        # checking if the provided end distance fits the washer with enough spacing
        if self.end_distance_out < self.plate_washer_dim_out:
            self.end_distance_out = self.plate_washer_dim_out

        # 6.1.2: edge distance [Reference: Clause 10.2.4.2 and 10.2.4.3, IS 800:2007]
        self.edge_distance_out = self.end_distance_out  # mm

        # 6.1.3: pitch and gauge distance [Reference: Clause 10.2.2 and 10.2.3.1, IS 800:2007]
        if self.anchors_outside_flange == 4 or 6:
            self.pitch_distance_out = 0.0
            self.gauge_distance_out = self.pitch_distance_out
        else:
            self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_outside_flange)  # mm
            self.gauge_distance_out = self.pitch_distance_out

        # 6.2: Inside flange

        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
            # 6.2.1: end distance [Reference: Clause 10.2.4.2 and 10.2.4.3, IS 800:2007]
            self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_inside_flange, self.dp_anchor_hole_in,
                                                                      self.dp_detail_edge_type)
            self.end_distance_in = round_up(1.5 * self.end_distance_in, 5)  # mm, adding 50% extra to end distance to incorporate weld etc.

            # checking if the provided end distance fits the washer with enough spacing
            if self.end_distance_in < self.plate_washer_dim_in:
                self.end_distance_in = self.plate_washer_dim_in

            # 6.2.2: edge distance [Reference: Clause 10.2.4.2 and 10.2.4.3, IS 800:2007]
            self.edge_distance_in = self.end_distance_in  # mm

            # 6.2.3: pitch and gauge distance [Reference: Clause 10.2.2 and 10.2.3.1, IS 800:2007]
            # Note: calculated when the bolts required inside flange is calculated in the respective method

        # 6: Base Plate Dimensions (trial)
        # minimum required dimensions (L X B) of the base plate [as per the detailing criteria]
        if self.connectivity == 'Hollow/Tubular Column Base':
            self.bp_length_min = self.column_D + (2 * (2 * self.end_distance_out))  # mm
            self.bp_width_min = self.column_bf + (2 * (2 * self.end_distance_out))  # mm
        else:
            self.bp_length_min = self.column_D + (2 * (2 * self.end_distance_out))  # mm
            self.bp_width_min = 0.85 * self.column_bf + (2 * (2 * self.edge_distance_out))  # mm

        # 7: Minimum Design Action

        # 7.1: Moment capacity of the column

        # 7.1.1: Section classification
        self.epsilon_col = round(math.sqrt(250 / self.dp_column_fy), 2)

        # flange b/t check
        if self.column_bf / self.column_tf > (42 * self.epsilon_col):
            self.col_classification = 'Semi-compact'
        else:
            self.col_classification = 'Compact'

        # web b/t check
        if self.connectivity == 'Hollow/Tubular Column Base':
            web_axial_load = self.column_area
        else:
            web_axial_load = ((((self.column_D - (2 * self.column_tf)) * self.column_tw) / self.column_area) * self.dp_column_fy) / self.gamma_m0  # N

        check = self.Table2_web_OfI_H_box_section((self.column_D - (2 * self.column_tf)), self.column_tw, self.dp_column_fy, web_axial_load,
                                                  load_type='Compression', section_class='Semi-compact')
        if (check[0] == 'Fail') or (check[1] == 'Fail') or (check[2] == 'Fail'):
            self.col_classification = 'Semi-compact'
        else:
            self.col_classification = 'Compact'

        # 7.1.2: Bending capacity
        if self.col_classification == 'Semi-compact':
            self.beta_b_z = self.column_Z_ez / self.column_Z_pz
            self.beta_b_y = self.column_Z_ey / self.column_Z_py

            self.M_dz = self.cl_8_2_1_2_design_moment_strength(self.column_Z_ez, self.column_Z_pz, self.dp_column_fy, section_class='semi-compact')
            self.M_dz = round(self.M_dz, 2)  # Nmm
            self.M_dy = self.cl_8_2_1_2_design_moment_strength(self.column_Z_ey, self.column_Z_py, self.dp_column_fy, section_class='semi-compact')
            self.M_dy = round(self.M_dy, 2)  # Nmm
        else:
            self.beta_b_z = 1.0
            self.beta_b_y = 1.0

            self.M_dz = self.cl_8_2_1_2_design_moment_strength(self.column_Z_ez, self.column_Z_pz, self.dp_column_fy, section_class='Compact')
            self.M_dz = round(self.M_dz, 2)  # Nmm
            self.M_dy = self.cl_8_2_1_2_design_moment_strength(self.column_Z_ey, self.column_Z_py, self.dp_column_fy, section_class='Compact')
            self.M_dy = round(self.M_dy, 2)  # Nmm

        # 7.2: Axial capacity
        self.column_axial_capacity = round(((self.column_area * self.dp_column_fy) / self.gamma_m0) * 1e-3, 2)  # kN
        self.load_axial_input = round(self.load_axial_compression * 1e-3, 2)  # N

        # Check for Axial compression
        if self.connectivity != 'Moment Base Plate':

            if self.load_axial_compression * 1e-3 < (0.3 * self.column_axial_capacity):
                logger.warning("[Minimum Design Action] The defined value of axial compression ({} kN) is less than 0.3 times the capacity of the "
                               "column section ({} kN) [Ref. Cl. 10.7, IS 800:2007]".
                               format(self.load_axial_compression * 1e-3, round(0.3 * self.column_axial_capacity, 2)))
                logger.info("Setting the value of axial compression equal to the minimum recommended value")

                self.load_axial_compression = round(0.3 * self.column_axial_capacity * 1e3, 2)  # N

            if self.load_axial_compression * 1e-3 > self.column_axial_capacity:
                self.design_status = False
                self.design_status_list.append(self.design_status)
                self.load_status = False
                logger.warning("[Maximum Design Action] The defined value of axial compression ({} kN) is greater than the capacity of the column "
                               "section ({} kN)".format(self.load_axial_compression * 1e-3, self.column_axial_capacity))
                logger.info("Setting the value of axial compression equal to the maximum capacity of the column section")

                self.load_axial_compression = self.column_axial_capacity * 1e3  # N

        # 7.3: Shear capacity
        self.column_shear_capacity = (((self.column_D - (2 * self.column_tf)) * self.column_tw) * self.dp_column_fy) / (math.sqrt(3) * self.gamma_m0)
        self.column_shear_capacity = round(0.60 * self.column_shear_capacity * 1e-3, 2)  # kN

        if (max(self.load_shear_major, self.load_shear_minor) * 1e-3) > self.column_shear_capacity:
            self.design_status = False
            self.design_status_list.append(self.design_status)
            self.load_status = False
            logger.warning("The defined value of horizontal shear force is greater than the shear capacity of the column "
                           "section ({} kN)".format(self.column_shear_capacity))
            logger.info("Reduce the load and re-design")

        # Interaction ratio check for loads
        if self.connectivity == 'Moment Base Plate':

            self.IR_axial = round((self.load_axial_compression * 1e-3) / self.column_axial_capacity, 3)
            self.IR_moment = round(self.load_moment_major / self.M_dz, 3)
            self.sum_IR = round(self.IR_axial + self.IR_moment, 3)

            # Minimum load consideration check
            if self.sum_IR <= 1.0:

                if self.IR_axial < 0.3 and self.IR_moment < 0.5:

                    logger.warning("The Load(s) defined is/are less than the minimum recommended value [Ref. IS 800:2007, Cl.10.7].")
                    logger.warning("[Minimum Factored Load] The external factored bending moment ({} kNm) is less than 0.5 times the plastic moment "
                                   "capacity of the column ({} kNm)".format(round(self.load_moment_major * 1e-6, 2),
                                                                            round(0.5 * self.M_dz * 1e-6, 2)))
                    self.load_moment_major = round(0.5 * self.M_dz, 2)  # Nmm
                    self.load_axial_compression = round(0.3 * self.column_axial_capacity * 1e3, 2)  # N
                    logger.info("The minimum factored bending moment should be at least 0.5 times the plastic moment capacity of the beam to "
                                "qualify the connection as rigid connection")
                    logger.info("The value of load(s) is/are set at minimum recommended value as per Cl.10.7")
                    logger.info("Designing the connection for a factored moment of {} kNm".format(round(self.load_moment_major * 1e-6, 2)))

                elif self.sum_IR <= 1.0 and self.IR_moment < 0.5:

                    if (0.5 - self.IR_moment) < (1 - self.sum_IR):
                        self.load_moment_major = round(0.5 * self.M_dz, 2)  # Nmm
                    else:
                        self.load_moment_major = round(self.load_moment_major + ((1 - self.sum_IR) * self.M_dz), 2)

                    self.load_axial_compression = round(self.load_axial_compression, 2)  # N

                    logger.warning("The Load(s) defined is/are less than the minimum recommended value [Ref. IS 800:2007, Cl.10.7].")
                    logger.warning("[Minimum Factored Load] The external factored bending moment ({} kNm) is less than 0.5 times the plastic moment "
                                   "capacity of the column ({} kNm)".format(round(2 * self.load_moment_major * 1e-6, 2),
                                                                            round(0.5 * self.M_dz * 1e-6, 2)))
                    logger.info("The minimum factored bending moment should be at least 0.5 times the plastic moment capacity of the beam to "
                                "qualify the connection as rigid connection")
                    logger.info("The value of load(s) is/are set at minimum recommended value as per Cl.10.7")
                    logger.info("Designing the connection for a factored moment of {} kNm".format(round(self.load_moment_major * 1e-6, 2)))

                elif self.sum_IR <= 1.0 and self.IR_axial < 0.3:

                    if (0.3 - self.IR_axial) < (1 - self.sum_IR):
                        self.load_axial_compression = round(0.3 * self.column_axial_capacity * 1e3, 2)  # N
                    else:
                        self.load_axial_compression = round(0.3 * self.column_axial_capacity * 1e3, 2)  # N

                    self.load_moment_major = round(self.load_moment_major, 2)  # Nmm

                    logger.warning("The Load(s) defined is/are less than the minimum recommended value [Ref. IS 800:2007, Cl.10.7]")
                    logger.info("The value of axial force is set at {} kN, as per the minimum recommended value by Cl.10.7".
                                format(round(0.3 * self.column_axial_capacity * 1e-3, 2)))
                else:
                    self.load_axial_compression = round(self.load_axial_compression, 2)
                    self.load_moment_major = round(self.load_moment_major, 2)

            else:
                self.load_moment_major = round(max(self.load_moment_major_report * 1e6, 0.5 * self.M_dz), 2)
                self.load_moment_major = round(min(self.load_moment_major, self.M_dz), 2)
                self.design_status = False
                self.design_status_list.append(self.design_status)
                self.load_status = False

                # Maximum moment check
                if self.load_moment_major > self.M_dz:
                    logger.error("[Maximum Factored Load] The external factored bending moment ({} kNm) is greater than the plastic moment "
                                 "capacity of the column ({} kNm)".format(round(self.load_moment_major_report * 1e-6, 2),
                                                                          round(self.M_dz * 1e-6, 2)))
                    logger.warning("The maximum moment carrying capacity of the column is {} kNm".format(round(self.M_dz * 1e-6, 2)))
                    logger.info("Reduce the factored bending moment and re-design")

                # Maximum axial force check
                if self.load_axial_compression * 1e-3 > self.column_axial_capacity:
                    logger.error("[Maximum Factored Load] The external factored axial force ({} kN) is greater than the axial capacity of "
                                 "the column ({} kN)".format(round(self.load_axial_compression * 1e-3, 2),
                                                             round(self.column_axial_capacity, 2)))

                    self.load_axial_compression = self.column_axial_capacity * 1e3  # N
                    logger.warning("The maximum axial capacity of the beam is {} kN".format(round(self.column_axial_capacity, 2)))
                    logger.info("Reduce the factored axial force and re-design")

                if self.load_axial_compression <= 0:
                    self.load_axial_compression = round(0.3 * self.column_axial_capacity * 1e3, 2)  # N

            # minor axis moment
            if self.load_moment_minor > 0:

                if self.load_moment_minor < (0.5 * self.M_dy):
                    logger.warning("[Minimum Moment] The external factored bending moment (acting along the minor (y-y) axis) is less than the "
                                   "minimum recommended design action effect [Reference: clause 10.7, IS 800:2007]")
                    logger.info("The minimum recommended design action effect for factored bending moment is 0.5 times the capacity of the column "
                                "(i.e. 0.5 X {}, kNm)".format(round(self.M_dy * 1e-6, 2)))
                    self.load_moment_minor = round(0.5 * self.M_dy, 2)
                    logger.info("The value of factored bending moment (M y-y) is set to {} kNm".format(round(self.load_moment_minor * 1e-6, 2)))

            if self.load_moment_minor > self.M_dy:
                self.design_status = False
                self.design_status_list.append(self.design_status)
                self.load_status = False

                logger.warning("[Maximum Moment] The external factored bending moment (acting along the major axis) is greater than the capacity of  "
                               "the column section")
                logger.info("The maximum moment is based on full capacity of the column")
                logger.info("The value of factored bending moment is set to be equal to the maximum capacity of the column {} kNm".
                            format(round(self.M_dy * 1e-6, 2)))

        # 8: Design Parameters

        # grout thickness fixed at 50 mm
        self.grout_thk = 50  # mm

    def bp_analyses(self):
        """ perform stress analyses of the base plate

        Args:

        Returns:

        # TODO: Write algorithm here
        """
        # bearing strength of concrete [Reference: Clause 7.4.1, IS 800:2007]
        self.bearing_strength_concrete = self.cl_7_4_1_bearing_strength_concrete(self.footing_grade)  # N/mm^2 or MPa

        # welded column base (pinned connection) and column base for hollow sections (fixed connection)
        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):

            # minimum required area for the base plate [bearing stress = axial force / area of the base]
            self.min_area_req = self.load_axial_compression / self.bearing_strength_concrete  # mm^2

            # calculate projection by the 'Effective Area Method' [Reference: Clause 7.4.1.1, IS 800:2007]
            # the calculated projection is added by half times the hole dia on each side to avoid stress concentration near holes
            if self.dp_column_type == 'Rolled' or 'Welded':

                if self.connectivity == 'Welded Column Base':
                    self.projection = self.calculate_c(self.column_bf, self.column_D, self.column_tw, self.column_tf, self.min_area_req,
                                                       self.anchor_hole_dia_out, section_type='I-section')  # mm
                    self.projection_dr = round(self.projection, 2)  # for design report
                    self.projection = round_up(self.projection_dr, 5)
                else:
                    if self.dp_column_designation[1:4] == 'CHS':
                        self.projection = self.calculate_c(0, self.column_D, 0, 0, self.min_area_req, self.anchor_hole_dia_out,
                                                           section_type='CHS')  # mm
                        self.projection_dr = round(self.projection, 2)  # for design report
                        self.projection = round_up(self.projection_dr, 5)
                    else:
                        self.projection = self.calculate_c(self.column_bf, self.column_D, 0, 0, self.min_area_req, self.anchor_hole_dia_out,
                                                           section_type='SHS')  # mm
                        self.projection_dr = round(self.projection, 2)  # for design report
                        self.projection = round_up(self.projection_dr, 5)

            if self.projection <= 0 or self.end_distance_out:
                logger.warning(": [Analysis Error] The value of the projection (c) as per the Effective Area Method is {} mm [Reference:"
                             " Clause 7.4.1.1, IS 800: 2007]".format(self.projection))
                logger.warning(": [Analysis Error] The computed value of c should at least be equal to the end/edge distance")
                logger.info(": [Analysis Error] Setting the value of c equal to end/edge distance")

            self.projection = max(self.projection, self.end_distance_out)  # projection should at-least be equal to the end distance

            # updating the length and the width by incorporating the value of projection
            self.bp_length_provided = self.column_D + (2 * self.projection) + (2 * self.end_distance_out)  # mm
            self.bp_width_provided = self.column_bf + (2 * self.projection) + (2 * self.edge_distance_out)  # mm

            # check for the provided area against the minimum required area
            self.bp_area_provided = self.bp_length_provided * self.bp_width_provided  # mm^2

            # checking if the provided dimensions (length and width) are sufficient
            bp_dimensions = [self.bp_length_provided, self.bp_width_provided]

            n = 1
            while self.bp_area_provided < self.min_area_req:
                bp_update_dimensions = [bp_dimensions[-2], bp_dimensions[-1]]

                for i in bp_update_dimensions:
                    i += 25
                    bp_dimensions.append(i)
                    i += 1

                self.bp_area_provided = bp_dimensions[-2] * bp_dimensions[-1]  # mm^2, area according to the updated length and width
                n += 1

            self.bp_length_provided = bp_dimensions[-2]  # mm, updated length if while loop is True
            self.bp_width_provided = bp_dimensions[-1]  # mm, updated width if while loop is True
            self.bp_area_provided = self.bp_length_provided * self.bp_width_provided  # mm^2, update area if while loop is True

            # actual bearing pressure acting on the provided area of the base plate
            self.w = round((self.load_axial_compression / self.bp_area_provided), 2)  # N/mm^2 (MPa)
            self.max_bearing_stress = self.w  # for design report

            # design of plate thickness
            # thickness of the base plate [Reference: Clause 7.4.3.1, IS 800:2007]
            self.plate_thk = self.projection * (math.sqrt((2.5 * self.w * self.gamma_m0) / self.base_plate.fy))  # mm
            self.plate_thk = round(self.plate_thk, 2)

            self.tension_demand_anchor = 0  # there will be no tension acting on the anchor bolts in this case
            # calculating tension capacity of the anchor bolt
            self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                          self.anchor_fu_fy_outside_flange[1],
                                                                                          self.anchor_area_outside_flange[0],
                                                                                          self.anchor_area_outside_flange[1],
                                                                                          safety_factor_parameter=self.dp_weld_fab)  # N
            self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

        elif self.connectivity == 'Moment Base Plate':

            # calculate eccentricity
            self.eccentricity_zz = round((self.load_moment_major / self.load_axial_compression), 2)  # mm, eccentricity about major (z-z) axis

            # Major axis
            # Defining cases: Case 1: e <= L/6        (compression throughout the BP)
            #                 Case 2: L/6 < e < L/3   (compression throughout + moderate tension/uplift in the anchor bolts)
            #                 Case 3: e >= L/3        (compression + high tension/uplift in the anchor bolts)

            if self.eccentricity_zz <= self.bp_length_min / 6:  # Case 1
                self.moment_bp_case = 'Case1'

                logger.info("[Base Plate Type] The value of eccentricity about the major axis is {} mm".format(round_down(self.eccentricity_zz, 2)))
                logger.info("Eccentricity is less than {} mm (L/6)".format(round(self.bp_length_min / 6, 2)))
                logger.info("Case 1: The base plate is purely under compression/bearing over it's length with no tension force acting on the anchor "
                            "bolts outside column flange on either side")

                # fixing length and width of the base plate
                self.width_min_req = round(2 * self.load_axial_compression / (self.bp_length_min * self.bearing_strength_concrete), 2)  # mm
                if self.width_min_req > self.bp_width_min:
                    self.min_width_check_Case1 = True
                else:
                    self.min_width_check_Case1 = False

                self.bp_length_provided = max(self.bp_length_min, round_up(self.width_min_req, 5))  # mm, assigning maximum dimension to length
                self.bp_width_provided = min(self.bp_length_min, round_up(self.width_min_req, 5))  # mm, assigning minimum dimension to width
                self.bp_area_provided = self.bp_length_provided * self.bp_width_provided  # mm^2

                # elastic section modulus of plate (BL^2/6)
                self.ze_zz = (self.bp_width_provided * self.bp_length_provided ** 2) / 6  # mm^3

                # calculating the maximum and minimum bending stresses
                self.sigma_max_zz = (self.load_axial_compression / self.bp_area_provided) + (self.load_moment_major / self.ze_zz)  # N/mm^2
                self.sigma_min_zz = (self.load_axial_compression / self.bp_area_provided) - (self.load_moment_major / self.ze_zz)  # N/mm^2

                self.max_bearing_stress = round(self.sigma_max_zz, 2)

                # calculating moment at the critical section

                # Assumption: the critical section (critical_xx) acts at a distance of 0.95 times the column depth, along the depth
                self.critical_xx = round((self.bp_length_provided - 0.95 * self.column_D) / 2, 2)  # mm
                self.sigma_xx = (self.sigma_max_zz - self.sigma_min_zz) * (self.bp_length_provided - self.critical_xx) / self.bp_length_provided
                self.sigma_xx = self.sigma_xx + self.sigma_min_zz  # N/mm^2, bending stress at the critical section

                self.critical_M_xx = (self.sigma_xx * (self.critical_xx ** 2 / 2) * self.bp_width_provided) + \
                                     (0.5 * self.critical_xx * (self.sigma_max_zz - self.sigma_xx) * (2 / 3) * self.critical_xx
                                      * self.bp_width_provided)
                # N-mm, bending moment at critical section (1 is the cantilever strip of unit thk)

                # equating critical moment with critical moment to compute the required minimum plate thickness
                # Assumption: The bending capacity of the plate is (M_d = 1.5*fy*Z_e/gamma_m0) [Reference: Clause 8.2.1.2, IS 800:2007]
                # Assumption: Z_e of the plate is = b*tp^2 / 6, where b = W for a cantilever strip of unit dimension

                self.plate_thk = math.sqrt((self.critical_M_xx * self.gamma_m0 * 6) / (1.5 * self.base_plate.fy * self.bp_width_provided))  # mm
                self.plate_thk = round(self.plate_thk, 2)

                # plate fy check
                # if self.plate_thk >= 20:
                #     self.base_plate.connect_to_database_to_get_fy_fu(self.dp_bp_material, self.plate_thk)  # update fy
                #     # update plate thk
                #     # self.plate_thk = math.sqrt((self.critical_M_xx * self.gamma_m0 * 6) / (1.5 * self.base_plate.fy * self.bp_width_provided))  # mm
                #     # self.plate_thk = round(self.plate_thk, 2)

                self.tension_demand_anchor = 0  # there will be no tension acting on the anchor bolts in this case
                # calculating tension capacity of the anchor bolt
                self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                              self.anchor_fu_fy_outside_flange[1],
                                                                                              self.anchor_area_outside_flange[0],
                                                                                              self.anchor_area_outside_flange[1],
                                                                                              safety_factor_parameter=self.dp_weld_fab)  # N
                self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

            else:  # Case 2 and Case 3
                self.moment_bp_case = 'Case2&3'

                if self.eccentricity_zz >= (self.bp_length_min / 3):  # Case 3
                    self.moment_bp_case = 'Case3'
                    logger.info("[Base Plate Type] The value of eccentricity about the major axis is {} mm".format(round_down(self.eccentricity_zz, 2)))
                    logger.info("Eccentricity is greater than {} (L/3) mm".format(round(self.bp_length_min / 3, 2)))
                    logger.info("Case 3: A smaller part of the base plate is under pure compression/bearing with a large tension/uplift force being "
                                "transferred through the anchor bolts outside column flange on the tension side")

                else:  # (self.eccentricity_zz > (self.bp_length_min / 6)) or (self.eccentricity_zz < (self.bp_length_min / 3))
                    self.moment_bp_case = 'Case2'
                    logger.info("[Base Plate Type] The value of eccentricity about the major axis is {} mm".format(round_down(self.eccentricity_zz, 2)))
                    logger.info("Eccentricity is greater than {} (L/6) mm but less than {} (L/3) mm".format(round(self.bp_length_min / 6, 2),
                                                                                                            round(self.bp_length_min / 3, 2)))
                    logger.info("Case 2: A larger part of the base plate is under compression/bearing with a small to moderate tension/uplift force "
                                "being transferred through the anchor bolts outside column flange on the tension side")

                # fixing length and width of the base plate
                # the second term assumes a minimum length of stiffener as 100 mm to compute the trial size
                self.bp_length_provided = max(self.bp_length_min, round_up(self.column_D + (2 * 100), 5))
                self.bp_width_provided = max(self.bp_width_min, round_up(self.column_bf + (2 * 100), 5))

                # calculating the distance (y) which lies under compression
                # Reference: Omer Blodgett, Column Bases, section 3.3, equation 13

                self.n = 2 * 10 ** 5 / (5000 * math.sqrt(self.cl_7_4_1_bearing_strength_concrete(self.footing_grade) / 0.45))
                self.n = round(self.n, 3)
                self.anchor_area_tension = self.anchor_area_outside_flange[0] * (self.anchor_nos_provided / 2)  # mm^2, area of anchor under tension
                # TODO: update f value for 4 and 6 bolts (should be column centre to the centre of the bolt group)
                self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm

                self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2

                # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                r_1 = roots[0]
                r_2 = roots[1]
                r_3 = roots[2]
                r = max(r_1, r_2, r_3)
                r = r.real  # separating the imaginary part

                self.y = round(r)  # mm

                # finding maximum tension in the anchor bolts
                self.tension_demand_anchor = (- self.load_axial_compression) * (
                            ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                            ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                if self.tension_demand_anchor < 0:
                    self.tension_demand_anchor = (- 1 * self.tension_demand_anchor)

                self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                # design of the anchor bolt(s) required to resist tension due to bending moment only
                self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                              self.anchor_fu_fy_outside_flange[1],
                                                                                              self.anchor_area_outside_flange[0],
                                                                                              self.anchor_area_outside_flange[1],
                                                                                              safety_factor_parameter=self.dp_weld_fab)  # N
                self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                # design number of anchor bolts required to resist tension (bolts outside the column flange)
                # Assumption: The minimum number of anchor bolts is 2 (on each side), for stability purpose.
                self.anchors_outside_flange = max(self.tension_demand_anchor / self.tension_capacity_anchor, 2)  # each side

                # if the number of bolts outside the flange exceeds 2, 3, 4 or 6 in number, then the loop will check
                # for a combination of less number- high diameter bolt from the given list of anchor diameters by the user.

                # Check 1: 2 bolts with higher diameter
                if self.anchors_outside_flange > 2:
                    check1 = 'Yes'

                    n = 1
                    while self.anchors_outside_flange > 2:
                        bolt_list = self.anchor_dia_out[n - 1:]

                        for i in bolt_list:
                            self.anchor_dia_provided_outside_flange = i
                            break

                        self.anchor_area_outside_flange = self.bolt_area(self.table1(self.anchor_dia_provided_outside_flange)[0])
                        self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                                      self.anchor_fu_fy_outside_flange[1],
                                                                                                      self.anchor_area_outside_flange[0],
                                                                                                      self.anchor_area_outside_flange[1],
                                                                                                      safety_factor_parameter=self.dp_weld_fab)  # N
                        self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                        self.anchors_outside_flange = max(self.tension_demand_anchor / self.tension_capacity_anchor, 2)
                        n += 1

                        self.anchor_dia_provided_outside_flange = self.table1(i)[0]  # updating the initialised anchor diameter

                        if ((n + 1) >= len(self.anchor_dia_out)) and (self.anchors_outside_flange > 2):
                            logger.warning("[Anchor Bolt] The design of anchor bolts for resisting tension/uplift force is not satisfied with 4 "
                                           "anchor bolts of {} mm diameter".format(self.anchor_dia_provided_outside_flange))
                            logger.info("Re-designing the connection with 6 anchor bolts of same diameter")
                            break
                else:
                    check1 = 'N/A'

                # Check 2: Checking for 3 bolts with 1. initial diameter input 2. every possible anchor diameter (if 1 fails)
                if (self.anchors_outside_flange > 2) and (check1 == 'Yes'):
                    check2 = 'Yes'

                    self.anchors_outside_flange = 3  # trying with 3 bolts
                    self.anchor_dia_provided_outside_flange = self.anchor_dia_outside_flange  # starting check with the initial provided diameter

                    self.anchor_area_outside_flange = self.bolt_area(self.anchor_dia_provided_outside_flange)
                    self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                                  self.anchor_fu_fy_outside_flange[1],
                                                                                                  self.anchor_area_outside_flange[0],
                                                                                                  self.anchor_area_outside_flange[1],
                                                                                                  safety_factor_parameter=self.dp_weld_fab)  # N
                    self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                    self.anchors_outside_flange = max(self.tension_demand_anchor / self.tension_capacity_anchor, 3)

                    # re-checking the detailing check with 3 bolts
                    self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                    self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                    self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                               self.dp_detail_edge_type)

                    if self.end_distance_out < self.plate_washer_dim_out:
                        self.end_distance_out = self.plate_washer_dim_out

                    self.edge_distance_out = self.end_distance_out

                    if (0.85 * self.column_bf) < (2 * self.edge_distance_out):
                        detailing_check = 'Fail'
                    else:
                        detailing_check = 'Pass'

                    # if the check fails with 3 bolts and initial diameter, checking for 3 bolts with higher possible diameters
                    # if the detailing check Passes
                    if (self.anchors_outside_flange > 3) and (detailing_check == 'Pass'):

                        n = 1
                        while (self.anchors_outside_flange > 3) and (detailing_check == 'Pass'):
                            bolt_list = self.anchor_dia_out[n - 1:]

                            for i in bolt_list:
                                self.anchor_dia_provided_outside_flange = i
                                break

                            self.anchor_area_outside_flange = self.bolt_area(self.table1(self.anchor_dia_provided_outside_flange)[0])
                            self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                                          self.anchor_fu_fy_outside_flange[1],
                                                                                                          self.anchor_area_outside_flange[0],
                                                                                                          self.anchor_area_outside_flange[1],
                                                                                                          safety_factor_parameter=self.dp_weld_fab)  # N
                            self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                            self.anchors_outside_flange = max(self.tension_demand_anchor / self.tension_capacity_anchor, 3)
                            n += 1

                            self.anchor_dia_provided_outside_flange = self.table1(i)[0]  # updating the initialised anchor diameter

                            # re-checking the detailing check with 3 bolts
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)

                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out

                            self.edge_distance_out = self.end_distance_out

                            if (0.85 * self.column_bf) < (2 * self.edge_distance_out):
                                detailing_check = 'Fail'
                                logger.warning("[Detailing Check] The detailing checks are not satisfied with 6 anchor bolts of {} mm diameter".
                                               format(self.anchor_dia_provided_outside_flange))
                                logger.info("Re-designing the connection with 8 anchor bolts")
                            else:
                                detailing_check = 'Pass'

                            if ((n + 1) >= len(self.anchor_dia_out)) and (self.anchors_outside_flange > 3):
                                logger.warning("[Anchor Bolt] The design of anchor bolts for resisting tension/uplift force is not satisfied with 6 "
                                               "anchor bolts of higher diameter and grade combination")
                                logger.info("Re-designing the connection with 8 anchor bolts")
                                break
                else:
                    check2 = 'N/A'

                # Check 3: Checking for 4 bolts with 1. initial diameter input 2. every possible anchor diameter (if 1 fails)
                if (self.anchors_outside_flange > 3) and (check2 == 'Yes'):
                    check3 = 'Yes'

                    self.anchors_outside_flange = 4  # trying with 4 bolts
                    self.anchor_dia_provided_outside_flange = self.anchor_dia_outside_flange  # starting check with the initial provided diameter

                    self.anchor_area_outside_flange = self.bolt_area(self.anchor_dia_provided_outside_flange)
                    self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                                  self.anchor_fu_fy_outside_flange[1],
                                                                                                  self.anchor_area_outside_flange[0],
                                                                                                  self.anchor_area_outside_flange[1],
                                                                                                  safety_factor_parameter=self.dp_weld_fab)  # N
                    self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                    self.anchors_outside_flange = max(self.tension_demand_anchor / self.tension_capacity_anchor, 4)

                    # if the check fails with 4 bolts and initial diameter, checking for 4 bolts with higher possible diameters
                    if self.anchors_outside_flange > 4:

                        n = 1
                        while self.anchors_outside_flange > 4:
                            bolt_list = self.anchor_dia_out[n - 1:]

                            for i in bolt_list:
                                self.anchor_dia_provided_outside_flange = i
                                break

                            self.anchor_area_outside_flange = self.bolt_area(self.table1(self.anchor_dia_provided_outside_flange)[0])
                            self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                                          self.anchor_fu_fy_outside_flange[1],
                                                                                                          self.anchor_area_outside_flange[0],
                                                                                                          self.anchor_area_outside_flange[1],
                                                                                                          safety_factor_parameter=self.dp_weld_fab)  # N
                            self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                            self.anchors_outside_flange = max(self.tension_demand_anchor / self.tension_capacity_anchor, 4)
                            n += 1

                            self.anchor_dia_provided_outside_flange = self.table1(i)[0]  # updating the initialised anchor diameter

                            if ((n + 1) >= len(self.anchor_dia_out)) and (self.anchors_outside_flange > 4):
                                logger.warning("[Anchor Bolt] The design of anchor bolts for resisting tension/uplift force is not satisfied with 8 "
                                               "anchor bolts of {} mm diameter".format(self.anchor_dia_provided_outside_flange))
                                logger.info("Re-designing the connection with 12 anchor bolts of same diameter")
                                break
                else:
                    check3 = 'N/A'

                # Check 4: Checking for 6 bolts with 1. initial diameter input 2. every possible anchor diameter (if 1 fails)
                if (self.anchors_outside_flange > 4) and (check3 == 'Yes'):
                    check4 = 'Yes'

                    self.anchors_outside_flange = 6  # trying with 6 bolts
                    self.anchor_dia_provided_outside_flange = self.anchor_dia_outside_flange  # starting check with the initial provided diameter

                    self.anchor_area_outside_flange = self.bolt_area(self.anchor_dia_provided_outside_flange)
                    self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                                  self.anchor_fu_fy_outside_flange[1],
                                                                                                  self.anchor_area_outside_flange[0],
                                                                                                  self.anchor_area_outside_flange[1],
                                                                                                  safety_factor_parameter=self.dp_weld_fab)  # N
                    self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                    self.anchors_outside_flange = max(self.tension_demand_anchor / self.tension_capacity_anchor, 6)

                    # re-checking the detailing check with 6 bolts
                    self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                    self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                    self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                               self.dp_detail_edge_type)

                    if self.end_distance_out < self.plate_washer_dim_out:
                        self.end_distance_out = self.plate_washer_dim_out

                    self.edge_distance_out = self.end_distance_out

                    if (0.85 * self.column_bf) < (2 * self.edge_distance_out):
                        detailing_check = 'Fail'
                        logger.warning("[Detailing Check] The detailing checks are not satisfied with 12 anchor bolts of {} mm diameter".
                                       format(self.anchor_dia_provided_outside_flange))
                        logger.info("Re-designing the connection with 12 anchor bolts of higher diameter")
                    else:
                        detailing_check = 'Pass'

                    # if the check fails with 6 bolts and initial diameter, checking for 6 bolts with higher possible diameters
                    if (self.anchors_outside_flange > 6) and (detailing_check == 'Pass'):

                        n = 1
                        while (self.anchors_outside_flange > 6) and (detailing_check == 'Pass'):
                            bolt_list = self.anchor_dia_out[n - 1:]

                            for i in bolt_list:
                                self.anchor_dia_provided_outside_flange = i
                                break

                            self.anchor_area_outside_flange = self.bolt_area(self.table1(self.anchor_dia_provided_outside_flange)[0])
                            self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                                          self.anchor_fu_fy_outside_flange[1],
                                                                                                          self.anchor_area_outside_flange[0],
                                                                                                          self.anchor_area_outside_flange[1],
                                                                                                          safety_factor_parameter=self.dp_weld_fab)  # N
                            self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                            self.anchors_outside_flange = max(self.tension_demand_anchor / self.tension_capacity_anchor, 6)
                            n += 1

                            self.anchor_dia_provided_outside_flange = self.table1(i)[0]  # updating the initialised anchor diameter

                            # re-checking the detailing check with 6 bolts
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)

                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out

                            self.edge_distance_out = self.end_distance_out

                            if (0.85 * self.column_bf) < (2 * self.edge_distance_out):
                                detailing_check = 'Fail'
                                self.safe = False
                                logger.warning("[Detailing Check] The detailing checks are not satisfied with 12 anchor bolts of {} mm diameter".
                                               format(self.anchor_dia_provided_outside_flange))
                                logger.error("[Anchor Bolt] The design of anchor bolts for resisting tension/uplift force is not satisfied with 12 "
                                             "anchor bolts of higher diameter and grade combination")
                                logger.info("Provision for design with more than 12 anchor bolts is not available in this version of Osdag")
                                logger.info("Cannot compute")

                            else:
                                detailing_check = 'Pass'

                            if ((n + 1) >= len(self.anchor_dia_out)) and (self.anchors_outside_flange > 6):
                                self.safe = False
                                logger.error("[Anchor Bolt] The design of anchor bolts for resisting tension/uplift force is not satisfied with 12 "
                                               "anchor bolts of higher diameter and grade combination")
                                logger.info("Provision for design with more than 12 anchor bolts is not available in this version of Osdag")
                                logger.info("Cannot compute")
                                break
                else:
                    check4 = 'N/A'

                if self.anchors_outside_flange > 6:
                    self.design_status_anchors_outside = False
                    logger.error("[Anchor Bolt] The design of anchor bolts for resisting tension/uplift force is not satisfied with 12 "
                                 "anchor bolts of higher diameter and grade combination")
                    logger.info("Provision for design with more than 12 anchor bolts is not available in this version of Osdag")
                    logger.info("Cannot compute")
                else:
                    # updating the end/edge and pitch/gauge distance (if the anchor diameter or numbers is improvised in the above loop(s))
                    self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                               self.dp_detail_edge_type)
                    self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)

                    self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                    self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                    if self.end_distance_out < self.plate_washer_dim_out:
                        self.end_distance_out = self.plate_washer_dim_out

                    self.edge_distance_out = self.end_distance_out

                    # fixing bp size and parameters calculations after the iteration checks
                    if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                        self.bolt_columns_outside_flange = 1

                        # updating the bp dimension
                        self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                        self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                        self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                        self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                    elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                        self.bolt_columns_outside_flange = 2

                        # provide pitch and gauge
                        self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_outside_flange)  # mm
                        self.pitch_distance_out = 1.5 * self.pitch_distance_out

                        if self.pitch_distance_out < self.plate_washer_dim_out:
                            self.pitch_distance_out = self.plate_washer_dim_out

                        self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                        self.gauge_distance_out = self.pitch_distance_out

                        # updating the bp dimension
                        self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out), 5)  # mm
                        self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                        self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                        self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                    # recalculating the parameters for bearing check
                    self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                    self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm

                    self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                    self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                    self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2

                    # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                    roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                    r_1 = roots[0]
                    r_2 = roots[1]
                    r_3 = roots[2]
                    r = max(r_1, r_2, r_3)
                    r = r.real  # separating the imaginary part

                    self.y = round(r)  # mm

                    self.tension_demand_anchor = (- self.load_axial_compression) * (
                            ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                            ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                    if self.tension_demand_anchor < 0:
                        self.tension_demand_anchor = (- 1 * self.tension_demand_anchor)

                    self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                # computing the actual bearing stress at the compression side
                # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                          ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                self.max_bearing_stress = abs(self.max_bearing_stress)

                if self.max_bearing_stress > self.bearing_strength_concrete:
                    bearing_stress_check = 'Fail'
                else:
                    bearing_stress_check = 'Pass'

                # anchor_bolt_list = [8, 10, 12, 16, 20, 24, 30, 36, 42, 48, 56, 64, 72]  #TODO: this should be the original list passed by user
                # anchor_bolt_list = self.anchor_dia_out

                # revise bolt design if the bearing check fails (increasing the number/area of bolts will reduce the bearing stress)
                # First iteration - with 2 bolts
                if (self.anchors_outside_flange == 2) and (bearing_stress_check == 'Fail'):
                    # self.anchor_area_tension = self.bolt_area(self.anchor_dia_outside_flange)[0] * self.anchors_outside_flange
                    self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                              ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                    self.max_bearing_stress = abs(self.max_bearing_stress)

                    n = 1
                    while self.max_bearing_stress > self.bearing_strength_concrete:
                        itr = len(self.anchor_dia_list_out) + 1
                        sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange <= x <= 72, self.anchor_dia_list_out)
                        for i in sort_bolt:
                            min_bolt_dia = i
                            break

                        bolt_index = self.anchor_dia_list_out.index(min_bolt_dia)
                        bolt_list = self.anchor_dia_list_out[bolt_index:]

                        for i in bolt_list:
                            self.anchor_dia_provided_outside_flange = i  # updating anchor dia to check for bearing stress
                            break

                        self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                        ### update design to check bearing stress ###
                        self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                                   self.dp_detail_edge_type)
                        self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                        self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                        self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                        if self.end_distance_out < self.plate_washer_dim_out:
                            self.end_distance_out = self.plate_washer_dim_out
                        self.edge_distance_out = self.end_distance_out

                        # fixing bp size and parameters calculations after the iteration checks
                        if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                            self.bolt_columns_outside_flange = 1
                            # updating the bp dimension
                            self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                            self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                            self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                        elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                            self.bolt_columns_outside_flange = 2
                            # provide pitch and gauge
                            self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                            self.pitch_distance_out = 1.5 * self.pitch_distance_out

                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                            if self.pitch_distance_out < self.plate_washer_dim_out:
                                self.pitch_distance_out = self.pitch_distance_out
                            self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                            self.gauge_distance_out = self.pitch_distance_out

                            # updating the bp dimension
                            self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                               5)  # mm
                            self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                            self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                        # recalculating the parameters with updated dimensions
                        # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                        self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                        self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                        self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                        self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                        # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                        roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                        r_1 = roots[0]
                        r_2 = roots[1]
                        r_3 = roots[2]
                        r = max(r_1, r_2, r_3)
                        r = r.real  # separating the imaginary part
                        self.y = round(r)  # mm

                        self.tension_demand_anchor = (- self.load_axial_compression) * (
                                ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                        self.tension_demand_anchor = abs(self.tension_demand_anchor)
                        self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                        ### end of update check ###
                        self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                                  ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                        self.max_bearing_stress = abs(self.max_bearing_stress)

                        n += 1
                        # selecting higher dia if the max bearing stress exceeds the limit
                        if self.max_bearing_stress > self.bearing_strength_concrete:
                            sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange < x <= 72, self.anchor_dia_list_out)
                            for i in sort_bolt:
                                self.anchor_dia_provided_outside_flange = i
                                break

                        if self.anchor_dia_provided_outside_flange == 72:
                            self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                            ### update design to check bearing stress ###
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)
                            self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out
                            self.edge_distance_out = self.end_distance_out

                            # fixing bp size and parameters calculations after the iteration checks
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                                self.bolt_columns_outside_flange = 1
                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                                self.bolt_columns_outside_flange = 2
                                # provide pitch and gauge
                                self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                                self.pitch_distance_out = 1.5 * self.pitch_distance_out

                                self.plate_washer_details_out = IS6649.square_washer_dimensions(
                                    self.anchor_dia_provided_outside_flange)  # outside flange
                                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                                if self.pitch_distance_out < self.plate_washer_dim_out:
                                    self.pitch_distance_out = self.pitch_distance_out
                                self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                                self.gauge_distance_out = self.pitch_distance_out

                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                                   5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                            # recalculating the parameters with updated dimensions
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                            roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            r_1 = roots[0]
                            r_2 = roots[1]
                            r_3 = roots[2]
                            r = max(r_1, r_2, r_3)
                            r = r.real  # separating the imaginary part
                            self.y = round(r)  # mm

                            self.tension_demand_anchor = (- self.load_axial_compression) * (
                                    ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                    ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            self.tension_demand_anchor = abs(self.tension_demand_anchor)
                            self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### end of update check ###
                            self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                                      ((self.anchor_area_tension * self.n) * (
                                                                  (self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                            self.max_bearing_stress = abs(self.max_bearing_stress)

                        if ((self.anchor_dia_provided_outside_flange == 72) and (self.max_bearing_stress > self.bearing_strength_concrete)) or \
                                ((n > itr) and (self.max_bearing_stress > self.bearing_strength_concrete)):
                            bearing_stress_check = 'Fail'
                            logger.warning("[Concrete Bearing Check] The compressive stress on the concrete footing/pedestal ({} N/mm2) is greater "
                                           "than the allowable bearing strength of the concrete ({} N/mm2)".format(round(self.max_bearing_stress, 3),
                                                                                                           round(self.bearing_strength_concrete, 3)))
                            logger.info("The check fails with {} numbers of anchors".format(2 * self.anchors_outside_flange))
                            logger.info("Re-designing the connection with more or higher diameter anchor bolts to reduce the bearing stress")

                            self.anchor_dia_provided_outside_flange = self.anchor_dia_list_out[0]  # initialise with least dia for next iteration
                            self.anchors_outside_flange = 3  # increase number of bolts if check with 2 bolts fails
                            self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                            ### update design to check bearing stress ###
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)
                            self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out
                            self.edge_distance_out = self.end_distance_out

                            # fixing bp size and parameters calculations after the iteration checks
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                                self.bolt_columns_outside_flange = 1
                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                                self.bolt_columns_outside_flange = 2
                                # provide pitch and gauge
                                self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                                self.pitch_distance_out = 1.5 * self.pitch_distance_out

                                self.plate_washer_details_out = IS6649.square_washer_dimensions(
                                    self.anchor_dia_provided_outside_flange)  # outside flange
                                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                                if self.pitch_distance_out < self.plate_washer_dim_out:
                                    self.pitch_distance_out = self.pitch_distance_out
                                self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                                self.gauge_distance_out = self.pitch_distance_out

                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                                   5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                            # recalculating the parameters with updated dimensions
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                            roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            r_1 = roots[0]
                            r_2 = roots[1]
                            r_3 = roots[2]
                            r = max(r_1, r_2, r_3)
                            r = r.real  # separating the imaginary part
                            self.y = round(r)  # mm

                            self.tension_demand_anchor = (- self.load_axial_compression) * (
                                    ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                    ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            self.tension_demand_anchor = abs(self.tension_demand_anchor)
                            self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### end of update check ###
                            break

                # Second iteration
                if (self.anchors_outside_flange == 3) and (bearing_stress_check == 'Fail'):
                    # self.anchor_area_tension = self.bolt_area(self.anchor_dia_outside_flange)[0] * self.anchors_outside_flange

                    self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                              ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                    self.max_bearing_stress = abs(self.max_bearing_stress)

                    n = 1
                    while self.max_bearing_stress > self.bearing_strength_concrete:
                        itr = len(self.anchor_dia_list_out) + 1
                        sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange <= x <= 72, self.anchor_dia_list_out)
                        for i in sort_bolt:
                            min_bolt_dia = i
                            break

                        bolt_index = self.anchor_dia_list_out.index(min_bolt_dia)
                        bolt_list = self.anchor_dia_list_out[bolt_index:]

                        for i in bolt_list:
                            self.anchor_dia_provided_outside_flange = i  # updating anchor dia to check for bearing stress
                            break

                        self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                        ### update design to check bearing stress ###
                        self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                                   self.dp_detail_edge_type)
                        self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                        self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                        self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                        if self.end_distance_out < self.plate_washer_dim_out:
                            self.end_distance_out = self.plate_washer_dim_out
                        self.edge_distance_out = self.end_distance_out

                        # fixing bp size and parameters calculations after the iteration checks
                        if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                            self.bolt_columns_outside_flange = 1
                            # updating the bp dimension
                            self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                            self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                            self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                        elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                            self.bolt_columns_outside_flange = 2
                            # provide pitch and gauge
                            self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                            self.pitch_distance_out = 1.5 * self.pitch_distance_out

                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                            if self.pitch_distance_out < self.plate_washer_dim_out:
                                self.pitch_distance_out = self.pitch_distance_out
                            self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                            self.gauge_distance_out = self.pitch_distance_out

                            # updating the bp dimension
                            self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                               5)  # mm
                            self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                            self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                        # recalculating the parameters with updated dimensions
                        # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                        self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                        self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                        self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                        self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                        # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                        roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                        r_1 = roots[0]
                        r_2 = roots[1]
                        r_3 = roots[2]
                        r = max(r_1, r_2, r_3)
                        r = r.real  # separating the imaginary part
                        self.y = round(r)  # mm

                        self.tension_demand_anchor = (- self.load_axial_compression) * (
                                ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                        self.tension_demand_anchor = abs(self.tension_demand_anchor)
                        self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                        ### end of update check ###
                        self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                                  ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                        self.max_bearing_stress = abs(self.max_bearing_stress)

                        n += 1
                        # selecting higher dia if the max bearing stress exceeds the limit
                        if self.max_bearing_stress > self.bearing_strength_concrete:
                            sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange < x <= 72, self.anchor_dia_list_out)
                            for i in sort_bolt:
                                self.anchor_dia_provided_outside_flange = i
                                break

                        if self.anchor_dia_provided_outside_flange == 72:
                            self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                            ### update design to check bearing stress ###
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)
                            self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out
                            self.edge_distance_out = self.end_distance_out

                            # fixing bp size and parameters calculations after the iteration checks
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                                self.bolt_columns_outside_flange = 1
                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                                self.bolt_columns_outside_flange = 2
                                # provide pitch and gauge
                                self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                                self.pitch_distance_out = 1.5 * self.pitch_distance_out

                                self.plate_washer_details_out = IS6649.square_washer_dimensions(
                                    self.anchor_dia_provided_outside_flange)  # outside flange
                                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                                if self.pitch_distance_out < self.plate_washer_dim_out:
                                    self.pitch_distance_out = self.pitch_distance_out
                                self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                                self.gauge_distance_out = self.pitch_distance_out

                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                                   5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                            # recalculating the parameters with updated dimensions
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                            roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            r_1 = roots[0]
                            r_2 = roots[1]
                            r_3 = roots[2]
                            r = max(r_1, r_2, r_3)
                            r = r.real  # separating the imaginary part
                            self.y = round(r)  # mm

                            self.tension_demand_anchor = (- self.load_axial_compression) * (
                                    ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                    ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            self.tension_demand_anchor = abs(self.tension_demand_anchor)
                            self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### end of update check ###
                            self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                                      ((self.anchor_area_tension * self.n) * (
                                                                  (self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                            self.max_bearing_stress = abs(self.max_bearing_stress)

                        if ((self.anchor_dia_provided_outside_flange == 72) and (self.max_bearing_stress > self.bearing_strength_concrete)) or \
                                ((n > itr) and (self.max_bearing_stress > self.bearing_strength_concrete)):
                            bearing_stress_check = 'Fail'
                            logger.warning("[Concrete Bearing Check] The compressive stress on the concrete footing/pedestal ({} N/mm2) is greater "
                                           "than the allowable bearing strength of the concrete ({} N/mm2)".format(round(self.max_bearing_stress, 3),
                                                                                                           round(self.bearing_strength_concrete, 3)))
                            logger.info("The check fails with {} numbers of anchors".format(2 * self.anchors_outside_flange))
                            logger.info("Re-designing the connection with more or higher diameter anchor bolts to reduce the bearing stress")

                            self.anchor_dia_provided_outside_flange = self.anchor_dia_list_out[0]  # initialise with least dia for next iteration
                            self.anchors_outside_flange = 4  # increase number of bolts if check fails
                            self.bolt_columns_outside_flange = 2

                            # # pitch and gauge
                            # self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                            # self.pitch_distance_out = 1.5 * self.pitch_distance_out  # pitch increased to accommodate the end plate at the end of anchor inside footing
                            #
                            # self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            # self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            #
                            # if self.pitch_distance_out < self.plate_washer_dim_out:
                            #     self.pitch_distance_out = self.pitch_distance_out
                            #
                            # self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                            # self.gauge_distance_out = self.pitch_distance_out
                            #
                            # # updating the bp dimension
                            # self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                            #                                    5)  # mm
                            # self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                            #
                            # self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            # self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            #
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            # self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            # self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            # self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            # self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            # r_1 = roots[0]
                            # r_2 = roots[1]
                            # r_3 = roots[2]
                            # r = max(r_1, r_2, r_3)
                            # r = r.real  # separating the imaginary part
                            # self.y = round(r)  # mm
                            #
                            # self.tension_demand_anchor = (- self.load_axial_compression) * (
                            #         ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                            #         ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            # if self.tension_demand_anchor < 0:
                            #     self.tension_demand_anchor = (- 1 * self.tension_demand_anchor)
                            #
                            # self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### update design to check bearing stress ###
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)
                            self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out
                            self.edge_distance_out = self.end_distance_out

                            # fixing bp size and parameters calculations after the iteration checks
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                                self.bolt_columns_outside_flange = 1
                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                                self.bolt_columns_outside_flange = 2
                                # provide pitch and gauge
                                self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                                self.pitch_distance_out = 1.5 * self.pitch_distance_out

                                self.plate_washer_details_out = IS6649.square_washer_dimensions(
                                    self.anchor_dia_provided_outside_flange)  # outside flange
                                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                                if self.pitch_distance_out < self.plate_washer_dim_out:
                                    self.pitch_distance_out = self.pitch_distance_out
                                self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                                self.gauge_distance_out = self.pitch_distance_out

                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                                   5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                            # recalculating the parameters with updated dimensions
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                            roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            r_1 = roots[0]
                            r_2 = roots[1]
                            r_3 = roots[2]
                            r = max(r_1, r_2, r_3)
                            r = r.real  # separating the imaginary part
                            self.y = round(r)  # mm

                            self.tension_demand_anchor = (- self.load_axial_compression) * (
                                    ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                    ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            self.tension_demand_anchor = abs(self.tension_demand_anchor)
                            self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### end of update check ###
                            break
                        else:  # check for detailing
                            # updating the end/edge and pitch/gauge distance (if the anchor diameter or numbers is improvised in the above loop(s))
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)

                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out

                            self.edge_distance_out = self.end_distance_out

                            if (0.85 * self.column_bf) < (2 * self.edge_distance_out):
                                self.safe = False
                                logger.warning("[Detailing Check] The detailing checks are not satisfied with anchor bolts of {} mm diameter".
                                               format(self.anchor_dia_provided_outside_flange))
                                logger.info("Re-designing the connection with lesser anchor bolts of higher diameter and grade combination")

                # Third iteration
                if (self.anchors_outside_flange == 4) and (bearing_stress_check == 'Fail'):
                    # self.anchor_area_tension = self.bolt_area(self.anchor_dia_outside_flange)[0] * self.anchors_outside_flange

                    self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                              ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                    self.max_bearing_stress = abs(self.max_bearing_stress)

                    n = 1
                    while self.max_bearing_stress > self.bearing_strength_concrete:
                        itr = len(self.anchor_dia_list_out) + 1
                        sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange <= x <= 72, self.anchor_dia_list_out)
                        for i in sort_bolt:
                            min_bolt_dia = i
                            break

                        bolt_index = self.anchor_dia_list_out.index(min_bolt_dia)
                        bolt_list = self.anchor_dia_list_out[bolt_index:]

                        for i in bolt_list:
                            self.anchor_dia_provided_outside_flange = i  # updating anchor dia to check for bearing stress
                            break

                        self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                        ### update design to check bearing stress ###
                        self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                                   self.dp_detail_edge_type)
                        self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                        self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                        self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                        if self.end_distance_out < self.plate_washer_dim_out:
                            self.end_distance_out = self.plate_washer_dim_out
                        self.edge_distance_out = self.end_distance_out

                        # fixing bp size and parameters calculations after the iteration checks
                        if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                            self.bolt_columns_outside_flange = 1
                            # updating the bp dimension
                            self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                            self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                            self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                        elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                            self.bolt_columns_outside_flange = 2
                            # provide pitch and gauge
                            self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                            self.pitch_distance_out = 1.5 * self.pitch_distance_out

                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                            if self.pitch_distance_out < self.plate_washer_dim_out:
                                self.pitch_distance_out = self.pitch_distance_out
                            self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                            self.gauge_distance_out = self.pitch_distance_out

                            # updating the bp dimension
                            self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                               5)  # mm
                            self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                            self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                        # recalculating the parameters with updated dimensions
                        # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                        self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                        self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                        self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                        self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                        # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                        roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                        r_1 = roots[0]
                        r_2 = roots[1]
                        r_3 = roots[2]
                        r = max(r_1, r_2, r_3)
                        r = r.real  # separating the imaginary part
                        self.y = round(r)  # mm

                        self.tension_demand_anchor = (- self.load_axial_compression) * (
                                ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                        self.tension_demand_anchor = abs(self.tension_demand_anchor)
                        self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                        ### end of update check ###
                        self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                                  ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                        self.max_bearing_stress = abs(self.max_bearing_stress)

                        n += 1
                        # selecting higher dia if the max bearing stress exceeds the limit
                        if self.max_bearing_stress > self.bearing_strength_concrete:
                            sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange < x <= 72, self.anchor_dia_list_out)
                            for i in sort_bolt:
                                self.anchor_dia_provided_outside_flange = i
                                break

                        if self.anchor_dia_provided_outside_flange == 72:
                            self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                            ### update design to check bearing stress ###
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)
                            self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out
                            self.edge_distance_out = self.end_distance_out

                            # fixing bp size and parameters calculations after the iteration checks
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                                self.bolt_columns_outside_flange = 1
                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                                self.bolt_columns_outside_flange = 2
                                # provide pitch and gauge
                                self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                                self.pitch_distance_out = 1.5 * self.pitch_distance_out

                                self.plate_washer_details_out = IS6649.square_washer_dimensions(
                                    self.anchor_dia_provided_outside_flange)  # outside flange
                                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                                if self.pitch_distance_out < self.plate_washer_dim_out:
                                    self.pitch_distance_out = self.pitch_distance_out
                                self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                                self.gauge_distance_out = self.pitch_distance_out

                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                                   5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                            # recalculating the parameters with updated dimensions
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                            roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            r_1 = roots[0]
                            r_2 = roots[1]
                            r_3 = roots[2]
                            r = max(r_1, r_2, r_3)
                            r = r.real  # separating the imaginary part
                            self.y = round(r)  # mm

                            self.tension_demand_anchor = (- self.load_axial_compression) * (
                                    ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                    ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            self.tension_demand_anchor = abs(self.tension_demand_anchor)
                            self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### end of update check ###
                            self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                                      ((self.anchor_area_tension * self.n) * (
                                                                  (self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                            self.max_bearing_stress = abs(self.max_bearing_stress)

                        if ((self.anchor_dia_provided_outside_flange == 72) and (self.max_bearing_stress > self.bearing_strength_concrete)) or \
                                ((n > itr) and (self.max_bearing_stress > self.bearing_strength_concrete)):
                            bearing_stress_check = 'Fail'
                            logger.warning("[Concrete Bearing Check] The compressive stress on the concrete footing/pedestal ({} N/mm2) is greater "
                                           "than the allowable bearing strength of the concrete ({} N/mm2)".format(round(self.max_bearing_stress, 3),
                                                                                                           round(self.bearing_strength_concrete, 3)))
                            logger.info("The check fails with {} numbers of anchors".format(2 * self.anchors_outside_flange))
                            logger.info("Re-designing the connection with more or higher diameter anchor bolts to reduce the bearing stress")

                            self.anchor_dia_provided_outside_flange = self.anchor_dia_list_out[0]  # initialise with least dia for next iteration
                            self.anchors_outside_flange = 6  # increase number of bolts if check fails
                            self.bolt_columns_outside_flange = 2

                            # # provide pitch and gauge
                            # self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                            # self.pitch_distance_out = 1.5 * self.pitch_distance_out  # pitch increased to accommodate the end plate at the end of anchor inside footing
                            #
                            # self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            # self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            #
                            # if self.pitch_distance_out < self.plate_washer_dim_out:
                            #     self.pitch_distance_out = self.pitch_distance_out
                            #
                            # self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                            # self.gauge_distance_out = self.pitch_distance_out
                            #
                            # # updating the bp dimension
                            # self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                            #                                    5)  # mm
                            # self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                            #
                            # self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            # self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            #
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            # self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            # self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            # self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            # self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            # r_1 = roots[0]
                            # r_2 = roots[1]
                            # r_3 = roots[2]
                            # r = max(r_1, r_2, r_3)
                            # r = r.real  # separating the imaginary part
                            # self.y = round(r)  # mm
                            #
                            # self.tension_demand_anchor = (- self.load_axial_compression) * (
                            #         ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                            #         ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            # if self.tension_demand_anchor < 0:
                            #     self.tension_demand_anchor = (- 1 * self.tension_demand_anchor)
                            #
                            # self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN
                            ### update design to check bearing stress ###
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)
                            self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out
                            self.edge_distance_out = self.end_distance_out

                            # fixing bp size and parameters calculations after the iteration checks
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                                self.bolt_columns_outside_flange = 1
                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                                self.bolt_columns_outside_flange = 2
                                # provide pitch and gauge
                                self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                                self.pitch_distance_out = 1.5 * self.pitch_distance_out

                                self.plate_washer_details_out = IS6649.square_washer_dimensions(
                                    self.anchor_dia_provided_outside_flange)  # outside flange
                                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                                if self.pitch_distance_out < self.plate_washer_dim_out:
                                    self.pitch_distance_out = self.pitch_distance_out
                                self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                                self.gauge_distance_out = self.pitch_distance_out

                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                                   5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                            # recalculating the parameters with updated dimensions
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                            roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            r_1 = roots[0]
                            r_2 = roots[1]
                            r_3 = roots[2]
                            r = max(r_1, r_2, r_3)
                            r = r.real  # separating the imaginary part
                            self.y = round(r)  # mm

                            self.tension_demand_anchor = (- self.load_axial_compression) * (
                                    ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                    ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            self.tension_demand_anchor = abs(self.tension_demand_anchor)
                            self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### end of update check ###
                            break

                # Fourth iteration
                if (self.anchors_outside_flange == 6) and (bearing_stress_check == 'Fail'):
                    # self.anchor_area_tension = self.bolt_area(self.anchor_dia_outside_flange)[0] * self.anchors_outside_flange

                    self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                              ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                    self.max_bearing_stress = abs(self.max_bearing_stress)

                    n = 1
                    while self.max_bearing_stress > self.bearing_strength_concrete:
                        itr = len(self.anchor_dia_list_out) + 1
                        sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange <= x <= 72, self.anchor_dia_list_out)
                        for i in sort_bolt:
                            min_bolt_dia = i
                            break

                        bolt_index = self.anchor_dia_list_out.index(min_bolt_dia)
                        bolt_list = self.anchor_dia_list_out[bolt_index:]
                        # print(len(bolt_list))

                        for i in bolt_list:
                            self.anchor_dia_provided_outside_flange = i  # updating anchor dia to check for bearing stress
                            break

                        self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                        ### update design to check bearing stress ###
                        self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                                   self.dp_detail_edge_type)
                        self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                        self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                        self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                        if self.end_distance_out < self.plate_washer_dim_out:
                            self.end_distance_out = self.plate_washer_dim_out
                        self.edge_distance_out = self.end_distance_out

                        # fixing bp size and parameters calculations after the iteration checks
                        if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                            self.bolt_columns_outside_flange = 1
                            # updating the bp dimension
                            self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                            self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                            self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                        elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                            self.bolt_columns_outside_flange = 2
                            # provide pitch and gauge
                            self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                            self.pitch_distance_out = 1.5 * self.pitch_distance_out

                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                            if self.pitch_distance_out < self.plate_washer_dim_out:
                                self.pitch_distance_out = self.pitch_distance_out
                            self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                            self.gauge_distance_out = self.pitch_distance_out

                            # updating the bp dimension
                            self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                               5)  # mm
                            self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                            self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                        # recalculating the parameters with updated dimensions
                        # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                        self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                        self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                        self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                        self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                        # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                        roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                        r_1 = roots[0]
                        r_2 = roots[1]
                        r_3 = roots[2]
                        r = max(r_1, r_2, r_3)
                        r = r.real  # separating the imaginary part
                        self.y = round(r)  # mm

                        self.tension_demand_anchor = (- self.load_axial_compression) * (
                                ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                        self.tension_demand_anchor = abs(self.tension_demand_anchor)
                        self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                        ### end of update check ###
                        self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                                  ((self.anchor_area_tension * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                        self.max_bearing_stress = abs(self.max_bearing_stress)

                        n += 1
                        # selecting higher dia if the max bearing stress exceeds the limit
                        if self.max_bearing_stress > self.bearing_strength_concrete:
                            sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange < x <= 72, self.anchor_dia_list_out)
                            for i in sort_bolt:
                                self.anchor_dia_provided_outside_flange = i
                                break

                        if self.anchor_dia_provided_outside_flange == 72:
                            self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange

                            ### update design to check bearing stress ###
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)
                            self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out
                            self.edge_distance_out = self.end_distance_out

                            # fixing bp size and parameters calculations after the iteration checks
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                                self.bolt_columns_outside_flange = 1
                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                                self.bolt_columns_outside_flange = 2
                                # provide pitch and gauge
                                self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                                self.pitch_distance_out = 1.5 * self.pitch_distance_out

                                self.plate_washer_details_out = IS6649.square_washer_dimensions(
                                    self.anchor_dia_provided_outside_flange)  # outside flange
                                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                                if self.pitch_distance_out < self.plate_washer_dim_out:
                                    self.pitch_distance_out = self.pitch_distance_out
                                self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                                self.gauge_distance_out = self.pitch_distance_out

                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                                   5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                            # recalculating the parameters with updated dimensions
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                            roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            r_1 = roots[0]
                            r_2 = roots[1]
                            r_3 = roots[2]
                            r = max(r_1, r_2, r_3)
                            r = r.real  # separating the imaginary part
                            self.y = round(r)  # mm

                            self.tension_demand_anchor = (- self.load_axial_compression) * (
                                    ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                    ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            self.tension_demand_anchor = abs(self.tension_demand_anchor)
                            self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### end of update check ###
                            self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / \
                                                      ((self.anchor_area_tension * self.n) * (
                                                                  (self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                            self.max_bearing_stress = abs(self.max_bearing_stress)

                        if ((self.anchor_dia_provided_outside_flange == 72) and (self.max_bearing_stress > self.bearing_strength_concrete)) or \
                                ((n > itr) and (self.max_bearing_stress > self.bearing_strength_concrete)):
                            bearing_stress_check = 'Fail'
                            logger.warning("[Concrete Bearing Check] The compressive stress on the concrete footing/pedestal ({} N/mm2) is greater "
                                           "than the allowable bearing strength of the concrete ({} N/mm2)".format(round(self.max_bearing_stress, 3),
                                                                                                           round(self.bearing_strength_concrete, 3)))
                            logger.info("The check fails with {} numbers of anchors".format(2 * self.anchors_outside_flange))
                            logger.info("Re-designing the connection with more or higher diameter anchor bolts to reduce the bearing stress")

                            self.anchor_dia_provided_outside_flange = self.anchor_dia_list_out[0]  # initialise with least dia for next iteration
                            self.anchors_outside_flange = 8
                            self.bolt_columns_outside_flange = 2

                            # # provide pitch and gauge
                            # self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                            # self.pitch_distance_out = 1.5 * self.pitch_distance_out  # pitch increased to accommodate the end plate at the end of anchor inside footing
                            #
                            # self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            # self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            #
                            # if self.pitch_distance_out < self.plate_washer_dim_out:
                            #     self.pitch_distance_out = self.pitch_distance_out
                            #
                            # self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                            # self.gauge_distance_out = self.pitch_distance_out
                            #
                            # # updating the bp dimension
                            # self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                            #                                    5)  # mm
                            # self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                            #
                            # self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                            # self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            #
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            # self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            # self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            # self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            # self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            # r_1 = roots[0]
                            # r_2 = roots[1]
                            # r_3 = roots[2]
                            # r = max(r_1, r_2, r_3)
                            # r = r.real  # separating the imaginary part
                            # self.y = round(r)  # mm
                            #
                            # self.tension_demand_anchor = (- self.load_axial_compression) * (
                            #         ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                            #         ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            # if self.tension_demand_anchor < 0:
                            #     self.tension_demand_anchor = (- 1 * self.tension_demand_anchor)
                            #
                            # self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN
                            ### update design to check bearing stress ###
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)
                            self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)
                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm
                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out
                            self.edge_distance_out = self.end_distance_out

                            # fixing bp size and parameters calculations after the iteration checks
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                                self.bolt_columns_outside_flange = 1
                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))
                            elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                                self.bolt_columns_outside_flange = 2
                                # provide pitch and gauge
                                self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                                self.pitch_distance_out = 1.5 * self.pitch_distance_out

                                self.plate_washer_details_out = IS6649.square_washer_dimensions(
                                    self.anchor_dia_provided_outside_flange)  # outside flange
                                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                                if self.pitch_distance_out < self.plate_washer_dim_out:
                                    self.pitch_distance_out = self.pitch_distance_out
                                self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                                self.gauge_distance_out = self.pitch_distance_out

                                # updating the bp dimension
                                self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out),
                                                                   5)  # mm
                                self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm
                                self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                                self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                            # recalculating the parameters with updated dimensions
                            # self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                            self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm
                            self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                            self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                            self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2
                            # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                            roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                            r_1 = roots[0]
                            r_2 = roots[1]
                            r_3 = roots[2]
                            r = max(r_1, r_2, r_3)
                            r = r.real  # separating the imaginary part
                            self.y = round(r)  # mm

                            self.tension_demand_anchor = (- self.load_axial_compression) * (
                                    ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                                    ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                            self.tension_demand_anchor = abs(self.tension_demand_anchor)
                            self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                            ### end of update check ###
                            break
                        else:  # check for detailing
                            # updating the end/edge and pitch/gauge distance (if the anchor diameter or numbers is improvised in the above loop(s))
                            self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange,
                                                                                       self.dp_anchor_hole_out,
                                                                                       self.dp_detail_edge_type)

                            self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                            self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                            if self.end_distance_out < self.plate_washer_dim_out:
                                self.end_distance_out = self.plate_washer_dim_out

                            self.edge_distance_out = self.end_distance_out

                            if (0.85 * self.column_bf) < (2 * self.edge_distance_out):
                                self.safe = False
                                logger.warning("[Detailing Check] The detailing checks are not satisfied with anchor bolts of {} mm diameter".
                                               format(self.anchor_dia_provided_outside_flange))
                                logger.info("Re-designing the connection with lesser anchor bolts of higher diameter and grade combination")

                # maximum allowed bolts is 6
                if (self.anchors_outside_flange >= 8) and (bearing_stress_check == 'Fail'):
                    self.safe = False
                    logger.warning("[Concrete Bearing Check] The compressive stress on the concrete footing/pedestal ({} N/mm2) is greater "
                                   "than the allowable bearing strength of the concrete ({} N/mm2)".format(round(self.max_bearing_stress, 3),
                                                                                                           round(self.bearing_strength_concrete, 3)))
                    # logger.info("The check fails with {} numbers of anchors".format(2 * self.anchors_outside_flange))
                    logger.info("Provide a higher grade of concrete and re-design")

                # optimise bolt diameter based on passed bearing check
                # anchor_dia_init = self.anchor_dia_provided_outside_flange
                #
                # self.anchor_area_tension = (self.tension_demand_anchor * 1000 * self.y) / \
                #                           ((self.max_bearing_stress * self.n) * ((self.bp_length_provided / 2) - self.y + self.f))  # mm^2
                #
                # self.anchor_dia_provided_outside_flange = math.sqrt((4 * self.anchor_area_tension) / (math.pi * self.n))  # mm
                #
                # sort_bolt = filter(lambda x: self.anchor_dia_provided_outside_flange <= x <= 72, self.anchor_dia_list_out)
                #
                # for i in sort_bolt:
                #     self.anchor_dia_provided_outside_flange = i  # optimised anchor dia provided (mm)
                #     break

                # updating the end/edge and pitch/gauge distance (if the anchor diameter or numbers is improvised in the above loop(s))
                self.end_distance_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out,
                                                                           self.dp_detail_edge_type)
                self.end_distance_out = round_up(1.5 * self.end_distance_out, 5)

                self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                if self.end_distance_out < self.plate_washer_dim_out:
                    self.end_distance_out = self.plate_washer_dim_out

                self.edge_distance_out = self.end_distance_out

                # fixing bp size and parameters calculations after the iteration checks
                if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
                    self.bolt_columns_outside_flange = 1

                    # updating the bp dimension
                    self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)), 5)  # mm
                    self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                    self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                    self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                elif (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):
                    self.bolt_columns_outside_flange = 2

                    # provide pitch and gauge
                    self.pitch_distance_out = self.cl_10_2_2_min_spacing(self.anchor_dia_provided_outside_flange)  # mm
                    self.pitch_distance_out = 1.5 * self.pitch_distance_out  # pitch increased to accommodate the end plate at the end of anchor inside footing

                    self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_provided_outside_flange)  # outside flange
                    self.plate_washer_dim_out = self.plate_washer_details_out['side']  # outside flange, mm

                    if self.pitch_distance_out < self.plate_washer_dim_out:
                        self.pitch_distance_out = self.pitch_distance_out

                    self.pitch_distance_out = round_up(self.pitch_distance_out, 5)
                    self.gauge_distance_out = self.pitch_distance_out

                    # updating the bp dimension
                    self.bp_length_provided = round_up(self.column_D + (2 * (2 * self.end_distance_out)) + (2 * self.pitch_distance_out), 5)  # mm
                    self.bp_width_provided = round_up((0.85 * self.column_bf) + (2 * (2 * self.edge_distance_out)), 5)  # mm

                    self.bp_length_provided = max(self.bp_length_provided, round_up(self.column_D + (2 * 100), 5))
                    self.bp_width_provided = max(self.bp_width_provided, round_up(self.column_bf + (2 * 100), 5))

                # recalculating the parameters with updated dimensions
                self.anchor_area_tension = self.bolt_area(self.anchor_dia_provided_outside_flange)[0] * self.anchors_outside_flange
                self.f = (self.bp_length_provided / 2) - self.end_distance_out  # mm

                self.k1 = 3 * (self.eccentricity_zz - (self.bp_length_provided / 2))
                self.k2 = ((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                self.k3 = ((self.bp_length_provided / 2) + self.f) * -self.k2

                # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                r_1 = roots[0]
                r_2 = roots[1]
                r_3 = roots[2]
                r = max(r_1, r_2, r_3)
                r = r.real  # separating the imaginary part

                self.y = round(r)  # mm

                self.tension_demand_anchor = (- self.load_axial_compression) * (
                            ((self.bp_length_provided / 2) - (self.y / 3) - self.eccentricity_zz) /
                            ((self.bp_length_provided / 2) - (self.y / 3) + self.f))  # N
                if self.tension_demand_anchor < 0:
                    self.tension_demand_anchor = (- 1 * self.tension_demand_anchor)

                self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                self.anchor_area_outside_flange = self.bolt_area(self.anchor_dia_provided_outside_flange)
                self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0],
                                                                                              self.anchor_fu_fy_outside_flange[1],
                                                                                              self.anchor_area_outside_flange[0],
                                                                                              self.anchor_area_outside_flange[1],
                                                                                              safety_factor_parameter=self.dp_weld_fab)  # N
                self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                # update bearing stress
                self.max_bearing_stress = (self.tension_demand_anchor * 1000 * self.y) / ((self.anchor_area_tension * self.n) *
                                                                                          ((self.bp_length_provided / 2) - self.y + self.f))  # N/mm^2
                self.max_bearing_stress = abs(self.max_bearing_stress)

                # designing the plate thickness

                # 1. Yielding of the base plate due to bearing on concrete
                # finding the length of the critical section from the edge of the base plate on the compression side
                self.critical_xx = round((self.bp_length_provided - (0.95 * self.column_D)) / 2, 2)  # mm
                if self.y > self.critical_xx:
                    self.critical_xx = self.critical_xx
                else:
                    self.critical_xx = self.y

                # moment acting at the critical section due to applied loads
                # Assumption: The moment acting at the critical section is taken as [0.45*f_ck*B*critical_xx * (*critical_xx / 2)] (plastic moment)
                self.critical_M_xx = (self.critical_xx * self.bearing_strength_concrete * self.bp_width_provided) * \
                                     (self.critical_xx / 2)  # N-mm

                # 2. Yielding of the base plate due to tension in the anchor bolts on the tension side
                # TODO: add lever arm for 4 & 6 bolts on one side
                self.lever_arm = (self.bp_length_provided / 2) - (self.column_D / 2) + (self.column_tf / 2) - self.end_distance_out  # mm

                # moment acting on the plate due to tension in the bolts
                self.moment_lever_arm = self.tension_demand_anchor * 1000 * self.lever_arm  # N-mm

                # updating the critical moment
                self.critical_M_xx = max(self.critical_M_xx, self.moment_lever_arm)  # N-mm

                # equating critical moment with critical moment to compute the required minimum plate thickness
                # Assumption: The bending capacity of the plate is (M_d = 1.5*fy*Z_e/gamma_m0) [Reference: Clause 8.2.1.2, IS 800:2007]
                # Assumption: Z_e of the plate is = b*tp^2 / 6, where b = W for a cantilever strip of unit dimension

                self.plate_thk = math.sqrt((self.critical_M_xx * self.gamma_m0 * 6) / (1.5 * self.base_plate.fy * self.bp_width_provided))  # mm
                self.plate_thk = round(self.plate_thk, 2)

                # plate fy check
                # if self.plate_thk >= 20:
                #     self.base_plate.connect_to_database_to_get_fy_fu(self.dp_bp_material, self.plate_thk)  # update fy
                #     # update plate thk
                #     self.plate_thk = math.sqrt((self.critical_M_xx * self.gamma_m0 * 6) / (1.5 * self.base_plate.fy * self.bp_width_provided))  # mm
                #     self.plate_thk = round(self.plate_thk, 2)

            self.anchor_dia_outside_flange = self.anchor_dia_provided_outside_flange

        # updating the minimum assumed detailing parameters for design report
        if self.connectivity == 'Hollow/Tubular Column Base':
            self.bp_length_min = self.column_D + (2 * (2 * self.end_distance_out))  # mm
            self.bp_width_min = self.column_bf + (2 * (2 * self.end_distance_out))  # mm
        else:
            if self.connectivity == 'Moment Base Plate' and (self.moment_bp_case == 'Case2' or self.moment_bp_case == 'Case3'):
                if self.bolt_columns_outside_flange == 1:
                    self.bp_length_min = self.column_D + (2 * (2 * self.end_distance_out))  # mm
                    self.bp_width_min = 0.85 * self.column_bf + (2 * (2 * self.edge_distance_out))  # mm
                else:
                    self.bp_length_min = self.column_D + (2 * ((2 * self.end_distance_out) + self.pitch_distance_out))  # mm
                    self.bp_width_min = 0.85 * self.column_bf + (2 * (2 * self.edge_distance_out))  # mm
            else:
                self.bp_length_min = self.column_D + (2 * (2 * self.end_distance_out))  # mm
                self.bp_width_min = 0.85 * self.column_bf + (2 * (2 * self.edge_distance_out))  # mm

        # number of bolts
        if self.connectivity == 'Moment Base Plate':

            if self.moment_bp_case == 'Case1':
                self.anchors_outside_flange = 2  # each side
                self.anchors_inside_flange = 0
                self.anchor_nos_provided = (2 * self.anchors_outside_flange) + self.anchors_inside_flange
            else:
                self.anchor_nos_provided = 2 * self.anchors_outside_flange
        else:
            self.anchors_outside_flange = 2  # each side
            self.anchors_inside_flange = 0
            self.anchor_nos_provided = (2 * self.anchors_outside_flange) + self.anchors_inside_flange

        # re-calculate the para for design report
        if self.connectivity == 'Moment Base Plate':

            self.eccentricity_zz = round((self.load_moment_major / self.load_axial_compression), 2)

            if self.eccentricity_zz > (self.bp_length_min / 6):  # Case 1

                if self.eccentricity_zz >= (self.bp_length_min / 3):  # Case 3
                    self.moment_bp_case = 'Case3'
                    logger.info("[Base Plate Type] The value of eccentricity about the major axis is {} mm".format(round_down(self.eccentricity_zz, 2)))
                    logger.info("Eccentricity is greater than {} (L/3) mm".format(round(self.bp_length_min / 3, 2)))
                    logger.info("Case 3: A smaller part of the base plate is under pure compression/bearing with a large tension/uplift force being "
                                "transferred through the anchor bolts outside column flange on the tension side")

                else:  # (self.eccentricity_zz > (self.bp_length_min / 6)) or (self.eccentricity_zz < (self.bp_length_min / 3))
                    self.moment_bp_case = 'Case2'
                    logger.info("[Base Plate Type] The value of eccentricity about the major axis is {} mm".format(round_down(self.eccentricity_zz, 2)))
                    logger.info("Eccentricity is greater than {} (L/6) mm but less than {} (L/3) mm".format(round(self.bp_length_min / 6, 2),
                                                                                                            round(self.bp_length_min / 3, 2)))
                    logger.info("Case 2: A larger part of the base plate is under compression/bearing with a small to moderate tension/uplift force "
                                "being transferred through the anchor bolts outside column flange on the tension side")

                self.n = 2 * 10 ** 5 / (5000 * math.sqrt(self.cl_7_4_1_bearing_strength_concrete(self.footing_grade) / 0.45))
                self.n = round(self.n, 3)
                self.anchor_area_tension = round(self.anchor_area_outside_flange[0] * (self.anchor_nos_provided / 2), 2)  # mm^2, area of anchor under tension
                self.f = round((self.bp_length_provided / 2) - self.end_distance_out, 2)  # mm

                self.k1 = round(3 * (self.eccentricity_zz - (self.bp_length_provided / 2)), 2)
                self.k2 = round(((6 * self.n * self.anchor_area_tension) / self.bp_width_provided) * (self.f + self.eccentricity_zz), 2)
                self.k3 = round(((self.bp_length_provided / 2) + self.f) * -self.k2, 2)

                # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                roots = np.roots([1, self.k1, self.k2, self.k3])  # finding roots of the equation
                r_1 = roots[0]
                r_2 = roots[1]
                r_3 = roots[2]
                r = max(r_1, r_2, r_3)
                r = r.real  # separating the imaginary part

                self.y = round(r)  # mm

                self.plate_thk = math.sqrt((self.critical_M_xx * self.gamma_m0 * 6) / (1.5 * self.base_plate.fy * self.bp_width_provided))  # mm
                self.plate_thk = round(self.plate_thk, 2)

        # Minor axis
        if self.load_moment_minor > 0:
            self.eccentricity_yy = round((self.load_moment_minor / self.load_axial_compression), 2)  # mm, eccentricity about minor (y-y) axis
            # Defining cases: Case 1: e <= W/6        (compression throughout the BP)
            #                 Case 2: W/6 < e < W/3   (compression throughout + moderate tension/uplift in the anchor bolts)
            #                 Case 3: e >= W/3        (compression + high tension/uplift in the anchor bolts)

            if self.eccentricity_yy <= (self.bp_width_provided / 6):  # Case 1
                self.moment_bp_case_yy = 'Case1'

                logger.info("[Minor Axis Moment] The value of eccentricity about the minor axis is {} mm".format(round_down(self.eccentricity_yy, 2)))
                logger.info("Eccentricity is less than {} mm (W/6)".format(round(self.bp_width_provided / 6, 2)))
                logger.info("Case 1: The base plate is purely under compression/bearing over it's width, thus there is no requirement of anchor "
                            "bolts along the width of the column section")
            else:
                if self.eccentricity_yy >= (self.bp_width_provided / 3):  # Case 3
                    self.moment_bp_case_yy = 'Case3'
                    logger.info("[Minor Axis Moment] The value of eccentricity about the minor axis is {} mm".format(round_down(self.eccentricity_yy, 2)))
                    logger.info("Eccentricity is greater than {} (W/3) mm".format(round(self.bp_width_provided / 3, 2)))
                    logger.info("Case 3: A smaller part of the base plate is under pure compression/bearing with a large tension/uplift force being "
                                "transferred through the anchor bolts required to be placed along the minor axis of the column section")
                else:
                    self.moment_bp_case_yy = 'Case2'
                    logger.info("[Minor Axis Moment] The value of eccentricity about the minor axis is {} mm".format(round_down(self.eccentricity_yy, 2)))
                    logger.info("Eccentricity is greater than {} (W/6) mm but less than {} (W/3) mm".format(round(self.bp_width_provided / 6, 2),
                                                                                                            round(self.bp_width_provided / 3, 2)))
                    logger.info("Case 2: A larger part of the base plate is under compression/bearing with a small to moderate tension/uplift force "
                                "being transferred through the anchor bolts required to be placed along the minor axis of the column section")

        # assign appropriate plate thickness according to available sizes in the marked
        self.plate_thk_provided = max(self.plate_thk, self.column_tf)  # base plate thickness should be larger than the flange thickness

        # assigning plate thickness according to the available standard sizes
        # the thicknesses of the flats (in mm) listed below is obtained from SAIL's product brochure

        self.standard_plate_thk = []
        for plt in PLATE_THICKNESS_SAIL:
            plt = int(plt)
            self.standard_plate_thk.append(plt)

        sort_plate = filter(lambda x: self.plate_thk_provided <= x <= self.standard_plate_thk[-1], self.standard_plate_thk)

        for i in sort_plate:
            self.plate_thk_provided = i  # plate thickness provided (mm)
            break

        # check for maximum plate thickness
        if self.plate_thk_provided > self.standard_plate_thk[-1]:
            self.safe = False
            logger.error("[Plate Thickness] The thickness of the base plate exceeds the maximum available/allowable thickness of {} mm".
                         format(self.standard_plate_thk[-1]))
            logger.info("If a plate of higher thickness(es) is available, update it into the Osdag data base and re-design the connection")

        # plate moment capacity
        if self.connectivity == 'Moment Base Plate':
            # plate fy check
            if self.plate_thk_provided >= 20:
                self.base_plate.connect_to_database_to_get_fy_fu(self.dp_bp_material, self.plate_thk_provided)  # update fy

            self.plate_moment_capacity = ((self.bp_width_provided * self.plate_thk_provided ** 2) / 4) * (self.base_plate.fy / self.gamma_m0)
            self.plate_moment_capacity = round(self.plate_moment_capacity * 1e-6, 2)  # kNm

    def anchor_bolt_design(self):
        """ Perform design checks for the anchor bolt

        Args:

        Returns:
        """
        # updating the anchor area (provided outside flange), if the diameter is updated in the previous check(s)
        self.anchor_area_outside_flange = self.bolt_area(self.anchor_dia_provided_outside_flange)  # list of areas [shank area, thread area] mm^2

        # Design strength of the anchor bolt [Reference: Clause 10.3.2, IS 800:2007; Section 3, IS 5624:1993]
        # Assumption: number of shear planes passing through - the thread is 1 (n_n) and through the shank is 0 (n_s)

        self.shear_capacity_anchor = self.cl_10_3_3_bolt_shear_capacity(self.anchor_fu_fy_outside_flange[0], self.anchor_area_outside_flange[1],
                                                                        self.anchor_area_outside_flange[0], 1, 0, self.dp_weld_fab)
        self.shear_capacity_anchor = round(self.shear_capacity_anchor / 1000, 2)  # kN

        self.bearing_capacity_anchor = self.cl_10_3_4_bolt_bearing_capacity(self.base_plate.fu, self.anchor_fu_fy_outside_flange[0], self.plate_thk_provided,
                                                                            self.anchor_dia_provided_outside_flange, self.end_distance_out,
                                                                            self.pitch_distance_out, self.dp_anchor_hole_out, self.dp_weld_fab)
        self.bearing_capacity_anchor = round(self.bearing_capacity_anchor / 1000, 2)  # kN

        self.anchor_capacity = min(self.shear_capacity_anchor, self.bearing_capacity_anchor)  # kN

        # design for shear acting along any axis
        if (self.load_shear_major or self.load_shear_minor) > 0:

            if self.connectivity == 'Moment Base Plate':
                if self.moment_bp_case == 'Case2' or 'Case3':
                    # Check: Combined shear + Tension [Reference: cl.10.3.6, IS 800:2007]
                    # v_sb is calculated considering shear distribution in bolts only on the tension side (outside flange), this is the critical case
                    self.v_sb = (max(self.load_shear_major, self.load_shear_minor) * 10 ** -3) / \
                                ((self.anchor_nos_provided - self.anchors_inside_flange) / 2)  # kN
                    self.v_db = self.anchor_capacity  # kN
                    self.t_b = self.tension_demand_anchor / self.anchors_outside_flange  # kN
                    self.t_db = self.tension_capacity_anchor  # kN
                    self.combined_capacity_anchor = self.cl_10_3_6_bearing_bolt_combined_shear_and_tension(self.v_sb, self.v_db, self.t_b, self.t_db)
                    self.combined_capacity_anchor = round(self.combined_capacity_anchor, 3)
                else:
                    self.combined_capacity_anchor = 'N/A'
            else:
                self.combined_capacity_anchor = 'N/A'

            # Check: shear resistance of the base plate
            self.shear_resistance = round(0.45 * self.load_axial_compression, 2)  # N

            if self.load_shear_major > self.shear_resistance:
                self.shear_key_along_ColDepth = 'Yes'

                logger.warning("[Design for Shear] The shear resistance of the base plate assembly due to the friction between the base plate and "
                               "the grout/concrete material is {} kN".format(self.shear_resistance * 1e-3))
                logger.warning("The horizontal shear force - {} kN, exceeds the shear resistance of the base plate".
                               format(self.load_shear_major * 1e-3))
                logger.info("Providing shear key to resist additional shear")
            else:
                self.shear_key_along_ColDepth = 'No'

                logger.info("[Design for Shear] The shear resistance of the base plate assembly due to the friction between the base plate and "
                               "the grout/concrete material is {} kN".format(self.shear_resistance * 1e-3))
                logger.info("The horizontal shear force - {} kN, is less than the shear resistance of the base plate".
                               format(self.load_shear_major * 1e-3))
                logger.info("Shear key is not required")

            if self.load_shear_minor > self.shear_resistance:
                self.shear_key_along_ColWidth = 'Yes'

                logger.warning("[Design for Shear] The shear resistance of the base plate assembly due to the friction between the base plate and "
                               "the grout/concrete material is {} kN".format(self.shear_resistance * 1e-3))
                logger.warning("The horizontal shear force - {} kN, exceeds the shear resistance of the base plate".
                               format(self.load_shear_major * 1e-3))
                logger.info("Providing shear key to resist additional shear")
            else:
                self.shear_key_along_ColWidth = 'No'

                logger.info("[Design for Shear] The shear resistance of the base plate assembly due to the friction between the base plate and "
                               "the grout/concrete material is {} kN".format(self.shear_resistance * 1e-3))
                logger.info("The horizontal shear force - {} kN, is less than the shear resistance of the base plate".
                               format(self.load_shear_major * 1e-3))
                logger.info("Shear key is not required")

            # shear key design

            # key along major axis
            if self.shear_key_along_ColDepth == 'Yes':

                # self.stiff_key = Material(material_grade=self.dp_stif_key_material, thickness=0)
                self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, 0)

                # initialize key with minimum dimensions
                self.shear_key_depth_ColDepth = self.grout_thk + 100  # mm
                self.shear_key_len_ColDepth = round_up(self.column_D, 5)  # mm

                # check for bearing of the shear key on concrete (along major axis)
                self.shear_key_stress_ColDepth = (self.load_shear_major - self.shear_resistance) / (self.shear_key_len_ColDepth *
                                                                                                    self.shear_key_depth_ColDepth)  # N/mm^2

                # bearing check

                # step 1: updating the length of key, if the stress demand is more
                if self.shear_key_stress_ColDepth > self.bearing_strength_concrete:
                    key_dimensions = [self.shear_key_len_ColDepth]

                    n = 1
                    while (self.shear_key_stress_ColDepth > self.bearing_strength_concrete) and (key_dimensions[-1] < self.bp_length_provided):
                        key_update_dimensions = [key_dimensions[-1]]

                        for i in key_update_dimensions:
                            i += 5
                            key_dimensions.append(i)
                            i += 1

                        self.shear_key_len_ColDepth = key_dimensions[-1]
                        self.shear_key_stress_ColDepth = (self.load_shear_major - self.shear_resistance) / (self.shear_key_len_ColDepth *
                                                                                                            self.shear_key_depth_ColDepth)

                # check 2: updating the depth of key, if the stress demand is more and max length allowed is reached
                if self.shear_key_stress_ColDepth > self.bearing_strength_concrete:
                    key_dimensions = [self.shear_key_depth_ColDepth]

                    n = 1
                    while (self.shear_key_stress_ColDepth > self.bearing_strength_concrete) and (self.shear_key_depth_ColDepth <
                                                                                                 (0.5 * self.shear_key_len_ColDepth)):
                        key_update_dimensions = [key_dimensions[-1]]

                        for i in key_update_dimensions:
                            i += 5
                            key_dimensions.append(i)
                            i += 1

                        self.shear_key_depth_ColDepth = key_dimensions[-1]
                        self.shear_key_stress_ColDepth = (self.load_shear_major - self.shear_resistance) / (self.shear_key_len_ColDepth *
                                                                                                            self.shear_key_depth_ColDepth)
                if self.shear_key_stress_ColDepth > self.bearing_strength_concrete:
                    self.shear_key_stress_ColDepth = round(self.shear_key_stress_ColDepth, 2)
                    self.shear_key_design_status = False
                    self.safe = False
                    logger.warning("[Shear Key] The aspect ratio of the shear key (depth/length) exceeds 1/2, horizontal shear force (along the "
                                   "major axis) is very high")
                    logger.warning("The aspect ratio of the key is restricted to keep a check on the thickness of the key and prevent failure of the "
                                   "base plate due to bending")
                    logger.info("Osdag suggests to design the connection with embedded base plate")
                else:
                    # checking shear key thk

                    # load distribution along the depth of the key
                    self.shear_key_w_1 = (self.load_shear_major - self.shear_resistance) / self.shear_key_len_ColDepth  # N/mm
                    self.shear_key_w_1 = round(self.shear_key_w_1, 2)
                    self.shear_key_moment_1 = self.shear_key_w_1 * (self.shear_key_depth_ColDepth ** 2 / 2)  # N-mm, max moment
                    self.shear_key_thk_1 = math.sqrt((4 * self.shear_key_moment_1 * self.gamma_m0) / (self.stiff_key.fy *
                                                                                                      self.shear_key_depth_ColDepth))
                    self.shear_key_thk = max(self.shear_key_thk_1, self.column_tw)
                    sort_plate = filter(lambda x: self.shear_key_thk <= x <= self.standard_plate_thk[-1], self.standard_plate_thk)
                    for i in sort_plate:
                        self.shear_key_thk = i  # plate thickness provided (mm)
                        break

                    self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, self.shear_key_thk)
                    self.fy_key_1 = self.stiff_key.fy

                    self.moment_capacity_key1 = (((self.shear_key_depth_ColDepth * self.shear_key_thk ** 2) / 4) * self.fy_key_1) / self.gamma_m0
                    self.moment_capacity_key1 = round(self.moment_capacity_key1 * 1e-6, 2)

                self.shear_key_stress_ColDepth = round(self.shear_key_stress_ColDepth, 2)
            else:
                self.shear_key_len_ColDepth = 'N/A'
                self.shear_key_depth_ColDepth = 'N/A'
                self.shear_key_stress_ColDepth = 'N/A'
                self.shear_key_thk = 'N/A'

            # key along minor axis
            if self.shear_key_along_ColWidth == 'Yes':

                if (self.load_shear_minor <= self.load_shear_major) and (self.shear_key_along_ColDepth == 'Yes'):
                    self.shear_key_depth_ColWidth = self.shear_key_depth_ColDepth
                    self.shear_key_len_ColWidth = self.shear_key_len_ColDepth
                    self.shear_key_thk = self.shear_key_thk
                    self.shear_key_stress_ColWidth = self.shear_key_stress_ColDepth

                    self.shear_key_w_2 = (self.load_shear_minor - self.shear_resistance) / self.shear_key_len_ColWidth  # N/mm
                    self.shear_key_w_2 = round(self.shear_key_w_2, 2)
                    self.shear_key_moment_2 = self.shear_key_w_2 * (self.shear_key_depth_ColWidth ** 2 / 2)  # N-mm, max moment
                    self.shear_key_thk_2 = math.sqrt((4 * self.shear_key_moment_2 * self.gamma_m0) / (self.stiff_key.fy *
                                                                                                      self.shear_key_depth_ColWidth))
                    self.fy_key_2 = self.fy_key_1
                    self.moment_capacity_key2 = (((self.shear_key_depth_ColWidth * self.shear_key_thk ** 2) / 4) * self.stiff_key.fy) / self.gamma_m0
                    self.moment_capacity_key2 = round(self.moment_capacity_key2 * 1e-6, 2)

                else:
                    # self.stiff_key = Material(material_grade=self.dp_stif_key_material, thickness=self.shear_key_thk)
                    self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, 0)

                    # initialize key with minimum dimensions
                    self.shear_key_depth_ColWidth = self.grout_thk + 100  # mm
                    self.shear_key_len_ColWidth = self.column_bf  # mm

                    # check for bearing of the shear key on concrete (along major axis)
                    self.shear_key_stress_ColWidth = (self.load_shear_minor - self.shear_resistance) / (self.shear_key_len_ColWidth *
                                                                                                        self.shear_key_depth_ColWidth)  # N/mm^2

                    # bearing check

                    # step 1: updating the length of key, if the stress demand is more
                    if self.shear_key_stress_ColWidth > self.bearing_strength_concrete:
                        key_dimensions = [self.shear_key_len_ColWidth]

                        n = 1
                        while (self.shear_key_stress_ColWidth > self.bearing_strength_concrete) and (key_dimensions[-1] < self.bp_width_provided):
                            key_update_dimensions = [key_dimensions[-1]]

                            for i in key_update_dimensions:
                                i += 5
                                key_dimensions.append(i)
                                i += 1

                            self.shear_key_len_ColWidth = key_dimensions[-1]
                            self.shear_key_stress_ColWidth = (self.load_shear_minor - self.shear_resistance) / (self.shear_key_len_ColWidth *
                                                                                                                self.shear_key_depth_ColWidth)

                    # check 2: updating the depth of key, if the stress demand is more and max length allowed is reached
                    if self.shear_key_stress_ColWidth > self.bearing_strength_concrete:
                        key_dimensions = [self.shear_key_depth_ColWidth]

                        n = 1
                        while (self.shear_key_stress_ColWidth > self.bearing_strength_concrete) and (self.shear_key_depth_ColWidth <
                                                                                                     (0.5 * self.shear_key_len_ColWidth)):
                            key_update_dimensions = [key_dimensions[-1]]

                            for i in key_update_dimensions:
                                i += 5
                                key_dimensions.append(i)
                                i += 1

                            self.shear_key_depth_ColWidth = key_dimensions[-1]
                            self.shear_key_stress_ColWidth = (self.load_shear_minor - self.shear_resistance) / (self.shear_key_len_ColWidth *
                                                                                                                self.shear_key_depth_ColWidth)

                    if self.shear_key_stress_ColWidth > self.bearing_strength_concrete:
                        self.shear_key_stress_ColWidth = round(self.shear_key_stress_ColWidth, 2)
                        self.shear_key_design_status = False
                        self.safe = False

                        logger.warning("[Shear Key] The aspect ratio of the shear key (depth/length) exceeds 1/2, horizontal shear force (along "
                                       "the minor axis) is very high")
                        logger.warning(
                            "The aspect ratio of the key is restricted to keep a check on the thickness of the key and prevent failure of the "
                            "base plate due to bending")
                        logger.info("Osdag suggets to design the connection with embedded base plate")
                    else:
                        # checking shear key thk

                        # load distribution along the depth of the key
                        self.shear_key_w_2 = (self.load_shear_minor - self.shear_resistance) / self.shear_key_len_ColWidth  # N/mm
                        self.shear_key_w_2 = round(self.shear_key_w_2, 2)
                        self.shear_key_moment_2 = self.shear_key_w_2 * (self.shear_key_depth_ColWidth ** 2 / 2)  # N-mm, max moment
                        self.shear_key_thk_2 = math.sqrt((4 * self.shear_key_moment_2 * self.gamma_m0) / (self.stiff_key.fy *
                                                                                                          self.shear_key_depth_ColWidth))
                        self.shear_key_thk = max(self.shear_key_thk_2, self.column_tw)
                        sort_plate = filter(lambda x: self.shear_key_thk <= x <= self.standard_plate_thk[-1], self.standard_plate_thk)
                        for i in sort_plate:
                            self.shear_key_thk = i  # plate thickness provided (mm)
                            break

                        self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, self.shear_key_thk)
                        self.fy_key_2 = self.stiff_key.fy

                        self.moment_capacity_key2 = (((self.shear_key_depth_ColWidth * self.shear_key_thk ** 2) / 4) * self.fy_key_2) / self.gamma_m0
                        self.moment_capacity_key2 = round(self.moment_capacity_key2 * 1e-6, 2)

                    # if self.shear_key_design_status != False:
                    #     self.shear_key_stress_ColWidth = round(self.shear_key_stress_ColWidth, 2)
            else:
                self.shear_key_len_ColWidth = 'N/A'
                self.shear_key_depth_ColWidth = 'N/A'
                self.shear_key_stress_ColWidth = 'N/A'

                self.shear_key_design_status = True
                self.weld_size_shear_key = 'N/A'
                if self.shear_key_along_ColDepth == 'No':
                    self.shear_key_thk = 'N/A'
        else:
            self.combined_capacity_anchor = 'N/A'
            self.weld_size_shear_key = 'N/A'

            self.shear_key_along_ColDepth = 'No'
            self.shear_key_len_ColDepth = 'N/A'
            self.shear_key_depth_ColDepth = 'N/A'
            self.shear_key_stress_ColDepth = 'N/A'

            self.shear_key_along_ColWidth = 'No'
            self.shear_key_len_ColWidth = 'N/A'
            self.shear_key_depth_ColWidth = 'N/A'
            self.shear_key_stress_ColWidth = 'N/A'

            self.shear_key_design_status = True
            self.shear_key_thk = 'N/A'

        if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
            self.shear_key_len_ColDepth = max(self.shear_key_len_ColDepth, self.shear_key_len_ColWidth)
            self.shear_key_depth_ColDepth = max(self.shear_key_depth_ColDepth, self.shear_key_depth_ColWidth)
            self.shear_key_stress_ColDepth = (self.load_shear_major - self.shear_resistance) / (self.shear_key_len_ColDepth *
                                                                                                self.shear_key_depth_ColDepth)
            self.shear_key_stress_ColDepth = round(self.shear_key_stress_ColDepth, 2)

            self.shear_key_len_ColWidth = self.shear_key_len_ColDepth
            self.shear_key_depth_ColWidth = self.shear_key_depth_ColDepth
            self.shear_key_stress_ColWidth = (self.load_shear_minor - self.shear_resistance) / (self.shear_key_len_ColWidth *
                                                                                                self.shear_key_depth_ColWidth)
            self.shear_key_stress_ColWidth = round(self.shear_key_stress_ColWidth, 2)

        # design of anchor bolts to resist axial tension/uplift force - initial iteration
        if self.connectivity == 'Moment Base Plate':

            if self.load_axial_tension > 0:
                self.anchor_inside_flange = 'Yes'

                # hole diameter
                self.anchor_hole_dia_in = self.cl_10_2_1_bolt_hole_size(self.anchor_dia_inside_flange, self.dp_anchor_hole_in)  # mm

                self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_inside_flange[0],
                                                                                                     self.anchor_fu_fy_inside_flange[1],
                                                                                                     self.anchor_area_inside_flange[0],
                                                                                                     self.anchor_area_inside_flange[1],
                                                                                                     safety_factor_parameter=self.dp_weld_fab)  # N
                self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

                self.anchors_inside_flange = self.load_axial_tension / (self.tension_capacity_anchor_uplift * 1000)

                if self.shear_key_along_ColWidth == 'Yes':
                    self.anchors_inside_flange = round_up(self.anchors_inside_flange, 4)  # provide minimum 4 bolts in this case
                    # detailing check for this case is done in additional_calculations method
                else:
                    self.anchors_inside_flange = round_up(self.anchors_inside_flange, 2)

                    # detailing check - 2 bolts
                    end_available = (self.column_D - (2 * self.column_tf)) / 2

                    self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)  # inside flange
                    self.plate_washer_dim_in = self.plate_washer_details_in['side']  # washer dimension - inside flange, mm

                    self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_inside_flange, self.dp_anchor_hole_in,
                                                                              self.dp_detail_edge_type)
                    self.end_distance_in = max(self.end_distance_in, self.plate_washer_dim_in)
                    self.edge_distance_in = self.end_distance_in

                    if self.end_distance_in > end_available:
                        logger.warning("[Detailing Check] The detailing checks are not satisfied with 2 anchor bolts of {} mm diameter".
                                       format(self.anchor_dia_inside_flange))
                        logger.info("Re-designing the connection with anchor bolts of higher diameter and grade combination")
                        self.anchors_inside_flange = 4

                # tension demand
                self.tension_demand_anchor_uplift = self.load_axial_tension / self.anchors_inside_flange
                self.tension_demand_anchor_uplift = round(self.tension_demand_anchor_uplift / 1000, 2)  # kN

                # updating total number of anchor bolts required (bolts outside flange + inside flange)
                self.anchor_nos_provided = (2 * self.anchors_outside_flange) + self.anchors_inside_flange
            else:
                if self.load_moment_minor <= 0:
                    self.anchor_inside_flange = 'No'
                    self.tension_demand_anchor_uplift = 0
                    self.anchors_inside_flange = 0
                    self.anchor_nos_provided = (2 * self.anchors_outside_flange) + self.anchors_inside_flange
                    self.anchor_dia_inside_flange = 'N/A'
                    self.tension_capacity_anchor_uplift = 'N/A'
        else:
            self.tension_demand_anchor_uplift = 0

        # anchor columns outside flange
        if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 3):
            self.bolt_columns_outside_flange = 1
        else:
            self.bolt_columns_outside_flange = 2

        # update washer details after bolt checks- dictionary {inner diameter, side dimension, washer thickness}
        self.plate_washer_details_out = IS6649.square_washer_dimensions(self.anchor_dia_outside_flange)  # outside flange
        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):  # inside flange
            self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)

        # validation of anchor bolt length [Reference: IS 5624:1993, Table 1]
        self.anchor_length_min_out = self.table1('M' + str(self.anchor_dia_outside_flange))[1]
        self.anchor_length_max_out = self.table1('M' + str(self.anchor_dia_outside_flange))[2]

        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
            self.anchor_length_min_in = self.table1(('M' + str(self.anchor_dia_inside_flange)))[1]
            self.anchor_length_max_in = self.table1(('M' + str(self.anchor_dia_inside_flange)))[2]

        # design of anchor length - outside flange [Reference: Design of Steel Structures by N. Subramanian 2nd. edition 2018, Example 15.5]
        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
            self.anchor_length_provided_out = round(self.anchor_length_min_out, 2)  # mm

        # Equation: T_b = k * sqrt(fck) * (anchor_length_req)^1.5
        elif self.connectivity == 'Moment Base Plate':

            if self.moment_bp_case == 'Case1':
                self.anchor_length_provided_out = round(self.anchor_length_min_out, 2)  # mm
                if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
                    self.anchor_length_provided_in = round(self.anchor_length_min_in, 2)  # mm

            else:
                # length of anchor for cast-in situ anchor bolts (k = 15.5)
                self.anchor_length_provided_out = (self.tension_capacity_anchor * 1000 /
                                                   (15.5 * math.sqrt(self.bearing_strength_concrete / 0.45))) ** 0.67  # mm
                self.anchor_length_provided_out_report = round(self.anchor_length_provided_out, 2)
                self.anchor_length_provided_out = round_up(self.anchor_length_provided_out, 5)
                self.anchor_length_provided_out = max(self.anchor_length_provided_out, self.anchor_length_min_out)

            if self.load_axial_tension > 0:
                self.anchor_length_provided_in = (self.tension_capacity_anchor_uplift * 1000 /
                                                  (15.5 * math.sqrt(self.bearing_strength_concrete / 0.45))) ** (0.67)  # mm
                self.anchor_length_provided_in_report = round(self.anchor_length_provided_in, 2)
                self.anchor_length_provided_in = round_up(self.anchor_length_provided_in, 5)
                self.anchor_length_provided_in = max(self.anchor_length_provided_in, self.anchor_length_min_in)

            if self.load_moment_minor > 0:
                self.anchor_length_provided_in = self.anchor_length_min_in  # mm
                self.anchor_length_provided_in_report = self.anchor_length_min_in

            logger.info("[Anchor Bolt Length] The length of the anchor bolt is computed assuming the anchor bolt is casted in-situ"
                        " during the erection of the column.")

        # updating anchor length (adding the length above the concrete pedestal)

        # nut thickness
        self.nut_thk_out = IS1364Part3.nut_thick(self.anchor_dia_outside_flange)  # nut thickness, mm
        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
            self.nut_thk_in = IS1364Part3.nut_thick(self.anchor_dia_inside_flange)  # nut thickness, mm

        # square plate washer details
        self.plate_washer_thk_out = self.plate_washer_details_out['washer_thk']  # washer thickness, mm
        self.plate_washer_inner_dia_out = self.plate_washer_details_out['dia_in']  # inner dia, mm
        self.plate_washer_dim_out = self.plate_washer_details_out['side']  # dimensions of the square washer plate, mm

        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
            self.plate_washer_thk_in = self.plate_washer_details_in['washer_thk']  # washer thickness, mm
            self.plate_washer_inner_dia_in = self.plate_washer_details_in['dia_in']  # inner dia, mm
            self.plate_washer_dim_in = self.plate_washer_details_in['side']  # dimensions of the square washer plate, mm

        # anchor length - outside flange bolts
        self.anchor_len_below_footing_out = self.anchor_length_provided_out + self.nut_thk_out + 20  # mm, 20mm is extra
        self.anchor_len_above_footing_out = self.grout_thk + self.plate_thk_provided + self.plate_washer_thk_out + self.nut_thk_out + 20  # mm, 20 mm is extra len

        self.anchor_length_provided_out = self.anchor_len_below_footing_out + self.anchor_len_above_footing_out  # total length of the anchor bolt
        self.anchor_length_provided_out = round(self.anchor_length_provided_out, 2)

        # anchor length - inside flange bolts
        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
            self.anchor_len_below_footing_in = self.anchor_length_provided_in + self.nut_thk_in + 20  # mm
            self.anchor_len_above_footing_in = self.grout_thk + self.plate_thk_provided + self.plate_washer_thk_in + self.nut_thk_in + 20  # mm, 20 mm is extra len

            self.anchor_length_provided_in = self.anchor_len_below_footing_in + self.anchor_len_above_footing_in  # total length of the anchor bolt
            self.anchor_length_provided_in = round(self.anchor_length_provided_in, 2)
        else:
            self.anchor_length_provided_in = 'N/A'

        # calling value of the anchor length from user from design preferences
        if self.dp_anchor_length_out < self.anchor_length_provided_out:
            self.dp_anchor_length_out = self.anchor_length_provided_out

        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
            if self.dp_anchor_length_in < self.anchor_length_provided_in:
                self.dp_anchor_length_in = self.anchor_length_provided_in

        # length check
        if self.anchor_len_below_footing_out < self.anchor_length_min_out:
            logger.error("[Anchor Bolt Length] The length of the anchor bolt computed is less than the minimum recommended value")
            logger.info("[Anchor Bolt Length] The minimum length of the anchor recommended is {}".format(self.anchor_length_min_out))
            logger.info("[Anchor Bolt Length] Updating length of anchor bolt to minimum required value")
        elif self.anchor_len_below_footing_out > self.anchor_length_max_out:
            logger.error("[Anchor Bolt Length] The length of the anchor bolt computed is greater than the maximum recommended value")
            logger.info("[Anchor Bolt Length] The maximum length of the anchor recommended is {}".format(self.anchor_length_max_out))
            logger.info("[Anchor Bolt Length] Restricting the length of the anchor bolt within the maximum allowed value")
        else:
            logger.info("[Anchor Bolt Length] The recommended range for the length of the anchor bolt of thread size {} mm is as follows:"
                        .format(self.anchor_dia_outside_flange))
            logger.info("[Anchor Bolt Length] Minimum length = {} mm, Maximum length = {} mm."
                        .format(self.anchor_length_min_out, self.anchor_length_max_out))
            logger.info("[Anchor Bolt Length] The provided length of the anchor bolt is {} mm".format(self.anchor_length_provided_out))
            logger.info("[Anchor Bolt] Designer/Erector should provide adequate anchorage depending on the availability "
                        "of standard lengths and sizes, satisfying the recommended range")
            logger.info("[Anchor Bolt Length] Reference: IS 5624:1993, Table 1")

        if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):
            if self.anchor_len_below_footing_in < self.anchor_length_min_in:
                logger.error("[Anchor Bolt Length] The length of the anchor bolt computed is less than the minimum recommended value")
                logger.info("[Anchor Bolt Length] The minimum length of the anchor recommended is {}".format(self.anchor_length_min_in))
                logger.info("[Anchor Bolt Length] Updating length of anchor bolt to minimum required value")
            elif self.anchor_len_below_footing_in > self.anchor_length_max_in:
                logger.error("[Anchor Bolt Length] The length of the anchor bolt computed is greater than the maximum recommended value")
                logger.info("[Anchor Bolt Length] The maximum length of the anchor recommended is {}".format(self.anchor_length_max_in))
                logger.info("[Anchor Bolt Length] Restricting the length of the anchor bolt within the maximum allowed value")
            else:
                logger.info("[Anchor Bolt Length] The recommended range for the length of the anchor bolt of thread size {} mm is as follows:"
                            .format(self.anchor_dia_inside_flange))
                logger.info("[Anchor Bolt Length] Minimum length = {} mm, Maximum length = {} mm."
                            .format(self.anchor_length_min_in, self.anchor_length_max_in))
                logger.info("[Anchor Bolt Length] The provided length of the anchor bolt is {} mm".format(self.anchor_length_provided_in))
                logger.info("[Anchor Bolt] Designer/Erector should provide adequate anchorage depending on the availability "
                            "of standard lengths and sizes, satisfying the recommended range")
                logger.info("[Anchor Bolt Length] Reference: IS 5624:1993, Table 1")

    def design_weld(self):
        """ design weld for the base plate and stiffeners

        Args:

        Returns:
        """
        # define parameters for the stiffener plates
        # self.base_plate.connect_to_database_to_get_fy_fu(self.dp_bp_material, self.plate_thk_provided)  # update fy
        self.stiffener_fy = self.stiff_key.fy  # initialize fy, MPa
        self.epsilon = round(math.sqrt(250 / self.stiffener_fy), 2)

        # design the weld connecting the column and the stiffeners to the base plate
        self.weld_fu = min(self.dp_weld_fu_overwrite, self.dp_column_fu)

        # length of the stiffener plate available in case of stiffener requirement/or extra welding

        if self.connectivity == 'Hollow/Tubular Column Base':

            if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                self.stiffener_plt_len_along_D = (self.bp_length_provided - self.column_D) / 2  # mm, (for SHS & RHS)
                self.stiffener_plt_len_along_B = (self.bp_width_provided - self.column_bf) / 2  # mm, (for SHS & RHS)
                self.stiffener_plt_thk_min = min(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B) / (13.6 * self.epsilon)  # mm
                self.stiffener_plt_thk_min = round(self.stiffener_plt_thk_min, 2)
                self.stiffener_plt_thk = round_up(self.stiffener_plt_thk_min, 2, self.column_tf)
                self.stiffener_plt_height = max(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B) + 50  # mm
            else:
                self.stiffener_plt_len_across_D = round_down((self.bp_length_provided - self.column_D) / 2, 1)  # mm, (for CHS)
                self.stiffener_plt_thk_min = round(self.stiffener_plt_len_across_D / (13.6 * self.epsilon), 2)  # mm
                self.stiffener_plt_thk = round_up(self.stiffener_plt_thk_min, 2, self.column_tf)
                self.stiffener_plt_height = self.stiffener_plt_len_across_D + 50  # mm

            # update stiffener fy
            self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, self.stiffener_plt_thk)
            self.stiffener_fy = self.stiff_key.fy
            # self.epsilon = round(math.sqrt(250 / self.stiffener_fy), 2)
            # # update plate thk by incorporating the updated epsilon, if the plate thk in initial check is greater than 20mm
            # self.stiffener_plt_thk_min = round(self.stiffener_plt_len_across_D / (13.6 * self.epsilon), 2)  # mm
            # self.stiffener_plt_thk = round_up(self.stiffener_plt_thk_min, 2, self.column_tf)

        else:
            self.stiffener_plt_len_along_flange = (self.bp_width_provided - self.column_bf) / 2  # mm (each, along the flange)
            self.stiffener_plt_len_along_web = (self.bp_length_provided - self.column_D) / 2  # mm (each, along the web)
            self.stiffener_plt_len_across_web = max(self.stiffener_plt_len_along_flange,
                                                    self.stiffener_plt_len_along_web)  # mm (each, across the web)
            self.stiffener_plt_len_across_web = min(self.stiffener_plt_len_across_web, (self.bp_width_provided - self.column_tw) / 2)

        # design of fillet weld
        if self.weld_type == 'Fillet Weld':
            # defining the maximum limit of weld size that can be provided, which is equal to/less than the flange/web thickness
            self.weld_size_flange_max = round_down(self.column_tf, 2)  # mm
            self.weld_size_web_max = round_down(self.column_tw, 2)  # mm

            if self.connectivity == 'Welded Column Base':

                if self.dp_column_type == 'Rolled' or 'Welded':

                    # available length for welding along the flange and web of the column, without the stiffeners
                    length_available_flange = 2 * (self.column_bf + (self.column_bf - self.column_tw - (2 * self.column_r1)))  # mm
                    length_available_web = 2 * (self.column_D - (2 * self.column_tf) - (2 * self.column_r1))  # mm

                    # TODO: check end returns reduction
                    # Note: The effective length of weld is calculated by assuming 1% reduction in length at each end return. Since, the
                    # total number of end returns are 12, a total of 12% reduction (8% at flange and 4% at web) is incorporated into the
                    # respective 'effective' lengths.
                    self.effective_length_flange = length_available_flange - (0.08 * length_available_flange)  # mm
                    self.effective_length_web = length_available_web - (0.04 * length_available_web)  # mm

                    self.strength_unit_len = self.load_axial_compression / (self.effective_length_flange + self.effective_length_web)  # N/mm
                    self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                    [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                    [self.plate_thk_provided, self.column_tf], self.dp_weld_fab)  # mm

                    self.weld_size_web = self.weld_size  # mm

                    # check against maximum allowed weld size at web
                    # checking if stiffener plates are required for providing extra length of weld
                    if self.weld_size_web > self.weld_size_web_max:
                        # Case 1: Adding stiffeners along the flanges of the column on either sides (total four in number)
                        self.stiffener_along_flange = 'Yes'

                        # length available on each stiffener plate for (fillet) welding on either sides
                        # effective length assuming 2% reduction to incorporate end returns
                        self.eff_stiffener_plt_len_along_flange = (self.stiffener_plt_len_along_flange * 2) - \
                                                                  (0.02 * self.stiffener_plt_len_along_flange)  # mm (for each stiffener)
                        # total effective len available including four stiffeners
                        self.total_eff_len_available = self.effective_length_flange + self.effective_length_web + \
                                                       (4 * self.eff_stiffener_plt_len_along_flange)  # mm

                        # relative strength of weld per unit weld length and weld size including stiffeners along the flange
                        self.strength_unit_len = self.load_axial_compression / self.total_eff_len_available  # N/mm
                        self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                        [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                        [self.plate_thk_provided, self.column_tf], self.dp_weld_fab)  # mm

                        self.weld_size_web = self.weld_size  # mm

                        # Second iteration: checking the maximum weld size (at web)
                        if self.weld_size_web > self.weld_size_web_max:
                            # Case 2: Adding stiffeners along web of the column (total two in number)
                            self.stiffener_along_web = 'Yes'

                            self.eff_stiffener_plt_len_along_web = (self.stiffener_plt_len_along_web * 2) - (
                                    0.02 * self.stiffener_plt_len_along_web)  # mm

                            # TODO: deduce notch size
                            # total effective len available including four stiffeners along flange and two along the web
                            self.total_eff_len_available = self.total_eff_len_available + (2 * self.eff_stiffener_plt_len_along_web)  # mm

                            # relative strength of weld per unit weld length and weld size, including stiffeners along the flange and the web
                            self.strength_unit_len = self.load_axial_compression / self.total_eff_len_available  # N/mm
                            self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                            [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                            [self.plate_thk_provided, self.column_tf], self.dp_weld_fab)  # mm

                            self.weld_size_web = self.weld_size  # mm

                            # Third iteration: checking the maximum weld size (at web)
                            if self.weld_size_web > self.weld_size_web_max:
                                # Case 3: Adding stiffeners across the web of the column, between the column depth (total two in number)
                                self.stiffener_across_web = 'Yes'

                                len_required = (self.load_axial_compression * math.sqrt(3) * self.gamma_mw) / (
                                        0.7 * self.weld_size_web_max * self.weld_fu)  # mm
                                # Adding 16% of the total length to incorporate end returns (total 16 end returns in this case)
                                len_required = len_required + (0.16 * len_required)  # mm

                                len_stiffener_req_across_web = len_required - self.total_eff_len_available  # mm
                                len_stiffener_available_across_web = 4 * (
                                            (self.bp_width_provided / 2) - (self.column_tw / 2) - self.edge_distance_out)  # mm

                                if len_stiffener_req_across_web < len_stiffener_available_across_web:

                                    self.stiffener_plt_len_across_web = max(self.stiffener_plt_len_across_web, len_stiffener_req_across_web)  # mm
                                    self.total_eff_len_available = self.total_eff_len_available + (4 * self.stiffener_plt_len_across_web)  # mm

                                    # relative strength of weld per unit weld length,
                                    # and, weld size, including stiffeners along the flange, web and across the web
                                    self.strength_unit_len = self.load_axial_compression / self.total_eff_len_available  # N/mm
                                    self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                                    [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                                    [self.plate_thk_provided, self.column_tf],
                                                                                                    self.dp_weld_fab)  # mm

                                    self.weld_size_web = self.weld_size  # mm
                                    self.weld_size_flange = self.weld_size  # mm
                                    self.weld_size_stiffener = self.weld_size  # mm

                                    if self.weld_size_web > self.weld_size_web_max:
                                        self.design_status = False
                                        logger.info("Cannot design with fillet wed,  use groove weld,load is very high")
                                else:
                                    self.design_status = False
                                    # TODO: add log messages

                                # TODO: add log messages
                            else:
                                self.stiffener_across_web = 'No'
                                self.weld_size_flange = self.weld_size  # mm
                                self.weld_size_stiffener = self.weld_size  # mm

                        else:
                            self.stiffener_along_web = 'No'
                            self.stiffener_across_web = 'No'
                            self.weld_size_flange = self.weld_size  # mm
                            self.weld_size_stiffener = self.weld_size  # mm

                    else:
                        self.stiffener_along_flange = 'No'
                        self.stiffener_along_web = 'No'
                        self.stiffener_across_web = 'No'

                        self.weld_size_flange = self.weld_size  # mm
                        self.weld_size_stiffener = self.weld_size  # mm

                else:  # TODO: add checks for other type(s) of column section here (Example: built-up, star shaped etc.)
                    pass

            elif self.connectivity == 'Hollow/Tubular Column Base':
                if self.dp_column_designation[1:4] == 'SHS' or 'RHS':
                    length_available = 2 * (self.column_D + self.column_bf)  # mm, provide weld along the perimeter of the hollow section
                else:
                    length_available = self.column_D  # mm

                self.strength_unit_len = self.load_axial_compression / length_available  # N/mm
                self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                [self.plate_thk_provided, self.column_tf], self.dp_weld_fab)  # mm

                self.weld_size_hollow = self.weld_size  # mm

                # check for weld size
                if self.weld_size_hollow > self.weld_size_flange_max:
                    # provide stiffeners for extra welding
                    self.stiffener_along_D = 'Yes'  # stiffener along the longer side of RHS or any side of CHS
                    self.stiffener_along_B = 'Yes'  # stiffener along the shorter side of RHS or SHS

                    # weld design including stiffeners
                    if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                        self.stiffener_plt_len_along_D = (self.bp_length_provided - self.column_D) / 2  # mm
                        self.stiffener_plt_len_along_B = (self.bp_width_provided - self.column_bf) / 2  # mm
                        self.stiffener_plt_thk_min = (max(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B)) / (13.6 * self.epsilon)  # mm
                        self.stiffener_plt_thk = round_up(self.stiffener_plt_thk_min, 2, self.column_tf)
                        self.stiffener_plt_height = max(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B) + 50  # mm

                        self.stiffener_nos = 4
                        effective_length_available = (2 * (self.column_D + self.column_bf)) - (4 * self.stiffener_plt_thk) + \
                                                     (2 * (4 * min(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B)))  # mm

                    else:
                        self.stiffener_plt_len_across_D = (self.bp_length_provided - self.column_D) / 2  # mm
                        self.stiffener_plt_thk_min = self.stiffener_plt_len_across_D / (13.6 * self.epsilon)  # mm
                        self.stiffener_plt_thk = round_up(self.stiffener_plt_thk_min, 2, self.column_tf)
                        self.stiffener_plt_height = self.stiffener_plt_len_across_D + 50  # mm

                        self.stiffener_nos = 4
                        effective_length_available = self.column_D - (4 * self.stiffener_plt_thk) + (2 * (4 * self.stiffener_plt_len_across_D))  # mm

                    # weld size after providing stiffeners
                    self.strength_unit_len = self.load_axial_compression / effective_length_available  # N/mm
                    self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                    [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                    [self.plate_thk_provided, self.column_tf], self.dp_weld_fab)  # mm

                    self.weld_size_hollow = self.weld_size  # mm

                    # TODO: check if the weld size still exceeds the max allowable value
            else:
                self.stiffener_along_D = 'No'
                self.stiffener_along_B = 'No'

        # design of butt/groove weld
        else:
            if self.connectivity == 'Hollow/Tubular Column Base':
                self.stiffener_along_D = 'Yes'
                self.stiffener_along_B = 'Yes'
                self.stiffener_nos = 4
                self.weld_size_hollow = self.column_tf
                self.weld_size_stiffener = self.stiffener_plt_thk
            else:
                if self.connectivity == 'Welded Column Base':
                    self.stiffener_along_flange = 'No'
                    self.stiffener_along_web = 'No'

                elif self.connectivity == 'Moment Base Plate':
                    self.stiffener_along_flange = 'Yes'
                    self.stiffener_along_web = 'Yes'
                    self.stiffener_across_web = 'No'

                self.weld_size_flange = self.column_tf  # mm
                self.weld_size_web = self.column_tw  # mm

        # design of weld - column to base plate connection
        if self.connectivity == 'Welded Column Base':
            self.weld_len_flange = 2 * (self.column_bf + (self.column_bf - self.column_tw - (2 * self.column_r1) - (2 * self.column_r2)) - 10)  # mm
            self.weld_len_web = 2 * (self.column_D - (2 * self.column_tf) - (2 * self.column_r1) - (2 * 10))  # mm

            self.weld_bp.set_min_max_sizes(max(self.column_tf, self.column_tw), self.plate_thk_provided, special_circumstance=False,
                                           fusion_face_angle=90)

            if self.weld_bp.min_size < self.weld_bp.max_size:
                self.weld_bp_groove = 'No'
                self.weld_size_bp = (max(self.load_axial_compression, self.load_shear_major, self.load_shear_minor) * math.sqrt(3) * self.gamma_mw) / \
                                    (0.7 * (self.weld_len_flange + self.weld_len_web) * self.weld_fu)
                self.weld_size_bp = max(self.weld_size_bp + 2, self.weld_bp.min_size)
                self.weld_size_bp = round_up(self.weld_size_bp, 2)
                if self.weld_size_bp > self.weld_bp.max_size:
                    self.weld_bp_groove = 'Yes'
            else:
                self.weld_bp_groove = 'Yes'

        elif self.connectivity == 'Moment Base Plate':
            self.weld_len_web = 2 * (self.column_D - (2 * self.column_tf) - (2 * self.column_r1) - (2 * 10))  # mm

            self.weld_bp.set_min_max_sizes(self.column_tw, self.plate_thk_provided, special_circumstance=False, fusion_face_angle=90)

            if self.weld_bp.min_size < self.weld_bp.max_size:
                self.weld_bp_groove = 'No'
                self.weld_size_bp = (self.load_axial_compression * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_len_web * self.weld_fu)
                self.weld_size_bp = max(self.weld_size_bp, self.weld_bp.min_size)
                self.weld_size_bp = round_up(self.weld_size_bp, 2)
                if self.weld_size_bp > self.weld_bp.max_size:
                    self.weld_bp_groove = 'Yes'
            else:
                self.weld_bp_groove = 'Yes'

        elif self.connectivity == 'Hollow/Tubular Column Base':
            if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                self.weld_length = 2 * (self.column_D + self.column_bf)  # mm
            else:
                self.weld_length = math.pi * self.column_D  # mm

            self.weld_bp.set_min_max_sizes(self.column_tf, self.plate_thk_provided, special_circumstance=False, fusion_face_angle=90)

            if self.load_shear_major > 0 or self.load_shear_minor > 0:
                self.weld_bp_groove = 'No'
                self.weld_size_bp = (max(self.load_shear_major, self.load_shear_minor) * math.sqrt(3) * self.gamma_mw) / \
                                    (0.7 * self.weld_length * self.weld_fu)
                self.weld_size_bp = max(self.weld_size_bp, self.weld_bp.min_size)
                self.weld_size_bp = round_up(self.weld_size_bp, 2)
                if self.weld_size_bp > self.weld_bp.max_size:
                    self.weld_bp_groove = 'Yes'
            else:
                self.weld_bp_groove = 'No'
                self.weld_size_bp = min(round_up(self.weld_bp.min_size + 2, 2), round_down(self.weld_bp.max_size, 2))

        # design of weld for the shear key (shear key will be groove welded - single bevel)
        if (self.load_shear_major or self.load_shear_minor) > 0:
            if self.shear_key_along_ColDepth or self.shear_key_along_ColWidth == 'Yes':
                self.weld_size_shear_key = self.shear_key_thk
            else:
                self.weld_size_shear_key = 'N/A'
        else:
            pass

    def design_stiffeners(self):
        """ design and detail the stiffener plates

        Args:

        Returns:
        """
        # check for the limiting width to the thickness ratio of the column web [Reference: Cl. 3.7.2 and 3.7.4, Table 2, IS 800:2007]
        # if the web does not classify as 'Plastic' section, stiffener shall be provided across the web to limit the effective width
        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Moment Base Plate'):
            check = self.Table2_web_OfI_H_box_section((self.column_D - (2 * self.column_tf)), self.column_tw, self.dp_column_fy,
                                                      self.load_axial_compression, load_type='Compression', section_class='Plastic')
            # check returns a list
            # check[0]: Neutral axis at mid depth of the column
            # check[1]: Generally (when there is axial tension/uplift force acting on the column)
            # check[2]: Axial compression

            if (check[0] == 'Fail') or (check[1] == 'Fail') or (check[2] == 'Fail'):
                self.stiffener_across_web = 'Yes'
            else:
                self.stiffener_across_web = 'No'

        elif self.connectivity == 'Hollow/Tubular Column Base':
            if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                check = self.Table2_web_OfI_H_box_section((min(self.column_D, self.column_bf) - self.column_tf), self.column_tw, self.dp_column_fy,
                                                          self.load_axial_compression, load_type='Compression', section_class='Plastic')
                if (check[0] == 'Fail') or (check[1] == 'Fail') or (check[2] == 'Fail'):
                    self.stiffener_along_D = 'Yes'
                    self.stiffener_along_B = 'Yes'
                else:
                    self.stiffener_along_D = 'Yes'
                    self.stiffener_along_B = 'Yes'

            else:
                check = self.Table2_hollow_tube(self.column_D, self.column_tf, self.dp_column_fy, load='Axial Compression', section_class='Plastic')
                if check == 'Fail':
                    self.stiffener_along_D = 'Yes'
                else:
                    self.stiffener_along_D = 'Yes'
                    logger.info("[Section Classification] The CHS subjected to purely axial load is classified as plastic section "
                                "[Ref. Table 2, IS 800:2007]")
                    logger.info("The column does not require additional stiffening")
                    logger.info("Providing stiffeners to resist the bending of the base plate due to the bearing stress")

        if (self.connectivity == 'Moment Base Plate') and (self.load_moment_minor > 0):
            self.stiffener_across_web = 'Yes'

        # design of stiffener
        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Moment Base Plate'):
            # self.stiffener_across_web = 'Yes'
            if (self.stiffener_along_flange == 'Yes') or (self.stiffener_along_web == 'Yes') or (self.stiffener_across_web == 'Yes'):

                # thickness of the stiffener plate as per Table 2 of IS 800:2007 [b/t_f <= 13.6 * epsilon] (semi-compact)
                if self.bolt_columns_outside_flange == 2:  # TODO: CAD for this?
                    self.thk_req_stiffener_along_flange = round((self.stiffener_plt_len_along_flange / 2) / (13.6 * self.epsilon), 2)  # mm
                    self.thk_req_stiffener_along_web = round((self.stiffener_plt_len_along_web / 2) / (13.6 * self.epsilon), 2)  # mm
                    self.thk_req_stiffener_across_web = round((self.stiffener_plt_len_across_web / 2) / (13.6 * self.epsilon), 2)  # mm
                else:
                    self.thk_req_stiffener_along_flange = round(self.stiffener_plt_len_along_flange / (13.6 * self.epsilon), 2)  # mm
                    self.thk_req_stiffener_along_web = round(self.stiffener_plt_len_along_web / (13.6 * self.epsilon), 2)  # mm
                    self.thk_req_stiffener_across_web = round(self.stiffener_plt_len_across_web / (13.6 * self.epsilon), 2)  # mm

                # stiffener plate should be at-least equal to the flange thickness along the flange and web thickness along the web

                # along flange
                self.stiffener_plt_thick_along_flange = round_up(self.thk_req_stiffener_along_flange, 2, self.column_tf)  # mm
                sort_plate = filter(lambda x: self.stiffener_plt_thick_along_flange <= x <= self.standard_plate_thk[-1], self.standard_plate_thk)
                for i in sort_plate:
                    self.stiffener_plt_thick_along_flange = i  # plate thickness provided (mm)
                    break

                # along web
                self.stiffener_plt_thick_along_web = round_up(self.thk_req_stiffener_along_web, 2, self.column_tw)  # mm
                sort_plate = filter(lambda x: self.stiffener_plt_thick_along_web <= x <= self.standard_plate_thk[-1], self.standard_plate_thk)
                for i in sort_plate:
                    self.stiffener_plt_thick_along_web = i  # plate thickness provided (mm)
                    break

                # across web
                self.stiffener_plt_thick_across_web = round_up(self.thk_req_stiffener_across_web, 2, self.column_tw)  # mm
                sort_plate = filter(lambda x: self.stiffener_plt_thick_across_web <= x <= self.standard_plate_thk[-1], self.standard_plate_thk)
                for i in sort_plate:
                    self.stiffener_plt_thick_across_web = i  # plate thickness provided (mm)
                    break

                # Check 1: update stiffener fy
                # 1. Stiffener along flange
                self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, self.stiffener_plt_thick_along_flange)
                self.stiffener_fy_along_flange = self.stiff_key.fy
                self.epsilon_st_along_flange = self.epsilon
                # self.epsilon_st_along_flange = round(math.sqrt(250 / self.stiffener_fy_along_flange), 2)

                # 2. Stiffener along web
                self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, self.stiffener_plt_thick_along_web)
                self.stiffener_fy_along_web = self.stiff_key.fy
                self.epsilon_st_along_web = self.epsilon
                # self.epsilon_st_along_web = round(math.sqrt(250 / self.stiffener_fy_along_web), 2)

                # 3. Stiffener across web
                self.stiff_key.connect_to_database_to_get_fy_fu(self.dp_stif_key_material, self.stiffener_plt_thick_across_web)
                self.stiffener_fy_across_web = self.stiff_key.fy
                self.epsilon_st_across_web = self.epsilon
                # self.epsilon_st_across_web = round(math.sqrt(250 / self.stiffener_fy_across_web), 2)

                # Check 2: update stiffener thk based on updated fy and epsilon (if the initial thk exceeds 20 mm)
                # if self.bolt_columns_outside_flange == 2:
                #     self.thk_req_stiffener_along_flange = (self.stiffener_plt_len_along_flange / 2) / (13.6 * self.epsilon_st_along_flange)  # mm
                #     self.thk_req_stiffener_along_web = (self.stiffener_plt_len_along_web / 2) / (13.6 * self.epsilon_st_along_web)  # mm
                #     self.thk_req_stiffener_across_web = (self.stiffener_plt_len_across_web / 2) / (13.6 * self.epsilon_st_across_web)  # mm
                # else:
                #     self.thk_req_stiffener_along_flange = self.stiffener_plt_len_along_flange / (13.6 * self.epsilon_st_along_flange)  # mm
                #     self.thk_req_stiffener_along_web = self.stiffener_plt_len_along_web / (13.6 * self.epsilon_st_along_web)  # mm
                #     self.thk_req_stiffener_across_web = self.stiffener_plt_len_across_web / (13.6 * self.epsilon_st_across_web)  # mm
                #
                # self.stiffener_plt_thick_along_flange = round_up(self.thk_req_stiffener_along_flange, 2, self.column_tf)  # mm
                # self.stiffener_plt_thick_along_web = round_up(self.thk_req_stiffener_along_web, 2, self.column_tw)  # mm
                # self.stiffener_plt_thick_across_web = round_up(self.thk_req_stiffener_across_web, 2, self.column_tw)  # mm

                # height of the stiffener plate
                # the size of the landing is 100 mm along its vertical side and 50 mm along its horizontal side
                # the assumed inclination of the stiffener plate is 45 degrees
                self.stiffener_plt_height_along_flange = self.stiffener_plt_len_along_flange + 50  # mm
                self.stiffener_plt_height_along_web = self.stiffener_plt_len_along_web + 50  # mm
                self.stiffener_plt_height_across_web = self.stiffener_plt_len_across_web + 50  # mm

                # defining stresses for the connectivity types
                # sigma_max_zz - at the edge of the base plate on compression side
                # sigma_xx - at the critical section (0.95 * column depth) of the base plate on compression side
                # sigma_web - at the centre of the base plate on compression side
                if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                    self.moment_bp_case = 'N/A'
                    self.sigma_max_zz = self.w  # MPa
                    self.sigma_xx = self.w  # MPa
                    self.sigma_web = self.w  # MPa
                    self.sigma_lby2 = self.w
                    self.sigma_avg = self.w  # MPa

                    self.y = 0.0
                    self.critical_xx = 0.0
                else:
                    if self.moment_bp_case == 'Case1':
                        self.sigma_max_zz = round(self.sigma_max_zz, 2)
                        self.sigma_min_zz = round(self.sigma_min_zz, 2)
                        self.sigma_xx = round(self.sigma_xx, 2)
                        self.sigma_web = round(self.sigma_min_zz + ((self.sigma_max_zz - self.sigma_min_zz) / 2), 2)
                        self.sigma_lby2 = round(self.sigma_min_zz + ((self.sigma_max_zz - self.sigma_min_zz) / 2), 2)
                        self.sigma_avg = round((self.sigma_max_zz + self.sigma_lby2) / 2, 2)  # for stiffener along flange
                        self.sigma_avg_2 = round((self.sigma_max_zz + self.sigma_xx) / 2, 2)  # for stiffener along web

                        self.y = 0.0
                    else:
                        self.sigma_max_zz = round(self.max_bearing_stress, 2)
                        self.sigma_min_zz = 0.0
                        self.sigma_lby2 = 0.0

                        if self.y > self.critical_xx:
                            self.sigma_xx = (self.max_bearing_stress * (self.y - ((self.bp_length_provided - (0.95 * self.column_D)) / 2))) / self.y
                            self.sigma_avg = ((self.sigma_max_zz + 0.0) / 2)  # for stiffener along flange
                        else:
                            self.sigma_xx = self.max_bearing_stress
                            self.sigma_avg = ((self.sigma_max_zz + self.sigma_xx) / 2)  # for stiffener along flange

                        self.sigma_avg_2 = round((self.sigma_max_zz + self.sigma_xx) / 2, 2)  # for stiffener along web

                        self.sigma_avg = round(self.sigma_avg, 2)
                        self.sigma_xx = round(self.sigma_xx, 2)

                        if self.y < (self.bp_length_provided / 2):
                            self.sigma_web = 0.0
                        else:
                            self.sigma_web = (self.max_bearing_stress * (self.y - (self.bp_length_provided / 2))) / self.y
                            self.sigma_web = round(self.sigma_web, 2)

                # shear yielding and moment capacity checks for the stiffener - along the flange
                if self.stiffener_along_flange == 'Yes':

                    # Note: the loop below calculates the influence area lying under the stiffener
                    # it will be helpful for the reader in interpreting the calculation by referring the Base Plate DDCL

                    # shear demand
                    if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                        self.shear_on_stiffener_along_flange = self.sigma_avg * (self.bp_length_provided / 2) * self.stiffener_plt_len_along_flange
                    else:
                        if self.moment_bp_case == 'Case1':
                            self.shear_on_stiffener_along_flange = self.sigma_avg * (self.bp_length_provided / 2) * \
                                                                   self.stiffener_plt_len_along_flange
                        else:
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 4):
                                self.shear_on_stiffener_along_flange = self.sigma_avg * self.y * self.stiffener_plt_len_along_flange
                            else:
                                if self.y > self.critical_xx:
                                    self.shear_on_stiffener_along_flange = self.sigma_avg * (self.y - self.critical_xx) * \
                                                                           self.stiffener_plt_len_along_flange + \
                                                                           self.sigma_avg * self.critical_xx * \
                                                                           self.stiffener_plt_len_along_flange * (1/2)
                                else:
                                    self.shear_on_stiffener_along_flange = self.sigma_avg * self.y * self.stiffener_plt_len_along_flange * (1/2)

                    self.shear_on_stiffener_along_flange = round((self.shear_on_stiffener_along_flange / 1000), 3)  # kN

                    # moment demand
                    if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                        self.moment_on_stiffener_along_flange = self.w * (self.bp_length_provided / 2) * \
                                                                self.stiffener_plt_len_along_flange * (self.stiffener_plt_len_along_flange / 2)
                    else:
                        if self.moment_bp_case == 'Case1':
                            self.moment_on_stiffener_along_flange = self.sigma_avg * (self.bp_length_provided / 2) * \
                                                                    (self.stiffener_plt_len_along_flange ** 2 / 2)

                        else:
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 4):
                                self.moment_on_stiffener_along_flange = self.sigma_avg * self.y * self.stiffener_plt_len_along_flange * \
                                                                        (self.stiffener_plt_len_along_flange / 2)

                            else:
                                if self.y > self.critical_xx:
                                    self.moment_on_stiffener_along_flange = self.sigma_avg * (self.y - self.critical_xx) * \
                                                                            self.stiffener_plt_len_along_flange * \
                                                                            (self.stiffener_plt_len_along_flange / 2) + \
                                                                            self.sigma_avg * self.critical_xx * self.stiffener_plt_len_along_flange * \
                                                                            (self.stiffener_plt_len_along_flange / 2) * (1/2)
                                else:
                                    self.moment_on_stiffener_along_flange = self.sigma_avg * self.y * self.stiffener_plt_len_along_flange * (1/2) * \
                                                                            (self.stiffener_plt_len_along_flange / 2)

                    self.moment_on_stiffener_along_flange = round((self.moment_on_stiffener_along_flange * 10 ** -6), 3)  # kNm

                    # shear and moment capacity calculations
                    self.shear_capa_stiffener_along_flange = IS800_2007.cl_8_4_design_shear_strength((self.stiffener_plt_height_along_flange *
                                                                                                      self.stiffener_plt_thick_along_flange),
                                                                                                     self.stiffener_fy_along_flange)
                    self.shear_capa_stiffener_along_flange = round((self.shear_capa_stiffener_along_flange / 1000), 3)  # kN

                    self.z_e_stiffener_along_flange = (self.stiffener_plt_thick_along_flange * self.stiffener_plt_height_along_flange ** 2) / 6  # mm^3

                    self.moment_capa_stiffener_along_flange = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener_along_flange, 1,
                                                                                                           self.stiffener_fy_along_flange,
                                                                                                           section_class='semi-compact')
                    self.moment_capa_stiffener_along_flange = round((self.moment_capa_stiffener_along_flange * 10 ** -6), 3)  # kNm

                    # checks
                    if self.shear_on_stiffener_along_flange > (0.6 * self.shear_capa_stiffener_along_flange):
                        logger.warning("[Shear Check - Stiffener] The stiffener along the flange fails the shear check")
                        logger.warning(" The shear demand on the stiffener ({} kN) exceeds 60% of it's capacity ({} kN)".
                                       format(round(self.shear_on_stiffener_along_flange, 2), round(0.6 * self.shear_capa_stiffener_along_flange, 2)))
                        logger.info("Increasing the thickness of the stiffener and re-checking against shear demand")

                        n = 1
                        while self.shear_on_stiffener_along_flange > (0.6 * self.shear_capa_stiffener_along_flange):
                            self.stiffener_plt_thick_along_flange += 2
                            sort_plate = filter(lambda x: self.stiffener_plt_thick_along_flange <= x <= self.standard_plate_thk[-1],
                                                self.standard_plate_thk)
                            for i in sort_plate:
                                self.stiffener_plt_thick_along_flange = i  # plate thickness provided (mm)
                                break

                            self.shear_capa_stiffener_along_flange = IS800_2007.cl_8_4_design_shear_strength((self.stiffener_plt_height_along_flange *
                                                                                                              self.stiffener_plt_thick_along_flange),
                                                                                                             self.stiffener_fy_along_flange)
                            self.shear_capa_stiffener_along_flange = round((self.shear_capa_stiffener_along_flange / 1000), 3)  # kN

                            n += 1

                        # re-calculating the moment capacity by incorporating the improvised stiffener thickness along flange
                        self.z_e_stiffener_along_flange = (self.stiffener_plt_thick_along_flange * self.stiffener_plt_height_along_flange ** 2) / 6  # mm^3

                        self.moment_capa_stiffener_along_flange = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener_along_flange, 1,
                                                                                                               self.stiffener_fy_along_flange,
                                                                                                               section_class='semi-compact')
                        self.moment_capa_stiffener_along_flange = round((self.moment_capa_stiffener_along_flange * 10 ** -6), 3)  # kNm

                    if self.moment_on_stiffener_along_flange > self.moment_capa_stiffener_along_flange:
                        logger.warning("[Moment Check - Stiffener] The stiffener along the flange fails the moment check")
                        logger.warning("The moment demand on the stiffener ({} kNm) exceeds it's capacity ({} kNm)".
                                       format(round(self.moment_on_stiffener_along_flange, 2), round(self.moment_capa_stiffener_along_flange, 2)))
                        logger.info("Increasing the thickness of the stiffener and re-checking against moment demand")

                        n = 1
                        while self.moment_on_stiffener_along_flange > self.moment_capa_stiffener_along_flange:
                            self.stiffener_plt_thick_along_flange += 2
                            sort_plate = filter(lambda x: self.stiffener_plt_thick_along_flange <= x <= self.standard_plate_thk[-1],
                                                self.standard_plate_thk)
                            for i in sort_plate:
                                self.stiffener_plt_thick_along_flange = i  # plate thickness provided (mm)
                                break

                            # re-calculating the moment capacity by incorporating the improvised stiffener thickness along flange

                            self.z_e_stiffener_along_flange = (self.stiffener_plt_thick_along_flange * self.stiffener_plt_height_along_flange ** 2) / 6  # mm^3

                            self.moment_capa_stiffener_along_flange = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener_along_flange, 1,
                                                                                                                   self.stiffener_fy_along_flange,
                                                                                                                   section_class='semi-compact')
                            self.moment_capa_stiffener_along_flange = round((self.moment_capa_stiffener_along_flange * 10 ** -6), 3)  # kNm
                            n += 1

                        # re-calculating the shear capacity by incorporating the improvised stiffener thickness along flange
                        self.shear_capa_stiffener_along_flange = IS800_2007.cl_8_4_design_shear_strength((self.stiffener_plt_height_along_flange *
                                                                                                          self.stiffener_plt_thick_along_flange),
                                                                                                         self.stiffener_fy_along_flange)
                        self.shear_capa_stiffener_along_flange = round((self.shear_capa_stiffener_along_flange / 1000), 3)  # kN

                # shear yielding and moment capacity checks for the stiffener - along the web
                if self.stiffener_along_web == 'Yes':

                    # shear demand
                    if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                        self.shear_on_stiffener_along_web = self.sigma_avg * self.stiffener_plt_len_along_web * self.column_bf
                    else:
                        if self.moment_bp_case == 'Case1':
                            self.shear_on_stiffener_along_web = self.sigma_avg_2 * self.stiffener_plt_len_along_web * self.column_bf
                        else:
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 4):
                                self.shear_on_stiffener_along_web = self.sigma_avg_2 * self.stiffener_plt_len_along_web * self.column_bf
                            else:
                                self.shear_on_stiffener_along_web = (self.sigma_avg_2 * self.critical_xx * self.stiffener_plt_len_along_flange *
                                                                     (1 / 2)) + (self.sigma_avg_2 * (self.column_bf / 2) *
                                                                                 self.stiffener_plt_len_along_web)

                    self.shear_on_stiffener_along_web = round((self.shear_on_stiffener_along_web / 1000), 3)  # kN

                    # moment demand
                    if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                        self.moment_on_stiffener_along_web = self.w * (self.column_bf + self.stiffener_plt_len_along_web) * \
                                                             (self.stiffener_plt_len_along_web / 2)
                    else:
                        if self.moment_bp_case == 'Case1':
                            self.moment_on_stiffener_along_web = (self.sigma_xx * (self.column_bf * self.stiffener_plt_len_along_web) *
                                                             (self.stiffener_plt_len_along_web / 2)) + ((self.sigma_max_zz - self.sigma_xx) *
                                                                                                        self.stiffener_plt_len_along_web * (1/2)
                                                                                                        * self.column_bf *
                                                                                                        (2 / 3) * self.stiffener_plt_len_along_web)
                        else:
                            if (self.anchors_outside_flange == 2) or (self.anchors_outside_flange == 4):
                                self.moment_on_stiffener_along_web = (self.sigma_xx * (self.column_bf * self.stiffener_plt_len_along_web) *
                                                             (self.stiffener_plt_len_along_web / 2)) + ((self.sigma_max_zz - self.sigma_xx) *
                                                                                                        self.stiffener_plt_len_along_web * (1/2)
                                                                                                        * self.column_bf *
                                                                                                        (2 / 3) * self.stiffener_plt_len_along_web)
                            else:
                                if self.y > self.critical_xx:
                                    self.moment_on_stiffener_along_web = (self.sigma_xx * (((self.column_bf / 2) * self.stiffener_plt_len_along_web) +
                                                                                           (self.stiffener_plt_len_along_web *
                                                                                            self.stiffener_plt_len_along_flange * (1 /2))) *
                                                                          (self.stiffener_plt_len_along_web / 2)) + \
                                                                         ((self.sigma_max_zz - self.sigma_xx) * ((self.stiffener_plt_len_along_web *
                                                                          (1/2) * (self.column_bf / 2)) + ((1 / 2) * self.stiffener_plt_len_along_web
                                                                                                           * self.stiffener_plt_len_along_flange)) *
                                                                          ((2 / 3) * self.stiffener_plt_len_along_web))
                                else:
                                    self.moment_on_stiffener_along_web = self.sigma_max_zz * (((self.column_bf / 2) *
                                                                                               self.stiffener_plt_len_along_web) +
                                                                                              ((1 / 2) * self.stiffener_plt_len_along_web *
                                                                                               self.stiffener_plt_len_along_flange)) * \
                                                                         (self.stiffener_plt_len_along_web / 2)

                    self.moment_on_stiffener_along_web = round((self.moment_on_stiffener_along_web * 10 ** -6), 3)  # kNm

                    # shear and moment capacity calculations
                    self.shear_capa_stiffener_along_web = IS800_2007.cl_8_4_design_shear_strength(self.stiffener_plt_height_along_web *
                                                                                                  self.stiffener_plt_thick_along_web,
                                                                                                  self.stiffener_fy_along_web)
                    self.shear_capa_stiffener_along_web = round((self.shear_capa_stiffener_along_web / 1000), 3)  # kN

                    self.z_e_stiffener_along_web = (self.stiffener_plt_thick_along_web * self.stiffener_plt_height_along_web ** 2) / 6  # mm^3

                    self.moment_capa_stiffener_along_web = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener_along_web, 1,
                                                                                                        self.stiffener_fy_along_web,
                                                                                                        section_class='semi-compact')
                    self.moment_capa_stiffener_along_web = round((self.moment_capa_stiffener_along_web * 10 ** -6), 3)  # kNm

                    # checks
                    if self.shear_on_stiffener_along_web > (0.6 * self.shear_capa_stiffener_along_web):
                        logger.warning("[Shear Check - Stiffener] The stiffener along the web fails the shear check")
                        logger.warning("The shear demand on the stiffener ({} kN) exceeds 60% of it's capacity ({} kN)".
                                       format(round(self.shear_on_stiffener_along_web, 2), round(0.6 * self.shear_capa_stiffener_along_web, 2)))
                        logger.info("Increasing the thickness of the stiffener and re-checking against shear demand")

                        n = 1
                        while self.shear_on_stiffener_along_web > (0.6 * self.shear_capa_stiffener_along_web):
                            self.stiffener_plt_thick_along_web += 2
                            sort_plate = filter(lambda x: self.stiffener_plt_thick_along_web <= x <= self.standard_plate_thk[-1],
                                                self.standard_plate_thk)
                            for i in sort_plate:
                                self.stiffener_plt_thick_along_web = i  # plate thickness provided (mm)
                                break

                            self.shear_capa_stiffener_along_web = IS800_2007.cl_8_4_design_shear_strength(self.stiffener_plt_height_along_web *
                                                                                                          self.stiffener_plt_thick_along_web,
                                                                                                          self.stiffener_fy_along_web)
                            self.shear_capa_stiffener_along_web = round((self.shear_capa_stiffener_along_web / 1000), 3)  # kN

                            n += 1

                        # re-calculating the moment capacity by incorporating the improvised stiffener thickness along web
                        self.z_e_stiffener_along_web = (self.stiffener_plt_thick_along_web * self.stiffener_plt_height_along_web ** 2) / 6  # mm^3
                        self.moment_capa_stiffener_along_web = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener_along_web, 1,
                                                                                                            self.stiffener_fy_along_web,
                                                                                                            section_class='semi-compact')
                        self.moment_capa_stiffener_along_web = round((self.moment_capa_stiffener_along_web * 10 ** -6), 3)  # kNm

                    if self.moment_on_stiffener_along_web > self.moment_capa_stiffener_along_web:
                        logger.warning("[Moment Check - Stiffener] The stiffener along the flange fails the moment check")
                        logger.warning("[Moment Check - Stiffener] The moment demand on the stiffener ({} kNm) exceeds it's capacity ({} kNm)".
                                       format(round(self.moment_on_stiffener_along_web, 2), round(self.moment_capa_stiffener_along_web, 2)))
                        logger.info("Increasing the thickness of the stiffener and re-checking against moment demand")

                        n = 1
                        while self.moment_on_stiffener_along_web > self.moment_capa_stiffener_along_web:
                            self.stiffener_plt_thick_along_web += 2
                            sort_plate = filter(lambda x: self.stiffener_plt_thick_along_web <= x <= self.standard_plate_thk[-1],
                                                self.standard_plate_thk)
                            for i in sort_plate:
                                self.stiffener_plt_thick_along_web = i  # plate thickness provided (mm)
                                break

                            # re-calculating the moment capacity by incorporating the improvised stiffener thickness along web
                            self.z_e_stiffener_along_web = (self.stiffener_plt_thick_along_web * self.stiffener_plt_height_along_web ** 2) / 6  # mm^3
                            self.moment_capa_stiffener_along_web = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener_along_web, 1,
                                                                                                                self.stiffener_fy_along_web,
                                                                                                                section_class='semi-compact')
                            self.moment_capa_stiffener_along_web = round((self.moment_capa_stiffener_along_web * 10 ** -6), 3)  # kNm
                            n += 1

                if self.stiffener_across_web == 'Yes':

                    # provide 4 bolts to resist uplift force when stiffener is required across the web
                    if self.load_axial_tension > 0:
                        self.anchor_nos_provided = self.anchor_nos_provided - self.anchors_inside_flange
                        if self.anchors_inside_flange <= 2:
                            self.anchors_inside_flange = 4

                            self.anchor_nos_provided = self.anchor_nos_provided + self.anchors_inside_flange

                # weld size at the stiffener plate
                # TODO: check the weld size at stiffener
                # self.weld_size_stiffener = self.weld_size_flange  # mm

                # self.weld_size_vertical_flange = self.cl_10_5_2_3_min_weld_size(self.column_tf, self.stiffener_plt_thick_along_flange)
                # self.weld_size_vertical_flange = max(self.weld_size_vertical_flange, 6)  # mm
                #
                # self.weld_size_vertical_web = self.cl_10_5_2_3_min_weld_size(self.column_tw, self.stiffener_plt_thick_along_web)
                # self.weld_size_vertical_web = max(self.weld_size_vertical_web, 6)  # mm

            # design of the stiffener plate between the column depth to support the outstanding stiffeners, when there are 3 or 6 bolts required
            # the governing ratio is D/t_g < 29.30 (Table 2, IS 800:2007)
            if self.connectivity == 'Moment Base Plate':
                if (self.anchors_outside_flange == 3) or (self.anchors_outside_flange == 6):

                    self.stiffener_inside_flange = 'Yes'

                    self.notch_stiffener_inside_flange = max(round(1.5 * self.column_r1, 2), 15)
                    self.stiffener_plt_len_btwn_D_out = self.column_D - (2 * self.column_tf)  # mm, outer side
                    self.stiffener_plt_len_btwn_D_in = self.stiffener_plt_len_btwn_D_out - self.notch_stiffener_inside_flange  # mm, inner side
                    self.stiffener_plt_width_btwn_D = round((self.column_bf - self.column_tw - (2 * self.notch_stiffener_inside_flange)) / 2)  # mm

                    self.stiffener_plt_thick_btwn_D_1 = round(self.stiffener_plt_len_btwn_D_out / (29.3 * 1), 2)
                    self.stiffener_plt_thick_btwn_D_2 = round(max(self.column_tf, self.stiffener_plt_thick_along_web), 2)
                    self.stiffener_plt_thick_btwn_D = max(self.stiffener_plt_thick_btwn_D_1, self.stiffener_plt_thick_btwn_D_2)

                    sort_plate = filter(lambda x: self.stiffener_plt_thick_btwn_D <= x <= self.standard_plate_thk[-1],
                                        self.standard_plate_thk)
                    for i in sort_plate:
                        self.stiffener_plt_thick_btwn_D = i  # plate thickness provided (mm)
                        break
                else:
                    self.stiffener_inside_flange = 'No'
                    self.notch_stiffener_inside_flange = 'N/A'
                    self.stiffener_plt_len_btwn_D_out = 'N/A'
                    self.stiffener_plt_len_btwn_D_in = 'N/A'
                    self.stiffener_plt_width_btwn_D = 'N/A'
                    self.stiffener_plt_thick_btwn_D = 'N/A'
            else:
                self.stiffener_inside_flange = 'No'
                self.notch_stiffener_inside_flange = 'N/A'
                self.stiffener_plt_len_btwn_D_out = 'N/A'
                self.stiffener_plt_len_btwn_D_in = 'N/A'
                self.stiffener_plt_width_btwn_D = 'N/A'
                self.stiffener_plt_thick_btwn_D = 'N/A'

            # weld checks of the stiffener welds - Combination of stresses [Reference: Cl. 10.5.10.1, IS 800:2007]

            # if self.stiffener_along_flange == 'Yes':
            #     # Stiffener along flange - weld connecting stiffener to the base plate
            #     # the weld will have shear due to the bearing force and axial force due to in-plane bending of the stiffener
            #     f_a = (self.shear_on_stiffener_along_flange * 1000 / 2) / (
            #                 0.7 * self.weld_size_stiffener * self.stiffener_plt_len_along_flange)  # MPa
            #     q = (self.moment_on_stiffener_along_flange * 10 ** 6 / self.stiffener_plt_height_along_flange) \
            #         / (0.7 * self.weld_size_stiffener * self.stiffener_plt_len_along_flange)  # MPa
            #     f_e = math.sqrt(f_a ** 2 + (3 * q ** 2))  # MPa
            #
            #     if f_e > ((min(self.dp_column_fu, self.dp_weld_fu_overwrite)) / (math.sqrt(3) * self.gamma_mw)):
            #         logger.warning("The weld fails in the comb check")
            #         logger.info("Updating the weld size")
            #     else:
            #         pass
            #
            # if self.stiffener_along_web == 'Yes':
            #     # Stiffener along web - weld connecting stiffener to the base plate
            #     # the weld will have shear due to the bearing force and axial force due to in-plane bending of the stiffener
            #     f_a = (self.shear_on_stiffener_along_web * 1000 / 2) / (0.7 * self.weld_size_stiffener * self.stiffener_plt_len_along_web)  # MPa
            #     q = (self.moment_on_stiffener_along_web * 10 ** 6 / self.stiffener_plt_height_along_web) \
            #         / (0.7 * self.weld_size_stiffener * self.stiffener_plt_len_along_web)  # MPa
            #     f_e = math.sqrt(f_a ** 2 + (3 * q ** 2))  # MPa
            #
            #     if f_e > ((min(self.dp_column_fu, self.dp_weld_fu_overwrite)) / (math.sqrt(3) * self.gamma_mw)):
            #         self.safe = False
            #         logger.warning("The weld fails in the comb check")
            #         logger.info("Updating the weld size")
            #     else:
            #         pass
            #
            # # updating the stiffener weld size if it fails in the stress combination check
            # if (self.stiffener_along_flange or self.stiffener_along_web) == 'Yes':
            #
            #     n = 1
            #     while f_e > ((min(self.dp_column_fu, self.dp_weld_fu_overwrite)) / (math.sqrt(3) * self.gamma_mw)):
            #         stiffener_plate_thick = min(self.stiffener_plt_thick_along_flange, self.stiffener_plt_thick_along_web,
            #                                     self.stiffener_plt_thick_across_web)
            #         weld_list = list(range(round_up(self.weld_size_stiffener, 2), stiffener_plate_thick, 2))
            #         weld_list = weld_list + [stiffener_plate_thick]
            #         weld_list = weld_list[n - 1:]
            #
            #         for i in weld_list:
            #             self.weld_size_stiffener = i
            #             break
            #
            #         if self.weld_size_stiffener <= 0:
            #             logger.error("The weld fails in combined stress check")
            #             logger.info("Cannot design with fillet weld. Provide groove weld")
            #
            #         else:
            #             # choosing maximum force and minimum length and height combination for a conservative weld size
            #             max_shear = max(self.shear_capa_stiffener_along_flange, self.shear_on_stiffener_along_web)
            #             max_moment = max(self.moment_on_stiffener_along_flange, self.moment_on_stiffener_along_web)
            #             min_len = min(self.stiffener_plt_len_along_flange, self.stiffener_plt_len_along_web)
            #             min_height = min(self.stiffener_plt_height_along_flange, self.stiffener_plt_height_along_web)
            #
            #             f_a = (max_shear * 1000 / 2) / (0.7 * self.weld_size_stiffener * min_len)  # MPa
            #             q = (max_moment * 10 ** 6 / min_height) / (0.7 * self.weld_size_stiffener * min_len)  # MPa
            #             f_e = math.sqrt(f_a ** 2 + (3 * q ** 2))  # MPa
            #
            #             n += 1
            #
            #             self.weld_size_stiffener = i
            #
            #             if n > len(weld_list):
            #                 logger.warning("The max weld size is ")
            #                 logger.error("Cannot compute weld size. Provide groove weld")
            #                 break

        elif self.connectivity == 'Hollow/Tubular Column Base':
            self.sigma_max = self.w  # N/mm^2
            self.moment_bp_case = 'N/A'
            self.sigma_max_zz = self.w  # MPa
            self.sigma_xx = self.w  # MPa
            self.sigma_web = self.w  # MPa
            self.sigma_lby2 = self.w
            self.sigma_avg = self.w  # MPa

            self.y = 0.0
            self.critical_xx = 0.0

            if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                if (self.stiffener_along_D == 'Yes') or (self.stiffener_along_B == 'Yes'):
                    stiffener_len = min(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B)
                else:
                    stiffener_len = 'N/A'
            else:
                if self.stiffener_along_D == 'Yes':
                    stiffener_len = self.stiffener_plt_len_across_D
                else:
                    stiffener_len = 'N/A'

            # shear yielding and moment capacity checks for the stiffener
            if stiffener_len != 'N/A':

                # shear demand and capacity calculations
                if self.dp_column_designation[1:4] == 'CHS':
                    self.shear_on_stiffener = self.sigma_max * (self.bp_width_provided * self.stiffener_plt_len_across_D)
                    self.shear_on_stiffener = round((self.shear_on_stiffener / 1000), 3)  # kN
                else:
                    self.shear_on_stiffener = self.sigma_max * (self.bp_width_provided *
                                                                (max(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B)))
                    self.shear_on_stiffener = round((self.shear_on_stiffener / 1000), 3)  # kN

                self.shear_capa_stiffener = IS800_2007.cl_8_4_design_shear_strength((self.stiffener_plt_height * self.stiffener_plt_thk),
                                                                                    self.stiffener_fy)
                self.shear_capa_stiffener = round((self.shear_capa_stiffener / 1000), 3)  # kN

                # moment demand and capcaity calculations
                if self.dp_column_designation[1:4] == 'CHS':
                    self.moment_on_stiffener = self.shear_on_stiffener * (self.stiffener_plt_len_across_D / 2)
                    self.moment_on_stiffener = round((self.moment_on_stiffener * 10 ** -3), 3)  # kNm
                else:
                    self.moment_on_stiffener = self.shear_on_stiffener * (self.stiffener_plt_len_along_D / 2)
                    self.moment_on_stiffener = round((self.moment_on_stiffener * 10 ** -3), 3)  # kNm

                self.z_e_stiffener = (self.stiffener_plt_thk * self.stiffener_plt_height ** 2) / 6  # mm^3

                self.moment_capa_stiffener = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener, 0, self.stiffener_fy,
                                                                                          section_class='semi-compact')
                self.moment_capa_stiffener = round((self.moment_capa_stiffener * 10 ** -6), 3)  # kNm

                # checks
                if self.shear_on_stiffener > (0.6 * self.shear_capa_stiffener):
                    logger.warning("[Shear Check - Stiffener] The stiffener fails the shear check")
                    logger.warning("The shear demand on the stiffener ({} kN) exceeds 60% of it's capacity ({} kN)".
                                   format(round(self.shear_on_stiffener, 2), round(0.6 * self.shear_capa_stiffener, 2)))
                    logger.info("Increasing the thickness of the stiffener and re-checking against shear demand")

                    n = 1
                    while self.shear_on_stiffener > (0.6 * self.shear_capa_stiffener):
                        self.stiffener_plt_thk += 2
                        sort_plate = filter(lambda x: self.stiffener_plt_thk <= x <= self.standard_plate_thk[-1],
                                            self.standard_plate_thk)
                        for i in sort_plate:
                            self.stiffener_plt_thk = i  # plate thickness provided (mm)
                            break

                        self.shear_capa_stiffener = IS800_2007.cl_8_4_design_shear_strength((self.stiffener_plt_height * self.stiffener_plt_thk),
                                                                                            self.stiffener_fy)
                        self.shear_capa_stiffener = round((self.shear_capa_stiffener / 1000), 3)  # kN

                        n += 1

                    # re-calculating the moment demand and capacity by incorporating the improvised stiffener thickness
                    self.z_e_stiffener = (self.stiffener_plt_thk * self.stiffener_plt_height ** 2) / 6  # mm^3

                    if self.dp_column_designation[1:4] == 'CHS':
                        self.moment_on_stiffener = self.shear_on_stiffener * (self.stiffener_plt_len_across_D / 2)
                        self.moment_on_stiffener = round((self.moment_on_stiffener * 10 ** -3), 3)  # kNm
                    else:
                        self.moment_on_stiffener = self.shear_on_stiffener * (self.stiffener_plt_len_along_D / 2)
                        self.moment_on_stiffener = round((self.moment_on_stiffener * 10 ** -3), 3)  # kNm

                    self.moment_capa_stiffener = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener, 0, self.stiffener_fy,
                                                                                              section_class='semi-compact')
                    self.moment_capa_stiffener = round((self.moment_capa_stiffener * 10 ** -6), 3)  # kNm

                if self.moment_on_stiffener > self.moment_capa_stiffener:
                    logger.warning("[Moment Check - Stiffener] The stiffener fails the moment check")
                    logger.warning("The moment demand on the stiffener ({} kNm) exceeds it's capacity ({} kNm)".
                                   format(round(self.moment_on_stiffener, 2), round(self.moment_capa_stiffener, 2)))
                    logger.info("Increasing the thickness of the stiffener and re-checking against moment demand")

                    n = 1
                    while self.moment_on_stiffener > self.moment_capa_stiffener:
                        self.stiffener_plt_thk += 2
                        sort_plate = filter(lambda x: self.stiffener_plt_thk <= x <= self.standard_plate_thk[-1],
                                            self.standard_plate_thk)
                        for i in sort_plate:
                            self.stiffener_plt_thk = i  # plate thickness provided (mm)
                            break

                        self.z_e_stiffener = (self.stiffener_plt_thk * self.stiffener_plt_height ** 2) / 6  # mm^3
                        self.moment_capa_stiffener = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener, 0, self.stiffener_fy,
                                                                                                  section_class='semi-compact')
                        self.moment_capa_stiffener = round((self.moment_capa_stiffener * 10 ** -6), 3)  # kNm

                        self.shear_capa_stiffener = IS800_2007.cl_8_4_design_shear_strength((self.stiffener_plt_height * self.stiffener_plt_thk),
                                                                                            self.stiffener_fy)
                        self.shear_capa_stiffener = round((self.shear_capa_stiffener / 1000), 3)  # kN
                        n += 1

                self.z_e_stiffener = round(self.z_e_stiffener, 2)
            else:
                self.shear_on_stiffener = 'N/A'
                self.shear_capa_stiffener = 'N/A'
                self.moment_on_stiffener = 'N/A'
                self.moment_capa_stiffener = 'N/A'

        # weld design for stiffeners

        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Moment Base Plate'):

            if self.stiffener_across_web == 'Yes':
                self.weld_stiffener_across_web.set_min_max_sizes(self.stiffener_plt_thick_across_web, self.column_tw, special_circumstance=False,
                                                                 fusion_face_angle=90)
                self.weld_size_stiffener_across_web = min(self.weld_stiffener_across_web.min_size + 2, self.weld_stiffener_across_web.max_size)
                self.weld_size_stiffener_across_web = round_up(self.weld_size_stiffener_across_web, 2)

            if self.stiffener_along_flange == 'Yes':
                self.weld_stiffener_flange.set_min_max_sizes(self.stiffener_plt_thick_along_flange, self.plate_thk_provided,
                                                                   special_circumstance=False, fusion_face_angle=90)
                self.weld_size_stiffener_along_flange = min(self.weld_stiffener_flange.min_size + 2, self.weld_stiffener_flange.max_size)
                self.weld_size_stiffener_along_flange = round_up(self.weld_size_stiffener_along_flange, 2)

            if self.stiffener_along_web == 'Yes':
                self.weld_stiffener_web.set_min_max_sizes(self.stiffener_plt_thick_along_web, self.plate_thk_provided,
                                                                   special_circumstance=False, fusion_face_angle=90)
                self.weld_size_stiffener_along_web = min(self.weld_stiffener_web.min_size + 2, self.weld_stiffener_web.max_size)
                self.weld_size_stiffener_along_web = round_up(self.weld_size_stiffener_along_web, 2)

        elif self.connectivity == 'Hollow/Tubular Column Base':
            if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                if (self.stiffener_along_D == 'Yes') or (self.stiffener_along_B == 'Yes'):
                    self.weld_stiffener_SHS.set_min_max_sizes(self.stiffener_plt_thk, self.plate_thk_provided, special_circumstance=False,
                                                              fusion_face_angle=90)

                    end_return_reduction = 2 * self.weld_stiffener_SHS.min_size
                    self.weld_length_stiffener_plt = (2 * (self.stiffener_plt_height - 25)) - end_return_reduction
                    self.weld_size_stiffener_plt = (self.shear_on_stiffener * 1e3 * math.sqrt(3) * self.gamma_mw) / \
                                                   (0.7 * self.weld_length_stiffener_plt * self.dp_weld_fu_overwrite)
                    self.weld_size_stiffener_plt = max(self.weld_size_stiffener_plt, self.weld_stiffener_SHS.min_size)
                    self.weld_size_stiffener_plt = round_up(self.weld_size_stiffener_plt, 2)
            else:
                if self.stiffener_along_D == 'Yes':
                    self.weld_stiffener_CHS.set_min_max_sizes(self.stiffener_plt_thk, self.plate_thk_provided, special_circumstance=False,
                                                              fusion_face_angle=90)

                    end_return_reduction = 2 * self.weld_stiffener_CHS.min_size
                    self.weld_length_stiffener_plt = (2 * (self.stiffener_plt_height - 25)) - end_return_reduction
                    self.weld_size_stiffener_plt = (self.shear_on_stiffener * 1e3 * math.sqrt(3) * self.gamma_mw) / \
                                                   (0.7 * self.weld_length_stiffener_plt * self.dp_weld_fu_overwrite)
                    self.weld_size_stiffener_plt = max(self.weld_size_stiffener_plt, self.weld_stiffener_CHS.min_size)
                    self.weld_size_stiffener_plt = round_up(self.weld_size_stiffener_plt, 2)

    def additional_calculations(self):
        """ Perform additional and common checks

        Args:

        Returns:

        """
        # design for minor axis moment
        if (self.connectivity == 'Moment Base Plate') and (self.load_moment_minor > 0):
            if self.stiffener_across_web == 'Yes':
                end_available = (self.column_D - (2 * self.column_tf) - self.stiffener_plt_thick_across_web) / 4  # mm
            if self.shear_key_along_ColWidth == 'Yes':
                end_available = (self.column_D - (2 * self.column_tf) - self.shear_key_thk) / 4  # mm
            if (self.stiffener_across_web == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                end_available = (self.column_D - (2 * self.column_tf) - max(self.stiffener_plt_thick_across_web, self.shear_key_thk)) / 4  # mm
            round(end_available, 2)

            self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)  # inside flange
            self.plate_washer_dim_in = self.plate_washer_details_in['side']  # washer dimension - inside flange, mm

            self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_inside_flange, self.dp_anchor_hole_in,
                                                                      self.dp_detail_edge_type)
            self.end_distance_in = max(self.end_distance_in, self.plate_washer_dim_in, end_available)
            self.edge_distance_in = self.end_distance_in

            self.anchors_inside_flange = 4
            self.anchor_nos_provided = (2 * self.anchors_outside_flange) + self.anchors_inside_flange

            if self.moment_bp_case_yy == 'Case1':
                self.tension_demand_anchor_uplift = 0
            else:
                self.tension_demand_anchor_uplift = 'N/A'
            self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_inside_flange[0],
                                                                                                 self.anchor_fu_fy_inside_flange[1],
                                                                                                 self.anchor_area_inside_flange[0],
                                                                                                 self.anchor_area_inside_flange[1],
                                                                                                 safety_factor_parameter=self.dp_weld_fab)  # N
            self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

        # design of anchor bolts to resist axial tension/uplift force - final iteration considering stiffeners, shear key etc.
        # calculate bolt and stiffener arrangement when stiffener is provided across the web and there is uplift force acting on the column
        # the configuration has 2 or 4 bolts, with or without stiffeners
        if self.connectivity == 'Moment Base Plate':
            if (self.load_axial_tension > 0) and (self.anchor_inside_flange == 'Yes'):

                # case where stiffeners are required across the column web or shear key is provided, provide min 4 bolts
                if (self.stiffener_across_web == 'Yes') or (self.shear_key_along_ColWidth == 'Yes'):
                    self.anchors_inside_flange = 4  # minimum 4 bolts provided in this case

                    anchors_inside_req = self.load_axial_tension / (self.tension_capacity_anchor_uplift * 1000)
                    anchors_inside_req = round_up(anchors_inside_req, 2)

                    if anchors_inside_req > self.anchors_inside_flange:
                        self.anchors_inside_flange = anchors_inside_req
                        # if the number of bolts exceeds 4 in number, provide a higher diameter of bolt from the given list of anchor diameters
                        n = 1
                        while self.anchors_inside_flange > 4:  # trying for 4 bolts with higher diameter
                            bolt_list = self.anchor_dia_list_in[n - 1:]
                            itr = len(self.anchor_dia_list_in) + 1

                            for i in bolt_list:
                                self.anchor_dia_inside_flange = i
                                break

                            self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                            self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_inside_flange[0],
                                                                                                                 self.anchor_fu_fy_inside_flange[1],
                                                                                                                 self.anchor_area_inside_flange[0],
                                                                                                                 self.anchor_area_inside_flange[1],
                                                                                                                 safety_factor_parameter=self.dp_weld_fab)  # N
                            self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

                            self.anchors_inside_flange = max(((self.load_axial_tension * 10 ** -3) / self.tension_capacity_anchor_uplift), 4)
                            n += 1

                            self.anchor_dia_inside_flange = i  # updating the initialised anchor diameter with the latest one

                            if n == itr:  # if 4 bolts with highest diameter is not sufficient
                                # self.safe = False
                                # TODO: give log errors
                                logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 4 anchor bolts with the highest "
                                             "trial diameter and grade")
                                logger.error("Re-designing the connection with 8 anchor bolts")
                                break

                    # detailing checks for the above case
                    # end distance available (along web)
                    if self.stiffener_across_web == 'Yes':
                        end_available = (self.column_D - (2 * self.column_tf) - self.stiffener_plt_thick_across_web) / 4  # mm
                    if self.shear_key_along_ColWidth == 'Yes':
                        end_available = (self.column_D - (2 * self.column_tf) - self.shear_key_thk) / 4  # mm
                    if (self.stiffener_across_web == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                        end_available = (self.column_D - (2 * self.column_tf) - max(self.stiffener_plt_thick_across_web,
                                                                                    self.shear_key_thk)) / 4  # mm

                    self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)  # inside flange
                    self.plate_washer_dim_in = self.plate_washer_details_in['side']  # washer dimension - inside flange, mm

                    self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_inside_flange, self.dp_anchor_hole_in,
                                                                              self.dp_detail_edge_type)
                    self.end_distance_in = max(self.end_distance_in, self.plate_washer_dim_in)
                    self.edge_distance_in = self.end_distance_in

                    if (self.anchors_inside_flange > 4) or (self.end_distance_in > end_available):
                        logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 4 anchor bolts with the highest "
                                     "trial diameter and grade or fails to satisfy the detailing criteria")
                        logger.error("Re-designing the connection with 8 anchor bolts")

                        self.anchors_inside_flange = 8  # minimum 8 bolts with a smaller diameter
                        self.anchor_dia_inside_flange = 20  # trying with (least) 20mm anchor dia

                        self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                        self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_inside_flange[0],
                                                                                                             self.anchor_fu_fy_inside_flange[1],
                                                                                                             self.anchor_area_inside_flange[0],
                                                                                                             self.anchor_area_inside_flange[1],
                                                                                                             safety_factor_parameter=self.dp_weld_fab)  # N
                        self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

                        anchors_inside_req = self.load_axial_tension / (self.tension_capacity_anchor_uplift * 1000)
                        anchors_inside_req = round_up(anchors_inside_req, 2)  # required number of bolts

                        if anchors_inside_req > self.anchors_inside_flange:
                            self.anchors_inside_flange = anchors_inside_req
                            # if the number of bolts exceeds 8 in number, provide a higher diameter of bolt from the given list of anchor diameters
                            n = 1
                            while self.anchors_inside_flange > 8:  # trying for 8 bolts with higher diameter
                                bolt_list = self.anchor_dia_list_in[n - 1:]
                                itr = len(self.anchor_dia_list_in) + 1

                                for i in bolt_list:
                                    self.anchor_dia_inside_flange = i
                                    break

                                self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                                self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(
                                    self.anchor_fu_fy_inside_flange[0],
                                    self.anchor_fu_fy_inside_flange[1],
                                    self.anchor_area_inside_flange[0],
                                    self.anchor_area_inside_flange[1],
                                    safety_factor_parameter=self.dp_weld_fab)  # N
                                self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

                                self.anchors_inside_flange = max(((self.load_axial_tension * 10 ** -3) / self.tension_capacity_anchor_uplift), 8)
                                n += 1

                                self.anchor_dia_inside_flange = i  # updating the initialised anchor diameter with the latest one

                                if n == itr:  # if 8 bolts with highest diameter is not sufficient
                                    self.safe = False
                                    logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 8 anchor bolts with the "
                                        "highest trial diameter and grade or fails to satisfy the detailing criteria")
                                    logger.error("Design for anchor bolts greater than 8 in numbers is not available in this version of Osdag")
                                    logger.error("Cannot compute")
                                    break

                        # detailing checks
                        if self.stiffener_across_web == 'Yes':
                            end_available = (self.column_D - (2 * self.column_tf) - self.stiffener_plt_thick_across_web) / 4  # mm
                        else:  # for shear key
                            end_available = (self.column_D - (2 * self.column_tf) - self.shear_key_thk) / 4  # mm
                        if (self.stiffener_across_web == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                            end_available = (self.column_D - (2 * self.column_tf) - max(self.stiffener_plt_thick_across_web,
                                                                                        self.shear_key_thk)) / 4  # mm

                        self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)  # inside flange
                        self.plate_washer_dim_in = self.plate_washer_details_in['side']  # washer dimension - inside flange, mm

                        self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_inside_flange, self.dp_anchor_hole_in,
                                                                                  self.dp_detail_edge_type)
                        self.end_distance_in = max(self.end_distance_in, self.plate_washer_dim_in)
                        self.edge_distance_in = self.end_distance_in

                        self.pitch_distance_in = self.cl_10_2_2_min_spacing(self.anchor_dia_inside_flange)  # mm
                        # adding 10mm to accommodate weld along the side of washer plate
                        self.pitch_distance_in = max(self.pitch_distance_in,
                                                     round_up(self.plate_washer_dim_in + (2 * self.plate_washer_thk_in) + 5, 2))  # mm
                        self.gauge_distance_in = self.pitch_distance_in

                        if self.end_distance_in > end_available:
                            self.safe = False
                            logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 8 anchor bolts with the "
                                         "highest trial diameter and grade or fails to satisfy the detailing criteria")
                            logger.error("Design for anchor bolts greater than 8 in numbers is not available in this version of Osdag")
                            logger.error("Cannot compute")

                # case where stiffeners are not required across the column web, try with 2 bolts
                else:
                    if self.anchors_inside_flange > 2:
                        logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 2 anchor bolts")
                        logger.error("Re-designing the connection with 2 anchor bolts of higher diameter or grade combination")

                        # if the number of bolts exceeds 2 in number, provide a higher diameter of bolt from the given list of anchor diameters
                        n = 1
                        while self.anchors_inside_flange > 2:  # trying for 2 bolts with higher diameter
                            bolt_list = self.anchor_dia_list_in[n - 1:]
                            itr = len(self.anchor_dia_list_in) + 1

                            for i in bolt_list:
                                self.anchor_dia_inside_flange = i
                                break

                            self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                            self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_inside_flange[0],
                                                                                                                 self.anchor_fu_fy_inside_flange[1],
                                                                                                                 self.anchor_area_inside_flange[0],
                                                                                                                 self.anchor_area_inside_flange[1],
                                                                                                                 safety_factor_parameter=self.dp_weld_fab)  # N
                            self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

                            self.anchors_inside_flange = max(((self.load_axial_tension * 10 ** -3) / self.tension_capacity_anchor_uplift), 2)
                            n += 1

                            self.anchor_dia_inside_flange = i  # updating the initialised anchor diameter with the latest one

                            # detailing check - 2 bolts
                            end_available = (self.column_D - (2 * self.column_tf)) / 2

                            self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)  # inside flange
                            self.plate_washer_dim_in = self.plate_washer_details_in['side']  # washer dimension - inside flange, mm

                            self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_inside_flange, self.dp_anchor_hole_in,
                                                                                      self.dp_detail_edge_type)
                            self.end_distance_in = max(self.end_distance_in, self.plate_washer_dim_in)
                            self.edge_distance_in = self.end_distance_in

                            if self.end_distance_in > end_available:
                                self.anchors_inside_flange = 4
                                logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 2 anchor bolts of highest diameter"
                                             "and grade combination")
                                logger.error("Re-designing the connection with 4 anchor bolts")

                            # if ((n - 1) >= len(bolt_list)) and (self.anchors_inside_flange > 2):
                            # if (self.anchor_dia_inside_flange == 72) and (self.anchors_inside_flange > 2):
                            if (n == itr) and (self.anchors_inside_flange > 2):
                                # try with 4 bolts if 2 is not sufficient with the highest diameter
                                logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 2 anchor bolts of highest diameter"
                                             "and grade combination")
                                logger.error("Re-designing the connection with 4 anchor bolts")

                                self.anchor_dia_inside_flange = 20
                                self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                                self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(
                                    self.anchor_fu_fy_inside_flange[0],
                                    self.anchor_fu_fy_inside_flange[1],
                                    self.anchor_area_inside_flange[0],
                                    self.anchor_area_inside_flange[1],
                                    safety_factor_parameter=self.dp_weld_fab)  # N
                                self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

                                # provide 4 anchors
                                self.anchors_inside_flange = max(((self.load_axial_tension * 10 ** -3) / self.tension_capacity_anchor_uplift), 4)

                                # detailing check - 4 bolts
                                self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)  # inside flange
                                self.plate_washer_dim_in = self.plate_washer_details_in['side']  # washer dimension - inside flange, mm

                                self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_inside_flange, self.dp_anchor_hole_in,
                                                                                          self.dp_detail_edge_type)
                                self.end_distance_in = round_up(self.end_distance_in, 5)
                                self.end_distance_in = max(self.end_distance_in, self.plate_washer_dim_in)

                                self.pitch_distance_in = self.cl_10_2_2_min_spacing(self.anchor_dia_inside_flange)  # mm
                                # adding 10mm to accommodate weld along the side of washer plate
                                self.pitch_distance_in = max(self.pitch_distance_in,
                                                             round_up(self.plate_washer_dim_in + (2 * self.plate_washer_thk_in) + 5, 2))  # mm

                                end_available = (self.column_D - (2 * self.column_tf) - self.pitch_distance_in) / 2
                                pitch_available = self.column_D - (2 * self.column_tf) - (2 * self.end_distance_in)

                                if (self.end_distance_in > end_available) or (self.pitch_distance_in > pitch_available):
                                    # self.safe = False
                                    logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 4 anchor bolts or fails to "
                                                 "satisfy the detailing criteria")
                                    logger.error("Re-designing the connection with 4 anchor bolts of higher diameter and grade combination")

                                if self.anchors_inside_flange > 4:
                                    # if the number of bolts exceeds 4, provide a higher diameter of bolt from the given list of anchor diameters
                                    logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 4 anchor bolts of 20 mm diameter "
                                                 "or fails to satisfy the detailing criteria")
                                    logger.error("Re-designing the connection with 4 anchor bolts of higher diameter and grade combination")

                                    n = 1
                                    while self.anchors_inside_flange > 4:  # trying for 4 bolts with higher diameter
                                        bolt_list = self.anchor_dia_list_in[n - 1:]
                                        itr = len(self.anchor_dia_list_in) + 1

                                        for i in bolt_list:
                                            self.anchor_dia_inside_flange = i
                                            break

                                        self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                                        # self.anchor_area_outside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                                        self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(
                                            self.anchor_fu_fy_inside_flange[0],
                                            self.anchor_fu_fy_inside_flange[1],
                                            self.anchor_area_inside_flange[0],
                                            self.anchor_area_inside_flange[1],
                                            safety_factor_parameter=self.dp_weld_fab)  # N
                                        self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

                                        self.anchors_inside_flange = max(((self.load_axial_tension * 10 ** -3) / self.tension_capacity_anchor_uplift),
                                                                         4)
                                        n += 1

                                        self.anchor_dia_inside_flange = i  # updating the initialised anchor diameter with the latest one

                                        # detailing check - 4 bolts with larger dia
                                        self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)  # inside flange
                                        self.plate_washer_dim_in = self.plate_washer_details_in['side']  # washer dimension - inside flange, mm

                                        self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_inside_flange,
                                                                                                  self.dp_anchor_hole_in,
                                                                                                  self.dp_detail_edge_type)
                                        self.end_distance_in = round_up(self.end_distance_in, 5)
                                        self.end_distance_in = max(self.end_distance_in, self.plate_washer_dim_in)

                                        self.pitch_distance_in = self.cl_10_2_2_min_spacing(self.anchor_dia_inside_flange)  # mm
                                        # adding 10mm to accommodate weld along the side of washer plate
                                        self.pitch_distance_in = max(self.pitch_distance_in,
                                                                     round_up(self.plate_washer_dim_in + (2 * self.plate_washer_thk_in) + 5, 2))  # mm

                                        end_available = (self.column_D - (2 * self.column_tf) - self.pitch_distance_in) / 2
                                        pitch_available = self.column_D - (2 * self.column_tf) - (2 * self.end_distance_in)

                                        if (self.end_distance_in > end_available) or (self.pitch_distance_in > pitch_available):
                                            logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 4 anchor bolts or "
                                                "fails to satisfy the detailing criteria")
                                            logger.error("Re-designing the connection with 8 anchor bolts")
                                            self.anchors_inside_flange = 8  # trying with 8 bolts as detailing check fails
                                            itr = n

                                        if (self.anchor_dia_inside_flange <= 72) and (self.anchors_inside_flange == 4):
                                            break

                                        # if ((n - 1) >= len(bolt_list)) and (self.anchors_inside_flange > 4):
                                        if (n == itr) and (self.anchors_inside_flange > 4):
                                            # if 4 bolts with highest diameter is not sufficient
                                            # self.safe = False
                                            logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 4 anchor bolts of"
                                                         " highest diameter or fails to satisfy the detailing criteria")
                                            logger.error("Re-designing the connection with 8 anchor bolts")

                                            self.anchors_inside_flange = 8  # minimum 8 bolts with a smaller diameter
                                            self.anchor_dia_inside_flange = 20  # trying with (least) 20mm anchor dia
                                            self.stiffener_inside_flange = 'Yes'

                                            self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                                            self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(
                                                self.anchor_fu_fy_inside_flange[0],
                                                self.anchor_fu_fy_inside_flange[1],
                                                self.anchor_area_inside_flange[0],
                                                self.anchor_area_inside_flange[1],
                                                safety_factor_parameter=self.dp_weld_fab)  # N
                                            self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000, 2)  # kN

                                            anchors_inside_req = self.load_axial_tension / (self.tension_capacity_anchor_uplift * 1000)
                                            anchors_inside_req = round_up(anchors_inside_req, 8)  # required number of bolts

                                            if anchors_inside_req > self.anchors_inside_flange:
                                                self.anchors_inside_flange = anchors_inside_req
                                                # if the number of bolts exceeds 8 in number, provide a higher diameter of bolt from the given list of anchor diameters
                                                n = 1
                                                while self.anchors_inside_flange > 8:  # trying for 8 bolts with higher diameter
                                                    bolt_list = self.anchor_dia_list_in[n - 1:]
                                                    itr = len(self.anchor_dia_list_in) + 1

                                                    for i in bolt_list:
                                                        self.anchor_dia_inside_flange = i
                                                        break

                                                    self.anchor_area_inside_flange = self.bolt_area(self.anchor_dia_inside_flange)
                                                    self.tension_capacity_anchor_uplift = self.cl_10_3_5_bearing_bolt_tension_resistance(
                                                        self.anchor_fu_fy_inside_flange[0],
                                                        self.anchor_fu_fy_inside_flange[1],
                                                        self.anchor_area_inside_flange[0],
                                                        self.anchor_area_inside_flange[1],
                                                        safety_factor_parameter=self.dp_weld_fab)  # N
                                                    self.tension_capacity_anchor_uplift = round(self.tension_capacity_anchor_uplift / 1000,
                                                                                                2)  # kN

                                                    self.anchors_inside_flange = max(
                                                        ((self.load_axial_tension * 10 ** -3) / self.tension_capacity_anchor_uplift),
                                                        8)
                                                    n += 1

                                                    self.anchor_dia_inside_flange = i  # updating the initialised anchor diameter with the latest one

                                                    # if n > len(bolt_list):  # if 8 bolts with highest diameter is not sufficient
                                                    if n > itr:
                                                        self.safe = False
                                                        logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 8 anchor "
                                                            "bolts with the highest diameter and grade or fails to satisfy the detailing criteria")
                                                        logger.error("Design for anchor bolts greater than 8 in numbers is not available in this "
                                                                     "version of Osdag")
                                                        logger.error("Cannot compute")
                                                        break

                                                # detailing check - 8 bolts with larger dia
                                                self.plate_washer_details_in = IS6649.square_washer_dimensions(self.anchor_dia_inside_flange)
                                                self.plate_washer_dim_in = self.plate_washer_details_in['side']  # mm

                                                self.end_distance_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_inside_flange,
                                                                                                          self.dp_anchor_hole_in,
                                                                                                          self.dp_detail_edge_type)
                                                self.end_distance_in = round_up(self.end_distance_in, 5)
                                                self.end_distance_in = max(self.end_distance_in, self.plate_washer_dim_in)
                                                self.edge_distance_in = self.end_distance_in

                                                self.pitch_distance_in = self.cl_10_2_2_min_spacing(self.anchor_dia_inside_flange)  # mm
                                                # adding 10mm to accommodate weld along the side of washer plate
                                                self.pitch_distance_in = max(self.pitch_distance_in,
                                                                             round_up(self.plate_washer_dim_in + (2 * self.plate_washer_thk_in) + 5,
                                                                                      2))  # mm
                                                self.gauge_distance_in = self.pitch_distance_in

                                                end_available = (self.column_D - (2 * self.column_tf) - self.pitch_distance_in) / 2
                                                pitch_available = self.column_D - (2 * self.column_tf) - (2 * self.end_distance_in)

                                                if (self.end_distance_in > end_available) or (self.pitch_distance_in > pitch_available):
                                                    self.safe = False
                                                    self.anchors_inside_flange = round_up(self.anchors_inside_flange, 2)
                                                    logger.error("[Anchor Bolt Design] The required uplift demand is not satisfied by 8 anchor "
                                                                 "bolts with the highest diameter and grade or fails to satisfy the detailing "
                                                                 "criteria")
                                                    logger.error("Design for anchor bolts greater than 8 in numbers is not available in this "
                                                                 "version of Osdag")
                                                    logger.error("Cannot compute anchor bolt for resisting the uplift force")
                                                    break
                                                else:
                                                    break

                                            if self.anchor_dia_inside_flange <= 72:
                                                if self.anchors_inside_flange == 8:
                                                    break
                                                else:
                                                    self.safe = False
                                                    logger.error("Cannot compute anchor bolt for resisting the uplift force")
                                                    break

                            if self.anchor_dia_inside_flange <= 72:
                                if (self.anchors_inside_flange == 2) or (self.anchors_inside_flange == 4) or (self.anchors_inside_flange == 8):
                                    break
                                else:
                                    logger.error("Design of anchor bolt with {} mm is unsafe. Running the next iteration with a higer diameter or "
                                                 "grade of anchor bolt".format(self.anchor_dia_inside_flange))

                            if (self.anchor_dia_inside_flange >= 72) and (self.anchors_inside_flange > 4):
                                # self.anchors_inside_flange = round_up(self.anchors_inside_flange, 2)
                                self.safe = False
                                # logger.error("Cannot compute anchor bolt for resisting the uplift force with 4 bolts")
                                # logger.info("Trying with 8 bolts")
                                break

                # Tension Demand
                self.tension_demand_anchor_uplift = self.load_axial_tension / self.anchors_inside_flange
                self.tension_demand_anchor_uplift = round(self.tension_demand_anchor_uplift / 1000, 2)

                # updating total number of anchor bolts required (bolts outside flange + inside flange)
                self.anchor_nos_provided = (2 * self.anchors_outside_flange) + self.anchors_inside_flange

            if (self.stiffener_across_web == 'Yes') or (self.shear_key_along_ColWidth == 'Yes'):
                if self.anchors_inside_flange == 4:
                    self.pitch_distance_in = 'N/A'
                    self.gauge_distance_in = 'N/A'

        if self.connectivity == 'Hollow/Tubular Column Base':
            self.end_distance_out = (self.bp_length_provided - (self.column_D + (2 * self.projection))) / 2  # mm
            self.edge_distance_out = self.end_distance_out  # mm

        # check for plate thickness
        if self.shear_key_thk != 'N/A':
            if self.plate_thk_provided < self.shear_key_thk:

                self.plate_thk_provided = self.shear_key_thk
                logger.warning("[Plate Thickness] Thickness of the base plate is less than the thickness of the shear key")
                logger.info("Thickness of the base plate should be at-least equal to the thickness of the shear key to avoid bending of the "
                            "base plate in case of high horizontal shear force")
                logger.info("Updating the thickness of the base plate")

        # design of weld for the continuity plate inside flange in case of 3 or 6 bolts on each side
        if self.connectivity == 'Moment Base Plate':
            if self.stiffener_inside_flange == 'Yes':
                self.weld_stiffener_key.set_min_max_sizes(min(self.column_tf, self.column_tw), self.stiffener_plt_thick_btwn_D,
                                                          special_circumstance=False, fusion_face_angle=90)

                self.weld_size_continuity_plate = min(round_up(self.weld_stiffener_key.min_size + 2, 2),
                                                      round_down(min(self.column_tf, self.column_tw), 2))

        # end of calculation
        for status in self.design_status_list:
            if status is False:
                self.safe = False
                self.design_status = False
                break
            else:
                self.safe = True
                self.design_status = True

        if self.safe:
            self.design_status = True
            logger.info(": =========== Design Status =============")
            logger.info(":      Overall base plate connection design is SAFE")
            logger.info(": ============ End Of Design ============")
        else:
            self.design_status = False
            logger.info(": =========== Design Status =============")
            logger.info(":     Overall base plate connection design is UNSAFE")
            logger.info(": ============ End Of Design ============")

        # printing values for output dock

        # Anchor Bolt - Outside Column Flange
        print(self.anchor_dia_outside_flange)  # Diameter (mm)
        print(self.anchor_grade_out)  # Property Class
        print(2 * self.anchors_outside_flange)  # No. of Anchor Bolts

        print(self.shear_capacity_anchor)  # Shear Capacity (kN)
        print(self.bearing_capacity_anchor)  # Bearing Capacity (kN)
        print(self.anchor_capacity)  # Bolt capacity (kN)

        if self.connectivity == 'Moment Base Plate':
            print(self.tension_demand_anchor)  # Tension Demand (kN)
            print(self.tension_capacity_anchor)  # Tension capacity (kN)
        else:
            print(self.tension_demand_anchor)  # Tension Demand (kN)

        print(self.combined_capacity_anchor)  # Combined capacity (kN)

        print(self.anchor_len_above_footing_out)
        print(self.anchor_len_below_footing_out)
        print(self.anchor_length_provided_out)  # Anchor Length (total) (mm)

        # Anchor Bolt - Inside Column Flange
        if self.connectivity == 'Moment Base Plate':
            if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):

                print(self.anchor_dia_inside_flange)  # Diameter (mm)
                print(self.anchor_grade_in)  # Property Class

                if self.load_axial_tension > 0:
                    print(self.tension_demand_anchor_uplift)  # Tension Demand (kN)
                else:
                    print(self.tension_demand_anchor_uplift)
                if self.connectivity == 'Moment Base Plate':
                    print(self.tension_capacity_anchor_uplift)  # Tension capacity (kN)

                print(self.anchors_inside_flange)  # No. of Anchor Bolts

                print(self.anchor_len_above_footing_in)
                print(self.anchor_len_below_footing_in)
                print(self.anchor_length_provided_in)  # Anchor Length (total) (mm)

        # Detailing for anchor bolts inside flange
        if self.connectivity == 'Moment Base Plate':
            if (self.load_axial_tension > 0) or (self.load_moment_minor > 0):

                if (self.stiffener_across_web == 'Yes') or (self.shear_key_along_ColWidth == 'Yes'):

                    if self.anchors_inside_flange == 4:
                        print(self.end_distance_in)
                        print(self.edge_distance_in)

                    if self.anchors_inside_flange == 8:
                        print(self.end_distance_in)
                        print(self.edge_distance_in)
                        print(self.gauge_distance_in)
                else:
                    if self.anchors_inside_flange == 4:
                        print(self.end_distance_in)
                        print(self.pitch_distance_in)

                    if self.anchors_inside_flange == 8:
                        print(self.end_distance_in)
                        print(self.edge_distance_in)
                        print(self.pitch_distance_in)
                        print(self.gauge_distance_in)

        # Base Plate
        print(self.plate_thk_provided)  # Thickness (mm)
        print(self.bp_length_provided)  # Length (mm)
        print(self.bp_width_provided)  # Width (mm)

        # Detailing
        print(self.anchor_nos_provided)  # Total No. of Anchor Bolts

        print(self.end_distance_out)  # End Distance (mm)
        print(self.edge_distance_out)  # Edge Distance (mm)

        print(self.pitch_distance_out)  # Pitch Distance (mm)
        print(self.gauge_distance_out)  # Gauge Distance (mm)

        if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
            print(self.projection)  # Effective Projection (mm)
        else:
            pass

        # Gusset/Stiffener Plate
        if self.connectivity == 'Hollow/Tubular Column Base':

            if (self.stiffener_along_D == 'Yes') or (self.stiffener_along_B == 'Yes'):

                print(self.stiffener_nos)
                print(self.stiffener_plt_thk)
                print(self.stiffener_plt_height)

                if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                    print(self.stiffener_plt_len_along_D)
                    print(self.stiffener_plt_len_along_B)
                else:
                    print(self.stiffener_plt_len_across_D)

                print(self.shear_on_stiffener)
                print(self.shear_capa_stiffener)
                print(self.moment_on_stiffener)
                print(self.moment_capa_stiffener)

            else:
                pass

        else:
            # Stiffener Plate Along Column Flange
            if self.stiffener_along_flange == 'Yes':
                print(self.stiffener_plt_len_along_flange)
                print(self.stiffener_plt_height_along_flange)
                print(self.stiffener_plt_thick_along_flange)
                print(self.shear_on_stiffener_along_flange)
                print(self.shear_capa_stiffener_along_flange)
                print(self.moment_on_stiffener_along_flange)
                print(self.moment_capa_stiffener_along_flange)
            else:
                print(self.stiffener_plt_len_along_flange == 'N/A')
                print(self.stiffener_plt_height_along_flange == 'N/A')
                print(self.stiffener_plt_thick_along_flange == 'N/A')
                print(self.shear_on_stiffener_along_flange == 'N/A')
                print(self.shear_capa_stiffener_along_flange == 'N/A')
                print(self.moment_on_stiffener_along_flange == 'N/A')
                print(self.moment_capa_stiffener_along_flange == 'N/A')

            # Stiffener Plate Along Column Web
            if self.stiffener_along_web == 'Yes':
                print(self.stiffener_plt_len_along_web)
                print(self.stiffener_plt_height_along_web)
                print(self.stiffener_plt_thick_along_web)
                print(self.shear_on_stiffener_along_web)
                print(self.shear_capa_stiffener_along_web)
                print(self.moment_on_stiffener_along_web)
                print(self.moment_capa_stiffener_along_web)
            else:
                print(self.stiffener_plt_len_along_web == 'N/A')
                print(self.stiffener_plt_height_along_web == 'N/A')
                print(self.stiffener_plt_thick_along_web == 'N/A')
                print(self.shear_on_stiffener_along_web == 'N/A')
                print(self.shear_capa_stiffener_along_web == 'N/A')
                print(self.moment_on_stiffener_along_web == 'N/A')
                print(self.moment_capa_stiffener_along_web == 'N/A')

            # Stiffener Plate Across Column Web
            if self.stiffener_across_web == 'Yes':
                print(self.stiffener_plt_len_across_web)
                print(self.stiffener_plt_height_across_web)
                print(self.stiffener_plt_thick_across_web)
                print(self.shear_on_stiffener_across_web)
                print(self.shear_capa_stiffener_across_web)
                print(self.moment_on_stiffener_across_web)
                print(self.moment_capa_stiffener_across_web)
            else:
                print(self.stiffener_plt_len_across_web == 'N/A')
                print(self.stiffener_plt_height_across_web == 'N/A')
                print(self.stiffener_plt_thick_across_web == 'N/A')
                print(self.shear_on_stiffener_across_web == 'N/A')
                print(self.shear_capa_stiffener_across_web == 'N/A')
                print(self.moment_on_stiffener_across_web == 'N/A')
                print(self.moment_capa_stiffener_across_web == 'N/A')

        # Stiffener plate inside flange
        if self.connectivity == 'Moment Base Plate':
            if (self.anchors_outside_flange == 3) or (self.anchors_outside_flange == 6):
                if self.stiffener_inside_flange == 'Yes':
                    print(self.stiffener_plt_len_btwn_D_out)
                    print(self.stiffener_plt_width_btwn_D)
                    print(self.stiffener_plt_thick_btwn_D)

        # Shear Key Details
        print("Shear key details start")

        if self.shear_key_along_ColDepth == 'Yes':
            print(self.shear_key_len_ColDepth)
            print(self.shear_key_depth_ColDepth)
            print(self.shear_key_stress_ColDepth)
        else:
            self.shear_key_len_ColDepth = 0
            self.shear_key_depth_ColDepth = 0
            self.shear_key_stress_ColDepth = 0

        if self.shear_key_along_ColWidth == 'Yes':
            print(self.shear_key_len_ColWidth)
            print(self.shear_key_depth_ColWidth)
            print(self.shear_key_stress_ColWidth)
        else:
            self.shear_key_len_ColWidth = 0
            self.shear_key_depth_ColWidth = 0
            self.shear_key_stress_ColWidth = 0

        print(self.shear_key_thk)
        print("Shear key details end")

        # Weld
        if self.connectivity == 'Hollow/Tubular Column Base':
            print(self.weld_size_hollow)
        else:
            print(self.weld_size_flange if self.weld_type != 'Butt Weld' else '')  # Size at Flange (mm)
            print(self.weld_size_web if self.weld_type != 'Butt Weld' else '')  # Size at Web (mm)

            if self.stiffener_along_flange == 'Yes':
                print(self.weld_size_stiffener if self.weld_type != 'Butt Weld' else '')  # weld size at stiffener along flange (mm)

            if self.stiffener_along_web == 'Yes':
                print(self.weld_size_stiffener if self.weld_type != 'Butt Weld' else '')  # weld size at stiffener along web (mm)

            if self.stiffener_across_web == 'Yes':
                print(self.weld_size_stiffener if self.weld_type != 'Butt Weld' else '')  # weld size at stiffener along web (mm)

        # col properties
        print(self.column_D, self.column_bf, self.column_tf, self.column_tw, self.column_r1, self.column_r2)
        # print(self.w)

    # design report

    def save_design(self, popup_summary):
        """ create design report for the base plate module

        Args:
            self
            popup_summary

        Returns:

        """
        # start of design report

        # Section 1: Input Parameters
        # select image of section for displaying in report
        if self.connectivity == 'Hollow/Tubular Column Base':
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
            section_type = 'I Section'

        if self.dp_column_source == 'IS808_Rev':
            self.dp_column_source = 'IS 808\_Rev'

        self.column_properties = {
            KEY_DISP_SEC_PROFILE: select_section_img,  # select image of the section for displaying in design report

            # properties fro DP
            KEY_DISP_COLSEC_REPORT: self.dp_column_designation,
            # 'Section Type': section_type,
            # 'Type': self.dp_column_type,
            # 'Source': self.dp_column_source,
            KEY_DISP_MATERIAL: self.dp_column_material,
            KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.dp_column_fu,
            KEY_DISP_YIELD_STRENGTH_REPORT: self.dp_column_fy,

            # properties from DB
            KEY_REPORT_MASS: self.column_properties.mass,
            KEY_REPORT_AREA: round(self.column_properties.area / 100, 2),

            KEY_REPORT_NB if self.dp_column_designation[1:4] == 'CHS' else None: self.column_properties.nominal_bore if
            self.dp_column_designation[1:4] == 'CHS' else None,

            KEY_REPORT_OD if self.dp_column_designation[1:4] == 'CHS' else None: self.column_properties.out_diameter
            if self.dp_column_designation[1:4] == 'CHS' else None,

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_DEPTH: None if self.dp_column_designation[1:4] == 'CHS' else
            self.column_properties.depth,

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_WIDTH: None if self.dp_column_designation[1:4] == 'CHS' else
            self.column_properties.flange_width,

            None if self.connectivity == 'Hollow/Tubular Column Base' else KEY_REPORT_FLANGE_THK: None if self.connectivity == 'Hollow/Tubular Column Base' else
            self.column_properties.flange_thickness,

            KEY_REPORT_WEB_THK: self.column_properties.web_thickness,

            None if self.connectivity == 'Hollow/Tubular Column Base' else KEY_DISP_FLANGE_S_REPORT:
                None if self.connectivity == 'Hollow/Tubular Column Base' else self.column_properties.flange_slope,

            None if self.connectivity == 'Hollow/Tubular Column Base' else KEY_REPORT_R1: None if self.connectivity == 'Hollow/Tubular Column Base'
            else self.column_properties.root_radius,

            None if self.connectivity == 'Hollow/Tubular Column Base' else KEY_REPORT_R2: None if self.connectivity == 'Hollow/Tubular Column Base'
            else self.column_properties.toe_radius,

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_IZ:
                None if self.dp_column_designation[1:4] == 'CHS' else round(self.column_properties.mom_inertia_z / 10000, 2),

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_IY:
                None if self.dp_column_designation[1:4] == 'CHS' else round(self.column_properties.mom_inertia_y / 10000, 2),

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_RZ:
                None if self.dp_column_designation[1:4] == 'CHS' else round(self.column_properties.rad_of_gy_z / 10, 2),

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_RY:
                None if self.dp_column_designation[1:4] == 'CHS' else round(self.column_properties.rad_of_gy_y / 10, 2),

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_ZEZ:
                None if self.dp_column_designation[1:4] == 'CHS' else round(self.column_properties.elast_sec_mod_z / 1000, 2),

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_ZEY:
                None if self.dp_column_designation[1:4] == 'CHS' else round(self.column_properties.elast_sec_mod_y / 1000, 2),

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_ZPZ:
                None if self.dp_column_designation[1:4] == 'CHS' else round(self.column_properties.plast_sec_mod_z / 1000, 2),

            None if self.dp_column_designation[1:4] == 'CHS' else KEY_REPORT_ZPY:
                None if self.dp_column_designation[1:4] == 'CHS' else round(self.column_properties.plast_sec_mod_y / 1000, 2),

            KEY_REPORT_2ND_MOM if self.dp_column_designation[1:4] == 'CHS' else None: self.column_properties.mom_inertia if
            self.dp_column_designation[1:4] == 'CHS' else None,

            KEY_REPORT_RADIUS_GYRATION if self.dp_column_designation[1:4] == 'CHS' else None: self.column_properties.rad_of_gy if
            self.dp_column_designation[1:4] == 'CHS' else None,

            KEY_REPORT_SECTION_MODULUS if self.dp_column_designation[1:4] == 'CHS' else None: self.column_properties.elast_sec_mod if
            self.dp_column_designation[1:4] == 'CHS' else None,
            ' ': ' '
        }

        self.report_input = {
            # general parameters
            KEY_MAIN_MODULE: self.mainmodule,
            KEY_MODULE: self.module,
            KEY_CONN: self.connectivity,
            KEY_END_CONDITION: self.end_condition,
            KEY_DISP_AXIAL_BP: round(self.load_axial_input, 2),
            KEY_DISP_AXIAL_TENSION_BP: round(self.load_axial_tension * 10 ** -3, 2),
            KEY_DISP_SHEAR_BP: None,
            KEY_DISP_SHEAR_MAJOR: round(self.load_shear_major * 10 ** -3, 2),
            KEY_DISP_SHEAR_MINOR: round(self.load_shear_minor * 10 ** -3, 2),
            KEY_DISP_MOMENT: None,
            '- Major axis ($M_{z-z}$)': self.load_moment_major_report,
            '- Minor axis ($M_{y-y}$)': self.load_moment_minor_report,

            # column section
            "Column Section - Mechanical Properties": "TITLE",
            "Section Details": self.column_properties,

            # base plate
            "Base Plate - Design Preference": "TITLE",
            KEY_DISP_BASE_PLATE_MATERIAL: self.dp_bp_material,
            KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.base_plate.fu,
            KEY_DISP_YIELD_STRENGTH_REPORT: self.base_plate.fy,
            ' ': '',

            # stiffener plate/ shear key
            "Stiffener/Shear Key - Design Preference": "TITLE",
            KEY_DISP_ST_SK_MATERIAL: self.dp_stif_key_material,
            KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.stiff_key.fu,
            KEY_DISP_YIELD_STRENGTH_REPORT: self.stiff_key.fy,

            # anchor bolt outside column flange
            "Anchor Bolt - Input and Design Preference" if self.connectivity == 'Hollow/Tubular Column Base'
            else "Anchor Bolt Outside Column Flange - Input and Design Preference": "TITLE",

            KEY_DISP_OUT_DIA_ANCHOR: str(self.anchor_dia_out),
            KEY_DISP_OUT_GRD_ANCHOR: str(self.anchor_grade_list_out),
            KEY_DISP_DP_ANCHOR_BOLT_TYPE: self.dp_anchor_type_out,
            KEY_DISP_DP_ANCHOR_BOLT_GALVANIZED: self.dp_anchor_galv_out,
            KEY_DISP_DESIGNATION: self.dp_anchor_designation_out,
            KEY_DISP_REPORT_HOLE_TYPE: self.dp_anchor_hole_out,
            KEY_DISP_DP_ANCHOR_BOLT_LENGTH: self.anchor_length_provided_out,
            KEY_DISP_REPORT_MATERIAL_GRADE: self.anchor_fu_fy_outside_flange[0],

            # anchor bolt inside column flange
            "Anchor Bolt Inside Column Flange - Input and Design Prefereself.anchor_grade_list_outnce" if self.connectivity != 'Hollow/Tubular Column Base' else '':
                "TITLE" if self.connectivity != 'Hollow/Tubular Column Base' else '',

            None if self.connectivity == 'Hollow/Tubular Column Base' else 'Diameter (mm) ':
                None if self.connectivity == 'Hollow/Tubular Column Base' else str(self.anchor_dia_in) if self.connectivity == 'Moment Base Plate'
                                                                                                          and self.load_axial_tension > 0 else 'N/A',

            None if self.connectivity == 'Hollow/Tubular Column Base' else 'Property Class ':
                None if self.connectivity == 'Hollow/Tubular Column Base' else str(self.anchor_grade_list_in)
                if self.connectivity == 'Moment Base Plate' and self.load_axial_tension > 0 else 'N/A',

            None if self.connectivity == 'Hollow/Tubular Column Base' else 'Anchor Bolt Type ':
                None if self.connectivity == 'Hollow/Tubular Column Base' else self.dp_anchor_type_in if self.connectivity == 'Moment Base Plate'
                and self.load_axial_tension > 0 else 'N/A',

            None if self.connectivity == 'Hollow/Tubular Column Base' else 'Anchor Bolt Galvanized? ':
                None if self.connectivity == 'Hollow/Tubular Column Base' else self.dp_anchor_galv_in if self.connectivity == 'Moment Base Plate'
                and self.load_axial_tension > 0 else 'N/A',

            None if self.connectivity == 'Hollow/Tubular Column Base' else "Designation ":
                None if self.connectivity == 'Hollow/Tubular Column Base' else self.dp_anchor_designation_in if
                self.connectivity == 'Moment Base Plate' and self.load_axial_tension > 0 else 'N/A',

            None if self.connectivity == 'Hollow/Tubular Column Base' else 'Hole Type ':
                None if self.connectivity == 'Hollow/Tubular Column Base' else self.dp_anchor_hole_in if self.connectivity == 'Moment Base Plate'
                and self.load_axial_tension > 0 else 'N/A',

            None if self.connectivity == 'Hollow/Tubular Column Base' else 'Total Length (mm) ':
                None if self.connectivity == 'Hollow/Tubular Column Base' else self.anchor_length_provided_in if
                self.connectivity == 'Moment Base Plate' and self.load_axial_tension > 0 else 'N/A',

            None if self.connectivity == 'Hollow/Tubular Column Base' else 'Material Grade, $F_{u}$ (MPa) ':
                None if self.connectivity == 'Hollow/Tubular Column Base' else (self.anchor_fu_fy_inside_flange[0] if
                self.connectivity == 'Moment Base Plate' and self.load_axial_tension > 0 else 'N/A'),

            'Friction Coefficient (between concrete and anchor bolt)': self.dp_anchor_friction,

            # weld
            "Weld - Design Preference": "TITLE",
            KEY_DISP_DP_WELD_FAB: self.dp_weld_fab,
            KEY_DISP_DP_WELD_MATERIAL_G_O_REPORT: self.dp_weld_fu_overwrite,

            # detailing
            "Detailing - Design Preference": "TITLE",
            KEY_DISP_DP_DETAILING_EDGE_TYPE: self.dp_detail_edge_type,
            KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM: self.dp_detail_is_corrosive,

            # design method
            "Design - Design Preference": "TITLE",
            KEY_DISP_DP_DESIGN_METHOD: self.dp_design_method,
            KEY_DISP_DP_DESIGN_BASE_PLATE: 'Elastic Analysis Method' if self.connectivity == 'Moment Base Plate' else self.dp_bp_method
        }

        # Section 2: Design Checks
        self.report_check = []

        # defining additional attributes
        if self.pitch_distance_out > 0:
            k_b_out = min((self.end_distance_out / (3.0 * self.anchor_hole_dia_out)), ((self.pitch_distance_out / (3.0 * self.anchor_hole_dia_out)) -
                                                                                       0.25), (self.anchor_fu_fy_outside_flange[0] / self.dp_column_fu),
                          1.0)
        else:
            k_b_out = 1

        # start of checks

        # Check 1.1: Design Parameters
        t1 = ('SubSection', 'Design Parameters', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = ('Bearing Strength of Concrete (N/mm$^2$)', '', bearing_strength_concrete((int(self.bearing_strength_concrete / 0.45)),
                                                                                       self.bearing_strength_concrete), 'OK')
        self.report_check.append(t1)

        t1 = ('Grout Thickness (mm)', '', display_prov(self.grout_thk, "t_g"), 'OK')
        self.report_check.append(t1)

        if self.connectivity == 'Moment Base Plate':
            if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):
                t1 = ('Modular Ratio', '', modular_ratio((2 * 10 ** 5), (int(self.bearing_strength_concrete / 0.45)), self.n), 'OK')
                self.report_check.append(t1)

        t1 = ('Epsilon - stiffener plate', '', epsilon(self.stiffener_fy, round(self.epsilon, 2)), 'OK')
        self.report_check.append(t1)

        # Load Consideration Check
        t1 = ('SubSection', 'Load Consideration', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        t1 = (KEY_DISP_AXIAL_BP, display_prov(self.load_axial_input, "P_x"),
              axial_compression_prov(self.load_axial_input, self.column_axial_capacity, round(self.load_axial_compression * 1e-3, 2)),
              get_pass_fail(self.load_axial_input, self.column_axial_capacity, relation='leq'))
        self.report_check.append(t1)

        if self.connectivity == 'Moment Base Plate':
            t1 = (KEY_DISP_AXIAL_TENSION_BP, '', display_load_bp(round(self.load_axial_tension * 1e-3, 2), 'P_{up}'), "OK")
            self.report_check.append(t1)

        t1 = ("Shear Force - along major (z-z) axis (kN)", display_load_bp(round(self.column_shear_capacity, 2), 'V_{d}'),
              display_load_bp(round(self.load_shear_major * 1e-3, 2), 'V_1'),
              get_pass_fail(self.load_shear_major * 1e-3, self.column_shear_capacity, relation='leq'))
        self.report_check.append(t1)

        t1 = ("Shear Force - along minor (y-y) axis (kN)", display_load_bp(round(self.column_shear_capacity, 2), 'V_{d}'),
              display_load_bp(round(self.load_shear_minor * 1e-3, 2), 'V_2'),
              get_pass_fail(self.load_shear_minor * 1e-3, self.column_shear_capacity, relation='leq'))
        self.report_check.append(t1)

        if self.connectivity == 'Moment Base Plate':

            t1 = ("Bending Moment - major (z-z) axis (kNm)", display_load_bp(round(self.load_moment_major_report, 2), 'M_z'),
                  prov_moment_load_bp(moment_input=round(self.load_moment_major_report, 2), min_mc=round(0.5 * self.M_dz * 1e-6, 2),
                                      app_moment_load=round(self.load_moment_major * 1e-6, 2),
                                      moment_capacity=round(self.M_dz * 1e-6, 2), axis='Major', classification=self.col_classification),
                  get_pass_fail(self.load_moment_major_report, round(self.M_dz * 1e-6, 2), relation='leq'))
            self.report_check.append(t1)

            if self.load_moment_minor > 0:
                if self.load_moment_minor < (0.5 * self.M_dy):
                    t1 = ("Bending Moment - minor (y-y) axis (kNm)", display_load_bp(round(self.load_moment_minor_report, 2), 'M_y'),
                          prov_moment_load_bp(moment_input=round(self.load_moment_minor_report, 2), min_mc=round(0.5 * self.M_dy * 1e-6, 2),
                                              app_moment_load=round(self.load_moment_minor * 1e-6, 2),
                                              moment_capacity=round(self.M_dy * 1e-6, 2), axis='Minor', classification=self.col_classification),
                          get_pass_fail(self.load_moment_minor_report, round(self.M_dy * 1e-6, 2), relation='leq'))
                else:
                    t1 = ("Bending Moment - minor (y-y) axis (kNm)", display_load_bp(round(self.load_moment_minor_report, 2), 'M'),
                          display_load_bp(round(self.load_moment_minor_report, 2), 'M_{y}'),
                          get_pass_fail(self.load_moment_minor_report, round(self.M_dy * 1e-6, 2), relation='leq'))

                self.report_check.append(t1)

        if self.connectivity == 'Moment Base Plate':
            t1 = (KEY_INTERACTION_RATIO, 'I.R. < 1.0', IR_base_plate(round(self.load_axial_input, 2),
                                                                        round(self.column_axial_capacity, 2), round(self.load_moment_major_report, 2),
                                                                        round(self.M_dz * 1e-6, 2), self.IR_axial, self.IR_moment, self.sum_IR),
                  get_pass_fail(self.sum_IR, 1.0, relation='leq'))
        else:
            self.IR_axial = round(self.load_axial_input / self.column_axial_capacity, 2)
            self.sum_IR = round(self.IR_axial, 2)

            t1 = (KEY_INTERACTION_RATIO, 'I.R. < 1.0', IR_base_plate(round(self.load_axial_input, 2),
                                                                        round(self.column_axial_capacity, 2), 0.0, 0.0,
                                                                        self.IR_axial, 0.0, self.sum_IR),
                  get_pass_fail(self.sum_IR, 1.0, relation='leq'))

        self.report_check.append(t1)

        if self.connectivity == 'Moment Base Plate' and self.sum_IR <= 1.0:
            print_report_checks = True
        else:
            print_report_checks = False

        if self.connectivity != 'Moment Base Plate':
            if ((max(self.load_shear_major, self.load_shear_minor) * 1e-3) < self.column_shear_capacity) and (self.sum_IR <= 1.0):
                print_report_checks = True
            else:
                print_report_checks = False

        if print_report_checks == True:

            # Check 1.2: Plate Washer and Nut Details - Anchor Bolt Outside Column Flange
            if self.connectivity == 'Hollow/Tubular Column Base':
                t1 = ('SubSection', 'Plate Washer and Nut Details', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
            else:
                t1 = ('SubSection', 'Plate Washer and Nut Details - Anchor Bolt Outside Column Flange', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

            t1 = ('Plate Washer Size (mm)', '', square_washer_size(self.plate_washer_dim_out), 'Pass')
            self.report_check.append(t1)

            t1 = ('Plate Washer Thickness (mm)', '', square_washer_thk(self.plate_washer_thk_out), 'Pass')
            self.report_check.append(t1)

            t1 = ('Plate Washer Hole Diameter (mm)', '', square_washer_in_dia(self.plate_washer_inner_dia_out), 'Pass')
            self.report_check.append(t1)

            t1 = ('Nut (hexagon) Thickness (mm)', '', hexagon_nut_thickness(self.nut_thk_out), 'Pass')
            self.report_check.append(t1)

            t1 = ('End Plate Size (mm)', '', 'Square - ' + str(2 * self.plate_washer_dim_out) + ' X ' + str(2 * self.plate_washer_dim_out) + '', 'Pass')
            self.report_check.append(t1)

            t1 = ('End Plate Thickness (mm)', '', round_up(1.5 * self.plate_washer_thk_out, 2), 'Pass')
            self.report_check.append(t1)

            if self.load_axial_tension > 0 or self.load_moment_minor > 0:
                # Check 1.3: Plate Washer and Nut Details - Anchor Bolt Outside Column Flange
                t1 = ('SubSection', 'Plate Washer and Nut Details - Anchor Bolt Inside Column Flange', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t1 = ('Plate Washer Size (mm)', '', square_washer_size(self.plate_washer_dim_in), 'Pass')
                self.report_check.append(t1)

                t1 = ('Plate Washer Thickness (mm)', '', square_washer_thk(self.plate_washer_thk_in), 'Pass')
                self.report_check.append(t1)

                t1 = ('Plate Washer Hole Diameter (mm)', '', square_washer_in_dia(self.plate_washer_inner_dia_in), 'Pass')
                self.report_check.append(t1)

                t1 = ('Nut (hexagon) Thickness (mm)', '', hexagon_nut_thickness(self.nut_thk_in), 'Pass')
                self.report_check.append(t1)

                t1 = ('End Plate Size (mm)', '', 'Square - ' + str(2 * self.plate_washer_dim_in) + ' X ' + str(2 * self.plate_washer_dim_in) + '', 'Pass')
                self.report_check.append(t1)

                t1 = ('End Plate Thickness (mm)', '', round_up(1.5 * self.plate_washer_thk_in, 2), 'Pass')
                self.report_check.append(t1)

            # Check 2-1: Anchor Bolt Summary - Outside Column Flange
            if self.connectivity == 'Hollow/Tubular Column Base':
                t1 = ('SubSection', 'Anchor Bolt Summary', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
            else:
                t1 = ('SubSection', 'Anchor Bolt Summary - Outside Column Flange', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

            t2 = (KEY_REPORT_DIAMETER, '', self.anchor_dia_outside_flange, 'Pass')
            self.report_check.append(t2)

            t4 = (KEY_REPORT_BOLT_NOS, '', no_bolts(2 * self.anchors_outside_flange, location='out'), 'Pass')
            self.report_check.append(t4)

            t3 = (KEY_REPORT_PROPERTY_CLASS, '', self.anchor_grade_out, 'Pass')
            self.report_check.append(t3)

            # Check 2-2: Anchor Bolt Summary - Inside Column Flange

            if self.connectivity == 'Hollow/Tubular Column Base':
                pass
            else:
                t1 = ('SubSection', 'Anchor Bolt Summary - Inside Column Flange', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                if self.load_axial_tension > 0 or self.load_moment_minor > 0:

                    t2 = (KEY_REPORT_DIAMETER, '', self.anchor_dia_inside_flange, 'Pass')
                    self.report_check.append(t2)

                    t4 = (KEY_REPORT_BOLT_NOS, '', no_bolts(self.anchors_inside_flange, location='in'), 'Pass')
                    self.report_check.append(t4)

                    t3 = (KEY_REPORT_PROPERTY_CLASS, '', self.anchor_grade_in, 'Pass')
                    self.report_check.append(t3)
                else:
                    t2 = (KEY_REPORT_DIAMETER, '0', 'N/A', 'N/A')
                    self.report_check.append(t2)

                    t4 = (KEY_REPORT_BOLT_NOS, '0', no_bolts(0, location='in'), 'N/A')
                    self.report_check.append(t4)

                    t3 = (KEY_REPORT_PROPERTY_CLASS, 'N/A', 'N/A', 'N/A')
                    self.report_check.append(t3)

            # Check 3-1: Detailing Checks - Outside Column Flange
            if self.dp_detail_is_corrosive == "Yes":
                self.dp_detail_is_corrosive = True
            else:
                self.dp_detail_is_corrosive = False

            if self.connectivity == 'Hollow/Tubular Column Base':
                t1 = ('SubSection', 'Detailing Checks', '|p{4cm}|p{6.5cm}|p{4cm}|p{1.5cm}|')
                self.report_check.append(t1)
            else:
                t1 = ('SubSection', 'Detailing Checks - Outside Column Flange', '|p{4cm}|p{6.5cm}|p{4cm}|p{1.5cm}|')
                self.report_check.append(t1)

            min_end_out = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_outside_flange, self.dp_anchor_hole_out, self.dp_detail_edge_type)
            t2 = (KEY_REPORT_MIN_END, cl_10_2_4_2_min_edge_end_dist(self.anchor_hole_dia_out, edge_type=self.dp_detail_edge_type,
                                                                          parameter='end_dist'), self.end_distance_out,
                  get_pass_fail(min_end_out, self.end_distance_out, relation='leq'))
            self.report_check.append(t2)

            max_end_out = self.cl_10_2_4_3_max_edge_dist([(self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy), (0, 0, 0)],
                                                         corrosive_influences=self.dp_detail_is_corrosive)
            t3 = (KEY_REPORT_MAX_END, cl_10_2_4_3_max_edge_end_dist([(self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy),
                                                                             (self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy)],
                                                                            corrosive_influences=self.dp_detail_is_corrosive, parameter='end_dist'),
                  self.end_distance_out,
                  get_pass_fail(max_end_out, self.end_distance_out, relation='geq'))
            self.report_check.append(t3)

            min_edge_out = min_end_out
            t4 = (KEY_REPORT_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(self.anchor_hole_dia_out, edge_type=self.dp_detail_edge_type,
                                                                           parameter='edge_dist'), self.end_distance_out,
                  get_pass_fail(min_edge_out, self.edge_distance_out, relation='leq'))
            self.report_check.append(t4)

            max_edge_out = max_end_out
            t5 = (KEY_REPORT_MAX_EDGE, cl_10_2_4_3_max_edge_end_dist([(self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy),
                                                                              (self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy)],
                                                                             corrosive_influences=self.dp_detail_is_corrosive, parameter='edge_dist'),
                  self.end_distance_out,
                  get_pass_fail(max_edge_out, self.edge_distance_out, relation='geq'))
            self.report_check.append(t5)

            if (self.anchors_outside_flange == 4) or (self.anchors_outside_flange == 6):

                min_pitch_out = self.cl_10_2_2_min_spacing(self.anchor_dia_outside_flange)
                t6 = (KEY_REPORT_MIN_PITCH, cl_10_2_2_min_spacing(self.anchor_dia_outside_flange, parameter='pitch'), self.pitch_distance_out,
                      get_pass_fail(min_pitch_out, self.pitch_distance_out, relation='leq'))
                self.report_check.append(t6)

                max_pitch_out = self.cl_10_2_3_1_max_spacing([self.plate_thk_provided])
                t7 = (KEY_REPORT_MAX_PITCH, cl_10_2_3_1_max_spacing([self.plate_thk_provided, self.plate_thk_provided], parameter='pitch'),
                      self.pitch_distance_out,
                      get_pass_fail(max_pitch_out, self.pitch_distance_out, relation='geq'))
                self.report_check.append(t7)
            else:
                t8 = (KEY_REPORT_MIN_PITCH, 'N/A', self.pitch_distance_out, 'N/A')
                self.report_check.append(t8)

                t9 = (KEY_REPORT_MAX_PITCH, 'N/A', self.pitch_distance_out, 'N/A')
                self.report_check.append(t9)

            # Check 3-2: Detailing Checks - Inside Column Flange
            if self.load_axial_tension > 0:

                t1 = ('SubSection', 'Detailing Checks - Inside Column Flange', '|p{4cm}|p{6.5cm}|p{4cm}|p{1.5cm}|')
                self.report_check.append(t1)

                min_end_in = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided_inside_flange, self.dp_anchor_hole_in, self.dp_detail_edge_type)
                t2 = (KEY_REPORT_MIN_END, cl_10_2_4_2_min_edge_end_dist(self.anchor_hole_dia_in, edge_type=self.dp_detail_edge_type,
                                                                              parameter='end_dist'), self.end_distance_in,
                      get_pass_fail(min_end_in, self.end_distance_in,
                                    relation='leq'))
                self.report_check.append(t2)

                max_end_in = self.cl_10_2_4_3_max_edge_dist([(self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy), (0, 0, 0)],
                                                            corrosive_influences=self.dp_detail_is_corrosive)
                t3 = (KEY_REPORT_MAX_END, cl_10_2_4_3_max_edge_end_dist([(self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy),
                                                                                 (self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy)],
                                                                                corrosive_influences=self.dp_detail_is_corrosive, parameter='end_dist'),
                      self.end_distance_in,
                      get_pass_fail(max_end_in, self.end_distance_in, relation='geq'))
                self.report_check.append(t3)

                min_edge_in = min_end_in
                t4 = (KEY_REPORT_MIN_EDGE, cl_10_2_4_2_min_edge_end_dist(self.anchor_hole_dia_in, edge_type=self.dp_detail_edge_type,
                                                                               parameter='edge_dist'), self.end_distance_in,
                      get_pass_fail(min_edge_in, self.edge_distance_in,
                                    relation='leq'))
                self.report_check.append(t4)

                max_edge_in = max_end_in
                t5 = (KEY_REPORT_MAX_EDGE, cl_10_2_4_3_max_edge_end_dist([(self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy),
                                                                                  (self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy)],
                                                                                 corrosive_influences=self.dp_detail_is_corrosive, parameter='edge_dist'),
                      self.end_distance_in,
                      get_pass_fail(max_edge_in, self.edge_distance_in, relation='geq'))
                self.report_check.append(t5)

                if self.anchors_inside_flange == 8:
                    min_gauge_in = self.cl_10_2_2_min_spacing(self.anchor_dia_inside_flange)
                    t10 = (KEY_REPORT_MIN_GAUGE, cl_10_2_2_min_spacing(self.anchor_dia_inside_flange, parameter='gauge'), self.gauge_distance_in,
                           get_pass_fail(min_gauge_in, self.gauge_distance_in, relation='leq'))
                    self.report_check.append(t10)

                    max_gauge_in = self.cl_10_2_3_1_max_spacing([self.plate_thk_provided])
                    t11 = (KEY_REPORT_MAX_GAUGE, cl_10_2_3_1_max_spacing([self.plate_thk_provided, self.plate_thk_provided], parameter='pitch'),
                           self.gauge_distance_in,
                           get_pass_fail(max_gauge_in, self.gauge_distance_in, relation='geq'))
                    self.report_check.append(t11)

            # Check 4: Base Plate Dimension

            if self.connectivity == 'Hollow/Tubular Column Base':

                t1 = ('SubSection', 'Base Plate Dimension (L X W)', '|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                if self.dp_column_designation[1:4] == 'CHS':
                    t2 = (KEY_REPORT_PLATE_LENGTH, bp_length_sb(self.column_D, self.end_distance_out, self.bp_length_provided, self.projection, col_type='CHS'),
                          self.bp_length_provided,
                          get_pass_fail(self.bp_length_min, self.bp_length_provided, relation='leq'))
                    self.report_check.append(t2)
                else:
                    t2 = (KEY_REPORT_PLATE_LENGTH, bp_length_sb(self.column_D, self.end_distance_out, self.bp_length_provided, self.projection, col_type='SHS&RHS'),
                          self.bp_length_provided,
                          get_pass_fail(self.bp_length_min, self.bp_length_provided, relation='leq'))
                    self.report_check.append(t2)

                # width_min = 2 * self.load_axial_compression / (self.bp_length_min * self.bearing_strength_concrete)
                t3 = (KEY_REPORT_PLATE_WIDTH, bp_width(self.column_bf, self.edge_distance_out, self.bp_width_provided, self.dp_column_designation,
                                             self.projection, bp_type='hollow_bp', mom_bp_case='None'),
                      self.bp_width_provided, get_pass_fail(self.bp_width_min, self.bp_width_provided, relation='leq'))
                self.report_check.append(t3)
            else:
                if self.connectivity == 'Moment Base Plate':
                    t1 = ('SubSection', 'Base Plate Dimension (L X W)', '|p{4cm}|p{6.5cm}|p{4cm}|p{1.5cm}|')
                    self.report_check.append(t1)
                else:
                    t1 = ('SubSection', 'Base Plate Dimension (L X W)', '|p{4cm}|p{6cm}|p{4.5cm}|p{1.5cm}|')
                    self.report_check.append(t1)

                if self.connectivity == 'Moment Base Plate' and (self.moment_bp_case == 'Case2' or self.moment_bp_case == 'Case3'):
                    bolt_columns_out = self.bolt_columns_outside_flange
                else:
                    self.pitch_distance_out = 0
                    bolt_columns_out = 1

                t2 = (KEY_REPORT_PLATE_LENGTH, bp_length(self.column_D, self.end_distance_out, self.pitch_distance_out, round(self.bp_length_min, 2),
                                                         bolt_columns_out),
                      self.bp_length_provided,
                      get_pass_fail(self.bp_length_min, self.bp_length_provided, relation='leq'))
                self.report_check.append(t2)

                if self.connectivity == 'Moment Base Plate':
                    if self.moment_bp_case == 'Case1':
                        if self.min_width_check_Case1:

                            width_req = round(((2 * self.load_axial_compression) / (self.bp_length_provided * self.bearing_strength_concrete)), 2)  # mm
                            t3 = (KEY_REPORT_PLATE_WIDTH, bp_width(self.column_bf, self.edge_distance_out, round(self.bp_width_min, 2), self.dp_column_designation,
                                                         projection=0, bp_type='welded_moment_bp', mom_bp_case=self.moment_bp_case),
                                  bp_width_case1(self.load_axial_compression, self.bp_length_provided, self.bearing_strength_concrete,
                                                 self.bp_width_provided, width_req),
                                  get_pass_fail(self.bp_width_min, self.bp_width_provided, relation='leq'))
                            self.report_check.append(t3)
                        else:
                            t3 = (KEY_REPORT_PLATE_WIDTH,
                                  bp_width(self.column_bf, self.edge_distance_out, round(self.bp_width_min, 2), self.dp_column_designation, projection=0,
                                           bp_type='welded_moment_bp', mom_bp_case=self.moment_bp_case),
                                  self.bp_width_provided, get_pass_fail(self.bp_width_min, self.bp_width_provided, relation='leq'))
                            self.report_check.append(t3)
                    else:
                        t3 = (KEY_REPORT_PLATE_WIDTH, bp_width(self.column_bf, self.edge_distance_out, round(self.bp_width_min, 2), self.dp_column_designation, projection=0,
                                                     bp_type='welded_moment_bp', mom_bp_case=self.moment_bp_case),
                              self.bp_width_provided, get_pass_fail(self.bp_width_min, self.bp_width_provided, relation='leq'))
                        self.report_check.append(t3)

                else:
                    t3 = (KEY_REPORT_PLATE_WIDTH, bp_width(self.column_bf, self.edge_distance_out, round(self.bp_width_min, 2), self.dp_column_designation,
                                                 projection=0, bp_type='welded_moment_bp', mom_bp_case='None'),
                          self.bp_width_provided, get_pass_fail(self.bp_width_min, self.bp_width_provided, relation='leq'))
                    self.report_check.append(t3)

            # Check 5: Base Plate Analyses

            if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                t1 = ('SubSection', 'Base Plate Analysis', '|p{3cm}|p{8.2cm}|p{4.3cm}|p{1cm}|')
                self.report_check.append(t1)

                t2 = ('Min. Area Required (mm$^2$)', min_area_req(round(self.load_axial_compression, 2), self.bearing_strength_concrete, self.min_area_req),
                      min_area_provided(self.bp_area_provided, self.bp_length_provided, self.bp_width_provided),
                      get_pass_fail(self.min_area_req, self.bp_area_provided, relation='leq'))
                self.report_check.append(t2)

                if self.connectivity == 'Welded Column Base':
                    t3 = ('Effective Bearing Area (mm$^2$)', eff_bearing_area(self.column_D, self.column_bf, self.column_tf, self.column_tw,
                                                                            col_type='I-section'), '', 'OK')
                    self.report_check.append(t3)
                else:
                    if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                        t3 = ('Effective Bearing Area (mm$^2$)', eff_bearing_area(self.column_D, self.column_bf, self.column_tf, self.column_tw,
                                                                                col_type='SHS&RHS'), '', 'OK')
                        self.report_check.append(t3)
                    else:
                        t3 = ('Effective Bearing Area (mm$^2$)', eff_bearing_area(self.column_D, self.column_bf, self.column_tf, self.column_tw,
                                                                                col_type='CHS'), '', 'OK')
                        self.report_check.append(t3)

                if self.connectivity == 'Welded Column Base':
                    t4 = ('Projection (mm)', eff_projection(self.column_D, self.column_bf, self.column_tf, self.column_tw, self.min_area_req,
                                                            self.projection_dr, self.end_distance_out, col_type='I-section'), self.projection, 'Pass')
                    self.report_check.append(t4)
                else:
                    if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                        t4 = ('Projection (mm)', eff_projection(self.column_D, self.column_bf, self.column_tf, self.column_tw, self.min_area_req,
                                                                self.projection_dr, self.end_distance_out, col_type='SHS&RHS'), self.projection, 'Pass')
                        self.report_check.append(t4)
                    else:
                        t4 = ('Projection (mm)', eff_projection(self.column_D, self.column_bf, self.column_tf, self.column_tw, self.min_area_req,
                                                                self.projection_dr, self.end_distance_out, col_type='CHS'), self.projection, 'Pass')
                        self.report_check.append(t4)

                t5 = ('Actual Bearing Stress (N/mm$^2$)', self.bearing_strength_concrete,
                      actual_bearing_pressure(round(self.load_axial_compression, 2), self.bp_area_provided, self.w),
                      get_pass_fail(self.bearing_strength_concrete, self.w, relation='geq'))
                self.report_check.append(t5)

                if (self.shear_key_along_ColDepth == 'Yes') or (self.shear_key_along_ColWidth == 'Yes'):
                    plate_thk_check = max(self.column_tf, self.column_tw, self.shear_key_thk)
                else:
                    plate_thk_check = max(self.column_tf, self.column_tw)

                t6 = ('Thickness of Base Plate (mm)', plate_thk_required(self.column_tf, self.column_tw, self.shear_key_along_ColDepth,
                                                                         self.shear_key_thk, self.shear_key_along_ColWidth, self.shear_key_thk,
                                                                         self.standard_plate_thk[-1]),
                      bp_thk_1(self.plate_thk, self.plate_thk_provided, self.projection, self.w, self.gamma_m0, self.base_plate.fy),
                      get_pass_fail(plate_thk_check, self.plate_thk_provided, relation='leq') and
                      get_pass_fail(self.standard_plate_thk[-1], self.plate_thk_provided, relation='geq'))
                self.report_check.append(t6)

            elif self.connectivity == 'Moment Base Plate':
                t1 = ('SubSection', 'Base Plate Analysis', '|p{3cm}|p{6.5cm}|p{5.5cm}|p{1cm}|')
                self.report_check.append(t1)

                t1 = ('Eccentricity - about major axis (mm)', '', eccentricity(round(self.load_moment_major * 10 ** -6, 2),
                                                                                 round(self.load_axial_compression * 10 ** -3, 2),
                                                                                 self.eccentricity_zz), 'OK')
                self.report_check.append(t1)

                if self.moment_bp_case == 'Case1':
                    t2 = ('Base Plate Type', mom_bp_case(self.moment_bp_case, self.eccentricity_zz, self.bp_length_min),
                          'Case 1: The base plate is purely under compression/bearing with no tension force acting on the anchor bolts outside column '
                          'flange on either side', 'OK')
                    self.report_check.append(t2)
                elif self.moment_bp_case == 'Case2':
                    t2 = ('Base Plate Type', mom_bp_case(self.moment_bp_case, self.eccentricity_zz, self.bp_length_min),
                          'Case 2: The base plate is mostly under compression/bearing while a small tension force being transferred through the anchor '
                          'bolts outside column flange on the tension side', 'OK')
                    self.report_check.append(t2)
                elif self.moment_bp_case == 'Case3':
                    t2 = ('Base Plate Type', mom_bp_case(self.moment_bp_case, self.eccentricity_zz, self.bp_length_min),
                          'Case 3: A smaller part of the base plate is under compression/bearing while a large tension force being transferred through '
                          'the anchor bolts outside column flange on the tension side', 'OK')
                    self.report_check.append(t2)

                if self.moment_bp_case == 'Case1':
                    t10 = ('Total tension demand $(kN)$', 'P_t = 0 ', '', 'OK')
                    self.report_check.append(t10)

                    t3 = ('Elastic Section Modulus - of the base plate $(mm^3)$', '', bp_section_modulus(self.bp_length_provided, self.bp_width_provided,
                                                                                                     self.ze_zz), 'OK')
                    self.report_check.append(t3)

                    t5 = ('Critical Section (mm)', critical_section(self.bp_length_provided, self.column_D, self.critical_xx), '', 'OK')
                    self.report_check.append(t5)

                    t4 = ('Bending Stress (N/mm$^2$)', self.bearing_strength_concrete,
                          bending_stress(round(self.load_axial_compression * 10 ** -3, 2), self.load_moment_major * 10 ** -6, self.bp_length_provided,
                                         self.bp_width_provided, self.bp_area_provided, self.ze_zz, self.sigma_max_zz, self.sigma_min_zz),
                          get_pass_fail(self.sigma_max_zz, self.bearing_strength_concrete, relation='leq'))
                    self.report_check.append(t4)

                    t6 = ('Bending Stress - at critical section (N/mm$^2$)', self.bearing_strength_concrete, bending_stress_critical_sec(self.sigma_xx),
                          'OK')
                    self.report_check.append(t6)

                    t7 = ('Bending Moment - at critical section $(N-mm)$', moment_critical_section(self.sigma_xx, self.sigma_max_zz, self.critical_xx,
                                                                                                 self.critical_M_xx, 0, self.bp_width_provided,
                                                                                                   case='Case1'),
                          'Bending of the base plate is governed by the bearing stress caused by the footing', 'OK')
                    self.report_check.append(t7)

                    t8 = ('Moment Capacity - of base plate', md_plate(), '', 'OK')
                    self.report_check.append(t8)

                    if (self.shear_key_along_ColDepth == 'Yes') or (self.shear_key_along_ColWidth == 'Yes'):
                        plate_thk_check = max(self.column_tf, self.column_tw, self.shear_key_thk)
                    else:
                        plate_thk_check = max(self.column_tf, self.column_tw)

                    self.base_plate.connect_to_database_to_get_fy_fu(self.dp_bp_material, 0)  # update fy
                    t9 = ('Thickness of Base Plate (mm)', plate_thk_required(self.column_tf, self.column_tw, self.shear_key_along_ColDepth,
                                                                             self.shear_key_thk, self.shear_key_along_ColWidth, self.shear_key_thk,
                                                                             self.standard_plate_thk[-1]),
                          plate_thk1(self.critical_M_xx, self.plate_thk, self.plate_thk_provided, self.gamma_m0, self.base_plate.fy,
                                     self.bp_width_provided, case='Case1'),
                          get_pass_fail(plate_thk_check, self.plate_thk_provided, relation='leq') and
                          get_pass_fail(self.standard_plate_thk[-1], self.plate_thk_provided, relation='geq'))
                    self.report_check.append(t9)

                if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):
                    t3 = ('k1', k1(self.eccentricity_zz, self.bp_length_provided, self.k1), '', 'OK')
                    self.report_check.append(t3)

                    t4 = ('Total Area of Anchor Bolt -  under tension (mm$^2$)', total_anchor_area_tension(self.anchor_dia_outside_flange,
                                                                                                      self.anchors_outside_flange,
                                                                                                      self.anchor_area_tension), '', 'OK')
                    self.report_check.append(t4)

                    t5 = ('Lever Arm - distance between the centre of the column and the C.G of the bolt group under tension (mm)',
                          calc_f(self.end_distance_out, self.bp_length_provided, self.f), '', 'OK')
                    self.report_check.append(t5)

                    t6 = ('k2', k2(self.n, self.anchor_area_tension, self.bp_width_provided, self.f, self.eccentricity_zz, self.k2), '', 'OK')
                    self.report_check.append(t6)

                    t7 = ('k3', k3(self.k2, self.bp_length_provided, self.f, self.k3), '', 'OK')
                    self.report_check.append(t7)

                    t8 = ('Effective Bearing Length (mm)', y(self.k1, self.k2, self.k3, self.y), '', 'OK')
                    self.report_check.append(t8)

                    t9 = ('Total Tension Demand $(kN)$', tension_demand_anchor(round(self.load_axial_compression * 10 ** -3, 2), self.bp_length_provided,
                                                                               self.y, self.eccentricity_zz, self.f, self.tension_demand_anchor), '', 'OK')
                    self.report_check.append(t9)

                    t11 = ('Critical Section - compression side (mm)', critical_section_case_2_3(self.critical_xx, self.y, self.bp_length_provided,
                                                                                                   self.column_D), '', 'OK')
                    self.report_check.append(t11)

                    t12 = ('Bending Moment - at critical section (due to bearing stress) $(N-mm)$',
                           moment_critical_section(0, 0, round(self.critical_xx, 2), self.critical_M_xx, (self.bearing_strength_concrete / 0.45),
                                                   self.bp_width_provided, case='Case2&3'), '', 'OK')
                    self.report_check.append(t12)

                    t13 = ('Lever Arm - distance between center of the flange and bolt group (tension side) (mm)',
                           lever_arm_tension(self.bp_length_provided, self.column_D, self.column_tf, self.end_distance_out, self.lever_arm), '', 'OK')
                    self.report_check.append(t13)

                    t14 = ('Bending Moment - at critical section (due to tension in the anchor bolts) $(N-mm)$',
                           lever_arm_moment(self.tension_demand_anchor, self.lever_arm, self.moment_lever_arm), '', 'OK')
                    self.report_check.append(t14)

                    if self.critical_M_xx > self.moment_lever_arm:
                        governing = 'bearing'
                    else:
                        governing = 'tension'

                    t15 = ('Maximum Bending Moment $(N-mm)$', max_moment(self.critical_M_xx, self.moment_lever_arm),
                           'Bending of the base plate is governed by the bearing stress caused by the footing' if governing == 'bearing' else
                           'Bending of the base plate is governed by the tension in the anchor bolts due to uplift', 'OK')
                    self.report_check.append(t15)

                    t16 = ('Moment Capacity of Base Plate', md_plate(), '', 'OK')
                    self.report_check.append(t16)

                    if (self.shear_key_along_ColDepth == 'Yes') or (self.shear_key_along_ColWidth == 'Yes'):
                        plate_thk_check = max(self.column_tf, self.column_tw, self.shear_key_thk)
                    else:
                        plate_thk_check = max(self.column_tf, self.column_tw)

                    self.base_plate.connect_to_database_to_get_fy_fu(self.dp_bp_material, 0)  # update fy
                    t17 = ('Thickness of Base Plate (mm)', plate_thk_required(self.column_tf, self.column_tw, self.shear_key_along_ColDepth,
                                                                             self.shear_key_thk, self.shear_key_along_ColWidth, self.shear_key_thk,
                                                                             self.standard_plate_thk[-1]),
                          plate_thk1(self.critical_M_xx, self.plate_thk, self.plate_thk_provided, self.gamma_m0, self.base_plate.fy,
                                     self.bp_width_provided, case='Case2&3'),
                          get_pass_fail(plate_thk_check, self.plate_thk_provided, relation='leq') and
                          get_pass_fail(self.standard_plate_thk[-1], self.plate_thk_provided, relation='geq'))
                    self.report_check.append(t17)

                    t18 = ('Maximum Bearing Stress on Footing (N/mm$^2$)', sigma_allowalbe(self.bearing_strength_concrete),
                           max_bearing_stress(self.tension_demand_anchor, self.y, self.anchor_area_tension, self.n, self.bp_length_provided, self.f,
                                              self.max_bearing_stress), get_pass_fail(self.bearing_strength_concrete, self.max_bearing_stress,
                                                                                      relation='geq'))
                    self.report_check.append(t18)

            # Check 6: Anchor Bolt Design - Outside Column Flange

            if self.connectivity == 'Hollow/Tubular Column Base':
                t1 = ('SubSection', 'Anchor Bolt Design', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
            else:
                t1 = ('SubSection', 'Anchor Bolt Design - Outside Column Flange', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

            t2 = (KEY_REPORT_SHEAR_CAPA, '', cl_10_3_3_bolt_shear_capacity(self.anchor_fu_fy_outside_flange[0], 1, self.anchor_area_outside_flange[1],
                                                                             self.gamma_mb, self.shear_capacity_anchor), 'OK')
            self.report_check.append(t2)

            if self.pitch_distance_out > 0:
                k_b_out = min(self.end_distance_out / (3.0 * self.anchor_hole_dia_out), self.pitch_distance_out / (3.0 * self.anchor_hole_dia_out) - 0.25,
                              self.anchor_fu_fy_outside_flange[0] / self.dp_column_fu, 1.0)
            else:
                k_b_out = min(self.end_distance_out / (3.0 * self.anchor_hole_dia_out), self.anchor_fu_fy_outside_flange[0] / self.dp_column_fu, 1.0)

            t3 = (KEY_DISP_KB, '', cl_10_3_4_calculate_kb(self.end_distance_out, self.pitch_distance_out, self.anchor_hole_dia_out,
                                                          self.anchor_fu_fy_outside_flange[0], self.dp_column_fu), 'OK')
            self.report_check.append(t3)

            self.base_plate.connect_to_database_to_get_fy_fu(self.dp_bp_material, self.plate_thk_provided)  # update fy
            t4 = (KEY_REPORT_BEARING_CAPA, '', cl_10_3_4_bolt_bearing_capacity(k_b_out, self.anchor_dia_provided_outside_flange,
                                                                                 [(self.plate_thk_provided, self.base_plate.fu, self.base_plate.fy),
                                                                                  (0, 0, 0)], self.gamma_mb, self.bearing_capacity_anchor,
                                                                                 self.dp_anchor_hole_out), 'OK')
            self.report_check.append(t4)

            t5 = (KEY_REPORT_BOLT_CAPA, '', cl_10_3_2_bolt_capacity(self.shear_capacity_anchor, self.bearing_capacity_anchor, self.anchor_capacity),
                  'OK')
            self.report_check.append(t5)

            t6 = ('Tension Demand - per anchor bolt $(kN)$', tension_demand_per_bolt(self.tension_demand_anchor, self.anchors_outside_flange),
                  cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_outside_flange[0], self.anchor_fu_fy_outside_flange[1],
                                                            self.anchor_area_outside_flange[0], self.anchor_area_outside_flange[1],
                                                            self.tension_capacity_anchor, fabrication=KEY_DP_FAB_FIELD),
                  get_pass_fail((self.tension_demand_anchor / self.anchors_outside_flange), self.tension_capacity_anchor, relation='leq'))
            self.report_check.append(t6)

            t7 = ('Anchor Length - above concrete footing (mm)', '', anchor_len_above(self.grout_thk, self.plate_thk_provided, self.plate_washer_thk_out,
                                                                                      self.nut_thk_out, self.anchor_len_above_footing_out), 'Pass')
            self.report_check.append(t7)

            if self.connectivity == 'Moment Base Plate':
                if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):

                    t8 = ('Anchor Length - below concrete footing (mm)', '', anchor_len_below(self.tension_capacity_anchor,
                                                                                              (self.bearing_strength_concrete / 0.45),
                                                                                              self.anchor_len_below_footing_out,
                                                                                                self.anchor_length_provided_out_report,
                                                                                                round_up(self.anchor_length_provided_out_report, 5),
                                                                                                self.anchor_length_min_out, self.nut_thk_out,
                                                                                                connectivity='Moment Base Plate', case='Case2&3'), 'Pass')
                    self.report_check.append(t8)
                else:
                    t8 = ('Anchor Length - below concrete footing (mm)', '', anchor_len_below(0, 0, self.anchor_len_below_footing_out, 0, 0, 0, 0,
                                                                                                connectivity='Moment Base Plate', case='Case1'), 'Pass')
                    self.report_check.append(t8)
            else:
                t8 = ('Anchor Length - below concrete footing (mm)', '', anchor_len_below(0, 0, self.anchor_len_below_footing_out, 0, 0, 0, 0,
                                                                                            connectivity='Welded Column Base', case='None'), 'Pass')
                self.report_check.append(t8)

            t9 = ('Anchor Length - total (mm)', anchor_range(self.anchor_length_min_out, self.anchor_length_max_out),
                  anchor_length(self.anchor_len_above_footing_out, self.anchor_len_below_footing_out, self.anchor_length_provided_out),
                  get_pass_fail(self.anchor_length_min_out, self.anchor_length_provided_out, relation='leq'))
            self.report_check.append(t9)

            # Check 7: Anchor Bolt Design - Inside Column Flange
            if self.connectivity == 'Moment Base Plate':

                if self.load_axial_tension > 0 or self.load_moment_minor > 0:

                    t1 = ('SubSection', 'Anchor Bolt Design - Inside Column Flange', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                    self.report_check.append(t1)

                    t2 = (KEY_REPORT_SHEAR_CAPA, 'The bolts are not designed to carry shear force', 'N/A', 'N/A')
                    self.report_check.append(t2)

                    t4 = (KEY_REPORT_BEARING_CAPA, 'The bolts are not designed to carry shear force', 'N/A', 'N/A')
                    self.report_check.append(t4)

                    t5 = (KEY_REPORT_BOLT_CAPA, 'N/A', 'N/A', 'N/A')
                    self.report_check.append(t5)

                    t6 = (KEY_REPORT_TENSION_DEMAND, uplift_demand(self.load_axial_tension * 10 ** -3), '', 'OK')
                    self.report_check.append(t6)

                    t7 = (KEY_REPORT_TENSION_CAPA, '', cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy_inside_flange[0],
                                                                                                 self.anchor_fu_fy_inside_flange[1],
                                                                                                 self.anchor_area_inside_flange[0],
                                                                                                 self.anchor_area_inside_flange[1],
                                                                                                 self.tension_capacity_anchor_uplift), 'OK')
                    self.report_check.append(t7)

                    t8 = ('Anchor Bolts Required $(kN)$', no_bolts_uplift(self.load_axial_tension * 10 ** -3, self.tension_capacity_anchor_uplift),
                          self.anchors_inside_flange,
                          get_pass_fail((self.load_axial_tension * 10 ** -3) / self.tension_capacity_anchor_uplift, self.anchors_inside_flange,
                                        relation='leq'))
                    self.report_check.append(t8)

                    t9 = ('Anchor Length - above concrete footing (mm)', '', anchor_len_above(self.grout_thk, self.plate_thk_provided, self.plate_washer_thk_in,
                                                                                              self.nut_thk_in, self.anchor_len_above_footing_in), 'Pass')
                    self.report_check.append(t9)

                    if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):
                        t10 = ('Anchor Length - below concrete footing (mm)', '', anchor_len_below(self.tension_capacity_anchor_uplift,
                                                                                              (self.bearing_strength_concrete / 0.45),
                                                                                              self.anchor_len_below_footing_in,
                                                                                                self.anchor_length_provided_in_report,
                                                                                                round_up(self.anchor_length_provided_in_report, 5),
                                                                                                self.anchor_length_min_in, self.nut_thk_in,
                                                                                                connectivity='Moment Base Plate', case='Case2&3'),
                               'Pass')
                        self.report_check.append(t10)
                    else:
                        t10 = ('Anchor Length - below concrete footing (mm)', '', anchor_len_below(0, 0, self.anchor_len_below_footing_in, 0, 0, 0, 0,
                                                                                                    connectivity='Moment Base Plate', case='Case1'),
                              'Pass')
                        self.report_check.append(t10)

                    t11 = ('Anchor Length - total (mm)', anchor_range(self.anchor_length_min_in, self.anchor_length_max_in),

                           anchor_length(self.anchor_len_above_footing_in, self.anchor_len_below_footing_in, self.anchor_length_provided_in),

                           get_pass_fail(self.anchor_length_min_in, self.anchor_length_provided_in, relation='leq'))
                    self.report_check.append(t11)

            # Check 8: Stiffener Design

            # Check 8.1: For moment and welded case
            if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Moment Base Plate'):

                if self.stiffener_along_flange == 'Yes':
                    t1 = ('SubSection', 'Stiffener Design - Along Column Flange', '|p{3.5cm}|p{6cm}|p{5.5cm}|p{1cm}|')
                    self.report_check.append(t1)

                    self.stiffener_plt_len_along_flange = round(self.stiffener_plt_len_along_flange, 2)

                    t2 = ('Length of Stiffener (mm)', '', stiff_len_flange(self.bp_width_provided, self.column_bf,
                                                                             round(self.stiffener_plt_len_along_flange, 2)),
                          'OK')
                    self.report_check.append(t2)

                    t3 = ('Height of Stiffener (mm)', '', stiff_height_flange(self.stiffener_plt_len_along_flange,
                                                                                self.stiffener_plt_height_along_flange), 'OK')
                    self.report_check.append(t3)

                    t4 = ('Thickness of Stiffener (mm)', stiff_thk_flange(self.thk_req_stiffener_along_flange, self.stiffener_plt_len_along_flange,
                                                                            self.epsilon, self.column_tf),
                          self.stiffener_plt_thick_along_flange,
                          get_pass_fail(max(self.thk_req_stiffener_along_flange, self.column_tf), self.stiffener_plt_thick_along_flange, relation='leq'))
                    self.report_check.append(t4)

                    t5 = ('Stress (average) at Stiffener (N/mm$^2$)', stiffener_stress_allowable(self.bearing_strength_concrete),

                          stiffener_stress_flange(self.sigma_xx, self.sigma_max_zz, self.sigma_min_zz, self.bp_length_provided, self.column_D, self.y,
                                                  self.critical_xx, self.sigma_avg, self.sigma_lby2, self.connectivity, self.moment_bp_case),

                          get_pass_fail(self.bearing_strength_concrete, self.sigma_avg, relation='geq'))
                    self.report_check.append(t5)

                    t6 = ('Shear on Stiffener $(kN)$', shear_demand_stiffener(self.sigma_avg, self.y, self.critical_xx, self.column_bf,
                                                                              self.bp_length_provided, self.shear_on_stiffener_along_flange,
                                                                              self.connectivity, self.moment_bp_case, self.anchors_outside_flange,
                                                                              self.stiffener_plt_len_along_flange, 0, location='flange'),

                          shear_capacity_stiffener(self.stiffener_plt_thick_along_flange, self.stiffener_plt_height_along_flange, self.stiffener_fy,
                                                   self.shear_capa_stiffener_along_flange, self.gamma_m0, location='flange'),

                          get_pass_fail(self.shear_on_stiffener_along_flange, self.shear_capa_stiffener_along_flange, relation='leq'))
                    self.report_check.append(t6)

                    t7 = ('Section Modulus of the Stiffener $(mm^3)$', '', section_modulus_stiffener(self.z_e_stiffener_along_flange,
                                                                                                       modulus='elastic'), 'OK')
                    self.report_check.append(t7)

                    t8 = ('Moment on Stiffener $(kNm)$', moment_demand_stiffener(self.sigma_max_zz, self.sigma_xx, self.sigma_avg, self.y,
                                                                                  self.critical_xx, self.bp_length_provided, self.column_bf,
                                                                                  self.stiffener_plt_len_along_flange, self.stiffener_plt_len_along_web,
                                                                                  self.moment_on_stiffener_along_flange, self.anchors_outside_flange,
                                                                                  self.connectivity, self.moment_bp_case, location='flange'),

                          moment_capacity_stiffener(self.z_e_stiffener_along_flange, self.stiffener_fy, self.gamma_m0,
                                                    self.moment_capa_stiffener_along_flange, location='flange', modulus='elastic'),

                          get_pass_fail(self.moment_on_stiffener_along_flange, self.moment_capa_stiffener_along_flange, relation='leq'))
                    self.report_check.append(t8)

                    t5 = ('Weld Size (mm)', self.weld_stiffener_flange.min_size, self.weld_size_stiffener_along_flange, 'Pass')
                    self.report_check.append(t5)

                if self.stiffener_along_web == 'Yes':

                    t1 = ('SubSection', 'Stiffener Design - Along Column Web', '|p{3.5cm}|p{6cm}|p{5.5cm}|p{1cm}|')
                    self.report_check.append(t1)

                    self.stiffener_plt_len_along_web = round(self.stiffener_plt_len_along_web, 2)

                    t2 = ('Length of Stiffener (mm)', '', stiff_len_web(self.bp_length_provided, self.column_D,
                                                                          round(self.stiffener_plt_len_along_web, 2)),
                          'OK')
                    self.report_check.append(t2)

                    t3 = ('Height of Stiffener (mm)', '', stiff_height_web(self.stiffener_plt_len_along_web, self.stiffener_plt_height_along_web),
                          'OK')
                    self.report_check.append(t3)

                    t4 = ('Thickness of Stiffener (mm)', stiff_thk_web(self.thk_req_stiffener_along_web, self.stiffener_plt_len_along_web,
                                                                         self.epsilon, self.column_tw, self.bolt_columns_outside_flange),
                          self.stiffener_plt_thick_along_web,
                          get_pass_fail(max(self.thk_req_stiffener_along_web, self.column_tw), self.stiffener_plt_thick_along_web, relation='leq'))
                    self.report_check.append(t4)

                    if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                        t5 = ('Stress (average) at Stiffener (mm)', stiffener_stress_allowable(self.bearing_strength_concrete),
                              stiffener_stress_web(0, 0, self.sigma_xx, type='welded_hollow_bp'),
                              get_pass_fail(self.bearing_strength_concrete, self.sigma_xx, relation='geq'))
                        self.report_check.append(t5)

                    if self.connectivity == 'Moment Base Plate':

                        t5 = ('Stress (average) at Stiffener (mm)', stiffener_stress_allowable(self.bearing_strength_concrete),
                              stiffener_stress_web(self.sigma_max_zz, self.sigma_xx, self.sigma_avg_2, type='moment_bp'),
                              get_pass_fail(self.bearing_strength_concrete, self.sigma_avg_2, relation='geq'))
                        self.report_check.append(t5)

                    t6 = ('Shear on Stiffener $(kN)$', shear_demand_stiffener(self.sigma_avg_2, self.y, self.critical_xx, self.column_bf,
                                                                              self.bp_length_provided, self.shear_on_stiffener_along_web,
                                                                              self.connectivity, self.moment_bp_case, self.anchors_outside_flange,
                                                                              self.stiffener_plt_len_along_flange, self.stiffener_plt_len_along_web,
                                                                              location='web'),

                          shear_capacity_stiffener(self.stiffener_plt_thick_along_web, self.stiffener_plt_height_along_web, self.stiffener_fy,
                                                   self.shear_capa_stiffener_along_web, self.gamma_m0, location='web'),

                          get_pass_fail(self.shear_on_stiffener_along_web, self.shear_capa_stiffener_along_web, relation='leq'))
                    self.report_check.append(t6)

                    t7 = ('Section Modulus of the Stiffener $(mm^3)$', '', section_modulus_stiffener(self.z_e_stiffener_along_web,
                                                                                                       modulus='elastic'), 'OK')
                    self.report_check.append(t7)

                    t8 = ('Moment on Stiffener $(kNm)$', moment_demand_stiffener(self.sigma_max_zz, self.sigma_xx, self.sigma_avg, self.y,
                                                                                  self.critical_xx, self.bp_length_provided, self.column_bf,
                                                                                  self.stiffener_plt_len_along_flange, self.stiffener_plt_len_along_web,
                                                                                  self.moment_on_stiffener_along_web, self.anchors_outside_flange,
                                                                                  self.connectivity, self.moment_bp_case, location='web'),

                          moment_capacity_stiffener(self.z_e_stiffener_along_web, self.stiffener_fy, self.gamma_m0,
                                                    self.moment_capa_stiffener_along_web, location='web', modulus='elastic'),

                          get_pass_fail(self.moment_on_stiffener_along_web, self.moment_capa_stiffener_along_web, relation='leq'))
                    self.report_check.append(t8)

                    t5 = ('Weld Size (mm)', self.weld_stiffener_web.min_size, self.weld_size_stiffener_along_web, 'Pass')
                    self.report_check.append(t5)

                if self.stiffener_across_web == 'Yes':

                    t1 = ('SubSection', 'Stiffener Design - Across Column Web', '|p{3.5cm}|p{6cm}|p{5.5cm}|p{1cm}|')
                    self.report_check.append(t1)

                    self.stiffener_plt_len_across_web = round(self.stiffener_plt_len_across_web, 2)

                    t2 = ('Length of Stiffener (mm)', '', stiff_len_across_web(round(self.stiffener_plt_len_along_flange, 2),
                                                                                 round(self.stiffener_plt_len_along_web, 2),
                                                                                 round(self.stiffener_plt_len_across_web, 2), self.connectivity),
                          'Pass')
                    self.report_check.append(t2)

                    t3 = ('Height of Stiffener (mm)', '', stiff_height_across_web(self.stiffener_plt_len_across_web,
                                                                                  self.stiffener_plt_height_across_web), 'Pass')
                    self.report_check.append(t3)

                    t4 = ('Thickness of Stiffener (mm)', stiff_thk_across_web(self.thk_req_stiffener_across_web, self.stiffener_plt_len_across_web,
                                                                                self.epsilon, self.column_tw, self.standard_plate_thk[-1]),
                          self.stiffener_plt_thick_across_web,
                          get_pass_fail(max(self.thk_req_stiffener_across_web, self.column_tw), self.stiffener_plt_thick_across_web, relation='leq') and
                          get_pass_fail(self.standard_plate_thk[-1], self.stiffener_plt_thick_across_web, relation='geq'))
                    self.report_check.append(t4)

                    t5 = ('Weld Size (mm)', self.weld_stiffener_across_web.min_size, self.weld_size_stiffener_across_web, 'Pass')
                    self.report_check.append(t5)

                    # if (self.connectivity == 'Welded Column Base') or (self.connectivity == 'Hollow/Tubular Column Base'):
                    #     t5 = ('Max. stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_across_web(self.sigma_web, 0, 0,
                    #                                                                                                        type='welded_hollow_bp',
                    #                                                                                                        case='None'),
                    #           get_pass_fail(self.bearing_strength_concrete, self.sigma_web, relation='geq'))
                    #     self.report_check.append(t5)
                    #
                    # if self.connectivity == 'Moment Base Plate':
                    #
                    #     if (self.moment_bp_case == 'Case2') or (self.moment_bp_case == 'Case3'):
                    #         t5 = ('Max. Stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_across_web(self.sigma_web, 0, 0,
                    #                                                                                                            type='moment_bp',
                    #                                                                                                            case='Case2&3'),
                    #               get_pass_fail(self.bearing_strength_concrete, self.sigma_web, relation='geq'))
                    #         self.report_check.append(t5)
                    #
                    #     else:
                    #         t5 = ('Max. Stress at Stiffener (mm)', self.bearing_strength_concrete, stiffener_stress_across_web(self.sigma_web,
                    #                                                                                                            self.sigma_max_zz,
                    #                                                                                                            self.sigma_min_zz,
                    #                                                                                                            type='moment_bp',
                    #                                                                                                            case='Case1'),
                    #               get_pass_fail(self.bearing_strength_concrete, self.sigma_web, relation='geq'))
                    #         self.report_check.append(t5)
                    #
                    # t6 = ('Shear on Stiffener $(kN)$', shear_demand_stiffener(self.sigma_avg, self.y, self.critical_xx, self.bp_length_provided,
                    #                                                           self.bp_width_provided, self.column_bf, self.shear_on_stiffener_along_flange,
                    #                                                           self.connectivity, self.moment_bp_case, self.anchors_outside_flange,
                    #                                                           location='across_web'),
                    #
                    #       shear_capacity_stiffener(self.stiffener_plt_thick_across_web, self.stiffener_plt_height_across_web, self.stiffener_fy,
                    #                                self.shear_capa_stiffener_across_web, self.gamma_m0, location='across_web'),
                    #
                    #       get_pass_fail(self.shear_on_stiffener_across_web, self.shear_capa_stiffener_across_web, relation='leq'))
                    # self.report_check.append(t6)
                    #
                    # t7 = ('Plastic Section Modulus of Stiffener $(mm^3)$', '', section_modulus_stiffener(self.z_p_stiffener_across_web,
                    #                                                                                    modulus='plastic'), 'N/A')
                    # self.report_check.append(t7)
                    #
                    # t8 = ('Moment on Stiffener $(kNm)$', moment_demand_stiffener(((self.sigma_max_zz + self.sigma_xx) / 2),
                    #                                                             self.stiffener_plt_thick_across_web, self.stiffener_plt_len_across_web,
                    #                                                             self.moment_on_stiffener_across_web, location='across_web'),
                    #       moment_capacity_stiffener(self.z_p_stiffener_across_web, self.stiffener_fy, self.gamma_m0,
                    #                                 self.moment_capa_stiffener_across_web, location='across_web', modulus='elastic'),
                    #       get_pass_fail(self.moment_on_stiffener_across_web, self.moment_capa_stiffener_across_web, relation='leq'))
                    # self.report_check.append(t8)

            # Check 8.2: Stiffener for hollow sections
            if self.connectivity == 'Hollow/Tubular Column Base':

                if (self.stiffener_along_D == 'Yes') or (self.stiffener_along_B == 'Yes'):

                    # if self.dp_column_designation[1:4] == 'CHS' or self.dp_column_designation[1:4] == 'SHS':
                    t1 = ('SubSection', 'Stiffener Design', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                    self.report_check.append(t1)

                    t1 = ('No. of Stiffeners', '', '4', 'OK')
                    self.report_check.append(t1)

                    if self.dp_column_designation[1:4] == 'CHS':
                        t2 = ('Length of Stiffener (mm)', '', stiff_len_chs(self.bp_length_provided, self.column_D, self.stiffener_plt_len_across_D),
                              'OK')

                        t3 = ('Height of Stiffener (mm)', '', stiff_height_chs(self.stiffener_plt_len_across_D, self.stiffener_plt_height), 'OK')

                        t4 = ('Thickness of Stiffener (mm)', stiff_thk_hollow(self.stiffener_plt_len_across_D, self.epsilon, self.stiffener_plt_thk_min,
                                                                                self.column_tf),
                              self.stiffener_plt_thk,
                              get_pass_fail(max(self.stiffener_plt_thk_min, self.column_tf), self.stiffener_plt_thk, relation='leq'))

                        t6 = ('Max. Shear on Stiffener $(kN)$', shear_demand_stiffener(self.sigma_max, 0.0, 0.0, 0.0, self.bp_width_provided,
                                                                                       self.shear_on_stiffener, 'N/A', 'N/A-CHS', 0, 0.0,
                                                                                       self.stiffener_plt_len_across_D, location='hollow_cs'),

                              shear_capacity_stiffener(self.stiffener_plt_thk, self.stiffener_plt_height, self.stiffener_fy, self.shear_capa_stiffener,
                                                       self.gamma_m0, location='hollow_cs'),

                              get_pass_fail(self.shear_on_stiffener, self.shear_capa_stiffener, relation='leq'))

                        t8 = ('Max. Moment on Stiffener $(kNm)$', moment_demand_stiffener(self.shear_on_stiffener, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                                                           self.stiffener_plt_len_across_D, self.moment_on_stiffener,
                                                                                           0.0, 'N/A', 'N/A-CHS', location='hollow_cs'),
                              moment_capacity_stiffener(self.z_e_stiffener, self.stiffener_fy, self.gamma_m0, self.moment_capa_stiffener,
                                                  location='hollow_cs', modulus='elastic'),
                              get_pass_fail(self.moment_on_stiffener, self.moment_capa_stiffener, relation='leq'))
                    else:

                        t2 = ('Length of Stiffener (mm)', '', stiff_len_shs_rhs(self.bp_length_provided, self.bp_width_provided, self.column_D,
                                                                                  self.column_bf, self.stiffener_plt_len_along_D,
                                                                                  self.stiffener_plt_len_along_B), 'OK')

                        t3 = ('Height of Stiffener (mm)', '', stiff_height_shs_rhs(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B,
                                                                                     self.stiffener_plt_len_along_D + 50,
                                                                                     self.stiffener_plt_len_along_B + 50), 'OK')

                        t4 = ('Thickness of Stiffener (mm)', stiff_thk_hollow(max(self.stiffener_plt_len_along_D, self.stiffener_plt_len_along_B),
                                                                                self.epsilon, self.stiffener_plt_thk_min, self.column_tf),
                              self.stiffener_plt_thk,
                              get_pass_fail(max(self.stiffener_plt_thk_min, self.column_tf), self.stiffener_plt_thk, relation='leq'))

                        t6 = ('Max. Shear on Stiffener $(kN)$', shear_demand_stiffener(self.sigma_max, 0.0, 0.0, 0.0, self.bp_width_provided,
                                                                                       self.shear_on_stiffener, 'N/A', 'N/A-CHS', 0, 0.0,
                                                                                       (max(self.stiffener_plt_len_along_D,
                                                                                            self.stiffener_plt_len_along_B)), location='hollow_cs'),
                              shear_capacity_stiffener(self.stiffener_plt_thk, self.stiffener_plt_height, self.stiffener_fy, self.shear_capa_stiffener,
                                                       self.gamma_m0, location='hollow_cs'),
                              get_pass_fail(self.shear_on_stiffener, self.shear_capa_stiffener, relation='leq'))

                        t8 = ('Max. Moment on Stiffener $(kNm)$', moment_demand_stiffener(self.shear_on_stiffener, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                                                           self.stiffener_plt_len_along_D, self.moment_on_stiffener,
                                                                                           0.0, 'N/A', 'N/A-CHS', location='hollow_cs'),
                              moment_capacity_stiffener(self.z_e_stiffener, self.stiffener_fy, self.gamma_m0, self.moment_capa_stiffener,
                                                  location='hollow_cs', modulus='elastic'),
                              get_pass_fail(self.moment_on_stiffener, self.moment_capa_stiffener, relation='leq'))

                    self.report_check.append(t2)
                    self.report_check.append(t3)
                    self.report_check.append(t4)

                    t5 = ('Stress (average) at Stiffener $(N/mm^{2})$', self.bearing_strength_concrete, stiffener_stress(self.sigma_max),
                          get_pass_fail(self.bearing_strength_concrete, self.sigma_max, relation='geq'))
                    self.report_check.append(t5)

                    self.report_check.append(t6)

                    t9 = ('High Shear Check', high_shear_req(self.shear_capa_stiffener),
                          high_shear_provided(self.shear_on_stiffener),
                          get_pass_fail(0.6 * self.shear_capa_stiffener, self.shear_on_stiffener, relation='geq'))
                    self.report_check.append(t9)

                    t7 = ('Section Modulus of the Stiffener $(mm^3)$', '', section_modulus_stiffener(self.z_e_stiffener, modulus='elastic'),
                          'OK')
                    self.report_check.append(t7)

                    self.report_check.append(t8)

                    if (self.dp_column_designation[1:4] == 'SHS') or (self.dp_column_designation[1:4] == 'RHS'):
                        t1 = ('Weld Size (mm)', self.weld_stiffener_SHS.min_size, self.weld_size_stiffener_plt, "Pass")
                    else:
                        t1 = ('Weld Size (mm)', self.weld_stiffener_CHS.min_size, self.weld_size_stiffener_plt, "Pass")
                    self.report_check.append(t1)

            # Check 9: Continuity Plate Design
            if self.connectivity == 'Moment Base Plate':
                if self.stiffener_inside_flange == 'Yes':
                    t1 = ('SubSection', 'Continuity Plate Design', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                    self.report_check.append(t1)

                    t2 = ('Length of Plate (mm)', '', continuity_plate_len_bp(self.stiffener_plt_len_btwn_D_out, self.stiffener_plt_len_btwn_D_in,
                                                                                self.column_D, self.column_tf, self.notch_stiffener_inside_flange),
                          'OK')
                    self.report_check.append(t2)

                    t3 = ('Width of (each) Plate (mm)', '', continuity_plate_width_bp(self.column_bf, self.column_tw, self.notch_stiffener_inside_flange,
                                                                                 self.stiffener_plt_width_btwn_D), 'OK')
                    self.report_check.append(t3)

                    t4 = ('Thickness of Plate (mm)', continuity_plate_thk_req_bp(self.stiffener_plt_thick_btwn_D_1, self.stiffener_plt_thick_btwn_D_2,
                                                                                   self.column_tf, self.stiffener_plt_len_btwn_D_out,
                                                                                   self.stiffener_plt_thick_along_web),
                          continuity_plate_thk_prov_bp(self.stiffener_plt_thick_btwn_D),
                          get_pass_fail(max(self.stiffener_plt_thick_btwn_D_1, self.stiffener_plt_thick_btwn_D_2), self.stiffener_plt_thick_btwn_D,
                                        relation='leq'))
                    self.report_check.append(t4)

                    t3 = ('Weld Size (mm)', round(self.weld_stiffener_key.min_size), self.weld_size_continuity_plate, 'Provide weld at top side')
                    self.report_check.append(t3)

            # Check 10: Shear Design
            if self.load_shear_major or self.load_shear_minor > 0:

                t1 = ('SubSection', 'Shear Design', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t2 = ('Shear Resistance $(kN)$', '', shear_resistance(round(self.load_axial_compression * 10 ** -3, 2), 0.45,
                                                                      round(self.shear_resistance * 1e-3, 2)),
                      'OK')
                self.report_check.append(t2)

                # key along column depth
                if self.shear_key_along_ColDepth == 'Yes':
                    remark_1 = 'Shear key required'
                else:
                    remark_1 = 'Shear key not required'

                t2 = ('Shear Key Requirement - along column depth', shear_load(self.load_shear_major * 1e-3, location='L1'),
                      shear_resistance_check(self.load_shear_major * 1e-3, round(self.shear_resistance * 1e-3, 2), remark_1, location='L1'), remark_1)
                self.report_check.append(t2)

                if self.shear_key_along_ColDepth == 'Yes':
                    t2 = ('Length of Key (mm)', '', key_length(self.shear_key_len_ColDepth, location='L1'), 'Pass')
                    self.report_check.append(t2)

                    t3 = ('Depth of Key (mm)', '', key_depth(self.shear_key_depth_ColDepth, location='L1'), 'Pass')
                    self.report_check.append(t3)

                    t3 = ('Bearing Stress (N/mm$^2$)', self.bearing_strength_concrete, key_bearing_stress(self.load_shear_major,
                                                                                                          round(self.shear_resistance, 2),
                                                                                                        self.shear_key_len_ColDepth,
                                                                                                        self.shear_key_depth_ColDepth,
                                                                                                        self.shear_key_stress_ColDepth, location='L1'),
                          get_pass_fail(self.bearing_strength_concrete, self.shear_key_stress_ColDepth, relation='geq'))
                    self.report_check.append(t3)

                    t3 = ('Moment Demand $(kNm)$', key_moment_demand(self.load_shear_major, round(self.shear_resistance, 2),
                                                                     self.shear_key_len_ColDepth,
                                                                        self.shear_key_w_1, self.shear_key_depth_ColDepth,
                                                                        round(self.shear_key_moment_1 * 1e-3, 2), location='L1'), '', 'OK')
                    self.report_check.append(t3)

                    t4 = ('Thickness of Key (mm)', '', key_thk(self.shear_key_moment_1, self.gamma_m0, self.stiff_key.fy,
                                                                 self.shear_key_depth_ColDepth, self.shear_key_thk_1, self.column_tw, self.shear_key_thk, location='L1'), 'OK')
                    self.report_check.append(t4)

                    t3 = ('Moment Capacity $(kNm)$', round(self.shear_key_moment_1 * 1e-6, 2), key_moment_capacity(self.shear_key_depth_ColDepth,
                                                                                                                  self.shear_key_thk, self.fy_key_1,
                                                                                                                  self.gamma_m0,
                                                                                                                   self.moment_capacity_key1,
                                                                                                                   beta_b=1, location='L1'),
                          get_pass_fail(self.shear_key_moment_1 * 1e-6, self.moment_capacity_key1, relation='leq'))
                    self.report_check.append(t3)

                # key along column width
                if self.shear_key_along_ColWidth == 'Yes':
                    remark_2 = 'Shear key required'
                else:
                    remark_2 = 'Shear key not required'

                t2 = ('Shear Key Requirement - along column width', shear_load(self.load_shear_minor * 1e-3, location='L2'),
                      shear_resistance_check(self.load_shear_minor * 1e-3, round(self.shear_resistance * 1e-3, 2), remark_2, location='L2'), remark_2)
                self.report_check.append(t2)

                if self.shear_key_along_ColWidth == 'Yes':
                    t2 = ('Length of Key (mm)', '', key_length(self.shear_key_len_ColWidth, location='L2'), 'Pass')
                    self.report_check.append(t2)

                    t3 = ('Depth of Key (mm)', '', key_depth(self.shear_key_depth_ColWidth, location='L2'), 'Pass')
                    self.report_check.append(t3)

                    t3 = ('Bearing Stress (N/mm$^2$)', self.bearing_strength_concrete, key_bearing_stress(self.load_shear_minor,
                                                                                                          round(self.shear_resistance, 2),
                                                                                                        self.shear_key_len_ColWidth,
                                                                                                        self.shear_key_depth_ColWidth,
                                                                                                        self.shear_key_stress_ColWidth, location='L2'),
                          get_pass_fail(self.bearing_strength_concrete, self.shear_key_stress_ColWidth, relation='geq'))
                    self.report_check.append(t3)

                    t3 = ('Moment Demand $(kNm)$', key_moment_demand(self.load_shear_minor, round(self.shear_resistance, 2),
                                                                     self.shear_key_len_ColWidth,
                                                                        self.shear_key_w_2, self.shear_key_depth_ColWidth,
                                                                        round(self.shear_key_moment_2 * 1e-3, 2), location='L2'), '', 'OK')
                    self.report_check.append(t3)

                    t4 = ('Thickness of Key (mm)', '', key_thk(self.shear_key_moment_2, self.gamma_m0, self.stiff_key.fy,
                                                                 self.shear_key_depth_ColWidth, self.shear_key_thk_2, self.column_tw,
                                                                 self.shear_key_thk, location='L2'), 'OK')
                    self.report_check.append(t4)

                    t3 = ('Moment Capacity $(kNm)$', round(self.shear_key_moment_2 * 1e-6, 2), key_moment_capacity(self.shear_key_depth_ColWidth,
                                                                                                                    self.shear_key_thk, self.fy_key_2,
                                                                                                                    self.gamma_m0,
                                                                                                                    self.moment_capacity_key2,
                                                                                                                    beta_b=1, location='L2'),
                          get_pass_fail(self.shear_key_moment_2 * 1e-6, self.moment_capacity_key2, relation='leq'))
                    self.report_check.append(t3)

            # Check 11: Weld checks

            if self.connectivity == 'Welded Column Base':
                if self.weld_bp_groove == 'No':

                    t1 = ('SubSection', 'Weld Design - Column to Base Plate Connection', '|p{3.5cm}|p{5.3cm}|p{6.5cm}|p{1.2cm}|')
                    self.report_check.append(t1)

                    t1 = ('Weld Strength (N/mm$^2$)', weld_fu(self.dp_weld_fu_overwrite, self.dp_column_fu), weld_fu_provided(self.weld_fu),
                          get_pass_fail(max(self.dp_weld_fu_overwrite, self.dp_column_fu), self.weld_fu, relation="geq"))
                    self.report_check.append(t1)

                    t1 = ('Total Weld Length - at flange (mm)', "", round(self.weld_len_flange), "Pass")
                    self.report_check.append(t1)

                    t1 = ('Total Weld Length - at web (mm)', "", round(self.weld_len_web), "Pass")
                    self.report_check.append(t1)

                    t1 = ('Weld Size (mm)', self.weld_bp.min_size, self.weld_size_bp, "Pass")
                    self.report_check.append(t1)

            if self.connectivity == 'Moment Base Plate':

                if (self.shear_key_along_ColDepth == 'No') and (self.shear_key_along_ColWidth == 'No'):
                    if self.weld_bp_groove == 'No':

                        t1 = ('SubSection', 'Weld Design - Column Web to Base Plate Connection', '|p{3.5cm}|p{5.3cm}|p{6.5cm}|p{1.2cm}|')
                        self.report_check.append(t1)

                        t1 = ('Weld Strength (N/mm$^2$)', weld_fu(self.dp_weld_fu_overwrite, self.dp_column_fu), weld_fu_provided(self.weld_fu),
                              get_pass_fail(max(self.dp_weld_fu_overwrite, self.dp_column_fu), self.weld_fu, relation="geq"))
                        self.report_check.append(t1)

                        t1 = ('Total Weld Length - at web (mm)', "", round(self.weld_len_web), "Pass")
                        self.report_check.append(t1)

                        t1 = ('Weld Size (mm)', self.weld_bp.min_size, self.weld_size_bp, "Pass")
                        self.report_check.append(t1)

            if self.connectivity == 'Hollow/Tubular Column Base':
                if self.weld_bp_groove == 'No':

                    t1 = ('SubSection', 'Weld Design - Hollow CS to Base Plate Connection', '|p{3.5cm}|p{5.3cm}|p{6.5cm}|p{1.2cm}|')
                    self.report_check.append(t1)

                    t1 = ('Weld Strength (N/mm$^2$)', weld_fu(self.dp_weld_fu_overwrite, self.dp_column_fu), weld_fu_provided(self.weld_fu),
                          get_pass_fail(max(self.dp_weld_fu_overwrite, self.dp_column_fu), self.weld_fu, relation="geq"))
                    self.report_check.append(t1)

                    t1 = ('Total Weld Length (mm)', "", round(self.weld_length), "Pass")
                    self.report_check.append(t1)

                    t1 = ('Weld Size (mm)', self.weld_bp.min_size, self.weld_size_bp, "Pass")
                    self.report_check.append(t1)

        # End of checks

        # typical sketch
        if self.connectivity == 'Moment Base Plate':
            if self.moment_bp_case == 'Case1':
                sketch_path = '/ResourceFiles/images/Moment_BP.png'
            elif self.moment_bp_case == 'Case2':
                sketch_path = '/ResourceFiles/images/Moment_BP_C2.png'
            elif self.moment_bp_case == 'Case3':
                sketch_path = '/ResourceFiles/images/Moment_BP_C3.png'
            else:
                sketch_path = ''
        elif self.connectivity == 'Welded Column Base':
            sketch_path = '/ResourceFiles/images/Welded_BP.png'

        elif self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                sketch_path = '/ResourceFiles/images/SHS_BP.png'
            elif self.dp_column_designation[1:4] == 'RHS':
                sketch_path = '/ResourceFiles/images/RHS_BP.png'
            elif self.dp_column_designation[1:4] == 'CHS':
                sketch_path = '/ResourceFiles/images/CHS_BP.png'
            else:
                sketch_path = ''
        else:
            sketch_path = ''

        # typical detailing
        if self.connectivity == 'Moment Base Plate':
            detailing_path = '/ResourceFiles/images/Moment_BP_Detailing.png'
        elif self.connectivity == 'Welded Column Base':
            detailing_path = '/ResourceFiles/images/Welded_BP_Detailing.png'
        elif self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                detailing_path = '/ResourceFiles/images/SHS_BP_Detailing.png'
            elif self.dp_column_designation[1:4] == 'RHS':
                detailing_path = '/ResourceFiles/images/RHS_BP_Detailing.png'
            elif self.dp_column_designation[1:4] == 'CHS':
                detailing_path = '/ResourceFiles/images/CHS_BP_Detailing.png'
            else:
                detailing_path = ''
        else:
            detailing_path = ''

        # shear key
        if self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                    key_path = '/ResourceFiles/images/Key_SHS.png'
                elif self.shear_key_along_ColDepth == 'Yes':
                    key_path = '/ResourceFiles/images/Key_SHS_D.png'
                elif self.shear_key_along_ColWidth == 'Yes':
                    key_path = '/ResourceFiles/images/Key_SHS_B.png'
                else:
                    key_path = ''
            elif self.dp_column_designation[1:4] == 'RHS':
                if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                    key_path = '/ResourceFiles/images/Key_RHS.png'
                elif self.shear_key_along_ColDepth == 'Yes':
                    key_path = '/ResourceFiles/images/Key_RHS_D.png'
                elif self.shear_key_along_ColWidth == 'Yes':
                    key_path = '/ResourceFiles/images/Key_RHS_B.png'
                else:
                    key_path = ''
            elif self.dp_column_designation[1:4] == 'CHS':
                if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                    key_path = '/ResourceFiles/images/Key_CHS.png'
                elif self.shear_key_along_ColDepth == 'Yes':
                    key_path = '/ResourceFiles/images/Key_CHS_key1.png'
                elif self.shear_key_along_ColWidth == 'Yes':
                    key_path = '/ResourceFiles/images/Key_CHS_key2.png'
                else:
                    key_path = ''
            else:
                key_path = ''
        else:
            if (self.shear_key_along_ColDepth == 'Yes') and (self.shear_key_along_ColWidth == 'Yes'):
                key_path = '/ResourceFiles/images/shear_key.png'
            elif self.shear_key_along_ColDepth == 'Yes':
                key_path = '/ResourceFiles/images/shear_key_colD.png'
            elif self.shear_key_along_ColWidth == 'Yes':
                key_path = '/ResourceFiles/images/shear_key_colB.png'
            else:
                key_path = ''

        # weld details
        if self.connectivity == 'Moment Base Plate':
            if self.weld_bp_groove == 'Yes':
                web_groove_weld = 'Yes'
            else:
                web_groove_weld = 'No'

            if web_groove_weld == 'No':
                if (self.shear_key_along_ColDepth == 'Yes') or (self.shear_key_along_ColWidth == 'Yes'):
                    web_groove_weld = 'Yes'
                else:
                    web_groove_weld = 'No'

            if (self.column_tf < 40.0) and (web_groove_weld == 'No'):
                weld_path = '/ResourceFiles/images/Moment_BP_weld_details_1-1.png'
            elif (self.column_tf < 40.0) and (web_groove_weld == 'Yes'):
                weld_path = '/ResourceFiles/images/Moment_BP_weld_details_1-2.png'
            elif self.column_tf > 40.0:
                weld_path = '/ResourceFiles/images/Moment_BP_weld_details_2.png'

        elif self.connectivity == 'Welded Column Base':
            if self.weld_bp_groove == 'No':
                weld_path = '/ResourceFiles/images/BP_welded_weld_details.png'
            else:
                if self.column_tf < 40.0:
                    weld_path = '/ResourceFiles/images/Welded_BP_single_bevel.png'
                if self.column_tf >= 40.0:
                    weld_path = '/ResourceFiles/images/Welded_BP_double_J.png'
                else:
                    weld_path = '/ResourceFiles/images/BP_welded_weld_details.png'

        elif self.connectivity == 'Hollow/Tubular Column Base':
            if self.dp_column_designation[1:4] == 'SHS':
                if self.weld_bp_groove == 'Yes':
                    weld_path = '/ResourceFiles/images/SHS_BP_groove_weld_details.png'
                else:
                    weld_path = '/ResourceFiles/images/SHS_BP_weld_details.png'
            elif self.dp_column_designation[1:4] == 'RHS':
                if self.weld_bp_groove == 'Yes':
                    weld_path = '/ResourceFiles/images/RHS_BP_groove_weld_details.png'
                else:
                    weld_path = '/ResourceFiles/images/RHS_BP_weld_details.png'
            elif self.dp_column_designation[1:4] == 'CHS':
                if self.weld_bp_groove == 'Yes':
                    weld_path = '/ResourceFiles/images/CHS_BP_groove_weld_details.png'
                else:
                    weld_path = '/ResourceFiles/images/CHS_BP_weld_details.png'
            else:
                weld_path = ''
        else:
            weld_path = ''

        # anchor bolt
        bolt_path = '/ResourceFiles/images/Anchor_bolt.png'

        Disp_2d_image = [sketch_path, detailing_path, weld_path, bolt_path, key_path]
        display_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']

        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext, rel_path, Disp_2d_image,
                               display_3D_image, module=self.module)
