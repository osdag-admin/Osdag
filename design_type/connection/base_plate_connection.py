"""

@Author:    Danish Ansari - Osdag Team, IIT Bombay
@Co-author: Aditya Pawar, Project Intern, MIT College (Aurangabad)


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
from Common import *
from utils.common.load import Load
from utils.common.other_standards import *
import yaml
from design_report.reportGenerator import save_html

import cmath
import time
import os
import shutil
import logging
import pickle
import pdfkit
import configparser
import cairosvg
from io import StringIO

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog, QMessageBox


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

                anchor_dia (str): diameter of the anchor bolt [Ref: IS 5624: 1993, page 5].
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

                dp_anchor_designation (str): designation of the anchor bolt as per IS 5624: 1993, clause 5.
                dp_anchor_type (str): type of the anchor bolt [Ref: IS 5624: 1993, Annex A, clause 4].
                dp_anchor_hole (str): type of hole 'Standard' or 'Over-sized'.
                dp_anchor_fu_overwrite (float): ultimate strength of the anchor bolt corresponding to its grade.
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
        """Initialize all attributes."""
        super(BasePlateConnection, self).__init__()

        # attributes for input dock UI
        self.connectivity = ""
        self.end_condition = ""
        self.column_section = ""
        self.material = ""

        self.load_axial = 0.0
        self.load_shear = 0.0
        self.load_moment_major = 0.0
        self.load_moment_minor = 0.0

        self.anchor_dia = []
        self.anchor_type = ""

        self.footing_grade = 0.0

        # attributes for design preferences
        self.dp_column_designation = ""  # dp for column
        self.dp_column_type = ""
        self.dp_column_source = ""
        self.dp_column_material = ""
        self.dp_column_fu = 0.0
        self.dp_column_fy = 0.0

        self.dp_bp_material = ""  # dp for base plate
        self.dp_bp_fu = 0.0
        self.dp_bp_fy = 0.0

        self.dp_anchor_designation = ""  # dp for anchor bolt
        self.dp_anchor_type = ""
        self.dp_anchor_hole = "Standard"
        self.dp_anchor_length = 0
        self.dp_anchor_fu_overwrite = 0.0
        self.dp_anchor_friction = 0.0

        self.dp_weld_fab = "Shop Weld"  # dp for weld
        self.dp_weld_fu_overwrite = 0.0

        self.dp_detail_edge_type = "b - Machine flame cut"  # dp for detailing
        self.dp_detail_is_corrosive = "No"

        self.dp_design_method = "Limit State Design"  # dp for design
        self.dp_bp_method = "Effective Area Method"

        # other attributes
        self.gamma_m0 = 0.0
        self.gamma_m1 = 0.0
        self.gamma_mb = 0.0
        self.gamma_mw = 0.0

        self.column_properties = Column(designation=self.column_section, material_grade=self.dp_column_material)
        self.column_D = 0.0
        self.column_bf = 0.0
        self.column_tf = 0.0
        self.column_tw = 0.0
        self.column_r1 = 0.0
        self.column_r2 = 0.0

        self.bearing_strength_concrete = 0.0
        self.min_area_req = 0.0
        self.effective_bearing_area = 0.0
        self.projection = 0.0
        self.plate_thk = 0.0
        self.neglect_anchor_dia = []
        self.anchor_dia_provided = 1
        self.anchor_length_min = 1
        self.anchor_length_max = 1
        self.anchor_length_provided = 1
        self.anchor_nos_provided = 0
        self.bp_length_provided = 0.0
        self.bp_width_provided = 0.0
        self.end_distance = 0.0
        self.edge_distance = 0.0
        self.pitch_distance = 0.0
        self.gauge_distance = 0.0
        self.bp_area_provided = 0.0
        self.anchor_grade_provided = 0.0
        self.anchor_area = self.bolt_area(self.table1(self.anchor_dia_provided)[0])  # TODO check if this works
        self.anchor_area_shank = 0.0
        self.anchor_area_thread = 0.0
        self.n_n = 1
        self.n_s = 0
        self.shear_capacity_anchor = 0.0
        self.bearing_capacity_anchor = 0.0
        self.anchor_capacity = 0.0

        self.safe = True

    def set_osdaglogger(key):
        """
        Set logger for Base Plate Module.
        """
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
        handler = OurLog(key)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def module_name(self):
        """
        Call the Base Plate Module key for displaying the module name.
        """
        return KEY_DISP_BASE_PLATE

    def input_values(self, existingvalues={}):
        """
        Return a-list of tuple, used to create the Base Plate input dock U.I in Osdag design window.
        """
        self.module = KEY_DISP_BASE_PLATE

        options_list = []

        if KEY_DISP_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_DISP_CONN]
        else:
            existingvalue_key_conn = ''

        if KEY_SUPTNGSEC in existingvalues:  # this might not be required
            existingvalue_key_suptngsec = existingvalues[KEY_SUPTNGSEC]
        else:
            existingvalue_key_suptngsec = ''

        if KEY_SUPTDSEC in existingvalues:
            existingvalue_key_suptdsec = existingvalues[KEY_SUPTDSEC]
        else:
            existingvalue_key_suptdsec = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_AXIAL in existingvalues:
            existingvalue_key_axial = existingvalues[KEY_AXIAL]
        else:
            existingvalue_key_axial = ''

        if KEY_MOMENT in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_MOMENT]
        else:
            existingvalue_key_versh = ''

        if KEY_SHEAR in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_SHEAR]
        else:
            existingvalue_key_versh = ''

        if KEY_DIA_ANCHOR in existingvalues:
            existingvalue_key_d = existingvalues[KEY_DIA_ANCHOR]
        else:
            existingvalue_key_d = ''

        # if KEY_TYP in existingvalues:
        #     existingvalue_key_typ = existingvalues[KEY_TYP]
        # else:
        #     existingvalue_key_typ = ''

        # if KEY_GRD in existingvalues:
        #     existingvalue_key_grd = existingvalues[KEY_GRD]
        # else:
        #     existingvalue_key_grd = ''

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_MODULE, KEY_DISP_BASE_PLATE, TYPE_MODULE, None, None)
        options_list.append(t2)

        t3 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN_BP)
        options_list.append(t3)

        t4 = (KEY_IMAGE, None, TYPE_IMAGE, None, "./ResourceFiles/images/base_plate.png")
        options_list.append(t4)

        t5 = (KEY_END_CONDITION, KEY_DISP_END_CONDITION, TYPE_NOTE, existingvalue_key_conn, 'Pinned')
        options_list.append(t5)

        t6 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec,
              connectdb("Columns"))  # this might not be required
        options_list.append(t6)

        # t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, connectdb("Columns"))
        # options_list.append(t4)

        t7 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t7)

        t8 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t8)

        t9 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None)
        options_list.append(t9)

        t10 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None)
        options_list.append(t10)

        t11 = (KEY_MOMENT, KEY_DISP_MOMENT, '', existingvalue_key_axial, None)
        options_list.append(t11)

        t12 = (KEY_MOMENT_MAJOR, KEY_DISP_MOMENT_MAJOR, TYPE_TEXTBOX, existingvalue_key_conn, None)
        options_list.append(t12)

        t13 = (KEY_MOMENT_MINOR, KEY_DISP_MOMENT_MINOR, TYPE_TEXTBOX, existingvalue_key_conn, None)
        options_list.append(t13)

        t14 = (None, DISP_TITLE_ANCHOR_BOLT, TYPE_TITLE, None, None)
        options_list.append(t14)

        t15 = (KEY_DIA_ANCHOR, KEY_DISP_DIA_ANCHOR, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_DIA_ANCHOR)
        options_list.append(t15)

        t16 = (KEY_TYP_ANCHOR, KEY_DISP_TYP_ANCHOR, TYPE_COMBOBOX, existingvalue_key_d, VALUES_TYP_ANCHOR)
        options_list.append(t16)

        t17 = (None, DISP_TITLE_FOOTING, TYPE_TITLE, None, None)
        options_list.append(t17)

        t18 = (KEY_GRD_FOOTING, KEY_DISP_GRD_FOOTING, TYPE_COMBOBOX, existingvalue_key_d, VALUES_GRD_FOOTING)
        options_list.append(t18)

        # t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        # options_list.append(t11)

        # t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        # options_list.append(t12)

        # t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        # options_list.append(t13)

        # t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        # options_list.append(t14)

        return options_list

    def output_values(self, flag):
        return []

    def major_minor(self):
        if self in ['Bolted-Slab Base', 'Gusseted Base Plate', 'Hollow Section']:
            return True
        else:
            return False

    def end_condition(self):
        if self in ['Gusseted Base Plate', 'Hollow Section']:
            return 'Fixed'
        else:
            return 'Pinned'

    def input_value_changed(self):

        lst = []

        t1 = (KEY_CONN, KEY_MOMENT_MAJOR, TYPE_TEXTBOX, self.major_minor)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_MOMENT_MINOR, TYPE_TEXTBOX, self.major_minor)
        lst.append(t2)

        t3 = (KEY_CONN, KEY_END_CONDITION, TYPE_NOTE, self.end_condition)
        lst.append(t3)

        return lst

    @staticmethod
    def diam_bolt_customized():
        c = connectdb2()
        return c

    def customized_input(self):

        list1 = []
        t1 = (KEY_DIA_ANCHOR, self.diam_bolt_customized)
        list1.append(t1)

        return list1

    def func_for_validation(self, window, design_dictionary):
        self.design_status = False
        flag = False
        option_list = self.input_values(self)
        missing_fields_list = []
        if design_dictionary[KEY_CONN] == 'Welded-Slab Base':
            design_dictionary[KEY_MOMENT_MAJOR] = 'Disabled'
            design_dictionary[KEY_MOMENT_MINOR] = 'Disabled'
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) > 0:
            QMessageBox.information(window, "Information",
                                    generate_missing_fields_error_string(missing_fields_list))
            # flag = False
        else:
            flag = True

        if flag:
            print(design_dictionary)
            # self.set_input_values(self, design_dictionary)
            self.bp_parameters(self, design_dictionary)
        else:
            pass

    def tab_list(self):
        tabs = []

        t0 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_column_section)
        tabs.append(t0)

        t5 = ("Base Plate", TYPE_TAB_2, self.tab_bp)
        tabs.append(t5)

        t1 = ("Anchor Bolt", TYPE_TAB_2, self.anchor_bolt_values)
        tabs.append(t1)

        t2 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t2)

        t3 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t3)

        t4 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t4)

        # t5 = ("Connector", TYPE_TAB_2, self.connector_values)
        # tabs.append(t5)

        return tabs

    @staticmethod
    def anchor_bolt_values():
        anchor_bolt = []

        t1 = (KEY_DP_ANCHOR_BOLT_DESIGNATION, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, '')
        anchor_bolt.append(t1)

        t2 = (KEY_DP_ANCHOR_BOLT_TYPE, KEY_DISP_DP_ANCHOR_BOLT_TYPE, TYPE_COMBOBOX, VALUES_TYP_ANCHOR)
        anchor_bolt.append(t2)

        t3 = (KEY_DP_ANCHOR_BOLT_GALVANIZED, KEY_DISP_DP_ANCHOR_BOLT_GALVANIZED, TYPE_COMBOBOX, ['Yes', 'No'])
        anchor_bolt.append(t3)

        t4 = (
            KEY_DP_ANCHOR_BOLT_HOLE_TYPE, KEY_DISP_DP_ANCHOR_BOLT_HOLE_TYPE, TYPE_COMBOBOX, ['Standard', 'Over-sized'])
        anchor_bolt.append(t4)

        t5 = (KEY_DP_ANCHOR_BOLT_LENGTH, KEY_DISP_DP_ANCHOR_BOLT_LENGTH, TYPE_TEXTBOX, '')
        anchor_bolt.append(t5)

        t6 = (KEY_DP_ANCHOR_BOLT_MATERIAL_G_O, KEY_DISP_DP_ANCHOR_BOLT_MATERIAL_G_O, TYPE_TEXTBOX, '')
        anchor_bolt.append(t6)

        t7 = (KEY_DP_ANCHOR_BOLT_FRICTION, KEY_DISP_DP_ANCHOR_BOLT_FRICTION, TYPE_TEXTBOX, '0.30')
        anchor_bolt.append(t7)

        return anchor_bolt

    @staticmethod
    def tab_bp():
        tab_bp = []
        t1 = (KEY_BASE_PLATE_MATERIAL, KEY_DISP_MATERIAL, TYPE_TEXTBOX, None)
        tab_bp.append(t1)

        t2 = (KEY_BASE_PLATE_FU, KEY_DISP_BASE_PLATE_FU, TYPE_TEXTBOX, None)
        tab_bp.append(t2)

        t3 = (KEY_BASE_PLATE_FY, KEY_DSIP_BASE_PLATE_FY, TYPE_TEXTBOX, None)
        tab_bp.append(t3)

        return tab_bp

    @staticmethod
    def detailing_values():
        detailing = []

        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX, [
            'a - Sheared or hand flame cut', 'b - Rolled, machine-flame cut, sawn and planed'])
        detailing.append(t1)

        t3 = (KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES, TYPE_COMBOBOX,
              ['No', 'Yes'])
        detailing.append(t3)

        t4 = ["textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION]
        detailing.append(t4)

        return detailing

    @staticmethod
    def design_values():

        design = []

        t1 = (KEY_DP_DESIGN_METHOD, KEY_DISP_DP_DESIGN_METHOD, TYPE_COMBOBOX, ['Limit State Design',
                                                                               'Limit State (Capacity based) Design',
                                                                               'Working Stress Design'])
        design.append(t1)

        t2 = (KEY_DP_DESIGN_BASE_PLATE, KEY_DISP_DP_DESIGN_BASE_PLATE, TYPE_COMBOBOX, ['Effective Area Method'])
        design.append(t2)

        return design

    @staticmethod
    def tab_column_section():
        supporting_section = []
        t1 = (KEY_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_DESIGNATION, TYPE_TEXTBOX, None)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
        supporting_section.append(t2)

        # material = connectdb("Material", call_type="popup")
        # material.append('Custom')
        t34 = (KEY_SUPTNGSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_TEXTBOX, None)
        supporting_section.append(t34)

        # t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None)
        # supporting_section.append(t3)

        # t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None)
        # supporting_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None)
        supporting_section.append(t5)

        t6 = (KEY_SUPTNGSEC_DEPTH, KEY_DISP_SUPTNGSEC_DEPTH, TYPE_TEXTBOX, None)
        supporting_section.append(t6)

        t7 = (KEY_SUPTNGSEC_FLANGE_W, KEY_DISP_SUPTNGSEC_FLANGE_W, TYPE_TEXTBOX, None)
        supporting_section.append(t7)

        t8 = (KEY_SUPTNGSEC_FLANGE_T, KEY_DISP_SUPTNGSEC_FLANGE_T, TYPE_TEXTBOX, None)
        supporting_section.append(t8)

        t9 = (KEY_SUPTNGSEC_WEB_T, KEY_DISP_SUPTNGSEC_WEB_T, TYPE_TEXTBOX, None)
        supporting_section.append(t9)

        t10 = (KEY_SUPTNGSEC_FLANGE_S, KEY_DISP_SUPTNGSEC_FLANGE_S, TYPE_TEXTBOX, None)
        supporting_section.append(t10)

        t11 = (KEY_SUPTNGSEC_ROOT_R, KEY_DISP_SUPTNGSEC_ROOT_R, TYPE_TEXTBOX, None)
        supporting_section.append(t11)

        t12 = (KEY_SUPTNGSEC_TOE_R, KEY_DISP_SUPTNGSEC_TOE_R, TYPE_TEXTBOX, None)
        supporting_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None)
        supporting_section.append(t13)

        t14 = (KEY_SUPTNGSEC_TYPE, KEY_DISP_SUPTNGSEC_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'])
        supporting_section.append(t14)

        # t18 = (None, None, TYPE_ENTER, None)
        # supporting_section.append(t18)

        t18 = (None, None, TYPE_ENTER, None)
        supporting_section.append(t18)

        t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None)
        supporting_section.append(t3)

        # t15 = (KEY_SUPTNGSEC_MOD_OF_ELAST, KEY_SUPTNGSEC_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None)
        # supporting_section.append(t15)
        #
        # t16 = (KEY_SUPTNGSEC_MOD_OF_RIGID, KEY_SUPTNGSEC_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None)
        # supporting_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None)
        supporting_section.append(t17)

        t18 = (KEY_SUPTNGSEC_MASS, KEY_DISP_SUPTNGSEC_MASS, TYPE_TEXTBOX, None)
        supporting_section.append(t18)

        t19 = (KEY_SUPTNGSEC_SEC_AREA, KEY_DISP_SUPTNGSEC_SEC_AREA, TYPE_TEXTBOX, None)
        supporting_section.append(t19)

        t20 = (KEY_SUPTNGSEC_MOA_LZ, KEY_DISP_SUPTNGSEC_MOA_LZ, TYPE_TEXTBOX, None)
        supporting_section.append(t20)

        t21 = (KEY_SUPTNGSEC_MOA_LY, KEY_DISP_SUPTNGSEC_MOA_LY, TYPE_TEXTBOX, None)
        supporting_section.append(t21)

        t22 = (KEY_SUPTNGSEC_ROG_RZ, KEY_DISP_SUPTNGSEC_ROG_RZ, TYPE_TEXTBOX, None)
        supporting_section.append(t22)

        t23 = (KEY_SUPTNGSEC_ROG_RY, KEY_DISP_SUPTNGSEC_ROG_RY, TYPE_TEXTBOX, None)
        supporting_section.append(t23)

        t24 = (KEY_SUPTNGSEC_EM_ZZ, KEY_DISP_SUPTNGSEC_EM_ZZ, TYPE_TEXTBOX, None)
        supporting_section.append(t24)

        t25 = (KEY_SUPTNGSEC_EM_ZY, KEY_DISP_SUPTNGSEC_EM_ZY, TYPE_TEXTBOX, None)
        supporting_section.append(t25)

        t26 = (KEY_SUPTNGSEC_PM_ZPZ, KEY_DISP_SUPTNGSEC_PM_ZPZ, TYPE_TEXTBOX, None)
        supporting_section.append(t26)

        t27 = (KEY_SUPTNGSEC_PM_ZPY, KEY_DISP_SUPTNGSEC_PM_ZPY, TYPE_TEXTBOX, None)
        supporting_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None)
        supporting_section.append(t28)

        t29 = (KEY_SUPTNGSEC_SOURCE, KEY_DISP_SUPTNGSEC_SOURCE, TYPE_TEXTBOX, None)
        supporting_section.append(t29)

        # t30 = (None, None, TYPE_ENTER, None)
        # supporting_section.append(t30)

        t30 = (None, None, TYPE_ENTER, None)
        supporting_section.append(t30)

        t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_SUPTNGSEC_FY, TYPE_TEXTBOX, None)
        supporting_section.append(t4)

        # t31 = (KEY_SUPTNGSEC_POISSON_RATIO, KEY_DISP_SUPTNGSEC_POISSON_RATIO, TYPE_TEXTBOX, None)
        # supporting_section.append(t31)
        #
        # t32 = (KEY_SUPTNGSEC_THERMAL_EXP, KEY_DISP_SUPTNGSEC_THERMAL_EXP, TYPE_TEXTBOX, None)
        # supporting_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None)
        supporting_section.append(t33)

        return supporting_section

    # def dia_to_len(self, d):
    #
    #     ob = IS_5624_1993()
    #     l = ob.table1(d)
    #     return l

    # Start of calculation

    def bp_parameters(self, design_dictionary):
        """ Initialize variables to use in calculation from input dock and design preference UI.

        Args: design dictionary based on the user inputs from the GUI

        Returns: None
        """
        # attributes of input dock
        self.connectivity = str(design_dictionary[KEY_CONN])
        self.end_condition = str(design_dictionary[KEY_END_CONDITION])
        self.column_section = str(design_dictionary[KEY_SUPTNGSEC])
        self.material = str(design_dictionary[KEY_MATERIAL])

        self.load_axial = float(design_dictionary[KEY_AXIAL])
        self.load_shear = float(design_dictionary[KEY_SHEAR])
        self.load_moment_major = float(design_dictionary[KEY_MOMENT_MAJOR] if design_dictionary[KEY_MOMENT_MAJOR] != 'Disabled' else 0)
        self.load_moment_minor = float(design_dictionary[KEY_MOMENT_MINOR] if design_dictionary[KEY_MOMENT_MINOR] != 'Disabled' else 0)

        self.anchor_dia = design_dictionary[KEY_DIA_ANCHOR]
        self.anchor_type = str(design_dictionary[KEY_TYP_ANCHOR])

        self.footing_grade = str(design_dictionary[KEY_GRD_FOOTING])

        # attributes of design preferences
        self.dp_column_designation = str(design_dictionary[KEY_SUPTNGSEC])
        self.dp_column_type = str(design_dictionary[KEY_SUPTNGSEC_TYPE])
        self.dp_column_source = str(design_dictionary[KEY_SUPTNGSEC_SOURCE])
        self.dp_column_material = str(design_dictionary[KEY_SUPTNGSEC_MATERIAL])
        self.dp_column_fu = float(design_dictionary[KEY_SUPTNGSEC_FU])
        self.dp_column_fy = float(design_dictionary[KEY_SUPTNGSEC_FY])

        self.dp_bp_material = str(design_dictionary[KEY_BASE_PLATE_MATERIAL])
        self.dp_bp_fu = float(design_dictionary[KEY_BASE_PLATE_FU])
        self.dp_bp_fy = float(design_dictionary[KEY_BASE_PLATE_FY])

        self.dp_anchor_designation = str(design_dictionary[KEY_DP_ANCHOR_BOLT_DESIGNATION])
        self.dp_anchor_type = str(design_dictionary[KEY_DP_ANCHOR_BOLT_TYPE])
        self.dp_anchor_hole = str(design_dictionary[KEY_DP_ANCHOR_BOLT_HOLE_TYPE])
        self.dp_anchor_length = int(design_dictionary[KEY_DP_ANCHOR_BOLT_LENGTH])
        self.dp_anchor_fu_overwrite = float(design_dictionary[KEY_DP_ANCHOR_BOLT_MATERIAL_G_O])
        self.dp_anchor_friction = float(design_dictionary[KEY_DP_ANCHOR_BOLT_FRICTION] if
                                        design_dictionary[KEY_DP_ANCHOR_BOLT_FRICTION] != "" else 0.30)

        self.dp_weld_fab = str(design_dictionary[KEY_DP_WELD_FAB])
        self.dp_weld_fu_overwrite = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])

        self.dp_detail_edge_type = str(design_dictionary[KEY_DP_DETAILING_EDGE_TYPE])
        self.dp_detail_is_corrosive = str(design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        self.dp_design_method = str(design_dictionary[KEY_DP_DESIGN_METHOD])
        self.dp_bp_method = str(design_dictionary[KEY_DP_DESIGN_BASE_PLATE])

        # other attributes
        self.gamma_m0 = 1.10
        self.gamma_m1 = 1.25
        self.gamma_mb = 1.25
        if self.dp_weld_fab == 'Shop Weld':
            self.gamma_mw = 1.25
        else:
            self.gamma_mw = 1.50

        self.safe = True

    def design_pinned_bp_welded(self):
        """ design pinned base plate (welded connection)

        Args:

        Returns:
        """
        self.bearing_strength_concrete = self.cl_7_4_1_bearing_strength_concrete(self.footing_grade)  # N/mm^2 (MPa)
        self.min_area_req = self.load_axial / self.bearing_strength_concrete  # mm^2

        # TODO: add calculation of projection for other type(s) of column section (example: tubular)
        if self.dp_column_type == 'Rolled' or 'Welded':
            self.projection = self.calculate_c(self.flange_width, self.depth, self.web_thickness, self.flange_thickness,
                                               self.min_area_req)
        else:
            pass

        if self.projection <= 0:
            self.safe = False
            logger.error(": [Analysis Error] The value of the projection (c) as per the Effective Area Method is {}. [Reference:"
                         " Clause 7.4.1.1, IS 800: 2007]".format(self.projection))
            logger.error(": [Analysis Error] The computed value of the projection occurred out of range.")
            logger.info(": [Analysis Error] Check the column section and its properties.")
            logger.info(": Re-design the connection")
        else:
            pass

        #  Reference: Clause 7.4.3.1, IS 800:2007
        self.plate_thk = max(self.projection * (math.sqrt((2.5 * self.bearing_strength_concrete * self.gamma_m0) / self.dp_bp_fy)),
                             self.flange_thickness)  # base plate thickness should be larger than the flange thickness
        self.plate_thk = round_up(self.plate_thk, 2)  # mm TODO check standard plate thk output

    def bolt_design_detailing(self):
        """ Perform design and detailing of the anchor bolt

        Args:

        Returns:
        """
        # design/assigning of anchor bolt diameter [Reference: based on design experience and sample calculations]
        self.neglect_anchor_dia = ['M8', 'M10', 'M12', 'M16']  # the listed diameters are neglected due its practical non acceptance

        for i in list(self.anchor_dia):
            if i in self.neglect_anchor_dia:
                self.anchor_dia.remove(i)
            else:
                pass
        self.anchor_dia_provided = self.anchor_dia[0]  # providing the least diameter anchor bolt from the resulting list (mm)

        # number of anchor bolts
        self.anchor_nos_provided = 4  # TODO add condition for number of anchor bolts depending on col depth and force

        # perform detailing checks
        self.end_distance = self.cl_10_2_4_2_min_edge_end_dist(self.table1(self.anchor_dia_provided)[0],
                                                               self.dp_anchor_hole, self.dp_detail_edge_type)

        # Note: end distance is along the depth, whereas, the edge distance is along the flange of the column section
        self.end_distance = round_up(self.end_distance, 5) + 10  # adding 10 mm extra for a conservative design # mm
        self.edge_distance = self.end_distance  # mm

        if self. anchor_nos_provided == 4:
            self.pitch_distance = 0.0
            self.gauge_distance = self.pitch_distance
        else:
            pass  # TODO add pitch and gauge calc for bolts more than 4 nos

        # design strength of anchor bolt [Reference: Clause 10.3.2, IS 800:2007]
        self.anchor_grade_provided = 0.0  # TODO call from UI - Umair
        # self.anchor_area = self.bolt_area(self.table1(self.anchor_dia_provided)[0])  # returns a list [shank area, thread area]
        self.anchor_area_shank = self.anchor_area[0]  # mm^2
        self.anchor_area_thread = self.anchor_area[1]  # mm^2
        self.n_n = 1
        self.n_s = 0

        self.shear_capacity_anchor = self.cl_10_3_3_bolt_shear_capacity(self.dp_anchor_fu_overwrite, self.anchor_area_thread,
                                                                        self.anchor_area_shank, self.n_n, self.n_s, self.gamma_mb)
        self.bearing_capacity_anchor = self.cl_10_3_4_bolt_bearing_capacity(self.dp_bp_fu, self.dp_anchor_fu_overwrite,
                                                                            self.plate_thk, self.table1(self.anchor_dia_provided)[0],
                                                                            self.end_distance, self.pitch_distance, self.dp_anchor_hole,
                                                                            self.gamma_mb)
        self.shear_capacity_anchor = round(self.shear_capacity_anchor / 1000, 2)  # kN
        self.bearing_capacity_anchor = round(self.bearing_capacity_anchor / 1000, 2)  # kN

        self.anchor_capacity = min(self.shear_capacity_anchor, self.bearing_capacity_anchor)

        if self.load_shear > 0:
            logger.info(": [Anchor Bolt] The anchor bolt is not designed to resist any shear force")
        else:
            pass

        # design of anchor bolt length [Reference: IS 5624:1993, Table 1]
        self.anchor_length_min = self.table1(self.anchor_dia_provided)[1]
        self.anchor_length_max = self.table1(self.anchor_dia_provided)[2]
        self.anchor_length_provided = self.anchor_length_min

        logger.info(": [Anchor Bolt] The preferred range of length for anchor bolt of thread size {} is as follows:"
                    .format(self.anchor_dia_provided))
        logger.info(": [Anchor Bolt] Minimum length = {} mm, Maximum length = {} mm."
                    .format(self.anchor_length_min, self.anchor_length_max))
        logger.info(": [Anchor Bolt] The provided length of the anchor bolt is {} mm".format(self.anchor_length_provided))
        logger.info(": [Anchor Bolt] Designer/Erector should provide adequate anchorage depending on the availability "
                    "of standard lengths and sizes, satisfying the suggested range.")
        logger.info(": [Anchor Bolt] Reference: IS 5624:1993, Table 1.")

    def design_detail_bp(self):
        """ Design base plate dimensions and provide detailing

        Args:

        Returns:
        """
        if self.connectivity == 'Welded-Slab Base':
            self.bp_length_provided = self.depth + self.projection + self.end_distance  # mm
            self.bp_width_provided = self.flange_width + self.projection + self.edge_distance  # mm
        else:
            pass

        # check for the provided area
        self.bp_area_provided = self.bp_length_provided * self.bp_width_provided  # mm^2
        if self.bp_area_provided < self.min_area_req:
            self.safe = False
            logger.error("[Base Plate] The calculated area of the base plate is less than the required area.")
            logger.warning("[Base Plate] Cannot compute the required area of the base plate.")
            logger.info("[Base Plate] Check the input values and re-design the connection.")
        else:
            pass

        # end of calculation
        if self.safe:
            logger.info(": Overall base plate connection design is safe")
            logger.debug(": =========End Of design===========")
        else:
            logger.info(": Overall base plate connection design is unsafe")
            logger.debug(": =========End Of design===========")




